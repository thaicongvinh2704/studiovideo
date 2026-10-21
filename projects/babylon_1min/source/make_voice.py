"""Generate sentence cues with the already installed Vietnamese model."""
import os,re,json,hashlib,subprocess,wave
from story import DEST,ANGKOR,STORY
os.environ['HF_HOME']=str(ANGKOR/'.models'/'huggingface')
os.environ['XDG_CACHE_HOME']=str(ANGKOR/'.models'/'cache')
os.environ['HF_HUB_DISABLE_XET']='1'
os.environ['HF_HUB_OFFLINE']='1'
os.environ['PYTHONIOENCODING']='utf-8'
import numpy as np
import soundfile as sf
from vieneu import Vieneu
FLAGS=getattr(subprocess,'CREATE_NO_WINDOW',0)
def ff(args):subprocess.run(['ffmpeg','-v','error',*args],check=True,creationflags=FLAGS)
def run():
 folder=DEST/'voice';folder.mkdir(parents=True,exist_ok=True)
 (DEST/'review').mkdir(exist_ok=True)
 tts=Vieneu(mode='v3turbo',device='cpu',backend='onnx',precision='fp32',threads=4)
 phrases=[]
 for scene,row in enumerate(STORY):
  for sentence in re.split(r'(?<=[.!?])\s+',row['text']):
   spoken=sentence.replace('Babylon','Ba bi lon').replace('Nineveh','Ni ni vê')
   i=len(phrases);raw=folder/f'raw_{i:02}.wav';marker=raw.with_suffix('.sha256')
   digest=hashlib.sha256((spoken+'|HaiDang|Babylon').encode()).hexdigest()
   if not raw.exists() or not marker.exists() or marker.read_text()!=digest:
    np.random.seed(151+i)
    audio=tts.infer(spoken,voice='Hải Đăng',temperature=.55,top_k=25,max_chars=180)
    tts.save(audio,str(raw));marker.write_text(digest)
   clean=folder/f'clean_{i:02}.wav'
   ff(['-y','-i',str(raw),'-af','silenceremove=start_periods=1:start_duration=0.015:start_threshold=-48dB,areverse,silenceremove=start_periods=1:start_duration=0.015:start_threshold=-48dB,areverse','-ar','48000','-ac','1',str(clean)])
   with wave.open(str(clean)) as w:seconds=w.getnframes()/w.getframerate()
   phrases.append(dict(scene=scene,text=sentence,length=seconds,file=clean))
   print(f'VOICE {i+1}: {seconds:.2f}s',flush=True)
 gaps=[.34 if a['scene']!=b['scene'] else .16 for a,b in zip(phrases,phrases[1:])]+[0]
 tempo=sum(x['length'] for x in phrases)/(60-.25-.7-sum(gaps))
 track=np.zeros(60*48000,dtype=np.float32);cursor=.25;cues=[]
 for i,(phrase,gap) in enumerate(zip(phrases,gaps)):
  fitted=folder/f'cue_{i:02}.wav'
  ff(['-y','-i',str(phrase['file']),'-af',f'atempo={tempo:.9f}','-ar','48000','-ac','1',str(fitted)])
  audio,sr=sf.read(fitted,dtype='float32');a=round(cursor*sr);b=a+len(audio)
  assert b<=len(track)
  track[a:b]=audio;cues.append(dict(scene=phrase['scene'],text=phrase['text'],start=a/sr,end=b/sr))
  cursor=b/sr+gap
 sf.write(folder/'unmastered.wav',track,48000,subtype='PCM_16')
 ff(['-y','-i',str(folder/'unmastered.wav'),'-af','loudnorm=I=-17:TP=-2:LRA=7','-ar','48000','-ac','2',str(DEST/'narration.wav')])
 (DEST/'voice_timing.json').write_text(json.dumps(dict(voice='Hải Đăng',engine='VieNeu-TTS v3 Turbo',tempo=tempo,cues=cues),ensure_ascii=False,indent=2),encoding='utf-8')
 print(f'NARRATION READY: 60s, atempo={tempo:.3f}',flush=True)
if __name__=='__main__':run()
