"""Validate the delivered MP4, audio continuity and actual decoded motion samples."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from PySide6.QtGui import QGuiApplication
from studio.exporter import binary,validate_output
from studio.project import duration,missing
from studio.character_qc import project_issues

BASE=ROOT/'projects/mo_den_maya/director_v2'
VIDEO=BASE/'Mo_Den_Maya_Dao_Dien_V2_1080p.mp4'


def pcm(path,start,length=2):
    raw=subprocess.check_output([binary('ffmpeg'),'-v','error','-ss',str(start),'-i',str(path),
                                 '-t',str(length),'-vn','-ac','1','-ar','48000','-f','s16le','pipe:1'])
    return np.frombuffer(raw,dtype='<i2').astype(np.float64)


def main():
    app=QGuiApplication(sys.argv[:1])
    p=json.loads((BASE/'project.json').read_text(encoding='utf-8'))
    report=dict(missing=missing(p,BASE),character_qc=project_issues(p,BASE),
                duration_seconds=duration(p),shots=len(p['scenes']))
    assert not report['missing'] and not report['character_qc']
    for a,b in zip(p['scenes'],p['scenes'][1:]):
        assert abs(a['start']+a['duration']-b['start'])<1e-7
    validate_output(VIDEO,1920,1080,24,duration(p))
    probe=json.loads(subprocess.check_output([binary('ffprobe'),'-v','error','-show_format','-show_streams','-of','json',str(VIDEO)]))
    video=next(s for s in probe['streams'] if s['codec_type']=='video')
    audio=next(s for s in probe['streams'] if s['codec_type']=='audio')
    report['av_start_delta_ms']=round(1000*(float(video.get('start_time',0))-float(audio.get('start_time',0))),4)
    assert abs(report['av_start_delta_ms'])<2
    (BASE/'final_ffprobe.json').write_text(json.dumps(probe,indent=2),encoding='utf-8')
    subprocess.run([binary('ffmpeg'),'-v','error','-i',str(VIDEO),'-f','null','-'],check=True)
    report['full_decode']='PASS'
    report['mp4_structure']='PASS'
    report['audio_identity_samples']=[]
    voice=BASE/p['audio'][0]['file']
    for t in [5,60,201,421,691,827]:
        a=pcm(voice,t);b=pcm(VIDEO,t)
        n=min(len(a),len(b));a=a[:n]-a[:n].mean();b=b[:n]-b[:n].mean()
        # Sample the middle to avoid cut-window/AAC edge effects, and compare
        # waveform identity independently of mono/stereo gain conversion.
        correlations=[]
        for lag in range(-960,961,24):
            aa=a[1200:n-1200:4];bb=b[1200+lag:n-1200+lag:4]
            correlations.append((float(np.dot(aa,bb)/max(1e-12,np.linalg.norm(aa)*np.linalg.norm(bb))),lag))
        corr,lag=max(correlations)
        report['audio_identity_samples'].append(dict(seconds=t,correlation=round(corr,5),offset_ms=lag/48))
        assert corr>.85, (t,corr,lag)
    folder=BASE/'review/decoded';folder.mkdir(exist_ok=True)
    samples=[(1,.3),(10,.2),(12,.2),(41,.3),(63,.2),(70,.2),(86,.2),(109,.2),(111,.2),(183,.2),(208,.2)]
    font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',18)
    for number,offset in samples:
        s=p['scenes'][number-1];max_delta=max(.1,s['duration']-.4)
        times=[s['start']+min(v,max_delta) for v in [.1,.5,max(.8,s['duration']*.6)]]
        frames=[]
        for j,t in enumerate(times):
            path=folder/f'shot_{number:03d}_{j}.jpg'
            subprocess.run([binary('ffmpeg'),'-v','error','-y','-ss',str(t),'-i',str(VIDEO),'-frames:v','1','-vf','scale=640:360',str(path)],check=True)
            frames.append(Image.open(path).convert('RGB'))
        board=Image.new('RGB',(1920,400),'#ede7de');draw=ImageDraw.Draw(board)
        for j,im in enumerate(frames):
            board.paste(im,(j*640,0));draw.text((j*640+10,370),f'Shot {number:03d} · {times[j]:.2f}s',fill='#30241f',font=font)
        board.save(folder/f'motion_{number:03d}.jpg',quality=93)
    report['motion_samples']='Decoded MP4 strips rendered for visual review; not an automatic aesthetic pass.'
    report['caption_timing']='Phrase estimates within semantic synthesis units; not word-level alignment.'
    report['listening_qc']='Not newly certified; preserved user-selected full H track.'
    report['video_sha256']=hashlib.sha256(VIDEO.read_bytes()).hexdigest()
    (BASE/'delivery_verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2),flush=True)


if __name__=='__main__':main()
