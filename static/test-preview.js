'use strict';
const previewDestination='/?qa=1'+(location.hash||'#dashboard');
document.getElementById('personal-entry').href='/'+(location.hash||'#dashboard');
document.getElementById('preview-entry').addEventListener('click',()=>{
  try {
    sessionStorage.setItem('quant-atelier-preview-entry',JSON.stringify({at:Date.now(),destination:previewDestination}));
    location.assign(previewDestination);
  } catch {
    document.getElementById('preview-entry-error').textContent='Test preview needs browser session storage. Your personal workspace is still available.';
  }
});
