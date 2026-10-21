# Demo A/B giọng kể tiếng Việt

**Người dùng đã chốt bản B làm chuẩn giọng và cách kể của dự án.**
Voice Studio mặc định chọn **Mỏ Đen · giọng Bắc · bản B**. WAV B được giữ nguyên;
hồ sơ giọng lưu nhịp nền và các mức nhấn/nghỉ để dựng lời mới theo nội dung.

- A: `A_giong_ke_tieng_viet.wav`, 51 giây, kể đều tự nhiên.
- B: `B_giong_ke_tieng_viet.wav`, khoảng 52,6 giây, thêm nhịp/nghỉ/cường độ vừa đủ.
- Cùng văn bản đã chuẩn hóa, cùng các đoạn lời tổng hợp gốc, cùng mã giọng Bắc
  đã được người dùng xác nhận. Không đổi sang preset hay vùng giọng khác.
- Cùng thiết lập âm sắc toàn cục của mẫu 04. B không thêm bẻ cao độ, rung giọng,
  nhạc nền, thẻ cảm xúc thử nghiệm hoặc cách đọc quảng cáo.

Kịch bản gốc: `kich_ban_goc.txt`. Bản đưa vào TTS: `kich_ban_doc.txt`.
Từng thay đổi cách đọc có offset, bản gốc và lý do trong `doi_chieu_cach_doc.json`.
Số và tên chỉ thay trong câu thử có ngữ cảnh, không là quy tắc thay toàn dự án.
Câu sáu thanh là phép thử cố ý; các dấu phẩy khác không được dùng để cắt thành
từng clip. Mỗi đoạn tổng hợp là một ý trọn vẹn; chunk thực tế của engine được
lưu trong `bao_cao.json` để đối chiếu.

Ví dụ cách đọc đã chọn riêng cho bài thử: 21/10/2026 đọc đủ ngày/tháng/năm;
2,5 km đọc hai phẩy năm ki lô mét; TP.HCM đọc thành phố Hồ Chí Minh;
UNESCO và New York có cách đọc Việt hóa để giữ lời kể tiếng Việt.

VieNeu-TTS v3 Turbo có tiếng Việt và chức năng lấy giọng tham chiếu; SDK đang
chạy là 3.8.3, CPU/ONNX fp32. Mã tham chiếu gồm speaker embedding và audio codes,
có thể ảnh hưởng cả chất giọng/cách đọc. Tham số `style` bị bỏ qua ở v3 Turbo;
không có lời hứa diễn xuất chính xác hay đúng mọi thanh.
Nguồn: https://huggingface.co/pnnbao-ump/VieNeu-TTS-v3-Turbo .

**Trạng thái: bản để nghe đối chiếu, chưa đánh dấu đạt chất lượng nghe.**
Các kiểm tra duration, định dạng, tính toàn vẹn, cùng văn bản và cùng mã giọng
chỉ xác nhận cơ chế. Chưa có QC nghe độc lập cho đọc đủ lời, sáu thanh, vùng Bắc
nhất quán, cụm nghĩa, tên riêng hoặc mức biểu cảm. Reference đã giảm nhiễu nhưng
chưa xác nhận sạch hết nhạc nền/chỉ một người nói qua nghe. Khi nghe có lỗi phải
sửa đúng đoạn, không bẻ cao độ để che lỗi thanh hoặc suy ra PASS từ waveform.
