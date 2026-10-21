# Phần mềm và tài nguyên bên thứ ba

## Bút vector trong bàn vẽ

- `perfect-freehand-python` 1.2.0, MIT; nguồn: https://github.com/bigbluebutton/perfect-freehand-python .
- Thuật toán gốc: https://github.com/steveruizok/perfect-freehand .
- Copyright 2021 Stephen Ruiz Ltd; 2022 Calvin Walton. Mã Python không sửa đổi được đóng kèm trong `studio/vendor/perfect_freehand`; giữ SPDX trong từng tệp, `LICENSE.txt` và `NOTICE.md`.
- Thư viện biến quỹ đạo bút thành đường bao vector; không phải mô hình sinh ảnh.

Mã nguồn Studio được cung cấp theo GPL-3.0-or-later; giữ toàn bộ mã nguồn khi phân phối bản sửa đổi theo điều kiện của GPL. Không có tài khoản, API trả phí hay cơ chế cấp phép thương mại trong ứng dụng.

## Piper

- Engine: Open Home Foundation / Michael Hansen và những người đóng góp. `piper-tts` 1.8.0, GPL-3.0-or-later.
- Nguồn engine và hướng dẫn: https://github.com/OHF-Voice/piper1-gpl
- Bản phát hành Windows x64 chính thức: https://pypi.org/project/piper-tts/1.8.0/
- Mô hình: `vi_VN-vais1000-medium`, một speaker, 22,050 Hz. Không có bốn voice riêng cho bốn vai.
- Nguồn mô hình, revision cố định: https://huggingface.co/rhasspy/piper-voices/tree/3d796cc2f2c884b3517c527507e084f7bb245aea/vi/vi_VN/vais1000/medium
- Repository mô hình công bố MIT. Model card riêng công bố **dataset CC BY 4.0**, fine-tune từ Lessac medium; giữ nguyên model card trong `voices/MODEL_CARD`. Không suy diễn mọi mô hình trong repository có cùng giấy phép.
- Attribution dataset: **VAIS-1000 Vietnamese Speech Synthesis Corpus**, tác giả/nhà cung cấp VAIS; https://ieee-dataport.org/documents/vais-1000-vietnamese-speech-synthesis-corpus ; https://creativecommons.org/licenses/by/4.0/
- Voice model không bị sửa đổi. Các WAV demo do Studio tạo từ văn bản demo tự viết. SHA-256 và nguồn tải trong `voices/provenance.json`.
- eSpeak NG do các tác giả eSpeak NG phát triển, GPL-3.0-or-later: https://github.com/espeak-ng/espeak-ng . Được Piper dùng để phonemize. Fallback độc lập chỉ hiện khi thực sự có trên PATH.

## Qt / Python / công cụ

- PySide6, Shiboken6 và Qt: The Qt Company và những người đóng góp, LGPL-3.0/GPL hoặc giấy phép tương ứng của từng module. DLL được liên kết động; bản onedir giữ DLL riêng. Nguồn Qt/PySide: https://download.qt.io/official_releases/qt/ và https://code.qt.io/cgit/pyside/pyside-setup.git/ . Bản runtime 6.10.2.
- Python 3.12: Python Software Foundation License; https://www.python.org/downloads/source/ . Không yêu cầu Python được cài sẵn khi dùng EXE.
- ONNX Runtime: Microsoft và những người đóng góp, MIT; https://github.com/microsoft/onnxruntime . Chỉ CPU execution provider.
- Pillow: HPND / PIL Software License; https://github.com/python-pillow/Pillow . Được cài cho mở rộng xử lý ảnh; renderer hiện dùng QImage.
- NumPy: BSD-3-Clause; https://github.com/numpy/numpy .
- PyInstaller: GPL-2.0-or-later với bootloader exception; https://github.com/pyinstaller/pyinstaller .
- FFmpeg: https://ffmpeg.org/ ; bản FFmpeg của máy hiện tại được copy khi đóng gói. Bản có libx264/`--enable-gpl` chịu GPL. Nguồn FFmpeg: https://git.ffmpeg.org/ffmpeg.git ; nguồn libx264: https://code.videolan.org/videolan/x264 . Bản Windows upstream của gyan.dev: https://www.gyan.dev/ffmpeg/builds/ . Giữ LICENSE và cấu hình build trong `third_party_licenses`.
- Segoe UI là font có sẵn trên Windows, không kèm file font trong gói; có thể thay font trong SRT Editor.

`tools/package_runtime.py` chép các tệp LICENSE của dependency đã cài vào `dist/StickmanAnimationStudio/third_party_licenses`. Đọc các giấy phép này trước khi phân phối ra ngoài; nguồn Studio đầy đủ đi kèm bản bàn giao.

Không sử dụng nhạc hoặc ảnh của bên thứ ba trong demo. Nhân vật, đạo cụ, nền, hiệu ứng và câu chuyện demo được tạo trong mã nguồn dự án này.
