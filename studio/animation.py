"""Pure deterministic skeleton engine. Coordinates use a 1280 x 720 design space."""
import math

ACTIONS = ['idle', 'walk', 'run', 'jump', 'sit', 'stand_up', 'bend_down', 'wave', 'point',
           'look', 'turn', 'cry', 'laugh', 'hug', 'reach', 'hold', 'pick_up', 'give', 'receive', 'umbrella_walk']
LABELS = ['Đứng / thở', 'Đi bộ', 'Chạy', 'Nhảy', 'Ngồi', 'Đứng lên', 'Cúi xuống', 'Vẫy tay',
          'Chỉ tay', 'Nhìn trái / phải', 'Xoay người', 'Khóc', 'Cười', 'Ôm', 'Vươn tay', 'Cầm đồ',
          'Nhặt đồ', 'Đưa đồ', 'Nhận đồ', 'Đi bộ cầm ô']
EXPRESSIONS = ['normal', 'happy', 'sad', 'angry', 'surprised', 'worried', 'curious', 'confident']
ENGINE_VERSION = 'ink-voice-performance-4.5'
PARENTS = {'neck':'hip', 'head':'neck', 'shoulder_l':'neck', 'shoulder_r':'neck',
           'elbow_l':'shoulder_l', 'hand_l':'elbow_l',
           'elbow_r':'shoulder_r', 'hand_r':'elbow_r', 'knee_l':'hip', 'foot_l':'knee_l',
           'knee_r':'hip', 'foot_r':'knee_r', 'toe_l':'foot_l', 'toe_r':'foot_r'}

def ease(u, mode='linear', bezier=None):
    u = min(1., max(0., u))
    if mode == 'ease_in': return u*u
    if mode == 'ease_out': return 1-(1-u)**2
    if mode == 'ease_in_out': return u*u*(3-2*u)
    if mode == 'hold': return 0. if u<1 else 1.
    if mode == 'bezier':
        x1, y1, x2, y2 = bezier or (.25, .1, .25, 1.)
        def curve(v, a, b): return 3*(1-v)**2*v*a + 3*(1-v)*v*v*b + v**3
        lo, hi = 0., 1.
        for _ in range(24):
            mid = (lo+hi)/2
            if curve(mid, x1, x2) < u: lo = mid
            else: hi = mid
        return curve((lo+hi)/2, y1, y2)
    return u

def sample(keys, t, default):
    keys = sorted(keys, key=lambda k: k['t'])
    if not keys: return default
    if t <= keys[0]['t']: return keys[0]['v']
    for a, b in zip(keys, keys[1:]):
        if t <= b['t']:
            u = ease((t-a['t']) / max(1e-8, b['t']-a['t']), b.get('ease', 'linear'), b.get('bezier'))
            return a['v'] + (b['v']-a['v'])*u
    return keys[-1]['v']

def ik(a, target, l1, l2, bend=1):
    dx, dy = target[0]-a[0], target[1]-a[1]
    d = min(l1+l2-.0001, max(abs(l1-l2)+.0001, math.hypot(dx, dy)))
    base = math.atan2(dy, dx)
    offset = math.acos(min(1., max(-1., (l1*l1+d*d-l2*l2)/(2*l1*d))))
    angle = base + bend*offset
    joint = (a[0]+l1*math.cos(angle), a[1]+l1*math.sin(angle))
    endpoint = (a[0]+d*math.cos(base), a[1]+d*math.sin(base))
    return joint, endpoint

def fk(parent, length, angle):
    return (parent[0]+length*math.sin(angle), parent[1]+length*math.cos(angle))


PROPORTIONS = {
    'child': (58, 30, 29, 37, 36, 10),
    'teen': (75, 39, 37, 49, 47, 13),
    'adult': (82, 43, 41, 53, 53, 14),
    'elderly': (78, 43, 41, 51, 51, 14),
}

def age_at(obj,t=0):
    return stepped(obj.get('ages',[]),t,obj.get('age','adult'))

def dimensions(obj,t=0):
    values = PROPORTIONS.get(age_at(obj,t), PROPORTIONS['adult'])
    return tuple(obj.get('rig', {}).get(k, v) for k, v in zip(
        ('torso','upper_arm','forearm','thigh','shin','shoulder'), values))

def active_motion(obj, t):
    for clip in sorted(obj.get('motions', []), key=lambda c:c['start']):
        if clip['start'] <= t < clip['end']:
            return clip['action'], t-clip['start'], clip
    return obj.get('action','idle'), t, {}

def stepped(keys, t, default):
    for key in sorted(keys, key=lambda k:k['t']):
        if key['t'] > t: break
        default = key['v']
    return default

def pose(action, time, speed=1., amp=1.):
    t = time*speed
    c = math.sin(t*math.tau*1.05)
    p = dict(torso=0., arm_l=-.16, fore_l=-.1, arm_r=.16, fore_r=.1,
             thigh_l=-.12, shin_l=0., thigh_r=.12, shin_r=0., lift=0., head=0.)
    if action in ('walk','run','umbrella_walk'):
        p.update(arm_l=-c*.4*amp, fore_l=-c*.3-.12, arm_r=c*.4*amp, fore_r=c*.3+.12,
                 torso=.16 if action=='run' else .025*c)
    elif action=='jump':
        # One jump, including crouch and landing. Looping is explicit on the clip.
        lift = sample([{'t':0,'v':0},{'t':.3,'v':-14,'ease':'ease_in_out'},
            {'t':.5,'v':0},{'t':.9,'v':80,'ease':'ease_out'},
            {'t':1.35,'v':0,'ease':'ease_in'},{'t':1.5,'v':-12},
            {'t':1.85,'v':0,'ease':'ease_in_out'}],t,0)
        reach=ease(t/.45,'ease_in_out')*(1-ease((t-1.1)/.75,'ease_in_out'))
        p.update(lift=lift,arm_l=-.16-.64*reach,arm_r=.16+.74*reach,
                 fore_l=-.1-1.1*reach,fore_r=.1+reach)
    elif action in ('sit','stand_up'):
        f=1 if action=='sit' else 1-ease(t/1.8,'ease_in_out')
        p.update(lift=-48*f,thigh_l=-1.35*f,thigh_r=1.35*f)
    elif action in ('bend_down','pick_up'):
        f=1 if action=='bend_down' else math.sin(math.pi*min(1,t/2.4))
        p.update(torso=.65*f,arm_r=-.35*f,fore_r=-.4*f,lift=-20*f)
    elif action=='wave': p.update(arm_r=2.1,fore_r=2.5+.4*math.sin(t*7))
    elif action=='point': p.update(arm_r=1.35,fore_r=1.5,head=.2)
    elif action=='reach':
        f=ease(t/.7,'ease_in_out');p.update(arm_r=.16+.7*f,fore_r=.1+1.35*f,torso=.08*f)
    elif action=='give':
        f=ease(t/.9,'ease_in_out');p.update(arm_r=.35+.5*f,fore_r=1.1+.45*f,torso=.05*f)
    elif action=='receive':
        f=ease(t/.8,'ease_in_out');p.update(arm_r=.2+.9*f,fore_r=.1+1.6*f)
    elif action=='hold': p.update(arm_r=.65,fore_r=2.35)
    elif action=='look': p['head']=.35*math.sin(t*1.6)
    elif action=='turn': p['head']=.5*ease(t/1.2,'ease_in_out')
    elif action=='cry': p.update(torso=.12,arm_l=-2.4,fore_l=-2.8,arm_r=2.4,fore_r=2.8,head=-.2)
    elif action=='laugh': p.update(torso=.045*math.sin(t*6),arm_r=.5,fore_r=-1.2)
    elif action=='hug':
        p.update(arm_l=-.2,fore_l=.1,arm_r=.2,fore_r=-.1)
    if action=='umbrella_walk': p.update(arm_r=.65,fore_r=2.35)
    return p

def motion_pose(obj, t):
    action,local,current=active_motion(obj,t)
    if current.get('loop') and action=='jump':local%=current.get('period',2.5)
    args=(obj.get('speed',1.),obj.get('amplitude',1.))
    def build(name,local_time,world_time):
        if name in ('walk','run','umbrella_walk') and obj.get('keys',{}).get('x'):
            _,_,_,thigh,shin,_=dimensions(obj,world_time);st=state(obj,world_time)
            stride=stride_length(obj,thigh,shin)*st['scale']
            local_time=(st['x']-obj['keys']['x'][0]['v'])/stride/1.05
            result=pose(name,local_time,1,obj.get('amplitude',1))
        else:result=pose(name,local_time,*args)
        if obj.get('character_design')=='reference_black' and name in ('walk','umbrella_walk'):
            # The reference is a front/three-quarter drawing. Keep the hands
            # outside the torso rather than swinging both arms through it.
            c=math.sin(local_time*math.tau*1.05)
            result.update(arm_l=-.30+.12*c,fore_l=-.15+.10*c,
                          arm_r=.30+.12*c,fore_r=.15+.10*c,torso=.012*c)
            if name=='umbrella_walk':result.update(arm_r=.65,fore_r=2.35)
        return result
    result=build(action,local,t)
    previous=next((c for c in reversed(sorted(obj.get('motions',[]),key=lambda c:c['end']))
                   if c['end']<=t),None)
    blend=current.get('blend',.25)
    if current and blend and local<blend:
        adjacent=previous and abs(previous['end']-current['start'])<.001
        before=build(previous['action'],previous['end']-previous['start'],previous['end']) if adjacent else build(obj.get('action','idle'),t,t)
        u=ease(local/blend,'ease_in_out');result={k:before[k]+(v-before[k])*u for k,v in result.items()}
    elif not current and previous and 0<=t-previous['end']<.25:
        before=build(previous['action'],previous['end']-previous['start'],previous['end'])
        u=ease((t-previous['end'])/.25,'ease_in_out');result={k:before[k]+(v-before[k])*u for k,v in result.items()}
    return result

def state(obj, t):
    values={k:sample(obj.get('keys',{}).get(k,[]),t,obj.get(k,d)) for k,d in
            [('x',640.),('y',575.),('scale',1.),('rotation',0.),('opacity',1.),('facing',1.)]}
    values['visible']=obj.get('start',0)<=t<obj.get('end',1e10)
    values['pivot']=obj.get('pivot',[0,0])
    return values

def local_to_world(point, st):
    pivot=st.get('pivot',[0,0])
    rad=math.radians(st['rotation']);x=(point[0]-pivot[0])*st['scale'];y=(point[1]-pivot[1])*st['scale']
    return st['x']+x*math.cos(rad)-y*math.sin(rad),st['y']+x*math.sin(rad)+y*math.cos(rad)

def stride_length(obj,thigh,shin):
    return max(.001,obj.get('stride',(thigh+shin)*(.52 if obj.get('character_design')=='reference_black' else .8)))


def gait(obj,t,side):
    """Distance-driven stance anchors. Pure evaluation permits arbitrary seeking."""
    _,_,_,thigh,shin,_=dimensions(obj,t);st=state(obj,t)
    reference=obj.get('character_design')=='reference_black'
    stride=stride_length(obj,thigh,shin)*st['scale']
    keys=sorted(obj.get('keys',{}).get('x',[]),key=lambda k:k['t'])
    origin=keys[0]['v'] if keys else st['x']
    # Find the current monotonic leg of a path, also supporting a return journey.
    direction=1 if st.get('facing',1)>=0 else -1
    for i,(a,b) in enumerate(zip(keys,keys[1:])):
        if a['t']<=t and a['v']!=b['v']:
            if i==0 or (keys[i]['v']-keys[i-1]['v'])*(b['v']-a['v'])<=0: origin=a['v']
            direction=1 if b['v']>a['v'] else -1
            if t<=b['t']:break
    moved=abs(st['x']-origin)
    offset=0 if side=='l' else .5
    moving=bool(keys and any(k['v']!=keys[0]['v'] for k in keys))
    distance=moved if moving else t*stride*obj.get('speed',1)*.85
    cycle=distance/stride+offset;index=math.floor(cycle);phase=cycle-index
    anchor=origin+direction*(index-offset+.3)*stride
    if phase<.6:
        x=anchor;lift=0.;stance=True
    else:
        u=(phase-.6)/.4
        x=anchor+direction*stride*ease(u,'ease_in_out')
        height=(thigh+shin)*(.11 if reference else .17) if reference else 18
        if active_motion(obj,t)[0]=='run':height=(thigh+shin)*.25 if reference else 30
        lift=math.sin(math.pi*u)**2*height*st['scale']
        stance=False
    if not moving:
        x=st['x']+(x-origin-direction*distance)
    if reference:x+=(-12 if side=='l' else 12)*st['scale']
    anchor=local_to_world((0,0),st)
    return (x+anchor[0]-st['x'],anchor[1]-lift),stance

def skeleton(obj,t):
    p=motion_pose(obj,t);keys=obj.get('keys',{})
    for k in p:p[k]=sample(keys.get('bone_'+k,[]),t,p[k])
    torso,upper,fore,thigh,shin,shoulder=dimensions(obj,t)
    st=state(obj,t);action,local,_=active_motion(obj,t)
    facing=1 if st['facing']>=0 else -1
    if age_at(obj,t)=='elderly':p['torso']+=.14
    walking=action in ('walk','run','umbrella_walk')
    weight=1. if walking else 0.
    clip=active_motion(obj,t)[2]
    if walking and clip and clip.get('blend',.25)>0:
        duration=clip.get('blend',.25)
        weight=ease(min(1,local/duration,(clip['end']-t)/duration),'ease_in_out')
    # Leave room for reachable stride endpoints and bent knees at contact.
    reference=obj.get('character_design')=='reference_black'
    hip=(0.,-(thigh+shin)*(.99-(.02 if reference else .025)*weight)-p['lift'])
    if walking:
        stride=stride_length(obj,thigh,shin)*st['scale']
        path=keys.get('x',[]);distance=abs(st['x']-path[0]['v']) if path else t*stride*obj.get('speed',1)*.85
        phase=distance/max(.001,stride)
        hip=(hip[0],hip[1]+(.35 if reference else 3)*weight*math.sin(math.tau*phase)**2)
    neck=(hip[0]+torso*math.sin(p['torso'])*facing,hip[1]-torso*math.cos(p['torso']))
    breath=obj.get('breath',.5)*math.sin(t*2.1)
    neck=(neck[0],neck[1]+breath)
    joints=dict(hip=hip,neck=neck,head=(neck[0]+6*math.sin(p['head']),neck[1]-(33 if obj.get('skin')=='ink' else 27)))
    for side in ('l','r'):
        sign=-1 if side=='l' else 1
        sh=(neck[0]+sign*shoulder,neck[1]+6)
        elbow=fk(sh,upper,p['arm_'+side]);hand=fk(elbow,fore,p['fore_'+side])
        knee=fk(hip,thigh,p['thigh_'+side]);foot=fk(knee,shin,p['shin_'+side])
        # Manual bone overrides remain available for posed legs.
        posed_leg=any('bone_'+name+'_'+side in keys for name in ('thigh','shin'))
        if action not in ('sit','stand_up') and not posed_leg:
            lift=max(0,p['lift']) if action=='jump' else 0
            foot=(sign*obj.get('stance',14),-lift)
            leg_root=(hip[0]+sign*10,hip[1]) if reference else hip
            knee,foot=ik(leg_root,foot,thigh,shin,-sign if not reference and obj.get('skin') in ('illustrated','ink') else -facing)
        target=obj.get('rig',{}).get('hand_'+side)
        tx,ty=keys.get('hand_'+side+'_x',[]),keys.get('hand_'+side+'_y',[])
        if tx or ty:
            base=target or hand;target=(sample(tx,t,base[0]),sample(ty,t,base[1]))
        if target:elbow,hand=ik(sh,target,upper,fore,obj.get('rig',{}).get('bend_'+side,sign))
        joints.update({f'shoulder_{side}':sh,f'elbow_{side}':elbow,f'hand_{side}':hand,
                       f'knee_{side}':knee,f'foot_{side}':foot,f'toe_{side}':(foot[0]+14*facing,foot[1])})
    joints={k:local_to_world(v,st) for k,v in joints.items()}
    if walking:
        for side in ('l','r'):
            foot,_=gait(obj,t,side)
            rest=joints['foot_'+side]
            foot=tuple(a+(b-a)*weight for a,b in zip(rest,foot))
            leg_root=local_to_world((hip[0]+(-10 if side=='l' else 10),hip[1]),st) if reference else joints['hip']
            knee,foot=ik(leg_root,foot,thigh*st['scale'],shin*st['scale'],-facing)
            joints['knee_'+side]=knee;joints['foot_'+side]=foot
            joints['toe_'+side]=(foot[0]+14*facing*st['scale'],foot[1])
    return joints,st

def evaluate_scene(objects,t):
    """Resolve contacts from a shared immutable base pose, never recursive IK."""
    poses={o['id']:skeleton(o,t) for o in objects if o['kind']=='character'}
    from .hierarchy import world_states,transform_point
    world=world_states(objects,t)
    for obj in objects:
        if obj['kind']=='character' and obj.get('parent'):
            js,_=poses[obj['id']];ps=world[obj['parent']]
            poses[obj['id']]=({k:transform_point(v,ps) for k,v in js.items()},world[obj['id']])
    base={i:dict(js) for i,(js,_) in poses.items()}
    for obj in objects:
        if obj['id'] not in poses:continue
        joints,st=poses[obj['id']];_,upper,fore,_,_,_=dimensions(obj,t)
        for contact in obj.get('contacts',[]):
            start,end=contact.get('start',0),contact.get('end',obj.get('end',15))
            if not start<=t<end:continue
            side=contact.get('hand','r');key='hand_'+side
            if contact.get('target'):
                if contact['target'] not in poses or not poses[contact['target']][1]['visible']:continue
                target=base.get(contact['target'],{}).get(contact.get('joint','hand_l'))
                if target is None:continue
            else:
                target=(sample(contact.get('keys',{}).get('x',[]),t,contact.get('x',st['x'])),
                        sample(contact.get('keys',{}).get('y',[]),t,contact.get('y',st['y']-140)))
            ox,oy=contact.get('offset',[0,0]);target=(target[0]+ox,target[1]+oy)
            blend=contact.get('blend',.3);release=contact.get('release',.3)
            weight=min(1,(t-start)/blend if blend>0 else 1,(end-t)/release if release>0 else 1)
            weight=ease(weight,'ease_in_out')
            elbow,hand=ik(joints['shoulder_'+side],target,upper*st['scale'],fore*st['scale'],contact.get('bend',-1 if side=='l' else 1))
            if weight<1:
                # Blend angles, not IK branch choice. This also preserves bone lengths.
                shoulder=joints['shoulder_'+side];old_elbow=joints['elbow_'+side];old_hand=joints[key]
                def angle(a,b):return math.atan2(b[1]-a[1],b[0]-a[0])
                def blend_angle(a,b):return a+((b-a+math.pi)%math.tau-math.pi)*weight
                ua=blend_angle(angle(shoulder,old_elbow),angle(shoulder,elbow))
                fa=blend_angle(angle(old_elbow,old_hand),angle(elbow,hand))
                elbow=(shoulder[0]+upper*st['scale']*math.cos(ua),shoulder[1]+upper*st['scale']*math.sin(ua))
                hand=(elbow[0]+fore*st['scale']*math.cos(fa),elbow[1]+fore*st['scale']*math.sin(fa))
            joints['elbow_'+side]=elbow;joints[key]=hand
    return poses

def attachment(obj,objects,t,poses=None):
    keys=sorted(obj.get('attachment',[]),key=lambda k:k['t']);match=None
    for k in keys:
        if k['t']<=t:match=k
    if not match or not match.get('character'):return None
    parent=next((o for o in objects if o['id']==match['character']),None)
    if not parent:return None
    poses=poses if poses is not None else evaluate_scene(objects,t)
    joints,st=poses[parent['id']]
    if not st['visible']:return None
    point=joints.get(match.get('joint','hand_r'))
    if point is None:return None
    off=match.get('offset',[0,0]);return point[0]+off[0],point[1]+off[1]

def camera_values(scene,t):
    camera=scene.get('camera',{});ck=camera.get('keys',{})
    for shot in camera.get('shots',[]):
        if shot['start']<=t<shot['end']:
            ck=shot.get('keys',{});camera={**camera,**shot};break
    z=max(.1,sample(ck.get('zoom',[]),t,camera.get('zoom',1)))
    x=sample(ck.get('x',[]),t,camera.get('x',640));y=sample(ck.get('y',[]),t,camera.get('y',360))
    follow=next((o for o in scene['objects'] if o['id']==camera.get('follow')),None)
    if follow:x=state(follow,t)['x']+camera.get('offset_x',0)
    return z,x,y
