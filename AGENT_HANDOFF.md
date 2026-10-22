# Phối hợp và tiếp quản Studio

Cập nhật: 22/10/2026. Đây là quy trình bàn giao qua file trong repo, không phải
dịch vụ tự gọi Antigravity hay cam kết chất lượng của một model.

## Vai trò

| Việc | Khi Codex đang làm | Khi người dùng chuyển sang Antigravity |
|---|---|---|
| Mục tiêu, phạm vi và thứ tự việc | Codex giữ mục tiêu và checkpoint | Đọc checkpoint, đối chiếu working tree và tiếp tục đúng mục tiêu đã được giao |
| Python/PySide6, timeline, renderer/exporter | Codex sửa; Antigravity review độc lập khi người dùng giao trực tiếp | Có thể làm người phụ trách kỹ thuật sau bài kiểm tra năng lực; sửa từng phần và chạy kiểm tra liên quan |
| Asset, JSON/SRT, đường dẫn, credit | Antigravity kiểm kê và báo cáo có dẫn chứng | Dùng cùng manifest và bản gốc; không yêu cầu lại tài sản đã có |
| Biên kịch, phân cảnh, chuyển động dẫn mắt | Codex chịu trách nhiệm trong phạm vi sản xuất được giao | Tiếp quản việc được giao, đọc quy định hình ảnh, xuất và kiểm tra preview thật |
| Giọng kể Maya | Giữ nguyên custom H | Giữ H/Bắc/1,25× một lần; kiểm tra runtime trước khi tạo mới, không tự đổi engine/giọng |
| QC hình ảnh và nghe tiếng Việt | Xem/nghe bằng công cụ thực tế và ghi bằng chứng | Cùng tiêu chuẩn; thiếu công cụ thì ghi chưa kiểm tra, không tự đánh PASS |
| Chốt thiết kế/giọng, phê duyệt thành phẩm | Người dùng | Vẫn thuộc người dùng; tiếp quản không biến bản thử thành bản được duyệt |

Antigravity không bị giới hạn vĩnh viễn ở vai trò reviewer. Khi người dùng bàn
giao trực tiếp, nó có thể tiếp tục các việc kỹ thuật và sản xuất đã được giao.
Từng loại việc vẫn cần bằng chứng năng lực tương ứng.

## Trạng thái dùng chung

- `coordination/state.json`: mục tiêu, người đang sửa, bước tiếp theo, giới hạn.
- `coordination/tasks.json`: công việc và điều kiện hoàn thành.
- `coordination/checkpoint.json`: HEAD, file thay đổi, môi trường, tài sản khi lưu.
- `coordination/reports/`: kết quả thực tế; không chứa khóa/token đăng nhập.
- `coordination/ANTIGRAVITY_START.md`: nhiệm vụ nhập trực tiếp trong Antigravity.

`AGENTS.md` là quy định sản xuất chính. Đọc `projects/mo_den_maya/HANDOFF.md`.
Tài liệu cũ có chỗ lỗi thời: đã có MP4 và V3 trong working tree; tên file “Final”,
việc tồn tại V3 hoặc số lần lặp thấp không chứng minh người dùng đã duyệt.

## Một người sửa tại một thời điểm

Trước khi sửa, dùng Python đang hoạt động để chạy:

```powershell
python tools/agent_handoff.py claim --owner codex
# Hoặc, trong phiên Antigravity do người dùng mở:
python tools/agent_handoff.py claim --owner antigravity
```

Nếu agent khác đang giữ quyền sửa, mặc định chỉ đọc và báo cáo trong hội thoại.
Chỉ dùng `--takeover` khi người dùng xác nhận dừng bên cũ hoặc chuyển việc:

```powershell
python tools/agent_handoff.py claim --owner antigravity --takeover
```

Đây là khóa phối hợp tự nguyện, không chặn chương trình khác ghi thẳng vào file.
Không cùng sửa production, không tự force-push/reset/clean. Nếu thấy `.state.lock`,
kiểm tra tiến trình trước; không tự xóa khóa đang dùng.

## Checkpoint trước khi hết hạn mức

Không chờ token cuối. Sau mỗi phần việc hoàn tất, trước tác vụ dài, trước khi
dừng/đổi agent và trước câu trả lời cuối của một lượt làm repo:

1. Lưu file; cập nhật `state.json` và task: đã xong gì, còn gì, đường dẫn thực tế,
   lệnh đã chạy, kết quả/lỗi và bước kế tiếp cụ thể.
2. Ghi checkpoint. Công cụ chỉ ghi trạng thái repo; không gọi model, không đọc
   credential, không biết hạn mức tài khoản Codex/Google.
3. Khi dừng sửa, release rồi tạo lại checkpoint để ghi nhận writer đã rảnh.

```powershell
python tools/agent_handoff.py release --owner codex
python tools/agent_handoff.py checkpoint --owner codex --summary "Việc vừa hoàn tất và kết quả kiểm tra" --next "Một bước tiếp theo cụ thể"
```

Nếu quota hết bất ngờ, agent tiếp nhận phải coi checkpoint là ảnh chụp cũ:
đọc `git status`, `git diff`, task/report và tiến trình đang chạy trước khi làm
tiếp. Không rollback thay đổi mới hơn checkpoint. Context bị rút gọn và hết
quota là hai tình huống khác nhau; repo không có daemon tự chuyển nhà cung cấp.

## Bàn giao khi Codex không tiếp tục được

1. Người dùng mở Antigravity chính thức tại repo và gửi:
   **“Read coordination/ANTIGRAVITY_START.md and follow it.”**
2. Antigravity làm AG-001 trước, không dựng phim hay thay lời kể/nhân vật. Kết quả
   phải do chính Antigravity tạo, không sao chép baseline Codex rồi coi là đã thử.
3. Khi AG-001 chứng minh khả năng cần thiết, người dùng có thể giao:
   **“Tiếp quản công việc Codex đang dở theo checkpoint.”** Antigravity claim quyền
   sửa và tiếp tục mục tiêu đã được cho phép; không tự mở rộng phạm vi.
4. Codex quay lại phải đọc trạng thái mới và diff trước, không dùng trí nhớ cũ
   ghi đè công việc Antigravity.

Nếu còn ở Plan mode, Antigravity chỉ nghiên cứu/lập kế hoạch. Người dùng cần
chọn chế độ cho phép thao tác trong client trước bước ghi file hoặc test tạo file
tạm; không bật bỏ qua toàn bộ quyền.

Google hiện không hỗ trợ bọc `agy` trong agent bên thứ ba hoặc tự động luân phiên
tài khoản cá nhân. Ở đây người dùng khởi chạy và giao việc trực tiếp trong client,
chia sẻ trạng thái bằng repo. Tài liệu: https://antigravity.google/docs/faq/ và
https://antigravity.google/docs/rules .

## Môi trường trên máy này

- HEAD khảo sát: `30b1e621995bc167819f0498eb44ec2ddd2ab1f5`.
- Python mặc định 3.12.10 thiếu PySide6 và Piper, chưa chạy được app đầy đủ.
- Interpreter cũ có PySide6 + Pillow, đã dùng được cho renderer/test:
  `projects/angkor_wat_1min/.venv/Scripts/python.exe`.
- `.venv/Scripts/python.exe` ở root chưa có. Máy khác cần probe lại, không chép
  venv giữa máy. `install_windows.bat` còn tải giọng/demo legacy; không chạy mù
  như bước sửa môi trường Maya.
- FFmpeg/ffprobe có trên PATH. VoxCPM2 GGUF có runtime riêng; thiếu module Python
  `voxcpm` chưa kết luận runtime GGUF thiếu. Chưa thử tạo giọng mới trong lượt này.
- Bảo toàn sáu WAV local đã ghi trong checkpoint; không reset/clean.

Lệnh mẫu với môi trường Qt đã kiểm tra:

```powershell
$env:QT_QPA_PLATFORM = 'offscreen'
& 'projects/angkor_wat_1min/.venv/Scripts/python.exe' -X utf8 tools/agent_handoff.py status
& 'projects/angkor_wat_1min/.venv/Scripts/python.exe' -X utf8 -m unittest discover -s tests -p 'test_media_delivery.py' -v
```

`coordination/reports/codex_baseline.md` ghi những gì Codex đã thật sự chạy.
Nó không chứng nhận năng lực Antigravity, QC thẩm mỹ hay QC nghe.
