'use strict';
// Personal continuation is driven by verified records, not page visits or checks alone.
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const bank=JSON.parse(fs.readFileSync('static/content.json','utf8')),codes=JSON.parse(fs.readFileSync('static/coding.json','utf8'));
const els={},handlers={};const context={URLSearchParams,location:{search:'?qa=1',hash:'#dashboard'},console,Math,Date,setTimeout,clearTimeout,
 document:{querySelector:s=>els[s]||null,querySelectorAll:()=>[],activeElement:null},window:{},localStorage:{getItem:()=>null}};
vm.createContext(require('./workspace-fixture.cjs')(context));vm.runInContext(fs.readFileSync('static/app.js','utf8').replace(/init\(\);\s*$/,''),context);context.bank=bank;context.codes=codes;
const run=js=>vm.runInContext(js,context);run("content=bank;coding=codes;state=fresh();route=['dashboard'];");
assert.equal(run('nextRouteActivity().activity.id'),'l01');
run("state.lessons.l01={passed:true};state.questions.q01={reviewed:true};");
assert.equal(run('nextRouteActivity().activity.id'),'q01','A review does not retire a problem');
assert.match(run('dashboard()'),/href="#questions\/q01\/journey\/researcher\/l01"/);
assert.match(run('dashboard()'),/Next unchecked lesson: Condition, then normalise/);
run("state.questions.q01={solved:true};state.questions.q05={selfSolved:true};");assert.equal(run('nextRouteActivity().activity.id'),'c01');
run("state.coding.c01={accepted:true,acceptedAssisted:true};");assert.equal(run('nextRouteActivity().activity.id'),'l02','Passing with an editorial retains its provenance but completes code work');
// All checks passed is distinct from finishing their linked practice.
run("journeyLessons().forEach(l=>state.lessons[l.id]={passed:true});");assert.equal(run('nextRouteActivity().activity.id'),'q02');assert.doesNotMatch(run('dashboard()'),/Your core route is complete/);
for(const path of ['researcher','trader']){
 context.path=path;run("state=fresh();state.preferences.path=path;journeyLessons().filter(l=>l.path==='shared').forEach(l=>{state.lessons[l.id]={passed:true};l.questions.forEach(id=>state.questions[id]={solved:true});l.coding.forEach(id=>state.coding[id]={accepted:true});});");
 assert.equal(run('nextRouteActivity().lesson.path'),path);assert.match(run('dashboard()'),new RegExp(path==='researcher'?'Quant researcher / Understand':'Quant trader / Understand'));
 run("journeyLessons().forEach(l=>{state.lessons[l.id]={passed:true};l.questions.forEach(id=>state.questions[id]={selfSolved:true});l.coding.forEach(id=>state.coding[id]={accepted:true});});");
 assert.equal(run('nextRouteActivity()'),null,'Optional drills do not prevent core completion');
 assert.doesNotMatch(run('dashboard()'),/code you still have to complete/);assert.match(run('dashboard()'),/Your core route is complete/);assert.doesNotMatch(run('dashboard()'),/Read lesson &amp; take check|Read lesson & take check/);
 assert.match(run('dashboard()'),/self-assessed/);run("route=['paths',path];");assert.match(run('paths()'),/Core route complete/);
}
// Progress filters distinguish true completions, draft work and editorial provenance.
run("state=fresh();route=['questions'];filters={...emptyFilters(),status:'pending'};state.questions.q01={solved:true};state.questions.q21={selfSolved:true};state.questions.q05={reviewed:true};");
assert.equal(run('filtered(content.questions).length'),49);assert.ok(run("filtered(content.questions).some(q=>q.id==='q05')"));
run("filters.status='self-solved';");assert.deepEqual(JSON.parse(run('JSON.stringify(filtered(content.questions).map(q=>q.id))')),['q21']);
run("filters.status='reviewed';");assert.equal(run('filtered(content.questions)[0].id'),'q05');
run("state.coding.c01={accepted:true,acceptedAssisted:false,assisted:true};state.coding.c02={accepted:true,acceptedAssisted:true};state.drafts.c03='def solve(values): return []';state.coding.c04={assisted:true};filters={...emptyFilters(),status:'passed'};route=['coding'];");
assert.equal(run('filtered(coding)[0].id'),'c01','Later editorial reading does not relabel an unaided pass');
run("filters.status='assisted';");assert.equal(run('filtered(coding)[0].id'),'c02');run("filters.status='practising';");assert.equal(run('filtered(coding)[0].id'),'c03');run("filters.status='reviewed';");assert.equal(run('filtered(coding)[0].id'),'c04');
run("filters={...emptyFilters(),search:' impossible-result ',difficulty:'Hard',status:'pending'};route=['questions'];");
assert.equal(run('filtered(content.questions).length'),0);assert.match(run('questionTable([])'),/Clear all filters/);
// Use the real reset handler: restore every control and list without rerendering fields or changing study data.
for(const name of ['search','difficulty','topic','path','status'])els['#'+name]={value:run('filters.'+name),addEventListener:(event,fn)=>handlers[name]=fn,focus(){context.focused=name;}};
els['#page']={contains:()=>false,addEventListener:(event,fn)=>handlers[event]=fn};els['#collection']={innerHTML:''};els['#result-count']={textContent:''};els['#reset-filters']={disabled:false};
const before=run('JSON.stringify(state)');run('bindPage()');
(async()=>{
 await handlers.click({target:{closest:()=>({dataset:{action:'reset-filters'},focus(){}})}});
 assert.equal(els['#search'].value,'');assert.equal(els['#status'].value,'all');assert.equal(els['#difficulty'].value,'all');assert.equal(context.focused,'search');assert.equal(els['#result-count'].textContent,51);assert.equal(els['#reset-filters'].disabled,true);assert.equal(run('JSON.stringify(state)'),before);
 console.log('Core activity resumption, separate checks/practice, both branches, completed routes, optional drills, progress filters, editorial provenance and non-destructive reset passed.');
})().catch(e=>{console.error(e);process.exitCode=1;});
