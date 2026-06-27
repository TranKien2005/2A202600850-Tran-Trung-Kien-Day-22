# Hướng Dẫn Từng Bước Thực Hiện & Nộp Bài Lab 22 (DPO Alignment)

Chào bạn! Do máy tính cá nhân của bạn hiện không hỗ trợ GPU NVIDIA đủ khỏe để chạy Unsloth và DPO cục bộ, bài lab này đã được thiết lập sẵn sàng để **chạy hoàn toàn trên Google Colab T4 miễn phí**. Mọi thay đổi code giải đã được tích hợp sẵn vào file notebook stitched: `colab/Lab22_DPO_T4.ipynb`.

Hãy làm theo các bước chi tiết sau đây để hoàn thành bài lab và đạt điểm số tối đa:

---

## Bước 1: Lưu mã nguồn lên GitHub cá nhân của bạn

1. Tôi đã cập nhật đầy đủ mã nguồn và các file cấu hình cần thiết trực tiếp trong thư mục dự án cục bộ của bạn.
2. Bạn hãy commit các thay đổi này và push lên một repository **Công khai (Public)** của riêng bạn trên GitHub.
   - Ví dụ repository của bạn: `https://github.com/huyvanzzz/2A202600773-Nguyen-Van-Huy-Day22-Track3-DPO-Alignment-Lab`

---

## Bước 2: Khởi chạy trên Google Colab

1. Truy cập trực tiếp link mở Colab bằng cách click vào badge **"Open T4 in Colab"** ở đầu file [README.md](file:///d:/Vin/2A202600773-Nguyen-Van-Huy-Day22-Track3-DPO-Alignment-Lab/README.md) của repository của bạn (sau khi đã push).
2. Hoặc mở trực tiếp trang [Google Colab](https://colab.research.google.com/), chọn tab **GitHub**, nhập URL repository của bạn và chọn file notebook `colab/Lab22_DPO_T4.ipynb`.
3. Bấm **Runtime** ➔ **Change runtime type** ➔ Chọn **T4 GPU** ➔ Bấm **Save**.

---

## Bước 3: Cấu hình API Keys & Biến Môi Trường (.env)

Trong Colab, để mô hình gọi chấm đánh giá tự động (NB4 & NB6) bằng mô hình `openai/gpt-oss-20b` thông qua OpenRouter và để đẩy adapter lên Hugging Face Hub (Lấy điểm thưởng Bonus):

* **Cách 1 (Khuyên dùng):** Upload trực tiếp file `.env` đã điền đầy đủ key của bạn từ máy tính lên thư mục `/content/lab22/` của Colab sau khi chạy cell khởi tạo thư mục.
* **Cách 2:** Nhập trực tiếp API Keys vào ô bảo mật của Google Colab (nút biểu tượng **🔑 chiếc khóa** bên cột trái màn hình Colab) với các biến:
  - `OPENAI_API_KEY`: Điền key OpenRouter của bạn.
  - `OPENAI_BASE_URL`: `https://openrouter.ai/api/v1`
  - `JUDGE_MODEL`: `openai/gpt-oss-20b`
  - `HF_TOKEN`: Token Hugging Face có quyền WRITE của bạn.

---

## Bước 4: Chạy toàn bộ các Cell trong Notebook

Bấm nút **Run all** (hoặc nhấn `Ctrl + F9`) trên Colab. Tiến trình bao gồm:
1. **Khởi tạo và cài đặt thư viện:** Cài đặt Unsloth, TRL, PEFT và các công cụ bổ trợ (mất ~3-5 phút).
2. **NB1 — SFT-mini:** Tải base model `Qwen2.5-3B-bnb-4bit` và huấn luyện nhanh trên 1000 mẫu Vietnamese Alpaca (mất ~10 phút). Cell này sẽ sinh ra biểu đồ `02-sft-loss.png` trong thư mục `submission/screenshots/`.
3. **NB2 — Preference Data:** Xử lý dữ liệu preference từ UltraFeedback thành cấu trúc `prompt / chosen / rejected` và lưu thành file Parquet.
4. **NB3 — DPO Training:** Huấn luyện DPO trên adapter vừa tạo, tối ưu hóa sự khác biệt giữa phản hồi tốt và xấu (mất ~15 phút). Cell này sẽ vẽ và lưu đồ thị phần thưởng `03-dpo-reward-curves.png`.
5. **NB4 — Compare and Eval:** Tự động sinh câu trả lời side-by-side từ mô hình SFT-only và SFT+DPO cho 8 prompts thử nghiệm, gọi judge từ OpenRouter chấm điểm, xuất ra bảng so sánh `04-side-by-side-table.png`.
6. **NB5 (Tùy chọn) — Merge & Quantize:** Gộp adapter vào base weights và chuyển đổi sang định dạng GGUF Q4_K_M siêu nhẹ để chạy thử local.
7. **NB6 (Tùy chọn) — Benchmark:** Chạy các bài test tiêu chuẩn (IFEval, MMLU...) để đánh giá tổng thể độ căn chỉnh.

---

## Bước 5: Chụp ảnh và tải về máy các file Screenshots cần thiết

Sau khi chạy xong, hãy vào mục quản lý files của Colab (bên cột trái), truy cập vào thư mục `submission/screenshots/` và tải về máy các bức ảnh sau:
1. `01-setup-gpu.png` (Chụp đầu ra cell kiểm tra GPU `nvidia-smi`)
2. `02-sft-loss.png` (Biểu đồ loss giảm dần ở NB1)
3. `03-dpo-reward-curves.png` (Đồ thị phần thưởng chosen vs rejected ở NB3)
4. `04-side-by-side-table.png` (Bảng so sánh đầu ra 8 prompts ở NB4)
5. `05-judge-output.png` (Chụp log chi tiết kết quả chấm của Judge cho ít nhất 3 prompt)
6. `06-gguf-smoke.png` (Kết quả chạy thử file GGUF bằng llama.cpp ở NB5)
7. `07-benchmark-comparison.png` (Biểu đồ so sánh cột 4 bài test ở NB6)

*Lưu ý:* Sau khi tải các ảnh này về máy tính, bạn hãy chép đè chúng vào đúng thư mục `submission/screenshots/` trên máy local của bạn.

---

## Bước 6: Chạy verify và nộp bài lên LMS

1. Mở terminal tại thư mục dự án trên máy tính của bạn và chạy lệnh sau để kiểm tra xem đã đủ mọi file nộp chưa:
   ```bash
   python scripts/verify.py
   ```
2. Nếu màn hình hiện dòng chữ **`✓ Core checks passed.`**, nghĩa là bạn đã hoàn tất mọi yêu cầu!
3. Commit toàn bộ ảnh screenshots và file `REFLECTION.md` đã điền đầy đủ và push lên repository GitHub công khai của bạn.
4. Sao chép link repository GitHub công khai của bạn và dán vào ô nộp bài của bài Lab 22 trên hệ thống VinUni LMS.
