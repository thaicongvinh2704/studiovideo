import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
DEST=ROOT/'projects'/'nguoi_viet_co_performance'
from PySide6.QtWidgets import QApplication
from studio.project import load
from studio.renderer import Renderer
from studio.exporter import export_video
from PIL import Image,ImageDraw
APP=QApplication.instance() or QApplication([])
r=Renderer();p=load(DEST/'project.json')
times=(.5,2,3.5,5.5,7.5,10,15,19,29,38,48,58)
sheet=Image.new('RGB',(1920,1440),'white');d=ImageDraw.Draw(sheet)
for i,t in enumerate(times):
    f=DEST/'review'/f'pose_{t}.png';r.frame(p,DEST,t,1920,1080).save(str(f))
    im=Image.open(f);im.thumbnail((640,360));sheet.paste(im,(i%3*640,i//3*360))
    d.text((i%3*640+8,i//3*360+8),f'{t}s',fill='#cc2222')
sheet.save(DEST/'review'/'acting_sheet.jpg')
print('Acting contact sheet ready',flush=True)
if '--export' in sys.argv:
    short=load(DEST/'acting_proof.json')
    export_video(short,DEST,DEST/'Thu_dien_xuat_13_giay.mp4',1920,1080,30)
    print('Acting proof exported',flush=True)
