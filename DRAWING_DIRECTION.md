# Bàn vẽ riêng cho Studio — nghiên cứu và bản thử 01

**Bàn vẽ đã được nâng cấp:** xem [DRAWING_DESK_GUIDE.md](DRAWING_DESK_GUIDE.md) để chạy công cụ chỉnh nút, dựng mốc liên kết và xem ba ảnh chuẩn. Bài tập khởi động mới chỉ chứa vật thể; không mở lại người bị loại. Chưa có master nhân vật được duyệt.

**Nghiên cứu tiếp theo ngày 20/10/2026:** xem [DRAWING_TOOL_RESEARCH.md](DRAWING_TOOL_RESEARCH.md) về công cụ riêng có dựng hình liên kết, chỉnh Bézier, mẫu tư thế và API cho agent. Đây là thiết kế đề xuất, chưa triển khai; những giới hạn của bàn vẽ hiện tại vẫn còn.

**Trạng thái mới nhất:** người dùng đã loại cả người cầm sổ bản 01 lẫn study-02. Mọi mô tả study-02 đạt QC bên dưới là lịch sử đánh giá sai đã bị thu hồi. Hiện chưa có master nhân vật đạt yêu cầu; chỉ bộ ba ảnh người dùng là chuẩn phong cách.

**Cập nhật sau phản hồi người dùng:** mẫu người “Nét Mộc 01” ở tài liệu này đã bị từ chối. Chuẩn bắt buộc hiện tại là ba ảnh gốc của người dùng, xem [CHARACTER_STANDARD.md](CHARACTER_STANDARD.md) và [AGENTS.md](AGENTS.md). Thông tin màu/tóc/người cầm sổ bên dưới là lịch sử bản thử, không phải preset được duyệt. Vật thể được giữ nguyên. Project mẫu hiện đã thay bằng study nhân vật 02 có hồ sơ QC nội bộ; người dùng chưa duyệt thiết kế mới này.

Yêu cầu ghi nhận ngày 20/10/2026. Các nguyên tắc dưới đây đến trực tiếp từ người dùng. “Nét Mộc” là tên tạm của bản thử, chưa phải phong cách được người dùng duyệt.

## Điều đã rõ

- Studio tự sở hữu bộ quy tắc tạo hình, thư viện hình vẽ và tài liệu nét vẽ chỉnh sửa được.
- Minh họa đơn giản như ba ảnh tham chiếu: nền trắng, đường viền tối, màu phẳng ít, nhân vật cách điệu, sơ đồ dễ đọc.
- Kết hợp hình vẽ với ảnh chụp thật. Không dùng dịch vụ/mô hình sinh ảnh, không biến ảnh AI thành vector rồi gọi là vẽ.
- Nhân vật là hình tĩnh. Không cần xương, nháy mắt, nhép miệng hoặc chuyển tư thế.
- Chuyển động do đạo diễn gán sau theo câu nói: gạch rơi, mũi tên xuất hiện, đường nước chạy, khoanh hoặc gạch nhấn.
- Nhân vật chỉ có mặt khi giúp kể chuyện; không đặt người chỉ tay vô cớ trong mọi cảnh.
- Tham khảo mức độ đơn giản và ngôn ngữ trình bày. Không sao chép nhân vật, biểu tượng áo hay nét nhận diện của kênh tham chiếu.

## Chuẩn thử để giữ hình đồng bộ

Khung thiết kế 1280 × 720. Mực `#252b2d`; nét chính 3.5 px, nét chi tiết 1.8–2.6 px; đầu và góc nét bo tròn. Đường cong được đặt có chủ đích, không thêm nhiễu ngẫu nhiên ở từng khung hình. Giữ khoảng trống quanh đối tượng; một cảnh phục vụ một câu hỏi hay một quan hệ cần giải thích.

Màu thử: da `#f3cfaa`, xanh ngọc `#40827e`, xanh nhạt `#d9e8e3`, đất nung `#d58b62`, đá `#b9b9b2`. Xanh `#326dc9` cho đường đi/nước; đỏ `#d74d43` cho chỗ cần chú ý. Chưa coi bảng màu hay khuôn mặt thử là quyết định cuối cùng.

Hình dùng ít chi tiết nhưng vẫn có hình khối rõ: silhouette, tỷ lệ đầu–thân, hướng tay, mặt trước/mặt bên vật thể. Đẹp lên nhờ bản vẽ và cách chọn chi tiết; thư viện làm mượt nét chỉ xử lý đường bút, không thay việc thiết kế.

## Kết luận kỹ thuật

Dự án đã dùng PySide6/Qt. Có thể viết bàn vẽ riêng trực tiếp trong ứng dụng với `QPainterPath`, rồi xuất SVG để dùng cùng renderer hiện tại. Không cần chuyển sang Blender, nhúng nguyên một phần mềm vẽ hay thêm dịch vụ bên ngoài cho mức minh họa này.

Nguồn đã kiểm tra:

- [QPainterPath — Qt for Python](https://doc.qt.io/qtforpython-6/PySide6/QtGui/QPainterPath.html): đường thẳng, đường cong Bézier, khép vùng và tô.
- [perfect-freehand-python](https://github.com/bigbluebutton/perfect-freehand-python) và [API](https://bigbluebutton.github.io/perfect-freehand-python/api.html): chuyển quỹ đạo bút có áp lực thành đường bao. Phù hợp nếu sau này cần bút đổi độ dày. **Bản thử hiện tại không phụ thuộc thư viện này**; nét đều và làm mượt midpoint của Qt đủ cho bài toán đang kiểm tra.
- [Rough.js](https://github.com/rough-stuff/rough): tạo hình và gạch bóng có cảm giác phác. Hữu ích cho sơ đồ phụ nhưng không chọn làm nền phong cách nhân vật. Bản thử không dùng Rough.js.

Mã nguồn của bàn vẽ và hình mẫu do dự án tự viết. Qt vẫn là thư viện nền. Không tuyên bố công cụ tự thiết kế được mọi chủ đề: người vẽ/agent vẫn phải chọn bố cục, tạo đường nét và kiểm tra chất lượng trước khi đưa vào phim.

## Bản thử đã triển khai

Nút **Bàn vẽ…** trong thanh Minh họa của Studio chạy từ mã nguồn. Có bút kéo nét, đường gấp/vùng kín tô màu, chữ, tẩy cả nét, di chuyển lớp, đổi thứ tự/ẩn/đổi tên/xóa lớp, undo/redo, mở/lưu `.drawing.json`, xuất SVG và PNG xem trước.

Chạy `start_studio_drawing.bat` để mở Studio từ mã nguồn cùng project mẫu; nút **Bàn vẽ…** ở đầu thanh Minh họa. Chạy `start_drawing_desk.bat` để mở riêng bàn vẽ và xuất tệp. Bản EXE đóng gói cũ chưa được build lại trong lần nghiên cứu này.

“Đưa từng lớp vào cảnh” xuất mỗi lớp thành một SVG riêng; giữ dữ liệu nét vẽ trong đối tượng project để mở lại bằng **Sửa nội dung…**. Thời gian, vị trí, keyframe và lớp cha của đối tượng được giữ khi sửa lại nét. Ảnh thật nhập bằng **Nhập → Ảnh chụp thật…**, vẫn là lớp ảnh riêng trong Studio. Nhân vật phải qua QC, thay nét phải xem ảnh và ghi QC lại.

Lưu project và Lưu thành sao chép các SVG vào gói media. JSON chứa dữ liệu đường nét, không chứa ảnh bitmap được sinh từ mô hình. PNG là bản raster hóa để xem trước hình vector đã vẽ.

Mẫu thử gồm nhân vật tĩnh cầm sổ, bệ gạch, viên gạch rời, đường nước và dấu hỏi. Đây là sơ đồ kiểm tra công cụ, không phải khẳng định cách cấp nước của Babylon hay phục dựng một di tích.

## Giới hạn hiện tại và phần phát triển sau

Đây là bàn vẽ thử nghiệm. Chưa có chỉnh từng điểm Bézier bằng tay nắm, lực bút tablet, tẩy một phần nét, flood fill, thư viện nhân vật nhiều góc nhìn hay hệ thống quản lý phiên bản style. Sửa nét mẫu hiện bằng tẩy/vẽ lại; muốn sửa hình học chính xác có thể chỉnh dữ liệu vector bằng mã.

Tách lớp đã hoạt động; gán chuyển động vẫn dùng timeline/keyframe của Studio. Chưa có nút tự đạo diễn mọi nét vẽ thành chuyển động. Nên duyệt hình tĩnh trước, rồi mới xây bộ chuyển động thường dùng: rơi/nảy, vẽ tuyến, đầu mũi tên bám tuyến, khoanh, gạch nhấn. Khi diễn giải lịch sử cần tách ảnh tư liệu, sơ đồ giải thích và giả thuyết theo kịch bản.

## Tệp kiểm chứng

Thư mục `projects/drawing_desk_study` có `.drawing.json`, SVG, PNG, project chứa các lớp và một cảnh ghép ảnh thật. Các tệp này là bản thử riêng; không thay video Angkor Wat hoặc Babylon cũ.

Ba ảnh tham chiếu của người dùng được dùng để đọc yêu cầu, không cắt ra làm asset phim. Tên tệp nguồn: `codex-clipboard-ddf88de4-86d5-49de-ade1-a5f6e39108ac.png`, `codex-clipboard-608c29e4-8a0f-4813-a0df-2cfb2a82a7ce.png`, `codex-clipboard-24fb2854-2808-4320-843d-00efbc94f7dc.png`.

Kiểm tra ngày 20/10/2026: 28 bài test drawing/explainer/ink đạt, gồm thao tác chuột vẽ nét, undo/redo, ẩn/sắp lớp, SVG giữ bố cục, Lưu thành project có đủ media, sửa lại nét trong cửa sổ Studio vẫn giữ timing/transform/keyframe. Clip kỹ thuật 10 giây đã xuất H.264 1280 × 720, 24 fps và giải mã toàn bộ bằng FFmpeg thành công. Clip không có lời đọc; chỉ minh họa gạch rơi và vẽ tuyến, không phải video lịch sử hoàn chỉnh.
