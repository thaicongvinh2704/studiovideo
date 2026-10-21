from PySide6.QtCore import Qt, Signal, QRectF, QPointF
from PySide6.QtGui import QColor,QPen,QPixmap,QTransform
from PySide6.QtWidgets import QGraphicsView,QGraphicsScene
from ..animation import state,skeleton,attachment,sample,camera_values,evaluate_scene

class Canvas(QGraphicsView):
    selected=Signal(str)
    edit_started=Signal()
    moved=Signal(str,float,float)
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setScene(QGraphicsScene(self));self.setBackgroundBrush(QColor('#0e131c'))
        self.setFrameShape(QGraphicsView.Shape.NoFrame)
        self.setMinimumSize(320,190)
        self.pixmap=self.scene().addPixmap(QPixmap())
        self.selection=self.scene().addRect(QRectF(),QPen(QColor('#edc95e'),2,Qt.PenStyle.DashLine))
        self.selection.setZValue(10)
        self.safe=self.scene().addRect(QRectF(),QPen(QColor('#889eac'),1,Qt.PenStyle.DashLine));self.safe.setZValue(9)
        self.safe.hide();self.selection.hide()
        self.current_scene=None;self.time=0;self.selected_id='';self.drag=None;self.zoom=1.
        self.width_px=854;self.height_px=480

    def show_frame(self,image,scene,time,selected='',safe=False):
        self.current_scene,self.time,self.selected_id=scene,time,selected
        self.width_px,self.height_px=image.width(),image.height()
        self.pixmap.setPixmap(QPixmap.fromImage(image))
        self.scene().setSceneRect(0,0,image.width(),image.height())
        self.fit()
        self.safe.setRect(image.width()*.05,image.height()*.05,image.width()*.9,image.height()*.9)
        self.safe.setVisible(safe)
        self.selection.hide()
        if scene:
            o=next((o for o in scene['objects'] if o['id']==selected),None)
            if o:
                rect=self.bounds(o)
                a=self.camera_point(rect.topLeft());b=self.camera_point(rect.bottomRight())
                self.selection.setRect(QRectF(a,b));self.selection.show()

    def camera_values(self):
        return camera_values(self.current_scene,self.time) if self.current_scene else (1,640,360)

    def camera_point(self,point):
        z,x,y=self.camera_values()
        scale=min(self.width_px/1280,self.height_px/720)
        dx=(self.width_px-1280*scale)/2;dy=(self.height_px-720*scale)/2
        return QPointF(((point.x()-x)*z+640)*scale+dx,((point.y()-y)*z+360)*scale+dy)

    def point(self,event):
        pt=self.mapToScene(event.position().toPoint())
        z,x,y=self.camera_values()
        scale=min(self.width_px/1280,self.height_px/720)
        dx=(self.width_px-1280*scale)/2;dy=(self.height_px-720*scale)/2
        return QPointF(((pt.x()-dx)/scale-640)/z+x,((pt.y()-dy)/scale-360)/z+y)

    def bounds(self,obj):
        from ..hierarchy import world_states,transform_point
        world=world_states(self.current_scene['objects'],self.time);st=world[obj['id']]
        if obj['kind'] in ('text','shape','image') and 'width' in obj:
            anchor=attachment(obj,self.current_scene['objects'],self.time)
            if anchor:st={**st,'x':anchor[0],'y':anchor[1]}
            tr=QTransform();tr.translate(st['x'],st['y']);tr.rotate(st['rotation']);tr.scale(st['scale'],st['scale'])
            pivot=obj.get('pivot',[0,0]);tr.translate(-pivot[0],-pivot[1])
            return tr.mapRect(QRectF(-obj['width']/2,-obj['height']/2,obj['width'],obj['height']))
        if obj['kind']=='character':
            js,_=evaluate_scene(self.current_scene['objects'],self.time)[obj['id']]
            xs=[v[0] for v in js.values()];ys=[v[1] for v in js.values()]
            return QRectF(min(xs)-30,min(ys)-30,max(xs)-min(xs)+60,max(ys)-min(ys)+60)
        pt=attachment(obj,self.current_scene['objects'],self.time) or (st['x'],st['y'])
        return QRectF(pt[0]-90*st['scale'],pt[1]-210*st['scale'],180*st['scale'],230*st['scale'])

    def fit(self):
        self.resetTransform();self.fitInView(self.sceneRect(),Qt.AspectRatioMode.KeepAspectRatio);self.scale(self.zoom,self.zoom)
    def resizeEvent(self,event):
        super().resizeEvent(event);self.fit()
    def mousePressEvent(self,event):
        if event.button()==Qt.MouseButton.LeftButton and self.current_scene:
            pt=self.point(event)
            for o in sorted(self.current_scene['objects'],key=lambda o:o.get('layer',0),reverse=True):
                from ..hierarchy import world_states
                st=world_states(self.current_scene['objects'],self.time)[o['id']]
                if not o.get('locked') and st['visible'] and o['kind']!='group' and self.bounds(o).contains(pt):
                    self.selected.emit(o['id'])
                    self.drag=(o['id'],pt.x()-st['x'],pt.y()-st['y'])
                    self.edit_started.emit();return
            self.selected.emit('')
        super().mousePressEvent(event)
    def mouseMoveEvent(self,event):
        if self.drag:
            pt=self.point(event);ident,dx,dy=self.drag
            self.moved.emit(ident,pt.x()-dx,pt.y()-dy);return
        super().mouseMoveEvent(event)
    def mouseReleaseEvent(self,event):
        self.drag=None;super().mouseReleaseEvent(event)
