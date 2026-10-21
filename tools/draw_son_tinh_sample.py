"""Sơn Tinh style preview authored as editable Studio vector paths.

An original stylized interpretation of the legendary mountain lord, not a
claim of an authenticated historical costume. Reuses the user's accepted
simplified person construction, not a rejected human study.
"""
import copy
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QImage, QPainter, QColor
from PySide6.QtWidgets import QApplication
from studio import drawing as ink
from studio import drawing_edit as edit
from studio.character_qc import prepare_packet
from tools.draw_simple_person_sample import create as base_person

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'projects' / 'son_tinh_vector_01'
LINE = '#181b18'
SKIN = '#f6d5b7'
GOLD = '#cba45d'
GREEN = '#63846a'


def create():
    base, _ = base_person()
    original = base['layers'][0]
    doc=ink.document();doc.update(width=900,height=800)
    entry=copy.deepcopy(original);entry['items']=[]
    entry.update(name='Sơn Tinh · gọi núi',role='character')
    entry['character'].update(identity='son-tinh-simple-vector-01')
    entry['character']['style_override'].update(reference='../simple_person_vector_01/preview.png',
        concept='Original legendary mountain lord; illustrative costume, not historical reconstruction.')
    entry['character']['landmarks'].update(elbow_right=[552,511],wrist_right=[597,470])
    for guide in entry['guides']:
        if guide['name'] in ('elbow_right','wrist_right'):
            guide['point']=entry['character']['landmarks'][guide['name']][:]
    doc['layers']=[entry]
    anchors={g['name']:g['id'] for g in entry['guides']}
    commands=[]

    def p(name,path,fill='none',width=5.7,stroke=LINE,parts=(),anchor=None,layer=0):
        nonlocal doc
        command=dict(op='add_path',layer=layer,path=path,fill=fill,stroke=stroke,width=width)
        commands.append(command);doc=edit.apply_command(doc,command)
        item=doc['layers'][layer]['items'][-1];item.update(name=name,parts=list(parts))
        if anchor:edit.bind_items(doc['layers'][layer],[len(doc['layers'][layer]['items'])-1],anchors[anchor])

    # Compact robe and relaxed left hand preserve the accepted body language.
    p('Tay trái thả', 'M286 537 C282 558 286 577 297 583 Q306 587 313 584 L313 541 Z',SKIN,
      parts=('hand_left','fingers_left'),anchor='wrist_left')
    p('Tà áo sau', 'M321 557 L480 557 L505 674 C482 695 437 704 400 704 '
      'C359 704 320 696 297 677 Z', '#496651',parts=('leg_left','leg_right'))
    p('Tà áo chính', 'M321 553 L479 553 L484 675 C456 689 429 691 400 691 '
      'C372 691 342 688 316 677 Z', GREEN,width=5.1)
    p('Viền gấu', 'M317 658 C366 671 435 672 483 659 L484 675 '
      'C435 695 365 693 316 677 Z',GOLD,width=3.4)
    p('Nếp áo', 'M365 586 L359 655 M434 586 L441 657',width=3,stroke='#3d5a45')
    # Lifted right forearm connects continuously into an open mitten hand.
    p('Tay gọi núi', 'M502 479 L541 509 Q549 515 558 506 L584 475 '
      'C587 470 589 463 587 458 L584 447 C583 442 586 440 590 442 L600 455 '
      'L620 450 C627 448 630 454 625 458 L613 464 '
      'L631 462 C638 462 639 468 632 471 L617 475 '
      'L628 477 C635 479 634 484 628 485 L616 484 '
      'L625 488 C631 490 628 495 623 495 L609 490 '
      'Q604 489 600 482 L574 524 Q556 546 537 534 L485 501 Z',
      SKIN,parts=('upper_arm_right','forearm_right','hand_right','fingers_right'),anchor='wrist_right')
    p('Nếp lòng bàn tay', 'M600 456 Q596 466 600 475',width=2.5,stroke='#9e7555',anchor='wrist_right')
    p('Áo tông đất', 'M348 426 C329 429 314 442 301 465 C290 488 282 519 278 547 '
      'L309 555 L312 576 Q400 590 488 576 L490 519 L516 493 L492 463 '
      'C481 444 467 432 452 427 Z', '#bc8d58',
      parts=('torso','sleeve_left','sleeve_right','upper_arm_left','forearm_left'))
    p('Bóng áo', 'M475 449 L493 465 L506 491 L483 514 L481 574 L459 578 '
      'C469 537 473 487 475 449 Z','#a77744',width=1,stroke='none')
    p('Viền tay áo trái', 'M282 526 L311 534 L308 554 L278 547 Z',GREEN,width=4.3)
    p('Viền tay áo phải', 'M501 478 L516 493 L490 519 L480 504 Z',GREEN,width=4.3)
    p('Vai và mép tay áo', 'M321 475 L311 534',width=4.7)
    p('Cổ áo giao', 'M344 433 L400 475 L455 434 M400 475 L427 564',width=4.7)
    p('Dải cổ áo trái', 'M341 436 L391 477 L401 467 L354 431 Z','#e1bc79',width=2.4)
    p('Đai lưng', 'M311 560 Q400 577 488 560 L488 582 Q400 599 311 582 Z','#87503a',width=4.9)
    p('Khóa đai', 'M381 567 Q400 571 419 567 L419 587 Q400 592 381 587 Z',GOLD,width=3.7)
    p('Khóa đai giữa', 'M394 574 L406 574 L406 584 L394 584 Z','#7c5834',width=1,stroke='none')
    p('Dải đai rủ', 'M434 588 L448 588 L458 633 L444 628 L437 636 Z','#87503a',width=3.7)
    # Hair knot is behind the same large head construction as the style sample.
    p('Búi tóc', 'M367 126 C353 111 356 86 374 78 C393 67 420 72 430 89 '
      'C440 108 429 124 418 131 Z','#34353c',width=6.1,parts=('hair',),anchor='head_top')
    p('Dây buộc búi', 'M364 116 Q395 128 427 116 L425 131 Q396 141 368 130 Z',GOLD,width=3.8,anchor='head_top')
    names={'Cổ khuất theo thiết kế','Khuôn mặt','Tóc','Mày trái','Mày phải','Mắt trái','Mắt trái phản sáng','Mắt phải','Mắt phải phản sáng','Miệng cười'}
    for item in original['items']:
        if item['name'] in names:
            item=copy.deepcopy(item)
            if item.get('fill')=='#fbe4d9':item['fill']=SKIN
            doc['layers'][0]['items'].append(item)
    # One compact headband with a mountain-shaped crest; not an imperial crown.
    p('Băng trán', 'M245 226 C320 190 460 178 545 218 L549 239 '
      'C460 198 323 208 242 247 Z',GOLD,width=4.7,anchor='head_top')
    p('Huy hiệu núi', 'M380 216 L394 193 L404 205 L414 188 L434 214 Z',
      '#527354',width=3.4,anchor='head_top')
    # Object layers are genuinely separate from the character for later directing.
    doc['layers'].append(ink.layer('Núi được gọi lên · vật thể độc lập'))
    p('Núi xa', 'M590 407 L631 340 Q634 335 638 341 L672 394 L695 367 '
      'Q698 364 701 370 L724 407 Z','#98aa8d',width=4.4,layer=1)
    p('Núi gần', 'M617 415 L658 352 Q662 346 666 353 L699 400 L714 380 '
      'L742 415 Z','#648462',width=4.8,layer=1)
    p('Mặt sáng sườn núi', 'M662 352 L654 380 L665 373 L671 393 L678 384 Z',
      '#c7cda5',width=1,stroke='none',layer=1)
    p('Đá bay trái', 'M585 431 L592 422 L605 425 L608 435 L594 439 Z',
      '#b1a188',width=3.3,layer=1)
    p('Đá bay phải', 'M711 434 L718 423 L732 426 L734 439 L719 443 Z',
      '#a3947e',width=3.3,layer=1)
    p('Luồng nâng núi', 'M645 431 Q646 440 643 446 M674 431 Q677 441 674 447 M699 440 L699 447',
      width=3.1,stroke='#84987a',layer=1)
    entry=doc['layers'][0]
    entry['character']['review_regions'].update(face=[220,65,360,386],hand_left=[272,531,50,66],hand_right=[576,432,70,65])
    entry['character_qc']=dict(status='pending',reason='Style preview requested by user, simplified anatomy; not a historical costume reconstruction or an approved production asset.')
    return doc,commands


def main():
    app=QApplication.instance() or QApplication([])
    OUT.mkdir(parents=True,exist_ok=True)
    doc,commands=create()
    ink.render(doc,1350).save(str(OUT/'preview.png'))
    image=QImage(1350,1200,QImage.Format.Format_ARGB32_Premultiplied);image.fill(Qt.GlobalColor.transparent)
    p=QPainter(image);p.setRenderHint(QPainter.RenderHint.Antialiasing);p.scale(1.5,1.5)
    for entry in doc['layers']:ink.paint_layer(p,entry)
    p.end();image.save(str(OUT/'preview_transparent.png'))
    prepare_packet(doc['layers'][0],OUT)
    ink.save_drawing(doc,OUT/'son_tinh.drawing.json')
    (OUT/'authoring_commands.json').write_text(json.dumps(commands,ensure_ascii=False,indent=2),encoding='utf-8')
    from studio.ui.drawing_dialog import DrawingDialog
    from studio.ui.style import STYLE
    app.setStyle('Fusion');app.setStyleSheet(STYLE)
    desk=DrawingDialog(doc,standalone=True);desk.resize(1440,920);desk.canvas.show_guides=False
    desk.tools.setCurrentIndex(desk.tools.findData('node'));desk.canvas.selected={1};desk.canvas.selection_changed.emit(0)
    desk.show();app.processEvents();desk.grab().save(str(OUT/'studio_editor.png'));desk.close()
    for item in doc['layers'][0]['qc_packet']['evidence']:
        if item['kind'] in ('face','hand_left','hand_right','thumbnail','comparison'):
            print(item['kind'],(OUT/item['file']).resolve())
    print(OUT/'preview.png')


if __name__=='__main__':main()
