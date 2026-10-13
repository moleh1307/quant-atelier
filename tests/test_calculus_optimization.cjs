'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const ctx={console,Math,Date};vm.createContext(ctx);for(const file of ['course-textbook.js','lesson-calculus.js','lesson-optimization.js'])vm.runInContext(fs.readFileSync('static/'+file,'utf8'),ctx);
const calc=ctx.QuantCourseLessons.get('l26').models,opt=ctx.QuantCourseLessons.get('l27').models;
for(let theta=-.5;theta<=4;theta+=.1)for(let h=.1;h<=2;h+=.1){const v=calc.local(theta,h);assert.ok(Math.abs(v.change-v.predicted-v.remainder)<1e-12);assert.ok(Math.abs(v.secant-v.change/h)<1e-12);}
for(let a=0;a<=360;a++){const v=calc.direction(a);assert.ok(Math.abs(v.x*v.x+v.y*v.y-1)<1e-12);assert.ok(v.slope>=-Math.sqrt(10)-1e-12);assert.ok(v.curvature>=3-Math.sqrt(2)-1e-12);}
for(const a of [.02,.111,.2,2/9,.25])for(const v of opt.trajectory(a)){assert.ok(Math.abs(v.x-2*(1-a)**v.k)<1e-12);assert.ok(Math.abs(v.y-(1-9*a)**v.k)<1e-12);assert.ok(Math.abs(v.loss-(v.x*v.x+9*v.y*v.y)/2)<1e-12);assert.ok(Math.abs(v.x)<4.5&&Math.abs(v.y)<4.5,'All displayed paths fit the fixed axes');}
assert.equal(opt.trajectory(2/9)[6].y,1);assert.ok(opt.trajectory(.25)[6].loss>opt.trajectory(.25)[0].loss);
for(let cap=.2;cap<=1;cap+=.01){const v=opt.box(cap);assert.ok(Math.abs(v.gap-(1-cap)**2/2)<1e-12);assert.ok(v.gradient[1]<=0);}
for(const z of [-1000,-10,0,10,1000])for(const y of [0,1])assert.ok(Number.isFinite(calc.binaryLoss(z,y)));
// Actual animation helper: retarget from what is on screen, stop after a
// detached route, honor reduced motion and handle hosts without RAF.
let next=1,queue=new Map(),drawn=[],cancelled=[];ctx.requestAnimationFrame=fn=>{const id=next++;queue.set(id,fn);return id;};ctx.cancelAnimationFrame=id=>{cancelled.push(id);queue.delete(id);};ctx.matchMedia=()=>({matches:false});const root={isConnected:true};const move=calc.motion([0],v=>drawn.push(v[0]),root);
function tick(time){const jobs=[...queue.values()];queue.clear();for(const fn of jobs)fn(time);}
move([10]);tick(0);tick(170);assert.equal(drawn.at(-1),5);move([20]);tick(200);assert.equal(drawn.at(-1),5);tick(370);assert.equal(drawn.at(-1),12.5);tick(540);assert.equal(drawn.at(-1),20);assert.ok(cancelled.length);
move([0]);root.isConnected=false;const size=drawn.length;tick(600);assert.equal(drawn.length,size);assert.equal(queue.size,0);
root.isConnected=true;ctx.matchMedia=()=>({matches:true});move([7]);assert.equal(drawn.at(-1),7);assert.equal(queue.size,0);
delete ctx.requestAnimationFrame;ctx.matchMedia=()=>({matches:false});move([9]);assert.equal(drawn.at(-1),9);
console.log('Differential geometry, exact iteration stability, box certificates and retargeted/reduced/detached/no-RAF animation passed.');
