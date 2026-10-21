import re
from pathlib import Path
from .project import uid

def seconds(value):
    m = re.fullmatch(r'(\d+):(\d{2}):(\d{2})[,.](\d{3})', value.strip())
    if not m:
        raise ValueError('Timestamp phải có dạng 00:00:05,000: ' + value)
    h, minute, sec, ms = map(int, m.groups())
    if minute > 59 or sec > 59:
        raise ValueError('Phút và giây phải nhỏ hơn 60.')
    return h * 3600 + minute * 60 + sec + ms / 1000

def stamp(t):
    ms = round(max(0, t) * 1000)
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f'{h:02}:{m:02}:{s:02},{ms:03}'

def parse(text):
    cues = []
    for block in re.split(r'\n\s*\n', text.lstrip('\ufeff').replace('\r', '').strip()):
        lines = block.splitlines()
        if not lines:
            continue
        if '-->' not in lines[0]:
            lines = lines[1:]
        if len(lines) < 2 or '-->' not in lines[0]:
            raise ValueError('Cue SRT thiếu timestamp hoặc nội dung.')
        start, end = lines[0].split('-->', 1)
        a, b = seconds(start), seconds(end.strip().split()[0])
        if b <= a:
            raise ValueError('Cue SRT có thời điểm kết thúc <= bắt đầu.')
        cues.append(dict(id=uid(), start=a, end=b, text='\n'.join(lines[1:]), role='Narrator'))
    return sorted(cues, key=lambda c: c['start'])

def read(path):
    return parse(Path(path).read_text(encoding='utf-8-sig'))

def write(cues, path):
    Path(path).write_text('\n\n'.join(f"{i+1}\n{stamp(c['start'])} --> {stamp(c['end'])}\n{c['text']}"
                                      for i, c in enumerate(cues)) + '\n', encoding='utf-8-sig')

def active(cues, time):
    return '\n'.join(c['text'] for c in cues if c['start'] <= time < c['end'])
