"""Purposeful, presenter-free vector direction. All layers remain editable in Studio."""
import sys, json, math, copy
from pathlib import Path
from revision2_story import DEST, ROOT, ORIGINAL, STORY, SOURCES
sys.path.insert(0,str(ROOT))
from studio.project import new_project, new_scene, new_object, uid, save
from studio.explainer import image_item, text_item, item
from studio.directing import preflight
from studio.subtitles import write as write_srt

ART = DEST/'art'
INK, PAPER = '#292d2a', '#fffefb'
STONE, SHADE, WATER, RED = '#e9d5ad', '#cfb27d', '#cae2e5', '#b96342'

def path(d, fill='none', stroke=INK, sw=2.4, extra=''):
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" {extra}/>'

def poly(points, fill, stroke=INK, sw=2.4):
    return path('M'+'L'.join(f'{x:.2f} {y:.2f}' for x,y in points)+'Z',fill,stroke,sw)

def ellipse(x,y,rx,ry,fill='none',stroke=INK,sw=2.4):
    return f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'

def svg(name, body, w, h):
    (ART/(name+'.svg')).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{body}</svg>',encoding='utf-8')

def make_art():
    ART.mkdir(parents=True,exist_ok=True)
    # Lotus-bud tower: a tapered, tiered outline with niches, ribs and petal shoulders.
    cx, ground, height = 100, 305, 278
    left=[(cx-65,ground),(cx-65,ground-72),(cx-50,ground-81),(cx-50,ground-128),
          (cx-39,ground-138),(cx-37,ground-179),(cx-27,ground-189),(cx-24,ground-221),
          (cx-14,ground-230),(cx-11,ground-249),(cx,ground-height)]
    points=left+[(2*cx-x,y) for x,y in left[-2::-1]]
    b=poly(points,STONE,sw=2.8)
    b+=poly([(100,27),(111,56),(114,75),(124,84),(127,116),(137,126),(139,167),(150,177),(150,224),(165,233),(165,305),(125,305),(124,228),(119,169),(112,119)],SHADE,'none')
    for level,half in [(72,62),(128,47),(179,34),(221,21),(249,10)]:
        y=ground-level
        b+=path(f'M{cx-half} {y}Q100 {y+3} {cx+half} {y}',sw=2)
        b+=path(f'M{cx-half+3} {y+7}Q100 {y+10} {cx+half-3} {y+7}',stroke='#ad956a',sw=1.1)
    for frac,half in [(.29,46),(.50,34),(.68,24),(.82,15)]:
        y=ground-height*frac
        for side in [-1,1]:
            x=cx+side*half
            b+=path(f'M{x} {y+9}Q{x+side*10} {y-3} {x-side*3} {y-29}Q{x-side*10} {y-11} {x-side*7} {y+4}',STONE,sw=1.7)
    b+=path('M81 305V252Q100 230 119 252V305Z','#776c52',sw=2)
    b+=path('M87 305V255Q100 241 113 255V305','#b19b72',sw=1.2)
    for x in [49,59,141,151]:
        b+=path(f'M{x} 292V247',stroke='#7d7159',sw=1.3)
    for x,y,w,h in [(88,177,24,31),(91,129,18,23),(94,90,12,16)]:
        b+=path(f'M{x} {y+h}V{y+6}Q{x+w/2} {y-5} {x+w} {y+6}V{y+h}Z','#e0c593',sw=1.4)
    b+=path('M25 305H175V319H25Z','#e5cfaa',sw=2.5)
    b+=path('M20 320H180V333H20Z','#c8ad7e',sw=2.5)
    svg('lotus_tower',b,200,340)
    # The long galleries and ascending terraces give the temple a specific silhouette.
    b=path('M44 24H956L983 66H17Z',STONE,sw=2.8)
    b+=path('M23 70H977V117H23Z','#f2e5c8',sw=2.8)
    for x in range(42,966,29):
        if 447<x<553:continue
        b+=path(f'M{x} 74V111M{x+11} 74V111',sw=1.7)
        b+=path(f'M{x+2} 81H{x+9}',stroke='#b99d70',sw=1)
    b+=path('M15 119H985V135H15Z','#d5bc8f',sw=2.8)
    b+=path('M4 137H996V154H4Z','#e8d4af',sw=2.8)
    b+=path('M0 157H1000V176H0Z','#cbb187',sw=2.8)
    b+=path('M465 44H535L566 190H434Z','#f6ecd7',sw=2.8)
    for yy in range(62,190,10):
        width=35+(yy-44)*.21
        b+=path(f'M{500-width} {yy}H{500+width}',sw=1.3)
    for x in [20,230,780]:
        b+=path(f'M{x} 162h78m-61 8h45',stroke='#af9975',sw=1)
    svg('galleries',b,1000,205)
    # A plan makes the five positions unambiguous; it is a schematic, not a survey.
    b=path('M54 49L946 51L944 548L53 550Z','#f4ead5',sw=2.8)
    for inset in [20,45]:
        b+=path(f'M{54+inset} {49+inset}H{946-inset}V{550-inset}H{54+inset}Z',fill='none',stroke='#a2957a',sw=1.2)
    b+=path('M235 130H765V470H235Z','#fffbef',sw=2.4)
    b+=path('M470 470H530V596H470Z','#f9f3e6',sw=2)
    for x,y in [(300,175),(700,175),(300,425),(700,425),(500,300)]:
        b+=path(f'M{x-40} {y-36}H{x+40}V{y+36}H{x-40}Z',STONE,sw=2)
        b+=ellipse(x,y,23,23,'#f8eccf',sw=1.8)
        b+=path(f'M{x-10} {y}H{x+10}M{x} {y-10}V{y+10}',stroke='#a1885c',sw=1.5)
    svg('plan',b,1000,600)
    svg('ring',ellipse(60,60,48,48,'none',RED,3),120,120)
    # The same five anchors are used for the symbolic peaks and architectural towers.
    b=path('M20 302Q43 234 61 180L87 112L111 31Q132 72 143 105L170 164L199 215L230 302Z','#aab7a1',sw=2.8)
    b+=path('M111 31L119 134L148 178L145 225L190 302H230L199 215L170 164L143 105Z','#8f9f88','none')
    b+=path('M111 31L87 112L104 103L118 136L122 110L143 105',fill='none',sw=2)
    b+=path('M87 112L64 207L94 177L73 253M143 105L160 207L144 194L162 263',sw=1.4)
    b+=path('M35 305Q122 311 218 305',sw=2.2)
    svg('peak',b,250,330)
    def shifted(points):return [(x+600,y+350) for x,y in points]
    outer=[(-560,-165),(145,-345),(560,165),(-145,345)]
    inner=[(-405,-118),(105,-247),(405,118),(-105,247)]
    water=poly(shifted(outer),WATER,sw=2.7)+poly(shifted(inner),PAPER,sw=2.6)
    for x,y in [(-400,-135),(-210,-235),(300,-40),(410,150),(180,265),(-280,100),(-125,280)]:
        water+=path(f'M{x+570} {y+350}q14 -6 28 0t28 0',stroke='#81b0b6',sw=1.7)
    svg('moat_iso',water,1200,700)
    land=poly(shifted(inner),'#f0e5ce',sw=2.7)
    for k in [.75,.60]:
        land+=poly(shifted([(x*k,y*k) for x,y in inner]),'#e7d5b1',sw=2)
    svg('land_iso',land,1200,700)
    # Frontal water and a continuous causeway for the moving viewpoint.
    b=path('M0 28Q320 19 640 28T1280 28V270H0Z',WATER,sw=2)
    for x,y in [(50,80),(330,100),(900,60),(1110,140),(80,205),(1000,230)]:
        b+=path(f'M{x} {y}q20 -7 40 0t40 0',stroke='#82aeb4',sw=1.6)
    svg('water_front',b,1280,270)
    b=path('M274 0H326L590 280H10Z','#eadabd',sw=2.7)
    b+=path('M283 0L52 280M317 0L548 280',sw=2)
    for yy in [25,55,94,143,204,278]:
        half=26+yy*.98
        b+=path(f'M{300-half} {yy}H{300+half}',stroke='#b59d76',sw=1.2)
    svg('causeway',b,600,280)

class Stage:
    def __init__(self,scene):self.s=scene;self.L=scene['duration']
    def add(self,o,start=0,end=None,layer=20,parent=None):
        o.update(start=start,end=self.L if end is None else end,layer=layer)
        if parent:o['parent']=parent['id']
        self.s['objects'].append(o)
        return o
    def group(self,x,y,scale=1,parent=None,name='Composition'):
        o=new_object('group',name,x,y);o['scale']=scale
        return self.add(o,parent=parent)
    def art(self,name,x,y,w,h,layer=20,parent=None,start=0,end=None):
        return self.add(image_item(str(ART/(name+'.svg')),x,y,w,h),start,end,layer,parent)
    def text(self,text,x,y,w=1080,h=70,size=34,start=0,end=None,color=INK,font='Segoe UI',bold=False,parent=None):
        return self.add(text_item(text,x,y,w,h,size,color=color,font=font,bold=bold),start,end,85,parent)
    def key(self,o,k,points,ease='ease_in_out'):
        o.setdefault('keys',{})[k]=[dict(t=max(0,min(self.L,float(t))),v=v,ease=ease) for t,v in points]
        return o
    def fade(self,o,start,end,a=0,b=1):
        o['opacity']=a
        return self.key(o,'opacity',[(0,a),(start,a),(end,b)])
    def line(self,points,start=0,duration=.7,color=RED,sw=2.8,parent=None):
        o=item('shape','Meaningful connecting line',0,0,1280,720,shape='path',points=points,color=color,stroke=sw,reveal=True,enter_duration=duration)
        return self.add(o,start,layer=75,parent=parent)

def front(st,x=640,y=460,scale=1,assemble=False):
    root=st.group(x,y,scale,name='Five towers and rising galleries')
    specs=[(-300,-64,159), (300,-64,159),(-160,-38,208),(160,-38,208),(0,-3,280)]
    for j,(xx,base,h) in enumerate(specs):
        foot=st.group(xx,base,parent=root,name=f'Tower {j+1}, anchored to its footing')
        st.art('lotus_tower',0,-h/2,h*200/340,h,20+j,parent=foot)
        if assemble:
            t=.12+j*.12
            st.fade(foot,t,t+.4)
            st.key(foot,'y',[(0,base+22),(t,base+22),(t+.5,base)])
    st.art('galleries',0,16,1000,205,40,parent=root)
    return root

ANCHORS=[(-100,-85,155),(255,-20,155),(-255,65,155),(100,130,155),(0,0,235)]
def iso(st,x=640,y=390,scale=1,mode='tower',water=False,land=True):
    root=st.group(x,y,scale,name='Shared quincunx composition')
    if water:st.art('moat_iso',0,0,1200,700,2,parent=root)
    if land:st.art('land_iso',0,0,1200,700,4,parent=root)
    feet=[]
    for j,(xx,base,h) in enumerate(ANCHORS):
        foot=st.group(xx,base,parent=root,name=f'Meru correspondence {j+1}')
        asset='peak' if mode=='peak' else 'lotus_tower'
        hh=h*1.08 if mode=='peak' else h
        ww=hh*(250/330 if mode=='peak' else 200/340)
        st.art(asset,0,-hh/2,ww,hh,20+round((base+85)/10),parent=foot)
        feet.append(foot)
    return root,feet

def plan(st,x=640,y=360,scale=1):
    root=st.group(x,y,scale,name='Center and four corners')
    st.art('plan',0,0,1000,600,parent=root)
    return root

def build():
    make_art()
    timing=json.loads((DEST/'voice_timing.json').read_text(encoding='utf-8'))
    cues=timing['cues']
    by_scene=[[c for c in cues if c['scene']==i] for i in range(len(STORY))]
    boundaries=[0]+[c[0]['start']-.14 for c in by_scene[1:]]+[60]
    p=new_project('Angkor Wat · Bản đồ có thể bước vào',60,1920,1080)
    p.update(scenes=[],fps=30,render_profile='final',encoder_threads=2,audio_rate=48000,audio_channels=2,audio=[],subtitles=[],duck_music=True)
    p['subtitle_style'].update(size=26,font='Segoe UI',color=INK,background=False,y=.974)
    shots=[]
    for i,(a,b) in enumerate(zip(boundaries,boundaries[1:])):
        s=new_scene(STORY[i]['name'],b-a)
        s.update(start=a,background='white',background_color=PAPER,objects=[],style='ink_cosmogram_no_presenter')
        p['scenes'].append(s)
        st=Stage(s);L=st.L
        phrases=by_scene[i]
        marks=[max(0,c['start']-a) for c in phrases]
        if i==0:
            root=front(st,640,465,1.02,assemble=True)
            st.text('VÌ SAO LÀ NĂM?',640,81,size=40,bold=True,end=marks[1])
            st.text('NGÔI ĐỀN HAY MỘT BẢN ĐỒ?',640,81,size=37,bold=True,start=marks[1])
            # One measured pullback exposes all five towers, then holds for reading.
            st.key(root,'scale',[(0,1.10),(1.4,1.02)])
            st.text('ANGKOR WAT',640,593,size=20,h=35,color='#77796e',end=marks[-1])
        elif i==1:
            temple=front(st,345,440,.53)
            top=plan(st,950,385,.48)
            st.text('CAMPUCHIA · THẾ KỶ XII',640,75,size=25,bold=True,end=marks[1])
            st.text('Đền thờ Vishnu',345,583,w=500,h=45,size=27,end=marks[1])
            st.text('Nhìn từ trên xuống',950,583,w=520,h=45,size=27,end=marks[1])
            t=marks[1]
            st.fade(temple,t,t+.6,1,0)
            st.key(top,'x',[(0,950),(t,950),(t+.8,640)])
            st.key(top,'y',[(0,385),(t,385),(t+.8,363)])
            st.key(top,'scale',[(0,.48),(t,.48),(t+.8,.86)])
            st.text('ĐỔI GÓC NHÌN',640,78,size=35,bold=True,start=t)
        elif i==2:
            top=plan(st,640,363,.86)
            st.text('1 Ở GIỮA · 4 Ở GÓC',640,77,size=34,bold=True,end=marks[1])
            locations=[(0,0),(-200,-125),(200,-125),(-200,125),(200,125)]
            for j,(xx,yy) in enumerate(locations):
                ring=st.art('ring',xx,yy,95,95,60,parent=top)
                t=.15 if j==0 else .7+j*.24
                st.fade(ring,t,t+.25)
            t=marks[1]
            st.key(top,'x',[(0,640),(t,640),(t+.8,330)])
            st.key(top,'scale',[(0,.86),(t,.86),(t+.8,.54)])
            mountains,_=iso(st,950,420,.66,mode='peak')
            st.fade(mountains,t+.15,t+.8)
            st.text('NĂM VỊ TRÍ · NĂM ĐỈNH',640,77,size=34,bold=True,start=t)
            st.text('Bố cục ngôi đền',330,590,w=500,size=24,start=t)
            st.text('Núi Meru',950,590,w=500,size=24,start=t)
        elif i==3:
            mountains,feet=iso(st,950,420,.66,mode='peak')
            st.key(mountains,'x',[(0,950),(.8,640)])
            st.key(mountains,'y',[(0,420),(.8,380)])
            st.key(mountains,'scale',[(0,.66),(.8,.88)])
            t=marks[1]
            st.text('MERU · NÚI THIÊNG Ở TRUNG TÂM',640,77,size=32,bold=True,end=t)
            st.text('Ý NIỆM TRỞ THÀNH KIẾN TRÚC',640,77,size=33,bold=True,start=t)
            temple,_=iso(st,640,380,.88,mode='tower')
            st.fade(temple,t,t+.85)
            st.fade(mountains,t,t+.85,1,0)
            st.text('Cùng năm vị trí',640,617,size=23,h=35,color='#68715e',start=t)
        elif i==4:
            # Revealing the moat by pulling out is the explanation, not decoration.
            temple,_=iso(st,640,380,.88,mode='tower')
            water=st.art('moat_iso',0,0,1200,700,2,parent=temple)
            st.fade(water,.15,1.2)
            st.key(temple,'scale',[(0,.88),(1.65,.72)])
            st.key(temple,'y',[(0,380),(1.65,354)])
            st.text('KÉO GÓC NHÌN RA XA',640,77,size=33,bold=True,end=marks[1])
            st.text('HÀO NƯỚC → ĐẠI DƯƠNG',640,77,size=34,bold=True,start=marks[1])
            # Annotation terminates at the water, making the enclosure legible.
            t=marks[1]+.4
            st.line([(1020,545),(1010,510),(966,486)],start=t,duration=.6,color='#55848c',sw=2)
            st.text('bao quanh',1090,560,w=220,h=40,size=23,start=t,color='#55848c',font='Segoe Print')
        elif i==5:
            world=st.group(640,350,.98,name='Viewpoint travelling along the causeway')
            st.art('water_front',0,158,1500,315,2,parent=world)
            st.art('causeway',0,160,620,290,5,parent=world)
            temple=front(st,0,10,.72)
            temple['parent']=world['id']
            st.text('BƯỚC VÀO KHÔNG GIAN THIÊNG',640,76,size=32,bold=True)
            # Camera travels toward the sanctuary along the existing causeway.
            st.key(world,'scale',[(0,.98),(L-.6,1.18)])
            st.key(world,'y',[(0,350),(L-.6,404)])
            st.line([(0,285),(0,199),(0,120),(0,56)],start=.4,duration=L*.65,sw=2,color=RED,parent=world)
        else:
            st.art('water_front',640,582,1250,170,2)
            root=front(st,640,454,.94)
            # Match the opening composition; the correspondence is now the payoff.
            st.text('5 THÁP · 5 ĐỈNH NÚI',640,75,size=34,bold=True,end=marks[1])
            st.text('MỘT VŨ TRỤ BẰNG ĐÁ',640,75,size=40,bold=True,start=marks[1])
            st.text('Hào nước · Đại dương',640,615,size=23,h=34,color='#426c73',end=marks[1])
            st.text('Bản đồ có thể bước vào',640,605,size=29,h=50,font='Segoe Print',start=marks[1])
            st.key(root,'scale',[(0,.94),(1.2,.94),(L-1,1.0)])
        if i in (5,6):
            # Preserve a quiet reading area while the viewpoint moves through water.
            st.add(item('shape','Clear subtitle reading area',640,682,1500,92,shape='card',fill=PAPER,color=PAPER,stroke=0),layer=80)
        for cue in phrases:
            p['subtitles'].append(dict(id=uid(),start=cue['start'],end=cue['end'],text=cue['text'],role='Narrator',scene_id=s['id']))
        shots.append(dict(scene=i+1,start=a,end=b,name=s['name'],purpose=STORY[i]['purpose'],narration=STORY[i]['text'],phrase_timings=phrases))
    p['audio']=[dict(id='narration',name='Hải Đăng · VieNeu-TTS',file=str(DEST/'narration.wav'),start=0,duration=60,group='voice',volume=1),
                dict(id='music',name='Nhạc gảy nguyên bản, nền nhẹ',file=str(ORIGINAL/'music_original.wav'),start=0,duration=60,group='music',volume=.28,fade_in=1.2,fade_out=2)]
    assert not preflight(p,DEST),preflight(p,DEST)
    assert not any(o['kind']=='character' or 'host' in str(o.get('file','')) for s in p['scenes'] for o in s['objects'])
    saved=save(p,DEST/'project.json',DEST)
    write_srt(p['subtitles'],DEST/'phu_de.srt')
    (DEST/'kich_ban.txt').write_text('\n\n'.join(x['text'] for x in STORY),encoding='utf-8')
    (DEST/'shot_list.json').write_text(json.dumps(shots,ensure_ascii=False,indent=2),encoding='utf-8')
    (DEST/'sources.json').write_text(json.dumps(SOURCES,ensure_ascii=False,indent=2),encoding='utf-8')
    (DEST/'DAO_DIEN.md').write_text('''# Angkor Wat — Bản đồ có thể bước vào

Luận điểm duy nhất: bố cục năm tháp và hào nước diễn đạt một mô hình vũ trụ của Ấn Độ giáo.

Điểm nhìn dẫn chuyện thay cho người thuyết trình trên hình. Không có nhân vật chỉ tay, miệng nói, ngôi sao trang trí, bộ đếm cảnh hay hiệu ứng bật nảy tùy tiện.

Mỗi lần cắt có nhiệm vụ: đặt câu hỏi → đổi góc nhìn → nhận ra một tâm và bốn góc → đối chiếu núi/tháp ở cùng vị trí → kéo ra để thấy nước bao quanh → tiến theo đường vào đền → trở về hình mở đầu và trả lời câu hỏi.

Nét mực đen mảnh, nền trắng ngà, đá màu cát, nước xanh xám, núi xanh rêu. Màu đỏ đất chỉ dùng cho đường nhấn giải thích. Chữ ngắn để gọi tên quan hệ; lời kể nằm ở phụ đề và âm thanh. Chuyển động theo nhịp câu đã đo từ từng đoạn đọc.

Kiến trúc và núi Meru là minh họa giản lược để giải thích biểu tượng, không phải bản vẽ khảo cổ hay địa hình. Không gán hào nước một công dụng thực tế chưa được dẫn nguồn.

Giọng thực tế: Hải Đăng, VieNeu-TTS v3 Turbo. Chưa xác minh được preset Nguyễn Việt Cường. Phụ đề có mốc câu đo từ âm thanh, không phải căn đều theo số chữ.
''',encoding='utf-8')
    print(f'PROJECT READY: {len(p["scenes"])} scenes, {sum(len(s["objects"]) for s in p["scenes"])} editable layers, no presenter.',flush=True)
    return saved

def preview(p):
    from PySide6.QtWidgets import QApplication
    from PySide6.QtGui import QImage,QPainter,QColor
    from studio.renderer import Renderer
    app=QApplication.instance() or QApplication([])
    r=Renderer()
    sheet=QImage(1280,1440,QImage.Format.Format_RGB32);sheet.fill(QColor(PAPER));painter=QPainter(sheet)
    for i,s in enumerate(p['scenes']):
        ts=s['start']+s['duration']*.72
        frame=r.frame(p,DEST,ts,1280,720)
        frame.save(str(DEST/'review'/f'scene_{i+1:02}.png'))
        painter.drawImage((i%2)*640,(i//2)*360,frame.scaled(640,360))
    painter.end();sheet.save(str(DEST/'review'/'storyboard.png'))
    # Sample scene transitions and sentence transitions before committing to export.
    for i,s in enumerate(p['scenes']):
        r.frame(p,DEST,s['start']+.04,1280,720).save(str(DEST/'review'/f'opening_{i+1:02}.png'))

if __name__=='__main__':
    preview(build())
