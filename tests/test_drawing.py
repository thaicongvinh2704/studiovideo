import copy
import json
import tempfile
import unittest
from pathlib import Path

from PySide6.QtCore import Qt, QPoint
from PySide6.QtWidgets import QApplication
from PySide6.QtTest import QTest
from PySide6.QtSvg import QSvgRenderer

from studio import drawing
from studio.drawing_samples import sample_document
from studio.project import new_project, save, load, missing
from studio.renderer import Renderer
from studio.ui.drawing_dialog import DrawingCanvas, DrawingDialog
from tests.character_fixture import MechanicalCharacterFixtureMixin

APP = QApplication.instance() or QApplication([])


class DrawingTests(MechanicalCharacterFixtureMixin, unittest.TestCase):
    def test_mouse_stroke_roundtrip_and_history(self):
        canvas = DrawingCanvas(drawing.document()); canvas.resize(900, 520); canvas.show()
        APP.processEvents()
        QTest.mousePress(canvas, Qt.MouseButton.LeftButton, pos=QPoint(100, 200))
        for pt in (QPoint(150, 210), QPoint(200, 240), QPoint(250, 235)):
            QTest.mouseMove(canvas, pt)
        QTest.mouseRelease(canvas, Qt.MouseButton.LeftButton, pos=QPoint(280, 230))
        items = canvas.doc['layers'][0]['items']
        self.assertEqual(len(items), 1)
        self.assertGreaterEqual(len(items[0]['commands']), 3)
        before = copy.deepcopy(canvas.doc)
        canvas.undo(); self.assertFalse(canvas.doc['layers'][0]['items'])
        canvas.redo(); self.assertEqual(canvas.doc, before)
        with tempfile.TemporaryDirectory() as tmp:
            filename = Path(tmp) / 'test.drawing.json'
            drawing.save_drawing(canvas.doc, filename)
            self.assertEqual(drawing.validate(json.loads(filename.read_text(encoding='utf-8'))), before)
        canvas.close()

    def test_scene_export_preserves_composition_and_is_portable(self):
        doc = sample_document(); original = copy.deepcopy(doc)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); source = root / 'source'; target = root / 'portable'
            objects = drawing.scene_layers(doc, source, 0, 8)
            self.assertEqual(len(objects), 7)
            self.assertEqual(doc, original)
            for obj in objects:
                renderer = QSvgRenderer(str(source / obj['file']))
                self.assertTrue(renderer.isValid())
                self.assertAlmostEqual(renderer.viewBoxF().center().x(), obj['x'], places=4)
                self.assertAlmostEqual(renderer.viewBoxF().center().y(), obj['y'], places=4)
                self.assertNotIn('<image', (source / obj['file']).read_text(encoding='utf-8'))
            project = new_project(); project['scenes'][0].update(objects=objects, duration=8, background='white')
            saved = save(project, target / 'project.json', source)
            self.assertEqual(missing(saved, target), [])
            self.assertEqual(load(target / 'project.json'), saved)
            native = drawing.render(doc, 640)
            actual = Renderer().frame(saved, target, 2, 640, 360, burn=False, effects=False)
            # Native desk and portable timeline must place the same colored regions.
            for x, y in ((100, 180), (315, 255), (470, 185), (510, 245)):
                self.assertEqual(native.pixelColor(x, y), actual.pixelColor(x, y))

    def test_static_person_stays_identical_when_brick_moves(self):
        with tempfile.TemporaryDirectory() as tmp:
            objects = drawing.scene_layers(sample_document(), Path(tmp), 0, 8)
            person = objects[0]
            self.assertEqual(person['kind'], 'image')
            self.assertFalse(person['keys'])
            brick = next(o for o in objects if o['name'].startswith('Viên gạch'))
            brick['keys'] = dict(y=[dict(t=0, v=brick['y']), dict(t=3, v=brick['y'] + 170)])
            project = new_project(); project['scenes'][0].update(background='white', objects=objects)
            r = Renderer(); a = r.frame(project, tmp, .1, 640, 360, burn=False)
            b = r.frame(project, tmp, 3, 640, 360, burn=False)
            self.assertEqual(a.copy(60, 60, 90, 230), b.copy(60, 60, 90, 230))
            self.assertNotEqual(a, b)

    def test_layers_visibility_order_and_undo(self):
        dialog = DrawingDialog(sample_document()); before = copy.deepcopy(dialog.canvas.doc)
        dialog.canvas.index = 0; dialog.reorder(1)
        self.assertEqual(dialog.canvas.doc['layers'][1]['id'], before['layers'][0]['id'])
        dialog.canvas.undo(); self.assertEqual(dialog.canvas.doc, before)
        first = dialog.layers.item(0); first.setCheckState(Qt.CheckState.Unchecked)
        self.assertFalse(dialog.canvas.doc['layers'][-1]['visible'])
        dialog.canvas.undo(); self.assertEqual(dialog.canvas.doc, before)
        dialog.close()

    def test_reject_invalid_or_nonfinite_paths(self):
        doc = drawing.document(); doc['layers'][0]['items'] = [drawing.path_item('M1 2 L3 4')]
        doc['layers'][0]['items'][0]['commands'][1][1] = float('nan')
        with self.assertRaises(ValueError): drawing.validate(doc)

    def test_studio_insert_edit_and_project_history(self):
        from unittest.mock import patch
        from studio.ui.window import StudioWindow
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); project = new_project(); project['scenes'][0]['objects'] = []
            save(project, root / 'project.json', root)
            window = StudioWindow(root, root / 'project.json')
            def insert(dialog):
                dialog.result_doc = sample_document(); return 1
            with patch.object(DrawingDialog, 'exec', insert): window.drawing_desk()
            self.assertEqual(len(window.current_scene()['objects']), 7)
            obj = window.current_scene()['objects'][0]; window.selected_id = obj['id']
            obj.update(rotation=15, scale=.8, start=.5, end=7, keys={'opacity':[dict(t=0, v=.3), dict(t=1, v=1)]})
            original = copy.deepcopy(obj)
            def edit(dialog):
                dialog.result_doc = copy.deepcopy(dialog.canvas.doc)
                dialog.result_doc['layers'][0]['name'] = 'Nhân vật đã đổi tên; nét đã QC giữ nguyên'
                return 1
            with patch.object(DrawingDialog, 'exec', edit): window.graphic_dialog()
            for key in ('id', 'x', 'y', 'rotation', 'scale', 'start', 'end', 'keys'):
                self.assertEqual(obj[key], original[key])
            self.assertNotEqual(obj['file'], original['file'])
            window.undo()
            self.assertEqual(window.current_scene()['objects'][0]['file'], original['file'])
            window.dirty = False; window.close(); APP.processEvents()


if __name__ == '__main__': unittest.main()
