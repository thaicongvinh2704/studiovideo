# Tiến độ

2026-10-14. Đã nhận đủ docs/spec/00–05 và triển khai nền tảng 0.1 trên Windows thật. Không khẳng định hoàn thành toàn bộ sản phẩm/gu tham chiếu.

## Đã hoạt động

- FastAPI/Pydantic/SQLite, source hash bất biến, import SRT BOM/Unicode và audio working 48 kHz.
- Revision/optimistic conflict, idempotency, một phiên agent lease trên toàn studio. SQLite schema v2, backup trước migration.
- Job queue bền, snapshot, progress/SSE, cancel/resume, cache theo dependency. Worker nặng tuần tự, subprocess được thu hồi.
- Timeline sample/frame, anchors theo ID/mốc thủ công có evidence; span nửa mở liên tục.
- PixiJS 8 preview/export chung evaluator: transform/keyframe, pose/expression, point/look, hand attachment, camera, text, arrow/path, cut/dissolve.
- MP4 48 giây 1080p30 đã xuất bằng NVENC, 1.440 frame + SRT/manifest. Audio của clip này là tone tổng hợp, không narration.
- UI tiếng Việt nối API thật, editor scene/layer/keyframe, form prompt/event/anchor, waveform, queue, policy, backup/restore và thư viện dùng chung.
- MCP STDIO thật qua SDK ClientSession; config mẫu Codex/Antigravity. Chưa kết nối bằng các client đó.
- TTS VieNeu 3.7.1 CPU/ONNX fp32 đã tạo 16,99 giây, một preset trong SDK. Whisper medium CPU/INT8 đã nhận dạng cùng đoạn, bốn segment, diff không báo mismatch. Không tuyên bố đã nghe toàn audio.
- Backup/restore, shared library API, image replacement giữ source/motion, episode history API.

## Bằng chứng

- 8 test foundation, 3 test cache/lease/coalescing, 2 test resource/cancel và 1 test asset replacement đã qua theo từng nhóm liên quan. Không chạy lại model đã thành công.
- reports/browser-verification.json: seek trực tiếp và tuần tự tới frame 390 trả cùng PNG; ảnh UI trong reports/studio-ui.png.
- reports/live-verification.json: job thật idempotent, cancel sau checkpoint và resume cùng ID (2 attempts, 3 cached spans). Audio marker sau decode lệch fiducial khoảng 0,000042 giây ở giây 34 và 46; tiêu chí 1/30 giây.
- reports/speech-verification.json: TTS/ASR thật, không chất lượng tự chấm.
- reports/mcp-verification.json: transport STDIO, 41 tools; initialize/list_tools/capabilities/summary/preflight đã qua.
- reports/integration-session.json chứa project/job IDs; job_fa17591013ac4766 là clip cuối dùng rig parts/pivots đã pin, ffprobe đạt; file/ref bàn giao trong reports/delivery.json.
- reports/image-verification.json: SD 1.5 thật 512×512 opaque, provider_job_id 5d366e81-cbcd-4aa5-b921-bf15ae33d700; cache hit không sinh lần hai, shared asset dùng lại ở project thứ hai.
- Dự án thứ hai có outline/hướng so sánh, dùng ảnh shared, plan committed và timeline compiled; không render thêm toàn clip.

## Đang chờ / chưa xác minh

- ComfyUI commit e0a32bce84f4603f2b61b16b50f8958e68fd6171 + SD 1.5 4,27 GB đã cài/pin hash/chạy một ảnh trên RTX 3050. Job job_547711b4bb924ff3 succeeded; process đã đóng, GPU/RAM được release.
- Người dùng đã đóng app nặng; RAM đo lúc tiếp tục 6.988 MB. Profile cần ít nhất 6.144 MB trước engine, reserve 2.300 MB sau engine. Không hạ resolution hoặc tự chuyển cloud.
- WhisperX alignment có adapter, chưa cài/chạy: default model tiếng Việt CC-BY-NC-4.0, registry ghi hạn chế. Câu/mốc thủ công có thể dùng.
- Nhánh ASR CUDA chưa kiểm chứng; core không tự sửa driver/CUDA toàn máy.
- Chưa đo render video dài, chưa kiểm chứng bằng video/SRT sản xuất của người dùng hoặc nghe/xem toàn bộ media tham chiếu.
- Burn-in phụ đề, footage video timestamp playback, audio mix/SFX/TTS replacement nâng cao và rig authoring tùy ý chưa có. Capability manifest không công bố các nhánh này.

## Bước tiếp theo sau bàn giao nền tảng

1. Dùng SRT/audio sản xuất thật khi người dùng cung cấp/chọn trong UI; agent lập plan theo nội dung, không dùng fixture làm AI template.
2. Chọn profile alignment có quyền dùng phù hợp hoặc dùng manual word anchors; chưa gọi nhánh default phi thương mại.
3. Kiểm chứng narration thật 45–60 giây và gu nhân vật theo phản hồi cụ thể. Clip hiện tại 48 giây là tone; speech worker test riêng 16,99 giây.
4. Các mở rộng đã ghi (mix/SFX/TTS splice, footage playback, burn-in, rig authoring tùy ý) chưa có; không đánh dấu sản phẩm đầy đủ P0–P7 đã hoàn tất.

Bản nền tảng 0.1 chạy được đã bàn giao với launcher, docs, output/backup và model registry thực. Core đang chạy localhost, không publish.

## Lỗi đã sửa có căn cứ

- pnpm 11 dùng allowBuilds cho esbuild; UI đã build.
- SDK preset Hải Đăng không tồn tại ở 3.7.1: fail trước inference, chọn đúng default Minh Quân từ roster pin; không sinh lại vì thẩm mỹ.
- PyAV 19 bỏ metadata_errors: pin 16.0.1, chỉ chạy lại nhánh decode/ASR bị lỗi; giữ TTS output.
- Progress ghi đè cancel_requested: cập nhật atomically, live cancel/resume đã qua.
- Guard RAM ảnh áp budget ban đầu hai lần: tách before/after-engine, không đổi chất lượng output.

Sandbox thường lỗi khởi tạo; shell cài/read/test được môi trường duyệt qua escalation. Không thay cấu hình bảo mật máy.

## Đưa mã nguồn lên GitHub — 15/10/2026

Theo yêu cầu trực tiếp: repo đích https://github.com/thaicongvinh2704/studiovideo.git, nhánh mặc định main; remote trống lúc kiểm tra.
Chuẩn bị source/lockfiles/specs và snapshot bằng chứng đã bỏ đường dẫn máy tại docs/evidence.
Không version env/model/data/reports hoặc cấu hình máy/session. Registry mẫu workers.example.json được dùng khi clone; setup không ghi đè cấu hình local đã có.
Không chạy lại ASR/TTS/sinh ảnh để đưa code lên Git.
