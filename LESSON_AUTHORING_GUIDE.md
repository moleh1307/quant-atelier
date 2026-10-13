# Quant Atelier: lesson authoring and design guide

**Status:** approved direction, recorded 2026-10-04.  
**Canonical reference:** lesson 01, “Count the right sample space”, after the continuous textbook and purposeful-motion revisions.  
**Reference URL:** <http://127.0.0.1:8768/#courses/l01/journey/researcher/l01>.  
**Purpose:** preserve the user's decisions across context resets and guide future course updates. Creating this guide does not authorise rewriting other lessons now. Later user instructions take precedence.

**Maintenance:** implementation pointers reviewed against live files on 2026-10-09. This guide records the teaching contract; [COURSE_REDESIGN_STATUS.md](COURSE_REDESIGN_STATUS.md) records current curriculum work. A planned, implemented or tested page is not automatically an approved or fully reviewed page.

## 1. Read this first after a context reset

The user wants a carefully authored, illustrated, sometimes interactive mathematical textbook inside Quant Atelier. Prose, notation, figures and controls should work together to explain an idea. Choose each lesson's form from its subject and the learner's likely misunderstandings. Lesson 01 is the approved quality reference; it is not a template to duplicate.

Keep the warm, light site identity and continuous reading experience. Use color to connect mathematical objects across prose, formulas and figures. Include code only when it reveals reasoning that is better expressed or checked computationally. Include a diagram only when it makes a relationship clearer. Add interaction only when changing something teaches something. Animate that change so the learner can follow it. Preserve the existing learning-module journey and honest progress.

**Recovery sequence:** read this guide, inspect lesson 01's live source and current evidence, inspect the target lesson and its linked practice, then author a topic-specific explanation. Do not start by copying lesson 01's seven sections or its collection of widgets.

### Compact recovery contract

After compaction, recover these decisions before designing anything:

- **Experience:** a thoughtfully written mathematical textbook within the existing warm Quant Atelier interface, with connected prose and precise mathematical reasoning.
- **Purpose:** help this learner understand, remember and transfer the concept into the existing quant practice; visual polish is part of clarity, not a substitute for it.
- **Selection:** every paragraph, figure, code block and interaction must explain a particular step or distinction. Omit ingredients that do not help.
- **Variation:** preserve the design system and navigation, while choosing the argument and representations independently for each topic.
- **Depth:** define objects and assumptions, justify the consequential steps, interpret the result and test its limits. Do not use a length target to decide whether it is detailed enough.
- **Motion:** retain object identity and show meaningful change smoothly; rapid input and reduced motion must retain truthful results.
- **Continuity:** keep the module, branch and next practice visible; preserve assessment semantics and personal work.
- **Evidence:** verify the actual target, distinguish mathematical checks from visual review and learning outcomes, and leave an exact remaining scope.

This capsule is a quick orientation. Read the relevant detailed sections before implementing; the capsule does not replace the full contract.

## 2. What the user actually approved

The user supplied screenshots of an illustrated technical textbook and discussion of effective pedagogy and 3Blue1Brown-style explanation. The useful qualities were the integration of text, meaningful mathematical color, diagrams, figures and occasional code. The dark theme and the subject of the reference were incidental. A Python block appeared in the reference because that particular argument needed it; this was not a request to put Python into every lesson.

The first lesson prototype did not capture the intended feeling. Adding separate interactive blocks, oversized diagrams or a prescribed set of ingredients was insufficient. The approved revision became a continuous explanation: the question, the record, the probability carried by that record, the change of representation, and the consequences of that change. Text directs attention to the relevant parts of the figures; the figures make the reasoning visible; equations express the relationships precisely.

The user subsequently approved both its appearance and its teaching approach. They explicitly said future pages must not copy the same structure. They also approved the more purposeful, smoother interactions and requested this durable guide.

Interpret “3Blue1Brown-style textbook” here as a useful direction for reasoning and visual explanation, not a requirement for a video, a dark canvas, scripted spectacle, an imitation of a creator's assets, or an animation on every paragraph.

### Product context

- Personal quantitative researcher/trader preparation, shared foundation followed by separate paths; researcher first.
- Probability and statistics basics are familiar but need refresh and retention.
- Mental arithmetic starts with basic fluency and needs speed and accuracy.
- Python practice currently includes easy and medium algorithm problems. Explain prerequisites when harder material introduces them.
- Keep real reasoning depth in the curriculum. A foundation lesson can be approachable without making later interview practice trivial.
- Courses, original interview questions, coding, trainers and mental math matter. Articles and firm-attribution labels do not.
- No AI coaching, AI APIs, autocomplete suggestions or external runtime dependency. Authored explanations and ordinary interactive computation are appropriate.
- The user prefers professional restraint and has repeatedly rejected UI clutter. Every addition should earn its place.

## 3. The authoring principle: follow the ingredients of the subject

Start with the intellectual obstacle. What does the learner tend to confuse, and what observation would change their understanding? Write the reasoning first. Choose the representation that makes that reasoning easier to see or test.

A lesson is not complete because it contains a definition, a chart, a code sample and a quiz. It is complete when those elements, if present, help the learner build and use the intended concept.

Use this test for each proposed addition:

1. What exact idea, relationship or misconception does it address?
2. What does it reveal beyond the surrounding prose?
3. Where does the prose refer to it, and what should the learner notice?
4. How does it support a later inference or practice task?
5. Is it mathematically faithful, readable and controllable?

If the answers are weak, revise or remove the addition. The same test applies to an extra paragraph: length is not evidence of depth.

### Consistency versus variation

Keep consistent fonts, colors, navigation, control behavior, notation quality, accessibility and progress rules. Vary the opening, section structure, examples, visual representations, amount of code, interactions and derivation style.

A lesson might be an annotated proof, an investigation of a counterexample, a geometric explanation, a sequence of changing observations, a carefully worked research experiment, or an algorithm developed from a state definition. These are possibilities, not a rotation schedule. Never invent a different format merely for novelty.

The current content bank has seven teaching sections per lesson. That is an implementation fact, not the user's pedagogical requirement. A justified change in section count must also update its outline metadata and section-target mapping. Do not silently remove navigation targets while claiming flexibility.

## 4. Plan a lesson before building it

Read the target's current source, learning goals, quiz, worked example, linked interview questions and coding/trainer activities. Check the preceding and following lessons. Identify what this page must establish and what belongs later.

Prepare a small internal lesson brief containing:

- **Outcome:** a concrete thing the learner should explain, derive, critique or implement afterward.
- **Prerequisites:** facts the page can assume, and facts that need a reminder.
- **Central obstacle:** the misleading intuition or missing distinction.
- **Opening:** a specific question, experiment, conflict or prediction that creates a reason to read.
- **Argument:** the sequence of observations that resolves the obstacle.
- **Representations:** what each equation, figure, interaction or code block contributes.
- **Assumptions:** where they are introduced and where they are used.
- **Transfer:** a new case that tests reasoning beyond the opening example.
- **Practice handoff:** the existing activities in which the learner uses the concept.

This is a working brief, not a new visible block on every page. A short prose outline is often sufficient. Do not add project-management artifacts for an ordinary lesson edit.

## 5. Write for understanding, not coverage alone

### Define the experiment and objects before calculating

Specify what exists, what is observed, and what the symbols mean. A prior failure literally used n balls without introducing n. That is the kind of omission the guide must prevent.

Depending on the subject, define sample sizes, sampling rules, independence, distributions and their parameters, labels, random variables, dimensions, units, time indices, available information, objective functions and boundary conditions before relying on them. Say whether a statement is a definition, assumption, consequence, approximation or empirical observation when that distinction matters.

For a finite probability example, explain why records have equal weights instead of assuming equality from the fact that they can be listed. For a statistical example, explain the data-generating or sampling procedure. For a trading example, define the payoff, information and costs. For an algorithm, define the state and invariant.

### Let concrete reasoning lead into notation

A useful default is observation → named object → relationship → equation → interpretation. This is not a mandatory order. A familiar formula can instead open a lesson if examining its terms is the best way to expose the misconception.

Show intermediate steps where they carry the argument. “Therefore” should correspond to a reason the learner has actually been given. Explain why a denominator, covariance term, conditional probability, matrix constraint or boundary term appears. Name exactly where an assumption is needed.

Avoid unexplained jumps from a picture to a general theorem. If the figure illustrates rather than proves the statement, supply the missing argument and label the figure's limits.

### Develop examples as connected reasoning

Reuse an example when it lets the learner compare representations or change one assumption. Introduce a new example when transfer matters. Each change should be explicit: what stayed fixed, what changed, and why the conclusion changes.

Do not carry coins, dice and colored balls into topics for which they are no longer the useful model. Regression should not be made to look like the dice lesson simply to preserve a visual template.

### Ask selective, substantive questions

Use prediction or explanation prompts where a learner might otherwise read passively. Ask for a reason or a consequence: “Which term changes?”, “Does this evidence update the prior?”, “What state survives a failure?”, “What would break this conclusion?”

Optional disclosures can let the learner think before seeing reasoning. Their answers should supply the reasoning, not just “yes/no” or an unexplained result. Avoid repeating “Pause & explain” after every section. Do not hide prerequisites or the essential argument behind optional disclosure controls.

Ungraded prompts and explorations do not earn completion. The existing understanding check remains the grading boundary unless changing assessment is separately within scope.

### Add useful boundary cases

A small counterexample can have more teaching value than another page of general prose. Lesson 01's added AA-versus-AB example changes the replacement rule and shows why the earlier equal-size grouping argument no longer applies. It tests a condition of the rule instead of repeating its calculation.

Choose boundary cases that expose the target lesson's assumptions. Do not add pathological exceptions before the main concept is established, or broaden the page into everything adjacent to the topic.

### Know when there is enough

Depth means explicit assumptions, justified steps, understandable representations and transfer to a new case. It does not require a word quota. A strong foundation lesson also needs independent practice; reading an elegant explanation alone does not establish mastery or interview readiness.

## 6. Integrate prose, notation and visuals

Place an explanation near the object it explains. Introduce a figure before it appears, tell the learner what to inspect, and use the observation afterward. Captions should clarify meaning or limitations rather than repeat a heading.

Use selective bold for a crucial distinction or result; italics for attention or a change in perspective; color for objects that can be followed across representations. Entire paragraphs should not become a set of bold, colored fragments. The main text still needs to read well as prose.

Label mathematical components directly where practical. Lesson 01 annotates the numerator and denominator on the fraction instead of creating a disconnected legend. Similar annotations can explain a residual, a conditioning set, a covariance term or a transition probability. Use them only while they help; heavily annotating every formula makes reading harder.

### Color must carry meaning

Within an explanation, the same object should have the same color in prose, notation, a figure and a corresponding control/result. Introduce and maintain the mapping. A highlighted quantity should be named or labeled, not identifiable only by color.

Lesson 01 uses green for the selected event, teal for the sample space, red/blue for distinguishable dice or ball colors, and a muted rust for merging. In its later event comparison, A is specifically the red-die event and B the blue-die event. This is a locally explained change in meaning, not a universal rule that A must always be green.

Future lessons may need different semantic mappings: fitted values and residuals, past and future, posterior components, exposures or competing hypotheses. Choose a small coherent set from the existing palette. Do not color unrelated symbols with every available color.

### Figures must be mathematically honest

- Distinguish an exact enumeration from a schematic picture.
- If area or distance is not quantitative, say so when a learner could infer it is.
- Define axes, units, support, labels, direction and scale when they matter.
- Put labels where they describe the object without touching boundaries or colliding with other labels.
- Explain which information a representation preserves and which it discards.
- Check formulas, counted outcomes and displayed results against each other.
- A simulation illustrates a model; it is not a proof or an empirical trading result.

The earlier overlap diagram had a label near a boundary and visually muddled strokes. The correction placed (6,6) within the shared region, aligned counts and painted outlines after both fills. Retain the general lesson: inspect the final figure, not just its markup.

## 7. Decide whether a figure, interaction or code is needed

| Need in the argument | Possible representation | Decision criterion |
| --- | --- | --- |
| Explain a set, grouping or count | Outcome records, mapping, small grid | The learner can inspect why the count or weight arises. |
| Explain information updating | Conditional paths, area partition, before/after weights | The visual shows what the new observation rules out or reweights. |
| Explain a recurrence | State diagram and equations | Transitions make the required memory and restart behavior visible. |
| Explain a geometric relation | Projection, vectors or constrained directions | Geometry corresponds to the actual algebra and dimensions. |
| Explain variability | Repeated-sample plot or distribution comparison | The visualization distinguishes a statistic from its sampling distribution. |
| Explain dependence over time | Timeline, lag view or correlated paths | Time and information boundaries are visible. |
| Explain a computational failure | Minimal code with input/output comparison | Code reveals the mechanism more clearly than another verbal description. |
| Explain a precise derivation | Annotated equations and a worked example | A diagram would add little, so prose and math may suffice. |

For an interaction, identify the independent input, model update and observation. Change as few things at once as possible so the causal relationship is clear. Make the initial state meaningful and the current result truthful. Provide a readable explanation alongside it; the learner should not need to discover all meaning by dragging randomly.

Use native SVG/HTML/CSS or a suitable local plotting implementation for mathematical visuals. Native vector figures are inspectable, crisp and easy to keep consistent. Decorative generated images are usually not the right tool for this curriculum.

### Code belongs where computation helps

Useful reasons include enumerating a small space to check a derivation, demonstrating leakage, exposing a stability issue, simulating repeated sampling, implementing an invariant, or comparing an algorithm's behavior under a changed assumption.

Use the smallest understandable script that answers the question. Explain inputs, output and the connection to the math. A plot or result table may communicate the result better than showing every line of implementation. If code is displayed, preserve whitespace and syntax highlighting. If execution is offered, make its behavior and limits clear; do not introduce a new runner casually.

Do not insert generic imports, random arrays or boilerplate just because the user is preparing for quant roles. Do not require coding inside every course to mirror the Implement stage. Linked Python practice can remain the appropriate place to implement a concept. Lesson 01 deliberately has no embedded Python block.

## 8. Maintain the approved visual language

Use the existing site as the design system. The following are observed baseline values from the approved lesson, not immutable values for every layout.

| Element | Baseline |
| --- | --- |
| Page surface | Warm paper, #f5f2ed. |
| Main ink | #30372f; lesson prose #3d4438. |
| Supporting UI text | #5f6b54. |
| UI accent | Vermilion/rust in the existing site palette. |
| Editorial headings | Locally bundled Instrument Serif. |
| Reading prose | Georgia/Times serif fallback, 17px, line-height 1.85 on desktop; 16px at the small breakpoint. |
| Interface text | Locally bundled Geist. |
| Navigation and compact labels | Geist Mono where the existing interface uses it. |
| Mathematical notation | Locally bundled KaTeX with HTML and MathML. |
| Icons | Existing local Lucide library, consistent strokes and dimensions. |
| Main lesson heading | 54px desktop, 42px at the small breakpoint. |
| Section heading | 35px desktop, 31px at the small breakpoint. |
| Reading layout | Continuous, transparent article; figures integrated into the argument. |

Preserve meaningful spacing, hierarchy and comfortable reading width. The lesson does not need another border/background around every paragraph or figure. Avoid dashboard-style card walls, decorative gradients, enormous primary buttons, redundant labels and a duplicate page header.

Some whitespace is useful for reading. Reclaim unused side columns through the existing collapsible panels instead of filling every empty area with content. In the approved lesson, related practice moves below the reading at widths up to 1300px; the collapse control still works. Treat this as a layout reference, not an instruction to force all pages to those exact columns.

A short action label should fit comfortably. Check text wrapping, padding and arrow placement at narrow widths. Earlier “Read lesson & take check” text overflowed an oversized button; making an action prominent does not justify poor containment.

Keep the removed routine “PRIVATE · LOCAL / Saved locally” and “MELIH / PRACTICE ATELIER” banners removed. Meaningful save/recovery failure feedback remains useful; routine technical status should not dominate the study flow.

## 9. Use proper mathematical typesetting

Author math explicitly with inline `\(...\)` and display `\[...\]` delimiters. Use proper fractions, binomial coefficients, subscripts, superscripts, vectors and matrices. Do not show `(n2)` as a substitute for a binomial coefficient or leave formulas as plain-text approximations when real notation is available.

Introduce notation in prose. Clarify overloaded symbols such as vertical bars when first needed. Use display equations for derivations or relationships that need attention, and inline notation for small terms within a sentence.

JavaScript strings must preserve TeX backslashes. In an ordinary JS string or template literal, `\\frac` produces the required `\frac`. A single `\dfrac` can silently lose its backslash through string escaping; strict parsing and inspection must catch this. Python raw strings have different escaping rules. Test the actual rendered string, not the source's appearance alone.

Reuse `typesetMath(root)` in `static/app.js`, which uses local KaTeX, excludes literal code/input tags, emits HTML and MathML, and disables trust. Strictly parse authored and generated formulas in tests; the runtime's nonthrowing error behavior is not a substitute for checking them. Do not apply mathematical conversion to Python source or user drafts.

When TeX is inserted into an HTML string, escape HTML-significant characters before insertion. A literal less-than comparison such as `U<V` can otherwise begin a browser tag and swallow subsequent prose, even though KaTeX accepts the intended formula in a source-only test. The shared course math helper escapes its TeX; model tests decode HTML entities before strict parsing. Verify the complete surrounding sentence in the actual browser as well as the formula. Alignment ampersands in matrices must survive the same round trip.

On narrow screens, keep a long equation's overflow local to the equation. Avoid shrinking the whole page or making math illegible. Inspect the actual line, labels and fractions at the target width.

## 10. Make motion explain change

Animation should preserve object identity and direct attention to the change. It should not delay using a control or create a showreel. Do not add automatic loops, distracting entrances on scroll, or a play button simply to make a page seem dynamic.

### Approved lesson 01 behavior

- Coin outcome nodes stay mounted. Bar widths interpolate over 360ms with `cubic-bezier(.22,.61,.36,1)`.
- The 36 dice cells stay mounted. Event backgrounds and borders transition over 280ms.
- Ball records have stable keys. Ordered records split from their physical pair and reverse orders merge back; measured positions and figure height interpolate over 420ms with the same restrained easing.
- Replacement leaves routes and colored nodes in place. Only changed conditional fractions receive a small 240ms fade/vertical movement.
- Segmented controls transition their selected colors over 200ms.
- Choosing an already-selected option does nothing.

These timings are references. A new interaction may need a different duration, but it should be similarly deliberate and easy to follow. Do not copy the ball-record mechanism into a graph where it has no meaning.

### Implementation principles

Keep stable DOM nodes for stable mathematical objects. Updating an entire figure's `innerHTML` on every slider event destroys the browser's ability to interpolate its old and new state. Update styles, classes, labels and the changed math result in place.

When layout really changes, use stable keys and measured old/new positions. Read current visual geometry before cancelling an in-flight animation so rapid inputs retarget from the visible position. Batch geometry reads and DOM writes; avoid continuous forced layout in an animation loop. Size changes should not jerk surrounding prose unnecessarily.

Clean up interrupted animations and temporary elements. Lesson 01's merge copies are aria-hidden, non-interactive, unkeyed for future measurement, and removed on finish or interruption. Do not leave stale overlays or old state available to a screen reader.

The current mathematical result should reflect the selected input immediately; motion helps interpret the change. Do not make animated counters look like earned progress or freeze a slider while a visual transition finishes.

Honor `prefers-reduced-motion` in both CSS and JavaScript. Check the current preference when running a transition. Preserve the correct final state without motion and when the Web Animations API is unavailable. Avoid adding uncancelled timers or global listeners when the user leaves a lesson.

A settled screenshot demonstrates layout and state, not smooth frame pacing. Describe motion verification honestly; functional tests and visual checks do not establish a universal performance guarantee.

## 11. Preserve the learning journey and user work

The user specifically disliked losing the roadmap after opening a course. Keep the current module title, branch, Understand/Apply/Implement stages, Steps/Sections controls and next-step handoffs. Reading the lesson should lead naturally into applying and implementing it without requiring repeated trips back to the roadmap.

Maintain originating-module URLs, reload/Back behavior, exact roadmap return, linked activities, and the lesson-end continuation. Standalone library entry should still work.

**Updated practice contract, approved 2026-10-12:** each topic follows lesson → topic interview list → topic coding list. The interview list has Easy/Medium/Hard sections, each with at least two questions. The coding list has those same three sections, with exactly one exercise per difficulty. Students choose freely within a list; returning from a problem or exercise leads back to its originating list, rather than imposing a Q1 → Q2 → coding sequence. This applies to every existing and future topic. See [TOPIC_PRACTICE_STATUS.md](TOPIC_PRACTICE_STATUS.md) for the exact expansion scope and checks.

Author meaningful coding transfer from the topic itself: do not fill a difficulty slot with an unrelated algorithm. State any new prerequisite explicitly, especially in a hard transfer task. This practice requirement does not require code inside the illustrated lesson body. Inline code, figures and interaction still need to justify their contribution to the explanation.

Keep stable lesson/question/code IDs and the current grading semantics. A page visit, a slider drag, an expanded explanation, an animation or an ungraded prediction earns no completion. Lesson checks, numeric solves, written self-assessments, coding passes and trainer rounds remain distinct.

Preserve quiz selections, scratchpads, drafts, reading position and focus during unrelated layout updates. Do not change a stored assessment's meaning by silently changing question semantics or answer-index ordering. If assessment changes are actually in scope, consider their compatibility explicitly.

Development submissions must use the isolated preview workspace. Enter through `/test-preview.html#your-destination` and click **Enter test preview**; verify the Test preview notice before submitting. Bare `?qa=1` links, reloads and restored previews default to personal practice. Re-enter explicitly after reload; the exact workflow is maintained in README.md. Never solve an exercise, pass a check, import a fixture or create a trainer round in the user's ordinary workspace merely to verify UI. Read-only inspection and ungraded exploration in the personal page are suitable. Do not reset personal progress or drafts to restore a development baseline.

Check the personal disk file before and after work when relevant, but do not treat an old hash or zero-progress note as the future user's correct baseline. Record the baseline at the beginning of that work. As the user studies, their records will legitimately change. Browser state and disk state can also differ while synchronization is pending; inspect the relevant current state before drawing conclusions.

## 12. Keep accessibility and responsive reading intact

Use real labels, buttons, selects, ranges and native disclosure semantics. All meaningful controls need names and keyboard access. Preserve a visible, bounded focus indicator. The earlier roadmap outline crossed unrelated content; focus rings should identify the actual focused element without obscuring reading.

Give meaningful SVGs accessible titles/descriptions and text explanations. Decorative strokes should not be separate focus stops. Support non-color ways to recognize highlighted values and relationships. Update accessible event descriptions alongside visible highlights. Prefer restrained live announcements; do not announce meaningless animation frames.

Inspect desktop, narrow and short-height layouts. Check long headings, formulas, captions, select labels, slider labels, large-state figures and optional reasoning blocks. Sticky module controls must not conceal the active input or section target. Keep existing measured scroll offsets and available-height menus.

Native browser zoom is useful for enlarged-text/breakpoint inspection, but it is not a physical mobile/touch test. Restore zoom and any temporary layout changes. Actual screen-reader use and OS preference changes are separate checks; do not claim them from an accessibility-tree inspection or a mocked preference test.

## 13. Where the implementation lives

Paths below are relative to this project directory. Inspect live files because routing and architecture can evolve.

| File or area | Responsibility and editing rule |
| --- | --- |
| `static/lesson-sample-space.js` | Approved l01 authored body, math helpers, experiment models, bindings and motion. Read it as a reference; avoid turning its topic-specific functions into a mandatory lesson framework. |
| `static/lesson-sample-space.css` | Scoped l01 reading, figures, controls, responsive and reduced-motion styles. |
| `static/course-textbook.js`, `static/course-textbook.css` | Shared presentation helpers, authored-lesson registry and supporting figure styles. Helpers are implementation conveniences, not a mandatory educational structure. |
| `static/lesson-conditioning.js`, `static/lesson-expectation.js`, `static/lesson-distributions.js`, `static/lesson-stopping.js`, `static/lesson-arithmetic.js`, `static/lesson-variance.js`, `static/lesson-data-time.js` | Custom l02–l08 authored bodies and models/bindings. Their existence does not establish completed browser review; consult the status and evidence records. l08 includes purposeful, display-only Python rather than a new execution UI. |
| `static/lesson-likelihood.js`, `static/lesson-likelihood.css`, `likelihood_content.py`, `tests/test_likelihood.cjs` | l25 is the first research-driven addition, placed after l09 without changing existing IDs. Likelihood comparison, support boundaries and observation mechanisms determine its argument. The stable relative-likelihood curve is ungraded; it is not a posterior density. |
| `static/lesson-estimation.js`, `static/lesson-covariance.js`, `static/lesson-regression.js`, `static/lesson-inference.js`, `static/lesson-time-series.js`, `static/lesson-validation.js` | Custom l09–l14 bodies. Repeated-sample distributions, feasibility geometry, projection, inference design, covariance lag counts and information intervals each have their own explanatory structure. The time-series marker follows the plotted curve, with interruption and reduced-motion handling. |
| `static/lesson-search.js`, `static/lesson-research-defence.js`, `static/lesson-monte-carlo.js`, `static/lesson-algorithms.js` | Custom l15–l18 arguments: search/selection, a traceable research defence, designed simulation units and algorithm invariants. Code is display-only and used where it explains the computation. Review evidence belongs in the status record. |
| `static/lesson-fair-value.js`, `static/lesson-order-flow.js`, `static/lesson-continuation-growth.js`, `static/lesson-joint-risk.js`, `static/lesson-finance-core.js`, `static/lesson-strategic-calibration.js` | Custom l19–l24 arguments: conditional payoff/execution, selected flow, continuation/log objectives, joint risk, replication/local sensitivities and strategic inference/calibration. Figures are scoped to those arguments. Consult status/evidence for what was actually checked. |
| `static/app.js` | Shared lesson renderer, outline targets, module journey, quiz handling, math typesetting and binding dispatch. `authoredLesson(l)` selects l01's module or a registered authored lesson. |
| `build_content.py` | Regenerates the public content bank; contains l01 baseline metadata and conventional lesson content. Its l01 prose is not the approved illustrated body currently rendered by the custom module. |
| `course_lessons.py` | Conventional l02–l24 sections/examples and catalog/assessment metadata. Registered custom modules override the displayed body; this file is not the sole source of their visible prose. |
| `static/content.json` | Generated content; change source rather than making an isolated manual JSON edit that regeneration overwrites. |
| `static/index.html` | Local assets, ordering and cache-version tags. Include new authored assets before their consumers. |
| `static/style.css` | Existing shared design system; prevent local lesson changes from leaking to unrelated pages. |
| `math_markup.py` | Existing build-time math conversion; literal code and inputs must remain literal. |
| `tests/test_sample_space.cjs` | l01 isolation, targets, strict math, exhaustive experiment models, stable nodes, interruption, reduced motion, fallback and state-integrity checks. |
| `tests/test_course_textbook.cjs` | Current custom-course renderer isolation, outline/quiz continuity, strict authored math, independent model checks and ungraded binding integrity. Expand the declared changed set and coverage as new lessons are authored. |
| `tests/test_reading.cjs`, `tests/test_journey.cjs` | Section navigation and lesson-to-practice continuity. |
| `tests/test_course_examples.py` | Independent arithmetic checks for delicate expanded-course examples. Extend only when useful to verify a changed derivation. |
| `evidence/verification.md` | Dated test/browser evidence and exact limitations. |
| `COURSE_REDESIGN_STATUS.md` | Current per-lesson authoring/review state and remaining scope for the curriculum goal. Keep completion claims consistent with recorded evidence. |
| `data/progress.json` | Personal study data. It is not a content fixture or a development scratch file. |

When several lessons warrant custom rendering, a small explicit dispatch mechanism may be appropriate. Decide from the actual implementation scope. Reuse mathematical rendering, control styling and lifecycle utilities when useful; keep the pedagogy authored per topic. A generic framework or registry is not itself a user requirement.

`lessonSections(l)` currently uses an authored module's section titles when supplied, otherwise `l.sections`, then adds `lesson-example` and `lesson-check`. The custom body must provide matching targets exactly once. Preserve heading hierarchy and focusability. If the authored structure changes, update the actual outline source and rendered targets rather than leaving a misleading Sections menu. The registry currently generates numbered sections and a worked-example target; do not mistake that convenience for a reason every lesson needs the same argument. If a topic requires a different body arrangement, adapt the helper deliberately while preserving the target contract.

## 14. Topic-specific possibilities for remaining lessons

These are working ideas, not user-approved designs, mandatory components or completed work. Inspect each lesson and choose what explains its particular argument. It is reasonable to use none of the suggested visuals if a better approach emerges.

| Lesson | Possible explanatory emphasis |
| --- | --- |
| l02 Condition, then normalise | Observe evidence, remove incompatible possibilities, then renormalise remaining weights. A mixture-weight diagram may help. |
| l03 Expectation without independence | Decompose a quantity into indicators; show why dependence matters for variance rather than for linearity. |
| l04 Distributions as usable models | Choose a distribution from a mechanism; connect support and parameters to its behavior. Avoid an encyclopedia of density plots. |
| l05 A state is a sufficient memory | A partial-match state diagram can explain how failure preserves or erases information before writing a recurrence. |
| l06 Arithmetic with a method | Show efficient decompositions and regrouping; timed games belong in relevant trainers. |
| l07 Variance remembers dependence | Compare joint behavior and covariance contributions with an explicitly defined model. |
| l08 Write data code that respects time | A time/information boundary and minimal wrong-versus-correct Python example may expose leakage. |
| l09 Estimators, bias and uncertainty | Repeated samples can distinguish an estimate, estimator bias and sampling uncertainty. |
| l10 Covariance is a matrix constraint | Show what happens along a direction and why an impossible covariance matrix implies negative variance. |
| l11 Regression as projection | A geometric picture can link fitted values, residual orthogonality and the algebra. |
| l12 Inference is a procedure | Show repeated procedure outcomes and the interpretation of coverage or rejection, without mislabeling posterior probabilities. |
| l13 Dependent returns and effective sample size | Correlated sequences and uncertainty comparisons may show why observation count is not independent information count. |
| l14 Validation must imitate deployment | A deployment timeline can reveal train/test information boundaries and realistic evaluation. |
| l15 Search size belongs in the result | Compare a fixed analysis with repeated selection; state dependence and selection assumptions. |
| l16 Defend a research result | A concrete research claim can be examined through evidence, alternatives, limits and a falsification attempt. More diagrams may not help. |
| l17 Monte Carlo with variance reduction | Paired/control samples and an exact tractable case can explain reduced variance; computation can be justified here. |
| l18 Algorithms for a research notebook | Derive a state, invariant or data structure from the required computation; a short trace may be better than a large code listing. |
| l19 Fair value before a trade | Define the payoff and information, then derive a price; a payoff representation may help. |
| l20 Order flow is information | Conditioning on which orders arrive can make adverse selection visible. |
| l21 Continuation value and log growth | A decision tree or growth comparison can explain a defined objective; avoid conflating expected wealth and expected log wealth. |
| l22 Risk lives in joint exposures | Joint outcomes or factor directions can show risk missing from individual position summaries. |
| l23 The small mathematical-finance core | Use payoff identities and carefully defined assumptions; show code only if a numerical method needs explanation. |
| l24 Strategic inference and calibration | A structured information scenario and forecast-outcome comparison can reveal strategic updating or calibration. |

Do not claim these internal courses equal a particular employer's interviews. Difficulty and readiness need separate evidence. Use authoritative mathematical or teaching sources to verify uncertain technical claims when needed; write original explanations and avoid copying a commercial question bank, figures or assets.

## 15. Verification workflow for a future lesson update

### Before editing

Confirm the requested scope, read the approved reference, inspect the target's source and links, and capture the current personal-data baseline where appropriate. Do not start or replace a running server unnecessarily. Use the documented launcher if the local site is unavailable.

### Mathematical and functional checks

Use independent reasoning or exact small-case enumeration to verify changed calculations. Strictly parse the actual authored and generated TeX. Check all interaction branches, support boundaries and small/large allowed inputs. Assert that controls and result text describe the same current model.

Check section/example/check target uniqueness, linked activity destinations, repeated bindings, route departure, and focus preservation. For motion, test interruption, temporary-node cleanup, reduced motion and correct no-animation fallback. Ensure ungraded bindings do not call progress-saving or completion logic.

Run checks appropriate to the changed files. The following focused suites were used for the approved l01 implementation; adapt coverage when a different feature changes:

```sh
node tests/test_sample_space.cjs
node tests/test_reading.cjs
node tests/test_journey.cjs
node tests/test_boot.cjs
node tests/test_panels.cjs
node tests/test_accessibility.cjs
```

Run the actual changed lesson's math/content tests too. If Python course sources changed, include the relevant example checks; rebuild generated content only when its source actually changed. Do not regenerate coding assets or alter the judge for an ordinary prose/figure change.

Current l01 isolation tests assert the other 23 lesson renderings are byte-for-byte unchanged. When a later request intentionally updates another lesson, adapt that expectation to the explicit changed set while preserving assertions for all untouched lessons. Do not disable the isolation test merely because it catches an intentional new renderer. Retain l01 as a regression reference.

### Browser checks

Inspect the exact requested route in the available browser using current browser/computer-use instructions. Verify controls, math, labels and navigation visibly. Exercise small and large valid states, interrupted or repeated changes, disclosures and keyboard input. Graded interactions belong only in preview.

Review desktop, narrow and short-height states where relevant. Look at figure labels, formula overflow, focus and sticky-header offsets. Restore temporary zoom/state; never erase personal work. Save a small number of screenshots that show the important decisions, not every minor action.

### Closeout evidence

Record the changed lesson IDs, authored-source location, asset version, checks actually run, browser actually used, observed states, preserved-data evidence and remaining limitations. Keep screenshot and performance claims precise. Passing code checks does not certify teaching quality; user approval of a visual direction does not certify mathematical correctness.

Update the canonical evidence record and any necessary navigation pointers once. Avoid duplicating this guide into a growing set of session transcripts or competing design documents.

## 16. Acceptance review

Use these as review questions, not a visible checklist inside the product.

**Teaching:** Can the learner explain why the central result is true? Are prerequisites and assumptions explicit? Are symbols defined? Does the lesson resolve its opening? Is there an appropriate new case or linked task that demands the reasoning?

**Representations:** Does every figure/code block/interaction have a specific purpose? Is its meaning explained in nearby prose? Are quantities, weights and labels faithful? Could an unnecessary component be removed without losing understanding?

**Visual craft:** Does the page read as one authored piece? Are color and emphasis meaningful? Do diagrams and equations look carefully placed at normal and narrow widths? Are controls restrained, readable and contained?

**Interaction:** Is the selected state clear? Does motion preserve identity? Can rapid inputs interrupt safely? Do reduced motion, keyboard use and final-state fallback work? Does the learner retain their place in the module?

**Integrity:** Are identifiers, drafts, assessments and progress preserved? Are preview and personal work separate? Are statements about difficulty, correctness and verification supported by the evidence actually obtained?

A lesson is ready to deliver when these questions are answered concretely. Do not add more material solely because a page looks shorter than the reference.

## 17. Failure patterns to avoid

| Earlier or foreseeable failure | Correction |
| --- | --- |
| Undefined n, parameters or assumptions | Define the experiment and mathematical objects before using them. |
| Correct formulas surrounded by too little reasoning | Explain the steps and why their conditions hold. |
| More widgets mistaken for better pedagogy | Choose representations from the argument and remove additions without a teaching purpose. |
| Copying l01's section/widget sequence everywhere | Preserve quality and style while authoring the target topic's own structure. |
| Generic Python inserted to signal sophistication | Include code only when it explains or checks the subject better. |
| Oversized diagrams with awkward labels | Use a suitable scale, inspect actual rendered geometry and support responsive labels. |
| Random color or excessive bold | Maintain a small semantic mapping and emphasize only consequential distinctions. |
| Whole-figure replacement causes abrupt motion | Preserve stable objects; update their values or animate keyed layout changes. |
| Delayed/stale animation output after rapid inputs | Retarget from current geometry and cancel stale motion/temporary nodes. |
| Large buttons and redundant metadata dominate reading | Use existing restrained controls; preserve meaningful context and failure feedback. |
| The course loses its roadmap on entry | Keep module stages, next activity and exact roadmap return. |
| Testing creates apparent personal achievement | Use preview for graded work and preserve the current personal baseline. |
| Seven sections or a word count become a quality quota | Treat structure as a means to understanding; synchronize navigation when it changes. |
| A screenshot or passing tests are called a complete pedagogy/performance certification | Separate observed layout, functional correctness, mathematical checks and learning outcomes. |

## 18. Approved reference and recovery pointers

Read current source and evidence first. The following screenshots document the approved direction as of 2026-10-04:

- [Grouping and connected explanation](evidence/lesson01-textbook-grouping.png).
- [Annotated mathematical notation](evidence/lesson01-textbook-annotated-math.png).
- [Dice category comparison](evidence/lesson01-textbook-dice-comparison.png).
- [Overlap and corresponding derivation](evidence/lesson01-textbook-overlap-derivation.png).
- [Current probability weights](evidence/lesson01-motion-coin.png).
- [Ordered ball records](evidence/lesson01-motion-pairs.png).
- [New transfer question and reasoning](evidence/lesson01-transfer-check.png).
- [Narrow enlarged-text record layout](evidence/lesson01-motion-pairs-narrow.png).

The earlier boxed prototype and its embedded Python block are superseded as the visual/authoring reference. Narrow screenshots show a scrolling viewport, not a promise that an entire figure fits vertically. Settled motion screenshots do not measure smoothness.

The baseline asset version was `textbook-lesson01-20261004-4`. This is historical provenance, not a required version string for future changes. [Verification record](evidence/verification.md) contains the exact mathematical, test, browser and data-preservation evidence. [README](README.md) supplies launching and general editing instructions. [PROJECT](PROJECT.md) supplies the broader product contract.

## 19. How to resume when asked to update the rest

1. Read this guide and the current project instructions.
2. Reopen the current approved l01 implementation and inspect the requested target lessons.
3. Confirm the scope from the new user instruction. “Update the rest” authorises the requested remaining-course work; this guide alone does not.
4. Plan each lesson around its own concept and misunderstandings. Share useful UI/math utilities, not a rigid teaching script.
5. Implement in manageable lesson-sized changes with appropriate math, functional and browser checks.
6. Keep the originating learning journey and current user data intact.
7. Report which lessons actually changed and what was verified. Save exact remaining scope if work spans a context reset; never mark unreviewed lessons as complete.

When the user changes the direction, update this canonical guide with the new decision. Keep proposals visibly separate from approved requirements. Preserve one authoritative guide rather than accumulating competing versions.

## 20. Examples of authoring judgment

These examples explain the decision process. They are not additional approved designs or instructions to insert particular widgets.

### The approved sample-space lesson

The intellectual obstacle is that a list of possible outcomes does not by itself justify equal probabilities. The lesson first defines the experiment and what a record contains, then follows the probability carried by records when the representation changes. A grouping figure is useful because the learner can inspect which ordered records merge into an unordered outcome. The later replacement example tests whether those groups still have equal size.

The prose should tell the learner what the mapping reveals; the equation should express the probability consequence; the counterexample should expose the assumption. Removing any one of those explanatory connections leaves a weaker lesson even if the page still contains attractive pictures. Python would add little to this particular explanation, so its absence is a deliberate choice.

### A possible covariance lesson brief

Suppose a learner accepts any plausible-looking correlation table. The target outcome is to explain why a covariance matrix must give a nonnegative variance in every direction, and use that fact to reject an impossible matrix. Define the centered vector, its covariance matrix and a weighted scalar exposure before using matrix notation.

The argument can begin with the variance of a weighted sum, derive the quadratic form, then ask what a negative value would mean. A two-dimensional direction diagram may clarify how a weight vector selects an exposure. A small exact counterexample can establish the constraint without requiring a numerical eigensolver or a large interactive canvas. If a directional control is added, its purpose is to show the same matrix evaluated along changing weights; labels, formula and figure must refer to the same current weights. A code block belongs only if checking many directions or computing eigenvalues contributes something the derivation has not already made clear.

This lesson should not borrow dice grids, ball-merging motion or Bayes controls merely because those worked elsewhere. Its own obstacle determines the representation.

### Evaluate a draft as a learner

Read the argument without interacting first. Can the reader identify what is random, which assumptions are in force, what each symbol denotes and why the key step follows? Then inspect each figure without relying on color: do labels and prose still make its meaning clear? Change an input and explain the expected change before checking the result. Finally attempt a new case using the lesson's reasoning.

If a figure cannot be explained in one concrete sentence, its role probably needs clarification. If an interaction changes several unexplained things at once, simplify it. If a proof depends on a condition the reader has not yet seen, introduce that condition before the step. If transfer fails, repair the missing distinction rather than adding unrelated examples or more decoration.

### Decide what to add when asked whether a lesson is enough

Identify the specific gap: an undefined prerequisite, an unjustified transition, a misleading intuition, a missing boundary case or a weak practice handoff. Add the smallest explanation or representation that closes it. If no such gap is evident, retain the page's clarity and let the existing practice do its work. The user wants depth and craft; they have not asked for an indefinitely expanding textbook chapter.

When continuing across multiple context resets, leave the next target, its central obstacle, its authored-source location and unfinished checks in the existing status record. Future work should recover the argument and verification state, not reconstruct them from screenshots or optimistic completion labels.


## 21. Topic practice contract, approved 2026-10-12

Every existing and future topic follows **lesson → topic interview list → topic coding list**. The interview list groups at least two Easy, two Medium and two Hard questions; the coding list has exactly one exercise at each difficulty. Questions within a list are freely chosen. Returning from a detail goes to its own list, rather than forcing the next question. The originating topic and researcher/trader branch stay visible throughout.

Read the target lesson’s actual authored body and learning goals before selecting practice. Build escalation from its conceptual obstacles: explicit assumptions, meaningful changed conditions, worked derivations, counterexamples and substantive follow-ups. A Hard label needs deeper reasoning, not a larger number or longer prose. Written tasks use specific assessment obligations; numeric checks do not certify an unwritten proof. Coding contracts define information/order, boundaries, missing values, input mutation, outputs and defensible complexity. Check expected outputs with an independent small oracle, enumeration or exact calculation, rather than generating them by running the reference itself. For exact integer or rational outputs beyond JavaScript’s safe integer range, choose and state a lossless output format, such as canonical decimal strings, and verify the actual public sample and debugging-copy round trip. Do not let display or serialization silently alter an exact arithmetic contract. Share infrastructure, never a generic question template or compulsory diagram/code ingredient.

Practice sources live in `topic_practice/`; [the expansion status](TOPIC_PRACTICE_STATUS.md) tracks reviewed banks and remaining scope. Register future topics explicitly and satisfy the build coverage checks before publishing them. Every registered topic must meet the complete difficulty contract; there is no publishing exception for unfinished banks. Rebuild public JSON from Python sources; retain hidden coding cases in their source bank.

Permanent question/exercise IDs, grading meaning, saved drafts, assessed results and older journey bookmarks must survive. If an exercise moves out of a topic’s exactly-three coding list, explicitly register its old link in `LEGACY_CODING_LINKS`. Its `legacyCoding` metadata supports an additional-practice destination and return path without including it in the current list, completion counts, resume or Steps menu. Preserve any separate current link from another topic. The build rejects forgotten removed bookmarks, invalid legacy IDs and overlap with current slots; navigation tests cover both branches and verify that an additional-practice pass does not fill a current slot. Do not delete old work or invent a replacement pass.

Use the isolated preview launcher for graded browser checks and solution inspection. Compare actual personal question/code/lesson/draft/trainer records with a fresh baseline for the current work. Report reviewed topics and independently verified behavior, keeping unfinished topics explicit. This approved practice contract supplements the topic-specific teaching guidance; it does not require a uniform lesson layout or AI coaching.
