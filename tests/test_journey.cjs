'use strict';
// Module context is bookmarkable, branch-specific and independent of score writes.
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const bank=JSON.parse(fs.readFileSync('static/content.json','utf8')),codeBank=JSON.parse(fs.readFileSync('static/coding.json','utf8'));
const context={URLSearchParams,location:{search:'?qa=1',hash:''},console,Math,Date,setTimeout,clearTimeout,document:{querySelector:()=>null},bank,codeBank};
vm.createContext(require('./workspace-fixture.cjs')(context));vm.runInContext(fs.readFileSync('static/app.js','utf8').replace(/init\(\);\s*$/,''),context);
const run=s=>vm.runInContext(s,context);
run("content=bank;coding=codeBank;state=fresh();route=['paths','trader'];");
assert.match(run('roadmapPractice(content.lessons[0])'),/#courses\/l01\/journey\/trader\/l01/);
const before=run('JSON.stringify(state)');
for(const [kind,id,next] of [['courses','l01','q01'],['questions','q01','q05'],['questions','q05','c01'],['coding','c01','l02']]){
 run(`route=['${kind}','${id}','journey','trader','l01']`);
 assert.equal(run('moduleContext().lesson.id'),'l01');assert.equal(run('moduleContext().path'),'trader');
 assert.ok(run('followingActivity(moduleContext()).href').includes('/'+next+'/journey/trader/'));
 assert.match(run('moduleTrail(moduleContext())'),/aria-current="step"/);
 assert.match(run('moduleTrail(moduleContext())'),/#paths\/trader\/step-l01/);
 assert.equal(run('JSON.stringify(state)'),before,'Navigation and module indicators earn no study credit');
}
// A lesson's existing practice links also retain the originating branch.
run("route=['courses','l01','journey','trader','l01']");
assert.match(run('moduleLinks(lessonDetail(content.lessons[0]),moduleContext())'),/#questions\/q05\/journey\/trader\/l01/);
assert.match(run('lessonNavigation(content.lessons[0])'),/Open problem/);
run("state.questions.q01={reviewed:true};");
assert.equal(run('followingActivity(moduleContext()).id'),'q01','Reviewed work does not become solved');
run("state.questions.q01={solved:true};");
assert.equal(run('followingActivity(moduleContext()).id'),'q05','Resume the first outstanding exercise after a lesson');
run("state.questions.q05={selfSolved:true};state.coding.c01={accepted:true};");
assert.ok(run('followingActivity(moduleContext()).href').includes('/l02/journey/trader/l02'));
// The shared-to-specialist boundary follows the bookmarked branch, not preferences.
const sharedLast=bank.lessons.find(l=>l.id==='l08'),lastCode=sharedLast.coding.at(-1);
for(const [path,next] of [['researcher','l09'],['trader','l19']]){
 run(`route=['coding','${lastCode}','journey','${path}','l08']`);
 assert.ok(run('followingActivity(moduleContext()).href').includes('/'+next+'/journey/'+path+'/'+next));
}
// A shared exercise retains its exact origin rather than guessing a parent lesson.
run("route=['questions','q44','journey','researcher','l18']");assert.equal(run('moduleContext().lesson.id'),'l18');
run("route=['questions','q44','journey','researcher','l08']");assert.equal(run('moduleContext().lesson.id'),'l08');
for(const route of ["['questions','q01']","['questions','q01','journey','trader','l24']","['questions','q01','journey','trader','missing']","['questions','q01','journey','other','l01']","['coding','c01','journey','researcher','l24']"]){
 run('route='+route);assert.equal(run('moduleContext()'),null,'Invalid or unrelated context falls back to standalone practice');
}
run("route=['courses','l21'];");assert.equal(run('moduleContext().path'),'trader');
run("route=['trainers','math','journey','researcher','l06'];");assert.equal(run('followingActivity(moduleContext()).id'),'fractions');
const last=bank.lessons.find(l=>l.id==='l24');
run(`route=['coding','${last.coding.at(-1)}','journey','trader','l24']`);
assert.equal(run('followingActivity(moduleContext())'),null);assert.match(run('moduleContinuation(moduleContext())'),/End of this route/);
// Every activity has a valid independent bookmark and resolves to its own module.
for(const path of ['researcher','trader'])for(const l of bank.lessons.filter(l=>l.path==='shared'||l.path===path)){
 for(const a of run(`moduleActivities(content.lessons.find(l=>l.id==='${l.id}'),'${path}')`)){
  run('route='+JSON.stringify(a.href.slice(1).split('/')));
  assert.equal(run('moduleContext().lesson.id'),l.id);
  assert.equal(run('moduleContext().path'),path);
 }
}
const estimationLast=run("moduleActivities(content.lessons.find(l=>l.id==='l09'),'researcher')").at(-1);
run('route='+JSON.stringify(estimationLast.href.slice(1).split('/')));
assert.equal(run('followingActivity(moduleContext()).href'),'#courses/l25/journey/researcher/l25');
run("route=['coding','c15','journey','researcher','l25'];");
assert.equal(run('followingActivity(moduleContext()).href'),'#courses/l10/journey/researcher/l10');
assert.equal(run("moduleNumber(content.lessons.find(l=>l.id==='l25'))"),'10');
console.log('Lesson→problem→code continuity, new likelihood placement, reload bookmarks, branch boundaries, shared exercises, honest evidence and all activity destinations passed.');
