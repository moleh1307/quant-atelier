'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const source=fs.readFileSync('static/app.js','utf8').replace(/init\(\);\s*$/,''),bank=JSON.parse(fs.readFileSync('static/content.json')),codes=JSON.parse(fs.readFileSync('static/coding.json'));
function harness(){
 const nodes={},requests=[],labels={},stages=[],menu=[];let resultWrites=0,renderCalls=0;
 const node=()=>({innerHTML:'',textContent:'',scrollTop:19,scrollLeft:7,selectionStart:3,selectionEnd:9,setAttribute(k,v){this[k]=v;},addEventListener(type,fn){this.events??={};this.events[type]=fn;},classList:{toggle(k,v){this[k]=v;}}});
 for(const selector of ['#page','#code-host','#code','#runner-result','#runner-status','#editor-help','#runner-draft-note','#coding-completion','#runner-notice','.module-continuation p'])nodes[selector]=node();
 let html='Previous receipt';Object.defineProperty(nodes['#runner-result'],'innerHTML',{get:()=>html,set:value=>{html=value;resultWrites++;}});
 for(const action of ['run-code','submit-code','restore-starter']){labels[action]=node();nodes[`[data-action="${action}"]`]={disabled:false,querySelector:()=>labels[action]};}
 for(const stage of ['Understand','Apply','Implement']){const label=node(),evidence=node();label.textContent=stage;stages.push({querySelector:s=>s==='span'?label:evidence,classList:{toggle(k,v){this[k]=v;}},evidence});}
 const marker=node(),meta=node();menu.push({getAttribute:()=> '#coding-list/l01/journey/researcher/l01',querySelector:s=>s==='.activity-marker'?marker:meta,marker,meta});
 const ctx={URLSearchParams,console,Math,Date,AbortController,location:{search:'?qa=1',hash:'#coding/c01/journey/researcher/l01'},bank,codes,document:{querySelector:s=>nodes[s]||null,querySelectorAll:s=>s==='.module-stages a'?stages:s==='.module-menu a'?menu:[]},window:{},sessionStorage:{getItem:()=>null,setItem(){}},localStorage:{getItem:()=>null,setItem(){}},setTimeout:()=>0,clearTimeout(){},fetch:()=>new Promise((resolve,reject)=>requests.push({resolve,reject})),renderFailure:()=>{renderCalls++;throw Error('Editor/page rebuild forbidden');}};
 vm.createContext(require('./workspace-fixture.cjs')(ctx));const run=s=>vm.runInContext(s,ctx);run(source);run('content=bank;coding=codes;state=fresh();route=["coding","c01","journey","researcher","l01"];render=renderFailure;touch=()=>{};announce=()=>{};typesetMath=()=>{};codeEditor={undoHistory:["edit"],selection:[3,9],scrollTop:19,destroy(){throw Error("Editor destroyed");}};view.c01={result:{passed:1,total:1,elapsedMs:1,results:[{passed:true}]},mode:"debug",checkedCode:"old code"};');
 return {run,ctx,nodes,requests,stages,menu,labels,writes:()=>resultWrites,renders:()=>renderCalls};
}
const response=result=>({ok:true,json:async()=>result}),passed={passed:1,total:1,elapsedMs:1,results:[{passed:true}]};
(async()=>{
 const h=harness(),editor=h.run('codeEditor'),host=h.nodes['#code-host'],fields=h.nodes['#code'];
 for(const mode of ['debug','submit']){
  const pending=h.run(`executeCode(coding.find(c=>c.id==='c01'),'${mode}','checked code',[])`);
  assert.equal(h.nodes['#runner-result'].innerHTML,mode==='debug'?'Previous receipt':h.previousHTML,'Pending run keeps old receipt mounted');
  assert.equal(h.nodes['#runner-result']['aria-busy'],'true');assert.equal(h.nodes['[data-action="run-code"]'].disabled,true);assert.match(h.nodes['#runner-status'].textContent,/keep editing/);
  const pendingHTML=h.run('codeDetail(coding.find(c=>c.id==="c01"))');assert.match(pendingHTML,/Checked version/);assert.match(pendingHTML,new RegExp(mode==='debug'?'old code':'checked code'));
  const writes=h.writes();h.run('state.drafts.c01="edited while running"');h.run('updateRunnerDraftNote("c01")');assert.match(h.nodes['#runner-draft-note'].innerHTML,/version sent/);assert.equal(h.writes(),writes);
  const duplicate=h.run('executeCode(coding.find(c=>c.id==="c01"),"submit","duplicate")');await duplicate;assert.equal(h.requests.length,mode==='debug'?1:2);
  h.requests.at(-1).resolve(response(passed));await pending;
  assert.equal(h.nodes['#runner-result']['aria-busy'],'false');assert.equal(h.nodes['[data-action="run-code"]'].disabled,false);assert.match(h.nodes['#runner-result'].innerHTML,/checked code/);assert.equal(h.run('state.drafts.c01'),'edited while running');
  assert.equal(h.run('codeEditor'),editor);assert.equal(h.nodes['#code-host'],host);assert.equal(h.nodes['#code'],fields);assert.equal(fields.scrollTop,19);assert.equal(fields.selectionEnd,9);assert.equal(editor.undoHistory.length,1);assert.equal(h.renders(),0);
  assert.equal(h.run('!!state.coding.c01?.accepted'),mode==='submit');assert.equal(h.stages[2].evidence.textContent,mode==='submit'?'1/3':'0/3');assert.match(h.nodes['.module-continuation p'].textContent,new RegExp(mode==='submit'?'1/3 code passed':'0/3 code passed'));
  if(mode==='submit'){assert.match(h.nodes['#coding-completion'].textContent,/Exercise passed/);assert.equal(h.menu[0].marker.textContent,'○');assert.match(h.menu[0].meta.textContent,/1.*3/);}
  h.previousHTML=h.nodes['#runner-result'].innerHTML;
 }
 const error=h.run('executeCode(coding.find(c=>c.id==="c01"),"debug","broken",[])');h.requests.at(-1).resolve(response({error:'SyntaxError: <script>',errorLine:1}));await error;assert.match(h.nodes['#runner-result'].innerHTML,/Error · check could not finish/);assert.doesNotMatch(h.nodes['#runner-result'].innerHTML,/<script>/);assert.equal(h.run('codeEditor'),editor);assert.equal(h.renders(),0);
 const background=h.run('executeCode(coding.find(c=>c.id==="c01"),"debug","away",[])'),output=h.nodes['#runner-result'].innerHTML;h.run('route=["dashboard"]');h.requests.at(-1).resolve(response(passed));await background;assert.equal(h.nodes['#runner-result'].innerHTML,output);assert.match(h.nodes['#runner-notice'].innerHTML,/View result/);
 const copy=harness();copy.run('view.c01.result.results[0].argumentsJSON="[1,2]";view.c01.result.results[0].expectedJSON="3";bindPage();addDebugCase=(c,selected,label)=>{copied={selected,label};};');
 const copyPending=copy.run('executeCode(coding.find(c=>c.id==="c01"),"submit","new code")');
 await copy.nodes['#page'].events.click({target:{closest:()=>({dataset:{action:'debug-result-case',index:'0'},focus(){}})}});
 assert.equal(copy.run('copied.selected.argumentsJSON'),'[1,2]');assert.equal(copy.run('copied.label'),'Run 1');copy.requests[0].resolve(response(passed));await copyPending;
 console.log('Real Run/Submit lifecycle preserves editor identity/history/selection and old pending receipts; updates completion without rebuild, ignores duplicate clicks, retains live edits, and handles errors/background results.');
})().catch(e=>{console.error(e);process.exitCode=1;});
