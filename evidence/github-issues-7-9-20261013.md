# Coding workspace fixes: issues 7, 8 and 9

Verified 2026-10-13. Scope is presentation and local test-panel updates; source banks, curriculum, judge, official cases and grading/progress rules are unchanged.

## Fixes

- [#7](https://github.com/moleh1307/quant-atelier/issues/7): coding topic lists use a prominent completion marker, green passed row and explicit badge. Passed with editorial and passed without editorial use the original submission-time `acceptedAssisted`/fallback rules. Drafts, editorial-only work and not-started rows remain distinct and unfinished. Links, counts and originating module/legacy contexts remain intact.
- [#8](https://github.com/moleh1307/quant-atelier/issues/8): selecting a debugging case previously called the full `render()`, rebuilding the workspace. `selectDebugCase` now updates only existing field values, inclusion state and selected controls. Editor, output and form nodes stay mounted. Per-case textarea scroll is retained; selecting the same or an invalid case is a no-op. Inclusion toggles update locally too. Existing persistence of case selection/drafts remains; selection awards no practice evidence or check.
- [#9](https://github.com/moleh1307/quant-atelier/issues/9): summary receipts and individual cases explicitly show Passed, Failed, Error or Output only, using text, a marker and restrained state styling. Debugging success says completion unchanged; only successful full Submit says Exercise passed / Submission saved. Matching expected/returned values use neutral readable output. Inspect output, debug copies, printed output, line jumps and checked source remain available. Unasserted outputs say No assertions checked instead of a misleading 0/0 pass count.

Assets: `static/app.js`, `static/style.css`, `static/index.html`, cache version `issues-789-20261013-1`. No new library or service.

## Automated verification

All **28 frontend suites passed**. New `tests/test_coding_issue_fixes.cjs` exercises the actual case-select/include click/change handlers with rerender forbidden, checks stable editor/result references, preserved drafts/case scroll and no earned evidence, and tests all completion provenance and result variants. Existing Python-debug, runner safety, topic-list, synchronization, recovery, editor, accessibility, roadmap and math suites passed. An existing Draft in progress label expectation caught an incidental wording change; the original label was retained.

Result tests cover exact-set no-credit boundaries, plain output inspection, error escaping, source line jumps, accepted-assistance provenance and preserved links/counts. The Python/judge source and data banks were not changed, so this frontend task did not rerun the entire Python suite. Actual local Run/Submit endpoints were verified below.

## Native browser observations

Preferred Atlas IAB found no backend; native IAB controls were used. The existing local server was retained, with no restart needed for frontend changes. All developer grading and solution inspection occurred after explicit test-preview entry and verified notice. The user's Chrome study tab was not operated.

- On `c_l01_medium`, a long developer draft established internal editor scroll1961, cursorLn94/Col15 and one selection. Twelve rapid mouse activations and keyboard Space activation preserved these values and editor text. Page scroll stayed within one pixel of its initial position; source code performs no page-scroll operation on case selection. Unit handlers independently forbid remount/rerender.
- Custom whitespace in Example1 arguments survived switching. Example2's exclusion remained visible, the included count updated immediately, and code state remained stable. Existing runner text was byte-identical across subsequent case switching.
- Actual debug pass showed Debugging tests passed /1 of1, while module completion remained0/3. Incorrect expected output showed Tests failed / Failed. A ValueError showed Test error / Error and a line2 jump. Blank expected output inspected a return value and awarded no completion.
- Actual medium Submit passed9/9, then viewing its editorial retained Passed without editorial. Separate c01 editorial-assisted Submit passed5/5 and displayed Passed with editorial. These are preview verification records, not learner achievement.
- At390×844, passed/unfinished coding rows fit341px of usable content; editorial badges wrapped below titles, with no document overflow. Desktop debug success used a prominent green receipt and readable case badge/neutral output.
- A temporary static fixture doubled affected title/badge/result text (32px titles,26px badges,34px result heading and24px output) using the actual styles. At390px, rows and result blocks had no horizontal overflow or overlapping labels. This is enlarged-text layout verification, not a claim of native200% zoom or physical device testing. Fixture HTML/CSS were removed before commit, with no progress logic and synthetic states only.
- Final viewport override was reset. The delivered browser is the PERSONAL `#coding-list/l01/journey/researcher/l01`, without preview records or notice.

Screenshots: [successful debug case](issues789-debug-pass-desktop.png), [coding list with explicit preview notice](issues789-coding-list-mobile.png), [enlarged synthetic result](issues789-enlarged-result.png). The latter two explicitly identify development/synthetic states; none contain personal solution drafts.

## Personal-data integrity and limits

A fresh pre-edit disk baseline was retained privately. Personal bytes changed during the task through existing medium-code study activity; only that coding record/draft differed. Its draft differs from the developer reference and contains none of the developer continuity comments. Personal debugging-case records stayed unchanged despite developer whitespace/exclusion/output edits in preview. Questions, lessons and trainer records stayed equal. Concurrent work was retained without resetting, importing or restoring a historical baseline. The final personal view uses current learner records.

No private records, local baselines, fixture files, logs or exports are published. These checks establish the affected UI/interaction scope, not independent accessibility testing with a screen reader or universal browser performance. Add/remove/copy operations retain their prior behavior; this issue specifically fixes selecting existing cases and their inclusion settings.
