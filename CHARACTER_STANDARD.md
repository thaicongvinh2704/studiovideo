# Chuẩn nhân vật bắt buộc — reference-v1

**Kết luận mới nhất của người dùng: study-02 cũng bị loại.** Mẫu có bộ phận rời rạc, tỷ lệ/kích thước và ngũ quan thiếu hài hòa. Nhãn PASS nội bộ trước đó là đánh giá sai và đã bị thu hồi; hiện chưa có master nhân vật đạt yêu cầu. Hồ sơ kỹ thuật và số lượng test không chứng minh chất lượng tạo hình. Không tái sử dụng study-02 hoặc chỉ đổi vài tọa độ rồi coi là mẫu mới. Cần dựng cấu trúc tổng thể, silhouette và bảng tỷ lệ thống nhất trước khi đi nét/chi tiết.

Ngày 20/10/2026. Ba ảnh người dùng gửi là chuẩn phong cách. Nhân vật “Nét Mộc” áo xanh cầm sổ ở bản thử 01 đã bị người dùng từ chối. Không dùng mẫu đó làm chuẩn hoặc suy diễn rằng đổi bảng màu là sửa được hình người.

## Chuẩn nhìn trực tiếp

Đọc manifest tại `assets/styles/explainer_reference_v1/manifest.json`, mở cả ba ảnh gốc trong thư mục đó. Ảnh được lưu trong project cùng hash để không phụ thuộc thư mục Temp hoặc trí nhớ của agent. Chúng là tài liệu đối chiếu, không phải asset được cắt ra đưa vào phim.

- Ảnh 01: toàn thân, quần áo và giày hoàn chỉnh; tay chống hông và tay cầm xẻng đều có bàn tay, tỷ lệ đầu lớn được kiểm soát; đồ vật và người cùng ngôn ngữ nét.
- Ảnh 02: vai tròn tự nhiên, cổ áo rõ; khuỷu tay gập có cấu trúc, cổ tay nối bàn tay, ngón trỏ và ngón gập đọc được; tóc đen có hướng chải, mặt có đủ mắt/mày/mũi/miệng/tai.
- Ảnh 03: cùng độ hoàn thiện ở cỡ lớn, tóc có các lọn và mảng bên thái dương; bàn tay được thiết kế thành hình chứ không là đầu cánh tay tròn; hình vẽ đặt cạnh ảnh thật vẫn đồng bộ.

Đây là người hoạt họa cách điệu, không yêu cầu giải phẫu ảnh chụp. Giữ ngôn ngữ của ba ảnh: nền trắng, mực tối gần đen, nét bo hơi hữu cơ, da ấm hoặc sáng, trang phục đơn giản, màu phẳng. Không tự chuyển sang đầu dài, tóc dạng đám mây, tay ống tròn, thân hình que hoặc tạo hình hình học tối giản. Không thêm logo của kênh khác.

## Điều kiện hoàn thiện

| Hạng mục | Điều kiện đạt | Lỗi phải sửa |
|---|---|---|
| Tổng thể | Đầu, cổ, vai, thân, tay nối rõ; dáng đọc được ở cỡ sử dụng | Cổ dài/thắt bất thường, vai nhọn, khớp gãy, tay dính thân |
| Khuôn mặt | Hai mắt và mày nhất quán, mũi và miệng rõ, hàm–tai–tóc có cấu trúc | Mặt trống, mắt lệch vô cớ, miệng trôi, tóc là khối tùy tiện |
| Bàn tay trái và phải | Có lòng bàn tay, ngón cái và các ngón được thể hiện theo tư thế; chỉ tay/cầm nắm rõ | Tay cụt, ngón dính, thừa ngón, ngón chỉ xuất phát sai chỗ, bàn tay bị đạo cụ che lỗi |
| Chi và trọng lượng | Vai–cánh tay–khuỷu–cẳng tay–cổ tay hợp lý; chân/giày chịu trọng lượng | Tay xúc xích, không có cổ tay, hai chân nhập một ống, giày chưa hoàn thiện |
| Trang phục | Cổ áo, tay áo, gấu áo, cạp/quần và giày có kết thúc rõ | Mảng da rò qua áo, nét áo cắt tay, đồ vật xuyên người |
| Nét và màu | Nét chính nhất quán, đường cong có chủ đích, ít màu như tham chiếu | Nét rung ngẫu nhiên, đúp viền, hở vùng tô, thêm texture che hình kém |
| Nhất quán | Giữ cùng nhận diện và tỷ lệ khi tái sử dụng; biểu cảm có mục đích | Mỗi cảnh đổi đầu/tóc/tuổi; mô hình cũ tự quay lại |
| Đặt trong cảnh | Khoảng trống và kích cỡ hợp lý, không cắt tay/ngón ngoài ý muốn | Crop che lỗi, chỉ tay vào vùng không có thông tin, người chồng chữ |

Tỷ lệ QC kỹ thuật khởi điểm được suy ra gần đúng từ ảnh, **không phải số đo cơ thể người thật**: toàn thân khoảng 2.6–3.5 chiều cao đầu tính cả tóc; rộng vai khoảng 1.15–1.7 rộng đầu; rộng đầu/cao đầu khoảng 0.72–1.05. Bản vẽ bán thân dùng cùng đầu/vài, khai báo crop có chủ đích; không ép vào tiêu chuẩn toàn thân. Nếu cần ngoại lệ cho vai quay, phối cảnh, tuổi hay nhân vật khác, ghi lý do cụ thể và vẫn kiểm tra trực quan. Không kéo hình cho lọt tỷ lệ rồi coi là đẹp.

## Quy trình bắt buộc mỗi nhân vật / tư thế mới

1. Đọc và mở lại reference. Chọn mẫu nhân vật đã QC hoặc vẽ bản mới theo cùng ngôn ngữ. Không dùng AI sinh ảnh.
2. Tách nhân vật khỏi vật thể; khai báo `role=character`, góc nhìn, các phần cơ thể và mốc khớp. Phần khuất/crop phải có nguyên nhân thực và vật che hoặc mép khung rõ. Tay đang nhìn thấy không được khai là khuất.
3. Chạy kiểm tra thiếu phần, mốc/tỷ lệ, đường nét hữu hạn và các vùng review. Tạo ảnh toàn thân, cận mặt, tay trái, tay phải, ảnh nhỏ tương đương cỡ lên hình và bảng đối chiếu reference.
4. **Mở ảnh thực vừa render bằng công cụ xem ảnh.** Xem toàn hình, mặt và từng tay ở 100–200%, rồi xem bản nhỏ và cảnh thực. Không chỉ đọc SVG/JSON hoặc log test.
5. Chấm từng mục trong rubric bằng nhận xét cụ thể. Bất kỳ lỗi nghiêm trọng nào = FAIL; sửa hình rồi làm lại. Chỉ ghi `passed` sau khi đã xem và sửa.
6. Lưu receipt có hash đường nét, hash ảnh đã xem, phiên bản reference, reviewer và nhận xét. Đây là QC nội bộ, không gán cho người dùng đã duyệt thiết kế mới.
7. Đưa vào cảnh và kiểm tra crop/che khuất/kích thước. Giữ người tĩnh; chuyển động của vật, mũi tên và nước là bước đạo diễn riêng.

Lưu bản nháp luôn được phép. Nhân vật thiếu QC, FAIL, đổi nét sau QC hoặc bị sửa SVG bên ngoài sẽ bị chặn khi đưa lớp vào cảnh / xuất video cuối. Chỉ xem nháp để sửa không phải bàn giao. Các project cũ có nhân vật chưa có hồ sơ cần QC trước khi xuất lại theo chuẩn này.

## Những điều phần mềm không tự biết

Máy kiểm tra được dữ liệu, phần đã khai báo, mốc tương đối, hash và tình trạng review. Nó không thể tự xác nhận ngón tay “đẹp”, biểu cảm tự nhiên hoặc giống phong cách bằng vài con số. Trách nhiệm của agent/người vẽ là nhìn ảnh và sửa; không tự động đóng dấu PASS cho đủ quy trình.

Phân loại người vẫn là bước bắt buộc của người vẽ/agent. Cổng kiểm tra không tự nhận diện được một hình người bị cố tình gắn nhãn “vật thể”; quy định `AGENTS.md` cấm bỏ nhãn hoặc đổi nhãn để né QC. Ảnh chụp thật không phải hình người vector và giữ nguồn riêng.

## Cách thực hiện trong bản mã nguồn

Bàn vẽ hiện đã có tab **Mốc** để đặt/kéo mốc và tab **Nét** để gắn bộ phận, mở **Thiết lập hồ sơ nhân vật**, tính vùng cận mặt/hai tay từ các nét. Xem `DRAWING_DESK_GUIDE.md`. Các chỉ dẫn bên dưới về việc chưa có giao diện gán mốc/part là mô tả của bản cũ; không còn áp dụng. Hồ sơ vẫn không tự duyệt QC.

Chạy `start_studio_drawing.bat`. Trong **Bàn vẽ…**, phân loại lớp **Nhân vật → QC nhân vật…**. Cửa sổ có chín tab: toàn hình, cỡ nhỏ, mặt, hai tay, ba ảnh chuẩn và bảng đối chiếu; bắt buộc mở đủ và ghi nhận xét từng mục. Hình mới phải có phần cơ thể và mốc QC do người vẽ/agent khai báo trong dữ liệu bản vẽ; giao diện hiện chưa có công cụ gán từng mốc/part bằng chuột. Nếu thiếu mốc, giữ nháp và hoàn thiện dữ liệu, không tự cho qua.

Agent có thể dùng `tools/character_qc.py <drawing.json>` để tạo bộ ảnh **pending**; mở ảnh thực rồi viết một tệp review có `reviewer` và nhận xét từng mục. Dùng `--review <review.json> --output <drawing.json>` để ghi QC. CLI không có chế độ auto-pass. Nét sửa, thay reference hoặc mất/sửa ảnh chứng cứ làm QC không hợp lệ. Ghi một mục FAIL làm trạng thái failed và không khôi phục dấu PASS cũ.

Tệp mẫu mới: `assets/characters/reference_person_v2.drawing.json`. Kết quả review nằm trong bản vẽ, ảnh chứng cứ đi theo project khi Lưu thành/đóng ZIP. Bản đầu của lần sửa có lỗi thiếu ngón đã bị loại, lưu tại `qc/characters/e38e26b99d8cade06bc8/review_failed.json`; không dùng bản đó để lên cảnh.

## Nguồn nghiên cứu

Nguồn tạo hình quyết định là ba ảnh người dùng, không phải một preset trên mạng. Cách giữ bộ reference ngay trong hồ sơ cũng phù hợp với [Krita Reference Images Tool](https://docs.krita.org/en/reference_manual/tools/reference_images_tool.html), cho phép lưu một bộ reference và giữ ảnh quan trọng trong tài liệu. Kiểm tra hình học dùng [Qt QPainterPath](https://doc.qt.io/qtforpython-6/PySide6/QtGui/QPainterPath.html); các kiểm tra này chỉ là một phần QC, không thay thẩm định trực quan.
