'use strict';
// Practice entry must preserve the bookmarked module and all earned records.
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const source=fs.readFileSync('static/app.js','utf8').replace(/init\(\);\s*$/,'');
let heading,trail,revision,topbar,focus='',attributes={};
const context={console,URLSearchParams,Math,Date,setTimeout,clearTimeout,
 location:{hash:'#questions/q01/journey/trader/l01',search:'?qa=1'},
 document:{querySelector:s=>s==='#page h1'?heading:s==='#page'?heading:s==='.module-trail'?trail:s==='.revision-context'?revision:s==='.topbar'?topbar:null},
 window:{scrollY:900,getComputedStyle:()=>({top:'53px'}),scrollTo(options){this.last=options;}}};
vm.createContext(require('./workspace-fixture.cjs')(context));vm.runInContext(source,context);const run=s=>vm.runInContext(s,context);
heading={setAttribute(k,v){attributes[k]=v;},focus(options){focus=options.preventScroll?'heading':'';},getBoundingClientRect:()=>({top:240})};
trail={getBoundingClientRect:()=>({height:104})};
const before=run('JSON.stringify(state)'),bookmark=context.location.hash;
run('skipToPractice()');assert.equal(focus,'heading');assert.equal(attributes.tabindex,'-1');assert.equal(context.window.last.top,965);assert.equal(context.window.last.behavior,'auto');
assert.equal(context.location.hash,bookmark);assert.equal(run('JSON.stringify(state)'),before);
trail=null;revision={getBoundingClientRect:()=>({height:80})};run('skipToPractice()');assert.equal(context.window.last.top,989);
revision=null;topbar={getBoundingClientRect:()=>({height:53})};run('skipToPractice()');assert.equal(context.window.last.top,1069);
heading=null;focus='';run('skipToPractice()');assert.equal(focus,'');
// Arrow entry reaches every menu item without trapping Tab or grading work.
let keyHandler,prevented=0;
const summary={},items=Array.from({length:9},(_,i)=>({focus(){focus='item-'+i;}}));
context.outline={open:false,querySelector:()=>summary,querySelectorAll:()=>items,addEventListener:(event,handler)=>keyHandler=handler};
run("bindOutlineKeys(outline,'[data-section]')");
function press(key,target=summary){keyHandler({key,target,preventDefault(){prevented++;}});}
press('ArrowDown');assert.equal(focus,'item-0');assert.equal(context.outline.open,true);
press('ArrowDown',items[0]);assert.equal(focus,'item-1');
press('End',items[1]);assert.equal(focus,'item-8');
press('ArrowDown',items[8]);assert.equal(focus,'item-8');
press('ArrowUp',items[8]);assert.equal(focus,'item-7');
press('Home',items[7]);assert.equal(focus,'item-0');
press('ArrowUp');assert.equal(focus,'item-8');
const handled=prevented;press('Tab',items[8]);press('ArrowDown',{});assert.equal(prevented,handled,'Unrelated keys and targets retain native behavior');
assert.equal(run('JSON.stringify(state)'),before);
// A recovery notice lands directly on the opened copies instead of losing the user in Progress.
let recoveryFocused=false,recoveryLocated=false;
const copyDisclosure={open:false,querySelector:()=>({focus(){recoveryFocused=true;}}),scrollIntoView(){recoveryLocated=true;}};
const previousQuery=context.document.querySelector;
context.document.querySelector=s=>s==='#tab-copy-history'?copyDisclosure:previousQuery(s);
context.location.hash='#progress/tab-copies';run('route=["progress","tab-copies"];restoreNavigation()');
assert.equal(copyDisclosure.open,true);assert.ok(recoveryFocused&&recoveryLocated);assert.equal(run('JSON.stringify(state)'),before);
// Header height/zoom must never place the bottom of a menu offscreen.
let menuTop=318,position='absolute';
const fitMenu={style:{},clientHeight:200,scrollTop:0,getBoundingClientRect:()=>({top:menuTop}),contains:item=>items.includes(item),querySelector:()=>items[0]};
context.fitOutline={open:true,querySelector:()=>fitMenu};
context.window.innerHeight=612;context.window.getComputedStyle=()=>({position});
run('fitOutlineMenu(fitOutline)');assert.equal(fitMenu.style.maxHeight,'280px');
menuTop=160;run('fitOutlineMenu(fitOutline)');assert.equal(fitMenu.style.maxHeight,'367.2px','Deep reading can reclaim available menu space');
position='fixed';menuTop=65;context.window.innerHeight=360;run('fitOutlineMenu(fitOutline)');assert.equal(fitMenu.style.maxHeight,'281px');
items[0].offsetTop=10;items[0].offsetHeight=40;items[8].offsetTop=410;items[8].offsetHeight=40;
context.document.activeElement=items[8];run('alignOutlineMenu(fitOutline)');assert.equal(fitMenu.scrollTop,330,'Opening with End keeps the focused item visible instead of recentering the current section');
context.fitOutline.open=false;context.window.innerHeight=1800;run('fitOutlineMenu(fitOutline)');assert.equal(fitMenu.style.maxHeight,'281px','Closed menus do not measure or change layout');
assert.equal(run('JSON.stringify(state)'),before);
// Check shipped foreground/background pairs, including small syntax text.
// Menu geometry listeners are removed when their activity page leaves.
const listeners=new Map();
context.window.addEventListener=(name,handler)=>listeners.set(name,handler);
context.window.removeEventListener=(name,handler)=>{assert.equal(listeners.get(name),handler);listeners.delete(name);};
const originalQuery=context.document.querySelector;
context.document.querySelector=s=>s==='#module-outline'?context.outline:s==='#page'?{addEventListener(){}}:originalQuery(s);
run('bindModuleTrail()');assert.equal(listeners.size,2);run('releaseModuleOutline()');assert.equal(listeners.size,0);
// This static palette check is not a browser accessibility certification.
const css=fs.readFileSync('static/style.css','utf8').replace(/\/\*[\s\S]*?\*\//g,'');
function property(selector,name){let result;for(const match of css.matchAll(/([^{}]+)\{([^{}]*)\}/g))if(match[1].split(',').map(s=>s.trim()).includes(selector))for(const p of match[2].split(';')){const colon=p.indexOf(':');if(p.slice(0,colon).trim()===name)result=p.slice(colon+1).trim();}return result;}
function luminance(hex){hex=hex.replace('#','');if(hex.length===3)hex=[...hex].map(x=>x+x).join('');assert.equal(hex.length,6);const rgb=hex.match(/../g).map(x=>parseInt(x,16)/255).map(v=>v<=.04045?v/12.92:((v+.055)/1.055)**2.4);return rgb[0]*.2126+rgb[1]*.7152+rgb[2]*.0722;}
function contrast(a,b){const x=luminance(a),y=luminance(b);return (Math.max(x,y)+.05)/(Math.min(x,y)+.05);}
const pairs=[['body','#f5f2ed'],['.muted','#e8eadc'],['.eyebrow','#e8eadc'],['.nav-link','#fbf9f5'],['.nav-link.active','#fbe9e0'],['.row-meta','#faf9f4'],['.activity-meta','#fbfaf6'],['.activity-marker','#fbe9e0'],['.reading p','#fbfaf6'],['.reading .intro','#fbfaf6'],['.practice-note','#faf9f4'],['.feedback','#f2e7d9'],['.feedback.good','#e8eedb'],['.feedback.bad','#f6e0d6'],['.badge.Medium','#efe6d2'],['.badge.Hard','#f3ded4'],['.badge.written','#e7e8e3'],['.select','#fbfaf6'],['.revision-context span','#f5f2ed'],['.revision-context a','#f5f2ed'],['.revision-receipt','#faf9f4'],['.editor-head','#ecede1'],['.code-host .cm-gutters','#f0f1e7'],['.footer','#f5f2ed'],['.skip-link','#414e37'],['.btn.primary','#c84220'],['.btn.dark','#414e37'],['input::placeholder','#fffdf8']];
let minimum=Infinity;for(const [selector,bg] of pairs){const color=property(selector,'color');assert.ok(color,selector+' foreground exists');const ratio=contrast(color,bg);minimum=Math.min(minimum,ratio);assert.ok(ratio>=4.5,`${selector} contrast ${ratio.toFixed(2)} against ${bg}`);}
const editor=fs.readFileSync('editor/editor.mjs','utf8');let syntaxCount=0;for(const match of editor.matchAll(/color: '(#[0-9a-f]{6})'/g)){assert.ok(contrast(match[1],'#fafbf4')>=4.5,'Small Python syntax remains readable: '+match[1]);syntaxCount++;}
// Test the shipped editor's keyboard escape without constructing an artificial editor.
vm.runInContext(editor.slice(editor.indexOf('export function exitKeys'),editor.indexOf('export function mount')).replace('export ',''),context);
const exits=[];context.exitCallback=backwards=>{exits.push(backwards);return true;};
const exitHandler=run('exitKeys(exitCallback)');let exitPrevented=0;
const exitEvent=(key,shiftKey=false)=>({key,shiftKey,preventDefault(){exitPrevented++;}});
assert.equal(exitHandler.keydown(exitEvent('Tab')),false,'Ordinary Tab retains indentation');
assert.equal(exitHandler.keydown(exitEvent('Escape')),true);assert.equal(exitHandler.keydown(exitEvent('Tab')),true);assert.deepEqual(exits,[false]);
exitHandler.keydown(exitEvent('Escape'));exitHandler.keydown(exitEvent('Tab',true));assert.deepEqual(exits,[false,true]);
exitHandler.keydown(exitEvent('Escape'));exitHandler.keydown(exitEvent('x'));assert.equal(exitHandler.keydown(exitEvent('Tab')),false);
exitHandler.keydown(exitEvent('Escape'));exitHandler.blur();assert.equal(exitHandler.keydown(exitEvent('Tab')),false);
const unavailable=run('exitKeys(()=>false)');unavailable.keydown(exitEvent('Escape'));assert.equal(unavailable.keydown(exitEvent('Tab')),false,'Missing external controls cannot trap focus');
assert.equal(run('JSON.stringify(state)'),before);
assert.ok(contrast(property('.input','border-color'),'#f5f2ed')>=3,'Form boundaries remain visible');
assert.equal(property('#page h1[tabindex="-1"]:focus-visible','outline'),'2px solid #b23b1d','Keyboard heading focus overrides ordinary programmatic-focus reset');
assert.equal(property('.module-menu button:focus','outline'),'2px solid #c84220','Programmatic arrow-key focus stays visible in native Safari');
assert.match(css,/@media\(max-height:600px\)[\s\S]*\.module-outline \.module-menu[^}]*position:fixed;[^}]*bottom:14px/);
console.log(`Bookmarked practice entry, measured module/revision/header offsets, unchanged credit, focus-ring specificity and ${pairs.length+syntaxCount} text contrast pairs passed (minimum UI ratio ${minimum.toFixed(2)}).`);
