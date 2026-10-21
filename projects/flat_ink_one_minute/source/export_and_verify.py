"""Render in shipped Studio and verify the delivered MP4, not just project state."""
import hashlib,json,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
DEST=Path(__file__).resolve().parents[1]
from studio.exporter import binary,FLAGS
from studio.project import load,pack
from studio.directing import preflight
from studio.subtitles import read

def export():
    exe=ROOT/'dist'/'StickmanAnimationStudio'/'StickmanAnimationStudio.exe'
    out=DEST/'Mot_phut_nguoi_Viet_co_net_muc_1080p.mp4';start=time.perf_counter()
    with (DEST/'review'/'export.log').open('wb') as log:
        subprocess.run([str(exe),str(DEST/'project.json'),'--render',str(out),'--resolution','1080p'],check=True,stdout=log,stderr=log,creationflags=FLAGS)
    print('Studio EXE rendered clip in',round(time.perf_counter()-start,1),'seconds',flush=True)
    p=load(DEST/'project.json');assert not preflight(p,DEST)
    info=json.loads(subprocess.check_output([binary('ffprobe'),'-v','error','-show_format','-show_streams','-of','json',str(out)],creationflags=FLAGS))
    v=next(s for s in info['streams'] if s['codec_type']=='video');a=next(s for s in info['streams'] if s['codec_type']=='audio')
    assert (v['width'],v['height'],v['r_frame_rate'])==(1920,1080,'30/1')
    assert int(v['nb_frames'])==1800 and abs(float(info['format']['duration'])-60)<.05
    assert a['channels']==2 and int(a['sample_rate'])==48000
    original=read(ROOT/'projects'/'nguoi_viet_co_5phut'/'source'/'kich_ban_goc.srt')[:13]
    assert [c['text'] for c in p['subtitles']]==[c['text'] for c in original]
    source_hash=hashlib.sha256((DEST/'art'/'presenter_master.png').read_bytes()).hexdigest()
    assert source_hash=='85b814d6ad7e6d6e3076b80cf136469b98a2733ab02ef1c00964188b86217c15'
    subprocess.run([binary('ffmpeg'),'-v','error','-threads','2','-i',str(out),'-f','null','-'],capture_output=True,check=True,creationflags=FLAGS)
    from PIL import Image,ImageDraw
    sheet=Image.new('RGB',(1920,1080),'white');draw=ImageDraw.Draw(sheet)
    for i,t in enumerate((2,7,11,20,29,34,43,53,58)):
        path=DEST/'review'/f'decoded_{t}.png'
        subprocess.run([binary('ffmpeg'),'-y','-v','error','-ss',str(t),'-i',str(out),'-frames:v','1',str(path)],check=True,capture_output=True,creationflags=FLAGS)
        im=Image.open(path).convert('RGB');im.thumbnail((640,360));sheet.paste(im,((i%3)*640,(i//3)*360))
        draw.text(((i%3)*640+8,(i//3)*360+8),f'{t}s',fill='#dd2222')
    sheet.save(DEST/'review'/'MP4_contact_sheet.jpg')
    subprocess.run([str(exe),str(DEST/'project.json'),'--screenshot',str(DEST/'review'/'Studio_project.png')],check=True,creationflags=FLAGS,timeout=60)
    pack(p,DEST,DEST/'Du_an_1_phut.zip')
    report=dict(technical_status='PASS',exported_with='Shipped Studio EXE',seconds=float(info['format']['duration']),frames=int(v['nb_frames']),width=v['width'],height=v['height'],fps=v['r_frame_rate'],video_codec=v['codec_name'],audio_codec=a['codec_name'],audio_channels=a['channels'],audio_rate=int(a['sample_rate']),decode='PASS',frozen_project_open='PASS',scenes=len(p['scenes']),editable_layers=sum(len(s['objects']) for s in p['scenes']),subtitles=len(p['subtitles']),source_subtitle_texts='13 complete cues unchanged, uniformly retimed',presenter_sha256=source_hash,presenter_motion='Original fixed pointing pose; no new animation rig',sha256=hashlib.sha256(out.read_bytes()).hexdigest(),style_approval='Pending user review')
    (DEST/'review'/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=True,indent=2),flush=True)

if __name__=='__main__':export()
