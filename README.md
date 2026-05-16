<h1 align="center">
Voice-Pro (Colab-Optimized Fork)
</h1>

<p align="center">
  <i>Bản sao siêu nhẹ của Voice-Pro, được tinh chỉnh đặc biệt để chạy mượt mà trên Google Colab với sự hỗ trợ F5-TTS Tiếng Việt.</i>
</p>

---

## 🚀 Giới thiệu

Đây là phiên bản **Fork đã được "ép cân" (De-bloated)** từ dự án gốc [Voice-Pro](https://github.com/abus-aikorea/voice-pro) của ABUS. 

Phiên bản này được tạo ra nhằm mục đích **chạy hoàn hảo trên Google Colab (GPU T4)**, với thời gian cài đặt siêu nhanh và không gặp các lỗi xung đột thư viện. 

**Những thay đổi chính so với bản gốc:**
- 🗑️ **Lược bỏ thành phần nặng:** Đã xóa bỏ các thư viện cồng kềnh như CosyVoice, Kokoro, WhisperX, OpenAI Whisper. Chỉ giữ lại **faster-whisper** (bộ nhận diện nhanh nhất hiện nay).
- 🇻🇳 **Hỗ trợ Tiếng Việt:** Tích hợp sẵn mô hình **F5-TTS Tiếng Việt** (`hynt/F5-TTS-Vietnamese-ViVoice`) để lồng tiếng chuẩn giọng Việt Nam.
- 🛠️ **Vá lỗi tự động:** Tự động hạ cấp `pip`, cài đặt đúng phiên bản `cuDNN` và `setuptools` để chạy trơn tru trên môi trường Colab.
- ⚡ **Nhẹ và Nhanh:** Rút ngắn thời gian khởi động, giải phóng hàng chục GB dung lượng đĩa cứng trên máy ảo.

---

## ⭐ Các tính năng chính

1. **Tải và Xử lý Video:** Tải trực tiếp từ YouTube và tự động tách âm thanh/giọng nói bằng **Demucs**.
2. **Nhận diện giọng nói (ASR):** Sử dụng **faster-whisper** cho tốc độ dịch siêu tốc với độ chính xác cao.
3. **Dịch thuật:** Dịch phụ đề sang hơn 100 ngôn ngữ khác nhau.
4. **Lồng tiếng (TTS):** 
   - **F5-TTS (Zero-shot Voice Cloning):** Nhân bản giọng nói chỉ với 3-10 giây âm thanh mẫu (hỗ trợ Tiếng Việt).
   - **Edge-TTS:** Hỗ trợ giọng đọc chất lượng cao từ Microsoft.

---

## 💻 Hướng dẫn chạy trên Google Colab

Chỉ với 1 ô lệnh (Code Cell) duy nhất trên Google Colab (Nhớ chọn Runtime là **T4 GPU**), dự án sẽ tự động cài đặt và cấp cho bạn một đường link Public Web UI.

```bash
# 1. Clone phiên bản đã tối ưu này về Colab
!git clone https://github.com/TEN_GITHUB_CUA_BAN/voice-pro.git

# 2. Di chuyển vào thư mục dự án
%cd voice-pro

# 3. Đổi biến môi trường matplotlib về agg để tắt tính năng vẽ đồ thị inline của Colab
%env MPLBACKEND=agg

# 4. Chạy phần mềm
!bash start.sh
```

*(Lưu ý: Thay `TEN_GITHUB_CUA_BAN` bằng username GitHub thực tế của bạn sau khi bạn tải repo này lên).*

---

## 🙏 Credits & Giấy phép

* **Tác giả gốc:** [ABUS](https://github.com/abus-aikorea/voice-pro) - Vui lòng ủng hộ và thả sao (Star) cho tác giả gốc nếu bạn thấy phần mềm này hữu ích.
* **Giấy phép:** [GNU General Public License v3.0 (GPLv3)](LICENSE)
* **Các thư viện mã nguồn mở:** faster-whisper, F5-TTS, gradio, yt-dlp, demucs.
