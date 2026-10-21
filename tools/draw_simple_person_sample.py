"""Draw a simplified person with Studio paths; no image generation or tracing.

The user's latest reference deliberately uses mitten hands and a single lower
body silhouette. This is a local style exercise, not a new production master.
"""
import argparse
import copy
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QImage, QColor, QPainter, QFont
from PySide6.QtWidgets import QApplication
from studio import drawing as ink
from studio import drawing_edit as edit
from studio.character_qc import prepare_packet, PROFILE, source_hash

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'projects' / 'simple_person_vector_01'
LINE = '#151516'
SKIN = '#fbe4d9'
SHIRT = '#8298ac'
HAIR = '#34353c'


def create():
    doc = ink.document(); doc.update(width=800, height=800)
    entry = doc['layers'][0]
    entry.update(name='Nhân vật đơn giản · theo mẫu người dùng', role='character')
    # Common silhouette coordinates establish a large head above a compact body.
    guides = {}
    landmarks = dict(head_top=[400, 116], chin=[400, 438], head_left=[248, 304],
                     head_right=[553, 304], neck_base=[400, 451],
                     shoulder_left=[322, 459], shoulder_right=[478, 459], waist=[400, 578],
                     elbow_left=[290, 521], elbow_right=[510, 521],
                     wrist_left=[295, 557], wrist_right=[505, 557],
                     foot_left=[345, 688], foot_right=[455, 688])
    for name, point in landmarks.items(): guides[name] = edit.add_guide(entry, name, point)
    entry['character'] = dict(identity='simple-person-reference-exercise-01', profile=PROFILE,
        view='full_body', landmarks=landmarks, review_regions={},
        style_override=dict(reference='user_reference.png', requested_by='user',
            proportions='oversized head and compact continuous lower body',
            hands='simplified mitten silhouettes as explicitly shown in latest reference',
            lower_body='single rounded block, not separate trousers and shoes',
            status='preview_only_not_a_production_qc_exception'))
    commands = []

    def p(name, path, fill='none', width=5.7, stroke=LINE, parts=(), anchor=None):
        nonlocal doc
        command = dict(op='add_path', layer=0, path=path, fill=fill, stroke=stroke, width=width)
        commands.append(command); doc = edit.apply_command(doc, command)
        item = doc['layers'][0]['items'][-1]
        item.update(name=name, parts=list(parts))
        if anchor: edit.bind_items(doc['layers'][0], [len(doc['layers'][0]['items'])-1], guides[anchor])

    # The two hands continue under sleeves and are covered by them at the wrist.
    p('Tay trái giản lược', 'M286 538 C282 558 286 576 296 582 Q304 587 312 586 L313 541 Z',
      SKIN, parts=('hand_left', 'fingers_left'), anchor='wrist_left')
    p('Tay phải giản lược', 'M514 538 C518 558 514 576 504 582 Q496 587 488 586 L487 541 Z',
      SKIN, parts=('hand_right', 'fingers_right'), anchor='wrist_right')
    # One lower silhouette, following the new user's intentional style.
    p('Thân dưới liền khối', 'M309 560 L491 560 L491 661 C491 680 457 690 400 690 '
      'C343 690 309 680 309 661 Z', '#393a3f', parts=('leg_left', 'leg_right'))
    p('Bóng phẳng thân dưới', 'M474 578 L488 575 L488 661 Q486 674 462 678 '
      'C472 653 472 613 474 578 Z', '#303136', width=1, stroke='none')
    # Both sleeves and torso come from one connected outline.
    p('Áo và hai tay áo', 'M347 427 C327 433 312 448 301 469 C289 491 282 520 278 547 '
      'L308 554 L310 574 C360 583 441 583 490 574 L492 554 L522 547 '
      'C518 520 511 491 499 469 C488 448 473 433 453 427 Z', SHIRT,
      parts=('torso', 'sleeve_left', 'sleeve_right', 'upper_arm_left', 'forearm_left',
             'upper_arm_right', 'forearm_right'))
    p('Bóng phẳng áo', 'M476 451 C498 478 508 513 514 543 L490 549 L488 573 L470 575 '
      'C478 536 477 483 476 451 Z', '#758ca1', width=1, stroke='none')
    p('Đường tay áo trái', 'M319 475 L309 549 M283 525 Q295 531 310 532', width=5.1)
    p('Đường tay áo phải', 'M481 475 L491 549 M517 525 Q505 531 490 532', width=5.1)
    p('Nẹp áo', 'M400 447 L400 578', width=4.5)
    p('Cổ áo trái', 'M335 434 L373 482 L400 452 Z', '#9bafbf', width=5.3)
    p('Cổ áo phải', 'M465 434 L427 482 L400 452 Z', '#9bafbf', width=5.3)
    p('Cúc trên', 'M420 500 C420 507 410 507 410 500 C410 493 420 493 420 500 Z', LINE, 1, 'none')
    p('Cúc dưới', 'M420 531 C420 538 410 538 410 531 C410 524 420 524 420 531 Z', LINE, 1, 'none')
    p('Cạp thân dưới', 'M310 562 C364 577 437 577 490 562 L490 581 '
      'C439 595 362 595 310 581 Z', '#323338', width=5.1)
    # Neck is behind the face, never painted over its finished jaw contour.
    p('Cổ khuất theo thiết kế', 'M380 435 Q400 442 420 435 L420 447 L400 452 L380 447 Z',
      SKIN, width=1, stroke='none', parts=('neck',), anchor='head_top')
    # Face is one coherent contour; hair overlaps it rather than a dangling head.
    p('Khuôn mặt', 'M274 226 C254 248 246 281 249 320 C251 363 273 400 310 420 '
      'C335 434 367 441 400 441 C433 441 465 434 490 420 '
      'C527 400 549 363 551 320 C554 281 546 248 526 226 '
      'C490 195 310 195 274 226 Z', SKIN, parts=('head',), anchor='head_top')
    p('Tóc', 'M252 330 C235 307 227 282 231 253 L225 257 '
      'C222 240 228 217 237 200 L225 205 C232 180 250 162 276 147 '
      'L261 140 C286 132 313 122 344 118 C401 109 454 115 478 143 '
      'C508 142 533 164 548 190 C561 213 571 242 566 260 '
      'L558 254 C560 277 551 304 542 319 L539 286 '
      'L521 264 C514 248 509 231 503 212 L485 214 L475 203 '
      'L420 231 L427 211 C403 225 374 237 340 243 L359 215 '
      'C338 227 318 235 298 235 L281 280 L271 277 Z',
      HAIR, width=6.4, parts=('hair',), anchor='head_top')
    p('Mày trái', 'M312 271 C321 261 337 260 347 266', width=6.6,
      parts=('brow_left',), anchor='head_top')
    p('Mày phải', 'M453 266 C463 260 479 261 488 271', width=6.6,
      parts=('brow_right',), anchor='head_top')

    def eye(name, x, part):
        p(name, f'M{x} 313 C{x} 328 {x-6} 339 {x-12} 339 '
          f'C{x-19} 339 {x-24} 328 {x-24} 313 C{x-24} 298 {x-19} 288 {x-12} 288 '
          f'C{x-6} 288 {x} 298 {x} 313 Z', '#101010', 1, 'none', (part,), 'head_top')
        p(name+' phản sáng', f'M{x-11} 300 C{x-11} 305 {x-17} 305 {x-17} 300 '
          f'C{x-17} 295 {x-11} 295 {x-11} 300 Z', '#ffffff', 1, 'none', (), 'head_top')
    eye('Mắt trái', 340, 'eye_left'); eye('Mắt phải', 483, 'eye_right')
    p('Miệng cười', 'M380 380 Q400 394 420 380', width=4.8,
      parts=('mouth',), anchor='head_top')
    entry = doc['layers'][0]
    entry['character']['occlusions'] = {
        'ear_left':dict(reason='Latest user reference hides ears beneath side hair.',occluder='hair'),
        'ear_right':dict(reason='Latest user reference hides ears beneath side hair.',occluder='hair')}
    entry['character']['review_regions'] = dict(face=[220,105,360,345], hand_left=[272,532,50,62],hand_right=[478,532,50,62])
    entry['character_qc'] = dict(status='pending', reason='Latest-reference style preview; historical anatomy rubric is not a match for intentional mitten hands and block lower body.')
    return doc, commands


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--open',action='store_true');args=parser.parse_args()
    app=QApplication.instance() or QApplication([])
    OUT.mkdir(parents=True,exist_ok=True)
    doc,commands=create()
    ink.save_drawing(doc,OUT/'character.drawing.json')
    (OUT/'authoring_commands.json').write_text(json.dumps(commands,ensure_ascii=False,indent=2),encoding='utf-8')
    ink.render(doc,1200).save(str(OUT/'preview.png'))
    transparent=QImage(1200,1200,QImage.Format.Format_ARGB32_Premultiplied);transparent.fill(Qt.GlobalColor.transparent)
    painter=QPainter(transparent);painter.setRenderHint(QPainter.RenderHint.Antialiasing);painter.scale(1.5,1.5)
    ink.paint_layer(painter,doc['layers'][0]);painter.end();transparent.save(str(OUT/'preview_transparent.png'))
    prepare_packet(doc['layers'][0],OUT);ink.save_drawing(doc,OUT/'character.drawing.json')
    board=QImage(1600,900,QImage.Format.Format_ARGB32_Premultiplied);board.fill(QColor('white'))
    painter=QPainter(board);painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
    font=QFont('Segoe UI');font.setPixelSize(24);font.setBold(True);painter.setFont(font);painter.setPen(QColor('#252b2d'))
    painter.drawText(65,50,'THAM CHIẾU BẠN GỬI');painter.drawText(845,50,'BẢN VẼ VECTOR TRONG STUDIO')
    reference=QImage(str(OUT/'user_reference.png'))
    painter.drawImage(QRectF(10,95,770,708),reference)
    painter.drawImage(QRectF(800,70,790,790),ink.render(doc,1000))
    painter.end();board.save(str(OUT/'comparison.png'))
    from studio.ui.drawing_dialog import DrawingDialog
    from studio.ui.style import STYLE
    app.setStyle('Fusion');app.setStyleSheet(STYLE)
    desk=DrawingDialog(doc,standalone=True);desk.resize(1440,920)
    desk.tools.setCurrentIndex(desk.tools.findData('node'));desk.canvas.selected={17}
    desk.canvas.selection_changed.emit(0)
    desk.editor_tabs.setCurrentIndex(3);desk.show();app.processEvents();desk.grab().save(str(OUT/'studio_editor.png'))
    if args.open:
        desk.protect_unsaved=True;sys.exit(app.exec())
    desk.close()
    print(OUT/'preview.png')


if __name__=='__main__':main()
