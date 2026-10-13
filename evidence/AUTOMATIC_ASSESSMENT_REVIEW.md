# Automatic interview assessment review

Verified 2026-10-13. User requested automatic answers for the 70 self-assessed questions without reducing their intellectual scope.

## Delivered contract

All 164 interview questions now have automatic grading. The 94 existing numeric answer/tolerance contracts are unchanged. All 70 written questions retain their original IDs, full prompts, hints, worked derivations, reasoning obligations, difficulty, paths, minutes and follow-ups. They now have 156 authored checkpoints: 81 numeric and 75 exact-set multiple-selection checks, containing 335 true/false claims. Quantitative transfer cases accompany general arguments; 26 harder sets include additional close mathematical distractors. Every checkpoint must pass, with no missing true statements or extra false statements. Worked solutions include the reason for every choice.

This checks the defined numerical results and reasoning claims. It does not machine-grade arbitrary written proofs, empirically calibrate interview difficulty, or prove that recognition and free-form derivation have identical difficulty. The original derivation tasks and substantive follow-ups remain available.

## Implementation and compatibility

- `automatic_assessments.py` authors the conversion and rejects missing/invalid automatic contracts. `build_content.py` reproduces the generated bank. Mathematical choices have explicit spoken labels; stable option IDs are independent of deterministic display order.
- `static/app.js` renders integrated, keyboard-operable checkpoints and saves versioned answer drafts. The full derivation scratchpad remains available. Invalid/blank/partial submissions cannot award a pass; checkpoint answer explanations appear with the worked solution.
- A structured question counts only if its stored unaided pass names the current assessment version. Historical self-assessment flags and written drafts remain in their original records without promotion. This rule applies to lists, roadmap/resume, overview, progress, filters and backup comparisons.
- Viewing hints/solutions/follow-ups or old work marks assistance. An assisted correct answer records review; a fresh attempt preserves a recoverable prior answer/scratchpad. The obsolete self-solved action cannot award credit.
- Original topic lists, free practice choice, both branches, lesson checks, all coding contracts and module bookmarks remain intact.

## Verification

261 Python tests and all 24 frontend suites passed. Existing independent per-topic mathematics/algorithm checks remain; new exact-fraction, finite-record, covariance, likelihood, numerical-quadrature and optimization oracles check concrete checkpoint keys. The pre-conversion public hash fixture verifies every original question field except its explicitly changed grading type.

The actual frontend grader was checked on all 70 keys and 1,765 nonempty choice subsets: exactly the correct set passes each selection checkpoint. Missing/extra choices, duplicate/unknown IDs, incorrect numbers, blank fields and invalid expressions fail appropriately. Real submit/input handlers, saved selections, fresh/restore, assistance, old-progress compatibility, both route totals and export totals are covered. All 3,320 authored/generated math spans parse strictly with accessible MathML.

Preferred Atlas IAB discovery was unavailable; native IAB controls were used. Live preview submissions verified a correct unaided pass, partial correctness without a pass, and solution-assisted correctness recorded only as reviewed. Reload through the development launcher retained inputs/selections and provided spoken checkbox names. Every converted page was inspected at a 390px viewport: all checkpoint/choice counts matched source, no KaTeX errors, no document overflow and no overflowing choice containers. A representative desktop view was visually checked with the scratchpad visible beside the checks. These are browser/DOM checks, not a physical-device or screen-reader certification.

Graded actions and solution reveals used explicit Test preview admission. Personal study continued concurrently in another browser; no baseline was restored or reset. Development-tested problem records remained unchanged in the personal file. The final IAB page is personal, with preview selections/passes absent and normal viewport restored. Live structure-only record: `objective-live-audit.json` (ignored local evidence, contains no study records). Screenshot: `objective-checks-personal.png`.
