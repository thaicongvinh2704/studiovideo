"""Download pinned portable build tools and checksum-verified VoxCPM2 GGUFs."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import threading
import time

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'voices/local_design'
LOCK=threading.Lock()


def sha256(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(8*1024*1024),b''):h.update(block)
    return h.hexdigest()


def download(item):
    import requests
    target=BASE/item['path'];target.parent.mkdir(parents=True,exist_ok=True)
    expected=item.get('sha256')
    if target.exists() and (not item.get('bytes') or target.stat().st_size==item['bytes']):
        if not expected or sha256(target)==expected:
            print('Cached: '+item['path'],flush=True);return dict(**item,actual_sha256=sha256(target))
    temporary=target.with_suffix(target.suffix+'.partial')
    for attempt in range(3):
        try:
            start=temporary.stat().st_size if temporary.exists() else 0
            headers={'Range':f'bytes={start}-'} if start else {}
            with requests.get(item['url'],headers=headers,stream=True,timeout=(30,90)) as response:
                response.raise_for_status()
                if response.status_code!=206:start=0
                mode='ab' if start else 'wb';total=item.get('bytes',0)
                mark=int(start/total*10) if total else 0
                with temporary.open(mode) as f:
                    done=start
                    for block in response.iter_content(4*1024*1024):
                        if not block:continue
                        f.write(block);done+=len(block)
                        if total and int(done/total*10)>mark:
                            mark=int(done/total*10)
                            with LOCK:print(f'{item["path"]}: {done/total:.0%}',flush=True)
            if item.get('bytes') and temporary.stat().st_size!=item['bytes']:
                raise ValueError('Incomplete download '+item['path'])
            actual=sha256(temporary)
            if expected and actual!=expected:raise ValueError('SHA256 mismatch '+item['path'])
            temporary.replace(target)
            print('Verified: '+item['path'],flush=True)
            return dict(**item,actual_sha256=actual)
        except Exception:
            if attempt==2:raise
            time.sleep(2*(attempt+1))


def main():
    import requests
    BASE.mkdir(exist_ok=True)
    models=json.loads((BASE/'model_metadata.json').read_text(encoding='utf-8'))
    tools=json.loads((BASE/'toolchain_metadata.json').read_text(encoding='utf-8'))
    items=[]
    for name in ['VoxCPM2-BaseLM-Q8_0.gguf','VoxCPM2-Acoustic-F16.gguf']:
        entry=next(x for x in models if x['path']==name)
        items.append(dict(path='models/'+name,bytes=entry['size'],sha256=entry['lfs']['oid'],
            url='https://huggingface.co/DennisHuang648/VoxCPM2-GGUF/resolve/main/'+name))
    for repo,suffix in [('skeeto/w64devkit','x64-2.10.1.7z.exe'),('Kitware/CMake','windows-x86_64.zip')]:
        release=tools[repo];asset=next(a for a in release['assets'] if a['name'].endswith(suffix))
        item=dict(path='downloads/'+asset['name'],bytes=asset['size'],url=asset['browser_download_url'])
        if asset.get('digest','').startswith('sha256:'):item['sha256']=asset['digest'].split(':')[1]
        items.append(item)
    session=requests.Session()
    commit=session.get('https://api.github.com/repos/tc-mb/llama.cpp-omni/commits/master',timeout=30).json()['sha']
    items.extend([
        dict(path='downloads/7zr.exe',url='https://www.7-zip.org/a/7zr.exe'),
        dict(path='downloads/llama.cpp-omni-'+commit+'.zip',url='https://codeload.github.com/tc-mb/llama.cpp-omni/zip/'+commit),
    ])
    (BASE/'download_plan.json').write_text(json.dumps(dict(runtime_commit=commit,files=items),indent=2),encoding='utf-8')
    with ThreadPoolExecutor(max_workers=3) as executor:results=list(executor.map(download,items))
    (BASE/'download_receipt.json').write_text(json.dumps(dict(runtime_commit=commit,files=results),indent=2),encoding='utf-8')
    print('All downloads verified; ready to unpack/build.',flush=True)


if __name__=='__main__':main()
