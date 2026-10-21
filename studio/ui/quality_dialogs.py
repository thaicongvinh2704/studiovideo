"""Author reusable contact targets and camera shots without editing project JSON."""
import copy
from PySide6.QtWidgets import (QDialog,QVBoxLayout,QHBoxLayout,QLabel,QTableWidget,
    QComboBox,QDialogButtonBox,QHeaderView)
from .dialogs import spin,button,error,KeyframeDialog
from ..animation import camera_values

class StateTrackDialog(QDialog):
    def __init__(self,obj,field,options,base,duration,parent=None):
        super().__init__(parent);self.obj=obj;self.field=field;self.options=options;self.duration=duration
        self.setWindowTitle('Theo thời gian · '+('Biểu cảm' if field=='expressions' else 'Độ tuổi'));self.resize(500,380)
        layout=QVBoxLayout(self);layout.addWidget(QLabel('Trạng thái giữ từ mốc này đến mốc kế tiếp.'))
        self.table=QTableWidget(0,2);self.table.setHorizontalHeaderLabels(['Giây trong cảnh','Trạng thái']);self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch);layout.addWidget(self.table)
        for k in obj.get(field,[]) or [dict(t=0,v=obj.get(base,options[0]))]:self.add(k)
        row=QHBoxLayout();layout.addLayout(row);button('Thêm mốc',lambda:self.add(dict(t=0,v=options[0])),row);button('Xóa mốc',lambda:self.table.removeRow(self.table.currentRow()),row)
        actions=QDialogButtonBox(QDialogButtonBox.StandardButton.Save|QDialogButtonBox.StandardButton.Cancel)
        actions.accepted.connect(self.commit);actions.rejected.connect(self.reject);layout.addWidget(actions)
    def add(self,k):
        r=self.table.rowCount();self.table.insertRow(r);self.table.setCellWidget(r,0,spin(k['t'],0,self.duration,.1,3))
        v=QComboBox();v.addItems(self.options);v.setCurrentText(k['v']);self.table.setCellWidget(r,1,v)
    def commit(self):
        keys=[dict(t=self.table.cellWidget(r,0).value(),v=self.table.cellWidget(r,1).currentText()) for r in range(self.table.rowCount())]
        if len({k['t'] for k in keys})!=len(keys):error(self,'Hai mốc trạng thái không được trùng thời gian.');return
        self.obj[self.field]=sorted(keys,key=lambda k:k['t']);self.accept()

class ContactDialog(QDialog):
    def __init__(self,obj,scene,parent=None):
        super().__init__(parent);self.obj=obj;self.scene=scene;self.items=copy.deepcopy(obj.get('contacts',[]))
        self.setWindowTitle('Tiếp xúc · IK tay theo nhân vật / điểm trong cảnh');self.resize(1120,470)
        layout=QVBoxLayout(self);layout.addWidget(QLabel('X/Y là điểm trong cảnh khi chọn Tự do. Với nhân vật, X/Y là offset so với khớp đích.'))
        self.table=QTableWidget(0,10);self.table.setHorizontalHeaderLabels(['Tay','Mục tiêu','Khớp','Start','End','X','Y','Blend','Thả','Gập'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch);layout.addWidget(self.table)
        for c in self.items:self.add_row(c)
        row=QHBoxLayout();layout.addLayout(row)
        button('Thêm tiếp xúc',self.add,row);button('Xóa',self.remove,row);button('Keyframe điểm tự do…',self.trajectory,row)
        actions=QDialogButtonBox(QDialogButtonBox.StandardButton.Save|QDialogButtonBox.StandardButton.Cancel)
        actions.accepted.connect(self.commit);actions.rejected.connect(self.reject);layout.addWidget(actions)
    def add(self):
        c=dict(hand='r',start=0,end=self.scene['duration'],x=self.obj['x']+40,y=self.obj['y']-150,blend=.4,release=.4,bend=1)
        self.items.append(c);self.add_row(c)
    def add_row(self,c):
        r=self.table.rowCount();self.table.insertRow(r)
        hand=QComboBox();hand.addItems(['l','r']);hand.setCurrentText(c.get('hand','r'));self.table.setCellWidget(r,0,hand)
        target=QComboBox();target.addItem('Tự do','')
        for o in self.scene['objects']:
            if o['kind']=='character' and o['id']!=self.obj['id']:target.addItem(o['name'],o['id'])
        target.setCurrentIndex(max(0,target.findData(c.get('target',''))));self.table.setCellWidget(r,1,target)
        joint=QComboBox();joint.addItems(['hand_l','hand_r','shoulder_l','shoulder_r','neck','hip']);joint.setCurrentText(c.get('joint','hand_l'));self.table.setCellWidget(r,2,joint)
        x,y=c.get('offset',[0,0]) if c.get('target') else (c.get('x') or 0,c.get('y') or 0)
        for j,val,low,high in [(3,c.get('start',0),0,self.scene['duration']),(4,c.get('end',15),0,self.scene['duration']),
            (5,x,-5000,5000),(6,y,-5000,5000),(7,c.get('blend',.4),0,5),(8,c.get('release',.4),0,5)]:
            self.table.setCellWidget(r,j,spin(val,low,high,.1))
        bend=QComboBox();bend.addItems(['1','-1']);bend.setCurrentText(str(c.get('bend',1)));self.table.setCellWidget(r,9,bend)
    def remove(self):
        r=self.table.currentRow()
        if r>=0:self.items.pop(r);self.table.removeRow(r)
    def trajectory(self):
        r=self.table.currentRow()
        if r<0:return
        if self.table.cellWidget(r,1).currentData():error(self,'Chọn mục tiêu Tự do để tạo quỹ đạo điểm.');return
        item=self.items[r];temp=dict(keys=copy.deepcopy(item.get('keys',{})),x=self.table.cellWidget(r,5).value(),y=self.table.cellWidget(r,6).value())
        if KeyframeDialog(temp,0,self,camera=True).exec():item['keys']=temp['keys']
    def commit(self):
        result=[]
        for r,item in enumerate(self.items):
            c=copy.deepcopy(item);c.update(hand=self.table.cellWidget(r,0).currentText(),joint=self.table.cellWidget(r,2).currentText(),
                start=self.table.cellWidget(r,3).value(),end=self.table.cellWidget(r,4).value(),blend=self.table.cellWidget(r,7).value(),
                release=self.table.cellWidget(r,8).value(),bend=int(self.table.cellWidget(r,9).currentText()))
            if c['end']<=c['start']:error(self,'End phải lớn hơn Start.');return
            target=self.table.cellWidget(r,1).currentData();x=self.table.cellWidget(r,5).value();y=self.table.cellWidget(r,6).value()
            if target:c.update(target=target,offset=[x,y]);c.pop('keys',None)
            else:c.pop('target',None);c.pop('offset',None);c.update(x=x,y=y)
            result.append(c)
        self.obj['contacts']=result;self.accept()

class ShotDialog(QDialog):
    def __init__(self,scene,parent=None):
        super().__init__(parent);self.scene=scene;self.items=copy.deepcopy(scene['camera'].get('shots',[]))
        self.setWindowTitle('Góc máy · Các shot trong cảnh');self.resize(740,430)
        layout=QVBoxLayout(self);layout.addWidget(QLabel('Mỗi shot dùng camera riêng. Để trống danh sách để dùng camera toàn cảnh.'))
        self.table=QTableWidget(0,5);self.table.setHorizontalHeaderLabels(['Start','End','X','Y','Zoom']);self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch);layout.addWidget(self.table)
        for item in self.items:self.add_row(item)
        row=QHBoxLayout();layout.addLayout(row);button('Thêm shot',self.add,row);button('Xóa shot',self.remove,row)
        actions=QDialogButtonBox(QDialogButtonBox.StandardButton.Save|QDialogButtonBox.StandardButton.Cancel)
        actions.accepted.connect(self.commit);actions.rejected.connect(self.reject);layout.addWidget(actions)
    def add(self):
        z,x,y=camera_values(self.scene,0);item=dict(start=0,end=self.scene['duration'],x=x,y=y,zoom=z)
        self.items.append(item);self.add_row(item)
    def add_row(self,item):
        r=self.table.rowCount();self.table.insertRow(r)
        for j,(key,lo,hi,step) in enumerate([('start',0,self.scene['duration'],.1),('end',0,self.scene['duration'],.1),('x',-5000,5000,5),('y',-5000,5000,5),('zoom',.1,8,.05)]):
            self.table.setCellWidget(r,j,spin(item.get(key,{'x':640,'y':360,'zoom':1}.get(key,0)),lo,hi,step))
    def remove(self):
        r=self.table.currentRow()
        if r>=0:self.items.pop(r);self.table.removeRow(r)
    def commit(self):
        result=[]
        for r,item in enumerate(self.items):
            c=copy.deepcopy(item)
            for j,key in enumerate(['start','end','x','y','zoom']):c[key]=self.table.cellWidget(r,j).value()
            if c['end']<=c['start']:error(self,'Shot cần End lớn hơn Start.');return
            result.append(c)
        result.sort(key=lambda c:c['start'])
        if any(a['end']>b['start'] for a,b in zip(result,result[1:])):error(self,'Các shot không được chồng thời gian.');return
        self.scene['camera']['shots']=result;self.accept()
