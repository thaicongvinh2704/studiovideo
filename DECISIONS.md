# Quyết định

- 2026-10-14: Nhận đủ spec v1.0 và policy file 05 v2.0 từ ZIP, lưu nguyên bản tại docs/spec.
- Workspace ban đầu trống, không có repo hoặc code cần thay thế.
- Máy thật: Python 3.12.10, RTX 3050 6144 MiB, driver 610.88, FFmpeg 9.0.2, Edge local.
- Chẩn đoán ban đầu: RAM trống khoảng 2.2 GiB; không tải model nặng khi chưa đủ tài nguyên.
- Giữ FastAPI/Pydantic/SQLite, React/TypeScript/PixiJS 8 và MCP STDIO. Không dùng Sites.
- Mọi cài đặt ứng dụng nằm trong workspace. Không sửa driver, security hoặc config agent toàn máy.
- Fixture kỹ thuật có audio tổng hợp, không coi là kiểm chứng ASR hoặc chất lượng giọng tiếng Việt.
- Cài core .venv và env TTS/audio/comfy riêng; pin dependency sau kiểm chứng. Có lockfiles và model artifact manifests.
- ASR dùng medium CPU/INT8 để tránh sửa CUDA toàn máy; không đổi model sang small trong kiểm chứng đã chạy.
- Default WhisperX vi weights có license CC-BY-NC-4.0; giữ nhánh này chưa sẵn sàng cho sản xuất, hỗ trợ câu/manual word IDs theo spec fallback.
- TTS SDK có roster khác README mới: dùng đúng default Minh Quân của vieneu 3.7.1, babble_retries=0, offline local artifacts.
- ComfyUI riêng ở port 8189 để không chiếm server khác. Core sở hữu process, đóng sau job để release GPU. Một SD 1.5 checkpoint OpenRAIL-M, một workflow 512×512/12 steps/seed cố định cho kiểm chứng.
- Sửa cache job theo dependency, không toàn project revision. Lease một agent trên toàn studio, UI vẫn optimistic revision.
- Test thêm fiducial/cancel pause chỉ cho fixture kỹ thuật nhằm kiểm chứng drift và checkpoint; không dùng cho production.
- Chờ người dùng đóng app nặng trước image job; không tự kill app của người dùng hoặc retry OOM.
