'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const context={console,URLSearchParams,location:{search:'?qa=1',hash:'#courses/l01/journey/researcher/l01'},Math,Date,setTimeout,clearTimeout,document:{querySelector:()=>null}};
vm.createContext(require('./workspace-fixture.cjs')(context));
vm.runInContext(fs.readFileSync('static/app.js','utf8').replace(/init\(\);\s*$/,''),context);
const run=s=>vm.runInContext(s,context);
context.bank=JSON.parse(fs.readFileSync('static/content.json','utf8'));context.codes=JSON.parse(fs.readFileSync('static/coding.json','utf8'));
run("content=bank;coding=codes;route=['courses','l01'];lessonNavigation=()=>'';");
const originals=context.bank.lessons.map(l=>{context.lesson=l;return run('lessonDetail(lesson)');});
vm.runInContext(fs.readFileSync('static/lesson-sample-space.js','utf8'),context);
for(const [i,l] of context.bank.lessons.entries()){
 context.lesson=l;const html=run('lessonDetail(lesson)');
 if(l.id!=='l01'){assert.equal(html,originals[i],'Other lessons are byte-for-byte unchanged');continue;}
 assert.ok(html.includes('sample-space-reading'));
 for(const target of run('lessonSections(lesson)'))assert.equal(html.split('id="'+target.id+'"').length-1,1,'Outline target '+target.id);
 assert.equal(html.split('id="quiz-form"').length-1,1);
 // Strict parsing of the actual rendered authored lesson and every experiment variant.
 const katex=require('../static/vendor/katex/katex.min.js');let spans=0;
 const inspect=value=>{for(const m of value.matchAll(/\\\(([\s\S]*?)\\\)|\\\[([\s\S]*?)\\\]/g)){try{katex.renderToString(m[1]??m[2],{displayMode:m[2]!==undefined,throwOnError:true,strict:'error',trust:false});}catch(error){console.error('Invalid lesson math:',m[1]??m[2],error.message);process.exit(1);}spans++;}};
 inspect(html);
 for(const [event,expected] of [['six',11],['seven',6],['two',1],['double',6]]){context.event=event;const model=run('QuantSampleSpaceLesson.dieGrid(event)');assert.equal(model.count,expected);assert.equal((model.html.match(/class="atlas-dice-cell /g)||[]).length,36);inspect(model.html);}
 for(let n=2;n<=8;n++)for(const ordered of [false,true]){context.n=n;context.ordered=ordered;const pairs=run('QuantSampleSpaceLesson.ballPairs(n,ordered)');assert.equal((pairs.match(/class="atlas-pair"/g)||[]).length,n*(n-1)/(ordered?1:2));inspect(pairs);}
 for(let p=10;p<=90;p+=10){context.chance=p;const weights=run('QuantSampleSpaceLesson.coinWeights(chance)');const shown=[...weights.matchAll(/<span>([\d.]+)%<\/span>/g)].map(m=>Number(m[1]));assert.equal(shown.length,4);assert.ok(Math.abs(shown.reduce((a,b)=>a+b,0)-100)<1e-8);assert.ok(weights.includes(String(Number((1-(1-p/100)**2).toFixed(4)))));inspect(weights);}
 inspect(run('QuantSampleSpaceLesson.replacementTree(false)'));inspect(run('QuantSampleSpaceLesson.replacementTree(true)'));assert.ok(spans>100);
}
// Interactive exploration changes only ephemeral controls. Stable figures keep
// their nodes so transitions survive; keyed records split/merge and can retarget.
const elements={},buttons=[],animations=[];let reduced=false;
context.matchMedia=()=>({matches:reduced});
function node(key,box={left:0,top:0,width:60,height:30}){
 const classes=new Set();
 return {dataset:key?{atlasMotion:key}:{},style:{},attrs:{},textContent:'',innerHTML:'',children:[],
 classList:{toggle(c,on){on?classes.add(c):classes.delete(c);},add(c){classes.add(c);},contains:c=>classes.has(c)},
 addEventListener(type,fn){this[type]=fn;},setAttribute(k,v){this.attrs[k]=v;},removeAttribute(k){delete this.attrs[k];if(k==='data-atlas-motion')delete this.dataset.atlasMotion;},
 getBoundingClientRect(){return {...box};},cloneNode(){return node(key,box);},remove(){this.removed=true;},appendChild(n){this.children.push(n);},
 animate(frames,timing){const a={frames,timing,target:this,cancelled:false,cancel(){this.cancelled=true;}};animations.push(a);return a;}
 };
}
for(const id of ['atlas-heads','atlas-heads-value','atlas-coin-output','atlas-dice-event','atlas-dice-output','atlas-ball-count','atlas-pairs-output','atlas-tree-output'])elements['#'+id]=node();
const rows=Array.from({length:4},()=>{const row=node(),bar=node(),label=node();row.querySelector=s=>s.includes('track')?bar:label;return row;});
const cells=Array.from({length:36},()=>node());
const coinResult=node(),diceResult=node(),diceLabel=node(),diceCount=node(),treeResult=node(),second=[node(),node()];
Object.assign(elements['#atlas-coin-output'],{querySelectorAll:()=>rows,querySelector:()=>coinResult});
Object.assign(elements['#atlas-dice-output'],{querySelectorAll:()=>cells,querySelector:s=>s.includes('label')?diceLabel:s.includes('count')?diceCount:diceResult});
Object.assign(elements['#atlas-tree-output'],{querySelectorAll:()=>second,querySelector:()=>treeResult});
const pairs=elements['#atlas-pairs-output'];let records=[],pairsHtml='';
Object.defineProperty(pairs,'innerHTML',{get:()=>pairsHtml,set(html){pairsHtml=html;records=[...html.matchAll(/data-atlas-motion="([^"]+)"/g)].map((m,i)=>node(m[1],{left:(i%4)*75,top:Math.floor(i/4)*35,width:60,height:30}));}});
pairs.getBoundingClientRect=()=>({left:0,top:0,width:300,height:Math.ceil(records.length/4)*35+70});
pairs.querySelectorAll=()=>records;
pairs.innerHTML=context.QuantSampleSpaceLesson.ballPairs(4,false);
for(const [kind,values] of [['atlasOrder',['unordered','ordered']],['atlasReplace',['no','yes']]])for(const value of values){const b=node();b.dataset[kind]=value;buttons.push(b);}
context.root={querySelector:s=>elements[s],querySelectorAll:s=>buttons.filter(b=>s.includes('order')?b.dataset.atlasOrder:b.dataset.atlasReplace)};
const baseline=run('JSON.stringify(state)');run('QuantSampleSpaceLesson.bind(root,()=>{})');
elements['#atlas-heads'].input({target:{value:'80'}});
assert.equal(elements['#atlas-heads-value'].textContent,'80%');assert.match(coinResult.innerHTML,/0\.96/);
assert.deepEqual(rows.map(r=>Math.round(parseFloat(r.querySelector('track').style.width))),[64,16,16,4]);
assert.equal(elements['#atlas-coin-output'].innerHTML,'','Coin figure is not replaced');
elements['#atlas-dice-event'].change({target:{value:'two'}});
assert.equal(diceCount.textContent,'1 of 36');assert.equal(cells.filter(c=>c.classList.contains('is-event')).length,1);
assert.equal(cells[0].attrs['aria-label'],'Red 1, blue 1, in the event');
assert.equal(elements['#atlas-dice-output'].innerHTML,'','All 36 dice cells remain mounted');
elements['#atlas-dice-event'].change({target:{value:'six'}});assert.equal(cells.filter(c=>c.classList.contains('is-event')).length,11);
const ordered=buttons.find(b=>b.dataset.atlasOrder==='ordered'),unordered=buttons.find(b=>b.dataset.atlasOrder==='unordered');
ordered.click();
assert.equal((pairs.innerHTML.match(/class="atlas-pair"/g)||[]).length,12);
assert.equal(animations.filter(a=>a.target.dataset.atlasMotion?.startsWith('pair-')&&a.frames[0].opacity===0).length,6,'Six reverse orders split from existing pairs');
const firstAnimations=animations.slice();unordered.click();
assert.ok(firstAnimations.every(a=>a.cancelled),'An interruption cancels stale motion');
const ghosts=pairs.children.filter(g=>!g.removed);
assert.equal(ghosts.length,6);assert.ok(ghosts.every(g=>g.attrs['aria-hidden']==='true'&&!g.dataset.atlasMotion),'Merge copies cannot be announced or measured again');
ordered.click();assert.ok(ghosts.every(g=>g.removed),'Interrupted merge copies are cleaned up');
const heightMoves=animations.filter(a=>a.target===pairs);assert.ok(heightMoves.length>0,'Following text tracks changed figure height');
reduced=true;let count=animations.length;unordered.click();assert.equal(animations.length,count,'Reduced motion applies immediately');
assert.equal((pairs.innerHTML.match(/class="atlas-pair"/g)||[]).length,6);
elements['#atlas-ball-count'].change({target:{value:'5'}});ordered.click();assert.equal((pairs.innerHTML.match(/class="atlas-pair"/g)||[]).length,20);
buttons.find(b=>b.dataset.atlasReplace==='yes').click();assert.match(treeResult.innerHTML,/frac\{12\}\{25\}/);
assert.ok(second.every(s=>s.innerHTML.includes('dfrac')),'Both conditional fractions retain their math command');
assert.equal(elements['#atlas-tree-output'].innerHTML,'','Tree routes remain mounted');
reduced=false;count=animations.length;buttons.find(b=>b.dataset.atlasReplace==='no').click();assert.equal(animations.length-count,2,'Only changed conditional fractions move');
const treeAnimations=animations.slice(-2);buttons.find(b=>b.dataset.atlasReplace==='yes').click();assert.ok(treeAnimations.every(a=>a.cancelled));
count=animations.length;buttons.find(b=>b.dataset.atlasReplace==='yes').click();assert.equal(animations.length,count,'Selecting the active option does nothing');
// Browsers without Web Animations still receive the correct final records.
pairs.animate=undefined;unordered.click();assert.equal((pairs.innerHTML.match(/class="atlas-pair"/g)||[]).length,10);
assert.equal(run('JSON.stringify(state)'),baseline);
console.log('Lesson isolation, strict math, exhaustive counts, stable diagrams, split/merge interruption, reduced motion, fallback, and ungraded bindings passed.');
