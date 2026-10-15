"""Local Windows launcher. Installs nothing; starts one core and serves built UI."""
from pathlib import Path
import os,sys,json,secrets,shutil,subprocess,time,urllib.request,argparse,socket
ROOT=Path(__file__).resolve().parent

def main():
    args=argparse.ArgumentParser();args.add_argument('--headless',action='store_true');options=args.parse_args()
    os.chdir(ROOT)
    if not (ROOT/'ui/dist/index.html').is_file():raise SystemExit('Chưa build UI. Chạy SETUP_STUDIO.cmd trước.')
    path=ROOT/'runtime.json';runtime=json.loads(path.read_text('utf-8')) if path.exists() else {}
    port=runtime.get('port',8765);url=f'http://127.0.0.1:{port}'
    try:
        with urllib.request.urlopen(url+'/api/health',timeout=2) as r:health=json.load(r)
        if health.get('result',{}).get('name')!='Story Motion Studio Local':raise RuntimeError('Cổng do dịch vụ khác sử dụng')
    except (OSError,ValueError):
        paths_file=ROOT/'config/runtime-paths.json'
        paths=json.loads(paths_file.read_text('utf-8')) if paths_file.exists() else {}
        node=shutil.which('node') or runtime.get('node') or paths.get('node')
        if not node or not Path(node).exists():raise SystemExit('Thiếu Node.js. Cập nhật config/runtime-paths.json hoặc PATH.')
        runtime={'port':port,'url':url,'token':secrets.token_urlsafe(32),'node':node,'data':str(ROOT/'data')}
        path.write_text(json.dumps(runtime,indent=2),encoding='utf-8')
        logs=ROOT/'logs';logs.mkdir(exist_ok=True)
        with open(logs/'core.log','a',encoding='utf-8') as out:
            process=subprocess.Popen([str(ROOT/'.venv/Scripts/python.exe'),'-m','uvicorn','studio.api:app','--host','127.0.0.1','--port',str(port)],cwd=ROOT,stdout=out,stderr=out,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        runtime['pid']=process.pid;path.write_text(json.dumps(runtime,indent=2),encoding='utf-8')
        for _ in range(80):
            if process.poll() is not None:raise SystemExit('Core không khởi động. Xem logs/core.log')
            try:
                urllib.request.urlopen(url+'/api/health',timeout=1).close();break
            except OSError:time.sleep(.25)
        else:raise SystemExit('Core chưa sẵn sàng sau 20 giây; xem logs/core.log')
    if not options.headless:
        import webbrowser
        webbrowser.open(url+'/#token='+runtime['token'])
    print('Story Motion Studio Local ready at '+url)

if __name__=='__main__':main()
