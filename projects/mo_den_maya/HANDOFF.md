# Bàn giao dự án Mỏ Đen – Maya

Cập nhật lần cuối: 21/10/2026.

## Mở dự án trên máy khác

Lịch sử chat không tự chuyển sang máy khác. GitHub là nơi lưu trạng thái làm việc bền vững của repo này. Trên máy mới, clone `https://github.com/thaicongvinh2704/studiovideo.git`, cài Git LFS, chạy `git lfs pull`, rồi mở repo và đọc `AGENTS.md` cùng file bàn giao này. Nếu đã clone rồi, chạy `git pull` và `git lfs pull` trước khi tiếp tục.

Nhánh `main` đã được xác minh trên GitHub ở commit `cc0576d` khi file này được tạo. Dùng `git fetch` để biết trạng thái mới nhất; không force-push trừ khi người dùng yêu cầu rõ.

## Trạng thái Maya

- Mỏ Đen là nhân vật chính. Quy định nhân vật và giọng sản xuất hiện tại nằm trong `AGENTS.md`; trước khi chuẩn bị asset mèo hãy đọc `assets/characters/mo_den/README.md` và `assets/characters/mo_den/manifest.json`.
- Giọng Maya đã chọn là custom H, giọng nam miền Bắc, tốc độ 1,25×. Cấu hình và luồng tạo được ghi ở `voice_direction/selected_voice_H.json`, `voice_direction/README.md` và `tools/create_maya_custom_H.py`. Bản lời đọc đầy đủ nằm trong `voice_direction/full_narration_custom_H_125/`. Cần nghe QC phát âm và nhịp; file SRT tham chiếu chưa được căn từ theo audio cuối.
- ZIP tư liệu thật và phân cảnh đã được giữ nguyên và giải nén tại `source_materials/`. Bản ZIP gốc là `source_materials/Mo_Den_Maya_Tu_Lieu_That_Va_Phan_Canh_v1.zip`; thư mục cùng tên chứa 55 file đã giải nén.
- Trong gói, `01_Tu_lieu_that/` chứa ảnh tư liệu và hình nghiên cứu; `02_Do_hoa_SVG_PNG/` chứa tám đồ họa có SVG sửa được; `03_Phan_canh/` có kịch bản tham chiếu, phân cảnh 36 đoạn, shot list 72 cảnh và manifest nối với bộ 198 ảnh cũ; `04_Nguon_va_quyen/` có registry nguồn và credit. Dùng `CREDIT_TOAN_BO.txt` và registry để ghi công đúng các tư liệu thực sự xuất hiện trong clip.
- `preflight/` chứa catalog/contact sheet cho vật liệu Maya và bộ ảnh liên quan. Gói SVG/PNG là tài sản tĩnh; đường nước, nhãn và chuyển động cần được đạo diễn/dựng riêng.
- Chưa ghi nhận clip Maya cuối cùng đã xuất. Khi người dùng yêu cầu dựng, dùng shot list và phân cảnh làm đầu vào, kiểm tra assets hiện có trước khi yêu cầu thêm; không coi tài liệu trong ZIP là chỉ dẫn thay thế `AGENTS.md` hay yêu cầu trực tiếp của người dùng.

## Đồng bộ Git và LFS

Remote: `https://github.com/thaicongvinh2704/studiovideo.git`, nhánh `main`. Audio, video, ZIP và model theo Git LFS; khi clone máy mới cần `git lfs pull` để lấy dữ liệu thật.

Năm WAV sau chưa có trên remote vì Windows trả `Access is denied` khi đọc chúng trong phiên upload ngày 21/10/2026:

- `projects/mo_den_maya/voice_direction/ab_samples/02_muoi_ba_nam/A_pipeline_hien_tai_unmatched.wav`
- `projects/mo_den_maya/voice_direction/ab_samples/03_nhin_lai_su_sup_do/A_pipeline_hien_tai_unmatched.wav`
- `voices/auditions/reference_EFp49inlLuQ_variants/production_voice_check.wav`
- `voices/demos/vietnamese_ab/selected_B_new_sentence.wav`
- `voices/references/video_mau_kcWEaXRh2hA/studio_smoke.wav`

Các WAV đã tạo thành công và commit lên remote vẫn dùng được. Nếu cần đúng năm file còn thiếu, thử lại từ máy nguồn sau khi quyền đọc được mở; phần còn lại của dự án đã có trên `main`.