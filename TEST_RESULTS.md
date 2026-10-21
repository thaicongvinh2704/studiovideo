# Kiểm thử V4 — 19/10/2026

- Engine `ink-user-reference-4.4`: **44/44 unit tests PASS**, log `outputs/ink_v4/unit_tests.log`.
- UI native mở/phát, bảng pose/thư viện, nhân bản nhóm/lưu/đọc và seek bất kỳ đã chạy. Báo cáo `outputs/ink_v4/verification_v4.json` ghi số frame preview thực tế, không dùng làm cam kết 30 FPS trên mọi máy.
- Pilot 87,4 giây, 2.622 frame ở 1080p/30; clip ba chuyển động 24 giây, 720 frame; thử 4K 2 giây, 60 frame. Đã giải mã toàn file.
- Đo độ trượt trên bàn chân của skeleton đã giải IK, thay cho chỉ đo target mong muốn; sai số dưới 0,001 design pixel trong khoảng chân trụ được kiểm tra. Kiểm tra độ dài tay và hand contact cũng đạt.
- `outputs/ink_v4/release_verification.json` ghi kết quả gói EXE/media sau khi thực chạy. `long_verification.json` ghi riêng engine của bài tải dài; không đồng nhất một bài tải cũ với phiên bản hiện tại.
- Tạo hình mới bám ảnh áo đen do người dùng gửi. **Chưa coi mỹ thuật đã được người dùng duyệt**; kiểm thử kỹ thuật không xác nhận mức giống video tham chiếu. Phạm vi còn thiếu được ghi tại `INK_V4.md`.

---

# Kiểm thử Video minh họa V3 — 18/10/2026

- **33/33 unit tests PASS**; log: `outputs/explainer_v3/unit_tests.log`.
- Native UI: biên tập storyboard, chữ, kéo nhóm, cắt lớp, undo, nhân bản/đổi cảnh kèm voice/SRT; playback theo đồng hồ thực đã chạy.
- Thành phẩm mới: **68,6 giây, 1920×1080, 30 FPS, đúng 2.058 frame**, H.264/AAC, audio stereo 48 kHz. Đã giải mã toàn file và kiểm tra các frame trích ra.
- 4K: đoạn thật **3840×2160, 30 FPS, 2 giây, 60 frame**, xuất và ffprobe thành công.
- Bài tải dài: **1.303,4 giây, 21:43,4, 1080p/30 FPS, 39.102 frame**. Dùng 19 lần bộ 8 cảnh, 152 cảnh tổng cộng; đã render và giải mã toàn file. Đây là bài tải lặp, không phải tác phẩm mới dài 21 phút.
- Đồng bộ: 8 tín hiệu âm thanh qua các điểm cắt không trùng frame; stereo tách kênh đúng; nhịp timestamp video đều. Đối chiếu audio đầu/giữa/cuối bài tải dài với voice nguồn bằng tương quan tín hiệu; sai lệch dưới 15 ms.
- Bản **EXE frozen PASS, exit 0**: startup, Piper Việt, save/load, SVG trong project mặc định, FFmpeg export. CLI frozen đã biên dịch storyboard thành 8 cảnh và xác nhận có mã pose mới.
- CLI source đã tạo project portable từ storyboard. Source ZIP phải được đối chiếu sau đóng gói bằng bản nguồn hiện tại.
- Bằng chứng và số đo chi tiết ở `outputs/explainer_v3/verification.json`; screenshot native/frozen, contact sheet và decoded frames cùng thư mục. Thời gian render có thể dùng lại scene cache, không dùng các số này làm cam kết tốc độ cho máy khác.
- Các kiểm tra kỹ thuật không thay thế đánh giá mỹ thuật. Chưa có nhận dạng voice/forced alignment hoặc sinh mọi minh họa từ kịch bản; TXT chia thời gian ước lượng, cần căn theo voice/SRT và biên tập.

---

Các kết quả V2 dưới đây được giữ làm lịch sử của bản cũ.

# Kiểm thử bản tối ưu V2 — 13/10/2026

- `python -X utf8 -m unittest discover -s tests -v`: **22/22 PASS**, gồm 10 bài nền tảng và 12 bài chất lượng mới. Các test mới kiểm tra chân trụ, clip walk với action gốc idle, tiếp xúc/đổi người cầm, ôm, nhảy một lần, ranh giới motion không bật khớp, seek không phụ thuộc lịch sử, tỷ lệ tuổi, camera/sàn qua pixel, cache và dialog.
- `tools/verify_quality.py`: kiểm tra save/load portable, startup, nhân bản cảnh/remap contact/undo, cancel giữ output cũ, cache chỉ render lại cảnh thay đổi, supersampling, full decode MP4 180s/1080p/24 FPS/4.320 frame có AAC. Kết quả cụ thể ở `outputs/quality_v2/verification.json`.
- `tools/verify_extended.py`: clip 720p/24, 1080p/30, portrait/12, nối/cache cảnh và mixer ducking: đã chạy lại đạt.
- `tools/quality_review.py`: tạo project riêng có đủ 36 WAV cũ, ảnh đối chiếu 12 cảnh, pilot 30s và phim 180s. Bản cũ/project cũ giữ nguyên.
- Kiểm tra thị giác thực hiện trên contact sheet, chuỗi frame chuyển động và frame giải mã từ MP4. Chưa có đánh giá nghệ thuật độc lập hoặc xác nhận từ người dùng; không dùng test PASS thay cho việc đánh giá cảm xúc/chất lượng diễn xuất.
- Giới hạn: hình vẫn là vector người que procedural; contact không phải physics va chạm toàn thân, portrait chưa có dàn cảnh riêng, chưa render bài tải 15 phút hoặc thử máy Windows khác.

- EXE V2 đã build và chạy `--runtime-check`: **PASS, exit code 0, frozen=true**. Startup, Piper tiếng Việt, save/load và FFmpeg export từ bundle đã thực thi. Bằng chứng: `outputs/quality_v2/frozen_check/runtime_check.json`. Đã đối chiếu 29 file Python trong source ZIP với source và kiểm tra 36 WAV trong demo đóng gói.
- Phim cuối 180s/1080p24 xuất trong khoảng 85 giây trên máy hiện tại. Probe renderer 300 frame đạt khoảng 5,24 giây, peak working set của tiến trình probe khoảng 152 MB; không phải peak RAM của mọi tiến trình render/FFmpeg và không suy diễn cho máy yếu khác.

Phần dưới là kết quả lưu trữ của bản đầu, không phải thông số video V2.

---

# Kết quả kiểm thử thực tế

Ngày kiểm thử: **13/10/2026**, Windows 11 x64, Python 3.12.14, PySide6 6.10.2, Piper 1.8.0, FFmpeg 8.1.1. Dùng CPU, không CUDA và không API trả phí.

## Đã thực thi

`python -X utf8 -m unittest discover -s tests -v`: **10/10 unit test PASS**. Bao gồm SRT BOM/đa dòng/timestamp sai, interpolation/Bezier, FK/IK và chiều dài xương, 20 action, blend, bám tay/trao ô, lưu/mở/package và timeline 18 phút.

`python -X utf8 tools/verify.py --full`: **12/12 bài kiểm thử yêu cầu PASS**, thêm kiểm tra cancel giữ nguyên output cũ. Bằng chứng máy đọc được trong `outputs/verification.json` và log ở `outputs/verification-log.txt`.

| Test | Kết quả và phạm vi thực tế |
|---|---|
| 1. Khởi động | Cửa sổ native hiện lên, canvas có frame thật |
| 2. Save/Open | Lưu JSON và mở lại giữ 12 cảnh, 36 cue |
| 3. Đi bộ | Khớp gối và tay đổi vị trí theo timestamp; chiều dài xương kiểm tra bằng unit test |
| 4. SRT | Đọc 36 cue UTF-8 BOM; ranh giới 5s hiện đúng cue |
| 5. Chỉnh sửa | Đổi action/X, keyframe, Undo; kéo nhân vật bằng QtTest; resize clip 15→14s rồi kéo clip 0→1s |
| 6. Background | Import PNG qua luồng UI và kiểm tra pixel của frame render |
| 7. Voice | Piper sinh WAV tiếng Việt thật; Qt player chạy qua timestamp >0, không có lỗi media |
| 8. Cảnh + giọng | 36 WAV được lưu dưới assets và đặt lên timeline; các dialog editor khởi tạo thành công |
| 9. MP4 | Pipe frame vector thật qua FFmpeg, không giữ toàn bộ frame trong RAM |
| 10. Media | ffprobe kiểm tra H.264/AAC, 854×480, 12 FPS; MP4 phát được bằng Qt video player |
| 11. Cảnh đầu | Xuất `first_scene_15s.mp4`, thời lượng 15.000s |
| 12. Demo | Lưu/mở lại và render đủ 12 cảnh, `yellow_umbrella_180s.mp4`, 180.000s |

Kiểm tra bổ sung `python -X utf8 tools/verify_extended.py`:

- 1280×720 / 24 FPS / 1 giây: PASS.
- 1920×1080 / 30 FPS / 0.5 giây: PASS.
- 480×854 / 12 FPS / 1 giây: PASS.
- Cache 2 cảnh: render, nối MP4, xuất lại và kiểm tra mtime của cả hai scene không đổi: PASS.
- Mixer giọng + nhạc + SFX, delay/trim/fades, bật/tắt ducking, output WAV đúng 4s: PASS.

Test mixer phát hiện một trường hợp `apad` không giới hạn có thể ghi WAV tạm rất dài với SFX ngắn bị delay. Đã sửa bằng padding có giới hạn, chặn theo số mẫu, chuẩn hóa timestamp và đặt `-t` cho các bước audio. Tác vụ lỗi đã dừng, tệp tạm do test tạo đã dọn; bài mixer đã chạy lại đạt.

Screenshot thật ở `outputs/studio_1366x768.png` và `outputs/studio_1920x1080.png`. Timeline có cuộn dọc và splitter để xem các track phía dưới trên màn hình nhỏ. Frame ví dụ ở `outputs/demo_frame.png`.

## Build Windows

PyInstaller đã thực thi trên Windows và tạo thành công `dist/StickmanAnimationStudio/StickmanAnimationStudio.exe`. Log build: `build/build-final.log`. Runtime đi kèm model/config tiếng Việt, demo có giọng, FFmpeg/ffprobe, Qt DLL và notices.

Bài kiểm tra từ chính EXE dùng lệnh:

```bat
dist\StickmanAnimationStudio\StickmanAnimationStudio.exe --runtime-check outputs\frozen_check
```

**Đã chạy từ chính EXE cuối cùng: PASS, exit code 0, `frozen: true`.** Kết quả và bằng chứng riêng nằm trong `outputs/frozen_check_final/runtime_check.json`. Bài này chạy startup, voice Piper, save/load, xuất MP4 2s ở 320×180/12 FPS và kiểm tra ffprobe từ bundle.

Lần build đầu gặp lỗi import QtCore do PyInstaller tìm nhầm `icuuc.dll` từ Poppler trên PATH. Đã xác định nguồn DLL trong Analysis TOC, loại DLL đó để Qt sử dụng ICU native của Windows, và giữ bộ MSVC DLL đồng bộ. Spec/build script đã có sửa lỗi này. Bản EXE bàn giao sau sửa đã chạy được cả giọng tiếng Việt và xuất video.

## Chưa kiểm thử hoặc còn giới hạn

- Chưa chạy video đầy đủ 15 phút; đã kiểm tra dữ liệu timeline 18 phút và render demo 3 phút. Chưa chạy cả demo ở 720p/1080p, chỉ xuất clip ngắn ở các mức đó.
- Kiểm tra phát WAV/MP4 là kiểm tra media load/playback bằng Qt; ngữ điệu giọng đọc vẫn cần người dùng nghe và biên tập theo ý muốn.
- Chưa thử trên máy Windows khác, Windows 10, CPU rất cũ hay môi trường không có Segoe UI. Không suy diễn từ máy hiện tại sang mọi cấu hình.
- Foot lock chưa tuyệt đối; hug không tự ràng buộc hai nhân vật; preset là animation procedural đơn giản. Portrait hiện fit cảnh ngang giữ tỷ lệ. Một model voice, chưa có bốn voice tự nhiên riêng.

Hướng dẫn sử dụng và danh sách giới hạn đầy đủ trong `README_VI.md`. Đây là bản Studio hoạt động end-to-end; không khẳng định mọi khả năng nâng cao đã hoàn thiện.
