# Nonlinear machine learning — verified 2026-10-13

l30, **Give the model a way to bend**, follows l29 and precedes l12 on the researcher route. Personal entry: <http://127.0.0.1:8768/#courses/l30/journey/researcher/l30>. Original ten-section warm textbook plus a worked deletion derivation; no compulsory inline Python. The two figures explain distinct obstacles, rather than reproducing the preceding chapter's layout.

The argument covers interaction versus additivity, greedy discovery versus representability, fixed bases, kernel span reduction and feature-norm penalties, normalization and singular representations, bandwidth/local support and extrapolation, weighted tree means/gains and stopping, forest covariance and OOB limits, squared/logistic gradient and Newton boosting, learned neural features and chain derivatives, proper losses/cost thresholds, and complete-procedure validation. The worked example derives the fixed-procedure deletion identity by block elimination before checking two records. Full deep-network training, SVM optimization and broad algorithms/projects remain further study; this addition is not an employer-readiness certification.

## Practice

Six original automatically checked interviews: two per difficulty. Easy checks leaf fitting and nonlinear ridge; Medium checks correlated-ensemble risk and a penalized Newton logit update; Hard requires singular kernel penalty reasoning and a proof/shift analysis of an interaction invisible to additive stumps. Hard tasks have three numerical checkpoints plus an exact-set claim checkpoint each. Worked derivations and deeper follow-ups remain; specified answers are graded, arbitrary scratchpad proofs are not.

Three deterministic coding contracts:

- Easy: weighted means/RSS inside supplied leaves, including sparse IDs and repeated queries.
- Medium: weighted stump search with tied feature values, minimum RECORD counts, exact rational RSS comparisons and stable feature/threshold ties.
- Hard: fixed degree-two polynomial kernel ridge and exact LOO predictions from one Cholesky factorization; duplicates, empty queries and summed-penalty normalization are explicit.

Permanent IDs q_l30_e1/e2/m1/m2/h1/h2 and c_l30_easy/medium/hard. Sources: nonlinear_ml_content.py, static/lesson-nonlinear-ml.js/.css and topic_practice/nonlinear_ml*.py. Coverage/assessment guards include l30; unknown-topic fixtures now use l31. All previous 29 lesson, 188 interview and 87 public coding records were compared in full against fresh pre-task copies and remained identical.

Current inventory: **30 lessons / 194 interviews / 90 library codes**; paths 8 shared/16 researcher/6 trader. Researcher route: 24 modules/154 distinct interviews/71 current codes. Trader remains 14/90/42. Interviews: 114 numeric/80 structured. Structured checks: 188 parts, comprising 103 numeric and 85 exact-set selections.

## Independent verification

- All **299 Python tests** passed (full discovery). All **29 frontend suites** passed. After the final explanatory/proportional-label refinements, affected model/renderer/math suites passed again.
- tests/test_nonlinear_ml.py uses direct residual enumeration for leaf/stump expectations, exact rational deleted kernel REFITS rather than the reference's inverse-diagonal shortcut, a maximum-dimension rank-one closed law, common/individual-noise covariance construction, and exact singular/XOR calculations. Seeded small cases preserve inputs. All three references pass the actual bounded judge; wrong unweighted means and wrong deletion denominators are rejected.
- tests/test_nonlinear_ml.cjs checks covariance sums, all corner representations, mounted node updates, current accessible descriptions, identical-option no-op, interruption from visible state, reduced/no-RAF/disconnected fallbacks, ungraded state integrity, l29→l30→l12 continuity and six/three grouped lists.
- Strict authored renderer checks: 1,261 registered math spans, original l01 rendering retained, unique section/example/check targets and original shared quiz intact. Generated/authored math suite passes strict KaTeX; source-wide span totals vary with its source-string scan, so the stable registered-body count is the clearer authoring measure.

## Live browser evidence

Preferred Atlas IAB connection was attempted but reported no backend. Native Codex IAB controls were used, with a separate review tab. Chrome's study tab was untouched. The existing loopback server was identified by exact command/interpreter and restarted on port8768 to refresh TASKS. The new server uses the same Python3.13 interpreter; no personal-data reset/import occurred.

Personal, ungraded checks covered all representation choices, forest correlation endpoints via keyboard, correct immediate results, proper math, long captions, desktop1440×1000, narrow390×844 and short900×500. The final narrow figure has readable labels with no collisions. Narrow page width equalled client width (375px with scrollbar); formula/table scrolling remains local. No KaTeX errors observed. At the settled short-height worked-example jump, target top140.52px exceeded module bottom122.89px. Temporary viewport overrides were reset.

Explicit launcher + **Enter test preview**, followed by a visible Test preview notice, preceded grading. The lesson check passed and continued into the grouped question list. Hard h2 rejected empty choices, then an incomplete choice set (3/4), and passed only all four exact checkpoints. The coding list contained exactly three difficulty slots. Hard code editorial was revealed in preview, reference submitted via the real editor and live endpoint, and **6/6 passed, 14.4ms** was observed; the list reported **Passed · with editorial**. This timing is one observed local run, not a performance guarantee. All three reference suites also pass independently through judge.run.

Fresh personal data was compared before/after: no l30 lesson/question/code/draft test records entered personal storage. Existing ordinary learner activity was retained; no baseline restored. Returning through Open personal workspace and reloading showed the new module's personal zero state. The review tab ends at the personal l30 route with viewport reset. Mocked reduced-motion checks and screenshots do not constitute physical mobile, screen-reader or universal frame-pacing validation.

Screenshots:

- [Desktop interaction](nonlinear-corners-desktop-20261013.png)
- [Narrow interaction](nonlinear-corners-narrow-20261013.png)
- [Narrow forest variance](nonlinear-forest-narrow-20261013.png)
- [Personal coding list](nonlinear-coding-list-narrow-20261013.png)
- [Live preview Submit](nonlinear-hard-submit-20261013.png)

## Primary calibration sources

Used to verify method definitions and assumptions; prose, calculations and visuals here are original.

- [Cornell kernels](https://www.cs.cornell.edu/courses/cs4780/2024sp/lectures/lecturenote14.html)
- [Cornell decision trees](https://www.cs.cornell.edu/courses/cs4780/2024sp/lectures/lecturenote17.html)
- [Cornell bagging](https://www.cs.cornell.edu/courses/cs4780/2024sp/lectures/lecturenote18.html)
- [Cornell boosting](https://www.cs.cornell.edu/courses/cs4780/2024sp/lectures/lecturenote19.html)
- [Stanford boosting](https://web.stanford.edu/class/stats202/notes/Tree/Boosting.html)
- [Breiman's Random Forests paper](https://www.stat.berkeley.edu/~breiman/randomforest2001.pdf)

The elementary equicorrelated regression-variance calculation is derived explicitly, not presented as the paper's classification error bound. Conditional randomization independence and repeated-dataset covariance are distinguished. Row-wise OOB exclusion is not asserted to certify chronological validation.
