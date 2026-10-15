"""Targeted real job cancellation/resume, cache and decoded A/V fiducial test."""
from pathlib import Path
import json,time,uuid,httpx,subprocess,array,math
ROOT=Path(__file__).resolve().parent.parent
rt=json.loads((ROOT/'runtime.json').read_text('utf-8'));session=json.loads((ROOT/'reports/integration-session.json').read_text('utf-8'))
c=httpx.Client(base_url=rt['url'],headers={'Authorization':'Bearer '+rt['token']},timeout=60)
def api(method,path,data=None):
    r=c.request(method,'/api'+path,json=data);r.raise_for_status();return r.json()['result']
def mutation(p,data,reason,key=None):return {'expected_revision':p['revision'],'actor':'ui','change_reason':reason,'idempotency_key':key or str(uuid.uuid4()),'data':data}
pid=session['project_id'];p=api('GET','/projects/'+pid)
original=api('GET','/jobs/'+session['job_id'])
assert original['status']=='succeeded'
# Add visible fiducials only to last scene; first two video spans must be reused.
nodes=p['plan']['scenes'][2]['nodes']
if not any(n['id']=='fiducial34' for n in nodes):
    import sys
    sys.path.insert(0,str(ROOT))
    from studio.contracts import Node
    for sec in [34,46]:nodes.append(Node(id='fiducial'+str(sec),kind='prop',shape='circle',x=1770,y=110,width=72,height=72,color='#ff0000',visible_from=sec*48000,visible_until=int((sec+.1)*48000)).model_dump())
    api('POST',f'/projects/{pid}/plan/patch',mutation(p,{'patches':[{'collection':'scenes','id':'scene_3','changes':{'nodes':nodes}}]},'V09: thêm fiducial để đo drift decode, không đổi biên tập'))
    p=api('GET','/projects/'+pid);api('POST',f'/projects/{pid}/plan/commit',mutation(p,{},'Chốt fixture có fiducial'))
    p=api('GET','/projects/'+pid);api('POST',f'/projects/{pid}/timeline/compile',mutation(p,{},'Compile spans kiểm chứng'))
p=api('GET','/projects/'+pid);jobdata={'test_pause_after_spans':2}
job=api('POST',f'/projects/{pid}/jobs/render',mutation(p,jobdata,'V06/V09: cancel và resume clip có fiducial','fiducial-render-checkpoint'))
duplicate=api('POST',f'/projects/{pid}/jobs/render',mutation(p,jobdata,'V06/V09: cancel và resume clip có fiducial','fiducial-render-checkpoint'))
assert duplicate['job_id']==job['job_id'] and duplicate['cache_hit']
jid=job['job_id'];deadline=time.monotonic()+240
cancelled=False
while time.monotonic()<deadline:
    j=api('GET','/jobs/'+jid)
    if j['status']=='running' and len(j['checkpoint'].get('spans',[]))>=2:
        api('POST','/jobs/'+jid+'/cancel',{});cancelled=True;break
    if j['status'] in ['succeeded','failed','blocked']:break
    time.sleep(.1)
if cancelled:
    while time.monotonic()<deadline:
        j=api('GET','/jobs/'+jid)
        if j['status']=='cancelled':break
        time.sleep(.2)
    assert j['status']=='cancelled'
    api('POST','/jobs/'+jid+'/resume',{})
while time.monotonic()<deadline:
    j=api('GET','/jobs/'+jid)
    if j['status']=='succeeded':break
    if j['status'] in ['failed','blocked']:raise RuntimeError(j['error'])
    time.sleep(1)
assert j['status']=='succeeded',j
assert j['result']['cached_spans']>=2
video=j['result']['mp4']
# Decode a narrow ROI: actual red fiducial is visible exactly at specified frames.
cmd=['ffmpeg','-v','error','-i',video,'-vf','crop=8:8:1766:106','-pix_fmt','rgb24','-f','rawvideo','pipe:1']
raw=subprocess.check_output(cmd);stride=8*8*3;video_markers=[];prev=False
for k in range(len(raw)//stride):
    block=raw[k*stride:(k+1)*stride];red=sum(block[i] for i in range(0,stride,3))/64;green=sum(block[i] for i in range(1,stride,3))/64
    current=red>180 and green<80
    if current and not prev:video_markers.append(k/30)
    prev=current
pcm=subprocess.check_output(['ffmpeg','-v','error','-i',video,'-map','0:a:0','-ac','1','-ar','48000','-f','s16le','pipe:1']);samples=array.array('h');samples.frombytes(pcm)
audio_markers=[];last=-100000
for i,v in enumerate(samples):
    if abs(v)>1000 and i-last>48000//2:audio_markers.append(i/48000);last=i
drifts=[]
for marker in video_markers:
    nearest=min(audio_markers,key=lambda a:abs(a-marker));drifts.append(abs(nearest-marker))
assert len(video_markers)==2 and max(drifts)<=1/30,(video_markers,audio_markers,drifts)
report={'V06':{'duplicate_job_id':True,'cancelled_after_checkpoint':cancelled,'resume_attempts':j['attempts'],'cached_spans':j['result']['cached_spans']},'V09':{'ffprobe':'passed','frame_count':j['result']['frame_count'],'video_markers':video_markers,'decoded_audio_markers':audio_markers,'drift_seconds':drifts,'max_allowed_seconds':1/30},'job_id':jid,'mp4':video,'fixture_audio':'synthetic tone, not Vietnamese speech'}
(ROOT/'reports/live-verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
session['verified_job_id']=jid;(ROOT/'reports/integration-session.json').write_text(json.dumps(session),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
