# Lộ trình xây và nghiệm thu có giới hạn

Phiên bản 1.0 — 14/10/2026. Không có thời gian hoàn thành cố định vì chưa đo môi trường mục tiêu. Một agent triển khai tuần tự. “P0–P7” trong file này là giai đoạn, không phải mức nghiêm trọng của issue.

## 1. Nguyên tắc kiểm chứng

Phân biệt kiểm chứng chức năng trong lúc xây phần mềm và đánh giá sáng tạo của từng video. Người dùng không muốn vòng tạo–chấm–tạo lại tốn token. Bộ này không yêu cầu vòng đó.

- Dùng một bộ fixture nhỏ, tái sử dụng qua các giai đoạn; ưu tiên kiểm tra bằng code local.
- Thay đổi chỉ một module thì chạy đúng kiểm chứng liên quan, không toàn suite tùy hứng.
- Không ASR/TTS/sinh ảnh thật cho test parser, cache, state hoặc timeline có thể dùng fixture.
- Một lần kiểm tra model nhỏ khi tích hợp đúng worker; không tải hàng loạt model để so sánh.
- Không chạy audit hình bằng AI cho mọi asset/scene; không tự làm nhiều phiên bản cho đẹp hơn.
- Kiểm chứng phần mềm không thay thế việc người dùng đánh giá gu. Khi cần phản hồi, đưa đúng đoạn minh họa và câu hỏi cụ thể.

## 2. Các giai đoạn

| Giai đoạn | Công việc | Đầu ra phải có | Điều kiện hoàn thành | Không mở rộng sang |
|---|---|---|---|---|
| **P0 — khởi tạo đúng môi trường** | Đọc spec, inspect repo, doctor, bố trí env, registry nguồn model và thư mục dữ liệu | Repo, decisions/progress, cấu hình máy, danh sách dependency thiếu | Biết phần nào chạy trên máy thật; không nhầm môi trường cloud; không cần API trả phí | Làm UI bóng bẩy hoặc tải nhiều model |
| **P1 — dữ liệu và điều phối** | Schema, SQLite, import, revisions, jobs, leases, cache, checkpoint | Core API và CLI nhỏ hoạt động | Import Unicode, job idempotent, conflict/resume hoạt động trên fixture | Lập kế hoạch AI bằng template giả |
| **P2 — audio và clock** | Audio master, normalize kỹ thuật, SRT parser, ASR/alignment adapters, anchors/time map | Audio analysis, mismatch list, word/câu anchors và timeline contracts | Đồng hồ sample/frame đúng; không timestamp giả; sửa audio invalidation đúng phạm vi | Tạo lại lời gốc không được yêu cầu |
| **P3 — bộ dựng 2D và export** | Scene graph, keyframe, pose, attachment, camera, text, offline export, FFmpeg | Renderer thật, clip MP4 từ fixture, preview seek | Một hành động với đạo cụ; frame clock đúng; không thu playback realtime | Physics, full 3D, lip-sync hoặc generative video |
| **P4 — biên tập và tài nguyên** | Channel/episode plan, scene brief, preflight, prompt requests, shared library, ComfyUI/TTS | Plan editor, asset pipeline thực, model profiles/policies | Không sinh trước preflight; cache đúng; TTS tùy chọn; asset quyền dùng được ghi rõ | Tự kiểm tra bằng nhiều AI, train LoRA |
| **P5 — giao diện và agent** | UI tiếng Việt nối API, MCP bridge, client configs, capability manifest | Agent điều khiển project, user chỉnh scene/timeline | Tool dùng cùng service với UI; response gọn, job dài trả ID; chỉ một writer agent | Hosted SaaS, cloud billing, đăng YouTube |
| **P6 — tích hợp có mục tiêu** | Tái dùng fixture cho một đoạn 45–60 giây có nhiều nhịp và tương tác | Video thật + project reopen + báo cáo ngắn | Đường từ audio/plan/assets đến MP4 hoạt động; lỗi kỹ thuật đã sửa theo phạm vi | Nhiều vòng làm đẹp hoặc benchmark model hàng loạt |
| **P7 — bàn giao và vận hành nhiều video** | Launcher, docs, backup, episode history, queue, khả năng video dài | Hướng dẫn sử dụng, cấu hình client, migration/backup, giới hạn đã biết | Một dự án mới dùng lại assets nhưng hướng kể khác; không mất dữ liệu khi chuyển phiên | Tự coi là đạt mọi chủ đề/mọi độ dài |

Các giai đoạn có thể chia nhánh code theo modules nhưng một agent điều khiển. Không cần hỏi người dùng “tiếp tục?” giữa các giai đoạn đã được giao. Không phát triển hết GUI trước khi P2/P3 chứng minh được clock/export.

## 3. Bộ fixture chung

Tạo kịch bản giả định ngắn, được ghi rõ là minh họa, có:

- Từ phủ định và một tên riêng để kiểm tra mismatch.
- Một câu kéo đồ vật hoặc cầm đạo cụ có nhiều sự kiện theo lời.
- Một câu có nhịp tiết lộ, một con số và chữ tiếng Việt.
- Một đoạn tĩnh có chủ ý để không mặc định “không chuyển động là lỗi”.

Audio thử có thể do người dùng cung cấp hoặc dùng một lần giọng preset local khi worker TTS đã tích hợp. Trước đó, test kỹ thuật dùng waveform/tone và timestamp fixture tổng hợp; ghi rõ loại dữ liệu, không nói đã kiểm chứng tiếng Việt thật bằng sine tone.

Scene assets kỹ thuật dùng SVG tự dựng và text thật. Một ảnh local nhỏ chỉ để xác minh adapter sinh/ghi file/cache. Đoạn tích hợp có thể dùng lại những asset này; việc chọn thêm tài nguyên theo gu người dùng không biến thành benchmark nhiều model.

## 4. Các kiểm chứng nền tảng bắt buộc

| ID | Rủi ro cần loại trừ | Kiểm chứng nhỏ | Tiêu chí |
|---|---|---|---|
| V01 | Import làm hỏng dữ liệu | File tên tiếng Việt/khoảng trắng, SRT BOM và cue không hợp lệ | Bản gốc không đổi; parser nêu đúng lỗi; nguồn có hash |
| V02 | Sai clock/drift | Anchor tổng hợp ở đầu, giữa và cuối timeline logic 15 phút; cùng event qua preview/export | Cùng frame index cho cùng event; sai số lượng tử trong quy tắc dưới một frame, không tích lũy |
| V03 | Seek khác playback | Seek trực tiếp vào giữa và sau một pose swap/attachment | Trạng thái giống đánh giá theo thứ tự trong cùng runtime; không phụ thuộc callback đã chạy |
| V04 | Chuyển cảnh làm lặp/mất frame | Hai render spans có transition và frame counter tổng hợp | Phủ đúng `[0,N)`, không gap/overlap; video/audio cuối không bị kéo vì transition |
| V05 | Audio edit dùng cache cũ | Đổi gain rồi đổi duration một đoạn trong fixture | Gain không tạo lại hình; duration cập nhật downstream anchors/spans cần thiết |
| V06 | Job bị gọi lặp/ngắt | Gọi cùng idempotency key; ngắt sau checkpoint rồi resume | Một kết quả logic, không mất scene, không sinh thêm asset trùng |
| V07 | Ghi đè từ agent/UI | Hai mutation cùng expected_revision hoặc hai agent leases | Một ghi thành công; thao tác xung đột bị từ chối có delta; không mất sửa tay |
| V08 | Worker vượt policy | Thiếu VRAM giả lập, workflow thiếu model, request TTS không được phép | Chặn trước job hoặc ghi lỗi rõ; không chuyển cloud, không tự tạo lại vô hạn |
| V09 | Output final không đúng | Export fixture bằng profile cuối và ffprobe/decode kiểm tra | Đúng video/audio/subtitle revision, kích thước/fps; frame count như timeline; duration xử lý codec padding đúng |
| V10 | Tái sử dụng/backup không thật | Mở lại project, phục hồi backup, đổi một asset | References tìm đúng; chỉ cache liên quan invalidated; nguồn còn nguyên |

V02 kiểm chứng toán thời gian, không phải benchmark render thực 15 phút. V09 kiểm chứng file ngắn thật. Lượt video dài thực đầu tiên có thể là công việc sản xuất; nếu chưa chạy thì bàn giao phải ghi “chưa đo hiệu năng video dài trên máy này”, không chạy thêm full render chỉ để có nhãn đã test.

Kiểm tra drift thực dùng fiducial frame và audio marker có thời điểm biết trước trong fixture, tính cả AAC priming/padding của file đã encode. Đặt mục tiêu kỹ thuật sai lệch sau decode không quá một frame ở 30 fps cho marker chuẩn; đây không phải cam kết độ chính xác word alignment của speech thật. Nếu không đạt, sửa timebase/mux, không tự kéo tốc độ narration để che lỗi.

## 5. Ngân sách kiểm chứng khởi đầu

| Loại | Mặc định |
|---|---|
| Fixtures kỹ thuật | Một bộ dùng chung, chạy phần liên quan sau thay đổi |
| ASR/alignment thật | Một đoạn ngắn khoảng 20–30 giây; cache để tái sử dụng |
| TTS thật | Một đoạn ngắn, chỉ khi tích hợp nhánh TTS; không thử nhiều giọng tự động |
| Ảnh local | Một request nhỏ để kiểm chứng worker/profile đầu tiên, không A/B |
| Clip tích hợp | Một clip 45–60 giây tái sử dụng tài nguyên, không tạo nhiều bản toàn clip vì thẩm mỹ |
| Sửa lỗi chức năng | Sửa đúng module, chạy lại kiểm chứng bị ảnh hưởng; không dùng giới hạn để bỏ qua lỗi thật |
| Sinh lại vì gu/chất lượng | 0 tự động; có yêu cầu cụ thể thì phạm vi do yêu cầu quyết định |

Đây là ngân sách đề xuất nhằm tránh mở rộng ngoài mục tiêu. Nếu lỗi kỹ thuật thật cần kiểm chứng bổ sung, ghi rủi ro cụ thể và phép kiểm tra nhỏ nhất. Không hứa có thể phát triển phần mềm đáng tin cậy với hoàn toàn không kiểm chứng.

## 6. Đánh giá đoạn tích hợp

Không dùng điểm tự chấm của agent như bằng chứng nghệ thuật. Đoạn tích hợp cần thể hiện trực tiếp:

1. Nhân vật/đạo cụ có chuyển động riêng và quan hệ tiếp xúc rõ.
2. Hình, chữ, hành động bám các mốc lời cụ thể.
3. Có ít nhất hai cách trình bày hợp ý, không chỉ thay nền.
4. Có một nhịp giữ hình hoặc tiết lộ có chủ đích.
5. Chữ Việt đúng, lời nghe rõ, file xuất thật và mở lại dự án được.

Agent mô tả chính xác dữ liệu đã kiểm tra. Chỉ xem storyboard thì ghi đã xem storyboard; không khẳng định đã nghe hoặc xem toàn video. Người dùng có thể góp ý một lần về hướng hình/nhịp; không biến phản hồi thành yêu cầu mọi cảnh phải qua duyệt bắt buộc.

## 7. Những điều không được coi là hoàn thành

- UI đẹp nhưng renderer/worker trả dữ liệu giả.
- Chỉ nhận prompt tự do rồi tự tạo ảnh không có scene plan, model registry hay revision.
- Render dựa vào tốc độ phát realtime khiến máy chậm làm video lệch.
- Một ảnh nguyên khối zoom/pan thay cho tương tác nhân vật đã cam kết.
- Cài ComfyUI nhưng không gọi được job, nhận kết quả hoặc lưu provider_job_id.
- TTS phải dùng API trả phí hoặc âm thanh tạo ra chưa được tích hợp vào revision/anchor.
- Agent mất phiên thì phải bắt đầu toàn bộ dự án lại.
- Chỉ đọc model docs nhưng báo đã chạy trên RTX 3050.
- Tự báo “đã đạt giống mẫu” mà chỉ có các test kỹ thuật.

## 8. Bàn giao cuối cùng của người triển khai

| Hạng mục | Bằng chứng |
|---|---|
| Chạy local | Launcher, README tiếng Việt, doctor output có phần chưa sẵn sàng |
| Kết nối agent | Config mẫu đúng đường dẫn và client; nêu client thực sự đã dùng |
| Dự án demo | SRT/audio/plan/asset/timeline và MP4 thực nếu môi trường cho phép |
| Tiếp tục công việc | PROGRESS.md, checkpoint, resume workflow |
| Sửa cục bộ | Một thay đổi minh họa và danh sách spans/jobs tái sử dụng |
| Kiểm chứng | Kết quả V01–V10, phần nào chưa chạy, không tự thêm số liệu |
| Dữ liệu | Backup/import, model/license/source registry |
| Hạn chế | Khả năng motion thực có, model nào đủ/không đủ phần cứng, giới hạn quan sát media |

Nếu môi trường chỉ là cloud sandbox, bàn giao code hoạt động ở phạm vi đã chạy và hướng dẫn cài trên Windows. Không gọi đó là “đã nghiệm thu máy người dùng” khi chưa có bằng chứng.
