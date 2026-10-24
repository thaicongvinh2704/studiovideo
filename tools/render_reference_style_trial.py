"""Short user-requested directing trial; supplied artwork, fixed H excerpt, no synthesis.

People remain static. A source-to-source cut changes standing to kneeling.
All newly drawn elements are simple explanatory vectors, rain and typography.
This is a separate preview, never an export of the full Phong Than film.
"""
from pathlib import Path
from functools import lru_cache
import argparse
import csv
import hashlib
import json
import math
import subprocess

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / 'projects/mo_den_phong_than/assets/Mo_Den_Phong_Than_V2/images'
WORK = ROOT / 'projects/mo_den_phong_than/reference_style_trial_32s'
OUT = ROOT / 'outputs/mo_den_reference_style_trial_32s'
VOICE = ROOT / 'projects/mo_den_phong_than/voice_direction'
START, END, FPS = 212.025, 243.562, 24
DURATION = END - START + .25
W, H = 1280, 720
INK, RED, BLUE, PAPER = '#292c30', '#b34434', '#355c6b', '#fffdf8'


def sha(p):
    with Path(p).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


@lru_cache(maxsize=32)
def font(size, bold=False):
    return ImageFont.truetype('C:/Windows/Fonts/' + ('segoeuib.ttf' if bold else 'segoeui.ttf'), size)


def text(im, value, xy, size=32, color=INK, bold=False, anchor='mm'):
    ImageDraw.Draw(im).multiline_text(xy, value, font=font(size, bold), fill=color,
                                    anchor=anchor, align='center', spacing=7)


def smooth(u):
    u = max(0, min(1, u))
    return u*u*(3-2*u)


def image(path):
    return Image.open(path).convert('RGBA')


def place(im, source, box, contain=True, alpha=1):
    x, y, w, h = map(int, box)
    ratio = min(w/source.width, h/source.height) if contain else max(w/source.width, h/source.height)
    sw, sh = max(1, round(source.width*ratio)), max(1, round(source.height*ratio))
    resized = source.resize((sw, sh), Image.Resampling.LANCZOS)
    if not contain:
        left, top = (sw-w)//2, (sh-h)//2
        resized = resized.crop((left, top, left+w, top+h))
        sw, sh = w, h
    if alpha < 1:
        resized.putalpha(resized.getchannel('A').point(lambda a: round(a*alpha)))
    im.alpha_composite(resized, (round(x+(w-sw)/2), round(y+(h-sh)/2)))


def arrow(im, points, progress=1, color=RED, width=5):
    n = max(0, min(len(points), int(len(points)*progress)))
    if n < 2:
        return
    d = ImageDraw.Draw(im)
    d.line(points[:n], fill=color, width=width, joint='curve')
    x, y = points[n-1]; px, py = points[max(0, n-4)]
    ang = math.atan2(y-py, x-px)
    d.polygon([(x, y), (x-17*math.cos(ang-.45), y-17*math.sin(ang-.45)),
               (x-17*math.cos(ang+.45), y-17*math.sin(ang+.45))], fill=color)


def curve(a, b, c, n=72):
    return [((1-u)**2*a[0]+2*(1-u)*u*b[0]+u*u*c[0],
             (1-u)**2*a[1]+2*(1-u)*u*b[1]+u*u*c[1]) for u in [i/(n-1) for i in range(n)]]


def cloud(im, x, y, scale=1, color='#d8e4e5'):
    d=ImageDraw.Draw(im)
    for a,b,r in [(-52,2,31),(-15,-18,45),(33,-12,38),(65,6,28)]:
        d.ellipse((x+(a-r)*scale,y+(b-r)*scale,x+(a+r)*scale,y+(b+r)*scale), fill=color)
    d.rounded_rectangle((x-69*scale,y,x+77*scale,y+29*scale),radius=20*scale,fill=color)


def seconds(s):
    h,m,s=s.replace(',','.').split(':')
    return int(h)*3600+int(m)*60+float(s)


def cues():
    blocks=(VOICE/'Mo_Den_Phong_Than_Dien_Nghia.srt').read_text(encoding='utf-8-sig').strip().split('\n\n')
    result=[]
    for block in blocks:
        lines=block.splitlines()
        if len(lines)<3: continue
        a,b=lines[1].split(' --> '); a,b=seconds(a),seconds(b)
        if a >= START-.001 and b <= END+.001:
            result.append({'id':int(lines[0]),'in':a-START,'out':b-START,'text':' '.join(lines[2:])})
    return result


SHOTS = [
    (0,1.30,'Gặp nhau tại đàn','Y02','Định vị hai người và thứ bậc; không kéo dài đại cảnh.'),
    (1.30,4.944,'Văn Trọng chưa chịu quỳ','Y02 + Mỏ Đen 14','Cận người đối đầu; Mỏ Đen chỉ xuất hiện như phản ứng nghi ngờ.'),
    (4.944,7.48,'Roi và mệnh lệnh','Y02','Cận đúng roi đang cầm, đường chỉ dẫn sang nơi nhận lệnh.'),
    (7.48,8.952,'Làm theo sắc lệnh','Y02_B','Cut sang tư thế quỳ được cung cấp; cùng không gian, không kéo méo người.'),
    (8.952,13.936,'Nhận chức Lôi bộ','Y02_B + O01','Người nhận và cuộn sắc; nội dung hiện theo nhịp, không che mặt.'),
    (13.936,16.45,'Tận trung hai đời vua','O01','Cận sắc và hai dấu mốc; nêu phẩm chất được lời kể nhắc.'),
    (16.45,21.125,'Chức trách mới','B15 + vector mây/mưa','Mây đưa nước xuống đất, có giọt chạm đất và vòng nước; nhìn thấy hệ quả.'),
    (21.125,27.057,'Phạm vi rộng hơn triều đại','O06 + B15 + chân dung Văn Trọng','Cờ Thương bên trái, ruộng bên phải, đổi đích của đường nối.'),
    (27.057,DURATION,'Nhìn nhận phẩm chất đối thủ','Mỏ Đen 13/16 + chân dung hai người','Tò mò chuyển sang nhận ra; đưa lại quan hệ hai người để kết ý.'),
]


class Trial:
    def __init__(self):
        self.stand=image(PACK/'Y02.png');self.kneel=image(PACK/'Y02_B.png')
        self.field=image(PACK/'B15.png');self.scroll=image(PACK/'O01.png');self.flag=image(PACK/'O06.png')
        # Source scene crops, never synthesized or redrawn human geometry.
        self.wz=self.stand.crop((950,175,1610,920))
        self.jz=self.stand.crop((60,115,680,600))
        self.wzk=self.kneel.crop((940,345,1650,920))
        self.wzface=self.stand.crop((1080,180,1290,410))
        self.jzface=self.stand.crop((275,120,470,345))
        manifest=json.loads((ROOT/'assets/characters/mo_den/manifest.json').read_text(encoding='utf-8'))
        self.cat={};self.cat_entries={}
        for ident in ['mo_den_13','mo_den_14','mo_den_16']:
            a=next(a for a in manifest['assets'] if a['id']==ident)
            p=ROOT/'assets/characters/mo_den'/a['file']
            if sha(p)!=a['sha256']:raise ValueError('Original cat source mismatch: '+ident)
            self.cat_entries[ident]=a
            self.cat[ident]=image(p).crop(tuple(a['alpha_bbox']))
        self.cues=cues()
        self.bases={}

    def base(self, which):
        if which in self.bases:return self.bases[which].copy()
        im=Image.new('RGBA',(W,H),PAPER)
        if which in [0,3]:
            place(im,self.stand if which==0 else self.kneel,(0,0,1280,626))
        elif which==1:
            place(im,self.wz,(610,35,590,565))
            place(im,self.cat['mo_den_14'],(110,285,300,310))
        elif which==2:
            place(im,self.jz,(-55,5,775,625),contain=False)
            text(im,'KHƯƠNG TỬ NHA',(920,115),31,bold=True)
            text(im,'QUỲ NGHE SẮC',(925,380),39,RED,True)
        elif which==4:
            place(im,self.wzk,(60,90,480,500))
        elif which==5:
            place(im,self.scroll,(330,0,620,600))
            text(im,'SẮC PHONG',(640,150),24,BLUE,True)
            text(im,'TẬN TRUNG',(640,265),42,RED,True)
        elif which==6:
            place(im,self.field,(0,-40,1280,720),contain=False)
        elif which==7:
            text(im,'MỘT TRIỀU ĐẠI',(265,75),30,RED,True)
            text(im,'VẠN VẬT',(990,75),30,BLUE,True)
            place(im,self.flag,(95,140,280,390))
            place(im,self.field,(770,170,470,330),contain=False)
            self.portrait(im,self.wzface,(530,155,210,230))
        elif which==8:
            self.portrait(im,self.jzface,(620,85,220,250))
            self.portrait(im,self.wzface,(975,85,220,250))
            text(im,'TỬ NHA',(730,365),25,bold=True)
            text(im,'VĂN TRỌNG',(1085,365),25,bold=True)
        self.bases[which]=im.copy()
        return im

    def portrait(self, im, src, box):
        x,y,w,h=map(int,box)
        lay=Image.new('RGBA',(w,h));place(lay,src,(0,0,w,h),contain=False)
        mask=Image.new('L',(w,h));ImageDraw.Draw(mask).ellipse((0,0,w-1,h-1),fill=255)
        lay.putalpha(mask);im.alpha_composite(lay,(x,y));ImageDraw.Draw(im).ellipse((x,y,x+w,y+h),outline=INK,width=3)

    def frame(self,t, subtitles=True):
        idx=next((i for i,s in enumerate(SHOTS) if s[0]<=t<s[1]),8)
        local=t-SHOTS[idx][0];im=self.base(idx);d=ImageDraw.Draw(im)
        if idx==1 and local>.8:
            d.rounded_rectangle((80,65,465,210),radius=34,fill='white',outline=INK,width=3)
            d.polygon([(250,208),(275,242),(285,208)],fill='white')
            text(im,'CHƯA CHỊU\nQUỲ?',(272,134),34,RED,True)
        elif idx==2:
            # Circle the source-held staff, then lead the eye to the order.
            if local>.3:
                d.ellipse((146,55,251,490),outline='#f2c154',width=5)
            arrow(im,curve((260,263),(560,212),(725,355)),smooth((local-.55)/.6),RED,5)
        elif idx==4:
            u=smooth(local/.65)
            place(im,self.scroll,(610,35+35*(1-u),595,555),alpha=u)
            if local>.7:text(im,'LÔI BỘ',(900,250),54,BLUE,True)
            if local>1.3:text(im,'ĐỨNG ĐẦU',(900,330),30,RED,True)
            if local>2.2:
                cloud(im,867,430,.5)
                d.line([(930,397),(912,427),(936,427),(916,453)],fill='#d4a347',width=6)
        elif idx==5 and local>.6:
            for x, numeral in [(560,'I'),(720,'II')]:
                d.ellipse((x-24,335,x+24,383),fill='#ba4b39')
                text(im,numeral,(x,358),22,'#fffdf8',True)
            text(im,'HAI ĐỜI VUA',(640,415),27,bold=True)
        elif idx==6:
            overlay=Image.new('RGBA',(W,H),(30,68,82,round(45*smooth(local/.6))))
            im=Image.alpha_composite(im,overlay);d=ImageDraw.Draw(im)
            for x,y,s in [(220,90,1.5),(620,55,1.6),(1040,100,1.5)]:cloud(im,x,y,s,'#9fb6be')
            progress=smooth((local-.45)/.7)
            for i in range(62):
                x=65+(i*83)%1170; y=160+((local*280+i*67)%440)
                if y<160+440*progress:d.line((x,y,x-8,y+22),fill='#d8f2ff',width=3)
            for i in range(10):
                phase=(local*1.4+i*.2)%1; x=80+i*125; y=530+(i%3)*20
                if progress>.5:d.ellipse((x-24*phase,y-5*phase,x+24*phase,y+5*phase),outline='#d5e7c3',width=2)
            if local>1.0:
                d.rounded_rectangle((350,220,930,286),radius=13,fill=(255,253,248,232))
                text(im,'MÂY MƯA → NUÔI VẠN VẬT',(640,253),29,BLUE,True)
            if local>2.7:
                text(im,'TRỪ GIAN · XÉT THIỆN ÁC',(640,337),25,'#fffdf8',True)
        elif idx==7:
            if local<2.8:
                arrow(im,curve((560,405),(440,460),(310,485)),smooth(local/.7),RED,5)
                if local>1.0:text(im,'KHÔNG GIỮ ĐƯỢC',(268,560),23,RED,True)
            else:
                arrow(im,curve((720,405),(850,460),(1000,475)),smooth((local-2.8)/.7),BLUE,5)
                if local>3.5:text(im,'CHỨC TRÁCH RỘNG HƠN',(1000,560),23,BLUE,True)
                cloud(im,1000,205,.75)
                for i in range(13):
                    x=850+i*24;y=265+((local*110+i*26)%170)
                    d.line((x,y,x-5,y+13),fill=BLUE,width=2)
        elif idx==8:
            pose='mo_den_13' if local<1.8 else 'mo_den_16'
            place(im,self.cat[pose],(60,125,405,450))
            if local>.6:arrow(im,curve((840,220),(900,255),(968,220)),smooth((local-.6)/.5),BLUE,4)
            if local>1.85:
                text(im,'NHÌN NHẬN PHẨM CHẤT',(900,460),32,BLUE,True)
                text(im,'CỦA MỘT ĐỐI THỦ',(900,510),30,RED,True)
        # Reserved subtitle band; no feet, prop or source label is hidden by it.
        d=ImageDraw.Draw(im);d.rectangle((0,626,W,H),fill='#fffdf8')
        if subtitles:
            cue=next((c for c in self.cues if c['in']<=t<c['out']),None)
            if cue:
                words=cue['text'].split();lines=['']
                for word in words:
                    test=(lines[-1]+' '+word).strip()
                    if d.textlength(test,font=font(24))>1160:lines.append(word)
                    else:lines[-1]=test
                text(im,'\n'.join(lines),(640,673),24,INK)
        if t>DURATION-.2:
            fade=Image.new('RGBA',(W,H),PAPER);im=Image.blend(im,fade,smooth((t-(DURATION-.2))/.2))
        return im.convert('RGB')


def prepare(trial):
    WORK.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
    shots=[{'in':a,'out':b,'name':n,'assets':s,'purpose':p} for a,b,n,s,p in SHOTS]
    (WORK/'shot_plan.json').write_text(json.dumps(shots,ensure_ascii=False,indent=2),encoding='utf-8')
    with (WORK/'shot_list.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=shots[0].keys());w.writeheader();w.writerows(shots)
    def stamp(t):
        ms=round(t*1000);s,ms=divmod(ms,1000);m,s=divmod(s,60);h,m=divmod(m,60)
        return f'{h:02}:{m:02}:{s:02},{ms:03}'
    (OUT/'demo.srt').write_text('\n\n'.join(f"{i+1}\n{stamp(c['in'])} --> {stamp(c['out'])}\n{c['text']}" for i,c in enumerate(trial.cues))+'\n',encoding='utf-8')
    snapshots=[.65,3.3,6.1,8.2,11.3,15.2,18.8,25.7,29.7]
    board=Image.new('RGB',(1440,900),'#eee9df');d=ImageDraw.Draw(board)
    for i,t in enumerate(snapshots):
        frame=trial.frame(t);frame.save(OUT/f'preview_{t:05.2f}.png')
        x=(i%3)*480;y=(i//3)*300;board.paste(frame.resize((480,270)),(x,y));d.text((x+8,y+273),f'{t:.2f}s',fill=INK,font=font(18))
    board.save(OUT/'contact_sheet.jpg',quality=94)
    paths=[PACK/(a+'.png') for a in ['Y02','Y02_B','B15','O01','O06']]
    paths+=[ROOT/'assets/characters/mo_den'/a['file'] for a in trial.cat_entries.values()]
    assets=[]
    for p in paths:
        role='character' if p.name.startswith(('Y02','mo_den')) else 'object_or_environment'
        assets.append({'file':str(p.relative_to(ROOT)),'sha256':sha(p),'role':role,'original_preserved':True,'source':'existing supplied library','human_motion':'static source pose, source-to-source cuts only' if p.name.startswith('Y02') else None})
    voice=VOICE/'Mo_Den_Phong_Than_Dien_Nghia_Custom_H_1_25x.wav'
    manifest={'kind':'user_requested_short_directing_trial','duration_seconds':DURATION,'fps':FPS,
              'full_film_rendered':False,'image_generation':False,'new_voice_generation':False,
              'voice_source':str(voice.relative_to(ROOT)),'voice_source_sha256':sha(voice),
              'source_excerpt':[START,END],'source_cues':[68,69,70,71,72,73],
              'speed_applied_to_excerpt':1.0,'existing_master_speed':1.25,'assets':assets,
              'review_status':'draft_for_user_review','human_rig_used':False,
              'note':'Composite sources and crops preserve supplied illustrations; no new human master or changed anatomy. This demo does not approve the long-form edit.'}
    (WORK/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')


def render(trial):
    audio=WORK/'H_existing_excerpt.wav'
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(START),'-i',str(VOICE/'Mo_Den_Phong_Than_Dien_Nghia_Custom_H_1_25x.wav'),'-t',str(END-START),'-af',f'apad=pad_dur=0.25,atrim=duration={DURATION}',str(audio)],check=True)
    video=OUT/'Mo_Den_Phong_Than_thu_dao_dien_32s.mp4'
    args=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{W}x{H}','-framerate',str(FPS),'-i','pipe:0','-i',str(audio),'-map','0:v','-map','1:a','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-t',str(DURATION),'-movflags','+faststart',str(video)]
    with (OUT/'encode.log').open('wb') as log:
        p=subprocess.Popen(args,stdin=subprocess.PIPE,stderr=log)
        for i in range(math.ceil(DURATION*FPS)):
            p.stdin.write(trial.frame(i/FPS).tobytes())
            if i%(FPS*5)==0:print(f'Rendered {i/FPS:.0f}/{DURATION:.1f}s',flush=True)
        p.stdin.close()
        if p.wait():raise RuntimeError('Video encode failed; see encode.log')
    print(str(video),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--render',action='store_true');args=parser.parse_args()
    trial=Trial();prepare(trial)
    if args.render:render(trial)
    else:print('Prepared board and source manifest; no video rendered.')
