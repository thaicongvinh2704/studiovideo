"""Original static line artwork authored as editable paths, not generated bitmaps.

This is a style study for review, not a user-approved style or historical reconstruction.
"""
from .drawing import document, layer, path_item, INK


def rejected_person_v1():
    entry = layer('Nhân vật tĩnh · sổ ghi chép')
    def p(d, fill='none', width=3.5, stroke=INK):
        entry['items'].append(path_item(d, fill, stroke, width))
    skin = '#f3cfaa'; teal = '#40827e'; pants = '#70685c'
    # Relaxed, weight-bearing silhouette; no pointing hand or rig.
    p('M160 439 Q194 444 230 439 L228 557 Q218 563 204 558 L199 490 L188 559 Q174 563 160 557 Z', pants)
    p('M160 552 Q174 557 188 554 L188 570 Q160 575 148 568 Q147 560 160 552 Z', '#faf6ec')
    p('M206 554 Q219 558 228 552 Q238 558 239 568 Q222 575 204 570 Z', '#faf6ec')
    p('M149 311 Q133 328 126 361 L116 417 Q114 431 124 438 Q135 443 139 429 L149 381 L164 351 Z', skin)
    p('M174 298 L175 275 L212 274 L214 299 L227 309 Q199 335 164 310 Z', skin)
    p('M153 303 L174 297 Q192 316 214 299 L235 308 L249 347 L228 360 L231 443 Q195 452 157 442 L158 361 L135 349 Z', teal)
    p('M177 305 Q191 322 209 306 L212 443 L178 444 Z', '#fbf5e7', 2.8)
    p('M171 302 L180 327 L172 341 M218 303 L210 327 L220 340', width=2.4)
    p('M165 362 L175 364 M219 362 L229 360 M164 419 Q164 432 175 433', width=2.3)
    # Notebook and right forearm are separate shapes within one static character layer.
    p('M220 371 L254 365 L269 433 L234 442 Z', '#e7ba71', 3)
    p('M228 374 L259 435 M238 386 L251 383 M241 397 L254 394', width=1.6)
    p('M241 345 L249 374 L248 401 L227 401 Q220 395 216 399 Q210 404 215 409 L228 416 Q243 421 258 412 Q266 409 265 397 L260 369 L251 345 Z', skin, 3)
    p('M224 402 L234 407 M222 408 L232 412', width=1.8)
    # Ear, face and a calm, slightly curious expression.
    p('M150 214 Q137 205 137 222 Q137 240 151 240 M237 214 Q250 207 248 224 Q246 239 236 238', skin, 3)
    p('M150 194 Q153 155 190 155 Q235 157 239 197 L237 240 Q232 267 208 280 Q192 286 174 275 Q151 262 149 239 Z', skin)
    p('M148 218 L144 193 Q137 178 148 168 Q145 156 161 153 Q165 137 181 144 Q196 131 211 144 Q229 139 234 155 Q248 159 243 175 L238 211 L229 191 Q224 183 219 178 Q211 191 194 182 Q181 192 167 181 Q157 193 155 216 Z', '#303636')
    p('M156 169 Q161 156 174 157 M178 153 Q190 144 203 153 M212 155 Q223 152 229 164', width=1.8, stroke='#646762')
    p('M165 211 Q174 204 182 209 M206 210 Q215 204 223 210', width=3.3)
    p('M173 225 L173 230 M214 224 L214 229', width=5)
    p('M194 224 Q190 236 196 238', width=2.5)
    p('M180 250 Q194 260 210 249 Q199 268 187 258 Z', '#ffffff', 2.6)
    p('M149 226 L153 230 M241 225 L237 230', width=1.8)
    return entry


def person():
    from .character_art import reviewed_person
    return reviewed_person()


def sample_document():
    doc = document(); doc['layers'] = []
    doc['layers'].append(person())
    base = layer('Bệ gạch · giữ tĩnh')
    def p(entry, d, fill='none', width=3.5, stroke=INK):
        entry['items'].append(path_item(d, fill, stroke, width))
    # A small, deliberately clear diagram: three steps, not an ornate scene.
    p(base, 'M497 484 Q622 481 731 484 L1061 480 L1060 539 Q767 544 495 540 Z', '#d58b62')
    p(base, 'M498 484 L533 458 L1087 456 L1061 481', '#e7b084')
    p(base, 'M1061 481 L1087 456 L1085 512 L1060 539 Z', '#b67653')
    p(base, 'M670 388 Q787 385 887 389 L1060 386 L1061 479 Q885 483 668 482 Z', '#d58b62')
    p(base, 'M670 388 L700 363 Q897 360 1088 362 L1060 386', '#e7b084')
    p(base, 'M1060 386 L1088 362 L1087 456 L1061 481 Z', '#b67653')
    p(base, 'M843 293 Q951 290 1061 294 L1060 387 Q950 390 842 386 Z', '#d58b62')
    p(base, 'M843 293 L873 268 Q980 266 1088 269 L1061 294', '#e7b084')
    p(base, 'M1061 294 L1088 269 L1088 363 L1060 387 Z', '#b67653')
    # Sparse mortar seams. Gaps and slight asymmetry are authored once, never jittered per frame.
    for d in ['M496 513 Q751 510 1061 513', 'M594 484 L591 512 M747 484 L749 512 M902 482 L900 511',
              'M667 513 L670 540 M826 514 L823 541 M979 513 L982 539',
              'M671 434 Q875 430 1061 433', 'M774 389 L773 432 M925 388 L928 432',
              'M704 434 L706 482 M851 432 L848 481 M1002 434 L1000 479',
              'M844 339 Q949 341 1060 338 M945 294 L942 339 M886 339 L887 387 M1001 340 L999 388']:
        p(base, d, width=2.4)
    doc['layers'].append(base)
    ground = layer('Mặt đất')
    p(ground, 'M461 543 Q704 548 1117 542 M478 558 L510 558 M1037 559 L1066 558', width=2.6)
    p(ground, 'M388 520 Q424 517 457 521 L454 542 Q421 548 386 543 Z', '#b9b9b2')
    p(ground, 'M388 520 L403 509 L466 510 L457 521 M457 521 L466 510 L465 534 L454 542', width=2.6)
    doc['layers'].append(ground)
    brick = layer('Viên gạch rời · có thể cho rơi')
    p(brick, 'M719 200 L790 196 L792 233 L722 238 Z', '#d58b62')
    p(brick, 'M719 200 L735 188 L804 184 L790 196 M790 196 L804 184 L807 222 L792 233', '#e7b084', 3)
    doc['layers'].append(brick)
    # Water route is authored separately so it can be revealed by a director later.
    water = layer('Đường nước · tách riêng')
    p(water, 'M546 574 Q560 564 571 575 Q582 586 597 575 Q610 563 625 575 Q638 587 653 575', width=3.5, stroke='#326dc9')
    p(water, 'M602 563 L602 461 Q600 448 612 448 L770 448 Q784 448 784 433 L784 361 Q783 349 797 350 L945 350 Q958 350 959 338 L959 226', width=4, stroke='#326dc9')
    p(water, 'M946 242 L959 226 L972 242', width=4, stroke='#326dc9')
    doc['layers'].append(water)
    mark = layer('Câu hỏi · tách riêng')
    p(mark, 'M968 184 Q968 166 986 166 Q1004 166 1003 183 Q1003 193 987 200 L987 211', width=4.5, stroke='#d74d43')
    p(mark, 'M987 225 L987 226', width=6, stroke='#d74d43')
    doc['layers'].append(mark)
    title = layer('Chữ chú giải')
    for text, at, size, bold, color in [
        ('Nước lên cao bằng cách nào?', [414, 117], 35, True, INK),
        ('Một sơ đồ để giải thích một câu hỏi.', [415, 154], 22, False, '#727870'),
        ('CHUẨN THAM CHIẾU  /  NHÂN VẬT 02', [80, 77], 15, True, '#40827e'),
        ('Nhân vật giữ tĩnh', [126, 618], 19, False, '#727870'),
        ('Minh họa nguyên lý · chưa phải phục dựng lịch sử', [501, 618], 18, False, '#727870')]:
        title['items'].append(dict(kind='text', text=text, at=at, size=size, bold=bold, stroke=color))
    doc['layers'].append(title)
    return doc
