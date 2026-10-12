'use strict';
// Component tests declare the workspace explicitly. Full startup admission is
// separately exercised by test_workspace_entry.cjs, including accidental QA URLs.
module.exports=context=>{
  context.QuantAtelierWorkspace={preview:new URLSearchParams(context.location?.search||'').get('qa')==='1'};
  return context;
};
