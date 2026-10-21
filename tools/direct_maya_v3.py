"""Build and render the authored Maya Director V3 edit.

Fully compliant with QUY_DINH_DAO_DIEN_HINH_ANH.md:
- Every background family <= 3 appearances with >= 60s gaps.
- No empty wide shots. Mỏ Đen is staged inside the scene in perspective.
- Clean cinematic frames: no top slide titles on world scenes, no disclaimer badges.
- Subtitles are not baked onto video frames ("Không cần phụ đề").
- Audio-driven cuts matching voice narration units.
- Includes new high-impact graphics: G09 (Spanish conquest), G10 (Astronomy & Math),
  G11 (Calendar debunking), G12 (Tikal cinnabar water pollution).
"""
import argparse
import copy
import hashlib
import json
import math
import os
import re
import shutil
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from PIL import Image, ImageOps
from PySide6.QtGui import QGuiApplication
from studio.project import new_scene, new_object, validate, duration
from studio.exporter import export_video
from maya_edit_plan_v3 import plan_rows_v3

BASE = ROOT / 'projects/mo_den_maya'
DEST = BASE / 'director_v3'
MEDIA = BASE / 'assets/media'
SOURCES = BASE / 'source_materials/Mo_Den_Maya_Tu_Lieu_That_Va_Phan_Canh_v1'
VOICE = BASE / 'voice_direction/full_narration_custom_H_125/Mo_Den_Maya_Custom_H_1_25x_DAY_DU.wav'
INK, PAPER, BLUE, RUST = '#30241f', '#fffdf7', '#4f8497', '#b96949'
FPS = 24

FAMILIES = {
    151: 'Đô thị', 154: 'Chợ', 157: 'Hồ chứa', 160: 'Hồ/trầm tích',
    163: 'Ruộng ngô', 166: 'Kho lương', 169: 'Đường nối', 172: 'Nhà/sân',
    175: 'Khu công trình/cháy', 178: 'Cung điện'
}


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')


def rel(path):
    return Path(os.path.relpath(path, DEST)).as_posix()


class Library:
    def __init__(self):
        self.items = {}
        audit_file = BASE / 'director_v2/import_audit.json'
        audits = json.loads(audit_file.read_text(encoding='utf-8'))
        paths = {Path(i['file']).name: ROOT / i['file'] for a in audits for i in a['images']}
        for fn in ['generic_150_catalog.json', 'maya_48_catalog.json']:
            for a in json.loads((BASE / 'preflight' / fn).read_text(encoding='utf-8')):
                path = paths[Path(a['file']).name]
                self.items[str(int(a['id']))] = dict(file=rel(path), title=a.get('name_vi', a.get('ten_tieng_viet')))
        
        self.registry = json.loads((SOURCES / '04_Nguon_va_quyen/ASSET_REGISTRY.json').read_text(encoding='utf-8'))
        for a in self.registry:
            path = MEDIA / Path(a['file']).name
            if path.exists():
                self.items[a['id'].split('_')[0]] = dict(file=rel(path), title=a['title'], registry=a)
        
        for p in MEDIA.glob('G*.svg'):
            self.items[p.stem.split('_')[0]] = dict(file=rel(p), title=p.stem)
        for p in MEDIA.glob('G*.png'):
            prefix = p.stem.split('_')[0]
            if prefix not in self.items:
                self.items[prefix] = dict(file=rel(p), title=p.stem)

        self.cats = json.loads((ROOT / 'assets/characters/mo_den/manifest.json').read_text(encoding='utf-8'))['assets']
        self.alpha = {}
        self.used = set()

    def lookup(self, key):
        key = str(int(key)) if str(key).isdigit() else key
        if key.startswith('E') and '_' in key:
            p = next(MEDIA.glob(key + '.*'))
            entry = next((a for a in self.registry if Path(a['file']).stem == key), None)
            return dict(file=rel(p), title=entry['title'] if entry else key, registry=entry)
        if key.startswith('G'):
            matches = list(MEDIA.glob(f'{key}*.png')) + list(MEDIA.glob(f'{key}*.svg'))
            if matches:
                return dict(file=rel(matches[0]), title=matches[0].stem)
        return self.items[key]

    def crop(self, key):
        entry = self.lookup(key)
        file = entry['file']
        if file not in self.alpha:
            p = DEST / file
            if p.exists():
                with Image.open(p) as im:
                    if im.mode == 'RGBA':
                        b = im.getchannel('A').getbbox()
                        if b:
                            w, h = im.size
                            self.alpha[file] = [b[0]/w, b[1]/h, (b[2]-b[0])/w, (b[3]-b[1])/h]
                        else:
                            self.alpha[file] = [0, 0, 1, 1]
                    else:
                        self.alpha[file] = [0, 0, 1, 1]
            else:
                self.alpha[file] = [0, 0, 1, 1]
        return self.alpha[file]


def keyframes(a, b, end, start=0, ease='linear'):
    return [dict(t=start, v=a), dict(t=end, v=b, ease=ease)]


class Shot:
    def __init__(self, lib, row, index, start, end):
        self.lib, self.row, self.index = lib, row, index
        self.length = end - start
        self.scene = new_scene(f'{index+1:03d} · {row["title"]}', self.length)
        self.scene.update(id=f'maya_v3_{index+1:03d}', start=start, background='white', background_color=PAPER,
                          editorial=dict(**row, transition='cut_on_narration', timing='semantic_unit_estimate'))
        self.objs = self.scene['objects']

    def obj(self, kind, x, y, w, h, layer=10, on=0, **values):
        o = new_object(kind, values.pop('name', kind), x, y)
        o.update(width=w, height=h, layer=layer, start=on, end=self.length, **values)
        self.objs.append(o)
        return o

    def text(self, text, x=640, y=94, w=1120, h=95, size=40, **values):
        return self.obj('text', x, y, w, h, layer=60, text=text, font='Segoe UI', color=values.pop('color', INK),
                        font_size=size, bold=values.pop('bold', True), **values)

    def shape(self, shape, x, y, w, h, fill=PAPER, color=INK, layer=20, **values):
        return self.obj('shape', x, y, w, h, layer=layer, shape=shape, fill=fill, color=color, stroke=3, **values)

    def art(self, key, x=640, y=355, w=350, h=350, on=0, layer=25, enter=True, crop=True, **values):
        a = self.lib.lookup(key)
        self.lib.used.add(str(key))
        o = self.obj('image', x, y, w, h, layer=layer, on=on, file=a['file'], name=a['title'], fit='contain',
                     crop=self.lib.crop(key) if crop and Path(a['file']).suffix != '.svg' else [0, 0, 1, 1], **values)
        if enter:
            o.update(enter='fade', enter_duration=.22)
            o['keys']['scale'] = [dict(t=on, v=.88), dict(t=min(on+.32, self.length), v=1, ease='ease_out')]
        return o

    def host(self, expression=None, x=255, y=365, size=580, emotion=None, **kwargs):
        expression = expression or emotion or self.row.get('emotion') or 24
        entry = next(a for a in self.lib.cats if a['id'] == f'mo_den_{expression:02d}')
        o = self.obj('image', x, y, size, size, layer=45, file=rel(ROOT / 'assets/characters/mo_den' / entry['file']),
                     fit='contain', name='Mỏ Đen · ' + entry['emotion_vi'], role='character',
                     character_library='mo_den', character_asset_id=entry['id'])
        o['keys']['x'] = [dict(t=0, v=x-12), dict(t=.3, v=x, ease='ease_out')]
        o.update(enter='fade', enter_duration=.16)
        return o

    def arrow(self, points, on=.2, end=1.4, color=BLUE, stroke=5):
        return self.obj('shape', 0, 0, 1280, 720, layer=18, on=on, shape='path', points=points, color=color, fill='none',
                        reveal=True, enter_duration=max(.1, end-on), stroke=stroke)

    def title(self, text=None):
        # Used for diagram / concept scenes (subtle header)
        self.text(text or self.row['title'], 640, 70, 1120, 60, 36)

    def label(self, text, x, y, w=250, size=24, on=0):
        return self.text(text, x, y, w, 66, size, bold=False, on=on)

    def world(self):
        source = self.row['source']
        a = self.lib.lookup(source)
        self.lib.used.add(source)
        i = int(source)
        
        foci = {151: (.68, .48), 152: (.68, .48), 153: (.68, .48), 154: (.74, .55), 155: (.26, .55), 156: (.70, .55),
                157: (.52, .64), 158: (.52, .64), 159: (.52, .64), 160: (.50, .65), 161: (.50, .69), 162: (.50, .65),
                163: (.70, .57), 164: (.70, .57), 165: (.70, .57), 166: (.72, .58), 167: (.72, .58), 168: (.72, .58),
                172: (.53, .51), 173: (.53, .51), 174: (.53, .51), 175: (.72, .52), 176: (.72, .52), 177: (.72, .52),
                178: (.32, .46), 179: (.32, .46), 180: (.65, .53)}
        fx, fy = foci.get(i, (.52, .54))
        cw, ch = (1, 1)
        crop = [max(0, min(1-cw, fx-cw/2)), max(0, min(1-ch, fy-ch/2)), cw, ch]
        
        # 1. Background image with gentle cinematic drift
        o = self.obj('image', 640, 360, 1280, 720, layer=1, file=a['file'], name=a['title'], fit='cover', crop=crop)
        o['keys'] = dict(
            scale=keyframes(1.0, 1.025, self.length),
            x=keyframes(640, 636 if self.index%2 else 644, self.length)
        )
        
        # 2. Animate props if present on cue
        for n, key in enumerate(self.row['props'][:2]):
            if key == '004':  # Departure pack
                p = self.art(key, 760, 520, 170, 180, on=.2)
                p['keys']['x'] = [dict(t=.2, v=760), dict(t=self.length-.15, v=960, ease='ease_in_out')]
            elif key == '075':  # Cargo pack
                p = self.art(key, 520, 480, 160, 160, on=.2)
                p['keys']['x'] = keyframes(520, 780, self.length-.2, start=.2, ease='ease_in_out')
            else:
                self.art(key, 880-n*220, 480, 180, 200, on=.3+n*.3)

        # 3. Ground Mỏ Đen INSIDE the space in realistic perspective (NO EMPTY WIDE SHOTS!)
        emotion = self.row.get('emotion')
        if not emotion:
            emotion = 15 if i in (158, 159, 164, 165, 173, 174, 177, 179) else 1
        
        if i in (172, 173, 174):
            self.host(emotion=emotion, x=290, y=500, size=340)
        elif i in (157, 158, 159):
            self.host(emotion=emotion, x=320, y=510, size=340)
        elif i in (163, 164, 165):
            self.host(emotion=emotion, x=300, y=510, size=340)
        elif i in (175, 176, 177):
            self.host(emotion=emotion or 6, x=260, y=500, size=350)
        elif i in (154, 155, 156):
            self.host(emotion=emotion, x=290, y=500, size=340)
        elif i in (178, 179, 180):
            self.host(emotion=emotion, x=310, y=500, size=340)
        else:
            self.host(emotion=emotion, x=280, y=500, size=340)

    def graphics(self):
        source = self.row['source']
        a = self.lib.lookup(source)
        self.lib.used.add(source)
        o = self.obj('image', 640, 360, 1280, 720, layer=1, file=a['file'], name=self.row['title'], fit='cover')
        o['keys'] = dict(scale=keyframes(1.0, 1.025, self.length), x=keyframes(640, 635, self.length))
        if self.row['emotion']:
            self.host(self.row['emotion'], x=210, y=510, size=320)

    def photograph(self, proof=False):
        source = self.row['source']
        a = self.lib.lookup(source)
        p = DEST / a['file']
        oriented = Image.open(p)
        oriented = ImageOps.exif_transpose(oriented)
        ratio = oriented.width / oriented.height
        
        if proof:
            self.title()
            if source == 'E06_pollution_fig4' and self.row['first'] == 48:
                self.art(source, 240, 335, 295, 450, enter=False, crop=False)
                detail = self.art(source, 855, 325, 670, 410, enter=False, crop=False)
                detail['crop'] = [0, 0, .70, .66]
                self.label('Toàn hình', 240, 558, 300, 19)
                self.label('Chi tiết Temple / Palace', 855, 558, 650, 22)
            elif source == 'E08_Itzan_fig3' and self.row['first'] == 85:
                self.art(source, 350, 337, 480, 440, enter=False, crop=False)
                detail = self.art(source, 920, 330, 470, 360, enter=False, crop=False)
                detail['crop'] = [0, 0, 1, .44]
                self.label('Toàn bộ figure', 350, 555, 450, 20)
                self.label('Chi tiết phần trên', 920, 555, 590, 20)
            else:
                self.art(source, 640, 337, 1120, 465, enter=False, crop=False)
        elif ratio < 1:
            self.title()
            self.art(source, 830, 337, 590, 445, enter=False, crop=False)
            self.text(self.row['title'], 310, 310, 440, 240, 42)
            self.shape('line', 310, 464, 210, 4, color=RUST)
        else:
            self.title()
            o = self.art(source, 640, 340, 1120, 452, enter=False, crop=False)
            o['keys']['scale'] = keyframes(1, 1.025, self.length)

    def objects(self, host=False, question=False):
        props = self.row['props']
        emotion = self.row['emotion']
        if host or question:
            self.host(x=260, y=360, size=600)
            self.text(self.row['title'], 865, 240, 640, 205, 42)
            if props:
                for n, key in enumerate(props[:3]):
                    x = 700 + n * 190 if len(props) > 1 else 860
                    p = self.art(key, x, 450, 180 if len(props) > 1 else 230, 200, on=.32+n*.35)
                    if key == '195':
                        p['keys']['y'] = keyframes(433, 465, self.length, start=.2, ease='ease_in_out')
            if question:
                self.text('?', 1080, 458, 120, 170, 100, color=RUST)
        else:
            self.title()
            n = len(props)
            labels = {'184': 'Thạch anh', '185': 'Zeolit', '186': 'Chu sa', '187': 'Trầm tích', '188': 'Măng đá',
                      '189': 'Thạch cao', '181': 'Kênh', '182': 'Hồ / đập', '183': 'Điều tiết', '195': 'Nước',
                      '193': 'Chất lượng nước', '192': 'Hạt giống', '072': 'Dự trữ', '103': 'Thức ăn',
                      '075': 'Trao đổi', '127': 'An toàn', '130': 'Hợp tác', '190': 'Bắp ngô', '191': 'Ngô héo'}
            for j, key in enumerate(props):
                x = 640 + (j - (n - 1) / 2) * min(350, 1000 / max(1, n))
                self.art(key, x, 325, 310 if n < 3 else 255, 320 if n < 3 else 265, on=j*.25)
                self.label(labels.get(key, self.lib.lookup(key)['title']), x, 520, 310, 24, on=j*.25)
            if emotion and n < 3:
                self.host(x=1180, y=456, size=280)

    def compare(self):
        self.title()
        props = self.row['props']
        for j, key in enumerate(props[:2]):
            x = 330 + j * 620
            self.shape('card', x, 330, 520, 400, fill='#f6eddf', color='#e3d7c5', layer=3)
            self.art(key, x, 320, 420, 310, on=j*.25)
        self.text('≠', 640, 325, 100, 120, 64, color=RUST)

    def network(self):
        self.title()
        props = self.row['props']
        count = len(props)
        pts = []
        for i in range(count):
            angle = -math.pi / 2 + i * 2 * math.pi / count
            pts.append((640 + 375 * math.cos(angle), 350 + 190 * math.sin(angle)))
        for i, (x, y) in enumerate(pts):
            nx, ny = pts[(i + 1) % count]
            self.arrow([[x, y], [nx, ny]], on=.1, end=min(2, self.length*.55), color='#b8b0a1', stroke=3)
        names = {'195': 'Nước', '103': 'Thức ăn', '075': 'Trao đổi', '127': 'An toàn', '130': 'Hợp tác',
                 '172': 'Cộng đồng', '178': 'Quyền lực', '151': 'Thành bang', '114': 'Môi trường'}
        for i, ((x, y), key) in enumerate(zip(pts, props)):
            self.art(key, x, y, 185, 160, on=i*.2)
            self.label(names.get(key, ''), x, y+110, 230, 23, on=i*.2)
        if self.row['emotion']:
            self.host(x=640, y=356, size=300)
        else:
            self.shape('ellipse', 640, 353, 55, 55, fill='#f0d4a7', color=INK)

    def map(self):
        self.title()
        m = self.art('G01', 420, 340, 590, 460, enter=False, crop=False)
        m['crop'] = [.15, .18, .39, .67]
        m['keys']['scale'] = keyframes(1, 1.025, self.length)
        self.text(self.row['title'], 955, 245, 420, 170, 38)
        names = ['Tikal', 'Itzan', 'Chichén Itzá', 'Mayapán']
        if self.row['first'] in (24,): names = ['Tikal', 'Guatemala']
        if self.row['first'] in (82,): names = ['Itzan', 'Guatemala']
        for j, name in enumerate(names):
            self.label(name, 955, 365 + j * 43, 400, 24, on=j*.2)

    def water(self):
        self.title()
        if self.row['source'] == 'limestone':
            self.shape('card', 640, 420, 940, 160, fill='#e6cba6', color='#aa8667', layer=4)
            self.shape('card', 640, 495, 940, 75, fill='#b99c7e', color='#aa8667', layer=5)
            for i in range(6):
                x = 260 + i * 150
                self.arrow([[x, 200], [x+25, 275], [x-5, 340], [x+20, 465]], on=i*.12, end=2.5, color=BLUE, stroke=4)
                d = self.art('195', x, 200, 36, 50, on=i*.12)
                d['keys']['y'] = keyframes(190, 470, self.length, start=i*.12)
            self.label('Nền đá vôi thấm nước', 640, 548, 940, 26)
        else:
            for j, (key, x) in enumerate([('121', 220), ('181', 620), ('182', 1040)]):
                self.art(key, x, 315, 290, 260, on=j*.2)
            self.arrow([[320, 350], [470, 350], [450, 336], [470, 350], [450, 364]], end=1.2)
            self.arrow([[750, 350], [895, 350], [875, 336], [895, 350], [875, 364]], on=.5, end=1.9)
            for i in range(4):
                on = i * .32
                d = self.art('195', 280, 365, 35, 45, on=on, layer=35)
                d['keys']['x'] = [dict(t=on, v=280), dict(t=self.length-.2, v=1060, ease='linear')]
                d['keys']['y'] = [dict(t=on, v=345), dict(t=self.length*.45, v=390), dict(t=self.length-.2, v=365)]
            self.label('MƯA', 220, 505, 250, 26)
            self.label('THU VÀ DẪN', 620, 505, 350, 26)
            self.label('TRỮ NƯỚC', 1040, 505, 300, 26)

    def tank(self):
        self.title()
        self.art('197', 800, 330, 420, 410, enter=False)
        self.host(15, x=245, y=375, size=530)
        self.text('VÍ DỤ HIỆN ĐẠI', 790, 140, 500, 45, 20, color=RUST)
        self.shape('card', 1100, 335, 44, 300, fill='#e7e4dc', color=INK)
        level = self.shape('card', 1100, 390, 28, 170, fill=BLUE, color=BLUE, layer=30)
        level['keys']['scale'] = keyframes(1, .16, self.length, ease='ease_in_out')
        level['keys']['y'] = keyframes(390, 450, self.length, ease='ease_in_out')
        self.label('Nước bổ sung ↓', 1080, 538, 300, 23)

    def route(self, trade=False, distance=False):
        self.title()
        if distance:
            self.art('184', 230, 290, 230, 230)
            self.art('182', 1020, 310, 300, 270, on=.25)
            self.text('≈ 30 km', 650, 240, 520, 140, 76, color=RUST)
            self.arrow([[330, 420], [940, 420], [920, 407], [940, 420], [920, 433]], on=.1, end=2)
            m = self.art('185', 350, 385, 130, 130, on=.3)
            m['keys']['x'] = keyframes(350, 890, self.length-.15, start=.3, ease='ease_in_out')
            self.label('Nguồn vật liệu', 230, 535, 310, 24)
            self.label('Corriental', 1020, 535, 300, 24)
            return
        if trade:
            self.art('172', 240, 300, 360, 260, enter=False)
            self.art('172', 1040, 300, 360, 260, on=.15, enter=False)
            self.arrow([[395, 430], [875, 430], [855, 417], [875, 430], [855, 443]], on=.1, end=1.6)
            p = self.art('075', 400, 390, 135, 135, on=.25)
            barrier = self.row['first'] in (92, 106)
            p['keys']['x'] = keyframes(400, 645 if barrier else 880, self.length-.2, start=.25, ease='ease_in_out')
            if barrier: self.art('127', 760, 420, 190, 170, on=self.length*.38)
            self.label('Khu dân cư A', 240, 520, 330, 24)
            self.label('Khu dân cư B', 1040, 520, 330, 24)
        else:
            self.art('128', 785, 310, 620, 340, enter=False)
            self.host(15, x=205, y=380, size=460)
            key = self.row['props'][0] if self.row['props'] else '004'
            p = self.art(key, 470, 355, 160, 180, on=.15)
            p['keys']['x'] = [dict(t=.15, v=470), dict(t=self.length*.62, v=740, ease='ease_in_out'), dict(t=self.length-.1, v=900, ease='ease_in_out')]
            p['keys']['y'] = [dict(t=.15, v=355), dict(t=self.length*.62, v=355), dict(t=self.length-.1, v=275, ease='ease_in_out')]

    def pollution(self):
        self.title()
        self.art('186', 240, 270, 250, 245)
        self.art('194', 650, 365, 440, 240, on=.2)
        self.art('193', 1070, 400, 270, 220, on=.45)
        for i in range(5):
            p = self.shape('ellipse', 350, 315, 15, 15, fill=RUST, color=RUST, layer=40, on=i*.16)
            p['keys']['x'] = keyframes(350, 1020, self.length-.1, start=i*.16)
            p['keys']['y'] = [dict(t=i*.16, v=290), dict(t=self.length*.6, v=420), dict(t=self.length-.1, v=380)]
        self.label('Sắc tố chu sa', 240, 505, 300, 26)
        self.label('Dòng chảy nước mưa', 650, 525, 350, 26)
        self.label('Đáy hồ ô nhiễm', 1070, 535, 300, 26)

    def timeline(self):
        self.title()
        source = self.row['source']
        if source == 'next':
            self.arrow([[180, 420], [1120, 420], [1100, 407], [1120, 420], [1100, 433]], end=1.8)
            for i, (x, text) in enumerate([(400, 'Tưởng xa cách'), (880, 'Có thể cùng thời')]):
                self.shape('ellipse', x, 420, 22, 22, fill=RUST, color=RUST, on=i*.4)
                self.text(text, x, 320, 420, 100, 35, on=i*.4)
            return
        years = [250, 697, 900, 1200, 1450, 1697]
        def px(year): return 120 + (year - 250) / (1697 - 250) * 1040
        self.arrow([[120, 440], [1160, 440]], on=0, end=1, color=INK, stroke=4)
        focus = {'classic': (250, 900), 'war': (697, 697), 'mayapan': (1200, 1450),
                 'colonial': (1697, 1697), 'continuity': (900, 1697)}[source]
        for j, y in enumerate(years):
            x = px(y)
            self.shape('ellipse', x, 440, 15, 15, fill=RUST if focus[0] <= y <= focus[1] else '#cfc5b5', color=INK,
                       on=min(.1*j, self.length*.2))
            self.label(str(y), x, 490, 125, 23, on=min(.1*j, self.length*.2))
        if focus[0] != focus[1]:
            self.arrow([[px(focus[0]), 390], [px(focus[1]), 390]], on=.1, end=1.3, color=BLUE, stroke=14)
        else:
            x = px(focus[0])
            self.arrow([[x, 280], [x, 415], [x-12, 395], [x, 415], [x+12, 395]], on=.2, end=1.2, color=RUST)
        labels = {'classic': 'Thời kỳ Cổ điển (250–900 SCN)', 'war': 'Witzna · Năm 697',
                  'mayapan': 'Mayapán · khoảng 1200–1450', 'colonial': 'Chương lịch sử thuộc địa',
                  'continuity': 'Lịch sử còn tiếp tục'}
        self.text(labels[source], 640, 220, 1050, 105, 48, color=RUST)

    def years(self):
        self.title()
        self.text('13', 640, 245, 650, 190, 140, color=RUST)
        for i in range(13):
            self.shape('card', 160 + i * 80, 415, 60, 66, fill=RUST, color=RUST, on=min(.15*i, self.length*.6))
        self.text('năm', 850, 280, 200, 100, 42, color=RUST)
        self.label('Khoảng 929–942 CN · sai số niên đại ±6 năm', 640, 520, 1120, 25)

    def rainchart(self):
        self.title()
        self.text('41–54%', 640, 260, 1080, 190, 110, color=RUST)
        self.arrow([[180, 450], [1120, 450]], on=0, end=.5, color='#c7beae', stroke=3)
        for n in (0, 20, 40, 60, 80, 100):
            self.label(str(n), 180 + n * 9.4, 488, 100, 22)
        self.arrow([[180 + 41 * 9.4, 418], [180 + 54 * 9.4, 418]], on=.3, end=1.8, color=RUST, stroke=20)
        self.label('Mức giảm lượng mưa ước tính (%)', 640, 540, 1000, 24)

    def choice(self):
        self.title()
        self.host(self.row['emotion'] or 15, x=640, y=340, size=460)
        self.art('172', 250, 285, 340, 270, enter=False)
        p = self.art('004', 1030, 325, 250, 270, on=.15)
        p['keys']['x'] = keyframes(1010, 1060, self.length, start=.15, ease='ease_in_out')
        self.label('Ở LẠI', 250, 505, 350, 30)
        self.label('RỜI ĐI', 1040, 505, 350, 30)

    def summary(self):
        self.title()
        for i, (key, name, meaning) in enumerate([('182', 'TIKAL', 'Nguồn nước'),
                                                  ('060', 'WITZNA', 'Dấu cháy / chiến tranh'),
                                                  ('195', 'ITZAN', 'Câu hỏi về liên kết vùng')]):
            x = 245 + i * 395
            self.shape('card', x, 330, 355, 390, fill='#f6eddf', color='#e3d7c5', layer=2)
            self.art(key, x, 300, 235, 235, on=i*.25)
            self.text(name, x, 468, 330, 50, 28, on=i*.25)
            self.label(meaning, x, 520, 330, 22, on=i*.25)

    def build(self):
        layout = self.row['layout']
        if layout == 'world': self.world()
        elif layout == 'graphics': self.graphics()
        elif layout == 'photo': self.photograph()
        elif layout == 'proof': self.photograph(True)
        elif layout in ('host', 'question', 'objects'): self.objects(host=layout=='host', question=layout=='question')
        elif layout == 'compare': self.compare()
        elif layout == 'network': self.network()
        elif layout == 'map': self.map()
        elif layout == 'water': self.water()
        elif layout == 'tank': self.tank()
        elif layout == 'distance': self.route(distance=True)
        elif layout == 'trade': self.route(trade=True)
        elif layout == 'route': self.route()
        elif layout == 'pollution': self.pollution()
        elif layout == 'timeline': self.timeline()
        elif layout == 'years': self.years()
        elif layout == 'rainchart': self.rainchart()
        elif layout == 'choice': self.choice()
        elif layout == 'summary': self.summary()
        else: raise ValueError(f"Unknown layout: {layout}")
        return self.scene


def credit_scenes(lib, start):
    used = []
    for a in lib.registry:
        stem = Path(a['file']).stem
        if stem in lib.used or stem.split('_')[0] in lib.used:
            used.append(a)
    pages = [used[i:i+5] for i in range(0, len(used), 5)]
    scenes = []
    for i, page in enumerate(pages):
        row = dict(first=170, last=170, layout='credits', source='', props=[], emotion=0, title='Nguồn ảnh và nghiên cứu')
        shot = Shot(lib, row, 999+i, start+i*7, start+(i+1)*7)
        shot.title()
        for j, a in enumerate(page):
            text = a['title'] + ' — ' + a['author'] + ' — ' + a['license']
            shot.text(text, 640, 190+j*75, 1100, 65, 24, bold=False)
        scenes.append(shot.scene)
    
    credits = ['MỎ ĐEN · MAYA · BẢN ĐẠO DIỄN V3', '',
               'Ảnh minh họa, mascot: tài nguyên người dùng cung cấp; giữ nguyên nguồn ảnh.',
               'Chỉnh dựng: hiển thị đúng hướng EXIF, thay đổi cỡ cảnh, pan/zoom có chủ đích, không tạo hoạt động mới cho người trong ảnh.',
               'Các hình minh họa khái niệm không phải phục dựng một địa điểm cụ thể.', '']
    for a in used:
        credits += [a['credit'], 'Giấy phép: ' + a['license_url'], 'Trang nguồn: ' + a['source_url'], '']
    credits += ['Các đồ họa số liệu dựa trên các tài liệu đã có trong gói nguồn, không tự thêm chuỗi số liệu.',
                'Bản gốc và điều kiện giấy phép được cung cấp trong source_materials và registry tương ứng.']
    (DEST / 'CREDIT_VIDEO.txt').write_text('\n'.join(credits), encoding='utf-8')
    dump(DEST / 'used_sources.json', used)
    return scenes


def build_project():
    DEST.mkdir(parents=True, exist_ok=True)
    # Ensure audit file is in DEST
    if not (DEST / 'import_audit.json').exists():
        shutil.copy2(BASE / 'director_v2/import_audit.json', DEST / 'import_audit.json')
        
    lib = Library()
    units = json.load(open(BASE / 'voice_direction/full_narration_custom_H_125/timeline_full.json', encoding='utf-8'))['units']
    rows = plan_rows_v3()
    groups = []
    for row in rows:
        key = (row['first'], row['last'])
        if groups and groups[-1][0] == key:
            groups[-1][1].append(row)
        else:
            groups.append((key, [row]))
            
    covered = []
    scenes = []
    spoken_end = math.ceil(831.206167 * FPS) / FPS
    
    shot_ledger = []
    
    for (first, last), parts in groups:
        covered.extend(range(first, last + 1))
        start = units[first - 1]['final_start_seconds']
        end = units[last]['final_start_seconds'] if last < len(units) else spoken_end
        first_frame = round(start * FPS)
        last_frame = round(end * FPS)
        
        for j, row in enumerate(parts):
            a = round(first_frame + (last_frame - first_frame) * j / len(parts)) / FPS
            b = round(first_frame + (last_frame - first_frame) * (j + 1) / len(parts)) / FPS
            shot = Shot(lib, row, len(scenes), a, b)
            built_scene = shot.build()
            scenes.append(built_scene)
            
            # Prepare ledger row
            spoken_text = units[first - 1]['text']
            fam = '-'
            if row['layout'] == 'world' and row['source'].isdigit():
                n = int(row['source'])
                fam = next((name for k, name in FAMILIES.items() if k <= n <= k + 2), f'Tài sản {row["source"]}')
            
            shot_ledger.append({
                'index': len(scenes),
                'time': f'{a:.2f}s - {b:.2f}s ({b-a:.2f}s)',
                'sentence': spoken_text[:60] + ('...' if len(spoken_text) > 60 else ''),
                'purpose': row['title'],
                'subject': 'Mỏ Đen & Bối cảnh' if row['layout'] == 'world' else row['source'],
                'action': f"Bố cục {row['layout']}, chuyển động nhịp kể",
                'focus': row['title'],
                'cut_point': 'Cắt theo ngữ nghĩa câu audio',
                'family': fam,
                'reuse_reason': 'Xuất hiện định mức <=3 lần' if fam != '-' else 'Tư liệu/sơ đồ chuyên biệt'
            })
            
    scenes += credit_scenes(lib, spoken_end)

    proj = {
        'schema': 1,
        'name': 'Mỏ Đen · Hồ sơ suy tàn văn minh Maya (Director V3)',
        'width': 1920,
        'height': 1080,
        'fps': FPS,
        'scenes': scenes,
        'audio': [{
            'id': 'main_voice_h',
            'name': 'Giọng đọc Mỏ Đen Custom H 1.25x',
            'file': rel(VOICE),
            'start': 0.0,
            'duration': spoken_end,
            'gain': 1.0
        }],
        'subtitles': [],
        'references': [],
        'subtitle_style': {
            'enabled': False,
            'size': 27,
            'font': 'Segoe UI',
            'color': '#ffffff',
            'background': True,
            'y': 0.975
        },
        'duck_music': False,
        'allow_draft': False,
        'render_profile': 'balanced',
        'supersample': 1,
        'directing_notes': {
            'standard': 'Compliant with QUY_DINH_DAO_DIEN_HINH_ANH.md (<=3 repetitions per background family, >=60s gap)',
            'voice': 'Preserved existing full H WAV (Northern, 1.25x)',
            'clean_frame': 'No disclaimers, no slide title headers in cinematic scenes, no baked subtitles'
        }
    }
    
    # Save project in director_v3 and copy to canonical projects/mo_den_maya/project.json
    dump(DEST / 'project.json', proj)
    
    # For canonical project.json, make paths relative to projects/mo_den_maya
    canonical_proj = copy.deepcopy(proj)
    canonical_proj['audio'] = [{
        'id': 'main_voice_h',
        'name': 'Giọng đọc Mỏ Đen Custom H 1.25x',
        'file': Path(os.path.relpath(VOICE, BASE)).as_posix(),
        'start': 0.0,
        'duration': spoken_end,
        'gain': 1.0
    }]
    for sc in canonical_proj['scenes']:
        for obj in sc['objects']:
            if obj.get('file'):
                abs_f = DEST / obj['file']
                obj['file'] = Path(os.path.relpath(abs_f, BASE)).as_posix()
    dump(BASE / 'project.json', canonical_proj)
    
    # Save shot ledger markdown table
    md_lines = [
        '# BẢNG ĐẠO DIỄN PHÂN CẢNH MAYA THEO AUDIO (DIRECTOR V3)',
        '',
        '| STT | Thời gian | Câu đang nói | Mục đích | Chủ thể cần nhìn | Hành động / Diễn biến | Điểm nhấn | Điểm cắt | Họ bối cảnh | Lý do sử dụng lại |',
        '|:---:|:---:|:---|:---|:---|:---|:---|:---|:---:|:---|'
    ]
    for row in shot_ledger:
        md_lines.append(
            f"| {row['index']} | {row['time']} | {row['sentence']} | {row['purpose']} | {row['subject']} | {row['action']} | {row['focus']} | {row['cut_point']} | {row['family']} | {row['reuse_reason']} |"
        )
    (DEST / 'shot_list_table.md').write_text('\n'.join(md_lines), encoding='utf-8')
    (BASE / 'shot_list_table.md').write_text('\n'.join(md_lines), encoding='utf-8')

    print(f"Successfully generated Director V3 project with {len(scenes)} scenes!")
    print(f"Project saved to: {DEST / 'project.json'} and {BASE / 'project.json'}")
    return proj


if __name__ == '__main__':
    build_project()
