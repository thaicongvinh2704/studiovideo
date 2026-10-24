# Bàn giao Phong Thần · 24/10/2026

## Bản dựng mới nhất và trạng thái thật

`reference_style_edit_v2/preview.html`, `timeline.json`, `project.json` và
`review/` là bản dựng 192 nhịp hình / 243 cue / 14:55,6 để xem trước. Giọng H/Bắc
đã áp 1,25× một lần; không tăng tốc lần nữa. Chưa render phim hoàn chỉnh.

Người dùng đã phát hiện bốn lỗi cụ thể; bản dựng **chưa được duyệt**. Sau đó
người dùng yêu cầu dừng sửa để trao đổi. Lượt cài công cụ và đồng bộ Git không
phải yêu cầu tiếp tục sửa/render phim.

1. Khoảng 00:13–00:17: thiếu hình hai người bị áp giải, thi hành án và lính báo
   việc xong. K03 chỉ có cổng và bóng, không đủ minh họa hành động. Cần kiểm kê
   và bổ sung tư liệu đúng hành động; không dùng ảnh gần nghĩa để lấp cảnh.
2. Khoảng 00:47–00:51: phải thấy Tử Nha cầm Roi Đả Thần rồi zoom vào roi.
   Có tư liệu Y02 phù hợp để đối chiếu; hiện bản dựng dùng roi rời.
3. Khoảng 00:51–00:56: cuộn sắc trong sơ đồ còn trống; cần nội dung có mục đích
   và kiểm tra chữ thật trong khung hình.
4. Khoảng 01:54–02:00: phải thể hiện nhận phù sắc từ Nguyên Thủy Thiên Tôn.
   Đã tìm thấy K10 diễn tả trao sắc; hiện cảnh A17 chỉ đưa tay trống.

Chưa áp dụng bốn sửa đổi này. Bản sao trước sửa được giữ tại
`reference_style_edit_v2/feedback_20261024_01/`.

## Vật liệu và công cụ

- `assets/`: ZIP V2 gốc và các hình đã giải nén; ảnh/media lớn được Git LFS quản lý.
- `motion_test_*`: bản thử chuyển động trước, không phải chứng nhận đã duyệt.
- `reference_style_trial_32s/` và `outputs/mo_den_reference_style_trial_32s/`:
  đoạn thử cách đạo diễn, không phải phim hoàn chỉnh đã duyệt.
- `docs/research/tay_du_5y9RFw9eAz8/`: nghiên cứu đạo diễn từ video tham chiếu.
- `docs/EDITING_TOOLS.md`: WhisperX, Glaxnimate, Qwen3-VL local và cách cài lại.
  Binary, model và venv không đưa lên Git; máy khác chạy script cài đặt.

Máy mới cần Git LFS và `git lfs pull`, đọc `AGENTS.md` cùng trạng thái phối hợp
trước khi sửa. Có thể chạy `tools/serve_studio_review.py` theo hướng dẫn của bản
dựng để mở preview; đường dẫn localhost của máy cũ không phải dịch vụ công khai.
