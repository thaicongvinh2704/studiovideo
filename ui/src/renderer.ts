import {Application,Container,Graphics,Text,Sprite,Assets,Texture} from 'pixi.js';
import {sampleAt,track,nodeState} from './clock';
import defaultRig from '../../config/character-kit.json';

export function hand(pose:string,side:string,rig:any=defaultRig):[number,number] {
  return rig.poses[pose]?.[side]||rig.poses.neutral[side];
}
const ink=0x26313d;
function line(g:Graphics,pts:number[][],width=7,color=ink){g.moveTo(pts[0][0],pts[0][1]);for(const p of pts.slice(1))g.lineTo(p[0],p[1]);g.stroke({width,color,cap:'round',join:'round'});}
function character(n:any,states:Map<string,any>,rig:any=defaultRig) {
  const c=new Container();
  function part(id:string){const definition=rig.parts.find((p:any)=>p.id===id);if(!definition)throw new Error('Rig part missing: '+id);const g=new Graphics();g.label=id;g.pivot.set(...definition.pivot as [number,number]);g.position.set(...definition.pivot as [number,number]);c.addChild(g);return g;}
  let g=part('legs');
  // Original layered outline character: legs, body, head, articulated arms and face.
  g.roundRect(-45,-30,36,95,15).fill(0x364958).stroke({width:6,color:ink});
  g.roundRect(10,-30,36,95,15).fill(0x364958).stroke({width:6,color:ink});
  g.roundRect(-65,53,54,19,8).fill(0x20313d);g.roundRect(10,53,57,19,8).fill(0x20313d);
  g=part('body');
  g.roundRect(-58,-170,116,155,28).fill(n.color||0x14b8a6).stroke({width:7,color:ink});
  g=part('neck');
  g.roundRect(-16,-202,32,43,10).fill(0xffd9b7).stroke({width:6,color:ink});
  g=part('head');
  g.ellipse(0,-244,68,74).fill(0xffd9b7).stroke({width:7,color:ink});
  g=part('hair');
  g.moveTo(-62,-267).bezierCurveTo(-55,-330,49,-339,62,-269).lineTo(42,-282).lineTo(7,-302).lineTo(-28,-279).closePath().fill(0x26313d);
  let pose=n.pose;
  if(n.point_target){const target=states.get(n.point_target);pose=target&&target.x<n.x?'point_left':'point_right';}
  const left=hand(pose,'hand_left',rig),right=hand(pose,'hand_right',rig);
  g=part('arms');
  line(g,[[-48,-143],[-75,(left[1]-143)/2],left],15,n.color||0x14b8a6);line(g,[[48,-143],[85,(right[1]-143)/2],right],15,n.color||0x14b8a6);
  g=part('hands');
  for(const p of [left,right])g.circle(p[0],p[1],12).fill(0xffd9b7).stroke({width:4,color:ink});
  g=part('face');
  const target=states.get(n.look_target),dx=target?Math.max(-6,Math.min(6,(target.x-n.x)/100)):0;
  g.ellipse(-25,-247,8,11).fill(ink);g.ellipse(25,-247,8,11).fill(ink);
  g.circle(-24+dx,-251,2).fill(0xffffff);g.circle(26+dx,-251,2).fill(0xffffff);
  if(n.expression==='surprised'){g.ellipse(0,-207,12,16).fill(ink);line(g,[[-40,-277],[-13,-285]],5);line(g,[[13,-285],[40,-277]],5);}
  else if(n.expression==='skeptical'){line(g,[[-40,-272],[-13,-263]],5);line(g,[[13,-274],[40,-279]],5);line(g,[[-15,-208],[19,-210]],5);}
  else {g.moveTo(-18,-211).quadraticCurveTo(0,n.expression==='happy'?-184:-199,18,-211).stroke({width:5,color:ink,cap:'round'});line(g,[[-40,-275],[-13,-278]],4);line(g,[[13,-278],[40,-275]],4);}
  return c;
}

export class SceneRenderer {
  app=new Application(); timeline:any; textures=new Map<string,Texture>(); projectId='';
  async init(element:HTMLElement,width=1280,height=720){
    await this.app.init({width,height,antialias:true,autoStart:false,sharedTicker:false,preference:'webgl',preserveDrawingBuffer:true,background:0xf5f0e7});
    this.app.stop();element.appendChild(this.app.canvas);await document.fonts.ready;
  }
  async load(timeline:any,pid:string){
    this.timeline=timeline;this.projectId=pid;
    for(const asset of timeline.assets||[])if(asset.media_type==='image'&&!this.textures.has(asset.id))this.textures.set(asset.id,await Assets.load(`/api/files/${pid}/${asset.id}`));
    await document.fonts.load('48px Arial');await document.fonts.ready;
  }
  drawScene(scene:any,sample:number,alpha=1){
    const root=new Container();root.alpha=alpha;
    const bg=new Graphics().rect(0,0,1920,1080).fill(scene.background);root.addChild(bg);
    const camera=new Container();root.addChild(camera);
    camera.position.set(track(scene.camera?.x,sample,0),track(scene.camera?.y,sample,0));camera.scale.set(track(scene.camera?.scale,sample,1));
    const ev=this.timeline.events.filter((e:any)=>e.scene_id===scene.id);
    const states=new Map<string,any>(scene.nodes.map((n:any)=>[n.id,nodeState(n,ev,sample)]));
    const containers=new Map<string,Container>();camera.sortableChildren=true;
    for(const n of states.values()){
      const c=new Container();c.position.set(n.x,n.y);c.scale.set(n.scale);c.rotation=n.rotation*Math.PI/180;c.pivot.set(n.pivot_x,n.pivot_y);c.zIndex=n.z;c.alpha=n.opacity;c.visible=n.visible&&n.reveal>0;c.sortableChildren=true;
      containers.set(n.id,c);
      if(n.kind==='character')c.addChild(character(n,states,this.timeline.rig||defaultRig));
      else if(n.kind==='text'){
        if(n.highlight>0)c.addChild(new Graphics().roundRect(-14,-8,n.width+28,n.height+16,12).fill({color:0xffd369,alpha:n.highlight}));
        const text=new Text({text:n.text,style:{fontFamily:'Arial',fontSize:n.font_size,fill:n.color,wordWrap:true,wordWrapWidth:n.width,lineHeight:n.font_size*1.28,fontWeight:'600'}});c.addChild(text);
      }
      else if(n.kind==='image'){
        const texture=this.textures.get(n.asset_id);if(!texture)throw new Error(`Missing asset ${n.asset_id}`);
        const sprite=new Sprite(texture);sprite.width=n.width;sprite.height=n.height;c.addChild(sprite);
      }
      else{
        const g=new Graphics();c.addChild(g);
        if(n.kind==='arrow'){line(g,[[0,0],[n.width*n.reveal,0]],8);line(g,[[n.width*n.reveal-24,-18],[n.width*n.reveal,0],[n.width*n.reveal-24,18]],8);}
        else if(n.kind==='path'){
          const pts=n.points;if(pts.length>1){const count=Math.max(2,Math.ceil(pts.length*n.reveal));line(g,pts.slice(0,count),7);}
        }
        else if(n.shape==='stone'){g.moveTo(-n.width/2,-n.height/2).lineTo(n.width/3,-n.height/2-20).lineTo(n.width/2,0).lineTo(n.width/3,n.height/2).lineTo(-n.width/2,n.height/2).closePath().fill(n.color).stroke({width:7,color:ink});}
        else if(n.shape==='circle')g.circle(0,0,n.width/2).fill(n.color).stroke({width:6,color:ink});
        else if(n.shape==='rope')line(g,[[0,0],[n.width*n.reveal,0]],8,0x9b7755);
        else {g.roundRect(-n.width/2,-n.height/2,n.width,n.height,14).fill(n.color).stroke({width:6,color:ink});line(g,[[-n.width/2,-n.height/2],[0,0],[n.width/2,-n.height/2]],4,0x85552f);}
      }
    }
    for(const n of states.values()){
      const c=containers.get(n.id)!;
      if(n.parent_id){const parent=containers.get(n.parent_id);if(!parent)throw new Error('Missing parent');parent.addChild(c);
        if(n.attachment){const p=states.get(n.parent_id),target=states.get(p.point_target),pose=target?(target.x<p.x?'point_left':'point_right'):p.pose,h=hand(pose,n.attachment,this.timeline.rig||defaultRig);c.position.set(h[0]+n.x,h[1]+n.y);}
      } else camera.addChild(c);
    }
    return root;
  }
  frame(index:number){
    if(!this.timeline) return;
    const {fps_num:num,fps_den:den}=this.timeline.output_profile;
    const sample=sampleAt(index,num,den);const scenes=this.timeline.scenes;
    let pos=scenes.findIndex((s:any)=>sample>=s.start_sample&&sample<s.end_sample);
    if(pos<0)pos=scenes.length-1;
    const scene=scenes[pos];
    for(const child of this.app.stage.removeChildren())child.destroy({children:true});
    const wrapper=new Container();wrapper.scale.set(this.app.renderer.width/1920,this.app.renderer.height/1080);this.app.stage.addChild(wrapper);
    if(pos>0&&scene.transition==='dissolve'&&sample<scene.start_sample+scene.transition_samples){
      const u=(sample-scene.start_sample)/scene.transition_samples;
      wrapper.addChild(this.drawScene(scenes[pos-1],Math.min(sample,scenes[pos-1].end_sample-1),1));wrapper.addChild(this.drawScene(scene,sample,u));
    }else wrapper.addChild(this.drawScene(scene,sample));
    this.app.renderer.render(this.app.stage);
  }
  destroy(){this.app.destroy(true,{children:true});}
}
