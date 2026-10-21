import argparse,copy,json,math,subprocess,sys,time,wave,array
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtTest import QTest
from studio.project import load,save,uid,duration,new_scene,new_project,resequence,resolve
from studio.renderer import Renderer
from studio.exporter import export_video,export_cached,mix_audio,binary,FLAGS
from studio.explainer import compile_board,suggest_board,load_board

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'outputs'/'explainer_v3';OUT.mkdir(parents=True,exist_ok=True)
APP=QApplication.instance() or QApplication([])
from studio.ui.style import STYLE
APP.setStyle('Fusion');APP.setStyleSheet(STYLE)

def probe(path):
    return json.loads(subprocess.check_output([binary('ffprobe'),'-v','error','-show_streams','-show_format','-of','json',str(path)],creationflags=FLAGS))

def sync_test():
    # Non-frame-aligned cuts; clicks alternate stereo channels at absolute timestamps.
    import numpy as np
    rate=48000;length=4;data=np.zeros((rate*length,2),dtype=np.int16)
    stamps=[.18,.71,1.24,1.77,2.30,2.83,3.36,3.89]
    for i,t in enumerate(stamps):
        k=round(t*rate);n=480;data[k:k+n,i%2]=(np.sin(np.arange(n)*2*math.pi*880/rate)*22000).astype(np.int16)
    wav=OUT/'stereo_sync_input.wav'
    with wave.open(str(wav),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(rate);w.writeframes(data.tobytes())
    p=new_project('Sync',1,320,180);p.update(fps=30,audio_rate=48000,audio_channels=2)
    cuts=[0,.411,1.023,1.666,2.333,3.017,4];p['scenes']=[]
    for i,(a,b) in enumerate(zip(cuts,cuts[1:])):
        s=new_scene(str(i),b-a);s.update(start=a,background='white');p['scenes'].append(s)
    p['audio']=[dict(id='sync',file=str(wav),group='voice',start=0,duration=4)]
    path=OUT/'stereo_sync_cached.mp4';export_cached(p,OUT,path,320,180,30)
    raw=subprocess.check_output([binary('ffmpeg'),'-v','error','-i',str(path),'-vn','-ar',str(rate),'-ac','2','-f','s16le','pipe:1'],creationflags=FLAGS)
    decoded=np.frombuffer(raw,dtype=np.int16).reshape(-1,2);errors=[];crosstalk=[]
    for i,t in enumerate(stamps):
        center=round(t*rate);lo=max(0,center-2400);window=np.abs(decoded[lo:center+2400,i%2].astype(np.int32));indices=np.flatnonzero(window>2500)
        assert len(indices),'Missing audio pulse'
        actual=(lo+indices[0])/rate;errors.append(actual-t)
        other=np.max(np.abs(decoded[center:center+480,1-i%2].astype(np.int32)));crosstalk.append(int(other))
    assert max(map(abs,errors))<.015,errors
    assert max(crosstalk)<500,crosstalk
    info=probe(path);video=next(s for s in info['streams'] if s['codec_type']=='video')
    assert int(video['nb_frames'])==120,video
    pts=subprocess.check_output([binary('ffprobe'),'-v','error','-select_streams','v:0','-show_entries','frame=best_effort_timestamp_time','-of','csv=p=0',str(path)],creationflags=FLAGS).decode()
    times=[float(line.strip().split(',')[0]) for line in pts.splitlines() if line.strip().split(',')[0]]
    assert max(abs((b-a)-1/30) for a,b in zip(times,times[1:]))<.001
    return dict(audio_errors_seconds=errors,other_channel_peak=crosstalk,video_frames=len(times),max_frame_interval_error=max(abs((b-a)-1/30) for a,b in zip(times,times[1:])))

def gui_check(project):
    from studio.ui.window import StudioWindow
    from studio.ui.explainer_dialogs import StoryboardDialog,GraphicDialog
    from unittest.mock import patch
    window=StudioWindow(ROOT,project);window.show();APP.processEvents()
    window.resize(1366,768);window.set_time(2);window.grab().save(str(OUT/'studio_1366x768.png'))
    board=load_board(ROOT/'examples'/'explainer_showcase'/'storyboard.json')
    d=StoryboardDialog(window);d.board=board;d.populate();d.show();APP.processEvents();d.grab().save(str(OUT/'storyboard_editor.png'))
    d.commit();assert d.result_project and len(d.result_project['scenes'])==8;d.close()
    first=window.project['scenes'][0];o=first['objects'][0];window.selected_id=o['id']
    gd=GraphicDialog(o,window);gd.text.setPlainText('Tiêu đề sửa trực tiếp');gd.commit();assert o['text']=='Tiêu đề sửa trực tiếp'
    # Group movement, cuts and undo are exercised through actual window handlers.
    peer=first['objects'][-1];o['group']=peer['group']='review';window.set_time(2)
    old=(o['x'],peer['x']);window.move_object(o['id'],o['x']+40,o['y'])
    assert o['x']==old[0]+40 and peer['x']==old[1]+40
    before=len(first['objects']);window.split_object();assert len(first['objects'])==before+1
    window.undo();assert len(window.current_scene()['objects'])==before
    # Duplication must carry scene-bound voice and SRT; reorder must retain association.
    original_id=window.current_scene()['id'];window.duplicate_scene();clone=window.current_scene()
    assert any(a.get('scene_id')==clone['id'] for a in window.project['audio'])
    window.reorder_scene(-1)
    a=next(a for a in window.project['audio'] if a.get('scene_id')==clone['id']);assert abs(a['start']-clone['start'])<1e-6
    # Native event loop playback, actual frame delivery count on this machine.
    window.set_time(1);window.toggle_play();QTest.qWait(2200)
    performance=dict(frames=window.preview_frames,late=window.preview_late,time=window.t)
    assert window.t>2.5,performance
    window.pause();window.dirty=False;window.close();APP.processEvents()
    return performance

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--long',action='store_true');args=parser.parse_args()
    root=ROOT/'examples'/'explainer_showcase';p=load(root/'project.json');report={}
    renderer=Renderer()
    from PIL import Image,ImageDraw,ImageFont
    sheet=Image.new('RGB',(1280,4*390),'#e7e9e8');draw=ImageDraw.Draw(sheet);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',20)
    for i,s in enumerate(p['scenes']):
        path=OUT/f'scene_{i+1:02}.png';renderer.frame(p,root,s['start']+2,1280,720).save(str(path))
        x=i%2*640;y=i//2*390;sheet.paste(Image.open(path).resize((640,360)),(x,y));draw.text((x+10,y+363),f'{i+1:02} / {s["layout"]}',font=font,fill='#24323a')
    sheet.save(OUT/'showcase_contact_sheet.jpg',quality=94)
    report['gui']=gui_check(root/'project.json');print('GUI:',report['gui'],flush=True)
    report['sync']=sync_test();print('Stereo sync:',report['sync'],flush=True)
    start=time.perf_counter();path=OUT/'history_explainer_1080p.mp4'
    export_cached(p,root,path,1920,1080,30)
    report['showcase_seconds']=time.perf_counter()-start;report['showcase_probe']=probe(path)
    subprocess.run([binary('ffmpeg'),'-v','error','-i',str(path),'-f','null','-'],check=True,creationflags=FLAGS)
    for name,t in [('decoded_start',2),('decoded_map',38),('decoded_end',63)]:
        subprocess.run([binary('ffmpeg'),'-y','-v','error','-ss',str(t),'-i',str(path),'-frames:v','1',str(OUT/(name+'.png'))],check=True,creationflags=FLAGS)
    print('1080p:',report['showcase_seconds'],flush=True)
    path=OUT/'sample_4k.mp4';export_video(p,root,path,3840,2160,30,start=1,length=2)
    report['4k_probe']=probe(path);print('4K OK',flush=True)
    report['status']='LONG_RUNNING' if args.long else 'PASS'
    (OUT/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    if args.long:
        if (OUT/'long_project.json').exists():long=load(OUT/'long_project.json')
        else:
            long=copy.deepcopy(p);long['scenes']=[];long['audio']=[];long['subtitles']=[];long.pop('storyboard',None)
            for i in range(19):
                for original in p['scenes']:
                    s=copy.deepcopy(original);sid=uid();s['id']=sid
                    for o in s['objects']:o['id']=uid()
                    long['scenes'].append(s)
                    for track in ('audio','subtitles'):
                        for original_clip in p[track]:
                            if original_clip.get('scene_id')==original['id']:
                                c=copy.deepcopy(original_clip);c['id']=uid();c['scene_id']=sid;long[track].append(c)
            resequence(long)
            # Repeated scenes form a technical stress fixture, not a new editorial video.
            save(long,OUT/'long_project.json',root);long=load(OUT/'long_project.json')
        start=time.perf_counter();path=OUT/'long_21min_1080p.mp4'
        export_cached(long,OUT,path,1920,1080,30,progress=lambda a,b:print(f'Long {a}/{b}',flush=True) if a%1800==0 else None)
        report['long_render_seconds']=time.perf_counter()-start;report['long_probe']=probe(path)
        subprocess.run([binary('ffmpeg'),'-v','error','-i',str(path),'-f','null','-'],check=True,creationflags=FLAGS)
        print('Long OK:',duration(long),flush=True)
    report['status']='PASS'
    (OUT/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print('All integration checks completed',flush=True)

if __name__=='__main__':main()
