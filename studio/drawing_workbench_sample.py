"""A tool exercise with objects only; no unapproved character master."""
from .drawing import document, layer, path_item, INK
from .drawing_edit import add_guide, bind_items, brush_item


def workbench_document():
    doc = document(); doc['layers'] = []
    title = layer('Hướng dẫn bài tập')
    for text, at, size, color in [
        ('BÀN VẼ STUDIO', [65, 70], 22, '#168d83'),
        ('Dựng hình. Chỉnh nét. Giữ phong cách.', [65, 120], 34, INK),
        ('Bài tập công cụ · vật thể vector · không phải mẫu nhân vật', [65, 158], 18, '#6c7774'),
        ('01 / SỬA ĐƯỜNG CONG', [65, 237], 18, '#168d83'),
        ('Chọn bình → Sửa nút → kéo điểm / tay nắm', [65, 605], 17, '#6c7774'),
        ('02 / DI CHUYỂN THEO MỐC', [660, 237], 18, '#168d83'),
        ('Chọn lớp Cụm gạch → Mốc → kéo “gach”', [660, 605], 17, '#6c7774'),
        ('Cuộn để phóng to  •  Chuột giữa để kéo  •  F để vừa khung', [65, 680], 18, '#6c7774'),
    ]:
        title['items'].append(dict(kind='text', text=text, at=at, size=size, stroke=color))
    title['locked'] = True
    vase = layer('Bình gốm · chỉnh Bézier')
    vase['items'] = [
        path_item('M242 295 C244 330 227 350 201 385 C179 414 178 470 202 503 C229 538 331 538 358 503 C381 471 380 414 358 385 C332 350 315 330 318 295 Z', '#d79b75', INK, 3.4),
        path_item('M242 295 C255 286 303 286 318 295 C307 306 254 307 242 295 Z', '#f1c49d', INK, 3),
        path_item('M214 403 C234 420 323 422 346 403 M204 431 C230 450 327 452 356 432', 'none', '#875d48', 2.6),
        path_item('M215 472 C229 490 252 494 268 495', 'none', '#efd1b6', 5),
        path_item('M164 540 C230 545 334 547 396 540', 'none', '#7b827c', 2),
    ]
    vase_anchor = add_guide(vase, 'binh', [280, 400])
    bind_items(vase, list(range(4)), vase_anchor)
    brick = layer('Cụm gạch · kéo mốc')
    brick['items'] = [
        path_item('M728 408 C832 405 932 410 1038 407 L1035 523 C934 527 829 525 727 522 Z', '#cf8b60', INK, 3.4),
        path_item('M728 408 L768 372 C873 369 979 372 1078 370 L1038 407 Z', '#e6b18a', INK, 3.4),
        path_item('M1038 407 L1078 370 L1076 485 L1035 523 Z', '#b77550', INK, 3.4),
        path_item('M729 465 C827 462 932 467 1036 464 M824 408 L823 463 M929 409 L931 465 M776 465 L778 523 M881 465 L879 524 M983 464 L982 524', 'none', '#624c40', 2.5),
        path_item('M696 538 C827 544 990 542 1107 538', 'none', '#7b827c', 2),
    ]
    ground = add_guide(brick, 'goc', [728, 523])
    anchor = add_guide(brick, 'gach', [900, 430], parent=ground, lock_length=True)
    bind_items(brick, list(range(4)), anchor)
    ink_layer = layer('Nét bút đậm nhạt · sửa độc lập')
    ink_layer['items'].append(brush_item([[726, 313, .1], [772, 292, .45], [820, 314, .85],
                                          [872, 293, .65], [922, 314, .3], [973, 294, .1]], '#326dc9', 7, .65, .5, True))
    doc['layers'] = [vase, brick, ink_layer, title]
    return doc
