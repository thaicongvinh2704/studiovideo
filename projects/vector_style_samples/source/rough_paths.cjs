// Convert authored paths using the actual Rough.js generator, without a browser.
const fs=require('fs');
const path=require('path');
const rough=require('../.deps/roughjs/rough.cjs.js');
const input=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
const gen=rough.generator();
const output=input.map((entry,i)=>{
 const drawable=gen.path(entry.d,{seed:100+i,roughness:.95,bowing:.35,stroke:entry.color||'#353c35',strokeWidth:entry.width||1.7,fill:entry.fill||undefined,fillStyle:'hachure',hachureGap:6.5,fillWeight:.55,disableMultiStroke:true,preserveVertices:true});
 return gen.toPaths(drawable);
});
fs.writeFileSync(process.argv[3],JSON.stringify(output));
console.log('Rough.js paths:',output.length);
