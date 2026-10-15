from pathlib import Path
import json,os,sys,hashlib,shutil,subprocess
ROOT=Path(__file__).resolve().parent.parent
cache=ROOT/'data/models/hf-cache';os.environ['HF_HOME']=str(cache)
from huggingface_hub import hf_hub_download
plan=json.loads(Path(sys.argv[1]).read_text('utf-8'));kind=Path(sys.argv[1]).name.split('-')[0]
dest=ROOT/'data/models'/('vieneu-turbo' if kind=='tts' else 'faster-whisper-medium');dest.mkdir(parents=True,exist_ok=True)
records=[]
def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()
for index,item in enumerate(plan['files']):
    downloaded=Path(hf_hub_download(item['repo'],item['file'],revision=item['revision'],cache_dir=str(cache/'hub')))
    folder=dest/('codec' if 'Nano-ONNX' in item['repo'] else '')
    target=folder/item['file'];target.parent.mkdir(parents=True,exist_ok=True)
    if not target.exists():
        try:os.link(downloaded,target)
        except OSError:shutil.copyfile(downloaded,target)
    if target.stat().st_size!=item['size']:raise SystemExit('Artifact size mismatch')
    records.append(item|{'local_path':str(target.relative_to(dest)),'sha256':sha(target)})
    # SDK's fixed codec repo resolves "main" from this explicitly pinned local ref, offline.
    refs=cache/'hub'/('models--'+item['repo'].replace('/','--'))/'refs';refs.mkdir(exist_ok=True)
    (refs/'main').write_text(item['revision'],encoding='utf-8')
    print(json.dumps({'downloaded':index+1,'total':len(plan['files']),'file':item['file']}),flush=True)
if kind=='tts':
    import vieneu
    voices=Path(vieneu.__file__).parent/'assets/voices_v3_turbo.json';shutil.copyfile(voices,dest/'voices_v3_turbo.json');records.append({'local_path':'voices_v3_turbo.json','sha256':sha(voices),'source':'vieneu==3.7.1 bundled preset voices'})
(dest/'artifact-manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
profiles_path=ROOT/'config/workers.json';profiles_source=profiles_path if profiles_path.exists() else ROOT/'config/workers.example.json';profiles=json.loads(profiles_source.read_text('utf-8'))
key='vieneu-turbo-cpu' if kind=='tts' else 'whisper-medium-cpu'
profile=profiles.get(key,profiles['whisper-medium'].copy())
profile.update(python=sys.executable,model_path=str(dest/'onnx_update') if kind=='tts' else str(dest),model_hash=sha(dest/'artifact-manifest.json'),artifact_manifest=str(dest/'artifact-manifest.json'),license_record={'spdx':'Apache-2.0' if kind=='tts' else 'MIT','source':profile.get('source'),'commercial_use':True,'artifact_revisions':{r['repo']:r['revision'] for r in plan['files']},'verified_date':'2026-10-14'},status='installed_not_tested')
if kind=='tts':profile['backbone_path']=str(dest);profile['codec_path']=str(dest/'codec')
else:profile.update(device='cpu',compute_type='int8',min_ram_mb=3500)
profiles[key]=profile;profiles_path.write_text(json.dumps(profiles,ensure_ascii=False,indent=2),encoding='utf-8')
with open(ROOT/'config'/f'{kind}-requirements-lock.txt','w',encoding='utf-8') as f:subprocess.run([sys.executable,'-m','pip','freeze'],stdout=f,check=True)
print('Installed pinned '+key+'; real inference remains to be verified.',flush=True)
