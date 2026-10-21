# Một ngày cùng người Việt cổ · Bản dựng 5 phút

Kịch bản: file SRT do người dùng cung cấp, sao lưu nguyên bản trong `source/kich_ban_goc.srt`. Video giữ 64 đoạn, nguyên văn và nguyên mốc thời gian; 32 cảnh phủ đúng 00:00–05:00. Giọng đọc được tạo bằng model tiếng Việt Piper CPU có sẵn trong Studio, sau đó căn từng đoạn vào khoảng SRT; không dùng voice có sẵn của một người dẫn trên YouTube.

Mở `Mo_du_an_trong_Studio.bat` để xem/chỉnh dự án. `project.json` và thư mục `assets` cần đi cùng nhau. `phu_de.srt` là phụ đề rời. Video được xuất bằng `dist/StickmanAnimationStudio/StickmanAnimationStudio.exe`, 1080p/30 FPS, H.264/AAC. Lệnh và mã kiểm tra nằm trong `source`; nhật ký thực chạy trong `review`. Không sửa mã lõi Studio để dựng tác phẩm này.

## Hình và âm thanh

- Người dẫn áo đen dùng nhân vật đã được đưa vào Studio theo ảnh người dùng.
- 44 SVG mới trong `art` được vẽ bằng mã cho bộ phim: nhà sàn, người lao động, gia đình, ruộng, thuyền, cá, bếp, khuôn, mũi tên, sơ đồ thành… Các cảnh này là minh họa diễn giải, không phải ảnh khảo cổ hoặc bản phục dựng được chứng nhận. Sơ đồ sông/vòng thành không theo tỷ lệ. Trang phục, từng căn nhà và sinh hoạt gia đình là cách hình dung của bộ phim.
- Ảnh trống Ngọc Lũ: **VuThiAnh**, [Ngoc Lu.jpg — Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Ngoc_Lu.jpg), tác giả công bố public domain. Tập tin ảnh gốc giữ nguyên; phim đặt ảnh vào bố cục.
- Hình vẽ mặt trống: **Ebaychatter0**, [Trong Dong Ngoc Lu.svg — Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Trong_Dong_Ngoc_Lu.svg), [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/). Đây là hình vẽ dựa trên tài liệu, không phải ảnh mặt hiện vật. Tệp vector gốc giữ nguyên, tên và giấy phép được ghi trên cảnh dùng hình và cuối phim; phim đặt hình theo kích thước/góc khung hình. Giữ ghi công và giấy phép khi tái sử dụng tệp này hoặc bản sửa đổi của nó.
- Những hình chung như lịch, điện thoại, bóng đèn dùng thư viện SVG hiện có của Studio.
- Nền nhạc nhẹ, tiếng sông/chim, bếp và điểm nhấn kim loại được tổng hợp mới bằng `source/make_sound.py`; không dùng sample tải từ bên thứ ba và không coi là bản phục dựng âm nhạc cổ đại. Studio tự hạ nhạc dưới lời đọc.

## Tư liệu đối chiếu khi dựng

- [Bảo tàng Lịch sử quốc gia — Trống đồng Ngọc Lũ](https://baotanglichsu.vn/VI/Articles/1002/28053/trong-djong-ngoc-lu.html): hình dáng, đề tài sinh hoạt và 14 tia ở trung tâm.
- [Bảo tàng Lịch sử quốc gia — Lưỡi hái](https://baotanglichsu.vn/vi/Articles/1002/28063/luoi-hai.html): công cụ nông nghiệp Đông Sơn.
- [Khu di tích Cổ Loa — Di tích Cầu Vực](https://thanhcoloa.vn/di-tich-cau-vuc): phát hiện mũi tên năm 1959.
- [Khu di tích Cổ Loa — Sưu tập khuôn đúc](https://thanhcoloa.vn/suu-tap-khuon-duc-co-loa): khuôn, dấu tích lò đúc và các đợt khai quật.

Những nguồn này dùng để đối chiếu hình và phân biệt truyền thuyết/dấu tích. Phim đọc kịch bản người dùng, không bổ sung lời khẳng định mới về mọi chi tiết khảo cổ. Kiểm tra codec, số frame và đồng bộ âm thanh không thay thế nhận xét của người xem về chất lượng kể chuyện, giọng đọc và chuyển động.
