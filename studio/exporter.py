"""Bounded-memory CPU rendering; atomic delivery, real progress, cancellation."""
import math
import os
import shutil
import subprocess
import tempfile
import threading
import json
import hashlib
from pathlib import Path
from .project import duration, resolve, missing
from .renderer import Renderer
from .animation import ENGINE_VERSION
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QFontInfo

EXPORT_VERSION='explainer-3.2-photo-orientation'
PROFILES={'draft':dict(crf=23,preset='veryfast'),'balanced':dict(crf=20,preset='fast'),'final':dict(crf=18,preset='medium')}

FLAGS = getattr(subprocess,'CREATE_NO_WINDOW',0)

def binary(name):
    import sys
    root=Path(sys.executable).parent if getattr(sys,'frozen',False) else Path(__file__).resolve().parents[1]
    local=root/'bin'/f'{name}.exe'
    found=str(local) if local.exists() else shutil.which(name)
    if not found: raise FileNotFoundError(f'Thiếu {name}. Cài FFmpeg hoặc đặt {name}.exe trong thư mục bin.')
    return found

class Cancelled(Exception): pass

def checked_run(args,cancel=None):
    with tempfile.TemporaryFile(dir=Path(args[-1]).parent) as log:
        p=subprocess.Popen(args,stdout=subprocess.DEVNULL,stderr=log,creationflags=FLAGS)
        while True:
            try: code=p.wait(timeout=.15);break
            except subprocess.TimeoutExpired:
                if cancel and cancel.is_set():
                    p.kill();p.wait();raise Cancelled('Đã hủy xuất video.')
        if code:
            log.seek(0);raise RuntimeError(log.read().decode('utf-8','replace')[-4000:])

def mix_audio(project,root,output,start=0.,length=None,cancel=None):
    length=length or duration(project)
    ffmpeg=binary('ffmpeg')
    rate=int(project.get('audio_rate',48000));channels=int(project.get('audio_channels',2))
    if rate not in (22050,44100,48000) or channels not in (1,2):raise ValueError('Thông số âm thanh không hợp lệ.')
    # Mix small batches before grouping to avoid hundreds of FFmpeg input streams/handles.
    groups={g:[] for g in ('voice','music','sfx')}
    for a in project['audio']:
        if a.get('mute'): continue
        if a['start'] < start+length-.5/rate and a['start']+a['duration'] > start+.5/rate:
            groups.setdefault(a.get('group','voice'),[]).append(a)
    with tempfile.TemporaryDirectory(prefix='stickman_audio_',dir=Path(output).parent) as tmp:
        stems={}
        for group,clips in groups.items():
            batches=[]
            for offset in range(0,len(clips),12):
                args=[ffmpeg,'-y','-v','error'];filters=[];labels=[]
                for i,a in enumerate(clips[offset:offset+12]):
                    path=resolve(root,a['file'])
                    if not path.exists(): raise FileNotFoundError(path)
                    args+=['-i',str(path)]
                    cut=max(0,start-a['start']);clip_len=min(a['duration']-cut,start+length-max(a['start'],start))
                    trim=a.get('trim',0)+cut;delay=round(max(0,a['start']-start)*1000)
                    fi=min(a.get('fade_in',0),clip_len);fo=min(a.get('fade_out',0),clip_len)
                    filters.append(f'[{i}:a]atrim=start={trim:.9f}:duration={clip_len:.9f},asetpts=PTS-STARTPTS,'
                        f'volume={a.get("volume",1)},afade=t=in:d={fi:.9f},afade=t=out:st={max(0,clip_len-fo):.9f}:d={fo:.9f},'
                        f'adelay={delay}:all=1[a{i}]')
                    labels.append(f'[a{i}]')
                filters.append(''.join(labels)+f'amix=inputs={len(labels)}:normalize=0,aresample={rate},'
                    f'apad=whole_dur={length},atrim=end_sample={round(length*rate)},asetpts=N/SR/TB[mix]')
                dest=Path(tmp)/f'{group}_{offset}.wav'
                args+=['-filter_complex',';'.join(filters),'-map','[mix]','-t',str(length),'-ar',str(rate),'-ac',str(channels),str(dest)]
                checked_run(args,cancel);batches.append(dest)
            if batches:
                args=[ffmpeg,'-y','-v','error']
                for b in batches: args+=['-i',str(b)]
                dest=Path(tmp)/f'{group}.wav'
                args+=['-filter_complex', ''.join(f'[{i}:a]' for i in range(len(batches)))+
                       f'amix=inputs={len(batches)}:normalize=0,asetpts=N/SR/TB[a]','-map','[a]','-t',str(length),str(dest)]
                checked_run(args,cancel);stems[group]=dest
        if not stems:
            checked_run([ffmpeg,'-y','-v','error','-f','lavfi','-i',f'anullsrc=r={rate}:cl={"stereo" if channels==2 else "mono"}','-t',str(length),str(output)],cancel)
            return
        args=[ffmpeg,'-y','-v','error'];index={}
        for i,(g,path) in enumerate(stems.items()): args+=['-i',str(path)];index[g]=i
        filters=[];labels=[]
        if project.get('duck_music') and 'voice' in index and 'music' in index:
            filters.append(f'[{index["voice"]}:a]asplit=2[v][side]')
            filters.append(f'[{index["music"]}:a][side]sidechaincompress=threshold=0.02:ratio=6:attack=25:release=400[m]')
            labels=['[v]','[m]']
        else:
            labels=[f'[{i}:a]' for g,i in index.items() if g in ('voice','music')]
        labels += [f'[{i}:a]' for g,i in index.items() if g not in ('voice','music')]
        filters.append(''.join(labels)+f'amix=inputs={len(labels)}:normalize=0,alimiter=limit=0.95:latency=1,aresample={rate},'
            f'apad=whole_dur={length},atrim=end_sample={round(length*rate)},asetpts=N/SR/TB[out]')
        args+=['-filter_complex',';'.join(filters),'-map','[out]','-t',str(length),'-ar',str(rate),'-ac',str(channels),str(output)]
        checked_run(args,cancel)

def export_video(project,root,output,width=None,height=None,fps=None,start=0,length=None,burn=True,
                 progress=lambda a,b:None,cancel=None,gpu=False):
    from .character_qc import require_project_qc
    require_project_qc(project,root)
    from .directing import preflight
    gaps=preflight(project,root)
    if gaps and not project.get('allow_draft',False):
        raise ValueError('Chưa thể xuất bản hoàn chỉnh:\n'+'\n'.join(x.get('scene','')+': '+x['message'] for x in gaps))
    width=width or project['width'];height=height or project['height'];fps=fps or project.get('fps',24)
    if width%2 or height%2 or fps not in (12,24,30):raise ValueError('Kích thước phải chẵn; FPS: 12, 24 hoặc 30.')
    profile=PROFILES.get(project.get('render_profile','final'),PROFILES['final'])
    supersample=min(2,max(1,int(project.get('supersample',1))))
    cancel=cancel or threading.Event()
    length=length if length is not None else duration(project)-start
    if length<=0: raise ValueError('Không có thời lượng để xuất.')
    absent=missing(project,root)
    if absent: raise FileNotFoundError('Thiếu tài nguyên:\n'+'\n'.join(absent))
    output=Path(output).resolve();output.parent.mkdir(parents=True,exist_ok=True)
    total=math.ceil(length*fps-1e-8)
    ffmpeg=binary('ffmpeg')
    renderer=Renderer()
    # Temporary files stay on the output drive; final path changes only after success.
    with tempfile.TemporaryDirectory(prefix='stickman_render_',dir=output.parent) as tmp:
        tmp=Path(tmp);video=tmp/'video.mp4'
        use_gpu = gpu or project.get('gpu', False)
        if use_gpu:
            codec_opts = ['-c:v', 'h264_nvenc', '-preset', 'p4', '-cq', str(profile['crf'])]
        else:
            codec_opts = ['-c:v', 'libx264', '-preset', profile['preset'], '-crf', str(profile['crf']),
                          '-threads', str(min(2, max(1, int(project.get('encoder_threads', 2)))))]
        args=[ffmpeg,'-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{width}x{height}',
              '-r',str(fps),'-i','pipe:0','-an','-vf','scale=out_color_matrix=bt709:out_range=tv'] +              codec_opts +              ['-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-color_range','tv',
              '-pix_fmt','yuv420p',str(video)]
        with (tmp/'ffmpeg.log').open('w+b') as log:
            proc=subprocess.Popen(args,stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=log,creationflags=FLAGS)
            try:
                for i in range(total):
                    if cancel.is_set(): raise Cancelled('Đã hủy xuất video.')
                    if i%fps==0 and shutil.disk_usage(output.parent).free < 32*1024**2:
                        raise OSError('Dung lượng ổ đĩa còn dưới 32 MB.')
                    im=renderer.frame(project,root,start+i/fps,width*supersample,height*supersample,burn=burn)
                    if supersample>1:im=im.scaled(width,height,Qt.AspectRatioMode.IgnoreAspectRatio,Qt.TransformationMode.SmoothTransformation)
                    data=bytes(im.constBits())
                    # Qt adds scanline padding at widths such as 854.
                    if im.bytesPerLine()!=width*3:
                        stride=im.bytesPerLine();data=b''.join(data[y*stride:y*stride+width*3] for y in range(height))
                    proc.stdin.write(data)
                    progress(i+1,total)
                proc.stdin.close()
                while proc.poll() is None:
                    if cancel.is_set(): raise Cancelled('Đã hủy xuất video.')
                    try: proc.wait(timeout=.15)
                    except subprocess.TimeoutExpired: pass
                if proc.returncode:
                    log.seek(0);raise RuntimeError(log.read().decode('utf-8','replace')[-4000:])
            except BrokenPipeError:
                proc.wait();log.seek(0);raise RuntimeError(log.read().decode('utf-8','replace')[-4000:])
            finally:
                if proc.poll() is None: proc.kill();proc.wait()
                if proc.stdin and not proc.stdin.closed: proc.stdin.close()
        progress(total,total)
        mixed=tmp/'audio.wav';mix_audio(project,root,mixed,start,length,cancel)
        final=tmp/'final.mp4'
        checked_run([ffmpeg,'-y','-v','error','-i',str(video),'-i',str(mixed),'-c:v','copy',
                     '-c:a','aac','-b:a','128k','-t',str(length),'-movflags','+faststart',str(final)],cancel)
        validate_output(final,width,height,fps,length)
        if cancel.is_set(): raise Cancelled('Đã hủy xuất video.')
        os.replace(final,output)
    return output

def validate_output(path,width,height,fps,length):
    result=json.loads(subprocess.check_output([binary('ffprobe'),'-v','error','-show_streams','-show_format',
        '-of','json',str(path)],creationflags=FLAGS))
    video=next((s for s in result['streams'] if s['codec_type']=='video'),{})
    audio=next((s for s in result['streams'] if s['codec_type']=='audio'),{})
    if video.get('width')!=width or video.get('height')!=height or video.get('codec_name')!='h264' or not audio:
        raise RuntimeError('Kiểm tra MP4 thất bại: sai kích thước/codec hoặc thiếu audio stream.')
    num,den=map(int,video['r_frame_rate'].split('/'))
    if abs(num/den-fps)>.01 or abs(float(result['format']['duration'])-length)>max(.2,1/fps):
        raise RuntimeError('Kiểm tra MP4 thất bại: sai FPS hoặc thời lượng.')
    expected=math.ceil(length*fps-1e-8)
    if video.get('nb_frames') and int(video['nb_frames'])!=expected:
        raise RuntimeError(f'Kiểm tra MP4 thất bại: cần {expected} frame, nhận {video["nb_frames"]}.')

def export_cached(project,root,output,width=None,height=None,fps=None,burn=True,
                  progress=lambda a,b:None,cancel=None):
    """Retain successfully rendered scenes; retry interrupted jobs without rerendering them."""
    from .character_qc import require_project_qc
    require_project_qc(project,root)
    from .directing import preflight
    gaps=preflight(project,root)
    if gaps and not project.get('allow_draft',False):raise ValueError('Cần hoàn thiện hình / tài nguyên trước khi xuất:\n'+'\n'.join(x['message'] for x in gaps))
    width=width or project['width'];height=height or project['height'];fps=fps or project.get('fps',24)
    cancel=cancel or threading.Event();output=Path(output).resolve()
    cache=output.parent/(output.stem+'_scenes');cache.mkdir(parents=True,exist_ok=True)
    from .project import media_entries
    media=[(o[k],resolve(root,o[k]).stat().st_mtime_ns) for o,k in media_entries(project)]
    manifest_path=cache/'manifest.json'
    manifest=json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    manifest.setdefault('completed',[]);manifest.setdefault('scene_keys',{})
    total=math.ceil(duration(project)*fps-1e-8);done=0;files=[]
    for i,s in enumerate(project['scenes']):
        if cancel.is_set():raise Cancelled('Đã hủy; các cảnh hoàn tất được giữ để tiếp tục.')
        path=cache/f'scene_{i+1:04}.mp4'
        first=math.ceil(s['start']*fps-1e-8);last=math.ceil((s['start']+s['duration'])*fps-1e-8);count=last-first
        if count<=0:continue
        render_start=first/fps;render_length=count/fps
        local={k:v for k,v in project.items() if k!='storyboard'};local['scenes']=[s]
        for field,end_key in [('subtitles','end'),('audio','duration')]:
            local[field]=[a for a in project[field] if a['start']<s['start']+s['duration'] and
                          (a['end'] if end_key=='end' else a['start']+a['duration'])>s['start']]
        names={o[k] for o,k in media_entries(local)}
        fingerprint=cache_fingerprint(local,[m for m in media if m[0] in names],width,height,fps,burn)
        valid=False
        if manifest['scene_keys'].get(str(i))==fingerprint and path.exists():
            try:validate_output(path,width,height,fps,render_length);valid=True
            except Exception:pass
        if not valid:
            export_video(local,root,path,width,height,fps,render_start,render_length,burn,
                         lambda a,b,offset=done:progress(offset+a,total),cancel)
            if i not in manifest['completed']:manifest['completed'].append(i)
            manifest['scene_keys'][str(i)]=fingerprint
            temp=manifest_path.with_suffix('.tmp');temp.write_text(json.dumps(manifest));temp.replace(manifest_path)
        done+=count;progress(done,total);files.append((path.name,render_length))
    concat=cache/'concat.txt';concat.write_text('\n'.join(f'file {name}\nduration {length:.10f}' for name,length in files),encoding='utf-8')
    with tempfile.TemporaryDirectory(prefix='stickman_concat_',dir=output.parent) as tmp:
        video=Path(tmp)/'video.mp4'
        checked_run([binary('ffmpeg'),'-y','-v','error','-f','concat','-safe','1','-i',str(concat),
                     '-map','0:v:0','-an','-c:v','copy','-movflags','+faststart',str(video)],cancel)
        # The concat demuxer can carry the first scene's AAC priming into the
        # video timestamps even when its audio stream is discarded. Normalize
        # that single global offset before combining with the full audio mix.
        start_probe=json.loads(subprocess.check_output([binary('ffprobe'),'-v','error','-select_streams','v:0',
            '-show_entries','stream=start_time','-of','json',str(video)],creationflags=FLAGS))
        video_start=float(start_probe['streams'][0].get('start_time',0) or 0)
        # One full-length audio mix avoids per-scene AAC priming accumulating over long videos.
        mixed=Path(tmp)/'audio.wav';mix_audio(project,root,mixed,0,duration(project),cancel)
        final=Path(tmp)/'final.mp4'
        checked_run([binary('ffmpeg'),'-y','-v','error','-itsoffset',f'{-video_start:.9f}','-i',str(video),'-i',str(mixed),'-map','0:v:0','-map','1:a:0',
                     '-c:v','copy','-c:a','aac','-b:a','192k','-t',str(duration(project)),'-movflags','+faststart',str(final)],cancel)
        validate_output(final,width,height,fps,duration(project))
        if cancel.is_set():raise Cancelled('Đã hủy xuất video.')
        os.replace(final,output)
    return output


def cache_fingerprint(project,media,width,height,fps,burn):
    font=QFontInfo(QFont(project.get('subtitle_style',{}).get('font','Segoe UI'))).family()
    payload=[ENGINE_VERSION,EXPORT_VERSION,font,project,media,width,height,fps,burn]
    return hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest()
