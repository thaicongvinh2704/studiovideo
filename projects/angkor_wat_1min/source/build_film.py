"""Original doodle cutout film authored as editable Studio SVG/parent/keyframe layers."""
import sys, math, json, copy, random, wave
from pathlib import Path
from xml.sax.saxutils import escape
from story import DEST, ROOT, STORY, SOURCES
sys.path.insert(0,str(ROOT))
from studio.project import new_project,new_scene,new_object,uid,save,pack
from studio.explainer import image_item,text_item,item
from studio.animation import ik
from studio.directing import preflight
from studio.subtitles import write as write_srt
ART=DEST/'art';INK='#222221';SKIN='#ffe4bf';BLUE='#8fc3da';STONE='#e6c58b';GREEN='#9bbd89';RED='#dd5948'

def path(d,fill='none',stroke=INK,sw=3,**attrs):
    extra=' '.join(f'{k.replace("_","-")}="{v}"' for k,v in attrs.items())
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" {extra}/>'
def ellipse(x,y,rx,ry,fill,stroke=INK,sw=3):
    return f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def svg(name,body,w,h):
    (ART/(name+'.svg')).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{body}</svg>',encoding='utf-8')

def tower(x,ground,height,width=105,fill=STONE):
    # Five nested lotus-like tiers on an original, deliberately simplified tower.
    top=ground-height;out=''
    points=[(x-width*.53,ground),(x-width*.53,ground-height*.24),(x-width*.39,ground-height*.27),
            (x-width*.39,ground-height*.46),(x-width*.30,ground-height*.49),
            (x-width*.30,ground-height*.64),(x-width*.21,ground-height*.67),
            (x-width*.21,ground-height*.80),(x-width*.12,ground-height*.82),
            (x-width*.12,ground-height*.90),(x,top),(x+width*.12,ground-height*.90),
            (x+width*.12,ground-height*.82),(x+width*.21,ground-height*.80),
            (x+width*.21,ground-height*.67),(x+width*.30,ground-height*.64),
            (x+width*.30,ground-height*.49),(x+width*.39,ground-height*.46),
            (x+width*.39,ground-height*.27),(x+width*.53,ground-height*.24),(x+width*.53,ground)]
    out+=path('M'+'L'.join(f'{a:.1f} {b:.1f}' for a,b in points)+'Z',fill,sw=3.5)
    # Petal-like shoulders, carved niches and tapered vertical ribs soften the outline.
    for f,ww in ((.30,.40),(.50,.30),(.68,.21),(.83,.12)):
        yy=ground-height*f;dy=height*.12
        out+=path(f'M{x-width*ww} {yy}Q{x-width*(ww+.10)} {yy-dy*.44} {x-width*(ww-.045)} {yy-dy}Q{x-width*(ww-.12)} {yy-dy*.25} {x-width*(ww-.08)} {yy}',fill,sw=2.3)
        out+=path(f'M{x+width*ww} {yy}Q{x+width*(ww+.10)} {yy-dy*.44} {x+width*(ww-.045)} {yy-dy}Q{x+width*(ww-.12)} {yy-dy*.25} {x+width*(ww-.08)} {yy}',fill,sw=2.3)
    for sign in (-1,1):
        out+=path(f'M{x+sign*width*.27} {ground-height*.05}V{ground-height*.20}Q{x+sign*width*.25} {ground-height*.29} {x+sign*width*.19} {ground-height*.36}',sw=1.6)
        out+=path(f'M{x+sign*width*.13} {ground-height*.48}L{x+sign*width*.08} {ground-height*.75}',stroke='#a88c5f',sw=1.8)
    for fraction,ww in ((.24,.49),(.46,.36),(.64,.27),(.80,.18)):
        yy=ground-height*fraction;out+=path(f'M{x-width*ww} {yy}Q{x} {yy+2} {x+width*ww} {yy}',sw=2)
    out+=path(f'M{x-14} {ground}V{ground-height*.20}Q{x} {ground-height*.27} {x+14} {ground-height*.20}V{ground}', '#8d765b',sw=2)
    return out

def make_art():
    ART.mkdir(exist_ok=True)
    ground=385
    body=path('M48 412Q250 408 496 412T953 412L955 435Q550 439 46 435Z','#e5cc9f',sw=3.5)
    body+=path('M85 384Q335 378 501 383T916 384L916 411H85Z','#efdab1',sw=3.5)
    # Background towers are lower; the central spire dominates the silhouette.
    for x,height,width in [(186,193,109),(814,193,109),(343,255,117),(657,255,117),(500,345,143)]:
        body+=tower(x,ground,height,width)
    body+=path('M100 354H899L919 379H80Z','#e9cf9f')
    body+=path('M91 380H910M92 397H910',sw=2)
    for x in range(113,905,43):
        if abs(x-500)>58:body+=path(f'M{x} 382V403M{x+14} 382V403',sw=1.8)
    body+=path('M452 434L470 359L531 359L549 434Z','#f6e9cb')
    for y in range(375,433,9):body+=path(f'M{467-(y-375)*.24:.1f} {y}H{533+(y-375)*.24:.1f}',sw=1.6)
    body+=path('M37 450Q100 445 166 450M839 450Q917 443 970 450',sw=2.5)
    svg('angkor_front',body,1000,470)
    svg('tower',tower(90,270,242,125)+path('M15 272H165V290H15Z','#eed7a9'),180,300)
    body=''
    for x,h,w in [(130,130,150),(300,210,190),(500,315,215),(700,210,190),(870,130,150)]:
        y=385-h;body+=path(f'M{x-w*.65} 392Q{x-w*.25} {y+65} {x} {y}Q{x+w*.25} {y+58} {x+w*.65} 392Z','#d0dce2')
        body+=path(f'M{x-w*.19} {y+62}L{x} {y}L{x+w*.19} {y+62}L{x+6} {y+43}L{x-6} {y+53}Z','#ffffff',sw=2)
    svg('meru',body,1000,470)
    # Clean common coordinate system for the new host: 300 px tall, head ~1/3.
    head=path('M15 62Q5 25 34 15Q68 -1 100 17Q125 31 118 69Q118 114 77 124Q32 130 17 94Z',SKIN,sw=3.2)
    head+=path('M17 60Q0 48 8 32L4 28L22 18L16 15L41 7L34 16L61 3L58 13L80 5L78 15L105 13L101 22L121 28L112 38Q87 29 75 37Q51 33 30 43L25 64Z','#343330',sw=3)
    head+=path('M11 62Q-1 52 1 69Q0 85 16 83',SKIN,sw=2.5)
    head+=path('M113 66Q131 56 128 75Q127 89 114 85',SKIN,sw=2.5)
    for d in ['M17 32L44 17','M29 29L62 15','M51 25L83 17','M76 26L104 27']:
        head+=path(d,stroke='#77736a',sw=1)
    svg('host_head',head,132,132)
    eyes=ellipse(44,70,3,5,INK,'none')+ellipse(86,70,3,5,INK,'none')+path('M36 55Q44 50 51 55M79 55Q87 50 94 55',sw=2.5)+path('M65 74L62 82L67 83',sw=1.7)
    svg('eyes',eyes,132,132)
    svg('blink',path('M37 71Q44 75 51 71M79 71Q86 75 93 71',sw=2.5)+path('M36 55Q44 50 51 55M79 55Q87 50 94 55',sw=2.5)+path('M65 74L62 82L67 83',sw=1.7),132,132)
    svg('mouth_closed',path('M53 96Q65 107 78 95',sw=2.5),132,132)
    svg('mouth_open',path('M52 94Q65 99 79 93Q77 114 65 113Q55 111 52 94Z','#49332d',sw=2.2)+path('M55 96Q66 100 76 95L74 101H58Z','#ffffff',sw=1),132,132)
    svg('body',path('M10 15L31 5Q48 13 64 5L86 16L97 48L78 53L72 41L75 114Q45 121 16 114L18 41L11 54L-1 45Z','#dcebf0',sw=3)+path('M32 7Q47 29 63 7',SKIN,sw=2.5)+path('M22 101Q45 104 69 101',stroke='#9ab9c6',sw=1.5),100,123)
    svg('arm',path('M8 -2L20 -2L19 65L7 65Z',SKIN,'none')+path('M8 -2Q8 30 7 65M20 -2Q20 30 19 65',sw=2.8),28,65)
    svg('elbow',ellipse(10,10,6,6,SKIN,'none'),20,20)
    svg('hand',path('M11 2L20 2L24 8L24 15L21 24L18 26L15 21L13 25L10 22L7 23L5 19L3 17L2 10L6 9L8 15L10 16Z',SKIN,sw=2.2),30,30)
    svg('hand_point',path('M10 2H20L22 9L24 10L23 15L19 18L16 30Q15 35 12 31L13 19L7 21L3 18L2 10L6 7L9 13Z',SKIN,sw=2.2),30,38)
    svg('leg',path('M6 2L29 2L26 89L34 97Q34 105 26 107L3 105L3 96L8 86Z','#728fa9',sw=3)+path('M4 95L24 94L34 98L34 106H3Z','#ffffff',sw=2.5),40,110)
    # Location sketch, not a surveyed boundary map.
    cmap=path('M84 30L128 34L147 14L204 32L236 26L253 62L278 71L292 115L283 141L304 168L279 208L236 211L219 245L196 247L174 287L152 271L138 238L114 242L94 214L76 207L63 177L45 165L52 126L27 106L42 77L69 74Z','#e5eedc',sw=3.5)
    cmap+=path('M117 89Q154 109 170 147Q177 180 209 208',stroke='#82aec5',sw=5)
    cmap+=ellipse(113,84,10,10,RED,'#ffffff',3)+path('M113 82V62',stroke=RED,sw=3)
    svg('cambodia',cmap,330,310)
    # A symbolic Vishnu illustration, visibly distinct from an archaeological photograph.
    v=path('M85 147Q40 140 24 104M115 148Q156 135 174 99M85 169Q42 179 18 153M113 170Q153 185 181 154',stroke=INK,sw=11)
    v+=path('M85 147Q40 140 24 104M115 148Q156 135 174 99M85 169Q42 179 18 153M113 170Q153 185 181 154',stroke='#a7c8da',sw=6)
    v+=path('M83 127L118 127L134 236H67Z','#f0cc7b')+ellipse(100,94,30,34,'#a7c8da')
    v+=path('M69 74L78 46L88 47L100 20L113 48L122 46L131 74Z','#e7be66')
    v+=ellipse(89,94,2.3,3.2,INK,'none')+ellipse(111,94,2.3,3.2,INK,'none')+path('M93 110Q100 114 108 109',sw=2)
    v+=ellipse(21,92,13,13,'none',sw=3)+path('M169 101L173 65L184 59L191 71L185 84L174 86','#e9c886')
    v+=path('M7 143Q16 128 29 141Q32 155 19 161Z','#f4ede2')+path('M171 155Q173 136 181 135Q187 138 187 150Q194 141 198 149Q198 165 181 168Z','#eeb4ae')
    v+=path('M63 237Q99 248 137 236L144 255H54Z','#e9d7a1')
    svg('vishnu',v,205,270)
    # Schematic temple plan: center plus the four corners, with a causeway.
    plan=path('M25 33Q29 18 47 22L686 23Q704 20 705 39L703 446Q699 461 679 459L42 457Q22 459 24 439Z','#bfdeec',sw=3.8)
    plan+=path('M111 104L618 107L615 373L108 370Z','#efe0bc',sw=3.5)
    plan+=path('M263 170L464 171L462 304L262 302Z','#f8edd4',sw=2.5)
    for x,y in [(293,193),(432,193),(293,277),(432,277),(362,235)]:plan+=ellipse(x,y,21 if x!=362 else 29,19 if x!=362 else 27,STONE,sw=3)
    plan+=path('M342 301H381L380 460H342Z','#f8f5e9',sw=3)
    for x,y in [(57,70),(476,65),(50,417),(485,418),(53,245),(649,232)]:plan+=path(f'M{x} {y}q15 -9 30 0t30 0',stroke='#6da7c1',sw=2)
    svg('moat_plan',plan,730,485)
    top=path('M40 35L690 38L687 415L38 411Z','#f5e9cb',sw=3.5)
    for j,(x,y) in enumerate([(170,120),(550,120),(170,330),(550,330),(360,224)]):
        top+=ellipse(x,y,40 if j<4 else 54,36 if j<4 else 49,STONE,sw=3.5)
        top+=path(f'M{x-16} {y}H{x+16}M{x} {y-16}V{y+16}',sw=2)
    svg('five_plan',top,730,450)
    monk=ellipse(76,49,31,35,SKIN,sw=3)+path('M55 43Q61 40 66 43M84 43Q91 40 97 43M67 64Q77 70 87 63',sw=2.1)
    monk+=path('M56 84L89 84L119 212L28 213L39 117Z','#e9aa69',sw=3)
    monk+=path('M56 87L96 145L39 165M48 170L82 149M63 174L93 163',stroke='#bb7743',sw=2)
    monk+=path('M38 111Q22 128 44 143L65 130M99 115Q123 138 102 146L82 132',SKIN,sw=3)
    monk+=ellipse(74,125,10,17,SKIN,sw=2.5)+path('M49 213L45 235H70L74 217M89 214L96 235H115L109 214',SKIN,sw=2.5)
    svg('monk',monk,145,245)
    # A playful question mark and hand drawn emphasis marks are separate editable assets.
    svg('question',path('M24 52Q17 9 60 9Q108 12 93 50Q86 66 61 75V99',stroke=RED,sw=11)+ellipse(61,126,6,6,RED,'none'),120,145)
    svg('spark',path('M40 2L45 28L73 37L46 44L39 73L32 45L4 36L30 29Z','#f1cf75',sw=2.6),80,80)
    svg('arrow',path('M8 39Q86 28 165 39L144 19M165 39L143 58',stroke=RED,sw=4),180,75)
    svg('underline',path('M8 17Q137 9 290 16M48 23Q155 18 265 23',stroke=RED,sw=4),300,40)
    svg('cross',path('M15 14L101 98M101 15L14 100',stroke=RED,sw=8),115,115)

class Stage:
    def __init__(self,scene):self.s=scene;self.L=scene['duration'];self.objects=scene['objects']
    def add(self,o,start=0,end=None,layer=20,parent=None):
        o.update(start=start,end=self.L if end is None else end,layer=layer)
        if parent:o['parent']=parent['id'] if isinstance(parent,dict) else parent
        self.objects.append(o);return o
    def group(self,x=0,y=0,scale=1,parent=None,start=0):
        o=new_object('group','group',x,y);o['scale']=scale;return self.add(o,start,parent=parent)
    def art(self,name,x,y,w,h,layer=20,start=0,end=None,parent=None,**extra):
        o=image_item(str(ART/(name+'.svg')),x,y,w,h);o.update(extra)
        return self.add(o,start,end,layer,parent)
    def text(self,value,x,y,w=850,h=95,size=34,start=0,end=None,color=INK,**extra):
        settings=dict(font='Segoe Print',color=color);settings.update(extra)
        o=text_item(value,x,y,w,h,size,**settings)
        return self.add(o,start,end,80)
    def key(self,o,name,pairs,ease='ease_in_out'):
        o.setdefault('keys',{})[name]=[dict(t=round(t,5),v=v,ease=ease) for t,v in pairs];return o
    def appear(self,o,t=.2):
        o['start']=t;o['enter']='fade';o['enter_duration']=.24
        sc=o.get('scale',1);self.key(o,'scale',[(t,sc*.92),(t+.23,sc*1.025),(t+.4,sc)])
        return o
    def line(self,points,start=0,color=INK,sw=3,reveal=False):
        o=item('shape','drawn line',0,0,1280,720,shape='path',points=points,color=color,stroke=sw,reveal=reveal,enter_duration=.65)
        return self.add(o,start,layer=50)
    def host(self,x=192,y=597,scale=1.28,poses=None,speaking=True):
        root=self.group(x,y,scale);root['name']='Người kể · rig doodle mới'
        body=self.art('body',0,-137,100,123,25,parent=root)
        for side,xx in [('l',-20),('r',20)]:
            leg=self.group(xx,-91,parent=root)
            self.art('leg',0,53,40,110,15,parent=leg)
        head=self.group(0,-236,parent=root)
        self.art('host_head',0,0,132,132,40,parent=head)
        eyes=self.art('eyes',0,0,132,132,43,parent=head)
        blink=self.art('blink',0,0,132,132,44,parent=head)
        shut=self.art('mouth_closed',0,0,132,132,44,parent=head)
        opened=self.art('mouth_open',0,0,132,132,45,parent=head)
        blinkkeys=[(0,0)]
        for t in [1.7,4.9,8.0,11.1]:
            if t+.12<self.L:blinkkeys.extend([(t,0),(t+.02,1),(t+.12,0)])
        self.key(blink,'opacity',blinkkeys,'hold');self.key(eyes,'opacity',[(t,1-v) for t,v in blinkkeys],'hold')
        if speaking:
            samples,rate=NARRATION
            keys=[]
            for j in range(int(self.L*12)+1):
                t=min(self.L,j/12);a=int((self.s['start']+t)*rate);seg=samples[a:a+int(rate*.07)]
                rms=float((seg*seg).mean()**.5) if len(seg) else 0
                keys.append((t,1 if rms>.018 else 0))
            self.key(opened,'opacity',keys,'hold');self.key(shut,'opacity',[(t,1-v) for t,v in keys],'hold')
        else:opened['opacity']=0
        beats=poses or [(0,'rest'),(.6,'question'),(2.2,'point'),(4.2,'explain'),(self.L-.8,'rest')]
        beats=[(min(max(0,t),self.L),pose) for t,pose in beats]
        targets={'rest':((-46,-57),(46,-57)),'point':((-54,-92),(143,-176)),
                 'explain':((-80,-113),(107,-222)),'think':((-62,-95),(18,-213)),
                 'question':((-112,-211),(110,-211)),'greet':((-50,-89),(78,-259)),
                 'wide':((-130,-185),(130,-185))}
        for side,sign in [('l',-1),('r',1)]:
            sx=sign*36;sy=-171;upper=self.group(sx,sy,parent=root)
            self.art('arm',0,30,28,65,18,parent=upper)
            fore=self.group(0,55,parent=upper)
            self.art('arm',0,30,28,65,28,parent=fore)
            self.art('elbow',0,0,20,20,29,parent=fore)
            self.art('hand_point' if side=='r' else 'hand',0,67,30,38 if side=='r' else 30,31,parent=fore)
            uk=[];fk=[]
            for t,pose in beats:
                target=targets.get(pose,targets['rest'])[0 if side=='l' else 1]
                elbow,wrist=ik((sx,sy),target,55,55,bend=-sign)
                a=math.degrees(math.atan2(-(elbow[0]-sx),elbow[1]-sy))
                b=math.degrees(math.atan2(-(wrist[0]-elbow[0]),wrist[1]-elbow[1]))-a
                if t>0:
                    uk.append((max(0,t-.38),uk[-1][1] if uk else a));fk.append((max(0,t-.38),fk[-1][1] if fk else b))
                uk.append((t,a));fk.append((t,b))
            self.key(upper,'rotation',uk);self.key(fore,'rotation',fk)
        self.key(head,'rotation',[(0,-3),(.7,2),(2.2,-4),(3.8,2),(self.L,0)])
        return root

def make_sound():
    import numpy as np, soundfile as sf
    sr=48000;audio=np.zeros(60*sr,dtype=np.float32)
    # Original quiet pentatonic plucks. These are not represented as Cambodian traditional music.
    for i in range(28):
        start=.3+i*2.1;freq=[196,246.94,293.66,369.99,440,293.66,246.94][i%7]
        t=np.arange(int(sr*2.7))/sr;env=np.exp(-t*2.2)*(1-np.exp(-t*90))
        tone=.06*env*(np.sin(2*np.pi*freq*t)+.25*np.sin(2*np.pi*freq*2*t)+.09*np.sin(2*np.pi*freq*3*t))
        a=int(start*sr);n=min(len(tone),len(audio)-a);audio[a:a+n]+=tone[:n]
    sf.write(DEST/'music_original.wav',audio,sr,subtype='PCM_16')
    rng=np.random.default_rng(77);t=np.arange(int(.14*sr))/sr
    pop=(np.sin(2*np.pi*(800*t-1600*t*t))*.35+rng.normal(0,.03,len(t)))*np.exp(-t*38)
    sf.write(DEST/'pop_original.wav',pop,sr,subtype='PCM_16')

NARRATION=None
def build():
    import numpy as np,soundfile as sf
    global NARRATION
    samples,rate=sf.read(DEST/'narration.wav',dtype='float32');NARRATION=(samples.mean(axis=1) if samples.ndim>1 else samples,rate)
    timing=json.loads((DEST/'voice_timing.json').read_text(encoding='utf-8'));cues=timing['cues']
    make_art();make_sound()
    boundaries=[0]+[row['start']-.10 for row in cues[1:]]+[60]
    p=new_project('Angkor Wat · Một vũ trụ bằng đá',60,1920,1080)
    p.update(scenes=[],fps=30,render_profile='final',encoder_threads=2,audio_rate=48000,audio_channels=2,audio=[],subtitles=[],duck_music=True)
    p['subtitle_style'].update(size=26,font='Segoe UI',background=True,y=.974)
    shots=[]
    for i,(a,b) in enumerate(zip(boundaries,boundaries[1:])):
        s=new_scene(STORY[i]['name'],b-a);s.update(start=a,background='white',style='doodle_angkor_original',objects=[])
        p['scenes'].append(s);st=Stage(s);L=b-a
        st.text('ANGKOR WAT',178,42,280,45,21,color='#686760',font='Segoe UI',bold=True)
        st.text(f'{i+1:02} / 08',1173,42,140,45,18,color='#89867e',font='Segoe UI')
        if i==0:
            st.host(180,602,1.32,[(0,'think'),(.7,'question'),(2.4,'point'),(4.5,'wide'),(L-.6,'point')])
            temple=st.art('angkor_front',820,393,770,362);st.appear(temple,.18)
            st.text('Chỉ là một ngôi đền?',810,113,780,95,39,end=L*.5)
            st.text('MỘT VŨ TRỤ BẰNG ĐÁ!',813,113,810,95,39,start=L*.5,color=INK,bold=True)
            st.appear(st.art('question',1115,212,68,82),.8);st.appear(st.art('spark',514,217,51,51),L*.5)
            st.appear(st.art('underline',818,175,350,40),L*.5)
        elif i==1:
            st.host(157,601,1.19,[(0,'rest'),(.6,'point'),(2.4,'explain'),(L-.5,'point')])
            st.appear(st.art('cambodia',497,310,325,305),.12)
            st.text('CAMPUCHIA',501,498,370,65,30)
            st.appear(st.art('angkor_front',938,348,515,242),1.0)
            st.text('ĐẦU THẾ KỶ XII',935,139,550,75,34,start=1.0)
            st.appear(st.art('underline',938,190,340,37),1.5)
            st.text('Vua Suryavarman II',938,519,540,85,29,start=max(1,L*.48))
            st.line([(328,587),(1190,587)],start=.5,color='#999386',reveal=True)
        elif i==2:
            st.host(160,602,1.22,[(0,'point'),(1.8,'explain'),(3.5,'question'),(L-.4,'point')])
            st.appear(st.art('vishnu',524,334,245,322),.1)
            st.text('VISHNU',525,125,400,70,37)
            st.text('Ấn Độ giáo',525,548,400,65,28)
            st.art('angkor_front',964,355,420,198)
            st.appear(st.art('question',966,185,76,92),max(.5,L*.48))
            st.text('Năm tháp để làm gì?',949,535,550,90,30,start=max(.5,L*.48))
        elif i==3:
            st.host(143,606,1.1,[(0,'point'),(1.9,'wide'),(4,'explain'),(L-.5,'point')])
            temple=st.art('angkor_front',826,366,786,369)
            mountain=st.art('meru',826,366,786,369)
            change=L*.24
            st.key(temple,'opacity',[(0,1),(change-.2,1),(change+.5,0)])
            st.key(mountain,'opacity',[(0,0),(change-.2,0),(change+.5,1)])
            st.text('5 THÁP',833,113,700,85,39,end=change+.1)
            st.text('5 ĐỈNH NÚI MERU',833,113,780,85,39,start=change+.1)
            for j,(xx,yy) in enumerate([(579,341),(701,291),(826,221),(949,291),(1072,341)]):
                st.text(str(j+1),xx,yy-30,70,60,29,start=.3+j*.25,color=RED,bold=True)
            st.text('Sơ đồ biểu tượng · không phải bản phục dựng',825,572,800,45,19,font='Segoe UI',color='#77736c',start=change)
            topstart=L*.56
            st.key(mountain,'opacity',[(0,0),(change-.2,0),(change+.5,1),(topstart-.2,1),(topstart+.2,0)])
            st.appear(st.art('five_plan',825,363,670,413,start=topstart),topstart)
            st.text('NHÌN TỪ TRÊN XUỐNG',825,109,830,83,33,start=topstart)
            # Prevent the new title from being superimposed on the preceding one.
            for prior in s['objects']:
                if prior['kind']=='text' and prior.get('text')=='5 ĐỈNH NÚI MERU':prior['end']=topstart
                if prior['kind']=='text' and prior.get('text') in ('1','2','3','4','5'):prior['end']=topstart
        elif i==4:
            st.host(150,604,1.12,[(0,'question'),(1.7,'point'),(3.4,'explain'),(L-.5,'point')])
            st.art('moat_plan',820,366,665,442)
            st.text('HÀO NƯỚC',816,103,770,85,38,end=L*.32)
            st.text('ĐẠI DƯƠNG BAO QUANH',816,103,800,85,35,start=L*.32,color='#346f8b')
            st.appear(st.art('arrow',385,353,150,62),.8)
            # A tiny traveller crosses the moat on the causeway as the line explains it.
            mini=st.art('monk',820,557,41,70,start=L*.48)
            st.key(mini,'y',[(L*.48,557),(L*.87,409),(L,409)])
            st.text('Từ thế giới thường → không gian thiêng',827,611,810,50,22,start=L*.5)
        elif i==5:
            st.host(162,605,1.16,[(0,'point'),(1.6,'explain'),(L-.5,'wide')])
            st.art('angkor_front',807,359,690,324)
            st.appear(st.art('monk',1093,456,104,176),max(.3,L*.25))
            st.text('ẤN ĐỘ GIÁO',562,144,420,70,31,end=L*.35)
            st.text('PHẬT GIÁO',1000,144,420,70,31,start=L*.35)
            st.appear(st.art('arrow',792,144,175,73),L*.3)
            st.text('Một công trình · nhiều lớp lịch sử',813,580,820,70,28,start=L*.46)
        elif i==6:
            st.host(178,600,1.25,[(0,'question'),(1.6,'think'),(3,'point'),(L-.4,'explain')])
            st.text('TỪNG BỊ QUÊN LÃNG?',825,117,840,95,38,end=L*.40)
            st.text('NGƯỜI ĐỊA PHƯƠNG VẪN BIẾT ĐẾN',820,117,860,95,30,start=L*.40,bold=True)
            st.art('angkor_front',825,356,730,343)
            st.appear(st.art('cross',1140,213,80,80,end=L*.40),L*.22)
            for j in range(2):
                monk=st.art('monk',470-j*61,527+j*7,71,120,start=L*.36+j*.28)
                st.key(monk,'x',[(L*.36+j*.28,440-j*61),(L*.84,634-j*64),(L,634-j*64)])
            st.text('Các nhà sư vẫn lui tới nơi này',829,589,760,70,27,start=L*.56)
        else:
            st.host(179,603,1.29,[(0,'think'),(1.3,'point'),(3,'wide'),(L-.4,'greet')])
            st.art('angkor_front',820,365,755,355)
            st.text('ĐỌC NGÔI ĐỀN NHƯ MỘT…',820,104,830,85,32,end=L*.45)
            st.text('BẢN ĐỒ VŨ TRỤ',820,104,800,85,43,start=L*.45,bold=True)
            for j,(xx,yy) in enumerate([(500,180),(1132,220),(1043,155)]):st.appear(st.art('spark',xx,yy,43,43),.5+j*.4)
            st.text('Nguồn: APSARA · NASA · Carter và cộng sự, PNAS 2019',803,598,890,45,17,font='Segoe UI',color='#77736c',start=L*.5)
        # Keep every hand and shoe within the picture safe area.
        for root in s['objects']:
            if root['kind']=='group' and root.get('name')=='Người kể · rig doodle mới':
                root['x']=max(205,root['x']);root['y']-=16
        # Subtitle cues follow measured speech boundaries. Split whole sentences for legibility.
        cue=cues[i];sentences=[z.strip()+'.' for z in cue['text'].rstrip('.').split('. ') if z.strip()]
        total=sum(len(z.split()) for z in sentences);cursor=cue['start']
        for sentence in sentences:
            end=cursor+(cue['end']-cue['start'])*len(sentence.split())/total
            p['subtitles'].append(dict(id=uid(),start=cursor,end=end,text=sentence,role='Narrator',scene_id=s['id']));cursor=end
        shots.append(dict(scene=i+1,name=s['name'],start=a,end=b,narration=cue['text'],layers=len(s['objects'])))
    p['audio']=[dict(id='narration',name='VieNeu-TTS · Hải Đăng',file=str(DEST/'narration.wav'),start=0,duration=60,group='voice',volume=1),
                dict(id='music',name='Nhạc gảy nhẹ · sáng tác bằng tổng hợp âm',file=str(DEST/'music_original.wav'),start=0,duration=60,group='music',volume=.48,fade_in=1.0,fade_out=1.7)]
    for j,s in enumerate(p['scenes']):
        if j in (0,1,3,4,7):p['audio'].append(dict(id='pop_'+str(j),name='Nét bật · tự tạo',file=str(DEST/'pop_original.wav'),start=s['start']+.3,duration=.14,group='sfx',volume=.17))
    assert not preflight(p,DEST),preflight(p,DEST)
    saved=save(p,DEST/'project.json',DEST);write_srt(p['subtitles'],DEST/'phu_de.srt')
    (DEST/'shot_list.json').write_text(json.dumps(shots,ensure_ascii=False,indent=2),encoding='utf-8')
    (DEST/'art_manifest.json').write_text(json.dumps(dict(style='Original white-background ink doodle, flat colors, articulated SVG cutouts',source='All SVG paths authored specifically for this film; no frames copied from the reference video',reference='https://www.youtube.com/watch?v=kcWEaXRh2hA',voice=timing['voice'],assets=[x.name for x in ART.glob('*.svg')]),ensure_ascii=False,indent=2),encoding='utf-8')
    print('PROJECT READY:',len(p['scenes']),'scenes;',sum(len(s['objects']) for s in p['scenes']),'editable layers;',len(p['subtitles']),'subtitles',flush=True)
    return saved

def render_preview(p):
    from PySide6.QtWidgets import QApplication
    from PySide6.QtGui import QImage,QPainter,QFont,QColor
    from studio.renderer import Renderer
    app=QApplication.instance() or QApplication([]);r=Renderer()
    sheet=QImage(1280,1440,QImage.Format.Format_RGB32);sheet.fill(QColor('white'));painter=QPainter(sheet)
    for i,s in enumerate(p['scenes']):
        t=s['start']+min(s['duration']*.65,s['duration']-.1)
        frame=r.frame(p,DEST,t,1280,720);frame.save(str(DEST/'review'/f'scene_{i+1:02}.png'))
        painter.drawImage((i%2)*640,(i//2)*360,frame.scaled(640,360))
    painter.end();sheet.save(str(DEST/'review'/'storyboard.png'))
    print('PREVIEW READY',flush=True)

if __name__=='__main__':
    project=build();render_preview(project)
