"""Render character proofs and inspect release media, without judging art similarity."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QImage,QPainter,QColor
from studio.animation import ENGINE_VERSION,skeleton
from studio.explainer import presenter
from studio.renderer import Renderer
from studio.exporter import binary,FLAGS

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'outputs'/'ink_v4'


def media_info(path):
    data=json.loads(subprocess.check_output([binary('ffprobe'),'-v','error','-show_format','-show_streams','-of','json',str(path)],creationflags=FLAGS))
    video=next(s for s in data['streams'] if s['codec_type']=='video')
    subprocess.run([binary('ffmpeg'),'-v','error','-threads','2','-i',str(path),'-f','null','-'],check=True,capture_output=True,creationflags=FLAGS)
    return dict(width=video['width'],height=video['height'],fps=video['r_frame_rate'],frames=video.get('nb_frames'),duration=data['format']['duration'],decode='PASS')


def proofs():
    app=QApplication.instance() or QApplication([])
    r=Renderer();im=QImage(600,650,QImage.Format.Format_RGB32);im.fill(QColor('white'))
    o=presenter(285,610,2.8,'point');p=QPainter(im);p.setRenderHint(QPainter.RenderHint.Antialiasing)
    r.character(p,o,1,False,skeleton(o,1));p.end();im.save(str(OUT/'user_reference_point.png'))
    sheet=QImage(1050,760,QImage.Format.Format_RGB32);sheet.fill(QColor('white'));p=QPainter(sheet);p.setRenderHint(QPainter.RenderHint.Antialiasing)
    for i,pose in enumerate(('point','rest','think','explain','hold','confident')):
        p.save();p.translate((i%3)*350,(i//3)*380)
        o=presenter(150,340,1.45,pose);r.character(p,o,1,False,skeleton(o,1));p.setPen(QColor('#191919'));p.drawText(15,365,pose);p.restore()
    p.end();sheet.save(str(OUT/'black_character_poses.jpg'))
    from PIL import Image,ImageDraw
    frames=OUT/'release_frames';frames.mkdir(exist_ok=True)
    sheet=Image.new('RGB',(1600,560),'white')
    for i,t in enumerate((2,10,19,27,35,44,52,77)):
        path=frames/f'pilot_{t}.png'
        subprocess.run([binary('ffmpeg'),'-y','-v','error','-ss',str(t),'-i',str(OUT/'ink_history_1080p.mp4'),'-frames:v','1',str(path)],check=True,capture_output=True,creationflags=FLAGS)
        im=Image.open(path).convert('RGB');im.thumbnail((400,245));sheet.paste(im,((i%4)*400,(i//4)*280+25));ImageDraw.Draw(sheet).text(((i%4)*400+10,(i//4)*280+8),f'{t}s',fill='black')
    sheet.save(OUT/'decoded_contact_sheet.jpg')


def verify():
    proofs();report=dict(engine=ENGINE_VERSION,status='PASS',art_approval='Pending user visual review',media={})
    for name in ('ink_history_1080p.mp4','second_story_1080p.mp4','motion_three_cases_1080p.mp4','ink_4k_2s.mp4'):
        report['media'][name]=media_info(OUT/name)
    check=OUT/'frozen_runtime'/'runtime_check.json'
    if check.exists():report['frozen_runtime']=json.loads(check.read_text(encoding='utf-8'))
    else:report.update(status='INCOMPLETE',frozen_runtime='Not run')
    exe=ROOT/'dist'/'StickmanAnimationStudio'/'StickmanAnimationStudio.exe'
    from PyInstaller.archive.readers import CArchiveReader
    archive=CArchiveReader(str(exe)).open_embedded_archive('PYZ.pyz')
    code=archive.extract('studio.animation')
    assert ENGINE_VERSION in code.co_consts, 'EXE contains a different animation engine'
    report['packaged_engine']=ENGINE_VERSION
    report['exe_sha256']=hashlib.sha256(exe.read_bytes()).hexdigest()
    (OUT/'release_verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=True,indent=2))


if __name__=='__main__':verify()
