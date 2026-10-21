"""Editable, offline storyboard compiler. No remote generation or hidden assets."""
import copy
import json
import math
import re
import subprocess
import unicodedata
from pathlib import Path
from .project import new_project, new_scene, new_object, uid, resequence
from .subtitles import parse

LAYOUTS = {'presenter':'Người dẫn + bảng', 'compare':'So sánh hai hình',
           'timeline':'Dòng thời gian', 'process':'Các bước / nguyên nhân',
           'gallery':'Bộ sưu tập hình', 'quote':'Câu hỏi / kết luận', 'pan':'Ảnh toàn cảnh', 'custom':'Các lớp tự bố trí',
           'focus':'Người dẫn cận cảnh','map':'Bản đồ và tuyến','crowd':'Nhóm người / bối cảnh'}
POSES = {'welcome':'Giới thiệu', 'point':'Chỉ bên phải', 'point_left':'Chỉ bên trái',
         'explain':'Giải thích', 'think':'Suy nghĩ', 'question':'Thắc mắc',
         'surprised':'Ngạc nhiên', 'hold':'Cầm vật', 'celebrate':'Vui mừng',
         'rest':'Đứng nghỉ', 'sit':'Ngồi', 'walk':'Đi bộ'}
POSE_ANGLES = {
    'welcome':(-.9,-1.8,.9,1.8), 'point':(-.18,.5,1.15,1.65),
    'point_left':(-1.15,-1.65,.18,-.5), 'explain':(-.2,.1,.7,2.0),
    'think':(-.3,-1.35,.65,-2.7), 'question':(-.8,-2.0,.8,2.0),
    'surprised':(-.65,-2.5,.65,2.5), 'hold':(-.5,-1.5,.5,1.5),
    'celebrate':(-2.0,-2.6,2.0,2.6), 'rest':(-.15,-.1,.15,.1),
    'sit':(-.3,-.4,.3,.4),
}

POSES.update(idea='Nảy ra ý tưởng',disagree='Phản biện',listen='Lắng nghe',
             read='Đọc tài liệu',receive='Nhận vật',give='Đưa vật',
             bow='Cúi chào',confident='Tự tin')
POSE_ANGLES.update(idea=(-.45,-.8,1.0,2.95),disagree=(-.2,-.25,.9,2.5),
                   listen=(-.1,-.05,.12,.05),read=(-.55,-1.8,.55,1.8),
                   receive=(-.3,-.8,.85,1.15),give=(-.2,-.15,1.1,1.35),
                   bow=(-.1,-.1,.1,.1),confident=(-.85,1.1,.9,-1.1))

def probe_media(path):
    from .exporter import binary, FLAGS
    r=subprocess.run([binary('ffprobe'),'-v','error','-show_format','-show_streams','-of','json',str(path)],
                     capture_output=True,check=True,creationflags=FLAGS)
    data=json.loads(r.stdout);length=float(data['format']['duration'])
    if not any(s.get('codec_type')=='audio' for s in data.get('streams',[])):raise ValueError('File voice cần có luồng âm thanh.')
    if not math.isfinite(length) or length<=0:raise ValueError('File không có thời lượng hợp lệ.')
    return length,data

def normalized(text):
    return ''.join(c for c in unicodedata.normalize('NFD',text.lower().replace('đ','d')) if unicodedata.category(c)!='Mn')

def script_cues(text, length):
    if '-->' in text:return parse(text),'srt'
    blocks=[s.strip() for s in re.split(r'\n\s*\n|(?<=[.!?])\s+(?=[A-ZÀ-ỸĐ])',text.strip()) if s.strip()]
    if not blocks:raise ValueError('Hãy nhập kịch bản hoặc SRT.')
    weights=[max(1,len(b.split())) for b in blocks];total=sum(weights);cursor=0;cues=[]
    for b,w in zip(blocks,weights):
        end=cursor+length*w/total
        cues.append(dict(id=uid(),start=cursor,end=end,text=b,role='Narrator'));cursor=end
    return cues,'estimated'

def suggest_board(text, voice, assets=(),pause_assist=False):
    length,_=probe_media(voice)
    cues,mode=script_cues(text,length)
    if mode=='estimated' and pause_assist:
        from .media import align_estimated_cues
        cues=align_estimated_cues(cues,voice,length);mode='pause-assisted'
    if not cues:raise ValueError('Kịch bản chưa có nội dung.')
    if cues[-1]['end']>length+.2:raise ValueError('SRT dài hơn voice. Chỉnh timestamp hoặc chọn đúng file voice.')
    rows=[]
    for i,c in enumerate(cues):
        # Scene coverage remains continuous even when SRT has silence between cues.
        start=0 if i==0 else c['start'];end=cues[i+1]['start'] if i+1<len(cues) else length
        if end<=start:raise ValueError('Các cue phải có thời điểm bắt đầu tăng dần.')
        tokens=set(normalized(c['text']).split())
        scored=sorted(assets,key=lambda a:len(tokens & set(normalized(Path(a).stem.replace('_',' ')).split())),reverse=True)
        chosen=[str(a) for a in scored[:2] if tokens & set(normalized(Path(a).stem.replace('_',' ')).split())]
        title=' '.join(c['text'].split()[:10]).rstrip(',.')
        rows.append(dict(start=start,end=end,text=c['text'],title=title,layout='presenter',
                         assets=chosen,labels=[],pose='explain' if i%2 else 'point',
                         cue_start=c['start'],cue_end=c['end']))
    from .directing import editorial_suggestions
    directed=editorial_suggestions(cues,assets)
    for original,row in zip(rows,directed):
        row.update(start=original['start'],end=original['end'])
    return dict(version=1,name='Video minh họa',voice=str(Path(voice).resolve()),timing=mode,rows=directed)

def item(kind,name,x,y,w=300,h=180,**extra):
    o=new_object(kind,name,x,y);o.update(width=w,height=h,layer=20);o.update(extra);return o

def text_item(text,x,y,w=500,h=100,size=32,**extra):
    data=dict(text=text,font_size=size,color='#18252b');data.update(extra)
    return item('text',text[:35],x,y,w,h,**data)

def apply_pose(obj, name, t=0, blend=.35):
    if name=='walk':obj['action']='walk';obj['pose']='walk';obj['keys']={k:v for k,v in obj.get('keys',{}).items() if not k.startswith('bone_')};return
    from .animation import motion_pose, sample
    before=motion_pose(obj,t)
    angles=POSE_ANGLES.get(name,POSE_ANGLES['rest'])
    if obj.get('skin')=='ink' and obj.get('character_design')=='reference_black':
        angles={'point':(-.75,.6,1.77,1.93),'point_left':(-1.77,-1.93,.75,-.6),
                'rest':(-.1,-.05,.1,.05),'confident':(-.75,.6,.75,-.6)}.get(name,angles)
    targets=dict(zip(('arm_l','fore_l','arm_r','fore_r'),angles))
    targets.update(torso=0,head=0,lift=-40 if name=='sit' else 0)
    if obj.get('skin')=='ink':
        targets.update(torso={'think':-.045,'question':-.025,'explain':.04,'point':.035,'bow':.3}.get(name,0),
                       head={'think':-.12,'question':-.08,'listen':.06,'idea':.08}.get(name,0))
    if name=='sit':
        targets.update(thigh_l=-1.15,shin_l=0,thigh_r=1.15,shin_r=0)
        if obj.get('skin')=='ink':
            from .animation import dimensions,ik
            _,_,_,thigh,shin,_=dimensions(obj,t);targets['lift']=-34
            hip=(0,-(thigh+shin)*(.94 if obj.get('character_design')=='reference_black' else .99)-targets['lift'])
            for side,sign in (('l',-1),('r',1)):
                knee,foot=ik(hip,(sign*27,0),thigh,shin,-sign)
                targets['thigh_'+side]=math.atan2(knee[0]-hip[0],knee[1]-hip[1])
                targets['shin_'+side]=math.atan2(foot[0]-knee[0],foot[1]-knee[1])
    elif any('bone_thigh_'+s in obj.get('keys',{}) for s in ('l','r')):
        targets.update(thigh_l=-.12,shin_l=0,thigh_r=.12,shin_r=0)
    keys=obj.setdefault('keys',{})
    for k,v in targets.items():
        prop='bone_'+k;old=sample(keys.get(prop,[]),t,before.get(k,0))
        if t>0 and k!='lift':v=old+(v-old+math.pi)%math.tau-math.pi
        frames=[f for f in keys.get(prop,[]) if f['t']<t]
        if t>0 and blend>0:frames.append(dict(t=t,v=old));frames.append(dict(t=t+blend,v=v,ease='ease_in_out'))
        else:frames.append(dict(t=t,v=v))
        keys[prop]=frames
    obj['pose']=name;obj['action']='sit' if name=='sit' else 'idle'
    poses=[f for f in obj.get('poses',[]) if f['t']<t];poses.append(dict(t=t,v=name));obj['poses']=poses
    expression='surprised' if name=='surprised' else 'worried' if name in ('think','question','disagree') else 'normal' if name in ('listen','read','rest') else 'happy'
    if t>0:
        frames=[f for f in obj.get('expressions',[]) if f['t']<t]
        if not frames:frames.append(dict(t=0,v=obj.get('expression','happy')))
        frames.append(dict(t=t,v=expression));obj['expressions']=frames
    else:obj['expression']=expression;obj['expressions']=[dict(t=0,v=expression)]

def presenter(x=230,y=590,scale=1.65,pose='explain'):
    o=new_object('character','presenter',x,y)
    o.update(name='Người dẫn · Áo đen',speech_role='narrator',skin='ink',character_design='reference_black',scale=scale,color='#191919',shirt='#252525',shirt_mark='plus',
             pants='#719aca',skin_color='#fbe5bd',shoes='#faf9f4',breath=0,stance=18,rig={'torso':51,'upper_arm':28,'forearm':30,'thigh':32,'shin':31,'shoulder':21},layer=30)
    apply_pose(o,pose);return o

def image_item(path,x,y,w,h):
    return item('image',Path(path).stem,x,y,w,h,file=str(path),fit='contain',image_width=w)

def build_scene(row,index=0):
    if row.get('style')=='ink' or row.get('layout') in ('focus','map','crowd'):
        from .directing import build_ink_scene
        return build_ink_scene(row,index)
    length=float(row['end'])-float(row['start'])
    s=new_scene(row.get('title') or f'Cảnh {index+1}',length);s.update(background='white',narration=row.get('text',''))
    layout=row.get('layout','presenter');assets=row.get('assets',[]);labels=row.get('labels',[])
    title=row.get('title','');s['layout']=layout
    objects=[text_item(title,640,76,1120,100,38,bold=True,align='left')]
    def card(i,x,y,w,h):
        if i<len(assets):return image_item(assets[i],x,y,w,h)
        label=labels[i] if i<len(labels) else 'Ý chính '+str(i+1)
        return item('shape','Thẻ thông tin',x,y,w,h,shape='card',text=label,font_size=30,fill='#f1f5f4',color='#27373d',stroke=3)
    if layout=='presenter':
        objects.append(presenter(pose=row.get('pose','explain')))
        objects.append(card(0,820,350,660,350))
        if labels:objects.append(text_item(' • '.join(labels[:3]),820,590,660,100,26))
    elif layout=='compare':
        for i,x in enumerate((335,945)):
            objects.append(card(i,x,345,520,330))
            objects.append(text_item(labels[i] if i<len(labels) else f'Hình {i+1}',x,568,520,70,30,bold=True))
        objects.append(item('shape','So sánh',640,340,64,64,shape='arrow',color='#d45d47'))
    elif layout in ('timeline','process'):
        entries=labels or ['Bắt đầu','Thay đổi','Kết quả']
        n=min(5,len(entries));spacing=1040/max(1,n-1)
        objects.append(item('shape','Đường nối',640,352,1070,20,shape='arrow',color='#263840',stroke=5))
        for i,label in enumerate(entries[:n]):
            x=120+i*spacing if n>1 else 640
            o=card(i,x,265,min(230,980/n),150);o['start']=min(i*.45,length*.5);objects.append(o)
            objects.append(item('shape','Mốc',x,352,24,24,shape='ellipse',fill='#e7b441',color='#263840'))
            objects.append(text_item(label,x,440,min(240,1000/n),120,26,bold=True,start=o['start']))
        objects.append(presenter(1120,655,.65,'point_left'))
    elif layout=='gallery':
        for i in range(max(1,min(4,max(len(assets),len(labels),3)))):
            x=340+(i%2)*600;y=265+(i//2)*235
            o=card(i,x,y,510,200);o['start']=min(i*.5,length*.5);objects.append(o)
    elif layout=='pan':
        if assets:
            o=image_item(assets[0],640,380,1150,490);objects.append(o)
            o['keys']['scale']=[dict(t=0,v=1),dict(t=length,v=1.08,ease='ease_in_out')]
        else:objects.append(card(0,640,370,1100,420))
    elif layout=='quote':
        objects.append(presenter(240,610,1.7,row.get('pose','question')))
        objects.append(item('shape','Bong bóng',820,365,650,350,shape='callout',text='\n'.join(labels) if labels else row.get('text',''),font_size=32,fill='#fff5d8',color='#27373d',stroke=3))
    explicit_ends={}
    for data in row.get('objects',[]):
        o=new_object(data.get('kind','shape'),data.get('preset','custom'))
        o.update(copy.deepcopy(data));o['id']=uid();o.setdefault('width',300);o.setdefault('height',180)
        if 'end' in data:explicit_ends[o['id']]=data['end']
        objects.append(o)
    for o in objects:
        o['end']=explicit_ends.get(o['id'],length)
        o.setdefault('enter','fade');o.setdefault('enter_duration',.28)
    if row.get('camera'):s['camera'].update(copy.deepcopy(row['camera']))
    s['objects']=objects;return s

def compile_board(board):
    rows=board.get('rows',[])
    if not rows:raise ValueError('Storyboard chưa có cảnh.')
    p=new_project(board.get('name','Video minh họa'),1,1920,1080)
    p.update(fps=30,audio_rate=48000,audio_channels=2,render_profile='final',storyboard=copy.deepcopy(board))
    p['scenes']=[];p['subtitles']=[]
    expected=0
    for i,row in enumerate(rows):
        start=float(row['start']);end=float(row['end'])
        if not all(map(math.isfinite,(start,end))) or abs(start-expected)>.0011 or end<=start:
            raise ValueError(f'Cảnh {i+1}: thời gian phải liên tục, kết thúc lớn hơn bắt đầu (mốc cần: {expected:.3f}s).')
        if row.get('layout','presenter') not in LAYOUTS:raise ValueError('Bố cục không hợp lệ.')
        for path in row.get('assets',[]):
            if not Path(path).is_file():raise FileNotFoundError(path)
        for data in row.get('objects',[]):
            if data.get('file') and not Path(data['file']).is_file():raise FileNotFoundError(data['file'])
        s=build_scene(row,i);s['start']=start;p['scenes'].append(s)
        a=max(start,float(row.get('cue_start',start)));b=min(end,float(row.get('cue_end',end)))
        if row.get('text') and b>a:p['subtitles'].append(dict(id=uid(),start=a,end=b,text=row['text'],role='Narrator',scene_id=s['id']))
        expected=end
    voice=board.get('voice')
    if voice:
        length,_=probe_media(voice)
        if expected>length+.25:raise ValueError('Storyboard dài hơn voice; hãy kiểm tra điểm kết thúc.')
        # Each scene owns a trimmed piece, allowing reorder without detaching narration.
        for s in p['scenes']:
            p['audio'].append(dict(id=uid(),name='Lời · '+s['name'],file=str(voice),start=s['start'],
                trim=s['start'],duration=s['duration'],group='voice',volume=1,scene_id=s['id']))
    p['subtitle_style'].update(enabled=False,size=26,y=.96)
    if voice:
        from .media import add_waveforms
        add_waveforms(p,Path(voice).parent)
    return p

def load_board(path):
    path=Path(path);data=json.loads(path.read_text(encoding='utf-8-sig'))
    if data.get('version')!=1:raise ValueError('Storyboard cần version: 1.')
    def absolute(p):return str((path.parent/p).resolve()) if not Path(p).is_absolute() else p
    if data.get('voice'):data['voice']=absolute(data['voice'])
    for row in data.get('rows',[]):
        row['assets']=[absolute(p) for p in row.get('assets',[])]
        for obj in row.get('objects',[]):
            if obj.get('file'):obj['file']=absolute(obj['file'])
    return data
