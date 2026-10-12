# Likelihood module and revision selector — 2026-10-12

The first researcher-path addition from the interview research is **l25, Let the data compare the models**. It follows l09 (estimation), precedes l10 (covariance), and keeps the existing lesson IDs and all original assessment records intact. In the roadmap it is module 10; the bookmark uses stable ID l25.

The lesson builds from an ordered Bernoulli record into likelihood ratios, probability/density versus likelihood/posterior, log-likelihood optimization, endpoints, parameter-dependent uniform support, normal location/scale fitting, dependence/selection, and exponential waiting-time exposure with independent right censoring. The figures serve two specific explanations: candidate comparisons and feasible support. No embedded code block was added. Numerical stability motivates the linked Python exercise instead.

New original practice: q49 (exponential rate with censoring follow-up), q50 (support and boundary optimization), q51 (duplicated evidence versus independent observations), c15 (stable ordered-record Bernoulli log-likelihood). Difficulty labels remain internal; these are not questions attributed to employers or certified replicas of hiring assessments.

The curriculum now contains **25 lessons / 51 interview problems / 15 Python exercises**. The researcher route contains **19 checks / 42 distinct problems / 15 coding exercises**. The trader route retains its existing contents. Completing this topic does not close the other gaps in the research report.

## Verification

- Compared generated records against the preceding commit: all original 24 lessons, 48 questions and 14 coding records were identical. New records were added, and l25 was inserted after l09.
- Strict KaTeX checks cover 1,014 authored mathematical spans across the registered textbook modules. No KaTeX error elements appeared on l25 in Chrome.
- The new likelihood test compares direct probability products with the log implementation over a grid, checks impossible and boundary records, small-p numerical stability, maximum likelihood ratios, ungraded control behavior, immediate numeric results, interruptible curve animation and reduced-motion/fallback paths.
- All 21 frontend suites and all 18 Python tests passed. The actual c15 solution passes seven cases; the naive `log(1-p)` implementation fails two. The runner was restarted to load the expanded coding bank.
- In Chrome, explicitly entered `/test-preview.html` and verified the Test preview notice. Passed the new understanding check, followed the Apply handoff, checked q49, scheduled a seven-day revision, followed Implement, and passed c15's full seven-case suite. Returned to the personal lesson URL afterwards. Test submissions remained isolated.
- Compared personal questions, coding, lessons, drafts and trainer records before and after browser verification: unchanged. Ungraded navigation and reading location are not achievements. No personal data is included in this evidence file.
- Normal-width and 390-pixel viewport figures reviewed; the narrow page had no horizontal page overflow. Viewport override was reset. A viewport simulation is not a physical mobile-device test. Functional/mocked motion checks and settled screenshots do not establish universal animation frame pacing or actual screen-reader usability.
- Revision options now read **Tomorrow**, **In 3 days**, **In 7 days**. The select has an explicit 150-pixel basis and arrow allowance; the button wraps when space is insufficient. Schedule values and due-date behavior are unchanged. Native select styling remains browser-dependent.
- Catalog fetches bypass stale browser caches. Course/module sequence labels derive from the route order; stable bookmark IDs are unchanged.

## Review images

- [Explanation and likelihood explorer](likelihood-20261012.png)
- [Narrow likelihood explorer](likelihood-narrow-20261012.png)
- [Narrow revision control](revision-select-20261012.png)

## Mathematical source checks

The lesson and practice are original. Standard results were checked against primary teaching material rather than copied into the page:

- [Joseph C. Watkins, University of Arizona — Maximum Likelihood Estimation](https://math.arizona.edu/~jwatkins/o-mle.pdf): the likelihood definition, Bernoulli optimization and support-sensitive estimation.
- [Marco Taboga — Normal distribution maximum likelihood](https://www.statlect.com/fundamentals-of-statistics/normal-distribution-maximum-likelihood): joint normal fitting and the unadjusted variance denominator. The lesson separately makes existence at zero empirical spread explicit.
- [Penn State STAT 504 — Introduction to discrete data](https://online.stat.psu.edu/stat504/Lesson01): ordered Bernoulli and binomial-count likelihoods differ by a parameter-independent coefficient.

The later resampling, machine-learning/optimization, algorithmic and open-ended research additions remain outstanding. See [the interview research](../research/QUANT_INTERVIEW_RESEARCH_2026-10-12.md) and [lesson authoring guide](../LESSON_AUTHORING_GUIDE.md).
