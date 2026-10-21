import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
DEST=Path(__file__).resolve().parents[1]
from PySide6.QtWidgets import QApplication
from studio.project import load
from studio.renderer import Renderer
from PIL import Image,ImageDraw
app=QApplication.instance() or QApplication([])
p=load(DEST/'project.json');r=Renderer()
sheet=Image.new('RGB',(1920,1080),'#dddddd');draw=ImageDraw.Draw(sheet)
times=[2,7,11,16,20,29,34,43,49]
for i,t in enumerate(times):
    path=DEST/'review'/f'preview_{t}.png'
    r.frame(p,DEST,t,1920,1080).save(str(path))
    im=Image.open(path);im.thumbnail((640,360));sheet.paste(im,((i%3)*640,(i//3)*360))
    draw.text(((i%3)*640+8,(i//3)*360+8),f'{t}s',fill='#dd2222')
sheet.save(DEST/'review'/'preview_sheet.jpg')
print('Preview complete')
