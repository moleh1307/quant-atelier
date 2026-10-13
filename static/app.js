'use strict';
const $ = selector => document.querySelector(selector);
let codeEditor=null,releaseReadingOutline=null,releaseModuleOutline=null;
const esc = value => String(value ?? '').replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
function typesetMath(root){
  if(typeof renderMathInElement!=='function')return;
  renderMathInElement(root,{
    delimiters:[{left:'\\[',right:'\\]',display:true},{left:'\\(',right:'\\)',display:false}],
    ignoredTags:['script','noscript','style','textarea','pre','code','option'],
    ignoredClasses:['math-plain'],output:'htmlAndMathml',trust:false,strict:'error',throwOnError:false,
    errorCallback:message=>console.error('Math typesetting:',message)
  });
}
// Trainer expressions contain only generated numbers and arithmetic operators.
// Written prompts and user-entered text never pass through this conversion.
function trainerMath(prompt){
  if(!/^[\d\s.,?+−×÷/]+$/.test(prompt))return esc(prompt);
  const tex=prompt.replace(/(\d+)\s*\/\s*(\d+)/g,'\\frac{$1}{$2}').replaceAll('−','-').replaceAll('×','\\times ').replaceAll('÷','\\div ');
  return esc('\\('+tex+'\\)');
}
const QA = typeof QuantAtelierWorkspace!=='undefined' && QuantAtelierWorkspace.preview===true;
const KEY = QA ? 'quant-atelier-qa' : 'quant-atelier-v1';
// Layout choices are separate from study records and never update practice scores.
const LAYOUT_KEY=KEY+'-layout';
let panels={navigation:true,practice:true},navigationReturn=null;
try{
  const stored=JSON.parse(localStorage.getItem(LAYOUT_KEY));
  for(const name of ['navigation','practice'])if(typeof stored?.[name]==='boolean')panels[name]=stored[name];
}catch{}
const fresh = () => ({version:1,updatedAt:0,questions:{},coding:{},lessons:{},drafts:{},trainers:[],preferences:{path:'researcher'}});
let state=fresh(), content, coding, route, saving=false, saveTimer, pending=false, saved='Opening…';
let filters={search:'',difficulty:'all',topic:'all',path:'all',status:'all'};
let view={};
// Tab-local navigation memory never writes to study records or the disk backup.
const NAV_KEY=KEY+'-navigation';
const RECOVERY_KEY=KEY+'-recovery';
let pendingImport=null,importFeedback='';
let browserBase=fresh(),diskBase=fresh(),diskRevision, syncConflict=null,browserWrites=Promise.resolve();
let tabID='tab-'+Date.now()+'-'+Math.random().toString(36).slice(2);
try{tabID=sessionStorage.getItem(KEY+'-tab-id')||tabID;sessionStorage.setItem(KEY+'-tab-id',tabID);}catch{}
const CONFLICT_KEY=KEY+'-tab-copy-'+tabID;
const PENDING_WRITE_KEY=KEY+'-pending-write-'+tabID;
const TRAINING_KEY=KEY+'-trainer-session';
const RUNNER_KEY=KEY+'-runner-results';
let runnerGeneration=0;
const emptyFilters=()=>({search:'',difficulty:'all',topic:'all',path:'all',status:'all'});
let navigation={},renderedHash=null,renderEpoch=0,scrollTimer,departingFocus=null;
try{const cached=JSON.parse(sessionStorage.getItem(NAV_KEY));if(cached&&typeof cached==='object'&&!Array.isArray(cached))navigation=cached;}catch{}
const frame=callback=>typeof requestAnimationFrame==='function'?requestAnimationFrame(callback):callback();
function pageFocus(){
  const el=document.activeElement,page=$('#page');
  if(!el||!page?.contains?.(el))return null;
  if(el.closest?.('.cm-content'))return {kind:'editor'};
  let focus=null;
  if(el.id)focus={kind:'id',value:el.id};
  else if(el.dataset?.action)focus={kind:'action',value:el.dataset.action};
  else if(el.matches?.('input[type="radio"]'))focus={kind:'radio',name:el.name,value:el.value};
  else if(el.matches?.('button[type="submit"]')&&el.form?.id)focus={kind:'submit',value:el.form.id};
  else if(el.matches?.('a[href]'))focus=linkFocus(el);
  if(focus&&typeof el.selectionStart==='number')focus.selection=[el.selectionStart,el.selectionEnd];
  return focus;
}
function linkFocus(el){
  const value=el.getAttribute('href'),links=Array.from(document.querySelectorAll?.('#page a[href]')||[]).filter(link=>link.getAttribute('href')===value);
  return {kind:'link',value,slot:Math.max(0,links.indexOf(el))};
}
function restoreFocus(focus){
  if(!focus)return;
  let el;
  if(focus.kind==='editor')el=$('#code-host .cm-content');
  if(focus.kind==='id')el=document.getElementById?.(focus.value);
  const all=selector=>Array.from(document.querySelectorAll?.(selector)||[]);
  if(focus.kind==='action')el=all('#page [data-action]').find(el=>el.dataset.action===focus.value);
  if(focus.kind==='radio')el=all('#page input[type="radio"]').find(el=>el.name===focus.name&&el.value===focus.value);
  if(focus.kind==='submit')el=document.getElementById?.(focus.value)?.querySelector('button[type="submit"]');
  if(focus.kind==='link')el=all('#page a[href]').filter(el=>el.getAttribute('href')===focus.value)[focus.slot||0];
  if(!el||el.disabled||el.closest?.('[inert]'))return;
  el.focus?.({preventScroll:true});
  if(focus.selection)try{el.setSelectionRange(...focus.selection);}catch{}
}
function captureNavigation(){
  if(!renderedHash)return;
  const open=Array.from(document.querySelectorAll?.('.roadmap-step')||[]).map(el=>({id:el.id,open:el.open}));
  navigation[renderedHash]={y:Math.max(0,window.scrollY||0),filters:{...filters},open,focus:departingFocus||pageFocus()};
  const keys=Object.keys(navigation);while(keys.length>60)delete navigation[keys.shift()];
  try{sessionStorage.setItem(NAV_KEY,JSON.stringify(navigation));}catch{}
}
function restoreNavigation(){
  const hash=location.hash||'#dashboard',memory=navigation[hash],epoch=renderEpoch;
  frame(()=>{
    if(epoch!==renderEpoch)return;
    for(const item of memory?.open||[]){const step=document.getElementById?.(item.id);if(step?.matches?.('.roadmap-step'))step.open=item.open===true;}
    if(route[0]==='progress'&&route[1]==='reconcile'&&syncConflict){const heading=$('#sync-review-title');heading?.focus({preventScroll:true});heading?.scrollIntoView({block:'center'});return;}
    if(route[0]==='progress'&&route[1]==='tab-copies'){const copies=$('#tab-copy-history');if(copies){copies.open=true;copies.querySelector('summary')?.focus({preventScroll:true});copies.scrollIntoView({block:'center'});return;}}
    if(route[0]==='paths'&&/^step-l\d{2}$/.test(route[2]||'')){locateRoadmapStep();return;}
    window.scrollTo?.(0,Number.isFinite(memory?.y)?memory.y:0);
    if(memory?.focus)restoreFocus(memory.focus);
    else {const heading=$('#page h1');heading?.setAttribute?.('tabindex','-1');heading?.focus?.({preventScroll:true});}
  });
}
function navigatePage(){
  captureNavigation();departingFocus=null;
  const memory=navigation[location.hash||'#dashboard'];
  filters={...emptyFilters(),...(memory?.filters||{})};
  render();restoreNavigation();
}
function retainFormFocus(event){
  if(!pageFocus())event.submitter?.focus?.({preventScroll:true});
}
function skipToPractice(){
  const heading=$('#page h1')||$('#page');if(!heading)return;
  heading.setAttribute('tabindex','-1');heading.focus({preventScroll:true});
  window.scrollTo({top:Math.max(0,(window.scrollY||0)+heading.getBoundingClientRect().top-readingOffset()),behavior:'auto'});
}
function capturePageUI(){
  return {y:window.scrollY||0,focus:pageFocus(),
    choices:Array.from(document.querySelectorAll?.('#page input[type="radio"]:checked')||[]).map(el=>({name:el.name,value:el.value})),
    selects:Array.from(document.querySelectorAll?.('#page select[id]')||[]).map(el=>({id:el.id,value:el.value}))};
}
function restorePageUI(ui,epoch){
  for(const choice of ui.choices)for(const el of document.querySelectorAll?.('#page input[type="radio"]')||[])if(el.name===choice.name&&el.value===choice.value)el.checked=true;
  for(const item of ui.selects){const el=document.getElementById?.(item.id);if(el)el.value=item.value;}
  frame(()=>{if(epoch!==renderEpoch)return;window.scrollTo?.(0,ui.y);restoreFocus(ui.focus);});
}
function announce(message){
  const el=$('#announcer');if(!el)return;
  el.textContent='';frame(()=>{el.textContent=message;});
}

const pathName = path => ({shared:'Shared foundation',researcher:'Quant researcher',trader:'Quant trader'}[path]);
const dateLabel = timestamp => new Date(timestamp).toLocaleDateString(undefined,{month:'short',day:'numeric'});
const badge = level => `<span class="badge ${esc(level)}">${esc(level)}</span>`;
// Lucide v1.49.0. See static/vendor/lucide/LICENSE for upstream notices.
const icon = name => `<svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><use href="/vendor/lucide/icons.svg#${esc(name)}"/></svg>`;
const artwork = (n=0) => `<svg viewBox="0 0 400 140" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="1.1" opacity=".8">${n%3===0?'<ellipse cx="200" cy="70" rx="132" ry="52" transform="rotate(-25 200 70)"/><ellipse cx="200" cy="70" rx="132" ry="52" transform="rotate(25 200 70)" stroke-dasharray="3 6"/><path d="M45 115C95 115 135-40 210 25S290 130 370 12"/>':n%3===1?'<circle cx="120" cy="70" r="90"/><circle cx="210" cy="70" r="90" stroke-dasharray="3 6"/><circle cx="300" cy="70" r="90" stroke-dasharray="3 6"/><path d="M30 70h340" opacity=".4"/>':'<path d="M70 0v140M155 0v140M240 0v140M325 0v140" stroke-dasharray="3 5"/><path d="m0 130 90-85 90 45 90-65 130 35"/><path d="M0 15 400 130" stroke-dasharray="3 5"/>'}</g><circle cx="${n%3===0?248:n%3===1?300:270}" cy="${n%3===0?34:n%3===1?70:25}" r="6" fill="currentColor"/></svg>`;
function validState(candidate) {
  const object=value=>value && typeof value==='object' && !Array.isArray(value);
  return object(candidate) && candidate.version===1 && ['questions','coding','lessons','drafts'].every(k=>object(candidate[k]))
    && ['questions','coding','lessons'].every(k=>Object.values(candidate[k]).every(object))
    && ['questions','coding','lessons'].every(k=>Object.values(candidate[k]).every(s=>['solved','selfSolved','reviewed','assisted','accepted','acceptedAssisted','passed'].every(flag=>s[flag]===undefined||typeof s[flag]==='boolean')))
    && Object.values(candidate.drafts).every(v=>typeof v==='string')
    && Number.isFinite(candidate.updatedAt) && candidate.updatedAt>=0
    && Array.isArray(candidate.trainers) && candidate.trainers.every(s=>object(s)
      && typeof s.type==='string' && ['Easy','Medium','Hard'].includes(s.level)
      && Number.isFinite(s.date) && Number.isFinite(s.elapsed) && s.elapsed>=0
      && Number.isInteger(s.correct) && Number.isInteger(s.attempts) && s.correct>=0 && s.attempts>=s.correct
      && (s.meanSeconds===null||Number.isFinite(s.meanSeconds)) && typeof s.finished==='boolean'
      && Array.isArray(s.mistakes) && s.mistakes.every(m=>object(m)&&typeof m.prompt==='string'&&typeof m.given==='string'&&Number.isFinite(m.answer)));
}
const cloneRecord=value=>JSON.parse(JSON.stringify(value));
// Structure alone does not establish provenance. Known preview records must
// never be adopted from disk, another tab or recovery storage in personal mode.
const validWorkspaceState=candidate=>validState(candidate) && (candidate.workspace===undefined || candidate.workspace===(QA?'preview':'personal'));
function stableValue(value){if(value===undefined)return 'undefined';if(value===null||typeof value!=='object')return JSON.stringify(value);if(Array.isArray(value))return '['+value.map(stableValue).join(',')+']';return '{'+Object.keys(value).sort().map(k=>JSON.stringify(k)+':'+stableValue(value[k])).join(',')+'}';}
const sameRecord=(a,b)=>stableValue(a)===stableValue(b);
function mergeProgress(base,local,remote){
  const merged={...fresh(),updatedAt:Math.max(local.updatedAt,remote.updatedAt)},conflicts=[];
  for(const group of ['questions','coding','lessons','drafts','preferences']){
    const before=base[group]||{},ours=local[group]||{},theirs=remote[group]||{},joined=Object.create(null);
    for(const id of new Set([...Object.keys(before),...Object.keys(ours),...Object.keys(theirs)])){
      let value;
      if(sameRecord(ours[id],theirs[id])||sameRecord(theirs[id],before[id]))value=ours[id];
      else if(sameRecord(ours[id],before[id]))value=theirs[id];
      else{value=ours[id];conflicts.push({group,id,local:ours[id],remote:theirs[id]});}
      if(value!==undefined)joined[id]=value;
    }
    merged[group]=joined;
  }
  if(sameRecord(local.trainers,base.trainers))merged.trainers=remote.trainers;
  else if(sameRecord(remote.trainers,base.trainers))merged.trainers=local.trainers;
  else merged.trainers=[...new Map([...local.trainers,...remote.trainers].map(round=>[stableValue(round),round])).values()].sort((a,b)=>a.date-b.date).slice(-200);
  return {state:cloneRecord(merged),conflicts};
}
function storedProgress(){try{const stored=JSON.parse(localStorage.getItem(KEY));return validWorkspaceState(stored)?stored:null;}catch{return null;}}
function persistConflict(){
  if(!syncConflict)return;
  syncConflict.local=cloneRecord(state);
  syncConflict.conflicts=syncConflict.conflicts.map(item=>({...item,local:state[item.group]?.[item.id],remote:syncConflict.remote[item.group]?.[item.id]}));
  try{localStorage.setItem(CONFLICT_KEY,JSON.stringify({...syncConflict,date:Date.now(),workspace:QA?'preview':'personal',resolved:false}));}
  catch{saved='Tab conflict · export this copy now';}
}
function receiveExternal(remote,base=browserBase){
  if(!validWorkspaceState(remote))return false;
  const result=mergeProgress(base,state,remote);
  state=result.state;
  // Preserve an open editor/answer when the same draft changes elsewhere.
  if(base===browserBase&&route&&['coding','questions'].includes(route[0])){
    for(const id of [route[1],route[1]+'-scratch',...(route[0]==='coding'?[route[1]+'-tests']:[])])if(!sameRecord(base.drafts[id],remote.drafts[id])&&!sameRecord(base.drafts[id],undefined)&&!sameRecord(base.drafts[id],state.drafts[id])&&!result.conflicts.some(c=>c.group==='drafts'&&c.id===id)){
      result.conflicts.push({group:'drafts',id,local:base.drafts[id],remote:remote.drafts[id]});state.drafts[id]=base.drafts[id];
    }
  }
  if(result.conflicts.length||syncConflict){
    const existing=syncConflict?.conflicts||[];
    const conflicts=[...new Map([...existing,...result.conflicts].map(c=>[c.group+'.'+c.id,c])).values()];
    syncConflict={local:cloneRecord(state),remote:cloneRecord(remote),conflicts};saved='Changes need review';persistConflict();
  }
  if(base===browserBase)browserBase=cloneRecord(remote);
  return !syncConflict;
}
function syncNotice(){
  if(syncConflict)return `<aside class="sync-notice" role="status"><span>Two copies have changes. Both are kept; review them before continuing to save.</span><a href="#progress/reconcile">Review changes ↗</a></aside>`;
  const copies=pendingSaveCopies();
  return copies.length?`<aside class="sync-notice" role="status"><span>An interrupted tab has recoverable changes.</span><a href="#progress/tab-copies">Review saved tab copies ↗</a></aside>`:'';
}
function pendingSaveCopies(){
  const copies=[];
  try{for(let i=0;i<(localStorage.length||0);i++){const key=localStorage.key(i);if(!key?.startsWith(KEY+'-pending-write-'))continue;const copy=JSON.parse(localStorage.getItem(key));if(copy?.pending&&copy.workspace===(QA?'preview':'personal')&&validWorkspaceState(copy.local)&&validWorkspaceState(copy.remote)&&!sameRecord(copy.local,storedProgress()))copies.push({key,copy});}}catch{}
  return copies;
}
function updateSyncNotice(){if(route?.[0]==='progress'&&syncConflict&&!$('#sync-review-title')){render();return;}const notice=$('#sync-notice');if(notice)notice.innerHTML=syncNotice();}
function publishProgress(){
  const remote=storedProgress();if(remote&&!sameRecord(remote,browserBase))receiveExternal(remote);
  if(syncConflict){persistConflict();updateSyncNotice();updateSave();return false;}
  try{localStorage.setItem(KEY,JSON.stringify(state));browserBase=cloneRecord(state);saved=QA?'Test records · browser only':'Saved in browser';try{localStorage.setItem(PENDING_WRITE_KEY,'null');}catch{}}
  catch{saved='Storage full · export progress';}
  updateSave();return true;
}
function withProgressLock(action){return typeof navigator!=='undefined'&&navigator.locks?.request?navigator.locks.request(KEY+'-write',action):Promise.resolve().then(action);}
function commitBrowserProgress(){
  if(!publishProgress())return;
  if(!QA){clearTimeout(saveTimer);saveTimer=setTimeout(flush,500);}
}
function touch() {
  state.updatedAt=Math.max(Date.now(),state.updatedAt+1);
  if(typeof navigator!=='undefined'&&navigator.locks?.request){
    // This synchronous copy survives closing the document before its lock runs.
    try{localStorage.setItem(PENDING_WRITE_KEY,JSON.stringify({local:state,remote:browserBase,date:Date.now(),workspace:QA?'preview':'personal',pending:true}));}catch{}
    browserWrites=browserWrites.then(()=>withProgressLock(commitBrowserProgress)).catch(()=>{saved='Tab save unavailable · export progress';updateSave();});
  }else commitBrowserProgress();
}
async function restorePendingWrite(){
  let copy;try{copy=JSON.parse(localStorage.getItem(PENDING_WRITE_KEY));}catch{return;}
  if(!copy?.pending||copy.workspace!==(QA?'preview':'personal')||!validWorkspaceState(copy.local)||!validWorkspaceState(copy.remote)||syncConflict)return;
  const primary=cloneRecord(state);
  state=cloneRecord(copy.local);browserBase=cloneRecord(copy.remote);receiveExternal(primary);
  if(!syncConflict)await withProgressLock(commitBrowserProgress);
}
async function flush() {
  if(QA||syncConflict)return;
  await browserWrites;if(syncConflict)return;
  if(saving){pending=true;return;}
  saving=true;pending=false;
  try{
    if(diskRevision===undefined){const response=await fetch('/api/progress');if(!response.ok)throw Error('Save unavailable');const data=await response.json();diskRevision=data.revision??null;const remote=validWorkspaceState(data.state)?data.state:fresh();if(!receiveExternal(remote,diskBase))return;diskBase=cloneRecord(remote);if(!await withProgressLock(publishProgress))return;}
    for(let attempt=0;attempt<3;attempt++){
      const snapshot=cloneRecord(state),response=await fetch('/api/progress',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({state:snapshot,revision:diskRevision})});
      const data=await response.json?.()||{};
      if(response.status===409){const remote=validWorkspaceState(data.state)?data.state:null;if(!remote)throw Error('Invalid saved copy');diskRevision=data.revision;const before=diskBase;diskBase=cloneRecord(remote);if(!receiveExternal(remote,before)||!await withProgressLock(publishProgress))return;continue;}
      if(!response.ok)throw Error('Save failed');
      diskRevision=data.revision??null;diskBase=snapshot;saved='Saved locally';if(!sameRecord(state,snapshot))pending=true;return;
    }
    saved='Browser saved · retry disk backup';
  }catch{saved='Browser saved · disk unavailable';}
  finally{saving=false;updateSave();updateSyncNotice();if(pending&&!syncConflict)flush();}
}
function handleStorageChange(event){
  if(event.key!==KEY||!event.newValue)return;
  try{const remote=JSON.parse(event.newValue);if(!validWorkspaceState(remote))return;receiveExternal(remote);if(content&&coding)render();else updateSave();}catch{}
}
function syncFieldTitle(item){
  if(item.group==='preferences')return 'Learning route';
  const id=item.id.replace(/-(?:scratch|tests)$/,''),entry=item.group==='coding'||item.group==='drafts'&&id.startsWith('c')?coding.find(c=>c.id===id):item.group==='lessons'?content.lessons.find(l=>l.id===id):content.questions.find(q=>q.id===id);
  return (item.id.endsWith('-scratch')?'Scratchpad · ':'')+(entry?.title||item.id);
}
function syncValue(item,value){
  if(item.group==='drafts')return `<pre>${esc(value===undefined?'No saved draft':value)}</pre>`;
  if(item.group==='preferences')return `<p>${esc(pathName(value)||value||'No route selected')}</p>`;
  if(value===undefined)return '<p>No saved result</p>';
  const result=item.group==='lessons'?(value.passed?'Check passed':'Check to do'):item.group==='coding'?(value.accepted?(acceptedWithEditorial(value)?'Passed with editorial':'Passed without editorial'):value.assisted?'Editorial read':'No Python pass'):value.solved?'Unaided solve':value.selfSolved?'Self-assessed':value.reviewed?'Reviewed':'Not yet solved';
  return `<p>${result}${value.attempts!==undefined?' · '+value.attempts+' attempts':''}${value.due?' · revision '+esc(dateLabel(value.due)):''}</p>`;
}
function syncReview(){
  if(!syncConflict)return '';
  return `<section class="sync-review" aria-labelledby="sync-review-title"><div class="eyebrow">Reconcile your copies</div><h3 id="sync-review-title" tabindex="-1">Choose which changes to keep</h3><p>Independent changes have been combined. Choose a version for each item edited in both copies. Both full records remain available after saving.</p>${syncConflict.conflicts.map((item,i)=>`<fieldset class="sync-choice"><legend>${esc(syncFieldTitle(item))}</legend>${[['local','This tab',item.local],['remote','Saved copy',item.remote]].map(([value,label,record])=>`<label><span><input type="radio" name="sync-${i}" value="${value}" ${value==='local'?'checked':''}> ${label}</span>${syncValue(item,record)}</label>`).join('')}</fieldset>`).join('')}<button class="btn dark" type="button" data-action="resolve-sync">Save chosen changes</button></section>`;
}
function resolveSyncConflict(){
  if(!syncConflict)return;
  if(Object.values(view).some(v=>v?.running))throw Error('Wait for the Python check to finish before reconciling copies.');
  const latest=storedProgress();if(latest&&!sameRecord(latest,browserBase)){receiveExternal(latest);throw Error('The saved copy changed again. Review the refreshed choices.');}
  const previous=cloneRecord(syncConflict),next=cloneRecord(state);
  syncConflict.conflicts.forEach((item,i)=>{const choice=$(`input[name="sync-${i}"]:checked`)?.value||'local',value=choice==='remote'?item.remote:state[item.group]?.[item.id];if(value===undefined)delete next[item.group][item.id];else next[item.group][item.id]=value;});
  next.updatedAt=Math.max(Date.now(),state.updatedAt+1);
  try{localStorage.setItem(CONFLICT_KEY,JSON.stringify({...previous,date:Date.now(),workspace:QA?'preview':'personal',resolved:true}));localStorage.setItem(KEY,JSON.stringify(next));}
  catch{try{localStorage.setItem(CONFLICT_KEY,JSON.stringify({...previous,date:Date.now(),workspace:QA?'preview':'personal',resolved:false}));}catch{}throw Error('Could not save the chosen changes. Both copies remain; export this tab’s progress before freeing storage.');}
  state=next;browserBase=cloneRecord(next);syncConflict=null;view={};try{localStorage.setItem(PENDING_WRITE_KEY,'null');}catch{}importFeedback='Chosen changes saved. Both previous copies are available below.';updateSyncNotice();saved=QA?'Test records · browser only':'Saved in browser';updateSave();if(!QA){clearTimeout(saveTimer);saveTimer=setTimeout(flush,500);}
}
function otherTabCopies(){
  const copies=[];
  try{for(let i=0;i<(localStorage.length||0);i++){const key=localStorage.key(i);if(key===CONFLICT_KEY||!(key?.startsWith(KEY+'-tab-copy-')||key?.startsWith(KEY+'-pending-write-')))continue;const copy=JSON.parse(localStorage.getItem(key));if(copy?.workspace===(QA?'preview':'personal')&&validWorkspaceState(copy.local)&&validWorkspaceState(copy.remote)&&(!copy.pending||!sameRecord(copy.local,storedProgress())))copies.push({key,copy});}}catch{}
  return copies.length?`<details class="tab-copy-history" id="tab-copy-history"><summary>Other saved tab copies · ${copies.length}</summary><div class="tab-copy-list">${copies.sort((a,b)=>b.copy.date-a.copy.date).map(({key,copy})=>`<div><p>${copy.pending?'Interrupted tab save · ':''}Kept on ${esc(new Date(copy.date).toLocaleString())}</p><div class="answer-buttons"><button class="btn compact" type="button" data-action="review-other-tab" data-copy-key="${esc(key)}" data-copy-part="local">Review tab copy</button><button class="btn compact" type="button" data-action="review-other-tab" data-copy-key="${esc(key)}" data-copy-part="remote">Review saved copy</button></div></div>`).join('')}</div></details>`:'';
}
function tabCopyControl(){
  try{const copy=JSON.parse(localStorage.getItem(CONFLICT_KEY));if(copy?.resolved&&copy.workspace===(QA?'preview':'personal')&&validWorkspaceState(copy.local)&&validWorkspaceState(copy.remote))return `<details class="tab-copy-history"><summary>Copies kept before reconciling</summary><div class="answer-buttons"><button class="btn compact" type="button" data-action="review-tab-local">Review this tab’s previous copy</button><button class="btn compact" type="button" data-action="review-tab-remote">Review previous saved copy</button></div></details>`;}catch{}
  return '';
}
function saveNeedsAttention(){return !['Opening…','Saved locally','Saved in browser','Test records · browser only'].includes(saved);}
function saveStatus(){const attention=saveNeedsAttention();return `<div class="save-status" id="save-status" role="status" aria-live="polite"${attention?'':' hidden'}><span id="save-label">${attention?esc(saved):''}</span></div>`;}
function updateSave(){const status=$('#save-status'),label=$('#save-label');if(status)status.hidden=!saveNeedsAttention();if(label)label.textContent=saveNeedsAttention()?saved:'';}
function notify(message){$('#toast').textContent=message;$('#toast').classList.add('visible');setTimeout(()=>$('#toast').classList.remove('visible'),3000);}
function questionRecordState(q,record={}){
  return {...record,solved:record.solved===true&&(q?.type!=='structured'||record.assessmentVersion===q.assessmentVersion),selfSolved:false,reviewed:!!(record.reviewed||record.selfSolved)};
}
function questionState(id){return questionRecordState(content?.questions.find(q=>q.id===id),state.questions[id]||{});}
function questionStatus(id){const s=questionState(id);return s.solved?'solved':s.selfSolved?'self-solved':s.reviewed?'reviewed':s.attempts?'practising':'new';}
function statusHTML(id){const status=questionStatus(id);return `<span class="status ${status==='solved'?'solved':status==='reviewed'?'reviewed':''}">${({solved:'✓ Unaided solve','self-solved':'✓ Self-assessed',reviewed:'↗ Reviewed',practising:'In practice',new:'—'}[status])}</span>`;}
function dueQuestions(){return content.questions.filter(q=>questionState(q.id).due && questionState(q.id).due<=Date.now()).sort((a,b)=>questionState(a.id).due-questionState(b.id).due);}
function revisionHref(q){return '#questions/'+q.id+'/revision';}
function revisionContext(q){
  if(route[2]!=='revision')return '';
  const due=questionState(q.id).due,next=dueQuestions().find(item=>item.id!==q.id);
  return `<nav class="revision-context" aria-label="Revision session"><div><a href="#review">← Revision queue</a><span>${due?(due<=Date.now()?'Due now · ':'Scheduled · ')+esc(dateLabel(due)):'Not currently scheduled'}</span></div><div class="revision-actions"><button class="btn link compact" type="button" data-action="new-attempt">Fresh revision</button>${next?`<a href="${revisionHref(next)}">Next due: ${esc(next.title)} ↗</a>`:'<span class="small muted revision-empty">No other problems due</span>'}</div></nav>`;
}
function previousAttempt(q){
  const answer=state.drafts[(q.type==='structured'?objectiveDraftKey(q):q.id)+'-previous']||'',scratch=state.drafts[q.id+'-scratch-previous']||'',v=view[q.id]||{};
  if(!answer&&!scratch)return '';
  return `<section class="previous-attempt"><button class="btn link" type="button" data-action="previous-attempt" aria-expanded="${!!v.previous}">${v.previous?'Hide':'Show'} previous attempt</button>${v.previous?`<div><p class="practice-note">Kept when you began a fresh attempt. Viewing or restoring this text counts as assistance for the current attempt.</p>${answer?`<div class="eyebrow">Previous ${q.type==='structured'?'checkpoint answers':'answer'}</div><pre>${esc(answer)}</pre>`:''}${scratch?`<div class="eyebrow">Previous scratchpad</div><pre>${esc(scratch)}</pre>`:''}<button class="btn compact" type="button" data-action="restore-attempt">Restore previous text</button></div>`:''}</section>`;
}
function freshQuestionAttempt(q){
  for(const key of [q.type==='structured'?objectiveDraftKey(q):q.id,q.id+'-scratch']){if(state.drafts[key]?.trim())state.drafts[key+'-previous']=state.drafts[key];state.drafts[key]='';}
  const s=state.questions[q.id]||={};s.hints=0;s.reveal=false;s.assisted=false;view[q.id]={feedback:'Fresh attempt ready. Previous text is kept below when available.',feedbackClass:''};
}
function restoreQuestionAttempt(q){
  for(const key of [q.type==='structured'?objectiveDraftKey(q):q.id,q.id+'-scratch']){const previous=state.drafts[key+'-previous'];if(typeof previous==='string'){state.drafts[key+'-previous']=state.drafts[key]||'';state.drafts[key]=previous;}}
  (state.questions[q.id]||={}).assisted=true;view[q.id]={feedback:'Previous text restored. This attempt is marked as assisted.',feedbackClass:''};
}
function counts(){return {solved:content.questions.filter(q=>questionState(q.id).solved===true).length,reviewed:content.questions.filter(q=>questionState(q.id).reviewed||questionState(q.id).selfSolved).length,lessons:content.lessons.filter(l=>state.lessons[l.id]?.passed===true).length,coding:coding.filter(c=>state.coding[c.id]?.accepted===true).length};}
// Accepted-result provenance is separate from a later editorial review.
function acceptedWithEditorial(s){return s.acceptedAssisted??!!s.assisted;}
function markEditorialRead(id){
  const s=state.coding[id]||={};
  if(s.accepted&&s.acceptedAssisted===undefined)s.acceptedAssisted=!!s.assisted;
  s.assisted=true;touch();
}
function progressExport(){return {...state,workspace:QA?'preview':'personal'};}
function checkProgressImport(imported){
  if(!validState(imported)||!['personal','preview',undefined].includes(imported.workspace))throw Error('This is not a valid Quant Atelier progress export.');
  if(imported.preferences!==undefined&&(!imported.preferences||typeof imported.preferences!=='object'||Array.isArray(imported.preferences)||(imported.preferences.path!==undefined&&!['researcher','trader'].includes(imported.preferences.path))))throw Error('The backup has an invalid route preference.');
  if(imported.workspace==='preview'&&!QA)throw Error('This backup contains development test records. Open Test preview to import it; your personal progress was not changed.');
}
function backupTotals(record){
  return {checks:content.lessons.filter(l=>record.lessons[l.id]?.passed).length,
    problems:content.questions.filter(q=>questionRecordState(q,record.questions[q.id]).solved).length,
    code:coding.filter(c=>record.coding[c.id]?.accepted).length,
    drafts:Object.values(record.drafts).filter(value=>value.trim()).length,rounds:record.trainers.length};
}
function readRecovery(){
  try{const recovery=JSON.parse(localStorage.getItem(RECOVERY_KEY));if(recovery&&validWorkspaceState(recovery.state)&&Number.isFinite(recovery.date)&&recovery.workspace===(QA?'preview':'personal')){checkProgressImport({...recovery.state,workspace:recovery.workspace});return recovery;}}catch{}
  return null;
}
function stageProgressImport(imported,name){
  checkProgressImport(imported);
  pendingImport={state:JSON.parse(JSON.stringify(imported)),name:String(name||'Progress backup')};importFeedback='';
}
function replaceProgressFromImport(){
  if(!pendingImport)throw Error('Choose a backup to review first.');
  if(syncConflict)throw Error('Reconcile the changed tab copies before importing a backup.');
  const latest=storedProgress();if(latest&&!sameRecord(latest,browserBase)){receiveExternal(latest);throw Error('Progress changed in another tab. Review the current record before replacing it.');}
  if(Object.values(view).some(v=>v?.running))throw Error('Wait for the Python check to finish before replacing progress.');
  checkProgressImport(pendingImport.state);
  // Persist the current copy first. Storage failure must leave it untouched.
  const previous={date:Date.now(),workspace:QA?'preview':'personal',state:JSON.parse(JSON.stringify(state))};
  try{localStorage.setItem(RECOVERY_KEY,JSON.stringify(previous));}
  catch{throw Error('Could not keep a recovery copy. Export your current progress and free browser storage before importing. Nothing was replaced.');}
  const name=pendingImport.name,pendingCopyKey=pendingImport.pendingCopyKey,next={...fresh(),...pendingImport.state,updatedAt:Date.now()};delete next.workspace;
  try{localStorage.setItem(KEY,JSON.stringify(next));}
  catch{throw Error('Could not save the imported record. Nothing was replaced; export your current progress and free browser storage first.');}
  state=next;browserBase=cloneRecord(next);pendingImport=null;view={};lastSession=null;
  try{localStorage.setItem(PENDING_WRITE_KEY,'null');}catch{}
  if(pendingCopyKey?.startsWith(KEY+'-pending-write-'))try{localStorage.setItem(pendingCopyKey,'null');}catch{}
  try{sessionStorage.setItem(RUNNER_KEY,'null');}catch{}
  try{sessionStorage.setItem(TRAINING_KEY,'null');}catch{}
  saved=QA?'Test records · browser only':'Saved in browser';updateSave();
  if(!QA){clearTimeout(saveTimer);saveTimer=setTimeout(flush,500);}
  importFeedback='Restored '+name+'. Your previous record is available below.';
}
function focusBackupReview(){
  const epoch=renderEpoch;frame(()=>{if(epoch!==renderEpoch)return;const heading=$('#backup-review-title');heading?.focus({preventScroll:true});heading?.scrollIntoView({block:'center'});});
}
function backupReview(){
  if(!pendingImport)return '';
  const current=backupTotals(state),incoming=backupTotals(pendingImport.state);
  return `<section class="backup-review" aria-labelledby="backup-review-title"><div class="eyebrow">Review before restoring</div><h3 id="backup-review-title" tabindex="-1">${esc(pendingImport.name)}</h3><p>${pendingImport.state.workspace?'This is a '+(pendingImport.state.workspace==='preview'?'test preview':'personal')+' backup':'This older backup has no workspace label and may contain test records'}. Replacing uses this file’s complete record, including drafts. Your current copy will be kept for recovery.</p><div class="table-wrap"><table><caption class="sr-only">Compare current progress with the selected backup</caption><thead><tr><th scope="col">Record</th><th scope="col">Current</th><th scope="col">Backup</th></tr></thead><tbody>${[['checks','Lesson checks'],['problems','Interview problems'],['code','Python passes'],['drafts','Saved drafts'],['rounds','Trainer rounds']].map(([key,label])=>`<tr><th scope="row">${label}</th><td>${current[key]}</td><td>${incoming[key]}</td></tr>`).join('')}</tbody></table></div><p class="small muted">Interview passes use the current grading format. Earlier self-assessments and drafts remain in the backup without becoming automatic passes.</p><div class="answer-buttons"><button class="btn dark" type="button" data-action="apply-import">Replace with this backup</button><button class="btn" type="button" data-action="cancel-import">Keep current record</button></div></section>`;
}
function recoveryControl(){
  const recovery=readRecovery();
  return recovery?`<div class="recovery-control"><div><strong>Previous record available</strong><p>Saved before your last replacement on ${esc(new Date(recovery.date).toLocaleString())}. Review it before restoring.</p></div><button class="btn compact" type="button" data-action="review-recovery">Review previous record</button></div>`:'';
}
function saveRunnerResults(){
  try{const records={workspace:QA?'preview':'personal'};for(const [id,v] of Object.entries(view))if(v.checkedCode!==undefined&&(v.running||v.result))records[id]={mode:v.mode,checkedCode:v.checkedCode,checkedCases:v.checkedCases,origin:v.origin,started:v.started,running:!!v.running,result:v.result,unread:!!v.unread};sessionStorage.setItem(RUNNER_KEY,JSON.stringify(records));}catch{}
}
function suspendRunnerChecks(){runnerGeneration++;saveRunnerResults();}
function validRunnerResult(result){
  if(!result||typeof result!=='object'||Array.isArray(result))return false;
  if(typeof result.error==='string'&&result.error)return true;
  return Number.isInteger(result.total)&&result.total>0&&Number.isInteger(result.passed)&&result.passed>=0&&result.passed<=result.total&&Number.isFinite(result.elapsedMs)&&result.elapsedMs>=0&&Array.isArray(result.results)&&result.results.length===result.total&&result.results.every(r=>r&&(typeof r.passed==='boolean'||result.mode==='debug'&&r.passed===null))&&result.results.filter(r=>r.passed===true).length===result.passed;
}
function restoreRunnerResults(){
  try{const records=JSON.parse(sessionStorage.getItem(RUNNER_KEY));if(!records||typeof records!=='object'||Array.isArray(records))return;
    if(records.workspace!==undefined&&records.workspace!==(QA?'preview':'personal'))return;
    for(const c of coding){const v=records[c.id];if(!v||!['run','submit','debug'].includes(v.mode)||typeof v.checkedCode!=='string'||v.checkedCode.length>30000)continue;
      const result=v.running?{error:'This check was interrupted. Your draft is saved; run or submit again.'}:v.result;
      if(!validRunnerResult(result))continue;
      view[c.id]={...v,running:false,result,origin:typeof v.origin==='string'&&v.origin.startsWith('#coding/'+c.id)?v.origin:'#coding/'+c.id,unread:!!v.unread||!!v.running};
    }
  }catch{}
}
function runnerNotice(){
  const jobs=coding.filter(c=>!(route?.[0]==='coding'&&route[1]===c.id)&&(view[c.id]?.running||view[c.id]?.unread));
  return jobs.length?`<aside class="runner-notice" aria-label="Python checks">${jobs.map(c=>{const v=view[c.id];return `<div><span>${v.running?'Python check running':'Python check finished'} · ${esc(c.title)}</span><a href="${esc(v.origin||'#coding/'+c.id)}">${v.running?'Return to check':'View result'} ↗</a></div>`;}).join('')}</aside>`:'';
}
function updateRunnerNotice(){const notice=$('#runner-notice');if(notice)notice.innerHTML=runnerNotice();}
function runnerDraftNote(c){
  const v=view[c.id];if(!v)return '';
  const codeChanged=v.checkedCode!==undefined&&(state.drafts[c.id]??c.starter)!==v.checkedCode;
  const casesChanged=v.mode==='debug'&&Array.isArray(v.checkedCases)&&!sameRecord(v.checkedCases,debugCases(c).cases.filter(t=>t.enabled).map(t=>({argumentsJSON:t.argumentsJSON,expectedJSON:t.expectedJSON})));
  return (codeChanged?'<p class="runner-draft-note">Your draft changed after this check began. These results refer to the checked version below.</p>':'')+(casesChanged?'<p class="runner-draft-note">Your debugging cases changed after this check began. Results show the cases sent for that run; run tests again to check your edits.</p>':'');
}
function updateRunnerDraftNote(id){const c=coding.find(c=>c.id===id),note=$('#runner-draft-note');if(c&&note&&route[0]==='coding'&&route[1]===id)note.innerHTML=runnerDraftNote(c);}
async function executeCode(c,mode,code,cases){
  const v=view[c.id]||={};if(v.running)return;
  const generation=runnerGeneration;
  const assisted=!!state.coding[c.id]?.assisted;
  state.drafts[c.id]=code;touch();Object.assign(v,{running:true,mode,result:null,checkedCode:code,checkedCases:mode==='debug'?cases:undefined,origin:location.hash||'#coding/'+c.id,started:Date.now(),unread:false,returnFocus:pageFocus()});saveRunnerResults();render();announce(mode==='debug'?'Running your debugging cases.':mode==='run'?'Running the visible example.':'Checking the complete suite.');
  let deadline,controller=typeof AbortController!=='undefined'?new AbortController():null;
  try{
    const request=(async()=>{const response=await fetch('/api/judge',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:c.id,code,mode,...(mode==='debug'?{cases}:{})}),...(controller?{signal:controller.signal}:{})});const result=await response.json();if(!response.ok)throw Error(result.error||'The local runner could not complete this request.');return result;})();
    const timeout=new Promise((resolve,reject)=>{deadline=setTimeout(()=>{controller?.abort();reject(Error('The local runner did not respond in time. Your draft is saved; try the check again.'));},7000);});
    const result=await Promise.race([request,timeout]);if(generation!==runnerGeneration)return;if(!validRunnerResult(result))throw Error('The local runner returned an incomplete result. Your draft is saved; try again.');v.result=result;
    if(mode==='submit'&&!result.error&&Number.isInteger(result.total)&&result.total>0&&result.passed===result.total){state.coding[c.id]={...state.coding[c.id],accepted:true,acceptedAssisted:assisted,date:Date.now()};touch();}
  }catch(error){if(generation===runnerGeneration)v.result={error:/load failed|failed to fetch|networkerror|network request failed|aborterror/i.test(error.message||error.name||'')?'This check was interrupted or the local server is unavailable. Your draft is saved; restart the server if needed, then run or submit again.':error.message||'Local Python server is unavailable. Restart it and try again.'};}
  finally{
    clearTimeout(deadline);if(generation!==runnerGeneration)return;v.running=false;const current=route[0]==='coding'&&route[1]===c.id;v.unread=!current;saveRunnerResults();
    if(current){const returnFocus=pageFocus()?null:v.returnFocus;render();const epoch=renderEpoch;frame(()=>{if(epoch===renderEpoch)restoreFocus(returnFocus);});announce(v.result.error||`${v.result.passed} of ${v.result.total-(v.result.results?.filter(r=>r.passed===null).length||0)} checked tests passed. ${mode==='debug'?'Debugging only; completion unchanged.':mode==='run'?'Visible example only.':'Complete suite.'}`);}
    else{updateRunnerNotice();announce('Python check finished for '+c.title+'. The result is available in the Python check notice.');}
  }
}
function sidebar(){return `<aside class="sidebar" id="navigation-panel"><a class="brand" href="#dashboard"><svg viewBox="0 0 30 30" fill="none" aria-hidden="true"><path d="M5 3 26 15 5 27V3Z" stroke="currentColor" stroke-width="3"/><path d="m12 10 8 5-8 5z" fill="currentColor"/></svg>Quant Atelier</a><nav aria-label="Main navigation">${[['dashboard','Overview',''],['paths','Learning roadmap',''],['questions','Interview questions',content.questions.length],['courses','Courses',content.lessons.length],['coding','Python workspace',coding.length],['trainers','Trainers','5'],['review','Revision queue',''],['progress','Progress & data','']].map(([key,name,total])=>`<a class="nav-link ${(route[0]==='question-list'?'questions':route[0]==='coding-list'?'coding':route[0])===key?'active':''}" href="#${key}" ${(route[0]==='question-list'?'questions':route[0]==='coding-list'?'coding':route[0])===key?'aria-current="page"':''}>${icon(key)}<span>${name}</span><span class="nav-index">${total}</span></a>`).join('')}</nav></aside>`;}
function panelControl(name,label,target){
  const action=(panels[name]?'Collapse':'Expand')+' '+label;
  const side=name==='navigation'?'left':'right';
  return `<button class="panel-handle panel-handle-${name}" type="button" data-panel="${name}" aria-controls="${target}" aria-expanded="${panels[name]}" aria-label="${action}" data-tooltip="${action}">${icon('panel-'+side+'-'+(panels[name]?'close':'open'))}<span class="panel-handle-label" aria-hidden="true">${label}</span></button>`;
}
function syncPanels(){
  $('.shell').classList.toggle('navigation-collapsed',!panels.navigation);
  const navigation=$('#navigation-panel');
  navigation.inert=!panels.navigation;
  navigation.setAttribute('aria-hidden',String(!panels.navigation));
  const practice=$('#practice-panel');
  if(practice){
    practice.inert=!panels.practice;
    practice.setAttribute('aria-hidden',String(!panels.practice));
    $('.lesson-layout').classList.toggle('practice-collapsed',!panels.practice);
  }
  document.querySelectorAll('[data-panel]').forEach(button=>{
    const name=button.dataset.panel,side=name==='navigation'?'left':'right';
    const action=button.closest('.mobile-panel-tools')?(name==='navigation'?'Navigation':'Practice'):(panels[name]?'Collapse':'Expand')+' '+(name==='navigation'?'navigation':'practice');
    button.setAttribute('aria-expanded',String(panels[name]));
    button.setAttribute('aria-label',action);
    button.dataset.tooltip=action;
    button.querySelector('use').setAttribute('href','/vendor/lucide/icons.svg?v=panel-motion-20261003#panel-'+side+'-'+(panels[name]?'close':'open'));
  });
}
function bindPanels(){
  syncPanels();
  document.querySelectorAll('[data-panel]').forEach(button=>button.addEventListener('click',()=>{
    const name=button.dataset.panel;
    const compact=window.matchMedia?.('(max-width:800px)').matches;
    if(name==='navigation'&&compact&&panels.navigation&&$('#navigation-panel').getBoundingClientRect().bottom<=0){
      navigationReturn={hash:location.hash,y:window.scrollY};$('#navigation-panel').scrollIntoView({block:'start'});keepNavigationVisible();return;
    }
    const previousY=window.scrollY;
    panels[name]=!panels[name];
    try{localStorage.setItem(LAYOUT_KEY,JSON.stringify(panels));}catch{}
    // Resize in place: keep quiz selections, drafts, editor history and focus.
    syncPanels();
    if(name==='navigation'&&panels.navigation)keepNavigationVisible();
    if(name==='navigation'&&compact){
      if(panels.navigation){navigationReturn={hash:location.hash,y:previousY};$('#navigation-panel').scrollIntoView({block:'start'});}
      else {if(navigationReturn?.hash===location.hash){const y=navigationReturn.y,hash=location.hash;frame(()=>{if(location.hash===hash)window.scrollTo(0,y);});}navigationReturn=null;}
    }
  }));
}
function keepNavigationVisible(){
  const nav=$('.sidebar nav'),active=nav.querySelector('[aria-current="page"]');
  if(active&&nav.scrollWidth>nav.clientWidth){
    const linkBox=active.getBoundingClientRect(),navBox=nav.getBoundingClientRect();
    nav.scrollLeft+=linkBox.left-navBox.left-(nav.clientWidth-linkBox.width)/2;
  }
}
function header(eyebrow,title,description,actions=''){return `<div class="page-head"><div><h1>${title}</h1>${description?`<p>${description}</p>`:''}</div>${actions?`<div class="head-actions">${actions}</div>`:''}</div>`;}
function previewNotice(){
  if(!QA)return '';
  const personal='/'+(location.hash||'#dashboard');
  return `<aside class="preview-notice" aria-label="Development test preview"><span class="preview-tag mono">Test preview</span><p>These are development test records, separate from your personal progress.</p><a href="${esc(personal)}">Open personal workspace ↗</a></aside>`;
}
function render(){
  const hash=location.hash||'#dashboard',ui=renderedHash===hash?capturePageUI():null,epoch=++renderEpoch;
  releaseReadingOutline?.();releaseReadingOutline=null;
  releaseModuleOutline?.();releaseModuleOutline=null;
  codeEditor?.destroy();codeEditor=null;
  route=(location.hash.slice(1)||'dashboard').split('/');
  if(route[0]==='paths'&&['researcher','trader'].includes(route[1])&&preferredPath()!==route[1]){
    state.preferences={...state.preferences,path:route[1]};touch();
  }
  if(training && (route[0]!=='trainers'||route[1]!==training.type||route[2]==='round'))endTraining(false,false,'left');
  if(route[0]==='coding'&&view[route[1]]?.unread){view[route[1]].unread=false;saveRunnerResults();}
  const module=moduleContext();
  let body=({dashboard:dashboard,paths:paths,questions:questions,'question-list':()=>topicPracticePage('questions'),'coding-list':()=>topicPracticePage('coding'),courses:courses,coding:codePage,trainers:trainers,review:review,progress:progress}[route[0]]||dashboard)();
  if(module)body=moduleTrail(module)+moduleSupplementNotice(module)+moduleLinks(body,module)+(route[0]==='courses'?'':moduleContinuation(module));
  const panelButtons=panelControl('navigation','Navigation','navigation-panel')+(body.includes('id="practice-panel"')?panelControl('practice','Practice','practice-panel'):'');
  $('#app').innerHTML=`<a class="skip-link" href="#page">Skip to practice</a><div class="shell">${sidebar()}<div class="panel-handles" role="group" aria-label="Workspace panels">${panelButtons}</div><main class="main" aria-label="Practice workspace"><div class="topbar"><div class="mobile-panel-tools" role="group" aria-label="Workspace panels">${panelButtons}</div>${saveStatus()}</div>${previewNotice()}<div id="sync-notice">${syncNotice()}</div><div id="runner-notice">${runnerNotice()}</div><div id="page"${module?' class="in-module"':''}>${body}</div></main></div>`;
  typesetMath($('#page'));
  bindPage();
  bindPanels();
  bindModuleTrail();
  bindReadingOutline();
  // Keep the current destination visible in the horizontally scrolling phone menu.
  keepNavigationVisible();
  renderedHash=hash;
  if(ui)restorePageUI(ui,epoch);
}
function locateRoadmapStep(){
  if(route[0]!=='paths'||!/^step-l\d{2}$/.test(route[2]||''))return;
  const step=document.getElementById(route[2]);
  if(step){step.open=true;step.scrollIntoView({block:'start'});step.querySelector('summary').focus({preventScroll:true});}
}
function statGrid(){const c=counts();return `<div class="stat-grid"><div class="stat"><span class="num">${c.solved}<span class="small muted"> / ${content.questions.length}</span></span><span class="muted">UNAIDED INTERVIEW PASSES</span></div><div class="stat"><span class="num">${c.lessons}<span class="small muted"> / ${content.lessons.length}</span></span><span class="muted">LESSON CHECKS PASSED</span></div><div class="stat"><span class="num">${c.coding}<span class="small muted"> / ${coding.length}</span></span><span class="muted">PYTHON EXERCISES PASSED</span></div><div class="stat"><span class="num">${dueQuestions().length}</span><span class="muted">PROBLEMS DUE FOR REVISION</span></div></div>`;}
function activityLabel(kind){return {courses:'Read lesson & take check',questions:'Continue practice','question-list':'Choose an interview question',coding:'Continue coding','coding-list':'Choose a coding exercise',trainers:'Start a round'}[kind];}
function activityMeta(activity,lesson){
  if(activity.kind==='question-list'||activity.kind==='coding-list')return `${activity.stage} · ${activity.status}`;
  const question=content.questions.find(q=>activity.kind==='questions'&&q.id===activity.id);
  const code=coding.find(c=>activity.kind==='coding'&&c.id===activity.id);
  return [activity.stage,question?question.difficulty:code?code.difficulty:'',activity.kind==='courses'?lesson.minutes+' min':question?question.minutes+' min':code?'Python 3':'Optional drill'].filter(Boolean).join(' · ');
}
// Resume core work in curriculum order. Fluency rounds remain optional and repeatable.
function nextRouteActivity(path=preferredPath()){
  for(const lesson of journeyLessons(path)){
    const activity=moduleSteps(lesson,path).find(a=>a.kind!=='trainers'&&!a.done);
    if(activity)return {lesson,activity};
  }
  return null;
}
function dashboard(){
  const path=preferredPath(),resume=nextRouteActivity(path),due=dueQuestions(),unchecked=nextLesson(path);
  const lesson=resume?.lesson,activity=resume?.activity;
  const stages={Understand:'Read the lesson and take its understanding check. Then carry the idea into problems and code in this same module.',Apply:'Put the idea to work in the remaining interview problems. A reviewed solution stays available for another attempt; it does not count as a solve.',Implement:'Turn the reasoning into working Python. Submit against the full test suite to complete the implementation step.'};
  const remaining=lesson?moduleSteps(lesson,path).filter(a=>a.kind!=='trainers'&&!a.done).slice(0,3):[];
  const hardTarget=content.questions.find(q=>(q.path==='shared'||q.path===path)&&q.difficulty==='Hard');
  const reviewTarget=due[0]||hardTarget;
  const session=remaining.length?remaining.map((a,i)=>`<a class="row" href="${a.href}"><span class="row-num">${String(i+1).padStart(2,'0')}</span><div><span class="row-title">${esc(a.title)}</span><div class="row-meta">${esc(activityMeta(a,lesson))}</div></div><span class="row-arrow" aria-hidden="true">↗</span></a>`).join(''):
    `<a class="row" href="${due.length?revisionHref(reviewTarget):'#questions/'+reviewTarget.id}"><span class="row-num">01</span><div><span class="row-title">${due.length?'Revise':'Revisit'}: ${esc(reviewTarget.title)}</span><div class="row-meta">${due.length?'DUE FOR REVISION':'REVIEW A HARD PROBLEM'} · ${reviewTarget.minutes} MIN</div></div><span class="row-arrow" aria-hidden="true">↗</span></a><a class="row" href="#trainers/math"><span class="row-num">02</span><div><span class="row-title">Keep your arithmetic fluent</span><div class="row-meta">OPTIONAL · CHOOSE A SHORT ROUND</div></div><span class="row-arrow" aria-hidden="true">↗</span></a>`;
  return header('Your daily practice','Overview','')+`<section class="hero"><div class="hero-copy"><div class="eyebrow">${lesson?`${pathName(lesson.path)} / ${activity.stage}`:`${pathName(path)} / Core route complete`}</div><h2>${lesson?esc(lesson.title):'Your core route is complete.'}</h2><p>${lesson?stages[activity.stage]:'Every linked lesson check, interview problem and Python exercise has a recorded result. Keep revising and practising; these records do not certify interview readiness.'}</p><div class="hero-actions"><a class="btn dark" href="${activity?.href||'#paths/'+path}">${activity?activityLabel(activity.kind):'Review your roadmap'} <span aria-hidden="true">↗</span></a>${lesson?`<a class="hero-roadmap" href="#paths/${path}/step-${lesson.id}">See this module on your roadmap ↗</a>`:''}</div></div><div class="hero-art">${artwork(0)}</div></section>${statGrid()}<div class="split"><section><div class="section-title"><h2>${resume?'Your next activities':'Keep the reasoning fresh'}</h2><span class="mono">${lesson?'MODULE '+moduleNumber(lesson,path):pathName(path).toUpperCase()}</span></div><div class="panel">${session}</div><div class="session-options">${unchecked&&unchecked.id!==lesson?.id?`<a href="${moduleHref('courses',unchecked.id,unchecked,path)}">Next unchecked lesson: ${esc(unchecked.title)} ↗</a>`:''}<a href="#trainers">Choose a fluency drill ↗</a>${due.length?`<a href="#review">${due.length} problem${due.length===1?'':'s'} due for revision ↗</a>`:''}</div></section><section><div class="section-title"><h2>The difficult part</h2><a class="btn link" href="#questions/${hardTarget.id}">Try a hard problem ↗</a></div><div class="note"><strong>Explain why the shortcut fails.</strong><p>Hard questions add dependence, selection, overlapping labels, or a changed information set. A correct number is the start; the follow-up tests whether the reasoning survives.</p></div></section></div>`;
}
// A route suggests sequence, while evidence retains its original grading type.
function preferredPath(){return ['researcher','trader'].includes(state.preferences?.path)?state.preferences.path:'researcher';}
function selectedPath(){return route?.[0]==='paths'&&['researcher','trader'].includes(route[1])?route[1]:preferredPath();}
function journeyLessons(path=preferredPath()){return content.lessons.filter(l=>l.path==='shared'||l.path===path);}
function nextLesson(path=preferredPath()){return journeyLessons(path).find(l=>!state.lessons[l.id]?.passed)||null;}
function lessonEvidence(l){
  const qs=l.questions.map(questionState),cs=l.coding.map(id=>state.coding[id]||{});
  return {
    checked:!!state.lessons[l.id]?.passed,
    numeric:qs.filter(s=>s.solved).length,
    self:qs.filter(s=>!s.solved&&s.selfSolved).length,
    reviewed:qs.filter(s=>!s.solved&&!s.selfSolved&&s.reviewed).length,
    questionTotal:qs.length,
    accepted:cs.filter(s=>s.accepted).length,
    assisted:cs.filter(s=>s.accepted&&acceptedWithEditorial(s)).length,
    codingTotal:cs.length,
    sessions:state.trainers.filter(s=>s.finished&&s.attempts>0&&(l.trainers||[]).includes(s.type)).length
  };
}
function routeEvidence(lessons){
  // A linked exercise can appear in several lessons; count it once on the route.
  const questions=[...new Set(lessons.flatMap(l=>l.questions))],codes=[...new Set(lessons.flatMap(l=>l.coding))];
  return {checked:lessons.filter(l=>state.lessons[l.id]?.passed).length,total:lessons.length,
    solved:questions.filter(id=>questionState(id).solved||questionState(id).selfSolved).length,
    self:questions.filter(id=>!questionState(id).solved&&questionState(id).selfSolved).length,
    questionTotal:questions.length,accepted:codes.filter(id=>state.coding[id]?.accepted).length,
    codingTotal:codes.length};
}
const roadmapPhases={
  shared:[['Probability & reasoning','Rebuild the tools you will use in every interview.',['l01','l02','l03','l04','l05']],
    ['Quant fluency','Make arithmetic, dependence and temporal code reliable.',['l06','l07','l08']]],
  researcher:[['Calculus & optimization','Understand local change, then choose and verify an update.',['l26','l27']],['Statistical models','Estimate, fit and quantify what the data can tell you.',['l09','l25','l10','l11','l29','l12','l13','l28']],
    ['The research process','Separate discovery from evidence you can defend.',['l14','l15','l16']],
    ['Simulation & algorithms','Turn a mathematical argument into a tested implementation.',['l17','l18']]],
  trader:[['Value & information','Price the payoff, then learn from the order.',['l19','l20']],
    ['Decisions & risk','Compare alternatives and understand joint exposure.',['l21','l22']],
    ['Payoffs & judgement','Reason from replication, selection and calibrated beliefs.',['l23','l24']]]
};
// The bookmark carries the originating module, including exercises shared by lessons.
function moduleNumber(l,path=preferredPath()){return String(journeyLessons(l.path==='shared'?path:l.path).findIndex(item=>item.id===l.id)+1).padStart(2,'0');}
function moduleHref(kind,id,l,path){return `#${kind}/${id}/journey/${path}/${l.id}`;}
function moduleActivities(l,path){
  const make=(kind,id,title,stage,done,status)=>({kind,id,title,stage,done,status,href:moduleHref(kind,id,l,path)});
  return [make('courses',l.id,l.title,'Understand',!!state.lessons[l.id]?.passed,state.lessons[l.id]?.passed?'Check passed':'Check to do'),
    ...l.questions.map(id=>{const q=content.questions.find(q=>q.id===id),s=questionState(id);return make('questions',id,q.title,'Apply',!!(s.solved||s.selfSolved),({solved:'Unaided solve','self-solved':'Self-assessed',reviewed:'Reviewed',practising:'In practice',new:q.difficulty}[questionStatus(id)]));}),
    ...l.coding.map(id=>{const c=coding.find(c=>c.id===id),s=state.coding[id]||{};return make('coding',id,c.title,'Implement',!!s.accepted,s.accepted?(acceptedWithEditorial(s)?'Passed with editorial':'Tests passed'):c.difficulty);}),
    ...(l.trainers||[]).map(id=>{const t=trainerTypes.find(t=>t.id===id),finished=state.trainers.some(s=>s.type===id&&s.finished&&s.attempts>0);return make('trainers',id,t.name,'Fluency',finished,finished?'Round finished':'Start a round');})];
}
function moduleLegacyActivities(l,path){
  return (l.legacyCoding||[]).map(id=>({kind:'coding',id,href:moduleHref('coding',id,l,path)}));
}
function moduleSupplementNotice(context){
  return context.additional?'<p class="small muted">Additional practice · completion is tracked separately from this topic’s three exercises.</p>':'';
}
// The journey has three core destinations. Problems inside a list are choices,
// not a sequence whose next item is chosen for the learner.
function moduleSteps(l,path){
  const activities=moduleActivities(l,path),e=lessonEvidence(l);
  const list=(kind,title,stage,done,total)=>({kind,id:l.id,title,stage,done:total>0&&done===total,status:done+'/'+total+(kind==='question-list'?' passed':' passed'),href:moduleHref(kind,l.id,l,path)});
  return [activities[0],
    ...(l.questions.length?[list('question-list','Interview questions','Apply',e.numeric+e.self,e.questionTotal)]:[]),
    ...(l.coding.length?[list('coding-list','Coding exercises','Implement',e.accepted,e.codingTotal)]:[]),
    ...activities.filter(a=>a.kind==='trainers')];
}
function moduleStageEvidence(l,stage){
  const e=lessonEvidence(l);
  return stage==='Apply'?(e.numeric+e.self)+'/'+e.questionTotal:stage==='Implement'?e.accepted+'/'+e.codingTotal:null;
}
function practiceBreadcrumb(kind,topic){
  const context=moduleContext();
  const href=context?moduleHref(kind==='questions'?'question-list':'coding-list',context.lesson.id,context.lesson,context.path):'#'+kind;
  const label=context?(kind==='questions'?'Question list':'Coding list'):(kind==='questions'?'Interview questions':'Python workspace');
  return `<div class="breadcrumbs"><a href="${href}">← ${label}</a><span>/</span><span>${esc(topic)}</span></div>`;
}
function topicQuestionPresentation(q){
  const record=state.questions[q.id]||{},s=questionState(q.id);
  if(s.solved)return {state:'solved',label:'Unaided solve',note:''};
  if(record.selfSolved===true)return {state:'historical',label:'Previously self-assessed',note:'Retake the automatic check'};
  if(record.solved===true&&q.type==='structured')return {state:'historical',label:'Previous check passed',note:'Retake the current check'};
  if(s.reviewed)return {state:'reviewed',label:'Reviewed',note:'Try again unaided'};
  if(s.attempts)return {state:'practising',label:'In progress',note:''};
  return {state:'new',label:'Not started',note:''};
}
function topicPracticePage(kind){
  const l=content.lessons.find(l=>l.id===route[1]);
  if(!l)return header('','Topic not found','')+'<a class="btn link" href="#courses">Browse courses →</a>';
  const context=moduleContext(),path=context?.path||(l.path==='shared'?preferredPath():l.path),e=lessonEvidence(l);
  const isQuestions=kind==='questions',items=(isQuestions?l.questions:l.coding).map(id=>(isQuestions?content.questions:coding).find(item=>item.id===id));
  const difficulty=['Easy','Medium','Hard'];
  const complete=item=>isQuestions?!!(questionState(item.id).solved||questionState(item.id).selfSolved):!!state.coding[item.id]?.accepted;
  const status=item=>{if(isQuestions){const view=topicQuestionPresentation(item);return `<span class="topic-row-state"><span class="topic-status-badge">${esc(view.label)}</span>${view.note?`<span class="topic-status-note">${esc(view.note)}</span>`:''}</span>`;}return `<span class="status ${complete(item)?'solved':''}">${complete(item)?`✓ Passed${acceptedWithEditorial(state.coding[item.id])?' · with editorial':''}`:codingStatus(item)==='reviewed'?'↗ Editorial read':codingStatus(item)==='practising'?'Draft in progress':'—'}</span>`;};
  const totalDone=items.filter(complete).length;
  return header('',isQuestions?'Interview questions':'Coding exercises',esc(l.title))+`<div class="topic-list-summary"><span>${totalDone} / ${items.length} passed</span>${isQuestions&&e.self?`<span class="muted">${e.self} self-assessed</span>`:''}<a href="${moduleHref('courses',l.id,l,path)}">Revisit lesson ↗</a></div><div class="topic-practice-list">${difficulty.map(level=>{
    const group=items.filter(item=>item.difficulty===level),done=group.filter(complete).length;
    return `<section class="topic-level" aria-labelledby="topic-${level.toLowerCase()}"><div class="topic-level-heading"><h2 id="topic-${level.toLowerCase()}">${level}</h2><span class="small muted">${done} / ${group.length} ${isQuestions?'complete':'passed'}</span></div><div class="topic-level-rows">${group.map(item=>`<a class="topic-practice-row"${isQuestions?` data-question-state="${topicQuestionPresentation(item).state}"`:''} href="${moduleHref(kind,item.id,l,path)}">${isQuestions?`<span class="topic-row-marker" aria-hidden="true">${topicQuestionPresentation(item).state==='solved'?'✓':''}</span>`:''}<div><span class="row-title">${esc(item.title)}</span>${isQuestions?`<span class="row-meta">${item.minutes} min · ${item.type==='structured'?'Multi-part automatic check':'Numeric answer & reasoning'}</span>`:''}</div>${status(item)}<span class="row-arrow" aria-hidden="true">↗</span></a>`).join('')||'<p class="small muted topic-list-empty">Practice for this difficulty is being prepared.</p>'}</div></section>`;
  }).join('')}</div>`;
}
function lessonPractice(l){
  const e=lessonEvidence(l);
  return `<aside class="study-aside" id="practice-panel" aria-label="Related practice"><div class="panel panel-pad"><h3>Put it into practice</h3>${l.questions.length?`<a href="#question-list/${l.id}">Interview question list <span class="accent">↗</span><div class="row-meta">${e.numeric+e.self} / ${e.questionTotal} passed</div></a>`:''}${l.coding.length?`<a href="#coding-list/${l.id}">Coding exercise list <span class="accent">↗</span><div class="row-meta">${e.accepted} / ${e.codingTotal} passed</div></a>`:''}${(l.trainers||[]).length?`<div class="divider"></div><div class="eyebrow">Fluency drills</div>${l.trainers.map(id=>`<a href="#trainers/${id}">${esc(trainerTypes.find(t=>t.id===id).name)} ↗</a>`).join('')}`:''}<div class="divider"></div><a href="#paths/${l.path==='shared'?preferredPath():l.path}/step-${l.id}">View your learning roadmap ↗</a></div></aside>`;
}
function moduleContext(){
  if(!content||!coding||!route)return null;
  if(route[2]==='journey'&&['researcher','trader'].includes(route[3])){
    const l=content.lessons.find(l=>l.id===route[4]&&(l.path==='shared'||l.path===route[3]));
    if(l){
      const matches=a=>a.kind===route[0]&&a.id===route[1];
      if([...moduleSteps(l,route[3]),...moduleActivities(l,route[3])].some(matches))return {lesson:l,path:route[3]};
      if(moduleLegacyActivities(l,route[3]).some(matches))return {lesson:l,path:route[3],additional:true};
    }
  }
  if(route[0]==='courses'||(['question-list','coding-list'].includes(route[0])&&route[2]!=='journey')){
    const l=content.lessons.find(l=>l.id===route[1]);
    if(l)return {lesson:l,path:l.path==='shared'?preferredPath():l.path};
  }
  return null;
}
function moduleLinks(html,context){
  const activities=[...moduleSteps(context.lesson,context.path),...moduleActivities(context.lesson,context.path),...moduleLegacyActivities(context.lesson,context.path)];
  return html.replace(/href="#(courses|questions|coding|question-list|coding-list|trainers)\/([^"/]+)"/g,(match,kind,id)=>activities.some(a=>a.kind===kind&&a.id===id)?`href="${moduleHref(kind,id,context.lesson,context.path)}"`:match);
}
function followingActivity(context){
  const l=context.lesson,steps=moduleSteps(l,context.path),kind=context.kind||route[0];
  const questions=steps.find(a=>a.kind==='question-list'),codes=steps.find(a=>a.kind==='coding-list');
  let next=kind==='courses'?(questions||codes):kind==='questions'?questions:kind==='question-list'?codes:kind==='coding'?codes:null;
  if(kind==='trainers'){
    const drills=steps.filter(a=>a.kind==='trainers'),index=drills.findIndex(a=>a.id===(context.id||route[1]));next=drills[index+1];
  }
  if(next)return {...next,nextModule:false,returnToList:kind==='questions'||kind==='coding'};
  const lessons=journeyLessons(context.path),nextLesson=lessons[lessons.findIndex(item=>item.id===l.id)+1];
  return nextLesson?{title:nextLesson.title,stage:'Next module',kind:'courses',href:moduleHref('courses',nextLesson.id,nextLesson,context.path),nextModule:true}:null;
}
function moduleTrail(context){
  const l=context.lesson,activities=moduleSteps(l,context.path),current=activities.find(a=>a.kind===route[0]&&a.id===route[1])||activities.find(a=>a.kind===(route[0]==='questions'?'question-list':route[0]==='coding'?'coding-list':'')),next=followingActivity(context);
  const stages=[...new Set(activities.map(a=>a.stage))];
  return `<section class="module-trail" aria-label="Current learning module"><div class="module-heading"><a class="module-location" href="#paths/${context.path}/step-${l.id}">← Roadmap <span>· ${moduleNumber(l,context.path)} / ${pathName(context.path)}</span></a><strong title="${esc(l.title)}">${esc(l.title)}</strong></div><nav class="module-stages" aria-label="Module stages">${stages.map(stage=>{const group=activities.filter(a=>a.stage===stage),target=current?.stage===stage?current:group.find(a=>!a.done)||group[0],done=group.filter(a=>a.done).length;return `<a href="${target.href}" class="module-stage ${current?.stage===stage?'current':''} ${done===group.length?'done':''}" ${current?.stage===stage?'aria-current="step"':''}><span>${stage}</span><span class="stage-evidence">${stage==='Understand'?(done?'✓':'○'):moduleStageEvidence(l,stage)??done+'/'+group.length}</span></a>`;}).join('')}</nav><div class="module-tools">${route[0]==='courses'?lessonOutline(l):''}${next?`<a class="module-forward" href="${next.href}" aria-label="${next.returnToList?'Back to list':next.nextModule?'Next module':'Next step'}: ${esc(next.title)}" title="${esc(next.title)}">${next.returnToList?'Back to list':next.nextModule?'Next module':'Next step'} <span aria-hidden="true">→</span></a>`:''}<details class="module-outline" id="module-outline"><summary aria-label="Show all module activities" title="All module activities">${icon('paths')}<span class="module-outline-label" aria-hidden="true">Steps</span></summary><nav class="module-menu" aria-label="All module activities"><div class="eyebrow">This module</div>${activities.map(a=>`<a href="${a.href}" class="${a===current?'current':''}" ${a===current?'aria-current="page"':''}><span class="activity-marker">${a.done?'✓':'○'}</span><span><span class="activity-title">${esc(a.title)}</span><span class="activity-meta">${a.stage} · ${a.status}</span></span></a>`).join('')}</nav></details></div></section>`;
}
function moduleContinuation(context){
  const l=context.lesson,next=followingActivity(context),e=lessonEvidence(l);
  const href=next?.href||'#paths/'+context.path+'/step-'+l.id;
  const label=next?.returnToList?(next.kind==='question-list'?'Back to question list':'Back to coding list'):next?.kind==='question-list'?'Choose an interview question':next?.kind==='coding-list'?'Choose a coding exercise':next?.kind==='trainers'?'Open drill':next?.kind==='courses'?'Next lesson':'View roadmap';
  const extra=next?.returnToList&&next.kind==='question-list'&&l.coding.length?`<a class="module-return" href="${moduleHref('coding-list',l.id,l,context.path)}">Continue to coding list →</a>`:'';
  return `<nav class="module-continuation" aria-label="Continue learning module"><div><div class="eyebrow">${next?(next.returnToList?'Choose your next practice':next.nextModule?'Next module · available anytime':'Continue this module'):'End of this route'}</div><h3>${next?esc(next.title):'Return to your roadmap'}</h3><p>${e.checked?'Check passed':'Check to do'}${e.questionTotal?' · '+(e.numeric+e.self)+'/'+e.questionTotal+' problems passed':''}${e.codingTotal?' · '+e.accepted+'/'+e.codingTotal+' code passed':''}</p></div><div class="continuation-actions"><a class="btn dark" href="${href}">${label} →</a>${extra}<a class="module-return" href="#paths/${context.path}/step-${l.id}">Back to this roadmap module</a></div></nav>`;
}
function bindOutlineKeys(outline,selector){
  outline.addEventListener('keydown',event=>{
    if(!['ArrowDown','ArrowUp','Home','End'].includes(event.key))return;
    const summary=outline.querySelector('summary'),items=Array.from(outline.querySelectorAll(selector));
    if(!items.length)return;
    const index=items.indexOf(event.target);
    if(event.target!==summary&&index<0)return;
    event.preventDefault();outline.open=true;
    const target=event.key==='Home'?0:event.key==='End'?items.length-1:index<0?(event.key==='ArrowUp'?items.length-1:0):Math.max(0,Math.min(items.length-1,index+(event.key==='ArrowUp'?-1:1)));
    items[target].focus();
  });
}
function fitOutlineMenu(outline){
  if(!outline.open)return;
  const menu=outline.querySelector('.module-menu');
  if(!menu?.style||!menu.getBoundingClientRect||!Number.isFinite(window.innerHeight))return;
  const available=window.innerHeight-menu.getBoundingClientRect().top-14;
  const limit=window.getComputedStyle?.(menu).position==='fixed'?window.innerHeight:window.innerHeight*.6;
  menu.style.maxHeight=Math.max(0,Math.min(available,limit))+'px';
}
function alignOutlineMenu(outline){
  fitOutlineMenu(outline);
  const menu=outline.querySelector('.module-menu');
  const current=menu.contains?.(document.activeElement)?document.activeElement:menu.querySelector('[aria-current]');
  if(current)menu.scrollTop=Math.max(0,current.offsetTop-(menu.clientHeight-current.offsetHeight)/2);
}
function bindModuleTrail(){
  const outline=$('#module-outline');
  if(!outline)return;
  bindOutlineKeys(outline,'.module-menu a');
  outline.addEventListener('toggle',()=>{if(outline.open)alignOutlineMenu(outline);});
  outline.addEventListener('keydown',event=>{if(event.key==='Escape'){outline.open=false;outline.querySelector('summary').focus();event.stopPropagation();}});
  $('#page').addEventListener('click',event=>{if(outline.open&&!outline.contains(event.target))outline.open=false;});
  const fit=()=>fitOutlineMenu(outline);
  window.addEventListener?.('resize',fit);window.addEventListener?.('scroll',fit,{passive:true});
  releaseModuleOutline=()=>{window.removeEventListener?.('resize',fit);window.removeEventListener?.('scroll',fit);};
}
function authoredLesson(l){
  if(l.id==='l01'&&typeof QuantSampleSpaceLesson!=='undefined')return QuantSampleSpaceLesson;
  return typeof QuantCourseLessons!=='undefined'?QuantCourseLessons.get(l.id):undefined;
}
function lessonSections(l){
  const authored=authoredLesson(l),sections=authored?.sections?authored.sections.map(([title])=>({title})):l.sections;
  return [...sections.map((s,i)=>({id:'lesson-section-'+i,title:s.title})),{id:'lesson-example',title:'A concrete example'},{id:'lesson-check',title:'Understanding check'}];
}
function lessonOutline(l){
  return `<details class="module-outline lesson-outline" id="lesson-outline"><summary aria-label="Show lesson sections" title="Lesson sections">${icon('courses')}<span class="lesson-outline-label" aria-hidden="true">Sections</span></summary><nav class="module-menu lesson-menu" aria-label="Lesson sections"><div class="eyebrow">In this lesson</div>${lessonSections(l).map((s,i)=>`<button type="button" data-section="${s.id}"><span class="section-number" aria-hidden="true">${String(i+1).padStart(2,'0')}</span><span>${esc(s.title)}</span></button>`).join('')}</nav></details>`;
}
function readingOffset(){
  const trail=$('.module-trail')||$('.revision-context');
  return trail?(parseFloat(window.getComputedStyle?.(trail).top)||0)+trail.getBoundingClientRect().height+18:($('.topbar')?.getBoundingClientRect?.().height??0)+18;
}
function bindReadingOutline(){
  const outline=$('#lesson-outline');if(!outline)return;
  bindOutlineKeys(outline,'[data-section]');
  const buttons=Array.from(outline.querySelectorAll('[data-section]'));
  let queued=false,disposed=false;
  const update=()=>{
    queued=false;if(disposed)return;
    const offset=readingOffset();let current=buttons[0];
    for(const button of buttons){const section=document.getElementById(button.dataset.section);if(section?.getBoundingClientRect().top<=offset+35)current=button;}
    for(const button of buttons){if(button===current)button.setAttribute('aria-current','location');else button.removeAttribute('aria-current');}
    const label=outline.querySelector('.lesson-outline-label'),title=current?.querySelector('span:last-child')?.textContent||'Lesson sections';
    label.textContent='Sections';outline.querySelector('summary').title='Current section: '+title;
    fitOutlineMenu(outline);
  };
  const schedule=()=>{if(!queued){queued=true;frame(update);}};
  const page=$('#page'),outside=event=>{if(outline.open&&!outline.contains(event.target))outline.open=false;};
  outline.addEventListener('click',event=>{
    const button=event.target.closest('[data-section]');if(!button||!outline.contains(button))return;
    const target=document.getElementById(button.dataset.section);if(!target)return;
    outline.open=false;target.focus({preventScroll:true});
    window.scrollTo({top:Math.max(0,window.scrollY+target.getBoundingClientRect().top-readingOffset()),behavior:window.matchMedia?.('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});
  });
  outline.addEventListener('keydown',event=>{if(event.key==='Escape'){outline.open=false;outline.querySelector('summary').focus();event.stopPropagation();}});
  outline.addEventListener('toggle',()=>{if(outline.open){update();alignOutlineMenu(outline);}});
  page.addEventListener('click',outside);window.addEventListener?.('scroll',schedule,{passive:true});window.addEventListener?.('resize',schedule);
  releaseReadingOutline=()=>{disposed=true;page.removeEventListener('click',outside);window.removeEventListener?.('scroll',schedule);window.removeEventListener?.('resize',schedule);};
  schedule();
}
function roadmapPractice(l){
  const path=l.path==='shared'?selectedPath():l.path,e=lessonEvidence(l);
  return `<div class="roadmap-practice">
    <div><div class="eyebrow">Understand</div><a href="${moduleHref('courses',l.id,l,path)}">${e.checked?'✓ Check passed · revisit lesson':'Read the lesson & take its check'} ↗</a></div>
    ${l.questions.length?`<div><div class="eyebrow">Apply</div><a href="${moduleHref('question-list',l.id,l,path)}">Interview question list <span class="practice-label">${e.numeric+e.self}/${e.questionTotal} passed ↗</span></a></div>`:''}
    ${l.coding.length?`<div><div class="eyebrow">Implement</div><a href="${moduleHref('coding-list',l.id,l,path)}">Coding exercise list <span class="practice-label">${e.accepted}/${e.codingTotal} passed ↗</span></a></div>`:''}
    ${(l.trainers||[]).length?`<div><div class="eyebrow">Build fluency</div>${l.trainers.map(id=>`<a href="${moduleHref('trainers',id,l,path)}">${esc(trainerTypes.find(t=>t.id===id).name)} ↗</a>`).join('')}</div>`:''}
  </div>`;
}
function roadmapStep(l,index,next){
  const e=lessonEvidence(l),isNext=l.id===next?.id;
  return `<details class="roadmap-step ${e.checked?'checked':''} ${isNext?'is-next':''}" id="step-${l.id}" ${isNext?'open':''}>
    <summary><span class="route-node" aria-hidden="true">${e.checked?'✓':String(index+1).padStart(2,'0')}</span><span class="step-copy"><span class="step-title">${esc(l.title)}</span><span class="step-meta">${esc(l.topic)} <span>·</span> ${l.minutes} min ${isNext?'<span class="next-label">Up next</span>':''}</span><span class="evidence-line"><span class="evidence-dot ${e.checked?'filled':''}"></span>${e.checked?'Check passed':'Check to do'}${e.questionTotal?`<span class="evidence-dot ${e.numeric+e.self===e.questionTotal?'filled':''}"></span>${e.numeric+e.self}/${e.questionTotal} ${e.questionTotal===1?'problem':'problems'}${e.self?' · self-assessed':''}`:''}${e.codingTotal?`<span class="evidence-dot ${e.accepted===e.codingTotal?'filled':''}"></span>${e.accepted}/${e.codingTotal} code${e.assisted?' · assisted':''}`:''}${(l.trainers||[]).length?`<span class="evidence-dot ${e.sessions?'filled':''}"></span>${e.sessions} drill rounds`:''}</span></span><span class="step-chevron" aria-hidden="true">⌄</span></summary>
    <div class="step-body"><p>${esc(l.intro)}</p><ul class="step-objectives">${(l.objectives||[]).map(o=>`<li>${esc(o)}</li>`).join('')}</ul>${roadmapPractice(l)}</div>
  </details>`;
}
function paths(){
  const path=selectedPath(),lessons=journeyLessons(path),e=routeEvidence(lessons),resume=nextRouteActivity(path),next=resume?.lesson;
  const phases=[...roadmapPhases.shared,...roadmapPhases[path]];
  const routeDescription=path==='researcher'?'Inference, validation, simulation and research code.':'Conditional value, order flow, decisions and payoff mathematics.';
  return header('Your learning roadmap','Learning roadmap','Shared foundation, then your research or trading path.')+`
  <section class="route-overview" aria-label="Route and progress">
    <div class="route-switch" aria-label="Choose your destination"><div class="route-origin"><span class="mono">START HERE</span><strong>Shared foundation</strong><span class="small muted">${content.lessons.filter(l=>l.path==='shared').length} modules for both paths</span></div><span class="route-fork" aria-hidden="true">${icon('paths')}</span><div class="route-destinations">${['researcher','trader'].map(p=>`<a href="#paths/${p}" data-destination="${p}" class="route-destination ${p===path?'selected':''}" ${p===path?'aria-current="true"':''}><span class="destination-dot" aria-hidden="true"></span><span>${pathName(p)}</span><span class="small muted">${content.lessons.filter(l=>l.path===p).length} modules</span></a>`).join('')}</div></div>
    <div class="route-progress"><div class="route-progress-heading"><span class="mono">${QA?'TEST PREVIEW ·':'YOUR'} ${path==='researcher'?'RESEARCH':'TRADING'} ROUTE</span><span><strong>${e.checked}</strong> / ${e.total} ${QA?'test ':''}lesson checks</span></div>${QA?`<p class="route-preview-note">Development results, separate from your progress. <a href="${esc('/'+(location.hash||'#paths'))}">Open my personal route ↗</a></p>`:''}<progress value="${e.checked}" max="${e.total}" aria-label="${QA?'Test preview: ':''}Lesson checks passed on your ${path} route"></progress><div class="route-progress-detail"><span>${QA?'Test problems: ':''}${e.solved} / ${e.questionTotal} interview problems solved${e.self?` · ${e.self} self-assessed`:''}</span><span>${QA?'Test exercises: ':''}${e.accepted} / ${e.codingTotal} Python exercises passed</span></div></div>
  </section>
  <div class="roadmap-layout"><div class="roadmap-journey">
    ${phases.map(([title,description,ids],i)=>`<section class="roadmap-phase" aria-labelledby="phase-${i}">${i===2?`<div class="specialisation-marker"><span>SHARED FOUNDATION</span><span>↳ ${pathName(path).toUpperCase()}</span></div>`:''}<div class="phase-heading"><span class="phase-number mono">${String(i+1).padStart(2,'0')}</span><div><h2 id="phase-${i}">${title}</h2><p>${description}</p></div><span class="phase-count mono">${ids.filter(id=>state.lessons[id]?.passed).length}/${ids.length}</span></div><div class="phase-steps">${ids.map(id=>{const l=content.lessons.find(l=>l.id===id);return roadmapStep(l,lessons.indexOf(l),next);}).join('')}</div></section>`).join('')}
  </div>${routeCompass(path,resume,e,routeDescription)}</div>`;
}
function routeCompass(path,resume,e,description){
  const l=resume?.lesson,a=resume?.activity;
  return `<aside class="roadmap-compass" aria-label="Your next move"><div class="compass-card"><div class="eyebrow">${a?'Your next move':'Core route complete'}</div><h2>${l?esc(l.title):'Keep the reasoning fresh.'}</h2><p>${a?`${a.title!==l?.title?esc(a.title)+' · ':''}${esc(activityMeta(a,l))}`:'All linked checks, problems and code have recorded results. Keep revisiting the reasoning and practising your fluency.'}</p>${e.checked===e.total?'<p class="small">Every lesson check passed. Problem solves and Python submissions are tracked separately.</p>':''}<a class="btn dark" href="${a?.href||'#review'}"><span class="btn-label">${a?activityLabel(a.kind):'Open revision queue'}</span><span class="btn-arrow" aria-hidden="true">↗</span></a>${l?`<a class="compass-link" href="#paths/${path}/step-${l.id}">Locate on roadmap ↓</a>`:''}</div></aside>`;
}
function lessonNavigation(l){
  const active=moduleContext(),path=active?.lesson.id===l.id?active.path:l.path==='shared'?preferredPath():l.path;
  return moduleContinuation({lesson:l,path,kind:'courses',id:l.id});
}
function progressFilters(kind){return kind==='exercises'?[['all','All progress'],['pending','Not yet passed'],['passed','Passed without editorial'],['assisted','Passed with editorial'],['practising','Draft in progress'],['reviewed','Editorial read']]:[['all','All progress'],['pending','Not yet solved'],['solved','Unaided solve'],['reviewed','Reviewed'],['practising','In practice']];}
function hasFilters(){return Object.entries(filters).some(([name,value])=>name==='search'?value.trim():value!=='all');}
function filterBar(data,kind){const topics=[...new Set(data.map(q=>q.topic))].sort();return `<div class="filters"><input class="search" id="search" aria-label="Search ${kind}" placeholder="Search ${kind}…" value="${esc(filters.search)}"><select class="select" id="difficulty" aria-label="Difficulty">${['all','Easy','Medium','Hard'].map(x=>`<option value="${x}" ${x===filters.difficulty?'selected':''}>${x==='all'?'All difficulties':x}</option>`).join('')}</select><select class="select" id="topic" aria-label="Topic"><option value="all">All topics</option>${topics.map(x=>`<option value="${esc(x)}" ${x===filters.topic?'selected':''}>${esc(x)}</option>`).join('')}</select><select class="select" id="path" aria-label="Path">${['all','shared','researcher','trader'].map(x=>`<option value="${x}" ${x===filters.path?'selected':''}>${x==='all'?'All paths':pathName(x)}</option>`).join('')}</select><select class="select" id="status" aria-label="Progress">${progressFilters(kind).map(([value,label])=>`<option value="${value}" ${value===filters.status?'selected':''}>${label}</option>`).join('')}</select><button class="btn compact filter-reset" id="reset-filters" type="button" data-action="reset-filters" ${hasFilters()?'':'disabled'}>Reset filters</button></div>`;}
function codingStatus(item){
  const s=state.coding[item.id]||{};
  if(s.accepted)return acceptedWithEditorial(s)?'assisted':'passed';
  if(s.assisted)return 'reviewed';
  return state.drafts[item.id]!==undefined&&state.drafts[item.id]!==item.starter?'practising':'new';
}
function matchesProgress(item){
  if(filters.status==='all')return true;
  const code=typeof item.starter==='string',status=code?codingStatus(item):questionStatus(item.id);
  if(filters.status==='pending')return code?!state.coding[item.id]?.accepted:!questionState(item.id).solved&&!questionState(item.id).selfSolved;
  return status===filters.status;
}
function filtered(data){return data.filter(q=>(filters.difficulty==='all'||q.difficulty===filters.difficulty)&&(filters.topic==='all'||q.topic===filters.topic)&&(filters.path==='all'||q.path===filters.path)&&matchesProgress(q)&&`${q.title} ${q.topic} ${q.prompt}`.toLowerCase().includes(filters.search.trim().toLowerCase()));}
function emptyCollection(kind,columns){return `<tr><td colspan="${columns}" class="empty"><strong>No ${kind} match these filters.</strong><p class="small muted">Broaden a filter or return to the complete library.</p><button class="btn compact" type="button" data-action="reset-filters">Clear all filters</button></td></tr>`;}
function refreshCollection(){
  const isCode=route[0]==='coding',items=filtered(isCode?coding:content.questions);
  $('#collection').innerHTML=isCode?codeTable(items):questionTable(items);
  if($('#result-count'))$('#result-count').textContent=items.length;
  if($('#result-unit'))$('#result-unit').textContent=(isCode?'exercise':'problem')+(items.length===1?'':'s');
  if($('#reset-filters'))$('#reset-filters').disabled=!hasFilters();
}
function questionTable(data){return `<div class="table-wrap"><table><thead><tr><th>Problem</th><th>Topic</th><th>Difficulty</th><th>Format</th><th>Progress</th></tr></thead><tbody>${data.map(q=>`<tr><td class="title-cell"><a href="#questions/${q.id}">${esc(q.title)} ↗</a><div class="row-meta">${pathName(q.path).toUpperCase()} · ${q.minutes} MIN</div></td><td class="muted">${esc(q.topic)}</td><td>${badge(q.difficulty)}</td><td class="muted">${q.type==='numeric'?'Numeric':'Multi-part check'}</td><td>${statusHTML(q.id)}</td></tr>`).join('')||emptyCollection('problems',5)}</tbody></table></div>`;}
function questions(){
  if(route[1]){const q=content.questions.find(q=>q.id===route[1]);if(q)return questionDetail(q);}
  return header('Practice / Interview questions','Interview questions','')+filterBar(content.questions,'problems')+`<div class="practice-note"><span role="status" aria-live="polite" aria-atomic="true"><span id="result-count">${filtered(content.questions).length}</span> <span id="result-unit">${filtered(content.questions).length===1?'problem':'problems'}</span></span> · All questions are checked automatically. Multi-part checks require every checkpoint to pass.</div><div id="collection">${questionTable(filtered(content.questions))}</div>`;
}
function objectiveDraftKey(q){return q.id+'-'+q.assessmentVersion;}
function objectiveDraft(q){
  try{const value=JSON.parse(state.drafts[objectiveDraftKey(q)]||'{}');return value&&typeof value==='object'&&!Array.isArray(value)?value:{};}catch{return {};}
}
function gradeObjective(q,answers){
  // No partial-credit completion: every numerical and exact-set checkpoint
  // must pass. Reject malformed inputs rather than normalizing into a pass.
  let matched=0;
  for(const check of q.checks){
    const value=answers[check.id];
    if(check.type==='numeric'){
      if(typeof value!=='string'||!value.trim())return {complete:false,message:'Answer every checkpoint before checking.'};
      const parsed=numberAnswer(value);
      if(Math.abs(parsed-check.answer)<=check.tolerance)matched++;
    }else{
      if(!Array.isArray(value)||!value.length)return {complete:false,message:'Select at least one statement in each choice checkpoint.'};
      const ids=new Set(value);
      if(ids.size!==value.length||value.some(id=>typeof id!=='string'||!check.options.some(o=>o.id===id)))return {complete:false,message:'Choose statements from the displayed options.'};
      if(check.options.every(o=>ids.has(o.id)===o.correct))matched++;
    }
  }
  return {complete:true,correct:matched===q.checks.length,matched,total:q.checks.length};
}
function objectiveForm(q){
  const draft=objectiveDraft(q);
  return `<form id="answer-form" class="objective-checks"><div class="checkpoint-intro"><h2>Check your reasoning</h2><p>Work through the problem, then answer every checkpoint. For choice checkpoints, select <strong>all</strong> valid statements. Every checkpoint must match to pass.</p></div>${q.checks.map((c,i)=>`<fieldset class="objective-part"><legend><span class="checkpoint-number">${String(i+1).padStart(2,'0')}</span><span>${esc(c.prompt)}</span></legend>${c.type==='numeric'?`<label class="sr-only" for="check-${c.id}">Checkpoint ${i+1} answer</label><input class="input checkpoint-number-input" id="check-${c.id}" name="${c.id}" data-check="${c.id}" autocomplete="off" placeholder="A number or expression" value="${esc(typeof draft[c.id]==='string'?draft[c.id]:'')}"><p class="checkpoint-help">Fractions and arithmetic accepted · tolerance ${c.tolerance}</p>`:`<p class="checkpoint-help">Select all valid statements.</p><div class="checkpoint-choices">${c.options.map((o,j)=>`<label class="checkpoint-choice"><input type="checkbox" aria-label="${esc(o.label)}" id="check-${c.id}-${o.id}" name="${c.id}" data-check="${c.id}" value="${o.id}" ${Array.isArray(draft[c.id])&&draft[c.id].includes(o.id)?'checked':''}><span class="choice-letter" aria-hidden="true">${String.fromCharCode(65+j)}</span><span>${esc(o.text)}</span></label>`).join('')}</div>`}</fieldset>`).join('')}<div class="answer-buttons"><button class="btn primary" type="submit">Check answers →</button><button class="btn" type="button" data-action="new-attempt">Fresh attempt</button></div><div id="answer-feedback" class="feedback ${esc(view[q.id]?.feedbackClass||'')}" role="status">${esc(view[q.id]?.feedback||'')}</div></form>`;
}
function objectiveReview(q){
  if(q.type!=='structured')return '';
  return `<div class="checkpoint-review"><h3>Checkpoint reasoning</h3>${q.checks.map((c,i)=>`<section><h4>${i+1}. ${esc(c.prompt)}</h4>${c.type==='numeric'?`<p>Answer: <strong>${esc(String(c.answer))}</strong>. ${esc(c.explanation)}</p>`:`<ol type="A">${c.options.map(o=>`<li><strong>${o.correct?'Valid':'Invalid'}.</strong> ${esc(o.text)}<p>${esc(o.explanation)}</p></li>`).join('')}</ol>`}</section>`).join('')}</div>`;
}
function legacyReasoning(q){
  if(q.type!=='structured'||!state.drafts[q.id])return '';
  const v=view[q.id]||{};
  return `<section class="previous-attempt"><button class="btn link" type="button" data-action="legacy-reasoning" aria-expanded="${!!v.legacy}">${v.legacy?'Hide':'Show'} earlier written work</button>${v.legacy?`<p class="practice-note">Kept from the previous format. Viewing it counts as assistance for this attempt.</p><pre>${esc(state.drafts[q.id])}</pre>`:''}</section>`;
}
function questionDetail(q){
  const s=questionState(q.id),v=view[q.id]||{},hintCount=s.hints||0,context=moduleContext(),related=context?moduleHref('courses',context.lesson.id,context.lesson,context.path):'#courses/'+q.lesson,structured=q.type==='structured';
  const numericForm=`<form id="answer-form"><label for="answer">Answer</label><input class="input" id="answer" autocomplete="off" placeholder="e.g. 11/36" value="${esc(state.drafts[q.id]||'')}"><div class="answer-buttons"><button class="btn primary" type="submit">Check answer →</button><button class="btn" type="button" data-action="new-attempt">Fresh attempt</button></div></form><div id="answer-feedback" class="feedback ${esc(v.feedbackClass||'')}" role="status">${esc(v.feedback||'')}</div>`;
  return revisionContext(q)+`${practiceBreadcrumb('questions',q.topic)}<div class="detail-layout${structured?' objective-layout':''}"><article class="problem"><div class="tags">${badge(q.difficulty)}<span class="badge written">${pathName(q.path)}</span><span class="small muted">${q.minutes} min suggested</span></div><h1>${esc(q.title)}</h1><p class="prompt">${esc(q.prompt)}</p>${structured?objectiveForm(q):''}<div class="divider"></div><div class="answer-buttons"><button class="btn" data-action="hint" ${hintCount>=q.hints.length?'disabled':''}>${hintCount>=q.hints.length?'All hints revealed':`Reveal hint ${hintCount+1} / ${q.hints.length}`}</button><button class="btn" data-action="solution">${s.reveal?'Hide':'Show'} worked solution</button></div>${q.hints.slice(0,hintCount).map((h,i)=>`<div class="hint"><div class="eyebrow">Hint ${i+1}</div>${esc(h)}</div>`).join('')}${s.reveal?`<section class="solution"><h3>Worked solution</h3>${esc(q.solution)}${objectiveReview(q)}<div class="answer-buttons"><button class="btn compact" data-action="reviewed">Save as reviewed</button><a class="btn compact" href="${related}">Related lesson ↗</a></div></section>`:''}<section class="follow"><div class="eyebrow">The interviewer goes further</div><p>${esc(q.followup)}</p><button class="btn link" data-action="follow">${v.follow?'Hide':'Reveal'} follow-up reasoning ↗</button>${v.follow?`<div class="hint">${esc(q.followSolution)}</div>`:''}</section></article><aside><section class="panel answer-panel"><div class="eyebrow">Your attempt</div><h3>${structured?'Derive. Then verify.':'Work it out. Then check.'}</h3><p class="small muted">${structured?'Numerical and reasoning checkpoints are checked automatically. Use the scratchpad for your derivation.':'Decimals, fractions, percentages, and arithmetic expressions are accepted. Tolerance: 0.000001.'}</p>${structured?'':numericForm}<p class="practice-note">${s.assisted?'Hints, solutions or previous work viewed in this attempt.':'Closed-book attempt.'} ${statusHTML(q.id)}</p>${structured&&state.questions[q.id]?.selfSolved?'<p class="practice-note">Earlier self-assessment kept in your record. Pass these checks to complete the new format.</p>':''}${legacyReasoning(q)}${previousAttempt(q)}<div class="revision-schedule"><label for="confidence">Schedule your next revision</label><select id="confidence" class="select"><option value="1">Tomorrow</option><option value="3" selected>In 3 days</option><option value="7">In 7 days</option></select><button class="btn compact" data-action="schedule">Schedule revision</button>${s.due?`<p class="revision-receipt">Next revision: <strong>${esc(dateLabel(s.due))}</strong>${s.due<=Date.now()?' · due now':''}</p>`:''}</div></section><section class="scratch panel answer-panel"><label for="scratchpad">Scratchpad</label><textarea id="scratchpad" rows="8" placeholder="An equation, a sample space, a counterexample…">${esc(state.drafts[q.id+'-scratch']||'')}</textarea></section></aside></div>`+(route[2]==='revision'?'<div class="revision-return"><a class="btn" href="#review">Back to revision queue ↗</a></div>':'');
}
function courses(){
  if(route[1]){const l=content.lessons.find(l=>l.id===route[1]);if(l)return lessonDetail(l);}
  const chosen=route[2]||'all';
  return header('Library / Courses','Courses','')+`<div class="path-tabs">${['all','shared','researcher','trader'].map(p=>`<a class="chip ${p===chosen?'active':''}" href="#courses/filter/${p}">${p==='all'?'All '+content.lessons.length+' modules':pathName(p)}</a>`).join('')}</div><div class="card-grid course-grid">${content.lessons.filter(l=>chosen==='all'||l.path===chosen).map((l,i)=>`<article class="card"><div class="card-body"><div class="eyebrow">${l.id.slice(1)} / ${pathName(l.path)}</div><h3>${esc(l.title)}</h3><p>${esc(l.intro)}</p><div class="card-foot"><span class="small muted">${l.minutes} min ${state.lessons[l.id]?.passed?'· ✓ Check passed':''}</span><a class="btn compact" href="#courses/${l.id}">Study ↗</a></div></div></article>`).join('')}</div>`;
}
function lessonDetail(l){const result=view[l.id]||{},authored=authoredLesson(l),illustrated=Boolean(authored);return `<div class="breadcrumbs"><a href="#courses">Courses</a><span>/</span><span>${pathName(l.path)}</span></div><div class="lesson-layout${illustrated?' sample-space-layout':''}"><article class="reading${illustrated?' sample-space-reading':''}"><div class="eyebrow">Module ${moduleNumber(l)} · ${l.minutes} min</div><h1>${esc(l.title)}</h1><p class="intro">${esc(l.intro)}</p>${illustrated?`<details class="atlas-goals"><summary>What you’ll learn</summary><ul>${(l.objectives||[]).map(o=>`<li>${esc(o)}</li>`).join('')}</ul></details>`:`<section class="lesson-objectives" aria-label="Learning goals"><div class="eyebrow">By the end of this module</div><ul>${(l.objectives||[]).map(o=>`<li>${esc(o)}</li>`).join('')}</ul></section>`}${illustrated?authored.body(l):`${l.sections.map((s,i)=>`<section class="lesson-section" aria-labelledby="lesson-section-${i}"><h2 id="lesson-section-${i}" tabindex="-1">${esc(s.title)}</h2><p>${esc(s.text)}</p></section>`).join('')}<div class="example" id="lesson-example" tabindex="-1" aria-label="A concrete example"><div class="eyebrow">A concrete example</div><p>${esc(l.example)}</p></div>`}<section class="quiz" id="lesson-check" tabindex="-1" aria-label="Understanding check"><div class="eyebrow">Understanding check ${state.lessons[l.id]?.passed?'· ✓ Passed':''}</div><h3>${esc(l.check)}</h3><form id="quiz-form">${l.options.map((option,i)=>`<label class="option"><input type="radio" name="option" value="${i}" ${result.choice===i?'checked':''} aria-label="${esc(l.optionLabels?.[i]||option)}" required><span>${esc(option)}</span></label>`).join('')}<button class="btn primary" type="submit">Check understanding →</button></form><div class="feedback ${result.passed?'good':'bad'}">${esc(result.message||'')}</div></section>${lessonNavigation(l)}</article>${lessonPractice(l)}</div>`;}
function codeTable(data){return `<div class="table-wrap"><table><thead><tr><th>Exercise</th><th>Topic</th><th>Difficulty</th><th>Progress</th></tr></thead><tbody>${data.map(c=>`<tr><td class="title-cell"><a href="#coding/${c.id}">${esc(c.title)} ↗</a></td><td class="muted">${esc(c.topic)}</td><td>${badge(c.difficulty)}</td><td class="status ${state.coding[c.id]?.accepted?'solved':''}">${state.coding[c.id]?.accepted?`✓ Passed${acceptedWithEditorial(state.coding[c.id])?' · with editorial':''}`:codingStatus(c)==='reviewed'?'↗ Editorial read':codingStatus(c)==='practising'?'Draft in progress':'—'}</td></tr>`).join('')||emptyCollection('exercises',4)}</tbody></table></div>`;}
function codePage(){
  if(route[1]){const c=coding.find(c=>c.id===route[1]);if(c)return codeDetail(c);}
  return header('Practice / Python','Python workspace','')+filterBar(coding,'exercises')+`<div class="practice-note"><span role="status" aria-live="polite" aria-atomic="true"><span id="result-count">${filtered(coding).length}</span> <span id="result-unit">${filtered(coding).length===1?'exercise':'exercises'}</span></span> · Python 3 · Standard library only · Debugging runs earn no completion; Submit checks the official suite.</div><div id="collection">${codeTable(filtered(coding))}</div>`;
}
// Debug cases live beside solution drafts, so they use the same workspace,
// backup, recovery and multi-tab conflict handling. They never confer credit.
function debugCases(c){
  try{
    const saved=JSON.parse(state.drafts[c.id+'-tests']);
    if(saved&&Array.isArray(saved.cases)&&saved.cases.length<=20&&saved.cases.every(t=>t&&typeof t.id==='string'&&typeof t.label==='string'&&typeof t.argumentsJSON==='string'&&typeof t.expectedJSON==='string'&&typeof t.enabled==='boolean')&&new Set(saved.cases.map(t=>t.id)).size===saved.cases.length){
      if(!saved.cases.some(t=>t.id===saved.selected))saved.selected=saved.cases[0]?.id||'';
      return saved;
    }
  }catch{}
  const cases=c.samples.map((sample,i)=>({id:'example-'+i,label:'Example '+(i+1),argumentsJSON:JSON.stringify(sample.args),expectedJSON:JSON.stringify(sample.expected),enabled:true}));
  return {selected:cases[0]?.id||'',cases};
}
function saveDebugCases(c,record){state.drafts[c.id+'-tests']=JSON.stringify(record);touch();}
function debugError(c,message){(view[c.id]||={}).debugError=message;const node=$('#debug-feedback');if(node)node.textContent=message;if(message)announce(message);}
function debugRunCases(c){
  const selected=debugCases(c).cases.filter(t=>t.enabled);
  if(!selected.length)throw Error('Include at least one debugging case before running.');
  return selected.map(t=>{
    try{
      if(t.argumentsJSON.length+t.expectedJSON.length>500000)throw Error('Use at most 500,000 characters per case.');
      const args=JSON.parse(t.argumentsJSON);
      if(!Array.isArray(args))throw Error('Arguments must be a JSON array, with one entry per function parameter.');
      if(t.expectedJSON.trim())JSON.parse(t.expectedJSON);
    }catch(error){throw Error(t.label+': '+error.message);}
    // Preserve the original JSON text, particularly integers beyond JS precision.
    return {argumentsJSON:t.argumentsJSON,expectedJSON:t.expectedJSON};
  });
}
function addDebugCase(c,copy,label){
  const record=debugCases(c);
  if(record.cases.length>=20){debugError(c,'You can keep up to 20 debugging cases. Remove one before adding another.');return false;}
  const id='case-'+Date.now().toString(36)+'-'+Math.random().toString(36).slice(2);
  record.cases.push({id,label:label||'Custom '+(record.cases.length+1),argumentsJSON:copy?.argumentsJSON??'[]',expectedJSON:copy?.expectedJSON??'',enabled:true});
  record.selected=id;saveDebugCases(c,record);debugError(c,'');render();
  const epoch=renderEpoch;frame(()=>{if(epoch!==renderEpoch)return;const field=$('#debug-arguments');field?.focus({preventScroll:true});field?.scrollIntoView?.({block:'center',behavior:window.matchMedia?.('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});});return true;
}
async function loadSubmissionCases(c){
  const v=view[c.id]||={};if(v.loadingCases)return;v.loadingCases=true;v.debugError='';render();
  const generation=runnerGeneration;
  try{
    const response=await fetch('/api/coding-cases',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:c.id})});
    const result=await response.json();if(!response.ok)throw Error(result.error||'Could not load submission cases.');
    if(!Array.isArray(result.cases)||!result.cases.length||!result.cases.every(t=>typeof t.argumentsJSON==='string'&&typeof t.expectedJSON==='string'))throw Error('The server returned incomplete cases.');
    if(generation===runnerGeneration)v.officialCases=result.cases;
  }catch(error){if(generation===runnerGeneration)v.debugError=error.message||'The local server is unavailable.';}
  finally{v.loadingCases=false;if(generation===runnerGeneration&&route[0]==='coding'&&route[1]===c.id){render();$('#submission-case')?.focus({preventScroll:true});}}
}
function startCodeCheck(c,mode){
  if(view[c.id]?.running)return;
  let cases;
  if(mode==='debug'){try{cases=debugRunCases(c);debugError(c,'');}catch(error){debugError(c,error.message);return;}}
  const code=codeEditor?codeEditor.getValue():$('#code').value;
  return executeCode(c,mode,code,cases);
}
function handleCodingShortcut(event,c){
  if(event.defaultPrevented||event.isComposing||!event.metaKey||event.ctrlKey||event.altKey||event.shiftKey)return false;
  const mode=event.key==='Enter'?'submit':event.key==="'"?'debug':null;
  if(!mode)return false;
  event.preventDefault();event.stopPropagation();
  if(!event.repeat&&!view[c.id]?.running)startCodeCheck(c,mode);
  return true;
}
function debugPanel(c){
  const record=debugCases(c),selected=record.cases.find(t=>t.id===record.selected),v=view[c.id]||{};
  return `<section class="debug-panel math-plain" aria-labelledby="debug-title"><div class="debug-heading"><h3 id="debug-title">Test cases</h3><span class="small muted">${record.cases.filter(t=>t.enabled).length} included · debugging only</span><button type="button" class="btn compact" data-action="add-debug-case" ${record.cases.length>=20?'disabled':''}>+ Add case</button></div><div class="debug-case-tabs" role="group" aria-label="Choose a debugging case">${record.cases.map(t=>`<button type="button" class="debug-case-tab" id="debug-case-${esc(t.id)}" data-action="select-debug-case" data-case="${esc(t.id)}" aria-pressed="${t.id===record.selected}">${esc(t.label)}${t.enabled?'':' · excluded'}</button>`).join('')}</div>${selected?`<div class="debug-case-tools"><label class="debug-include"><input type="checkbox" id="debug-enabled" ${selected.enabled?'checked':''}> Include in run</label><button type="button" class="btn link" data-action="remove-debug-case">Remove case</button></div><div class="debug-fields"><div><label for="debug-arguments">Arguments · JSON array</label><textarea id="debug-arguments" rows="3" spellcheck="false" aria-describedby="debug-input-help debug-feedback">${esc(selected.argumentsJSON)}</textarea></div><div><label for="debug-expected">Expected result · optional</label><textarea id="debug-expected" rows="3" spellcheck="false" aria-describedby="debug-input-help debug-feedback">${esc(selected.expectedJSON)}</textarea></div></div>`:'<p class="small muted">Add a case or copy one from the submission suite.</p>'}<p id="debug-input-help" class="small muted">One array entry per solve parameter. Use JSON: lists, numbers, strings, true, false, null. Leave expected blank to inspect output; null checks for Python None.</p><details class="submission-cases" ${v.officialCases||v.loadingCases?'open':''}><summary>Copy from submission suite</summary><p class="small muted">Editable debugging copies. Submit always checks the original suite.</p>${v.officialCases?`<div class="submission-case-picker"><label class="sr-only" for="submission-case">Submission case</label><select class="select" id="submission-case">${v.officialCases.map((t,i)=>`<option value="${i}">Submission case ${t.caseNumber||i+1}</option>`).join('')}</select><button type="button" class="btn compact" data-action="copy-submission-case">Add copy</button></div>`:`<button type="button" class="btn compact" data-action="load-submission-cases" ${v.loadingCases?'disabled':''}>${v.loadingCases?'Loading…':'Choose a submission case'}</button>`}</details><p id="debug-feedback" class="debug-feedback" role="alert">${esc(v.debugError||'')}</p></section>`;
}

function codeDetail(c){const v=view[c.id]||{},s=state.coding[c.id]||{};return `${practiceBreadcrumb('coding',c.topic)}<div class="coding-layout"><article class="panel coding-description"><div class="tags">${badge(c.difficulty)}<span class="badge written">Python 3</span></div><h1>${esc(c.title)}</h1><p>${esc(c.prompt)}</p><div class="divider"></div><div class="eyebrow">Visible examples</div>${c.samples.map((s,i)=>`<div class="sample">Example ${i+1}\nArguments: ${esc(JSON.stringify(s.args))}\nExpected: ${esc(JSON.stringify(s.expected))}</div>`).join('')}<p class="practice-note">Define solve with the supplied signature. Return the result rather than printing it. Follow the exercise’s stated output format.</p><button class="btn link" data-action="editorial">${v.editorial?'Hide':'Read'} editorial ↗</button>${v.editorial?`<div class="editorial"><h3>The approach</h3><p>${esc(c.explanation)}</p><pre>${esc(c.solution)}</pre></div>`:''}</article><section class="panel python-workspace" aria-label="Python editor and results"><div class="editor-head"><span>solution.py</span><span>${s.accepted?(acceptedWithEditorial(s)?'✓ Exercise passed · with editorial':'✓ Exercise passed · full suite'):'Python 3'}</span></div><div id="code-host" class="code-host math-plain"><textarea id="code" class="code-editor" spellcheck="false" autocapitalize="off" autocomplete="off" aria-label="Python solution">${esc(state.drafts[c.id]??c.starter)}</textarea></div><div class="editor-status"><span id="editor-position">Ln 1, Col 1</span><span>Python · 4 spaces</span></div><div class="editor-help" id="editor-help">Tab to indent · Shift+Tab to unindent · Esc then Tab to leave editor</div>${debugPanel(c)}<div class="editor-actions"><button class="btn compact" data-action="restore-starter" ${v.running?'disabled':''}>Restore starter</button><button class="btn" data-action="run-code" ${v.running?'disabled':''}>${v.running&&v.mode!=='submit'?'Running…':'Run tests'} <kbd>⌘ '</kbd></button><button class="btn primary" data-action="submit-code" ${v.running?'disabled':''}>${v.running&&v.mode==='submit'?'Checking…':'Submit'} <kbd>⌘ ↵</kbd></button></div><div id="runner-draft-note">${runnerDraftNote(c)}</div><div id="runner-result" class="runner-result" aria-busy="${!!v.running}">${v.running?'<p class="small muted">Executing Python locally… You can keep editing; this check uses the version sent when you clicked.</p>':runnerHTML(v.result,v.mode)}${v.checkedCode!==undefined?`<details class="checked-code"><summary>Checked version · ${v.mode==='debug'?'debugging cases':v.mode==='run'?'visible example':'complete suite'}</summary><pre>${esc(v.checkedCode)}</pre></details>`:''}</div></section></div>`;}
function errorLineButton(line){return Number.isInteger(line)&&line>0?`<button class="btn link error-line" type="button" data-action="error-line" data-line="${line}">Go to line ${line} ↗</button>`:'';}
function runnerHTML(result,mode){
  if(!result)return '<p class="small muted">Run your debugging cases, then submit against the complete test suite.</p>';
  const stdout=result.stdout?`<details class="runner-output" open><summary>Printed output</summary><pre>${esc(result.stdout)}</pre></details>`:'';
  if(result.error)return `<div class="feedback bad"><strong>Check could not finish</strong><pre>${esc(result.error)}</pre>${errorLineButton(result.errorLine)}${/your draft is saved/i.test(result.error)?'':'<p>Your draft is saved. Correct the issue, then run or submit again.</p>'}</div>${stdout}`;
  const unchecked=result.results.filter(r=>r.passed===null).length;
  return `<h3>${result.passed===result.total?'✓':'↗'} ${result.passed} / ${result.total-unchecked} tests passed${unchecked?` · ${unchecked} output${unchecked===1?'':'s'} inspected`:''}</h3><div class="small muted">${mode==='debug'?'Debugging only · completion unchanged':mode==='run'?'Visible example only':'Complete suite'} · ${result.elapsedMs} ms${mode==='submit'&&result.passed===result.total?' · Submission saved':''}</div>${(result.results||[]).map((r,i)=>`<div class="result-row"><div class="result-case-heading"><span>${r.passed===null?'○':r.passed?'✓':'×'} ${i===0&&mode!=='debug'?'Example':'Case '+(i+1)} · ${r.passed===null?'Output only':r.passed?'Passed':'Failed'}</span>${typeof r.argumentsJSON==='string'?`<button type="button" class="btn compact" data-action="debug-result-case" data-index="${i}">Debug this case</button>`:''}</div>${!r.passed||mode==='debug'?`<details ${mode==='debug'?'open':''}><summary>${r.passed===false?`Inspect ${i===0&&mode!=='debug'?'example':'case '+(i+1)} failure`:'Inspect output'}</summary><pre>${esc(r.argumentsJSON!==undefined?'Arguments: '+r.argumentsJSON+'\n':r.arguments!==undefined?'Arguments: '+r.arguments+'\n':'')}${esc(r.expectedJSON!==undefined?'Expected: '+r.expectedJSON+'\n':r.expected!==undefined?'Expected: '+r.expected+'\n':'')}${esc(r.error||'Returned: '+r.actual)}</pre>${errorLineButton(r.errorLine)}</details>`:''}</div>`).join('')}${stdout}`;
}
function revisionRows(items){return `<div class="panel revision-list">${items.map(q=>`<a class="row" href="${revisionHref(q)}"><div><span class="row-title">${esc(q.title)}</span><span class="row-meta">${esc(q.topic)} · ${q.difficulty} · ${q.minutes} min · ${questionState(q.id).due<=Date.now()?'Due ':'Scheduled '}${esc(dateLabel(questionState(q.id).due))}</span>${statusHTML(q.id)}</div><span class="row-arrow" aria-hidden="true">↗</span></a>`).join('')}</div>`;}
function review(){
  const due=dueQuestions(),upcoming=content.questions.filter(q=>questionState(q.id).due>Date.now()).sort((a,b)=>questionState(a.id).due-questionState(b.id).due);
  return header('Retention / Revision','Revision queue','Wrong answers and reviewed solutions return after one day. Successful checks default to three days; choose a longer interval when you can explain the answer comfortably.')+`<div class="section-title"><h2>Due now</h2><span class="mono">${due.length} ${due.length===1?'PROBLEM':'PROBLEMS'}</span></div>${due.length?revisionRows(due):`<div class="panel empty empty-state">${icon("review")}<h3>${upcoming.length?'Nothing due today':'Your revision queue is empty'}</h3><p>${upcoming.length?'Your scheduled practice is below. You can revisit it early or continue your learning route.':'Attempt an interview problem or schedule one below its answer panel.'}</p><a class="btn" href="#questions">Choose a problem ↗</a></div>`}<div class="section-title"><h2>Coming up</h2><span class="mono">${upcoming.length} SCHEDULED</span></div>${upcoming.length?revisionRows(upcoming):'<div class="panel empty">No scheduled revisions.</div>'}`;
}
function trainerHistory(sessions){
  if(!sessions.length)return '<div class="empty">Your first session will appear here.</div>';
  const ordered=[...sessions].reverse(),row=s=>{const known=trainerTypes.find(t=>t.id===s.type),tag=known?'a':'div';return `<${tag} class="row"${known?` href="#trainers/${esc(s.type)}/round/${esc(roundKey(s))}"`:''}><div><span class="row-title">${esc(known?.name||s.type)}</span><span class="row-meta">${dateLabel(s.date)} · ${s.finished?'FINISHED':'STOPPED'} · ${s.level.toUpperCase()}</span><div class="small muted">${s.correct}/${s.attempts} correct · ${s.elapsed}s · ${s.attempts&&s.elapsed?Math.round(s.correct*60/s.elapsed):'—'} correct/min</div></div>${known?'<span class="row-arrow" aria-hidden="true">↗</span>':''}</${tag}>`;};
  return ordered.slice(0,10).map(row).join('')+(ordered.length>10?`<details class="trainer-history-older"><summary>Show earlier rounds · ${ordered.length-10}</summary><div>${ordered.slice(10).map(row).join('')}</div></details>`:'');
}
function progress(){const sessions=state.trainers||[];return header('Your record','Progress & data','')+statGrid()+`<div class="progress-grid"><section><div class="section-title"><h2>Interview practice by topic</h2></div><div class="panel">${[...new Set(content.questions.map(q=>q.topic))].map(topic=>{const qs=content.questions.filter(q=>q.topic===topic),solved=qs.filter(q=>questionState(q.id).solved||questionState(q.id).selfSolved).length;return `<div class="progress-topic"><div class="meta"><span>${esc(topic)}</span><span class="muted">${solved} / ${qs.length} passed</span></div><meter value="${solved}" max="${qs.length}" aria-label="${esc(topic)} completion"></meter></div>`;}).join('')}</div></section><section><div class="section-title"><h2>Trainer history</h2><span class="mono">${sessions.length} SESSIONS</span></div><div class="panel">${trainerHistory(sessions)}</div><div class="section-title"><h2>Backup & restore</h2></div><div class="panel"><div class="panel-pad"><p class="small muted">${QA?'Test records stay in this browser. Exports are labelled as test previews and cannot be imported into personal progress.':'Progress and drafts are saved in this browser and backed up to the local project folder. Export a copy to move browsers or keep an extra backup.'}</p></div><div class="data-actions"><a class="btn" id="export-link" download>Export progress ↓</a><button class="btn" type="button" data-action="choose-import">Import progress ↑</button><input type="file" id="import-file" accept="application/json,.json" class="hidden"></div>${importFeedback?`<p class="import-feedback" role="status">${esc(importFeedback)}</p>`:''}${syncReview()}${backupReview()}${recoveryControl()}${tabCopyControl()}${otherTabCopies()}</div></section></div>`;}

// Arithmetic parser: no eval, no script execution, fractions and percentages supported.
function numberAnswer(raw){
  const source=raw.replace(/\s/g,'').replace(/[×]/g,'*').replace(/[÷]/g,'/').replace(/[−]/g,'-');
  if(!source||source.length>120||/[^0-9.eE+\-*/^()%]/.test(source))throw Error('Enter a number, fraction, percentage, or arithmetic expression.');
  const tokens=source.match(/(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?|[+\-*/^()%]/g)||[];
  if(tokens.join('')!==source)throw Error('Check the expression.');
  let i=0;
  function atom(){let value;if(tokens[i]==='('){i++;value=add();if(tokens[i++]!==')')throw Error('Close the parentheses.');}else{value=Number(tokens[i++]);if(!Number.isFinite(value))throw Error('Expected a number.');}if(tokens[i]==='%'){i++;value/=100;}return value;}
  function unary(){if(tokens[i]==='+'){i++;return unary();}if(tokens[i]==='-'){i++;return -unary();}return power();}
  function power(){let value=atom();if(tokens[i]==='^'){i++;value=Math.pow(value,unary());}return value;}
  function mul(){let value=unary();while(tokens[i]==='*'||tokens[i]==='/'){const op=tokens[i++],next=unary();value=op==='*'?value*next:value/next;}return value;}
  function add(){let value=mul();while(tokens[i]==='+'||tokens[i]==='-'){const op=tokens[i++],next=mul();value=op==='+'?value+next:value-next;}return value;}
  const result=add();if(i!==tokens.length||!Number.isFinite(result))throw Error('Check the expression; it must give a finite number.');return result;
}
function bindPage(){

  ['search','difficulty','topic','path','status'].forEach(name=>{const el=$('#'+name);if(el)el.addEventListener(name==='search'?'input':'change',()=>{filters[name]=el.value;refreshCollection();});});
  const q=content.questions.find(q=>route[0]==='questions'&&q.id===route[1]);
  if(q){
    const saveDraft=(id,el)=>el?.addEventListener('input',()=>{state.drafts[id]=el.value;touch();});
    saveDraft(q.id,$('#answer'));saveDraft(q.id+'-scratch',$('#scratchpad'));
    if(q.type==='structured'){
      $('#answer-form').addEventListener('input',event=>{
        if(!event.target.dataset.check)return;
        const draft=objectiveDraft(q),check=q.checks.find(c=>c.id===event.target.dataset.check);
        if(!check)return;
        if(check.type==='numeric')draft[check.id]=event.target.value;
        else draft[check.id]=[...$('#answer-form').querySelectorAll('input[data-check="'+check.id+'"]:checked')].map(el=>el.value);
        state.drafts[objectiveDraftKey(q)]=JSON.stringify(draft);touch();
      });
    }
    $('#answer-form').addEventListener('submit',event=>{
      event.preventDefault();retainFormFocus(event);
      const s=state.questions[q.id]||={},v=view[q.id]||={};
      try{
        let result;
        if(q.type==='structured'){
          // Read current controls at submit too: autofill and restored forms
          // need not have emitted an input event.
          const answers={};
          for(const check of q.checks)answers[check.id]=check.type==='numeric'?$('#check-'+check.id).value:[...$('#answer-form').querySelectorAll('input[data-check="'+check.id+'"]:checked')].map(el=>el.value);
          state.drafts[objectiveDraftKey(q)]=JSON.stringify(answers);
          result=gradeObjective(q,answers);
          if(!result.complete){v.feedback=result.message;v.feedbackClass='bad';touch();render();announce(v.feedback);return;}
        }else{
          const answer=$('#answer').value;state.drafts[q.id]=answer;
          result={correct:Math.abs(numberAnswer(answer)-q.answer)<=q.tolerance};
        }
        s.attempts=(s.attempts||0)+1;
        if(result.correct){
          if(!s.assisted){s.solved=true;if(q.type==='structured')s.assessmentVersion=q.assessmentVersion;}else s.reviewed=true;
          s.correct=(s.correct||0)+1;s.last=Date.now();s.due=Date.now()+(s.assisted?1:3)*86400000;
          v.feedback=s.assisted?'Correct with assistance. Saved as reviewed; try again closed-book on revision.':q.type==='structured'?'All checkpoints correct. Unaided pass recorded.':'Correct. Unaided solve recorded. Now test your reasoning with the follow-up.';v.feedbackClass='good';
        }else{
          s.due=Date.now()+86400000;v.feedback=q.type==='structured'?'Not yet. '+result.matched+' of '+result.total+' checkpoints matched. Recheck the calculations and every selected statement.':'Not quite. Recheck the sample space, assumptions, and algebra. A hint is available when you need it.';v.feedbackClass='bad';
        }
        touch();render();announce(v.feedback);
      }catch(error){v.feedback=error.message;v.feedbackClass='bad';touch();render();announce(error.message);}
    });
  }
  const l=content.lessons.find(l=>route[0]==='courses'&&l.id===route[1]);
  if(l)authoredLesson(l)?.bind?.($('#page'),typesetMath);
  if(l)$('#quiz-form').addEventListener('submit',event=>{event.preventDefault();retainFormFocus(event);const raw=new FormData(event.target).get('option');if(raw===null){notify('Choose an answer before checking.');return;}const option=Number(raw);if(!Number.isInteger(option)||option<0||option>=l.options.length)return;const passed=option===l.correct;view[l.id]={passed,choice:option,message:passed?'Correct. '+l.explanation:'Not quite. Return to the key idea and try another answer.'};if(passed){state.lessons[l.id]={passed:true,date:Date.now()};touch();}render();announce(view[l.id].message);});
  const c=coding.find(c=>route[0]==='coding'&&c.id===route[1]);
  if(c){
    $('#page').addEventListener('keydown',event=>{if(event.target.closest?.('.python-workspace'))handleCodingShortcut(event,c);});
    for(const [selector,field] of [['#debug-arguments','argumentsJSON'],['#debug-expected','expectedJSON'],['#debug-enabled','enabled']]){
      $(selector)?.addEventListener(field==='enabled'?'change':'input',event=>{const record=debugCases(c),selected=record.cases.find(t=>t.id===record.selected);if(!selected)return;selected[field]=field==='enabled'?event.target.checked:event.target.value;saveDebugCases(c,record);debugError(c,'');updateRunnerDraftNote(c.id);if(field==='enabled')render();});
    }
    if(typeof QuantPythonEditor!=='undefined'){
      codeEditor=QuantPythonEditor.mount({parent:$('#code-host'),id:c.id,
        value:state.drafts[c.id]??c.starter,status:$('#editor-position'),
        onChange:value=>{state.drafts[c.id]=value;touch();updateRunnerDraftNote(c.id);},
        onShortcut:event=>handleCodingShortcut(event,c),
        onExit:backwards=>{const target=(backwards?null:$('#page .editor-actions button:not(:disabled)'))||$('#page [data-action="editorial"]');if(!target)return false;target.focus();return true;}});
    }else{
      // A plain input remains usable if the bundled editor cannot load.
      $('#code').addEventListener('input',()=>{state.drafts[c.id]=$('#code').value;touch();updateRunnerDraftNote(c.id);});
      $('#editor-help').textContent='Plain editor · reload to restore syntax highlighting';
    }
  }
  $('#page').addEventListener('click',async event=>{
    const button=event.target.closest('[data-action]');if(!button)return;const action=button.dataset.action;
    if(!pageFocus())button.focus?.({preventScroll:true});
    if(action==='reset-filters'){filters=emptyFilters();for(const name of ['search','difficulty','topic','path','status']){const el=$('#'+name);if(el)el.value=filters[name];}refreshCollection();$('#search')?.focus({preventScroll:true});announce('Filters cleared. Full library restored.');return;}
    if(q){const s=state.questions[q.id]||={},v=view[q.id]||={};
      if(action==='legacy-reasoning'){v.legacy=!v.legacy;if(v.legacy)s.assisted=true;}
      if(action==='hint'){s.hints=Math.min((s.hints||0)+1,q.hints.length);s.assisted=true;}
      if(action==='solution'){s.reveal=!s.reveal;if(s.reveal)s.assisted=true;}
      if(action==='follow'){v.follow=!v.follow;if(v.follow)s.assisted=true;}
      if(action==='reviewed'){if(!state.drafts[q.id]?.trim()&&!state.drafts[objectiveDraftKey(q)]&&!s.reveal){notify('Attempt the problem or read its solution before recording a review.');return;}s.reviewed=true;s.last=Date.now();s.due=Date.now()+86400000;notify('Saved as reviewed. It returns tomorrow.');}
      if(action==='self-solved')return; // Retired: legacy records remain read-only.
      if(action==='new-attempt'){freshQuestionAttempt(q);announce(view[q.id].feedback);}
      if(action==='previous-attempt'){v.previous=!v.previous;if(v.previous)s.assisted=true;}
      if(action==='restore-attempt'){restoreQuestionAttempt(q);announce(view[q.id].feedback);}
      if(action==='schedule'){const days=Number($('#confidence').value);if(![1,3,7].includes(days))return;s.due=Date.now()+days*86400000;notify('Revision scheduled for '+dateLabel(s.due));announce('Revision scheduled for '+dateLabel(s.due));}
      touch();render();
      if(['new-attempt','restore-attempt'].includes(action)){const epoch=renderEpoch;frame(()=>{if(epoch===renderEpoch){const input=$('#answer')||$('#answer-form input');input?.focus({preventScroll:true});input?.scrollIntoView?.({block:'center'});}});}
    }
    if(c){
      const v=view[c.id]||={};
      if(action==='editorial'){v.editorial=!v.editorial;if(v.editorial)markEditorialRead(c.id);render();}
      if(action==='error-line'){const line=Number(button.dataset.line);if(Number.isInteger(line)&&line>0){if(codeEditor)codeEditor.goToLine(line);else{const editor=$('#code'),position=editor.value.split('\n').slice(0,line-1).join('\n').length+(line>1?1:0);editor.focus();editor.setSelectionRange(position,position);}}}
      if(action==='restore-starter'){if(codeEditor)codeEditor.replace(c.starter);else{state.drafts[c.id]=c.starter;touch();render();}}
      if(action==='add-debug-case')addDebugCase(c);
      if(action==='select-debug-case'){const record=debugCases(c);if(record.cases.some(t=>t.id===button.dataset.case)){record.selected=button.dataset.case;saveDebugCases(c,record);render();}}
      if(action==='remove-debug-case'){const record=debugCases(c),index=record.cases.findIndex(t=>t.id===record.selected);record.cases=record.cases.filter(t=>t.id!==record.selected);record.selected=record.cases[Math.min(index,record.cases.length-1)]?.id||'';saveDebugCases(c,record);debugError(c,'');render();$('#debug-arguments')?.focus({preventScroll:true});}
      if(action==='load-submission-cases')await loadSubmissionCases(c);
      if(action==='copy-submission-case'){const selected=v.officialCases?.[Number($('#submission-case')?.value)];if(selected)addDebugCase(c,selected,'Submission '+selected.caseNumber);}
      if(action==='debug-result-case'){const selected=v.result?.results?.[Number(button.dataset.index)];if(selected&&typeof selected.argumentsJSON==='string')addDebugCase(c,selected,(v.mode==='submit'?'Submission ':'Run ')+(selected.caseNumber||Number(button.dataset.index)+1));}
      if(action==='run-code'||action==='submit-code'){
        await startCodeCheck(c,action==='run-code'?'debug':'submit');
      }
    }

    if(action==='resolve-sync'){try{await browserWrites;await withProgressLock(resolveSyncConflict);render();announce(importFeedback);}catch(error){importFeedback=error.message;render();announce(error.message);}}
    if(action==='review-other-tab'){try{const copy=JSON.parse(localStorage.getItem(button.dataset.copyKey));if(copy.workspace!==(QA?'preview':'personal'))throw Error('This copy belongs to another workspace.');stageProgressImport({...copy[button.dataset.copyPart],workspace:copy.workspace},'Saved tab copy · '+new Date(copy.date).toLocaleString());if(copy.pending)pendingImport.pendingCopyKey=button.dataset.copyKey;render();focusBackupReview();}catch(error){notify(error.message);}}
    if(action==='review-tab-local'||action==='review-tab-remote'){try{const copy=JSON.parse(localStorage.getItem(CONFLICT_KEY));if(copy.workspace!==(QA?'preview':'personal'))throw Error('This copy belongs to another workspace.');stageProgressImport({...copy[action==='review-tab-local'?'local':'remote'],workspace:QA?'preview':'personal'},action==='review-tab-local'?'Previous tab copy':'Previous saved copy');render();focusBackupReview();}catch(error){notify(error.message);}}
    if(action==='choose-import')$('#import-file')?.click();
    if(action==='cancel-import'){pendingImport=null;render();frame(()=>document.querySelector('[data-action="choose-import"]')?.focus({preventScroll:true}));}
    if(action==='review-recovery'){const recovery=readRecovery();if(!recovery){notify('No valid previous record is available.');return;}stageProgressImport({...recovery.state,workspace:recovery.workspace},'Previous record · '+new Date(recovery.date).toLocaleString());render();focusBackupReview();}
    if(action==='apply-import'){try{await browserWrites;await withProgressLock(replaceProgressFromImport);render();announce(importFeedback);frame(()=>document.querySelector('[data-action="review-recovery"]')?.focus({preventScroll:true}));}catch(error){importFeedback=error.message;render();announce(error.message);}}

    if(action==='start-trainer')startTraining(route[1]);
    if(action==='stop-trainer')endTraining(false);
    if(action==='skip-trainer')answerTraining(true);
  });
  if($('#export-link')){
    const link=$('#export-link');link.textContent='Preparing backup…';
    fetch('/api/export',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(progressExport())})
      .then(async response=>{if(!response.ok)throw Error('Export failed');return response.json();})
      .then(data=>{if(link.isConnected){link.href=data.url;link.download=(QA?'quant-atelier-test-preview-':'quant-atelier-progress-')+new Date().toISOString().slice(0,10)+'.json';link.textContent='Export progress ↓';}})
      .catch(()=>{if(link.isConnected){link.textContent='Export unavailable';notify('Restart the local server to download a backup. Your browser copy is still saved.');}});
  }
  if($('#import-file'))$('#import-file').addEventListener('change',async event=>{
    const file=event.target.files[0];if(!file)return;
    try{if(file.size>2_000_000)throw Error('File too large.');stageProgressImport(JSON.parse(await file.text()),file.name);render();focusBackupReview();announce('Backup ready to review. Current progress has not changed.');}
    catch(error){importFeedback=error.message;render();announce(error.message);}
    finally{event.target.value='';}
  });
  if($('#trainer-form'))$('#trainer-form').addEventListener('submit',event=>{event.preventDefault();answerTraining(false);});
  $('#trainer-answer')?.addEventListener('input',event=>{if(training){training.answer=event.target.value;checkpointTraining();}});
}

const trainerTypes=[
  {id:'math',name:'Mental arithmetic',topic:'Numerical',description:'Addition, subtraction, multiplication, division, percentages, and fractions. Develop speed without trading away accuracy.'},
  {id:'fractions',name:'Fractions to decimals',topic:'Numerical',description:'Make useful fraction conversions automatic. Repeating decimals are accepted within 0.0001.'},
  {id:'probability',name:'Probability sprint',topic:'Probability',description:'Small, generated sample-space problems. Dice, coins, and sampling without replacement, at a deliberate pace.'},
  {id:'sequences',name:'Sequence patterns',topic:'Numerical',description:'Find the next term under a stated pattern family. Arithmetic and geometric progressions, then changing differences.'},
  {id:'pricing',name:'Dice fair value',topic:'Trading',description:'Update an expected payoff as information arrives. Price conditional dice outcomes without relying on the unconditional mean.'}
];
let training=null,trainerInterval=null,lastSession=null;
function roundKey(round){
  if(typeof round.id==='string'&&round.id)return round.id;
  let hash=2166136261;for(const c of stableValue(round))hash=Math.imul(hash^c.charCodeAt(0),16777619);
  return 'saved-'+(hash>>>0).toString(36);
}
function trainerEndLabel(round){return !round.attempts?'No attempts':round.finished?'Round complete':round.reason==='reloaded'?'Round interrupted':round.reason==='left'?'Round ended when you left':'Round ended early';}
function checkpointTraining(){
  if(!training)return;
  try{sessionStorage.setItem(TRAINING_KEY,JSON.stringify({workspace:QA?'preview':'personal',active:true,at:Date.now(),round:training}));}
  catch{training.recoveryUnavailable=true;}
}
function keepTrainerResult(round){
  if(!round.attempts)return false;
  if(!state.trainers.some(s=>roundKey(s)===roundKey(round))){state.trainers.push(round);state.trainers=state.trainers.slice(-200);touch();}
  return true;
}
function trainingResult(t,finished,reason,at=Date.now()){
  const elapsed=Math.min(t.duration,Math.max(.1,(at-t.start)/1000));
  return {id:t.id,type:t.type,level:t.level,duration:t.duration,date:at,correct:t.correct,attempts:t.attempts,elapsed:Math.round(elapsed*10)/10,finished,reason,mistakes:t.mistakes.slice(-50),meanSeconds:t.latencies.length?t.latencies.reduce((x,y)=>x+y,0)/t.latencies.length:null};
}
function restoreTrainerSession(){
  try{
    const copy=JSON.parse(sessionStorage.getItem(TRAINING_KEY));if(!copy||copy.workspace!==(QA?'preview':'personal'))return;
    let round=copy.round;
    if(copy.active){
      if(!round||typeof round.id!=='string'||!trainerTypes.some(t=>t.id===round.type)||![60,120,180].includes(round.duration)||!Number.isFinite(round.start)||!Number.isFinite(round.end)||!Number.isFinite(copy.at)||copy.at<round.start||!Array.isArray(round.mistakes)||!Array.isArray(round.latencies)||!round.latencies.every(n=>Number.isFinite(n)&&n>=0))return;
      round=trainingResult(round,false,'reloaded',Math.min(copy.at,round.end));
    }
    if(!trainerTypes.some(t=>t.id===round?.type)||!validState({...fresh(),trainers:[round]}))return;
    lastSession=state.trainers.find(s=>roundKey(s)===roundKey(round))||round;
    keepTrainerResult(lastSession);
    sessionStorage.setItem(TRAINING_KEY,JSON.stringify({workspace:QA?'preview':'personal',active:false,round:lastSession}));
  }catch{}
}
function selectedTrainerResult(type){
  if(route[2]==='round')return state.trainers.find(s=>s.type===type&&roundKey(s)===route[3])||null;
  return lastSession?.type===type?lastSession:null;
}
function trainerTick(){
  if(!training)return;
  if(Date.now()>=training.end){endTraining(true);return;}
  if($('#timer'))$('#timer').textContent=Math.ceil((training.end-Date.now())/1000)+'s';
  if(!training.checkpointAt||Date.now()-training.checkpointAt>=1000){training.checkpointAt=Date.now();checkpointTraining();}
}
const rand=(a,b)=>Math.floor(Math.random()*(b-a+1))+a;
function exercise(type,level){
  const hard=level==='Hard',medium=level==='Medium',a=rand(hard?12:medium?5:2,hard?99:medium?30:15),b=rand(2,hard?35:medium?15:10);
  if(type==='math'){
    const op=rand(0,hard?5:medium?4:3);
    if(op===0)return {prompt:`${a} + ${b}`,answer:a+b};
    if(op===1)return {prompt:`${a} − ${b}`,answer:a-b};
    if(op===2)return {prompt:`${a} × ${b}`,answer:a*b};
    if(op===3)return {prompt:`${a*b} ÷ ${b}`,answer:a};
    if(op===4){const p=[5,10,12.5,15,20,25,40][rand(0,6)],n=rand(2,20)*20;return {prompt:`${p}% of ${n}`,answer:p*n/100};}
    return {prompt:`${a}/${b} + ${b}/${a}`,answer:a/b+b/a};
  }
  if(type==='fractions'){const denominators=hard?[7,9,11,12,16,32,64]:medium?[3,6,8,12,16,20]:[2,4,5,8,10];const d=denominators[rand(0,denominators.length-1)],n=rand(1,d-1);return {prompt:`${n} / ${d}`,answer:n/d,tolerance:.0001};}
  if(type==='sequences'){
    const start=rand(1,9),d=rand(2,8);
    if(!medium&&!hard)return {prompt:[0,1,2,3].map(i=>start+i*d).join(', ')+' , ?',answer:start+4*d,context:'Arithmetic progression'};
    if(!hard||Math.random()<.5){const ratio=rand(2,4);return {prompt:[0,1,2,3].map(i=>start*ratio**i).join(', ')+' , ?',answer:start*ratio**4,context:'Geometric progression'};}
    return {prompt:[0,1,2,3].map(i=>start+d*i*(i+1)/2).join(', ')+' , ?',answer:start+10*d,context:'Successive differences increase by a fixed amount'};
  }
  if(type==='probability'){
    if(!medium&&!hard){const n=rand(2,5);return {prompt:`Flip ${n} fair coins. Probability of all heads?`,answer:2**(-n),long:true};}
    if(!hard||Math.random()<.5){const red=rand(2,9),blue=rand(2,9);return {prompt:`${red} red and ${blue} blue balls. Draw two without replacement. Probability of different colours?`,answer:2*red*blue/((red+blue)*(red+blue-1)),long:true};}
    const total=rand(3,11),pairs=[];for(let i=1;i<=6;i++)for(let j=1;j<=6;j++)if(i+j===total)pairs.push([i,j]);const k=rand(2,5);return {prompt:`Two fair dice sum to ${total}. Conditional probability the first die is at least ${k}?`,answer:pairs.filter(p=>p[0]>=k).length/pairs.length,long:true};
  }
  if(type==='pricing'){
    if(!hard&&!medium){const n=rand(2,5),revealed=rand(1,n-1),values=Array.from({length:revealed},()=>rand(1,6));return {prompt:`Payoff is the sum of ${n} fair dice. ${revealed} revealed: ${values.join(', ')}. Expected total payoff?`,answer:values.reduce((x,y)=>x+y,0)+(n-revealed)*3.5,long:true};}
    if(medium){const revealed=rand(1,6);return {prompt:`Payoff is the maximum of two fair dice. One is revealed as ${revealed}; the other remains hidden. Expected payoff?`,answer:[1,2,3,4,5,6].reduce((sum,die)=>sum+Math.max(die,revealed),0)/6,long:true};}
    const cut=rand(6,10),pairs=[];for(let i=1;i<=6;i++)for(let j=1;j<=6;j++)if(i+j>=cut)pairs.push(i+j);return {prompt:`Payoff is the sum of two fair dice. You learn the sum is at least ${cut}. Conditional fair value?`,answer:pairs.reduce((x,y)=>x+y,0)/pairs.length,long:true};
  }
}
function trainers(){
  const t=trainerTypes.find(t=>t.id===route[1]);
  if(!t)return header('Practice / Trainers','Trainers','')+`<div class="card-grid trainer-grid">${trainerTypes.map((t,i)=>`<article class="card"><div class="card-art">${artwork(i)}</div><div class="card-body"><div class="eyebrow">${t.topic}</div><h3>${t.name}</h3><p>${t.description}</p><div class="card-foot"><span class="small muted">1–3 minute rounds</span><a class="btn primary" href="#trainers/${t.id}">Start ↗</a></div></div></article>`).join('')}</div>`;
  const result=selectedTrainerResult(t.id),base=`<div class="breadcrumbs"><a href="#trainers">Trainers</a><span>/</span><span>${t.name}</span>${route[2]==='round'?'<span>/</span><a href="#progress">Trainer history</a>':''}</div>`+header('A focused drill',t.name,t.description);
  if(route[2]==='round')return base+`${result?summaryHTML(result):'<div class="panel empty"><h3>This round is no longer in this record.</h3><p>History keeps the most recent 200 attempted rounds.</p></div>'}<div class="answer-buttons trainer-return"><a class="btn primary" href="#trainers/${t.id}">Start a new round →</a><a class="btn" href="#progress">Back to trainer history ↗</a></div>`;
  return base+`<div class="trainer-layout">${training?arena():`<section class="panel trainer-config"><div class="field"><label for="trainer-level">Difficulty</label><select id="trainer-level" class="select">${['Easy','Medium','Hard'].map(level=>`<option ${level===(result?.level||'Easy')?'selected':''}>${level}</option>`).join('')}</select></div><div class="field"><label for="trainer-duration">Duration</label><select id="trainer-duration" class="select">${[60,120,180].map(duration=>`<option value="${duration}" ${duration===(result?.duration||120)?'selected':''}>${duration/60} minute${duration===60?'':'s'}</option>`).join('')}</select></div><button class="btn primary" data-action="start-trainer">${result?'Begin another round':'Begin round'} →</button></section><p class="practice-note">Fractions and expressions are accepted. Accuracy includes wrong submissions and skips. Switching browser tabs keeps the timer running; leaving this trainer or reloading ends the round.</p>`}${result&&!training?summaryHTML(result):''}</div>`;
}
function arena(){const t=training;return `<section class="arena"><div class="arena-top"><span>${t.level.toUpperCase()} · ${t.correct} CORRECT / ${t.attempts} ATTEMPTS</span><span class="timer" id="timer">${Math.max(0,Math.ceil((t.end-Date.now())/1000))}s</span></div><div class="math-prompt ${t.current.long?'long':''}">${trainerMath(t.current.prompt)}</div>${t.current.context?`<div class="small muted">${esc(t.current.context)}</div>`:''}${t.recoveryUnavailable?'<p class="practice-note">Round recovery is unavailable in this browser. End the round before reloading to keep your attempts.</p>':''}<form id="trainer-form"><label for="trainer-answer">Your answer ${t.type==='fractions'?'· 4 decimal places or better':''}</label><input class="input" id="trainer-answer" value="${esc(t.answer||'')}" autocomplete="off" autofocus inputmode="decimal"><div class="answer-buttons"><button class="btn primary" type="submit">Check →</button><button class="btn" type="button" data-action="skip-trainer">Skip</button><button class="btn link" type="button" data-action="stop-trainer">End round</button></div></form><div class="feedback ${t.feedbackGood?'good':'bad'}">${esc(t.feedback||'')}</div></section>`;}
function startTraining(type){
  const level=$('#trainer-level').value,duration=Number($('#trainer-duration').value);
  if(!trainerTypes.some(t=>t.id===type)||!['Easy','Medium','Hard'].includes(level)||![60,120,180].includes(duration))return;
  if(training)return;
  const now=Date.now();training={id:tabID+'-'+now+'-'+Math.random().toString(36).slice(2),type,level,duration,start:now,end:now+duration*1000,current:exercise(type,level),questionStart:now,correct:0,attempts:0,mistakes:[],latencies:[]};
  lastSession=null;checkpointTraining();render();$('#trainer-answer').focus();clearInterval(trainerInterval);trainerInterval=setInterval(trainerTick,250);
}
function answerTraining(skip){if(!training)return;if(Date.now()>=training.end){endTraining(true);return;}const t=training,raw=$('#trainer-answer').value;let correct=false;
  if(!skip){try{correct=Math.abs(numberAnswer(raw)-t.current.answer)<=(t.current.tolerance||1e-6);}catch(error){t.answer=raw;t.feedback=error.message;t.feedbackGood=false;checkpointTraining();render();announce(error.message);$('#trainer-answer').focus();return;}}
  t.attempts++;
  if(correct){t.correct++;t.latencies.push((Date.now()-t.questionStart)/1000);t.feedback='Correct. Keep going.';t.feedbackGood=true;}
  else{t.mistakes.push({prompt:t.current.prompt,answer:t.current.answer,given:skip?'Skipped':raw});t.feedback=skip?`Previous problem skipped. Answer: ${Number(t.current.answer.toFixed(6))}.`:`Previous answer: ${Number(t.current.answer.toFixed(6))}. Saved for review.`;t.feedbackGood=false;}
  t.answer='';t.current=exercise(t.type,t.level);t.questionStart=Date.now();checkpointTraining();render();$('#trainer-answer').focus();
}
function endTraining(finished,show=true,reason=finished?'finished':'stopped'){
  if(!training)return;if(Date.now()>=training.end){finished=true;reason='finished';}clearInterval(trainerInterval);lastSession=trainingResult(training,finished,reason);training=null;
  try{sessionStorage.setItem(TRAINING_KEY,JSON.stringify({workspace:QA?'preview':'personal',active:false,round:lastSession}));}catch{}
  keepTrainerResult(lastSession);
  if(show){render();const heading=$('.trainer-summary h2'),epoch=renderEpoch;heading?.setAttribute('tabindex','-1');frame(()=>{if(epoch!==renderEpoch)return;heading?.focus({preventScroll:true});heading?.scrollIntoView({block:'nearest'});});announce(`${trainerEndLabel(lastSession)}. ${lastSession.attempts?lastSession.correct+' correct out of '+lastSession.attempts+' attempts.':'No practice result was recorded.'}`);}
}
function summaryHTML(s){
  const attempted=s.attempts>0;
  return `<section class="panel trainer-summary"><div class="eyebrow">${trainerEndLabel(s)} · ${s.elapsed}s elapsed</div><h2>${attempted?s.correct+' correct. Review the round.':'Ready when you are.'}</h2>${!attempted?'<p class="practice-note">No answers or skips were submitted. This round adds no history or completed drill.</p>':''}${s.reason==='reloaded'?'<p class="practice-note">Recovered the last saved part of this round. The timer stopped; start a new round when you are ready.</p>':s.reason==='left'?'<p class="practice-note">Leaving this trainer ends the round. Your submitted attempts are kept below.</p>':''}<div class="mini-stats"><div><span class="num">${attempted?Math.round(s.correct/s.attempts*100)+'%':'—'}</span><span class="small muted">Accuracy</span></div><div><span class="num">${attempted&&s.elapsed?Math.round(s.correct*60/s.elapsed):'—'}</span><span class="small muted">Correct / minute</span></div><div><span class="num">${s.meanSeconds===null?'—':s.meanSeconds.toFixed(1)+'s'}</span><span class="small muted">Mean correct-response time</span></div></div>${attempted?`<div class="eyebrow">Mistakes to revisit</div>${s.mistakes.length?s.mistakes.map(m=>`<div class="mistake">${trainerMath(m.prompt)}<div class="small muted">Your answer: ${esc(m.given)} · Correct: ${Number(m.answer.toFixed(6))}</div></div>`).join(''):'<p class="practice-note">No mistakes recorded in this round.</p>'}`:''}</section>`;
}

async function init(){
  try{
    const responses=await Promise.all([fetch('/content.json',{cache:'no-store'}),fetch('/coding.json',{cache:'no-store'})]);[content,coding]=await Promise.all(responses.map(r=>r.json()));
    try{const local=JSON.parse(localStorage.getItem(KEY));if(validWorkspaceState(local))state={...fresh(),...local};}catch{}
    browserBase=cloneRecord(state);
    try{const copy=JSON.parse(localStorage.getItem(CONFLICT_KEY));if(copy&&!copy.resolved&&Array.isArray(copy.conflicts)&&copy.conflicts.every(c=>['questions','coding','lessons','drafts','preferences'].includes(c.group)&&typeof c.id==='string')&&copy.workspace===(QA?'preview':'personal')&&validWorkspaceState(copy.local)&&validWorkspaceState(copy.remote)){syncConflict=copy;state=copy.local;saved='Changes need review';}}catch{}
    await restorePendingWrite();
    if(!QA){try{
      const response=await fetch('/api/progress');if(!response.ok)throw Error('Backup unavailable');
      const data=await response.json(),disk=validWorkspaceState(data.state)?data.state:null;diskRevision=data.revision??null;diskBase=cloneRecord(disk||fresh());
      if(!syncConflict&&disk&&disk.updatedAt>state.updatedAt){state={...fresh(),...disk};localStorage.setItem(KEY,JSON.stringify(state));}
      if(syncConflict&&disk)receiveExternal(disk,syncConflict.remote);
      browserBase=cloneRecord(storedProgress()||state);saved=syncConflict?'Changes need review':'Saved locally';
      if(!syncConflict&&state.updatedAt>(disk?.updatedAt||0))await flush();
    }catch{saved='Browser saved · disk unavailable';}}
    else saved=syncConflict?'Changes need review':'Test records · browser only';
    restoreTrainerSession();
    restoreRunnerResults();
    try{history.scrollRestoration='manual';}catch{}
    window.addEventListener('hashchange',navigatePage);
    window.addEventListener('storage',handleStorageChange);
    $('#app').addEventListener?.('click',event=>{
      const link=event.target.closest?.('a[href^="#"]');
      if(link?.classList.contains('skip-link')){event.preventDefault();skipToPractice();return;}
      if(link&&link.getAttribute('href')==='#progress/reconcile'&&location.hash==='#progress/reconcile'){event.preventDefault();const heading=$('#sync-review-title');heading?.focus({preventScroll:true});heading?.scrollIntoView({block:'center'});}
      if(link&&link.getAttribute('href')!==location.hash&&$('#page')?.contains?.(link))departingFocus=linkFocus(link);
    });
    window.addEventListener('scroll',()=>{clearTimeout(scrollTimer);scrollTimer=setTimeout(()=>{if(renderedHash===(location.hash||'#dashboard'))captureNavigation();},150);},{passive:true});
    document.addEventListener('visibilitychange',()=>{if(document.visibilityState==='visible'&&training&&Date.now()>=training.end)endTraining(true);});
    window.addEventListener('pagehide',()=>{suspendRunnerChecks();captureNavigation();if(training)endTraining(false,false,'reloaded');if(!QA&&!syncConflict&&diskRevision!==undefined)navigator.sendBeacon('/api/progress',new Blob([JSON.stringify({state,revision:diskRevision})],{type:'application/json'}));});
    window.addEventListener('pageshow',event=>{if(event.persisted){restoreRunnerResults();render();restoreNavigation();}});
    filters={...emptyFilters(),...(navigation[location.hash||'#dashboard']?.filters||{})};
    render();restoreNavigation();
  }catch(error){$('#app').innerHTML='<p class="loading">The practice library could not load. Start the local server and reload this page.'+(QA?' '+esc(error.message):'')+'</p>';console.error(error);}
}
init();
