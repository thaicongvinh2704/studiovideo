# V3 — sửa chân trước sau phản hồi chưa tự nhiên

Video thực: `outputs/mo_den_motion_demo_articulated_v3/Mo_Den_demo_15s_articulated_v3.mp4`.
Mã render: `tools/render_mo_den_articulated_demo.py`.

## Phản hồi và thay đổi

Người dùng phản hồi chân trước V2 chưa tự nhiên. V2 xoay toàn cánh chân 48–60°
quanh một pivot, không có khuỷu/cổ chân độc lập, gây cảm giác miếng cắt cứng.
Không dùng V2 làm rig được duyệt; giữ lại file làm lịch sử.

V3 dùng hai đoạn xương cố định 55/50 px cho mỗi chân trước, giải vị trí khuỷu
theo mục tiêu cổ chân với nhánh gập ra ngoài. Mục tiêu không đạt được bị chặn,
không kéo dài xương. Vùng lông nối được vẽ bằng đường cong vector mềm bao quanh
cấu trúc; không phải mesh làm co kéo toàn ảnh. Vai cố định; hai chân trụ giữ
nguyên tư thế ngồi. Không tạo dáng đi/chạy hoặc thêm ngón tay người.

Bàn chân nâu dùng texture từ PNG gốc đã có, xoay riêng tối đa 5,88° với độ trễ
0,11 giây, thay vì xoay cùng cánh chân 60°. Mục tiêu cổ chân di chuyển tối đa
28 px ngang và 18 px dọc. Hai bên vào/ra lệch nhịp, chỉ cử chỉ theo các đoạn
kể, có nghỉ. Keyframe và 900 mẫu vị trí khớp lưu trong manifest/joint_track.

Audio dùng nguyên WAV H của demo trước, không đổi speaker/tốc độ/nội dung.
Không có mô hình sinh ảnh/video. Original PNG giữ hash thư viện. Phần nối tay
là derivative vẽ thủ công theo hình nguồn; đây không phải ảnh gốc tách lớp sẵn.

## Kiểm tra và giới hạn

Đã mở ảnh nguồn, toàn thân nghỉ, các tư thế trái/phải và bảng khung xuất MP4
cận vai/cổ chân ở 2 fps. Bản vẽ thử có nét offset giao nhau và vòng khớp mảnh;
đã bỏ cách vẽ đó trước xuất cuối. Bản hiện dùng một đường viền ngoài liên tục
và nét gập nối tới bàn chân, không vẽ vòng tròn quanh khớp.

Trong các khung hiện đã xem: chân trụ/thân giữ nguyên kích thước và vị trí,
bàn chân nâu có nét ngón từ ảnh nguồn; chuyển động vào/ra có khung trung gian;
không thấy khớp bị hở thành nền hoặc miệng chồng. Độ chi tiết vai/cổ chân vẫn
đơn giản theo minh họa 2D; không chứng nhận giải phẫu hay độ tự nhiên từ solver.
QC thẩm mỹ của người dùng và xem/nghe real time vẫn chờ. Chưa tích hợp rig
vào exporter Studio, chưa áp dụng toàn phim Maya, chưa hỗ trợ góc nhìn mới.

Kiểm tra toán trên toàn 450 khung: hai chiều dài xương giữ 55/50 px. Đây chỉ
là kiểm tra chống kéo xương, không phải bằng chứng hoạt hình đẹp. FFprobe xác
nhận 15 giây, 1920×1080, 30 fps, 450 khung H264, AAC 15 giây. Giải mã toàn
video FFmpeg trả 0. `manifest.json` lưu source/audio/video/code hash.
