'use strict';
// Exercise navigation recovery and feedback focus without changing study records.
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const source=fs.readFileSync('static/app.js','utf8').replace(/init\(\);\s*$/,'');
const stored={},frames=[];let elements={},radios=[],selects=[],steps=[],links=[],focused=null;
const page={contains:el=>!!el?.inPage};
const node=(id,extra={})=>({id,inPage:true,closest:()=>null,matches:()=>false,
 focus(){focused=this.id;document.activeElement=this;},setSelectionRange(a,b){this.selectionStart=a;this.selectionEnd=b;},...extra});
const document={activeElement:null,querySelector:s=>s==='#page'?page:s==='#page h1'?elements.heading:elements[s.slice(1)]||null,
 getElementById:id=>elements[id]||null,querySelectorAll:s=>s==='.roadmap-step'?steps:s.includes('radio')?radios.filter(r=>!s.endsWith(':checked')||r.checked):s.includes('select')?selects:s==='#page a[href]'?links:[],addEventListener(){}};
const context={URLSearchParams,location:{hash:'#questions',search:'?qa=1'},document,
 localStorage:{getItem:()=>null},sessionStorage:{getItem:k=>stored[k]||null,setItem:(k,v)=>stored[k]=v},
 window:{scrollY:420,scrollTo(x,y){this.scrollY=y;}},requestAnimationFrame:fn=>frames.push(fn),console,Date,Math,setTimeout,clearTimeout};
vm.createContext(require('./workspace-fixture.cjs')(context));vm.runInContext(source,context);
const run=js=>vm.runInContext(js,context),drain=()=>{while(frames.length)frames.shift()();};
run("render=()=>{route=(location.hash.slice(1)||'dashboard').split('/');renderedHash=location.hash||'#dashboard';renderEpoch++;};");
const baseline=run('JSON.stringify(state)');
elements.search=node('search',{selectionStart:2,selectionEnd:2});document.activeElement=elements.search;
run("renderedHash='#questions';filters={...emptyFilters(),search:'dice',difficulty:'Hard'};");
context.location.hash='#questions/q02';run('navigatePage()');drain();
assert.equal(context.window.scrollY,0);assert.equal(run('filters.search'),'');
context.window.scrollY=260;context.location.hash='#questions';run('navigatePage()');drain();
assert.equal(run('filters.search'),'dice');assert.equal(run('filters.difficulty'),'Hard');assert.equal(context.window.scrollY,420);assert.equal(focused,'search');
// Session cache restores a deep reading position after reload.
run("renderedHash='#courses/l01';filters=emptyFilters();");context.window.scrollY=1800;run('captureNavigation()');
context.location.hash='#courses/l01';context.window.scrollY=0;run("navigation=JSON.parse(sessionStorage.getItem(NAV_KEY));render();restoreNavigation();");drain();assert.equal(context.window.scrollY,1800);
// Roadmap stops preserve both open and deliberately closed states.
steps=[node('step-l01',{open:false,matches:s=>s==='.roadmap-step'}),node('step-l02',{open:true,matches:s=>s==='.roadmap-step'})];steps.forEach(s=>elements[s.id]=s);
run("renderedHash='#paths';route=['paths'];");context.window.scrollY=640;run('captureNavigation()');steps[0].open=true;steps[1].open=false;
context.location.hash='#paths';run('render();restoreNavigation()');drain();assert.equal(steps[0].open,false);assert.equal(steps[1].open,true);
// A later navigation cancels a queued restore from an earlier destination.
context.location.hash='#questions';run('render();restoreNavigation()');context.location.hash='#coding';run('render();restoreNavigation()');drain();assert.equal(context.window.scrollY,0);
// Feedback rerenders retain answer caret, radio choice and revision interval.
elements.answer=node('answer',{selectionStart:1,selectionEnd:3});document.activeElement=elements.answer;
radios=[node('',{name:'option',value:'2',checked:true})];selects=[node('confidence',{value:'7'})];elements.confidence=selects[0];context.window.scrollY=510;
run('var ui=capturePageUI();');elements.answer=node('answer',{selectionStart:0,selectionEnd:0});radios[0].checked=false;selects[0].value='3';context.window.scrollY=0;
run('restorePageUI(ui,renderEpoch)');drain();assert.equal(radios[0].checked,true);assert.equal(selects[0].value,'7');assert.equal(focused,'answer');assert.equal(elements.answer.selectionStart,1);assert.equal(elements.answer.selectionEnd,3);assert.equal(context.window.scrollY,510);
// Duplicate destinations must restore the exact footer link, not a sticky-bar twin.
links=[node('stage-link',{getAttribute:()=> '#questions/q01'}),node('footer-link',{getAttribute:()=> '#questions/q01'})];
context.departure=links[1];run('restoreFocus(linkFocus(departure))');assert.equal(focused,'footer-link');
assert.equal(run('JSON.stringify(state)'),baseline,'Navigation and feedback restoration earn no credit or draft mutations');
assert.ok(stored['quant-atelier-qa-navigation']);assert.equal(stored['quant-atelier-v1-navigation'],undefined);
console.log('Back/filter/scroll recovery, reload, open and closed roadmap stops, rapid navigation, answer caret, quiz choice, select retention and QA isolation passed.');
