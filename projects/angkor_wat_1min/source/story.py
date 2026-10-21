"""Original one-minute script; subtitles and pronunciation hints are separate."""
from pathlib import Path
DEST = Path(__file__).resolve().parents[1]
ROOT = DEST.parents[1]
STORY = [
    dict(name='Một vũ trụ trong ngôi đền', text='Nhìn năm ngọn tháp này, anh em thấy một ngôi đền. Nhưng người Khmer xưa lại đặt cả một vũ trụ vào đó. Không chỉ là chuyện xây cho to hay trang trí cho đẹp.'),
    dict(name='Campuchia · thế kỷ XII', text='Đây là Angkor Wat, ở Campuchia, được xây vào đầu thế kỷ mười hai, dưới thời vua Suryavarman đệ nhị. Nó thuộc quần thể kinh đô của đế chế Khmer.', spoken='Đây là Ăng co Vát, ở Cam pu chia, được xây vào đầu thế kỷ mười hai, dưới thời vua Su ri a va man đệ nhị. Nó thuộc quần thể kinh đô của đế chế Khơ me.'),
    dict(name='Đền thờ Vishnu', text='Ban đầu, đền thờ thần Vishnu của Ấn Độ giáo. Hình khắc trên tường còn kể lại những câu chuyện thần thoại. Và năm tháp không chỉ để nhìn cho oai.', spoken='Ban đầu, đền thờ thần Vi snu của Ấn Độ giáo. Hình khắc trên tường còn kể lại những câu chuyện thần thoại. Và năm tháp không chỉ để nhìn cho oai.'),
    dict(name='Năm tháp · năm đỉnh núi', text='Chúng tượng trưng cho năm đỉnh núi Meru, ngọn núi thiêng trong quan niệm về vũ trụ. Hãy nhìn từ trên xuống: một tháp ở giữa, bốn tháp ở bốn góc.', spoken='Chúng tượng trưng cho năm đỉnh núi Mê ru, ngọn núi thiêng trong quan niệm về vũ trụ. Hãy nhìn từ trên xuống: một tháp ở giữa, bốn tháp ở bốn góc.'),
    dict(name='Hào nước là đại dương', text='Còn hào nước bao quanh? Đó là hình ảnh đại dương. Bước qua hào, anh em đang tiến vào một thế giới thiêng được dựng bằng đá.'),
    dict(name='Những lớp lịch sử', text='Về sau, nơi này trở thành chốn thờ Phật. Sự thay đổi ấy vẫn để lại dấu vết ngay bên trong đền. Một công trình, nhưng mang nhiều lớp lịch sử.'),
    dict(name='Có thực sự bị quên lãng?', text='Và đừng tưởng ngôi đền từng bị quên lãng hoàn toàn. Người địa phương và các nhà sư vẫn biết đến, vẫn lui tới nơi này.'),
    dict(name='Đọc một ngôi đền', text='Lần tới nhìn năm ngọn tháp, hãy thử đọc chúng như một bản đồ vũ trụ. Hào nước, tầng nền, ngọn tháp: mỗi phần là một dấu gợi ý. Ngôi đền kể nhiều hơn mình tưởng.'),
]
SOURCES = [
    dict(title='APSARA National Authority — Angkor Wat', url='https://apsaraauthority.gov.kh/2021/06/14/angkor-wat/', claims='Suryavarman II; original Vishnu dedication; later Buddhist pilgrimage.'),
    dict(title='NASA Earth Observatory — Angkor Wat', url='https://science.nasa.gov/earth/earth-observatory/angkor-wat-5112/', claims='Five towers symbolize peaks of Mount Meru; moat symbolizes cosmic ocean.'),
    dict(title='Carter et al., PNAS (2019), Temple occupation and the tempo of collapse at Angkor Wat', url='https://doi.org/10.1073/pnas.1821879116', claims='Angkor Wat was never completely abandoned; continuing religious importance.'),
]
if __name__ == '__main__':
    import json
    (DEST/'kich_ban.txt').write_text('\n\n'.join(row['text'] for row in STORY), encoding='utf-8')
    (DEST/'sources.json').write_text(json.dumps(SOURCES, ensure_ascii=False, indent=2), encoding='utf-8')
    print('Script:',sum(len(row['text'].split()) for row in STORY),'space-separated Vietnamese syllables/words')
