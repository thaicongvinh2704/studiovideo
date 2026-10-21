"""Editable vector drawings. Coordinates, paths and paint only; no image generation."""
import copy
import html
import json
import math
import re
from pathlib import Path

from PySide6.QtCore import Qt, QPointF, QRectF
from PySide6.QtGui import QColor, QFont, QFontMetricsF, QPainterPath, QPen, QImage, QPainter

INK = '#252b2d'
PALETTE = [INK, '#ffffff', '#f3cfaa', '#40827e', '#d9e8e3', '#d58b62', '#b9b9b2', '#326dc9', '#d74d43']


def document():
    return dict(format='studio-drawing', version=1, width=1280, height=720,
                style='explainer-reference-v1', layers=[dict(layer('Nét vẽ 1'), role='unclassified')])


def layer(name):
    from .project import uid
    return dict(id=uid(), name=name, role='object', visible=True, offset=[0, 0], items=[])


def path_commands(data):
    """Small authoring syntax: explicit absolute M/L/Q/C/Z commands."""
    tokens = re.findall(r'[MLQCZ]|[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?', data)
    counts = dict(M=2, L=2, Q=4, C=6, Z=0)
    result = []
    while tokens:
        op = tokens.pop(0)
        if op not in counts:
            raise ValueError('Lệnh đường nét không hợp lệ: ' + op)
        n = counts[op]
        result.append([op, *[float(tokens.pop(0)) for _ in range(n)]])
    return result


def path_item(data, fill='none', stroke=INK, width=3.5):
    return dict(kind='path', commands=path_commands(data), fill=fill, stroke=stroke, width=width)


def stroke_item(points, color=INK, width=3.5, fill='none', closed=False):
    # Quadratic midpoint smoothing retains the actual endpoints and pen trajectory.
    points = [list(map(float, p[:2])) for p in points]
    if not points:
        return path_item('')
    commands = [['M', *points[0]]]
    if len(points) == 1:
        commands.append(['L', points[0][0] + .01, points[0][1]])
    for a, b in zip(points[1:-1], points[2:]):
        commands.append(['Q', *a, (a[0] + b[0]) / 2, (a[1] + b[1]) / 2])
    if len(points) > 1:
        commands.append(['L', *points[-1]])
    if closed:
        commands.append(['Z'])
    return dict(kind='path', commands=commands, fill=fill if closed else 'none', stroke=color, width=width)


def painter_path(item):
    p = QPainterPath()
    for op, *args in item.get('commands', []):
        if op == 'M': p.moveTo(*args)
        elif op == 'L': p.lineTo(*args)
        elif op == 'Q': p.quadTo(*args)
        elif op == 'C': p.cubicTo(*args)
        elif op == 'Z': p.closeSubpath()
    return p


def text_font(item):
    font = QFont('Segoe UI')
    font.setPixelSize(int(item.get('size', 28)))
    font.setBold(item.get('bold', False))
    return font


def item_bounds(item):
    if item['kind'] == 'text':
        return QFontMetricsF(text_font(item)).boundingRect(item['text']).translated(*item['at'])
    margin = item.get('width', 3.5) / 2 + 1
    return painter_path(item).boundingRect().adjusted(-margin, -margin, margin, margin)


def layer_bounds(entry):
    bounds = QRectF()
    for item in entry['items']:
        bounds = bounds.united(item_bounds(item))
    return bounds.translated(*entry.get('offset', [0, 0]))


def paint_layer(painter, entry):
    if not entry.get('visible', True):
        return
    painter.save()
    painter.translate(*entry.get('offset', [0, 0]))
    for item in entry['items']:
        color = item.get('stroke', INK)
        if item['kind'] == 'text':
            painter.setPen(QColor(color)); painter.setFont(text_font(item))
            painter.drawText(QPointF(*item['at']), item['text'])
        else:
            painter.setPen(QPen(QColor(color), item.get('width', 3.5), Qt.PenStyle.SolidLine,
                                Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
                           if color != 'none' else Qt.PenStyle.NoPen)
            fill = item.get('fill', 'none')
            painter.setBrush(QColor(fill) if fill != 'none' else Qt.BrushStyle.NoBrush)
            painter.drawPath(painter_path(item))
    painter.restore()


def render(doc, width=None):
    width = width or doc['width']
    scale = width / doc['width']
    image = QImage(width, round(doc['height'] * scale), QImage.Format.Format_ARGB32_Premultiplied)
    image.fill(QColor('white'))
    p = QPainter(image)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.scale(scale, scale)
    for entry in doc['layers']:
        if entry.get('draft'): continue
        paint_layer(p, entry)
    p.end()
    return image


def svg(doc, entries=None, crop=False):
    entries = [e for e in (entries if entries is not None else doc['layers']) if e.get('visible', True) and not e.get('draft')]
    bounds = QRectF(0, 0, doc['width'], doc['height'])
    if crop:
        bounds = QRectF()
        for entry in entries:
            bounds = bounds.united(layer_bounds(entry))
        if bounds.isEmpty(): bounds = QRectF(0, 0, 1, 1)
        bounds = bounds.adjusted(-2, -2, 2, 2)
    n = lambda v: format(float(v), '.5f').rstrip('0').rstrip('.') or '0'
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{n(bounds.width())}" height="{n(bounds.height())}" viewBox="{n(bounds.x())} {n(bounds.y())} {n(bounds.width())} {n(bounds.height())}">']
    for entry in entries:
        dx, dy = entry.get('offset', [0, 0])
        out.append(f'<g id="{html.escape(entry["id"], quote=True)}" transform="translate({n(dx)} {n(dy)})">')
        for item in entry['items']:
            stroke = html.escape(item.get('stroke', INK), quote=True)
            if item['kind'] == 'text':
                x, y = item['at']
                out.append(f'<text x="{n(x)}" y="{n(y)}" font-family="Segoe UI" font-size="{n(item.get("size",28))}" font-weight="{700 if item.get("bold") else 400}" fill="{stroke}">{html.escape(item["text"])}</text>')
            else:
                d = ' '.join(c[0] + ' '.join(n(v) for v in c[1:]) for c in item['commands'])
                fill = html.escape(item.get('fill', 'none'), quote=True)
                out.append(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{n(item.get("width",3.5))}" stroke-linecap="round" stroke-linejoin="round"/>')
        out.append('</g>')
    out.append('</svg>')
    return '\n'.join(out), bounds


def validate(doc):
    if doc.get('format') != 'studio-drawing' or doc.get('version') != 1:
        raise ValueError('Đây không phải bản vẽ Studio phiên bản 1.')
    if not all(isinstance(doc.get(k), (int, float)) and math.isfinite(doc[k]) and 64 <= doc[k] <= 7680 for k in ('width', 'height')):
        raise ValueError('Kích thước bản vẽ không hợp lệ.')
    if not doc.get('layers') or len(doc['layers']) > 500:
        raise ValueError('Bản vẽ cần từ 1 đến 500 lớp.')
    counts = dict(M=2, L=2, Q=4, C=6, Z=0)
    seen = set()
    for entry in doc['layers']:
        from .drawing_edit import validate_guides
        validate_guides(entry)
        if entry['id'] in seen: raise ValueError('ID lớp bị trùng.')
        seen.add(entry['id'])
        if len(entry.get('offset', [0, 0])) != 2 or not all(math.isfinite(v) for v in entry.get('offset', [0, 0])):
            raise ValueError('Vị trí lớp không hợp lệ.')
        for item in entry['items']:
            if item['kind'] == 'text':
                if len(item['at']) != 2 or not all(math.isfinite(v) for v in item['at']): raise ValueError('Vị trí chữ không hợp lệ.')
                if not 6 <= item.get('size', 28) <= 300: raise ValueError('Cỡ chữ không hợp lệ.')
            elif item['kind'] == 'path':
                if not 0 < item.get('width', 3.5) <= 100: raise ValueError('Cỡ bút không hợp lệ.')
                for op, *args in item['commands']:
                    if op not in counts or len(args) != counts[op] or not all(math.isfinite(v) for v in args):
                        raise ValueError('Đường nét không hợp lệ.')
            else: raise ValueError('Loại nét không được hỗ trợ.')
    return doc


def save_drawing(doc, filename):
    validate(doc)
    path = Path(filename); path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding='utf-8')
    tmp.replace(path)


def scene_layers(doc, root, start=0, end=15):
    """Each semantic layer becomes an independently directable vector asset."""
    from .explainer import image_item
    from .project import uid
    from .character_qc import drawing_issues, is_character, materialize_evidence
    validate(doc)
    issues = drawing_issues(doc, root)
    if issues: raise ValueError('Bản vẽ chưa đạt QC bắt buộc:\n' + '\n'.join(issues))
    folder = Path(root) / 'assets' / 'drawings'; folder.mkdir(parents=True, exist_ok=True)
    objects = []
    for index, entry in enumerate(doc['layers']):
        if not entry.get('visible', True) or entry.get('draft') or not entry['items']: continue
        content, bounds = svg(doc, [entry], crop=True)
        filename = folder / (uid() + '.svg')
        filename.write_text(content, encoding='utf-8')
        obj = image_item(filename.relative_to(root).as_posix(), bounds.center().x(), bounds.center().y(), bounds.width(), bounds.height())
        source = copy.deepcopy(doc); source['layers'] = [copy.deepcopy(entry)]
        if is_character(entry): materialize_evidence(source['layers'][0], root)
        obj.update(name=entry['name'], start=start, end=end, layer=20 + index, drawing_doc=source,
                   role='character' if is_character(entry) else entry.get('role', 'object'))
        objects.append(obj)
    return objects
