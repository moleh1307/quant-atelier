"""Original transfer practice for l04: event probabilities before formulas."""
import math


def add_questions(add, questions):
    def question(suffix, title, level, minutes, prompt, answer, hints,
                 solution, follow, follow_answer, rubric):
        add(f'q_l04_{suffix}', title, 'Distributions', level, 'shared',
            minutes, prompt, answer, hints, solution, follow, follow_answer, 'l04')
        questions[-1]['rubric'] = rubric

    question('e1', 'A density of one and a half', 'Easy', 4,
        r'A continuous random variable X has density \(f(x)=2x\) for \(0<x<1\), and density zero elsewhere. What is \(P(X>3/4)\)? A colleague reports \(f(3/4)=3/2\) as the probability of observing 3/4. Explain what is wrong with that interpretation.',
        7/16,
        ['An interval receives the area under the density, not its height.',
         r'Find the CDF by integrating from the lower support boundary.'],
        r'The total area is \(\int_0^1 2x\,dx=1\), so this is a valid density even though some heights exceed one. On the support, \(F(x)=x^2\). Hence \(P(X>3/4)=1-(3/4)^2=7/16\). An individual point has probability zero in this continuous model. The height 3/2 describes probability per unit of x near 3/4: for a small positive interval width h, \(P(3/4<X\leq3/4+h)=3h/2+h^2\), provided the interval stays inside the support.',
        'If Y=100X is a percentage-scale measurement, does its density still reach two?',
        r'No. The support becomes \((0,100)\), the CDF is \(F_Y(y)=(y/100)^2\), and the density is \(f_Y(y)=y/5000\). Its maximum limiting height is 0.02. The event Y>75 still has probability 7/16. Density heights depend on the measurement units; event probabilities do not.',
        ['Integrate over (3/4,1) or use the CDF to obtain 7/16.',
         'Distinguish a zero-probability point from density per unit of x.',
         'Check the support and total density area.'])

    question('h1', 'A quiet race reveals its hidden regime', 'Hard', 18,
        r'A regime A or B is chosen once, each with probability 1/2. Given A, X and Y are independent exponential waiting times with rates 4 and 1 per minute. Given B, they are independent exponential waiting times with rates 1 and 1 per minute. The regime remains fixed for the entire race. Let \(W=\min(X,Y)\). You learn that neither clock has rung by \(s=\log 2\) minutes, where log is natural. What is the probability that X eventually rings first? Derive how this observation changes the regime weights; do not average the rates first.',
        8/15,
        ['Within each regime, the probability of surviving to s is the product of the two clock survival probabilities.',
         'Condition on the quiet race before mixing the within-regime winner probabilities.',
         'Memorylessness applies within a fixed regime; uncertainty about that regime can still change.'],
        r'Within A, \(P(W>s\mid A)=e^{-5s}=1/32\); within B it is \(e^{-2s}=1/4\). Including the equal prior weights and normalising gives \(P(A\mid W>s)=1/9\), and B has posterior weight 8/9. Given the regime and survival, exponential memorylessness leaves the rates unchanged. X therefore wins with probability 4/5 under A and 1/2 under B. Mixing with the updated weights gives \[P(X<Y\mid W>s)=\frac19\frac45+\frac89\frac12=\frac8{15}.\] The unconditional winner probability was 13/20. A quiet race favours the slower regime and lowers the winner advantage. Conditional independence of the clocks within regimes does not justify multiplying their marginal survival functions after hiding a common regime.',
        r'Instead you learn that the first ring occurred in \([s,s+h]\), without being told the winner. What is the limiting probability that X was the winner as \(h\downarrow0\), at the same s=log 2? Why is this different from survival past s?',
        r'The first-ring densities at s are \(5e^{-5s}\) under A and \(2e^{-2s}\) under B. Bayes weights these densities, not survival probabilities. At s=log 2 the posterior A weight is \((5/32)/(5/32+1/2)=5/21\). Within either fixed regime, winner and first-ring time are independent, since the winner-specific joint density is its rate fraction times the first-ring density. The limiting winner probability is \((5/21)(4/5)+(16/21)(1/2)=4/7\). The small-interval limit defines the conditioning rigorously; an exact continuous time is a zero-probability event. Observing a ring around s and observing no ring before s have different likelihoods.',
        ['Compute the regime-specific survival likelihoods 1/32 and 1/4.',
         'Update the A/B weights to 1/9 and 8/9 before using memorylessness.',
         'Mix winner probabilities to obtain 8/15 and explain why marginal rate averaging fails.'])


def add_coding(add, tasks):
    def exercise(level, title, prompt, signature, samples, tests, solution, explanation):
        add(f'c_l04_{level.lower()}', title, level, 'Distributions', prompt,
            signature, samples, tests, solution, explanation)
        tasks[-1].update(path='shared', lesson='l04')

    exercise('Easy', 'Read probabilities from a discrete CDF',
        r'distribution is a nonempty list of [value, probability] pairs, with distinct finite numeric values, nonnegative probabilities summing to one, and arbitrary input order. For each value t in thresholds return \(P(X\leq t)\), preserving threshold order. Values and thresholds may be negative; include mass exactly at t. At most 100 support values and 100 thresholds. Return [] for no thresholds. Zero-mass support values are allowed. Do not simulate, round or modify either input. An O(support * thresholds) solution is sufficient.',
        'def solve(distribution, thresholds):',
        [{'args': [[[3,.5],[-1,.25],[0,.25]], [-2,-1,0,2,3]], 'expected': [0,.25,.5,.5,1]}],
        [{'args': [[[2,1]], []], 'expected': []},
         {'args': [[[2,1]], [2,1,3,2]], 'expected': [1,0,1,1]},
         {'args': [[[9,0],[-4,1]], [-5,-4,8,9]], 'expected': [0,1,1,1]},
         {'args': [[[-3,.2],[5,.3],[1,.5]], [1,-3,5,-4,4]], 'expected': [.7,.2,1,0,.7]}],
        '''def solve(distribution, thresholds):
    return [sum(p for value, p in distribution if value <= t)
            for t in thresholds]''',
        r'The CDF is the probability of an event, \(F(t)=P(X\leq t)\). Add the masses of precisely the eligible support values. A point mass belongs to the CDF at its own location, so use <= rather than <. No density approximation or independence assumption is involved. Scan all support values for each threshold: O(mq) time, O(q) output space and O(1) additional working space. Sorting is optional at these limits.')

    exercise('Medium', 'The first of unequal discrete clocks',
        'distributions is a nonempty list of PMFs for independent waiting times. Each PMF is a nonempty list of [time, probability] pairs; its times are distinct finite nonnegative numbers in arbitrary order, and its nonnegative probabilities sum to one. Return the PMF of the minimum waiting time as sorted [time, probability] pairs. Include every time appearing in any input PMF, even when the minimum has zero mass there. Different clocks need not have the same distribution, and ties count once at their common time. At most 30 clocks and 50 support times per clock. Do not enumerate all joint outcomes, simulate, mutate the inputs or round. Aim for O(S log S + mU) time, where S is total support size, m is clock count and U is the number of distinct times.',
        'def solve(distributions):',
        [{'args': [[[[1,.5],[3,.5]],[[2,.25],[3,.75]]]], 'expected': [[1,.5],[2,.125],[3,.375]]}],
        [{'args': [[[[2,1]]]], 'expected': [[2,1]]},
         {'args': [[[[2,.5],[0,.5]],[[0,.25],[1,.75]]]], 'expected': [[0,.625],[1,.375],[2,0]]},
         {'args': [[[[4,1]],[[4,1]]]], 'expected': [[4,1]]},
         {'args': [[[[0,0],[5,1]],[[2,1],[9,0]]]], 'expected': [[0,0],[2,1],[5,0],[9,0]]},
         {'args': [[[[1,.25],[3,.75]],[[2,.5],[4,.5]],[[0,.2],[5,.8]]]], 'expected': [[0,.2],[1,.2],[2,.3],[3,.3],[4,0],[5,0]]},
         {'args': [[[[0,.5],[1,.5]] for _ in range(30)]], 'expected': [[0,1-2**-30],[1,2**-30]]}],
        '''def solve(distributions):
    ordered = [sorted(pmf) for pmf in distributions]
    support = sorted({value for pmf in ordered for value, _ in pmf})
    positions = [0] * len(ordered)
    cdfs = [0.0] * len(ordered)
    previous_survival = 1.0
    result = []
    for value in support:
        survival = 1.0
        for j, pmf in enumerate(ordered):
            while positions[j] < len(pmf) and pmf[positions[j]][0] <= value:
                cdfs[j] += pmf[positions[j]][1]
                positions[j] += 1
            tail = max(0.0, 1.0 - cdfs[j])
            if positions[j] == len(pmf):
                tail = 0.0
            survival *= tail
        result.append([value, max(0.0, previous_survival - survival)])
        previous_survival = survival
    return result''',
        r'For \(L=\min_j X_j\), \(L>t\) means every clock exceeds t. Independence gives \(P(L>t)=\prod_j(1-F_j(t))\); identical distributions are unnecessary. Traverse the union of support times. At each time update the clock CDFs, multiply survival probabilities, and subtract the new survival from the previous one to obtain the point mass. All ties are already accounted for by this event identity; adding individual winning-clock probabilities would double-count tied rings. A zero-mass input location remains in the requested output. At the largest support of a clock its tail is exactly zero; clamps remove tiny negative roundoff. Sorting costs O(S log S), the traversal O(S+mU), with O(S+m) working storage and O(U) output storage.')

    exercise('Hard', 'A ranked outcome without identical distributions',
        r"There are m independent real-valued random variables. distributions[j] is variable j's nonempty PMF as [value, probability] pairs, with distinct finite values in arbitrary order and nonnegative probabilities summing to one. The variables need not be identically distributed. rank is an integer from 1 to m. Sort the realised m values, retaining duplicates: the rank-th entry is R. For each t in thresholds return \(P(R\leq t)\) in input threshold order. Ties at t count as <=. Limits: 1 <= m <= 60, at most 30 support values per PMF, at most 40 thresholds. Return [] for no thresholds. Do not simulate, enumerate the Cartesian product, assume a binomial count with a common success probability, mutate inputs or round. Derive a dynamic program for the number of variables at or below a threshold; aim for O(S log S + q*m*(rank + log s_max)) time. Here S is total support size, q is threshold count and s_max is the largest individual support size.",
        'def solve(distributions, rank, thresholds):',
        [{'args': [[[[0,.5],[2,.5]],[[1,.25],[3,.75]],[[1,.75],[4,.25]]],2,[0,1,2,4]], 'expected': [0,.5,.8125,1]}],
        [{'args': [[[[3,1]]],1,[]], 'expected': []},
         {'args': [[[[2,1]],[[2,1]],[[2,1]]],2,[2,1,3]], 'expected': [1,0,1]},
         {'args': [[[[-1,.25],[1,.75]],[[0,.5],[2,.5]]],1,[-2,-1,0,1,2]], 'expected': [0,.25,.625,1,1]},
         {'args': [[[[-1,.25],[1,.75]],[[0,.5],[2,.5]]],2,[2,1,0,-1,-2]], 'expected': [1,.5,.125,0,0]},
         {'args': [[[[0,0],[1,1]],[[0,1],[1,0]]],2,[0,1]], 'expected': [0,1]},
         {'args': [[[[0,.9],[1,.1]],[[0,.1],[1,.9]],[[0,.5],[1,.5]]],2,[0]], 'expected': [.5]},
         {'args': [[[[0,.5],[1,.5]] for _ in range(60)],30,[0]], 'expected': [sum(math.comb(60,k) for k in range(30,61))/2**60]},
         {'args': [[[[0,.5],[1,.5]] for _ in range(60)],60,[1,0]], 'expected': [1,2**-60]}],
        '''from bisect import bisect_right
def solve(distributions, rank, thresholds):
    tables = []
    for pmf in distributions:
        ordered = sorted(pmf)
        values = [value for value, _ in ordered]
        prefix = [0.0]
        for _, probability in ordered:
            prefix.append(prefix[-1] + probability)
        tables.append((values, prefix))
    result = []
    for threshold in thresholds:
        dp = [0.0] * (rank + 1)
        dp[0] = 1.0
        for values, prefix in tables:
            index = bisect_right(values, threshold)
            probability = 1.0 if index == len(values) else prefix[index]
            probability = min(1.0, max(0.0, probability))
            for count in range(rank, 0, -1):
                if count == rank:
                    dp[count] += dp[count - 1] * probability
                else:
                    dp[count] = (dp[count] * (1.0 - probability)
                                 + dp[count - 1] * probability)
            dp[0] *= 1.0 - probability
        result.append(dp[rank])
    return result''',
        r'The event \(R\leq t\) is equivalent to at least rank of the m realised values being <=t. Variable j contributes an independent indicator with probability \(p_j=F_j(t)\). These probabilities can differ, so a common-p binomial formula is generally wrong. Let dp[k] track exactly k successes for k<rank, and dp[rank] track all counts >=rank. Start with dp[0]=1. For each variable, interior masses update as \(d_k(1-p_j)+d_{k-1}p_j\). The capped state updates as \(d_r+d_{r-1}p_j\): mass already in that state stays there regardless of the next indicator. Update descending so old masses are not reused twice. Sorted PMFs and prefix sums supply each CDF by binary search, including ties. Preprocessing takes O(S log S); each threshold takes O(m(log s_max+rank)), with O(S+rank) working storage. For rank=1 this reduces to one minus the product of survivals; for rank=m it reduces to the product of CDFs.')
