"""Prepare the user-supplied sample's reference and an honestly labelled audition.

Run with the optional VieNeu environment. Never edits the supplied original.
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
NAME = 'video_mau_kcWEaXRh2hA'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source', type=Path)
    parser.add_argument('--start', type=float, default=60)
    args = parser.parse_args()
    profile_path = ROOT / 'voices' / (NAME + '.voice.json')
    if profile_path.is_file():
        previous = json.loads(profile_path.read_text(encoding='utf-8'))
        if previous.get('status') == 'user_selected':
            raise RuntimeError('Giọng này đã được người dùng chốt. Không ghi đè tham chiếu và bản đọc đã chọn.')
    if not args.source.is_file() or args.start < 0:
        raise ValueError('Source audio or reference start is invalid.')
    dest = ROOT / 'voices' / 'references' / NAME
    dest.mkdir(parents=True, exist_ok=True)
    source = dest / 'source.mp3'
    if args.source.resolve() != source.resolve():
        shutil.copy2(args.source, source)
    reference = dest / 'reference_raw.wav'
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
                    '-ss', str(args.start), '-i', str(source), '-t', '8',
                    '-ac', '1', '-ar', '44100', '-c:a', 'pcm_s16le', str(reference)], check=True)
    cache = ROOT / 'projects' / 'angkor_wat_1min' / '.models' / 'huggingface'
    os.environ['HF_HOME'] = str(cache)
    os.environ['HF_HUB_OFFLINE'] = '1'
    os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'
    import numpy as np
    import soundfile as sf
    from vieneu import Vieneu
    tick = time.perf_counter()
    print('Loading cached CPU model...', flush=True)
    tts = Vieneu(mode='v3turbo', device='cpu', backend='onnx', precision='fp32', threads=4)
    raw, rate = sf.read(reference, dtype='float32')
    if tts.engine.denoiser is None:
        raise RuntimeError('Reference denoiser is unavailable; do not silently use noisy audio.')
    clean = tts.engine.denoiser.denoise(raw, rate)
    clean_path = dest / 'reference_clean.wav'
    sf.write(clean_path, clean, 44100, subtype='PCM_16')
    print('Encoding the supplied voice reference...', flush=True)
    embedding, codes = tts.engine.prepare_reference(clean, sr=44100, denoise=False)
    encoded = dest / 'reference_codes.npz'
    np.savez_compressed(encoded, speaker_emb=embedding, codes=codes)
    text = ('Bạn có bao giờ tự hỏi, vì sao lịch sử vẫn còn những khoảng trống? '
            'Trong video này, Mỏ Đen sẽ cùng bạn lần theo từng dấu vết. '
            'Chúng ta sẽ phân biệt điều đã có bằng chứng, điều còn tranh luận, '
            'và những câu hỏi chưa thể trả lời.')
    print('Synthesizing NEW audition text...', flush=True)
    np.random.seed(20261021)
    audio = tts.infer(text, voice={'speaker_emb': embedding, 'codes': codes},
                      temperature=.6, top_k=25, max_chars=160)
    audio = np.asarray(audio, dtype=np.float32)
    if not len(audio) or not np.isfinite(audio).all():
        raise RuntimeError('Generated audio is empty or non-finite.')
    unmastered = dest / 'audition_raw.wav'
    audition = dest / 'audition.wav'
    sf.write(unmastered, audio, tts.sample_rate, subtype='PCM_16')
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(unmastered),
                    '-af', 'loudnorm=I=-18:TP=-2:LRA=7', '-ar', '48000', '-ac', '1', str(audition)], check=True)
    profile = dict(version=1, engine='vieneu-v3turbo', name='Giọng tham chiếu · video mẫu',
                   reference='references/' + NAME + '/reference_clean.wav',
                   codes='references/' + NAME + '/reference_codes.npz',
                   reference_sha256=hashlib.sha256(clean_path.read_bytes()).hexdigest(),
                   codes_sha256=hashlib.sha256(encoded.read_bytes()).hexdigest(),
                   source_url='https://www.youtube.com/watch?v=kcWEaXRh2hA',
                   source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                   source_segment_seconds=[args.start, args.start + 8],
                   speaker_identity='Unverified; do not attribute to a named individual.',
                   status='audition_pending_user_review',
                   preferred=True,
                   audition_text=text,
                   audition_seconds=round(len(audio) / tts.sample_rate, 3),
                   elapsed_seconds=round(time.perf_counter() - tick, 2),
                   quality_note='Denoised 8-second reference; no listening or similarity approval implied.')
    (ROOT / 'voices' / (NAME + '.voice.json')).write_text(
        json.dumps(profile, ensure_ascii=False, indent=2), encoding='utf-8')
    (dest / 'audition.txt').write_text(text, encoding='utf-8')
    print(json.dumps({'audition': str(audition), 'seconds': profile['audition_seconds'],
                      'elapsed_seconds': profile['elapsed_seconds']}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
