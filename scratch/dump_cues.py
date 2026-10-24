import json

data = json.load(open('projects/mo_den_phong_than/voice_direction/report_phong_than.json', 'r', encoding='utf-8'))
for e in data['timeline']:
    print(f"[{e['id']:03d}] (Sec {e['section_num']}) {e['start_seconds']:.2f}-{e['end_seconds']:.2f}s ({e['end_seconds']-e['start_seconds']:.2f}s): {e['spoken_text']}")
