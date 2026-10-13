'use strict';
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const ctx={Math,console};vm.createContext(ctx);
for(const name of ['course-textbook.js','lesson-likelihood.js'])vm.runInContext(fs.readFileSync('static/'+name,'utf8'),ctx);
const lesson=ctx.QuantCourseLessons.get('l25'),{logLikelihood:log,relative}=lesson.models;
const close=(a,b)=>assert.ok(Math.abs(a-b)<1e-11,`${a} versus ${b}`);
// Compare against the independent direct probability product on a small grid.
for(let n=1;n<=20;n++)for(let k=0;k<=n;k++)for(let j=0;j<=100;j++){
 const p=j/100,product=p**k*(1-p)**(n-k);
 if(product===0)assert.equal(log(k,n,p),-Infinity);else close(Math.exp(log(k,n,p)),product);
 const r=relative(k,n,p);assert.ok(r>=0&&r<=1+1e-12);
}
close(log(0,10**18,1e-20),-.01);
assert.equal(log(0,10,0),0);assert.equal(log(10,10,1),0);
assert.equal(log(7,10,0),-Infinity);assert.equal(log(7,10,1),-Infinity);
for(const args of [[1,0,.5],[-1,10,.5],[11,10,.5],[.1,10,.5],[1,10,NaN],[1,10,1.1]])assert.throws(()=>log(...args));
for(const n of [10,20,40,100])close(relative(.7*n,n,.7),1);
assert.ok(relative(70,100,.5)<relative(7,10,.5),'Independent evidence concentrates likelihood');
// A minimal DOM checks ungraded controls and interruptible animation ownership.
class El{
 constructor(value=''){this.value=value;this.max='10';this.style={};this.events={};this.attributes={};this.textContent='';}
 addEventListener(name,fn){this.events[name]=fn;}
 setAttribute(name,value){this.attributes[name]=value;}
}
const names=['[data-lk-n]','[data-lk-k]','[data-lk-p]','[data-lk-curve]','[data-lk-k-label]','[data-lk-p-label]','[data-lk-best]','[data-lk-log]','[data-lk-ratio]','[data-lk-peak]','[data-lk-marker]','[data-lk-note]','#likelihood-desc'];
const els=Object.fromEntries(names.map(n=>[n,new El()]));
els['[data-lk-n]'].value='10';els['[data-lk-k]'].value='7';els['[data-lk-p]'].value='50';
const box={isConnected:true,querySelector:s=>els[s]},root={querySelector:()=>box};
// Fake progress functions deliberately throw if exploration tries to earn credit.
ctx.save=ctx.persist=()=>{throw Error('Ungraded exploration must not save progress');};
lesson.bind(root);els['[data-lk-n]'].value='100';els['[data-lk-n]'].events.change();
assert.equal(els['[data-lk-k]'].max,'100');assert.equal(els['[data-lk-k]'].value,'70');
assert.equal(els['[data-lk-best]'].textContent,'p̂ = 0.70');
assert.ok(!els['[data-lk-curve]'].attributes.d.includes('NaN'));
els['[data-lk-p]'].value='0';els['[data-lk-p]'].events.input();
assert.equal(els['[data-lk-log]'].textContent,'−∞');assert.match(els['[data-lk-note]'].textContent,/impossible/);
els['[data-lk-k]'].value='0';els['[data-lk-k]'].events.input();
assert.equal(els['[data-lk-ratio]'].textContent,'1.000');assert.equal(els['[data-lk-log]'].textContent,'0.000');
let next=0,queue=new Map();ctx.requestAnimationFrame=fn=>{queue.set(++next,fn);return next;};ctx.cancelAnimationFrame=id=>queue.delete(id);
ctx.matchMedia=()=>({matches:false});lesson.bind(root);
els['[data-lk-k]'].value='50';els['[data-lk-k]'].events.input();assert.equal(queue.size,1);
els['[data-lk-k]'].value='90';els['[data-lk-k]'].events.input();assert.equal(queue.size,1,'A new target cancels the stale frame');
const tick=time=>{const [id,fn]=queue.entries().next().value;queue.delete(id);fn(time);};
tick(0);tick(220);assert.equal(queue.size,1);tick(440);assert.equal(queue.size,0);
ctx.matchMedia=()=>({matches:true});els['[data-lk-k]'].value='40';els['[data-lk-k]'].events.input();assert.equal(queue.size,0);
const bank=JSON.parse(fs.readFileSync('static/content.json')),codes=JSON.parse(fs.readFileSync('static/coding.json'));
const ids=bank.lessons.filter(l=>l.path==='shared'||l.path==='researcher').map(l=>l.id);
assert.deepEqual(ids.slice(ids.indexOf('l09'),ids.indexOf('l09')+3),['l09','l25','l10']);
assert.equal(ids.length,21);
const meta=bank.lessons.find(l=>l.id==='l25');assert.deepEqual(meta.questions.slice(0,3),['q49','q50','q51']);assert.equal(meta.questions.length,8);assert.deepEqual(meta.coding,['c_l25_easy','c15','c_l25_hard']);
assert.equal(codes.find(c=>c.id==='c15').path,'researcher');
console.log('Likelihood grid, endpoints, stability, ungraded controls, interrupted/reduced motion, new route and practice links passed.');
