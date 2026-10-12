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
| l04–l08 foundation | Pending | Pending | Pending |
| l09, l25, l10–l18 researcher | Pending | Pending | Pending |
| l19–l24 trader | Pending | Pending | Pending |

Sources: `topic_practice/foundation_questions.py`, `foundation_coding.py`, the
existing banks, and `tests/test_topic_practice.py`. Generated assets are
`static/content.json` and `static/coding.json`; rebuild their Python sources.

The two list destinations and nonsequential journey handoffs are implemented
across the site. Existing pending topics expose their current linked practice;
their banks do not yet satisfy the approved difficulty contract. The first three
topics do. Current inventory: 25 lessons, 63 interview questions, 22 coding
exercises. Researcher route: 19 checks, 54 distinct questions, 22 codes.

Next: author l04–l08, then researcher and trader practice in topic-sized batches.
Finish live checks of the remaining topic lists and representative exercises.
Inspect each lesson’s
actual learning goals and authored explanation before selecting its problems.
The full goal remains active until all 25 topics, future-topic validation,
navigation, preservation checks and commit/push evidence are complete.

As of 2026-10-12, all 23 frontend suites and 34 Python tests pass. Independent
small-case enumeration checks the first three topics' delicate mathematical
answers and coding references; all seven new reference solutions also pass the
actual judge. Every original public question/exercise item is unchanged. Personal
assessments, drafts and trainer history match the baseline captured for this work.
See [verification](evidence/topic-practice-20261012.md) for scope and limitations.
