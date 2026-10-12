# Topic practice expansion

User-approved contract, 2026-10-12: **lesson → topic interview list → topic coding list**.
Every existing and future lesson needs at least two Easy, two Medium and two Hard
interview questions, plus exactly one Easy, one Medium and one Hard coding exercise.
Students choose questions within the lists; no forced Q1 → Q2 → code chain.

## Quality and compatibility

- Original questions with explicit experiments, assumptions, hints, worked reasoning
  and substantive follow-ups. Difficulty comes from reasoning, not larger numbers.
- Written tasks have specific self-assessment criteria. Numeric tasks explain the
  derivation and common failure, not just the final number.
- Coding defines inputs, outputs, edge cases and realistic complexity; deterministic
  cases and independently checked references are required.
- Preserve q01–q51 and c01–c15 semantics and all current assessments/drafts. Extra
  practice increases denominators, never awards completion. Existing standalone
  and journey bookmarks remain usable.
- If an old linked exercise is removed to keep one coding slot per difficulty,
  register it in `LEGACY_CODING_LINKS`. Its `legacyCoding` bookmark/context and
  original draft/result remain available as additional practice; current list,
  module evidence, resume and completion use only `coding`. Do not silently lose
  a journey or count a fourth exercise.
- No AI coaching, suggested solutions in the editor, firm-attribution padding or
  copied commercial interview-bank content.
- All new topics must be registered explicitly. `topic_practice/__init__.py` checks
  complete-topic difficulty coverage at build time. During this expansion, the
  exact unfinished set is `PENDING_TOPICS`; remove that exception when all are done.
  A future unregistered lesson fails the build.

## Current implementation

| Topic | Bank authoring | Independent math/code review | List/journey/browser review |
| --- | --- | --- | --- |
| l01 sample space | 6 interviews; 3 coding | Verified | Automated + live desktop/narrow |
| l02 conditioning | 6 interviews; 3 coding | Verified | Automated |
| l03 expectation | 6 interviews; 3 coding | Verified | Automated |
| l04 distributions | 6 interviews; 3 coding | Verified | Automated + live numeric/code grading |
| l05 stopping times | 8 interviews; 3 coding | Verified | Automated + desktop/narrow written/list |
| l06 arithmetic | 6 interviews; 3 coding | Verified | Automated + desktop list/narrow numeric proof |
| l07 variance/dependence | 6 interviews; 3 coding | Verified | Automated + live code grading/narrow written rubric |
| l08 data timing | 6 interviews; 3 coding | Verified | Automated + live grading/legacy bookmark/narrow proof |
| l09 estimation | 6 interviews; 3 coding | Verified | Automated + live grading/narrow minimax proof |
| l25 likelihood | 8 interviews; 3 coding | Verified | Automated + live grading/narrow mixture proof |
| l10–l18 researcher | Pending | Pending | Pending |
| l19–l24 trader | Pending | Pending | Pending |

Sources: `topic_practice/foundation_questions.py`, `foundation_coding.py`,
`distributions.py`, `stopping.py`, `arithmetic.py`, `variance.py`, `data_time.py`, `estimation.py`, `likelihood.py`, the existing banks, and
`tests/test_topic_practice.py`, `test_distribution_stopping_practice.py`, and
`test_arithmetic_variance_practice.py`, `test_data_time_practice.py`, and
`test_estimation_practice.py`, and `test_likelihood_practice.py`. Generated assets are
`static/content.json` and `static/coding.json`; rebuild their Python sources.

The two list destinations and nonsequential journey handoffs are implemented
across the site. Existing pending topics expose their current linked practice;
their banks do not yet satisfy the approved difficulty contract. The eight foundation
topics and researcher estimation l09 and likelihood l25 do. Current inventory: 25 lessons, 92 interview questions, 38 coding
exercises. Researcher route: 19 checks, 83 distinct questions, 38 codes.

Next: author researcher l10–l18; finish the trader topics.
Finish live checks of the remaining topic lists and representative exercises.
Inspect each lesson’s
actual learning goals and authored explanation before selecting its problems.
The full goal remains active until all 25 topics, future-topic validation,
navigation, preservation checks and commit/push evidence are complete.

As of 2026-10-12, all 23 frontend suites and 84 Python tests pass. Independent
enumeration, exact moments and rational state equations check the completed topics' delicate
mathematical answers and coding references; all twenty-three new reference solutions
also pass the actual judge. Existing grading meaning and IDs are preserved; q44, q24 and q49–q51 now have topic-specific
written assessment criteria in place of their generic rubrics. Personal
assessments, drafts and trainer history match the baseline captured for this work.
See [verification](evidence/topic-practice-20261012.md) for scope and limitations.
