"""Full voiceover narration rendering for 'Vì sao kẻ địch của Khương Tử Nha vẫn được phong thần?'
using Mỏ Đen Custom H (Northern Vietnamese accent, 1.25x speed, broadcast -18 LUFS standard).
"""
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

import numpy as np
import soundfile as sf

ROOT = Path(__file__).resolve().parents[3]
WORK_DIR = Path(__file__).resolve().parent
LOCAL = ROOT / 'voices/local_design'
SPEED = 1.25
FLAGS = getattr(subprocess, 'CREATE_NO_WINDOW', 0)


def sha(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def save(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')


def run_ff(*args, capture=False):
    return subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'info' if capture else 'error',
                           '-y', *map(str, args)], check=True, capture_output=capture, creationflags=FLAGS)


def measure(path):
    result = run_ff('-i', path, '-af', 'loudnorm=I=-18:TP=-1.5:LRA=11:print_format=json',
                    '-f', 'null', '-', capture=True)
    text = result.stderr.decode('utf-8', errors='replace')
    matches = re.findall(r'\{[^{}]*"input_i"[^{}]*\}', text, re.S)
    if not matches:
        raise RuntimeError('Không đo được mức âm lượng.')
    d = json.loads(matches[-1])
    return {k: float(d[k]) for k in ['input_i', 'input_tp', 'input_lra', 'input_thresh']}


def edge_silence(audio, rate, from_end=False):
    x = audio[::-1] if from_end else audio
    frame = round(rate * 0.01)
    threshold = 10 ** (-46 / 20)
    count = 0
    for start in range(0, len(x), frame):
        block = x[start:start + frame]
        if float(np.sqrt(np.mean(block * block))) > threshold:
            break
        count += len(block)
    return 1000.0 * count / rate


def pause_padding_ms(trailing_ms, leading_ms, target_ms):
    return max(0.0, float(target_ms) - float(trailing_ms) - float(leading_ms))


def format_srt_time(seconds):
    millis = int(round((seconds - int(seconds)) * 1000))
    total_seconds = int(seconds)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def main():
    print("=== BẮT ĐẦU QUY TRÌNH BIÊN TẬP VÀ XUẤT GIỌNG ĐỌC MỎ ĐEN (PHONG THẦN DIỄN NGHĨA) ===")
    
    plan_path = WORK_DIR / '03_Kich_Ban_Bien_Kich_Dien_Doc.json'
    plan_data = json.loads(plan_path.read_text(encoding='utf-8'))
    units = plan_data['units']
    print(f"Tổng số cụm nghĩa (Semantic Units): {len(units)}")

    raw_dir = WORK_DIR / 'raw'
    raw_dir.mkdir(exist_ok=True)
    processed_dir = WORK_DIR / 'units'
    processed_dir.mkdir(exist_ok=True)

    reference = ROOT / 'projects/mo_den_maya/voice_direction/full_narration_custom_H_125/H_reference_native_16k.wav'
    if not reference.exists():
        raise RuntimeError(f"Reference native audio không tồn tại: {reference}")

    model_paths = [
        LOCAL / 'models/VoxCPM2-BaseLM-Q8_0.gguf',
        LOCAL / 'models/VoxCPM2-Acoustic-F16.gguf'
    ]
    runtime = LOCAL / 'build-vulkan/bin/studio-voice-batch.exe'
    if not runtime.exists():
        raise RuntimeError(f"Batch runtime Vulkan không tồn tại: {runtime}")

    jobs = []
    to_synthesize = []
    for u in units:
        i = u['id']
        raw_file = raw_dir / f"unit_{i:03d}.wav"
        job_item = {
            'id': i,
            'text': u['spoken_text'],
            'seed': 284617,
            'output': str(raw_file)
        }
        jobs.append(job_item)
        if not (raw_file.exists() and raw_file.stat().st_size > 1000):
            to_synthesize.append(job_item)

    print(f"Cần tổng hợp mới qua GPU: {len(to_synthesize)} / {len(units)} units")

    if to_synthesize:
        batch_job = {
            'base_lm': str(model_paths[0]),
            'acoustic': str(model_paths[1]),
            'reference': str(reference),
            'gpu': True,
            'gpu_layers': 29,
            'threads': 6,
            'max_steps': 350,
            'units': to_synthesize
        }
        batch_job_path = WORK_DIR / 'batch_job.json'
        save(batch_job_path, batch_job)

        env = dict(os.environ, STUDIO_SINGLE_REFERENCE_CACHE='1')
        print(f"Khởi chạy engine VoxCPM2 GPU Vulkan trên {len(to_synthesize)} units...")
        
        proc = subprocess.Popen(
            [str(runtime), str(batch_job_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8',
            errors='replace',
            bufsize=1,
            env=env,
            creationflags=FLAGS
        )

        log_path = WORK_DIR / 'synthesis.log'
        with open(log_path, 'w', encoding='utf-8') as log_f:
            for line in proc.stdout:
                log_f.write(line)
                log_f.flush()
                if line.startswith(('DONE ', 'CACHED ', 'START ', 'BATCH_ERROR ')):
                    print(line.strip(), flush=True)

        code = proc.wait()
        if code != 0:
            raise RuntimeError("Quá trình tổng hợp batch audio thất bại. Kiểm tra synthesis.log")
        print("Tổng hợp toàn bộ các units thành công!")

    # Step 2: Micro-tempo and gain processing per unit
    print("\n--- BƯỚC 2: XỬ LÝ NHỊP ĐIỆU (MICRO-PACE) VÀ CƯỜNG ĐỘ (GAIN) TỪNG CỤM NGHĨA ---")
    rendered = []
    for u in units:
        i = u['id']
        raw_file = raw_dir / f"unit_{i:03d}.wav"
        proc_file = processed_dir / f"unit_{i:03d}_proc.wav"

        audio, rate = sf.read(raw_file, dtype='float32')
        if rate != 48000 or audio.ndim != 1 or not audio.size or not np.isfinite(audio).all():
            raise RuntimeError(f"Audio lỗi tại unit {i}")

        pace = u.get('pace', 1.0)
        gain_db = u.get('gain_db', 0.0)

        # Micro rubberband filters
        filters = f"rubberband=tempo={pace}:pitch=1:formant=preserved,volume={gain_db}dB"
        run_ff('-i', raw_file, '-af', filters, '-ar', 48000, '-ac', 1, '-c:a', 'pcm_s16le', proc_file)

        proc_audio, _ = sf.read(proc_file, dtype='float32')
        leading = edge_silence(proc_audio, rate, from_end=False)
        trailing = edge_silence(proc_audio, rate, from_end=True)

        rendered.append({
            'id': i,
            'file': proc_file,
            'frames': len(proc_audio),
            'leading_ms': leading,
            'trailing_ms': trailing,
            'raw_sha256': sha(raw_file),
            'unit_info': u
        })

    # Step 3: Stitching with semantic pauses into base timeline
    print("\n--- BƯỚC 3: GHÉP DÒNG THỜI GIAN VỚI KHOẢNG NGHỈ BIÊN KỊCH CHUẨN XÁC ---")
    native_timeline_wav = WORK_DIR / 'Phong_Than_H_native_timeline.wav'
    cursor = 0
    timeline = []

    with sf.SoundFile(native_timeline_wav, 'w', samplerate=48000, channels=1, subtype='PCM_16') as target:
        for idx, item in enumerate(rendered):
            audio, rate = sf.read(item['file'], dtype='float32')
            target.write(audio)
            
            start_frame = cursor
            cursor += len(audio)

            u = item['unit_info']
            target_ms = u.get('pause_ms', 400)

            # Check next unit's leading silence
            next_leading = rendered[idx + 1]['leading_ms'] if idx + 1 < len(rendered) else 0.0
            pad_ms = pause_padding_ms(item['trailing_ms'], next_leading, target_ms)
            pad_frames = int(round(pad_ms * 48))

            final_start_sec = (start_frame / 48000) / SPEED
            final_end_sec = (cursor / 48000) / SPEED

            timeline.append({
                'id': u['id'],
                'section_num': u['section_num'],
                'section_title': u['section_title'],
                'source_text': u['source_text'],
                'spoken_text': u['spoken_text'],
                'intent': u['intent'],
                'tone': u['tone'],
                'start_seconds': final_start_sec,
                'end_seconds': final_end_sec,
                'pause_target_ms': target_ms,
                'pause_padded_ms': pad_ms
            })

            if pad_frames > 0:
                target.write(np.zeros(pad_frames, dtype=np.float32))
                cursor += pad_frames

    native_duration = cursor / 48000
    print(f"Thời lượng timeline gốc: {native_duration:.2f}s ({native_duration/60:.2f} phút)")

    # Step 4: Apply 1.25x speed once using high-quality rubberband
    print("\n--- BƯỚC 4: TĂNG TỐC 1.25x DUY NHẤT MỘT LẦN (CHUẨN H MỎ ĐEN) ---")
    fast_wav = WORK_DIR / 'Phong_Than_H_125_unmatched.wav'
    run_ff(
        '-i', native_timeline_wav,
        '-af', 'rubberband=tempo=1.25:pitch=1:formant=preserved:pitchq=quality',
        '-ar', 48000, '-ac', 1, '-c:a', 'pcm_s16le', fast_wav
    )

    # Step 5: Loudness normalization (-18 LUFS, -1.5 dBTP max)
    print("\n--- BƯỚC 5: CHUẨN HÓA ÂM LƯỢNG ĐIỆN ẢNH (-18 LUFS, PEAK -1.5 dBTP) ---")
    lvl = measure(fast_wav)
    print(f"Loudness hiện tại: Input I={lvl['input_i']:.2f} LUFS, TP={lvl['input_tp']:.2f} dBTP")
    gain = min(-18.0 - lvl['input_i'], -1.5 - lvl['input_tp'])
    print(f"Áp dụng bù Gain tuyến tính: {gain:+.2f} dB")

    final_wav = WORK_DIR / 'Mo_Den_Phong_Than_Dien_Nghia_Custom_H_1_25x.wav'
    final_mp3 = WORK_DIR / 'Mo_Den_Phong_Than_Dien_Nghia_Custom_H_1_25x.mp3'

    run_ff('-i', fast_wav, '-af', f"volume={gain:.6f}dB", '-ar', 48000, '-ac', 1, '-c:a', 'pcm_s16le', final_wav)
    run_ff('-i', final_wav, '-c:a', 'libmp3lame', '-b:a', '192k', final_mp3)

    final_info = sf.info(final_wav)
    final_lvl = measure(final_wav)
    print(f"File hoàn thiện WAV: {final_wav.name} ({final_info.duration:.2f}s, {final_lvl['input_i']:.2f} LUFS)")
    print(f"File hoàn thiện MP3: {final_mp3.name} ({final_mp3.stat().st_size / 1024 / 1024:.2f} MB)")

    # Step 6: Export synchronized SRT with original text
    print("\n--- BƯỚC 6: XUẤT PHỤ ĐỀ ĐỒNG BỘ CHUẨN XÁC (SRT) ---")
    srt_file = WORK_DIR / 'Mo_Den_Phong_Than_Dien_Nghia.srt'
    srt_lines = []
    for i, t in enumerate(timeline):
        s_time = format_srt_time(t['start_seconds'])
        e_time = format_srt_time(min(t['end_seconds'], final_info.duration))
        srt_lines.append(f"{i + 1}\n{s_time} --> {e_time}\n{t['source_text']}\n")

    srt_file.write_text("\n".join(srt_lines), encoding='utf-8-sig')
    print(f"Đã xuất SRT đồng bộ: {srt_file.name} ({len(timeline)} cues)")

    # Step 7: Export comprehensive report
    report = {
        "status": "COMPLETED_READY_FOR_LISTENING",
        "title": plan_data['title'],
        "speaker": plan_data['speaker'],
        "accent": plan_data['accent'],
        "total_units": len(units),
        "total_sections": plan_data['total_sections'],
        "final_duration_seconds": final_info.duration,
        "final_duration_formatted": f"{int(final_info.duration // 60)}m{int(final_info.duration % 60):02d}s",
        "speed_multiplier": SPEED,
        "loudness": final_lvl,
        "gain_applied_db": gain,
        "files": {
            "wav": {
                "path": str(final_wav),
                "sha256": sha(final_wav),
                "bytes": final_wav.stat().st_size
            },
            "mp3": {
                "path": str(final_mp3),
                "sha256": sha(final_mp3),
                "bytes": final_mp3.stat().st_size
            },
            "srt": {
                "path": str(srt_file),
                "sha256": sha(srt_file),
                "cues": len(timeline)
            }
        },
        "timeline": timeline
    }

    report_path = WORK_DIR / 'report_phong_than.json'
    save(report_path, report)
    print(f"Đã ghi báo cáo hoàn thành: {report_path.name}")
    print("\n=== HOÀN TẤT TOÀN BỘ QUY TRÌNH THÀNH CÔNG ===")


if __name__ == '__main__':
    main()
