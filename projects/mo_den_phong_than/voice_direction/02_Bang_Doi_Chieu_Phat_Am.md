# Bảng đối chiếu phát âm (Pronunciation & Context Ledger)
**Dự án:** Mỏ Đen — Vì sao kẻ địch của Khương Tử Nha vẫn được phong thần?  
**Quy chuẩn áp dụng:** `VIETNAMESE_NARRATION_STANDARD.md`  
**Giọng đọc:** Mỏ Đen · Giọng Bắc · Hồ sơ Custom H (`projects/mo_den_maya/voice_direction/selected_voice_H.json`)  
**Nguyên tắc:** 
1. Giữ nguyên 100% ngữ nghĩa và chính tả gốc trong kịch bản lưu trữ và phụ đề hiển thị (SRT).
2. Phiên âm / chuẩn hóa chỉ áp dụng trong lớp TTS đọc (TTS Reading Layer) để model tổng hợp phát âm tròn vành rõ chữ, đúng thanh điệu, không vấp.
3. Toàn bộ các mốc hồi (hồi năm mươi hai, hồi một trăm...) và số năm tu hành (ba mươi hai, bảy mươi hai, bốn mươi năm...) đã được viết sẵn bằng chữ tiếng Việt trong bản thảo gốc, đảm bảo tính chuẩn mực tuyệt đối.

---

## 1. Bảng đối chiếu các danh xưng & chức vị đặc biệt

| STT | Cụm từ gốc (Kịch bản & Phụ đề) | Cách đọc TTS (Reading Layer) | Vai trò / Ngữ cảnh trong Phong Thần |
|---|---|---|---|
| 1 | **Khương Tử Nha** | Khương Tử Nha | Nhân vật chính, đệ tử Nguyên Thủy Thiên Tôn, người thừa sắc phong thần. |
| 2 | **Nguyên Thủy Thiên Tôn** | Nguyên Thủy Thiên Tôn | Giáo chủ Xiển Giáo, sư phụ Khương Tử Nha, người ban sắc phong thần. |
| 3 | **Côn Lôn** | Côn Lôn | Núi Côn Lôn (Côn Lôn Sơn), nơi tu đạo của Tử Nha trong 40 năm. |
| 4 | **Trụ Vương** | Trụ Vương | Vị vua cuối cùng của nhà Thương. |
| 5 | **Đát Kỷ** | Đát Kỷ | Vương phi mê hoặc Trụ Vương. |
| 6 | **Văn Trọng** | Văn Trọng | Thái sư đầu triều nhà Thương, trụ cột tận trung đến chết tại Tuyệt Long Lĩnh. |
| 7 | **Tuyệt Long Lĩnh** | Tuyệt Long Lĩnh | Nơi Văn Trọng trúng kế thần hỏa của Vân Trung Tử và hy sinh. |
| 8 | **Vân Trung Tử** | Vân Trung Tử | Tiên nhân Xiển giáo vây hãm Văn Trọng bằng Thông Thiên Thần Hỏa Trụ. |
| 9 | **mặc kỳ lân** | mặc kỳ lân | Linh thú thú cưỡi màu đen của Văn Trọng tử trận cùng chủ. |
| 10 | **Lôi bộ** | Lôi bộ | Bộ sấm sét trong thiên đình do Văn Trọng đứng đầu. |
| 11 | **Cửu Thiên Ứng Nguyên Lôi Thanh Phổ Hóa Thiên Tôn** | Cửu Thiên Ứng Nguyên Lôi Thanh Phổ Hóa Thiên Tôn | Thần vị tối cao của Văn Trọng cai quản Lôi bộ, mây mưa và thưởng phạt. |
| 12 | **Phi Liêm, Ác Lai** | Phi Liêm, Ác Lai | Hai gian thần bán nước hàng Chu, bị Tử Nha chém đầu rồi phong thần. |
| 13 | **Băng Tiêu Ngõa Giải** | Băng Tiêu Ngõa Giải | Tinh tú thần vị của Phi Liêm - Ác Lai (ngụ ý băng tan ngói vỡ, tan rã). |
| 14 | **Thân Công Báo** | Thân Công Báo | Sư đệ đối nghịch của Tử Nha, rủ rê các tiên nhân cản đường Tây Kỳ. |
| 15 | **Phân Thủy Tướng Quân** | Phân Thủy Tướng Quân | Thần vị của Thân Công Báo cai quản phân ranh giới nước ở Đông Hải. |
| 16 | **Triệu Công Minh** | Triệu Công Minh | Đại tiên Tiệt giáo ở Nga Mi sơn, bạn thân Văn Trọng, tử trận vì Đinh Đầu Thất Tiễn. |
| 17 | **Vân Tiêu** | Vân Tiêu | Em gái Công Minh (Tam Tiêu nương nương), người khuyên anh dừng bước chiến tranh. |
| 18 | **Lục Áp** | Lục Áp | Tán tiên trao phép Đinh Đầu Thất Tiễn cho Khương Tử Nha. |
| 19 | **Đinh Đầu Thất Tiễn** | Đinh Đầu Thất Tiễn | Phép thuật dùng hình nhân rơm bắn tên để đoạt mệnh Triệu Công Minh. |
| 20 | **Huyền Đàn Chân Quân** | Huyền Đàn Chân Quân | Thần vị của Triệu Công Minh (Chính Nhất Long Hổ Huyền Đàn Chân Quân - Tài thần). |
| 21 | **Tiêu Thăng, Cao Bảo** | Tiêu Thăng, Cao Bảo | Hai ẩn sĩ núi Vũ Di; Tiêu Thăng dùng Lạc Bảo Kim Tiền rớt báu vật nhưng bị roi đánh chết. |
| 22 | **Lạc Bảo Kim Tiền** | Lạc Bảo Kim Tiền | Đồng tiền có cánh làm rơi pháp bảo của Triệu Công Minh. |
| 23 | **Định Hải Châu** | Định Hải Châu | Hai mươi bốn hạt châu chí bảo của Triệu Công Minh. |
| 24 | **Chiêu Bảo Thiên Tôn** | Chiêu Bảo Thiên Tôn | Thần vị của Tiêu Thăng, xếp làm thuộc hạ dưới quyền Triệu Công Minh. |
| 25 | **Trịnh Luân, Trần Kỳ** | Trịnh Luân, Trần Kỳ | Hai tướng có dị thuật (thổi khí trắng / khí vàng), phong chung làm Hanh Cáp Nhị Tướng. |
| 26 | **Hanh Cáp Nhị Tướng** | Hanh Cáp Nhị Tướng | Hai vị hộ pháp giữ cửa chùa / đền miếu. |
| 27 | **Dương Tiễn, Na Tra** | Dương Tiễn, Na Tra | Nhóm bảy tướng lập công nhưng không nhận chức thần, trở về núi "nhục thân thành thánh". |
| 28 | **nhục thân thành thánh** | nhục thân thành thánh | Tu luyện thành tiên ngay bằng thân xác sống, không cần chết để nhận sắc phong. |

---

## 2. Kiểm chứng kỹ thuật và QC phát âm
- Đã xác nhận toàn bộ danh xưng tiếng Hán Việt chuẩn xác theo âm học truyền thống của tiểu thuyết *Phong Thần Diễn Nghĩa*.
- Lớp phát âm tiếng Việt đảm bảo phát âm rõ ràng, chuẩn 6 thanh điệu (ngang, huyền, sắc, hỏi, ngã, nặng) theo đúng âm vực trầm ấm, thông minh của giọng Bắc Mỏ Đen.
