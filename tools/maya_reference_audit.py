"""Extract local reference frames and inspect supplied production assets."""
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'projects/mo_den_maya/director_v2/reference'
REFERENCE = Path('C:/Users/thaii/Downloads/YouTube/Những Khoảng Trống Trong Lịch Sử Không Ai Giải Thích Được [kcWEaXRh2hA].mkv')

def sheet(frames, output, cols=4):
    w, h = 400, 250
    im = Image.new('RGB', (cols*w, ((len(frames)+cols-1)//cols)*h), '#e9e6df')
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 18)
    for i,(label,path) in enumerate(frames):
        tile = Image.open(path).convert('RGB'); tile.thumbnail((w-12,h-32))
        x=(i%cols)*w; y=(i//cols)*h
        im.paste(tile,(x+(w-tile.width)//2,y))
        draw.text((x+8,y+h-28),label,fill='#182527',font=font)
    im.save(output)

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    for name,source,times in [
        ('reference_opening',REFERENCE,list(range(0,100,5))),
        ('reference_range',REFERENCE,[120,180,240,300,420,540,660,780,900,1020,1140,1240]),
        ('previous_maya',ROOT/'outputs/maya_full_documentary_1080p.mp4',[2,12,30,60,120,200,320,440,560,680,760,820])]:
        frames=[]
        for t in times:
            path=OUT/f'{name}_{t:04d}.jpg'
            subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(source),'-frames:v','1','-vf','scale=640:-1',str(path)],check=True)
            frames.append((f'{t//60:02d}:{t%60:02d}',path))
        sheet(frames,OUT/f'{name}_sheet.jpg')
    print(OUT)

if __name__=='__main__': main()
