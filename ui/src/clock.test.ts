import {frameAt,sampleAt,nodeState} from './clock';
function assert(condition:boolean,message:string){if(!condition)throw new Error(message);}
for(const [num,den] of [[30,1],[30000,1001],[24,1]])for(const sample of [0,1,672000,21600131,43199999]){
  const k=frameAt(sample,num,den);assert(k*48000*den>=sample*num,'early quantization');assert((k-1)*48000*den<sample*num,'late quantization');
}
const n={id:'prop',x:0,y:0,scale:1,rotation:0,opacity:1,visible_from:0,pose:'neutral',keyframes:{x:[{sample:0,value:0,easing:'linear'},{sample:48000,value:100,easing:'linear'}]}};
const events=[{target_id:'prop',action:'pose_swap',sample:24000,parameters:{pose:'hold'}},{target_id:'prop',action:'attach',sample:30000,parameters:{parent_id:'hand',slot:'hand_right'}}];
const sequential=[0,20,21,30,45].map(frame=>nodeState(n,events,sampleAt(frame)));
assert(JSON.stringify(nodeState(n,events,sampleAt(45)))===JSON.stringify(sequential[4]),'seek changed state');
assert(nodeState(n,events,sampleAt(45)).parent_id==='hand','attachment missing');
assert(frameAt(672000)===420,'known frame anchor');
console.log('V02/V03 TypeScript clock and seek passed');
