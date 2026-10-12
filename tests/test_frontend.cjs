// Test the actual parser and generators without a browser or third-party package.
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const source=fs.readFileSync('static/app.js','utf8').replace(/init\(\);\s*$/,'');
const context={URLSearchParams,location:{search:''},document:{querySelector:()=>null},console,Math,Date,setTimeout,clearTimeout};
vm.createContext(require('./workspace-fixture.cjs')(context));vm.runInContext(source,context);
const parse=s=>vm.runInContext('numberAnswer('+JSON.stringify(s)+')',context);
for(const [input,value] of [['11/36',11/36],['28%',.28],['1-(5/6)^2',11/36],['2^-3',.125],['-2^2',-4],['(-2)^2',4],['1e-3',.001],['2×3',6],['.5+.25',.75]])assert.ok(Math.abs(parse(input)-value)<1e-10,input);
for(const input of ['', 'alert(1)','1/0','1..2','1+','(2*3','0/0','2;3','Infinity','1e999'])assert.throws(()=>parse(input),undefined,input);
assert.equal(vm.runInContext('validState(fresh())',context),true);
assert.equal(vm.runInContext('validState({...fresh(),drafts:{q01:42}})',context),false);
assert.equal(vm.runInContext('validState({...fresh(),trainers:[null]})',context),false);
assert.equal(vm.runInContext('validState({...fresh(),questions:{q01:null}})',context),false);
for(const type of ['math','fractions','probability','sequences','pricing']){
  for(const level of ['Easy','Medium','Hard']){
    for(let i=0;i<200;i++){
      const q=vm.runInContext(`exercise('${type}','${level}')`,context);
      assert.equal(typeof q.prompt,'string');assert.ok(Number.isFinite(q.answer));
      if(type==='probability')assert.ok(q.answer>=0&&q.answer<=1);
      if(type==='fractions')assert.ok(q.answer>0&&q.answer<1);
      if(type==='math')assert.ok(Math.abs(parse(q.prompt.replace(' of ','*'))-q.answer)<1e-7,q.prompt);
    }
  }
}
console.log('Parser checks and 3,000 generated trainer cases passed.');
