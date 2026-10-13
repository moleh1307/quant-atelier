'use strict';
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const katex=require('../static/vendor/katex/katex.min.js');
const context={console,URLSearchParams,location:{search:'?qa=1',hash:'#courses/l02/journey/researcher/l02'},Math,Date,setTimeout,clearTimeout,document:{querySelector:()=>null}};
vm.createContext(require('./workspace-fixture.cjs')(context));const run=s=>vm.runInContext(s,context);
run(fs.readFileSync('static/app.js','utf8').replace(/init\(\);\s*$/,''));
context.bank=JSON.parse(fs.readFileSync('static/content.json'));context.codes=JSON.parse(fs.readFileSync('static/coding.json'));
run("content=bank;coding=codes;route=['courses','l02'];lessonNavigation=()=>'';");
run(fs.readFileSync('static/lesson-sample-space.js','utf8'));
const before=new Map(context.bank.lessons.map(l=>{context.lesson=l;return [l.id,run('lessonDetail(lesson)')];}));
for(const name of ['course-textbook.js','lesson-conditioning.js','lesson-expectation.js','lesson-distributions.js','lesson-stopping.js','lesson-arithmetic.js','lesson-variance.js','lesson-data-time.js','lesson-estimation.js','lesson-likelihood.js','lesson-covariance.js','lesson-regression.js','lesson-inference.js','lesson-time-series.js','lesson-validation.js','lesson-search.js','lesson-research-defence.js','lesson-monte-carlo.js','lesson-algorithms.js','lesson-fair-value.js','lesson-order-flow.js','lesson-continuation-growth.js','lesson-joint-risk.js','lesson-finance-core.js','lesson-strategic-calibration.js','lesson-calculus.js','lesson-optimization.js','lesson-resampling.js'])run(fs.readFileSync('static/'+name,'utf8'));
const targets=new Set(['l02','l03','l04','l05','l06','l07','l08','l09','l10','l11','l12','l13','l14','l15','l16','l17','l18','l19','l20','l21','l22','l23','l24','l25','l26','l27','l28']);let spans=0;
const decode=s=>s.replace(/&(amp|lt|gt|quot|#39);/g,(_,k)=>({amp:'&',lt:'<',gt:'>',quot:'"','#39':"'"}[k]));
function inspect(html){for(const match of html.matchAll(/\\\(([\s\S]*?)\\\)|\\\[([\s\S]*?)\\\]/g)){const encoded=match[1]??match[2];assert.ok(!encoded.includes('<'),'TeX comparisons must remain text, not browser markup');try{katex.renderToString(decode(encoded),{displayMode:match[2]!==undefined,throwOnError:true,strict:'error',trust:false});}catch(error){assert.fail('Authored math '+decode(encoded)+': '+error.message);}spans++;}}
for(const l of context.bank.lessons){context.lesson=l;const html=run('lessonDetail(lesson)');
 if(!targets.has(l.id)){assert.equal(html,before.get(l.id),'Untouched rendering '+l.id);continue;}
 assert.notEqual(html,before.get(l.id));assert.equal((html.match(/id="quiz-form"/g)||[]).length,1);assert.ok(html.includes('sample-space-reading'));
 for(const s of run('lessonSections(lesson)')){assert.equal(html.split('id="'+s.id+'"').length-1,1,l.id+' target '+s.id);assert.ok(run('lessonOutline(lesson)').includes(s.title.replace(/&/g,'&amp;')));}
 // Original choices and grading data stay in the shared renderer.
 for(const label of l.optionLabels)assert.ok(html.includes('aria-label="'+label+'"'));
 if(l.id==='l08')assert.equal((html.match(/class="course-code"/g)||[]).length,2,'Purposeful Python in the timing argument');else if(l.id==='l17')assert.equal((html.match(/class="course-code"/g)||[]).length,1,'Independent simulation units justify this Python example');else if(l.id==='l18')assert.equal((html.match(/class="course-code"/g)||[]).length,2,'State invariants justify streaming and deque code');else if(l.id==='l26')assert.equal((html.match(/class="course-code"/g)||[]).length,1,'Stable loss evaluation justifies the numerical example');else assert.ok(!/<pre[ >]/.test(html),'No forced code block in other topics');inspect(html);
}
assert.equal(run("lessonSections(content.lessons.find(l=>l.id==='l03')).length"),8,'Six authored sections plus example/check, rather than copied seven-section template');
const registry=context.QuantCourseLessons;
const alg=registry.get('l18').models;
const algorithmCheck=spawnAlgorithmCheck();
function spawnAlgorithmCheck(){
 const {spawnSync}=require('node:child_process');
 const result=spawnSync('python3',['-c',String.raw`
import sys, json, itertools, math
sources=json.load(sys.stdin)
ns={}
exec(sources[0],ns);exec(sources[1],ns)
moments,maxima=ns['moments'],ns['maxima']
assert moments([])==(None,None,None)
assert moments([9])==(9,0,None)
assert moments([2,4,6])==(4,8/3,4)
assert moments([10**12+2,10**12+4,10**12+6])==(10**12+4,8/3,4)
for n in range(7):
 for seq in itertools.product([-2,0,3],repeat=n):
  for k in range(1,n+3):
   expected=[max(seq[i:i+k]) for i in range(n-k+1)]
   assert maxima(seq,k)==expected,(seq,k)
  if n:
   mu=sum(seq)/n;v=sum((x-mu)**2 for x in seq)/n
   mean,var,sample=moments(seq)
   assert math.isclose(mean,mu,abs_tol=1e-12)
   assert math.isclose(var,v,abs_tol=1e-12)
   if n>1:assert math.isclose(sample,v*n/(n-1),abs_tol=1e-12)
print('Actual authored algorithms passed exhaustive small windows and variance references.')
`],{input:JSON.stringify([alg.varianceSource,alg.maximumSource]),encoding:'utf8'});
 assert.equal(result.status,0,result.stderr);console.log(result.stdout.trim());return result;
}
assert.equal(alg.moments([2,4,6]).m2,8);
for(const seq of [[4,2,5,1],[3,3,3],[1,2,3],[3,2,1]])for(const k of [1,2,4]){
 let inserted=0,removed=0;
 for(const row of alg.trace(seq,k)){
  inserted++;removed+=row.expired.length+row.dominated.length;
  assert.ok(row.candidates.every(j=>j>row.i-k&&j<=row.i));
  for(let a=1;a<row.candidates.length;a++){assert.ok(row.candidates[a]>row.candidates[a-1]);assert.ok(seq[row.candidates[a]]<seq[row.candidates[a-1]]);}
  assert.equal(row.maximum,row.i>=k-1?Math.max(...seq.slice(row.i-k+1,row.i+1)):null);
 }
 assert.ok(removed<=inserted);
}
for(const source of [alg.varianceSource,alg.maximumSource])assert.equal(decode(registry.python(source).replace(/^<pre[^>]*><code>/,'').replace(/<\/code><\/pre>$/,'').replace(/<\/?span[^>]*>/g,'')),source);
assert.equal(registry.math('0<U<V<1'),'\\(0&lt;U&lt;V&lt;1\\)');
assert.equal(decode(registry.math(String.raw`\begin{matrix}1&2\\3&4\end{matrix}`)),String.raw`\(\begin{matrix}1&2\\3&4\end{matrix}\)`);
const wm=registry.get('l02').models;
for(let prior=10;prior<=90;prior+=10)for(let heads=0;heads<=6;heads++){
 const x=wm.weights(prior,heads),odds=prior/(100-prior)*2**heads;
 assert.ok(Math.abs(x.posterior-odds/(1+odds))<1e-12);assert.ok(Math.abs(x.predict-(.5+.5*x.posterior))<1e-12);inspect(wm.weightResult(x));
}
const im=registry.get('l03').models;
for(let n=2;n<=10;n++){
 let sum=0,square=0;
 for(let bits=0;bits<2**n;bits++){const record=Array.from({length:n},(_,i)=>bits&(1<<i)?'H':'T').join('');const count=im.indicators(record).count;sum+=count;square+=count*count;}
 const mean=sum/2**n,variance=square/2**n-mean*mean;assert.equal(mean,(n-1)/4);assert.equal(variance,(5*n-7)/16);
}
assert.equal(im.indicators('HHHHTT').count,3);assert.equal(im.indicators('HTHTHT').count,0);
let maxSum=0,minSum=0;for(let x=1;x<=6;x++)for(let y=1;y<=6;y++){maxSum+=Math.max(x,y);minSum+=Math.min(x,y);}assert.equal(maxSum,161);assert.equal(minSum,91);
const dm=registry.get('l04').models;
for(let age=0;age<=9;age++){const x=dm.remaining(age);assert.equal(x.exponential,.5);assert.equal(x.total,age+.5);assert.equal(x.uniform,(10-age)/2);inspect(dm.waitResult(x));}
assert.ok(!/NaN|Infinity/.test(dm.curve(x=>x*x,1)));
const sm=registry.get('l05').models;
for(const pattern of ['HH','HT']){
 for(let n=0;n<=10;n++)for(let bits=0;bits<2**n;bits++){
  const record=Array.from({length:n},(_,i)=>bits&(1<<i)?'H':'T').join('');
  let actual='0';for(const flip of record)actual=sm.step(pattern,actual,flip);
  assert.equal(actual,record.includes(pattern)?'done':record.endsWith('H')?'H':'0',pattern+' suffix for '+record);
 }
 for(const prob of [.1,.25,.5,.8]){
  const v=sm.waits(pattern,prob);
  assert.ok(Math.abs(v.empty-(1+(1-prob)*v.empty+prob*v.head))<1e-10);
  assert.ok(Math.abs(v.head-(1+(pattern==='HH'?(1-prob)*v.empty:prob*v.head)))<1e-10);
 }
 inspect(sm.stateResult(pattern));
}
for(let k=1;k<=8;k++){assert.equal(sm.runMean(k,.5),2**(k+1)-2);assert.equal(sm.runMean(k,1),k);}
const am=registry.get('l06').models;
for(const factor of [97,99,103]){const v=am.compensate(factor);assert.equal(v.anchor+v.delta,factor*37);assert.ok(320+v.position>=40&&320+v.position<=600);inspect(am.result(v));}
for(const [a,b,answer] of [[97,103,9991],[97,104,10088],[98,102,9996],[98,103,10094]])assert.equal(a*b,answer);
assert.equal(240*19/100,45.6);assert.equal(600/6,100);assert.ok(Math.abs(.1667*600-100.02)<1e-12);
const vm7=registry.get('l07').models;
for(const mode of ['same','independent','opposite']){
 const v=vm7.joint(mode);let meanX=0,meanY=0,meanSum=0,secondSum=0;
 for(let x=0;x<=1;x++)for(let y=0;y<=1;y++){const prob=v.weights[2*x+y];meanX+=x*prob;meanY+=y*prob;meanSum+=(x+y)*prob;secondSum+=(x+y)**2*prob;}
 assert.equal(meanX,.5);assert.equal(meanY,.5);assert.equal(meanSum,1);assert.equal(v.variance,secondSum-meanSum**2);
 assert.equal(v.sum.reduce((a,b)=>a+b),1);assert.equal(v.weights.reduce((a,b)=>a+b),1);inspect(vm7.result(v));
}
for(const n of [2,3,10,100]){
 assert.ok(Math.abs(vm7.meanVariance(n,-1/(n-1)))<1e-12);
 assert.equal(vm7.meanVariance(n,0),1/n);assert.equal(vm7.meanVariance(n,1),1);
 const rho=.1,explicit=(n+n*(n-1)*rho)/(n*n);assert.ok(Math.abs(vm7.meanVariance(n,rho)-explicit)<1e-12);
}
assert.equal(vm7.meanVariance(100,.1),.109);
assert.ok(vm7.meanVariance(100,-.1)<0,'Reject impossible model rather than calling negative variance uncertainty');
const tm=registry.get('l08').models;
assert.deepEqual(Array.from(tm.priorMean([2,4,6,8],3)),[null,null,null,4]);
assert.deepEqual(Array.from(tm.priorMean([2,4,6,800],3)),[null,null,null,4]);
assert.deepEqual(Array.from(tm.priorMean([],1)),[]);assert.throws(()=>tm.priorMean([1],0));
const features=[{available:-1,value:5},{available:2,value:7},{available:5,value:9}],decisions=[-2,1,2,3,5];
assert.deepEqual(Array.from(tm.asOf(features,decisions)),[null,5,7,7,9]);
assert.deepEqual(Array.from(tm.asOf(features,decisions,false)),[null,5,5,7,7]);
const renderedCode=registry.python(tm.source);
assert.equal(decode(renderedCode.replace(/^<pre[^>]*><code>/,'').replace(/<\/code><\/pre>$/,'').replace(/<\/?span[^>]*>/g,'')),tm.source,'Highlighting preserves literal source and whitespace');
assert.ok(renderedCode.includes('&lt;'));assert.ok(!renderedCode.includes('window < 1'));
const {spawnSync}=require('node:child_process');
const pythonCheck=spawnSync('python3',['-c',String.raw`
import sys, itertools, math
namespace={}
exec(sys.stdin.read(),namespace)
fn=namespace['prior_mean']
assert fn([],1)==[]
assert fn([2,4,6,8],3)==[None,None,None,4.0]
for n in range(7):
 for seq in itertools.product([-2,0,3],repeat=n):
  for w in range(1,5):
   actual=fn(seq,w)
   expected=[None if i<w else sum(seq[i-w:i])/w for i in range(n)]
   assert actual==expected,(seq,w,actual,expected)
   for i in range(n):
    changed=list(seq);changed[i:]=[1000]*(n-i)
    assert fn(changed,w)[i]==actual[i]
print('Authored Python passed exhaustive small windows and future-invariance checks.')
`],{input:tm.source,encoding:'utf8'});
assert.equal(pythonCheck.status,0,pythonCheck.stderr);console.log(pythonCheck.stdout.trim());
const em=registry.get('l09').models;
for(const prob of [0,.25,.5,.75,1]){
 const v=em.sampling(prob),weights=[0,0,0,0,0];
 for(let bits=0;bits<16;bits++){const successes=Array.from({length:4},(_,i)=>Boolean(bits&(1<<i))).filter(Boolean).length;weights[successes]+=prob**successes*(1-prob)**(4-successes);}
 assert.deepEqual(Array.from(v.weights),weights);
 const rawMean=weights.reduce((sum,w,k)=>sum+w*k/4,0),shrunkMean=weights.reduce((sum,w,k)=>sum+w*(k+1)/6,0);
 const rawMSE=weights.reduce((sum,w,k)=>sum+w*(k/4-prob)**2,0),shrunkMSE=weights.reduce((sum,w,k)=>sum+w*((k+1)/6-prob)**2,0);
 assert.ok(Math.abs(rawMean-v.rawMean)<1e-12);assert.ok(Math.abs(shrunkMean-v.shrunkMean)<1e-12);
 assert.ok(Math.abs(rawMSE-v.rawMSE)<1e-12);assert.ok(Math.abs(shrunkMSE-v.shrunkMSE)<1e-12);inspect(em.result(v));
}
assert.equal(em.sampling(0).rawMSE,0);assert.ok(em.sampling(0).shrunkMSE>0);

const cm=registry.get('l10').models;
const qform=(matrix,w)=>w.reduce((sum,wi,i)=>sum+wi*matrix[i].reduce((inner,r,j)=>inner+r*w[j],0),0);
for(const c of [0,.28,.64,1]){
 const matrix=[[1,.8,c],[.8,1,.8],[c,.8,1]],v=cm.candidate(c);
 assert.ok(Math.abs(qform(matrix,[1,-1.6,1])-v.quadratic)<1e-12);
 const det=1*(1-.8*.8)-.8*(.8-.8*c)+c*(.8*.8-c);
 assert.ok(Math.abs(det-v.determinant)<1e-12);
 assert.equal(v.feasible,Math.abs(c)<=1&&det>=-1e-12);
 inspect(cm.result(v));
}
// Independent Gram construction: Y,U orthogonal, X/Z opposing residuals.
const vectors=[[.8,.6],[1,0],[.8,-.6]];
const gram=vectors.map(a=>vectors.map(b=>a.reduce((sum,x,i)=>sum+x*b[i],0)));
assert.ok(Math.abs(gram[0][2]-.28)<1e-12);
assert.ok(Math.abs(qform(gram,[1,-1.6,1]))<1e-12);
assert.equal(qform([[1,.8,1],[.8,1,.8],[1,.8,1]],[1,0,-1]),0);
const combo=w=>w*w+4*(1-w)**2;
assert.ok(Math.abs(combo(.8)-.8)<1e-12);
for(const w of [-2,0,.4,1,2])assert.ok(combo(w)>=combo(.8));


const rm=registry.get('l11').models;
const fitted=rm.fit([0,1,2],[1,1,4]);
assert.equal(fitted.slope,1.5);assert.equal(fitted.offset,.5);
assert.deepEqual(Array.from(fitted.residuals),[.5,-1,.5]);
assert.equal(fitted.residuals.reduce((a,b)=>a+b),0);
assert.equal(fitted.residuals.reduce((sum,r,i)=>sum+i*r,0),0);
assert.ok(Math.abs(rm.fit([0,1,2],[1,1,4],false).residuals.reduce((a,b)=>a+b)-.6)<1e-12);
for(const dx of [0,3,-7])for(const dy of [0,5,-2]){
 const r=rm.fit([0,1,2].map(x=>x+dx),[1,1,4].map(y=>y+dy));
 assert.ok(Math.abs(r.slope-1.5)<1e-12);assert.ok(Math.abs(r.offset-(.5+dy-1.5*dx))<1e-12);
}
let w2=0,wy=0;
for(const z of [-1,1])for(const u of [-Math.sqrt(3),Math.sqrt(3)]){w2+=(z+u)**2/4;wy+=(z+u)*(2*z-u)/4;}
assert.ok(Math.abs(wy/w2+.25)<1e-12,'Feasible correlated feature/response noise reverses the slope');

const inf=registry.get('l12').models;
for(let k=0;k<=10;k++){
 let extreme=0;for(let bits=0;bits<1024;bits++)if(bits.toString(2).replace(/0/g,'').length>=k)extreme++;
 assert.equal(inf.tail(k),extreme/1024);
}
assert.equal(inf.tail(8),56/1024);assert.equal(inf.tail(9),11/1024);
for(let percent=0;percent<=100;percent+=10){
 const v=inf.mixture(percent);assert.ok(Math.abs(v.treatment-v.control-.1)<1e-12);
 assert.ok(Math.abs(v.treatment-(.9*percent+.2*(100-percent))/100)<1e-12);inspect(inf.result(v));
}
assert.ok(29/110<81/110);assert.ok(.9>.8&&.2>.1);

const series=registry.get('l13').models;
for(const n of [1,2,3,5,10,100])for(const rho of [-.8,0,.8]){
 let variance=0;for(let i=0;i<n;i++)for(let j=0;j<n;j++)variance+=rho**Math.abs(i-j);
 assert.ok(Math.abs(series.factor(n,rho)-variance/n)<1e-10);
 assert.ok(series.factor(n,rho)>0);
}
assert.equal(series.factor(1,.8),1);assert.equal(series.factor(100,0),1);
assert.ok(Math.abs(series.factor(100,.8)-8.6)<1e-7);
assert.ok(series.summary(100).effective>series.summary(100).asymptotic);
assert.ok(series.factor(100,-.8)<1);
for(const n of [1,2,10,100])inspect(series.result(series.summary(n)));

const val=registry.get('l14').models;
for(let a=0;a<6;a++)for(let b=a+1;b<=7;b++)for(let u=0;u<6;u++)for(let v=u+1;v<=7;v++){
 // Half-integer probes independently enumerate intersection of integer endpoints.
 const intersects=Array.from({length:14},(_,i)=>i/2+.25).some(time=>time>=a&&time<b&&time>=u&&time<v);
 assert.equal(val.overlap([a,b],[u,v]),intersects);
}
assert.equal(val.overlap([95,100],[100,105]),false);
assert.equal(val.overlap([98,103],[100,105]),true);
assert.equal(val.overlap([105,110],[100,105]),false);
for(const [start,horizon,cutoff,want] of [[94,5,100,true],[95,5,100,true],[98,5,100,false],[105,5,100,false]])assert.equal(val.eligible(start,horizon,cutoff),want);

const search=registry.get('l15').models;
const risk=registry.get('l22').models;
assert.equal(risk.variance(.5,.5,2,2,.5),3);assert.equal(risk.variance(.5,.5,2,2,1),4);assert.equal(risk.variance(.5,.5,3,3,1),9);assert.equal(risk.variance(.5,.5,2,2,-1),0);
for(const rho of [-1,-.5,0,.5,1])for(const w of [-1,0,.5,1,2]){
 // Independent factor construction with centred, uncorrelated unit factors.
 const load1=w*2+(1-w)*2*rho,load2=(1-w)*2*Math.sqrt(1-rho*rho);
 assert.ok(Math.abs(risk.variance(w,1-w,2,2,rho)-(load1*load1+load2*load2))<1e-12);
}
for(const dist of [[[-1,.5],[1,.5]],[[-3,.1],[1/3,.9]]]){
 const mean=dist.reduce((s,[x,p])=>s+x*p,0),second=dist.reduce((s,[x,p])=>s+x*x*p,0);
 assert.ok(Math.abs(mean)<1e-12);assert.ok(Math.abs(second-1)<1e-12);
}
const finance=registry.get('l23').models;
for(const strike of [0,50,100,150])for(let spot=0;spot<=200;spot++)assert.equal(finance.call(spot,strike)-finance.put(spot,strike),spot-strike);
assert.equal(finance.change(5,1),2.8);assert.equal(finance.change(-5,1),-1.2);
assert.equal(finance.change(5,0,0),1);assert.equal(finance.change(-5,0,0),1);
for(const s of [-8,-5,0,5,8])assert.ok(Math.abs(finance.change(s)-.4*s-.04*s*s)<1e-12);
const strategy=registry.get('l24').models;
assert.ok(Math.abs(strategy.posteriorHigh(.5,.8,.2)-.2)<1e-12);
for(let i=0;i<=100;i++)for(let j=0;j<=100;j++){
 const p=i/100,q=j/100;assert.ok(Math.abs(strategy.expectedBrier(p,q)-((p-q)**2+q*(1-q)))<1e-12);
 assert.ok(strategy.expectedBrier(q,q)<=strategy.expectedBrier(p,q)+1e-12);
}
assert.ok(Math.abs((.2-.2*.2+.8-.8*.8)/2-.16)<1e-12);
assert.ok(Math.abs((7*.09+3*.49)/10-.21)<1e-12);
// A monotone winning likelihood must tilt a signal-only posterior downward.
for(const weights of [[.5,.5],[.2,.8],[.9,.1]]){
 const priorMean=100*weights[1],winnerMean=100*weights[1]*.2/(weights[0]*.8+weights[1]*.2);
 assert.ok(winnerMean<=priorMean);
}
const fv=registry.get('l19').models;
for(const first of [null,1,6]){
 const d=fv.distribution(first);let sum=0,total=0;
 for(let b=1;b<=6;b++)for(let c=1;c<=6;c++)for(const a of first===null?[1,2,3,4,5,6]:[first]){total++;sum+=a+b+c;}
 assert.equal(d.total,total);assert.equal(d.mean,sum/total);assert.equal(d.counts.reduce((a,b)=>a+b),total);inspect(fv.valueResult(d));
}
assert.equal(fv.distribution().counts[10],27);
const flow=registry.get('l20').models;
for(const alpha of [0,.25,.5,.75,1])for(const ask of [55,60,70]){
 const f=flow.flow(alpha,ask),states=[[.5*alpha,100,true],[.5*(1-alpha),100,true],[.5*alpha,0,false],[.5*(1-alpha),0,true]];
 const fill=states.reduce((s,[p,v,buy])=>s+(buy?p:0),0),pnl=states.reduce((s,[p,v,buy])=>s+(buy?p*(ask-v):0),0);
 assert.equal(f.fill,fill);assert.ok(Math.abs(f.perOpportunity-pnl)<1e-12);assert.ok(Math.abs(f.perFill-pnl/fill)<1e-12);
}
const decision=registry.get('l21').models;
assert.equal(decision.continuation(3.5),4.25);assert.equal(decision.continuation(4.25),14/3);assert.equal(decision.continuation(3.5,1),23/6);
for(const prob of [.4,.5,.52,.6,.9]){
 const optimum=Math.max(0,2*prob-1);
 for(let i=0;i<100;i++)assert.ok(decision.growth(optimum,prob)>=decision.growth(i/100,prob)-1e-12);
}
assert.ok(Math.abs(decision.growth(.2,.52)+.012302)<1e-5);assert.ok(decision.growth(.5,.6)<0);
assert.ok(Math.abs(search.posterior(1)-9/58)<1e-12);assert.ok(Math.abs(search.posterior(2)-81/130)<1e-12);
for(const count of [1,2,20,100]){
 assert.ok(search.family(count)>=.05-1e-12&&search.family(count)<=Math.min(1,count*.05)+1e-12);
}
let rejected=0;
for(let a=0;a<20;a++)for(let b=0;b<20;b++)if(a===0||b===0)rejected++;
assert.ok(Math.abs(search.family(2)-rejected/400)<1e-12);
assert.ok(Math.abs(search.family(20)-.6415140775914581)<1e-12);
// Independent numerical integration of the two Gaussian-score maximum.
const dx=.001;let maxMoment=0;
for(let x=-8;x<=8;x+=dx){
 const phi=Math.exp(-x*x/2)/Math.sqrt(2*Math.PI);
 const erf=(()=>{const sign=x<0?-1:1,z=Math.abs(x)/Math.sqrt(2),t=1/(1+.3275911*z);return sign*(1-(((((1.061405429*t-1.453152027)*t)+1.421413741)*t-.284496736)*t+.254829592)*t*Math.exp(-z*z));})();
 maxMoment+=x*2*phi*(.5+.5*erf)*dx;
}
assert.ok(Math.abs(maxMoment-1/Math.sqrt(Math.PI))<1e-6);

const defence=registry.get('l16').models;
assert.ok(Math.abs(defence.pnl(100.08,100.10,.01,.01))<1e-12);
assert.ok(Math.abs(defence.pnl(100.05,100.10,.01,.01)-.03)<1e-12);
assert.ok(defence.pnl(100.08,100.06,0,0)<0);
assert.ok(Math.abs(defence.pnl(100.08,100.10,.01,.01)-defence.pnl(200.08,200.10,.01,.01))<1e-12);
const mc=registry.get('l17').models;
for(let k=0;k<=100;k++){const u=k/100;assert.ok(Math.abs(mc.pair(u)-(u*u-u+.5))<1e-12);assert.ok(mc.pair(u)>=.25&&mc.pair(u)<=.5);}
const integrate=coeff=>coeff.reduce((sum,c,i)=>sum+c/(i+1),0);
const pairMean=integrate([.5,-1,1]),pairSecond=integrate([.25,-1,2,-2,1]);
assert.ok(Math.abs(pairMean-1/3)<1e-12);assert.ok(Math.abs(pairSecond-pairMean**2-1/180)<1e-12);
assert.ok(Math.abs((2/45)/(1/180)-8)<1e-12);
assert.ok(Math.abs(integrate([0,0,1,-2,1])-1/30)<1e-12);
const mcCode=registry.python(mc.source);
assert.equal(decode(mcCode.replace(/^<pre[^>]*><code>/,'').replace(/<\/code><\/pre>$/,'').replace(/<\/?span[^>]*>/g,'')),mc.source);
const mcPython=spawnSync('python3',['-c',String.raw`
import sys, math, random
ns={}
exec(sys.stdin.read(),ns)
fn=ns['estimate']
for n in [0,1]:
 try: fn(n)
 except ValueError: pass
 else: raise AssertionError(n)
for n in [2,10,1000]:
 for seed in [0,7,23]:
  value,se=fn(n,seed)
  rng=random.Random(seed)
  units=[(u*u-u+.5) for u in [rng.random() for _ in range(n)]]
  mean=sum(units)/n
  expected=math.sqrt(sum((a-mean)**2 for a in units)/(n*(n-1)))
  assert abs(value-mean)<1e-12 and abs(se-expected)<1e-12
  assert .25<=value<=.5 and se>=0
assert fn(1000,7)==fn(1000,7)
print('Authored Monte Carlo Python matched independent-unit error calculation.')
`],{input:mc.source,encoding:'utf8'});
assert.equal(mcPython.status,0,mcPython.stderr);console.log(mcPython.stdout.trim());
// Execute each actual binding and verify final text/model state without credits.
function el(){return {style:{},attrs:{},innerHTML:'',textContent:'',classList:{toggle(){}},addEventListener(k,fn){this[k]=fn;},setAttribute(k,v){this.attrs[k]=v;}};}
const baseline=run('JSON.stringify(state)');
const nodes=new Map();const root={querySelector:s=>{if(!nodes.has(s))nodes.set(s,el());return nodes.get(s);}};
registry.get('l02').bind(root,()=>{});root.querySelector('#bayes-heads').change({target:{value:'2'}});assert.ok(root.querySelector('#bayes-result').innerHTML.includes('0.8'));
root.querySelector('#bayes-prior').input({target:{value:'10'}});assert.ok(root.querySelector('#bayes-result').innerHTML.includes('0.3077'));
const flips=Array.from({length:6},el),rows=Array.from({length:5},()=>{const r=el();r.label=el();r.value=el();r.querySelector=s=>s==='strong'?r.label:r.value;return r;});
root.querySelectorAll=s=>s.includes('flips')?flips:rows;
registry.get('l03').bind(root,()=>{});root.querySelector('#indicator-record').change({target:{value:'TTTTTT'}});assert.ok(root.querySelector('#indicator-result').innerHTML.includes('C=0+0+0+0+0=0'));assert.ok(flips.every(x=>x.textContent==='T'));
registry.get('l04').bind(root,()=>{});root.querySelector('#wait-age').input({target:{value:'9'}});assert.equal(root.querySelector('#wait-uniform-label').textContent,'0.5 min');assert.equal(root.querySelector('#wait-uniform-bar').style.width,'10%');
const final=root.querySelector('#wait-result').innerHTML;root.querySelector('#wait-age').input({target:{value:'10'}});assert.equal(root.querySelector('#wait-result').innerHTML,final,'Reject zero-probability conditioning boundary');
const buttons=['HH','HT'].map(pattern=>{const b=el();b.dataset={targetPattern:pattern};return b;});
root.querySelectorAll=()=>buttons;registry.get('l05').bind(root,()=>{});
const suffixReset=root.querySelector('#suffix-reset'),suffixRetain=root.querySelector('#suffix-retain');
for(const pattern of ['HT','HH','HT','HH','HT']){
 buttons[pattern==='HH'?0:1].click();
 assert.equal(root.querySelector('#suffix-done-label').textContent,pattern);
 assert.ok(root.querySelector('#suffix-result').innerHTML.includes('E_0='+(pattern==='HH'?6:4)));
 assert.equal(suffixReset.style.opacity,pattern==='HH'?'1':'0');
 assert.equal(suffixRetain.style.opacity,pattern==='HT'?'1':'0');
 assert.equal(buttons[pattern==='HH'?0:1].attrs['aria-pressed'],'true');
 assert.equal(root.querySelector('#suffix-reset'),suffixReset,'Preserve stable transition nodes');
}
const selectedResult=root.querySelector('#suffix-result').innerHTML;buttons[1].click();assert.equal(root.querySelector('#suffix-result').innerHTML,selectedResult);
const factorButtons=[97,99,103].map(factor=>{const b=el();b.dataset={factor:String(factor)};return b;});
root.querySelectorAll=()=>factorButtons;registry.get('l06').bind(root,()=>{});
const productNode=root.querySelector('#anchor-product');
for(const factor of [103,97,99,103]){
 factorButtons[[97,99,103].indexOf(factor)].click();
 assert.equal(root.querySelector('#anchor-product-label').textContent,String(factor*37));
 assert.equal(productNode.style.transform,`translateX(${am.compensate(factor).position}px)`);
 assert.equal(root.querySelector('#anchor-product'),productNode);
 assert.ok(root.querySelector('#anchor-desc').textContent.includes(String(factor*37)));
}
const couplingButtons=['same','independent','opposite'].map(mode=>{const b=el();b.dataset={coupling:mode};return b;});
const jointCells=Array.from({length:4},el),sumBars=Array.from({length:3},el),sumLabels=Array.from({length:3},el);
root.querySelectorAll=s=>s==='[data-coupling]'?couplingButtons:s==='[data-joint-cell]'?jointCells:s==='[data-sum-bar]'?sumBars:sumLabels;
registry.get('l07').bind(root,()=>{});
for(const mode of ['same','opposite','independent','same','opposite']){
 couplingButtons[['same','independent','opposite'].indexOf(mode)].click();
 const v=vm7.joint(mode);assert.deepEqual(jointCells.map(c=>c.textContent),Array.from(v.weights,p=>100*p+'%'));
 assert.deepEqual(sumBars.map(b=>b.style.width),Array.from(v.sum,p=>100*p+'%'));
 assert.ok(root.querySelector('#coupling-result').innerHTML.includes('='+v.variance+'.'));
}
const samplingStems=['raw','shrunk'].flatMap(kind=>Array.from({length:5},(_,i)=>{const node=el();node.dataset={samplingStem:kind+'-'+i};return node;}));
root.querySelectorAll=()=>samplingStems;registry.get('l09').bind(root,()=>{});
for(const prob of [0,1,.5,.25]){
 root.querySelector('#sampling-prob').change({target:{value:String(prob)}});
 assert.equal(root.querySelector('#sampling-truth').attrs.d,`M${50+540*prob} 50V400`);
 assert.ok(samplingStems.every((node,i)=>node.style.transform===`scaleY(${em.sampling(prob).weights[i%5]})`));
 assert.ok(root.querySelector('#sampling-desc').textContent.includes('True probability '+prob));
}
registry.get('l10').bind(root,()=>{});
for(const c of [0,.28,1,.64,0]){
 root.querySelector('#covariance-c').change({target:{value:String(c)}});
 assert.equal(root.querySelector('#covariance-result').innerHTML,cm.result(cm.candidate(c)));
}
registry.get('l12').bind(root,()=>{});
for(const percent of [0,100,50,30]){
 root.querySelector('#mixture-weight').input({target:{value:String(percent)}});
 assert.equal(root.querySelector('#mixture-treatment').style.width,(100*inf.mixture(percent).treatment).toFixed(0)+'%');
 assert.equal(root.querySelector('#mixture-result').innerHTML,inf.result(inf.mixture(percent)));
}
registry.get('l13').bind(root,()=>{});
const seriesPoint=root.querySelector('#series-point');
for(const n of [1,100,10,2,100]){
 root.querySelector('#series-n').input({target:{value:String(n)}});
 assert.equal(root.querySelector('#series-point'),seriesPoint);
 assert.equal(root.querySelector('#series-selected').attrs.d,'M'+series.px(n)+' 50V330');
 assert.equal(root.querySelector('#series-result').innerHTML,series.result(series.summary(n)));
}

// The marker must travel along the piecewise covariance curve, not its chord.
const motionPoint=el(),motions=[];
motionPoint.animate=(frames,options)=>{const anim={frames,options,cancelled:false,cancel(){this.cancelled=true;},effect:{getComputedTiming:()=>({progress:.5})}};motions.push(anim);return anim;};
const motionNodes=new Map([['#series-point',motionPoint]]);
const motionRoot={querySelector:s=>{if(!motionNodes.has(s))motionNodes.set(s,el());return motionNodes.get(s);}};
registry.get('l13').bind(motionRoot,()=>{});
motionRoot.querySelector('#series-n').input({target:{value:'1'}});
assert.equal(motions.length,1);
for(const frame of motions[0].frames){
 const values=frame.transform.match(/translate\(([-\d.]+)px,([-\d.]+)px\)/);
 const n=1+(Number(values[1])+540)*99/540,lo=Math.floor(n+1e-10),hi=Math.ceil(n-1e-10);
 const f=series.factor(lo,.8)+(n-lo)*(series.factor(hi,.8)-series.factor(lo,.8));
 assert.ok(Math.abs(Number(values[2])-(series.py(f)-series.py(series.factor(100,.8))))<1e-8);
}
motionRoot.querySelector('#series-n').input({target:{value:'100'}});
assert.equal(motions[0].cancelled,true);assert.ok(motions[1].frames.length>2);
context.matchMedia=()=>({matches:true});
motionRoot.querySelector('#series-n').input({target:{value:'2'}});
assert.equal(motions[1].cancelled,true);assert.equal(motions.length,2);
assert.ok(motionPoint.style.transform.includes(String(series.px(2)-600)));
delete context.matchMedia;
assert.equal(run('JSON.stringify(state)'),baseline);
const valueBars=Array.from({length:16},(_,i)=>{const node=el();node.dataset={valueBar:String(i+3)};return node;});
root.querySelectorAll=()=>valueBars;registry.get('l19').bind(root,()=>{});
for(const value of ['6','1','prior','6']){
 root.querySelector('#value-information').value=value;root.querySelector('#value-information').change();const d=fv.distribution(value==='prior'?null:Number(value));
 assert.equal(root.querySelector('#value-result').innerHTML,fv.valueResult(d));
 valueBars.forEach((bar,i)=>assert.ok(Math.abs(bar.attrs.height-1000*d.counts[i+3]/d.total)<1e-12));
 assert.equal(root.querySelector('#value-mean').attrs.d,`M${60+29*(d.mean-3)} 60V290`);
}
assert.equal(run('JSON.stringify(state)'),baseline);
assert.ok(spans>150);
console.log('Twenty-seven authored courses: preserved l01 reference, outline/quiz continuity, '+spans+' strict math spans, exhaustive indicator/suffix states, first-step means, Bayes odds and ungraded bindings passed.');
