import copy
import math
import tempfile
import unittest
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QImage,QPainter,QColor
from studio.explainer import presenter,apply_pose,compile_board,POSES
from studio.animation import skeleton,evaluate_scene,sample
from studio.hierarchy import world_states,transform_point,to_parent
from studio.project import new_object,new_project,save,load
from studio.renderer import Renderer
from studio.asset_library import CATALOG,asset
from studio.directing import preflight,editorial_suggestions

APP=QApplication.instance() or QApplication([])


class InkTests(unittest.TestCase):
    def test_all_library_art_is_valid_vector_and_renders_without_raster_cache(self):
        self.assertGreaterEqual(len(CATALOG),40)
        r=Renderer()
        for name in CATALOG:
            svg=r.vector('.',asset(name));self.assertTrue(svg.isValid(),name)
            im=QImage(400,320,QImage.Format.Format_ARGB32_Premultiplied);im.fill(QColor('white'))
            p=QPainter(im);svg.render(p);p.end()
            self.assertNotEqual(im, QImage(),name)
        self.assertFalse(r.cache)

    def test_pose_transitions_are_seekable_and_keep_bone_lengths(self):
        obj=presenter();obj['end']=50
        for i,pose in enumerate(POSES):
            if pose not in ('walk','sit'):apply_pose(obj,pose,i*2,.85)
        before=copy.deepcopy(obj)
        for t in [0,.35,2.1,5.3,17.4,8.9,2.1]:
            joints,_=skeleton(obj,t)
            for side in ('l','r'):
                self.assertAlmostEqual(math.dist(joints['shoulder_'+side],joints['elbow_'+side]),obj['rig']['upper_arm']*obj['scale'],places=5)
                self.assertAlmostEqual(math.dist(joints['elbow_'+side],joints['hand_'+side]),obj['rig']['forearm']*obj['scale'],places=5)
        self.assertEqual(obj,before)
        for t in (2,4,6,8):
            a=skeleton(obj,t-1e-6)[0];b=skeleton(obj,t+1e-6)[0]
            self.assertLess(max(math.dist(a[k],b[k]) for k in a),.01)

    def test_nested_parent_rotation_scale_opacity_and_inverse_coordinates(self):
        parent=new_object('group',x=100,y=200);parent.update(scale=2,rotation=90,opacity=.5,pivot=[10,0])
        child=new_object('group',x=20,y=5);child.update(parent=parent['id'],scale=.5,rotation=-30)
        leaf=new_object('shape',x=15,y=10);leaf['parent']=child['id']
        states=world_states([parent,child,leaf],0)
        self.assertAlmostEqual(states[child['id']]['x'],90)
        self.assertAlmostEqual(states[child['id']]['y'],220)
        self.assertAlmostEqual(states[leaf['id']]['rotation'],60)
        self.assertAlmostEqual(states[leaf['id']]['opacity'],.5)
        world=states[leaf['id']]
        local=to_parent((world['x'],world['y']),leaf,[parent,child,leaf],0)
        self.assertAlmostEqual(local[0],15);self.assertAlmostEqual(local[1],10)
        parent['parent']=leaf['id']
        with self.assertRaises(ValueError):world_states([parent,child,leaf],0)

    def test_bezier_editor_preserves_custom_curve_on_save(self):
        from studio.ui.dialogs import KeyframeDialog
        o=new_object();o['keys']={'x':[dict(t=0,v=20),dict(t=2,v=300,ease='bezier',bezier=[.4,-.1,.7,1.2],custom='keep')]}
        before=sample(o['keys']['x'],1,0)
        dialog=KeyframeDialog(o,0);dialog.commit();dialog.close()
        self.assertEqual(o['keys']['x'][1]['bezier'],[.4,-.1,.7,1.2])
        self.assertEqual(o['keys']['x'][1]['custom'],'keep');self.assertAlmostEqual(sample(o['keys']['x'],1,0),before)

    def test_portable_new_scene_and_placeholder_preflight(self):
        board=dict(version=1,rows=[dict(start=0,end=3,style='ink',layout='presenter',text='Một câu.',title='Kiểm tra',assets=[asset('city')])])
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as tmp:
            p=save(compile_board(board),Path(tmp)/'project.json')
            p=load(Path(tmp)/'project.json')
            # Legacy presenters can reopen, but final export now requires character QC.
            issues=preflight(p,tmp);self.assertTrue(issues)
            self.assertTrue(all(issue.get('code')=='character_qc' for issue in issues))
            renderer=Renderer();renderer.frame(p,tmp,1,640,360)
            self.assertFalse(renderer.cache);self.assertTrue(renderer.vectors)
        board['rows'][0]['assets']=[]
        self.assertTrue(preflight(compile_board(board),'.'))

    def test_suggestions_do_not_invent_a_visual_for_unknown_subject(self):
        rows=editorial_suggestions([dict(start=0,end=4,text='Một thuật ngữ hoàn toàn xa lạ được đặt ở đây.')],[])
        self.assertIn('missing_visual',rows[0]);self.assertEqual(rows[0]['assets'],[])
        rows=editorial_suggestions([dict(start=0,end=4,text='Bản đồ chỉ ra những tuyến đường di cư.')],[])
        self.assertEqual(rows[0]['layout'],'map');self.assertTrue(rows[0]['assets'])

    def test_pose_picker_and_library_are_real_populated_widgets(self):
        from studio.ui.ink_dialogs import PosePicker,ArtPicker
        p=PosePicker();self.assertEqual(p.box.count(),len(POSES));p.box.setCurrentRow(2);p.choose();self.assertIsNotNone(p.pose);p.close()
        a=ArtPicker();self.assertEqual(a.box.count(),len(CATALOG));a.box.setCurrentRow(3);a.choose();self.assertTrue(Path(a.file).is_file());a.close()

    def test_frame_cache_tracks_blinks_edits_and_changed_raster_files(self):
        p=new_project(duration=4);p['scenes'][0].update(background='white',objects=[])
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as tmp:
            path=Path(tmp)/'image.png';im=QImage(50,50,QImage.Format.Format_RGB32);im.fill(QColor('red'));im.save(str(path))
            o=new_object('image');o.update(file=str(path),width=200,height=200);p['scenes'][0]['objects']=[o]
            r=Renderer();a=r.frame(p,tmp,0,1280,720);b=r.frame(p,tmp,.5,1280,720)
            self.assertEqual(a,b)
            im.fill(QColor('blue'));im.save(str(path));c=r.frame(p,tmp,1,1280,720)
            self.assertNotEqual(a,c);self.assertEqual(c.pixelColor(640,570).name(),'#0000ff')
            o['x']=800;d=r.frame(p,tmp,1,1280,720);self.assertNotEqual(c,d)

    def test_vector_crop_and_cover_never_rasterize(self):
        from studio.explainer import image_item
        p=new_project(duration=4);p['scenes'][0].update(background='white',objects=[image_item(asset('map'),640,350,400,200)])
        o=p['scenes'][0]['objects'][0];o.update(crop=[.1,.1,.8,.8],fit='cover')
        r=Renderer();a=r.frame(p,'.',1,3840,2160)
        self.assertFalse(a.isNull());self.assertFalse(r.cache);self.assertTrue(r.vectors)

    def test_contacts_are_solved_in_world_space_after_parent_transform(self):
        parent=new_object('group',x=100,y=50);parent.update(rotation=10,scale=1.2)
        o=presenter(400,550,1.5,'rest');o['parent']=parent['id'];js,_=evaluate_scene([parent,o],0)[o['id']]
        shoulder=js['shoulder_r'];target=(shoulder[0]+45,shoulder[1]+25)
        o['contacts']=[dict(hand='r',start=0,end=4,x=target[0],y=target[1],blend=0,release=0)]
        actual=evaluate_scene([parent,o],1)[o['id']][0]['hand_r']
        self.assertLess(math.dist(actual,target),.001)

    def test_character_pivot_matches_transform_for_every_joint(self):
        o=presenter(400,550,1.5,'point');base=skeleton(o,1)[0]
        o['pivot']=[12,-45];o['rotation']=27
        actual,st=skeleton(o,1)
        for key,point in base.items():
            local=((point[0]-400)/1.5,(point[1]-550)/1.5)
            self.assertLess(math.dist(actual[key],transform_point(local,st)),.001)


if __name__=='__main__':unittest.main()
