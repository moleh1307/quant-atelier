'use strict';
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const source=fs.readFileSync('static/app.js','utf8').replace(/init\(\);\s*$/,'');
const bank=JSON.parse(fs.readFileSync('static/content.json','utf8')),codes=JSON.parse(fs.readFileSync('static/coding.json','utf8'));
function harness(qa=true,stored={}){let failing='';const ctx={console,Date,Math,URLSearchParams,location:{search:qa?'?qa=1':'',hash:'#progress'},bank,codes,document:{querySelector:()=>null},setTimeout:()=>0,clearTimeout(){},localStorage:{getItem:k=>stored[k]||null,setItem(k,v){if(k===failing)throw Error('Quota');stored[k]=v;}}};vm.createContext(require('./workspace-fixture.cjs')(ctx));vm.runInContext(source,ctx);const run=js=>vm.runInContext(js,ctx);run('content=bank;coding=codes;route=["progress"];');return {ctx,stored,run,fail:k=>failing=k};}
const h=harness();
h.run("state={...fresh(),updatedAt:10,lessons:{l01:{passed:true}},coding:{c02:{accepted:true,acceptedAssisted:false}},drafts:{c01:'my unfinished code'},questions:{q01:{solved:true},q21:{selfSolved:true}},trainers:[]};view={c01:{result:{passed:0,total:5}}};");
const original=h.run('JSON.stringify(state)'),incoming=h.run('({...fresh(),updatedAt:5,workspace:"preview",drafts:{c01:"older draft"}})');h.ctx.incoming=incoming;
h.run('stageProgressImport(incoming,"backup <script>.json")');assert.equal(h.run('JSON.stringify(state)'),original);assert.match(h.run('backupReview()'),/backup &lt;script&gt;.json/);assert.match(h.run('backupReview()'),/Current/);
// Both storage writes must succeed before any study record or stale feedback changes.
h.fail('quant-atelier-qa-recovery');assert.throws(()=>h.run('replaceProgressFromImport()'),/Nothing was replaced/);assert.equal(h.run('JSON.stringify(state)'),original);
h.fail('quant-atelier-qa');assert.throws(()=>h.run('replaceProgressFromImport()'),/Nothing was replaced/);assert.equal(h.run('JSON.stringify(state)'),original);assert.ok(h.run('pendingImport'));
h.fail('');h.run('view.c01.running=true');assert.throws(()=>h.run('replaceProgressFromImport()'),/Python check/);assert.equal(h.run('JSON.stringify(state)'),original);h.run('view.c01.running=false;replaceProgressFromImport()');
assert.equal(h.run('state.drafts.c01'),'older draft');assert.equal(h.run('counts().lessons'),0);assert.equal(h.run('Object.keys(view).length'),0);assert.equal(h.run('pendingImport'),null);assert.equal(h.run('JSON.stringify(readRecovery().state)'),original);assert.match(h.run('recoveryControl()'),/Review previous record/);assert.equal(h.run('state.workspace'),undefined);
// Recovery survives reload and can be reviewed/restored. Latest edited record is kept as its replacement copy.
const reloaded=harness(true,h.stored);reloaded.run('state=JSON.parse(localStorage.getItem(KEY));browserBase=cloneRecord(state);state.drafts.c01="edited imported draft";stageProgressImport({...readRecovery().state,workspace:"preview"},"Previous record");replaceProgressFromImport();');
assert.equal(reloaded.run('state.drafts.c01'),'my unfinished code');assert.equal(reloaded.run('counts().lessons'),1);assert.equal(reloaded.run('readRecovery().state.drafts.c01'),'edited imported draft');
assert.ok(h.stored['quant-atelier-qa-recovery']);assert.equal(h.stored['quant-atelier-v1-recovery'],undefined);
const personal=harness(false,h.stored);personal.ctx.incoming=incoming;assert.equal(personal.run('readRecovery()'),null);assert.throws(()=>personal.run('stageProgressImport(incoming,"preview")'),/development test records/);
for(const prefs of ['researcher',{path:'bogus'},[],null]){personal.ctx.badPrefs=prefs;assert.throws(()=>personal.run('checkProgressImport({...fresh(),preferences:badPrefs})'),/route preference/);}
assert.throws(()=>personal.run('checkProgressImport({...fresh(),workspace:"other"})'),/valid Quant/);
assert.doesNotThrow(()=>personal.run('checkProgressImport(fresh())'));assert.match(personal.run('progress()'),/<button[^>]*data-action="choose-import"/);assert.doesNotMatch(personal.run('progress()'),/<label[^>]*for="import-file"/);
const focusFrames=[];let reviewFocus=0;personal.ctx.requestAnimationFrame=fn=>focusFrames.push(fn);personal.ctx.document.querySelector=()=>({focus(){reviewFocus++;},scrollIntoView(){}});personal.run('focusBackupReview();renderEpoch++;');while(focusFrames.length)focusFrames.shift()();assert.equal(reviewFocus,0,'Stale review focus cannot affect another page');personal.run('focusBackupReview()');while(focusFrames.length)focusFrames.shift()();assert.equal(reviewFocus,1);
console.log('Import staging, current/backup comparison, two storage failure boundaries, in-flight runner protection, reload recovery, restored drafts/provenance and preview isolation passed.');
