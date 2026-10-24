"""Align the supplied Vietnamese SRT, preserving script and narration byte-for-byte.

Run in .deps/editing/whisperx. Output is a separate proposal, never auto-imported.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from studio.subtitles import read, write

ALIGN_MODEL = 'dragonSwing/wav2vec2-base-vietnamese'


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--audio', required=True, type=Path)
    parser.add_argument('--srt', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    out = args.output.resolve()
    # Refuse overwriting either supplied input via an output filename.
    targets = [out / name for name in ('alignment.json', 'aligned_proposal.srt')]
    if any(p.resolve() in (args.audio.resolve(), args.srt.resolve()) for p in targets):
        parser.error('Thư mục đầu ra trùng với tư liệu gốc.')
    cues = read(args.srt)
    if not cues:
        parser.error('SRT không có lời đọc.')
    original = {'audio_sha256': digest(args.audio), 'srt_sha256': digest(args.srt)}
    import numpy as np
    import torch
    from whisperx.alignment import align, load_align_model
    torch.set_num_threads(min(4, max(1, torch.get_num_threads())))
    decoded = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(args.audio),
                              '-f', 'f32le', '-ac', '1', '-ar', '16000', '-'],
                             check=True, capture_output=True)
    audio = np.frombuffer(decoded.stdout, dtype=np.float32).copy()
    duration = len(audio) / 16000
    if any(c['start'] < 0 or c['end'] > duration + .05 for c in cues):
        parser.error('Mốc SRT vượt độ dài audio; cần đúng SRT của audio, không dùng mốc timeline có intro.')
    print('Loading Vietnamese alignment model...', flush=True)
    model, metadata = load_align_model(language_code='vi', device='cpu', model_name=ALIGN_MODEL)
    segments = [{'start': c['start'], 'end': c['end'], 'text': c['text']} for c in cues]
    result = align(segments, model, metadata, audio, device='cpu',
                   return_char_alignments=False, print_progress=True)
    # Keep each original cue and its text. Word timing is auxiliary, not a rewrite.
    words = result.get('word_segments', [])
    missing = [w.get('word', '') for w in words if 'start' not in w or 'end' not in w]
    proposal = []
    aligned_segments = result.get('segments', [])
    for cue in cues:
        matches = [s for s in aligned_segments
                   if s.get('start', -1) < cue['end'] and s.get('end', -1) > cue['start']]
        timed = [w for s in matches for w in s.get('words', [])
                 if 'start' in w and 'end' in w and cue['start'] <= w['start'] < cue['end']]
        if timed:
            proposal.append(dict(cue, start=min(w['start'] for w in timed),
                                 end=max(w['end'] for w in timed)))
        else:
            proposal.append(cue.copy())
    report = dict(language='vi', engine='whisperx', alignment_model=ALIGN_MODEL,
                  device='cpu', original_inputs=original, duration_seconds=duration,
                  original_cues=cues, aligned_segments=aligned_segments, word_segments=words,
                  words_missing_timestamps=missing, source_text_preserved=True,
                  timing_requires_review=True, listening_qc=False,
                  region_and_tones_verified=False, voice_modified=False)
    out.mkdir(parents=True, exist_ok=True)
    (out / 'alignment.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    write(proposal, out / 'aligned_proposal.srt')
    if original != {'audio_sha256': digest(args.audio), 'srt_sha256': digest(args.srt)}:
        raise RuntimeError('Input changed during alignment; discard result and investigate.')
    print(json.dumps({'output': str(out), 'cues': len(cues), 'words': len(words),
                      'words_missing_timestamps': len(missing), 'listening_qc': False}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
