from common import *
import urllib.request,urllib.parse,time,uuid
ctx=context();profile=ctx['worker_profile'];req=ctx['request'];endpoint=profile['endpoint']
host=urllib.parse.urlparse(endpoint).hostname
if host not in ['127.0.0.1','localhost','::1']:fail(ctx,'LOCAL_ENDPOINT_REQUIRED','ComfyUI phải chạy trên loopback')
def get(route):
    with urllib.request.urlopen(endpoint+route,timeout=30) as r:return json.load(r)
try:
    workflow=json.loads(Path(profile['workflow_path']).read_text('utf-8'))
    ids=profile['nodes'];params=req['parameters'];width=int(req['output']['width']);height=int(req['output']['height'])
    if width>1024 or height>1024 or width%8 or height%8:fail(ctx,'WORKFLOW_INCOMPATIBLE','Profile nhẹ: kích thước bội 8, tối đa 1024')
    workflow[ids['positive']]['inputs']['text']=req['prompt'];workflow[ids['negative']]['inputs']['text']=req['negative_prompt']
    workflow[ids['latent']]['inputs'].update(width=width,height=height,batch_size=1)
    allowed=['seed','steps','cfg','sampler_name','scheduler','denoise']
    if set(params)-set(allowed):fail(ctx,'WORKFLOW_INCOMPATIBLE','Tham số ngoài allowlist')
    workflow[ids['sampler']]['inputs'].update(params)
    cp=ctx['checkpoint'];provider_id=cp.get('provider_job_id')
    if not provider_id:
        data=json.dumps({'prompt':workflow,'client_id':str(uuid.uuid4())}).encode()
        request=urllib.request.Request(endpoint+'/prompt',data=data,headers={'Content-Type':'application/json'})
        try:
            with urllib.request.urlopen(request,timeout=30) as r:provider_id=json.load(r)['prompt_id']
        except Exception as e:fail(ctx,'PROVIDER_SUBMIT_UNKNOWN','Submit chưa rõ kết quả; không tự gửi lại',{'error':str(e)})
        progress(.05,{'provider_job_id':provider_id})
    for attempt in range(600):
        history=get('/history/'+provider_id).get(provider_id)
        if history:
            if history.get('status',{}).get('status_str')=='error':fail(ctx,'COMFY_FAILED','ComfyUI trả lỗi',{'provider_job_id':provider_id,'status':history['status']})
            images=[x for out in history.get('outputs',{}).values() for x in out.get('images',[])]
            if images:
                item=images[0];url=endpoint+'/view?'+urllib.parse.urlencode(item)
                target=Path(ctx['work'])/'generated.png'
                with urllib.request.urlopen(url,timeout=60) as r:target.write_bytes(r.read())
                save(ctx,{'asset_path':str(target),'provider_job_id':provider_id,'request_id':req['id'],'model_hash':profile['model_hash'],'generation_record':{'request':req,'profile':profile,'workflow':workflow},'license_record':profile['license_record'],'alpha_status':'unverified','automatically_registered':False});progress(1,{'provider_job_id':provider_id});break
        time.sleep(2)
    else:fail(ctx,'PROVIDER_TIMEOUT','Chưa có kết quả sau 20 phút; giữ provider_job_id',{'provider_job_id':provider_id})
except Exception as e:fail(ctx,'COMFY_FAILED',str(e))
