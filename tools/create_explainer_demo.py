"""Create original editable illustration assets, voice, SRT, storyboard and showcase."""
import sys,json,subprocess,wave
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from studio.explainer import compile_board
from studio.project import save
from studio.subtitles import write
from studio.tts import VoiceEngine

ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'examples'/'explainer_showcase'
ART=ROOT/'assets'/'explainer'
INK='#242c31';GOLD='#f4c44f';BLUE='#9dc9dc';GREEN='#90bd9d';RED='#d86e55'

def svg(name,body):
    p=ART/(name+'.svg');p.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="900" height="560" viewBox="0 0 900 560"><g stroke="{INK}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round">{body}</g></svg>',encoding='utf-8');return str(p)

def assets():
    ART.mkdir(parents=True,exist_ok=True)
    city=svg('thanh_co',f'<path d="M70 460H830" fill="none"/><path d="M120 440V260H190V210H260V260H330V440M560 440V250H630V200H700V250H780V440" fill="{GOLD}"/><path d="M330 440V310H560V440M390 440V370Q445 320 500 370V440" fill="#f3ddac"/><path d="M120 295H330M560 285H780M120 330H330M560 330H780M120 370H330M560 370H780" fill="none"/><path d="M90 250L230 140L365 250M525 240L665 120L810 240" fill="{RED}"/><circle cx="450" cy="130" r="47" fill="{GOLD}"/><path d="M420 210Q450 175 480 210" fill="none"/>')
    pot=svg('hien_vat',f'<path d="M250 160H500L480 240Q610 340 540 440Q510 490 375 490Q240 490 210 440Q140 340 270 240Z" fill="{RED}"/><ellipse cx="375" cy="160" rx="125" ry="30" fill="#f2d7bd"/><path d="M220 330H530M210 370H540M260 420L300 390L340 420L380 390L420 420L460 390L500 420" fill="none"/><path d="M590 170L790 140L810 420L610 450Z" fill="#fff5d8"/><path d="M625 220L755 205M630 265L770 250M635 310L775 295M640 355L745 345" fill="none"/>')
    scroll=svg('van_ban',f'<path d="M200 110H720Q770 110 750 170H660V430Q660 480 600 470H160Q110 470 130 415H220V150Q220 110 200 110Z" fill="#f3ddac"/><path d="M660 170V150Q660 115 700 110M220 415H600Q570 475 600 470" fill="none"/><path d="M295 210H585M295 260H550M295 310H580M295 360H490" fill="none"/>')
    book=svg('doi_chieu',f'<path d="M95 160Q260 100 440 180V470Q260 400 95 455ZM440 180Q620 100 805 160V455Q620 400 440 470Z" fill="#fff5d8"/><path d="M140 210Q270 175 390 220M140 270Q270 235 390 280M140 330Q270 295 390 340M490 220Q620 175 760 210M490 280Q620 235 760 270" fill="none"/><circle cx="635" cy="365" r="82" fill="{BLUE}"/><path d="M690 425L770 505" stroke-width="20"/><path d="M590 365L625 400L680 330" stroke="{GREEN}" stroke-width="14" fill="none"/>')
    mapart=svg('ban_do',f'<path d="M70 400L140 210L300 100L440 180L580 90L760 160L825 350L720 440L550 390L410 470L260 400L130 470Z" fill="{GREEN}"/><path d="M440 180Q350 280 480 320T550 390M180 360Q400 120 710 330" stroke="{BLUE}" stroke-width="16" fill="none"/><path d="M180 360Q400 120 710 330" stroke="{RED}" stroke-width="5" stroke-dasharray="13 14" fill="none"/><circle cx="180" cy="360" r="18" fill="{RED}"/><circle cx="710" cy="330" r="18" fill="{RED}"/>')
    ship=svg('giao_thuong',f'<path d="M140 360H780L720 455H230Z" fill="#b98765"/><path d="M420 110V360M420 130L230 330H420Z" fill="{GOLD}"/><path d="M445 150L670 330H445Z" fill="#f9f5e9"/><path d="M80 485Q150 450 220 485T360 485T500 485T640 485T780 485T900 485" stroke="{BLUE}" fill="none"/><path d="M300 390H660" fill="none"/>')
    return dict(city=city,pot=pot,scroll=scroll,book=book,map=mapart,ship=ship)

SCRIPTS=[
('Vì sao lịch sử còn khoảng trống?', 'Lịch sử không phải một cuốn sách còn nguyên mọi trang. Điều chúng ta biết được ghép lại từ những dấu vết còn sót lại. Vậy điều gì xảy ra khi một phần dấu vết biến mất?', 'presenter','city',[], 'question'),
('Hai nguồn, hai góc nhìn', 'Một chiếc bình có thể kể về đời sống thường ngày. Một văn bản ghi lại cách người xưa nhìn thế giới. Mỗi nguồn cho ta một góc nhìn, và mỗi nguồn cũng có giới hạn riêng.', 'compare','pot,scroll',['Hiện vật','Văn bản'], 'point'),
('Từ dấu vết đến cách giải thích', 'Công việc nghiên cứu bắt đầu từ việc tìm thấy dấu vết, xác định bối cảnh, rồi đối chiếu nhiều nguồn. Một cách giải thích có thể thay đổi khi xuất hiện bằng chứng mới.', 'timeline','pot,scroll,book',['Phát hiện','Bối cảnh','Đối chiếu'], 'point'),
('Một dấu hỏi chưa phải lời giải', 'Nếu chỉ nhìn một mảnh ghép, chúng ta rất dễ tưởng tượng ra toàn bộ câu chuyện. Điều cần làm là phân biệt điều đã biết, điều suy đoán, và điều vẫn chưa có đủ bằng chứng.', 'quote','',['Đã biết → Có căn cứ','Suy đoán → Cần kiểm tra','Chưa biết → Tiếp tục tìm hiểu'], 'think'),
('Những dấu vết kết nối', 'Bản đồ giúp đặt các dấu vết vào không gian. Một tuyến đường có thể gợi ra sự liên hệ giữa những nơi xa nhau. Nhưng mối liên hệ ấy vẫn cần được kiểm tra bằng các nguồn khác.', 'presenter','map',['Không gian','Tuyến đường','Bằng chứng'], 'point'),
('Đặt câu hỏi theo từng bước', 'Thay vì đi thẳng đến một kết luận hấp dẫn, hãy hỏi: nguồn này đến từ đâu, được tạo ra trong hoàn cảnh nào, và có nguồn độc lập nào giúp kiểm chứng hay không?', 'process','scroll,pot,book',['Nguồn gốc?','Bối cảnh?','Kiểm chứng?'], 'explain'),
('Nhìn rộng hơn một khung hình', 'Khi thay đổi góc nhìn, chúng ta có thể nhận ra những chi tiết trước đó bị bỏ qua. Một câu chuyện thuyết phục cần được xây dựng từ nhiều mảnh ghép phù hợp với nhau.', 'gallery','city,pot,ship,book',[], 'welcome'),
('Giữ sự tò mò, cùng sự thận trọng', 'Những khoảng trống khiến lịch sử trở nên thú vị. Hãy giữ sự tò mò, nhưng luôn hỏi về bằng chứng. Một câu hỏi tốt có thể đưa chúng ta đến gần sự thật hơn một câu trả lời quá vội vàng.', 'presenter','book',['Tò mò','Đối chiếu','Thận trọng'], 'welcome')]

def prepare():
    DEST.mkdir(parents=True,exist_ok=True);art=assets();engine=VoiceEngine(ROOT/'voices');voice=next(v for _,v in engine.voices() if v.endswith('.onnx'))
    parts=[];rows=[];cues=[];cursor=0;rate=None;frames=[]
    for i,(title,text,layout,images,labels,pose) in enumerate(SCRIPTS):
        path=DEST/f'voice_{i+1:02}.wav'
        if not path.exists():engine.synthesize(text,voice,path,speed=.98)
        with wave.open(str(path),'rb') as wav:
            if rate is None:rate=wav.getframerate()
            assert wav.getframerate()==rate and wav.getnchannels()==1 and wav.getsampwidth()==2
            data=wav.readframes(wav.getnframes());actual=wav.getnframes()/rate
        # Scene boundaries are aligned to the 30 FPS frame grid; silence pads the phrase.
        length=__import__('math').ceil((actual+.55)*30)/30;silence=round(length*rate)-len(data)//2
        frames.extend((data,b'\0\0'*silence));parts.append(path)
        row=dict(start=cursor,end=cursor+length,title=title,text=text,layout=layout,assets=[art[k] for k in images.split(',') if k],labels=labels,pose=pose,cue_start=cursor,cue_end=cursor+actual)
        rows.append(row);cues.append(dict(id=str(i),start=cursor,end=cursor+actual,text=text));cursor+=length
        print(i+1,title,round(length,2),flush=True)
    voicepath=DEST/'narration.wav'
    with wave.open(str(voicepath),'wb') as wav:wav.setnchannels(1);wav.setsampwidth(2);wav.setframerate(rate);wav.writeframes(b''.join(frames))
    board=dict(version=1,name='Những mảnh ghép lịch sử · Studio',voice=str(voicepath),timing='srt',rows=rows)
    (DEST/'storyboard.json').write_text(json.dumps(board,ensure_ascii=False,indent=2),encoding='utf-8')
    write(cues,DEST/'narration.srt');(DEST/'script.txt').write_text('\n\n'.join(x[1] for x in SCRIPTS),encoding='utf-8')
    project=compile_board(board)
    # Same pose controls exposed by the UI; subtle acting while preserving a readable hold.
    from studio.explainer import apply_pose
    for s in project['scenes']:
        for o in s['objects']:
            if o['kind']=='character' and o['scale']>1:
                apply_pose(o,'explain',min(4,s['duration']*.35),1.05)
    from studio.media import add_waveforms
    add_waveforms(project,DEST)
    saved=save(project,DEST/'project.json',DEST)
    (DEST/'storyboard.json').write_text(json.dumps(saved['storyboard'],ensure_ascii=False,indent=2),encoding='utf-8')
    print('Project:',DEST/'project.json','duration:',cursor,flush=True)

if __name__=='__main__':prepare()
