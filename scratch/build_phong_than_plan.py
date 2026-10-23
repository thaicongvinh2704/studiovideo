import json
import re
from pathlib import Path

OUT_DIR = Path("projects/mo_den_phong_than/voice_direction")
clean_text = (OUT_DIR / "01_Loi_Ke_Sach.txt").read_text(encoding="utf-8").strip()

# Split into paragraphs
paragraphs = [p.strip() for p in clean_text.split("\n\n") if p.strip()]
print(f"Total paragraphs in clean text: {len(paragraphs)}")

# Read full text to identify section boundaries
full_text = (OUT_DIR / "00_Kich_Ban_Goc_Day_Du.md").read_text(encoding="utf-8")
section_matches = list(re.finditer(r'### (\d+)\. (.*?)\n\n(.*?)(?=\n###|\n---|\Z)', full_text, re.DOTALL))
print(f"Found {len(section_matches)} sections.")

def split_paragraph_into_sentences(p):
    # Regex to split on sentence boundaries (. ? ! ...) keeping the delimiter attached
    # Avoid splitting on abbreviations if any (none in this literary text)
    sentences = re.split(r'(?<=[.!?…])\s+', p)
    sentences = [s.strip() for s in sentences if s.strip()]
    return sentences

# Build semantic units
units = []
unit_id = 1

for sec_idx, match in enumerate(section_matches, start=1):
    sec_num = match.group(1)
    sec_title = match.group(2).strip()
    sec_body = match.group(3).strip()
    sec_paras = [p.strip() for p in sec_body.split("\n\n") if p.strip()]

    for p_idx, p in enumerate(sec_paras, start=1):
        # Determine if paragraph should be split into multiple units
        # If paragraph is short (<= 140 chars) or a single sentence, keep as 1 unit
        s_list = split_paragraph_into_sentences(p)
        
        # If there are multiple sentences and total length > 160 chars, split into sentences
        if len(s_list) > 1 and len(p) > 160:
            chunks = s_list
        else:
            chunks = [p]

        for c_idx, chunk in enumerate(chunks):
            # Design tone and pause based on punctuation and content
            pause_ms = 400
            pace = 1.0
            gain_db = 0.0
            intent = f"Kể tự nhiên, rõ lời (Phần {sec_num}: {sec_title})"
            tone = "tự nhiên, điềm tĩnh"

            # Specific rules for punctuation
            if chunk.endswith("?"):
                pause_ms = 600
                pace = 0.98
                tone = "trăn trở, tò mò, mở rộng suy ngẫm"
                intent = "Câu hỏi tu từ, ngắt nghỉ để người nghe suy ngẫm."
            elif chunk.endswith("…"):
                pause_ms = 550
                pace = 0.97
                tone = "lắng đọng, ngập ngừng, gợi mở"
            elif len(chunk.split()) <= 4:
                # Very short punchy sentence
                pause_ms = 550
                pace = 0.96
                gain_db = 0.2
                tone = "dứt khoát, điểm nhấn kịch tính"
                intent = "Nhịp ngắt kịch tính, ngắn gọn, chắc chắn."
            elif c_idx == len(chunks) - 1 and p_idx == len(sec_paras):
                # End of a section
                pause_ms = 850
                pace = 0.97
                gain_db = 0.1
                tone = "đúc kết, chuyển đoạn"
                intent = "Kết thúc phần, để khoảng lặng chuyển ý."
            elif c_idx == len(chunks) - 1:
                # End of a paragraph
                pause_ms = 500
            else:
                pause_ms = 350

            # Tailor emotional intent by section and keywords
            if "Khương Tử Nha vừa ra lệnh xử chém" in chunk:
                intent = "Mở đầu kịch tính, dứt khoát, gây tò mò."
                pace = 0.98
                gain_db = 0.2
            elif "Khoan đã" in chunk:
                intent = "Dừng lại bất ngờ, kéo người nghe vào nghịch lý."
                pause_ms = 600
                pace = 0.95
                gain_db = 0.3
            elif "Văn Trọng là trụ cột" in chunk:
                intent = "Giới thiệu nhân vật bi tráng của triều Thương."
                pace = 0.99
            elif "Và nhà vua lại yên lòng" in chunk:
                intent = "Giọng chua chát, ngậm ngùi trước sự u mê của Trụ Vương."
                pause_ms = 650
                pace = 0.96
            elif "Thân Công Báo" in chunk and len(chunk.split()) <= 4:
                intent = "Xướng tên nhân vật đối nghịch truyền kiếp."
                pause_ms = 600
                gain_db = 0.3
            elif "Người phong thần đi về đâu" in chunk or "với Khương Tử Nha, có một nỗi ngậm ngùi" in chunk:
                intent = "Giọng trầm buồn, thấu cảm số phận cô đơn của Tử Nha."
                pace = 0.97
            elif "làm mây, làm mưa, nuôi dưỡng vạn vật" in chunk:
                intent = "Câu kết toàn bài, âm hưởng bao la, xúc động, lắng đọng nghìn năm."
                pause_ms = 1100
                pace = 0.95
                gain_db = 0.2

            units.append({
                "id": unit_id,
                "section_num": int(sec_num),
                "section_title": sec_title,
                "source_text": chunk,
                "spoken_text": chunk,
                "intent": intent,
                "tone": tone,
                "pause_ms": pause_ms,
                "pace": pace,
                "gain_db": gain_db
            })
            unit_id += 1

print(f"Generated {len(units)} semantic units.")

# Integrity verification: Concatenation of units must match clean_text
def normalize_spaces(s):
    return re.sub(r'\s+', ' ', s).strip()

source_all = normalize_spaces(" ".join(u["source_text"] for u in units))
clean_all = normalize_spaces(clean_text)

assert source_all == clean_all, "Source text does not match clean text!"
print(f"VERIFICATION PASSED 100%: All {len(clean_all)} characters match exactly!")

plan_data = {
    "title": "Vì sao kẻ địch của Khương Tử Nha vẫn được phong thần?",
    "speaker": "Mỏ Đen · Custom H (nam ~30 tuổi, thông minh, tò mò, khám phá, giàu chất triết lý nhân sinh)",
    "accent": "Bắc",
    "speed_multiplier": 1.25,
    "total_units": len(units),
    "total_sections": len(section_matches),
    "units": units
}

(OUT_DIR / "03_Kich_Ban_Bien_Kich_Dien_Doc.json").write_text(json.dumps(plan_data, ensure_ascii=False, indent=2), encoding="utf-8")
print("Saved 03_Kich_Ban_Bien_Kich_Dien_Doc.json successfully.")
