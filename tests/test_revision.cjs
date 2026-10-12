'use strict';
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const source=fs.readFileSync('static/app.js','utf8').replace(/init\(\);\s*$/,'');
const bank=JSON.parse(fs.readFileSync('static/content.json','utf8')),codes=JSON.parse(fs.readFileSync('static/coding.json','utf8'));
const events={},nodes={},messages=[],frames=[];
for(const id of ['page','answer-form','answer','scratchpad','confidence'])nodes[id]={value:'',addEventListener:(name,fn)=>events[id+':'+name]=fn,focus(){this.focused=true;},scrollIntoView(){this.scrolled=true;}};
const context={console,Date,Math,URLSearchParams,location:{search:'?qa=1',hash:'#questions/q01/revision'},bank,codes,requestAnimationFrame:fn=>frames.push(fn),setTimeout:()=>0,clearTimeout(){},document:{querySelector:s=>nodes[s.slice(1)]||null},localStorage:{getItem:()=>null,setItem(){}},sessionStorage:{getItem:()=>null,setItem(){}},window:{}};
vm.createContext(require('./workspace-fixture.cjs')(context));vm.runInContext(source,context);const run=s=>vm.runInContext(s,context),drain=()=>{while(frames.length)frames.shift()();};context.messages=messages;
run('content=bank;coding=codes;route=["questions","q01","revision"];notify=message=>messages.push(message);announce=message=>messages.push(message);render=()=>{renderEpoch++;};');
const baseline=run('JSON.stringify(state)');assert.match(run('review()'),/queue is empty/);assert.equal(run('JSON.stringify(state)'),baseline);
run('state.questions={q01:{reviewed:true,due:Date.now()-1000},q02:{selfSolved:true,due:Date.now()-2000},q21:{reviewed:true,due:Date.now()+86400000},obsolete:{due:1}};');
assert.equal(run('dueQuestions().map(q=>q.id).join(",")'),'q02,q01');const queue=run('review()');assert.ok(queue.indexOf('#questions/q02/revision')<queue.indexOf('#questions/q01/revision'));assert.match(queue,/Self-assessed/);assert.doesNotMatch(queue,/self-solved|obsolete/);assert.match(queue,/#questions\/q21\/revision/);assert.match(run('questionDetail(content.questions[0])'),/Revision session/);assert.match(run('revisionContext(content.questions[0])'),/Next due: A sum changes the sample space/);
run('state.drafts.q01="11/36";state.drafts["q01-scratch"]="old scratch <script>";state.questions.q01.reveal=true;state.questions.q01.hints=2;state.questions.q01.assisted=true;bindPage();');
const click=action=>events['page:click']({target:{closest:()=>({dataset:{action},focus(){}})}});
(async()=>{
 await click('new-attempt');drain();assert.equal(run('state.drafts.q01'),'');assert.equal(run('state.drafts["q01-scratch"]'),'');assert.equal(run('state.drafts["q01-previous"]'),'11/36');assert.equal(run('state.questions.q01.reveal'),false);assert.equal(run('state.questions.q01.assisted'),false);assert.equal(nodes.answer.focused,true);assert.equal(nodes.answer.scrolled,true);
 // Restarting an empty attempt retains the previously kept text. Showing it marks assistance.
 await click('new-attempt');await click('previous-attempt');assert.equal(run('state.questions.q01.assisted'),true);assert.match(run('previousAttempt(content.questions[0])'),/old scratch &lt;script&gt;/);assert.doesNotMatch(run('previousAttempt(content.questions[0])'),/<script>/);
 run('state.drafts.q01="my newer work";');await click('restore-attempt');assert.equal(run('state.drafts.q01'),'11/36');assert.equal(run('state.drafts["q01-previous"]'),'my newer work');assert.equal(run('state.questions.q01.assisted'),true);
 nodes.confidence.value='7';const now=Date.now();await click('schedule');assert.ok(run('state.questions.q01.due')>=now+7*86400000);assert.match(run('questionDetail(content.questions[0])'),/Next revision:/);assert.equal(run('dueQuestions().length'),1);assert.equal(run('counts().solved'),0,'Scheduling and text recovery earn no solve');
 nodes.confidence.value='999';const due=run('state.questions.q01.due');await click('schedule');assert.equal(run('state.questions.q01.due'),due);
 run('route=["questions","q21","revision"];state.questions.q21={};state.drafts.q21="";bindPage();');await click('self-solved');assert.equal(run('!!state.questions.q21.selfSolved'),false);assert.match(messages.at(-1),/Compare/);await click('solution');await click('self-solved');assert.match(messages.at(-1),/Write your reasoning/);assert.equal(run('!!state.questions.q21.selfSolved'),false);
 run('state.drafts.q21="The residuals are orthogonal to the intercept column, so their sum is zero.";');await click('self-solved');assert.equal(run('state.questions.q21.selfSolved'),true);assert.equal(run('state.questions.q21.solved'),undefined,'A written self-assessment is not a numeric solve');
 run('state.questions.q02.due=Date.now()+86400000;');assert.match(run('review()'),/Nothing due today/);assert.equal(run('dueQuestions().length'),0);
 run('route=["questions","q01","journey","trader","l01"];state.questions.q01.reveal=true;');assert.match(run('questionDetail(content.questions[0])'),/href="#courses\/l01\/journey\/trader\/l01"/);assert.doesNotMatch(run('revisionContext(content.questions[0])'),/Revision session/);
 console.log('Revision empty/due/upcoming states, chronological queue, readable provenance, exact return, fresh/restored drafts, assistance, scheduling, self-assessment guards and related-module continuity passed.');
})().catch(error=>{console.error(error);process.exitCode=1;});
