"""Northern voice auditions aiming for a lighter, mischievous narrator."""
import hashlib
import json
import os
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from studio.reference_voice import ReferenceSynthesizer,postprocess_filters
from studio.voice_direction import pause_padding_ms
from create_maya_directed_ab import digest,run_ff,measure,edge_silence

OUT=ROOT/'projects/mo_den_maya/voice_direction/playful_auditions_v1'
PRESETS=ROOT/'voices/auditions/mo_den_20261021'
UNITS=[
    dict(text='Khoan đã! Một thành phố có đền đài đồ sộ, biết quan sát bầu trời, còn có cả cách lọc nước. Vậy mà người ta vẫn phải chuyển đi. Nghe hơi lạ nhỉ?',pace=1.,gain=.15,pause=300),
    dict(text='Mình là Mỏ Đen. Hôm nay, mình thử lần theo những dấu vết ấy. Nhưng đừng vội kéo người ngoài hành tinh vào nhé. Cứ để họ nghỉ một hôm đã!',pace=1.,gain=.3,pause=400),
    dict(text='Trước hết, thử nghĩ đơn giản thôi: nhà vẫn còn, đường vẫn đi được, nhưng nước thì thiếu. Đến lúc ấy, bạn sẽ cố ở lại, hay bắt đầu gói ghém đồ đạc?',pace=.99,gain=.15,pause=350),
    dict(text='Và nhớ nhé, người Maya không biến mất. Họ vẫn sống đến hôm nay. Thứ chúng ta cần tìm hiểu là vì sao nhiều thành phố từng đông đúc lại dần vắng người.',pace=1.,gain=0,pause=250),
    dict(text='Một câu hỏi tưởng nhỏ, mà mở ra cả đống chuyện. Nào, soi từng dấu vết một. Có khi câu trả lời nằm ngay ở chỗ mình vừa lướt qua đấy!',pace=1.,gain=.25,pause=200),
]
VARIANTS=[
    dict(id='01_adam_lanh_loi',preset='01_adam_bua',label='Adam · thử hướng lanh lợi',semitones=.4),
    dict(id='02_adam_sang_hon',preset='01_adam_bua',label='Adam · sắc giọng sáng hơn',semitones=.95),
    dict(id='03_xuan_vinh_nhe_hon',preset='02_xuan_vinh',label='Xuân Vĩnh · sắc giọng nhẹ hơn',semitones=.7),
]


def main():
    import numpy as np
    import soundfile as sf
    from vieneu_utils.phonemize_text import normalize_to_chunks_v3_with_gaps
    OUT.mkdir(exist_ok=True)
    work=OUT/'processing';work.mkdir(exist_ok=True)
    manifest=json.loads((PRESETS/'manifest.json').read_text(encoding='utf-8'))
    selected=ROOT/'voices/mo_den_EFp49inlLuQ_04.voice.json'
    before=digest(selected)
    for u in UNITS:
        chunks,gaps=normalize_to_chunks_v3_with_gaps(u['text'],max_chars=280)
        if len(chunks)!=1:raise RuntimeError('Engine chia cụm ngoài kế hoạch.')
        u['actual_engine_chunks']=chunks;u['actual_engine_gaps']=gaps
    os.environ['HF_HUB_OFFLINE']='1';engine=None;pending=[]
    for v in VARIANTS:
        entry=next(c for c in manifest['candidates'] if c['id']==v['preset'])
        if 'Bắc' not in entry['catalog_label']:raise RuntimeError('Sai vùng giọng danh mục.')
        audition=PRESETS/entry['file'];codes=PRESETS/(v['preset']+'_codes.npz')
        if digest(audition)!=entry['sha256']:raise RuntimeError('Mẫu gốc thay đổi.')
        with np.load(codes,allow_pickle=False) as z:
            voice=dict(speaker_emb=z['speaker_emb'].astype(np.float32),codes=z['codes'].astype(np.int64))
        print('Đang tạo '+v['label'],flush=True)
        recipe=dict(postprocess=dict(pitch_semitones=v['semitones'],tempo=1.,formant='preserved',
            equalizers=[dict(frequency=230,width=.8,gain=-1.5),dict(frequency=2800,width=.8,gain=.6)]))
        rendered=[]
        for i,u in enumerate(UNITS):
            key=hashlib.sha256(json.dumps(dict(text=u['text'],codes=digest(codes),seed=20261021,
                sdk='3.8.3',temperature=.6,top_k=25,max_chars=280),ensure_ascii=False,sort_keys=True).encode()).hexdigest()
            raw=work/(key+'.wav')
            if not raw.is_file():
                if engine is None:engine=ReferenceSynthesizer().engine
                np.random.seed(20261021)
                audio=np.asarray(engine.infer(u['text'],voice=voice,temperature=.6,top_k=25,max_chars=280),dtype=np.float32)
                if not audio.size or not np.isfinite(audio).all():raise RuntimeError('Audio tổng hợp lỗi.')
                sf.write(raw,audio,engine.sample_rate,subtype='PCM_16')
            processed=work/(v['id']+f'_{i+1:02}.wav')
            run_ff('-i',raw,'-af',postprocess_filters(recipe,u['pace'],10**(u['gain']/20)),
                   '-ar',48000,'-ac',1,'-c:a','pcm_s16le',processed)
            audio,rate=sf.read(processed,dtype='float32');rendered.append(audio)
        parts=[];pauses=[]
        for i,(audio,u) in enumerate(zip(rendered,UNITS)):
            parts.append(audio)
            next_leading=edge_silence(rendered[i+1],48000) if i+1<len(rendered) else 0
            padding=pause_padding_ms(edge_silence(audio,48000,True),next_leading,u['pause'])
            if padding:parts.append(np.zeros(round(padding*48),dtype=np.float32))
            pauses.append(dict(after_unit=i+1,total_target_ms=u['pause'],added_ms=padding))
        joined=work/(v['id']+'_joined.wav');sf.write(joined,np.concatenate(parts),48000,subtype='PCM_16')
        fast=work/(v['id']+'_125.wav')
        run_ff('-i',joined,'-af','rubberband=tempo=1.25:pitch=1:formant=preserved:pitchq=quality',
               '-ar',48000,'-ac',1,'-c:a','pcm_s16le',fast)
        pending.append(dict(**v,catalog_label=entry['catalog_label'],codes_sha256=digest(codes),
                            recipe=recipe,pauses=pauses,path=fast))
    levels=[measure(v['path']) for v in pending]
    target=min(-18.,*[m['input_i']-m['input_tp']-1.8 for m in levels])
    for v,m in zip(pending,levels):
        final=OUT/(v['id']+'.wav')
        run_ff('-i',v.pop('path'),'-af',f'volume={target-m["input_i"]:.9f}dB','-c:a','pcm_s16le',final)
        audio,rate=sf.read(final,dtype='float32')
        if not audio.size or not np.isfinite(audio).all() or np.max(np.abs(audio))>=1:raise RuntimeError('Lỗi file nghe.')
        run_ff('-i',final,'-f','null','-')
        v.update(file=final.name,seconds=len(audio)/rate,loudness=measure(final),sha256=digest(final))
        print(f'Xong {v["label"]}: {len(audio)/rate:.2f}s',flush=True)
    if max(v['loudness']['input_i'] for v in pending)-min(v['loudness']['input_i'] for v in pending)>.3:
        raise RuntimeError('Mức nghe chưa tương đương.')
    if digest(selected)!=before:raise RuntimeError('Hồ sơ giọng chính bị đổi.')
    report=dict(variants=pending,units=UNITS,speed=1.25,language='vi-VN',
        source_text='New audition script with light humor; not an edit of the production Maya script.',
        region='Northern according to preset catalog; listening confirmation pending.',
        expression_method='Saved preset performance plus playful wording, semantic grouping, modest phrase pace/gain and gaps. No unsupported emotion/style parameter.',
        pitch_method='Fixed small whole-track offsets, formant preserved; no emotional F0 contours.',
        listening_qc='Pending user listening; signal checks do not prove playfulness, pronunciation, tone accuracy or naturalness.',
        default_voice_unchanged=True,production_script_unchanged=True)
    (OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    (OUT/'loi_doc_thu.txt').write_text('\n\n'.join(u['text'] for u in UNITS),encoding='utf-8')


if __name__=='__main__':main()
