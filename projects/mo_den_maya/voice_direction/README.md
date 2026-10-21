# Trạng thái xử lý giọng Maya

**Lựa chọn hiện tại: custom H, nam, Bắc, 1,25×.** Người dùng đã chọn
`local_custom_voices_nam_v3/08_nam_custom_H_1_25x.wav` để sản xuất toàn bài.
Cấu hình khóa mẫu: `selected_voice_H.json`. Bản native H được giữ nguyên ở
`voices/references/mo_den_custom_H/H_native.wav`; dùng làm reference cùng một
speaker, không thiết kế người nói mới ở mỗi câu. Tăng tốc 1,25× đúng một lần,
không dịch cao độ. Những mục B và Xuân Vĩnh dưới đây là lịch sử so sánh.

Runner mới: `tools/create_maya_custom_H.py`, VoxCPM2 GGUF local, không gọi API.
Đầu ra riêng: `full_narration_custom_H_125/`. Giữ nguyên TXT/JSON/SRT nguồn;
đọc đủ 36 beat / 275 cue, chia thành 169 cụm nghĩa và áp khoảng nghỉ JSON.
SRT cụm ý đo theo file tổng hợp là bản gần đúng, chưa căn từng từ. Giọng mẫu
đã được người dùng chọn; phát âm và độ nhất quán của toàn bài vẫn cần nghe.

```powershell
projects/angkor_wat_1min/.venv/Scripts/python.exe -X utf8 tools/create_maya_custom_H.py
```

Người dùng yêu cầu xử lý giọng trước. Gói nguồn đã giải nén, giữ nguyên trong
`input/Mo_Den_Maya_Dao_Dien_Giong_Viet/`.

Adapter: `studio/voice_direction.py`. Tạo lại mẫu/cached audio bằng
`tools/create_maya_directed_ab.py` trong môi trường Python có VieNeu.

Kết quả nằm trong `ab_samples/`: ba cặp mở bài, mười ba năm, nhìn lại sự sụp đổ.
Xem `ab_samples/BAO_CAO_VA_CACH_NGHE.md` trước khi nghe và đánh giá.

**Yêu cầu mới:** người dùng đã chỉ định tăng tốc 1,25× và tạo lời đọc toàn bộ
kịch bản Maya sau bước A/B. Dùng pipeline đạo diễn B với cùng mã giọng Bắc,
tăng tốc toàn bản (kể cả khoảng nghỉ), giữ cao độ ở bước tăng tốc.

Runner: `tools/create_maya_full_narration.py`; kết quả ở `full_narration_125/`.
Hồ sơ giọng và bản B gốc vẫn được bảo toàn; mức 1,25× áp dụng riêng ở bản Maya
này, không nhân hai lần vào hồ sơ giọng. Chưa render clip. Không gọi SRT nguồn
hoặc SRT cụm ý quy đổi thời gian là phụ đề đã căn từng từ với audio mới.
Kiểm tra kỹ thuật không thay thế nghe duyệt phát âm và chất lượng kể.

## Bản so sánh Xuân Vĩnh

Người dùng yêu cầu thêm một bản tương tự bằng mẫu
`voices/auditions/mo_den_20261021/02_xuan_vinh.wav`. Dùng trực tiếp mã preset
`02_xuan_vinh_codes.npz` đã lưu cùng mẫu, không clone lại từ WAV tổng hợp.
Danh mục preset ghi nam, Bắc; phát âm/vùng giọng trên toàn bài vẫn cần nghe.

Hồ sơ so sánh: `voices/mo_den_xuan_vinh_maya_comparison.voice.json`;
giữ cao độ và nhịp gốc preset ở lớp âm sắc, áp chỉ đạo nhịp/nghỉ giống bản
trước rồi tăng tốc cả bài 1,25×. Thời lượng tự nhiên có thể khác bản B.
Thư mục riêng: `full_narration_xuan_vinh_125/`. Không thay giọng mặc định
hoặc ghi đè bản Maya giọng B.

Lệnh tạo:
```powershell
projects/angkor_wat_1min/.venv/Scripts/python.exe -X utf8 tools/create_maya_full_narration.py --profile voices/mo_den_xuan_vinh_maya_comparison.voice.json --output projects/mo_den_maya/voice_direction/full_narration_xuan_vinh_125 --voice-label "Xuân Vĩnh · giọng Bắc" --file-stem Mo_Den_Maya_Xuan_Vinh_1_25x_DAY_DU
```
