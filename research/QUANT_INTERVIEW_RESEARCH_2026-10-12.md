# Quant firm interviews and the next Quant Atelier curriculum

**Implementation update, 2026-10-13:** Dedicated calculus and optimization foundations now exist as l26/l27 before l09/l25. Their assessment covers derivatives/composition, directional curvature, reverse mode, stable evaluation, convexity, conditioning, line search, Newton failure, constrained certificates and KKT degeneracy. Each adds six interview problems and three codes. This updates the dedicated-optimization gap in the original dated audit below. Resampling/bootstrap now has a dedicated l28 chapter after dependence and before validation, with assessed empirical/error-law, paired, block, unequal-cluster and nonregular problems. Substantive regularized/statistical learning, broader ML, broader algorithms and open research projects still need further curriculum work. See also [resampling implementation](../evidence/RESAMPLING_BOOTSTRAP.md). See [the implementation audit](../evidence/CALCULUS_OPTIMIZATION.md).


Research checked on **12 October 2026**. This report covers quantitative researcher and quantitative trader preparation, primarily for internships, graduate recruitment and early-career roles. It informs future curriculum work; it does not change the website or certify interview readiness.

## 1. Main finding

Quant Atelier is a useful starting curriculum, but its present breadth and assessment depth are insufficient to call it comprehensive preparation for the research roles considered here. Expanding the number of puzzles would help only partly. The larger needs are mathematical statistics, statistical learning, optimisation, algorithms, open-ended data analysis and the ability to defend a research decision.

For trading, the gap is different: fluent probability and expected-value reasoning, numeracy, decisions under uncertainty, adaptation to new information and clear communication. Difficult reasoning can arise from elementary ingredients. Advanced mathematics is relevant to some research specialisms, but it is not a universal entry requirement for every quant interview.

These curriculum conclusions are **my synthesis**, not a syllabus endorsed by any employer. They come from the firm evidence below and the actual local content inventory.

## 2. How to interpret the evidence

Three evidence types must remain separate:

1. **Interview guidance:** strongest evidence for published stages and assessed skills.
2. **Job requirements and role descriptions:** evidence about the work and desired background, not proof that every listed subject appears in an interview.
3. **Curriculum proposals:** our decisions about how to prepare. They should be useful across firms without pretending to reproduce proprietary assessments.

Current official webpages and employer preparation documents were prioritised. Older documents are dated when used. Candidate anecdotes, preparation-company claims, purported leaked questions and advertised passing scores were not used to establish technical requirements. Several official pages do not publish the complete interview sequence. An unknown stage should remain unknown.

Processes vary by office, team, candidate background and recruitment cycle. A Sydney campus FAQ cannot establish the Amsterdam process, and an engineering guide cannot establish a research interview. The recruiter invitation for a specific application is the final operational source for that application.

## 3. Requested firms

### IMC

**Published process.** IMC's APAC campus guidance describes assessments, a recruiter behavioural conversation, a technical interview and a final assessment day with technical and behavioural stations. Its broader recruitment page says assessments vary by role and may include a technical home assignment. This is APAC guidance, not a fixed global quantitative research sequence. [Campus interview preparation](https://www.imc.com/ap/articles/how-to-prepare-for-an-interview-at-imc), [recruitment process](https://www.imc.com/ap/careers/recruitment-process).

**Trading knowledge.** IMC's Europe trader preparation document covers probability, expected value, conditioning, independence, Bayes reasoning, numeracy and market-making problems. Pricing, spreads, inventory and information matter. It also stresses explaining an approach, recognising uncertainty and adapting. The guide says its coverage is not exhaustive; it does not require proving complex mathematical theorems. [Official trader preparation PDF](https://cdn.sanity.io/files/l1io23s3/production/386c4a31665862232d285b19f53378d0d04dcfec.pdf).

**Research knowledge.** The Chicago 2027 BS/MS graduate researcher posting describes rigorous data analysis, mathematical modelling, custom research tools and implementation into production. Programming proficiency is highly desired. This establishes that research preparation must extend beyond fast arithmetic; it does not publish the research interview's exact stages. [Graduate researcher role](https://www.imc.com/in/careers/jobs/4907368101).

**Implication for us.** Add problems that evolve: first estimate value, then condition on new evidence, then choose an action and discuss risk. Research exercises should require code and evidence supporting a model, rather than merely knowing a formula. Behavioural preparation should use real examples of learning, mistakes and collaboration.

### Jane Street

**Published process and role distinction.** Jane Street describes early phone interviews and an in-person final for trading. Possible final topics include probability, statistics, coding, data analysis and problem solving. Its trading guidance explicitly says elementary mathematics is sufficient and prior finance knowledge is not tested. The interviews emphasise reasoning, conversation, feedback and correction. This statement must not be broadened into a claim that every research or ML role requires only elementary mathematics. [Trading interviews](https://www.janestreet.com/trading-interviews/).

Jane Street explicitly says quantitative research interviews combine elements of trading and software engineering interviews. It also distinguishes a machine learning interview track. Candidates can use a language they know well; learning OCaml solely for interviewing is unnecessary. [Role-specific interview overview](https://www.janestreet.com/join-jane-street/interviewing/).

**Technical preparation.** Its official probability and markets guide spans counting, random variables, expectation, conditional probability, confidence intervals and market making, including adverse selection. [Probability and Markets PDF](https://www.janestreet.com/static/pdfs/trading-interview.pdf).

**Implication for us.** Keep deep elementary probability in the shared foundation. A question should support follow-ups, counterexamples and changes in assumptions. The researcher branch also needs coding and data reasoning. Speed alone, isolated puzzle memorisation and advanced-theorem collecting are poor substitutes for this combination.

### Optiver

**Published process.** The current Sydney campus FAQ, dated 5 January 2026, distinguishes:

- Trading: application → online assessment → behavioural interview → final interview day.
- Research: application → online assessment → behavioural interview → technical assignment → final interview.

These answers were verified by expanding the FAQ in the browser; the ordinary text extraction initially exposed only the questions. This is Australia/New Zealand campus guidance. [Sydney recruiting FAQ](https://www.optiver.com/join-us/stories/optiver-sydney-campus-recruiting-faqs/).

**Research knowledge.** The Amsterdam 2027 graduate researcher role names probability, calculus, linear algebra and programming, preferably Python. It presents ML as central to a research cycle involving data, model construction, testing and deployment. Its selected applicants receive an assessment invitation, but the posting does not enumerate all subsequent interview rounds. [Amsterdam graduate research role](https://www.optiver.com/join-us/jobs/quantitative-research-and-machine-learning/amsterdam/graduate-quantitative-researcher-2027-start/).

**Implication for us.** A researcher curriculum should contain mathematical ML foundations and an assignment-style research task. Trading preparation should preserve timed numeracy and uncertain decisions. Do not attach a universal “80 in 8” format, penalty scheme or pass mark to all Optiver applications: the reviewed official evidence does not establish one current global rule.

### Hudson River Trading (HRT)

**Published student process.** HRT's student FAQ lists a coding test, one or two technical phone screens and a multi-round onsite. Topics and duration depend on the role. Algorithm Developer candidates can select Python or C++. Student routes include undergraduate, master's and PhD candidates; prior finance experience is not required. [Student opportunities and FAQ](https://www.hudsonrivertrading.com/student-opportunities/).

**Research role.** HRT's Algorithm Developers work on statistical analysis, predictive models and model performance. Core software engineering has a different emphasis, including low-level systems. HRT's engineering interview article explicitly excludes Algorithm Development research/trading, so its engineering-specific assessments cannot simply be imposed on the research branch. [Role descriptions](https://www.hudsonrivertrading.com/work-at-hrt/), [engineering interview guide](https://www.hudsonrivertrading.com/hrtbeat/engineering-and-interviewing-at-hrt/).

**Implication for us.** Research candidates need both mathematical reasoning and dependable algorithmic coding. Include complexity analysis, tests, edge cases and explaining an implementation. Do not make C++ mandatory for this user's initial researcher path, and do not mistake operating-system trivia for a universal research prerequisite.

### G-Research

**Published process.** The current quant interview guide describes application, a general quant or ML-specific quiz, technical interviews and leadership interviews. It describes a typical general route with four one-hour technical interviews, including in-depth mathematics; an ML-suited profile has two one-hour ML interviews with relevant mathematics, statistics and programming. This is unusually explicit evidence of substantial subject depth. [Quant interview guide](https://www.gresearch.com/career-guides/quantitative-researcher-interview-questions/).

**Document variation.** Its linked July 2025 reading PDF also mentions a triage stage and subject combinations. The web summary and PDF should not be joined into a supposedly universal fixed round count. The PDF recommends advanced quant practice, coding practice and *The Elements of Statistical Learning* for ML preparation; detailed prior finance knowledge is not assumed. [Official recommended reading PDF](https://www.gresearch.com/wp-content/uploads/2025/07/Quantitative-research-and-machine-learning-interview-prep-recommended-reading.pdf).

**Research background.** The London postgraduate role seeks a master's or PhD in a quantitative subject and interest in translating theoretical ideas into working code. It describes advanced statistical research and ML, while also offering internal ML training. This supports deeper preparation without implying candidates must already master every ML technique. [Postgraduate researcher role](https://www.gresearch.com/vacancies/quantitative-researcher-postgraduate/).

**Implication for us.** G-Research is a strong reason to add mathematical statistics, derivations, optimisation and substantive ML. Short conceptual checks are not adequate evidence for hour-long subject interviews. Add problems requiring an argument, not just recognition of the correct statement.

### Citadel

**Published campus research process.** Citadel's guide, published 9 November 2024 and still available at review, describes a 45–60 minute remote first round combining technical and behavioural assessment. Topics include programming, research ability, data structures/algorithms and problem solving, using CoderPad. Python and C++ are core languages, but other languages are welcomed. The usual second round contains three to five 60-minute onsite interviews, followed by team review and a possible offer. These are campus research details, not a guarantee for every team or experienced application. [Campus research interview process](https://www.citadel.com/careers/career-perspectives/our-quantitative-research-interview-process/).

**Implication for us.** Research preparation must include algorithms, discussing previous projects and explaining technical choices under follow-up questions. A polished notebook is not enough if the candidate cannot justify the baseline, assumptions, validation and practical limitations. We should prepare for sustained interviews, not only three-minute written answers.

### Citadel Securities

Citadel Securities is a separate firm, despite the shared campus recruiting guide. Its published research process has a similar remote/onsite/team-review structure. Its researcher FAQ identifies probability, statistics, predictive modelling, programming and applied research; it emphasises explaining and reconsidering approaches. [Research interview process](https://www.citadelsecurities.com/careers/career-perspectives/our-quantitative-research-interview-process/), [research candidate FAQ](https://www.citadelsecurities.com/careers/career-perspectives/candidate-faqs-quantitative-research/).

The researcher role also describes large datasets, mathematical models, backtesting and live implementation, with time series and ML among preferred skills. This is role evidence, not a promise of a question on every named technique. [Researcher role](https://www.citadelsecurities.com/careers/details/quantitative-researcher-quantitative-research-analyst/).

For markets/trading, its FAQ instead emphasises uncertainty, programming, algorithmic reasoning, statistics and updating quickly. That page does not establish the same fixed stages as the research guide. [Trading candidate FAQ](https://www.citadelsecurities.com/careers/career-perspectives/candidate-faqs-markets-trading/).

**Implication for us.** Teach research and trading as connected but distinct. The trader should interpret information and act; the researcher should develop and validate evidence. Both need to explain their reasoning and handle a changed premise.

## 4. Additional useful comparisons

### Two Sigma

Its official research/modeling guide identifies three interview areas: open-ended data analysis, coding/algorithms and statistics or the candidate's research domain. It describes practical problems and discussion in video interviews, with preparation guidance and opportunities to clarify and iterate. It does not establish one universal round count. [Research/modeling interview guide](https://www.twosigma.com/interviewing-for-quantitative-research-modeling/).

**Curriculum implication:** add small messy datasets with no prescribed technique. Ask the learner to formulate a question, choose a baseline, justify an estimator, inspect failure modes and state what the evidence supports. This prepares a different skill from solving a fully specified puzzle.

### D. E. Shaw

Its official interviewing guide describes application review, phone/virtual interviews, references and an offer stage. Technical roles can involve mathematics, statistics, algorithms, logic and programming, alongside discussion of earlier work and methodological choices. Requirements differ by role; statements about fundamental analysts should not be transferred to quantitative researchers. [Official interviewing guide PDF](https://www.deshaw.com/assets/articles/D_E_Shaw_Group_Interviewing_Guide.pdf).

**Curriculum implication:** combine rigorous technical practice with defence of assumptions and past research. Do not build one indiscriminate finance-and-coding syllabus for every position carrying a similar title.

### DRW

Its quantitative trading analyst account describes a take-home quantitative screen, an approximately 45-minute probability/statistics Zoom interview, and a final day involving Python quantitative coding, a trading simulation and technical interviews. It discusses scientific Python tools and market knowledge. This is a particular trading analyst route, not a fixed sequence for all DRW research vacancies. [Quantitative trading analyst recruitment](https://www.drw.com/updates/insights/the-journey-of-a-quantitative-trading-analyst-at-drw).

**Curriculum implication:** do not eliminate market literacy entirely. Basic mechanisms, risk and trading decisions should be taught concretely alongside the mathematics, even when finance knowledge is not required at another firm's entry interview.

### Susquehanna / SIG

The official indexed London 2027 graduate trader posting emphasises quantitative problem solving and communication, and describes training involving game theory, poker, options and programming without requiring prior finance background. Direct retrieval of the posting returned an access error; only its indexed official text was available. It does not establish a complete current interview sequence. [London graduate trader posting](https://careers.sig.com/jobs/11031).

**Curriculum implication:** strategic decisions, uncertainty and calibration are useful preparation. This evidence does not justify claiming that every interview includes poker or a specific game. A historical Sydney process on an external recruitment board should not be substituted for a current London process.

Jump Trading was also investigated, but the retrieved experienced-researcher material did not provide a sufficiently clear current graduate interview sequence. It is intentionally not assigned an invented sequence or a universal entry-level skill bar here.

## 5. Comparison for curriculum design

The following is an **interpretive preparation map**, not an employer-issued weighting or a ranking of firm difficulty.

| Target | Main preparation emphasis supported by the sources | What would be misleading |
| --- | --- | --- |
| IMC trading | Probability, numeracy, value, information, risk, adaptation | Treating arithmetic speed as the whole job |
| IMC research | Mathematical models, rigorous data work, implementation | Assuming the APAC trader sequence is its global QR sequence |
| Jane Street trading | Deep elementary probability and interactive reasoning | Assuming advanced finance is required |
| Jane Street research | Trading-style reasoning plus software/data skills | Copying only the trader syllabus |
| Optiver research | Mathematical ML foundations and research assignments | Assuming one globally fixed online assessment |
| HRT Algorithm Development | Statistical modelling plus algorithmic coding | Importing the entire core-engineering interview syllabus |
| G-Research | Substantial maths, statistics, programming; profile-specific ML | Assuming all profiles have identical interviews |
| Citadel research | Coding, algorithms, research reasoning and project discussion | Preparing only probability puzzles |
| Citadel Securities | Applied modelling or trading decisions, depending on role | Treating research and trading as the same assessment |
| Two Sigma research | Open-ended data analysis, algorithms and statistical reasoning | Training exclusively on fully specified questions |
| D. E. Shaw quant roles | Technical depth and methodological explanation | Combining all job families into one prerequisite list |
| DRW trading analyst | Probability, Python/data, simulation and markets | Treating all finance knowledge as irrelevant |

There is no defensible universal conversion from these descriptions to “LeetCode Medium” or “LeetCode Hard.” Coding-platform labels capture only part of the task. An elementary probability question can be demanding because the model is hidden, the assumptions change or the explanation must remain sound through several follow-ups.

## 6. What knowledge should the shared foundation contain?

The list below is a proposed preparation standard, not a claim that every firm tests every item.

### Probability that can be used without prompting

Counting with an explicit sampling procedure; conditioning and Bayes; expectation via indicators; variance and covariance; independence versus lack of correlation; standard distributions; conditional expectation and total variance; recurrences and stopping problems. Learners should be able to choose a method before seeing a chapter label.

Depth matters: explain why a calculation is valid, construct a counterexample, change an assumption, and estimate whether a numerical result is plausible. The present l01–l05 and l07 are good anchors, but practice should extend well beyond their first worked examples.

### Mathematical fluency

Vectors and matrices, projections, rank, eigenvalues and positive semidefiniteness; derivatives, gradients, Taylor approximations and constrained optimisation; translating a mathematical statement into an algorithm. Research extensions should include numerical stability and convexity. Teach these because they explain estimators and models, not as disconnected prerequisites.

### Programming and algorithms

Python fluency, clean functions, array/data operations, tests, complexity and edge cases. Broaden the bank to hashing, sorting, binary search, two pointers, heaps, graph traversal and dynamic programming. Topic membership alone is not mastery: ask why an approach is correct and when its cost becomes unacceptable.

Keep automatic delimiters and syntax highlighting, but honour the user's request for no suggestions or AI coaching. During a timed attempt, hints and editorials should remain an explicit learner choice and should not be confused with independent success.

### Communication and judgement

State the unknowns, ask a useful clarifying question, narrate key decisions, accept a hint and revise, and distinguish a derived conclusion from a guess. Include short spoken explanations and project defence prompts. These can work as static structured exercises; a live AI interviewer is unnecessary.

## 7. Researcher branch: the principal expansion

1. **Statistical inference:** likelihood and maximum likelihood; bias, consistency and efficiency at an appropriate level; confidence intervals; hypothesis tests; likelihood ratios; bootstrap and permutation methods; Bayesian estimation; how dependence changes uncertainty. Connect each method to assumptions and failure modes.
2. **Statistical learning:** regression in depth; regularisation; logistic regression; bias/variance; trees and ensembles; objective functions; gradient-based fitting; feature selection; calibration; imbalanced outcomes; interpretation of metrics. Include neural networks only when their concepts and use justify them, not because “quant ML” sounds advanced.
3. **Optimisation and numerical reasoning:** derive a gradient, explain convexity, compare closed-form and iterative methods, diagnose conditioning, and distinguish numerical failure from an invalid statistical model.
4. **Time series and research design:** stationarity, autocorrelation, forecasting baselines, temporal dependence, availability timestamps, validation under deployment, selection bias and multiple testing. The current curriculum already has meaningful material here; expand it through research cases rather than replacing it with generic ML tutorials.
5. **Open-ended work:** inspect data, define the target, choose a baseline, design an experiment, quantify uncertainty and explain what a result does not establish. Include at least one case where the right conclusion is that the evidence is insufficient.
6. **Research defence:** explain a real project in five minutes, then answer questions about the weakest assumption, alternative explanations, failed experiments, reproducibility and next steps. A negative result can demonstrate excellent research judgement.

Advanced stochastic calculus, derivatives PDEs and specialised optimisation can form optional extensions when a target role warrants them. The reviewed interview evidence does not establish them as the universal starting point for this user's researcher preparation.

## 8. Trader branch: a different expansion

Prioritise arithmetic fluency, fractions, percentages, approximation and estimation; probability under changing information; fair value and spreads; adverse selection and inventory; risk/reward and decision thresholds; strategic interactions; and basic market mechanisms.

Timed drills should distinguish speed from accuracy and track both. Trading scenarios should reward a justified decision, not reckless speed or a single lucky outcome. A changing quote can teach Bayesian updating; an inventory constraint can teach why positive expected value is not sufficient to accept unlimited exposure.

The user is right that a broad conventional finance course should not crowd out mathematics and coding. However, mathematical and practical market concepts still help explain the problems. Teach only the finance needed for the current argument, then offer further depth where relevant.

## 9. Local curriculum audit

The catalogue files inspected were `static/content.json` and `static/coding.json`; authored lesson modules and source banks were also searched. This was a content inventory, not an independent mathematical review of every solution.

| Inventory on 12 October 2026 | Count |
| --- | ---: |
| Lessons | 24 |
| Interview questions | 48 |
| Question labels | 7 Easy / 22 Medium / 19 Hard |
| Python exercises | 14 |
| Coding labels | 2 Easy / 11 Medium / 1 Hard |
| Research route | 18 lesson checks / 39 problems / 14 coding exercises |

Counts and difficulty labels are internal. Nineteen questions labelled Hard do not establish an employer-equivalent standard.

**Existing strengths:** sample spaces and probability; recurrences; variance/dependence; estimation; covariance and regression geometry; temporal availability; validation and multiple testing; Monte Carlo; market making, adverse selection and research defence. The current coding bank includes Welford statistics, lagged calculations, availability joins, OLS, sample autocorrelation, purged/walk-forward validation, cost-aware P&L, control variates and a sliding-window maximum. These are useful foundations.

**Gaps to address:** there is no visible dedicated course/exercise sequence for likelihood-based inference, resampling, regularised/logistic learning, broader supervised ML or gradient-based optimisation. The algorithm bank is too narrow to provide broad interview practice. Topic searches alone cannot prove the absence of every incidental mention; this judgement refers to dedicated teaching and assessed practice.

Many lesson checks are a single conceptual multiple-choice question. They can check recognition, but they cannot establish derivation skill, transfer to unfamiliar settings or performance through an interview's follow-ups. Written problem completion is self-assessed, which is useful when honestly labelled but cannot be treated as independent verification.

| Area | Current anchor | Next meaningful improvement |
| --- | --- | --- |
| Probability | l01–l05, l07 | Unseen multi-stage problems, changed assumptions, counterexamples |
| Estimation/inference | l09, l12 | Likelihood derivations, intervals, tests, Bayesian/resampling comparisons |
| Linear algebra/regression | l10–l11 | Rank/conditioning, regularisation, optimisation, model diagnostics |
| Temporal research | l08, l13–l15 | Messy datasets, uncertainty under dependence, selection-aware cases |
| Research defence | l16 | Substantive project brief, adversarial follow-ups, evidence rubric |
| Simulation | l17 | Error estimates, estimator comparisons, diagnostic experiments |
| Algorithms | l18 and coding bank | Binary search, heaps, graph traversal, dynamic programming and variety |
| Trading judgement | l19–l24 | Multi-step information, inventory and risk decisions |
| ML | Scattered connections | Coherent research branch with theory, implementation and evaluation |

## 10. Illustrative target exercises

These are **original curriculum sketches**, not actual questions attributed to any firm. They illustrate the depth we should build toward. Some deliberately need a choice of model; that choice must be made explicit before calculation.

### A. A hidden coin and a decision

A coin is selected uniformly from two coins with head probabilities 0.3 and 0.7. You observe three heads in four independent tosses of the selected coin. Find the probability of a head next. An offer pays £1 for a head and costs £0.60 to enter: should a risk-neutral person accept it? Then change the selection probability. Finally suppose the observations were disclosed only after a favourable result: what additional information is needed?

The progression tests a correctly specified likelihood, posterior weighting, prediction, expected value and awareness of selection. Its difficulty comes from connecting ideas and spotting when information is insufficient.

### B. An apparently convincing signal

You inspect 200 candidate features and retain the best-looking one. Its next-period return prediction has a small positive average on highly autocorrelated observations. Design an evaluation without using the selected feature's test data for further tuning. What uncertainty estimate would you use, what baseline would you compare against, and what changes if features were chosen after inspecting the whole dataset?

The learner must distinguish statistical evidence, model selection and deployment assumptions. There need not be a unique correct test; the justification and limitations are part of the answer.

### C. Regression when the columns are almost the same

Two predictors are nearly collinear. Explain what happens to least-squares coefficients, whether predictions must also become poor, and how a penalty changes the fit. Derive the ridge solution with an explicitly unpenalised intercept. Compare solving a linear system with forming a matrix inverse. Choose a validation method for temporally dependent data.

This integrates geometry, statistics, numerical implementation and evaluation. A diagram can clarify the nearly aligned directions; a small numerical experiment is useful if it reveals instability. Neither is mandatory decoration.

### D. A streaming implementation

Maintain the maximum over the latest k observations in a stream. Start with a correct straightforward implementation, then improve its cost. Explain the invariant and amortised complexity, handle repeated values and define behaviour when fewer than k observations exist. Extend to asynchronous timestamps with an explicit ordering policy.

The site already has a related sliding-window task. Its deeper follow-ups can teach correctness and constraints, but additional algorithm families are still needed.

### E. An informed counterparty

An asset pays either £0 or £100. Specify a prior and a model for whether the arriving counterparty has information. Determine how a buy request changes your valuation before setting a quote. Then add a current position and a risk constraint. Explain how an uninformed-flow assumption changes the answer.

The problem needs a defined information model before there is a numerical solution. The lesson should show how the model changes the price and why inventory affects the decision.

### F. A small research assignment

Provide timestamped features, publication times, missing values, labels and costs. Ask for a reproducible baseline and a one-page conclusion. The learner must explain which rows were available at each decision, how the split was chosen, which alternatives were tried and what remains uncertain. Include a plausible leakage trap and a case where the result disappears after costs.

Assess the method, code, diagnostic evidence and conclusion separately. An attractive chart or positive sample return is not sufficient evidence of a robust result.

## 11. Recommended order of work

This is a proposal, not an implemented expansion.

**First: strengthen assessment depth.** Preserve the approved lessons, but give important modules multiple unseen checks: derivation, explanation, a changed assumption and implementation where useful. Add independent reattempts and delayed review. No navigation, example run or development fixture should earn personal progress.

**Second: build the missing research core.** Add inference, resampling, regularisation/logistic learning and optimisation in a dependency order. Continue into broader ML after the necessary mathematics. A small set of well-authored modules is better than hurried nominal coverage of dozens of methods.

**Third: broaden coding systematically.** Organise exercises by the skill being assessed and vary the surface story. Include efficient algorithm problems and practical data tasks. Keep correctness, complexity and numerical issues distinct.

**Fourth: add research cases and interview practice.** Use fixed briefs, follow-up prompts and explicit rubrics. Include both timed technical sessions and untimed investigation. The platform does not need AI coaching to support this.

**Fifth: deepen the trader branch.** Develop probability-driven games and market decisions with purposeful feedback. Speed games should supplement the branch, not replace judgement.

Do not retag the whole platform by employer. The user requested portable skills rather than “which firm asked this.” Firm research should inform the standard behind the curriculum; the learning interface can remain organised by concepts and researcher/trader goals.

## 12. Difficulty and readiness should mean something

Use an internal rubric that separates:

- **Prerequisite depth:** how much subject knowledge is needed.
- **Discovery:** whether the method is given or must be found.
- **Reasoning length:** how many linked arguments must remain correct.
- **Transfer:** whether assumptions or constraints change.
- **Implementation:** correctness, efficiency and numerical demands.
- **Ambiguity:** how much the learner must clarify and justify.

Easy should reinforce one well-defined skill. Medium should require method selection and a connected argument. Hard should involve substantial discovery, proof, integration or constraints—not obscure wording or omitted assumptions. Display a useful explanation of difficulty rather than an unsupported claim of matching a named firm's exam.

Readiness should be evaluated with unseen tasks and honest evidence: can the learner solve, explain, implement, revisit after a delay and defend the limitations? Track assisted attempts separately. A course check, self-assessed answer, full coding pass and oral explanation represent different evidence and should retain their own labels.

Because this user's stated probability knowledge needs refreshing and Python experience is currently Easy/Medium, begin with a diagnostic and a sensible ramp. Research ambition should determine the destination, not force an immediate jump to specialist material. Finishing a large bank is less informative than reliably handling new problems.

## 13. Teaching and interface constraints for future implementation

Read the project's [Lesson Authoring Guide](../LESSON_AUTHORING_GUIDE.md) and [course status](../COURSE_REDESIGN_STATUS.md) before rewriting pages.

The approved direction is a continuous illustrated textbook with topic-specific pedagogy. A representation belongs because it explains the argument: a geometric figure for projection, linked colour for conditional events, a small experiment for variance, code for an algorithm or empirical phenomenon. Do not impose identical diagram/code/quiz sections on every lesson.

Introduce notation and assumptions before use. Use semantic colour consistently between prose, mathematics and figures. Interactions should reveal a mathematical relationship and animate smoothly, with reduced-motion support. Preserve the site's light editorial identity, compact integrated controls and roadmap continuity.

No AI coaching, no decorative filler, no unnecessary articles, no fabricated firm question provenance and no synthetic personal progress. Existing identifiers and progress provenance must be preserved when content expands.

## 14. Evidence limits and refresh points

No employer supplied a complete exhaustive syllabus or an objective employer-to-employer difficulty scale. Public guides describe selected processes and expectations; hiring teams can change them.

The Optiver Sydney answers were directly verified in browser accordions. Other offices need their own process confirmation. SIG's official London text was available through search indexing but the direct page was inaccessible. Jump's current graduate stages remain unconfirmed in this review. G-Research's current web summary and linked PDF use different process detail; retain that difference and confirm the route when applying.

Official mock interview videos were located, but their presence must not be confused with having watched and analysed their full contents. This report does not claim such an analysis.

Refresh office, role, assessment format, permitted tools/languages and round expectations when selecting a concrete application. Do not spend study time optimising around an unverified internet pass score.

**Decision supported now:** keep Quant Atelier as the personal foundation and expand its researcher preparation deliberately. The present course count, coding count and self-assessed problem bank should not be presented as comprehensive preparation for these firms.
