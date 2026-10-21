"""Reference, construction and selected-path controls for the Studio drawing desk."""
import copy
import json
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QColor
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTabWidget, QScrollArea, QDialog, QComboBox, QLineEdit, QCheckBox, QMessageBox,
    QColorDialog, QInputDialog, QFileDialog, QDoubleSpinBox)

from .. import drawing as ink
from .. import drawing_edit as edit
from ..project import uid


def button(layout, title, callback):
    control = QPushButton(title); control.clicked.connect(callback); layout.addWidget(control)
    return control


def reference_panel():
    from ..character_qc import STYLE, reference_manifest
    panel = QScrollArea(); panel.setWidgetResizable(True)
    content = QWidget(); layout = QVBoxLayout(content)
    label = QLabel('BA ẢNH CHUẨN\nBấm ảnh để xem lớn. Chỉ đối chiếu, không xuất vào phim.')
    label.setWordWrap(True); layout.addWidget(label)
    try:
        references = reference_manifest()['references']
    except Exception as exc:
        layout.addWidget(QLabel(str(exc))); references = []
    for index, entry in enumerate(references, 1):
        path = STYLE / entry['file']; pix = QPixmap(str(path))
        title = QLabel(f'Tham chiếu {index}'); layout.addWidget(title)
        control = QPushButton()
        from PySide6.QtGui import QIcon
        from PySide6.QtCore import QSize
        control.setIcon(QIcon(pix)); control.setIconSize(QSize(250, 155)); control.setMinimumHeight(165)
        def show(checked=False, image=pix, number=index):
            viewer = QDialog(panel); viewer.setWindowTitle(f'Tham chiếu {number} · ảnh gốc')
            viewer.resize(1100, 760); outer = QVBoxLayout(viewer)
            scroll = QScrollArea(); picture = QLabel(); picture.setPixmap(image)
            scroll.setWidget(picture); outer.addWidget(scroll)
            button(outer, 'Đóng', viewer.accept); viewer.exec()
        control.clicked.connect(show); layout.addWidget(control)
    layout.addStretch(); panel.setWidget(content)
    return panel


class ConstructionPanel(QWidget):
    def __init__(self, desk):
        super().__init__(); self.desk = desk; self.canvas = desk.canvas
        layout = QVBoxLayout(self)
        note = QLabel('MỐC DỰNG HÌNH\nMốc chỉ giúp chỉnh bản vẽ, không lên phim. Gắn nhóm nét vào một mốc để kéo chúng cùng nhau.')
        note.setWordWrap(True); layout.addWidget(note)
        self.name = QLineEdit('head'); self.name.setPlaceholderText('Tên mốc'); layout.addWidget(self.name)
        self.parent_guide = QComboBox(); layout.addWidget(QLabel('Mốc cha khi thêm mốc mới')); layout.addWidget(self.parent_guide)
        self.fixed = QCheckBox('Giữ khoảng cách tới mốc cha'); layout.addWidget(self.fixed)
        self.show = QCheckBox('Hiện mốc trên bàn vẽ'); self.show.setChecked(True); layout.addWidget(self.show)
        button(layout, 'Đặt / kéo mốc trên canvas', self.activate)
        self.anchor = QComboBox(); layout.addWidget(QLabel('Gắn các nét đang chọn vào')); layout.addWidget(self.anchor)
        button(layout, 'Gắn nhóm nét đã chọn', self.bind)
        button(layout, 'Nối nút đang chọn vào mốc', self.bind_node)
        button(layout, 'Tháo liên kết nhóm nét', self.unbind)
        button(layout, 'Xóa mốc đã chọn', self.remove)
        self.status = QLabel(); self.status.setWordWrap(True); layout.addWidget(self.status)
        layout.addStretch()
        self.name.textChanged.connect(self.settings)
        self.parent_guide.currentIndexChanged.connect(self.settings); self.fixed.toggled.connect(self.settings)
        self.show.toggled.connect(lambda value: (setattr(self.canvas, 'show_guides', value), self.canvas.update()))
        self.canvas.changed.connect(self.refresh); self.canvas.selection_changed.connect(self.refresh)
        self.refresh()

    def settings(self, *_):
        self.canvas.guide_name = self.name.text().strip() or 'moc'
        self.canvas.guide_parent = self.parent_guide.currentData()
        self.canvas.guide_lock = self.fixed.isChecked()

    def activate(self):
        self.settings(); self.desk.tools.setCurrentIndex(self.desk.tools.findData('guide'))

    def refresh(self, *_):
        self.setEnabled(not self.canvas.entry.get('locked'))
        for control in (self.parent_guide, self.anchor):
            old = control.currentData(); control.blockSignals(True)
            control.clear(); control.addItem('Không chọn', None)
            for guide in self.canvas.entry.get('guides', []): control.addItem(guide['name'], guide['id'])
            control.setCurrentIndex(max(0, control.findData(old))); control.blockSignals(False)
        self.settings()
        self.status.setText(f'{len(self.canvas.entry.get("guides", []))} mốc · {len(self.canvas.selected)} nét được chọn\nChọn nhiều nét: Shift + bấm.')

    def bind(self):
        if not self.canvas.selected or not self.anchor.currentData(): return
        self.canvas.remember()
        edit.bind_items(self.canvas.entry, self.canvas.selected, self.anchor.currentData())
        self.canvas.changed.emit()

    def bind_node(self):
        if not self.canvas.node or not self.anchor.currentData(): return
        original = copy.deepcopy(self.canvas.doc)
        try:
            edit.bind_node(self.canvas.entry, *self.canvas.node, self.anchor.currentData())
        except ValueError as exc:
            self.canvas.doc = original; QMessageBox.information(self, 'Nối nút', str(exc)); return
        self.canvas.undo_states.append(original); self.canvas.redo_states.clear(); self.canvas.changed.emit()

    def unbind(self):
        if not self.canvas.selected: return
        self.canvas.remember()
        for index in self.canvas.selected:
            self.canvas.entry['items'][index].pop('guide_binding', None)
            self.canvas.entry['items'][index].pop('node_bindings', None)
        edit.invalidate(self.canvas.entry); self.canvas.changed.emit()

    def remove(self):
        key = self.anchor.currentData() or self.canvas.active_guide
        if not key: return
        self.canvas.remember(); entry = self.canvas.entry
        entry['guides'] = [g for g in entry.get('guides', []) if g['id'] != key]
        for g in entry['guides']:
            if g.get('parent') == key: g.pop('parent'); g.pop('length', None)
        for item in entry['items']:
            if item.get('guide_binding') == key: item.pop('guide_binding')
            item['node_bindings'] = [b for b in item.get('node_bindings', []) if b['guide'] != key]
        edit.invalidate(entry); self.canvas.active_guide = None; self.canvas.changed.emit()


class PathPanel(QWidget):
    def __init__(self, desk):
        super().__init__(); self.desk = desk; self.canvas = desk.canvas
        layout = QVBoxLayout(self)
        self.status = QLabel('Chọn nét để chỉnh.'); layout.addWidget(self.status)
        button(layout, 'Đổi màu nét đã chọn…', lambda: self.color('stroke'))
        button(layout, 'Đổi màu tô đã chọn…', lambda: self.color('fill'))
        button(layout, 'Bỏ màu tô', lambda: self.set_property('fill', 'none'))
        button(layout, 'Bỏ viền', lambda: self.set_property('stroke', 'none'))
        button(layout, 'Áp dụng cỡ / đậm nhạt / mượt', self.restyle)
        button(layout, 'Khép đường nét', self.close_paths)
        button(layout, 'Chia đôi đoạn tại nút chọn', lambda: self.node_op(edit.split_segment))
        button(layout, 'Thẳng → Bézier', lambda: self.node_op(edit.curve_segment))
        button(layout, 'Xóa nút cuối đoạn đã chọn', lambda: self.node_op(edit.remove_knot))
        button(layout, 'Làm mượt nút nối Bézier', lambda: self.node_op(edit.smooth_knot))
        button(layout, 'Nhân đôi nhóm nét', self.duplicate)
        button(layout, 'Đưa nét lên trước', lambda: self.reorder(True))
        button(layout, 'Đưa nét ra sau', lambda: self.reorder(False))
        self.part = QComboBox()
        from ..character_qc import BASE_PARTS, LOWER_PARTS
        for value in sorted(BASE_PARTS | LOWER_PARTS): self.part.addItem(value)
        layout.addWidget(QLabel('Gắn bộ phận cho nét nhân vật')); layout.addWidget(self.part)
        button(layout, 'Gắn nhãn bộ phận', self.tag)
        button(layout, 'Thiết lập hồ sơ nhân vật…', self.metadata)
        layout.addStretch()
        self.canvas.selection_changed.connect(self.refresh); self.canvas.changed.connect(self.refresh)

    def refresh(self, *_):
        self.setEnabled(not self.canvas.entry.get('locked'))
        self.status.setText(f'Đã chọn {len(self.canvas.selected)} nét. Delete để xóa.')

    def set_property(self, key, value):
        if not self.canvas.selected or self.canvas.entry.get('locked'): return
        self.canvas.remember()
        for i in self.canvas.selected: self.canvas.entry['items'][i][key] = value
        edit.invalidate(self.canvas.entry); self.canvas.changed.emit()

    def color(self, key):
        color = QColorDialog.getColor(QColor(self.canvas.color), self, 'Màu ' + key)
        if color.isValid(): self.set_property(key, color.name())

    def close_paths(self):
        if not self.canvas.selected: return
        self.canvas.remember()
        for i in self.canvas.selected:
            item = self.canvas.entry['items'][i]
            if item.get('commands') and item['commands'][-1][0] != 'Z': item['commands'].append(['Z'])
        edit.invalidate(self.canvas.entry); self.canvas.changed.emit()

    def restyle(self):
        if not self.canvas.selected: return
        self.canvas.remember()
        for i in self.canvas.selected:
            edit.restyle_stroke(self.canvas.entry, i, self.canvas.size, self.canvas.thinning, self.canvas.smoothing)
        self.canvas.changed.emit()

    def node_op(self, operation):
        if not self.canvas.node:
            QMessageBox.information(self, 'Chỉnh nút', 'Chọn công cụ Sửa nút, chọn nét rồi bấm điểm cuối của đoạn.'); return
        i, ci, ai = self.canvas.node
        before = copy.deepcopy(self.canvas.doc)
        try:
            operation(self.canvas.entry, i, ci)
        except ValueError as exc:
            self.canvas.doc = before; QMessageBox.information(self, 'Chỉnh nút', str(exc)); return
        self.canvas.undo_states.append(before); self.canvas.redo_states.clear()
        self.canvas.node = None; self.canvas.changed.emit()

    def duplicate(self):
        if not self.canvas.selected: return
        self.canvas.remember(); indices = []
        for i in sorted(self.canvas.selected):
            item = copy.deepcopy(self.canvas.entry['items'][i]); item['id'] = uid()
            item.pop('guide_binding', None); item.pop('node_bindings', None); edit.translate_item(item, 16, 16)
            indices.append(len(self.canvas.entry['items'])); self.canvas.entry['items'].append(item)
        self.canvas.selected = set(indices); edit.invalidate(self.canvas.entry); self.canvas.changed.emit()

    def reorder(self, front):
        if not self.canvas.selected: return
        self.canvas.remember(); items = self.canvas.entry['items']
        chosen = [p for i, p in enumerate(items) if i in self.canvas.selected]
        rest = [p for i, p in enumerate(items) if i not in self.canvas.selected]
        self.canvas.entry['items'] = rest + chosen if front else chosen + rest
        self.canvas.selected = set(range(len(rest), len(items))) if front else set(range(len(chosen)))
        edit.invalidate(self.canvas.entry); self.canvas.changed.emit()

    def tag(self):
        if not self.canvas.selected: return
        self.canvas.remember()
        for i in self.canvas.selected:
            item = self.canvas.entry['items'][i]
            item['parts'] = sorted(set(item.get('parts', [])) | {self.part.currentText()})
        self.canvas.entry['role'] = 'character'
        edit.invalidate(self.canvas.entry); self.canvas.changed.emit()

    def metadata(self):
        from ..character_qc import PROFILE, LANDMARKS, parts
        entry = self.canvas.entry
        dlg = QDialog(self); dlg.setWindowTitle('Hồ sơ nhân vật · không tự duyệt QC')
        layout = QVBoxLayout(dlg)
        description = QLabel('Đặt các mốc bằng công cụ Mốc với tên bên dưới.\nGắn nhãn bộ phận cho nét. Vùng cận cảnh sẽ lấy theo các nét đã gắn nhãn.')
        description.setWordWrap(True); layout.addWidget(description)
        marks = QLabel(', '.join(sorted(LANDMARKS | {'foot_left', 'foot_right'}))); marks.setWordWrap(True); layout.addWidget(marks)
        identity = QLineEdit(entry.get('character', {}).get('identity', '')); identity.setPlaceholderText('Tên nhận diện mẫu mới')
        # Rejected identities must not be renamed through the UI to evade revocation.
        if identity.text(): identity.setReadOnly(True)
        layout.addWidget(identity)
        view = QComboBox(); view.addItem('Bán thân', 'waist_up'); view.addItem('Toàn thân', 'full_body')
        view.setCurrentIndex(max(0, view.findData(entry.get('character', {}).get('view')))); layout.addWidget(view)
        button(layout, 'Lưu hồ sơ nháp', dlg.accept); button(layout, 'Hủy', dlg.reject)
        if not dlg.exec(): return
        self.canvas.remember()
        meta = entry.setdefault('character', {})
        meta.update(profile=PROFILE, identity=identity.text().strip() or uid(), view=view.currentData())
        meta['landmarks'] = {g['name']: list(g['point']) for g in entry.get('guides', [])}
        regions = meta.setdefault('review_regions', {})
        bypart = parts(entry)
        from PySide6.QtCore import QRectF
        for key, part in (('face', 'head'), ('hand_left', 'hand_left'), ('hand_right', 'hand_right')):
            rect = QRectF()
            for item in bypart.get(part, []): rect = rect.united(ink.item_bounds(item))
            if not rect.isEmpty():
                rect = rect.adjusted(-12, -12, 12, 12); regions[key] = [rect.x(), rect.y(), rect.width(), rect.height()]
        entry['role'] = 'character'; edit.invalidate(entry); self.canvas.changed.emit()


def install_panels(desk, splitter, side):
    tabs = QTabWidget(); tabs.setMinimumWidth(280)
    tabs.addTab(side, 'Lớp')
    tabs.addTab(reference_panel(), 'Chuẩn')
    desk.construction = ConstructionPanel(desk); tabs.addTab(desk.construction, 'Mốc')
    desk.path_panel = PathPanel(desk)
    path_scroll = QScrollArea(); path_scroll.setWidgetResizable(True); path_scroll.setWidget(desk.path_panel)
    tabs.addTab(path_scroll, 'Nét')
    splitter.addWidget(tabs); splitter.setSizes([950, 310])
    desk.editor_tabs = tabs


def install_toolbar(desk, layout):
    row = QHBoxLayout(); layout.addLayout(row)
    button(row, 'Vừa khung · F', desk.canvas.fit_view)
    button(row, 'Màu bút…', lambda: custom_color(desk, False))
    button(row, 'Màu tô…', lambda: custom_color(desk, True))
    row.addWidget(QLabel('Đậm nhạt'))
    thinning = QDoubleSpinBox(); thinning.setRange(0, 1); thinning.setSingleStep(.1); thinning.setValue(.35); row.addWidget(thinning)
    thinning.valueChanged.connect(lambda v: setattr(desk.canvas, 'thinning', v))
    row.addWidget(QLabel('Mượt'))
    smooth = QDoubleSpinBox(); smooth.setRange(0, 1); smooth.setSingleStep(.1); smooth.setValue(.5); row.addWidget(smooth)
    smooth.valueChanged.connect(lambda v: setattr(desk.canvas, 'smoothing', v))
    button(row, 'Lưu lớp vào thư viện…', lambda: save_template(desk))
    button(row, 'Thêm từ thư viện…', lambda: load_template(desk))
    row.addStretch()


def custom_color(desk, fill):
    color = QColorDialog.getColor(QColor(desk.canvas.fill if fill else desk.canvas.color), desk, 'Chọn màu')
    if not color.isValid(): return
    combo = desk.fill_color if fill else desk.stroke_color
    i = combo.findData(color.name())
    if i < 0: combo.addItem(color.name(), color.name()); i = combo.count() - 1
    combo.setCurrentIndex(i)


def save_template(desk):
    desk.canvas.finish()
    name, ok = QInputDialog.getText(desk, 'Lưu mẫu', 'Tên mẫu (nháp vẫn lưu được, QC giữ nguyên)', text=desk.canvas.entry['name'])
    if not ok or not name.strip(): return
    entry = copy.deepcopy(desk.canvas.entry); entry['name'] = name.strip()
    doc = ink.document(); doc.update(width=desk.canvas.doc['width'], height=desk.canvas.doc['height'], layers=[entry])
    folder = Path(desk.qc_root) / 'assets' / 'drawing_library'; folder.mkdir(parents=True, exist_ok=True)
    from ..character_qc import is_character, materialize_evidence
    if is_character(entry) and entry.get('character_qc', {}).get('status') == 'passed':
        materialize_evidence(entry, desk.qc_root)
    ink.save_drawing(doc, folder / (uid() + '.drawing.json'))
    QMessageBox.information(desk, 'Thư viện', 'Đã lưu mẫu. Lưu mẫu không duyệt QC hoặc thay đổi trạng thái bị loại.')


def load_template(desk):
    folder = Path(desk.qc_root) / 'assets' / 'drawing_library'
    folder.mkdir(parents=True, exist_ok=True)
    files = sorted(folder.glob('*.drawing.json')); choices = []; documents = []
    for path in files:
        try:
            doc = ink.validate(json.loads(path.read_text(encoding='utf-8')))
            entry = doc['layers'][0]; status = entry.get('character_qc', {}).get('status', 'nháp')
            choices.append(f'{entry["name"]} · {status} · {path.stem[:8]}'); documents.append(doc)
        except (ValueError, KeyError, TypeError): continue
    if not choices:
        QMessageBox.information(desk, 'Thư viện', 'Chưa có mẫu. Lưu một lớp đã vẽ để tái sử dụng.'); return
    choice, ok = QInputDialog.getItem(desk, 'Thêm mẫu', 'Mẫu lưu trong Studio', choices, 0, False)
    if not ok: return
    desk.canvas.finish(); desk.canvas.remember(); desk.canvas.reset_selection()
    for entry in copy.deepcopy(documents[choices.index(choice)]['layers']):
        entry['id'] = uid(); desk.canvas.doc['layers'].append(entry)
    desk.canvas.index = len(desk.canvas.doc['layers']) - 1; desk.refresh_layers()
