# Topic practice — verification

2026-10-12. Latest verified scope: grouped list/journey navigation across the site,
and expanded banks for l01–l05. The full 25-topic expansion remains active;
20 topic banks are pending, as recorded in [the status file](../TOPIC_PRACTICE_STATUS.md).

The first batch below documents l01–l03 at its own verification baseline
(63 questions / 22 codes). The later l04/l05 batch is recorded at the end.

## Content

- Each of l01–l03 now has 2 Easy, 2 Medium and 2 Hard interview questions, and
  exactly one coding exercise per difficulty. Added 12 interview questions and
  seven coding exercises. Total banks: 63 questions / 22 exercises / 25 lessons.
- New interview questions include weighted unordered records, conditional
  multiplicities, constrained permutations, report-dependent evidence,
  dependence bounds, random cycles and crossing indicators. Worked solutions
  derive the result and address a specific invalid shortcut; written rubrics are
  problem-specific.
- Coding covers retaining probability mass, subset-state counting, finite Bayes
  updates, stable hidden-state filtering, linear expectation and order statistics
  without replacement. The log-space filtering reference preserves tiny states
  that can regain importance after later evidence; scaling ordinary probabilities
  alone is insufficient for its documented inputs.
- Original q01–q51 and c01–c15 public records were compared with the previous
  commit and remain exactly unchanged. Permanent IDs and grading are retained.

## Checks actually run

- All **23 frontend suites** passed, including difficulty-list coverage, stage
  evidence, all existing/new journey bookmarks, branch boundaries, return-to-list
  navigation, assistance provenance and rendering without awarding progress.
- All **34 Python tests** passed. New independent checks enumerate physical
  draws, permutations, small circle matchings, hidden state paths with rational
  probabilities, and all small subsets with duplicate card labels. Assignment DP
  is compared with every 3×3 binary matrix's allowed permutations. Exact joint
  tables attain the conditional dependence bounds.
- All **seven new coding references** pass their actual complete judge suites.
  Input preservation is checked separately. Existing reference/judge/progress
  tests also pass. Large deterministic cases reject obvious brute-force or
  underflow failures; these are not formal asymptotic runtime proofs.
- Generated mathematical spans parse with strict local KaTeX and include MathML.
- Build validation enforces complete-topic difficulty counts and rejects a new
  unregistered lesson. The unfinished set is explicit during this expansion;
  remove that exception when the curriculum is complete.

## Browser evidence

The IAB backend was unavailable. Chrome reviewed the real local site using the
explicit `/test-preview.html` launcher and **Enter test preview**. The visible
preview notice was checked before submissions. A freely chosen hard question
accepted 2/5, returned to the question list and updated its preview counter. The
new medium l01 coding reference passed **9/9** through the UI, returned to the
coding list and updated that list's preview counter.

- [Question list, desktop](topic-question-list-20261012.png).
- [Coding list, desktop](topic-coding-list-20261012.png).
- [Question list, 390px viewport](topic-question-list-narrow-20261012.png).

All screenshot counters are **development records**, not personal achievement.
At 390px, document width was 390px and all six question rows remained inside the
viewport. Hard titles, statuses, the sticky stage strip and the continuation were
inspected while scrolling. The viewport override was reset; the tab was returned
to the personal question list. Personal question, coding, lesson, draft and trainer
records matched this task's disk baseline afterward. No personal record was reset.

These checks establish specified behaviour and mathematical case consistency.
They do not certify employer difficulty, interview readiness, learning outcomes,
physical mobile interaction or screen-reader usability. l02/l03 use the same
verified list component and have automated bookmark/render checks; their entire
new practice was not manually submitted in the browser.

## Second batch: distributions and stopping times

Added six interview questions and five coding exercises. l04 has two questions
per difficulty; l05 has two Easy, two Medium and four Hard questions. Both have
exactly one coding exercise per difficulty. All 63 preceding question records and
22 preceding coding records remain byte-for-byte equivalent after JSON parsing.
Current totals: **25 lessons / 69 questions / 27 codes**. Researcher route:
**19 checks / 60 distinct questions / 27 codes**. The illustrated lesson bodies,
lesson checks and previous permanent IDs were not rewritten.

The new reasoning includes density versus point probability, posterior regime
weights in a quiet exponential race, a density-based observation follow-up,
geometric count conventions, objective-specific random-walk boundaries,
nonuniform collection and almost-sure termination with infinite mean. The hard
walk solution justifies its conclusions through bounded barriers; its biased
follow-up establishes integrability before applying an expected-increment identity.

Coding progresses from finite CDFs to heterogeneous minima and ranked outcomes,
and from geometric stages to arbitrary binary pattern waits. The latter explains
its overlap identity with fair bettors and a justified stopped limit, rather than
merely stating a formula. Integer-probability accumulation avoids repeated float
products; all allowed length/probability extremes remain finite.

Verification:

- All **41 Python tests** and **23 frontend suites** passed. All twelve new coding
  references across both batches pass their complete actual judge suites.
- A separate exact seen-set recurrence checks 73/10 for the unequal collector.
  Direct joint-outcome enumeration checks CDF/minimum/rank outputs on 100 seeded
  finite models, including unequal PMFs, negative values in the rank task,
  zero masses, ties and unsorted/repeated thresholds.
- Every binary pattern of lengths 1–6 is compared with rational first-step
  equations at three coin biases (378 systems). These systems use direct suffix
  search rather than the reference's failure links and border identity. Allowed
  200-symbol extremes are checked by exact integer/rational expressions.
- Rational finite-walk systems independently check duration and hitting formulas
  for barriers 2–25. The proof for all barriers supplies the infinite-mean result;
  no finite simulation is described as proving it.
- Public sample/test expectations are separately checked against those models.
  Official suites reject strict-CDF, failure-count and reciprocal-pattern shortcuts.
  Large deterministic cases and reference review support the stated algorithms;
  judge success alone is not a formal complexity proof.
- Strict local KaTeX parsing covers the generated new bank. l05's rendered narrow
  proof had 12 math spans, zero math errors and document width/scroll width 390px.

Chrome was used after the IAB connection failed. Explicit preview entry and its
notice were verified before submitting 8/15 to the hard race question and the
rank-CDF reference to the coding judge (**9/9**). Returning from the individual
question led to the coding list without forcing another problem. The l05 list
displayed all eight choices, with the written task explicitly labelled
self-assessed and its specific rubric visible. Reload correctly returned to
personal mode; worked-solution inspection then re-entered preview explicitly.
Viewport overrides were reset and the final tab was left at the personal l05
question list. Question/code/lesson/draft/trainer data matched the freshly
captured disk baseline; no personal record was reset or graded.

- [Stopping-time question list, desktop preview](stopping-question-list-20261012.png).
- [Written proof, 390px preview capture](stopping-proof-narrow-20261012.png).

Preview screenshots contain development notices and may contain saved-tab
recovery feedback while preview writes are pending. That feedback disappeared on
navigation; no personal recovery was applied. Full-page capture includes sticky
elements and focus indicators; it is not a physical-device or screen-reader test.
The two new banks satisfy the authored contract, but the remaining 20 banks and
broader manual review are still required for the full goal.
