import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from studio.reference_voice import load_profile
from studio.tts import VoiceEngine


class ReferenceVoiceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.profile = self.root / 'sample.voice.json'
        self.data = dict(version=1, engine='vieneu-v3turbo', name='Giọng mẫu',
                         preferred=True, status='audition_pending_user_review')
        for key in ('reference', 'codes'):
            asset = self.root / (key + '.bin')
            asset.write_bytes(key.encode())
            self.data[key] = asset.name
            self.data[key + '_sha256'] = hashlib.sha256(asset.read_bytes()).hexdigest()
        self.save()

    def save(self):
        self.profile.write_text(json.dumps(self.data), encoding='utf-8')

    def test_catalog_keeps_piper_and_marks_reference_as_audition(self):
        (self.root / 'old.onnx').write_bytes(b'model')
        (self.root / 'old.onnx.json').write_text('{}')
        voices = VoiceEngine(self.root).voices()
        self.assertEqual(voices[0], ('Giọng mẫu · Bản thử', str(self.profile)))
        self.assertIn(('old', str(self.root / 'old.onnx')), voices)

    def test_changed_reference_is_rejected_before_loading_any_tts(self):
        (self.root / self.data['reference']).write_bytes(b'changed')
        with patch('studio.reference_voice.ReferenceSynthesizer') as backend:
            with self.assertRaisesRegex(ValueError, 'đã thay đổi'):
                VoiceEngine(self.root).synthesize('Xin chào', str(self.profile), self.root / 'out.wav')
            backend.assert_not_called()
        self.assertFalse((self.root / 'out.wav').exists())

    def test_missing_codes_are_not_listed(self):
        (self.root / self.data['codes']).unlink()
        self.assertNotIn(str(self.profile), [p for _, p in VoiceEngine(self.root).voices()])

    def test_outside_asset_path_is_rejected(self):
        self.data['reference'] = '../outside.wav'
        self.save()
        with self.assertRaisesRegex(ValueError, 'ngoài thư mục'):
            load_profile(self.profile)

    def test_unknown_engine_cannot_be_treated_as_piper(self):
        self.data['engine'] = 'unknown'
        self.save()
        with self.assertRaisesRegex(ValueError, 'không được hỗ trợ'):
            VoiceEngine(self.root).synthesize('Xin chào', str(self.profile), self.root / 'out.wav')

    def test_invalid_selected_tone_is_rejected_before_synthesis(self):
        self.data['postprocess'] = dict(pitch_semitones=float('nan'), tempo=1.035)
        self.save()
        with patch('studio.reference_voice.ReferenceSynthesizer') as backend:
            with self.assertRaisesRegex(ValueError, 'Cao độ'):
                VoiceEngine(self.root).synthesize('Xin chào', str(self.profile), self.root / 'out.wav')
            backend.assert_not_called()


if __name__ == '__main__':
    unittest.main()
