# Đồng bộ Git ngày 24/10/2026

Phạm vi: thay đổi mã nguồn, quy định duyệt trước render, nghiên cứu video tham
chiếu, tư liệu Phong Thần V2, dự án và bảng xem trước, đoạn thử, ba công cụ hỗ trợ
dựng và kết quả kiểm tra. Không đổi giọng, không sửa hoặc render phim trong lượt
đồng bộ. Bốn phản hồi Phong Thần còn tồn tại; xem handoff của dự án.

Remote được kiểm tra: `https://github.com/thaicongvinh2704/studiovideo.git`,
nhánh `main`, khởi đầu local/remote cùng `4881053`. Không ghi đè lịch sử.

Các môi trường, bộ cài, model và cache máy vẫn được ignore (`.deps`, `.models`,
`.cache`, venv). Hướng dẫn và script cài lại được đưa lên. Ảnh mới Phong Thần,
audio/video và ZIP được Git LFS quản lý. Quét tên tệp và mẫu khóa truy cập trong
tệp văn bản mới không tìm thấy credential theo các mẫu đã kiểm tra.

Đã thử đọc lại đầy đủ sáu WAV lỗi cũ ngoài sandbox ngày 24/10: Windows vẫn trả
`Permission denied` (errno 13). Giữ nguyên chúng tại máy, không đổi ACL, không
thay bằng tệp rỗng và không xóa nội dung đã có trong lịch sử Git:

- `projects/mo_den_maya/voice_direction/ab_samples/01_mo_bai/A_pipeline_hien_tai_unmatched.wav`
- `projects/mo_den_maya/voice_direction/ab_samples/02_muoi_ba_nam/A_pipeline_hien_tai_unmatched.wav`
- `projects/mo_den_maya/voice_direction/ab_samples/03_nhin_lai_su_sup_do/A_pipeline_hien_tai_unmatched.wav`
- `voices/auditions/reference_EFp49inlLuQ_variants/production_voice_check.wav`
- `voices/demos/vietnamese_ab/selected_B_new_sentence.wav`
- `voices/references/video_mau_kcWEaXRh2hA/studio_smoke.wav`

Kết quả push và commit được ghi vào task `GIT-PUBLISH-20261024` sau khi xác minh
remote. Upload thành công không chứng nhận chất lượng hình ảnh hoặc nghe giọng.

## Kết quả xác minh

- Commit nội dung: `95c8bfb3eddee4949a92f928d74d9d5445e615cf` — 1.585 file.
- `git push origin main`: exit 0, `4881053..95c8bfb`.
- LFS upload: 793 objects, 890 MB, 100%.
- `git ls-remote origin refs/heads/main`: khớp commit nội dung sau push.
- Đã kiểm tra cú pháp 21 file Python; không có blob Git vượt 90 MiB hoặc runtime/cache trong commit.
- Cảnh báo khoảng trắng cuối dòng ở HTML cũ được giữ; không chỉnh bản dựng trong lượt upload.
- Sáu WAV cũ vẫn là ngoại lệ; không có tư liệu mới hôm nay bị bỏ vì lỗi này.
