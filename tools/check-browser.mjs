import fs from 'node:fs';
const tab=await fetch('http://127.0.0.1:9222/json/new?about:blank',{method:'PUT'}).then(r=>r.json());
const ws=new WebSocket(tab.webSocketDebuggerUrl); await new Promise(r=>ws.addEventListener('open',r,{once:true}));
const requests=new Map();
let seq=0;const pending=new Map();let errors=[],failed=[];
ws.addEventListener('message',e=>{const m=JSON.parse(e.data);if(m.id){pending.get(m.id)?.(m.result);pending.delete(m.id);} if(m.method==='Network.requestWillBeSent')requests.set(m.params.requestId,m.params.request.url); if(m.method==='Runtime.exceptionThrown')errors.push(m.params.exceptionDetails);if(m.method==='Network.responseReceived'&&m.params.response.status>=400)failed.push({url:m.params.response.url,status:m.params.response.status});if(m.method==='Network.loadingFailed')failed.push({url:requests.get(m.params.requestId),error:m.params.errorText});});
function call(method,params={}){return new Promise(r=>{const id=++seq;pending.set(id,r);ws.send(JSON.stringify({id,method,params}));});}
await call('Page.enable');await call('Runtime.enable');await call('Network.enable');
const results=[];
for(const route of ['/','/spectrum/','/xfinity/']){
 errors=[];failed=[];await call('Page.navigate',{url:'http://127.0.0.1:8080'+route});await new Promise(r=>setTimeout(r,3000));
 await call('Runtime.evaluate',{expression:"window.dispatchEvent(new Event('mouseover')); window.scrollTo(0,document.body.scrollHeight)"});await new Promise(r=>setTimeout(r,6000));
 const interaction=await call('Runtime.evaluate',{expression:`JSON.stringify((()=>{const b=document.querySelector('[data-mobile-toggle]');if(!b)return null; const initial=document.body.classList.contains('mobile-nav-open'); b.click();const toggled=document.body.classList.contains('mobile-nav-open')!==initial;b.click();return {mobileMenuToggles:toggled};})())`,returnByValue:true});
 const dom=await call('Runtime.evaluate',{expression:`JSON.stringify({title:document.title,canonical:[...document.querySelectorAll('link[rel="canonical"]')].map(e=>e.href),brokenImages:[...document.images].filter(i=>i.currentSrc&&!i.currentSrc.startsWith('data:')&&(!i.complete||!i.naturalWidth)).map(i=>i.currentSrc),forms:[...document.forms].map(f=>({action:f.action,method:f.method})),jquery:typeof jQuery})`,returnByValue:true});
 results.push({route,interaction:JSON.parse(interaction.result.value),...JSON.parse(dom.result.value),errors:[...new Set(errors)],failed});
}
fs.writeFileSync('browser-check.json',JSON.stringify(results,null,2)+'\n');console.log(JSON.stringify(results,null,2));await call('Page.close');ws.close();
