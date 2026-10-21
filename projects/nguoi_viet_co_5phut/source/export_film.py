"""Render the authored project with the installed Studio EXE, recording real progress."""
import hashlib,json,subprocess,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];DEST=Path(__file__).resolve().parents[1]


def export():
    exe=ROOT/'dist'/'StickmanAnimationStudio'/'StickmanAnimationStudio.exe'
    project=DEST/'project.json';output=DEST/'Mot_ngay_cung_nguoi_Viet_co_1080p.mp4'
    manifest=DEST/'Mot_ngay_cung_nguoi_Viet_co_1080p_scenes'/'manifest.json'
    start=time.perf_counter();previous=-1
    with (DEST/'review'/'frozen_export.log').open('wb') as log:
        proc=subprocess.Popen([str(exe),str(project),'--render',str(output),'--resolution','1080p'],stdout=log,stderr=log,creationflags=subprocess.CREATE_NO_WINDOW)
        while proc.poll() is None:
            count=0
            if manifest.exists():
                try:count=len(json.loads(manifest.read_text())['scene_keys'])
                except (OSError,ValueError):pass
            if count!=previous:print('Studio EXE · cảnh hoàn tất',count,'/ 32',flush=True);previous=count
            time.sleep(3)
        if proc.returncode:raise RuntimeError('Studio export failed: '+str(proc.returncode)+'; see frozen_export.log')
    report=dict(status='PASS',renderer='Installed Studio EXE',exe_sha256=hashlib.sha256(exe.read_bytes()).hexdigest(),project_sha256=hashlib.sha256(project.read_bytes()).hexdigest(),elapsed_seconds=round(time.perf_counter()-start,2),output=str(output))
    (DEST/'review'/'execution.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print('VIDEO READY',round(time.perf_counter()-start,1),'seconds',flush=True)


if __name__=='__main__':export()
