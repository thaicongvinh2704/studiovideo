# Kết quả cài công cụ hỗ trợ dựng · 24/10/2026

Đã cài và nối vào Studio source qua **Hỗ trợ dựng…**; không build lại EXE cũ.

| Công cụ | Chạy thật | Kết quả |
|---|---|---|
| WhisperX 3.8.6 / torch 2.8.0 CPU | Căn 10,5 giây audio H có sẵn, 3 cue, 49 từ | Có mốc cho 49 từ, giữ nguyên nội dung cue; chưa nghe QC |
| Glaxnimate 0.6.0-git-d2da67a | Nhập Lottie mũi tên do code vẽ, xuất PNG frame 0 và 15 | Hai ảnh trong suốt 400×180, mũi tên thay vị trí đúng keyframe |
| Qwen3-VL 2B Instruct / Ollama 0.40.10 | Đối chiếu shot_005.jpg với yêu cầu áp giải | Trả nhận xét tiếng Việt: chưa thấy hai người bị áp giải và quân lính rõ ràng |
| Studio source | Khởi tạo cửa sổ chính/cửa sổ hỗ trợ | Mục hỗ trợ có mặt, xem `dialog.png` |

Tư liệu/đầu ra:
- `doctor.json`: đường dẫn, phiên bản và import thực tế.
- `whisperx_environment.txt`: dependency của môi trường riêng; `pip check` không có xung đột.
- `downloads_sha256.json`: hash ba bộ tải; bộ cài Glaxnimate được Windows xác minh chữ ký KDE hợp lệ.
- `sample_H.wav`, `sample_H.srt`: trích 10,5 giây của giọng H hiện tại để thử, không tạo voice mới.
- `alignment_sample_v2/alignment.json`: hash đầu vào, từ/mốc/score, nguyên văn cue.
- `alignment_sample_v2/aligned_proposal.srt`: nội dung đúng nguyên văn; mốc nằm trong audio.
- `vector_tool_test.json`, `vector_frame_0.png`, `vector_frame_15.png`, `vector_test_result.json`.
- `gate_review.json`: nhận xét thực tế, bắt buộc người dựng xem lại, không cấp QC.
- `vision_models.json`: tag/digest các model đã tải; launcher chỉ dùng bản Instruct.

Hai vấn đề đã xử lý: KDE thiếu thư viện chuẩn Python, dùng stdlib Python nhúng
3.11 riêng cho Glaxnimate; model căn mặc định không tương thích đầy đủ với loader
chuẩn trên đoạn thử, đã đổi sang dragonSwing base. `alignment_sample/` là lượt thử
model mặc định bị loại (score trung bình ~0,011), không dùng mốc đó cho phim.
Bản v2 có score trung bình ~0,841 trên đoạn thử; con số chỉ là chẩn đoán kỹ thuật.

Không có audio sản xuất bị đổi tốc độ/giọng; không sửa bốn cảnh phản hồi trong
lượt cài này. Việc dựng đang tạm dừng để trao đổi. Không xuất phim hoàn chỉnh,
không đánh dấu chất lượng giọng, thẩm mỹ hoặc nhân vật đã được người dùng duyệt.

Hướng dẫn dùng/cài lại: `docs/EDITING_TOOLS.md` và `tools/install_editing_tools.ps1`.
Model/cache/venv được Git ignore; không đẩy binary/runtime lên repo trong lượt này.
