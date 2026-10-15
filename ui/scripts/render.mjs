import {chromium} from 'playwright';
import fs from 'node:fs/promises';
import path from 'node:path';
import {spawn,spawnSync} from 'node:child_process';
import {once} from 'node:events';
const ctx=JSON.parse(await fs.readFile(process.argv[2],'utf8'));
const p=ctx.project,t=p.timeline,profile=t.output_profile,base=ctx.base;
const output=path.join(ctx.export_dir,`${ctx.job_id}.mp4`);
const nvenc=spawnSync('ffmpeg',['-v','error','-f','lavfi','-i','color=size=320x180:rate=30','-frames:v','1','-c:v','h264_nvenc','-f','null','-'],{windowsHide:true}).status===0;
const encoder=nvenc?'h264_nvenc':'libx264';
const browser=await chromium.launch({channel:'msedge',headless:true});
const page=await browser.newPage({viewport:{width:profile.width,height:profile.height}});
const errors=[];page.on('pageerror',e=>errors.push(e.message));
let child;
async function checked(args){
  const proc=spawn('ffmpeg',args,{windowsHide:true});let err='';proc.stderr.on('data',c=>err+=c);
  const [code]=await once(proc,'close');if(code!==0)throw new Error(err.slice(-2000));
}
try{
  await page.goto(ctx.runtime.url+'/render.html');
  await page.evaluate(async token=>{const r=await fetch('/api/session',{method:'POST',headers:{Authorization:`Bearer ${token}`}});if(!r.ok)throw new Error('Session rejected');},ctx.runtime.token);
  await page.waitForFunction(()=>typeof window.loadTimeline==='function');
  await page.evaluate(async({timeline,pid})=>await window.loadTimeline(timeline,pid),{timeline:t,pid:p.id});
  const files=[],done=[];let cached=0;
  for(const span of t.spans){
    const file=path.join(ctx.cache_dir,`${span.dependency_hash}-${encoder}.mp4`),metadata=file+'.json';
    let reuse=false;
    try{const m=JSON.parse(await fs.readFile(metadata,'utf8'));const stat=await fs.stat(file);reuse=m.dependency_hash===span.dependency_hash&&m.frames===span.end_frame-span.start_frame&&stat.size>0;}catch{}
    if(reuse){cached++;files.push(file);done.push(span.id);process.stdout.write(JSON.stringify({progress:span.end_frame/t.frame_count,checkpoint:{spans:done,encoder}})+'\n');if(p.fixture_notice&&done.length===ctx.parameters.test_pause_after_spans)await new Promise(r=>setTimeout(r,2000));continue;}
    const tmp=file+'.partial.mp4';
    child=spawn('ffmpeg',['-y','-v','error','-f','image2pipe','-vcodec','png','-framerate',`${profile.fps_num}/${profile.fps_den}`,'-i','pipe:0','-an','-c:v',encoder,...(nvenc?['-preset','p4','-cq','20']:['-preset','veryfast','-crf','20']),'-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-video_track_timescale',String(profile.fps_num*1000),tmp],{windowsHide:true});
    let err='';child.stderr.on('data',c=>err+=c);let pipeError;child.stdin.on('error',e=>pipeError=e);
    const closed=once(child,'close');
    for(let k=span.start_frame;k<span.end_frame;k++){
      if(pipeError)throw pipeError;
      if(errors.length)throw new Error(errors.join('\n'));
      const png=Buffer.from(await page.evaluate(k=>window.renderFrame(k),k),'base64');
      if(!child.stdin.write(png))await once(child.stdin,'drain');
      if(k%30===0)process.stdout.write(JSON.stringify({progress:k/t.frame_count,checkpoint:{spans:done,encoder,frame:k}})+'\n');
    }
    child.stdin.end();const [code]=await closed;if(code!==0)throw new Error(err.slice(-2000));child=null;
    await fs.rename(tmp,file);await fs.writeFile(metadata,JSON.stringify({dependency_hash:span.dependency_hash,frames:span.end_frame-span.start_frame,encoder}));
    files.push(file);done.push(span.id);process.stdout.write(JSON.stringify({progress:span.end_frame/t.frame_count,checkpoint:{spans:done,encoder}})+'\n');
  }
  const concat=path.join(ctx.work,'spans.txt');
  await fs.writeFile(concat,files.map(f=>`file '${f.replaceAll('\\','/').replaceAll("'","'\\''")}'`).join('\n'));
  await checked(['-y','-v','error','-f','concat','-safe','0','-i',concat,'-i',path.join(base,p.audio.path),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-ar','48000','-b:a','192k','-af','apad','-t',String(t.frame_count*profile.fps_den/profile.fps_num),'-movflags','+faststart',output]);
  const stamp=s=>{let ms=Math.round(s/48),h=Math.floor(ms/3600000);ms%=3600000;const m=Math.floor(ms/60000);ms%=60000;const sec=Math.floor(ms/1000);return `${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}:${String(sec).padStart(2,'0')},${String(ms%1000).padStart(3,'0')}`;};
  const srt=output.replace('.mp4','.srt');await fs.writeFile(srt,p.utterances.map((u,i)=>`${i+1}\n${stamp(u.start_sample)} --> ${stamp(u.end_sample)}\n${u.raw_text}\n`).join('\n'),'utf8');
  const result={mp4:output,srt,encoder,cpu_fallback:!nvenc,cached_spans:cached,span_count:files.length,timeline_hash:t.hash,subtitle_revision:p.revision,audio_revision:p.audio.id,fixture_notice:p.fixture_notice||null};
  await fs.writeFile(path.join(ctx.work,'result.json'),JSON.stringify(result,null,2));
  await fs.writeFile(output+'.manifest.json',JSON.stringify({result,project_id:p.id,input_revision:p.revision,timeline:t.hash,span_hashes:t.spans.map(s=>s.dependency_hash)},null,2));
}finally{if(child)child.kill();await browser.close();}
