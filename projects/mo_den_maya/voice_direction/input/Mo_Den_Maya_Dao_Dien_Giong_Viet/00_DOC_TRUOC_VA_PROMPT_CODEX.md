# Bộ đạo diễn giọng kể tiếng Việt — Mỏ Đen: Maya

Bản này bổ sung chỉ đạo diễn đạt cho lời kể đã biên tập. Chưa tạo hoặc nghe kiểm tra audio; chưa biết model TTS của dự án. Các chỉ dẫn là ý đồ biên tập để Codex ánh xạ vào tính năng thật của model.

## Cách dùng

1. Giải nén và đưa cả thư mục vào dự án studio mà Codex đang sửa.
2. Dùng giọng/reference audio đã chọn trong dự án. Bộ này không chứa audio mẫu.
3. Dán phần PROMPT CHO CODEX bên dưới vào Codex.
4. Nghe bản thử A/B trước. Khi đã chốt giọng, tạo toàn bài rồi căn lại SRT theo audio mới.

## Các file

- `01_Loi_Ke_Sach.txt`: toàn bộ lời kể, chia đoạn theo ý, không chứa timecode hay chỉ dẫn để đọc thành tiếng.
- `02_Dao_Dien_Giong_Viet.json`: 36 đoạn đạo diễn với sắc thái, nhịp, cụm cần nhấn, điểm nghỉ, các câu cần giữ liền và danh sách tên cần nghe kiểm tra. `beats[].text` là lời đọc. Các trường khác là chỉ dẫn.
- `03_Maya_Timecode_Tham_Chieu.srt`: 275 đoạn với timecode của bản đã biên tập; chỉ dùng để đối chiếu khi tạo voice mới. Đây chưa phải phụ đề được căn với audio mới.

## PROMPT CHO CODEX

Hãy áp dụng bộ đạo diễn này vào hệ thống TTS tiếng Việt hiện tại của dự án và tạo bản nghe thử. Làm việc một agent tại một thời điểm; ưu tiên local, không dùng API trả phí.

Đầu tiên, đọc repo và xác định engine, version, đường inference, giọng/reference đang dùng, giới hạn độ dài và cách xử lý tiếng Việt. Xác nhận bằng code và tài liệu chính thức những điều khiển thực sự hỗ trợ. Không bịa tham số cảm xúc, không coi JSON này là định dạng mà engine tự hiểu.

Tạo adapter chuyển ý đồ trong JSON thành điều khiển hợp lệ của engine. Nếu engine hỗ trợ style/prosody/reference performance, dùng đúng cơ chế. Nếu không hỗ trợ, ghi rõ phần chưa thực hiện được; vẫn có thể cải thiện chia cụm và khoảng nghỉ ở lớp pipeline. Không tuyên bố đã tạo cảm xúc chỉ vì đã đọc file JSON hoặc thêm khoảng lặng. Đề xuất thay model khi có bằng chứng về giới hạn; trước khi tải model lớn, nêu dung lượng và khả năng chạy trên phần cứng thực tế.

Giữ giọng và vùng giọng hiện tại. Nếu chưa có giọng/reference được chọn, hỏi người dùng thông tin còn thiếu; không tự chọn giọng thay thế. Không làm mất thanh điệu tiếng Việt để đạt một đường cao độ giả định. Không đổi tốc độ, pitch hoặc âm lượng ngẫu nhiên. Không thêm tiếng khóc, cười, thở hay tiếng đệm tự phát.

Lấy lời đọc từ beats[].text. Không đọc title, intent, tone, direction, số cue, timecode hoặc tên trường JSON. Cũng không đọc lặp source_cues sau beats: hai phần là hai biểu diễn của cùng nội dung. Giữ nguyên nội dung; chuẩn hóa cách đọc chỉ trong lớp TTS và lưu ánh xạ về bản gốc.

Mỗi beat là một cụm ý để hiểu ngữ cảnh, không phải ràng buộc một lần inference. Chia cụm câu hoàn chỉnh khi cần theo giới hạn engine. Không tạo 275 mẩu audio riêng theo cue SRT. Các protected_cue_spans đánh dấu những câu/cụm không được cắt tại ranh giới phụ đề; đồng thời rà các ranh giới còn lại theo cú pháp. Đặc biệt giữ liền khoảng số bốn mươi mốt đến năm mươi tư phần trăm.

pause_events và pause_after_ms_target là thời lượng nghỉ tổng mong muốn tại vị trí tương ứng, có thể điều chỉnh khi nghe. Tìm đúng vị trí trong audio trước khi thêm nghỉ, bằng alignment hoặc ranh giới câu khi tổng hợp. Nếu audio đã ngừng thì chỉ bù phần thiếu. Khi event trùng cuối beat, dùng event thay cho pause_after; không cộng dồn. Không cắt giữa âm tiết, không trim sạch khoảng nghỉ tự nhiên. Không bắt audio chạy theo thời lượng SRT cũ.

Kiểm tra phát âm các tên trong pronunciation_review. Không tự bịa phiên âm. Nếu engine có từ điển phát âm, chỉ thêm cách đọc đã kiểm tra và giữ nguyên chính tả của tên trong phụ đề.

Tạo ba cặp thử theo ab_test.excerpts_source_cues: mở bài, mười ba năm, và đoạn nhìn lại sự sụp đổ. Mỗi cặp dùng cùng lời và cùng speaker: baseline bằng pipeline hiện tại, directed bằng pipeline đã cải tiến. Giữ seed nếu engine hỗ trợ, chuẩn bị âm lượng nghe so sánh tương đương, bảo toàn độ mạnh nhẹ trong câu. Cache audio và chỉ tạo lại phần thay đổi. Không render video hoặc toàn bộ 17 phút ở bước này.

Kiểm tra audio có đủ lời, không lặp/mất từ, không đọc chỉ dẫn, không cắt âm đầu/cuối, không clipping hoặc lỗi nối. Kiểm tra bằng nghe: đúng dấu tiếng Việt; cùng giọng xuyên suốt; nhấn đúng ý; nghỉ tự nhiên; không đều đều, không diễn quá mức. Chỉ số tự động không thay thế nghe. Nếu không có khả năng nghe, nói rõ và giao các file thử để tôi chọn; không tự báo đạt.

Sau khi tôi chọn bản đọc thử, tạo full narration, căn lời theo audio cuối, rồi xuất SRT mới. Kiểm tra lại tên riêng và mốc cue sau alignment. Không gọi SRT tham chiếu là đã đồng bộ. Đầu ra gồm demo A/B, cấu hình thực dùng, báo cáo khả năng model và các trường đã/chưa thực thi; sau bước chốt demo mới có narration đầy đủ và SRT đã căn.

## Trạng thái và phạm vi

Lời kể giữ nguyên bản SRT đã biên tập, không bổ sung kiểm chứng lịch sử mới. Mốc SRT cũ dài 17:03,726; thời lượng audio mới có thể khác. Các con số nghỉ là điểm bắt đầu để thử nghe, không phải kết quả đo giọng người. Bộ hướng dẫn này chưa chứng minh engine hiện tại tạo được mọi sắc thái yêu cầu.
