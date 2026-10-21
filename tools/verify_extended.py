import sys
import copy
import json
import math
import wave
import array
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from PySide6.QtWidgets import QApplication
from studio.demo import demo
from studio.project import new_project,resequence
from studio.exporter import export_video,export_cached,mix_audio

def main():
    app=QApplication([]);root=Path(__file__).resolve().parents[1];out=root/'outputs';report={}
    p=new_project(duration=1);p['scenes'][0]['objects'][0]['end']=1
    for w,h,fps,length in [(1280,720,24,1),(1920,1080,30,.5),(480,854,12,1)]:
        output=out/f'export_{w}x{h}_{fps}fps.mp4'
        export_video(p,root,output,w,h,fps,length=length)
        report[output.name]='PASS (ffprobe validated by exporter)';print('PASS',output.name,flush=True)
    p=demo();p['scenes']=p['scenes'][:2];p['subtitles']=[]
    for s in p['scenes']:
        s['duration']=1
        for o in s['objects']:o['end']=1
    resequence(p)
    output=out/'cached_scene_test.mp4';export_cached(p,root,output,320,180,12)
    cache=out/'cached_scene_test_scenes';before=[(cache/f'scene_{i:04}.mp4').stat().st_mtime_ns for i in (1,2)]
    export_cached(p,root,output,320,180,12)
    after=[(cache/f'scene_{i:04}.mp4').stat().st_mtime_ns for i in (1,2)]
    assert before==after
    report['scene_cache_resume']='PASS (2 scenes concatenated; retry reused both cached MP4 files)';print('PASS scene cache resume',flush=True)
    tone=out/'generated_tone.wav'
    samples=array.array('h',(round(7000*math.sin(math.tau*440*i/22050)) for i in range(22050*4)))
    with wave.open(str(tone),'wb') as wav:
        wav.setnchannels(1);wav.setsampwidth(2);wav.setframerate(22050);wav.writeframes(samples.tobytes())
    p=new_project(duration=4);p['audio']=[
        dict(id='v',file=str(out/'voice_test.wav'),group='voice',start=.5,duration=1.4,volume=.8,trim=0,fade_in=0,fade_out=0),
        dict(id='m',file=str(tone),group='music',start=0,duration=4,volume=.7,trim=0,fade_in=.15,fade_out=.2),
        dict(id='s',file=str(tone),group='sfx',start=2.5,duration=.5,volume=.2,trim=.1,fade_in=.1,fade_out=.1)]
    mixed=out/'mixer_duck.wav';mix_audio(p,root,mixed)
    p['duck_music']=False;plain=out/'mixer_plain.wav';mix_audio(p,root,plain)
    assert mixed.read_bytes()!=plain.read_bytes()
    with wave.open(str(mixed),'rb') as wav:
        assert wav.getnchannels()==1 and abs(wav.getnframes()/wav.getframerate()-4)<.01
    report['audio_mixer']='PASS (voice + music + SFX; trim/fades/delay; ducking changes output; 4 seconds validated)'
    print('PASS audio mixer',flush=True)
    (out/'extended_verification.json').write_text(json.dumps(report,indent=2))

if __name__=='__main__':main()
