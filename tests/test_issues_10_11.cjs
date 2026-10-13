'use strict';
// Compare next navigation to ACTUAL rendered lists in every valid journey;
// preserve state rather than deriving completion from navigation.
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const bank=JSON.parse(fs.readFileSync('static/content.json')),codes=JSON.parse(fs.readFileSync('static/coding.json'));
const ctx={console,Math,Date,URLSearchParams,setTimeout,clearTimeout,location:{search:'',hash:''},document:{querySelector:()=>null},bank,codes};vm.createContext(require('./workspace-fixture.cjs')(ctx));const run=s=>vm.runInContext(s,ctx);run(fs.readFileSync('static/app.js','utf8').replace(/init\(\);\s*$/,''));run('content=bank;coding=codes;state=fresh();');
run(`state.drafts.q01='11/36';state.drafts['q01-scratch']='A retained numerical derivation';state.drafts[objectiveDraftKey(content.questions.find(q=>q.id==='q_l01_h1'))]='{"part1":"0.5","part2":["choice1"]}';state.drafts['q_l01_h1-scratch']='A retained structured derivation';`);
const before=run('JSON.stringify(state)');let transitions=0;
for(const path of ['researcher','trader'])for(const lesson of bank.lessons.filter(l=>l.path==='shared'||l.path===path)){
 run('route='+JSON.stringify(['question-list',lesson.id,'journey',path,lesson.id]));
 const list=run("topicPracticePage('questions')"),hrefs=[...list.matchAll(/class="topic-practice-row"[^>]*href="([^"]+)"/g)].map(m=>m[1]);
 assert.equal(hrefs.length,lesson.questions.length);
 for(let i=0;i<hrefs.length;i++){
  run('route='+JSON.stringify(hrefs[i].slice(1).split('/')));
  const context=run('moduleContext()'),html=run('moduleContinuation(moduleContext())');
  assert.equal(context.lesson.id,lesson.id);assert.equal(context.path,path);
  const next=[...html.matchAll(/data-next-question href="([^"]+)"/g)].map(m=>m[1]);
  assert.deepEqual(next,i+1<hrefs.length?[hrefs[i+1]]:[],`${path}/${lesson.id} position ${i}`);
  assert.match(html,new RegExp(`#question-list/${lesson.id}/journey/${path}/${lesson.id}`));
  if(lesson.coding.length)assert.ok(html.includes(`#coding-list/${lesson.id}/journey/${path}/${lesson.id}`));
  assert.ok(html.includes(`#paths/${path}/step-${lesson.id}`));
  assert.equal(run('followingActivity(moduleContext()).kind'),'question-list','The list handoff remains optional navigation, not a forced sequence');
  assert.equal(run('JSON.stringify(state)'),before,'Navigation mutates neither drafts nor grading evidence');
  if(next.length)transitions++;
 }
}
// Explicitly scramble authored IDs: order must match grouped rows, not the
// raw lesson IDs, global bank, title order or completion status.
run("content.lessons[0].questions=['q_l01_h2','q05','q_l01_m2','q01','q_l01_h1','q_l01_m1'];route=['question-list','l01','journey','trader','l01'];");
const ordered=run('topicQuestionSequence(content.lessons[0]).map(q=>q.id)');assert.deepEqual(Array.from(ordered),['q05','q01','q_l01_m2','q_l01_m1','q_l01_h2','q_l01_h1']);
run("route=['questions','q01','journey','trader','l01'];");assert.equal(run('nextModuleQuestion(moduleContext()).id'),'q_l01_m2','Easy→Medium');
run("route=['questions','q_l01_m1','journey','trader','l01'];");assert.equal(run('nextModuleQuestion(moduleContext()).id'),'q_l01_h2','Medium→Hard');
run("state.questions.q_l01_h2={solved:true,assessmentVersion:content.questions.find(q=>q.id==='q_l01_h2').assessmentVersion};");assert.equal(run('nextModuleQuestion(moduleContext()).id'),'q_l01_h2','Solved questions remain in the visible sequence');
run("route=['questions','q_l01_h1','journey','trader','l01'];");assert.equal(run('nextModuleQuestion(moduleContext())'),null,'Final has no wrap');
for(const route of [['courses','l01','journey','trader','l01'],['question-list','l01','journey','trader','l01'],['coding','c01','journey','trader','l01']]){run('route='+JSON.stringify(route));assert.doesNotMatch(run('moduleContinuation(moduleContext())'),/data-next-question/);}
for(const route of [['questions','q01'],['questions','q01','journey','trader','l24'],['questions','q01','journey','other','l01']]){run('route='+JSON.stringify(route));assert.equal(run('moduleContext()'),null);}
// l02 clarification independently fixes experiment/evidence, retaining key
// and option order. The two joint masses normalize to two thirds.
const l02=bank.lessons.find(l=>l.id==='l02'),check=l02.check.replaceAll(String.raw`\(\frac{1}{2}\)`,'1/2');assert.match(check,/fair coin with probability 1\/2/);assert.match(check,/always-heads coin with probability 1\/2/);assert.match(check,/once and observe heads/);assert.match(check,/Conditional on that observation/);assert.match(check,/independent of the exploration controls/);assert.doesNotMatch(check,/this mixture/);assert.deepEqual(l02.options,[String.raw`\(\frac{1}{2}\)`,String.raw`\(\frac{2}{3}\)`,String.raw`\(\frac{3}{4}\)`,'1']);assert.equal(l02.correct,1);assert.equal((.5*1)/(.5*1+.5*.5),2/3);
console.log(`Issues10/11: ${transitions} next links match grouped lists, both branches and boundaries; drafts/credit unchanged; fixed coin experiment/key verified.`);
