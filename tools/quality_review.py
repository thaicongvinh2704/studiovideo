"""Prepare a separate editable demo, inspect poses, and render quality outputs."""
import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from PySide6.QtWidgets import QApplication
from PIL import Image,ImageDraw,ImageFont
from studio.demo import demo
from studio.project import load,save
from studio.renderer import Renderer
from studio.exporter import export_video
from studio.subtitles import write

root=Path(__file__).resolve().parents[1]
folder=root/'examples/yellow_umbrella_v2'
output=root/'outputs/quality_v2'

def prepare():
    p=demo()
    old=load(root/'examples/yellow_umbrella/project.json')
    p['audio']=old['audio']
    p=save(p,folder/'project.json',root/'examples/yellow_umbrella')
    write(p['subtitles'],folder/'story.srt')
    return p

def stills(p):
    renderer=Renderer();times=[8,18.4,37,53,67,83,98,113,128,143,158,173]
    canvas=Image.new('RGB',(1920,4*392),'#e3e6df');draw=ImageDraw.Draw(canvas)
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
    for i,t in enumerate(times):
        im=renderer.frame(p,folder,t,1920,1080);path=output/f'frame_{t:g}.png';im.save(str(path))
        small=Image.open(path).resize((640,360),Image.Resampling.LANCZOS)
        x=i%3*640;y=i//3*392;canvas.paste(small,(x,y));draw.text((x+12,y+365),f'Scene {i+1:02} / {t:g}s',font=font,fill='#303b34')
    canvas.save(output/'story_contact_sheet.jpg',quality=95)
    for name,ts in [('handoff',[156,157,157.96,158,158.04,159,161,163]),('hug',[166,168,169,171,173,176]),('jump',[17.5,18,18.4,18.85,19,19.5])]:
        cols=4 if name=='handoff' else 3
        sheet=Image.new('RGB',(cols*640,((len(ts)+cols-1)//cols)*392),'#e3e6df');d=ImageDraw.Draw(sheet)
        for i,t in enumerate(ts):
            im=renderer.frame(p,folder,t,1280,720);path=output/f'{name}_{t:g}.png';im.save(str(path))
            x=i%cols*640;y=i//cols*392;sheet.paste(Image.open(path).resize((640,360)),(x,y));d.text((x+10,y+365),f'{t:g}s',font=font,fill='#303b34')
        sheet.save(output/f'{name}_motion.jpg',quality=95)

def render(p,kind):
    began=time.perf_counter()
    def progress(a,b):
        if a%240==0 or a==b:print(f'{kind}: {a}/{b} frames, {time.perf_counter()-began:.1f}s',flush=True)
    if kind=='pilot':
        paths=[]
        for n,(start,length) in enumerate([(0,10),(155,10),(168,10)]):
            dest=output/f'pilot_{n+1}.mp4'
            export_video(p,folder,dest,1920,1080,24,start,length,progress=progress);paths.append(dest)
        from studio.exporter import binary,checked_run
        concat=output/'pilot_concat.txt';concat.write_text('\n'.join('file '+p.name for p in paths),encoding='utf-8')
        checked_run([binary('ffmpeg'),'-y','-v','error','-f','concat','-safe','1','-i',str(concat),'-c','copy','-movflags','+faststart',str(output/'quality_pilot_30s.mp4')])
    else:
        export_video(p,folder,output/'yellow_umbrella_180s_1080p.mp4',1920,1080,24,progress=progress)
        write(p['subtitles'],output/'yellow_umbrella_180s_1080p.srt')
    (output/f'{kind}_timing.json').write_text(json.dumps({'seconds':time.perf_counter()-began,'resolution':[1920,1080],'fps':24,'profile':p['render_profile']}),encoding='utf-8')

if __name__=='__main__':
    args=argparse.ArgumentParser();args.add_argument('mode',choices=['stills','pilot','full']);args.add_argument('--prepare',action='store_true');args=args.parse_args()
    app=QApplication([]);output.mkdir(parents=True,exist_ok=True)
    p=prepare() if args.prepare else load(folder/'project.json')
    if args.mode=='stills':stills(p)
    else:render(p,args.mode)
