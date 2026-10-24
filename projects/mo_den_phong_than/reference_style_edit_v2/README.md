# Mỏ Đen · Tập 2 · Phong Thần — bản dựng lại để duyệt

Người dùng yêu cầu dựng lại toàn tập và **khoan render để xem trước**. Bản này độc lập với project 102 cảnh cũ; không ghi đè project, lời đọc hoặc PNG supplied.

Mở `preview.html` qua máy chủ local của repo. Địa chỉ trong phiên làm việc:

http://127.0.0.1:62824/projects/mo_den_phong_than/reference_style_edit_v2/preview.html

Có phát/tạm dừng, tua theo thời gian, chín chương, chọn từng cảnh, bật/tắt phụ đề, lời đọc đang phát và bảng ảnh toàn tập. Các lớp xuất hiện, đường nối chạy, vật rơi, mưa và thay ảnh diễn ra trực tiếp, không dùng một MP4 toàn phim làm preview.

## Tệp dựng

- `edit_plan.txt`: chỉ dẫn từng nhịp gắn cue và mục đích mới; là đầu vào có thể chỉnh.
- `timeline.json`: lệnh dựng theo lớp và thời gian mà trình xem thực hiện.
- `project.json`: bản chỉnh sửa được trong Studio, có ảnh, chữ, vector và key chuyển động riêng. Đây là bản nháp, không tự cấp quyền xuất final hoặc bỏ qua QC nhân vật.
- `shot_list.csv`: đầy đủ mốc, cue, nguồn hình, mục đích, lời kể tương ứng.
- `subtitles.srt`: 243 cue đã cộng phần mở đầu 1,5 giây.
- `review/board_*.jpg`: 16 bảng ảnh đại diện toàn tập; các cảnh có diễn biến còn có ảnh đầu/cuối.
- `assets_manifest.json`: nguồn, crop, SHA-256 và vai trò nhân vật/đạo cụ của từng derivative.
- `build_report.json`, `repetition_audit.json`: kiểm tra kỹ thuật; không phải duyệt thẩm mỹ.
- `review_notes.md`: nhận xét thực tế và các giới hạn trước final.

Tổng thời lượng khoảng 14:55,6. Dùng nguyên master H tiếng Bắc đã có (~14:52,1), thêm mở 1,5 giây và kết 2 giây. Không áp tốc độ lần hai, không sinh ảnh/giọng hoặc thay bản sắc Mỏ Đen. Thay người đứng/quỳ bằng cut giữa ảnh supplied, không coi là tween cơ thể mượt.

## Dựng lại / mở trên máy khác

Chạy `tools/build_phong_than_reference_edit.py` với môi trường Pillow/Studio đang dùng của repo để tạo lại JSON, ảnh và bảng duyệt. Công cụ không gọi trình mã hóa video. Phục vụ repo bằng `tools/serve_studio_review.py --port 62824` rồi mở đường dẫn trên. Máy chủ này hỗ trợ byte range để tua audio; máy chủ không hỗ trợ Range có thể làm tiếng quay về đầu khi phát từ giữa tập. Chưa cần cài model giọng để xem vì dùng lại audio đã có; máy khác cần lấy các file LFS thật.

Chỉ thực hiện bước xuất phim đầy đủ sau khi người dùng duyệt bản edit; không diễn giải yêu cầu tạo bản xem này thành phê duyệt render.
