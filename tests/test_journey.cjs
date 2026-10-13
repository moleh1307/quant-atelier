'use strict';
// Lesson -> question list -> coding list is bookmarkable; exercises are choices.
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const bank=JSON.parse(fs.readFileSync('static/content.json','utf8')),codeBank=JSON.parse(fs.readFileSync('static/coding.json','utf8'));
const context={URLSearchParams,location:{search:'?qa=1',hash:''},console,Math,Date,setTimeout,clearTimeout,document:{querySelector:()=>null},bank,codeBank};
vm.createContext(require('./workspace-fixture.cjs')(context));vm.runInContext(fs.readFileSync('static/app.js','utf8').replace(/init\(\);\s*$/,''),context);
const run=s=>vm.runInContext(s,context);
run("content=bank;coding=codeBank;state=fresh();route=['paths','trader'];");
assert.match(run('roadmapPractice(content.lessons[0])'),/#courses\/l01\/journey\/trader\/l01/);
assert.match(run('roadmapPractice(content.lessons[0])'),/#question-list\/l01\/journey\/trader\/l01/);
assert.match(run('roadmapPractice(content.lessons[0])'),/#coding-list\/l01\/journey\/trader\/l01/);
const before=run('JSON.stringify(state)');
for(const [kind,id,nextKind,nextId] of [
 ['courses','l01','question-list','l01'],
 ['question-list','l01','coding-list','l01'],
 ['questions','q01','question-list','l01'],
 ['questions','q_l01_h2','question-list','l01'],
 ['coding','c01','coding-list','l01'],
 ['coding','c_l01_hard','coding-list','l01'],
 ['coding-list','l01','courses','l02']]){
 run(`route=['${kind}','${id}','journey','trader','l01']`);
 assert.equal(run('moduleContext().lesson.id'),'l01');assert.equal(run('moduleContext().path'),'trader');
 assert.equal(run('followingActivity(moduleContext()).href'),`#${nextKind}/${nextId}/journey/trader/${nextId==='l02'?'l02':'l01'}`);
 assert.match(run('moduleTrail(moduleContext())'),/aria-current="step"/);
 assert.match(run('moduleTrail(moduleContext())'),/#paths\/trader\/step-l01/);
 assert.equal(run('JSON.stringify(state)'),before,'Navigation earns no study credit');
}
run("route=['courses','l01','journey','trader','l01'];");
assert.match(run('moduleLinks(lessonDetail(content.lessons[0]),moduleContext())'),/#question-list\/l01\/journey\/trader\/l01/);
assert.match(run('lessonNavigation(content.lessons[0])'),/Choose an interview question/);
run("state.questions.q01={reviewed:true};");
assert.equal(run('followingActivity(moduleContext()).kind'),'question-list','Reviewed work does not skip the list');
run("content.lessons[0].questions.forEach(id=>state.questions[id]={solved:true});content.lessons[0].coding.forEach(id=>state.coding[id]={accepted:true});");
assert.equal(run('followingActivity(moduleContext()).kind'),'question-list','The lesson handoff remains an explicit list even after completion');
// Return from a detail to its originating list, then advance explicitly.
for(const [path,next] of [['researcher','l26'],['trader','l19']]){
 run(`route=['coding-list','l08','journey','${path}','l08']`);
 assert.equal(run('followingActivity(moduleContext()).href'),`#courses/${next}/journey/${path}/${next}`);
}
run("route=['questions','q44','journey','researcher','l18']");assert.equal(run('moduleContext().lesson.id'),'l18');
assert.match(run("practiceBreadcrumb('questions','Research coding')"),/#question-list\/l18\/journey\/researcher\/l18/);
run("route=['questions','q44','journey','researcher','l08']");assert.equal(run('moduleContext().lesson.id'),'l08');
for(const route of ["['questions','q01']","['questions','q01','journey','trader','l24']","['questions','q01','journey','trader','missing']","['questions','q01','journey','other','l01']","['coding','c01','journey','researcher','l24']","['question-list','l25','journey','trader','l25']"]){
 run('route='+route);assert.equal(run('moduleContext()'),null,'Invalid or unrelated context cannot claim another module');
}
run("route=['courses','l21'];");assert.equal(run('moduleContext().path'),'trader');
run("route=['trainers','math','journey','researcher','l06'];");assert.equal(run('followingActivity(moduleContext()).id'),'fractions','Optional fluency drills retain their continuity');
run("route=['coding-list','l24','journey','trader','l24'];");
assert.equal(run('followingActivity(moduleContext())'),null);assert.match(run('moduleContinuation(moduleContext())'),/End of this route/);
// Every old activity bookmark and every new list resolves to its own module.
for(const path of ['researcher','trader'])for(const l of bank.lessons.filter(l=>l.path==='shared'||l.path===path)){
 for(const a of run(`[...moduleActivities(content.lessons.find(l=>l.id==='${l.id}'),'${path}'),...moduleLegacyActivities(content.lessons.find(l=>l.id==='${l.id}'),'${path}'),...moduleSteps(content.lessons.find(l=>l.id==='${l.id}'),'${path}')]`)){
  run('route='+JSON.stringify(a.href.slice(1).split('/')));
  assert.equal(run('moduleContext().lesson.id'),l.id);assert.equal(run('moduleContext().path'),path);
 }
}
// A removed slot is still a valid saved-work destination, never a fourth slot.
for(const path of ['researcher','trader']){
 run(`route=['coding','c05','journey','${path}','l08'];state=fresh();`);
 assert.equal(run('moduleContext().additional'),true);
 assert.equal(run('followingActivity(moduleContext()).href'),`#coding-list/l08/journey/${path}/l08`);
 assert.match(run('moduleTrail(moduleContext())'),/Implement/);
 assert.match(run('moduleSupplementNotice(moduleContext())'),/Additional practice/);
 assert.match(run("practiceBreadcrumb('coding','Time-aware data')"),new RegExp(`#coding-list/l08/journey/${path}/l08`));
 assert.match(run('moduleLinks(\'<a href="#coding/c05">old saved work</a>\',moduleContext())'),new RegExp(`#coding/c05/journey/${path}/l08`));
 run("state.coding.c05={accepted:true};state.drafts.c05='my original draft';");
 assert.equal(run('moduleStageEvidence(content.lessons.find(l=>l.id===\'l08\'),"Implement")'),'0/3');
 run(`route=['coding-list','l08','journey','${path}','l08'];`);
 const list=run("topicPracticePage('coding')");
 assert.doesNotMatch(list,/#coding\/c05\//);
 assert.match(list,/0 \/ 3 passed/);
 assert.equal(run('state.drafts.c05'),'my original draft');
}
// l14 retains its former second Medium exercise through a permanent bookmark.
run("route=['coding','c10','journey','researcher','l14'];state=fresh();");
assert.equal(run('moduleContext().additional'),true);
assert.equal(run('followingActivity(moduleContext()).href'),'#coding-list/l14/journey/researcher/l14');
assert.match(run('moduleSupplementNotice(moduleContext())'),/Additional practice/);
run("state.coding.c10={accepted:true};state.drafts.c10='saved old fold implementation';");
assert.equal(run('moduleStageEvidence(content.lessons.find(l=>l.id===\'l14\'),"Implement")'),'0/3');
run("route=['coding-list','l14','journey','researcher','l14'];");
assert.doesNotMatch(run("topicPracticePage('coding')"),/#coding\/c10\//);
assert.equal(run('state.drafts.c10'),'saved old fold implementation');
// l18 replaces unrelated calibration only in its current list; its old work survives.
run("route=['coding','c14','journey','researcher','l18'];state=fresh();");
assert.equal(run('moduleContext().additional'),true);
assert.equal(run('followingActivity(moduleContext()).href'),'#coding-list/l18/journey/researcher/l18');
assert.match(run('moduleSupplementNotice(moduleContext())'),/Additional practice/);
run("state.coding.c14={accepted:true};state.drafts.c14='old calibration draft';");
assert.equal(run('moduleStageEvidence(content.lessons.find(l=>l.id===\'l18\'),"Implement")'),'0/3');
run("route=['coding-list','l18','journey','researcher','l18'];");
assert.doesNotMatch(run("topicPracticePage('coding')"),/#coding\/c14\//);
assert.match(run("topicPracticePage('coding')"),/#coding\/c_l18_easy\//);
assert.equal(run('state.drafts.c14'),'old calibration draft');
run("route=['coding','c14','journey','trader','l24'];");
assert.equal(run('moduleContext().additional'),undefined);
assert.equal(run('moduleStageEvidence(content.lessons.find(l=>l.id===\'l24\'),"Implement")'),'1/3');
run("route=['coding','c05','journey','researcher','l18'];");
assert.equal(run('moduleContext().lesson.id'),'l18');
assert.equal(run('moduleContext().additional'),undefined,'Another module may still own that current exercise');
run("route=['coding-list','l09','journey','researcher','l09'];");
assert.equal(run('followingActivity(moduleContext()).href'),'#courses/l25/journey/researcher/l25');
run("route=['coding-list','l25','journey','researcher','l25'];");
assert.equal(run('followingActivity(moduleContext()).href'),'#courses/l10/journey/researcher/l10');
assert.equal(run("moduleNumber(content.lessons.find(l=>l.id==='l25'))"),'12');
console.log('Lesson -> grouped question list -> coding list, free exercise choice, return links, both branches, all old/new bookmarks and no navigation credit passed.');
