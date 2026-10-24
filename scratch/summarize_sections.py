import json

data = json.load(open('projects/mo_den_phong_than/voice_direction/report_phong_than.json', 'r', encoding='utf-8'))
for s in range(1, 10):
    cues = [e for e in data['timeline'] if e['section_num'] == s]
    title = cues[0]["section_title"]
    start = cues[0]["start_seconds"]
    end = cues[-1]["end_seconds"]
    print(f"=== PHẦN {s}: {title} ({len(cues)} cues, {start:.1f}s -> {end:.1f}s, dài {end-start:.1f}s) ===")
    for c in cues:
        print(f"  [{c['id']:03d}] {c['start_seconds']:.2f}-{c['end_seconds']:.2f}s: {c['spoken_text']}")
    print()
