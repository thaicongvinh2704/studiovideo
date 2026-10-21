# Nghiên cứu công cụ minh họa riêng cho Studio

**Cập nhật triển khai:** phần bàn vẽ, tham chiếu, chỉnh node/Bézier, bút áp lực, mốc cha/con, liên kết nút và nhóm nét, thư viện, hồ sơ nhân vật và API lệnh đã được xây trong mã nguồn. Xem [DRAWING_DESK_GUIDE.md](DRAWING_DESK_GUIDE.md). Chưa có master nhân vật hoặc ba tư thế đạt yêu cầu. Phần bên dưới giữ nguyên đề xuất ban đầu; không hiểu mọi đề xuất là chức năng đã triển khai.

Ngày 20/10/2026. Trạng thái: đề xuất kỹ thuật sau khi đọc mã nguồn, xem trực tiếp cả ba ảnh chuẩn và kiểm tra tài liệu nguồn. Các chức năng mới bên dưới CHƯA được triển khai. Không có nhân vật mẫu mới được duyệt.

## Mục tiêu

Xây công cụ vẽ bên trong Studio để người dùng và agent cùng chỉnh được hình minh họa: nhân vật hoạt họa tĩnh, vật thể, kiến trúc, sơ đồ và chú giải. Hình có nét viền hữu cơ, màu phẳng, bố cục trắng thoáng như ba ảnh chuẩn. Ảnh chụp thật được đưa vào cảnh dưới dạng tài sản riêng.

Không dùng mô hình sinh ảnh, không vector hóa ảnh AI. Agent có thể viết lệnh dựng/chỉnh vector; toàn bộ nét, điểm điều khiển và lịch sử thay đổi phải đọc và sửa được. Phần mềm dựng hình không tự có khả năng thẩm mỹ như họa sĩ.

## Quan sát ba ảnh

- Ảnh 01: dáng toàn thân với đầu lớn, hai chân đỡ thân, một tay chống hông và một tay nắm cán xẻng. Nét ít nhưng thế tay và vùng che khuất có chủ đích.
- Ảnh 02: bán thân; vai, tay áo, cánh tay gập, cổ tay và bàn tay chỉ tạo thành cấu trúc liên tục. Tóc là một khối rõ với nét chi tiết theo hướng.
- Ảnh 03: chi tiết mặt/tóc nhiều hơn; nhân vật vẫn đọc rõ bên ảnh chụp. Cánh tay nằm trước thân nên cần thứ tự che khuất chính xác.
- Ba ảnh không chứng minh chỉ có một bộ tỷ lệ số học duy nhất. Mẫu toàn thân và mẫu bán thân cần quy tắc riêng; không kéo hình cho vừa một khoảng tỷ lệ rồi xem là đạt.
- Mức hoàn thiện phụ thuộc silhouette, vị trí ngũ quan, hình bàn tay và đường nối cơ thể. Nét rung hay hiệu ứng giấy không thay thế được những yếu tố đó.

## Kiểm tra hệ thống hiện có

| Thành phần | Đã có | Khoảng thiếu liên quan |
|---|---|---|
| `studio/drawing.py` | Lưu M/L/Q/C/Z, tô vùng, render Qt, xuất SVG | Nét là các item độc lập; chưa có quan hệ ràng buộc giữa các điểm |
| `stroke_item` | Làm mượt midpoint, độ rộng cố định | Chưa lưu lực bút, chưa chỉnh độ dày theo dọc nét |
| `DrawingCanvas` | Vẽ, vùng kín, tẩy cả nét, di chuyển cả lớp | Chưa chọn/sửa node và tay nắm, chưa zoom/pan chuyên dụng, chưa tẩy đoạn |
| `studio/character_art.py` | Các đường nhân vật và mốc QC viết sẵn | Mốc không điều khiển đường nét; chưa có mô hình dựng dáng chung |
| QC hiện tại | Kiểm tra dữ liệu, lưu bằng chứng, thu hồi mẫu bị loại | Không tự nhận biết vẻ hài hòa; đã từng đánh giá thị giác sai |
| Studio video | Nhập ảnh, lớp SVG và chuyển động theo timeline | Có thể giữ làm đầu ra; chưa cần viết lại để giải quyết nét vẽ |

Nguyên nhân rời rạc có cơ sở từ mã nguồn: đường vai, tay, cổ tay, mặt và thân được tác giả đặt riêng; khai báo thêm landmark không tạo ra quan hệ hình học. Chất lượng kém còn nằm ở quyết định tạo hình và cách đánh giá trước đây, không thể quy hết cho renderer.

## Kiến trúc đề xuất

### 1. Bàn tham chiếu và phác tổng thể

Giữ ba ảnh chuẩn cạnh canvas; ảnh tham chiếu không xuất vào video. Có zoom, pan, lật ngang bản xem, xem cỡ thực trong cảnh và lớp phác giảm opacity. Lật bản xem không tự sửa dữ liệu gốc.

Trước khi đi nét nhân vật cần phác nguyên dáng và silhouette. Có hướng đầu, đường mắt, vai, lồng ngực, chậu, khuỷu, cổ tay, gối, cổ chân. Các đường hướng dẫn chỉ là công cụ tác giả, không phải bộ xương hoạt hình và không xuất ra phim.

### 2. Dựng hình có quan hệ

Các vùng cơ thể cùng dùng một cấu trúc hướng dẫn có hệ tọa độ nhất quán. Điểm của đường nét có thể gắn vào mốc hoặc khung cục bộ; thay vị trí đầu có thể mang theo mắt, tai, mày, mũi, miệng đã gắn, thay vì di chuyển từng item độc lập.

Quan hệ cần hỗ trợ trước:

- Điểm nối trùng nhau, tiếp tuyến cùng hướng tại đoạn nối cần mềm.
- Giữ chiều dài tương đối của cánh tay/cẳng tay khi chỉnh dáng phác.
- Mặt dùng đường hướng dẫn chung; đối xứng chỉ là trợ giúp, có thể tắt để thể hiện góc nhìn.
- Lòng bàn tay có hướng và bề rộng; các ngón gắn theo cấu trúc bàn tay, không xếp năm nét tùy ý.
- Quần áo, da, tóc và tay trước/sau có thứ tự che khuất rõ.

Ràng buộc chỉ giữ những quan hệ đã thiết kế. Nó không tự quyết định bàn tay đẹp hay chuyển đúng từ mọi góc nhìn. Đổi dáng lớn phải sửa silhouette, nếp áo và bàn tay; không kéo méo toàn bộ nét cũ rồi coi là hoàn thiện.

Không hợp nhất toàn bộ nhân vật thành một path duy nhất: cần giữ đường cổ áo, tay áo và vùng chồng lớp. Phép hợp/trừ vùng chỉ dùng tại chỗ phù hợp; ranh giới nào hiện, ranh giới nào khuất do bản vẽ xác định.

### 3. Đi nét và sửa nét

- Chọn node, kéo tay nắm Bézier; thêm/xóa điểm, nối/tách nét.
- Bút có ổn định quỹ đạo và độ dày tùy chỉnh; lưu điểm đầu vào để sửa lại.
- Giữ đường tâm riêng với đường bao nét có độ dày. Đường bao dùng để render; đường tâm phục vụ chỉnh sửa và hiệu ứng vẽ nét về sau.
- Có nét viền, nét chi tiết, mảng tóc/da/áo; tô và viền có thể chỉnh độc lập.
- Hạn chế làm mượt quá tay ở ngón tay, góc môi, khuỷu. Không thêm rung ngẫu nhiên để giả nét người.
- Bản đầu dùng vùng tô khép kín có kiểm soát. Flood fill và tẩy đoạn có thể bổ sung sau; không cần chúng để chứng minh chất lượng mẫu đầu tiên.

### 4. Mẫu nhân vật của Studio

Chỉ sau khi có bản vẽ mới đạt chất lượng mới lưu thành mẫu gốc. Mẫu gồm đầu/mặt/tóc, tỷ lệ thân, ngôn ngữ nét, bảng màu và các tư thế được vẽ hoàn thiện.

Tư thế ưu tiên để kiểm chứng: đứng toàn thân; bán thân chỉ tay; cầm một đạo cụ. Mỗi tư thế phải được thiết kế như một tổng thể. Không dùng thư viện tay/chân bất kỳ ghép vào một người.

Biểu cảm và màu áo có thể là biến thể trong giới hạn đã kiểm tra. Tư thế/góc nhìn ngoài phạm vi phải thành bản nháp mới, không tự xuất thành asset hoàn chỉnh. Mẫu study-01 và study-02 vẫn bị loại.

### 5. Hai cách điều khiển cùng một công cụ

Người dùng chỉnh qua canvas. Agent dùng API lệnh có thể kiểm tra được, chẳng hạn `add_guide`, `move_anchor`, `edit_curve`, `set_occlusion`, `render_review`. Đây là tên API đề xuất, chưa tồn tại.

Cả hai đi qua cùng validation, undo/redo và cơ chế vô hiệu hóa QC khi đổi nét. Sau mỗi nhóm sửa hình đáng kể, agent render lại và xem ảnh thực. Không viết một khối tọa độ lớn rồi chỉ đọc log để đánh giá.

Không gán việc người dùng phải tự vẽ mọi thứ. Agent vẫn có thể thực hiện công việc tạo nét và sửa hình; khả năng đạt chất lượng của quy trình này phải được chứng minh bằng bản thử, không suy ra từ việc API hoạt động.

### 6. Đưa vào video

Người là ảnh vẽ tĩnh. Đạo cụ, mũi tên, đường nước, viên gạch và chú giải là các đối tượng có ID riêng; timeline điều khiển chúng sau. Ảnh thật lưu nguồn riêng. Hình vector xuất SVG; PNG chỉ là bản render từ nét để xem/QC.

## Thư viện đã nghiên cứu và lựa chọn

| Nguồn | Tác dụng đã được tài liệu xác nhận | Quyết định |
|---|---|---|
| [Qt QPainterPath](https://doc.qt.io/qt-6/qpainterpath.html) | Bézier, vùng tô, giao/hợp/trừ đường | Giữ nền Qt hiện có; tự viết editor và quan hệ dựng hình |
| [Qt QTabletEvent](https://doc.qt.io/qt-6/qtabletevent.html) | Đọc vị trí, áp lực, độ nghiêng từ tablet được driver hỗ trợ | Bổ sung đường nhập lực bút; chưa kiểm thử thiết bị thật |
| [perfect-freehand-python](https://github.com/bigbluebutton/perfect-freehand-python) | Chuyển quỹ đạo bút thành đường bao có độ dày; Python port, mã nguồn MIT | Ứng viên cho bộ xử lý nét, không phải bộ tạo nhân vật |
| [perfect-freehand gốc](https://github.com/steveruizok/perfect-freehand) | Điều chỉnh smoothing, streamline, thinning, taper và áp lực | Tham chiếu thuật toán; chọn tham số bằng bản nét thử |
| [Paper.js](https://github.com/paperjs/paper.js), [Path API](https://paperjs.org/reference/path/) | Chỉnh đường vector, làm mượt và thao tác hình học trong JavaScript | Phương án nếu chuyển canvas sang web; chưa có lý do đổi nền native hiện tại |

Qt ghi rõ phép hợp/simplify có thể làm phẳng Bézier thành đoạn thẳng. Vì vậy không áp dụng destructive boolean lên toàn bộ bản gốc; giữ source và kiểm tra đường xuất. Những thư viện này không có sẵn phong cách ba ảnh hay khả năng tự sửa giải phẫu.

Giữ ghi nhận giấy phép và nguồn cho dependency được chọn; không gọi mã thư viện là do Studio tự viết. Trong lượt nghiên cứu này chưa cài mới hoặc tích hợp các dependency.

## Dữ liệu cần bổ sung

Đề xuất phiên bản tài liệu mới sau khi thử nghiệm, chưa sửa schema đang chạy:

- `references`: nguồn và crop của bảng tham chiếu, không render vào thành phẩm.
- `guides`: mốc dựng hình, hướng và khung cục bộ.
- `constraints`: các quan hệ rõ loại, điểm tác động, trạng thái và sai số.
- `strokes`: điểm nguồn/áp lực hoặc đường Bézier; đường bao render được suy ra.
- `regions`: mảng tô và quan hệ trước/sau.
- `models`: nhận diện mẫu, phiên bản và phạm vi tư thế đã kiểm tra.

Nét nghệ thuật vẫn sửa tự do được; phần gắn ràng buộc phải cho phép tháo gắn có chủ đích. Khi solver không giải được, hiển thị xung đột và giữ bản hợp lệ trước đó. Bản vẽ v1 phải tiếp tục mở được; không tự gắn ràng buộc hay tự duyệt lại các nhân vật cũ.

## Thứ tự triển khai và điều kiện dừng

1. **Công cụ chỉnh hình:** bảng tham chiếu, zoom/pan, phác/ink, chỉnh node và tay nắm. Kiểm chứng sửa một đường cụ thể, undo và mở lại giữ nguyên hình.
2. **Dựng hình liên kết:** hướng đầu/thân và các điểm nối; hiển thị ràng buộc. Kiểm chứng thay đầu không làm ngũ quan trôi, sửa khuỷu không tách cổ tay trong phạm vi hỗ trợ. Đây chỉ là kiểm tra cơ học.
3. **Một bản vẽ nhân vật mới hoàn chỉnh:** dựng silhouette trước, rồi mặt/tóc, tay và áo. Xem cạnh ảnh chuẩn và ở cỡ lên hình. Nếu vẫn xấu thì sửa phương pháp tạo hình; dừng mở rộng thư viện và dừng làm video mẫu.
4. **Ba tư thế nhất quán:** chỉ mở rộng sau khi hình đầu đạt mức hoàn thiện. Giữ phân biệt QC nội bộ và người dùng duyệt mẫu.
5. **Một cảnh hỗn hợp:** nhân vật tĩnh + ảnh thật + vật thể/đường chú giải có chuyển động độc lập, dùng pipeline video hiện có.

Đích của nghiên cứu là một công cụ cho phép dựng, quan sát và sửa hình chính xác hơn. Thành công mỹ thuật phải thể hiện ở bản vẽ mới. Chưa có bằng chứng để hứa “nhập bất cứ yêu cầu nào cũng tự vẽ đẹp như họa sĩ”.
