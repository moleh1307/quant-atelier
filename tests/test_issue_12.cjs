'use strict';
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const bank=JSON.parse(fs.readFileSync('static/content.json')),codes=JSON.parse(fs.readFileSync('static/coding.json')),requests=[],nodes={'#runner-notice':{innerHTML:''}};
const ctx={console,Math,Date,AbortController,URLSearchParams,setTimeout,clearTimeout,location:{search:'?qa=1',hash:'#coding/c01/journey/researcher/l01'},document:{querySelector:s=>nodes[s]||null},window:{},sessionStorage:{getItem:()=>null,setItem(){}},localStorage:{getItem:()=>null,setItem(){}},fetch:()=>new Promise(resolve=>requests.push(resolve)),bank,codes};
vm.createContext(require('./workspace-fixture.cjs')(ctx));const run=s=>vm.runInContext(s,ctx);run(fs.readFileSync('static/app.js','utf8').replace(/init\(\);\s*$/,''));run('content=bank;coding=codes;state=fresh();touch=()=>{};announce=()=>{};render=()=>{throw Error("Late result must not rebuild destination");};');
run(`state.drafts.c01='source code draft';state.drafts.c_l01_medium='destination code draft';state.drafts['c01-tests']=JSON.stringify({selected:'a',cases:[{id:'a',label:'Custom A',argumentsJSON:'[[1,2],3]',expectedJSON:'1',enabled:false},{id:'b',label:'Custom B',argumentsJSON:'[[2,2],4]',expectedJSON:'1',enabled:true}]});`);
const before=run('JSON.stringify(state)');let transitions=0,details=0;
for(const path of ['researcher','trader'])for(const l of bank.lessons.filter(l=>l.path==='shared'||l.path===path)){
 run('route='+JSON.stringify(['coding-list',l.id,'journey',path,l.id]));
 const list=run("topicPracticePage('coding')"),hrefs=[...list.matchAll(/class="topic-practice-row"[^>]*href="([^"]+)"/g)].map(m=>m[1]);assert.equal(hrefs.length,l.coding.length);
 for(let i=0;i<hrefs.length;i++){
  run('route='+JSON.stringify(hrefs[i].slice(1).split('/')));const html=run('moduleContinuation(moduleContext())'),next=[...html.matchAll(/data-next-coding href="([^"]+)"/g)].map(m=>m[1]);
  assert.deepEqual(next,i+1<hrefs.length?[hrefs[i+1]]:[],`${path}/${l.id}/${i}`);assert.ok(html.includes(`#coding-list/${l.id}/journey/${path}/${l.id}`));assert.ok(html.includes(`#paths/${path}/step-${l.id}`));assert.doesNotMatch(html,/data-next-question/);assert.equal(run('followingActivity(moduleContext()).kind'),'coding-list');assert.equal(run('JSON.stringify(state)'),before,'Navigation cannot alter drafts/tests/inclusion or award credit');
  if(next.length){assert.match(html,/class="btn primary compact" data-next-coding/);transitions++;}else assert.doesNotMatch(html,/Next coding exercise/);
  details++;
 }
}
// Deliberately reverse authored IDs: Next must follow the rendered difficulty
// groups rather than raw IDs, the global bank or current acceptance state.
run("content.lessons[0].coding=['c_l01_hard','c_l01_medium','c01'];route=['coding-list','l01','journey','trader','l01'];");const hrefs=[...run("topicPracticePage('coding')").matchAll(/class="topic-practice-row"[^>]*href="([^"]+)"/g)].map(m=>m[1]);assert.deepEqual(hrefs,['#coding/c01/journey/trader/l01','#coding/c_l01_medium/journey/trader/l01','#coding/c_l01_hard/journey/trader/l01']);
run("route=['coding','c01','journey','trader','l01'];state.coding.c_l01_medium={accepted:true};");assert.equal(run('nextModuleCoding(moduleContext()).id'),'c_l01_medium','Accepted exercise is still next');run("route=['coding','c_l01_medium','journey','trader','l01'];");assert.equal(run('nextModuleCoding(moduleContext()).id'),'c_l01_hard');
for(const route of [['coding','c01'],['coding','c01','journey','trader','l24'],['coding','c01','journey','other','l01'],['coding','c_l31_easy','journey','trader','l31']]){run('route='+JSON.stringify(route));assert.equal(run('moduleContext()'),null);}
for(const route of [['courses','l01','journey','trader','l01'],['questions','q01','journey','trader','l01'],['coding-list','l01','journey','trader','l01']]){run('route='+JSON.stringify(route));assert.doesNotMatch(run('moduleContinuation(moduleContext())'),/data-next-coding/);}
run("route=['coding','c14','journey','researcher','l18'];");assert.equal(run('moduleContext().additional'),true);assert.equal(run('nextModuleCoding(moduleContext())'),null);assert.match(run('moduleContinuation(moduleContext())'),/Back to coding list/);
(async()=>{
 run("state=fresh();route=['coding','c01','journey','researcher','l01'];state.drafts.c_l01_medium='retained destination draft';");
 const pending=run('executeCode(coding.find(c=>c.id==="c01"),"submit","submitted source code")');assert.equal(requests.length,1);
 const link=run('nextModuleCoding(moduleContext()).href');assert.equal(link,'#coding/c_l01_medium/journey/researcher/l01');run('route='+JSON.stringify(link.slice(1).split('/')));ctx.location.hash=link;
 const destination=run('codeDetail(coding.find(c=>c.id==="c_l01_medium"))');assert.match(destination,/retained destination draft/);assert.match(run('runnerNotice()'),/Return to check/);assert.match(run('runnerNotice()'),/#coding\/c01\/journey\/researcher\/l01/);
 requests[0]({ok:true,json:async()=>({passed:1,total:1,elapsedMs:1,results:[{passed:true}]})});await pending;
 assert.equal(run('state.coding.c01.accepted'),true);assert.equal(run('state.coding.c_l01_medium'),undefined);assert.equal(run('state.drafts.c_l01_medium'),'retained destination draft');assert.equal(run('view.c01.unread'),true);assert.match(nodes['#runner-notice'].innerHTML,/View result/);assert.equal(run('route[1]'),'c_l01_medium');
 console.log(`Issue12: ${transitions} next links across ${details} coding details match actual grouped lists; both journeys, final/legacy boundaries, draft/test preservation and in-flight source ownership passed.`);
})().catch(error=>{console.error(error);process.exitCode=1;});
