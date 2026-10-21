"""Offline editorial scene construction; all generated layers remain editable."""
import copy
import math
from pathlib import Path
from .project import new_scene, new_object, uid


def gesture_sequence(obj, sequence):
    """Authored pose beats with anticipation, settle and a readable held pose."""
    from .explainer import apply_pose
    for beat in sequence:
        t=float(beat.get('t',0));blend=float(beat.get('blend',.65))
        apply_pose(obj,beat['pose'],t,blend)
        if t>0 and blend>.15:
            for name,frames in obj.get('keys',{}).items():
                if not name.startswith('bone_') or len(frames)<2 or abs(frames[-1]['t']-(t+blend))>.001:continue
                # Mild anticipation and settle in a continuous timing curve. Forearms
                # trail the shoulder slightly; avoid all channels moving as one hinge.
                frames[-1].update(ease='bezier',bezier=[.33,-.06,.48,1.04])
                if 'fore_' in name:
                    frames.insert(len(frames)-1,dict(t=t+min(.07,blend*.12),v=frames[-2]['v']))
    return obj


def build_ink_scene(row,index=0):
    from .explainer import presenter, text_item, item, image_item
    from .asset_library import asset
    length=float(row['end'])-float(row['start'])
    scene=new_scene(row.get('title') or f'Cảnh {index+1}',length)
    layout=row.get('layout','presenter')
    scene.update(background='white',layout=layout,narration=row.get('text',''),style='ink')
    objects=[];labels=row.get('labels',[]);images=list(row.get('assets',[]))
    reveal_times=row.get('reveal_times',[])
    def reveal(i,default=0):return float(reveal_times[i]) if i<len(reveal_times) else default
    images.extend(asset(name) for name in row.get('asset_ids',[]))
    font=row.get('font','Segoe Print')
    def text(value,x,y,w=500,h=85,size=32,**extra):
        obj=text_item(value,x,y,w,h,size,font=font,color='#191d20',**extra);objects.append(obj);return obj
    def art(i,x,y,w,h,start=0):
        if i>=len(images):
            # Draft gaps are explicit and collected by preflight. Never disguise them as art.
            o=item('shape','Thiếu hình',x,y,w,h,shape='callout',fill='#fff1cd',text='Cần hình minh họa',font_size=24)
            o['placeholder']=True
        else:o=image_item(images[i],x,y,w,h)
        o['start']=start;objects.append(o);return o
    def host(x=235,y=640,scale=2.45,pose=None):
        o=presenter(x,y,scale,pose or row.get('pose','explain'))
        count=sum(1 for obj in objects if obj['kind']=='character')
        o['id']=row.get('presenter_id','presenter')+('' if count==0 else '_'+str(count+1))
        if row.get('shirt'):o['shirt']=row['shirt']
        if row.get('expressions'):o['expressions']=copy.deepcopy(row['expressions'])
        if row.get('gestures'):gesture_sequence(o,row['gestures'])
        objects.append(o);return o
    def shape(name,x,y,w,h,**extra):
        o=item('shape',name,x,y,w,h,shape=name,color='#191d20',fill='#ffffff',stroke=3,**extra);objects.append(o);return o
    if row.get('show_title'):
        text(row.get('title',''),640,65,1140,85,34)
    if layout=='focus':
        host(710,915,4.0,row.get('pose','idea'))
        if images:art(0,1040,180,190,190,reveal(0,min(.7,length*.1)))
        if labels:
            shape('callout',260,225,350,210)
            text(labels[0],260,215,300,160,36)
    elif layout=='presenter':
        host()
        art(0,865,340,650,435,reveal(0))
        if labels:text(labels[0],865,590,650,95,30)
    elif layout=='quote':
        host(270,680,2.9)
        if images:art(0,925,190,180,170,reveal(0))
        shape('callout',850,405,620,285)
        text('\n'.join(labels) or row.get('title',''),850,395,560,225,34)
    elif layout=='compare':
        for i,x in enumerate((340,940)):
            art(i,x,320,510,405,start=reveal(i,min(i*.7,length*.15)))
            if i<len(labels):text(labels[i],x,590,510,95,32,start=reveal(i,min(i*.7,length*.15)))
        if row.get('relation',True):shape('arrow',640,335,65,20)
    elif layout in ('timeline','process'):
        n=max(1,min(4,max(len(labels),len(images))))
        shape('arrow',700,455,990,16)
        host(70,690,1.05,'point')
        for i in range(n):
            x=260+i*(850/max(1,n-1));on=reveal(i,min(row.get('reveal_step',1.1)*i,length*.45))
            art(i,x,300,230,245,on)
            o=shape('ellipse',x,455,19,19);o['fill']='#f6ca45';o['start']=on
            if i<len(labels):text(labels[i],x,535,245,105,27,start=on)
    elif layout=='map':
        art(0,820,355,810,570)
        host(190,650,2.15,'point')
        # Route is editable, and can be revealed at the narration cue.
        if row.get('route'):
            o=shape('path',820,355,650,400);o.update(points=row['route'],color='#dd5146',stroke=4,reveal=True,start=row.get('route_start',1.2),enter_duration=1.5)
        if labels:text(labels[0],835,660,740,75,29)
    elif layout=='gallery':
        for i in range(min(4,max(1,len(images)))):
            x=335+(i%2)*610;y=220+(i//2)*300
            art(i,x,y,510,270,reveal(i,min(i*.8,length*.3)))
            if i<len(labels):text(labels[i],x,y+137,500,50,23,start=reveal(i,min(i*.8,length*.3)))
    elif layout=='pan':
        o=art(0,640,365,1160,640)
        o['keys']['scale']=[dict(t=0,v=1),dict(t=length,v=1.12,ease='ease_in_out')]
        if labels:text(labels[0],640,665,1000,65,28)
    elif layout=='crowd':
        # A wide staged scene; each person and prop remains a distinct layer.
        art(0,775,315,700,440)
        for i,(x,y,sc) in enumerate(((180,650,1.95),(515,655,1.2),(740,655,1.1),(1010,655,1.05))):
            o=host(x,y,sc,'point' if i==0 else 'hold')
            o['shirt']='#252525' if i==0 or i%2 else '#ffffff'
            if i>0:o['shirt_mark']='none'
        if labels:text(labels[0],800,80,780,85,34)
    elif layout=='custom':
        if row.get('title'):text(row['title'],640,76,1120,100,34)
    explicit_ends={}
    for data in row.get('objects',[]):
        o=new_object(data.get('kind','shape'),data.get('preset','custom'));o.update(copy.deepcopy(data));o.setdefault('width',300);o.setdefault('height',180)
        objects.append(o)
        if 'end' in data:explicit_ends[o['id']]=data['end']
    for o in objects:
        o.setdefault('enter','none')
        o['end']=explicit_ends.get(o['id'],length)
    # Imported object IDs are local authoring IDs; preserve references while uniquifying.
    ids={o['id']:uid() for o in objects}
    for o in objects:
        old=o['id'];o['id']=ids[old]
        if o.get('parent') in ids:o['parent']=ids[o['parent']]
        for binding in o.get('attachment',[]):
            if binding.get('character') in ids:binding['character']=ids[binding['character']]
        for contact in o.get('contacts',[]):
            if contact.get('target') in ids:contact['target']=ids[contact['target']]
    scene['objects']=objects
    if row.get('camera'):
        scene['camera'].update(copy.deepcopy(row['camera']))
        scene['camera']['follow']=ids.get(scene['camera'].get('follow'),scene['camera'].get('follow',''))
    return scene


def editorial_suggestions(cues,assets):
    """Transparent rules, not a claim of semantic AI or factual asset recognition."""
    from .explainer import normalized
    from .asset_library import CATALOG,asset
    paths=[Path(a) for a in assets];rows=[]
    for i,cue in enumerate(cues):
        value=normalized(cue['text']);tokens=set(value.split())
        scores=[]
        for name,(title,tags) in CATALOG.items():
            terms=set(tags.split());overlap=tokens & terms
            # Multiword title match is more meaningful than a lone generic token.
            phrase=normalized(title)
            score=(6 if phrase in value else 0)+len(overlap)
            if score>=3:scores.append((score,name))
        scores.sort(reverse=True)
        matches=sorted(paths,key=lambda p:len(tokens & set(normalized(p.stem.replace('_',' ')).split())),reverse=True)
        chosen=[str(p.resolve()) for p in matches[:3] if len(tokens & set(normalized(p.stem.replace('_',' ')).split()))>=2]
        builtin=[name for _,name in scores[:3]] if not chosen else []
        if any(word in value for word in ('truoc tien','tiep theo','cuoi cung','giai doan')):layout='timeline'
        elif any(word in value for word in ('ban do','tuyen duong','di cu')):layout='map'
        elif any(word in value for word in ('so sanh','hai nguon','trong khi')) and len(chosen or builtin)>=2:layout='compare'
        elif '?' in cue['text'] and not chosen and not builtin:layout='focus';builtin=['question']
        elif len(chosen or builtin)>=3:layout='gallery'
        else:layout='presenter'
        title=' '.join(cue['text'].split()[:8]).rstrip(',.?!')
        row=dict(start=cue['start'],end=cue['end'],cue_start=cue['start'],cue_end=cue['end'],text=cue['text'],title=title,
                 style='ink',layout=layout,pose='question' if '?' in cue['text'] else 'explain',assets=chosen+[asset(n) for n in builtin],
                 labels=[],show_title=False,gestures=[dict(t=0,pose='rest'),dict(t=.5,pose='question' if '?' in cue['text'] else 'explain',blend=.8)],
                 editorial_note='Gợi ý bằng từ khóa; kiểm tra hình và mốc theo lời đọc.')
        if not row['assets']:row['missing_visual']='Cần chọn hoặc chuẩn bị minh họa đúng nội dung: '+title
        rows.append(row)
    return rows


def preflight(project,root):
    from .project import missing
    problems=[dict(level='error',message='Thiếu file: '+name) for name in missing(project,root)]
    for scene in project['scenes']:
        for o in scene['objects']:
            if o.get('placeholder'):problems.append(dict(level='error',scene=scene['name'],message='Cảnh còn thiếu hình minh họa.'))
    from .character_qc import project_issues
    problems.extend(project_issues(project,root))
    return problems
