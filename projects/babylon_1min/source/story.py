from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
DEST=Path(__file__).resolve().parents[1]
ANGKOR=ROOT/'projects'/'angkor_wat_1min'
STORY=[
 dict(name='Một ngọn đồi xanh giữa miền khô nóng',purpose='Reveal the imagined wonder, then open a question that is answered with appropriate uncertainty.',
      text='Một khu rừng mọc trên những tầng lầu, giữa miền đất khô nóng. Đó là hình dung nổi tiếng về Vườn treo Babylon. Nhưng khu vườn ấy thực sự ở đâu?'),
 dict(name='Treo nghĩa là gì?',purpose='Show trees rooted in elevated terraces rather than floating in the sky.',
      text='Theo những mô tả cổ, cây cối được trồng trên các tầng nền nâng cao, tạo cảm giác một ngọn đồi xanh. Chữ treo không có nghĩa là khu vườn lơ lửng giữa trời.'),
 dict(name='Bài toán nước',purpose='Trace a conceptual water path without claiming a specific unverified irrigation machine.',
      text='Nếu có một khu vườn như vậy, cây trên cao sẽ cần nước. Nước phải được đưa lên rồi phân phối đến các tầng. Cơ cấu cụ thể vẫn chưa được xác nhận.'),
 dict(name='Hình dung khác với chứng cứ',purpose='Cut from lush reconstruction to archaeological illustration and identify the evidentiary gap.',
      text='Vấn đề là tại Babylon, khảo cổ chưa tìm được bằng chứng thuyết phục cho công trình như lời kể. Một bức tranh phục dựng đẹp không thể thay thế dấu tích.'),
 dict(name='Đổi hướng tìm kiếm',purpose='Locate Babylon and Nineveh on a schematic map without presenting the alternative as settled fact.',
      text='Vì thế, có học giả đề xuất một hướng khác: Nineveh, ở phía bắc. Nơi đó từng có những khu vườn hoàng gia và hệ thống dẫn nước đồ sộ.'),
 dict(name='Giả thuyết nhầm tên',purpose='Show written accounts as material being interpreted, with the hypothesis clearly labelled.',
      text='Liệu người viết đời sau đã nhầm tên hai thành phố? Đó là một giả thuyết được nghiên cứu, chưa phải kết luận cuối cùng.'),
 dict(name='Trở lại kỳ quan',purpose='Return to the opening image with a distinction between imaginative reconstruction and historical certainty.',
      text='Sức hút của Vườn treo nằm ở cả hai điều: ý tưởng dựng một ngọn núi xanh bằng kỹ thuật, và bí ẩn về nơi nó từng tồn tại. Một kỳ quan vẫn đang được tìm lời giải.'),
]
SOURCES=[
 dict(title='British Museum — Paradise on earth: the gardens of Ashurbanipal',url='https://www.britishmuseum.org/blog/paradise-earth-gardens-ashurbanipal',supports='Raised gardens in classical accounts, royal gardens at Nineveh, alternative identification and lack of evidence at Babylon.'),
 dict(title='French Ministry of Culture — Nineveh',url='https://archeologie.culture.gouv.fr/en/nineveh',supports='Sennacherib gardens and water supply; possible confusion between Nineveh and Babylon.'),
 dict(title='Somerville College, Oxford — Stephanie Dalley',url='https://www.some.ox.ac.uk/our-people/stephanie-dalley/',supports='Nineveh identification is a scholarly proposal.'),
]
if __name__=='__main__':
 print(sum(len(row['text'].split()) for row in STORY))
