# Mỏ Đen — kho nhân vật chính

**Cập nhật mới nhất: đủ 24/24 ảnh dùng được.** Ba file thay thế 03, 18, 21 đã nhận, đọc đầy đủ bằng Pillow và Qt, có alpha thật và giữ nguyên byte trong kho. Tệp hỏng từ ZIP cũ chỉ giữ để lưu nguồn; manifest trỏ sang bản thay thế. Chân vẫn cùng đường chuẩn; ảnh 03 nghiêng và lệch trái hơn trạng thái mặc định nên cần xem vị trí khi đổi ảnh. Xem `qc/named_24_v01/replacements_background_check.png`.

Các kết quả 21/24 bên dưới là lịch sử kiểm tra gói ZIP trước khi nhận bản thay thế.

Người dùng chọn Mỏ Đen thay người dẫn hoạt họa. Đã nhận `Mo_Den_Studio_Named_24_PNG.zip` và kiểm tra: **21 PNG dùng được để ghép cảnh tĩnh; 3 PNG thiếu dữ liệu cần gửi lại**. Bản ZIP và mọi ảnh gốc được giữ tại `incoming/named_24_v01/`; 21 ảnh hợp lệ được chép nguyên byte vào `library/named_24_v01/`.

## Kết quả kiểm tra bộ 24 ảnh

- Cả Pillow và bộ đọc Qt của Studio xác nhận ảnh 03 **Cười lớn**, 18 **Cười gượng**, 21 **Bất lực** không giải mã đầy đủ được. ZIP CRC vẫn đúng: lỗi nằm trong dữ liệu PNG có sẵn trong gói, không phải lỗi giải nén. Không cố đọc nửa ảnh hoặc tự vẽ phần thiếu.
- 21 ảnh còn lại đều RGBA, 2048 × 2048, có alpha từ 0 đến 255, không chạm mép canvas. Đã xem toàn bộ biểu cảm trên bảng ảnh và thử ảnh 01/08/24 trên nền trắng và tối: không thấy nền trắng đóng sẵn hoặc viền trắng rõ ở cỡ ghép thử.
- Mặt nạ, màu thân, mắt, tai, chân và đuôi nhận diện nhất quán. Chân dưới cùng ở y=1779–1780 px; giữ nguyên canvas khi đổi biểu cảm. Đầu/tai hạ ở ảnh buồn/sợ là thay đổi tư thế có chủ đích.
- 01 dùng làm trạng thái mặc định, 08 cho nét láu cá, 13 tò mò, 14 hoài nghi, 15 suy nghĩ, 16 nhận ra và 24 giải thích. Tên và tình huống dùng khác nằm trong manifest. Không đoán đường dẫn.
- README của gói nói ảnh 2048 đã được phóng từ nguồn 1254 px; đây là thông tin nhà cung cấp, chưa xác minh độc lập. Phù hợp dùng nhân vật ở một phần khung; không suy ra ảnh có chi tiết 2048 gốc.
- Chưa có tư thế chỉ trái/phải chính xác, nắm đạo cụ hay góc quay lưng. Chỉ yêu cầu bổ sung khi kịch bản cần, chưa cần tạo thêm hàng loạt.
- Tệp PNG đã được Qt ghép thử thành công; luồng chọn kho mèo và QC xuất riêng cho mèo **chưa được tích hợp trong lần kiểm tra này**.

Xem `qc/named_24_v01/contact_sheet.png`, `background_check.png` và `audit.json`. Manifest ghi nhận xét cụ thể cho từng ảnh hợp lệ; ảnh hỏng không có đường dẫn dùng trong library.

## Nhận diện giữ cố định

Mèo thân tròn nhỏ, lông kem/nâu nhạt; mặt nạ, tai, bàn chân và đuôi nâu đậm; mắt xanh xám; viền đậm đơn giản. Bản chính có mắt hơi khép, nét tinh nghịch. Khi đổi cảm xúc vẫn giữ hình đầu, mảng màu, tỷ lệ thân và đuôi. Đây là mô tả ảnh tham chiếu, không tự đổi tên nhân vật thành giống mèo hoặc thiết kế khác.

## Cấu trúc kho

- `references/`: ảnh để đối chiếu. Không cắt nhân vật nhỏ từ screenshot để dùng làm thành phẩm.
- `incoming/`: bản gốc người dùng gửi; giữ nguyên.
- `library/`: tài sản đã kiểm tra để tái sử dụng, sau khi nhận ảnh rời.
- `manifest.json`: nhận diện và danh mục đủ 24 mục, cả 24 mục hiện dùng được và có trường `file` trỏ vào library; ba bản thay giữ đường dẫn và hash của bản hỏng trước đó để tra nguồn.

Mỗi mục ảnh cần ghi ID, file gốc, file dùng trong Studio, biểu cảm, tư thế, góc nhìn, hướng nhìn/chỉ, toàn thân/bán thân, đạo cụ, kích thước, alpha, hash và trạng thái kiểm tra. Tên gợi ý: `mo_den_point_right_curious_full_v01.png`. Không ghi approved trước khi thực sự kiểm tra/được duyệt theo phạm vi.

## Bộ ảnh khởi đầu đề nghị

Ưu tiên 8 ảnh toàn thân, cùng kích thước canvas và tỷ lệ nhân vật:

1. Ngồi bình thường, nét tinh nghịch mặc định.
2. Tò mò, hơi nghiêng đầu.
3. Suy nghĩ.
4. Ngạc nhiên.
5. Hoài nghi, nhướng mày.
6. Vui/cười.
7. Chỉ sang trái khung hình.
8. Chỉ sang phải khung hình.

Mở rộng theo kịch bản: lo lắng, buồn, tự tin, giải thích với chân trước mở, cầm đạo cụ cụ thể, góc ba phần tư hoặc quay lưng. Không yêu cầu mọi cảm xúc × mọi dáng × mọi góc nhìn ngay từ đầu. Không cần ảnh miệng nói/nhắm mắt nếu chưa có nhu cầu diễn hoạt nhân vật.

## Định dạng yêu cầu

- PNG nền trong suốt thật; không nền ô caro được vẽ sẵn.
- Mỗi file một nhân vật/tư thế, không chữ, watermark, viền giao diện hoặc bảng nhiều ô.
- Khởi đầu có thể dùng canvas vuông 2048 × 2048, chừa khoảng quanh tai, chân và đuôi. Giữ tỷ lệ/căn chân tương đối giữa các ảnh cùng loại.
- Không gắn mũi tên, lời thoại hay nền vào ảnh nhân vật. Chú giải vẽ riêng bằng vector trong Studio.
- Gửi một ảnh mặc định riêng trước để kiểm tra nhận diện, alpha và khả năng ghép cảnh; sau đó bổ sung bộ biểu cảm.

## Quy trình dựng video

Viết kịch bản và chia cảnh trước. Kiểm tra danh mục, chọn ảnh đang có theo mục đích cảnh. Chỉ yêu cầu người dùng bổ sung ảnh còn thiếu, nêu tư thế, biểu cảm, hướng, đạo cụ và lý do dùng. Đặt nhân vật tĩnh hoặc biến đổi vị trí/kích thước theo đạo diễn; mũi tên, đường nước, gạch rơi và chú giải là các lớp độc lập.

Kiểm tra mèo theo nhận diện, cấu trúc chân/đuôi phù hợp cách điệu, không cụt/cắt ngoài ý muốn, viền tách nền, độ phân giải, alpha và nhất quán. Không dùng tiêu chí giải phẫu/ngón tay của người cho mèo.

Hiện cổng QC của Studio có những kiểm tra riêng cho người; việc lưu tham chiếu này chưa thay đổi cổng xuất hoặc triển khai nhập ảnh mèo. Khi tích hợp ảnh thật nhận được phải bổ sung luồng phù hợp, giữ nguyên chặn các hình người đã bị loại.
