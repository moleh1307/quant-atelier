# Resampling and bootstrap researcher chapter

Verified 2026-10-13. Original content; difficulty tiers describe reasoning within this bank and are not validated replicas of any employer's interview.

## Scope and sequence

l28, **Resample the experiment, not the rows** (50 minutes), is researcher-only and follows l13 time series, before l14 validation. The topic needs the earlier sampling-distribution, inference and dependence foundations. The visible module is researcher stop 17; stable ID l28 does not imply pedagogical position 28.

The 11 authored sections explain:

1. True sampling error versus conditional bootstrap error; parametric generation and refitting.
2. The empirical law, physical-record multiplicity, multinomial counts and out-of-bag membership.
3. An exact bootstrap-mean distribution, including its finite-sample variance factor.
4. Statistical uncertainty versus finite-B Monte Carlo precision, standard error and bias.
5. Percentile/basic interval construction and inversion with explicit quantile rules.
6. Studentization and BCa structure, with degeneracy and tie conventions.
7. Delete-one jackknife variance, bias and acceleration sensitivity.
8. Paired covariance, independent clusters, unequal sizes and different targets.
9. Contiguous/circular blocks, final-block truncation and dependence assumptions.
10. Ordinary bootstrap failure for a Uniform endpoint and a separate exact model pivot.
11. Permutation nulls/exchangeability, fixed-model versus refitted-procedure targets and evaluation leakage.

Continuous serif teaching prose, purposeful mathematical color and three native figures follow the approved textbook direction. The mean-law and block figures interact; the endpoint CDF comparison is static. No Python fragment is forced into this chapter. Code belongs in the linked exercises where implementation is the learning objective. Existing Sections, understanding check, Steps, practice drawers and journey navigation are retained.

## Practice

| Difficulty | Interview problems | Coding exercise |
| --- | --- | --- |
| Easy | Exact bootstrap-mean variance; expected distinct physical records | Supplied paired-record index resamples |
| Medium | Invert centered errors into a basic interval; preserve paired covariance | Bias, standard error, percentile/basic intervals with explicit linear quantiles |
| Hard | Nonregular endpoint failure; unequal-size cluster ratio law | Exact circular-block mean variance in linear time with a truncated final block |

IDs are `q_l28_e1/e2/m1/m2/h1/h2` and `c_l28_easy/medium/hard`. Four numeric interviews and two structured Hard interviews use automatic grading. The Hard tasks add four numerical and two exact-set claim checkpoints. Full derivations, specific reasoning obligations, graduated hints and substantive ungraded follow-ups remain available; checking claims does not grade an arbitrary scratchpad proof.

Every topic list has two interviews and exactly one code per difficulty. The module flow remains lesson → grouped interview list → grouped coding list, with free choice within lists and exact originating-module returns. Visiting or exploring earns no progress.

## Mathematics and independent checks

The checks below were formulated separately from the reference implementations. This is an author review supported by independent calculations, not a second independent reviewer.

- Enumerating all physical-index resamples gives mean variance 14/27 for [1,2,4], compared with the usual unbiased mean-variance estimate 7/9. Averaging B simulated estimates introduces another factor 1/B for that simulation average, not for the estimator's standard error.
- Expected distinct indices at n=4 are 175/64. Value duplicates retain physical multiplicity.
- Centered-error quantiles −3 and 5 at estimate 10 give basic interval [5,13], while the percentile interval is [7,15]. The medium code uses index h=(B−1)p, linear interpolation and variance denominator B−1. Fraction-based interpolation/moment oracles check endpoints, affine changes, ties and ordering.
- Paired differences for (1,2),(2,3),(4,5) are constant −1, whereas independent column resampling gives variance 28/27. This example does not imply pairing always lowers variance under negative covariance.
- Four Uniform draws give bootstrap maximum-gap zero-atom probability 175/256; the atom tends to 1−exp(−1), while the true normalized gap has a continuous Exponential(1) limit. Empirical percentile endpoints cannot exceed the observed maximum, hence have zero coverage for the unknown continuous endpoint. The model-specific interval [M, M/alpha^(1/n)] instead has exact 1−alpha coverage. These are different procedures.
- Whole-cluster draws from [0,0] and [10,10,10,10] have pooled means 0,20/3,20/3,10; exact expectation 35/6, variance 475/36 and bias −5/6. Cluster-mean averaging and individual-row draws use different laws/targets. The example is not a reliable-inference claim with only two original clusters.
- Jackknife mean variance simplifies independently to s²/n.
- Circular window covariance identities and small whole-start enumerations independently check the block algorithm. At n=8, length3, the retained-tail variance is 325/64; treating the tail as a full block fails. A 20,000-element alternating record tests length10,001 with exact variance 0.005. Integer moment numerators avoid premature subtractive floating cancellation.
- A six-label-subset permutation law for [1,2,4,5] gives differences −3,−1,0,0,1,3: one-sided p=1/6 and absolute two-sided p=1/3. Null exchangeability is stated explicitly.

Sources consulted for concepts and scope: [Wasserman's CMU bootstrap chapter](https://www.stat.cmu.edu/~larry/=sml/Boot.pdf), [CMU model-based and block-resampling lecture](https://stat.cmu.edu/~cshalizi/dst/20/lectures/16/lecture-16.html) and [R Journal m-out-of-n bootstrap paper](https://journal.r-project.org/articles/RJ-2025-031/). Prose, figures, examples and practice are original. No new external runtime dependency was added.

## Automated verification

- `python3 build_content.py` and `python3 coding_bank.py`: registered l28 builds with full difficulty coverage; unknown future-topic test IDs moved to l29 so guards remain meaningful.
- `python3 -m unittest discover -s tests`: **279 tests passed**.
- All `tests/test_*.cjs`: **26 frontend suites passed**, zero failures.
- `tests/test_resampling.py`: exact enumeration/rational/covariance oracles, interval invariance, real judge passes and rejection of wrong SE/sqrt(B) or untruncated-block code.
- `tests/test_resampling.cjs`: probability laws, source-index continuity, block boundary cases, CDF jump, stable four stems/eight slots, animation retargeting, reduced/no-RAF/disconnected hosts, ungraded binding and l13 → l28 → l14 handoffs.
- Final focused resampling/course-renderer checks passed after prose and divisible-block label refinements. Strict parsing checked **3,537 math spans** across authored/generated material, including **1,166** authored registered spans. This verifies typesetting syntax; independent calculations above address meaning.
- Complete key/exact-set checker tests cover all76 structured tasks and1,951 choice subsets, plus real form/storage/provenance handlers.

## Live browser checks

Preferred Atlas IAB connection had no backend; native IAB controls were used. The existing local Python 3.13 server on port8768 was restarted with the same interpreter/port to load new imported coding tasks. Personal data were retained.

- Personal chapter opened at `#courses/l28/journey/researcher/l28`, with check to do,0/6 interviews and0/3 codes. No KaTeX errors or browser error/warning logs were observed.
- Default desktop and390×844 mobile views fit without document horizontal overflow. Mean-law slider changed z6→12, updating mean2→4 and variance8/3→32/3. Mobile labels and annotations were readable.
- Block length2→3 produced exact variance325/64 and the stated two-value tail. Length8 gave zero variance; labels distinguish wholly retained blocks from a shortened tail. The source indices, seams and colored slots remained coherent.
- Mobile endpoint CDF showed the zero atom and continuous true law on the same probability scale.
- Explicit `/test-preview.html` → **Enter test preview**, verified visible notice, preceded every graded action. Incorrect lesson choice earned no completion; correct choice passed and continued to the six-question list.
- Partial Hard cluster response matched2/3 checkpoints and earned no pass. Completing both numeric answers and the exact claim set earned a preview unaided pass. The link continued to a three-code list, one per tier; next module remained l14.
- Hard reference code passed **9/9 tests through live Submit** (reported9.1ms), establishing that the running backend knows the new exercise. Unit tests also run the three correct references through the real judge and reject selected incorrect alternatives.
- Reload exited preview. Final browser is personal l28 with0/6 interviews,0/3 codes and an unchecked lesson. Temporary viewport override was reset. The user's separate Chrome study tab was not used.

Screenshots: [desktop mean law](resampling-mean-desktop.png), [mobile mean law](resampling-mean-mobile.png), [mobile blocks](resampling-blocks-mobile.png), [mobile endpoint failure](resampling-endpoint-mobile.png), [Hard submission in test preview](resampling-hard-preview.png). Preview grades in screenshots are development records, never personal evidence.

## Preservation and current inventory

A fresh pre-edit comparison confirmed all **27 original lesson records,176 interview records and81 public coding records are identical by permanent ID**, including metadata/assessment keys. Personal `data/progress.json` remained byte-for-byte equal to the fresh pre-edit baseline throughout browser grading and server restart. No reset/import or baseline restoration was used. Ignored personal data, baselines and temporary code were not included in the public commit.

Current bank: **28 lessons /182 interviews /84 library codes**, including106 numeric and76 structured interviews. Structured tasks contain173 checkpoints (92 numerical,81 selection). Researcher route:22 modules,142 distinct interviews,65 current codes; trader unchanged at14/90/42. Extra practice increases denominators without creating completion. Old dated reports remain historical.

## Limits and continuity

The understanding check examines one distinction and does not certify mastery. Small exact examples illustrate conditional laws; they do not establish actual coverage for a user's dataset. BCa/studentization, nonregular resampling remedies and block selection need model-specific assumptions. The Python judge checks specified deterministic cases, not every possible complexity claim. Additional independent pedagogical review and broader statistical learning/regularization, ML, algorithms and research projects remain future work.

Authoring guidance section24 records the topic-specific argument, stable IDs, source ownership and failure cases. Reuse shared infrastructure, not a compulsory chapter layout, figure or code ingredient.
