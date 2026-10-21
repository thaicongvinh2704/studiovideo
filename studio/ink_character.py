"""Resolution independent cutout drawing driven by the evaluated character joints.

All paths are deterministic. No frame noise is used to imitate hand drawing.
The silhouette is drawn as filled, tapered contours; there are no joint caps.
"""
import math
from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QPainterPath, QPen, QTransform
from .animation import stepped, sample


INK = '#191d20'


def face_values(o,t):
    keys=o.get('keys',{})
    phase=(t+o.get('blink_offset',1.2))%4.9
    blink=math.sin(math.pi*phase/.16)**2 if phase<.16 else 0
    return (sample(keys.get('mouth_open',[]),t,-1),
            min(1,max(0,sample(keys.get('blink',[]),t,blink))),
            sample(keys.get('brow_lift',[]),t,0))


def path(points):
    p = QPainterPath(QPointF(*points[0]))
    for point in points[1:]:
        if len(point) == 2: p.lineTo(*point)
        elif len(point) == 4: p.quadTo(*point)
        else: p.cubicTo(*point)
    p.closeSubpath()
    return p


def ribbon(points, widths):
    """A continuous tapered contour with smooth joins instead of outlined bones."""
    result=QPainterPath()
    for (a,b),(wa,wb) in zip(zip(points,points[1:]),zip(widths,widths[1:])):
        dx,dy=b[0]-a[0],b[1]-a[1];length=max(.001,math.hypot(dx,dy));nx,ny=-dy/length,dx/length
        part=path([(a[0]+nx*wa,a[1]+ny*wa),(b[0]+nx*wb,b[1]+ny*wb),
                   (b[0]-nx*wb,b[1]-ny*wb),(a[0]-nx*wa,a[1]-ny*wa)])
        result=result.united(part)
    for (x,y),w in zip(points,widths):
        cap=QPainterPath();cap.addEllipse(QPointF(x,y),w,w);result=result.united(cap)
    return result


def draw_hand(p, wrist, elbow, scale, gesture, ink, skin):
    p.save()
    p.translate(*wrist)
    angle = math.degrees(math.atan2(wrist[1]-elbow[1], wrist[0]-elbow[0]))
    p.rotate(angle); p.scale(scale, scale)
    p.setPen(QPen(ink, 1.4, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
    p.setBrush(skin)
    if gesture == 'point':
        hand = path([(-2,-3),(2,-4),(11,-5),(14,-5,14,-3),(12,-1,7,0),(9,2),(8,4),(7,5),(3,6),(-1,4),(-3,1)])
    elif gesture == 'grip':
        hand = path([(-3,-3),(2,-5),(6,-4),(8,-1),(7,5),(3,7),(-1,4),(-3,2)])
    elif gesture == 'rest':
        hand = path([(-3,-3),(3,-4),(8,-2),(10,1,8,3),(4,5),(-1,4)])
    else:
        hand = path([(-3,-3),(2,-4),(5,-8),(7,-9,7,-6),(6,-3),
                     (13,-5),(16,-4,13,-2),(17,-2),(19,0,16,1),
                     (14,2),(16,3),(17,5,13,5),(9,6),(3,5),(-2,3)])
    p.drawPath(hand)
    if gesture=='point':
        p.setBrush(Qt.BrushStyle.NoBrush)
        for a,b in [((3,1),(6,2)),((2,3),(5,4))]:p.drawPath(_open_path([a,b]))
    if gesture == 'grip':
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawPath(_open_path([(3,-1),(6,0),(6,3)]))
    p.restore()


def _open_path(points):
    result=QPainterPath(QPointF(*points[0]))
    for point in points[1:]:
        if len(point)==2:result.lineTo(*point)
        elif len(point)==4:result.quadTo(*point)
        else:result.cubicTo(*point)
    return result


def draw(p,o,t,joints,st):
    # Normalize the evaluated world joints; apply the root transform once to all artwork.
    sc=st['scale'];a=math.radians(-st['rotation']);c,s=math.cos(a),math.sin(a)
    local={}
    for k,(x,y) in joints.items():
        dx,dy=x-st['x'],y-st['y'];local[k]=((dx*c-dy*s)/sc,(dx*s+dy*c)/sc)
    p.save();p.translate(st['x'],st['y']);p.rotate(st['rotation']);p.scale(sc,sc)
    _draw(p,o,t,local,{**st,'scale':1,'rotation':0,'x':0,'y':0})
    p.restore()


def _draw(p, o, t, joints, st):
    sc=st['scale']; ink=QColor(o.get('color',INK)); skin=QColor(o.get('skin_color','#ffdbb5'))
    shirt=QColor(o.get('shirt','#ffffff')); pants=QColor(o.get('pants','#6695ba'))
    pen=QPen(ink,1.35*sc,Qt.PenStyle.SolidLine,Qt.PenCapStyle.RoundCap,Qt.PenJoinStyle.RoundJoin)
    p.setPen(pen)
    pose=stepped(o.get('poses',[]),t,o.get('pose','rest'))
    reference=o.get('character_design')=='reference_black'
    hip,neck=joints['hip'],joints['neck']
    # A separate leg root at each side creates a pelvis, instead of crossing rods.
    for side,sign in (('l',-1),('r',1)):
        root=(hip[0]+sign*(10 if reference else 8)*sc,hip[1]-2*sc)
        knee,foot=joints['knee_'+side],joints['foot_'+side]
        p.setBrush(pants)
        p.drawPath(ribbon([root,knee,(foot[0],foot[1]-3*sc)],[(9 if reference else 7.5)*sc,(7.6 if reference else 5.8)*sc,(6.9 if reference else 5)*sc]))
        # Closed shoe silhouette. No exposed joint circles at the ankle.
        x,y=foot;direction=1 if st.get('facing',1)>=0 else -1
        p.setBrush(QColor(o.get('shoes','#eef0ee')))
        shoe=path([(x-7*sc,y-5*sc),(x+5*sc,y-6*sc),
                   (x+direction*14*sc,y-4*sc,x+direction*16*sc,y+1*sc),
                   (x+direction*16*sc,y+3*sc,x+3*sc,y+4*sc),(x-8*sc,y+3*sc)])
        p.drawPath(shoe)
    # Arms are behind the single shirt silhouette. Sleeves are merged into it.
    cuffs={};front_hands=[]
    for side in ('l','r'):
        a,b,c=joints['shoulder_'+side],joints['elbow_'+side],joints['hand_'+side]
        p.setBrush(skin);p.drawPath(ribbon([a,b,c],[4.5*sc,3.8*sc,2.8*sc]))
        sleeve=(a[0]+(b[0]-a[0])*.43,a[1]+(b[1]-a[1])*.43)
        dx,dy=b[0]-a[0],b[1]-a[1];arm_length=max(.001,math.hypot(dx,dy));nx,ny=-dy/arm_length,dx/arm_length
        sign=-1 if side=='l' else 1
        cuffs[side]=((sleeve[0]-sign*nx*6.2*sc,sleeve[1]-sign*ny*6.2*sc),(sleeve[0]+sign*nx*6.2*sc,sleeve[1]+sign*ny*6.2*sc))
        hand='point' if pose in ('point','point_left','idea','disagree') and side==('l' if pose=='point_left' else 'r') else 'grip' if pose in ('hold','receive','give','read') else 'rest' if pose in ('rest','walk','sit','listen') else 'open'
        if reference and ((pose=='point' and side=='l') or (pose=='point_left' and side=='r') or pose=='confident'):
            front_hands.append((c,b,'grip'))
        else:draw_hand(p,c,b,sc*.88,hand,ink,skin)
    p.setPen(pen);p.setBrush(skin)
    hx,hy=joints['head']
    p.drawPath(ribbon([(hx,hy+19*sc),neck],[6.5*sc,6.8*sc]))
    left,right=joints['shoulder_l'],joints['shoulder_r']
    lo,li=cuffs['l'];ro,ri=cuffs['r']
    body=path([(neck[0]-7*sc,neck[1]-2*sc),(left[0]-4*sc,left[1]-4*sc),lo,li,
               (left[0]+5*sc,left[1]+16*sc),(hip[0]-21*sc,hip[1]+3*sc),
               (hip[0],hip[1]+7*sc,hip[0]+21*sc,hip[1]+3*sc),
               (right[0]-5*sc,right[1]+16*sc),ri,ro,(right[0]+4*sc,right[1]-4*sc),
               (neck[0]+7*sc,neck[1]-2*sc),(neck[0],neck[1]+6*sc,neck[0]-7*sc,neck[1]-2*sc)])
    p.setBrush(shirt);p.drawPath(body)
    if o.get('shirt_mark')=='plus':
        # Logo follows the torso basis rather than floating in world space.
        p.save();p.translate(neck[0]+9*sc,neck[1]+14*sc)
        angle=math.degrees(math.atan2(neck[0]-hip[0],hip[1]-neck[1]));p.rotate(-angle-4)
        p.setPen(QPen(QColor('#f5f5ef'),2.0*sc,Qt.PenStyle.SolidLine,Qt.PenCapStyle.RoundCap))
        p.drawLine(QPointF(-3.2*sc,0),QPointF(3.2*sc,0));p.drawLine(QPointF(0,-4.1*sc),QPointF(0,4.1*sc));p.restore()
    p.setBrush(Qt.BrushStyle.NoBrush)
    # Head, face and hair use a local coordinate system, so tilt actually rotates them.
    p.save();p.translate(hx,hy)
    tilt=sample(o.get('keys',{}).get('face_tilt',[]),t,0)
    tilt+=math.degrees(sample(o.get('keys',{}).get('bone_head',[]),t,0))*.55
    p.rotate(tilt);p.scale(sc*1.12,sc*1.12)
    if reference:
        _reference_head(p,o,t,ink,skin)
        p.restore()
        for wrist,elbow,gesture in front_hands:draw_hand(p,wrist,elbow,sc*.9,gesture,ink,skin)
        if pose=='think':draw_hand(p,joints['hand_r'],joints['elbow_r'],sc*.9,'rest',ink,skin)
        return
    face_pen=QPen(ink,1.2,Qt.PenStyle.SolidLine,Qt.PenCapStyle.RoundCap,Qt.PenJoinStyle.RoundJoin)
    p.setPen(face_pen);p.setBrush(skin)
    p.drawEllipse(QRectF(-28,-1,7,12));p.drawEllipse(QRectF(21,-1,7,12))
    p.drawPath(path([(-24,-12),(-25,9,-18,21),(-9,32,9,32,19,19),(26,8,24,-15),(12,-32,-17,-31,-24,-12)]))
    p.setBrush(ink)
    hair=path([(-24,1),(-27,-10,-27,-17,-24,-23),(-29,-22),(-23,-29),(-28,-28),
               (-16,-35),(-18,-32),(-8,-39),(-10,-34),(0,-37),(4,-34),(13,-36),
               (12,-32),(23,-30),(20,-28),(27,-22),(25,-21),(27,-12),(24,-3),(22,-1),
               (20,-11,21,-18,16,-20),(10,-20,4,-20,-2,-20),(-12,-20,-18,-16,-19,-10),(-21,2)])
    p.drawPath(hair)
    p.setPen(QPen(ink,.85,Qt.PenStyle.SolidLine,Qt.PenCapStyle.RoundCap))
    for coords in [(-26,-16,-34,-30,-8,-35),(-24,-23,-25,-39,1,-33),(-19,-28,-10,-41,8,-32),
                   (-8,-31,8,-40,19,-29),(2,-32,24,-36,27,-20),(-27,-7,-33,-19,-22,-29)]:
        p.drawPath(_open_path([coords[:2],coords[2:]]))
    p.setPen(QPen(QColor('#f9f7f0'),.55,Qt.PenStyle.SolidLine,Qt.PenCapStyle.RoundCap))
    for coords in [(-22,-24,-13,-32,-2,-31),(-16,-28,-4,-36,9,-30),(0,-30,11,-34,20,-24),(-24,-18,-28,-26,-17,-30)]:
        p.drawPath(_open_path([coords[:2],coords[2:]]))
    expression=stepped(o.get('expressions',[]),t,o.get('expression','happy'))
    p.setPen(face_pen);p.setBrush(ink)
    blink=(t+o.get('blink_offset',1.2))%4.9<.11
    gaze=sample(o.get('keys',{}).get('gaze',[]),t,o.get('gaze',0))*2
    for sign in (-1,1):
        x=sign*9+gaze
        if blink:p.drawPath(_open_path([(x-3,1),(x,3,x+3,1)]))
        else:p.drawEllipse(QRectF(x-1.35,-1.4,2.7,4.9))
        y=-7 if expression not in ('worried','sad','angry','curious') else -8+sign*2
        if expression=='confident':y=-6
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawPath(_open_path([(x-4,y+1),(x,y-2,x+4,y)]))
        p.setBrush(ink)
    p.setBrush(Qt.BrushStyle.NoBrush)
    p.drawPath(_open_path([(0,4),(2,10,-1,10)]))
    if expression=='surprised':
        p.setBrush(QColor('#ffffff'));p.drawEllipse(QRectF(-4,14,8,10))
    elif expression in ('worried','sad'):
        p.drawPath(_open_path([(-7,22),(0,15,7,22)]))
    elif expression in ('normal','listen'):
        p.drawPath(_open_path([(-6,18),(0,21,6,18)]))
    elif expression=='angry':
        p.drawPath(_open_path([(-7,20),(0,17,7,20)]))
    else:
        p.setBrush(QColor('#ffffff'))
        p.drawPath(path([(-9,15),(0,18,9,15),(7,27,-6,29,-9,15)]))
    p.restore()
    if pose=='think':draw_hand(p,joints['hand_r'],joints['elbow_r'],sc,'rest',ink,skin)


def _reference_head(p,o,t,ink,skin):
    """Three-quarter facial landmarks and swept sketch hair from the supplied guide."""
    face_pen=QPen(ink,1.45,Qt.PenStyle.SolidLine,Qt.PenCapStyle.RoundCap,Qt.PenJoinStyle.RoundJoin)
    p.setPen(face_pen);p.setBrush(skin)
    p.drawPath(path([(-23,-13),(-24,1),(-28,0,-31,4,-30,9),(-30,14,-24,16,-20,12),
                     (-16,23,-4,29,9,25),(24,20,27,7,23,-12),(20,-27,12,-28,2,-25),
                     (-12,-23,-20,-22,-23,-13)]))
    p.setBrush(ink)
    p.drawPath(path([(-23,5),(-27,5),(-29,-7,-27,-20,-22,-25),(-25,-25),(-19,-32),
                     (-23,-31),(-12,-38),(-15,-33),(-5,-39),(-6,-35),(7,-39),(5,-35),
                     (18,-37),(14,-33),(26,-34),(21,-31),(30,-31),(24,-28),(29,-28),(20,-25),
                     (8,-25,-6,-24,-18,-16),(-22,-13,-23,-4,-23,5)]))
    p.setBrush(Qt.BrushStyle.NoBrush)
    p.setPen(QPen(ink,1.0,Qt.PenStyle.SolidLine,Qt.PenCapStyle.RoundCap))
    for coords in [(-26,-13,-31,-26,-11,-34),(-26,-22,-20,-34,-3,-39),(-19,-28,-10,-39,4,-38),
                   (-9,-31,5,-42,17,-35),(0,-32,19,-39,27,-34),(7,-28,24,-34,31,-30)]:
        p.drawPath(_open_path([coords[:2],coords[2:]]))
    p.setPen(QPen(QColor('#f4eee0'),.52,Qt.PenStyle.SolidLine,Qt.PenCapStyle.RoundCap))
    for coords in [(-22,-24,-16,-31,-7,-34),(-14,-28,-5,-34,4,-35),(-4,-29,7,-35,16,-33),(5,-28,16,-32,23,-30),(-26,-9,-28,-16,-24,-22)]:
        p.drawPath(_open_path([coords[:2],coords[2:]]))
    ex=stepped(o.get('expressions',[]),t,o.get('expression','happy'))
    mouth,blink,brow=face_values(o,t)
    gaze=sample(o.get('keys',{}).get('gaze',[]),t,o.get('gaze',0))*1.5
    p.setPen(face_pen);p.setBrush(ink)
    for i,(x,y) in enumerate(((-4,1),(13,-2))):
        x+=gaze
        if blink>.92:p.drawPath(_open_path([(x-2,y),(x,y+1.3,x+2,y)]))
        else:
            eye_height=(6.7 if ex=='surprised' else 4.1 if ex in ('sad','worried') else 5.0)*(1-blink)
            p.drawEllipse(QRectF(x-1.45,y-eye_height*.48,2.9,eye_height))
        p.setBrush(Qt.BrushStyle.NoBrush)
        y-=brow
        lift=(-1 if i==0 else -2) if ex=='curious' else 0
        if ex in ('worried','sad'):
            p.drawPath(_open_path([(x-3.6,y-(6 if i==0 else 10)),(x+3.4,y-(10 if i==0 else 6))]))
        elif ex=='surprised':p.drawPath(_open_path([(x-3.7,y-11),(x,y-14,x+3.4,y-12)]))
        elif ex=='angry':p.drawPath(_open_path([(x-3.5,y-8-i*2),(x+3.5,y-6+i*2)]))
        else:p.drawPath(_open_path([(x-3.7,y-7+lift),(x,y-10+lift,x+3.4,y-8+lift)]))
        p.setBrush(ink)
    p.setBrush(Qt.BrushStyle.NoBrush)
    p.drawPath(_open_path([(7,5),(9,6,8,8)]))
    if mouth>=0:
        if mouth<.07:
            p.drawPath(_open_path([(0,18),(7,21 if ex=='happy' else 12 if ex in ('sad','worried') else 17,13,17)]))
        else:
            height=1+mouth*6;width=9 if ex=='surprised' else 14
            p.setBrush(QColor('#49322e'))
            if ex in ('sad','worried'):
                p.drawPath(path([(0,19),(6,12,13,18),(13,18+height,1,18+height,0,19)]))
            elif ex=='surprised':p.drawEllipse(QRectF(3,13,7,3+mouth*7))
            else:
                p.drawPath(path([(7-width/2,15),(7,17 if ex=='happy' else 14,7+width/2,14),
                                 (7+width/2,15+height,7-width/2,17+height,7-width/2,15)]))
            if ex not in ('sad','worried','surprised'):
                p.setPen(Qt.PenStyle.NoPen);p.setBrush(QColor('#fffdf6'))
                p.drawPath(path([(7-width/2+1,15.7),(7,17,7+width/2-1,15),
                                 (7+width/2-2,17.4),(7,19,7-width/2+2,17.8)]))
                p.setPen(face_pen)
    elif ex=='surprised':p.setBrush(QColor('white'));p.drawEllipse(QRectF(3,14,7,9))
    elif ex in ('worried','sad'):p.drawPath(_open_path([(0,21),(6,15,13,19)]))
    elif ex in ('normal','angry'):p.drawPath(_open_path([(0,17),(7,18,13,15)]))
    else:
        p.setBrush(QColor('#ffffff'))
        p.drawPath(path([(-1,13),(7,14,14,11),(14,18,4,25,-1,13)]))
