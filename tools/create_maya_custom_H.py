"""Full Maya narration with the user's selected local synthetic H speaker."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from studio.voice_direction import read_package, compile_excerpt, pause_padding_ms, space
from create_maya_directed_ab import BASE, PACKAGE, SUPPLIED, run_ff, measure, edge_silence
from create_maya_full_narration import timestamp

OUT = BASE / 'full_narration_custom_H_125'
LOCAL = ROOT / 'voices/local_design'
SPEED = 1.25


def sha(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')


def main():
    import numpy as np
    import soundfile as sf
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prepare', action='store_true')
    parser.add_argument('--limit', type=int)
    parser.add_argument('--cpu', action='store_true')
    parser.add_argument('--gpu-layers', type=int, default=29)
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    raw_dir = OUT/'raw'; raw_dir.mkdir(exist_ok=True)
    units_dir = OUT/'units'; units_dir.mkdir(exist_ok=True)
    profile_path = BASE/'selected_voice_H.json'
    profile = json.loads(profile_path.read_text(encoding='utf-8'))
    for key, hash_key in [('reference','reference_sha256'),('selected_audition','selected_audition_sha256')]:
        if sha(ROOT/profile[key]) != profile[hash_key]:
            raise RuntimeError('Selected H source changed: '+key)
    direction = read_package(PACKAGE, SUPPLIED)
    plan = compile_excerpt(direction,direction['source_cues'][0]['id'],direction['source_cues'][-1]['id'])
    if space(' '.join(u['text'] for u in plan)) != space((PACKAGE/'01_Loi_Ke_Sach.txt').read_text(encoding='utf-8-sig')):
        raise RuntimeError('Full input text differs')
    covered = [c for u in plan for c in u['source_cue_ids']]
    if covered != [c['id'] for c in direction['source_cues']]:
        raise RuntimeError('Missing or duplicate source cue')
    save(OUT/'directed_plan.json',plan)
    (OUT/'loi_doc_day_du.txt').write_text('\n\n'.join(b['text'] for b in direction['beats']),encoding='utf-8')
    reference = OUT/'H_reference_native_16k.wav'
    if not reference.exists():
        run_ff('-i',ROOT/profile['reference'],'-ar',16000,'-ac',1,'-c:a','pcm_s16le',reference)
    model_paths = [LOCAL/'models/VoxCPM2-BaseLM-Q8_0.gguf',LOCAL/'models/VoxCPM2-Acoustic-F16.gguf']
    runtime = LOCAL/('build-cpu' if args.cpu else 'build-vulkan')/'bin/studio-voice-batch.exe'
    settings = dict(reference_sha256=sha(reference),models={p.name:sha(p) for p in model_paths},
                    engine='VoxCPM2 GGUF clone API',seed=284617,max_steps=350,timesteps=10,cfg=2.,temperature=1.,
                    text_normalization='Original Vietnamese text, no aliases or punctuation replacements',
                    reference_rate=16000,reference_origin='Unretimed native original of selected H',
                    backend='CPU' if args.cpu else 'Vulkan',gpu_layers=0 if args.cpu else args.gpu_layers)
    settings['context_capacity']=2048
    settings['reference_prefill']='Compact active patches; one-reference cache in a single-model batch process; numerical compaction error verified 0'
    jobs=[]
    for i,unit in enumerate(plan):
        request=dict(settings,text=unit['text'])
        key=hashlib.sha256(json.dumps(request,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
        raw=raw_dir/(key+'.wav'); marker=raw.with_suffix('.wav.json')
        if raw.exists() and not marker.exists():
            raw.rename(raw.with_suffix('.orphan.wav'))
        if marker.exists():
            old=json.loads(marker.read_text(encoding='utf-8'))
            if old['text']!=unit['text'] or not old.get('complete'):raise RuntimeError('Cache mismatch')
        jobs.append(dict(id=i+1,text=unit['text'],seed=284617,output=str(raw)))
    job=dict(base_lm=str(model_paths[0]),acoustic=str(model_paths[1]),reference=str(reference),
             gpu=not args.cpu,gpu_layers=args.gpu_layers,threads=6,max_steps=350,units=jobs[:args.limit])
    save(OUT/'batch_job.json',job)
    save(OUT/'effective_config.json',dict(profile=profile,settings=settings,beats=len(direction['beats']),
         semantic_units=len(plan),source_cues=len(covered),speed_multiplier=SPEED,pitch_multiplier=1.,
         source_files={p.name:sha(p) for p in PACKAGE.iterdir() if p.is_file()},
         reading_edit_ledger=[],emphasis_scope='Modest whole semantic unit gain/pace, no aligned syllable control',
         independent_listening_qc='Pending; selected short audition does not pass all narration'))
    if args.prepare:
        print(f'Prepared {len(plan)} units / {len(covered)} source cues',flush=True);return
    if not runtime.exists():raise RuntimeError('Batch runtime not built: '+str(runtime))
    runtime_provenance=dict(executable=str(runtime.relative_to(ROOT)),sha256=sha(runtime),
         wrapper_sha256=sha(LOCAL/'driver/batch.cpp'),upstream_commit='a64932ec615e1463158129feaf2f0752d0c07a2e')
    history_path=OUT/'runtime_history.json'
    history=json.loads(history_path.read_text(encoding='utf-8')) if history_path.exists() else []
    previous_path=OUT/'runtime_provenance.json'
    if previous_path.exists():
        previous=json.loads(previous_path.read_text(encoding='utf-8'))
        if previous not in history:history.append(previous)
    if runtime_provenance not in history:history.append(runtime_provenance)
    save(history_path,history);save(previous_path,runtime_provenance)
    with (OUT/'synthesis.log').open('a',encoding='utf-8') as log:
        environment=dict(os.environ,STUDIO_SINGLE_REFERENCE_CACHE='1')
        process=subprocess.Popen([str(runtime),str(OUT/'batch_job.json')],stdout=subprocess.PIPE,
              stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace',bufsize=1,
              env=environment,
              creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        for line in process.stdout:
            log.write(line);log.flush()
            if line.startswith(('DONE ','CACHED ','START ','BATCH_ERROR ')):
                print(line.strip(),flush=True)
                if line.startswith('DONE '):
                    progress=json.loads(line[5:])
                    save(OUT/'progress.json',dict(stage='synthesis',completed_units=progress['id'],
                         total_units=len(plan),last_unit_seconds=progress['seconds'],completed=False))
        code=process.wait()
    if code:raise RuntimeError('Local runtime failed; inspect synthesis.log')
    chosen_plan=plan[:args.limit]; chosen_jobs=jobs[:args.limit];rendered=[]
    for i,(unit,request) in enumerate(zip(chosen_plan,chosen_jobs)):
        raw=Path(request['output']);audio,rate=sf.read(raw,dtype='float32')
        if rate!=48000 or audio.ndim!=1 or not audio.size or not np.isfinite(audio).all():raise RuntimeError('Invalid raw audio')
        if len(audio)/rate >=350*.16-.2:raise RuntimeError('Decode step limit reached; review unit '+str(i+1))
        filters=f'rubberband=tempo={unit["pace_multiplier"]}:pitch=1:formant=preserved,volume={unit["gain_db"]}dB'
        processed=units_dir/f'{i+1:03}.wav'
        run_ff('-i',raw,'-af',filters,'-ar',48000,'-ac',1,'-c:a','pcm_s16le',processed)
        audio,rate=sf.read(processed,dtype='float32')
        rendered.append(dict(file=processed,frames=len(audio),leading_ms=edge_silence(audio,rate),
                             trailing_ms=edge_silence(audio,rate,True),raw_sha256=sha(raw)))
    timeline=[];cursor=0;base=OUT/('Maya_H_native_directed.wav' if not args.limit else 'preview_native.wav')
    with sf.SoundFile(base,'w',samplerate=48000,channels=1,subtype='PCM_16') as target:
        for i,(unit,item) in enumerate(zip(chosen_plan,rendered)):
            audio,rate=sf.read(item['file'],dtype='float32');target.write(audio)
            start=cursor;cursor+=len(audio)
            leading=rendered[i+1]['leading_ms'] if i+1<len(rendered) else 0
            padding=pause_padding_ms(item['trailing_ms'],leading,unit['pause']['target_ms'])
            added=round(padding*48)
            timeline.append(dict(unit=i+1,text=unit['text'],beat_id=unit['beat_id'],source_cue_ids=unit['source_cue_ids'],
                     final_start_seconds=start/48000/SPEED,final_end_seconds=cursor/48000/SPEED,
                     pause=dict(unit['pause'],added_ms=added/48),raw_sha256=item['raw_sha256']))
            if added:target.write(np.zeros(added,dtype=np.float32));cursor+=added
    fast=OUT/'H_125_unmatched.wav'
    run_ff('-i',base,'-af','rubberband=tempo=1.25:pitch=1:formant=preserved:pitchq=quality',
           '-ar',48000,'-ac',1,'-c:a','pcm_s16le',fast)
    level=measure(fast);gain=min(-18-level['input_i'],-1.5-level['input_tp'])
    stem='Mo_Den_Maya_Custom_H_1_25x_'+('DAY_DU' if not args.limit else 'MO_DAU')
    final=OUT/(stem+'.wav');mp3=OUT/(stem+'.mp3')
    run_ff('-i',fast,'-af',f'volume={gain:.9f}dB','-ar',48000,'-ac',1,'-c:a','pcm_s16le',final)
    run_ff('-i',final,'-c:a','libmp3lame','-b:a','192k',mp3)
    info=sf.info(final);peak=0.
    for block in sf.blocks(final,blocksize=480000,dtype='float32'):
        if not np.isfinite(block).all():raise RuntimeError('Nonfinite final audio')
        peak=max(peak,float(np.max(np.abs(block))))
    if peak>=1 or abs(info.duration-cursor/48000/SPEED)>.15:raise RuntimeError('Final integrity failed')
    for file in [final,mp3]:run_ff('-i',file,'-f','null','-')
    suffix='full' if not args.limit else 'preview'
    save(OUT/f'timeline_{suffix}.json',dict(method='Measured semantic synthesis units / 1.25, approximate after time stretch',units=timeline))
    (OUT/f'Maya_H_{suffix}_CUM_Y.srt').write_text('\n\n'.join(
        f'{i+1}\n{timestamp(t["final_start_seconds"])} --> {timestamp(min(t["final_end_seconds"],info.duration))}\n{t["text"]}'
        for i,t in enumerate(timeline))+'\n',encoding='utf-8-sig')
    report=dict(completed=not bool(args.limit),generated_units=len(chosen_plan),total_units=len(plan),source_cues=covered,
                complete_input_text_covered_once=not bool(args.limit),final_seconds=info.duration,peak=peak,
                speed_multiplier=SPEED,additional_pitch_semitones=0,linear_gain_db=gain,loudness=measure(final),
                files={p.name:dict(sha256=sha(p),bytes=p.stat().st_size) for p in [final,mp3]},
                listening_qc='PENDING_USER_LISTENING: no independent listening or ASR; numeric checks do not prove tones, accent, speaker consistency, or no omitted/repeated spoken words.',
                pronunciation_review=direction['pronunciation_review'],video_rendered=False)
    save(OUT/f'report_{suffix}.json',report)
    for key, hash_key in [('reference','reference_sha256'),('selected_audition','selected_audition_sha256')]:
        if sha(ROOT/profile[key]) != profile[hash_key]:raise RuntimeError('Selected source was altered')
    save(OUT/'progress.json',dict(stage='complete' if not args.limit else 'preview_complete',
         completed_units=len(chosen_plan),total_units=len(plan),completed=not bool(args.limit)))
    print(json.dumps(dict(output=str(mp3),seconds=info.duration,units=len(chosen_plan)),ensure_ascii=False),flush=True)


if __name__=='__main__':main()
