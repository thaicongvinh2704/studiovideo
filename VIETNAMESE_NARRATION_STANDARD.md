# Chuẩn giọng kể tiếng Việt của Mỏ Đen

**Cập nhật cho video Maya:** người dùng đã chọn mẫu custom H:
`projects/mo_den_maya/voice_direction/local_custom_voices_nam_v3/08_nam_custom_H_1_25x.wav`.
Cấu hình mới ở `projects/mo_den_maya/voice_direction/selected_voice_H.json`.
Dùng đúng reference H gốc đã giữ, cùng speaker xuyên bài; không tạo một người
nói mới cho mỗi cụm. Áp 1,25× một lần, không thêm dịch cao độ. Engine cho bản
này là VoxCPM2 GGUF local. Mẫu được chọn không tự duyệt phát âm toàn bài.
Phần mô tả B dưới đây là chuẩn cũ/UI legacy, không thay lựa chọn H cho Maya.

Ngôn ngữ lời kể và kịch bản thử: **tiếng Việt**. Vùng giọng **Bắc**, do người dùng
xác nhận ngày 21/10/2026. Không tự thay vùng hoặc đổi người nói giữa các đoạn.
Giọng đã chọn: `voices/mo_den_EFp49inlLuQ_04.voice.json`.

**Mẫu B cũ, chỉ còn là cấu hình UI legacy:** `voices/demos/vietnamese_ab/B_giong_ke_tieng_viet.wav`.
Giữ cùng âm sắc và nhịp nền của B. Các mức nhấn, nghỉ theo ý nằm trong
`delivery.intent_settings` của hồ sơ; người dựng áp dụng theo nội dung từng cảnh,
không lặp máy móc tám đoạn của demo. Lựa chọn B thay cho mẫu ngắn 04 làm chuẩn
cách kể, không tự đánh dấu toàn bộ QC phát âm đã đạt.

## Khả năng model và giới hạn đã kiểm tra

- Môi trường đang dùng `vieneu==3.8.3`, model `pnnbao-ump/VieNeu-TTS-v3-Turbo`,
  backend CPU/ONNX fp32. Model có tiếng Việt, bộ chuyển chữ sang âm vị sea-g2p,
  chức năng lấy giọng tham chiếu tiếng Việt và xử lý WAV 48 kHz.
- Hồ sơ gốc và mã nguồn tác giả: https://huggingface.co/pnnbao-ump/VieNeu-TTS-v3-Turbo
  và https://github.com/pnnbao97/VieNeu-TTS . Đối chiếu thêm mã SDK cài tại máy;
  số preset và phiên bản trên trang model có thể cũ hơn bản đang cài.
- Engine dùng cả speaker embedding và reference audio codes để điều kiện hóa
  giọng. Reference có thể ảnh hưởng cách đọc; không bảo đảm sao chép chính xác
  nhịp/ngữ điệu. Tham số `style` bị bỏ qua ở v3 Turbo, không được báo là đang
  điều khiển diễn xuất bằng tham số này.
- Hỗ trợ tiếng Việt và clone âm sắc **không chứng minh** đọc đúng thanh điệu,
  đúng vùng hoặc nói tự nhiên. Những mục đó phải nghe kiểm tra trên bản hiện tại.

## Tham chiếu

Ưu tiên 3–8 giây tiếng Việt, một người nói, phát âm rõ, không nhạc hay tiếng động.
Engine cắt tối đa 8 giây khi lấy giọng. Giữ file gốc, mốc trích và hash.
Tham chiếu hiện tại là giây 60–68 của MP3 người dùng gửi, đã giảm nhiễu. Chưa có
kiểm tra nghe độc lập xác nhận chỉ một người nói hoặc hết nhạc nền. Không gắn
nhãn sạch/đạt cho tham chiếu chỉ vì đã chạy denoiser; nếu nghe thấy nhiễu hoặc
giọng lẫn thì thay đoạn tham chiếu sau khi trao đổi với người dùng.

## Chuẩn bị lời đọc

Giữ nguyên kịch bản gốc. Lưu bản đọc riêng cùng bảng đối chiếu từng thay đổi
số, ngày tháng, đơn vị, viết tắt và từ nước ngoài. Chỉ thay ở vị trí đã xác nhận
ngữ cảnh bằng `studio/vietnamese_narration.py`; không thay thế hàng loạt mù.
Không đổi dấu tiếng Việt, không xóa thanh để ép phát âm. Tên riêng phải có
cách đọc được ghi rõ; bản gốc luôn giữ nguyên tên để tra lại.

Chia theo câu và cụm nghĩa trọn vẹn, không tách mọi dấu phẩy. Tránh chia giữa
tên riêng, số và đơn vị, hoặc các từ thuộc cùng cụm. Xuất danh sách chunk mà
engine thực sự dùng để kiểm tra, vì normalizer có thể thay dấu và ranh giới.

## Cách kể và demo A/B

Ưu tiên rõ lời, đúng thanh, đúng giọng Bắc rồi mới tăng biểu cảm. Tự nhiên,
gần gũi, vừa cảm xúc; không mặc định quảng cáo, phát thanh hay bi lụy.
Không bẻ cao độ theo cảm xúc hoặc thêm rung/nhấn làm sai thanh, nghe như hát.
Hai bản giữ cùng thiết lập âm sắc toàn cục của bản 04 đã chọn (+0,8 bán âm,
giữ formant), không thêm đường cao độ khác nhau giữa A và B.

Demo A/B mỗi bản 45–60 giây, cùng văn bản tiếng Việt đã chuẩn hóa và cùng mã
giọng. A kể đều tự nhiên; B thay đổi nhẹ độ dài cụm, cường độ và khoảng nghỉ
theo ý. Có kể bình thường, tò mò, một điểm nhấn cảm xúc, kết lắng, câu sáu
thanh và kiểm tra số/ngày/đơn vị/tên riêng. Không cắt từ để ép đủ thời lượng.

QC nghe phải ghi rõ: đọc đủ lời, thanh ngang/sắc/huyền/hỏi/ngã/nặng, vùng Bắc
nhất quán, cụm nghĩa, số/ngày/đơn vị/tên riêng, mức cảm xúc và cùng danh tính
giọng giữa A/B. Chỉ số tín hiệu, codec, duration và test phần mềm là kiểm tra
cơ chế. Không tự đánh dấu QC nghe đạt, không coi lựa chọn một mẫu ngắn là
phê duyệt mọi lời đọc sau này.
