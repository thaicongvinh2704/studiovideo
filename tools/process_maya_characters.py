"""Process generated Maya characters: transparent background and indexing for reuse."""
import json
from pathlib import Path
from PIL import Image, ImageFilter
import numpy as np

ARTIFACT_DIR = Path(r"C:\Users\thaii\.gemini\antigravity\brain\a41f0f2b-4806-47bc-ac21-b024ddef65d0")
ROOT = Path(__file__).resolve().parents[1]

TARGET_DIRS = [
    ROOT / "projects" / "mo_den_maya" / "assets" / "characters" / "maya_people",
    ROOT / "assets" / "characters" / "maya_people"
]

IMAGES = [
    ("maya_farmer_man_1792589907192.jpg", "maya_01_farmer_man.png", "Người nông dân Maya (cầm cuốc/nông cụ)", "SC15, SC16 (Đợt hạn hán 13 năm, mùa màng, đời sống nông nghiệp)"),
    ("maya_weaver_woman_1792589932188.jpg", "maya_02_weaver_woman.png", "Người phụ nữ Maya (áo Huipil, cầm bát đất nung)", "SC02, SC25, SC29, SC34 (Đời sống gia đình, dệt vải, di cư)"),
    ("maya_water_bearer_1792589959519.jpg", "maya_03_water_bearer.png", "Người đi lấy nước Maya (ôm bình gốm Olla)", "SC01, SC05, SC06, SC08, SC11, SC12 (Nguồn nước, hồ chứa Tikal, chia sẻ nước)"),
    ("maya_noble_priest_1792589990751.jpg", "maya_04_noble_priest.png", "Tư tế / Thủ lĩnh tri thức Maya (mũ lông vũ, chỉ tay, cầm sách giấy gấp)", "SC03, SC04, SC20, SC21, SC23, SC24 (Thiên văn, chữ viết, giới quyền lực)"),
    ("maya_drought_farmer_1792590559083.jpg", "maya_05_drought_farmer.png", "Nông dân tuyệt vọng ôm trán bên ruộng bắp khô héo", "SC15, SC16, SC17 (Hạn hán kỷ lục 13 năm, mùa màng thất bát, bế tắc sinh kế)"),
    ("maya_migrant_family_1792590625222.jpg", "maya_06_migrant_family.png", "Gia đình Maya di cư rời bỏ kinh đô (cha mang gùi dắt con, mẹ mang tay nải đượm buồn)", "SC02, SC25, SC29, SC33, SC34 (Cuộc rời bỏ quy mô lớn, gia đình bồng bế nhau đi tìm sự sống)"),
    ("maya_exhausted_water_1792590655607.jpg", "maya_07_exhausted_water.png", "Dân làng kiệt sức quỳ bên bình gốm cạn trơ đáy, gạt mồ hôi nhìn trời cầu mưa", "SC01, SC08, SC11, SC12 (Khủng hoảng thiếu nước ngọt, chia khẩu phần cạn kiệt, thiên nhiên khắc nghiệt)"),
    ("maya_dilemma_choice_1792590686241.jpg", "maya_08_dilemma_choice.png", "Ngã rẽ sinh tử: Ra đi hay ở lại? (Một người khóc ngoái nhìn cố hương, một người chỉ về chân trời mới)", "SC02, SC25, SC30, SC31 (Giằng xé nội tâm đau đớn trước quyết định bỏ lại di sản ngàn năm)")
]


def make_transparent(img_path):
    im = Image.open(img_path).convert("RGBA")
    arr = np.array(im)
    r, g, b, a = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2], arr[:, :, 3]

    # White mask
    is_white = (r > 240) & (g > 240) & (b > 240)
    
    # Flood fill from edges to only remove outside white, not clothes
    from collections import deque
    h, w = is_white.shape
    visited = np.zeros((h, w), dtype=bool)
    queue = deque()

    # Add border pixels that are white
    for y in range(h):
        for x in (0, w - 1):
            if is_white[y, x] and not visited[y, x]:
                visited[y, x] = True
                queue.append((y, x))
    for x in range(w):
        for y in (0, h - 1):
            if is_white[y, x] and not visited[y, x]:
                visited[y, x] = True
                queue.append((y, x))

    # BFS
    while queue:
        cy, cx = queue.popleft()
        for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            ny, nx = cy + dy, cx + dx
            if 0 <= ny < h and 0 <= nx < w and not visited[ny, nx]:
                if is_white[ny, nx]:
                    visited[ny, nx] = True
                    queue.append((ny, nx))

    # Apply alpha: outside visited white becomes transparent
    # Smooth edges slightly
    alpha_channel = np.where(visited, 0, 255).astype(np.uint8)
    
    # Soften transition on border
    mask_im = Image.fromarray(alpha_channel, mode='L')
    mask_im = mask_im.filter(ImageFilter.BoxBlur(0.8))
    
    im.putalpha(mask_im)
    return im


def main():
    for d in TARGET_DIRS:
        d.mkdir(parents=True, exist_ok=True)

    manifest_entries = []

    for src_name, dst_name, title, suggested_scenes in IMAGES:
        src_path = ARTIFACT_DIR / src_name
        if not src_path.exists():
            print(f"File not found: {src_path}")
            continue

        im = make_transparent(src_path)
        
        for d in TARGET_DIRS:
            out_file = d / dst_name
            im.save(out_file, format="PNG")
            print(f"Saved: {out_file} ({im.size[0]}x{im.size[1]})")

        manifest_entries.append({
            "file": dst_name,
            "title": title,
            "suggested_scenes": suggested_scenes,
            "size": list(im.size),
            "format": "PNG",
            "alpha": True,
            "style": "2D hand-drawn explainer cartoon (explainer-reference-v1 compatible)"
        })

    for d in TARGET_DIRS:
        manifest_path = d / "manifest.json"
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump({
                "collection": "Maya Ancient People Cartoon Illustrations",
                "version": 1,
                "created_at": "2026-10-21",
                "style_compliance": "Matches explainer_reference_v1 line weight and flat palette",
                "characters": manifest_entries
            }, f, ensure_ascii=False, indent=2)
        print(f"Manifest written to: {manifest_path}")

    print("All Maya characters successfully processed!")


if __name__ == "__main__":
    main()
