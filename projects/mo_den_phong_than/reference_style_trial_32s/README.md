# Bản thử đạo diễn 32 giây

Người dùng yêu cầu thử khoảng 30 giây bằng tư liệu sẵn có sau khi nghiên cứu video Tây Du Ký. Đây là snippet để người dùng đánh giá cách dựng, không phải phim hoàn chỉnh đã được duyệt.

- Video: `outputs/mo_den_reference_style_trial_32s/Mo_Den_Phong_Than_thu_dao_dien_32s.mp4` (31.792 giây, 1280×720, 24 fps, H.264/AAC).
- Audio: trích liên tục cue 68–73 từ master Custom H đã có; không tạo người nói mới, không áp dụng 1.25x lần thứ hai.
- Nguồn: Y02/Y02_B (nhân vật người, giữ nguyên hình); O01/O06 (đạo cụ); B15 (ruộng); Mỏ Đen 13/14/16 đúng manifest. Không sinh ảnh.
- Dựng: chín nhịp có mục đích trong `shot_plan.json`. Cắt từ đứng sang quỳ bằng hai ảnh nguồn; không giả là đã diễn hoạt động tác quỳ liên tục. Đường chỉ, sơ đồ, mây/mưa và chữ là phần dựng bổ sung.

## Kiểm tra bản hiện tại

Đã mở contact sheet và ảnh lấy lại từ MP4: bố cục người giữ tỉ lệ, không kéo dãn cơ thể; các crop loại phần nhãn bị cắt; cảnh quỳ giữ chân trong vùng hình thay vì che bằng phụ đề. Nhân vật nguồn là tranh người supplied đã có, không phải character master vector mới hoặc rig được duyệt. Không thay đổi mặt, bàn tay hay hình học nguồn. Cuộn sắc và biểu tượng mưa đi theo lời kể; các khung so sánh giữ vùng riêng, không tràn vào chân dung. Mỏ Đen sử dụng pose nguyên vẹn và không bóp dọc/ngang. Nguồn gốc và SHA-256 nằm trong `manifest.json`.

Đã giải mã toàn bộ MP4 bằng FFmpeg không báo lỗi; xác nhận có cả hình và tiếng. Việc này không chứng nhận thẩm mỹ hoặc QC nghe. Chưa có đánh giá nghe trực tiếp mới cho trích đoạn; dùng lại master H hiện có. Bản thử chờ phản hồi của người dùng, không cấp quyền render cả phim.

Tái tạo: `projects/angkor_wat_1min/.venv/Scripts/python.exe tools/render_reference_style_trial.py --render`.
