"""Editorial review of retained assessments; IDs and checked answers stay fixed."""


def review_original_questions(questions):
    by_id = {q['id']: q for q in questions}
    rubrics = {
        'q01': ['Count the twenty-five no-six ordered outcomes and obtain 11/36.',
                'Identify the double-six outcome counted twice by addition.',
                'Use the independent n-dice complement and strict threshold to obtain thirteen.'],
        'q02': ['List all five ordered sum-eight outcomes and justify equal conditional weights.',
                'Obtain double probability one fifth without counting unordered records uniformly.',
                'Use symmetry and the fixed sum to obtain conditional mean four.'],
        'q03': ['Weight each coin’s head likelihood by its equal prior probability.',
                'Normalise the joint masses one half and one quarter to obtain two thirds.',
                'Derive the repeated-head posterior under a fixed coin and conditional independent flips.'],
        'q05': ['Count uniform physical pairs, with twenty-four mixed pairs out of forty-five.',
                'Obtain 8/15 or the equivalent two ordered colour paths.',
                'Derive the general formula with at least two balls and distinguish replacement.'],
        'q06': ['Use nineteen overlapping-pair indicators, each with mean one quarter.',
                'Obtain 19/4 without assuming indicator independence.',
                'Include adjacent covariance twice in the variance sum and handle short sequences.'],
        'q07': ['Derive the maximum CDF from two independent die crossings.',
                'Difference the CDF and sum to obtain 161/36.',
                'Use the pointwise maximum-plus-minimum identity to obtain 91/36.'],
        'q08': ['Derive minimum survival (1−x)³ on the stated unit support.',
                'Integrate survival to obtain one quarter.',
                'Derive the maximum CDF, including its support boundaries, and mean three quarters.'],
        'q09': ['Describe the four discovery stages and their success probabilities.',
                'Count the successful draw in each geometric wait and obtain 25/3.',
                'Derive the harmonic-sum generalisation without replacing unequal probabilities by their average.'],
        'q10': ['Define empty and trailing-head states and both first-step recurrences.',
                'Explain the head self-loop and derive expectation four.',
                'Change the reset transition for HH and obtain expectation six.'],
        'q11': ['Define trailing-head states and terminal expectation zero.',
                'Derive expectation fourteen from first-step equations, including every final flip.',
                'Derive the k-head formula and its p=0/p=1 boundaries without treating overlapping windows as trials.'],
        'q12': ['Specify absorbing boundaries and the expected-time difference equation.',
                'Justify finite expected exit time and derive i(12−i), giving thirty-five.',
                'Solve the distinct harmonic hitting-probability equation to obtain five twelfths.'],
        'q14': ['Order the two independent uniform cut locations and retain the correct density.',
                'Translate strict triangle inequalities into a region of area one eighth and probability one quarter.',
                'Derive the explicitly different sequential-cut probability log(2)−1/2 and explain its weighting.'],
        'q15': ['Apply memorylessness to the remaining time, whose mean is two minutes.',
                'Add the three elapsed minutes to obtain total expectation five.',
                'Use a four-minute conditional survival interval to obtain exp(−2).'],
        'q16': ['Integrate the rate-three density times the independent rate-two survival.',
                'Obtain winning probability three fifths and first-ring rate five.',
                'Factor the joint winner/time density and identify constant rates as an essential assumption.'],
        'q17': ['Include all ordered off-diagonal covariances in the mean variance.',
                'Obtain 0.109 and explain why independent averaging would give a different result.',
                'Take the fixed-correlation limit and derive feasible equicorrelation bounds.'],
        'q23': ['Derive the maximum distribution and its expectation under iid uniform sampling.',
                'Use the factor five fourths to obtain estimate ten.',
                'Compare squared-error risks rather than assuming unbiasedness alone is decisive.'],
        'q45': ['Square the scale factor and remove the translation from variance.',
                'Obtain variance thirty-six and distinguish the standard-deviation change.',
                'Use positive variance to derive correlation minus one after negative scaling.'],
        'q46': ['Use a common Bernoulli parameter and its stated Beta prior.',
                'Derive posterior Beta(5,3) and mean five eighths.',
                'Integrate the next success probability over the posterior rather than replacing it by the empirical rate.']
    }
    for id, rubric in rubrics.items():
        by_id[id]['rubric'] = rubric

    # These clarify assumptions already required by the retained checked answers.
    by_id['q02']['prompt'] = by_id['q02']['prompt'].replace('Two fair dice', 'Two independent fair dice')
    by_id['q06']['prompt'] = by_id['q06']['prompt'].replace('Flip a fair coin 20 times', 'Make 20 independent flips of a fair coin')
    by_id['q10']['prompt'] = by_id['q10']['prompt'].replace('Flip a fair coin until', 'Make independent flips of a fair coin until')
    by_id['q11']['prompt'] = by_id['q11']['prompt'].replace('Flip a fair coin until', 'Make independent flips of a fair coin until')
    by_id['q46']['prompt'] = by_id['q46']['prompt'].replace('Observe 3 successes and 1 failure.', 'Conditional on a common fixed p, observe four independent trials with 3 successes and 1 failure.')
    by_id['q45']['title'] = 'Scaling squares; translation disappears'
    by_id['q19']['prompt'] = by_id['q19']['prompt'].replace(
        'mutually independent, centred,', 'mutually independent, centred, with finite second moments,')
    by_id['q37']['prompt'] = 'A repeated independent bet wins even money with probability 0.6. Before each round you stake a fixed fraction 0≤f<1 of current positive wealth. A win multiplies wealth by 1+f and a loss by 1−f; there are no fees or other outcomes. What f maximises expected natural-log wealth growth? Derive and justify the global optimum under this stated toy objective.'

    by_id['q18']['solution'] = r'''For the usual stationary AR(1) covariance structure, \(\gamma_h=\gamma_0\rho^h\). Expanding all covariance pairs in the sample mean gives

\[\operatorname{Var}(\bar X_n)=\frac{\gamma_0}{n}\left[1+2\sum_{h=1}^{n-1}(1-h/n)\rho^h\right].\]

At fixed |ρ|<1 and growing n, the bracket tends to the convergent geometric-sum factor \(1+2\rho/(1-\rho)=(1+\rho)/(1-\rho)\). Matching this asymptotic variance to γ₀/n_eff gives

\[n_{eff}\approx\frac{n(1-\rho)}{1+\rho}.\]

For n=100 and ρ=0.8 this is 100/9≈11.11. This is the requested fixed-correlation large-sample approximation for the MEAN, not the exact finite-window value or an independent-sample representation for every statistic. Keeping the lag taper answers the separate finite-n follow-up.'''

    by_id['q20']['solution'] = r'''Write a=Corr(X,Y), b=Corr(Y,Z), c=Corr(X,Z). Standardisation gives unit variances. Remove the shared Y projection: residuals X−aY and Z−bY have variances 1−a² and 1−b² and covariance c−ab. Cauchy–Schwarz therefore requires

\[(c-ab)^2\leq(1-a^2)(1-b^2).\]

Here a=b=0.8, so the residual standard deviations are both 0.6 and c must lie in [0.64−0.36,0.64+0.36]=[0.28,1]. The smallest feasible value is 0.28. It is ATTAINED by giving the two residuals opposite signs of the same standardised random variable independent of Y, as constructed in the follow-up. Thus this is a sharp bound, not just a necessary pairwise condition. At the lower endpoint the joint covariance is singular.'''

    by_id['q37']['solution'] = r'''For fixed initial positive wealth W, its log contributes a constant. The one-round expected log multiplier is

\[g(f)=0.6\log(1+f)+0.4\log(1-f).\]

The derivative is \(0.6/(1+f)-0.4/(1-f)\), which vanishes at f=0.2. Its second derivative is

\[g''(f)=-\frac{0.6}{(1+f)^2}-\frac{0.4}{(1-f)^2}<0.\]

Strict concavity proves the unique global maximum on 0≤f<1; g(0)=0 and g(f) tends to minus infinity as f approaches one. Expected total log growth over a fixed number of independent rounds is that round count times g(f), so the same fraction optimises the declared repeated objective. The optimum is conditional on this specified probability, payoff and loss model.'''

    by_id['q37']['followSolution'] = r'''First specify what uncertainty means and which objective judges the decision. For ONE round, if p itself has a prior distribution and the objective averages expected log utility over that prior, linearity gives \(E[p]\log(1+f)+(1-E[p])\log(1-f)\). When E[p]<1, the nonnegative optimum is max(0,2E[p]−1); uncertainty alone does not force a smaller fraction than the same mean would give. If E[p]=1, growth increases up to the excluded boundary f=1, so there is only a supremum on the stated domain. For an ambiguity SET p∈[p_low,p_high] and a worst-case objective, every fixed positive f has growth increasing in p, so the least-favourable probability is p_low and the optimum is max(0,2p_low−1), assuming the interval lies strictly below one. Those two interpretations can produce different answers. Estimation error, dynamic learning, constraints and additional loss outcomes need their own model; merely saying “uncertainty” does not establish a universal fractional rule. The linked Hard practice develops these distinctions.'''

    by_id['q03']['followSolution'] = r'''Keep the SAME chosen coin for all k flips, conditionally independent given its identity. The always-heads branch has joint mass one half; the fair branch has mass \((1/2)2^{-k}\). Normalising gives

\[P(\mathrm{always\ heads}\mid k\ \mathrm{heads})=\frac{1}{1+2^{-k}}.\]

At k=0 this recovers the equal prior; as k grows it tends to one without reaching certainty at any finite k. A tail rules out the always-heads coin under this exact model. Choosing a fresh coin before EACH flip would define a different inference problem.'''

    by_id['q05']['followSolution'] = r'''Assume r,b are nonnegative integer counts and r+b≥2, with uniform physical sampling without replacement. Ordered mixed paths have probabilities \(r/(r+b)\) times \(b/(r+b-1)\), and the reverse product with r and b exchanged. Their sum is

\[\frac{2rb}{(r+b)(r+b-1)}.\]

It is zero if either colour is absent. Independent draws WITH replacement instead give \(2rb/(r+b)^2\). The record count and its denominator must follow the sampling procedure.'''

    by_id['q08']['followSolution'] = r'''For the maximum M, all three independent draws must be at most x. Thus its CDF is zero for x<0, \(x^3\) for 0≤x≤1 and one for x>1. The nonnegative tail identity gives

\[E[M]=\int_0^1(1-x^3)\,dx=\frac34.\]

The minimum CDF is \(1-(1-x)^3\) on the same support, not x³. Reflecting each uniform draw around one also maps the maximum to one minus the minimum, checking that the two expectations sum to one.'''

    by_id['q11']['followSolution'] = r'''Let k≥1 and let E_j be the expected additional flips from j trailing heads, with E_k=0. With independent flips of head probability 0<p<1, every nonterminal state satisfies

\[E_j=1+pE_{j+1}+(1-p)E_0.\]

Unroll from j=0 through the k states:

\[E_0=\left(\sum_{j=0}^{k-1}p^j\right)[1+(1-p)E_0].\]

Since \((1-p)\sum_{j=0}^{k-1}p^j=1-p^k\), moving the E₀ term to the left yields

\[E_0=\frac{1-p^k}{(1-p)p^k}.\]

The mean is finite: every independent disjoint block of k flips has probability p^k of being all heads, so the true stopping time is bounded above by k times a geometric block count. This validates the expectation equations; overlapping windows themselves are not independent trials. At p=1 the wait is exactly k, matching the continuous limit. At p=0 the target never occurs and the expected wait is infinite.'''

    by_id['q12']['solution'] = r'''Write t_i for expected additional steps from integer i. The boundaries are absorbing, so t₀=t₁₂=0. For an interior state, one step is taken before the remaining wait:

\[t_i=1+\tfrac12t_{i-1}+\tfrac12t_{i+1}.\]

Finite expectation is justified independently. From any interior state, twelve consecutive downward moves would hit zero within twelve steps and have probability at least 2⁻¹². Conditional on any surviving history, a new twelve-step block has at least this exit chance. Hence the block survival tail is bounded by a geometric tail, giving finite expected exit time.

Rearrange the recurrence to \(t_{i+1}-2t_i+t_{i-1}=-2\). Its general quadratic solution is \(t_i=-i^2+ai+b\); the two boundaries force b=0 and a=12. Therefore \(t_i=i(12-i)\) and t₅=35. Uniqueness follows because the difference of two solutions has zero second difference and zero boundary values, so is the zero affine function. A distance-to-nearest-boundary shortcut misses the repeated backtracking.'''

    by_id['q12']['followSolution'] = r'''Let p_i be the probability of hitting twelve before zero. First-step conditioning now gives \(p_i=(p_{i-1}+p_{i+1})/2\), with p₀=0 and p₁₂=1. There is NO added one-step time cost in this probability equation. Zero second difference makes p_i affine; the boundaries give p_i=i/12. Starting at five gives 5/12. This is the chance of one exit side, not the expected elapsed time.'''

    by_id['q14']['solution'] = r'''Write U for the smaller cut location and V for the larger. Ordering two independent uniform cuts gives density TWO on the triangle 0<U<V<1: each ordered pair comes from two equally dense original orders, except a zero-probability diagonal. The piece lengths are U, V−U and 1−V. With total length one, the strict triangle inequalities are equivalent to every piece being less than one half. Thus

\[U<\tfrac12,\quad V>\tfrac12,\quad V<U+\tfrac12.\]

For a fixed U in (0,1/2), valid V runs from 1/2 to U+1/2, an interval of length U. The valid region’s area is

\[\int_0^{1/2}U\,dU=\frac18.\]

Multiply by ordered density two, or divide by total ordered-region area one half, to obtain probability one quarter. Strict equality boundaries have probability zero under this continuous procedure. Counting three possible piece positions uniformly would not define their joint length distribution.'''

    by_id['q14']['followup'] = 'Instead, make one uniform cut on the unit stick; choose one of the resulting TWO pieces with equal probability, independently of its length; cut that chosen piece at a uniform location within it. Is the triangle probability still one quarter? Derive it for this explicitly stated procedure.'
    by_id['q14']['followSolution'] = r'''Let the first left-piece length be u, uniform on (0,1). If u>1/2, only choosing the left (longer) piece can succeed, because leaving it uncut violates the triangle condition. That choice has probability one half. Given it, the new cut coordinate z must satisfy u−1/2<z<1/2 inside (0,u). Its success probability is (1−u)/u. If u<1/2, choosing the right piece instead gives the symmetric condition and probability u/(1−u). Therefore

\[\begin{aligned}P(\mathrm{triangle})&=2\cdot\frac12\int_{1/2}^1\frac{1-u}{u}\,du\\&=\log 2-\frac12\\&\approx0.193147.\end{aligned}\]

The equal choice between pieces is NOT equal choice between physical locations on the whole stick: a shorter piece concentrates the conditional cut density more strongly. The new cuts therefore are not two independent uniform locations. This comparison changes the sampling measure, not the strict geometric triangle criterion.'''

    by_id['q17']['followSolution'] = r'''For fixed nonnegative equicorrelation ρ, the mean variance is \(\rho+(1-\rho)/n\), tending to ρ. At ρ=0.1 it therefore tends to 0.1, not zero. A representation \(X_i=\mu_i+\sqrt{\rho}Z+\sqrt{1-\rho}\,\varepsilon_i\), using mutually independent unit-variance centered variables, shows the common shock that averaging retains.

For a fixed dimension n≥2, the unit-variance equicorrelation matrix has eigenvalue 1+(n−1)ρ on the all-ones direction and 1−ρ on directions perpendicular to it. Nonnegative variance in every direction requires

\[-\frac{1}{n-1}\leq\rho\leq1.\]

A fixed negative ρ cannot satisfy this condition for arbitrarily large n. The limit with fixed ρ is meaningful only along feasible covariance models; the positive common-factor representation above does not apply to negative ρ.'''

    by_id['q23']['followSolution'] = r'''Unbiasedness describes mean error, not squared-error risk. In the declared iid uniform model, write M for the sample maximum; its second moment is \(E[M^2]=n\theta^2/(n+2)\). For estimates cM, completing the quadratic squared-error risk gives the minimum at c=(n+2)/(n+1), with risk θ²/(n+1)². The unbiased choice c=(n+1)/n has risk θ²/[n(n+2)], which is larger. At n=4 those risks are θ²/25 and θ²/24; the corresponding estimates at M=8 are 9.6 and ten. This compares a specified estimator family under squared loss, not every possible loss or sampling model. The numeric question still asks the UNBIASED estimate ten.'''
