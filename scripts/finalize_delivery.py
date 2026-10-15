from pathlib import Path
import json,httpx,uuid,copy
from studio.contracts import Node
ROOT=Path(__file__).resolve().parent.parent;rt=json.loads((ROOT/'runtime.json').read_text('utf-8'));session=json.loads((ROOT/'reports/integration-session.json').read_text('utf-8'));image=json.loads((ROOT/'reports/image-verification.json').read_text('utf-8'))
c=httpx.Client(base_url=rt['url'],headers={'Authorization':'Bearer '+rt['token']},timeout=120)
def api(method,path,data=None):
    r=c.request(method,'/api'+path,json=data);r.raise_for_status();return r.json()['result']
def mutation(p,data,reason,key=None):return {'expected_revision':p['revision'],'actor':'ui','change_reason':reason,'idempotency_key':key or str(uuid.uuid4()),'data':data}
pid=session['project_id'];p=api('GET','/projects/'+pid)
api('POST',f'/projects/{pid}/timeline/compile',mutation(p,{},'Chốt timeline chỉ tham chiếu assets thực dùng'))
p=api('GET','/projects/'+pid);job=api('GET','/jobs/'+session['rig_render_job_id'])
assert p['timeline']['hash']==job['result']['timeline_hash'],'Timeline changed: requires a new export'
if not any(e['job_id']==job['id'] for e in p['exports']):api('POST',f'/projects/{pid}/export/finalize',mutation(p,{'job_id':job['id']},'Ghi nhận export đúng timeline/audio'))
p=api('GET','/projects/'+pid);api('POST',f'/projects/{pid}/history',mutation(p,{'summary':'Fixture 48 giây: nhân vật giữ hộp, diễn xuất theo anchor, sơ đồ ba bước, khoảng tĩnh; audio tone tổng hợp.','notable_layouts':['nhân vật và đạo cụ gắn tay','ba bước','giữ hình'],'feedback_scope':'episode'},'Lưu episode history có phạm vi'))
p=api('GET','/projects/'+pid);backup=api('POST',f'/projects/{pid}/backup',{})
newid=image['reuse_project_id'];new=api('GET','/projects/'+newid)
if not new['audio']:
    base=ROOT/'data/projects'/pid;audio=base/p['source_ids'][0]['path'];srt=base/p['source_ids'][1]['path']
    api('POST',f'/projects/{newid}/import-paths',mutation(new,{'audio_path':str(audio),'srt_path':str(srt)},'Tái sử dụng nguồn fixture cho hướng so sánh'))
new=api('GET','/projects/'+newid)
if not new['plan']:
    plan=copy.deepcopy(p['plan']);plan['audio_revision']=new['audio']['id'];mapping={a['id']:b['id'] for a,b in zip(p['utterances'],new['utterances'])}
    for scene in plan['scenes']:scene['utterance_ids']=[mapping[x] for x in scene['utterance_ids']]
    for event in plan['events']:event['anchor']['audio_revision']=new['audio']['id']
    plan['asset_requests']=[];plan['narrative_approach']='So sánh minh họa có cấu trúc và ảnh dùng lại';plan['distinctiveness_notes']='Cùng kit/nhận diện, thay trọng tâm cảnh 2 thành so sánh hai cách dùng hình';plan['outline']=['Hành động có tiếp xúc','So sánh tài nguyên','Giữ kết quả'];plan['scenes'][1]['purpose']='So sánh tài nguyên ảnh dùng lại và đồ họa có cấu trúc'
    plan['scenes'][1]['visual_strategy']='Ảnh trong một panel cạnh nhãn ba bước'
    plan['scenes'][1]['nodes'][-1]['visible_until']=30*48000
    plan['scenes'][1]['nodes'].append(Node(id='shared_box_image',kind='image',asset_id=image['reuse_asset_id'],x=1370,y=650,width=320,height=320,visible_from=24*48000,visible_until=32*48000,z=2).model_dump())
    api('POST',f'/projects/{newid}/plan/write',mutation(new,{'plan':plan},'Lập hướng so sánh bằng asset dùng chung, fixture minh họa'))
    new=api('GET','/projects/'+newid);api('POST',f'/projects/{newid}/plan/commit',mutation(new,{},'Preflight/chốt hướng kể thứ hai'))
    new=api('GET','/projects/'+newid);api('POST',f'/projects/{newid}/timeline/compile',mutation(new,{},'Compile project tái sử dụng'))
new=api('GET','/projects/'+newid);api('POST',f'/projects/{newid}/history',mutation(new,{'summary':'Project fixture thứ hai dùng ảnh local đã pin và hướng so sánh; plan/timeline hợp lệ, chưa export video thứ hai.','notable_layouts':['panel ảnh cạnh đồ họa có cấu trúc'],'feedback_scope':'episode'},'Ghi hướng kể khác, không suy gu thành luật kênh'))
report={'primary_project':pid,'final_job':job['id'],'mp4':job['result']['mp4'],'srt':job['result']['srt'],'backup':backup['path'],'second_project':newid,'second_project_validation':'plan committed and timeline compiled, no second full render','model_generations':{'TTS':1,'ASR':1,'images':1},'media_observation':'static preview + programmatic decode checks, not full audio/video creative review'}
(ROOT/'reports/delivery.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(report,ensure_ascii=False))
