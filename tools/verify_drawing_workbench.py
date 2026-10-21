"""Reproducible app-owned screenshots and a portable workbench project."""
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from PySide6.QtWidgets import QApplication
from studio import drawing
from studio.drawing_workbench_sample import workbench_document
from studio.ui.drawing_dialog import DrawingDialog
from studio.ui.style import STYLE
from studio.project import new_project, save, load, missing
from studio.renderer import Renderer

root = Path(__file__).resolve().parents[1]
folder = root / 'projects' / 'drawing_workbench'; folder.mkdir(parents=True, exist_ok=True)
app = QApplication.instance() or QApplication([])
app.setStyle('Fusion'); app.setStyleSheet(STYLE)
doc = workbench_document()
drawing.save_drawing(doc, folder / 'workbench.drawing.json')
drawing.render(doc, 1600).save(str(folder / 'workbench.png'))
(folder / 'workbench.svg').write_text(drawing.svg(doc)[0], encoding='utf-8')
desk = DrawingDialog(doc, standalone=True); desk.resize(1440, 960); desk.show()
desk.tools.setCurrentIndex(desk.tools.findData('node')); desk.canvas.selected = {0}
desk.canvas.selection_changed.emit(0)
desk.editor_tabs.setCurrentIndex(3); app.processEvents()
desk.grab().save(str(folder / 'editor_nodes.png'))
desk.editor_tabs.setCurrentIndex(1); app.processEvents()
desk.grab().save(str(folder / 'editor_references.png'))
desk.canvas.index = 1; desk.canvas.reset_selection(); desk.refresh_layers()
desk.tools.setCurrentIndex(desk.tools.findData('guide')); desk.editor_tabs.setCurrentIndex(2)
app.processEvents(); desk.grab().save(str(folder / 'editor_guides.png'))
project = new_project(); project['scenes'][0].update(objects=drawing.scene_layers(doc, folder, 0, 6), background='white', duration=6)
save(project, folder / 'project.json', folder)
loaded = load(folder / 'project.json')
assert not missing(loaded, folder), missing(loaded, folder)
preview = Renderer().frame(loaded, folder, 0, 1280, 720, burn=False, effects=False)
preview.save(str(folder / 'timeline.png'))
report = dict(status='software_verified', character_master='none_approved',
              project=str(folder / 'project.json'), screenshots=['editor_nodes.png', 'editor_references.png', 'editor_guides.png'],
              missing_media=missing(loaded, folder), layers=len(loaded['scenes'][0]['objects']))
(folder / 'verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
desk.close()
print(json.dumps(report, ensure_ascii=False))
