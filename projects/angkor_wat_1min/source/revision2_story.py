"""A single visual argument, without an on-screen presenter."""
from pathlib import Path

ORIGINAL = Path(__file__).resolve().parents[1]
DEST = ORIGINAL / 'revision2'
ROOT = ORIGINAL.parents[1]
STORY = [
    dict(name='Đặt lại câu hỏi', purpose='Establish the five towers as the mystery that the ending will resolve.',
         text='Nhìn năm ngọn tháp này, bạn thấy một ngôi đền. Nhưng người Khmer xưa còn đặt vào đây cả một cách hình dung vũ trụ. Muốn hiểu, hãy đổi góc nhìn.'),
    dict(name='Đổi góc nhìn', purpose='Give only the context needed for the Hindu symbolism, then move from elevation to plan.',
         text='Đây là Angkor Wat, ở Campuchia, được xây vào thế kỷ mười hai để thờ thần Vishnu. Thay vì nhìn mặt trước, ta sẽ nhìn ngôi đền từ trên xuống.'),
    dict(name='Nhận ra bố cục', purpose='Make the center and four corners legible before interpreting them.',
         text='Một tháp ở giữa, bốn tháp ở bốn góc. Đặt chúng cạnh hình ảnh núi Meru: năm vị trí ấy tương ứng với năm đỉnh của ngọn núi thiêng.'),
    dict(name='Tháp trở thành núi', purpose='Match the positions of architectural towers and symbolic peaks; explain the correspondence.',
         text='Trong quan niệm vũ trụ của Ấn Độ giáo, Meru nằm ở trung tâm thế giới. Những ngọn tháp vươn lên đã biến hình ảnh của núi thành một công trình bằng đá.'),
    dict(name='Lộ ra đại dương', purpose='Pull back from the inner sanctuary to reveal the enclosing moat and complete the cosmogram.',
         text='Giờ kéo góc nhìn ra xa. Hào nước bao quanh tượng trưng cho đại dương ở rìa vũ trụ. Nước và tháp là hai phần của cùng một ý tưởng.'),
    dict(name='Đi vào ý niệm', purpose='Move the viewpoint along the causeway so the viewer experiences the spatial relationship.',
         text='Con đường băng qua hào dẫn người đến đền, qua mặt nước rồi tiến về những tầng nền cao dần. Không gian được sắp đặt như hành trình tới ngọn núi thiêng.'),
    dict(name='Trả lời câu mở đầu', purpose='Return to the opening temple with its two symbolic correspondences now visible.',
         text='Bây giờ nhìn lại: năm tháp là năm đỉnh núi, hào nước là đại dương. Angkor Wat là một bản đồ vũ trụ được xây để con người có thể bước vào.'),
]
SOURCES = [dict(title='NASA Earth Observatory — Angkor Wat',
                url='https://science.nasa.gov/earth/earth-observatory/angkor-wat-5112/',
                supports='12th century, original Vishnu dedication, five towers / Meru, enclosing moat / cosmic ocean, causeway and rising terraces.')]

if __name__ == '__main__':
    print(sum(len(s['text'].split()) for s in STORY), 'Vietnamese space-separated syllables')
