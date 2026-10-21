"""Check this production's real MP4, exact SRT preservation and audio synchronization."""
import hashlib,json,subprocess,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
DEST=Path(__file__).resolve().parents[1]
from studio.project import load
from studio.subtitles import read
from studio.exporter import binary,FLAGS
from studio.directing import preflight


def run(args):return subprocess.check_output(args,stderr=subprocess.PIPE,creationflags=FLAGS)


def verify():
    output=DEST/'Mot_ngay_cung_nguoi_Viet_co_1080p.mp4';project=load(DEST/'project.json');source=read(DEST/'source'/'kich_ban_goc.srt')
    report=dict(status='PASS',checks={},visual_review='Source previews reviewed; decoded MP4 frames require final inspection')
    assert len(source)==len(project['subtitles'])==64
    for a,b in zip(source,project['subtitles']):
        assert a['text']==b['text'] and abs(a['start']-b['start'])<1e-6 and abs(a['end']-b['end'])<1e-6
    assert not preflight(project,DEST)
    report['checks']['original_srt']='64 cues, exact text and timestamps preserved'
    info=json.loads(run([binary('ffprobe'),'-v','error','-show_format','-show_streams','-of','json',str(output)]));v=next(s for s in info['streams'] if s['codec_type']=='video');a=next(s for s in info['streams'] if s['codec_type']=='audio')
    assert (v['width'],v['height'],v['r_frame_rate'],v['nb_frames'])==(1920,1080,'30/1','9000')
    assert abs(float(info['format']['duration'])-300)<.05 and a['channels']==2 and a['sample_rate']=='48000'
    report['checks']['media']=dict(width=v['width'],height=v['height'],fps=v['r_frame_rate'],frames=v['nb_frames'],duration=info['format']['duration'],video_codec=v['codec_name'],audio_codec=a['codec_name'],channels=a['channels'],sample_rate=a['sample_rate'],size_bytes=output.stat().st_size)
    run([binary('ffmpeg'),'-v','error','-threads','2','-i',str(output),'-f','null','-'])
    report['checks']['full_decode']='PASS'
    times=run([binary('ffprobe'),'-v','error','-select_streams','v:0','-show_entries','frame=best_effort_timestamp_time','-of','csv=p=0',str(output)]).decode().splitlines()
    pts=np.array([float(x.strip().strip(',')) for x in times if x.strip().strip(',')]);gaps=np.diff(pts)
    assert len(pts)==9000 and np.max(np.abs(gaps-1/30))<.00001
    report['checks']['frame_clock']=dict(frame_count=len(pts),max_gap_seconds=float(gaps.max()),min_gap_seconds=float(gaps.min()))
    def pcm(path):return np.frombuffer(run([binary('ffmpeg'),'-v','error','-i',str(path),'-vn','-ar','8000','-ac','1','-f','f32le','pipe:1']),dtype='<f4').astype(np.float64)
    original=pcm(DEST/'narration.wav');encoded=pcm(output);checks=[]
    timings=json.loads((DEST/'voice_timing.json').read_text(encoding='utf-8'))['cues']
    for i in (0,7,15,23,31,39,47,55,63):
        start=round((source[i]['start']+.15)*8000);length=round(min(2.8,timings[i]['speech_seconds']-.20)*8000)
        x=original[start:start+length];y=encoded[start:start+length];x=x-x.mean();y=y-y.mean()
        size=1<<((2*length-1).bit_length());corr=np.fft.irfft(np.fft.rfft(y,size)*np.conj(np.fft.rfft(x,size)),size)
        lags=np.arange(-400,401);best=int(lags[np.argmax(corr[lags%size])]);coefficient=float(np.dot(x,y)/max(1e-12,np.linalg.norm(x)*np.linalg.norm(y)))
        assert abs(best)<=80 and coefficient>.90,(i+1,best,coefficient)
        checks.append(dict(cue=i+1,lag_ms=best/8,correlation=round(coefficient,5)))
    report['checks']['narration_sync_samples']=checks
    loud=subprocess.run([binary('ffmpeg'),'-hide_banner','-i',str(output),'-vn','-af','volumedetect','-f','null','-'],capture_output=True,creationflags=FLAGS,check=True).stderr.decode('utf-8','replace')
    (DEST/'review'/'audio_levels.txt').write_text(loud,encoding='utf-8')
    report['checks']['sound_levels']=[line.split(']')[-1].strip() for line in loud.splitlines() if 'mean_volume:' in line or 'max_volume:' in line]
    report['sha256']=hashlib.sha256(output.read_bytes()).hexdigest()
    frames=DEST/'review'/'decoded';frames.mkdir(exist_ok=True)
    from PIL import Image,ImageDraw
    sheet=Image.new('RGB',(1920,1160),'#eae6df');d=ImageDraw.Draw(sheet)
    for i,t in enumerate((2,14,32,52,70,87,99,115,127,145,163,180,201,226,246,294)):
        path=frames/f'{t:03}.png';run([binary('ffmpeg'),'-y','-v','error','-ss',str(t),'-i',str(output),'-frames:v','1',str(path)])
        im=Image.open(path).convert('RGB');im.thumbnail((480,270));x=i%4*480;y=i//4*290;sheet.paste(im,(x,y+20));d.text((x+8,y+3),str(t)+'s',fill='black')
    sheet.save(DEST/'review'/'MP4_contact_sheet.jpg')
    exe=ROOT/'dist'/'StickmanAnimationStudio'/'StickmanAnimationStudio.exe'
    subprocess.run([str(exe),str(DEST/'project.json'),'--screenshot',str(DEST/'review'/'Studio_project.png')],check=True,creationflags=FLAGS,timeout=60)
    report['checks']['frozen_studio_project_open']='PASS'
    (DEST/'review'/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=True,indent=2),flush=True)


if __name__=='__main__':verify()
