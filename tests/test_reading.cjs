'use strict';
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const source=fs.readFileSync('static/app.js','utf8').replace(/init\(\);\s*$/,'');
const frames=[],listeners={},events={};let offset=50,reduced=false,focused='',removed=0;
const sections=Array.from({length:9},(_,i)=>({id:i<7?'lesson-section-'+i:i===7?'lesson-example':'lesson-check',top:500+i*400,focus(){focused=this.id;},getBoundingClientRect(){return {top:this.top-context.window.scrollY};}}));
const buttons=sections.map((s,i)=>({dataset:{section:s.id},attrs:{},offsetTop:30+i*44,offsetHeight:44,title:{textContent:'Section '+i},setAttribute(k,v){this.attrs[k]=v;},removeAttribute(k){delete this.attrs[k];},querySelector(){return this.title;}}));
const summary={title:'',focus(){focused='summary';}},label={},menu={clientHeight:300,scrollTop:0,querySelector(){return buttons.find(b=>b.attrs['aria-current']);}};
const outline={open:false,contains:el=>buttons.includes(el)||el===summary,querySelectorAll:()=>buttons,querySelector:s=>s==='summary'?summary:s==='.lesson-outline-label'?label:menu,addEventListener:(k,f)=>events[k]=f};
const page={addEventListener:(k,f)=>events.outside=f,removeEventListener(){removed++;}},trail={getBoundingClientRect:()=>({height:100})};
const context={console,Date,Math,URLSearchParams,location:{hash:'#courses/l01',search:'?qa=1'},localStorage:{getItem:()=>null},sessionStorage:{getItem:()=>null},setTimeout,clearTimeout,requestAnimationFrame:fn=>frames.push(fn),
 document:{querySelector:s=>s==='#lesson-outline'?outline:s==='.module-trail'?trail:s==='#page'?page:null,getElementById:id=>sections.find(s=>s.id===id),addEventListener(){}},
 window:{scrollY:0,getComputedStyle:()=>({top:String(offset)+'px'}),matchMedia:()=>({matches:reduced}),addEventListener(k,f){listeners[k]=f;},removeEventListener(k){delete listeners[k];},scrollTo(options){this.last=options;this.scrollY=options.top;}}};
vm.createContext(require('./workspace-fixture.cjs')(context));vm.runInContext(source,context);const run=s=>vm.runInContext(s,context),drain=()=>{while(frames.length)frames.shift()();};
const baseline=run('JSON.stringify(state)');run('bindReadingOutline()');drain();assert.equal(buttons[0].attrs['aria-current'],'location');
// Section jumps subtract measured sticky height and preserve route and scores.
events.click({target:{closest:()=>buttons[3]}});assert.equal(focused,'lesson-section-3');assert.equal(context.window.last.top,1700-168);assert.equal(context.window.last.behavior,'smooth');assert.equal(outline.open,false);
listeners.scroll();drain();assert.equal(buttons[3].attrs['aria-current'],'location');assert.match(summary.title,/Section 3/);
// Current location tracks actual scroll, without labelling any section completed.
context.window.scrollY=sections[6].top-168;listeners.scroll();listeners.scroll();assert.equal(frames.length,1);drain();assert.equal(buttons[6].attrs['aria-current'],'location');assert.equal(buttons[3].attrs['aria-current'],undefined);
reduced=true;offset=76;events.click({target:{closest:()=>buttons[8]}});assert.equal(focused,'lesson-check');assert.equal(context.window.last.top,3700-194);assert.equal(context.window.last.behavior,'auto');
outline.open=true;events.toggle();assert.ok(menu.scrollTop>0);events.keydown({key:'Escape',stopPropagation(){}});assert.equal(outline.open,false);assert.equal(focused,'summary');
outline.open=true;events.outside({target:{}});assert.equal(outline.open,false);
listeners.scroll();run('releaseReadingOutline()');drain();assert.equal(Object.keys(listeners).length,0);assert.equal(removed,1);assert.equal(run('JSON.stringify(state)'),baseline);
// Every authored lesson has exactly one target for each section menu destination.
context.bank=JSON.parse(fs.readFileSync('static/content.json','utf8'));run("content=bank;coding=[];route=['courses','l01'];lessonNavigation=()=>'';");
for(const l of context.bank.lessons){context.lesson=l;const html=run('lessonDetail(lesson)'),nav=run('lessonOutline(lesson)');for(const s of run('lessonSections(lesson)')){assert.equal(html.split('id="'+s.id+'"').length-1,1,l.id+' target '+s.id);assert.ok(nav.includes('data-section="'+s.id+'"'));}assert.equal(run('lessonSections(lesson).length'),l.sections.length+2);}
console.log('All lesson section targets, measured sticky offsets, active location, keyboard dismissal, reduced motion, listener cleanup and unchanged study records passed.');
