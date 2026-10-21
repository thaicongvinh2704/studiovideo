"""Source and framing checks for the user's indexed Mỏ Đen PNGs.

These checks establish file identity and framing, not aesthetic approval.
The human drawing review continues to use character_qc unchanged.
"""
import hashlib
import json
import math
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIBRARY = ROOT / 'assets/characters/mo_den'


@lru_cache(maxsize=96)
def _sha(path, size, modified):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def source_issues(obj, root):
    if obj.get('role') != 'character' or obj.get('character_library') != 'mo_den':
        return ['Ảnh Mỏ Đen cần được phân loại là nhân vật từ kho mo_den.']
    manifest = json.loads((LIBRARY / 'manifest.json').read_text(encoding='utf-8'))
    entry = next((a for a in manifest['assets'] if a['id'] == obj.get('character_asset_id')), None)
    if not entry or entry.get('status') != 'technically_usable':
        return ['Ảnh Mỏ Đen chưa được chỉ mục hoặc không dùng được.']
    path = (Path(root) / obj.get('file', '')).resolve()
    if not path.is_file(): return ['Thiếu PNG Mỏ Đen: ' + str(path)]
    stat = path.stat()
    if _sha(str(path), stat.st_size, stat.st_mtime_ns) != entry['sha256']:
        return ['PNG Mỏ Đen khác ảnh gốc đã chỉ mục; cần kiểm tra lại nhận diện.']
    if entry.get('alpha_extrema') != [0, 255] or entry.get('mode') != 'RGBA':
        return ['PNG Mỏ Đen chưa được xác minh nền trong suốt.']
    w, h = obj.get('width', 0), obj.get('height', 0)
    if not w or not h or abs(w / h - entry['width'] / entry['height']) > .001:
        return ['Không được kéo méo tỷ lệ ảnh Mỏ Đen.']
    return []


def framing_issues(obj, scene):
    """Check the visible alpha bounds at keys and intermediate camera positions."""
    from .animation import state, camera_values
    from .hierarchy import world_states
    manifest = json.loads((LIBRARY / 'manifest.json').read_text(encoding='utf-8'))
    entry = next((a for a in manifest['assets'] if a['id'] == obj.get('character_asset_id')), None)
    if not entry: return []  # source_issues reports the missing identity
    start, end = obj.get('start', 0), min(obj.get('end', scene['duration']), scene['duration'])
    times = {start, max(start, end - 1e-5)}
    for frames in obj.get('keys', {}).values():
        times.update(k['t'] for k in frames if start <= k['t'] < end)
    times.update(start+(end-start)*i/12 for i in range(1, 12))
    bx, by, ex, ey = entry['alpha_bbox']
    iw, ih = entry['width'], entry['height']
    w, h = obj.get('width', 0), obj.get('height', 0)
    for t in sorted(times):
        st = world_states(scene['objects'], t)[obj['id']]
        if not st['visible'] or st['opacity'] <= .01: continue
        zoom, cx, cy = camera_values(scene, t)
        angle = math.radians(st['rotation']); c, s = math.cos(angle), math.sin(angle)
        for px, py in ((bx, by), (ex, by), (ex, ey), (bx, ey)):
            lx, ly = (px/iw-.5)*w*st['scale'], (py/ih-.5)*h*st['scale']
            x = 640 + (st['x']+lx*c-ly*s-cx)*zoom
            y = 360 + (st['y']+lx*s+ly*c-cy)*zoom
            if not (-2 <= x <= 1282 and -2 <= y <= 722):
                return ['Khung hình cắt phần thân/tai/đuôi Mỏ Đen; cần chỉnh bố cục.']
    return []
