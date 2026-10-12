# Quant Atelier

Melih’s private browser practice website. Shared foundation → quantitative researcher first → a separate quantitative trader path. No AI services, accounts, external assets, firm attribution, or articles.

Source repository: [moleh1307/quant-atelier](https://github.com/moleh1307/quant-atelier). The source is public; the application runs locally and each user's study records stay local. Personal progress (`data/`), runtime logs, local verification JSON exports and installed dependencies are excluded from Git. A fresh clone starts without anyone else's progress or drafts. This repository is not a hosted multi-user service.

## Open it

Double-click **Start Quant Atelier.command**. It opens the site and starts the local Python server if needed. Leave its Terminal window open; Ctrl+C stops it. Python 3.9+ is required (already available on this Mac).

Alternatively, from this directory:

```sh
python3 server.py --port 8768
```

Visit <http://127.0.0.1:8768/>. This is a local website; opening `static/index.html` as a file will not provide the Python runner or durable backup.

## Included

- 51 original interview problems: numerical answers and written reasoning, graduated hints, worked solutions, harder follow-ups, scratchpads, and revision scheduling.
- 25 lessons: 8 foundation, 11 researcher, 6 trader. Modules have topic-specific illustrated explanations, learning goals, explicit assumptions and worked examples. Understanding checks determine completion. Exercises are linked to each lesson.
- 15 Python exercises with actual local execution, sample runs, full test submissions, persistent drafts, and optional editorials.
- 5 generated trainers: mental arithmetic, fraction conversions, probability, sequence patterns, and conditional dice pricing. Difficulty levels, timed rounds, accuracy, pace, latency, and mistake review.
- Honest progress: unaided numeric checks, self-assessed written answers, reviewed solutions, passed coding suites, and passed lesson checks are distinguished.

Difficulty reflects the reasoning required within this bank, not verified equivalence to a particular firm’s hiring test. Some foundations are deliberately easy; hard exercises introduce dependence, selection, state recurrences, covariance constraints, and deployment-time validation. Public official interview guides were used only to calibrate topic coverage; the content and design assets are original.

## Authoring future lessons

Read [the lesson authoring guide](LESSON_AUTHORING_GUIDE.md) before updating course content or interactions. It records the approved lesson 01 direction, topic-specific teaching choices, visual and motion standards, implementation boundaries and verification workflow. Lesson 01 is a quality reference, not a structure to copy into every course. Project [AGENTS.md](AGENTS.md) routes future agents to this guide.

## Reading layout

Use the small panel handle at the left menu's edge to collapse navigation. In a lesson, the handle at the right edge collapses related practice. Closed panels leave slim labelled tabs for reopening. Hover or focus a handle for its action label; Tab and Enter/Space work from the keyboard. Panels slide and fade over 320 milliseconds while the reading width changes, with animations disabled for reduced-motion preferences. Choices are remembered locally, separately from study progress. Toggling panels preserves a selected quiz answer and entered text.

A module stays visible while you read, solve its interview problems and work in Python. **Understand → Apply → Implement** shows separate evidence; **Next step** continues the sequence, and **Steps** opens every activity in the same module. **Roadmap** returns to that exact expanded stop. These links retain the originating module and researcher/trader branch through reload and Back. Visiting an activity never earns completion.

**Sections** jumps through the lesson, example and understanding check. In either Sections or Steps, Up/Down enter and move through items; Home/End reach the first/last; Escape closes and returns focus to the control. Short browser windows use a bounded, scrollable menu within the viewport. The first keyboard link, **Skip to practice**, bypasses navigation and focuses the activity heading without changing its bookmark. Supporting text, syntax comments, line numbers and form boundaries use stronger contrast within the existing palette.

## Python editor

The workspace uses a locally bundled CodeMirror editor with Python syntax colours, line numbers, automatic bracket/quote closing, matching-bracket highlighting and four-space indentation. It provides no autocomplete, code suggestions or AI assistance.

- Enter carries Python indentation into the next line.
- Tab indents; Shift+Tab unindents. Press Esc, then Tab to leave the editor using the keyboard.
- Cmd+Z / Cmd+Shift+Z undo and redo on this Mac. Undo history survives sample runs, submissions and navigating between exercises within the same session.
- Restore starter can be undone. Draft text continues to save in the browser/local backup and survives reloads; undo history is kept only for the current page session.

Run checks only the visible example; Submit checks the complete suite. Error feedback includes line jumps when Python can identify the source line, failure arguments and optional printed output. **Checked version** shows the exact source sent to the runner. Editing while it runs keeps your new draft and labels the older result clearly. Leaving the exercise displays a check notice; **View result** returns to the originating learning module without stealing focus when the check finishes.

Results survive reload in this tab. A pending check interrupted by reload requires a fresh Run or Submit; restoring feedback never awards a pass. Python has a four-second runtime limit and the browser releases its busy state after seven seconds if the local request does not respond. Tab-local result recovery depends on session storage; portable progress backups contain drafts and earned results rather than this temporary feedback.

Build source and pinned packages: `editor/`. To rebuild the shipped bundle, run `npm ci` and `npm run build` there. Node/npm are not required for everyday practice. Upstream licenses and provenance are in `static/vendor/codemirror/`.

## Revision practice

The revision queue separates **Due now** from **Coming up**, ordered by scheduled date. Opening an item keeps a compact queue toolbar visible with its date, a direct return and the next due problem when available. Early revision stays available. Return restores the selected queue row, including after its due date changes.

Choose **Fresh revision** or **Fresh attempt** to hide hints/solutions and clear the active answer and scratchpad. The latest nonempty text is kept under **Show previous attempt**, including after reload. **Restore previous text** swaps it back while preserving the text it replaces. Viewing or restoring prior work marks the current attempt as assisted; existing historical results remain recorded. Only one previous answer and scratchpad are retained per problem, rather than an unlimited attempt archive.

A revision date appears below the scheduling controls. Scheduling alone earns no result. Written reasoning requires a substantial draft and comparison with the worked solution before **My reasoning matched** records an explicit self-assessment. Such records remain separate from automatically checked numeric solves.

## Trainer rounds

Begin a 1–3 minute round and enter numbers, fractions or expressions. Switching browser tabs keeps the timer running. Leaving the trainer or reloading ends the round and retains its submitted attempts; returning shows the summary. Reload recovery uses this tab’s session storage and the last checkpoint, so it stops the round instead of counting time spent away. An empty round shows no accuracy score and adds no history or completed drill. Existing earlier records are preserved.

Select a round under **Progress & data → Trainer history** to reopen its mistakes and results. **Back to trainer history** returns to that selected round. The newest ten are visible first; **Show earlier rounds** exposes the rest of the retained 200. Completed fluency evidence requires at least one answer or skip. This is practice evidence, not a mastery score.

## Progress and privacy

Browser storage holds progress and drafts. The local server also saves them atomically to `data/progress.json`. A timestamp chooses the fresher copy on startup; newer browser work is immediately backed up to disk, with an accurate save-status label. Use **Progress & data → Export progress** for a portable JSON backup. Import first compares current and backup totals; **Keep current record** cancels without changes. **Replace with this backup** keeps a browser recovery copy before replacing the complete record and drafts. Use **Review previous record** to inspect and restore it, including after reload. Each replacement keeps the immediately preceding record; portable exports remain useful for longer history and moving browsers. Storage failures abort replacement, and a running Python check must finish first. New exports carry a personal/preview workspace label; preview exports cannot be imported into personal progress. Startup, disk/tab reconciliation and recovery also reject known foreign workspace labels, and new cached Python results identify their workspace. Older unlabelled backups remain supported with an origin warning. Nothing is sent to an external service.

**More than one tab:** independent changes combine automatically. If two copies edit the same draft or practice record, a notice links directly to the conflicting items in Progress & data. Select the version to keep and choose **Save chosen changes**. Both previous copies remain available for review, including copies left by a closed tab. Imports wait until a conflict is reconciled. The disk backup checks its revision before every write, so an older tab cannot silently replace a newer server record. Reload tabs opened before this update to load these protections. Browsers with Web Locks serialize browser saves; use one editing tab in browsers without Web Locks, where truly simultaneous browser writes have weaker protection.

**Closing a tab during a save:** the latest edit gets an immediate browser recovery copy before a queued save runs. Reopening the same tab merges it with independent saved work; competing changes still require review. If the browser creates a new tab instead, a recovery notice opens the saved tab copies directly. Review the comparison before replacing, and your current record remains recoverable. A real browser or OS crash can retain only data the browser actually persisted; if browser storage is unavailable, export your work before closing.

The website uses no cookies or analytics. All frontend assets and the question bank are local. The server binds only to `127.0.0.1` and rejects unexpected Host and cross-site Origin values. Do not expose it through a public tunnel or network-facing proxy.

The Python runner is for **your own trusted practice code**. It restricts imports, certain builtins and private attributes, runs in a subprocess, caps CPU/output, and has a four-second timeout. These are helpful limits, **not a hardened sandbox for hostile code or a multi-user service**. Code runs on this Mac. The supplied tests validate behaviour; passing them does not prove every complexity claim or mathematical argument.

## Content and validation

Before course edits, read [LESSON_AUTHORING_GUIDE.md](LESSON_AUTHORING_GUIDE.md). It records the approved teaching direction, topic-specific design decisions, mathematical and interaction standards, rejected patterns, and recovery procedure. [COURSE_REDESIGN_STATUS.md](COURSE_REDESIGN_STATUS.md) tracks the current curriculum work separately from this durable contract.

`build_content.py` regenerates `static/content.json`; it contains l01 baseline prose/metadata, while `course_lessons.py` holds conventional l02–l24 content and metadata. The approved illustrated l01 body instead lives in `static/lesson-sample-space.js` and its CSS. It uses continuous serif prose, coordinated mathematical colors and explanatory figures, without embedded Python. Its original check and metadata still come from the content bank. Persistent nodes and keyed records support purposeful motion; explorations remain ungraded.

As observed 2026-10-09, custom l02–l24 bodies are registered through `static/course-textbook.js` from the conditioning, expectation, distributions, stopping, arithmetic, variance, data-time, estimation, covariance, regression, inference, time-series, validation, search, research-defence, monte-carlo, algorithms, fair-value, order-flow, continuation-growth, joint-risk, finance-core and strategic-calibration lesson modules. These modules own their visible prose and section outline; the content bank retains quiz/catalog metadata. l08's small Python examples explain timing and do not introduce a lesson runner. Review status belongs in the status and evidence records. Edit the source that actually renders the target, not generated JSON. `coding_bank.py` separately holds private test cases and regenerates public `static/coding.json`.

Typography uses locally bundled Geist for body text, Geist Mono for navigation and controls, and Instrument Serif for headings. The Geist fonts match Tradermath’s current interface; Instrument Serif is an open-source alternative to its commercial Teodor heading font. Font licenses and provenance are in `static/vendor/fonts/`. Sidebar icons use Lucide 1.49.0, bundled locally in `static/vendor/lucide/` with upstream licenses.

Mathematical prose uses locally bundled KaTeX 0.19.0, including fonts and its MIT license. `math_markup.py` converts the existing reviewed formulas at build time; new content can use `\(...\)` for inline notation and `\[...\]` for separate equations. Python code and user drafts remain literal. Longer equations scroll within their line on narrow screens.

```sh
python3 build_content.py
python3 coding_bank.py
python3 -m unittest discover -s tests -v
node tests/test_frontend.cjs
node tests/test_math.cjs
node tests/test_roadmap.cjs
node tests/test_boot.cjs
node tests/test_progress.cjs
node tests/test_journey.cjs
node tests/test_navigation.cjs
node tests/test_resume.cjs
node tests/test_panels.cjs
node tests/test_reading.cjs
node tests/test_sample_space.cjs
node tests/test_course_textbook.cjs
node tests/test_likelihood.cjs
node tests/test_recovery.cjs
node tests/test_sync.cjs
node tests/test_trainers.cjs
node tests/test_runner_ux.cjs
node tests/test_revision.cjs
node tests/test_accessibility.cjs
```

Personal practice is the default, including old `?qa=1` bookmarks and restored tabs. The launcher always opens the ordinary root URL. Startup removes accidental QA parameters while preserving the lesson/route destination and other query parameters before reading study records.

For browser QA, open `/test-preview.html#your-destination` (for example `/test-preview.html#paths/researcher`) and click **Enter test preview**. This supplies a short-lived, single-use entry ticket for the separate `?qa=1` workspace and disables disk progress writes. Merely viewing the development launcher grants no preview entry. Reloading, reopening or restoring a preview through Back/Forward returns to personal practice; explicitly re-enter through the launcher when testing reload recovery. Verify the **Test preview** notice before graded development actions. Test records and drafts remain in separate browser storage and are never reset by the entry guard. It still uses the actual Python runner. Tests use isolated fixtures/temporary progress directories; user progress is not changed. Screenshots and the verification record are in `evidence/`.

As of 2026-10-03, all 24 modules contain learning goals, seven teaching sections, explicit assumptions and a worked example: approximately 19,300 words across the curriculum. Definitions precede the derivations; changed assumptions and common failure cases are discussed. Written interview derivations remain self-assessed. The understanding check tests one key idea per module and does not certify full mastery.

## Follow your roadmap

Open **Learning roadmap**. The eight shared modules lead into ten researcher modules or six trader modules. Researcher is the default; choosing a branch is remembered and also drives Overview's next activity. All modules remain accessible.

The module containing the first unfinished core activity expands automatically. Overview and the roadmap resume its lesson check, interview practice or Python exercise; passing a check leaves outstanding practice visible. Optional fluency rounds remain available without blocking core completion. Open any module to see its learning goals and activities. Each lesson ends with a direct continuation into its remaining practice, a return to its exact roadmap module and an optional jump to the next module.

Progress uses your existing records: lesson checks, unaided numeric solves, written self-assessments, full Python test passes and finished relevant drill rounds. Reviewed answers do not count as solves. Coding passes record whether the submitted attempt used an editorial. Reading the editorial later does not relabel an earlier unaided pass. Run and Submit are disabled together during execution, and only a successful full-suite submission earns a coding pass. A repeated exercise link counts once in route totals. Passing a lesson check advances the route while leaving its practice exercises outstanding.

The roadmap uses keyboard-operable native disclosures, subtle opening motion and reduced-motion styles. Independent optional reading panels remain available. New topics and harder practice sets can be added through the same content schema.

## Stay with a module

Opening a lesson or practice link from the roadmap keeps that module with you. A compact sticky strip shows its title, the active Understand / Apply / Implement stage (or Fluency), and actual check/problem/code evidence. **Next step** moves from the lesson into its questions and Python exercise. The same handoff appears below the lesson check and at the end of a problem or coding page. All activities remain optional; visiting one earns no progress.

For example, module 01 flows through Count the right sample space → One six is enough → Without replacement → Count pairs with a target sum. Use **Steps** to jump directly to any activity, or **Roadmap** to return to the exact expanded module. The menu highlights your current activity, retains assistance/self-assessment labels, closes with Escape or a click outside it, and remains scrollable on short screens.

Inside a lesson, **Sections** stays beside Steps. Jump to any teaching section, the worked example or the understanding check. The selected destination receives focus and lands below the sticky controls. Its highlight follows your reading position; it is a location marker and earns no completion credit. Escape returns focus to Sections. Reading position still survives Back and reload.

Activity URLs include the originating module and branch. Reload and browser Back retain the sequence, including an exercise shared by several modules. Directly opening a lesson from Courses starts its own sequence; standalone questions and coding pages keep their existing library behaviour. Completed practice is skipped when resuming from a lesson. The final activity offers the next module, while outstanding evidence remains visible. No new completion records or changes to grading are introduced.
