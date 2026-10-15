from __future__ import annotations
import threading, queue, time, subprocess, json, os, shutil
from pathlib import Path
import psutil
from .contracts import uid,digest
from .store import StudioError
from .service import ROOT,probe,filehash

class Cancelled(Exception):pass

class Jobs:
    """One durable queue; heavy processes run serially and exit before next job."""
    def __init__(self,service):
        self.service=service;self.store=service.store;self.queue=queue.Queue();self.stop=threading.Event();self.processes={}
        for j in self.store.jobs():
            if j['status'] in ['running','cancel_requested']:j['status']='interrupted';self.store.update_job(j)
            elif j['status']=='queued':self.queue.put(j['id'])
        self.thread=threading.Thread(target=self.loop,daemon=True);self.thread.start();service.jobs=self

    def submit(self,pid,m,kind):
        with self.store.lock:
            p=self.store.get(pid);self.store.check_writer(pid,m.actor,m.lease_token)
            if p['revision']!=m.expected_revision:raise StudioError('REVISION_CONFLICT','Dự án đã đổi',{'current_revision':p['revision']},409)
            snapshot={'project':p,'parameters':m.data}
            if kind=='render':
                if not p.get('timeline') or p['timeline']['audio_revision']!=p['audio']['id']:raise StudioError('STALE_DEPENDENCY','Cần compile timeline hiện tại')
                if p['output_profile']['subtitle_mode']=='burn_in':raise StudioError('CAPABILITY_UNSUPPORTED','Burn-in chưa sẵn sàng; chọn SRT riêng')
            elif kind in ['audio_analyze','audio_align','tts_generate','asset_generate']:
                profiles=self.service.worker_profiles();profile=profiles.get(m.data.get('profile',kind),{})
                if profile.get('kind')!=kind or not profile.get('installed'):raise StudioError('MODEL_NOT_INSTALLED','Worker/model chưa cài',{'profile':m.data.get('profile',kind)})
                if not profile.get('license_record') or not profile.get('model_hash'):raise StudioError('LICENSE_UNRESOLVED','Profile cần license và model hash đã kiểm tra')
                if profile.get('license_record',{}).get('commercial_use') is False:raise StudioError('LICENSE_UNRESOLVED','Profile này hạn chế phi thương mại; chưa bật cho sản xuất')
                if kind=='tts_generate' and p['policies']['tts_replacement']!='allowed':raise StudioError('POLICY_BLOCKED','TTS cần quyền rõ trong dự án')
                if kind=='tts_generate' and profile.get('voices') and m.data.get('voice',profile.get('voice')) not in profile['voices']:raise StudioError('VOICE_UNSUPPORTED','Giọng không có trong SDK đã pin',{'voices':profile['voices']})
                if kind=='asset_generate':
                    if not p['committed_plan']:raise StudioError('PLAN_NOT_COMMITTED','Tạo ảnh cần plan đã chốt')
                    req=next((r for r in p['plan']['asset_requests'] if r['id']==m.data.get('request_id')),None)
                    if not req:raise StudioError('REFERENCE_MISSING','Không có asset request')
                    if req['workflow_profile']!=m.data['profile']:raise StudioError('WORKFLOW_INCOMPATIBLE','Profile không khớp request')
                    if req['layer_requirements'] or req['output'].get('alpha'):raise StudioError('WORKFLOW_INCOMPATIBLE','Profile ảnh V1 không xuất alpha/layer')
                    snapshot['request']=req
                if kind=='audio_align' and not p.get('analysis'):raise StudioError('TRANSCRIPT_MISSING','Phải accept transcript trước alignment; không chạy ASR lần hai')
                snapshot['worker_profile']=profile
            else:raise StudioError('JOB_UNSUPPORTED','Loại job không hỗ trợ')
            if kind=='render':
                inputs={'spans':p['timeline']['spans'],'audio_hash':p['audio']['pcm_hash'],'subtitles':p['utterances'],'profile':p['output_profile'],'parameters':m.data,'engine':p['timeline']['engine']}
            else:
                inputs={'kind':kind,'model_hash':profile['model_hash'],'adapter_hash':filehash(ROOT/'workers'/f'{kind}.py'),'software_hash':profile.get('software_hash'),'profile':{k:profile.get(k) for k in ['device','compute_type','language','precision','voice','engine_commit']}}
                if kind in ['audio_analyze','audio_align']:inputs['audio_hash']=p['audio']['pcm_hash']
                if kind=='audio_align':inputs['transcript']=p['utterances'];inputs['analysis']=p['analysis'].get('segments')
                if kind=='tts_generate':inputs['parameters']=m.data
                if kind=='asset_generate':inputs.update(request=snapshot['request'],references=[a['content_hash'] for a in p['assets'] if a['id'] in snapshot['request']['references']],workflow_hash=filehash(profile['workflow_path']))
            input_hash=digest(inputs)
            j={'id':uid('job'),'project_id':pid,'type':kind,'input_revision':p['revision'],'input_hash':input_hash,'idempotency_key':m.idempotency_key,'status':'queued','progress':0,'checkpoint':{},'resource_profile':m.data.get('profile','render'),'attempts':0,'cursor':0,'created':time.time(),'result':None,'error':None}
            j,created=self.store.put_job(j,snapshot)
            if created:self.queue.put(j['id'])
        return {'job_id':j['id'],'status':j['status'],'cache_hit':not created}

    def update(self,j,**kw):
        with self.store.lock:
            current,_=self.store.job(j['id'])
            if 'status' not in kw:j['status']=current['status']
            if kw.get('status')=='running' and current['status']=='cancelled':kw['status']='cancelled'
            j.update(kw);j['cursor']=current['cursor']+1;self.store.update_job(j)

    def cancel(self,jid):
        j,_=self.store.job(jid)
        if j['status']=='queued':self.update(j,status='cancelled')
        elif j['status']=='running':self.update(j,status='cancel_requested')
        return {'job_id':jid,'status':self.store.job(jid)[0]['status']}

    def resume(self,jid):
        j,_=self.store.job(jid)
        if j['status'] not in ['failed','blocked','interrupted','cancelled']:return {'job_id':jid,'status':j['status']}
        if (j.get('error') or {}).get('code') in ['PROVIDER_SUBMIT_UNKNOWN','GPU_OOM']:raise StudioError('RESUME_BLOCKED','Cần xử lý nguyên nhân trước khi resume',j['error'])
        self.update(j,status='queued',error=None);self.queue.put(jid)
        return {'job_id':jid,'status':'queued'}

    def close(self):
        self.stop.set()
        for process in list(self.processes.values()):self.kill(process)

    def kill(self,process):
        try:
            parent=psutil.Process(process.pid)
            for child in parent.children(recursive=True):child.kill()
            parent.kill()
        except psutil.NoSuchProcess:pass

    def loop(self):
        while not self.stop.is_set():
            try:jid=self.queue.get(timeout=.5)
            except queue.Empty:continue
            j,snapshot=self.store.job(jid)
            if j['status']!='queued':continue
            self.update(j,status='running',attempts=j['attempts']+1)
            if j['status']!='running':continue
            engine=None
            try:
                if j['type']=='asset_generate':engine=self.start_comfy(j,snapshot)
                result=self.execute(j,snapshot)
                self.update(j,status='succeeded',progress=1,result=result,error=None)
            except Cancelled:self.update(j,status='cancelled')
            except StudioError as e:self.update(j,status='blocked' if e.code in ['RESOURCE_INSUFFICIENT','MODEL_NOT_INSTALLED'] else 'failed',error={'code':e.code,'message':e.message,'details':e.details})
            except Exception as e:self.update(j,status='failed',error={'code':'WORKER_FAILED','message':str(e)[-2000:]})
            finally:
                if engine:
                    self.kill(engine);self.processes.pop(j['id']+'_engine',None)

    def start_comfy(self,j,snapshot):
        import socket,urllib.request
        profile=snapshot['worker_profile'];port=profile['port'];engine=None
        if psutil.virtual_memory().available/1048576<max(profile['min_ram_mb'],6144):raise StudioError('RESOURCE_INSUFFICIENT','Thiếu RAM để mở ComfyUI; cần ít nhất 6144 MB trống trước engine')
        with socket.socket() as sock:
            if sock.connect_ex(('127.0.0.1',port))==0:raise StudioError('PORT_IN_USE','Cổng ComfyUI riêng của studio đang bị dùng; không chiếm server khác')
        logs=ROOT/'logs';logs.mkdir(exist_ok=True)
        with open(logs/'comfy.log','a',encoding='utf-8') as log:
            engine=subprocess.Popen([profile['engine_python'],profile['engine_script'],'--listen','127.0.0.1','--port',str(port),'--lowvram','--disable-auto-launch'],cwd=Path(profile['engine_script']).parent,stdout=log,stderr=log,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        self.processes[j['id']+'_engine']=engine
        try:
            for _ in range(180):
                if self.store.job(j['id'])[0]['status']=='cancel_requested':raise Cancelled()
                if engine.poll() is not None:raise StudioError('COMFY_START_FAILED',(logs/'comfy.log').read_text('utf-8')[-2500:])
                try:
                    urllib.request.urlopen(profile['endpoint']+'/system_stats',timeout=1).close();return engine
                except OSError:time.sleep(1)
            raise StudioError('COMFY_START_TIMEOUT','ComfyUI chưa sẵn sàng sau 180 giây')
        except BaseException:
            self.kill(engine);self.processes.pop(j['id']+'_engine',None);raise

    def execute(self,j,snapshot):
        p=snapshot['project'];base=self.store.root/'projects'/p['id'];work=base/'reports'/j['id'];work.mkdir(exist_ok=True)
        profile=snapshot.get('worker_profile',{})
        available=psutil.virtual_memory().available/1048576
        required_ram=profile.get('reserve_after_engine_mb',2300) if j['type']=='asset_generate' else profile.get('min_ram_mb',512)
        if available<required_ram:raise StudioError('RESOURCE_INSUFFICIENT','RAM trống thấp hơn mức dự trữ của giai đoạn worker',{'available_mb':round(available),'required_mb':required_ram})
        if profile.get('min_vram_mb'):
            from .service import run
            memory=int(run(['nvidia-smi','--query-gpu=memory.free','--format=csv,noheader,nounits'],15).decode().splitlines()[0])
            if memory<profile['min_vram_mb']:raise StudioError('RESOURCE_INSUFFICIENT','VRAM trống thấp hơn mức profile',{'available_mb':memory,'required_mb':profile['min_vram_mb']})
        if shutil.disk_usage(base).free<512*1048576:raise StudioError('RESOURCE_INSUFFICIENT','Cần ít nhất 512 MB đĩa trống')
        context=snapshot|{'base':str(base),'work':str(work),'checkpoint':j['checkpoint']}
        if j['type']=='render':
            runtime=json.loads((ROOT/'runtime.json').read_text('utf-8'))
            context['runtime']=runtime;context['cache_dir']=str(base/'cache');context['export_dir']=str(base/'exports');context['job_id']=j['id']
            args=[runtime['node'],str(ROOT/'ui/scripts/render.mjs'),str(work/'input.json')]
        else:
            model=Path(profile['model_path'])
            if model.is_file() and filehash(model)!=profile['model_hash']:raise StudioError('MODEL_HASH_MISMATCH','Checkpoint khác profile đã pin')
            args=[profile['python'],str(ROOT/'workers'/f'{j["type"]}.py'),str(work/'input.json')]
        (work/'input.json').write_text(json.dumps(context,ensure_ascii=False),encoding='utf-8')
        env=os.environ.copy();env['PYTHONUTF8']='1';env['HF_HUB_OFFLINE']='1';env['HF_HOME']=str(self.store.root/'models'/'hf-cache')
        with open(work/'stderr.log','w',encoding='utf-8') as stderr:
            process=subprocess.Popen(args,stdout=subprocess.PIPE,stderr=stderr,text=True,encoding='utf-8',env=env,cwd=ROOT,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
            self.processes[j['id']]=process;lines=queue.Queue()
            def read():
                for line in process.stdout:lines.put(line)
                lines.put(None)
            threading.Thread(target=read,daemon=True).start();start=time.monotonic()
            try:
                while True:
                    current,_=self.store.job(j['id'])
                    if self.stop.is_set():self.kill(process);raise StudioError('INTERRUPTED','Core đóng trong khi worker đang chạy')
                    if current['status']=='cancel_requested':self.kill(process);raise Cancelled()
                    if time.monotonic()-start>profile.get('timeout_seconds',7200):self.kill(process);raise StudioError('WORKER_TIMEOUT','Job vượt timeout; giữ checkpoint')
                    try:line=lines.get(timeout=.25)
                    except queue.Empty:continue
                    if line is None:break
                    try:
                        event=json.loads(line)
                        if 'progress' in event:self.update(j,progress=event['progress'],checkpoint=event.get('checkpoint',j['checkpoint']))
                    except json.JSONDecodeError:pass
                process.wait(timeout=10)
            finally:
                if process.poll() is None:self.kill(process)
                self.processes.pop(j['id'],None)
        if process.returncode:
            resultfile=work/'error.json'
            if resultfile.exists():
                error=json.loads(resultfile.read_text('utf-8'));raise StudioError(error['code'],error['message'],error.get('details'))
            tail=(work/'stderr.log').read_text('utf-8')[-2500:]
            raise StudioError('GPU_OOM' if 'out of memory' in tail.lower() else 'WORKER_FAILED',tail)
        result=json.loads((work/'result.json').read_text('utf-8'))
        result['input_revision']=p['revision'];result['audio_revision']=(p.get('audio') or {}).get('id')
        if j['type']=='render':
            meta=probe(result['mp4']);video=next(x for x in meta['streams'] if x['codec_type']=='video');audio=next(x for x in meta['streams'] if x['codec_type']=='audio')
            expected=p['output_profile'];frames=p['timeline']['frame_count']
            if video['width']!=expected['width'] or video['height']!=expected['height'] or video['r_frame_rate']!=f'{expected["fps_num"]}/{expected["fps_den"]}' or int(video.get('nb_frames',-1))!=frames or int(audio['sample_rate'])!=48000:raise StudioError('OUTPUT_INVALID','ffprobe output không khớp timeline',{'probe':meta})
            result['technical_validation']='passed';result['frame_count']=frames;result['mp4_hash']=filehash(result['mp4']);result['user_reviewed']=False
        return result
