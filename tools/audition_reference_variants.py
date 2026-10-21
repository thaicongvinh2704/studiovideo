"""Five subtle pitch/tempo/tone variants of NEW speech from a supplied reference.

Does not modify Studio's selected production voice or its reference files.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
TEXT = ('Khoan đã, chuyện này chưa đơn giản như bạn nghĩ đâu. '
        'Mình là Mỏ Đen. Hôm nay, chúng ta sẽ lần theo những dấu vết còn lại của quá khứ. '
        'Ai đã kể câu chuyện này, và bằng chứng thực sự nằm ở đâu? Cùng mình tìm hiểu nhé!')
VARIANTS = [
    dict(id='01_tram_cham', name='Trầm hơn, chậm hơn nhẹ', semitones=-.9, tempo=.97,
         eq='equalizer=f=180:t=q:w=0.8:g=0.8'),
    dict(id='02_tram_vua', name='Trầm vừa, nhịp bình thường', semitones=-.45, tempo=1.,
         eq='equalizer=f=220:t=q:w=0.8:g=0.6'),
    dict(id='03_sang_nhe', name='Sáng hơn nhẹ, nhịp bình thường', semitones=.35, tempo=1.,
         eq='equalizer=f=2400:t=q:w=0.8:g=0.5'),
    dict(id='04_cao_nhanh', name='Cao hơn và nhanh hơn nhẹ', semitones=.8, tempo=1.035,
         eq='equalizer=f=2800:t=q:w=0.8:g=0.7'),
    dict(id='05_tram_nhanh', name='Trầm nhẹ nhưng nhanh hơn', semitones=-.3, tempo=1.045,
         eq='equalizer=f=200:t=q:w=0.8:g=0.4,equalizer=f=2200:t=q:w=0.8:g=0.4'),
]


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def ff(*args):
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', *map(str,args)],
                   check=True, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=Path)
    parser.add_argument('--start', type=float, default=60.)
    args = parser.parse_args()
    if not args.source.is_file() or args.start < 0:
        raise ValueError('Invalid source or reference start.')
    dest = ROOT / 'voices/auditions/reference_EFp49inlLuQ_variants'
    active_profile = ROOT / 'voices/mo_den_EFp49inlLuQ_04.voice.json'
    if active_profile.is_file() and json.loads(active_profile.read_text(encoding='utf-8')).get('status') == 'user_selected':
        raise RuntimeError('Bản số 4 đã được chốt làm giọng chính. Không ghi đè tài nguyên đã chọn.')
    dest.mkdir(parents=True, exist_ok=True)
    selected = ROOT / 'voices/video_mau_kcWEaXRh2hA.voice.json'
    selected_hash = digest(selected)
    source_hash = digest(args.source)
    source = dest / 'source.mp3'
    if args.source.resolve() != source.resolve():
        shutil.copy2(args.source, source)
    if digest(source) != source_hash:
        raise RuntimeError('Source copy mismatch.')
    raw_reference = dest / 'reference_raw.wav'
    ff('-ss', args.start, '-i', source, '-t', 8, '-ac', 1, '-ar', 44100,
       '-c:a', 'pcm_s16le', raw_reference)
    os.environ['HF_HOME'] = str(ROOT / 'projects/angkor_wat_1min/.models/huggingface')
    os.environ['HF_HUB_OFFLINE'] = '1'
    os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'
    import numpy as np
    import soundfile as sf
    from vieneu import Vieneu
    tick = time.perf_counter()
    print('Loading cached voice synthesis model...', flush=True)
    tts = Vieneu(mode='v3turbo', device='cpu', backend='onnx', precision='fp32', threads=4)
    raw, rate = sf.read(raw_reference, dtype='float32')
    if len(raw) < 7 * rate or not np.isfinite(raw).all():
        raise RuntimeError('Incomplete reference audio.')
    if tts.engine.denoiser is None:
        raise RuntimeError('Reference denoiser is missing.')
    clean = tts.engine.denoiser.denoise(raw, rate)
    clean_path = dest / 'reference_clean.wav'
    sf.write(clean_path, clean, 44100, subtype='PCM_16')
    print('Encoding new reference; synthesizing new text...', flush=True)
    embedding, codes = tts.engine.prepare_reference(clean, sr=44100, denoise=False)
    np.savez_compressed(dest / 'reference_codes.npz', speaker_emb=embedding, codes=codes)
    np.random.seed(20261021)
    speech = np.asarray(tts.infer(TEXT, voice={'speaker_emb': embedding, 'codes': codes},
                                temperature=.6, top_k=25, max_chars=160), dtype=np.float32)
    if not speech.size or not np.isfinite(speech).all():
        raise RuntimeError('Invalid synthesized speech.')
    base = dest / 'base_synthesized.wav'
    sf.write(base, speech, tts.sample_rate, subtype='PCM_16')
    report = dict(version=1, engine='VieNeu-TTS v3 Turbo 3.8.3',
                  source_sha256=source_hash, source_video_id='EFp49inlLuQ',
                  source_segment_seconds=[args.start, args.start+8],
                  reference_sha256=digest(clean_path), base_sha256=digest(base),
                  text=TEXT, base_seconds=len(speech)/tts.sample_rate,
                  method='New TTS from denoised reference, followed by formant-preserving pitch shift, tempo and gentle EQ. Five variants of one reference, not five independent speakers.',
                  status='auditions_only_no_voice_selected', listening_review='not_performed',
                  candidates=[])
    for settings in VARIANTS:
        pitch = 2 ** (settings['semitones'] / 12)
        filters = (f"rubberband=tempo={settings['tempo']}:pitch={pitch:.10f}:"
                   f"formant=preserved:pitchq=quality,{settings['eq']},"
                   'loudnorm=I=-18:TP=-2:LRA=7,alimiter=limit=0.98:level=false')
        output = dest / (settings['id'] + '.wav')
        ff('-i', base, '-af', filters, '-ar', 48000, '-ac', 1, '-c:a', 'pcm_s16le', output)
        audio, rate = sf.read(output, dtype='float32')
        seconds = len(audio)/rate
        peak = float(np.max(np.abs(audio)))
        rms = float(np.sqrt(np.mean(audio*audio)))
        if not np.isfinite(audio).all() or rms < .001 or peak >= 1.:
            raise RuntimeError('Invalid variant audio: ' + settings['id'])
        if abs(seconds - report['base_seconds']/settings['tempo']) > .3:
            raise RuntimeError('Unexpected variant duration: ' + settings['id'])
        item = dict(**settings, file=output.name, pitch_ratio=pitch, seconds=round(seconds,3),
                    peak=round(peak,5), rms=round(rms,5), sha256=digest(output), filter=filters)
        report['candidates'].append(item)
        print(json.dumps({k:item[k] for k in ['id','name','seconds','semitones','tempo']},
                         ensure_ascii=False), flush=True)
    if len({v['sha256'] for v in report['candidates']}) != 5:
        raise RuntimeError('Variants are not distinct.')
    if digest(selected) != selected_hash or digest(args.source) != source_hash:
        raise RuntimeError('Production voice or source was unexpectedly modified.')
    report.update(elapsed_seconds=round(time.perf_counter()-tick,2),
                  production_voice_unchanged=True, user_source_unchanged=True)
    (dest/'manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    (dest/'script.txt').write_text(TEXT,encoding='utf-8')
    print('Five distinct WAVs ready; current production voice unchanged.',flush=True)


if __name__ == '__main__':
    main()
