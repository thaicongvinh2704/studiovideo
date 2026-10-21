"""Report repeated dominant-background families; never certifies visual quality."""
import argparse
import json
from collections import defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
FAMILIES={151:'Đô thị',154:'Chợ',157:'Hồ chứa',160:'Hồ/trầm tích',
          163:'Ruộng ngô',166:'Kho lương',169:'Đường nối',172:'Nhà/sân',
          175:'Khu công trình/cháy',178:'Cung điện'}


def audit(project):
    result=defaultdict(lambda:dict(count=0,seconds=0,shots=[]))
    for i,scene in enumerate(project['scenes'],1):
        edit=scene.get('editorial',{})
        if edit.get('layout')!='world':continue
        source=str(edit.get('source',''))
        if not source.isdigit():continue
        number=int(source)
        family=next((name for first,name in FAMILIES.items() if first<=number<=first+2),'Tài sản '+source)
        entry=result[family];entry['count']+=1;entry['seconds']+=scene['duration']
        entry['shots'].append(dict(number=i,id=scene['id'],start=scene['start'],duration=scene['duration'],
                                  source=source,title=edit.get('title',''),
                                  new_information=edit.get('new_information',''),
                                  repetition_reason=edit.get('repetition_reason','')))
    families=[]
    for family,entry in sorted(result.items(),key=lambda item:-item[1]['count']):
        entry.update(family=family,seconds=round(entry['seconds'],3),default_limit=3,
                     exceeds_default_budget=entry['count']>3)
        families.append(entry)
    return dict(scope='Dominant background setups tagged editorial.layout=world; includes broad crops and variants.',
                limits_source='QUY_DINH_DAO_DIEN_HINH_ANH.md',
                dominant_background_shots=sum(e['count'] for e in families),
                dominant_background_seconds=round(sum(e['seconds'] for e in families),3),
                families=families,
                editorial_status='REVIEW_REQUIRED',
                limits='Counts flag repetition; they do not establish whether a shot has meaningful action or whether it is aesthetically successful. Untagged layouts require separate review.')


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('project',type=Path)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    result=audit(json.loads(args.project.read_text(encoding='utf-8-sig')))
    out=args.output or args.project.parent/'repetition_audit.json'
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='families'},ensure_ascii=False,indent=2))
    for family in result['families']:
        print(f"{family['family']}: {family['count']} lần, {family['seconds']} giây; giới hạn mặc định 3")


if __name__=='__main__':main()
