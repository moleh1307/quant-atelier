'use strict';
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const bank=JSON.parse(fs.readFileSync('static/content.json')),codes=JSON.parse(fs.readFileSync('static/coding.json'));
const source=fs.readFileSync('static/app.js','utf8').replace(/init\(\);\s*$/,'');
const events={},nodes={},messages=[],saved=[];
const form={addEventListener:(name,fn)=>events[name]=fn,querySelectorAll:selector=>{
 const part=selector.match(/data-check="([^"]+)"/)[1];return Object.values(nodes).filter(el=>el.dataset?.check===part&&el.checked);
}};
const context={console,Math,Date,URLSearchParams,location:{search:'?qa=1',hash:''},bank,codes,
 document:{querySelector:selector=>selector==='#answer-form'?form:selector==='#page'?{addEventListener:(name,fn)=>events['page:'+name]=fn}:nodes[selector]||null},window:{},
 localStorage:{getItem:()=>null,setItem:(k,v)=>saved.push([k,v])},sessionStorage:{getItem:()=>null},setTimeout:()=>0,clearTimeout(){}};
vm.createContext(require('./workspace-fixture.cjs')(context));vm.runInContext(source,context);
const run=s=>vm.runInContext(s,context);context.messages=messages;
run('content=bank;coding=codes;state=fresh();route=["questions"];render=()=>{};announce=m=>messages.push(m);notify=m=>messages.push(m);');
const structured=bank.questions.filter(q=>q.type==='structured');assert.equal(structured.length,76);
const before=run('JSON.stringify(state)');
let masks=0;
for(const q of structured){
 context.q=q;
 const answers=Object.fromEntries(q.checks.map(c=>[c.id,c.type==='numeric'?String(c.answer):c.options.filter(o=>o.correct).map(o=>o.id)]));context.answers=answers;
 assert.equal(run('gradeObjective(q,answers).correct'),true,q.id);
 for(const c of q.checks){
  if(c.type==='numeric'){
   context.bad={...answers,[c.id]:String(c.answer+Math.max(1,Math.abs(c.answer)))};
   assert.equal(run('gradeObjective(q,bad).correct'),false,q.id+' numeric mismatch');
   context.bad={...answers,[c.id]:''};assert.equal(run('gradeObjective(q,bad).complete'),false);
   context.bad={...answers,[c.id]:'alert(1)'};assert.throws(()=>run('gradeObjective(q,bad)'));
  }else{
   // Only one subset can pass. In particular, checking every statement,
   // missing one true statement, or adding any false statement cannot pass.
   let passes=0;
   for(let mask=1;mask<2**c.options.length;mask++){
    context.bad={...answers,[c.id]:c.options.filter((_,i)=>mask&(1<<i)).map(o=>o.id)};
    if(run('gradeObjective(q,bad).correct'))passes++;masks++;
   }
   assert.equal(passes,1,q.id+' exact-set uniqueness');
   context.bad={...answers,[c.id]:[]};assert.equal(run('gradeObjective(q,bad).complete'),false);
   const ids=answers[c.id];context.bad={...answers,[c.id]:[...ids,ids[0]]};assert.equal(run('gradeObjective(q,bad).complete'),false);
   context.bad={...answers,[c.id]:['invented']};assert.equal(run('gradeObjective(q,bad).complete'),false);
  }
 }
 const html=run('questionDetail(q)');
 assert.equal((html.match(/<fieldset /g)||[]).length,q.checks.length,q.id);
 assert.doesNotMatch(html,/My reasoning matched|Save reasoning|No automatic grading/);
 assert.ok(!html.includes(q.checks.find(c=>c.type==='select').options[0].explanation),'Key explanation stays behind solution reveal');
 const renderedIds=[...html.matchAll(/id="([^"]+)"/g)].map(m=>m[1]);assert.equal(new Set(renderedIds).size,renderedIds.length,'Unique keyboard targets '+q.id);
}
assert.equal(run('JSON.stringify(state)'),before,'Rendering/grading pure functions never record credit');
const q=structured.find(q=>q.id==='q_l09_h2');context.q=q;run("route=['questions',q.id,'journey','researcher','l09'];");
function controls(correct){
 for(const key of Object.keys(nodes))delete nodes[key];
 nodes['#scratchpad']={value:'',addEventListener(){}};
 nodes['#answer-feedback']={className:'',textContent:''};
 for(const c of q.checks){
  if(c.type==='numeric')nodes['#check-'+c.id]={value:correct?String(c.answer):'123',dataset:{check:c.id}};
  else c.options.forEach(o=>nodes['#check-'+c.id+'-'+o.id]={value:o.id,checked:correct?o.correct:true,dataset:{check:c.id}});
 }
 run('bindPage()');
}
const submit=()=>events.submit({preventDefault(){},target:form});
controls(false);submit();assert.equal(run('!!state.questions[q.id].solved'),false);assert.equal(run('state.questions[q.id].attempts'),1);
controls(true);submit();assert.equal(run('questionState(q.id).solved'),true);assert.equal(run('state.questions[q.id].assessmentVersion'),'objective-v1');
assert.equal(run('counts().solved'),1);
run('state.questions[q.id]={selfSolved:true,solved:true};state.drafts[q.id]="Earlier derivation remains intact.";');
const legacy=run('JSON.stringify(state)');
assert.equal(run('questionState(q.id).solved'),false);assert.equal(run('questionState(q.id).selfSolved'),false);assert.equal(run('counts().solved'),0);assert.equal(run('backupTotals(state).problems'),0);
assert.match(run('questionDetail(q)'),/Earlier self-assessment kept/);assert.equal(run('JSON.stringify(state)'),legacy,'Compatibility view preserves raw records');
// Explicitly viewing old written work is assistance, and can never promote it.
(async()=>{
 await events['page:click']({target:{closest:()=>({dataset:{action:'legacy-reasoning'},focus(){}})}});
 assert.equal(run('state.questions[q.id].assisted'),true);controls(true);submit();assert.equal(run('questionState(q.id).solved'),false);assert.equal(run('state.questions[q.id].reviewed'),true);
 const raw=run('JSON.stringify(state)');await events['page:click']({target:{closest:()=>({dataset:{action:'self-solved'},focus(){}})}});assert.equal(run('JSON.stringify(state)'),raw,'Retired action cannot award completion');
 run('freshQuestionAttempt(q)');assert.equal(run('state.drafts[q.id]'),'Earlier derivation remains intact.');assert.equal(run('state.drafts[objectiveDraftKey(q)]'),'');assert.equal(run('state.questions[q.id].assisted'),false);
 // Save an actual numeric input and checkbox change; both survive rerender.
 controls(false);const first=q.checks[0],input=nodes['#check-'+first.id];input.value='1/100';events.input({target:input});
 const second=q.checks[1],option=second.options[0],box=nodes['#check-'+second.id+'-'+option.id];box.checked=true;events.input({target:box});
 assert.equal(run('objectiveDraft(q).part1'),'1/100');assert.match(run('objectiveForm(q)'),/value="1\/100"/);assert.ok(run('objectiveDraft(q).part2').includes(option.id));
 run('freshQuestionAttempt(q)');assert.equal(run('objectiveDraft(q).part1'),undefined);run('restoreQuestionAttempt(q)');assert.equal(run('objectiveDraft(q).part1'),'1/100');assert.equal(run('state.questions[q.id].assisted'),true);
 // All current-format passes aggregate correctly across both routes, including
 // restores/exports. Old self assessments never bypass the new checks.
 run("state=fresh();content.questions.forEach(q=>state.questions[q.id]={solved:true,assessmentVersion:q.assessmentVersion});");assert.equal(run('counts().solved'),bank.questions.length);assert.equal(run('backupTotals(state).problems'),bank.questions.length);
 for(const path of ['researcher','trader']){context.path=path;assert.equal(run('routeEvidence(journeyLessons(path)).solved'),run('routeEvidence(journeyLessons(path)).questionTotal'));}
 assert.ok(saved.every(([key])=>key.startsWith('quant-atelier-qa')),'All simulated writes belong to isolated preview');
 console.log(`All ${structured.length} question keys, ${masks} choice subsets, invalid/blank input, real submit/save handlers, versioned progress, assistance, legacy work, fresh/restore and both routes passed.`);
})().catch(e=>{console.error(e);process.exitCode=1;});
