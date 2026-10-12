'use strict';
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const source=fs.readFileSync('static/app.js','utf8').replace(/init\(\);\s*$/,'');
const bank=JSON.parse(fs.readFileSync('static/content.json')),codes=JSON.parse(fs.readFileSync('static/coding.json'));
function harness(){
 const requests=[],events={},nodes={};
 for(const id of ['#page','#code','#code-host','#editor-help','#editor-position','#runner-notice','#runner-draft-note','#debug-arguments','#debug-expected','#debug-enabled','#debug-feedback','#submission-case'])nodes[id]={value:'',innerHTML:'',textContent:'',addEventListener:(type,fn)=>events[id+type]=fn,focus(){}};
 const ctx={URLSearchParams,location:{search:'?qa=1',hash:'#coding/c01'},Math,Date,console,AbortController,document:{querySelector:s=>nodes[s]||null},localStorage:{getItem:()=>null,setItem(){}},sessionStorage:{getItem:()=>null,setItem(){}},window:{},setTimeout:()=>0,clearTimeout(){},bank,codes,fetch:(url,options)=>new Promise(resolve=>requests.push({url,options,resolve}))};
 vm.createContext(require('./workspace-fixture.cjs')(ctx));vm.runInContext(source,ctx);const run=s=>vm.runInContext(s,ctx);run('content=bank;coding=codes;route=["coding","c01"];render=()=>{};announce=()=>{};touch=()=>{};');return {ctx,run,requests,nodes,events};
}
function event(key,extra={}){return {key,metaKey:true,prevented:false,stopped:false,preventDefault(){this.prevented=this.defaultPrevented=true;},stopPropagation(){this.stopped=true;},...extra};}
const result={mode:'debug',passed:0,total:1,elapsedMs:1,results:[{passed:null,actual:'None',argumentsJSON:'[[],0]'}]};
(async()=>{
 const h=harness();assert.equal(h.run('debugCases(coding[0]).cases.length'),codes[0].samples.length);
 h.ctx.copy={argumentsJSON:'[[9007199254740993,null],0]',expectedJSON:'null'};
 h.run('addDebugCase(coding[0],copy,"Submission 9")');assert.equal(h.run('debugCases(coding[0]).cases[1].argumentsJSON'),h.ctx.copy.argumentsJSON);
 const persisted=h.run('state.drafts["c01-tests"]');h.run('route=["coding","c02"];addDebugCase(coding[1]);route=["coding","c01"]');assert.equal(h.run('state.drafts["c01-tests"]'),persisted);
 h.run('bindPage()');h.events['#debug-argumentsinput']({target:{value:'[invalid'}});assert.match(h.run('state.drafts["c01-tests"]'),/invalid/);h.run('startCodeCheck(coding[0],"debug")');assert.equal(h.requests.length,0);assert.match(h.nodes['#debug-feedback'].textContent,/Submission 9/);
 h.events['#debug-argumentsinput']({target:{value:h.ctx.copy.argumentsJSON}});h.events['#debug-expectedinput']({target:{value:''}});
 h.run('const rec=debugCases(coding[0]);rec.cases[0].enabled=false;saveDebugCases(coding[0],rec);codeEditor={getValue:()=>"def solve(a,b): return None"};');
 const pending=h.run('startCodeCheck(coding[0],"debug")');const payload=JSON.parse(h.requests[0].options.body);assert.equal(payload.mode,'debug');assert.deepEqual(payload.cases,[{argumentsJSON:h.ctx.copy.argumentsJSON,expectedJSON:''}]);assert.equal(payload.code,'def solve(a,b): return None');
 h.run('const changed=debugCases(coding[0]);changed.cases[1].expectedJSON="null";saveDebugCases(coding[0],changed)');assert.match(h.run('runnerDraftNote(coding[0])'),/debugging cases changed/);assert.equal(h.run('view.c01.checkedCases[0].expectedJSON'),'');
 h.run('state.drafts.c01="new code"');h.requests[0].resolve({ok:true,json:async()=>result});await pending;assert.equal(h.run('!!state.coding.c01?.accepted'),false);assert.match(h.run('runnerHTML(view.c01.result,"debug")'),/completion unchanged|output inspected/);assert.equal(h.run('validRunnerResult({...view.c01.result,mode:"submit"})'),false);
 h.run('const none=debugCases(coding[0]);none.cases.forEach(t=>t.enabled=false);saveDebugCases(coding[0],none)');assert.throws(()=>h.run('debugRunCases(coding[0])'),/at least one/);
 h.run('view.c01.result={results:[copy]};view.c01.mode="submit"');await h.events['#pageclick']({target:{closest:()=>({dataset:{action:'debug-result-case',index:'0'},focus(){}})}});assert.equal(h.run('debugCases(coding[0]).cases.at(-1).argumentsJSON'),h.ctx.copy.argumentsJSON);
 await h.events['#pageclick']({target:{closest:()=>({dataset:{action:'remove-debug-case'},focus(){}})}});assert.equal(h.run('debugCases(coding[0]).cases.length'),2);
 const limits=harness();limits.ctx.big=JSON.stringify(['x'.repeat(300000),0]);
 limits.run('addDebugCase(coding[0],{argumentsJSON:big,expectedJSON:"null"},"Large copied case");const lr=debugCases(coding[0]);lr.cases[0].enabled=false;saveDebugCases(coding[0],lr)');
 assert.equal(limits.run('debugRunCases(coding[0])[0].argumentsJSON'),limits.ctx.big);
 limits.ctx.oversize=' '.repeat(500001);
 limits.run('const over=debugCases(coding[0]);over.cases[1].argumentsJSON=oversize;saveDebugCases(coding[0],over)');
 assert.throws(()=>limits.run('debugRunCases(coding[0])'),/500,000/);
 const merging=harness();merging.run('state.drafts["c01-tests"]="local cases";browserBase=cloneRecord(state);const remote=cloneRecord(state);remote.drafts["c01-tests"]="other tab cases";receiveExternal(remote)');assert.equal(merging.run('state.drafts["c01-tests"]'),'local cases');assert.equal(merging.run('syncConflict.conflicts[0].id'),'c01-tests');
 const keys=harness();keys.ctx.calls=[];keys.run('startCodeCheck=(c,mode)=>calls.push(mode)');
 for(const [key,mode] of [["'",'debug'],['Enter','submit']]){const e=event(key);keys.ctx.e=e;assert.equal(keys.run('handleCodingShortcut(e,coding[0])'),true);assert.equal(e.prevented,true);assert.equal(e.stopped,true);assert.equal(keys.ctx.calls.at(-1),mode);}
 for(const extra of [{repeat:true},{isComposing:true},{ctrlKey:true},{altKey:true},{shiftKey:true},{metaKey:false},{defaultPrevented:true}]){const count=keys.ctx.calls.length;keys.ctx.e=event('Enter',extra);keys.run('handleCodingShortcut(e,coding[0])');assert.equal(keys.ctx.calls.length,count);}
 keys.run('view.c01={running:true}');keys.ctx.e=event("'");keys.run('handleCodingShortcut(e,coding[0])');assert.equal(keys.ctx.calls.length,2);assert.equal(keys.ctx.e.prevented,true);
 const fallback=harness();fallback.run('bindPage();startCodeCheck=(c,mode)=>{shortcutMode=mode};');const e=event('Enter',{target:{closest:()=>true}});fallback.events['#pagekeydown'](e);assert.equal(fallback.ctx.shortcutMode,'submit');assert.equal(e.prevented,true);
 const mounted=harness();mounted.ctx.QuantPythonEditor={mount:options=>{mounted.ctx.mountOptions=options;return {getValue:()=>''};}};mounted.run('bindPage();startCodeCheck=(c,mode)=>{shortcutMode=mode}');assert.equal(mounted.ctx.mountOptions.onShortcut(event("'")),true);assert.equal(mounted.ctx.shortcutMode,'debug');
 const loading=harness(),loaded=loading.run('loadSubmissionCases(coding[0])');assert.equal(loading.requests[0].url,'/api/coding-cases');loading.requests[0].resolve({ok:true,json:async()=>({cases:[{...h.ctx.copy,caseNumber:1}]})});await loaded;assert.equal(loading.run('view.c01.officialCases[0].argumentsJSON'),h.ctx.copy.argumentsJSON);assert.equal(loading.run('Object.keys(state.coding).length'),0);
 console.log('Custom case editing/persistence, validation, exact copies, optional expected without credit, official case loading, editor/fallback shortcuts and duplicate guards passed.');
})().catch(e=>{console.error(e);process.exitCode=1;});
