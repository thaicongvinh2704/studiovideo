# Studio V4 · Video minh họa theo lời

Bản triển khai ngày 19/10/2026. Mở `start_studio.bat` hoặc EXE trong `dist/StickmanAnimationStudio`. Studio mở dự án `examples/ink_showcase/project.json` khi có. Đây là video mới dài 87,4 giây về một thành phố tưởng tượng, không dùng khung hình từ video tham chiếu.

## Những phần đã thay đổi

- Người dẫn mới dạng vector: tóc đen vuốt dựng, mặt góc 3/4, áo thun đen có dấu cộng trắng, quần xanh và giày trắng, theo ảnh người dùng gửi ngày 19/10. Pose chỉ tay có tay còn lại chống hông. Tất cả bộ phận dùng khớp được đánh giá cùng renderer preview/export; không phải chiếu một ảnh người đứng yên. Ảnh tham chiếu được giữ trong `assets/characters/reference`.
- Bảng tư thế có 20 lựa chọn bằng hình; 8 trạng thái khuôn mặt; màu áo/quần/da/nét/giày sửa bằng **Diện mạo…**. Một số tư thế cố ý giữ hình; đi bộ và chuyển tư thế có diễn hoạt. Đây là hình mặt trước với nghiêng mặt, chưa phải bộ nhân vật nhiều góc nhìn hoàn chỉnh.
- 42 SVG gốc trong `assets/ink`, có tên, tag và catalog. **Thư viện hình…** tìm và chèn được ảnh. Cần hình đặc thù của kịch bản thì vẫn phải cung cấp/chuẩn bị riêng. Không coi 42 biểu tượng là thư viện đủ cho mọi chủ đề.
- SVG có fit/cover/crop được render vector trực tiếp ở độ phân giải đầu ra, không giới hạn vào raster 2048 px của đường nhập cũ.
- Bố cục cận cảnh, người dẫn, so sánh, timeline, các bước, bản đồ, gallery, cảnh rộng và nhóm người. `style: "ink"` trong storyboard chọn cách dựng mới; `show_title` tùy chọn; `reveal_times` đặt mốc xuất hiện từng hình. Chữ và hình vẫn là các lớp độc lập.
- `gestures` đặt pose/t/blend, có curve lấy đà nhẹ và dừng mềm, cẳng tay đi sau vai. Hand contact/attachment dùng điểm khớp thật; hỗ trợ lớp hình cầm trong tay và vẽ bàn tay phía trước.
- **Nhóm…** tạo lớp cha thật để di chuyển/xoay/scale. **Cha / điểm xoay…** đổi quan hệ và pivot. Đổi cha bake các biến đổi trên lưới FPS để giữ chuyển động tại từng frame. Bỏ contact trước khi đổi cha của nhân vật. Không xóa/cắt riêng cha đang có con; bỏ quan hệ cha trước hoặc thao tác trên cả cảnh.
- Keyframe editor giữ tham số Bezier, cho sửa bốn điểm điều khiển và bảo toàn dữ liệu frame khi lưu. Chưa có đồ thị curve kéo tay/onion skin.
- Tái sử dụng một khung hình giữ nguyên; thay pose, blink, camera, biểu cảm, nội dung, thời gian xuất hiện hoặc file hình sẽ làm mới cache. Chỉ giữ một frame hoàn chỉnh; cache raster và SVG có giới hạn.

## Đưa kịch bản, voice và hình vào

1. Bấm **Kịch bản + voice…**, chọn audio và TXT/SRT; chọn thư mục hình. Tạo bảng phân cảnh chạy ở tác vụ nền.
2. SRT giữ các mốc gốc. TXT dùng phân bổ theo từ; tùy chọn khoảng nghỉ chỉ gợi ý thời gian gần khoảng im lặng. Đây chưa phải nhận dạng giọng nói/forced alignment.
3. Bố cục và hình được gợi ý bằng quy tắc từ khóa, không phải AI hiểu tư liệu. Bảng báo rõ cảnh thiếu minh họa. Kiểm tra từng cảnh, chọn đúng hình, đặt nhãn ngắn và pose.
4. Tạo project, căn mốc trên waveform, đặt thời gian từng lớp và keyframe. Những chỗ cần hình mới phải chuẩn bị asset trước khi xuất bản cuối.
5. Xuất 1080p/30 hoặc 4K/30. Bản final từ chối placeholder/thiếu file. CLI chỉ cho phép chúng khi chủ động dùng `--allow-draft`.

Ví dụ chuẩn bị project từ đầu vào:

```powershell
& '..\.venv\Scripts\python.exe' main.py --script 'input\narration.srt' --voice 'input\voice.wav' --assets-dir 'input\images' --save-project 'output\edit\project.json'
```

Ví dụ dựng storyboard đã biên tập:

```powershell
& '..\.venv\Scripts\python.exe' main.py --storyboard 'input\storyboard.json' --save-project 'output\project.json' --render 'output\video.mp4' --resolution 1080p
```

Các tham số cũng dùng được với EXE. Studio chạy offline sau khi cài model Piper và FFmpeg, không dùng API tạo video hay credit khi render. Không cài thêm model nhận dạng giọng nói trong bản này.

Ví dụ một hàng storyboard mới:

```json
{
  "start": 0, "end": 8,
  "style": "ink", "layout": "timeline",
  "title": "Đặt dấu vết vào bối cảnh", "text": "Lời đọc…",
  "asset_ids": ["house", "city", "clock"],
  "labels": ["Khởi đầu", "Phát triển", "Tiếp theo"],
  "reveal_times": [0.4, 2.5, 4.5],
  "gestures": [{"t": 0, "pose": "rest"}, {"t": 0.5, "pose": "point", "blend": 0.85}]
}
```

`assets` nhận đường dẫn hình người dùng. `asset_ids` nhận ID trong catalog. `objects` đặt thêm lớp, keyframes, attachment và parent. Trong layout có người dẫn, ID authoring mặc định `presenter`; compiler remap các liên kết sang ID riêng của cảnh. Thời gian trong hàng là giây toàn video; thời gian lớp, gesture và reveal là giây trong cảnh.

## Thành phẩm và kiểm tra

- `outputs/ink_v4/ink_history_1080p.mp4`: pilot 87,4 giây, 11 cảnh có lời.
- `examples/ink_showcase/project.json`: project portable chỉnh sửa được của pilot.
- `outputs/ink_v4/second_story_1080p.mp4`: câu chuyện khác dài khoảng 3 phút 10 giây, dựng cùng engine/thư viện. Không phải quy trình tự động đã được chứng minh trên mọi chủ đề.
- `outputs/ink_v4/motion_three_cases_1080p.mp4`: ba đoạn 8 giây kiểm tra chỉ tay, đi/dừng, nhận/giữ vật.
- `outputs/ink_v4/ink_4k_2s.mp4`: đoạn thử 4K, không đại diện cho toàn phim 4K.
- `outputs/ink_v4/load_21min_1080p.mp4`: bài tải 126 cảnh có nhiều bố cục/asset. Đây là bài tải kỹ thuật, không phải một tác phẩm 21 phút đã biên tập nội dung. Báo cáo cần ghi đúng phiên bản engine đã chạy.
- `unit_tests.log`, `verification_v4.json`, báo cáo gói EXE và báo cáo video dài trong cùng thư mục chỉ xác nhận hạng mục có kết quả thực chạy.

Chạy lại kiểm thử:

```powershell
& '..\.venv\Scripts\python.exe' -X utf8 -m unittest discover -s tests -v
& '..\.venv\Scripts\python.exe' -X utf8 tools\verify_ink.py
```

Video và ảnh phải được người dùng xem để chốt mỹ thuật. Kết quả test hình học, codec, thời gian hoặc số frame không chứng minh thành phẩm giống mẫu về thẩm mỹ. Cổng mỹ thuật chưa được coi là duyệt chỉ vì một lựa chọn khác đã được xác nhận.

## Phạm vi còn cần hoàn thiện theo kế hoạch

Chưa có bộ hình đủ ba góc/mặt nghiêng độc lập, công cụ vẽ tự do, đồ thị curve kéo trực tiếp, forced alignment đã kiểm chứng tiếng Việt, hay tự sinh hình chính xác cho một chủ đề bất kỳ. Các bước này không được ghi là đã hoàn thành. Studio hiện cung cấp pipeline dựng và bộ minh họa mới; khâu biên tập và chuẩn bị tài nguyên vẫn quyết định mức gần mẫu của từng video.
