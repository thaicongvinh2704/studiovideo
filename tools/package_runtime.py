"""Copy editable resources beside the frozen app; bundle local FFmpeg if available."""
from pathlib import Path
import shutil
import subprocess
import importlib.metadata
import sys
import zipfile

root=Path(__file__).resolve().parents[1]
target=root/'dist'/'StickmanAnimationStudio'
target.mkdir(parents=True,exist_ok=True)
for name in ('assets','voices','presets','examples'):
    if (root/name).exists():shutil.copytree(root/name,target/name,dirs_exist_ok=True)
for name in ('README_VI.md','TEST_RESULTS.md','THIRD_PARTY_NOTICES.md','LICENSE','config.json','QUALITY_V2.md','EXPLAINER_V3.md','INK_V4.md','AGENTS.md','CHARACTER_STANDARD.md','DRAWING_DIRECTION.md','DRAWING_DESK_GUIDE.md','DRAWING_TOOL_RESEARCH.md'):
    if (root/name).exists():shutil.copy2(root/name,target/name)
showcase=root/'outputs'/'explainer_v3'/'history_explainer_1080p.mp4'
if showcase.exists():
    dest=target/'examples'/'explainer_showcase'/'showcase.mp4';dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(showcase,dest)
proof=target/'verification_v3';proof.mkdir(exist_ok=True)
for name in ('verification.json','unit_tests.log','motion_measurements.json','showcase_contact_sheet.jpg','package_verification.json'):
    source=root/'outputs'/'explainer_v3'/name
    if source.exists():shutil.copy2(source,proof/name)
showcase_v4=root/'outputs'/'ink_v4'/'ink_history_1080p.mp4'
if showcase_v4.exists():
    dest=target/'examples'/'ink_showcase'/'showcase.mp4';dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(showcase_v4,dest)
proof_v4=target/'verification_v4';proof_v4.mkdir(exist_ok=True)
for name in ('verification_v4.json','unit_tests.log','black_character_poses.jpg','user_reference_point.png','decoded_contact_sheet.jpg','long_verification.json','release_verification.json'):
    source=root/'outputs'/'ink_v4'/name
    if source.exists():shutil.copy2(source,proof_v4/name)
# Keep the MSVC helper DLLs on one version; NumPy retains its private renamed DLL.
qt=Path(importlib.metadata.distribution('PySide6_Essentials').locate_file('PySide6'))
internal=target/'_internal'
for dll in qt.glob('*.dll'):
    if dll.name.lower().startswith(('msvcp140','vcruntime140')):shutil.copy2(dll,internal/dll.name)
if (internal/'icuuc.dll').exists():
    # Never let a third-party versioned ICU shadow the native Windows ICU used by Qt.
    (internal/'icuuc.dll').rename(internal/'icuuc.dll.disabled-poppler')
(target/'bin').mkdir(exist_ok=True)
for name in ('ffmpeg','ffprobe'):
    found=shutil.which(name)
    if found:shutil.copy2(found,target/'bin'/(name+'.exe'))
    else:print('Not bundled:',name)
licenses=target/'third_party_licenses';licenses.mkdir(exist_ok=True)
vendor=licenses/'perfect-freehand-python';vendor.mkdir(exist_ok=True)
for name in ('LICENSE.txt','NOTICE.md'):
    shutil.copy2(root/'studio'/'vendor'/'perfect_freehand'/name,vendor/name)
for dist in importlib.metadata.distributions():
    for entry in dist.files or []:
        if 'license' in str(entry).lower() or str(entry).lower().endswith('copying'):
            path=Path(dist.locate_file(entry))
            if path.is_file():
                dest=licenses/dist.metadata['Name']/str(entry).replace('..','_')
                dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,dest)
ff=shutil.which('ffmpeg')
if ff:
    source=Path(ff).parent.parent
    if (source/'LICENSE').exists():shutil.copy2(source/'LICENSE',licenses/'FFmpeg_LICENSE.txt')
    info=subprocess.check_output([ff,'-version'],text=True,encoding='utf-8')
    (licenses/'FFmpeg_build.txt').write_text(info,encoding='utf-8')
with zipfile.ZipFile(target/'StickmanAnimationStudio-Source.zip','w',zipfile.ZIP_DEFLATED) as archive:
    source_names=['main.py','requirements.txt','StickmanAnimationStudio.spec','install_windows.bat',
                  'start_studio.bat','start_studio_drawing.bat','start_drawing_desk.bat','build_windows.bat','README_VI.md','TEST_RESULTS.md','AGENTS.md','CHARACTER_STANDARD.md','DRAWING_DIRECTION.md',
                  'THIRD_PARTY_NOTICES.md','LICENSE','config.json','QUALITY_V2.md','EXPLAINER_V3.md','INK_V4.md','studio','tools','tests','presets','assets','examples','voices']
    for name in source_names:
        source=root/name
        files=source.rglob('*') if source.is_dir() else [source]
        for path in files:
            if not path.is_file() or '__pycache__' in path.parts or path.suffix in ('.pyc','.onnx','.download'):continue
            archive.write(path,path.relative_to(root).as_posix())
print('Runtime packaged:',target)
