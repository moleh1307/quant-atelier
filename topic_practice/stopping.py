"""l05 practice: count conventions, sufficient state and finite expectations."""
from fractions import Fraction


def add_questions(add, questions):
    def question(suffix, title, level, minutes, prompt, answer, hints,
                 solution, follow, follow_answer, rubric):
        add(f'q_l05_{suffix}', title, 'Stopping times', level, 'shared',
            minutes, prompt, answer, hints, solution, follow, follow_answer, 'l05')
        questions[-1]['rubric'] = rubric

    question('e1', 'Does the successful trial count?', 'Easy', 4,
        r'Independent trials succeed with probability 1/5 each. T is the number of trials up to and including the first success. What is \(E[T]\)? Explain the first-step equation, then state the expected number of failed trials before that success.',
        5,
        ['The next trial always costs one trial, even if it succeeds.',
         'After a failure the future is a fresh copy of the same experiment.'],
        r'Let e be the expected additional number of trials before success. The next trial costs one; success leaves zero additional trials, while failure returns to the same state. Thus \(e=1+(4/5)e\), so e=5. The successful trial is included. The failure count is T-1 and has mean 4. Finiteness follows from \(P(T>n)=(4/5)^n\), whose sum over n>=0 is finite. Confusing trials with failures shifts the mean by one.',
        'Each failed trial takes one second and the successful trial takes three seconds. What is the expected total time, and why is five times three the wrong calculation?',
        r'The total time is (T-1)+3=T+2 seconds, so its mean is seven seconds. Only one trial is successful; charging all five expected trials the success duration would give the wrong fifteen seconds. The random trial count and the cost attached to each outcome are different parts of the model.',
        ['Include the successful trial and derive e=1+(4/5)e.',
         'Obtain five trials and distinguish four failures.',
         'Justify finite expectation by the geometric survival tail.'])

    question('e2', 'Probability is not elapsed time', 'Easy', 5,
        r'A fair random walk starts at integer position 2. Each independent step moves left or right by one with probability 1/2. Stop when position 0 or 5 is reached. What is the probability of reaching 5 first? Define the state-dependent quantity and its boundary values; do not use the expected-duration formula as a probability.',
        2/5,
        ['Use h_i for the probability of hitting 5 first, starting at i.',
         'The terminal values are h_0=0 and h_5=1; there is no one-step time charge.'],
        r'The hit probability satisfies \(h_i=(h_{i-1}+h_{i+1})/2\), because the next step selects one of those positions. The second difference is zero, so h_i is linear in i. The boundary values h_0=0 and h_5=1 give \(h_i=i/5\), hence \(h_2=2/5\). In contrast, the expected duration satisfies \(t_i=1+(t_{i-1}+t_{i+1})/2\), with both terminal durations zero; t_2=2*(5-2)=6 steps. Different objectives require different boundary values and immediate costs.',
        'If you already took seven steps and are currently at position 2 without absorption, does the future hit probability change?',
        r'No, under this independent fair-step model the present position is sufficient for the future hitting event. The remaining hit probability is still 2/5. Elapsed time affects the total duration already paid, but not these transition probabilities. A model in which step probabilities depend on time would require a larger state.',
        ['Set h_0=0 and h_5=1 and omit a duration cost.',
         'Solve the linear recurrence to obtain h_2=2/5.',
         'Explain why current position is a sufficient state here.'])

    question('h1', 'Collecting symbols of unequal frequency', 'Hard', 17,
        r'Each independent draw returns A, B or C with probabilities 1/2, 1/3 and 1/6 respectively. Stop as soon as all three have appeared. Starting with none seen, what is the expected number of draws, including the completing draw? Derive the answer and explain why simply tracking how many symbols have been seen loses information.',
        73/10,
        ['T>n means at least one of the three symbols is missing after n draws.',
         'Use inclusion–exclusion for missing-symbol events, then the nonnegative-integer tail identity E[T]=sum_{n>=0} P(T>n).',
         'Missing two particular symbols means every draw avoids their combined probability mass.'],
        r'For n>=0, let M_A, M_B and M_C be the events that the named symbol is still missing. If symbol i has probability p_i, then \(P(M_i)=(1-p_i)^n\), and \(P(M_i\cap M_j)=(1-p_i-p_j)^n\). All three are missing only at n=0. Inclusion–exclusion and the tail identity therefore give \[E[T]=\sum_i\frac1{p_i}-\sum_{i<j}\frac1{p_i+p_j}+\frac1{p_A+p_B+p_C}.\] In this case it is \(2+3+6-6/5-3/2-2+1=73/10\). The final +1 includes the empty draw history; without it the mean would be off by one. A finite-mean bound is supplied by the sum of the three individual first-arrival times, whose means sum to eleven. After seeing only A, the chance of something new is 1/2; after seeing only C it is 5/6. Thus the count alone is not sufficient. The individual first-arrival times are dependent, so a product of their CDFs is not justified.',
        'For m symbols with positive probabilities summing to one, write a general expression. What fails if a required symbol has probability zero?',
        r'For every nonempty subset S of symbols, let \(p(S)=\sum_{i\in S}p_i\). Inclusion–exclusion gives \(E[T]=\sum_{S\ne\varnothing}(-1)^{|S|+1}/p(S)\). The required zero-probability symbol would never appear, so the collection time is infinite almost surely; expressions with 1/0 are not finite expectation calculations. The subset formula has exponentially many terms and may suffer numerical cancellation; it is a derivation, not automatically an efficient or stable implementation for large m.',
        ['Form the union of missing-symbol events with correct pair intersections.',
         'Sum the geometric tails, including n=0, to obtain 73/10.',
         'Give a finite-mean bound and distinguish seen-set state from seen-count state.'])

    question('h2', 'Termination does not imply a finite mean', 'Hard', 20,
        r'A fair random walk starts at position 1 on the nonnegative integers. Each independent step moves one unit left or right until it first hits 0, when it stops. There is no upper boundary. Prove that it stops with probability one, yet its expected number of steps is infinite. You may use the bounded-walk results: from integer i strictly between 0 and N, \(P(\text{hit N first})=i/N\) and the mean time to hit either boundary is \(i(N-i)\). Explain why a finite first-step equation alone cannot settle the unbounded problem.',
        None,
        ['Introduce an artificial upper boundary N, without changing the original walk.',
         'Hitting 0 before N implies the original walk eventually hits 0.',
         'The original stopping time is at least the time to hit {0,N}, for every N.'],
        r'For any integer N>1, stop the same path at its first visit to 0 or N, at time \(\tau_N\). It hits 0 first with probability \(1-1/N\), so \(P(T<\infty)\geq1-1/N\). Letting N grow proves almost-sure termination. Pathwise \(T\geq\tau_N\); the artificial upper boundary can only shorten the wait. The bounded result gives \(E[\tau_N]=N-1\). Consequently \(E[T]\geq N-1\) for every N, forcing infinite mean. Eventual absorption and integrable duration are different statements. Writing \(e_i=1+(e_{i-1}+e_{i+1})/2\) presupposes finite quantities if used in ordinary algebra. Its real-valued formal solutions \(e_i=-i^2+bi\), with e_0=0, become negative for sufficiently large i and cannot represent nonnegative finite expected durations on this half-line. A finite answer from local algebra must satisfy the global state space and expectation conditions.',
        'Now move right with probability 2/5 and left with probability 3/5. From position 1, derive the expected time to 0 and justify finiteness before passing to an unbounded stopping time.',
        r'At the bounded time \(T\wedge n\), the stopped position is nonnegative and has expectation \(1-(1/5)E[T\wedge n]\): each live step has mean increment -1/5. Thus \(E[T\wedge n]\leq5\). Monotone convergence proves E[T]<=5, hence T is integrable and finite almost surely. Bounded increments and integrable T justify the expected-increment identity at T (the sum of expected absolute increments is finite). At absorption the position is zero, so \(0=1-(1/5)E[T]\) and E[T]=5. Negative drift changes the integrability condition; it is not merely a different constant in an unchecked formal equation.',
        ['Use bounded barriers to prove the hitting probability tends to one.',
         'Compare the stopping time pathwise to each bounded hitting time, giving a mean lower bound of N−1 for every N.',
         'Identify the finiteness/global-boundary failure in formal recurrence algebra.'])


def add_coding(add, tasks):
    def exercise(level, title, prompt, signature, samples, tests, solution, explanation):
        add(f'c_l05_{level.lower()}', title, level, 'Stopping times', prompt,
            signature, samples, tests, solution, explanation)
        tasks[-1].update(path='shared', lesson='l05')

    exercise('Easy', 'Finish a sequence of geometric stages',
        'success_probabilities describes stages completed in order. At stage j, every fresh independent trial succeeds with probability success_probabilities[j]. A success advances one stage; a failure stays in that stage. Stop on completing every stage. Return the expected total number of trials, including each successful trial. Return None if any required stage has probability zero, and 0 for no stages. The list has at most 100 probabilities, each either zero or in [10^-12,1]. Trials within and between stages are independent with the stated fixed probabilities; there is no reset to stage zero. Do not simulate, round or mutate the list.',
        'def solve(success_probabilities):',
        [{'args': [[1,.5,.25]], 'expected': 7}],
        [{'args': [[]], 'expected': 0},
         {'args': [[0]], 'expected': None},
         {'args': [[.5,0,.5]], 'expected': None},
         {'args': [[1,1,1]], 'expected': 3},
         {'args': [[.25]], 'expected': 4},
         {'args': [[1e-12,1]], 'expected': 1000000000001},
         {'args': [[1,.75,.5,.25]], 'expected': 25/3}],
        '''def solve(success_probabilities):
    if any(p == 0 for p in success_probabilities):
        return None
    return sum(1.0 / p for p in success_probabilities)''',
        r'A stage with success probability p>0 has mean 1/p trials by the first-step recurrence, counting success. The total duration is the sum of the stage durations, so linearity gives \(\sum_j1/p_j\). A zero-probability required stage is impossible to finish; None represents an infinite mean without emitting an invalid JSON infinity. Empty input is an already-complete sequence. This differs from consecutive-head search: failures here keep the stage rather than discarding all progress. O(k) time, O(1) working space.')

    # Expected values below come from exact rational first-step equations and
    # the border identity, cross-checked independently in the test suite.
    exercise('Hard', 'The overlap of an arbitrary coin pattern',
        'Flip a coin independently until the first occurrence of pattern as a contiguous block. Return the expected number of flips from no previous history, counting the completing flip. pattern is a nonempty string of H and T, with length k <= 200. Heads has probability heads/total, where heads and total are integers, 2 <= total <= 100 and 1/10 <= heads/total <= 9/10; these are exact rational probabilities. Tails has the remaining probability. Do not treat sliding windows as independent, return the reciprocal of full-pattern probability without checking overlap, simulate, or round. A border is a nonempty prefix of pattern that is also its suffix; include the full pattern. Derive a state recurrence or an equivalent overlap identity. Aim for O(k) character comparisons by following prefix/suffix failure links: a link replaces a candidate prefix by its longest proper border. Ordinary exact-integer arithmetic and the final float return are allowed; account for integer sizes in your complexity discussion.',
        'def solve(pattern, heads, total):',
        [{'args': ['HTH',1,2], 'expected': 10},
         {'args': ['HHT',1,2], 'expected': 8}],
        [{'args': ['H',1,4], 'expected': 4},
         {'args': ['T',1,4], 'expected': 4/3},
         {'args': ['HH',1,2], 'expected': 6},
         {'args': ['HT',1,2], 'expected': 4},
         {'args': ['HTH',1,4], 'expected': 76/3},
         {'args': ['HTHT',1,2], 'expected': 20},
         {'args': ['HHTHHT',1,2], 'expected': 72},
         {'args': ['HHH',3,4], 'expected': float(Fraction(4,3)+Fraction(4,3)**2+Fraction(4,3)**3)},
         {'args': ['H'*200,1,2], 'expected': float(2**201-2)},
         {'args': ['T'+'H'*199,1,10], 'expected': float(Fraction(10**200,9))}],
        '''import math
def solve(pattern, heads, total):
    k = len(pattern)
    prefix = [0] * k
    for i in range(1, k):
        j = prefix[i - 1]
        while j and pattern[i] != pattern[j]:
            j = prefix[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
        prefix[i] = j
    borders = set()
    length = k
    while length:
        borders.add(length)
        length = prefix[length - 1]
    numerator = denominator = 1
    contributions = []
    for length, symbol in enumerate(pattern, 1):
        numerator *= total
        denominator *= heads if symbol == 'H' else total - heads
        if length in borders:
            contributions.append(numerator / denominator)
    return math.fsum(contributions)''',
        r'The sufficient state is the longest suffix that is a prefix of the target. Its first-step equations have zero remaining wait at the completed target. An equivalent identity is \[E[T]=\sum_{b\text{ a nonempty border}}\frac1{P(\text{first b symbols})}.\] This includes the full pattern; proper borders account for surviving overlaps. Here is a justification, not a guess from examples. Before each flip, a new bettor starts with one unit and predicts successive symbols of the target, reinvesting all wealth. A correct next-symbol prediction multiplies wealth by the reciprocal of its probability; a wrong prediction loses it. Each bet is fair, so expected total wealth after n flips, stopped at completion if earlier, equals the expected number of entrants. At the first completed target, precisely the border-length bettors survive, with wealth 1/P(prefix). Their total wealth is the displayed sum. Finiteness follows by checking disjoint k-flip blocks: a block equals the target with positive probability, bounding T by k times a geometric duration. Until completion there are at most k active bettors and their wealth is bounded by a fixed sum of reciprocal prefix probabilities. These bounds justify taking the stopped limit, yielding the identity. HTH has borders of lengths 1 and 3 and fair-coin mean 2+8=10; HHT has only length 3 and mean 8. The prefix-function links find all borders with O(k) character comparisons and O(k) storage. Prefix probability numerators and denominators are accumulated as exact integers before division, avoiding repeated floating products. Integer arithmetic is not constant-cost: the intermediates have O(k log total) bits. math.fsum combines the positive float contributions accurately; the probability and length bounds keep the answer finite.')
