# Voice Design local — VoxCPM2

**Cập nhật Maya / custom H:** có thêm runtime Vulkan portable ở
`build-vulkan/bin/studio-voice-batch.exe`, chạy một model liên tục cho cả bài.
Người dùng đã chọn H và cho phép dùng H làm reference để giữ danh tính giữa
các cụm; phần Voice Design không reference bên dưới mô tả bước thử giọng cũ.
Lệnh sản xuất Maya: `tools/create_maya_custom_H.py`. Kết quả riêng trong
`projects/mo_den_maya/voice_direction/full_narration_custom_H_125/`.

GPU RTX 3050 6 GB đã chạy thử clone H. Để vừa bộ nhớ, bản batch giới hạn
BaseLM/ResidualLM ở 2048 token; các cụm ngắn có dư khoảng trống cho reference
và tối đa 350 patch sinh. Overlay giữ nguồn upstream nguyên vẹn. LocEnc xử lý
từng patch độc lập nên bỏ phần zero bị mask, chỉ tính patch reference thật và
cache embedding cho đúng một model/reference trong một tiến trình batch.
Phép đối chiếu embedding reference H với cách cũ có sai số tối đa bằng 0;
đây là kiểm tra tối ưu bộ nhớ, không phải duyệt giọng bằng nghe.
Không bật cache này trong ứng dụng tự nạp lại nhiều model cùng tiến trình.

Thông tin build/hash: `vulkan_installation.json`. SDK Vulkan được tải từ
LunarG và chỉ giải nén payload, không chạy installer, sửa driver hay PATH hệ
thống. `tools/setup_voice_vulkan.py` giữ nguồn tải và kiểm tra checksum.

Bộ chạy riêng để thử giọng mới từ mô tả bằng văn bản. Không dùng preset,
không dùng audio tham chiếu và không tự thay giọng B mặc định của Studio.
Người dùng đã yêu cầu tiếp tục cài local ngày 21/10/2026.

## Các thành phần đã cài

- Model gốc: https://huggingface.co/openbmb/VoxCPM2 . Hỗ trợ tiếng Việt theo
  model card; khả năng giữ vùng Bắc và đúng thanh vẫn phải nghe kiểm tra.
- GGUF: https://huggingface.co/DennisHuang648/VoxCPM2-GGUF . Hai file tổng
  3.552.406.272 byte: BaseLM Q8_0 và Acoustic F16. SHA256 nguồn và file thực
  tế ở `download_receipt.json`, được kiểm tra lại ở `local_model_verification.json`.
- Runtime: https://github.com/tc-mb/llama.cpp-omni , commit
  `a64932ec615e1463158129feaf2f0752d0c07a2e`.
- GCC portable w64devkit 2.10.1 và CMake portable 4.4.4; không đổi PATH hệ thống.
- Executable: `build-cpu/bin/voxcpm2-cli.exe`, build Release CPU, phụ thuộc
  DLL hệ thống Windows. Không cần PyTorch hay API online để tổng hợp.

`vendor/`, `models/`, `downloads/`, `build*/` được bỏ qua khi quản lý Git;
mã setup, cấu hình, hash và phần vá tương thích được giữ trong repo.
Giấy phép và mã nguồn gốc nằm trong thư mục vendor đã giải nén. Runtime MIT;
model gốc và bản GGUF mang điều khoản Apache-2.0 theo nguồn tương ứng.

## Chạy mẫu local

Từ thư mục gốc Studio:

```powershell
projects/angkor_wat_1min/.venv/Scripts/python.exe -X utf8 tools/design_mo_den_local.py
```

Kết quả:
`projects/mo_den_maya/voice_direction/local_custom_voices_v1/`.
Mỗi thiết kế tổng hợp một đoạn liền, không cắt 275 cue, không đọc tên trường
JSON. Mô tả giọng đặt trong ngoặc trước câu theo giao diện Voice Design thật
của VoxCPM2. Không truyền `--reference`, `--prompt-wav` hoặc mã giọng preset.
Giữ bản native, mô tả, seed, hash và log UTF-8. Bản nghe tăng tốc 1,25×,
không dịch cao độ và được cân âm lượng để so sánh.

Có thể tạo riêng một mẫu bằng `--only 01_custom_A` (hoặc B/C). Khi dùng tùy
chọn này, mức nghe chỉ được xử lý cho mẫu đó; chạy đủ ba để cân so sánh.

## Build trên Windows

Tải có checksum bằng `tools/setup_local_voice_design.py` (cần mạng chỉ ở bước
tải). Build không thay mã nguồn model. Hai overlay trong `patches/`:

1. Manifest activeCodePage UTF-8 để argv có đủ dấu tiếng Việt trên Windows.
2. Khai báo `iovec` cho đường đọc Windows đã có sẵn trong mã upstream,
   giải quyết lỗi biên dịch của `llama-moe-slot.cpp`; không đổi thuật toán TTS.

Cấu hình hiện tại trong `build-cpu/CMakeCache.txt`. Tắt ccache vì máy này không
ghi được thư mục cache mặc định. Các đường overlay hiện gắn với vị trí checkout
này; khi chuyển máy/thư mục cần cập nhật đường trong `.cmake` và `.rc` trước build.

## Giới hạn và đánh giá

CPU smoke test tạo được WAV 48 kHz 6,24 giây trong khoảng 44 giây tổng hợp.
Đây là kiểm tra cơ chế, không phải duyệt nội dung âm thanh. GPU RTX 3050 có
6 GB VRAM; bản CPU lịch sử không bật CUDA/Vulkan. Bản Vulkan mới được ghi
riêng ở đầu tài liệu và `vulkan_installation.json`.

Voice Design sinh người nói mới; seed cố định không đảm bảo danh tính giữ
nguyên giữa mọi văn bản. Sau khi người dùng chọn, cần cố định chính giọng
đã sinh làm reference local cho các đoạn dài, rồi kiểm tra nhất quán. Không
tự quay lại preset cũ. Việc dùng bản sinh đã chọn làm reference để giữ giọng
khác với việc lấy một giọng mẫu sẵn làm thiết kế ban đầu.

Phải nghe từng mẫu để duyệt thanh điệu, số, cụm nghĩa, đầu/cuối câu, mức
tinh nghịch, vùng giọng Bắc và độ tự nhiên. Chỉ số peak/RMS/codec hoặc việc
build thành công không chứng minh chất lượng nói. Không báo QC nghe đạt
khi chưa có kiểm tra nghe. Lựa chọn mẫu không tự duyệt toàn bài Maya.
