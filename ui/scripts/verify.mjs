import fs from 'node:fs/promises';import path from 'node:path';import crypto from 'node:crypto';import {chromium} from 'playwright';
const root=path.resolve('..'),rt=JSON.parse(await fs.readFile(path.join(root,'runtime.json'),'utf8')),session=JSON.parse(await fs.readFile(path.join(root,'reports/integration-session.json'),'utf8'));
const headers={Authorization:`Bearer ${rt.token}`};const p=(await (await fetch(rt.url+'/api/projects/'+session.project_id,{headers})).json()).result;
const browser=await chromium.launch({channel:'msedge',headless:true});const page=await browser.newPage({viewport:{width:1440,height:1000}});const errors=[];page.on('pageerror',e=>errors.push(e.message));
try {
await page.goto(rt.url+'/#token='+rt.token);await page.waitForFunction(()=>document.querySelector('footer')?.textContent?.startsWith('Core local đã kết nối'));
await page.locator('.projectpick select').selectOption(p.id);await page.locator('nav button').nth(4).click();await page.locator('.previewframe canvas').waitFor();
await page.screenshot({path:path.join(root,'reports/studio-ui.png'),fullPage:true});
await page.goto(rt.url+'/render.html');await page.waitForFunction(()=>typeof window.loadTimeline==='function');await page.evaluate(async({t,pid})=>window.loadTimeline(t,pid),{t:p.timeline,pid:p.id});
const image=async k=>page.evaluate(k=>window.renderFrame(k),k);const first=await image(390);for(let k=350;k<=390;k++)await image(k);const last=await image(390);
if(first!==last)throw new Error('V03 direct seek differs from sequential evaluation');
await fs.writeFile(path.join(root,'reports/fixture-frame.png'),Buffer.from(last,'base64'));
if(errors.length)throw new Error(errors.join('\n'));
await fs.writeFile(path.join(root,'reports/browser-verification.json'),JSON.stringify({V03:'passed: same PNG for direct/sequential frame 390',ui:'real API, canvas preview, no browser page errors',png_sha256:crypto.createHash('sha256').update(Buffer.from(last,'base64')).digest('hex')},null,2));
console.log('UI and V03 verified; screenshots saved under reports/');
} finally {await browser.close();}
