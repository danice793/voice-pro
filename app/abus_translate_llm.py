import gradio as gr
import pysubs2
import gc
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from app.abus_genuine import *
from app.abus_path import *
from app.abus_text import *
from app.abus_nlp_spacy import *

import structlog
logger = structlog.get_logger()

class QwenTranslator:
    def __init__(self, model_id="Qwen/Qwen3-4B-Instruct-2507"):
        self.model_id = model_id
        self.tokenizer = None
        self.model = None

    def get_languages(self) -> list:
        return ["Vietnamese", "English", "Korean", "Japanese", "Chinese"]
        
    def get_language_code(self, language_name) -> str:
        # Giữ interface giống các Translator khác
        return language_name

    def load_model(self):
        if self.model is None:
            logger.info(f"Loading Qwen LLM from {self.model_id}...")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_id,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                device_map="auto"
            )
            logger.info("Model loaded successfully.")

    def release_model(self):
        if self.model is not None:
            logger.info("Releasing Qwen LLM from memory...")
            del self.model
            del self.tokenizer
            self.model = None
            self.tokenizer = None
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()

    def translate_file(self, source_lang: str, target_lang: str, subtitle_file_path: str, output_file_path: str, progress=gr.Progress()):
        tts_source_file = path_add_postfix(subtitle_file_path, f"-{source_lang}", ".srt")
        AbusSpacy.process_subtitle_for_tts(subtitle_file_path, tts_source_file)
        
        full_subs = pysubs2.load(tts_source_file)
        subs = full_subs

        self.load_model()
        
        for event in progress.tqdm(subs, desc='Translating with Qwen...'):
            if not event.text:
                continue
            
            text = event.plaintext
            duration_sec = (event.end - event.start) / 1000.0
            
            # System prompt for strict summarization & translation
            prompt = (
                f"You are a professional translator and dubbing assistant. "
                f"Translate the following text to {target_lang}. "
                f"CRITICAL REQUIREMENT: The translated text must be extremely concise so that it takes about {duration_sec:.1f} seconds to speak out loud. "
                f"Only output the translated text, do NOT explain, do NOT include quotes."
            )

            messages = [
                {"role": "system", "content": prompt},
                {"role": "user", "content": text}
            ]

            try:
                text_input = self.tokenizer.apply_chat_template(
                    messages,
                    tokenize=False,
                    add_generation_prompt=True
                )
                model_inputs = self.tokenizer([text_input], return_tensors="pt").to(self.model.device)

                generated_ids = self.model.generate(
                    **model_inputs,
                    max_new_tokens=512
                )
                generated_ids = [
                    output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
                ]

                translated_text = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
                
                if translated_text:
                    event.text = translated_text
                    logger.debug(f"[Qwen] Original ({duration_sec:.1f}s): {text}")
                    logger.debug(f"[Qwen] Translated: {translated_text}")
                else:
                    logger.warning(f"[Qwen] Empty translation for: {text}")

            except Exception as e:
                logger.error(f"Translation error for text '{text}': {e}")

        subs.save(output_file_path)   
        cmd_delete_file(tts_source_file)
        
        self.release_model()

    def translate_text(self, source_lang: str, target_lang: str, text: str, progress=gr.Progress()) -> str:
        self.load_model()
        prompt = (
            f"You are a professional translator. Translate the following text to {target_lang}. "
            f"Only output the translated text, no explanations."
        )
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": text}
        ]
        try:
            text_input = self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )
            model_inputs = self.tokenizer([text_input], return_tensors="pt").to(self.model.device)

            generated_ids = self.model.generate(
                **model_inputs,
                max_new_tokens=1024
            )
            generated_ids = [
                output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
            ]

            translated_text = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
            self.release_model()
            return translated_text
        except Exception as e:
            logger.error(f"Text translation error: {e}")
            self.release_model()
            return text
