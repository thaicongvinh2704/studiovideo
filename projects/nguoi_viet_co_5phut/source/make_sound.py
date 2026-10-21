"""Quiet original sound design; no sampled recording or purported ancient music."""
import subprocess,sys,wave
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
DEST=Path(__file__).resolve().parents[1];FOLDER=DEST/'sound';FOLDER.mkdir(exist_ok=True)
from studio.exporter import binary,FLAGS
RATE=48000


def save(name,signal):
    signal=np.clip(signal,-.8,.8);edge=min(RATE,len(signal)//4)
    signal[:edge]*=np.linspace(0,1,edge);signal[-edge:]*=np.linspace(1,0,edge)
    if signal.ndim==1:signal=np.column_stack([signal,signal*.97])
    raw=FOLDER/(name+'.wav')
    with wave.open(str(raw),'wb') as w:w.setparams((2,2,RATE,0,'NONE','not compressed'));w.writeframes((signal*32767).astype('<i2').tobytes())
    out=FOLDER/(name+'.m4a')
    subprocess.run([binary('ffmpeg'),'-y','-v','error','-i',str(raw),'-c:a','aac','-b:a','128k',str(out)],check=True,creationflags=FLAGS)


def prepare():
    rng=np.random.default_rng(20261019);length=12;time=np.arange(length*RATE)/RATE
    noise=np.convolve(rng.normal(0,1,len(time)),np.ones(47)/47,mode='same')
    river=noise/noise.std()*.0035
    for start in (1.5,4.2,8.3,10.7):
        tt=np.arange(int(.24*RATE))/RATE;chirp=.006*np.sin(2*np.pi*(2100*tt+2400*tt*tt))*np.sin(np.pi*tt/.24)**2;i=int(start*RATE);river[i:i+len(tt)]+=chirp
    save('river_and_birds',river)
    fire=noise/noise.std()*.0015
    for i in rng.integers(0,len(time)-1200,110):
        tt=np.arange(1200)/RATE;fire[i:i+1200]+=rng.normal(0,.018,len(tt))*np.exp(-tt*180)
    save('quiet_hearth',fire)
    metal=np.zeros(3*RATE);tt=np.arange(len(metal))/RATE
    for freq,amp in ((540,.028),(1013,.014),(1832,.007)):metal+=amp*np.sin(2*np.pi*freq*tt)*np.exp(-tt*(2.7+freq/2000))
    save('soft_metal',metal)
    bed=np.zeros(300*RATE,dtype=np.float32);notes=(196,246.9417,293.6648,329.6276,293.6648,246.9417,220,293.6648)
    for index,start in enumerate(np.arange(0,300,2.6)):
        tt=np.arange(min(4*RATE,len(bed)-round(start*RATE)))/RATE;f=notes[index%len(notes)]
        env=(1-np.exp(-tt*10))*np.exp(-tt*1.6)
        note=(np.sin(2*np.pi*f*tt)+.22*np.sin(2*np.pi*f*2*tt)+.08*np.sin(2*np.pi*f*3*tt))*env*.017
        i=round(start*RATE);bed[i:i+len(note)]+=note.astype(np.float32)
    save('original_soft_bed',bed)
    print('Original soundtrack and three ambience/effect files ready')


if __name__=='__main__':prepare()
