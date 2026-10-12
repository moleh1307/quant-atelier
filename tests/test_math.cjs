'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const root=path.join(__dirname,'..');
const katex=require(path.join(root,'static/vendor/katex/katex.min.js'));
let count=0;
function inspect(value){
  if(Array.isArray(value))return value.forEach(inspect);
  if(value&&typeof value==='object')return Object.values(value).forEach(inspect);
  if(typeof value!=='string')return;
  const expressions=[...value.matchAll(/\\\(([\s\S]*?)\\\)|\\\[([\s\S]*?)\\\]/g)];
  for(const match of expressions){
    const html=katex.renderToString(match[1]??match[2],{displayMode:match[2]!==undefined,throwOnError:true,strict:'error',trust:false,output:'htmlAndMathml'});
    assert.ok(html.includes('<math'),'Accessible MathML accompanies each formula');count++;
  }
  const plain=value.replace(/\\\([\s\S]*?\\\)|\\\[[\s\S]*?\\\]/g,'');
  assert.ok(!/\\[()[\]]/.test(plain),'No unbalanced math delimiters');
}
for(const bank of ['content','coding'])inspect(JSON.parse(fs.readFileSync(path.join(root,'static',bank+'.json'),'utf8')));
assert.ok(count>300);
const context={URLSearchParams,location:{search:''},console};vm.createContext(require('./workspace-fixture.cjs')(context));
vm.runInContext(fs.readFileSync(path.join(root,'static/app.js'),'utf8').replace(/init\(\);\s*$/,''),context);
const check=code=>vm.runInContext(code,context);
assert.equal(check("trainerMath('3 / 8')"),'\\(\\frac{3}{8}\\)');
assert.equal(check("trainerMath('1/2 + 3/4')"),'\\(\\frac{1}{2} + \\frac{3}{4}\\)');
assert.equal(check("trainerMath('Flip 3 fair coins. Probability of all heads?')"),'Flip 3 fair coins. Probability of all heads?');
assert.equal(check("trainerMath('<img src=x onerror=alert(1)>')"),'&lt;img src=x onerror=alert(1)&gt;');
for(let i=0;i<100;i++)for(const type of ['math','fractions','sequences'])for(const level of ['Easy','Medium','Hard']){
  context.testType=type;context.testLevel=level;
  const markup=check('trainerMath(exercise(testType,testLevel).prompt)');inspect(markup);
}
console.log(`${count} authored/generated math spans parse strictly; MathML, trainer notation and escaping checks passed.`);
