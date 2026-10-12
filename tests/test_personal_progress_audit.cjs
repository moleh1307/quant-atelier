'use strict';
// All progress, storage, sessions and requests are fixtures; real learning may
// legitimately earn credit later and must never make this regression test fail.
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const source=fs.readFileSync('static/app.js','utf8').replace(/init\(\);\s*$/,'');
const bank=JSON.parse(fs.readFileSync('static/content.json','utf8'));
const codes=JSON.parse(fs.readFileSync('static/coding.json','utf8'));
const personal={version:1,updatedAt:1,questions:{},coding:{},lessons:{},drafts:{c01:'def solve(values, target):\n    pass\n'},trainers:[],preferences:{path:'researcher'}};
const marker='PREVIEW_ONLY_AUDIT_SENTINEL';
const round={id:'preview-round',type:'math',level:'Easy',date:100,elapsed:60,correct:10,attempts:10,meanSeconds:1,finished:true,mistakes:[]};
const preview={...personal,workspace:'preview',updatedAt:Date.now()+10000,
  questions:Object.fromEntries(bank.questions.map(q=>[q.id,{solved:q.type==='numeric',selfSolved:q.type!=='numeric',reviewed:true,due:1}])),
  coding:Object.fromEntries(codes.map(c=>[c.id,{accepted:true}])),
  lessons:Object.fromEntries(bank.lessons.map(l=>[l.id,{passed:true}])),
  drafts:{c01:marker},trainers:[round]};
const runner={workspace:'preview',c01:{mode:'submit',checkedCode:marker,running:false,result:{passed:1,total:1,elapsedMs:1,results:[{passed:true}],stdout:marker}}};
async function harness(overrides={},disk=personal){
  const local={'quant-atelier-v1':JSON.stringify(personal),'quant-atelier-qa':JSON.stringify(preview),
    'quant-atelier-qa-recovery':JSON.stringify({workspace:'preview',date:10,state:preview}),...overrides};
  const session={'quant-atelier-v1-tab-id':'audit-tab','quant-atelier-qa-runner-results':JSON.stringify(runner),
    'quant-atelier-qa-trainer-session':JSON.stringify({workspace:'preview',active:false,round}),
    // Misfiled labelled copies must also be ignored, rather than relying on key names alone.
    'quant-atelier-v1-runner-results':JSON.stringify(runner),
    'quant-atelier-v1-trainer-session':JSON.stringify({workspace:'preview',active:false,round})};
  const app={innerHTML:''},requests=[],errors=[];
  const context={console:{error:e=>errors.push(e)},URLSearchParams,location:{search:'',hash:'#progress'},Date,Math,setTimeout,clearTimeout,
    localStorage:{getItem:k=>local[k]||null,setItem:(k,v)=>local[k]=v,get length(){return Object.keys(local).length;},key:i=>Object.keys(local)[i]},
    sessionStorage:{getItem:k=>session[k]||null,setItem:(k,v)=>session[k]=v},
    fetch:async(url,options)=>{requests.push({url,options});return {ok:true,json:async()=>url==='/content.json'?bank:url==='/coding.json'?codes:{state:disk,revision:'audit'}};},
    document:{querySelector:s=>s==='#app'?app:s==='#page'?{}:null,addEventListener(){}},window:{addEventListener(){}}};
  vm.createContext(context);vm.runInContext(source,context);
  const run=s=>vm.runInContext(s,context);
  for(const [,filename] of fs.readFileSync('static/index.html','utf8').matchAll(/src="\/((?:course-textbook|lesson-[^"?]+)\.js)/g))vm.runInContext(fs.readFileSync('static/'+filename,'utf8'),context);
  run('bindPage=()=>{};bindPanels=()=>{};keepNavigationVisible=()=>{};');await run('init()');
  assert.deepEqual(errors,[]);
  return {context,run,local,session,requests};
}
(async()=>{
  const audit=await harness();
  const before=audit.run('JSON.stringify(state)');
  assert.deepEqual(JSON.parse(audit.run('JSON.stringify(counts())')),{solved:0,reviewed:0,lessons:0,coding:0});
  assert.equal(audit.run('state.trainers.length'),0);
  assert.equal(audit.run('dueQuestions().length'),0);
  assert.equal(audit.run('Object.keys(view).length'),0,'Preview runner feedback must not appear as personal results');
  assert.equal(audit.run('lastSession'),null,'Preview trainer session must not be recovered as personal');
  for(const q of bank.questions)assert.equal(audit.run(`questionStatus('${q.id}')`),'new',q.id);
  for(const c of codes)assert.equal(audit.run(`codingStatus(coding.find(c=>c.id==='${c.id}'))`),personal.drafts[c.id]?.trim()?'practising':'new',c.id);
  const destinations=['dashboard','paths','questions','courses','coding','trainers','review','progress',
    ...bank.questions.map(q=>'questions/'+q.id),...bank.lessons.map(l=>'courses/'+l.id+'/journey/researcher/'+l.id),
    ...codes.map(c=>'coding/'+c.id),...['math','fractions','probability','sequences','pricing'].map(t=>'trainers/'+t),'paths/researcher','paths/trader'];
  for(const destination of destinations){
    audit.context.location.hash='#'+destination;
    audit.run(`route=${JSON.stringify(destination.split('/'))};`);
    const section=destination.split('/')[0],fn=section==='coding'?'codePage':section;
    const html=audit.run(fn+'()');
    assert.ok(!html.includes(marker),destination+' contains no preview text');
    assert.doesNotMatch(html,/✓ Unaided solve|✓ Self-assessed|✓ Exercise passed|✓ Check passed · revisit lesson|Submission saved/,destination+' contains no false personal achievement');
  }
  assert.equal(audit.run('JSON.stringify(state)'),before,'Reading every page earns no credit or changes drafts');
  assert.ok(!audit.requests.some(r=>r.options?.method==='POST'),'Audit makes no disk writes');
  audit.context.foreign=preview;
  assert.equal(audit.run('receiveExternal(foreign)'),false,'Foreign-labelled tab data cannot merge');
  assert.throws(()=>audit.run('checkProgressImport(foreign)'),/development test records/);
  const recovery={workspace:'preview',date:10,state:preview};
  const badCopies={
    'quant-atelier-v1-recovery':JSON.stringify(recovery),
    'quant-atelier-v1-tab-copy-audit-tab':JSON.stringify({workspace:'preview',resolved:true,local:preview,remote:preview}),
    'quant-atelier-v1-pending-write-audit-tab':JSON.stringify({workspace:'preview',pending:true,local:preview,remote:preview})};
  const recovered=await harness(badCopies);
  assert.equal(recovered.run('readRecovery()'),null);
  assert.equal(recovered.run('tabCopyControl()'),'');
  assert.equal(recovered.run('pendingSaveCopies().length'),0);
  assert.equal(recovered.run('counts().solved'),0);
  const misfiled=await harness({'quant-atelier-v1':JSON.stringify(preview)});
  assert.equal(misfiled.run('counts().solved'),0,'Misfiled labelled preview main record is ignored');
  assert.equal(misfiled.run('state.drafts.c01'),personal.drafts.c01,'Personal disk draft survives');
  const foreignDisk=await harness({},preview);
  assert.equal(foreignDisk.run('counts().solved'),0,'Foreign-labelled disk data cannot become personal state');
  assert.equal(foreignDisk.run('state.drafts.c01'),personal.drafts.c01);
  console.log(`Personal audit: ${destinations.length} pages, all question/code statuses, zero achievements/revisions/rounds, runner and trainer recovery, foreign-labelled storage/disk/tab/import rejection and unchanged drafts passed.`);
})().catch(error=>{console.error(error);process.exitCode=1;});
