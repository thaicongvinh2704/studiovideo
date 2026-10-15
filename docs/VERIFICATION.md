# Kiểm chứng thực — 14/10/2026

| ID | Kết quả | Bằng chứng/phạm vi |
|---|---|---|
| V01 | Qua | UTF-8 BOM, tên file/thư mục Việt có khoảng trắng, source hash giữ nguyên, SRT lỗi nêu cue |
| V02 | Qua | Python + TypeScript: đầu/giữa/cuối logic 15 phút, 30/1 và 30000/1001; không render 15 phút |
| V03 | Qua | PNG frame 390 seek trực tiếp giống đánh giá tuần tự, cả renderer sau bổ sung rig parts |
| V04 | Qua | 3 spans phủ đúng [0,1440), dissolve không thêm frame; output ffprobe 1440 frames |
| V05 | Qua | Gain giữ video spans; trim giảm 1 giây và dịch câu phía sau, timeline stale |
| V06 | Qua | Idempotency, coalescing pending job; cancel thật sau checkpoint, resume cùng ID, hai attempts, ba cache spans |
| V07 | Qua | Hai mutation cùng revision: một thành công, một conflict; hai agent khác project cũng conflict |
| V08 | Qua trong phạm vi | Guard RAM/VRAM giả lập chặn trước load; policy TTS/missing model. Guard thật Comfy chặn khi RAM thiếu. Không thử gây GPU OOM thật |
| V09 | Qua kỹ thuật | MP4 H.264 NVENC 1920×1080, 30 fps, AAC 48k, 1440 frames; decoded marker ở 34/46s lệch khoảng 0.000042s < 1/30s |
| V10 | Qua | Backup checksum/restore/reopen; thay ảnh giữ source/keyframe và invalidate đúng span; ảnh local dùng chung được reuse ở project thứ hai |

Các test chỉ mở rộng để xử lý rủi ro thật được phát hiện: race cancel, cache key, lease toàn studio, thay asset. Không có vòng AI chấm chất lượng.

Worker thật: một TTS preset 16,99 giây, một ASR medium CPU trên chính audio đó, một SD 1.5 request 512×512 trên RTX 3050. TTS giọng không có trong roster và ASR decoder version không tương thích đã fail trước inference; sửa cấu hình/phụ thuộc, không tạo nhiều ứng viên vì gu. Các lần image job blocked do guard trước submit không sinh ảnh; chỉ có một provider_job_id đã cho kết quả.

Clip 48 giây là fixture audio tone + markers. Speech fixture 16,99 giây là kiểm chứng worker riêng. Chưa có clip tích hợp với narration thật 45–60 giây; không gọi clip tone là đã nghiệm thu tiếng Việt/lời nghe rõ hoặc đồng bộ từ ASR thật.

WhisperX vi chưa cài/chạy vì license default model phi thương mại; câu/manual word anchors là fallback có thật. Chưa đo hiệu năng video dài, chưa dùng SRT/audio sản xuất của người dùng, chưa nghe/xem toàn bộ media và chưa đánh giá gu. SDK MCP transport đã thử; client Codex/Antigravity chưa được kết nối trực tiếp.

Chi tiết máy/job/file: reports/*.json. Source fixture và outputs được giữ trong data/projects/. Không dùng số liệu GPU cloud.
