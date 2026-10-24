# Kiểm tra bản dựng để duyệt — 24/10/2026

## Những gì đã thực sự xem và chạy

- Đã mở ba reference explainer thực; giữ chúng là tài liệu hướng dẫn, không cắt người từ reference vào phim. Hình người trong tập này là các ảnh supplied có sẵn của gói Phong Thần, giữ nguyên nhận diện và tư thế, không vẽ/sinh lại người.
- Đã mở catalog cảnh nguồn và các bảng ảnh xuyên suốt 9 phần. Đã sửa ba họ bối cảnh bị vượt số lần mặc định; đổi cảnh trao bảo vật sang cận bàn tay, cảnh roi sang cận điểm khắc chế thất bại, cảnh xét tội sang người bị hỏi.
- Các crop Y08/Y09 đã hạ khỏi mảnh nhãn bị cắt, đồng thời giữ khuôn mặt người trẻ/già. Cận K31 chuyển vào cuộn sắc thay vì cắt nửa đầu hai người; cận K19 vào bàn cờ; cận Y07 vào gương mặt. Nhân vật ngồi/quỳ được đặt theo đúng tỉ lệ, không biến dạng tay chân.
- Các nhịp Mỏ Đen được dàn dựng theo ý, không còn 21 lần cùng đứng cạnh một bảng trống. Chỉ hai lần giữ cấu trúc người kể cạnh câu hỏi; các lần khác có đối tượng: hai danh sách, người đối đầu, ấn quyền vị, ghế trống hoặc những lời phán khác nhau.
- Đã chạy trang thật trong trình duyệt, phát audio liên tục hơn hai phút, quan sát đồng hồ/khung hình đổi và tua sang phần 7. Trình phát báo audio readyState=4, đang phát, mốc audio +1,5 giây khớp đồng hồ; không có thông báo lỗi tải. Đây là kiểm tra vận hành/sync, **không** phải QC nghe trực tiếp toàn bài.
- Đã tạo ảnh bằng renderer Studio từ project native; phát hiện phụ đề tối trên nền tối và sửa thành chữ tối trên vùng giấy sáng dành riêng. Đã sửa native path reveal và easing để các lớp có chuyển động thực.
- Khi thử phát từ giữa tập, đã phát hiện máy chủ HTTP thường không cho tua audio (seekable chỉ 0–0). Đã thay bằng máy chủ local có byte range, kiểm tra HTTP 206 cho vùng byte thực; thử phát từ 09:58 tiếp tục đến 10:04, audioTime=603,4 giây, vùng tua 0–892,13 giây, không lỗi hiển thị. Ảnh giao diện bàn giao là `review/preview_ui.png`.

## Chủ đích trở lại trong cùng họ bối cảnh

Quy tắc cách nhau 60 giây là mặc định, các chuỗi này có diễn biến liền nhau cần giữ quan hệ. Bằng chứng từng nhịp được liên kết trong `repetition_exceptions.json`; không tăng ngân sách chỉ bằng thay tên PNG.

- Bàn án → cổng thi hành: chuyển từ người bị xét tội sang hệ quả ngoài khung, không lặp bàn án trống.
- Côn Lôn → 32 tuổi → 72 tuổi: một lần định vị ngắn, sau đó cùng góc tu hành để thấy thời gian thay con người. Hai trạng thái tuổi tính chung họ Côn Lôn.
- Đội quân → đường rút: thay điều đang bảo vệ bằng tổn thất cụ thể; cận lính về sau không phải đại cảnh mới.
- Người đợi sẵn → cột lửa: chuyển phục kích sang vòng vây, không dùng cùng địa hình làm nền cho lời không liên quan.
- Báo mộng → giải thích giấc mộng: thay người nói và trạng thái ngủ/thức để cho thấy lời can bị gạt đi.
- Đứng → roi → quỳ: cùng trục không gian, cut sang supplied Y02_B; không tuyên bố đã làm hoạt hình quỳ liên tục.
- Động phủ yên → đối thoại Vân Tiêu → anh rời đi: mở đầu động trống dưới hai giây; các lần còn lại có đối thoại và chia tay, còn trao bảo vật là cận hai tay.
- Nghi lễ → giường bệnh: mối liên hệ giữa tác động ở hình nhân và trạng thái người ở doanh khác; phần nghi lễ có ba ảnh thay theo thứ tự.
- Ván cờ → truy sát → hậu quả: thay cảnh yên bằng việc xâm nhập rồi người chết, các chi tiết pháp bảo ở giữa là lớp vật thể riêng.
- Công việc ở ruộng → ruộng tiếp tục nhận mưa: kết bằng đối tượng phận sự và hệ quả, không giữ lại chân dung để lấp hết câu cuối.
- Hai tờ giấy có bốn nhịp liền trong một phép giải thích: trống → tiêu đề trái → tiêu đề phải → tên/đường nối. Đây là một trình bày tiến triển, không bốn lần quay lại cùng bảng không đổi.

## Phần chưa được xác nhận

Bản edit là nháp cho người dùng duyệt, không ghi PASS thẩm mỹ từ số lần lặp hoặc kiểm tra dữ liệu. Chưa nghe đánh giá toàn bộ master H trong lượt dựng lại này; chưa xem liên tục toàn bộ gần 15 phút cùng âm thanh, chưa có âm nhạc/SFX mới. Gói người supplied có chất minh họa chi tiết hơn reference explainer; không tự nhận đây là character master vector mới đã được duyệt. Chưa có bộ QC cuối cho mọi người/pose trước xuất final; các source/crop hiện được giữ để kiểm tra ở bước đó. Không dùng `allow_draft` để bỏ cổng QC khi xuất final.

Trình xem dùng Canvas; project Studio giữ cùng nguồn/lớp/thời gian nhưng font wrap và một số chuyển động tuần hoàn cần đối chiếu ở bước xuất nháp ngắn sau khi chốt edit. Không tuyên bố hai renderer giống từng pixel. **Không có MP4 toàn tập được tạo trong công việc này.**
