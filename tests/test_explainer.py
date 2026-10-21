import copy,json,math,tempfile,unittest,wave
from pathlib import Path
from unittest.mock import patch
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QPoint,Qt
from PySide6.QtTest import QTest
from studio.explainer import compile_board,build_scene,script_cues,suggest_board,apply_pose,presenter,LAYOUTS
from studio.project import save,load,missing,pack,unpack,resequence,new_object
from studio.renderer import Renderer
from studio import animation as a

APP=QApplication.instance() or QApplication([])

class ExplainerTests(unittest.TestCase):
    def board(self):
        return dict(version=1,rows=[dict(start=0,end=3,title='Dấu vết lịch sử',text='Tìm kiếm và đối chiếu.',layout='presenter',labels=['Hiện vật'])])
    def test_script_estimate_is_explicit_and_srt_keeps_timestamps(self):
        cues,mode=script_cues('Một câu.\n\nMột câu dài hơn.',9)
        self.assertEqual(mode,'estimated');self.assertEqual(cues[-1]['end'],9)
        cues,mode=script_cues('1\n00:00:01,125 --> 00:00:02,700\nMột câu.',5)
        self.assertEqual((mode,cues[0]['start'],cues[0]['end']),('srt',1.125,2.7))
    def test_all_layouts_render_with_white_background_and_editable_objects(self):
        renderer=Renderer()
        for layout in LAYOUTS:
            board=self.board();board['rows'][0]['layout']=layout
            if layout=='custom':board['rows'][0]['objects']=[dict(kind='shape',shape='ellipse',x=640,y=360,width=100,height=100)]
            p=compile_board(board);im=renderer.frame(p,'.',1,640,360)
            self.assertEqual(im.pixelColor(0,0).name(),'#ffffff')
            self.assertTrue(any(o['kind']=='text' for o in p['scenes'][0]['objects']))
            self.assertGreater(len(p['scenes'][0]['objects']),1)
    def test_portable_assets_include_storyboard_and_reopen_after_pack(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as tmp:
            root=Path(tmp);asset=root/'book.svg';asset.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="200" height="100"><rect width="200" height="100" fill="red"/></svg>')
            voice=root/'voice.wav'
            with wave.open(str(voice),'wb') as wav:wav.setnchannels(1);wav.setsampwidth(2);wav.setframerate(48000);wav.writeframes(b'\0\0'*144000)
            board=self.board();board.update(voice=str(voice));board['rows'][0]['assets']=[str(asset)]
            project=save(compile_board(board),root/'saved'/'project.json',root)
            self.assertFalse(missing(project,root/'saved'))
            self.assertFalse(Path(project['storyboard']['voice']).is_absolute())
            pack(project,root/'saved',root/'portable.zip');path=unpack(root/'portable.zip',root/'unpacked')
            self.assertFalse(missing(load(path),path.parent))
            self.assertFalse(Renderer().frame(load(path),path.parent,1,640,360).isNull())
    def test_scene_reorder_moves_narration_and_subtitles_together(self):
        board=self.board();board['rows'].append(dict(start=3,end=5,title='Kết luận',text='Câu sau.'))
        p=compile_board(board);first,second=p['scenes'];p['audio']=[dict(id='voice',scene_id=second['id'],start=3,trim=3,duration=2)]
        p['scenes']=[second,first];resequence(p)
        self.assertEqual(p['audio'][0]['start'],0);self.assertEqual(p['audio'][0]['trim'],3)
        self.assertEqual(p['subtitles'][1]['start'],0);self.assertEqual(p['subtitles'][0]['start'],2)
    def test_invalid_times_and_missing_assets_are_rejected(self):
        for bad in (float('nan'),-1,2):
            board=self.board();board['rows'][0]['start']=bad
            with self.assertRaises(ValueError):compile_board(board)
        board=self.board();board['rows'][0]['assets']=['no_such_file.png']
        with self.assertRaises(FileNotFoundError):compile_board(board)
    def test_jump_is_continuous_inside_clip_and_zero_blend_contact_starts_at_target(self):
        obj=new_object();obj['action']='jump'
        left=a.skeleton(obj,1.35-1e-6)[0];right=a.skeleton(obj,1.35+1e-6)[0]
        self.assertLess(max(math.dist(left[k],right[k]) for k in left),.01)
        obj=new_object();obj['contacts']=[dict(hand='r',start=0,end=2,blend=0,release=0,x=675,y=420)]
        start=a.evaluate_scene([obj],0)[obj['id']][0]['hand_r'];after=a.evaluate_scene([obj],1e-6)[obj['id']][0]['hand_r']
        self.assertLess(math.dist(start,after),.001)
    def test_pose_transition_does_not_rewrite_earlier_pose(self):
        obj=presenter(pose='point');before=a.skeleton(obj,2)
        apply_pose(obj,'question',4,.7)
        self.assertEqual(a.skeleton(obj,2),before)
        left=a.skeleton(obj,4-1e-6)[0];right=a.skeleton(obj,4+1e-6)[0]
        self.assertLess(max(math.dist(left[k],right[k]) for k in left),.01)
    def test_pose_uses_shortest_rotation_instead_of_spinning_forearm(self):
        obj=presenter(pose='think');apply_pose(obj,'explain',4,1)
        frames=obj['keys']['bone_fore_r'];delta=frames[-1]['v']-frames[-2]['v']
        self.assertLess(abs(delta),math.pi)
        self.assertEqual(a.stepped(obj['expressions'],2,'happy'),'worried')
        self.assertEqual(a.stepped(obj['expressions'],5,'worried'),'happy')
    def test_image_contain_keeps_aspect_and_cover_fills(self):
        from PySide6.QtGui import QImage,QColor
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as tmp:
            path=Path(tmp)/'red.png';im=QImage(200,100,QImage.Format.Format_RGB32);im.fill(QColor('red'));im.save(str(path))
            board=self.board();board['rows'][0]['assets']=[str(path)];p=compile_board(board)
            obj=next(o for o in p['scenes'][0]['objects'] if o['kind']=='image');obj.update(x=640,y=360,width=200,height=200)
            r=Renderer();im=r.frame(p,tmp,1,1280,720)
            self.assertEqual(im.pixelColor(640,280).name(),'#ffffff');self.assertEqual(im.pixelColor(640,360).name(),'#ff0000')
            obj['fit']='cover';im=r.frame(p,tmp,1,1280,720);self.assertEqual(im.pixelColor(640,280).name(),'#ff0000')
    def test_storyboard_widget_roundtrip_compiles_all_scenes(self):
        from studio.ui.explainer_dialogs import StoryboardDialog
        d=StoryboardDialog();d.board=self.board();d.populate();d.table.item(0,2).setText('Chữ đã sửa')
        d.commit();self.assertIsNotNone(d.result_project);self.assertEqual(d.result_project['scenes'][0]['name'],'Chữ đã sửa');d.close()
    def test_custom_layers_camera_and_cue_times_survive_storyboard_editor(self):
        from studio.ui.explainer_dialogs import StoryboardDialog
        board=self.board();row=board['rows'][0]
        row.update(layout='custom',camera={'zoom':1.1},cue_start=.1,cue_end=2.8,
                   objects=[dict(kind='shape',shape='path',points=[[0,0],[120,40]],x=500,y=400,start=.3,end=2)])
        d=StoryboardDialog();d.board=board;d.populate();result=d.data();d.close()
        self.assertEqual(result['rows'][0]['objects'],row['objects']);self.assertEqual(result['rows'][0]['cue_start'],.1)
        scene=compile_board(result)['scenes'][0];self.assertEqual(scene['camera']['zoom'],1.1)
        custom=scene['objects'][-1];self.assertEqual((custom['start'],custom['end']),(.3,2))

if __name__=='__main__':unittest.main()
