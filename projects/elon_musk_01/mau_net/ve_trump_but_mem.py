"""Mẫu thử bút của Bàn vẽ Studio. Tất cả đường và lực nhấn đều do mã xác định."""
from math import ceil, cos, pi
from pathlib import Path
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPainter
from PySide6.QtWidgets import QApplication

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2]))
from studio import drawing
from studio.drawing_edit import brush_item
from studio.character_qc import prepare_packet

INK = '#2e2526'
SKIN = '#f4c5a0'
FOLD = '#aa795f'
HAIR = '#efd298'
GOLD = '#87684a'
SUIT = '#344158'
DARK = '#293449'


class Ink:
    """Sample an authored Bézier spine in arc length for the existing pressure brush."""
    def __init__(self, layer):
        self.items = layer['items']

    def add(self, item, parts):
        item.update(id=f'trump-{len(self.items):03d}', parts=parts.split())
        self.items.append(item)

    def stroke(self, part, data, width, color=INK, pressure=(.12, .84, .53, .08)):
        curve = drawing.painter_path(drawing.path_item(data))
        length = curve.length()
        if length <= 0:
            return
        steps = max(8, ceil(length / 1.4))
        points = []
        for i in range(steps + 1):
            t = i / steps
            pos = curve.pointAtPercent(curve.percentAtLength(t * length))
            u = t * (len(pressure) - 1)
            k = min(int(u), len(pressure) - 2)
            mix = (1 - cos(pi * (u - k))) / 2
            force = pressure[k] + mix * (pressure[k + 1] - pressure[k])
            points.append([round(pos.x(), 3), round(pos.y(), 3), round(force, 4)])
        self.add(brush_item(points, color, width, thinning=.77, smoothing=.48, pressure=True), part)

    def shape(self, part, data, fill, width=3.5, color=INK):
        # A closed colour shape gets a continuous rounded edge. Pen accents are open
        # strokes so a hair tip or fingertip can never leave a hole in the silhouette.
        self.add(drawing.path_item(data, fill, color if width else 'none', width or 1), part)


def clothes(b):
    s, i = b.shape, b.stroke
    s('leg_left leg_right','M131 346 C152 341 203 339 232 347 C233 372 239 407 245 433 Q231 441 209 436 L192 387 Q190 378 185 375 C179 393 169 421 165 436 Q144 440 125 435 C129 408 132 373 131 346 Z',DARK,4.0)
    i('leg_left','M149 426 C149 414 153 405 155 400',1.7,'#617184')
    i('leg_right','M226 424 Q222 413 221 405',1.6,'#616a7b')
    s('shoe_left','M126 430 C136 433 152 434 165 430 Q169 436 165 444 C156 451 126 453 108 450 Q101 449 104 444 Q107 439 118 437 Z','#39363b',3.5)
    s('shoe_right','M209 431 C220 434 234 434 243 430 L249 436 C258 437 269 441 271 446 Q273 451 263 451 Q235 453 211 449 Q206 446 209 431 Z','#39363b',3.5)
    i('shoe_left','M111 445 Q122 447 140 444',1.35,'#92857b')
    i('shoe_right','M237 443 Q249 446 262 445',1.35,'#92857b')
    s('neck','M166 237 Q181 247 208 240 L211 269 L166 277 Z',SKIN,2.5)
    s('upper_arm_right forearm_right sleeve_right','M225 256 C247 251 259 270 264 288 Q272 309 275 329 Q268 336 256 334 L249 315 L230 291 Z',DARK,4.0)
    s('sleeve_right','M256 325 Q264 326 274 322 L277 330 Q269 335 258 335 Z','#f5eee0',2.1)
    s('hand_right fingers_right','M258 332 Q263 333 270 329 Q275 327 279 332 Q284 338 282 346 Q281 352 276 354 Q269 358 263 354 Q258 354 256 349 Q252 347 251 342 Q249 338 252 335 Q255 333 258 335 Z',SKIN,3)
    i('fingers_right','M259 340 Q263 341 264 347 Q265 351 263 353',1.7,FOLD)
    i('fingers_right','M274 347 Q275 351 272 354',1.5,FOLD)
    s('torso','M126 261 C141 249 164 246 175 247 Q185 262 207 247 Q231 247 242 260 Q245 302 251 354 C230 366 162 370 122 355 Z','#f9f1df',3.1)
    s('torso','M167 249 L185 257 L178 271 L159 255 Z','#fff9eb',1.9)
    s('torso','M189 258 L205 246 L216 253 L201 271 Z','#fff9eb',1.9)
    s('torso','M178 259 Q186 255 193 259 L198 266 L192 277 L184 278 L176 268 Z','#b64339',2.25)
    s('torso','M184 274 L192 274 C194 298 200 324 207 350 L194 366 L181 356 Q185 312 184 274 Z','#c75044',2.8)
    s('torso','M159 247 Q139 245 124 257 Q117 271 120 303 Q121 324 111 354 C130 361 153 366 172 358 Q182 345 183 324 C180 292 174 263 159 247 Z',SUIT,3.8)
    s('torso','M212 248 C227 248 238 250 245 261 Q253 277 248 306 Q248 329 257 353 Q242 361 216 359 Q207 350 201 326 Q199 290 212 248 Z',SUIT,3.7)
    i('torso','M157 252 C152 259 146 264 145 267 Q154 269 162 274 L153 279 Q171 295 180 313',3.3)
    i('torso','M216 252 L229 265 L220 271 L226 274 Q210 289 202 307',2.9)
    i('torso','M129 335 Q141 340 153 338',2.2)
    i('torso','M228 333 Q240 333 246 328',1.9)
    s('upper_arm_left forearm_left sleeve_left','M132 254 C118 251 109 260 103 272 L91 290 C84 286 79 278 74 270 Q66 270 56 278 C60 296 68 315 82 320 C99 326 120 311 129 295 C137 280 144 265 132 254 Z',SUIT,3.9)
    i('sleeve_left','M86 306 Q95 302 100 294',1.7,'#626e80')
    s('sleeve_left','M55 272 Q65 273 72 266 L79 274 Q73 282 59 284 Z','#f9f1e2',2.4)


def head(b):
    s, i = b.shape, b.stroke
    # Face turns right, with the far side narrower and the cheek settling into the collar.
    s('head','M102 134 C100 96 135 67 185 61 C240 52 282 76 297 114 Q305 132 301 148 Q300 160 307 172 C315 186 322 200 317 216 C313 232 300 242 278 248 C251 258 207 260 183 254 Q149 248 133 231 Q120 217 117 206 C105 211 91 205 85 193 C78 180 81 165 92 162 L102 164 Z',SKIN,4.35)
    i('head','M317 216 C313 232 300 242 278 248 C251 258 207 260 183 254',4.6,INK,(.32,.76,.68,.3))
    s('ear_left','M115 165 Q102 154 93 162 C82 170 85 187 94 197 Q103 207 116 201 C107 198 106 188 105 179 Q106 169 115 165 Z','#eeb994',0)
    i('ear_left','M91 178 C94 170 104 168 110 176 Q113 179 111 184',2.5,'#885e4a')
    i('head','M144 222 Q156 239 176 242',1.8,'#c28d71')
    # Lay the back hair and crown together; the open locks cross the forehead at unequal lengths.
    s('hair','M96 170 C86 163 83 152 83 141 Q77 146 76 153 C69 134 73 112 82 94 C78 96 75 99 73 102 C77 80 92 62 113 52 C143 30 181 22 215 27 C238 30 257 36 278 45 C293 52 305 50 314 40 C315 50 311 60 299 69 Q308 69 315 63 C311 79 299 86 284 88 Q296 99 296 117 C289 111 284 104 274 102 L266 101 C249 100 232 94 215 90 C179 83 155 91 140 107 C130 118 126 136 123 153 L117 171 Q110 157 100 161 Z',HAIR,4.35)
    i('hair','M113 52 C143 30 181 22 215 27 C238 30 257 36 278 45',4.5,INK,(.25,.74,.58,.28))
    s('hair_accent','M82 126 C94 95 113 81 129 73 Q97 104 90 144 Q85 140 82 126 Z','#e6c187',0)
    s('hair_accent','M225 83 C248 89 266 90 283 87 Q279 97 265 100 C252 98 240 91 225 83 Z','#e6c187',0)
    i('hair','M103 84 C123 56 167 39 204 42 C223 42 240 48 248 53',2.65,'#695443',(.1,.81,.67,.1))
    i('hair','M143 80 C166 61 187 56 213 58',2.2,GOLD)
    i('hair','M211 76 C244 68 267 77 286 69 Q299 66 306 59',2.8,'#695443')
    i('hair','M86 142 Q93 116 105 106',1.9,GOLD)
    i('hair','M112 147 Q114 132 121 122',1.65,GOLD)
    s('brow_left','M149 142 C157 131 173 128 187 130 Q201 132 212 139 Q213 142 208 143 C190 139 170 136 150 145 Z','#c6a887',2.0,'#685448')
    s('brow_right','M242 135 C251 123 266 117 277 118 Q283 119 282 122 Q264 125 245 139 Z','#c6a887',2.05,'#685448')
    i('brow_left','M161 121 Q176 116 190 120',1.3,'#bc8d70')
    i('brow_right','M227 129 Q230 122 233 120',1.55,'#ba896f')
    s('eye_left','M153 161 Q171 147 193 151 Q205 153 210 155 C203 166 178 174 161 166 Z','#f9e6cd',0)
    s('eye_right','M246 151 Q258 136 281 135 C283 145 270 155 254 156 Z','#f9e6cd',0)
    s('eye_left','M188 152 Q194 148 199 153 C203 161 198 166 192 165 Q186 162 188 152 Z',INK,0)
    s('eye_right','M265 139 Q271 135 275 137 Q279 146 272 150 Q265 152 264 146 Z',INK,0)
    i('eye_left','M152 162 Q171 145 194 151 Q205 152 211 155',3.8)
    i('eye_right','M245 151 Q258 136 272 135 Q279 134 283 135',3.6)
    i('eye_left','M159 171 C170 180 191 178 201 169',2.4,'#9a705c')
    i('eye_right','M252 160 Q269 164 281 150',2.2,'#9a705c')
    i('nose','M225 148 C230 151 233 163 237 173 Q241 179 247 181 C251 182 254 178 254 175',2.95,'#61483f',(.18,.7,.85,.15))
    i('nose','M217 180 Q220 176 226 178',1.75,'#9a705c')
    i('cheek','M147 204 Q151 197 158 194',1.8,'#b18369')
    i('cheek','M285 182 Q292 186 295 194',1.85,'#ad7e65')


def hand(b):
    s, i = b.shape, b.stroke
    # Folded fingers read as one gesture; the thumb touches the index with a small clear countershape.
    s('hand_left fingers_left','M58 275 Q52 271 48 263 C42 258 38 249 38 240 Q38 233 43 234 Q47 235 48 242 L50 246 Q46 232 49 225 Q52 219 56 223 Q60 225 58 235 L60 239 Q59 222 65 216 Q70 212 74 216 Q77 219 73 226 L69 233 Q77 225 85 229 Q92 232 90 238 Q89 242 84 242 Q80 242 78 238 Q74 240 72 246 Q77 241 82 243 Q89 246 86 252 Q83 256 77 258 Q74 269 66 274 Q61 277 58 275 Z',SKIN,3.25)
    i('fingers_left','M51 247 Q52 253 56 256',1.65,FOLD)
    i('fingers_left','M60 239 Q60 244 63 247',1.75,FOLD)
    i('fingers_left','M72 246 Q70 249 71 253',2,'#885f4d')
    i('hand_left','M62 268 Q67 266 69 262',1.45,FOLD)


def build():
    doc = drawing.document()
    doc.update(width=360, height=480)
    layer = doc['layers'][0]
    layer.update(id='trump-ink-study', name='Donald Trump · bút đậm nhạt', role='character')
    pen = Ink(layer)
    clothes(pen)
    head(pen)
    hand(pen)
    layer['character'] = dict(profile='explainer-reference-v1', view='full_body', identity='trump-code-03',
        pose='three_quarter_pinch', design_notes='Đầu lớn, không miệng theo mẫu người dùng.',
        review_regions=dict(face=[66,18,260,249], hand_left=[31,208,65,74], hand_right=[245,323,45,41]),
        landmarks=dict(head_top=[203,26], chin=[219,257], head_left=[75,142], head_right=[319,207],
            shoulder_left=[131,254], shoulder_right=[241,258], neck_base=[189,260], waist=[190,349],
            elbow_left=[85,310], elbow_right=[259,295], wrist_left=[63,275], wrist_right=[267,332],
            foot_left=[133,450], foot_right=[240,450]),
        occlusions=dict(ear_right=dict(reason='Tai xa khuất sau đầu ở góc nhìn ba phần tư.', occluder='head')))
    return doc


def main():
    app = QApplication.instance() or QApplication([])
    doc = build()
    entry = doc['layers'][0]
    prepare_packet(entry, HERE)
    drawing.save_drawing(doc, HERE / 'Trump_but_mem_V03.drawing.json')
    scale = 3
    img = QImage(doc['width'] * scale, doc['height'] * scale, QImage.Format.Format_ARGB32_Premultiplied)
    img.fill(Qt.GlobalColor.transparent)
    p = QPainter(img)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.scale(scale, scale)
    drawing.paint_layer(p, entry)
    p.end()
    if not img.save(str(HERE / 'Trump_but_mem_V03.png')):
        raise OSError('Không thể lưu bản xem thử.')


if __name__ == '__main__':
    main()
