# Angkor Wat · Một vũ trụ bằng đá

Video nguyên bản dài 60 giây, 1920×1080, 30 FPS. Kịch bản, phân cảnh, hình SVG và nhạc nền được tạo riêng cho video này. Hình vẽ sử dụng nét đen, nền trắng và màu phẳng; nhân vật có các lớp đầu, mắt, miệng, thân và các khớp tay riêng. Đây là hoạt hình cutout đơn giản có chuyển tư thế, không phải chuyển động vẽ từng khung hình. Minh họa kiến trúc và tín ngưỡng được giản lược, không phải bản phục dựng khảo cổ.

Giọng thực tế: **Hải Đăng**, giọng nam Bắc có sẵn của **VieNeu-TTS v3 Turbo**, gói `vieneu==3.8.3`, model `pnnbao-ump/VieNeu-TTS-v3-Turbo`. Chưa tìm thấy preset được xác minh mang tên Nguyễn Việt Cường. Người dùng sau đó yêu cầu lấy giọng tiếng Việt từ một repo; tên giọng thực tế được ghi rõ, không gắn nhãn sai hay nhận là giọng của cá nhân đã yêu cầu ban đầu. Repo: https://github.com/pnnbao97/VieNeu-TTS (Apache-2.0). Không clone từ video tham chiếu.

Các tên riêng có hướng dẫn phát âm riêng trong `source/story.py`; phụ đề giữ tên chuẩn. Các đoạn WAV được sinh riêng và chỉnh tốc độ đồng đều khoảng 3,7% chậm hơn để đặt trong đồng hồ 60 giây; không cắt cụt câu. Mốc phụ đề cấp câu được phân bổ trong từng đoạn lời; chưa phải forced alignment ở mức từng từ.

Nguồn kiểm chứng nội dung được lưu trong `sources.json`: APSARA National Authority, NASA Earth Observatory và nghiên cứu của Carter và cộng sự trên PNAS năm 2019. Video tham chiếu của người dùng chỉ làm mốc cách diễn giải và ngôn ngữ minh họa; không lấy khung hình hoặc âm thanh từ đó.

Mở `project.json` trong Studio để sửa từng lớp. ZIP gồm project, media và mã tạo dựng; không chứa môi trường Python hay model tải về. Có thể dựng lại với môi trường riêng `.venv` trong thư mục dự án này. Thứ tự: `source/story.py`, `source/make_voice.py`, `source/build_film.py`, `source/render_and_verify.py`.

Kết quả kiểm tra kỹ thuật sau xuất nằm trong `review/verification.json`; ảnh trích từ MP4 nằm trong `review/MP4_contact_sheet.jpg`. Kiểm tra kỹ thuật không được coi là người dùng đã duyệt mỹ thuật.
