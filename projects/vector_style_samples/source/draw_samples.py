"""Original, deterministic vector illustrations. No image-generation model is used."""
import sys,math,random,json,subprocess,hashlib
from pathlib import Path
from xml.sax.saxutils import escape
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'.deps'))
from svgpathtools import parse_path
from perfect_freehand import get_stroke

W,H=1600,900
OUT=ROOT/'images';OUT.mkdir(parents=True,exist_ok=True)
INK='#303c38'

def p(x,y,z):return (800+.88*x-.76*y,641+.235*x+.30*y-z)
def coords(points):return ' '.join(f'{x:.2f},{y:.2f}' for x,y in points)
def polygon(points):return 'M'+'L'.join(f'{x:.2f} {y:.2f}' for x,y in points)+'Z'
def poly3(points):return polygon([p(*q) for q in points])
def cpoint(q):return f'{q[0]:.2f} {q[1]:.2f}'
def arc_front(x,y,z,w,h):
 a=p(x-w/2,y,z);b=p(x-w/2,y,z+h*.62)
 c=p(x-w/2,y,z+h);d=p(x,y,z+h)
 e=p(x+w/2,y,z+h);f=p(x+w/2,y,z+h*.62);g=p(x+w/2,y,z)
 return f'M{cpoint(a)}L{cpoint(b)}Q{cpoint(c)} {cpoint(d)}Q{cpoint(e)} {cpoint(f)}L{cpoint(g)}Z'
def arc_side(x,y,z,w,h):
 a=p(x,y-w/2,z);b=p(x,y-w/2,z+h*.62)
 c=p(x,y-w/2,z+h);d=p(x,y,z+h)
 e=p(x,y+w/2,z+h);f=p(x,y+w/2,z+h*.62);g=p(x,y+w/2,z)
 return f'M{cpoint(a)}L{cpoint(b)}Q{cpoint(c)} {cpoint(d)}Q{cpoint(e)} {cpoint(f)}L{cpoint(g)}Z'

PALETTES={
 '01_clean':dict(sky='#e7f1ed',paper='#fff9ec',stone='#dfb775',front='#e2bd83',side='#ba8f5c',cap='#f4deb0',dark='#665b40',mortar='#a08459',soil='#87744c',green='#62805a',deep='#345d4e',light='#b0ba75',water='#83b7bc',sand='#d9c99e'),
 '02_ink':dict(sky='#eef3e8',paper='#fff9e9',stone='#ddb27a',front='#e6c18d',side='#bb946a',cap='#f8e3b3',dark='#645842',mortar='#a38c65',soil='#8f7952',green='#72906c',deep='#3b6454',light='#bac282',water='#91bfc0',sand='#ded0a8'),
 '03_hatch':dict(sky='#f5f3e7',paper='#fffbef',stone='#dfc18d',front='#ebd5ac',side='#ceb384',cap='#f8e8c5',dark='#706247',mortar='#ac9872',soil='#94815a',green='#93a180',deep='#526f5a',light='#c6c994',water='#a6c4bd',sand='#e5d9b5'),
}

class Drawing:
 def __init__(self,style):
  self.style=style;self.pal=PALETTES[style];self.body=[];self.defs=[];self.rough=[];self.stroke_count=0;self.ids=[]
 def group(self,name):self.body.append(f'<g id="{name}">');self.ids.append(name)
 def end(self):self.body.append('</g>')
 def clip(self,name,d):self.defs.append(f'<clipPath id="{name}"><path d="{d}"/></clipPath>')
 def raw(self,code):self.body.append(code)
 def draw(self,d,fill='none',color=INK,width=2,organic=False,opacity=1,hatch=False):
  self.stroke_count+=1
  if color==INK and self.style=='02_ink':color='#233b32'
  if fill!='none':self.body.append(f'<path d="{d}" fill="{fill}" opacity="{opacity}"/>')
  if width<=0 or color=='none':return
  if self.style=='01_clean':
   self.body.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" opacity="{opacity}"/>')
  elif self.style=='02_ink':
   # Real pressure-outline polygons from perfect-freehand, sampled along authored Beziers.
   try:
    curve=parse_path(d)
    for sub in curve.continuous_subpaths():
     points=[]
     for seg in sub:
      n=max(2,min(80,int(abs(seg.end-seg.start)/4)+5))
      for i in range(n):
       t=i/(n-1);v=seg.point(t)
       pressure=.50+.23*math.sin(len(points)*.19+.7)+(.10 if organic else 0)
       points.append((v.real,v.imag,pressure))
     if len(points)<2:continue
     outline=get_stroke(points,size=width*(1.72 if organic else 1.35),thinning=.72 if organic else .45,smoothing=.5,streamline=0,simulate_pressure=False,last=True,taper_start=width*2 if organic else False,taper_end=width*3 if organic else False)
     if outline:self.body.append(f'<path d="{polygon(outline)}" fill="{color}" opacity="{opacity}"/>')
   except Exception as ex:raise RuntimeError(f'Failed pressure stroke: {d[:120]}') from ex
  else:
   # Filled shapes remain authored; Rough.js supplies only selected outlines / hatching.
   i=len(self.rough);self.rough.append(dict(d=d,color=color,width=width*.78,fill=self.pal['mortar'] if hatch else None))
   self.body.append(f'<!--ROUGH:{i}:{opacity}-->')
 def line(self,points,color=INK,width=1,opacity=1,organic=False):self.draw('M'+'L'.join(f'{x:.2f} {y:.2f}' for x,y in points),color=color,width=width,opacity=opacity,organic=organic)
 def ellipse(self,x,y,rx,ry,fill='none',color=INK,width=1.4):
  d=f'M{x-rx} {y}a{rx} {ry} 0 1 0 {2*rx} 0a{rx} {ry} 0 1 0 {-2*rx} 0Z'
  self.draw(d,fill,color,width,organic=True)
 def finish(self,path):
  body=''.join(self.body)
  if self.rough:
   src=ROOT/'rough_input.json';dst=ROOT/'rough_output.json';src.write_text(json.dumps(self.rough),encoding='utf-8')
   subprocess.run(['node',str(ROOT/'source'/'rough_paths.cjs'),str(src),str(dst)],check=True,capture_output=True)
   result=json.loads(dst.read_text(encoding='utf-8'))
   for i,paths in enumerate(result):
    snippets=[]
    for q in paths:
     snippets.append(f'<path d="{q["d"]}" stroke="{q["stroke"]}" stroke-width="{q["strokeWidth"]}" fill="{q["fill"]}" stroke-linejoin="round" stroke-linecap="round"/>')
    for op in ['1','.36','.45','.5','.55','.65','.7','.8','.9']:
     body=body.replace(f'<!--ROUGH:{i}:{op}-->',f'<g opacity="{op}">'+''.join(snippets)+'</g>')
   if '<!--ROUGH:' in body:
    import re
    def repl(match):
     i=int(match.group(1));opacity=match.group(2)
     return f'<g opacity="{opacity}">'+''.join(f'<path d="{q["d"]}" stroke="{q["stroke"]}" stroke-width="{q["strokeWidth"]}" fill="{q["fill"]}" stroke-linejoin="round" stroke-linecap="round"/>' for q in result[i])+'</g>'
    body=re.sub(r'<!--ROUGH:(\d+):([\d.]+)-->',repl,body)
  xml=f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" width="1600" height="900" viewBox="0 0 1600 900"><title>Original vector garden study, {self.style}</title><desc>Authored vector curves; no AI-generated imagery. Imagined garden for style comparison.</desc><defs>'+''.join(self.defs)+'</defs>'+body+'</svg>'
  path.write_text(xml,encoding='utf-8')

def stone_block(d,x0,x1,y0,y1,z,h,name):
 c=d.pal
 front=poly3([(x0,y1,z),(x1,y1,z),(x1,y1,z+h),(x0,y1,z+h)])
 side=poly3([(x1,y1,z),(x1,y0,z),(x1,y0,z+h),(x1,y1,z+h)])
 top=poly3([(x0,y0,z+h),(x1,y0,z+h),(x1,y1,z+h),(x0,y1,z+h)])
 d.group(name)
 d.draw(front,c['front'],width=2.4)
 d.draw(side,c['side'],width=2.4,hatch=d.style=='03_hatch')
 d.clip(name+'_front',front);d.clip(name+'_side',side)
 # Fine masonry joins are clipped to the real faces, instead of tiled over the entire image.
 d.raw(f'<g clip-path="url(#{name}_front)">')
 for row,zz in enumerate(range(int(z)+12,int(z+h)-2,17)):
  d.line([p(x0,y1,zz),p(x1,y1,zz)],c['mortar'],.7,.45)
  for xx in range(int(x0)+((row%2)*26),int(x1),52):d.line([p(xx,y1,zz),p(xx,y1,min(zz+17,z+h))],c['mortar'],.65,.45)
 d.raw('</g>')
 d.raw(f'<g clip-path="url(#{name}_side)">')
 for row,zz in enumerate(range(int(z)+12,int(z+h)-2,17)):
  d.line([p(x1,y0,zz),p(x1,y1,zz)],'#7e7454',.65,.45)
  for yy in range(int(y0)+((row%2)*24),int(y1),52):d.line([p(x1,yy,zz),p(x1,yy,min(zz+17,z+h))],'#7e7454',.65,.45)
 d.raw('</g>')
 d.draw(top,c['cap'],width=2)
 d.end()

def gallery(d,x0,x1,y0,y1,z,h,name):
 c=d.pal;stone_block(d,x0,x1,y0,y1,z,h,name)
 d.group(name+'_vaults')
 count=max(3,round((x1-x0)/105));pitch=(x1-x0)/count
 for j in range(count):
  x=x0+pitch*(j+.5);w=pitch*.66;ah=h*.69
  outer=arc_front(x,y1,z+12,w+13,ah+8)
  d.draw(outer,c['stone'],width=1.2)
  hole=arc_front(x,y1+.2,z+13,w,ah)
  d.draw(hole,c['dark'],width=1.65)
  # Recessed inner arch surface and a lit threshold establish thickness.
  d.draw(arc_front(x+4,y1+.3,z+13,w*.81,ah*.92),'#8a7955',width=.8)
  d.draw(poly3([(x-w/2,y1, z+13),(x+w/2,y1,z+13),(x+w/2-8,y1,z+22),(x-w/2+8,y1,z+22)]),c['cap'],width=.6)
  # Voussoirs around the arch: short radial strokes, distinct from the wall joints.
  for angle in [20,48,76,104,132,160]:
   t=math.radians(angle);cx=x+math.cos(t)*(w/2+3);cz=z+13+ah*.62+math.sin(t)*(ah*.38+4)
   d.line([p(cx,y1,cz),p(cx+math.cos(t)*7,y1,cz+math.sin(t)*7)],c['mortar'],.7,.8)
 n=max(2,round((y1-y0)/100));pitch=(y1-y0)/n
 for j in range(n):
  y=y0+pitch*(j+.5);w=pitch*.61
  d.draw(arc_side(x1,y,z+13,w+12,h*.72),c['stone'],width=1.1)
  d.draw(arc_side(x1+.3,y,z+13,w,h*.66),c['dark'],width=1.5)
 # Cornice bands and restrained blue-green glazed frieze.
 for zz,thick in [(z+h-7,7),(z+h-21,5)]:
  d.draw(poly3([(x0-4,y1+4,zz),(x1+4,y1+4,zz),(x1+4,y1+4,zz+thick),(x0-4,y1+4,zz+thick)]),c['cap'],width=1.2)
  d.draw(poly3([(x1+4,y1+4,zz),(x1+4,y0-4,zz),(x1+4,y0-4,zz+thick),(x1+4,y1+4,zz+thick)]),c['stone'],width=1.1)
 for x in range(int(x0)+12,int(x1)-8,24):
  d.draw(poly3([(x,y1+4,z+h-16),(x+13,y1+4,z+h-16),(x+13,y1+4,z+h-11),(x,y1+4,z+h-11)]),'#6a9591',color='none',width=0)
 d.end()

def foliage_blob(d,x,y,rx,ry,seed):
 rng=random.Random(seed);pts=[]
 for i in range(18):
  a=i*math.tau/18;r=1+rng.uniform(-.14,.14);pts.append((x+math.cos(a)*rx*r,y+math.sin(a)*ry*r))
 # Quadratic midpoint construction yields a soft, organic silhouette with actual curves.
 mids=[((a[0]+b[0])/2,(a[1]+b[1])/2) for a,b in zip(pts,pts[1:]+pts[:1])]
 shape=f'M{cpoint(mids[-1])}'+''.join(f'Q{cpoint(a)} {cpoint(b)}' for a,b in zip(pts,mids))+'Z'
 d.draw(shape,d.pal['green'],width=1.8,organic=True)
 # Broad shadow is a designed shape, not a blur filter.
 shadow=f'M{x-rx*.85} {y+ry*.15}Q{x-rx*.23} {y+ry*.8} {x+rx*.65} {y+ry*.03}Q{x+rx*.96} {y+ry*.7} {x+rx*.1} {y+ry*.92}Q{x-rx*.62} {y+ry*.9} {x-rx*.85} {y+ry*.15}Z'
 d.draw(shadow,d.pal['deep'],color='none',width=0)
 for j in range(8):
  xx=x+rng.uniform(-.7,.65)*rx;yy=y+rng.uniform(-.55,.15)*ry
  d.draw(f'M{xx-5} {yy+3}q5 -8 11 -1',color=d.pal['light'],width=2.2,organic=True)

def fig_tree(d,x,y,z,size,seed,name):
 bx,by=p(x,y,z);rng=random.Random(seed)
 d.group(name)
 d.ellipse(bx,by+2,size*.38,size*.08,'#685c43',color='none',width=0)
 trunk=f'M{bx-size*.09} {by}Q{bx-size*.02} {by-size*.54} {bx-size*.13} {by-size*.87}L{bx+size*.01} {by-size*.9}Q{bx+size*.03} {by-size*.42} {bx+size*.11} {by}Z'
 d.draw(trunk,'#a98753',width=1.8,organic=True)
 for dx,dy in [(-.43,-.95),(.39,-1.05),(-.12,-1.25)]:
  d.draw(f'M{bx} {by-size*.42}Q{bx+dx*size*.45} {by-size*.82} {bx+dx*size} {by+dy*size}',color='#5e6247',width=4.0,organic=True)
 for j,(dx,dy,rx,ry) in enumerate([(-.35,-1.03,.36,.29),(.35,-1.09,.37,.30),(-.07,-1.32,.4,.3),(0,-.97,.43,.30)]):
  foliage_blob(d,bx+dx*size,by+dy*size,size*rx,size*ry,seed+j*17)
 d.end()

def palm(d,x,y,z,h,seed,name):
 bx,by=p(x,y,z);rng=random.Random(seed);lean=rng.uniform(-13,14)
 tx,ty=bx+lean,by-h
 d.group(name)
 d.ellipse(bx,by+1,h*.18,h*.035,'#786d4f',color='none',width=0)
 d.draw(f'M{bx-4.5} {by}Q{bx+lean*.5-5} {by-h*.55} {tx-2.6} {ty}L{tx+3} {ty}Q{bx+lean*.5+4} {by-h*.55} {bx+5.5} {by}Z','#ad8c54',width=1.6,organic=True)
 for j in range(1,11):
  yy=by-h*j/11;xx=bx+lean*j/11
  d.draw(f'M{xx-3} {yy}q4 2 7 -1',color='#6e7051',width=.8,organic=True)
 for j in range(9):
  angle=(-178+j*23)*math.pi/180;length=h*rng.uniform(.38,.54)
  ex=tx+math.cos(angle)*length;ey=ty+math.sin(angle)*length*.54+length*.12
  mx=(tx+ex)/2;my=min(ty,ey)-length*.22
  d.draw(f'M{tx} {ty}Q{mx} {my} {ex} {ey}Q{mx+3} {my+11} {tx} {ty}Z',d.pal['deep'] if j%3==0 else d.pal['green'],width=1.2,organic=True)
  curve=parse_path(f'M{tx} {ty}Q{mx} {my} {ex} {ey}')
  for k in range(2,9):
   u=k/10;v=curve.point(u);tangent=curve.unit_tangent(u);normal=tangent*1j;amount=(1-u)*length*.15
   for sign in [-1,1]:
    tip=v+normal*amount*sign+tangent*amount*.7
    d.draw(f'M{v.real:.2f} {v.imag:.2f}Q{(v.real+tip.real)/2:.2f} {min(v.imag,tip.imag)-2:.2f} {tip.real:.2f} {tip.imag:.2f}',color=d.pal['light'] if sign<0 else d.pal['deep'],width=.8,organic=True)
 d.ellipse(tx+2,ty+4,5,3.5,'#bd9560',width=.8)
 d.end()

def shrub(d,x,y,z,size,seed,name):
 bx,by=p(x,y,z);d.group(name)
 for j,(dx,dy,r) in enumerate([(-.5,-.2,.5),(.35,-.22,.48),(0,-.5,.58)]):foliage_blob(d,bx+dx*size,by+dy*size,size*r,size*r*.75,seed+j*9)
 if seed%3==0:
  rng=random.Random(seed)
  for j in range(6):
   xx=bx+rng.uniform(-.6,.6)*size;yy=by+rng.uniform(-.7,-.25)*size
   d.ellipse(xx,yy,2.1,2.1,'#e4b68a',color='none',width=0)
 d.end()

def vines(d,x,y,z,length,seed,name):
 bx,by=p(x,y,z);rng=random.Random(seed);d.group(name)
 for j in range(3):
  xx=bx+j*8;le=length*rng.uniform(.65,1.12)
  d.draw(f'M{xx} {by}C{xx-13} {by+le*.3} {xx+10} {by+le*.61} {xx-8} {by+le}',color=d.pal['deep'],width=1.3,organic=True)
  for k in range(2,8):
   yy=by+k*le/9;xx2=xx+math.sin(k*.7)*6
   side=-1 if k%2 else 1
   d.draw(f'M{xx2} {yy}Q{xx2+side*14} {yy-9} {xx2+side*12} {yy+2}Q{xx2+side*4} {yy+9} {xx2} {yy}Z',d.pal['green'] if k%3 else d.pal['light'],width=.8,organic=True)
 d.end()

def stairs(d):
 d.group('central_stairway')
 steps=15
 for i in range(steps):
  u=i/steps;v=(i+1)/steps
  ya=180+u*160;yb=180+v*160;za=183*(1-u);zb=183*(1-v)
  x=54+u*16
  d.draw(poly3([(-x,ya,za),(x,ya,za),(x,yb,za),(-x,yb,za)]),d.pal['cap'],width=1.0)
  d.draw(poly3([(-x,yb,za),(x,yb,za),(x,yb,zb),(-x,yb,zb)]),d.pal['stone'],width=.9)
 for side in [-1,1]:
  x=side*77
  d.draw(poly3([(x,180,199),(x,345,20),(x+side*13,345,20),(x+side*13,180,199)]),d.pal['cap'],width=1.6)
 d.end()

def draw_scene(style):
 d=Drawing(style);c=d.pal;rng=random.Random(1129)
 d.defs.append(f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop stop-color="{c["sky"]}"/><stop offset="1" stop-color="{c["paper"]}"/></linearGradient>')
 d.raw('<rect width="1600" height="900" fill="url(#sky)"/>')
 d.group('distant_landscape')
 d.ellipse(1290,125,46,46,'#f2d497',color='none',width=0)
 for x,y,w in [(120,142,180),(1100,208,190),(360,98,220)]:
  d.draw(f'M{x} {y}q{w*.12} -16 {w*.26} -8q{w*.08} -20 {w*.25} -9q{w*.13} -6 {w*.22} 10h{w*.18}',fill='none',color='#fffdf3',width=7,organic=True)
 d.draw('M0 575Q138 515 234 557Q355 479 457 540Q595 493 708 548Q859 479 1027 529Q1151 461 1261 521Q1444 482 1600 542V769H0Z','#d1d5b6',color='none',width=0)
 for j in range(29):
  x=18+j*58+rng.uniform(-8,8);y=593+rng.uniform(-22,16);w=rng.uniform(32,58);h=rng.uniform(27,72)
  d.draw(f'M{x} {y}V{y-h}H{x+w}V{y+8}Z','#c9c3a0',color='#b1ac8c',width=.7)
  if j%3==0:
   for k in range(3):d.draw(f'M{x+k*w/3} {y-h}v-5h{w/6}v5','#c9c3a0',color='#b1ac8c',width=.7)
 d.end()
 d.group('river')
 d.draw('M0 690Q280 654 520 698T1060 686T1600 675V900H0Z',c['water'],color='none',width=0)
 d.draw('M70 737Q320 712 615 749T1360 718L1560 747Q1230 759 1050 750T560 788T20 772Z','#bfd2bd',color='none',width=0)
 for j in range(59):
  x=rng.uniform(-10,1590);y=rng.uniform(729,895);w=rng.uniform(18,95)
  d.draw(f'M{x:.2f} {y:.2f}q{w*.5:.2f} -3 {w:.2f} 0',color='#f7edcd' if j%3 else '#5f999f',width=1.15,opacity=.65,organic=True)
 d.end()
 d.group('river_bank')
 d.draw('M94 668L1174 574L1536 700L1080 821L339 835L55 757Z',c['sand'],color='#a39d77',width=1.4)
 d.ellipse(777,748,498,72,'#839384',color='none',width=0)
 d.end()
 d.raw('<g id="garden_composition" transform="translate(48 54) scale(.94)">')
 stone_block(d,-477,477,-214,192,0,29,'foundation')
 stone_block(d,-468,468,-210,186,29,18,'stepped_plinth')
 # Substantial parapets frame actual soil terraces; their openings lead to the stairs.
 for n,(x0,x1,y0,y1,base,height,name) in enumerate([(-460,460,-205,180,47,136,'lower_gallery'),(-334,334,-157,130,183,124,'middle_gallery'),(-211,211,-108,85,307,115,'upper_gallery')]):
  z=base+height
  gallery(d,x0,x1,y0,y1,base,height,name)
  d.group(f'terrace_{n}_soil_and_parapets')
  d.draw(poly3([(x0+8,y0+8,z+1),(x1-8,y0+8,z+1),(x1-8,y1-8,z+1),(x0+8,y1-8,z+1)]),c['cap'],width=1)
  # Earth beds occupy only the planting strips, with a generous walkable deck between them.
  for xa,xb in [(x0+17,x0+70),(x1-70,x1-17)]:
   d.draw(poly3([(xa,y0+13,z+2),(xb,y0+13,z+2),(xb,y1-20,z+2),(xa,y1-20,z+2)]),c['soil'],width=.85)
  for xa,xb in [(x0+24,-77),(77,x1-24)]:
   d.draw(poly3([(xa,y1-46,z+2),(xb,y1-46,z+2),(xb,y1-14,z+2),(xa,y1-14,z+2)]),c['soil'],width=.85)
  # Narrow water channels and inset paving joints have a shared vanishing direction.
  d.draw(poly3([(x1-91,y0+13,z+2),(x1-81,y0+13,z+2),(x1-81,y1-14,z+2),(x1-91,y1-14,z+2)]),c['water'],width=.8)
  for xx in range(int(x0)+82,int(x1)-74,38):
   d.line([p(xx,y1-65,z+2),p(xx,y1-51,z+2)],c['mortar'],.65,.45)
  for lo,hi in [(x0,-70),(70,x1)]:stone_block(d,lo,hi,y1-12,y1,z,15,f'parapet_{n}_{lo}')
  stone_block(d,x1-12,x1,y0,y1,z,15,f'side_parapet_{n}')
  d.end()
 # Upper pavilion: Mesopotamian flat roof and deep rectangular doorways, no generic pagoda.
 stone_block(d,-112,112,-72,57,422,105,'upper_pavilion')
 d.group('pavilion_doors')
 for x in [-68,0,68]:
  d.draw(poly3([(x-19,57.5,422),(x+19,57.5,422),(x+19,57.5,495),(x-19,57.5,495)]),c['dark'],width=1.7)
  d.draw(poly3([(x-15,57.7,422),(x+15,57.7,422),(x+15,57.7,489),(x-15,57.7,489)]),'#8f7d55',width=.75)
 stone_block(d,-127,127,-83,68,527,15,'pavilion_cornice')
 stone_block(d,-118,118,-76,61,542,9,'pavilion_roof')
 d.end()
 stairs(d)
 # Each tree is a named group with a separate trunk, crown and leaves, ready for animation.
 plants=[
  ('palm',-183,-58,437,112,11),('palm',173,-73,437,128,19),
  ('fig',-165,64,437,48,16),('fig',168,57,437,44,21),
  ('palm',-293,-115,322,137,31),('fig',-286,70,322,67,37),('palm',295,84,322,127,40),('fig',305,-99,322,57,44),
  ('palm',-410,20,198,151,51),('fig',-407,143,198,73,59),('palm',425,-128,198,151,64),('fig',423,132,198,67,68),
 ]
 plants.sort(key=lambda a:p(a[1],a[2],a[3])[1])
 for j,(kind,x,y,z,size,seed) in enumerate(plants):
  (palm if kind=='palm' else fig_tree)(d,x,y,z,size,seed,f'plant_{j}_{kind}')
 for lev,(x0,x1,y,z) in enumerate([(-442,442,166,198),(-315,315,116,322),(-195,195,72,437)]):
  for j,x in enumerate(range(x0+12,x1-8,43)):
   if abs(x)<83:continue
   shrub(d,x,y,z,17+(j%3)*3,83+lev*17+j,f'bed_{lev}_{j}')
   if j%3==1:vines(d,x,y+1,z,43+(j%4)*9,209+j+lev,f'vine_{lev}_{j}')
 # Additional beds grow down the side terraces, varied in height and silhouette.
 for lev,(xx,y0,y1,z) in enumerate([(424,-172,142,198),(296,-123,94,322),(173,-78,58,437)]):
  for side in [-1,1]:
   for j,yy in enumerate(range(y0,y1,37)):
    shrub(d,xx*side,yy,z,23+(j%3)*4,307+lev*40+j*3+(0 if side<0 else 1),f'side_bed_{lev}_{side}_{j}')
 # A restrained foreground plant gives depth without hiding the architecture.
 d.group('foreground_reeds')
 for j in range(21):
  bx=rng.uniform(70,315);by=rng.uniform(887,924);height=rng.uniform(49,125);lean=rng.uniform(-72,48)
  tx=bx+lean;ty=by-height
  d.draw(f'M{bx:.2f} {by:.2f}Q{bx+lean*.15:.2f} {by-height*.73:.2f} {tx:.2f} {ty:.2f}Q{bx+lean*.85+12:.2f} {by-height*.4:.2f} {bx:.2f} {by:.2f}Z',c['deep'] if j%3 else c['green'],width=1.2,organic=True)
 for x,y in [(1290,821),(1420,843),(1190,874)]:
  d.draw(f'M{x-30} {y}Q{x} {y-11} {x+28} {y}Q{x} {y+13} {x-30} {y}Z',c['green'],width=1.1,organic=True)
 d.end()
 # Discrete quiet highlights on selected architectural edges improve shape hierarchy.
 d.group('edge_highlights')
 for x0,x1,y,z in [(-460,460,180,183),(-334,334,130,307),(-211,211,85,422)]:
  d.line([p(x0,y,z+18),p(x1,y,z+18)],'#fff0cc',1.4,.9)
 d.end()
 d.raw('</g>')
 return d

def main():
 from PySide6.QtWidgets import QApplication
 from PySide6.QtGui import QImage,QPainter,QColor,QFont
 from PySide6.QtSvg import QSvgRenderer
 from PySide6.QtCore import QRectF
 app=QApplication.instance() or QApplication([])
 report=[]
 for style in PALETTES:
  d=draw_scene(style);svg_path=OUT/(style+'.svg');d.finish(svg_path)
  renderer=QSvgRenderer(str(svg_path));assert renderer.isValid(),svg_path
  image=QImage(W,H,QImage.Format.Format_ARGB32_Premultiplied);image.fill(QColor('#fff9ec'))
  painter=QPainter(image);painter.setRenderHints(QPainter.RenderHint.Antialiasing|QPainter.RenderHint.SmoothPixmapTransform);renderer.render(painter,QRectF(0,0,W,H));painter.end()
  image.save(str(OUT/(style+'.png')))
  # A vector-rendered detail crop, not a modification of a generated bitmap.
  detail=QImage(960,640,QImage.Format.Format_ARGB32_Premultiplied);detail.fill(QColor('#fff9ec'))
  painter=QPainter(detail);painter.setRenderHint(QPainter.RenderHint.Antialiasing);painter.translate(-230,-70);painter.scale(1.45,1.45);renderer.render(painter,QRectF(0,0,W,H));painter.end();detail.save(str(OUT/(style+'_detail.png')))
  report.append(dict(style=style,svg=svg_path.name,png=style+'.png',authored_shapes=d.stroke_count,groups=len(d.ids),actual_libraries=['svgpathtools']+(['perfect-freehand'] if style=='02_ink' else ['roughjs'] if style=='03_hatch' else []),sha256=hashlib.sha256(svg_path.read_bytes()).hexdigest()))
  print(f'READY {style}: {d.stroke_count} shapes, {len(d.ids)} named groups',flush=True)
 manifest=dict(method='Deterministic programmatic SVG drawing, no image generation AI; PNGs are rendered directly from the SVG with Qt.',subject='Imagined elevated garden, art-direction preview rather than archaeological reconstruction.',samples=report,dependencies=dict(perfect_freehand='1.2.0',svgpathtools='1.8.0',roughjs='4.6.6'))
 (ROOT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')

if __name__=='__main__':main()
