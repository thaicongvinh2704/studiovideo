from pathlib import Path
import subprocess,sys,json,hashlib,os,shutil,urllib.request
ROOT=Path(__file__).resolve().parent.parent
COMMIT='e0a32bce84f4603f2b61b16b50f8958e68fd6171'
MODEL_REV='451f4fe16113bff5a5d2269ed5ad43b0592e9a14'
repo=ROOT/'vendor/ComfyUI';env=ROOT/'.envs/comfy';python=env/'Scripts/python.exe'
if shutil.disk_usage(ROOT).free<15*1024**3:raise SystemExit('Cần dự trữ ít nhất 15 GiB để cài ComfyUI và checkpoint')
repo.parent.mkdir(exist_ok=True)
if not repo.exists():subprocess.run(['git','clone','--no-checkout','https://github.com/Comfy-Org/ComfyUI.git',str(repo)],check=True)
subprocess.run(['git','-C',str(repo),'checkout',COMMIT],check=True)
if not python.exists():subprocess.run([sys.executable,'-m','venv',str(env)],check=True)
subprocess.run([str(python),'-m','pip','install','torch==2.8.0','torchvision==0.23.0','--index-url','https://download.pytorch.org/whl/cu128'],check=True)
subprocess.run([str(python),'-m','pip','install','-r',str(repo/'requirements.txt')],check=True)
checkpoint=repo/'models/checkpoints/v1-5-pruned-emaonly.safetensors'
if not checkpoint.exists():
    url=f'https://huggingface.co/stable-diffusion-v1-5/stable-diffusion-v1-5/resolve/{MODEL_REV}/v1-5-pruned-emaonly.safetensors'
    tmp=checkpoint.with_suffix('.download')
    with urllib.request.urlopen(url,timeout=120) as response,tmp.open('wb') as output:
        copied=0
        while block:=response.read(4*1048576):
            output.write(block);copied+=len(block)
            if copied%(256*1048576)<4*1048576:print('SD 1.5 downloaded MB: '+str(copied//1048576),flush=True)
    if tmp.stat().st_size!=4265146304:raise SystemExit('Checkpoint size mismatch')
    tmp.replace(checkpoint)
h=hashlib.sha256()
with checkpoint.open('rb') as f:
    for block in iter(lambda:f.read(1048576),b''):h.update(block)
profiles_path=ROOT/'config/workers.json';profiles_source=profiles_path if profiles_path.exists() else ROOT/'config/workers.example.json';profiles=json.loads(profiles_source.read_text('utf-8'));profile=profiles['sd15-local']
profile.update(python=str(ROOT/'.venv/Scripts/python.exe'),engine_python=str(python),engine_script=str(repo/'main.py'),engine_commit=COMMIT,model_path=str(checkpoint),model_hash=h.hexdigest(),workflow_path=str(ROOT/'config/sd15-workflow.json'),endpoint='http://127.0.0.1:8189',port=8189,min_ram_mb=4096,min_vram_mb=2800,license_record={'spdx':'CreativeML-OpenRAIL-M','commercial_use':True,'source':'https://huggingface.co/stable-diffusion-v1-5/stable-diffusion-v1-5','revision':MODEL_REV,'conditions':'OpenRAIL usage restrictions apply; retain notices','verified_date':'2026-10-14'},nodes={'positive':'6','negative':'7','latent':'5','sampler':'3'},status='installed_not_tested')
profiles_path.write_text(json.dumps(profiles,ensure_ascii=False,indent=2),encoding='utf-8')
with open(ROOT/'config/comfy-requirements-lock.txt','w',encoding='utf-8') as f:subprocess.run([str(python),'-m','pip','freeze'],stdout=f,check=True)
profile.update(min_ram_mb=6144,reserve_after_engine_mb=2300)
profiles_path.write_text(json.dumps(profiles,ensure_ascii=False,indent=2),encoding='utf-8')
print('Pinned ComfyUI/SD15 installed; inference not yet verified.',flush=True)
