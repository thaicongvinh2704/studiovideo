# Elon Musk đã trở thành tỷ phú như thế nào?

Hồ sơ tiếp quản ngày 26/11/2026 · Nhánh `episode/elon-musk-ty-phu`. Đọc tiếp [sổ số liệu và chỉ dẫn biểu đồ](projects/elon_musk_01/SO_LIEU.md). Hai tài liệu này đủ để bắt đầu viết tập đầu trong một chat mới.

## Yêu cầu của chủ kênh

Làm video hoạt họa dài hơn 10 phút, tiếng Việt, mở một loạt phim kể chuyện người thật và hành trình hình thành tài sản. Tập đầu theo chân Elon Musk qua những quyết định, thành công và thất bại có thật, từ Zip2 đến lần đầu Forbes xếp ông vào danh sách tỷ phú. Giải thích từng khoản tiền bằng hình phù hợp ngay khi lời kể nhắc tới. Kể sao cho người chưa biết cổ phiếu vẫn theo được.

Chủ kênh muốn studio tự vẽ nhân vật bằng code, theo nét hoạt họa mềm đã thử, đầu lớn, thân gọn, mặt có mắt và mũi, để trống phần miệng. Cảnh có chuyển động có mục đích, chủ yếu đổi dáng, giật nhẹ, cắt góc hoặc chuyển động của vật thể. Khi dùng biểu đồ, phần đang nói phải thực sự tách, chạy, lớn lên hoặc được khoanh theo thời gian. Tránh thẻ chữ kéo dài. [Mẫu nét Trump vẽ bằng code](projects/elon_musk_01/mau_net/Trump_but_mem_V03.png) và [mã mẫu](projects/elon_musk_01/mau_net/ve_trump_but_mem.py) là tài liệu thử bút. Nhân vật Trump thuộc thử nghiệm trước, không xuất hiện trong tập Musk.

## Quyết định biên tập và tình trạng

- **Đã xác định với người dùng** — chủ đề là hành trình trở thành tỷ phú. Người dùng đã chỉnh lại cách hiểu cũ chỉ tập trung vào mức tăng tài sản năm 2020–2021. Câu chuyện Wave Alpha thuộc một hướng từng được gợi ý.
- **Đề xuất đang bàn giao** — nhắm khoảng 12 phút, mở ở lần phóng Falcon 1 thứ tư, quay về Zip2, kết ở Forbes 2012. Một giọng kể ngoài hình xuyên suốt. Mỏ Đen xuất hiện ngắn khi minh họa tiền đầu tư, nhường trọn cảnh bãi phóng cho nhân vật và đội ngũ. Người dùng chưa duyệt riêng lời dẫn, thời lượng từng đoạn hay vai trò này.
- **Đã có** — góc kể, nháp mở màn, dàn ý dưới đây, sổ nguồn và quy tắc dựng biểu đồ. Mẫu nét đính kèm cho thấy Bàn vẽ Studio dùng được Bézier và Perfect Freehand. Thư viện dáng Mỏ Đen có sẵn trong [manifest](assets/characters/mo_den/manifest.json). [Hướng dẫn Bàn vẽ](DRAWING_DESK_GUIDE.md).
- **Chưa sản xuất cho tập này** — kịch bản hoàn chỉnh, giọng đọc, thời lượng đo bằng âm thanh, nhân vật Musk, storyboard chi tiết, biểu đồ đã dựng, timeline và video. Quy ước của chủ kênh là xem bản dựng trước khi cho xuất phim hoàn chỉnh.

## Mạch khoảng 12 phút

| Mốc dự kiến | Lời kể cần giải đáp | Chỉ dẫn hình |
|---|---|---|
| 0:00–0:35 | Sau ba lần thất bại, SpaceX còn đủ tiền thử mấy lần? | Bệ phóng và phòng điều khiển. Dừng đếm ngược trước khi lộ kết quả. Cắt sang màn hình máy tính của Zip2. |
| 0:35–3:00 | Hai anh em Elon và Kimbal bán thứ gì ở Zip2? Musk có khoản vốn lớn đầu tiên ra sao? | Cho thấy một địa chỉ doanh nghiệp trên bản đồ trực tuyến thời kỳ đầu. Đến thương vụ Compaq năm 1999 mới hiện phần Musk thu được. |
| 3:00–5:30 | Từ X.com đến PayPal, vì sao thương vụ 1,5 tỷ USD chỉ mang về cho Musk một phần? | Dựng một giao dịch thanh toán, rồi chuyển sang giá mua của eBay. Tách riêng nhãn chủ thể và phần của Musk. |
| 5:30–8:45 | Musk đem tiền đi đâu và chuyện gì xảy ra khi Tesla khó gọi vốn, còn SpaceX phóng trượt? | Thanh vốn chia vào ba công ty. Theo nhánh tên lửa trở lại cảnh mở. Lần phóng thứ tư thành công. Cắt riêng sang vòng gọi vốn của Tesla vào đêm Giáng sinh 2008. |
| 8:45–12:00 | Từ tiền đầu tư đến tài sản ước tính diễn ra như thế nào? | Tesla lên sàn năm 2010. Dựng hai mốc Forbes 2011 và 2012 cùng thang đo rồi tách phần sở hữu ở các công ty. Kết ở lần đầu vào danh sách. |

**Lời dẫn thử, có thể viết lại.** “Năm 2008, SpaceX đã phóng ba lần. Cả ba lần đều thất bại. Musk kể rằng họ chỉ còn đủ tiền cho một lần nữa. Sáu năm trước, ông vừa có khoảng 180 triệu đô từ thương vụ PayPal. Số tiền ấy đã đi đâu mà giờ mọi người trong phòng điều khiển phải chờ vào lần đếm ngược này?” Đây là lời người dẫn. Khi tái hiện lịch sử, tránh tự đặt lời thoại vào miệng Musk.

## Việc tiếp theo cho AI nhận bàn giao

1. Viết bản lời kể tiếng Việt đầu tiên theo từng cảnh, mở bằng hành động. Mỗi cảnh có lời đọc, hình chuyển động, số liệu hoặc nguồn khi cần, và lý do chuyển sang cảnh sau. Giữ khoảng ngừng trước kết quả lần phóng thứ tư.
2. Đọc thử để đo độ dài thực tế. Nếu thiếu thời lượng, đào sâu một lựa chọn thực sự khó hoặc một sản phẩm cụ thể. Mốc giờ trong hồ sơ chỉ là ước lượng dựng.
3. Trình kịch bản và nháp hình 30–45 giây đầu để chủ kênh đánh giá cách kể và tạo hình Musk. Bản Trump chỉ minh họa kỹ thuật nét. Dựng bằng công cụ của studio. Khi làm giọng, kiểm tra lựa chọn giọng hiện hành trước khi tổng hợp.
