from pathlib import Path
import json,csv,zipfile,shutil,hashlib,struct,textwrap
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, Polygon
from PIL import Image,ImageOps,ImageDraw,ImageFont

ROOT=Path(__file__).parent
OUT=ROOT/'output/Mo_Den_Maya_Tu_Lieu_That_Va_Phan_Canh_v1'
for d in ['01_Tu_lieu_that','02_Do_hoa_SVG_PNG','03_Phan_canh','04_Nguon_va_quyen','05_Xem_nhanh','06_Du_lieu_va_ma_nguon']:(OUT/d).mkdir(parents=True,exist_ok=True)
def write(p,s): (OUT/p).write_text(s,encoding='utf-8')
def js(p,o):write(p,json.dumps(o,ensure_ascii=False,indent=2))
def table(p,rows):
 with (OUT/p).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v for k,v in a.items()} for a in rows)

sources={
 'S01':('Lọc nước tại Corriental — Tankersley và cộng sự, 2020','https://doi.org/10.1038/s41598-020-75023-7'),
 'S02':('Ô nhiễm hồ Tikal — Lentz và cộng sự, 2020','https://doi.org/10.1038/s41598-020-67044-z'),
 'S03':('Ước tính lượng mưa — Evans và cộng sự, 2018','https://doi.org/10.1126/science.aas9871'),
 'S04':('Hạn hán Tây Bắc Yucatán — James và cộng sự, 2025','https://doi.org/10.1126/sciadv.adw7661'),
 'S05':('Hồ sơ Itzan — Gwinneth và cộng sự, 2025','https://doi.org/10.5194/bg-22-7079-2025'),
 'S06':('Chiến tranh Witzna — Wahl và cộng sự, 2019','https://doi.org/10.1038/s41562-019-0671-x'),
 'S07':('Chính trị và đô thị — Arnauld, Méreuze, Hiquet, 2026; đã đối chiếu tóm tắt','https://doi.org/10.1017/laq.2026.10180'),
 'S08':('Mayapán — Kennett và cộng sự, 2022','https://doi.org/10.1038/s41467-022-31522-x'),
 'S09':('Lịch Maya và 2012 — Smithsonian NMAI','https://maya.nmai.si.edu/2012-resetting-count/meaning-of-2012'),
 'S10':('Natural Earth — ranh giới hiện đại 1:110m, public domain','https://www.naturalearthdata.com/about/terms-of-use/'),
 'S11':('Tikal — UNESCO','https://whc.unesco.org/en/list/64/'),
 'S12':('Chichén Itzá — UNESCO','https://whc.unesco.org/en/list/483/'),
 'S13':('Tọa độ Mayapán — nghiên cứu mẫu đồng vị tại di tích','https://pmc.ncbi.nlm.nih.gov/articles/PMC5091867/'),
}
license_urls={'CC0':'https://creativecommons.org/publicdomain/zero/1.0/','CC BY 4.0':'https://creativecommons.org/licenses/by/4.0/','CC BY-SA 4.0':'https://creativecommons.org/licenses/by-sa/4.0/','CC BY-SA 3.0':'https://creativecommons.org/licenses/by-sa/3.0/','Public Domain':'https://www.usgs.gov/information-policies-and-instructions/copyrights-and-credits'}
meta=[
 ('R01_Tikal_forest.jpg','Tikal: đền trên tán rừng','Gary Todd','2002-04-04','CC0','https://commons.wikimedia.org/wiki/File:Tikal_Temples_I,_II,_III,_%26_Lost_World_(10514930314).jpg','Ảnh di tích','Toàn cảnh Tikal, Guatemala. Không phải thành phố nguyên trạng thời Cổ điển.'),
 ('R02_Tikal_Temple_I.jpg','Tikal: Đền I','Kaldari','2015-06-26','CC0','https://commons.wikimedia.org/wiki/File:Tikal_Temple_I_01.jpg','Ảnh di tích','Ảnh đứng; giữ nguyên tỷ lệ, đặt trên nền màu khi dựng ngang.'),
 ('R03_Tzutujil_weaving_2019.jpg','Người Tz’utujil dệt vải','Chelalinda','2019-10-06','CC BY-SA 4.0','https://commons.wikimedia.org/wiki/File:Tzutujil.weaving.jpg','Ảnh đời sống','Guatemala, ảnh năm 2019. Không gọi đây là cảnh quay hôm nay; không khái quát mọi cộng đồng Maya.'),
 ('R04_Mayapan_panorama.jpg','Toàn cảnh di tích Mayapán','SiMeCaIS','2008-06-07','CC BY-SA 3.0','https://commons.wikimedia.org/wiki/File:Mayapan_Panorama.JPG','Ảnh di tích','Di tích khảo cổ Mayapán; ảnh panorama, dùng pan ngang chậm.'),
 ('R05_Chichen_Itza.jpg','Đền Kukulkán, Chichén Itzá','Gary Todd','2001-02-11 (ngày theo trang nguồn)','CC0','https://commons.wikimedia.org/wiki/File:Chichen_Itza_Temple_of_Kukulkan_(16302060359).jpg','Ảnh di tích','Không dùng thay Tikal hoặc Witzna.'),
 ('R06_Mayan_weaver_2023.jpg','Dệt vải tại San Antonio Palopó','Aandhu','2023-04-09','CC BY 4.0','https://commons.wikimedia.org/wiki/File:Mayan_Weaver.jpg','Ảnh đời sống','Guatemala, ảnh năm 2023; ảnh hoạt động trình diễn dệt. Không biến ảnh thành nhân vật AI nói chuyện.'),
 ('R07_Tikal_stele.jpg','Bia đá tại Tikal','Gary Todd','2002-04-04','CC0','https://commons.wikimedia.org/wiki/File:Tikal_Stele_(9791223315).jpg','Ảnh di tích','Chỉ minh họa bia đá Tikal; tuyệt đối không gắn nhãn bia Witzna hoặc văn khắc ghi năm 697.'),
 ('E01_Witzna_charcoal.png','Lớp than trong lõi trầm tích Laguna Ek’Naab','Dave Wahl / USGS','khoảng 04/2020','Public Domain','https://www.usgs.gov/media/images/section-laguna-eknaab-sediment-core','Bằng chứng nghiên cứu','Lớp than dày 3 cm. Tuổi có xác suất cao nhất theo mô hình là 692 CN; không đồng nhất phép định tuổi này với năm 697 trong văn khắc.'),
 ('E02_Witzna_cores.jpg','Các lõi trầm tích Laguna Ek’Naab','Dave Wahl / USGS','2014-12-26 (trang nguồn)','Public Domain','https://www.usgs.gov/media/images/sediment-cores-laguna-eknaab-guatemala','Ảnh mẫu nghiên cứu','Lõi trầm tích từ hồ gần Witzna, không phải ảnh phế tích Witzna.'),
 ('E03_zeolite_fig1.jpg','Bản đồ và LiDAR các hồ Tikal — Figure 1','Tankersley và cộng sự; LiDAR: Francisco Estrada-Belli / PACUNAM; GIS: Christopher Carr','2020','CC BY 4.0','https://pmc.ncbi.nlm.nih.gov/articles/PMC7582844/','Hình nghiên cứu','Định vị hồ Corriental. Bản tải có độ phân giải thấp, ưu tiên inset; không phóng to toàn màn hình 4K.'),
 ('E03_zeolite_fig3.jpg','Địa tầng, zeolite và ảnh mẫu — Figure 3','Tankersley và cộng sự','2020','CC BY 4.0','https://pmc.ncbi.nlm.nih.gov/articles/PMC7582844/','Hình nghiên cứu','Đây là hình phân tích mẫu thực, không phải ảnh toàn bộ hệ thống lọc còn nguyên.'),
 ('E03_zeolite_fig4.jpg','Giả thuyết cấu tạo bộ lọc — Figure 4','Tankersley và cộng sự','2020','CC BY 4.0','https://pmc.ncbi.nlm.nih.gov/articles/PMC7582844/','Sơ đồ nghiên cứu','PHẢI ghi: sơ đồ giả thuyết theo nghiên cứu. Không trình bày như kết cấu đã được khai quật nguyên vẹn.'),
 ('E06_pollution_fig4.jpg','Dữ liệu vi khuẩn lam ở bốn hồ — Figure 4','Lentz và cộng sự','2020','CC BY 4.0','https://pmc.ncbi.nlm.nih.gov/articles/PMC7316703/','Hình nghiên cứu','Không phải ảnh nước thời cổ. Giữ chú giải và tên hồ; chỉ dùng inset để giới thiệu phương pháp.'),
 ('E07_drought2025_fig2.jpg','Thạch nhũ Tzab06-1 và chuỗi đồng vị — Figure 2','James và cộng sự','2025','CC BY 4.0','https://pmc.ncbi.nlm.nih.gov/articles/PMC12346346/','Hình nghiên cứu','Mẫu thực trong hang Tzabnah. Năm 929–942 (±6) CN; 13 năm hạn không có nghĩa không có giọt mưa nào.'),
 ('E08_Itzan_fig1.png','Địa hình và lượng mưa hiện đại — Figure 1','Gwinneth, Johnston, Breckenridge và Douglas','2025','CC BY 4.0','https://bg.copernicus.org/articles/22/7079/2025/','Hình nghiên cứu','Lớp mưa là 1989–2019, KHÔNG phải bản đồ hạn hán thời Maya.'),
 ('E08_Itzan_fig3.png','Đối chiếu hồ sơ đồng vị bốn hồ — Figure 3','Gwinneth, Johnston, Breckenridge và Douglas','2025','CC BY 4.0','https://bg.copernicus.org/articles/22/7079/2025/','Hình nghiên cứu','Không thấy tín hiệu khô hạn tương ứng tại Itzan trong hồ sơ này; không suy rộng thành mọi mùa ở đây đều đủ mưa.'),
]
direct=dict(json.loads((ROOT/'maya_work/download_jobs.json').read_text()))
direct.update({'R01_Tikal_forest.jpg':'https://upload.wikimedia.org/wikipedia/commons/f/f1/Tikal_Temples_I%2C_II%2C_III%2C_%26_Lost_World_%2810514930314%29.jpg','R02_Tikal_Temple_I.jpg':'https://upload.wikimedia.org/wikipedia/commons/c/c2/Tikal_Temple_I_01.jpg','R03_Tzutujil_weaving_2019.jpg':'https://upload.wikimedia.org/wikipedia/commons/0/0e/Tzutujil.weaving.jpg','R04_Mayapan_panorama.jpg':'https://upload.wikimedia.org/wikipedia/commons/5/5f/Mayapan_Panorama.JPG'})
assets=[]
for filename,title,author,date,lic,url,kind,note in meta:
 p=OUT/'01_Tu_lieu_that'/filename;shutil.copy2(ROOT/'maya_work/photos'/filename,p)
 im=Image.open(p)
 assets.append(dict(id=p.stem,file=str(p.relative_to(OUT)),title=title,author=author,date=date,type=kind,license=lic,license_url=license_urls[lic],source_url=url,download_url=direct[filename],downloaded_on='2026-10-21',width=im.width,height=im.height,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),notes=note,credit=f'{title} — {author} — {lic}. Nguồn: {url}',modifications_in_package='Không chỉnh sửa ảnh gốc; contact sheet là bản thu nhỏ.'))
js('04_Nguon_va_quyen/ASSET_REGISTRY.json',assets);table('04_Nguon_va_quyen/ASSET_REGISTRY.csv',assets)

inventory=[]
for pattern,manifest in [('*150*zip','DANH_MUC_ANH.json'),('*48*zip','danh_muc_48_anh.json')]:
 zpath=next((ROOT/'upload').glob(pattern));z=zipfile.ZipFile(zpath)
 m=next(n for n in z.namelist() if n.endswith('/'+manifest));data=json.loads(z.read(m));data=data.get('items',[]) if isinstance(data,dict) else data
 for a in data:
  inventory.append(dict(id=f"I{int(a['id']):03}",name=a.get('name_vi',a.get('ten_tieng_viet')),zip_file=zpath.name,zip_member=m.rsplit('/',1)[0]+'/'+a['file'],sha256=a['sha256'],type='Minh họa do dự án cung cấp; không phải ảnh tư liệu'))
assert len(inventory)==198
js('03_Phan_canh/198_ANH_CU_MANIFEST.json',inventory)

# Đồ họa gốc, 1920x1080. SVG giữ chữ có thể sửa, PNG để dựng ngay.
plt.rcParams.update({'font.family':'DejaVu Sans','svg.fonttype':'none','font.size':24,'text.color':'#362d26','axes.labelcolor':'#362d26'})
CREAM='#f6efdf';INK='#362d26';TEAL='#397d83';RUST='#b85e3c';MUTED='#7f8060'
graphics=[]
def canvas(title,sub):
 f=plt.figure(figsize=(19.2,10.8),dpi=100,facecolor=CREAM);a=f.add_axes([0,0,1,1]);a.set(xlim=(0,1920),ylim=(1080,0));a.axis('off')
 a.text(100,105,title,fontsize=36,weight='bold',va='center');a.text(100,165,sub,fontsize=20,va='center',color='#6a6458');return f,a
def txt(a,x,y,s,size=25,**kw):a.text(x,y,s,fontsize=size,va='center',**kw)
def box(a,x,y,w,h,label,color=TEAL):
 a.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0,rounding_size=18',facecolor=color,edgecolor='none'))
 txt(a,x+w/2,y+h/2,label,26,color='white',ha='center')
def arrow(a,x1,y1,x2,y2):a.annotate('',xy=(x2,y2),xytext=(x1,y1),arrowprops={'arrowstyle':'-|>','lw':4,'color':INK})
def save(f,a,id,title,source,note):
 txt(a,100,1000,source,16,color='#6a6458')
 for ext in ['svg','png']:f.savefig(OUT/'02_Do_hoa_SVG_PNG'/f'{id}.{ext}',dpi=100,facecolor=CREAM)
 plt.close(f);graphics.append(dict(id=id,title=title,svg=f'02_Do_hoa_SVG_PNG/{id}.svg',png=f'02_Do_hoa_SVG_PNG/{id}.png',source=source,notes=note))

f,a=canvas('Những nơi được nhắc trong câu chuyện','Bản đồ định vị khu vực • ranh giới quốc gia hiện đại, không phải biên giới Maya cổ')
ma=f.add_axes([.07,.17,.57,.63],facecolor='#e3eeeb')
z=zipfile.ZipFile(ROOT/'maya_work/research/naturalearth_countries.zip');raw=z.read(next(n for n in z.namelist() if n.endswith('.shp')))
pos=100
while pos<len(raw):
 n,words=struct.unpack('>ii',raw[pos:pos+8]);b=raw[pos+8:pos+8+words*2];pos+=8+words*2
 if struct.unpack('<i',b[:4])[0]!=5:continue
 nparts,npoints=struct.unpack('<ii',b[36:44]);parts=list(struct.unpack('<'+'i'*nparts,b[44:44+4*nparts]))+[npoints];off=44+4*nparts;points=[struct.unpack('<dd',b[off+16*i:off+16*i+16]) for i in range(npoints)]
 for k in range(nparts):ma.add_patch(Polygon(points[parts[k]:parts[k+1]],facecolor='#d7d3ae',edgecolor='#8d917d',lw=1))
ma.set_xlim(-94,-86);ma.set_ylim(14,22);ma.set_aspect(1/.95);ma.tick_params(labelsize=13);ma.grid(alpha=.12)
places=[('Tikal',17.22,-89.62,(-.8,.35),'S11'),('Chichén Itzá',20.68,-88.57,(-.3,.5),'S12'),('Mayapán',20.63,-89.46,(-2,.1),'S13'),('Hồ Itzan',16.598,-90.4784,(-2,-.35),'S05')]
for label,lat,lon,(dx,dy),s in places:
 ma.plot(lon,lat,'o',color=RUST,ms=8);ma.annotate(label,(lon,lat),(lon+dx,lat+dy),fontsize=17,arrowprops={'arrowstyle':'-','color':INK})
for x,y,t in [(-91,19.2,'MEXICO'),(-90,14.8,'GUATEMALA'),(-87.8,17.1,'BELIZE')]:ma.text(x,y,t,fontsize=13,color='#666b5d',ha='center')
txt(a,1310,330,'BÁN ĐẢO YUCATÁN',25,weight='bold');txt(a,1310,435,'Witzna: đông bắc Petén,\nGuatemala.',23)
txt(a,1310,580,'Chưa đặt ghim Witzna:\nkhông suy đoán tọa độ\ntừ bản đồ minh họa.',20)
txt(a,1310,755,'Hồ Itzan: điểm lấy mẫu.\nCác di tích: vị trí xấp xỉ\nđể định hướng khu vực.',20)
save(f,a,'G01_Ban_do','Bản đồ khu vực','Natural Earth 1:110m (public domain) • Tikal/Chichén: UNESCO • Mayapán: S13 • Hồ Itzan: S05','Không có tuyến di cư, tuyến nước hoặc biên giới cổ trên bản đồ này.')
js('06_Du_lieu_va_ma_nguon/map_points.json',[dict(name=n,latitude=lat,longitude=lon,source_id=s,precision='approximate site / exact reported lake sampling coordinate for Itzan') for n,lat,lon,off,s in places])
shutil.copy2(ROOT/'maya_work/research/naturalearth_countries.zip',OUT/'06_Du_lieu_va_ma_nguon/naturalearth_countries.zip')

f,a=canvas('Không có một thời điểm kết thúc duy nhất','Các mốc chọn lọc • năm Công nguyên • trục thời gian theo tỷ lệ')
x=lambda v:180+(v-250)/1250*1560
a.plot([x(250),x(1500)],[770,770],color=INK,lw=3)
for year in [250,500,750,1000,1250,1500]:a.plot([x(year),x(year)],[760,780],color=INK);txt(a,x(year),820,str(year),20,ha='center')
a.add_patch(Rectangle((x(250),300),x(900)-x(250),85,color=TEAL));txt(a,x(250)+25,342,'Cổ điển: khoảng 250–900',24,color='white')
a.add_patch(Rectangle((x(1200),425),x(1450)-x(1200),85,color=MUTED));txt(a,x(1325),468,'Mayapán\n1200–1450',21,color='white',ha='center')
a.plot([x(697),x(697)],[420,750],color=RUST,lw=3);txt(a,x(697)-25,565,'697\nVăn khắc về\ncuộc tấn công Witzna',21,ha='right')
a.plot([x(929),x(942)],[640,640],color=RUST,lw=9);txt(a,x(935)+35,640,'929–942 (±6)\nĐợt hạn trong hồ sơ Tzabnah',21)
txt(a,180,905,'Sau các mốc này, lịch sử và các cộng đồng Maya vẫn tiếp tục.',25,weight='bold')
save(f,a,'G02_Truc_thoi_gian','Trục thời gian','Nguồn: S06 Wahl et al. (2019) • S04 James et al. (2025) • S08 Kennett et al. (2022) • niên đại khái quát theo kịch bản','250–900 là phân kỳ khái quát; không phải ngày bắt đầu/kết thúc đồng loạt.')

f,a=canvas('Nước đến hồ bằng cách nào?','Sơ đồ nguyên lý để giải thích • không phải mặt bằng khai quật hay tuyến nước đo đạc')
for x0,label in [(120,'Mưa'),(560,'Bề mặt thu nước'),(1000,'Dòng chảy'),(1440,'Hồ chứa')]:box(a,x0,330,340,150,label)
for x0 in [460,900,1340]:arrow(a,x0,405,x0+100,405)
box(a,1000,610,780,170,'Corriental: bằng chứng quartz + zeolite\nGợi ý hệ thống lọc theo nghiên cứu',MUTED)
arrow(a,1170,490,1170,600)
txt(a,130,650,'Hồ tốt vẫn cần nước đầu vào.',30,weight='bold');txt(a,130,745,'Không gộp Corriental với các hồ\nTemple và Palace bị ô nhiễm.',24)
save(f,a,'G03_Nuoc_Tikal','Sơ đồ nước','Nguồn: S01 Tankersley et al. (2020) • S02 Lentz et al. (2020) • đồ họa diễn giải mới','Mũi tên là dòng nguyên lý, không mô tả dòng chảy có tọa độ.')

f,a=canvas('Lượng mưa giảm bao nhiêu?','Hồ Chichancanab • ước tính từ nghiên cứu năm 2018 • so với mức hiện đại trong mô hình')
ax=f.add_axes([.11,.36,.78,.25]);ax.set_facecolor(CREAM);ax.set_xlim(0,100);ax.set_ylim(0,1);ax.set_yticks([]);ax.set_xticks([0,20,40,60,80,100]);ax.tick_params(labelsize=22);ax.set_xlabel('Mức giảm lượng mưa (%)',fontsize=24,labelpad=20)
for spine in ['left','right','top']:ax.spines[spine].set_visible(False)
ax.plot([41,54],[.45,.45],color=RUST,lw=32,solid_capstyle='butt');ax.text(47.5,.85,'41–54%',ha='center',fontsize=42,weight='bold',color=RUST)
txt(a,210,820,'Đây là một khoảng ước tính cho khu vực nghiên cứu.',28,weight='bold');txt(a,210,885,'Không phải đường mưa từng năm hay con số áp dụng cho toàn vùng Maya.',23)
save(f,a,'G04_Mua_41_54','Khoảng giảm mưa','Nguồn: S03 Evans et al. (2018), Science • DOI: 10.1126/science.aas9871','Chỉ vẽ khoảng công bố; không gọi đây là khoảng tin cậy nếu bài báo không định nghĩa như vậy.')

f,a=canvas('Mười ba năm là nhiều mùa vụ nối tiếp','Hồ sơ thạch nhũ Tzab06-1, hang Tzabnah • Tây Bắc Yucatán • nghiên cứu 2025')
txt(a,140,345,'13 năm',80,color=RUST,weight='bold');txt(a,900,345,'Khoảng 929–942 CN\nSai số niên đại: ±6 năm',30)
for i in range(13):a.add_patch(Rectangle((145+i*125,510),105,115,facecolor=RUST,edgecolor='none'))
txt(a,145,700,'13 ô minh họa độ dài đợt hạn; không biểu diễn lượng mưa của từng năm.',23)
txt(a,145,815,'Hạn kéo dài không có nghĩa là hoàn toàn không có mưa.',28,weight='bold')
save(f,a,'G05_13_nam','Độ dài đợt hạn','Nguồn: S04 James et al. (2025), Science Advances • DOI: 10.1126/sciadv.adw7661','Niên đại có bất định; không đồng nhất với giai đoạn của mọi thành phố Maya.')

f,a=canvas('Itzan buộc chúng ta hỏi thêm','Đối chiếu bằng chứng địa phương • không phải biểu đồ lượng mưa hoặc dân số mới')
box(a,130,310,760,220,'Hồ sơ khí hậu tại Itzan\nKhông thấy tín hiệu khô hạn\ntương ứng trong dữ liệu này',TEAL)
box(a,1030,310,760,220,'Bối cảnh khảo cổ\nDân số địa phương\nvẫn suy giảm',RUST)
arrow(a,510,550,810,700);arrow(a,1410,550,1110,700)
box(a,500,720,920,145,'Cần xét thêm chiến tranh, liên kết vùng\nvà những sức ép khác — chưa chốt nguyên nhân',MUTED)
save(f,a,'G06_Itzan','Đối chiếu Itzan','Nguồn: S05 Gwinneth et al. (2025), Biogeosciences • DOI: 10.5194/bg-22-7079-2025','Không có tín hiệu trong hồ sơ không đồng nghĩa chứng minh không từng có mùa khô.')

f,a=canvas('Witzna: các bằng chứng gặp nhau','Hai loại niên đại cần được phân biệt')
box(a,120,310,780,270,'Lõi trầm tích Laguna Ek’Naab\nLớp than dày 3 cm\nTuổi có xác suất cao nhất: 692 CN\n(theo mô hình niên đại)',TEAL)
box(a,1020,310,780,270,'Văn khắc\nGhi cuộc tấn công\nNăm 697 CN',RUST)
arrow(a,500,600,810,735);arrow(a,1410,600,1110,735)
txt(a,960,800,'Đặt cạnh nhau để đối chiếu — không coi là cùng một phép đo.',27,ha='center',weight='bold')
save(f,a,'G07_Witzna','Bằng chứng Witzna','Nguồn: USGS, Section of Laguna Ek’Naab Sediment Core • S06 Wahl et al. (2019)','692 là đỉnh xác suất mô hình; 697 là năm văn khắc. Không dựng ảnh cháy như tư liệu ghi hình.')

f,a=canvas('Cung điện im tiếng, đời sống chưa hẳn kết thúc','Sơ đồ phân biệt khái niệm • không phải hai đường dân số được đo')
box(a,150,310,650,170,'Dấu vết quyền lực\nBia mới • công trình triều đình',RUST)
box(a,1120,310,650,170,'Dấu vết đời sống\nNhà ở • sản xuất • trao đổi',TEAL)
txt(a,960,395,'≠',70,ha='center')
txt(a,160,655,'Ít văn khắc hơn không tự chứng minh cả đô thị đã hết người.',30,weight='bold')
txt(a,160,785,'Cần đối chiếu nhiều loại bằng chứng và từng địa điểm cụ thể.',26)
save(f,a,'G08_Chinh_tri_Doi_song','Quyền lực và đời sống','Nguồn: S07 Arnauld, Méreuze & Hiquet (2026), Latin American Antiquity • dựa trên tóm tắt công bố','Đồ họa giải thích khái niệm; không tái tạo đồ thị từ toàn văn chưa đọc.')
js('04_Nguon_va_quyen/GRAPHICS_REGISTRY.json',graphics)
js('06_Du_lieu_va_ma_nguon/chart_data.json',{'rainfall_reduction_pct':[41,54],'rainfall_source':'S03','drought_duration_years':13,'drought_interval_ce':[929,942],'dating_uncertainty_years':6,'drought_source':'S04','annual_rainfall_values':None,'population_time_series':None})

# Hai nhịp hình trong mỗi đoạn, bám cue; không khóa vào audio cũ.
specs=[
 ('R01_Tikal_forest','G03_Nuoc_Tikal','Từ tán rừng tới dấu tích đô thị','Đặt câu hỏi về nước bằng sơ đồ','Pan rất chậm trên ảnh thật; cắt sang sơ đồ khi lời nhắc nước.','Không vẽ Tikal đầy người từ ảnh tư liệu.'),
 ('I172,I001','I173,I004','Một ngôi nhà vẫn đang có người sống','Gói đồ như một lựa chọn khó','Cho bình nước và túi đồ lần lượt xuất hiện; không tự dựng nhân vật lịch sử.','Ghi “Tình huống giả định”.'),
 ('G01_Ban_do','G02_Truc_thoi_gian','Định vị các thành phố','Phân biệt thời kỳ và các mốc','Làm nổi từng nhãn theo lời; timeline chạy con trỏ, không làm các thành phố tắt cùng lúc.','Bản đồ dùng ranh giới hiện đại.'),
 ('I151','I157,I158','Đô thị và năng lực xây dựng','Kỹ thuật có giới hạn nguồn cung','Từ toàn cảnh xuống hồ; có thể tạo mask mực nước trên một bố cục cố định.','Không giả rằng ba ảnh là các frame khớp nhau.'),
 ('R02_Tikal_Temple_I','I001,I157','Đền có thể chờ','Nước uống là nhu cầu trước mắt','Giữ ảnh đền trong khung đứng rồi cắt sang bình nước.','Không kéo giãn ảnh đứng.'),
 ('R01_Tikal_forest','G03_Nuoc_Tikal','Rừng xanh không bảo đảm nước quanh năm','Mưa, bề mặt thu nước, hồ chứa','Reveal từng mũi tên; chuyển động giọt nước theo đường nguyên lý.','Không dùng đây như bản vẽ hệ thống Tikal chính xác.'),
 ('E03_zeolite_fig3','I184,I185,E03_zeolite_fig4','Cho thấy bằng chứng vật liệu','Phân biệt mẫu thực và cấu tạo giả thuyết','Inset hình mẫu có nguồn; phóng hình minh họa khoáng vật, không phóng ảnh mẫu quá độ.','Figure 4 phải giữ nhãn giả thuyết.'),
 ('I197','I158,I159','So sánh với bồn nước hiện đại','Bể chứa không tạo thêm mưa','Tách màn bằng nhãn “Ví dụ hiện đại”; dùng mực nước hạ trong đồ họa.','I197 không phải dụng cụ Maya cổ.'),
 ('I158','I193,I195','Chuyển câu hỏi từ lượng sang chất','Nước còn lại có an toàn không','Zoom nhẹ vào mặt nước minh họa; thêm dấu hỏi.','Không biến màu nước minh họa thành quan sát khảo cổ.'),
 ('E06_pollution_fig4','I186,I194','Tư liệu phân tích bốn hồ','Giải thích khả năng đường ô nhiễm','Giữ figure như bằng chứng nghiên cứu; chuyển sang hạt màu và dòng chảy minh họa.','Đặt tên Temple/Palace; không suy luận tất cả hồ Tikal cùng độc.'),
 ('G03_Nuoc_Tikal','I158,I193','Nhắc giới hạn của kết luận','Áp lực thiếu và ô nhiễm nước','Giữ hai nhãn “Lượng nước” và “Chất lượng”; không thêm tỷ lệ tử vong.','Không có dữ liệu để kết luận nguyên nhân trực tiếp từng người rời đi.'),
 ('I001,I138','I128,I001','Đi tìm nước ảnh hưởng đời sống','Ai tiếp cận được nước','Di chuyển biểu tượng bình nước dọc một lối đi giả định; dừng ở ngã rẽ.','Ghi “Minh họa tình huống”, không vẽ tuyến đi thật trên bản đồ.'),
 ('E02_Witzna_cores','E07_drought2025_fig2,I187,I188,I189','Các dạng mẫu lưu dấu quá khứ','Từ mẫu tới ước tính khí hậu','Ảnh lõi trầm tích phải ghi địa điểm; sau đó thạch nhũ thật và minh họa gypsum.','Lõi Witzna không phải mẫu gypsum Chichancanab.'),
 ('G04_Mua_41_54','G04_Mua_41_54','Hiện khoảng 41–54%','Giữ địa điểm và giới hạn áp dụng','Animate thanh phạm vi từ 41 đến 54 rồi giữ; không tạo đường mưa giả.','Không xóa cụm “khu vực nghiên cứu”.'),
 ('E07_drought2025_fig2','G05_13_nam','Mẫu thạch nhũ và bài nghiên cứu','13 ô là 13 năm thời lượng','Inset figure, sau đó đếm ô đều theo lời; không coi mỗi ô có số mm mưa.','Giữ khoảng năm và ±6 năm.'),
 ('I163,I164','I166,I167,I192','Ruộng ngô mất sức','Lương thực dự trữ ít đi','Dùng lớp cây và bao hạt tách riêng; giảm lượng biểu tượng, không gán dữ liệu năng suất.','Đây là tình huống minh họa, không phục dựng một hộ gia đình thật.'),
 ('G01_Ban_do','G06_Itzan','Chuyển địa điểm về Itzan','Nêu điều không khớp với lời giải đơn giản','Làm sáng nhãn hồ Itzan; hai hộp bằng chứng xuất hiện lần lượt.','Điểm trên bản đồ là hồ lấy mẫu.'),
 ('E08_Itzan_fig3','G06_Itzan','Hồ sơ đồng vị và giới hạn','Mở câu hỏi về liên kết vùng','Giữ figure toàn vẹn trong inset; không vẽ lại dữ liệu bằng mắt.','E08 Figure 1 là khí hậu hiện đại, không dùng làm bản đồ hạn cổ.'),
 ('I169,I075','I170,I155','Nơi có nước vẫn cần nơi khác','Đường gián đoạn, chợ ít hàng','Di chuyển kiện hàng trên một đường sơ đồ; dừng khi đường bị chặn.','Sơ đồ quan hệ giả định, không tuyến thương mại được xác lập.'),
 ('E02_Witzna_cores,E01_Witzna_charcoal','G07_Witzna','Lõi trầm tích và dấu than','Đặt văn khắc 697 cạnh định tuổi lõi','Giữ ảnh rõ; dùng khung ngoài đánh dấu vùng than, không sửa thanh dữ liệu.','Không dùng R07 như văn khắc Witzna.'),
 ('G02_Truc_thoi_gian','I175,I176','Đặt 697 trước các mốc khủng hoảng sau','Một trường hợp chiến tranh cụ thể','Con trỏ tới697; cảnh cháy minh họa xuất hiện có nhãn rõ.','Không coi bối cảnh175–177 là phục dựng chính xác Witzna.'),
 ('I177,I170','I155,I182','Sau trận đánh: hạ tầng và đường đi','Hợp tác để duy trì đời sống','Dùng dấu ngắt trên đường; tô sáng đập nước như việc cần bảo trì.','Không thêm vũ khí hoặc cảnh tử vong không có căn cứ.'),
 ('R07_Tikal_stele','G08_Chinh_tri_Doi_song','Bia đá là một loại dấu vết','Quyền lực suy yếu khác với hết dân','Ảnh bia Tikal có nhãn địa điểm; chuyển sang hai loại bằng chứng.','Không dịch chữ trên bia từ ảnh này.'),
 ('I178,I179','I172,I154','Cung điện xuống cấp','Sinh hoạt vẫn có thể tiếp tục','Giữ bố cục khái niệm: cung điện mờ, nhà ở và chợ còn sáng.','Không gán mức dân số cụ thể cho minh họa.'),
 ('I173,I004','I174,I128','Một cuộc rời đi','Hai cách nhìn: mất thành phố, giữ gia đình','Túi đồ di chuyển ra ngoài khung; ngôi nhà còn lại.','Giữ nhãn giả định; không tự dựng tiểu sử người có thật.'),
 ('R05_Chichen_Itza','G02_Truc_thoi_gian','Chichén Itzá: câu chuyện tiếp diễn','Lịch sử không dừng sau thời Cổ điển','Reveal ảnh từ toàn cảnh, sau đó mở thêm khoảng thời gian.','Không nói mọi người Tikal đều chuyển tới Chichén Itzá.'),
 ('R04_Mayapan_panorama','G02_Truc_thoi_gian','Mayapán thật','Thế kỷ sau vẫn có trung tâm lớn','Pan ngang panorama; làm nổi dải1200–1450.','Tách bối cảnh Mayapán khỏi Witzna/Tikal.'),
 ('G02_Truc_thoi_gian','I124,I126','Tách thời thuộc địa khỏi khủng hoảng Cổ điển','Thẻ chữ về một chương lịch sử khác','Mở rộng trục bằng thẻ chữ theo đúng lời đọc; không dựng cảnh chinh phục giả làm tư liệu.','Mốc1697 theo kịch bản; cần đối chiếu nguồn lịch sử trước khi thêm bản đồ chiến dịch.'),
 ('R03_Tzutujil_weaving_2019','R06_Mayan_weaver_2023','Người Tz’utujil đang dệt, ảnh2019','Dệt tại San Antonio Palopó, ảnh2023','Giữ người và bối cảnh nguyên vẹn; pan/crop nhẹ, ghi năm ảnh.','Không AI làm người trong ảnh nói, cười hoặc thực hiện động tác mới.'),
 ('R02_Tikal_Temple_I','R06_Mayan_weaver_2023','Từ phế tích','Đổi góc nhìn sang con người','Match cut bằng nhịp kể, không ám chỉ người trong ảnh là hậu duệ của một di tích cụ thể.','Không gọi cộng đồng đang sống là tàn dư đã mất.'),
 ('I198','I198,I123','Ví dụ lịch hiện đại','Kết thúc chu kỳ không phải tận thế','Đổi trang lịch hiện đại có nhãn; thêm chữ giải thích, không tạo ký tự Maya giả.','I198 chỉ là phép so sánh. Nguồn lịch2012: S09.'),
 ('G03_Nuoc_Tikal,G06_Itzan','G07_Witzna','Ba địa điểm, các bằng chứng khác nhau','Các sức ép chồng lên nhau','Lần lượt hiện từng thẻ, mỗi lần giữ một ý trọng tâm.','Không ghép các niên đại và địa điểm thành một biến cố duy nhất.'),
 ('I172,I001','I173,I128','Người trong cuộc chỉ thấy từng ngày','Đặt câu hỏi ở lại hay đi','Chuyển chậm từ vật dụng tới ngã rẽ; giữ một nhịp tĩnh cho câu hỏi.','Tình huống giả định, không phải ghi chép nhân chứng.'),
 ('I174,I004','R01_Tikal_forest','Cái giá của rời đi','Trở lại câu hỏi đầu video','Túi đồ ra khỏi khung; cắt về toàn cảnh Tikal.','Không kết luận Maya biến mất.'),
 ('R03_Tzutujil_weaving_2019','R06_Mayan_weaver_2023','Lịch sử tiếp tục qua con người','Khép bằng một hoạt động đang sống','Hai ảnh giữ đủ lâu, credit rõ; không mô phỏng chuyển động tay bằng AI.','Ảnh2019/2023, không ghi “quay hôm nay”.'),
 ('I150,I123','I124,I125','Câu hỏi dành cho khán giả','Chỗ dành cho tập sau và credit','Nền ít chi tiết; đặt mascot sẵn có nếu dự án có rig, chừa chỗ phụ đề.','Không tự thay thiết kế mascot. Nhạc/SFX chọn sau.'),
]
voice=json.loads((ROOT/'output/Mo_Den_Maya_Dao_Dien_Giong_Viet/02_Dao_Dien_Giong_Viet.json').read_text())
beats=voice['beats'];cue_map={a['id']:a for a in voice['source_cues']};scenes=[];shots=[]
for i,(b,spec) in enumerate(zip(beats,specs),1):
 aa,bb,t1,t2,motion,note=spec;ids=b['source_cue_ids'];split=(len(ids)+1)//2
 scene=dict(scene_id=f'SC{i:02}',title=b['title'],source_cue_ids=ids,reference_start=b['reference_start'],reference_end=b['reference_end'],purpose=b['intent'],motion=motion,editorial_guardrail=note)
 scenes.append(scene)
 for k,(group,astr,desc) in enumerate([(ids[:split],aa,t1),(ids[split:],bb,t2)],1):
  shots.append(dict(shot_id=f'SC{i:02}_{k}',scene_id=f'SC{i:02}',source_cue_ids=group,reference_start=cue_map[group[0]]['reference_start'],reference_end=cue_map[group[-1]]['reference_end'],text_anchor=cue_map[group[0]]['text'],asset_ids=astr.split(','),visual=desc,motion=motion,transition='Cắt theo ý kể; dissolve nhẹ chỉ khi chuyển thời gian/không gian.',guardrail=note,timing='Mốc cũ tham chiếu; căn theo audio cuối bằng cue/text_anchor.'))
assert [c for sh in shots for c in sh['source_cue_ids']]==list(range(1,276))
allids={a['id'] for a in assets+inventory+graphics}
assert all(k in allids for sh in shots for k in sh['asset_ids'])
js('03_Phan_canh/PHAN_CANH_36_DOAN.json',scenes);table('03_Phan_canh/SHOT_LIST_72_CANH.csv',shots)
js('03_Phan_canh/SHOT_LIST_72_CANH.json',{'status':'KẾ HOẠCH DỰNG, CHƯA PHẢI VIDEO ĐÃ RENDER','voice_work':'EXCLUDED_PRESERVE_EXISTING','timing':'reference_only_retime_to_final_audio','shots':shots})
shutil.copy2(ROOT/'output/Mo_Den_Maya_Giong_Ke_Tu_Nhien.srt',OUT/'03_Phan_canh/KICH_BAN_THAM_CHIEU.srt')
write('03_Phan_canh/PHAN_CANH_DOC_NHANH.md','# Bảng phân cảnh — 36 đoạn / 72 nhịp hình\n\nMốc cũ chỉ để tra cứu; dựng theo audio hoàn chỉnh. Các nhịp có thể chia/ghép theo ý kể, không cần giữ mỗi ảnh suốt một đoạn dài.\n\n'+'\n\n'.join(f"## {s['scene_id']} — {s['title']}\nCue {s['source_cue_ids'][0]}–{s['source_cue_ids'][-1]} | {s['reference_start']} → {s['reference_end']}\n\nMục đích: {s['purpose']}\n\n"+'\n\n'.join(f"- {x['shot_id']}: {x['visual']} — `{', '.join(x['asset_ids'])}`" for x in shots if x['scene_id']==s['scene_id'])+f"\n\nChuyển động: {s['motion']}\n\nLưu ý: {s['editorial_guardrail']}" for s in scenes))

write('04_Nguon_va_quyen/NGUON_NGHIEN_CUU.md','# Nguồn nghiên cứu và giới hạn sử dụng\n\nKiểm tra: 21/10/2026. Dữ liệu hình ảnh và quyền của từng file ở ASSET_REGISTRY.json/CSV.\n\n'+'\n\n'.join(f'**{k} — {v[0]}**\n\n{v[1]}' for k,v in sources.items())+'\n\n## Phạm vi kiểm chứng\n\nS07: chỉ dùng nội dung tóm tắt có thể truy cập, không tuyên bố đã đọc toàn văn. Bản đồ G01 không đặt ghim Witzna vì chưa có tọa độ đủ chắc trong các nguồn đã đối chiếu. G03 là sơ đồ nguyên lý, không phải tuyến thủy lợi đo đạc. G04 không có chuỗi lượng mưa hàng năm; G05 không có lượng mưa từng mùa. G06 và G08 không phải đồ thị dân số.\n')
write('04_Nguon_va_quyen/QUYEN_SU_DUNG.md','''# Quyền và ghi công

16 file tư liệu được giữ nguyên trong gói. Tên tác giả, nguồn và giấy phép từng file có trong ASSET_REGISTRY. Các nguồn có giấy phép mở/public domain đã được chọn thay cho ảnh báo chí chưa rõ quyền. Đây không phải cam kết rằng mọi quyền ngoài bản quyền (ví dụ quyền hình ảnh cá nhân) đã được bên thứ ba cấp riêng.

- CC0 và Public Domain: vẫn ghi nguồn để người xem truy vết bằng chứng.
- CC BY 4.0: ghi tác giả, tên tác phẩm, nguồn, liên kết giấy phép và nêu chỉnh sửa thực tế khi crop/chỉnh màu/chèn nhãn.
- CC BY-SA 3.0/4.0: có điều kiện ShareAlike với phần chuyển thể thuộc phạm vi giấy phép. Giữ nguyên bản gốc; nếu tạo bản chuyển thể, cung cấp nó theo giấy phép tương thích và ghi rõ thay đổi. Đừng mặc định chỉ ghi tên tác giả là đủ hoặc mặc định giấy phép bao phủ mọi thành phần khác trong video.
- Nếu dự án không muốn dùng BY-SA: có thể bỏ R03, dùng R06 cho đoạn đời sống; R04 Mayapán cần tìm ảnh thay thế hoặc xử lý đầy đủ BY-SA. Không tự đổi nhãn giấy phép.
- Không xóa ghi công rồi dùng ảnh nguồn như ảnh tự chụp. Không ghi người/đơn vị trong ảnh bảo trợ dự án.
- Figure 1 của bài ô nhiễm Tikal (S02) có credit tái bản AAAS riêng nên KHÔNG đưa vào gói. Các hình được chọn có credit ghi trong registry.
- Hình vẽ mới G01–G08 được tạo cho dự án; dữ liệu nền/nguồn khoa học được ghi riêng. Không gắn giấy phép của ảnh nghiên cứu lên cả bộ ảnh minh họa cũ.

Credit cuối video và phần mô tả: bắt đầu bằng CREDIT_TOAN_BO.txt, bỏ mục không thực sự xuất hiện; bổ sung mô tả chỉnh sửa tương ứng. Giấy phép phải có đường dẫn, không chỉ chữ viết tắt.
''')
write('04_Nguon_va_quyen/CREDIT_TOAN_BO.txt','TƯ LIỆU HÌNH ẢNH — MỎ ĐEN / MAYA\n\n'+'\n\n'.join(a['credit']+'\nGiấy phép: '+a['license_url']+'\nThay đổi trong video: [điền theo dựng thực tế; không tự ghi “không chỉnh sửa” nếu đã crop/overlay].' for a in assets)+'\n\nBản đồ nền: Made with Natural Earth (public domain).\nĐồ họa giải thích: dựng mới cho dự án Mỏ Đen; nguồn dữ liệu ở NGUON_NGHIEN_CUU.md.\n')
write('04_Nguon_va_quyen/TU_LIEU_CHUA_DU_QUYEN.md','''# Tư liệu bổ sung tùy chọn, chưa đưa vào gói

## Ảnh phế tích và LiDAR Witzna
https://vcresearch.berkeley.edu/news/maya-more-warlike-previously-thought

Trang có ảnh/bản đồ với credit Francisco Estrada-Belli, PACUNAM, Tulane và bản quyền trang UC Regents. Chưa thấy giấy phép cho tái sử dụng video thương mại của từng ảnh; không tải vào thư mục “được dùng”. Nếu muốn dùng, liên hệ chủ quyền hoặc tìm phiên bản được cấp phép rõ. Hai ảnh USGS trong gói đã đủ cho đoạn bằng chứng trầm tích, nhưng không thay thế ảnh chụp chính di tích.

## Tư liệu hiện vật/văn khắc đúng cuộc tấn công năm 697
Chưa có ảnh cận cảnh văn khắc được định danh, phiên âm và cấp quyền đầy đủ. Dùng thẻ chữ có dẫn S06, không thay bằng bia Tikal R07.

## Các cảnh chưa có ảnh thực chuyên biệt
Ảnh trực tiếp hiện trường hồ Corriental; mẫu gypsum của đúng nghiên cứu2018; hoạt động khai quật đang diễn ra; cảnh đời sống Maya ngoài nghề dệt; tư liệu riêng thời thuộc địa. Kế hoạch hiện tại dùng hình nghiên cứu/đồ họa hoặc minh họa có nhãn. Đây là các lựa chọn nâng chất lượng, không được tự tạo ảnh AI rồi ghi là tư liệu.
''')
write('01_KIEM_KE_VA_PHAN_CON_THIEU.md','''# Kiểm kê và phần đã bổ sung

Hai ZIP cũ có 198 PNG: 150 hình tổng quát và 48 hình theo câu chuyện Maya. Trong 48 hình có 30 bối cảnh, 18 vật thể. Không có ảnh tư liệu thật. Các bối cảnh Maya là minh họa khái quát, không phải phục dựng đúng Tikal/Witzna/Mayapán.

## Đã bổ sung trong ZIP này
- 7 ảnh thực: Tikal (3), Chichén Itzá (1), Mayapán (1), đời sống dệt của người Maya (2).
- 9 hình tư liệu nghiên cứu: lõi trầm tích USGS (2), zeolite/Tikal (3), dữ liệu vi khuẩn lam (1), thạch nhũ và đồng vị2025 (1), Itzan (2). Trong nhóm này có cả sơ đồ và biểu đồ, không gọi tất cả là ảnh chụp.
- 8 đồ họa gốc dạng SVG có thể sửa và PNG1920×1080: bản đồ, trục thời gian, đường đi nguyên lý của nước, khoảng giảm mưa,13 năm hạn, Itzan, Witzna, quyền lực/đời sống.
- 36 đoạn/72 nhịp hình bao phủ275 cue; danh mục nối về đúng đường dẫn198 ảnh cũ; nguồn, quyền và credit theo từng file.

## Còn cần ở bước dựng
1. Audio cuối và SRT căn theo audio: do nhánh giọng đọc đang xử lý, gói này không thay đổi.
2. Motion thực: mask mực nước, đường chạy hàng hóa, hiện nhãn theo lời; SVG/PNG tĩnh chưa tự trở thành video.
3. Mascot/rig Mỏ Đen nếu muốn người dẫn xuất hiện. Không tìm thấy rig nhân vật trong198 hình; dùng asset dự án đã duyệt, không thay thiết kế tự ý.
4. Nhạc/SFX có quyền sử dụng: chọn sau khi có dựng nháp, không nằm trong gói này.
5. Tư liệu tùy chọn chưa đủ quyền: xem TU_LIEU_CHUA_DU_QUYEN.md; ưu tiên ảnh Witzna và văn khắc đúng sự kiện nếu muốn nâng cấp.

## Những hình cũ dễ dùng sai
Kính thiên văn/microscope/đàm thoại, điện thoại196, bồn197, lịch198 chỉ dành cho nghiên cứu hiện đại hoặc phép so sánh có nhãn. Không đưa vào cảnh Maya cổ. Tránh mái ngói, ống khói, vòm/cầu dẫn nước kiểu La Mã, xe đẩy/ngựa, tiền xu, lúa mì, lạc đà trong bối cảnh Maya trước tiếp xúc. Ưu tiên bộ151–198 cho bối cảnh Maya; chỉ chọn vật thể tổng quát phù hợp từ001–150.

Các chuỗi151–153,157–159… không phải frame animation khớp pixel. Có thể cắt cảnh giữa trạng thái; muốn chuyển đổi liên tục phải tách lớp hoặc dựng lại chuyển động. Không dùng crossfade toàn ảnh như thể đã mô phỏng mực nước hạ.
''')
write('00_DOC_TRUOC_VA_PROMPT_CODEX.md','''# Gói hình ảnh và phân cảnh Maya — giao Codex

Gói bổ sung này đi cùng **hai ZIP ảnh cũ**. Không cần mở từng file để gửi: giao nguyên ZIP này cho Codex, giữ hai ZIP cũ trong cùng workspace. Chúng không được chép lại vào gói để tránh tải lại150MB dữ liệu trùng.

## Prompt giao việc — sao chép nguyên đoạn dưới

Hãy tích hợp gói Mo_Den_Maya_Tu_Lieu_That_Va_Phan_Canh_v1 với hai bộ ảnh Mỏ Đen150 và Maya48 đã có trong dự án để dựng video kết hợp hình vẽ và tư liệu thật. Đọc00_DOC_TRUOC,01_KIEM_KE,SHOT_LIST_72_CANH.json,ASSET_REGISTRY.json,GRAPHICS_REGISTRY.json và198_ANH_CU_MANIFEST.json trước khi sửa timeline.

Giữ nguyên công việc giọng đọc đang chạy; không chọn giọng mới, không tạo lại lời đọc và không ghi đè audio/SRT cuối. KICH_BAN_THAM_CHIEU.srt chỉ cung cấp275 cue và mốc cũ. Khi audio cuối sẵn sàng, căn shot bằng source_cue_ids/text_anchor; nếu bản lời đã thay đổi, báo phần không khớp và remap có giải thích, không kéo audio cho vừa mốc cũ.

Tự giải nén, kiểm tra đủ asset, ánh xạ các ID I001–I198 về hai bộ cũ; ID R/E là tư liệu thật/nghiên cứu trong gói; ID G là đồ họa gốc. Giữ một asset registry chung. Không tự thay ảnh nghiên cứu thiếu độ phân giải bằng ảnh AI. Những hình nghiên cứu nhỏ dùng inset và chú giải lớn; không kéo căng hoặc dùng tăng nét AI để bịa chi tiết mẫu.

Dựng theo36 đoạn/72 nhịp hình, có thể chia/ghép hợp lý theo audio. Dùng ảnh thật cho địa điểm/bằng chứng/đời sống; dùng minh họa cho cơ chế và tình huống giả định. Hiện nhãn địa điểm,năm chụp,nguồn khi cần; luôn phân biệt ảnh mẫu thật,sơ đồ giả thuyết và tình huống minh họa. Chuyển động phải giải thích một ý: nước đi vào hồ,mực nước giảm,hàng hóa bị ngắt,nhãn xuất hiện theo lời. Với ảnh tư liệu chỉ pan/zoom/crop nhẹ,không AI làm người/hiện vật hoạt động.

Không vẽ dữ liệu mưa/dân số giả. Không đặt chính xác Witzna khi chưa có tọa độ nguồn. Không dùng bia Tikal thay văn khắc697. Không dùng bản đồ mưa1989–2019 như khí hậu cổ. Giữ bất định929–942±6 và phân biệt692(theo mô hình lõi) với697(văn khắc). Không biến13 năm hạn thành13 năm tuyệt đối không mưa.

Đọc điều kiện CC BY/CC BY-SA; ghi credit và giấy phép đúng từng ảnh, cập nhật mô tả thay đổi thực tế. Chưa dùng những mục trong TU_LIEU_CHUA_DU_QUYEN. Giữ thiết kế mascot đã được duyệt trong dự án; nếu không có rig thì làm bản dựng hình ảnh trước, ghi rõ thiếu asset nhân vật thay vì tự thiết kế lại.

Tạo dựng nháp1920×1080 theo pipeline hiện có, ưu tiên kiểm tra ba đoạn tiêu biểu: Tikal/nước, đồ thị hạn, Witzna/bằng chứng. Sau đó hoàn thiện toàn bộ timeline, kiểm tra phụ đề không che nhãn và nguồn, không kéo giãn ảnh đứng, không giữ một slide dài chỉ vì cue dài. Đầu ra gồm video nháp, timeline/project có thể sửa, asset manifest và credit cuối. Chưa cần thêm nhạc/SFX hoặc xuất bản lên nền tảng.

## Tệp nào dùng làm gì?
|Tệp/thư mục|Vai trò|
|---|---|
|01_Tu_lieu_that|16 file ảnh/hình nghiên cứu đã tải, không chỉ đường link|
|02_Do_hoa_SVG_PNG|8 đồ họa; SVG để sửa/animate, PNG để dùng ngay|
|03_Phan_canh|Cue,shot,text anchor và đường dẫn ảnh cũ|
|04_Nguon_va_quyen|Nguồn,tác giả,giấy phép,credit và mục chưa đủ quyền|
|05_Xem_nhanh|Contact sheet để duyệt nhanh|
|06_Du_lieu_va_ma_nguon|Dữ liệu bản đồ,số liệu và mã dựng để chỉnh tiếp|

Đây là gói tư liệu và kế hoạch dựng, không phải video đã render. Không có audio mới trong gói.
''')

# Bảng xem nhanh: ảnh thật + hình nghiên cứu, và đồ họa.
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',17)
def contact(paths,target,cols=4):
 w,h=420,300;rows=(len(paths)+cols-1)//cols;sheet=Image.new('RGB',(cols*w,rows*h),'#f6efdf');d=ImageDraw.Draw(sheet)
 for i,p in enumerate(paths):
  im=Image.open(p).convert('RGB');im.thumbnail((400,250));x=(i%cols)*w+(w-im.width)//2;y=(i//cols)*h+8
  sheet.paste(im,(x,y));d.text(((i%cols)*w+12,(i//cols)*h+268),p.stem,font=font,fill=INK)
 sheet.save(OUT/target,quality=92)
contact(sorted((OUT/'01_Tu_lieu_that').glob('*')),'05_Xem_nhanh/01_TU_LIEU.jpg')
contact(sorted((OUT/'02_Do_hoa_SVG_PNG').glob('*.png')),'05_Xem_nhanh/02_DO_HOA.jpg',2)
shutil.copy2(__file__,OUT/'06_Du_lieu_va_ma_nguon/build_visual_pack.py')
write('06_Du_lieu_va_ma_nguon/README.md','Mã dựng build_visual_pack.py là bản lưu quy trình của phiên này; cần các đầu vào trong workspace gốc (2 ZIPảnh,voice JSON,SRT,thư mục maya_work). SVG/PNG và dữ liệu đi kèm dùng độc lập, không cần chạy lại script. Dùng map_points.json và chart_data.json để sửa đồ họa; không tự nội suy dữ liệu chưa có. Natural Earth ZIP là dữ liệu nền gốc.\n')
js('KIEM_TRA_GOI.json',{'original_illustrations_indexed':len(inventory),'downloaded_media':len(assets),'graphics_svg':len(graphics),'graphics_png':len(graphics),'scenes':len(scenes),'shots':len(shots),'cue_coverage':'1–275, một lần mỗi cue','all_shot_asset_ids_resolve':True,'audio_created':False,'video_rendered':False,'source_srt_sha256':hashlib.sha256((OUT/'03_Phan_canh/KICH_BAN_THAM_CHIEU.srt').read_bytes()).hexdigest()})
zpath=OUT.with_suffix('.zip')
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(OUT.rglob('*')):
  if p.is_file():z.write(p,str(p.relative_to(OUT.parent)))
print(json.dumps({'zip':str(zpath),'bytes':zpath.stat().st_size,'files':sum(p.is_file() for p in OUT.rglob('*'))},ensure_ascii=False))
