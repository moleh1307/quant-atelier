# Final topic-practice audit

Historical audit before the user-approved written-to-automatic conversion. Current grading evidence: [automatic assessment review](AUTOMATIC_ASSESSMENT_REVIEW.md).

Verified 2026-10-13. Scope: all 25 existing topics and the future-topic publishing contract.

## Requirements and current evidence

| Requirement | Evidence | Result |
| --- | --- | --- |
| Lesson → interview list → coding list, free choice | `test_journey.cjs`, `test_topic_lists.cjs`; live66-page DOM audit | Passed |
| ≥2 interviews at every difficulty; exactly1 code at each difficulty, every topic | Unconditional build Counter checks and visible difficulty/link checks for all 66 destinations | Passed |
| Topic-specific reasoning, escalation, assumptions and follow-ups | Current lesson objectives and question/follow-up review; topic matrix below; per-topic authored source and independent tests | Reviewed and corrected |
| Specific assessment obligations and complete teaching/coding scaffolds | No generic rubric remains; negative authoring tests; code samples, hidden cases, references and editorials validated in both builds | Passed |
| Preserve prior checked answers and topic bookmarks | Public pre-expansion fixture from c377f0e; all 51 original answer/type/tolerance contracts and every original linked activity retained current or additional | Passed |
| Preserve coding grading meaning | All 75 existing signatures/references/samples unchanged in this audit; whole-bank reference suite | Passed |
| Mathematical clarity and lossless case copies | Strict actual-bank math parsing; semantic number-boundary/sum tests; all 651 official copies exact, largest 490,010 characters | Passed |
| Honest personal progress and preview separation | Fresh ignored pre-edit baseline; actual personal bytes/five groups exact; native personal/default entry and isolated reveals | Passed |
| Reproducible public banks and future coverage | Rebuild byte hashes identical; unregistered/incomplete registered topics, empty teaching fields and incomplete code scaffolds rejected | Passed |

255 Python tests and all 23 frontend suites pass. The Python suite invokes the actual judge for ALL 75 references. This is one author’s review with independently formulated mathematical oracles, not an independent reviewer or employer-certified calibration. Counts and minimum field checks alone are not a teaching-quality certification.

## Topic review

| Topic | Interviews E/M/H | Codes E/M/H | Reasoning progression | Conditions reviewed | Independent evidence |
| --- | --- | --- | --- | --- | --- |
| l01 · Count the right sample space | 2 / 2 / 2 | 1 / 1 / 1 | Uniform records → weighted representations → conditioning and inclusion–exclusion | Physical subsets, multiplicities, fixed-point dependence | `test_topic_practice.py` |
| l02 · Condition, then normalise | 2 / 2 / 2 | 1 / 1 / 1 | Restricted outcomes → posterior prediction → reporting mechanisms and sharp dependence bounds | Fixed latent coin, report likelihood and attainable joint tables | `test_topic_practice.py` |
| l03 · Expectation without independence | 2 / 2 / 2 | 1 / 1 / 1 | Single indicators → overlapping sums → cycles and crossing pairs | Linearity without independence; exact combinatorial counts | `test_topic_practice.py` |
| l04 · Distributions as usable models | 2 / 2 / 2 | 1 / 1 / 1 | Density/support → order statistics and clock races → hidden-regime selection | Continuous measure, survival versus event-density conditioning; cutting-law comparison | `test_distribution_stopping_practice.py` |
| l05 · A state is a sufficient memory | 2 / 2 / 4 | 1 / 1 / 1 | First-step boundaries → sufficient states → unequal coupons and infinite expectation | Terminal conditions and independent block finiteness bounds | `test_distribution_stopping_practice.py` |
| l06 · Arithmetic with a method | 2 / 2 / 2 | 1 / 1 / 1 | Exact scaling → changing bases → rounded intervals and identifiable fractions | Tie rule, feasible denominator bounds and attainable/open endpoints | `test_arithmetic_variance_practice.py` |
| l07 · Variance remembers dependence | 2 / 2 / 2 | 1 / 1 / 1 | Constant sums → nonlinear dependence → overlap covariance and joint feasibility | Distinguish zero covariance from independence; constructive correlation bounds | `test_arithmetic_variance_practice.py` |
| l08 · Write data code that respects time | 2 / 2 / 2 | 1 / 1 / 1 | Availability/ties → selection leaks → vintage uncertainty and causal families | Decision information, receipt boundaries and prefix invariance | `test_data_time_practice.py` |
| l09 · Estimators, bias and uncertainty | 2 / 2 / 2 | 1 / 1 / 1 | Standard error → bias corrections → risk comparison and global minimax proof | Estimator versus realised estimate, prior lower bound and known loss | `test_estimation_practice.py` |
| l25 · Let the data compare the models | 2 / 2 / 4 | 1 / 1 / 1 | Likelihood ratios/domain → observation bins → selection and mixture existence | Conditional observation mechanism, open support and global likelihood existence | `test_likelihood_practice.py` |
| l10 · Covariance is a matrix constraint | 2 / 2 / 3 | 1 / 1 / 1 | Weighted variance → inconsistent pairwise tables → singular feasibility and optimal weights | PSD directions, null space and constructive sufficiency | `test_covariance_practice.py` |
| l11 · Regression as projection | 2 / 2 / 4 | 1 / 1 / 1 | Population slope/units → confounding → latent identification and deletion errors | Projection versus causal intervention; rank and penalty conditions | `test_regression_practice.py` |
| l12 · Inference is a procedure | 2 / 2 / 4 | 1 / 1 / 1 | Exact tails/intervals → randomized tests → anytime validity and selected coverage | Pre-specified procedure, conditional information and valid stopped limits | `test_inference_practice.py` |
| l13 · Dependent returns and effective sample size | 2 / 2 / 4 | 1 / 1 / 1 | Finite covariance/forecast errors → squared risk and overlap → optimal weights and changing asymptotics | Stationarity/initialization, target-specific effective counts, explicit summation | `test_time_series_practice.py` |
| l14 · Validation must imitate deployment | 2 / 2 / 2 | 1 / 1 / 1 | Receipt eligibility/weighted loss → purging versus chronology → adaptive evaluation | Deployment information, half-open boundaries and predictable decisions | `test_validation_practice.py` |
| l15 · Search size belongs in the result | 2 / 2 / 2 | 1 / 1 / 1 | Random denominators/copies → family error → correlated selected scores | Search dependence and shared confirmation noise, not nominal trial count | `test_search_practice.py` |
| l16 · Defend a research result | 2 / 2 / 2 | 1 / 1 / 1 | Payoff/filled paths → mixture changes → policy identification under selective observation | Complete net episodes, action propensities and positivity/missing-support limits | `test_research_defence_practice.py` |
| l17 · Monte Carlo with variance reduction | 2 / 2 / 2 | 1 / 1 / 1 | Independent simulation units → rare events/fitted controls → antithetic and optimal-control arguments | Equal cost, paired dependence, fixed/pilot coefficients and actual coverage | `test_monte_carlo_practice.py` |
| l18 · Algorithms for a research notebook | 2 / 2 / 2 | 1 / 1 / 1 | Welford/ties → mergeable summaries → eviction memory and amortised deque proof | Exact identities versus floating arithmetic, eligible windows and state lower bounds | `test_algorithms_practice.py` |
| l19 · Fair value before a trade | 2 / 2 / 2 | 1 / 1 / 1 | Executable edge → joint signal updates/replication → information value and ambiguity | Payments versus exit cash, costs, still-available actions and model-set interpretation | `test_fair_value_practice.py` |
| l20 · Order flow is information | 2 / 2 / 3 | 1 / 1 / 1 | Opportunity versus fill/inventory → no-order/quote selection → finite-horizon constrained policy | Customer versus dealer direction, posterior state and whole-quote feasibility | `test_order_flow_practice.py` |
| l21 · Continuation value and log growth | 2 / 2 / 3 | 1 / 1 / 1 | Net continuation/wealth multipliers → optional fee order → Bayesian versus robust log growth and tails | Action-dependent fees, admissible positive wealth and declared uncertainty objective | `test_continuation_growth_practice.py` |
| l22 · Risk lives in joint exposures | 2 / 2 / 2 | 1 / 1 / 1 | Factor cancellation/stress → common-shock limit → pairwise-independent crashes and robust hedging | Signed quantities, joint tails, covariance limits and fixed model ambiguity | `test_joint_risk_practice.py` |
| l23 · The small mathematical-finance core | 2 / 3 / 2 | 1 / 1 / 1 | Signed contracts/dated cash → executable parity → incomplete pricing and self-financing rehedges | Physical support versus pricing weights, fees and exact versus local mark identities | `test_finance_core_practice.py` |
| l24 · Strategic inference and calibration | 2 / 2 / 3 | 1 / 1 / 1 | Proper loss/error units → coarse bins/winning posterior → action-dependent bids and calibrated refinement | Fixed information, pairing, population versus fitted expectations and strict win rules | `test_calibration_practice.py` |

## Corrections found by this audit

- Eighteen original generic rubrics now state question-specific obligations. Retained coin/dice/Bernoulli questions clarify independence without changing their checked answers.
- Original run-length, bounded-walk, correlation-bound, AR mean-variance and log-growth explanations now include the derivations their tasks require. The triangle follow-up specifies an alternate sampling law and derives log(2)−1/2; the original independent-cut answer stays one quarter. Point-estimation follow-ups compare loss-defined risks.
- The log-growth uncertainty follow-up now distinguishes a Bayesian mean from a worst-model probability; it does not assert that uncertainty alone forces shrinkage. The excluded certainty boundary is handled.
- Sums use explicit `\sum` rather than an automatically substituted covariance `\Sigma`. The squared-return task defines Y before asking about it. Formula matching no longer consumes prefixes of T=10, n=40, n=1000 or p=1/4. Accuracy pairs use “versus”, preserving their comparison meaning.
- Retained c14 is labelled trader in the standalone library, matching its current calibration topic. Its researcher l18 additional-practice bookmark, draft/result identity and all grading contracts survive.
- Future-topic and coding builds reject incomplete scaffolds and the known generic assessment placeholder. Substantive quality still requires topic-specific authoring/review; no automatic test can replace that judgment.

## Browser and record evidence

Native IAB controls were used after preferred Atlas IAB discovery failed. All 66 list destinations (eight shared topics in both paths plus seventeen branch-specific topics, each with two lists) matched current source links and visible difficulty counts. The public [DOM audit](final-topic-list-audit.json) records structure and links, not private study results. Current list completion uses only current slots; legacy links remain valid additional practice. The c14 trader filter was visibly checked.

Changed triangle and squared-return statements/proofs were inspected at a 390px override (375px content width) with no document overflow or KaTeX errors. T=10 remained intact in the real fit-time statement. Reveals occurred only after explicit launcher entry and a visible Test preview notice; no personal grading or reset occurred. Normal sizing was restored; the final tab is personal. Screenshots: [triangle follow-up](final-triangle-followup-narrow.png), [defined squared-return process](final-squared-return-definition-narrow.png).

Actual saved personal bytes and questions/coding/lessons/drafts/trainers match the fresh ignored final-audit baseline exactly. Existing legitimate learner work is retained; a new topic showing zero does not imply the entire workspace is unused. No private records, baselines or reference scratch files are published.

Current catalogue: 25 lessons,164 interviews (94 numeric,70 written),75 coding exercises. There are75 topic coding slots across25 topics;74 unique current exercises because c04 is shared between two topics, plus the retained additional-only c10 in the library. Researcher19 checks/124 unique questions/56 current codes; trader14/90/42. Written reasoning is explicitly self-assessed; a numeric acceptance alone does not certify its derivation. No AI coaching or suggested solutions were added.

## Scope boundary

The requested existing-topic expansion and future-topic contract are complete after the verified audit commit is pushed. This does not author a new course, add an interview-simulation product, or certify readiness for any firm. Future course additions must follow the canonical authoring guide and pass the same build/test/review contract.
