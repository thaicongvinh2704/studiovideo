"""Export through the shipped Studio EXE and inspect the real delivered video."""
import hashlib,json,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
DEST=Path(__file__).resolve().parents[1]
from studio.exporter import binary,FLAGS
from studio.project import load,pack
from studio.directing import preflight


def export():
    exe=ROOT/'dist'/'StickmanAnimationStudio'/'StickmanAnimationStudio.exe'
    out=DEST/'Thu_phong_cach_hoat_hinh_lich_su_1080p.mp4';start=time.perf_counter()
    with (DEST/'review'/'export.log').open('wb') as log:
        subprocess.run([str(exe),str(DEST/'project.json'),'--render',str(out),'--resolution','1080p'],check=True,stdout=log,stderr=log,creationflags=FLAGS)
    print('Studio EXE rendered clip in',round(time.perf_counter()-start,1),'seconds',flush=True)
    p=load(DEST/'project.json');assert not preflight(p,DEST)
    info=json.loads(subprocess.check_output([binary('ffprobe'),'-v','error','-show_format','-show_streams','-of','json',str(out)],creationflags=FLAGS))
    v=next(s for s in info['streams'] if s['codec_type']=='video');a=next(s for s in info['streams'] if s['codec_type']=='audio')
    assert (v['width'],v['height'],v['r_frame_rate'])==(1920,1080,'30/1')
    assert int(v['nb_frames'])==971 and abs(float(info['format']['duration'])-32.364)<.05
    subprocess.run([binary('ffmpeg'),'-v','error','-threads','2','-i',str(out),'-f','null','-'],capture_output=True,check=True,creationflags=FLAGS)
    from PIL import Image,ImageDraw
    sheet=Image.new('RGB',(1920,720),'white')
    for i,t in enumerate((2,6.5,11.4,18,25,30.4)):
        path=DEST/'review'/f'decoded_{i+1}.png'
        subprocess.run([binary('ffmpeg'),'-y','-v','error','-ss',str(t),'-i',str(out),'-frames:v','1',str(path)],check=True,capture_output=True,creationflags=FLAGS)
        im=Image.open(path).convert('RGB');im.thumbnail((640,360));sheet.paste(im,((i%3)*640,(i//3)*360))
    sheet.save(DEST/'review'/'MP4_contact_sheet.jpg')
    subprocess.run([str(exe),str(DEST/'project.json'),'--screenshot',str(DEST/'review'/'Studio_sample.png')],check=True,creationflags=FLAGS,timeout=60)
    pack(p,DEST,DEST/'Du_an_clip_thu.zip')
    report=dict(status='PASS',exported_with='Installed Studio EXE',seconds=float(info['format']['duration']),frames=v['nb_frames'],width=v['width'],height=v['height'],fps=v['r_frame_rate'],video_codec=v['codec_name'],audio_codec=a['codec_name'],audio_channels=a['channels'],decode='PASS',frozen_project_open='PASS',scenes=len(p['scenes']),editable_layers=sum(len(s['objects']) for s in p['scenes']),subtitles=len(p['subtitles']),sha256=hashlib.sha256(out.read_bytes()).hexdigest(),style_approval='Pending user review')
    (DEST/'review'/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=True,indent=2),flush=True)


if __name__=='__main__':export()
