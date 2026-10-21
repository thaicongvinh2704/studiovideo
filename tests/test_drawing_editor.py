import copy
import json
import math
import tempfile
import unittest
from pathlib import Path

from PySide6.QtCore import Qt, QPoint, QPointF
from PySide6.QtGui import QWheelEvent
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication
from PySide6.QtSvg import QSvgRenderer

from studio import drawing as ink
from studio import drawing_edit as edit
from studio.ui.drawing_dialog import DrawingCanvas, DrawingDialog
from studio.drawing_workbench_sample import workbench_document
from studio.character_qc import drawing_issues

APP = QApplication.instance() or QApplication([])


def example():
    doc = ink.document(); entry = doc['layers'][0]; entry['role'] = 'object'
    entry['items'] = [ink.path_item('M100 100 C120 100 180 150 200 150 C220 150 280 100 300 100', width=4)]
    return doc


class EditingOperationsTests(unittest.TestCase):
    def test_knot_carries_both_handles_but_handle_edit_is_local(self):
        entry = example()['layers'][0]
        edit.move_node(entry, 0, 1, 5, [210, 160])
        self.assertEqual(entry['items'][0]['commands'][1], ['C', 120., 100., 190., 160., 210, 160])
        self.assertEqual(entry['items'][0]['commands'][2][1:3], [230, 160])
        edit.move_node(entry, 0, 1, 1, [125, 95])
        self.assertEqual(entry['items'][0]['commands'][1][-2:], [210, 160])

    def test_split_cubic_preserves_shape_and_guide_endpoint(self):
        entry = example()['layers'][0]
        g = edit.add_guide(entry, 'joint', [200, 150]); edit.bind_node(entry, 0, 1, 5, g)
        before = ink.painter_path(entry['items'][0])
        edit.split_segment(entry, 0, 1)
        after = ink.painter_path(entry['items'][0])
        # Compare at equal length, not parameter t (segment count changed).
        for i in range(21):
            a = before.pointAtPercent(before.percentAtLength(before.length() * i / 20))
            b = after.pointAtPercent(after.percentAtLength(after.length() * i / 20))
            self.assertLess(math.hypot(a.x() - b.x(), a.y() - b.y()), .2)
        self.assertEqual(entry['items'][0]['node_bindings'][0]['command'], 2)
        edit.validate_guides(entry)

    def test_shared_anchor_moves_connected_paths_together(self):
        entry = example()['layers'][0]
        entry['items'].append(ink.path_item('M200 150 C210 180 240 200 260 200'))
        g = edit.add_guide(entry, 'wrist', [200, 150])
        edit.bind_node(entry, 0, 1, 5, g); edit.bind_node(entry, 1, 0, 1, g)
        edit.move_node(entry, 0, 1, 5, [225, 175])
        self.assertEqual(entry['items'][0]['commands'][1][-2:], [225, 175])
        self.assertEqual(entry['items'][1]['commands'][0][1:], [225, 175])
        self.assertEqual(entry['items'][1]['commands'][1][1:3], [235, 205])

    def test_fixed_distance_and_subtree_carry_group(self):
        entry = example()['layers'][0]
        a = edit.add_guide(entry, 'parent', [0, 0])
        b = edit.add_guide(entry, 'joint', [100, 0], a, True)
        c = edit.add_guide(entry, 'tip', [120, 30], b)
        edit.bind_items(entry, [0], c)
        edit.move_guide(entry, b, [0, 200])
        self.assertAlmostEqual(math.dist(entry['guides'][0]['point'], entry['guides'][1]['point']), 100)
        self.assertEqual(entry['guides'][2]['point'], [20, 130])
        self.assertEqual(entry['items'][0]['commands'][0], ['M', 0, 200])

    def test_pressure_is_preserved_as_editable_source_and_svg_paths(self):
        stroke = edit.brush_item([[10, 20, .1], [40, 25, 1], [70, 20, .1]], '#252b2d', 10, .8, pressure=True)
        self.assertEqual(stroke['brush_source']['points'][1][2], 1)
        doc = ink.document(); doc['layers'][0]['items'] = [stroke]
        svg = ink.svg(doc)[0]
        self.assertIn('<path', svg); self.assertNotIn('<image', svg)
        self.assertTrue(QSvgRenderer(svg.encode()).isValid())
        original = copy.deepcopy(stroke['brush_source']['points'])
        edit.translate_item(stroke, 12, 7)
        self.assertEqual(stroke['brush_source']['points'][1], [original[1][0] + 12, original[1][1] + 7, 1])

    def test_restyle_rebuilds_pressure_outline_and_keeps_source(self):
        entry = ink.layer('Nét'); stroke = edit.brush_item([[0, 0, .5], [100, 0, .5]], '#111111', 4, pressure=True)
        entry['items'] = [stroke]; before = ink.item_bounds(stroke)
        source = copy.deepcopy(stroke['brush_source']['points'])
        edit.restyle_stroke(entry, 0, 12, .5, .5)
        self.assertGreater(ink.item_bounds(stroke).height(), before.height())
        self.assertEqual(stroke['brush_source']['points'], source)

    def test_convert_and_remove_nodes_keep_valid_binding_indices(self):
        entry = ink.layer('Test')
        entry['items'] = [ink.path_item('M0 0 L50 50 L100 0')]
        guide = edit.add_guide(entry, 'end', [100, 0]); edit.bind_node(entry, 0, 2, 1, guide)
        edit.curve_segment(entry, 0, 2)
        self.assertEqual(entry['items'][0]['node_bindings'][0]['argument'], 5)
        edit.remove_knot(entry, 0, 1)
        edit.validate_guides(entry)
        self.assertEqual(entry['items'][0]['node_bindings'][0]['command'], 1)

    def test_guides_and_sketch_are_absent_in_final_media(self):
        doc = example()
        g = edit.add_guide(doc['layers'][0], 'never_export_guide_label', [200, 150])
        sketch = ink.layer('Phác nhân vật'); sketch.update(draft=True, role='character')
        sketch['items'] = [ink.path_item('M600 600 L660 600', stroke='#ff0000')]
        doc['layers'].append(sketch)
        self.assertFalse(drawing_issues(doc, Path('.')))
        svg = ink.svg(doc)[0]
        self.assertNotIn('never_export', svg); self.assertNotIn('#ff0000', svg)
        self.assertEqual(ink.render(doc).pixelColor(620, 600).name(), '#ffffff')
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(len(ink.scene_layers(doc, Path(tmp))), 1)
        sketch['draft'] = False
        self.assertTrue(drawing_issues(doc, Path('.')))

    def test_invalid_guide_graph_and_binding_are_rejected(self):
        doc = example(); entry = doc['layers'][0]
        a = edit.add_guide(entry, 'a', [1, 1]); b = edit.add_guide(entry, 'b', [2, 2], a)
        entry['guides'][0]['parent'] = b
        with self.assertRaises(ValueError): ink.validate(doc)
        entry['guides'][0].pop('parent')
        entry['items'][0]['node_bindings'] = [dict(guide=a, command=99, argument=1)]
        with self.assertRaises(ValueError): ink.validate(doc)

    def test_atomic_commands_do_not_mutate_input_on_failure(self):
        doc = example(); before = copy.deepcopy(doc)
        with self.assertRaises(ValueError):
            edit.apply_command(doc, dict(op='move_node', item=0, command=1, argument=5, point=[float('inf'), 1]))
        self.assertEqual(doc, before)
        result = edit.apply_command(doc, dict(op='move_node', item=0, command=1, argument=5, point=[210, 150]))
        self.assertNotEqual(result, doc)

    def test_existing_review_is_invalidated_by_edit(self):
        entry = example()['layers'][0]
        entry['character_qc'] = dict(status='rejected_by_user')
        edit.move_node(entry, 0, 1, 5, [210, 160])
        # No mutation may create passed. Identity registry remains authoritative.
        self.assertNotEqual(entry['character_qc']['status'], 'passed')

    def test_save_open_preserves_bindings_and_pressure(self):
        doc = workbench_document()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'edit.drawing.json'; ink.save_drawing(doc, path)
            loaded = ink.validate(json.loads(path.read_text(encoding='utf-8')))
            self.assertEqual(loaded, doc)
            guide = loaded['layers'][0]['guides'][0]
            edit.move_guide(loaded['layers'][0], guide['id'], [300, 400])
            self.assertNotEqual(loaded, doc)


class EditorInteractionTests(unittest.TestCase):
    def setUp(self):
        self.canvas = DrawingCanvas(example()); self.canvas.resize(1000, 650)
        self.canvas.show(); APP.processEvents()

    def tearDown(self):
        self.canvas.close(); APP.processEvents()

    def screen(self, x, y):
        scale, ox, oy = self.canvas.mapping()
        return QPoint(round(ox + scale * x), round(oy + scale * y))

    def test_mouse_node_edit_and_undo_redo(self):
        c = self.canvas; before = copy.deepcopy(c.doc)
        c.set_tool('node'); c.selected = {0}
        QTest.mousePress(c, Qt.MouseButton.LeftButton, pos=self.screen(200, 150))
        QTest.mouseMove(c, self.screen(240, 180))
        QTest.mouseRelease(c, Qt.MouseButton.LeftButton, pos=self.screen(240, 180))
        actual = c.doc['layers'][0]['items'][0]['commands'][1][-2:]
        self.assertAlmostEqual(actual[0], 240, delta=1)
        changed = copy.deepcopy(c.doc); c.undo(); self.assertEqual(c.doc, before)
        c.redo(); self.assertEqual(c.doc, changed)

    def test_wheel_zoom_keeps_cursor_document_point(self):
        c = self.canvas; pos = QPointF(400, 300)
        event = QWheelEvent(pos, c.mapToGlobal(pos), QPoint(0, 0), QPoint(0, 120),
                            Qt.MouseButton.NoButton, Qt.KeyboardModifier.NoModifier, Qt.ScrollPhase.NoScrollPhase, False)
        before = c.point(event); c.wheelEvent(event); after = c.point(event)
        self.assertAlmostEqual(before.x(), after.x()); self.assertAlmostEqual(before.y(), after.y())
        self.assertGreater(c.zoom, 1)

    def test_bezier_tool_creates_editable_curve(self):
        c = self.canvas; c.set_tool('bezier')
        for point in ((400, 300), (440, 250), (480, 350), (520, 300)):
            QTest.mouseClick(c, Qt.MouseButton.LeftButton, pos=self.screen(*point))
        QTest.keyClick(c, Qt.Key.Key_Return)
        self.assertEqual(c.entry['items'][-1]['commands'][1][0], 'C')
        self.assertEqual(len(c.entry['items']), 2)

    def test_locked_layer_cannot_be_drawn_on(self):
        c = self.canvas; c.entry['locked'] = True; before = copy.deepcopy(c.doc)
        for tool in ('pen', 'brush', 'node', 'guide', 'erase'):
            c.set_tool(tool)
            QTest.mouseClick(c, Qt.MouseButton.LeftButton, pos=self.screen(200, 150))
        self.assertEqual(c.doc, before)

    def test_new_desk_can_show_all_panels_without_rejected_sample(self):
        desk = DrawingDialog(workbench_document(), standalone=True); desk.show(); APP.processEvents()
        for i in range(desk.editor_tabs.count()):
            desk.editor_tabs.setCurrentIndex(i); APP.processEvents()
        self.assertEqual(desk.editor_tabs.count(), 4)
        self.assertTrue(all(e.get('role') == 'object' for e in desk.canvas.doc['layers']))
        desk.close()

    def test_unsaved_close_can_be_cancelled_without_losing_work(self):
        from unittest.mock import patch
        from PySide6.QtWidgets import QMessageBox
        desk = DrawingDialog(example(), standalone=True); desk.protect_unsaved = True
        desk.canvas.entry['items'][0]['commands'][0][1] = 120
        before = copy.deepcopy(desk.canvas.doc)
        with patch.object(QMessageBox, 'question', return_value=QMessageBox.StandardButton.Cancel) as ask:
            desk.reject()
        ask.assert_called_once(); self.assertEqual(desk.canvas.doc, before)
        desk.protect_unsaved = False; desk.close()


if __name__ == '__main__': unittest.main()
