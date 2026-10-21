"""Original editable SVG illustrations and semantic asset catalog (offline)."""
import json
from pathlib import Path
from xml.sax.saxutils import escape

INK='#191d20'; GOLD='#f6ca45'; RED='#ed6557'; BLUE='#73b7d6'; GREEN='#77b67b'; PAPER='#fff1cd'; EARTH='#bc8964'


def svg_body(name):
    def path(d,fill='none',**attrs):
        extra=' '.join(f'{k.replace("_","-")}="{v}"' for k,v in attrs.items())
        return f'<path d="{d}" fill="{fill}" {extra}/>'
    def circle(x,y,r,fill):return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"/>'
    def rect(x,y,w,h,fill,rx=0):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"/>'
    def lines(items):return ''.join(path(d) for d in items)
    if name=='city':
        return path('M25 273H375M65 265V150H118V127H145V150H174V265M228 265V137H260V110H288V137H337V265',PAPER)+path('M47 149L118 96L190 149M210 137L278 77L352 137',RED)+path('M174 265V185H228V265M183 265V229Q201 205 220 229V265',EARTH)+lines(['M65 184H174M65 221H174M228 173H337M228 212H337','M94 163V178M143 163V178M254 151V166M304 151V166'])+circle(201,58,23,GOLD)
    if name=='temple':
        return path('M38 266H363V284H38ZM55 245H346V265H55ZM76 126H325V145H76Z',PAPER)+path('M55 124L201 43L347 124Z',EARTH)+''.join(rect(x,145,23,100,PAPER) for x in (88,145,204,263))+path('M140 103L201 69L263 103Z',GOLD)
    if name=='pyramid':
        return path('M45 264L194 47L351 264Z',GOLD)+path('M194 47L231 264H351Z','#dba847')+lines(['M75 222H319M103 181H288M131 140H260M158 99H229','M106 223V264M169 223V264M239 223V264M298 223V264M141 183V221M210 183V221M271 183V221'])+path('M12 277Q130 266 199 281T389 273')
    if name=='column':
        return path('M99 267H300V285H99ZM115 245H285V267H115ZM141 96H260V245H141ZM113 68H289V95H113Z',PAPER)+lines(['M158 105V234M183 105V234M208 105V234M234 105V234'])+path('M114 68Q79 37 106 24Q130 9 145 34M289 68Q323 37 299 24Q274 9 260 34')
    if name=='scroll':
        return path('M89 58H324Q358 61 344 99H293V240Q293 276 257 273H56Q25 270 39 235H94V86Q94 58 76 58Z',PAPER)+lines(['M293 99V82Q293 59 321 58M94 235H257Q238 270 257 273','M129 114H260M129 145H246M129 176H259M129 207H218'])
    if name=='book':
        return path('M41 86Q121 61 198 103Q279 60 359 87V267Q282 241 198 278Q119 241 41 265Z',PAPER)+lines(['M198 103V278','M64 119Q122 102 174 127M64 157Q122 140 174 165M64 195Q122 178 174 203M221 127Q278 103 335 120M221 165Q278 141 335 158M221 203Q278 179 335 196'])
    if name=='amphora':
        return path('M144 59H256L246 112Q304 147 287 225Q280 270 200 276Q120 270 113 225Q96 147 154 112Z',RED)+path('M135 132Q66 107 85 181Q91 205 114 202M265 132Q334 107 315 181Q309 205 286 202')+path('M143 59Q200 37 257 59Q200 81 143 59',PAPER)+lines(['M116 172H284M113 203H287M134 237L154 217L177 238L200 217L223 238L246 217L267 237'])
    if name=='map':
        return path('M35 219L55 126L108 100L134 47L188 80L231 55L287 89L339 77L370 174L326 218L274 202L215 261L162 240L96 267Z','#c4dfad')+path('M189 80Q160 126 207 159T215 261',stroke=BLUE,stroke_width=8)+path('M90 206Q174 92 309 170',stroke=RED,stroke_dasharray='8 9')+circle(90,206,8,RED)+circle(309,170,8,RED)
    if name=='globe':
        return circle(200,161,112,BLUE)+path('M118 91L155 61L173 80L166 112L206 117L213 142L177 160L159 185L128 174L105 139ZM235 61L270 77L267 104L289 120L280 146L239 136L224 102ZM225 177L272 175L286 200L261 238L241 259L222 219Z',GREEN)+path('M65 279Q202 298 340 279M200 273V290')
    if name in ('boat','ship'):
        return path('M42 203H357L312 267H96Z',EARTH)+path('M177 57V203M181 62L72 187H177Z',PAPER)+path('M194 82L311 187H194Z',GOLD)+lines(['M108 225H298','M35 285Q66 268 96 285T157 285T218 285T279 285T340 285T395 285'])
    if name=='tree':
        return path('M171 269L182 161L155 130L169 117L196 140L220 104L238 118L211 162L226 269Z',EARTH)+path('M98 155Q64 119 97 91Q80 45 132 43Q154 7 198 36Q237 5 264 42Q312 27 321 79Q354 113 318 143Q295 178 256 157Q218 183 187 157Q145 181 116 157Z',GREEN)+path('M131 282Q163 270 174 283M222 282L248 274M109 271L96 252M283 273L299 255')
    if name=='mountain':
        return path('M21 269L132 62L208 165L262 79L383 269Z',EARTH)+path('M105 112L132 62L173 118L152 107L135 122L123 107ZM231 134L262 79L299 139L276 125L261 145L248 126Z','#ffffff')+path('M54 269H359')
    if name=='house':
        return path('M79 143H320V271H79Z',PAPER)+path('M49 144L196 44L351 144Z',RED)+rect(176,187,57,84,EARTH)+rect(103,174,42,43,BLUE)+rect(258,174,39,43,BLUE)+lines(['M124 174V217M103 196H145M277 174V217M258 196H297'])
    if name=='coins':
        return ''.join(path(f'M{x} {y}V{y+36}Q{x+43} {y+54} {x+86} {y+36}V{y}Z',GOLD)+f'<ellipse cx="{x+43}" cy="{y}" rx="43" ry="17" fill="{GOLD}"/>' for x,y in [(51,234),(156,207),(156,168),(261,234)])+path('M187 161V184M177 166Q206 158 200 171Q172 170 179 180H199')
    if name=='crown':
        return path('M63 109L131 174L201 72L270 174L339 109L305 253H94Z',GOLD)+path('M94 228H305M136 204L149 218L162 204L149 188ZM237 204L250 218L263 204L250 188Z',RED)+''.join(circle(x,y,10,RED) for x,y in [(63,106),(201,69),(339,106)])
    if name=='bulb':
        return path('M146 204Q142 181 122 155Q78 73 151 44Q244 3 276 89Q295 143 251 178Q239 193 239 206Z',GOLD)+path('M151 207H236V239L222 256H164L151 239Z',PAPER)+lines(['M153 219L235 212M155 233L232 226M177 255Q190 275 209 255','M178 202L169 142L187 157L203 137L218 157L229 134L210 202','M71 40L55 20M38 106L13 102M319 44L338 24M339 112L366 109M194 15V0'])
    if name=='question':return path('M130 99Q127 27 203 31Q285 29 278 100Q279 139 225 165Q202 176 204 208',stroke=RED,stroke_width=16)+circle(204,256,10,RED)
    if name=='check':return path('M70 169L156 253L334 57',stroke=GREEN,stroke_width=23)
    if name=='cross':return path('M89 58L315 261M310 55L91 262',stroke=RED,stroke_width=19)
    if name=='clock':return circle(200,160,112,PAPER)+path('M200 76V160L255 188',stroke_width=7)+lines(['M200 55V70M200 250V265M95 160H109M290 160H305'])+circle(200,160,5,INK)
    if name=='calendar':return rect(68,74,266,208,PAPER,8)+rect(68,74,266,57,RED,8)+path('M119 51V94M281 51V94',stroke_width=9)+''.join(rect(x,y,22,20,GOLD if x==239 and y==204 else '#ffffff',2) for x in (103,148,194,239,283) for y in (160,204,247))
    if name=='magnifier':return circle(167,133,81,BLUE)+circle(167,133,64,'#e7f3f5')+path('M221 195L313 282',stroke=INK,stroke_width=27)+path('M128 101Q146 78 171 81',stroke='#ffffff',stroke_width=8)
    if name=='compass':return circle(200,162,111,PAPER)+circle(200,162,91,'#ffffff')+path('M161 199L222 92L241 126Z',RED)+path('M161 199L178 233L241 126Z',BLUE)+circle(200,162,7,INK)+lines(['M200 42V62M200 260V281M82 162H100M301 162H320'])
    if name=='archive':return rect(64,69,270,212,EARTH,4)+rect(54,52,291,35,PAPER,3)+rect(119,131,162,91,PAPER,3)+path('M151 155H249M148 178H245M168 202H231')
    if name=='document':return path('M94 35H245L310 102V282H94Z',PAPER)+path('M245 35V102H310')+lines(['M126 137H277M126 169H266M126 202H278M126 235H233'])
    if name=='flame':return path('M188 288Q60 274 99 163Q114 204 141 174Q121 111 179 32Q172 100 214 126Q241 88 257 54Q263 130 295 167Q345 267 240 287Z',RED)+path('M168 277Q133 232 170 180Q170 213 203 218Q222 191 226 161Q286 252 229 281Z',GOLD)
    if name=='shield':return path('M74 66Q199 23 325 65V161Q315 242 200 291Q87 242 74 161Z',BLUE)+path('M200 44V276M85 145H315',stroke_width=10)
    if name=='sword':return path('M167 213L275 41L307 28L302 68L191 231Z','#c9d7db')+path('M133 186L224 244',stroke=GOLD,stroke_width=16)+path('M169 226L134 277',stroke=EARTH,stroke_width=19)+circle(126,286,10,GOLD)
    if name=='cart':return path('M87 113H333L313 222H107Z',EARTH)+lines(['M96 147H326M103 182H318M128 117L139 216M186 117V218M245 117L234 218M297 117L279 218','M104 228H319M83 114L40 101'])+circle(133,253,32,EARTH)+circle(286,253,32,EARTH)+lines(['M133 221V285M101 253H165M286 221V285M254 253H318'])
    if name=='wheel':return circle(201,160,114,EARTH)+circle(201,160,91,PAPER)+''.join(path(f'M201 160L{x} {y}') for x,y in [(201,70),(201,250),(111,160),(291,160),(137,96),(265,224),(137,224),(265,96)])+circle(201,160,19,EARTH)
    if name=='bridge':return path('M37 266V183H362V266H314V224Q281 167 249 224V266H209V224Q176 167 144 224V266H103V224Q70 167 37 224Z',EARTH)+path('M34 178H365M37 157V181M86 156V181M135 156V181M184 156V181M233 156V181M282 156V181M331 156V181')+path('M10 289Q47 275 84 289T158 289T232 289T306 289T380 289',stroke=BLUE)
    if name=='factory':return path('M51 280V155L123 116V155L198 116V155L276 116V280Z',EARTH)+rect(293,45,38,235,RED)+''.join(rect(x,y,27,35,BLUE) for x in (77,139,211) for y in (184,234))+path('M312 34Q280 11 310 1M336 30Q365 10 345 0')
    if name=='balance':return path('M131 278H272M200 268V66M95 91H306',stroke_width=8)+circle(200,60,13,GOLD)+path('M92 94L49 192H135ZM308 94L265 192H351Z',PAPER)+path('M49 192Q92 252 135 192M265 192Q308 252 351 192',GOLD)
    if name=='network':return path('M200 161L84 67M200 161L319 70M200 161L70 249M200 161L329 250M84 67H319M70 249H329',stroke=RED)+''.join(circle(x,y,r,c) for x,y,r,c in [(200,161,42,BLUE),(84,67,25,GOLD),(319,70,25,GREEN),(70,249,25,GREEN),(329,250,25,GOLD)])
    if name=='chart':return path('M57 40V276H362',stroke_width=5)+rect(90,190,48,84,BLUE)+rect(166,131,48,143,GOLD)+rect(243,71,48,203,GREEN)+path('M83 149L166 92L236 104L325 25',stroke=RED,stroke_width=5)+path('M299 28L325 25L324 51',stroke=RED)
    if name=='computer':return rect(50,39,301,203,'#e7f3f5',7)+rect(63,53,275,172,'#ffffff',2)+path('M180 242V279H140M221 242V279H260',stroke_width=6)+path('M109 279H289')+rect(103,98,77,80,GOLD,3)+lines(['M201 99H291M201 126H277M201 153H290M201 178H255'])
    if name=='phone':return rect(127,22,148,272,INK,16)+rect(136,47,130,219,'#ffffff',4)+path('M179 34H222',stroke='#ffffff')+circle(201,280,6,'#ffffff')+rect(153,72,94,71,BLUE,5)+lines(['M155 166H246M155 192H234M155 218H244'])
    if name=='camera':return path('M66 106H130L153 68H245L268 106H337V268H66Z',EARTH)+circle(201,187,63,INK)+circle(201,187,48,BLUE)+circle(188,171,12,'#ffffff')+rect(287,123,30,19,GOLD,3)
    if name=='microphone':return rect(155,41,91,164,INK,43)+path('M128 142V166Q125 237 200 239Q278 238 274 164V142M200 239V280M150 280H250',stroke_width=7)+lines(['M174 76H227M174 99H227M174 123H227'])
    if name=='cloud':return path('M92 250Q25 251 33 195Q39 162 78 163Q60 110 113 96Q150 78 176 113Q206 50 266 83Q300 103 288 142Q351 119 365 172Q392 228 334 250Z','#e2eff2')
    if name=='water':return ''.join(path(f'M18 {y}Q58 {y-24} 98 {y}T178 {y}T258 {y}T338 {y}T418 {y}',stroke=BLUE,stroke_width=5) for y in (108,159,211))
    if name=='gear':
        import math
        pts=[(200+(.0+106 if i%4 in (0,1) else 86)*math.cos(i*math.pi/16),160+(106 if i%4 in (0,1) else 86)*math.sin(i*math.pi/16)) for i in range(32)]
        return path('M'+'L'.join(f'{x:.2f} {y:.2f}' for x,y in pts)+'Z',GOLD)+circle(200,160,42,PAPER)
    raise KeyError(name)


CATALOG = {
    'city':('Thành cổ','thanh pho thanh co do thi cu dan'), 'temple':('Đền cổ','den tho kien truc di tich'),
    'pyramid':('Kim tự tháp','kim tu thap ai cap'), 'column':('Cột đá','cot da hy lap la ma'),
    'scroll':('Văn bản cổ','van ban ghi chep tu lieu chu viet'), 'book':('Sách','sach lich su nghien cuu'),
    'amphora':('Bình gốm','binh gom hien vat khao co'), 'map':('Bản đồ','ban do tuyen duong di cu'),
    'globe':('Địa cầu','dia cau the gioi toan cau'), 'boat':('Thuyền buồm','thuyen bien du hanh'),
    'tree':('Cây','cay rung thien nhien'), 'mountain':('Núi','nui dia hinh'),
    'house':('Ngôi nhà','nha lang cu tru'), 'coins':('Tiền xu','tien xu kinh te thuong mai'),
    'crown':('Vương miện','vua vuong trieu quyen luc'), 'bulb':('Ý tưởng','y tuong phat hien sang tao'),
    'question':('Dấu hỏi','bi an cau hoi chua biet'), 'check':('Dấu kiểm','dung chung minh xac nhan'),
    'cross':('Gạch chéo','sai bac bo khong'), 'clock':('Đồng hồ','thoi gian nam thang'),
    'calendar':('Lịch','lich nien dai ngay nam'), 'magnifier':('Kính lúp','kiem tra doi chieu tim kiem'),
    'compass':('La bàn','la ban dinh huong hanh trinh'), 'archive':('Hộp tư liệu','luu tru tai lieu ho so'),
    'document':('Tài liệu','tai lieu bang chung thong tin'), 'flame':('Ngọn lửa','lua chay pha huy mat mat'),
    'shield':('Khiên','khien bao ve quan doi'), 'sword':('Kiếm','kiem chien tranh'),
    'cart':('Xe hàng','xe hang van chuyen di cu'), 'wheel':('Bánh xe','banh xe phat minh'),
    'bridge':('Cầu','cau ket noi giao thong'), 'factory':('Nhà máy','nha may cong nghiep'),
    'balance':('Cán cân','can bang danh gia so sanh'), 'network':('Mạng kết nối','mang ket noi lien he'),
    'chart':('Biểu đồ','bieu do tang truong so lieu'), 'computer':('Máy tính','may tinh cong nghe'),
    'phone':('Điện thoại','dien thoai thong tin'), 'camera':('Máy ảnh','may anh hinh anh chup'),
    'microphone':('Micro','micro giong noi am thanh'), 'cloud':('Mây','may bau troi'),
    'water':('Sóng nước','nuoc song bien'), 'gear':('Bánh răng','banh rang co khi'),
}


def library_root():
    import sys
    root=Path(sys.executable).parent if getattr(sys,'frozen',False) else Path(__file__).resolve().parents[1]
    return root/'assets'/'ink'


def install_library(folder=None):
    folder=Path(folder or library_root());folder.mkdir(parents=True,exist_ok=True)
    records=[]
    for name,(title,tags) in CATALOG.items():
        body=svg_body(name)
        svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="800" height="640" viewBox="0 0 400 320"><title>{escape(title)}</title><g stroke="{INK}" stroke-width="3.1" stroke-linecap="round" stroke-linejoin="round">{body}</g></svg>'
        (folder/(name+'.svg')).write_text(svg,encoding='utf-8')
        records.append(dict(id=name,title=title,tags=tags.split(),file=name+'.svg',source='Studio original vector library',pivot=[200,280]))
    (folder/'catalog.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
    return records


def asset(name):
    candidate=library_root()/(name+'.svg')
    if not candidate.is_file():raise FileNotFoundError('Thiếu bộ hình Studio: '+str(candidate))
    return str(candidate)
