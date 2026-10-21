"""An honest static style comparison, rendered in Studio using the unmodified reference file."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
DEST=Path(__file__).resolve().parents[1];ART=DEST/'art'
from PySide6.QtWidgets import QApplication
from studio.project import new_project,save
from studio.explainer import image_item,text_item,item
from studio.renderer import Renderer
from studio.directing import preflight


def image(scene,file,x,y,w,h,layer=10,**extra):
    o=image_item(str(file),x,y,w,h);o.update(layer=layer,end=5,**extra);scene['objects'].append(o);return o


def text(scene,value,x,y,w,h,size=24,**extra):
    o=text_item(value,x,y,w,h,size,font='Segoe UI',**extra);o.update(layer=60,end=5);scene['objects'].append(o)


def base(name):
    p=new_project(name,5,1920,1080);s=p['scenes'][0];s.update(background='white',objects=[],effects=[]);p['subtitle_style']['enabled']=False;return p,s


def prepare():
    app=QApplication.instance() or QApplication([])
    original=ART/'presenter_master.png';digest=hashlib.sha256(original.read_bytes()).hexdigest()
    assert digest=='85b814d6ad7e6d6e3076b80cf136469b98a2733ab02ef1c00964188b86217c15'
    p,s=base('Đối chiếu nhân vật gốc và cảnh cùng nét vẽ')
    image(s,ART/'village_flat_ink.png',640,360,1280,720,0)
    # White space is part of this background design. The presenter remains an
    # intact raster layer; only position, uniform size and a right-edge crop vary.
    image(s,original,240,433,441.37,480,30,crop=[0,0,.98,.99])
    assert not preflight(p,DEST)
    saved=save(p,DEST/'preview_project.json',DEST)
    r=Renderer();r.frame(saved,DEST,1,1920,1080).save(str(DEST/'scene_preview.png'))
    board,s=base('Khóa mẫu nhân vật và chuẩn nét vẽ chung')
    text(s,'GIỮ NHÂN VẬT GỐC · THIẾT KẾ CẢNH THEO CÙNG NÉT',640,55,1180,70,29,bold=True)
    text(s,'ẢNH MẪU NGƯỜI DÙNG',220,135,380,55,23,bold=True)
    image(s,original,220,390,334,360,20,crop=[0,0,.98,.99])
    text(s,'Giữ nguyên tệp · không vẽ lại người dẫn',220,613,380,60,18,color='#575757')
    image(s,DEST/'scene_preview.png',850,383,800,450,10)
    text(s,'CẢNH THỬ CÙNG NGÔN NGỮ HÌNH ẢNH',850,135,790,55,23,bold=True)
    text(s,'Nét mực mềm · Màu nhẹ · Ít chi tiết · Nền sáng',850,637,790,60,21,color='#575757')
    r.frame(board,DEST,1,1920,1080).save(str(DEST/'style_comparison.png'))
    report=dict(reference_file='art/presenter_master.png',sha256=digest,reference_dimensions=[392,422],reference_status='Original bytes preserved',preview_presenter_status='Original raster layer; no redraw',preview_transforms='Uniform resize, position and crop of right/bottom image borders; character contours preserved',rig_status='New animation rig not implemented or approved',supporting_people_status='Generated as part of the style proposal; not production rigs',palette_samples=dict(shirt='#232323',pants='#7197ce',skin='#fde7c9',shoes='#fdfdfd'),preview_project_preflight='PASS',art_direction_approval='Pending user review')
    (DEST/'reference_manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=True,indent=2))


if __name__=='__main__':prepare()
