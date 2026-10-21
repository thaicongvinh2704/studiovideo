"""Original cel-style cutout parts; designed for scene animation rather than icon layouts."""
from pathlib import Path
ART=Path(__file__).resolve().parents[1]/'art';INK='#292723';SKIN='#fff4de'


def write(name,body,w,h):
    (ART/(name+'.svg')).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><g stroke="{INK}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">{body}</g></svg>',encoding='utf-8')


def p(d,fill='none',extra=''):return f'<path d="{d}" fill="{fill}" {extra}/>'
def e(x,y,rx,ry,fill,extra=''):return f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{fill}" {extra}/>'


def prepare():
    ART.mkdir(exist_ok=True)
    write('body_host',p('M27 13L38 7L50 12L62 7L73 13L88 33L75 45L67 36L68 97Q47 102 25 97L26 36L18 45L7 33Z','#313637')+p('M30 16Q45 29 61 15',extra='stroke="#1d2324"')+p('M54 35L54 51M47 43L61 43',extra='stroke="#f4f0df" stroke-width="4"')+p('M26 90Q48 94 67 90',extra='stroke="#222829" stroke-width="1.6"'),94,106)
    write('body_man',p('M26 16L38 10L55 14L71 8L79 30L67 39L70 103L23 103L25 38L14 43L8 32Z',SKIN)+p('M28 21L69 10L75 29L32 72L27 95L69 95L75 123L50 118L20 123Z','#c99152')+p('M30 70L64 97M26 98L70 99',extra='stroke="#91683e" stroke-width="2"'),94,130)
    write('body_woman',p('M28 12L41 8L51 12L64 9L76 24L70 45L78 119Q49 128 17 119L26 44L19 26Z','#b76754')+p('M32 12L62 45L26 79M26 80L70 79M30 87L23 116M64 87L73 117',extra='stroke="#8b493e" stroke-width="2"'),94,130)
    write('body_child',p('M25 17L38 9L50 13L63 8L77 25L68 41L69 95L23 95L25 41L15 46L7 29Z','#809b91')+p('M25 87L69 87L75 111L49 105L18 111Z','#d6b575')+p('M33 15Q47 26 61 14',extra='stroke="#5d7972" stroke-width="2"'),94,120)
    for kind in ('host','man','woman','child'):
        hair=p('M21 56Q10 33 22 19Q34 1 58 8Q82 6 88 33L81 47L73 28Q52 44 26 34L27 56Z','#292d2d')
        if kind=='host':hair=p('M20 56Q12 32 24 19L19 19L38 6L34 15L55 4L50 14L72 8L66 17L84 17L80 23L90 25L73 35Q48 32 28 44L28 57Z','#252b2b')
        elif kind=='woman':hair=e(29,17,15,14,'#292d2d')+p('M17 60Q10 30 28 17Q48 3 68 17Q88 28 86 57L79 59L73 31Q56 42 29 29L27 62Z','#292d2d')
        elif kind=='child':hair=p('M19 50Q9 28 31 17Q64 0 83 29L84 48L75 32Q48 39 29 31L27 51Z','#292d2d')
        face=e(51,58,34,39,SKIN)+e(19,61,6,9,SKIN)+e(83,61,5,8,SKIN)+hair
        face+=p('M30 89Q50 102 71 88',extra='stroke="#e2cfb3" stroke-width="1.4"')
        write('head_'+kind,face,104,110)
    expressions={
        'normal':p('M40 76Q49 78 58 75'),
        'happy':p('M36 73Q49 81 63 72Q61 91 49 90Q39 89 36 73Z','#3a302b')+p('M39 75Q49 80 60 74L57 80L42 81Z','#fffdf5',extra='stroke-width="1"'),
        'worried':p('M39 82Q50 74 62 80')+p('M30 43L41 39M58 39L69 44'),
        'surprised':e(50,81,5,7,'#483b32')+p('M30 38Q36 34 42 37M58 37Q65 34 71 38'),
        'annoyed':p('M32 43L43 47M58 47L70 42M40 81L61 81'),
        'talk':p('M39 76Q50 73 61 76L60 86Q51 91 41 86Z','#483b32')+p('M42 77L58 77L58 80L42 80Z','#fffdf5',extra='stroke-width="1"'),
    }
    for name,mouth in expressions.items():
        brows='' if name in ('worried','annoyed','surprised') else p('M31 44Q36 41 42 44M58 44Q65 41 70 44')
        eyes=e(37,57,2.2,4,'#292723')+e(64,57,2.2,4,'#292723')
        write('face_'+name,eyes+brows+mouth,104,110)
        write('blink_'+name,p('M32 58L42 58M59 58L69 58')+brows+mouth,104,110)
    write('arm',p('M12 8Q20 3 25 10L25 41L28 69Q26 77 18 76L13 70L11 42Z',SKIN)+p('M14 47L23 47',extra='stroke="#d7c4ab" stroke-width="1"'),40,82)
    write('hand',p('M12 7Q10 0 16 1L19 7L23 3Q27 3 27 8L29 14Q28 24 19 27Q10 26 9 20L6 13Q6 9 10 10L14 14Z',SKIN)+p('M18 10L20 16M23 9L25 15',extra='stroke-width="1.2"'),36,34)
    write('point',p('M8 12L17 8L36 8Q43 7 43 11Q43 15 25 15L27 19Q30 24 24 25L20 27L10 24L6 18Z',SKIN)+p('M18 17L22 21M15 20L18 24',extra='stroke-width="1.2"'),48,34)
    write('leg_host',p('M10 5L31 6L28 57L34 70Q34 78 24 78L4 77L5 69L11 58Z','#698fa5')+p('M7 67L27 66L34 72L34 79L4 79L4 73Z','#f5ecd9')+p('M12 11L15 59',extra='stroke="#557b92" stroke-width="1.4"'),42,87)
    write('leg_bare',p('M11 5L27 5L25 52L36 63Q39 71 30 72L5 72L7 64L12 53Z',SKIN)+p('M7 68L34 68',extra='stroke="#bdab91" stroke-width="1.3"'),42,80)
    write('shoe_seated',p('M5 5Q23 1 33 13L60 14Q65 17 62 25Q33 33 6 24Z',SKIN),70,40)
    write('legs_seated',p('M61 6L116 6L121 29Q155 36 167 65Q151 84 111 87L89 72L66 87Q26 84 12 66Q20 38 55 29Z',SKIN)+p('M61 5L116 5L124 32L91 29L52 33Z','#d6b575')+p('M52 47L93 72L127 47M39 75L66 87M114 87L143 76',extra='stroke="#bda98d" stroke-width="1.5"'),180,100)
    write('shadow',e(120,15,113,10,'#2e3528','stroke="none" opacity=".21"'),240,30)
    write('bowl',p('M15 27Q79 53 146 27Q133 93 81 94Q29 92 15 27Z','#a86d45')+e(80,26,66,18,'#e3cfa5')+p('M31 24Q81 4 130 24', '#f9efd5')+p('M39 23L47 21M60 20L67 19M85 19L95 21M108 23L116 24',extra='stroke="#ccbb95" stroke-width="1.2"'),165,110)
    write('basket',p('M29 46Q15 3 61 3Q106 3 94 47',extra='stroke="#704c32" stroke-width="7"')+p('M10 40L112 40L99 117Q63 135 25 117Z','#c29c65')+''.join(p(f'M{18+i*12} 43L{30+i*8} 120',extra='stroke="#907044" stroke-width="1.2"') for i in range(8))+''.join(p(f'M{15+i*2} {52+i*14}Q64 {66+i*13} {108-i*2} {52+i*14}',extra='stroke="#907044" stroke-width="1.2"') for i in range(5)),130,140)
    write('steam',p('M20 110Q-6 92 17 70Q39 51 16 31M49 113Q70 94 49 76Q30 55 53 27',extra='stroke="#fcf1dc" stroke-width="5" opacity=".75"'),80,140)
    write('fire',p('M9 99Q-7 70 20 45Q22 69 33 61Q48 33 42 9Q86 44 82 72Q96 63 92 50Q117 91 87 108Q48 133 9 99Z','#e79145')+p('M39 103Q23 84 43 70Q49 86 57 80Q70 61 66 49Q95 87 76 105Q55 122 39 103Z','#f2c261'),120,130)
    write('gurgle',p('M10 20Q25 1 40 20Q55 40 72 18M22 45Q40 25 57 45Q74 65 90 44',extra='stroke="#774b37" stroke-width="4"'),110,80)
    write('bubble',p('M20 4L276 4Q291 4 291 20L291 94Q291 108 277 108L92 108L59 136L68 108L22 108Q6 108 6 92L6 20Q6 4 20 4Z','#fff7df'),300,145)
    print('Puppet parts ready:',len(list(ART.glob('*.svg'))))


if __name__=='__main__':prepare()
