import json
import math
import struct
import subprocess
import tempfile
import unittest
import wave
from pathlib import Path
from PIL import Image
from PySide6.QtGui import QGuiApplication
from studio.renderer import Renderer
from studio.project import new_project, new_scene, new_object
from studio.exporter import export_cached,binary

APP=QGuiApplication.instance() or QGuiApplication([])
ROOT=Path(__file__).resolve().parents[1]


class MediaDeliveryTests(unittest.TestCase):
    def test_camera_photo_is_displayed_upright_without_rewriting_original(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'outputs') as tmp:
            path=Path(tmp)/'camera.jpg'
            im=Image.new('RGB',(40,20),'red');im.paste('blue',(20,0,40,20))
            exif=im.getexif();exif[274]=6;im.save(path,exif=exif)
            before=path.read_bytes();actual=Renderer().image(tmp,path.name)
            self.assertEqual((actual.width(),actual.height()),(20,40))
            self.assertGreater(actual.pixelColor(10,5).red(),200)
            self.assertGreater(actual.pixelColor(10,35).blue(),200)
            self.assertEqual(path.read_bytes(),before)

    def test_cached_audio_scenes_do_not_shift_video_by_aac_priming(self):
        try:binary('ffmpeg');binary('ffprobe')
        except FileNotFoundError:self.skipTest('FFmpeg not installed')
        with tempfile.TemporaryDirectory(dir=ROOT/'outputs') as tmp:
            root=Path(tmp);audio=root/'tone.wav'
            with wave.open(str(audio),'wb') as wav:
                wav.setnchannels(1);wav.setsampwidth(2);wav.setframerate(48000)
                wav.writeframes(b''.join(struct.pack('<h',int(8000*math.sin(i*2*math.pi*440/48000))) for i in range(48000)))
            p=new_project(width=320,height=180);p['scenes']=[]
            for i in range(2):
                s=new_scene(duration=.5);s.update(start=i*.5,background='white')
                o=new_object('shape','card');o.update(shape='card',width=300,height=200,end=.5,fill='#e6cba6')
                s['objects']=[o];p['scenes'].append(s)
            p['audio']=[dict(id='tone',file=str(audio),start=0,duration=1,group='voice',volume=1)]
            p['render_profile']='draft'
            output=root/'cached.mp4';export_cached(p,root,output,320,180,24)
            probe=json.loads(subprocess.check_output([binary('ffprobe'),'-v','error','-show_streams','-of','json',str(output)]))
            v=next(s for s in probe['streams'] if s['codec_type']=='video')
            a=next(s for s in probe['streams'] if s['codec_type']=='audio')
            self.assertEqual(int(v['nb_frames']),24)
            self.assertLess(abs(float(v['start_time'])-float(a['start_time'])),.002)
