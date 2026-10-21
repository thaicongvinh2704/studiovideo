"""Generate new Vietnamese voices with official VoxCPM2 Voice Design, no references."""
import json
from pathlib import Path
import sys
import time
import argparse

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from create_maya_directed_ab import digest,run_ff,measure

OUT=ROOT/'projects/mo_den_maya/voice_direction/custom_voice_design_v1'
TEXT=('Xin chào! Khoan đã, bạn vừa nghe thấy gì thế? '
      'Một chiếc đồng hồ đang chạy, một chú chim đang hót, hay chỉ là chiếc bụng đang đòi ăn? '
      'Hôm nay, chúng ta thử kể một câu chuyện thật nhỏ. '
      'Một người mang theo chiếc ô vào ngày nắng, nhưng lại quên mang ô khi trời mưa. '
      'Nghe quen quen nhỉ? Có những chuyện đơn giản mà nghĩ lại vẫn thấy buồn cười. '
      'Bây giờ, nghe rõ sáu thanh nhé: ma, má, mà, mả, mã, mạ. '
      'Hẹn gặp bạn lúc tám giờ ba mươi sáng ngày mai!')
COMMON=('Native Vietnamese male speaking only Vietnamese, Northern Vietnam Hanoi pronunciation, '
        'clearly articulated lexical tones. Young adult, medium register, light vocal weight, '
        'lively conversational delivery, playful and mischievous with a subtle smile. '
        'Brisk natural storytelling, clear meaningful phrasing, subtle pauses for comic timing, '
        'clean dry studio recording. ')
DESIGNS=[
    dict(id='01_mo_den_custom_A',prompt=COMMON+'Distinctively forward, agile, lightly nasal timbre with crisp consonants; witty, curious, friendly character voice. Natural adult pitch, restrained energy.'),
    dict(id='02_mo_den_custom_B',prompt=COMMON+'Rounded clear timbre, a little airy at phrase endings, nimble articulation, warm cheeky grin in the delivery. Medium pitch and relaxed throat, conversational intimacy.'),
    dict(id='03_mo_den_custom_C',prompt=COMMON+'A distinctive lightly grainy papery texture with bright clear vowels, springy phrasing, dry understated humor, medium speaking pitch, friendly impish personality.'),
]


def save(data,path):path.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')


def community_generate(text,prompt,download,seed):
    """Documented Gradio call/SSE API; the demo's API schema endpoint is broken."""
    import requests
    base='https://inmean-voxcpm2-demo.hf.space'
    response=requests.post(base+'/gradio_api/call/handle_generation',json=dict(data=[
        'tab_design',prompt,'',None,False,'',text,2.,10,False,False,False,seed]),timeout=30)
    response.raise_for_status();event_id=response.json()['event_id']
    response=requests.get(base+'/gradio_api/call/handle_generation/'+event_id,stream=True,timeout=(30,240))
    response.raise_for_status();event='';result=None
    for line in response.iter_lines(decode_unicode=True):
        if line.startswith('event:'):event=line[6:].strip()
        if line.startswith('data:'):
            data=json.loads(line[5:].strip())
            if event=='error':raise RuntimeError('Community generation failed: '+str(data))
            if event=='complete':result=data;break
    if not result or not result[0]:raise RuntimeError('Demo không trả audio: '+str(result))
    info=result[0];url=info.get('url')
    if not url:raise RuntimeError('Demo không trả URL audio hợp lệ.')
    from urllib.parse import urlparse,urljoin
    url=urljoin(base,url)
    if urlparse(url).hostname!='inmean-voxcpm2-demo.hf.space':raise RuntimeError('Audio ở host không mong đợi.')
    response=requests.get(url,timeout=60);response.raise_for_status();download.write_bytes(response.content)
    return download


def main():
    import numpy as np
    import soundfile as sf
    from gradio_client import Client
    parser=argparse.ArgumentParser();parser.add_argument('--service',choices=['official','community'],default='official')
    args=parser.parse_args()
    OUT.mkdir(exist_ok=True);work=OUT/'processing';work.mkdir(exist_ok=True)
    # After an egress review rejected project-containing text, only this newly
    # authored, anonymous public test paragraph is eligible for the remote demo.
    # No local media, project narration, character name, or source voice is sent.
    outbound=' '.join([TEXT,*[d['prompt'] for d in DESIGNS]])
    for forbidden in ['Mỏ Đen','Maya','EFp49inlLuQ','kcWEaXRh2hA','studiovideo','stickman-animation-studio']:
        if forbidden.casefold() in outbound.casefold():raise RuntimeError('Payload chứa thông tin dự án.')
    service='OpenBMB/VoxCPM-Demo' if args.service=='official' else 'inmean/voxcpm2-demo'
    save(dict(engine='VoxCPM2',service=service,
              text=TEXT,designs=DESIGNS,reference_wav_path_input=None,use_prompt_text=False,
              cfg_value_input=2.,do_normalize=False,denoise=False,
              voice_presets_used=False,previous_voice_audio_uploaded=False,
              public_generic_test_only=True,project_script_sent=False,character_identity_sent=False,
              pronunciation_edits=[],official_source='https://huggingface.co/openbmb/VoxCPM2'),OUT/'request.json')
    (OUT/'loi_doc_thu.txt').write_text(TEXT,encoding='utf-8')
    client=Client('OpenBMB/VoxCPM-Demo',verbose=False,download_files=str(work/'downloads'),analytics_enabled=False) if args.service=='official' else None
    rows=[]
    for i,d in enumerate(DESIGNS):
        print(f'Thiết kế giọng {i+1}/3: '+d['id'],flush=True)
        raw=work/(d['id']+'_original.audio')
        if not raw.is_file():
            if args.service=='community':
                result=community_generate(TEXT,d['prompt'],raw,20261021+i)
            else:
                for attempt in range(3):
                    try:
                        result=client.predict(text_input=TEXT,control_instruction=d['prompt'],
                            reference_wav_path_input=None,use_prompt_text=False,prompt_text_input='',
                            cfg_value_input=2.,do_normalize=False,denoise=False,api_name='/generate')
                        break
                    except Exception as exc:
                        if 'backend is busy' not in str(exc).lower() or attempt==2:raise
                        delay=20*(attempt+1)
                        print(f'Demo đang bận; chờ {delay}s rồi thử lại ({attempt+1}/2).',flush=True)
                        time.sleep(delay)
            downloaded=Path(result)
            if not downloaded.is_file():raise RuntimeError('Demo chưa trả về file audio.')
            raw.write_bytes(downloaded.read_bytes())
        fast=work/(d['id']+'_125.wav')
        run_ff('-i',raw,'-af','rubberband=tempo=1.25:pitch=1:formant=preserved:pitchq=quality',
               '-ar',48000,'-ac',1,'-c:a','pcm_s16le',fast)
        rows.append(dict(**d,original_sha256=digest(raw),unmatched=fast,measurement=measure(fast)))
        save(dict(stage='generation',completed=i+1,total=3),OUT/'progress.json')
    target=min(-18.,*[r['measurement']['input_i']-r['measurement']['input_tp']-1.8 for r in rows])
    for r in rows:
        final=OUT/(r['id']+'.wav');m=r.pop('measurement')
        run_ff('-i',r.pop('unmatched'),'-af',f'volume={target-m["input_i"]:.9f}dB','-c:a','pcm_s16le',final)
        audio,rate=sf.read(final,dtype='float32')
        if not audio.size or not np.isfinite(audio).all() or np.max(np.abs(audio))>=1:
            raise RuntimeError('File audio lỗi kỹ thuật.')
        run_ff('-i',final,'-f','null','-')
        r.update(file=final.name,seconds=len(audio)/rate,sha256=digest(final),loudness=measure(final))
    if max(r['loudness']['input_i'] for r in rows)-min(r['loudness']['input_i'] for r in rows)>.3:
        raise RuntimeError('Âm lượng các mẫu chưa tương đương.')
    save(dict(completed=True,engine='VoxCPM2',service=service,mode='Voice Design from natural-language descriptions only',
         reference_audio=None,preset=None,speed_multiplier=1.25,postprocess_pitch_shift_semitones=0,
         source_text_unchanged=True,variants=rows,
         regional_accent='Northern Vietnamese requested in prompt, NOT independently listening-verified.',
         listening_qc='Pending user listening: no claimed PASS for Vietnamese tones, spoken text completeness, naturalness, playfulness or accent.',
         persistence='Original generated audio preserved. Save a user-approved reference before producing multi-chunk full narration; new prompt generations are not guaranteed the same speaker.',
         default_voice_changed=False),OUT/'report.json')
    save(dict(stage='complete',completed=3,total=3),OUT/'progress.json')
    print('HOÀN TẤT: '+str(OUT),flush=True)


if __name__=='__main__':main()
