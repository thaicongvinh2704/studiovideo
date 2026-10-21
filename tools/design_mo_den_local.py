"""Offline VoxCPM2 voice design: new speakers from descriptions, no voice samples."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from create_maya_directed_ab import digest,run_ff,measure

ENGINE=ROOT/'voices/local_design'
OUT=ROOT/'projects/mo_den_maya/voice_direction/local_custom_voices_v1'
TEXT=('Khoan đã! Nghe thì có lý, nhưng bằng chứng đâu? '
      'Mình là Mỏ Đen. Cùng mình soi từng dấu vết nhé. '
      'Đừng vội kéo người ngoài hành tinh vào, cứ để họ nghỉ một hôm đã! '
      'Có khi câu trả lời nằm ngay dưới chân mình đấy. '
      'Thử nghe sáu thanh: ma, má, mà, mả, mã, mạ.')
COMMON=('A young adult Vietnamese man speaking Vietnamese with Northern Hanoi pronunciation. '
        'Medium pitch, light vocal weight, clear Vietnamese tones, playful and mischievous, '
        'a subtle smile, nimble conversational storytelling, brisk natural pacing. ')
DESIGNS=[
    dict(id='01_custom_A',seed=20261021,prompt=COMMON+'Forward clear timbre, a hint of nasality, crisp consonants, friendly impish curiosity and dry understated humor.'),
    dict(id='02_custom_B',seed=20261022,prompt=COMMON+'Round smooth timbre with a little air at phrase endings, relaxed throat, warm cheeky delivery, quick witty phrasing.'),
    dict(id='03_custom_C',seed=20261023,prompt=COMMON+'Lightly grainy papery timbre, bright clear vowels, springy rhythmic phrasing, expressive curiosity and a restrained teasing smile.'),
]
FLAGS=getattr(subprocess,'CREATE_NO_WINDOW',0)


def save(path,data):
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')


def main():
    import numpy as np
    import soundfile as sf
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--only',choices=[d['id'] for d in DESIGNS])
    args=parser.parse_args()
    total=len(DESIGNS)
    if not total:raise ValueError('Chưa có thiết kế giọng.')
    OUT.mkdir(parents=True,exist_ok=True);rawdir=OUT/'originals';rawdir.mkdir(exist_ok=True)
    receipt=json.loads((ENGINE/'download_receipt.json').read_text(encoding='utf-8'))
    files=receipt['files']
    model_names=['VoxCPM2-BaseLM-Q8_0.gguf','VoxCPM2-Acoustic-F16.gguf']
    models=[ENGINE/'models'/name for name in model_names]
    for model in models:
        expected=next(x for x in files if x['path']=='models/'+model.name)
        if model.stat().st_size!=expected['bytes']:raise RuntimeError('Sai kích thước model.')
    # Model hashes were checked during setup. Recheck on first local audition run.
    verification=ENGINE/'local_model_verification.json'
    if not verification.is_file():
        checked=[]
        for model in models:
            expected=next(x for x in files if x['path']=='models/'+model.name)
            with model.open('rb') as model_stream:
                actual=hashlib.file_digest(model_stream,'sha256').hexdigest()
            if actual!=expected['sha256']:raise RuntimeError('Hash model sai.')
            checked.append(dict(file=model.name,sha256=actual))
        save(verification,dict(models=checked))
    exe=ENGINE/'build-cpu/bin/voxcpm2-cli.exe'
    if not exe.is_file():raise RuntimeError('Thiếu runtime đã biên dịch.')
    selected=ROOT/'voices/mo_den_EFp49inlLuQ_04.voice.json';before=digest(selected)
    config=dict(engine='VoxCPM2 Q8_0 BaseLM + F16 acoustic',backend='CPU',runtime_commit=receipt['runtime_commit'],
        binary_sha256=digest(exe),model_verification=str(verification.relative_to(ROOT)),
        mode='Voice Design',offline=True,reference_audio=None,preset=None,
        text=TEXT,normalization_edits=[],designs=DESIGNS,
        inference=dict(cfg=2.,timesteps=10,temperature=1.,max_steps=350,omp_threads=6),
        preview_speed_multiplier=1.25,postprocess_pitch_shift_semitones=0,
        regions='Northern Vietnamese requested by description; listening verification pending.',
        default_voice_changed=False)
    save(OUT/'effective_config.json',config)
    (OUT/'loi_doc_thu.txt').write_text(TEXT,encoding='utf-8')
    env=os.environ.copy();env['PATH']=str(ENGINE/'vendor/w64devkit/bin')+os.pathsep+env['PATH']
    env['OMP_NUM_THREADS']='6';env['HF_HUB_OFFLINE']='1'
    rows=[]
    for i,d in enumerate(DESIGNS):
        if args.only and d['id']!=args.only:continue
        original=rawdir/(d['id']+'_native.wav')
        native_text='('+d['prompt']+')'+TEXT
        request=dict(text=native_text,seed=d['seed'],binary=config['binary_sha256'],
                     inference=config['inference'],models=json.loads(verification.read_text(encoding='utf-8')))
        key=hashlib.sha256(json.dumps(request,ensure_ascii=False,sort_keys=True).encode()).hexdigest()
        marker=original.with_suffix('.json')
        print(f'Tạo giọng local {i+1}/{total}: {d["id"]}',flush=True)
        save(OUT/'progress.json',dict(stage='generation',current=d['id'],completed=len(rows),total=total))
        if not original.is_file() or not marker.is_file() or json.loads(marker.read_text()).get('key')!=key:
            log=OUT/(d['id']+'_runtime.log');tick=time.monotonic()
            command=[str(exe),'--cpu','--steps','350','--timesteps','10','--cfg','2',
                     '--temperature','1','--seed',str(d['seed']),'-t',native_text,'-o',str(original),*[str(m) for m in models]]
            with log.open('w',encoding='utf-8') as output:
                subprocess.run(command,env=env,stdout=output,stderr=subprocess.STDOUT,check=True,
                               creationflags=FLAGS,timeout=1500)
            logged=log.read_text(encoding='utf-8',errors='strict')
            if native_text not in logged:raise RuntimeError('Đầu vào tiếng Việt bị đổi mã hóa.')
            if 'Generation failed' in logged or 'WAV saved:' not in logged:raise RuntimeError('Model không hoàn tất.')
            save(marker,dict(key=key,request=request,elapsed_seconds=time.monotonic()-tick,original_sha256=digest(original)))
        audio,rate=sf.read(original,dtype='float32')
        if rate!=48000 or not len(audio) or not np.isfinite(audio).all() or float(np.max(np.abs(audio)))<.001:
            raise RuntimeError('Mẫu local lỗi hoặc im lặng.')
        # Hard decode limits can truncate a still-running sentence. Never hide this as success.
        if len(audio)/rate>=350/6.25-.5:raise RuntimeError('Chạm giới hạn thời lượng, cần kiểm tra kết thúc.')
        preview=rawdir/(d['id']+'_125_unmatched.wav')
        run_ff('-i',original,'-af','rubberband=tempo=1.25:pitch=1:formant=preserved:pitchq=quality',
               '-ar',48000,'-ac',1,'-c:a','pcm_s16le',preview)
        rows.append(dict(**d,native_seconds=len(audio)/rate,original_sha256=digest(original),
                         path=preview,measurement=measure(preview)))
        print(f'Xong bản gốc {d["id"]}: {len(audio)/rate:.2f}s',flush=True)
    target=min(-18.,*[r['measurement']['input_i']-r['measurement']['input_tp']-1.8 for r in rows])
    for r in rows:
        final=OUT/(r['id']+'_1_25x.wav');m=r.pop('measurement')
        run_ff('-i',r.pop('path'),'-af',f'volume={target-m["input_i"]:.9f}dB','-c:a','pcm_s16le',final)
        audio,rate=sf.read(final,dtype='float32')
        if not np.isfinite(audio).all() or float(np.max(np.abs(audio)))>=1:raise RuntimeError('Lỗi kỹ thuật bản nghe.')
        if abs(len(audio)/rate-r['native_seconds']/1.25)>.15:raise RuntimeError('Sai tỷ lệ tốc độ.')
        run_ff('-i',final,'-f','null','-')
        r.update(file=final.name,seconds=len(audio)/rate,sha256=digest(final),loudness=measure(final))
    if len(rows)>1 and max(r['loudness']['input_i'] for r in rows)-min(r['loudness']['input_i'] for r in rows)>.3:
        raise RuntimeError('Mức nghe các mẫu chưa tương đương.')
    if digest(selected)!=before:raise RuntimeError('Giọng mặc định bị đổi.')
    report=dict(completed=len(rows)==total,variants=rows,engine='VoxCPM2 local via llama.cpp-omni',
                offline=True,preset=None,reference_audio=None,new_speakers_by_description=True,
                default_voice_unchanged=True,preview_speed=1.25,
                listening_qc='PENDING_USER_LISTENING: pronunciation, full audible text, accent, naturalness and playfulness are not passed by technical checks.',
                persistence='Originals, descriptions and seeds retained. A new generation may vary; lock approved generated voice as a local reference before full production.')
    save(OUT/'report.json',report);save(OUT/'progress.json',dict(stage='complete',completed=len(rows),total=total))
    print('HOÀN TẤT '+str(OUT),flush=True)


if __name__=='__main__':main()
