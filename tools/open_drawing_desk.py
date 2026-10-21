"""Open the source prototype independently of the older packaged executable."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from PySide6.QtWidgets import QApplication
from studio.ui.drawing_dialog import DrawingDialog
from studio.ui.style import STYLE
from studio.drawing_workbench_sample import workbench_document

app = QApplication(sys.argv[:1]); app.setStyle('Fusion'); app.setStyleSheet(STYLE)
if '--studio' in sys.argv:
    from studio.ui.window import StudioWindow
    root = Path(__file__).resolve().parents[1]
    study = root / 'projects' / 'drawing_workbench' / 'project.json'
    window = StudioWindow(root, study if study.exists() else None)
    window.show()
    sys.exit(app.exec())
desk = DrawingDialog(workbench_document(), standalone=True)
desk.protect_unsaved = True
# Standalone desk exports files; insertion into a scene is available inside Studio.
desk.setWindowTitle('Bàn vẽ riêng của Studio · dựng hình và chỉnh nét')
desk.show()
sys.exit(app.exec())
