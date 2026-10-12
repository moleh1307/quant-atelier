'use strict';
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const source=fs.readFileSync('static/app.js','utf8').replace(/init\(\);\s*$/,'');
const bank=JSON.parse(fs.readFileSync('static/content.json','utf8')),codes=JSON.parse(fs.readFileSync('static/coding.json','utf8'));
function harness(qa=true,storage={},id='a'){
 let fail='',chosen='local';const session={};session[(qa?'quant-atelier-qa':'quant-atelier-v1')+'-tab-id']=id;
 const ctx={URLSearchParams,location:{hash:'#coding/c01',search:qa?'?qa=1':''},console,Date,Math,bank,codes,setTimeout:()=>0,clearTimeout(){},sessionStorage:{getItem:k=>session[k]||null,setItem:(k,v)=>session[k]=v},localStorage:{get length(){return Object.keys(storage).length;},key:i=>Object.keys(storage)[i],getItem:k=>storage[k]||null,setItem(k,v){if(k===fail)throw Error('Quota');storage[k]=v;}},document:{querySelector:s=>s.startsWith('input[name="sync-')?{value:chosen}:null},window:{},fetch:async()=>{throw Error('No network fixture');}};
 vm.createContext(require('./workspace-fixture.cjs')(ctx));vm.runInContext(source,ctx);const run=s=>vm.runInContext(s,ctx);run('content=bank;coding=codes;route=["coding","c01"];render=()=>{};state=storedProgress()||fresh();browserBase=cloneRecord(state);');return {run,ctx,storage,choose:v=>chosen=v,fail:k=>fail=k};
}
(async()=>{
 const storage={},a=harness(true,storage,'a'),b=harness(true,storage,'b');
 // Closing before a queued Web Lock runs still leaves a synchronous recoverable record.
 const closingStore={},closing=harness(true,closingStore,'closing');
 closing.ctx.navigator={locks:{request:()=>new Promise(()=>{})}};
 closing.run('state.drafts.c01="last edit before close";touch()');
 assert.equal(closingStore['quant-atelier-qa'],undefined,'The queued publication has not run');
 assert.equal(JSON.parse(closingStore['quant-atelier-qa-pending-write-closing']).local.drafts.c01,'last edit before close');
 const newTab=harness(true,closingStore,'new-tab');assert.match(newTab.run('syncNotice()'),/recoverable changes/);assert.match(newTab.run('otherTabCopies()'),/Interrupted tab save/);
 assert.equal(harness(false,closingStore,'personal').run('pendingSaveCopies().length'),0,'Preview journals stay out of personal recovery');
 // A restored document merges the pending edit with independent already-published work.
 closingStore['quant-atelier-qa']=JSON.stringify({version:1,updatedAt:99,questions:{q01:{solved:true}},coding:{},lessons:{},drafts:{c02:'another tab'},trainers:[],preferences:{path:'researcher'}});
 const reopened=harness(true,closingStore,'closing');await reopened.run('restorePendingWrite()');
 assert.equal(reopened.run('state.drafts.c01'),'last edit before close');assert.equal(reopened.run('state.drafts.c02'),'another tab');assert.equal(reopened.run('state.questions.q01.solved'),true);
 assert.equal(closingStore['quant-atelier-qa-pending-write-closing'],'null');assert.equal(reopened.run('syncConflict'),null);
 // Competing edits are reviewed instead of resurrecting either text silently.
 const disputedStore={},disputed=harness(true,disputedStore,'disputed');disputed.ctx.navigator=closing.ctx.navigator;disputed.run('state.drafts.c01="pending version";touch()');
 disputedStore['quant-atelier-qa']=JSON.stringify({...JSON.parse(closingStore['quant-atelier-qa']),drafts:{c01:'published version'}});
 const disputedReload=harness(true,disputedStore,'disputed');await disputedReload.run('restorePendingWrite()');assert.ok(disputedReload.run('syncConflict'));assert.equal(disputedReload.run('state.drafts.c01'),'pending version');
 disputedReload.choose('remote');disputedReload.run('resolveSyncConflict()');assert.equal(disputedReload.run('state.drafts.c01'),'published version');assert.equal(disputedStore['quant-atelier-qa-pending-write-disputed'],'null');
 // Rejected locks/storage never erase the journal; reviewing an orphan uses backup comparison.
 const failedStore={},failed=harness(true,failedStore,'failed');failed.ctx.navigator={locks:{request:()=>Promise.reject(Error('unavailable'))}};failed.run('state.drafts.c01="recover me";touch()');await failed.run('browserWrites');assert.match(failed.run('saved'),/save unavailable/);assert.equal(JSON.parse(failedStore['quant-atelier-qa-pending-write-failed']).local.drafts.c01,'recover me');
 const orphan=harness(true,failedStore,'replacement');orphan.run('stageProgressImport({...JSON.parse(localStorage.getItem("quant-atelier-qa-pending-write-failed")).local,workspace:"preview"},"Interrupted save");pendingImport.pendingCopyKey="quant-atelier-qa-pending-write-failed"');
 orphan.fail('quant-atelier-qa');assert.throws(()=>orphan.run('replaceProgressFromImport()'),/Nothing was replaced/);assert.notEqual(failedStore['quant-atelier-qa-pending-write-failed'],'null');orphan.fail('');orphan.run('replaceProgressFromImport()');assert.equal(orphan.run('state.drafts.c01'),'recover me');assert.equal(failedStore['quant-atelier-qa-pending-write-failed'],'null');assert.equal(orphan.run('pendingSaveCopies().length'),0);
 a.run('state.drafts.c01="draft A";touch()');b.run('state.drafts.c02="draft B";touch()');
 let primary=JSON.parse(storage['quant-atelier-qa']);assert.equal(primary.drafts.c01,'draft A');assert.equal(primary.drafts.c02,'draft B');assert.equal(b.run('syncConflict'),null,'Independent draft changes merge');
 a.ctx.event={key:'quant-atelier-qa',newValue:storage['quant-atelier-qa']};a.run('handleStorageChange(event)');assert.equal(a.run('state.drafts.c02'),'draft B');
 a.run('state.drafts.c01="new A";touch()');b.run('state.drafts.c01="new B";touch()');
 assert.equal(JSON.parse(storage['quant-atelier-qa']).drafts.c01,'new A','Stale tab cannot overwrite competing draft');assert.equal(b.run('state.drafts.c01'),'new B');assert.ok(b.run('syncConflict'));assert.match(b.run('syncReview()'),/Count pairs/);assert.match(b.run('syncNotice()'),/Both are kept/);
 const copy=JSON.parse(storage['quant-atelier-qa-tab-copy-b']);assert.equal(copy.local.drafts.c01,'new B');assert.equal(copy.remote.drafts.c01,'new A');
 // A reloaded pending tab retains its own complete record; alternatives survive resolution.
 b.fail('quant-atelier-qa');assert.throws(()=>b.run('resolveSyncConflict()'),/Could not save/);assert.ok(b.run('syncConflict'));assert.equal(JSON.parse(storage['quant-atelier-qa-tab-copy-b']).resolved,false);b.fail('');b.choose('remote');b.run('resolveSyncConflict()');assert.equal(b.run('state.drafts.c01'),'new A');assert.equal(b.run('syncConflict'),null);assert.match(b.run('tabCopyControl()'),/previous copy/);assert.equal(JSON.parse(storage['quant-atelier-qa-tab-copy-b']).local.drafts.c01,'new B');
 const c=harness(true,storage,'c');assert.match(c.run('otherTabCopies()'),/Other saved tab copies/);assert.equal(harness(false,storage,'personal').run('otherTabCopies()'),'');
 // Record conflicts retain assistance provenance instead of combining incompatible attempts.
 c.run('state.coding.c01={accepted:true,acceptedAssisted:false};touch()');a.run('state.coding.c01={accepted:true,acceptedAssisted:true};touch()');assert.ok(a.run('syncConflict'));assert.equal(JSON.parse(storage['quant-atelier-qa']).coding.c01.acceptedAssisted,false);
 // Trainer additions are deduplicated and both retained; key order alone is not a change.
 assert.equal(a.run('sameRecord({a:1,b:2},{b:2,a:1})'),true);
 a.run('var base=fresh(),local=fresh(),remote=fresh();local.trainers=[{date:1,type:"math"}];remote.trainers=[{type:"math",date:1},{date:2,type:"fractions"}];');assert.equal(a.run('mergeProgress(base,local,remote).state.trainers.length'),2);
 // An open, unchanged editor still offers the saved alternative before replacing its text.
 const editing=harness(true,storage,'editing');editing.run('syncConflict=null;state=storedProgress();browserBase=cloneRecord(state);');editing.ctx.remote=JSON.parse(storage['quant-atelier-qa']);editing.ctx.remote.drafts.c01='external replacement';editing.run('receiveExternal(remote)');assert.ok(editing.run('syncConflict'));assert.equal(editing.run('state.drafts.c01'),'new A');
 // Disk CAS conflict with independent work merges and retries against the returned revision.
 const diskStore={},disk=harness(false,diskStore,'disk');const calls=[];
 disk.run('state.drafts.c01="local Python";touch();diskBase=fresh();diskRevision="r1";');
 disk.ctx.fetch=async(url,options)=>{calls.push(JSON.parse(options.body));if(calls.length===1)return {ok:false,status:409,json:async()=>({state:{version:1,updatedAt:9,questions:{q01:{solved:true}},coding:{},lessons:{},drafts:{},trainers:[],preferences:{path:'researcher'}},revision:'r2'})};return {ok:true,status:200,json:async()=>({saved:true,revision:'r3'})};};
 await disk.run('flush()');assert.equal(calls.length,2);assert.equal(calls[0].revision,'r1');assert.equal(calls[1].revision,'r2');assert.equal(calls[1].state.drafts.c01,'local Python');assert.equal(calls[1].state.questions.q01.solved,true);assert.equal(disk.run('saved'),'Saved locally');assert.equal(disk.run('diskRevision'),'r3');
 // With Web Locks, simultaneous tabs serialize publication and read the latest primary copy.
 const lockedStore={},lockedA=harness(true,lockedStore,'locked-a'),lockedB=harness(true,lockedStore,'locked-b');let lockQueue=Promise.resolve(),activeLocks=0,maxLocks=0;const names=[];
 const locks={request(name,action){names.push(name);const operation=lockQueue.then(async()=>{activeLocks++;maxLocks=Math.max(maxLocks,activeLocks);try{return await action();}finally{activeLocks--;}});lockQueue=operation.catch(()=>{});return operation;}};
 lockedA.ctx.navigator={locks};lockedB.ctx.navigator={locks};lockedA.run('state.drafts.c03="left tab";touch()');lockedB.run('state.drafts.c04="right tab";touch()');
 await Promise.all([lockedA.run('browserWrites'),lockedB.run('browserWrites')]);assert.equal(maxLocks,1);assert.ok(names.every(name=>name==='quant-atelier-qa-write'));assert.equal(JSON.parse(lockedStore['quant-atelier-qa']).drafts.c03,'left tab');assert.equal(JSON.parse(lockedStore['quant-atelier-qa']).drafts.c04,'right tab');
 lockedA.run('state.drafts.c05="competing left";touch()');lockedB.run('state.drafts.c05="competing right";touch()');await Promise.all([lockedA.run('browserWrites'),lockedB.run('browserWrites')]);assert.equal(JSON.parse(lockedStore['quant-atelier-qa']).drafts.c05,'competing left');assert.ok(lockedB.run('syncConflict'));assert.equal(lockedB.run('state.drafts.c05'),'competing right');
 // Same-draft disk conflict pauses writes, preserves local text and the server copy.
 const conflict=harness(false,{},'disk-conflict');conflict.run('state.drafts.c01="ours";touch();diskBase={...fresh(),drafts:{c01:"base"}};diskRevision="old";');let count=0;conflict.ctx.fetch=async()=>{count++;return {ok:false,status:409,json:async()=>({state:{version:1,updatedAt:99,questions:{},coding:{},lessons:{},drafts:{c01:'theirs'},trainers:[],preferences:{path:'researcher'}},revision:'new'})};};await conflict.run('flush()');assert.equal(count,1);assert.equal(conflict.run('state.drafts.c01'),'ours');assert.equal(conflict.run('syncConflict.remote.drafts.c01'),'theirs');await conflict.run('flush()');assert.equal(count,1);
 console.log('Stale-tab independent merges, conflicting drafts/provenance, persisted alternatives, storage failure, orphan recovery, editor protection, trainer union, Web Locks serialization and disk CAS retry/pause passed.');
})().catch(error=>{console.error(error);process.exitCode=1;});
