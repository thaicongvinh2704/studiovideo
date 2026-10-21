"""An authored 32-shot film, operated through Studio's public project/renderer/exporter APIs."""
import copy,json,math,shutil,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
DEST=Path(__file__).resolve().parents[1];ART=DEST/'art'
from studio.project import new_project,new_scene,new_object,save
from studio.explainer import presenter,text_item,image_item,item
from studio.directing import gesture_sequence,preflight
from studio.subtitles import read,write
from studio.asset_library import asset
from studio.media import add_waveforms

CHAPTERS=[(0,'01 / THỨC DẬY BÊN DÒNG SÔNG'),(61.285,'02 / MỘT BỮA CƠM TỪ ĐẤT'),(93.879,'03 / SỐNG CÙNG SÔNG NƯỚC'),(121.423,'04 / NHỮNG BÀN TAY ĐÚC ĐỒNG'),(187.070,'05 / DẤU TÍCH CỔ LOA'),(238.485,'06 / KHÉP LẠI MỘT NGÀY')]
NAMES=['Nếu tỉnh dậy ở Việt Nam cổ','Hôm nay ăn gì?','Cư dân bên những dòng sông','Một bếp lửa và một gia đình','Những cái tên đã mất','Ngôi nhà trên những cột gỗ','Khoảng trống và cánh đồng','Bữa ăn bắt đầu từ đất','Đợi một mùa lúa','Bát cơm và thời tiết','Ra phía dòng sông','Lưỡi câu, lưới và thuyền','Một giỏ cá trở về','Bên lò đúc đồng','Khuôn, lửa và kinh nghiệm','Nhìn gần trống Ngọc Lũ','Con người trong hoa văn','Một dáng người giã gạo','Kỹ thuật và những câu hỏi','Sự im lặng của hiện vật','Từ ngôi làng đến Cổ Loa','Truyền thuyết và dấu tích','Khuôn đúc và xưởng chế tác','Năng lực của con người','Ai nuôi người thợ?','Những con người không tên','Bên bếp lửa buổi chiều','Giới hạn của tưởng tượng','Một mùa gặt bình an','Những vật nhỏ còn lại','Bát cơm hôm nay','Những bàn tay vì ngày mai']


class Stage:
    def __init__(self,scene):self.s=scene;self.L=scene['duration'];self.objects=scene['objects']
    def add(self,o,start=0,end=None):
        o.update(start=start,end=self.L if end is None else end);o.setdefault('enter','none');self.objects.append(o);return o
    def image(self,name,x,y,w,h,start=0,layer=12,parent=None,**extra):
        file=ART/(name if '.' in name else name+'.svg')
        if not file.exists():file=Path(asset(name))
        o=image_item(str(file),x,y,w,h);o.update(layer=layer,**extra)
        if parent:o['parent']=parent['id']
        if start:o.update(enter='fade',enter_duration=.30)
        return self.add(o,start)
    def text(self,value,x=640,y=121,w=1100,h=85,size=33,start=0,**extra):
        data=dict(font='Segoe Print',layer=50,color='#252525');data.update(extra)
        o=text_item(value,x,y,w,h,size,**data)
        if start:o.update(enter='fade',enter_duration=.3)
        return self.add(o,start)
    def shape(self,kind,x,y,w,h,start=0,**extra):
        data=dict(shape=kind,layer=22,color='#252525',fill='#fff8e9',stroke=3);data.update(extra)
        return self.add(item('shape',kind,x,y,w,h,**data),start)
    def host(self,x=210,y=600,sc=2.05,pose='explain',switch='point',when=None):
        o=presenter(x,y,sc,'rest')
        beats=[dict(t=0,pose='rest'),dict(t=.25,pose=pose,blend=.85)]
        if switch:beats.append(dict(t=when or self.L*.55,pose=switch,blend=.85))
        gesture_sequence(o,beats);o['name']='Người dẫn · Áo đen';return self.add(o)
    def group(self,name,x=0,y=0,**extra):
        o=new_object('group',name,x,y);o.update(**extra);return self.add(o)
    def drift(self,o,key,a,b,start=0,end=None):
        o.setdefault('keys',{})[key]=[dict(t=start,v=a),dict(t=self.L if end is None else end,v=b,ease='ease_in_out')];return o
    def oscillate(self,o,key,center,amount,period=2.5):
        frames=[]
        for i in range(math.ceil(self.L/(period/2))+1):frames.append(dict(t=i*period/2,v=center+amount*((-1)**i),ease='ease_in_out'))
        o.setdefault('keys',{})[key]=frames;return o
    def hearth(self,x=660,y=430,sc=1):
        self.image('hearth',x,y,370*sc,277*sc,layer=18)
        f=self.image('flame',x,y+59*sc,90*sc,100*sc,layer=19)
        self.oscillate(f,'scale',1,.035,1.3)
        sm=self.image('smoke',x,y-140*sc,95*sc,165*sc,layer=16,opacity=.50);self.drift(sm,'y',y-130*sc,y-160*sc)
    def boat(self,x=675,y=450,sc=1,travel=35):
        g=self.group('Thuyền và người chèo',x,y)
        self.image('boat',0,27,460*sc,265*sc,parent=g,layer=21)
        self.image('fisher',-25*sc,-10*sc,130*sc,177*sc,parent=g,layer=20)
        o=self.image('oar',-5*sc,14*sc,75*sc,165*sc,parent=g,layer=23,pivot=[-14*sc,-68*sc])
        self.oscillate(o,'rotation',-12,8,3.1);self.drift(g,'x',x-travel/2,x+travel/2);self.oscillate(g,'y',y,2,3)
        return g
    def field(self):self.image('rice_field',670,390,1160,408,layer=8)
    def note(self,text,start=0):self.text(text,905,594,650,35,17,start,font='Segoe UI',color='#73716b')


def compose(n,s,cues):
    st=Stage(s);L=st.L;second=cues[1]['start']-s['start']
    chapter=next(label for t,label in reversed(CHAPTERS) if t<=s['start']+.001)
    st.text(chapter,370,43,620,40,19,align='left',color='#8a6548',font='Segoe UI',bold=True)
    st.shape('line',640,79,1140,1,color='#d5c4ac',stroke=1)
    tag='ẢNH HIỆN VẬT / HÌNH THAM KHẢO' if n in (15,16,18,19) else 'CẢNH DỰNG MINH HỌA'
    st.text(tag,1070,43,300,35,12,font='Segoe UI',color='#817e76')
    if n==0:
        st.host(205,598,2.25,'question','point',second+.1)
        st.text('MỘT NGÀY CÙNG\nNGƯỜI VIỆT CỔ',845,175,730,160,46,bold=True)
        st.image('village',850,423,775,390,layer=8)
        sun=st.image('sun',1130,225,92,92,layer=7);st.drift(sun,'y',235,218)
        st.image('phone',795,450,100,125,second,layer=26);st.image('bulb',970,450,100,125,second,layer=26)
        for x in (795,970):st.shape('cross',x,448,80,80,second,color='#ba6956',stroke=5)
        st.note('Một hành trình hình dung từ dấu tích Đông Sơn')
    elif n==1:
        st.host(240,600,2.2,'question','welcome',second+.1)
        st.image('bowl',840,345,505,388);st.text('HÔM NAY, ĂN GÌ?',840,133,660,80,39)
        for i,a in enumerate(('rice','fish','hearth')):st.image(a,650+i*190,540,150,120,second+i*.28)
    elif n==2:
        st.host(220,600,2,'point','explain',second)
        st.image('rivers_map',850,354,630,490);st.text('CƯ DÂN ĐÔNG SƠN',820,125,740,70,36)
        st.text('Miền Bắc Việt Nam ngày nay',845,560,700,70,27,start=second)
        st.note('Sơ đồ gợi tả sông ngòi · không theo tỷ lệ')
    elif n==3:
        st.text('BẮT ĐẦU TỪ MỘT BẾP LỬA',size=37)
        st.image('stilt_house',1020,330,370,278,layer=6,opacity=.6)
        st.image('mother',475,395,211,289,layer=19);st.image('seated_child',825,474,135,183,start=second,layer=20)
        st.hearth(650,451,.9);st.image('bowl',993,528,150,110,second)
    elif n==4:
        st.host(220,602,2.05,'listen','think',second)
        st.image('mother',670,328,151,205,opacity=.40);st.image('child',824,361,112,152,opacity=.40)
        st.text('Không còn tên trong ghi chép',825,127,720,70,32)
        st.image('excavation',848,458,490,310,second,layer=24)
        st.text('Nhưng dấu vết lao động vẫn còn',845,586,700,45,26,start=second)
    elif n==5:
        st.image('stilt_house',735,362,780,475,layer=15)
        st.host(170,600,1.75,'point','think',second)
        st.text('NHÀ SÀN',795,120,650,70,37)
        st.shape('arrow',555,440,150,15,second,rotation=-22,color='#a67650')
        st.note('Hình dựng gợi tả · bố trí từng ngôi nhà chưa được biết đầy đủ',second)
    elif n==6:
        st.text('QUÁ KHỨ RỘNG HƠN ĐIỀU TA BIẾT',size=33)
        st.image('excavation',357,352,460,345);st.image('question',359,185,77,92)
        st.image('rice_field',900,365,600,360,second)
        st.text('Dấu tích còn lại',350,575,450,55,28);st.text('Một cuộc sống rộng lớn',920,575,520,55,28,start=second)
        st.shape('line',640,370,1,330,color='#dbd1c1',stroke=2)
    elif n==7:
        st.field();st.image('farmer',475,415,242,303,layer=22);h=st.image('hoe',545,486,170,195,layer=23,pivot=[27,-38.6]);st.oscillate(h,'rotation',-15,3,3.6)
        st.text('BỮA ĂN BẮT ĐẦU TỪ ĐẤT',size=35)
        for i,(a,label) in enumerate((('plough','Lưỡi cày'),('hoe','Cuốc'),('sickle','Lưỡi hái'))):
            st.image(a,815+i*145,336,130,155,second+i*.2,layer=27);st.text(label,815+i*145,458,140,55,22,start=second+i*.2)
    elif n==8:
        st.host(185,605,1.85,'explain','think',second)
        for i in range(3):
            st.image('rice',550+i*225,365,155+i*25,225+i*35,start=i*.7)
            st.text(('Gieo trồng','Chăm sóc','Chờ thu hoạch')[i],550+i*225,555,220,60,25,start=i*.7)
        st.shape('arrow',780,490,600,10,color='#9eae8d');st.image('calendar',1080,159,115,107,second)
        st.text('NHIỀU THÁNG CHỜ ĐỢI',775,122,760,70,34)
    elif n==9:
        st.text('MỘT MÙA VỤ CÓ THỂ THAY ĐỔI',size=34)
        st.image('rain',334,300,290,235);st.image('dry_earth',933,320,330,230)
        st.text('Mưa sai lúc',332,483,430,70,29);st.text('Khô hạn kéo dài',937,483,440,70,29)
        st.image('bowl',639,433,289,220,second,layer=30);st.text('Trong bát cơm là cả một mùa đợi chờ',640,587,1100,55,29,start=second)
    elif n==10:
        st.text('SỐNG CÙNG DÒNG SÔNG',size=37);st.image('river',810,403,800,440,layer=6)
        st.boat(721,394,1,72);st.image('net',1045,451,220,166,second)
        st.host(175,599,1.7,'point','explain',second)
    elif n==11:
        st.text('DẤU VẾT CỦA MỘT ĐỜI SỐNG SÔNG NƯỚC',size=32)
        for i,(a,label) in enumerate((('hook','Lưỡi câu'),('net','Lưới và vật dằn'),('boat','Thuyền'))):
            st.image(a,280+i*360,343,290,320,start=0 if i<2 else second)
            st.text(label,280+i*360,568,310,65,27,start=0 if i<2 else second)
    elif n==12:
        st.text('HÔM NAY, BỮA ĂN CÓ THÊM MỘT MÓN',size=33)
        st.image('river',388,397,650,370,layer=5);st.boat(356,392,.77,45)
        st.image('mother',909,397,167,228);st.image('child',1073,448,120,164)
        st.image('basket',781,472,190,171,second,layer=24);f=st.image('fish',776,423,140,100,second,layer=25);st.drift(f,'y',414,425,second,L)
    elif n==13:
        st.text('NƠI KIM LOẠI THÀNH ĐỒ DÙNG',size=36)
        st.host(190,600,1.95,'listen','point',second)
        st.image('furnace',804,393,385,350);st.image('adult',1062,392,180,246)
        f=st.image('flame',807,493,115,125,layer=23);st.oscillate(f,'scale',1,.05,1.5)
        st.image('smoke',800,198,90,169,opacity=.45);st.image('crucible',579,466,200,165,second)
    elif n==14:
        st.text('KHUÔN · LỬA · KINH NGHIỆM',size=37)
        for i,(a,label) in enumerate((('mold','Chuẩn bị khuôn'),('furnace','Kiểm soát lửa'),('crucible','Rót kim loại'))):
            st.image(a,280+i*360,340,270,270,start=i*.6);st.text(label,280+i*360,552,320,62,26,start=i*.6)
        st.shape('arrow',457,360,75,12);st.shape('arrow',818,360,75,12)
        st.text('Một sai sót có thể làm hỏng thành phẩm',640,605,1050,42,25,start=second,color='#9a5b47')
    elif n==15:
        st.text('TRỐNG ĐỒNG NGỌC LŨ',size=38)
        st.image('ngoc_lu_photo.jpg',334,380,500,390,layer=12)
        top=st.image('ngoc_lu_surface.svg',955,380,400,400,second,layer=15);st.drift(top,'rotation',0,-2.4,second,L)
        st.text('Ảnh: VuThiAnh · Public domain',333,605,530,35,15,font='Segoe UI',color='#767168')
        st.text('Hình vẽ: Ebaychatter0 · CC BY-SA 3.0',948,605,540,35,15,start=second,font='Segoe UI',color='#767168')
    elif n==16:
        st.host(180,600,1.9,'read','think',second)
        top=st.image('ngoc_lu_surface.svg',810,390,420,420,layer=14);st.drift(top,'scale',1,1.035)
        st.text('NHỮNG CON NGƯỜI TRONG HOA VĂN',795,123,830,70,31)
        st.text('Một thế giới lao động, lễ hội và sông nước',805,603,780,40,24)
        st.text('Ebaychatter0 · CC BY-SA 3.0',1080,579,270,25,13,font='Segoe UI',color='#817e76')
    elif n==17:
        st.text('MỘT DÁNG NGƯỜI GIÃ GẠO',size=38)
        st.image('pounder',555,376,220,300,layer=18);st.image('pounder_right',875,376,220,300,layer=18)
        st.image('mortar',710,505,210,176,layer=19)
        for x,angle in ((575,-28),(857,28)):
            o=st.image('pestle',x,291,120,312,layer=17,pivot=[0,-100]);st.oscillate(o,'rotation',angle,1,2.4)
        st.host(179,600,1.75,'point','welcome',second)
        st.note('Cảnh minh họa gợi từ đề tài giã gạo trên đồ đồng')
    elif n==18:
        st.text('KỸ THUẬT VÀ SỰ KIÊN NHẪN',size=37)
        st.image('ngoc_lu_surface.svg',369,386,430,430)
        st.host(950,600,2.15,'confident','question',second)
        st.text('Vẫn còn những câu hỏi…',970,164,470,50,27,start=second)
        st.text('Hình vẽ: Ebaychatter0 · CC BY-SA 3.0',362,605,540,35,15,font='Segoe UI',color='#767168')
    elif n==19:
        st.image('ngoc_lu_photo.jpg',825,390,630,400)
        st.host(200,600,2.05,'listen','explain',second)
        st.text('HIỆN VẬT IM LẶNG,\nCON NGƯỜI VẪN SỐNG ĐỘNG',810,126,780,100,30)
        st.note('Ảnh hiện vật: VuThiAnh · Public domain')
    elif n==20:
        st.text('RỜI NGÔI LÀNG · ĐẾN VỚI CỔ LOA',size=35)
        st.image('fortress',780,368,780,420);st.host(179,600,1.85,'point','question',second)
        st.text('THỜI ÂU LẠC',820,572,600,60,31)
        st.note('Sơ đồ gợi tả các vòng thành · không theo tỷ lệ')
    elif n==21:
        st.text('TRUYỀN THUYẾT ≠ CHỨNG CỨ KHẢO CỔ',size=31)
        st.image('turtle',292,283,250,200);st.image('crossbow',327,431,260,234)
        st.text('Nỏ thần · Rùa Vàng',320,590,490,55,28)
        st.image('excavation',930,359,470,355,second);st.text('1959 · CẦU VỰC',936,558,500,65,34,start=second,bold=True)
        st.shape('line',640,370,1,340,color='#dbd1c1',stroke=2)
    elif n==22:
        st.text('DẤU TÍCH CỦA MỘT NƠI CHẾ TÁC',size=35)
        for i,(a,label) in enumerate((('mold','Khuôn đúc'),('furnace','Dấu tích lò'),('arrowheads','Mũi tên đồng'))):
            st.image(a,280+i*360,351,280,300,start=i*.5);st.text(label,280+i*360,563,320,65,28,start=i*.5)
        st.text('CỔ LOA',640,605,500,40,26,color='#926b48')
    elif n==23:
        st.host(200,600,2.0,'disagree','explain',second)
        st.image('arrowhead',779,335,225,300);st.image('mold',1036,359,270,250,second)
        st.text('NĂNG LỰC CỦA CON NGƯỜI',827,125,800,70,35)
        st.text('Làm khuôn → Đúc → Cùng góp sức',842,575,760,70,27,start=second)
    elif n==24:
        st.text('AI LO BỮA ĂN CHO NGƯỜI THỢ?',size=37)
        for i,(a,label) in enumerate((('rice_field','Đồng ruộng'),('river','Bến sông'),('furnace','Nơi chế tác'))):
            st.image(a,280+i*360,325,300,270,start=i*.5);st.text(label,280+i*360,536,330,70,29,start=i*.5)
        for x in (458,818):st.shape('arrow',x,350,65,12,second,color='#a67650')
        st.text('Những cuộc sống nối vào nhau',640,606,900,45,27,start=second)
    elif n==25:
        st.text('LỊCH SỬ CỦA NHỮNG NGƯỜI KHÔNG TÊN',size=33)
        for i,(a,label) in enumerate((('mother','Giữ lửa'),('farmer','Làm ruộng'),('adult','Chế tác'),('child','Được chăm sóc'))):
            st.image(a,245+i*265,352,160,220,start=0 if i<2 else second);st.text(label,245+i*265,548,240,72,25,start=0 if i<2 else second)
        st.shape('line',640,494,1100,1,color='#d9cebb',stroke=2)
    elif n==26:
        st.text('CHIỀU XUỐNG, LẠI VỀ BÊN BẾP LỬA',size=33)
        st.image('stilt_house',1000,320,350,260,layer=5,opacity=.45)
        st.image('mother',455,390,220,300,layer=20);st.image('seated_child',842,470,145,198,layer=21);st.hearth(640,447,.9)
        st.image('bowl',1010,536,160,124,second);st.image('sun',1114,234,90,90,layer=4,opacity=.65)
    elif n==27:
        st.host(218,600,2.15,'question','think',second)
        st.shape('callout',865,354,610,300,fill='#fff9eb')
        st.text('ĐÂY LÀ PHẦN\nCHÚNG TA HÌNH DUNG',863,334,555,190,37)
        st.text('Người xưa đã mong điều gì?',865,557,650,70,31,start=second)
    elif n==28:
        st.text('MỘT MÙA GẶT · MỘT GIA ĐÌNH BÌNH AN',size=32)
        st.image('rice_field',700,400,1070,360,layer=6);st.image('mother',443,383,166,226);st.image('child',584,433,110,150)
        st.image('rice_sheaf',864,380,200,290,start=.4);st.image('rice_sheaf',1034,426,170,250,start=second)
        st.text('Ta không thể biết hết nỗi niềm riêng ấy',640,601,1000,45,25,start=second)
    elif n==29:
        st.text('NHỮNG VẬT NHỎ KỂ CHUYỆN LỚN',size=36)
        for i,(a,label) in enumerate((('sickle','Một lưỡi hái'),('mold','Một khuôn đúc'),('pounder','Một dáng người'))):
            st.image(a,280+i*360,350,270,290,start=i*.45);st.text(label,280+i*360,562,320,65,27,start=i*.45)
        st.text('Lao động · Đời sống thường ngày',640,607,900,40,26,start=second,color='#926b48')
    elif n==30:
        st.host(230,600,2.1,'welcome','listen',second)
        st.image('bowl',827,356,450,345);st.image('house',1082,280,175,160,layer=7)
        st.text('TRỞ VỀ BỮA CƠM HÔM NAY',815,126,830,75,35)
        st.text('Một ngày đủ đầy vẫn là điều ta mong',827,574,770,70,28,start=second)
    elif n==31:
        st.text('HƠN HAI NGHÌN NĂM,\nNHỮNG BÀN TAY VẪN VÌ NGÀY MAI',640,158,1120,140,38)
        st.image('hands',640,360,560,330);st.image('rice_sheaf',640,335,140,210,layer=21)
        st.host(189,600,1.7,'listen','welcome',second)
        st.text('MỘT NGÀY CÙNG NGƯỜI VIỆT CỔ',799,565,790,70,29,start=second)
        st.text('Ảnh Ngọc Lũ: VuThiAnh (PD) · Mặt trống: Ebaychatter0 (CC BY-SA 3.0)',799,606,790,28,13,start=second,font='Segoe UI',color='#7d776d')
    return st


def prepare():
    cues=read(DEST/'source'/'kich_ban_goc.srt');p=new_project('Một ngày cùng người Việt cổ · 5 phút',300,1920,1080)
    p.update(fps=30,audio_rate=48000,audio_channels=2,render_profile='final',scenes=[],audio=[],subtitles=[],duck_music=True)
    p['subtitle_style'].update(enabled=True,size=25,y=.978,color='#242424',background=False,font='Segoe UI')
    (DEST/'assets').mkdir(exist_ok=True);shutil.copy2(DEST/'narration.wav',DEST/'assets'/'narration.wav')
    for i in range(32):
        pair=cues[i*2:i*2+2];start=pair[0]['start'];end=pair[-1]['end'];s=new_scene(NAMES[i],end-start)
        s.update(start=start,background='white',style='ink',layout='custom',source_cues=[i*2+1,i*2+2],narration=' '.join(c['text'].replace('\n',' ') for c in pair))
        compose(i,s,pair);p['scenes'].append(s)
        p['audio'].append(dict(id=f'voice_{i+1}',name='Lời · '+NAMES[i],file=str(DEST/'assets'/'narration.wav'),start=start,trim=start,duration=end-start,group='voice',volume=1,scene_id=s['id']))
        p['subtitles'].extend({**c,'scene_id':s['id']} for c in pair)
    add_waveforms(p,DEST)
    if (DEST/'sound'/'original_soft_bed.m4a').exists():
        p['audio'].append(dict(id='music_original',name='Nền âm thanh tự tạo',file=str(DEST/'sound'/'original_soft_bed.m4a'),start=0,duration=300,group='music',volume=.65,fade_in=2,fade_out=3))
        for index in (0,2,10,12,24,28):
            s=p['scenes'][index];p['audio'].append(dict(id=f'river_{index}',name='Sông và chim · tự tạo',file=str(DEST/'sound'/'river_and_birds.m4a'),start=s['start'],duration=s['duration'],group='sfx',volume=.7,fade_in=.5,fade_out=.6,scene_id=s['id']))
        for index in (3,13,26):
            s=p['scenes'][index];p['audio'].append(dict(id=f'fire_{index}',name='Bếp lửa · tự tạo',file=str(DEST/'sound'/'quiet_hearth.m4a'),start=s['start'],duration=s['duration'],group='sfx',volume=.6,fade_in=.5,fade_out=.6,scene_id=s['id']))
        for index in (14,22):
            s=p['scenes'][index];p['audio'].append(dict(id=f'metal_{index}',name='Điểm nhấn kim loại · tự tạo',file=str(DEST/'sound'/'soft_metal.m4a'),start=s['start']+.5,duration=2.5,group='sfx',volume=.4,fade_in=.02,fade_out=.6,scene_id=s['id']))
    gaps=preflight(p,DEST);assert not gaps,gaps
    saved=save(p,DEST/'project.json',DEST);write(cues,DEST/'phu_de.srt')
    (DEST/'storyboard.json').write_text(json.dumps(dict(name=p['name'],timing='Original SRT clock, exact 300 seconds',shots=[dict(number=i+1,title=s['name'],start=s['start'],end=s['start']+s['duration'],source_cues=s['source_cues'],text=s['narration']) for i,s in enumerate(p['scenes'])]),ensure_ascii=False,indent=2),encoding='utf-8')
    print('PROJECT READY:',len(p['scenes']),'scenes,',len(p['subtitles']),'original cues,',sum(len(s['objects']) for s in p['scenes']),'editable layers')
    return saved


if __name__=='__main__':prepare()
