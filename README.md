# Studio Video

Ứng dụng Windows viết bằng Python/PySide6 để dựng video giải thích kiến thức với timeline, lời đọc, hình vẽ vector và ảnh tư liệu.

Đây là mã nguồn dự án hiện tại, thay nội dung ứng dụng trước đó trong repository này. Hướng dẫn đầy đủ: [README_VI.md](README_VI.md).

## Cài đặt và mở

1. Cài Python 3.11/3.12 x64, Git và Git LFS. Có FFmpeg/ffprobe trên PATH để xuất video.
2. Chạy `git lfs install`, rồi clone repository. Nếu đã clone, chạy `git lfs pull` để nhận các tệp media lớn.
3. Chạy `install_windows.bat` để tạo môi trường Python và cài dependency.
4. Chạy `start_studio.bat` để mở Studio hoặc `start_drawing_desk.bat` để mở bàn vẽ.

Audio, video, ZIP và mô hình ONNX được lưu qua Git LFS. Ảnh, project, kết quả minh họa và hồ sơ QC nằm trong repository; `dist/`, `build/`, môi trường Python và cache tải mô hình được tạo trên từng máy, không đóng kèm.

Voice Studio hỗ trợ thêm giọng tham chiếu VieNeu-TTS bên cạnh Piper. Người dùng đã chốt `voices/demos/vietnamese_ab/B_giong_ke_tieng_viet.wav`: **Mỏ Đen · giọng Bắc · bản B**, hồ sơ `voices/mo_den_EFp49inlLuQ_04.voice.json`. Lời đọc mới dùng cùng mã giọng, âm sắc và nhịp nền B đã lưu. Cách nhấn/nghỉ theo từng ý được ghi trong `delivery.intent_settings` để đạo diễn áp dụng theo kịch bản. Máy mới cần cài `requirements-voice.txt` vào môi trường Python và tải model ở lần dùng đầu. Xem [ghi chú giọng tham chiếu](voices/references/README.md).

Người dùng xác nhận vùng giọng **Bắc**; lời kể và demo dùng **tiếng Việt** theo [chuẩn giọng kể](VIETNAMESE_NARRATION_STANDARD.md). Demo A/B 51 và 52,6 giây, kịch bản gốc, bản chuẩn hóa cách đọc và hồ sơ chờ QC nghe nằm tại `voices/demos/vietnamese_ab/`. Kiểm tra kỹ thuật không thay cho nghe kiểm tra thanh điệu, phát âm và vùng giọng.

## Nội dung chính

- `studio/`: mã nguồn giao diện, renderer, timeline, âm thanh, bàn vẽ và kiểm tra chất lượng.
- `assets/characters/mo_den/`: kho 24 ảnh Mỏ Đen, nguồn gốc và danh mục biểu cảm. Các file lỗi từ gói ban đầu được lưu để tra nguồn; manifest chỉ tới các bản dùng được.
- `projects/`: các project, video, nguồn vector và bản thử, gồm Sơn Tinh. Bản thử không mặc nhiên là mẫu được duyệt.
- `examples/`, `presets/`, `outputs/`, `qc/`: tài nguyên mẫu, kết quả dựng và bằng chứng kiểm tra.
- `tools/`, `tests/`: công cụ tác giả, đóng gói và kiểm thử.

Xem [hướng dẫn bàn vẽ](DRAWING_DESK_GUIDE.md), [quy định dự án](AGENTS.md) và [thông tin bên thứ ba](THIRD_PARTY_NOTICES.md).

## Trạng thái cần biết

Mỏ Đen là nhân vật chính. Kho PNG đã đủ 24 ảnh; bộ chọn kho mèo và luồng QC xuất riêng cho mèo chưa được hoàn thiện. Bàn vẽ có Bézier, bút đậm nhạt, mốc liên kết, thư viện nháp và API lệnh. Các mẫu người/Sơn Tinh là bản thử để xem và chỉnh sửa, không được tự coi là master đã duyệt.

Các tệp thực thi cũ trong `dist` trên máy phát triển không phải bản đóng gói của mã mới. Lịch sử tài liệu và project có thể chứa các thiết kế đã bị loại; tuân theo trạng thái hiện tại trong `AGENTS.md` và manifest tài nguyên.
