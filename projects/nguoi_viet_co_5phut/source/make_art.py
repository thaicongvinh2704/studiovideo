"""Original editable vector artwork for this film, with separately credited museum media."""
import math
from pathlib import Path
ART=Path(__file__).resolve().parents[1]/'art'
INK='#252525';SKIN='#f3d6ac';BROWN='#a77e55';GREEN='#98aa7e';BLUE='#b9d6dc';GOLD='#e2bf6b'


def svg(name,body,w=600,h=450):
    (ART/(name+'.svg')).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><g stroke="{INK}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">{body}</g></svg>',encoding='utf-8')


def path(d,fill='none',extra=''):return f'<path d="{d}" fill="{fill}" {extra}/>'
def line(x1,y1,x2,y2,extra=''):return f'<path d="M{x1} {y1}L{x2} {y2}" fill="none" {extra}/>'
def ellipse(x,y,rx,ry,fill,extra=''):return f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{fill}" {extra}/>'
def group(body,x=0,y=0,s=1,rot=0):return f'<g transform="translate({x} {y}) rotate({rot}) scale({s})">{body}</g>'


def house():
    b=path('M85 363L520 363',extra='stroke="#c5c0b6"')
    for x in (156,238,340,450):b+=path(f'M{x} 250L{x} 379L{x+12} 379L{x+12} 250',BROWN)
    b+=path('M130 174L451 174L451 284L130 284Z','#e7cda4')
    for x in range(143,450,17):b+=line(x,179,x,281,'stroke="#baa07e" stroke-width="1.7"')
    b+=path('M270 199L331 199L331 284L270 284Z','#554638')
    b+=path('M155 204L208 204L208 242L155 242Z','#645341')
    b+=path('M89 180Q172 162 286 64Q389 155 499 180Q414 164 286 116Q164 168 89 180Z',GOLD)
    b+=path('M89 180Q179 183 286 142Q399 185 499 180L490 195Q390 198 286 158Q170 198 99 195Z','#d2ad62')
    for dx in range(-150,170,22):b+=path(f'M286 104Q{286+dx*.5} 148 {286+dx} 181',extra='stroke="#b28d4f" stroke-width="1.7"')
    b+=path('M340 282L388 282L435 386L379 386Z','#d8b88b')
    for t in range(6):b+=line(345+t*6,291+t*16,393+t*6,291+t*16)
    b+=path('M123 282L457 282L463 299L119 299Z',BROWN)
    return b


def person(kind='adult',pose='stand',color='#8c9a78'):
    # Clothing and silhouettes are interpretive, rather than reconstructions of an individual.
    b=''
    if kind=='child':
        b+=path('M85 209Q60 242 59 268L99 267L109 238L139 266L178 264Q165 227 133 209',SKIN)
        b+=path('M73 143L138 143L141 222L74 222Z',color)
        b+=path('M75 157L49 205L64 212L92 175M138 157L160 203L144 212L121 175',SKIN)
    elif pose=='bend':
        b+=path('M66 210L61 271L84 271L99 220M104 216L129 269L153 269L130 203',SKIN)
        b+=path('M69 170L143 192L127 226L70 217Z',color)
        b+=path('M88 115L58 162L72 200L126 179L137 146Z',SKIN)
        b+=path('M115 144L154 190L178 224L189 220L172 182L138 132',SKIN)
    else:
        b+=path('M76 210L66 278L89 279L109 224L129 279L153 279L139 210',SKIN)
        b+=path('M71 127L145 127L143 219L74 219Z',SKIN)
        b+=path('M75 198L141 198L149 236L110 225L70 235Z',color)
        if pose=='carry':b+=path('M72 137L50 186L78 207L100 184L92 174L78 187L69 180L90 147M142 140L164 183L137 204L120 184L126 174L138 186L147 177L128 149',SKIN)
        elif pose=='pound':b+=path('M74 136L76 105L118 58L132 65L94 112L93 140M140 138L161 109L140 59L127 66L141 109L122 138',SKIN)
        else:b+=path('M74 138L55 213L67 217L91 148M142 138L161 213L149 217L127 148',SKIN)
    hx,hy=(145,111) if pose=='bend' else (108,84)
    b+=ellipse(hx,hy,38,44,SKIN)
    b+=path(f'M{hx-37} {hy-2}Q{hx-48} {hy-47} {hx-5} {hy-47}Q{hx+34} {hy-51} {hx+37} {hy-20}Q{hx+8} {hy-37} {hx-27} {hy-13}L{hx-28} {hy+1}Z',INK)
    b+=ellipse(hx-20,hy-43,12,10,INK)
    b+=ellipse(hx-9,hy,2,3,INK)+ellipse(hx+14,hy-2,2,3,INK)+path(f'M{hx-4} {hy+17}Q{hx+6} {hy+23} {hx+16} {hy+15}')
    return b


def rice(stems=6):
    b=''
    for i in range(stems):
        x=45+i*20;y=220-(i%3)*12
        b+=path(f'M{x} 295Q{x-5} 232 {x+12} {y-50}',extra='stroke="#758b58"')
        b+=path(f'M{x} 261Q{x-35} 231 {x-28} 224M{x} 253Q{x+37} 210 {x+33} 201',extra='stroke="#758b58"')
        for j in range(5):b+=ellipse(x+9+j*2,y-52+j*9,5,7,GOLD,'stroke="#ad975c" stroke-width="1.5"')
    return b


def boat():
    return path('M48 187Q174 223 431 185L473 150L437 212Q260 274 69 213Z','#bd9061')+path('M51 188Q214 226 431 185')+path('M93 211Q214 240 415 211',extra='stroke="#8f6947"')


def prepare():
    ART.mkdir(exist_ok=True)
    svg('stilt_house',house())
    svg('adult',person(),220,300)
    mother=person(color='#b6745d')+path('M74 130L144 130L142 206L158 264L60 264L74 206Z','#b6745d')+path('M76 132L139 179M72 202L143 202',extra='stroke="#875341" stroke-width="2"')
    svg('mother',mother,220,300)
    svg('child',person('child',color='#c7a259'),220,300)
    seated=person('child',color='#c7a259').replace('M85 209Q60 242 59 268L99 267L109 238L139 266L178 264Q165 227 133 209','M81 210Q47 218 40 247Q81 264 113 243Q155 269 183 248Q172 218 137 210L113 225Z')
    svg('seated_child',seated,220,300)
    svg('farmer',person(pose='bend'),240,300)
    svg('fisher',person(pose='carry',color='#8aa4aa'),220,300)
    svg('pounder',person(pose='pound'),220,300)
    svg('pounder_right',f'<g transform="translate(220 0) scale(-1 1)">{person(pose="pound")}</g>',220,300)
    land=path('M40 392Q370 340 655 391Q960 337 1240 391L1240 512Q1100 541 850 507Q540 476 40 530Z','#dce3c7')
    land+=path('M0 450Q360 369 667 449Q1010 532 1280 446L1280 630L0 630Z',BLUE)
    for y in range(474,630,30):
        for x in range(20+(y%4)*70,1280,210):land+=path(f'M{x} {y}q49 -12 96 0',extra='stroke="#8eb7c0" stroke-width="2"')
    for x,y,s in ((65,115,.8),(480,140,.65),(815,95,.85)):land+=group(house(),x,y,s)
    for x,y in ((28,310),(440,302),(825,300),(1190,300)):
        land+=path(f'M{x} {y+90}L{x+8} {y+25}',BROWN)+ellipse(x,y,43,59,GREEN)+ellipse(x-23,y+34,34,33,GREEN)
    svg('village',land,1280,650)
    river=path('M0 190Q280 127 550 182Q880 231 1280 179L1280 490L0 490Z',BLUE)
    for y in range(220,470,44):
        for x in range(20+(y%3)*45,1270,180):river+=path(f'M{x} {y}q45 -12 90 0',extra='stroke="#8eb7c0" stroke-width="2"')
    river+=path('M0 171Q350 122 620 171Q950 207 1280 159',extra='stroke="#859b76" stroke-width="10"')
    for x in range(30,1280,105):river+=path(f'M{x} 184q-8 -64 12 -85M{x} 179q14 -45 28 -46',extra='stroke="#8da478"')
    svg('river',river,1280,520)
    svg('boat',boat(),520,300)
    svg('oar',path('M43 20L58 21L92 247L126 288Q109 316 85 298L79 254Z',BROWN),160,330)
    svg('sun',ellipse(100,100,52,52,GOLD)+''.join(line(100+math.cos(i*math.tau/12)*68,100+math.sin(i*math.tau/12)*68,100+math.cos(i*math.tau/12)*82,100+math.sin(i*math.tau/12)*82) for i in range(12)),200,200)
    svg('mist',''.join(path(f'M{30+i*65} {90+i*37}q180 -38 350 0q180 29 330 -4',extra='stroke="#cfdad9" stroke-width="12"') for i in range(4)),820,280)
    hearth=ellipse(205,259,164,29,'#e2d8c8')+path('M88 247L300 197M110 203L288 253',extra='stroke="#8c684c" stroke-width="17"')
    hearth+=path('M90 220L115 118L125 220M295 219L274 117L264 219',BROWN)+path('M111 121Q192 86 277 121',extra='stroke-width="6"')
    hearth+=path('M147 128Q144 190 193 197Q247 193 245 128Z','#51483f')+path('M145 128Q190 115 246 128',extra='stroke-width="5"')
    svg('hearth',hearth,400,300)
    svg('flame',path('M26 153Q-2 113 44 74Q49 103 65 97Q75 58 68 12Q137 69 129 110Q154 100 144 77Q190 138 147 169Q83 204 26 153Z','#df8e53')+path('M67 160Q50 140 78 116Q86 135 95 131Q110 107 109 93Q146 142 120 162Q92 184 67 160Z',GOLD),190,200)
    svg('smoke',path('M60 228Q-3 189 58 153Q106 115 57 88Q11 57 61 22',extra='stroke="#bcb8b0" stroke-width="13" opacity=".6"'),140,260)
    field=path('M20 190L540 75L1220 190L1270 405L40 405Z','#d1dec0')
    for i in range(5):field+=path(f'M{50+i*240} 410L{540+(i-2)*80} 80',extra='stroke="#9db58a" stroke-width="10"')
    for x in range(65,1200,120):field+=group(rice(3),x,80+(x%4)*20,.72)
    svg('rice_field',field,1280,450);svg('rice',rice(7),220,320)
    svg('rice_sheaf',rice(7)+path('M55 265L179 265L179 280L55 280Z',BROWN),220,320)
    bowl=ellipse(255,190,179,53,'#fff6df')+path('M79 190Q103 341 256 342Q411 335 433 190Q260 248 79 190Z','#c39b76')
    bowl+=ellipse(255,180,164,44,'#fcf8ed')
    for i in range(23):
        x=115+(i*53)%280;y=153+(i*17)%44;bowl+=path(f'M{x} {y}l10 -2',extra='stroke="#ccbda1" stroke-width="2"')
    svg('bowl',bowl,520,400)
    svg('hoe',path('M300 38L319 40L255 324L236 319Z',BROWN)+path('M226 275L338 294L288 366L198 338Z','#7f977e'),440,400)
    svg('sickle',path('M247 205Q112 260 93 130Q80 51 190 31Q106 89 144 146Q180 195 247 154Z','#92a58d')+path('M224 164L265 153L345 306Q331 330 311 325Z',BROWN),420,380)
    svg('plough',path('M88 170L242 82L352 183L276 288L177 262Z','#8b9c82')+path('M242 82L276 288M88 170L352 183',extra='stroke="#61765e"')+path('M219 113L239 120L343 26L325 16Z',BROWN),440,330)
    svg('hook',path('M220 42L220 210Q221 327 112 299Q61 282 78 212L91 179L98 237Q110 268 144 257Q180 253 177 216L177 42Z','#8d9b80')+ellipse(199,41,26,24,'none'),330,370)
    net=path('M55 67Q253 106 461 65L388 316Q245 366 126 313Z','#e0d4b5')
    for i in range(8):
        net+=line(62+i*55,85,137+i*34,320,'stroke="#a7977e" stroke-width="2"')
        net+=path(f'M{75+i*9} {99+i*30}Q250 {130+i*28} {448-i*9} {98+i*30}',extra='stroke="#a7977e" stroke-width="2"')
    for i in range(7):net+=ellipse(115+i*46,327+math.sin(i)*8,10,14,'#8d8b82')
    svg('net',net,520,390)
    fish=path('M64 115Q158 11 272 117Q168 226 64 115L24 60L26 167Z','#a9c3c5')+ellipse(224,104,4,5,INK)+path('M180 74Q159 117 180 158M93 104L138 94',extra='stroke="#6e929b"')
    svg('fish',fish,320,230)
    basket=path('M104 126Q69 15 196 22Q324 24 283 127',extra='stroke="#9b7750" stroke-width="13"')+path('M48 123L345 123L304 303Q195 344 89 301Z','#c7aa78')
    for y in range(140,295,23):basket+=path(f'M{55+(y-140)*.2} {y}Q197 {y+31} {339-(y-140)*.2} {y}',extra='stroke="#9b7750" stroke-width="2"')
    for x in range(70,330,24):basket+=line(x,129,100+(x-70)*.77,309,'stroke="#9b7750" stroke-width="2"')
    svg('basket',basket,400,360)
    furnace=path('M97 338L101 147Q106 87 167 61L245 61Q304 96 307 150L316 338Z','#d5ae87')+path('M139 338L142 240Q203 169 270 240L272 338Z','#5b4940')
    for x,y in ((125,155),(231,154),(117,197),(266,202),(108,286),(288,285)):furnace+=path(f'M{x} {y}l25 -8l22 13',extra='stroke="#ad8468" stroke-width="2"')
    svg('furnace',furnace,430,390)
    svg('crucible',path('M80 60L242 60L226 210Q160 242 95 210Z','#766650')+ellipse(161,62,81,23,'#efaa61')+path('M241 67L284 90L230 107Z','#766650')+path('M75 127L30 118L20 134L78 155M243 125L306 119L310 138L240 153Z',BROWN),340,280)
    mold=path('M84 70L316 47L356 90L335 324L87 341L53 293Z','#aaa593')
    mold+=path('M84 70L107 108L87 341M107 108L356 90',extra='stroke="#787869"')
    for x,y in ((157,141),(253,132),(151,227),(245,217)):
        mold+=path(f'M{x} {y}l-24 55l21 -10l18 7l-15 -52l1 73',extra='stroke="#626b60" stroke-width="5"')
    svg('mold',mold,420,390)
    arrow=path('M134 35L57 210L127 181L199 206Z','#8d9b7d')+path('M134 35L127 181L133 305L157 303L148 180L199 206Z','#647b64')+path('M134 35L127 181L57 210',extra='stroke="#455c4b"')
    svg('arrowhead',arrow,260,345)
    svg('arrowheads',''.join(group(arrow,15+(i%4)*125,5+(i//4)*160,.50,(-1)**i*7) for i in range(12)),590,560)
    dig=path('M70 178L320 58L536 181L304 331Z','#d2b28e')+path('M70 178L304 331L304 395L69 244Z','#b08b69')+path('M304 331L536 181L536 243L304 395Z','#916d50')
    dig+=path('M157 185L309 109L439 183L303 267Z','#9d7c59')+group(arrow,215,100,.30,15)
    for x,y in ((199,161),(354,194),(284,243)):dig+=ellipse(x,y,20,9,'#a3a48b')
    svg('excavation',dig,600,450)
    fortress=''
    for rx,ry in ((480,225),(350,164),(210,97)):
        fortress+=ellipse(600,295,rx,ry,'#d6dfd0','stroke="#9cb6b1" stroke-width="18"')+ellipse(600,295,rx-17,ry-14,'#e2d5b3','stroke="#9b8867" stroke-width="14"')
    fortress+=path('M595 310L601 476M594 310L261 385M594 310L909 180',extra='stroke="#8d775a" stroke-width="9"')+group(house(),450,156,.45)
    svg('fortress',fortress,1200,600)
    turtle=ellipse(195,180,124,84,'#9eaf83')+ellipse(332,163,46,27,'#aaba8b')+ellipse(344,158,3,4,INK)
    for x,y in ((108,111),(107,248),(260,110),(260,251)):turtle+=ellipse(x,y,26,17,'#9eaf83')
    turtle+=path('M97 172L155 121L221 124L291 175L238 237L167 242Z',extra='stroke="#71865e"')
    svg('turtle',turtle,420,330)
    svg('crossbow',path('M215 167L264 155L371 338L337 361Z',BROWN)+path('M46 281Q146 31 374 73Q240 71 161 158Q95 216 46 281Z',BROWN)+path('M46 281L374 73M104 220L293 340',extra='stroke="#8c7759"')+path('M272 132L373 71L363 105L346 88L272 155Z','#83957a'),440,400)
    svg('pestle',path('M69 19L85 19L83 353Q75 368 65 351Z',BROWN),150,390)
    svg('mortar',path('M55 83L250 82L231 190L78 189Z',BROWN)+ellipse(153,81,98,27,'#755c43')+path('M92 189L215 189L239 226L70 226Z','#bd9669'),310,260)
    svg('rain',ellipse(180,98,97,55,'#d7e0e3')+ellipse(115,114,77,40,'#d7e0e3')+ellipse(250,113,68,42,'#d7e0e3')+''.join(line(86+i*42,180+(i%2)*25,70+i*42,213+(i%2)*25,'stroke="#83a9b5" stroke-width="6"') for i in range(6)),370,300)
    dry=path('M15 112Q172 57 362 113L354 231L19 232Z','#e4c9a2')
    dry+=path('M170 97L155 152L197 180L167 230M155 152L78 162L42 213M197 180L271 152L332 170M271 152L284 104',extra='stroke="#b48e68"')
    svg('dry_earth',dry,390,280)
    svg('rivers_map',path('M105 50Q316 147 261 254Q194 381 440 438M389 58Q334 192 304 242Q293 332 440 438M440 438Q527 452 607 544M440 438Q456 495 443 569M440 438Q531 506 565 574',extra='stroke="#9bbfc8" stroke-width="24"')+ellipse(444,448,85,65,'#cad9ba','stroke="none" opacity=".55"')+path('M80 40Q170 10 245 90M350 25Q448 25 490 108',extra='stroke="#9aa98b" stroke-width="7"'),700,610)
    svg('hands',path('M50 193L89 150L138 111L159 120L135 153L176 138L194 150L164 173L198 165L211 182L164 211L108 236L64 230Z',SKIN)+path('M443 193L404 150L355 111L334 120L358 153L317 138L299 150L329 173L295 165L282 182L329 211L385 236L429 230Z',SKIN),500,330)
    print('Original SVG assets:',len(list(ART.glob('*.svg'))))


if __name__=='__main__':prepare()
