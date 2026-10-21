"""Render the complete Maya script using the directed B pipeline, then 1.25x."""
import hashlib
import argparse
import importlib.metadata
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from studio.voice_direction import read_package, compile_excerpt, pause_padding_ms, space
from studio.reference_voice import ReferenceSynthesizer, load_profile, postprocess_filters
from create_maya_directed_ab import BASE, PACKAGE, PROFILE, SUPPLIED, digest, run_ff, measure, edge_silence

OUT = BASE / 'full_narration_125'
SPEED = 1.25


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def cache_key(data):
    return hashlib.sha256(json.dumps(data, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def timestamp(seconds):
    milliseconds = round(seconds * 1000)
    hours, milliseconds = divmod(milliseconds, 3600000)
    minutes, milliseconds = divmod(milliseconds, 60000)
    seconds, milliseconds = divmod(milliseconds, 1000)
    return f'{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}'


def main():
    import numpy as np
    import soundfile as sf
    from vieneu_utils.phonemize_text import normalize_to_chunks_v3_with_gaps

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--profile', type=Path, default=PROFILE)
    parser.add_argument('--output', type=Path, default=OUT)
    parser.add_argument('--voice-label', default='Giọng Bắc bản B')
    parser.add_argument('--file-stem', default='Mo_Den_Maya_Giong_B_1_25x_DAY_DU')
    args = parser.parse_args()
    output_dir = args.output.resolve()
    profile_path = args.profile.resolve()
    if not output_dir.is_relative_to(BASE.resolve()):
        raise ValueError('Thư mục xuất phải nằm trong dự án giọng Maya.')
    if Path(args.file_stem).name != args.file_stem or any(c in args.file_stem for c in '/\\:'):
        raise ValueError('Tên file xuất không hợp lệ.')
    # Local variables keep parallel voice variants separate without changing the default.
    out = output_dir
    out.mkdir(parents=True, exist_ok=True)
    units_dir = out / 'units'; units_dir.mkdir(exist_ok=True)
    cache = BASE / 'ab_samples/cache'; cache.mkdir(exist_ok=True)
    direction = read_package(PACKAGE, SUPPLIED)
    profile = load_profile(profile_path)
    if profile['language'] != 'vi-VN' or profile['region'] != 'Bắc':
        raise RuntimeError('Sai giọng hoặc vùng giọng đã chốt.')
    preserved = {str(profile_path): digest(profile_path),
                 str(profile_path.parent / profile['selected_audition']): profile['selected_audition_sha256']}
    for path, expected in preserved.items():
        if digest(path) != expected: raise RuntimeError('Mẫu đã chốt bị đổi.')
    units = compile_excerpt(direction, direction['source_cues'][0]['id'], direction['source_cues'][-1]['id'])
    spoken = space(' '.join(u['text'] for u in units))
    if spoken != space((PACKAGE/'01_Loi_Ke_Sach.txt').read_text(encoding='utf-8-sig')):
        raise RuntimeError('Lời toàn bài khác TXT nguồn.')
    covered = [ident for u in units for ident in u['source_cue_ids']]
    if covered != [c['id'] for c in direction['source_cues']]:
        raise RuntimeError('Thiếu hoặc lặp cue nguồn.')
    # Resolve every native split before expensive inference. Never cut protected phrases.
    for unit in units:
        chunks, gaps = normalize_to_chunks_v3_with_gaps(unit['text'], max_chars=280)
        if len(chunks) != 1:
            raise RuntimeError('Engine chia câu ngoài kế hoạch: '+unit['text'])
        unit['actual_engine_chunks'] = chunks
        unit['actual_engine_gaps'] = gaps
    write_json(out/'directed_plan.json', units)
    (out/'loi_doc_day_du.txt').write_text('\n\n'.join(b['text'] for b in direction['beats']), encoding='utf-8')
    sdk = importlib.metadata.version('vieneu')
    synthesis = profile['synthesis']
    config = dict(language='vi-VN', region='Bắc', selected_voice=str(profile_path.relative_to(ROOT)),
                  voice_label=args.voice_label, profile_sha256=digest(profile_path), speaker_codes_sha256=profile['codes_sha256'],
                  sdk=sdk, synthesis=synthesis, postprocess=profile['postprocess'],
                  complete_directed_pipeline_B=True, final_speed_multiplier=SPEED,
                  speed_scope='Whole directed track including pauses; pitch=1 in final retiming.',
                  additional_pitch_semitones=0, beats=len(direction['beats']), units=len(units),
                  source_cues=len(covered), input_hashes={p.name:digest(p) for p in PACKAGE.iterdir() if p.is_file()},
                  authorization='User explicitly requested this full-script voice variant at the preceding 1.25x speed.',
                  no_video=True, reading_edits=[],
                  pronunciation_qc='Pending listening; original spelling preserved, no invented aliases.')
    write_json(out/'effective_config.json', config)
    previous_seeds = {}
    for report in (BASE/'ab_samples').glob('*/report.json'):
        old = json.loads(report.read_text(encoding='utf-8'))
        for unit in old['directed_units']: previous_seeds[unit['text']] = old['seed']
    os.environ['HF_HUB_OFFLINE'] = '1'
    native = None
    with np.load(profile['codes_path'], allow_pickle=False) as z:
        voice = dict(speaker_emb=z['speaker_emb'].astype(np.float32), codes=z['codes'].astype(np.int64))
    rendered = []; last_beat = None
    print(f'Toàn bài: {len(direction["beats"])} beat, {len(units)} cụm nghĩa, {len(covered)} cue nguồn.', flush=True)
    for index, unit in enumerate(units):
        seed = previous_seeds.get(unit['text'], 20261021)
        raw_config = dict(text=unit['text'], seed=seed, codes_sha256=profile['codes_sha256'], sdk=sdk,
                          temperature=synthesis['temperature'], top_k=synthesis['top_k'], max_chars=synthesis['max_chars'])
        key = cache_key(raw_config); raw = cache/(key+'.wav')
        if unit['beat_id'] != last_beat:
            last_beat = unit['beat_id']
            print(f'Đang dựng {last_beat} · cụm {index+1}/{len(units)}', flush=True)
        if not raw.is_file():
            if native is None: native = ReferenceSynthesizer().engine
            np.random.seed(seed)
            audio = np.asarray(native.infer(unit['text'], voice=voice,
                               temperature=synthesis['temperature'], top_k=synthesis['top_k'],
                               max_chars=synthesis['max_chars']), dtype=np.float32)
            if not audio.size or not np.isfinite(audio).all(): raise RuntimeError('Audio tổng hợp lỗi.')
            temporary = raw.with_suffix('.partial.wav')
            sf.write(temporary, audio, native.sample_rate, subtype='PCM_16'); temporary.replace(raw)
        filters = postprocess_filters(profile, unit['pace_multiplier'], 10**(unit['gain_db']/20))
        processed = units_dir/f'{index+1:03}.wav'; marker = processed.with_suffix('.json')
        process_config = dict(raw_sha256=digest(raw), filters=filters, sample_rate=48000)
        if not processed.is_file() or not marker.is_file() or json.loads(marker.read_text()) != process_config:
            temporary = processed.with_suffix('.partial.wav')
            run_ff('-i', raw, '-af', filters, '-ar', 48000, '-ac', 1, '-c:a', 'pcm_s16le', temporary)
            temporary.replace(processed); write_json(marker, process_config)
        audio, rate = sf.read(processed, dtype='float32')
        if rate != 48000 or audio.ndim != 1 or not len(audio) or not np.isfinite(audio).all():
            raise RuntimeError('Cụm audio không hợp lệ.')
        rendered.append(dict(file=processed, frames=len(audio),
                             leading_ms=edge_silence(audio,rate), trailing_ms=edge_silence(audio,rate,True),
                             raw_sha256=digest(raw), seed=seed))
        write_json(out/'progress.json', dict(stage='synthesis', completed_units=index+1, total_units=len(units),
                                            beat_id=last_beat, completed=False))
    base = out/'Maya_nhip_goc.wav'
    timeline = []; cursor = 0
    with sf.SoundFile(base, 'w', samplerate=48000, channels=1, subtype='PCM_16') as target:
        for index, (unit, item) in enumerate(zip(units, rendered)):
            audio, rate = sf.read(item['file'], dtype='float32'); target.write(audio)
            start = cursor; cursor += len(audio)
            timeline.append(dict(unit=index+1, beat_id=unit['beat_id'], source_cue_ids=unit['source_cue_ids'],
                                 text=unit['text'], base_start_seconds=start/48000, base_end_seconds=cursor/48000,
                                 final_start_seconds=start/48000/SPEED, final_end_seconds=cursor/48000/SPEED,
                                 raw_sha256=item['raw_sha256'], seed=item['seed']))
            leading = rendered[index+1]['leading_ms'] if index+1<len(rendered) else 0
            padding = pause_padding_ms(item['trailing_ms'], leading, unit['pause']['target_ms'])
            added = round(padding/1000*48000)
            if added: target.write(np.zeros(added, dtype=np.float32)); cursor += added
            timeline[-1]['pause'] = dict(unit['pause'], existing_trailing_ms=item['trailing_ms'],
                                        next_leading_ms=leading, added_ms=added/48,
                                        final_target_ms=unit['pause']['target_ms']/SPEED)
    print(f'Đã ghép đủ toàn bài {cursor/48000:.2f}s; đang tăng tốc 1,25× và xuất file.', flush=True)
    fast = out/'Maya_125_unmatched.wav'
    run_ff('-i',base,'-af','rubberband=tempo=1.25:pitch=1:formant=preserved:pitchq=quality',
           '-ar',48000,'-ac',1,'-c:a','pcm_s16le',fast)
    level = measure(fast)
    gain = min(-18-level['input_i'], -1.5-level['input_tp'])
    final = out/(args.file_stem+'.wav')
    run_ff('-i',fast,'-af',f'volume={gain:.9f}dB','-ar',48000,'-ac',1,'-c:a','pcm_s16le',final)
    mp3 = out/(args.file_stem+'.mp3')
    run_ff('-i',final,'-c:a','libmp3lame','-b:a','192k',mp3)
    info = sf.info(final)
    if abs(info.duration-cursor/48000/SPEED) > .15: raise RuntimeError('Sai tỷ lệ tốc độ toàn bài.')
    peak = 0.
    for block in sf.blocks(final, blocksize=480000, dtype='float32'):
        if not np.isfinite(block).all(): raise RuntimeError('Audio có giá trị lỗi.')
        peak = max(peak,float(np.max(np.abs(block))))
    if peak >= 1: raise RuntimeError('Audio clipping.')
    for output in [final,mp3]: run_ff('-i',output,'-f','null','-')
    write_json(out/'timeline_cum_y.json', dict(method='Measured concatenated inference-unit boundaries / 1.25; no forced word alignment.',
               boundary_precision='Approximate after whole-track rubberband; not 275 source cue alignment.',units=timeline))
    subtitle = '\n\n'.join(f'{i+1}\n{timestamp(t["final_start_seconds"])} --> {timestamp(min(t["final_end_seconds"],info.duration))}\n{t["text"]}' for i,t in enumerate(timeline))+'\n'
    (out/'Maya_1_25x_CUM_Y_CHUA_CAN_TUNG_TU.srt').write_text(subtitle,encoding='utf-8-sig')
    for path, expected in preserved.items():
        if digest(path) != expected: raise RuntimeError('Hồ sơ hoặc mẫu chọn đã bị đổi.')
    final_level = measure(final)
    report = dict(completed=True, complete_input_text_covered_once=True, source_cues=covered,
                  voice_label=args.voice_label, beats=len(direction['beats']), semantic_units=len(units), final_seconds=info.duration,
                  directed_base_seconds=cursor/48000, speed_multiplier=SPEED,
                  measured_duration_ratio=(cursor/48000)/info.duration, peak=peak, loudness=final_level,
                  linear_gain_db=gain, voice_originals_preserved=True, video_rendered=False,
                  files={p.name:dict(sha256=digest(p),bytes=p.stat().st_size) for p in [final,mp3]},
                  listening_qc='PENDING_USER_LISTENING: no independent listening or ASR in this run; signal checks do not prove pronunciation or audible word completeness.',
                  pronunciation_review=direction['pronunciation_review'],
                  subtitles='Semantic-unit approximate time map from measured units; no word-level forced alignment; original 275-cue SRT preserved unchanged.')
    write_json(out/'report.json',report)
    write_json(out/'progress.json', dict(stage='complete', completed_units=len(units), total_units=len(units),completed=True))
    (out/'CACH_NGHE_VA_GIOI_HAN.md').write_text(
        '# Lời đọc Maya đầy đủ — 1,25×\n\n'
        f'Đã tổng hợp toàn bộ 36 beat / 275 cue nguồn, gồm {len(units)} cụm nghĩa. '
        f'Thời lượng {info.duration/60:.2f} phút. Bản WAV là bản chính; MP3 để nghe gọn nhẹ.\n\n'
        f'Giọng: {args.voice_label}. Dùng mã giọng và công thức âm sắc trong effective_config.json. '
        'Tăng tốc toàn bộ bản đạo diễn 1,25 lần '
        '(cả khoảng nghỉ), không thêm dịch cao độ ở bước tăng tốc. Giữ nguyên TXT/JSON/SRT nguồn.\n\n'
        'Kiểm tra kỹ thuật: lời đầu vào đủ và đúng thứ tự, WAV/MP3 giải mã được, không clipping, '
        'thời lượng đúng tỷ lệ. Chưa nghe kiểm tra độc lập; không suy ra đúng thanh, tên riêng, '
        'cùng vùng giọng hoặc không lặp/mất từ trong âm thanh từ những chỉ số này.\n\n'
        'SRT CUM_Y dùng mốc cụm tổng hợp đo được, quy đổi theo tốc độ; chỉ là mốc tham khảo '
        'sau time-stretch. Chưa căn từng từ, chưa phải SRT cuối cho video. SRT 275 cue gốc '
        'vẫn được bảo toàn trong input/. Chưa dựng video.\n',encoding='utf-8')
    print(f'HOÀN TẤT: {final} · {info.duration:.3f}s',flush=True)


if __name__ == '__main__': main()
