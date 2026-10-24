import json

for name in ['prompts_v2.json', 'prompts_bo_sung_v2.json']:
    p = 'projects/mo_den_phong_than/assets/Mo_Den_Phong_Than_V2/' + name
    d = json.load(open(p, 'r', encoding='utf-8'))
    print(name, 'keys/type:', type(d), len(d) if isinstance(d, list) else list(d.keys())[:5])
    if isinstance(d, list):
        print('Sample item:', json.dumps(d[0], ensure_ascii=False, indent=2)[:300])
    elif isinstance(d, dict):
        first_key = list(d.keys())[0]
        print('First key:', first_key, json.dumps(d[first_key], ensure_ascii=False, indent=2)[:300])
