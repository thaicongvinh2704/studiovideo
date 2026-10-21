import copy
import json
import tempfile
import unittest
from pathlib import Path

from PySide6.QtWidgets import QApplication
from studio import drawing
from studio.character_art import authored_person
from tests.character_fixture import MechanicalCharacterFixtureMixin, mechanical_character_fixture as reviewed_person
from studio.character_qc import (geometry_issues, review_issues, prepare_packet, record_review,
    source_hash, project_issues, drawing_issues, ROOT)
from studio.project import new_project, save, load, missing, pack, unpack
from studio.exporter import export_video, export_cached
from studio.drawing_samples import rejected_person_v1

APP = QApplication.instance() or QApplication([])


class CharacterQCTests(MechanicalCharacterFixtureMixin, unittest.TestCase):
    def doc(self):
        doc = drawing.document(); doc['layers'] = [reviewed_person()]; return doc

    def project(self, root):
        project = new_project(); project['scenes'][0].update(background='white', objects=drawing.scene_layers(self.doc(),root))
        return project

    def test_historical_fixture_tests_mechanics_not_design_quality(self):
        entry = reviewed_person()
        self.assertEqual(geometry_issues(entry), [])
        self.assertEqual(review_issues(entry, ROOT), [])
        self.assertEqual(entry['character_qc']['source_sha256'], source_hash(authored_person()))

    def test_new_or_rejected_character_cannot_enter_scene(self):
        with tempfile.TemporaryDirectory() as tmp:
            for entry in (authored_person(), rejected_person_v1()):
                doc = drawing.document(); doc['layers'] = [entry]
                with self.assertRaisesRegex(ValueError, 'QC'): drawing.scene_layers(doc, tmp)
                # Draft data may still be saved for correction.
                drawing.save_drawing(doc, Path(tmp)/'draft.drawing.json')

    def test_hand_edit_invalidates_review_even_with_old_receipt(self):
        entry = reviewed_person()
        hand = next(i for i in entry['items'] if 'hand_left' in i.get('parts', []))
        hand['commands'][0][1] += 2
        self.assertTrue(any('đổi sau QC' in message for message in review_issues(entry, ROOT)))

    def test_missing_hand_or_false_occlusion_does_not_pass(self):
        entry = reviewed_person(); entry['items'] = [i for i in entry['items'] if 'hand_right' not in i.get('parts', [])]
        entry['character']['occlusions'] = dict(hand_right={'reason':'hidden','occluder':'imaginary-object'})
        self.assertTrue(any('hand_right' in message for message in geometry_issues(entry)))

    def test_manual_fail_never_restores_an_old_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            entry = reviewed_person(); prepare_packet(entry, tmp)
            checks = copy.deepcopy(entry['character_qc']['checks'])
            checks['left_hand'] = {'pass':False,'note':'Quan sát lại thấy lỗi bàn tay cần sửa, không được dùng bản này.'}
            with self.assertRaises(ValueError): record_review(entry,tmp,checks,'Test reviewer')
            self.assertEqual(entry['character_qc']['status'], 'failed')
            self.assertTrue(review_issues(entry,tmp))

    def test_svg_tampering_blocked_even_allow_draft_and_cached_export(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); project = self.project(root); obj = project['scenes'][0]['objects'][0]
            self.assertEqual(project_issues(project,root), [])
            path = root / obj['file']; path.write_text(path.read_text(encoding='utf-8').replace('#ffdeb6','#ff0000'),encoding='utf-8')
            project['allow_draft'] = True
            self.assertTrue(any('SVG' in p['message'] for p in project_issues(project,root)))
            for exporter in (export_video,export_cached):
                with self.assertRaisesRegex(ValueError,'QC'): exporter(project,root,root/'blocked.mp4',320,180,12)
            self.assertFalse((root/'blocked.mp4').exists())

    def test_qc_evidence_survives_save_as_and_portable_zip(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); project = self.project(root/'source')
            saved = save(project,root/'saved'/'project.json',root/'source')
            self.assertEqual(missing(saved,root/'saved'), [])
            self.assertEqual(project_issues(saved,root/'saved'), [])
            pack(saved,root/'saved',root/'portable.zip'); path = unpack(root/'portable.zip',root/'unpacked')
            opened = load(path)
            self.assertEqual(missing(opened,path.parent), [])
            self.assertEqual(project_issues(opened,path.parent), [])
            proof = opened['scenes'][0]['objects'][0]['drawing_doc']['layers'][0]['character_qc']['evidence'][0]
            (path.parent/proof['file']).write_bytes(b'tampered')
            self.assertTrue(project_issues(opened,path.parent))

    def test_legacy_presenter_is_not_silently_exempt_from_qc(self):
        project = new_project(); project['allow_draft'] = True
        with tempfile.TemporaryDirectory() as tmp:
            self.assertTrue(project_issues(project,tmp))
            with self.assertRaisesRegex(ValueError,'QC'): export_video(project,tmp,Path(tmp)/'legacy.mp4',320,180,12)

    def test_object_art_does_not_require_character_review(self):
        doc = drawing.document(); doc['layers'][0].update(role='object',items=[drawing.path_item('M20 20 L90 20 L90 90 L20 90 Z','#d58b62')])
        self.assertEqual(drawing_issues(doc,ROOT), [])
        with tempfile.TemporaryDirectory() as tmp: self.assertEqual(len(drawing.scene_layers(doc,tmp)),1)

    def test_unclassified_hand_drawing_is_not_exported_as_an_object_by_default(self):
        doc = drawing.document(); doc['layers'][0]['items'] = [drawing.path_item('M20 20 L70 70')]
        self.assertTrue(drawing_issues(doc,ROOT))

    def test_drawing_dialog_does_not_accept_an_unreviewed_character(self):
        from unittest.mock import patch
        from studio.ui.drawing_dialog import DrawingDialog
        doc = self.doc(); doc['layers'][0].pop('character_qc')
        dialog = DrawingDialog(doc)
        with patch('studio.ui.drawing_dialog.QMessageBox.warning') as warning:
            dialog.accept_drawing()
        self.assertTrue(warning.called); self.assertIsNone(dialog.result_doc)
        dialog.close()

    def test_qc_dialog_requires_opening_all_actual_evidence_tabs(self):
        from unittest.mock import patch
        from studio.ui.character_qc_dialog import CharacterQCDialog
        with tempfile.TemporaryDirectory() as tmp:
            dialog = CharacterQCDialog(reviewed_person(),tmp)
            self.assertEqual(len(dialog.kinds),9)
            with patch('studio.ui.character_qc_dialog.QMessageBox.warning') as warning:
                dialog.finish()
            self.assertTrue(warning.called)
            self.assertEqual(dialog.result(),0)
            dialog.close()

    def test_presenter_button_inserts_reviewed_static_art(self):
        from studio.ui.window import StudioWindow
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); project = new_project(); project['scenes'][0]['objects'] = []
            save(project,root/'project.json',root)
            window = StudioWindow(root,root/'project.json'); window.add_graphic('presenter')
            objects = window.current_scene()['objects']
            self.assertEqual(len(objects),1); self.assertEqual(objects[0]['kind'],'image')
            self.assertFalse(objects[0]['keys']); self.assertEqual(project_issues(window.project,root),[])
            window.dirty = False; window.close(); APP.processEvents()


class UserRejectionTests(unittest.TestCase):
    def rejected(self):
        from studio.character_art import reviewed_person as actual_model
        return actual_model()

    def test_actual_model_is_revoked(self):
        entry = self.rejected()
        self.assertEqual(entry['character_qc']['status'], 'rejected_by_user')
        self.assertTrue(any('người dùng loại' in issue for issue in review_issues(entry,ROOT)))

    def test_copied_old_pass_cannot_bypass_user_rejection(self):
        entry = self.rejected(); entry['character_qc']['status'] = 'passed'
        doc = drawing.document(); doc['layers'] = [entry]
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError,'người dùng loại'): drawing.scene_layers(doc,tmp)
        # Small coordinate edits must not silently revive the same rejected design.
        entry['items'][0]['commands'][0][1] += 1
        self.assertTrue(any('người dùng loại' in issue for issue in review_issues(entry,ROOT)))

    def test_existing_project_and_allow_draft_cannot_export_rejected_design(self):
        project = load(ROOT/'projects/drawing_desk_study/project.json'); project['allow_draft'] = True
        with tempfile.TemporaryDirectory() as tmp:
            for exporter in (export_video,export_cached):
                with self.assertRaisesRegex(ValueError,'người dùng loại'):
                    exporter(project,ROOT/'projects/drawing_desk_study',Path(tmp)/'rejected.mp4',320,180,12)


if __name__ == '__main__': unittest.main()
