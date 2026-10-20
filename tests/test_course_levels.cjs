'use strict';
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const context={console,URLSearchParams,location:{search:'?qa=1',hash:'#courses/l01'},Math,Date,setTimeout,clearTimeout,document:{querySelector:()=>null}};
vm.createContext(require('./workspace-fixture.cjs')(context));const run=s=>vm.runInContext(s,context);
run(fs.readFileSync('static/app.js','utf8').replace(/init\(\);\s*$/,''));
context.bank=JSON.parse(fs.readFileSync('static/content.json'));context.codes=JSON.parse(fs.readFileSync('static/coding.json'));
run("content=bank;coding=codes;route=['courses','l01'];lessonNavigation=()=>'';");
for(const name of ['lesson-sample-space','course-textbook','lesson-conditioning','lesson-expectation'])run(fs.readFileSync('static/'+name+'.js','utf8'));
const baseline=run('JSON.stringify(state)');
for(const id of ['l01','l02','l03']){
 context.lesson=context.bank.lessons.find(l=>l.id===id);
 const authored=run('authoredLesson(lesson)'),html=run('lessonDetail(lesson)'),outline=run('lessonOutline(lesson)');
 assert.deepEqual(Array.from(authored.levels,l=>l.name),['Easy','Medium','Hard']);
 assert.equal(authored.levels[0].start,0);
 for(const [i,level] of authored.levels.entries()){
  const end=authored.levels[i+1]?.start??authored.sections.length;
  assert.ok(end-level.start>=2,'Each level develops multiple ideas: '+id+level.name);
  assert.ok(level.goal.length>60);
  assert.ok(html.includes('data-lesson-level="lesson-section-'+level.start+'"'));
  assert.equal(html.split('<span class="lesson-level-label">'+level.name+'</span>').length-1,1);
  assert.equal(outline.split('<div class="lesson-menu-level">'+level.name+'</div>').length-1,1);
 }
 assert.equal((html.match(/class="lesson-level-start"/g)||[]).length,3);
 const indices=run('lessonSections(lesson)');
 assert.equal(indices.length,authored.sections.length+2);
 for(const s of indices)assert.equal(html.split('id="'+s.id+'"').length-1,1);
 assert.equal((html.match(/id="quiz-form"/g)||[]).length,1);
 assert.ok(!html.includes('type="checkbox"'),'Reading parts introduce no completion toggles');
 assert.ok(!html.includes('<pre'),'No gratuitous code in these probability arguments');
}
for(const l of context.bank.lessons.filter(l=>!['l01','l02','l03'].includes(l.id))){
 context.lesson=l;assert.ok(!run('lessonDetail(lesson)').includes('lesson-level-nav'));assert.ok(!run('lessonOutline(lesson)').includes('lesson-menu-level'));
}
assert.equal(run('JSON.stringify(state)'),baseline);
console.log('Three progressive course parts, substantial topic-specific sections, unique navigation targets, unchanged assessment identity and ungraded reading passed.');
