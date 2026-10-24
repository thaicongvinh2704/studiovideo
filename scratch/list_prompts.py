import json

prompts = json.load(open('projects/mo_den_phong_than/assets/Mo_Den_Phong_Than_V2/prompts_v2.json', 'r', encoding='utf-8'))
for p in prompts:
    print(f"{p.get('id')}\t{p.get('name')}\t{p.get('type')}\t{p.get('section')}\t{p.get('file')}")
