# GitHub issues 5 and 6

Verified 2026-10-13. Scope: [clipped Consecutive heads selection](https://github.com/moleh1307/quant-atelier/issues/5) and [unclear solved-question rows](https://github.com/moleh1307/quant-atelier/issues/6).

## Changes

- The lesson 02 coin-mixture selector now has 5.5rem of width, cannot shrink, and uses ordinary horizontal padding rather than reserving extra padding for a second arrow. It retains native appearance, its original label, all values 0–6, the existing model and keyboard behavior. Its label can wrap at large text sizes. Styles are scoped to the Bayes figure.
- Topic interview rows now identify an unaided solve with a green surface, left border, larger check marker, and readable “Unaided solve” badge. Unfinished rows say “Not started” or “In progress”. Reviewed work says “Reviewed / Try again unaided”.
- Historical self-assessment records are labelled “Previously self-assessed / Retake the automatic check”; stale structured passes say “Previous check passed / Retake the current check”. Those historical labels do not fill a current automatic-check slot. The current grading/version rules are unchanged.
- Status presentation reads the existing records without migrating or writing them. Original links, counts, keyboard link semantics and coding-list presentation remain intact. On narrow screens the badge moves below the title in its own grid row.
- CSS/JS asset references were updated. No question, lesson, coding bank or Python backend was changed.

## Checks

All **25 frontend suites passed**. The topic-list suite additionally tests row-state treatment, reviewed work, legacy self-assessments, stale/current structured versions, unchanged module counts and rendering without state mutation. Existing objective tests cover all 74 keys and 1,889 choice subsets; course tests cover the unchanged conditional models and ungraded bindings.

Live native in-app browser verification:

- Lesson 02: selected every value 0–6 and observed the correct fair likelihood and posterior. With equal priors, the always-heads posterior ran from 50% at zero heads to 98.5% at six. No KaTeX errors. The complete selected digit and native arrow fit the closed control at desktop and 390px width; no page overflow.
- Test preview was entered through its explicit launcher before grading. An actual q01 answer earned one unaided pass. An assisted correct q05 answer stayed reviewed. The list showed separate green/neutral states and remained at **1/6**, with original journey links intact.
- Native browser zoom shortcuts did not change the in-app browser's scale. A temporary, explicitly labelled, inert layout fixture instead doubled root and affected text sizes: selector font 24px, width 176px, row titles 34px, badges 26px. It rendered the actual updated list/figure source with synthetic states at 390px and 1280px. All badges stayed inside their rows and separate from titles; no page overflow. Its native dropdown was expanded through accessibility, moved with Down/Return from 1 to 2, and updated the actual posterior to 80%. All seven enlarged values were also selected. This is an enlarged-text stress check, not a claim of native 200% browser zoom or physical screen-reader testing.
- The temporary fixture had no persistence code and was removed. Personal progress remained byte-for-byte equal to the fresh pre-edit baseline throughout. No reset or fixture import occurred in personal mode.
- Final browser page: personal lesson 01 question list, with existing personal records preserved. Temporary viewport overrides were reset and the tab was marked deliverable. Other browser study tabs were not touched. The existing local server was not restarted.

Screenshots: [desktop question states in labelled test preview](issue6-question-states-20261013.png), [native select at phone width](issue5-dropdown-narrow-20261013.png), [enlarged selector in labelled development fixture](issue5-dropdown-enlarged-text-20261013.png).
