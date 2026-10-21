"""Mandatory, revision-bound character QC. Geometry is NOT visual judgement."""
import copy
import hashlib
import json
import math
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QColor, QFont, QImage, QPainter

ROOT = Path(sys.executable).parent if getattr(sys, 'frozen', False) else Path(__file__).resolve().parents[1]
STYLE = ROOT / 'assets' / 'styles' / 'explainer_reference_v1'
PROFILE = 'explainer-reference-v1'
CHECKS = {
    'reference_style': 'Đối chiếu đúng cả ba ảnh tham chiếu',
    'proportions': 'Tỷ lệ đầu, cổ, vai và thân tự nhiên theo mẫu',
    'face_hair': 'Mặt đủ nét; tóc có cấu trúc và hướng',
    'left_hand': 'Tay trái có lòng bàn tay, ngón cái và ngón hợp tư thế',
    'right_hand': 'Tay phải có lòng bàn tay, ngón cái và ngón hợp tư thế',
    'limb_connections': 'Vai, khuỷu, cổ tay và chân nối hợp lý',
    'clothing': 'Cổ áo, tay áo, gấu áo, quần và giày hoàn thiện',
    'line_fill': 'Viền sạch, vùng tô kín, không đúp nét hoặc rò màu',
    'identity': 'Nhận diện và mức hoàn thiện nhất quán',
    'small_size': 'Mặt, dáng và bàn tay vẫn đọc được khi thu nhỏ',
    'crop_overlap': 'Không crop hoặc dùng vật che để giấu lỗi',
    'static_delivery': 'Nhân vật tĩnh, phù hợp bố cục minh họa'
}
BASE_PARTS = {'head', 'hair', 'ear_left', 'ear_right', 'brow_left', 'brow_right',
              'eye_left', 'eye_right', 'nose', 'mouth', 'neck', 'torso',
              'sleeve_left', 'sleeve_right', 'upper_arm_left', 'upper_arm_right',
              'forearm_left', 'forearm_right', 'hand_left', 'hand_right',
              'fingers_left', 'fingers_right'}
LOWER_PARTS = {'leg_left', 'leg_right', 'shoe_left', 'shoe_right'}
LANDMARKS = {'head_top', 'chin', 'head_left', 'head_right', 'shoulder_left',
             'shoulder_right', 'neck_base', 'waist', 'elbow_left', 'elbow_right',
             'wrist_left', 'wrist_right'}


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')).hexdigest()


def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def rejected_characters():
    path = STYLE / 'rejected_characters.json'
    return json.loads(path.read_text(encoding='utf-8')).get('rejections', []) if path.exists() else []


def reference_manifest():
    manifest = json.loads((STYLE / 'manifest.json').read_text(encoding='utf-8'))
    for entry in manifest['references']:
        if file_hash(STYLE / entry['file']) != entry['sha256']:
            raise ValueError('Ảnh chuẩn đã đổi hoặc hỏng: ' + entry['file'])
    return manifest


def is_character(entry):
    name = entry.get('name', '').casefold()
    return entry.get('role') == 'character' or bool(entry.get('character')) or any(s in name for s in ('nhân vật', 'người dẫn', 'person', 'presenter'))


def source_hash(entry):
    # Moving/renaming a reviewed drawing does not change the artwork. Editing paths does.
    return digest(dict(items=entry.get('items', []), character=entry.get('character', {}), profile=PROFILE))


def parts(entry):
    result = {}
    for item in entry.get('items', []):
        for name in item.get('parts', [item.get('part', '')]):
            if name: result.setdefault(name, []).append(item)
    return result


def geometry_issues(entry):
    from .drawing import painter_path, item_bounds
    issues = []
    meta = entry.get('character', {})
    if meta.get('profile') != PROFILE: issues.append('Chưa gắn chuẩn ba ảnh reference-v1.')
    view = meta.get('view')
    if view not in ('full_body', 'waist_up'): issues.append('Khai báo toàn thân hoặc bán thân.')
    bypart = parts(entry)
    required = BASE_PARTS | (LOWER_PARTS if view == 'full_body' else set())
    hidden = meta.get('occlusions', {})
    for name in sorted(required - set(bypart)):
        detail = hidden.get(name, {})
        # A hand cannot disappear behind a generic "occluded" flag.
        if len(detail.get('reason', '').strip()) < 16 or detail.get('occluder') not in bypart:
            issues.append('Thiếu phần hoàn thiện: ' + name)
    for name in ('head', 'hair', 'torso', 'hand_left', 'hand_right'):
        for item in bypart.get(name, []):
            commands = item.get('commands', [])
            if item.get('kind') != 'path' or not commands or commands[-1][0] != 'Z' or item.get('fill', 'none') == 'none':
                issues.append('Đường bao phải khép và tô hoàn chỉnh: ' + name)
    landmarks = meta.get('landmarks', {})
    required_marks = LANDMARKS | ({'foot_left', 'foot_right'} if view == 'full_body' else set())
    if not required_marks <= landmarks.keys():
        issues.append('Thiếu mốc cơ thể: ' + ', '.join(sorted(required_marks - landmarks.keys())))
        return issues
    if any(not isinstance(pt, list) or len(pt) != 2 or not all(isinstance(v, (float, int)) and math.isfinite(v) for v in pt) for pt in landmarks.values()):
        return issues + ['Mốc cơ thể không hợp lệ.']
    top, chin = landmarks['head_top'][1], landmarks['chin'][1]
    head_h = chin - top
    head_w = math.dist(landmarks['head_left'], landmarks['head_right'])
    shoulder = math.dist(landmarks['shoulder_left'], landmarks['shoulder_right'])
    if head_h <= 0 or head_w <= 0: return issues + ['Kích thước đầu không hợp lệ.']
    if not .72 <= head_w/head_h <= 1.05: issues.append('Đầu quá dài/hẹp hoặc quá bẹt so với khoảng thử reference.')
    if not 1.15 <= shoulder/head_w <= 1.7: issues.append('Vai và đầu ngoài khoảng tỷ lệ reference.')
    if not top < chin < landmarks['neck_base'][1] < landmarks['waist'][1]: issues.append('Thứ tự đầu–cằm–cổ–eo không hợp lý.')
    if view == 'full_body':
        total = max(landmarks['foot_left'][1], landmarks['foot_right'][1]) - top
        if not 2.6 <= total/head_h <= 3.5: issues.append('Toàn thân ngoài khoảng 2.6–3.5 đầu của chuẩn thử.')
    for name in ('eye_left', 'eye_right', 'brow_left', 'brow_right', 'nose', 'mouth'):
        for item in bypart.get(name, []):
            r = item_bounds(item)
            head = QRectF()
            for face in bypart.get('head', []): head = head.united(painter_path(face).boundingRect())
            if not head.adjusted(-3, -3, 3, 3).contains(r): issues.append('Nét mặt nằm ngoài khuôn mặt: ' + name)
    for key in ('face', 'hand_left', 'hand_right'):
        region = meta.get('review_regions', {}).get(key)
        if not region or len(region) != 4 or not all(isinstance(v, (int, float)) and math.isfinite(v) for v in region) or min(region[2:]) <= 0:
            issues.append('Thiếu vùng ảnh QC: ' + key)
        elif key.startswith('hand'):
            for item in bypart.get(key, []):
                if not QRectF(*region).contains(item_bounds(item)): issues.append('Vùng QC cắt bàn tay: ' + key)
    return issues


def isolated_image(entry, rect, width):
    from .drawing import paint_layer
    image = QImage(width, max(1, round(width*rect.height()/rect.width())), QImage.Format.Format_ARGB32_Premultiplied)
    image.fill(QColor('white'))
    p = QPainter(image); p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.scale(width/rect.width(), width/rect.width()); p.translate(-rect.x(), -rect.y())
    local = copy.deepcopy(entry); local.update(visible=True, offset=[0, 0])
    paint_layer(p, local); p.end()
    return image


def prepare_packet(entry, root):
    """Render evidence only. This NEVER marks anything passed."""
    from .drawing import layer_bounds
    manifest = reference_manifest(); root = Path(root).resolve()
    folder = root / 'qc' / 'characters' / source_hash(entry)[:20]; folder.mkdir(parents=True, exist_ok=True)
    local = copy.deepcopy(entry); local['offset'] = [0, 0]
    rect = layer_bounds(local).adjusted(-14, -14, 14, 14)
    if rect.isEmpty(): raise ValueError('Nhân vật chưa có hình để QC.')
    prefix = source_hash(entry)[:12]
    evidence = []
    def record(kind, image):
        path = folder / (prefix + '_' + kind + '.png')
        if not image.save(str(path)): raise OSError('Không ghi được ảnh QC: ' + str(path))
        evidence.append(dict(kind=kind, file=path.relative_to(root).as_posix(), sha256=file_hash(path)))
        return image
    full = record('full', isolated_image(entry, rect, 600))
    record('thumbnail', isolated_image(entry, rect, 180))
    for key in ('face', 'hand_left', 'hand_right'):
        region = entry.get('character', {}).get('review_regions', {}).get(key)
        if region: record(key, isolated_image(entry, QRectF(*region), 460))
    board = QImage(1600, 940, QImage.Format.Format_ARGB32_Premultiplied); board.fill(QColor('white'))
    p = QPainter(board); p.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
    font = QFont('Segoe UI'); font.setPixelSize(22); font.setBold(True); p.setFont(font); p.setPen(QColor('#252b2d'))
    p.drawText(35, 42, 'QC NHÂN VẬT  /  ĐỐI CHIẾU BA ẢNH NGƯỜI DÙNG')
    sources = [full]
    for i, reference in enumerate(manifest['references'], 1):
        original = STYLE / reference['file']; target = folder / ('reference_0' + str(i) + '.png')
        shutil.copy2(original, target)
        evidence.append(dict(kind='reference_0' + str(i), file=target.relative_to(root).as_posix(), sha256=file_hash(target)))
        sources.append(QImage(str(original)).copy(*reference['person_crop']))
    for i, image in enumerate(sources):
        fit = image.scaled(350, 750, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        x = 25 + i*395; p.drawText(x, 90, 'BẢN ĐANG KIỂM TRA' if i == 0 else 'THAM CHIẾU ' + str(i))
        p.drawImage(x + (350-fit.width())//2, 125, fit)
    font.setPixelSize(17); font.setBold(False); p.setFont(font)
    p.drawText(35, 900, 'Chỉ là hồ sơ kiểm tra. Ảnh chụp tham chiếu không phải asset phim. QC nội bộ không thay việc người dùng nhận xét.')
    p.end(); record('comparison', board)
    entry['qc_packet'] = dict(source_sha256=source_hash(entry), reference_sha256=digest(manifest), evidence=evidence)
    return entry['qc_packet']


def resolve_evidence(root, value):
    path = Path(value)
    if path.is_absolute(): return path
    local = Path(root) / path
    return local if local.is_file() else ROOT / path


def review_issues(entry, root):
    issues = geometry_issues(entry)
    for rejected in rejected_characters():
        if rejected.get('source_sha256') == source_hash(entry) or (
            rejected.get('identity') and rejected['identity'] == entry.get('character', {}).get('identity')):
            issues.append('Mẫu nhân vật đã bị người dùng loại; QC cũ bị thu hồi. ' + rejected.get('reason', ''))
    qc = entry.get('character_qc', {})
    if qc.get('status') != 'passed': return issues + ['Chưa hoàn thành QC trực quan nhân vật.']
    if qc.get('source_sha256') != source_hash(entry): issues.append('Nét nhân vật đã đổi sau QC; phải xem và QC lại.')
    try:
        if qc.get('reference_sha256') != digest(reference_manifest()): issues.append('QC dùng bộ reference khác.')
    except (OSError, ValueError) as exc: issues.append(str(exc))
    reviews = qc.get('checks', {})
    for key, title in CHECKS.items():
        decision = reviews.get(key, {})
        if decision.get('pass') is not True or len(decision.get('note', '').strip()) < 20:
            issues.append('Chưa kiểm tra có nhận xét: ' + title)
    kinds = set()
    for evidence in qc.get('evidence', []):
        kinds.add(evidence.get('kind'))
        path = resolve_evidence(root, evidence.get('file', ''))
        if not path.is_file() or file_hash(path) != evidence.get('sha256'):
            issues.append('Ảnh QC thiếu hoặc đã đổi: ' + evidence.get('kind', '?'))
    if not {'full', 'face', 'hand_left', 'hand_right', 'thumbnail', 'comparison', 'reference_01', 'reference_02', 'reference_03'} <= kinds:
        issues.append('Thiếu ảnh toàn hình/mặt/hai tay/ảnh nhỏ/bảng so sánh hoặc reference.')
    if not qc.get('reviewer') or not qc.get('reviewed_at'): issues.append('Thiếu người kiểm tra hoặc thời điểm QC.')
    return issues


def record_review(entry, root, checks, reviewer):
    """Call only AFTER opening and evaluating the current evidence. No auto-pass path."""
    packet = entry.get('qc_packet', {})
    if packet.get('source_sha256') != source_hash(entry): raise ValueError('Tạo lại ảnh QC cho nét hiện tại trước.')
    if not reviewer.strip(): raise ValueError('Ghi tên người kiểm tra.')
    candidate = copy.deepcopy(packet)
    candidate.update(status='passed', checks=copy.deepcopy(checks), reviewer=reviewer.strip(),
                     reviewed_at=datetime.now(timezone.utc).isoformat(), scope='Internal visual QC, not user approval')
    entry['character_qc'] = candidate
    issues = review_issues(entry, root)
    if issues:
        entry['character_qc'] = dict(candidate, status='failed', failures=issues)
        raise ValueError('\n'.join(issues))
    entry.pop('qc_packet', None)
    return candidate


def materialize_evidence(entry, root):
    """Keep evidence portable when a reviewed model is inserted into another project."""
    root = Path(root).resolve(); folder = root / 'assets' / 'character_qc'; folder.mkdir(parents=True, exist_ok=True)
    for evidence in entry.get('character_qc', {}).get('evidence', []):
        source = resolve_evidence(root, evidence['file'])
        target = folder / (evidence['sha256'][:16] + '_' + Path(evidence['file']).name)
        if source.resolve() != target.resolve(): shutil.copy2(source, target)
        evidence['file'] = target.relative_to(root).as_posix()


def drawing_issues(doc, root):
    result = []
    for entry in doc['layers']:
        if not entry.get('visible', True) or entry.get('draft') or not entry['items']: continue
        if entry.get('role') not in ('object', 'character'): result.append(entry['name'] + ': Chọn lớp vật thể hoặc nhân vật trước khi đưa vào cảnh.')
        if is_character(entry):
            result.extend(entry['name'] + ': ' + message for message in review_issues(entry, root))
    return result


def object_issues(obj, root):
    from .drawing import svg
    if obj.get('character_library') == 'mo_den':
        from .supplied_character import source_issues
        return source_issues(obj, root)
    if obj.get('kind') == 'character':
        return ['Người dẫn/nhân vật rig cũ chưa qua chuẩn QC tĩnh reference-v1. Thay bằng bản vẽ đã QC.']
    doc = obj.get('drawing_doc')
    if not doc: return ['Nhân vật chưa có bản vẽ và QC.'] if obj.get('role') == 'character' else []
    issues = drawing_issues(doc, root)
    if any(is_character(e) for e in doc['layers']):
        actual = Path(root) / obj.get('file', '')
        expected, _ = svg(doc, crop=True)
        # Normalize the platform's CRLF/LF text encoding, not the path geometry.
        if not actual.is_file() or actual.read_text(encoding='utf-8') != expected:
            issues.append('SVG nhân vật khác bản nét đã QC; cần xuất/QC lại.')
    return issues


def project_issues(project, root):
    problems = []
    for scene in project['scenes']:
        for obj in scene['objects']:
            for message in object_issues(obj, root):
                problems.append(dict(level='error', code='character_qc', scene=scene['name'], object_id=obj['id'], message=obj.get('name', 'Nhân vật') + ': ' + message))
            if obj.get('character_library') == 'mo_den':
                from .supplied_character import framing_issues
                for message in framing_issues(obj, scene):
                    problems.append(dict(level='error', code='cat_framing', scene=scene['name'], object_id=obj['id'], message=message))
    return problems


def require_project_qc(project, root):
    problems = project_issues(project, root)
    if problems: raise ValueError('Nhân vật chưa đạt QC bắt buộc:\n' + '\n'.join(p['message'] for p in problems))
