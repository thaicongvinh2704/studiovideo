# Studio · Video minh họa V3

Bản ngày 18/10/2026 mở rộng Studio để dựng video giải thích trên nền trắng: người dẫn minh họa, ảnh/SVG, chữ, sơ đồ, bố cục theo lời đọc và xuất MP4. Cài đặt xong vẫn hoạt động offline bằng CPU. Không dùng dịch vụ AI tạo video hoặc credit.

## Mở và xem thành phẩm

Chạy `start_studio.bat`. Bản đóng gói mở `examples/explainer_showcase/project.json` khi có, nếu không mới dùng demo chiếc ô cũ. Cả hai demo vẫn chỉnh sửa được. Video mới ở `outputs/explainer_v3/history_explainer_1080p.mp4`, dài 68,6 giây, 8 cảnh, 1080p/30 FPS. Kịch bản minh họa mới là “Những mảnh ghép lịch sử”; không dùng lại khung hình của video tham chiếu để giả làm thành phẩm mới.

Trong thư mục EXE cũng có `examples/explainer_showcase/showcase.mp4` để xem bản mẫu và `verification_v3` chứa bằng chứng kiểm tra gọn. Khi chép ứng dụng sang máy khác, chép cả thư mục `dist/StickmanAnimationStudio`.

## Quy trình với file của bạn

1. Bấm **Kịch bản + voice…** trên hàng công cụ thứ hai.
2. Chọn voice WAV/MP3/M4A/FLAC/OGG/Opus; dán hoặc mở kịch bản TXT/SRT. Chọn thư mục ảnh PNG/JPG/WEBP/SVG nếu có.
3. Bấm **Tạo bảng phân cảnh**. Với SRT, Studio dùng mốc của SRT. Với TXT, thời gian được ước lượng theo số từ và độ dài voice, có thông báo rõ. Đây chưa phải nhận dạng giọng nói hoặc tự căn câu chính xác.
4. Trong bảng, chỉnh đầu/cuối, tiêu đề, bố cục, pose, file hình và nhãn. Các cảnh cần liên tục, bắt đầu từ 0 và kết thúc không vượt voice. Ghép ảnh theo tên file chỉ là gợi ý. Tự chọn hình nếu tên file không nói lên nội dung.
5. Chọn **Tạo project chỉnh sửa được**, chọn nơi lưu. Studio chép voice và hình vào `assets` cạnh project; waveform voice được phân tích trong tác vụ nền.
6. Xem/nghe lại. Chọn cảnh bên trái; sửa từng chữ/hình bằng **Sửa nội dung…**; kéo trên canvas hoặc đặt keyframe. Căn các mốc với voice và waveform trước khi xuất.
7. Bấm **Xuất MP4**: 1080p/30 FPS hoặc 4K/30 FPS. Bật lưu từng cảnh để tiếp tục khi hủy. Render cuối trộn audio một lần, tránh tích lũy độ trễ AAC ở mỗi cảnh.

Nếu bạn đưa kịch bản, voice và tài nguyên cho Codex, Codex có thể biên tập storyboard JSON, tạo project và render qua cùng engine. Studio cung cấp công cụ dựng; khả năng chọn nội dung, vẽ một minh họa đặc thù và dàn dựng thẩm mỹ vẫn cần biên tập. Bản offline này không tự hiểu mọi hình ảnh hoặc sinh mọi minh họa từ văn bản.

## Công cụ mới

- **Người dẫn:** nhân vật có áo/quần/tay/mặt, dùng rig thật. **Tư thế…** có 12 lựa chọn gồm giới thiệu, chỉ trái/phải, giải thích, suy nghĩ, thắc mắc, ngạc nhiên, cầm vật, vui mừng, nghỉ, ngồi và đi. Pose tay nội suy khi đặt sau thời điểm 0. Đi bộ vẫn là động tác procedural; cần kiểm tra khi có đường đi và tiếp xúc đặc thù.
- **Chữ:** nhập nội dung độc lập với phụ đề; phông chữ, màu, đậm, căn trái/giữa, kích thước vùng. Chữ tự giảm cỡ nếu vùng quá chật; nên rút gọn câu và tăng vùng để giữ dễ đọc.
- **Hình / mũi tên:** card, callout, ellipse, line, arrow, check, cross và path. Path nhận danh sách tọa độ để tạo sơ đồ riêng.
- **Ảnh:** nhập SVG hoặc ảnh raster; chọn contain/cover, vùng crop chuẩn hóa 0–1, thay ảnh. Ảnh raster nhỏ vẫn mờ khi phóng lớn; supersampling không bổ sung chi tiết gốc. SVG nhập được raster hóa tối đa 2048 px để giữ preview nhẹ.
- **Bố cục…:** người dẫn + bảng, hai hình so sánh, timeline, các bước/nguyên nhân, gallery, câu hỏi/kết luận, pan ảnh và các lớp tự bố trí. Bố cục tạo các đối tượng độc lập có thể sửa, không phải ảnh phẳng đóng kín.
- **Nhóm…:** chọn nhiều lớp để kéo cùng nhau. Đây là nhóm dịch chuyển vị trí, chưa phải hệ cha-con với pivot xoay/scale đầy đủ.
- **Nhân bản lớp / Cắt lớp:** giữ dữ liệu animation trên thời gian cục bộ của cảnh.
- **Waveform:** phân tích voice và vẽ sóng trên timeline. Cuộn dọc xuống track giọng đọc để xem. **← / →** bước một frame; snap clip theo FPS dự án.
- **Nền trắng:** trắng phẳng, không sàn. Project cũ dùng nền “studio” vẫn giữ nền cũ.

Các cảnh mới từ storyboard có voice/SRT gắn `scene_id`, nên khi đổi thứ tự, nhân bản hoặc xóa cảnh bằng giao diện, lời và phụ đề đi cùng cảnh. Khi rút ngắn cảnh, clip lời và phụ đề thuộc cảnh được cắt theo cảnh; tăng lại thời lượng không tự khôi phục phần đã cắt. Project cũ không có `scene_id` vẫn giữ audio/SRT theo thời gian tuyệt đối để tránh đổi dữ liệu ngầm. Dùng Undo nếu đổi nhầm thời lượng.

## Bộ file đầu vào thuận tiện

```text
my_video/
  script.txt         hoặc narration.srt
  narration.wav     voice hoàn chỉnh
  images/
    ban_do.png
    hien_vat.jpg
    van_ban.svg
  storyboard.json   tùy chọn, mô tả dựng chi tiết
```

Đặt tên ảnh có nghĩa giúp gợi ý ban đầu tốt hơn. SRT với mốc đã căn voice giúp dựng chính xác hơn TXT. Nếu nội dung cần ảnh cụ thể, cần có file ảnh đó hoặc biên tập asset mới; Studio không tự tải tư liệu trên mạng.

## Storyboard cho biên tập bằng Codex

Mỗi `row` là một cảnh. `start/end` là giây toàn video; `cue_start/cue_end` tùy chọn giữ phạm vi phụ đề nếu có khoảng lặng. `assets` và `voice` có thể là đường dẫn tương đối với file storyboard; loader chuyển thành đường dẫn đầy đủ trước khi biên dịch.

```json
{
  "version": 1,
  "name": "Video của tôi",
  "voice": "narration.wav",
  "timing": "manual",
  "rows": [
    {
      "start": 0,
      "end": 8,
      "title": "Hai nguồn tư liệu",
      "text": "Nội dung lời đọc trong cảnh này.",
      "layout": "compare",
      "pose": "point",
      "assets": ["images/hien_vat.jpg", "images/van_ban.svg"],
      "labels": ["Hiện vật", "Văn bản"]
    }
  ]
}
```

`layout` nhận `presenter`, `compare`, `timeline`, `process`, `gallery`, `quote`, `pan`, `custom`. `custom` bắt đầu với tiêu đề; `objects` cho phép đặt thêm text/shape/image/character bằng dữ liệu project, có keyframes riêng. `camera` nhận x/y/zoom và keys giống camera Studio. Đối tượng thêm có `start/end` tính bằng giây cục bộ của cảnh; nếu bỏ end sẽ kéo dài đến hết cảnh. Có thể trộn preset layout và lớp bổ sung. Tất cả vẫn mở được trong UI.

Chạy từ thư mục source trong workspace này:

```powershell
& '..\.venv\Scripts\python.exe' main.py --storyboard 'my_video\storyboard.json' --save-project 'my_video\edit\project.json' --render 'my_video\final.mp4' --resolution 1080p
```

Hoặc render project đã chỉnh:

```powershell
& '..\.venv\Scripts\python.exe' main.py 'my_video\edit\project.json' --render 'my_video\final.mp4' --resolution 4k
```

Bản EXE nhận cùng tham số; khi chạy GUI không cần Python. MP4 nằm ở đường dẫn đã chỉ định. Nếu EXE lỗi, xem `launch-error.log`.

## Kiểm chứng và giới hạn

Kiểm thử ở `tests/test_explainer.py` bao phủ thời gian SRT/TXT, các layout, hình contain/cover, SVG và assets đóng gói, cảnh đi cùng lời, pose liên tục, custom layer/camera, biên tập storyboard. `tools/verify_explainer.py` kiểm tra thao tác native UI, playback, tín hiệu stereo qua điểm cắt, export/giải mã mẫu 1080p và đoạn 4K. `--long` tạo bài tải 19 lần bộ 8 cảnh, dài 1.303,4 giây (21 phút 43,4 giây); đây là bài tải lặp cảnh, không phải tác phẩm mới dài 21 phút.

Kết quả thực thi ở `outputs/explainer_v3/verification.json` và `unit_tests.log`; chỉ mục nào có kết quả mới được coi là đã chạy. Khung hình giải mã từ MP4 ở `decoded_*.png`; bảng cảnh ở `showcase_contact_sheet.jpg`. Chất lượng mỹ thuật cần xem video thật và đối chiếu mục tiêu; số kiểm thử PASS không tự chứng minh mọi kịch bản sẽ đẹp như mẫu.

Chưa có nhận dạng voice/forced alignment, lip sync, sinh minh họa từ văn bản, biên tập video footage, pivot nhóm đầy đủ hoặc công cụ vẽ tự do như phần mềm đồ họa chuyên dụng. Tự động ban đầu là chia mốc/ghép tên file; dàn dựng cuối có thể do người dùng hoặc Codex biên tập.
