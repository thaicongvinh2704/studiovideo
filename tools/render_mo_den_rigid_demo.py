"""Second draft: rigid cutout transforms, no mesh/stretch of the supplied cat.

Uses the V1 face preparation/cue track; originals and V1 output remain unchanged.
Body occlusion plate is manually drawn from the supplied silhouette. No AI images.
"""
import argparse
import json
import math
import os
from pathlib import Path
import subprocess
import time
import numpy as np
from scipy.ndimage import binary_dilation, binary_fill_holes, gaussian_filter

from PySide6.QtCore import Qt, QPointF, QRectF
from PySide6.QtGui import (QColor, QGuiApplication, QFontDatabase, QImage, QPainter,
                           QPainterPath, QPen, QLinearGradient, QTransform)
from PIL import Image

import render_mo_den_motion_demo as base

WORK = base.ROOT / "projects/mo_den_motion_demo/rigid_v2"
OUT = base.ROOT / "outputs/mo_den_motion_demo_rigid_v2"
LEFT_KEYS = [(0,0),(.65,0),(1.25,60),(2.5,60),(3.25,0),(8.65,0),
             (9.4,48),(11.65,48),(12.6,0),(15,0)]
RIGHT_KEYS = [(0,0),(3.8,0),(4.45,-58),(6.0,-58),(6.8,0),(8.65,0),
              (9.4,-48),(11.65,-48),(12.6,0),(15,0)]
HEAD_KEYS = [(0,0),(.65,0),(1.3,-1.5),(2.5,-1.5),(3.25,0),(4.5,1.5),
             (6.1,1.5),(6.8,0),(8.65,0),(9.4,-2.2),(11.65,-2.2),(12.6,0),(15,0)]


def path(start, segments):
    result = QPainterPath(QPointF(*start))
    for segment in segments:
        if len(segment)==2:
            result.lineTo(*segment)
        else:
            result.cubicTo(*segment)
    result.closeSubpath()
    return result


def masks():
    return {
        "head": path((0,0), [(1024,0),(1024,560),(690,560),
            (666,581,630,588,612,588),(604,616),(426,616),(422,593),
            (355,592,322,579,300,560),(0,560)]),
        "left_arm": path((390,627), [(414,630,428,637,433,650),
            (431,666,439,680,447,689),(473,700,485,739,474,759),
            (454,786,406,781,393,750),(369,741,354,727,354,704),
            (355,674,372,643,390,627)]),
        "right_arm": path((618,621), [(647,647,671,678,684,702),
            (666,725,648,740,613,751),(601,779,568,791,542,776),
            (514,766,514,740,533,715),(544,699,557,693,569,690),
            (581,674,587,660,590,650),(597,632,605,621,618,621)]),
        "tail": path((695,852), [(745,851,796,813,821,767),
            (858,712,856,646,825,607),(794,566,748,568,722,584),
            (688,603,680,643,704,663),(724,680,749,669,763,658),
            (781,710,748,755,711,783),(695,852)]),
        "feet": path((352,867), [(353,842,380,813,412,817),
            (443,813,474,832,474,859),(480,894,432,898,392,893),
            (364,892,347,887,352,867)]).united(path((546,864),[
            (548,839,572,815,601,816),(635,813,662,828,671,851),
            (685,887,658,897,624,894),(576,896,541,893,546,864)])),
    }


def cutout(texture, mask):
    layer = QImage(1024,1024,QImage.Format.Format_ARGB32_Premultiplied)
    layer.fill(Qt.GlobalColor.transparent)
    painter = QPainter(layer)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setClipPath(mask)
    painter.drawImage(0,0,texture)
    painter.end()
    return layer


def body_plate(texture):
    # Hidden neck and chest regions completed once, behind preserved cutouts.
    layer = QImage(1024,1024,QImage.Format.Format_ARGB32_Premultiplied)
    layer.fill(Qt.GlobalColor.transparent)
    painter = QPainter(layer)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    outline = path((421,563), [(477,555,577,550,611,570),
        (651,610,672,658,685,701),(712,730,729,773,720,811),
        (716,850,686,875,647,878),(392,877),
        (348,875,328,847,329,804),(328,774,343,745,359,722),
        (358,686,373,634,402,595),(421,563)])
    painter.setBrush(Qt.GlobalColor.white)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawPath(outline)
    painter.end()
    # Fit original cream fur only. Reconstruct hidden chest deterministically,
    # retaining the same broad colour surface as the source neck and legs.
    rgb=np.asarray(base.to_pil(texture)).astype(float)
    yy,xx=np.mgrid[:1024,:1024]
    x=(xx-520)/200
    y=(yy-730)/200
    design=np.stack([np.ones_like(x),x,y,x*x,x*y,y*y],axis=-1)
    samples=(yy>565)&(yy<885)&(xx>350)&(xx<720)&(rgb[:,:,3]>250)&(rgb[:,:,0]>210)&(rgb[:,:,1]>160)&(rgb[:,:,2]<220)
    coefficients=np.linalg.lstsq(design[samples],rgb[:,:,:3][samples],rcond=None)[0]
    arr=np.array(base.to_pil(layer))
    arr[:,:,:3]=np.clip(design@coefficients,0,255).astype(np.uint8)
    layer=base.to_qimage(Image.fromarray(arr))
    painter=QPainter(layer)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setPen(QPen(base.INK,9,Qt.PenStyle.SolidLine,
                       Qt.PenCapStyle.RoundCap,Qt.PenJoinStyle.RoundJoin))
    painter.setBrush(Qt.BrushStyle.NoBrush)
    side=QPainterPath(QPointF(404,594))
    side.cubicTo(398,604,392,616,389,625)
    side.cubicTo(366,664,356,696,359,722)
    side.cubicTo(343,745,328,774,329,804)
    side.cubicTo(328,847,348,875,392,877)
    side.lineTo(647,878)
    side.cubicTo(686,875,716,850,720,811)
    side.cubicTo(729,773,712,730,685,701)
    side.cubicTo(679,672,663,641,651,624)
    side.cubicTo(644,608,637,596,632,588)
    painter.drawPath(side)
    painter.end()
    return layer


def fade_overlap(layer,start,end):
    arr=np.array(base.to_pil(layer))
    yy=np.arange(1024)[:,None]
    factor=base.smooth(start,end,yy)
    arr[:,:,3]=(arr[:,:,3]*factor).astype(np.uint8)
    return base.to_qimage(Image.fromarray(arr))


def brown_cutout(texture,rectangle):
    arr=np.array(base.to_pil(texture))
    x0,y0,x1,y1=rectangle
    mask=np.zeros((1024,1024),bool)
    roi=arr[y0:y1,x0:x1]
    mask[y0:y1,x0:x1]=(roi[:,:,0]<185)&(roi[:,:,1]<150)&(roi[:,:,3]>200)
    mask=binary_dilation(binary_fill_holes(mask),iterations=1)
    coverage=gaussian_filter(mask.astype(float),.45)
    arr[:,:,3]=(arr[:,:,3]*coverage).astype(np.uint8)
    return base.to_qimage(Image.fromarray(arr))


def complete_arm(texture,body,side):
    layer=QImage(1024,1024,QImage.Format.Format_ARGB32_Premultiplied)
    layer.fill(Qt.GlobalColor.transparent)
    painter=QPainter(layer)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    gradient=QLinearGradient(390,630,630,750)
    gradient.setColorAt(0,body.pixelColor(425,640))
    gradient.setColorAt(1,body.pixelColor(590,740))
    painter.setBrush(gradient)
    painter.setPen(Qt.PenStyle.NoPen)
    if side=="left_arm":
        outline=path((389,625),[(372,648,354,680,354,703),
            (353,725,374,739,394,744),(445,691),
            (436,679,432,665,432,655),(430,636,408,617,389,625)])
        edges=QPainterPath(QPointF(389,625))
        edges.cubicTo(372,648,354,680,354,703)
        edges.cubicTo(353,725,374,739,394,744)
        edges.moveTo(432,655)
        edges.cubicTo(432,665,436,679,445,691)
        paw=brown_cutout(texture,(384,686,485,784))
    else:
        outline=path((569,641),[(591,622,617,635,622,659),
            (628,685,615,711,604,741),(534,731),
            (539,699,552,670,569,641)])
        edges=QPainterPath(QPointF(622,659))
        edges.cubicTo(628,685,615,711,604,741)
        edges.moveTo(569,650)
        edges.cubicTo(559,671,549,687,545,704)
        paw=brown_cutout(texture,(517,687,617,785))
    painter.drawPath(outline)
    painter.setBrush(Qt.BrushStyle.NoBrush)
    painter.setPen(QPen(base.INK,9,Qt.PenStyle.SolidLine,
                       Qt.PenCapStyle.RoundCap,Qt.PenJoinStyle.RoundJoin))
    painter.drawPath(edges)
    painter.drawImage(0,0,paw)
    painter.end()
    return layer


class RigidCat:
    def __init__(self, original, cleaned, track):
        self.original, self.cleaned, self.track = original, cleaned, track
        self.masks = masks()
        texture = original.scaled(1024,1024,Qt.AspectRatioMode.IgnoreAspectRatio,
                                  Qt.TransformationMode.SmoothTransformation)
        self.layers = {name:cutout(texture,mask) for name,mask in self.masks.items()
                       if name!="head"}
        self.layers["body"] = body_plate(texture)
        for side in ("left_arm","right_arm"):
            self.layers[side]=complete_arm(texture,self.layers["body"],side)
        self.layers["feet"]=brown_cutout(self.layers["feet"],(345,812,681,898))
        for name,layer in self.layers.items():
            layer.save(str(WORK/f"{name}.png"))

    @staticmethod
    def transformed(painter, image, pivot, angle):
        painter.save()
        painter.translate(*pivot)
        painter.rotate(angle)
        painter.translate(-pivot[0],-pivot[1])
        painter.drawImage(0,0,image)
        painter.restore()

    def at(self,t):
        image = QImage(1024,1024,QImage.Format.Format_ARGB32_Premultiplied)
        image.fill(Qt.GlobalColor.transparent)
        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.transformed(painter,self.layers["tail"],(708,840),
                         3.5*math.sin(t*1.1))
        painter.drawImage(0,0,self.layers["body"])
        painter.drawImage(0,0,self.layers["feet"])
        self.transformed(painter,self.layers["left_arm"],(402,644),
                         base.key_value(LEFT_KEYS,t))
        self.transformed(painter,self.layers["right_arm"],(590,644),
                         base.key_value(RIGHT_KEYS,t))
        face = base.to_qimage(base.texture_at(self.cleaned,self.original,self.track,t))
        head = cutout(face,self.masks["head"])
        arr=np.array(base.to_pil(head))
        yy=np.arange(1024)[:,None]
        arr[:,:,3]=(arr[:,:,3]*(1-base.smooth(594,618,yy))).astype(np.uint8)
        head=base.to_qimage(Image.fromarray(arr))
        self.transformed(painter,head,(516,596),base.key_value(HEAD_KEYS,t))
        painter.end()
        return image


def frame_at(cat,background,t):
    image = background.copy()
    painter = QPainter(image)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(QColor(77,61,37,25))
    painter.drawEllipse(QRectF(760,914,420,15))
    painter.drawImage(410,28,cat.at(t))
    painter.end()
    return image


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--previews-only",action="store_true")
    args=parser.parse_args()
    WORK.mkdir(parents=True,exist_ok=True)
    OUT.mkdir(parents=True,exist_ok=True)
    os.environ.setdefault("QT_QPA_PLATFORM","offscreen")
    app=QGuiApplication.instance() or QGuiApplication([])
    for filename in ("segoeui.ttf","seguisb.ttf"):
        if QFontDatabase.addApplicationFont(str(Path("C:/Windows/Fonts")/filename))<0:
            raise RuntimeError("Font unavailable")
    library=json.loads((base.LIBRARY/"manifest.json").read_text(encoding="utf-8"))
    entry=next(a for a in library["assets"] if a["id"]=="mo_den_01")
    source=base.LIBRARY/entry["file"]
    assert base.sha(source)==entry["sha256"]
    original=QImage(str(source))
    # V1 derivative is independently kept; this renderer does not replace it.
    cleaned=QImage(str(base.WORK/"face_clean_derivative.png")).scaled(1024,1024,
        Qt.AspectRatioMode.IgnoreAspectRatio,Qt.TransformationMode.SmoothTransformation)
    cat=RigidCat(original,cleaned,base.MouthTrack())
    background=base.stage()
    times=[0,1.72,2.2,4.8,5.94,7,9.8,11.2,14.7]
    sheet=Image.new("RGB",(1440,810),"#faf7ef")
    for i,t in enumerate(times):
        frame=frame_at(cat,background,t)
        frame.save(str(OUT/f"preview_{t:05.2f}.png"))
        sheet.paste(base.to_pil(frame).resize((480,270),Image.Resampling.LANCZOS),
                    ((i%3)*480,(i//3)*270))
    sheet.save(OUT/"contact_sheet.jpg",quality=95)
    if args.previews_only:
        print("Rigid previews ready",flush=True)
        return
    video=OUT/"Mo_Den_demo_15s_rigid_v2.mp4"
    command=["ffmpeg","-v","error","-y","-f","rawvideo","-pixel_format","rgb24",
        "-video_size","1920x1080","-framerate","30","-i","pipe:0","-i",
        str(base.WORK/"audio_H_excerpt_15s.wav"),"-map","0:v:0","-map","1:a:0",
        "-c:v","libx264","-preset","fast","-crf","18","-pix_fmt","yuv420p",
        "-c:a","aac","-b:a","192k","-t","15","-movflags","+faststart",str(video)]
    started=time.monotonic()
    with (OUT/"encode.log").open("w") as log:
        process=subprocess.Popen(command,stdin=subprocess.PIPE,stderr=log)
        try:
            for i in range(450):
                frame=frame_at(cat,background,i/30)
                process.stdin.write(bytes(frame.constBits()))
                if i%90==0:
                    print(f"Rigid frame {i}/450: {time.monotonic()-started:.1f}s",flush=True)
            process.stdin.close()
            if process.wait():
                raise RuntimeError("Encoder failed")
        except BaseException:
            process.kill()
            process.wait()
            raise
    base.save_json(WORK/"manifest.json",{
        "role":"character","kind":"rigid_cutout_draft_v2","source":str(source.relative_to(base.ROOT)),
        "source_sha256":base.sha(source),"source_preserved":base.sha(source)==entry["sha256"],
        "video":str(video.relative_to(base.ROOT)),"video_sha256":base.sha(video),
        "audio":str((base.WORK/"audio_H_excerpt_15s.wav").relative_to(base.ROOT)),
        "audio_sha256":base.sha(base.WORK/"audio_H_excerpt_15s.wav"),"speed_reapplied":False,
        "code_sha256":base.sha(Path(__file__)),"fps":30,"frames":450,"seconds":15,
        "method":"Rigid rotations about shoulder/head/tail pivots. No mesh or nonuniform scale.",
        "artwork":"Supplied head, forearms, feet and tail cutouts; manually completed hidden neck/chest silhouette and cream fill.",
        "left_arm_keyframes":LEFT_KEYS,"right_arm_keyframes":RIGHT_KEYS,"head_keyframes":HEAD_KEYS,
        "hind_feet":"Fixed seated support; do not animate as a walking pose.",
        "production_approved":False,"visual_qc":"Pending current rendered inspection",
        "listening_qc":"Not independently certified", "render_seconds":round(time.monotonic()-started,2)})
    print(str(video),flush=True)


if __name__=="__main__":
    main()
