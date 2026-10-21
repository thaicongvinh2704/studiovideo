"""Audition moderate timbre changes on the selected B narration; retain its timing."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from create_maya_directed_ab import digest, run_ff, measure

BASE = ROOT/'projects/mo_den_maya/voice_direction'
SOURCE = BASE/'full_narration_125'
OUT = BASE/'B_am_sac_rieng_v1'
VARIANTS = [
    dict(id='01_can_bang', name='Cân bằng', resonance_ratio=1.065, semitones=0,
         eq='highpass=f=65,equalizer=f=240:t=q:w=0.7:g=-1.3,equalizer=f=1100:t=q:w=0.8:g=-0.7,equalizer=f=3000:t=q:w=0.8:g=0.6'),
    dict(id='02_day_va_ro', name='Cộng hưởng dày hơn', resonance_ratio=.94, semitones=.25,
         eq='highpass=f=75,equalizer=f=220:t=q:w=0.7:g=-2,equalizer=f=800:t=q:w=0.8:g=-0.8,equalizer=f=3000:t=q:w=0.8:g=1.1'),
    dict(id='03_sang_gon', name='Cộng hưởng sáng hơn', resonance_ratio=1.10, semitones=-.25,
         eq='highpass=f=65,equalizer=f=300:t=q:w=0.7:g=0.5,equalizer=f=1800:t=q:w=0.8:g=-1.2,equalizer=f=4200:t=q:w=0.8:g=-0.7'),
]


def filters(v):
    # Rate change moves resonance and F0 together. Rubber Band compensates F0
    # and duration while preserving the shifted resonance of its input.
    ratio = v['resonance_ratio']
    rate = round(48000*ratio)
    actual = rate/48000
    pitch = 2**(v['semitones']/12)
    return (f'asetrate={rate},aresample=48000,'
            f'rubberband=tempo={1/actual:.12f}:pitch={pitch/actual:.12f}:'
            f'formant=preserved:pitchq=quality,{v["eq"]}')


def main():
    import numpy as np
    import soundfile as sf
    OUT.mkdir(exist_ok=True)
    original = json.loads((SOURCE/'report.json').read_text(encoding='utf-8'))
    source = SOURCE/'Mo_Den_Maya_Giong_B_1_25x_DAY_DU.wav'
    chosen_mp3 = SOURCE/'Mo_Den_Maya_Giong_B_1_25x_DAY_DU.mp3'
    originals = {p:digest(p) for p in [source,chosen_mp3,ROOT/'voices/mo_den_EFp49inlLuQ_04.voice.json']}
    for p in [source,chosen_mp3]:
        if digest(p)!=original['files'][p.name]['sha256']:raise RuntimeError('Bản B đã đổi.')
    timeline=json.loads((SOURCE/'timeline_cum_y.json').read_text(encoding='utf-8'))['units']
    # End on a complete semantic unit, including its existing tail, never at 55s blindly.
    duration=timeline[9]['final_end_seconds']
    raw_dir=OUT/'processing';raw_dir.mkdir(exist_ok=True)
    neutral=raw_dir/'00_B_goc_excerpt.wav'
    run_ff('-i',source,'-t',duration,'-ar',48000,'-ac',1,'-c:a','pcm_s16le',neutral)
    inputs=[neutral]; rows=[]
    for index,v in enumerate(VARIANTS):
        full=index==0
        work=raw_dir/(v['id']+'_unmatched.wav')
        run_ff('-i',source if full else neutral,'-af',filters(v),'-ar',48000,'-ac',1,'-c:a','pcm_s16le',work)
        clip=raw_dir/(v['id']+'_excerpt.wav')
        if full:run_ff('-i',work,'-t',duration,'-c:a','pcm_s16le',clip)
        else:clip=work
        inputs.append(clip)
        rows.append(dict(**v,filter=filters(v),work=work,excerpt=clip,full=full))
    levels=[measure(p) for p in inputs]
    target=min(-18,*[m['input_i']-m['input_tp']-1.8 for m in levels])
    output_rows=[]
    for index,(work,m) in enumerate(zip(inputs,levels)):
        slug='00_B_goc' if index==0 else rows[index-1]['id']
        preview=OUT/(slug+'_nghe_thu.wav')
        gain=target-m['input_i']
        run_ff('-i',work,'-af',f'volume={gain:.9f}dB','-c:a','pcm_s16le',preview)
        audio,rate=sf.read(preview,dtype='float32')
        if not np.isfinite(audio).all() or np.max(np.abs(audio))>=1:raise RuntimeError('Lỗi mẫu.')
        if abs(len(audio)/rate-duration)>.15:raise RuntimeError('Sai thời lượng mẫu.')
        level=measure(preview)
        output_rows.append(dict(id=slug,file=preview.name,seconds=len(audio)/rate,loudness=level,sha256=digest(preview)))
    if max(r['loudness']['input_i'] for r in output_rows)-min(r['loudness']['input_i'] for r in output_rows)>.3:
        raise RuntimeError('Mức nghe mẫu chưa tương đương.')
    full=OUT/'Mo_Den_Maya_B_Can_Bang_1_25x_DAY_DU.wav'
    level=measure(rows[0]['work'])
    gain=min(-18-level['input_i'],-1.8-level['input_tp'])
    run_ff('-i',rows[0]['work'],'-af',f'volume={gain:.9f}dB','-c:a','pcm_s16le',full)
    mp3=full.with_suffix('.mp3')
    run_ff('-i',full,'-c:a','libmp3lame','-b:a','192k',mp3)
    info=sf.info(full)
    if abs(info.duration-sf.info(source).duration)>.15:raise RuntimeError('Thời lượng toàn bài thay đổi.')
    for p in [full,mp3]:run_ff('-i',p,'-f','null','-')
    for block in sf.blocks(full,blocksize=480000,dtype='float32'):
        if not np.isfinite(block).all() or np.max(np.abs(block))>=1:raise RuntimeError('Lỗi audio toàn bài.')
    for p,h in originals.items():
        if digest(p)!=h:raise RuntimeError('Đã thay đổi bản gốc.')
    report=dict(source=str(source.relative_to(ROOT)),source_sha256=originals[source],
        user_selected_mp3_sha256=originals[chosen_mp3],speed_relative_to_selected_B=1.,retains_prior_1_25x=True,
        source_text_unchanged=True,new_tts_generated=False,voice_default_changed=False,
        source_voice='Same selected speaker; postprocessed variants, not independent new speakers.',
        selected_variant=None,listening_qc='Pending user listening: no independent validation of naturalness, lexical tones or accent.',
        method='Fixed resonance shift via resampling plus compensating duration/F0 with formant-preserving Rubber Band; mild EQ. No pitch contour modulation.',
        limitation='Existing phrasing, pronunciation and many speaker traits remain; cannot guarantee a new voice identity from postprocessing.',
        variants=[{k:v for k,v in row.items() if k not in ['work','excerpt']} for row in rows],
        preview_end_seconds=duration,preview_source_units=list(range(1,11)),previews=output_rows,
        full=dict(variant='01_can_bang',seconds=info.duration,level=measure(full),
                  files={p.name:dict(sha256=digest(p),bytes=p.stat().st_size) for p in [full,mp3]}))
    (OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    (OUT/'loi_nghe_thu.txt').write_text('\n\n'.join(u['text'] for u in timeline[:10]),encoding='utf-8')
    print(json.dumps(dict(completed=True,full_seconds=info.duration,preview_seconds=duration,output=str(OUT)),ensure_ascii=False),flush=True)


if __name__=='__main__':main()
