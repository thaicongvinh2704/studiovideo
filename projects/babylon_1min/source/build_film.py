"""Illustrated 2.5D documentary with a single visual narrative and editable Studio layers."""
import sys,json,math,random
from pathlib import Path
from story import ROOT,DEST,STORY,SOURCES
sys.path.insert(0,str(ROOT))
from studio.project import new_project,new_scene,new_object,uid,save
from studio.explainer import item,text_item,image_item
from studio.directing import preflight
from studio.subtitles import write as write_srt
ART=DEST/'art';INK='#24302e';CREAM='#fff3d5';TEAL='#74d4d6';GOLD='#f6cf7a'

def svg(name,body,w=1280,h=720):
 (ART/(name+'.svg')).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{body}</svg>',encoding='utf-8')

def make_vectors():
 svg('reading_shade','''<defs><linearGradient id="top" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#101f24" stop-opacity=".83"/><stop offset="1" stop-color="#101f24" stop-opacity="0"/></linearGradient><linearGradient id="bottom" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#101f24" stop-opacity="0"/><stop offset="1" stop-color="#101f24" stop-opacity=".95"/></linearGradient></defs><rect width="1280" height="190" fill="url(#top)"/><rect y="530" width="1280" height="190" fill="url(#bottom)"/>''')
 # An illustrative location map, with northern Nineveh above and slightly west of Babylon.
 body='''<defs><linearGradient id="sand" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#f4e2b9"/><stop offset="1" stop-color="#d8b77c"/></linearGradient></defs><rect width="1280" height="720" fill="url(#sand)"/>'''
 rng=random.Random(317)
 for j in range(110):
  x,y=rng.uniform(0,1280),rng.uniform(30,720);w=rng.uniform(18,80)
  body+=f'<path d="M{x:.1f} {y:.1f}q{w/2:.1f} -7 {w:.1f} 0" fill="none" stroke="#b99262" stroke-opacity=".22" stroke-width="1.1"/>'
 # Hill contours at the north-east edge, rendered in the same warm ink palette.
 for j in range(5):
  x=755+j*70;y=100+j*24
  body+=f'<path d="M{x-60} {y+115}L{x} {y}L{x+90} {y+120}M{x-19} {y+45}l19 -45 24 44" fill="#bfa47a" stroke="#887c5b" stroke-opacity=".6" stroke-width="1.5"/>'
 euphrates='M140 62C270 95 285 192 310 262S410 360 470 420S522 482 570 504S720 593 810 680'
 tigris='M565 32C566 108 622 137 630 192S697 269 718 323S690 383 732 433S754 501 794 545S827 625 885 685'
 for d in [euphrates,tigris]:
  body+=f'<path d="{d}" fill="none" stroke="#385f65" stroke-width="13" stroke-linecap="round"/><path d="{d}" fill="none" stroke="#7cb5b4" stroke-width="8" stroke-linecap="round"/>'
 body+='<path d="M794 545Q816 578 845 602" fill="none" stroke="#7cb5b4" stroke-width="5"/>'
 svg('mesopotamia_map',body)
 svg('pin','<path d="M20 3C8 3 1 11 1 21C1 34 20 52 20 52S39 34 39 21C39 11 32 3 20 3Z" fill="#ae5638" stroke="#fff0d0" stroke-width="2.3"/><circle cx="20" cy="20" r="6" fill="#fff0d0"/>',40,56)
 svg('halo','<circle cx="60" cy="60" r="47" fill="none" stroke="#f5d18b" stroke-width="2.5"/><circle cx="60" cy="60" r="35" fill="none" stroke="#f5d18b" stroke-width="1" stroke-opacity=".6"/>',120,120)
 svg('small_glint','<path d="M3 5Q24 1 45 5T87 5M26 13Q42 10 61 13" fill="none" stroke="#ffeac0" stroke-width="1.4" stroke-linecap="round"/>',94,20)

class Stage:
 def __init__(self,s):self.s=s;self.L=s['duration']
 def add(self,o,start=0,end=None,layer=20,parent=None):
  o.update(start=start,end=self.L if end is None else end,layer=layer)
  if parent:o['parent']=parent['id']
  self.s['objects'].append(o);return o
 def group(self,x=640,y=360,scale=1,name='Composition',parent=None):
  o=new_object('group',name,x,y);o['scale']=scale;return self.add(o,parent=parent)
 def image(self,name,x=640,y=360,w=1280,h=720,layer=20,parent=None,start=0,end=None):
  return self.add(image_item(str(ART/name),x,y,w,h),start,end,layer,parent)
 def text(self,text,x=640,y=75,w=1120,h=70,size=34,start=0,end=None,color=CREAM,bold=False,align='center',layer=90):
  return self.add(text_item(text,x,y,w,h,size,color=color,font='Segoe UI',bold=bold,align=align),start,end,layer)
 def key(self,o,k,points,ease='ease_in_out'):
  o.setdefault('keys',{})[k]=[dict(t=max(0,min(self.L,float(t))),v=v,ease=ease) for t,v in points];return o
 def fade(self,o,t,d=.4,initial=0,final=1):
  o['opacity']=initial;return self.key(o,'opacity',[(0,initial),(t,initial),(t+d,final)])
 def line(self,points,t=0,d=.8,color=TEAL,sw=3,parent=None,layer=65):
  o=item('shape','Water / evidence route',0,0,1280,720,shape='path',points=points,color=color,stroke=sw,reveal=True,enter_duration=d)
  return self.add(o,start=t,layer=layer,parent=parent)
 def dot(self,x,y,r=4,color=CREAM,parent=None,layer=72):
  return self.add(item('shape','Moving water cue',x,y,r*2,r*2,shape='ellipse',fill=color,color=color,stroke=0),parent=parent,layer=layer)
 def shade(self):return self.image('reading_shade.svg',layer=80)
 def title(self,title,eyebrow='',t=0,end=None,size=34):
  if eyebrow:self.text(eyebrow,y=31,h=26,size=15,start=t,end=end,color='#e1dfc8',bold=True)
  o=self.text(title,y=78,h=75,size=size,start=t,end=end,bold=True)
  if t>0:self.fade(o,t,.35)
  return o
 def background(self,name,z0=1.03,z1=1.08,x0=640,x1=640,y0=360,y1=360):
  g=self.group(name='Illustrated background: '+name)
  self.image(name,x=0,y=0,parent=g)
  self.key(g,'scale',[(0,z0),(self.L,z1)])
  self.key(g,'x',[(0,x0),(self.L,x1)]);self.key(g,'y',[(0,y0),(self.L,y1)])
  return g
 def foreground(self,right=False):
  g=self.group(275 if not right else 1150,580,.76,name='Independent foreground plants')
  self.image('foreground_plants.png',0,0,1100,619,layer=62,parent=g)
  self.key(g,'x',[(0,g['x']-12),(self.L,g['x']+10)])
  self.key(g,'rotation',[(t,1.0*math.sin(t*1.6)) for t in [i*.35 for i in range(math.ceil(self.L/.35)+1)]])
  return g

def make_sound():
 import numpy as np,soundfile as sf
 sr=48000;L=60;t=np.arange(sr*L)/sr;music=np.zeros(sr*L,dtype=np.float32)
 # Original restrained modal plucks, no claim to authentic ancient music.
 for i in range(30):
  at=.3+i*2.0;freq=[146.832,174.614,220,261.626,220,174.614][i%6]
  tt=np.arange(int(sr*2.5))/sr;env=(1-np.exp(-tt*100))*np.exp(-tt*2.1)
  tone=.045*env*(np.sin(2*np.pi*freq*tt)+.24*np.sin(4*np.pi*freq*tt)+.07*np.sin(6*np.pi*freq*tt))
  a=int(at*sr);n=min(len(tone),len(music)-a);music[a:a+n]+=tone[:n]
 music+=.008*np.sin(2*np.pi*73.416*t)*np.minimum(1,t/4)*np.minimum(1,(60-t)/4)
 sf.write(DEST/'music_original.wav',music,sr,subtype='PCM_16')
 rng=np.random.default_rng(214);noise=rng.normal(0,1,sr*12)
 smooth=np.convolve(noise,np.ones(110)/110,mode='same');smooth*=.11
 smooth*=np.minimum(1,np.arange(len(smooth))/sr)*np.minimum(1,(len(smooth)-np.arange(len(smooth)))/sr)
 sf.write(DEST/'water_original.wav',smooth,sr,subtype='PCM_16')
 tt=np.arange(int(sr*.38))/sr
 whoosh=np.convolve(rng.normal(0,1,len(tt)),np.ones(12)/12,mode='same')*.045*np.sin(np.pi*tt/.38)**2
 sf.write(DEST/'transition_original.wav',whoosh,sr,subtype='PCM_16')

def build():
 make_vectors();make_sound()
 timing=json.loads((DEST/'voice_timing.json').read_text(encoding='utf-8'));cues=timing['cues']
 grouped=[[c for c in cues if c['scene']==i] for i in range(len(STORY))]
 bounds=[0]+[c[0]['start']-.16 for c in grouped[1:]]+[60]
 p=new_project('Vườn treo Babylon · Kỳ quan ở đâu?',60,1920,1080)
 p.update(scenes=[],fps=30,render_profile='final',encoder_threads=2,audio_rate=48000,audio_channels=2,audio=[],subtitles=[],duck_music=True)
 p['subtitle_style'].update(size=27,font='Segoe UI',background=False,y=.962,color='#fff8e9')
 shots=[]
 for i,(a,b) in enumerate(zip(bounds,bounds[1:])):
  s=new_scene(STORY[i]['name'],b-a);s.update(start=a,background='white',background_color='#162e31',objects=[],style='illustrated_comic_babylon')
  p['scenes'].append(s);st=Stage(s);L=st.L;phrases=grouped[i];marks=[c['start']-a for c in phrases]
  if i==0:
   bg=st.background('garden_wide.png',1.13,1.02,x0=615,x1=640,y0=375,y1=360)
   st.foreground()
   # Slow luminous ripples are independent layers rather than a static photograph zoom.
   for j,(x,y,w) in enumerate([(690,579,120),(940,601,155),(1120,563,105),(790,622,95)]):
    glint=st.image('small_glint.svg',x,y,w,25,layer=55)
    st.key(glint,'x',[(0,x-12),(L,x+16)])
    st.key(glint,'opacity',[(t,.18+.22*(1+math.sin(t*1.8+j))) for t in [k*.45 for k in range(math.ceil(L/.45)+1)]])
   st.shade()
   st.title('VƯỜN TREO BABYLON','HÌNH DUNG MỘT KỲ QUAN',end=marks[-1],size=42)
   st.title('KỲ QUAN ẤY Ở ĐÂU?',t=marks[-1],size=38)
   st.text('Minh họa giả định',x=1112,y=598,w=260,h=24,size=13,color='#e5e4cc',layer=88)
  elif i==1:
   bg=st.background('terrace_close.png',1.07,1.16,x0=650,x1=602,y0=365,y1=380)
   # Two subtle water glints progress down the real painted channel.
   for j in range(3):
    glint=st.image('small_glint.svg',773,465,48,12,layer=60,parent=None)
    st.key(glint,'x',[(0,610+j*65),(L,862+j*45)])
    st.key(glint,'y',[(0,413+j*34),(L,571+j*25)])
    st.key(glint,'opacity',[(0,0),(.4+j*.3,.45),(L-.4,.45),(L,0)])
   st.shade();st.title('MỘT NGỌN ĐỒI ĐƯỢC XÂY LÊN','CÂY MỌC TRÊN CÁC TẦNG NỀN',end=marks[-1])
   st.title('“TREO” KHÔNG PHẢI LƠ LỬNG',t=marks[-1],size=34)
   st.text('Hình dung theo mô tả cổ',x=1090,y=597,w=330,h=25,size=13,color='#e5e4cc')
  elif i==2:
   bg=st.background('water_section.png',1,1)
   # A deliberately schematic overlay marks only the need to raise and distribute water.
   route=[(143,539),(143,163),(176,163)]
   st.line(route,t=.65,d=2.5,color='#193f4c',sw=8,layer=60)
   st.line(route,t=.65,d=2.5,color=TEAL,sw=4,layer=61)
   for j in range(3):
    dot=st.dot(143,539,4,color='#fff3c9')
    tt=.7+j*.7
    dot['start']=tt;dot['end']=min(L,tt+2.7)
    st.key(dot,'y',[(tt,539),(tt+2.4,163)]);st.key(dot,'x',[(tt,143),(tt+2.4,143)])
   t=marks[1]
   for j,pts in enumerate([[(194,155),(465,155)],[(370,289),(792,289)],[(744,468),(1043,468)]]):
    st.line(pts,t=t+j*.28,d=1.5,color='#22434a',sw=7,layer=60)
    st.line(pts,t=t+j*.28,d=1.5,color=TEAL,sw=3.6,layer=61)
   st.shade();st.title('BÀI TOÁN LÀ NƯỚC','MINH HỌA NGUYÊN LÝ · KHÔNG PHẢI CƠ CẤU ĐÃ XÁC NHẬN',end=marks[-1])
   st.title('CƠ CẤU CỤ THỂ: CHƯA XÁC NHẬN',t=marks[-1],size=31)
  elif i==3:
   st.background('excavation.png',1.02,1.09,x0=640,x1=625,y0=360,y1=365)
   st.shade();st.title('HÌNH DUNG KHÁC VỚI CHỨNG CỨ','BẰNG CHỨNG Ở BABYLON VẪN CHƯA THUYẾT PHỤC',size=33)
   st.text('Cảnh khảo cổ minh họa',x=1090,y=598,w=330,h=25,size=13,color='#e5e4cc')
  elif i==4:
   st.image('mesopotamia_map.svg')
   # Schematic relative locations: Babylon on the Euphrates, Nineveh on the Tigris to the north.
   st.text('LƯỠNG HÀ',x=1045,y=500,w=330,h=70,size=39,color='#947852',bold=True,layer=40)
   st.text('Euphrates',x=300,y=353,w=200,h=35,size=21,color='#3c696e',layer=45)
   st.text('Tigris',x=770,y=276,w=170,h=35,size=21,color='#3c696e',layer=45)
   st.image('pin.svg',570,484,40,56,layer=55)
   st.text('BABYLON',x=397,y=506,w=260,h=45,size=29,color=INK,bold=True)
   pin=st.image('pin.svg',630,166,40,56,layer=55);st.fade(pin,.6,.4)
   label=st.text('NINEVEH',x=798,y=180,w=260,h=45,size=30,color=INK,bold=True);st.fade(label,.8,.4)
   # A soft dashed line asks about attribution, not travel or a proven relocation.
   for j in range(14):
    u=j/14;v=(j+.5)/14
    pts=[(570+(630-570)*u,504+(192-504)*u),(570+(630-570)*v,504+(192-504)*v)]
    line=st.line(pts,t=.9+j*.07,d=.2,color='#ad603b',sw=2,layer=48)
   halo=st.image('halo.svg',630,193,110,110,layer=50)
   st.key(halo,'scale',[(t,.65+.2*(1+math.sin(t*2))) for t in [k*.4 for k in range(math.ceil(L/.4)+1)]])
   st.key(halo,'opacity',[(0,0),(.8,.7),(L,.7)])
   st.shade();st.title('HAY LÀ NINEVEH?','MỘT HƯỚNG NGHIÊN CỨU KHÁC',size=38)
   st.text('Sơ đồ vị trí tương đối · không theo tỷ lệ',x=1005,y=599,w=450,h=28,size=14,color='#f1e4c2')
  elif i==5:
   st.background('evidence_table.png',1.04,1.11,x0=640,x1=653,y0=360,y1=353)
   st.shade();st.title('NHẦM TÊN HAI THÀNH PHỐ?','CÂU HỎI TỪ NHỮNG NGUỒN TƯ LIỆU',end=marks[-1],size=35)
   st.title('GIẢ THUYẾT · CHƯA PHẢI KẾT LUẬN',t=marks[-1],size=31)
   st.text('Bảng đất và phù điêu minh họa',x=1060,y=598,w=380,h=25,size=13,color='#e5e4cc')
  else:
   st.background('garden_wide.png',1.04,1.11,x0=640,x1=627,y0=360,y1=370)
   st.foreground()
   st.shade();st.title('MỘT NGỌN NÚI XANH · MỘT BÍ ẨN','VƯỜN TREO BABYLON',end=marks[-1],size=33)
   st.title('VẪN ĐANG TÌM LỜI GIẢI',t=marks[-1],size=40)
   st.text('Minh họa giả định',x=1112,y=598,w=260,h=24,size=13,color='#e5e4cc')
   # End on the image and central question, without a random decorative outro.
   last=st.add(item('shape','Final fade',640,360,1400,800,shape='card',fill='#10282c',color='#10282c',stroke=0),layer=100)
   st.key(last,'opacity',[(0,0),(L-.55,0),(L,.9)])
  # Long sentences split at natural punctuation; measured sentence timing is preserved.
  for cue in phrases:
   text=cue['text'];chunks=[]
   if len(text)>120 and ', ' in text:
    pieces=text.split(', ');mid=max(1,len(pieces)//2)
    chunks=[', '.join(pieces[:mid])+',',', '.join(pieces[mid:])]
   else:chunks=[text]
   cursor=cue['start'];weight=sum(len(x.split()) for x in chunks)
   for chunk in chunks:
    end=cursor+(cue['end']-cue['start'])*len(chunk.split())/weight
    p['subtitles'].append(dict(id=uid(),start=cursor,end=end,text=chunk,role='Narrator',scene_id=s['id']));cursor=end
  shots.append(dict(scene=i+1,start=a,end=b,name=s['name'],purpose=STORY[i]['purpose'],narration=STORY[i]['text']))
 p['audio']=[dict(id='voice',name='Hải Đăng · VieNeu-TTS',file=str(DEST/'narration.wav'),start=0,duration=60,group='voice',volume=1),dict(id='music',name='Nhạc nền nguyên bản',file=str(DEST/'music_original.wav'),start=0,duration=60,group='music',volume=.48,fade_in=1.5,fade_out=2)]
 for j in [0,1,2,6]:
  s=p['scenes'][j];p['audio'].append(dict(id='water_'+str(j),name='Nước nền tổng hợp',file=str(DEST/'water_original.wav'),start=s['start'],duration=min(12,s['duration']),group='sfx',volume=.32,fade_in=.5,fade_out=.6))
 for j in [2,3,4,5]:p['audio'].append(dict(id='transition_'+str(j),name='Chuyển cảnh nhẹ',file=str(DEST/'transition_original.wav'),start=p['scenes'][j]['start'],duration=.38,group='sfx',volume=.4))
 assert not preflight(p,DEST),preflight(p,DEST)
 saved=save(p,DEST/'project.json',DEST);write_srt(p['subtitles'],DEST/'phu_de.srt')
 (DEST/'shot_list.json').write_text(json.dumps(shots,ensure_ascii=False,indent=2),encoding='utf-8')
 (DEST/'sources.json').write_text(json.dumps(SOURCES,ensure_ascii=False,indent=2),encoding='utf-8')
 (DEST/'kich_ban.txt').write_text('\n\n'.join(row['text'] for row in STORY),encoding='utf-8')
 print(f'PROJECT READY: {len(p["scenes"])} scenes, {sum(len(s["objects"]) for s in p["scenes"])} layers.',flush=True)
 return saved

def preview(p):
 from PySide6.QtWidgets import QApplication
 from PySide6.QtGui import QImage,QPainter,QColor
 from studio.renderer import Renderer
 app=QApplication.instance() or QApplication([]);renderer=Renderer()
 sheet=QImage(1536,1728,QImage.Format.Format_RGB32);sheet.fill(QColor('#173137'));painter=QPainter(sheet)
 for i,s in enumerate(p['scenes']):
  frame=renderer.frame(p,DEST,s['start']+s['duration']*.65,1280,720)
  frame.save(str(DEST/'review'/f'scene_{i+1:02}.png'))
  painter.drawImage((i%2)*768,(i//2)*432,frame.scaled(768,432))
 painter.end();sheet.save(str(DEST/'review'/'storyboard.jpg'))
 print('PREVIEW READY',flush=True)
if __name__=='__main__':preview(build())
