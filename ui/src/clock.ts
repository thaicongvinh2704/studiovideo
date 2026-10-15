export const RATE=48000;
export function frameAt(sample:number,num=30,den=1,rule='not_before') {
  const a=BigInt(sample)*BigInt(num), b=BigInt(RATE)*BigInt(den);
  return Number(rule==='not_before' ? (a+b-1n)/b : (2n*a+b)/(2n*b));
}
export function sampleAt(frame:number,num=30,den=1) { return frame*RATE*den/num; }
export type KF={sample:number,value:number,easing:'linear'|'smooth'|'hold'};
export function track(keys:KF[]|undefined,sample:number,fallback:number):number {
  if(!keys?.length)return fallback;
  const ks=[...keys].sort((a,b)=>a.sample-b.sample);
  if(sample<ks[0].sample)return fallback;
  for(let i=0;i<ks.length-1;i++){
    const a=ks[i],b=ks[i+1];if(sample>=b.sample)continue;
    if(a.easing==='hold')return a.value;
    let u=(sample-a.sample)/(b.sample-a.sample);if(a.easing==='smooth')u=u*u*(3-2*u);
    return a.value+(b.value-a.value)*u;
  }
  return ks[ks.length-1].value;
}
export function nodeState(node:any,events:any[],sample:number):any {
  const n={...node};
  for(const prop of ['x','y','scale','rotation','opacity','reveal','highlight'])n[prop]=track(node.keyframes?.[prop],sample,node[prop]??(prop==='reveal'?1:0));
  const list=events.filter(e=>e.target_id===node.id&&e.sample<=sample).sort((a,b)=>a.sample-b.sample);
  for(const e of list){
    if(e.action==='pose_swap')n.pose=e.parameters.pose;
    if(e.action==='expression_swap')n.expression=e.parameters.expression;
    if(e.action==='reveal')n.reveal=e.parameters.value??1;
    if(e.action==='text_highlight')n.highlight=e.parameters.value??1;
    if(e.action==='attach'){n.parent_id=e.parameters.parent_id;n.attachment=e.parameters.slot;}
    if(e.action==='point_at')n.point_target=e.parameters.target_id;
    if(e.action==='look_at')n.look_target=e.parameters.target_id;
  }
  n.visible=sample>=node.visible_from&&(node.visible_until==null||sample<node.visible_until);
  return n;
}
