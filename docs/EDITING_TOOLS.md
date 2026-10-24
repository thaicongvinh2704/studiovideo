# Công cụ hỗ trợ dựng local

Thêm ngày 24/10/2026 theo yêu cầu người dùng. Đây là bộ hỗ trợ; người dựng vẫn
phải xem từng cảnh, đối chiếu hành động với lời đọc, kiểm tra tư liệu thiếu và
duyệt hình. Không công cụ nào tự cấp chứng nhận thẩm mỹ, QC nhân vật hoặc QC nghe.
Việc chỉnh Phong Thần đang tạm dừng để trao đổi; cài công cụ không cho phép render phim.

## Mở trong Studio

Chạy Studio từ source như thường lệ, chọn **Hỗ trợ dựng…** ở thanh Minh họa.
Đóng/mở lại Studio để nhận mục mới. Bản EXE đóng gói cũ chưa được build lại.

- **Trạng thái**: kiểm tra thư viện và dịch vụ local.
- **Vector**: mở Glaxnimate hoặc tệp SVG/Lottie/rawr. Xuất SVG/PNG để nhập lại;
  chưa có adapter chuyển toàn bộ Lottie thành keyframe native của Studio.
- **Căn lời**: chọn audio và SRT đúng mốc audio, thư mục lưu riêng. Nhận mốc từng từ
  và SRT đề xuất. Không nhận dạng rồi viết đè kịch bản, không chỉnh âm thanh/tốc độ.
- **Kiểm tra hình**: chọn khung hình và nhập lời kể + những chi tiết bắt buộc.
  Nhận nhận xét tiếng Việt để người dựng đối chiếu. Một ảnh không xác nhận được
  trình tự chuyển động/độ mượt/khớp thời điểm. Bản 2B có thể nhận nhầm hoặc bỏ sót.

## Thành phần và môi trường

| Công cụ | Phiên bản / vị trí | Mục đích |
|---|---|---|
| WhisperX | 3.8.6; `.deps/editing/whisperx` | Căn kịch bản đã có vào giọng đọc; CPU để giữ VRAM cho công cụ đọc hình |
| Transformers | 4.57.6; cùng venv | Nạp model căn tiếng Việt |
| PyTorch/torchaudio | 2.8.0 CPU; cùng venv | Môi trường riêng, không đổi runtime TTS |
| Glaxnimate | 0.6.0; `C:/Program Files/Glaxnimate/bin/glaxnimate.exe` trên máy cài | Sửa/chuyển động vector; bộ cài KDE có chữ ký hợp lệ |
| Ollama | 0.40.10; `.deps/editing/ollama` | Chạy model đọc hình local |
| Qwen3-VL | `qwen3-vl:2b-instruct` Q4_K_M; `.models/editing/ollama` | Nhận xét ảnh, không sinh ảnh |

Dịch vụ Ollama riêng bind **127.0.0.1:11435**, chỉ khởi động khi cần đọc hình.
Tắt tính năng cloud; ứng dụng gửi khung hình đến localhost, không upload tư liệu.
Model được unload sau mỗi nhận xét để trả VRAM. Log tại `.cache/editing/ollama.log`.
Cài mới cần mạng tải dependency/model; các môi trường/model/cache nằm ngoài Git.
Glaxnimate là ứng dụng Windows riêng, được nối vào Studio bằng launcher.
Gói KDE Windows thiếu thư viện chuẩn Python 3.11: launcher cấp `PYTHONHOME` riêng
tới `.deps/editing/python311`, dùng thư viện chuẩn Python nhúng 3.11.9 chính thức.
DLL của Glaxnimate vẫn là 3.11.11. Không đổi biến môi trường toàn máy.

Model căn tiếng Việt: `dragonSwing/wav2vec2-base-vietnamese` (model card: Apache-2.0) từ Hugging Face,
cache tại `.cache/editing/huggingface`. Model căn không tạo voice và không chứng minh
đúng thanh điệu/vùng giọng. Giữ giọng H/Bắc/1,25× một lần của các dự án hiện tại.
Không cần token/diarization cho luồng căn lời một người nói này.

## CLI cho agent

Chạy bằng Python Studio đã có (`projects/angkor_wat_1min/.venv/Scripts/python.exe`):

```powershell
& projects/angkor_wat_1min/.venv/Scripts/python.exe -X utf8 tools/editing_tools.py doctor
& projects/angkor_wat_1min/.venv/Scripts/python.exe -X utf8 tools/editing_tools.py glaxnimate
& projects/angkor_wat_1min/.venv/Scripts/python.exe -X utf8 tools/editing_tools.py align --audio INPUT.wav --srt INPUT.srt --output outputs/alignment_review
& projects/angkor_wat_1min/.venv/Scripts/python.exe -X utf8 tools/editing_tools.py review-frame --image FRAME.jpg --narration 'Lời kể' --expected 'Chi tiết bắt buộc' --output outputs/frame_review.json
```

`alignment.json` chứa hash đầu vào, nguyên văn cue, từ có/thiếu mốc và cờ chưa nghe QC.
`aligned_proposal.srt` giữ nguyên nội dung cue, chỉ đề xuất mốc; không tự nhập lại project.
SRT phải cùng gốc thời gian với audio. Nếu timeline có intro 1,5 giây, dùng SRT
gốc của lời đọc thay vì SRT đã cộng intro. Giữ lại các tên/số chưa căn được để xử lý.

## Cài lại trên máy khác

Từ repo, chạy `tools/install_editing_tools.ps1` với PowerShell, mạng và Python 3.12
đã có. Tham số `-StudioPython` cho phép trỏ đến interpreter của máy mới. Script
cài venv riêng, Glaxnimate chính thức, Ollama portable và tải Qwen 2B; model căn
tiếng Việt tải ở lần căn đầu. Không chép venv giữa máy. Không tự đổi Python giọng đọc.

Nguồn chính thức:
- https://github.com/m-bain/whisperX
- https://huggingface.co/dragonSwing/wav2vec2-base-vietnamese
- https://glaxnimate.org/download/
- https://github.com/ollama/ollama/releases/tag/v0.40.10
- https://ollama.com/library/qwen3-vl:2b-instruct

Kết quả chạy thử trên máy: `coordination/reports/editing_tools_20261024/`.
Không coi việc cài thành công hoặc nhận xét của model là đã sửa bốn cảnh người dùng phản hồi.

## Kết quả và lựa chọn sau thử nghiệm

- WhisperX đã căn ba cue / 49 từ trên 10,5 giây giọng H có sẵn. Bản dùng cuối
  ở `alignment_sample_v2/`, giữ nguyên nội dung SRT và hash đầu vào. Chưa nghe QC.
- Model mặc định của WhisperX (`nguyenvulebinh/wav2vec2-base-vi-vlsp2020`) bỏ qua
  lớp `feature_transform` khi nạp bằng Transformers chuẩn; score từ rất thấp
  trong lượt thử (~0,011). Kết quả `alignment_sample/` chỉ là bằng chứng thử bị
  loại, không dùng sản xuất. Model card còn ghi CC-BY-NC-4.0. Đã chuyển sang model
  `dragonSwing/wav2vec2-base-vietnamese`, card ghi Apache-2.0, nạp chuẩn và có
  tín hiệu căn tốt hơn trong đoạn thử. Score không thay cho kiểm tra nghe/mốc.
- Tag Ollama `qwen3-vl:2b` trỏ bản Thinking, thử bị hết giới hạn trước khi trả
  nội dung. Chọn rõ `qwen3-vl:2b-instruct` và từ chối phản hồi rỗng. Tag Thinking
  còn trong cache máy để truy nguyên thử nghiệm, không được dùng bởi launcher.
- Glaxnimate đã xuất hai khung của một mũi tên vector, vị trí khác nhau đúng
  keyframe; `vector_test_result.json` ghi bằng chứng. Không render phim.
- Cửa sổ hỗ trợ đã khởi tạo trong Studio và xem ảnh chụp có chữ tiếng Việt.
