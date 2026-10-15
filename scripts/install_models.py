"""Inspect first; --install downloads only pinned profiles, never random model candidates."""
from pathlib import Path
import sys,os,json,argparse,shutil,subprocess,hashlib
import httpx
ROOT=Path(__file__).resolve().parent.parent
parser=argparse.ArgumentParser();parser.add_argument('profile',choices=['tts','asr']);parser.add_argument('--install',action='store_true');args=parser.parse_args()
groups={
 'tts':[('pnnbao-ump/VieNeu-TTS-v3-Turbo',['onnx_update/config.json','onnx_update/tokenizer.json','onnx_update/vieneu_acoustic_cached.onnx','onnx_update/vieneu_backbone_shared.data','onnx_update/vieneu_decode_step.onnx','onnx_update/vieneu_prefill.onnx','onnx_update/vieneu_v3_heads.npz','README.md']),('OpenMOSS-Team/MOSS-Audio-Tokenizer-Nano-ONNX',['moss_audio_tokenizer_decode_full.onnx','moss_audio_tokenizer_decode_shared.data','moss_audio_tokenizer_decode_step.onnx','codec_browser_onnx_meta.json','moss_audio_tokenizer_encode.onnx','moss_audio_tokenizer_encode.data','README.md'])],
 'asr':[('Systran/faster-whisper-medium',['config.json','model.bin','tokenizer.json','vocabulary.txt','README.md'])]
}
manifest=[];total=0
for repo,names in groups[args.profile]:
    data=httpx.get('https://huggingface.co/api/models/'+repo+'?blobs=true',timeout=30).json()
    if data.get('cardData',{}).get('license') not in ['apache-2.0','mit']:raise SystemExit('Model license unresolved; refusing download')
    sizes={x['rfilename']:x.get('size',0) for x in data['siblings']}
    for name in names:
        if name not in sizes:raise SystemExit('Missing artifact '+name)
        manifest.append({'repo':repo,'revision':data['sha'],'file':name,'size':sizes[name],'license':data['cardData']['license']});total+=sizes[name]
planpath=ROOT/'config'/f'{args.profile}-install-plan.json';planpath.write_text(json.dumps({'total_bytes':total,'files':manifest},indent=2),encoding='utf-8')
print(json.dumps({'profile':args.profile,'download_mb':round(total/1048576,1),'artifacts':len(manifest),'plan':str(planpath)},ensure_ascii=False),flush=True)
if not args.install:raise SystemExit()
if shutil.disk_usage(ROOT).free<total+1024**3:raise SystemExit('Insufficient disk reserve')
env=ROOT/'.envs'/('tts' if args.profile=='tts' else 'audio');python=env/'Scripts/python.exe'
if not python.exists():subprocess.run([sys.executable,'-m','venv',str(env)],check=True)
packages=['vieneu==3.7.1'] if args.profile=='tts' else ['faster-whisper==1.2.1','av==16.0.1']
subprocess.run([str(python),'-m','pip','install',*packages],check=True)
subprocess.run([str(python),str(ROOT/'scripts/model_download.py'),str(planpath)],check=True)
