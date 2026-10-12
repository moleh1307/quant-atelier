"""l07: marginal variability, joint feasibility and overlapping records."""


def add_questions(add, questions):
    def question(suffix, title, level, minutes, prompt, answer, hints,
                 solution, follow, follow_answer, rubric):
        add(f'q_l07_{suffix}', title, 'Variance and dependence', level, 'shared',
            minutes, prompt, answer, hints, solution, follow, follow_answer, 'l07')
        questions[-1]['rubric'] = rubric

    question('e1', 'Two random variables, one constant sum', 'Easy', 4,
        r'X is zero or one with probability 1/2 each. Set Y=1-X using that same draw, rather than making a second draw. What is \(\operatorname{Var}(X+Y)\)? Reconcile the answer with \(\operatorname{Var}(X)=\operatorname{Var}(Y)=1/4\).',
        0,
        ['List the only two possible joint records.',
         'The variance-of-a-sum formula includes two covariance terms.'],
        r'The only records are (0,1) and (1,0), each of probability 1/2. Their sum is always one, so its variance is zero. Also E[XY]=0 and E[X]E[Y]=1/4, giving covariance -1/4. Hence \(\operatorname{Var}(X+Y)=1/4+1/4+2(-1/4)=0\). Adding marginal variances alone would assert zero covariance, which this shared-draw construction does not have.',
        'What would change if Y instead came from a second independent fair zero/one draw?',
        r'Both margins would be unchanged, but the four joint records would each have probability 1/4. Covariance would be zero and the sum variance 1/2. Marginal distributions do not determine the distribution of a sum; the joint construction matters.',
        ['Identify the constant sum from the two permitted joint records.',
         'Compute covariance -1/4 and its doubled contribution.',
         'Distinguish the shared draw from independent draws with the same margins.'])

    question('m1', 'Zero covariance still allows a nonlinear link', 'Medium', 8,
        r'X takes -1, 0 and 1 with equal probabilities, and Y=X^2. What is \(\operatorname{Var}(X+Y)\)? Compute the covariance as part of your reasoning, and decide whether X and Y are independent.',
        8/9,
        ['Use symmetry for E[X] and E[XY]=E[X^3].',
         'Check the distribution of X+Y directly as a separate verification.'],
        r'E[X]=0 and E[X^2]=2/3, so Var(X)=2/3. Y is one with probability 2/3 and zero with probability 1/3, hence Var(Y)=2/9. Since E[XY]=E[X^3]=0, covariance is zero. The sum variance is \(2/3+2/9=8/9\). Directly, X+Y is zero with probability 2/3 and two with probability 1/3, yielding \(E[(X+Y)^2]-E[X+Y]^2=4/3-(2/3)^2=8/9\). Zero covariance permits this addition of variances, but does not make the variables independent: observing Y=0 determines X=0, whereas marginally X=0 has probability 1/3.',
        'Does knowing Y reveal the sign of a nonzero X? How can strong dependence coexist with zero correlation?',
        r'If Y=1, the sign remains equally likely positive or negative. The nonlinear observation reveals magnitude, not sign. The positive and negative products of centered deviations cancel in covariance. Correlation measures linear co-movement when variances are positive; it cannot summarize every kind of dependence.',
        ['Compute marginal means and variances explicitly.',
         'Use symmetry to get zero covariance and obtain sum variance 8/9.',
         'Give a conditional-probability counterexample to independence.'])

    question('h1', 'Overlap can create negative and positive covariance', 'Hard', 18,
        r'Flip a fair coin independently 20 times. C counts occurrences of the contiguous pattern HTH, including overlaps: each starting position from 1 through 18 contributes an indicator. What is \(\operatorname{Var}(C)\)? Classify overlapping pairs by their distance between starting positions, instead of treating C as binomial.',
        31/16,
        ['Every HTH indicator has success probability 1/8.',
         'At a distance of one, the two required patterns conflict; at distance two they share a consistent H.',
         'Count unordered pairs at each distance and double their covariance contribution.'],
        r'Each of the 18 indicators has variance \((1/8)(7/8)=7/64\). Two starts one apart would require the shared second flip to be both T and H, so their joint probability is zero and covariance -1/64. There are 17 such pairs. Two starts two apart require H T H T H, whose probability is 1/32; covariance is \(1/32-1/64=1/64\). There are 16 such pairs. At distances at least three the windows use disjoint independent flips, hence zero covariance. Therefore \[\operatorname{Var}(C)=18\frac7{64}+2(17)\left(-\frac1{64}\right)+2(16)\frac1{64}=\frac{31}{16}.\] The mean is 18/8=9/4 by linearity, but that mean does not make the count binomial. The doubled pair sums account for each cross term exactly once.',
        'Replace HTH by HHT while keeping the same 20 flips. The mean stays the same. Does the variance?',
        r'No. HHT conflicts with itself at both overlapping distances one and two. Both joint probabilities are zero, so both covariances are -1/64. Thus the variance becomes \((126-34-32)/64=15/16\). Equal window probabilities and equal means do not specify the overlap covariances. Negative overlap dependence can reduce the variance, rather than merely increasing it.',
        ['Derive covariance -1/64 at distance one and +1/64 at distance two.',
         'Count 18 variances, 17 adjacent pairs and 16 distance-two pairs.',
         'Use the doubled pair contributions to get 31/16 and reject the binomial shortcut.'])

    question('h2', 'A plausible pairwise number can be collectively impossible', 'Hard', 19,
        r'Five centered random variables each have variance one. A proposed model gives every distinct pair correlation -3/10. Show that the joint model is impossible, derive the full feasible interval of a common correlation rho for five such variables, and prove the lower boundary is attainable by constructing a joint model. You may begin with five independent centered variance-one variables Z_i; their distributions need not be normal.',
        None,
        ['A proposed variance of a sum must be nonnegative.',
         'A variance of a difference supplies the upper bound.',
         'Subtract the average of the Z_i from each variable, then restore unit marginal variance.'],
        r'The proposed sum variance is \(5+20(-3/10)=-1\), impossible for a variance. More generally it is \(5+20\rho\), so rho>=-1/4. A difference has variance \(2-2\rho\), so rho<=1. To attain the lower bound, set \[X_i=\sqrt{5/4}\,(Z_i-\bar Z),\qquad\bar Z=\tfrac15\sum_{j=1}^5Z_j.\] Independence and unit variance give Var(Z_i−Zbar)=4/5 and Cov(Z_i−Zbar,Z_j−Zbar)=-1/5 for i!=j. The scale restores marginal variance one and gives each correlation -1/4. The centered sum is identically zero. The upper bound is attained by making all X_i equal to one centered variance-one variable. Every intermediate correlation is attainable: independently combine the lower-bound construction Y_i with a common shock Z as \(X_i=\sqrt{\alpha}Z+\sqrt{1-\alpha}Y_i\), for alpha in [0,1]. This keeps each variance one and yields \(\rho=\alpha-(1-\alpha)/4\). Thus the bounds are sufficient as well as necessary; merely checking that each correlation lies in [-1,1] is insufficient.',
        'Can the lower-bound five-variable construction be extended to six variables while retaining variance one and the same common correlation -1/4?',
        r'No. Six variables would give sum variance \(6+30(-1/4)=-3/2\). The general lower bound is \(-1/(n-1)\), so the feasible correlation depends on collection size. A valid joint construction for five cannot be extended arbitrarily while preserving all its pair correlations.',
        ['Reject the proposed model using the negative sum variance.',
         'Derive both common-correlation bounds and calculate the centered-noise construction.',
         'Verify unit marginal variances, boundary correlations and attainability of the whole interval.'])


def add_coding(add, tasks):
    def exercise(level, title, prompt, signature, samples, tests, solution, explanation):
        add(f'c_l07_{level.lower()}', title, level, 'Variance and dependence', prompt,
            signature, samples, tests, solution, explanation)
        tasks[-1].update(path='shared', lesson='l07')

    exercise('Easy', 'Variance from the actual joint records',
        r'joint is a nonempty list of [x,y,probability] records for a joint distribution. Probabilities are nonnegative and sum to one; duplicate records and zero-mass records are allowed. a and b are fixed numeric weights. Return \([E[Z],\operatorname{Var}(Z)]\) for Z=aX+bY under this joint distribution. Do not assume independence from the margins. There are at most 10000 records; |x|, |y|<=1000 and |a|, |b|<=100. All inputs are finite. Compute population variance about the distribution mean, without a sample n-1 denominator. Do not simulate, round or mutate joint.',
        'def solve(joint, a, b):',
        [{'args': [[[0,1,.5],[1,0,.5]],1,1], 'expected': [1,0]},
         {'args': [[[0,0,.25],[0,1,.25],[1,0,.25],[1,1,.25]],1,1], 'expected': [1,.5]}],
        [{'args': [[[3,-2,1]],2,-1], 'expected': [8,0]},
         {'args': [[[0,0,.5],[1,1,.5]],1,1], 'expected': [1,1]},
         {'args': [[[0,0,.25],[1,1,.75]],1,-1], 'expected': [0,0]},
         {'args': [[[-1,1,.25],[0,0,.5],[1,1,.25]],1,1], 'expected': [.5,.75]},
         {'args': [[[1,2,.25],[1,2,.25],[-1,0,.5],[100,100,0]],2,-1], 'expected': [-1,1]},
         {'args': [[[7,8,1]],0,0], 'expected': [0,0]}],
        '''import math
def solve(joint, a, b):
    mean = math.fsum((a*x+b*y)*p for x,y,p in joint)
    variance = math.fsum((a*x+b*y-mean)**2*p for x,y,p in joint)
    return [mean, variance]''',
        r'Each joint record determines one realised weighted sum. Compute its probability-weighted mean, then the mean squared deviation about that mean. This uses the actual coupling and automatically includes covariance. Two identical margins can produce a constant sum, an independent sum or perfectly reinforced movement; their joint records distinguish them. The centered second pass avoids subtracting two nearly equal raw moments. Duplicate records simply contribute their masses separately. This is a distribution variance, so no sample correction is used. Two linear scans give O(r) time and O(1) working space for r records.')

    exercise('Hard', 'Variance of a pattern count without generating the flips',
        r'An iid coin is flipped n times. pattern is a nonempty H/T string of length k<=100. Heads has exact rational probability heads/total, with integer 2<=total<=100 and 1/10<=heads/total<=9/10. Return \([E[C],\operatorname{Var}(C)]\), where C counts every occurrence of pattern in consecutive k-flip windows, including overlaps. n is an integer from 0 to 10^12; return [0,0] when n<k. Do not simulate, enumerate flip sequences, iterate through n windows, or treat their indicators as independent. Use overlap compatibility and the number of pairs at each distance. Aim for O(k) character comparisons using border/failure links and O(k) working storage; account separately for exact-integer arithmetic. Return floats without rounding.',
        'def solve(n, pattern, heads, total):',
        [{'args': [20,'HTH',1,2], 'expected': [9/4,31/16]},
         {'args': [20,'HHT',1,2], 'expected': [9/4,15/16]}],
        [{'args': [0,'H',1,2], 'expected': [0,0]},
         {'args': [2,'HTH',1,2], 'expected': [0,0]},
         {'args': [3,'HTH',1,2], 'expected': [1/8,7/64]},
         {'args': [4,'HTH',1,2], 'expected': [1/4,3/16]},
         {'args': [10,'HH',1,2], 'expected': [9/4,43/16]},
         {'args': [10,'H',1,4], 'expected': [5/2,15/8]},
         {'args': [5,'HT',1,4], 'expected': [3/4,51/128]},
         {'args': [10**12,'HT',1,2], 'expected': [(10**12-1)/4,(10**12+1)/16]},
         {'args': [10**12,'HHH',1,2], 'expected': [(10**12-2)/8,(15*10**12-40)/64]},
         {'args': [102,'H'*100,1,2], 'expected': [3/2**100, (11*2**99-9)/2**200]}],
        '''import math
def solve(n, pattern, heads, total):
    k = len(pattern)
    windows = n-k+1
    if windows <= 0:
        return [0,0]
    prefix = [0]*k
    for i in range(1,k):
        j = prefix[i-1]
        while j and pattern[i] != pattern[j]:
            j = prefix[j-1]
        if pattern[i] == pattern[j]:
            j += 1
        prefix[i] = j
    suffix_probabilities = [1.0]
    numerator = denominator = 1
    for symbol in reversed(pattern):
        numerator *= heads if symbol == 'H' else total-heads
        denominator *= total
        suffix_probabilities.append(numerator/denominator)
    probability = suffix_probabilities[k]
    max_lag = min(k-1,windows-1)
    pair_count = max_lag*windows - max_lag*(max_lag+1)//2
    terms = [windows*probability*(1-probability),
             -2*pair_count*probability**2]
    border = prefix[-1]
    while border:
        lag = k-border
        if lag <= max_lag:
            joint = probability*suffix_probabilities[lag]
            terms.append(2*(windows-lag)*joint)
        border = prefix[border-1]
    return [windows*probability,math.fsum(terms)]''',
        r'Let m=n-k+1 and q be the full-pattern probability. Every indicator has mean q and variance q(1-q). Starts separated by at least k use disjoint flips and have zero covariance. At a shorter distance d, two patterns can occur together exactly when pattern[d:] equals pattern[:-d]; this is a border of length k-d. If compatible, their union requires the first pattern followed by its last d symbols, so the joint probability is q times that suffix probability. If incompatible it is zero. With D=min(k-1,m-1), there are m-d unordered pairs at distance d. Hence \[\operatorname{Var}(C)=mq(1-q)+2\sum_{d=1}^D(m-d)(P(I_0=I_d=1)-q^2).\] Sum the negative q² contribution for all these pairs using \(\sum_{d=1}^D(m-d)=Dm-D(D+1)/2\), then add joint mass only at compatible lags. The prefix function stores the longest proper border of each prefix; following its links visits every compatible overlap. Backward exact-integer products give the suffix probabilities before float conversion. This takes O(k) character operations and O(k) storage without depending on the number of flips; integer operands have O(k log total) bits. For k=1 there are no overlapping pairs and the binomial variance is valid. For HTH, distance one contributes negative covariance and distance two positive covariance. math.fsum combines the signed contributions, so a loss of precision in raw cancellation is reduced.')
