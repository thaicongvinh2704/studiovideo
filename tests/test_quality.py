"""Quality invariants which the original functional tests did not cover."""
import copy
import math
import unittest
from unittest.mock import patch
from PySide6.QtWidgets import QApplication
from studio import animation as a
from studio.demo import demo
from studio.project import new_object
from studio.exporter import cache_fingerprint

APP=QApplication.instance() or QApplication([])

class QualityTests(unittest.TestCase):
    def test_stance_foot_is_locked_in_world_space(self):
        obj=demo()['scenes'][0]['objects'][0]
        for side in ('l','r'):
            anchors={}
            for i in range(1,359):
                t=i/24;target,stance=a.gait(obj,t,side)
                if not stance:continue
                joints,st=a.skeleton(obj,t)
                self.assertLess(math.dist(joints['foot_'+side],target),.001)
                self.assertAlmostEqual(target[1],575)
                index=round(target[0],3)
                anchors.setdefault(index,[]).append(joints['foot_'+side][0])
            self.assertGreater(len(anchors),3)
            self.assertTrue(all(max(xs)-min(xs)<.001 for xs in anchors.values()))

    def test_walk_clip_uses_grounding_even_with_idle_base(self):
        obj=new_object(x=200,y=575);obj['motions']=[dict(start=1,end=4,action='walk',blend=0)]
        obj['keys']['x']=[dict(t=1,v=200),dict(t=4,v=400)]
        for side in ('l','r'):
            for t in (1.1,1.5,2,2.5,3):
                target,_=a.gait(obj,t,side)
                self.assertLess(math.dist(a.skeleton(obj,t)[0]['foot_'+side],target),.001)

    def test_contact_and_umbrella_ownership_are_continuous(self):
        scene=demo()['scenes'][10];father,son,umbrella=scene['objects']
        before=a.attachment(umbrella,scene['objects'],3.2-1e-6)
        after=a.attachment(umbrella,scene['objects'],3.2+1e-6)
        self.assertLess(math.dist(before,after),.001)
        for t in (2.5,3,3.2,3.5):
            poses=a.evaluate_scene(scene['objects'],t)
            self.assertLess(math.dist(poses[father['id']][0]['hand_l'],poses[son['id']][0]['hand_r']),.001)

    def test_hug_contacts_reach_the_other_person(self):
        scene=demo()['scenes'][-1]
        for t in (4.5,6,8):
            poses=a.evaluate_scene(scene['objects'],t)
            for obj in scene['objects']:
                for c in obj.get('contacts',[]):
                    target=poses[c['target']][0][c['joint']]
                    target=tuple(x+y for x,y in zip(target,c.get('offset',[0,0])))
                    self.assertLess(math.dist(target,poses[obj['id']][0]['hand_'+c['hand']]),.01)

    def test_jump_has_a_landing_and_does_not_loop_implicitly(self):
        self.assertLess(a.pose('jump',.3)['lift'],0)
        self.assertGreater(a.pose('jump',.9)['lift'],70)
        self.assertEqual(a.pose('jump',3)['lift'],0)
        self.assertEqual(a.pose('jump',8)['lift'],0)

    def test_arbitrary_seek_is_deterministic_and_does_not_mutate_project(self):
        scene=demo()['scenes'][-1];original=copy.deepcopy(scene)
        expected=a.evaluate_scene(scene['objects'],8)
        for t in (12,0,4,11,2):a.evaluate_scene(scene['objects'],t)
        self.assertEqual(a.evaluate_scene(scene['objects'],8),expected)
        self.assertEqual(scene,original)

    def test_demo_motion_boundaries_do_not_pop(self):
        for scene in demo()['scenes']:
            for obj in scene['objects']:
                if obj['kind']!='character':continue
                boundaries={c[k] for c in obj.get('motions',[]) for k in ('start','end')}
                for t in boundaries:
                    if t<=0 or t>=scene['duration']:continue
                    before=a.evaluate_scene(scene['objects'],t-1e-6)[obj['id']][0]
                    after=a.evaluate_scene(scene['objects'],t+1e-6)[obj['id']][0]
                    for joint in before:
                        self.assertLess(math.dist(before[joint],after[joint]),.05,(scene['name'],obj['preset'],t,joint))

    def test_age_proportions_and_turn_do_not_collapse(self):
        obj=new_object();lengths=[]
        for age in ('child','teen','adult'):
            obj['age']=age;lengths.append(sum(a.dimensions(obj)[:5]))
        self.assertLess(lengths[0],lengths[1]);self.assertLess(lengths[1],lengths[2])
        obj['action']='turn';joints,_=a.skeleton(obj,math.pi/4)
        self.assertGreater(math.dist(joints['shoulder_l'],joints['shoulder_r']),20)

    def test_camera_selects_shot_and_editor_uses_same_values(self):
        from studio.ui.canvas import Canvas
        scene=demo()['scenes'][10];canvas=Canvas();canvas.current_scene=scene;canvas.time=3
        self.assertEqual(canvas.camera_values(),a.camera_values(scene,3))
        self.assertNotEqual(a.camera_values(scene,3),a.camera_values(scene,7));canvas.close()

    def test_floor_moves_with_camera_in_rendered_pixels(self):
        from studio.project import new_project
        from studio.renderer import Renderer
        p=new_project();p['scenes'][0]['camera'].update(x=640,y=500,zoom=2)
        im=Renderer().frame(p,'.',2,1280,720,burn=False,effects=False)
        self.assertEqual(im.pixelColor(50,520).name(),'#e2e1d6')
        self.assertNotEqual(im.pixelColor(50,500).name(),'#e2e1d6')

    def test_cache_invalidates_when_engine_or_profile_changes(self):
        p=demo();key=cache_fingerprint(p,[],1920,1080,24,True)
        with patch('studio.exporter.ENGINE_VERSION','next'):
            self.assertNotEqual(key,cache_fingerprint(p,[],1920,1080,24,True))
        p['render_profile']='draft'
        self.assertNotEqual(key,cache_fingerprint(p,[],1920,1080,24,True))

    def test_contact_and_shot_editors_preserve_authored_data(self):
        from studio.ui.quality_dialogs import ContactDialog,ShotDialog
        scene=demo()['scenes'][10];obj=scene['objects'][0];original=copy.deepcopy(obj['contacts'])
        d=ContactDialog(obj,scene);d.commit();self.assertEqual(obj['contacts'],original)
        original=copy.deepcopy(scene['camera']['shots']);d=ShotDialog(scene);d.commit()
        self.assertEqual(scene['camera']['shots'],original)

if __name__=='__main__':unittest.main()
