"""Scene-local parent transforms with cycle validation and consistent hit testing."""
import math
from .animation import state


def transform_point(point, st):
    a=math.radians(st['rotation']);c=math.cos(a)*st['scale'];s=math.sin(a)*st['scale']
    pivot=st.get('pivot',[0,0]);x,y=point[0]-pivot[0],point[1]-pivot[1]
    return st['x']+c*x-s*y,st['y']+s*x+c*y


def world_states(objects,t):
    byid={o['id']:o for o in objects};result={};visiting=set()
    def resolve(o):
        if o['id'] in result:return result[o['id']]
        if o['id'] in visiting:raise ValueError('Nhóm cha–con có vòng lặp.')
        visiting.add(o['id']);local=state(o,t);parent=o.get('parent')
        local['pivot']=o.get('pivot',[0,0])
        if not all(math.isfinite(local[k]) for k in ('x','y','scale','rotation','opacity')) or local['scale']<=0:
            raise ValueError('Vị trí / góc / scale của lớp không hợp lệ.')
        if len(local['pivot'])!=2 or not all(math.isfinite(v) for v in local['pivot']):raise ValueError('Điểm xoay phải có hai tọa độ hữu hạn.')
        if parent:
            if parent not in byid:raise ValueError('Không tìm thấy lớp cha: '+parent)
            ps=resolve(byid[parent]);x,y=transform_point((local['x'],local['y']),ps)
            local.update(x=x,y=y,rotation=local['rotation']+ps['rotation'],scale=local['scale']*ps['scale'],
                         opacity=local['opacity']*ps['opacity'],visible=local['visible'] and ps['visible'])
        visiting.remove(o['id']);result[o['id']]=local;return local
    for obj in objects:resolve(obj)
    return result


def to_parent(point,obj,objects,t):
    if not obj.get('parent'):return point
    ps=world_states(objects,t)[obj['parent']];a=-math.radians(ps['rotation'])
    dx,dy=point[0]-ps['x'],point[1]-ps['y'];scale=ps['scale']
    return ((dx*math.cos(a)-dy*math.sin(a))/scale+ps['pivot'][0],
            (dx*math.sin(a)+dy*math.cos(a))/scale+ps['pivot'][1])
