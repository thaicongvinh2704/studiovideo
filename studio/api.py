from __future__ import annotations
import os,json,secrets,asyncio,tempfile,contextlib
from pathlib import Path
from fastapi import FastAPI,Request,UploadFile,File,Form
from fastapi.responses import JSONResponse,FileResponse,StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from .contracts import Mutation,Policies,OutputProfile,uid,digest
from .service import Service,StudioError,ROOT,bounded_path
from .jobs import Jobs

service=Service();jobs=Jobs(service)
runtime_path=ROOT/'runtime.json'
runtime=json.loads(runtime_path.read_text('utf-8')) if runtime_path.exists() else {}
TOKEN=runtime.get('token') or secrets.token_urlsafe(32)

@contextlib.asynccontextmanager
async def lifespan(app):
    yield
    jobs.close()

app=FastAPI(title='Story Motion Studio Local',lifespan=lifespan)

def ok(result,pid=None):
    return {'ok':True,'project_id':pid,'revision':service.store.get(pid)['revision'] if pid else None,'result':result,'issues':[]}

@app.middleware('http')
async def protect(request:Request,call_next):
    host=request.headers.get('host','').split(':')[0]
    origin=request.headers.get('origin')
    if host not in ['127.0.0.1','localhost','testserver']:return JSONResponse({'ok':False,'error':{'code':'HOST_BLOCKED','message':'Chỉ localhost'}},403)
    if origin and origin not in [f'http://127.0.0.1:{runtime.get("port",8765)}',f'http://localhost:{runtime.get("port",8765)}']:return JSONResponse({'ok':False,'error':{'code':'ORIGIN_BLOCKED','message':'Origin ngoài studio'}},403)
    if request.url.path.startswith('/api') and request.url.path!='/api/health':
        incoming=request.headers.get('authorization','').removeprefix('Bearer ') or request.cookies.get('studio_session','')
        if not secrets.compare_digest(incoming,TOKEN):return JSONResponse({'ok':False,'error':{'code':'AUTH_REQUIRED','message':'Cần session local'}},401)
    response=await call_next(request)
    response.headers['X-Content-Type-Options']='nosniff';response.headers['Referrer-Policy']='no-referrer'
    return response

@app.exception_handler(StudioError)
async def studio_error(request,e):
    return JSONResponse({'ok':False,'project_id':None,'revision':None,'error':{'code':e.code,'message':e.message,'details':e.details},'issues':e.details.get('issues',[])},status_code=e.status)

@app.exception_handler(ValueError)
async def value_error(request,e):
    return JSONResponse({'ok':False,'error':{'code':'VALIDATION_FAILED','message':str(e)}},400)

@app.exception_handler(RequestValidationError)
async def request_validation(request,e):
    return JSONResponse({'ok':False,'project_id':None,'revision':None,'error':{'code':'VALIDATION_FAILED','message':'Dữ liệu request không hợp lệ','details':{'fields':[{'location':list(x['loc']),'message':x['msg']} for x in e.errors()]}},'issues':[]},422)

@app.get('/api/health')
def health():return ok({'service':'ready','name':'Story Motion Studio Local','schema_version':'1.0'})

@app.post('/api/session')
def session():
    response=JSONResponse(ok({'session':'ready'}));response.set_cookie('studio_session',TOKEN,httponly=True,samesite='strict');return response

@app.get('/api/capabilities')
def capabilities():return ok(service.capabilities())

@app.get('/api/doctor')
def doctor():return ok(service.doctor())

@app.post('/api/fixture')
def fixture():
    from .fixture import create_fixture
    return ok(create_fixture(service))

@app.get('/api/projects/{pid}/waveform')
def waveform(pid:str):
    import wave,array
    p=service.store.get(pid)
    if not p['audio']:raise StudioError('AUDIO_MISSING','Chưa nhập audio')
    peaks=[]
    with wave.open(str(service.store.root/'projects'/pid/p['audio']['path'])) as f:
        chunk=max(1,(f.getnframes()+1199)//1200)
        while data:=f.readframes(chunk):
            values=array.array('h');values.frombytes(data);peaks.append(max(abs(v) for v in values)/32768)
    return ok({'peaks':peaks,'audio_revision':p['audio']['id']},pid)

@app.get('/api/projects')
def projects():return ok(service.store.list())

@app.post('/api/projects')
def create(body:dict):
    p=service.store.create(body.get('name','Dự án mới'),body.get('policies'),body.get('output_profile'));return ok(service.store.summary(p),p['id'])

@app.get('/api/projects/{pid}')
def project(pid:str):return ok(service.store.get(pid),pid)

@app.get('/api/projects/{pid}/summary')
def summary(pid:str):return ok(service.store.summary(service.store.get(pid)),pid)

@app.get('/api/projects/{pid}/changes')
def changes(pid:str,since_revision:int=0):return ok(service.store.changes(pid,since_revision),pid)

@app.post('/api/projects/{pid}/lease')
def lease(pid:str,body:dict):return ok(service.store.acquire(pid,body['actor']),pid)

@app.delete('/api/projects/{pid}/lease')
def release(pid:str,body:dict):return ok(service.store.release(pid,body['lease_token']),pid)

@app.post('/api/projects/{pid}/import')
async def upload_sources(pid:str,audio:UploadFile=File(),srt:UploadFile=File(),mutation:str=Form()):
    m=Mutation.model_validate_json(mutation)
    with tempfile.TemporaryDirectory(dir=service.store.root) as folder:
        paths=[]
        for f in [audio,srt]:
            path=Path(folder)/Path(f.filename or 'input').name
            with path.open('wb') as target:
                while chunk:=await f.read(1024*1024):target.write(chunk)
            paths.append(path)
        return service.import_sources(pid,m,*paths)

@app.post('/api/projects/{pid}/import-paths')
def import_paths(pid:str,m:Mutation):
    roots=[ROOT]+[Path(x) for x in os.environ.get('STUDIO_IMPORT_ROOTS','').split(os.pathsep) if x]
    return service.import_sources(pid,m,bounded_path(m.data['audio_path'],roots),bounded_path(m.data['srt_path'],roots))

@app.post('/api/projects/{pid}/plan/write')
def plan_write(pid:str,m:Mutation):return service.write_plan(pid,m)

@app.post('/api/projects/{pid}/plan/patch')
def plan_patch(pid:str,m:Mutation):return service.patch_plan(pid,m)

@app.get('/api/projects/{pid}/plan/preflight')
def preflight(pid:str):return ok({'issues':service.preflight(service.store.get(pid))},pid)

@app.post('/api/projects/{pid}/plan/commit')
def plan_commit(pid:str,m:Mutation):return service.commit(pid,m)

@app.post('/api/projects/{pid}/timeline/compile')
def compile_timeline(pid:str,m:Mutation):return service.compile(pid,m)

@app.post('/api/projects/{pid}/settings')
def settings(pid:str,m:Mutation):
    def apply(p):
        if 'name' in m.data:p['name']=str(m.data['name'])
        if 'policies' in m.data:p['policies']=Policies(**m.data['policies']).model_dump()
        if 'output_profile' in m.data:p['output_profile']=OutputProfile(**m.data['output_profile']).model_dump();p['timeline']=None
        if 'channel_profile' in m.data:p['channel_profile']=m.data['channel_profile']
        return {'updated':list(m.data)}
    return service.store.mutate(pid,m,'settings',apply)

@app.post('/api/projects/{pid}/audio/edits')
def edits(pid:str,m:Mutation):return service.audio_edits(pid,m)

@app.post('/api/projects/{pid}/audio/anchor')
def manual_anchor(pid:str,m:Mutation):
    def apply(p):
        if not p['audio']:raise StudioError('AUDIO_MISSING','Chưa có audio')
        u=next((u for u in p['utterances'] if u['id']==m.data['utterance_id']),None)
        if not u:raise StudioError('REFERENCE_MISSING','Utterance không có')
        index=int(m.data['token_index']);tokens=u['raw_text'].split()
        if not 0<=index<len(tokens):raise StudioError('ANCHOR_INVALID','Token index ngoài câu')
        start,end=int(m.data['start_sample']),int(m.data['end_sample'])
        if not 0<=start<end<=p['audio']['sample_count'] or not m.data.get('evidence','').strip():raise StudioError('ANCHOR_INVALID','Mốc cần khoảng audio hợp lệ và bằng chứng')
        wid=u['id']+'_word_'+str(index);word={'id':wid,'utterance_id':u['id'],'token_index':index,'text':tokens[index],'start_sample':start,'end_sample':end,'method':'manual','evidence_status':'user_confirmed','evidence':m.data['evidence'],'audio_revision':p['audio']['id']}
        p['words']=[w for w in p['words'] if w['id']!=wid]+[word];p['committed_plan']=None;p['timeline']=None;p['validation_status']='not_checked'
        return {'word_id':wid,'audio_revision':p['audio']['id']}
    return service.store.mutate(pid,m,'word_anchor_write',apply)

@app.get('/api/shared/assets')
def shared_assets():
    folder=service.store.root/'shared/assets'
    return ok([json.loads(path.read_text('utf-8')) for path in folder.glob('*.json')])

@app.post('/api/projects/{pid}/assets/share')
def share_asset(pid:str,m:Mutation):
    import shutil
    def apply(p):
        a=next((a for a in p['assets'] if a['id']==m.data['asset_id']),None)
        if not a:raise StudioError('ASSET_MISSING','Không có asset')
        source=service.store.root/'projects'/pid/a['path'];folder=service.store.root/'shared/assets';target=folder/source.name
        if not target.exists():shutil.copyfile(source,target)
        record=a|{'shared_id':'shared_'+a['content_hash'][:20],'shared_path':source.name,'origin_project_id':pid,'path':None}
        (folder/(record['shared_id']+'.json')).write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
        return {'shared_id':record['shared_id']}
    return service.store.mutate(pid,m,'asset_share',apply)

@app.post('/api/projects/{pid}/assets/reuse')
def reuse_asset(pid:str,m:Mutation):
    folder=service.store.root/'shared/assets';sid=m.data['shared_id']
    if not sid.startswith('shared_') or not sid[7:].isalnum():raise StudioError('ASSET_ID_INVALID','Shared ID không hợp lệ')
    record=json.loads((folder/(sid+'.json')).read_text('utf-8'));source=bounded_path(folder/record['shared_path'],[folder])
    m.data.update(path=str(source),name=record['name'],license_record=record['license_record'],source={'kind':'shared_reuse','shared_id':sid,'origin_project_id':record['origin_project_id']},generation_record=record.get('generation_record'))
    return service.register_asset(pid,m,source)

@app.post('/api/projects/{pid}/jobs/{kind}')
def submit(pid:str,kind:str,m:Mutation):return ok(jobs.submit(pid,m,kind),pid)

@app.get('/api/jobs')
def job_list(project_id:str|None=None):return ok(service.store.jobs(project_id))

@app.get('/api/jobs/{jid}')
def job_status(jid:str,cursor:int=-1):
    j,_=service.store.job(jid)
    p=service.store.get(j['project_id']);return ok(j|{'stale':p['revision']!=j['input_revision']},j['project_id'])

@app.post('/api/jobs/{jid}/{action}')
def job_action(jid:str,action:str):
    if action not in ['cancel','resume']:raise StudioError('ACTION_UNKNOWN','Action không hợp lệ')
    return ok(jobs.cancel(jid) if action=='cancel' else jobs.resume(jid))

@app.get('/api/events')
async def events(request:Request):
    async def stream():
        last=''
        while not await request.is_disconnected():
            summary=[{k:j[k] for k in ['id','project_id','type','status','progress','cursor','input_revision','error']} for j in service.store.jobs()]
            data=json.dumps(summary,ensure_ascii=False)
            if data!=last:yield f'data: {data}\n\n';last=data
            else:yield ': heartbeat\n\n'
            await asyncio.sleep(2)
    return StreamingResponse(stream(),media_type='text/event-stream')

@app.post('/api/projects/{pid}/assets/register-path')
def register_path(pid:str,m:Mutation):return service.register_asset(pid,m,bounded_path(m.data['path'],[ROOT,service.store.root]))

@app.post('/api/projects/{pid}/assets/patch')
def patch_asset(pid:str,m:Mutation):return service.replace_asset(pid,m,bounded_path(m.data['replacement_path'],[ROOT,service.store.root]))

@app.post('/api/projects/{pid}/assets/accept-job')
def accept_asset_job(pid:str,m:Mutation):
    j,snapshot=service.store.job(m.data['job_id'])
    if j['project_id']!=pid or j['status']!='succeeded' or j['type'] not in ['asset_generate','tts_generate']:raise StudioError('JOB_INVALID','Không phải media job thành công của dự án')
    result=j['result'];path=result.get('asset_path') or result.get('audio_path')
    m.data.update(path=path,license_record=result['license_record'],source={'kind':'local_generation','job_id':j['id']},generation_record=result.get('generation_record') or {'model_hash':result['model_hash'],'voice':result.get('voice'),'parameters':snapshot['parameters']},name=m.data.get('name','Ảnh local' if j['type']=='asset_generate' else 'Giọng local'))
    return service.register_asset(pid,m,bounded_path(path,[service.store.root/'projects'/pid]))

@app.get('/api/projects/{pid}/issues')
def list_issues(pid:str):return ok(service.store.get(pid)['issues'],pid)

@app.post('/api/projects/{pid}/issues/resolve')
def resolve_issue(pid:str,m:Mutation):
    def apply(p):
        item=next((i for i in p['issues'] if i['id']==m.data['issue_id']),None)
        if not item:raise StudioError('ISSUE_NOT_FOUND','Không tìm thấy issue')
        evidence=m.data.get('evidence','').strip()
        if not evidence:raise StudioError('EVIDENCE_REQUIRED','Resolve cần bằng chứng và phạm vi xử lý')
        item.update(status='resolved',resolution={'evidence':evidence,'actor':m.actor,'revision':p['revision']+1})
        return {'issue_id':item['id'],'status':'resolved','preflight_still_required':True}
    return service.store.mutate(pid,m,'issue_resolve',apply)

@app.post('/api/projects/{pid}/assets/upload')
async def upload_asset(pid:str,file:UploadFile=File(),mutation:str=Form()):
    with tempfile.TemporaryDirectory(dir=service.store.root) as folder:
        path=Path(folder)/Path(file.filename or 'image.png').name
        with path.open('wb') as f:
            while chunk:=await file.read(1024*1024):f.write(chunk)
        return service.register_asset(pid,Mutation.model_validate_json(mutation),path)

@app.get('/api/projects/{pid}/assets')
def search_assets(pid:str,q:str=''):
    return ok([a for a in service.store.get(pid)['assets'] if q.lower() in a['name'].lower()],pid)

@app.post('/api/projects/{pid}/analysis/accept')
def accept_analysis(pid:str,m:Mutation):
    j,_=service.store.job(m.data['job_id'])
    if j['project_id']!=pid or j['status']!='succeeded' or j['type'] not in ['audio_analyze','audio_align']:raise StudioError('JOB_INVALID','Không phải analysis thành công của dự án')
    def apply(p):
        if j['result']['audio_revision']!=p['audio']['id']:raise StudioError('STALE_DEPENDENCY','Analysis trỏ audio cũ')
        result=j['result'];p['analysis']=result
        if j['type']=='audio_align':p['words']=result['words']
        p['issues']=[i for i in p['issues'] if i['code']!='SRT_UNVERIFIED']+result.get('issues',[])
        p['committed_plan']=None;p['timeline']=None
        return {'words':len(p['words']),'analysis_job':j['id']}
    return service.store.mutate(pid,m,'audio_accept_analysis',apply)

@app.post('/api/projects/{pid}/checkpoint')
def checkpoint(pid:str):
    p=service.store.get(pid);path=service.store.root/'projects'/pid/'plans'/f'checkpoint-r{p["revision"]}.json';path.write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf-8');return ok({'path':str(path)},pid)

@app.post('/api/projects/{pid}/export/finalize')
def finalize(pid:str,m:Mutation):
    j,_=service.store.job(m.data['job_id'])
    def apply(p):
        if j['project_id']!=pid or j['status']!='succeeded' or j['type']!='render':raise StudioError('OUTPUT_INVALID','Không có render thành công')
        if not p['timeline'] or j['result']['timeline_hash']!=p['timeline']['hash'] or j['result']['audio_revision']!=p['audio']['id']:raise StudioError('STALE_DEPENDENCY','Render không dùng revision hiện tại')
        p['exports'].append({'job_id':j['id'],'input_revision':j['input_revision'],'result':j['result']});p['content_status']='rendered';p['validation_status']='output_technical_passed'
        return {'job_id':j['id'],'technical_validation':'passed','user_reviewed':False,'content_accuracy':'not_certified'}
    return service.store.mutate(pid,m,'export_finalize',apply)

@app.post('/api/projects/{pid}/backup')
def backup(pid:str):return ok(service.backup(pid),pid)

@app.post('/api/restore-path')
def restore(body:dict):return ok(service.restore(bounded_path(body['path'],[ROOT,service.store.root])))

@app.post('/api/restore')
async def restore_upload(file:UploadFile=File()):
    with tempfile.TemporaryDirectory(dir=service.store.root) as directory:
        target=Path(directory)/'backup.zip'
        with target.open('wb') as output:
            while block:=await file.read(1048576):output.write(block)
        return ok(service.restore(target))

@app.get('/api/history')
def history():
    with service.store.lock:return ok([json.loads(r[0]) for r in service.store.db.execute('SELECT summary FROM history')])

@app.post('/api/projects/{pid}/history')
def record_history(pid:str,m:Mutation):
    def apply(p):
        plan=p.get('plan') or {}
        h={'project_id':pid,'summary':m.data.get('summary',''),'approach':plan.get('narrative_approach'),'notable_layouts':m.data.get('notable_layouts',[]),'actions':list({e['action'] for e in plan.get('events',[])}),'opening':plan.get('opening_promise'),'ending':plan.get('payoff'),'feedback_scope':m.data.get('feedback_scope','episode')}
        service.store.db.execute('INSERT OR REPLACE INTO history VALUES(?,?)',(pid,json.dumps(h,ensure_ascii=False)));return h
    return service.store.mutate(pid,m,'episode_history',apply)

@app.get('/api/files/{pid}/{fid}')
def artifact(pid:str,fid:str):
    p=service.store.get(pid);base=service.store.root/'projects'/pid;path=None
    if fid=='audio' and p['audio']:path=base/p['audio']['path']
    for a in p['assets']:
        if a['id']==fid:path=base/a['path']
    for j in service.store.jobs(pid):
        if fid==j['id'] and j['status']=='succeeded' and j['type']=='render':path=Path(j['result']['mp4'])
    if path is None or not bounded_path(path,[base]).is_file():raise StudioError('ARTIFACT_NOT_FOUND','Không tìm thấy artifact',status=404)
    return FileResponse(path)

if (ROOT/'ui/dist').exists():app.mount('/',StaticFiles(directory=ROOT/'ui/dist',html=True),name='ui')
