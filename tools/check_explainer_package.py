import hashlib,json,sys,zipfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from studio.project import load,missing

root=Path(__file__).resolve().parents[1];target=root/'dist'/'StickmanAnimationStudio'
files=[p for directory in ('studio','tools','tests') for p in (root/directory).rglob('*.py') if '__pycache__' not in p.parts]
files += [root/n for n in ('main.py','README_VI.md','EXPLAINER_V3.md','TEST_RESULTS.md')]
with zipfile.ZipFile(target/'StickmanAnimationStudio-Source.zip') as archive:
    assert archive.testzip() is None
    for path in files:assert archive.read(path.relative_to(root).as_posix())==path.read_bytes(),path
project=target/'examples'/'explainer_showcase'/'project.json';p=load(project)
assert not missing(p,project.parent),missing(p,project.parent)
assert p==load(root/'examples'/'explainer_showcase'/'project.json')
assert (target/'voices'/'vi_VN-vais1000-medium.onnx').is_file()
assert (target/'bin'/'ffmpeg.exe').is_file() and (target/'bin'/'ffprobe.exe').is_file()
report=dict(status='PASS',source_files_matched=len(files),scenes=len(p['scenes']),portable_assets=True,
    exe_sha256=hashlib.sha256((target/'StickmanAnimationStudio.exe').read_bytes()).hexdigest())
(root/'outputs'/'explainer_v3'/'package_verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(report)
