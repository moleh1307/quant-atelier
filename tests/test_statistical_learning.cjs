'use strict';
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const ctx={console,Math};vm.createContext(ctx);for(const f of ['course-textbook.js','lesson-statistical-learning.js'])vm.runInContext(fs.readFileSync('static/'+f,'utf8'),ctx);const lesson=ctx.QuantCourseLessons.get('l29'),M=lesson.models;
// Repeated training-noise enumeration rather than the model's moment formula.
for(const lambda of [0,.05,.5,1,2,6]){
 const estimates=[];for(const u of [-1,1])for(const v of [-1,1])estimates.push([2*(2+u)/(4+lambda),.5*v/(.25+lambda)]);
 const means=[0,1].map(j=>estimates.reduce((s,b)=>s+b[j],0)/4),bias=(means[0]-1)**2+means[1]**2,variance=estimates.reduce((s,b)=>s+(b[0]-means[0])**2+(b[1]-means[1])**2,0)/4;
 assert.ok(Math.abs(M.risk(lambda).bias-bias)<1e-12);assert.ok(Math.abs(M.risk(lambda).variance-variance)<1e-12);assert.ok(Math.abs(M.risk(lambda).total-bias-variance)<1e-12);
}
assert.equal(M.risk(0).total,4.25);assert.ok(Math.abs(M.risk(1).total-.36)<1e-12);
for(const z of [-2,-.6,0,.6,2])for(const lambda of [0,.1,.6,1,2,2.4]){
 const b=M.soft(z,lambda),score=z-b;assert.ok(b?Math.abs(score-lambda*Math.sign(b))<1e-12:Math.abs(score)<=lambda+1e-12);
}
assert.equal(M.path(.6).lasso[1],0);assert.ok(M.path(2).ridge[1]>0);assert.equal(M.path(2).lasso[0],0);
let sequence=0,queue=new Map(),drawn=[],cancels=0;ctx.requestAnimationFrame=fn=>{queue.set(++sequence,fn);return sequence;};ctx.cancelAnimationFrame=id=>{queue.delete(id);cancels++;};ctx.matchMedia=()=>({matches:false});const root={isConnected:true},move=M.animate(1,v=>drawn.push(v),root);function tick(time){const jobs=[...queue.values()];queue.clear();for(const fn of jobs)fn(time);}
move(5);tick(0);tick(180);assert.equal(drawn.at(-1),3);move(1);tick(200);assert.equal(drawn.at(-1),3);tick(380);assert.equal(drawn.at(-1),2);tick(560);assert.equal(drawn.at(-1),1);assert.ok(cancels>0);move(4);root.isConnected=false;const n=drawn.length;tick(600);assert.equal(drawn.length,n);assert.equal(queue.size,0);root.isConnected=true;ctx.matchMedia=()=>({matches:true});move(6);assert.equal(drawn.at(-1),6);delete ctx.requestAnimationFrame;ctx.matchMedia=()=>({matches:false});move(2);assert.equal(drawn.at(-1),2);
function el(value=''){return {value,textContent:'',innerHTML:'',dataset:{},attrs:{},events:{},setAttribute(k,v){this.attrs[k]=v;},addEventListener(k,fn){this.events[k]=fn;}};}
const ids={};for(const id of ['risk-lambda','risk-label','risk-guide','risk-result','path-lambda','path-label','path-guide','path-result'])ids['#learn-'+id]=el();ids['#learn-risk-lambda'].value='1';ids['#learn-path-lambda'].value='.5';const risks=['total','bias','variance'].map(k=>{const x=el();x.dataset.learnRisk=k;return x;}),paths=['ridge-0','ridge-1','lasso-0','lasso-1'].map(k=>{const x=el();x.dataset.learnPath=k;return x;});const host={isConnected:true,querySelector:s=>ids[s],querySelectorAll:s=>s==='[data-learn-risk]'?risks:paths};lesson.bind(host);
for(const value of [0,.5,1,6]){ids['#learn-risk-lambda'].value=String(value);ids['#learn-risk-lambda'].events.input();assert.ok(ids['#learn-risk-result'].innerHTML.includes('excess risk'));assert.ok(!/NaN|Infinity/.test(ids['#learn-risk-result'].innerHTML));for(const node of risks)assert.ok(Number.isFinite(node.attrs.cx)&&Number.isFinite(node.attrs.cy));assert.equal(risks.length,3);}
for(const value of [.5,.6,1,2.4]){ids['#learn-path-lambda'].value=String(value);ids['#learn-path-lambda'].events.input();assert.ok(ids['#learn-path-result'].innerHTML.includes('Lasso'));assert.ok(!/NaN|Infinity/.test(ids['#learn-path-result'].innerHTML));assert.equal(paths.length,4);}
assert.equal(paths[2].attrs.cy,330);assert.equal(paths[3].attrs.cy,330);
const bank=JSON.parse(fs.readFileSync('static/content.json')),codes=JSON.parse(fs.readFileSync('static/coding.json'));const app={console,Math,Date,URLSearchParams,setTimeout,clearTimeout,location:{search:'',hash:''},document:{querySelector:()=>null},bank,codes};vm.createContext(require('./workspace-fixture.cjs')(app));const run=s=>vm.runInContext(s,app);run(fs.readFileSync('static/app.js','utf8').replace(/init\(\);\s*$/,''));run('content=bank;coding=codes;state=fresh();');const before=run('JSON.stringify(state)');
for(const [id,next] of [['l11','l29'],['l29','l12']]){run(`route=['coding-list','${id}','journey','researcher','${id}'];`);assert.equal(run('followingActivity(moduleContext()).href'),`#courses/${next}/journey/researcher/${next}`);}
run("route=['question-list','l29','journey','researcher','l29'];");assert.equal((run("topicPracticePage('questions')").match(/class="topic-practice-row"/g)||[]).length,6);run("route=['coding-list','l29','journey','researcher','l29'];");assert.equal((run("topicPracticePage('coding')").match(/class="topic-practice-row"/g)||[]).length,3);assert.equal(run('JSON.stringify(state)'),before);
console.log('Independent ridge risk, lasso subgradients, stable figure bindings, interruption/reduced motion and l11→l29→l12 journey passed.');
