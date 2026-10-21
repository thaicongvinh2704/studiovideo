import argparse
import sys
import json
from pathlib import Path
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication
from .ui.style import STYLE
from .ui.window import StudioWindow

def main():
    parser=argparse.ArgumentParser(description='Stickman Animation Studio')
    parser.add_argument('project',nargs='?');parser.add_argument('--smoke',action='store_true')
    parser.add_argument('--screenshot');parser.add_argument('--runtime-check',metavar='OUTPUT_FOLDER')
    parser.add_argument('--storyboard',help='Compile an editable storyboard JSON')
    parser.add_argument('--script',help='Prepare an editable film from TXT/SRT and --voice')
    parser.add_argument('--voice',help='Existing narration for --script')
    parser.add_argument('--assets-dir',help='Directory of illustrations for --script')
    parser.add_argument('--allow-draft',action='store_true',help='Explicitly allow placeholders in a draft export')
    parser.add_argument('--save-project',help='Output portable project.json for --storyboard')
    parser.add_argument('--render',help='Render project/storyboard directly to MP4 without opening editor')
    parser.add_argument('--resolution',choices=['720p','1080p','4k'],default='1080p')
    args=parser.parse_args()
    app=QApplication(sys.argv[:1]);app.setApplicationName('Stickman Animation Studio');app.setStyle('Fusion');app.setStyleSheet(STYLE)
    root=Path(sys.executable).parent if getattr(sys,'frozen',False) else Path(__file__).resolve().parents[1]
    if args.storyboard or args.render or args.script:
        from .explainer import load_board,compile_board
        from .project import save,load
        from .exporter import export_cached
        if args.script:
            from .explainer import suggest_board
            if not args.voice:parser.error('--script needs --voice')
            assets=[p for p in Path(args.assets_dir).iterdir() if p.suffix.lower() in ('.png','.jpg','.jpeg','.webp','.svg')] if args.assets_dir else []
            board=suggest_board(Path(args.script).read_text(encoding='utf-8-sig'),args.voice,assets,pause_assist=True)
            project=compile_board(board);project_root=Path(args.script).resolve().parent
            if args.save_project:
                project=save(project,args.save_project,project_root);project_root=Path(args.save_project).resolve().parent
        elif args.storyboard:
            project=compile_board(load_board(args.storyboard));project_root=Path(args.storyboard).resolve().parent
            if args.save_project:
                project=save(project,args.save_project,project_root);project_root=Path(args.save_project).resolve().parent
        elif args.project:project=load(args.project);project_root=Path(args.project).resolve().parent
        else:parser.error('--render needs a project or --storyboard')
        if args.render:
            if args.allow_draft:project['allow_draft']=True
            width,height={'720p':(1280,720),'1080p':(1920,1080),'4k':(3840,2160)}[args.resolution]
            export_cached(project,project_root,args.render,width,height,project.get('fps',30))
        if not args.render and not args.save_project:parser.error('--storyboard needs --save-project or --render')
        return
    window=StudioWindow(root,args.project);window.show()
    if args.runtime_check:
        from .ui.workers import Worker
        from .tts import VoiceEngine
        from .project import save,load
        from .exporter import export_video
        folder=Path(args.runtime_check).resolve();folder.mkdir(parents=True,exist_ok=True)
        window.set_time(2);window.grab().save(str(folder/'frozen_ui.png'))
        result_code=[0]
        def check(worker):
            engine=VoiceEngine(root/'voices');voice=next(v for _,v in engine.voices() if v.endswith('.onnx'))
            wav=folder/'frozen_voice.wav';length=engine.synthesize('Cha đưa chiếc ô vàng cho con.',voice,wav)
            p=window.project.copy();p['audio']=[dict(id='runtime_voice',file=str(wav),start=0,duration=length,group='voice',volume=1)]
            p=save(p,folder/'runtime_project.json',window.root);assert load(folder/'runtime_project.json')==p
            export_video(p,folder,folder/'frozen_video.mp4',320,180,12,length=2,cancel=worker.cancel)
            return dict(status='PASS',frozen=bool(getattr(sys,'frozen',False)),voice_seconds=length,
                        checks=['startup','Piper Vietnamese','save/load','FFmpeg export and ffprobe validation'])
        def finished(result):
            (folder/'runtime_check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
        def failed(message):
            result_code[0]=1;finished(dict(status='FAIL',error=message))
        window.project_worker=Worker(check,window);window.project_worker.done.connect(finished);window.project_worker.failed.connect(failed)
        window.project_worker.finished.connect(lambda:app.exit(result_code[0]));window.project_worker.start()
    elif args.screenshot:
        def capture():window.set_time(2);window.grab().save(args.screenshot);app.quit()
        QTimer.singleShot(1400,capture)
    elif args.smoke:QTimer.singleShot(1500,app.quit)
    sys.exit(app.exec())
