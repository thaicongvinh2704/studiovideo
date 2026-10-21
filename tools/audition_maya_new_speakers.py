"""Compare independent saved Northern presets with the Maya B delivery adapter."""
import json
import os
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from studio.reference_voice import ReferenceSynthesizer,postprocess_filters
from studio.voice_direction import pause_padding_ms
from create_maya_directed_ab import digest,run_ff,measure,edge_silence

BASE=ROOT/'projects/mo_den_maya/voice_direction'
OUT=BASE/'new_speakers_B_delivery'
PRESETS=ROOT/'voices/auditions/mo_den_20261021/batch_02'
IDS=['05_thien_minh','06_pham_tuyen']


def main():
    import numpy as np
    import soundfile as sf
    OUT.mkdir(exist_ok=True)
    work=OUT/'processing';work.mkdir(exist_ok=True)
    source=BASE/'full_narration_125'
    units=json.loads((source/'directed_plan.json').read_text(encoding='utf-8'))[:10]
    manifest=json.loads((PRESETS/'manifest.json').read_text(encoding='utf-8'))
    previous=json.loads((ROOT/'voices/mo_den_EFp49inlLuQ_04.voice.json').read_text(encoding='utf-8'))
    profile_before=digest(ROOT/'voices/mo_den_EFp49inlLuQ_04.voice.json')
    source_wav=source/'Mo_Den_Maya_Giong_B_1_25x_DAY_DU.wav'
    source_hash=digest(source_wav)
    timeline=json.loads((source/'timeline_cum_y.json').read_text(encoding='utf-8'))['units']
    end=timeline[9]['final_end_seconds']
    original=work/'00_B_goc.wav'
    run_ff('-i',source_wav,'-t',end,'-c:a','pcm_s16le',original)
    outputs=[dict(id='00_B_goc',voice='B gốc',path=original)]
    recipe=dict(postprocess=dict(pitch_semitones=0,tempo=previous['postprocess']['tempo'],
                                formant='preserved',equalizers=[]))
    os.environ['HF_HUB_OFFLINE']='1'
    engine=None
    for ident in IDS:
        entry=next(c for c in manifest['candidates'] if c['id']==ident)
        if 'Bắc' not in entry['catalog_label']:raise RuntimeError('Sai vùng giọng danh mục.')
        audition=PRESETS/entry['file']
        if digest(audition)!=entry['sha256']:raise RuntimeError('Mẫu preset thay đổi.')
        codes=PRESETS/(ident+'_codes.npz')
        if digest(codes)==previous['codes_sha256']:raise RuntimeError('Đã dùng lại giọng cũ.')
        with np.load(codes,allow_pickle=False) as z:
            voice=dict(speaker_emb=z['speaker_emb'].astype(np.float32),codes=z['codes'].astype(np.int64))
        folder=work/ident;folder.mkdir(exist_ok=True)
        print('Đang tạo giọng gốc khác: '+entry['voice'],flush=True)
        rendered=[]
        for i,unit in enumerate(units):
            raw=folder/f'{i+1:02}_raw.wav'
            if not raw.is_file():
                if engine is None:engine=ReferenceSynthesizer().engine
                np.random.seed(20261021)
                audio=np.asarray(engine.infer(unit['text'],voice=voice,temperature=.6,top_k=25,max_chars=280),dtype=np.float32)
                if not audio.size or not np.isfinite(audio).all():raise RuntimeError('Tổng hợp lỗi.')
                sf.write(raw,audio,engine.sample_rate,subtype='PCM_16')
            processed=folder/f'{i+1:02}.wav'
            run_ff('-i',raw,'-af',postprocess_filters(recipe,unit['pace_multiplier'],10**(unit['gain_db']/20)),
                   '-ar',48000,'-ac',1,'-c:a','pcm_s16le',processed)
            audio,rate=sf.read(processed,dtype='float32')
            rendered.append(audio)
        parts=[];pause_log=[]
        for i,(audio,unit) in enumerate(zip(rendered,units)):
            parts.append(audio)
            following=edge_silence(rendered[i+1],48000) if i+1<len(rendered) else 0
            target=unit['pause']['target_ms'] if i+1<len(rendered) else 0
            padding=pause_padding_ms(edge_silence(audio,48000,True),following,target)
            if padding:parts.append(np.zeros(round(padding*48),dtype=np.float32))
            pause_log.append(dict(after_source_cue=unit['source_cue_ids'][-1],target_ms=target,added_ms=padding))
        base=folder/'joined.wav';sf.write(base,np.concatenate(parts),48000,subtype='PCM_16')
        fast=work/(ident+'_125.wav')
        run_ff('-i',base,'-af','rubberband=tempo=1.25:pitch=1:formant=preserved:pitchq=quality',
               '-ar',48000,'-ac',1,'-c:a','pcm_s16le',fast)
        outputs.append(dict(id=ident,voice=entry['voice'],catalog_label=entry['catalog_label'],path=fast,
                            codes_sha256=digest(codes),original_audition_sha256=digest(audition),
                            uses_old_speaker_codes=False,pitch_shift_semitones=0,pause_log=pause_log))
    levels=[measure(o['path']) for o in outputs]
    target=min(-18.,*[m['input_i']-m['input_tp']-1.8 for m in levels])
    for o,m in zip(outputs,levels):
        final=OUT/(o['id']+'_Maya_1_25x.wav')
        gain=target-m['input_i']
        run_ff('-i',o['path'],'-af',f'volume={gain:.9f}dB','-c:a','pcm_s16le',final)
        audio,rate=sf.read(final,dtype='float32')
        if not audio.size or not np.isfinite(audio).all() or np.max(np.abs(audio))>=1:raise RuntimeError('Lỗi file nghe.')
        run_ff('-i',final,'-f','null','-')
        o.pop('path');o.update(file=final.name,seconds=len(audio)/rate,sha256=digest(final),loudness=measure(final))
        print(f'Xong {o["voice"]}: {len(audio)/rate:.2f}s',flush=True)
    if max(o['loudness']['input_i'] for o in outputs)-min(o['loudness']['input_i'] for o in outputs)>.3:
        raise RuntimeError('Mức nghe chưa tương đương.')
    if profile_before!=digest(ROOT/'voices/mo_den_EFp49inlLuQ_04.voice.json') or source_hash!=digest(source_wav):
        raise RuntimeError('Bản đã chọn bị thay đổi.')
    report=dict(speaker_strategy='Independent installed preset codes, not EQ/pitch variants of old B.',
        candidates=outputs,text_origin='First ten complete semantic units from the full B directed plan.',
        text='\n\n'.join(u['text'] for u in units),speed=1.25,language='vi-VN',
        region='Bắc according to installed catalog; pending listening confirmation.',
        rhythm='Same semantic boundaries, directed pace multipliers and gap targets as B; native timings vary.',
        old_speaker_not_used_for_new_candidates=True,preferred_voice_unchanged=True,
        scope='Two short auditions; no new full narration or video.',
        listening_qc='PENDING_USER_LISTENING: no claim of correct tone, naturalness or perceived dissimilarity from signal metrics.')
    (OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    (OUT/'loi_doc.txt').write_text(report['text'],encoding='utf-8')


if __name__=='__main__':main()
