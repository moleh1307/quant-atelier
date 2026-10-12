'use strict';
// Shared presentation primitives, not a prescribed teaching sequence.
// Each registered lesson owns its argument, section count, figures and models.
globalThis.QuantCourseLessons=(()=>{
 const lessons=new Map();
 const escape=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 // TeX is text inside HTML. Escape comparisons and alignment characters so
 // the browser cannot interpret a mathematical < as the start of a tag.
 const math=(tex,display=false)=>`${display?'\\[':'\\('}${escape(tex)}${display?'\\]':'\\)'}`;
 const equation=tex=>`<div class="atlas-formula-main">${math(tex,true)}</div>`;
 const paragraph=html=>`<p>${html}</p>`;
 const opening=(question,context)=>`<div class="atlas-opening"><p>${question}</p><p>${context}</p></div>`;
 const pause=(question,answer)=>`<details class="atlas-pause"><summary>${question}</summary><div class="atlas-reasoning">${answer}</div></details>`;
 const figure=(html,caption)=>`<figure class="course-figure">${html}<figcaption>${caption}</figcaption></figure>`;
 // Display-only highlighting for small authored Python examples. This never
 // parses, runs or modifies a learner's editor draft.
 function python(source){
  const tokens=/#[^\n]*|"(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*'|\b(?:from|import|def|if|else|for|while|in|return|raise|None|True|False)\b|\b\d+(?:\.\d+)?\b/g;
  let html='',offset=0;
  for(const token of source.matchAll(tokens)){
   const value=token[0],kind=value.startsWith('#')?'comment':/^["']/.test(value)?'string':/^\d/.test(value)?'number':'keyword';
   html+=escape(source.slice(offset,token.index))+`<span class="course-code-${kind}">${escape(value)}</span>`;offset=token.index+value.length;
  }
  return `<pre class="course-code" tabindex="0" aria-label="Python example"><code>${html+escape(source.slice(offset))}</code></pre>`;
 }
 function register(id,lesson){
  if(lessons.has(id))throw Error('Duplicate authored lesson '+id);
  lesson.body=()=>lesson.opening+lesson.sections.map(([title,html],i)=>`<section class="lesson-section atlas-section" aria-labelledby="lesson-section-${i}"><div class="atlas-section-number" aria-hidden="true">${String(i+1).padStart(2,'0')}</div><h2 id="lesson-section-${i}" tabindex="-1">${escape(title)}</h2>${html}</section>`).join('')+`<section class="example atlas-worked" id="lesson-example" tabindex="-1" aria-label="A concrete example"><h2>${escape(lesson.exampleTitle)}</h2>${lesson.example}<p class="atlas-bridge">Take the check below, then continue with the linked practice in this module.</p></section>`;
  lessons.set(id,lesson);
 }
 return {register,get:id=>lessons.get(id),ids:()=>[...lessons.keys()],math,equation,paragraph,opening,pause,figure,escape,python};
})();
