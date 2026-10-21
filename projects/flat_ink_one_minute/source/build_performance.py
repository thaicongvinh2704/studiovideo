"""Repair the rejected static cutout with authored character acting in Studio."""
import copy,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
SOURCE=Path(__file__).resolve().parents[1];DEST=ROOT/'projects'/'nguoi_viet_co_performance';DEST.mkdir(exist_ok=True)
(DEST/'review').mkdir(exist_ok=True)
from studio.project import load,save,media_entries,resolve
from studio.explainer import presenter,apply_pose
from studio.media import add_waveforms
from studio.directing import preflight
from studio.animation import sample

def key(o,name,points):
    o.setdefault('keys',{})[name]=[dict(t=t,v=v,ease='ease_in_out') for t,v in points]

def build():
    p=load(SOURCE/'project.json');p['name']='Một phút người Việt cổ · Diễn xuất nhân vật'
    for owner,field in media_entries(p):owner[field]=str(resolve(SOURCE,owner[field]))
    actors=[]
    beats=[
        [(0,'rest'),(.35,'question'),(1.8,'think'),(2.9,'surprised'),(4.3,'disagree'),(5.5,'look'),(6.5,'point'),(7.8,'explain')],
        [(0,'think'),(.8,'question'),(2.2,'curious'),(3.2,'think'),(4.8,'question'),(6.2,'explain'),(7.5,'point')],
        [(0,'rest'),(1.7,'point'),(4.5,'confident'),(6.1,'explain'),(8,'point')],
        [(0,'disagree'),(2.5,'listen'),(3.6,'point'),(5.5,'listen'),(6.3,'explain'),(8,'point')],
        [(0,'rest'),(.6,'think'),(3,'listen'),(4.9,'point'),(7,'explain')],
        [(0,'rest'),(1.6,'point'),(4.5,'listen'),(5.1,'question'),(7.1,'explain'),(9,'point')],
        [(0,'think'),(1.8,'listen'),(2.8,'explain')]
    ]
    for i,s in enumerate(p['scenes']):
        L=s['duration'];s['objects']=[o for o in s['objects'] if not (o['kind']=='image' and Path(o.get('file','')).name=='presenter_master.png')]
        # Keep shoes entirely above the two-line subtitle safe area.
        close=i in (1,4,6)
        o=presenter(380 if close else 220,600 if close else 606,2.25 if close else 1.85,'rest');o.update(end=L,breath=.3,skin_color='#fbe7c7',blink_offset=1.2+i*.53)
        if close:
            for overlay in s['objects']:
                if overlay['kind']=='text' and overlay.get('name')!='Cảnh minh họa':overlay['end']=0
        if i==5:
            for title in s['objects']:
                if title['kind']=='text' and 'Một căn' in title.get('text',''):title['y']=105
                if title['kind']=='text' and 'Một phần bức tranh' in title.get('text',''):title.update(y=187,height=60)
        for t,pose in beats[i]:
            if t<L:apply_pose(o,pose,t,.5 if pose not in ('disagree','surprised') else .38)
        key(o,'face_tilt',[(0,-2),(.7,-6),(2.4,2),(3.6,-3),(min(5.2,L),4),(L,0)])
        key(o,'gaze',[(0,0),(.8,1.2),(2.1,0),(3.5,1),(min(5,L),0),(L,1)])
        key(o,'brow_lift',[(0,0),(.8,1.8),(1.6,0),(3.1,2),(3.8,0),(L,0)])
        if i in (2,5):
            key(o,'x',[(0,155),(1.6,228),(L,228)])
            o['motions']=[dict(start=0,end=1.6,action='walk',blend=.2)]
        if i==0:
            o['expressions']=[dict(t=0,v='curious'),dict(t=2.8,v='surprised'),dict(t=4.7,v='worried'),dict(t=6.5,v='normal')]
        elif i==1:
            o['expressions']=[dict(t=0,v='curious'),dict(t=1.2,v='worried'),dict(t=3.4,v='curious'),dict(t=5.2,v='happy')]
        elif i==3:
            o['expressions']=[dict(t=0,v='normal'),dict(t=3.6,v='curious'),dict(t=5.5,v='happy')]
            key(o,'face_tilt',[(0,0),(.4,-5),(.75,4),(1.1,-4),(1.5,0),(4,4),(5.3,0),(6.1,5),(6.7,0),(L,1)])
        elif i==4:
            o['expressions']=[dict(t=0,v='sad'),dict(t=4.9,v='normal'),dict(t=7,v='confident')]
            key(o,'face_tilt',[(0,-8),(2,-10),(4,-6),(5.4,0),(6.4,3),(L,0)])
        elif i==6:
            o['expressions']=[dict(t=0,v='curious'),dict(t=1.8,v='normal'),dict(t=2.8,v='happy')]
        s['objects'].append(o);actors.append(o)
        # Camera acts as a cut between wide and detail shots, instead of an idle zoom everywhere.
        if i in (1,4):
            s['camera']['keys']={'zoom':[dict(t=0,v=1),dict(t=L,v=1.04,ease='ease_in_out')]}
    add_waveforms(p,DEST);assert not preflight(p,DEST),preflight(p,DEST)
    saved=save(p,DEST/'project.json',DEST)
    short=copy.deepcopy(saved);short['name']='Thử diễn xuất 13 giây'
    short['scenes']=short['scenes'][:2];short['scenes'][1]['duration']=13.258-short['scenes'][1]['start']
    short['subtitles']=[c for c in short['subtitles'] if c['end']<=13.259]
    short['audio']=[dict(a,duration=min(a['duration'],13.258-a['start'])) for a in short['audio'] if a['start']<13.258]
    save(short,DEST/'acting_proof.json',DEST)
    (DEST/'acting_beats.json').write_text(json.dumps(beats,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Performance project ready: seven authored acting tracks; voice envelope bound')
    return saved

if __name__=='__main__':build()
