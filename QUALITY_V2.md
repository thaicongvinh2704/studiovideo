# Bản tối ưu hình ảnh V2

Đã thay đổi mã nguồn, project demo và cấu hình xuất theo kế hoạch rà soát. Bản nguồn/project trước thay đổi nằm trong `backups/before_quality_v2.zip`; video 480p và project `examples/yellow_umbrella` giữ nguyên. Bản EXE trước thay đổi được build script giữ trong `dist/StickmanAnimationStudio_backup_*`.

## Kết quả bàn giao

- Project chỉnh sửa: `examples/yellow_umbrella_v2/project.json`, 12 cảnh, 36 cue và 36 WAV tiếng Việt.
- MP4: `outputs/quality_v2/yellow_umbrella_180s_1080p.mp4`, 1920×1080, 24 FPS, 180s, H.264/AAC.
- Đoạn thử: `outputs/quality_v2/quality_pilot_30s.mp4`.
- Bằng chứng: `outputs/quality_v2/story_contact_sheet.jpg`, các chuỗi frame và `decoded_*.png`, `final_probe.json`, `verification.json`.

## Thay đổi chính

1. Rig có vai, bốn tỷ lệ tuổi; bỏ cách co toàn bộ người về một đường khi turn. Mắt, biểu cảm, gaze và độ nghiêng mặt có điều khiển theo thời gian.
2. Chân trụ theo quãng đường X và IK, đồng bộ arm swing với quãng đường; clip walk dùng đúng action đang phát. Nhảy có lấy đà, bay, hạ và ổn định, không tự lặp liên tục.
3. Blend các clip và quá trình bật/tắt contact bằng góc khớp, giữ chiều dài tay. Có test kiểm tra mọi ranh giới motion trong demo không bật khớp tại timestamp chuyển.
4. Contact hai tay/khớp người khác hoặc điểm world có keyframe, giải quyết từ base pose chung để seek tùy ý vẫn deterministic. Trao ô ở local 3.2s cảnh 11 sau khi hai bàn tay gặp tại cùng điểm; sau đó con nâng/ nghiêng ô trong đoạn lời kể tương ứng.
5. Camera cùng biến đổi với nền/sàn/FX trong cảnh; shot toàn/trung/cận có editor và dùng chung hàm camera với Canvas.
6. Dàn cảnh có chủ thể lớn hơn, nền nhà/đường rõ hơn, insert tin nhắn/ảnh ô, phụ đề co theo nội dung bằng kích thước pixel, bỏ debug scene label khỏi export. Fade chỉ đặt ở mở đầu/kết phim.
7. Mưa nhiều lớp với vùng che đơn giản dưới ô; ripple giới hạn vào vũng nước. Bóng chân thay đổi khi nhảy.
8. Export Final 1080p/24 từ vector gốc, CRF 18/medium, BT.709; có các profile khác và tùy chọn supersample 2×. Render qua pipe, không chứa toàn phim trong RAM. Cache nhận biết phiên bản engine/font/profile và chỉ dựng lại cảnh thay đổi.
9. Studio mở demo V2 có giọng mặc định; thêm editor contact, shot, biểu cảm/tuổi, keyframe gaze/facing; nhân bản cảnh remap các reference mới.

## Kiểm tra và giới hạn

22 unit test đạt. EXE V2 đã build và chạy kiểm tra từ chính bundle: startup, Piper, save/load, export MP4 đều PASS (exit code 0); bằng chứng ở `outputs/quality_v2/frozen_check/runtime_check.json`. Kiểm tra tích hợp gồm save/load, startup/duplicate/undo, cache scene, cancel, supersampling và giải mã toàn bộ video. Thông số thời gian và bộ nhớ của probe renderer được lưu trong `verification.json`; không coi số đó là cam kết hiệu năng cho mọi máy hoặc peak RAM của toàn pipeline có FFmpeg.

Việc xem ảnh kiểm tra đã dẫn đến chỉnh lại bố cục, tư thế đứng, hướng gập tay và timing. Đây vẫn là diễn hoạt người que procedural/keyframe, không phải hoạt hình vẽ tay chuyên nghiệp hay mô phỏng va chạm toàn thân. Các tương tác ngoài tầm tay, di chuyển Y/scale/rotation phức tạp và dàn cảnh portrait cần biên tập riêng. Turn hiện đơn giản; chưa có bộ sprite nhiều góc nhìn. Chưa đổi model/diễn cảm giọng, chưa thêm lip sync.

Không coi kết quả test tự động là chứng nhận thẩm mỹ. Người dùng có thể đánh giá trực tiếp video mới và tiếp tục chỉnh nhịp/diễn xuất bằng project đi kèm.

## Chạy kiểm tra

```
python -X utf8 -m unittest discover -s tests -v
python -X utf8 tools/verify_extended.py
python -X utf8 tools/quality_review.py stills --prepare
python -X utf8 tools/quality_review.py pilot
python -X utf8 tools/quality_review.py full
python -X utf8 tools/verify_quality.py
```

`--prepare` tái tạo riêng demo V2 từ factory; không dùng tùy chọn đó trên project V2 đã chỉnh tay mà chưa lưu bản riêng. Không chạy lại `tools/verify.py --full` để đánh giá chất lượng V2: script đó lưu/xuất baseline trong thư mục demo cũ.
