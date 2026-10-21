# Maya — ba cặp nghe thử giọng kể tiếng Việt

Chỉ tạo ba cặp theo `ab_test.excerpts_source_cues` trong gói người dùng gửi.
Chưa tạo lời đọc toàn bài, video, hoặc SRT được căn mới. SRT 17:03,726 là
tài liệu truy nguyên nội dung, không phải thời lượng buộc audio phải theo.

| Trích đoạn | A: pipeline hiện tại | B: adapter JSON |
|---|---:|---:|
| Mở bài, cue 1–7 | 23,472 giây | 23,427 giây |
| Mười ba năm, cue 111–117 | 18,157 giây | 20,620 giây |
| Nhìn lại sự sụp đổ, cue 252–258 | 23,281 giây | 24,760 giây |

Mỗi thư mục có A/B WAV, lời đọc và báo cáo. A/B cùng lời, cùng speaker embedding,
reference codes, vùng Bắc và thiết lập âm sắc của giọng đã chọn. Đổi cách chia
inference nên tín hiệu không giống nhau từng mẫu; seed NumPy được giữ cố định
trong mỗi cặp. Chuẩn hóa mức nghe bằng gain tuyến tính chung theo đo LUFS,
không dùng nhạc nền hoặc nén động toàn cặp để che lỗi.

## Bộ tài liệu đã sử dụng

- Đọc toàn bộ `00_DOC_TRUOC_VA_PROMPT_CODEX.md`.
- TXT dùng kiểm tra đủ lời và so khớp với toàn bộ 36 beat.
- JSON dùng lập kế hoạch cho 36 beat, cụm nhấn, các pause event và protected spans.
- SRT đóng gói dùng đối chiếu đủ 275 cue; SRT `(1)` người dùng gửi trùng từng byte.
- Chỉ `beats[].text` được lấy làm lời nói. `source_cues` giúp truy nguyên vị trí,
  không được đọc lặp. Không đọc title, intent, direction hay số cue.

## Khả năng engine đã đối chiếu

Local: VieNeu-TTS v3 Turbo, SDK 3.8.3, ONNX Runtime 1.31.0, sea-g2p 0.10.0,
CPU/ONNX fp32, WAV 48 kHz. Dùng đúng reference/mã giọng đã chốt; không tải model
lớn mới, không gọi API trả phí. Có hỗ trợ tiếng Việt và lấy giọng từ tham chiếu;
điều này không tự chứng minh phát âm hoặc thanh điệu của sáu file đạt yêu cầu.

Đối chiếu mã `infer`, sampler NumPy, đường normalize/chunk và `_resolve_style_id`
trong SDK cài tại máy với nguồn chính thức:

- https://huggingface.co/pnnbao-ump/VieNeu-TTS-v3-Turbo
- https://github.com/pnnbao97/VieNeu-TTS

Tham số `style` bị bỏ qua ở v3 Turbo. Không truyền JSON như API của engine hoặc
bịa `emotion=...`. Không thêm tiếng cười, thở hay từ đệm. Reference ảnh hưởng
giọng/cách đọc qua speaker embedding và audio codes, không bảo đảm diễn xuất
đúng mọi sắc thái. Native engine có cue âm thanh thử nghiệm nhưng không dùng
trong các mẫu này vì không phù hợp yêu cầu tiết chế.

## Đã ánh xạ và giới hạn

| Ý đồ JSON | Thực thi |
|---|---|
| Câu/cụm phải liền, protected cue spans | Chia bằng câu đủ nghĩa, giữ các khoảng bảo vệ trong cùng đơn vị; kiểm tra cả 36 beat. |
| pace_relative_to_natural_voice | B dùng mức chậm nhẹ có quy tắc, giữ nguyên pitch toàn cục; không đổi ngẫu nhiên. |
| emphasis_phrases | Xấp xỉ bằng speed/gain nhẹ trên toàn cụm nghĩa chứa cụm nhấn. Chưa có nhấn chính xác từng từ/âm tiết bằng alignment. |
| pause_events | Đặt tại ranh giới câu hoàn chỉnh đã tổng hợp; ước lượng phần im lặng có sẵn ở hai mép rồi chỉ bù phần thiếu. Không cắt audio giữa âm tiết. |
| pause_after_ms_target | Dùng ở cuối beat thực sự; event cuối beat thay thế mục tiêu này, không cộng hai lần. |
| tone / intent / direction / emotion_intensity | Giữ làm ý đồ, dùng để diễn giải mức nhịp/gain; không tuyên bố model đã diễn xuất đúng cảm xúc chỉ vì đã đọc JSON. |
| pronunciation_review | Giữ danh sách đầy đủ 18 mục chờ nghe/tra nguồn; các mẫu có Maya, Yucatán, măng đá. Chưa thêm phiên âm chưa kiểm chứng. |

Nghỉ đo tại mép im lặng là ước lượng tín hiệu ở ranh giới đã biết, không phải
forced alignment theo từ. Không trim khoảng nghỉ tự nhiên. Mọi thông số nghỉ,
phần đã có và phần bù được lưu trong report từng cặp. Câu lặp “Mười ba năm.”
là lời có chủ đích trong kịch bản, cần nghe phân biệt với lặp phát sinh từ TTS.

## Trạng thái QC và bước tiếp

**Chưa nghe kiểm tra trực tiếp trong phiên này; không tự báo đạt chất lượng.**
Đã kiểm tra cơ chế adapter, toàn vẹn đầu vào, đủ file, giải mã, clipping,
thời lượng và mức nghe tương đương. Những điều đó không xác nhận đọc đủ lời,
không lặp/mất từ, đúng dấu, đúng vùng, không cụt âm hay nhấn/nghỉ tự nhiên.

Khi nghe, ưu tiên: (1) đủ lời, thanh điệu và giọng Bắc; (2) câu dài không vụn;
(3) “mười ba năm” lặp tự nhiên; (4) tương phản “nhìn lại / từng ngày”; (5) câu hỏi
cuối chân thành, không như lời kêu gọi quảng cáo. Báo cặp, A/B và vị trí cần sửa.
Chỉ sau khi người dùng duyệt mẫu mới tạo toàn bài và căn SRT theo audio cuối.

`model_capabilities.json`, `effective_config.json`, `adapter_plan_36_beats.json`
và `ab_report.json` ghi cấu hình, phần hỗ trợ/xấp xỉ/chưa thực thi và phạm vi QC.
