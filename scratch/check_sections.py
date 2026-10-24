import json

data = json.load(open('projects/mo_den_phong_than/voice_direction/report_phong_than.json', 'r', encoding='utf-8'))
sections = {}
for e in data['timeline']:
    s = e['section_num']
    if s not in sections:
        sections[s] = {'title': e['section_title'], 'start': e['start_seconds'], 'end': e['end_seconds'], 'cues': []}
    sections[s]['end'] = e['end_seconds']
    sections[s]['cues'].append(e['id'])

for s, v in sections.items():
    print(f"Phần {s}: {v['title']} | Cues {v['cues'][0]}-{v['cues'][-1]} ({len(v['cues'])} cues) | {v['start']:.2f}s -> {v['end']:.2f}s ({v['end']-v['start']:.1f}s)")
