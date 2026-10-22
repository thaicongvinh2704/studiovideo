"""Mỏ Đen V3: fixed-length two-bone forelimbs and independent supplied paws.

No image generation. Only the derivative forelimb connection is drawn; originals
and the rejected V1/V2 previews remain untouched. Not a production rig approval.
"""
import argparse
import json
import math
import os
from pathlib import Path
import subprocess
import time

import numpy as np
from PIL import Image
from scipy.ndimage import binary_dilation, binary_fill_holes, gaussian_filter, label
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import (QColor, QFontDatabase, QGuiApplication, QImage,
                           QLinearGradient, QPainter, QPainterPath, QPainterPathStroker, QPen)

import render_mo_den_motion_demo as base
import render_mo_den_rigid_demo as previous

WORK = base.ROOT/"projects/mo_den_motion_demo/articulated_v3"
OUT = base.ROOT/"outputs/mo_den_motion_demo_articulated_v3"
LEFT = [(0,0,0),(1,0,0),(1.8,-23,-13),(2.4,-28,-18),(3.4,-9,-5),
        (3.9,0,0),(8.6,0,0),(9.6,-18,-10),(10.7,-25,-14),
        (11.8,-11,-6),(12.7,0,0),(15,0,0)]
RIGHT = [(0,0,0),(4,0,0),(4.9,23,-12),(5.6,28,-17),(6.5,9,-4),
         (7.1,0,0),(9.15,0,0),(10.1,14,-8),(11.1,21,-12),
         (12.4,0,0),(15,0,0)]
SETTINGS = {
    "left": {"shoulder":(410,644),"wrist":(419,716),"pole":1,
             "paw_box":(382,682,487,785),"track":LEFT},
    "right":{"shoulder":(623,644),"wrist":(591,718),"pole":-1,
             "paw_box":(515,683,619,788),"track":RIGHT},
}


def target(track,t):
    return np.array([base.key_value([(a,x) for a,x,y in track],t),
                     base.key_value([(a,y) for a,x,y in track],t)])


def elbow_at(shoulder,wrist,pole,upper=55.,lower=50.):
    direction=wrist-shoulder
    distance=float(np.linalg.norm(direction))
    if not abs(upper-lower)+1 < distance < upper+lower-1:
        raise ValueError("Forelimb target unreachable; refuse to stretch bone")
    unit=direction/distance
    along=(upper*upper-lower*lower+distance*distance)/(2*distance)
    height=math.sqrt(max(0,upper*upper-along*along))
    return shoulder+unit*along+np.array([-unit[1],unit[0]])*height*pole


def limb_edges(shoulder,elbow,wrist):
    # A rounded centerline, tangent-continuous at the elbow. No joint circles.
    start=elbow+(shoulder-elbow)*.34
    end=elbow+(wrist-elbow)*.34
    a=np.linspace(0,1,18)[:,None]
    center=np.concatenate([
        shoulder+(start-shoulder)*a,
        (1-a[1:])**2*start+2*(1-a[1:])*a[1:]*elbow+a[1:]**2*end,
        end+(wrist-end)*a[1:]])
    tangent=np.gradient(center,axis=0)
    normal=np.stack([-tangent[:,1],tangent[:,0]],axis=1)
    normal/=np.linalg.norm(normal,axis=1)[:,None]
    distance=np.concatenate([[0],np.cumsum(np.linalg.norm(np.diff(center,axis=0),axis=1))])
    radius=np.interp(distance/distance[-1],[0,.55,1],[31,30,27])
    return center+normal*radius[:,None],center-normal*radius[:,None]


def polyline(points):
    p=QPainterPath(QPointF(*points[0]))
    for point in points[1:]:
        p.lineTo(*point)
    return p


def half_plane(point,direction):
    normal=np.array([-direction[1],direction[0]])*2048
    along=direction*2048
    region=polyline([point+normal,point-normal,point-normal+along,point+normal+along])
    region.closeSubpath()
    return region


def paw_texture(texture,rectangle):
    # Start with the brown fur component, then include its black contour.
    # Do not import the old forearm lines dangling above the wrist.
    arr=np.array(base.to_pil(texture))
    x0,y0,x1,y1=rectangle
    roi=arr[y0:y1,x0:x1]
    seed=(roi[:,:,0]>45)&(roi[:,:,0]<185)&(roi[:,:,1]>25)&(roi[:,:,1]<150)&(roi[:,:,3]>240)
    components,count=label(seed)
    if not count:
        raise ValueError("Missing supplied paw")
    sizes=np.bincount(components.ravel())
    sizes[0]=0
    region=components==sizes.argmax()
    region=binary_dilation(binary_fill_holes(region),iterations=5)
    coverage=np.zeros((1024,1024))
    coverage[y0:y1,x0:x1]=region
    coverage=gaussian_filter(coverage,.45)
    arr[:,:,3]=(arr[:,:,3]*coverage).astype(np.uint8)
    return base.to_qimage(Image.fromarray(arr))


class ArticulatedCat(previous.RigidCat):
    def __init__(self,original,cleaned,track):
        # Parent stores derived layers under the new work directory.
        super().__init__(original,cleaned,track)
        texture=original.scaled(1024,1024,Qt.AspectRatioMode.IgnoreAspectRatio,
                               Qt.TransformationMode.SmoothTransformation)
        self.paws={side:paw_texture(texture,config["paw_box"])
                   for side,config in SETTINGS.items()}
        for side,image in self.paws.items():
            image.save(str(WORK/f"{side}_supplied_paw.png"))

    def geometry(self,side,t):
        config=SETTINGS[side]
        shoulder=np.array(config["shoulder"],float)
        wrist=np.array(config["wrist"],float)+target(config["track"],t)
        elbow=elbow_at(shoulder,wrist,config["pole"])
        # A delayed, small wrist turn independent from the forearm rotation.
        displacement=target(config["track"],max(0,t-.11))
        angle=float(displacement[0])*.21
        return shoulder,elbow,wrist,angle

    def draw_arm(self,painter,side,t):
        shoulder,elbow,wrist,angle=self.geometry(side,t)
        centerline=QPainterPath(QPointF(*shoulder))
        centerline.quadTo(QPointF(*elbow),QPointF(*wrist))
        stroker=QPainterPathStroker()
        stroker.setWidth(59)
        stroker.setCapStyle(Qt.PenCapStyle.RoundCap)
        stroker.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        outline=stroker.createStroke(centerline).simplified()
        gradient=QLinearGradient(390,630,630,750)
        gradient.setColorAt(0,self.layers["body"].pixelColor(425,640))
        gradient.setColorAt(1,self.layers["body"].pixelColor(590,740))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(gradient)
        painter.drawPath(outline)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(base.INK,8.5,Qt.PenStyle.SolidLine,
                           Qt.PenCapStyle.RoundCap,Qt.PenJoinStyle.RoundJoin))
        rest=SETTINGS[side]["wrist"]
        # Draw only the continuous convex outer edge. Stroking both offset
        # edges of a very short bent limb creates crossing ink at the wrist.
        a=np.linspace(0,1,60)[:,None]
        center=(1-a)**2*shoulder+2*(1-a)*a*elbow+a*a*wrist
        tangent=2*(1-a)*(elbow-shoulder)+2*a*(wrist-elbow)
        normal=np.stack([-tangent[:,1],tangent[:,0]],axis=1)
        normal/=np.linalg.norm(normal,axis=1)[:,None]
        edge=center+normal*29.5*(1 if side=="left" else -1)
        painter.drawPath(polyline(edge))
        radians=math.radians(angle)
        rotate=np.array([[math.cos(radians),-math.sin(radians)],
                         [math.sin(radians),math.cos(radians)]])
        contact=np.array((443,691) if side=="left" else (568,691),float)
        contact=wrist+rotate@(contact-np.array(rest))
        crease_start=shoulder+np.array((22,11) if side=="left" else (-33,6))
        crease=QPainterPath(QPointF(*crease_start))
        crease.quadTo(QPointF(float(crease_start[0]),float(contact[1])),QPointF(*contact))
        painter.drawPath(crease)
        painter.save()
        painter.translate(float(wrist[0]),float(wrist[1]))
        painter.rotate(angle)
        painter.translate(-rest[0],-rest[1])
        painter.drawImage(0,0,self.paws[side])
        painter.restore()

    def at(self,t):
        image=QImage(1024,1024,QImage.Format.Format_ARGB32_Premultiplied)
        image.fill(Qt.GlobalColor.transparent)
        painter=QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.transformed(painter,self.layers["tail"],(708,840),3.5*math.sin(t*1.1))
        painter.drawImage(0,0,self.layers["body"])
        painter.drawImage(0,0,self.layers["feet"])
        self.draw_arm(painter,"left",t)
        self.draw_arm(painter,"right",t)
        face=base.to_qimage(base.texture_at(self.cleaned,self.original,self.track,t))
        head=previous.cutout(face,self.masks["head"])
        arr=np.array(base.to_pil(head))
        yy=np.arange(1024)[:,None]
        arr[:,:,3]=(arr[:,:,3]*(1-base.smooth(594,618,yy))).astype(np.uint8)
        self.transformed(painter,base.to_qimage(Image.fromarray(arr)),(516,596),
                         base.key_value(previous.HEAD_KEYS,t))
        painter.end()
        return image


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--previews-only",action="store_true")
    args=parser.parse_args()
    WORK.mkdir(parents=True,exist_ok=True)
    OUT.mkdir(parents=True,exist_ok=True)
    previous.WORK=WORK
    os.environ.setdefault("QT_QPA_PLATFORM","offscreen")
    app=QGuiApplication.instance() or QGuiApplication([])
    for filename in ("segoeui.ttf","seguisb.ttf"):
        if QFontDatabase.addApplicationFont(str(Path("C:/Windows/Fonts")/filename))<0:
            raise RuntimeError("Vietnamese font unavailable")
    library=json.loads((base.LIBRARY/"manifest.json").read_text(encoding="utf-8"))
    entry=next(a for a in library["assets"] if a["id"]=="mo_den_01")
    source=base.LIBRARY/entry["file"]
    if base.sha(source)!=entry["sha256"]:
        raise RuntimeError("Supplied original changed")
    original=QImage(str(source))
    cleaned=QImage(str(base.WORK/"face_clean_derivative.png")).scaled(1024,1024,
        Qt.AspectRatioMode.IgnoreAspectRatio,Qt.TransformationMode.SmoothTransformation)
    cat=ArticulatedCat(original,cleaned,base.MouthTrack())
    background=base.stage()
    times=[0,1.5,2.4,3.1,4.5,5.6,6.5,9.6,10.7,11.5,12.5,14.7]
    sheet=Image.new("RGB",(1920,810),"#faf7ef")
    for i,t in enumerate(times):
        frame=previous.frame_at(cat,background,t)
        frame.save(str(OUT/f"preview_{t:05.2f}.png"))
        sheet.paste(base.to_pil(frame).resize((480,270),Image.Resampling.LANCZOS),
                    ((i%4)*480,(i//4)*270))
    sheet.save(OUT/"contact_sheet.jpg",quality=95)
    if args.previews_only:
        print("V3 previews ready",flush=True)
        return
    evidence=[]
    for i in range(450):
        for side in SETTINGS:
            shoulder,elbow,wrist,angle=cat.geometry(side,i/30)
            lengths=[float(np.linalg.norm(elbow-shoulder)),float(np.linalg.norm(wrist-elbow))]
            if not np.allclose(lengths,[55,50],atol=1e-6):
                raise RuntimeError("Bone length changed")
            evidence.append({"frame":i,"side":side,"shoulder":shoulder.tolist(),
                "elbow":elbow.tolist(),"wrist":wrist.tolist(),"paw_angle":angle,"lengths":lengths})
    base.save_json(WORK/"joint_track.json",evidence)
    video=OUT/"Mo_Den_demo_15s_articulated_v3.mp4"
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
                frame=previous.frame_at(cat,background,i/30)
                process.stdin.write(bytes(frame.constBits()))
                if i%90==0:
                    print(f"V3 frame {i}/450: {time.monotonic()-started:.1f}s",flush=True)
            process.stdin.close()
            if process.wait():
                raise RuntimeError("Encode failed")
        except BaseException:
            process.kill()
            process.wait()
            raise
    base.save_json(WORK/"manifest.json",{
        "role":"character","kind":"two_bone_forelimb_draft_v3",
        "source":str(source.relative_to(base.ROOT)),"source_sha256":base.sha(source),
        "source_preserved":base.sha(source)==entry["sha256"],
        "video":str(video.relative_to(base.ROOT)),"video_sha256":base.sha(video),
        "audio":str((base.WORK/"audio_H_excerpt_15s.wav").relative_to(base.ROOT)),
        "audio_sha256":base.sha(base.WORK/"audio_H_excerpt_15s.wav"),"speed_reapplied":False,
        "code_sha256":base.sha(Path(__file__)),"fps":30,"frames":450,"seconds":15,
        "method":"Two fixed-length bones per forelimb, smooth vector connector, independent original paw texture with delayed wrist rotation. Body and hind feet fixed.",
        "bone_lengths":[55,50],"tracks":{"left":LEFT,"right":RIGHT},
        "wrist_delay_seconds":.11,"maximum_wrist_rotation_degrees":5.88,
        "image_generation_model":None,"production_approved":False,
        "visual_qc":"Pending inspection of current rendered frames",
        "realtime_audiovisual_qc":"Not independently certified",
        "render_seconds":round(time.monotonic()-started,2)})
    print(str(video),flush=True)


if __name__=="__main__":
    main()
