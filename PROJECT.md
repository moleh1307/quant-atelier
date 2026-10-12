# Quant Atelier

As verified 2026-10-12, the original 24-course authored textbook pass is preserved and a new likelihood/MLE module (l25) follows l09 on the researcher route. Current inventory: 25 lessons, 51 interview problems and 15 Python exercises. The researcher route has 19 modules, 42 distinct interview problems and 15 coding exercises. This is the first addition from the interview research; remaining coverage gaps are still open. l01 remains the approved reference; l02–l24 now render topic-specific authored modules. The shared foundation and both branches retain their original assessments, identifiers, module handoffs and personal data. Current curriculum state: [COURSE_REDESIGN_STATUS.md](COURSE_REDESIGN_STATUS.md); exact checks and limitations: [evidence/verification.md](evidence/verification.md).

Course authoring direction, approved 2026-10-04: [LESSON_AUTHORING_GUIDE.md](LESSON_AUTHORING_GUIDE.md) is the canonical guidance for future course updates. Lesson 01 establishes the approved continuous illustrated textbook approach; other lessons should choose their own explanatory structure. Read the guide before course work. Its topic suggestions are proposals, and this documentation request did not change other courses.

Final UX review, 2026-10-04: ready for local personal practice within the documented verification scope. Completed researcher/trader routes, all eight narrow main sections and representative lesson/answer/editor/trainer/recovery screens reviewed in Safari. Menu height follows available viewport space, arrow-key focus stays visible, and editor Esc→Tab/Shift+Tab lands directly on adjacent controls. Immediate per-tab save copies protect work while Web Locks are queued, with direct recovery for a reopened tab. Preview fixtures reversed; personal progress and original draft unchanged. See UX_REVIEW.md and evidence/verification.md for practical browser/storage/accessibility limits.

## Earlier implementation notes

Keyboard/readability pass (2026-10-04): practice skip link preserves the bookmarked module and focuses its heading; supporting labels, editor comments/line numbers and input borders have stronger contrast. Sections/Steps support arrows, Home/End and Escape. A native short-window failure was fixed with bounded, scrollable activity menus. Sixteen Node suites passed, including 36 defined text contrast pairs; Safari normal and 644×420 windows verified the module sequence, reload/exact return and section-menu reachability. Personal progress hash unchanged. Remaining acceptance is in UX_REVIEW.md.

Active UX refinement (2026-10-03): module continuity, resume unfinished core activities, progress filters and empty-result recovery, tab-local Back/reload recovery, stable form focus and accessible feedback. Lessons have a sticky Sections menu with current location and focused jumps. Compact header controls preserve reading position when opening navigation. Current coverage and remaining acceptance criteria: [UX_REVIEW.md](UX_REVIEW.md). Personal records remain separate from preview verification.

Backup import now has a comparison stage and persistent previous-record recovery. Selecting a file earns no changes; replacing requires both browser writes to succeed and waits for an in-flight judge. Review/restore verified in isolated Safari preview. Concurrent-tab saving now combines independent records and offers per-item conflict review with retained alternatives. Browser writes serialize through Web Locks when available; server writes use revision checks. Two-tab preview reconciliation and reload verified; rapid close/crash and unsupported-browser concurrency remain review items.

Trainer continuity (2026-10-03): entered text survives rerenders; tab-local checkpoints recover interrupted rounds on reload; route exits retain attempts and stop timers. Empty rounds add no history or completed drill and show no accuracy score. History links reopen mistakes, preserve Back focus and expose older retained rounds. Desktop/compact Safari timer expiry, reload and navigation verified; regression scope and limits in evidence/verification.md.

Python feedback (2026-10-04): source-line jumps, inspectable arguments/printed output and exact checked-source snapshots. Editing or navigating during a check keeps the new draft and reports completion without stealing focus; return links retain the original module. Reload retains completed feedback and gives interrupted checks a clear retry path. Seven-second request deadline and departed-document guards prevent stale results from awarding credit. Fourteen Node suites and eighteen Python checks passed; Safari normal/compact errors, retry, completed/pending reload and in-flight navigation verified. Broader acceptance remains in UX_REVIEW.md.

Revision continuity (2026-10-04): chronologically ordered due/upcoming items with readable provenance and a compact queue toolbar. Fresh revision preserves one previous answer/scratchpad; viewing/restoring it counts as assistance. Date receipts persist, queue return focuses the selected row after rescheduling, and written self-assessment guards remain explicit. Fifteen Node suites passed; native Safari normal/compact empty, due/upcoming, recoverable fresh work, assisted checking, scheduling and written comparison verified. Python library filters/reload/Back/keyboard empty recovery also verified. Preview fixtures were reversed; personal data unchanged.

Implementation status (2026-10-02): first working local version delivered. Open at <http://127.0.0.1:8768/> while the Python server is running. See [README.md](README.md) for the launcher and [verification record](evidence/verification.md) for checks and limits.

Course expansion (2026-10-03): all 24 modules now have three learning goals, seven teaching sections, definitions and explicit assumptions, worked derivations, failure cases and a substantial example. About 19,300 words total. Stable lesson IDs and original quiz answers preserve progress; new lesson source is `course_lessons.py`. Mental math links to arithmetic/fraction drills instead of an unrelated variance question. Mathematical and functional checks are documented in `evidence/verification.md`; these checks are not an independent pedagogical review.

Learning roadmap (2026-10-03): connected phases for shared foundation and a remembered researcher/trader destination; expandable module goals and related practice; distinct lesson/problem/code evidence; relevant drill rounds; next unchecked lesson, milestone state, bookmarked module locations and lesson sequence navigation. Shared exercises are deduplicated in route totals. No locks or AI coaching. The dashboard follows the selected branch.

Progress audit (2026-10-03): sample runs cannot be miscredited by overlapping Submit requests; accepted coding results preserve their submission-time assistance status; preview backups carry a workspace label and are blocked from personal imports; fresher browser records sync immediately to disk. Overview uses the 31 numeric questions as its numeric denominator; obsolete lesson/code IDs cannot inflate totals. Blank quiz submissions cannot select option zero. Personal state and draft preserved; regression and isolated Safari checks documented in the verification record.

Module continuity (2026-10-03): sticky module title/stage strip, Steps activity menu and next-step handoffs preserve the originating lesson and branch through problems, coding and drills. Context is bookmarkable and survives reload/Back, including shared exercises. Lesson-end continuation prioritises practice; roadmap returns locate the exact expanded module. Standalone library practice stays available. No navigation credit or grading change. Native Safari flow and compact layout verified; regression coverage in tests/test_journey.cjs.

Private browser-based quant practice for Melih. User-authorised 2026-10-02.

## Product contract

- Shared foundation, then researcher-first and trader branches.
- User knows probability/statistics basics but wants retention; arithmetic needs speed; Python currently easy/medium algorithm practice.
- Courses, original interview questions, coding, trainers and mental math. No articles, firm attribution, AI coaching, AI APIs, subscriptions or cloud dependency.
- Difficulty reflects reasoning depth: Easy refreshes one idea, Medium combines ideas, Hard requires a derivation, state recurrence, statistical critique or constraints. These are internal ratings, not verified employer cutoffs.
- Original content and worked solutions; no copying Tradermath's question bank or assets.

## Design and interaction

Polished product. Reference: user-supplied Tradermath screenshot and live practice flows inspected 2026-10-02. Warm paper palette, vermilion accent, serif editorial headings, monospaced labels, persistent sidebar, dense question tables, generous workspace margins. Typography: local Geist body, Geist Mono navigation/controls, and Instrument Serif headings; Teodor was identified on the reference site but is not bundled. Sidebar icons use locally bundled Lucide 1.49.0 with consistent rounded strokes; original diagrams remain native SVG code. Avoid marketing hero pages, decorative gradients and generic dashboard card walls.

Question: attempt -> graduated hints -> solution -> harder follow-up -> revision rating. Numeric checks and explicit self-assessment for explanations. Lesson completion requires passing its check. Coding requires actual Python tests. Trainer sessions record accuracy, pace and mistakes; stopped sessions are recorded as stopped. No fictitious historical scores.

Interface consistency review (2026-10-02): all eight main sections and representative detail screens checked at desktop, tablet and phone sizes. Supporting text, navigation spacing, controls, empty states and responsive practice layouts polished. See the verification record for exact coverage.

Python editor update (2026-10-02): offline CodeMirror 6 with Python highlighting, line numbers, bracket/quote closing, indentation, matching brackets and per-exercise undo history. No completion extension or suggestions. Existing draft, run and submit contracts retained; source and lockfile in `editor/`.

Reading layout update (2026-10-03): independent navigation and lesson-practice drawers with slim edge handles, locally bundled Lucide panel icons, hover/focus labels and labelled reopening tabs. Replaces the initial large toolbar buttons. Coordinated 320ms column/slide transitions and fading, with reduced-motion support. Collapsing panels reclaims their columns; preferences persist in separate local browser layout storage. Updates happen in place to retain quiz selections and drafts. Closed panels are inert and excluded from accessibility navigation. Desktop and compact layout checked through native Chrome controls in QA mode.

## Architecture

HTML/CSS/vanilla JavaScript; Python standard-library loopback server with a local subprocess judge. Browser progress backed up to a local JSON file with atomic writes. No external runtime assets. This is a trusted personal-code environment, not a public multi-user coding sandbox. Bind only to 127.0.0.1.

Mathematical typesetting added 2026-10-02: local KaTeX 0.19.0 with accessible MathML, explicit authored TeX spans, and responsive equation lines. Build-time conversions live in `math_markup.py`; actual Python source, sample data and numeric answer contracts are preserved.

## Calibration sources

- https://www.gresearch.com/career-guides/quantitative-researcher-interview-questions/
- https://www.janestreet.com/probability-markets/
- https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/

Sources inform subject coverage only. Problems, explanations and lesson wording are authored for this project. No employment or readiness guarantee.

Course reference checks for this expansion used primary teaching material; wording and examples are original:
- MIT 18.05 conditional probability: https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/mit18_05_s22_lec03.pdf
- Stanford CS229 regression: https://cs229.stanford.edu/summer2020/cs229-notes1.pdf
- Penn State STAT510 time series: https://online.stat.psu.edu/stat510/Lesson01
- MIT 15.450 simulation: https://www.ocw.mit.edu/courses/15-450-analytics-of-finance-fall-2010/4fa033082ff5ee58722a67fe81f0dce7_MIT15_450F10_lec03.pdf
- MIT 15.401 payoff/parity review: https://ocw.mit.edu/courses/15-401-finance-theory-i-fall-2008/d28223e0ac8822df9538f33b1542881e_MIT15_401F08_review_fin.pdf
- Stanford Kelly derivation: https://theory.stanford.edu/~blynn/pr/kelly.html
