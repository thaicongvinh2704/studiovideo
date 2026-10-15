# Hợp đồng đã triển khai

FastAPI OpenAPI tại localhost `/docs`; JSON Schema trong schemas/. Schema version nội dung 1.0; DB migration 2.

Mọi mutation metadata: expected_revision, actor (`ui` hoặc tên phiên agent có lease), change_reason, idempotency_key, lease_token cho agent, data. Source text không được dùng như shell hoặc chỉ dẫn điều khiển.

Plan: outline toàn bài + scene briefs có purpose, knowledge_before, reveal_rules, emotional_intent, visual_strategy, requirements. Scene khoảng sample nửa mở liên tục phủ audio. Node thời gian tuyệt đối trên audio master. Pose/attach phải nằm trong manifest. Event anchor đúng một word ID, utterance ID hoặc manual sample có evidence; audio_revision bắt buộc.

Transform x/y theo scene coordinates 1920×1080, rotation theo độ, scale vô hướng, opacity [0,1]. Keyframes dùng sample tuyệt đối; easing gắn key đầu khoảng. Camera riêng. Export đánh giá frame_index qua cùng SceneRenderer với preview, ticker dừng; textures/fonts sẵn. Event not_before lượng tử ceil, nearest round half-up; sample/frame không tích lũy float.

Job đọc snapshot cố định, trả ID ngay, cursor/progress/checkpoint qua SSE. Cancel không bị progress ghi đè. Resume cùng ID, không semantic revision mới. Output cũ giữ traceability nhưng finalize từ chối timeline/audio stale. ASR/TTS/asset cache theo audio/text/model/workflow/config dependencies; render span theo scene hai phía transition + assets/font/engine/profile.

MCP: 41 tools, có các nhóm capabilities, health, project, agent leases, audio/acceptance/manual anchor, plan, timeline, assets/patch/shared reuse, issues, TTS, jobs/detail objects, export, history và backup/restore. Job status mặc định gọn; transcript/workflow đầy đủ chỉ lấy khi yêu cầu. Asset patch V1 là thay raster image ở scene được chọn, không phải chỉnh tùy ý một phần ảnh bằng diffusion.

Audio replacement/mix nâng cao, video footage playback, burn-in và rig authoring tùy ý chưa có; manifest không công bố hỗ trợ. Clip narration thật 45–60 giây chưa nghiệm thu; xem docs/VERIFICATION.md.
