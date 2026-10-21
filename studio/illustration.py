"""CPU vector illustration and editable graphic layers."""
import math
from PySide6.QtCore import Qt,QRectF,QPointF
from PySide6.QtGui import QColor,QPen,QBrush,QFont,QFontMetricsF,QPainterPath,QPolygonF,QTransform
from .animation import state, stepped, ease

def fitted_text(p,text,rect,size=30,color='#202a30',bold=False,align='center',font='Segoe UI'):
    f=QFont(font);f.setBold(bold)
    flags=Qt.TextFlag.TextWordWrap | (Qt.AlignmentFlag.AlignLeft if align=='left' else Qt.AlignmentFlag.AlignHCenter) | Qt.AlignmentFlag.AlignVCenter
    for px in range(max(10,int(size)),9,-1):
        f.setPixelSize(px);p.setFont(f)
        if QFontMetricsF(f).boundingRect(rect,int(flags),text).height()<=rect.height():break
    p.setPen(QColor(color));p.drawText(rect,int(flags),text)

def layer_rect(o):
    return QRectF(-o.get('width',300)/2,-o.get('height',180)/2,o.get('width',300),o.get('height',180))

def graphic(p,o,t,root,renderer,st=None):
    st=st or state(o,t);p.translate(st['x'],st['y']);p.rotate(st['rotation']);p.scale(st['scale'],st['scale'])
    p.translate(*[-v for v in o.get('pivot',[0,0])])
    rect=layer_rect(o);color=o.get('color','#24323a');stroke=o.get('stroke',3)
    p.setPen(QPen(QColor(color),stroke,Qt.PenStyle.SolidLine,Qt.PenCapStyle.RoundCap,Qt.PenJoinStyle.RoundJoin))
    p.setBrush(QColor(o.get('fill','#fff5d8')))
    kind=o['kind']
    if kind=='shape' and o.get('shape')=='path':
        points=o.get('points',[])
        if points:
            path=QPainterPath(QPointF(*points[0]))
            if o.get('reveal'):
                from .animation import ease
                progress=ease((t-o.get('start',0))/max(.001,o.get('enter_duration',1)),'ease_in_out')
                distances=[math.dist(a,b) for a,b in zip(points,points[1:])];remaining=sum(distances)*progress
                for a,b,d in zip(points,points[1:],distances):
                    if remaining>=d:path.lineTo(*b);remaining-=d
                    else:
                        u=remaining/max(.001,d);path.lineTo(a[0]+(b[0]-a[0])*u,a[1]+(b[1]-a[1])*u);break
            else:
                for point in points[1:]:path.lineTo(QPointF(*point))
            if o.get('closed'):path.closeSubpath()
            else:p.setBrush(Qt.BrushStyle.NoBrush)
            p.drawPath(path)
        return
    if kind=='text':
        fitted_text(p,o.get('text',''),rect,o.get('font_size',32),color,o.get('bold',False),o.get('align','center'),o.get('font','Segoe UI'));return
    if kind=='image':
        if str(o.get('file','')).lower().endswith('.svg'):
            svg=renderer.vector(root,o['file']);full=svg.viewBoxF();crop=o.get('crop',[0,0,1,1])
            source=QRectF(full.x()+crop[0]*full.width(),full.y()+crop[1]*full.height(),crop[2]*full.width(),crop[3]*full.height())
            ratio=source.width()/max(1,source.height());target=QRectF(rect)
            if o.get('fit','contain')=='cover':
                if ratio>rect.width()/rect.height():
                    w=source.height()*rect.width()/rect.height();source.setLeft(source.center().x()-w/2);source.setWidth(w)
                else:
                    h=source.width()*rect.height()/rect.width();source.setTop(source.center().y()-h/2);source.setHeight(h)
            else:
                if ratio>rect.width()/rect.height():target.setHeight(rect.width()/ratio)
                else:target.setWidth(rect.height()*ratio)
                target.moveCenter(rect.center())
            sx=target.width()/max(.001,source.width());sy=target.height()/max(.001,source.height())
            mapped=QRectF(target.left()-(source.left()-full.left())*sx,target.top()-(source.top()-full.top())*sy,full.width()*sx,full.height()*sy)
            p.setClipRect(rect);svg.render(p,mapped);return
        im=renderer.image(root,o['file']);source=QRectF(0,0,im.width(),im.height())
        crop=o.get('crop',[0,0,1,1]);source=QRectF(crop[0]*im.width(),crop[1]*im.height(),crop[2]*im.width(),crop[3]*im.height())
        ratio=source.width()/max(1,source.height());target=QRectF(rect)
        if o.get('fit','contain')=='cover':
            if ratio>rect.width()/rect.height():
                w=source.height()*rect.width()/rect.height();source.setLeft(source.center().x()-w/2);source.setWidth(w)
            else:
                h=source.width()*rect.height()/rect.width();source.setTop(source.center().y()-h/2);source.setHeight(h)
        else:
            if ratio>rect.width()/rect.height():target.setHeight(rect.width()/ratio)
            else:target.setWidth(rect.height()*ratio)
            target.moveCenter(rect.center())
        p.setClipRect(rect);p.drawImage(target,im,source);return
    shape=o.get('shape','card')
    if shape=='ellipse':p.drawEllipse(rect)
    elif shape in ('arrow','line'):
        a=QPointF(rect.left(),0);b=QPointF(rect.right(),0);p.drawLine(a,b)
        if shape=='arrow':
            p.setBrush(QColor(color));p.drawPolygon(QPolygonF([b,QPointF(b.x()-18,-10),QPointF(b.x()-18,10)]))
    elif shape=='callout':
        path=QPainterPath();path.addRoundedRect(rect,20,20)
        tail=QPainterPath(QPointF(rect.left()+40,rect.bottom()-2));tail.lineTo(rect.left()+5,rect.bottom()+25);tail.lineTo(rect.left()+85,rect.bottom()-2);tail.closeSubpath()
        p.drawPath(path.united(tail))
    elif shape=='check':
        p.drawPolyline(QPolygonF([QPointF(rect.left(),0),QPointF(-rect.width()*.12,rect.bottom()),QPointF(rect.right(),rect.top())]))
    elif shape=='cross':p.drawLine(rect.topLeft(),rect.bottomRight());p.drawLine(rect.topRight(),rect.bottomLeft())
    else:p.drawRoundedRect(rect,12,12)
    if o.get('text'):fitted_text(p,o['text'],rect.adjusted(18,14,-18,-14),o.get('font_size',30),color,o.get('bold',False))

def illustrated_character(p,o,t,joints,st):
    """Clothed silhouette follows the same evaluated joints as the original rig."""
    sc=st['scale'];ink=QColor(o.get('color','#20262a'));skin=QColor(o.get('skin_color','#f1c6a2'))
    def pen(w,c=ink):return QPen(c,w*sc,Qt.PenStyle.SolidLine,Qt.PenCapStyle.RoundCap,Qt.PenJoinStyle.RoundJoin)
    def line(a,b,w,c):p.setPen(pen(w,c));p.drawLine(QPointF(*a),QPointF(*b))
    hip=joints['hip'];neck=joints['neck'];head=joints['head']
    for side in ('l','r'):
        knee=joints['knee_'+side];foot=joints['foot_'+side];toe=joints['toe_'+side]
        for a,b in ((hip,knee),(knee,foot)):line(a,b,15,ink);line(a,b,11,QColor(o.get('pants','#426c8c')))
        line((foot[0]-4*sc,foot[1]),(toe[0]+2*sc,toe[1]),9,ink)
        line((foot[0]-4*sc,foot[1]-2*sc),(toe[0]+2*sc,toe[1]-2*sc),5,QColor('#f6f3ea'))
    left=joints['shoulder_l'];right=joints['shoulder_r']
    p.setPen(pen(2.2));p.setBrush(QColor(o.get('shirt','#f4c44f')))
    path=QPainterPath(QPointF(left[0]-3*sc,left[1]-3*sc))
    path.quadTo(neck[0],neck[1]+8*sc,right[0]+3*sc,right[1]-3*sc)
    path.lineTo(hip[0]+21*sc,hip[1]+3*sc);path.quadTo(hip[0],hip[1]+9*sc,hip[0]-21*sc,hip[1]+3*sc);path.closeSubpath();p.drawPath(path)
    for side in ('l','r'):
        shoulder=joints['shoulder_'+side];elbow=joints['elbow_'+side];hand=joints['hand_'+side]
        for a,b in ((shoulder,elbow),(elbow,hand)):line(a,b,10,ink);line(a,b,6.5,skin)
        sleeve=tuple(a+(b-a)*.40 for a,b in zip(shoulder,elbow))
        line(shoulder,sleeve,14,ink);line(shoulder,sleeve,10,QColor(o.get('shirt','#f4c44f')))
        p.setPen(pen(1.7));p.setBrush(skin);p.drawEllipse(QPointF(*hand),4.5*sc,5*sc)
        dx=hand[0]-elbow[0];dy=hand[1]-elbow[1];length=max(1,math.hypot(dx,dy));dx/=length;dy/=length
        pose=stepped(o.get('poses',[]),t,o.get('pose','rest'))
        if pose in ('point','point_left') and side==('l' if pose=='point_left' else 'r'):
            line(hand,(hand[0]+dx*10*sc,hand[1]+dy*10*sc),3,ink)
        else:
            for n in (-1,0,1):
                a=(hand[0]-dy*n*2*sc,hand[1]+dx*n*2*sc);b=(a[0]+dx*5*sc,a[1]+dy*5*sc);line(a,b,1.7,ink)
    hx,hy=head;r=26*sc
    line(neck,(hx,hy+19*sc),11,ink);line(neck,(hx,hy+19*sc),7,skin)
    p.setPen(pen(2));p.setBrush(skin)
    for sign in (-1,1):p.drawEllipse(QPointF(hx+sign*25*sc,hy+2*sc),4*sc,6*sc)
    p.drawEllipse(QPointF(hx,hy),r,r*1.08)
    hair=QPainterPath(QPointF(hx-25*sc,hy-3*sc));hair.cubicTo(hx-33*sc,hy-35*sc,hx+8*sc,hy-42*sc,hx+28*sc,hy-18*sc)
    hair.lineTo(hx+25*sc,hy-1*sc);hair.quadTo(hx+20*sc,hy-18*sc,hx+7*sc,hy-19*sc)
    hair.quadTo(hx-10*sc,hy-10*sc,hx-19*sc,hy-17*sc);hair.closeSubpath();p.setBrush(ink);p.drawPath(hair)
    ex=stepped(o.get('expressions',[]),t,o.get('expression','happy'));blink=(t+1.2)%5<.10
    p.setPen(pen(1.9));p.setBrush(ink)
    for dx in (-9,9):
        if blink:p.drawLine(QPointF(hx+(dx-3)*sc,hy),QPointF(hx+(dx+3)*sc,hy))
        else:p.drawEllipse(QPointF(hx+dx*sc,hy),1.8*sc,2.8*sc)
        p.drawArc(QRectF(hx+(dx-4)*sc,hy-11*sc,8*sc,6*sc),20*16,140*16)
    p.setBrush(QColor('#ffffff'))
    if ex=='surprised':p.drawEllipse(QPointF(hx,hy+13*sc),4*sc,5*sc)
    elif ex in ('worried','sad'):p.drawArc(QRectF(hx-7*sc,hy+10*sc,14*sc,9*sc),0,180*16)
    else:
        smile=QPainterPath(QPointF(hx-9*sc,hy+10*sc));smile.quadTo(hx,hy+16*sc,hx+9*sc,hy+10*sc);smile.quadTo(hx+3*sc,hy+27*sc,hx-9*sc,hy+10*sc);p.drawPath(smile)

def animated_opacity(o,t):
    st=state(o,t);alpha=st['opacity'];d=max(.001,o.get('enter_duration',.3))
    if o.get('enter','none')=='fade':alpha*=ease((t-o.get('start',0))/d,'ease_in_out')
    return max(0,min(1,alpha))
