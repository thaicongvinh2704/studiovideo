import unittest
from pathlib import Path

from studio.voice_direction import read_package,compile_excerpt,pause_target,pause_padding_ms,space

PACKAGE=Path(__file__).resolve().parents[1]/'projects/mo_den_maya/voice_direction/input/Mo_Den_Maya_Dao_Dien_Giong_Viet'


class VoiceDirectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.direction=read_package(PACKAGE)

    def test_protected_number_range_is_one_inference_unit(self):
        plan=compile_excerpt(self.direction,105,110)
        phrase='bốn mươi mốt đến năm mươi tư phần trăm'
        self.assertEqual(sum(phrase in u['text'] for u in plan),1)
        self.assertTrue(any(106 in u['source_cue_ids'] and 107 in u['source_cue_ids'] for u in plan))

    def test_mid_protected_excerpt_is_rejected(self):
        with self.assertRaisesRegex(ValueError,'giữ liền'):
            compile_excerpt(self.direction,107,110)

    def test_event_at_beat_end_replaces_not_adds_pause(self):
        beat=next(b for b in self.direction['beats'] if b['id']=='beat_33')
        target=pause_target(beat,258,True)
        self.assertEqual(target['target_ms'],700)
        self.assertTrue(target['replaces_beat_pause'])

    def test_pause_only_tops_up_and_never_removes_natural_silence(self):
        self.assertEqual(pause_padding_ms(250,100,650),300)
        self.assertEqual(pause_padding_ms(500,300,650),0)

    def test_excerpts_are_only_spoken_text_without_duplicate_cues(self):
        by_id={c['id']:c for c in self.direction['source_cues']}
        for first,last in self.direction['ab_test']['excerpts_source_cues']:
            plan=compile_excerpt(self.direction,first,last)
            self.assertEqual(space(' '.join(u['text'] for u in plan)),space(' '.join(by_id[i]['text'] for i in range(first,last+1))))
            self.assertEqual([i for u in plan for i in u['source_cue_ids']],list(range(first,last+1)))
            self.assertTrue(all(u['text_origin']=='beats[].text' for u in plan))

    def test_all_36_beats_can_be_compiled_without_metadata_as_speech(self):
        for beat in self.direction['beats']:
            plan=compile_excerpt(self.direction,beat['source_cue_ids'][0],beat['source_cue_ids'][-1])
            self.assertEqual(space(' '.join(u['text'] for u in plan)),space(beat['text']))


if __name__=='__main__':unittest.main()
