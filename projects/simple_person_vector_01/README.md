# Mẫu người giản lược bằng vector Studio

Vẽ bằng `studio.drawing_edit.apply_command` và render bằng `studio.drawing`. Không dùng mô hình sinh ảnh, không nhúng bitmap tham chiếu trong các đường nét, không tự động vector hóa ảnh.

- `preview.png`: ảnh nền trắng để xem.
- `preview_transparent.png`: cùng bản vẽ raster hóa trên nền trong suốt.
- `character.drawing.json`: bản gốc mở bằng nút Mở bản vẽ trong bàn vẽ Studio; chỉnh được node, màu, mốc và thứ tự nét.
- `authoring_commands.json`: 24 lệnh thêm đường nét đã sử dụng; metadata và mốc được tạo trong script tác giả.
- `studio_editor.png`: ảnh chụp widget Qt thực với bản vẽ mở và nút có thể chỉnh.
- `comparison.png`: ảnh tham chiếu mới cạnh bản vector.
- `visual_review_notes.json`: nhận xét sau khi xem toàn hình, mặt, hai tay và thumbnail.

Bản thử theo ảnh mới có tay giản lược và thân dưới liền khối. Không đăng ký PASS theo bộ tiêu chí người đầy đủ cũ, không thay mẫu chính Mỏ Đen, không tự bật xuất video cho mẫu này. Màu phẳng và mảng bóng cứng khác phần gradient mềm của ảnh mới.

Tái dựng bằng Python có PySide6: `tools/draw_simple_person_sample.py`. Thêm `--open` để giữ cửa sổ bàn vẽ mở.
