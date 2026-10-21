"""Direct an original full-frame historical cartoon using editable Studio cutout layers."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
DEST=Path(__file__).resolve().parents[1];ART=DEST/'art';ORIGINAL=ROOT/'projects'/'nguoi_viet_co_5phut'
from studio.project import new_project,new_scene,new_object,save
from studio.explainer import image_item,text_item,item
from studio.subtitles import read,write
from studio.directing import preflight
from studio.asset_library import asset
from studio.media import add_waveforms


class Set:
    def __init__(self,scene):self.s=scene;self.L=scene['duration'];self.objects=scene['objects']
    def add(self,o,parent=None,layer=20,start=0,end=None):
        o.update(layer=layer,start=start,end=self.L if end is None else end)
        if parent:o['parent']=parent['id']
        self.objects.append(o);return o
    def group(self,name,x=0,y=0,parent=None,scale=1):
        o=new_object('group',name,x,y);o['scale']=scale;return self.add(o,parent)
    def art(self,name,x,y,w,h,parent=None,layer=20,pivot=None,start=0,end=None,**extra):
        path=ART/(name if '.' in name else name+'.svg')
        if not path.exists():path=Path(asset(name))
        o=image_item(str(path),x,y,w,h);o.update(extra)
        if pivot:o['pivot']=pivot
        return self.add(o,parent,layer,start,end)
    def keys(self,o,key,values):
        o.setdefault('keys',{})[key]=[dict(t=t,v=v,ease='ease_in_out') for t,v in values];return o
    def text(self,value,x,y,w,h,size=30,start=0,end=None,parent=None,**extra):
        data=dict(font='Segoe UI',color='#fff4da',bold=True);data.update(extra)
        return self.add(text_item(value,x,y,w,h,size,**data),parent,80,start,end)
    def shadow(self,x,y,width=190,parent=None):return self.art('shadow',x,y,width,width/8,parent,layer=10)
    def background(self,name):
        return self.art(name,640,360,1370,771,layer=0,fit='cover')
    def puppet(self,name,kind,x,y,scale=1,expression='normal',pose='rest',basket=False,seated=False):
        root=self.group(name,x,y,scale=scale);body_group=self.group(name+' · thân',0,0,root)
        # Slightly oversized circular head, compact torso and cloth silhouette.
        legname='leg_host' if kind=='host' else 'leg_bare'
        if seated:self.art('legs_seated',0,-40,150,83,root,14)
        else:
            for side,sgn in (('L',-1),('R',1)):
                leg=self.group(name+' · chân '+side,sgn*16,-84 if kind=='host' else -74,root)
                self.art(legname,0,0,42,100 if kind=='host' else 88,leg,14,pivot=[-1,-44 if kind=='host' else -39.5])
        left=self.group(name+' · vai trái',-28,-148,body_group)
        right=self.group(name+' · vai phải',28,-148,body_group)
        arms={}
        for side,g in (('L',left),('R',right)):
            self.art('arm',0,0,24,49.2,g,16,pivot=[-1.2,-18.6])
            lower=self.group(name+' · khuỷu '+side,0,35,g)
            self.art('arm',0,0,22,45.1,lower,17,pivot=[-1.1,-17.05])
            hand=self.art('point' if pose=='point' and side=='R' else 'hand',0,37,32 if pose=='point' and side=='R' else 26,24.6,lower,30)
            arms[side]=(g,lower,hand)
        height=106 if kind=='host' else 124
        self.art('body_'+kind,0,-126,88,height,body_group,22)
        head=self.group(name+' · đầu',0,-205,body_group)
        self.art('head_'+kind,0,0,107,113,head,35)
        self.face(head,expression)
        if pose=='rest':angles=(-7,-4,7,4)
        elif pose=='welcome':angles=(34,76,-34,-76)
        elif pose=='point':angles=(-12,-15,-79,-12)
        elif pose=='belly':angles=(-10,-85,10,85)
        elif pose=='carry':angles=(-12,-48,-20,85)
        elif pose=='cook':angles=(15,-55,-45,-28)
        else:angles=(-7,-4,7,4)
        for o,a in zip((arms['L'][0],arms['L'][1],arms['R'][0],arms['R'][1]),angles):o['rotation']=a
        self.shadow(x,y+7,150*scale)
        result=dict(root=root,body=body_group,head=head,arms=arms,kind=kind)
        if basket:self.art('basket',42,-61,73,79,root,40)
        return result
    def face(self,head,expression,start=0,end=None):
        end=self.L if end is None else end
        # Pose replacements are discrete; eyelids close without moving the head.
        spans=[];cursor=start
        for t in (2.4,5.8,9.7,13.3):
            if start+.3<t<end-.2:spans.append((cursor,t,False));spans.append((t,t+.10,True));cursor=t+.10
        spans.append((cursor,end,False))
        for a,b,blink in spans:self.art(('blink_' if blink else 'face_')+expression,0,0,107,113,head,36,start=a,end=b)
    def expression(self,puppet,beats):
        head=puppet['head'];self.objects[:]=[o for o in self.objects if not (o.get('parent')==head['id'] and ('face_' in o.get('file','') or 'blink_' in o.get('file','')))]
        for i,(t,ex) in enumerate(beats):self.face(head,ex,t,beats[i+1][0] if i+1<len(beats) else self.L)
    def pose(self,puppet,beats):
        values={('L',0):[],('L',1):[],('R',0):[],('R',1):[]}
        for t,angles in beats:
            for pair,v in zip(values,angles):values[pair].append((t,v))
        for (side,part),points in values.items():self.keys(puppet['arms'][side][part],'rotation',points)
    def push(self,a=1,b=1.035,x=640,y=360):
        self.s['camera'].update(x=x,y=y,keys={'zoom':[dict(t=0,v=a),dict(t=self.L,v=b,ease='ease_in_out')]})


def scene(index,start,end):
    s=new_scene(('Bến sông buổi sớm','Không điện, không điện thoại','Một cái bụng đói','Người dẫn giữa ngôi làng','Dòng sông nuôi làng','Một bếp lửa bắt đầu ngày mới')[index],end-start)
    s.update(start=start,background='white',layout='custom',style='ink');st=Set(s)
    st.background('kitchen_background.png' if index==5 else 'village_background.png')
    if index==0:
        h=st.puppet('Người dẫn','host',485,647,1.80,'surprised','welcome')
        st.pose(h,[(0,(-6,-4,6,4)),(.4,(-6,-4,6,4)),(1.2,(31,70,-31,-70)),(3.5,(31,70,-31,-70)),(4.2,(-7,-4,-75,-14))])
        st.expression(h,[(0,'surprised'),(1.3,'worried'),(3.6,'happy')]);st.push(1,1.022)
        title=st.text('MỘT NGÀY\nCÙNG NGƯỜI VIỆT CỔ',925,164,580,165,40,end=3.7,color='#fff6db')
        title['enter']='fade';title['enter_duration']=.35
    elif index==1:
        h=st.puppet('Người dẫn','host',495,770,2.65,'annoyed','rest')
        st.expression(h,[(0,'normal'),(.35,'annoyed'),(2.8,'surprised')])
        st.pose(h,[(0,(-7,-4,7,4)),(.5,(25,65,-64,-14)),(2.7,(25,65,-64,-14)),(3.3,(35,85,-35,-85))])
        st.art('bubble',865,277,395,191,start=.20,end=2.95,layer=60)
        st.text('ĐIỆN?\nĐIỆN THOẠI?',862,250,344,120,31,start=.2,end=2.95,color='#392f27')
        line=item('shape','Không có điện thoại',866,293,330,4,shape='line',color='#b34c36',stroke=8,rotation=-12)
        st.add(line,layer=85,start=1.28,end=2.95)
        st.push(1.0,1.018)
    elif index==2:
        h=st.puppet('Người dẫn','host',486,764,2.55,'worried','belly')
        st.pose(h,[(0,(-10,-85,10,85)),(1.1,(-10,-85,10,85)),(1.65,(-8,-90,8,90)),(2.3,(-10,-85,10,85)),(4.3,(31,73,-31,-73))])
        st.expression(h,[(0,'normal'),(.9,'worried'),(3.8,'surprised')])
        st.art('gurgle',486,507,90,65,start=1.0,end=1.32,layer=65)
        st.art('gurgle',486,507,90,65,start=1.52,end=1.84,layer=65)
        st.art('bubble',894,250,400,194,start=2.1,end=st.L,layer=60)
        st.text('ĂN GÌ BÂY GIỜ?',891,221,340,100,29,start=2.1,color='#392f27')
        st.art('bowl',879,465,184,123,start=2.35,layer=45)
        st.push(1,1.015)
    elif index==3:
        h=st.puppet('Người dẫn','host',346,638,1.63,'happy','point')
        man=st.puppet('Người mang giỏ','man',825,575,1.28,'normal','carry',basket=True)
        woman=st.puppet('Người phụ nữ','woman',1070,605,1.43,'normal','welcome')
        child=st.puppet('Em bé','child',961,623,.88,'happy','rest')
        st.keys(man['head'],'rotation',[(0,-3),(1,-3),(2.1,2),(3.0,0)])
        st.pose(h,[(0,(-12,-15,-79,-12)),(4.0,(-12,-15,-79,-12)),(4.8,(32,71,-32,-71)),(st.L,(32,71,-32,-71))])
        st.expression(woman,[(0,'happy'),(3.5,'talk'),(4.2,'happy'),(5.8,'talk'),(6.3,'happy')])
        st.keys(child['head'],'rotation',[(0,0),(2.5,0),(3.1,-9),(4.7,-9),(5.3,0)])
        st.text('CƯ DÂN ĐÔNG SƠN',765,126,640,80,34,start=4.8,color='#fff7dd')
        st.push(1,1.025)
    elif index==4:
        man=st.puppet('Người mang giỏ','man',832,594,1.38,'happy','carry',basket=True)
        child=st.puppet('Em bé','child',1010,620,.95,'normal','point')
        st.expression(child,[(0,'normal'),(1.9,'happy')])
        st.keys(child['head'],'rotation',[(0,-3),(1.3,-3),(2,5),(3.8,5),(4.5,0)])
        st.push(1.035,1.075,x=700,y=365)
    else:
        mother=st.puppet('Người nhóm bếp','woman',580,637,1.57,'normal','cook')
        child=st.puppet('Em bé chờ cơm','child',405,650,1.05,'worried','belly',seated=True)
        st.pose(mother,[(0,(15,-55,-45,-28)),(.8,(15,-55,-48,-32)),(2.3,(15,-55,-45,-28)),(4.7,(15,-55,-48,-32))])
        st.expression(mother,[(0,'normal'),(1.9,'happy')]);st.expression(child,[(0,'worried'),(2.1,'surprised'),(3.3,'happy')])
        st.keys(child['head'],'rotation',[(0,0),(1.3,0),(2,-6),(4.7,-6)])
        st.art('bowl',434,594,108,72,layer=50)
        f=st.art('fire',937,494,88,96,layer=38)
        st.keys(f,'scale',[(0,.88),(.3,1),(.6,.92),(1.0,1.02),(1.4,.94),(1.8,1.01),(2.2,.9),(2.6,1.03),(3,.96),(3.5,1.0),(4,.92),(4.8,1)])
        sm=st.art('steam',914,349,80,140,layer=39,opacity=.7)
        st.keys(sm,'y',[(0,349),(st.L,329)]);st.keys(sm,'opacity',[(0,.25),(1.5,.7),(3,.45),(4.8,.65)])
        st.push(1.0,1.032)
    # No slide headers or frames: the scene and characters share a full environment.
    st.text('Cảnh minh họa',1162,32,200,28,13,color='#fff8e7',bold=False)
    return s


def prepare():
    p=new_project('Một ngày người Việt cổ · Thử phong cách hoạt hình lịch sử',32.364,1920,1080)
    p.update(scenes=[],audio=[],fps=30,audio_rate=48000,audio_channels=2,render_profile='final',duck_music=True)
    times=[0,4.82,8.722,13.542,22.724,27.544,32.364]
    for i,(a,b) in enumerate(zip(times,times[1:])):p['scenes'].append(scene(i,a,b))
    p['audio'].append(dict(id='voice',name='Lời đọc từ kịch bản SRT',file=str(ORIGINAL/'narration.wav'),start=0,trim=0,duration=times[-1],group='voice',volume=1))
    p['audio'].append(dict(id='bed',name='Nền âm nhạc gốc',file=str(ORIGINAL/'sound'/'original_soft_bed.m4a'),start=0,trim=0,duration=times[-1],group='music',volume=.6,fade_in=.8,fade_out=1.1))
    for i in (0,3,4):
        s=p['scenes'][i];p['audio'].append(dict(id=f'river{i}',name='Sông và chim',file=str(ORIGINAL/'sound'/'river_and_birds.m4a'),start=s['start'],duration=min(12,s['duration']),group='sfx',volume=.5,fade_in=.3,fade_out=.5))
    p['audio'].append(dict(id='fire',name='Bếp lửa',file=str(ORIGINAL/'sound'/'quiet_hearth.m4a'),start=27.544,duration=4.82,group='sfx',volume=.7,fade_in=.3,fade_out=.5))
    cues=read(ORIGINAL/'source'/'kich_ban_goc.srt')[:7];p['subtitles']=cues
    p['subtitle_style'].update(enabled=True,font='Segoe UI',size=26,y=.972,color='#ffffff',background=True)
    for cue in cues:
        cue['scene_id']=next(s['id'] for s in p['scenes'] if s['start']<=cue['start']<s['start']+s['duration'])
    add_waveforms(p,DEST)
    assert not preflight(p,DEST),preflight(p,DEST)
    result=save(p,DEST/'project.json',DEST);write(cues,DEST/'phu_de.srt')
    (DEST/'shot_list.json').write_text(json.dumps([dict(name=s['name'],start=s['start'],duration=s['duration'],layers=len(s['objects'])) for s in p['scenes']],ensure_ascii=False,indent=2),encoding='utf-8')
    print('Sample ready:',times[-1],'seconds;',len(p['scenes']),'shots;',sum(len(s['objects']) for s in p['scenes']),'editable layers')
    return result


if __name__=='__main__':prepare()
