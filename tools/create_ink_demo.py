"""Create a new, portable editorial film; no frames from the reference are reused."""
import json
import math
import sys
import wave
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from studio.asset_library import install_library,asset
from studio.explainer import compile_board,apply_pose,presenter,image_item
from studio.project import save
from studio.tts import VoiceEngine
from studio.subtitles import write
from studio.media import add_waveforms

ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'examples'/'ink_showcase'

# An original hypothetical story, not historical claims or the reference's script.
SHOTS=[
    ('Một thành phố không tên','Hãy tưởng tượng bạn tìm thấy một tấm bản đồ cũ. Ở giữa bản đồ là một thành phố không còn tên gọi. Chuyện gì đã xảy ra ở nơi ấy?', 'focus',['question'],['MỘT THÀNH PHỐ\nKHÔNG CÒN TÊN?'],'question'),
    ('Những dấu vết đầu tiên','Bạn bước qua cổng thành. Những mái nhà đã biến mất, nhưng nền đá vẫn còn. Chỉ từ những dấu vết này, liệu chúng ta có thể kể lại cả một câu chuyện?', 'presenter',['city'],['Chúng ta thực sự biết điều gì?'],'point'),
    ('Hai mảnh ghép','Một chiếc bình và một cuộn giấy xuất hiện. Chiếc bình gợi ra sinh hoạt của cư dân, còn cuộn giấy mang theo lời ghi chép. Hai mảnh ghép chưa chắc đã kể cùng một chuyện.', 'compare',['amphora','scroll'],['Dấu vết vật chất','Lời ghi chép'],'explain'),
    ('Câu hỏi về thời gian','Trước tiên, hãy đặt từng mảnh ghép lên một dòng thời gian. Một ngôi làng có thể phát triển thành đô thị, rồi thay đổi. Nhưng thứ tự ấy cần được kiểm tra, không thể chỉ đoán.', 'timeline',['house','city','clock'],['Khởi đầu','Phát triển','Điều gì tiếp theo?'],'point'),
    ('Đừng vội kết luận','Nếu nhìn thấy dấu vết của lửa, bạn có thể nghĩ ngay đến một trận cháy. Nhưng một dấu vết riêng lẻ chưa đủ để giải thích vì sao cả thành phố không còn nữa.', 'quote',['flame'],['DẤU VẾT\n≠\nKẾT LUẬN'],'think'),
    ('Theo một tuyến đường','Hãy mở rộng bản đồ. Con đường nối thành phố với bến thuyền có thể gợi ra một hướng tìm kiếm khác. Bây giờ, câu chuyện không còn nằm trong một bức tường thành.', 'map',['map'],['Theo dấu một hành trình'],'point'),
    ('Những con người','Và đừng quên những con người. Sau mỗi đồ vật là người làm ra nó, sử dụng nó và mang nó đi. Một câu chuyện tốt cần nhìn thấy cả những cuộc sống ấy.', 'crowd',['tree'],['Ai đã sống ở đây?'],'welcome'),
    ('Kiểm tra nguồn','Khi đọc một tài liệu, hãy hỏi ai đã viết, viết vào lúc nào, và dựa trên điều gì. Những câu hỏi nhỏ này giúp chúng ta hiểu giới hạn của chính nguồn tư liệu.', 'process',['document','calendar','magnifier'],['Ai ghi lại?','Khi nào?','Dựa vào đâu?'],'read'),
    ('Nhìn gần hơn','Đôi khi, thay đổi góc nhìn sẽ làm một chi tiết trở nên rõ ràng. Bạn không cần một câu trả lời thật nhanh. Bạn cần một cách kiểm tra tốt hơn cho câu trả lời ấy.', 'pan',['book'],['Nhìn kỹ trước khi kết luận'],'rest'),
    ('Ý tưởng mới','Khi một mảnh ghép mới xuất hiện, cách giải thích cũ có thể cần thay đổi. Đó không phải thất bại của việc tìm hiểu. Đó là lúc câu chuyện bắt đầu rõ ràng hơn.', 'focus',['bulb'],['MỘT\nCÁCH NHÌN MỚI'],'idea'),
    ('Giữ sự tò mò','Thành phố trong câu chuyện này chỉ là tưởng tượng. Nhưng sự tò mò và thói quen kiểm tra bằng chứng thì rất thật. Hãy bắt đầu bằng một câu hỏi, rồi tìm từng mảnh ghép.', 'presenter',['compass'],['Tò mò · Kiểm tra · Kết nối'],'welcome'),
]


def prepare():
    install_library();DEST.mkdir(parents=True,exist_ok=True)
    engine=VoiceEngine(ROOT/'voices');voice=next(v for _,v in engine.voices() if v.endswith('.onnx'))
    chunks=[];cursor=0;rows=[];cues=[];rate=None
    for i,(title,text,layout,ids,labels,pose) in enumerate(SHOTS):
        output=DEST/f'voice_{i+1:02}.wav'
        # Cache only when the exact source text and speech settings match.
        fingerprint=text+'|speed=0.93'
        sidecar=output.with_suffix('.voice.txt')
        if not output.exists() or not sidecar.exists() or sidecar.read_text(encoding='utf-8')!=fingerprint:
            engine.synthesize(text,voice,output,speed=.93);sidecar.write_text(fingerprint,encoding='utf-8')
        with wave.open(str(output),'rb') as wav:
            if rate is None:rate=wav.getframerate()
            assert wav.getframerate()==rate and wav.getnchannels()==1 and wav.getsampwidth()==2
            raw=wav.readframes(wav.getnframes());seconds=wav.getnframes()/rate
        length=math.ceil((seconds+.45)*30)/30;chunks.extend([raw,b'\0\0'*(round(length*rate)-len(raw)//2)])
        gestures=[dict(t=0,pose='rest'),dict(t=.35,pose=pose,blend=.85)]
        if layout in ('presenter','quote','focus'):
            gestures.append(dict(t=length*.56,pose='explain' if pose!='idea' else 'welcome',blend=1.1))
        row=dict(start=cursor,end=cursor+length,cue_start=cursor,cue_end=cursor+seconds,
                 title=title,text=text,style='ink',layout=layout,assets=[asset(n) for n in ids],labels=labels,
                 pose=pose,gestures=gestures,show_title=False)
        if layout=='map':row.update(route=[[-210,80],[-140,20],[-50,-50],[40,-20],[120,15]],route_start=2)
        if i==2:row['reveal_times']=[0,3.2]
        if i==3:row['reveal_times']=[2.8,4.3,5.8]
        if i==4:row['reveal_times']=[1.1]
        if i==7:row['reveal_times']=[.4,2.5,4.5]
        if i==9:row['reveal_times']=[2.0]
        rows.append(row);cues.append(dict(id=str(i),start=cursor,end=cursor+seconds,text=text));cursor+=length
        print(i+1,title,round(length,2),flush=True)
    narration=DEST/'narration.wav'
    with wave.open(str(narration),'wb') as wav:
        wav.setnchannels(1);wav.setsampwidth(2);wav.setframerate(rate);wav.writeframes(b''.join(chunks))
    board=dict(version=1,name='Một thành phố không tên · Ink Studio',voice=str(narration),timing='authored',rows=rows)
    project=compile_board(board)
    # A real brief walk within the crowd shot, with stable world-space stance.
    crowd=next(s for s in project['scenes'] if s['layout']=='crowd')
    walker=next(o for o in crowd['objects'] if o['kind']=='character' and o['scale']<1.3)
    walker['action']='walk';walker['pose']='walk';walker['poses']=[];walker['keys']={}
    walker['motions']=[dict(start=.5,end=crowd['duration']-1,action='walk',blend=.5)]
    x=walker['x'];walker['keys']['x']=[dict(t=0,v=x),dict(t=.5,v=x),dict(t=crowd['duration']-1,v=x+140,ease='ease_in_out'),dict(t=crowd['duration'],v=x+140)]
    add_waveforms(project,DEST)
    saved=save(project,DEST/'project.json',DEST)
    (DEST/'storyboard.json').write_text(json.dumps(saved['storyboard'],ensure_ascii=False,indent=2),encoding='utf-8')
    write(cues,DEST/'narration.srt');(DEST/'script.txt').write_text('\n\n'.join(s[1] for s in SHOTS),encoding='utf-8')
    print('DURATION',cursor,flush=True)
    return project


if __name__=='__main__':prepare()
