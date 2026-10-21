import copy
import math
import tempfile
import unittest
from pathlib import Path
from studio import animation as a
from studio.demo import demo
from studio.project import new_project,new_object,save,load,duration,scene_at,pack,unpack
from studio.subtitles import parse,active,stamp,seconds,write,read

class CoreTests(unittest.TestCase):
    def test_srt_bom_and_multiline(self):
        cues=parse('\ufeff1\r\n00:00:02,500 --> 00:00:05,000\r\nCha và con\r\nĐi dưới mưa\r\n')
        self.assertEqual(cues[0]['start'],2.5);self.assertEqual(active(cues,2.499),'')
        self.assertIn('Đi dưới mưa',active(cues,2.5));self.assertEqual(active(cues,5),'')
    def test_invalid_srt(self):
        for text in ('1\n00:00:05,000 --> 00:00:01,000\na','1\n00:61:00,000 --> 00:62:00,000\na'):
            with self.assertRaises(ValueError):parse(text)
    def test_roundtrip_timestamps(self):
        for t in (0,5.125,3599.999,3600,54000.25):self.assertAlmostEqual(seconds(stamp(t)),t,places=3)
    def test_interpolation(self):
        self.assertEqual(a.sample([{'t':2,'v':10},{'t':4,'v':20}],3,0),15)
        self.assertEqual(a.sample([{'t':2,'v':10}],1,0),10)
        self.assertEqual(a.sample([],2,5),5)
        self.assertLess(a.ease(.25,'ease_in'),.25)
        self.assertGreater(a.ease(.25,'ease_out'),.25)
        self.assertAlmostEqual(a.ease(.5,'ease_in_out'),.5)
        self.assertAlmostEqual(a.ease(.5,'bezier',(0,0,1,1)),.5,places=6)
    def test_two_bone_ik(self):
        joint,end=a.ik((0,0),(50,40),43,41)
        self.assertAlmostEqual(math.hypot(*joint),43)
        self.assertAlmostEqual(math.dist(joint,end),41)
        self.assertAlmostEqual(math.dist(end,(50,40)),0)
        j,end=a.ik((0,0),(500,0),43,41)
        self.assertLessEqual(math.hypot(*end),84)
    def test_walk_has_articulated_motion(self):
        o=new_object();o['action']='walk'
        j0,_=a.skeleton(o,0);j1,_=a.skeleton(o,.2)
        self.assertNotEqual(j0['knee_l'],j1['knee_l']);self.assertNotEqual(j0['hand_r'],j1['hand_r'])
        self.assertEqual(a.skeleton(o,.2),a.skeleton(o,.2))
        self.assertAlmostEqual(math.dist(j1['shoulder_r'],j1['elbow_r']),43)
    def test_actions_and_blend(self):
        self.assertEqual(len(a.ACTIONS),20)
        for action in a.ACTIONS:
            o=new_object();o['action']=action
            joints,st=a.skeleton(o,.4)
            self.assertTrue(all(math.isfinite(v) for point in joints.values() for v in point))
        o=new_object();o['motions']=[dict(start=0,end=2,action='walk'),dict(start=2,end=4,action='wave',blend=.5)]
        before=a.motion_pose(o,1.999);after=a.motion_pose(o,2.001)
        self.assertLess(abs(before['arm_r']-after['arm_r']),.02)
    def test_prop_attachment_handoff(self):
        s=demo()['scenes'][10];umbrella=s['objects'][-1];father,son=s['objects'][:2]
        self.assertEqual(a.attachment(umbrella,s['objects'],3),a.evaluate_scene(s['objects'],3)[father['id']][0]['hand_l'])
        self.assertEqual(a.attachment(umbrella,s['objects'],9),a.evaluate_scene(s['objects'],9)[son['id']][0]['hand_r'])
        self.assertNotEqual(a.evaluate_scene(s['objects'],9)[son['id']][0]['hand_r'],a.skeleton(son,12)[0]['hand_r'])
    def test_project_roundtrip_and_media_package(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as tmp:
            folder=Path(tmp);p=demo();media=folder/'source.wav';media.write_bytes(b'example')
            p['audio']=[dict(file=str(media),start=0,duration=1,group='voice')]
            saved=save(p,folder/'original'/'project.json',folder)
            self.assertEqual(saved,load(folder/'original'/'project.json'))
            self.assertFalse(Path(saved['audio'][0]['file']).is_absolute())
            pack(saved,folder/'original',folder/'project.zip')
            opened=unpack(folder/'project.zip',folder/'imported')
            self.assertEqual(load(opened),saved)
    def test_demo_and_long_timeline_boundaries(self):
        p=demo();self.assertEqual(len(p['scenes']),12);self.assertEqual(len(p['subtitles']),36);self.assertEqual(duration(p),180)
        self.assertEqual(scene_at(p,15)[0]['name'],p['scenes'][1]['name']);self.assertIsNone(scene_at(p,180)[0])
        p['scenes'][-1]['duration']=915
        self.assertEqual(duration(p),1080)
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as tmp:
            saved=save(p,Path(tmp)/'long.json');self.assertEqual(duration(load(Path(tmp)/'long.json')),1080)

if __name__=='__main__':unittest.main()
