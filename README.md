# Story Motion Studio Local

Ứng dụng Windows chạy tại localhost, UI tiếng Việt. Nhận SRT/audio, để một agent bên ngoài lập kế hoạch qua MCP, chỉnh cảnh/layer/keyframe và xuất MP4 H.264 + SRT. Không có LLM nhúng hoặc API AI trả phí.

## Cài từ GitHub

Clone repository, cài Python 3.12, Node.js 22+ và pnpm 11; FFmpeg/ffprobe cần có trong PATH, Microsoft Edge dùng cho export. Chạy `SETUP_STUDIO.cmd`, sau đó `START_STUDIO.cmd`.

Setup tạo `config/workers.json` từ `config/workers.example.json` nếu chưa có, và sinh cấu hình MCP theo đường dẫn checkout thực. Mỗi máy cài model riêng bằng các script đã mô tả bên dưới. File mẫu luôn ghi model chưa cài; không mang trạng thái đã kiểm chứng của máy phát triển sang máy mới.

Git chỉ chứa mã nguồn, lockfiles, đặc tả và bằng chứng đã bỏ đường dẫn máy tại `docs/evidence/`. Môi trường Python/Node, model, dữ liệu/video dự án, session/token và cấu hình riêng của máy được giữ local, không tải lên repository. Xem ảnh giao diện tại [docs/evidence/studio-ui.png](docs/evidence/studio-ui.png).

## Chạy trên máy này

1. Mở `START_STUDIO.cmd`. Core chạy ẩn, trình duyệt mở studio tại `http://127.0.0.1:8765` với session local.
2. Chọn dự án hoặc tạo mới. Tab **Audio & phụ đề** nhập audio + SRT UTF-8.
3. Kết nối agent để lập outline và scene briefs. Tab **Biên tập** cũng cho nhập plan có sẵn ở phần nâng cao; schema tại `schemas/`.
4. Kiểm tra → chốt kế hoạch → tạo timeline. Tab **Timeline** dùng audio master để phát/seek.
5. **Xuất MP4 + SRT** trả job ID ngay. Theo dõi/hủy/tiếp tục trong **Hàng đợi**. Sau thành công, chọn **Ghi nhận bản xuất** để xác nhận đúng timeline/audio hiện tại.
6. `STOP_STUDIO.cmd` dừng đúng core của workspace. Job đang chạy giữ checkpoint, hiện interrupted khi mở lại; chọn tiếp tục.

Nếu chưa có env/build: `SETUP_STUDIO.cmd`. Core dùng `.venv`, các model có env riêng trong `.envs/`. Runtime Node/pnpm thực của máy được ghi tại `config/runtime-paths.json`; có thể cập nhật khi chuyển máy. Không cần Docker/Redis/Electron.

## Agent

Chạy studio trước. Cấu hình mẫu tuyệt đối được tạo bằng `scripts/client_configs.py`:

- Codex: thêm nội dung `config/codex.toml` vào cấu hình MCP của client. Không tự sửa cấu hình tài khoản toàn máy.
- Antigravity: thêm server từ `config/antigravity.json` vào cấu hình MCP của client.

Bridge STDIO gọi HTTP core chung với UI, log stderr, không tải/spawn model khi agent kết nối. Chỉ một phiên agent được giữ lease trên studio; mutation dùng expected_revision, actor, change_reason và idempotency_key. Agent lấy `agent_acquire`, dùng tên phiên/lease token rồi `agent_release` khi đổi client. UI vẫn dùng revision để tránh ghi đè.

Nguồn cấu hình đã đọc: [Codex MCP](https://learn.chatgpt.com/docs/extend/mcp?surface=cli), [Antigravity MCP](https://www.antigravity.google/docs/mcp), [Python MCP SDK](https://github.com/modelcontextprotocol/python-sdk). Đã thử bằng SDK MCP ClientSession thật (41 tools); chưa kết nối từ ứng dụng Codex/Antigravity của người dùng.

## Chỉnh một cảnh và tiếp tục

Chọn cảnh trong **Biên tập**, sửa mục đích, điều đã biết, tiết lộ/cảm xúc hoặc node/keyframe, rồi lưu. Chốt và compile lại. Hash span phụ thuộc cảnh/transition/asset/font/profile; các span không đổi được dùng lại. Source, audio và tài nguyên còn dùng được được giữ. Hoàn tác/làm lại ở editor tạo revision mới.

Gain tạo audio revision và mix mới, giữ video spans. Trim có quyền riêng, làm timing downstream stale; phải xử lý lại câu/anchor/scene bị ảnh hưởng trước render. Mốc SRT ban đầu chỉ là mốc chưa xác minh. Căn từ không có timestamp thì giữ unresolved; có công cụ mốc từ thủ công với word ID và bằng chứng.

## Model

Registry: `config/workers.json`, artifact manifests và hash trong `data/models/`. Chẩn đoán không tải model. Mọi worker subprocess thoát sau job; hàng đợi nặng chạy tuần tự. Không tự chuyển cloud, hạ resolution hoặc sinh lại vì thẩm mỹ.

- VieNeu Turbo 3.7.1 CPU/ONNX fp32, preset roster pin theo SDK, không voice cloning trong bản này. TTS chỉ chạy khi project cho phép và không tự thay audio gốc. Giấy phép artifact/preset đã đối chiếu từ [model card](https://huggingface.co/pnnbao-ump/VieNeu-TTS-v3-Turbo).
- Whisper medium CPU INT8, faster-whisper 1.2.1, PyAV 16.0.1. Nhánh CUDA chưa kiểm chứng trên máy này. [Nguồn](https://github.com/SYSTRAN/faster-whisper).
- WhisperX adapter alignment có code, không chạy ASR lần hai. Default Vietnamese weights hiện [CC-BY-NC-4.0](https://huggingface.co/nguyenvulebinh/wav2vec2-base-vi-vlsp2020), chưa bật cho sản xuất; dùng câu/mốc thủ công. Không coi adapter là worker đã nghiệm thu.
- ComfyUI + một SD 1.5 profile 512px. Checkpoint [OpenRAIL-M](https://huggingface.co/stable-diffusion-v1-5/stable-diffusion-v1-5) có điều kiện sử dụng. Không tự tải LoRA/ControlNet/SDXL. Trạng thái thực và evidence xem `PROGRESS.md`.

`scripts/install_models.py tts` hoặc `asr` chỉ inspect dung lượng/artifact. `--install` cài/tải profile đã kiểm tra license, pin revision/hash, không thử nhiều model. `scripts/install_comfy.py` cài env GPU riêng + một checkpoint; không sửa driver.

## Dữ liệu và bằng chứng

- Đặc tả gốc đủ sáu file: `docs/spec/`.
- `data/studio.sqlite`: core sở hữu trạng thái; manifest là snapshot. Migration v1→v2 có backup SQLite trước thay đổi.
- `data/projects/<id>/`: source bất biến, working, plans, assets, cache, exports, reports.
- Backup xuất ZIP chứa manifest, checksums và source/working/assets cần thiết. Restore qua service, không tin đường dẫn trong ZIP, tạo project ID mới. Model lớn chỉ registry chung.
- `reports/`: kết quả nền tảng, ảnh UI/seek, MCP, cancel/resume và drift sau decode, speech verification. Các fixture ghi rõ dữ liệu tổng hợp.
- `docs/evidence/`: snapshot kiểm chứng của máy phát triển để đọc từ GitHub; không phải kết quả mới chạy khi clone.

Không xác nhận chất lượng ngang video tham chiếu, nội dung chính xác tuyệt đối hoặc đã nghe/xem toàn video. Chưa đo hiệu năng video dài. Các khả năng motion công bố đúng manifest: transform, reveal, pose/expression, point/look, hand attachment, camera và cut/dissolve. Chưa có arbitrary animation, IK, lip-sync, video asset playback hoặc burn-in SRT.
