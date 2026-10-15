import json,sys,traceback,hashlib
from pathlib import Path

def context():return json.loads(Path(sys.argv[1]).read_text('utf-8'))
def progress(value,checkpoint=None):print(json.dumps({'progress':value,'checkpoint':checkpoint or {}}),flush=True)
def save(ctx,result):
    (Path(ctx['work'])/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
def fail(ctx,code,message,details=None):
    (Path(ctx['work'])/'error.json').write_text(json.dumps({'code':code,'message':message,'details':details or {}}),encoding='utf-8');raise SystemExit(1)
