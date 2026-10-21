"""Compare encoded narration to the sixty-second source, including the final sentence."""
import json,subprocess,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
DEST=Path(__file__).resolve().parents[1]
from studio.exporter import binary,FLAGS
def pcm(path):
    data=subprocess.check_output([binary('ffmpeg'),'-v','error','-i',str(path),'-vn','-ar','8000','-ac','1','-f','f32le','pipe:1'],stderr=subprocess.PIPE,creationflags=FLAGS)
    return np.frombuffer(data,dtype='<f4').astype(np.float64)
out=DEST/'Mot_phut_nguoi_Viet_co_net_muc_1080p.mp4'
xall=pcm(DEST/'narration.wav');yall=pcm(out);checks=[]
for t in (1,10,20,29,39,48,56):
    start=t*8000;length=16000;x=xall[start:start+length];y=yall[start:start+length]
    x-=x.mean();y-=y.mean();size=1<<((2*length-1).bit_length())
    corr=np.fft.irfft(np.fft.rfft(y,size)*np.conj(np.fft.rfft(x,size)),size)
    lags=np.arange(-400,401);best=int(lags[np.argmax(corr[lags%size])])
    coefficient=float(np.dot(x,y)/max(1e-12,np.linalg.norm(x)*np.linalg.norm(y)))
    assert abs(best)<=80 and coefficient>.9,(t,best,coefficient)
    checks.append(dict(time=t,lag_ms=best/8,correlation=round(coefficient,5)))
report=json.loads((DEST/'review'/'verification.json').read_text(encoding='utf-8'))
report['encoded_narration_sync']=checks
(DEST/'review'/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(checks,indent=2))
