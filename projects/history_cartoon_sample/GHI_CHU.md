# Clip thử hoạt hình lịch sử · 32 giây

Đây là clip thử hướng kể chuyện hoạt hình lịch sử do người dùng chọn sau khi xem tham khảo OverSimplified. Nhân vật, đạo cụ và nền cảnh được làm riêng cho clip; không lấy hình, nhân vật, đoạn phim hoặc giọng đọc từ kênh tham khảo.

Video: `Thu_phong_cach_hoat_hinh_lich_su_1080p.mp4`. Dự án chỉnh được: `project.json` đi cùng thư mục `assets`, hoặc gói `Du_an_clip_thu.zip`. Mở project bằng Studio EXE. Sáu cảnh dùng bảy đoạn đầu từ SRT người dùng đã cung cấp; voice Piper tiếng Việt và âm nền tự tổng hợp được dùng lại từ bản 5 phút. Khi xuất, thời lượng được làm tròn lên lưới 30 FPS.

Hai nền raster mới trong `art` được tạo bằng **image_gen tích hợp**, sau đó chép vào dự án. Prompt nguyên văn, tên tệp và ảnh tham chiếu được lưu ở `imagegen_prompts.json`. Hình là cách hình dung cảnh sinh hoạt, không phải bản phục dựng khảo cổ chính xác. Các bộ phận nhân vật mặt tròn, thân, tay, chân, mắt/miệng và đạo cụ là SVG gốc được tạo bằng `source/make_puppets.py`. Mỗi bộ phận được đặt trong hệ cha/con, có điểm xoay và keyframe, tạo thành chuyển động trong Studio.

Clip dùng nền kín khung có phối cảnh, cận/toàn cảnh xen kẽ, biểu cảm và phản ứng ngắn, thay cho bố cục biểu tượng trên nền trắng của bản trước. Đây là bản mẫu mỹ thuật để người dùng đánh giá, chưa coi phong cách mới đã được duyệt cho toàn phim.

`source/build_sample.py` biên tập dự án; `source/export_and_verify.py` gọi bản EXE đã cài để xuất MP4, kiểm tra số frame/codec/giải mã toàn clip, trích hình và mở lại dự án. Báo cáo thực chạy ở `review/verification.json`. Không sửa mã lõi Studio cho clip thử này.
