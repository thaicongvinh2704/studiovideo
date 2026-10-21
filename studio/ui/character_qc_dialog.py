"""Visual inspection desk; no automatic aesthetic PASS."""
from pathlib import Path
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTabWidget,
    QScrollArea, QWidget, QCheckBox, QLineEdit, QPushButton, QMessageBox, QSplitter)
from ..character_qc import CHECKS, prepare_packet, geometry_issues, record_review, resolve_evidence


class CharacterQCDialog(QDialog):
    def __init__(self, entry, root, parent=None):
        super().__init__(parent)
        self.entry = entry; self.root = Path(root); self.seen = set()
        self.setWindowTitle('QC nhân vật bắt buộc · ba ảnh tham chiếu'); self.resize(1400, 900)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel('Xem ảnh thực ở từng tab, ghi nhận xét và sửa mọi lỗi trước khi ghi QC. Đây là QC nội bộ.'))
        problems = geometry_issues(entry)
        if problems:
            label = QLabel('Cần sửa hồ sơ / hình trước khi đạt QC:\n' + '\n'.join(problems[:12])); label.setWordWrap(True)
            label.setStyleSheet('color:#ed9d75;padding:8px'); layout.addWidget(label)
        packet = prepare_packet(entry, root)
        splitter = QSplitter(); layout.addWidget(splitter, 1)
        self.tabs = QTabWidget(); splitter.addWidget(self.tabs)
        titles = dict(full='Toàn hình', face='Mặt', hand_left='Tay trái', hand_right='Tay phải',
            thumbnail='Cỡ nhỏ', comparison='Đối chiếu', reference_01='Ảnh chuẩn 1', reference_02='Ảnh chuẩn 2', reference_03='Ảnh chuẩn 3')
        self.kinds = []
        for evidence in packet['evidence']:
            label = QLabel(); label.setPixmap(QPixmap(str(resolve_evidence(root, evidence['file'])))); label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
            scroll = QScrollArea(); scroll.setWidget(label); self.tabs.addTab(scroll, titles[evidence['kind']]); self.kinds.append(evidence['kind'])
        self.tabs.currentChanged.connect(lambda i: self.seen.add(self.kinds[i]))
        if self.kinds: self.seen.add(self.kinds[0])
        side = QScrollArea(); side.setWidgetResizable(True); panel = QWidget(); form = QVBoxLayout(panel); side.setWidget(panel)
        self.reviewer = QLineEdit(); self.reviewer.setPlaceholderText('Người kiểm tra'); form.addWidget(self.reviewer)
        self.checks = {}
        for key, title in CHECKS.items():
            check = QCheckBox(title); note = QLineEdit(); note.setPlaceholderText('Nhận xét cụ thể sau khi xem ảnh')
            form.addWidget(check); form.addWidget(note); self.checks[key] = check, note
        form.addStretch(); splitter.addWidget(side); splitter.setSizes([900, 450])
        row = QHBoxLayout(); layout.addLayout(row)
        close = QPushButton('Đóng để sửa tiếp'); close.clicked.connect(self.reject); row.addWidget(close); row.addStretch()
        save = QPushButton('Ghi QC đạt cho nét hiện tại'); save.setObjectName('primary'); save.clicked.connect(self.finish); row.addWidget(save)

    def finish(self):
        required = {'full', 'face', 'hand_left', 'hand_right', 'thumbnail', 'comparison', 'reference_01', 'reference_02', 'reference_03'}
        if not required <= self.seen:
            QMessageBox.warning(self, 'Chưa xem đủ ảnh', 'Mở toàn hình, mặt, cả hai tay, cỡ nhỏ, bảng đối chiếu và ba ảnh chuẩn trước.'); return
        checks = {key:dict(pass_=check.isChecked(), note=note.text().strip()) for key, (check,note) in self.checks.items()}
        checks = {key:{'pass':value['pass_'], 'note':value['note']} for key,value in checks.items()}
        try: record_review(self.entry, self.root, checks, self.reviewer.text())
        except ValueError as exc: QMessageBox.warning(self, 'Chưa đạt QC', str(exc)); return
        self.accept()
