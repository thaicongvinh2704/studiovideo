import copy
import json
import shutil
import subprocess
from pathlib import Path
from PySide6.QtCore import Qt,QUrl
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (QDialog,QVBoxLayout,QHBoxLayout,QFormLayout,QPushButton,QLabel,
    QComboBox,QDoubleSpinBox,QSpinBox,QTextEdit,QTableWidget,QTableWidgetItem,QHeaderView,
    QFileDialog,QMessageBox,QDialogButtonBox,QCheckBox,QLineEdit,QProgressBar,QColorDialog)
from PySide6.QtMultimedia import QMediaPlayer,QAudioOutput
from ..animation import ACTIONS,LABELS,EXPRESSIONS,dimensions
from ..project import uid,resolve
from ..subtitles import stamp,seconds,write
from ..tts import VoiceEngine
from ..exporter import binary
from .workers import Worker

def spin(value=0,minimum=-10000,maximum=10000,step=1,decimals=2):
    w=QDoubleSpinBox();w.setRange(minimum,maximum);w.setDecimals(decimals);w.setSingleStep(step);w.setValue(value)
    return w

def button(text,fn,layout,primary=False):
    b=QPushButton(text);b.clicked.connect(fn)
    if primary: b.setObjectName('primary')
    layout.addWidget(b);return b

def error(parent,exc):
    QMessageBox.warning(parent,'Không thể thực hiện',str(exc))

class SubtitleDialog(QDialog):
    def __init__(self,project,parent=None):
        super().__init__(parent);self.setWindowTitle('SRT Editor · Timestamp giữ theo file gốc');self.resize(970,580)
        self.project=project;layout=QVBoxLayout(self)
        self.table=QTableWidget(0,4);self.table.setHorizontalHeaderLabels(['Bắt đầu','Kết thúc','Nội dung','Vai đọc'])
        self.table.horizontalHeader().setSectionResizeMode(2,QHeaderView.ResizeMode.Stretch)
        self.table.setColumnWidth(0,145);self.table.setColumnWidth(1,145);layout.addWidget(self.table)
        for c in project['subtitles']: self.add(c)
        row=QHBoxLayout();layout.addLayout(row)
        button('Thêm cue',lambda:self.add(dict(start=0,end=5,text='Lời thoại mới',role='Narrator')),row)
        button('Xóa cue',self.remove,row);button('Xuất SRT…',self.export,row)
        form=QFormLayout();layout.addLayout(form);style=project['subtitle_style']
        self.enabled=QCheckBox('Hiện phụ đề trong preview');self.enabled.setChecked(style['enabled']);form.addRow(self.enabled)
        self.font=QLineEdit(style['font']);form.addRow('Font',self.font)
        self.size=spin(style['size'],10,80,1,0);form.addRow('Cỡ chữ',self.size)
        self.y=spin(style['y'],0,1,.02);form.addRow('Vị trí Y (0–1)',self.y)
        self.bg=QCheckBox('Nền tối dưới chữ');self.bg.setChecked(style['background']);form.addRow(self.bg)
        self.color=QLineEdit(style['color']);form.addRow('Màu chữ (#hex)',self.color)
        actions=QDialogButtonBox(QDialogButtonBox.StandardButton.Save|QDialogButtonBox.StandardButton.Cancel)
        actions.accepted.connect(self.commit);actions.rejected.connect(self.reject);layout.addWidget(actions)
    def add(self,c):
        r=self.table.rowCount();self.table.insertRow(r)
        for j,text in enumerate([stamp(c['start']),stamp(c['end']),c['text'],c.get('role','Narrator')]):
            item=QTableWidgetItem(text)
            if j==0: item.setData(Qt.ItemDataRole.UserRole,c.get('id',uid()))
            self.table.setItem(r,j,item)
    def remove(self):
        for r in sorted({i.row() for i in self.table.selectedIndexes()},reverse=True): self.table.removeRow(r)
    def cues(self):
        result=[]
        for r in range(self.table.rowCount()):
            a,b=[seconds(self.table.item(r,j).text()) for j in (0,1)]
            if b<=a: raise ValueError(f'Cue {r+1}: kết thúc phải lớn hơn bắt đầu.')
            result.append(dict(id=self.table.item(r,0).data(Qt.ItemDataRole.UserRole),start=a,end=b,
                text=self.table.item(r,2).text(),role=self.table.item(r,3).text()))
        return sorted(result,key=lambda c:c['start'])
    def export(self):
        path,_=QFileDialog.getSaveFileName(self,'Xuất phụ đề','','SRT (*.srt)')
        if path:
            try: write(self.cues(),path)
            except Exception as exc:error(self,exc)
    def commit(self):
        try:
            cues=self.cues()
            if not QColor(self.color.text()).isValid(): raise ValueError('Màu chữ không hợp lệ.')
            self.project['subtitles']=cues
            self.project['subtitle_style']=dict(enabled=self.enabled.isChecked(),font=self.font.text(),
                size=int(self.size.value()),y=self.y.value(),background=self.bg.isChecked(),color=self.color.text())
            self.accept()
        except Exception as exc:error(self,exc)

class KeyframeDialog(QDialog):
    def __init__(self,obj,time,parent=None,camera=False):
        super().__init__(parent);self.obj=obj;self.camera=camera
        self.setWindowTitle('Keyframe Editor · Giá trị tại thời gian cục bộ của cảnh');self.resize(760,500)
        layout=QVBoxLayout(self)
        layout.addWidget(QLabel('Nội suy đặt ở keyframe đích. Bezier dùng đường cong (0.25, 0.1, 0.25, 1).'))
        self.table=QTableWidget(0,5);self.table.setHorizontalHeaderLabels(['Thuộc tính','Giây trong cảnh','Giá trị','Nội suy','Bezier x1,y1,x2,y2'])
        self.original_keys=copy.deepcopy(obj.get('keys',{}))
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch);layout.addWidget(self.table)
        self.properties=['x','y','zoom'] if camera else ['x','y','scale','rotation','opacity',
            'bone_torso','bone_arm_l','bone_fore_l','bone_arm_r','bone_fore_r',
            'bone_thigh_l','bone_shin_l','bone_thigh_r','bone_shin_r','bone_lift','bone_head',
            'hand_l_x','hand_l_y','hand_r_x','hand_r_y','gaze','facing']
        for prop,keys in obj.get('keys',{}).items():
            for k in keys:self.add(prop,k['t'],k['v'],k.get('ease','linear'),k.get('bezier'))
        row=QHBoxLayout();layout.addLayout(row)
        button('Thêm tại playhead',lambda:self.add('x',time,obj.get('x',640),'ease_in_out'),row)
        button('Xóa keyframe',self.remove,row)
        actions=QDialogButtonBox(QDialogButtonBox.StandardButton.Save|QDialogButtonBox.StandardButton.Cancel)
        actions.accepted.connect(self.commit);actions.rejected.connect(self.reject);layout.addWidget(actions)
    def add(self,prop,time,value,ease,bezier=None):
        r=self.table.rowCount();self.table.insertRow(r)
        p=QComboBox();p.addItems(self.properties);p.setCurrentText(prop);self.table.setCellWidget(r,0,p)
        self.table.setCellWidget(r,1,spin(time,0,86400,.1,3));self.table.setCellWidget(r,2,spin(value,-100000,100000,.1,3))
        e=QComboBox();e.addItems(['linear','ease_in','ease_out','ease_in_out','bezier','hold']);e.setCurrentText(ease);self.table.setCellWidget(r,3,e)
        control=QLineEdit(','.join(str(v) for v in (bezier or [.25,.1,.25,1])));self.table.setCellWidget(r,4,control)
    def remove(self):
        rows={i.row() for i in self.table.selectedIndexes()}
        if not rows and self.table.currentRow()>=0:rows={self.table.currentRow()}
        for r in sorted(rows,reverse=True):self.table.removeRow(r)
    def commit(self):
        keys={}
        for r in range(self.table.rowCount()):
            prop=self.table.cellWidget(r,0).currentText();t=self.table.cellWidget(r,1).value();v=self.table.cellWidget(r,2).value()
            if prop in ('scale','zoom') and v<=0:error(self,'Scale/Zoom phải lớn hơn 0.');return
            if any(k['t']==t for k in keys.get(prop,[])):error(self,'Hai keyframe cùng thuộc tính không được trùng thời gian.');return
            import math
            try:
                bezier=[float(x.strip()) for x in self.table.cellWidget(r,4).text().split(',')]
                if len(bezier)!=4 or not all(math.isfinite(x) for x in bezier) or not all(0<=bezier[i]<=1 for i in (0,2)):raise ValueError()
            except ValueError:error(self,'Bezier cần 4 số hữu hạn, X1/X2 nằm trong 0–1.');return
            frame=copy.deepcopy(next((k for k in self.original_keys.get(prop,[]) if abs(k['t']-t)<.0001),{}))
            frame.update(t=t,v=v,ease=self.table.cellWidget(r,3).currentText(),bezier=bezier)
            keys.setdefault(prop,[]).append(frame)
        self.obj['keys']=keys;self.accept()

class RigDialog(QDialog):
    def __init__(self,obj,parent=None):
        super().__init__(parent);self.obj=obj;self.setWindowTitle('Rig · Tỷ lệ xương và IK bàn tay');layout=QVBoxLayout(self)
        layout.addWidget(QLabel('Ảnh phẳng dùng làm tham chiếu. Chỉnh rig của nhân vật vector tại đây.'))
        form=QFormLayout();layout.addLayout(form);self.fields={}
        defaults=dict(zip(('torso','upper_arm','forearm','thigh','shin','shoulder'),dimensions(obj)))
        for key,value in defaults.items():
            w=spin(obj.get('rig',{}).get(key,value),10,200);form.addRow(key,w);self.fields[key]=w
        self.hands={}
        for side in ('l','r'):
            current=obj.get('rig',{}).get('hand_'+side)
            check=QCheckBox('Ghim bàn tay '+side+' bằng IK');check.setChecked(current is not None);form.addRow(check)
            x=spin(current[0] if current else 50,-250,250);y=spin(current[1] if current else -150,-350,100)
            form.addRow('Tay '+side+' · X',x);form.addRow('Tay '+side+' · Y',y);self.hands[side]=(check,x,y)
        row=QDialogButtonBox(QDialogButtonBox.StandardButton.Save|QDialogButtonBox.StandardButton.Cancel)
        row.accepted.connect(self.commit);row.rejected.connect(self.reject);layout.addWidget(row)
    def commit(self):
        self.obj['rig']={k:w.value() for k,w in self.fields.items()}
        for side,(check,x,y) in self.hands.items():
            if check.isChecked():self.obj['rig']['hand_'+side]=[x.value(),y.value()]
        self.accept()

class AttachmentDialog(QDialog):
    def __init__(self,obj,scene,time,parent=None):
        super().__init__(parent);self.obj=obj;self.scene=scene;self.time=time
        self.setWindowTitle('Đạo cụ · Gắn vào tay / chuyển người cầm');layout=QVBoxLayout(self)
        layout.addWidget(QLabel('Mỗi mốc thay người cầm được lưu trên timeline cảnh. Chọn tự do để thả đạo cụ.'))
        self.table=QTableWidget(0,3);self.table.setHorizontalHeaderLabels(['Giây','Người cầm','Khớp'])
        layout.addWidget(self.table)
        for k in obj.get('attachment',[]):self.add(k)
        row=QHBoxLayout();layout.addLayout(row)
        button('Thêm mốc',lambda:self.add(dict(t=time,character='',joint='hand_r')),row)
        button('Xóa mốc',lambda:self.table.removeRow(self.table.currentRow()),row)
        actions=QDialogButtonBox(QDialogButtonBox.StandardButton.Save|QDialogButtonBox.StandardButton.Cancel)
        actions.accepted.connect(self.commit);actions.rejected.connect(self.reject);layout.addWidget(actions)
    def add(self,k):
        r=self.table.rowCount();self.table.insertRow(r);self.table.setCellWidget(r,0,spin(k['t'],0,self.scene['duration'],.1))
        c=QComboBox();c.addItem('Tự do','')
        for o in self.scene['objects']:
            if o['kind']=='character':c.addItem(o['name'],o['id'])
        c.setCurrentIndex(max(0,c.findData(k['character'])));self.table.setCellWidget(r,1,c)
        j=QComboBox();j.addItems(['hand_r','hand_l','head','hip']);j.setCurrentText(k.get('joint','hand_r'));self.table.setCellWidget(r,2,j)
    def commit(self):
        self.obj['attachment']=sorted([dict(t=self.table.cellWidget(r,0).value(),character=self.table.cellWidget(r,1).currentData(),
                  joint=self.table.cellWidget(r,2).currentText()) for r in range(self.table.rowCount())],key=lambda k:k['t'])
        self.accept()

class AudioDialog(QDialog):
    def __init__(self,project,root,parent=None):
        super().__init__(parent);self.project=project;self.root=root;self.setWindowTitle('Audio Mixer · Giọng / Nhạc / SFX');self.resize(1060,470)
        layout=QVBoxLayout(self);self.table=QTableWidget(0,9)
        self.table.setHorizontalHeaderLabels(['Tên','Nhóm','Start (s)','Độ dài','Trim nguồn','Volume','Fade in','Fade out','Mute'])
        self.table.horizontalHeader().setSectionResizeMode(0,QHeaderView.ResizeMode.Stretch)
        for j in range(1,9):self.table.setColumnWidth(j,90)
        layout.addWidget(self.table)
        self.clips=copy.deepcopy(project['audio'])
        for a in self.clips:self.add(a)
        self.audio_output=QAudioOutput(self);self.player=QMediaPlayer(self);self.player.setAudioOutput(self.audio_output)
        row=QHBoxLayout();layout.addLayout(row)
        button('Nhập MP3/WAV…',self.import_audio,row);button('Nghe clip chọn',self.play,row);button('Dừng',self.player.stop,row)
        button('Xóa clip',self.remove,row)
        self.duck=QCheckBox('Giảm nhạc khi có lời đọc');self.duck.setChecked(project.get('duck_music',True));layout.addWidget(self.duck)
        actions=QDialogButtonBox(QDialogButtonBox.StandardButton.Save|QDialogButtonBox.StandardButton.Cancel)
        actions.accepted.connect(self.commit);actions.rejected.connect(self.reject);layout.addWidget(actions)
    def add(self,a):
        r=self.table.rowCount();self.table.insertRow(r);self.table.setItem(r,0,QTableWidgetItem(a.get('name',Path(a['file']).stem)))
        group=QComboBox();group.addItem('Giọng','voice');group.addItem('Nhạc','music');group.addItem('SFX','sfx')
        group.setCurrentIndex(max(0,group.findData(a['group'])));self.table.setCellWidget(r,1,group)
        for j,key in enumerate(['start','duration','trim','volume','fade_in','fade_out'],2):
            self.table.setCellWidget(r,j,spin(a.get(key,0),0,4 if key=='volume' else 86400,.1))
        check=QCheckBox();check.setChecked(a.get('mute',False));self.table.setCellWidget(r,8,check)
    def import_audio(self):
        path,_=QFileDialog.getOpenFileName(self,'Nhập audio','','Audio (*.mp3 *.wav *.ogg *.flac)')
        if not path:return
        try:
            info=json.loads(subprocess.check_output([binary('ffprobe'),'-v','quiet','-show_format','-of','json',path],creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0)))
            folder=Path(self.root)/'assets';folder.mkdir(exist_ok=True);dest=folder/(uid()+'_'+Path(path).name);shutil.copy2(path,dest)
            a=dict(id=uid(),file=dest.relative_to(self.root).as_posix(),name=Path(path).stem,group='music',start=0,
                   duration=float(info['format']['duration']),trim=0,volume=.5,fade_in=0,fade_out=0,mute=False)
            self.clips.append(a);self.add(a)
        except Exception as exc:error(self,exc)
    def remove(self):
        r=self.table.currentRow()
        if r>=0:self.table.removeRow(r);self.clips.pop(r)
    def play(self):
        r=self.table.currentRow()
        if r>=0:self.player.setSource(QUrl.fromLocalFile(str(resolve(self.root,self.clips[r]['file']))));self.player.play()
    def commit(self):
        for r,a in enumerate(self.clips):
            a['name']=self.table.item(r,0).text();a['group']=self.table.cellWidget(r,1).currentData()
            for j,key in enumerate(['start','duration','trim','volume','fade_in','fade_out'],2):a[key]=self.table.cellWidget(r,j).value()
            if a['duration']<=0:error(self,'Thời lượng audio phải lớn hơn 0.');return
            a['mute']=self.table.cellWidget(r,8).isChecked()
        self.project['audio']=self.clips;self.project['duck_music']=self.duck.isChecked();self.player.stop();self.accept()
    def closeEvent(self,event):self.player.stop();super().closeEvent(event)
    def reject(self):self.player.stop();super().reject()

class VoiceDialog(QDialog):
    def __init__(self,project,root,voices,time,parent=None):
        super().__init__(parent);self.project=project;self.root=Path(root);self.time=time;self.engine=VoiceEngine(voices);self.worker=None;self.last=None
        self.setWindowTitle('Voice Studio · Tiếng Việt offline · Không credit');self.resize(720,600)
        layout=QVBoxLayout(self);form=QFormLayout();layout.addLayout(form)
        self.voice=QComboBox()
        for label,path in self.engine.voices():self.voice.addItem(label,path)
        form.addRow('Voice / Language',self.voice)
        self.role=QComboBox();self.role.addItems(['Narrator','Father','Mother','Son']);form.addRow('Vai (có thể dùng chung một voice)',self.role)
        self.speed=spin(1,.65,1.6,.05);form.addRow('Tốc độ',self.speed)
        self.volume=spin(1,0,2,.1);form.addRow('Âm lượng',self.volume)
        self.cue=QComboBox();self.cue.addItem('Văn bản tự nhập',None)
        for c in project['subtitles']:self.cue.addItem(f"{stamp(c['start'])} · {c['text'][:65]}",c)
        self.cue.currentIndexChanged.connect(self.cue_changed);form.addRow('Đoạn SRT',self.cue)
        self.text=QTextEdit();self.text.setPlaceholderText('Nhập tiếng Việt có dấu…');layout.addWidget(self.text)
        self.info=QLabel('Chỉ liệt kê voice đã có model + config. Vai đọc không tạo ra voice mới.');self.info.setWordWrap(True);layout.addWidget(self.info)
        self.progress=QProgressBar();layout.addWidget(self.progress)
        self.audio_output=QAudioOutput(self);self.player=QMediaPlayer(self);self.player.setAudioOutput(self.audio_output)
        row=QHBoxLayout();layout.addLayout(row)
        self.generate_button=button('Tạo WAV',lambda:self.generate(False),row,True)
        self.all_button=button('Tạo tất cả cue SRT',lambda:self.generate(True),row)
        button('Hủy',self.cancel,row)
        row=QHBoxLayout();layout.addLayout(row)
        self.preview_button=button('Nghe WAV',self.preview,row);self.preview_button.setEnabled(False)
        self.save_button=button('Lưu WAV ra ngoài…',self.save_wav,row);self.save_button.setEnabled(False)
        self.apply_button=button('Áp dụng vào timeline',self.apply,row);self.apply_button.setEnabled(False)
        button('Đóng',self.accept,row)
    def cue_changed(self):
        c=self.cue.currentData()
        if c:self.text.setPlainText(c['text']);self.role.setCurrentText(c.get('role','Narrator'))
    def cancel(self):
        if self.worker and self.worker.isRunning():self.worker.cancel.set();self.info.setText('Đang hủy sau đoạn hiện tại…')
    def generate(self,all_cues):
        if self.worker and self.worker.isRunning():return
        cues=copy.deepcopy(self.project['subtitles']) if all_cues else [copy.deepcopy(self.cue.currentData()) or dict(start=self.time,end=self.time+5,text=self.text.toPlainText())]
        if not all_cues:cues[0]['text']=self.text.toPlainText()
        if not cues or any(not c['text'].strip() for c in cues):error(self,'Chưa có nội dung để đọc.');return
        voice=self.voice.currentData();speed=self.speed.value();volume=self.volume.value();role=self.role.currentText()
        folder=self.root/'assets'/'voice';folder.mkdir(parents=True,exist_ok=True)
        self.generate_button.setEnabled(False);self.all_button.setEnabled(False);self.apply_button.setEnabled(False)
        self.info.setText('Đang tạo giọng bằng CPU…')
        def work(w):
            result=[]
            for i,c in enumerate(cues):
                if w.cancel.is_set():break
                path=folder/(uid()+'.wav');length=self.engine.synthesize(c['text'],voice,path,speed,volume)
                result.append(dict(path=path,duration=length,cue=c,role=role));w.progress.emit(i+1,len(cues))
            return result
        self.worker=Worker(work,self);self.worker.progress.connect(lambda a,b:self.progress.setValue(round(a*100/b)))
        self.worker.done.connect(lambda result:self.generated(result,all_cues));self.worker.failed.connect(self.failed);self.worker.start()
    def generated(self,result,all_cues):
        self.generate_button.setEnabled(True);self.all_button.setEnabled(True)
        if not result:self.info.setText('Đã hủy, chưa tạo WAV.');return
        self.last=result[-1];self.preview_button.setEnabled(True);self.save_button.setEnabled(True);self.apply_button.setEnabled(True)
        warnings=[r for r in result if r['duration']>r['cue']['end']-r['cue']['start']+.05]
        self.info.setText(f'Đã tạo {len(result)} WAV. '+(f'{len(warnings)} đoạn dài hơn cue: tăng tốc đọc / chỉnh thời lượng; giữ nguyên lời, không cắt từ.' if warnings else 'Lời đọc vừa thời lượng cue.'))
        if all_cues:
            for r in result:self.insert(r)
            self.info.setText(self.info.text()+' Đã áp dụng các WAV vào timeline.')
    def failed(self,message):
        self.generate_button.setEnabled(True);self.all_button.setEnabled(True);self.info.setText('Tạo voice thất bại: '+message);error(self,message)
    def insert(self,r):
        cue=r['cue']
        # Re-generating a cue replaces its voice clip, avoiding doubled narration.
        if cue.get('id'):self.project['audio']=[a for a in self.project['audio'] if a.get('cue_id')!=cue['id']]
        self.project['audio'].append(dict(id=uid(),cue_id=cue.get('id'),file=r['path'].relative_to(self.root).as_posix(),
            name=r['role']+' · '+cue['text'][:30],group='voice',start=cue['start'],duration=r['duration'],
            volume=1.,trim=0.,fade_in=0.,fade_out=0.,mute=False))
    def apply(self):
        if self.last:self.insert(self.last);self.info.setText('Đã áp dụng WAV tại timestamp của cue / playhead.')
    def preview(self):
        if self.last:self.player.setSource(QUrl.fromLocalFile(str(self.last['path'])));self.player.play()
    def save_wav(self):
        path,_=QFileDialog.getSaveFileName(self,'Lưu giọng đọc','','WAV (*.wav)')
        if path and self.last:shutil.copy2(self.last['path'],path)
    def reject(self):
        if self.worker and self.worker.isRunning():self.cancel();self.info.setText('Đợi tác vụ hiện tại dừng rồi đóng Voice Studio.');return
        self.player.stop();super().reject()
    def accept(self):
        if self.worker and self.worker.isRunning():self.cancel();self.info.setText('Đợi tác vụ hiện tại dừng rồi đóng Voice Studio.');return
        self.player.stop();super().accept()
