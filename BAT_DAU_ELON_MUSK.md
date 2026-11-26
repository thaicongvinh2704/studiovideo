# Elon Musk đã trở thành tỷ phú như thế nào?

Bàn giao cuối buổi 26/11/2026 trên nhánh `episode/elon-musk-ty-phu`. **Bản đang chờ chủ kênh nghe duyệt là Ngọc Huyền V2, dài 10 phút 59 giây.** Bản đầu dài 11 phút 16 giây đã nhận phản hồi rằng giọng đọc đều. Tập đang ở bước duyệt tiếng.

## Mở từ đây

- [Nghe toàn bộ V2](projects/elon_musk_01/delivery/Elon_Musk_Ngoc_Huyen_V2.mp3) · [WAV dùng để dựng](projects/elon_musk_01/delivery/Elon_Musk_Ngoc_Huyen_V2.wav) · [28 giây mở đầu](projects/elon_musk_01/delivery/Elon_Musk_V2_Mo_dau.mp3).
- [Kịch bản và chỉ dẫn dựng theo sáu cảnh](projects/elon_musk_01/KICH_BAN.md) · [sổ số liệu và nguồn](projects/elon_musk_01/SO_LIEU.md) · [bản tự biên tập](projects/elon_musk_01/TU_REVIEW_KICH_BAN.md).
- [Lời đọc thật và mốc từng câu trong V2](projects/elon_musk_01/dien_doc_v2/moc_thu.json) · [bảng điều khiển nhịp](projects/elon_musk_01/dien_doc_v2/bang_nhip.txt) · [mã dựng tiếng V2](projects/elon_musk_01/dien_doc_v2/dung_giong.py). V2 đã sửa một số câu cho hợp lời nói. Dùng trường `text`, `start` và `end` trong bảng mốc để khớp hình với tiếng.
- [Bản đầu để so sánh](projects/elon_musk_01/delivery/Elon_Musk_Ngoc_Huyen.mp3) · [39 đoạn thu của bản đầu](projects/elon_musk_01/audio_ngoc_huyen/units/) · [126 đoạn thu của V2](projects/elon_musk_01/dien_doc_v2/takes/). Trong V2, bản thu riêng “Đợi đến tối” có một lần lặp. Mã ghép đã cắt phần lặp trong cả bản mở đầu lẫn bản toàn tập.

## Buổi làm tiếp

1. Nghe V2 theo phản hồi của chủ kênh. Ba mốc đối chiếu là 00:00–00:28 ở phần mở, 05:41–05:49 ở câu đùa Tesla đăng kế hoạch bí mật và 07:48–08:03 khi Falcon 1 cất cánh. Nếu cần sửa, đánh dấu câu trong bảng mốc và chỉnh riêng cụm đó.
2. Sau khi chủ kênh duyệt nhịp kể, dựng nháp 30–45 giây đầu theo WAV V2. Trình bản nháp để duyệt hình và chuyển động trước khi làm tiếp.

## Khôi phục trên máy khác

Clone nhánh `episode/elon-musk-ty-phu` và dùng Git LFS để lấy âm thanh. Trong thư mục gốc của bản clone, chạy `git lfs pull --include="projects/elon_musk_01/**"`. Các MP3 và WAV trong `delivery/` dùng được ngay sau khi tải.

Nếu cần chạy lại bộ dựng tiếng trên máy khác, giải nén [bộ công cụ giọng của tập](projects/elon_musk_01/cong_cu_giong_Elon_Musk.zip) vào gốc một **bản clone làm việc riêng**. Gói giữ nguyên các mô-đun Studio cần cho tập, cấu hình và mẫu nghe đã chọn của Ngọc Huyền. File `MOI_TRUONG_ELON_MUSK.json` trong gói ghi các phiên bản đã dùng. Với Python 3.12, NumPy và FFmpeg trong PATH, chạy `python projects/elon_musk_01/dien_doc_v2/dung_giong.py` từ gốc repo để ráp lại những câu đã lưu. Để sinh lời mới, máy còn cần VieNeu 3.5.0 và bộ mô hình VieNeu-TTS-v3-Turbo cho chế độ ONNX CPU. Script sử dụng bộ nhớ đệm mô hình ngoại tuyến.

## Yêu cầu của chủ kênh

Làm video hoạt họa dài hơn 10 phút, tiếng Việt, mở một loạt phim kể chuyện người thật và hành trình hình thành tài sản. Tập đầu theo chân Elon Musk qua những quyết định, thành công và thất bại có thật, từ Zip2 đến lần đầu Forbes xếp ông vào danh sách tỷ phú. Giải thích từng khoản tiền bằng hình phù hợp ngay khi lời kể nhắc tới. Kể sao cho người chưa biết cổ phiếu vẫn theo được.

Chủ kênh muốn studio tự vẽ nhân vật bằng code, theo nét hoạt họa mềm đã thử, đầu lớn, thân gọn, mặt có mắt và mũi, để trống phần miệng. Cảnh có chuyển động có mục đích, chủ yếu đổi dáng, giật nhẹ, cắt góc hoặc chuyển động của vật thể. Khi dùng biểu đồ, phần đang nói phải thực sự tách, chạy, lớn lên hoặc được khoanh theo thời gian. Tránh thẻ chữ kéo dài. [Mẫu nét Trump vẽ bằng code](projects/elon_musk_01/mau_net/Trump_but_mem_V03.png) và [mã mẫu](projects/elon_musk_01/mau_net/ve_trump_but_mem.py) là tài liệu thử bút. Nhân vật Trump thuộc thử nghiệm trước, không xuất hiện trong tập Musk.

## Bối cảnh lúc lập dàn ý

- **Đã xác định với người dùng** — chủ đề là hành trình trở thành tỷ phú. Người dùng đã chỉnh lại cách hiểu cũ chỉ tập trung vào mức tăng tài sản năm 2020–2021. Câu chuyện Wave Alpha thuộc một hướng từng được gợi ý.
- **Đề xuất đang bàn giao** — nhắm khoảng 12 phút, mở ở lần phóng Falcon 1 thứ tư, quay về Zip2, kết ở Forbes 2012. Một giọng kể ngoài hình xuyên suốt. Mỏ Đen xuất hiện ngắn khi minh họa tiền đầu tư, nhường trọn cảnh bãi phóng cho nhân vật và đội ngũ. Người dùng chưa duyệt riêng lời dẫn, thời lượng từng đoạn hay vai trò này.
- **Đã có** — góc kể, nháp mở màn, dàn ý dưới đây, sổ nguồn và quy tắc dựng biểu đồ. Mẫu nét đính kèm cho thấy Bàn vẽ Studio dùng được Bézier và Perfect Freehand. Thư viện dáng Mỏ Đen có sẵn trong [manifest](assets/characters/mo_den/manifest.json). [Hướng dẫn Bàn vẽ](DRAWING_DESK_GUIDE.md).
- **Tại thời điểm lập dàn ý, chưa sản xuất** — kịch bản hoàn chỉnh, giọng đọc, thời lượng đo bằng âm thanh, nhân vật Musk, storyboard chi tiết, biểu đồ đã dựng, timeline và video. Quy ước của chủ kênh là xem bản dựng trước khi cho xuất phim hoàn chỉnh.

## Mạch khoảng 12 phút

| Mốc dự kiến | Lời kể cần giải đáp | Chỉ dẫn hình |
|---|---|---|
| 0:00–0:35 | Sau ba lần thất bại, SpaceX còn đủ tiền thử mấy lần? | Bệ phóng và phòng điều khiển. Dừng đếm ngược trước khi lộ kết quả. Cắt sang màn hình máy tính của Zip2. |
| 0:35–3:00 | Hai anh em Elon và Kimbal bán thứ gì ở Zip2? Musk có khoản vốn lớn đầu tiên ra sao? | Cho thấy một địa chỉ doanh nghiệp trên bản đồ trực tuyến thời kỳ đầu. Đến thương vụ Compaq năm 1999 mới hiện phần Musk thu được. |
| 3:00–5:30 | Từ X.com đến PayPal, vì sao thương vụ 1,5 tỷ USD chỉ mang về cho Musk một phần? | Dựng một giao dịch thanh toán, rồi chuyển sang giá mua của eBay. Tách riêng nhãn chủ thể và phần của Musk. |
| 5:30–8:45 | Musk đem tiền đi đâu và chuyện gì xảy ra khi Tesla khó gọi vốn, còn SpaceX phóng trượt? | Thanh vốn chia vào ba công ty. Theo nhánh tên lửa trở lại cảnh mở. Lần phóng thứ tư thành công. Cắt riêng sang vòng gọi vốn của Tesla vào đêm Giáng sinh 2008. |
| 8:45–12:00 | Từ tiền đầu tư đến tài sản ước tính diễn ra như thế nào? | Tesla lên sàn năm 2010. Dựng hai mốc Forbes 2011 và 2012 cùng thang đo rồi tách phần sở hữu ở các công ty. Kết ở lần đầu vào danh sách. |

**Lời dẫn thử, có thể viết lại.** “Năm 2008, SpaceX đã phóng ba lần. Cả ba lần đều thất bại. Musk kể rằng họ chỉ còn đủ tiền cho một lần nữa. Sáu năm trước, ông vừa có khoảng 180 triệu đô từ thương vụ PayPal. Số tiền ấy đã đi đâu mà giờ mọi người trong phòng điều khiển phải chờ vào lần đếm ngược này?” Đây là lời người dẫn. Khi tái hiện lịch sử, tránh tự đặt lời thoại vào miệng Musk.
