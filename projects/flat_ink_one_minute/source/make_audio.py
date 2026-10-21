"""Use thirteen complete supplied-script cues, uniformly retimed to exactly one minute."""
import json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
DEST=Path(__file__).resolve().parents[1];OLD=ROOT/'projects'/'nguoi_viet_co_5phut'
from studio.subtitles import read,write
from studio.exporter import binary,FLAGS


def prepare():
    cues=read(OLD/'source'/'kich_ban_goc.srt')[:13];original_end=cues[-1]['end'];factor=60/original_end
    for c in cues:c['start']*=factor;c['end']*=factor
    cues[-1]['end']=60;write(cues,DEST/'phu_de.srt')
    subprocess.run([binary('ffmpeg'),'-y','-v','error','-i',str(OLD/'narration.wav'),'-af',f'atrim=0:{original_end},asetpts=PTS-STARTPTS,atempo={1/factor:.12f},apad,atrim=duration=60','-ar','48000','-ac','2','-c:a','pcm_s16le',str(DEST/'narration.wav')],check=True,creationflags=FLAGS)
    (DEST/'timing.json').write_text(json.dumps(dict(source='First thirteen cues of user SRT',source_seconds=original_end,output_seconds=60,timing_scale=factor,voice='Existing generated Piper Vietnamese narration, uniformly retimed by 2.14%; no truncated sentences'),indent=2),encoding='utf-8')
    print('Audio and 13 subtitles ready: 60 seconds')


if __name__=='__main__':prepare()
