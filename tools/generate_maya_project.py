"""Script to generate the complete Maya documentary project.json with directed visuals, audio and subtitles."""
import json
import re
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from studio.project import uid, validate

PROJECT_DIR = ROOT / 'projects' / 'mo_den_maya'

# Emotional pose mapping for Mỏ Đen
EMOTIONS = {
    'neutral': 'mo_den_01_neutral_seated_paws_resting.png',
    'greeting': 'mo_den_02_happy_seated_greeting.png',
    'thinking': 'mo_den_15_thinking_seated_chin_rest.png',
    'curious': 'mo_den_13_curious_seated_paw_near_chin.png',
    'explaining': 'mo_den_24_explaining_seated_open_paw_gesture.png',
    'skeptical': 'mo_den_14_skeptical_seated_arms_crossed.png',
    'shocked': 'mo_den_06_shocked_seated_paws_raised.png',
    'worried': 'mo_den_07_worried_seated_paws_clasped.png',
    'realization': 'mo_den_16_realization_seated_paw_raised.png',
    'smug': 'mo_den_08_smug_seated_one_paw_shrug.png'
}

SCENE_META = {
    'SC01': ('TIKAL, GUATEMALA', 'BẮT ĐẦU HỒ SƠ MAYA: HỆ THỐNG TRỮ NƯỚC', 'R01_Tikal_forest.jpg', 'G03_Nuoc_Tikal.png', 'neutral', 'curious'),
    'SC02': ('BỐI CẢNH LỊCH SỬ', 'GÓC NHÌN NGƯỜI DÂN TRONG SỰ SUY TÀN', '172_nha_va_san_sinh_hoat.png', '173_nha_va_san_chuan_bi_roi_di.png', 'thinking', 'thinking'),
    'SC03': ('BẢN ĐỒ THÀNH BANG', '250 – 900 SCN: THỜI KỲ CỔ ĐIỂN', 'G01_Ban_do.png', 'G02_Truc_thoi_gian.png', 'explaining', 'explaining'),
    'SC04': ('TOÁN HỌC & THIÊN VĂN', 'CHỮ VIẾT, HỆ ĐẾM & LỊCH THIÊN VĂN', 'G10_Chu_viet_Thien_van.png', '151_do_thi_duoc_duy_tri.png', 'skeptical', 'explaining'),
    'SC05': ('DI TÍCH TIKAL', 'RỜI ĐỈNH ĐỀN, XUỐNG NƠI LẤY NƯỚC', 'R02_Tikal_Temple_I.jpg', '157_ho_chua_day_nuoc.png', 'curious', 'curious'),
    'SC06': ('HỒNG NGỌC GUATEMALA', 'TIKAL: HỒ CHỨA, ĐẬP & KÊNH DẪN NƯỚC', 'R01_Tikal_forest.jpg', 'G03_Nuoc_Tikal.png', 'explaining', 'explaining'),
    'SC07': ('HỒ CORRIENTAL', 'PHÁT HIỆN HỆ THỐNG LỌC BẰNG ZEOLITE', 'E03_zeolite_fig3.jpg', 'E03_zeolite_fig4.jpg', 'realization', 'realization'),
    'SC08': ('ĐÁNH GIÁ NGUỒN NƯỚC', 'GIỚI HẠN CỦA HỆ THỐNG TRỮ NƯỚC TIKAL', '158_ho_chua_nuoc_thap.png', '159_ho_chua_gan_can.png', 'thinking', 'worried'),
    'SC09': ('CÂU HỎI NGHIÊN CỨU', 'HẠN HÁN HAY CHẤT LƯỢNG NƯỚC UỐNG?', '159_ho_chua_gan_can.png', 'G12_O_nhiem_thuy_ngan_Tikal.png', 'skeptical', 'skeptical'),
    'SC10': ('DỮ LIỆU ĐÁY HỒ TIKAL', 'Ô NHIỄM THỦY NGÂN CHU SA & ĐỘC TỐ', 'E06_pollution_fig4.jpg', 'G12_O_nhiem_thuy_ngan_Tikal.png', 'shocked', 'shocked'),
    'SC11': ('HIỂM HỌA KÉP', 'NGUỒN NƯỚC ÍT ĐI VÀ KHÔNG CÒN AN TOÀN', 'G03_Nuoc_Tikal.png', '159_ho_chua_gan_can.png', 'worried', 'worried'),
    'SC12': ('SỨC ÉP XÃ HỘI', 'SỰ THỎA THUẬN VÀ CHIA SẺ NGUỒN NƯỚC', '169_duong_noi_thong_suot.png', '170_duong_noi_hu_hai.png', 'thinking', 'thinking'),
    'SC13': ('KHÍ HẬU CỔ ĐẠI', 'TRẦM TÍCH, KHOÁNG VẬT & MĂNG ĐÁ', 'E02_Witzna_cores.jpg', 'E07_drought2025_fig2.jpg', 'curious', 'curious'),
    'SC14': ('HỒ CHICHANCANAB', 'KẾT QUẢ 2018: LƯỢNG MƯA GIẢM 41% – 54%', 'G04_Mua_41_54.png', '163_ruong_ngo_xanh_tot.png', 'explaining', 'explaining'),
    'SC15': ('TÂY BẮC YUCATÁN', 'NGHIÊN CỨU 2025: ĐỢT HẠN HÁN KÉO DÀI 13 NĂM', 'G05_13_nam.png', '164_ruong_ngo_heo.png', 'worried', 'worried'),
    'SC16': ('ĐỜI SỐNG NÔNG NGHIỆP', '13 NĂM QUA ĐỜI MỘT THẾ HỆ', '165_ruong_ngo_that_mua.png', '167_kho_luong_con_it.png', 'thinking', 'worried'),
    'SC17': ('MỞ RỘNG ĐỊA BÀN', 'TÌM KIẾM CÁC THÀNH PHỐ NGOẠI LỆ', 'G01_Ban_do.png', 'G06_Itzan.png', 'curious', 'curious'),
    'SC18': ('HỒ ITZAN, GUATEMALA', 'DÂN SỐ GIẢM NHƯNG KHÔNG CÓ DẤU VẾT HẠN', 'E08_Itzan_fig3.png', 'G06_Itzan.png', 'realization', 'realization'),
    'SC19': ('LIÊN KẾT LIÊN VÙNG', 'SỰ ĐỔ VỠ MẠNG LƯỚI THƯƠNG MẠI', '154_cho_du_hang.png', '155_cho_it_hang.png', 'explaining', 'thinking'),
    'SC20': ('WITZNA · NĂM 697 SCN', 'DẤU TÍCH ĐÁM CHÁY & CUỘC CHIẾN TÀN KHỐC', 'E01_Witzna_charcoal.png', '175_khu_chay_nguyen_ven.png', 'shocked', 'shocked'),
    'SC21': ('THỜI ĐIỂM SỰ KIỆN', 'CHIẾN TRANH XẢY RA TRƯỚC ĐẠI HẠN HÁN', '176_khu_chay_chay_hu_hai.png', 'G07_Witzna.png', 'skeptical', 'skeptical'),
    'SC22': ('HẬU QUẢ XUNG ĐỘT', 'SỰ PHỤC HỒI DÂN SỐ BỊ TRIỆT TIÊU', '177_khu_chay_dau_tich.png', '152_do_thi_xuong_cap.png', 'worried', 'worried'),
    'SC23': ('VĂN KHẮC & BIA ĐÁ', 'TIẾNG NÓI CỦA BÊN THẮNG TRẬN', 'R07_Tikal_stele.jpg', 'G08_Chinh_tri_Doi_song.png', 'thinking', 'thinking'),
    'SC24': ('TẦNG LỚP THƯỢNG LƯU', 'GIỚI QUYỀN LỰC VÀ ĐỜI SỐNG DÂN THƯỜNG', '178_quyen_luc_duoc_duy_tri.png', '179_quyen_luc_suy_yeu.png', 'curious', 'curious'),
    'SC25': ('DI CƯ TỰ NHIÊN', 'LÀN SÓNG RỜI ĐI ÂM THẦM CỦA CÁC GIA ĐÌNH', '173_nha_va_san_chuan_bi_roi_di.png', '174_nha_va_san_bo_trong.png', 'thinking', 'thinking'),
    'SC26': ('DÒNG CHẢY LỊCH SỬ', 'CHICHÉN ITZÁ: TRUNG TÂM PHÍA BẮC PHỒN VINH', 'R05_Chichen_Itza.jpg', 'G02_Truc_thoi_gian.png', 'explaining', 'explaining'),
    'SC27': ('THỜI KỲ HẬU CỔ ĐIỂN', 'MAYAPÁN: NỀN QUẢN TRỊ LIÊN MINH', 'R04_Mayapan_panorama.jpg', 'G02_Truc_thoi_gian.png', 'explaining', 'realization'),
    'SC28': ('THẾ KỶ 16', 'CUỘC CHINH PHỤC CỦA TÂY BAN NHA', 'G09_Chinh_phuc_TBN_1697.png', 'G02_Truc_thoi_gian.png', 'thinking', 'thinking'),
    'SC29': ('HẬU DUỆ MAYA', 'HÀNG TRIỆU NGƯỜI MAYA VẪN ĐANG SỐNG', 'R03_Tzutujil_weaving_2019.jpg', 'R06_Mayan_weaver_2023.jpg', 'greeting', 'greeting'),
    'SC30': ('Ý NGHĨA QUÁ KHỨ', 'CUỘC SỐNG ĐÃ TIẾP NỐI THAY VÌ BIẾN MẤT', 'R02_Tikal_Temple_I.jpg', 'R06_Mayan_weaver_2023.jpg', 'thinking', 'thinking'),
    'SC31': ('GIẢI MÃ HIỂU NHẦM', 'CHU KỲ LỊCH MAYA KHÔNG PHẢI TẬN THẾ', 'G11_Lich_Maya_vs_Lich_ban.png', 'G02_Truc_thoi_gian.png', 'smug', 'explaining'),
    'SC32': ('TỔNG HÒA NGUYÊN NHÂN', 'TỔNG HỢP: NƯỚC, HẠN, CHIẾN TRANH & KINH TẾ', 'G03_Nuoc_Tikal.png', 'G07_Witzna.png', 'explaining', 'explaining'),
    'SC33': ('GÓC NHÌN CON NGƯỜI', 'ÁP LỰC CUỘC SỐNG TỪNG NGÀY TRONG LỊCH SỬ', '172_nha_va_san_sinh_hoat.png', '173_nha_va_san_chuan_bi_roi_di.png', 'thinking', 'thinking'),
    'SC34': ('LỰA CHỌN KHẮC NGHIỆT', 'Ở LẠI GIỮ ĐẤT HAY RA ĐI TÌM TƯƠNG LAI', '174_nha_va_san_bo_trong.png', 'R01_Tikal_forest.jpg', 'worried', 'worried'),
    'SC35': ('LỊCH SỬ SỐNG ĐỘNG', 'LỊCH SỬ NẰM Ở CON NGƯỜI, KHÔNG CHỈ Ở ĐÁ', 'R06_Mayan_weaver_2023.jpg', 'R03_Tzutujil_weaving_2019.jpg', 'realization', 'greeting'),
    'SC36': ('KẾT THÚC HỒ SƠ', 'CẢM ƠN BẠN ĐÃ LẮNG NGHE · MỎ ĐEN', 'R01_Tikal_forest.jpg', 'R05_Chichen_Itza.jpg', 'greeting', 'greeting')
}


def parse_srt(path):
    text = Path(path).read_text(encoding='utf-8')
    entries = []
    pattern = re.compile(r'(\d+)\s*\n(\d{2}:\d{2}:\d{2}[,\.]\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}[,\.]\d{3})\s*\n(.*?)(?=\n\s*\n|\Z)', re.DOTALL)
    for m in pattern.finditer(text):
        idx, start_str, end_str, content = m.groups()
        def to_sec(s):
            s = s.replace(',', '.')
            h, m, sec = s.split(':')
            return int(h) * 3600 + int(m) * 60 + float(sec)
        entries.append({
            'id': uid(),
            'start': to_sec(start_str),
            'end': to_sec(end_str),
            'text': content.strip().replace('\n', ' ')
        })
    return entries


def main():
    print('Generating Maya video project...')
    # Load timing units
    with open(PROJECT_DIR / 'voice_direction/full_narration_custom_H_125/timeline_full.json', encoding='utf-8') as f:
        timeline = json.load(f)['units']

    cue_time = {}
    for u in timeline:
        for c in u['source_cue_ids']:
            cue_time[c] = (u['final_start_seconds'], u['final_end_seconds'])

    # Load shot list
    with open(PROJECT_DIR / 'source_materials/Mo_Den_Maya_Tu_Lieu_That_Va_Phan_Canh_v1/03_Phan_canh/SHOT_LIST_72_CANH.json', encoding='utf-8') as f:
        shots_data = json.load(f)['shots']

    # Group shots into 36 scenes
    scenes_dict = {}
    for s in shots_data:
        sc_id = s['scene_id']
        if sc_id not in scenes_dict:
            scenes_dict[sc_id] = []
        scenes_dict[sc_id].append(s)

    project_scenes = []
    current_time = 0.0

    scene_keys = sorted(scenes_dict.keys(), key=lambda x: int(x.replace('SC', '')))

    for i, sc_id in enumerate(scene_keys):
        shots = scenes_dict[sc_id]
        # Calculate start and end
        shot_cues = []
        for sh in shots:
            shot_cues.extend(sh['source_cue_ids'])
        starts = [cue_time[c][0] for c in shot_cues if c in cue_time]
        ends = [cue_time[c][1] for c in shot_cues if c in cue_time]
        
        sc_start = min(starts) if starts else current_time
        sc_end = max(ends) if ends else (sc_start + 20.0)
        
        # Ensure continuity
        if sc_start < current_time:
            sc_start = current_time
        duration = max(1.0, sc_end - sc_start)
        
        meta = SCENE_META.get(sc_id, ('VĂN MINH MAYA', 'HỒ SƠ KHẢO CỔ HỌC', 'R01_Tikal_forest.jpg', 'R01_Tikal_forest.jpg', 'neutral', 'neutral'))
        badge_tag, title_text, bg1, bg2, pose1, pose2 = meta
        
        # Determine half-duration for 2 shots per scene
        half_dur = duration / len(shots) if len(shots) > 0 else duration
        
        scene_objects = []
        
        # Build objects for shot 1
        sh1_end = half_dur
        bg1_file = f'assets/media/{bg1}'
        pose1_file = f'assets/mo_den/{EMOTIONS[pose1]}'
        
        # 1. Background Shot 1
        scene_objects.append({
            'id': uid(),
            'kind': 'image',
            'name': f'BG_{sc_id}_1',
            'preset': 'background',
            'x': 640,
            'y': 360,
            'scale': 1.0,
            'rotation': 0.0,
            'opacity': 1.0,
            'layer': 10,
            'start': 0.0,
            'end': sh1_end,
            'width': 1280,
            'height': 720,
            'file': bg1_file,
            'fit': 'cover',
            'keys': {
                'scale': [{'t': 0.0, 'v': 1.0, 'ease': 'linear'}, {'t': sh1_end, 'v': 1.05, 'ease': 'linear'}]
            }
        })
        
        # 2. Presenter Mascot Shot 1 (Bottom Right)
        scene_objects.append({
            'id': uid(),
            'kind': 'image',
            'name': f'Presenter_{sc_id}_1',
            'preset': 'mascot',
            'x': 1110,
            'y': 550,
            'scale': 1.0,
            'rotation': 0.0,
            'opacity': 1.0,
            'layer': 40,
            'start': 0.0,
            'end': sh1_end,
            'width': 300,
            'height': 300,
            'file': pose1_file,
            'fit': 'contain'
        })
        
        # Build objects for shot 2 (if present)
        if len(shots) > 1:
            bg2_file = f'assets/media/{bg2}'
            pose2_file = f'assets/mo_den/{EMOTIONS[pose2]}'
            
            # Background Shot 2
            scene_objects.append({
                'id': uid(),
                'kind': 'image',
                'name': f'BG_{sc_id}_2',
                'preset': 'background',
                'x': 640,
                'y': 360,
                'scale': 1.0,
                'rotation': 0.0,
                'opacity': 1.0,
                'layer': 10,
                'start': sh1_end,
                'end': duration,
                'width': 1280,
                'height': 720,
                'file': bg2_file,
                'fit': 'cover',
                'keys': {
                    'scale': [{'t': sh1_end, 'v': 1.04, 'ease': 'linear'}, {'t': duration, 'v': 1.0, 'ease': 'linear'}]
                }
            })
            
            # Presenter Mascot Shot 2
            scene_objects.append({
                'id': uid(),
                'kind': 'image',
                'name': f'Presenter_{sc_id}_2',
                'preset': 'mascot',
                'x': 1110,
                'y': 550,
                'scale': 1.0,
                'rotation': 0.0,
                'opacity': 1.0,
                'layer': 40,
                'start': sh1_end,
                'end': duration,
                'width': 300,
                'height': 300,
                'file': pose2_file,
                'fit': 'contain'
            })
            
        # Maya Historical Human Illustration (Left / Mid-Left)
        maya_people_scenes = {
            'SC01': ('maya_03_water_bearer.png', 310, 510, 310, 310),
            'SC02': ('maya_08_dilemma_choice.png', 330, 490, 360, 360),
            'SC03': ('maya_04_noble_priest.png', 300, 490, 330, 330),
            'SC04': ('maya_04_noble_priest.png', 300, 490, 330, 330),
            'SC05': ('maya_03_water_bearer.png', 310, 510, 310, 310),
            'SC06': ('maya_03_water_bearer.png', 310, 510, 310, 310),
            'SC08': ('maya_07_exhausted_water.png', 320, 510, 330, 330),
            'SC09': ('maya_07_exhausted_water.png', 320, 510, 330, 330),
            'SC11': ('maya_07_exhausted_water.png', 320, 510, 330, 330),
            'SC12': ('maya_01_farmer_man.png', 310, 510, 310, 310),
            'SC14': ('maya_01_farmer_man.png', 310, 510, 310, 310),
            'SC15': ('maya_05_drought_farmer.png', 320, 500, 330, 330),
            'SC16': ('maya_05_drought_farmer.png', 320, 500, 330, 330),
            'SC17': ('maya_05_drought_farmer.png', 320, 500, 330, 330),
            'SC20': ('maya_04_noble_priest.png', 300, 490, 330, 330),
            'SC22': ('maya_08_dilemma_choice.png', 330, 490, 360, 360),
            'SC23': ('maya_04_noble_priest.png', 300, 490, 330, 330),
            'SC24': ('maya_04_noble_priest.png', 300, 490, 330, 330),
            'SC25': ('maya_06_migrant_family.png', 330, 490, 360, 360),
            'SC29': ('maya_02_weaver_woman.png', 310, 510, 300, 300),
            'SC30': ('maya_08_dilemma_choice.png', 330, 490, 360, 360),
            'SC33': ('maya_06_migrant_family.png', 330, 490, 360, 360),
            'SC34': ('maya_06_migrant_family.png', 330, 490, 360, 360),
            'SC35': ('maya_02_weaver_woman.png', 310, 510, 300, 300),
        }
        if sc_id in maya_people_scenes:
            mp_file, mpx, mpy, mpw, mph = maya_people_scenes[sc_id]
            scene_objects.append({
                'id': uid(),
                'kind': 'image',
                'name': f'MayaFigure_{sc_id}',
                'preset': 'maya_character',
                'x': mpx,
                'y': mpy,
                'width': mpw,
                'height': mph,
                'file': f'assets/characters/maya_people/{mp_file}',
                'fit': 'contain',
                'scale': 1.0,
                'rotation': 0.0,
                'opacity': 1.0,
                'layer': 35,
                'start': 0.0,
                'end': duration
            })
            
        # 3. Informative Topic Badge (Top Left Corner)
        # Background card
        scene_objects.append({
            'id': uid(),
            'kind': 'shape',
            'name': 'Badge_Card',
            'preset': 'badge_card',
            'shape': 'card',
            'x': 260,
            'y': 52,
            'width': 470,
            'height': 56,
            'fill': '#10161cf0',
            'color': '#3ea494',
            'stroke': 2,
            'layer': 50,
            'start': 0.0,
            'end': duration,
            'scale': 1.0,
            'rotation': 0.0,
            'opacity': 0.95
        })
        # Tag text
        scene_objects.append({
            'id': uid(),
            'kind': 'text',
            'name': 'Badge_Tag',
            'preset': 'text',
            'x': 260,
            'y': 40,
            'width': 450,
            'height': 20,
            'text': badge_tag,
            'font_size': 11,
            'font': 'Segoe UI',
            'color': '#4fe0cb',
            'bold': True,
            'align': 'left',
            'layer': 52,
            'start': 0.0,
            'end': duration,
            'scale': 1.0,
            'rotation': 0.0,
            'opacity': 1.0
        })
        # Title text
        scene_objects.append({
            'id': uid(),
            'kind': 'text',
            'name': 'Badge_Title',
            'preset': 'text',
            'x': 260,
            'y': 62,
            'width': 450,
            'height': 24,
            'text': title_text,
            'font_size': 14,
            'font': 'Segoe UI',
            'color': '#ffffff',
            'bold': True,
            'align': 'left',
            'layer': 52,
            'start': 0.0,
            'end': duration,
            'scale': 1.0,
            'rotation': 0.0,
            'opacity': 1.0
        })

        scene_dict = {
            'id': uid(),
            'name': f'{sc_id} · {badge_tag}',
            'start': sc_start,
            'duration': duration,
            'background': 'white',
            'background_color': '#11171d',
            'objects': scene_objects,
            'effects': [],
            'camera': {'keys': {}, 'follow': ''},
            'subtitle_ids': [],
            'audio_ids': []
        }
        
        project_scenes.append(scene_dict)
        current_time = sc_start + duration

    # Parse subtitles
    subtitles = parse_srt(PROJECT_DIR / 'assets/subtitles.srt')

    # Construct the project document
    project = {
        'schema': 1,
        'name': 'Mỏ Đen · Mở lại hồ sơ văn minh Maya',
        'width': 1920,
        'height': 1080,
        'fps': 24,
        'scenes': project_scenes,
        'subtitles': subtitles,
        'audio': [{
            'id': 'narration_full',
            'name': 'Giọng kể Mỏ Đen (Custom H 1.25x)',
            'file': 'assets/audio/narration.wav',
            'start': 0.0,
            'duration': current_time,
            'group': 'voice',
            'volume': 1.0,
            'fade_in': 0.1,
            'fade_out': 0.5
        }],
        'references': [],
        'subtitle_style': {
            'enabled': True,
            'size': 26,
            'font': 'Segoe UI',
            'color': '#ffffff',
            'background': True,
            'y': 0.92
        },
        'duck_music': True,
        'allow_draft': True
    }

    validate(project)

    output_path = PROJECT_DIR / 'project.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(project, f, ensure_ascii=False, indent=2)

    print(f'Successfully generated Maya project at: {output_path}')
    print(f'Total Scenes: {len(project_scenes)}, Total Duration: {current_time:.2f}s, Subtitle Cues: {len(subtitles)}')


if __name__ == '__main__':
    main()
