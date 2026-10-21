# Giọng tham chiếu của Studio

## Giọng chính hiện tại

Lựa chọn mới nhất là **bản B**: `../demos/vietnamese_ab/B_giong_ke_tieng_viet.wav`.
Voice Studio mặc định chọn **Mỏ Đen · giọng Bắc · bản B**. Hồ sơ
`../mo_den_EFp49inlLuQ_04.voice.json` giữ mã giọng của nguồn EFp49inlLuQ,
âm sắc đã chọn, nhịp nền B và bảng nhấn/nghỉ theo ý. Các thông số nhịp của mẫu
ngắn 04 bên dưới là lịch sử; dùng `postprocess` hiện tại và `delivery.intent_settings`
khi dựng mới. Không thay thế WAV B đã chọn.

Người dùng đã chọn `../auditions/reference_EFp49inlLuQ_variants/04_cao_nhanh.wav`
làm giọng chính, thay lựa chọn kcWEaXRh2hA trước đó. Voice Studio mặc định chọn
**Mỏ Đen · giọng chính**, hồ sơ `../mo_den_EFp49inlLuQ_04.voice.json`.
Mỗi lời đọc mới phải dùng đúng mã giọng của nguồn EFp49inlLuQ và xử lý đã chốt:
cộng 0,8 bán âm, nhịp 1,035×, giữ formant, EQ 2800 Hz / Q 0,8 / +0,7 dB,
chuẩn hóa âm lượng. Không chỉ dùng lại giọng tham chiếu chưa biến tấu.

WAV đã chọn và các tài nguyên nguồn được giữ nguyên; hash nằm trong hồ sơ.
Giọng cũ giữ để tra lại, không còn là lựa chọn mặc định.

## Lựa chọn trước đó

`video_mau_kcWEaXRh2hA/` chứa MP3 do người dùng cung cấp, đoạn tham chiếu
giây 60–68, bản giảm nhiễu, mã giọng dùng lại và WAV đọc thử **nội dung mới**.
MP3 gốc được sao chép nguyên byte; không sửa file trong Downloads.

Hồ sơ `../video_mau_kcWEaXRh2hA.voice.json` ghi hash nguồn, mốc trích,
hash tài nguyên và trạng thái `previously_selected`. Bản đọc
`video_mau_kcWEaXRh2hA/audition.wav` đã được chọn trước khi chuyển sang bản số 4.
Không xác nhận
danh tính người đọc, không gắn tên Nguyễn Việt Cường, không khẳng định giống hoàn toàn.
Giảm nhiễu không bảo đảm tách hết nhạc nền hoặc tiếng động.

Trong Voice Studio, giọng kcWEaXRh2hA có nhãn **Mỏ Đen · giọng trước**.
Việc đổi lựa chọn không sửa các WAV/video cũ.
Model CPU được nạp một lần cho mỗi Voice Studio khi môi trường có VieNeu.
Nếu VieNeu nằm trong môi trường riêng của dự án Angkor Wat, Studio gọi môi trường đó.
Máy mới cần cài `requirements-voice.txt`; lần đầu có thể cần mạng để tải model.
Cache model không nằm trong Git. Không tự chuyển sang Piper nếu giọng tham chiếu lỗi.

Script chuẩn bị tham chiếu bằng Python có VieNeu (không chạy lại để ghi đè giọng đã chốt):

```text
python -X utf8 tools/prepare_sample_video_voice.py "duong-dan-file-nguon.mp3"
```

Giữ nguyên tham chiếu, mã giọng và WAV của các lựa chọn để tra lại. Không tự thay
giọng chính hiện tại bằng Piper, Hải Đăng hay lựa chọn trước. Mỗi lời đọc mới vẫn cần nghe
kiểm tra phát âm, đọc đủ lời và căn thời gian với hình.
