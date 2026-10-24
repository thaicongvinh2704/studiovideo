"""Full editable review timeline. Creates images/HTML/JSON, NEVER encodes a film.

Supplied humans stay static. PNG derivatives are crops, never synthesized poses.
The browser and review boards use the same timed drawing commands. The Studio
document has separate image/text/vector layers and corresponding animation keys.
"""
from pathlib import Path
from functools import lru_cache
from collections import Counter, defaultdict
import csv
import hashlib
import html
import json
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
P = ROOT/'projects/mo_den_phong_than'
OUT = P/'reference_style_edit_v2'
PACK = P/'assets/Mo_Den_Phong_Than_V2'
INK, RED, BLUE, GOLD, PAPER = '#292c30', '#ad4337', '#315e6e', '#d8b56c', '#fffdf8'
OFFSET = 1.5
source_manifest = {}
source_cache = {}
used = {}


def digest(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f,'sha256').hexdigest()


def dump(path,value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


@lru_cache(maxsize=64)
def font(size,bold=False):
    return ImageFont.truetype('C:/Windows/Fonts/'+('segoeuib.ttf' if bold else 'segoeui.ttf'),int(size))


def load_assets():
    rows=list(csv.DictReader((PACK/'danh_muc_anh.csv').open(encoding='utf-8-sig')))
    for row in rows:
        v=list(row.values()); ident,name,category,filename=v[:4]
        source_manifest[ident]={'path':PACK/filename,'name':name,'role':'character' if ident.startswith(('C_','A','K','Y')) or ident=='X07' else 'object_or_environment'}
    cats=json.loads((ROOT/'assets/characters/mo_den/manifest.json').read_text(encoding='utf-8'))
    for a in cats['assets']:
        if a.get('file'):
            source_manifest['cat'+a['id'][-2:]]={'path':ROOT/'assets/characters/mo_den'/a['file'],'name':a['emotion_vi'],'role':'character','bbox':a['alpha_bbox'],'expected_sha256':a['sha256']}


def asset(spec):
    """Return derivative URL and metadata; originals are never modified."""
    if spec in used:return used[spec]
    ident,_,raw=spec.partition('@');entry=source_manifest[ident];path=entry['path']
    if ident not in source_cache:
        original=Image.open(path);original.load();source_cache[ident]=original.convert('RGBA')
        entry['sha256']=digest(path)
        if entry.get('expected_sha256') and entry['sha256']!=entry['expected_sha256']:raise ValueError('Cat hash mismatch '+ident)
    im=source_cache[ident].copy();crop=None
    if raw:
        crop=list(map(float,raw.split(',')));x,y,w,h=crop
        im=im.crop((round(x*im.width),round(y*im.height),round((x+w)*im.width),round((y+h)*im.height)))
    elif 'bbox' in entry:im=im.crop(tuple(entry['bbox']))
    elif ident.startswith(('C_','A','O')):
        bbox=im.getchannel('A').getbbox()
        if bbox:im=im.crop(bbox)
    # Preview derivatives retain proportions. Scene crops deliberately retain their background.
    im.thumbnail((1500,1000),Image.Resampling.LANCZOS)
    filename='media/'+hashlib.sha256((spec+entry['sha256']).encode()).hexdigest()[:16]+'.png'
    if not (OUT/filename).exists():im.save(OUT/filename,compress_level=1)
    record={'url':filename,'source_id':ident,'source':str(path.relative_to(ROOT)).replace('\\','/'),
            'source_sha256':entry['sha256'],'role':entry['role'],'crop':crop,'width':im.width,'height':im.height,'derivative_sha256':digest(OUT/filename),'original_preserved':True}
    used[spec]=record
    return record


class Scene:
    def __init__(self,a,b,kind,sources,headline,purpose,cues,chapter):
        self.start,self.end=a,b;self.kind=kind;self.sources=sources;self.headline=headline;self.purpose=purpose;self.cues=cues;self.chapter=chapter;self.layers=[];self.dominant_family=None;self.bg_reason=None

    def add(self,kind,box=None,show=0,**kw):
        c={'kind':kind,'show':show,**kw}
        if box:c['box']=list(box)
        self.layers.append(c);return c

    def image(self,spec,box,show=0,move=None):
        meta=asset(spec)
        c=self.add('image',box,show,url=meta['url'],role=meta['role'],source_id=meta['source_id'])
        if move:c['move']=move
        return c

    def text(self,value,xy,size=32,color=INK,show=0,bold=True,width=1100):
        return self.add('text',show=show,text=value,xy=list(xy),size=size,color=color,bold=bold,max_width=width)

    def line(self,points,show=0,color=BLUE,width=4,arrow=False,reveal=.6):
        return self.add('line',show=show,points=[list(p) for p in points],color=color,width=width,arrow=arrow,reveal=reveal)

    def rect(self,box,fill='white',outline='#d9d4ca',radius=12,show=0):
        return self.add('rect',box,show,fill=fill,outline=outline,radius=radius)

    def heading(self):
        self.text(self.headline.replace('~',' · '),(640,65),32,BLUE,width=1140)

    def window(self,spec,box,show=0):
        self.rect((box[0]-3,box[1]-3,box[2]+6,box[3]+6),PAPER,'#d9d4ca',5,show)
        self.image(spec,box,show)


def pair(s,sources,labels,style):
    # Purpose-specific compositions, not a universal two-card template.
    if style in ('age','memory'):
        boxes=[(75,140,435,400),(770,140,435,400)]
        for i in range(2):s.window(sources[i],boxes[i],i*.45)
        s.line([(535,330),(745,330)],.7,arrow=True)
        s.text(labels[0],(640,92),31,BLUE)
        if len(labels)>1:s.text(labels[1],(640,575),29,RED,show=1.0)
        if style=='age':
            s.text('32',(285,570),36);s.text('72',(985,570),36,show=.5)
    elif style in ('contrast','emotion'):
        for i in range(2):
            s.window(sources[i],(80+i*640,135,480,375),i*.4)
            s.text(labels[i],(320+i*640,555),30,RED if i==0 else BLUE,show=i*.4,width=550)
        s.line([(600,320),(680,320)],.8,RED,arrow=True)
    elif style in ('loss','orders2'):
        s.image(sources[0],(120,110,340,380));s.image(sources[1],(790,110,340,380),.6)
        for i in range(2):s.text(labels[i],(290+i*700,550),28,RED if i==0 else BLUE,show=.6*i,width=560)
        s.line([(500,300),(750,300)],.8,arrow=style=='orders2')
    elif style=='seas':
        s.text('LỜI THỀ',(300,90),31,RED);s.text('SẮC PHONG',(975,90),31,BLUE,show=.5)
        s.image(sources[0],(130,175,340,300));s.window(sources[1],(790,160,360,330),.5)
        for j,x in enumerate((300,975)):
            for row in range(3):s.line([(x-180+i*10,490+row*16+math.sin(i/3)*7) for i in range(37)],.2+j*.5,BLUE,2)
            s.text(labels[j],(x,565),25,RED if j==0 else BLUE,show=j*.5,width=580)
        s.line([(640,135),(640,590)],.6,'#d6d0c4',2)


def person(s,spec,box,show=0):
    # Static entire supplied pose. No puppet distortion, deformations or lip sync.
    s.image(spec,box,show)


def reaction(s):
    """An authored situation for every narrator beat; no recurring empty board."""
    n=s.cues[0] if s.cues else (-1 if s.start==0 else -2)
    cat='cat'+s.sources[0].zfill(2)
    if n in (-1,-2):
        s.image(cat,(455,160,370,405));s.text('MỎ ĐEN' if n==-2 else 'PHONG THẦN',(640,75),44,BLUE)
        if n==-1:s.text('VÌ SAO KẺ ĐỊCH VẪN ĐƯỢC PHONG THẦN?',(640,590),29,BLUE)
        return
    if n in (9,121):
        # Only two uses of the narrator + question board composition.
        s.image(cat,(60,145,430,440));s.rect((535,140,675,355),PAPER,'#d1c6b3',25)
        s.text(s.headline,(870,315),36,BLUE,show=.25,width=590)
        if n==9:
            s.line([(795,295),(845,345)],.9,RED,5);s.line([(795,345),(845,295)],.9,RED,5)
        return
    if n==12:
        s.image(cat,(40,325,270,270));s.image('C_WZ',(470,135,255,375),.25);s.image('C_SG',(950,175,220,325),.8)
        s.text('CHƯA CHỈ CÓ HAI NGƯỜI ẤY',(750,65),33,BLUE);s.line([(335,420),(450,370)],.4,BLUE,4,True);s.text('?',(1110,555),50,RED,show=.9)
    elif n==32:
        s.image('C_JZ',(70,135,300,395));s.image('O04',(850,215,250,245),.5)
        s.text('MONG MUỐN TU HÀNH',(760,140),31,BLUE);s.text('PHẦN ĐƯỢC GIAO: XUỐNG NÚI',(760,550),29,RED,show=.5,width=850)
        s.line([(470,285),(720,285)],.6,RED,4,True);s.line([(605,245),(605,325)],.8,RED,5)
    elif n==45:
        for j,label in enumerate(['THẮNG TRẬN','NHẬN THẦN CHỨC']):
            s.rect((150+j*650,100,360,370),'white',RED if j==0 else BLUE,5,j*.2);s.text(label,(330+j*650,200),29,RED if j==0 else BLUE,show=j*.2,width=320)
        s.image(cat,(520,335,230,250));s.line([(560,300),(510,300)],.5,RED,4,True);s.line([(720,300),(780,300)],.5,BLUE,4,True)
        s.text('TÁCH HAI DANH SÁCH',(640,580),29,BLUE,show=.6)
    elif n==73:
        s.image('C_JZ',(130,110,270,380));s.image('C_WZ',(870,110,270,380),.2);s.image(cat,(530,345,220,240),.6)
        s.line([(450,285),(820,285)],.35,BLUE,4,True);s.text('NHÌN NHẬN PHẨM CHẤT ĐỐI THỦ',(640,75),32,BLUE)
    elif n in (116,193):
        ids=('C_JZ','C_SG') if n==116 else ('C_ZM','C_XS')
        for j,a in enumerate(ids):s.image(a,(130+j*730,170,290,365),j*.2)
        s.text('?',(640,330),86,RED,show=.5)
        s.text('KHÔNG CÓ CẢNH BÍ MẬT BẮT TAY' if n==116 else 'KHÔNG CÓ LỜI THA THỨ ĐƯỢC KỂ',(640,80),33,BLUE,width=1120)
        s.text('Đừng biến điều không được kể thành một sự kiện.',(640,585),25,show=.7)
    elif n in (83,90,93):
        s.image(cat,(70,340,245,245))
        if n!=93:s.image('O01',(820,190,310,345),.2)
        top={83:'CHIẾN CÔNG BÍ MẬT',90:'PHONG THẦN = TUYÊN DƯƠNG',93:'PHONG THẦN = AI CŨNG BỊ PHẠT'}[n]
        s.text(top,(640,95),37,RED,width=1160);s.line([(225,120),(1055,120)],.8,RED,5)
        if n==93:s.image('C_WZ',(600,180,340,380),.5)
        else:s.text('KHÔNG ĐƯỢC TRUYỆN KỂ' if n==83 else 'PHẢI ĐỌC LỜI SẮC',(540,340),31,BLUE,show=.5,width=450)
    elif n==153:
        s.image(cat,(55,285,285,300));s.image('O01',(450,155,300,340))
        for j in range(3):s.rect((830+j*80,440-j*90,90,150+j*90),PAPER,GOLD,0,.2+j*.2)
        s.line([(790,515),(1160,155)],.6,RED,5,True);s.line([(1130,185),(1190,245)],.9,RED,5)
        s.text('NHẬN CHỨC ≠ TĂNG BẬC SỨC MẠNH',(640,65),34,BLUE)
    elif n==156:
        s.image('O01',(440,115,400,420));s.image(cat,(90,350,230,240));s.text('ÂN ĐIỂN',(270,190),35,BLUE,show=.2);s.text('KỶ LUẬT',(1030,470),35,RED,show=.6)
        s.text('KHÔNG THỂ GỌI MỌI THẦN VỊ LÀ NHÀ TÙ',(640,75),32,BLUE,width=1160)
    elif n==204:
        s.image('C_JZ',(95,135,290,400));s.image('O23',(860,210,260,240),.3)
        s.line([(420,355),(820,355)],.4,BLUE,4,True);s.text('NHẬN PHẦN Ở CÕI NGƯỜI',(800,80),33,BLUE,width=820)
        s.text('Không có cảnh tự gọi hồn để nhận thần vị.',(780,560),29,RED,show=.6,width=850)
    elif n==209:
        for j,(x,y) in enumerate([(310,380),(640,225),(970,420)]):
            s.rect((x-105,y,210,150),PAPER,GOLD,5,j*.2);s.text(str(j+1),(x,y+70),44,GOLD,show=j*.2)
        s.line([(220,580),(1080,125)],.7,RED,5);s.text('KHÔNG PHẢI MỘT BẢNG THÀNH TÍCH',(640,65),34,BLUE)
    elif n==214:
        s.image('O28',(450,185,360,350));s.text('QUÊN DÀNH GHẾ?',(245,170),30,RED,width=370);s.text('BỊ CHIẾM MẤT GHẾ?',(1020,470),28,RED,show=.3,width=400)
        s.line([(95,210),(405,210)],.5,RED,4);s.line([(835,510),(1210,510)],.8,RED,4);s.text('KHÔNG CÓ CĂN CỨ TỪ BẢN TRUYỆN NÀY',(640,65),31,BLUE,width=1160)
    elif n==231:
        for j,a in enumerate(['C_WZ','C_FL','C_SG']):s.image(a,(90+j*460,210,215,310),j*.25)
        s.text('CÙNG NGHI LỄ',(640,90),42,BLUE);s.text('GHI NHẬN',(200,565),27,BLUE,show=.4);s.text('NHẮC TỘI',(660,565),27,RED,show=.6);s.text('CHỊU TRÁCH NHIỆM',(1110,565),24,show=.8,width=320)
    elif n==232:
        s.image('O01',(425,125,430,420));s.image(cat,(100,370,240,230));s.text('VÌ SAO KẺ ĐỊCH VẪN ĐƯỢC PHONG THẦN?',(640,65),35,BLUE,width=1150);s.text('?',(640,320),100,RED,show=.2)
    elif n==237:
        s.image('O01',(130,90,540,470));s.image(cat,(900,235,300,350));s.text('ĐỌC CÁI TÊN',(400,220),32,BLUE);s.text('+ CUỘC ĐỜI',(400,330),34,RED,show=.5);s.line([(710,340),(865,340)],.6,BLUE,4,True)
    else:raise ValueError('Narrator beat has no authored composition: '+str(n))


def build_visual(s):
    k=s.kind;src=s.sources;labels=s.headline.split('~');dur=s.end-s.start
    if k=='wide':
        s.image(src[0],(35,60,1210,555));s.text(s.headline,(640,30),27,BLUE)
    elif k=='detail':
        if '@' in src[0]:
            w=float(src[0].split('@')[1].split(',')[2])
        else:w=1
        box=(50,120,1180,460) if w<=.55 else (255,125,770,430)
        s.image(src[0],box);s.text(s.headline,(640,62),32,BLUE)
        s.line([(460,595),(820,595)],.55,GOLD,4)
    elif k=='focus':
        s.window(src[0],(55,75,650,510));s.text(s.headline,(1000,300),35,RED,show=.35,width=440)
        s.line([(730,395),(950,395)],.7,GOLD,5,True)
    elif k=='portrait':
        person(s,src[0],(110,95,490,500));s.text(s.headline,(925,290),38,BLUE,show=.3,width=530)
        s.line([(735,400),(1110,400)],.65,GOLD,4)
    elif k=='object':
        s.heading()
        for j,a in enumerate(src):s.image(a,(150+j*620 if len(src)>1 else 420,145,350 if len(src)>1 else 440,400),j*.45)
        if len(src)>1:s.line([(540,365),(745,365)],.6,BLUE,4,True)
        else:s.line([(470,580),(810,580)],.6,GOLD,4)
    elif k=='reaction':
        reaction(s)
    elif k=='drop':
        s.text(s.headline,(640,70),36,RED);s.rect((160,515,960,34),'#b38e6a','#b38e6a',4)
        s.image(src[0],(460,190,360,320),move=[0,-115,.65])
        s.line([(430,535),(385,560)],.65,GOLD,4);s.line([(850,535),(895,560)],.65,GOLD,4)
    elif k in ('age','memory','contrast','emotion','loss','orders2','seas'):
        pair(s,src,labels,k)
    elif k=='scroll':
        s.image('O01',(300,48,680,550))
        for j,label in enumerate(labels):s.text(label,(640,220+j*(72 if len(labels)>2 else 105)),31 if len(label)<24 else 26,BLUE if j==0 else RED,show=.25+j*.65,width=450)
    elif k in ('orders','verdict'):
        s.image('cat14' if k=='orders' else 'cat24',(30,300,290,295))
        s.image(src[0],(370,120,260,325));s.image(src[1],(845,120,320,325),.5)
        for i,l in enumerate(labels):s.text(l,(500+i*500,500),29,RED if i==0 else BLUE,show=.5*i,width=420)
        s.line([(650,300),(810,300)],.8,BLUE,4,True)
        if k=='verdict':s.text('MỘT NGƯỜI · HAI THỜI ĐIỂM',(780,80),29,show=.1)
    elif k in ('mandate','mandate3'):
        boxes=[(70,180,310,340),(495,145,290,350),(930,200,270,340)]
        for j,a in enumerate(src):s.image(a,boxes[j],j*.4)
        s.line([(390,335),(480,335)],.4,BLUE,4,True);s.line([(800,335),(915,335)],.9,BLUE,4,True)
        s.heading();s.text('NGUYÊN THỦY',(220,570),23);s.text('PHÙ SẮC',(640,570),23,show=.4);s.text('TỬ NHA',(1060,570),23,show=.8)
    elif k=='mandate2':
        s.heading();s.image('O01',(120,125,480,420));person(s,'C_SG',(780,150,320,400),.4)
        s.line([(620,330),(755,330)],.7,BLUE,5,True)
    elif k in ('route','journey'):
        s.text('CON ĐƯỜNG ĐƯỢC GIAO' if k=='route' else 'CÁI GIÁ TRÊN ĐƯỜNG ĐI',(640,65),32,BLUE)
        for j,label in enumerate(labels):
            x=100+j*415;s.image(src[min(j,len(src)-1)],(x,170,250,280),j*.45);s.text(label,(x+125,510),26,show=j*.45,width=345)
            if j<2:s.line([(x+280,320),(x+380,320)],.4+j*.45,BLUE,4,True)
    elif k=='constellation':
        s.image('O01',(425,100,430,420));s.text('365',(640,280),96,RED,show=.2)
        for j,l in enumerate(['LÔI BỘ','CÁC BỘ','CHỨC TRÁCH','CHÍNH THẦN']):
            angle=j*math.pi/2;x=640+420*math.cos(angle);y=335+190*math.sin(angle)
            s.text(l,(x,y),27,BLUE,show=.55+j*.3,width=300);s.line([(640,360),(x,y)],.55+j*.3,GOLD,2)
    elif k=='levels':
        for j in range(2):
            s.rect((95,125+j*245,1090,200),PAPER,'#dacfbf',18);s.image(src[j],(130,140+j*245,180,165),j*.5);s.text(labels[j],(750,225+j*245),36,RED if j==0 else BLUE,show=j*.5,width=780)
        s.line([(640,335),(640,360)],.8,GOLD,4)
    elif k=='papers':
        s.image('cat15',(15,320,235,260));s.image('O10',(1070,470,180,130))
        for j in range(2):s.rect((280+j*450,100,380,475),'white','#d2c7b6',4)
        n=s.cues[0]
        if n>=41:s.text('AI THẮNG TRẬN?',(470,165),25,RED)
        if n>=42:s.text('AI NHẬN THẦN CHỨC?',(920,165),24,BLUE,show=.3)
        if n>=43:
            for i,(a,b) in enumerate([('CÙNG CÓ TÊN','CÙNG CÓ TÊN'),('NGƯỜI THẮNG','VĂN TRỌNG')]):
                s.text(a,(470,290+i*130),25,show=i*.5);s.text(b,(920,290+i*130),25,show=i*.5)
            s.line([(645,290),(745,290)],.3,BLUE,3)
    elif k=='kneel':
        # Explicit timed source substitution, not an anatomical tween.
        s.image('Y02@0.05,0.11,0.4,0.6',(50,80,680,500));s.text('QUỲ NGHE SẮC',(1010,310),34,RED,show=.2,width=430)
        s.line([(700,390),(1020,390)],.4,GOLD,5,True)
        s.add('switch',show=min(1.7,dur*.62),url=asset('Y02_B')['url'],box=[35,60,1210,555],role='character',source_id='Y02_B')
    elif k in ('rain','rainend'):
        s.image('B15',(30,55,1220,555))
        for j,l in enumerate(labels):s.rect((170,75+j*75,940,60),PAPER,PAPER,8,.4*j);s.text(l,(640,105+j*75),29,BLUE,show=.4*j)
        for j in range(38):
            x=90+(j*83)%1090;y=180+(j*67)%350
            c=s.line([(x,y),(x-7,y+22)],.5,'#86b3c1',3,reveal=.1);c['loop_move']=[-35,145,1.2,j*.071]
        for j in range(7):s.add('ellipse',(120+j*145,555+(j%2)*13,42,9),show=.8,fill=None,outline=BLUE,width=2)
    elif k=='scope':
        s.image(src[0],(80,155,280,345));s.window(src[1],(820,145,340,360),.6)
        s.image('C_WZ',(460,180,230,320));s.line([(465,420),(350,475)],.3,RED,4,True);s.line([(715,405),(860,475)],.9,BLUE,5,True)
        s.text(labels[0],(245,555),27,RED);s.text(labels[1],(995,555),27,BLUE,show=.6)
    elif k=='weather':
        for j in range(2):s.window(src[j],(70+j*640,150,500,340),j*.4);s.text(labels[j],(320+j*640,550),34,BLUE if j==0 else RED,show=j*.4)
        for j in range(15):
            c=s.line([(130+j*27,190),(125+j*27,210)],.4,BLUE,2,reveal=.1);c['loop_move']=[-10,180,.9,j*.13]
    elif k in ('relations','relations2'):
        if k=='relations':
            for j,a in enumerate(src[:2]):s.image(a,(70,70+j*280,225,260),j*.4);s.text(labels[j],(490,190+j*280),29,RED if j==0 else BLUE,show=.3+j*.4,width=370)
            s.image(src[2],(920,195,270,350),.3);s.line([(650,195),(900,330)],.7,RED,4,True);s.line([(650,475),(900,370)],1.0,RED,4,True)
        else:
            for j,a in enumerate(src):s.image(a,(110+j*730,130,330,375),j*.25);s.text(labels[j],(275+j*730,555),30,RED,show=j*.25)
            s.line([(465,330),(815,330)],.5,RED,5,True)
    elif k=='oath':
        s.image('C_SG',(60,135,315,420));s.rect((450,110,745,220),PAPER,RED,8)
        s.text('NẾU TIẾP TỤC CẢN ĐƯỜNG',(825,165),26,RED,width=690)
        s.text('ĐEM THÂN LẤP MẮT BIỂN BẮC HẢI',(825,245),29,show=.5,width=690)
        s.image('O11',(720,390,210,180),.8);s.line([(820,340),(820,390)],.7,BLUE,4,True)
        for row in range(3):s.line([(500+i*15,565+row*12+math.sin(i/3)*6) for i in range(46)],1,BLUE,2)
    elif k=='funnel':
        s.image('C_SG',(35,150,280,370));s.image('O01',(900,130,300,370),.8)
        s.text(s.headline,(640,65),33,BLUE)
        for j,name in enumerate(['NÚI','ĐẢO','NGƯỜI TU HÀNH']):
            s.text(name,(580,190+j*140),27,show=j*.3);s.line([(320,330),(450,190+j*140)],j*.3,RED,3,True);s.line([(735,190+j*140),(910,330)],.6+j*.3,BLUE,3,True)
    elif k=='ritual':
        for j,a in enumerate(src):
            s.add('switch',show=j*dur/3,url=asset(a)['url'],box=[35,105,1210,500],role='character',source_id=a)
            s.text(labels[j],(640,55),34,BLUE,show=j*dur/3)['until']=(j+1)*dur/3
    elif k=='causality':
        s.window(src[0],(30,115,590,390));s.window(src[1],(850,160,380,340),.5)
        s.text(labels[0],(320,555),28,RED);s.text(labels[1],(1040,555),27,BLUE,show=.5,width=400);s.line([(650,320),(820,320)],.7,RED,5,True)
    elif k in ('hierarchy','rank'):
        s.heading();s.image(src[0],(520,110,240,265));s.text(labels[0],(640,395),27,BLUE)
        s.line([(640,410),(640,440),(1060,440)],.6,BLUE,3);s.line([(640,440),(215,440)],.6,BLUE,3)
        for j in range(4):
            x=120+j*285;s.line([(x+90,440),(x+90,470)],.8,BLUE,3)
            if k=='rank' and j==0:s.image('C_XS',(x+20,468,135,125),.9)
            else:s.rect((x+35,475,110,70),PAPER,GOLD,9,.9)
        if len(labels)>1:s.text(labels[1],(640,600),25,BLUE,show=1,width=1100)
    elif k in ('paths','paths2'):
        s.image('cat24',(45,345,245,245))
        for j,l in enumerate(labels):
            x=365+j*310;s.image(src[j],(x,115+j*60,180,200),j*.35);s.text(l,(x+90,390+j*60),27,BLUE,show=j*.35,width=275);s.line([(275,510),(x+90,450 if j==0 else 470+j*45)],.45+j*.35,BLUE,3,True)
        if k=='paths':s.text('CON ĐƯỜNG KHÁC NHAU',(720,580),29,RED,show=s.cue_times.get(152,4.5),width=850)
    elif k=='origins':
        for j,a in enumerate(src):s.image(a,(100+j*440,115,210,310),j*.35)
        s.text(s.headline,(640,70),33,BLUE);s.rect((350,500,580,80),PAPER,GOLD,12,.8)
        s.text('KHÁC NHAU TRƯỚC KHI NHẬN CHỨC',(640,540),27,BLUE,show=.8)
        for j in range(3):s.line([(205+j*440,435),(640,495)],.55+j*.25,BLUE,3,True)
    elif k=='balance':
        s.heading();s.line([(640,180),(640,520)],.2,GOLD,6);s.line([(315,290),(965,290)],.4,BLUE,5)
        for j,l in enumerate(labels):s.rect((170+j*650,350,300,120),PAPER,GOLD,16,.6+j*.3);s.text(l,(320+j*650,410),35,RED if j==0 else BLUE,show=.6+j*.3);s.line([(320+j*650,290),(320+j*650,350)],.5,GOLD,3)
    elif k=='rope':
        s.heading();s.image('O16',(170,210,260,250),move=[-100,0,.65]);s.image('O17',(760,230,310,250),.5,move=[0,-130,1.1]);s.line([(460,320),(720,320)],.4,BLUE,4,True)
        s.text('DÂY RƠI SAU ĐIỂM CHẠM',(900,560),27,BLUE,show=.9,width=500)
    elif k=='pearls':
        s.heading();s.image('O16',(55,225,230,230));s.line([(300,340),(410,340)],.3,BLUE,4,True)
        for j in range(24):s.image('O18',(450+(j%6)*83,150+(j//6)*90,52,52),.45,move=[0,-65,.9])
        s.image('C_CB',(1000,285,190,260),1.2);s.line([(950,420),(1030,490)],1.1,BLUE,4,True);s.text('CAO BẢO THU LẤY',(1030,590),24,BLUE,show=1.2,width=360)
    elif k=='bypass':
        s.heading();s.image('O16',(460,210,220,240));s.image('O19',(770,235,330,260),.4,move=[220,0,.8]);s.line([(790,170),(680,140),(420,140),(250,270)],.6,RED,5,True)
        s.text('BINH KHÍ VƯỢT QUA',(630,565),33,RED,show=.8)
    elif k=='repeat':
        s.heading()
        for j,a in enumerate(src):
            s.image(a,(100+j*420,190,260,260),j*.35);s.text('LẦN '+str(j+1),(230+j*420,535),32,RED if j==2 else BLUE,show=.4+j*.35)
            x=230+j*420
            if j<2:s.line([(x-22,582),(x-6,595),(x+25,562)],.5+j*.35,BLUE,5)
            else:s.line([(x-18,563),(x+18,595)],1.2,RED,5);s.line([(x+18,563),(x-18,595)],1.2,RED,5)
    elif k=='sides':
        for j,a in enumerate(src):s.image(a,(160+j*650,110,300,410),j*.3);s.text(labels[j],(310+j*650,565),28,RED if j==0 else BLUE,show=j*.3,width=570)
        s.line([(640,130),(640,590)],.4,GOLD,3)
    elif k=='gates':
        for j,a in enumerate(src[:2]):s.image(a,(65+j*910,160,250,375))
        s.rect((430,140,420,415),PAPER,GOLD,7);s.rect((485,220,310,335),'#e6ddcc',GOLD,3)
        for j,l in enumerate(labels):s.text(l,(640,290+j*78),26,BLUE,show=.3+j*.5,width=310)
        s.line([(315,400),(420,400)],.4,BLUE,3,True);s.line([(960,400),(865,400)],.8,BLUE,3,True)
    elif k in ('oldlinks','newlinks','system','closingtableau'):
        for j,a in enumerate(src):
            boxes=[(500,75,270,300),(110,330,235,260),(920,320,235,260),(540,400,210,180)]
            s.image(a,boxes[j],j*.2)
        color=RED if k=='oldlinks' else BLUE
        s.line([(370,435),(530,280)],.4,color,4,True);s.line([(895,435),(750,280)],.8,color,4,True)
        s.text(s.headline.replace('~',' · '),(640,60),27,color,width=1150)
    elif k=='losses':
        s.heading()
        for j,a in enumerate(src):s.image(a,(110+j*420,190,260,285),j*.25);s.line([(120+j*420,490),(360+j*420,490)],.7+j*.3,RED,4)
    elif k=='obedience':
        s.window(src[0],(65,115,530,455));s.image('O01',(740,100,380,420),.3)
        for j,l in enumerate(labels):s.text(l,(930,280+j*80),28,BLUE if j==0 else RED,show=.4+j*.4,width=390)
    elif k=='criteria':
        s.image('O01',(35,95,420,420))
        for j,l in enumerate(labels):
            s.rect((550,110+j*120,620,85),PAPER,'#d5c5a9',10,j*.4);s.text(l,(850,153+j*120),32,BLUE,show=j*.4)
            s.line([(430,325),(530,153+j*120)],.3+j*.4,GOLD,2,True)
    elif k=='names':
        s.heading();s.image('O01',(450,120,380,415))
        for j,l in enumerate(['VĂN TRỌNG','PHI LIÊM · ÁC LAI','THÂN CÔNG BÁO','TRIỆU CÔNG MINH']):
            x=235 if j%2==0 else 1050;y=210+(j//2)*240;s.text(l,(x,y),27,BLUE,show=j*.3,width=390);s.line([(x+(150 if j%2==0 else -150),y),(640,y)],.3+j*.3,GOLD,2)
    else:raise ValueError('Unimplemented composition '+k)
    # Script-specific prop actions and information appear on their actual cue.
    n=s.cues[0] if s.cues else 0
    if k=='object':
        pictures=[c for c in s.layers if c['kind']=='image']
        if n in (53,57,77,138,170,207):
            pictures[0]['move']={53:[-260,0,.8],57:[0,-120,.6],77:[-220,0,.8],138:[-280,0,1],170:[-250,0,.65],207:[250,0,.8]}[n]
        if n==50:
            s.line([(810,400),(1070,250)],.3,BLUE,4,True);s.text('TRIỀU CA ?',(1060,190),28,BLUE,show=.5,width=320)
        elif n==53:
            s.line([(250,520),(1010,520)],.2,BLUE,4,True);s.rect((1020,430,45,105),'#b6ad9c','#b6ad9c',5,.7)
        elif n==57:
            s.line([(640,570),(640,480)],.2,BLUE,4,True);s.line([(580,490),(700,490)],.65,RED,5)
        elif n==66:
            c=s.text('SỬA CHÍNH SỰ · TÌM NGƯỜI HIỀN',(640,580),26,BLUE,show=.3);c['until']=dur*.6
        elif n==74:
            s.text('PHI LIÊM',(640,260),27,RED,show=.5);s.text('ÁC LAI',(640,350),27,RED,show=1)
        elif n==77:
            s.line([(820,410),(1050,410)],.5,BLUE,4,True);s.text('NHÀ CHU',(1050,330),30,BLUE,show=.7,width=300)
        elif n==109:s.text('THÂN CÔNG BÁO',(640,295),28,BLUE,show=.3,width=380)
        elif n==138:
            s.line([(840,400),(1100,400)],.5,RED,4,True);s.text('CHIẾN TRƯỜNG',(1030,535),26,RED,show=.65,width=390)
        elif n==213:
            s.line([(810,360),(1010,210)],.3,BLUE,4,True);s.line([(975,180),(1040,245)],.6,RED,5);s.text('ĐƯỜNG TU MONG MUỐN',(1010,125),25,BLUE,width=370)
        if n in (196,218,238):
            for c in s.layers:
                if c['kind']=='line':c['arrow']=False


def position(c,t):
    box=c.get('box',[0,0,0,0]).copy()
    if 'move' in c:
        dx,dy,d=c['move'];u=max(0,min(1,(t-c['show'])/d));u=u*u*(3-2*u);box[0]+=dx*(1-u);box[1]+=dy*(1-u)
    if 'loop_move' in c:
        dx,dy,d,phase=c['loop_move'];u=((t-c['show'])/d+phase)%1
        box[0]+=dx*u;box[1]+=dy*u
    return box


def wrapped(value,size,width,bold):
    result=[];d=ImageDraw.Draw(Image.new('RGB',(1,1)))
    for para in value.split('\n'):
        lines=['']
        for word in para.split():
            test=(lines[-1]+' '+word).strip()
            if d.textlength(test,font=font(size,bold))>width and lines[-1]:lines.append(word)
            else:lines[-1]=test
        result.extend(lines)
    return '\n'.join(result)


@lru_cache(maxsize=256)
def derivative(url):return Image.open(OUT/url).convert('RGBA')


def frame(s,t,subtitles=None):
    im=Image.new('RGBA',(1280,720),PAPER)
    for c in s.layers:
        if t<c['show'] or t>=c.get('until',1e9):continue
        d=ImageDraw.Draw(im);kind=c['kind']
        if kind in ('image','switch'):
            if kind=='switch':im=Image.new('RGBA',(1280,720),PAPER)
            src=derivative(c['url']);x,y,w,h=position(c,t);ratio=min(w/src.width,h/src.height);sw,sh=round(src.width*ratio),round(src.height*ratio)
            im.alpha_composite(src.resize((sw,sh),Image.Resampling.LANCZOS),(round(x+(w-sw)/2),round(y+(h-sh)/2)))
        elif kind=='text':
            text=wrapped(c['text'],c['size'],c['max_width'],c['bold']);d.multiline_text(c['xy'],text,font=font(c['size'],c['bold']),fill=c['color'],anchor='mm',align='center',spacing=7)
        elif kind in ('rect','ellipse'):
            x,y,w,h=position(c,t);b=(x,y,x+w,y+h)
            if kind=='rect':d.rounded_rectangle(b,radius=c['radius'],fill=c['fill'],outline=c['outline'],width=2)
            else:d.ellipse(b,fill=c['fill'],outline=c['outline'],width=c['width'])
        elif kind=='line':
            pts=c['points'];progress=max(0,min(1,(t-c['show'])/c['reveal']));out=[pts[0]];remaining=progress*sum(math.dist(a,b) for a,b in zip(pts,pts[1:]))
            for a,b in zip(pts,pts[1:]):
                length=math.dist(a,b);u=min(1,remaining/max(.001,length));out.append([a[0]+(b[0]-a[0])*u,a[1]+(b[1]-a[1])*u]);remaining-=length
                if remaining<=0:break
            if 'loop_move' in c:
                dx,dy,dur,phase=c['loop_move'];u=((t-c['show'])/dur+phase)%1;out=[[x+dx*u,y+dy*u] for x,y in out]
            if len(out)>1:
                d.line([tuple(p) for p in out],fill=c['color'],width=c['width'],joint='curve')
                if c['arrow'] and progress>.01:
                    a,b=out[-2:];ang=math.atan2(b[1]-a[1],b[0]-a[0]);d.polygon([b,(b[0]-16*math.cos(ang-.4),b[1]-16*math.sin(ang-.4)),(b[0]-16*math.cos(ang+.4),b[1]-16*math.sin(ang+.4))],fill=c['color'])
    d=ImageDraw.Draw(im);d.rectangle((0,630,1280,720),fill=PAPER)
    if subtitles:
        absolute=s.start+t;cue=next((a for a in subtitles if a['start']<=absolute<a['end']),None)
        if cue:d.multiline_text((640,676),wrapped(cue['text'],23,1180,False),font=font(23),fill=INK,anchor='mm',align='center',spacing=4)
    return im.convert('RGB')


FAMILIES={
    'court':{'K01','K02','K03'},'kunlun':{'B01','B02','Y08','Y09','K10','K12'},
    'dais':{'B03','B16','Y01','Y02','Y02_B','K30','K31'},'retreat':{'K04','K05','B04','X01'},
    'fire':{'B05','X02','Y03','K06'},'dream':{'B06','K07','K08','K09'},
    'forest':{'B07','K11'},'sea':{'B08','E04','K32','X04'},
    'cave':{'B09','X06','K14','K15','Y05'},'camp':{'B10','K17','K18','Y06','Y07','K16'},
    'chess':{'B11','K19','K20','K21','K22','X07'},'gate':{'B12','K24'},
    'zhou':{'B13','K25'},'field':{'B15','X03','X08','K28'},'qi':{'K27'},
}


def family(ident):return next((k for k,v in FAMILIES.items() if ident in v),ident)


def native_project(scenes,subs,audio_duration):
    """Editable Studio document, with roles preserved; pending user/aesthetic QC."""
    result={'schema':1,'name':'Mỏ Đen · Tập 2 · Phong Thần · bản dựng lại chờ duyệt','width':1280,'height':720,'fps':24,'audio':[{'id':'voice_H','file':'../voice_direction/Mo_Den_Phong_Than_Dien_Nghia_Custom_H_1_25x.wav','start':OFFSET,'duration':audio_duration,'gain':1}],
            'subtitles':subs,'subtitle_style':{'enabled':True,'size':23,'font':'Segoe UI','color':INK,'background':False,'y':.98},'references':[],'duck_music':False,'allow_draft':True,'scenes':[],
            'production_approval':{'status':'awaiting_user_edit_review','full_render_authorized':False,'new_voice_generated':False,'quality_review':'review_notes.md'}}
    for i,s in enumerate(scenes):
        sc={'id':f'pt_v2_{i:03}','name':f'{i:03} · {s.headline.replace("~"," / ")}','start':s.start,'duration':s.end-s.start,'background':'white','background_color':PAPER,'effects':[],'camera':{'x':640,'y':360,'zoom':1,'keys':{}},'objects':[],
            'editorial':{'chapter':s.chapter,'cue_ids':s.cues,'voice_text':' '.join(x['text'] for x in subs if x['source_cue'] in s.cues),'purpose':s.purpose,'composition':s.kind,'background_family':s.dominant_family,'review_image':f'review/shot_{i:03}.jpg'}}
        for j,c in enumerate(s.layers):
            kind=c['kind'];show=c['show'];end=min(s.end-s.start,c.get('until',s.end-s.start))
            if show>=end:continue
            o={'id':f'pt_v2_{i:03}_{j:03}','kind':'image' if kind in ('image','switch') else 'text' if kind=='text' else 'shape','name':c.get('text',c.get('source_id',kind)),
                'x':640,'y':360,'scale':1.,'rotation':0.,'opacity':1.,'layer':j,'start':show,'end':end,'keys':{},'width':1280,'height':720,'role':c.get('role','graphic')}
            if kind in ('image','switch'):
                x,y,w,h=c['box'];o.update(file=c['url'],x=x+w/2,y=y+h/2,width=w,height=h,fit='contain',source_id=c['source_id'],supplied_artwork=True)
                if kind=='switch':
                    for prior in sc['objects']:prior['end']=min(prior['end'],show)
                if 'move' in c:
                    dx,dy,d=c['move'];o['keys']={'x':[{'t':show,'v':o['x']+dx},{'t':min(end,show+d),'v':o['x'],'ease':'ease_in_out'}],'y':[{'t':show,'v':o['y']+dy},{'t':min(end,show+d),'v':o['y'],'ease':'ease_in_out'}]}
            elif kind=='text':o.update(text=c['text'],x=c['xy'][0],y=c['xy'][1],width=c['max_width'],height=180,font_size=c['size'],bold=c['bold'],color=c['color'],fill='transparent')
            elif kind=='line':
                # Native path reveal and arrow head represented as a second short path.
                o.update(shape='path',x=0,y=0,points=c['points'],color=c['color'],stroke=c['width'],fill='transparent',reveal=True,enter_duration=c['reveal'],keys={})
                if c['arrow']:
                    a,b=c['points'][-2:];ang=math.atan2(b[1]-a[1],b[0]-a[0]);points=[[b[0]-16*math.cos(ang-.4),b[1]-16*math.sin(ang-.4)],b,[b[0]-16*math.cos(ang+.4),b[1]-16*math.sin(ang+.4)]]
                    sc['objects'].append({**o,'id':o['id']+'_head','points':points,'start':min(end-.001,show+c['reveal']),'keys':{}})
                if 'loop_move' in c:
                    dx,dy,period,phase=c['loop_move'];keys={'x':[],'y':[]}
                    for z in range(math.ceil((end-show)/period)+1):
                        for off,fac in [(0,0),(period-.001,1)]:
                            t=show+z*period+off
                            if t<=end:keys['x'].append({'t':t,'v':dx*fac});keys['y'].append({'t':t,'v':dy*fac})
                    o['keys'].update(keys)
            else:
                x,y,w,h=c['box'];o.update(shape='ellipse' if kind=='ellipse' else 'card',x=x+w/2,y=y+h/2,width=w,height=h,fill=c['fill'] or 'transparent',color=c['outline'],stroke=c.get('width',2),radius=c.get('radius',0))
            sc['objects'].append(o)
        sc['objects'].append({'id':f'pt_v2_{i:03}_caption_band','kind':'shape','name':'Vùng dành cho phụ đề','shape':'card','x':640,'y':676,'width':1280,'height':92,'fill':PAPER,'color':PAPER,'stroke':0,'scale':1.,'rotation':0.,'opacity':1.,'layer':10000,'start':0.,'end':s.end-s.start,'keys':{},'role':'graphic'})
        result['scenes'].append(sc)
    from studio.project import validate
    validate(result);return result


def main():
    OUT.mkdir(exist_ok=True);(OUT/'media').mkdir(exist_ok=True);(OUT/'review').mkdir(exist_ok=True)
    load_assets();r=json.loads((P/'voice_direction/report_phong_than.json').read_text(encoding='utf-8'))
    timeline=r['timeline'];cues={a['id']:a for a in timeline};audio_duration=r['final_duration_seconds']
    scenes=[];covered=[]
    intro=Scene(0,OFFSET,'reaction',['13'],'MỎ ĐEN · PHONG THẦN','Giới thiệu rất ngắn rồi vào ngay nghịch lý, không giữ intro phong cảnh.',[],1);build_visual(intro);scenes.append(intro)
    for row in (OUT/'edit_plan.txt').read_text(encoding='utf-8').splitlines():
        if not row or row.startswith('#'):continue
        ids,kind,spec,headline,purpose=row.split('|');aa,_,bb=ids.partition('-');ids=list(range(int(aa),int(bb or aa)+1));covered+=ids
        # Asset specs use commas inside normalized crop coordinates. Split only at a new asset ID.
        import re
        sources=re.split(r',(?=[A-Z][A-Za-z0-9_]*(?:@|,|$))',spec) if '@' in spec else spec.split(',')
        a=cues[ids[0]];b=cues[ids[-1]];start=OFFSET+a['start_seconds'];end=OFFSET+(cues[ids[-1]+1]['start_seconds'] if ids[-1]<243 else audio_duration)
        s=Scene(start,end,kind,sources,headline,purpose,ids,a['section_num']);s.cue_times={n:OFFSET+cues[n]['start_seconds']-start for n in ids};build_visual(s);scenes.append(s)
    if covered!=list(range(1,244)):raise ValueError('Cue coverage is not exact')
    outro=Scene(scenes[-1].end,scenes[-1].end+2,'reaction',['08'],'MỎ ĐEN','Kết ngắn sau lời kể, giữ nhận diện không thêm thông điệp mới.',[],9);build_visual(outro);scenes.append(outro)
    subs=[{'id':'pt_v2_sub_'+str(c['id']),'source_cue':c['id'],'start':OFFSET+c['start_seconds'],'end':OFFSET+c['end_seconds'],'text':c['spoken_text'],'role':'Narrator'} for c in timeline]
    data={'version':2,'title':'Mỏ Đen · Tập 2: Phong Thần','duration':scenes[-1].end,'audio_offset':OFFSET,'audio':'../voice_direction/Mo_Den_Phong_Than_Dien_Nghia_Custom_H_1_25x.mp3','voice_speed_applied_here':1.,'scenes':[],'subtitles':subs,'full_render_authorized':False,'full_video_rendered':False}
    background_uses=defaultdict(list)
    for i,s in enumerate(scenes):
        # Count broad crops and state variants together, including source substitutes.
        dominant=[]
        for c in s.layers:
            if c['kind'] not in ('image','switch'):continue
            w,h=c['box'][2:];meta=next(v for v in used.values() if v['url']==c['url']);ident=meta['source_id'];crop=meta['crop']
            if family(ident)!=ident and w*h>=1280*630*.30 and (not crop or (crop[2]>.55 and crop[3]>.5)):dominant.append(family(ident))
        for fam in sorted(set(dominant)):
            s.dominant_family=fam;background_uses[fam].append({'shot':i,'start':s.start,'end':s.end,'purpose':s.purpose,'image':f'review/shot_{i:03}.jpg'})
        entry={'index':i,'start':s.start,'end':s.end,'kind':s.kind,'headline':s.headline,'purpose':s.purpose,'cue_ids':s.cues,'chapter':s.chapter,'sources':s.sources,'layers':s.layers,'dominant_background_families':sorted(set(dominant))}
        data['scenes'].append(entry)
        sample=min(s.end-s.start-.05,max(.15,(s.end-s.start)*.65));frame(s,sample,subs).save(OUT/f'review/shot_{i:03}.jpg',quality=88)
        # Start/end evidence exposes actual timed changes; no MP4 encoding.
        if s.kind not in ('wide','detail','focus','portrait','object','reaction'):
            for label,t in [('in',.05),('out',max(.05,s.end-s.start-.08))]:frame(s,t,subs).save(OUT/f'review/shot_{i:03}_{label}.jpg',quality=84)
    dump(OUT/'timeline.json',data);dump(OUT/'assets_manifest.json',list(used.values()))
    dump(OUT/'project.json',native_project(scenes,subs,audio_duration))
    def stamp(t):
        ms=round(t*1000);sec,ms=divmod(ms,1000);minute,sec=divmod(sec,60);hour,minute=divmod(minute,60)
        return f'{hour:02}:{minute:02}:{sec:02},{ms:03}'
    (OUT/'subtitles.srt').write_text('\n\n'.join(f"{i+1}\n{stamp(c['start'])} --> {stamp(c['end'])}\n{c['text']}" for i,c in enumerate(subs))+'\n',encoding='utf-8')
    audit={'method':'Draft screen counts broad images/crops with >=30% content box and >55% source width and >50% source height. True face/hand/prop details and small diagram windows need visual verification, never automatic aesthetic approval. State variants grouped.','families':background_uses,'over_default_limit':{k:v for k,v in background_uses.items() if len(v)>3},'not_aesthetic_approval':True}
    dump(OUT/'repetition_audit.json',audit)
    with (OUT/'shot_list.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f);w.writerow(['shot','start','end','chapter','cues','composition','sources','purpose','spoken_text'])
        for i,s in enumerate(scenes):w.writerow([i,round(s.start,3),round(s.end,3),s.chapter,','.join(map(str,s.cues)),s.kind,';'.join(s.sources),s.purpose,' '.join(cues[n]['spoken_text'] for n in s.cues)])
    for n in range(0,len(scenes),12):
        board=Image.new('RGB',(1440,4*239),'#e9e4da');d=ImageDraw.Draw(board)
        for j,s in enumerate(scenes[n:n+12]):
            i=n+j;x=(j%3)*480;y=(j//3)*239;im=Image.open(OUT/f'review/shot_{i:03}.jpg');im.thumbnail((480,210));board.paste(im,(x,y));d.text((x+6,y+212),f'{i:03} · {s.start//60:02.0f}:{s.start%60:04.1f} · {s.kind}',font=font(15),fill=INK)
        board.save(OUT/f'review/board_{n//12+1:02}.jpg',quality=91)
    summary={'shots':len(scenes),'duration_seconds':scenes[-1].end,'cues':len(covered),'assets':len(used),'compositions':dict(Counter(s.kind for s in scenes)),'background_family_counts':{k:len(v) for k,v in background_uses.items()},'over_limit':list(audit['over_default_limit']),'missing_sources':0,'full_video_rendered':False,'user_approved':False}
    dump(OUT/'build_report.json',summary)
    print(json.dumps(summary,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
