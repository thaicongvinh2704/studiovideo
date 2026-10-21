"""A second static pose, reusing the existing Son Tinh vector master trial."""
import copy
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage,QPainter
from PySide6.QtWidgets import QApplication
from studio import drawing as ink
from studio import drawing_edit as edit
from studio.character_qc import prepare_packet

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'projects/son_tinh_vector_02_lifting'
LINE='#181b18';SKIN='#f6d5b7'


def main():
    app=QApplication.instance() or QApplication([]);OUT.mkdir(parents=True,exist_ok=True)
    source=json.loads((ROOT/'projects/son_tinh_vector_01/son_tinh.drawing.json').read_text(encoding='utf-8'))
    doc=copy.deepcopy(source);doc['width']=800;doc['layers']=doc['layers'][:1]
    e=doc['layers'][0];e['name']='Sơn Tinh · hai tay nâng đá'
    e['character']['identity']='son-tinh-simple-vector-02-lifting'
    removed={'Tay trái thả','Tay gọi núi','Nếp lòng bàn tay'}
    e['items']=[i for i in e['items'] if i.get('name') not in removed]
    kept=copy.deepcopy(e['items'])
    # Hands and elbows move, the face, hair and clothes retain original paths.
    e['character']['landmarks'].update(elbow_left=[287,571],elbow_right=[532,548],
                                      wrist_left=[311,576],wrist_right=[493,567])
    for g in e['guides']:
        if g['name'] in e['character']['landmarks']:g['point']=e['character']['landmarks'][g['name']][:]
    additions=[]
    def shape(name,d,fill='none',width=5.7,stroke=LINE,parts=()):
        item=ink.path_item(d,fill,stroke,width);item.update(name=name,parts=list(parts));additions.append(item)
        return item
    left=shape('Cánh tay trái đỡ đá','M279 545 C275 562 277 579 289 587 '
       'Q300 595 316 590 L338 581 L329 561 L307 570 Q302 572 302 565 L307 553 Z',SKIN,
       parts=('upper_arm_left','forearm_left'))
    right=shape('Cánh tay phải đỡ đá','M516 493 L541 530 Q552 546 542 560 '
       'Q529 578 505 581 L482 580 L482 558 L502 555 Q519 551 519 545 L490 519 Z',SKIN,
       parts=('upper_arm_right','forearm_right'))
    # Put forearms behind torso; sleeve borders cover the shoulder joins.
    e['items']=[left,right]+e['items']
    rock=shape('Tảng đá được nâng','M292 519 L320 485 L376 477 L417 485 L468 478 '
       'L510 504 L520 543 L494 563 L332 569 L287 550 Z','#979b8f',width=5.5,parts=('prop_rock',))
    rock_top=shape('Mặt sáng của đá','M292 519 L320 485 L376 477 L417 485 L468 478 '
       'L488 491 L454 509 L397 503 L353 519 L308 525 Z','#b7b9ab',width=1,stroke='none')
    seams=shape('Vết gãy trên đá','M354 519 L347 539 L358 550 M454 509 L465 531 '
       'M397 503 L406 518',width=2.8,stroke='#747a6e')
    e['items'].extend([rock,rock_top,seams])
    left_hand=shape('Bàn tay trái nâng đá','M308 571 L302 559 C298 551 300 541 304 537 '
       'C307 534 311 537 312 542 L316 553 L334 549 C339 548 342 552 338 555 '
       'L322 561 L341 559 C347 559 347 564 341 567 L324 570 '
       'L338 570 C344 570 344 575 338 577 L323 579 L334 580 '
       'C339 581 337 586 331 587 L316 587 Q310 584 308 579 Z',SKIN,width=4.4,
       parts=('hand_left','fingers_left'))
    right_hand=copy.deepcopy(left_hand)
    for c in right_hand['commands']:
        for i in range(1,len(c),2):c[i]=800-c[i]
    right_hand.update(name='Bàn tay phải nâng đá',parts=['hand_right','fingers_right'])
    e['items'].extend([left_hand,right_hand])
    e['character']['review_regions'].update(hand_left=[285,529,70,68],hand_right=[445,529,70,68])
    edit.invalidate(e);e['character_qc']=dict(status='pending',reason='Second simplified pose for visual review only.')
    ink.render(doc,1200).save(str(OUT/'preview.png'))
    image=QImage(1200,1200,QImage.Format.Format_ARGB32_Premultiplied);image.fill(Qt.GlobalColor.transparent)
    p=QPainter(image);p.setRenderHint(QPainter.RenderHint.Antialiasing);p.scale(1.5,1.5);ink.paint_layer(p,e);p.end()
    image.save(str(OUT/'preview_transparent.png'))
    prepare_packet(e,OUT);ink.save_drawing(doc,OUT/'son_tinh_lifting.drawing.json')
    # Verify reuse by exact serialized path/style equality, not a claim of beauty.
    reused=sum(any(item==old for old in kept) for item in e['items'])
    stats=dict(start_utc='2026-10-20T09:55:29Z',first_render_utc=datetime.now(timezone.utc).isoformat(),
        unchanged_reused_paths=reused,new_paths=len(e['items'])-reused,total_paths=len(e['items']),
        source='projects/son_tinh_vector_01/son_tinh.drawing.json',status='pending_visual_review')
    (OUT/'reuse_and_timing.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(stats,ensure_ascii=False))
    for item in e['qc_packet']['evidence']:
        if item['kind'] in ('face','hand_left','hand_right','thumbnail','comparison'):
            print(item['kind'],(OUT/item['file']).resolve())


if __name__=='__main__':main()
