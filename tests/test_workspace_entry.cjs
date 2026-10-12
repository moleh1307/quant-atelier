'use strict';
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const gate=fs.readFileSync('static/workspace-entry.js','utf8');
const appSource=fs.readFileSync('static/app.js','utf8').replace(/init\(\);\s*$/,'');
const bank=JSON.parse(fs.readFileSync('static/content.json','utf8'));
const codes=JSON.parse(fs.readFileSync('static/coding.json','utf8'));
const routeQuestions=new Set(bank.lessons.filter(l=>l.path!=='trader').flatMap(l=>l.questions)).size;
const routeCodes=new Set(bank.lessons.filter(l=>l.path!=='trader').flatMap(l=>l.coding)).size;

const key='quant-atelier-preview-entry';
const personal={version:1,updatedAt:1,questions:{},coding:{},lessons:{},drafts:{c01:'my original draft'},trainers:[],preferences:{path:'researcher'}};
const preview={...personal,updatedAt:2,questions:{q20:{solved:true},q21:{selfSolved:true}},coding:{c01:{accepted:true}},lessons:{l10:{passed:true}}};
const storage={'quant-atelier-v1':JSON.stringify(personal),'quant-atelier-qa':JSON.stringify(preview)};
async function boot(url,session={},blocked=false){
  const location={};
  const change=path=>{const u=new URL(path,'http://127.0.0.1:8768');Object.assign(location,{pathname:u.pathname,search:u.search,hash:u.hash});};
  change(url);location.replace=change;
  const app={innerHTML:''},requests=[],errors=[],events={};
  const context={URLSearchParams,location,Date,Math,setTimeout,clearTimeout,console:{error:e=>errors.push(e)},
    sessionStorage:{getItem:k=>{if(blocked)throw Error('blocked');return session[k]||null;},removeItem:k=>{delete session[k];}},
    history:{state:null,replaceState:(_,title,path)=>change(path)},
    localStorage:{getItem:k=>storage[k]||null,setItem:(k,v)=>{storage[k]=v;}},
    fetch:async(url,options)=>{requests.push({url,options});return {ok:true,json:async()=>url==='/content.json'?bank:url==='/coding.json'?codes:{state:personal,revision:'fixture'}};},
    document:{querySelector:s=>s==='#app'?app:s==='#page'?{}:null,addEventListener(){}},window:{addEventListener:(name,fn)=>(events[name]||=[]).push(fn)}};
  vm.createContext(context);vm.runInContext(gate,context);vm.runInContext(appSource,context);
  vm.runInContext('bindPage=()=>{};bindPanels=()=>{};keepNavigationVisible=()=>{};',context);
  await vm.runInContext('init()',context);
  assert.deepEqual(errors,[]);
  return {context,app,requests,events,qa:vm.runInContext('QA',context),record:vm.runInContext('JSON.stringify(state)',context)};
}
(async()=>{
  const hash='#paths/researcher',url='/?qa=1'+hash;
  const before=JSON.stringify(storage);
  for(const oldURL of [url,'/?qa=0'+hash,'/?qa'+hash,'/index.html?qa=1&keep=yes'+hash]){
    const result=await boot(oldURL);
    assert.equal(result.qa,false,'A URL alone never opens preview');
    assert.equal(new URLSearchParams(result.context.location.search).has('qa'),false);
    assert.equal(result.context.location.hash,hash,'Destination survives cleanup');
    assert.match(result.app.innerHTML,new RegExp('0 / '+routeQuestions+' interview problems solved'));
    assert.match(result.app.innerHTML,new RegExp('0 / '+routeCodes+' Python exercises passed'));
    assert.doesNotMatch(result.app.innerHTML,/Test preview|Test problems:/);
    assert.equal(JSON.parse(result.record).drafts.c01,'my original draft');
    assert.ok(result.requests.some(r=>r.url==='/api/progress'),'Ordinary state uses personal disk backup');
    if(oldURL.includes('keep=yes'))assert.equal(result.context.location.search,'?keep=yes');
  }
  for(const ticket of [{at:Date.now()-20000,destination:url},{at:Date.now()+20000,destination:url},{at:Date.now(),destination:'/?qa=1#coding'},'invalid']){
    const session={[key]:JSON.stringify(ticket)};
    assert.equal((await boot(url,session)).qa,false);
    assert.equal(session[key],undefined,'Rejected ticket is discarded');
  }
  assert.equal((await boot(url,{},true)).qa,false,'Storage failure defaults to personal');
  // Exercise the actual development entry button, rather than manufacturing its ticket.
  const session={},elements={'personal-entry':{},'preview-entry':{addEventListener:(name,fn)=>elements.click=fn},'preview-entry-error':{}},navigation=[];
  const entryContext={Date,JSON,location:{hash,assign:path=>navigation.push(path)},document:{getElementById:id=>elements[id]},sessionStorage:{setItem:(k,v)=>session[k]=v}};
  vm.createContext(entryContext);vm.runInContext(fs.readFileSync('static/test-preview.js','utf8'),entryContext);
  assert.equal(session[key],undefined,'Merely viewing the development page grants nothing');
  assert.equal(elements['personal-entry'].href,'/'+hash,'Personal workspace is the default entry action');
  elements.click();assert.deepEqual(navigation,[url]);
  const authorized=await boot(url,session);
  assert.equal(authorized.qa,true);
  assert.equal(session[key],undefined,'Entry is consumed before loading study state');
  assert.match(authorized.app.innerHTML,new RegExp('Test problems: 2 / '+routeQuestions));
  assert.ok(!authorized.requests.some(r=>r.url==='/api/progress'),'Explicit preview never reads or writes personal disk');
  let stopped=false;
  authorized.events.pageshow[0]({persisted:true,stopImmediatePropagation(){stopped=true;}});
  assert.equal(stopped,true,'Cached restore cannot resume app handlers in preview');
  assert.equal(authorized.context.QuantAtelierWorkspace.preview,false);
  assert.equal(authorized.context.location.search,'','Back/Forward cached previews return to the personal destination');
  assert.equal(authorized.context.location.hash,hash);
  const reopened=await boot(url,session);
  assert.equal(reopened.qa,false,'Reload or restored tab defaults back to personal');
  assert.match(reopened.app.innerHTML,new RegExp('0 / '+routeQuestions+' interview problems solved'));
  assert.equal(JSON.stringify(storage),before,'Neither workspace record or draft is replaced');
  const index=fs.readFileSync('static/index.html','utf8');
  assert.ok(index.indexOf('/workspace-entry.js')<index.indexOf('/app.js'),'Workspace is resolved before the app reads storage');
  assert.match(index,/<script src="\/workspace-entry\.js[^\"]*"><\/script>/,'Admission executes synchronously');
  assert.match(appSource,/typeof QuantAtelierWorkspace!==.*undefined/,'Missing admission script defaults to personal');
  console.log('Old preview links, restored tabs, single-use explicit entry, storage failure, destination/draft preservation and disk isolation passed.');
})().catch(error=>{console.error(error);process.exitCode=1;});
