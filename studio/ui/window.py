import copy
import json
import math
import shutil
import time
from pathlib import Path
from PySide6.QtCore import Qt,QTimer,QSize,QEvent
from PySide6.QtGui import QAction,QKeySequence,QIcon,QPixmap,QColor
from PySide6.QtWidgets import (QMainWindow,QWidget,QVBoxLayout,QHBoxLayout,QFormLayout,QSplitter,
    QTabWidget,QListWidget,QListWidgetItem,QLabel,QPushButton,QToolBar,QFileDialog,QMessageBox,
    QInputDialog,QComboBox,QCheckBox,QLineEdit,QScrollArea,QSlider,QDialog,QDialogButtonBox,
    QProgressDialog,QGroupBox,QMenu,QStyle,QApplication,QAbstractSpinBox,QTextEdit,QPlainTextEdit)
from ..project import (new_project,new_scene,new_object,uid,load,save,duration,scene_at,resequence,
                       History,missing,pack,unpack,resolve)
from ..animation import ACTIONS,LABELS,EXPRESSIONS,state,sample,stepped,age_at
from ..renderer import Renderer
from ..demo import demo
from ..subtitles import read,write,stamp
from ..exporter import export_video,export_cached,binary
from .canvas import Canvas
from .timeline import Timeline
from .dialogs import (spin,button,error,SubtitleDialog,KeyframeDialog,RigDialog,AttachmentDialog,
                      AudioDialog,VoiceDialog)
from .workers import Worker
from .audio_preview import AudioPreview
from .quality_dialogs import ContactDialog,ShotDialog,StateTrackDialog
from .explainer_actions import ExplainerActions

class StudioWindow(ExplainerActions,QMainWindow):
    def __init__(self,app_root,project_path=None):
        super().__init__();self.app_root=Path(app_root);self.history=History();self.renderer=Renderer()
        if not project_path:
            candidate=self.app_root/'examples'/'ink_showcase'/'project.json'
            if not candidate.exists():candidate=self.app_root/'examples'/'explainer_showcase'/'project.json'
            if not candidate.exists():candidate=self.app_root/'examples'/'yellow_umbrella_v2'/'project.json'
            if candidate.exists():project_path=candidate
        self.project=load(project_path) if project_path else demo()
        self.path=Path(project_path) if project_path else None
        self.root=self.path.parent if self.path else self.app_root/'projects'/'working_demo'
        self.root.mkdir(parents=True,exist_ok=True)
        self.selected_id='';self.scene_index=0;self.t=0.;self.playing=False;self.dirty=False;self.loading=False
        self.export_worker=None;self.project_worker=None;self.clock_origin=0.;self.clock_time=0.
        self.setWindowTitle('STICKMAN ANIMATION STUDIO');self.resize(1366,768);self.setMinimumSize(1050,650)
        self.audio_preview=AudioPreview(self)
        config_path=self.app_root/'config.json'
        self.config=json.loads(config_path.read_text(encoding='utf-8')) if config_path.exists() else {}
        self.project.setdefault('encoder_threads',min(2,max(1,int(self.config.get('encoder_threads',2)))))
        self.build_toolbar();self.build_ui()
        self.quality.setCurrentIndex({'low':0,'medium':1,'high':2}.get(self.config.get('preview_quality','low'),0))
        self.refresh()
        self.timer=QTimer(self);self.timer.setTimerType(Qt.TimerType.PreciseTimer);self.timer.setSingleShot(True);self.timer.timeout.connect(self.tick)
        self.preview_frames=0;self.preview_late=0
        self.autosave_timer=QTimer(self);self.autosave_timer.setInterval(max(10,int(self.config.get('autosave_seconds',60)))*1000);self.autosave_timer.timeout.connect(self.autosave);self.autosave_timer.start()
        self.add_shortcut('Space',self.toggle_play);self.add_shortcut('Ctrl+S',self.save_project)
        self.add_shortcut('Ctrl+Z',self.undo);self.add_shortcut('Ctrl+Y',self.redo)
        self.add_shortcut('Ctrl+Shift+S',lambda:self.save_project(True))
        self.add_shortcut('Left',lambda:self.nudge_frame(-1));self.add_shortcut('Right',lambda:self.nudge_frame(1))
        QApplication.instance().installEventFilter(self)
        self.statusBar().showMessage('Sẵn sàng · Video minh họa · Nhập kịch bản + voice để bắt đầu')

    def add_shortcut(self,key,fn):
        action=QAction(self);action.setShortcut(QKeySequence(key));action.triggered.connect(fn);self.addAction(action)
    def eventFilter(self,obj,event):
        if event.type()==QEvent.Type.ShortcutOverride and event.key()==Qt.Key.Key_Space:
            focused=QApplication.focusWidget()
            if isinstance(focused,(QLineEdit,QAbstractSpinBox,QTextEdit,QPlainTextEdit)):
                event.accept();return True
        return super().eventFilter(obj,event)
    def build_toolbar(self):
        toolbar=QToolBar('Studio',self);toolbar.setMovable(False);toolbar.setIconSize(QSize(18,18));toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon);self.addToolBar(toolbar)
        title=QLabel('  STICKMAN  /  ANIMATION STUDIO  ');title.setObjectName('heading');toolbar.addWidget(title)
        actions=[('Mới',self.create_project,QStyle.StandardPixmap.SP_FileIcon),('Mở',self.open_project,QStyle.StandardPixmap.SP_DirOpenIcon),
                 ('Lưu',self.save_project,QStyle.StandardPixmap.SP_DialogSaveButton),('Lưu thành…',lambda:self.save_project(True),None)]
        for name,fn,icon in actions:
            a=QAction(self.style().standardIcon(icon) if icon else QIcon(),name,self);a.triggered.connect(fn);toolbar.addAction(a)
        imp=QPushButton('Nhập ▾');menu=QMenu(imp)
        for title,fn in [('SRT…',self.import_srt),('Background…',lambda:self.import_image('background')),
                         ('Ảnh chụp thật…',lambda:self.import_image('photo')),('Hình vẽ vật thể / sơ đồ…',lambda:self.import_image('image')),
                         ('Nhân vật vẽ từ tệp · cần QC…',lambda:self.import_image('character_image')),('Ảnh tham chiếu…',lambda:self.import_image('reference')),
                         ('Audio…',self.audio_dialog),('Gói project ZIP…',self.import_package)]:menu.addAction(title,fn)
        imp.setMenu(menu);toolbar.addWidget(imp)
        toolbar.addSeparator()
        for title,fn in [('↶',self.undo),('↷',self.redo),('Cài đặt',self.settings),('Xuất gói',self.export_package)]:
            a=QAction(title,self);a.triggered.connect(fn);toolbar.addAction(a)
        export=QPushButton('Xuất MP4');export.setObjectName('primary');export.clicked.connect(self.export_dialog);toolbar.addWidget(export)
        tools=QToolBar('Minh họa',self);tools.setMovable(False);self.addToolBarBreak();self.addToolBar(tools)
        for title,fn in [('Bàn vẽ…',self.drawing_desk),('Kịch bản + voice…',self.story_wizard),('Người dẫn',lambda:self.add_graphic('presenter')),('Chữ',lambda:self.add_graphic('text')),
            ('Hình / mũi tên',lambda:self.add_graphic('shape')),('Sửa nội dung…',self.graphic_dialog),('Tư thế…',self.pose_picker),('Diện mạo…',self.appearance_picker),
            ('Bố cục…',self.add_layout),('Thư viện hình…',self.art_picker),('Cha / điểm xoay…',self.parent_picker),('Nhóm…',self.group_dialog),('Nhân bản lớp',self.duplicate_object),('Cắt lớp',self.split_object),('Waveform',self.analyze_voice)]:
            a=QAction(title,self);a.triggered.connect(fn);tools.addAction(a)

    def build_ui(self):
        outer=QSplitter(Qt.Orientation.Vertical);self.setCentralWidget(outer)
        body=QSplitter(Qt.Orientation.Horizontal);outer.addWidget(body)
        left=QWidget();lv=QVBoxLayout(left);lv.setContentsMargins(8,8,8,8)
        h=QLabel('ASSET LIBRARY');h.setObjectName('heading');lv.addWidget(h)
        self.assets=QTabWidget();lv.addWidget(self.assets,2)
        self.asset_lists={}
        specs={'Nhân vật':['Người dẫn · Nét minh họa','Father','Mother','Son · Trẻ em','Son · Thiếu niên','Son · Trưởng thành','Father · Lớn tuổi'],
               'Actions':LABELS,'Nền':['Studio trắng','Phố','Mưa','Nhà'],
               'Đạo cụ':['umbrella','chair','table','phone','book','backpack','door','bag','towel'],
               'Hiệu ứng':['rain','leaves','snow','ripple','fade','flash','shake'], 'Reference':[]}
        for title,items in specs.items():
            box=QListWidget();box.addItems(items);box.itemDoubleClicked.connect(lambda item,k=title:self.add_asset(k,item.text()))
            self.asset_lists[title]=box;self.assets.addTab(box,title)
        button('Thêm mục đang chọn',self.add_selected_asset,lv)
        h=QLabel('CẢNH / SCENES');h.setObjectName('heading');lv.addWidget(h)
        self.scenes_list=QListWidget();self.scenes_list.setIconSize(QSize(96,54));self.scenes_list.currentRowChanged.connect(self.select_scene);lv.addWidget(self.scenes_list,3)
        row=QHBoxLayout();lv.addLayout(row)
        button('+',self.add_scene,row);button('Nhân bản',self.duplicate_scene,row);button('Xóa',self.delete_scene,row)
        row=QHBoxLayout();lv.addLayout(row);button('↑',lambda:self.reorder_scene(-1),row);button('↓',lambda:self.reorder_scene(1),row)
        row=QHBoxLayout();lv.addLayout(row)
        button('Voice Studio',self.voice_dialog,row);button('SRT',self.subtitle_dialog,row);button('Audio',self.audio_dialog,row)
        body.addWidget(left)
        center=QWidget();cv=QVBoxLayout(center);cv.setContentsMargins(5,8,5,5)
        top=QHBoxLayout();cv.addLayout(top);h=QLabel('PREVIEW');h.setObjectName('heading');top.addWidget(h);top.addStretch()
        self.quality=QComboBox();self.quality.addItems(['Low · 480p','Medium · 720p','High · 1080p']);self.quality.currentIndexChanged.connect(self.preview);top.addWidget(self.quality)
        self.rig_check=QCheckBox('Xương');self.rig_check.toggled.connect(self.preview);top.addWidget(self.rig_check)
        self.effects_check=QCheckBox('Hiệu ứng');self.effects_check.setChecked(True);self.effects_check.toggled.connect(self.preview);top.addWidget(self.effects_check)
        self.safe_check=QCheckBox('Safe');self.safe_check.toggled.connect(self.preview);top.addWidget(self.safe_check)
        self.canvas=Canvas();cv.addWidget(self.canvas,1)
        self.canvas.selected.connect(self.select_object);self.canvas.edit_started.connect(self.remember);self.canvas.moved.connect(self.move_object)
        transport=QHBoxLayout();cv.addLayout(transport)
        button('|◀',lambda:self.set_time(self.current_scene()['start']),transport)
        self.play_button=button('▶ Phát',self.toggle_play,transport,True)
        button('■',self.stop,transport);button('▶|',lambda:self.set_time(self.current_scene()['start']+self.current_scene()['duration']-.001),transport)
        self.time_label=QLabel('00:00:00,000');transport.addWidget(self.time_label);transport.addStretch()
        zoom=QComboBox();zoom.addItems(['Fit','125%','150%','200%']);zoom.currentIndexChanged.connect(lambda i:self.preview_zoom(i));transport.addWidget(zoom)
        self.scrub=QSlider(Qt.Orientation.Horizontal);self.scrub.sliderMoved.connect(lambda value:self.set_time(value/1000));cv.addWidget(self.scrub)
        body.addWidget(center)
        right=QScrollArea();right.setWidgetResizable(True);panel=QWidget();right.setWidget(panel);pv=QVBoxLayout(panel)
        h=QLabel('PROPERTIES');h.setObjectName('heading');pv.addWidget(h)
        self.object_list=QComboBox();self.object_list.currentIndexChanged.connect(self.object_combo);pv.addWidget(self.object_list)
        self.object_fields={};form=QFormLayout();pv.addLayout(form)
        self.name=QLineEdit();form.addRow('Tên',self.name)
        for key,title,value,minv,maxv,step in [('x','X',640,-5000,5000,5),('y','Y',575,-5000,5000,5),
            ('scale','Scale',1,.05,10,.05),('rotation','Góc °',0,-360,360,5),('opacity','Opacity',1,0,1,.1),
            ('layer','Layer',10,-100,100,1),('start','Bắt đầu (s)',0,0,86400,.5),('end','Kết thúc (s)',15,.1,86400,.5),
            ('speed','Tốc độ',1,.1,5,.1),('amplitude','Biên độ',1,0,3,.1)]:
            w=spin(value,minv,maxv,step);form.addRow(title,w);self.object_fields[key]=w
        self.action=QComboBox();self.action.addItems(LABELS);form.addRow('Chuyển động',self.action)
        self.expression=QComboBox();self.expression.addItems(EXPRESSIONS);form.addRow('Biểu cảm',self.expression)
        self.age=QComboBox();self.age.addItems(['child','teen','adult','elderly']);form.addRow('Độ tuổi',self.age)
        self.color=QLineEdit('#242938');form.addRow('Màu (#hex)',self.color)
        self.autokey=QCheckBox('Đặt keyframe transform tại playhead');pv.addWidget(self.autokey)
        button('Áp dụng thuộc tính',self.apply_properties,pv,True)
        row=QHBoxLayout();pv.addLayout(row);button('Keyframe…',self.keyframe_dialog,row);button('Rig / IK…',self.rig_dialog,row)
        button('Đặt action từ playhead…',self.motion_dialog,pv)
        row=QHBoxLayout();pv.addLayout(row);button('Lưu motion preset',self.save_motion,row);button('Nạp preset',self.load_motion,row)
        button('Gắn / trao đạo cụ…',self.attachment_dialog,pv)
        button('Tiếp xúc tay / ôm…',self.contact_dialog,pv)
        button('Biểu cảm / tuổi theo thời gian…',self.state_track_dialog,pv)
        button('Xóa đối tượng',self.delete_object,pv)
        scene_box=QGroupBox('Cảnh đang chọn');pv.addWidget(scene_box);sf=QFormLayout(scene_box)
        self.scene_name=QLineEdit();sf.addRow('Tên cảnh',self.scene_name);self.scene_duration=spin(15,.1,86400,1);sf.addRow('Độ dài (s)',self.scene_duration)
        button('Áp dụng cảnh',self.apply_scene,sf)
        button('Camera keyframes…',self.camera_dialog,sf)
        button('Góc máy trong cảnh…',self.shot_dialog,sf)
        self.follow=QComboBox();sf.addRow('Camera theo',self.follow);self.follow.currentIndexChanged.connect(self.camera_follow)
        pv.addStretch();body.addWidget(right);body.setSizes([250,820,290]);body.setStretchFactor(1,1)
        bottom=QWidget();bv=QVBoxLayout(bottom);bv.setContentsMargins(6,5,6,5)
        row=QHBoxLayout();bv.addLayout(row);h=QLabel('TIMELINE');h.setObjectName('heading');row.addWidget(h)
        row.addWidget(QLabel('  Kéo clip / mép phải · Snap theo frame · ← → từng frame  '));row.addStretch()
        snap=QCheckBox('Snap');snap.setChecked(True);snap.toggled.connect(lambda v:setattr(self.timeline,'snap',v));row.addWidget(snap)
        slider=QSlider(Qt.Orientation.Horizontal);slider.setRange(2,90);slider.setValue(14);slider.setMaximumWidth(180)
        slider.valueChanged.connect(self.timeline_zoom);row.addWidget(QLabel('Zoom'));row.addWidget(slider)
        self.timeline=Timeline();self.timeline.seek.connect(self.set_time);self.timeline.selected.connect(self.timeline_select)
        self.timeline.edit_started.connect(self.remember);self.timeline.edited.connect(self.timeline_edit);bv.addWidget(self.timeline)
        outer.addWidget(bottom);outer.setSizes([505,230]);outer.setStretchFactor(0,1)

    def current_scene(self):return self.project['scenes'][min(max(0,self.scene_index),len(self.project['scenes'])-1)]
    def current_object(self):return next((o for o in self.current_scene()['objects'] if o['id']==self.selected_id),None)
    def remember(self):self.history.push(self.project)
    def changed(self,full=True):
        self.dirty=True;self.setWindowTitle(self.project['name']+' * · STICKMAN ANIMATION STUDIO')
        if full:self.refresh()
        else:self.preview()
    def refresh(self):
        self.loading=True
        self.scenes_list.clear()
        for s in self.project['scenes']:
            item=QListWidgetItem(f"{s['name']}\n{stamp(s['start'])}  /  {s['duration']:g}s")
            try:item.setIcon(QIcon(QPixmap.fromImage(self.renderer.frame(self.project,self.root,s['start']+min(1,s['duration']/2),160,90,burn=False,effects=False))))
            except Exception:pass
            self.scenes_list.addItem(item)
        self.scenes_list.setCurrentRow(self.scene_index)
        self.timeline.draw(self.project);self.timeline.set_time(self.t)
        self.scrub.setRange(0,round(duration(self.project)*1000))
        self.asset_lists['Reference'].clear()
        for r in self.project.get('references',[]):self.asset_lists['Reference'].addItem(r['name'])
        self.loading=False;self.update_properties();self.preview()
    def update_properties(self):
        self.loading=True;s=self.current_scene();self.object_list.clear();self.object_list.addItem('Chọn đối tượng trên canvas','')
        for o in sorted(s['objects'],key=lambda o:o['layer']):self.object_list.addItem(f"{o['layer']:g} · {o['name']}",o['id'])
        self.object_list.setCurrentIndex(max(0,self.object_list.findData(self.selected_id)))
        obj=self.current_object()
        if obj:
            self.name.setText(obj['name']);_,local=scene_at(self.project,self.t)
            values=state(obj,local)
            for key,w in self.object_fields.items():w.setValue(values.get(key,obj.get(key,1)))
            self.action.setCurrentIndex(ACTIONS.index(obj.get('action','idle')))
            self.expression.setCurrentText(stepped(obj.get('expressions',[]),local,obj.get('expression','normal')));self.age.setCurrentText(age_at(obj,local));self.color.setText(obj.get('color','#242938'))
        self.scene_name.setText(s['name']);self.scene_duration.setValue(s['duration'])
        self.follow.clear();self.follow.addItem('Statique','')
        for o in s['objects']:
            if o['kind']=='character':self.follow.addItem(o['name'],o['id'])
        self.follow.setCurrentIndex(max(0,self.follow.findData(s['camera'].get('follow',''))))
        self.loading=False
    def preview(self,*args):
        if not hasattr(self,'canvas'):return
        s,local=scene_at(self.project,min(self.t,max(0,duration(self.project)-.00001)))
        base=[854,1280,1920][self.quality.currentIndex()]
        h=round(base*self.project['height']/self.project['width'])
        try:
            im=self.renderer.frame(self.project,self.root,self.t,base,h,rig=self.rig_check.isChecked(),effects=self.effects_check.isChecked())
            self.canvas.show_frame(im,s,local,self.selected_id,self.safe_check.isChecked())
        except Exception as exc:
            self.statusBar().showMessage(str(exc));return
        self.time_label.setText(stamp(self.t)+' / '+stamp(duration(self.project)))
        self.scrub.setValue(round(self.t*1000));self.timeline.set_time(self.t)
    def preview_zoom(self,i):self.canvas.zoom=[1,1.25,1.5,2][i];self.canvas.fit()
    def set_time(self,t):
        self.t=min(max(0,float(t)),max(0,duration(self.project)-.00001))
        s,local=scene_at(self.project,self.t)
        if s:
            index=self.project['scenes'].index(s)
            if index!=self.scene_index:
                self.scene_index=index;self.selected_id='';self.loading=True;self.scenes_list.setCurrentRow(index);self.loading=False;self.update_properties()
        if self.playing:self.clock_origin=time.perf_counter();self.clock_time=self.t
        self.preview();self.audio_preview.update(self.project,self.root,self.t,self.playing)
    def tick(self):
        t=self.clock_time+time.perf_counter()-self.clock_origin
        if t>=duration(self.project):self.stop();return
        # Playback is measured by monotonic time, never by refresh count.
        fps=self.project.get('fps',30);self.t=math.floor(t*fps)/fps;s,local=scene_at(self.project,self.t)
        if s and self.project['scenes'].index(s)!=self.scene_index:
            self.scene_index=self.project['scenes'].index(s);self.selected_id='';self.loading=True;self.scenes_list.setCurrentRow(self.scene_index);self.loading=False;self.update_properties()
        self.preview();self.audio_preview.update(self.project,self.root,t,True)
        self.preview_frames+=1
        elapsed=self.clock_time+time.perf_counter()-self.clock_origin
        if elapsed-self.t>1/fps:self.preview_late+=1
        self.timer.start(max(1,math.ceil(((math.floor(elapsed*fps)+1)/fps-elapsed)*1000)))
    def toggle_play(self):
        self.playing=not self.playing;self.play_button.setText('Ⅱ Tạm dừng' if self.playing else '▶ Phát')
        if self.playing:self.clock_origin=time.perf_counter();self.clock_time=self.t;self.preview_frames=0;self.preview_late=0;self.timer.start(0)
        else:self.timer.stop();self.audio_preview.update(self.project,self.root,self.t,False)
    def stop(self):
        self.playing=False;self.timer.stop();self.play_button.setText('▶ Phát');self.audio_preview.stop();self.set_time(self.current_scene()['start'])
    def select_scene(self,index):
        if self.loading or index<0:return
        self.scene_index=index;self.selected_id='';self.set_time(self.current_scene()['start']);self.update_properties()
    def select_object(self,ident):self.selected_id=ident;self.update_properties();self.preview()
    def object_combo(self,index):
        if not self.loading:self.select_object(self.object_list.currentData() or '')
    def timeline_select(self,scene,ident):
        self.scene_index=next(i for i,s in enumerate(self.project['scenes']) if s['id']==scene);self.selected_id=ident
        self.loading=True;self.scenes_list.setCurrentRow(self.scene_index);self.loading=False;self.update_properties()
    def timeline_zoom(self,value):
        if hasattr(self,'timeline'):self.timeline.pps=value;self.timeline.draw(self.project);self.timeline.set_time(self.t)
    def timeline_edit(self):self.changed(False);self.update_properties()
    def move_object(self,ident,x,y):
        o=self.current_object()
        if not o:return
        t=self.t-self.current_scene()['start']
        from ..hierarchy import to_parent
        x,y=to_parent((x,y),o,self.current_scene()['objects'],t)
        old=state(o,t);dx=x-old['x'];dy=y-old['y']
        if o.get('group'):
            for peer in self.current_scene()['objects']:
                if peer['id']==o['id'] or peer.get('group')!=o['group'] or peer.get('locked'):continue
                current=state(peer,t)
                for key,value in [('x',current['x']+dx),('y',current['y']+dy)]:
                    if self.autokey.isChecked() or peer.get('keys',{}).get(key):self.put_key(peer,key,t,value)
                    else:peer[key]=value
        for key,value in [('x',x),('y',y)]:
            if self.autokey.isChecked() or o.get('keys',{}).get(key):self.put_key(o,key,t,value)
            else:o[key]=value
        self.changed(False);self.update_properties()
    def put_key(self,o,key,t,value):
        keys=o.setdefault('keys',{}).setdefault(key,[]);keys[:]=[k for k in keys if abs(k['t']-t)>.001]
        keys.append(dict(t=round(t,3),v=value,ease='ease_in_out'));keys.sort(key=lambda k:k['t'])
    def apply_properties(self):
        o=self.current_object()
        if not o:return
        if self.object_fields['end'].value()<=self.object_fields['start'].value():error(self,'Kết thúc phải lớn hơn bắt đầu.');return
        if not QColor(self.color.text()).isValid():error(self,'Màu không hợp lệ.');return
        self.remember();t=self.t-self.current_scene()['start']
        o['name']=self.name.text();o['color']=self.color.text()
        for key,w in self.object_fields.items():
            if self.autokey.isChecked() and key in ('x','y','scale','rotation','opacity'):self.put_key(o,key,t,w.value())
            else:
                o[key]=w.value()
                if key in o.get('keys',{}) and key in ('x','y','scale','rotation','opacity'):
                    self.put_key(o,key,t,w.value())
        o['action']=ACTIONS[self.action.currentIndex()]
        for base,track,value in [('expression','expressions',self.expression.currentText()),('age','ages',self.age.currentText())]:
            if self.autokey.isChecked() or o.get(track):
                frames=o.setdefault(track,[]);frames[:]=[k for k in frames if abs(k['t']-t)>.001];frames.append(dict(t=t,v=value));frames.sort(key=lambda k:k['t'])
            else:o[base]=value
        self.changed()
    def add_selected_asset(self):
        title=self.assets.tabText(self.assets.currentIndex());item=self.asset_lists[title].currentItem()
        if item:self.add_asset(title,item.text())
    def add_asset(self,title,value):
        s=self.current_scene()
        if title=='Nhân vật' and value.startswith('Người dẫn'):self.add_graphic('presenter');return
        if title=='Reference':
            r=next((r for r in self.project['references'] if r['name']==value),None)
            if r:
                d=QDialog(self);d.setWindowTitle('Ảnh tham chiếu · Ảnh phẳng không có rig');v=QVBoxLayout(d);label=QLabel()
                label.setPixmap(QPixmap(str(resolve(self.root,r['file']))).scaled(800,550,Qt.AspectRatioMode.KeepAspectRatio));v.addWidget(label);d.exec()
            return
        self.remember()
        if title=='Nhân vật':
            preset='father' if value.startswith('Father') else 'mother' if value.startswith('Mother') else 'son'
            o=new_object('character',preset);o['name']=value;o['end']=s['duration'];o['character_id']=preset
            o['age']='child' if 'Trẻ em' in value else 'teen' if 'Thiếu niên' in value else 'elderly' if 'Lớn tuổi' in value else 'adult'
            s['objects'].append(o);self.selected_id=o['id']
        elif title=='Đạo cụ':
            o=new_object('prop',value);o['color']='#f6c945';o['end']=s['duration'];o['layer']=20;s['objects'].append(o);self.selected_id=o['id']
        elif title=='Actions':
            o=self.current_object()
            if o and o['kind']=='character':o['action']=ACTIONS[LABELS.index(value)];o['motions']=[]
        elif title=='Nền':s['background']=['white','street','rain','home'][['Studio trắng','Phố','Mưa','Nhà'].index(value)];s.pop('background_file',None)
        elif title=='Hiệu ứng':
            if value in s['effects']:s['effects'].remove(value)
            else:s['effects'].append(value)
        self.changed()
    def add_scene(self):
        self.remember();self.project['scenes'].insert(self.scene_index+1,new_scene());self.scene_index+=1;resequence(self.project);self.t=self.current_scene()['start'];self.selected_id='';self.changed()
    def duplicate_scene(self):
        self.remember();source=self.current_scene();s=copy.deepcopy(source);s['id']=uid();s['name']+=' (bản sao)';mapping={o['id']:uid() for o in s['objects']}
        for track in ('audio','subtitles'):
            clones=[]
            for clip in self.project[track]:
                if clip.get('scene_id')==source['id']:
                    c=copy.deepcopy(clip);c['id']=uid();c['scene_id']=s['id'];clones.append(c)
            self.project[track]+=clones
        for o in s['objects']:
            o['id']=mapping[o['id']]
            if o.get('parent'):o['parent']=mapping.get(o['parent'],o['parent'])
            for a in o.get('attachment',[]):a['character']=mapping.get(a['character'],a['character'])
            for c in o.get('contacts',[]):
                if c.get('target'):c['target']=mapping.get(c['target'],c['target'])
        for shot in s['camera'].get('shots',[]):
            if shot.get('follow'):shot['follow']=mapping.get(shot['follow'],shot['follow'])
        s['camera']['follow']=mapping.get(s['camera'].get('follow'),s['camera'].get('follow',''))
        self.project['scenes'].insert(self.scene_index+1,s);self.scene_index+=1;resequence(self.project);self.t=s['start'];self.selected_id='';self.changed()
    def delete_scene(self):
        if len(self.project['scenes'])<=1:error(self,'Project cần ít nhất một cảnh.');return
        self.remember();removed=self.project['scenes'].pop(self.scene_index)
        for track in ('audio','subtitles'):self.project[track]=[c for c in self.project[track] if c.get('scene_id')!=removed['id']]
        self.scene_index=min(self.scene_index,len(self.project['scenes'])-1);resequence(self.project);self.t=self.current_scene()['start'];self.selected_id='';self.changed()
    def reorder_scene(self,delta):
        i=self.scene_index;j=i+delta
        if not 0<=j<len(self.project['scenes']):return
        self.remember();self.project['scenes'][i],self.project['scenes'][j]=self.project['scenes'][j],self.project['scenes'][i];self.scene_index=j;resequence(self.project);self.t=self.current_scene()['start'];self.changed()
    def apply_scene(self):
        self.remember();s=self.current_scene();s['name']=self.scene_name.text();old=s['duration'];s['duration']=self.scene_duration.value()
        for o in s['objects']:
            if abs(o['end']-old)<.001:o['end']=s['duration']
        for track in ('audio','subtitles'):
            kept=[]
            for clip in self.project[track]:
                if clip.get('scene_id')==s['id']:
                    limit=s['start']+s['duration']
                    if clip['start']>=limit:continue
                    if track=='audio':clip['duration']=min(clip['duration'],limit-clip['start'])
                    else:clip['end']=min(clip['end'],limit)
                kept.append(clip)
            self.project[track]=kept
        resequence(self.project);self.set_time(s['start']);self.changed()
    def delete_object(self):
        if not self.current_object():return
        if any(o.get('parent')==self.selected_id for o in self.current_scene()['objects']):
            error(self,'Nhóm còn lớp con. Bỏ lớp cha của các lớp con bằng “Cha / điểm xoay…” trước khi xóa.');return
        self.remember();s=self.current_scene();s['objects']=[o for o in s['objects'] if o['id']!=self.selected_id];self.selected_id='';self.changed()
    def keyframe_dialog(self):
        o=self.current_object()
        if o:self.remember();d=KeyframeDialog(o,self.t-self.current_scene()['start'],self);d.exec();self.changed()
    def rig_dialog(self):
        o=self.current_object()
        if o and o['kind']=='character':self.remember();RigDialog(o,self).exec();self.changed()
    def attachment_dialog(self):
        o=self.current_object()
        if o and o['kind']!='character':self.remember();AttachmentDialog(o,self.current_scene(),self.t-self.current_scene()['start'],self).exec();self.changed()
    def camera_dialog(self):
        s=self.current_scene();local=self.t-s['start'];camera=s['camera']
        camera=next((shot for shot in camera.get('shots',[]) if shot['start']<=local<shot['end']),camera)
        self.remember();KeyframeDialog(camera,local,self,True).exec();self.changed()
    def contact_dialog(self):
        o=self.current_object()
        if o and o['kind']=='character':
            self.remember()
            if ContactDialog(o,self.current_scene(),self).exec():self.changed()
    def shot_dialog(self):
        self.remember()
        if ShotDialog(self.current_scene(),self).exec():self.changed()
    def state_track_dialog(self):
        o=self.current_object()
        if not o or o['kind']!='character':return
        choice,ok=QInputDialog.getItem(self,'Trạng thái theo thời gian','Track',['Biểu cảm','Độ tuổi'],0,False)
        if not ok:return
        field,options,base=('expressions',EXPRESSIONS,'expression') if choice=='Biểu cảm' else ('ages',['child','teen','adult','elderly'],'age')
        self.remember()
        if StateTrackDialog(o,field,options,base,self.current_scene()['duration'],self).exec():self.changed()
    def camera_follow(self,index):
        if not self.loading:self.remember();self.current_scene()['camera']['follow']=self.follow.currentData() or '';self.changed(False)
    def motion_dialog(self):
        o=self.current_object()
        if not o or o['kind']!='character':return
        action,ok=QInputDialog.getItem(self,'Action clip','Chuyển động',LABELS,0,False)
        if not ok:return
        t=max(0,self.t-self.current_scene()['start']);length,ok=QInputDialog.getDouble(self,'Thời lượng action','Giây',min(5,self.current_scene()['duration']-t),.1,self.current_scene()['duration']-t,2)
        if not ok:return
        self.remember();o['motions']=[c for c in o.get('motions',[]) if c['end']<=t or c['start']>=t+length]
        o['motions'].append(dict(start=t,end=t+length,action=ACTIONS[LABELS.index(action)],blend=.35));self.changed()
    def save_motion(self):
        o=self.current_object()
        if not o:return
        path,_=QFileDialog.getSaveFileName(self,'Lưu motion preset',str(self.app_root/'presets'/'motion.json'),'JSON (*.json)')
        if path:Path(path).write_text(json.dumps({k:o[k] for k in ('action','speed','amplitude','motions','keys')},indent=2),encoding='utf-8')
    def load_motion(self):
        o=self.current_object()
        if not o:return
        path,_=QFileDialog.getOpenFileName(self,'Nạp motion preset',str(self.app_root/'presets'),'JSON (*.json)')
        if path:
            try:
                data=json.loads(Path(path).read_text(encoding='utf-8'));self.remember()
                for k in ('action','speed','amplitude','motions','keys'):
                    if k in data:o[k]=data[k]
                self.changed()
            except Exception as exc:error(self,exc)

    def undo(self):self.project=self.history.undo(self.project);self.scene_index=min(self.scene_index,len(self.project['scenes'])-1);self.selected_id='';self.changed()
    def redo(self):self.project=self.history.redo(self.project);self.scene_index=min(self.scene_index,len(self.project['scenes'])-1);self.selected_id='';self.changed()
    def ensure_save(self):
        if not self.dirty:return True
        result=QMessageBox.question(self,'Dự án chưa lưu','Lưu thay đổi trước khi tiếp tục?',QMessageBox.StandardButton.Save|QMessageBox.StandardButton.Discard|QMessageBox.StandardButton.Cancel)
        if result==QMessageBox.StandardButton.Cancel:return False
        if result==QMessageBox.StandardButton.Save:return self.save_project()
        return True
    def create_project(self):
        if not self.ensure_save():return
        dialog=QDialog(self);dialog.setWindowTitle('Dự án mới');v=QVBoxLayout(dialog);f=QFormLayout();v.addLayout(f)
        name=QLineEdit('Câu chuyện mới');f.addRow('Tên dự án',name);length=spin(15,1,86400,15);f.addRow('Thời lượng cảnh đầu (s)',length)
        ratio=QComboBox();ratio.addItems(['16:9','9:16','1:1']);f.addRow('Tỷ lệ',ratio)
        buttons=QDialogButtonBox(QDialogButtonBox.StandardButton.Ok|QDialogButtonBox.StandardButton.Cancel);buttons.accepted.connect(dialog.accept);buttons.rejected.connect(dialog.reject);v.addWidget(buttons)
        if dialog.exec()!=QDialog.DialogCode.Accepted:return
        self.stop();w,h=[(1280,720),(720,1280),(720,720)][ratio.currentIndex()]
        self.project=new_project(name.text(),length.value(),w,h)
        self.project['scenes'][0].update(background='white',objects=[]);self.project['fps']=30
        self.path=None;self.root=self.app_root/'projects'/uid();self.root.mkdir(parents=True,exist_ok=True)
        self.history=History();self.selected_id='';self.scene_index=0;self.t=0;self.changed()
    def open_project(self):
        if not self.ensure_save():return
        path,_=QFileDialog.getOpenFileName(self,'Mở project','','Project (*.json)')
        if path:self.open_path(path)
    def open_path(self,path):
        try:
            p=load(path)
            self.stop();self.project=p;self.path=Path(path);self.root=self.path.parent;self.history=History();self.scene_index=0;self.selected_id='';self.t=0;self.dirty=False;self.renderer.cache.clear();self.refresh()
            self.setWindowTitle(self.project['name']+' · STICKMAN ANIMATION STUDIO')
            absent=missing(p,self.root)
            if absent:error(self,'Thiếu tài nguyên. Có thể relink trong Cài đặt:\n'+'\n'.join(absent))
        except Exception as exc:error(self,exc)
    def save_project(self,save_as=False):
        path=self.path
        if save_as or not path:
            value,_=QFileDialog.getSaveFileName(self,'Lưu project',str(self.root/'project.json'),'Project (*.json)')
            if not value:return False
            path=Path(value)
        try:
            self.project=save(self.project,path,self.root);self.path=path;self.root=path.parent;self.dirty=False
            self.setWindowTitle(self.project['name']+' · STICKMAN ANIMATION STUDIO');self.statusBar().showMessage('Đã lưu '+str(path));return True
        except Exception as exc:error(self,exc);return False
    def autosave(self):
        if not self.dirty:return
        try:save(self.project,self.root/'project.autosave.json',self.root);self.statusBar().showMessage('Autosave · '+stamp(self.t))
        except Exception as exc:self.statusBar().showMessage('Autosave thất bại: '+str(exc))
    def import_srt(self):
        path,_=QFileDialog.getOpenFileName(self,'Nhập SRT · giữ nguyên timestamp','','SRT (*.srt)')
        if path:
            try:self.remember();self.project['subtitles']=read(path);self.changed();self.statusBar().showMessage('Đã nhập SRT. Timestamp giữ nguyên; có thể kéo dài cảnh nếu phụ đề vượt project.')
            except Exception as exc:error(self,exc)
    def import_image(self,kind):
        path,_=QFileDialog.getOpenFileName(self,'Nhập ảnh','','Ảnh (*.png *.jpg *.jpeg *.webp *.svg)')
        if not path:return
        try:
            self.remember();folder=self.root/'assets';folder.mkdir(exist_ok=True);dest=folder/(uid()+'_'+Path(path).name);shutil.copy2(path,dest);rel=dest.relative_to(self.root).as_posix()
            if kind=='background':self.current_scene()['background_file']=rel
            elif kind=='reference':self.project['references'].append(dict(id=uid(),name=Path(path).name,file=rel))
            else:
                from ..explainer import image_item
                o=image_item(rel,640,360,600,400);o['name']=Path(path).stem;o['end']=self.current_scene()['duration'];o['layer']=25
                o['role']='photo' if kind=='photo' else 'character' if kind=='character_image' else 'object'
                self.current_scene()['objects'].append(o);self.selected_id=o['id']
            self.changed()
        except Exception as exc:error(self,exc)
    def subtitle_dialog(self):self.remember();self.pause();SubtitleDialog(self.project,self).exec();self.changed()
    def audio_dialog(self):self.remember();self.pause();AudioDialog(self.project,self.root,self).exec();self.audio_preview.stop();self.changed()
    def voice_dialog(self):self.remember();self.pause();VoiceDialog(self.project,self.root,self.app_root/'voices',self.t,self).exec();self.audio_preview.stop();self.changed()
    def pause(self):
        if self.playing:self.toggle_play()
    def export_package(self):
        if not self.save_project():return
        path,_=QFileDialog.getSaveFileName(self,'Xuất project và assets','','Project ZIP (*.zip)')
        if path:
            try:pack(self.project,self.root,path);self.statusBar().showMessage('Đã đóng gói '+path)
            except Exception as exc:error(self,exc)
    def import_package(self):
        if not self.ensure_save():return
        path,_=QFileDialog.getOpenFileName(self,'Nhập gói project','','ZIP (*.zip)')
        if not path:return
        folder=QFileDialog.getExistingDirectory(self,'Chọn thư mục trống để giải nén')
        if folder:
            try:self.open_path(unpack(path,folder))
            except Exception as exc:error(self,exc)
    def settings(self):
        dialog=QDialog(self);dialog.setWindowTitle('Cài đặt / Chẩn đoán');layout=QVBoxLayout(dialog)
        for name in ('ffmpeg','ffprobe'):
            try:message=f'{name}: '+binary(name)
            except Exception as exc:message=str(exc)
            label=QLabel(message);label.setWordWrap(True);layout.addWidget(label)
        layout.addWidget(QLabel('Preview dừng render khi tạm dừng. Export dùng CPU, tối đa 2 thread FFmpeg.\nModel tiếng Việt: '+str(self.app_root/'voices')))
        button('Khôi phục autosave của project',lambda:self.recover(dialog),layout)
        button('Relink tài nguyên thiếu…',self.relink,layout)
        button('Mở demo 180 giây',lambda:self.load_demo(dialog),layout)
        button('Đóng',dialog.accept,layout);dialog.exec()
    def recover(self,dialog):
        path=self.root/'project.autosave.json'
        if not path.exists():error(dialog,'Chưa có autosave cho project này.');return
        if self.ensure_save():dialog.accept();self.open_path(path);self.path=self.root/'project.json';self.dirty=True
    def relink(self):
        from ..project import media_entries
        self.remember()
        for o,k in media_entries(self.project):
            if not resolve(self.root,o[k]).is_file():
                path,_=QFileDialog.getOpenFileName(self,'Tìm lại: '+o[k])
                if path:o[k]=path
        self.renderer.cache.clear();self.changed()
    def load_demo(self,dialog):
        if not self.ensure_save():return
        dialog.accept();path=self.app_root/'examples'/'yellow_umbrella_v2'/'project.json'
        if path.exists():self.open_path(path)
        else:self.project=demo();self.scene_index=0;self.t=0;self.selected_id='';self.changed()
    def export_dialog(self):
        if self.export_worker and self.export_worker.isRunning():error(self,'Đang xuất video.');return
        self.pause();dialog=QDialog(self);dialog.setWindowTitle('Xuất MP4 · CPU H.264');layout=QVBoxLayout(dialog);form=QFormLayout();layout.addLayout(form)
        res=QComboBox();res.addItems(['480p · 854×480','720p · 1280×720','1080p · 1920×1080','4K · 3840×2160']);res.setCurrentIndex(2);form.addRow('Độ phân giải',res)
        profile=QComboBox();profile.addItem('Nháp · nhanh','draft');profile.addItem('Cân bằng','balanced');profile.addItem('Bàn giao · nét cao','final');profile.setCurrentIndex(max(0,profile.findData(self.project.get('render_profile','final'))));form.addRow('Chất lượng encode',profile)
        smooth=QCheckBox('Làm mượt nét 2× · render chậm hơn');smooth.setChecked(self.project.get('supersample',1)==2);form.addRow(smooth)
        fps=QComboBox();fps.addItems(['12','24','30']);fps.setCurrentText(str(self.project['fps']));form.addRow('FPS',fps)
        scope=QComboBox();scope.addItems(['Toàn bộ project','Cảnh đang chọn']);form.addRow('Phạm vi',scope)
        burn=QCheckBox('Burn phụ đề vào video');burn.setChecked(True);form.addRow(burn)
        separate=QCheckBox('Xuất SRT riêng cạnh video');separate.setChecked(True);form.addRow(separate)
        cached=QCheckBox('Lưu từng cảnh để thử lại / tiếp tục export toàn project');form.addRow(cached)
        actions=QDialogButtonBox(QDialogButtonBox.StandardButton.Ok|QDialogButtonBox.StandardButton.Cancel)
        actions.accepted.connect(dialog.accept);actions.rejected.connect(dialog.reject);layout.addWidget(actions)
        if dialog.exec()!=QDialog.DialogCode.Accepted:return
        path,_=QFileDialog.getSaveFileName(self,'Lưu MP4','','MP4 (*.mp4)')
        if not path:return
        base=[854,1280,1920,3840][res.currentIndex()];height=round(base*self.project['height']/self.project['width']);height+=height%2
        if self.project['width']<self.project['height']:
            height=[854,1280,1920,3840][res.currentIndex()];height+=height%2;base=round(height*self.project['width']/self.project['height']);base+=base%2
        start=self.current_scene()['start'] if scope.currentIndex() else 0;length=self.current_scene()['duration'] if scope.currentIndex() else duration(self.project)
        self.remember();self.project['render_profile']=profile.currentData();self.project['supersample']=2 if smooth.isChecked() else 1;self.dirty=True
        self.start_export(path,base,height,int(fps.currentText()),start,length,burn.isChecked(),separate.isChecked(),cached.isChecked() and scope.currentIndex()==0)
    def start_export(self,path,w,h,fps,start,length,burn,separate,cached=False):
        project=copy.deepcopy(self.project);root=self.root
        self.export_progress=QProgressDialog('Đang render frame…','Hủy',0,100,self);self.export_progress.setWindowTitle('Xuất video');self.export_progress.setMinimumDuration(0);self.export_progress.setAutoClose(False)
        self.export_progress.setWindowModality(Qt.WindowModality.NonModal);self.export_progress.show()
        def work(worker):
            if cached:output=export_cached(project,root,path,w,h,fps,burn,lambda a,b:worker.progress.emit(a,b),worker.cancel)
            else:output=export_video(project,root,path,w,h,fps,start,length,burn,lambda a,b:worker.progress.emit(a,b),worker.cancel)
            if separate:
                cues=[]
                for c in project['subtitles']:
                    if c['start']<start+length and c['end']>start:
                        c=copy.deepcopy(c);c['start']=max(0,c['start']-start);c['end']=min(length,c['end']-start);cues.append(c)
                write(cues,Path(path).with_suffix('.srt'))
            return output
        self.export_worker=Worker(work,self)
        self.export_worker.progress.connect(self.export_update)
        self.export_progress.canceled.connect(self.export_worker.cancel.set)
        self.export_worker.done.connect(self.export_done);self.export_worker.failed.connect(self.export_failed);self.export_worker.start()
    def export_update(self,a,b):
        self.export_progress.setValue(min(99,round(a*100/b)))
        self.export_progress.setLabelText(f'Frame {a:,} / {b:,}' if a<b else 'Đang mix audio và đóng gói MP4…')
    def export_done(self,path):
        self.export_progress.close();self.statusBar().showMessage('Xuất thành công: '+str(path));QMessageBox.information(self,'Xuất thành công','MP4 đã lưu:\n'+str(path))
    def export_failed(self,message):
        self.export_progress.close();error(self,message)
    def closeEvent(self,event):
        if self.project_worker and self.project_worker.isRunning():
            self.project_worker.cancel.set();self.statusBar().showMessage('Đang dừng tác vụ. Đóng lại khi tác vụ kết thúc.');event.ignore();return
        if self.export_worker and self.export_worker.isRunning():
            self.export_worker.cancel.set();error(self,'Đang hủy export. Đợi worker dừng rồi đóng Studio.');event.ignore();return
        if not self.ensure_save():event.ignore();return
        self.audio_preview.stop();self.timer.stop();self.autosave();event.accept()
