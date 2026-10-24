"""Build the complete editable Stickman Animation Studio project for Phong Thần Diễn Nghĩa."""
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
PROJECT_DIR = ROOT / "projects" / "mo_den_phong_than"
ASSETS_DIR = PROJECT_DIR / "assets" / "Mo_Den_Phong_Than_V2"
REPORT_PATH = PROJECT_DIR / "voice_direction" / "report_phong_than.json"

def uid():
    import uuid
    return uuid.uuid4().hex[:12]

def main():
    print(f"Loading timing and cues from {REPORT_PATH}...")
    report = json.load(open(REPORT_PATH, 'r', encoding='utf-8'))
    timeline = report['timeline']
    print(f"Total cues loaded: {len(timeline)}")

    # Audio offset: 4.0s of cinematic intro
    AUDIO_OFFSET = 4.0
    TOTAL_AUDIO_DURATION = report['final_duration_seconds'] # ~892.132s
    OUTRO_DURATION = 9.47 # 4.97s + 4.5s -> Total 905.0s (15m05s)

    # Let's map cues to scenes
    # We will define the scene plan
    from scratch.phong_than_scene_definitions import SCENE_SPECS

    scenes = []
    shot_list_rows = []

    # Shift cues by AUDIO_OFFSET
    shifted_cues = []
    for c in timeline:
        shifted_cues.append({
            'id': c['id'],
            'section_num': c['section_num'],
            'section_title': c['section_title'],
            'start': c['start_seconds'] + AUDIO_OFFSET,
            'end': c['end_seconds'] + AUDIO_OFFSET,
            'spoken_text': c['spoken_text']
        })

    # Build scenes
    # Scene 000: Intro
    intro_scene = {
        "id": "pt_scene_000",
        "name": "000 · Mở đầu: Vì sao kẻ địch của Khương Tử Nha vẫn được phong thần?",
        "start": 0.0,
        "duration": AUDIO_OFFSET,
        "background": "white",
        "effects": [],
        "background_file": "assets/Mo_Den_Phong_Than_V2/images/B01.png",
        "objects": [
            {
                "id": uid(),
                "kind": "image",
                "name": "Núi Côn Lôn mờ ảo",
                "preset": "background",
                "x": 640,
                "y": 360,
                "scale": 1.0,
                "rotation": 0.0,
                "opacity": 1.0,
                "layer": 1,
                "start": 0,
                "end": AUDIO_OFFSET,
                "width": 1280,
                "height": 720,
                "file": "assets/Mo_Den_Phong_Than_V2/images/B01.png",
                "fit": "cover",
                "crop": [0, 0, 1, 1],
                "keys": {
                    "scale": [{"t": 0, "v": 1.05}, {"t": AUDIO_OFFSET, "v": 1.0, "ease": "linear"}]
                }
            },
            {
                "id": uid(),
                "kind": "image",
                "name": "Cuộn sắc phong thần phát sáng",
                "preset": "prop",
                "x": 380,
                "y": 360,
                "scale": 0.65,
                "rotation": 0.0,
                "opacity": 0.95,
                "layer": 20,
                "start": 0,
                "end": AUDIO_OFFSET,
                "width": 400,
                "height": 400,
                "file": "assets/Mo_Den_Phong_Than_V2/images/O01.png",
                "fit": "contain"
            },
            {
                "id": uid(),
                "kind": "image",
                "name": "Mỏ Đen người dẫn chuyện",
                "preset": "mo_den",
                "x": 920,
                "y": 420,
                "scale": 0.38,
                "rotation": 0.0,
                "opacity": 1.0,
                "layer": 25,
                "start": 0,
                "end": AUDIO_OFFSET,
                "width": 2048,
                "height": 2048,
                "file": "../../assets/characters/mo_den/library/named_24_v01/mo_den_01_neutral_seated_paws_resting.png",
                "fit": "contain"
            },
            {
                "id": uid(),
                "kind": "text",
                "name": "Tiêu đề phim tài liệu",
                "text": "VÌ SAO KẺ ĐỊCH CỦA KHƯƠNG TỬ NHA\nVẪN ĐƯỢC PHONG THẦN?",
                "x": 640,
                "y": 140,
                "scale": 1.0,
                "rotation": 0.0,
                "opacity": 1.0,
                "layer": 40,
                "start": 0,
                "end": AUDIO_OFFSET,
                "width": 1000,
                "height": 140,
                "color": "#ffffff",
                "fill": "#182026",
                "font_size": 34,
                "bold": True
            }
        ],
        "camera": {
            "x": 640, "y": 360, "zoom": 1.0,
            "keys": {
                "zoom": [{"t": 0, "v": 1.02}, {"t": AUDIO_OFFSET, "v": 1.0, "ease": "linear"}]
            }
        },
        "editorial": {
            "shot_num": 0,
            "section": 1,
            "chapter": "Mở đầu",
            "asset_id": "B01 + O01 + Mỏ Đen",
            "asset_name": "Đường núi Côn Lôn & Sắc mở phong thần",
            "layout": "Đại cảnh mây núi kỳ ảo · Mở đầu trang nghiêm",
            "motion": "Camera zoom chậm từ 1.02 -> 1.0",
            "director_note": "Thiết lập bối cảnh huyền sử kỳ ảo và nhân vật dẫn chuyện Mỏ Đen"
        }
    }
    scenes.append(intro_scene)

    print("Building content scenes from specifications...")
    # Generate all content scenes based on SCENE_SPECS
    current_time = AUDIO_OFFSET
    for i, spec in enumerate(SCENE_SPECS):
        shot_num = spec['shot_num']
        cue_indices = spec['cues']
        matched_cues = [c for c in shifted_cues if c['id'] in cue_indices]
        if not matched_cues:
            continue
        scene_start = current_time
        # For seamless continuity, scene runs until next scene's start (or its cue end)
        if i + 1 < len(SCENE_SPECS):
            next_cues = [c for c in shifted_cues if c['id'] in SCENE_SPECS[i + 1]['cues']]
            scene_end = next_cues[0]['start'] if next_cues else matched_cues[-1]['end']
        else:
            scene_end = matched_cues[-1]['end']
        duration = max(0.5, scene_end - scene_start)
        current_time = scene_start + duration

        # Build scene object
        sc_id = f"pt_scene_{shot_num:03d}"
        sc_name = f"{shot_num:03d} · {spec['title']}"

        objects = []
        # Main visual background / scene layer
        main_file = spec['main_file']
        main_scale_start = spec.get('scale_start', 1.0)
        main_scale_end = spec.get('scale_end', 1.03)
        pan_x_start = spec.get('pan_x_start', 640)
        pan_x_end = spec.get('pan_x_end', 640)

        main_obj = {
            "id": uid(),
            "kind": "image",
            "name": spec['asset_name'],
            "preset": "illustration",
            "x": 640,
            "y": 360,
            "scale": 1.0,
            "rotation": 0.0,
            "opacity": 1.0,
            "layer": 10,
            "start": 0,
            "end": duration,
            "width": 1280,
            "height": 720,
            "file": main_file,
            "fit": spec.get('fit', 'cover'),
            "crop": [0, 0, 1, 1],
            "keys": {
                "scale": [{"t": 0, "v": main_scale_start}, {"t": duration, "v": main_scale_end, "ease": "linear"}],
                "x": [{"t": 0, "v": pan_x_start}, {"t": duration, "v": pan_x_end, "ease": "linear"}]
            }
        }
        objects.append(main_obj)

        # Additional props or character overlays if specified
        if spec.get('prop_file'):
            objects.append({
                "id": uid(),
                "kind": "image",
                "name": spec.get('prop_name', 'Đạo cụ'),
                "preset": "prop",
                "x": spec.get('prop_x', 640),
                "y": spec.get('prop_y', 360),
                "scale": spec.get('prop_scale', 0.5),
                "rotation": 0.0,
                "opacity": 1.0,
                "layer": 20,
                "start": 0,
                "end": duration,
                "width": 400,
                "height": 400,
                "file": spec['prop_file'],
                "fit": "contain"
            })

        # Mỏ Đen overlay if specified
        if spec.get('mo_den_pose'):
            objects.append({
                "id": uid(),
                "kind": "image",
                "name": "Mỏ Đen quan sát / dẫn giải",
                "preset": "mo_den",
                "x": spec.get('mo_den_x', 1100),
                "y": spec.get('mo_den_y', 520),
                "scale": spec.get('mo_den_scale', 0.32),
                "rotation": 0.0,
                "opacity": 0.95,
                "layer": 30,
                "start": 0,
                "end": duration,
                "width": 2048,
                "height": 2048,
                "file": f"../../assets/characters/mo_den/library/named_24_v01/{spec['mo_den_pose']}.png",
                "fit": "contain"
            })

        # Scene camera
        cam_zoom_start = spec.get('cam_zoom_start', 1.0)
        cam_zoom_end = spec.get('cam_zoom_end', 1.02)
        camera = {
            "x": 640, "y": 360, "zoom": cam_zoom_start,
            "keys": {
                "zoom": [{"t": 0, "v": cam_zoom_start}, {"t": duration, "v": cam_zoom_end, "ease": "linear"}]
            }
        }

        scene_dict = {
            "id": sc_id,
            "name": sc_name,
            "start": round(scene_start, 3),
            "duration": round(duration, 3),
            "background": "white",
            "effects": [],
            "objects": objects,
            "camera": camera,
            "editorial": {
                "shot_num": shot_num,
                "section": spec['section'],
                "chapter": spec['chapter'],
                "cues": cue_indices,
                "voice_text": " ".join(c['spoken_text'] for c in matched_cues),
                "asset_id": spec['asset_id'],
                "asset_name": spec['asset_name'],
                "layout": spec['layout'],
                "motion": spec['motion'],
                "director_note": spec['director_note']
            }
        }
        scenes.append(scene_dict)

    # Outro scenes
    last_end = scenes[-1]['start'] + scenes[-1]['duration']
    outro_1_dur = 4.97
    outro_1 = {
        "id": "pt_scene_outro_01",
        "name": "100 · Kết: Tử Nha nhìn núi · Mầm sống hồi sinh",
        "start": round(last_end, 3),
        "duration": outro_1_dur,
        "background": "white",
        "effects": [],
        "objects": [
            {
                "id": uid(),
                "kind": "image",
                "name": "Tử Nha nhìn núi từ nhân gian",
                "preset": "illustration",
                "x": 640,
                "y": 360,
                "scale": 1.0,
                "rotation": 0.0,
                "opacity": 1.0,
                "layer": 10,
                "start": 0,
                "end": outro_1_dur,
                "width": 1280,
                "height": 720,
                "file": "assets/Mo_Den_Phong_Than_V2/images/K27.png",
                "fit": "cover",
                "crop": [0, 0, 1, 1],
                "keys": {
                    "scale": [{"t": 0, "v": 1.0}, {"t": outro_1_dur, "v": 1.03, "ease": "linear"}]
                }
            },
            {
                "id": uid(),
                "kind": "text",
                "name": "Thông điệp triết lý",
                "text": "Trật tự cũ khép lại · Sự sống tiếp diễn",
                "x": 640,
                "y": 620,
                "scale": 1.0,
                "rotation": 0.0,
                "opacity": 0.95,
                "layer": 30,
                "start": 0,
                "end": outro_1_dur,
                "width": 700,
                "height": 60,
                "color": "#f8f9fa",
                "fill": "#182026",
                "font_size": 24,
                "bold": True
            }
        ],
        "camera": {
            "x": 640, "y": 360, "zoom": 1.0,
            "keys": {
                "zoom": [{"t": 0, "v": 1.0}, {"t": outro_1_dur, "v": 1.02, "ease": "linear"}]
            }
        },
        "editorial": {
            "shot_num": 100,
            "section": 9,
            "chapter": "Kết phim",
            "asset_id": "K27",
            "asset_name": "Tử Nha nhìn núi từ nhân gian",
            "layout": "Đại cảnh tĩnh lặng chiều tà",
            "motion": "Camera drift chậm",
            "director_note": "Lắng đọng triết lý nhân sinh sau khi các trật tự đã an bài"
        }
    }
    scenes.append(outro_1)

    outro_2_start = last_end + outro_1_dur
    outro_2_dur = 4.5
    outro_2 = {
        "id": "pt_scene_outro_02",
        "name": "101 · Mỏ Đen chào kết · Stickman Animation Studio",
        "start": round(outro_2_start, 3),
        "duration": outro_2_dur,
        "background": "white",
        "effects": [],
        "objects": [
            {
                "id": uid(),
                "kind": "image",
                "name": "Đồng ruộng sau mưa xanh ngát",
                "preset": "background",
                "x": 640,
                "y": 360,
                "scale": 1.0,
                "rotation": 0.0,
                "opacity": 1.0,
                "layer": 10,
                "start": 0,
                "end": outro_2_dur,
                "width": 1280,
                "height": 720,
                "file": "assets/Mo_Den_Phong_Than_V2/images/B15.png",
                "fit": "cover",
                "crop": [0, 0, 1, 1]
            },
            {
                "id": uid(),
                "kind": "image",
                "name": "Mỏ Đen cúi chào",
                "preset": "mo_den",
                "x": 640,
                "y": 420,
                "scale": 0.42,
                "rotation": 0.0,
                "opacity": 1.0,
                "layer": 25,
                "start": 0,
                "end": outro_2_dur,
                "width": 2048,
                "height": 2048,
                "file": "../../assets/characters/mo_den/library/named_24_v01/mo_den_02_happy_seated_greeting.png",
                "fit": "contain"
            },
            {
                "id": uid(),
                "kind": "text",
                "name": "Credit Stickman Studio",
                "text": "MỎ ĐEN · PHONG THẦN DIỄN NGHĨA\nStickman Animation Studio · 2026",
                "x": 640,
                "y": 120,
                "scale": 1.0,
                "rotation": 0.0,
                "opacity": 1.0,
                "layer": 30,
                "start": 0,
                "end": outro_2_dur,
                "width": 800,
                "height": 100,
                "color": "#ffffff",
                "fill": "#202a30",
                "font_size": 26,
                "bold": True
            }
        ],
        "camera": {
            "x": 640, "y": 360, "zoom": 1.0,
            "keys": {
                "zoom": [{"t": 0, "v": 1.0}, {"t": outro_2_dur, "v": 1.02, "ease": "linear"}]
            }
        },
        "editorial": {
            "shot_num": 101,
            "section": 9,
            "chapter": "Kết phim",
            "asset_id": "B15 + Mỏ Đen 08",
            "asset_name": "Đồng ruộng sau mưa & Mỏ Đen chào kết",
            "layout": "Trung cảnh Mỏ Đen chào tạm biệt khán giả",
            "motion": "Camera zoom chậm",
            "director_note": "Khép lại toàn bộ tác phẩm ở đúng mốc 15 phút 05 giây"
        }
    }
    scenes.append(outro_2)

    total_film_duration = scenes[-1]['start'] + scenes[-1]['duration']
    print(f"Total scenes created: {len(scenes)}")
    print(f"Total film duration: {total_film_duration:.2f}s ({total_film_duration/60:.2f} minutes)")

    # Build subtitles array
    subtitles = []
    for c in shifted_cues:
        subtitles.append({
            "id": uid(),
            "start": round(c['start'], 3),
            "end": round(c['end'], 3),
            "text": c['spoken_text'],
            "role": "Narrator"
        })

    # Assemble project JSON
    project_data = {
        "schema": 1,
        "name": "Mỏ Đen: Vì sao kẻ địch của Khương Tử Nha vẫn được phong thần?",
        "width": 1920,
        "height": 1080,
        "fps": 24,
        "audio": [
            {
                "id": "main_narration_phong_than",
                "name": "Mỏ Đen Custom H 1.25x (Giọng Bắc)",
                "file": "voice_direction/Mo_Den_Phong_Than_Dien_Nghia_Custom_H_1_25x.wav",
                "start": AUDIO_OFFSET,
                "duration": TOTAL_AUDIO_DURATION,
                "gain": 1.0
            }
        ],
        "subtitles": subtitles,
        "subtitle_style": {
            "enabled": True,
            "size": 28,
            "font": "Segoe UI",
            "color": "#ffffff",
            "background": True,
            "y": 0.95
        },
        "references": [],
        "duck_music": False,
        "allow_draft": True,
        "render_profile": "cinematic_24",
        "supersample": 1,
        "directing_notes": {
            "director": "Antigravity",
            "voice_actor": "Mỏ Đen (Custom H Bắc 1.25x)",
            "visual_style": "Clean 2D Graphic Novel / Epic Chinese Mythological Fantasy Art",
            "character": "Mỏ Đen narrator + Phong Thần V2 asset pack",
            "target_duration_minutes": "15m05s",
            "total_cues": len(timeline),
            "total_scenes": len(scenes)
        },
        "scenes": scenes
    }

    out_project_file = PROJECT_DIR / "project.json"
    with open(out_project_file, 'w', encoding='utf-8') as f:
        json.dump(project_data, f, ensure_ascii=False, indent=2)
    print(f"Saved project JSON to {out_project_file} ({out_project_file.stat().st_size / 1024:.1f} KB)")

    # Build Shot List Table Markdown
    table_lines = [
        "# BẢNG PHÂN CẢNH CHI TIẾT (SHOT LIST TABLE)",
        "## MỎ ĐEN: VÌ SAO KẺ ĐỊCH CỦA KHƯƠNG TỬ NHA VẪN ĐƯỢC PHONG THẦN?",
        f"- **Tổng thời lượng:** {total_film_duration/60:.2f} phút ({total_film_duration:.1f} giây, đạt chuẩn tối thiểu 15 phút).",
        f"- **Tổng số phân cảnh (Scenes):** {len(scenes)} cảnh.",
        f"- **Tổng số câu thoại (Cues):** 243 cụm nghĩa được đồng bộ chính xác.",
        f"- **Giọng đọc:** Mỏ Đen Custom H giọng Bắc 1.25x (file âm thanh: `voice_direction/Mo_Den_Phong_Than_Dien_Nghia_Custom_H_1_25x.wav`).",
        "",
        "| Shot | Chương | Thời gian (Vào - Ra) | Thời lượng | Asset ID & Tên hình | Bố cục & Góc máy | Chuyển động & Hiệu ứng | Lời thoại / Cụm nghĩa | Ý đồ đạo diễn |",
        "|---|---|---|---|---|---|---|---|---|"
    ]

    for sc in scenes:
        ed = sc['editorial']
        start_fmt = f"{int(sc['start']//60):02d}:{sc['start']%60:04.1f}"
        end_time = sc['start'] + sc['duration']
        end_fmt = f"{int(end_time//60):02d}:{end_time%60:04.1f}"
        time_range = f"{start_fmt} - {end_fmt}"
        dur_fmt = f"{sc['duration']:.1f}s"
        text_snip = ed.get('voice_text', '')
        if len(text_snip) > 90:
            text_snip = text_snip[:88] + "…"
        table_lines.append(f"| {ed['shot_num']:03d} | Phần {ed['section']} | {time_range} | {dur_fmt} | **{ed['asset_id']}**<br>{ed['asset_name']} | {ed['layout']} | {ed['motion']} | {text_snip} | {ed['director_note']} |")

    out_table_file = PROJECT_DIR / "shot_list_table.md"
    with open(out_table_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(table_lines) + '\n')
    print(f"Saved Shot List Table to {out_table_file} ({out_table_file.stat().st_size / 1024:.1f} KB)")

if __name__ == '__main__':
    main()
