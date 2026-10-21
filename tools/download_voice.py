"""Explicit setup-time download from the upstream voice repository."""
from pathlib import Path
from urllib.request import urlretrieve
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
REVISION = '3d796cc2f2c884b3517c527507e084f7bb245aea'
BASE = f'https://huggingface.co/rhasspy/piper-voices/resolve/{REVISION}/vi/vi_VN/vais1000/medium/'

def main():
    folder = ROOT / 'voices'
    folder.mkdir(exist_ok=True)
    files = ['MODEL_CARD','vi_VN-vais1000-medium.onnx.json','vi_VN-vais1000-medium.onnx']
    result = {}
    for name in files:
        output = folder / name
        if not output.exists():
            print('Downloading',name,flush=True)
            temp = output.with_suffix(output.suffix+'.download')
            urlretrieve(BASE+name,temp)
            temp.replace(output)
        result[name] = hashlib.sha256(output.read_bytes()).hexdigest()
    (folder/'provenance.json').write_text(json.dumps(dict(source=BASE,sha256=result),indent=2))
    print('Vietnamese voice ready. See THIRD_PARTY_NOTICES.md for attribution.')

if __name__=='__main__': main()
