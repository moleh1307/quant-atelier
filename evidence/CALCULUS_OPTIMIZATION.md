# Calculus and optimization researcher foundation

Verified 2026-10-13. This is an original curriculum addition, not a collection of attributed firm questions or an employer-readiness certification.

## Scope and sequence

Two researcher-only modules follow the eight shared modules and precede estimation/likelihood:

1. l26, **Calculus is a local model** (45 minutes): local slopes and units; total versus coordinate differentiability; directional gradients; vector composition and coordinate changes; weighted squared-loss derivatives; mixed Hessian curvature; finite-difference error and stable evaluation; reverse derivatives through a shared recurrence.
2. l27, **Optimize the loss you actually defined** (50 minutes): objective/domain/existence; convex, strict and strong convexity; smooth descent bounds; exact quadratic step stability and conditioning; Armijo backtracking; Newton ascent counterexample; feasible first-order certificates; coupled box geometry; KKT signs, complementary slackness and failed necessity under degeneracy; noisy-gradient second moments and stopping evidence.

The chapters keep the warm illustrated textbook direction and differ in teaching sequence. Calculus has a tangent/secant explorer and unit-direction contours, plus one small Python fragment explaining overflow-safe evaluation. Optimization has a discrete-update contour trace and a coupled-box explorer, with no decorative code block. Every symbol's operational role, relevant assumption, failure case and worked transfer is explained in context. Existing outline, quiz, journey bar and related-practice controls remain shared.

Each lesson owns **two Easy, two Medium and two Hard interviews**, plus **exactly one Easy, one Medium and one Hard code**. The lesson → grouped interview list → grouped coding list flow remains freely navigable. All interview grading is automatic: 8 new numeric problems and 4 new structured Hard problems, with 7 numeric and 4 exact-set selection checkpoints. Scratchpad proofs are ungraded; full original derivations and nontrivial follow-ups remain available.

Stable new IDs: `q_l26_e1/e2/m1/m2/h1/h2`, `q_l27_e1/e2/m1/m2/h1/h2`, `c_l26_easy/medium/hard`, `c_l27_easy/medium/hard`. Nothing was rekeyed in the earlier curriculum.

## Implementation

- `calculus_optimization_content.py`: catalog, checks, fallback sections and learning goals.
- `static/lesson-calculus.js`, `static/lesson-optimization.js`: independent chapter arguments, stable SVG models, accessible controls and pure model exports.
- `static/lesson-differential.css`: scoped figures and reading controls using existing fonts/palette.
- `topic_practice/calculus_optimization.py`: original prompts, hints, detailed derivations/follow-ups, specific assessment obligations and objective checkpoints.
- `topic_practice/calculus_optimization_coding.py`: six local Python references with independently constructed expectations: rational weighted gradients, forward sensitivities, closed-form iteration factors and rational active-set/KKT enumeration.
- Existing build/registry/roadmap plumbing registers both modules explicitly. No unregistered future-topic exception was added; l28 is now the future-module test fixture.

Motion runs for 340 ms, retargets from visible mathematical parameters, recalculates geometry, keeps SVG nodes stable, honors reduced motion and no-RAF hosts, and stops when the lesson root detaches. Selected iterations remain discrete; joining segments are explicitly not extra algorithm steps. Controls update requested numerical results immediately. Displayed six-step paths stay within fixed equal-scale axes across the whole offered step range.

## Verification

- **269 Python tests passed** in the full suite.
- **25 frontend suites passed**, including source/route coverage, all objective keys and 1,889 choice subsets, provenance and future-registration checks.
- **3,463 authored/generated math spans** passed strict KaTeX parsing; the authored-course renderer additionally checked **1,111 spans**, unique outline anchors, quiz preservation and purposeful code exceptions. These are separate representations, not an additive inventory of unique formulas.
- New independent checks compare reverse gradients to forward sensitivities and centered differences; weighted gradients to exact rational expansions and weight-scale invariance; logistic derivatives to probability/log-loss calculations and ±1000 scores; quadratic trajectories to geometric-error formulas; Armijo updates to rational acceptance thresholds; and 300 randomized positive-definite box cases to a distinct exact KKT oracle and feasible-direction signs. All six coding references passed their actual submission suites.
- Animation tests verify interruption/retargeting, reduced motion, absent RAF and route detachment. Geometry tests verify directional unit length and curvature, exact Taylor remainders, iteration stability/oscillation/divergence and coupled-box loss gaps.
- Live native in-app browser checked both course pages at desktop and 390×844 without page overflow or KaTeX errors; keyboard sliders updated their specified numerical models. All four grouped lists showed the required difficulty counts and correct module links.
- Through the explicit isolated preview launcher, both understanding checks passed. The recurrence Hard problem rejected an incomplete answer (2/3 checkpoints; no pass), then accepted the complete answer (3/3; unaided pass). Its return link led to the grouped coding list and next module.
- The first browser coding submission exposed a stale imported bank in the previously running Python server. The exact loopback server was restarted with its same interpreter/port, preserving personal data. The new Hard box solver then passed **7/7 tests through the browser's actual Submit endpoint**. This runtime refresh is required when importing new Python bank entries.
- Every prior public lesson record, question record and coding record was compared by permanent ID against the pre-edit public bank and is exactly unchanged. The ignored personal progress file remained **byte-for-byte unchanged**, including after preview checks and server restart; no baseline was restored or reset.
- Final in-app browser page is the **personal** calculus journey with its new-module check unpassed, 0/6 interview passes and 0/3 coding passes. Temporary viewport override was reset. The user's other browser study tab was not touched.

Evidence screenshots: [local model](calculus-local-model-20261013.png), [direction at phone width](calculus-direction-narrow-20261013.png), [coupled box](optimization-box-20261013.png).

## Current inventory and limits

27 lessons, **176 automatic interviews** (102 numeric, 74 structured), **81 library Python exercises**. Structured questions together contain 167 checkpoints (88 numeric, 79 selection). Researcher: **21 modules / 136 distinct interviews / 62 current codes**. Trader remains **14 modules / 90 interviews / 42 current codes**. An existing shared coding ID is used by two current modules, and additional-only legacy activities remain preserved; these counts intentionally use distinct IDs.

This closes dedicated calculus and optimization foundations. Statistical learning/regularization, resampling, broader ML/algorithms and open research projects still need dedicated expansions. A correct set of numerical/claim checkpoints does not establish the quality of an arbitrary written proof or a live verbal defense. Pedagogical review and independent mathematical formulations here were performed by the same author, not a separate reviewer.

Primary further-study references: [MIT multivariable tangent approximation and optimization](https://ocw.mit.edu/courses/18-02sc-multivariable-calculus-fall-2010/pages/2.-partial-derivatives/part-a-functions-of-two-variables-tangent-approximation-and-optimization/), [Boyd and Vandenberghe's official convex optimization book](https://web.stanford.edu/~boyd/cvxbook/). Examples, exercises and prose in this addition are original.
