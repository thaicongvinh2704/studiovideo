"""Sentence-level narration timings for a deliberate visual argument."""
import os, re, json, hashlib, subprocess, wave
from revision2_story import ORIGINAL, DEST, STORY
os.environ['HF_HOME'] = str(ORIGINAL / '.models' / 'huggingface')
os.environ['XDG_CACHE_HOME'] = str(ORIGINAL / '.models' / 'cache')
os.environ['HF_HUB_DISABLE_XET'] = '1'
os.environ['HF_HUB_OFFLINE'] = '1'
os.environ['PYTHONIOENCODING'] = 'utf-8'
import numpy as np
import soundfile as sf
from vieneu import Vieneu

FLAGS = getattr(subprocess, 'CREATE_NO_WINDOW', 0)

def ff(args):
    subprocess.run(['ffmpeg','-v','error',*args], check=True, creationflags=FLAGS)

def run():
    voice_dir = DEST / 'voice'
    voice_dir.mkdir(parents=True, exist_ok=True)
    (DEST / 'review').mkdir(exist_ok=True)
    tts = Vieneu(mode='v3turbo',device='cpu',backend='onnx',precision='fp32',threads=4)
    phrases = []
    for scene, row in enumerate(STORY):
        for sentence in re.split(r'(?<=[.!?])\s+', row['text']):
            spoken = sentence.replace('Angkor Wat','Ăng co Vát').replace('Vishnu','Vi snu').replace('Meru','Mê ru').replace('Khmer','Khơ me')
            i = len(phrases)
            raw = voice_dir / f'phrase_{i:02}_raw.wav'
            digest = hashlib.sha256((spoken+'|HaiDang|v3turbo').encode()).hexdigest()
            marker = raw.with_suffix('.sha256')
            if not raw.exists() or not marker.exists() or marker.read_text() != digest:
                np.random.seed(95+i)
                audio = tts.infer(spoken,voice='Hải Đăng',temperature=.55,top_k=25,max_chars=180)
                tts.save(audio,str(raw))
                marker.write_text(digest)
            clean = voice_dir / f'phrase_{i:02}_clean.wav'
            ff(['-y','-i',str(raw),'-af','silenceremove=start_periods=1:start_duration=0.015:start_threshold=-48dB,areverse,silenceremove=start_periods=1:start_duration=0.015:start_threshold=-48dB,areverse','-ar','48000','-ac','1',str(clean)])
            with wave.open(str(clean)) as w:
                length = w.getnframes()/w.getframerate()
            phrases.append(dict(scene=scene,text=sentence,length=length,file=clean))
            print(f'VOICE {i+1}: {length:.2f}s',flush=True)
    lead, tail = .25, .8
    gaps = [.32 if b['scene'] != a['scene'] else .18 for a,b in zip(phrases,phrases[1:])] + [0]
    tempo = sum(p['length'] for p in phrases)/(60-lead-tail-sum(gaps))
    print(f'Speech tempo: {tempo:.3f}',flush=True)
    track = np.zeros(60*48000,dtype=np.float32)
    cursor, cues = lead, []
    for i,(phrase,gap) in enumerate(zip(phrases,gaps)):
        fitted = voice_dir / f'phrase_{i:02}.wav'
        ff(['-y','-i',str(phrase['file']),'-af',f'atempo={tempo:.9f}','-ar','48000','-ac','1',str(fitted)])
        samples,sr = sf.read(fitted,dtype='float32')
        a = round(cursor*sr)
        b = a+len(samples)
        assert b <= len(track)
        track[a:b] = samples
        cues.append(dict(scene=phrase['scene'],text=phrase['text'],start=a/sr,end=b/sr))
        cursor = b/sr+gap
    sf.write(voice_dir/'narration_unmastered.wav',track,48000,subtype='PCM_16')
    ff(['-y','-i',str(voice_dir/'narration_unmastered.wav'),'-af','loudnorm=I=-17:TP=-2:LRA=7','-ar','48000','-ac','2',str(DEST/'narration.wav')])
    report = dict(voice='Hải Đăng',engine='VieNeu-TTS v3 Turbo',repo='https://github.com/pnnbao97/VieNeu-TTS',requested_voice_confirmed=False,tempo=tempo,cues=cues)
    (DEST/'voice_timing.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print('NARRATION READY',flush=True)

if __name__ == '__main__':
    run()
