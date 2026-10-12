'use strict';
// Test completion provenance and overlapping runner requests without study writes.
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const source=fs.readFileSync('static/app.js','utf8').replace(/init\(\);\s*$/,'');
const bank=JSON.parse(fs.readFileSync('static/content.json','utf8'));
const codes=JSON.parse(fs.readFileSync('static/coding.json','utf8'));
const routeQuestions=new Set(bank.lessons.filter(l=>l.path!=='trader').flatMap(l=>l.questions)).size;
const routeCodes=new Set(bank.lessons.filter(l=>l.path!=='trader').flatMap(l=>l.coding)).size;

function harness(qa=true){
 const calls=[],writes=[],context={URLSearchParams,location:{search:qa?'?qa=1':'',hash:'#coding/c01'},console,Math,Date,
  setTimeout:()=>0,clearTimeout(){},localStorage:{getItem:()=>null,setItem(){}},document:{querySelector:()=>null},bank,codes,
  fetch:(url,options)=>new Promise(resolve=>calls.push({url,options,resolve}))};
 vm.createContext(require('./workspace-fixture.cjs')(context));vm.runInContext(source,context);
 vm.runInContext("content=bank;coding=codes;route=['coding','c01'];render=()=>{};",context);
 return {context,calls,writes,run:s=>vm.runInContext(s,context)};
}
const response=(result,ok=true)=>({ok,json:async()=>Number.isInteger(result.total)&&result.total>0&&Number.isInteger(result.passed)?{...result,elapsedMs:0,results:Array.from({length:result.total},(_,i)=>({passed:i<result.passed}))}:result});
(async()=>{
 const h=harness();
 // A sample-only implementation passes Run, fails Submit, and must never earn credit.
 const sample=h.run("executeCode(coding[0],'run','def solve(values,target): return 2')");
 assert.equal(h.calls.length,1);
 assert.match(h.run('codeDetail(coding[0])'),/data-action="submit-code" disabled/);
 await h.run("executeCode(coding[0],'submit','def solve(values,target): return 2')");
 assert.equal(h.calls.length,1,'A second request is blocked while the sample is running');
 // Even a changing UI mode cannot turn a sample request into a full submission.
 h.run("view.c01.mode='submit'");
 h.calls[0].resolve(response({passed:1,total:1}));await sample;
 assert.equal(h.run('!!state.coding.c01?.accepted'),false);
 const full=h.run("executeCode(coding[0],'submit','def solve(values,target): return 2')");
 h.calls[1].resolve(response({passed:1,total:5}));await full;
 assert.equal(h.run('!!state.coding.c01?.accepted'),false);
 for(const [result,ok] of [[{passed:0,total:0},true],[{},true],[{passed:5,total:5},false]]){
  const request=h.run("executeCode(coding[0],'submit','bad')");h.calls.at(-1).resolve(response(result,ok));await request;
  assert.equal(h.run('!!state.coding.c01?.accepted'),false,'Invalid or unsuccessful results earn no pass');
 }
 // Editorial reads after a successful unaided pass must not rewrite its provenance.
 const unaided=h.run("executeCode(coding[0],'submit','correct')");
 h.calls.at(-1).resolve(response({passed:5,total:5}));await unaided;
 h.run("markEditorialRead('c01')");
 assert.equal(h.run('acceptedWithEditorial(state.coding.c01)'),false);
 assert.doesNotMatch(h.run('codeTable([coding[0]])'),/with editorial/);
 // Reading during execution also does not alter the captured submitted attempt.
 h.run('state=fresh()');const inFlight=h.run("executeCode(coding[0],'submit','correct')");
 h.run("markEditorialRead('c01')");h.calls.at(-1).resolve(response({passed:5,total:5}));await inFlight;
 assert.equal(h.run('acceptedWithEditorial(state.coding.c01)'),false);
 const assisted=h.run("executeCode(coding[0],'submit','correct')");
 h.calls.at(-1).resolve(response({passed:5,total:5}));await assisted;
 assert.equal(h.run('acceptedWithEditorial(state.coding.c01)'),true);
 // Legacy passes retain their former assistance status when first reviewed again.
 h.run("state.coding.c01={accepted:true};markEditorialRead('c01')");
 assert.equal(h.run('acceptedWithEditorial(state.coding.c01)'),false);
 h.run("state.coding.c01={accepted:true,assisted:true};markEditorialRead('c01')");
 assert.equal(h.run('acceptedWithEditorial(state.coding.c01)'),true);
 const before=h.calls.length;await h.run('flush()');assert.equal(h.calls.length,before,'Preview cannot write disk even if flush is called directly');

 const personal=harness(false);personal.context.preview=h.run('progressExport()');
 assert.throws(()=>personal.run('checkProgressImport(preview)'),/development test records/);
 assert.equal(personal.run('Object.keys(state.coding).length'),0,'Rejected preview import leaves personal state alone');
 assert.equal(personal.run('progressExport().workspace'),'personal');
 assert.doesNotThrow(()=>personal.run('checkProgressImport(fresh())'),'Older personal backups remain importable');
 assert.equal(personal.run("validState({...fresh(),lessons:{l01:{passed:'false'}}})"),false);
 personal.run("content=bank;coding=codes;state.lessons.obsolete={passed:true};state.coding.obsolete={accepted:true};");
 assert.equal(personal.run('counts().lessons'),0);assert.equal(personal.run('counts().coding'),0);
 assert.match(personal.run('statGrid()'),new RegExp('/ '+bank.questions.filter(q=>q.type==='numeric').length+'</span></span><span class="muted">UNAIDED NUMERIC SOLVES'));
 assert.match(h.run('progress()'),/cannot be imported into personal progress/);
 // The roadmap's own counters must identify preview results even when its top notice is offscreen.
 const routePreview=harness();
 routePreview.context.location.hash='#paths/researcher';
 routePreview.run("route=['paths','researcher'];state.questions.q20={solved:true};state.questions.q21={selfSolved:true};state.coding.c01={accepted:true};");
 const previewRoute=routePreview.run('paths()');
 assert.match(previewRoute,new RegExp('Test problems: 2 / '+routeQuestions+' interview problems solved'));
 assert.match(previewRoute,new RegExp('Test exercises: 1 / '+routeCodes+' Python exercises passed'));
 assert.match(previewRoute,/Development results, separate from your progress/);
 assert.match(previewRoute,/href="\/#paths\/researcher">Open my personal route/);
 const routePersonal=harness(false);
 routePersonal.run("route=['paths','researcher'];");
 const personalRoute=routePersonal.run('paths()');
 assert.match(personalRoute,new RegExp('0 / '+routeQuestions+' interview problems solved'));
 assert.match(personalRoute,new RegExp('0 / '+routeCodes+' Python exercises passed'));
 assert.doesNotMatch(personalRoute,/Test problems:|Test exercises:|route-preview-note/);
 // A blank understanding check cannot accidentally choose option zero.
 let quizHandler,choice=null,notice='';
 personal.context.FormData=class {get(){return choice;}};
 personal.context.document.querySelector=selector=>selector==='#quiz-form'?{addEventListener:(name,fn)=>quizHandler=fn}:selector==='#page'?{addEventListener(){}}:null;
 personal.context.captureNotice=message=>notice=message;
 personal.run("route=['courses','l21'];notify=captureNotice;bindPage()");
 quizHandler({preventDefault(){},target:{}});
 assert.equal(personal.run('!!state.lessons.l21?.passed'),false);
 assert.match(notice,/Choose an answer/);
 choice='0';quizHandler({preventDefault(){},target:{}});
 assert.equal(personal.run('state.lessons.l21.passed'),true);

 // Render every library entry and check the generated practice destinations.
 const audit=harness();const pages=[];
 for(const destination of ['dashboard','paths','questions','courses','coding','trainers','review','progress']){
  audit.run(`route=['${destination}']`);
  pages.push(audit.run(({coding:'codePage'}[destination]||destination)+'()'));
 }
 for(const q of bank.questions)pages.push(audit.run(`questionDetail(content.questions.find(q=>q.id==='${q.id}'))`));
 for(const l of bank.lessons)pages.push(audit.run(`lessonDetail(content.lessons.find(l=>l.id==='${l.id}'))`));
 for(const c of codes)pages.push(audit.run(`codeDetail(coding.find(c=>c.id==='${c.id}'))`));
 const ids={questions:new Set(bank.questions.map(q=>q.id)),courses:new Set(bank.lessons.map(l=>l.id)),coding:new Set(codes.map(c=>c.id)),trainers:new Set(['math','fractions','probability','sequences','pricing'])};
 for(const html of pages)for(const [,section,id] of html.matchAll(/href="#(questions|courses|coding|trainers)\/([^"/]+)"/g))assert.ok(ids[section].has(id),section+'/'+id);
 console.log('Runner overlap, full-suite credit, editorial provenance, backup isolation, totals, quiz selection and 94 page/link renders passed.');
})().catch(error=>{console.error(error);process.exitCode=1;});
