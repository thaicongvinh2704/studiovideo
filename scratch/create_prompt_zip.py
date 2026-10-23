import os
import csv
import zipfile
from pathlib import Path

BASE_DIR = Path("projects/mo_den_phong_than")
PROMPT_MD_PATH = BASE_DIR / "FULL_STORYBOARD_ASSET_PACK_50_PROMPTS.md"

content = PROMPT_MD_PATH.read_text(encoding="utf-8")

# Temporary folder to assemble all zip files
TEMP_DIR = Path("scratch/zip_assembly")
if TEMP_DIR.exists():
    import shutil
    shutil.rmtree(TEMP_DIR)
TEMP_DIR.mkdir(parents=True, exist_ok=True)

# 1. Save full markdown
(TEMP_DIR / "FULL_STORYBOARD_54_PROMPTS.md").write_text(content, encoding="utf-8")
(TEMP_DIR / "FULL_STORYBOARD_54_PROMPTS.txt").write_text(content, encoding="utf-8")

# 2. README instruction
readme_text = """BỘ 54 PROMPT TẠO HÌNH AI CHO PHIM HOẠT HỌA PHONG THẦN DIỄN NGHĨA
====================================================================
Dự án: Vì sao kẻ địch của Khương Tử Nha vẫn được phong thần?
Thời lượng: 15–18 phút (Mỏ Đen dẫn chuyện)

HƯỚNG DẪN SỬ DỤNG:
1. Bạn có thể mở file `PROMPTS_LIST_EXCEL.csv` bằng Microsoft Excel hoặc Google Sheets để dễ quản lý và theo dõi tiến độ tạo ảnh.
2. Thư mục `PROMPTS_BY_CATEGORY/` đã chia sẵn 5 file text tương ứng với 5 nhóm nội dung. Bạn chỉ cần copy từng dòng prompt vào Midjourney, DALL-E 3 hoặc Stable Diffusion (SDXL/Flux).
3. ĐẶC BIỆT LƯU Ý VỀ TÁCH NỀN:
   - Tất cả các item, nhân vật đều đã được gắn lệnh `isolated on pure solid white background` để tạo trên nền trắng tinh khiết.
   - Khi tạo xong, bạn lưu file ảnh PNG/JPG vào thư mục:
     `projects/mo_den_phong_than/incoming_assets/`
   - Studio sẽ tự động tách nền trong suốt (Alpha Channel) và đưa vào dựng video!

CƠ CẤU 54 PROMPTS:
- Nhóm 1 (1 - 8): Khương Tử Nha & Văn Trọng qua các thời kỳ và biến cố
- Nhóm 2 (9 - 18): Tuyến nhân vật đối địch, gian thần, quân vương (Thân Công Báo, Trụ Vương, Đát Kỷ, Phi Liêm, Ác Lai...)
- Nhóm 3 (19 - 30): Tuyến tiên gia, thần tướng & hộ pháp (Triệu Công Minh, Tam Tiêu, Lục Áp, Tiêu Thăng, Hanh Cáp...)
- Nhóm 4 (31 - 42): Trọn bộ bảo vật, pháp khí, cấm thuật (Lạc Bảo Kim Tiền, Định Hải Châu, Đinh Đầu Thất Tiễn, Đả Thần Tiên...)
- Nhóm 5 (43 - 54): Đạo cụ diễn giải (Explainer UI), thẻ bài so sánh & các đại cảnh then chốt
"""
(TEMP_DIR / "00_README_HUONG_DAN_SU_DUNG.txt").write_text(readme_text, encoding="utf-8")

# 3. Categorized prompts text files
cat_dir = TEMP_DIR / "PROMPTS_BY_CATEGORY"
cat_dir.mkdir(exist_ok=True)

import re

# Parse sections and prompts
categories = [
    ("01_Khuong_Tu_Nha_va_Van_Trong.txt", r"## HẠNG MỤC 1:.*?(?=## HẠNG MỤC 2:|\Z)"),
    ("02_Tuyen_Doi_Dich_va_Gian_Than.txt", r"## HẠNG MỤC 2:.*?(?=## HẠNG MỤC 3:|\Z)"),
    ("03_Tuyen_Tien_Gia_va_Than_Tuong.txt", r"## HẠNG MỤC 3:.*?(?=## HẠNG MỤC 4:|\Z)"),
    ("04_Bao_Vat_va_Phap_Khi.txt", r"## HẠNG MỤC 4:.*?(?=## HẠNG MỤC 5:|\Z)"),
    ("05_Dao_Cu_Explainer_va_Canh_Ket.txt", r"## HẠNG MỤC 5:.*?\Z")
]

csv_rows = [["ID", "Category", "Name_VN", "Scene_Context", "Prompt_English", "Aspect_Ratio"]]

for filename, pattern in categories:
    m = re.search(pattern, content, re.DOTALL)
    if m:
        sec_text = m.group(0).strip()
        (cat_dir / filename).write_text(sec_text, encoding="utf-8")
        
        # Extract individual prompts for CSV
        cat_title = sec_text.split("\n")[0].replace("#", "").strip()
        items = re.findall(r'### (\d+)\. (.*?)\n- \*\*Cảnh:\*\* (.*?)\n- \*\*Prompt:\*\*\s*\n\s*>\s*`(.*?)`', sec_text, re.DOTALL)
        for num, name, context, prompt in items:
            prompt_clean = " ".join(prompt.strip().split())
            ar_match = re.search(r'--ar (\d+:\d+)', prompt_clean)
            ar = ar_match.group(1) if ar_match else "1:1"
            csv_rows.append([num, cat_title, name.strip(), context.strip(), prompt_clean, ar])

# 4. Save CSV
csv_path = TEMP_DIR / "PROMPTS_LIST_EXCEL.csv"
with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(csv_rows)

print(f"Extracted {len(csv_rows) - 1} prompts into CSV.")

# 5. Create ZIP Archive
ZIP_OUTPUT = BASE_DIR / "Bo_54_Prompt_Tao_Hinh_Phong_Than.zip"
with zipfile.ZipFile(ZIP_OUTPUT, "w", zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(TEMP_DIR):
        for file in files:
            file_path = Path(root) / file
            arcname = file_path.relative_to(TEMP_DIR)
            zipf.write(file_path, arcname)

# Also copy a shortcut to outputs/ for convenience
outputs_dir = Path("outputs")
outputs_dir.mkdir(exist_ok=True)
outputs_zip = outputs_dir / "Bo_54_Prompt_Tao_Hinh_Phong_Than.zip"
import shutil
shutil.copy2(ZIP_OUTPUT, outputs_zip)

print(f"Created ZIP file successfully:")
print(f"1. {ZIP_OUTPUT} ({ZIP_OUTPUT.stat().st_size} bytes)")
print(f"2. {outputs_zip} ({outputs_zip.stat().st_size} bytes)")
