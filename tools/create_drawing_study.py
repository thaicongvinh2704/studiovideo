"""Rebuild the review assets from original path data and a credited real photograph."""
import copy
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from PySide6.QtWidgets import QApplication
from studio import drawing
from studio.drawing_samples import sample_document, person
from studio.explainer import image_item, item
from studio.project import new_project, new_scene, save
from studio.renderer import Renderer

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'projects' / 'drawing_desk_study'


def make():
    app = QApplication.instance() or QApplication([])
    OUT.mkdir(parents=True, exist_ok=True)
    doc = sample_document()
    drawing.save_drawing(doc, OUT / 'net_moc.drawing.json')
    drawing.render(doc, 1600).save(str(OUT / '01_vector_study.png'))
    (OUT / 'net_moc.svg').write_text(drawing.svg(doc)[0], encoding='utf-8')
    project = new_project('Bàn vẽ riêng · nhân vật theo chuẩn và QC', 5)
    project['fps'] = 24
    project['subtitle_style']['enabled'] = False
    first = project['scenes'][0]
    first.update(background='white', name='Hình vẽ · nhân vật tĩnh', objects=drawing.scene_layers(doc, OUT, 0, 5))
    # Demonstrate direction on selected props without adding motion to the person.
    brick = next(o for o in first['objects'] if o['name'].startswith('Viên gạch'))
    y = brick['y']
    brick['keys'] = dict(y=[dict(t=.5, v=y), dict(t=1.15, v=y+126, ease='ease_in'),
                            dict(t=1.3, v=y+118, ease='ease_out'), dict(t=1.5, v=y+126, ease='ease_in')])
    water_layer = next(e for e in doc['layers'] if e['name'].startswith('Đường nước'))
    first['objects'] = [o for o in first['objects'] if not o['name'].startswith('Đường nước')]
    for i, entry in enumerate(water_layer['items']):
        path = drawing.painter_path(entry)
        count = max(8, round(path.length()/3))
        points = [[path.pointAtPercent(j/count).x(), path.pointAtPercent(j/count).y()] for j in range(count+1)]
        bounds = drawing.item_bounds(entry)
        center = bounds.center()
        first['objects'].append(item('shape', ['Mặt nước', 'Tuyến nước', 'Đầu mũi tên'][i], center.x(), center.y(), bounds.width(), bounds.height(),
            shape='path', points=[[x-center.x(), y-center.y()] for x,y in points], color=entry['stroke'], fill='none',
            stroke=entry['width'], reveal=i>0, start=[0,1.5,3.8][i], end=5, enter_duration=[1,2.3,.25][i], layer=40+i))
    photo = OUT / 'assets' / 'angkor_wat_david_wilmot.jpg'
    if photo.exists():
        second = new_scene('Hình vẽ + ảnh chụp thật', 5); second.update(start=5, background='white')
        mixed_doc = drawing.document(); mixed_doc['layers'] = [person()]
        labels = drawing.layer('Chữ và chú giải')
        for text, at, size, color, bold in [
            ('Từ ảnh thật đến lời giải thích', [416, 110], 34, drawing.INK, True),
            ('CHUẨN THAM CHIẾU  /  NHÂN VẬT 02', [80, 77], 15, '#40827e', True),
            ('Angkor Wat · ảnh chụp thực tế', [475, 603], 22, drawing.INK, False),
            ('Ảnh: David Wilmot · Wikimedia Commons · CC BY 2.0', [475, 636], 16, '#727870', False)]:
            labels['items'].append(dict(kind='text', text=text, at=at, size=size, stroke=color, bold=bold))
        mixed_doc['layers'].append(labels)
        second['objects'] = drawing.scene_layers(mixed_doc, OUT, 0, 5)
        image = image_item(photo.relative_to(OUT).as_posix(), 800, 355, 650, 440)
        image.update(name='Ảnh chụp Angkor Wat · David Wilmot', layer=10, start=0, end=5,
                     attribution=dict(author='David Wilmot', license='CC BY 2.0',
                         source='https://commons.wikimedia.org/wiki/File:Angkor_Wat_reflection.jpg',
                         license_url='https://creativecommons.org/licenses/by/2.0/', changes='Scaled to fit, no image generation'))
        second['objects'].append(image)
        annotation = item('shape', 'Khoanh vùng mặt nước', 800, 355, 650, 440, shape='path',
            points=[[-245,145],[-151,148],[-30,151],[91,147],[180,142]],
            color='#326dc9', stroke=4, start=.7, end=5, reveal=True, enter_duration=1.3, layer=40)
        second['objects'].append(annotation)
        project['scenes'].append(second)
        metadata = image['attribution']
        (OUT / 'PHOTO_CREDIT.json').write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding='utf-8')
        Renderer().frame(project, OUT, 8, 1600, 900, burn=False).save(str(OUT / '02_drawing_and_real_photo.png'))
    saved = save(project, OUT / 'project.json', OUT)
    from studio.ui.drawing_dialog import DrawingDialog
    from studio.ui.style import STYLE
    app.setStyle('Fusion'); app.setStyleSheet(STYLE)
    desk = DrawingDialog(doc); desk.resize(1400, 900); desk.show(); app.processEvents()
    desk.grab().save(str(OUT / '03_drawing_desk.png')); desk.close()
    print(json.dumps(dict(layers=len(doc['layers']), paths=sum(len(e['items']) for e in doc['layers']), scenes=len(saved['scenes']), output=str(OUT))))
    return saved


if __name__ == '__main__':
    project = make()
    if '--video' in sys.argv:
        from studio.exporter import export_video
        export_video(project, OUT, OUT / 'drawing_demo_10s.mp4', 1280, 720, 24)
        print('Video exported')
