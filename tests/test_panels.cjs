'use strict';
// Compact menu recovery must not collapse an offscreen menu or lose reading position.
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const handlers={},frames=[],layoutWrites=[];let compact=true;
const nodes={},context={URLSearchParams,location:{hash:'#courses/l01',search:'?qa=1'},console,Date,Math,setTimeout,clearTimeout,
 localStorage:{getItem:()=>null,setItem:(k,v)=>layoutWrites.push(k)},requestAnimationFrame:fn=>frames.push(fn),
 document:{querySelector:s=>nodes[s],querySelectorAll:()=>[nodes.button]},
 window:{scrollY:800,matchMedia:()=>({matches:compact}),scrollTo(x,y){this.scrollY=y;}}};
vm.createContext(require('./workspace-fixture.cjs')(context));vm.runInContext(fs.readFileSync('static/app.js','utf8').replace(/init\(\);\s*$/,''),context);
const run=s=>vm.runInContext(s,context),drain=()=>{while(frames.length)frames.shift()();};
nodes.button={dataset:{panel:'navigation'},addEventListener:(event,fn)=>handlers[event]=fn};
nodes['#navigation-panel']={getBoundingClientRect:()=>({bottom:140-context.window.scrollY}),scrollIntoView(){context.window.scrollY=0;}};
run('syncPanels=()=>{};keepNavigationVisible=()=>{};');run('bindPanels()');
const baseline=run('JSON.stringify(state)');
// Reveal the already-open menu that has scrolled above the viewport.
handlers.click();assert.equal(run('panels.navigation'),true);assert.equal(context.window.scrollY,0);assert.equal(layoutWrites.length,0);
// Now it is visible: closing must work and restore the exact reading point.
handlers.click();drain();assert.equal(run('panels.navigation'),false);assert.equal(context.window.scrollY,800);
// A closed menu opens with one click and closes back to the same point.
context.window.scrollY=950;handlers.click();assert.equal(run('panels.navigation'),true);assert.equal(context.window.scrollY,0);handlers.click();drain();assert.equal(context.window.scrollY,950);
// A route change cancels a queued return, rather than scrolling a different activity.
context.window.scrollY=730;handlers.click();handlers.click();context.location.hash='#questions/q01';context.window.scrollY=0;drain();assert.equal(context.window.scrollY,0);
// Desktop controls retain their column-toggle contract and never jump the page.
compact=false;context.window.scrollY=500;handlers.click();drain();assert.equal(context.window.scrollY,500);
assert.equal(run('JSON.stringify(state)'),baseline);assert.ok(layoutWrites.every(k=>k==='quant-atelier-qa-layout'));
console.log('Compact offscreen reveal, visible-menu collapse, reading recovery, route-change cancellation, desktop behavior and isolated layout preferences passed.');
