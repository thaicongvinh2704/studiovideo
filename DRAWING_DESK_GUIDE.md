# Bàn vẽ riêng của Studio — bản có thể sử dụng

Ngày 20/10/2026. Đã triển khai trong mã nguồn và kiểm tra chạy trên máy này. Mở bằng `start_drawing_desk.bat`; mở cùng timeline bằng `start_studio_drawing.bat`. `start_studio.bat` ưu tiên mã nguồn khi có runtime để không mở nhầm EXE cũ.

Đây là công cụ tạo và sửa minh họa vector. Không dùng mô hình sinh ảnh. Chưa có mẫu nhân vật được người dùng duyệt; công cụ không tự biến yêu cầu bất kỳ thành hình người đẹp.

## Các thao tác đã có

| Việc cần làm | Cách dùng |
|---|---|
| Xem ảnh chuẩn | Tab **Chuẩn** giữ ba ảnh gốc. Bấm ảnh để mở bản lớn. Ảnh chuẩn không đưa vào phim |
| Nhìn chi tiết | Cuộn chuột để zoom tại con trỏ; chuột giữa hoặc **Kéo khung nhìn** để pan; F để vừa khung |
| Vẽ thường | **Bút nét**, kéo chuột; nét vector độ rộng cố định |
| Vẽ đậm nhạt | **Bút đậm nhạt**; chỉnh cỡ, Đậm nhạt, Mượt. Chuột dùng áp lực mô phỏng; tablet dùng áp lực thiết bị |
| Vẽ Bézier | Bấm đầu nét, tay nắm 1, tay nắm 2, cuối đoạn; tiếp tục từng nhóm ba điểm; Enter kết thúc, Esc bỏ nét đang phác |
| Chọn nhiều nét | **Chọn / kéo nét**, giữ Shift để thêm/bớt nét khỏi lựa chọn |
| Sửa hình | **Sửa nút Bézier**, chọn nét, kéo điểm hoặc tay nắm. Kéo nút mang theo tay nắm lân cận |
| Thêm/bớt nút | Chọn nút cuối đoạn; tab **Nét** có chia đoạn, xóa nút và chuyển đoạn thẳng sang Bézier |
| Nối mềm hai đoạn cubic | Chọn nút chung giữa hai đoạn C; **Làm mượt nút nối Bézier** điều chỉnh hướng tay nắm tiếp theo |
| Sửa màu và nét | Tab **Nét**: viền, màu tô, bỏ viền/tô, khép đường, áp dụng cỡ/đậm nhạt/mượt cho nét đã chọn |
| Thứ tự che khuất | Đưa nét lên trước/ra sau trong lớp; đưa lớp lên/xuống ở tab Lớp |
| Lớp phác | Chọn **Lớp phác**: hiện mờ trong bàn vẽ, không xuất SVG/PNG cuối hoặc timeline |
| Lớp khóa | Chọn **Khóa nét**: chặn thao tác vẽ/chỉnh nét trên canvas và các panel chỉnh |
| Lưu và phục hồi | Lưu `.drawing.json`; undo/redo; khi đóng cửa sổ thật có cảnh báo lưu thay đổi chưa lưu |
| Tái sử dụng | Lưu lớp vào thư viện, thêm mẫu từ thư viện. Mẫu nháp và trạng thái QC không bị tự nâng thành đạt |

Màu bút/tô tùy chọn bằng hộp màu. Nét brush giữ quỹ đạo và áp lực trong `brush_source`; đổi tham số có thể dựng lại đường bao. Nếu sửa node trực tiếp trên đường bao thì quỹ đạo nguồn được bỏ để tránh hai dữ liệu mâu thuẫn.

## Dựng hình liên kết

Mốc là dữ liệu biên tập, không phải người que đưa lên phim.

1. Chọn lớp. Trong tab **Mốc**, đặt tên mốc rồi bấm **Đặt / kéo mốc trên canvas**.
2. Bấm vị trí để thêm; kéo mốc đã có để chỉnh. Có thể chọn mốc cha và giữ khoảng cách lúc tạo mốc mới.
3. Để kéo cả nhóm mặt/tóc cùng nhau: chọn các nét, chọn mốc trong tab Mốc, bấm **Gắn nhóm nét đã chọn**.
4. Để hai đường thực sự chung điểm nối: chọn nút cuối/đầu của từng đường bằng **Sửa nút**, dùng **Nối nút đang chọn vào mốc** với cùng một mốc. Nút được đưa đúng về vị trí mốc; kéo một nút liên kết sẽ di chuyển các nút cùng gắn mốc.
5. Mốc con đi theo khi kéo mốc cha. Ràng buộc khoảng cách giới hạn điểm con trên vòng tròn quanh cha. Đây là một ràng buộc dựng hình cụ thể, không phải bộ giải tự tạo mọi tư thế cơ thể.

Một nét có thể gắn toàn nét hoặc gắn từng nút; không dùng cả hai kiểu đồng thời. Nét đã gắn mốc cần kéo bằng mốc hoặc nút liên kết; kéo tự do bị chặn để tránh làm lệch quan hệ. Có nút tháo liên kết và xóa mốc.

Phép liên kết không tự sửa giải phẫu, tiếp tuyến giữa mọi đường hay vùng che khuất. Tạo dáng mới vẫn cần nhìn silhouette và sửa đường áo, tay, mặt. Không dùng nó để kéo méo mẫu bị loại rồi tuyên bố mẫu mới đạt.

## Hồ sơ nhân vật

Tab **Nét** cho phép gắn nhãn bộ phận cho các nét được chọn. **Thiết lập hồ sơ nhân vật** lưu nhận diện, toàn thân/bán thân, lấy mốc từ canvas và tính vùng cận cảnh từ nét đã gắn nhãn đầu/hai tay.

Các tên mốc cần dùng được hiển thị trong hộp hồ sơ. Không tự điền phần cơ thể còn thiếu hoặc tự khai phần khuất. Những trường hợp khuất đặc biệt hiện vẫn cần khai báo đúng trong dữ liệu; QC sẽ báo thiếu nếu chưa làm.

Hồ sơ này chỉ chuẩn bị dữ liệu. **QC nhân vật…** vẫn cần xem hình thực, mặt, hai tay và ảnh đối chiếu. Sửa nét làm review cũ hết hiệu lực; mẫu đã bị người dùng loại giữ trạng thái bị loại và bị chặn khi xuất. Nhận diện cũ không đổi tên qua hộp hồ sơ.

## API dành cho agent

Agent và giao diện dùng chung `studio/drawing_edit.py`. CLI không chạy mã tùy ý, chỉ nhận danh sách lệnh JSON:

```json
[
  {"op":"add_guide","layer":0,"name":"joint","point":[200,150]},
  {"op":"move_node","layer":0,"item":0,"command":1,"argument":5,"point":[210,160]}
]
```

`command` là chỉ số lệnh M/L/Q/C/Z trong path; `argument` là vị trí x trong mảng lệnh (1, 3 hoặc 5). `item` và `layer` bắt đầu từ 0. ID mốc được tạo và lưu trong JSON đầu ra; đọc ID đó trước khi dùng lệnh liên kết hoặc kéo mốc.

Lệnh có: `add_path`, `add_guide`, `move_guide`, `bind_items`, `bind_node`, `move_node`, `split_segment`, `smooth_knot`, `curve_segment`, `remove_knot`, `restyle_stroke`.

```powershell
projects\angkor_wat_1min\.venv\Scripts\python.exe -X utf8 tools\drawing_commands.py input.drawing.json --commands edits.json --output output.drawing.json --preview preview.png
```

`--preview` là render nháp để nhìn và sửa, không duyệt QC. `--svg final.svg` kiểm tra QC trước khi ghi thành phẩm. Mỗi lệnh tạo bản sao và kiểm tra hợp lệ; lệnh lỗi không sửa bản đầu vào. Không tạo lớp đã duyệt qua API.

## Kiểm chứng và giới hạn

- `tests/test_drawing_editor.py` kiểm tra tương tác chuột, liên kết điểm, khoảng cách, chia Bézier giữ hình, chỉnh áp lực, khóa lớp, dữ liệu sai, undo/redo, lưu/mở và loại bỏ phác khỏi thành phẩm.
- Các test drawing/QC/explainer/ink cũ vẫn chạy để kiểm tra tích hợp và chặn mẫu bị loại.
- `tools/verify_drawing_workbench.py` tạo ảnh từ cửa sổ Qt thực, SVG, JSON và project timeline có đủ media. Kết quả tại `projects/drawing_workbench/`.
- Tablet được xử lý bằng sự kiện áp lực Qt nhưng chưa thử với bảng vẽ vật lý trên máy này.
- Bản EXE trong `dist` chưa được đóng gói lại. Các launcher ở thư mục dự án chạy mã nguồn mới trên runtime có sẵn.
- Không có bộ sinh nhân vật tự động, bộ giải giải phẫu hoặc thư viện ba tư thế đã duyệt. Phần mềm chạy được không chứng minh hình người đã đạt chất lượng tham chiếu.

## Nguồn

Qt/PySide6 là nền render hiện có. Bút đậm nhạt dùng bản Python `perfect-freehand` 1.2.0 đóng kèm tại `studio/vendor/perfect_freehand`, giữ mã nguồn và giấy phép MIT. Xem `THIRD_PARTY_NOTICES.md`. Không cần tải dịch vụ hoặc mô hình ảnh khi dùng bàn vẽ.
