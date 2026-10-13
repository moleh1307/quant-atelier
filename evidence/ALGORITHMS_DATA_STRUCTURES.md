# Algorithms and data structures researcher expansion

Verified 2026-10-13. Two original connected chapters extend l18; all earlier public lesson, question and code records are unchanged. This is curriculum implementation and functional/mathematical verification, not an independent pedagogy study or an employer-readiness certificate.

## Delivered scope

- l31, **Keep the right state, find the boundary**, 65 minutes: eight teaching sections and a duplicate-expiry worked example. Cost models and contracts; lower/upper boundaries and equality; monotone feasibility and a signed counterexample; prefix-count hashing; stable bounded heaps; physical lazy storage; compression, Fenwick blocks and binary-lifted ranks. Interactive lower-bound trace, annotated count-block table and one invariant-driven Python snippet.
- l32, **Order the dependencies, solve the subproblems**, 75 minutes: nine teaching sections and a greedy scheduling counterexample. Directed graph contracts; BFS layers and enqueue marking; Dijkstra settlement, stale records, zero/negative costs; DFS/Kahn/DAG dependencies; sufficient DP states; weighted intervals, canonical reconstruction and transfer to edit distance/knapsack/path counts. One shared-graph BFS/Dijkstra exploration, a recurrence table and one enqueue-driven Python snippet.
- Each chapter: two Easy, two Medium, two Hard automatic interviews; exactly one coding exercise per difficulty. Hints, derivations, changed assumptions, scratchpads and substantive follow-ups remain available. Hard tasks assess explicit numerical and exact-selection checkpoints; they cannot judge arbitrary written proofs.
- Researcher order ends l17→l18→l31→l32; list, journey, optional Next question and next-module links preserve context. Shared foundation and trader sequence unchanged. No AI, copied commercial bank or fabricated learner progress.

Current inventory: **32 lessons / 206 interviews / 96 library codes**. Eight shared, eighteen researcher, six trader lessons. Researcher route:26 modules/166 distinct interviews/77 current codes. Trader:14/90/42. Interviews:122 numeric and84 structured;202 structured parts (113 numerical,89 selection). New permanent IDs q_l31_e1/e2/m1/m2/h1/h2, q_l32_e1/e2/m1/m2/h1/h2 and c_l31_easy/medium/hard, c_l32_easy/medium/hard.

## Independent mathematical and coding verification

`tests/test_algorithms_expansion.py` contains fourteen tests using independent contracts/oracles rather than reference-output copies. Boundary answers come from literal counts; stable winners from full sorting; sliding medians from independently sorted windows; graph distances from all-pairs Floyd–Warshall; interval optima from enumerated feasible subsets with a reverse sorted inclusion-vector tie rule. Exhaustive small duplicate/sign arrays, every three-vertex directed graph (including self-loops), random zero/parallel-weight graphs and random signed-profit interval sets check reference algorithms and input preservation. All topological permutations, all capacity cuts, literal rank multisets and explicit negative-edge routes independently check assessment keys.

Key numerical cross-checks: upper boundary for target8 is7; signed target-three prefix example has4 intervals; stable top-two second ID2; final doubled median12. Nonnegative at-most-three-chunk optimum14, capacity13 requires4. Rank-five frequency coordinate3; removing one −5 produces doubled median3. Dependency-order count10; DAG route count5 versus3 shortest-hop routes. Illustrated target4 has2 BFS hops versus Dijkstra cost3 over4 hops. Negative-edge original target cost3 versus permanently settled result4; added reachable target-relevant cycle cost−6. Scheduling optimum14 from original IDs[0,3,5]; earliest-finish value11; added job[0,7,14] yields canonical single ID7.

| Coding task | Actual judge | Independent expectation and boundaries |
| --- | --- | --- |
| l31 Easy, both boundaries | 6/6 | Empty inputs, missing/duplicate targets, zero/n insertion points;100000 sorted values and2000 queries |
| l31 Medium, stable top-k | 7/7 | Full-sort oracle, earliest ties, k=0/all;100000 values |
| l31 Hard, doubled sliding median | 9/9 | Signed/duplicate sorted-window oracle; odd/even widths, k>n, exact integers;100000 constant records and12000 distinct records |
| l32 Easy, directed hops | 5/5 | All-pairs unit-cost closure; self/parallel/disconnected edges;50000 vertices |
| l32 Medium, nonnegative costs | 7/7 | Floyd–Warshall; zero/self/parallel/stale improvements, None unreachable;50000 vertices and10000-edge large-cost chain |
| l32 Hard, canonical interval DP | 8/8 | Exhaustive feasible-subset oracle; touching endpoints, signed/zero profits, duplicate intervals, original identities and skip ties;50000 duplicate jobs and10000 compatible jobs |

Incorrect stable ties, missing median expiry, first-discovery distances, strict-end compatibility and take-on-equality are rejected by the real judge. Sample/hidden argument and expected-value JSON fit the500000-byte debugging-copy contract without truncation; all values satisfy the exact UI-number bounds.

`tests/test_algorithm_figures.cjs` independently verifies boundary traces, rank selection with zero counts and non-power-of-two vocabularies, both graph objectives via all-pairs closure, stable mounted nodes, selection no-ops, step resets and ungraded handlers. It executes both displayed Python snippets. Course/navigation suites check the actual authored text, outlines, quizzes, strict math and l18→l31→l32 continuity.

Full **313 Python tests and31 frontend suites passed**. Final affected algorithm-figure and textbook suites passed again after label/spacing refinements. The authored renderer validated1270 strict math spans; source/generated strict parsing also passed. Fresh full-record comparisons confirm all previous30 lessons,194 interviews and90 codes identical to the pre-change build. New registration guards use actually unknown l33 rather than bypassing coverage.

## Live browser and progress isolation

Native in-app browser review used the separate agent review tab because the preferred Atlas backend was unavailable. The user's study Chrome and original in-app tab were left untouched. Ungraded personal explorations showed lower boundaries0/1/5/8 and the differing graph objectives; changing controls never completed an activity.

Explicit `/test-preview.html#destination` → **Enter test preview**, followed by visible **Test preview**, preceded graded actions. Both lesson checks passed. l31 Hard capacity form rejected two matching numeric parts with an incomplete claim set, then accepted the exact set as assisted review. l32 negative-edge Hard accepted costs3/4/−6 and exactly the valid DAG/reopening/target-cycle claims as assisted review. Both grouped interview lists had2/2/2 and coding lists1/1/1. Lesson→list→code→next-module navigation retained its researcher topic.

Hard actual Submit: l31 median **9/9,107.1ms**; final l32 schedule **8/8,637ms**. Both final list states explicitly read **Passed · with editorial**. Observing route completion and the opened editorial before a shared-label click matters: hash navigation renders asynchronously. These timings are individual review observations, not performance guarantees.

Desktop1440×1000, narrow390×844 and short900×500 reviewed. Graph labels clear of edges; n boundary separate from cells; figure controls/captions remain readable. Narrow tables420px scroll inside341px containers; the page remains375px with no horizontal overflow and zero KaTeX errors. Narrow section jump settles at178.5px below header161px; short-window jump140.5px below header122.9px. Section menu has419px client height,628px scroll height, vertical auto-scroll, bottom486px in a500px viewport. Semantic color transitions honor reduced motion; discrete algorithm steps remain mathematically discrete.

Personal disk baseline comparison after preview activity found no changed learner record IDs and no new l31/l32 lesson/question/code/draft records. No reset, restore or import was performed. Preview exit visibly restored unpassed lesson checks,0/6 questions and0/3 codes. Final review tab is personal l31 and temporary viewport override reset. Screenshots contain ungraded personal chapter state:

- [Search invariant and executable loop](algorithms-search-desktop-20261013.png)
- [Graph objective and settled distances](algorithms-graph-desktop-20261013.png)
- [Narrow graph](algorithms-graph-narrow-20261013.png)

The existing loopback Python3.13 server was refreshed with the same interpreter/port8768 to import the six new TASKS. Static assets use algorithms-20261013-1; existing study tabs need a normal reload to load them. Personal data, local baseline exports, runtime logs and installed dependencies are excluded from publication.

## Primary references and original authorship

Standard mathematical contracts and implementation details were checked against primary teaching/author documentation. Prose, examples, diagrams, questions and code here are original; no external artwork or commercial interview question was copied. Our explicit tie, interval, signed-profit and output rules should be read as our contracts, not inferred from outside examples.

- [MIT6.006 lecture index](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/pages/lecture-notes/): algorithms/data structures and dependency-first DP organization.
- [MIT heaps](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/40d4851e550507ca14dc778b9b2266cc_MIT6_006S20_lec8.pdf): heap order, operations and construction.
- [MIT BFS](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/196a95604877d326c6586e60477b59d4_MIT6_006S20_lec9.pdf): layers and linear traversal.
- [MIT Dijkstra](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/d819e7f4568aced8d5b59e03db6c7b67_MIT6_006S20_lec13.pdf): nonnegative settlement proof; our lazy queue has a different explicit storage bound from decrease-key.
- [MIT dynamic programming](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/9eb3e9a51a7b5b60b0f67c2277f8b0ee_MIT6_006S20_lec15.pdf): subproblems, recurrence, evaluation order, base cases and work.
- [Cornell weighted intervals](https://www.cs.cornell.edu/courses/cs4820/2021sp/lectures/notes/cs4820-2021-02-22.pdf): prefix include/exclude structure.
- [Python3.13 bisect](https://docs.python.org/3.13/library/bisect.html), [heapq](https://docs.python.org/3.13/library/heapq.html): insertion-boundary and heap APIs.
- [Fenwick author's improved frequency-to-symbol report](https://www.cs.auckland.ac.nz/~peter-f/FTPfiles/TechRep110.pdf): cumulative-frequency/rank background. The chapter's binary-lifting derivation and zero-frequency behavior were independently verified; it does not reuse the original nonzero-frequency selection procedure.

## Limits that remain explicit

Complexity assumes bounded-word arithmetic/comparison; Python's arbitrary integer bit costs and serialization can matter. Hash lookup is expected-cost, not unconditional worst-case constant. Whole-array compression is batch storageO(u), not onlineO(k). Lazy Dijkstra permitsO(M) physical heap entries; only nonnegative weights receive its standard guarantee. Weighted-interval equality is skip-current, not a promise of globally fewest jobs. Automated forms check chosen claims/results, not arbitrary proof quality or live interview fluency. Advanced graph algorithms, richer balanced-tree implementations, additional DP families and open research projects remain further study. VoiceOver and physical touch were not exercised.
