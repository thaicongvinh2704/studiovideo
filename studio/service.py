from __future__ import annotations
from pathlib import Path
import os, json, shutil, subprocess, hashlib, math, wave, zipfile, tempfile, time
import psutil
from .store import Store, StudioError
from .contracts import *

ROOT=Path(__file__).resolve().parent.parent

def run(args,timeout=120):
    try:
        r=subprocess.run([str(x) for x in args],capture_output=True,timeout=timeout,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
    except FileNotFoundError as e: raise StudioError('DEPENDENCY_MISSING',str(e)) from e
    if r.returncode: raise StudioError('WORKER_FAILED',r.stderr.decode('utf-8','replace')[-2500:])
    return r.stdout

def filehash(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()

def probe(path):
    return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',path]))

def bounded_path(path,roots):
    p=Path(path).resolve()
    if not any(p.is_relative_to(Path(r).resolve()) for r in roots):
        raise StudioError('PATH_NOT_ALLOWED','Đường dẫn ngoài thư mục được cấp quyền')
    return p

def issue(code,message,ids=None,severity='error',evidence=None):
    return dict(id='issue_'+digest([code,message,ids])[:16],code=code,severity=severity,message=message,object_ids=ids or [],evidence=evidence or {},status='open',source='local_rules')

class Service:
    def __init__(self,root=None):
        self.store=Store(Path(root or os.environ.get('STUDIO_DATA',ROOT/'data')))
        self.jobs=None
        shutil.copyfile(ROOT/'config/character-kit.json',self.store.root/'shared/profiles/character-kit-r1.json')

    def capabilities(self):
        return {'schema_versions':[SCHEMA],'engine':ENGINE,'actions':{
          'keyframes':{'properties':['x','y','scale','rotation','opacity'],'easing':['linear','smooth','hold']},
          'pose_swap':{'prerequisites':['builtin_character_v1'],'poses':['neutral','present','point_left','point_right','think','hold','pull']},
          'expression_swap':{'expressions':['neutral','curious','surprised','skeptical','happy']},
          'point_at':{'prerequisites':['character','target_node']},'look_at':{'prerequisites':['character','target_node']},
          'attach':{'prerequisites':['character_parent'],'slots':['hand_left','hand_right']},
          'reveal':{},'text_highlight':{},'camera':{'properties':['x','y','scale']},'transitions':['cut','dissolve'],
          'video_playback':False,'arbitrary_animation':False,'lip_sync':False},
          'rig':json.loads((ROOT/'config/character-kit.json').read_text('utf-8')),'workers':self.worker_profiles(),'media_observation':{'agent_audio_verified':False,'agent_full_video_verified':False},'active_agents':self.active_leases()}

    def active_leases(self):
        with self.store.lock:
            return [dict(r) for r in self.store.db.execute('SELECT project_id,actor,expiry FROM leases WHERE expiry>?',(time.time(),))]

    def worker_profiles(self):
        path=ROOT/'config'/'workers.json'
        if not path.exists():path=ROOT/'config'/'workers.example.json'
        configs=json.loads(path.read_text('utf-8')) if path.exists() else {}
        for key,p in configs.items():
            p['installed']=bool(p.get('python') and Path(p['python']).is_file() and p.get('model_path') and Path(p['model_path']).exists())
        return configs

    def doctor(self):
        mem=psutil.virtual_memory();disk=shutil.disk_usage(self.store.root)
        gpu=[]
        if shutil.which('nvidia-smi'):
            try: gpu=run(['nvidia-smi','--query-gpu=name,memory.total,memory.free,driver_version','--format=csv,noheader,nounits'],15).decode().strip().splitlines()
            except StudioError: pass
        return {'python':os.sys.version.split()[0],'node':shutil.which('node'),'ffmpeg':shutil.which('ffmpeg'),'ffprobe':shutil.which('ffprobe'),'edge':Path(r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe').exists(),'ram_available_mb':mem.available//1048576,'ram_total_mb':mem.total//1048576,'disk_free_gb':round(disk.free/1024**3,1),'gpu':gpu,'workers':self.worker_profiles(),'font':str(Path(os.environ.get('WINDIR','C:/Windows'))/'Fonts'/'arial.ttf'),'bind':'127.0.0.1','models_loaded':False}

    def import_sources(self,pid,m,audio_path,srt_path):
        utterances=parse_srt(Path(srt_path).read_bytes())
        info=probe(audio_path)
        if not any(s.get('codec_type')=='audio' for s in info['streams']): raise StudioError('AUDIO_INVALID','File không có audio')
        def apply(p):
            base=self.store.root/'projects'/pid
            sources=[]
            for src,kind in [(Path(audio_path),'audio'),(Path(srt_path),'srt')]:
                sha=filehash(src);rel=f'source/{sha}{src.suffix.lower()}'
                dest=base/rel
                if not dest.exists():shutil.copyfile(src,dest)
                sources.append({'id':uid('source'),'content_hash':sha,'path':rel,'original_name':src.name,'kind':kind})
            aid=uid('audio');rel=f'working/{aid}.wav'
            run(['ffmpeg','-v','error','-i',audio_path,'-vn','-ar',str(RATE),'-ac','2','-c:a','pcm_s16le',base/rel])
            with wave.open(str(base/rel)) as f: count=f.getnframes()
            p['source_ids']=sources
            p['audio']={'id':aid,'source_hash':sources[0]['content_hash'],'pcm_hash':filehash(base/rel),'path':rel,'sample_rate':RATE,'sample_count':count,'edit_map':[],'parent_id':None}
            p['utterances']=utterances;p['words']=[];p['plan']=None;p['committed_plan']=None;p['timeline']=None
            p['issues']=[issue('SRT_UNVERIFIED','Mốc SRT chưa được căn với giọng đọc',severity='warning')]
            for u in utterances:
                if u['end_sample']>count:p['issues'].append(issue('AUDIO_TEXT_MISMATCH','Cue vượt thời lượng audio',[u['id']]))
            p['content_status']='audio_ready';p['validation_status']='not_checked'
            return {'audio_revision':aid,'utterance_count':len(utterances),'sample_count':count}
        return self.store.mutate(pid,m,'project_import',apply)

    def anchor_sample(self,p,a):
        if a['audio_revision']!=p['audio']['id']:raise StudioError('STALE_DEPENDENCY','Anchor trỏ audio cũ')
        if a.get('manual_sample') is not None:base=a['manual_sample']
        else:
            kind='words' if a.get('word_id') else 'utterances';key=a.get('word_id') or a.get('utterance_id')
            obj=next((x for x in p[kind] if x['id']==key),None)
            if not obj or obj.get(a['edge']+'_sample') is None:raise StudioError('ANCHOR_UNRESOLVED','Không có timestamp cho anchor',{'id':key})
            if kind=='words' and obj.get('evidence_status')=='unresolved':raise StudioError('ANCHOR_UNRESOLVED','Word chưa căn được',{'id':key})
            base=obj[a['edge']+'_sample']
        return base+a['offset_samples']

    def preflight(self,p):
        errors=[];plan=p.get('plan')
        if not p.get('audio'):return [issue('AUDIO_MISSING','Cần nhập audio')]
        if not plan:return [issue('PLAN_MISSING','Cần agent lập kế hoạch hoặc nhập kế hoạch')]
        if plan['audio_revision']!=p['audio']['id']:errors.append(issue('STALE_DEPENDENCY','Plan trỏ audio cũ'))
        scenes=plan['scenes'];last=0;ids=set();assets={a['id']:a for a in p['assets']};utterances={u['id'] for u in p['utterances']}
        if any(u['start_sample'] is None or u['end_sample'] is None for u in p['utterances']):errors.append(issue('ANCHOR_UNRESOLVED','Câu trong audio chỉnh sửa còn chưa căn được'))
        event_ids=[e['id'] for e in plan['events']]
        if len(event_ids)!=len(set(event_ids)):errors.append(issue('DUPLICATE_ID','Event ID trùng'))
        for s in scenes:
            if s['id'] in ids:errors.append(issue('DUPLICATE_ID','Scene ID trùng',[s['id']]))
            ids.add(s['id'])
            if s['start_sample']!=last or s['end_sample']<=s['start_sample']:errors.append(issue('TIMELINE_COVERAGE','Scenes cần liên tục, không trùng và có thời lượng dương',[s['id']]))
            last=s['end_sample']
            if s['transition_samples']>s['end_sample']-s['start_sample']:errors.append(issue('TRANSITION_INVALID','Transition dài hơn scene',[s['id']]))
            if set(s['utterance_ids'])-utterances:errors.append(issue('REFERENCE_MISSING','Utterance không tồn tại',[s['id']]))
            nodes={n['id']:n for n in s['nodes']}
            if len(nodes)!=len(s['nodes']):errors.append(issue('DUPLICATE_ID','Node ID trùng',[s['id']]))
            for n in s['nodes']:
                if n['kind']=='image' and (n['asset_id'] not in assets or not (self.store.root/'projects'/p['id']/assets[n['asset_id']]['path']).is_file()):errors.append(issue('ASSET_MISSING','Thiếu ảnh',[n['id']]))
                if n['parent_id'] and n['parent_id'] not in nodes:errors.append(issue('REFERENCE_MISSING','Parent node không tồn tại',[n['id']]))
                chain=set();cursor=n
                while cursor and cursor.get('parent_id'):
                    if cursor['id'] in chain:errors.append(issue('SCENE_CYCLE','Parent cycle',[n['id']]));break
                    chain.add(cursor['id']);cursor=nodes.get(cursor['parent_id'])
                if n['attachment'] and (not n['parent_id'] or nodes.get(n['parent_id'],{}).get('kind')!='character'):errors.append(issue('ATTACHMENT_INVALID','Đạo cụ cần character parent',[n['id']]))
                for prop,ks in n['keyframes'].items():
                    if len({k['sample'] for k in ks})!=len(ks):errors.append(issue('PROPERTY_CONFLICT','Keyframe cùng property/time',[n['id']]))
                    if any(k['sample']>p['audio']['sample_count'] for k in ks):errors.append(issue('TIME_OUT_OF_RANGE','Keyframe vượt audio',[n['id']]))
            for event in [e for e in plan['events'] if e['scene_id']==s['id']]:
                n=nodes.get(event['target_id'])
                if not n:errors.append(issue('REFERENCE_MISSING','Event target không tồn tại',[event['id']]));continue
                if event['action'] in ['pose_swap','expression_swap','point_at','look_at'] and n['kind']!='character':errors.append(issue('POSE_UNSUPPORTED','Action cần character rig',[event['id']]))
                if event['action'] in ['point_at','look_at'] and event['parameters'].get('target_id') not in nodes:errors.append(issue('REFERENCE_MISSING','Thiếu target để chỉ/nhìn',[event['id']]))
                if event['action']=='pose_swap' and event['parameters'].get('pose') not in self.capabilities()['actions']['pose_swap']['poses']:errors.append(issue('POSE_UNSUPPORTED','Pose chưa được hỗ trợ',[event['id']]))
                if event['action']=='expression_swap' and event['parameters'].get('expression') not in self.capabilities()['actions']['expression_swap']['expressions']:errors.append(issue('POSE_UNSUPPORTED','Expression chưa được hỗ trợ',[event['id']]))
                if event['action']=='attach':
                    parent=nodes.get(event['parameters'].get('parent_id'))
                    if not parent or parent['kind']!='character' or event['parameters'].get('slot') not in ['hand_left','hand_right']:errors.append(issue('ATTACHMENT_INVALID','Attach event cần character và slot hợp lệ',[event['id']]))
                try:
                    sample=self.anchor_sample(p,event['anchor'])
                    if not s['start_sample']<=sample<s['end_sample']:errors.append(issue('TIME_OUT_OF_RANGE','Event ngoài scene',[event['id']]))
                except StudioError as e:errors.append(issue(e.code,e.message,[event['id']]))
        if last!=p['audio']['sample_count']:errors.append(issue('TIMELINE_COVERAGE','Plan phải phủ đúng audio master'))
        for e in plan['events']:
            if e['scene_id'] not in ids:errors.append(issue('REFERENCE_MISSING','Event scene không tồn tại',[e['id']]))
        properties={'pose_swap':'pose','expression_swap':'expression','reveal':'reveal','attach':'parent','point_at':'point','look_at':'look','text_highlight':'highlight'}
        seen=set()
        for e in plan['events']:
            try:
                prop=properties[e['action']];frame=frame_at(self.anchor_sample(p,e['anchor']),p['output_profile']['fps_num'],p['output_profile']['fps_den'],e['anchor']['quantization']);key=(e['scene_id'],e['target_id'],prop,frame)
                if key in seen:errors.append(issue('PROPERTY_CONFLICT','Hai action ghi cùng property/frame',[e['id']]))
                seen.add(key)
            except StudioError:pass
        for c in plan['claims']:
            if c.get('verification_status')!='verified' and c.get('certainty_type')=='fact':errors.append(issue('CLAIM_UNVERIFIED','Dữ kiện khẳng định chưa có xác minh',[c.get('id','claim')],severity='warning'))
        return errors

    def write_plan(self,pid,m):
        plan=EpisodePlan.model_validate(m.data['plan']).model_dump()
        def apply(p):
            p['plan']=plan;p['committed_plan']=None;p['timeline']=None;p['content_status']='planning';p['validation_status']='not_checked'
            return {'scene_ids':[s['id'] for s in plan['scenes']]}
        return self.store.mutate(pid,m,'plan_write',apply)

    def patch_plan(self,pid,m):
        def apply(p):
            if not p['plan']:raise StudioError('PLAN_MISSING','Chưa có kế hoạch')
            touched=[]
            for change in m.data['patches']:
                group=change['collection'];oid=change['id']
                if group not in ['scenes','events','asset_requests','claims','entities']:raise StudioError('PATCH_INVALID','Collection không hỗ trợ')
                obj=next((o for o in p['plan'][group] if o['id']==oid),None)
                if obj is None:raise StudioError('REFERENCE_MISSING','Patch ID không tồn tại')
                if 'id' in change['changes']:raise StudioError('PATCH_INVALID','Không đổi ID')
                obj.update(change['changes']);touched.append(oid)
            p['plan']=EpisodePlan.model_validate(p['plan']).model_dump();p['committed_plan']=None;p['timeline']=None;p['content_status']='planning';p['validation_status']='not_checked'
            return {'touched_objects':touched,'assets_preserved':True,'audio_preserved':True}
        return self.store.mutate(pid,m,'plan_patch',apply)

    def commit(self,pid,m):
        def apply(p):
            issues=self.preflight(p)
            if any(x['severity']=='error' for x in issues):raise StudioError('PREFLIGHT_FAILED','Kế hoạch chưa đủ điều kiện',{'issues':issues})
            p['committed_plan']={'id':uid('plan'),'revision':p['revision']+1,'hash':digest(p['plan']),'plan':p['plan']};p['issues']=issues;p['content_status']='plan_committed';p['validation_status']='preflight_passed'
            return {'plan_hash':p['committed_plan']['hash']}
        return self.store.mutate(pid,m,'plan_commit',apply)

    def compile(self,pid,m):
        def apply(p):
            if not p['committed_plan']:raise StudioError('PLAN_NOT_COMMITTED','Cần chốt kế hoạch')
            issues=self.preflight(p)
            if any(i['severity']=='error' for i in issues):raise StudioError('PREFLIGHT_FAILED','Preflight không đạt',{'issues':issues})
            profile=p['output_profile'];num,den=profile['fps_num'],profile['fps_den']
            events=[]
            for e in p['plan']['events']:
                sample=self.anchor_sample(p,e['anchor']);frame=frame_at(sample,num,den,e['anchor']['quantization'])
                events.append(e|{'frame':frame,'sample':frame*RATE*den/num})
            spans=[];start=0;total=frame_at(p['audio']['sample_count'],num,den)
            for index,s in enumerate(p['plan']['scenes']):
                end=frame_at(s['end_sample'],num,den)
                if end<=start:raise StudioError('TIMELINE_COVERAGE','Scene ngắn hơn frame')
                dependencies=[s]
                if s['transition']=='dissolve' and index:dependencies.insert(0,p['plan']['scenes'][index-1])
                scene_ids={x['id'] for x in dependencies}
                used={n['asset_id'] for sc in dependencies for n in sc['nodes'] if n['asset_id']}
                key=digest({'scenes':dependencies,'events':[e for e in events if e['scene_id'] in scene_ids],'assets':[{k:a[k] for k in ['id','content_hash','revision']} for a in p['assets'] if a['id'] in used],'profile':profile,'engine':ENGINE,'rig_hash':filehash(ROOT/'config/character-kit.json'),'font':filehash(Path(os.environ.get('WINDIR','C:/Windows'))/'Fonts/arial.ttf')})
                spans.append({'id':'span_'+key[:16],'start_frame':start,'end_frame':end,'dependency_hash':key,'render_profile_hash':digest(profile),'status':'pending'});start=end
            used_assets={n['asset_id'] for scene in p['plan']['scenes'] for n in scene['nodes'] if n['asset_id']}
            timeline={'schema_version':SCHEMA,'engine':ENGINE,'rig':json.loads((ROOT/'config/character-kit.json').read_text('utf-8')),'audio_revision':p['audio']['id'],'frame_count':total,'output_profile':profile,'scenes':p['plan']['scenes'],'events':events,'spans':spans,'assets':[a for a in p['assets'] if a['id'] in used_assets]}
            timeline['hash']=digest(timeline);p['timeline']=timeline;p['content_status']='timeline_ready'
            return {'timeline_hash':timeline['hash'],'frame_count':total,'spans':spans}
        return self.store.mutate(pid,m,'timeline_compile',apply)

    def register_asset(self,pid,m,path):
        path=Path(path)
        if path.suffix.lower() not in ['.png','.jpg','.jpeg','.webp','.wav','.mp3','.flac']:raise StudioError('MEDIA_UNSUPPORTED','Chỉ nhập raster image hoặc audio; SVG dùng kit có cấu trúc')
        license_record=m.data.get('license_record')
        if not license_record:raise StudioError('LICENSE_UNRESOLVED','Cần khai nguồn/quyền dùng')
        sha=filehash(path)
        def apply(p):
            old=next((a for a in p['assets'] if a['content_hash']==sha),None)
            if old:return {'asset_id':old['id'],'cache_hit':True}
            aid=uid('asset');rel=f'assets/{sha}{path.suffix.lower()}'
            shutil.copyfile(path,self.store.root/'projects'/pid/rel)
            media='image' if path.suffix.lower() in ['.png','.jpg','.jpeg','.webp'] else 'audio'
            dimensions=None;alpha='not_applicable'
            if media=='image':
                from PIL import Image
                with Image.open(path) as im:
                    im.load();dimensions=list(im.size);alpha='present' if 'A' in im.getbands() and im.getchannel('A').getextrema()[0]<255 else 'opaque'
            a=dict(id=aid,content_hash=sha,path=rel,media_type=media,dimensions=dimensions,alpha_status=alpha,source=m.data.get('source','user_import'),license_record=license_record,generation_record=m.data.get('generation_record'),revision=1,name=m.data.get('name',path.name))
            p['assets'].append(a);return {'asset_id':aid,'metadata':a}
        return self.store.mutate(pid,m,'asset_register',apply)

    def audio_edits(self,pid,m):
        def apply(p):
            if p['policies']['narration_edits']!='allowed':raise StudioError('POLICY_BLOCKED','Dự án đang giữ nguyên narration')
            old=p['audio'];base=self.store.root/'projects'/pid;aid=uid('audio');rel=f'working/{aid}.wav'
            kind=m.data['kind']
            if kind=='gain':
                gain=float(m.data['gain_db'])
                if not -60<=gain<=12:raise StudioError('EDIT_INVALID','Gain ngoài phạm vi')
                run(['ffmpeg','-v','error','-i',base/old['path'],'-af',f'volume={gain}dB','-c:a','pcm_s16le',base/rel])
                editmap=[{'kind':'gain','gain_db':gain}]
            elif kind=='trim':
                a,b=int(m.data['start_sample']),int(m.data['end_sample'])
                if not 0<=a<b<=old['sample_count']:raise StudioError('EDIT_INVALID','Khoảng cắt không hợp lệ')
                with wave.open(str(base/old['path'])) as src:
                    params=src.getparams();samples=src.readframes(src.getnframes());stride=src.getsampwidth()*src.getnchannels()
                with wave.open(str(base/rel),'wb') as dst:dst.setparams(params);dst.writeframes(samples[:a*stride]+samples[b*stride:])
                shift=b-a;editmap=[{'source':[0,a],'target':[0,a]},{'source':[b,old['sample_count']],'target':[a,old['sample_count']-shift]}]
                for u in p['utterances']+p['words']:
                    if u.get('start_sample') is None:continue
                    if u['start_sample']>=b:u['start_sample']-=shift;u['end_sample']-=shift
                    elif u['end_sample']>a:u['start_sample']=None;u['end_sample']=None;u['evidence_status']='unresolved'
                p['committed_plan']=None;p['timeline']=None;p['validation_status']='stale';p['content_status']='planning'
                p['issues'].append(issue('ANCHOR_UNRESOLVED','Audio đổi thời lượng: cần sửa scenes và anchors vùng cắt',evidence={'removed_samples':[a,b]}))
            else:raise StudioError('EDIT_INVALID','Chỉ hỗ trợ gain hoặc trim có quyền')
            with wave.open(str(base/rel)) as f:count=f.getnframes()
            p['audio']=old|{'id':aid,'pcm_hash':filehash(base/rel),'path':rel,'sample_count':count,'parent_id':old['id'],'edit_map':editmap}
            for w in p['words']:w['audio_revision']=aid
            if kind=='gain':
                if p['plan']:
                    p['plan']['audio_revision']=aid
                    for e in p['plan']['events']:e['anchor']['audio_revision']=aid
                if p['committed_plan']:
                    p['committed_plan']['plan']=p['plan'];p['committed_plan']['hash']=digest(p['plan'])
                if p['timeline']:
                    p['timeline']['audio_revision']=aid;p['timeline']['hash']=digest({k:v for k,v in p['timeline'].items() if k!='hash'})
            return {'audio_revision':aid,'video_spans_preserved':kind=='gain','downstream_timing_stale':kind=='trim'}
        return self.store.mutate(pid,m,'audio_apply_edits',apply)

    def replace_asset(self,pid,m,path):
        from PIL import Image
        source=Path(path)
        if source.suffix.lower() not in ['.png','.jpg','.jpeg','.webp']:raise StudioError('MEDIA_UNSUPPORTED','Asset patch V1 chỉ thay raster image')
        if not m.data.get('license_record'):raise StudioError('LICENSE_UNRESOLVED','Ảnh thay thế cần quyền dùng')
        with Image.open(source) as im:
            im.load();dimensions=list(im.size);alpha='present' if 'A' in im.getbands() and im.getchannel('A').getextrema()[0]<255 else 'opaque'
        sha=filehash(source)
        def apply(p):
            old=next((a for a in p['assets'] if a['id']==m.data['asset_id']),None)
            if not old or old['media_type']!='image':raise StudioError('ASSET_MISSING','Asset image không tồn tại')
            selected=set(m.data['scene_ids']);scenes=(p.get('plan') or {}).get('scenes',[])
            if not selected or selected-{s['id'] for s in scenes}:raise StudioError('REFERENCE_MISSING','Scene patch không hợp lệ')
            aid=uid('asset');rel=f'assets/{sha}{source.suffix.lower()}';target=self.store.root/'projects'/pid/rel
            if not target.exists():shutil.copyfile(source,target)
            a=old|{'id':aid,'path':rel,'content_hash':sha,'dimensions':dimensions,'alpha_status':alpha,'revision':old['revision']+1,'license_record':m.data['license_record'],'source':m.data.get('source','user_replacement'),'generation_record':m.data.get('generation_record'),'parent_asset_id':old['id']}
            p['assets'].append(a);touched=[]
            for s in scenes:
                if s['id'] in selected:
                    for n in s['nodes']:
                        if n['asset_id']==old['id']:n['asset_id']=aid;touched.append(n['id'])
            if not touched:raise StudioError('REFERENCE_MISSING','Các scene chọn không dùng asset này')
            p['committed_plan']=None;p['timeline']=None;p['content_status']='planning';p['validation_status']='not_checked'
            return {'new_asset_id':aid,'previous_asset_id':old['id'],'touched_nodes':touched,'source_preserved':True,'motion_preserved':True}
        return self.store.mutate(pid,m,'asset_patch',apply)

    def backup(self,pid):
        p=self.store.get(pid);base=self.store.root/'projects'/pid
        target=base/'exports'/f'backup-r{p["revision"]}-{uid("backup")}.zip'
        files={v['path'] for v in p['source_ids']+p['assets']}
        if p['audio']:files.add(p['audio']['path'])
        checks={rel:filehash(base/rel) for rel in files}
        with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as z:
            z.writestr('manifest.json',json.dumps(p,ensure_ascii=False,indent=2));z.writestr('checksums.json',json.dumps(checks))
            for rel in files:z.write(base/rel,rel)
        return {'path':str(target),'revision':p['revision'],'checksums':len(checks)}

    def restore(self,path):
        with zipfile.ZipFile(path) as z:
            if sum(i.file_size for i in z.infolist())>20*1024**3:raise StudioError('BACKUP_INVALID','Backup quá lớn')
            p=json.loads(z.read('manifest.json'));checks=json.loads(z.read('checksums.json'))
            if p.get('schema_version')!=SCHEMA:raise StudioError('SCHEMA_INCOMPATIBLE','Schema backup chưa hỗ trợ')
            original=p['id'];new=self.store.create(p['name']+' — phục hồi',p['policies'],p['output_profile']);pid=new['id'];base=self.store.root/'projects'/pid
            for rel,sha in checks.items():
                dest=bounded_path(base/rel,[base])
                data=z.read(rel)
                if hashlib.sha256(data).hexdigest()!=sha:raise StudioError('BACKUP_INVALID','Checksum không khớp')
                dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
            p['id']=pid;p['revision']=0;p['exports']=[]
            with self.store.lock,self.store.db:
                self.store.db.execute('UPDATE projects SET state=? WHERE id=?',(json.dumps(p,ensure_ascii=False),pid))
                self.store.db.execute('UPDATE revisions SET state=? WHERE project_id=? AND revision=0',(json.dumps(p,ensure_ascii=False),pid))
            self.store.snapshot(p)
            return {'project_id':pid,'original_id':original,'revision':0}
