# Bản sửa diễn hoạt cứng — 22/10/2026

**Phản hồi tiếp theo:** người dùng nhận xét tay mèo chưa tự nhiên. V2 không
được duyệt làm rig. Bản sửa mới và giới hạn: `../articulated_v3/README.md`.

Video: `outputs/mo_den_motion_demo_rigid_v2/Mo_Den_demo_15s_rigid_v2.mp4`.
Mã: `tools/render_mo_den_rigid_demo.py`. Đây là bản thử tiếp theo, chưa được người
dùng duyệt và chưa tích hợp vào exporter sản xuất.

## Nguyên nhân V1

V1 dịch chân trước bằng trường mesh chỉ khoảng 2 px ở ảnh xuất. Khán giả gần
như chỉ thấy miệng. Chuyển động đầu/thân/đuôi dùng chung texture và vùng trọng
số chuyển tiếp nên có thể kéo giãn hình quanh khớp. Các khung tĩnh đã xem không
chứng minh chuyển động liên tục đạt; phản hồi người dùng có giá trị ưu tiên.

## Thay đổi thực tế

- Bỏ mesh và mọi scale độc lập theo trục. Đầu, đuôi và hai chân trước là các lớp
  xoay cứng, có pivot; chiều dài trong từng lớp không bị thay đổi theo thời gian.
- Giữ thân và hai chân trụ ngồi cố định. Chân trước trái xoay tối đa 60°, phải
  58°, rồi cùng mở 48° ở nhịp câu hỏi. Có giai đoạn vào, giữ và trở về, không
  rung liên tục theo sóng âm. Keyframe lưu trong manifest.
- Dùng texture đầu/mắt/mặt nạ, bàn chân, chân trụ và đuôi từ PNG được cung cấp.
  Phần thân bị che và đoạn chân trước kết nối được hoàn thiện thủ công bằng
  đường vector và màu lông lấy từ nguồn, trong derivative riêng. Không dùng
  mô hình sinh ảnh/video. PNG nguồn giữ đúng SHA256 trong thư viện.
- Dùng cùng WAV H của V1, không đổi âm sắc, tốc độ, cue miệng hoặc lời kể.

## Kiểm tra thực hiện

Đã mở toàn thân nghỉ, các pose trái/phải/cùng mở và bảng khung giải mã MP4 cận
vai/cổ/thân ở 2 khung/giây. Bản cắt thử đầu lộ mảng màu vai, đường cắt cổ và
miếng nền hình chữ nhật quanh chân; đã bỏ các cách cắt đó, hoàn thiện vùng che
và xuất lại trước giao. Các khung hiện xem không thấy hình chữ nhật màu lông,
không có miệng chồng, tai/đuôi không bị cắt; chân trụ và kích thước thân giữ
cùng vị trí. Cử chỉ chân trước đọc được rõ hơn V1 ở cỡ toàn thân.

Khớp chân trước còn đơn giản theo kiểu cutout; chưa có elbow/wrist độc lập.
Không coi đây là rig hoàn chỉnh hoặc đảm bảo thẩm mỹ. Chưa đánh giá độc lập
xem/nghe real time, chưa chứng nhận chính xác khẩu hình tiếng Việt. Cần người
dùng xem video hiện tại; không áp dụng hàng loạt toàn phim theo kết quả test.

FFprobe: 15,000 giây, 1920×1080, 30 fps, 450 khung H264; AAC 15 giây. FFmpeg
giải mã toàn bộ trả 0. `manifest.json` lưu provenance và hash video/audio.
