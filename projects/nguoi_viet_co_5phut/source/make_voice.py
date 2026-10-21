"""Generate narration for the supplied SRT, preserving its exact five-minute clock."""
import array,hashlib,json,subprocess,sys,wave
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
DEST=Path(__file__).resolve().parents[1]
from studio.tts import VoiceEngine
from studio.subtitles import read
from studio.exporter import binary,FLAGS


def prepare():
    cues=read(DEST/'source'/'kich_ban_goc.srt');folder=DEST/'voice';folder.mkdir(exist_ok=True)
    engine=VoiceEngine(ROOT/'voices');voice=next(v for _,v in engine.voices() if v.endswith('.onnx'))
    rate=48000;track=array.array('h',[0])*round(cues[-1]['end']*rate);measurements=[]
    for i,cue in enumerate(cues):
        text=' '.join(cue['text'].split());raw=folder/f'raw_{i+1:02}.wav';mark=raw.with_suffix('.sha256')
        digest=hashlib.sha256((text+'|piper:.98').encode()).hexdigest()
        if not raw.exists() or not mark.exists() or mark.read_text()!=digest:
            engine.synthesize(text,voice,raw,speed=.98);mark.write_text(digest)
        clean=subprocess.check_output([binary('ffmpeg'),'-v','error','-i',str(raw),'-af','silenceremove=start_periods=1:start_duration=0.015:start_threshold=-48dB,areverse,silenceremove=start_periods=1:start_duration=0.015:start_threshold=-48dB,areverse','-ar',str(rate),'-ac','1','-f','s16le','pipe:1'],creationflags=FLAGS)
        seconds=len(clean)/2/rate;available=cue['end']-cue['start']-.24
        tempo=max(.87,seconds/available)
        fitted=subprocess.check_output([binary('ffmpeg'),'-v','error','-f','s16le','-ar',str(rate),'-ac','1','-i','pipe:0','-af',f'atempo={tempo:.9f},afade=t=in:d=0.008,afade=t=out:st={max(0,min(seconds/tempo,available)-.012):.9f}:d=0.012','-f','s16le','pipe:1'],input=clean,creationflags=FLAGS)
        samples=array.array('h');samples.frombytes(fitted)
        assert len(samples)<=round(available*rate)+960,'Cue overflows: '+str(i+1)
        first=round((cue['start']+.08)*rate);track[first:first+len(samples)]=samples
        dest=folder/f'cue_{i+1:02}.wav'
        with wave.open(str(dest),'wb') as wav:wav.setparams((1,2,rate,0,'NONE','not compressed'));wav.writeframes(samples.tobytes())
        measurements.append(dict(cue=i+1,start=cue['start'],end=cue['end'],text=text,source_seconds=seconds,tempo=tempo,speech_seconds=len(samples)/rate))
        print(f'Voice {i+1}/64, tempo {tempo:.3f}, speech {len(samples)/rate:.2f}s',flush=True)
    unmastered=folder/'narration_unmastered.wav'
    with wave.open(str(unmastered),'wb') as wav:wav.setparams((1,2,rate,0,'NONE','not compressed'));wav.writeframes(track.tobytes())
    subprocess.run([binary('ffmpeg'),'-y','-v','error','-i',str(unmastered),'-af','loudnorm=I=-17:TP=-2:LRA=7','-ar',str(rate),'-ac','2','-c:a','pcm_s16le',str(DEST/'narration.wav')],check=True,creationflags=FLAGS)
    (DEST/'voice_timing.json').write_text(json.dumps(dict(model=Path(voice).name,source='Piper CPU, generated from the supplied SRT',duration=300,cues=measurements),ensure_ascii=False,indent=2),encoding='utf-8')
    print('NARRATION READY',flush=True)


if __name__=='__main__':prepare()
