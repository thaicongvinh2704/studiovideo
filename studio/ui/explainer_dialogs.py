import copy
import json
from pathlib import Path
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QDialog,QVBoxLayout,QHBoxLayout,QFormLayout,QLabel,QLineEdit,
    QPlainTextEdit,QPushButton,QComboBox,QTableWidget,QTableWidgetItem,QHeaderView,
    QFileDialog,QDialogButtonBox,QCheckBox,QMessageBox,QTabWidget,QWidget)
from ..explainer import LAYOUTS,POSES,suggest_board,compile_board,load_board
from .dialogs import spin,error

class StoryboardDialog(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent);self.setWindowTitle('Kịch bản + voice → Video minh họa');self.resize(1180,680)
        self.board=None;self.result_project=None;self.worker=None
        v=QVBoxLayout(self);self.tabs=QTabWidget();v.addWidget(self.tabs)
        source=QWidget();sv=QVBoxLayout(source);self.tabs.addTab(source,'1 · Kịch bản và tài nguyên')
        form=QFormLayout();sv.addLayout(form);self.name=QLineEdit('Video minh họa');form.addRow('Tên dự án',self.name)
        self.voice=QLineEdit();row=QHBoxLayout();row.addWidget(self.voice);b=QPushButton('Chọn voice…');b.clicked.connect(self.choose_voice);row.addWidget(b);form.addRow('Voice có sẵn',row)
        self.folder=QLineEdit();row=QHBoxLayout();row.addWidget(self.folder);b=QPushButton('Chọn thư mục hình…');b.clicked.connect(self.choose_folder);row.addWidget(b);form.addRow('Ảnh / SVG',row)
        self.script=QPlainTextEdit();self.script.setPlaceholderText('Dán kịch bản hoặc SRT. Mỗi đoạn là một cảnh. SRT giữ thời gian chính xác; văn bản được chia theo độ dài voice và cần căn lại.');sv.addWidget(self.script)
        self.pause_assist=QCheckBox('TXT: gợi ý mốc gần khoảng nghỉ của voice (không phải nhận dạng lời)');self.pause_assist.setChecked(True);sv.addWidget(self.pause_assist)
        row=QHBoxLayout();sv.addLayout(row)
        for title,fn in [('Mở TXT / SRT…',self.choose_script),('Mở storyboard JSON…',self.import_board),('Tạo bảng phân cảnh',self.suggest)]:
            b=QPushButton(title);b.clicked.connect(fn);row.addWidget(b)
        edit=QWidget();ev=QVBoxLayout(edit);self.tabs.addTab(edit,'2 · Căn thời gian và bố trí')
        self.notice=QLabel('Chọn voice và nhập kịch bản trước.');self.notice.setWordWrap(True);ev.addWidget(self.notice)
        self.table=QTableWidget(0,8);self.table.setHorizontalHeaderLabels(['Bắt đầu (s)','Kết thúc (s)','Tiêu đề','Bố cục','Tư thế','Ảnh (mỗi dòng một file)','Nhãn (ngăn bằng |)','Lời đọc'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        for i,w in enumerate((88,88,200,175,130,220,200,300)):self.table.setColumnWidth(i,w)
        ev.addWidget(self.table)
        row=QHBoxLayout();ev.addLayout(row)
        for title,fn in [('Chọn ảnh cho cảnh',self.row_assets),('Thêm cảnh',self.add_row),('Xóa cảnh',self.remove_row),('Lưu storyboard…',self.save_board)]:
            b=QPushButton(title);b.clicked.connect(fn);row.addWidget(b)
        self.subtitles=QCheckBox('Hiện phụ đề trong video');ev.addWidget(self.subtitles)
        buttons=QDialogButtonBox(QDialogButtonBox.StandardButton.Ok|QDialogButtonBox.StandardButton.Cancel)
        buttons.button(QDialogButtonBox.StandardButton.Ok).setText('Tạo project chỉnh sửa được')
        buttons.accepted.connect(self.commit);buttons.rejected.connect(self.reject);v.addWidget(buttons)
    def choose_voice(self):
        p,_=QFileDialog.getOpenFileName(self,'Voice','','Âm thanh (*.wav *.mp3 *.m4a *.flac *.ogg *.opus)')
        if p:self.voice.setText(p)
    def choose_folder(self):
        p=QFileDialog.getExistingDirectory(self,'Thư mục hình')
        if p:self.folder.setText(p)
    def choose_script(self):
        p,_=QFileDialog.getOpenFileName(self,'Kịch bản','','Kịch bản (*.txt *.srt)')
        if p:
            try:self.script.setPlainText(Path(p).read_text(encoding='utf-8-sig'))
            except Exception as exc:error(self,exc)
    def suggest(self):
        if self.worker and self.worker.isRunning():return
        try:
            folder=Path(self.folder.text()) if self.folder.text() else None
            assets=[p for p in folder.iterdir() if p.suffix.lower() in ('.png','.jpg','.jpeg','.webp','.svg')] if folder else []
            text=self.script.toPlainText();voice=self.voice.text();name=self.name.text();assist=self.pause_assist.isChecked()
            from .workers import Worker
            self.notice.setText('Đang phân tích lời và chuẩn bị bố cục…');self.tabs.setCurrentIndex(1)
            self.worker=Worker(lambda _:suggest_board(text,voice,assets,pause_assist=assist),self)
            def done(board):self.board=board;self.board['name']=name;self.populate()
            self.worker.done.connect(done);self.worker.failed.connect(lambda message:error(self,message));self.worker.start()
        except Exception as exc:error(self,exc)
    def populate(self):
        self.table.setRowCount(0)
        for row in self.board['rows']:self.add_row(row)
        self.voice.setText(self.board.get('voice',''));self.name.setText(self.board.get('name','Video minh họa'))
        self.notice.setText('Mốc từ SRT. Kiểm tra lại bố cục và hình trước khi tạo project.' if self.board.get('timing')=='srt' else
            'Thời gian ước lượng theo độ dài lời. Căn lại bằng voice/waveform sau khi tạo project hoặc nhập SRT để có timestamp. Ghép ảnh theo tên file chỉ là gợi ý; hãy kiểm tra từng cảnh.')
        self.tabs.setCurrentIndex(1)
        gaps=[r.get('missing_visual') for r in self.board['rows'] if r.get('missing_visual') and not r.get('assets')]
        if gaps:self.notice.setText(self.notice.text()+f'\nCó {len(gaps)} cảnh cần chọn minh họa. Video final sẽ kiểm tra hình còn thiếu.')
    def closeEvent(self,event):
        if self.worker and self.worker.isRunning():event.ignore();return
        super().closeEvent(event)
    def reject(self):
        if self.worker and self.worker.isRunning():return
        super().reject()
    def add_row(self,data=None):
        if not isinstance(data,dict):
            try:end=float(self.table.item(self.table.rowCount()-1,1).text()) if self.table.rowCount() else 0
            except ValueError:error(self,'Mốc kết thúc cảnh trước cần là số giây.');return
            data=dict(start=end,end=end+5,title='Cảnh mới',text='',assets=[],labels=[],layout='presenter',pose='explain')
        r=self.table.rowCount();self.table.insertRow(r);self.table.setRowHeight(r,70)
        values={0:f"{data['start']:.3f}",1:f"{data['end']:.3f}",2:data.get('title',''),5:'\n'.join(data.get('assets',[])),6:' | '.join(data.get('labels',[])),7:data.get('text','')}
        for c,value in values.items():self.table.setItem(r,c,QTableWidgetItem(value))
        self.table.item(r,0).setData(Qt.ItemDataRole.UserRole,copy.deepcopy(data))
        for c,options,key,default in ((3,LAYOUTS,'layout','presenter'),(4,POSES,'pose','explain')):
            combo=QComboBox()
            for k,label in options.items():combo.addItem(label,k)
            combo.setCurrentIndex(max(0,combo.findData(data.get(key,default))));self.table.setCellWidget(r,c,combo)
    def remove_row(self):
        if self.table.currentRow()>=0:self.table.removeRow(self.table.currentRow())
    def row_assets(self):
        r=self.table.currentRow()
        if r<0:return
        paths,_=QFileDialog.getOpenFileNames(self,'Hình cho cảnh','','Ảnh (*.png *.jpg *.jpeg *.webp *.svg)')
        if paths:self.table.item(r,5).setText('\n'.join(paths))
    def data(self):
        rows=[]
        for r in range(self.table.rowCount()):
            old=self.table.item(r,0).data(Qt.ItemDataRole.UserRole) or {}
            start=float(self.table.item(r,0).text());end=float(self.table.item(r,1).text())
            data=copy.deepcopy(old);data.update(start=start,end=end,title=self.table.item(r,2).text(),layout=self.table.cellWidget(r,3).currentData(),pose=self.table.cellWidget(r,4).currentData(),
                assets=[x.strip() for x in self.table.item(r,5).text().splitlines() if x.strip()],labels=[x.strip() for x in self.table.item(r,6).text().split('|') if x.strip()],text=self.table.item(r,7).text())
            for k in ('cue_start','cue_end'):data.pop(k,None)
            if abs(start-old.get('start',-1))<.001 and abs(end-old.get('end',-1))<.001:
                for k in ('cue_start','cue_end'):
                    if k in old:data[k]=old[k]
            rows.append(data)
        return dict(version=1,name=self.name.text(),voice=self.voice.text(),timing=(self.board or {}).get('timing','manual'),rows=rows)
    def import_board(self):
        path,_=QFileDialog.getOpenFileName(self,'Storyboard','','JSON (*.json)')
        if path:
            try:self.board=load_board(path);self.populate()
            except Exception as exc:error(self,exc)
    def save_board(self):
        try:
            data=self.data();path,_=QFileDialog.getSaveFileName(self,'Lưu storyboard','','JSON (*.json)')
            if path:Path(path).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
        except Exception as exc:error(self,exc)
    def commit(self):
        try:
            self.result_project=compile_board(self.data());self.result_project['subtitle_style']['enabled']=self.subtitles.isChecked();self.accept()
        except Exception as exc:error(self,exc)

class GraphicDialog(QDialog):
    def __init__(self,obj,parent=None):
        super().__init__(parent);self.obj=obj;self.setWindowTitle('Chữ / hình / trình bày');self.resize(520,620)
        from PySide6.QtWidgets import QScrollArea
        v=QVBoxLayout(self);scroll=QScrollArea();scroll.setWidgetResizable(True);panel=QWidget();form=QFormLayout(panel);scroll.setWidget(panel);v.addWidget(scroll);self.fields={}
        self.text=QPlainTextEdit(obj.get('text',''));self.text.setMaximumHeight(130);form.addRow('Nội dung',self.text)
        self.file=QLineEdit(obj.get('file',''))
        if obj.get('kind')=='image':
            row=QHBoxLayout();row.addWidget(self.file);choose=QPushButton('Thay ảnh…');row.addWidget(choose);form.addRow('Tài nguyên',row)
            def choose_file():
                path,_=QFileDialog.getOpenFileName(self,'Thay ảnh','','Ảnh (*.png *.jpg *.jpeg *.webp *.svg)')
                if path:self.file.setText(path)
            choose.clicked.connect(choose_file)
        for key,label,default,low,high in [('width','Rộng',400,10,5000),('height','Cao',200,10,5000),('font_size','Cỡ chữ',32,10,160),('stroke','Nét',3,0,20),('enter_duration','Hiện dần (s)',.3,0,10)]:
            widget=spin(obj.get(key,default),low,high,.1);self.fields[key]=widget;form.addRow(label,widget)
        self.color=QLineEdit(obj.get('color','#24323a'));form.addRow('Màu chữ / nét',self.color)
        self.fill=QLineEdit(obj.get('fill','#fff5d8'));form.addRow('Màu nền',self.fill)
        self.shape=QComboBox();self.shape.addItems(['card','callout','ellipse','arrow','line','check','cross','path']);self.shape.setCurrentText(obj.get('shape','card'));form.addRow('Hình',self.shape)
        self.points=QLineEdit(json.dumps(obj.get('points',[])));form.addRow('Điểm đường [[x,y],…]',self.points)
        self.fit=QComboBox();self.fit.addItems(['contain','cover']);self.fit.setCurrentText(obj.get('fit','contain'));form.addRow('Ảnh: vừa / lấp khung',self.fit)
        self.bold=QCheckBox('Chữ đậm');self.bold.setChecked(obj.get('bold',False));form.addRow(self.bold)
        self.align=QComboBox();self.align.addItems(['center','left']);self.align.setCurrentText(obj.get('align','center'));form.addRow('Căn chữ',self.align)
        from PySide6.QtWidgets import QFontComboBox
        from PySide6.QtGui import QFont
        self.font=QFontComboBox();self.font.setCurrentFont(QFont(obj.get('font','Segoe UI')));form.addRow('Phông chữ',self.font)
        self.crop=[]
        for i,label in enumerate(('Crop X','Crop Y','Crop rộng','Crop cao')):
            w=spin(obj.get('crop',[0,0,1,1])[i],0 if i<2 else .01,1,.05);self.crop.append(w);form.addRow(label,w)
        self.group=QLineEdit(obj.get('group',''));form.addRow('Tên nhóm di chuyển',self.group)
        self.locked=QCheckBox('Khóa kéo trên canvas');self.locked.setChecked(obj.get('locked',False));form.addRow(self.locked)
        self.fade=QCheckBox('Hiện dần');self.fade.setChecked(obj.get('enter')=='fade');form.addRow(self.fade)
        buttons=QDialogButtonBox(QDialogButtonBox.StandardButton.Save|QDialogButtonBox.StandardButton.Cancel);buttons.accepted.connect(self.commit);buttons.rejected.connect(self.reject);v.addWidget(buttons)
    def commit(self):
        from PySide6.QtGui import QColor
        if not QColor(self.color.text()).isValid() or not QColor(self.fill.text()).isValid():error(self,'Màu phải hợp lệ, ví dụ #24323a.');return
        crop=[w.value() for w in self.crop]
        if crop[0]+crop[2]>1.001 or crop[1]+crop[3]>1.001:error(self,'Crop cần nằm trong vùng ảnh 0–1.');return
        try:
            import math
            points=json.loads(self.points.text())
            if not isinstance(points,list) or any(len(pt)!=2 or not all(math.isfinite(float(x)) for x in pt) for pt in points):raise ValueError()
        except (ValueError,TypeError):error(self,'Điểm cần có dạng [[0,0],[100,50]] với tọa độ hữu hạn.');return
        self.obj.update({k:w.value() for k,w in self.fields.items()})
        if self.obj.get('kind')=='image':
            candidate=self.file.text().strip()
            if Path(candidate).is_absolute() and not Path(candidate).is_file():error(self,'Không tìm thấy ảnh đã chọn.');return
            self.obj['file']=candidate
        self.obj.update(text=self.text.toPlainText(),color=self.color.text(),fill=self.fill.text(),shape=self.shape.currentText(),fit=self.fit.currentText(),
            bold=self.bold.isChecked(),align=self.align.currentText(),font=self.font.currentFont().family(),crop=crop,points=points,group=self.group.text().strip(),locked=self.locked.isChecked(),enter='fade' if self.fade.isChecked() else 'none')
        self.accept()
