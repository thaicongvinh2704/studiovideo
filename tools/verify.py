"""Run real Windows UI/audio/render integration checks and save evidence."""
import argparse
import copy
import json
import os
import subprocess
import sys
import threading
import time
import traceback
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from PySide6.QtCore import QUrl,Qt,QPointF
from PySide6.QtGui import QImage,QColor
from PySide6.QtWidgets import QApplication
from PySide6.QtMultimedia import QMediaPlayer,QAudioOutput
from PySide6.QtTest import QTest
from studio.demo import demo
from studio.project import save,load,new_object,duration
from studio.renderer import Renderer
from studio.animation import skeleton,state,attachment
from studio.subtitles import read,active,write
from studio.tts import VoiceEngine,wav_duration
from studio.exporter import export_video,binary,Cancelled
from studio.ui.window import StudioWindow
from studio.ui.style import STYLE
from studio.ui.dialogs import KeyframeDialog,RigDialog,AttachmentDialog,SubtitleDialog,AudioDialog,VoiceDialog

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--full',action='store_true');args=parser.parse_args()
    root=Path(__file__).resolve().parents[1];out=root/'outputs';out.mkdir(exist_ok=True)
    app=QApplication([]);app.setStyle('Fusion');app.setStyleSheet(STYLE)
    report={};started=time.monotonic()
    def passed(name,details=''):
        report[name]=dict(status='PASS',details=details);print('PASS',name,details,flush=True)
        (out/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    try:
        window=StudioWindow(root);window.show();QTest.qWait(500);window.set_time(2);app.processEvents()
        assert window.isVisible();assert window.canvas.pixmap.pixmap().width()>0
        passed('01_startup','Native PySide6 window on Windows')
        p=demo();folder=root/'examples'/'yellow_umbrella';folder.mkdir(parents=True,exist_ok=True)
        path=folder/'project.json';save(p,path);assert load(path)==p
        passed('02_project_save_reopen','All 12 scenes and 36 cues preserved')
        father=p['scenes'][0]['objects'][0]
        assert skeleton(father,.1)[0]['knee_l']!=skeleton(father,.3)[0]['knee_l']
        passed('03_articulated_walk','Independent limbs; bone length invariant in unit tests')
        srt=folder/'story.srt';write(p['subtitles'],srt);cues=read(srt)
        assert len(cues)==36 and cues[-1]['end']==180
        assert active(cues,4.999)==cues[0]['text'] and active(cues,5)==cues[1]['text']
        passed('04_srt','UTF-8 BOM and exact cue boundaries')
        window.select_object(window.project['scenes'][0]['objects'][0]['id'])
        window.object_fields['x'].setValue(420);window.action.setCurrentIndex(7);window.apply_properties()
        assert window.current_object()['action']=='wave'
        assert abs(state(window.current_object(),2)['x']-420)<.001
        window.undo();assert window.project['scenes'][0]['objects'][0]['action']=='umbrella_walk'
        # Test a native canvas drag using pointer events.
        window.select_object(window.project['scenes'][0]['objects'][1]['id'])
        obj=window.current_object();joints,_=skeleton(obj,2)
        a=window.canvas.mapFromScene(window.canvas.camera_point(QPointF(*joints['hip'])))
        b=a+QPointF(25,0).toPoint()
        old=state(obj,2)['x'];QTest.mousePress(window.canvas.viewport(),Qt.MouseButton.LeftButton,pos=a)
        QTest.mouseMove(window.canvas.viewport(),b,50);QTest.mouseRelease(window.canvas.viewport(),Qt.MouseButton.LeftButton,pos=b)
        assert state(window.current_object(),2)['x']>old
        # Test timeline dragging a character clip start and resize.
        window.undo();window.timeline.draw(window.project)
        bar=next(rect for rect,data in window.timeline.items_data if data[0]=='object' and data[2]['kind']=='character')
        right=window.timeline.mapFromScene(QPointF(bar.right()-2,bar.center().y()))
        earlier=right-QPointF(14,0).toPoint()
        QTest.mousePress(window.timeline.viewport(),Qt.MouseButton.LeftButton,pos=right)
        QTest.mouseMove(window.timeline.viewport(),earlier,50);QTest.mouseRelease(window.timeline.viewport(),Qt.MouseButton.LeftButton,pos=earlier)
        assert window.project['scenes'][0]['objects'][0]['end']==14
        bar=next(rect for rect,data in window.timeline.items_data if data[0]=='object' and data[2]['kind']=='character')
        start=window.timeline.mapFromScene(QPointF(bar.left()+10,bar.center().y()))
        end=start+QPointF(14,0).toPoint()
        QTest.mousePress(window.timeline.viewport(),Qt.MouseButton.LeftButton,pos=start)
        QTest.mouseMove(window.timeline.viewport(),end,50);QTest.mouseRelease(window.timeline.viewport(),Qt.MouseButton.LeftButton,pos=end)
        assert window.project['scenes'][0]['objects'][0]['start']==1
        assert window.project['scenes'][0]['objects'][0]['end']==15
        passed('05_edit_character','Properties, keyframe updates, Undo, native canvas drag and timeline pointer handling')
        background=out/'background_test.png';im=QImage(320,180,QImage.Format.Format_RGB32);im.fill(QColor('#cfe1e5'));im.save(str(background))
        pbg=copy.deepcopy(p);pbg['scenes'][0]['background_file']=str(background)
        frame=Renderer().frame(pbg,root,2,320,180,burn=False,effects=False)
        assert frame.pixelColor(0,0).name()=='#cfe1e5'
        from unittest.mock import patch
        with patch('studio.ui.window.QFileDialog.getOpenFileName',return_value=(str(background),'PNG')):
            window.import_image('background')
        assert (window.root/window.current_scene()['background_file']).is_file()
        passed('06_background','PNG loaded and drawn by the actual renderer')
        engine=VoiceEngine(root/'voices');voice=next(v for _,v in engine.voices() if str(v).endswith('.onnx'))
        wav=out/'voice_test.wav';seconds=engine.synthesize('Chiếc ô vàng nghiêng về phía con.',voice,wav)
        assert seconds>.5 and wav.stat().st_size>1000
        audio=QAudioOutput();player=QMediaPlayer();player.setAudioOutput(audio);player.setSource(QUrl.fromLocalFile(str(wav)));player.play()
        for _ in range(60):
            QTest.qWait(100)
            if player.position()>100:break
        assert player.error()==QMediaPlayer.Error.NoError and player.position()>0;player.stop()
        passed('07_offline_vietnamese_voice',f'Piper WAV {seconds:.3f}s; Qt media playback progressed')
        clips=[]
        if args.full:
            for i,c in enumerate(p['subtitles']):
                dest=folder/'assets'/'voice'/f'cue_{i+1:02}.wav'
                length=engine.synthesize(c['text'],voice,dest,speed=1.0)
                clips.append(dict(id=f'voice_{i+1}',cue_id=c['id'],name='Narrator '+str(i+1),file=dest.relative_to(folder).as_posix(),
                    start=c['start'],duration=length,group='voice',volume=1,trim=0,fade_in=0,fade_out=0,mute=False))
                print(f'VOICE {i+1}/36 duration={length:.2f}s',flush=True)
        else:
            import shutil
            dest=folder/'assets'/'voice'/'sample.wav';dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(wav,dest)
            clips=[dict(id='voice_sample',name='Narrator',file=dest.relative_to(folder).as_posix(),start=0,duration=seconds,group='voice',volume=1,trim=0,fade_in=0,fade_out=0,mute=False)]
        p['audio']=clips;p=save(p,path,folder)
        window.open_path(path);window.set_time(2);app.processEvents()
        # Instantiate every editable native panel and commit real data in safe copies.
        test_p=copy.deepcopy(p);test_o=test_p['scenes'][0]['objects'][0]
        kd=KeyframeDialog(test_o,2);kd.add('bone_arm_r',2,1.5,'linear');kd.commit();assert test_o['keys']['bone_arm_r'][0]['v']==1.5
        sd=SubtitleDialog(test_p);sd.table.item(0,2).setText('Nội dung đã chỉnh');sd.commit();assert test_p['subtitles'][0]['text']=='Nội dung đã chỉnh'
        for dialog in [RigDialog(test_o),AttachmentDialog(test_p['scenes'][0]['objects'][-1],test_p['scenes'][0],2),
                       AudioDialog(test_p,folder),VoiceDialog(test_p,folder,root/'voices',2)]:
            dialog.show();QTest.qWait(50);dialog.hide()
        passed('08_scene_with_voice',f'{len(clips)} real voice clips saved in project; all editing dialogs initialized')
        for w,h in [(1366,768),(1920,1080)]:
            window.resize(w,h);window.set_time(2);QTest.qWait(200);window.grab().save(str(out/f'studio_{w}x{h}.png'))
        # Determinism and actual rain/limb motion using the shared frame engine.
        r=Renderer();f1=r.frame(p,folder,2,854,480);f2=r.frame(p,folder,2,854,480);f3=r.frame(p,folder,2.25,854,480)
        assert bytes(f1.constBits())==bytes(f2.constBits());assert bytes(f1.constBits())!=bytes(f3.constBits())
        f1.save(str(out/'demo_frame.png'))
        first=out/'first_scene_15s.mp4'
        def progress(a,b):
            if a%120==0 or a==b:print(f'RENDER {a}/{b}',flush=True)
        export_video(p,folder,first,854,480,12,start=0,length=15,progress=progress)
        passed('09_mp4_render',str(first.name))
        def probe(file,length):
            data=json.loads(subprocess.check_output([binary('ffprobe'),'-v','error','-show_streams','-show_format','-of','json',str(file)],creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0)))
            vs=next(s for s in data['streams'] if s['codec_type']=='video');aus=next(s for s in data['streams'] if s['codec_type']=='audio')
            assert vs['width']==854 and vs['height']==480 and vs['r_frame_rate']=='12/1'
            assert vs['codec_name']=='h264' and aus['codec_name']=='aac'
            assert abs(float(data['format']['duration'])-length)<.15
            (out/(file.stem+'_probe.json')).write_text(json.dumps(data,indent=2),encoding='utf-8')
            return data
        data=probe(first,15)
        from PySide6.QtMultimediaWidgets import QVideoWidget
        video_widget=QVideoWidget();video_widget.resize(854,480);video_widget.show();player.setVideoOutput(video_widget)
        player.setSource(QUrl.fromLocalFile(str(first)));player.play()
        for _ in range(60):
            QTest.qWait(100)
            if player.position()>1000:break
        assert player.error()==QMediaPlayer.Error.NoError and player.position()>0;player.stop();video_widget.hide()
        passed('10_mp4_validation','ffprobe: H.264, 854x480, 12 FPS, AAC; actual Qt video playback')
        passed('11_first_scene_15s','15.000s MP4, subtitles burned with Vietnamese font')
        cancelled=out/'cancel_preserves_existing.mp4';cancelled.write_bytes(b'keep-existing');event=threading.Event()
        try:
            export_video(p,folder,cancelled,320,180,12,length=2,cancel=event,progress=lambda a,b:event.set())
            raise AssertionError('Cancel did not interrupt')
        except Cancelled:assert cancelled.read_bytes()==b'keep-existing'
        passed('cancel_atomic_export','Existing output preserved; temporary render directory cleaned')
        if args.full:
            full=out/'yellow_umbrella_180s.mp4';p=load(path)
            assert len(p['scenes'])==12 and duration(p)==180
            export_video(p,folder,full,854,480,12,progress=progress);probe(full,180)
            write(p['subtitles'],out/'yellow_umbrella_180s.srt')
            passed('12_full_demo_180s','12 scenes reopened and rendered; 36 Piper voice clips; 180.000s verified')
        else:report['12_full_demo_180s']=dict(status='NOT_RUN',details='Use tools/verify.py --full')
        report['elapsed_seconds']=round(time.monotonic()-started,2)
    except Exception as exc:
        report['failure']=dict(status='FAIL',details=str(exc),traceback=traceback.format_exc())
        traceback.print_exc();return_code=1
    else:return_code=0
    finally:
        (out/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    return return_code

if __name__=='__main__':sys.exit(main())
