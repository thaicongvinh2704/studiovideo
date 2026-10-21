"""Read final media and verify export/cache/editor behavior on isolated projects."""
import copy
import ctypes
import hashlib
import json
import math
import subprocess
import sys
import threading
import time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from PySide6.QtWidgets import QApplication
from studio.animation import ENGINE_VERSION,evaluate_scene,gait,skeleton,attachment
from studio.project import load,save,new_project,resequence
from studio.exporter import export_video,export_cached,binary,Cancelled
from studio.renderer import Renderer
from studio.ui.window import StudioWindow

root=Path(__file__).resolve().parents[1];out=root/'outputs/quality_v2';folder=root/'examples/yellow_umbrella_v2'

def memory():
    if sys.platform!='win32':return None
    from ctypes import wintypes
    class Counters(ctypes.Structure):
        _fields_=[('cb',wintypes.DWORD),('PageFaultCount',wintypes.DWORD)]+[(name,ctypes.c_size_t) for name in
            ('PeakWorkingSetSize','WorkingSetSize','QuotaPeakPagedPoolUsage','QuotaPagedPoolUsage',
             'QuotaPeakNonPagedPoolUsage','QuotaNonPagedPoolUsage','PagefileUsage','PeakPagefileUsage')]
    counters=Counters();counters.cb=ctypes.sizeof(counters)
    kernel=ctypes.WinDLL('kernel32');kernel.GetCurrentProcess.restype=wintypes.HANDLE
    psapi=ctypes.WinDLL('psapi');psapi.GetProcessMemoryInfo.argtypes=[wintypes.HANDLE,ctypes.POINTER(Counters),wintypes.DWORD]
    if not psapi.GetProcessMemoryInfo(kernel.GetCurrentProcess(),ctypes.byref(counters),counters.cb):raise ctypes.WinError()
    return dict(working_set_mb=round(counters.WorkingSetSize/1024**2,1),peak_working_set_mb=round(counters.PeakWorkingSetSize/1024**2,1))

def main():
    app=QApplication([]);p=load(folder/'project.json');report={'engine':ENGINE_VERSION,'checks':{}}
    checks=report['checks'];test=out/'integration';test.mkdir(exist_ok=True)
    result=save(p,test/'roundtrip/project.json',folder);assert load(test/'roundtrip/project.json')==result
    checks['portable_save_load']='PASS'
    window=StudioWindow(root,folder/'project.json');window.autosave_timer.stop();window.show();app.processEvents()
    window.scene_index=11;window.set_time(173);window.duplicate_scene();s=window.current_scene();ids={o['id'] for o in s['objects']}
    assert all(c['target'] in ids for o in s['objects'] for c in o.get('contacts',[]) if c.get('target'))
    window.undo();assert len(window.project['scenes'])==12
    for w,h in [(1366,768),(1920,1080)]:
        window.resize(w,h);window.set_time(158);app.processEvents();window.grab().save(str(out/f'studio_{w}x{h}.png'))
    window.dirty=False;window.close();app.processEvents();checks['startup_scene_duplicate_contact_remap_undo']='PASS'
    # Exercise atomic cancellation rather than assuming the previous implementation survived.
    tiny=new_project(duration=2);tiny['render_profile']='draft';dest=test/'cancel.mp4';dest.write_bytes(b'keep-existing')
    event=threading.Event()
    try:export_video(tiny,root,dest,320,180,12,length=2,cancel=event,progress=lambda a,b:event.set())
    except Cancelled:pass
    else:raise AssertionError('Cancellation did not interrupt render')
    assert dest.read_bytes()==b'keep-existing';checks['cancel_preserves_existing_file']='PASS'
    cached=new_project(duration=1);cached['scenes'].append(copy.deepcopy(cached['scenes'][0]));cached['scenes'][1]['id']='second'
    cached['scenes'][1]['objects'][0]['id']='second_actor';resequence(cached)
    path=test/'cache.mp4';export_cached(cached,root,path,320,180,12)
    scene_files=[test/'cache_scenes'/f'scene_{i:04}.mp4' for i in (1,2)]
    before=[f.stat().st_mtime_ns for f in scene_files]
    export_cached(cached,root,path,320,180,12);assert before==[f.stat().st_mtime_ns for f in scene_files]
    cached['scenes'][1]['objects'][0]['expression']='sad';export_cached(cached,root,path,320,180,12)
    after=[f.stat().st_mtime_ns for f in scene_files];assert before[0]==after[0] and before[1]!=after[1]
    checks['cache_reuses_only_unchanged_scenes']='PASS'
    sample=copy.deepcopy(tiny);sample['supersample']=2
    export_video(sample,root,test/'supersample.mp4',320,180,24,length=.5);checks['supersampling_export']='PASS'
    # Contact measurements at full weight, plus ownership continuity.
    max_error=0
    for s in p['scenes']:
        for obj in s['objects']:
            for c in obj.get('contacts',[]):
                start=c.get('start',0)+max(.05,c.get('blend',.3));end=c.get('end',15)-max(.05,c.get('release',.3))
                for i in range(40):
                    t=start+(end-start)*i/39;poses=evaluate_scene(s['objects'],t)
                    if c.get('target'):target=poses[c['target']][0][c.get('joint','hand_l')]
                    else:
                        from studio.animation import sample
                        target=(sample(c.get('keys',{}).get('x',[]),t,c.get('x',obj['x'])),sample(c.get('keys',{}).get('y',[]),t,c.get('y',obj['y']-150)))
                    target=tuple(a+b for a,b in zip(target,c.get('offset',[0,0])))
                    max_error=max(max_error,math.dist(poses[obj['id']][0]['hand_'+c.get('hand','r')],target))
    assert max_error<.001;report['max_full_weight_contact_error_world']=max_error
    s=p['scenes'][10];u=s['objects'][-1]
    report['handoff_jump_world']=math.dist(attachment(u,s['objects'],3.2-1e-6),attachment(u,s['objects'],3.2+1e-6))
    renderer=Renderer();began=time.perf_counter();before=memory()
    for i in range(300):
        im=renderer.frame(p,folder,i/24,1920,1080)
        assert im.width()==1920
    report['renderer_benchmark']={'frames':300,'seconds':round(time.perf_counter()-began,3),'memory_before':before,'memory_after':memory()}
    video=out/'yellow_umbrella_180s_1080p.mp4'
    probe=json.loads(subprocess.check_output([binary('ffprobe'),'-v','error','-show_streams','-show_format','-of','json',str(video)],creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0)))
    vs=next(s for s in probe['streams'] if s['codec_type']=='video');au=next(s for s in probe['streams'] if s['codec_type']=='audio')
    assert (vs['width'],vs['height'],vs['avg_frame_rate'],int(vs['nb_frames']))==(1920,1080,'24/1',4320)
    assert abs(float(probe['format']['duration'])-180)<.05 and au['codec_name']=='aac'
    subprocess.run([binary('ffmpeg'),'-v','error','-i',str(video),'-f','null','-'],check=True,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
    (out/'final_probe.json').write_text(json.dumps(probe,indent=2),encoding='utf-8')
    checks['full_180s_1080p24_4320_frames_audio_decode']='PASS'
    for t in [8,37,107,143,158,173]:
        subprocess.run([binary('ffmpeg'),'-y','-v','error','-ss',str(t),'-i',str(video),'-frames:v','1',str(out/f'decoded_{t}.png')],check=True,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
    report['video_sha256']=hashlib.sha256(video.read_bytes()).hexdigest()
    report['visual_review_scope']='Contact sheets and decoded frames inspected; automated checks do not certify artistic quality.'
    (out/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2),flush=True)

if __name__=='__main__':main()
