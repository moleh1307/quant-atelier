"""Estimation practice: repeated-sample risk and posterior predictive uncertainty.

The predictive reference starts at a mode, not at an underflowing endpoint.
Published expectations are checked by a separate exact integer-moment oracle.
"""


def add_questions(add, questions):
    next(q for q in questions if q['id'] == 'q24')['rubric'] = [
        'Derive the centred-sum identity and use iid finite-variance sampling to get expectation (n−1)σ².',
        'Require n>1 for the corrected divisor; distinguish unbiased variance from unbiased standard deviation.',
        'Explain that dependence changes Var(sample mean), so the same n−1 correction is not generally unbiased.',
    ]

    def question(suffix, title, level, minutes, prompt, answer, hints, solution,
                 follow, follow_answer, rubric):
        add(f'q_l09_{suffix}', title, 'Estimation', level, 'researcher', minutes,
            prompt, answer, hints, solution, follow, follow_answer, 'l09')
        questions[-1]['rubric'] = rubric
        for key in ('prompt', 'solution', 'followSolution'):
            questions[-1][key] = questions[-1][key].replace(r'\n\n', '\n\n')

    question('e1', 'Spread of observations, uncertainty of a mean', 'Easy', 5,
        r'You observe 36 iid measurements with unknown mean \(\mu\) and known population standard deviation 12 units. Their observed sample mean is 10 units. What is the standard error of the sample-mean estimator, in units? Assume finite variance; do not assume normality or substitute the observed mean for the unknown \(\mu\).',
        2,
        ['What varies if you repeat the whole 36-observation experiment?',
         'Independence makes the variance of the mean equal to the individual variance divided by 36.'],
        r'The estimator is \(\bar X\); its realised estimate is 10. Under iid sampling, \(\operatorname{Var}(\bar X)=12^2/36=4\), so its standard error is \(\sqrt4=2\) units. The 12 describes individual measurements, not repeated sample means. The realised error \(10-\mu\) remains unknown. This calculation is exact without normality; it does not justify an exact normal confidence interval.',
        r'For one fresh measurement Y, independent of the sample and from the same population, what is the repeated-experiment mean squared prediction error of using \(\bar X\) to predict Y?',
        r'Write \(Y-\bar X=(Y-\mu)-(\bar X-\mu)\). Both terms have zero mean and are independent. Thus \(E[(Y-\bar X)^2]=144+4=148\) square units. Its root is \(\sqrt{148}\), approximately 12.166 units. Predicting an individual adds its own noise; the standard error 2 describes estimation of the common mean. After conditioning on the observed sample, prediction MSE is \(144+(10-\mu)^2\), not necessarily 148.',
        ['Compute variance 144/36 before taking its square root.',
         'Distinguish the random estimator from the observed value 10 and its unknown realised error.',
         'State that finite-variance iid sampling suffices for the standard error, but not exact Gaussian coverage.'])

    question('h1', 'The correction that improves bias and worsens risk', 'Hard', 20,
        r'Let \(X_1,\ldots,X_n\) be iid Uniform(0,θ), with integer \(n\geq1\) and unknown \(\theta>0\). Write \(M=\max_iX_i\). Use squared-error risk \(R_\theta(T)=E_\theta[(T-\theta)^2]\).\n\nAmong estimators \(T_c=cM\), choose a real coefficient c depending only on n, not on θ or the realised sample. Derive its risk, find the risk-minimising c, and compare it with both M and the unbiased correction \((n+1)M/n\). Does the unbiased rule have the smallest risk? Justify the comparison for every θ, including n=1.',
        None,
        [r'From \(P(M\leq x)=(x/\theta)^n\), derive both \(E[M]\) and \(E[M^2]\).',
         'Expand the squared error as a quadratic in c. The unknown scale θ factors out.',
         'Compare complete risks, not just biases; a coefficient greater than one need not remove all bias.'],
        r'On \([0,\theta]\), the maximum has density \(nx^{n-1}/\theta^n\). Integration gives \(E[M]=n\theta/(n+1)\) and \(E[M^2]=n\theta^2/(n+2)\). Therefore\n\n\[R_\theta(cM)=\theta^2\left(\frac{nc^2}{n+2}-\frac{2nc}{n+1}+1\right).\]\n\nIts positive quadratic coefficient gives a unique minimum at \(c_*=(n+2)/(n+1)\). Completing the square gives \(R_\theta(cM)=\theta^2/(n+1)^2+[n\theta^2/(n+2)](c-c_*)^2\). The best rule has negative bias \(-\theta/(n+1)^2\); its risk is \(\theta^2/(n+1)^2\). The raw maximum has risk \(2\theta^2/[(n+1)(n+2)]\), and the unbiased correction has risk \(\theta^2/[n(n+2)]\). Each exceeds the best risk for every positive θ and every n≥1. Bias removal increases variance enough to lose under this loss. At \(n=1\), the three risks are \(\theta^2/4\), \(\theta^2/3\) and \(\theta^2/3\), respectively.\n\nThis proves optimality within fixed multiples of M and pointwise dominance over those two comparators. It does not, by itself, prove minimax optimality over all estimators or all θ; absolute risks grow without bound as θ grows.',
        r'Instead use \(T_a=a\bar X\), with a depending only on n. Find its best squared-error risk and compare it with \(c_*M\). Does using all observations through their mean necessarily improve this estimation problem?',
        r'Here \(E[\bar X]=\theta/2\) and \(\operatorname{Var}(\bar X)=\theta^2/(12n)\). Thus \(R_\theta(a\bar X)/\theta^2=a^2/(12n)+(a/2-1)^2\). Minimising gives \(a_*=6n/(3n+1)\), with risk \(\theta^2/(3n+1)\). Since \((n+1)^2-(3n+1)=n(n-1)\), the best maximum rule has strictly smaller risk for n>1 and equal risk for n=1. The mean compresses the sample differently from the maximum; using every value in an arithmetic average is not a universal efficiency guarantee.',
        ['Derive the first and second moments of the uniform maximum under the stated iid model.',
         'Optimise the whole risk quadratic to obtain c*=(n+2)/(n+1) and its residual negative bias.',
         'Compute and compare all three risks for every θ>0, checking n=1.',
         'Keep the restricted-class result separate from a global minimax claim.'])

    question('h2', 'Balance endpoint error against central noise', 'Hard', 25,
        r'Observe the success count \(K\sim\operatorname{Binomial}(n,p)\), where \(n\geq1\) is known and \(p\in[0,1]\) is unknown. Only K is observed. Under squared-error loss, consider \(\delta_a(K)=(K+a)/(n+2a)\), with \(a>0\) chosen from n before observing K.\n\nDerive the frequentist risk at fixed p, choose a so that the risk is constant over the whole parameter interval, and prove that this rule minimises the worst-case risk among ALL estimators based on K, not merely this family. “Minimax” here means minimising \(\sup_{0\leq p\leq1}E_p[(\delta(K)-p)^2]\).\n\nFor the global lower bound you may introduce a \(\operatorname{Beta}(a,a)\) prior. Derive why its posterior mean minimises posterior expected squared error, and explain how an average risk can lower-bound a worst-case risk. Do not treat constant risk alone as a proof of optimality.',
        None,
        [r'Compute the bias and variance separately; use \((1-2p)^2=1-4p(1-p)\).',
         'The endpoint risks and the p=1/2 risk must agree to flatten this quadratic.',
         'For any competing rule, its worst risk is at least its average risk under your chosen prior. Which rule minimises that average?'],
        r'The bias is \(a(1-2p)/(n+2a)\), and the variance is \(np(1-p)/(n+2a)^2\). Thus\n\n\[R_p(\delta_a)=\frac{a^2+(n-4a^2)p(1-p)}{(n+2a)^2}.\]\n\nChoose \(a_* = \sqrt n/2\). Then the coefficient of p(1−p) vanishes and the risk is the constant \(r_*=1/[4(\sqrt n+1)^2]\), including at p=0 and p=1. Constant risk supplies an attainable upper bound on the minimax value, but an inferior rule could also have constant risk.\n\nFor a lower bound assign p the proper \(\operatorname{Beta}(a_*,a_*)\) prior. After count \(K=k\), its posterior is \(\operatorname{Beta}(k+a_*,n-k+a_*)\), whose mean is \(\delta_{a_*}(k)\). For any proposed output d, expand its posterior squared error as \(E[(d-p)^2\mid K=k]=\operatorname{Var}(p\mid K=k)+(d-E[p\mid K=k])^2\). The posterior mean minimises this for every k, hence minimises average risk under this prior. Its average risk equals \(r_*\), since its fixed-p risk is constant. For any other rule g,\n\n\[\sup_{p\in[0,1]}R_p(g)\ \geq\ \int_0^1R_p(g)\,d\pi(p)\ \geq\ r_*.\]\n\nOur rule attains \(r_*\), proving global minimax optimality for the specified observation and loss. Independent randomisation cannot improve the lower bound: conditional on K, randomising the output adds nonnegative variance to the same decomposition. This is a frequentist worst-case claim established using a prior as a proof device, not a claim that the unknown p was actually sampled from that prior.',
        r'For \(a=1\) (a uniform Beta prior), give the worst-case risk for arbitrary n and identify exactly when that rule equals the minimax rule. Why is a fixed amount of shrinkage not universally optimal?',
        r'The risk is \([1+(n-4)p(1-p)]/(n+2)^2\). For n<4, its largest value is \(1/(n+2)^2\), attained at p=0 or 1; for n>4 it is \(n/[4(n+2)^2]\), attained at p=1/2. At n=4 it is constant 1/36, and \(a_*=1\), so the uniform-prior rule is exactly minimax. For other n its worst risk is strictly larger than \(r_*\). Changing the parameter interval or the loss changes this balance; the proof used the full [0,1] interval and squared error.',
        [r'Derive the risk as a function of the fixed p and identify \(a_*=\sqrt n/2\).',
         r'Check that the constant includes p=0 and p=1 and compute \(r_*\).',
         'Derive posterior-mean optimality via the conditional squared-error decomposition.',
         'Give the prior-average lower bound for every competing rule, including randomisation; constant risk alone is insufficient.'])


def add_coding(add, tasks):
    def exercise(level, title, prompt, signature, samples, tests, solution, explanation):
        add(f'c_l09_{level.lower()}', title, level, 'Estimation', prompt,
            signature, samples, tests, solution, explanation)
        tasks[-1]['path'] = 'researcher'
        for key in ('prompt', 'explanation'):
            tasks[-1][key] = tasks[-1][key].replace(r'\n\n', '\n\n')

    exercise('Easy', 'Update a probability without discarding its uncertainty',
        r'An unknown common Bernoulli success probability p has a Beta(alpha,beta) prior. Conditional on p, all past and future trials are independent with that same p. alpha and beta are integers from 1 to 10^6. batches contains at most 100000 [successes,failures] pairs; each count is an integer from 0 to 10^9, and batches are disjoint. After EACH batch, return [posterior_mean, posterior_variance] for p, in input order. Return [] for no batches. A [0,0] batch still emits the current posterior summary. Do not round or mutate batches. Use cumulative counts, O(number of batches) time and O(1) auxiliary state apart from output. This variance measures uncertainty about p, not the variance of a new Bernoulli outcome.',
        'def solve(alpha, beta, batches):',
        [{'args': [2,2,[[3,1],[0,0],[1,3]]], 'expected': [[5/8,5/192],[5/8,5/192],[.5,1/52]]}],
        [{'args': [1,1,[]], 'expected': []},
         {'args': [1,1,[[0,0]]], 'expected': [[.5,1/12]]},
         {'args': [1,1,[[0,2],[2,0]]], 'expected': [[1/4,3/80],[.5,1/28]]},
         {'args': [3,7,[[0,0],[0,0]]], 'expected': [[.3,21/1100],[.3,21/1100]]},
         {'args': [1,1,[[10**9,0],[0,10**9]]], 'expected': [[(10**9+1)/(10**9+2),(10**9+1)/((10**9+2)**2*(10**9+3))],[.5,1/(4*(2*10**9+3))]]},
         {'args': [1,1,[[1,1]]*3000], 'expected': [[.5,1/(4*(2*i+3))] for i in range(1,3001)]}],
        '''def solve(alpha, beta, batches):
    a, b = alpha, beta
    result = []
    for successes, failures in batches:
        a += successes
        b += failures
        total = a + b
        result.append([a / total, (a / total) * (b / total) / (total + 1)])
    return result''',
        r'After cumulative counts s,f, multiply the prior by the Bernoulli likelihood to get Beta(A,B), with A=alpha+s and B=beta+f. Its mean is A/(A+B). To obtain the variance, the beta-integral moment ratios give \(E[p^2]=A(A+1)/[(A+B)(A+B+1)]\); subtracting the squared mean gives \(AB/[(A+B)^2(A+B+1)]\). Compute this as two proportions divided by total+1, keeping cumulative counts as integers. Resetting to the prior at each batch loses information. An empty batch changes nothing but still emits; no batches emit nothing. A new single outcome has predictive variance mean×(1−mean), which includes outcome noise and differs from posterior variance. O(b) time and O(1) extra state, excluding the b output rows.')

    # Fixed expectations: reviewed independently using beta-integral moments
    # and high-precision endpoint probabilities in test_estimation_practice.py.
    tests = [{'args': [1, 1, 0, 0, 0, [0, 1]], 'expected': [1.0, 0.0]},
     {'args': [1, 1, 0, 0, 4, [0, 1, 2, 4, 5, 2]], 'expected': [1.0, 0.8, 0.6, 0.2, 0.0, 0.6]},
     {'args': [1, 5, 0, 0, 9, [0, 1, 4, 9, 10]],
      'expected': [1.0, 0.6428571428571429, 0.1258741258741259, 0.0004995004995004995, 0.0]},
     {'args': [5, 1, 0, 0, 9, [0, 1, 4, 9, 10]],
      'expected': [1.0, 0.9995004995004995, 0.972027972027972, 0.35714285714285715, 0.0]},
     {'args': [2, 3, 4, 1, 20, [0, 1, 7, 15, 20, 21]],
      'expected': [1.0, 0.9998231653404067, 0.925644869872756, 0.26627595293262457, 0.005305039787798408, 0.0]},
     {'args': [1, 1, 1000000000, 0, 4000, [0, 1, 3999, 4000, 4001]],
      'expected': [1.0, 1.0, 0.9999999999840041, 0.999996000016004, 0.0]},
     {'args': [1, 1, 0, 1000000000, 4000, [0, 1, 2, 4000, 4001]],
      'expected': [1.0, 3.999983996064032e-06, 1.5995872016771996e-11, 0.0, 0.0]},
     {'args': [2000, 2000, 0, 0, 3000, [0, 1, 1499, 1500, 1501, 1502, 2999, 3000, 3001]],
      'expected': [1.0,
                   1.0,
                   0.5165117700134811,
                   0.505505320283415,
                   0.494494679716585,
                   0.4834882299865189,
                   0.0,
                   0.0,
                   0.0]},
     {'args': [3, 7, 0, 0, 200, [0, 1, 100, 150, 199, 200, 201]],
      'expected': [1.0,
                   0.9999439919348386,
                   0.09719957307885702,
                   0.0018708783448369197,
                   9.143593836611098e-11,
                   1.1529375499347326e-11,
                   0.0]},
     {'args': [1, 1, 0, 0, 100000, [0, 1, 50000, 100000, 100001]],
      'expected': [1.0, 0.999990000099999, 0.5000049999500005, 9.99990000099999e-06, 0.0]},
     {'args': [1, 1, 0, 0, 4, []], 'expected': []}]

    tests.append({'args': [1,1,10**9,10**9,100000,[49900,50000,50001,50100]],
                  'expected': [0.7374819381557225,0.5012615315692034,0.4987384684307966,0.26458379573982616]})
    # Keep the official stress case small enough for an editable debug copy.
    # Maximum query-count behaviour is checked separately by the test oracle.
    queries = [0,1,100000,100001] + [(i*37)%100002 for i in range(6000)]
    tests.append({'args': [1,1,0,0,100000,queries],
                  'expected': [(100001-r)/100001 for r in queries]})

    exercise('Hard', 'Predict a batch without pretending p is known',
        r'Prior p is Beta(alpha,beta). Observe successes successful trials and failures unsuccessful trials, then predict m future trials. Conditional on the SAME p, all observed and future trials are independent Bernoulli(p). alpha,beta are integers in [1,10000]; observed counts are integers in [0,10^9]; m is an integer in [0,100000]. thresholds has at most 100000 integers r in [0,m+1]. Return the posterior predictive probability that the future success count H is AT LEAST r, for each query in its original order, retaining duplicates. Return [] for no queries; if m=0 only H=0 is possible. Do not mutate inputs, simulate, round, or replace p by its posterior mean.\n\nAim for O(m+number of queries) time and O(m) auxiliary space, with floating-point probabilities. A direct endpoint probability can underflow for valid inputs: normalise relative masses from a mode or use an equivalently stable method. The editorial derives the predictive mass, adjacent-mass ratios and a mode; no external numerical libraries are needed. Numerical answers are checked with absolute tolerance 10^(-7), so unrepresentably small tails may return zero. P(H≥0) is one and P(H≥m+1) is zero.',
        'def solve(alpha, beta, successes, failures, m, thresholds):',
        [{'args': [1,1,0,0,2,[2,1,0,3,2]], 'expected': [1/3,2/3,1,0,1/3]},
         {'args': [2,2,3,1,2,[2,1]], 'expected': [5/12,5/6]}],
        tests,
        '''from math import fsum
def solve(alpha, beta, successes, failures, m, thresholds):
    if not thresholds:
        return []
    a, b = alpha + successes, beta + failures
    mode = 0 if a + b == 2 else min(m, (m + 1) * (a - 1) // (a + b - 2))
    weights = [0.0] * (m + 1)
    weights[mode] = 1.0
    for k in range(mode, m):
        weights[k + 1] = weights[k] * ((m - k) * (k + a)) / ((k + 1) * (m - k - 1 + b))
    for k in range(mode, 0, -1):
        weights[k - 1] = weights[k] * (k * (m - k + b)) / ((m - k + 1) * (k - 1 + a))
    normalizer = fsum(weights)
    tail = [0.0] * (m + 2)
    for k in range(m, -1, -1):
        tail[k] = tail[k + 1] + weights[k] / normalizer
    tail[0] = 1.0
    return [tail[r] for r in thresholds]''',
        r'First update to A=alpha+successes, B=beta+failures. Integrate the conditional count mass \(\binom mk p^k(1-p)^{m-k}\) against the Beta(A,B) posterior. This gives \(w_k=P(H=k)=\binom mk\,\mathrm B(A+k,B+m-k)/\mathrm B(A,B)\), where \(\mathrm B\) is the beta integral, not the posterior parameter B. Future trials are independent conditional on p, but share parameter uncertainty after integrating it out. For example a uniform posterior makes H uniform on 0,…,m, rather than Binomial(m,1/2).\n\nCancel neighbouring factorial/beta factors to obtain \(w_{k+1}/w_k=(m-k)(k+A)/[(k+1)(m-k-1+B)]\). Because A,B≥1, the condition that this ratio is at least one reduces to \((A+B-2)k\leq m(A-1)+1-B\). One mode is \(k_* = \min(m,\lfloor(m+1)(A-1)/(A+B-2)\rfloor)\) when A+B>2. If A=B=1, every mass is equal, so choose zero. Exact integer arithmetic locates the mode, including ties and one-sided modes. Set its RELATIVE mass to one, propagate right using the ratio, and left using the reciprocal ratio. Moving away from a mode never increases exact relative masses above one. This avoids starting from a tiny endpoint mass that has already rounded to zero; tails may still harmlessly underflow below the stated absolute tolerance.\n\nNormalise the relative masses using math.fsum, then build suffix probabilities from k=m down to zero. Read each requested suffix directly; computing 1−a CDF can lose a small upper tail through cancellation. The empty-query shortcut and m=0 are covered. With prior Beta(2,2) and 3 successes/1 failure, the posterior is Beta(5,3); P(H=2) for m=2 is E[p²]=5×6/(8×9)=5/12, not (5/8)². Each recurrence step and query costs O(1) with the bounded integer sizes, giving O(m+q) time and O(m) working space, excluding output. This calculation relies on one common p; a changing probability or extra conditional dependence requires a different model.')
