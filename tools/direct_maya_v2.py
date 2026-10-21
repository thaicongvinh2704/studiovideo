"""Build and render the authored Maya edit from the user's existing assets.

The source voice is preserved byte-for-byte. Captions are estimated within the
existing semantic synthesis units; no claim of word-level forced alignment.
"""
import argparse
import copy
import hashlib
import json
import math
import os
import re
import subprocess
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from PIL import Image, ImageDraw, ImageFont, ImageOps
from PySide6.QtGui import QGuiApplication
from studio.project import new_scene, new_object, validate, missing, duration
from studio.renderer import Renderer
from studio.character_qc import project_issues
from studio.exporter import export_video, export_cached, binary
from maya_edit_plan import plan_rows

BASE = ROOT/'projects/mo_den_maya'
DEST = BASE/'director_v2'
MEDIA = BASE/'assets/media'
SOURCES = BASE/'source_materials/Mo_Den_Maya_Tu_Lieu_That_Va_Phan_Canh_v1'
VOICE = BASE/'voice_direction/full_narration_custom_H_125/Mo_Den_Maya_Custom_H_1_25x_DAY_DU.wav'
INK, PAPER, BLUE, RUST = '#30241f', '#fffdf7', '#4f8497', '#b96949'
FPS = 24


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')


def rel(path): return Path(os.path.relpath(path, DEST)).as_posix()


class Library:
    def __init__(self):
        self.items = {}
        audits = json.loads((DEST/'import_audit.json').read_text(encoding='utf-8'))
        paths = {Path(i['file']).name: ROOT/i['file'] for a in audits for i in a['images']}
        for fn in ['generic_150_catalog.json', 'maya_48_catalog.json']:
            for a in json.loads((BASE/'preflight'/fn).read_text(encoding='utf-8')):
                path = paths[Path(a['file']).name]
                actual = hashlib.sha256(path.read_bytes()).hexdigest()
                if actual != a['sha256']: raise ValueError('Asset hash mismatch: '+str(path))
                self.items[str(int(a['id']))] = dict(file=rel(path), title=a.get('name_vi', a.get('ten_tieng_viet')))
        self.registry = json.loads((SOURCES/'04_Nguon_va_quyen/ASSET_REGISTRY.json').read_text(encoding='utf-8'))
        for a in self.registry:
            path = MEDIA/Path(a['file']).name
            self.items[a['id'].split('_')[0]] = dict(file=rel(path), title=a['title'], registry=a)
        for p in MEDIA.glob('G*.svg'):
            self.items[p.stem.split('_')[0]] = dict(file=rel(p), title=p.stem)
        self.cats = json.loads((ROOT/'assets/characters/mo_den/manifest.json').read_text(encoding='utf-8'))['assets']
        self.alpha = {}
        self.used = set()

    def lookup(self, key):
        key = str(int(key)) if str(key).isdigit() else key
        if key.startswith('E') and '_' in key:
            p = next(MEDIA.glob(key+'.*'))
            entry = next((a for a in self.registry if Path(a['file']).stem == key), None)
            return dict(file=rel(p), title=entry['title'] if entry else key, registry=entry)
        return self.items[key]

    def crop(self, key):
        entry = self.lookup(key); file = entry['file']
        if file not in self.alpha:
            with Image.open(DEST/file) as im:
                if im.mode == 'RGBA':
                    b = im.getchannel('A').getbbox()
                    self.alpha[file] = [b[0]/im.width, b[1]/im.height, (b[2]-b[0])/im.width, (b[3]-b[1])/im.height]
                else: self.alpha[file] = [0, 0, 1, 1]
        return self.alpha[file]


def keyframes(a, b, end, start=0, ease='linear'):
    return [dict(t=start, v=a), dict(t=end, v=b, ease=ease)]


class Shot:
    def __init__(self, lib, row, index, start, end):
        self.lib, self.row, self.index = lib, row, index
        self.length = end-start
        self.scene = new_scene(f'{index+1:03d} · {row["title"]}', self.length)
        self.scene.update(id=f'maya_v2_{index+1:03d}', start=start, background='white', background_color=PAPER,
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
        a = self.lib.lookup(key); self.lib.used.add(str(key))
        o = self.obj('image', x, y, w, h, layer=layer, on=on, file=a['file'], name=a['title'], fit='contain',
                     crop=self.lib.crop(key) if crop and Path(a['file']).suffix != '.svg' else [0,0,1,1], **values)
        if enter:
            o.update(enter='fade', enter_duration=.22)
            o['keys']['scale'] = [dict(t=on, v=.88), dict(t=min(on+.32,self.length), v=1, ease='ease_out')]
        return o

    def host(self, expression=None, x=255, y=365, size=580):
        expression = expression or self.row.get('emotion') or 24
        entry = next(a for a in self.lib.cats if a['id'] == f'mo_den_{expression:02d}')
        o = self.obj('image', x, y, size, size, layer=45, file=rel(ROOT/'assets/characters/mo_den'/entry['file']),
                     fit='contain', name='Mỏ Đen · '+entry['emotion_vi'], role='character',
                     character_library='mo_den', character_asset_id=entry['id'])
        # The supplied pose stays static; only a small, controlled entrance settles.
        o['keys']['x'] = [dict(t=0,v=x-16), dict(t=.3,v=x,ease='ease_out')]
        o.update(enter='fade', enter_duration=.16)
        return o

    def arrow(self, points, on=.2, end=1.4, color=BLUE, stroke=5):
        o = self.obj('shape',0,0,1280,720,layer=18,on=on,shape='path',points=points,color=color,fill='none',
                     reveal=True,enter_duration=max(.1,end-on),stroke=stroke)
        # The last two legs make the arrowhead; the whole path reveals in order.
        return o

    def note(self, text):
        self.text(text, 640, 590, 1150, 36, 18, bold=False, name='Contexte / source')

    def title(self, text=None, light=False):
        if light:
            width=min(1180,max(480,24*len(text or self.row['title'])+80))
            self.shape('card',640,65,width,75,fill=PAPER,color=PAPER,layer=54,opacity=.94)
            self.text(text or self.row['title'],640,65,width-50,65,36)
        else:self.text(text or self.row['title'],640,76,1120,72,36)

    def label(self, text, x, y, w=250, size=24, on=0):
        return self.text(text,x,y,w,66,size,bold=False,on=on)

    def world(self):
        source = self.row['source']
        a = self.lib.lookup(source); self.lib.used.add(source)
        i = int(source); close = self.index%3 == 1
        foci = {151:(.68,.48),152:(.68,.48),153:(.68,.48),154:(.74,.55),155:(.26,.55),156:(.70,.55),
                157:(.52,.64),158:(.52,.64),159:(.52,.64),161:(.50,.69),162:(.50,.65),163:(.70,.57),
                164:(.70,.57),165:(.70,.57),166:(.72,.58),167:(.72,.58),168:(.72,.58),
                172:(.53,.51),173:(.53,.51),174:(.53,.51),175:(.72,.52),176:(.72,.52),177:(.72,.52),
                178:(.32,.46),179:(.32,.46),180:(.65,.53)}
        fx,fy = foci.get(i,(.52,.54))
        cw,ch = ((.79,.79) if close else (1,1))
        crop = [max(0,min(1-cw,fx-cw/2)),max(0,min(1-ch,fy-ch/2)),cw,ch]
        o = self.obj('image',640,360,1280,720,layer=1,file=a['file'],name=a['title'],fit='cover',crop=crop)
        o['keys'] = dict(scale=keyframes(1.012,1.055,self.length),x=keyframes(650 if self.index%2 else 630,630 if self.index%2 else 650,self.length))
        self.title(light=True)
        # Full backgrounds are supplied illustrations, never identified as footage.
        note = 'Minh họa khái quát'
        if self.row['first'] in range(6,11) or self.row['first'] in range(58,63) or self.row['first'] in range(90,95):
            note = 'Tình huống giả định'
        self.shape('card',1065,590,330,32,fill=PAPER,color=PAPER,layer=54,opacity=.92)
        self.text(note,1065,590,310,30,17,bold=False)
        for n,key in enumerate(self.row['props'][:2]):
            if key == '004':
                p = self.art(key,600,470,180,190,on=.3)
                p['keys']['x'] = [dict(t=.3,v=570),dict(t=self.length-.15,v=920,ease='ease_in_out')]
            elif key == '075':
                p = self.art(key,460,445,170,170,on=.2)
                p['keys']['x'] = keyframes(440,750,self.length-.2,start=.2,ease='ease_in_out')
            else:self.art(key,990-n*250,445,200,220,on=.35+n*.35)
        if self.row['emotion']: self.host(x=215,y=384,size=430)

    def photograph(self, proof=False):
        source = self.row['source']; a = self.lib.lookup(source)
        with Image.open(DEST/a['file']) as im:
            oriented=ImageOps.exif_transpose(im);ratio=oriented.width/oriented.height
        self.title()
        if proof:
            if source=='E06_pollution_fig4' and self.row['first']==48:
                self.art(source,240,335,295,450,enter=False,crop=False)
                detail=self.art(source,855,325,670,410,enter=False,crop=False)
                detail['crop']=[0,0,.70,.66]
                self.label('Toàn hình',240,558,300,19)
                self.label('Chi tiết Temple / Palace',855,558,650,22)
            elif source=='E08_Itzan_fig3' and self.row['first']==85:
                self.art(source,350,337,480,440,enter=False,crop=False)
                detail=self.art(source,920,330,470,360,enter=False,crop=False)
                detail['crop']=[0,0,1,.44]
                self.label('Toàn bộ figure',350,555,450,20)
                self.label('Chi tiết phần trên · giữ nguyên trục',920,555,590,20)
            else:self.art(source,640,337,1120,465,enter=False,crop=False)
            # All graph axes, captions and hypothesis labels remain inside the image.
            r = a.get('registry') or {}
            self.note(r.get('title',source)+' · '+r.get('author','')+' · '+r.get('license',''))
            if source == 'E03_zeolite_fig4': self.label('Cấu tạo giả thuyết được đề xuất trong nghiên cứu',640,556,1110,20)
        elif ratio < 1:
            self.art(source,830,337,590,445,enter=False,crop=False)
            # A portrait is kept whole. The left text gives it a deliberate composition.
            self.text(self.row['title'],310,310,440,240,45)
            self.shape('line',310,464,210,4,color=RUST)
            self.label('ẢNH TƯ LIỆU',310,500,400,20)
        else:
            o=self.art(source,640,340,1120,452,enter=False,crop=False)
            o['keys']['scale'] = keyframes(1,1.025,self.length)
        r=a.get('registry') or {}
        if not proof:
            self.note(r.get('author','')+' · '+r.get('date','')+' · '+r.get('license',''))

    def objects(self, host=False, question=False):
        props=self.row['props']; emotion=self.row['emotion']
        if host or question:
            self.host(x=260,y=360,size=600)
            self.text(self.row['title'],865,240,640,205,45)
            if props:
                for n,key in enumerate(props[:3]):
                    x=700+n*190 if len(props)>1 else 860
                    p=self.art(key,x,450,180 if len(props)>1 else 230,200,on=.32+n*.35)
                    if key=='195':p['keys']['y']=keyframes(433,465,self.length,start=.2,ease='ease_in_out')
            if question:
                self.text('?',1080,458,120,170,100,color=RUST)
        else:
            self.title()
            n=len(props)
            labels={'184':'Thạch anh','185':'Zeolit','186':'Chu sa','187':'Trầm tích','188':'Măng đá','189':'Thạch cao',
                    '181':'Kênh','182':'Hồ / đập','183':'Điều tiết','195':'Nước','193':'Chất lượng nước',
                    '192':'Hạt giống','072':'Dự trữ','103':'Thức ăn','075':'Trao đổi','127':'An toàn','130':'Hợp tác'}
            for j,key in enumerate(props):
                x=640+(j-(n-1)/2)*min(350,1000/max(1,n))
                p=self.art(key,x,325,310 if n<3 else 255,320 if n<3 else 265,on=j*.25)
                self.label(labels.get(key,self.lib.lookup(key)['title']),x,520,310,24,on=j*.25)
            if emotion and n<3:self.host(x=1180,y=456,size=280)
            self.note('Hình minh họa khái niệm · tài nguyên do người dùng cung cấp')

    def compare(self):
        self.title()
        props=self.row['props']
        for j,key in enumerate(props[:2]):
            x=330+j*620
            self.shape('card',x,330,520,400,fill='#f6eddf',color='#e3d7c5',layer=3)
            self.art(key,x,320,420,310,on=j*.25)
        self.text('≠',640,325,100,120,64,color=RUST)
        self.note('Tikal: Gary Todd · CC0 | Mayapán: SiMeCaIS · CC BY-SA 3.0' if props==['R01','R04'] else 'Sơ đồ khái niệm · không phải số liệu đo')

    def network(self):
        self.title()
        props=self.row['props']; count=len(props)
        pts=[]
        for i in range(count):
            angle=-math.pi/2+i*2*math.pi/count
            pts.append((640+375*math.cos(angle),350+190*math.sin(angle)))
        for i,(x,y) in enumerate(pts):
            nx,ny=pts[(i+1)%count]
            self.arrow([[x,y],[nx,ny]],on=.1, end=min(2,self.length*.55),color='#b8b0a1',stroke=3)
        names={'195':'Nước','103':'Thức ăn','075':'Trao đổi','127':'An toàn','130':'Hợp tác','172':'Cộng đồng','178':'Quyền lực','151':'Thành bang','114':'Môi trường'}
        for i,((x,y),key) in enumerate(zip(pts,props)):
            p=self.art(key,x,y,185,160,on=i*.2)
            self.label(names.get(key,''),x,y+110,230,23,on=i*.2)
        if self.row['emotion']:self.host(x=640,y=356,size=300)
        else:self.shape('ellipse',640,353,55,55,fill='#f0d4a7',color=INK)
        self.note('Sơ đồ quan hệ · không biểu thị tuyến đi hay mức dân số thực')

    def map(self):
        self.title()
        m=self.art('G01',420,340,590,460,enter=False,crop=False)
        m['crop']=[.15,.18,.39,.67]
        m['keys']['scale']=keyframes(1,1.025,self.length)
        self.text(self.row['title'],955,245,420,170,38)
        names=['Tikal','Itzan','Chichén Itzá','Mayapán']
        if self.row['first'] in (24,):names=['Tikal','Guatemala']
        if self.row['first'] in (82,):names=['Itzan','Guatemala']
        for j,name in enumerate(names):self.label(name,955,365+j*43,400,24,on=j*.2)
        self.note('Định vị khu vực · ranh giới quốc gia hiện đại · điểm Itzan là hồ lấy mẫu')

    def water(self):
        self.title()
        if self.row['source']=='limestone':
            self.shape('card',640,420,940,160,fill='#e6cba6',color='#aa8667',layer=4)
            self.shape('card',640,495,940,75,fill='#b99c7e',color='#aa8667',layer=5)
            for i in range(6):
                x=260+i*150
                self.arrow([[x,200],[x+25,275],[x-5,340],[x+20,465]],on=i*.12,end=2.5,color=BLUE,stroke=4)
                d=self.art('195',x,200,36,50,on=i*.12)
                d['keys']['y']=keyframes(190,470,self.length,start=i*.12)
            self.label('Nền đá vôi thấm nước',640,548,940,26)
        else:
            for j,(key,x) in enumerate([('121',220),('181',620),('182',1040)]):
                self.art(key,x,315,290,260,on=j*.2)
            self.arrow([[320,350],[470,350],[450,336],[470,350],[450,364]],end=1.2)
            self.arrow([[750,350],[895,350],[875,336],[895,350],[875,364]],on=.5,end=1.9)
            for i in range(4):
                on=i*.32
                d=self.art('195',280,365,35,45,on=on,layer=35)
                d['keys']['x']=[dict(t=on,v=280),dict(t=self.length-.2,v=1060,ease='linear')]
                d['keys']['y']=[dict(t=on,v=345),dict(t=self.length*.45,v=390),dict(t=self.length-.2,v=365)]
            self.label('MƯA',220,505,250,26)
            self.label('THU VÀ DẪN',620,505,350,26)
            self.label('TRỮ NƯỚC',1040,505,300,26)
        self.note('Sơ đồ nguyên lý · không phải bản vẽ khảo cổ chính xác của Tikal')

    def tank(self):
        self.title()
        self.art('197',800,330,420,410,enter=False)
        self.host(15,x=245,y=375,size=530)
        self.text('VÍ DỤ HIỆN ĐẠI',790,140,500,45,20,color=RUST)
        # A separate schematic gauge illustrates replenishment, not a measured level.
        self.shape('card',1100,335,44,300,fill='#e7e4dc',color=INK)
        level=self.shape('card',1100,390,28,170,fill=BLUE,color=BLUE,layer=30)
        level['keys']['scale']=keyframes(1,.16,self.length,ease='ease_in_out')
        level['keys']['y']=keyframes(390,450,self.length,ease='ease_in_out')
        self.label('Nước bổ sung ↓',1080,538,300,23)
        self.note('Bồn hiện đại dùng để ví von · thước mức bên cạnh chỉ mang tính minh họa')

    def route(self, trade=False, distance=False):
        self.title()
        if distance:
            self.art('184',230,290,230,230)
            self.art('182',1020,310,300,270,on=.25)
            self.text('≈ 30 km',650,240,520,140,76,color=RUST)
            self.arrow([[330,420],[940,420],[920,407],[940,420],[920,433]],on=.1,end=2)
            m=self.art('185',350,385,130,130,on=.3)
            m['keys']['x']=keyframes(350,890,self.length-.15,start=.3,ease='ease_in_out')
            self.label('Nguồn vật liệu',230,535,310,24)
            self.label('Corriental',1020,535,300,24)
            self.note('Sơ đồ khoảng cách theo lời kể · không phải tuyến vận chuyển đã xác lập')
            return
        if trade:
            self.art('172',240,300,360,260,enter=False)
            self.art('172',1040,300,360,260,on=.15,enter=False)
            self.arrow([[395,430],[875,430],[855,417],[875,430],[855,443]],on=.1,end=1.6)
            p=self.art('075',400,390,135,135,on=.25)
            barrier=self.row['first'] in (92,106)
            p['keys']['x']=keyframes(400,645 if barrier else 880,self.length-.2,start=.25,ease='ease_in_out')
            if barrier:self.art('127',760,420,190,170,on=self.length*.38)
            self.label('Khu dân cư A',240,520,330,24)
            self.label('Khu dân cư B',1040,520,330,24)
            self.note('Tình huống giả định · không phải bản đồ thương mại Maya')
        else:
            self.art('128',785,310,620,340,enter=False)
            self.host(15,x=205,y=380,size=460)
            key=self.row['props'][0] if self.row['props'] else '004'
            p=self.art(key,470,355,160,180,on=.15)
            p['keys']['x']=[dict(t=.15,v=470),dict(t=self.length*.62,v=740,ease='ease_in_out'),dict(t=self.length-.1,v=900,ease='ease_in_out')]
            p['keys']['y']=[dict(t=.15,v=355),dict(t=self.length*.62,v=355),dict(t=self.length-.1,v=275,ease='ease_in_out')]
            self.note('Minh họa tình huống · quyết định và tuyến đi đều mang tính sơ đồ')

    def pollution(self):
        self.title()
        self.art('186',240,270,250,245)
        self.art('194',650,365,440,240,on=.2)
        self.art('193',1070,400,270,220,on=.45)
        for i in range(5):
            p=self.shape('ellipse',350,315,15,15,fill=RUST,color=RUST,layer=40,on=i*.16)
            p['keys']['x']=keyframes(350,1020,self.length-.1,start=i*.16)
            p['keys']['y']=[dict(t=i*.16,v=290),dict(t=self.length*.6,v=420),dict(t=self.length-.1,v=380)]
        self.label('Sắc tố',240,505,300,26)
        self.label('Dòng chảy',650,525,350,26)
        self.label('Nguồn nước',1070,535,300,26)
        self.note('Giải thích được đề xuất · không thể hiện mức ô nhiễm đo được')

    def calendar(self):
        self.title()
        self.art('198',820,345,480,410,enter=False)
        self.host(self.row['emotion'] or 24,x=240,y=385,size=525)
        modern=self.row['first']>=145
        self.text('12' if modern else 'MÙA VỤ',820,350,280,150,90 if modern else 42,color=RUST)
        if modern:
            text=self.text('1',820,350,280,150,90,color=BLUE,on=self.length*.55)
            # A clean graphic page wipes over the old number, leaving the supplied calendar intact.
            self.shape('card',820,350,220,150,fill='#fff2da',color='#fff2da',layer=65,on=self.length*.55)
            text['layer']=66
            self.label('Sang một chu kỳ mới',820,535,560,26)
        self.note('Lịch bàn hiện đại dùng để ví von · không mô phỏng ký tự lịch Maya')

    def timeline(self):
        self.title()
        source=self.row['source']
        if source=='next':
            self.arrow([[180,420],[1120,420],[1100,407],[1120,420],[1100,433]],end=1.8)
            for i,(x,text) in enumerate([(400,'Tưởng xa cách'),(880,'Có thể cùng thời')]):
                self.shape('ellipse',x,420,22,22,fill=RUST,color=RUST,on=i*.4)
                self.text(text,x,320,420,100,35,on=i*.4)
            self.note('Gợi mở tập tiếp theo')
            return
        years=[250,697,900,1200,1450,1697]
        def px(year):return 120+(year-250)/(1697-250)*1040
        self.arrow([[120,440],[1160,440]],on=0,end=1,color=INK,stroke=4)
        focus={'classic':(250,900),'war':(697,697),'mayapan':(1200,1450),'colonial':(1697,1697),'continuity':(900,1697)}[source]
        for j,y in enumerate(years):
            x=px(y)
            self.shape('ellipse',x,440,15,15,fill=RUST if focus[0]<=y<=focus[1] else '#cfc5b5',color=INK,on=min(.1*j,self.length*.2))
            self.label(str(y),x,490,125,23,on=min(.1*j,self.length*.2))
        if focus[0]!=focus[1]:
            self.arrow([[px(focus[0]),390],[px(focus[1]),390]],on=.1,end=1.3,color=BLUE,stroke=14)
        else:
            x=px(focus[0]);self.arrow([[x,280],[x,415],[x-12,395],[x,415],[x+12,395]],on=.2,end=1.2,color=RUST)
        labels={'classic':'Thời kỳ Cổ điển','war':'Witzna · 697','mayapan':'Mayapán · khoảng 1200–1450','colonial':'Chương lịch sử thuộc địa','continuity':'Lịch sử còn tiếp tục'}
        self.text(labels[source],640,220,1050,105,48,color=RUST)
        self.note('Mốc chọn lọc theo kịch bản · trục năm Công nguyên theo tỷ lệ')

    def years(self):
        self.title()
        self.text('13',640,245,650,190,140,color=RUST)
        for i in range(13):
            self.shape('card',160+i*80,415,60,66,fill=RUST,color=RUST,on=min(.15*i,self.length*.6))
        self.text('năm',850,280,200,100,42,color=RUST)
        self.label('Khoảng 929–942 CN · sai số niên đại ±6 năm',640,520,1120,25)
        self.note('13 ô chỉ minh họa thời lượng · không biểu diễn lượng mưa từng năm')

    def rainchart(self):
        self.title()
        self.text('41–54%',640,260,1080,190,110,color=RUST)
        self.arrow([[180,450],[1120,450]],on=0,end=.5,color='#c7beae',stroke=3)
        for n in (0,20,40,60,80,100):self.label(str(n),180+n*9.4,488,100,22)
        self.arrow([[180+41*9.4,418],[180+54*9.4,418]],on=.3,end=1.8,color=RUST,stroke=20)
        self.label('Mức giảm lượng mưa (%)',640,540,1000,24)
        self.note('Ước tính tại khu vực hồ Chichancanab · Evans et al. (2018) · không áp dụng cho toàn vùng')

    def choice(self):
        self.title()
        self.host(self.row['emotion'] or 15,x=640,y=340,size=460)
        self.art('172',250,285,340,270,enter=False)
        p=self.art('004',1030,325,250,270,on=.15)
        p['keys']['x']=keyframes(1010,1060,self.length,start=.15,ease='ease_in_out')
        self.label('Ở LẠI',250,505,350,30)
        self.label('RỜI ĐI',1040,505,350,30)
        self.note('Tình huống giả định · không dựng tiểu sử một gia đình cụ thể')

    def summary(self):
        self.title()
        for i,(key,name,meaning) in enumerate([('182','TIKAL','Nguồn nước'),('060','WITZNA','Dấu cháy / chiến tranh'),('195','ITZAN','Câu hỏi về liên kết vùng')]):
            x=245+i*395
            self.shape('card',x,330,355,390,fill='#f6eddf',color='#e3d7c5',layer=2)
            self.art(key,x,300,235,235,on=i*.25)
            self.text(name,x,468,330,50,28,on=i*.25)
            self.label(meaning,x,520,330,22,on=i*.25)
        self.note('Ba địa điểm · những bằng chứng khác nhau · không một công thức cho tất cả')

    def build(self):
        layout=self.row['layout']
        if layout=='world':self.world()
        elif layout=='photo':self.photograph()
        elif layout=='proof':self.photograph(True)
        elif layout in ('host','question','objects'):self.objects(host=layout=='host',question=layout=='question')
        elif layout=='compare':self.compare()
        elif layout=='network':self.network()
        elif layout=='map':self.map()
        elif layout=='water':self.water()
        elif layout=='tank':self.tank()
        elif layout=='distance':self.route(distance=True)
        elif layout=='trade':self.route(trade=True)
        elif layout=='route':self.route()
        elif layout=='pollution':self.pollution()
        elif layout=='calendar':self.calendar()
        elif layout=='timeline':self.timeline()
        elif layout=='years':self.years()
        elif layout=='rainchart':self.rainchart()
        elif layout=='choice':self.choice()
        elif layout=='summary':self.summary()
        else:raise ValueError(layout)
        return self.scene


def subtitles(units):
    result=[]
    for u in units:
        # Sentence boundaries first; short readable captions within each sentence.
        clauses=re.split(r'(?<=[.!?])\s+',u['text'])
        chunks=[]
        for clause in clauses:
            words=clause.split()
            count=max(1,math.ceil(len(words)/16))
            for n in range(count):chunks.append(' '.join(words[round(n*len(words)/count):round((n+1)*len(words)/count)]))
        chunks=[s for s in chunks if s]
        total=sum(len(s.split()) for s in chunks); cursor=u['final_start_seconds']
        end=u['final_end_seconds']; full=end-cursor
        for i,s in enumerate(chunks):
            next_time=end if i==len(chunks)-1 else cursor+full*len(s.split())/max(1,total)
            result.append(dict(id=f'sub_{len(result)+1:04d}',start=cursor,end=max(cursor+.05,next_time),text=s))
            cursor=next_time
    return result


def srt_write(cues, path):
    def stamp(t):
        ms=round(t*1000);return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}'
    path.write_text('\n\n'.join(f'{i+1}\n{stamp(c["start"])} --> {stamp(c["end"])}\n{c["text"]}' for i,c in enumerate(cues))+'\n',encoding='utf-8')


def credit_scenes(lib,start):
    # Credit the actual photographs/figures, with complete URLs in the companion file.
    used=[]
    for a in lib.registry:
        stem=Path(a['file']).stem
        if stem in lib.used or stem.split('_')[0] in lib.used:used.append(a)
    pages=[used[i:i+5] for i in range(0,len(used),5)]
    scenes=[]
    for i,page in enumerate(pages):
        row=dict(first=170,last=170,layout='credits',source='',props=[],emotion=0,title='Nguồn ảnh và nghiên cứu')
        shot=Shot(lib,row,999+i,start+i*7,start+(i+1)*7)
        shot.title()
        for j,a in enumerate(page):
            text=a['title']+' — '+a['author']+' — '+a['license']
            shot.text(text,640,190+j*75,1100,65,24,bold=False)
        shot.note('Nguồn, URL, giấy phép và mô tả chỉnh sửa đầy đủ: CREDIT_VIDEO.txt cạnh video')
        scenes.append(shot.scene)
    credits=['MỎ ĐEN · MAYA · BẢN ĐẠO DIỄN V2','',
             'Ảnh minh họa, mascot: tài nguyên người dùng cung cấp; giữ nguyên nguồn ảnh.',
             'Chỉnh dựng: hiển thị đúng hướng EXIF, thay bố cục, pan/zoom, thay đổi tỷ lệ trình bày, chèn chữ và khung; không tạo hoạt động mới cho người trong ảnh.',
             'Các hình minh họa khái quát không phải phục dựng một địa điểm/cộng đồng cụ thể.','']
    for a in used:
        credits += [a['credit'],'Giấy phép: '+a['license_url'],'Trang nguồn: '+a['source_url'],
                    'Chỉnh sửa trong phim: hiển thị theo EXIF; thu/phóng và đặt ảnh trong bố cục; hình nghiên cứu ô nhiễm và Itzan có thêm cửa sổ cận chi tiết cạnh hình toàn vẹn; chèn tiêu đề/nguồn ngoài ảnh.','']
    credits += ['Các đồ họa số liệu dựa trên các tài liệu đã có trong gói nguồn, không tự thêm chuỗi số liệu.',
                'Mayapán (SiMeCaIS) CC BY-SA 3.0 và ảnh Tz’utujil (Chelalinda) CC BY-SA 4.0 được giữ toàn bộ nội dung ảnh trong bố cục.',
                'Bản gốc và điều kiện giấy phép được cung cấp trong source_materials và registry tương ứng. Không đổi giấy phép ảnh gốc.']
    (DEST/'CREDIT_VIDEO.txt').write_text('\n'.join(credits),encoding='utf-8')
    dump(DEST/'used_sources.json',used)
    return scenes


def build_project():
    lib=Library()
    units=json.loads((BASE/'voice_direction/full_narration_custom_H_125/timeline_full.json').read_text(encoding='utf-8'))['units']
    rows=plan_rows(); groups=[]
    for row in rows:
        key=(row['first'],row['last'])
        if groups and groups[-1][0]==key:groups[-1][1].append(row)
        else:groups.append((key,[row]))
    covered=[];scenes=[]
    spoken_end=math.ceil(831.206167*FPS)/FPS
    for (first,last),parts in groups:
        covered.extend(range(first,last+1))
        start=units[first-1]['final_start_seconds']
        end=units[last]['final_start_seconds'] if last<len(units) else spoken_end
        first_frame=round(start*FPS);last_frame=round(end*FPS)
        for j,row in enumerate(parts):
            a=round(first_frame+(last_frame-first_frame)*j/len(parts))/FPS
            b=round(first_frame+(last_frame-first_frame)*(j+1)/len(parts))/FPS
            shot=Shot(lib,row,len(scenes),a,b);scenes.append(shot.build())
    if covered!=list(range(1,170)):raise ValueError('Semantic coverage gap/overlap: '+str(covered))
    scenes+=credit_scenes(lib,spoken_end)
    p=dict(schema=1,name='Mỏ Đen · Maya · Bản đạo diễn chuyển động V2',width=1920,height=1080,fps=FPS,
           scenes=scenes,audio=[dict(id='H_narration_preserved',name='Custom H · Bắc · 1.25× đã áp dụng',file=rel(VOICE),
                                   start=0,duration=831.206167,group='voice',volume=1,fade_in=0,fade_out=0)],
           subtitles=subtitles(units),references=[],subtitle_style=dict(enabled=True,size=27,font='Segoe UI',
           color='#ffffff',background=True,y=.975),duck_music=False,allow_draft=False,render_profile='balanced',supersample=1,
           directing_notes=dict(reference='User supplied local kcWEaXRh2hA.mkv; studied frames, no content copied',
                                voice='Preserved existing full H WAV; no new synthesis, no second 1.25x',
                                subtitle_timing='Estimated phrase timing inside preserved semantic-unit audio spans; not word aligned',
                                source_policy='Preserved supplied originals, real photography and research figures separately credited'))
    validate(p)
    problems=project_issues(p,DEST)
    absent=missing(p,DEST)
    if absent or problems:raise ValueError(json.dumps(dict(missing=absent,qc=problems),ensure_ascii=False,indent=2))
    dump(DEST/'project.json',p)
    srt_write(p['subtitles'],DEST/'Maya_H_phu_de_cum_y.srt')
    dump(DEST/'shot_list.json',[dict(id=s['id'],start=s['start'],end=s['start']+s['duration'],**s['editorial']) for s in scenes])
    counts=Counter(s['editorial']['layout'] for s in scenes)
    report=dict(technical_preflight='PASS',duration_seconds=duration(p),shots=len(scenes),setups=counts,
                unique_assets_used=sorted(lib.used),narration_sha256=hashlib.sha256(VOICE.read_bytes()).hexdigest(),
                caption_timing='semantic estimate, requires playback review',visual_review='PENDING',
                character_checks='source hash, supplied identity, transparent alpha, aspect ratio, on-screen bounds; aesthetic review separate')
    dump(DEST/'build_report.json',report)
    print(json.dumps({k:v for k,v in report.items() if k!='unique_assets_used'},ensure_ascii=False),flush=True)
    return p


def review_frames(p):
    folder=DEST/'review';folder.mkdir(exist_ok=True)
    renderer=Renderer();frames=[]
    # Each authored shot is rendered at its settled composition for visual inspection.
    for i,s in enumerate(p['scenes']):
        t=s['start']+min(s['duration']*.6,max(.45,s['duration']-.25))
        path=folder/f'shot_{i+1:03d}.jpg'
        renderer.frame(p,DEST,t,960,540).save(str(path),quality=90)
        frames.append((f'{i+1:03d} {s["start"]/60:.2f}m · {s["editorial"]["layout"]}',path))
    font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',16)
    for k in range(0,len(frames),16):
        board=Image.new('RGB',(1600,1008),'#e9e5dc');draw=ImageDraw.Draw(board)
        for j,(label,path) in enumerate(frames[k:k+16]):
            im=Image.open(path);im.thumbnail((394,222));x=j%4*400;y=j//4*252
            board.paste(im,(x,y));draw.text((x+5,y+226),label,fill=INK,font=font)
        board.save(folder/f'board_{k//16+1:02d}.jpg',quality=93)
    dump(folder/'frames.json',[dict(label=x,file=rel(y)) for x,y in frames])
    print('Review boards:',math.ceil(len(frames)/16),flush=True)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('mode',choices=['build','review','preview','render'])
    parser.add_argument('--length',type=float,default=65.75)
    args=parser.parse_args()
    app=QGuiApplication(sys.argv[:1])
    if args.mode=='build':p=build_project();review_frames(p);return
    p=json.loads((DEST/'project.json').read_text(encoding='utf-8'))
    if args.mode=='review':review_frames(p);return
    out=DEST/('Maya_mo_dau_1080p.mp4' if args.mode=='preview' else 'Mo_Den_Maya_Dao_Dien_V2_1080p.mp4')
    started=time.monotonic();last=[0]
    def progress(n,total):
        if time.monotonic()-last[0]>12 or n==total:
            elapsed=time.monotonic()-started; speed=n/max(.1,elapsed)
            info=dict(frames=n,total=total,percent=round(n/total*100,2),render_fps=round(speed,2),elapsed_seconds=round(elapsed),eta_minutes=round((total-n)/max(.01,speed)/60,1))
            dump(DEST/'render_progress.json',info);print(json.dumps(info),flush=True);last[0]=time.monotonic()
    if args.mode=='preview':export_video(p,DEST,out,1920,1080,FPS,length=args.length,progress=progress)
    else:export_cached(p,DEST,out,1920,1080,FPS,progress=progress)
    print('CREATED: '+str(out),flush=True)


if __name__=='__main__':main()
