"""Visual pose/library pickers and editable parent/pivot controls."""
import copy
import math
from PySide6.QtCore import Qt,QSize
from PySide6.QtGui import QImage,QPainter,QPixmap,QIcon,QColor
from PySide6.QtWidgets import (QDialog,QVBoxLayout,QHBoxLayout,QListWidget,QListWidgetItem,
    QDialogButtonBox,QLineEdit,QLabel,QComboBox,QFormLayout)
from .dialogs import spin,error


class PosePicker(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent);self.setWindowTitle('Tư thế người dẫn · Thư viện hình');self.resize(860,600)
        from ..explainer import POSES,presenter
        from ..renderer import Renderer
        self.pose=None;layout=QVBoxLayout(self);self.box=QListWidget()
        self.box.setViewMode(QListWidget.ViewMode.IconMode);self.box.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.box.setIconSize(QSize(125,154));self.box.setGridSize(QSize(155,190));self.box.setWordWrap(True)
        renderer=Renderer()
        for name,label in POSES.items():
            im=QImage(140,180,QImage.Format.Format_ARGB32_Premultiplied);im.fill(QColor('#ffffff'))
            painter=QPainter(im);painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            renderer.character(painter,presenter(70,173,.77,name),0);painter.end()
            item=QListWidgetItem(QIcon(QPixmap.fromImage(im)),label);item.setData(Qt.ItemDataRole.UserRole,name);self.box.addItem(item)
        layout.addWidget(self.box);layout.addWidget(QLabel('Áp dụng tại playhead; chuyển tư thế có giữ hình và nội suy mềm.'))
        buttons=QDialogButtonBox(QDialogButtonBox.StandardButton.Ok|QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.choose);buttons.rejected.connect(self.reject);layout.addWidget(buttons)
        self.box.itemDoubleClicked.connect(lambda _:self.choose())
    def choose(self):
        item=self.box.currentItem()
        if item:self.pose=item.data(Qt.ItemDataRole.UserRole);self.accept()


class ArtPicker(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent);self.setWindowTitle('Hình minh họa vector · Offline');self.resize(850,620)
        from ..asset_library import CATALOG,asset
        self.file=None;layout=QVBoxLayout(self);search=QLineEdit();search.setPlaceholderText('Tìm hình: bản đồ, lịch sử, thuyền, công nghệ…');layout.addWidget(search)
        self.box=QListWidget();self.box.setViewMode(QListWidget.ViewMode.IconMode);self.box.setResizeMode(QListWidget.ResizeMode.Adjust)
        self.box.setIconSize(QSize(120,96));self.box.setGridSize(QSize(160,130));layout.addWidget(self.box)
        for name,(title,tags) in CATALOG.items():
            item=QListWidgetItem(QIcon(asset(name)),title);item.setData(Qt.ItemDataRole.UserRole,asset(name));item.setData(Qt.ItemDataRole.UserRole+1,title+' '+tags);self.box.addItem(item)
        def filter_items(value):
            from ..explainer import normalized
            for i in range(self.box.count()):
                item=self.box.item(i);item.setHidden(normalized(value) not in normalized(item.data(Qt.ItemDataRole.UserRole+1)))
        search.textChanged.connect(filter_items)
        buttons=QDialogButtonBox(QDialogButtonBox.StandardButton.Ok|QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.choose);buttons.rejected.connect(self.reject);layout.addWidget(buttons)
        self.box.itemDoubleClicked.connect(lambda _:self.choose())
    def choose(self):
        item=self.box.currentItem()
        if item:self.file=item.data(Qt.ItemDataRole.UserRole);self.accept()


class ParentPicker(QDialog):
    def __init__(self,obj,scene,t,fps,parent=None):
        super().__init__(parent);self.setWindowTitle('Lớp cha và điểm xoay');self.obj=obj;self.scene=scene;self.t=t;self.fps=fps
        layout=QVBoxLayout(self);form=QFormLayout();layout.addLayout(form)
        self.parent_box=QComboBox();self.parent_box.addItem('Không có','')
        for other in scene['objects']:
            if other['id']!=obj['id']:self.parent_box.addItem(other['name'],other['id'])
        self.parent_box.setCurrentIndex(max(0,self.parent_box.findData(obj.get('parent',''))));form.addRow('Lớp cha',self.parent_box)
        self.px=spin(obj.get('pivot',[0,0])[0],-10000,10000,1)
        self.py=spin(obj.get('pivot',[0,0])[1],-10000,10000,1)
        form.addRow('Điểm xoay X',self.px);form.addRow('Điểm xoay Y',self.py)
        layout.addWidget(QLabel('Đổi cha giữ chuyển động trên lưới frame bằng keyframe.​\nĐiểm xoay tính bằng tọa độ trong lớp.'))
        buttons=QDialogButtonBox(QDialogButtonBox.StandardButton.Save|QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.commit);buttons.rejected.connect(self.reject);layout.addWidget(buttons)
    def commit(self):
        from ..hierarchy import world_states,to_parent
        try:
            old=copy.deepcopy(self.scene['objects']);staged=copy.deepcopy(old);target=next(o for o in staged if o['id']==self.obj['id'])
            target['parent']=self.parent_box.currentData();world_states(staged,self.t)
            if target['parent']!=self.obj.get('parent',''):
                # Contact targets are world-space. Reparenting a constrained character would
                # change their meaning; require detaching the constraint first.
                if target.get('contacts'):raise ValueError('Bỏ contact của nhân vật trước khi đổi lớp cha.')
                frames=max(1,math.ceil(self.scene['duration']*self.fps))
                if frames>60000:raise ValueError('Cảnh quá dài để đổi lớp cha. Hãy tách cảnh trước.')
                keys={k:[] for k in ('x','y','scale','rotation','opacity')}
                for frame in range(frames+1):
                    t=frame/self.fps;was=world_states(old,t)[target['id']]
                    x,y=to_parent((was['x'],was['y']),target,staged,t)
                    ps=world_states(staged,t).get(target.get('parent'),dict(rotation=0,scale=1,opacity=1))
                    for key,value in dict(x=x,y=y,rotation=was['rotation']-ps['rotation'],scale=was['scale']/ps['scale'],opacity=was['opacity']/ps['opacity'] if ps['opacity'] else 0).items():keys[key].append(dict(t=t,v=value))
                target.setdefault('keys',{}).update(keys)
            target['pivot']=[self.px.value(),self.py.value()]
            self.obj.update(target);self.accept()
        except Exception as exc:error(self,exc)


class AppearancePicker(QDialog):
    def __init__(self,obj,parent=None):
        super().__init__(parent);self.obj=obj;self.setWindowTitle('Diện mạo người dẫn');layout=QVBoxLayout(self);form=QFormLayout();layout.addLayout(form);self.fields={}
        for key,label,default in [('shirt','Áo','#ffffff'),('pants','Quần','#6695ba'),('skin_color','Da','#ffdbb5'),('color','Nét','#191d20'),('shoes','Giày','#eef0ee')]:
            widget=QLineEdit(obj.get(key,default));form.addRow(label,widget);self.fields[key]=widget
        from ..animation import EXPRESSIONS
        self.expression=QComboBox();self.expression.addItems(EXPRESSIONS);self.expression.setCurrentText(obj.get('expression','happy'));form.addRow('Biểu cảm mặc định',self.expression)
        layout.addWidget(QLabel('Biểu cảm theo mốc thời gian vẫn ưu tiên hơn biểu cảm mặc định.'))
        buttons=QDialogButtonBox(QDialogButtonBox.StandardButton.Save|QDialogButtonBox.StandardButton.Cancel);buttons.accepted.connect(self.commit);buttons.rejected.connect(self.reject);layout.addWidget(buttons)
    def commit(self):
        if any(not QColor(w.text()).isValid() for w in self.fields.values()):error(self,'Nhập màu hợp lệ, ví dụ #6695ba.');return
        self.obj.update({k:w.text() for k,w in self.fields.items()});self.obj['expression']=self.expression.currentText();self.accept()
