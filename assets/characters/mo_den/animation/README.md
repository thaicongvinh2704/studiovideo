# Mỏ Đen nói chuyện và diễn hoạt 2D — yêu cầu mới 22/10/2026

Trạng thái: **V1 bị phản hồi co kéo thân; V2 bị phản hồi chân chưa tự nhiên**
ngày 22/10. Không dùng V1/V2 làm mẫu đạt chuyển động. Bản thử mới, chưa duyệt:
`outputs/mo_den_motion_demo_articulated_v3/Mo_Den_demo_15s_articulated_v3.mp4`.
V3 dùng hai đoạn xương mỗi chân, bàn chân gốc xoay nhẹ riêng và cử chỉ lệch
nhịp. Xem `projects/mo_den_motion_demo/articulated_v3/README.md`.
Quy trình và giới hạn: `projects/mo_den_motion_demo/README.md`.
V1 là prototype mesh liên tục với mắt/miệng riêng, đã bị phản hồi lỗi; chưa có
rig tách lớp đầy đủ tích hợp vào exporter sản xuất của Studio.

V2 chuyển sang cutout xoay cứng: không mesh, không scale riêng theo trục. Thân và
chân trụ cố định, đầu/đuôi/chân trước xoay quanh pivot. Thân che khuất và gốc
chân trước được hoàn thiện thủ công trong derivative, không sửa PNG nguồn.
Chi tiết và QC: `projects/mo_den_motion_demo/rigid_v2/README.md`.

## QC chuyển động bắt buộc sau phản hồi V1

- Không kéo toàn ảnh để thay cho cử chỉ. Giữ hình đầu, chiều dài chi và tỷ lệ
  thân khi chuyển động; nếu dùng mesh phải kiểm tra biến dạng ở vùng nối.
- Cử chỉ phải nhìn thấy ở cỡ dùng thật. V1 chỉ dịch chân khoảng 2 px là chưa đạt.
- Cảnh ngồi giữ chân trụ; chân trước có thể diễn đạt theo nhịp kể, không ép mọi
  chi chuyển động liên tục. Không biến pose ngồi thành đi/chạy.
- Kiểm tra khung giữa chuyển động, hai biên và khớp vai/cổ/đuôi. Không chỉ xem
  ảnh nghỉ hoặc dùng FPS/decoder làm bằng chứng mượt hay đúng giải phẫu.
- Ghi trạng thái xem/nghe thời gian thật trung thực, giữ clip lỗi làm đối chiếu.
- Không chỉ thêm tên khớp rồi coi chân tự nhiên. Kiểm tra đường viền vai/khuỷu/
  cổ chân, bàn chân giữ nhận diện, nhịp nâng–giữ–hạ và phối hợp hai bên trên
  khung trung gian. Tránh cử chỉ hai chân xoay cứng, cùng nhịp như máy.
Người dùng yêu cầu Mỏ Đen chuyển động, nhép miệng như hoạt hình và phải mượt.
Yêu cầu này mở diễn hoạt cho Mỏ Đen; hình người vẫn theo chuẩn tĩnh hiện hành.

## Đã kiểm tra

- Đã đọc README/manifest và mở trực tiếp ảnh `mo_den_01`:
  `assets/characters/mo_den/library/named_24_v01/mo_den_01_neutral_seated_paws_resting.png`.
- Có 24 PNG static hoàn chỉnh, không phải các lớp của một model chuyển động.
  Miệng, mắt, đầu và chân đã nằm chung trong raster. Chưa có bằng chứng kho có PSD
  tách lớp, mắt khép hay bảng khẩu hình cùng cấu trúc.
- `studio/renderer.py` ghép PNG qua nhánh image; diễn hoạt rig/blink của nhánh
  character cũ không tự áp dụng cho PNG mèo và không được dùng thay thiết kế mèo.
- `studio/supplied_character.py` kiểm tra hash PNG gốc. Rig tách lớp mới cần nhánh
  dữ liệu/QC riêng có provenance; không thay hash gốc hoặc gán role object để né.

## Hướng thực hiện

Dựng một rig 2D tái sử dụng từ đúng thiết kế hiện có, với keyframe và mesh/bone
cho chuyển động nhỏ. Giữ originals byte-for-byte; mọi vật liệu tách lớp và bản sửa
nằm trong gói derivative riêng. Không sinh ảnh/video mới bằng mô hình generative.

V1 nên giới hạn ở Mỏ Đen ngồi kể chuyện: chớp mắt, nhìn, nghiêng/gật đầu nhẹ,
thở, chuyển trọng lượng nhỏ, cử chỉ chân trước và đuôi; miệng nói theo audio.
Đi/chạy, xoay đầu nhiều, nhìn sau lưng cần cấu trúc/ảnh góc nhìn bổ sung và QC riêng.
Không coi kéo một PNG là diễn hoạt xương hay lip sync.

### Chuẩn bị hình một lần

Ưu tiên PSD/SVG có lớp hoặc PNG rời cùng hệ tọa độ, giữ nguyên thiết kế/màu/viền:

- Thân đầy đủ, đầu/mặt nền sạch, tai, đuôi và từng chân trước rời.
- Mắt tách vùng trắng/con ngươi/mí; lông mày riêng; mũi/râu giữ kết nối với đầu.
- Miệng nghỉ và các dáng nói: khép, mở nhỏ, mở rộng, dẹt, tròn, chúm và răng-môi.
  Đây là các dáng nhìn (viseme), không phải mọi chữ viết cần một ảnh riêng.
- Vẽ hoàn thiện vùng bị che ở cổ, khớp chân và gốc đuôi. Chừa phần chồng lớp để
  khi xoay không lộ lỗ/hai đường viền. Mắt/miệng cũ không được còn trên nền mặt.
- Ghi pivot, thứ tự trước/sau, vùng được biến dạng và giới hạn chuyển động.

Có thể chuẩn bị thủ công từ PNG đang có; PSD gốc không bắt buộc. Nhưng PNG không
chứa thông tin vùng bị che: cắt tự động rồi xoay không tự tạo được phần còn thiếu.
Không dùng 24 biểu cảm khác cấu trúc làm các frame khẩu hình vì dễ giật hình.

### Lip sync tiếng Việt

Dùng audio cuối đã áp 1,25×, không dùng SRT ước lượng để suy chính xác âm tiết.
Một nhánh thử có thể lấy cue từ Rhubarb phonetic và chỉnh timeline; tài liệu dự
án chỉ nói chế độ này dùng cho non-English và kém chính xác hơn recognizer English,
không chứng minh chất lượng tiếng Việt. Chỉ theo âm lượng cho mở/đóng không đủ
cho các dáng môi. Không thay giọng hay tốc độ H để ép khớp miệng.

Miệng nghỉ khi hết câu, không rung liên tục theo từng biến động waveform; chuyển
dáng có thời gian giữ và phần chuyển tiếp hợp lý. Mắt/đầu/cử chỉ theo ý kể, không
lặp cùng chu kỳ cho mọi câu. Đánh giá bằng xem/nghe bản xuất, không bằng FPS đơn lẻ.

## Demo trước khi áp dụng cả phim

1. Chọn đoạn 10–15 giây của audio H đã có, có nói, nghỉ và một điểm nhấn.
2. Duyệt model đứng yên và các biên chuyển động trước; chưa ghép vào phim Maya.
3. Xuất demo với nhịp hình xác định; nội suy chuyển động khớp thời gian, render
   từ timeline xác định để preview/export và seek cho cùng kết quả.
4. Xem toàn thân, mặt cận và các frame biên: không méo mặt, hở cổ, đứt chân,
   double mouth, râu trôi, tai/đuôi bị crop hoặc mắt đổi nhận diện.
5. Xem/nghe real time: môi không trễ lời rõ rệt, âm ngậm đóng miệng, khoảng nghỉ
   đúng, mắt/chân/đuôi không giật hoặc lặp máy móc. Không coi decode/test pass là
   QC thẩm mỹ. Người dùng chốt demo rồi mới triển khai toàn phim.

## Tham khảo kỹ thuật đã đọc

- Rhubarb: https://github.com/DanielSWolf/rhubarb-lip-sync
  (mouth cue JSON, recognizer phonetic cho audio non-English; phải thử tiếng Việt).
- Live2D standard parameters:
  https://docs.live2d.com/en/cubism-editor-manual/standard-parameter-list/
  (tham khảo điều khiển mắt/đầu/thân/miệng; chưa chọn/cài runtime Live2D cho Studio).

Demo dùng Rhubarb 1.14.0 chính thức (Windows, recognizer phonetic), lưu dependency
ở `.deps/rhubarb-v1.14.0/` (ignored). Không sử dụng runtime Live2D.
