# Mẫu mỹ thuật vector — Vườn trên các tầng nền

Ba mẫu được vẽ nguyên bản bằng mã SVG, dùng cùng bố cục và hình học để so sánh cách hoàn thiện nét. Không dùng công cụ sinh ảnh AI, ảnh tham chiếu AI, ảnh raster nhúng, hoặc tự động trace một ảnh có sẵn. Đây là một khu vườn tưởng tượng phục vụ so sánh mỹ thuật, không phải phục dựng khảo cổ.

- `images/01_clean.svg`: đường cong Bézier và màu phẳng, nét viền sạch.
- `images/02_ink.svg`: cùng hình học, dùng thư viện perfect-freehand-python thật để chuyển điểm lấy mẫu thành đường bao nét bút biến thiên độ dày.
- `images/03_hatch.svg`: cùng hình học, dùng bộ sinh Rough.js thật để tạo nét phác và gạch bóng ở mặt khuất.

Các PNG cùng tên được Qt QSvgRenderer xuất trực tiếp từ SVG ở kích thước 1600 × 900, để xem trước trong chat. Không phải bộ hình bối cảnh PNG được tạo bằng mô hình AI. Các file `_detail.png` là vùng chi tiết được render lại từ vector.

Mỗi file có các nhóm được đặt tên cho thân kiến trúc, mái, nền, cây, dây leo, nước và chi tiết. Đây là nguồn để tiếp tục tách thành các lớp animation; chưa phải một project Studio đã được rig hoặc một clip đã dựng xong. Không coi việc người dùng xem mẫu là đã duyệt mỹ thuật.

Nguồn thư viện:

- https://github.com/bigbluebutton/perfect-freehand-python — perfect-freehand 1.2.0, MIT.
- https://github.com/mathandy/svgpathtools — svgpathtools 1.8.0, MIT; xử lý và lấy mẫu đường Bézier.
- https://github.com/rough-stuff/rough — Rough.js 4.6.6, MIT; bản phát hành npm và checksum lưu tại `.deps/roughjs/provenance.json`.
- svgwrite 1.4.3 là phụ thuộc của svgpathtools.

Các dependency thử nghiệm nằm trong `.deps` riêng của thư mục mẫu. Không sửa requirements hoặc bộ renderer của Studio. `source/draw_samples.py` chứa toàn bộ hình học, phối màu và các bước xuất ảnh; `source/rough_paths.cjs` gọi Rough.js. `manifest.json` ghi hash SVG và thư viện thực dùng cho từng mẫu.
