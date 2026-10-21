"""The Studio's small vector desk: static artwork, semantic layers, no rig."""
import copy
import json
import math
from pathlib import Path

from PySide6.QtCore import Qt, Signal, QPointF, QRectF
from PySide6.QtGui import QColor, QPainter, QPen, QPainterPathStroker, QAction, QKeySequence
from PySide6.QtWidgets import (QDialog, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QComboBox, QDoubleSpinBox, QCheckBox, QLabel, QListWidget, QListWidgetItem,
    QSplitter, QFileDialog, QInputDialog, QMessageBox)

from .. import drawing as ink


class BasicDrawingCanvas(QWidget):
    changed = Signal()
    selection_changed = Signal(int)

    def __init__(self, doc, parent=None):
        super().__init__(parent)
        self.doc = copy.deepcopy(doc)
        self.index = 0; self.tool = 'pen'; self.color = ink.INK; self.fill = '#d9e8e3'
        self.size = 3.5; self.closed = False
        self.points = []; self.drag = None; self.undo_states = []; self.redo_states = []
        self.setMinimumSize(640, 360); self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def remember(self):
        self.undo_states.append(copy.deepcopy(self.doc)); self.undo_states = self.undo_states[-80:]
        self.redo_states.clear()

    def undo(self):
        self.points = []
        if self.undo_states:
            self.redo_states.append(copy.deepcopy(self.doc)); self.doc = self.undo_states.pop()
            self.index = min(self.index, len(self.doc['layers']) - 1)
            self.changed.emit(); self.update()

    def redo(self):
        if self.redo_states:
            self.undo_states.append(copy.deepcopy(self.doc)); self.doc = self.redo_states.pop()
            self.index = min(self.index, len(self.doc['layers']) - 1)
            self.changed.emit(); self.update()

    def mapping(self):
        scale = min((self.width() - 28) / self.doc['width'], (self.height() - 28) / self.doc['height'])
        return scale, (self.width() - self.doc['width'] * scale) / 2, (self.height() - self.doc['height'] * scale) / 2

    def point(self, event):
        scale, x, y = self.mapping()
        return QPointF((event.position().x() - x) / scale, (event.position().y() - y) / scale)

    def local(self, point):
        dx, dy = self.doc['layers'][self.index].get('offset', [0, 0])
        return [point.x() - dx, point.y() - dy]

    def paintEvent(self, event):
        p = QPainter(self); p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.fillRect(self.rect(), QColor('#e7eae8'))
        scale, x, y = self.mapping(); p.translate(x, y); p.scale(scale, scale)
        rect = QRectF(0, 0, self.doc['width'], self.doc['height'])
        p.fillRect(rect, QColor('white')); p.setClipRect(rect)
        for entry in self.doc['layers']: ink.paint_layer(p, entry)
        if self.points:
            entry = ink.layer('Đang vẽ'); entry['offset'] = self.doc['layers'][self.index].get('offset', [0, 0])
            entry['items'] = [self.current_stroke()]; ink.paint_layer(p, entry)
        if self.tool == 'move':
            entry = self.doc['layers'][self.index]
            if entry.get('visible', True) and entry['items']:
                p.setPen(QPen(QColor('#40827e'), 1 / scale, Qt.PenStyle.DashLine))
                p.setBrush(Qt.BrushStyle.NoBrush); p.drawRect(ink.layer_bounds(entry))
        p.end()

    def current_stroke(self):
        if self.tool == 'polygon':
            commands = [['M', *self.points[0]]] + [['L', *pt] for pt in self.points[1:]]
            if self.closed: commands.append(['Z'])
            return dict(kind='path', commands=commands, stroke=self.color, width=self.size,
                        fill=self.fill if self.closed else 'none')
        return ink.stroke_item(self.points, self.color, self.size, self.fill, self.closed)

    def finish(self):
        if self.points:
            self.remember()
            self.doc['layers'][self.index]['items'].append(self.current_stroke())
            self.points = []; self.changed.emit(); self.update()

    def set_tool(self, tool):
        self.finish(); self.tool = tool; self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self.finish(); return
        if event.button() != Qt.MouseButton.LeftButton: return
        self.setFocus(); point = self.point(event)
        if not QRectF(0, 0, self.doc['width'], self.doc['height']).contains(point): return
        entry = self.doc['layers'][self.index]
        if not entry.get('visible', True) or entry.get('locked'): return
        if self.tool == 'move':
            if ink.layer_bounds(entry).contains(point):
                self.remember(); self.drag = (point, list(entry.get('offset', [0, 0])))
        elif self.tool == 'erase':
            pt = QPointF(*self.local(point))
            for i in range(len(entry['items']) - 1, -1, -1):
                item = entry['items'][i]
                if item['kind'] == 'text': hit = ink.item_bounds(item).contains(pt)
                else:
                    path = ink.painter_path(item); stroker = QPainterPathStroker()
                    stroker.setWidth(max(14, item.get('width', 3.5) + 8))
                    hit = stroker.createStroke(path).contains(pt) or (item.get('fill', 'none') != 'none' and path.contains(pt))
                if hit:
                    self.remember(); entry['items'].pop(i); self.changed.emit(); self.update(); break
        elif self.tool == 'text':
            text, ok = QInputDialog.getText(self, 'Chữ trong hình', 'Nội dung')
            if ok and text:
                self.remember(); entry['items'].append(dict(kind='text', text=text, at=self.local(point), size=28, stroke=self.color))
                self.changed.emit(); self.update()
        elif self.tool == 'polygon':
            self.points.append(self.local(point)); self.update()
        else:
            self.points = [self.local(point)]; self.update()

    def mouseMoveEvent(self, event):
        point = self.point(event)
        if self.drag:
            anchor, original = self.drag
            self.doc['layers'][self.index]['offset'] = [original[0] + point.x() - anchor.x(), original[1] + point.y() - anchor.y()]
            self.update()
        elif self.points and self.tool == 'pen' and event.buttons() & Qt.MouseButton.LeftButton:
            pt = self.local(point)
            if math.dist(pt, self.points[-1]) >= .8:
                self.points.append(pt); self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.drag: self.drag = None; self.changed.emit()
            elif self.tool == 'pen' and self.points:
                self.points.append(self.local(self.point(event))); self.finish()

    def mouseDoubleClickEvent(self, event):
        if self.tool == 'polygon': self.finish()

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter): self.finish()
        elif event.key() == Qt.Key.Key_Escape: self.points = []; self.update()
        else: super().keyPressEvent(event)


from .drawing_editor import EditingCanvasMixin


class DrawingCanvas(EditingCanvasMixin, BasicDrawingCanvas):
    pass


class DrawingDialog(QDialog):
    def __init__(self, doc=None, parent=None, standalone=False):
        super().__init__(parent)
        self.setWindowTitle('Bàn vẽ Studio · dựng hình và chỉnh nét'); self.resize(1440, 920)
        self.result_doc = None
        from ..character_qc import ROOT
        self.qc_root = Path(parent.root) if parent is not None and hasattr(parent, 'root') else ROOT
        layout = QVBoxLayout(self)
        heading = QLabel('BÀN VẼ STUDIO     /     Nét viền • Màu phẳng • Lớp độc lập')
        heading.setStyleSheet('font-size:17px;font-weight:600;padding:8px'); layout.addWidget(heading)
        row = QHBoxLayout(); layout.addLayout(row)
        self.tools = QComboBox()
        for title, tool in [('Bút nét', 'pen'), ('Bút đậm nhạt', 'brush'), ('Chọn / kéo nét', 'select'),
                            ('Sửa nút Bézier', 'node'), ('Vẽ Bézier', 'bezier'), ('Mốc dựng hình', 'guide'),
                            ('Kéo khung nhìn', 'pan'), ('Đường gấp / vùng kín', 'polygon'),
                            ('Di chuyển lớp', 'move'), ('Tẩy cả nét', 'erase'), ('Chữ', 'text')]:
            self.tools.addItem(title, tool)
        row.addWidget(self.tools)
        self.stroke_color = QComboBox(); self.fill_color = QComboBox()
        names = ['Mực', 'Trắng', 'Da', 'Xanh ngọc', 'Xanh nhạt', 'Đất nung', 'Đá', 'Xanh chú giải', 'Đỏ nhấn']
        for title, color in zip(names, ink.PALETTE):
            self.stroke_color.addItem(title, color); self.fill_color.addItem(title, color)
        self.fill_color.setCurrentIndex(4)
        row.addWidget(QLabel('Nét')); row.addWidget(self.stroke_color)
        self.size = QDoubleSpinBox(); self.size.setRange(1, 18); self.size.setSingleStep(.5); self.size.setValue(3.5)
        row.addWidget(self.size); row.addWidget(QLabel('px'))
        self.closed = QCheckBox('Khép kín + tô'); row.addWidget(self.closed); row.addWidget(self.fill_color); row.addStretch()
        for title, callback in [('↶', lambda: self.canvas.undo()), ('↷', lambda: self.canvas.redo())]:
            button = QPushButton(title); button.clicked.connect(callback); row.addWidget(button)
        splitter = QSplitter(); layout.addWidget(splitter, 1)
        self.canvas = DrawingCanvas(doc or ink.document()); splitter.addWidget(self.canvas)
        self.saved_doc = copy.deepcopy(self.canvas.doc)
        self.protect_unsaved = False  # Enabled by production entry points, not offscreen test dialogs.
        from .drawing_panels import install_panels, install_toolbar
        install_toolbar(self, layout)
        side = QWidget(); right = QVBoxLayout(side); right.addWidget(QLabel('LỚP VẼ  ·  lớp trên cùng ở đầu danh sách'))
        self.layers = QListWidget(); right.addWidget(self.layers, 1)
        self.draft = QCheckBox('Lớp phác · không xuất vào phim'); right.addWidget(self.draft)
        self.locked = QCheckBox('Khóa nét trên lớp'); right.addWidget(self.locked)
        self.role = QComboBox()
        for title, role in [('Chưa phân loại', 'unclassified'), ('Vật thể / chữ / sơ đồ', 'object'), ('Nhân vật · QC bắt buộc', 'character')]:self.role.addItem(title, role)
        right.addWidget(self.role)
        qc_button = QPushButton('QC nhân vật…'); qc_button.clicked.connect(self.character_qc); right.addWidget(qc_button)
        self.qc_status = QLabel(); self.qc_status.setWordWrap(True); right.addWidget(self.qc_status)
        for title, callback in [('+ Lớp', self.add_layer), ('Đổi tên lớp', self.rename_layer), ('↑ Đưa lên', lambda: self.reorder(1)), ('↓ Đưa xuống', lambda: self.reorder(-1)), ('Xóa lớp', self.delete_layer)]:
            button = QPushButton(title); button.clicked.connect(callback); right.addWidget(button)
        guide = QLabel('Cuộn: phóng to tại con trỏ. Chuột giữa: kéo khung.\nChọn nét: Shift để chọn nhiều.\nBézier: đầu nét → tay nắm 1 → tay nắm 2 → cuối đoạn. Enter để kết thúc.\nTab Chuẩn: ba ảnh tham chiếu.\nTab Mốc: dựng hình liên kết. Tab Nét: chỉnh hình và hồ sơ nhân vật.')
        guide.setWordWrap(True); right.addWidget(guide)
        install_panels(self, splitter, side)
        self.hint = QLabel(); layout.addWidget(self.hint)
        row = QHBoxLayout(); layout.addLayout(row)
        for title, callback in [('Mở bản vẽ…', self.open_doc), ('Lưu bản vẽ…', self.save_doc), ('Xuất SVG…', self.export_svg), ('Xuất PNG…', self.export_png), ('Bài tập công cụ', self.sample)]:
            button = QPushButton(title); button.clicked.connect(callback); row.addWidget(button)
        row.addStretch()
        cancel = QPushButton('Đóng'); cancel.clicked.connect(self.reject); row.addWidget(cancel)
        accept = QPushButton('Lưu bản vẽ…' if standalone else 'Đưa từng lớp vào cảnh'); accept.setObjectName('primary')
        accept.clicked.connect(self.save_doc if standalone else self.accept_drawing); row.addWidget(accept)
        self.canvas.changed.connect(self.refresh_layers)
        self.tools.currentIndexChanged.connect(lambda _: self.canvas.set_tool(self.tools.currentData()))
        self.stroke_color.currentIndexChanged.connect(lambda _: setattr(self.canvas, 'color', self.stroke_color.currentData()))
        self.fill_color.currentIndexChanged.connect(lambda _: setattr(self.canvas, 'fill', self.fill_color.currentData()))
        self.size.valueChanged.connect(lambda value: setattr(self.canvas, 'size', value))
        self.closed.toggled.connect(lambda value: setattr(self.canvas, 'closed', value))
        self.layers.currentRowChanged.connect(self.select_layer); self.layers.itemChanged.connect(self.visibility)
        self.role.currentIndexChanged.connect(self.set_role)
        self.draft.toggled.connect(lambda value: self.layer_flag('draft', value))
        self.locked.toggled.connect(lambda value: self.layer_flag('locked', value))
        for key, callback in [('Ctrl+Z', self.canvas.undo), ('Ctrl+Y', self.canvas.redo)]:
            action = QAction(self); action.setShortcut(QKeySequence(key)); action.triggered.connect(callback); self.addAction(action)
        self.refresh_layers()

    def layer_flag(self, key, value):
        self.canvas.finish(); self.canvas.remember()
        self.canvas.entry[key] = value; self.refresh_layers()

    def reject(self):
        self.canvas.finish()
        if self.protect_unsaved and self.canvas.doc != self.saved_doc:
            answer = QMessageBox.question(self, 'Bản vẽ chưa lưu', 'Lưu bản vẽ trước khi đóng?',
                QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel,
                QMessageBox.StandardButton.Save)
            if answer == QMessageBox.StandardButton.Cancel: return
            if answer == QMessageBox.StandardButton.Save and not self.save_doc(): return
        super().reject()

    def refresh_layers(self):
        self.layers.blockSignals(True); self.layers.clear()
        for index in range(len(self.canvas.doc['layers']) - 1, -1, -1):
            entry = self.canvas.doc['layers'][index]; item = QListWidgetItem(entry['name'])
            item.setData(Qt.ItemDataRole.UserRole, index)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Checked if entry.get('visible', True) else Qt.CheckState.Unchecked)
            self.layers.addItem(item)
        self.layers.setCurrentRow(len(self.canvas.doc['layers']) - 1 - self.canvas.index)
        self.layers.blockSignals(False)
        count = sum(len(e['items']) for e in self.canvas.doc['layers'])
        self.hint.setText(f'{len(self.canvas.doc["layers"])} lớp · {count} nét / hình · Vector chỉnh sửa được · Không dùng mô hình sinh ảnh')
        self.canvas.update()
        self.refresh_qc()
        for control, key in ((self.draft, 'draft'), (self.locked, 'locked')):
            control.blockSignals(True); control.setChecked(bool(self.canvas.entry.get(key))); control.blockSignals(False)
        self.construction.refresh(); self.path_panel.refresh()

    def select_layer(self, row):
        if row < 0: return
        self.canvas.finish(); self.canvas.reset_selection()
        self.canvas.index = len(self.canvas.doc['layers']) - 1 - row; self.refresh_layers()

    def refresh_qc(self):
        from ..character_qc import is_character, review_issues
        entry = self.canvas.doc['layers'][self.canvas.index]
        self.role.blockSignals(True); self.role.setCurrentIndex(max(0, self.role.findData(entry.get('role', 'unclassified')))); self.role.blockSignals(False)
        issues = review_issues(entry, self.qc_root) if is_character(entry) else []
        self.qc_status.setText(('QC: cần sửa / kiểm tra lại\n' + issues[0]) if issues else ('QC nhân vật: đạt cho nét hiện tại' if is_character(entry) else 'Lớp vật thể / chữ' if entry.get('role') == 'object' else 'Cần phân loại lớp trước khi đưa vào cảnh.'))

    def set_role(self):
        self.canvas.finish(); self.canvas.remember()
        self.canvas.doc['layers'][self.canvas.index]['role'] = self.role.currentData(); self.refresh_qc()

    def character_qc(self):
        from ..character_qc import is_character
        from .character_qc_dialog import CharacterQCDialog
        self.canvas.finish(); entry = self.canvas.doc['layers'][self.canvas.index]
        if not is_character(entry):
            QMessageBox.information(self, 'QC nhân vật', 'Chọn lớp nhân vật cần kiểm tra.'); return
        self.canvas.remember()
        try:
            dialog = CharacterQCDialog(entry, self.qc_root, self); dialog.exec(); self.refresh_qc()
        except Exception as exc: QMessageBox.warning(self, 'Hồ sơ QC', str(exc))

    def ready(self):
        from ..character_qc import drawing_issues
        issues = drawing_issues(self.canvas.doc, self.qc_root)
        if issues:
            QMessageBox.warning(self, 'Chưa đạt QC', '\n'.join(issues[:14])); return False
        return True

    def visibility(self, item):
        self.canvas.remember(); self.canvas.doc['layers'][item.data(Qt.ItemDataRole.UserRole)]['visible'] = item.checkState() == Qt.CheckState.Checked
        self.canvas.update()

    def add_layer(self):
        self.canvas.finish()
        name, ok = QInputDialog.getText(self, 'Lớp mới', 'Tên', text='Nét vẽ ' + str(len(self.canvas.doc['layers']) + 1))
        if ok and name:
            self.canvas.remember(); self.canvas.reset_selection(); self.canvas.doc['layers'].append(dict(ink.layer(name),role='unclassified')); self.canvas.index = len(self.canvas.doc['layers']) - 1; self.refresh_layers()

    def rename_layer(self):
        entry = self.canvas.doc['layers'][self.canvas.index]
        name, ok = QInputDialog.getText(self, 'Đổi tên lớp', 'Tên', text=entry['name'])
        if ok and name: self.canvas.remember(); entry['name'] = name; self.refresh_layers()

    def reorder(self, delta):
        self.canvas.finish(); i = self.canvas.index; j = i + delta
        if 0 <= j < len(self.canvas.doc['layers']):
            self.canvas.remember(); entries = self.canvas.doc['layers']; entries[i], entries[j] = entries[j], entries[i]
            self.canvas.index = j; self.refresh_layers()

    def delete_layer(self):
        self.canvas.finish(); self.canvas.remember(); self.canvas.reset_selection(); self.canvas.doc['layers'].pop(self.canvas.index)
        if not self.canvas.doc['layers']: self.canvas.doc['layers'].append(dict(ink.layer('Nét vẽ 1'),role='unclassified'))
        self.canvas.index = min(self.canvas.index, len(self.canvas.doc['layers']) - 1); self.refresh_layers()

    def open_doc(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Mở bản vẽ Studio', '', 'Bản vẽ (*.drawing.json *.json)')
        if path:
            try:
                doc = ink.validate(json.loads(Path(path).read_text(encoding='utf-8-sig')))
                self.canvas.finish(); self.canvas.remember(); self.canvas.reset_selection()
                self.canvas.doc = doc; self.canvas.index = 0; self.canvas.points = []; self.canvas.fit_view(); self.refresh_layers()
                self.saved_doc = copy.deepcopy(doc)
            except Exception as exc: QMessageBox.warning(self, 'Không mở được', str(exc))

    def save_doc(self):
        self.canvas.finish()
        path, _ = QFileDialog.getSaveFileName(self, 'Lưu bản vẽ', 'ban-ve.drawing.json', 'Bản vẽ (*.drawing.json)')
        if path:
            try:
                ink.save_drawing(self.canvas.doc, path); self.saved_doc = copy.deepcopy(self.canvas.doc)
                return True
            except (ValueError, OSError) as exc: QMessageBox.warning(self, 'Không lưu được', str(exc))
        return False

    def export_svg(self):
        self.canvas.finish()
        if not self.ready():return
        path, _ = QFileDialog.getSaveFileName(self, 'Xuất vector', 'ban-ve.svg', 'SVG (*.svg)')
        if path: Path(path).write_text(ink.svg(self.canvas.doc)[0], encoding='utf-8')

    def export_png(self):
        self.canvas.finish()
        if not self.ready():return
        path, _ = QFileDialog.getSaveFileName(self, 'Xuất ảnh xem trước', 'ban-ve.png', 'PNG (*.png)')
        if path: ink.render(self.canvas.doc).save(path)

    def sample(self):
        from ..drawing_workbench_sample import workbench_document
        self.canvas.finish(); self.canvas.remember(); self.canvas.reset_selection()
        self.canvas.doc = workbench_document(); self.canvas.index = 0; self.canvas.fit_view(); self.refresh_layers()

    def accept_drawing(self):
        self.canvas.finish()
        if not self.ready():return
        if not any(e['items'] and e.get('visible', True) for e in self.canvas.doc['layers']):
            QMessageBox.information(self, 'Bàn vẽ', 'Vẽ ít nhất một nét trên lớp đang hiển thị.'); return
        self.result_doc = copy.deepcopy(self.canvas.doc); self.accept()
