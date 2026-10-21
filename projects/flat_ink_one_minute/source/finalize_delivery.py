import json,zipfile
from pathlib import Path
DEST=Path(__file__).resolve().parents[1]
file=DEST/'review'/'verification.json';report=json.loads(file.read_text(encoding='utf-8'))
report['decoded_visual_review']='Contact sheet at 2, 7, 11, 20, 29, 34, 43, 53 and 58 seconds inspected; source presenter retained, captions readable, final scene present. Character poses remain static.'
file.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
with zipfile.ZipFile(DEST/'Du_an_1_phut.zip','a',zipfile.ZIP_DEFLATED) as z:
    for name in ('GHI_CHU.md','phu_de.srt','timing.json','shot_list.json','review/verification.json','source/imagegen_prompts.json'):
        z.write(DEST/name,name)
print('Delivery package finalized')
