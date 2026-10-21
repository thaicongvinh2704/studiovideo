import json
import tempfile
import unittest
from pathlib import Path
from studio.project import new_project, new_object
from studio.character_qc import project_issues
from studio.supplied_character import LIBRARY


class SuppliedCatTests(unittest.TestCase):
    def project(self):
        p = new_project()
        entry = json.loads((LIBRARY/'manifest.json').read_text(encoding='utf-8'))['assets'][0]
        o = new_object('image', 'Mỏ Đen', 640, 390)
        o.update(role='character', character_library='mo_den', character_asset_id=entry['id'],
                 file=str(LIBRARY/entry['file']), width=400, height=400)
        p['scenes'][0]['objects'] = [o]
        return p

    def test_indexed_png_passes_without_human_anatomy_metadata(self):
        self.assertEqual(project_issues(self.project(), LIBRARY), [])

    def test_tampering_or_reclassifying_is_rejected(self):
        p = self.project(); o = p['scenes'][0]['objects'][0]
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[1]/'outputs') as tmp:
            path = Path(tmp)/'altered.png'; path.write_bytes(Path(o['file']).read_bytes()+b'changed')
            o['file'] = str(path); self.assertTrue(project_issues(p, LIBRARY))
        p = self.project(); p['scenes'][0]['objects'][0]['role'] = 'object'
        self.assertTrue(project_issues(p, LIBRARY))

    def test_camera_or_animation_cannot_cut_off_cat(self):
        p = self.project(); p['scenes'][0]['objects'][0]['keys'] = {'x':[{'t':0,'v':640},{'t':8,'v':10}]}
        self.assertTrue(project_issues(p, LIBRARY))

    def test_legacy_human_still_blocked(self):
        self.assertTrue(project_issues(new_project(), LIBRARY))
