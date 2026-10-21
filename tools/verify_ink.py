"""Exercise the shipped editorial workflow, rendering and motion invariants."""
import copy,json,math,subprocess,sys,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from PySide6.QtWidgets import QApplication
from PySide6.QtTest import QTest
from studio.project import load,save,new_object
from studio.renderer import Renderer
from studio.exporter import export_video,validate_output,binary,FLAGS
from studio.animation import skeleton,dimensions,evaluate_scene,gait,ENGINE_VERSION
from studio.ui.window import StudioWindow
from studio.ui.ink_dialogs import PosePicker,ArtPicker,ParentPicker

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'outputs'/'ink_v4'


def probe(path):
    return json.loads(subprocess.check_output([binary('ffprobe'),'-v','error','-show_format','-show_streams','-of','json',str(path)],creationflags=FLAGS))


def verify():
    app=QApplication.instance() or QApplication([]);OUT.mkdir(parents=True,exist_ok=True)
    from studio.ui.style import STYLE
    app.setStyle('Fusion');app.setStyleSheet(STYLE)
    result={'engine':ENGINE_VERSION,'checks':{},'timings_seconds':{}}
    project_path=ROOT/'examples'/'ink_showcase'/'project.json';project=load(project_path)
    window=StudioWindow(ROOT,project_path);window.show();QTest.qWait(250)
    window.set_time(2);window.grab().save(str(OUT/'studio_v4.png'))
    window.toggle_play();QTest.qWait(1600);window.toggle_play()
    assert window.t>2.5
    result['checks']['native_startup_playback']={'frames':window.preview_frames,'late':window.preview_late,'time':window.t}
    poses=PosePicker(window);poses.show();QTest.qWait(100);poses.grab().save(str(OUT/'pose_picker.png'));poses.close()
    art=ArtPicker(window);art.show();QTest.qWait(100);art.grab().save(str(OUT/'art_picker.png'));art.close()
    # Grouping must survive duplicate/save/load and resolve children to the cloned parent.
    scene=window.current_scene();parent=new_object('group','Test group',0,0);parent['end']=scene['duration']
    scene['objects'].append(parent);scene['objects'][0]['parent']=parent['id']
    window.duplicate_scene();cloned=window.current_scene();ids={o['id'] for o in cloned['objects']}
    assert all(o.get('parent','') in ids for o in cloned['objects'] if o.get('parent'))
    save(window.project,OUT/'gui_saved_project.json',project_path.parent)
    load(OUT/'gui_saved_project.json');result['checks']['group_duplicate_save_load']='PASS'
    window.dirty=False;window.close();app.processEvents()
    renderer=Renderer()
    a=renderer.frame(project,project_path.parent,3,640,360);renderer.frame(project,project_path.parent,17,640,360)
    b=renderer.frame(project,project_path.parent,3,640,360);assert a==b
    result['checks']['arbitrary_seek']='PASS'
    motion=load(OUT/'motion_project.json');max_error=0;stance_error=0;contacts=[]
    for scene in motion['scenes']:
        obj=next(o for o in scene['objects'] if o['kind']=='character')
        for i in range(240):
            t=i/30;js,st=evaluate_scene(scene['objects'],t)[obj['id']]
            _,upper,fore,_,_,_=dimensions(obj,t)
            for side in ('l','r'):
                max_error=max(max_error,abs(math.dist(js['shoulder_'+side],js['elbow_'+side])-upper*st['scale']),abs(math.dist(js['elbow_'+side],js['hand_'+side])-fore*st['scale']))
            for c in obj.get('contacts',[]):
                if c['start']+c['blend']<t<c['end']-c['release']:contacts.append(math.dist(js['hand_'+c['hand']],(c['x'],c['y'])))
        if obj.get('motions'):
            for i in range(45,150):
                t=i/30
                for side in ('l','r'):
                    x,ground=gait(obj,t,side);y,after=gait(obj,t+1/30,side)
                    # Inspect the rendered skeleton, so unreachable IK targets
                    # cannot pass merely because the requested anchor was fixed.
                    if ground and after:
                        before=evaluate_scene(scene['objects'],t)[obj['id']][0]['foot_'+side]
                        after_foot=evaluate_scene(scene['objects'],t+1/30)[obj['id']][0]['foot_'+side]
                        stance_error=max(stance_error,math.dist(before,after_foot))
    assert max_error<.001 and stance_error<.001 and max(contacts,default=0)<.001
    result['checks']['motion']={'max_arm_length_error_design_px':max_error,'max_stance_drift_design_px':stance_error,'max_locked_hand_error_design_px':max(contacts,default=0)}
    start=time.perf_counter();export_video(motion,OUT,OUT/'motion_three_cases_1080p.mp4',1920,1080,30)
    result['timings_seconds']['motion_export']=time.perf_counter()-start
    start=time.perf_counter();export_video(project,project_path.parent,OUT/'ink_4k_2s.mp4',3840,2160,30,start=1,length=2)
    result['timings_seconds']['4k_export']=time.perf_counter()-start
    for name in ('motion_three_cases_1080p.mp4','ink_4k_2s.mp4','ink_history_1080p.mp4'):
        path=OUT/name
        data=probe(path);result['checks'][name]={'width':data['streams'][0]['width'],'height':data['streams'][0]['height'],'fps':data['streams'][0]['r_frame_rate'],'frames':data['streams'][0].get('nb_frames'),'duration':data['format']['duration']}
        subprocess.run([binary('ffmpeg'),'-v','error','-threads','2','-i',str(path),'-f','null','-'],check=True,capture_output=True,creationflags=FLAGS)
    result['status']='PASS';(OUT/'verification_v4.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=True,indent=2),flush=True)


if __name__=='__main__':verify()
