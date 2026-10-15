# Bộ bàn giao xây studio video local

Phiên bản 1.0 — 14/10/2026. Đây là tài liệu và prompt để giao Codex triển khai; chưa phải ứng dụng đã xây.

## Cách dùng

1. Giải nén bộ tài liệu vào một thư mục dự án trên máy Windows của bạn.
2. Mở thư mục đó trong Codex chạy trên máy bạn, hoặc phiên agent có quyền truy cập đúng máy. Phiên cloud không tự có quyền dùng RTX 3050 của máy bạn.
3. Mở `03_PROMPT_GIAO_CODEX.md`, sao chép toàn bộ phần **Prompt triển khai** và gửi cho Codex. Giữ các tài liệu khác trong thư mục để Codex đọc theo từng giai đoạn.
4. Khi cần tiếp tục phiên mới, dùng **Prompt tiếp tục** trong cùng file. Khi studio đã hoàn thành, dùng **Prompt sản xuất một video**.

Không cần mua API AI riêng. Codex/Antigravity dùng quyền truy cập model của tài khoản đang có; các bước ASR, tạo ảnh, TTS, dựng, render chạy local. Hạn mức gói agent vẫn áp dụng. Các tác vụ local không tiêu thụ token của gói agent để chạy suy luận, nhưng việc agent lập kế hoạch và đọc kết quả vẫn tiêu thụ hạn mức.

## Các tài liệu

| File | Nội dung | Ai cần đọc |
|---|---|---|
| `01_KE_HOACH_STUDIO.md` | Phạm vi, kiến trúc, công cụ, biên tập, nhiều video, GPU và trải nghiệm vận hành | Bạn và agent |
| `02_HOP_DONG_DU_LIEU_VA_CONG_CU.md` | Timeline, cấu trúc dữ liệu, công cụ MCP, phiên bản, lỗi và cache | Agent xây phần mềm |
| `03_PROMPT_GIAO_CODEX.md` | Prompt xây, tiếp tục và vận hành | Bạn sao chép phần phù hợp |
| `04_LO_TRINH_VA_NGHIEM_THU.md` | Các giai đoạn, điều kiện hoàn thành và kiểm chứng tối thiểu | Bạn và agent |
| `05_PHONG_LOI_NOI_DUNG.md` | 50 rủi ro chuyển thành biện pháp phòng ngừa theo chính sách tiết kiệm token | Agent theo giai đoạn liên quan |

## Yêu cầu đã chốt

- Đầu vào chính: SRT + file giọng đọc; sản xuất nhiều video YouTube theo hướng minh họa/giải thích có chuyển động.
- Máy: i5-12400F, RAM 16 GB, RTX 3050 **6 GB VRAM**, SSD, Windows.
- Một agent điều khiển tại một thời điểm: Codex **hoặc** Google Antigravity.
- Không thêm AI trả phí, không yêu cầu API key của nhà cung cấp AI khác.
- Chuẩn bị nội dung, prompt, tài nguyên và chuyển động trước khi tạo; hạn chế vòng AI tự xem lại rồi tạo lại.
- Một video mẫu là tham khảo chất lượng, không phải khuôn bắt buộc cho mọi video.
- Không tự đăng YouTube, không gắn thương hiệu VPN Paper Box vào dự án này.

## Mặc định để có thể triển khai ngay

Tên làm việc: **Story Motion Studio Local**, có thể đổi trong giao diện. Giao diện tiếng Việt. Video ngang 1080p/30 fps; preview 720p. Audio làm chuẩn thời gian. Giữ nội dung lời đọc và bản gốc; sửa nghĩa hoặc TTS thay đoạn chỉ khi quyền dự án cho phép. Tư liệu web là tùy chọn, mặc định không tự tìm/tải. Những mặc định này được chỉnh ở cấu hình, không khóa cứng.

## Chính sách kiểm tra mới nhất

Đây là quy tắc ưu tiên, thay cho các mô tả trước đó về vòng agent tự kiểm tra–sửa liên tục:

- Kiểm tra điều kiện trước khi tạo, bằng schema/quy tắc local.
- Không tự tạo A/B, không tự sinh lại vì agent cho điểm thẩm mỹ thấp.
- Mặc định **0 lần tự tạo lại vì chất lượng**; chỉ retry lỗi hạ tầng an toàn có giới hạn.
- Kiểm chứng chức năng lúc xây phần mềm dùng dữ liệu nhỏ, tổng hợp và miễn phí; không chạy model ảnh/TTS cho các test không cần chúng.
- Một đoạn tích hợp ngắn trong giai đoạn xây để chứng minh đường xuất và hành động hoạt động. Không yêu cầu mỗi video sau đều có một vòng dựng thử riêng.
- Sửa cục bộ; không phân tích lại và render lại toàn bộ khi dữ liệu liên quan không đổi.

## Điều tài liệu không khẳng định

Chưa cài đặt, benchmark hoặc chạy studio trên máy bạn. Chưa bảo đảm độ hấp dẫn ngang video mẫu hoặc thời gian sản xuất cố định. Phần mềm có thể đảm bảo hợp đồng thời gian/phiên bản qua kiểm chứng chức năng; chất lượng hình sinh và lựa chọn biên tập còn phụ thuộc tài nguyên, model và nội dung.

## Thứ tự ưu tiên khi có mâu thuẫn

Chỉ dẫn mới trực tiếp của người dùng → yêu cầu đã chốt trong bộ này → `01` về phạm vi và chính sách → `02` về hợp đồng kỹ thuật → `04` về nghiệm thu → `05` về phòng lỗi. Ví dụ trong tài liệu là minh họa, không được ghi đè quy tắc. Agent ghi quyết định mới vào `DECISIONS.md` và trạng thái vào `PROGRESS.md` khi thực sự triển khai.
