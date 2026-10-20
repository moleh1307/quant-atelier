# Progressive course parts — 2026-10-20

The user chose three successive Easy → Medium → Hard parts inside each lesson, starting with the first three modules. Implemented l01, l02 and l03 only; the other 29 authored lesson renderings are byte-for-byte identical to commit 48166d1.

## Authored material

| Module | Easy | Medium | Hard |
| --- | --- | --- | --- |
| 01 — Count the right sample space | Experiment, record, event, equal weights | Ordered/unordered records, replacement, conditional paths, overlap, independence | General choose/group weights, hypergeometric counts, repeated-object multiplicities, exact collisions and approximation limits, notebook exclusions/assignment states |
| 02 — Condition, then normalise | Surviving population, direction, numerical base-rate example | Joint weights, Bayes, persistent identity, likelihood ratios, posterior prediction | Continuous likelihoods, reporting protocols, sharp bounds without conditional independence, changing hidden states and stable log normalization |
| 03 — Expectation without independence | Weighted payoff, linearity, dependent card draws | Overlapping windows, tail sums, discrete maxima, occupied/singleton labels | Dependence and spread, permutation cycles, matching crossings, rank weights without replacement |

The three parts contain 11 / 12 / 11 teaching subsections respectively, followed by the existing worked-example/check destinations. Original illustrations and bindings are retained. A base-rate count table, a prediction/update belief flow and a four-endpoint crossing figure support specific new arguments. No code block was needed in these three authored probability explanations.

Reading-time estimates are now 45 / 50 / 50 minutes for the whole chapters, with learning goals extended to match the new scope. These are estimates, not measured completion times.

## Reading UX

Compact Easy/Medium/Hard navigation jumps within the continuous argument; the existing sticky Sections menu groups its destinations by part. Native buttons support keyboard activation, focused subsection destinations, smooth scrolling with measured toolbar clearance, and immediate jumps under reduced-motion preferences. Current-location markers follow actual scrolling and include a part's introduction when it begins. Menus retain arrow/Home/End/Escape navigation and available-height limits. Opening, reading and exploring confer no progress.

## Verification performed

- All **34 frontend suites** passed. Relevant authored-course/sample-space/reading/level suites were also rerun after the final changes. The registered-course suite strictly parses **1,444 math spans** across l02–l32; l01 and its figure variants are strictly parsed separately.
- **Nine new independent Python tests** enumerate small multiplicity groups, physical subsets, collisions, derangements/fixed points, reporting weights, attainable dependence bounds, two-state joint paths, occupancy/singletons, permutation cycles, circle matchings and sampled ranks, including repeated/negative labels. Four existing course-example tests also passed. No backend or judge implementation changed; the entire Python platform suite was not rerun.
- Rendering all courses with the prior versus current source confirmed identical HTML for the other **29** lessons. The public catalog differs only in l01–l03 reading-time estimates and learning objectives. All interview records, check keys/options/explanations, links and the complete coding bank are identical to the fresh pre-edit copies.
- Native in-app browser review used a separate temporary tab after the preferred browser runtime could not connect. Actual pages l01/l02/l03, keyboard part jumps, outline destinations, final math and new figures were inspected. At 390×844 (375 CSS-pixel content width), page overflow was absent and new navigation/figure labels remained readable. A 1280×500 short viewport kept the final check destination reachable by End, with the menu between y=65 and y=486.
- Preview entry was explicit through the development launcher. No check, answer, Run, Submit or editorial reveal was invoked. Existing preview scores in screenshots are earlier development records, not learner achievement from this review. Personal progress remained exactly equal to its fresh private baseline; nothing was reset or imported. Viewport overrides were reset and the temporary tab closed after returning to a personal URL. User-owned study tabs were not operated.

## Screenshots

- [Course overview and three parts](course-levels-l01-overview.png)
- [Sample-space Hard introduction](course-levels-l01-hard.png)
- [Changing-state prediction/update explanation](course-levels-l02-filter.png)
- [Crossings and their four endpoints](course-levels-l03-crossings.png)
- [Narrow reading-part navigation](course-levels-narrow.png)

These screenshots document settled layout, not animation frame pacing, touch or assistive-technology certification. Independent arithmetic checks were written by the same author; they are not an independent pedagogy review. One understanding check does not certify all three parts, and this expansion does not certify readiness for a particular firm's interviews.

## Sources and continuity

Visible prose: static/lesson-sample-space.js, static/lesson-conditioning.js, static/lesson-expectation.js. Shared opt-in renderer: static/course-textbook.js. Navigation/focus: static/app.js. Styles: static/course-textbook.css. Catalog sources: build_content.py and course_lessons.py; generated static/content.json. Asset version: course-levels-20261020-2. Existing server on port 8768 was used without a backend restart.

The user-approved future authoring contract is in LESSON_AUTHORING_GUIDE.md section 28. Extending this progression to the remaining courses is future work, outside this initial three-module rollout. Question lists still have at least two items per E/M/H; coding lists still have one per E/M/H. No new completion schema or AI service was introduced.
