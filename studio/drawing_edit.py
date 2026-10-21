"""Deterministic drawing operations shared by the canvas and agent CLI.

Guides are authoring aids, not animation bones or finished illustrations.
All visible geometry remains explicit in the original version-1 path format.
"""
import copy
import math

from .project import uid
from .vendor.perfect_freehand import get_stroke


def invalidate(entry):
    if 'character_qc' in entry and entry['character_qc'].get('status') != 'rejected_by_user':
        entry['character_qc']['status'] = 'stale'
    entry.pop('qc_packet', None)


def identify(entry):
    for item in entry['items']:
        item.setdefault('id', uid())


def point_refs(item):
    for ci, command in enumerate(item.get('commands', [])):
        for ai in range(1, len(command), 2):
            yield ci, ai, command[ai:ai + 2], ai == len(command) - 2


def move_node(entry, item_index, command_index, argument_index, target, _from_guide=False):
    item = entry['items'][item_index]
    if not _from_guide:
        binding = next((b for b in item.get('node_bindings', []) if
                        b['command'] == command_index and b['argument'] == argument_index), None)
        if binding:
            return move_guide(entry, binding['guide'], target)
    command = item['commands'][command_index]
    if not any(ci == command_index and ai == argument_index for ci, ai, _, _ in point_refs(item)):
        raise ValueError('Điểm điều khiển không hợp lệ.')
    if not all(math.isfinite(v) for v in target) or len(target) != 2:
        raise ValueError('Tọa độ không hợp lệ.')
    dx, dy = target[0] - command[argument_index], target[1] - command[argument_index + 1]
    command[argument_index:argument_index + 2] = list(target)
    # Moving a knot carries adjacent handles; dragging a handle is independent.
    if argument_index == len(command) - 2:
        if command[0] in ('Q', 'C'):
            command[-4] += dx; command[-3] += dy
        if command_index + 1 < len(item['commands']):
            following = item['commands'][command_index + 1]
            if following[0] in ('Q', 'C'):
                following[1] += dx; following[2] += dy
    item.pop('brush_source', None)  # Outline is now edited explicitly.
    invalidate(entry)


def split_segment(entry, item_index, ci):
    """Exact de Casteljau split at t=.5; preserves shape and endpoint handles."""
    item = entry['items'][item_index]
    if ci < 1 or ci >= len(item['commands']):
        raise ValueError('Chọn điểm cuối của đoạn cần chia.')
    c = item['commands'][ci]
    previous = item['commands'][ci - 1]
    if previous[0] == 'Z' or c[0] not in ('L', 'Q', 'C'):
        raise ValueError('Chỉ chia đoạn thẳng hoặc Bézier.')
    points = [previous[-2:]] + [c[i:i + 2] for i in range(1, len(c), 2)]
    left, right = [points[0]], [points[-1]]
    while len(points) > 1:
        points = [[(a + b) / 2 for a, b in zip(p, q)] for p, q in zip(points, points[1:])]
        left.append(points[0]); right.append(points[-1])
    a = [c[0]] + [v for p in left[1:] for v in p]
    b = [c[0]] + [v for p in list(reversed(right))[1:] for v in p]
    item['commands'][ci:ci + 1] = [a, b]
    for binding in item.get('node_bindings', []):
        if binding['command'] >= ci: binding['command'] += 1
    item.pop('brush_source', None); invalidate(entry)


def smooth_knot(entry, item_index, ci):
    item = entry['items'][item_index]
    commands = item['commands']
    if ci < 1 or ci + 1 >= len(commands) or commands[ci][0] != 'C' or commands[ci + 1][0] != 'C':
        raise ValueError('Chọn nút nối giữa hai đoạn Bézier bậc ba.')
    c, nxt = commands[ci], commands[ci + 1]
    x, y = c[-2:]; vx, vy = x - c[-4], y - c[-3]
    length = math.hypot(vx, vy)
    other = math.hypot(nxt[1] - x, nxt[2] - y)
    if length < 1e-8: raise ValueError('Tay nắm trước nút đang bằng không.')
    nxt[1:3] = [x + vx / length * other, y + vy / length * other]
    item.pop('brush_source', None); invalidate(entry)


def remove_knot(entry, item_index, ci):
    item = entry['items'][item_index]; commands = item['commands']
    if ci <= 0 or ci >= len(commands) or commands[ci][0] not in ('L', 'Q', 'C'):
        raise ValueError('Chọn nút cuối đoạn. Không xóa điểm mở đầu bằng lệnh này.')
    if sum(c[0] in ('L', 'Q', 'C') for c in commands) <= 1:
        raise ValueError('Nét cần ít nhất một đoạn. Dùng Delete để xóa cả nét.')
    commands.pop(ci)
    item['node_bindings'] = [b for b in item.get('node_bindings', []) if b['command'] != ci]
    for binding in item['node_bindings']:
        if binding['command'] > ci: binding['command'] -= 1
    item.pop('brush_source', None); invalidate(entry)


def curve_segment(entry, item_index, ci):
    item = entry['items'][item_index]; commands = item['commands']
    if ci < 1 or ci >= len(commands) or commands[ci][0] != 'L' or commands[ci - 1][0] == 'Z':
        raise ValueError('Chọn điểm cuối một đoạn thẳng.')
    a, b = commands[ci - 1][-2:], commands[ci][-2:]
    commands[ci] = ['C', *[x + (y - x) / 3 for x, y in zip(a, b)],
                   *[x + 2 * (y - x) / 3 for x, y in zip(a, b)], *b]
    for binding in item.get('node_bindings', []):
        if binding['command'] == ci: binding['argument'] = 5
    item.pop('brush_source', None); invalidate(entry)


def translate_item(item, dx, dy):
    if item['kind'] == 'text':
        item['at'] = [item['at'][0] + dx, item['at'][1] + dy]
    else:
        for command in item['commands']:
            for i in range(1, len(command), 2):
                command[i] += dx; command[i + 1] += dy
    for point in item.get('brush_source', {}).get('points', []):
        point[0] += dx; point[1] += dy


def add_guide(entry, name, point, parent=None, lock_length=False):
    if len(point) != 2 or not all(math.isfinite(v) for v in point):
        raise ValueError('Mốc phải có hai tọa độ hữu hạn.')
    guides = entry.setdefault('guides', [])
    if any(g['name'] == name for g in guides): raise ValueError('Tên mốc đã tồn tại.')
    guide = dict(id=uid(), name=name, point=list(point))
    if parent:
        origin = next((g for g in guides if g['id'] == parent), None)
        if origin is None: raise ValueError('Mốc cha không tồn tại.')
        guide['parent'] = parent
        if lock_length:
            length = math.dist(point, origin['point'])
            if length < .001: raise ValueError('Hai mốc phải khác vị trí.')
            guide['length'] = length
    guides.append(guide)
    return guide['id']


def bind_items(entry, indices, guide_id):
    if guide_id not in {g['id'] for g in entry.get('guides', [])}:
        raise ValueError('Mốc không tồn tại.')
    identify(entry)
    for i in indices:
        entry['items'][i]['guide_binding'] = guide_id
        entry['items'][i].pop('node_bindings', None)
    invalidate(entry)


def bind_node(entry, item_index, ci, ai, guide_id):
    guide = next((g for g in entry.get('guides', []) if g['id'] == guide_id), None)
    if not guide: raise ValueError('Mốc không tồn tại.')
    item = entry['items'][item_index]
    if not any(c == ci and a == ai and knot for c, a, _, knot in point_refs(item)):
        raise ValueError('Chỉ gắn nút đầu/cuối đoạn, không gắn tay nắm.')
    item.pop('guide_binding', None)
    item['node_bindings'] = [b for b in item.get('node_bindings', []) if (b['command'], b['argument']) != (ci, ai)]
    move_node(entry, item_index, ci, ai, guide['point'], _from_guide=True)
    item['node_bindings'].append(dict(command=ci, argument=ai, guide=guide_id))
    invalidate(entry)


def move_guide(entry, guide_id, target):
    """Move a guide plus descendants and their attached artwork.

    Optional fixed parent distance is a positional authoring constraint.
    Descendants translate together; no claim of automatic anatomical re-posing.
    """
    guides = {g['id']: g for g in entry.get('guides', [])}
    if guide_id not in guides: raise ValueError('Mốc không tồn tại.')
    if len(target) != 2 or not all(math.isfinite(v) for v in target): raise ValueError('Tọa độ không hợp lệ.')
    guide = guides[guide_id]; target = list(target)
    if 'length' in guide:
        parent = guides[guide['parent']]['point']
        vx, vy = target[0] - parent[0], target[1] - parent[1]
        length = math.hypot(vx, vy)
        if length < .001: return
        target = [parent[0] + vx / length * guide['length'], parent[1] + vy / length * guide['length']]
    affected = {guide_id}
    while True:
        children = {g['id'] for g in guides.values() if g.get('parent') in affected}
        if children <= affected: break
        affected.update(children)
    dx, dy = target[0] - guide['point'][0], target[1] - guide['point'][1]
    for key in affected:
        g = guides[key]; g['point'] = [g['point'][0] + dx, g['point'][1] + dy]
        marks = entry.get('character', {}).get('landmarks', {})
        if g['name'] in marks: marks[g['name']] = list(g['point'])
    for index, item in enumerate(entry['items']):
        if item.get('guide_binding') in affected:
            translate_item(item, dx, dy)
        else:
            for binding in item.get('node_bindings', []):
                if binding['guide'] in affected:
                    move_node(entry, index, binding['command'], binding['argument'],
                              guides[binding['guide']]['point'], _from_guide=True)
    invalidate(entry)


def brush_item(points, color, width, thinning=.35, smoothing=.5, pressure=False):
    options = dict(size=width, thinning=thinning, smoothing=smoothing,
                   streamline=.35, simulate_pressure=not pressure, last=True)
    outline = get_stroke(points, **options)
    commands = ([['M', *outline[0]]] + [['L', *p] for p in outline[1:]] + [['Z']]) if outline else []
    return dict(id=uid(), kind='path', commands=commands, fill=color, stroke='none', width=width,
                brush_source=dict(points=copy.deepcopy(points), options=options))


def restyle_stroke(entry, index, width, thinning=.35, smoothing=.5):
    if not 0 < width <= 100 or not 0 <= thinning <= 1 or not 0 <= smoothing <= 1:
        raise ValueError('Thông số bút ngoài phạm vi.')
    item = entry['items'][index]
    if item['kind'] != 'path': return
    source = item.get('brush_source')
    if source:
        rebuilt = brush_item(source['points'], item['fill'], width, thinning, smoothing,
                             not source['options']['simulate_pressure'])
        for key in ('commands', 'width', 'brush_source'): item[key] = rebuilt[key]
    else:
        item['width'] = width
    invalidate(entry)


def apply_command(doc, command):
    """Atomic agent API: return a validated new document, never partially mutate."""
    from .drawing import validate
    result = copy.deepcopy(doc)
    entry = result['layers'][int(command.get('layer', 0))]
    if entry.get('locked'): raise ValueError('Lớp đang khóa.')
    op = command['op']
    if op == 'add_guide':
        add_guide(entry, command['name'], command['point'], command.get('parent'), command.get('lock_length', False))
    elif op == 'move_guide':
        move_guide(entry, command['guide'], command['point'])
    elif op == 'bind_items':
        bind_items(entry, command['items'], command['guide'])
    elif op == 'bind_node':
        bind_node(entry, command['item'], command['command'], command['argument'], command['guide'])
    elif op == 'move_node':
        move_node(entry, command['item'], command['command'], command['argument'], command['point'])
    elif op == 'split_segment':
        split_segment(entry, command['item'], command['command'])
    elif op == 'smooth_knot':
        smooth_knot(entry, command['item'], command['command'])
    elif op == 'remove_knot':
        remove_knot(entry, command['item'], command['command'])
    elif op == 'curve_segment':
        curve_segment(entry, command['item'], command['command'])
    elif op == 'restyle_stroke':
        restyle_stroke(entry, command['item'], command['width'], command.get('thinning', .35), command.get('smoothing', .5))
    elif op == 'add_path':
        from .drawing import path_item
        entry['items'].append(path_item(command['path'], command.get('fill', 'none'),
                                        command.get('stroke', '#252b2d'), command.get('width', 3.5)))
        invalidate(entry)
    else:
        raise ValueError('Lệnh chưa hỗ trợ: ' + op)
    return validate(result)


def validate_guides(entry):
    guides = entry.get('guides', [])
    ids = {g.get('id') for g in guides}
    if None in ids or len(ids) != len(guides): raise ValueError('ID mốc bị thiếu hoặc trùng.')
    by_id = {g['id']: g for g in guides}
    for g in guides:
        if len(g.get('point', [])) != 2 or not all(isinstance(v, (int, float)) and math.isfinite(v) for v in g['point']):
            raise ValueError('Tọa độ mốc không hợp lệ.')
        visited = {g['id']}; parent = g.get('parent')
        while parent:
            if parent not in ids or parent in visited: raise ValueError('Mốc cha thiếu hoặc tạo vòng lặp.')
            visited.add(parent); parent = by_id[parent].get('parent')
        if 'length' in g and (not g.get('parent') or not isinstance(g['length'], (int, float)) or
                              not math.isfinite(g['length']) or g['length'] <= 0):
            raise ValueError('Độ dài liên kết không hợp lệ.')
    for item in entry['items']:
        if item.get('guide_binding') and item['guide_binding'] not in ids:
            raise ValueError('Nét đang gắn vào mốc không tồn tại.')
        valid = {(ci, ai) for ci, ai, _, knot in point_refs(item) if knot}
        bindings = item.get('node_bindings', [])
        if item.get('guide_binding') and bindings: raise ValueError('Không gắn cả nét và nút của cùng nét.')
        seen = set()
        for b in bindings:
            key = (b.get('command'), b.get('argument'))
            if key in seen or key not in valid or b.get('guide') not in ids:
                raise ValueError('Liên kết nút không hợp lệ.')
            seen.add(key)
