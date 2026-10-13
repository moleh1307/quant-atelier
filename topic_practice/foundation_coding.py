"""Deterministic topic exercises; reference solutions are never test oracles.

Expected cases use exact combinatorial counts, hand calculations or elementary
identities. Independent exhaustive checks live in test_topic_practice.py.
"""
import math


def add_foundation_coding(add, tasks):
    def exercise(lesson, level, title, prompt, signature, samples, tests, solution, explanation):
        topics = {'l01': 'Counting', 'l02': 'Conditioning', 'l03': 'Expectation'}
        add(f'c_{lesson}_{level.lower()}', title, level, topics[lesson], prompt,
            signature, samples, tests, solution, explanation)
        tasks[-1].update(path='shared', lesson=lesson)

    exercise('l01', 'Medium', 'Keep the mass when order disappears',
        'An urn contains counts[i] distinct physical balls of colour i. Return every unordered colour-pair record as [i, j, probability], in ascending i then j order with i <= j. Include zero-probability records. With replacement=True, make two independent uniform physical-ball draws; otherwise make two uniform draws without replacement. counts is a list of nonnegative integers, with at most 50 colours and each count at most 10^9. If no two draws are possible, return []. Derive the probabilities from ordered physical records; do not treat unordered colour pairs uniformly. Do not modify counts or simulate.',
        'def solve(counts, replacement):',
        [{'args': [[2, 1], True], 'expected': [[0, 0, 4/9], [0, 1, 4/9], [1, 1, 1/9]]},
         {'args': [[2, 1], False], 'expected': [[0, 0, 1/3], [0, 1, 2/3], [1, 1, 0]]}],
        [{'args': [[], True], 'expected': []},
         {'args': [[0, 0], False], 'expected': []},
         {'args': [[1], False], 'expected': []},
         {'args': [[1], True], 'expected': [[0, 0, 1]]},
         {'args': [[0, 2, 0], False], 'expected': [[0,0,0], [0,1,0], [0,2,0], [1,1,1], [1,2,0], [2,2,0]]},
         {'args': [[1, 1, 1], True], 'expected': [[0,0,1/9], [0,1,2/9], [0,2,2/9], [1,1,1/9], [1,2,2/9], [2,2,1/9]]},
         {'args': [[10**9, 10**9], False], 'expected': [[0,0,(10**9-1)/(2*(2*10**9-1))], [0,1,10**9/(2*10**9-1)], [1,1,(10**9-1)/(2*(2*10**9-1))]]}],
        '''def solve(counts, replacement):
    total = sum(counts)
    if total == 0 or (not replacement and total < 2):
        return []
    denominator = total * (total if replacement else total - 1)
    result = []
    for i, a in enumerate(counts):
        for j in range(i, len(counts)):
            if i == j:
                mass = a * (a if replacement else a - 1)
            else:
                mass = 2 * a * counts[j]
            result.append([i, j, mass / denominator])
    return result''',
        r'Use the ordered physical sample space of size \(N^2\) or \(N(N-1)\). A same-colour pair has \(a_i^2\) ordered records with replacement and \(a_i(a_i-1)\) without. A mixed pair has \(2a_i a_j\) because either colour can come first. Combine probability mass only after counting the records. Zero-count colours remain in the specified output, and an impossible experiment returns []. There are m(m+1)/2 output records: O(m²) time and output space, with O(1) additional working space beyond the output.')

    derangement_15 = sum((-1)**j * math.factorial(15)//math.factorial(j) for j in range(16))
    exercise('l01', 'Hard', 'Count constrained notebook assignments',
        'n distinct notebooks must be assigned bijectively to n researchers. allowed[i][j] is 1 if researcher i may receive notebook j, otherwise 0. Return the exact integer number of permitted assignments. allowed is a square matrix of zeros and ones with 0 <= n <= 15. For n=0 there is one empty assignment. Each notebook is used once; rows can have no permitted assignment, and individually nonempty rows do not guarantee a joint assignment exists. Aim for O(n * 2^n) time and O(2^n) space; enumerating all permutations is too slow. Do not mutate allowed.',
        'def solve(allowed):',
        [{'args': [[[1,1,0], [0,1,1], [1,0,1]]], 'expected': 2}],
        [{'args': [[]], 'expected': 1},
         {'args': [[[0]]], 'expected': 0},
         {'args': [[[1]]], 'expected': 1},
         {'args': [[[1,0,0], [1,0,0], [0,1,1]]], 'expected': 0},
         {'args': [[[1,1,0,0], [1,1,0,0], [0,0,1,1], [0,0,1,1]]], 'expected': 4},
         {'args': [[[1]*15 for _ in range(15)]], 'expected': math.factorial(15)},
         {'args': [[[int(i != j) for j in range(15)] for i in range(15)]], 'expected': derangement_15}],
        '''def solve(allowed):
    n = len(allowed)
    dp = [0] * (1 << n)
    dp[0] = 1
    for mask in range(1 << n):
        row = mask.bit_count()
        if row == n or dp[mask] == 0:
            continue
        for notebook in range(n):
            bit = 1 << notebook
            if not mask & bit and allowed[row][notebook]:
                dp[mask | bit] += dp[mask]
    return dp[-1]''',
        r'Let dp[mask] count assignments of the first popcount(mask) researchers using exactly the notebooks named by mask. The row is determined by that count, so no extra row dimension is needed. Extend each partial assignment by an allowed unused notebook. Every complete assignment has one unique sequence of extensions, so this neither loses nor duplicates assignments. dp[0]=1 makes the empty case work. An infeasible matrix produces zero. Use integer addition throughout: the desired count is exact. Under a uniform random assignment, its probability would be this count divided by n!, not a product of independent row success rates. O(n2ⁿ) time and O(2ⁿ) space.')

    exercise('l02', 'Easy', 'Restrict, then normalise',
        'weights contains nonnegative finite weights for mutually exclusive outcomes; keep contains equally many booleans describing an observed event. Return a probability list of the same length, conditional on that event: excluded outcomes have probability zero, and included weights are normalised. If the event has total weight zero, return None, including empty input. The original weights need not sum to one. Their sum is at most 10^12. Do not modify either input.',
        'def solve(weights, keep):',
        [{'args': [[2,3,5], [True,False,True]], 'expected': [2/7,0,5/7]}],
        [{'args': [[],[]], 'expected': None},
         {'args': [[1,2],[False,False]], 'expected': None},
         {'args': [[0,4],[True,False]], 'expected': None},
         {'args': [[0,4],[True,True]], 'expected': [0,1]},
         {'args': [[2,3,5],[True,True,True]], 'expected': [.2,.3,.5]},
         {'args': [[10**9,3*10**9],[True,True]], 'expected': [.25,.75]}],
        '''def solve(weights, keep):
    total = sum(w for w, included in zip(weights, keep) if included)
    if total == 0:
        return None
    return [w / total if included else 0 for w, included in zip(weights, keep)]''',
        r'The observed event removes incompatible outcomes. Its weight, not the original total, is the conditioning denominator. Scale invariance follows because multiplying every weight by the same positive constant changes both numerator and denominator equally. Conditioning on a zero-weight event is undefined in this finite model, so return None rather than inventing uniform probabilities. O(n) time and O(n) output space.')

    exercise('l02', 'Medium', 'Update a persistent hidden model',
        'prior is a probability vector over m mutually exclusive hidden models. One model is selected once and persists. likelihoods[t][j] is the probability of observation t under model j; observations are conditionally independent given that model. Return the posterior vector after all observations, or None if they are impossible under every positive-prior model. An empty observation list returns the prior unchanged as a list. Inputs: 1 <= m <= 30, at most 20 observations, each row length m, prior nonnegative and sums to one, likelihoods entries in [0,1]; each nonzero prior and likelihood is at least 10^-6. Do not reselect the model at each observation, simulate, or mutate input.',
        'def solve(prior, likelihoods):',
        [{'args': [[.5,.5], [[.25,.75],[.25,.75]]], 'expected': [.1,.9]}],
        [{'args': [[.2,.8], []], 'expected': [.2,.8]},
         {'args': [[0,1], [[1,0]]], 'expected': None},
         {'args': [[.3,.7], [[0,0]]], 'expected': None},
         {'args': [[.5,.5], [[0,1],[1,0]]], 'expected': None},
         {'args': [[.2,.3,.5], [[1,.5,0],[.5,1,.5]]], 'expected': [.4,.6,0]},
         {'args': [[.5,.5], [[1e-6,2e-6]]*20], 'expected': [1/(1+2**20), 2**20/(1+2**20)]}],
        '''def solve(prior, likelihoods):
    posterior = list(prior)
    for row in likelihoods:
        mass = [p * likelihood for p, likelihood in zip(posterior, row)]
        total = sum(mass)
        if total == 0:
            return None
        posterior = [value / total for value in mass]
    return posterior''',
        r'For each observation, multiply current model probabilities by that observation’s model-specific likelihood and normalise. The posterior becomes the next prior because the hidden model persists. Sequential normalisation gives the same posterior as one product of conditionally independent likelihoods. Zero prior mass stays zero. If every weighted likelihood is zero, the supplied model regards the observations as impossible; stop with None. The stated short-input bounds prevent product underflow, while sequential normalisation is still a useful habit. O(Tm) time and O(m) working space.')

    exercise('l02', 'Hard', 'Condition when the hidden state can change',
        'A hidden state takes one of m labels. prior gives the initial state probabilities. transition[i][j] gives P(next state j | current state i), each row summing to one. likelihoods[t][j] gives P(the observation at time t | state j). At t=0 use prior directly; before each later observation apply one transition. Given states, observations are independent and depend only on their corresponding state. Return [final_state_posterior, natural_log_probability_of_all_observations], or None if the observation sequence is mathematically impossible. An empty sequence returns [prior, 0]. Inputs: 1 <= m <= 8, up to 2000 observations, probabilities in [0,1], prior sums to one, each row has m entries; every nonzero probability is at least 10^-200. Tiny posterior states may become important after later evidence, so do not discard them internally: compute state updates in log space using stable log-sum-exp. Direct products and ordinary scaled posterior updates can underflow. Use no external libraries or simulation. Do not modify input.',
        'def solve(prior, transition, likelihoods):',
        [{'args': [[.5,.5], [[.8,.2],[.1,.9]], [[.2,.8],[.6,.3]]], 'expected': [[12/31,19/31], math.log(.186)]}],
        [{'args': [[.2,.8], [[1,0],[0,1]], []], 'expected': [[.2,.8],0]},
         {'args': [[.5,.5], [[1,0],[0,1]], [[1,0],[0,1]]], 'expected': None},
         {'args': [[1,0], [[0,1],[1,0]], [[1,0],[0,1],[1,0]]], 'expected': [[1,0],0]},
         {'args': [[.5,.5], [[.5,.5],[.5,.5]], [[.001,.001]]*1000], 'expected': [[.5,.5],1000*math.log(.001)]},
         {'args': [[.2,.8], [[1,0],[0,1]], [[1e-200,1e-200]]*2000], 'expected': [[.2,.8],2000*math.log(1e-200)]},
         {'args': [[.5,.5], [[1,0],[0,1]], [[1e-200,1],[1e-200,1],[1,0]]], 'expected': [[1,0],math.log(.5)+2*math.log(1e-200)]},
         {'args': [[0,1], [[.5,.5],[1,0]], [[1,1],[.3,.7]]], 'expected': [[1,0],math.log(.3)]}],
        '''import math
def solve(prior, transition, likelihoods):
    if not likelihoods:
        return [list(prior), 0.0]
    negative_infinity = -math.inf
    def log(p):
        return math.log(p) if p else negative_infinity
    def log_sum(values):
        largest = max(values)
        if largest == negative_infinity:
            return largest
        return largest + math.log(sum(math.exp(value - largest) for value in values))
    log_posterior = [log(p) for p in prior]
    log_transition = [[log(p) for p in row] for row in transition]
    log_probability = 0.0
    m = len(prior)
    for t, row in enumerate(likelihoods):
        if t:
            log_posterior = [log_sum([log_posterior[i] + log_transition[i][j]
                                     for i in range(m)]) for j in range(m)]
        mass = [log_posterior[j] + log(row[j]) for j in range(m)]
        scale = log_sum(mass)
        if scale == negative_infinity:
            return None
        log_probability += scale
        log_posterior = [value - scale for value in mass]
    return [[math.exp(value) for value in log_posterior], log_probability]''',
        r'First predict: \(\tilde p_t(j)=\sum_i p_{t-1}(i)T_{ij}\). Then condition: multiply by observation likelihoods and normalise. In log space use \(\log\sum_i e^{a_i}=b+\log\sum_i e^{a_i-b}\), where b is the largest finite term. At time zero there is no transition. Each log scale is the log conditional probability of the next observation given earlier ones; the chain rule makes their sum the sequence log probability. A zero-probability state is represented internally by negative infinity. A positive but tiny state retains a finite log weight, so later decisive evidence can restore it; ordinary probability normalisation alone can lose this state. Convert to probabilities only for the final output, where negligible components may round to zero. If every term is negative infinity, the sequence is impossible. This O(Tm²) recurrence sums over hidden paths without enumerating mᵀ paths. Stored log transitions cost O(m²) space, with O(m) state-update space. The posterior and the probability of the observations are different quantities.')

    exercise('l03', 'Easy', 'A linear payoff from marginals',
        'marginals[j] is a list of [value, probability] outcomes for random variable X_j. Each marginal has nonnegative probabilities summing to one. coefficients[j] is its fixed payoff weight. Return E[sum_j coefficients[j] * X_j]. Dependence between variables is unspecified; it is not needed for this linear payoff. Empty marginals and coefficients return 0. Lists have equal length, each supplied marginal is nonempty, values and coefficients have absolute value at most 10^6. No simulation, external libraries or input mutation.',
        'def solve(marginals, coefficients):',
        [{'args': [[[[1,.25],[5,.75]], [[0,.5],[2,.5]]], [2,-3]], 'expected': 5}],
        [{'args': [[],[]], 'expected': 0},
         {'args': [[[[-4,1]]], [2]], 'expected': -8},
         {'args': [[[[1,.5],[-1,.5]], [[3,1]]], [100,0]], 'expected': 0},
         {'args': [[[[5,.25],[1,.75]], [[2,1]]], [-2,3]], 'expected': 2},
         {'args': [[[[0,0],[7,1]], [[7,.5],[7,.5]]], [1,-1]], 'expected': 0}],
        '''def solve(marginals, coefficients):
    return sum(coefficient * sum(value * probability for value, probability in marginal)
               for marginal, coefficient in zip(marginals, coefficients))''',
        r'Compute each marginal mean, multiply by its fixed coefficient, and add. Linearity of expectation is valid for dependent variables with finite expectations. The supplied bounded finite supports guarantee this condition. Do not invent a joint distribution or enumerate combinations. The same marginals would be insufficient for a nonlinear payoff such as max(X₁,X₂). O(S) time for S supplied outcomes and O(1) working space, apart from generator machinery.')

    exercise('l03', 'Hard', 'Expected rank without replacement',
        'There are n distinguishable cards with integer labels values[i]; duplicate labels are allowed but cards remain distinct. Choose uniformly from all k-card subsets without replacement, sort the selected labels, and return the expected label in rank r (1 means the smallest). Inputs: 1 <= r <= k <= n <= 2000, labels between -10^6 and 10^6. Do not enumerate subsets or simulate. Derive the probability for each sorted population position; aim for O(n log n) sorting and O(n) combinatorial updates, treating integer arithmetic as one operation. Exact integer weights may be large; avoid converting binomial coefficients individually to floats. Do not mutate values.',
        'def solve(values, k, r):',
        [{'args': [[2,4,9,11], 2,1], 'expected': 23/6},
         {'args': [[2,4,9,11], 2,2], 'expected': 55/6}],
        [{'args': [[7],1,1], 'expected': 7},
         {'args': [[3,1,9,2],4,3], 'expected': 3},
         {'args': [[2,2,2,8],2,1], 'expected': 2},
         {'args': [[2,2,2,8],2,2], 'expected': 5},
         {'args': [[-5,-1,4,8],1,1], 'expected': 1.5},
         {'args': [list(range(2000)),1000,500], 'expected': 500*2001/1001-1},
         {'args': [list(range(2000,0,-1)),1999,1000], 'expected': 1000*2001/2000},
         {'args': [[-10**6]*1000 + [10**6]*1000,2000,1001], 'expected': 10**6}],
        '''import math
def solve(values, k, r):
    ordered = sorted(values)
    n = len(ordered)
    denominator = math.comb(n, k)
    first = r - 1
    last = n - k + r - 1
    weight = math.comb(n - r, k - r)
    numerator = 0
    for i in range(first, last + 1):
        numerator += ordered[i] * weight
        if i < last:
            weight = (weight * (i + 1) * (n - i - 1 - (k - r))
                      // ((i - r + 2) * (n - i - 1)))
    return numerator / denominator''',
        r'Break label ties by original card identity to obtain a total order; the returned label does not depend on that tie rule. Position i (zero-based) is the selected r-th card exactly when it is included, r-1 cards are chosen before it, and k-r after it. Its multiplicity is \(w_i=\binom{i}{r-1}\binom{n-i-1}{k-r}\), divided by \(\binom nk\). Feasible positions run from r-1 through n-k+r-1. Sum label times multiplicity as an integer, then divide once. Consecutive weights satisfy \(w_{i+1}/w_i=(i+1)(n-i-1-k+r)/[(i-r+2)(n-i-1)]\); stop before its final zero denominator. This avoids repeated combination calculations and overflow from individually converting enormous weights to floats. Duplicate labels remain distinct cards. Sorting costs O(n log n), followed by O(n) big-integer updates; actual bit-operation cost also depends on the integer sizes. O(n) space for the sorted copy.')
