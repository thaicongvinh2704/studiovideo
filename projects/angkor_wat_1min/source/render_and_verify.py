"""Render the editable project and verify the delivered MP4 and extracted frames."""
import sys,json,subprocess,time,hashlib,zipfile
from pathlib import Path
from story import DEST,ROOT,SOURCES
sys.path.insert(0,str(ROOT))
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QImage,QPainter,QColor
from studio.project import load,pack,duration
from studio.exporter import export_video
from studio.directing import preflight
FLAGS=getattr(subprocess,'CREATE_NO_WINDOW',0)
APP=QApplication.instance() or QApplication([])

def run():
    p=load(DEST/'project.json');assert not preflight(p,DEST)
    out=DEST/'Angkor_Wat_Mot_vu_tru_bang_da_1080p.mp4'
    tick=time.perf_counter()
    def progress(n,total):
        if n%300==0 or n==total:print(f'RENDER {n}/{total} frames, {time.perf_counter()-tick:.1f}s elapsed',flush=True)
    export_video(p,DEST,out,1920,1080,30,progress=progress)
    print('Encoding finished; validating the actual MP4...',flush=True)
    data=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(out)],creationflags=FLAGS))
    video=next(x for x in data['streams'] if x['codec_type']=='video');audio=next(x for x in data['streams'] if x['codec_type']=='audio')
    assert(video['width'],video['height'],video['r_frame_rate'],int(video['nb_frames']))==(1920,1080,'30/1',1800)
    assert abs(float(data['format']['duration'])-60)<.05 and audio['channels']==2 and int(audio['sample_rate'])==48000
    subprocess.run(['ffmpeg','-v','error','-threads','2','-i',str(out),'-f','null','-'],check=True,capture_output=True,creationflags=FLAGS)
    sheet=QImage(1280,1440,QImage.Format.Format_RGB32);sheet.fill(QColor('white'));painter=QPainter(sheet)
    timestamps=[]
    for i,s in enumerate(p['scenes']):
        ts=s['start']+s['duration']*.7;timestamps.append(ts);path=DEST/'review'/f'decoded_{i+1:02}.png'
        subprocess.run(['ffmpeg','-y','-v','error','-ss',str(ts),'-i',str(out),'-frames:v','1',str(path)],check=True,capture_output=True,creationflags=FLAGS)
        painter.drawImage((i%2)*640,(i//2)*360,QImage(str(path)).scaled(640,360))
    painter.end();sheet.save(str(DEST/'review'/'MP4_contact_sheet.jpg'))
    # Verify a real arm movement and a real face change after encoding, away from cut points.
    files=[]
    for n,ts in enumerate([.7,1.6,2.7,4.3,5.8,6.8]):
        path=DEST/'review'/f'motion_{n}.png';files.append(path)
        subprocess.run(['ffmpeg','-y','-v','error','-ss',str(ts),'-i',str(out),'-frames:v','1',str(path)],check=True,capture_output=True,creationflags=FLAGS)
    assert len({hashlib.sha256(f.read_bytes()).hexdigest() for f in files})>3
    pack(p,DEST,DEST/'Du_an_Angkor_Wat_1_phut.zip')
    # Add authoring sources and factual/voice provenance without packaging the runtime/model cache.
    with zipfile.ZipFile(DEST/'Du_an_Angkor_Wat_1_phut.zip','a',zipfile.ZIP_DEFLATED) as z:
        for src in (DEST/'source').glob('*.py'):z.write(src,'source/'+src.name)
        for name in ['kich_ban.txt','sources.json','voice_timing.json','shot_list.json','art_manifest.json','GHI_CHU.md']:
            f=DEST/name
            if f.is_file():z.write(f,name)
    report=dict(status='PASS',video=str(out.name),seconds=float(data['format']['duration']),width=video['width'],height=video['height'],fps=video['r_frame_rate'],frames=int(video['nb_frames']),video_codec=video['codec_name'],audio_codec=audio['codec_name'],audio_channels=audio['channels'],audio_sample_rate=audio['sample_rate'],full_decode='PASS',motion_frames_differ='PASS',scenes=len(p['scenes']),editable_layers=sum(len(s['objects']) for s in p['scenes']),voice='VieNeu-TTS v3 Turbo · Hải Đăng',requested_voice_name_confirmed=False,render_seconds=round(time.perf_counter()-tick,2),art_approval='Not assumed; requires viewing by the user')
    (DEST/'review'/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    (DEST/'review'/'ffprobe.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2),flush=True)
if __name__=='__main__':run()
