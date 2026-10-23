# Dự án Diễn đọc Phim tài liệu: Vì sao kẻ địch của Khương Tử Nha vẫn được phong thần?

## 1. Tổng quan dự án
- **Tác phẩm nguồn**: *Phong Thần Diễn Nghĩa* (bản 100 hồi công khai trên Wikisource).
- **Nhân vật người kể chuyện**: Mỏ Đen (giọng Bắc, Custom H, nam ~30 tuổi, thông minh, sâu sắc, giàu chất triết lý nhân sinh và lòng trắc ẩn).
- **Hồ sơ giọng chuẩn**: `projects/mo_den_maya/voice_direction/selected_voice_H.json`.
- **Engine tổng hợp**: `VoxCPM2 GGUF local` tăng tốc phần cứng qua GPU Vulkan (`voices/local_design/build-vulkan/bin/studio-voice-batch.exe`).
- **Tốc độ đọc**: Tăng tốc 1.25x một lần duy nhất theo chuẩn giọng Mỏ Đen đã duyệt, đạt nhịp kể 245–275 đơn vị cách trắng/phút (thời lượng thiết kế khoảng 16–18 phút).
- **Tiêu chuẩn chất lượng**: Tuân thủ nghiêm ngặt `VIETNAMESE_NARRATION_STANDARD.md`.

---

## 2. Ý đồ biên kịch & Diễn đạt cảm xúc ("Có hồn nhấn nhá như con người")

Kịch bản được chia thành **243 cụm ý nghĩa (Semantic Units)** qua **9 phân đoạn cảm xúc lớn**, bóc tách từng tầng ý nghĩa của Phong Thần Bảng:

### Phần 1: Hai mệnh lệnh (Cues 1–13)
- *Tâm lý & Sắc thái*: Mở đầu kịch tính, dứt khoát. Tương phản mạnh mẽ giữa lệnh xử chém lạnh lùng và lệnh phong thần trang nghiêm.
- *Nhịp thở*: Nhấn vào câu hỏi tu từ và ngắt nhịp: *"Khoan đã. Lệnh giết còn chưa nguội, sao đã có lệnh bổ nhiệm?"* (nghỉ 600ms).

### Phần 2: Người đọc danh sách (Cues 14–37)
- *Tâm lý & Sắc thái*: Hồi tưởng chậm rãi về 40 năm tu hành khổ hạnh của Khương Tử Nha trên núi Côn Lôn; bi kịch bị từ chối đường tiên để gánh vác việc trần thế.
- *Hình ảnh trực quan*: *"Hãy hình dung trên bàn Mỏ Đen có hai tờ giấy. Một tờ ghi ai thắng trận. Tờ kia ghi ai đảm nhiệm chức vụ sau khi chết..."* $\to$ Giọng tâm sự, tách bạch hai khái niệm.

### Phần 3: Văn Trọng đã chết, nhưng chưa chịu cúi đầu (Cues 38–71)
- *Tâm lý & Sắc thái*: Bi tráng, kiên cường của vị thái sư tận trung.
- *Nỗi buồn sâu sắc*: Người bề tôi đã chết vẫn cố về báo mộng can gián vua, còn kẻ sống nghe xong lại gác sang một bên.
- *Khí phách trước đài*: Hồn Văn Trọng dẫn Lôi bộ đến mà chưa chịu quỳ, Tử Nha phải cầm roi nhắc sắc lệnh mới cúi đầu nhận chức.

### Phần 4: Có thần vị, tội vẫn còn (Cues 72–95)
- *Tâm lý & Sắc thái*: Sắc bén, nghiêm cẩn. Bẻ gãy ngộ nhận "phong thần = khen thưởng".
- *Phi Liêm & Ác Lai*: Tội cũ làm mất nước vẫn bị đọc rành rọt; chức Băng Tiêu Ngõa Giải là định việc cai quản thế giới tâm linh chứ không xóa bỏ bản án cuộc đời.

### Phần 5: Kẻ cản đường lại giúp danh sách thành hình (Cues 96–122)
- *Tâm lý & Sắc thái*: Hóm hỉnh, sâu cay trước nghịch lý của Thân Công Báo.
- *Nghịch lý vũ trụ*: Càng rủ người chống Tây Kỳ để trả thù cá nhân, Thân Công Báo càng kéo thêm người vào số phong thần, thực thi đúng vai trò quy tụ mà Nguyên Thủy Thiên Tôn đã thấy trước.

### Phần 6: Một chức thần có thể đổi lấy điều gì? (Cues 123–158)
- *Tâm lý & Sắc thái*: Lắng đọng xót xa trước cái giá của sự cố chấp.
- *Triệu Công Minh & Vân Tiêu*: Lời khuyên rút lui của em gái bị bỏ ngoài tai; cái chết đau đớn vì Đinh Đầu Thất Tiễn; sự phân biệt rõ ràng giữa Tiên đạo (thanh tịnh) và Thần đạo (chức trách, ràng buộc).

### Phần 7: Đứng dưới quyền người từng giết mình (Cues 159–192)
- *Tâm lý & Sắc thái*: Trầm tư về sự sắp đặt trớ trêu của trật tự mới.
- *Mối quan hệ tréo ngoe*: Tiêu Thăng bị roi Công Minh đánh chết, nay làm phó thần dưới quyền chính Công Minh; Trịnh Luân và Trần Kỳ từ hai chiến tuyến trở thành Hanh Cáp Nhị Tướng cùng canh giữ cổng trời.

### Phần 8: Người phong thần đi về đâu? (Cues 193–218)
- *Tâm lý & Sắc thái*: Nỗi ngậm ngùi lớn nhất của toàn bộ câu chuyện.
- *Số phận Khương Tử Nha*: Phong thần cho muôn người nhưng chính mình ở lại cõi phàm nhân tuổi già bóng xế. Bảy vị nhục thân thành thánh trở về núi, còn Tử Nha nhận đất Tề, kết thúc giấc mộng tiên đạo dang dở.

### Phần 9: Trở lại trước đàn (Cues 219–243)
- *Tâm lý & Sắc thái*: Đúc kết triết lý toàn diện.
- *Hình ảnh kết*: Văn Trọng từ vị tướng bại trận giữ thành Thương nay làm mây làm mưa nuôi dưỡng vạn vật. Âm hưởng vang vọng nghìn năm, để lại suy tư sâu lắng.

---

## 3. Cấu trúc thư mục dự án

```
projects/mo_den_phong_than/
├── README.md                                     # Hồ sơ dự án & ý đồ biên kịch
└── voice_direction/
    ├── 00_Kich_Ban_Goc_Day_Du.md                 # Toàn bộ bản thảo gốc (gồm cả hồ sơ biên tập)
    ├── 01_Loi_Ke_Sach.txt                        # Lời kể sạch (4,393 từ cách trắng, 147 đoạn)
    ├── 02_Bang_Doi_Chieu_Phat_Am.md              # Bảng đối chiếu phát âm danh xưng & thần vị
    ├── 03_Kich_Ban_Bien_Kich_Dien_Doc.json       # Thiết kế chi tiết 243 Semantic Units
    ├── render_phong_than_narration.py            # Pipeline tự động hóa GPU Vulkan
    ├── Mo_Den_Phong_Than_Dien_Nghia_Custom_H_1_25x.wav # File âm thanh master WAV 48kHz
    ├── Mo_Den_Phong_Than_Dien_Nghia_Custom_H_1_25x.mp3 # File nén MP3 192kbps
    ├── Mo_Den_Phong_Than_Dien_Nghia.srt          # Phụ đề đồng bộ 243 cues
    └── report_phong_than.json                    # Báo cáo đo kiểm kỹ thuật chi tiết
```
