# Vườn treo Babylon — Kỳ quan ở đâu?

Phim minh họa 60 giây, Full HD 1920 × 1080, 30 FPS, tiếng Việt. Bảy cảnh bám một câu hỏi: ý tưởng một khu vườn trên cao hấp dẫn ra sao, và vì sao địa điểm của kỳ quan vẫn chưa được xác định chắc chắn.

Mỹ thuật dùng hướng tranh truyện màu phẳng của mẫu Angkor Wat số 2: nét viền đậm có chi tiết chọn lọc, bóng ba sắc độ, đá vàng đất, cây xanh và nước xanh lam ngọc. Năm bối cảnh và một lớp cây nền trong suốt được tạo bằng công cụ image_gen, không phải ảnh khảo cổ hoặc SVG vẽ tay. Prompt nằm trong `art/prompts.json`. Sơ đồ vị trí, các lớp nhấn và đường nước được viết bằng SVG và các lớp vector của Studio.

Đây là hoạt họa minh họa 2.5D: điểm nhìn di chuyển, tiền cảnh cây có chuyển động riêng, gợn sáng mặt nước, mốc vị trí và tuyến dẫn nước xuất hiện theo nội dung. Không có người dẫn chỉ tay và không có hoạt họa nhân vật từng khung hình. Các ảnh bối cảnh là raster; các lớp ảnh, chữ, đường dẫn và keyframe được sửa trong `project.json` bằng Studio. Một ảnh bối cảnh chưa được tách từng cây và từng viên gạch.

Các khu vườn, mặt cắt, tư liệu và cảnh khảo cổ trên hình đều là minh họa. Hình dáng chính xác và cơ cấu tưới chưa được xác nhận; tuyến nước chỉ biểu diễn nhu cầu nâng và phân phối nước. Các bảng đất không được dùng như bản sao hoặc bản dịch của hiện vật có thật. Sơ đồ Babylon / Nineveh chỉ diễn tả vị trí tương đối.

Nguồn nội dung: British Museum, Bộ Văn hóa Pháp và Somerville College, Oxford, được lưu với phạm vi hỗ trợ trong `sources.json`. Giả thuyết Nineveh được trình bày như một đề xuất nghiên cứu, không coi là sự thật đã ngã ngũ.

Giọng đọc thực tế: Hải Đăng của VieNeu-TTS v3 Turbo, chạy từ repo https://github.com/pnnbao97/VieNeu-TTS bằng môi trường và model đã cài cho dự án Angkor Wat. Không gắn tên giọng Nguyễn Việt Cường. Lời đọc được tạo từng câu, sau đó đổi tốc độ đồng đều để vừa 60 giây. Mốc câu được đo từ WAV; một số câu dài chia phụ đề theo tỷ lệ số từ, không phải căn từng từ bằng forced alignment.

Nhạc gảy, nền nước và âm chuyển cảnh được tổng hợp nguyên bản trong `source/build_film.py`; không được mô tả như âm nhạc Babylon xác thực. Không lấy âm thanh hay khung hình từ video tham chiếu của người dùng.

Trình tự dựng lại: `source/make_voice.py`, `source/build_film.py`, `source/export_and_verify.py`. Cần Studio cùng các phụ thuộc Python, FFmpeg và model VieNeu đã cài; ZIP không chứa môi trường và model. Trình phát cục bộ `source/preview_server.py` chỉ phục vụ video và gói project trên địa chỉ 127.0.0.1.
