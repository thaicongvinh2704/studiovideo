"""Three local Maya A/B excerpts, with a JSON-to-pipeline adapter and honest QC."""
import hashlib
import importlib.metadata
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from studio.voice_direction import read_package,compile_excerpt,pause_padding_ms,space
from studio.reference_voice import ReferenceSynthesizer,load_profile,postprocess_filters

BASE=ROOT/'projects/mo_den_maya/voice_direction'
PACKAGE=BASE/'input/Mo_Den_Maya_Dao_Dien_Giong_Viet'
OUT=BASE/'ab_samples'
PROFILE=ROOT/'voices/mo_den_EFp49inlLuQ_04.voice.json'
SUPPLIED=Path(r'C:\Users\ADMIN\Downloads\Mo_Den_Maya_Giong_Ke_Tu_Nhien (1).srt')
SLUGS=['01_mo_bai','02_muoi_ba_nam','03_nhin_lai_su_sup_do']
FLAGS=getattr(subprocess,'CREATE_NO_WINDOW',0)


def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def run_ff(*args, capture=False):
    return subprocess.run(['ffmpeg','-hide_banner','-loglevel','info' if capture else 'error',
                           '-y',*map(str,args)],check=True,capture_output=capture,creationflags=FLAGS)


def measure(path):
    result=run_ff('-i',path,'-af','loudnorm=I=-18:TP=-1.5:LRA=11:print_format=json',
                  '-f','null','-',capture=True)
    text=result.stderr.decode('utf-8',errors='replace')
    matches=re.findall(r'\{[^{}]*"input_i"[^{}]*\}',text,re.S)
    if not matches:raise RuntimeError('Không đo được mức nghe để so sánh.')
    d=json.loads(matches[-1])
    metrics={k:float(d[k]) for k in ['input_i','input_tp','input_lra','input_thresh']}
    if not all(math.isfinite(x) for x in metrics.values()):raise RuntimeError('Mẫu bị im lặng hoặc mức nghe lỗi.')
    return metrics


def edge_silence(audio,rate,from_end=False):
    """Estimate quiet edges only. Never use this estimate to cut speech."""
    import numpy as np
    x=audio[::-1] if from_end else audio
    frame=round(rate*.01);threshold=10**(-46/20);count=0
    for start in range(0,len(x),frame):
        block=x[start:start+frame]
        if float(np.sqrt(np.mean(block*block)))>threshold:break
        count+=len(block)
    return 1000*count/rate


def main():
    import numpy as np
    import soundfile as sf
    OUT.mkdir(parents=True,exist_ok=True)
    cache=OUT/'cache';cache.mkdir(exist_ok=True)
    direction=read_package(PACKAGE,SUPPLIED)
    profile=load_profile(PROFILE)
    if profile.get('region')!='Bắc' or profile.get('language')!='vi-VN':
        raise RuntimeError('Giọng/vùng giọng hiện tại chưa đúng lựa chọn người dùng.')
    original_profile_hash=digest(PROFILE)
    chosen=PROFILE.parent/profile['selected_audition'];chosen_hash=digest(chosen)
    if chosen_hash!=profile['selected_audition_sha256']:raise RuntimeError('Mẫu đã chốt bị đổi.')
    all_plan=[]
    for beat in direction['beats']:
        all_plan.append(dict(beat_id=beat['id'],intent=beat['intent'],title=beat['title'],
            units=compile_excerpt(direction,beat['source_cue_ids'][0],beat['source_cue_ids'][-1])))
    (OUT/'adapter_plan_36_beats.json').write_text(json.dumps(all_plan,ensure_ascii=False,indent=2),encoding='utf-8')
    input_files={p.name:digest(p) for p in PACKAGE.iterdir() if p.is_file()}
    (OUT/'input_integrity.json').write_text(json.dumps(dict(files=input_files,
        supplied_srt_sha256=digest(SUPPLIED),supplied_equals_packaged_srt=True,
        txt_equals_beats=True,srt_equals_source_cues=True,all_275_cues_covered_once=True),indent=2),encoding='utf-8')
    capabilities=dict(engine='VieNeu-TTS v3 Turbo',sdk=importlib.metadata.version('vieneu'),
        onnxruntime=importlib.metadata.version('onnxruntime'),sea_g2p=importlib.metadata.version('sea-g2p'),
        backend='CPU ONNX fp32',inference='vieneu.Vieneu(mode=v3turbo).infer',sample_rate=48000,
        verified_controls=['text','voice with speaker_emb + codes','temperature','top_k','max_chars'],
        seed='Fixed NumPy seed; local ONNX sampler uses np.random.choice. No public seed argument passed.',
        reference='Stored denoised 8-second Vietnamese reference; same codes for all six samples.',
        style='Ignored by installed v3 Turbo; no fake style/emotion arguments passed.',
        applied=['Meaningful complete-sentence grouping','Protected source cue spans','Pause events at complete inference boundaries, topping up existing silence',
                 'Modest whole-unit time stretch and gain when editorial pace/emphasis requests it'],
        approximate=['emphasis_phrases: entire semantic unit, not exact aligned words'],
        unsupported_or_unverified=['Guaranteed subtle emotional acting from tone/intent/direction labels',
            'Word-level alignment or precise stressed syllable placement','Independent listening validation of pronunciation, region and reference cleanliness'],
        metadata_not_spoken=['title','intent','delivery','pause_events','source cue numbers','timecodes'],
        engine_style_evidence='Installed vieneu/v3turbo.py infer; _v3_turbo_engine/onnx_runtime_lite.py _resolve_style_id',
        official_sources=['https://huggingface.co/pnnbao-ump/VieNeu-TTS-v3-Turbo','https://github.com/pnnbao97/VieNeu-TTS'],
        reference_quality='Denoised is not proof of no music/one speaker; independent listening remains pending.',
        no_paid_api=True,new_large_model_downloads=False)
    (OUT/'model_capabilities.json').write_text(json.dumps(capabilities,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Đã kiểm tra 36 beat, TXT/JSON/SRT khớp; chỉ dựng ba trích đoạn.',flush=True)
    os.environ['HF_HUB_OFFLINE']='1'
    synth=ReferenceSynthesizer();native=synth.engine
    from vieneu_utils.phonemize_text import normalize_to_chunks_v3_with_gaps
    with np.load(profile['codes_path'],allow_pickle=False) as z:
        voice=dict(speaker_emb=z['speaker_emb'].astype(np.float32),codes=z['codes'].astype(np.int64))
    results=[]
    for pair,(first,last) in enumerate(direction['ab_test']['excerpts_source_cues']):
        slug=SLUGS[pair];folder=OUT/slug;folder.mkdir(exist_ok=True)
        plan=compile_excerpt(direction,first,last)
        spoken=space(' '.join(u['text'] for u in plan))
        (folder/'loi_doc.txt').write_text(spoken,encoding='utf-8')
        (folder/'directed_plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
        seed=20261021+pair
        baseline=folder/'A_pipeline_hien_tai_unmatched.wav'
        config=dict(text=spoken,profile_sha256=original_profile_hash,seed=seed,
                    sdk=capabilities['sdk'],pipeline='current ReferenceSynthesizer.synthesize v1')
        key=hashlib.sha256(json.dumps(config,ensure_ascii=False,sort_keys=True).encode()).hexdigest()
        marker=baseline.with_suffix('.sha256')
        if not baseline.is_file() or not marker.is_file() or marker.read_text()!=key:
            print(f'{pair+1}/3 · A: '+slug,flush=True)
            np.random.seed(seed)
            synth.synthesize(spoken,PROFILE,baseline)
            marker.write_text(key)
        directed_parts=[];boundary_log=[];rendered=[]
        for index,unit in enumerate(plan):
            raw_key=dict(text=unit['text'],seed=seed,codes_sha256=profile['codes_sha256'],
                sdk=capabilities['sdk'],temperature=.6,top_k=25,max_chars=280)
            key=hashlib.sha256(json.dumps(raw_key,ensure_ascii=False,sort_keys=True).encode()).hexdigest()
            raw=cache/(key+'.wav')
            if not raw.is_file():
                print(f'{pair+1}/3 · B: cụm {index+1}/{len(plan)}',flush=True)
                np.random.seed(seed)
                audio=np.asarray(native.infer(unit['text'],voice=voice,temperature=.6,top_k=25,max_chars=280),dtype=np.float32)
                if not audio.size or not np.isfinite(audio).all():raise RuntimeError('Lỗi audio tổng hợp.')
                sf.write(raw,audio,native.sample_rate,subtype='PCM_16')
            chunks,gaps=normalize_to_chunks_v3_with_gaps(unit['text'],max_chars=280)
            if len(chunks)!=1:
                raise RuntimeError('Engine tự chia cụm nội bộ; cần duyệt lại để bảo vệ ranh giới: '+unit['text'])
            unit['actual_engine_chunks']=chunks;unit['actual_engine_gaps']=gaps
            processed=folder/f'B_unit_{index+1:02}.wav'
            filters=postprocess_filters(profile,unit['pace_multiplier'],10**(unit['gain_db']/20))
            run_ff('-i',raw,'-af',filters,'-ar',48000,'-ac',1,'-c:a','pcm_s16le',processed)
            audio,rate=sf.read(processed,dtype='float32')
            rendered.append((audio,unit))
        cursor=0.;directed_timing=[]
        for index,(audio,unit) in enumerate(rendered):
            directed_parts.append(audio)
            directed_timing.append(dict(start_seconds=cursor,end_seconds=cursor+len(audio)/48000,
                source_cue_ids=unit['source_cue_ids'],text=unit['text'],pause_target=unit['pause'],
                pace_multiplier=unit['pace_multiplier'],gain_db=unit['gain_db']))
            cursor+=len(audio)/48000
            trailing=edge_silence(audio,48000,True)
            leading=edge_silence(rendered[index+1][0],48000) if index+1<len(rendered) else 0.
            target=unit['pause']['target_ms']
            padding=pause_padding_ms(trailing,leading,target)
            if padding:
                silence=np.zeros(round(padding/1000*48000),dtype=np.float32)
                directed_parts.append(silence);cursor+=len(silence)/48000
            boundary_log.append(dict(after_source_cue=unit['source_cue_ids'][-1],
                requested_total_ms=target,estimated_existing_trailing_ms=trailing,
                estimated_next_leading_ms=leading,added_ms=padding,
                source=unit['pause']['source'],replaces_beat_pause=unit['pause']['replaces_beat_pause'],
                method='Complete sentence/inference boundary; quiet-edge estimate at -46 dBFS. No word cuts or silence trims.'))
        directed=folder/'B_dao_dien_json_unmatched.wav'
        sf.write(directed,np.concatenate(directed_parts),48000,subtype='PCM_16')
        measurements=[measure(p) for p in [baseline,directed]]
        target=min(-18.,*[m['input_i']-m['input_tp']-1.5 for m in measurements])
        final_files=[]
        for label,path,m in zip(['A','B'],[baseline,directed],measurements):
            final=folder/(label+('_pipeline_hien_tai.wav' if label=='A' else '_dao_dien_json.wav'))
            gain=target-m['input_i']
            run_ff('-i',path,'-af',f'volume={gain:.9f}dB','-ar',48000,'-ac',1,'-c:a','pcm_s16le',final)
            audio,rate=sf.read(final,dtype='float32');level=measure(final)
            if not np.isfinite(audio).all() or float(np.max(np.abs(audio)))>=1:
                raise RuntimeError('Lỗi kỹ thuật mẫu '+str(final))
            run_ff('-i',final,'-f','null','-')
            final_files.append(dict(version=label,file=str(final.relative_to(OUT)),
                seconds=round(len(audio)/rate,3),sha256=digest(final),loudness=level,
                linear_comparison_gain_db=gain,text_sha256=hashlib.sha256(spoken.encode()).hexdigest()))
        if abs(final_files[0]['loudness']['input_i']-final_files[1]['loudness']['input_i'])>.25:
            raise RuntimeError('Mức nghe A/B chưa tương đương.')
        result=dict(excerpt_source_cues=[first,last],slug=slug,seed=seed,
            text=spoken,text_origin='Exact spans of beats[].text; source_cues used only for traceability.',
            baseline_config=config,directed_units=plan,pause_log=boundary_log,directed_timing=directed_timing,
            comparison_target_lufs=target,audio=final_files,
            pronunciation_terms_in_excerpt=[t for t in direction['pronunciation_review']['terms'] if t.casefold() in spoken.casefold()],
            listening_status='CHƯA NGHE KIỂM TRA; không suy ra đạt từ chỉ số.',
            normalized_reading_edits=[],normalization_note='Giữ nguyên lời và chính tả tên; chỉ gộp khoảng trắng. Số đã viết bằng chữ. Không bịa phiên âm.')
        results.append(result)
        (folder/'report.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
        print('Xong '+slug+': '+', '.join(f"{v['version']} {v['seconds']}s" for v in final_files),flush=True)
    if digest(PROFILE)!=original_profile_hash or digest(chosen)!=chosen_hash:
        raise RuntimeError('Giọng đã chốt bị thay đổi trong lúc thử.')
    report=dict(scope='THREE_EXCERPT_PAIRS_ONLY',full_narration_generated=False,video_rendered=False,
        final_aligned_srt_generated=False,source_srt_reference_only=True,inputs=input_files,
        speaker_codes_sha256=profile['codes_sha256'],selected_voice_preserved=True,language='vi-VN',region='Bắc',
        model_capabilities_file='model_capabilities.json',all_36_beats_planned_not_synthesized=True,
        pronunciation_review={term:'Cần nghe/tra nguồn trước khi duyệt; chưa thêm phiên âm.' for term in direction['pronunciation_review']['terms']},
        listening_qc='PENDING_USER_LISTENING; assistant has no listening validation in this run.',
        results=results)
    (OUT/'ab_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Đủ ba cặp A/B. Chờ người dùng nghe; chưa làm toàn bài hoặc video.',flush=True)


if __name__=='__main__':main()
