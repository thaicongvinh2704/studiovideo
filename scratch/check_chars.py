import json
import re

plan = json.load(open('projects/mo_den_phong_than/voice_direction/03_Kich_Ban_Bien_Kich_Dien_Doc.json', encoding='utf-8'))
all_text = ' '.join(u['spoken_text'] for u in plan['units'])

# Find numbers or unusual symbols
nums = re.findall(r'\d+', all_text)
print("Digits found in speech text:", nums)

# Check unusual characters
chars = set(all_text)
for c in sorted(chars):
    if not (c.isalnum() or c.isspace() or c in ".,!?:;…–-—'\"()"):
        print("Special char:", repr(c))
