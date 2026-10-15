from pathlib import Path
import json,time,uuid,httpx,subprocess
ROOT=Path(__file__).resolve().parent.parent;rt=json.loads((ROOT/'runtime.json').read_text('utf-8'))
c=httpx.Client(base_url=rt['url'],headers={'Authorization':'Bearer '+rt['token']},timeout=60)
def api(method,path,data=None):
    r=c.request(method,'/api'+path,json=data);r.raise_for_status();return r.json()['result']
def mutation(p,data,reason,key):return {'expected_revision':p['revision'],'actor':'ui','change_reason':reason,'idempotency_key':key,'data':data}
def wait(jid,seconds=600):
    deadline=time.monotonic()+seconds
    while time.monotonic()<deadline:
        j=api('GET','/jobs/'+jid)
        if j['status']=='succeeded':return j
        if j['status'] in ['failed','blocked']:raise RuntimeError(json.dumps(j['error'],ensure_ascii=False))
        time.sleep(2)
    raise TimeoutError(jid)
reportfile=ROOT/'reports/speech-session.json'
if reportfile.exists():session=json.loads(reportfile.read_text('utf-8'));pid=session['project_id']
else:
    p=api('POST','/projects',{'name':'Kiểm chứng giọng local','policies':{'tts_replacement':'allowed'}});pid=p['id'];session={'project_id':pid};reportfile.write_text(json.dumps(session),encoding='utf-8')
p=api('GET','/projects/'+pid)
text='An không buông chiếc hộp. Cậu giữ nó trong tay, chuẩn bị di chuyển, rồi kéo chiếc hộp sang phải. Hành động này có ba bước: chuẩn bị, chuyển động và giữ yên. Chữ chỉ xuất hiện khi câu chuyện đến đúng thời điểm. Đây là dữ liệu minh họa để kiểm tra phần mềm, không phải một sự kiện lịch sử. Khoảng tĩnh cuối cùng giúp người xem nhìn rõ kết quả.'
if 'tts_job_id' not in session:
    job=api('POST',f'/projects/{pid}/jobs/tts_generate',mutation(p,{'profile':'vieneu-turbo-cpu','text':text},'Kiểm chứng TTS với giọng tồn tại trong SDK đã pin','tts-fixture-supported-voice'))
    session['tts_job_id']=job['job_id'];reportfile.write_text(json.dumps(session),encoding='utf-8')
tts=wait(session['tts_job_id']);audio=tts['result']['audio_path']
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',audio]));duration=float(probe['format']['duration'])
if not p['audio']:
    srt=ROOT/'reports'/'Giọng local thử.srt';ms=int(duration*1000);stamp=f'00:{ms//60000:02}:{ms//1000%60:02},{ms%1000:03}'
    srt.write_text('1\n00:00:00,000 --> '+stamp+'\n'+text+'\n',encoding='utf-8')
    api('POST',f'/projects/{pid}/import-paths',mutation(p,{'audio_path':audio,'srt_path':str(srt)},'Nhập speech fixture đã tạo local','import-generated-speech'))
p=api('GET','/projects/'+pid)
if 'asr_job_id' not in session:
    job=api('POST',f'/projects/{pid}/jobs/audio_analyze',mutation(p,{'profile':'whisper-medium-cpu'},'Một lần kiểm chứng ASR medium CPU','asr-fixture-compatible-decoder'));session['asr_job_id']=job['job_id'];reportfile.write_text(json.dumps(session),encoding='utf-8')
asr=wait(session['asr_job_id'])
report={'project_id':pid,'TTS':{'job_id':tts['id'],'duration_seconds':duration,'profile':'VieNeu Turbo CPU/ONNX fp32','audio_path':audio,'automatic_quality_retries':0},'ASR':{'job_id':asr['id'],'profile':'Whisper medium CPU int8','segments':len(asr['result']['segments']),'issues':asr['result']['issues']},'alignment':'Not run: default vi weights are CC-BY-NC-4.0; sentence/manual anchors remain available','observation':'Inference and file probe verified; no claim of having listened to full audio'}
(ROOT/'reports/speech-verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(report,ensure_ascii=False))
