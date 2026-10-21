"""Portable Vulkan build dependencies; no installer or system PATH changes."""
import hashlib
import io
import json
from pathlib import Path
import re
import shutil
import tarfile
import zipfile
import subprocess
import zlib

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'voices/local_design'


def main():
    import requests
    meta=json.loads((BASE/'vulkan_metadata.json').read_text(encoding='utf-8'))
    vendor=BASE/'vendor/vulkan';vendor.mkdir(parents=True,exist_ok=True)
    downloads=BASE/'downloads';records=[]
    for repo,commit in meta['repos'].items():
        filename=downloads/(repo+'-'+commit+'.zip')
        url=f'https://codeload.github.com/KhronosGroup/{repo}/zip/{commit}'
        if not filename.exists():
            response=requests.get(url,timeout=90);response.raise_for_status();filename.write_bytes(response.content)
        dest=vendor/repo;dest.mkdir(exist_ok=True)
        with zipfile.ZipFile(filename) as z:
            for info in z.infolist():
                rel=Path(*Path(info.filename).parts[1:]);target=dest/rel
                if not target.resolve().is_relative_to(dest):raise ValueError('Archive path traversal')
                if info.is_dir():target.mkdir(parents=True,exist_ok=True)
                else:
                    target.parent.mkdir(parents=True,exist_ok=True)
                    with z.open(info) as source,target.open('wb') as output:shutil.copyfileobj(source,output)
        records.append(dict(repo=repo,commit=commit,sha256=hashlib.file_digest(filename.open('rb'),'sha256').hexdigest()))
        print('Headers: '+repo,flush=True)
    # Google's continuous-build link currently points to a removed artifact.
    # Extract the official SDK payload; never execute its installer.
    url='https://sdk.lunarg.com/sdk/download/1.4.309.0/windows/VulkanSDK-1.4.309.0-Installer.exe'
    archive=downloads/'vulkansdk-1.4.309.0.exe'
    if not archive.exists():
        with requests.get(url,stream=True,timeout=(30,90)) as response:
            response.raise_for_status()
            with archive.open('wb') as output:
                for block in response.iter_content(4*1024*1024):output.write(block)
    actual=hashlib.file_digest(archive.open('rb'),'sha256').hexdigest()
    if actual!='48b132169b64fe65cdb0f20970195335a65354e73f1ea5373032c2a8bbad4297':
        raise RuntimeError('Pinned SDK archive hash changed')
    data=archive.read_bytes();signature=b'7z\xbc\xaf\x27\x1c';offset=0;payload=None
    while True:
        offset=data.find(signature,offset)
        if offset<0:break
        if zlib.crc32(data[offset+12:offset+32])==int.from_bytes(data[offset+8:offset+12],'little'):
            size=32+int.from_bytes(data[offset+12:offset+20],'little')+int.from_bytes(data[offset+20:offset+28],'little')
            payload=data[offset:offset+size];break
        offset+=6
    if payload is None:raise RuntimeError('No verified 7z payload in SDK')
    embedded=downloads/'vulkan_sdk_payload.7z';embedded.write_bytes(payload)
    dest=vendor/'sdk';dest.mkdir(exist_ok=True)
    subprocess.run([str(downloads/'7zr.exe'),'x',str(embedded),'-o'+str(dest),'-y'],check=True,
                   creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
    records.append(dict(sdk_url=url,sha256=actual,installer_executed=False,payload_crc_validated=True))
    (BASE/'vulkan_download_receipt.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
    print('glslc:',list(dest.rglob('glslc.exe')),flush=True)


if __name__=='__main__':main()
