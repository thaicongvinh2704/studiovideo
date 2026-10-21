"""Original path study based on the user's required cartoon finish, not traced art."""
import copy
import json
from pathlib import Path
from .drawing import layer, path_item
from .character_qc import ROOT

MODEL = ROOT / 'assets' / 'characters' / 'reference_person_v2.drawing.json'


def authored_person():
    entry = layer('Nhân vật tĩnh · mẫu đối chiếu 02')
    entry['role'] = 'character'
    ink = '#202322'; skin = '#ffdeb6'
    def p(part, d, fill='none', width=3.2, stroke=ink, extra=()):
        item = path_item(d, fill, stroke, width)
        item['parts'] = [part, *extra]; entry['items'].append(item)
    # Distinct trouser legs and finished shoe silhouettes.
    p('leg_left', 'M151 415 Q177 420 201 418 L194 476 L186 537 Q173 543 158 537 L153 478 Z', '#87a8c0')
    p('leg_right', 'M199 419 Q224 421 247 415 L241 477 L237 537 Q223 543 208 537 L203 476 L197 455 Z', '#87a8c0')
    p('trouser_seam', 'M157 429 Q197 437 239 429 M200 435 L198 456', width=2)
    p('shoe_left', 'M158 534 Q171 537 185 535 L186 548 Q183 554 169 555 L147 555 Q142 550 147 544 Z', '#ffffff')
    p('shoe_right', 'M209 535 Q221 540 237 534 L249 545 Q252 553 244 555 L210 555 Q205 550 209 535 Z', '#ffffff')
    p('shoe_detail', 'M146 550 L183 550 M210 550 L249 550', width=1.7)
    # Arms connect at shoulders, elbows and wrists; hands are separate finished contours.
    p('upper_arm_left', 'M121 336 Q114 357 118 381 L129 425 L144 421 L138 380 L145 349 Z', skin, extra=('forearm_left',))
    p('hand_left', 'M129 420 L142 419 L142 431 Q145 432 148 437 Q151 442 148 444 Q145 446 142 441 L140 439 L143 454 Q143 459 140 460 Q137 461 136 457 L134 448 L137 459 Q138 464 135 465 Q131 467 129 462 L127 450 L130 460 Q131 465 128 466 Q124 467 122 462 L119 449 L121 456 Q122 461 119 461 Q115 462 114 456 L110 439 Q109 432 117 428 Z', skin, 2.1)
    p('fingers_left', 'M119 437 Q124 433 130 435 M138 432 L142 438', width=1.3)
    p('upper_arm_right', 'M268 336 L282 369 Q285 378 294 375 L326 355 L337 369 L302 397 Q283 407 271 392 L251 350 Z', skin, extra=('forearm_right',))
    # Open hand in side view: thumb plus four distinct fingertips, gentle knuckle arcs.
    p('hand_right', 'M326 356 Q326 349 332 344 L347 329 Q351 325 355 329 Q359 333 354 338 L345 348 L369 335 Q374 333 376 337 Q379 342 373 345 L354 357 L381 347 Q387 346 388 351 Q389 356 382 359 L358 368 L378 361 Q384 360 385 365 Q387 370 381 373 L357 380 L370 377 Q375 377 376 381 Q377 385 371 388 L350 391 Q339 392 333 382 L326 373 Z', skin, 2.7)
    p('fingers_right', 'M338 355 Q340 363 347 367 M344 374 L352 373', width=1.7)
    p('neck', 'M177 257 L177 283 Q193 303 219 284 L218 257 Z', skin)
    p('torso', 'M168 283 Q193 303 224 283 Q251 287 266 307 L281 335 Q271 347 255 351 L248 334 L248 418 Q200 432 150 419 L151 338 L141 354 Q127 350 116 338 L128 310 Q143 288 168 283 Z', '#ffffff', extra=('sleeve_left', 'sleeve_right'))
    p('collar', 'M169 284 Q194 310 223 284 M169 289 Q193 318 225 289', width=2)
    p('sleeve_edge_left', 'M119 334 Q130 343 143 348 M151 338 L143 319', width=2.1)
    p('sleeve_edge_right', 'M258 346 Q269 342 278 333 M248 334 L252 320', width=2.1)
    p('shirt_hem', 'M153 413 Q199 424 245 412 M158 394 L157 405 M236 387 L238 405', width=1.8)
    p('ear_left', 'M150 205 Q138 195 136 209 Q135 225 149 230 Z', skin, 2.8)
    p('ear_right', 'M249 205 Q263 197 263 211 Q261 228 249 231 Z', skin, 2.8)
    p('head', 'M151 183 Q153 150 195 149 Q240 148 249 184 L250 220 Q251 247 227 262 Q211 274 194 268 Q163 264 152 241 Q146 226 149 207 Z', skin)
    p('hair', 'M148 213 L143 190 Q139 178 146 167 L142 158 L156 153 L150 146 L168 144 L164 136 L186 139 Q206 126 223 135 Q242 131 249 147 L258 151 L251 163 L254 179 L249 210 L242 202 L237 181 Q216 184 200 174 Q182 184 161 178 L156 212 Z', '#191d1c')
    for d in ['M151 175 Q161 155 181 147', 'M158 174 Q172 151 194 142',
              'M166 174 Q182 150 205 140', 'M175 174 Q191 150 216 141',
              'M187 173 Q203 151 229 145', 'M199 171 Q217 153 239 152',
              'M210 174 Q228 158 246 159', 'M222 176 Q236 166 249 166',
              'M146 186 L150 201', 'M246 182 L248 197']:
        p('hair_detail', d, width=1.4, stroke='#4b504b')
    p('brow_left', 'M164 203 Q173 196 182 201', width=3.2)
    p('brow_right', 'M208 201 Q217 196 226 202', width=3.2)
    # Narrow oval eyes, rather than a stroke that floats on an empty face.
    p('eye_left', 'M171 214 Q175 209 178 214 L178 221 Q175 227 171 221 Z', ink, 1)
    p('eye_right', 'M214 213 Q218 208 221 213 L221 220 Q218 226 214 220 Z', ink, 1)
    p('nose', 'M196 215 Q193 222 198 226 Q201 230 194 232', width=2.3)
    p('mouth', 'M179 244 Q195 251 213 242 Q208 258 196 259 Q185 257 179 244 Z', '#ffffff', 2.6)
    p('ear_detail', 'M142 210 Q148 211 146 220 M257 210 Q252 214 255 221', width=1.7)
    entry['character'] = dict(profile='explainer-reference-v1', view='full_body',
        identity='reference-person-study-02', pose='static_open_hand',
        landmarks=dict(head_top=[201,128], chin=[201,270], head_left=[143,208], head_right=[254,208],
            shoulder_left=[133,307], shoulder_right=[269,307], neck_base=[198,289], waist=[198,422],
            elbow_left=[125,380], elbow_right=[283,387], wrist_left=[136,422], wrist_right=[331,365],
            foot_left=[166,555], foot_right=[227,555]),
        review_regions=dict(face=[126,119,145,160], hand_left=[100,410,64,68], hand_right=[316,318,78,77]),
        occlusions={})
    return entry


def reviewed_person():
    if not MODEL.exists(): return authored_person()
    # Geometry/QC freshness are checked again at insertion and export, never trusted blindly.
    return copy.deepcopy(json.loads(MODEL.read_text(encoding='utf-8'))['layers'][0])
