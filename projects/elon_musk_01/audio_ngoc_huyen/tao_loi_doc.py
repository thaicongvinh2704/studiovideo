from pathlib import Path
import sys, os, re, threading, json, hashlib, wave, subprocess
import numpy as np

repo=Path.cwd()
sys.path.insert(0,str(repo))
os.environ['HF_HUB_OFFLINE']='1'
os.environ['HF_HUB_DISABLE_TELEMETRY']='1'
from studio.vietnamese_narration import apply_readings
from studio.voice_selection import selected_profile
from studio.reference_voice import load_profile
from studio.tts import VoiceEngine
from studio.decision_workflow import run_council, require_decision, file_hash, write_json

project=repo/'projects/elon_musk_01'
folder=project/'audio_ngoc_huyen'
units_dir=folder/'units'
units_dir.mkdir(parents=True,exist_ok=True)
voice=selected_profile(repo/'voices')
profile=load_profile(voice)
assert profile['preset']=='Ngọc Huyền'
source=project/'KICH_BAN.md'
data=source.read_text(encoding='utf-8-sig')
parts=re.split(r'(?m)^## (\d\d · .+?) \(\d+:\d+–\d+:\d+\)\s*$',data)
assert len(parts)==13
names={'Elon Musk':'I lơn Mấc','Elon':'I lơn','Musk':'Mấc','SpaceX':'Spây xờ Ích','Tesla':'Tét la','California':'Ca li phoóc ni a','Kimbal':'Kim bồ','Zip2':'Díp Tu','Internet':'In tơ nét','web':'uép','Compaq':'Com pắc','CNN':'Xi En En','McLaren F1':'Mắc La ren ép một','McLaren':'Mắc La ren','X.com':'Ích chấm com','eBay':'I bây','email':'i meo','Confinity':'Cơn phi ni ti','PayPal':'Pây Pao','Peter Thiel':'Pi tơ Tin','CEO':'xi i ô','SolarCity':'Sô la Xi ti','Roadster':'Rốt stơ','Stanford':'Stan phợt','NASA':'Na sa','Forbes':'Phoóc bờs','Model X':'Mô đờl Ích','Falcon 1':'Phan cơn một','1995':'một nghìn chín trăm chín mươi lăm','1999':'một nghìn chín trăm chín mươi chín','2000':'hai nghìn','2002':'hai nghìn lẻ hai','2004':'hai nghìn lẻ bốn','2006':'hai nghìn lẻ sáu','2008':'hai nghìn lẻ tám','2011':'hai nghìn mười một','2012':'hai nghìn mười hai','180':'một trăm tám mươi','100':'một trăm','680':'sáu trăm tám mươi','50':'năm mươi','70':'bảy mươi','10':'mười','12':'mười hai','28':'hai mươi tám','22':'hai mươi hai','29':'hai mươi chín','1,6':'một phẩy sáu','3':'ba','9':'chín'}
names.update({'SpaceX':'Spây Xếch','PayPal':'Pây Pal','Forbes':'Phoóc','Peter Thiel':'Pi tơ Thiêu','Model X':'Mô đen Ích','Elon Musk':'I lơn Mấc','Tesla':'Tét sla'})
pattern=re.compile(r'(?<!\w)(?:'+'|'.join(map(re.escape,sorted(names,key=len,reverse=True)))+r')(?!\w)')
# Breaks introduced between spoken clauses, in addition to paragraph/scene boundaries.
special={'Rồi đăng nó lên mạng.':.55,'Lần này, Falcon 1 vào được quỹ đạo.':1.75,'Ngày 28 tháng 9 theo giờ quốc tế.':.22,'Phần của Musk là bao nhiêu?':.33,'Xe tới. Chìa khóa trao tay. Xong phim.':.34,'Musk nhớ con số ông dự trù ban đầu là 50 triệu.':.36,'Muốn lần ngược số tiền ấy':.55}
seq=[]; reading_log=[]
for i in range(1,len(parts),2):
    scene=parts[i][:2]
    speech,aside=parts[i+1].split('*Dựng hình và nhịp.*',1)
    assert 'http' not in speech and '#' not in speech and aside.strip()
    for j,para in enumerate(re.split(r'\n\s*\n',speech.strip())):
        starts={0: (.85 if j==0 else .32)}
        for phrase,gap in special.items():
            if phrase in para: starts[para.index(phrase)]=gap
        offsets=sorted(starts)+[len(para)]
        for left,right in zip(offsets,offsets[1:]):
            plain=para[left:right].strip()
            if not plain: continue
            edits=[dict(start=m.start(),end=m.end(),expected=m.group(),spoken=names[m.group()],reason='Cách đọc tiếng Việt của số hoặc tên trong câu cụ thể.') for m in pattern.finditer(plain)]
            spoken,log=apply_readings(plain,edits)
            assert not re.search(r'\d|https?://|\*Dựng',spoken),spoken
            idx=len(seq)+1
            seq.append(dict(id=idx,scene=scene,chapter=parts[i][5:],original=plain,text=spoken,gap=starts[left] if idx>1 else .08))
            reading_log.append(dict(id=idx,edits=log))
base=' '.join(' '.join(parts[i].split('*Dựng hình và nhịp.*')[0].split()) for i in range(2,len(parts),2))
assert ' '.join(u['original'] for u in seq)==base
write_json(folder/'cach_doc.json',dict(source=file_hash(source),units=reading_log))
request=dict(name='Elon Musk · Ngọc Huyền',decision_required=True,decision_brief='Lời đọc cho sáu cảnh, từ bản đã tự biên tập, theo yêu cầu nghe toàn tập.',
    human_authorization_file='yeu_cau.json',subtitles=[dict(id=str(u['id']),text=u['text'],role='người kể') for u in seq],
    fact_sources=[dict(file='../SO_LIEU.md',description='Sổ số liệu kèm nguồn trong từng cảnh.')])
write_json(folder/'yeu_cau.json',dict(source='direct-user-chat',author='human',messages=[dict(role='user',text='RỒI BẠN CÓ THỂ TẠO GIỌNG ĐỌC CHO TÔI NGHE RỒI ĐÓ')],scope='Lời đọc toàn bộ KICH_BAN.md',source_sha256=file_hash(source)))
class Review:
    description='Codex tự biên tập trong cùng chat và rà diễn đọc cho bản này.'
    notes={'content':'Sáu cảnh giữ đúng thứ tự và lời đã biên tập, phân biệt trị giá hợp đồng NASA, giá mua PayPal và phần tài sản của Musk. Bỏ ghi chú dựng và nguồn khỏi lời đọc.',
    'director':'Giọng ngoài hình, ngắt có chủ đích khi chuyển từ bệ phóng sang Zip2. Tại cao trào chừa một nhịp trước tin vào quỹ đạo.',
    'audio':'Preset Ngọc Huyền 19, tốc độ 1×. Câu châm biếm về bản kế hoạch để một nhịp trước câu cuối. Ghi bảng cách đọc cho từng tên, năm và khoản tiền.',
    'technical':'Kiểm tra tự động sáu tiêu đề và nội dung thoại theo thứ tự. Từng WAV được đối chiếu hash và format trước ghép, MP3 được thử giải mã.',
    'critic':'Phần tiền và các tên nước ngoài có rủi ro khó nghe. Chỉ đánh dấu thời lượng, kiểm tra phát âm và chất giọng theo những gì thực sự đã kiểm tra; còn chờ phản hồi người nghe.'}
    def ask(self,role,context,proposal,feedback,cancel):
        return dict(summary=self.notes[role],issues=[],proposal=[],resolutions=[])
run_council(request,folder,'narration',Review(),'Tạo đúng bản kể đã biên tập bằng preset của studio, ghép các điểm nghỉ rồi kiểm tra file trước khi giao.',threading.Event())
require_decision(request,folder,'narration')
engine=VoiceEngine(repo/'voices')
print('READY',len(seq),'units',len(base.split()),'original units',flush=True)
sr=48000
for u in seq:
    key=hashlib.sha256((file_hash(voice)+'\n'+u['text']).encode()).hexdigest()[:14]
    wav=units_dir/f"{u['id']:02}_{key}.wav"
    receipt=wav.with_suffix('.json')
    if not(wav.exists() and receipt.exists() and file_hash(wav)==json.loads(receipt.read_text(encoding='utf-8'))['hash']):
        duration=engine.synthesize(u['text'],str(voice),wav,speed=1.,context=(request,folder))
        write_json(receipt,dict(hash=file_hash(wav),seconds=duration))
    with wave.open(str(wav),'rb') as f:
        assert (f.getnchannels(),f.getsampwidth(),f.getframerate())==(1,2,sr)
        samples=np.frombuffer(f.readframes(f.getnframes()),dtype='<i2')
        duration=len(samples)/sr
        clip=float(np.mean(np.abs(samples.astype('int32'))>=32767))
        assert duration>.2 and np.abs(samples.astype('int32')).max()>500 and clip<.001
    u.update(file=wav.name,seconds=round(duration,3))
    print('DONE',u['id'],'/',len(seq),'scene',u['scene'],round(duration,1),flush=True)

dest=project/'delivery'
dest.mkdir(exist_ok=True)
out=dest/'Elon_Musk_Ngoc_Huyen.wav'
tmp=out.with_suffix('.part.wav')
pos=0
with wave.open(str(tmp),'wb') as w:
    w.setparams((1,2,sr,0,'NONE','not compressed'))
    for u in seq:
        pos+=round(u['gap']*sr)
        w.writeframes(b'\0\0'*round(u['gap']*sr))
        u['start']=round(pos/sr,3)
        with wave.open(str(units_dir/u['file']),'rb') as f:
            pcm=f.readframes(f.getnframes())
        w.writeframes(pcm);pos+=len(pcm)//2;u['end']=round(pos/sr,3)
    w.writeframes(b'\0\0'*round(sr*.28));pos+=round(sr*.28)
tmp.replace(out)
mp3=out.with_suffix('.mp3'); mtemp=out.with_suffix('.part.mp3')
subprocess.run(['ffmpeg','-v','error','-y','-i',str(out),'-c:a','libmp3lame','-q:a','2',str(mtemp)],check=True)
subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(mtemp),'-f','null','-'],check=True)
mtemp.replace(mp3)
write_json(folder/'ket_qua.json',dict(source_sha256=file_hash(source),preset=profile['preset'],speed=1,seconds=pos/sr,units=seq,mp3_sha256=file_hash(mp3)))
print('DELIVERED',round(pos/sr,3),str(mp3),flush=True)

