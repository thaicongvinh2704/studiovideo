"""Generate a real Vietnamese repo voice, then fit complete cues to one minute."""
import os, sys, json, subprocess, wave, hashlib
from pathlib import Path
from story import DEST, ROOT, STORY
os.environ['HF_HOME']=str(DEST/'.models'/'huggingface')
os.environ['XDG_CACHE_HOME']=str(DEST/'.models'/'cache')
os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING']='1'
os.environ['HF_HUB_DISABLE_XET']='1'
os.environ['PYTHONIOENCODING']='utf-8'
import numpy as np
import soundfile as sf
from vieneu import Vieneu

FLAGS=getattr(subprocess,'CREATE_NO_WINDOW',0)
VOICE='Hải Đăng'
def ff(args,**kwargs):
    return subprocess.run(['ffmpeg','-hide_banner','-loglevel','error',*args],check=True,creationflags=FLAGS,**kwargs)

def run():
    print('Loading official VieNeu-TTS v3 Turbo, CPU fp32...',flush=True)
    tts=Vieneu(mode='v3turbo',device='cpu',backend='onnx',precision='fp32',threads=4)
    voices=tts.list_preset_voices()
    (DEST/'voice'/'available_voices.json').write_text(json.dumps(voices,ensure_ascii=False,indent=2),encoding='utf-8')
    assert any(v==VOICE for _,v in voices),voices
    lengths=[]
    for i,row in enumerate(STORY):
        text=row.get('spoken',row['text']);path=DEST/'voice'/f'raw_{i:02}.wav'
        digest=hashlib.sha256((text+'|v3turbo|'+VOICE).encode()).hexdigest();mark=path.with_suffix('.sha256')
        if not path.exists() or not mark.exists() or mark.read_text()!=digest:
            np.random.seed(51+i)
            audio=tts.infer(text,voice=VOICE,temperature=.6,top_k=25,max_chars=180)
            tts.save(audio,str(path));mark.write_text(digest)
        clean=DEST/'voice'/f'clean_{i:02}.wav'
        ff(['-y','-i',str(path),'-af','silenceremove=start_periods=1:start_duration=0.015:start_threshold=-48dB,areverse,silenceremove=start_periods=1:start_duration=0.015:start_threshold=-48dB,areverse','-ar','48000','-ac','1',str(clean)])
        with wave.open(str(clean)) as w:seconds=w.getnframes()/w.getframerate()
        lengths.append(seconds);print(f'VOICE {i+1}/8: {seconds:.2f} seconds',flush=True)
    # Preserve every word. A single tempo ratio retains the same voice and cadence.
    gap=.25;lead=.2;tail=.55;available=60-lead-tail-gap*(len(STORY)-1)
    ratio=sum(lengths)/available
    print(f'Unretimed speech {sum(lengths):.2f}s; global atempo={ratio:.3f}',flush=True)
    track=np.zeros(60*48000,dtype=np.float32);cursor=lead;cues=[]
    for i,(row,source_len) in enumerate(zip(STORY,lengths)):
        dest=DEST/'voice'/f'cue_{i:02}.wav'
        ff(['-y','-i',str(DEST/'voice'/f'clean_{i:02}.wav'),'-af',f'atempo={ratio:.9f}','-ar','48000','-ac','1','-c:a','pcm_s16le',str(dest)])
        audio,rate=sf.read(dest,dtype='float32');a=round(cursor*rate);b=a+len(audio)
        if b>len(track):raise RuntimeError('Narration overflows final clock')
        track[a:b]+=audio
        cues.append(dict(index=i,start=round(cursor,6),end=round(b/rate,6),text=row['text'],raw_seconds=source_len,tempo=ratio))
        cursor=b/rate+gap
    unmastered=DEST/'voice'/'narration_unmastered.wav';sf.write(unmastered,track,48000,subtype='PCM_16')
    ff(['-y','-i',str(unmastered),'-af','loudnorm=I=-17:TP=-2:LRA=7','-ar','48000','-ac','2','-c:a','pcm_s16le',str(DEST/'narration.wav')])
    report=dict(engine='VieNeu-TTS v3 Turbo 3.8.3',model='pnnbao-ump/VieNeu-TTS-v3-Turbo',voice=VOICE,requested_name='Nguyễn Việt Cường',requested_name_found=False,clarification='User requested a Vietnamese repo voice; no verified preset for the originally requested name was found.',repo='https://github.com/pnnbao97/VieNeu-TTS',length=60,rate=48000,cues=cues)
    (DEST/'voice_timing.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print('NARRATION READY: 60 seconds, actual voice '+VOICE,flush=True)
if __name__=='__main__':run()
