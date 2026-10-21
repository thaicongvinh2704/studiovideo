from PySide6.QtCore import Qt,Signal,QRectF,QPointF
from PySide6.QtGui import QPen,QColor,QFont,QPainterPath
from PySide6.QtWidgets import QGraphicsView,QGraphicsScene
from ..project import duration

class Timeline(QGraphicsView):
    seek=Signal(float)
    selected=Signal(str,str)
    edit_started=Signal()
    edited=Signal()
    def __init__(self,parent=None):
        super().__init__(parent);self.setScene(QGraphicsScene(self));self.setMinimumHeight(170)
        self.setBackgroundBrush(QColor('#111722'));self.setFrameShape(QGraphicsView.Shape.NoFrame)
        self.project=None;self.pps=14;self.items_data=[];self.drag=None;self.snap=True;self.playhead=None
        self.setAlignment(Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignLeft)

    def draw(self,project):
        self.project=project;self.scene().clear();self.items_data=[]
        total=duration(project)
        char_lanes=max(1,max((sum(o['kind']=='character' for o in s['objects']) for s in project['scenes']),default=1))
        prop_lanes=max(1,max((sum(o['kind']!='character' for o in s['objects']) for s in project['scenes']),default=1))
        # Independent lanes keep simultaneous characters and props selectable.
        lane_counts=[1,1,char_lanes,prop_lanes,2,2,1]
        row_y=[];y=34
        for count in lane_counts:row_y.append(y);y+=count*28
        height=y
        self.scene().setSceneRect(0,0,max(800,150+total*self.pps),height)
        tracks=['CẢNH','BACKGROUND','NHÂN VẬT','ĐẠO CỤ','GIỌNG ĐỌC','NHẠC / SFX','PHỤ ĐỀ']
        colors=['#37697b','#314254','#427b75','#9b8039','#69589d','#795f78','#50677a']
        for row,title in enumerate(tracks):
            y=row_y[row]
            self.scene().addRect(QRectF(0,y,150+total*self.pps,lane_counts[row]*28-1),QPen(QColor('#253142')),QColor('#18212d'))
            text=self.scene().addText(title,QFont('Segoe UI',8));text.setDefaultTextColor(QColor('#91a6bb'));text.setPos(7,y+3)
        step=5 if self.pps>=12 else 15 if self.pps>=5 else 60
        for time in range(0,int(total)+1,step):
            x=148+time*self.pps
            self.scene().addLine(x,27,x,height,QPen(QColor('#283442')))
            txt=self.scene().addText(f'{time//60:02}:{time%60:02}',QFont('Segoe UI',8));txt.setDefaultTextColor(QColor('#b7c4d1'));txt.setPos(x-10,1)
        def bar(row,start,end,text,data,lane=0):
            rect=QRectF(148+start*self.pps,row_y[row]+2+lane*28,max(3,(end-start)*self.pps),23)
            item=self.scene().addRect(rect,QPen(QColor(colors[row]).lighter(130)),QColor(colors[row]))
            item.setToolTip(text+' · Kéo để di chuyển, kéo mép phải để đổi độ dài')
            label=self.scene().addText(text[:max(0,int(rect.width()/7)-1)],QFont('Segoe UI',8))
            label.setDefaultTextColor(QColor('#f2f5f8'));label.setPos(rect.x()+2,rect.y()+1)
            self.items_data.append((rect,data))
        for s in project['scenes']:
            bar(0,s['start'],s['start']+s['duration'],s['name'],('scene',s,s))
            bar(1,s['start'],s['start']+s['duration'],s['background'],('background',s,s))
            counts={2:0,3:0}
            for o in sorted(s['objects'],key=lambda o:o.get('layer',0)):
                row=2 if o['kind']=='character' else 3
                bar(row,s['start']+o['start'],s['start']+o['end'],o['name']+' · '+o.get('action',''),('object',s,o),counts[row]);counts[row]+=1
        audio_counts={4:[],5:[]}
        for a in sorted(project['audio'],key=lambda a:a['start']):
            row=4 if a['group']=='voice' else 5
            lane=0
            while lane<len(audio_counts[row]) and audio_counts[row][lane]>a['start']:lane+=1
            lane=min(1,lane)
            if lane>=len(audio_counts[row]):audio_counts[row].append(0)
            audio_counts[row][lane]=a['start']+a['duration']
            bar(row,a['start'],a['start']+a['duration'],a.get('name','Audio'),('audio',None,a),lane)
            peaks=a.get('waveform',[])
            if peaks:
                path=QPainterPath();step=max(1,int(len(peaks)/max(1,a['duration']*self.pps)))
                for i in range(0,len(peaks),step):
                    x=148+(a['start']+i/a.get('waveform_hz',20))*self.pps;y=row_y[row]+14+lane*28
                    amp=max(peaks[i:i+step])*10;path.moveTo(x,y-amp);path.lineTo(x,y+amp)
                self.scene().addPath(path,QPen(QColor('#b8d9cf'),1))
        for c in project['subtitles']:
            bar(6,c['start'],c['end'],c['text'],('subtitle',None,c))
        self.playhead=self.scene().addLine(148,0,148,height,QPen(QColor('#f5cc60'),2));self.playhead.setZValue(100)

    def set_time(self,t):
        if self.playhead: self.playhead.setLine(148+t*self.pps,0,148+t*self.pps,self.sceneRect().height())

    def mousePressEvent(self,event):
        pt=self.mapToScene(event.position().toPoint())
        if pt.x()<148: return
        time=max(0,(pt.x()-148)/self.pps)
        if event.button()==Qt.MouseButton.LeftButton:
            for rect,data in reversed(self.items_data):
                if rect.contains(pt):
                    kind,scene,obj=data
                    if scene: self.selected.emit(scene['id'],obj['id'] if kind=='object' else '')
                    if kind in ('object','audio','subtitle'):
                        mode='end' if rect.right()-pt.x()<8 else 'move'
                        self.edit_started.emit()
                        self.drag=(data,mode,time,obj['start'],obj.get('end',obj['start']+obj.get('duration',0)))
                    break
            self.seek.emit(min(time,duration(self.project)))

    def mouseMoveEvent(self,event):
        if not self.drag: return
        data,mode,initial,start,end=self.drag;kind,scene,obj=data
        t=(self.mapToScene(event.position().toPoint()).x()-148)/self.pps
        delta=t-initial
        if self.snap:
            fps=self.project.get('fps',30);delta=round(delta*fps)/fps
        minimum=0;maximum=scene['duration'] if scene else duration(self.project)
        if mode=='end':
            new_end=min(maximum,max(start+.1,end+delta))
            if kind=='audio': obj['duration']=new_end-start
            else: obj['end']=new_end
        else:
            length=end-start;obj['start']=min(max(0,maximum-length),max(0,start+delta))
            if kind!='audio': obj['end']=obj['start']+length
        self.draw(self.project);self.set_time(max(0,t));self.edited.emit()

    def mouseReleaseEvent(self,event):
        self.drag=None;super().mouseReleaseEvent(event)
