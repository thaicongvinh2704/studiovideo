"""Bounded-memory waveform analysis used by the native timeline."""
import array
import subprocess
from .exporter import binary,FLAGS

def waveform(path,cancel=None):
    proc=subprocess.Popen([binary('ffmpeg'),'-v','error','-i',str(path),'-vn','-ar','8000','-ac','1','-f','s16le','pipe:1'],
        stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,creationflags=FLAGS)
    peaks=[]
    try:
        while True:
            if cancel and cancel.is_set():raise RuntimeError('Đã hủy phân tích voice.')
            data=proc.stdout.read(800) # 50ms, 400 int16 samples
            if not data:break
            values=array.array('h');values.frombytes(data[:len(data)//2*2])
            peaks.append(round(max((abs(v) for v in values),default=0)/32768,4))
        if proc.wait()!=0:raise ValueError('Không đọc được waveform voice.')
    finally:
        if proc.poll() is None:proc.kill();proc.wait()
        proc.stdout.close()
    return peaks

def add_waveforms(project,root,cancel=None):
    from .project import resolve
    cache={}
    for clip in project.get('audio',[]):
        if clip.get('group')!='voice':continue
        path=str(resolve(root,clip['file']))
        if path not in cache:cache[path]=waveform(path,cancel)
        offset=round(clip.get('trim',0)*20);count=round(clip['duration']*20)
        clip['waveform']=cache[path][offset:offset+count];clip['waveform_hz']=20
    bind_narrator_mouth(project)
    return project


def bind_narrator_mouth(project):
    """Persist an editable voice envelope, not phoneme/viseme recognition.

    Clip waveforms already include source trim. Times below are scene-local,
    so imported/reordered scene-owned narration stays aligned with its actor.
    Hand-authored mouth keys are preserved.
    """
    clips=[a for a in project.get('audio',[]) if a.get('group')=='voice' and a.get('volume',1)>0 and a.get('waveform')]
    maximum=max((max(a['waveform']) for a in clips),default=0)
    threshold=max(.008,maximum*.035)
    for scene in project['scenes']:
        start=scene['start'];length=scene['duration']
        relevant=[a for a in clips if a['start']<start+length and a['start']+a['duration']>start]
        if not relevant:continue
        for actor in scene['objects']:
            if actor.get('speech_role')!='narrator' or actor.get('skin')!='ink':continue
            keys=actor.setdefault('keys',{})
            if keys.get('mouth_open') and actor.get('speech_source')!='voice_waveform':continue
            frames=[]
            for i in range(int(length*20)+2):
                local=min(length,i/20);world=start+local;peak=0
                for clip in relevant:
                    if not clip['start']<=world<clip['start']+clip['duration']:continue
                    hz=clip.get('waveform_hz',20);position=(world-clip['start'])*hz
                    index=int(position);wave=clip['waveform']
                    if index<len(wave):
                        left=wave[index];right=wave[min(index+1,len(wave)-1)]
                        peak=max(peak,left+(right-left)*(position-index))
                value=0 if peak<=threshold else min(.85,((peak-threshold)/max(.001,maximum-threshold))**1.1)
                frames.append(dict(t=local,v=round(value,4)))
                if local==length:break
            keys['mouth_open']=frames;actor['speech_source']='voice_waveform'
    return project


def pause_boundaries(path,length):
    """Silent spans are timing hints, never word recognition or forced alignment."""
    peaks=waveform(path);spans=[];start=None
    threshold=max(.008,max(peaks,default=0)*.035)
    for i,value in enumerate(peaks+[1]):
        if value<threshold and start is None:start=i
        elif value>=threshold and start is not None:
            if i-start>=3:spans.append((start/20,min(length,i/20)))
            start=None
    return spans


def align_estimated_cues(cues,path,length):
    import copy
    result=copy.deepcopy(cues);pauses=pause_boundaries(path,length)
    previous=0
    for i in range(len(result)-1):
        target=cues[i]['end'];upper=cues[i+1]['end']-.25
        options=[(a+b)/2 for a,b in pauses if previous+.25<(a+b)/2<upper and abs((a+b)/2-target)<=.8]
        chosen=min(options,key=lambda v:abs(v-target)) if options else target
        result[i]['end']=chosen;result[i+1]['start']=chosen;previous=chosen
    return result
