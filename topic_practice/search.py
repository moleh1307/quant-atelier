"""Original practice on selection, dependence and exact family calibration."""


def add_questions(add, questions):
    for q in questions:
        if q['id'] == 'q04':
            q['rubric'] = ['Condition on the declared useful/useless population and construct both passing masses.', 'Normalize 0.018 by 0.116 to obtain 9/58, distinguishing sensitivity from posterior usefulness.', 'For repeated screens state conditional independence given usefulness; copied evidence cannot be squared.']
        elif q['id'] == 'q25':
            q['prompt'] = 'You run 20 independent tests of true null hypotheses. Each has an EXACT true-null rejection probability of 5%. What is the probability that at least one rejects?'
            q['rubric'] = ['Use independence of rejection decisions and complement the event of no rejections.', 'Obtain 1−0.95^20; a nominal level alone supplies an upper bound, not necessarily equality.', 'Justify Bonferroni by the union bound without requiring independence.']
        elif q['id'] == 'q32':
            q['rubric'] = ['Identify selecting and reporting the best noisy in-sample score as a changed evaluation procedure.', 'Specify a frozen independent confirmation or outer evaluation that repeats the complete inner search.', 'Record the actual search and handle correlated candidates without inventing a universal effective test count.']
            q['followSolution'] += ' Perfectly identical copies of one unbiased score add no selection gain: their maximum is that same score. Partial correlation can reduce optimism, but the joint distribution and selection rule, not a universal scalar effective count, determine it.'

    def question(suffix,title,level,minutes,prompt,answer,hints,solution,follow,follow_solution,rubric):
        add('q_l15_'+suffix,title,'Search',level,'researcher',minutes,prompt,answer,hints,solution,follow,follow_solution,'l15')
        questions[-1]['rubric']=rubric
        for key in ('prompt','solution','followSolution'):
            questions[-1][key]=questions[-1][key].replace(r'\n\n','\n\n')

    question('e1','A discovery fraction has a random denominator','Easy',7,
        r'A repeated procedure has exactly two equally likely outcomes: (V,R)=(1,1) or (0,9), where V counts false rejections and R counts all rejections. Define false discovery rate as \(E[V/\max(R,1)]\), assigning zero when R=0. What is its value? These are stipulated count outcomes, not a claim about calibrated individual p-values.',1/2,
        ['Calculate the false fraction inside each repetition before averaging.', 'A ratio of average counts is a different quantity.'],
        r'The within-run fractions are one and zero, so FDR is one half. In contrast, \(E[V]=1/2\) and \(E[R]=5\); their ratio is one tenth. Pooling discoveries weights a run with nine discoveries nine times as much as a run with one. FDR weights repetitions according to their probabilities. Here family-wise error \(P(V>0)\) happens also to equal one half; that equality is not a general identity.',
        r'Change the two outcomes to (0,0) and (1,2), still equally likely. Calculate FDR, family-wise error and the ratio of expected counts. Why must the zero-rejection convention be explicit?',
        r'The fractions are zero and one half, giving FDR one quarter. Family-wise error is one half, and the pooled population ratio is (1/2)/1=one half. A run without any rejection contributes zero to the false-discovery proportion; it must neither cause division by zero nor be silently removed from the repetition average. Dropping it changes the target to a conditional average given at least one rejection.',
        ['Average the two within-run fractions to obtain 1/2.', 'Distinguish FDR from a ratio of expected counts and from family-wise error.', 'Apply the zero-rejection convention and obtain follow-up values 1/4,1/2,1/2.'])

    question('e2','Copies repeat a rejection event','Easy',8,
        r'Twelve true-null tests are arranged in three blocks of four. Inside a block the four rejection decisions are IDENTICAL copies of one decision. Each block decision has exact false-rejection probability 0.1, and the three block decisions are independent. What is the probability of at least one false rejection among the twelve reported tests?',271/1000,
        ['There are three distinct random decisions, not twelve independent ones.', 'Complement the event that all three blocks accept.'],
        r'No rejection occurs precisely when all three block decisions accept. Thus \(P(V>0)=1-0.9^3=271/1000\). The independent twelve-test formula counts copied evidence as new randomness. Nevertheless \(E[V]=12(0.1)=1.2\): linearity of expectation does not require independence, and four false reports are counted whenever a block falsely rejects. Expected counts and the chance of any error answer different questions.',
        r'If the blocks contain two, four and seven identical copies, does the family-wise error change? What are the expected false count and FDR when all hypotheses are true?',
        r'The three underlying decisions still determine the same event, so family-wise error remains 271/1000. Expected false count is (2+4+7)·0.1=1.3. Under the global null V=R, so V/max(R,1) equals the indicator of any rejection; FDR equals family-wise error. This last identity depends on ALL hypotheses being true, not on independence.',
        ['Identify three independent block decisions and calculate 271/1000.', 'Use linearity for expected false reports without asserting independent copies.', 'Explain the global-null identity between FDR and family-wise error.'])

    question('h1','Correlated winners and shared confirmation noise','Hard',38,
        r'Two candidates have the SAME true value \(\theta\), and observed scores \(X_i=\theta+\varepsilon_i\). The errors are jointly Gaussian, mean zero, with variance \(\sigma^2>0\) each and correlation \(\rho\in[-1,1]\). Select \(J=\arg\max_i X_i\), breaking ties toward candidate one. Derive the mean and variance of the selected score, including both singular endpoints of rho. Then let confirmation errors be \(\eta_i=a\varepsilon_i+\sqrt{1-a^2}\,\zeta_i\), where \(a\in[-1,1]\), the zeta errors are iid \(N(0,\sigma^2)\), and are independent of the original pair. Derive the mean of the selected candidate’s confirmation score \(\theta+\eta_J\). Does calling a file a holdout make that mean unbiased?',None,
        [r'Use \(S=(\varepsilon_1+\varepsilon_2)/2\) and \(D=(\varepsilon_1-\varepsilon_2)/2\). Their Gaussian covariance is zero.', r'The winning error is S+|D|. A centered Gaussian with standard deviation t has mean absolute value \(t\sqrt{2/\pi}\).', 'Condition on the original errors before averaging the independently indexed confirmation noise.'],
        r'The Gaussian variables S and D are independent, including the degenerate cases. Their variances are \(\sigma^2(1+\rho)/2\) and \(\sigma^2(1-\rho)/2\). Let \(b=\sigma\sqrt{(1-\rho)/\pi}\). The winning error is S+|D|, so\n\n\[\begin{aligned}E[X_J]&=\theta+b,\\\operatorname{Var}(X_J)&=\sigma^2\left(1-\frac{1-\rho}{\pi}\right).\end{aligned}\]\n\nThe variance uses \(\operatorname{Var}|D|=E[D^2]-(E|D|)^2\), plus the independent S variance. At rho=1 both scores are identical: b=0 and variance sigma squared. At rho=−1 they are opposite errors: the winner is theta plus a folded normal, with bias \(\sigma\sqrt{2/\pi}\) and variance \(\sigma^2(1-2/\pi)\). At rho=0 the bias is sigma divided by square root pi.\n\nConditional on the original pair, J is fixed and the chosen zeta has mean zero. Therefore \(E[\theta+\eta_J]=\theta+ab\). Separate storage says nothing about a. Independent confirmation has a=0; reused noise has a=1 and keeps the full optimism; negative a can make confirmation pessimistic. The expected original-minus-confirmation gap is (1−a)b. This model makes the dependence mechanism explicit rather than equating a held-out filename with independent evidence.',
        r'Now let true candidate values differ, with delta=theta1−theta2. For \(s=\sigma\sqrt{2(1-\rho)}>0\), express the expected TRUE value of the selected candidate and its expected score optimism in terms of the standard normal density phi and distribution function Phi. Give the confirmation mean and handle s=0. Is score optimism measured relative to the better candidate’s true value?',
        r'Write W=epsilon1−epsilon2, so W is N(0,s squared), and J=1 when W≥−delta. Hence \(E[\theta_J]=\theta_2+\delta\Phi(\delta/s)\). The selected error equals \(\varepsilon_2+W\mathbf1\{W\geq-\delta\}\), whose mean is\n\n\[E[\varepsilon_J]=\int_{-\delta}^{\infty} w\frac{\phi(w/s)}s\,dw=s\phi(\delta/s).\]\n\nThe selected observed mean is the selected TRUE mean plus this optimism, and confirmation mean is \(E[\theta_J]+a s\phi(\delta/s)\). No independence between epsilon2 and W was used: only its unconditional zero mean. When s=0 the error is common to both candidates; select the higher true value deterministically (tie to one), with zero added bias. For delta=0 the formula recovers b; large absolute delta/s makes selection optimism vanish. Relative to the BEST true value, the difference also includes the loss from sometimes choosing the worse candidate. Confusing that benchmark with the selected candidate’s own truth hides a different source of error.',
        ['Derive independent Gaussian sum/difference variables and the folded-normal mean and variance.', 'Check rho=1,0,−1 rather than applying a nonsingular density at the endpoints.', 'Condition correctly on selection to derive theta+ab; identify the needed confirmation independence.', 'For unequal means derive selected truth and s phi(delta/s), distinguish its benchmark and handle s=0.'])


def add_coding(add,tasks):
    def exercise(level,title,prompt,samples,tests,reference,explanation):
        add('c_l15_'+level.lower(),title,level,'Search',prompt,'def solve('+SIGNATURES[level]+'):',samples,tests,reference,explanation)
        tasks[-1]['path']='researcher'
        for key in ('prompt','explanation'):
            tasks[-1][key]=tasks[-1][key].replace(r'\n\n','\n\n')

    exercise('Easy','Summarize discovery ratios per repetition',
        r'runs is an unsorted list of [false_rejections,total_rejections]. Each pair satisfies 0≤V≤R≤10^9 and contains integers; repetitions, including duplicate pairs, are distinct. There are at most 100000 pairs. Return [empirical_FDR,empirical_FWER,pooled_false_fraction]. The first is the mean of V/max(R,1) over ALL runs; the second is the fraction of runs with V>0; the third is sum(V)/sum(R), or None if there are no rejections. Empty input returns [None,None,None]. Use ordinary finite floats for defined ratios, O(n) time and O(1) auxiliary accumulators; preserve the input. These summarize supplied repetitions, without certifying calibrated p-values or estimating posterior usefulness.',
        [{'args':[[[1,1],[0,9]]],'expected':[.5,.5,.1]}, {'args':[[[0,0],[1,2]]],'expected':[.25,.5,.5]}],
        [{'args':[[]],'expected':[None,None,None]}, {'args':[[[0,0],[0,0]]],'expected':[0.,0.,None]}, {'args':[[[0,9]]],'expected':[0.,0.,0.]}, {'args':[[[10**9,10**9],[1,10**9],[0,0]]],'expected':[(1+1e-9)/3,2/3,(10**9+1)/(2*10**9)]}, {'args':[[[1,2]]*4000+[[0,0]]*4000],'expected':[.25,.5,.5]}],EASY_REFERENCE,
        r'Compute the false fraction before accumulating each repetition. The zero-rejection case contributes zero to that mean and still belongs in its denominator. Accumulate a separate indicator for any false report and separate integer totals for pooling. A pooled ratio weights runs by discovery counts; it must not replace an average of ratios. The loop makes one pass and leaves the input unchanged. Empty and all-zero cases have different outputs because the former has no repetition denominator.')

    exercise('Medium','Holm adjustment with exact boundaries',
        r'p_values is a list of rational pairs [numerator,denominator], each with 0≤numerator≤denominator≤10^9 and denominator≥1. alpha is another such pair. Fractions need not be reduced; the list may be empty and has at most 20000 entries. Every position names a separate hypothesis, even at equal or copied p-values. Sort the values ascending conceptually, and define the adjusted value at sorted position i (one-based) as \(\min(1,\max_{j\leq i}(m-j+1)p_{(j)})\). Return {"adjusted": [exact adjusted pairs in ORIGINAL order], "rejected": [original indices whose adjusted value≤alpha, in input order]}. Output every rational as a reduced pair of decimal STRINGS with positive denominator; zero is ["0","1"]. Reject at equality. Preserve both inputs. Avoid floating comparisons; aim for O(m log m) comparisons and O(m) storage, with integer/gcd bit costs additional.\n\nThis is Holm’s step-down Bonferroni method. For a fixed finite family it controls the probability of ANY false rejection under arbitrary dependence, provided every true-null individual p-value is valid (Pr(p≤t)≤t). It does not establish those prerequisite p-value assumptions. The formula above defines this task even for an arbitrary supplied list.',
        [{'args':[[[1,10],[1,10],[2,5]],[3,10]],'expected':{'adjusted':[['3','10'],['3','10'],['2','5']],'rejected':[0,1]}}, {'args':[[[1,2],[0,7],[2,20]],[1,5]],'expected':{'adjusted':[['1','2'],['0','1'],['1','5']],'rejected':[1,2]}}],
        [{'args':[[],[1,20]],'expected':{'adjusted':[],'rejected':[]}}, {'args':[[[0,1],[1,1]],[0,1]],'expected':{'adjusted':[['0','1'],['1','1']],'rejected':[0]}}, {'args':[[[3,10],[4,10],[1,2]],[1,1]],'expected':{'adjusted':[['9','10']]*3,'rejected':[0,1,2]}}, {'args':[[[1,10**9],[2,10**9],[10**9-1,10**9]],[2,10**9]],'expected':{'adjusted':[['3','1000000000'],['1','250000000'],['999999999','1000000000']],'rejected':[]}}, {'args':[[[1,4000]]*2000,[1,2]],'expected':{'adjusted':[['1','2']]*2000,'rejected':list(range(2000))}}],MEDIUM_REFERENCE,
        r'Sort original indices by cross multiplication. At sorted rank i starting at zero, compare (m−i) times that p-value against the running maximum, cap at one and reduce by gcd. Restore original positions; compare adjusted and alpha by exact cross products. Ties give equal adjusted values, regardless of stable ordering.\n\nWhy strong family-wise control does not need independence: if there are m0 true nulls, consider the FIRST true null rejected by the step-down procedure. At its rank at least m0 hypotheses remain, so its raw p-value must be≤alpha/m0. Thus any false rejection implies that at least one true-null p-value is≤alpha/m0. Validity and the union bound give probability at most m0(alpha/m0)=alpha. False-null p-values can behave arbitrarily. No rejection is possible after the first step-down failure; the running maximum expresses that rule for every alpha at once. Copies remain positions in the declared family and can make adjustment conservative. Do not substitute Holm–Sidak, which is a different method.')

    exercise('Hard','Calibrate the whole search by exact label randomization',
        r'features has n rows and m columns of integers in [−10^6,10^6], where n is even, 2≤n≤18 and 1≤m≤8. assignment is a length-n binary list with exactly n/2 ones. All candidate columns and their comparable scales were fixed BEFORE inspecting assignment. Conditional on this fixed matrix, the GLOBAL NULL states that assignment is uniform over ALL balanced assignments. This assumption is supplied, not inferred from having a dataset: arbitrary time-series label shuffling is not justified. Preserve both inputs.\n\nFor each column compute the ABSOLUTE difference between the mean over group one and the mean over group zero. In every balanced reassignment recompute ALL columns jointly and take their maximum statistic. Enumerate every distinct balanced assignment, including the observed one. Return {"statistics": [observed column statistics], "adjusted": [Pr(randomized maximum≥observed column statistic)], "global_p": Pr(randomized maximum≥observed maximum)}. Each value must be an exact reduced [numerator_text,denominator_text] string pair with positive denominator, including ["0","1"] for zero. Preserve original column order and include ties in the upper tail. This is exhaustive enumeration, so do NOT use a Monte Carlo +1 correction.\n\nLet C=binomial(n,n/2). Aim for O(Cnm+C log C+m log C+nm) time and O(C+nm) storage, rather than scanning all C maxima for each observed column. The exponential enumeration is intentional and bounded by n≤18. Calibration here concerns the complete/global null. Strong family-wise control under partial nulls needs extra assumptions; the Holm exercise instead establishes that control from valid marginal p-values.',
        HARD_SAMPLES,HARD_CASES,HARD_REFERENCE,
        r'With k=n/2, total column sum T and group-one sum S, the mean difference is (2S−T)/k. Keep absolute integer numerators D=|2S−T|; the common positive denominator k cancels in every comparison. Enumerate balanced index subsets, compute the JOINT maximum D for each, sort those maxima once, and use a lower-bound search to count values≥each observed numerator. Reduce counts/C and observed D/k exactly by gcd. Equal rows still have distinct indices and must not be deduplicated.\n\nUnder the stated conditional uniform assignment, the observed global statistic is one uniformly chosen member of this finite null multiset. Its inclusive upper-tail rank has a super-uniform p-value: ties can make it conservative. Rejecting any column when its maximum-adjusted tail is≤alpha is the same event as the global p-value≤alpha, because the largest observed statistic has the smallest tail. This proves global-null family calibration, not unrestricted partial-null strong control. Joint reassignment retains correlations; independent column shuffles destroy the declared joint null. A copied or sign-reversed column does not change an absolute-statistic maximum. Every exhaustive tail includes at least the observed assignment, so p-values cannot be zero. No randomized-sampling adjustment belongs in this exact calculation.')


SIGNATURES={'Easy':'runs','Medium':'p_values, alpha','Hard':'features, assignment'}
EASY_REFERENCE='''def solve(runs):
    if not runs:
        return [None,None,None]
    fractions = 0.0
    any_false = total_false = total_rejections = 0
    for v,r in runs:
        fractions += v / max(r,1)
        any_false += v > 0
        total_false += v
        total_rejections += r
    n = len(runs)
    return [fractions/n,any_false/n,
            total_false/total_rejections if total_rejections else None]'''

MEDIUM_REFERENCE='''from functools import cmp_to_key
from math import gcd
def solve(p_values, alpha):
    def compare(i,j):
        a,b = p_values[i]
        c,d = p_values[j]
        difference = a*d-c*b
        return (difference > 0)-(difference < 0)
    m = len(p_values)
    adjusted = [None]*m
    rejected = []
    running_n,running_d = 0,1
    for rank,index in enumerate(sorted(range(m),key=cmp_to_key(compare))):
        n,d = p_values[index]
        n *= m-rank
        if n >= d:
            n,d = 1,1
        if n*running_d > running_n*d:
            divisor = gcd(n,d)
            running_n,running_d = n//divisor,d//divisor
        adjusted[index] = [str(running_n),str(running_d)]
    a,b = alpha
    for index,(n,d) in enumerate(adjusted):
        if int(n)*b <= a*int(d):
            rejected.append(index)
    return {"adjusted":adjusted,"rejected":rejected}'''

HARD_REFERENCE='''from itertools import combinations
from bisect import bisect_left
from math import gcd
def solve(features, assignment):
    n,m = len(features),len(features[0])
    k = n//2
    totals = [sum(row[j] for row in features) for j in range(m)]
    observed = [abs(2*sum(features[i][j] for i in range(n) if assignment[i])-totals[j])
                for j in range(m)]
    maxima = []
    for chosen in combinations(range(n),k):
        maxima.append(max(abs(2*sum(features[i][j] for i in chosen)-totals[j])
                          for j in range(m)))
    maxima.sort()
    count = len(maxima)
    def pair(a,b):
        d = gcd(a,b)
        return [str(a//d),str(b//d)]
    def tail(d):
        return pair(count-bisect_left(maxima,d),count)
    return {"statistics":[pair(d,k) for d in observed],
            "adjusted":[tail(d) for d in observed],
            "global_p":tail(max(observed))}'''

HARD_SAMPLES=[
    {'args':[[[0,0],[0,1],[2,0],[2,1]],[0,0,1,1]],'expected':{'statistics':[['2','1'],['0','1']],'adjusted':[['1','3'],['1','1']],'global_p':['1','3']}},
    {'args':[[[0,0],[1,1],[2,2],[3,3]],[0,1,0,1]],'expected':{'statistics':[['1','1']]*2,'adjusted':[['2','3']]*2,'global_p':['2','3']}},
]
HARD_CASES=[
    {'args':[[[0,0,0]]*6,[0,0,0,1,1,1]],'expected':{'statistics':[['0','1']]*3,'adjusted':[['1','1']]*3,'global_p':['1','1']}},
    {'args':[[[-7,3],[9,0]],[0,1]],'expected':{'statistics':[['16','1'],['3','1']],'adjusted':[['1','1']]*2,'global_p':['1','1']}},
    {'args':[[[-10**6]*8]*9+[[10**6]*8]*9,[0]*9+[1]*9], 'expected':{'statistics':[['2000000','1']]*8,'adjusted':[['1','24310']]*8,'global_p':['1','24310']}},
]

# Independent finite bitstring enumeration supplies these literal expectations.
HARD_CASES += [{'args': [[[-3, 2], [4, 0], [1, 5], [0, -2], [2, 2], [7, -1]], [1, 0, 1, 0, 1, 0]], 'expected': {'statistics': [['11', '3'], ['4', '1']], 'adjusted': [['3', '10'], ['3', '10']], 'global_p': ['3', '10']}}, {'args': [[[2, 0, 4], [0, 9, -1], [5, 2, 5], [1, 4, 2]], [0, 1, 1, 0]], 'expected': {'statistics': [['1', '1'], ['7', '2'], ['1', '1']], 'adjusted': [['1', '1'], ['2', '3'], ['1', '1']], 'global_p': ['2', '3']}}, {'args': [[[0], [1], [2], [3], [4], [5]], [1, 0, 1, 0, 1, 0]], 'expected': {'statistics': [['1', '1']], 'adjusted': [['7', '10']], 'global_p': ['7', '10']}}]
