"""Comparable, music-free auditions from existing Vietnamese presets."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'voices' / 'auditions' / 'mo_den_20261021'
TEXT = ('Khoan đã! Nghe thì có lý, nhưng bằng chứng đâu? '
        'Mình là Mỏ Đen. Cùng mình lần theo từng dấu vết nhé. '
        'Biết đâu, điều thú vị nhất lại nằm ở chi tiết mà chúng ta vừa bỏ qua!')
CANDIDATES = [
    ('01_adam_bua', 'Adam bựa'),
    ('02_xuan_vinh', 'Xuân Vĩnh'),
    ('03_thai_son', 'Thái Sơn'),
    ('04_truc_ly', 'Trúc Ly'),
]
EXTRA_CANDIDATES = [
    ('05_thien_minh', 'Thiện Minh'),
    ('06_pham_tuyen', 'Phạm Tuyên'),
    ('07_adam', 'Adam'),
    ('08_quang_son', 'Quang Sơn'),
    ('09_ngoc_huyen', 'Ngọc Huyền'),
    ('10_thuc_doan', 'Thục Đoan'),
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch', choices=['first', 'extra'], default='first')
    args = parser.parse_args()
    candidates = EXTRA_CANDIDATES if args.batch == 'extra' else CANDIDATES
    dest = DEST / 'batch_02' if args.batch == 'extra' else DEST
    dest.mkdir(parents=True, exist_ok=True)
    os.environ['HF_HOME'] = str(ROOT / 'projects/angkor_wat_1min/.models/huggingface')
    os.environ['HF_HUB_OFFLINE'] = '1'
    os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'
    import numpy as np
    import soundfile as sf
    from vieneu import Vieneu
    tts = Vieneu(mode='v3turbo', device='cpu', backend='onnx', precision='fp32', threads=4)
    catalog = {name: label for label, name in tts.list_preset_voices()}
    results = []
    for slug, name in candidates:
        if name not in catalog:
            raise ValueError('Preset not in installed catalog: ' + name)
        tick = time.perf_counter()
        print('Generating ' + name, flush=True)
        np.random.seed(20261021)
        audio = np.asarray(tts.infer(TEXT, voice=name, temperature=.6,
                                    top_k=25, max_chars=160), dtype=np.float32)
        if not audio.size or not np.isfinite(audio).all():
            raise RuntimeError('Invalid audio: ' + name)
        raw = dest / (slug + '_raw.wav')
        output = dest / (slug + '.wav')
        sf.write(raw, audio, tts.sample_rate, subtype='PCM_16')
        subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
                        '-i', str(raw), '-af',
                        'loudnorm=I=-18:TP=-2:LRA=7,alimiter=limit=0.98:level=false',
                        '-ar', '48000', '-ac', '1', '-c:a', 'pcm_s16le', str(output)], check=True)
        final, rate = sf.read(output, dtype='float32')
        preset = tts.get_preset_voice(name)
        codes = dest / (slug + '_codes.npz')
        np.savez_compressed(codes, speaker_emb=preset['speaker_emb'], codes=preset['codes'])
        results.append(dict(id=slug, voice=name, catalog_label=catalog[name],
                            file=output.name, seconds=round(len(final)/rate, 3),
                            peak=round(float(np.max(np.abs(final))), 5),
                            rms=round(float(np.sqrt(np.mean(final*final))), 5),
                            finite=bool(np.isfinite(final).all()),
                            sha256=hashlib.sha256(output.read_bytes()).hexdigest(),
                            generated_seconds=round(time.perf_counter()-tick, 2)))
        print(json.dumps(results[-1], ensure_ascii=False), flush=True)
        (dest / 'manifest.json').write_text(json.dumps(dict(
            version=1, engine='VieNeu-TTS v3 Turbo 3.8.3', source='installed preset catalog',
            source_repo='https://github.com/pnnbao97/VieNeu-TTS', text=TEXT,
            conditions='Same text, seed, sampling, unaltered pitch and tempo; no music; -18 LUFS target.',
            status='auditions_only_no_voice_selected', listening_review='not_performed',
            candidates=results), ensure_ascii=False, indent=2), encoding='utf-8')
    (dest / 'script.txt').write_text(TEXT, encoding='utf-8')


if __name__ == '__main__':
    main()
