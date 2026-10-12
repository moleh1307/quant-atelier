'use strict';
// Exercise real asynchronous startup, including direct roadmap bookmarks.
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const bank=JSON.parse(fs.readFileSync('static/content.json','utf8'));
const coding=JSON.parse(fs.readFileSync('static/coding.json','utf8'));
(async()=>{
 for(const hash of ['#dashboard','#paths','#paths/trader/step-l20','#courses/l01/journey/trader/l01','#questions/q44/journey/researcher/l18','#coding/c01/journey/researcher/l01']){
  const app={innerHTML:''},errors=[],windowEvents={};let scrolled=false,focused=false;
  const step={open:false,scrollIntoView(){scrolled=true;},querySelector(){return {focus(){focused=true;}};}};
  const context={URLSearchParams,location:{search:'?qa=1',hash},console:{error:e=>errors.push(e)},Math,Date,setTimeout,clearTimeout,
   localStorage:{getItem:()=>null,setItem:()=>{}},fetch:async url=>({json:async()=>url==='/content.json'?bank:coding}),
   document:{querySelector:s=>s==='#app'?app:s==='#page'?{}:null,getElementById:id=>id==='step-l20'?step:null,addEventListener(){}},
   window:{addEventListener:(name,fn)=>windowEvents[name]=fn}};
  vm.createContext(require('./workspace-fixture.cjs')(context));
  vm.runInContext(fs.readFileSync('static/app.js','utf8').replace(/init\(\);\s*$/,''),context);
  // Browser bindings have their own interaction QA; keep the startup order real.
  vm.runInContext('bindPage=()=>{};bindPanels=()=>{};keepNavigationVisible=()=>{};',context);
  await vm.runInContext('init()',context);
  assert.deepEqual(errors,[],hash);
  assert.ok(!app.innerHTML.includes('could not load'),hash);
  assert.ok(app.innerHTML.includes(hash==='#dashboard'?'Overview':hash.startsWith('#paths')?'Learning roadmap':'Current learning module'),hash);
  assert.equal(typeof windowEvents.hashchange,'function');
  assert.ok(app.innerHTML.includes('development test records'),'QA history is explicitly identified');
  assert.ok(app.innerHTML.includes('href="/'+hash+'"'),'Personal link removes the QA parameter and retains the page');
  assert.ok(app.innerHTML.includes('Test preview'));

  if(hash.includes('/journey/'))assert.equal(vm.runInContext('moduleContext().path',context),hash.split('/')[3],'Direct activity bookmark retains its branch');
  if(hash.endsWith('step-l20')){assert.equal(vm.runInContext('preferredPath()',context),'trader','Bookmark retains the chosen route');assert.ok(step.open&&scrolled&&focused,'Bookmarked stop is opened, located and focused after rendering');}
 }
 // Startup must back up newer browser work immediately, not merely claim it did.
 for(const [localStamp,diskStamp,backupOK] of [[200,100,true],[100,200,true],[200,100,false],[100,100,true]]){
  const app={innerHTML:''},errors=[],posts=[],storage={};
  const record=stamp=>({version:1,updatedAt:stamp,questions:{},coding:{},lessons:{},drafts:{c01:'draft-'+stamp},trainers:[]});
  const context={URLSearchParams,location:{search:'',hash:'#dashboard'},console:{error:e=>errors.push(e)},Math,Date,setTimeout,clearTimeout,
   localStorage:{getItem:key=>key==='quant-atelier-v1'?JSON.stringify(record(localStamp)):null,setItem:(key,value)=>storage[key]=value},
   fetch:async(url,options)=>{
    if(options?.method==='POST'){posts.push(JSON.parse(options.body).state);return {ok:backupOK};}
    return {ok:true,json:async()=>url==='/content.json'?bank:url==='/coding.json'?coding:{state:record(diskStamp)}};
   },
   document:{querySelector:s=>s==='#app'?app:s==='#page'?{}:null,addEventListener(){}},window:{addEventListener(){}}};
  vm.createContext(require('./workspace-fixture.cjs')(context));vm.runInContext(fs.readFileSync('static/app.js','utf8').replace(/init\(\);\s*$/,''),context);
  vm.runInContext('bindPage=()=>{};bindPanels=()=>{};keepNavigationVisible=()=>{};',context);
  await vm.runInContext('init()',context);
  assert.deepEqual(errors,[]);
  assert.equal(vm.runInContext('state.updatedAt',context),Math.max(localStamp,diskStamp));
  assert.equal(posts.length,localStamp>diskStamp?1:0);
  if(posts.length)assert.equal(posts[0].drafts.c01,'draft-'+localStamp);
  if(diskStamp>localStamp)assert.equal(JSON.parse(storage['quant-atelier-v1']).drafts.c01,'draft-'+diskStamp);
  assert.equal(vm.runInContext('saveNeedsAttention()',context),!backupOK,'Only save problems need a visible status');
  if(backupOK)assert.ok(app.innerHTML.includes('id="save-status" role="status" aria-live="polite" hidden'), 'Routine success status is hidden');
  else assert.ok(app.innerHTML.includes('disk unavailable'),'Backup failure remains visible');
  assert.ok(!app.innerHTML.includes('development test records'),'Personal startup never displays preview records');
 }
 console.log('Dashboard, roadmap, bookmarked-module startup and fresh-browser/disk reconciliation passed.');
})().catch(e=>{console.error(e);process.exitCode=1;});
