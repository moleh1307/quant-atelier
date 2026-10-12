# Topic practice — first verified batch

2026-10-12. Scope: the list/journey change across the site and expanded practice
for l01–l03. The full 25-topic expansion remains active; 22 topic banks are still
pending, as recorded in [the status file](../TOPIC_PRACTICE_STATUS.md).

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
