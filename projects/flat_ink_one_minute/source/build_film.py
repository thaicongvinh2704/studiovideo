"""One-minute art-direction film: fixed source presenter and matching ink illustrations."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
DEST=Path(__file__).resolve().parents[1];ART=DEST/'art';OLD=ROOT/'projects'/'nguoi_viet_co_5phut'
from studio.project import new_project,new_scene,save,new_object
from studio.explainer import image_item,text_item,item
from studio.subtitles import read
from studio.directing import preflight
from studio.media import add_waveforms


def effects_art():
    prefix='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 140"><g stroke="#242421" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">'
    (ART/'fire.svg').write_text(prefix+'<path d="M22 105Q2 84 27 59Q31 77 41 66Q55 39 48 16Q88 50 83 79Q99 71 93 55Q121 100 86 118Q48 139 22 105Z" fill="#e69c55"/><path d="M45 110Q27 93 48 77Q55 93 62 83Q75 65 70 53Q100 98 76 113Q60 127 45 110Z" fill="#f0c779"/></g></svg>',encoding='utf-8')
    (ART/'steam.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 130 200"><g fill="none" stroke="#b9b7ad" stroke-width="4.5" stroke-linecap="round"><path d="M34 181Q6 155 35 127Q59 101 31 77Q14 54 36 30"/><path d="M82 171Q111 147 84 117Q63 91 91 64"/></g></svg>',encoding='utf-8')


class Stage:
    def __init__(self,s):self.s=s;self.L=s['duration'];self.o=s['objects']
    def add(self,o,layer=10,start=0,end=None):o.update(layer=layer,start=start,end=self.L if end is None else end);self.o.append(o);return o
    def art(self,name,x=640,y=360,w=1280,h=720,layer=10,start=0,**extra):
        o=image_item(str(ART/name),x,y,w,h);o.update(extra)
        if start:o.update(enter='fade',enter_duration=.4)
        return self.add(o,layer,start)
    def bg(self,name):return self.art(name,w=1330,h=748,layer=0)
    def text(self,value,x,y,w=800,h=80,size=30,start=0,end=None,**extra):
        data=dict(font='Segoe Print',color='#252525');data.update(extra);o=text_item(value,x,y,w,h,size,**data)
        if start:o.update(enter='fade',enter_duration=.4)
        return self.add(o,60,start,end)
    def key(self,o,name,values):
        o.setdefault('keys',{})[name]=[dict(t=t,v=v,ease='ease_in_out') for t,v in values];return o
    def presenter(self,x=230,y=430,height=445):
        # The character is the original image, not a newly generated or remixed rig.
        return self.art('presenter_master.png',x,y,height*(392*.98)/(422*.99),height,30,crop=[0,0,.98,.99])
    def push(self,a=1,b=1.025):
        self.s['camera']['keys']={'zoom':[dict(t=0,v=a),dict(t=self.L,v=b,ease='ease_in_out')]}
    def smoke(self,x,y,w=58,h=105):
        for i in range(2):
            o=self.art('steam.svg',x+i*8,y,w,h,25,opacity=.3)
            points=[];alpha=[]
            for j in range(5):
                t=self.L*j/4;points.append((t,y-9*j));alpha.append((t,.2 if (j+i)%2 else .48))
            self.key(o,'y',points);self.key(o,'opacity',alpha)


def prepare():
    effects_art();cues=read(DEST/'phu_de.srt');factor=60/61.285
    boundaries=[x*factor for x in (0,8.722,18.133,27.544,36.955,46.366,56.695,61.285)];boundaries[-1]=60
    names=['Tỉnh dậy bên dòng sông','Một bữa ăn cho ngày mới','Cư dân Đông Sơn','Bên bếp lửa','Dấu vết của đời sống','Ngôi nhà sàn','Quá khứ rộng hơn điều ta biết']
    p=new_project('Một ngày người Việt cổ · Mẫu nét mực đồng bộ · 1 phút',60,1920,1080)
    p.update(scenes=[],fps=30,audio_rate=48000,audio_channels=2,render_profile='final',audio=[],subtitles=cues,duck_music=True)
    p['subtitle_style'].update(enabled=True,size=27,font='Segoe UI',color='#ffffff',background=True,y=.975)
    for i,(a,b) in enumerate(zip(boundaries,boundaries[1:])):
        s=new_scene(names[i],b-a);s.update(start=a,objects=[],background='white',style='ink',layout='custom');st=Stage(s);L=st.L
        if i==0:
            st.bg('village_flat_ink.png');st.presenter()
            st.text('MỘT NGÀY CÙNG\nNGƯỜI VIỆT CỔ',338,113,590,140,34,end=4.5*factor,bold=True)
            st.text('Hơn hai nghìn\nnăm trước',270,118,460,100,28,start=4.82*factor)
            st.push(1,1.018)
        elif i==1:
            st.bg('kitchen_flat_ink.png')
            st.text('Hôm nay, mình sẽ ăn gì?',340,155,570,100,33,end=(13.542-8.722)*factor)
            st.text('Một ngày được hình dung\ntừ những dấu tích',310,187,540,150,30,start=(13.542-8.722)*factor)
            st.push(1,1.02)
        elif i==2:
            st.bg('village_flat_ink.png');st.presenter(210,452,402)
            st.text('Cư dân Đông Sơn',245,100,455,85,32)
            st.text('Miền Bắc Việt Nam\nngày nay',245,184,455,80,25,start=(22.724-18.133)*factor)
            st.push(1.02,1)
        elif i==3:
            st.bg('kitchen_flat_ink.png');st.presenter(191,459,375)
            st.text('Bắt đầu từ một bếp lửa',360,122,650,90,31)
            # Fire and steam positions are authored against the finished background.
            fire=st.art('fire.svg',1103,611,43,50,26)
            st.key(fire,'scale',[(0,.94),(L*.15,1.04),(L*.3,.96),(L*.45,1.02),(L*.6,.94),(L*.75,1.04),(L*.9,.98),(L,1)])
            st.smoke(1104,468,w=48,h=85)
            st.push(1.015,1.035)
        elif i==4:
            st.bg('traces_flat_ink.png');st.presenter(220,443,420)
            st.text('Dấu vết của những\ncon người\nkhông còn tên',235,132,430,180,29)
            st.push(1,1.02)
        elif i==5:
            st.bg('house_flat_ink.png');st.presenter(220,448,410)
            st.text('Một căn\nnhà sàn',235,132,425,130,34)
            st.text('Một phần bức tranh\nvẫn còn bỏ ngỏ',235,237,425,85,23,start=(51.186-46.366)*factor)
            st.push(1.02,1)
        else:
            st.bg('village_flat_ink.png');st.presenter(220,455,405)
            st.text('Quá khứ luôn rộng hơn\nđiều mình đã biết.',298,126,565,160,30,bold=True)
            st.push(1.015,1.0)
        st.text('Cảnh minh họa',105,30,190,30,13,font='Segoe UI',color='#77746d')
        p['scenes'].append(s)
    for cue in cues:cue['scene_id']=next(s['id'] for s in p['scenes'] if s['start']-1e-6<=cue['start']<s['start']+s['duration']-1e-6)
    p['audio'].append(dict(id='narration',name='Lời kịch bản · 60 giây',file=str(DEST/'narration.wav'),start=0,duration=60,group='voice',volume=1))
    p['audio'].append(dict(id='original_bed',name='Nhạc nền tự tạo',file=str(OLD/'sound'/'original_soft_bed.m4a'),start=0,duration=60,group='music',volume=.6,fade_in=1.0,fade_out=1.8))
    for i in (0,2,6):
        s=p['scenes'][i];p['audio'].append(dict(id=f'river_{i}',name='Sông và chim · tự tạo',file=str(OLD/'sound'/'river_and_birds.m4a'),start=s['start'],duration=s['duration'],group='sfx',volume=.4,fade_in=.3,fade_out=.4))
    s=p['scenes'][3];p['audio'].append(dict(id='fire',name='Bếp lửa · tự tạo',file=str(OLD/'sound'/'quiet_hearth.m4a'),start=s['start'],duration=s['duration'],group='sfx',volume=.6,fade_in=.4,fade_out=.5))
    add_waveforms(p,DEST);assert not preflight(p,DEST),preflight(p,DEST)
    original=ART/'presenter_master.png';assert hashlib.sha256(original.read_bytes()).hexdigest()=='85b814d6ad7e6d6e3076b80cf136469b98a2733ab02ef1c00964188b86217c15'
    saved=save(p,DEST/'project.json',DEST)
    (DEST/'shot_list.json').write_text(json.dumps([dict(name=s['name'],start=s['start'],duration=s['duration']) for s in p['scenes']],ensure_ascii=False,indent=2),encoding='utf-8')
    print('PROJECT READY:',len(p['scenes']),'scenes, 60 seconds, original presenter preserved')
    return saved


if __name__=='__main__':prepare()
