from pathlib import Path
import sys,subprocess,json,shutil
ROOT=Path(__file__).resolve().parent.parent
worker_config=ROOT/'config/workers.json'
if not worker_config.exists():shutil.copyfile(ROOT/'config/workers.example.json',worker_config)
python=ROOT/'.venv/Scripts/python.exe'
if not python.exists():subprocess.run([sys.executable,'-m','venv',str(ROOT/'.venv')],check=True)
subprocess.run([str(python),'-m','pip','install','-r',str(ROOT/'requirements-lock.txt')],check=True)
pathsfile=ROOT/'config/runtime-paths.json';paths=json.loads(pathsfile.read_text('utf-8')) if pathsfile.exists() else {}
pnpm=shutil.which('pnpm') or paths.get('pnpm')
node=shutil.which('node') or paths.get('node')
if not pnpm or not node:raise SystemExit('Cần Node.js và pnpm; cập nhật config/runtime-paths.json')
env=dict(__import__('os').environ);env['PATH']=str(Path(node).parent)+';'+env.get('PATH','')
for command in ['install --frozen-lockfile','build']:
    # cmd scripts are invoked via fixed, trusted executable/arguments; no document/source interpolation.
    subprocess.run([pnpm,*command.split()],cwd=ROOT/'ui',env=env,check=True,shell=False)
subprocess.run([str(python),str(ROOT/'scripts/client_configs.py')],check=True)
print('Đã cài core/UI. Model env được giữ riêng; chạy START_STUDIO.cmd.')
