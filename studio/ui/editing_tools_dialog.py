"""Small optional-tool bridge; never changes the open film automatically."""
import json
from pathlib import Path
import subprocess
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget,
                               QLabel, QPushButton, QLineEdit, QPlainTextEdit, QFileDialog,
                               QFormLayout, QMessageBox)
from .. import editing_tools as helpers
from .workers import Worker


class EditingToolsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Hỗ trợ dựng · Công cụ local')
        self.resize(820, 650)
        self.worker = None
        layout = QVBoxLayout(self)
        note = QLabel('Kết quả được lưu riêng để duyệt; không tự sửa phim, đổi giọng hoặc duyệt QC.')
        note.setWordWrap(True)
        layout.addWidget(note)
        tabs = QTabWidget()
        layout.addWidget(tabs)
        self.run_buttons = []

        status = QWidget()
        sl = QVBoxLayout(status)
        self.add_button(sl, 'Kiểm tra bộ công cụ', lambda: self.run(helpers.doctor))
        sl.addWidget(QLabel('WhisperX · căn lời\nGlaxnimate · chuyển động vector\nQwen3-VL 2B · nhận xét khung hình'))
        sl.addStretch()
        tabs.addTab(status, 'Trạng thái')

        vector = QWidget()
        vl = QVBoxLayout(vector)
        vl.addWidget(QLabel('Mở Glaxnimate để sửa chuyển động vector. Xuất SVG/PNG để đưa lại vào Studio.\n'
                            'Chưa có bộ nhập trực tiếp toàn bộ hoạt hình Lottie vào timeline Studio.'))
        self.add_button(vl, 'Mở Glaxnimate', self.open_glax)
        self.add_button(vl, 'Mở tệp vector…', lambda: self.open_glax(True))
        vl.addStretch()
        tabs.addTab(vector, 'Vector')

        align = QWidget()
        al = QFormLayout(align)
        self.audio = self.path_row(al, 'Audio gốc', 'Audio (*.wav *.mp3 *.m4a *.flac)')
        self.srt = self.path_row(al, 'SRT khớp audio', 'Phụ đề (*.srt)')
        self.align_out = self.path_row(al, 'Thư mục lưu mới', directory=True)
        self.add_button(al, 'Căn lời tiếng Việt', self.align)
        al.addRow(QLabel('Giữ nguyên lời và âm thanh. Mốc phải tính từ đầu audio, không gồm intro video.\n'
                          'Kết quả là đề xuất thời gian; cần nghe lại và kiểm tra các từ thiếu mốc.'))
        tabs.addTab(align, 'Căn lời')

        review = QWidget()
        rl = QFormLayout(review)
        self.frame = self.path_row(rl, 'Khung hình', 'Ảnh (*.png *.jpg *.jpeg *.webp)')
        self.narration = QPlainTextEdit()
        self.narration.setPlaceholderText('Lời đọc tương ứng với khung hình')
        self.narration.setMaximumHeight(80)
        rl.addRow('Lời kể', self.narration)
        self.expected = QPlainTextEdit()
        self.expected.setPlaceholderText('Những chi tiết bắt buộc phải thấy, hành động và quan hệ giữa các nhân vật')
        self.expected.setMaximumHeight(80)
        rl.addRow('Yêu cầu cảnh', self.expected)
        self.review_out = self.path_row(rl, 'Lưu nhận xét JSON', 'JSON (*.json)', save=True)
        self.add_button(rl, 'Đối chiếu khung hình', self.review)
        tabs.addTab(review, 'Kiểm tra hình')
        self.output = QPlainTextEdit()
        self.output.setReadOnly(True)
        self.output.setPlaceholderText('Kết quả / lỗi được hiển thị tại đây.')
        layout.addWidget(self.output, 1)

    def add_button(self, layout, title, callback):
        button = QPushButton(title)
        button.clicked.connect(callback)
        self.run_buttons.append(button)
        if isinstance(layout, QFormLayout):
            layout.addRow(button)
        else:
            layout.addWidget(button)

    def path_row(self, layout, title, filter='', directory=False, save=False):
        widget = QWidget()
        row = QHBoxLayout(widget)
        row.setContentsMargins(0, 0, 0, 0)
        edit = QLineEdit()
        browse = QPushButton('Chọn…')
        def choose():
            if directory:
                path = QFileDialog.getExistingDirectory(self, title)
            elif save:
                path, _ = QFileDialog.getSaveFileName(self, title, '', filter)
            else:
                path, _ = QFileDialog.getOpenFileName(self, title, '', filter)
            if path:
                edit.setText(path)
        browse.clicked.connect(choose)
        row.addWidget(edit)
        row.addWidget(browse)
        layout.addRow(title, widget)
        return edit

    def run(self, function):
        if self.worker and self.worker.isRunning():
            return
        self.output.setPlainText('Đang xử lý bằng công cụ local…')
        for button in self.run_buttons:
            button.setEnabled(False)
        self.worker = Worker(lambda worker: function(), self)
        self.worker.done.connect(lambda result: self.output.setPlainText(
            result if isinstance(result, str) else json.dumps(result, ensure_ascii=False, indent=2)))
        self.worker.failed.connect(lambda message: self.output.setPlainText('Chưa hoàn tất: ' + message))
        self.worker.finished.connect(lambda: [button.setEnabled(True) for button in self.run_buttons])
        self.worker.start()

    def open_glax(self, choose=False):
        try:
            file = None
            if choose:
                file, _ = QFileDialog.getOpenFileName(self, 'Mở vector', '', 'Vector (*.rawr *.json *.svg)')
                if not file:
                    return
            helpers.open_vector_editor(file)
        except Exception as exc:
            self.output.setPlainText(str(exc))

    def align(self):
        audio, srt, output = self.audio.text(), self.srt.text(), self.align_out.text()
        if not all((audio, srt, output)):
            self.output.setPlainText('Chọn đủ audio, SRT và thư mục đầu ra.')
            return
        def work():
            result = subprocess.run(helpers.align_command(audio, srt, output),
                                    capture_output=True, text=True, encoding='utf-8', errors='replace',
                                    env=helpers.environment(), creationflags=helpers.NO_WINDOW, timeout=7200)
            if result.returncode:
                raise RuntimeError(result.stderr[-4000:] or result.stdout[-4000:])
            return result.stdout[-5000:]
        self.run(work)

    def review(self):
        image, narration = self.frame.text(), self.narration.toPlainText().strip()
        expected, output = self.expected.toPlainText().strip(), self.review_out.text()
        if not all((image, narration, expected, output)):
            self.output.setPlainText('Chọn khung hình, nhập lời kể, yêu cầu cảnh và tệp lưu mới.')
            return
        def work():
            path = Path(output)
            if path.exists():
                raise ValueError('Chọn tên tệp mới để giữ nhận xét cũ.')
            result = helpers.review_frame(image, narration, expected)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
            return result
        self.run(work)

    def reject(self):
        if self.worker and self.worker.isRunning():
            QMessageBox.information(self, 'Đang xử lý', 'Chờ công cụ chạy xong trước khi đóng cửa sổ này.')
            return
        super().reject()

    def closeEvent(self, event):
        if self.worker and self.worker.isRunning():
            event.ignore()
        else:
            super().closeEvent(event)
