from pathlib import Path
import wave,math,array
from .contracts import RATE,Mutation,uid,Node,Scene,EpisodePlan

def create_fixture(service):
    p=service.store.create('Minh họa kỹ thuật — chiếc hộp')
    base=service.store.root/'projects'/p['id'];wav=base/'working'/'Giọng thử có khoảng trắng.wav';srt=base/'working'/'Phụ đề tiếng Việt.srt'
    count=48*RATE;values=array.array('h',[0])*count*2
    for second in [2,18,34,46]:
        for i in range(RATE//10):
            value=int(8000*math.sin(2*math.pi*880*i/RATE))
            values[(second*RATE+i)*2]=value;values[(second*RATE+i)*2+1]=value
    with wave.open(str(wav),'wb') as f:f.setnchannels(2);f.setsampwidth(2);f.setframerate(RATE);f.writeframes(values.tobytes())
    srt.write_text('\ufeff1\n00:00:00,000 --> 00:00:16,000\nAn không buông chiếc hộp. Cậu kéo nó sang phải, rồi dừng lại.\n\n2\n00:00:16,000 --> 00:00:32,000\nBa bước: chuẩn bị, di chuyển, giữ yên.\n\n3\n00:00:32,000 --> 00:00:48,000\nĐây là minh họa kỹ thuật. Khoảng tĩnh có chủ ý giúp nhìn rõ kết quả.\n',encoding='utf-8')
    def mutate(data,reason):
        current=service.store.get(p['id']);return Mutation(expected_revision=current['revision'],actor='ui',change_reason=reason,idempotency_key=uid('fixture'),data=data)
    service.import_sources(p['id'],mutate({},'Nhập fixture có tên Unicode'),wav,srt)
    p=service.store.get(p['id']);aid=p['audio']['id'];utterances=p['utterances']
    def node(**kw):return Node(**kw).model_dump()
    def text(id,text,x,y,width=900,size=48,**kw):return node(id=id,kind='text',text=text,x=x,y=y,width=width,height=size*2,font_size=size,color='#26313d',**kw)
    k=lambda sec,value,easing='smooth':dict(sample=int(sec*RATE),value=value,easing=easing)
    first=[text('title1','AN KHÔNG BUÔNG CHIẾC HỘP',160,140,1500,56),text('label1','Tay và đạo cụ cùng chuyển động',160,238,1200,30),node(id='an',kind='character',x=660,y=750,pose='hold',expression='curious',scale=1.2,keyframes={'x':[k(0,660,'hold'),k(4,660),k(10,1120),k(16,1120)]}),node(id='box',kind='prop',parent_id='an',attachment='hand_right',x=12,y=-12,width=120,height=100,color='#e7b76c',z=2),text('reveal1','DỪNG LẠI — vẫn giữ hộp',260,900,1350,42,keyframes={'reveal':[k(0,0,'hold')]})]
    second=[text('title2','3 BƯỚC ĐỂ THẤY RÕ MỘT HÀNH ĐỘNG',150,130,1550,54)]
    for i,(label,color) in enumerate([('1. Chuẩn bị','#dce7d2'),('2. Di chuyển','#91c8bb'),('3. Giữ yên','#e7b76c')]):
        second.append(node(id=f'card{i}',kind='prop',x=380+i*570,y=560,width=440,height=310,color=color,keyframes={'opacity':[k(16,0,'hold'),k(18+i*3,1)]}))
        second.append(text(f'step{i}',label,215+i*570,515,400,40,keyframes={'opacity':[k(16,0,'hold'),k(18+i*3,1)]}))
    third=[text('title3','KHOẢNG TĨNH CŨNG LÀ MỘT LỰA CHỌN',170,155,1500,52),node(id='an_end',kind='character',x=520,y=775,pose='hold',expression='happy',scale=1.2),node(id='box_end',kind='prop',parent_id='an_end',attachment='hand_right',x=12,y=-12,width=120,height=100,color='#e7b76c',z=2),text('closing','Giữ hình để người xem\nnhìn rõ kết quả.',970,430,700,56),text('fixture_notice','FIXTURE KỸ THUẬT · audio là tone, mốc lời tổng hợp',210,970,1500,27)]
    scenes=[]
    for i,nodes in enumerate([first,second,third]):
        scenes.append(Scene(id=f'scene_{i+1}',start_sample=i*16*RATE,end_sample=(i+1)*16*RATE,purpose=['Thể hiện phủ định, tiếp xúc tay–đạo cụ và di chuyển','Giải thích hành động bằng bố cục ba bước','Giữ hình có chủ ý để chốt kết quả'][i],utterance_ids=[utterances[i]['id']],knowledge_before='Đây là nhân vật An và chiếc hộp minh họa',reveal_rules='Chỉ hiện kết quả tại anchor đã khai báo',emotional_intent='Tò mò rồi hiểu rõ',visual_strategy=['Diễn xuất nhân vật và hộp gắn tay','Sơ đồ ba bước bằng chữ thật','Giữ hình có chủ ý'][i],requirements=['Kit nhân vật gốc','Chữ tiếng Việt','Audio master'],nodes=nodes,transition='dissolve' if i else 'cut',transition_samples=RATE//2 if i else 0).model_dump())
    events=[]
    for id,sec,action,params in [('evt_pull',4,'pose_swap',{'pose':'pull'}),('evt_stop',12,'pose_swap',{'pose':'hold'}),('evt_reaction',12,'expression_swap',{'expression':'surprised'}),('evt_reveal',12,'reveal',{'value':1})]:
        events.append({'id':id,'scene_id':'scene_1','target_id':'reveal1' if action=='reveal' else 'an','action':action,'anchor':{'audio_revision':aid,'manual_sample':sec*RATE,'evidence':'Timestamp fixture tổng hợp, không phải alignment giọng thật'},'duration_samples':1600,'parameters':params,'dependency_ids':['builtin_character_v1']})
    plan=EpisodePlan(audio_revision=aid,outline=['Một chuyển động có tiếp xúc','Giải thích ba bước','Giữ hình và chốt'],open_questions=[],payoff='Đạo cụ đi theo tay, chữ tiết lộ đúng mốc',narrative_approach='Giải thích cơ chế bằng một hành động',distinctiveness_notes='Một cảnh diễn xuất, một sơ đồ, một khoảng tĩnh',opening_promise='Cho thấy quan hệ giữa nhân vật và đạo cụ',scenes=scenes,events=events).model_dump()
    service.write_plan(p['id'],mutate({'plan':plan},'Lưu kế hoạch fixture'))
    service.commit(p['id'],mutate({},'Chốt fixture đã preflight'))
    service.compile(p['id'],mutate({},'Compile fixture'))
    def notice(state):
        state['fixture_notice']='DỮ LIỆU MINH HỌA: audio tổng hợp có marker; không có giọng đọc và chưa kiểm chứng ASR tiếng Việt.'
    service.store.mutate(p['id'],mutate({},'Gắn nhãn fixture tổng hợp'),'fixture_notice',notice)
    return {'project_id':p['id'],'revision':service.store.get(p['id'])['revision'],'notice':'48 giây; audio tone; 3 cảnh; đạo cụ gắn tay'}
