# MỎ ĐEN — BỘ HÌNH TÁI SỬ DỤNG 01

24 hình gốc bằng vector, dành cho video lịch sử và bí ẩn 16:9. Đây là bộ hỗ trợ trình bày, chưa phải bộ nhân vật/bối cảnh lịch sử. Phong cách đang chờ người dùng duyệt.

## Trong bộ file
- PNG/: 24 ảnh riêng, RGBA 2560 × 1440, nền trong suốt thật, không có chữ hay watermark.
- SVG/: 24 bản đường nét chỉnh sửa được, canvas 1600 × 900 (16:9).
- XEM_TRUOC.png: bảng xem toàn bộ; nền ô vuông và chữ ở bảng này không nằm trong ảnh rời.
- manifest.json: tên, mục đích, đường dẫn, vùng đặt nội dung và vùng có hình của từng tài sản để Codex chọn đúng file.
- SOURCE/build_assets.py: mã nguồn tạo bộ bằng Inkscape + Pillow (chạy với Python 3, sửa ROOT theo máy sử dụng).

## Cách dùng
1. Đọc manifest.json, chọn tài sản theo mục đích, không chọn chỉ theo số thứ tự.
2. Khung rỗng: đặt ảnh bên dưới; crop/mask ảnh theo content_regions. Các vùng này dùng tọa độ viewBox 1600 × 900; nhân 1.6 khi làm việc trên PNG 2560 × 1440.
3. Đặt chữ, nguồn ảnh và niên đại ở lớp riêng. Thẻ 15, 17, 18 có nền kem đặc; các khung 11–14, 16 có vùng trung tâm trong suốt.
4. Không kéo giãn PNG mất tỷ lệ. Có thể xoay/lật mũi tên; chỉnh đường nối và vị trí mốc trong SVG khi cần.
5. PNG dùng toàn canvas 16:9 để giữ nét đồng nhất. alpha_bbox_px cho biết vùng có hình nếu cần cắt gọn.
6. Hình vector có thể xuất lại ở kích thước lớn hơn. PNG hiện tại được Inkscape render trực tiếp từ vector, không phóng lớn ảnh raster.

## Quy tắc phong cách
Viền nâu đen tròn mềm; màu kem và nâu làm nền chính; xám xanh và đất nung chỉ là màu nhấn. Bảng màu là đề xuất theo ảnh Mỏ Đen đã xem, chưa được đo màu để khớp tuyệt đối. Đây là đồ họa chức năng nên đường nét đơn giản hơn nhân vật.

## Độ chính xác nội dung
- Mũi tên, trục thời gian và sơ đồ là thành phần trình bày, không phải bằng chứng.
- Các mốc chia đều không mặc định biểu thị khoảng thời gian bằng nhau.
- Sơ đồ 23 chỉ là mẫu phân nhánh trống, không phải cây tiến hóa loài người. Phải dựng lại nhánh dựa trên nguồn khoa học nếu dùng cho chủ đề đó.
- Khoảng trống tư liệu không tự đồng nghĩa với điều siêu nhiên hoặc một sự kiện bí ẩn.
- Không chứa ảnh thực tế, bản đồ, cổ vật hoặc nội dung lấy từ video tham khảo. Video tham khảo tải lỗi nên chưa được phân tích.
- Không bao gồm bộ Mỏ Đen 24 biểu cảm gốc.

## Kiểm tra bản giao
Đã kiểm tra đủ 24 SVG + 24 PNG, kích thước, kênh alpha, vùng hình nằm trọn trong canvas và xem bảng tổng hợp. Chất lượng khớp phong cách cuối cùng cần người dùng duyệt. Chưa triển khai kết nối studio tự động.

## Danh mục

- **01_arrow_straight — Mũi tên thẳng**: Chỉ một chi tiết hoặc hướng thay đổi; xoay/lật tùy bố cục.

- **02_arrow_curved — Mũi tên cong**: Nối hai chi tiết ở vị trí lệch nhau.

- **03_arrow_double — Mũi tên hai chiều**: So sánh hoặc chỉ khoảng cách; thêm số đo riêng khi có nguồn.

- **04_route_dashed — Đường dẫn đứt đoạn**: Minh họa đường đi mang tính sơ đồ; không thay thế bản đồ chính xác.

- **05_focus_oval — Vòng khoanh chi tiết**: Khoanh vùng đáng chú ý trên ảnh tư liệu; phần giữa trong suốt.

- **06_focus_corners — Bốn góc đánh dấu**: Đánh dấu một vùng chữ nhật mà không che nội dung.

- **07_group_bracket — Ngoặc nhóm**: Gom nhiều hình vào một nhóm khái niệm.

- **08_detail_connector — Đường nối chi tiết**: Nối điểm trên ảnh với ô giải thích; thêm ô và chữ riêng.

- **09_emphasis_rays — Nét nhấn phát hiện**: Đặt quanh chủ thể để nhấn khoảnh khắc nhận ra hoặc bất ngờ.

- **10_underline — Gạch chân mềm**: Gạch dưới tiêu đề hoặc một cụm từ; chữ đặt riêng.

- **11_evidence_frame — Khung ảnh tư liệu**: Đặt ảnh thực tế bên dưới khung. Nhãn kem dành cho tiêu đề ngắn.

- **12_comparison_pair — So sánh hai bên**: Đặt hai ảnh hoặc hai cách giải thích cạnh nhau.

- **13_detail_inset — Khung phóng to chi tiết**: Đặt ảnh tổng thể bên trái, ảnh cắt cận bên phải. Đường nối minh họa có thể chỉnh SVG.

- **14_quotation_frame — Khung trích dẫn**: Nhập trích dẫn ở giữa và nguồn ở góc dưới; không tự coi câu kể là trích dẫn.

- **15_note_card — Thẻ ghi chú**: Thẻ nền đặc để đặt lời giải thích ngắn.

- **16_hypothesis_cards — Ba thẻ giả thuyết**: Đặt ba khả năng hoặc ba nhóm chứng cứ. Các thẻ cùng kích thước không thể hiện xác suất.

- **17_source_caption — Thẻ nguồn tư liệu**: Đặt nguồn ảnh, bảo tàng, tác giả hoặc chú thích. Thay chữ riêng theo từng tư liệu.

- **18_callout_bubble — Ô giải thích có đuôi**: Đặt một ý giải thích hoặc lời dẫn ngắn của Mỏ Đen.

- **19_timeline_four — Trục thời gian bốn mốc**: Sơ đồ thứ tự bốn mốc. Khoảng cách mặc định không biểu diễn số năm.

- **20_timeline_gap — Khoảng trống tư liệu**: Đánh dấu vùng thiếu dữ liệu hoặc thời gian chưa rõ; phải giải thích bằng chữ, không mặc định là sự kiện bí ẩn.

- **21_sequence_three — Ba bước nối tiếp**: Đặt ba hình minh họa theo trình tự. Không tự suy ra quan hệ nguyên nhân.

- **22_timeline_parallel — Hai dòng thời gian**: So sánh hai chuỗi sự kiện; vị trí mốc cần chỉnh nếu thể hiện thời gian thực.

- **23_branch_diagram — Sơ đồ phân nhánh**: Sơ đồ khái niệm ba nhánh; không phải cây tiến hóa có căn cứ. Khi minh họa tiến hóa phải sửa cấu trúc theo nguồn.

- **24_duration_span — Dấu khoảng thời gian**: Gom một giai đoạn; nhập nhãn khoảng thời gian vào thẻ bên dưới.
