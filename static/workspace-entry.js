'use strict';
// A URL, bookmark or restored tab never grants access to the development workspace.
// Only the development launcher supplies a short-lived, single-use entry ticket.
var QuantAtelierWorkspace = {preview:false};
(() => {
  const ticketKey='quant-atelier-preview-entry';
  const params=new URLSearchParams(location.search);
  const personalURL=()=>{
    const query=new URLSearchParams(location.search);
    query.delete('qa');
    return location.pathname+(query.toString()?'?'+query.toString():'')+location.hash;
  };
  // Back/Forward cache restores skip script execution; revoke preview on restoration too.
  window.addEventListener('pageshow',event=>{
    if(event.persisted && QuantAtelierWorkspace.preview){
      QuantAtelierWorkspace.preview=false;
      event.stopImmediatePropagation();
      location.replace(personalURL());
    }
  });
  let ticket=null;
  try {
    ticket=JSON.parse(sessionStorage.getItem(ticketKey));
    sessionStorage.removeItem(ticketKey);
  } catch { /* Unavailable storage defaults to personal practice. */ }
  const destination=location.pathname+location.search+location.hash;
  const age=Date.now()-ticket?.at;
  if(params.get('qa')==='1' && ticket?.destination===destination && age>=0 && age<10000){
    QuantAtelierWorkspace.preview=true;
    return;
  }
  if(!params.has('qa'))return;
  const personal=personalURL();
  try { history.replaceState(history.state,'',personal); }
  catch { location.replace(personal); }
})();
