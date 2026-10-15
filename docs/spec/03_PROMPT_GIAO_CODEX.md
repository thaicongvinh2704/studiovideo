# Prompt giao Codex xây studio

## Cách dùng

Giải nén cả bộ tài liệu vào workspace, rồi sao chép phần **Prompt triển khai** bên dưới vào Codex. Đây là lệnh dành cho phiên Codex nhận bàn giao sau này; việc tạo file tài liệu này chưa chạy lệnh xây ứng dụng. Nếu dùng Google Antigravity thay Codex, giữ nguyên yêu cầu và sử dụng một agent duy nhất trong môi trường đó.

## Prompt triển khai

Bạn hãy trực tiếp xây dựng ứng dụng local **Story Motion Studio Local** theo các tài liệu trong thư mục này. Đây là yêu cầu triển khai phần mềm chạy được, không chỉ lập thêm kế hoạch, vẽ giao diện hoặc tạo demo slideshow.

### A. Đọc yêu cầu và giữ đúng phạm vi

Đọc `00_BAT_DAU.md`, `01_KE_HOACH_STUDIO.md`, `02_HOP_DONG_DU_LIEU_VA_CONG_CU.md`, `04_LO_TRINH_VA_NGHIEM_THU.md`. Dùng `05_PHONG_LOI_NOI_DUNG.md` theo nhóm công việc liên quan; không nạp lại toàn bộ tài liệu sau mỗi thao tác. Kiểm tra AGENTS.md và repo hiện có nếu có; giữ công việc người dùng, không xóa hoặc thay repo tùy tiện.

Mục tiêu: nhận SRT và audio giọng đọc, giúp một agent lập kế hoạch nội dung/hình ảnh/chuyển động rồi điều khiển các công cụ local để xuất video YouTube có minh họa sống động. Studio dùng cho nhiều chủ đề và nhiều video, không ép mọi nội dung vào một preset. Nhân vật cần có tư thế/biểu cảm/hành động và tương tác với đạo cụ; không coi việc phóng to ảnh tĩnh là đã đạt yêu cầu hoạt hình.

Cấu hình mục tiêu đã được cung cấp đầy đủ: Windows, Intel i5-12400F, RAM 16 GB, NVIDIA RTX 3050 **6 GB VRAM**, SSD. Không hỏi lại cấu hình này. Kiểm tra driver, bộ nhớ trống và dung lượng đĩa trên máy thực tế khi cần.

Chỉ có **Codex hoặc Google Antigravity**, một agent điều khiển mỗi lần, cộng model AI miễn phí chạy local. Không spawn thêm agent/subagent nếu người dùng chưa yêu cầu. Không thêm API LLM/image/TTS/video trả phí; không tự mua credits hoặc đổi gói. Model của agent không nhúng vào backend qua API riêng. Không đề nghị thuê GPU làm mặc định.

Không triển khai Sites/website cloud, không publish internet, không đăng YouTube và không gắn thương hiệu VPN Paper Box. Tên studio là tên làm việc có thể đổi. UI tiếng Việt; mặc định video 16:9, 1080p, 30 fps, audio working 48 kHz.

### B. Các quyết định nền tảng phải giữ

1. Core Python/FastAPI/Pydantic, SQLite, worker process riêng; UI React/TypeScript; PixiJS 8 làm nền dựng 2D; FFmpeg/ffprobe xử lý/mã hóa; bridge MCP STDIO cho cả hai agent.
2. UI và MCP dùng chung service layer, project state và revision; không tạo hai pipeline độc lập.
3. Audio revision cuối làm master clock. Gắn events vào word/utterance ID cụ thể, offset chủ đích; renderer đánh giá theo frame index. SRT cue không mặc định là một cảnh.
4. Preview và export dùng cùng scene evaluator. Không export bằng quay lại playback, MediaRecorder hoặc wall-clock timer. Font, texture và video frame phải sẵn trước khi xuất.
5. Lưu bản gốc, checkpoint, job state, idempotency và cache phụ thuộc; thay một phần chỉ làm lại phần bị ảnh hưởng. Sửa thời lượng audio phải cập nhật cả mốc phía sau khi cần, không giả chỉ có một scene đổi.
6. Một GPU-heavy job hoạt động tại một thời điểm, release worker trước khi đổi tác vụ. Không bắt buộc Docker, Redis, cloud database hoặc huấn luyện model mới.
7. Scene capability manifest phải trung thực: chỉ công bố hành động đã hỗ trợ. Agent phải kiểm tra prerequisites trước khi lập asset request tốn tài nguyên.

Nếu một lựa chọn kỹ thuật thật sự không khả thi trên môi trường, ghi bằng chứng và chọn phương án thay thế nhỏ nhất giữ nguyên quyền điều khiển, dữ liệu, tính đồng bộ và giới hạn chi phí. Không đổi kiến trúc chỉ vì framework khác quen hơn.

### C. Biên tập và tài nguyên

Trước khi tạo ảnh phải có outline, scene brief, mục đích hình, chủ thể, bố cục, tư thế/biểu cảm, thông tin chưa được tiết lộ, action anchors, reference/style revision, output/layer requirements và prompt cụ thể. Các ràng buộc này được validate trước khi chạy worker.

Ưu tiên tài nguyên dùng lại và đồ họa có cấu trúc. Chữ, số liệu, sơ đồ cần chính xác được vẽ bằng công cụ, không để diffusion tự viết. Tạo bộ nhân vật gốc 2D riêng có các bộ phận/pose và hành động có thể tái sử dụng; không sao chép tài nguyên video tham chiếu. Asset mới không được mặc định là PSD tách lớp hoặc có alpha nếu workflow không hỗ trợ.

ASR dùng faster-whisper; alignment dùng WhisperX theo ngôn ngữ. Tái sử dụng transcript để tránh chạy hai lượt ASR trùng. VieNeu-TTS v3 Turbo là công cụ tạo giọng local tùy chọn. ComfyUI chạy profile ảnh local; bắt đầu một profile nhẹ đã xác minh, thêm profile chất lượng cao khi phần cứng/nhu cầu phù hợp. Kiểm tra model weights, phụ thuộc và giấy phép trước tích hợp, lưu hash/version. Không suy giấy phép weights/voices chỉ từ code license.

Không hứa diffusion luôn giữ đúng nhân vật. Giữ character kit/poses đã khóa, dùng tham chiếu và ràng buộc, sinh mới đúng phần cần thiết. Không bắt mọi video phải có lip-sync, diffusion video, LoRA training hoặc physics simulation.

Nhiều video: có ChannelProfile, EpisodePlan, EpisodeHistory, bộ nhớ sở thích có phạm vi; tham khảo tóm tắt video trước để tránh lặp. Giữ nhận diện nhưng thay cách kể theo nội dung. Không chọn bố cục/hiệu ứng ngẫu nhiên chỉ để khác biệt.

### D. Tiết kiệm token và hạn chế thử lại

Người dùng ưu tiên chuẩn bị đúng ngay từ đầu. Thực hiện chính sách sau:

- Kiểm tra kỹ thuật bằng schema/rules local, không gọi model tự chấm liên tục.
- Không mặc định sinh A/B, tạo nhiều ảnh ứng viên hoặc render preview cho mọi scene.
- **0 lần tự sinh lại vì thẩm mỹ/chất lượng**. Nếu tài nguyên sai mà không có cách sửa xác định, giữ nguyên và trả một issue cụ thể; chỉ tạo lại theo phạm vi được giao.
- Retry lỗi hạ tầng an toàn tối đa một lần; kiểm tra job provider đã hoàn thành chưa trước khi submit lại. OOM hoặc submit không rõ kết quả không phải lý do retry mù.
- Tool responses trả summary/delta/IDs; không đổ cả log, base64, transcript hay manifest dài vào context mỗi lần.
- Cache ASR, alignment, asset, render theo dependencies/version; công việc không đổi không làm lại.
- Không tự lấy footage/nhạc trên web hoặc thay lời gốc. Mặc định nhập tài nguyên có sẵn và giữ narration. Các chức năng này có thể bật ở project policy khi người dùng muốn.

Kiểm chứng khi xây phần mềm vẫn cần cho các rủi ro nền tảng nhưng phải tối thiểu, dùng fixture nhỏ và không gọi model khi không cần. Làm theo `04_LO_TRINH_VA_NGHIEM_THU.md`, không tự mở thêm nhiều vòng kiểm thử tùy hứng. Không yêu cầu video sản xuất nào cũng phải có đoạn thử riêng.

### E. Cách triển khai và làm việc

1. Bắt đầu bằng kiểm tra workspace và môi trường. Nếu không truy cập máy Windows/GPU thật, vẫn triển khai code, contracts và fixtures được; ghi rõ phần nào cần chạy trên máy mục tiêu, không ngụy tạo benchmark.
2. Tạo `AGENTS.md` ngắn cho repo, `DECISIONS.md`, `PROGRESS.md` và `docs/` phù hợp. Ghi đường dẫn file/spec, giai đoạn hiện tại, những gì đã chạy và việc tiếp theo để phiên sau không phải đọc lại mọi log.
3. Thực hiện từng giai đoạn P0–P7 trong tài liệu 04. Sau mỗi giai đoạn ghi bằng chứng ngắn và tiếp tục phần đã được giao; không hỏi “có tiếp tục không” sau mỗi bước.
4. Thiết kế contracts, source versions và master clock trước khi đầu tư giao diện lớn. Xây UI thực sử dụng API, không tạo state giả hoặc progress giả để trình diễn.
5. Tách model environments. Pin phiên bản sau xác minh compatibility. Không tự nâng driver toàn máy, tắt bảo vệ hệ thống hoặc vượt quyền của môi trường. Với cài đặt cần quyền, trình bày chính xác phần bị chặn; phần không bị chặn vẫn làm tiếp.
6. Mọi job dài trả ID, progress, cancel và resume. Mất phiên agent không làm mất tiến độ dự án.
7. Cho người dùng xem/chỉnh scene, prompt, tài nguyên, keyframe và mốc lời qua UI; JSON chỉ ở phần nâng cao.
8. Cung cấp cấu hình kết nối thực tế cho Codex và Antigravity. Chỉ một client ghi tại một thời điểm. Không khẳng định đã thử client nào nếu không thực sự có client đó.

### F. Điều kiện hoàn thành

- Có launcher local, hướng dẫn tiếng Việt và doctor cho máy mục tiêu.
- Import SRT/audio, chuẩn bị/căn lời, tạo và commit plan, gọi media worker, dựng 2D và xuất MP4 thật.
- Có ít nhất một tương tác nhân vật–đạo cụ thực trong đoạn tích hợp; chữ/ảnh xuất hiện theo mốc lời, không slideshow giả.
- Timeline seek và export dùng cùng clock; chức năng sửa cục bộ, resume, revision conflict và cache được chứng minh bằng các kiểm chứng nhỏ đã định.
- Một project mở lại được; final export chỉ dùng đúng revision. Không còn placeholder mà ghi trạng thái đã hoàn tất.
- ASR, ảnh local, TTS có adapter thực và trạng thái cài đặt minh bạch. Feature chưa có model hoặc chưa chạy được phải hiện chưa sẵn sàng; không giả có kết quả.
- Không cần thêm AI trả phí. Các hạn chế về tốc độ, model chất lượng cao hoặc bộ nhớ phải được báo rõ.

Khi bàn giao, báo: cách chạy; phần đã hoàn thành; các kiểm chứng đã chạy; file video mẫu thực tế nếu có; phần còn chưa xác minh; cấu hình agent; cách sửa một cảnh và tiếp tục dự án. Không tuyên bố đạt chất lượng ngang video tham chiếu chỉ vì render thành công.

**Hãy bắt đầu triển khai theo tài liệu, không trả lời chỉ bằng một kế hoạch mới.**

## Prompt tiếp tục phiên làm việc

Tiếp tục triển khai Story Motion Studio Local trong workspace hiện tại. Đọc AGENTS.md, PROGRESS.md và DECISIONS.md trước; sau đó chỉ đọc phần đặc tả liên quan đến giai đoạn đang làm. Giữ code, assets, model và kết quả đã có; không khởi tạo lại dự án, không chạy lại model/test đã đạt nếu không có thay đổi liên quan. Hoàn thành việc còn lại theo `04_LO_TRINH_VA_NGHIEM_THU.md`. Vẫn dùng một agent, không thêm AI trả phí, không tự chạy vòng sinh lại vì chất lượng. Nếu gặp lỗi, sửa phạm vi nhỏ nhất và ghi rõ checkpoint tiếp theo.

## Prompt sản xuất một video khi studio đã sẵn sàng

Hãy dùng studio local để tạo một video từ cặp SRT và audio tôi chọn trong dự án này. Trước hết đọc project summary, policy, capability manifest, channel profile và một số episode summaries liên quan; không đọc lại toàn bộ thư viện. Giữ nội dung và giọng gốc trừ phần tôi đã cho phép sửa.

Lập outline toàn bài rồi chuẩn bị scene briefs, prompt ảnh, tài nguyên, hành động, cảm xúc, mốc lời và âm thanh. Giữ nhận diện của kênh, chọn hướng kể phù hợp nội dung mới và tránh lặp công thức của các tập trước. Commit bản dựng khi điều kiện kỹ thuật hợp lệ; không yêu cầu tôi duyệt từng prompt nếu không có quyết định thật sự cần tôi chọn.

Tái sử dụng tài nguyên trước, tạo local phần còn thiếu; không sinh A/B, không tự đánh giá–tạo lại liên tục. Dùng audio master và anchors thực để đồng bộ. Giao bộ điều phối chạy các job local, chỉ đọc kết quả tóm tắt và vấn đề cần xử lý. Không sửa lại phần không bị ảnh hưởng.

Xuất MP4 và SRT cùng dự án chỉnh sửa được, cập nhật episode history. Báo những phần chưa xác minh hoặc có ngoại lệ; không tự đăng YouTube. Nếu thiếu quyền để sửa nội dung, thiếu tài nguyên bắt buộc hoặc có mâu thuẫn ảnh hưởng ý nghĩa, hỏi một câu cụ thể kèm đoạn liên quan; các công việc không bị ảnh hưởng vẫn tiếp tục.
