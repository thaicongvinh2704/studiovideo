"""Export and inspect the encoded film, including key moments of its visual argument."""
import sys, json, subprocess, time, zipfile
from revision2_story import DEST, ROOT, ORIGINAL
sys.path.insert(0,str(ROOT))
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QImage, QPainter, QColor
from studio.project import load, pack
from studio.exporter import export_video

FLAGS=getattr(subprocess,'CREATE_NO_WINDOW',0)
app=QApplication.instance() or QApplication([])

def run():
    p=load(DEST/'project.json')
    out=DEST/'Angkor_Wat_Ban_do_co_the_buoc_vao_1080p.mp4'
    tick=time.perf_counter()
    def progress(n,total):
        if n%300==0 or n==total:
            print(f'RENDER {n}/{total} · {time.perf_counter()-tick:.1f}s',flush=True)
    export_video(p,DEST,out,1920,1080,30,progress=progress)
    data=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(out)],creationflags=FLAGS))
    video=next(s for s in data['streams'] if s['codec_type']=='video')
    audio=next(s for s in data['streams'] if s['codec_type']=='audio')
    assert (video['width'],video['height'],video['r_frame_rate'],int(video['nb_frames']))==(1920,1080,'30/1',1800)
    assert abs(float(data['format']['duration'])-60)<.05
    subprocess.run(['ffmpeg','-v','error','-i',str(out),'-f','null','-'],capture_output=True,check=True,creationflags=FLAGS)
    times=[1.7,8.8,16.2,19.2,23.4,28.4,32.5,38.6,46.9,57.2]
    sheet=QImage(1536,2160,QImage.Format.Format_RGB32);sheet.fill(QColor('white'));painter=QPainter(sheet)
    for i,ts in enumerate(times):
        image=DEST/'review'/f'decoded_{i:02}.png'
        subprocess.run(['ffmpeg','-y','-v','error','-ss',str(ts),'-i',str(out),'-frames:v','1',str(image)],capture_output=True,check=True,creationflags=FLAGS)
        painter.drawImage((i%2)*768,(i//2)*432,QImage(str(image)).scaled(768,432))
    painter.end();sheet.save(str(DEST/'review'/'MP4_contact_sheet.jpg'))
    archive=DEST/'Du_an_Angkor_Wat_Ban_2.zip'
    pack(p,DEST,archive)
    with zipfile.ZipFile(archive,'a',zipfile.ZIP_DEFLATED) as z:
        for name in ['kich_ban.txt','phu_de.srt','shot_list.json','voice_timing.json','sources.json','DAO_DIEN.md']:
            z.write(DEST/name,name)
        for src in (ORIGINAL/'source').glob('revision2_*.py'):
            z.write(src,'source/'+src.name)
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
    report=dict(status='PASS',video=out.name,seconds=float(data['format']['duration']),width=video['width'],height=video['height'],fps=video['r_frame_rate'],frames=int(video['nb_frames']),full_decode='PASS',archive='PASS',scenes=len(p['scenes']),presenter_layers=0,voice='Hải Đăng · VieNeu-TTS v3 Turbo',review_timestamps=times,render_seconds=round(time.perf_counter()-tick,2),art_approval='Not assumed')
    (DEST/'review'/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2),flush=True)

if __name__=='__main__':
    run()
