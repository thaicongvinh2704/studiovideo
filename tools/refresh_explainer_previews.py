"""Preview evidence decoded from the delivered MP4, rather than a second render."""
import subprocess,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from studio.project import load
from studio.exporter import binary,FLAGS

root=Path(__file__).resolve().parents[1];out=root/'outputs'/'explainer_v3'
p=load(root/'examples'/'explainer_showcase'/'project.json');video=out/'history_explainer_1080p.mp4'
sheet=Image.new('RGB',(1280,1560),'#e7e9e8');draw=ImageDraw.Draw(sheet);font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',20)
for i,scene in enumerate(p['scenes']):
    path=out/f'scene_{i+1:02}.png';t=scene['start']+min(2,scene['duration']/2)
    subprocess.run([binary('ffmpeg'),'-y','-v','error','-ss',str(t),'-i',str(video),'-frames:v','1','-vf','scale=1280:720',str(path)],check=True,creationflags=FLAGS)
    x=i%2*640;y=i//2*390;sheet.paste(Image.open(path).resize((640,360)),(x,y));draw.text((x+10,y+363),f'{i+1:02} / {scene["layout"]}',font=font,fill='#24323a')
sheet.save(out/'showcase_contact_sheet.jpg',quality=94)
for name,t in [('decoded_start',2),('decoded_map',38),('decoded_end',63)]:
    subprocess.run([binary('ffmpeg'),'-y','-v','error','-ss',str(t),'-i',str(video),'-frames:v','1',str(out/(name+'.png'))],check=True,creationflags=FLAGS)
print('Preview images decoded from final MP4')
