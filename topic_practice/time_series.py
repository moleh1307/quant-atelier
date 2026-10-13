"""Time-series practice: the estimator, initialization and information set matter."""


def add_questions(add, questions):
    rubrics = {
        'q18': ['Derive the covariance-pair count and the fixed-rho asymptotic variance factor.',
                'Report 100/9 for the requested asymptotic mean-estimation comparison.',
                'Give the finite-sample taper and explain its limits near a unit root.'],
        'q31': ['Define the summed excess-return object, its mean and all covariance terms.',
                'Derive square-root scaling under vanishing nonzero-lag covariances and explain the dependent denominator.',
                'Distinguish summing from compounding and investigate smoothing, marks and costs before interpreting Sharpe.'],
    }
    for q in questions:
        if q['id'] in rubrics:
            q['rubric'] = rubrics[q['id']]

    def question(suffix, title, level, minutes, prompt, answer, hints, solution, follow, follow_solution, rubric):
        add(f'q_l13_{suffix}', title, 'Time series', level, 'researcher', minutes,
            prompt, answer, hints, solution, follow, follow_solution, 'l13')
        questions[-1]['rubric'] = rubric
        for key in ('prompt', 'solution', 'followSolution'):
            questions[-1][key] = questions[-1][key].replace(r'\n\n', '\n\n')

    question('e1', 'Three observations, counted covariance pairs', 'Easy', 7,
        r'A stationary AR(1) process has constant mean µ, marginal variance 4 and autoregressive coefficient ρ=1/2. Innovations are iid, centered, independent of the past and have variance 3, so these marginal assumptions are consistent. You observe THREE consecutive values and estimate µ by their arithmetic mean. What is the EXACT variance of this estimate? Count pairs at each separation; do not use a large-sample effective-size formula.', 22/9,
        ['Lag-one covariance is 2; lag-two covariance is 1.', 'There are two unordered lag-one pairs and one lag-two pair. Each appears twice in the variance of the sum.'],
        r'The sum variance is 3·4+2(2·2+1·1)=22. Dividing by 3² gives 22/9. The iid shortcut gives 4/3 and misses the covariance pairs. The exact variance factor is (22/9)/(4/3)=11/6; its standard-error factor is √(11/6), not 11/6. Equating mean-estimation variance to 4/n_eff gives n_eff=18/11. The asymptotic AR factor three would instead give n_eff=1; that is not the requested finite calculation.',
        r'Change ONLY ρ to −1/2, retaining stationary marginal variance 4 and innovation variance 3. What changes? Can this target-specific effective count exceed three?',
        r'Lag-one covariance becomes −2 while lag-two remains +1. Sum variance is 12+2(−4+1)=6, hence mean variance 2/3. The effective count is 4/(2/3)=6, exceeding three because adjacent noise partly cancels. This is a variance comparison for the mean, not six observed independent rows. Negative lag-one correlation does not make every later covariance negative.',
        ['Count both separations and both covariance orientations.', 'Obtain exact mean variance 22/9 and distinguish variance from standard-error inflation.', 'Keep the positive lag-two term under negative rho and interpret effective count six.'])

    question('e2', 'Forecast error accumulates future innovations', 'Easy', 7,
        r'A stationary process satisfies Xₜ−2=(1/2)(Xₜ₋₁−2)+εₜ. Its iid innovations have mean zero and variance 3 and are independent of the past. All parameters are known, and Xₜ=10 is observed exactly. Forecast Xₜ₊₂ using the information through t. What is the conditional mean-squared error of the optimal conditional-mean forecast? Do not confuse it with variance of a sample mean or impose Gaussian innovations.', 15/4,
        ['Iterate the recurrence twice before separating known and unknown terms.', 'Future innovations are independent, so add their weighted variances.'],
        r'Two steps give Xₜ₊₂=2+(1/4)(Xₜ−2)+(1/2)εₜ₊₁+εₜ₊₂. The conditional mean is 4 and the forecast error is (1/2)εₜ₊₁+εₜ₊₂. Its conditional variance and mean-squared error are 3(1/4+1)=15/4. A zero-mean independent innovation assumption justifies this conditional mean without normality. The stationary marginal variance is 3/(1−1/4)=4, slightly larger than this finite-horizon uncertainty.',
        r'Derive the h-step forecast and error variance for h≥1. Are the one-step and two-step forecast errors independent? Can this variance alone justify an exact Gaussian prediction interval?',
        r'The forecast is 2+(1/2)^h(Xₜ−2), and its error variance is \(3\sum_{j=0}^{h-1}(1/4)^j=4(1-4^{-h})\), approaching four. The one-step error εₜ₊₁ and two-step error share that innovation; their covariance is 3/2, so they are not independent. Finite variance alone does not specify their distribution or justify exact normal quantiles. A Gaussian innovation assumption would make these weighted errors jointly Gaussian.',
        ['Iterate the model and identify forecast four and the future-innovation error.', 'Add independent weighted innovation variances to obtain 15/4.', 'Derive horizon dependence, shared-error covariance and the distributional limit of a variance-only statement.'])

    question('m1', 'White returns can hide dependent risk', 'Medium', 18,
        r'Let εₜ be iid standard Gaussian over all integer times and Xₜ=εₜεₜ₋₁. You may use E[ε²]=1 and E[ε⁴]=3. Show that X has mean zero, variance one and ZERO autocovariance at every nonzero lag, yet adjacent X values are dependent. Define \(Y_t=X_t^2\), then derive the EXACT variance of \(\bar Y_n=n^{-1}\sum_{t=1}^nY_t\) for n≥1. Is the iid shortcut for that risk estimator valid?', None,
        ['The lag-one product contains two independent factors with mean zero.', 'For dependence, compare E[Xₜ²Xₜ₊₁²] with E[Xₜ²]E[Xₜ₊₁²].', 'Squared values have variance eight; only adjacent squared values share an innovation.'],
        r'E[Xₜ]=0 and E[Xₜ²]=1. At lag one, E[εₜ₋₁εₜ²εₜ₊₁]=0; at larger lags the innovation sets are disjoint, so covariance is again zero. But E[Xₜ²Xₜ₊₁²]=1·3·1=3, whereas the product of the second moments is one. This proves dependence. For Yₜ=Xₜ², E[Y]=1, E[Y²]=3²=9 and Var(Y)=8. Its lag-one covariance is 3−1=2; further lags vanish by independence. Therefore\n\n\[\operatorname{Var}(\bar Y_n)=\frac{8n+4(n-1)}{n^2}=\frac{12n-4}{n^2}.\]\n\nThe iid risk shortcut 8/n understates uncertainty for n>1 even though ordinary X autocorrelations vanish. Second-order whiteness of returns does not imply independence or second-order whiteness of a nonlinear target.',
        r'Compare exact mean-estimation effective counts for X and Y using EACH target’s own marginal variance. Does an iid-looking variance for the X mean imply iid data?',
        r'The X mean has variance 1/n, so its variance-comparison effective count is exactly n. For Y, it is 8n²/(12n−4)=2n²/(3n−1), approaching 2n/3. The reference marginal variance changed from one to eight with the target. The X mean variance identity is exact, but it does not establish an iid sampling distribution, independence, or a Gaussian interval. Effective size belongs to the estimator and assumptions.',
        ['Compute vanishing return autocovariances without claiming independence.', 'Prove dependence through the shared fourth moment.', 'Derive squared-return marginal variance eight, lag-one covariance two and finite tapered mean variance.', 'Compare target-specific effective counts and avoid an iid-distribution claim.'])

    question('m2', 'Overlapping labels manufacture autocorrelation', 'Medium', 20,
        r'One-period returns rₜ are iid with mean µ and positive variance σ². Define k-period SUM labels \(Y_t=\sum_{j=0}^{k-1}r_{t+j}\) for a fixed positive integer k. Observe Y₁,…,Yₙ, with n≥k, and estimate the one-period mean by \(\hat\mu=(nk)^{-1}\sum_{t=1}^nY_t\). Derive the label autocovariances and EXACT variance of \(\hat\mu\). Explain why treating the n labels as independent fails even when the underlying returns are iid. These are sums, not compounded returns.', None,
        ['Covariance comes only from underlying returns shared by two labels.', 'At lag h<k, exactly k−h returns overlap.', 'Use the finite pair count n−h, then divide by (nk)².'],
        r'E[Y]=kµ and γ₀=kσ². For 1≤h<k, the shared returns give γ_h=(k−h)σ²; at h≥k the blocks are disjoint and independent. Thus\n\n\[\operatorname{Var}\!\left(\sum_{t=1}^nY_t\right)=\sigma^2\left[nk+2\sum_{h=1}^{k-1}(n-h)(k-h)\right]=\sigma^2\left[nk^2-\frac{k(k^2-1)}3\right].\]\n\nDividing by n²k² gives Var(\(\hat\mu\))=σ²[1/n−(k²−1)/(3n²k)]. The independent-label shortcut σ²/(nk) omits the reused observations. For fixed k and large n the actual variance is approximately σ²/n, about k times the shortcut. This persistence arises from label construction, not necessarily an economically predictable daily-return process. The n≥k condition matters for the displayed polynomial; shorter samples require truncating at min(n−1,k−1).',
        r'Use only labels starting at 1,1+k,1+2k,… within 1…n. What variance results? If all n+k−1 underlying returns are available, can their direct mean improve on the overlapping-label estimator?',
        r'There are m=1+floor((n−1)/k) disjoint labels. Their mean divided by k has variance σ²/(mk). The direct mean of all n+k−1 iid underlying returns has variance σ²/(n+k−1). The overlapping estimator instead gives each underlying return a weight proportional to its multiplicity: smaller near the endpoints, larger inside. All weights sum to one, so Cauchy–Schwarz gives \(\sum_i w_i^2\geq1/(n+k-1)\). Thus the direct equal-weight mean has no larger variance, with equality precisely when these multiplicities are uniform (including k=1). For n≥k>1 they are unequal. Overlapping labels create repeated use, not extra independent information.',
        ['Count shared underlying returns and derive the finite label autocovariances.', 'Retain the lag taper, the n≥k condition and the exact one-period-mean variance.', 'Distinguish construction-induced dependence from predictable daily returns.', 'Derive disjoint-label variance and justify the direct-mean comparison with weights.'])

    question('h1', 'The arithmetic mean need not be the best mean estimate', 'Hard', 30,
        r'Observe n≥2 consecutive values of a weakly stationary process with unknown constant mean µ and KNOWN covariance \(\Sigma_{ij}=\gamma_0\rho^{|i-j|}\), where γ₀>0 and −1<ρ<1. Among estimators \(\hat\mu=\sum_iw_iX_i\) with deterministic weights summing to one, derive the unique minimum-variance weights and variance. Give explicit endpoint and interior weights, rather than only citing a generalized least-squares formula. Justify the covariance inverse or verify the vector it needs. Gaussianity is NOT assumed.', None,
        ['Minimize wᵀΣw with the sum constraint, or separate any weights from a proposed optimum.', 'The inverse AR correlation matrix is tridiagonal: endpoint diagonals one, interior diagonals 1+ρ², off-diagonals −ρ, all divided by 1−ρ².', 'Apply this matrix to the all-ones vector and normalize its sum.'],
        r'Let \(R_{ij}=\rho^{|i-j|}\) and let B be the stated tridiagonal matrix before division by 1−ρ². Multiplying a row of B by column j of R cancels the geometric terms off the diagonal; its diagonal is 1−ρ². Hence R⁻¹=B/(1−ρ²). It is positive definite: \(x^\top Bx=(1-\rho^2)x_1^2+\sum_{i=2}^n(x_i-\rho x_{i-1})^2>0\) for x≠0. Its row sums divided by 1−ρ² are 1/(1+ρ) at both endpoints and (1−ρ)/(1+ρ) inside. Write D=n−(n−2)ρ=2+(n−2)(1−ρ). Then\n\n\[w_1=w_n=\frac1D,\qquad w_i=\frac{1-\rho}D\ (2\leq i\leq n-1),\qquad\operatorname{Var}(\hat\mu)=\frac{\gamma_0(1+\rho)}D.\]\n\nThe weights sum to one and are positive. For \(w^*=\Sigma^{-1}\mathbf1/(\mathbf1^\top\Sigma^{-1}\mathbf1)\), \(\Sigma w^*\) is a constant times 1. Any other unbiased weights w*+v have \(\mathbf1^\top v=0\); the cross term vanishes and their variance is \(\operatorname{Var}(\hat\mu_{w^*})+v^\top\Sigma v\), strictly larger unless v=0. This proves uniqueness among deterministic linear unbiased estimates without normality. For n=2 both weights are one half; for n>2 positive correlation gives endpoints more weight than interior observations.',
        r'Compare n=3, ρ=1/2, γ₀=4 with the arithmetic mean. Then someone estimates weights from the same sample and claims that weights summing to one still guarantee unbiasedness. Give an explicit counterexample under iid N(µ,1) data.',
        r'Here D=5/2; weights are (2/5,1/5,2/5) and variance is 12/5, below arithmetic variance 22/9. The gain concerns mean estimation with known covariance; it is not a universal sampling policy. For random same-sample weights, \(\sum_i w_i=1\) only gives \(\hat\mu=\mu+\sum_iw_i(X_i-\mu)\); the last term need not have mean zero. With three iid Gaussian observations, choose weights (1,0,0) if X₁≥X₃ and (0,0,1) otherwise. The estimate is max(X₁,X₃)= (X₁+X₃+|X₁−X₃|)/2 and has mean µ+1/√π, because X₁−X₃∼N(0,2). The sum constraint alone therefore does not preserve unbiasedness after data-dependent selection.',
        ['Establish positive definiteness and verify the needed inverse or precision-vector identity.', 'Derive explicit normalized endpoint/interior weights and their variance.', 'Prove optimality and uniqueness in the deterministic linear unbiased class.', 'Compare the finite example and demonstrate same-sample random-weight bias.'])

    question('h2', 'A limit that holds rho fixed can fail', 'Hard', 35,
        r'For EACH n, take a stationary Gaussian AR(1) sample of n observations with common mean µ, marginal variance γ₀>0 FIXED across n, and \(\rho_n=e^{-c/n}\) for fixed c>0. Its innovation variance is \(\gamma_0(1-\rho_n^2)\), and its initial distribution is stationary. Derive the limit of \(\operatorname{Var}(\bar X_n)/\gamma_0\) and of the exact mean-estimation effective count \(\gamma_0/\operatorname{Var}(\bar X_n)\). Compare with substituting \(\rho_n\) into the usual fixed-ρ asymptotic count n(1−ρ)/(1+ρ). Is \(\bar X_n\) a consistent estimator here? State which assumptions differ from a single fixed-ρ model.', None,
        [r'Start with \(n^{-2}\sum_{i=1}^n\sum_{j=1}^n e^{-c|i-j|/n}\), not an infinite-lag shortcut.', 'Treat the double sum as a Riemann integral on the unit square.', 'The integral equals 2∫₀¹(1−u)exp(−cu)du.'],
        r'The sample changes its persistence with n while retaining its marginal noise scale. The continuous kernel gives the Riemann-sum limit\n\n\[\begin{aligned}g(c)&=\int_0^1\!\int_0^1 e^{-c|s-t|}\,ds\,dt\\&=2\int_0^1(1-u)e^{-cu}\,du\\&=\frac{2(c-1+e^{-c})}{c^2}>0.\end{aligned}\]\n\nThus \(\operatorname{Var}(\bar X_n)\)→γ₀g(c) and n_eff→1/g(c), a finite number. In contrast, the substituted fixed-ρ formula tends to c/2 and is not valid uniformly in this changing model. At c=1 the exact limit is e/2≈1.359, whereas that shortcut is 1/2. As c→0, g(c)→1 and the true count tends to one; it does not tend to zero. Each centered sample mean is Gaussian, so its positive limiting variance implies nonvanishing probabilities of fixed estimation errors, not consistency. Variance alone would not establish this probability conclusion for arbitrary non-Gaussian triangular arrays; Gaussianity supplies it here. Absolute lag summability for each n does not supply a uniform fixed-model limit.',
        r'Keep \(\rho_n\) and innovation variance \(\gamma_0(1-\rho_n^2)\), but initialize X₀=µ deterministically instead of stationarily. Derive the changed covariance kernel and mean-variance limit. Separately, what if stationary initialization is retained but innovation variance τ²>0 is fixed across n?',
        r'For deterministic initialization, \(X_i-\mu=\sum_{j=1}^i\rho_n^{i-j}\epsilon_j\). Summing shared innovation covariances gives \(\gamma_0(\rho_n^{|i-j|}-\rho_n^{i+j})\); it is no longer weakly stationary. The mean-variance ratio tends to\n\n\[g(c)-\left(\frac{1-e^{-c}}c\right)^2.\]\n\nThis subtracts the random stationary initial component that the deterministic experiment removed. Its c→0 limit is zero, contrasting with g(c)→1; using the stationary formula for a zero-start simulation changes the experiment. This ratio is to the original stationary scale γ₀, not a common marginal variance in the nonstationary sample. If instead τ² is fixed with stationary initialization, the marginal variance \(\gamma_{0,n}=\tau^2/(1-\rho_n^2)\) grows like τ²n/(2c). Consequently \(\operatorname{Var}(\bar X_n)\) grows like \(\tau^2 n(c-1+e^{-c})/c^3\). Specify the initialization and which variance scale is fixed before interpreting persistence.',
        ['Derive the finite covariance Riemann sum and positive limiting function g(c).', 'Compare exact and incorrectly substituted effective counts, including c=1 and small-c behavior.', 'Use the Gaussian sampling law to justify nonconsistency, rather than a variance-only assertion.', 'Derive both changed initialization and fixed-innovation limits with their variance scales.'])


def add_coding(add, tasks):
    def exercise(level, title, prompt, signature, samples, tests, solution, explanation):
        add(f'c_l13_{level.lower()}', title, level, 'Time series', prompt, signature,
            samples, tests, solution, explanation)
        tasks[-1]['path'] = 'researcher'
        for key in ('prompt', 'explanation'):
            tasks[-1][key] = tasks[-1][key].replace(r'\n\n', '\n\n')

    exercise('Easy', 'Count the finite lag pairs exactly',
        r'For n consecutive observations with a constant mean, variance is a positive integer marginal variance, and lag_covariances[h−1] is their integer covariance at separation h. Unlisted covariances are zero; supplied lags h≥n have no pairs in this window and are ignored. The resulting n×n covariance matrix is GUARANTEED positive semidefinite; you do not need to test feasibility. Return the EXACT variance of the arithmetic sample mean as a reduced canonical decimal-string rational pair [numerator_text,denominator_text]. Zero is ["0","1"]. This is finite covariance-pair counting, not an asymptotic effective count.\n\n1≤n≤10^9, 1≤variance≤10^18, at most 100000 supplied lags, and each covariance has absolute value at most variance. Use O(min(n−1,len(lag_covariances))) scalar iterations and O(1) integer accumulators beyond the output; integer multiplication/gcd/bit costs are additional. Preserve the input list. Do not use float arithmetic or omit the n−h taper.',
        'def solve(n, variance, lag_covariances):',
        [{'args':[3,4,[2,1]],'expected':['22','9']}, {'args':[3,4,[-2,1]],'expected':['2','3']}],
        EASY_CASES,
        'from math import gcd\ndef solve(n, variance, lag_covariances):\n    numerator = n * variance\n    for h in range(1, min(n - 1, len(lag_covariances)) + 1):\n        numerator += 2 * (n - h) * lag_covariances[h - 1]\n    denominator = n * n\n    divisor = gcd(numerator, denominator)\n    return [str(numerator // divisor), str(denominator // divisor)]',
        r'Expanding the sum’s variance counts n marginal terms and, for each relevant lag h, n−h unordered pairs in both orientations. Therefore the mean variance is \([n\gamma_0+2\sum_{h=1}^{n-1}(n-h)\gamma_h]/n^2\). Ignore beyond-window lags before iterating. Reduce the integer numerator and denominator by their gcd; PSD guarantees a nonnegative numerator, including possible zero. Negative covariances can reduce mean uncertainty. A covariance estimate not guaranteed feasible could give a negative answer, but validation of such estimates is outside this contract.')

    exercise('Hard', 'Forecast noisy states without seeing future measurements',
        r'This task extends the lesson’s observed AR process to a LATENT Gaussian state measured with noise. X₀∼N(prior_mean,prior_variance), and for integer t≥1, Xₜ=ρXₜ₋₁+εₜ with ρ=rho_numerator/rho_denominator and iid εₜ∼N(0,innovation_variance). A supplied observation [time,value,noise_variance] means Y_time=X_time+η_time with independent η_time∼N(0,noise_variance). Initial state, innovations and all measurement errors are mutually independent. Missing observations mean no measurement, not a zero value. All parameters are KNOWN; no stationarity is required, and ρ=0 or ±1 is allowed.\n\nFor each request [asof,target] return {"mean":[signed_numerator_text,denominator_text],"variance":[nonnegative_numerator_text,denominator_text]} for X_target CONDITIONAL ONLY on supplied Y measurements at times ≤asof, including equality. target≥asof. Later measurements must be ignored even when they occur before target or at target. Predict the latent X, not a future noisy Y. Preserve request order and duplicates. Every pair must be exact, reduced canonical decimal strings with positive denominator; zero is ["0","1"].\n\nAll inputs are integers: 1≤rho_denominator≤20, |rho_numerator|≤rho_denominator; 0≤innovation_variance,prior_variance≤10^6, |prior_mean|≤10^6. Observations have distinct STRICTLY increasing times 1…120, |value|≤10^6 and 1≤noise_variance≤10^6. There are at most 10000 requests with 0≤asof≤target≤120. Lists may be empty. Use O(T+len(observations)+len(requests)) scalar rational operations and O(T+len(observations)) rational storage beyond outputs, where T is the largest supplied time or zero. Additional rational bit/gcd/string costs apply. Do not mutate inputs, use floats, refit a dense covariance system per request or assimilate future observations.\n\nPrerequisite: Gaussian conditioning. If the current predicted state has mean m and variance P, observing Y=x+noise with independent noise variance R uses gain K=P/(P+R), updated mean m+K(y−m), and variance PR/(P+R). P may be zero because R is strictly positive. Derive the prediction step and keep its information set explicit.',
        'def solve(rho_numerator, rho_denominator, innovation_variance, prior_mean, prior_variance, observations, requests):',
        HARD_SAMPLES, HARD_CASES,
        HARD_REFERENCE,
        r'Gaussian conditioning yields the given scalar update, because Cov(X,Y)=P and Var(Y)=P+R. If P=0, the gain is zero: a noisy observation cannot change a state already known exactly. Between observations, a prediction sends (m,P) to (ρm,ρ²P+Q), where Q is innovation_variance. Filter once through the finite timeline, applying only that time’s measurement AFTER its transition, and store the filtered distribution at every asof. This is filtering, not smoothing with all later measurements.\n\nFor h=target−asof, precompute A₀=1,G₀=0 and Aₕ₊₁=ρAₕ, Gₕ₊₁=ρ²Gₕ+Q. The requested latent mean is Aₕm_asof and variance Aₕ²P_asof+Gₕ. These formulas sum future innovation uncertainty; they do not assimilate any future Y. Unit roots work through the recurrence, without dividing by 1−ρ². Store all fractions in reduced integer pairs and normalize denominators. The reference uses math.gcd because the practice runner does not import fractions. Its timeline and per-request work satisfy the scalar bound; exact arithmetic here teaches the information boundary and is not a production floating Kalman implementation.')


HARD_REFERENCE = '''from math import gcd
def solve(rho_numerator, rho_denominator, innovation_variance, prior_mean, prior_variance, observations, requests):
    def fraction(a, b=1):
        if b < 0:
            a, b = -a, -b
        g = gcd(a, b)
        return (a // g, b // g)
    def add(x, y):
        return fraction(x[0] * y[1] + y[0] * x[1], x[1] * y[1])
    def multiply(x, y):
        return fraction(x[0] * y[0], x[1] * y[1])
    def divide(x, y):
        return fraction(x[0] * y[1], x[1] * y[0])
    def text(x):
        return [str(x[0]), str(x[1])]
    rho = fraction(rho_numerator, rho_denominator)
    rho_squared = multiply(rho, rho)
    process_variance = (innovation_variance, 1)
    horizon = max([0] + [row[0] for row in observations] + [row[1] for row in requests])
    measurements = {t: (y, r) for t, y, r in observations}
    means = [(prior_mean, 1)]
    variances = [(prior_variance, 1)]
    powers, noise_sums = [(1, 1)], [(0, 1)]
    for t in range(1, horizon + 1):
        m = multiply(rho, means[-1])
        p = add(multiply(rho_squared, variances[-1]), process_variance)
        if t in measurements:
            y, r = measurements[t]
            denominator = add(p, (r, 1))
            gain = divide(p, denominator)
            innovation = add((y, 1), (-m[0], m[1]))
            m = add(m, multiply(gain, innovation))
            p = divide(multiply(p, (r, 1)), denominator)
        means.append(m)
        variances.append(p)
        powers.append(multiply(rho, powers[-1]))
        noise_sums.append(add(multiply(rho_squared, noise_sums[-1]), process_variance))
    result = []
    for asof, target in requests:
        a = powers[target - asof]
        m = multiply(a, means[asof])
        p = add(multiply(multiply(a, a), variances[asof]), noise_sums[target - asof])
        result.append({"mean": text(m), "variance": text(p)})
    return result'''

# Expected cases are independently derived from covariance matrices, not by
# evaluating HARD_REFERENCE. See tests/test_time_series_practice.py.
EASY_CASES = [{'args': [1, 7, [2, 1]], 'expected': ['7', '1']}, {'args': [4, 5, []], 'expected': ['5', '4']},
 {'args': [2, 4, [-4]], 'expected': ['0', '1']}, {'args': [2, 2, [-1, 0, 1]], 'expected': ['1', '2']},
 {'args': [5, 3, [-2, 1]], 'expected': ['1', '5']},
 {'args': [1000000000, 3, [-2, 1]], 'expected': ['1', '1000000000']},
 {'args': [999999937, 1000000000000000000, [500000000000000000]],
  'expected': ['1999999873000000000000000000', '999999874000003969']}]
EASY_CASES += [
    {'args': [2, 2, [1]+[0]*10000], 'expected': ['3', '2']},
    {'args': [10**9, 1000, list(range(999,0,-1))], 'expected': ['999999666667', '1000000000000000']},
]

HARD_SAMPLES = [{'args': [1, 2, 3, 0, 4, [[1, 8, 1], [3, -10, 4]], [[0, 2], [1, 2], [2, 2], [3, 3], [1, 1]]],
  'expected': [{'mean': ['0', '1'], 'variance': ['4', '1']}, {'mean': ['16', '5'], 'variance': ['16', '5']},
               {'mean': ['16', '5'], 'variance': ['16', '5']},
               {'mean': ['-158', '39'], 'variance': ['76', '39']},
               {'mean': ['32', '5'], 'variance': ['4', '5']}]},
 {'args': [1, 1, 1, 2, 0, [[2, 5, 2]], [[0, 3], [2, 2], [2, 4], [1, 3]]],
  'expected': [{'mean': ['2', '1'], 'variance': ['3', '1']}, {'mean': ['7', '2'], 'variance': ['1', '1']},
               {'mean': ['7', '2'], 'variance': ['3', '1']}, {'mean': ['2', '1'], 'variance': ['3', '1']}]}]

HARD_CASES = [{'args': [1, 2, 3, 0, 4, [], []], 'expected': []},
 {'args': [1, 2, 0, -7, 0, [], [[0, 0], [0, 3], [3, 3]]],
  'expected': [{'mean': ['-7', '1'], 'variance': ['0', '1']}, {'mean': ['-7', '8'], 'variance': ['0', '1']},
               {'mean': ['-7', '8'], 'variance': ['0', '1']}]},
 {'args': [0, 1, 3, 5, 7, [[1, 6, 3], [3, -8, 1]], [[0, 0], [0, 1], [1, 1], [1, 3], [3, 3]]],
  'expected': [{'mean': ['5', '1'], 'variance': ['7', '1']}, {'mean': ['0', '1'], 'variance': ['3', '1']},
               {'mean': ['3', '1'], 'variance': ['3', '2']}, {'mean': ['0', '1'], 'variance': ['3', '1']},
               {'mean': ['-6', '1'], 'variance': ['3', '4']}]},
 {'args': [-1, 1, 2, 3, 4, [[2, -7, 2], [5, 20, 5]], [[0, 5], [2, 5], [5, 5], [1, 2]]],
  'expected': [{'mean': ['-3', '1'], 'variance': ['14', '1']}, {'mean': ['5', '1'], 'variance': ['38', '5']},
               {'mean': ['295', '21'], 'variance': ['190', '63']},
               {'mean': ['3', '1'], 'variance': ['8', '1']}]},
 {'args': [1, 1, 0, 3, 0, [[1, 999, 1], [4, -500, 2]], [[0, 4], [1, 1], [4, 120]]],
  'expected': [{'mean': ['3', '1'], 'variance': ['0', '1']}, {'mean': ['3', '1'], 'variance': ['0', '1']},
               {'mean': ['3', '1'], 'variance': ['0', '1']}]},
 {'args': [-2, 3, 2, 5, 7, [[1, -4, 2], [3, 20, 3], [6, 999, 1]], [[0, 6], [1, 6], [3, 6], [6, 6], [1, 6]]],
  'expected': [{'mean': ['320', '729'], 'variance': ['1927114', '531441']},
               {'mean': ['122', '243'], 'variance': ['210362', '59049']},
               {'mean': ['-18913', '6750'], 'variance': ['103862', '30375']},
               {'mean': ['207346059', '268474'], 'variance': ['103862', '134237']},
               {'mean': ['122', '243'], 'variance': ['210362', '59049']}]},
 {'args': [2, 4, 3, 0, 4, [[1, 8, 1]], [[0, 3], [1, 3], [1, 1], [1, 3]]],
  'expected': [{'mean': ['0', '1'], 'variance': ['4', '1']}, {'mean': ['8', '5'], 'variance': ['19', '5']},
               {'mean': ['32', '5'], 'variance': ['4', '5']},
               {'mean': ['8', '5'], 'variance': ['19', '5']}]},
 {'args': [19, 20, 1000000, -1000000, 1000000,
           [[10, 999999, 11], [20, 999999, 21], [30, 999999, 31], [40, 999999, 41], [50, 999999, 51],
            [60, 999999, 61], [70, 999999, 71], [80, 999999, 81], [90, 999999, 91], [100, 999999, 101],
            [110, 999999, 111], [120, 999999, 121]],
           [[0, 120], [50, 120], [119, 120], [120, 120]]],
  'expected': [{'mean': ['-2821188561558006050182806325699651325904349317385522184850131166315238114862945518835835570975439814916967715430619167129237431101638511203016746250533601',
                         '1329227995784915872903807060280344576000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'],
                'variance': ['18121434683961150777033905111414277726416294760580875530082226568024037576693124939942291926944504220491724639218784836975879098677028411984608792591376635999714417080557817434672935674237421197831469386170660329751706442516791503273516393699675684932280508897205716205806394650426227919832987504887498164614363601',
                             '1766847064778384329583297500742918515827483896875618958121606201292619776000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000']},
               {'mean': ['7668535168706763528299603432337358578562865175288539646076669434430499267930236010656558459710702747595442282166871502807813951658141712562706096477797229721756528774646623048644218690790597745646842252111122023153116798316850460896266021020489259541057',
                         '278010903072364136569050813331370568035083430693203147148508910270935421899817087258856411404690000816111475784758723286841159583889894101575740808028465509870841253245372145336320000000000000000000000000000000000000000000000000000000000000000000000'],
                'variance': ['235463929749598062889644818333659370504008446966210568413339136246687273902939622050209383951608201809399408651344182696479951989847576741685633040687882766256648247459386849642683733715526092106903531999766037639530197466141902385592929116420666146762239793659991913137184140560090255853065511362407748326179745941818605184588294325214552148477251',
                             '22975213984471946229282951608764882417518366738375283073874706683024025441014672233164564670364893553835454107062566101146004875567296759261645075493425173743104160974399718396334350216405074583329177600000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000']},
               {'mean': ['2224592701089684434435418015771900385408885430786117602894498654132711075192274544860922003817798297831145496062219818370539453132627467743230802948514533819804864068294225460104475006144055055319573808518959549133355061729388446130038918152545948711813583647209330864620021832587732393985259855385818399559830579918563009782893968926487879034940976736409633096148120588401',
                         '3715504821875326892359318151423259245404214577754601839689185825438069049853810327245132034260385754331945594697264520540780675024712855928375347330363275733738958285052167911653744195086240174807366821362695042523300320385601385710880741305690766431087303113541873752616220159147378741739864879367435579834352188931103288729243830707898760944188102137845760000000000'],
                'variance': ['250335238663295975523589575291114143596160481755228119154979403233828594123474236091443425940534084436989515889736525777323084821030146169541520520220579496516954983444097851741189256164524112773402473784613156905126056987228577753424531280426028780351878798695276262308106444222863317068975237034869116119956537121437338727126121496371095769415163922251451871086343285296010313612351689',
                             '38046769376003347377759417870574174672939157276207122838417262852485827070503017750990152030826350124359122889699988690337594112253059644706563556662919943513486932838934199415334340557683099390027436250753997235438595280748558189679418790970273448254333983882668787226790094429669158315416216364722540337503766414654497676587456826448883312068486165891540582400000000000000000000']},
               {'mean': ['22757976789763424580928699505625192227042765692740956832546812604912525171746428986641763543082523118882547600248734270331005575559030417284816686490376782125949323409808144265495600256725414634478676686079189056691719095766115973300642801755990553168671848392650891389196239537115503973600328323273027135933655252489269053281730524290259824896457632759576827329660331847278079088825279695301',
                         '22758167483853679266238389470970589370117809763023503656076622883875794991686342450599208704448164947759505758509652679632237788174338980887139092219175973620920010487542851161756228329066508402584424282218136194435595005205231666269589317281794198494465233918847824111941898711299027912466491127004477049757943188833955629213180779877008734935993109916138613408801244117819119419304699'],
                'variance': ['2753687625296255730759485328202255579557765299307509310704773435572114535358216597005877685345874928806884674787101783550553933031331607864956725722426374461686504817885076369153081817809765240507427211630744725956386626859514355287669844084686316583870666785648038885389170886451496487758727607383560277319521908335810725998387336460082053463566803144765970581949776138256113449735868579',
                             '22758167483853679266238389470970589370117809763023503656076622883875794991686342450599208704448164947759505758509652679632237788174338980887139092219175973620920010487542851161756228329066508402584424282218136194435595005205231666269589317281794198494465233918847824111941898711299027912466491127004477049757943188833955629213180779877008734935993109916138613408801244117819119419304699']}]}]
HARD_CASES.append({'args': [0,1,3,-5,7,[],[[0,0],[0,120],[119,120]]*300],
                   'expected': [{'mean': ['-5', '1'], 'variance': ['7', '1']}, {'mean': ['0', '1'], 'variance': ['3', '1']}, {'mean': ['0', '1'], 'variance': ['3', '1']}]*300})
