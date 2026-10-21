import unittest
from PySide6.QtWidgets import QApplication
from studio.project import new_project
from studio.explainer import presenter
from studio.media import bind_narrator_mouth
from studio.animation import sample
from studio.renderer import Renderer

APP=QApplication.instance() or QApplication([])

class VoicePerformanceTests(unittest.TestCase):
    def test_trimmed_voice_uses_scene_local_time_and_closes_in_gaps(self):
        p=new_project(duration=2);s=p['scenes'][0];s['start']=10
        actor=presenter();s['objects']=[actor]
        p['audio']=[dict(start=10.5,duration=.5,trim=90,group='voice',waveform=[.4]*10,waveform_hz=20)]
        bind_narrator_mouth(p);keys=actor['keys']['mouth_open']
        self.assertEqual(sample(keys,.1,0),0)
        self.assertGreater(sample(keys,.65,0),.7)
        self.assertEqual(sample(keys,1.3,0),0)
        actor['speech_source']='manual';actor['keys']['mouth_open']=[dict(t=0,v=.25)]
        bind_narrator_mouth(p);self.assertEqual(actor['keys']['mouth_open'],[dict(t=0,v=.25)])

    def test_held_skeleton_does_not_cache_over_speaking_face(self):
        p=new_project(duration=3);p['subtitle_style']['enabled']=False
        s=p['scenes'][0];s['background']='white';o=presenter(640,620,2,'rest');s['objects']=[o]
        o['keys']['mouth_open']=[dict(t=0,v=0),dict(t=1,v=1),dict(t=2,v=0)]
        o['keys']['blink']=[dict(t=0,v=0)]
        r=Renderer();closed=r.frame(p,'.',0);opened=r.frame(p,'.',1)
        self.assertNotEqual(closed,opened)
        self.assertEqual(closed,r.frame(p,'.',2))

if __name__=='__main__':unittest.main()
