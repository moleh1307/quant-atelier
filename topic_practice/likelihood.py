"""Likelihood practice: actual observation mechanisms and attained optima.

Hard transfer distinguishes truncation from censoring and proves mixture
singularity. The coding solver brackets a unique selected-sample score root.
"""


def add_questions(add, questions):
    specific = {
        'q49': ['Multiply independent event densities to obtain λ⁴ exp(−10λ).',
                'Verify a unique global maximum at 0.4 and give inverse-second units.',
                'Include censored exposure in the follow-up and distinguish an excluded zero-rate limit from a positive-rate MLE.'],
        'q50': ['Include the support indicator θ≥M before optimising; use the specified closed-support density.',
                'Show decreasing likelihood on the feasible interval and derive E[M]=nθ/(n+1).',
                'Distinguish the strict-support unattained supremum from an unchanged continuous probability law.'],
        'q51': ['Identify one random observation and deterministic copies, giving likelihood p rather than p¹⁰⁰.',
                'Compare the same endpoint MLE with likelihood ratios 1/2 versus 2⁻¹⁰⁰.',
                'Explain why agreement of estimates does not validate precision and why distinct equal-valued events need a sampling argument.'],
    }
    for q in questions:
        if q['id'] in specific:q['rubric']=specific[q['id']]

    def question(suffix,title,level,minutes,prompt,answer,hints,solution,follow,follow_answer,rubric):
        add(f'q_l25_{suffix}',title,'Likelihood',level,'researcher',minutes,
            prompt,answer,hints,solution,follow,follow_answer,'l25')
        questions[-1]['rubric']=rubric
        for key in ('prompt','solution','followSolution'):
            questions[-1][key]=questions[-1][key].replace(r'\n\n','\n\n')

    question('e1','A larger success probability can fit worse','Easy',5,
        r'Five iid Bernoulli trials share an unknown success probability p. The specified ordered record is H,T,H,H,T, with H meaning success. Compute the likelihood ratio \(L(3/4)/L(1/2)\) for this SAME record. No prior is assigned. Does a larger ratio mean a posterior probability?',27/32,
        ['Count both successes and failures.', 'Use three factors of p and two of 1−p; compare the joint record probabilities.'],
        r'There are three successes and two failures, so \(L(p)=p^3(1-p)^2\). At 3/4 the likelihood is 27/1024; at 1/2 it is 1/32. Their ratio is \(27/32=0.84375\), below one. Raising p rewards successes but penalises failures; “more likely to succeed” is not the same as “better fit to this whole record.” A likelihood ratio compares candidates for fixed data; it is not a normalised probability over p.',
        r'Compare two changes: observing only the success count K=3, and analysing the ordered record CONDITIONAL ON K=3. Which change preserves the ratio, and which discards its information about p?',
        r'Observing only the count gives \(P_p(K=3)=\binom53p^3(1-p)^2\), so the parameter-free factor 10 cancels and the ratio remains 27/32. Conditional on K=3, each of the ten compatible records has probability 1/10 for every \(0<p<1\); the conditional likelihood ratio is one. Changing the representation to a count retains the information used here, whereas conditioning away that count discards it. Both candidates in the question lie in the open interval, so this conditioning is well-defined.',
        ['Use the whole ordered record, including its two failures.',
         'Obtain 27/32 and interpret it as a likelihood comparison, not a posterior.',
         'Distinguish a parameter-free count factor from conditioning away the informative count.'])

    question('e2','The allowed domain changes the best fit','Easy',5,
        r'Eight iid Bernoulli trials are all successes. The model restricts their common probability to \(0\leq p\leq0.9\). What is its maximum likelihood estimate of p? Evaluate the stated domain; do not add a prior or an unbiasedness correction.',.9,
        ['Write the likelihood of the all-success record.', 'Which feasible candidate makes every observed success most likely?'],
        r'The likelihood is \(p^8\), strictly increasing for positive p. The largest permitted value, 0.9, is therefore the unique maximiser. An unconstrained empirical success fraction of one lies outside this model. A boundary maximum does not require an interior derivative to vanish.',
        r'If instead the domain is \(0<p<1\), does a maximum exist? What happens on \([0,1]\), and does either fitting result establish that a failure is impossible?',
        r'On the open interval, the likelihood approaches one as p approaches one but never attains it, so there is no MLE there. On the closed interval the MLE is one. Neither observation of eight successes nor the fitting criterion establishes certainty about the real probability: every positive p assigns some probability to that record. A statement about uncertainty needs further assumptions and a separate procedure.',
        ['Respect the closed upper bound 0.9 and maximise the likelihood there.',
         'Distinguish an attained boundary maximum from an open-domain supremum.',
         'Keep a fitted parameter separate from certainty about future outcomes.'])

    from math import log
    question('m1','Rounded waits are interval observations','Medium',12,
        r'Four independent waits have an Exponential distribution with common rate \(\lambda>0\), in events per second. You observe only the integer bin \(K_i=\lfloor X_i\rfloor\): K=k records \(k\leq X<k+1\) seconds, not an exact duration of k. The bins are [0,1,2,1]. Derive the likelihood of what was observed, verify its maximum, and report the MLE of λ. Give a numerical answer in inverse seconds.',log(2),
        [r'A bin contributes \(P(k\leq X<k+1)\), not the density evaluated at k.',
         r'Integrate the exponential density across the bin to get \(e^{-\lambda k}(1-e^{-\lambda})\).'],
        r'Bin k contributes \(e^{-\lambda k}-e^{-\lambda(k+1)}\). With four bins summing to four,\n\n\[L(\lambda)=(1-e^{-\lambda})^4e^{-4\lambda},\qquad\ell^{\prime}(\lambda)=\frac4{e^\lambda-1}-4.\]\n\nThe score vanishes at \(e^\lambda=2\), giving \(\hat\lambda=\log2\approx0.693147\) per second. The score strictly decreases, is positive near zero and negative at large rates; the likelihood tends to zero at both limits. This is the unique global maximum. Treating bins as exact waits would incorrectly give 4/4=1. The observation mechanism changes the likelihood, not merely the precision of a reported estimate.',
        r'For n bins of width Δ>0 seconds, with K=k recording \(k\Delta\leq X<(k+1)\Delta\), derive the general fit. What if every bin is zero?',
        r'Let \(S=\sum_iK_i\). Then \(L(\lambda)=(1-e^{-\lambda\Delta})^n e^{-\lambda\Delta S}\). For S>0 the maximiser is \(\hat\lambda=\Delta^{-1}\log(1+n/S)\). For S=0 the likelihood increases to one as λ grows without bound; no finite positive-rate MLE exists. A recorded zero bin means a wait shorter than Δ, not a zero-duration event. A different rounding rule, such as nearest integer, needs different intervals.',
        ['Integrate over the observed intervals rather than substitute integer bins into a density.',
         'Derive the score and verify the unique global maximum at log(2), with correct units.',
         'Handle the all-zero-bin boundary without inventing a finite maximiser.'])

    question('h1','Discarded waits change more than the sample size','Hard',25,
        r'Underlying waits are iid Exponential(λ), with \(\lambda>0\). A data export keeps only completed waits shorter than a known cutoff c>0. You receive n≥1 retained exact durations \(0<x_i<c\), but no rejected waits and no count of screened subjects. Analyse their conditional iid distribution given retention, with n held fixed.\n\nDerive the conditional likelihood and prove exactly when it has a finite positive-rate maximiser. Show uniqueness when it exists, and describe the other case as a maximum or a supremum on the stated open domain. Explain why taking the reciprocal of the retained sample mean is wrong. You may use integration or the fact that the derivative of a mean under a density proportional to \(e^{-\lambda x}\) is minus its variance, but justify that fact for this bounded support.',None,
        [r'Retention has probability \(1-e^{-\lambda c}\), which depends on λ and cannot be dropped.',
         r'The conditional mean is \(g(\lambda)=1/\lambda-c/(e^{\lambda c}-1)\). Compare it with the observed mean.',
         'The conditional law approaches a uniform law on (0,c) as λ tends to zero.'],
        r'For one retained duration, the density is \(\lambda e^{-\lambda x}/(1-e^{-\lambda c})\) on (0,c). Thus\n\n\[\ell(\lambda)=n\log\lambda-\lambda\sum_i x_i-n\log(1-e^{-\lambda c}),\qquad\ell^{\prime}(\lambda)=n[g(\lambda)-\bar x].\]\n\nTo justify strict monotonicity, write the conditional density as \(e^{-\lambda x}/Z(\lambda)\), with \(Z(\lambda)=\int_0^c e^{-\lambda u}\,du\). Differentiation under this bounded-support integral gives \(g=-Z^{\prime}/Z\) and \(g^{\prime}=-[E_\lambda[X^2]-E_\lambda[X]^2]<0\). Its variance is positive because the density has positive mass across the interval. Integration gives the displayed g. Its limit is c/2 at λ approaching zero, from the limiting uniform density, and zero as λ grows without bound.\n\nConsequently a unique score root, and global maximiser, exists exactly when \(0<\bar x<c/2\). The score is positive before that root and negative afterwards. If \(\bar x\geq c/2\), the score is strictly negative for every positive λ, including the equality case. The likelihood has its supremum at the excluded limit λ→0, not an attained MLE. The limit density is uniform, with joint density \(c^{-n}\). The unselected exponential rule \(1/\bar x\) ignores the parameter-dependent retention normaliser and solves the wrong model.',
        r'Now the original fixed screening count N≥n and each retention status become available. Every rejected wait is known only to exceed c. Derive the FULL likelihood and its fit when n>0. How can a retained mean above c/2 now permit a positive-rate MLE?',
        r'Under fixed N and this deterministic cutoff, multiply n event densities and N−n survival probabilities. The parameter-dependent likelihood is \(\lambda^n\exp[-\lambda(\sum_i x_i+(N-n)c)]\). Any count-ordering coefficient is parameter-free. Its unique positive maximiser is \(n/[\sum_i x_i+(N-n)c]\). The screening statuses restore information discarded by conditioning on retention. For c=1, one retained duration 3/4 and N=2, this full fit is 4/7; the retained-only conditional fit has no positive maximiser. If n=0 and N>0, the full likelihood is decreasing on λ>0 and again has only a zero-rate supremum. Changing the censoring/selection mechanism or making N data-dependent requires stating the new experiment.',
        ['Include the λ-dependent retention normaliser and derive the conditional score.',
         'Prove the mean is strictly decreasing using its variance, with limits c/2 and zero.',
         'Give the exact existence condition and distinguish the equality-case supremum from an attained maximum.',
         'Explain the different full-screening likelihood and why retained mean alone cannot recover its exposure.'])

    question('h2','A mixture can collapse around one observation','Hard',25,
        r'A fixed dataset \(x_1,\ldots,x_n\), with n≥2 and at least two distinct real values, is fitted as iid from a TWO-component normal mixture. Its density is \(f(x)=\tfrac12\phi(x;\mu_1,v_1)+\tfrac12\phi(x;\mu_2,v_2)\), where \(\phi(x;\mu,v)=(2\pi v)^{-1/2}\exp[-(x-\mu)^2/(2v)]\), both means are unrestricted and both variances are positive. The weights are fixed at one half; the component labels are unobserved.\n\nA colleague argues that the sample has nonzero spread, so a finite joint MLE must exist as in the single-normal model. Prove or disprove this by a concrete parameter sequence and a bound on the likelihood of the WHOLE record, not only one density factor. Does a finite answer returned by an optimiser prove that a global MLE exists?',None,
        ['Collapse one component around one observed value while leaving the other component fixed.',
         'Each other observation still has a strictly positive density from the fixed component.',
         'An unbounded likelihood has no finite maximiser even if numerical iterations stop.'],
        r'Set \(\mu_1=x_1\), \(v_1=\varepsilon^2\), and keep \(\mu_2=0,v_2=1\). At x₁, the first component contributes \(1/(2\sqrt{2\pi}\varepsilon)\). For every other observation, the mixture is at least \(\phi(x_i;0,1)/2>0\). Therefore\n\n\[L\ \geq\ \frac1{2\sqrt{2\pi}\varepsilon}\prod_{i=2}^n\frac{\phi(x_i;0,1)}2\ \longrightarrow\ \infty.\]\n\nThe fixed product is strictly positive for this finite dataset. Thus the likelihood is unbounded and no finite positive-variance global MLE exists, despite nonzero overall sample spread. The second component supports the remaining observations while the first concentrates around one; a single normal cannot perform that separation. At every allowed finite parameter tuple the density is finite, so setting variance to zero is not an admissible maximiser. Numerical convergence can identify a local fit or an imposed floor, not rescue the unrestricted global problem.',
        r'Impose a KNOWN variance floor \(v_j\geq v_0>0\), keeping the half weights fixed. Prove that a finite global maximiser now exists even though the means and variances initially have no upper bounds. Does this guarantee uniqueness or that an optimiser finds it?',
        r'Let \(a=\min_i x_i\), \(b=\max_i x_i\), and \(D=b-a>0\). Clipping either mean into [a,b] decreases its distance to every observed value, hence cannot decrease any component density or the mixture likelihood. With clipped means, all squared residuals are at most D². The derivative of a component log-density with respect to its variance is \([(x-\mu)^2-v]/(2v^2)\). For variance above \(V=\max(v_0,D^2)\), reducing it to V cannot decrease any component density. Thus every feasible tuple has an equally good or better representative in the compact box \([a,b]^2\times[v_0,V]^2\). The likelihood is continuous there, so it attains a finite maximum, also global over the original constrained domain. This is an existence proof, not uniqueness: swapping components preserves the fit, and other equal maxima or local maxima may remain. A numerical method still needs a global-optimality argument. The variance floor changes the statistical model and must be reported.',
        ['Use an admissible shrinking-variance sequence and bound every remaining record factor away from zero.',
         'Conclude unbounded likelihood, excluding variance zero from the allowed model.',
         'Explain why single-normal nonzero spread and finite optimiser output do not prove existence here.',
         'For the follow-up, justify mean clipping, a variance upper cap, continuity and compactness; separate existence from uniqueness.'])


def add_coding(add,tasks):
    def exercise(level,title,prompt,signature,samples,tests,solution,explanation):
        add(f'c_l25_{level.lower()}',title,level,'Likelihood',prompt,signature,samples,tests,solution,explanation)
        tasks[-1]['path']='researcher'
        for key in ('prompt','explanation'):tasks[-1][key]=tasks[-1][key].replace(r'\n\n','\n\n')

    exercise('Easy','Fit a probability within its permitted interval',
        r'Inputs successes and trials give the success count and total trial count of an ordered iid Bernoulli record. Both counts are integers with \(0\leq\text{successes}\leq\text{trials}\leq10^{18}\). low and high are numeric bounds satisfying 0≤low≤high≤1, including endpoints. Return the maximum-likelihood probability in that CLOSED interval. If several values maximise, return the smallest. An empty record has likelihood one for every p. Return None if EVERY allowed p gives the record zero likelihood, so no allowed model can explain it. Otherwise return a numerical probability without manual rounding. Do not add a prior or an n−1 correction; O(1) time/space. The all-zero-likelihood rule is an explicit diagnostic, rather than calling a zero-probability fit explanatory.',
        'def solve(successes, trials, low, high):',
        [{'args':[7,10,.2,.6],'expected':.6}, {'args':[0,0,.1,.9],'expected':.1}],
        [{'args':[0,8,0,1],'expected':0}, {'args':[8,8,0,1],'expected':1},
         {'args':[2,8,.4,.9],'expected':.4}, {'args':[6,8,.2,.9],'expected':.75},
         {'args':[4,8,.3,.3],'expected':.3}, {'args':[4,8,0,0],'expected':None},
         {'args':[0,8,1,1],'expected':None}, {'args':[0,0,1,1],'expected':1},
         {'args':[0,8,.3,.7],'expected':.3}, {'args':[8,8,.2,.9],'expected':.9},
         {'args':[10**18-1,10**18,0,1],'expected':(10**18-1)/10**18}],
        '''def solve(successes, trials, low, high):
    if trials == 0:
        return low
    if (high == 0 and successes > 0) or (low == 1 and successes < trials):
        return None
    return max(low, min(high, successes / trials))''',
        r'For a nonempty record with both outcomes, the log-likelihood score has the sign of successes−trials×p. It increases before the empirical success fraction and decreases after it. For all failures or all successes the same directional conclusion holds at the boundary. Project the unrestricted fit onto the closed interval. Test impossible endpoint-only models using the integer counts before floating-point division; a proportion extremely close to one can round to one even when there was a failure. With zero trials the empty product is one and every allowed p ties, so choose low. No likelihood product or logarithm is needed. O(1) operations and bounded input sizes; None diagnoses an impossible allowed model, rather than changing the parameter domain.')

    # Fixed expectations are verified using a separate high-precision score
    # equation and finite-support quadrature in test_likelihood_practice.py.
    tests=[{'args': [[], 10], 'expected': None},
     {'args': [[3, 7], 10], 'expected': None},
     {'args': [[3, 8], 10], 'expected': None},
     {'args': [[1], 2], 'expected': None},
     {'args': [[1], 3], 'expected': [2.1491257999070625, 0.7163752666356875]},
     {'args': [[49], 100], 'expected': [0.12002881086621887, 0.0012002881086621887]},
     {'args': [[1], 1000000000000], 'expected': [1000000000000.0, 1.0]},
     {'args': [[499999999999], 1000000000000], 'expected': [1.2e-11, 1.2e-23]},
     {'args': [[499999999999], 999999999999], 'expected': [6.000000000006e-12, 6.000000000012e-24]},
     {'args': [[1, 4, 9], 10], 'expected': [0.4010711571941434, 0.04010711571941434]},
     {'args': [[1, 1, 1, 9], 10], 'expected': [2.6721038552733853, 0.26721038552733856]},
     {'args': [[1, 1], 4], 'expected': [3.5935119694474262, 0.8983779923618566]},
     {'args': [[2, 4, 6], 16], 'expected': [3.5935119694474262, 0.22459449809046414]}]
    tests.append({'args':[[3,1,2]*1000,8],'expected':[3.5935119694474262, 0.4491889961809283]})
    exercise('Hard','Fit the waits a selection rule retained',
        r'Underlying waits are iid Exponential(λ), λ>0. A fixed export rule retains only exact completed waits shorter than cutoff c. No rejected-subject count is available. waits is a list of at most 100000 integer durations, each strictly between zero and integer cutoff, with \(2\leq\text{cutoff}\leq10^{12}\). Treat the supplied durations as exact density-evaluation values, NOT rounded bins. Fit the CONDITIONAL distribution of retained waits, with retained sample size held fixed.\n\nReturn [scaled_rate, rate], where scaled_rate is \(z=\hat\lambda c\) and rate is \(\hat\lambda\) per input time unit. Return None when the data do not determine a unique finite positive-rate MLE: empty waits, or retained mean at least c/2. Do not return zero as an attained MLE. Do not mutate waits, simulate or round. Aim for O(n) data work plus a bounded one-dimensional root solve, with O(1) auxiliary state. Tiny positive roots and scaled rates up to 10^12 are valid; guard both cancellation near the uniform limit and exponential overflow. The editorial derives a bracket, monotonicity and a stable small-root expansion. No external numerical package is needed.',
        'def solve(waits, cutoff):',
        [{'args':[[1,2,3],8],'expected':[3.5935119694474262, 0.4491889961809283]},
         {'args':[[5,7],10],'expected':None}],tests,
        '''from math import expm1
def solve(waits, cutoff):
    n = len(waits)
    if n == 0:
        return None
    total = sum(waits)
    exposure = n * cutoff
    gap = exposure - 2 * total
    if gap <= 0:
        return None
    mean = total / exposure
    delta = gap / (2 * exposure)
    low, high = 0.0, exposure / total
    for _ in range(120):
        z = (low + high) / 2
        if z < 0.01:
            squared = z * z
            departure = z * (1/12 + squared * (-1/720 + squared * (1/30240 - squared/1209600)))
            increase = departure < delta
        else:
            conditional_mean = 1/z - (1/expm1(z) if z < 50 else 0.0)
            increase = conditional_mean > mean
        if increase:
            low = z
        else:
            high = z
    z = (low + high) / 2
    return [z, z / cutoff]''',
        r'Retention has probability \(1-e^{-\lambda c}\). The correct conditional density on (0,c) is \(\lambda e^{-\lambda x}/(1-e^{-\lambda c})\); its normaliser depends on λ. Let \(r=\sum_i x_i/(nc)\) and \(z=\lambda c\). The score vanishes precisely when\n\n\[g(z)=\frac1z-\frac1{e^z-1}=r.\]\n\nThe conditional mean g strictly decreases from 1/2 to zero; its derivative is minus the variance of the normalised duration under the exponentially tilted bounded distribution. Thus r<1/2 gives exactly one finite positive root. If r≥1/2, the likelihood decreases throughout the open rate domain and only approaches a uniform limit at zero, so return None. Empty data give a flat likelihood and no unique estimate. Check \(nc-2\sum_i x_i\) as an INTEGER before division, preserving the existence decision near equality.\n\nFor a positive root, \(0<z<1/r\), because g(z)<1/z. Bracket and bisect this monotone equation. Using expm1 preserves e^z−1, but subtracting its reciprocal from 1/z still loses precision for tiny z. Near zero instead compare \(h(z)=1/2-g(z)\) with \(\delta=(nc-2\sum_i x_i)/(2nc)\), computed from the exact integer gap. Expanding the exponential and dividing its series gives\n\n\[h(z)=\frac z{12}-\frac{z^3}{720}+\frac{z^5}{30240}-\frac{z^7}{1209600}+O(z^9).\]\n\nBelow z=0.01 the omitted leading term is about 2.1×10^(-26), safely smaller than the required numerical tolerance. Away from zero compare g directly with r; for z≥50, its exponential correction is less than 2×10^(-22), so omit it to avoid overflow. Keep the lower bracket when the modeled mean is too large, otherwise the upper. Since r≥1/c≥10^(-12), the initial bracket is at most 10^12 wide. After 120 halvings its exact width is below 10^(-24); floating-point arithmetic eventually limits further improvement. Return z and z/c to separate the scaled fitting problem from rate units. The solver uses one count/sum pass and constant root iterations, O(n) time/O(1) auxiliary state. This is the selected-sample model; a known number of rejected subjects would contribute censored exposure and yield a different fit.')
