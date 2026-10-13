"""Original practice on scoring, information refinement and auction selection.

The auction laws are specified joint distributions, not equilibrium claims.
Exact score grouping uses identical forecasts, never arbitrary reliability bins.
"""
from fractions import Fraction


def rational(value):
    value = Fraction(value)
    return f'{value.numerator}/{value.denominator}'


def score_result(score, reliability, resolution, uncertainty):
    return dict(zip(('score', 'reliability', 'resolution', 'uncertainty'),
                    map(rational, (score, reliability, resolution, uncertainty))))


def bid_result(bid, gain, probability, value):
    return {'bid': bid, 'gain': rational(gain),
            'win_probability': rational(probability),
            'win_value': None if value is None else rational(value)}


def add_questions(add, questions):
    next(q for q in questions if q['id'] == 'q41')['rubric'] = [
        'Explain how winning can select an optimistic noise realization despite an unbiased estimate before selection.',
        'Condition value on both the observed signal and the winning event, with an explicit information model.',
        'Separate value inference from an optimal bid, which also depends on payment rules and rival strategies.',
        'Distinguish common-value inference from a known private consumption value.'
    ]

    def question(suffix, title, level, minutes, prompt, answer, hints,
                 solution, follow, follow_solution, rubric):
        add('q_l24_' + suffix, title, 'Strategic inference and calibration',
            level, 'trader', minutes, prompt, answer, hints, solution,
            follow, follow_solution, 'l24')
        questions[-1]['rubric'] = rubric

    question('e1', 'One success does not reward the best probability', 'Easy', 8,
        r'''Under your fixed pre-outcome information, a binary outcome Y has success probability 3/4. You report p before Y occurs, and receive Brier LOSS \((p-Y)^2\), with lower loss better. Your report cannot affect the outcome. What is the EXCESS EXPECTED loss of reporting p=1 rather than p=3/4? Average over both outcomes; this asks a difference, not either individual loss.''',
        1/16,
        ['Compute each report’s loss on success and failure, then weight them by 3/4 and 1/4.',
         'For true probability q, expected loss is (p−q)²+q(1−q).'],
        r'''Honest reporting has expected loss (3/4)(1/4)²+(1/4)(3/4)²=3/16. Reporting one has zero loss on success but loss one on failure, so its expectation is 1/4. The excess is 1/16. More generally, for fixed true probability q,

\[E[(p-Y)^2]=(p-q)^2+q(1-q).\]

The irreducible term is the same for both reports; certainty adds avoidable expected error. This argument uses a probability under the specified information, not a success rate estimated after seeing this outcome.''',
        'A success occurs and the report one receives loss zero. Does that contradict the comparison? Calculate the realised differences on success and failure and recover the expected excess.',
        r'''On success, loss(one)−loss(honest)=−1/16. On failure it is 1−9/16=7/16. Their weighted mean is (3/4)(−1/16)+(1/4)(7/16)=1/16. A worse probability can be luckier on a single realisation. Neither a success nor a failure alone certifies long-run calibration.''',
        ['Obtain the expected losses 3/16 and 1/4 and their difference 1/16.',
         'Keep the forecast information fixed and average over both binary outcomes.',
         'Explain the realised reversal and recover the expectation without treating one event as calibration evidence.'])

    question('e2', 'The error units determine the best point estimate', 'Easy', 10,
        r'''A positive target Y equals four or sixteen, each with probability one half under your current information. Choose a single estimate x>0 before observing Y. Your objective is to minimise EXPECTED SQUARED log-ratio loss [log(x/Y)]², using natural logs. What is the unique minimising x? Explain why this differs from minimising squared error in the original quantity.''',
        8,
        ['Write z=log(x); the objective becomes squared error for the random variable log(Y).',
         'The mean of the two log values is the log of their geometric mean.'],
        r'''Let z=log(x). Completing the square gives

\[E[(z-\log Y)^2]=(z-E[\log Y])^2+\operatorname{Var}(\log Y).\]

Here E[log Y]=3 log 2, so x=8 is unique because log is one-to-one on the positive domain. Both possible log errors have magnitude log 2, giving minimum squared loss (log 2)². Ordinary squared error instead selects E[Y]=10. Its minimum is thirty-six, whereas choosing eight gives original-unit squared error forty. The scoring rule, not a universal idea of an accurate estimate, determines which answer is optimal.''',
        'Replace SQUARED log-ratio loss by ABSOLUTE log-ratio loss. Is eight still the unique optimum? Also describe what happens when both the target and estimate are converted to units one hundred times larger, or when the target can be zero.',
        r'''Absolute error in log space is minimised by any median. For these two equally likely log values, every z between log 4 and log 16 is a median; thus EVERY x in [4,16] minimises the absolute log loss, with value log 2. Eight remains optimal but is no longer unique. Multiplying both x and Y by one hundred leaves x/Y and both log losses unchanged. A zero target makes this log-ratio objective undefined; adding an arbitrary offset changes the task rather than extending the same loss.''',
        ['Transform to log space and derive the unique squared-loss estimate eight.',
         'Compare with the original-unit squared-loss optimum ten and its losses.',
         'Derive the whole absolute-log-loss optimum interval and respect the positive domain and unit conversion.'])

    question('m1', 'A perfect-looking bin can hide opposite forecasts', 'Medium', 20,
        r'''Two pre-outcome forecasts are p₁=0.1 and p₂=0.9. Dataset A pairs them with outcomes (0,1); dataset B pairs them with outcomes (1,0). A diagnostic puts both records in ONE coarse bin. Compare the bin count, mean forecast, observed rate and direct mean Brier loss for the two datasets. Can the three bin summaries reconstruct the loss? Derive the missing relationship using empirical variances and covariance with divisor TWO.''',
        None,
        ['The summaries forget which outcome was paired with which forecast.',
         'Expand the mean of (p−y)² around the two empirical means.',
         'The covariance term changes sign although both marginal lists stay the same.'],
        r'''Both bins have count two, mean forecast one half and observed rate one half. Their average forecast-minus-outcome gap is zero. But A has loss 0.01 on each record, while B has loss 0.81 on each record. Let empirical means be \(\bar p,\bar y\), and use divisor n in empirical variances and covariance. Expanding centred records yields

\[\begin{aligned}\overline{(p-y)^2}&=(\bar p-\bar y)^2\\&\quad+\operatorname{Var}_{emp}(p)\\&\quad+\operatorname{Var}_{emp}(y)\\&\quad-2\operatorname{Cov}_{emp}(p,y).\end{aligned}\]

Here the forecast variance is 0.16 and outcome variance 0.25. Covariance is +0.2 in A and −0.2 in B, giving 0.01 and 0.81 respectively. Coarse bin averages erase this pairing term. A zero bin gap therefore neither determines Brier loss nor proves population calibration.''',
        'Suppose the two outcomes are independent Bernoulli variables with TRUE success probabilities 0.1 and 0.9. What are the probabilities of the two observed datasets? Would the bad score in B prove the model probabilities wrong? Would splitting into one-record bins establish long-run calibration?',
        r'''A has probability (1−0.1)·0.9=0.81, while B has probability 0.1·(1−0.9)=0.01. Other outcome pairs account for the remaining 0.18. B is unusual but possible under the correct probabilities. Singleton bins expose their individual observed discrepancies, yet a binary outcome is not its underlying probability. Preserve matched forecasts, outcome timestamps and an evaluation protocol; use adequate counts and uncertainty rather than proclaiming calibration from this tiny sample. The probability calculation needs the explicitly added independence assumption; the empirical covariance identity does not.''',
        ['Calculate equal bin summaries but Brier losses 0.01 and 0.81.',
         'Derive the centred identity with divisor n and the correct covariance signs.',
         'Distinguish lost pairing, a realised score and population calibration; obtain event probabilities under the added independent model.'])

    question('m2', 'Winning reweights the value behind your signal', 'Medium', 23,
        r'''After observing your own signal, common asset value V is one hundred with probability 1/4 and zero otherwise. You have ALREADY fixed a first-price bid of ten. Conditional on V AND your current information, two rival bids are independent. Each rival bids below ten with probability 0.8 if V=0 and 0.4 if V=100. You win precisely when both rival bids are below ten, pay ten on winning and pay nothing otherwise. What is E[V | your information, winning]? This is inference at the fixed bid, not an equilibrium bid calculation.''',
        100/13,
        ['Square each conditional crossing probability before applying Bayes.',
         'The prior weights already include your signal; do not use that signal a second time.'],
        r'''The winning likelihoods are 16/25 and 4/25. Multiplying by the signal-conditioned prior gives low-value-and-win mass 12/25 and high-value-and-win mass 1/25. Total winning probability is 13/25, so the conditional high-value probability is 1/13 and conditional value is 100/13. Conditional expected net gain is 100/13−10=−30/13. Ex-ante gain under your present information is (13/25)(−30/13)=−6/5. The signal-only mean twenty-five is insufficient: subtracting ten from it ignores the value-dependent event on which you pay.''',
        'Use one rival instead, then m conditionally independent rivals with the same crossing probabilities. Derive the winning posterior. Could you optimise your bid by using this posterior unchanged at every bid?',
        r'''With one rival, joint winning masses are 3/5 and 1/10; win probability is 7/10, conditional high-value probability 1/7, conditional value 100/7 and ex-ante gain three. For m rivals,

\[P(V=100\mid\mathrm{Win})=\frac{1}{1+3\cdot2^m}.\]

Its mean is one hundred times that probability. These crossing probabilities are stipulated AT BID TEN. Changing the bid changes the rival crossing events, requiring their laws at the new threshold. No calculation here establishes a best response or equilibrium. Without conditional independence, multiplying crossing probabilities is unjustified.''',
        ['Use both rival likelihoods and the signal-conditioned prior exactly once.',
         'Obtain conditional value 100/13, win probability 13/25 and expected net gain −6/5.',
         'Derive the one-rival and m-rival changes, identifying the independence and fixed-bid boundaries.'])

    question('h1', 'Optimise the bid and the selection event together', 'Hard', 38,
        r'''A risk-neutral bidder’s current information assigns common value V=100 or V=200 equal probability. There are two rivals, whose bids are conditionally independent given V. If V=100, each bid is uniform on [0,100]; if V=200, each is uniform on [100,200]. These rival laws are fixed and exogenous: no equilibrium is asserted. Choose a real first-price bid b in [0,200], win if it exceeds BOTH rival bids, pay b only on winning and receive V then. Otherwise gain is zero. Ties have probability zero, and there are no other costs. Derive expected gain over the WHOLE allowed interval and prove its global maximising bid. Compare that bid with the conditional value on winning.''',
        None,
        ['For b below one hundred, a win is possible only in the low-value state.',
         'For b above one hundred, low-value wins are certain but incur a negative margin.',
         'Compare the maxima of both pieces and all boundaries, not just a stationary point.'],
        r'''For 0≤b≤100, two independent uniform crossings give

\[G(b)=\tfrac12(100-b)(b/100)^2.\]

Its derivative is \(b(200-3b)/20000\), positive up to 200/3 and negative thereafter; boundaries give zero. The interior maximum is therefore at b=200/3 with gain 200/27. For 100≤b≤200 write x=(b−100)/100, so x∈[0,1]. The low state always wins and the high state wins with probability x². Hence

\[G(b)=50[-x+(1-x)x^2].\]

For x>0, (1−x)x²<x, so this entire piece is negative; at x=0 it is zero. The low-piece optimum is the global unique maximum. At that bid, winning reveals V=100, with total win probability 2/9. Conditional margin is 100/3, whose product with 2/9 gives 200/27. Conditional value ONE HUNDRED is not the optimal bid: raising the bid trades margin against win probability. Bidding the unconditional mean 150 wins with probability 5/8, gives winning mean value 120 and expected gain −75/4.''',
        'Replace the two rivals by m≥1 conditionally independent rivals with the same state-dependent uniform laws. Find the global optimum and maximum gain. Explain which parts would need reconsideration for a second-price auction or endogenous rival strategies.',
        r'''The low piece is G(b)=50(1−z)z^m with z=b/100. Its derivative changes sign at z=m/(m+1), yielding

\[b^*=\frac{100m}{m+1},\qquad G(b^*)=\frac{50m^m}{(m+1)^{m+1}}.\]

The upper piece is 50[−x+(1−x)x^m], negative for x>0 because x^m≤x and 1−x<1. Boundaries do not improve the positive interior gain. Within the upper piece the winning high-state probability is x^m/(1+x^m), so the winning value itself changes with the action. Second-price payments depend on the highest rival bid, not your b, altering the margin objective. If rival strategies respond to you, the fixed crossing laws need a strategic model; the present optimum is a best response to specified exogenous laws.''',
        ['Derive both expected-gain pieces using conditional joint crossings and first-price payments.',
         'Prove global optimality at 200/3 including boundaries and the negative upper piece.',
         'Calculate gain 200/27 and distinguish the optimum from conditional value and the raw mean.',
         'Derive the m-rival formula and state precisely what changes with payment rules or strategic responses.'])

    question('h2', 'Can new information improve an already calibrated forecast?', 'Hard', 35,
        r'''Let Y be binary, P∈[0,1] a probability report, and G another feature. Both P and G are available BEFORE Y occurs. Under a fixed population joint law define \(R=E[Y\mid P]\) and \(T=E[Y\mid P,G]\); use the exact conditional expectations, not fitted estimates. Prove that R and T are each calibrated and derive the changes in expected Brier loss from P to R and from R to T. Does calibration of P alone rule out a strict improvement from G? State when each improvement is strict.''',
        None,
        ['For any information set, subtract its conditional mean and make the cross term vanish.',
         'R is a function of P, whereas T uses the larger information set.',
         'Apply the tower property to show calibration even when multiple information states produce the same report.'],
        r'''Because \(E[Y-R\mid P]=0\), expanding squared loss around R gives

\[E[(P-Y)^2]-E[(R-Y)^2]=E[(P-R)^2].\]

Likewise R and T are measurable under the enlarged information (P,G), and \(E[Y-T\mid P,G]=0\), so

\[E[(R-Y)^2]-E[(T-Y)^2]=E[(T-R)^2].\]

The right sides are nonnegative and strictly positive precisely when the corresponding forecasts differ with positive probability. Tower conditioning gives E[Y|R]=E[E[Y|P]|R]=R and E[Y|T]=E[E[Y|P,G]|T]=T. If P is calibrated then R=P almost surely, but T can still vary within a fixed P. For example, two equally likely regimes have conditional success probabilities 1/4 and 3/4 while P=1/2 in both. P is calibrated globally and has expected loss 1/4; the regime-informed T has expected loss 3/16, improving by 1/16. No independence across successive evaluation records is needed for these population identities; pre-outcome availability and the declared joint law are essential.''',
        'A developer estimates T from the same finite dataset used to evaluate it and obtains smaller empirical loss. Does your proof certify future improvement? What if G actually contains the eventual outcome? Specify a valid comparison protocol.',
        r'''The proof concerns exact population conditional means. A fitted estimate can have approximation and estimation error; minimising in-sample residuals can reward overfitting. A feature containing the eventual outcome would make T=Y and give zero retrospective error, but is unavailable for a forecast. Define the feature timestamp and baseline in advance, fit transformations/recalibration only on training data, then evaluate paired pre-outcome forecasts on untouched data with a split appropriate to dependence and deployment time. Report both losses and uncertainty. Finite bin frequencies can help diagnose reliability but neither equal the population means by definition nor guarantee out-of-sample improvement.''',
        ['Derive both squared-loss differences through conditional cross-term cancellation.',
         'Prove calibration using tower conditioning and state the positive-probability strictness criteria.',
         'Construct the calibrated constant/report-with-regime counterexample and compute its losses.',
         'Separate exact conditional means from fitted in-sample estimates and exclude post-outcome information.'])


MEDIUM_REFERENCE = '''from math import gcd

def ratio(num, den):
    g = gcd(abs(num), den)
    return str(num//g) + '/' + str(den//g)

def solve(probabilities, outcomes, weights, scale):
    groups = {}
    total = successes = squares = paired = 0
    for p,y,w in zip(probabilities,outcomes,weights):
        if not w:
            continue
        n,s = groups.get(p,(0,0))
        groups[p] = (n+w,s+w*y)
        total += w
        successes += w*y
        squares += w*p*p
        paired += w*p*y
    tnum,tden = 0,1
    for n,s in groups.values():
        tnum,tden = tnum*n+s*s*tden,tden*n
        g = gcd(tnum,tden)
        tnum,tden = tnum//g,tden//g
    d = scale
    base = squares-2*d*paired
    return {'score':ratio(base+d*d*successes,total*d*d),
            'reliability':ratio(base*tden+d*d*tnum,total*d*d*tden),
            'resolution':ratio(tnum*total-successes*successes*tden,tden*total*total),
            'uncertainty':ratio(successes*(total-successes),total*total)}'''


HARD_REFERENCE = '''from math import gcd

def ratio(num,den):
    g = gcd(abs(num),den)
    return str(num//g) + '/' + str(den//g)

def solve(states, cap):
    total = sum(w for v,h,w in states)
    ordered = sorted(states,key=lambda row:row[1])
    mass = value_sum = best_gain = best_bid = 0
    best_mass = best_value = 0
    i = 0
    while i < len(ordered):
        threshold = ordered[i][1]
        if threshold >= cap:
            break
        while i < len(ordered) and ordered[i][1] == threshold:
            v,h,w = ordered[i]
            mass += w
            value_sum += w*v
            i += 1
        bid = threshold+1
        gain = value_sum-bid*mass
        if gain > best_gain:
            best_bid,best_gain = bid,gain
            best_mass,best_value = mass,value_sum
    return {'bid':best_bid,'gain':ratio(best_gain,total),
            'win_probability':ratio(best_mass,total),
            'win_value':ratio(best_value,best_mass) if best_mass else None}'''


def add_coding(add, tasks):
    def code(suffix, title, level, prompt, signature, samples, tests, solution, explanation):
        add('c_l24_' + suffix, title, level, 'Strategic inference and calibration',
            prompt, signature, samples, tests, solution, explanation)
        tasks[-1]['path'] = 'trader'

    code('medium', 'Decompose a weighted Brier score without rounding', 'Medium',
        r'''probabilities, outcomes and weights are equal-length lists, with 1≤n≤50000. Forecast ticks p are integers in [0,D], where scale D is an integer in [1,10^9]; the actual forecast is p/D. Outcomes are zero or one. Weights are integers in [0,10^9], with positive total W; they represent evaluation mass, not necessarily independent repetitions. There are at most FIFTY distinct forecast ticks. Group records by EXACTLY IDENTICAL forecast ticks, discarding zero-weight groups. For group \(g\), define weighted mass \(N_g\), weighted success mass \(S_g\), forecast \(f_g=p_g/D\) and rate \(r_g=S_g/N_g\); define global rate \(r=\sum_i w_i y_i/W\). Return a dict with these four exact quantities:

\[\begin{aligned}\mathrm{score}&=\sum_i w_i(f_i-y_i)^2/W,\\\mathrm{reliability}&=\sum_g N_g(f_g-r_g)^2/W,\\\mathrm{resolution}&=\sum_g N_g(r_g-r)^2/W,\\\mathrm{uncertainty}&=r(1-r).\end{aligned}\]

Each value must be ONE reduced fraction STRING "numerator/denominator", with canonical decimal integers and a positive denominator; zero is "\(\texttt{0/1}\)". Preserve all inputs. Use O(n+g) arithmetic operations and O(g) group state, g≤50; integer bit/gcd costs are additional. Do not use floats, merge nearby forecasts into coarse bins, or treat small empirical reliability as proof of population calibration. The identity score=uncertainty−resolution+reliability must hold for this exact grouping.''',
        'def solve(probabilities, outcomes, weights, scale):',
        [{'args':[[1]*4+[3]*4,[1,0,0,0,1,1,1,0],[1]*8,4],
          'expected':score_result(Fraction(3,16),0,Fraction(1,16),Fraction(1,4))},
         {'args':[[1,1],[0,1],[1,1],2],
          'expected':score_result(Fraction(1,4),0,0,Fraction(1,4))},
         {'args':[[1,999999999],[1,0],[10**9,999999999],10**9],
          'expected':score_result(Fraction(999999998000000001,10**18),Fraction(999999998000000001,10**18),Fraction(999999999000000000,3999999996000000001),Fraction(999999999000000000,3999999996000000001))}],
        [{'args':[[0,10],[0,1],[5,7],10],'expected':score_result(0,0,Fraction(35,144),Fraction(35,144))},
         {'args':[[0,1,2],[1,0,1],[0,2,0],2],'expected':score_result(Fraction(1,4),Fraction(1,4),0,0)},
         {'args':[[1,1],[1,1],[2,3],4],'expected':score_result(Fraction(9,16),Fraction(9,16),0,0)},
         {'args':[[1,3],[0,1],[2,2],4],'expected':score_result(Fraction(1,16),Fraction(1,16),Fraction(1,4),Fraction(1,4))},
         {'args':[[0,1]*25000,[0,1]*25000,[1]*50000,1],
          'expected':score_result(0,0,Fraction(1,4),Fraction(1,4))}],
        MEDIUM_REFERENCE,
        r'''The grouping is part of the mathematics. Let A=Σw_i p_i², B=Σw_i p_i y_i, S=Σw_i y_i and W=Σw_i. Aggregate each exact forecast level into (N_g,S_g), then form the rational T=Σ_g S_g²/N_g. Direct loss is (A−2DB+D²S)/(WD²). Expanding the group squares gives reliability (A−2DB)/(WD²)+T/W; resolution is T/W−S²/W²; uncertainty is S/W−S²/W². Their signed combination cancels T and S²/W² to recover direct score. Within a group, y²=y and the forecast is constant; a coarse bin with different forecasts would lose terms, just as in the paired-record interview problem. Reduce the sum T after every addition using gcd, and reduce each returned fraction. Zero weights carry no evaluation mass. In sample one the two exact rates equal their forecasts, giving reliability zero and resolution 1/16. This is a finite weighted identity; empirical rates and resolution can overfit without validating future forecasts.''')

    code('hard', 'Choose a bid using the value–rival joint law', 'Hard',
        r'''states contains 1≤n≤20000 rows [net_value, highest_rival_bid, weight]. These describe a discrete JOINT law already conditional on your observed information: value V is an integer in [−10^9,10^9], highest rival bid H is an integer in [0,10^9], and weight is an integer in [0,10^9], with positive total W. Negative V represents a net terminal value after liabilities. cap is an integer in [0,10^9]. Choose an INTEGER bid b∈[0,cap]. You win only when b>H; ties LOSE. On a win, gain is V−b; otherwise zero. Rival laws stay fixed when choosing b; no independence or equilibrium is assumed. Maximise expected gain, breaking ties by the SMALLEST bid. Return {"bid":b,"gain":fraction_text,"win_probability":fraction_text,"win_value":fraction_text_or_None}. The latter is E[V|winning at the SELECTED bid], or None for zero winning mass. Every fraction is a reduced canonical decimal STRING "numerator/positive_denominator"; zero is "\(\texttt{0/1}\)". Preserve the input. Use O(n log n) comparisons/arithmetic and O(n) auxiliary storage or better, with integer bit/gcd costs additional; do not scan every bid through cap. Evaluate duplicate rival thresholds as one complete group. A fixed conditional winning value cannot be used unchanged to optimise all actions.''',
        'def solve(states, cap):',
        [{'args':[[[0,0,48],[0,20,27],[100,0,4],[100,20,21]],21],
          'expected':bid_result(21,4,1,25)},
         {'args':[[[100,0,1],[200,100,1]],200],
          'expected':bid_result(1,Fraction(99,2),Fraction(1,2),100)},
         {'args':[[[0,0,10**9],[10**9,0,999999999]],1],
          'expected':bid_result(1,Fraction(999999997000000001,1999999999),1,Fraction(999999999000000000,1999999999))}],
        [{'args':[[[0,0,48],[0,20,27],[100,0,4],[100,20,21]],20],
          'expected':bid_result(1,Fraction(87,25),Fraction(13,25),Fraction(100,13))},
         {'args':[[[10,0,1],[5,2,1]],3],'expected':bid_result(1,Fraction(9,2),Fraction(1,2),10)},
         {'args':[[[1,0,1],[-10,5,7]],1],'expected':bid_result(0,0,0,None)},
         {'args':[[[10**9,10**9,1]],10**9],'expected':bid_result(0,0,0,None)},
         {'args':[[[-5,0,2],[10**9,0,0]],0],'expected':bid_result(0,0,0,None)},
         {'args':[[[9,4,1],[-20,4,1],[100,100,0]],100],
          'expected':bid_result(0,0,0,None)},
         {'args':[[[100,999,1] for _ in range(20000)],10**9],
          'expected':bid_result(0,0,0,None)}],
        HARD_REFERENCE,
        r'''Start with bid zero, which wins no states because H is nonnegative and ties lose. Its gain is zero. The winning set changes only at b=H+1. Between two consecutive such INTEGER breakpoints, winning mass and weighted value stay fixed, while subtracting b times positive winning mass makes gain decrease. Therefore only zero and distinct thresholds H+1≤cap can be optimal; extra zero-mass thresholds do not invalidate this reasoning. Sort by H and add EVERY row sharing a threshold before evaluating its candidate. Maintain cumulative mass M and weighted value A. Candidate gain numerator is A−bM over the common denominator W, so compare integers without rounding. Process bids ascending and update only on strictly greater gain to retain the smallest bid on ties. Remember the chosen M and A for win probability M/W and value A/M; use None when M=0. The conditional mean can be much higher than the selected bid and changes at each new winning set. In sample one, admitting all four states at bid twenty-one beats the narrow low-threshold subset; cap twenty instead makes that admission impossible. Summaries that keep only marginal means of V and H cannot replace their joint pairing. This is risk-neutral optimisation under a declared fixed law, not an inferred auction equilibrium.''')
