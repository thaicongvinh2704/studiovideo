from .project import new_project, new_scene, new_object, uid, resequence

NARRATION = [
    'Ngày còn nhỏ, tôi luôn đi dưới chiếc ô vàng của cha.',
    'Mưa rơi trên con đường quen thuộc, cha bước chậm theo tôi.',
    'Chiếc ô nghiêng về phía con, còn vai cha thì ướt.',
    'Tôi thích nhảy qua những vũng nước sau cơn mưa.',
    'Cha đưa tay giữ lấy tôi trước mỗi bước nhảy.',
    'Khi ấy, tôi chỉ biết cười, chưa hiểu sự chở che.',
    'Mẹ đứng chờ hai cha con trước cánh cửa nhỏ.',
    'Mẹ lau những giọt nước trên vai áo của cha.',
    'Cha cười và nói rằng con không bị ướt là được.',
    'Thời gian trôi qua, đôi chân tôi dài thêm từng ngày.',
    'Những bước chân nhỏ dần trở thành bước chân vội vã.',
    'Chiếc ô vàng vẫn ở đó, bình lặng cạnh cửa nhà.',
    'Lên tuổi thiếu niên, tôi muốn tự đi con đường của mình.',
    'Tôi lắc đầu khi cha mang ô đến đón.',
    'Cha hạ bàn tay xuống, rồi lặng lẽ nhìn theo.',
    'Chiều hôm ấy, cha đứng một mình giữa tiếng mưa.',
    'Chiếc ô vàng không còn một đứa trẻ đi bên cạnh.',
    'Nhưng cha vẫn giữ thói quen nghiêng ô về phía ấy.',
    'Lớn lên, tôi sống xa nhà, bận rộn với những cuộc hẹn.',
    'Điện thoại reo. Cha hỏi tôi có mang ô theo không.',
    'Tôi đáp vội rằng mình ổn, rồi im lặng thật lâu.',
    'Mẹ gửi cho tôi một bức hình chiếc ô cũ.',
    'Cha vừa sửa lại nan ô, dù màu vàng đã bạc.',
    'Có những điều được giữ lại chỉ vì một người thương.',
    'Tôi gấp công việc lại và đặt vé trở về nhà.',
    'Trong chiếc túi nhỏ, tôi mang theo lời chưa kịp nói.',
    'Con đường cũ hiện ra, cùng một buổi chiều có mưa.',
    'Cha đã già, đứng trước cổng và nhìn ra đầu ngõ.',
    'Bàn tay cầm ô run nhẹ, mái tóc đã bạc nhiều.',
    'Tôi bước đến gần cha, chậm như cha từng bước.',
    'Cha đưa chiếc ô sang. Lần này, tôi nhận lấy.',
    'Tôi nâng ô lên và nghiêng về phía cha.',
    'Mưa chạm vào vai tôi. Cha nhìn tôi và mỉm cười.',
    'Mẹ vẫn đứng chờ trước cánh cửa ngày xưa.',
    'Ba người cùng bước vào nhà, trong một vòng tay ấm.',
    'Chiếc ô vẫn nghiêng. Chỉ có người cầm ô đã đổi.'
]
SCENES = ['Cha dắt con dưới mưa','Bước nhảy qua vũng nước','Mẹ chờ trước cửa',
          'Những năm tháng lớn lên','Con muốn đi một mình','Chiếc ô chờ đợi',
          'Cuộc gọi của cha','Chiếc ô được sửa lại','Đường về nhà',
          'Cha già trước cổng','Lần này, con che cho cha','Gia đình đoàn tụ']

def key(o,prop,a,b,t0=0,t1=15,ease='ease_in_out'):
    o['keys'][prop]=[dict(t=t0,v=a,ease='linear'),dict(t=t1,v=b,ease=ease)]


def keys(obj,prop,points):
    obj['keys'][prop]=[dict(t=t,v=v,ease='ease_in_out') for t,v in points]

def motion(obj,*clips):
    obj['motions']=[dict(start=a,end=b,action=action,blend=.22) for a,b,action in clips]

def hand(obj,side,points):
    keys(obj,'hand_'+side+'_x',[(t,x) for t,x,y in points])
    keys(obj,'hand_'+side+'_y',[(t,y) for t,x,y in points])
    obj.setdefault('front_hands',[]).append(side)

def touch(obj,side,target=None,joint='hand_l',start=0,end=15,x=None,y=None,points=None,blend=.4,release=.4,bend=1,offset=None):
    c=dict(hand=side,joint=joint,start=start,end=end,blend=blend,release=release,bend=bend)
    if target:c.update(target=target['id'],joint=joint)
    else:c.update(x=obj['x'] if x is None else x,y=obj['y']-150 if y is None else y)
    if points:c['keys']={'x':[dict(t=t,v=x,ease='ease_in_out') for t,x,y in points],
                         'y':[dict(t=t,v=y,ease='ease_in_out') for t,x,y in points]}
    if offset:c['offset']=offset
    obj.setdefault('contacts',[]).append(c)

def camera(scene,x,y=415,zoom=1.65,shots=None):
    scene['camera'].update(x=x,y=y,zoom=zoom)
    if shots:scene['camera']['shots']=shots

def shot(start,end,x,y,zoom):
    return dict(start=start,end=end,x=x,y=y,zoom=zoom)

def demo():
    p=new_project('Chiếc Ô Nghiêng Về Phía Con · Bản tối ưu',180,1920,1080)
    p.update(quality_version=2,render_profile='final',encoder_threads=2)
    p['subtitle_style'].update(size=27,y=.955)
    p['scenes']=[]
    for i,name in enumerate(SCENES):
        s=new_scene(f'{i+1:02} · {name}')
        s['background']='home' if i in (2,9,11) else 'room' if i in (6,7) else 'rain' if i in (0,1,5,10) else 'street'
        s['effects']=['rain','ripple'] if i in (0,1,5,9,10) else []
        father=new_object(preset='father',x=500,y=575);son=new_object(preset='son',x=582,y=575)
        mother=new_object(preset='mother',x=850,y=575)
        mother.update(facing=-1,gaze=-3)
        for o,role in [(father,'father'),(son,'son'),(mother,'mother')]:
            o.update(character_id=role,color='#303b34',gaze=2)
        son['age']='child' if i<3 else 'teen' if i<6 else 'adult'
        father['age']='elderly' if i>=9 else 'adult'
        if i in (9,10):father['facing']=-1
        son['expression']='happy' if i<3 or i>=10 else 'normal'
        father['expression']='sad' if i in (4,5) else 'happy'
        umbrella=new_object('prop','umbrella');umbrella.update(layer=20,color='#edc54e',rotation=25)
        umbrella['attachment']=[dict(t=0,character=father['id'],joint='hand_l')]
        hand(father,'l',[(0,25,-155),(15,25,-155)])
        if i==0:
            father['action']='umbrella_walk';son['action']='walk'
            keys(father,'x',[(0,220),(15,1020)]);keys(son,'x',[(0,302),(15,1102)])
            hand(son,'l',[(0,-25,-150),(15,-25,-150)])
            touch(father,'r',son,'hand_l',blend=0,release=0)
            s['objects']=[father,son,umbrella];s['puddles']=[[430,592,120],[790,590,150],[1120,594,100]]
            camera(s,270,420,1.6);s['camera'].update(follow=father['id'],offset_x=50)
            keys(umbrella,'rotation',[(0,17),(5,28),(15,28)]);s['fade']={'in':.7}
        elif i==1:
            father['action']='idle';son['action']='idle'
            motion(son,(0,2.5,'walk'),(2.5,4.5,'jump'),(5.5,8,'walk'),(8,10,'jump'))
            keys(son,'x',[(0,582),(2.5,582),(2.95,582),(3.85,685),(5.5,685),(8,720),(8.45,720),(9.35,810),(15,810)])
            keys(father,'x',[(0,500),(4.5,608),(8,638),(10,728),(15,728)])
            motion(father,(0,2.5,'umbrella_walk'),(2.5,4.5,'reach'),(4.5,8,'umbrella_walk'),(8,10,'reach'))
            hand(son,'l',[(0,-25,-150),(2.6,-25,-150),(3.3,-40,-120),(4.5,-25,-150),(8.2,-25,-150),(8.9,-40,-120),(10,-25,-150)])
            touch(father,'r',son,'hand_l',start=0,end=3,blend=0,release=.35)
            touch(father,'r',son,'hand_l',start=4,end=8.4,blend=.4,release=.35)
            touch(father,'r',son,'hand_l',start=9.7,end=15,blend=.4,release=0)
            s['objects']=[father,son,umbrella];s['puddles']=[[640,589,70],[770,590,65]]
            camera(s,650,420,1.5)
        elif i==2:
            father['x']=600;son['x']=720;mother['x']=820
            motion(mother,(0,4,'walk'),(4,12,'reach'))
            keys(mother,'x',[(0,820),(4,665),(15,665)])
            mother['expression']='happy';father['action']='idle';father['keys']={};father['front_hands']=[]
            hand(mother,'r',[(0,22,-105),(15,22,-105)])
            towel=new_object('prop','towel');towel.update(scale=.55,rotation=-15,layer=20)
            towel['attachment']=[dict(t=0,character=mother['id'],joint='hand_l')]
            # World-space wipe positions at father's right shoulder.
            touch(mother,'l',start=4,end=12,points=[(4,650,420),(5,617,407),(6,624,420),(7,617,407),(8,624,420),(9,617,407),(10,624,420),(11,636,430)],bend=-1)
            s['objects']=[father,son,mother,towel]
            keys(father,'gaze',[(0,0),(4,4),(12,3)]);keys(son,'gaze',[(0,-3),(15,-3)])
            camera(s,660,430,1.7,shots=[shot(0,5,730,420,1.5),shot(5,12,650,382,2.7),shot(12,15,680,430,1.65)])
        elif i==3:
            son['action']='walk';son['age']='child'
            # A continuous walk, with explicit age cuts instead of scaling one body.
            son['ages']=[dict(t=5,v='teen')];s['background']='home'
            keys(son,'x',[(0,330),(15,970)]);s['objects']=[son]
            umbrella['attachment']=[];umbrella.update(x=935,y=575,scale=.6,rotation=8);s['objects'].append(umbrella)
            s['effects']=['leaves'];camera(s,640,420,1.55);s['camera'].update(follow=son['id'],offset_x=45)
        elif i==4:
            son['x']=650;father['x']=535;father['action']='give'
            keys(son,'bone_head',[(0,0),(5.5,0),(6,.4),(6.5,-.4),(7,.4),(7.5,-.3),(8.5,0)])
            son['expressions']=[dict(t=0,v='worried'),dict(t=5,v='angry')]
            motion(son,(0,10,'point'),(10,15,'walk'));keys(son,'x',[(0,650),(10,650),(15,1080)])
            hand(father,'l',[(0,45,-150),(10,45,-150),(13,15,-90),(15,15,-90)])
            keys(father,'gaze',[(0,4),(15,5)]);keys(umbrella,'rotation',[(0,25),(10,25),(13,5),(15,5)])
            s['objects']=[father,son,umbrella];camera(s,630,420,1.65,shots=[shot(0,5,605,415,1.9),shot(5,10,645,400,2.1),shot(10,15,735,425,1.4)])
        elif i==5:
            father['x']=590;father['action']='idle';father['gaze']=4
            keys(umbrella,'rotation',[(0,10),(5,25),(15,25)])
            keys(father,'bone_head',[(0,0),(5,.25),(10,.1),(15,.1)])
            s['objects']=[father,umbrella];s['puddles']=[[700,591,140]]
            camera(s,665,415,1.5);s['camera']['keys']={'zoom':[dict(t=0,v=1.45),dict(t=15,v=1.6,ease='ease_in_out')]}
        elif i in (6,7):
            son['x']=650;son['action']='hold';phone=new_object('prop','phone');phone['layer']=20
            phone['attachment']=[dict(t=0,character=son['id'],joint='hand_r')]
            hand(son,'r',[(0,40,-95),(5,40,-95),(7.5,38,-198),(10,38,-198),(12,42,-150),(15,42,-150)])
            son['expressions']=[dict(t=0,v='normal'),dict(t=8,v='worried'),dict(t=12,v='sad')]
            keys(son,'gaze',[(0,0),(3,4),(10,2),(15,-3)])
            s['objects']=[son,phone];camera(s,650,420,1.8,shots=[shot(0,5,630,425,1.6),shot(5,15,658,400,2.05)])
            if i==7:
                hand(son,'r',[(0,42,-145),(12,42,-145),(15,35,-95)])
                s['insert']=dict(start=1,end=8,kind='photo',title='Mẹ · Tin nhắn',text='Cha vừa sửa lại nan ô. Vẫn chiếc ô ngày con còn nhỏ.')
                son['expressions']=[dict(t=0,v='normal'),dict(t=8,v='sad'),dict(t=12,v='worried')]
        elif i==8:
            son['x']=350;son['action']='idle';bag=new_object('prop','bag');bag['layer']=20
            bag['attachment']=[dict(t=0,character=son['id'],joint='hand_l')]
            hand(son,'l',[(0,-25,-60),(15,-25,-60)])
            motion(son,(4.5,15,'run'));keys(son,'x',[(0,350),(4.5,350),(15,1050)])
            son['expressions']=[dict(t=0,v='worried'),dict(t=5,v='normal')]
            s['objects']=[son,bag];s['effects']=['rain','ripple']
            s['insert']=dict(start=0,end=4.5,kind='ticket',title='Chuyến đi',text='Công việc để lại. Lần này, con trở về.')
            camera(s,600,425,1.6);s['camera'].update(follow=son['id'],offset_x=70)
        elif i==9:
            father['x']=710;father['action']='idle';father['expression']='worried';father['gaze']=-4
            hand(father,'l',[(0,22,-153),(15,22,-153)])
            keys(father,'bone_head',[(0,-.2),(5,.05),(10,-.15),(15,-.1)])
            keys(umbrella,'rotation',[(0,-15),(5,-14),(10,-15),(15,-14)])
            son.update(x=340,start=10,action='walk',expression='worried')
            keys(son,'x',[(10,340),(15,625)]);s['objects']=[father,son,umbrella]
            camera(s,735,420,1.5,shots=[shot(0,5,735,425,1.5),shot(5,10,710,405,1.45),shot(10,15,600,420,1.4)])
        elif i==10:
            father['x']=710;father['gaze']=-4;son['x']=625;son['gaze']=4
            father['action']='idle';son['action']='idle'
            motion(son,(0,5,'receive'),(5,15,'hold'))
            father['keys']={};father['front_hands']=[]
            # Both grips converge at exactly the same reachable point before ownership changes.
            grip=[(0,690,425),(1,690,425),(2.5,672,423),(5,672,423),(7,672,414),(10,672,397),(15,672,397)]
            touch(father,'l',start=0,end=4.5,points=grip,blend=0,release=.5,bend=-1)
            touch(son,'r',start=.3,end=15,points=grip,blend=.7,release=0,bend=1)
            umbrella['attachment']=[dict(t=0,character=father['id'],joint='hand_l'),dict(t=3.2,character=son['id'],joint='hand_r')]
            keys(umbrella,'rotation',[(0,-15),(5,-15),(10,18),(15,18)])
            father['expressions']=[dict(t=0,v='worried'),dict(t=10,v='happy')]
            son['expressions']=[dict(t=0,v='worried'),dict(t=7,v='happy')]
            s['objects']=[father,son,umbrella];s['puddles']=[[790,592,140]]
            camera(s,660,420,1.6,shots=[shot(0,5,674,405,2.7),shot(5,15,665,405,1.5)])
        else:
            father['x']=620;son['x']=790;mother['x']=960
            father['keys']={};father['front_hands']=[]
            keys(son,'x',[(0,790),(3.5,675),(9,675),(15,850)])
            keys(mother,'x',[(0,960),(4,725),(9,725),(15,905)])
            keys(father,'x',[(0,620),(9,620),(15,790)])
            for o in (father,son,mother):
                o['expression']='happy';o['action']='idle';motion(o,(0,3.5,'walk'),(3.5,9,'hug'),(9,15,'walk'))
            motion(father,(3.5,9,'hug'),(9,15,'walk'))
            touch(father,'r',son,'shoulder_r',start=3,end=9,bend=1,offset=[0,10])
            touch(son,'l',father,'shoulder_l',start=3,end=9,bend=-1,offset=[0,10])
            touch(son,'r',mother,'shoulder_r',start=3.8,end=9,bend=1,offset=[0,10])
            touch(mother,'l',son,'shoulder_l',start=3.8,end=9,bend=-1,offset=[0,10])
            mother['layer']=12
            umbrella['attachment']=[];umbrella.update(x=865,y=575,scale=.75,rotation=9,layer=3)
            s['objects']=[father,son,mother,umbrella]
            camera(s,700,425,1.7,shots=[shot(0,4,790,425,1.4),shot(4,9,673,422,2.05),shot(9,15,805,420,1.45)])
            s['fade']={'out':1.2}
        p['scenes'].append(s)
    resequence(p)
    p['subtitles']=[dict(id=uid(),start=i*5,end=(i+1)*5,text=text,role='Narrator') for i,text in enumerate(NARRATION)]
    return p
