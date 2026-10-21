"""Original character trials authored through the Studio vector tools.

No raster/image-generation input. Construction first; --finish adds inking.
These remain review trials, never installed as an approved character master.
"""
import argparse
import copy
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QColor, QFont, QImage, QPainter
from PySide6.QtWidgets import QApplication
from studio import drawing as ink
from studio import drawing_edit as edit
from studio.character_qc import PROFILE, prepare_packet, geometry_issues

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'projects' / 'character_trials_03'
BLACK = '#242624'
SKIN = '#f5d4ad'
WHITE = '#fdfdfb'


class Author:
    def __init__(self, pose, finished):
        self.doc = ink.document()
        self.doc.update(width=440, height=680 if pose != 'point' else 490)
        entry = self.doc['layers'][0]
        entry.update(name='Nhân vật thử 03 · ' + pose, role='character')
        self.pose = pose; self.finished = finished
        self.anchors = {}
        for name, point in [('head_top', [201, 43]), ('chin', [201, 234]),
                            ('head_left', [120, 150]), ('head_right', [280, 150]),
                            ('shoulder_left', [105, 283]), ('shoulder_right', [295, 283]),
                            ('neck_base', [200, 254]), ('waist', [200, 448]),
                            ('elbow_left', [108, 373] if pose != 'point' else [126, 399]),
                            ('elbow_right', [300, 373] if pose != 'staff' else [337, 357]),
                            ('wrist_left', [102, 395] if pose != 'point' else [261, 306]),
                            ('wrist_right', [298, 395] if pose != 'staff' else [371, 331]),
                            ('foot_left', [153, 621]), ('foot_right', [245, 621])]:
            self.anchors[name] = edit.add_guide(entry, name, point)
        entry['character'] = dict(profile=PROFILE, identity='studio-ink-person-03-' + pose,
                                   view='waist_up' if pose == 'point' else 'full_body',
                                   landmarks={g['name']: g['point'][:] for g in entry['guides']},
                                   review_regions={})
        entry['character_qc'] = dict(status='pending', note='Original trial; not user-approved.')

    @property
    def entry(self): return self.doc['layers'][0]

    def path(self, data, fill='none', width=3.2, stroke=BLACK, parts=(), anchor=None, detail=False):
        if detail and not self.finished: return
        if not self.finished and fill != 'none': fill = '#e0e4e1'
        self.doc = edit.apply_command(self.doc, dict(op='add_path', path=data, fill=fill, stroke=stroke, width=width))
        item = self.entry['items'][-1]
        item['parts'] = list(parts)
        if anchor: edit.bind_items(self.entry, [len(self.entry['items']) - 1], self.anchors[anchor])

    def oval(self, x, y, rx, ry, fill, part, stroke='none', width=1):
        k = .55228475
        self.path(f'M{x-rx} {y} C{x-rx} {y-k*ry} {x-k*rx} {y-ry} {x} {y-ry} '
                  f'C{x+k*rx} {y-ry} {x+rx} {y-k*ry} {x+rx} {y} '
                  f'C{x+rx} {y+k*ry} {x+k*rx} {y+ry} {x} {y+ry} '
                  f'C{x-k*rx} {y+ry} {x-rx} {y+k*ry} {x-rx} {y} Z',
                  fill, width, stroke, (part,), 'head_top', detail=True)

    def down_arm(self, right=False):
        # Left arm outline is a single flowing contour; right is its exact
        # construction reflection, not an independently sized component.
        fill = ink.path_item('M100 322 C96 344 90 373 91 397 L112 395 C112 370 122 349 130 332 Z', SKIN, 'none')
        contour = ink.path_item('M100 322 C96 344 90 373 91 397 M112 395 C112 370 122 349 130 332', 'none', BLACK, 3.2)
        hand = ink.path_item('M105 396 C102 403 103 414 106 421 L109 434 C110 438 114 439 116 436 '
                            'L116 441 C118 445 123 444 124 440 C128 443 131 439 130 435 '
                            'C134 436 137 432 134 426 L129 411 C132 413 136 411 135 407 '
                            'L130 398 C128 395 126 394 125 395 Z', SKIN, 'none')
        outline = ink.path_item('M105 396 C102 403 103 414 106 421 L109 434 C110 438 114 439 116 436 '
                               'L116 441 C118 445 123 444 124 440 C128 443 131 439 130 435 '
                               'C134 436 137 432 134 426 L129 411 C132 413 136 411 135 407 '
                               'L130 398 C128 395 126 394 125 395', 'none', BLACK, 2.8)
        creases = ink.path_item('M114 423 L116 436 M121 421 L124 440 M127 419 L130 435 M118 409 Q121 407 125 410', 'none', BLACK, 1.6)
        for shape in (hand, outline, creases): edit.translate_item(shape, -14, 0)
        side = 'right' if right else 'left'
        for item, tags in [(fill, ['upper_arm_'+side, 'forearm_'+side]),
                           (contour, []), (hand, ['hand_'+side]),
                           (outline, ['fingers_'+side]), (creases, [])]:
            if item is creases and not self.finished: continue
            if right:
                for command in item['commands']:
                    for i in range(1, len(command), 2): command[i] = 400 - command[i]
            if not self.finished and item['fill'] != 'none': item['fill'] = '#e0e4e1'
            item['parts'] = tags; self.entry['items'].append(item)
            edit.bind_items(self.entry, [len(self.entry['items']) - 1], self.anchors['wrist_'+side])

    def body(self):
        p = self.path
        if self.pose != 'point':
            p('M129 441 C171 448 226 448 271 441 L269 578 C255 583 234 583 216 578 '
              'L204 493 Q199 487 195 494 L183 578 C165 583 146 581 130 577 Z',
              '#7591a6', parts=('leg_left', 'leg_right'))
            p('M200 461 L199 483 M142 452 Q143 468 158 470 M258 452 Q257 468 242 470 '
              'M144 527 L142 560 M255 527 L257 561', width=1.9, stroke='#445c6c', detail=True)
            p('M131 575 C145 579 164 580 180 576 L181 600 C177 606 164 608 145 608 '
              'L119 607 C117 599 122 589 131 587 Z', WHITE, parts=('shoe_left',))
            p('M216 576 C234 580 254 579 268 575 L269 587 C282 592 287 598 285 607 '
              'L256 608 C237 608 220 606 215 600 Z', WHITE, parts=('shoe_right',))
            p('M119 607 L119 618 Q149 624 182 618 L181 600 M215 600 L214 618 Q251 624 285 618 L285 607',
              WHITE, width=2.8, detail=True)
            p('M135 589 L149 592 M132 595 L146 598 M253 592 L268 589 M257 598 L272 595',
              width=1.8, detail=True)
        if self.pose != 'point': self.down_arm()
        if self.pose != 'staff': self.down_arm(True)
        # Neck enters the shirt opening and is overlapped by the face.
        p('M175 213 L175 249 C178 266 222 266 225 249 L225 213 Z',
          SKIN, parts=('neck',))
        p('M176 222 Q200 244 224 222 L224 238 Q199 251 176 237 Z', '#e9bc91', 1, 'none', detail=True)
        p('M172 248 C152 248 129 255 113 268 C102 282 96 301 90 320 '
          'L122 336 L132 314 L128 447 C171 455 227 456 272 447 L268 314 '
          'L278 336 L310 320 C305 300 298 282 284 269 C270 257 247 250 228 248 '
          'C224 267 178 268 172 248 Z',
          WHITE, parts=('torso', 'sleeve_left', 'sleeve_right'))
        p('M265 318 L270 443 Q257 446 245 446 C255 420 255 368 254 350 Z', '#edf0ed', 1, 'none', detail=True)
        p('M165 251 C168 278 232 280 236 251 M101 318 L120 327 M281 327 L300 317 '
          'M138 425 L138 440 Q201 448 261 440 M138 304 L134 317 M264 304 L268 315',
          width=1.8, stroke='#555c57', detail=True)

    def head(self):
        p = self.path
        p('M133 145 C125 135 116 140 117 152 C118 166 123 176 134 175 Z',
          SKIN, parts=('ear_left',), anchor='head_top')
        p('M268 145 C277 135 285 140 283 153 C282 167 276 177 267 175 Z',
          SKIN, parts=('ear_right',), anchor='head_top')
        p('M132 118 C131 91 158 77 199 78 C241 77 266 91 269 118 L271 165 '
          'C271 193 250 217 222 228 C209 236 192 236 177 228 C149 215 131 194 130 165 Z',
          SKIN, parts=('head',), anchor='head_top')
        p('M129 153 L124 125 C117 104 123 85 140 73 C142 58 159 49 178 49 '
          'C195 37 214 45 229 50 C250 49 271 67 281 82 L269 84 L280 95 L272 104 '
          'L272 151 L262 153 L257 114 C246 112 234 101 226 97 '
          'C207 110 173 108 150 123 L142 155 Z', '#232624', parts=('hair',), anchor='head_top')
        # Directional locks, following the silhouette and the part, not a texture overlay.
        for data in [
            'M135 118 C131 96 146 82 163 74',
            'M140 108 C141 83 158 65 178 59',
            'M148 103 C153 77 173 59 193 54',
            'M157 99 C167 73 186 59 207 57',
            'M169 97 C183 74 199 63 219 63',
            'M183 95 C198 79 212 68 229 71',
            'M199 94 C212 83 224 78 239 81',
            'M231 91 C245 91 255 97 264 104',
            'M239 82 C252 83 262 89 270 94',
            'M249 73 Q263 76 271 82',
            'M133 127 L137 142 M265 121 L267 141',
        ]:
            p(data, width=1.6, stroke='#4d514b', anchor='head_top', detail=True)
        p('M154 142 C161 136 173 134 182 139', width=4.4, anchor='head_top', detail=True)
        p('M218 139 C227 134 239 136 246 142', width=4.4, anchor='head_top', detail=True)
        # Keep feature tags on actual feature paths.
        if self.finished:
            self.entry['items'][-2]['parts'] = ['brow_left']
            self.entry['items'][-1]['parts'] = ['brow_right']
        self.oval(169, 159, 4.4, 6.4, BLACK, 'eye_left')
        self.oval(232, 159, 4.4, 6.4, BLACK, 'eye_right')
        p('M201 157 C201 164 197 170 200 173 C202 176 207 175 209 173',
          width=2.5, parts=('nose',), anchor='head_top', detail=True)
        p('M179 192 C193 199 210 199 224 191 C222 206 213 213 201 213 '
          'C189 213 183 204 179 192 Z', WHITE, width=2.7, parts=('mouth',), anchor='head_top', detail=True)
        p('M122 150 Q127 147 129 155 M276 149 Q272 148 272 155',
          width=1.6, anchor='head_top', detail=True)

    def pointing(self):
        p = self.path
        # Forearm and hand share wrist endpoints, no visible seam across the wrist.
        p('M122 336 L137 372 C139 376 141 376 145 373 L251 294 L271 318 '
          'L151 412 C139 422 124 425 112 413 C101 397 94 372 90 320 Z',
          SKIN, stroke='none', parts=('upper_arm_left', 'forearm_left'))
        # A small interior overlap removes the antialias seam between two skin
        # regions while preserving independently editable hand and forearm paths.
        p('M253 294 L271 315 L269 318 L251 297 Z', SKIN, stroke='none',
          parts=('forearm_left',))
        p('M122 336 L137 372 C139 376 141 376 145 373 L251 294 M271 318 '
          'L151 412 C139 422 124 425 112 413 C101 397 94 372 90 320', width=3.2)
        p('M251 294 C256 288 258 281 258 274 C258 267 265 265 269 272 L274 281 '
          'L320 237 C325 231 331 230 334 234 C337 238 334 242 330 246 L301 276 '
          'C309 273 314 277 311 284 C319 283 323 289 316 295 C323 296 323 302 316 308 '
          'L289 327 C280 332 273 325 271 318 Z',
          SKIN, stroke='none', parts=('hand_left',), anchor='wrist_left')
        p('M251 294 C256 288 258 281 258 274 C258 267 265 265 269 272 L274 281 '
          'L320 237 C325 231 331 230 334 234 C337 238 334 242 330 246 L301 276 '
          'C309 273 314 277 311 284 C319 283 323 289 316 295 C323 296 323 302 316 308 '
          'L289 327 C280 332 273 325 271 318',
          width=3, parts=('fingers_left',), anchor='wrist_left')
        p('M301 276 L289 287 M311 284 L300 294 M316 295 L307 303 M266 290 Q271 294 270 301',
          width=1.6, anchor='wrist_left', detail=True)
        p('M121 395 Q126 402 133 403', width=1.5, stroke='#b98d69', detail=True)

    def staff(self):
        p = self.path
        p('M377 233 Q381 230 385 233 L384 529 Q382 538 379 530 Z',
          '#bd8d5d', width=2.6, parts=('prop',))
        p('M310 320 L332 343 C336 346 340 346 344 342 L365 322 L377 340 '
          'L350 366 C342 373 330 372 322 366 L278 336 Z',
          SKIN, stroke='none', parts=('upper_arm_right', 'forearm_right'))
        p('M310 320 L332 343 C336 346 340 346 344 342 L365 322 M377 340 '
          'L350 366 C342 373 330 372 322 366 L278 336', width=3.2)
        p('M365 322 C363 315 367 309 373 310 L379 311 C382 307 389 310 389 315 '
          'C396 315 398 322 394 325 C399 328 397 335 392 336 C395 341 388 346 382 343 '
          'L377 340 L366 338 Z', SKIN, stroke='none', parts=('hand_right',), anchor='wrist_right')
        p('M365 322 C363 315 367 309 373 310 L379 311 C382 307 389 310 389 315 '
          'C396 315 398 322 394 325 C399 328 397 335 392 336 C395 341 388 346 382 343 '
          'L377 340 M366 338 L365 332', width=2.8, parts=('fingers_right',), anchor='wrist_right')
        p('M365 322 C369 319 375 319 379 321 C383 322 383 327 379 329 L371 331 '
          'M384 318 L391 319 M384 326 L393 327 M383 334 L391 336',
          width=1.8, anchor='wrist_right', detail=True)

    def finish(self):
        self.body()
        self.head()
        if self.pose == 'point': self.pointing()
        if self.pose == 'staff': self.staff()
        # Bounds from the actual tagged closed hand contour, with room for outlines.
        for key, part in [('face', 'head'), ('hand_left', 'hand_left'), ('hand_right', 'hand_right')]:
            rect = QRectF()
            for item in self.entry['items']:
                if part in item.get('parts', []): rect = rect.united(ink.item_bounds(item))
            rect = rect.adjusted(-9, -9, 9, 9)
            self.entry['character']['review_regions'][key] = [rect.x(), rect.y(), rect.width(), rect.height()]
        self.entry['character_qc'] = dict(status='pending', note='Trial for visual comparison, not an approved master.')
        return self.doc


def board(documents, path, construction=False):
    image = QImage(2100, 1120, QImage.Format.Format_ARGB32_Premultiplied); image.fill(QColor('white'))
    painter = QPainter(image); painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
    title = QFont('Segoe UI'); title.setPixelSize(29); title.setBold(True); painter.setFont(title); painter.setPen(QColor(BLACK))
    painter.drawText(60, 62, 'NHÂN VẬT THỬ 03' if not construction else 'DỰNG TỔNG THỂ · NHÂN VẬT THỬ 03')
    title.setPixelSize(20); title.setBold(False); painter.setFont(title); painter.setPen(QColor('#77817a'))
    painter.drawText(60, 101, 'Bản vẽ vector của Studio · ba tư thế để đối chiếu · chưa phải mẫu được duyệt')
    labels = ['01  Đứng tự nhiên', '02  Chỉ vào nội dung', '03  Cầm bút chỉ']
    for i, doc in enumerate(documents):
        rendered = ink.render(doc, 900)
        box = QRectF(35 + 690 * i, 150, 650, 850)
        scaled = rendered.scaled(int(box.width()), int(box.height()), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        painter.drawImage(int(box.center().x() - scaled.width() / 2), int(box.center().y() - scaled.height() / 2), scaled)
        title.setPixelSize(24); painter.setFont(title); painter.setPen(QColor(BLACK))
        painter.drawText(140 + 690 * i, 1063, labels[i])
    painter.end(); image.save(str(path))


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--finish', action='store_true'); args = parser.parse_args()
    app = QApplication.instance() or QApplication([])
    OUT.mkdir(parents=True, exist_ok=True)
    documents = []
    for pose in ('stand', 'point', 'staff'):
        author = Author(pose, args.finish); doc = author.finish(); documents.append(doc)
        suffix = '' if args.finish else '_construction'
        folder = OUT / (pose + suffix); folder.mkdir(exist_ok=True)
        ink.save_drawing(doc, folder / 'character.drawing.json')
        ink.render(doc, 1000).save(str(folder / 'preview.png'))
        if args.finish:
            packet = prepare_packet(doc['layers'][0], folder)
            ink.save_drawing(doc, folder / 'character.drawing.json')
            (folder / 'geometry_issues.json').write_text(json.dumps(geometry_issues(doc['layers'][0]), ensure_ascii=False, indent=2), encoding='utf-8')
    board(documents, OUT / ('three_poses.png' if args.finish else 'construction.png'), not args.finish)
    print(OUT / ('three_poses.png' if args.finish else 'construction.png'))


if __name__ == '__main__': main()
