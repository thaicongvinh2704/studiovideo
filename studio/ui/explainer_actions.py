import copy
from pathlib import Path
from PySide6.QtWidgets import QFileDialog,QInputDialog,QDialog
from ..project import uid,save,new_object,resolve
from ..explainer import presenter,text_item,item,POSES,apply_pose,image_item,LAYOUTS,build_scene
from .dialogs import error
from .explainer_dialogs import StoryboardDialog,GraphicDialog
from .workers import Worker
from ..animation import state

class ExplainerActions:
    def drawing_desk(self, checked=False, obj=None):
        from .drawing_dialog import DrawingDialog
        from ..drawing import scene_layers
        self.pause()
        dialog=DrawingDialog(obj.get('drawing_doc') if obj else None,self)
        dialog.protect_unsaved=True
        if not dialog.exec():return
        try:
            scene=self.current_scene()
            layers=scene_layers(dialog.result_doc,self.root,max(0,self.t-scene['start']),scene['duration'])
            if not layers:return
            self.remember()
            if obj:
                replacement=layers[0]
                for key in ('file','width','height','drawing_doc','name','role'):obj[key]=replacement[key]
                # Timing, transforms, parenting and authored motion remain on this object.
                self.selected_id=obj['id']
                if len(layers)>1:scene['objects'].extend(layers[1:])
            else:
                top=max((o.get('layer',0) for o in scene['objects']),default=19)+1
                for i,entry in enumerate(layers):entry['layer']=top+i
                scene['objects'].extend(layers);self.selected_id=layers[-1]['id']
            self.changed()
            self.statusBar().showMessage(f'Đã đưa {len(layers)} lớp vector vào cảnh. Chọn lớp → Sửa nội dung để vẽ tiếp.')
        except Exception as exc:error(self,exc)

    def story_wizard(self):
        self.pause()
        if not self.ensure_save():return
        dialog=StoryboardDialog(self)
        if not dialog.exec():return
        path,_=QFileDialog.getSaveFileName(self,'Lưu video minh họa',str(self.app_root/'projects'/'explainer'/'project.json'),'JSON (*.json)')
        if not path:return
        try:
            p=save(dialog.result_project,path,Path(path).parent)
            self.open_path(path);self.analyze_voice()
        except Exception as exc:error(self,exc)
    def add_graphic(self,kind):
        s=self.current_scene()
        if kind=='presenter':
            from ..drawing import document,scene_layers
            from ..character_art import reviewed_person
            doc=document();doc['layers']=[reviewed_person()]
            try:layers=scene_layers(doc,self.root,max(0,self.t-s['start']),s['duration'])
            except Exception as exc:error(self,exc);return
            self.remember();s['objects'].extend(layers);self.selected_id=layers[0]['id'];self.changed();return
        o=text_item('Nhập nội dung',640,200) if kind=='text' else presenter() if kind=='presenter' else item('shape','Thẻ thông tin',760,350,420,240,shape='card',text='Ý chính',fill='#fff5d8')
        o['end']=s['duration'];o['start']=max(0,self.t-s['start'])
        if kind!='presenter' and not GraphicDialog(o,self).exec():return
        self.remember();s['objects'].append(o);self.selected_id=o['id'];self.changed()
    def graphic_dialog(self):
        o=self.current_object()
        if not o:return
        if o.get('drawing_doc'):self.drawing_desk(obj=o);return
        if o['kind']=='character':self.pose_picker();return
        staged=copy.deepcopy(o)
        if GraphicDialog(staged,self).exec():self.remember();o.update(staged);self.changed()
    def pose_picker(self):
        o=self.current_object()
        if not o or o['kind']!='character':return
        from .ink_dialogs import PosePicker
        dialog=PosePicker(self)
        if not dialog.exec():return
        name=dialog.pose;self.remember()
        apply_pose(o,name,max(0,self.t-self.current_scene()['start']));self.changed()
    def art_picker(self):
        from .ink_dialogs import ArtPicker
        dialog=ArtPicker(self)
        if not dialog.exec():return
        o=image_item(dialog.file,780,350,500,400);o['start']=max(0,self.t-self.current_scene()['start']);o['end']=self.current_scene()['duration']
        self.remember();self.current_scene()['objects'].append(o);self.selected_id=o['id'];self.changed()
    def appearance_picker(self):
        from .ink_dialogs import AppearancePicker
        o=self.current_object()
        if not o or o['kind']!='character':return
        staged=copy.deepcopy(o);d=AppearancePicker(staged,self)
        if d.exec():self.remember();o.update(staged);self.changed()
    def parent_picker(self):
        from .ink_dialogs import ParentPicker
        o=self.current_object()
        if not o:return
        staged=copy.deepcopy(o);d=ParentPicker(staged,self.current_scene(),self.t-self.current_scene()['start'],self.project.get('fps',30),self)
        if d.exec():self.remember();o.update(staged);self.changed()
    def add_layout(self):
        label,ok=QInputDialog.getItem(self,'Thêm bố cục','Mẫu',list(LAYOUTS.values()),0,False)
        if not ok:return
        layout=next(k for k,v in LAYOUTS.items() if v==label);s=self.current_scene()
        data=build_scene(dict(start=0,end=s['duration'],title='Tiêu đề mới',style='ink',layout=layout,labels=['Mốc đầu','Thay đổi','Kết quả']))
        self.remember();s['objects']+=data['objects'];s['background']='white';self.changed()
    def analyze_voice(self):
        if self.project_worker and self.project_worker.isRunning():return
        from ..media import add_waveforms
        snapshot=copy.deepcopy(self.project);root=self.root;target=self.project
        self.statusBar().showMessage('Đang phân tích waveform voice…')
        self.project_worker=Worker(lambda w:add_waveforms(snapshot,root,w.cancel),self)
        def done(result):
            if self.project is not target:return
            byid={a['id']:a for a in result['audio']}
            for a in self.project['audio']:
                if a['id'] in byid and 'waveform' in byid[a['id']]:a.update(waveform=byid[a['id']]['waveform'],waveform_hz=20)
            from ..media import bind_narrator_mouth
            bind_narrator_mouth(self.project)
            self.changed();self.statusBar().showMessage('Waveform và nhịp miệng người dẫn đã sẵn sàng. Dùng SRT / audio để căn mốc chính xác.')
        self.project_worker.done.connect(done);self.project_worker.failed.connect(lambda e:self.statusBar().showMessage(e));self.project_worker.start()
    def duplicate_object(self):
        o=self.current_object()
        if not o:return
        self.remember();clone=copy.deepcopy(o);clone['id']=uid();clone['name']+=' (bản sao)';clone['x']+=30;clone['group']=''
        self.current_scene()['objects'].append(clone);self.selected_id=clone['id'];self.changed()
    def group_dialog(self):
        from PySide6.QtWidgets import QListWidget,QVBoxLayout,QLineEdit,QDialogButtonBox,QAbstractItemView
        d=QDialog(self);d.setWindowTitle('Tạo nhóm cha–con · kéo / xoay / scale');v=QVBoxLayout(d);name=QLineEdit('Nhóm 1');v.addWidget(name)
        box=QListWidget();box.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        for o in self.current_scene()['objects']:box.addItem(o['name'])
        v.addWidget(box);buttons=QDialogButtonBox(QDialogButtonBox.StandardButton.Save|QDialogButtonBox.StandardButton.Cancel);v.addWidget(buttons);buttons.accepted.connect(d.accept);buttons.rejected.connect(d.reject)
        if d.exec():
            selected=[self.current_scene()['objects'][i] for i in range(box.count()) if box.item(i).isSelected()]
            if not selected:return
            parents={o.get('parent','') for o in selected}
            if len(parents)>1:error(self,'Chọn các lớp cùng một lớp cha trước khi tạo nhóm.');return
            if any(o.get('contacts') for o in selected):error(self,'Bỏ contact trước khi đưa nhân vật vào nhóm cha–con.');return
            self.remember()
            t=self.t-self.current_scene()['start'];cx=sum(state(o,t)['x'] for o in selected)/len(selected)
            cy=sum(state(o,t)['y'] for o in selected)/len(selected)
            group=new_object('group',name.text().strip() or 'Nhóm',cx,cy);group.update(parent=parents.pop(),end=self.current_scene()['duration'],layer=0)
            for o in selected:
                o['parent']=group['id'];o['group']=''
                for key,delta in (('x',cx),('y',cy)):
                    o[key]-=delta
                    for frame in o.get('keys',{}).get(key,[]):frame['v']-=delta
            self.current_scene()['objects'].append(group);self.selected_id=group['id']
            self.changed()
    def split_object(self):
        o=self.current_object();t=self.t-self.current_scene()['start']
        if not o or not o['start']<t<o['end']:return
        if o['kind']=='group':error(self,'Cắt cảnh hoặc cắt các lớp con; chưa hỗ trợ cắt riêng lớp cha.');return
        self.remember();after=copy.deepcopy(o);after['id']=uid();after['start']=t;after['enter']='none';after['name']+=' (tiếp)';o['end']=t
        self.current_scene()['objects'].append(after);self.selected_id=after['id'];self.changed()
    def nudge_frame(self,delta):
        self.pause();self.set_time(self.t+delta/self.project.get('fps',30))
