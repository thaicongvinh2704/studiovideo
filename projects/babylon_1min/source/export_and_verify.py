"""Render the actual MP4, decode it completely and inspect delivery artifacts."""
import sys,json,subprocess,time,zipfile,hashlib
from pathlib import Path
from story import ROOT,DEST
sys.path.insert(0,str(ROOT))
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QImage,QPainter,QColor
from studio.project import load,pack
from studio.exporter import export_video
FLAGS=getattr(subprocess,'CREATE_NO_WINDOW',0)
APP=QApplication.instance() or QApplication([])

def run():
 p=load(DEST/'project.json');out=DEST/'Vuon_Treo_Babylon_1080p.mp4';tick=time.perf_counter()
 def progress(n,total):
  if n%300==0 or n==total:print(f'RENDER {n}/{total}: {time.perf_counter()-tick:.1f}s',flush=True)
 export_video(p,DEST,out,1920,1080,30,progress=progress)
 data=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(out)],creationflags=FLAGS))
 video=next(x for x in data['streams'] if x['codec_type']=='video');audio=next(x for x in data['streams'] if x['codec_type']=='audio')
 assert(video['width'],video['height'],video['r_frame_rate'],int(video['nb_frames']))==(1920,1080,'30/1',1800)
 assert abs(float(data['format']['duration'])-60)<.05
 assert audio['channels']==2 and audio['sample_rate']=='48000'
 subprocess.run(['ffmpeg','-v','error','-i',str(out),'-f','null','-'],capture_output=True,check=True,creationflags=FLAGS)
 sheet=QImage(1536,1728,QImage.Format.Format_RGB32);sheet.fill(QColor('#173137'));painter=QPainter(sheet)
 times=[]
 for i,s in enumerate(p['scenes']):
  ts=s['start']+s['duration']*.68;times.append(ts);img=DEST/'review'/f'decoded_{i:02}.png'
  subprocess.run(['ffmpeg','-y','-v','error','-ss',str(ts),'-i',str(out),'-frames:v','1',str(img)],capture_output=True,check=True,creationflags=FLAGS)
  painter.drawImage((i%2)*768,(i//2)*432,QImage(str(img)).scaled(768,432))
 painter.end();sheet.save(str(DEST/'review'/'MP4_contact_sheet.jpg'))
 # Inspect encoded frames around independent foliage and the water route animation.
 motion=[]
 for j,ts in enumerate([1.0,2.1,4.2,p['scenes'][2]['start']+1,p['scenes'][2]['start']+3.2]):
  img=DEST/'review'/f'motion_{j:02}.png'
  subprocess.run(['ffmpeg','-y','-v','error','-ss',str(ts),'-i',str(out),'-frames:v','1',str(img)],capture_output=True,check=True,creationflags=FLAGS)
  motion.append(hashlib.sha256(img.read_bytes()).hexdigest())
 assert len(set(motion))==len(motion)
 archive=DEST/'Du_an_Vuon_Treo_Babylon.zip';pack(p,DEST,archive)
 with zipfile.ZipFile(archive,'a',zipfile.ZIP_DEFLATED) as z:
  for name in ['kich_ban.txt','phu_de.srt','shot_list.json','voice_timing.json','sources.json','GHI_CHU.md']:
   z.write(DEST/name,name)
  z.write(DEST/'art'/'prompts.json','art/prompts.json')
  for path in (DEST/'source').glob('*.py'):z.write(path,'source/'+path.name)
 with zipfile.ZipFile(archive) as z:assert z.testzip() is None
 report=dict(status='PASS',video=out.name,seconds=float(data['format']['duration']),width=1920,height=1080,fps=30,frames=1800,video_codec=video['codec_name'],audio_codec=audio['codec_name'],full_decode='PASS',distinct_motion_frames='PASS',archive='PASS',scenes=len(p['scenes']),layers=sum(len(s['objects']) for s in p['scenes']),voice='Hải Đăng · VieNeu-TTS v3 Turbo',art='AI-generated raster comic backgrounds with authored SVG overlays and Studio animation; not frame-by-frame character animation',review_timestamps=times,render_seconds=round(time.perf_counter()-tick,2),user_art_approval='Not assumed')
 (DEST/'review'/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 (DEST/'review'/'ffprobe.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps(report,ensure_ascii=False,indent=2),flush=True)
if __name__=='__main__':run()
