# Topic practice — verification

2026-10-12. Latest verified scope: grouped list/journey navigation across the site,
and expanded banks for l01–l16 and likelihood l25. The full 25-topic expansion remains active;
8 topic banks are pending, as recorded in [the status file](../TOPIC_PRACTICE_STATUS.md).

The first batch below documents l01–l03 at its own verification baseline
(63 questions / 22 codes). Later batches are recorded below.

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


## Third batch: arithmetic and variance/dependence

Added ten interview questions and five coding exercises. l06 and l07 each have
two interviews per difficulty and exactly one coding exercise per difficulty.
l07 keeps q45, q17 and c04 unchanged. All 69 preceding public question records
and 27 preceding public coding records are identical after JSON parsing. Totals:
**25 lessons / 79 questions / 32 codes**; researcher route
**19 checks / 70 distinct questions / 32 codes**. Eighteen topic banks remain.

Arithmetic moves from compensating products and scaling quotients to changed
percentage bases, value-weighted changes, exact fraction recovery under a
denominator bound and a rigorously constructed ranking reversal. Half-up
rounding defines half-open intervals; tighter measurement precision is explicitly
distinguished from adding display zeroes. Coding starts with reduced-denominator
termination, compounds integer basis-point rates as exact rational values, then
uses accelerated Stern–Brocot neighbor jumps to recover a minimum-denominator
fraction consistent with up to 100 decimal places. The hard editorial proves
minimality through the unimodular neighbor representation and distinguishes a
simplest compatible fraction from identifying the original measurement.

Variance progresses through a constant random sum, uncorrelated nonlinear
dependence, signed covariance from overlapping windows and feasibility of a
common correlation. The written hard problem requires both bounds, an explicit
attainable boundary construction and a construction for the full interval; its
self-assessment rubric names these obligations. Coding computes population
variance from joint records, retains the existing online Welford exercise, and
calculates coin-pattern count moments using border links and pair counts in
O(k) character comparisons even when the flip count is 10^12. Exact-integer
arithmetic costs are described separately.

Verification on 2026-10-12:

- All **51 Python tests** and **23 frontend suites** pass, including strict KaTeX
  checks of the generated mathematical bank and actual-judge runs of all
  seventeen expanded reference solutions. Public sample/test expectations are
  separately checked; implementations must preserve their supplied inputs.
- Fraction termination agrees with divisibility by powers of ten across small
  signed numerators/denominators. Exact compounded rates agree with a separate
  Fraction-based product oracle on deterministic and seeded lists, including a
  430-digit result and an irreversible 100-percent loss.
- Every nonzero one-, two- and three-decimal report (1,107 bins) agrees with
  an independent denominator-by-denominator fraction search. Both 100-digit
  extremes and included/excluded rounding endpoints are checked.
- Exact fraction enumeration checks the 2/7 uniqueness at denominator 15 and
  the additional 5/17 possibility at denominator 20. Rational comparisons check
  the rounding reversal, sharp interval approaches and guaranteed ranking
  after genuinely more precise measurement.
- Joint variances agree with a separate rational raw-moment identity. Enumeration
  of all 32 centered sign-vector inputs verifies the common-correlation boundary
  construction's marginal variances, pair covariances and zero sum.
- Every H/T pattern of lengths 1–4, flip counts 0–8 and three coin biases is
  compared with direct enumeration of the flips. An independent exact
  probability/first-moment/second-moment state calculation checks the published
  cases, seeded longer patterns and the 100-symbol case. Huge flip counts are
  also checked against separate analytical expressions for HT and HHH.
- The actual judge rejects representative shortcuts: using the displayed fraction
  as the unknown original, adding percentage changes, dropping covariance and
  applying a binomial variance to overlapping occurrences. Judge success alone
  is not a proof of the editorial's complexity claims.

Chrome was used after the IAB connection was unavailable. The personal arithmetic
list displayed two questions in every difficulty group and linked to a coding
list with one exercise per group. Explicit launcher entry and the Test preview
notice were verified before grading: the hard fraction question accepted 2/7 and
the hard variance reference passed **12/12** complete-suite cases. The rendered
fraction proof and the variance written rubric were checked at a 390px viewport;
both had zero KaTeX errors and document/scroll width 390px. The variance list
displayed six choices and its development coding pass remained confined to
preview. A transient saved-tab recovery notice appeared after preview writes
and disappeared upon navigation; no recovery copy was applied.

Viewport overrides were reset and the review tab was returned to the personal
arithmetic list. Question, coding, lesson, draft and trainer records match the
fresh disk baseline captured before this batch. No personal solve was added or
removed. This is desktop/browser breakpoint verification, not a physical-device
or screen-reader certification.

- [Arithmetic interview list, personal workspace](topic-arithmetic-list-20261012.png).

Next: l08 data timing, including preservation of its second original Medium
coding bookmark when the new list contains exactly one Medium slot. Continue
with researcher and trader topics; do not describe seven completed banks as the
completed 25-topic goal.


## Fourth batch: data timing and publication histories

All eight foundation topics now satisfy the interview/coding difficulty contract.
l08 adds five interviews and two coding exercises, retains q44 and c06, and
preserves c05 as additional practice. Totals: **25 lessons / 84 questions / 34
codes**. Researcher route: **19 checks / 75 distinct questions / 34 codes**.
Seventeen researcher/trader banks remain. q44 now has specific availability-join
assessment criteria; every other q44 field, all other 78 preceding public question
records and all 32 preceding coding records are unchanged after JSON parsing.

Easy questions distinguish elapsed time from record count and inclusive release
eligibility from a strict-before rule. Medium practice pairs the existing
availability audit with a future-dependent row-selection counterexample: a causal
feature cannot repair a population selected on its future success. The historical
vintage problem constructs compatible histories, derives sharp identified profit
sets under component and aggregate revision bounds, and treats the unattained
shared-budget boundary at four explicitly. The other Hard question proves a
necessary/sufficient prefix condition across different stream lengths, using one
finite-time batch evaluator; lagged observations with future-fitted normalization
provide a concrete failure. Written rubrics identify the actual proof obligations.

The Easy code counts distinct records in a half-open elapsed-time interval,
excluding the whole current-time tie group. The Medium code is the original c06
availability scan. Hard coding replays per-key publication histories with original
measurement revisions, retractions, restorations, tie precedence, elapsed-time
expiration and decisions in arbitrary input order. Its reference uses a sorted
sweep, version map and per-key heap, and captures scalar results at the historical
decision before later versions change. It does not use the last publication as a
substitute for the greatest active event timestamp.

Verification on 2026-10-12:

- **62 Python tests** and **23 frontend suites** pass. All nineteen expanded
  coding references pass the actual judge and preserve their supplied inputs.
- The elapsed-window code agrees with direct record-membership enumeration
  across every sorted timestamp sequence of length 0–6 over five timestamp
  values and five horizons. A longer arithmetic progression checks boundary
  counts without generating its expectations through the reference.
- c06 agrees with separate eligible-row scans on 250 seeded histories.
  The new Hard reference agrees with rebuilding each decision's publication
  history on 750 seeded multi-key histories, including ties, missing keys,
  negative/zero values, deletion, restoration, expiration and arbitrary orders.
  Reversing input release order leaves sequence-based precedence unchanged.
- Future revisions and unrelated-key releases cannot change earlier outputs.
  Original public examples and hidden expectations are separately checked
  against these oracles. The judge rejects current-time inclusion and
  last-publication shortcuts; sorting/heap invariants, not a passing timer,
  establish the stated asymptotic algorithm.
- Four binary outcomes check the future-selection probability and retention
  rate. Rational grids check the historical-profit constructions, component
  bounds and exact shared-budget boundaries. The proof in the solution supplies
  the all-real identified sets and unattained infimum; finite grids do not prove
  universal real-valued claims. The prefix theorem is reviewed as a proof;
  finite altered-suffix examples demonstrate its counterexample rather than
  purporting to prove the universal condition.
- The build requires explicit retention of removed coding bookmarks and rejects
  duplicate/invalid additional links or overlap with current slots. Both branch
  navigation tests resolve c05 in l08, preserve its draft, exclude its pass from
  l08's current 0/3 evidence and keep its separate current l18 context intact.
- Strict local KaTeX parsing checks the authored/generated mathematical bank
  after the final wording corrections. The browser review caught an inappropriate literal
  field-name subscript and replaced it with the defined interval [t-h,t]. Long
  setups and derivations use intentional paragraph boundaries, preserved by
  practice-prose styling rather than a single wall of text.

Chrome was used after the IAB connection was unavailable. The personal question
list displayed two choices per difficulty; the coding list displayed exactly one
per difficulty and linked to researcher l09. The permanent c05/l08 journey opened
with its Additional practice label and returned to this same coding list.
Explicit launcher entry and the Test preview notice preceded submission of the
Hard snapshot reference (**11/11**). Reload returned to personal mode, and later
solution inspection re-entered preview explicitly. The final Hard historical
proof and its rubric rendered at 390px with zero math errors and document/scroll
width 390px. No written self-assessment was awarded during inspection.

Temporary viewport settings were reset; the review tab was left at the personal
l08 coding list, which showed 0/3 rather than the preview's development pass.
Question, code, lesson, draft and trainer records matched the fresh disk baseline.
The transient preview saved-tab recovery notice disappeared on navigation; no
personal recovery was applied. This is desktop/breakpoint evidence, not physical
mobile-device or screen-reader certification.

- [Data-timing coding list, personal workspace](data-time-coding-list-20261012.png).

Next: researcher l09 estimators, then likelihood l25 and the remaining researcher
and trader banks. Preserve the new additional-practice mechanism when later
lessons have multiple original coding links at the same difficulty. The full goal
remains active until all 25 topics and the final preservation/navigation audit
are complete.


## Fifth batch: researcher estimation l09

As of 2026-10-12, l09 has two Easy, two Medium and two Hard interview questions,
and exactly one coding exercise per difficulty. Read the actual authored
`static/lesson-estimation.js` argument and learning goals before selecting the
practice. The chapter itself, its check and all assessment meanings are unchanged.
Current total: 25 lessons / 87 interviews / 36 codes; researcher route 19 checks /
78 distinct questions / 36 codes. Sixteen topics remain unfinished.

New interviews distinguish standard error from observation/prediction noise,
optimise the uniform-maximum risk rather than its bias, compare the best scaled
sample mean, and prove Bernoulli minimax optimality beyond a chosen shrinkage
family. Hard prompts define the loss, observed information, fixed versus
sample-dependent choices and the scope of the conclusion. Written solutions
include intermediate moments, risk comparisons, a posterior-loss decomposition
and an average-risk lower bound; follow-ups test a changed estimator or fixed
amount of shrinkage. New written rubrics name the proof obligations. The existing
q24 variance-divisor rubric now names its iid assumption, n>1 correction and
dependence limitation; every other field of q24 and all 83 other preceding
question records are unchanged. All 34 preceding public code records are equal
to the previous commit, including the original c04 streaming-variance exercise.

`topic_practice/estimation.py` adds posterior summaries after disjoint batches
(Easy) and stable posterior predictive batch tails (Hard). The Hard editorial
integrates the conditional binomial distribution, derives adjacent-mass ratios
and a mode, and explains why a mode-anchored relative distribution and suffix
sums avoid endpoint underflow and upper-tail cancellation. The shared-p model,
integer parameters, no-mutation rule, empty/zero-trial cases, equality endpoints,
query order/duplicates, numerical tolerance and O(m+q) target are explicit.

Independent verification in `tests/test_estimation_practice.py`:

- Eleven tests include exact polynomial integration for uniform-maximum risk,
  completed-square perturbations, sample-mean comparison and n=1 boundaries.
- Binomial count enumeration verifies constant risk for n=1–44 across interior
  and endpoint probabilities. Rational square-n examples independently integrate
  posterior variance under the prior, checking the attained global lower bound
  and a competing-rule perturbation. These checks support the written proof;
  finite enumeration alone is not the universal minimax proof.
- Three hundred seeded cumulative-posterior cases use exact prefix moments,
  rather than the reference's update/variance factorisation. All published
  posterior-summary expectations agree with that oracle; splitting batches
  retains the same final posterior.
- All 325 combinations A,B=1–5, m=0–12 use exact beta-integral count masses.
  Means/variances agree with independent moment identities; asymmetric examples
  reject swapped parameter conventions and mean plug-in predictions.
- An 85-digit Decimal distribution starts at the endpoint and is not
  renormalised. It independently checks all nonuniform large official cases,
  including 100000 future trials with billion-count posteriors. The 3000-trial
  balanced case has a true endpoint below double precision; the floating
  reference still computes its central tail correctly. Uniform predictions use
  an exact closed form, including a separate 100000-query check.
- One hundred fifty seeded symmetry/update/order cases, input-preservation
  assertions, and actual-judge checks reject batch-reset, binomial plug-in and
  underflowed-endpoint shortcuts. All new official cases also fit the editor's
  existing 200000-character combined debugging-copy limit; the official stress
  case uses 6004 queries spread over the full 100000-trial support.

All 73 Python tests and 23 frontend suites passed. All 21 expanded reference
solutions pass the actual judge. Strict parsing covers the generated/authored
math with no errors. The standard minimax argument was cross-checked against
[UC Berkeley's statistical decision theory notes](https://stat210a.berkeley.edu/fall-2025/reader/minimax-estimation.html).
The predictive model was cross-checked against the
[NIST beta-binomial reference](https://www.itl.nist.gov/div898/software/dataplot/refman2/auxillar/bbnpdf.htm);
NIST uses a different shape-parameter order, so the exercise defines A as the
success shape and checks asymmetric cases explicitly. These are mathematical
verification sources, not claims of an employer's exact interview questions.

The in-app browser connection was unavailable; Chrome reviewed the normal
lesson-to-list handoff, both difficulty lists and the minimax worked proof.
Preview entry was explicit and the Test preview notice was verified before
solution inspection and coding submission. The final server suite passed 15/15
in the browser, including its long numerical/query cases. The proof, specific
rubric and Python exercise rendered at 390px with zero math errors and document
width equal to scroll width (390px). No written self-assessment was awarded.
Temporary viewport settings were reset and the review tab was left at the
personal l09 coding list, showing 0/3 rather than the preview's development pass.
All five personal question/code/lesson/draft/trainer groups matched the fresh
baseline captured for this batch. No recovery copy was applied or data reset.

- [Estimation interview list, personal workspace](estimation-question-list-20261012.png).
- [Estimation coding list, personal workspace](estimation-coding-list-20261012.png).

Next: likelihood l25, researcher l10–l18, then trader l19–l24. The goal remains
active until every topic bank, future-topic coverage guard and final
preservation/navigation audit are complete. Passing checks validate the stated
calculations and behaviour; they do not certify learning outcomes or universal
interview readiness.


## Sixth batch: likelihood l25

2026-10-12. Read the actual likelihood chapter and existing q49–q51/c15 before
selecting practice. The expanded list contains two Easy, two Medium and four Hard
interviews; coding has exactly one Easy, Medium and Hard. The existing Hard
questions remain, supplemented by deeper transfer beyond the chapter examples.
Current total: 25 lessons / 92 interviews / 38 codes; researcher route 19 checks /
83 distinct questions / 38 codes. Ten topic banks meet the contract; fifteen remain.

New questions distinguish count representation from conditioning away an
informative count, closed-domain maxima from open-domain suprema, interval-bin
probabilities from exact-duration densities, conditional selected data from full
screening/censored exposure, and Gaussian-mixture collapse from a finite optimum.
The selected-sample proof differentiates bounded-support integrals, establishes
strict monotonicity through variance, supplies limiting means and treats the
half-cutoff equality case. The mixture proof bounds every factor of the whole
record and its follow-up uses mean clipping, a variance cap and compactness to
prove existence with a known positive variance floor. Each written rubric names
its particular proof obligations. Only q49–q51's rubrics changed among the 87
preceding public interviews; all other fields and all 36 preceding public coding
records are unchanged. One chapter closing sentence now refers to linked practice
without an obsolete count; its check and lesson interactions are unchanged.

`topic_practice/likelihood.py` adds constrained Bernoulli fitting (Easy) and
selected-exponential fitting (Hard), retaining c15 as Medium. The Hard solver
uses exact integer existence decisions, scales rate by the cutoff, brackets a
unique root, switches to a small-root series to avoid cancellation and omits a
negligible large-root exponential correction to prevent overflow. The editorial
derives each step and distinguishes the fitted rate's units from the scaled root.
Integer durations are explicitly treated as exact values, not rounded bins.

Eleven independent tests in `tests/test_likelihood_practice.py` verify:

- Exact Bernoulli record/count/conditioning ratios and closed interval MLEs,
  including impossible endpoint models, empty records and huge counts.
- Integrated exponential-bin probabilities, score signs and all-zero-bin limits.
- Numerical bounded-support quadrature and derivative/variance identities,
  conditional existence boundaries and the full-screening counterexample.
- Whole-record mixture-collapse lower bounds and 500 seeded checks supporting
  the compactification inequalities. The universal existence argument is the
  written proof; finite checks alone do not establish it.
- Exact rational series division through order ten and the small-root remainder.
- A separate 85-digit Decimal root oracle based on an exponentially weighted
  score numerator, rather than the reference's reciprocal/series formula.
  It checks 150 seeded cases and all official expectations, including tiny
  positive roots and scaled rates up to 10^12. Unit scaling, permutation,
  100000-duration inputs and input preservation are checked separately.
- Actual judge acceptance of both new references, rejection of unselected and
  prior-smoothed shortcuts, and the existing debugging-copy size limit for all
  official cases. Hard coding has two examples plus fourteen hidden cases.

All 84 Python tests and 23 frontend suites passed. All 23 expanded coding
references pass the actual judge. The full frontend run includes strict parsing
of authored/generated mathematics and current/legacy journey coverage. The
[Langevin/truncated-exponential paper abstract](https://arxiv.org/abs/1501.02535)
confirms the connection between truncated exponential MLE and inversion of this
mean function; the solution and numerical checks here were derived independently.
No commercial question bank was copied and these questions are not attributed to
specific employers.

The in-app browser connection was unavailable. Chrome verified the actual
lesson → interview list → coding list handoffs, all difficulty groups, and the
Hard reference's 16/16 server submission after explicitly entering Test preview.
The new mixture proof and variance-floor follow-up rendered at 390px with zero
math errors and document width equal to scroll width. No written self-assessment
was awarded. The temporary viewport was reset and the review tab returned to the
personal likelihood coding list, showing 0/3. All five personal question, coding,
lesson, draft and trainer groups matched this batch's fresh baseline. No recovery
copy was applied and no data was reset. The server was restarted after bank changes.

- [Likelihood interview list, personal workspace](likelihood-question-list-20261012.png).
- [Likelihood coding list, personal workspace](likelihood-coding-list-20261012.png).

Next: researcher l10–l18, then trader l19–l24. The goal remains active until all
topic banks and the final preservation/navigation audit are complete.


## Seventh batch: covariance l10

2026-10-12. Read the actual covariance chapter, objectives and q20/q29 before
selecting practice. The list has two Easy, two Medium and three Hard interviews,
with exactly one code per difficulty. The original three-correlation-bound
question remains alongside deeper singular-system transfer problems. Current
inventory: 25 lessons / 97 interviews / 41 codes; researcher route 19 checks /
88 distinct questions / 41 codes. Eleven topics satisfy the contract, fourteen
remain. The chapter and its check are unchanged.

New interviews derive cross terms with consistent units, distinguish zero
variation from equality of raw levels, exhibit an incompatible table produced by
pairwise deletion, and derive its exact identity-shrinkage threshold. Hard tasks
prove the null-space/range compatibility condition for a singular covariance
extension, its residual-variance bound and an explicit joint construction; a
ridge follow-up quantifies the divergent null contribution. A second proof
characterises all sum-one minimum-variance weights, separating attainable zero
risk from singular systems with unavoidable common noise, and proves the global
bound and equality cases. Specific rubrics name these obligations. Among the 92
preceding interview records, only q20/q29 rubrics changed; every other field and
all 38 preceding public coding records are unchanged.

`topic_practice/covariance.py` adds exact two-variable PSD feasibility (Easy), a
minimum-variance nonnegative blend with integer cancellation guards (Medium),
and exact shared-factor pooling with singular covariance (Hard). The Hard task
uses a known second-moment factor model, not an estimated covariance or a promise
of out-of-sample cancellation. It derives an always-consistent equality-constrained
system, proves that its unique multiplier identifies the global minimum despite
nonunique weights, and implements rank-aware integer elimination with whole-row
gcd normalisation. It never adds a ridge or treats singularity as zero variance.
Exact reduced rational output is a pair of decimal strings, preserving values
beyond JavaScript's safe numeric range. Dimensions, signs, equality constraints,
input preservation, canonical zero output and integer bit-cost caveats are stated.

Nine independent tests in `tests/test_covariance_practice.py` cover:

- Exact finite-factor enumeration for cross terms, unit changes and centered
  deterministic relationships; pair-specific correlation calculations, a negative
  joint variance and all eigen-directions of the shrinkage repair.
- Rational orthonormal geometry, completed-square identities, explicit Rademacher
  constructions for singular block extensions, rejecting null-coupling directions
  even with huge target variance, and the exact regularisation threshold.
- Two-variable feasibility through an independent trace/determinant criterion,
  and constrained blend risks compared at exact rational candidate weights.
- A range/null-space optimisation oracle that solves a different system from the
  production multiplier reference. In 220 seeded models it supplies witness
  weights, checks stationarity and verifies the exact nonnegative objective change
  for feasible perturbations. Duplicate common-noise and zero-noise models include
  every supported estimate dimension.
- A second oracle reconstructs determinant/cofactor polynomials and takes their
  zero-ridge ratio limit in 65 models. The limit is valid because a fixed original
  minimiser bounds the ridge optimum from above and the unregularised optimum
  bounds it below. It agrees with the first oracle and integer reference. A huge
  almost-parallel factor pair has Gram determinant one and exact risk one half.
- Eighty seeded permutation, sign, unit-scaling, duplication, zero-factor and
  input-preservation checks, plus maximum 12×12 large-entry cases. All official
  expectations were calculated independently. A diagonal case has a 144-digit
  numerator and 134-digit denominator and remains exact.
- All three references pass the actual judge; strict-PD, independence and
  always-zero shortcuts fail. Every official case fits the debugging-copy size
  limit. The Hard suite has two examples plus sixteen hidden cases.

All 93 Python tests and 23 frontend suites pass after the final layout change;
all 26 expanded coding references pass the actual judge. Strict mathematical
parsing and current/legacy journey tests are included. The singular block
condition was cross-checked against
[Stanford's generalised Schur-complement statement](https://see.stanford.edu/materials/lsocoee364a/hw5extra.pdf).
[R's covariance documentation](https://www.stat.math.ethz.ch/R-manual/R-devel/library/stats/html/cor.html)
confirms that pairwise-complete calculations may yield a non-PSD matrix. The
original examples, derivations and exercise implementations here do not claim to
reproduce particular employers' interview questions.

The in-app browser connection was unavailable. Chrome verified the actual
lesson → interview list → coding list handoffs and all difficulty groups. After
explicit Test preview entry, the Hard solver passed 18/18 server cases. Copying
its final large-rational case into the debugger retained every digit and the
included three-case debug run passed without awarding completion.

The first 390px proof inspection exposed a real grid minimum-size defect: a long
equation widened the entire question panel. Grid children now have minimum width
zero so mathematical overflow stays inside its panel. The Cauchy–Schwarz proof
also defines its two coordinate vectors and breaks its displayed inequality into
three meaningful lines. After reload and explicit preview re-entry, the proof
and follow-up have zero math errors, panel width 356px and document width equal
to scroll width (390px). The equation and prose were visually inspected; these
are layout and calculation checks, not evidence of learner mastery.

Viewport settings were reset and the review tab returned to the personal
covariance coding list, showing 0/3. All five personal question, coding, lesson,
draft and trainer groups match this batch's fresh baseline. No recovery was
applied, data reset or written self-assessment awarded. The server was restarted
after bank changes. Future authoring guidance now requires checking lossless
formats for exact outputs beyond browser-safe integers.

- [Covariance interview list, personal workspace](covariance-question-list-20261012.png).
- [Covariance coding list, personal workspace](covariance-coding-list-20261012.png).
- [Narrow worked proof after the layout repair](covariance-proof-narrow-20261012.png).

Next: researcher l11–l18 and trader l19–l24. The goal remains active until all
25 topic banks, future-topic validation and final preservation/navigation audit
are complete.

## Eighth batch: regression l11

2026-10-12. Read the actual regression chapter before selecting the practice.
Added five interviews, giving 2 Easy, 2 Medium and 4 Hard. Existing q19/q21/q30
retain their meanings, numeric answers, difficulty and worked solutions; only
specific assessment rubrics replace generic ones. All 97 preceding interview
records match the previous commit apart from those three rubrics, and all 41
preceding public coding records match exactly. The original c07 remains Medium.

Easy questions derive population slope/intercept/error and transform a fitted
line plus its slope-only ridge penalty under changed units. Medium practice
constructs an orthogonal residual with confounding, then two Gaussian causal
generators with the same full observed law but different intervention effects.
The new Hard questions derive identification from two noisy measurements with
precise covariance restrictions, exhibit full-law nonidentification when sensor
errors may covary, and derive deletion errors from leverage. The latter handles
leverage one, unidentified deleted predictions, redundant-feature ridge,
unpenalized intercepts and fixed preprocessing/penalties explicitly. Hints,
complete proofs, changed-condition follow-ups and specific written rubrics are
included; a self-assessment remains distinct from automatic proof verification.

The coding list contains proposed-fit verification (Easy), original OLS (Medium)
and exact ridge leave-one-out residuals (Hard). The Hard reference builds one
integer normal matrix and computes its determinant/adjugate by fraction-free
elimination, then obtains all deletion errors in O(n(d+1)²+(d+1)³) scalar work.
Its output is a list of reduced rational pairs of decimal strings. The contract
states dimensions, empty/one-row behavior, redundant features, an unpenalized
intercept, positive fixed penalty, no mutation and additional integer bit costs.
This exact arithmetic teaching task does not prescribe explicitly inverting
floating normal equations for a production regression pipeline.

Ten independent tests in `tests/test_regression_practice.py` check:

- Exact population moments, unchanged predictions and equivalent penalties after
  unit conversion; finite-factor confounding/instrument examples and the full
  covariance tables of both Gaussian countermodels.
- An OLS deletion proof on a concrete fit, and an explicit deleted-design null
  direction at leverage one. The Gaussian full-law claims additionally use the
  mathematical fact that a centered Gaussian law is determined by covariance;
  finite enumeration alone is not presented as proving Gaussianity.
- Proposed minimizers against independently computed minimum SSE in 350 seeded
  records, constant predictors, wrong slopes with zero residual sum, and the
  maximum 100,000-row bound.
- A separate oracle refitting EACH deleted dataset using centered rational
  feature covariances and an independently solved slope system. It uses no
  full-data augmented inverse or leverage shortcut. All official expected
  results and 180 seeded models agree with the production reference.
- Analytic intercept-only errors, empty and single-row records, nearly unit
  leverage, redundant and constant columns, maximum dimension and a direct
  10,000-row six-feature large-integer case. Permuting rows/columns, changing
  feature signs/offsets, jointly scaling features/penalty, adding zero columns
  and transforming targets preserve the appropriate predictions/errors.
- Exact rational reduction, strings beyond browser-safe integers, input
  preservation, debugging-copy size limits and actual-judge checks. Mean-zero
  residual-only and always-zero shortcuts fail. A passing suite is not a formal
  asymptotic complexity proof.

All **103 Python tests** and **23 frontend suites** pass, including strict local
KaTeX parsing and all current/legacy journey bookmarks. All **28 expanded coding
references** pass the actual judge. Inventory is 25 lessons / 102 interviews /
43 codes; the researcher route has 19 checks / 93 distinct questions / 43 codes.
Twelve topics now meet the contract. The standard OLS deletion formula was
cross-checked with the
[University of Chicago computational companion](https://uchicago-pol-methods.github.io/EstimationI/ch04-sensitivity.html).
The measurement-error instrument assumptions were cross-checked with
[Angrist and Krueger's identification discussion](https://economics.mit.edu/sites/default/files/publications/Instrumental%20Variables%20and%20the%20Search%20for%20Identifi.pdf).
These sources support standard mathematical principles; the tasks, numerical
examples, countermodels, coding contract and implementations are original.

The IAB connection was unavailable. Chrome verified the actual regression
lesson → interview list → coding list handoffs, with 2/2/4 interview choices and
one code in each group. After explicit launcher entry and visible **TEST
PREVIEW** verification, the Hard reference passed **13/13** server cases. Copying
a case with 32-digit rational numerators into the debugger preserved every digit;
the three-case debug run passed and reported completion unchanged. No preview
record was imported, recovered, reset or self-assessed as personal work.

At 390px the worked deletion proof and follow-up have zero math errors, a 356px
question panel and document scroll width exactly 390px. The proof was visually
inspected, including the coefficient correction, held-out residual formula and
rank-loss argument. Viewport settings were reset. The review tab returned to
the personal regression coding list showing **0/3**. Actual personal question,
coding, lesson, draft and trainer groups match this batch's fresh baseline.
The local server was restarted after bank generation.

- [Regression interview list, personal workspace](regression-question-list-20261012.png).
- [Regression coding list, personal workspace](regression-coding-list-20261012.png).
- [Narrow worked deletion proof, test preview](regression-proof-narrow-20261012.png).

Next: researcher l12–l18 and trader l19–l24. The goal remains active until all
25 topic banks, future-topic validation and final preservation/navigation audit
are complete.


## Ninth batch: inference l12

2026-10-12. Read the actual inference chapter and its goals before selecting
practice. Added five interviews, yielding **2 Easy, 2 Medium and 4 Hard**.
The original q22/q26/q47 retain their wording, answers, difficulty and solutions;
only their specific written-assessment rubrics replace generic ones. All 102
preceding questions match the previous commit apart from those three rubrics,
and all 43 preceding public coding records remain exactly unchanged.

Easy practice derives a six-flip upper tail and inverts a specified inclusive
known-variance test, retaining its actual 95.45% coverage. Medium practice spends
an exact discrete 5% error budget using independent boundary randomization and
proves simple-model power optimality by an exchange argument. The new Hard tasks
prove a likelihood-ratio crossing bound through bounded stopped increments and
increasing crossing events, and derive all three branches of interval coverage
after a significance filter. Follow-ups distinguish predictable alternatives
from current-observation selection, extend to a conditional composite null, and
restore selected-sample coverage through independent replication or inversion
of a truncated-normal conditional pivot. Full hints, derivations and specific
rubrics accompany the original questions. Written self-assessment is not an
automated proof certificate.

The coding list has exactly one exercise per difficulty:

- Easy: invert a known-variance test with integer comparisons, inclusive
  boundaries and repeated candidate means; near-boundary large values expose
  an incorrect floating shortcut.
- Medium: calculate exact fixed-endpoint null size and alternative power from
  integer binomial recurrences, including zero flips, impossible rejection,
  certain rejection and degenerate alternatives.
- Hard: count only surviving prefixes to calculate first-crossing size/power
  and expected flips actually taken. Looks share observations. Contracts fix
  their timing, cumulative counts, endpoint inclusion and maximum horizon;
  finite-horizon calibration does not claim unlimited-horizon validity.

Rational results are canonical decimal-string pairs, rather than rounded
browser numbers. Bounds, empty inputs, mutation rules, scalar complexity and
additional integer bit costs are explicit. All copied official cases stay
within the debugger's size limit.

Twelve independent tests in `tests/test_inference_practice.py` check:

- Exhaustive six-flip records, actual size and power, exact randomized boundary
  mass and likelihood-ratio ordering; test/interval duality and width scaling.
- Finite binary records for stopped likelihood-ratio expectations, predictable
  adaptation and a current-flip counterexample. The written infinite-horizon
  claim uses the event limit; finite enumeration alone does not prove it.
- Selected-interval coverage against independent numerical integration of the
  normal density, all branches and their boundaries; conditional-pivot
  quantiles, 95% conditional mass and independent-replication factorization.
- Exact rational-statistic Easy checks on 250 seeded inputs, a difference-one
  large-integer boundary and the maximum 100,000 candidate bound.
- Fixed-endpoint probabilities against independent combination formulas and
  complete small binary records, rather than the production integer recurrence.
- Sequential size/cost against both exhaustive ordered records and a backward
  conditional-probability recursion using `Fraction`. All official expected
  results, 120 seeded procedures and the maximum 120-flip case agree.
- One-look equivalence, impossible/empty looks, alternative probability
  reparameterization, input preservation, exact JSON round trips, actual judge
  execution and rejection of always/never-reject and floating shortcuts.

All **115 Python tests** and **23 frontend suites** pass, including strict local
KaTeX parsing and current/legacy journey bookmarks. All **31 expanded coding
references** pass the actual judge. Inventory: 25 lessons / 107 interviews /
46 codes; researcher route: 19 checks / 98 distinct questions / 46 codes.
Thirteen topics meet the contract; twelve remain pending.

The crossing principle was cross-checked with
[Ramdas's CMU notes on Ville's inequality](https://www.stat.cmu.edu/~aramdas/martingales18/L13-Ville%27s.pdf).
The conditional-pivot principle was cross-checked with
[Tibshirani et al.'s exact post-selection inference paper](https://www.stat.berkeley.edu/~ryantibs/papers/lassoinf.pdf).
These support standard mathematical principles; the six-flip examples,
scalar significance-filter task, coding specifications and implementations are
original. The bounded-stop proof avoids asserting an expectation identity at an
unbounded stopping time without its required conditions.

The IAB backend was unavailable. Chrome verified lesson → interview list →
coding list, freely chosen 2/2/4 questions and one code in each group. After
explicit launcher entry and visible **Test preview** verification, the Hard
reference passed **13/13** complete server cases. Copying submission case 13,
with hundreds of decimal digits in exact rational components, preserved its
string values. The copied case plus two examples passed **3/3** debug checks;
the UI explicitly reported debugging only and completion unchanged.

The Hard selected-interval proof and follow-up were checked at a 390px viewport:
zero math-render errors and no page-width overflow (document scroll width
375px, available viewport 390px). The piecewise formula was visually inspected
inside its 289px solution block. Viewport override was reset, and the review
tab returned to the personal inference coding list showing **0/3**. Personal
question, coding, lesson, draft and trainer groups match this batch's fresh
pre-edit baseline. No personal assessment was awarded, reset or recovered.
The local server was restarted after the generated bank changed.

- [Inference interview list, personal workspace](inference-question-list-20261012.png).
- [Inference coding list, personal workspace](inference-coding-list-20261012.png).
- [Narrow selected-interval proof, test preview](inference-proof-narrow-20261012.png).

These checks verify the specified cases and navigation; they do not certify
employer difficulty, learning outcomes, physical touch or screen-reader use.
Next: researcher l13–l18 and trader l19–l24, followed by the final site-wide
preservation/navigation audit. The full goal remains active.


## Tenth batch: time series l13

The actual authored lesson and learning goals were reviewed before selecting
practice. l13 retains original q18/q31 and c08 and now has **2 Easy, 2 Medium,
4 Hard interviews** and exactly **one coding exercise per difficulty**.
The six new interviews are original:

- Three-observation stationary covariance counting, negative correlation and
  variance versus standard-error inflation.
- Conditional forecast error as future innovation loadings, shared forecast
  errors and the limits of variance-only prediction intervals.
- Gaussian innovation products with zero return autocovariance but dependent
  squares; exact uncertainty for the nonlinear risk target.
- Overlapping summed labels, finite lag counts and the unequal weights placed
  on underlying returns; disjoint-label and direct-mean comparisons.
- Explicit minimum-variance deterministic unbiased weights under a known AR
  covariance; positive definiteness, uniqueness and same-sample weight bias.
- A stationary Gaussian triangular array with persistence exp(-c/n), its
  covariance integral and failure of a fixed-rho shortcut. The follow-up changes
  initial-state and innovation-variance assumptions separately.

Every task has hints, worked reasoning, a substantive follow-up and specific
assessment obligations. q18/q31 change only their rubrics. All **107 preceding
interview records** otherwise match the preceding commit; all **46 preceding
public coding records** remain exactly unchanged. No original identifier or
assessment meaning is replaced.

Easy coding computes exact finite mean variance from feasible lag covariances,
including zero variance, negative lags, irrelevant supplied lags, long kernels
and large integer bounds. Medium remains the original sample-autocorrelation
exercise. Hard coding filters a scalar Gaussian latent state observed with
noise and answers unordered, repeated forecasts conditional only on information
through each asof. Missing measurements, deterministic states, unit roots,
negative persistence and future observations have explicit semantics. The
Gaussian update is supplied as a prerequisite; forecasting requires deriving
and applying the innovation recurrence. Canonical string rational pairs avoid
browser integer rounding. Bounds, input preservation and rational-operation
complexity plus bit/gcd/string costs are explicit.

Twelve independent time-series tests check finite covariance matrices and
innovation loadings; finite moment-matching enumeration for the nonlinear
risk example; exhaustive small overlapping labels; dense exact covariance
solutions for optimal weights; changing-persistence sums at increasing sample
sizes; 180 seeded moving-average kernels for Easy coding; and 90 seeded latent
models against joint Gaussian conditioning by independent Fraction matrix
elimination. That oracle does not reuse the production filtering recurrence.
Further checks cover causal prefixes, signs, probability reparameterization,
request ordering, maximum time and 10000 requests, fixture-contract bounds,
actual judge execution, input preservation and lossless debug-case round trips.
Finite checks support the written derivations; they are not proofs of arbitrary
limit theorems or Gaussianity of the moment-matching proxy.

All **127 Python tests** and **23 frontend suites** pass. All **33 expanded
coding references** pass the actual judge. Inventory: **25 lessons / 113
interviews / 48 codes**; researcher route: **19 checks / 104 distinct questions /
48 codes**. Fourteen topics meet the contract; eleven remain pending.

The scalar state-space conditioning principle was cross-checked against
[Zivot's University of Washington state-space/Kalman notes](https://faculty.washington.edu/ezivot/econ584/notes/statespacemodels.pdf).
The exercise specification, finite examples and exact-arithmetic implementation
are original, rather than copied interview questions.

Chrome reviewed the actual lists and the Hard proof. Earlier in this batch,
after explicit launcher entry and visible **Test preview** verification, the
Hard reference passed **11/11** complete server cases. Submission case 10,
containing 392-digit rational components, was copied into the debugger and
passed **3/3** checks with its examples; debugging reported completion unchanged.
Only explicit preview held those development results.

The final changing-persistence proof and follow-up were checked at a **390px**
viewport. Long integral equality was revised into three mathematical lines:
its solution and display widths are **289px**, with equal scroll widths; the
follow-up display is 255px. Document width is **375px**, and there are **zero
math-render errors**. The actual screenshot was visually inspected. The
viewport was reset; the browser returned to the personal coding list showing
**0/3**, while its interview stage shows **0/8**. All five personal question,
coding, lesson, draft and trainer groups match the fresh pre-edit baseline.
No personal assessment was awarded, reset or recovered. The local server was
restarted after generating the new bank; later changes only polished notation.

- [Time-series interview list, personal workspace](time-series-question-list-20261012.png).
- [Time-series coding list, personal workspace](time-series-coding-list-20261012.png).
- [Narrow changing-persistence proof, isolated preview](time-series-proof-narrow-20261012.png).

These checks establish the stated mathematical cases and observed UI behavior;
they do not certify firm-specific interview difficulty, learning outcomes,
physical touch or screen-reader use. Next: researcher l14–l18 and trader
l19–l24, followed by the final site-wide navigation/preservation audit.
The full goal remains active.


## Eleventh batch: validation l14

The authored validation lesson and learning goals were inspected before
selecting practice. The topic now has **2 Easy, 2 Medium and 2 Hard interviews**
and exactly **one coding exercise per difficulty**. Existing q27/q28 remain,
with specific rubrics; q27's casual "touch" wording is clarified to overlapping
test-label information. Its original prompt, written grading meaning and
follow-up remain. All **113 preceding interview records** otherwise match the
preceding commit, and all **48 preceding public coding records** remain exact.

Four original interviews practice distinct evaluation failures and reasoning:

- Historical decisions with features received too late or labels not yet mature;
  inclusive versus strict receipt boundaries and causal missing-input policies.
- Decision-weighted versus equally weighted block scores, defining the estimand
  before assigning uncertainty to an aggregated number.
- Disjoint half-open intervals versus chronological availability, including
  delayed label publication and why purging does not establish independence.
- Honest predictable adaptive evaluation. The argument defines its nested
  information sets, centered increments and random conditional-risk target,
  proves zero cross moments, and derives a fixed-horizon Chebyshev band. A
  two-fair-outcome counterexample separates predictable adaptation from choosing
  the best retrospectively scored constant classifier. The selected reported
  loss is 1/4 while independent future error is 1/2.

Every new interview includes hints, justified worked reasoning, a substantive
follow-up and specific self-check obligations. A numeric answer does not assess
the unwritten reasoning. The uncertainty argument evaluates the recorded
procedure's average conditional risk, not a frozen final model or future regime.

Easy coding preserves original sample indices while checking historical
feature and label receipt boundaries. Medium retains c09 interval purging.
Hard coding audits many candidate folds with independently delayed labels,
a rolling lower bound on sample starts and a protected half-open information
block. A receipt-time sweep and nested compressed Fenwick counts implement
independent maturity/causality/overlap constraints without scanning every row
per query. The two non-overlap branches are proved disjoint; exact endpoint
rules, duplicate samples/queries, ordering, mutation, bounds and complexity
including query sorting are stated. Arbitrary historical protected blocks
serve the declared interval-audit contract, not a claim of forward-deployment
validity. Future coordinate support never activates future labels.

The old second Medium c10 remains available through `LEGACY_CODING_LINKS` and
`legacyCoding` as **Additional practice**. Its draft, result and permanent
standalone/journey URLs survive; its pass does not fill one of the three
current coding slots. Automated journey tests now exercise this exact l14
bookmark and preserve a synthetic old draft separately from real user data.

Twelve independent validation tests check:

- Availability, weighting and half-open boundaries by direct membership and
  explicit half-unit interval sets; the original c09/c10 examples remain valid.
- Exhaustive fair-bit histories under three predictable policies and an exact
  dependent-outcome model with genuinely varying conditional-risk averages.
  Their probability-weighted centered moments agree with the written argument.
- Exact retrospective selection over the four binary pairs and an independent
  future bit; finite checks support the proof rather than replace it.
- Exhaustive small Easy row pairs, feature/label bounds and 100000 rows.
- 240 seeded Hard instances against direct per-query intersection membership,
  independently of the reference's sweep, complement and Fenwick structure.
- Every authored fixture, row/query permutations, duplicate multiplicity,
  prefix-only equivalence, future-label additions, timestamp endpoints,
  maximum 20000 rows and queries, input preservation and empty cases.
- Actual judge execution, rejection of a maturity-only shortcut, official
  debugging-copy size bounds and exact serialization round trips.

All **139 Python tests** and **23 frontend suites** pass. All **35 expanded
coding references** pass the actual judge. Inventory: **25 lessons / 117
interviews / 50 codes**; researcher route: **19 checks / 108 distinct questions /
49 current codes**. c10 remains in the coding library and saved-work history
outside current route slots. Fifteen topics meet the contract; ten remain pending.

Standard preprocessing and selection distinctions were cross-checked with
[scikit-learn's leakage guidance](https://scikit-learn.org/stable/common_pitfalls.html)
and its [nested-evaluation example](https://scikit-learn.org/stable/auto_examples/model_selection/plot_nested_cross_validation_iris.html).
The finite examples, adaptive-risk argument, exercise contracts and code are
original; no commercial interview content was copied.

Chrome verified lesson → question list → coding list with the correct grouped
counts. In explicit **Test preview**, the Hard reference passed **9/9** complete
server cases. Submission case 9 copied **3000 rows and 2000 queries** exactly
(arguments JSON 120857 characters, expected JSON 9890); with the two examples,
the debugger passed **3/3** and explicitly reported completion unchanged.
The old c10 personal bookmark visibly labels Additional practice and retains
its module/list return. No personal grading occurred.

The final adaptive proof and follow-up were reviewed at **390px** viewport:
zero math-render errors, document width **375px**, solution **289px**, and
multiline display **289px** with equal scroll width. Actual screenshots were
visually inspected. Viewport was reset and the tab returned to the personal
coding list **0/3**, with interview stage **0/6**. Personal question, coding,
lesson, draft and trainer groups match the fresh pre-edit baseline. No personal
assessment was awarded, reset or recovered. Server restarted after generating
the new bank; later changes only clarified prose and mathematical notation.

- [Validation interview list, personal workspace](validation-question-list-20261012.png).
- [Validation coding list, personal workspace](validation-coding-list-20261012.png).
- [Narrow adaptive-evaluation proof, isolated preview](validation-proof-narrow-20261012.png).

These checks establish the specified cases and observed navigation, not
employer-certified difficulty, learner mastery, touch or screen-reader use.
Next: researcher l15–l18 and trader l19–l24, then final site-wide navigation
and preservation audit. The full goal remains active.

## Twelfth batch: search and multiple testing

Read the actual `static/lesson-search.js` body before selecting tasks. l15 now
has **two Easy, two Medium and two Hard interviews**, plus exactly one coding
exercise per difficulty. Added three interviews and three codes. Existing q04,
q25 and q32 remain linked under their permanent IDs and retain grading meaning.
All **50 prior coding records** remain exact after JSON parsing. Of 117 prior
questions, 114 are exact; q04 changes only its rubric; q25 replaces ambiguous
nominal-level wording with the intended EXACT true-null rejection probability
and adds its rubric; q32 adds specific assessment obligations and the identical-copy
exception to its correlated-search follow-up. Their answers/prompts otherwise
remain intact. Current inventory: **25 lessons / 120 interviews / 53 codes**;
researcher route **19 checks / 111 distinct interviews / 52 current codes**.
**16 topics complete; nine pending.**

The interviews distinguish mean false-discovery fractions from pooled counts,
FWER from expected false reports, copied decisions from independent candidates,
and selected-score optimism from the selected candidate’s own true value.
The hard Gaussian derivation handles correlation ±1 and unequal means; shared
confirmation noise exposes why a separate file alone is not independent evidence.
Coding progresses from repetition summaries to exact rational Holm adjustment
and exhaustive balanced-assignment calibration of a jointly searched maximum.
The latter explicitly supplies the exchangeable GLOBAL null, includes ties and
the observed assignment, and claims only global-null family calibration. It
neither permits arbitrary chronological shuffles nor asserts strong partial-null
control without additional assumptions. Rational outputs use canonical decimal
string pairs, not rounded p-values.

**151 Python tests and all 23 frontend suites passed.** Twelve new tests compare
Holm against exhaustive closed Bonferroni intersection testing (including ties,
unreduced fractions and exact rejection boundaries), check finite independent
and copied valid true-null families with a false-null candidate, and verify
20,000-hypothesis boundaries. Discovery summaries use exact Fraction oracles.
Randomization is independently computed by balanced binary vectors and direct
rational group means, with 100 seeded matrices at n=2,4,6,8. Finite global-null
ranks are checked for super-uniformity, ties and equivalence of any adjusted
rejection to global rejection. Checks include row/column permutation, complement
assignments, copied/sign-reversed columns, and dominance over individual tails.
For n=18,m=8, two extreme assignments out of 48,620 give exactly **1/24,310**.
Independent quadrature checks the Gaussian truncated-normal first moment;
algebra checks the endpoint variance decomposition. All **38 expanded coding
references** pass their actual complete judge, including all three new references.
Input preservation and every official debugging-copy round trip are checked.

Chrome opened the explicit launcher and visibly verified **Test preview** before
all grading and solution inspection. A freely selected Easy accepted **271/1000**
and returned through the list/stage flow. The Hard reference passed **8/8** through
the UI in **235 ms** (observed once, not a runtime guarantee). Copying Submission 5
into the debugger retained **18 rows, eight columns, nine group-one assignments**
and the string pair **["1","24310"]**; its debugging run passed **3/3** and did not
award extra completion. The hard solution and unequal-mean follow-up were checked
at **390px** viewport: document width **375px**, primary solution/display **289px**,
follow-up display **255px**, equal scroll widths and zero KaTeX errors. No console
errors were observed. The narrow proof crop was visually inspected. Viewport reset;
tab left at the personal question list **0/6**, coding stage **0/3**. All five personal
record groups match the fresh pre-edit baseline; no personal assessments/drafts
were reset or credited. The local server was restarted to load the new judge bank.

- [Interview list, personal workspace](search-personal-question-list-20261012.png).
- [Interview list, isolated preview](search-question-list-20261012.png).
- [Coding list, isolated preview](search-coding-list-20261012.png).
- [Narrow Gaussian derivation, isolated preview](search-proof-narrow-20261012.png).

Primary method references consulted: [statsmodels Holm implementation](https://www.statsmodels.org/stable/_modules/statsmodels/stats/multitest.html)
and [SciPy exact permutation-test documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.permutation_test.html).
The content, proofs and integer implementation are original; no package is added
to the learner runner. These checks establish stated mathematical examples and
observed UI behavior, not employer difficulty, learner mastery or independent
pedagogical certification. Next: **l16–l18 and l19–l24**, then the final broad
navigation/preservation audit and removal of the temporary pending exception.
The full goal remains active.

## Thirteenth batch: research defence

Read the actual `static/lesson-research-defence.js` body and l16 learning metadata
before designing its practice. Added four interviews and two coding exercises.
l16 now has **two interviews per difficulty and exactly one code per difficulty**.
Existing q33/q34 stay in place; only their generic rubrics become specific evidence
obligations. All **118 other preceding questions and all 53 preceding public
coding records remain exact** after JSON parsing. The Medium c11 keeps its original
lagged exposures, two-unit reversal turnover and no-terminal-charge conventions.
Current inventory: **25 lessons / 124 interviews / 55 codes**; researcher route
**19 checks / 115 distinct interviews / 54 current codes**. **17 topics complete;
eight pending.**

The interviews require explicit economic payoffs before turning a hit rate into
profit, distinguish conditional fills from all posted opportunities, and quantify
how unchanged conditional accuracy can reverse a model-versus-baseline result
when the market-state mix changes. The hard question defines a fixed-policy
inverse-propensity evaluation model completely, then derives its mean, variance,
selective-observation contrast and sharp missing-support bounds. It makes action
randomization, overlap, net liquidation accounting, independence and excluded
interference explicit. It does not infer those assumptions from a historical log;
weight clipping and post-selection are distinct procedures.

The new Easy coding task counts paired correctness disagreements rather than
manufacturing profit from accuracy. Hard coding minimizes fixed state payoffs over
a declared total-variation ball, including zero-count states, ties and unused
budgets. The derivation gives both a feasible transfer witness and a lower bound
over ALL continuous probability vectors. Returned mean and least used distance
are canonical decimal string fractions. The task changes only regime composition;
it explicitly excludes uncertain state payoffs, execution validation and unknown
states. Its optimum is a sensitivity calculation for a fixed rule, not hindsight
trade selection or a live profitability claim.

**163 Python tests and all 23 frontend suites passed.** Twelve new tests enumerate
all paired binary forecast triples through length four and check the 100,000-row
limit; 200 seeded lagged-accounting checks use a separate exact rational holding
path. Finite randomized-action worlds check inverse-propensity first/second moments
and the example value **1**, traded-only mean **0** and score variance **53/3**.
An unrecorded-action-selection counterexample preserves known marginal propensity
while breaking identification. Missing-support endpoints and clipping bias are
checked separately. The robust coding reference is compared with an independent
exact rational LP: enumerate vertices of a total-variation EPIGRAPH, then minimize
payoff and distance lexicographically, without using donor sorting. These cases
have at most three states. A second oracle enumerates admissible mass vectors for
150 seeded cases with up to four states. Checks cover insufficient donor mass,
multiple minima, all-equal payoffs, zero-count minimum states, permutation and
unreduced budget invariance, 20,000 states and boundary integers. Every official
small hard fixture is also checked against the continuous LP. All **40 expanded
coding references** pass their actual complete judge; both new references and
retained c11 preserve inputs and exact official debugging-copy round trips.

Chrome explicitly entered the launcher and visibly verified **Test preview**
before every grade/reveal. A freely chosen Easy accepted **−1/2**. The Hard reference
passed **11/11** through the UI (**1.3 ms** observed once). Submission 11 copied
exactly into the debugger with worst-mean strings
**["68999994274000048447","1999999795000004473"]**, both beyond JavaScript’s safe
integer range, and used distance **["1","999999929"]**. The debugging rerun passed
**4/4** without extra completion. The actual lesson’s Next step returned to the
question list, and the list continued to the coding list. Hard proof and support-bound
follow-up at **390px**: document width **375px**, main solution/display **289px**,
follow-up display **255px**, matching scroll widths, zero KaTeX errors. The proof
crop was visually inspected. No console errors observed. Viewport reset; the tab
was verified at the personal question list **0/6**, coding stage **0/3**, after an
explicit navigation wait confirmed the personal URL. All five personal record
groups match the fresh pre-edit baseline; no personal credit/reset occurred.
Server restarted to load the new judge bank.

- [Interview list, personal workspace](defence-personal-question-list-20261012.png).
- [Coding list, isolated preview](defence-coding-list-20261012.png).
- [Narrow policy-identification proof, isolated preview](defence-proof-narrow-20261012.png).

Primary context consulted: [Dudík, Langford and Li, policy evaluation, section 2.1](https://icml.cc/2011/papers/554_icmlpaper.pdf).
The toy experiments, calculations, wording and code are original. No package is
added to the student runner. These checks verify stated mathematics and observed
navigation, not employer difficulty, learner mastery, live execution or physical
touch/screen-reader interaction. Next: **l17–l18 and l19–l24**, then the required
final broad navigation/preservation audit and removal of the pending-topic exception.
The full goal remains active.


## Fourteenth expansion batch: Monte Carlo, l17

Read the actual authored simulation lesson before selecting this practice. Added
four interviews and two coding exercises, completing **2 Easy / 2 Medium / 2 Hard**
and **one code per difficulty**. Retained c12 Medium exactly, including its fixed
coefficient, empty/singleton rules and original tests. All **55 prior public code
records** and **122 of 124 prior interview records** remain exact. q43 changes
rubric only. q48 adds its necessary finite-second-moment assumption and expresses
the optimum residual variance without undefined correlation for a constant target;
ID and assessment meaning remain unchanged. Current inventory: **25 lessons /
128 interviews / 57 codes**; researcher route **19 checks / 119 distinct interviews /
56 current codes**. **18 topics complete; seven pending**.

Interviews distinguish pair averages from dependent component outputs and compare
variance at the same number/cost of evaluations. The zero-hit question proves a
complete, conservative one-sided confidence procedure, includes endpoints and
minimum fixed sample count, and gives an almost-sure miscoverage counterexample
under repeated block selection. The fitted-control question enumerates all nine
same-sample outcomes, then conditions on an independent pilot: unchanged target
mean, noisy-coefficient variance and zero variance of its conditional mean are
separate facts. Hard retained questions derive antithetic moments and optimum
control coefficients with specific assessment obligations.

Easy coding uses exact integer pair totals before final float conversion to retain
small variation around large offsets. Hard coding minimizes stratified simulation
variance under explicit independent with-replacement draws, equal costs, known
population variances and mandatory positive counts. A decreasing marginal-gain
proof establishes a global integer optimum; exact comparison and original-index
ties yield the lexicographically largest optimal allocation. Returned variance
uses reduced decimal string fractions. No continuous-allocation rounding, guessed
pilot precision or financial-profit claim substitutes for this contract.

**175 Python tests and all 23 frontend suites passed.** Twelve new tests use exact
polynomial integrals, a specified finite joint law, rational-grid coverage checks,
all nine same-sample and 81 independent-pilot worlds, 250 centered-rational pair
checks and 200 independent retained-control checks. Allocation is verified against
ALL positive integer compositions for 180 seeded instances with up to five strata
and budgets through 12, plus a grid of two-stratum weights/variances and every
small official fixture. Scaling, monotonicity, zero gains, mandatory zero-weight
strata and the full 20,000-stratum/200,000-draw limits are checked. A Pell identity
separates two large marginal priorities by exactly one, where floating arithmetic
ties them. All **42 expanded references** pass their actual complete judge.

The maximum allocation fixture exposed a genuine debugging-copy boundary:
spaced JSON was **200,057** characters across arguments and expected output, above
the existing 200,000-character per-case limit. `case_copy` now emits compact JSON
without changing any value or that limit. All official cases round-trip through
the actual parser, including the unchanged full maximum fixture. Python debugging
regressions and the frontend debugging suite pass; no fixture scope was reduced.

Chrome explicitly entered the launcher and visibly verified **Test preview** for
all grades/reveals. Easy **3/8** was accepted. Hard code passed **9/9**, observed
**726.2 ms** once. The large exact variance
**["1771308307978070401","3441313796169221282"]** survived actual UI debugging copy;
the rerun passed **4/4**, with completion unchanged. The authored lesson continues
to the interview list; a freely chosen detail continues to the coding list. At
**390px**, the coefficient matrix and pilot-variance displays had widths/scroll
widths **304/304px** and **270/270px**, with document width **390px** and zero KaTeX
errors. The saved narrow proof was visually inspected. No console errors observed.
Viewport reset; explicit navigation confirmed the personal question list **0/6**
and coding stage **0/3**, with no preview notice. Questions, coding, lessons, drafts
and trainers match the fresh pre-edit baseline; no personal credit/reset occurred.
Server restarted to load the expanded judge and compact-copy change.

- [Interview list, personal workspace](monte-carlo-personal-question-list-20261012.png).
- [Coding list, isolated preview](monte-carlo-coding-list-20261012.png).
- [Narrow independent-pilot derivation, isolated preview](monte-carlo-proof-narrow-20261012.png).

Primary context consulted: [Wright, exact integer stratified allocation, Census
Bureau](https://www.census.gov/library/working-papers/2014/adrm/rrs2014-07.html).
Our toy uses an explicitly with-replacement simulation contract; its wording,
proof, fixtures and code are original. These checks establish stated mathematics
and observed navigation, not employer calibration or learner mastery. Next:
**l18 and l19–l24**, then the final broad navigation/preservation audit and removal
of the pending-topic exception. The full goal remains active.


## Fifteenth expansion batch: researcher algorithms, l18

Read all of the actual authored algorithm lesson and its goals: centred streaming
moments, dominance/expiry, amortised costs and information availability. Added
five interviews and one coding exercise to complete **2 Easy / 2 Medium / 2 Hard**
and **one code per difficulty**. All **128 prior interview records** and **57 prior
public coding records** remain exactly unchanged. q44 remains shared with l08,
including its existing specific timing rubric. Retained c05 Medium and c13 Hard
with every original prompt, assessment, reference and full fixture. The old c14
calibration bookmark is registered as l18 additional practice; its draft/results
remain and its current l24 trader link is preserved. Current l18 lists, resume and
evidence use only the three current slots. Inventory: **25 lessons /133 interviews /
58 codes**; researcher route **19 checks /124 distinct interviews /56 current codes**.
**19 topics complete; six trader topics pending**. Every shared/researcher topic
now meets the coverage contract; the full goal and final audit remain open.

Easy questions distinguish old/new means and earliest-versus-newest maximum
indices. Medium asks for a mergeable centred summary with count-weighted and
between-batch terms, empty/singleton rules, disjointness and exact-versus-floating
associativity. Hard practice derives remove-then-add moments, proves insufficient
state using indistinguishable ordered windows, and gives a binary-state information
lower bound with its precise bit/word distinction. Its numerical discussion does
not turn an exact identity or a clamped negative into an accuracy guarantee. The
other Hard question proves that a lazily cleaned heap can answer correctly yet
retain Θ(n) entries at fixed k, then proves earliest-tie deque dominance, amortised
costs, a costly individual update and the failure under backward re-expansion.
These are reasoning contracts rather than performance slogans.

New Easy coding keeps the earliest argmax for each prefix, including negative
values and equal records. It retains the entire prefix rather than silently
substituting a rolling window. Medium excludes the current observation; Hard
includes it. Keeping their original meanings protects existing study work.

**188 Python tests and all 23 frontend suites passed.** Twelve new topic tests
check 200 exact-rational Welford prefix sequences, 200 independently centred batch
partitions with both merge associations, exhaustive small tie-index windows,
remove/add windows through width five, and distinct binary continuation signatures
through width eight. They separate correct lazy-heap roots from retained size and
count logarithmic push swaps on increasing input. Deque traces check index/value
ordering, eligibility, single-removal obligations, aggregate costs and a full-window
pop burst. Prefix code is compared with exhaustive prefix scans through length
seven and checked at 100,000 observations. Retained rolling tasks have 300 seeded
slow-window comparisons, no-mutation checks, current-observation perturbations and
the original 30,000-observation maximum fixture. All **43 expanded references**
pass the actual full judge. Every official current l18 case round-trips through
the debugging parser.

That last check exposed an existing limitation: c13’s full large official case has
**168,899 argument characters +90,007 expected characters =258,906** in compact
JSON, above the former 200,000-character limit. Both frontend and backend now
allow **500,000 characters per debugging case** and retain their upper-bound
checks. No official fixture, correctness assertion, execution time limit or
request-size bound was reduced or removed. A new backend regression accepts the
exact 500,000 boundary and rejects 500,001; frontend regressions accept a large
copied case and reject oversize text. API request size remains bounded at 2 MB.
App asset version was advanced so existing tabs load the matching frontend rule
when reopened. No new dependency or AI assistance was added.

Chrome visibly verified **Test preview** after every explicit launcher entry.
Numeric **20** was accepted. New Easy passed **8/8** (1.6ms observed), retained Hard
passed **6/6** (8.4ms observed). Its full large case copied without loss/truncation:
argument and expected lengths/endpoints matched the official case, and the sample
plus copied case passed **2/2** as debugging only, with no additional completion.
The saved c14 l18 URL opens labelled Additional practice with the same topic
return. A frontend fixture additionally proves an old c14 pass does not fill an
l18 slot while still counting as current l24 evidence, and retains its draft.
The actual lesson continues to the interview list, and a freely chosen detail
continues to the coding list.

At **390px**, removal/insertion displays had matching width/scroll width **304px**;
the binary reconstruction display **270px**. Document width/scroll width **390px**,
zero KaTeX errors. Both saved proof crops were visually inspected. On reopening,
the worked-solution reveal was already retained: a Show selector had no match;
inspection confirmed Hide worked solution, then only the follow-up was opened.
This was restored attempt state, not a website failure. No console errors observed.
Viewport reset; explicit navigation confirmed personal mode. Both personal lists
are **0/6 interviews and 0/3 codes**; questions, coding, lessons, drafts and trainers
match the fresh pre-edit baseline. No personal credit/reset occurred. Tab left at
the personal interview list; server restarted for the expanded bank/debug rule.

- [Interview list, personal workspace](algorithms-personal-question-list-20261012.png).
- [Coding list, personal workspace](algorithms-personal-coding-list-20261012.png).
- [Narrow rolling-moment derivation, isolated preview](algorithms-proof-narrow-20261012.png).
- [Narrow bit-state lower bound, isolated preview](algorithms-state-bound-narrow-20261012.png).

Primary context consulted: [Python deque operation costs](https://docs.python.org/3/library/collections.html#collections.deque)
and [Chan, Golub and LeVeque, variance analysis abstract](https://www.tandfonline.com/doi/abs/10.1080/00031305.1983.10483115).
Toy examples, proofs, wording and code are original. Verification establishes
these declared calculations/contracts and observed navigation, not employer
calibration, learner mastery or physical touch/screen-reader interaction. Next:
**l19–l24**, then the required full navigation/preservation audit and removal of
the pending-topic exception. The full goal remains active.

## Sixteenth batch: fair value, l19

Read the authored `static/lesson-fair-value.js` and its learning goals before
selecting practice. The completed bank has **two Easy, two Medium and two Hard
interviews**, and **one code at each difficulty**. Five interviews and three codes
are new. The existing q35 prompt, answer, tolerance, hints, solution and follow-up
are preserved; only its generic rubric becomes specific to die means, executable
sides and a revealed die. All **133 prior interview records** retain their grading
meaning; q35’s rubric is the only prior record difference. All **58 prior public
coding records** are exact. No old links, assessments or drafts were removed.

The progression is specific to the lesson: cash profit at settlement versus an
executable early exit; joint-record Bayesian updates when components are dependent;
physical expected payment versus a two-state replicating portfolio; optimised
information value with fixed actions versus a dealer that updates the quote;
and a set of ambiguous priors versus a hierarchical mixture whose model weights
must also be conditioned. Worked answers show the normalising probability,
conditional means, cash-flow signs and costs. Written tasks have explicit proof
and counterexample obligations; numeric acceptance does not certify those proofs.
The robust interview uses one common adverse model to rule out randomisation,
rather than incorrectly mixing different worst-case models for each action.

Easy code computes exact weighted payoff and executable edges. Medium conditions
every signal in a finite joint model, returning an explicit unreachable result
for zero-probability signals; its marginal probabilities and conditional means
satisfy mass/tower conservation. Hard optimises a conditional ratio over bounded
REAL prior weights with one total-mass constraint. Its proof uses vertices with
at most one non-bound coordinate and denominator-weighted convex combinations.
A supplied counterexample defeats sorting only by raw payoff. The declared small
state bound supports exponential vertex enumeration; the explanation separates
arithmetic-operation cost from unbounded-integer bit cost. Inputs are preserved.
Every exact rational uses canonical decimal strings, including integers and zero;
no rounded numerical output stands in for an exact pricing boundary.

**199 Python tests and all 23 frontend suites pass.** Eleven new topic tests check
cash flows, exact dependent-signal posteriors/tower identities, replication in
both states, actual noisy-signal loss outcomes, 300 rational convexity checks,
model-weight updating and the ambiguity interval. Code is checked using independent
Fraction probability models: 350 seeded weighted distributions, 180 joint signal
models with marginal/tower/scaling checks, and 180 bounded-prior models against
ALL small integer compositions, not the reference’s vertex shortcut. Permutations,
weight/likelihood scaling and real convex mixtures are also checked. Fixed bounds,
zero state weights, impossible signals, negative payments, zero edges, total mass
at both bound-sum extremes and n=1 are covered. Maximum lengths/magnitudes and
lossless copied results are verified. All **46 expanded reference solutions** pass
the actual complete judge. All official l19 case copies round-trip through the
backend parser and their rational strings are reduced/canonical. The largest
copy has 400,014 argument characters and remains within the existing 500,000
combined-character cap. No fixture or execution/request bound was weakened.

The initial debugging-test call supplied already-parsed objects to `run`, which
expects original JSON-text copies; it was corrected to test the actual API input.
The first frontend run preceded rebuilding `static/coding.json` and detected its
missing new IDs. Both public banks were rebuilt before rerunning all suites.
Final strict rendering checks parse **2,693 authored/generated math spans**.
No dependency or AI assistance was added.

The in-app browser connection was unavailable; the existing Chrome session was
used. Each grading/solution session entered the explicit launcher and visibly
verified **Test preview**. Numeric **3/4** was accepted. Easy passed **7/7** (3.8ms
observed), Medium **6/6** (9.2ms), Hard **9/9** (35.2ms). The full 100,000-state
Easy case copied with all 400,014 argument characters and ran with both samples,
**3/3**, debugging-only. The Hard fraction numerator **999999999000000000** and
its denominator **1000000001** survived the actual expected-output textbox and
copied-case run, **3/3**, with no extra completion. An observation selector matched
two result headings; inspecting the result selected the specific passed-tests
heading without repeating grading. Reloads returned to personal mode and preview
was explicitly re-entered. A previously revealed worked solution restored as
Hide worked solution; its separate follow-up was opened for inspection.

The actual lesson hands off to the interview list. A freely chosen question
continues to the coding list; Hard code is selectable before Easy or Medium and
returns to that same list. At **390px**, the information-value displays have
matching width/scroll width **304px**, the ambiguity display **304px**, and the
Hard code’s payoff-ratio/vertex displays **302px/256px**. Document width and scroll
width are both **390px**, with no KaTeX errors. Saved proof crops and both personal
lists were visually inspected. No browser console errors observed. Temporary
viewport was reset; browser left at the personal interview list with **0/6
interviews and 0/3 code passes**. Personal questions, coding, lessons, drafts and
trainers equal the fresh pre-edit baseline. No personal credit or reset occurred.

- [Fair-value interviews, personal workspace](fair-value-personal-question-list-20261012.png).
- [Fair-value coding list, personal workspace](fair-value-personal-coding-list-20261012.png).
- [Fixed-action information-value proof, isolated narrow preview](fair-value-information-proof-narrow-20261012.png).
- [Conditional-ratio vertex proof, isolated narrow preview](fair-value-vertex-proof-narrow-20261012.png).

Primary context consulted: [Jane Street’s stated probability/expected-value/market
preparation topics](https://www.janestreet.com/probability-markets/) and
[MIT’s arbitrage-free pricing lecture, replication and law of one price](https://www.ocw.mit.edu/courses/15-450-analytics-of-finance-fall-2010/219406be97b96bc540e0be6aa778c0b7_MIT15_450F10_lec01.pdf).
Examples, proofs and code are original; no employer-specific question or difficulty
claim is inferred. These checks establish declared calculations/contracts and
observed navigation, not learner mastery or physical touch/screen-reader coverage.
Inventory is **25 lessons /138 interviews /61 codes**. **20 topics complete;
l20–l24 remain**, followed by the full navigation/preservation audit and removal
of the pending-topic exception. The full goal remains active.

## Seventeenth batch: order flow, l20

Read the authored `static/lesson-order-flow.js` and its learning goals before
selecting practice. The bank has **two Easy, two Medium and three Hard interviews**
and **one code at each difficulty**. Five interviews and three codes are new.
Permanent q36 and q42 retain their prompts, types, answers, tolerances, hints,
solutions, follow-ups and difficulty; only their generic rubrics become specific
to selected fill populations, quote centre/width and constraints. All **138 prior
interview records** retain grading meaning; those two rubrics are their only
record differences. All **61 prior public coding records** are exact. No old
links, saved assessments or drafts were removed or replaced.

Progression follows the lesson’s conceptual obstacles. Easy separates profit
per fill from profit per opportunity and customer/dealer inventory directions.
Medium conditions on an entire buy/no-order history, then conditions again on a
future execution; its follow-up identifies conditional independence and persistent
counterparty types. The other Medium recomputes demand after each ask change,
handles undefined zero-fill conditional values and derives an informed-fraction
break-even threshold under the stated participation model. New Hard evaluates
complete paths over two opportunities with a signed inventory bound. A quote
with zero immediate expected edge reveals the state; adapting after buy OR no
order gives value five versus four for the greedy purchase. Its proof compares
all feasible first actions, defines the subsequent belief/inventory/horizon state
and excludes quotes that can breach limits before execution. Existing written
work remains explicitly self-assessed; numeric acceptance does not certify a proof.

Easy code reconciles selected liability, fill probability and both profit
denominators. Medium chooses a quote from its OWN stated state-dependent demand
and per-opportunity economics, including refraining and original-index ties.
Hard solves a small finite-horizon partially observed inventory game. One hidden
payoff stays fixed; every buy, sale or no-order observation changes its posterior.
Skip supplies no observation. Terminal marked inventory and a specified quadratic
penalty are separated from cash, and reported gain subtracts the initial
hold-to-settlement objective. Integer Bellman numerators share a positive common
denominator. Gcd-normalised beliefs are cached, with the removed weight factor
restored in parent contributions. This avoids rounded posterior comparisons and
incorrect branch weights. Feasibility uses CURRENT reachable events rather than
all hypothetical states or retroactively discarded fills. All exact outputs use
canonical decimal strings, including large public sample fractions.

**210 Python tests and all 23 frontend suites pass.** Eleven new topic tests
independently enumerate the four informed/uninformed branches, complete conditional
histories, cash-flow directions and the price-response threshold. Easy references
have 400 seeded independent Fraction branch models with denominator reconciliation;
Medium has 300 action-enumeration comparisons, zero/tie cases and a 100,000-quote
reference check. Hard is checked by enumerating COMPLETE observation-indexed
policies, evaluating each policy in both physical states and only then averaging
and maximising. Seventy seeded two-opportunity models include zero prior weights,
reachable/unreachable events, fees, penalties and binding inventory limits.
A separate Fraction-posterior recursion agrees with full-policy enumeration and
checks a three-menu/five-opportunity, state-dependent case with gain
11179260/7891499 and action two. A full-horizon three-event uninformative model
has an independently derived gain twenty. Prior/likelihood scaling invariance,
no input mutation, canonical fractions and all official debug-copy round trips
are checked. All **49 expanded reference solutions** pass the actual full judge.
No official fixture, time/request bound, dependency or grading rule was weakened.
Final strict checks parse over **2,700 authored/generated math spans**.

The old browser connection was unavailable. The native in-app browser control
was reachable and used for final checks. The local server had stopped; its
remembered PID was verified to belong to a different process and was NOT stopped.
A new server was started on the free local port. Every graded or solution session
entered the explicit launcher and visibly verified **Test preview**. Numeric
**−6/5** was accepted. Easy passed **5/5** (0.7ms observed), Medium **8/8** (1.1ms),
Hard **12/12** (5.2ms). The public Hard numerator **999999999000000000** and
denominator **1999999999** survived the actual expected-output textbox and
submission-case copy. Both samples plus the copied case passed **3/3** as
**debugging only, completion unchanged**. Selecting Hard before Easy/Medium was
allowed; returns stayed in the coding list. The actual lesson continued to the
interview list, and a question continued to the coding list. Reloads defaulted
to personal and preview was explicitly re-entered. A restored worked solution
was already open; its separate follow-up was opened after confirming preview.

At a **390px viewport**, this browser’s scrollbar leaves a **375px document**;
client/scroll widths both equal 375, with no page overflow. Both integer-recursion
displays have matching width/scroll width **241px**, and the policy terminal-value
display **255px**. Zero KaTeX errors and no browser console errors observed.
Proof review caught symbols introduced before definition: the final wording
explicitly defines low/high payments, penalty coefficient, likelihood ROW COUNTS,
posterior weights, event cash and inventory increments before using the equations.
Saved proof crops and both personal lists were visually inspected. Temporary
viewport reset; final loaded personal URL was confirmed with no preview notice
and **0/7 interviews /0/3 codes**. An immediate observation after the exit click
briefly still showed the previous page; the final loaded-route check confirmed
personal mode before delivery.

The temporary pre-edit verification copy became unavailable after runtime
reconnection, so a direct equality claim against that lost copy is not made.
The actual saved study file’s creation/last-modification time precedes this topic’s
source creation and remains unchanged; no saved study-file write occurred during
this batch. A durable, ignored verification copy was then retained locally.
Its whole-file hash and all five study groups (questions, coding, lessons, drafts,
trainers) match at final review. Existing study records were preserved; no
reset/replacement or personal grading was performed. The temporary-copy limitation
is recorded here rather than presenting a later capture as a pre-edit baseline.

- [Order-flow interviews, personal workspace](order-flow-personal-question-list-20261012.png).
- [Order-flow coding list, personal workspace](order-flow-personal-coding-list-20261012.png).
- [Defined policy state and terminal value, isolated narrow preview](order-flow-policy-proof-narrow-20261012.png).
- [Integer Bellman numerator and branch contribution, isolated narrow preview](order-flow-bellman-proof-narrow-20261012.png).

Primary context consulted: [Jane Street’s Probability & Markets guide, market
making, adverse selection and recursion sections](https://www.janestreet.com/static/pdfs/trading-interview.pdf).
New examples, proofs, demand rules, wording and code are original. No employer
question provenance or calibrated difficulty is claimed. Verification establishes
the declared finite models/contracts and observed navigation, not learner mastery,
actual-market profitability or physical touch/screen-reader coverage. Inventory:
**25 lessons /143 interviews /64 codes**; **21 topics complete**, **l21–l24 remain**,
then the full navigation/preservation audit and removal of the pending-topic
exception. The full goal remains active.
