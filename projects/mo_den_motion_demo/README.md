# Demo Mỏ Đen nói chuyện — 15 giây

**Phản hồi mới nhất:** người dùng nhận xét chân không thấy chuyển động và thân
bị kéo giãn. V1 không đạt yêu cầu diễn hoạt, dù giải mã file và một số khung hình
đã qua kiểm tra kỹ thuật. Không lấy các nhận xét khung tĩnh dưới đây làm duyệt
chuyển động. Bản sửa: `rigid_v2/README.md`.

Người dùng yêu cầu demo ngày 22/10/2026. Video:
`outputs/mo_den_motion_demo_15s/Mo_Den_demo_15s.mp4`.

## Vật liệu và cách làm

- Dùng đúng `mo_den_01` trong manifest thư viện. Không thay đổi PNG gốc.
- Tạo bản dẫn xuất riêng: sửa nền vùng mắt/miệng bằng màu lông lân cận,
  giữ texture mắt gốc, vẽ khẩu hình vector, biến dạng mesh liên tục toàn hình.
  Không dùng mô hình sinh ảnh hoặc sinh video.
- Đầu nghiêng nhẹ theo keyframe, mắt chớp, thân thở, chân trước và đuôi chuyển
  động nhỏ. Không đổi pose toàn thân hoặc nối các PNG biểu cảm khác cấu trúc.
- Audio lấy 0–11,82 giây đầu narration H đã chọn của Maya, thêm 0,55 giây nghỉ
  đầu và nghỉ cuối cho đủ 15 giây. Không đổi speaker hay áp thêm tốc độ 1,25×.
- Rhubarb 1.14.0 phonetic tạo cue. Nội suy hình miệng 22 ms, dùng mức âm để
  khép miệng khi nghỉ. Cue là ước lượng, chưa xác nhận đúng mọi âm tiếng Việt.

Mã render: `tools/render_mo_den_motion_demo.py`. Chạy trong môi trường Qt/Pillow/
numpy/scipy hiện có `projects/angkor_wat_1min/.venv/Scripts/python.exe`.
FFmpeg và FFprobe cần trong PATH. Cue đã lưu trong `mouth_cues_raw.json`.
Render lại không cần gọi model hay tải dependency. `--previews-only` xuất ảnh.

## Kiểm tra hình đã thực hiện

Đã mở trực tiếp poster toàn thân, bảng 9 khung và cận mặt ở trạng thái nghỉ,
chớp mắt và nói. Phát hiện lỗi font ở preview đầu và đã sửa bằng cách nạp font
Windows vào Qt offscreen; preview hiện đọc được chữ tiếng Việt.

- Tai, đuôi và hai chân dưới nằm trọn trong hình; cổ và chân trước liền thân.
- Mặt nạ nâu, màu mắt, mũi, râu và silhouette giữ nhận diện PNG nguồn.
- Cận mặt không còn miệng cũ phía dưới miệng mới; các khung chớp không còn mắt
  mở chồng lên mí. Nền lông đã sửa không lộ mảng sáng vuông trong các cận đã xem.
- Miệng vector dùng cùng viền đen; độ mở còn nhỏ, phù hợp thử nghiệm ngồi kể.
  Mí khép là nét đơn giản và chuyển động chân trước chỉ rất nhẹ.

Đây là kiểm tra hình nội bộ trên các khung đã xem, không phải duyệt thẩm mỹ của
người dùng hoặc xác nhận nghe/khớp môi toàn clip ở tốc độ thật. Không tự đánh dấu
phát âm, vùng giọng hoặc độ chính xác khẩu hình tiếng Việt là đạt.

## Giới hạn

Chưa hỗ trợ đi/chạy, quay đầu nhiều hoặc góc nhìn mới. Chưa xây importer rig hay
QC export sản xuất; demo xuất bằng renderer độc lập, không sửa gate QC hiện có.
Không dùng demo để tuyên bố phim Maya đã sửa hoặc có rig hoạt hình hoàn chỉnh.
`demo_manifest.json` ghi hash nguồn, audio, cue, mã và video để đối chiếu.
