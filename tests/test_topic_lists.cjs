'use strict';
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const bank=JSON.parse(fs.readFileSync('static/content.json','utf8')),codes=JSON.parse(fs.readFileSync('static/coding.json','utf8'));
const context={URLSearchParams,location:{search:'?qa=1',hash:''},console,Math,Date,setTimeout,clearTimeout,document:{querySelector:()=>null},bank,codes};
vm.createContext(require('./workspace-fixture.cjs')(context));
vm.runInContext(fs.readFileSync('static/app.js','utf8').replace(/init\(\);\s*$/,''),context);
const run=s=>vm.runInContext(s,context);
run('content=bank;coding=codes;state=fresh();');
const before=run('JSON.stringify(state)');
for(const path of ['researcher','trader'])for(const l of bank.lessons.filter(l=>l.path==='shared'||l.path===path)){
 for(const [kind,bankKind,ids] of [['question-list','questions',l.questions],['coding-list','coding',l.coding]]){
  run('route='+JSON.stringify([kind,l.id,'journey',path,l.id]));
  if(ids.length){assert.equal(run('moduleContext().lesson.id'),l.id);assert.equal(run('moduleContext().path'),path);}
  const html=run(`topicPracticePage('${bankKind}')`);
  assert.equal((html.match(/class="topic-level"/g)||[]).length,3);
  for(const level of ['Easy','Medium','Hard'])assert.match(html,new RegExp('id="topic-'+level.toLowerCase()+'"'));
  assert.equal((html.match(/class="topic-practice-row"/g)||[]).length,ids.length);
  for(const id of ids)assert.ok(html.includes(`#${bankKind}/${id}/journey/${path}/${l.id}`));
  if(l.practiceExpanded)assert.doesNotMatch(html,/being prepared/);
  assert.equal(run('JSON.stringify(state)'),before,'List rendering earns no progress');
 }
}
// The retained calibration exercise belongs to its current trader topic in the
// library; its earlier researcher additional-practice bookmark is tested separately.
run("filters.path='trader';");
assert.equal(run("filtered(coding).some(c=>c.id==='c14')"),true);
run("filters.path='researcher';");
assert.equal(run("filtered(coding).some(c=>c.id==='c14')"),false);
run("filters.path='all';");
run("route=['question-list','l01','journey','researcher','l01'];state.questions.q01={solved:true};state.questions.q05={solved:true};state.questions.q_l01_h1={reviewed:true};");
assert.match(run("topicPracticePage('questions')"),/2 \/ 6 passed/);
assert.doesNotMatch(run("topicPracticePage('questions')"),/self-assessed/);
assert.match(run("topicPracticePage('questions')"),/Unaided solve/);
assert.match(run("topicPracticePage('questions')"),/Reviewed/);
assert.equal(run('moduleStageEvidence(content.lessons[0],"Apply")'),'2/6');
assert.equal(run('nextRouteActivity().activity.kind'),'courses','Viewing practice does not pass the lesson check');
run("route=['coding-list','l01','journey','researcher','l01'];state.coding.c01={accepted:true,acceptedAssisted:true};state.drafts.c_l01_medium='my draft';");
assert.match(run("topicPracticePage('coding')"),/1 \/ 3 passed/);
assert.match(run("topicPracticePage('coding')"),/with editorial/);
assert.match(run("topicPracticePage('coding')"),/Draft in progress/);
assert.equal(run('moduleStageEvidence(content.lessons[0],"Implement")'),'1/3');
run("route=['question-list','l01'];");assert.equal(run('moduleContext().lesson.id'),'l01','Bare list bookmarks infer a valid branch');
run("route=['question-list','missing'];");assert.match(run("topicPracticePage('questions')"),/Topic not found/);assert.equal(run('moduleContext()'),null);
console.log('Difficulty sections, every topic list/link, honest aggregate evidence, assistance, drafts, bare bookmarks and rendering without credit passed.');
