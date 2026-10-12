"""Monte Carlo design, honest precision and exact discrete allocation."""


def add_questions(add,questions):
    for q in questions:
        if q['id']=='q43':
            q['rubric']=['Preserve uniform marginals and target mean, and compute both fourth and product moments.', 'Derive covariance −7/90, pair variance 1/180 and equal-two-evaluation independent variance 2/45.', 'Use independent pairs for uncertainty and give a symmetric-function counterexample to automatic improvement.']
        elif q['id']=='q48':
            q['prompt']=q['prompt'].replace('assuming Var(X)>0.','assuming finite second moments and Var(X)>0.')
            q['solution']=q['solution'].replace('Substitution gives Var(Y)(1−Corr(X,Y)²).','Substitution gives Var(Y)−Cov(X,Y)²/Var(X). If Var(Y)>0 this equals Var(Y)(1−Corr(X,Y)²); if Var(Y)=0 the minimum is zero and correlation is undefined.')
            q['rubric']=['Expand the fixed-coefficient variance under finite second moments and known control mean.', 'Derive c*=Cov(X,Y)/Var(X) and the general residual variance, treating constant Y without undefined correlation.', 'Prove fixed/independent-pilot unbiasedness and separate it from fitting on the same main sample.']

    def question(suffix,title,level,minutes,prompt,answer,hints,solution,follow,follow_solution,rubric):
        add('q_l17_'+suffix,title,'Simulation',level,'researcher',minutes,prompt,answer,hints,solution,follow,follow_solution,'l17')
        questions[-1]['rubric']=rubric
        for key in ('prompt','solution','followSolution'):
            questions[-1][key]=questions[-1][key].replace(r'\n\n','\n\n')

    question('e1','Count independently drawn pairs','Easy',6,
        r'A simulation makes 512 function evaluations grouped into 256 pairs. Different pairs are independently sampled, while the two evaluations within a pair may be dependent. The 256 pair AVERAGES have sample variance 36 in squared payoff units. What is the estimated standard error of the mean of those pair averages? Use the usual sample-variance-over-independent-unit-count formula.',3/8,
        ['The independent sample count is 256, not 512.', 'The standard deviation of pair averages is six.'],
        r'The estimated variance of the mean is 36/256, so estimated standard error is 6/16=3/8 payoff unit. The covariance inside a pair has already influenced the variance of its average. Dividing that pair variance by 512 would pretend there were twice as many independently sampled pair averages. This is an estimated Monte Carlo precision for the chosen design; it does not certify the underlying model or the closeness of this one realized estimate.',
        r'Under the planning assumption that pair variance remains unchanged, how many independent pairs and function evaluations are needed to halve the standard error? Would copying each saved pair count as new sampling?',
        r'Standard error scales as the inverse square root of the independent pair count. Halving it needs four times the count: 1024 independent pairs and 2048 evaluations under the stated two-evaluation cost. Copies reuse the same randomness and do not reduce uncertainty. The future sample variance need not be exactly 36; the fourfold rule is the planning comparison under a stable variance assumption.',
        ['Identify 256 independent units and obtain 3/8 payoff unit.', 'Explain why within-pair dependence is incorporated before the count division.', 'Give 1024 pairs/2048 evaluations and reject duplicated records as new draws.'])

    question('e2','Compare variance at the same evaluation cost','Easy',8,
        r'Each output has the same mean theta and variance 4. A paired construction preserves both marginals and gives covariance −3 between its two outputs. Different pairs are independent. You can afford exactly 2000 function evaluations: either 1000 such pairs, averaged through their pair averages, or 2000 independent single outputs. What is the ratio of the PAIRED estimator variance to the independent estimator variance? Each evaluation has equal cost and pairing has no extra cost in this toy.',1/4,
        ['The variance of (Y1+Y2)/2 contains twice the covariance before division by four.', 'Divide the pair variance by 1000 and the single-output variance by 2000.'],
        r'One pair average has variance (4+4+2(−3))/4=1/2 and mean theta. Across 1000 independent pair averages the estimator variance is 1/2000. Across 2000 independent singles it is 4/2000=1/500. The variance ratio is one quarter; the standard-error ratio is one half. Counting pairs as 2000 independent units would exaggerate the gain. Equal marginals preserve the target; the covariance and cost determine this comparison.',
        r'Keep each marginal variance at four but change the pair covariance to +4. What is the equal-cost variance ratio? Why does a negative covariance alone not settle a comparison with a differently priced algorithm?',
        r'At covariance +4 the two centered outputs coincide almost surely, because their difference has zero variance. The pair-average variance is four, giving 4/1000 compared with 4/2000 for singles: ratio two. Its second evaluation repeats the same noise. With unequal costs, compare estimator variance at a common total computational budget; an expensive construction can use fewer independent units. Covariance alone describes variance per pair, not variance per unit of time or money.',
        ['Compute pair variance 1/2 and budget-matched estimator variances.', 'Obtain variance ratio 1/4 and distinguish it from standard-error ratio 1/2.', 'Derive the positive-covariance ratio two and name the needed cost comparison.'])

    question('m1','No rare-event hits is not zero uncertainty','Medium',22,
        r'Before sampling, fix n independent Bernoulli simulation trials with unknown event probability p. You observe K=0 events. The empirical event rate and its plug-in standard error are both zero. Derive a one-sided 95-percent upper bound u_n from the probability of zero hits, and prove coverage of this complete confidence rule: report [0,u_n] when K=0, and [0,1] otherwise. Compute u_1000 approximately, and the smallest integer n for which u_n≤0.001. Use alpha=0.05; include the endpoints. This is a deliberately conservative rule for nonzero K, not a claim that the observed event probability has a posterior distribution.',None,
        [r'For a fixed n, \(P_p(K=0)=(1-p)^n\).', 'Invert the zero-hit probability at alpha, and check the event on which the interval misses the true p.', 'Take logarithms carefully: log(0.999) is negative.'],
        r'Solve (1−u_n)^n=alpha, giving\n\n\[u_n=1-\alpha^{1/n}.\]\n\nIf p≤u_n, the reported interval always covers p. If p>u_n, the only possible miss is K=0, with probability (1−p)^n<alpha. Thus unconditional coverage is at least 95 percent at every p. Equality p=u_n is covered because the interval is closed. The statement concerns repetitions of the fixed-n procedure, not a 95-percent posterior probability after seeing zero.\n\nFor n=1000, u_n is approximately 0.00299125. The requirement u_n≤0.001 is equivalent to n≥log(0.05)/log(0.999), approximately 2994.234. Hence the smallest integer count is 2995. A zero sample variance reflects no observed variation in that finite sample; it does not rule out unobserved rare losses. Monte Carlo error, rare-event support and model error remain separate.',
        r'Instead inspect independent blocks of 2995 trials repeatedly until the FIRST all-zero block appears, then report the same upper bound. For a fixed p strictly between 0.001 and one, what is the chance that this procedure eventually reports an interval missing p? Would relabeling these dependent/adaptively selected trials as a fixed run repair coverage?',
        r'Each independent block is all-zero with positive probability (1−p)^2995. The probability of never seeing such a block after M blocks is [1−(1−p)^2995]^M, which tends to zero. Eventually an all-zero block appears almost surely, and its reported upper bound is below p. The eventual miscoverage probability is therefore one. A fixed sample count and one pre-specified inspection were part of the original coverage proof. Optional repetition/selection changes the reporting procedure; an appropriate sequential bound or a pre-specified error budget would require a new proof. Mere relabeling cannot make selected evidence fixed or independent.',
        ['Invert the fixed-n zero-hit tail to 1−alpha^(1/n).', 'Prove unconditional coverage for the stated complete rule, including boundary p=u_n.', 'Compute about 0.00299125 and minimum count 2995 without treating zero plug-in error as certainty.', 'Show almost-sure eventual miscoverage under repeated-block selection and explain which design assumption changed.'])

    question('m2','A coefficient fitted on two draws can bias the mean','Medium',23,
        r'The control C is uniform on {0,1,2}, with KNOWN mean one; target output is Y=C² and target expectation is 5/3. Draw C1,C2 independently. If C1 differs from C2, fit the secant coefficient c=(C1²−C2²)/(C1−C2)=C1+C2; if they coincide, set c=0. Report \(T=(C_1^2+C_2^2)/2-c((C_1+C_2)/2-1)\) using THESE SAME two draws. What is E[T]? Decide whether the known control mean alone guarantees unbiasedness here. All nine ordered pairs are equally likely.',13/9,
        ['Separate the equal-control branch from the secant-fit branch.', 'For unequal a,b, simplify the adjusted estimate to a+b−ab.', 'Average all nine ordered outcomes, retaining their multiplicities.'],
        r'The ordered-pair estimates, in row order C1=0,1,2 and column order C2=0,1,2, are\n\n\[\begin{pmatrix}0&1&2\\1&1&1\\2&1&4\end{pmatrix}.\]\n\nTheir sum is 13, so E[T]=13/9, with bias −2/9 relative to 5/3. Although the control sample mean minus one has mean zero, the fitted c is dependent on it. One cannot factor E[c(Cbar−1)] into the product of means. The coefficient was chosen to fit the same random observations whose average is then corrected. The explicit equal-draw convention matters: silently dividing by zero or discarding that branch changes the procedure.',
        r'Fit c by the SAME rule on a separate independent two-draw pilot, then freeze it and use TWO fresh main draws. Derive the main estimator’s unconditional mean and variance. Compare that variance with using the fixed population-optimal coefficient. Does a random independent pilot require adding a separate variance of its conditional mean?',
        r'Pilot c has probability 1/3 of zero and probability 2/9 each of one, two and three. Thus E[c]=4/3 and E[c²]=28/9. For the main law, Var(C)=2/3, Var(Y)=26/9 and Cov(C,Y)=4/3. Conditional on the pilot, the adjusted MAIN mean is always 5/3. Total variance therefore averages the conditional main variance with no extra conditional-mean term:\n\n\[\begin{aligned}\operatorname{Var}(T_{\mathrm{pilot}})&=\frac12\left(\frac{26}{9}+\frac{28}{9}\frac23-2\frac43\frac43\right)\\&=\frac{19}{27}.\end{aligned}\]\n\nThe fixed optimum is c*=2, giving one-output variance 2/9 and two-draw mean variance 1/9. The noisy pilot remains unbiased but has larger variance than that optimum. Its unconditional excess is (Var(C)/2)E[(c−2)²]=16/27. There is no separate Var(E[T|pilot]) contribution here because that conditional expectation is the same constant 5/3 for every pilot. Conditional main-sample uncertainty still needs to use the actual adjusted outputs. This argument fixes the sampling design; selecting a coefficient or estimator by its flattering main result would be another procedure.',
        ['Retain all nine ordered pairs and the c=0 tie convention to obtain E[T]=13/9.', 'Identify the forbidden factorization behind a false unbiasedness claim.', 'Condition on an independent pilot to restore mean 5/3.', 'Derive pilot moments and variance 19/27, compare optimum 1/9 and explain the zero conditional-mean variance term.'])


def add_coding(add,tasks):
    def exercise(level,title,prompt,signature,samples,tests,reference,explanation):
        add('c_l17_'+level.lower(),title,level,'Simulation',prompt,signature,samples,tests,reference,explanation)
        tasks[-1]['path']='researcher'
        for key in ('prompt','explanation'):
            tasks[-1][key]=tasks[-1][key].replace(r'\n\n','\n\n')

    exercise('Easy','Estimate uncertainty from independent pair averages',
        r'pairs is a list of [left_output,right_output] from independently drawn pairs; dependence WITHIN each pair is allowed. Both entries are integers in [−10^9,10^9], and there are at most 100000 pairs. For A_i=(left_i+right_i)/2, return [mean(A),estimated_standard_error_of_mean]. With n≥2 use \(\sqrt{\sum_i(A_i-\bar A)^2/[n(n-1)]}\); one pair returns [its average,None], and empty input returns [None,None]. Defined outputs are ordinary finite floats. Preserve the input. Use O(n) time and O(1) auxiliary accumulators, with integer arithmetic bit costs additional. Large offsets with small variation are allowed: do not lose variation by subtracting rounded floating second moments. Pair totals are integers and may be accumulated exactly before converting the final result. The formula audits the declared independent-pair design, not model correctness or rare-event coverage.',
        'def solve(pairs):',
        [{'args':[[[0,2],[2,4]]],'expected':[2.,1.]}, {'args':[[[0,2],[2,0],[1,1]]],'expected':[1.,0.]}, {'args':[[[7,-2]]],'expected':[2.5,None]}],
        [{'args':[[]],'expected':[None,None]}, {'args':[[[10**9,10**9]]*4000],'expected':[float(10**9),0.]}, {'args':[[[10**9,10**9],[10**9-1,10**9]]],'expected':[10**9-.25,.25]}, {'args':[[[-10**9,10**9],[0,0]]],'expected':[0.,0.]}, {'args':[[[ -2,-2],[2,2]]],'expected':[0.,2.]}, {'args':[[[0,0],[1,1],[2,2]]],'expected':[1.,(1/3)**.5]}],EASY_REFERENCE,
        r'Use z_i=left_i+right_i, so A_i=z_i/2. Accumulate the INTEGER sum S and square sum Q. For n≥2 the exact variance numerator nQ−S² is nonnegative, and\n\n\[\widehat{\mathrm{SE}}^2=\frac{nQ-S^2}{4n^2(n-1)}.\]\n\nConvert only the final mean S/(2n) and nonnegative variance ratio to floats. This algebra avoids catastrophic cancellation from large floating second moments. The denominator counts n independently drawn pairs, not 2n dependent component outputs. A singleton has a defined mean but insufficient units for this sample-variance estimate; an empty run has neither. One linear scan and integer accumulators leave the source list unchanged.')

    exercise('Hard','Allocate a fixed simulation budget exactly',
        r'weights and variances are equal-length lists for k simulation strata, 1≤k≤20000. Weights are integers in [0,10^9] with positive total W; population weights are p_h=weights_h/W. Variances are KNOWN nonnegative integer within-stratum output variances, at most 10^9. Each draw costs one budget unit. Draws are independent both within and across strata, sampled WITH replacement. Before main sampling choose integer n_h≥1 in EVERY declared stratum, even a zero-weight or zero-variance stratum, with sum(n_h)=budget. budget is an integer k≤budget≤200000. The stratified estimator is the sum of p_h times that stratum’s sample mean, with variance \(\sum_h p_h^2\sigma_h^2/n_h\).\n\nFind a globally minimum-variance allocation. Among all optima choose the LEXICOGRAPHICALLY LARGEST allocation in original stratum order (at the first differing index, prefer the larger count). Return {"allocation": [integer counts in input order], "variance": [exact_reduced_numerator_text,positive_denominator_text]}. The variance pair uses canonical decimal STRINGS; zero is ["0","1"]. Preserve all inputs. Aim for O(k+(budget−k)log(k+1)) exact comparisons plus O(k) rational-accumulation steps, and O(k) storage. Integer multiplication/gcd bit costs are additional. Do not rescan every stratum for every extra draw or round a continuous allocation. Nearly equal marginal gains can differ by one at sizes beyond floating precision.\n\nPrerequisite: a binary priority heap. The variance DROP from increasing n to n+1 in stratum h is \(p_h^2\sigma_h^2/[n(n+1)]\). Explain why choosing by current marginal drop is globally valid under this equal-cost, fixed-variance contract. Allocations chosen from changing estimated variances, unequal costs, dependent draws or a finite population without replacement require a different analysis.',
        'def solve(weights, variances, budget):',HARD_SAMPLES,HARD_CASES,HARD_REFERENCE,
        r'Let a_h=weights_h²·variances_h. The common W² cancels from comparisons. Start with one sample per stratum. Each stratum offers a decreasing stream of gains a_h/[n(n+1)] for successive extra samples. Maximizing total variance reduction chooses the largest budget−k gains across these streams. Such a selection is prefix-feasible: every gain’s preceding gain in its stratum is at least as large. A priority heap of the next available gain therefore yields a GLOBAL optimum, not just a locally good step.\n\nAt a positive threshold each nonzero stream is strictly decreasing, so it can have at most one tied threshold gain. Award those tied draws to smaller original indices to obtain the lexicographically largest optimum. If all a_h are zero, every allocation is optimal and all extras go to index zero. Zero-benefit strata otherwise keep their required single draw. The reference compares gains by exact cross multiplication and stores only stratum indices and current counts. Updating the root decreases its priority, so one downward heap repair is enough; no unsupported custom comparator class is needed in the restricted runner. Building the heap bottom-up is O(k).\n\nFinally sum exact rationals a_h/n_h, divide by W² and reduce. Use gcd while accumulating so denominators do not grow by unnecessary repeated factors. The reference performs O(k) rational updates; their bit cost depends on the resulting denominators. The continuous solution’s proportionality to p_h·sigma_h is useful intuition, but its rounding need not select the best integer allocation or honor mandatory counts and exact ties. Known population variances and fixed counts support the stated estimator variance; the arithmetic does not certify a pilot estimate of those variances.')


EASY_REFERENCE='''from math import sqrt
def solve(pairs):
    n = len(pairs)
    if not n:
        return [None,None]
    total = squares = 0
    for left,right in pairs:
        z = left+right
        total += z
        squares += z*z
    mean = total/(2*n)
    if n == 1:
        return [mean,None]
    variance_of_mean = (n*squares-total*total)/(4*n*n*(n-1))
    return [mean,sqrt(variance_of_mean)]'''

HARD_REFERENCE='''from math import gcd
def solve(weights, variances, budget):
    k = len(weights)
    gains = [w*w*v for w,v in zip(weights,variances)]
    counts = [1]*k
    denominators = [2]*k
    heap = list(range(k))
    def better(i,j):
        left = gains[i]*denominators[j]
        right = gains[j]*denominators[i]
        return left > right or (left == right and i < j)
    def sift(position):
        item = heap[position]
        while 2*position+1 < k:
            child = 2*position+1
            if child+1 < k and better(heap[child+1],heap[child]):
                child += 1
            if not better(heap[child],item):
                break
            heap[position] = heap[child]
            position = child
        heap[position] = item
    for position in range(k//2-1,-1,-1):
        sift(position)
    for _ in range(budget-k):
        chosen = heap[0]
        counts[chosen] += 1
        denominators[chosen] = counts[chosen]*(counts[chosen]+1)
        sift(0)
    numerator,denominator = 0,1
    for a,n in zip(gains,counts):
        common = gcd(denominator,n)
        numerator = numerator*(n//common)+a*(denominator//common)
        denominator *= n//common
        reduce = gcd(numerator,denominator)
        numerator //= reduce
        denominator //= reduce
    denominator *= sum(weights)**2
    reduce = gcd(numerator,denominator)
    return {"allocation":counts,
            "variance":[str(numerator//reduce),str(denominator//reduce)]}'''

HARD_SAMPLES=[
    {'args':[[1,2],[1,1],5],'expected':{'allocation':[2,3],'variance':['11','54']}},
    {'args':[[1,1],[1,1],3],'expected':{'allocation':[2,1],'variance':['3','8']}},
    {'args':[[0,2,1],[9,0,4],5],'expected':{'allocation':[1,1,3],'variance':['4','27']}},
]
HARD_CASES=[
    {'args':[[1,2,3],[0,0,0],9],'expected':{'allocation':[7,1,1],'variance':['0','1']}},
    {'args':[[5],[7],4],'expected':{'allocation':[4],'variance':['7','4']}},
    {'args':[[1,2],[1,1],2],'expected':{'allocation':[1,1],'variance':['5','9']}},
    {'args':[[1,1,1],[1,1,1],5],'expected':{'allocation':[2,2,1],'variance':['2','9']}},
    {'args':[[1]*20000,[1]*20000,200000],'expected':{'allocation':[10]*20000,'variance':['1','200000']}},
]

# Pell identity separates the two gains by exactly one; exact two-choice comparison.
HARD_CASES += [{'args': [[543339720, 768398401], [2, 1], 3], 'expected': {'allocation': [1, 2], 'variance': ['1771308307978070401', '3441313796169221282']}}]
