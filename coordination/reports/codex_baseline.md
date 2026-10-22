# Baseline kỹ thuật do Codex thực hiện

Ngày 22/10/2026, working tree dựa trên HEAD `30b1e62`.
Người thực hiện các kiểm tra ở file này: **Codex**, không phải Antigravity.
Chưa có báo cáo `antigravity_acceptance.md`; không suy năng lực agent từ baseline.

## Môi trường và tài sản

- Python hệ thống: 3.12.10, có Pillow, thiếu PySide6 và Piper.
- Đã dùng `projects/angkor_wat_1min/.venv/Scripts/python.exe`: 3.12.10,
  có PySide6/Pillow; thiếu module piper/voxcpm. Module voxcpm không phải runtime
  GGUF của Maya nên không dùng kết quả này để kết luận engine H thiếu.
- `ffmpeg`/`ffprobe`: có trên PATH.
- Có `voices/local_design/build-vulkan/bin/studio-voice-batch.exe`,
  `voices/local_design/models/VoxCPM2-BaseLM-Q8_0.gguf` và
  `voices/local_design/models/VoxCPM2-Acoustic-F16.gguf`.
  Bản `build-cpu/bin/studio-voice-batch.exe` chưa có tại vị trí đó.
  Đây là kiểm tra tồn tại, chưa chạy synthesis hay kiểm chứng driver Vulkan.
- SHA256 của H native và audition đã chọn khớp `selected_voice_H.json`.
- Manifest Mỏ Đen có 24 mục và 24 đường dẫn tồn tại. Chưa xem lại hình trong
  lượt bàn giao này; không tạo thêm chứng nhận thẩm mỹ từ kiểm tra tồn tại.

## Các test đã chạy

Đặt `QT_QPA_PLATFORM=offscreen`; prefix mỗi lệnh là:

```powershell
& 'projects/angkor_wat_1min/.venv/Scripts/python.exe' -X utf8
```

| Phần lệnh tiếp theo | Kết quả thực tế |
|---|---|
| `-m unittest discover -s tests -p 'test_supplied_character.py' -v` | 4/4 OK, exit 0 |
| `-m unittest discover -s tests -p 'test_media_delivery.py' -v` | 2/2 OK, exit 0; có xuất clip test 1 giây và ffprobe; không skip |
| `-m unittest discover -s tests -p 'test_agent_handoff.py' -v` | Ban đầu 6/6; sau sửa Unicode console trong lượt khảo sát hoạt hình chạy lại 7/7 OK, exit 0 |
| `-m unittest discover -s tests -p 'test_vietnamese_narration.py' -v` | 4/4 OK, exit 0 |

Các lần chạy trên bao phủ 17 test, không failure/error/skip. Không chạy toàn bộ
test suite hoặc UI smoke. Thêm một test cho console Windows dùng code page cũ:
claim từng ghi trạng thái xong nhưng lỗi in tiếng Việt; CLI nay xuất UTF-8.
Test bàn giao gồm ngăn ghi đè writer khác, takeover rõ ràng, tranh chấp khóa,
phân biệt pointer LFS, giữ đúng trạng thái Git và ghi lỗi LFS thay vì báo tree sạch.
Test normalization tiếng Việt không kiểm tra phát âm hay vùng giọng.

## Probe media thật

```powershell
ffprobe -v error -show_entries format=duration:stream=codec_type,codec_name,width,height,sample_rate -of json 'outputs/Mo_Den_Maya_Dao_Dien_Final_1080p.mp4'
ffprobe -v error -show_entries format=duration:stream=codec_type,codec_name,sample_rate -of json 'projects/mo_den_maya/assets/audio/narration.wav'
```

Cả hai exit 0. MP4: H.264 1920×1080, AAC 48 kHz, 852,208333 giây.
WAV: PCM s16le 48 kHz, 831,206167 giây. Không phải pointer LFS.
Khác độ dài không tự kết luận sai: cần đối chiếu timeline/credit nếu sửa phim.
Không xem/nghe lại toàn bộ video trong lượt này. Tên “Final” không là phê duyệt.

## Git và dữ liệu chưa commit cần bảo toàn

`git status` trong sandbox có thể lỗi clean filter LFS vì không ghi được `.git/lfs/tmp`.
Đã kiểm tra trạng thái với quyền phù hợp và ghi checkpoint ở cuối lượt.
Không tắt filter để coi một ZIP đã hydrate là file bị sửa; không báo tree sạch
khi `git status` thất bại.

Các WAV có sẵn trước thay đổi bàn giao:

- Modified: `projects/mo_den_maya/voice_direction/ab_samples/01_mo_bai/A_pipeline_hien_tai_unmatched.wav`
- Untracked: `projects/mo_den_maya/voice_direction/ab_samples/02_muoi_ba_nam/A_pipeline_hien_tai_unmatched.wav`
- Untracked: `projects/mo_den_maya/voice_direction/ab_samples/03_nhin_lai_su_sup_do/A_pipeline_hien_tai_unmatched.wav`
- Untracked: `voices/auditions/reference_EFp49inlLuQ_variants/production_voice_check.wav`
- Untracked: `voices/demos/vietnamese_ab/selected_B_new_sentence.wav`
- Untracked: `voices/references/video_mau_kcWEaXRh2hA/studio_smoke.wav`

## Chưa kiểm chứng

Khả năng Antigravity thực thi nhiệm vụ này; trả lời model trong phiên mới;
khả năng agent xem ảnh/nghe audio; tạo giọng H mới; chất lượng thẩm mỹ/nội dung
V3/Final; phát âm, vùng giọng và nhịp toàn bài. Không mục nào được đánh PASS.
AG-001 sẽ do Antigravity thực hiện trong client do người dùng trực tiếp vận hành.
