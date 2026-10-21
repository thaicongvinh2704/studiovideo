import unittest
from studio.vietnamese_narration import apply_readings


class VietnameseReadingsTests(unittest.TestCase):
    def test_only_contextually_selected_occurrence_changes(self):
        original='Mã 12; cân nặng 12 kg.'
        start=original.index('12 kg')
        spoken,audit=apply_readings(original,[dict(start=start,end=start+5,expected='12 kg',
            spoken='mười hai ki lô gam',reason='Đây là khối lượng, không phải mã định danh.')])
        self.assertEqual(spoken,'Mã 12; cân nặng mười hai ki lô gam.')
        self.assertEqual(original,'Mã 12; cân nặng 12 kg.')
        self.assertEqual(audit[0]['original'],'12 kg')

    def test_stale_script_cannot_get_old_reading(self):
        with self.assertRaisesRegex(ValueError,'Bản gốc'):
            apply_readings('Ngày 22/10',[dict(start=5,end=10,expected='21/10',spoken='hai mươi mốt tháng mười',reason='Ngày.')])

    def test_overlapping_normalizations_are_rejected(self):
        entries=[dict(start=0,end=3,expected='2,5',spoken='hai phẩy năm',reason='Số thập phân.'),
                 dict(start=0,end=6,expected='2,5 km',spoken='hai phẩy năm ki lô mét',reason='Khoảng cách.')]
        with self.assertRaisesRegex(ValueError,'chồng lấn'):
            apply_readings('2,5 km',entries)

    def test_diacritics_and_commas_outside_edits_are_preserved(self):
        text='Má bảo Mã, mà Mã vẫn giữ bó mạ.'
        self.assertEqual(apply_readings(text,[]),(text,[]))


if __name__=='__main__':unittest.main()
