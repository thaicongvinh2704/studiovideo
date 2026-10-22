# Báo cáo nghiệm thu năng lực Antigravity (AG-001)

Ngày: 22/10/2026.
Người thực hiện: **Antigravity** (phiên làm việc trực tiếp trong client chính thức của người dùng).
Mục đích: Xác thực độc lập khả năng đọc repo, chạy công cụ/test, kiểm tra media và ảnh thật theo `coordination/ANTIGRAVITY_START.md`.

## 1. Bảng đánh giá năng lực thực tế

| Khả năng | Trạng thái | Bằng chứng thực tế |
|---|---|---|
| Hiểu repo & Quy chuẩn sản xuất | **VERIFIED** | Đã đọc `AGENTS.md`, `GEMINI.md`, `QUY_DINH_DAO_DIEN_HINH_ANH.md`, `projects/mo_den_maya/HANDOFF.md`. Hiểu rõ: nhân vật chính là Mỏ Đen (kho 24 PNG nguyên bản), giọng đọc cố định là custom H giọng Bắc 1.25x (chỉ áp dụng 1 lần), Maya V2 bị từ chối vì lặp đại cảnh trống, các bản demo diễn hoạt Mỏ Đen trước (V1 co kéo, V2 tay cứng) chưa được duyệt thẩm mỹ; kiểm tra kỹ thuật không suy ra QC thẩm mỹ hay QC nghe. |
| Môi trường Python & Thực thi lệnh | **VERIFIED** | Đã dùng interpreter `projects/angkor_wat_1min/.venv/Scripts/python.exe` (Python 3.12.10, PySide6 6.8.0, PIL 10.4.0, numpy 2.1.2, scipy 1.14.1). Thực thi thành công lệnh claim quyền qua `tools/agent_handoff.py`. |
| Chạy Unit Tests | **VERIFIED** | Chạy 4 bộ test bằng lệnh `python -X utf8 -m unittest discover ...` với `QT_QPA_PLATFORM=offscreen`. Tổng cộng 17/17 tests pass (7 test bàn giao, 4 test nhân vật supplied, 2 test media delivery, 4 test chuẩn hóa tiếng Việt), exit code 0. Không có failure/error/skip. |
| Kiểm tra Media (ffprobe) | **VERIFIED** | Dùng `C:\Users\ADMIN\ffmpeg\bin\ffprobe.exe` kiểm tra: `projects/mo_den_maya/assets/audio/narration.wav` (PCM s16le, 831.21s, 79.8MB, không phải LFS pointer) và `outputs/Mo_Den_Maya_Dao_Dien_Final_1080p.mp4` (H.264 1920x1080 24fps, AAC, 852.21s, 111.3MB, không phải LFS pointer). |
| Xem và đánh giá hình ảnh | **VERIFIED** | Sử dụng công cụ xem ảnh trực tiếp mở và quan sát: `outputs/mo_den_motion_demo_articulated_v3/contact_sheet.jpg` và `assets/characters/mo_den/library/named_24_v01/mo_den_01_neutral_seated_paws_resting.png`. Xác nhận ảnh Mỏ Đen 2048x2048 RGBA, lông kem/be, mặt nạ nâu, tai nâu, mắt xanh lơ, nét viền đen bo tròn, alpha sạch hoàn toàn. |
| Tạo giọng nói mới (Voice Synthesis) | **NOT_EVALUATED** | Chưa được người dùng yêu cầu tạo giọng mới trong lượt này; giữ nguyên tài sản audio giọng H 1.25x hiện có. |
| QC Nghe toàn bài (Listening QC) | **NOT_EVALUATED** | Chưa thực hiện nghe kiểm tra từng câu; metadata kỹ thuật không thay thế cho QC nghe của con người. |

## 2. Chi tiết kết quả Unit Tests

- `tests/test_agent_handoff.py`: 7/7 tests OK (0.099s).
- `tests/test_supplied_character.py`: 4/4 tests OK (0.069s).
- `tests/test_media_delivery.py`: 2/2 tests OK (1.273s).
- `tests/test_vietnamese_narration.py`: 4/4 tests OK (0.001s).

Tổng: 17/17 pass, 0 fail, 0 error.

## 3. Quan sát hình ảnh trực tiếp

- Ảnh `mo_den_01_neutral_seated_paws_resting.png`: Đúng nhận diện Mỏ Đen gốc (mèo Xiêm hoạt hình, lông be, mặt nạ mắt/mũi nâu sẫm, mắt xanh lam mí lờ đờ thư thái, hai chân trước đặt trước bụng, hai chân sau co phía dưới, đuôi vểnh sang phải). Không có artifact viền, alpha sạch.
- Contact sheet V3 (`contact_sheet.jpg`): Mỏ Đen ngồi tại chỗ ở tâm bệ tròn, nhép miệng theo khẩu hình thô, tay trước có cử chỉ nhẹ. Bản V3 tuy sửa khớp xương nhưng chưa thể hiện nhân vật hoạt hình tương tác và có hành động di chuyển trong không gian cảnh.
