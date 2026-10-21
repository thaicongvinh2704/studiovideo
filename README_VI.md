# STICKMAN ANIMATION STUDIO

## Bàn vẽ riêng đã triển khai

Mở `start_drawing_desk.bat` để dùng bàn vẽ có chỉnh nút Bézier, bút đậm nhạt, ba ảnh chuẩn, mốc liên kết, thư viện và hồ sơ QC. `start_studio_drawing.bat` mở project bài tập cùng timeline. [Hướng dẫn dùng](DRAWING_DESK_GUIDE.md).

Launcher `start_studio.bat` đã ưu tiên mã nguồn mới khi có Python của dự án. Bản EXE cũ trong `dist` chưa được build lại. Bài tập mới chỉ có vật thể; chưa có mẫu nhân vật được duyệt.

## Bắt buộc: nhân vật theo ba ảnh tham chiếu và QC

**Trạng thái hiện tại:** người dùng đã loại cả mẫu 01 và mẫu study-02. QC thẩm mỹ của study-02 là false positive, đã thu hồi. Chưa có master nhân vật đạt yêu cầu; nút Người dẫn sẽ bị chặn với mẫu cũ. Không dùng các kết quả test cơ chế phía dưới làm bằng chứng rằng nhân vật đẹp hoặc giống tham chiếu.

Đọc [AGENTS.md](AGENTS.md) và [CHARACTER_STANDARD.md](CHARACTER_STANDARD.md) trước khi vẽ/sửa người. Ba ảnh gốc đã được giữ tại `assets/styles/explainer_reference_v1/`; không dùng trí nhớ hoặc người dẫn mặc định cũ làm chuẩn. Nhân vật áo xanh cầm sổ “Nét Mộc 01” đã bị người dùng từ chối; vật thể vẫn giữ cách vẽ hiện có.

Mỗi nhân vật cần ảnh QC toàn hình, mặt, hai tay, bản nhỏ và bảng so sánh ba reference; kiểm tra từng mục có nhận xét, lưu cùng hash nét và hash ảnh đã xem. Đổi nét thì QC hết hiệu lực. Bàn vẽ chặn xuất SVG/PNG/đưa vào cảnh khi chưa đạt; cả hai đường xuất video chặn QC thiếu hoặc cũ, kể cả khi `allow_draft` được bật. Lưu nháp và render ảnh để QC vẫn được phép. Người dẫn rig cũ cần thay bằng hình tĩnh đã QC trước khi xuất lại. Bản EXE cũ chưa build lại.

Trong bàn vẽ, phân loại lớp **Nhân vật → QC nhân vật…**, mở đủ các tab, kiểm tra và ghi nhận xét trước khi lưu QC. Nút **Người dẫn** chỉ được chèn mẫu còn hiệu lực; hiện mẫu cũ đã bị loại. `start_studio_drawing.bat` mở bản hiện tại. Ghi QC nội bộ không có nghĩa người dùng đã duyệt một thiết kế mới.

## Bàn vẽ riêng · nghiên cứu 20/10/2026

Yêu cầu hiện tại: hình vẽ vector theo bộ quy tắc riêng, nhân vật tĩnh, kết hợp ảnh chụp thật; không dùng AI sinh ảnh. Chuyển động đạo diễn sau trên từng lớp như gạch rơi, mũi tên và tuyến nước. Chuẩn yêu cầu và giới hạn bản thử ở [DRAWING_DIRECTION.md](DRAWING_DIRECTION.md). Mẫu “Nét Mộc” chưa được người dùng duyệt làm phong cách chính thức.

Chạy **start_studio_drawing.bat** để mở bản mã nguồn có nút **Bàn vẽ…** và project mẫu; **start_drawing_desk.bat** mở riêng bàn vẽ. Có bút nét/vùng kín, tô màu, tẩy cả nét, lớp, undo/redo, lưu bản vẽ, xuất SVG/PNG và đưa từng lớp vào cảnh. Ảnh xem trước ở `projects/drawing_desk_study/`. EXE cũ chưa được build lại; các mục V4/V3 bên dưới mô tả các bản trước.

## Video minh họa V4 · 19/10/2026

Studio hiện ưu tiên mở `examples/ink_showcase/project.json`: video 87,4 giây với người dẫn áo đen có dấu cộng trắng, quần xanh, giày trắng theo ảnh tham chiếu người dùng. Có bảng 20 tư thế, 42 SVG, nhóm cha/con, điểm xoay, chỉnh Bezier và quy trình nhập kịch bản/voice/hình. Xem **INK_V4.md** để biết cách dùng và phạm vi đã triển khai. Video ở `outputs/ink_v4/ink_history_1080p.mp4`; clip chuyển động ở `outputs/ink_v4/motion_three_cases_1080p.mp4`. Các kết quả V3/V2 bên dưới là lịch sử của bản cũ.

## Video minh họa V3 · 18/10/2026

Bấm **Kịch bản + voice…** để nhập TXT/SRT, voice và ảnh; chỉnh bảng phân cảnh, chọn bố cục rồi tạo project. Thêm người dẫn có trang phục, chữ, hình, SVG, crop ảnh, waveform và nhóm lớp. Studio mở demo `examples/explainer_showcase/project.json` khi có. Video mới: `outputs/explainer_v3/history_explainer_1080p.mp4` (68,6 giây, 8 cảnh, 1080p/30 FPS).

Hướng dẫn đầy đủ và mẫu storyboard: **EXPLAINER_V3.md**. TXT được chia thời gian ước lượng; muốn mốc chính xác cần SRT đã căn hoặc biên tập theo voice. Studio chưa tự nhận dạng giọng nói/sinh mọi minh họa từ văn bản. Codex có thể biên tập storyboard và xuất video từ các file bạn cung cấp.

V3 thêm xuất 4K; audio mặc định stereo 48 kHz; ghép cảnh theo lưới frame và trộn audio cuối một lần. Các phần V2 dưới đây là hướng dẫn cho demo chiếc ô vẫn được giữ lại.

Ứng dụng Windows native bằng Python + PySide6. Render xương vector 2D bằng QPainter, giọng tiếng Việt bằng Piper CPU, MP4 H.264/AAC bằng FFmpeg. Sau khi cài dependency và voice, chạy offline, không GPU rời, không token/credit.

## Mở ngay trên máy này

Chạy **start_studio.bat**. Nếu đã build, script mở `dist\StickmanAnimationStudio\StickmanAnimationStudio.exe`. Nếu chưa build, script dùng môi trường Python riêng đã cài.

Để mở demo chiếc ô có giọng đọc: **Mở → examples\yellow_umbrella_v2\project.json**. Bản này có 12 cảnh, 36 cue, 36 WAV tiếng Việt và tổng thời lượng 180 giây. Video ở `outputs/quality_v2/yellow_umbrella_180s_1080p.mp4` (1080p/24 FPS); bản cũ được giữ để đối chiếu. Studio ưu tiên mở demo minh họa V4 khi khởi động.

## Bản tối ưu hình ảnh V2

- Đi/chạy theo quãng đường, chân trụ bằng IK, blend vào/ra clip; nhảy một lần có lấy đà và tiếp đất.
- Camera biến đổi cả cảnh, có nhiều shot; nhân vật lớn hơn, biểu cảm/ánh nhìn/chớp mắt theo thời gian, tỷ lệ tuổi khác nhau.
- Tiếp xúc tay và trao ô liên tục; cảnh đoàn tụ dùng contact vai/upper arm, không chỉ pose tự khoanh tay.
- Nền, phụ đề và hiệu ứng được chỉnh lại; có vùng che mưa đơn giản dưới ô và insert ảnh chiếc ô cũ trên điện thoại.
- Export mặc định 1080p; chọn Nháp/Cân bằng/Bàn giao, tùy chọn làm mượt nét 2×. Final dùng H.264 CRF 18 / medium và BT.709. Preview mặc định 720p, vẫn có thể hạ 480p.

Công cụ mới ở Properties (cuộn xuống): **Tiếp xúc tay / ôm**, **Biểu cảm / tuổi theo thời gian**. Phần cảnh có **Góc máy trong cảnh**. Camera keyframes chỉnh shot chứa playhead nếu có; nếu không, chỉnh camera toàn cảnh. Contact dùng tọa độ world khi chọn Tự do; khi chọn nhân vật, X/Y là offset so với khớp đích. Có thể đặt quỹ đạo điểm tự do bằng Keyframe.

Dữ liệu project vẫn mở được từ schema 1; chỉ dùng bản Studio V2 để chỉnh các track mới. Chi tiết thay đổi và kiểm thử ở `QUALITY_V2.md` và `outputs/quality_v2/verification.json`.

## Cài mới trên Windows x64

1. Cài Python 3.11 hoặc 3.12 x64 từ python.org. Bản phát triển này được kiểm thử với Python 3.12.14 trên Windows.
2. Chạy `install_windows.bat` khi có internet. Script cài thư viện trong `.venv` và tải voice từ upstream, không cài dịch vụ nền.
3. Cần `ffmpeg.exe` và `ffprobe.exe` trên PATH hoặc trong thư mục `bin` của Studio. Bản EXE bàn giao đã kèm hai tệp này.
4. Chạy `start_studio.bat`. Từ đây có thể ngắt mạng.

## Tạo câu chuyện của riêng bạn

1. Bấm **Mới**: nhập tên, thời lượng cảnh đầu, tỷ lệ khung hình. Timeline lưu được trên 15 phút; không giữ toàn bộ frame trong RAM.
2. Chọn cảnh ở cột trái, dùng **+ / Nhân bản / Xóa / ↑ / ↓**. Ở Properties, kéo xuống phần cảnh để đổi tên và độ dài.
3. Chọn tab **Nhân vật / Đạo cụ / Nền / Hiệu ứng**, chọn mục rồi bấm **Thêm mục đang chọn**, hoặc nhấp đúp. Bấm lại hiệu ứng để tắt/bật hiệu ứng đó.
4. Chọn nhân vật trên canvas hoặc danh sách ở Properties. Kéo nhân vật để đổi vị trí. Sửa X/Y, Scale, Rotation, Opacity, Layer, Start/End, tốc độ, action, biểu cảm rồi bấm **Áp dụng thuộc tính**.
5. **Đặt action từ playhead** tạo action clip với blend 0.35 giây. Chọn action từ Library sẽ áp dụng toàn cảnh và xóa action clip cũ của nhân vật đó.
6. **Keyframe** chỉnh timestamp cục bộ của cảnh và nội suy linear/ease/Bezier. `bone_*` là góc tính bằng radian, `bone_lift` là độ nâng tính bằng pixel. `hand_l/r_x/y` là target IK cục bộ quanh gốc nhân vật. Keyframe transform đã có được cập nhật tại playhead khi kéo nhân vật; bật ô **Đặt keyframe transform** để tự thêm keyframe cho transform chưa có.
7. **Rig / IK** thay chiều dài thân, tay, chân và ghim bàn tay vào target hai khớp. Checkbox **Xương** trong preview hiển thị các khớp.
8. Chọn đạo cụ và dùng **Gắn / trao đạo cụ**: mỗi mốc có thời gian, người cầm và khớp. Trong demo V2, ô chuyển từ Father sang Son ở giây 3.2 trong cảnh 11, sau khi hai tay đã cùng chạm điểm cầm. Thả đạo cụ bằng mốc có người cầm **Tự do**. X/Y không có hiệu lực trong thời gian đạo cụ đang gắn vào tay; scale/rotation vẫn có hiệu lực.
9. **Nhập → Background / Overlay / Reference** nhận PNG, JPG, JPEG, WEBP. Reference là ảnh phẳng, mở để tham khảo; không tự động rig ảnh. Danh sách đối tượng có số Layer để sắp xếp trước/sau.
10. **Nhập → SRT** giữ nguyên timestamp của file UTF-8/BOM. **SRT Editor** chỉnh thời gian, lời, vai, font, size, màu, vị trí/nền phụ đề. Có thể thêm/xóa và xuất SRT.
11. **Voice Studio** chọn cue hoặc nhập chữ, chỉnh speed/volume, tạo WAV, nghe, lưu WAV, áp dụng timeline. **Tạo tất cả cue SRT** sinh từng WAV và đặt ở đúng timestamp. Vai Narrator/Father/Mother/Son dùng cùng voice nếu chỉ có một model. Không cắt lời dài hơn cue: thông báo cảnh báo để bạn tăng tốc hoặc sửa thời lượng. WAV nằm trong assets của project.
12. **Audio** nhập MP3/WAV (cũng nhận OGG/FLAC), chọn nhóm, start/duration/trim/volume/fades/mute, nghe clip; bật giảm nhạc khi có lời. Preview dùng Qt media; export mix theo nhóm bằng FFmpeg, limiter chống clipping. Với source trim vượt độ dài file, hãy giảm trim/duration.
13. **Camera keyframes** đặt x/y/zoom; dropdown Camera theo chọn nhân vật. Safe frame, Preview Quality, Zoom preview đều hoạt động. Tắt hiệu ứng preview để giảm CPU; export vẫn render hiệu ứng.
14. **Xuất MP4**: 480p/720p/1080p/4K, 12/24/30 FPS, toàn project hoặc cảnh chọn, burn subtitle và/hoặc SRT riêng. Progress theo frame thật; giai đoạn mix có thông báo riêng. Có Hủy và giao diện tiếp tục nhận thao tác. Output cũ chỉ được thay khi xuất thành công. Bật **Lưu từng cảnh** để giữ MP4 từng cảnh trong thư mục `tên_video_scenes`; nếu lỗi/hủy, xuất lại cùng đường dẫn và dữ liệu để bỏ qua các cảnh đã hoàn tất. Thay project/assets/thông số sẽ làm cache cũ hết hiệu lực.
15. **Lưu / Lưu thành / Xuất gói** chép asset vào thư mục project, dùng đường dẫn tương đối. **Nhập gói** cần thư mục đích mới. Autosave mỗi 60 giây khi có thay đổi; **Cài đặt → Khôi phục autosave** mở lại bản tự lưu. **Relink** tìm tài nguyên thiếu.

Phím tắt: **Space** phát/tạm dừng, **Ctrl+S** lưu, **Ctrl+Shift+S** lưu thành, **Ctrl+Z / Ctrl+Y** Undo/Redo. Khi nhập chữ trong bảng hoặc Voice Studio, phím Space dành cho ô đang nhập.

Timeline: mỗi nhân vật/đạo cụ có lane riêng. Kéo thân clip để đổi Start; kéo mép phải để đổi End. Snap theo frame của FPS dự án; dùng Zoom để chọn clip ngắn. Cuộn dọc để xem audio/phụ đề và waveform. Có thể kéo splitter để mở rộng timeline. Cảnh mới từ storyboard có voice/SRT đi cùng cảnh khi sắp lại; project cũ hoặc clip không gắn scene_id giữ timestamp tuyệt đối.

## Kiểm thử và bằng chứng

Chạy từ thư mục source (đổi `.venv` thành `..\.venv` nếu đang dùng môi trường của workspace bàn giao):

```bat
.venv\Scripts\python.exe -X utf8 -m unittest discover -s tests -v
.venv\Scripts\python.exe -X utf8 tools\verify.py --full
.venv\Scripts\python.exe -X utf8 main.py --smoke
```

`tools/verify.py --full` tạo WAV thật, phát WAV bằng Qt, thao tác canvas/timeline bằng QtTest, khởi tạo các panel, xuất 15s và 180s rồi kiểm tra ffprobe và phát MP4 bằng Qt. `outputs/verification.json` lưu trạng thái thực tế; các tệp `*_probe.json` lưu codec, duration, FPS, resolution, audio stream. Screenshot 1366×768 và 1920×1080 nằm trong outputs.

**Không dùng NOT_RUN làm PASS.** Bản bàn giao ghi rõ các kiểm thử đã thực thi trong `TEST_RESULTS.md`.

## Build EXE

Chạy `build_windows.bat`. Bản **onedir** giữ DLL Qt riêng và giúp thay model/assets. Copy cả thư mục `dist\StickmanAnimationStudio`, không chỉ EXE. Bản EXE không cần Codex hay Python cài sẵn. Trước khi build lại, bản app hiện có được đổi tên thành thư mục backup để giữ project/demo đã chỉnh; script không xóa bản cũ. `tools/package_runtime.py` kèm voices, demo, presets và FFmpeg tìm thấy trên PATH. `THIRD_PARTY_NOTICES.md` và thư mục third_party_licenses chứa nguồn/giấy phép.

Trong thư mục EXE có `StickmanAnimationStudio-Source.zip` chứa mã nguồn tương ứng, tests, script build, presets và demo. ONNX không lặp lại trong source ZIP; copy thư mục `voices` cạnh EXE vào source sau khi giải nén, hoặc chạy install script để tải từ nguồn chính thức.

## Kiến trúc

- `studio/project.py`: JSON schema 1, save/load, media, history, ZIP.
- `studio/animation.py`: engine độc lập UI, FK/IK, 20 action procedural, keyframes, blending, attachments.
- `studio/renderer.py`: vẽ vector, ảnh cached, biểu cảm, camera, mưa/tuyết/lá/gợn/fade/flash/shake/shadow; preview/export cùng engine.
- `studio/tts.py`: Piper offline, eSpeak NG hoặc System.Speech fallback khi phù hợp.
- `studio/exporter.py`: pipe RGB → FFmpeg; mix audio theo batch; output atomic; cancel và lỗi.
- `studio/ui`: native splitter panels, canvas, timeline, editor dialogs, worker QThread, audio preview.

## Phạm vi và giới hạn hiện tại

- Các action dùng rig/IK và keyframe, không phải mô phỏng cơ thể đầy đủ. V2 có chân trụ theo quãng đường X và contact tay giữa nhân vật. Khóa chân được kiểm tra trên đường đi X của demo; di chuyển Y, scale/rotation thay đổi mạnh hoặc mục tiêu ngoài tầm với vẫn cần biên tập. Hug cần đặt contact đúng người/khớp; không tự hiểu nội dung văn bản để dàn dựng.
- V3 có waveform và chọn nhiều lớp để nhóm kéo cùng nhau. Chưa có ripple-edit, lồng cảnh, pivot nhóm đầy đủ hoặc Bezier tay nắm trực quan. Bezier hiện dùng một đường cong mặc định.
- Bản đầu có **một giọng Piper tiếng Việt**. Đổi vai không tạo giọng tự nhiên khác. Chất lượng/ngữ điệu cần người dùng nghe lại. Fallback system không đảm bảo máy có giọng tiếng Việt.
- Mỗi engine load model ở lần sinh đầu; Voice Studio cho hủy sau đoạn đang xử lý. Preview media dùng codec Qt trên Windows; nghe clip trước khi xuất.
- Thumbnails cập nhật khi chỉnh dữ liệu; không cache toàn bộ video. Cache tối đa 24 ảnh nguồn; nên dùng ảnh nền vừa phải để tiết kiệm RAM.
- Chưa có chế độ tự tách nền, rig ảnh, lip sync hoặc AI video. Không có nút giả cho những phần này.
- Tỷ lệ dọc/vuông giữ cùng không gian cảnh 1280×720 và fit vào canvas với khoảng trống, giữ nguyên tỷ lệ nhân vật. Chưa có layout riêng cho portrait. Chất lượng demo là hoạt hình người que đơn giản có thể chỉnh sửa, cần biên tập thêm nếu dùng để phát hành.
- Cache cảnh chỉ render lại cảnh có dữ liệu liên quan thay đổi; đổi phiên bản engine/render profile làm cache hết hiệu lực. SRT/audio không gắn scene_id giữ timestamp tuyệt đối khi chỉnh thứ tự cảnh.
- Demo V2 đã render đủ 180s ở 1080p/24 FPS. Các clip ngắn 720p/24, 1080p/30 và 480×854/12 cũng được kiểm tra. Kết quả V3, đoạn 4K và bài tải dài xem trong TEST_RESULTS.md; chưa xác nhận trên mọi cấu hình Windows.

Nếu thiếu FFmpeg, model, ảnh, output không ghi được hoặc encoding lỗi, ứng dụng hiển thị thông báo. Không yêu cầu tải nhạc hay mua tài nguyên.

Nếu cửa sổ không mở, xem `launch-error.log` cạnh EXE (hoặc cạnh main.py). Spec đã loại ICU của Poppler khỏi bundle để tránh xung đột với ICU native của Windows khi import QtCore.
