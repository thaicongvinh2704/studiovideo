import shutil
import subprocess
import wave
from pathlib import Path

def wav_duration(path):
    with wave.open(str(path),'rb') as w:
        return w.getnframes()/w.getframerate()

class VoiceEngine:
    def __init__(self, voice_folder):
        self.folder = Path(voice_folder)
        self.loaded = {}

    def voices(self):
        voices=[]
        for p in self.folder.glob('*.onnx'):
            if p.with_suffix(p.suffix+'.json').is_file():
                voices.append((p.stem,str(p)))
        if shutil.which('espeak-ng'): voices.append(('eSpeak NG · Tiếng Việt (robot)','espeak'))
        if not voices: voices.append(('Giọng hệ thống Windows (không đảm bảo tiếng Việt)','system'))
        return voices

    def synthesize(self,text,voice,path,speed=1.,volume=1.):
        if not text.strip(): raise ValueError('Nội dung giọng đọc đang trống.')
        Path(path).parent.mkdir(parents=True,exist_ok=True)
        if voice == 'espeak':
            subprocess.run(['espeak-ng','-v','vi','-s',str(round(165*speed)),'-a',str(round(volume*100)),
                            '-w',str(path),'--stdin'],input=text.encode('utf-8'),check=True,
                           creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        elif voice=='system':
            # Pass text and output via files rather than constructing PowerShell code from user input.
            source=Path(path).with_suffix('.txt');source.write_text(text,encoding='utf-8-sig')
            script=Path(path).with_suffix('.ps1')
            script.write_text('param([string]$textFile,[string]$waveFile,[int]$rate,[int]$volume)\n'
                'Add-Type -AssemblyName System.Speech\n'
                '$s=New-Object System.Speech.Synthesis.SpeechSynthesizer\n'
                '$s.Rate=$rate; $s.Volume=$volume\n'
                '$s.SetOutputToWaveFile($waveFile)\n'
                '$s.Speak([IO.File]::ReadAllText($textFile))\n$s.Dispose()\n',encoding='utf-8-sig')
            try:
                subprocess.run(['powershell','-NoProfile','-ExecutionPolicy','Bypass','-File',str(script),
                                str(source),str(path),str(round((speed-1)*5)),str(round(min(1,volume)*100))],
                               check=True,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
            finally: source.unlink(missing_ok=True);script.unlink(missing_ok=True)
        else:
            from piper import PiperVoice, SynthesisConfig
            if voice not in self.loaded:
                self.loaded[voice]=PiperVoice.load(voice,use_cuda=False)
            with wave.open(str(path),'wb') as wav:
                self.loaded[voice].synthesize_wav(text,wav,syn_config=SynthesisConfig(length_scale=1/max(.5,speed),volume=volume))
        return wav_duration(path)
