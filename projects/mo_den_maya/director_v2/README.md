# Mỏ Đen · Maya · bản đạo diễn V2

**Phản hồi người dùng 21/10/2026: bản này chưa đạt yêu cầu đạo diễn do lặp
nhiều cảnh nền trống.** Không dùng làm mẫu đã được duyệt. Quy định mới ở
`QUY_DINH_DAO_DIEN_HINH_ANH.md` tại gốc repository; thống kê ở
`repetition_audit.json`. Chưa dựng lại MP4 sau phản hồi này.

Bản dựng theo video tham chiếu người dùng cung cấp `kcWEaXRh2hA.mkv`:
luân phiên bối cảnh minh họa, mascot, đạo cụ, sơ đồ và ảnh tư liệu theo lời kể.
Không lấy hình hoặc âm thanh của video tham chiếu làm tài sản cho phim Maya.

## Tệp bàn giao

- `Mo_Den_Maya_Dao_Dien_V2_1080p.mp4`: video đầy đủ, 1920×1080, 24 FPS;
  210 nhịp hình nội dung và ba trang ghi nguồn. Tổng 852,208 giây.
- `Maya_mo_dau_1080p.mp4`: đoạn mở đầu 65,75 giây.
- `project.json`: project chỉnh sửa được trong Studio. Đường dẫn tài sản tương
  đối trong repository; giữ cả repository nếu chép sang máy khác.
- `Maya_H_phu_de_cum_y.srt`: phụ đề chia câu/cụm ngắn theo các đơn vị audio đã có.
- `CREDIT_VIDEO.txt`, `used_sources.json`: tác giả, nguồn, URL giấy phép và mô tả
  chỉnh sửa của những tư liệu thực sự dùng trong phim.
- `shot_list.json`: điểm cắt và quyết định hình ảnh theo từng đoạn lời đọc.
- `import_audit.json`: 198 PNG nhập từ hai ZIP, giữ byte gốc, hash và kích thước.
- `build_report.json`, `delivery_verification.json`, `review/`: kết quả kiểm tra.
  Kiểm tra xuất hoàn tất được ghi sau khi MP4 thực sự xuất và giải mã thành công.

## Cách dựng

Tái sử dụng các chuỗi bối cảnh 151–180 để thể hiện thay đổi của đô thị, hồ nước,
ruộng ngô, kho lương, nhà ở, chợ và cung điện. Xen cảnh toàn, cận trong cùng ảnh,
góc nhìn sơ đồ và khung tư liệu; không suy ra góc khuất 3D từ PNG phẳng.

Các lớp độc lập tạo chuyển động: nước chạy qua kênh, nước thấm xuống nền,
vật liệu di chuyển theo sơ đồ khoảng cách, sắc tố theo dòng chảy, kiện hàng
di chuyển và gặp chướng ngại, túi đồ rời nhà, mốc năm và nhãn lần lượt hiện.
Nhịp hình nội dung trung bình khoảng 3,96 giây; dài nhất khoảng 7,79 giây.

Mỏ Đen giữ nguyên PNG và biểu cảm từ manifest. Nhân vật là lớp `role=character`,
không được gắn nhãn vật thể để bỏ qua QC. Luồng xuất kiểm tra đúng hash tài sản,
alpha, tỷ lệ và biên khung hình; kiểm tra cơ chế không thay cho nhận xét mỹ thuật.
Các PNG nhân vật là hình tĩnh; bản dựng không tạo lip sync hoặc rig cơ thể mới.

Giữ nguyên WAV lời kể H đã chọn, giọng Bắc, 1,25× đã áp dụng ở khâu tạo lời.
Không đổi speaker, không tạo lại lời và không tăng tốc thêm. Thời gian phụ đề
được ước lượng theo câu/cụm trong từng đơn vị tổng hợp, chưa căn từng từ bằng
forced alignment. Bản dựng này không tự chứng nhận lại phát âm toàn bài.

Ảnh thật và figure giữ nguồn riêng. Figure ô nhiễm và Itzan có cửa sổ cận chi
tiết bên cạnh figure toàn vẹn. Sơ đồ/minh họa không được trình bày như dữ liệu
đo, bản đồ tuyến vận chuyển thật hay phục dựng chính xác một di tích.

## Mở / xuất lại

Từ thư mục mã nguồn, dùng Python của `.venv`:

```powershell
& .venv/Scripts/python.exe main.py projects/mo_den_maya/director_v2/project.json
& .venv/Scripts/python.exe -X utf8 tools/direct_maya_v2.py render
& .venv/Scripts/python.exe -X utf8 tools/verify_maya_v2.py
```

`tools/maya_edit_plan.py` chứa các quyết định đạo diễn theo 169 đơn vị lời đọc.
`tools/direct_maya_v2.py build` dựng lại JSON và ảnh kiểm tra, không tạo voice.
Thư mục MP4 từng cảnh được giữ để tiếp tục render khi gián đoạn.

Hai bộ ảnh gốc đã được nhập tại `assets/reusable/mo_den/generic_150/` và
`assets/reusable/mo_den/maya_48/`. ZIP người dùng cung cấp vẫn được giữ ở
Downloads. Các file mới trong lần dựng này chưa được commit/push lên GitHub.
