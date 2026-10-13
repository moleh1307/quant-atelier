# Topic practice expansion

User-approved contract, 2026-10-12: **lesson → topic interview list → topic coding list**.
Every existing and future lesson needs at least two Easy, two Medium and two Hard
interview questions, plus exactly one Easy, one Medium and one Hard coding exercise.
Students choose questions within the lists; no forced Q1 → Q2 → code chain.

## Quality and compatibility

- Original questions with explicit experiments, assumptions, hints, worked reasoning
  and substantive follow-ups. Difficulty comes from reasoning, not larger numbers.
- Every interview task has automatic numerical or multi-part exact-set checks.
  Retain specific reasoning obligations and full derivations; no self-assessment action.
  Check specified results/claims rather than pretending to grade arbitrary proofs.
- Coding defines inputs, outputs, edge cases and realistic complexity; deterministic
  cases and independently checked references are required.
- Preserve stable question/exercise IDs, original prompts/derivations, numeric keys and drafts.
  The user approved converting written grading on 2026-10-13; legacy self-assessments
  remain records but cannot count as passes of the new version. Extra
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
  every registered topic’s difficulty coverage at build time, without an unfinished-bank exception.
  A future unregistered lesson fails the build; registering one does not bypass coverage.

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
| l26 calculus | 6 interviews; 3 coding | Independent forward/finite-difference references verified | Automated + live checks, lists and desktop/narrow figures |
| l27 optimization | 6 interviews; 3 coding | Rational active-set/KKT and exact update references verified | Automated + live checks, lists, hard-code submission and desktop/narrow layouts |
| l09 estimation | 6 interviews; 3 coding | Verified | Automated + live grading/narrow minimax proof |
| l25 likelihood | 8 interviews; 3 coding | Verified | Automated + live grading/narrow mixture proof |
| l10 covariance | 7 interviews; 3 coding | Verified | Automated + live exact grading/debug copy/narrow proof |
| l11 regression | 8 interviews; 3 coding | Verified | Automated + live exact grading/debug copy/narrow proof |
| l29 regularization/statistical learning | 6 interviews; 3 coding | Exact active-face/risk oracles, high-precision logistic gradients and raw-coordinate rational fold solves | Automated + live lesson/partial-Hard/exact-set checks, lists, hard Submit and desktop/mobile figures |
| l12 inference | 8 interviews; 3 coding | Verified | Automated + live exact grading/debug copy/narrow proof |
| l13 time series | 8 interviews; 3 coding | Verified | Automated + live exact grading/debug copy/narrow proof |
| l28 resampling/bootstrap | 6 interviews; 3 coding | Exact rational/enumeration laws, interval invariance and circular covariance oracles verified | Automated + live check, partial/exact-set Hard grading, both lists, hard-code Submit and desktop/mobile figures |
| l14 validation | 6 interviews; 3 coding | Verified | Automated + live grading/debug copy/legacy bookmark/narrow proof |
| l15 search/multiple testing | 6 interviews; 3 coding | Verified | Automated + live exact grading/debug copy/narrow proof |
| l16 research defence | 6 interviews; 3 coding | Verified | Automated + live exact grading/debug copy/narrow proof |
| l17 Monte Carlo | 6 interviews; 3 coding | Verified | Automated + live exact grading/debug copy/narrow proof |
| l18 researcher algorithms | 6 interviews; 3 coding | Verified | Automated + live grading/full debug copy/legacy bookmark/narrow proofs |
| l19 fair value | 6 interviews; 3 coding | Verified | Automated + live grading/exact and large debug copies/narrow proofs |
| l20 order flow | 7 interviews; 3 coding | Verified | Automated + live grading/public exact debug copy/narrow policy proofs |
| l21 continuation/log growth | 7 interviews; 3 coding | Verified | Automated + live grading/exact debug copies/narrow Bayesian and tail proofs |
| l22 joint exposures/risk | 6 interviews; 3 coding | Verified | Automated + live grading/exact debug copies/narrow crash and hedge proofs |
| l23 mathematical finance | 7 interviews; 3 coding | Verified | Automated + live grading/three public exact debug copies/narrow pricing and cash-ledger proofs |
| l24 strategic inference/calibration | 7 interviews; 3 coding | Verified | Automated + live Hard-first grading/exact public debug copies/narrow proofs |

Sources: `topic_practice/foundation_questions.py`, `foundation_coding.py`,
`distributions.py`, `stopping.py`, `arithmetic.py`, `variance.py`, `data_time.py`, `estimation.py`, `likelihood.py`, `covariance.py`, `regression.py`, `inference.py`, `time_series.py`, `validation.py`, `search.py`, `research_defence.py`, `monte_carlo.py`, `algorithms.py`, `fair_value.py`, `order_flow.py`, `continuation_growth.py`, `joint_risk.py`, `finance_core.py`, `calibration.py`, the existing banks, and
`tests/test_topic_practice.py`, `test_distribution_stopping_practice.py`, and
`test_arithmetic_variance_practice.py`, `test_data_time_practice.py`, and
`test_estimation_practice.py`, and `test_likelihood_practice.py`, and `test_covariance_practice.py`, and `test_regression_practice.py`, and `test_inference_practice.py`, and `test_time_series_practice.py`, and `test_validation_practice.py`, and `test_search_practice.py`, and `test_research_defence_practice.py`, and `test_monte_carlo_practice.py`, and `test_algorithms_practice.py`, and `test_fair_value_practice.py`, and `test_order_flow_practice.py`, and `test_continuation_growth_practice.py`, and `test_joint_risk_practice.py`, and `test_finance_core_practice.py`, and `test_calibration_practice.py`. Generated assets are
`static/content.json` and `static/coding.json`; rebuild their Python sources.

The two list destinations and nonsequential journey handoffs are implemented across the site.
All 25 existing topic banks meet the approved difficulty contract. Current inventory:
25 lessons, 164 interview questions, 75 coding exercises. Researcher route:
19 checks, 124 distinct questions, 56 current codes. Trader route:
14 checks, 90 distinct questions, 42 current codes. Shared links count once per route.

The final all-topic audit is verified: [requirements, topic quality matrix and evidence](evidence/FINAL_TOPIC_PRACTICE_AUDIT.md). All66 live list destinations match the source contract; original grading/bookmarks and actual personal work are preserved. The audit corrections and publishing checks are recorded there.

As of 2026-10-13, all 23 frontend suites and 255 Python tests pass. Independent
enumeration, exact moments and rational state equations check the completed topics' delicate
mathematical answers and coding references; all sixty expanded reference solutions
also pass the actual judge. Existing grading meaning and IDs are preserved; q44, q24, q49–q51, q20/q29 and q19/q21/q30 and q22/q26/q47 and q18/q31 and q27/q28 and q04/q25/q32 and q33/q34 and q43/q48 and q35 and q36/q42 and q13/q37 and q38 and q39/q40 and q41 now have topic-specific
assessment criteria in place of their generic rubrics. q27 also clarifies overlap wording without changing its assessment meaning. q25 now states its intended exact rejection probability; q32 distinguishes identical copies from a genuine search. q48 explicitly includes finite second moments and handles a constant target without undefined correlation, preserving its assessment meaning. Existing saved study records are retained. Batch-specific preservation evidence and baseline availability limits are documented in verification.
See [verification](evidence/topic-practice-20261012.md) for scope and limitations.

## 2026-10-13 calculus and optimization addition

Current totals are 27 lessons, 176 automatically checked interviews and 81 library codes. The researcher route contains 21 modules, 136 distinct interview problems and 62 current codes. Original 25 topic records and assessment contracts are unchanged. [Implementation and verification](evidence/CALCULUS_OPTIMIZATION.md) documents this addition; older dated reports remain historical.


## 2026-10-13 resampling and bootstrap addition

Current totals: 28 lessons, 182 automatically checked interviews and 84 library codes. Researcher: 22 modules / 142 distinct interviews / 65 current codes; trader unchanged at 14/90/42. The original 27 lesson, 176 interview and 81 code records are identical to the pre-addition build. All 279 Python tests and 26 frontend suites pass. Detailed source, independent mathematical calculations, browser observations and limits: [resampling audit](evidence/RESAMPLING_BOOTSTRAP.md). Earlier counts above describe dated prior audits.


## 2026-10-13 regularization and statistical learning addition

Current totals29 lessons/188 automatic interviews/87 library codes; researcher23/148/68, trader14/90/42 unchanged. Previous28 lesson/182 interview/84 code records preserved exactly. All289 Python tests and27 frontend suites passed; [current audit](evidence/STATISTICAL_LEARNING.md) records exact calculations, live checks and remaining limits. Earlier counts above remain historical.
