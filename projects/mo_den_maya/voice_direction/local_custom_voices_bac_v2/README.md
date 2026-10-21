# Ba mẫu custom tiếp theo — yêu cầu giọng Bắc

Người dùng yêu cầu thêm giọng Bắc sau bộ local đầu tiên. Các mẫu D/E/F sinh
mới bằng VoxCPM2 local; không dùng preset hay audio tham chiếu. Mô tả yêu cầu
người nói Hà Nội, sáu thanh Bắc (phân biệt hỏi/ngã), cao độ trung bình, giọng
nam trẻ, nhẹ và tinh nghịch. Đây là yêu cầu cho model, chưa phải kết quả được
xác minh bằng nghe.

Ba mẫu dùng cùng `loi_doc_thu.txt`, cùng thiết lập tổng hợp và bản nghe 1,25×.
Chỉ mô tả giọng và seed khác nhau. Không đổi cao độ hậu kỳ. Bản native giữ
trong `originals/`; cấu hình, hash và log đầu vào UTF-8 được lưu để truy vết.
Không ghi đè bộ A/B/C hoặc thay giọng B mặc định.

Tạo lại từ thư mục gốc:

```powershell
projects/angkor_wat_1min/.venv/Scripts/python.exe -X utf8 tools/design_mo_den_northern_more.py
```

Nghe duyệt riêng các mục: đúng vùng Bắc, đủ lời, sáu thanh, độ tự nhiên và
mức tinh nghịch. Kiểm tra codec/peak/mức nghe không thay thế nghe đánh giá.
Chưa dùng mẫu chưa chọn để đọc lại toàn bài.
