"""Reusable VieNeu references, kept distinct from the Piper model catalog."""
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
FLAGS = getattr(subprocess, 'CREATE_NO_WINDOW', 0)


def postprocess_filters(profile, speed=1., volume=1.):
    """Apply a selected voice's pitch/tone recipe to every newly spoken script."""
    recipe = profile.get('postprocess', {})
    semitones = float(recipe.get('pitch_semitones', 0))
    tempo = float(recipe.get('tempo', 1))
    if not math.isfinite(semitones) or not -3 <= semitones <= 3:
        raise ValueError('Cao độ trong hồ sơ giọng không hợp lệ.')
    if not math.isfinite(tempo) or not .5 <= tempo <= 2:
        raise ValueError('Nhịp đọc trong hồ sơ giọng không hợp lệ.')
    if not math.isfinite(speed) or not .5 <= speed <= 2:
        raise ValueError('Tốc độ giọng tham chiếu phải từ 0.5 đến 2.')
    if not math.isfinite(volume) or not 0 <= volume <= 2:
        raise ValueError('Âm lượng phải từ 0 đến 2.')
    if recipe:
        filters = [f'rubberband=tempo={tempo*speed}:pitch={2**(semitones/12):.10f}:'
                   'formant=preserved:pitchq=quality']
        for eq in recipe.get('equalizers', []):
            freq, width, gain = (float(eq[k]) for k in ('frequency', 'width', 'gain'))
            if not (20 <= freq <= 20000 and .1 <= width <= 10 and -12 <= gain <= 12):
                raise ValueError('Sắc âm trong hồ sơ giọng không hợp lệ.')
            filters.append(f'equalizer=f={freq}:t=q:w={width}:g={gain}')
    else:
        filters = [f'atempo={speed}']
    filters.append('loudnorm=I=-18:TP=-2:LRA=7')
    if volume != 1.:
        filters.append(f'volume={volume}')
    filters.append('alimiter=limit=0.98:level=false')
    return ','.join(filters)


def load_profile(path):
    path = Path(path).resolve()
    data = json.loads(path.read_text(encoding='utf-8'))
    if data.get('version') != 1 or data.get('engine') != 'vieneu-v3turbo':
        raise ValueError('Hồ sơ giọng tham chiếu không được hỗ trợ.')
    for key in ('reference', 'codes'):
        asset = (path.parent / data[key]).resolve()
        if not asset.is_relative_to(path.parent):
            raise ValueError('Tài nguyên giọng nằm ngoài thư mục hồ sơ.')
        if not asset.is_file():
            raise ValueError('Thiếu tài nguyên giọng: ' + asset.name)
        if hashlib.sha256(asset.read_bytes()).hexdigest() != data[key + '_sha256']:
            raise ValueError('Tài nguyên giọng đã thay đổi: ' + asset.name)
        data[key + '_path'] = asset
    postprocess_filters(data)  # Reject malformed processing before synthesis starts.
    return data


def model_cache():
    existing = ROOT / 'projects/angkor_wat_1min/.models/huggingface'
    return existing if existing.is_dir() else ROOT / 'voices/.models/huggingface'


def configure_cache():
    cache = model_cache()
    os.environ['HF_HOME'] = str(cache)
    os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'
    os.environ['HF_HUB_DISABLE_XET'] = '1'
    # Avoid repeated network HEAD checks on an already installed offline runtime.
    installed = cache / 'hub/models--pnnbao-ump--VieNeu-TTS-v3-Turbo/snapshots'
    if any(installed.glob('*/onnx_update/vieneu_prefill.onnx')):
        os.environ.setdefault('HF_HUB_OFFLINE', '1')


class ReferenceSynthesizer:
    def __init__(self):
        configure_cache()
        from vieneu import Vieneu
        self.engine = Vieneu(mode='v3turbo', device='cpu', backend='onnx',
                             precision='fp32', threads=4)

    def synthesize(self, text, profile_path, output, speed=1., volume=1.):
        import numpy as np
        import soundfile as sf
        if not text.strip():
            raise ValueError('Nội dung giọng đọc đang trống.')
        if not math.isfinite(speed) or not .5 <= speed <= 2:
            raise ValueError('Tốc độ giọng tham chiếu phải từ 0.5 đến 2.')
        if not math.isfinite(volume) or not 0 <= volume <= 2:
            raise ValueError('Âm lượng phải từ 0 đến 2.')
        profile = load_profile(profile_path)
        with np.load(profile['codes_path'], allow_pickle=False) as z:
            embedding = z['speaker_emb'].astype(np.float32)
            codes = z['codes'].astype(np.int64)
        if not embedding.size or not codes.size or not np.isfinite(embedding).all():
            raise ValueError('Mã giọng tham chiếu không hợp lệ.')
        synthesis = profile.get('synthesis', {})
        audio = np.asarray(self.engine.infer(
            text, voice={'speaker_emb': embedding, 'codes': codes},
            temperature=synthesis.get('temperature', .6), top_k=synthesis.get('top_k', 25),
            max_chars=synthesis.get('max_chars', 160)), dtype=np.float32)
        if not audio.size or not np.isfinite(audio).all():
            raise ValueError('Kết quả giọng đọc bị rỗng hoặc lỗi.')
        output = Path(output).resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='reference_voice_', dir=output.parent) as folder:
            raw = Path(folder) / 'raw.wav'
            final = Path(folder) / 'final.wav'
            sf.write(raw, audio, self.engine.sample_rate, subtype='PCM_16')
            from .exporter import binary
            subprocess.run([binary('ffmpeg'), '-hide_banner', '-loglevel', 'error', '-y',
                            '-i', str(raw), '-af',
                            postprocess_filters(profile,speed,volume),
                            '-ar', '48000', '-ac', '1', '-c:a', 'pcm_s16le', str(final)],
                           check=True, creationflags=FLAGS)
            final.replace(output)
        from .tts import wav_duration
        return wav_duration(output)


def runtime():
    if importlib.util.find_spec('vieneu'):
        return Path(sys.executable)
    for python in (ROOT / '.venv/Scripts/python.exe', ROOT.parent / '.venv/Scripts/python.exe',
                   ROOT / 'projects/angkor_wat_1min/.venv/Scripts/python.exe'):
        if python.is_file():
            check = subprocess.run([str(python), '-c',
                                    'import importlib.util; raise SystemExit(0 if importlib.util.find_spec("vieneu") else 1)'],
                                   capture_output=True, creationflags=FLAGS)
            if check.returncode == 0:
                return python
    raise RuntimeError('Chưa cài VieNeu-TTS. Cài requirements-voice.txt vào môi trường Studio.')


def synthesize_external(text, profile, output, speed, volume):
    output = Path(output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    python = runtime()
    with tempfile.TemporaryDirectory(prefix='voice_request_', dir=output.parent) as folder:
        request = Path(folder) / 'request.json'
        request.write_text(json.dumps(dict(text=text, profile=str(Path(profile).resolve()),
                                           output=str(output), speed=speed, volume=volume),
                                      ensure_ascii=False), encoding='utf-8')
        subprocess.run([str(python), '-X', 'utf8', '-m', 'studio.reference_voice', str(request)],
                       cwd=ROOT, check=True, creationflags=FLAGS)
    from .tts import wav_duration
    return wav_duration(output)


if __name__ == '__main__':
    request = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
    ReferenceSynthesizer().synthesize(request['text'], request['profile'], request['output'],
                                      request['speed'], request['volume'])
