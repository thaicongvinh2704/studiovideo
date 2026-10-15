from pathlib import Path
import json,time,httpx,uuid
ROOT=Path(__file__).resolve().parent.parent;rt=json.loads((ROOT/'runtime.json').read_text('utf-8'));session=json.loads((ROOT/'reports/integration-session.json').read_text('utf-8'))
c=httpx.Client(base_url=rt['url'],headers={'Authorization':'Bearer '+rt['token']},timeout=60)
def api(method,path,data=None):
    r=c.request(method,'/api'+path,json=data);r.raise_for_status();return r.json()['result']
def mutation(p,data,reason,key=None):return {'expected_revision':p['revision'],'actor':'ui','change_reason':reason,'idempotency_key':key or str(uuid.uuid4()),'data':data}
pid=session['project_id'];p=api('GET','/projects/'+pid)
req={'id':'image_worker_fixture','scene_refs':['scene_2'],'role':'Minh họa đạo cụ hộp, chỉ kiểm chứng adapter/cache','exact_details':['một chiếc hộp giấy đóng kín','không có chữ'],'forbidden_details':['nhân vật lịch sử','logo','chữ'],'references':[],'prompt':'a single closed cardboard box, simple clean illustration, centered object on a plain cream background, soft natural light, no writing, no logo','prompt_vi':'Một chiếc hộp giấy đóng kín, nền kem đơn giản, không chữ hoặc logo. Dữ liệu minh họa kỹ thuật.','negative_prompt':'text, letters, watermark, logo, person','workflow_profile':'sd15-local','parameters':{'seed':123456,'steps':12,'cfg':7,'sampler_name':'euler','scheduler':'normal','denoise':1},'layer_requirements':[],'output':{'width':512,'height':512,'format':'png','alpha':False}}
if not any(r['id']==req['id'] for r in p['plan']['asset_requests']):
    plan=p['plan'];plan['asset_requests'].append(req);api('POST',f'/projects/{pid}/plan/write',mutation(p,{'plan':plan},'Thêm một request kiểm chứng ảnh, không A/B'))
    p=api('GET','/projects/'+pid);api('POST',f'/projects/{pid}/plan/commit',mutation(p,{},'Preflight và chốt asset request'))
p=api('GET','/projects/'+pid);data={'profile':'sd15-local','request_id':req['id']}
job=api('POST',f'/projects/{pid}/jobs/asset_generate',mutation(p,data,'Một lần kiểm chứng ComfyUI local','comfy-one-image'))
deadline=time.monotonic()+900
while time.monotonic()<deadline:
    j=api('GET','/jobs/'+job['job_id'])
    if j['status']=='succeeded':break
    if j['status'] in ['failed','blocked']:raise RuntimeError(j['error'])
    time.sleep(2)
assert j['status']=='succeeded'
result=j['result'];p=api('GET','/projects/'+pid)
existing=next((a for a in p['assets'] if (a.get('generation_record') or {}).get('request',{}).get('id')==req['id']),None)
if existing:registered={'asset_id':existing['id'],'metadata':existing}
else:registered=api('POST',f'/projects/{pid}/assets/register-path',mutation(p,{'path':result['asset_path'],'license_record':result['license_record'],'source':'local_sd15_fixture','name':'Hộp — ảnh kiểm chứng local','generation_record':result['generation_record']},'Đăng ký ảnh có provenance','register-comfy-fixture'))
p=api('GET','/projects/'+pid)
existing_shared=next((a for a in api('GET','/shared/assets') if a['content_hash']==registered['metadata']['content_hash']),None)
shared={'shared_id':existing_shared['shared_id']} if existing_shared else api('POST',f'/projects/{pid}/assets/share',mutation(p,{'asset_id':registered['asset_id']},'Lưu tài nguyên dùng chung','share-comfy-fixture'))
projects=api('GET','/projects');new=next((p for p in projects if p['name']=='Kiểm chứng tái sử dụng — so sánh'),None) or api('POST','/projects',{'name':'Kiểm chứng tái sử dụng — so sánh'})
new=api('GET','/projects/'+new['id']);existing_reuse=next((a for a in new['assets'] if a['content_hash']==registered['metadata']['content_hash']),None)
reused={'asset_id':existing_reuse['id']} if existing_reuse else api('POST',f'/projects/{new["id"]}/assets/reuse',mutation(new,{'shared_id':shared['shared_id']},'Dùng lại tài nguyên ở dự án mới','reuse-fixture'))
p=api('GET','/projects/'+pid)
dup=api('POST',f'/projects/{pid}/jobs/asset_generate',mutation(p,data,'Đọc lại job ảnh không tạo lần hai','comfy-one-image-read-again'))
assert dup['cache_hit'] and dup['job_id']==j['id']
report={'job_id':j['id'],'provider_job_id':result['provider_job_id'],'image':result['asset_path'],'asset_id':registered['asset_id'],'dimensions':registered['metadata']['dimensions'],'alpha_status':registered['metadata']['alpha_status'],'cache_hit':True,'automatic_quality_regenerations':0,'shared_asset_id':shared['shared_id'],'reuse_project_id':new['id'],'reuse_asset_id':reused['asset_id'],'style_quality':'not_certified'}
(ROOT/'reports/image-verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(report,ensure_ascii=False))
