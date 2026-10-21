"""Versioned, portable project documents; never embeds media in JSON."""
import copy
import json
import math
import shutil
import uuid
import zipfile
from pathlib import Path

SCHEMA = 1

def uid():
    return uuid.uuid4().hex[:12]

def new_object(kind='character', preset='father', x=640, y=570):
    return dict(id=uid(), kind=kind, name=preset, preset=preset, x=x, y=y,
                scale=1., rotation=0., opacity=1., layer=10, start=0., end=15.,
                expression='normal', color='#242938', age='adult', speed=1., amplitude=1.,
                action='idle', keys={}, motions=[], attachment=[], rig={})

def new_scene(name='Cảnh mới', duration=15):
    return dict(id=uid(), name=name, start=0., duration=float(duration), background='studio',
                objects=[], effects=[], camera=dict(keys={}, follow=''), subtitle_ids=[], audio_ids=[])

def new_project(name='Dự án mới', duration=15, width=1280, height=720):
    scene = new_scene(duration=duration)
    scene['objects'].append(new_object())
    scene['objects'][0]['end'] = duration
    return dict(schema=SCHEMA, name=name, width=width, height=height, fps=24, scenes=[scene],
                subtitles=[], audio=[], references=[], subtitle_style=dict(enabled=True, size=30,
                font='Segoe UI', color='#ffffff', background=True, y=.88), duck_music=True)

def duration(project):
    return max((s['start'] + s['duration'] for s in project['scenes']), default=0.)

def scene_at(project, t):
    for s in project['scenes']:
        if s['start'] <= t < s['start'] + s['duration']:
            return s, t - s['start']
    return None, 0.

def resequence(project):
    t = 0.
    for s in project['scenes']:
        delta=t-s['start']
        for clip in project.get('audio',[])+project.get('subtitles',[]):
            if clip.get('scene_id')==s['id']:
                clip['start']+=delta
                if 'end' in clip:clip['end']+=delta
        s['start'] = t
        t += s['duration']

def validate(project):
    if project.get('schema') != SCHEMA:
        raise ValueError('Phiên bản project chưa được hỗ trợ.')
    if not (64 <= project['width'] <= 7680 and 64 <= project['height'] <= 4320):
        raise ValueError('Kích thước canvas không hợp lệ.')
    ids = set()
    for s in project['scenes']:
        if not math.isfinite(s['duration']) or s['duration'] <= 0 or s['start'] < 0:
            raise ValueError('Thời lượng hoặc thời điểm cảnh không hợp lệ.')
        for o in s['objects']:
            if o['id'] in ids:
                raise ValueError('ID đối tượng bị trùng.')
            ids.add(o['id'])
        from .hierarchy import world_states
        world_states(s['objects'],0)
    for cue in project['subtitles']:
        if cue['start'] < 0 or cue['end'] <= cue['start']:
            raise ValueError('Timestamp phụ đề không hợp lệ.')

def media_entries(project):
    for s in project['scenes']:
        if s.get('background_file'):
            yield s, 'background_file'
        for o in s['objects']:
            if o.get('file'):
                yield o, 'file'
            for entry in o.get('drawing_doc',{}).get('layers',[]):
                for evidence in entry.get('character_qc',{}).get('evidence',[]):
                    if evidence.get('file'):yield evidence,'file'
    for a in project['audio'] + project.get('references', []):
        yield a, 'file'
    board=project.get('storyboard',{})
    if board.get('voice'):yield board,'voice'
    for row in board.get('rows',[]):
        for i in range(len(row.get('assets',[]))):yield row['assets'],i
        for obj in row.get('objects',[]):
            if obj.get('file'):yield obj,'file'

def resolve(root, relative):
    p = Path(relative)
    if p.is_absolute():
        return p
    return Path(root) / p

def missing(project, root):
    return [str(resolve(root, o[k])) for o, k in media_entries(project) if not resolve(root, o[k]).is_file()]

def save(project, path, source_root=None):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = copy.deepcopy(project)
    for o, k in media_entries(data):
        source = resolve(source_root or path.parent, o[k])
        if source.is_file():
            assets = path.parent / 'assets'
            assets.mkdir(exist_ok=True)
            dest = assets / source.name
            if dest.resolve() != source.resolve():
                if dest.exists() and dest.read_bytes() != source.read_bytes():
                    dest = assets / (uid() + '_' + source.name)
                shutil.copy2(source, dest)
            o[k] = dest.relative_to(path.parent).as_posix()
    validate(data)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    tmp.replace(path)
    return data

def load(path):
    data = json.loads(Path(path).read_text(encoding='utf-8-sig'))
    validate(data)
    return data

def pack(project, root, output):
    with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('project.json', json.dumps(project, ensure_ascii=False, indent=2))
        added=set()
        for o, k in media_entries(project):
            p = resolve(root, o[k])
            if not p.is_file():
                raise FileNotFoundError(p)
            rel = Path(o[k])
            if rel.is_absolute() or '..' in rel.parts:
                raise ValueError('Hãy lưu project để chuyển asset sang đường dẫn tương đối trước.')
            if rel.as_posix() not in added:z.write(p, rel.as_posix());added.add(rel.as_posix())

def unpack(package, folder):
    folder = Path(folder).resolve()
    if (folder / 'project.json').exists():
        raise ValueError('Chọn thư mục mới để không ghi đè project hiện có.')
    with zipfile.ZipFile(package) as z:
        if sum(i.file_size for i in z.infolist()) > 8 * 1024**3:
            raise ValueError('Gói project quá lớn.')
        for item in z.infolist():
            target = (folder / item.filename).resolve()
            if not target.is_relative_to(folder):
                raise ValueError('Gói có đường dẫn không an toàn.')
        z.extractall(folder)
    return folder / 'project.json'

class History:
    def __init__(self):
        self.undo_stack, self.redo_stack = [], []

    def push(self, project):
        self.undo_stack.append(copy.deepcopy(project))
        self.undo_stack = self.undo_stack[-60:]
        self.redo_stack.clear()

    def undo(self, project):
        if not self.undo_stack:
            return project
        self.redo_stack.append(copy.deepcopy(project))
        return self.undo_stack.pop()

    def redo(self, project):
        if not self.redo_stack:
            return project
        self.undo_stack.append(copy.deepcopy(project))
        return self.redo_stack.pop()
