import {SceneRenderer} from './renderer';
const renderer=new SceneRenderer();
(window as any).loadTimeline=async(timeline:any,pid:string)=>{await renderer.init(document.body,timeline.output_profile.width,timeline.output_profile.height);await renderer.load(timeline,pid);return true;};
(window as any).renderFrame=(index:number)=>{renderer.frame(index);return renderer.app.canvas.toDataURL('image/png').split(',')[1];};
