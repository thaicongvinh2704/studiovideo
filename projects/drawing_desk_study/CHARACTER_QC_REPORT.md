# Kiểm chứng cổng QC nhân vật — 20/10/2026

**THU HỒI:** người dùng đã loại mẫu study-02 vì chất lượng tạo hình kém, các bộ phận và kích thước không hài hòa. Các mục PASS dưới đây là lịch sử đánh giá nội bộ đã sai, không còn là kết luận hiện tại. Mẫu bị chặn bằng identity/hash, kể cả bản sao giữ receipt PASS cũ. 41 test trước đây chỉ kiểm tra cơ chế phần mềm, không đánh giá được độ đẹp/giống của hình.

Chuẩn bắt buộc: ba ảnh người dùng trong `assets/styles/explainer_reference_v1/`. Mẫu áo xanh cầm sổ của bản 01 đã bị từ chối. Mẫu study-02 là bản sửa có QC nội bộ, chưa được người dùng duyệt thành thiết kế chính thức.

## Đã thực hiện

- Lưu ba ảnh gốc và hash trong project; viết `AGENTS.md` buộc lần làm sau đọc chuẩn và mở ảnh trước khi vẽ người.
- Quy định đầy đủ tại `CHARACTER_STANDARD.md`: tỷ lệ, đầu/tóc/mặt, bàn tay và ngón, điểm nối chi, quần áo, nét, bản nhỏ, bố cục và tính nhất quán.
- Tạo ảnh toàn hình, mặt, hai tay, ảnh nhỏ và bảng đối chiếu ba reference. Đã mở và xem các ảnh thực, không chỉ đọc đường nét.
- Bản sửa đầu tiên bị FAIL do tay có bốn ngón thay vì năm trong tư thế đang vẽ. Giữ hồ sơ lỗi; sửa đường bao và ngón rồi render, xem lại.
- Bản hiện tại có receipt gắn hash nét `69ac5f5433aa35cb4696886d1156c1985336bf433862fbb8708581069d5e2cfb`, hash ảnh chứng cứ và nhận xét riêng cho 12 mục.
- Bàn vẽ chặn xuất SVG/PNG/đưa vào cảnh nếu nhân vật chưa đạt QC. Hai đường xuất video đều kiểm tra QC trước, `allow_draft` không bỏ qua lỗi nhân vật.
- Sửa nét, xóa phần tay, sửa SVG bên ngoài, thiếu/hỏng ảnh chứng cứ hoặc đổi bộ chuẩn đều làm QC không hợp lệ. Ghi review FAIL không khôi phục dấu PASS cũ.
- Lưu thành và ZIP mang theo ảnh QC. Người dẫn mới chèn bằng nút toolbar là hình tĩnh đã QC; mẫu rig cũ không tự được miễn kiểm tra.
- Đã xem mẫu ở cả bố cục sơ đồ và bố cục ảnh thật. Vật thể giữ dữ liệu nét hiện có.

## Kiểm tra chạy thực

`python -m unittest tests.test_character_qc tests.test_drawing tests.test_explainer tests.test_ink -q`

**41 tests đạt.** Có kiểm tra thao tác chuột, undo/redo, bố cục SVG, portable project, cổng QC thiếu/cũ/FAIL, sửa file và chặn bypass, cửa sổ QC yêu cầu mở đủ tab, cùng việc nút Người dẫn chèn đúng hình tĩnh.

Clip kỹ thuật 10 giây đã xuất lại sau khi thay mẫu người, bằng đường xuất thật có QC. Clip không phải video lịch sử hoàn chỉnh và không có lời đọc.

## Phạm vi và giới hạn

QC kỹ thuật xác nhận hồ sơ, phần được khai báo, mốc/tỷ lệ, hash và trạng thái review. Kiểm tra thẩm mỹ vẫn phải do người vẽ/agent nhìn ảnh thực. Không tuyên bố phần mềm tự hiểu mọi lỗi giải phẫu hay xác nhận người dùng thích một mẫu mới.

Người vẽ/agent bắt buộc phân loại lớp người và khai báo phần/mốc. Giao diện chưa có công cụ gán mốc/part bằng chuột; mẫu mới cần hoàn thiện dữ liệu trước khi QC. Không đổi nhãn người thành vật thể để né cổng. EXE đóng gói cũ chưa build lại; dùng `start_studio_drawing.bat` cho bản mã nguồn hiện tại.
