"""QPainter vector renderer shared by preview and export."""
import math
import json
from pathlib import Path
from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import QImage, QImageReader, QPainter, QPen, QColor, QPainterPath, QFont, QLinearGradient, QFontMetricsF, QTransform, QPolygonF
from .animation import skeleton, state, attachment, PARENTS, sample, evaluate_scene, camera_values, stepped, active_motion, age_at, motion_pose
from .project import scene_at, resolve
from .subtitles import active
from .illustration import graphic, illustrated_character, animated_opacity

class Renderer:
    def __init__(self):
        self.cache = {}
        self.image_stamps = {}
        self.vectors = {}
        self.last_frame_key=None;self.last_frame=None

    def vector(self,root,filename):
        from PySide6.QtSvg import QSvgRenderer
        path=str(resolve(root,filename));stamp=Path(path).stat().st_mtime_ns
        key=(path,stamp)
        if key not in self.vectors:
            svg=QSvgRenderer(path);svg.setAnimationEnabled(False)
            if not svg.isValid():raise ValueError('SVG không hợp lệ: '+path)
            self.vectors[key]=svg
            while len(self.vectors)>48:self.vectors.pop(next(iter(self.vectors)))
        return self.vectors[key]

    def image(self, root, filename):
        path = str(resolve(root,filename))
        stamp=Path(path).stat().st_mtime_ns
        if self.image_stamps.get(path)!=stamp:self.cache.pop(path,None);self.image_stamps[path]=stamp
        if path not in self.cache:
            if Path(path).suffix.lower()=='.svg':
                from PySide6.QtSvg import QSvgRenderer
                svg=QSvgRenderer(path)
                if not svg.isValid():raise ValueError('SVG không hợp lệ: '+path)
                size=svg.defaultSize();size.scale(2048,2048,Qt.AspectRatioMode.KeepAspectRatio)
                im=QImage(size,QImage.Format.Format_ARGB32_Premultiplied);im.fill(Qt.GlobalColor.transparent)
                painter=QPainter(im);svg.render(painter);painter.end()
            else:
                reader=QImageReader(path);reader.setAutoTransform(True);im=reader.read()
            if im.isNull(): raise FileNotFoundError('Ảnh không đọc được: '+path)
            self.cache[path] = im
            while len(self.cache)>1 and (len(self.cache)>24 or sum(i.sizeInBytes() for i in self.cache.values())>128*1024**2):
                self.cache.pop(next(iter(self.cache)))
        return self.cache[path]


    def frame(self,project,root,time,width=None,height=None,burn=True,rig=False,effects=True):
        width,height=width or project['width'],height or project['height']
        image=QImage(width,height,QImage.Format.Format_RGB888);image.fill(QColor('#f4f3ee'))
        p=QPainter(image)
        p.setRenderHints(QPainter.RenderHint.Antialiasing|QPainter.RenderHint.TextAntialiasing|QPainter.RenderHint.SmoothPixmapTransform)
        scale=min(width/1280,height/720);p.translate((width-1280*scale)/2,(height-720*scale)/2);p.scale(scale,scale)
        s,t=scene_at(project,time)
        if s:
            poses=evaluate_scene(s['objects'],t)
            from .hierarchy import world_states,transform_point
            world=world_states(s['objects'],t)
            # Reuse a held composition exactly; changed poses, source files, camera,
            # expressions, blinks and edits invalidate it. Never cache a whole film.
            dynamics=[];stamps=[]
            for obj in s['objects']:
                entry=[obj['id'],world[obj['id']],animated_opacity(obj,t)]
                if obj['kind']=='character':
                    entry.append(poses[obj['id']])
                    if obj.get('skin')=='ink' and obj.get('character_design')=='reference_black':
                        from .ink_character import face_values
                        entry.append(face_values(obj,t))
                    if obj.get('skin')=='ink':entry.extend([stepped(obj.get('poses',[]),t,obj.get('pose','rest')),stepped(obj.get('expressions',[]),t,obj.get('expression','happy')),
                        (t+obj.get('blink_offset',1.2))%4.9<.11,sample(obj.get('keys',{}).get('gaze',[]),t,obj.get('gaze',0)),sample(obj.get('keys',{}).get('face_tilt',[]),t,0),sample(obj.get('keys',{}).get('bone_head',[]),t,0)])
                    else:entry.append(t)
                if obj.get('reveal'):entry.append(min(1,max(0,(t-obj.get('start',0))/max(.001,obj.get('enter_duration',1)))))
                dynamics.append(entry)
                if obj.get('file'):
                    file=resolve(root,obj['file']);stamps.append((str(file),file.stat().st_mtime_ns))
            if s.get('background_file'):
                file=resolve(root,s['background_file']);stamps.append((str(file),file.stat().st_mtime_ns))
            key=json.dumps([width,height,str(root),s,dynamics,camera_values(s,t),stamps,burn,rig,effects,
                            active(project['subtitles'],time) if burn else None,project['subtitle_style'],t if s.get('effects') or s.get('insert') else None],sort_keys=True)
            if key==self.last_frame_key and self.last_frame is not None:
                p.end();return QImage(self.last_frame)
            p.save();z,x,y=camera_values(s,t)
            shake=1.5*math.sin(t*45) if effects and 'shake' in s['effects'] else 0
            p.translate(640+shake,360);p.scale(z,z);p.translate(-x,-y)
            self.background(p,s,root)
            if effects:self.world_effects(p,s,t,poses,False)
            ordered=sorted(s['objects'],key=lambda o:o.get('layer',10))
            for o in ordered:
                st=world[o['id']]
                if not st['visible'] or o['kind']=='group':continue
                if o.get('attachment') and o['kind'] in ('image','shape','text'):
                    anchor=attachment(o,s['objects'],t,poses)
                    if anchor:st={**st,'x':anchor[0],'y':anchor[1]}
                p.save();local_op=state(o,t)['opacity'];alpha=animated_opacity(o,t)
                p.setOpacity(st['opacity']*(alpha/local_op if local_op else 0))
                if o['kind']=='character':self.character(p,o,t,rig,poses[o['id']])
                elif o['kind'] in ('text','shape') or o['kind']=='image' and 'width' in o:graphic(p,o,t,root,self,st)
                else:
                    proxy=o
                    if o.get('parent'):
                        proxy={**o,**{k:st[k] for k in ('x','y','scale','rotation','opacity')}}
                        proxy['keys']={k:v for k,v in o.get('keys',{}).items() if k not in ('x','y','scale','rotation','opacity')}
                    self.prop(p,proxy,s['objects'],t,root,poses)
                p.restore()
            # Front arms and fingers cross in front of held objects / partners.
            for o in ordered:
                if o['kind']=='character' and o.get('skin')=='ink' and poses[o['id']][1]['visible']:
                    held=[a for a in ordered if a.get('attachment') and state(a,t)['visible'] and
                          next((b.get('character') for b in reversed(sorted(a['attachment'],key=lambda b:b['t'])) if b['t']<=t),None)==o['id']]
                    if held:
                        from .ink_character import draw_hand
                        js,st=poses[o['id']];p.save();p.setOpacity(st['opacity'])
                        for side in ('l','r'):draw_hand(p,js['hand_'+side],js['elbow_'+side],st['scale'],'grip',QColor(o.get('color','#191d20')),QColor(o.get('skin_color','#ffdbb5')))
                        p.restore()
                if o['kind']=='character' and o.get('skin') not in ('illustrated','ink') and poses[o['id']][1]['visible']:
                    p.save();p.setOpacity(poses[o['id']][1]['opacity'])
                    self.front_arms(p,o,t,poses[o['id']]);p.restore()
            if effects:self.world_effects(p,s,t,poses,True)
            p.restore()
            if s.get('insert') and s['insert']['start']<=t<s['insert']['end']:
                self.insert(p,s['insert'],t)
            if effects:self.screen_effects(p,s,t)
        if burn and project['subtitle_style'].get('enabled',True):
            text=active(project['subtitles'],time)
            if text:self.subtitle(p,text,project['subtitle_style'])
        p.end()
        if s:self.last_frame_key=key;self.last_frame=QImage(image)
        return image

    def subtitle(self,p,text,style):
        font=QFont(style.get('font','Segoe UI'));font.setPixelSize(style.get('size',28));font.setWeight(QFont.Weight.Medium)
        p.setFont(font);fm=QFontMetricsF(font);max_width=1000
        lines=[];line=''
        for word in text.split():
            candidate=(line+' '+word).strip()
            if line and fm.horizontalAdvance(candidate)>max_width:lines.append(line);line=word
            else:line=candidate
        if line:lines.append(line)
        h=len(lines)*fm.lineSpacing()+20;w=min(1080,max(fm.horizontalAdvance(x) for x in lines)+44)
        bottom=min(704,720*style.get('y',.95));rect=QRectF((1280-w)/2,bottom-h,w,h)
        p.setPen(Qt.PenStyle.NoPen)
        if style.get('background',True):
            p.setBrush(QColor(24,30,33,210));p.drawRoundedRect(rect,9,9)
        p.setPen(QColor(style.get('color','#ffffff')))
        p.drawText(rect,Qt.AlignmentFlag.AlignCenter,'\n'.join(lines))

    def background(self,p,s,root):
        if s.get('background')=='white':
            p.fillRect(QRectF(-3000,-2000,7000,5000),QColor(s.get('background_color','#ffffff')));return
        if s.get('background_file'):
            im=self.image(root,s['background_file']);p.drawImage(QRectF(0,0,1280,720),im);return
        name=s.get('background','studio');rain='rain' in s.get('effects',[])
        gradient=QLinearGradient(0,120,0,620)
        gradient.setColorAt(0,QColor('#dfe4e2' if rain else '#f7f5ef'))
        gradient.setColorAt(1,QColor('#f0f1eb' if rain else '#ebe9e0'))
        p.fillRect(QRectF(-3000,-2000,7000,5000),gradient)
        pen=lambda c,w:QPen(QColor(c),w,Qt.PenStyle.SolidLine,Qt.PenCapStyle.RoundCap,Qt.PenJoinStyle.RoundJoin)
        if name in ('rain','street'):
            # Two restrained depth planes, all in the scene's world coordinates.
            for x,h,w in [(-280,200,155),(-50,245,180),(190,145,130),(950,210,160),(1180,270,180),(1440,170,150)]:
                p.setPen(pen('#c7cfcb',1.8));p.setBrush(QColor('#e5e9e4'))
                p.drawRect(QRectF(x,575-h,w,h))
                for dx in (20,w-45):
                    for yy in range(int(595-h),540,45):
                        p.setBrush(QColor('#f5f4ed'));p.drawRect(QRectF(x+dx,yy,25,26))
            for x in (80,1070):
                p.setPen(pen('#aab4ae',4));p.drawLine(QPointF(x,575),QPointF(x,330))
                p.drawLine(QPointF(x,330),QPointF(x+40,330));p.setBrush(QColor('#edf0e9'))
                p.drawRoundedRect(QRectF(x+25,325,38,16),5,5)
            p.setPen(pen('#b9c2bc',2));p.drawLine(QPointF(-2500,555),QPointF(3500,555))
        elif name in ('home','room'):
            p.setPen(pen('#d3d4ca',2));p.setBrush(QColor('#edece3'))
            p.drawRect(QRectF(-180,150,1710,425))
            # Window, sill and curtain; a recognizable home, without dense detail.
            p.setPen(pen('#9fa9a1',3));p.setBrush(QColor('#e0e6df'))
            p.drawRoundedRect(QRectF(250,260,140,180),4,4)
            p.drawLine(QPointF(320,260),QPointF(320,440));p.drawLine(QPointF(250,350),QPointF(390,350))
            p.drawLine(QPointF(235,448),QPointF(405,448))
            p.setPen(pen('#909a92',4));p.setBrush(QColor('#d3d8cc'))
            p.drawRect(QRectF(875,245,150,330));p.setBrush(QColor('#737d74'))
            p.drawRect(QRectF(892,263,116,312));p.setPen(pen('#c4c9bd',2))
            p.drawRect(QRectF(908,288,83,110));p.drawRect(QRectF(908,420,83,132))
            p.setBrush(QColor('#d9c784'));p.drawEllipse(QPointF(985,420),4,4)
            p.setPen(pen('#afb6aa',4));p.drawLine(QPointF(220,225),QPointF(1060,225))
            p.drawLine(QPointF(190,225),QPointF(640,125));p.drawLine(QPointF(640,125),QPointF(1080,225))
            for x in (450,1100):
                p.setPen(pen('#8d9a89',3));p.setBrush(QColor('#b6c1ac'))
                p.drawEllipse(QRectF(x-16,505,30,45));p.drawEllipse(QRectF(x+8,492,26,45))
                p.setBrush(QColor('#afb3a1'));p.drawRoundedRect(QRectF(x-10,540,38,35),3,3)
            if name=='room':
                p.setPen(pen('#a1a99c',3));p.setBrush(QColor('#dadbce'))
                p.drawRoundedRect(QRectF(470,470,230,15),3,3)
                p.drawLine(QPointF(485,485),QPointF(485,575));p.drawLine(QPointF(685,485),QPointF(685,575))
        p.setPen(Qt.PenStyle.NoPen);p.setBrush(QColor('#d7ded8' if rain else '#e2e1d6'))
        p.drawRect(QRectF(-3000,575,7000,2000))
        p.setPen(pen('#9da99f',2));p.drawLine(QPointF(-3000,575),QPointF(4000,575))
        for x,y,w in s.get('puddles',[[600,592,160]] if name in ('rain','street') else []):
            p.setPen(pen('#aabbb5',1.5));p.setBrush(QColor('#c7d6d0'))
            p.drawEllipse(QRectF(x-w/2,y-7,w,14));p.setPen(pen('#edf0e8',2))
            p.drawLine(QPointF(x-w*.3,y-2),QPointF(x+w*.15,y-2))

    def character(self,p,o,t,rig=False,pose_data=None):
        joints,st=pose_data or skeleton(o,t);sc=st['scale'];color=o.get('color','#303932')
        if o.get('skin')=='ink':
            from .ink_character import draw
            draw(p,o,t,joints,st)
            if rig:
                p.setPen(QPen(QColor('#168a8b'),1));p.setBrush(QColor('#f7d35b'))
                for point in joints.values():p.drawEllipse(QPointF(*point),3,3)
            return
        if o.get('skin')=='illustrated':
            illustrated_character(p,o,t,joints,st)
            if rig:
                p.setPen(QPen(QColor('#168a8b'),1));p.setBrush(QColor('#f7d35b'))
                for point in joints.values():p.drawEllipse(QPointF(*point),3,3)
            return
        # Soft vector contact shadow shrinks with jump height.
        feet=[joints['foot_l'],joints['foot_r']];height=max(0,st['y']-max(v[1] for v in feet))
        size=max(.45,1-height/180)
        for expand,alpha in ((1.4,7),(1.15,11),(1,15)):
            p.setPen(Qt.PenStyle.NoPen);p.setBrush(QColor(48,60,49,alpha))
            p.drawEllipse(QRectF(st['x']-32*sc*size*expand,st['y']-3*sc*expand,64*sc*size*expand,7*sc*expand))
        pen=QPen(QColor(color),5.2*sc,Qt.PenStyle.SolidLine,Qt.PenCapStyle.RoundCap,Qt.PenJoinStyle.RoundJoin)
        p.setPen(pen)
        for joint,parent in PARENTS.items():
            if joint in ('head','shoulder_l','shoulder_r'):continue
            p.drawLine(QPointF(*joints[parent]),QPointF(*joints[joint]))
        p.drawLine(QPointF(*joints['shoulder_l']),QPointF(*joints['shoulder_r']))
        hx,hy=joints['head'];radius=(22 if age_at(o,t)=='child' else 24)*sc
        p.drawLine(QPointF(*joints['neck']),QPointF(hx,hy+radius*.8))
        p.setBrush(QColor('#faf8f0'));p.drawEllipse(QPointF(hx,hy),radius,radius)
        p.save();tilt=sample(o.get('keys',{}).get('bone_head',[]),t,motion_pose(o,t)['head'])
        p.translate(hx,hy);p.rotate(math.degrees(tilt)*.65);p.translate(-hx,-hy)
        hair='#a1a89d' if age_at(o,t)=='elderly' else color
        p.setPen(QPen(QColor(hair),3.7*sc,Qt.PenStyle.SolidLine,Qt.PenCapStyle.RoundCap))
        p.drawArc(QRectF(hx-radius*.87,hy-radius*.95,radius*1.74,radius*1.45),25*16,125*16)
        if o.get('preset')=='mother':
            p.setBrush(QColor(hair));p.drawEllipse(QPointF(hx-radius-3*sc,hy-9*sc),8*sc,11*sc)
        elif o.get('preset')=='son':
            p.drawLine(QPointF(hx-10*sc,hy-22*sc),QPointF(hx-3*sc,hy-29*sc))
        ex=stepped(o.get('expressions',[]),t,o.get('expression','normal'))
        gaze=sample(o.get('keys',{}).get('gaze',[]),t,o.get('gaze',0))*sc
        gaze=max(-5*sc,min(5*sc,gaze));ey=hy-2*sc
        blink=(t+sum(ord(c) for c in o.get('character_id',o['preset']))*.137)%4.3<.12
        p.setPen(QPen(QColor(color),2.2*sc,Qt.PenStyle.SolidLine,Qt.PenCapStyle.RoundCap))
        for dx in (-8,8):
            if blink:p.drawLine(QPointF(hx+(dx-3)*sc,ey),QPointF(hx+(dx+3)*sc,ey))
            elif ex=='happy':p.drawArc(QRectF(hx+(dx-3)*sc+gaze,ey-2*sc,6*sc,5*sc),0,180*16)
            else:p.drawPoint(QPointF(hx+dx*sc+gaze,ey))
        mouth=QRectF(hx-8*sc,hy+3*sc,16*sc,10*sc)
        if ex=='happy':p.drawArc(mouth,180*16,180*16)
        elif ex in ('sad','worried'):p.drawArc(mouth,0,180*16)
        elif ex=='surprised':p.drawEllipse(QPointF(hx,hy+9*sc),3*sc,4*sc)
        else:p.drawLine(QPointF(hx-5*sc,hy+9*sc),QPointF(hx+5*sc,hy+9*sc))
        if ex in ('sad','worried','angry'):
            tilt=-3 if ex=='angry' else 3
            for sign in (-1,1):p.drawLine(QPointF(hx+sign*5*sc,hy-11*sc),QPointF(hx+sign*13*sc,hy+(-11+tilt)*sc))
        if age_at(o,t)=='elderly':
            p.setPen(QPen(QColor('#9aa494'),1.2*sc))
            for sign in (-1,1):p.drawLine(QPointF(hx+sign*13*sc,hy+2*sc),QPointF(hx+sign*17*sc,hy+4*sc))
        if active_motion(o,t)[0]=='cry':
            p.setBrush(QColor('#a3c4c0'));p.setPen(Qt.PenStyle.NoPen)
            p.drawEllipse(QPointF(hx+12*sc,hy+(7+(t*18)%12)*sc),2*sc,3*sc)
        p.restore()
        if rig:
            p.setPen(QPen(QColor('#168a8b'),1));p.setBrush(QColor('#f7d35b'))
            for point in joints.values():p.drawEllipse(QPointF(*point),3,3)

    def front_arms(self,p,o,t,pose_data):
        js,st=pose_data
        sides=set(o.get('front_hands',[]))
        sides.update(c.get('hand','r') for c in o.get('contacts',[]) if c.get('start',0)<=t<c.get('end',15))
        p.setPen(QPen(QColor(o.get('color','#303932')),5.2*st['scale'],Qt.PenStyle.SolidLine,Qt.PenCapStyle.RoundCap,Qt.PenJoinStyle.RoundJoin))
        for side in sides:
            p.drawLine(QPointF(*js['shoulder_'+side]),QPointF(*js['elbow_'+side]))
            p.drawLine(QPointF(*js['elbow_'+side]),QPointF(*js['hand_'+side]))
            p.setBrush(QColor('#faf8f0'));p.drawEllipse(QPointF(*js['hand_'+side]),3*st['scale'],3*st['scale'])

    def prop(self,p,o,objects,t,root,poses=None):
        st=state(o,t)
        anchor=attachment(o,objects,t,poses) or (st['x'],st['y'])
        p.translate(*anchor);p.rotate(st['rotation']);p.scale(st['scale'],st['scale'])
        gx,gy=o.get('grip',[0,0]);px,py=o.get('pivot',[0,0]);p.translate(-gx-px,-gy-py)
        p.setPen(QPen(QColor('#353d48'),4,Qt.PenStyle.SolidLine,Qt.PenCapStyle.RoundCap))
        p.setBrush(QColor(o.get('color','#f6c945')))
        name=o.get('preset','book')
        if o.get('file'):
            im=self.image(root,o['file']);w=o.get('image_width',160)
            p.drawImage(QRectF(-w/2,-w*im.height()/im.width(),w,w*im.height()/im.width()),im)
        elif name=='umbrella':
            p.drawLine(QPointF(0,0),QPointF(0,-153))
            p.drawArc(QRectF(-12,-3,24,28),180*16,180*16)
            path=QPainterPath(QPointF(-120,-135))
            path.cubicTo(-105,-230,105,-230,120,-135)
            path.quadTo(80,-156,60,-135);path.quadTo(20,-156,0,-135)
            path.quadTo(-20,-156,-60,-135);path.quadTo(-80,-156,-120,-135)
            p.drawPath(path)
            p.setPen(QPen(QColor('#bf982e'),2))
            p.drawLine(QPointF(0,-205),QPointF(0,-137))
            p.drawLine(QPointF(0,-205),QPointF(-60,-137));p.drawLine(QPointF(0,-205),QPointF(60,-137))
        elif name=='chair':
            p.setBrush(QColor('#dddcd6'));p.drawRect(QRectF(-40,-60,80,12))
            p.drawLine(QPointF(-35,-60),QPointF(-35,0));p.drawLine(QPointF(35,-60),QPointF(35,0))
            p.drawLine(QPointF(-40,-60),QPointF(-40,-140));p.drawLine(QPointF(-40,-140),QPointF(25,-140))
        elif name=='table':
            p.setBrush(QColor('#dddcd6'));p.drawRoundedRect(QRectF(-100,-105,200,14),3,3)
            for x in (-85,85): p.drawLine(QPointF(x,-95),QPointF(x,0))
        elif name=='door':
            p.setBrush(QColor('#e0e1dc'));p.drawRect(QRectF(-55,-280,110,280))
            p.drawEllipse(QPointF(35,-135),4,4)
        elif name=='phone':
            p.setBrush(QColor('#434b58'));p.drawRoundedRect(QRectF(-12,-35,24,42),4,4)
            p.setBrush(QColor('#bdd9df'));p.drawRect(QRectF(-8,-29,16,27))
        elif name=='towel':
            p.setBrush(QColor('#dde3e4'));p.drawRoundedRect(QRectF(-35,-22,70,30),5,5)
        elif name in ('bag','backpack'):
            p.setBrush(QColor('#8b9caa'));p.drawRoundedRect(QRectF(-25,-55,50,60),10,10)
            p.drawArc(QRectF(-15,-70,30,25),0,180*16)
        else:
            p.setBrush(QColor('#dde2d8'));p.drawRect(QRectF(-25,-35,50,40))
            p.drawLine(QPointF(0,-35),QPointF(0,5))


    def world_effects(self,p,s,t,poses,front):
        effects=s.get('effects',[])
        if 'rain' in effects:
            shelter=QPainterPath()
            for o in s['objects']:
                if o['kind']=='prop' and o.get('preset')=='umbrella' and state(o,t)['visible']:
                    st=state(o,t);anchor=attachment(o,s['objects'],t,poses) or (st['x'],st['y'])
                    tr=QTransform();tr.translate(*anchor);tr.rotate(st['rotation']);tr.scale(st['scale'],st['scale'])
                    gx,gy=o.get('grip',[0,0]);tr.translate(-gx,-gy)
                    a=tr.map(QPointF(-120,-135));b=tr.map(QPointF(120,-135));top=tr.map(QPointF(0,-216))
                    path=QPainterPath(a);path.quadTo(top,b)
                    path.lineTo(QPointF(b.x()-70,640));path.lineTo(QPointF(a.x()-70,640));path.closeSubpath()
                    shelter=shelter.united(path)
            p.save()
            region=QPainterPath();region.addRect(QRectF(-3000,-2000,7000,5000));p.setClipPath(region.subtracted(shelter))
            count=110 if not front else 38
            for i in range(count):
                seed=i+(0 if not front else 200)
                speed=170+(seed%7)*17 if not front else 310+(seed%5)*19
                x=(seed*173.731-t*47)%2400-600;y=(seed*89.17+t*speed)%1100-200
                alpha=42 if not front else 72
                p.setPen(QPen(QColor(98,125,119,alpha),.8 if not front else 1.2))
                p.drawLine(QPointF(x,y),QPointF(x-5,y+14+(i%4)*3))
            p.restore()
        if not front:return
        if 'ripple' in effects:
            for x,y,w in s.get('puddles',[[600,592,160]]):
                for i in range(4):
                    phase=(t*.75+i*.27)%1
                    p.setPen(QPen(QColor(105,137,127,int((1-phase)*100)),1));p.setBrush(Qt.BrushStyle.NoBrush)
                    p.drawEllipse(QPointF(x-w*.32+i*w*.19,y),phase*18,phase*3)
        for effect in ('leaves','snow'):
            if effect not in effects:continue
            for i in range(24):
                x=(i*177.31+t*20+math.sin(t+i)*12)%1700-200;y=(i*97.5+t*32)%850-70
                p.save();p.translate(x,y);p.rotate(t*30+i*43);p.setPen(Qt.PenStyle.NoPen)
                p.setBrush(QColor('#aaa68c' if effect=='leaves' else '#ffffff'));p.drawEllipse(QRectF(-3,-1.5,6,3));p.restore()

    def screen_effects(self,p,s,t):
        fade=s.get('fade',{})
        if 'fade' in s.get('effects',[]) and not fade:fade={'in':1,'out':1}
        alpha=0
        if fade.get('in'):alpha=max(alpha,1-t/fade['in'])
        if fade.get('out'):alpha=max(alpha,1-(s['duration']-t)/fade['out'])
        if alpha>0:p.fillRect(QRectF(0,0,1280,720),QColor(25,32,28,int(min(1,alpha)*255)))
        if 'flash' in s.get('effects',[]) and t%3<.15:
            p.fillRect(QRectF(0,0,1280,720),QColor(255,255,255,int((1-t%3/.15)*140)))

    def insert(self,p,insert,t):
        # Story insert, authored as scene data rather than an editor label.
        p.fillRect(QRectF(0,0,1280,720),QColor('#eeeee5'))
        p.setPen(Qt.PenStyle.NoPen);p.setBrush(QColor('#d7d9cc'));p.drawRoundedRect(QRectF(374,76,532,530),22,22)
        p.setBrush(QColor('#303b34'));p.drawRoundedRect(QRectF(390,62,500,530),20,20)
        p.setBrush(QColor('#faf8f0'));p.drawRoundedRect(QRectF(408,90,464,475),10,10)
        p.setPen(QColor('#627063'));font=QFont('Segoe UI');font.setPixelSize(24);p.setFont(font)
        p.drawText(QRectF(435,116,410,40),Qt.AlignmentFlag.AlignLeft,insert.get('title','Mẹ'))
        p.setPen(QPen(QColor('#c6ccc0'),2));p.drawLine(QPointF(433,165),QPointF(847,165))
        kind=insert.get('kind','photo')
        if kind=='photo':
            p.setBrush(QColor('#dde2d6'));p.setPen(Qt.PenStyle.NoPen);p.drawRoundedRect(QRectF(435,190,410,245),8,8)
            p.save();p.setClipRect(QRectF(435,190,410,245));self.prop(p,{'id':'insert_umbrella','kind':'prop','preset':'umbrella','x':640,'y':405,
                'scale':.9,'rotation':12,'color':'#d8b94f','attachment':[]},[],0,Path('.'),{});p.restore()
            p.setPen(QPen(QColor('#f7f3d9'),4));p.drawLine(QPointF(685,262),QPointF(705,272))
        else:
            p.setBrush(QColor('#e2e7dc'));p.setPen(Qt.PenStyle.NoPen);p.drawRoundedRect(QRectF(435,205,410,205),10,10)
            p.setPen(QColor('#425548'));font.setPixelSize(35);p.setFont(font)
            p.drawText(QRectF(460,245,360,120),Qt.AlignmentFlag.AlignCenter,'VỀ NHÀ\nChiều nay')
        font.setPixelSize(25);p.setFont(font);p.setPen(QColor('#536452'))
        p.drawText(QRectF(435,454,410,82),Qt.TextFlag.TextWordWrap,insert.get('text','Cha vừa sửa lại chiếc ô.'))
