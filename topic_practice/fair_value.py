"""Conditional payments, executable actions and model ambiguity, kept distinct."""


def add_questions(add, questions):
    def question(suffix, title, level, minutes, prompt, answer, hints, solution,
                 follow, follow_solution, rubric):
        add('q_l19_'+suffix, title, 'Expected value', level, 'trader', minutes,
            prompt, answer, hints, solution, follow, follow_solution, 'l19')
        questions[-1]['rubric'] = rubric
        for key in ('prompt', 'solution', 'followSolution'):
            questions[-1][key] = questions[-1][key].replace(r'\n\n', '\n\n')

    # Keep this permanent numeric assessment and its follow-up unchanged.
    old = next(q for q in questions if q['id'] == 'q35')
    old['rubric'] = [
        'Use the sum of three die means to obtain 10.5, separately from the quoted midpoint.',
        'Compare buying at 11 and selling at 10 with expected payoff 10.5.',
        'After a six, retain its payment and use independence for the other two means to obtain 13.'
    ]

    question('e2', 'A settlement edge is not an early-exit profit', 'Easy', 8,
        r'A contract has conditional expected terminal cash payment 106. A dealer’s executable bid / ask is 104 / 105. You BUY one contract now; a purchase costs an additional 0.25 and there is no settlement fee. Interest is zero. Under expected-cash-profit preferences, what is the expected NET profit if you hold to settlement? Your quote is guaranteed executable and carries no extra information about the payment. An alternative plan is to sell before settlement at a guaranteed executable bid 104.5, paying another 0.25 sale fee. Explain why the two plans have different answers. Prices already contain the spread.',
        .75,
        ['A taker buys at the dealer’s ask, not its bid or midpoint.',
         'For holding, subtract 105 and the one applicable fee from 106.'],
        r'Holding gives expected net profit 106−105−0.25=0.75. The early exit instead gives cash profit 104.5−105−0.25−0.25=−1.00. Its exit payment is the bid you receive, not the still-uncertain terminal payment you no longer own. Do not subtract an extra bid–ask spread: the entry ask and exit bid already account for it. A positive settlement expectation is not a promise about an executable early exit, nor a guarantee of a gain at settlement.',
        r'If you instead SELL short one contract at the original bid and hold it to settlement, what is expected net profit when the sale fee is 0.25? If a second identical contract settles on the SAME underlying outcome, do two contracts remove the risk?',
        r'The short receives 104, pays 0.25 to trade and owes the terminal payment: expected net profit 104−0.25−106=−2.25. Two identical contracts on the same outcome double the random cash profit or loss; they do not make independent trials or diversify that exposure. Cash-flow signs, number of fees and the actual exit/settlement objective must be specified separately.',
        ['Buy at ask 105 and get 0.75 after the stated purchase fee.',
         'Use exit bid 104.5 and two fees to obtain −1, without subtracting spread twice.',
         'Obtain short edge −2.25 and identify shared, rather than independent, settlement risk.'])

    question('m1', 'A signal about one component moves both', 'Medium', 22,
        r'A contract pays V=A+B. The joint probabilities for (A,B)=(0,0),(0,10),(10,0),(10,10) are 0.4,0.1,0.1,0.4. A binary signal H/L is conditionally independent of B GIVEN A, with P(H|A=10)=3/4 and P(H|A=0)=1/4. You see H before acting. Derive the posterior weights and E[V|H]; explain whether updating A but leaving E[B]=5 is justified. A still-executable dealer quote is bid 12 / ask 14.5; either trade costs 0.25, interest is zero, shorting is allowed and the objective is expected cash profit at settlement. Should you buy, sell or abstain? Quote availability adds no further information.',
        None,
        ['Weight each JOINT record by its signal likelihood before normalising.',
         'The denominator is P(H), not the probability of the high A state.',
         'Conditional independence given A does not make A and B independent.'],
        r'The unnormalised H weights are 0.1,0.025,0.075,0.3. They sum to P(H)=1/2; posterior weights are 1/5,1/20,3/20,3/5. Thus\n\n\[\begin{aligned}E[A\mid H]&=10(3/20+3/5)=15/2,\\E[B\mid H]&=10(1/20+3/5)=13/2,\\E[V\mid H]&=14.\end{aligned}\]\n\nLearning about A also moves B because their joint distribution is dependent. Updating only A gives the incorrect value 12.5; treating H as a perfect reveal gives another incorrect value 15. The actual net buy edge is 14−14.5−0.25=−0.75 and sell edge is 12−14−0.25=−2.25. Abstain. The posterior is about specified payments, not a midpoint or a realised payout.',
        r'Now you also learn that B=10. What is E[V|H,B=10]? Separately compute E[V|L] and check that averaging over H/L recovers the prior E[V]. Does “the conditional means average back” imply no benefit from choosing an action after a signal?',
        r'Among the B=10 records after H, the weights are 1/20 and 3/5. The probability A=10 is (3/5)/(13/20)=12/13, so E[V|H,B=10]=10+120/13=250/13. For L the posterior weights are 3/5,3/20,1/20,1/5, giving E[V|L]=6. Hence (1/2)14+(1/2)6=10, equal to the prior mean. This is the tower property for one specified payment. Optimising a buy/sell/abstain action AFTER a signal applies a maximum to conditional edges; a maximum does not commute with averaging. Information can change the chosen action even when mean payoff averages back, provided that those actions/prices remain available.',
        ['Normalise the four joint H weights by 1/2 and obtain means 7.5, 6.5 and 14.',
         'Explain how dependence updates B despite conditional independence of the signal given A.',
         'Use the correct executable sides/costs and abstain on edges −0.75 and −2.25.',
         'Derive 250/13 after both observations and verify L mean six and the tower identity.',
         'Separate the expected payment from the value of an information-dependent action.'])

    question('m2', 'A physical expectation and a replicated price', 'Medium', 23,
        r'In a one-period, frictionless two-state market, cash has gross return one. A traded asset costs S0=5 and pays 2 in the low state or 8 in the high state. Both states are possible; your physical probability of high is 3/4. A new claim pays 1 in low and 13 in high. Fractional holdings, borrowing and shorting at these prices are allowed. Find the claim’s physical expected payoff and the cost of a portfolio that replicates its payment in BOTH states. Derive the no-arbitrage claim price and its risk-neutral weighting. Explain why replacing that weighting with your physical probability is not a replication argument.',
        None,
        ['Match the high-minus-low claim payment using units of the traded asset.',
         'Use the low state to determine the cash holding; it may be negative.',
         'A risk-neutral high weight makes the asset’s weighted payoff equal its current price.'],
        r'The physical expected payment is (1/4)1+(3/4)13=10. Matching the claim’s payoff difference gives delta=(13−1)/(8−2)=2 asset units. The cash holding is 1−2×2=−3: borrow three. Portfolio payment is two times the asset payment minus three, namely one or thirteen, and current cost is 2×5−3=7. An independently tradable claim must have price seven in this ideal market: if it trades above seven, sell it and buy the replicator; if below, buy it and sell the replicator. Either mismatch releases positive initial cash with exactly offsetting terminal payments.\n\nThe risk-neutral high weight q solves 2(1−q)+8q=5, hence q=1/2. Weighting the claim gives (1/2)1+(1/2)13=7. This q is inferred from traded prices and replication, not a forecast that high occurs half the time. Physical mean ten and replicated price seven answer different questions; neither calculation contradicts the other.',
        r'Suppose the claim has executable bid 6 / ask 8. Under your physical probabilities, buying at eight has positive expected profit. Is that an arbitrage? Can the physical probability change the replicating cost? What fails if borrowing/shorting is prohibited or a third state is added?',
        r'Buying at eight has expected profit 10−8=2 but loses seven in low, so it is not an arbitrage. The replicated value seven lies inside 6 / 8: buying the claim for eight or selling it for six does not lock in an arbitrage against the cost-seven replicator. If replication remains feasible, obtaining the same terminal payment through the cost-seven portfolio improves the physical expected profit, but it still has state risk when financed. Altering physical probabilities changes predicted profit, not the two state-matching equations or cost. Constraints can prevent the offsetting arbitrage portfolios; a third state generally adds a third payment equation with only two holdings, so arbitrary claims may cease to be replicable. Uniqueness here depends on the declared complete, frictionless two-state market.',
        ['Compute physical mean ten separately from delta two, cash −3 and replicating cost seven.',
         'Explain both directions of a price-mismatch arbitrage with offset terminal payments.',
         'Derive risk-neutral q=1/2 from the traded asset price, without calling it the physical probability.',
         'Separate positive physical expectation from arbitrage and explain the spread/constraint/third-state limits.'])

    question('h1', 'The value of a signal depends on the actions left open', 'Hard', 30,
        r'A contract pays zero or ten with equal prior probabilities. You may take AT MOST one action: buy one at ask six, sell one at bid four, or abstain. A trade costs an extra 1/2; settlement and financing cost nothing. A binary H/L signal has P(H|V=10)=4/5 and P(H|V=0)=1/5. Its acquisition fee f is paid once, whether you trade or abstain. First assume the quote is guaranteed to stay available after the signal and adds no other information. Derive the optimal signal-dependent policy, expected profit BEFORE its acquisition fee and the largest break-even f. Then prove why cost-free additional information cannot reduce the optimal expected profit under fixed available actions. State the exact assumptions needed; the payoff mean itself averages back.',
        None,
        ['For conditional mean m, optimise g(m)=max(0,m−6.5,3.5−m).',
         'Compute both signal probabilities and posterior means; do not pay the acquisition fee only when trading.',
         'A maximum of affine functions is convex, or you may imitate the old action after every signal.'],
        r'Before information the mean is five, giving buy and sell edge −1.5; abstain for zero. P(H)=P(L)=1/2, posterior means are eight and two. After H buy for expected net trading profit 8−6−0.5=1.5; after L sell for 4−2−0.5=1.5. Expected trading profit is 1.5, so total expected profit is 1.5−f. Break-even is f=1.5 (indifferent to not acquiring); strictly preferable when f<1.5. Costs already incurred to obtain information are common to the later actions and must not be charged only on fills.\n\nFor a generic available signal S and finite payoff expectation, let \(m_S=E[V\mid S]\). Fixed executable prices and fees give\n\n\[g(m)=\max\{0,m-a-c_b,b-m-c_s\}.\]\n\nThe no-trade option has zero; the other terms are affine. Consequently g is convex and\n\n\[E[g(m_S)]\geq g(E[m_S])=g(E[V]).\]\n\nEquivalently, after observing S you could ignore it and use the old action; maximising cannot do worse than that feasible baseline. This requires unchanged feasible actions and prices, expected-cash-profit evaluation, and the signal as the only new conditioning information relevant to those executions. It is a statement about gross information value before its acquisition cost. It is not a claim that every signal makes money, or that the average conditional payment rises.',
        r'Now the dealer sees the same signal and replaces its quote by bid \(m_S-1\) / ask \(m_S+1\) before you can act; trading still costs 1/2. What is the value of buying the signal for f=1? Compare with a PERFECT signal when the original quote stays fixed. Can a positive expected information value guarantee a realised profit?',
        r'With the updated quote, either trade loses 1.5 in conditional expectation; abstain. Acquiring for f=1 produces −1, so do not acquire. The fixed-action proof never promised that a dealer would leave a stale price executable. With perfect information and the original quote, buy at V=10 for net trading profit 3.5 or sell at V=0 for 3.5, so gross information value is 3.5, two more than the noisy signal. With the noisy signal, H can occur in the zero state (conditional probability 1/5), causing buy loss 6.5 before acquisition cost. L can occur in the ten state, causing sell loss 6.5. Positive expected information value under a model is compatible with an actual loss. Acquisition cost and loss tolerance are separate decisions.',
        ['Derive both posterior means and signal weights, and choose buy after H/sell after L.',
         'Average the optimised conditional edges to 1.5 and charge f on every signal acquisition.',
         'Prove the inequality by convexity/tower property or by feasibility of the old action.',
         'State the fixed executable action set and expected-profit assumptions explicitly.',
         'Reject signal purchase after quote updating, compute perfect-information value 3.5 and exhibit a noisy-signal loss.'])

    question('h2', 'A set of models is not a mixture of models', 'Hard', 32,
        r'A contract pays V=12 or zero. The prior high-state probability p is only known to lie in [1/4,3/4]; this is a SET of possible priors, not a probability distribution over p. A signal H has P(H|V=12)=3/4 and P(H|V=0)=1/4 under every model. You observe H, then may buy one at ask nine, sell one at bid eight, or abstain; either trade costs 1/4. Quotes are still executable and add no information, interest is zero and the objective is worst-case CONDITIONAL expected cash profit across the model set. Derive the posterior fair-value interval, worst-case buy/sell edges and optimal robust action. Could randomising between buy, sell and abstain strictly improve that minimax value? Do not average posterior endpoints as if ambiguity supplied probabilities.',
        None,
        ['Normalising a likelihood-weighted prior produces a ratio in p.',
         'A buy is hurt by the LOWEST conditional mean, a sale by the HIGHEST.',
         'To rule out randomisation, look for one allowed model that hurts both trading actions simultaneously.'],
        r'For any fixed allowed p, P(H)=(1+2p)/4 is positive, and\n\n\[m(p)=E[V\mid H,p]=\frac{36p}{1+2p}.\]\n\nIts derivative is 36/(1+2p)²>0. Endpoints give m(1/4)=6 and m(3/4)=54/5, so the conditional value interval is [6,10.8]. Net buy edge is m−37/4, with worst case 6−37/4=−13/4. Sell edge is 31/4−m, with worst case 31/4−54/5=−61/20. Abstention has worst-case profit zero and is optimal among deterministic actions.\n\nOne must not simply mix the TWO DIFFERENT worst-case endpoints to assess a randomised policy: one model governs its average payoff. At the allowed p=1/2, m=9, buy edge is −1/4 and sell edge −5/4. Any mixture with positive trading probability has negative conditional expected profit in this single model; its worst case is therefore negative. Pure abstention attains zero. This common adverse model proves that randomisation cannot strictly improve the minimax value.',
        r'Change the interpretation: before any signal, a hidden model is p=1/4 or p=3/4 with equal probability, then V and H are drawn from that model. Compute the model probabilities AFTER H and the mixture E[V|H]. Why is the average of the two posterior values with equal weights incorrect? Does this new answer remove the original ambiguity?',
        r'The signal probabilities under the low/high models are 3/8 and 5/8. With equal PRIOR model weights, posterior model weights become 3/8 and 5/8 (their normalising signal probability is 1/2). Thus mixture value is (3/8)6+(5/8)(54/5)=9, also obtained by first marginalising to prior high probability 1/2 and then applying Bayes. The naive equal average of posterior values is 42/5=8.4; it failed to update model weights after observing H. This hierarchy is an additional modelling choice with assigned model probabilities. It does not turn the earlier set-valued uncertainty into an empirical fact or change its minimax answer. Within-model conditioning, across-model mixing and worst-case optimisation are three distinct operations.',
        ['Derive and normalise m(p), prove monotonicity and obtain interval [6,54/5].',
         'Compute worst-case buy −13/4, sell −61/20 and choose abstention.',
         'Rule out randomisation using one allowed p=1/2, rather than mixing incompatible adverse models.',
         'Update hierarchical model weights to 3/8 and 5/8 and compute mixture value nine.',
         'Explain why equal posterior averaging gives 8.4 and why a model mixture differs from a prior set.'])


FRACTION_HELPERS = '''from math import gcd

def rational(numerator, denominator):
    factor = gcd(abs(numerator), denominator)
    return [str(numerator // factor), str(denominator // factor)]

def result(numerator, denominator, bid, ask, buy_cost, sell_cost):
    buy = numerator - (ask + buy_cost) * denominator
    sell = (bid - sell_cost) * denominator - numerator
    action = 'buy' if buy > 0 else 'sell' if sell > 0 else 'wait'
    return {'value': rational(numerator, denominator),
            'buy_edge': rational(buy, denominator),
            'sell_edge': rational(sell, denominator), 'action': action}
'''


def add_coding(add, tasks):
    def code(suffix, title, level, prompt, signature, samples, tests, solution, explanation):
        add('c_l19_'+suffix, title, level, 'Expected value', prompt, signature,
            samples, tests, solution, explanation)
        tasks[-1]['path'] = 'trader'
        for key in ('prompt', 'explanation'):
            tasks[-1][key] = tasks[-1][key].replace(r'\n\n', '\n\n')

    code('easy', 'Exact payoff weights and executable edges', 'Easy',
         r'payoffs and weights are equally long lists of n integers, 1≤n≤100000. Payoffs are in [−10^9,10^9]; weights are in [0,10^9] and have positive sum W. Each state’s physical probability is weights[i]/W; zero-weight states are impossible. bid and ask are integer executable sale/purchase prices in [−10^9,10^9], with bid≤ask. buy_cost and sell_cost are nonnegative integer per-trade fees at most 10^9. All payments are in the same unit, financing is zero and settlement adds no fee/information. Return a dictionary with value, buy_edge, sell_edge and action. Each of the first three is an EXACT reduced rational [numerator_string,denominator_string], with positive denominator, no leading zeros or plus sign, and zero written ["0","1"]. Integers must also use denominator "1". action is "buy" if value−ask−buy_cost>0, "sell" if bid−value−sell_cost>0, otherwise "wait". At zero edge choose wait. The noncrossed quote and nonnegative fees ensure both directions cannot be positive. Preserve both lists. Use O(n) arithmetic operations and O(1) auxiliary integer state; integer bit costs depend on magnitude. Do not simulate, round or convert the exact arithmetic to float.',
         'def solve(payoffs, weights, bid, ask, buy_cost, sell_cost):',
         [{'args':[[0,10,20],[1,2,1],9,11,1,0], 'expected':{'value':['10','1'],'buy_edge':['-2','1'],'sell_edge':['-1','1'],'action':'wait'}},
          {'args':[[-3,7],[2,1],0,0,0,0], 'expected':{'value':['1','3'],'buy_edge':['1','3'],'sell_edge':['-1','3'],'action':'buy'}}],
         [{'args':[[9],[5],10,12,1,0], 'expected':{'value':['9','1'],'buy_edge':['-4','1'],'sell_edge':['1','1'],'action':'sell'}},
          {'args':[[4,999],[3,0],4,4,0,0], 'expected':{'value':['4','1'],'buy_edge':['0','1'],'sell_edge':['0','1'],'action':'wait'}},
          {'args':[[-7,-7],[1,9],-10,-8,1,2], 'expected':{'value':['-7','1'],'buy_edge':['0','1'],'sell_edge':['-5','1'],'action':'wait'}},
          {'args':[[10**9,-10**9],[10**9,10**9-1],0,1,0,0], 'expected':{'value':['1000000000','1999999999'],'buy_edge':['-999999999','1999999999'],'sell_edge':['-1000000000','1999999999'],'action':'wait'}},
          {'args':[[0]*100000,[1]*100000,-1,0,0,0], 'expected':{'value':['0','1'],'buy_edge':['0','1'],'sell_edge':['-1','1'],'action':'wait'}}],
         FRACTION_HELPERS+'''\ndef solve(payoffs, weights, bid, ask, buy_cost, sell_cost):
    numerator = denominator = 0
    for payoff, weight in zip(payoffs, weights):
        numerator += payoff * weight
        denominator += weight
    return result(numerator, denominator, bid, ask, buy_cost, sell_cost)''',
         r'Compute the weighted sum N=Σw_i v_i and mass W=Σw_i using Python integers. The mean is N/W; edge numerators are N−(ask+buy_cost)W and (bid−sell_cost)W−N, all over W. Their signs decide the action without a floating threshold. Reduce each rational by its gcd and return decimal strings so the browser cannot lose large integers. Zero reduces canonically to 0/1. One pass uses O(n) arithmetic operations and O(1) auxiliary integers; gcd and multiplications are not constant bit-cost operations for unbounded integers. The midpoint never enters the calculation.')

    code('medium', 'Value every possible noisy signal', 'Medium',
         r'payoffs and weights are equally long integer lists for n states, 1≤n≤2000. Payoffs are in [−10^9,10^9]; weights are in [0,10^9] and total W is positive. State i has prior probability weights[i]/W. likelihoods is an n×k matrix of NONNEGATIVE integer counts, 1≤k≤100 and n×k≤100000. Every row has the SAME positive total D≤10^9; P(signal=j | state=i)=likelihoods[i][j]/D. Entries are at most 10^9. These are conditional likelihoods, not state probabilities; payoff states may encode dependent components. bid and ask are integer executable sale/purchase prices in [−10^9,10^9], with bid≤ask. buy_cost and sell_cost are additional nonnegative integer trade fees at most 10^9. All amounts share a currency unit; financing and settlement costs are zero. Quotes remain executable after each signal with no extra information. Return k dictionaries in signal-column order. For each reachable signal use keys probability, value, buy_edge, sell_edge, action: probability is its exact marginal P(signal=j); value and edges are its exact conditional quantities; action is "buy" when value−ask−buy_cost>0, "sell" when bid−value−sell_cost>0, otherwise "wait" (zero edge waits). Both edges cannot be positive under these quote/fee assumptions. All rational values use reduced [numerator_string,denominator_string], including integers/zero. If a signal has ZERO marginal probability, return probability=["0","1"], value=None, buy_edge=None, sell_edge=None, action="unreachable"; do not invent a conditional mean or normalise zero. Preserve all inputs. Use O(nk) arithmetic operations and O(k) auxiliary integers, excluding output. No simulation or floats. Input contracts are guaranteed, not validation tasks.',
         'def solve(payoffs, weights, likelihoods, bid, ask, buy_cost, sell_cost):',
         [{'args':[[0,10],[1,1],[[4,1],[1,4]],4,6,0,0], 'expected':[
             {'probability':['1','2'],'value':['2','1'],'buy_edge':['-4','1'],'sell_edge':['2','1'],'action':'sell'},
             {'probability':['1','2'],'value':['8','1'],'buy_edge':['2','1'],'sell_edge':['-4','1'],'action':'buy'}]},
          {'args':[[7,100],[3,0],[[0,2],[2,0]],6,8,0,0], 'expected':[
              {'probability':['0','1'],'value':None,'buy_edge':None,'sell_edge':None,'action':'unreachable'},
              {'probability':['1','1'],'value':['7','1'],'buy_edge':['-1','1'],'sell_edge':['-1','1'],'action':'wait'}]}],
         [{'args':[[-3],[2],[[1,1,0]],-3,-3,0,0], 'expected':[
             {'probability':['1','2'],'value':['-3','1'],'buy_edge':['0','1'],'sell_edge':['0','1'],'action':'wait'},
             {'probability':['1','2'],'value':['-3','1'],'buy_edge':['0','1'],'sell_edge':['0','1'],'action':'wait'},
             {'probability':['0','1'],'value':None,'buy_edge':None,'sell_edge':None,'action':'unreachable'}]},
          {'args':[[0,10,10,20],[4,1,1,4],[[1,3],[1,3],[3,1],[3,1]],12,15,0,0], 'expected':[
              {'probability':['1','2'],'value':['14','1'],'buy_edge':['-1','1'],'sell_edge':['-2','1'],'action':'wait'},
              {'probability':['1','2'],'value':['6','1'],'buy_edge':['-9','1'],'sell_edge':['6','1'],'action':'sell'}]},
          {'args':[[10**9,-10**9],[10**9,10**9-1],[[10**9,0],[10**9-1,1]],0,1,0,0], 'expected':[
              {'probability':['1999999998000000001','1999999999000000000'],'value':['1999999999000000000','1999999998000000001'],'buy_edge':['999999999','1999999998000000001'],'sell_edge':['-1999999999000000000','1999999998000000001'],'action':'buy'},
              {'probability':['999999999','1999999999000000000'],'value':['-1000000000','1'],'buy_edge':['-1000000001','1'],'sell_edge':['1000000000','1'],'action':'sell'}]},
          {'args':[[7]*2000,[1]*2000,[[1]*50 for _ in range(2000)],6,8,0,0], 'expected':[
              {'probability':['1','50'],'value':['7','1'],'buy_edge':['-1','1'],'sell_edge':['-1','1'],'action':'wait'} for _ in range(50)]}],
         FRACTION_HELPERS+'''\ndef solve(payoffs, weights, likelihoods, bid, ask, buy_cost, sell_cost):
    k = len(likelihoods[0])
    mass = [0] * k
    numerator = [0] * k
    total = sum(weights) * sum(likelihoods[0])
    for payoff, weight, row in zip(payoffs, weights, likelihoods):
        for j, count in enumerate(row):
            joint = weight * count
            mass[j] += joint
            numerator[j] += joint * payoff
    output = []
    for j, denominator in enumerate(mass):
        if denominator == 0:
            item = {'value': None, 'buy_edge': None, 'sell_edge': None,
                    'action': 'unreachable'}
        else:
            item = result(numerator[j], denominator, bid, ask, buy_cost, sell_cost)
        item['probability'] = rational(denominator, total)
        output.append(item)
    return output''',
         r'For signal j, retain Z_j=Σw_i L_ij and N_j=Σw_i L_ij v_i. The common denominator of the joint model is WD, hence marginal probability Z_j/(WD). If Z_j>0, its conditional mean is N_j/Z_j: W and D cancel. If Z_j=0 there is no conditional expectation under this model; mark unreachable explicitly. Do not divide by the state count, use signal counts alone or keep the prior mean unchanged. Integer accumulation and reduction preserve exact quantities beyond binary64. As a conservation check, ΣP(j)=1 and ΣP(j)E[V|j]=E[V] over reachable signals. This does not mean that the optimised actions average to the prior action. The nested pass uses O(nk) arithmetic operations and two length-k working arrays.')

    code('hard', 'Robust conditional value over bounded prior weights', 'Hard',
         r'There are \(1\leq n\leq12\) states with integer payoffs in [−10^9,10^9]. For an OBSERVED signal H, likelihoods[i] is an integer in [1,10^9], interpreted as P(H|state i)=likelihoods[i]/10^9; the complement is the other signal. Write \(v_i=\mathrm{payoffs}[i]\) and \(L_i=\mathrm{likelihoods}[i]\). Unknown REAL prior weights \(w_i\) obey \(\mathrm{lower}[i]\leq w_i\leq\mathrm{upper}[i]\) and \(\sum_i w_i=\mathrm{mass}\). Bounds and mass are integers in [0,10^9], mass>0, lower≤upper, and sum(lower)≤mass≤sum(upper), so the set is nonempty. The prior probability of state i is \(w_i/\mathrm{mass}\). A set of priors has NO assigned model probabilities. Strictly positive likelihoods ensure every allowed prior gives H positive probability.\n\nFind EXACT minimum and maximum over this bounded set of\n\n\[m(w)=\frac{\sum_i w_i L_i v_i}{\sum_i w_i L_i}.\]\n\n Return {"minimum":[num,den],"maximum":[num,den],"buy_floor":[num,den],"sell_floor":[num,den],"action":...}, with ALL num/den entries canonical reduced decimal STRINGS (positive denominator; zero=["0","1"]). bid and ask are integer executable sale/purchase prices in [−10^9,10^9], with bid≤ask; buy_cost and sell_cost are additional nonnegative integer trade fees at most 10^9. All amounts share a currency unit and settlement adds no cost. buy_floor is the worst conditional expected profit of buying ONE contract at ask plus buy_cost; sell_floor is that of selling one at bid minus sell_cost. Select the deterministic action with strictly positive worst-case profit, otherwise "wait"; zero edge waits. The quote is fixed/executable with no additional selection information, financing zero. No quantities, randomisation or hedging are requested.\n\nPreserve all lists. Aim for \(O(n^2 2^{n-1})\) arithmetic operations with O(n) working entries, excluding output; account separately for integer bit costs. Hint for the algorithmic target: the box with one sum equality has vertices with at most ONE weight strictly between its bounds. Justify why optimising a ratio with a positive denominator can use these vertices; simply filling largest/smallest PAYOFFS first can fail because changing a weight also changes the conditioning denominator. Do not round, enumerate every integer composition of mass, or silently average model endpoints.',
         'def solve(payoffs, likelihoods, lower, upper, mass, bid, ask, buy_cost, sell_cost):',
         [{'args':[[0,5,10],[100,100,1],[5,0,0],[5,5,5],10,2,3,0,0], 'expected':{'minimum':['10','101'],'maximum':['5','2'],'buy_floor':['-293','101'],'sell_floor':['-1','2'],'action':'wait'}},
          {'args':[[0,12],[1,3],[1,1],[3,3],4,0,5,0,0], 'expected':{'minimum':['6','1'],'maximum':['54','5'],'buy_floor':['1','1'],'sell_floor':['-54','5'],'action':'buy'}}],
         [{'args':[[0,5,10],[100,100,1],[5,0,0],[5,5,5],10,4,5,0,0], 'expected':{'minimum':['10','101'],'maximum':['5','2'],'buy_floor':['-495','101'],'sell_floor':['3','2'],'action':'sell'}},
          {'args':[[-7],[13],[0],[100],10,-8,-7,0,0], 'expected':{'minimum':['-7','1'],'maximum':['-7','1'],'buy_floor':['0','1'],'sell_floor':['-1','1'],'action':'wait'}},
          {'args':[[0,99,-10],[1,100,7],[2,0,0],[2,0,0],2,-1,1,0,0], 'expected':{'minimum':['0','1'],'maximum':['0','1'],'buy_floor':['-1','1'],'sell_floor':['-1','1'],'action':'wait'}},
          {'args':[[0,2,4],[1,2,3],[0,0,0],[1,1,1],3,2,3,0,0], 'expected':{'minimum':['8','3'],'maximum':['8','3'],'buy_floor':['-1','3'],'sell_floor':['-2','3'],'action':'wait'}},
          {'args':[[0,2,4],[1,2,3],[1,1,1],[2,2,2],3,2,3,0,0], 'expected':{'minimum':['8','3'],'maximum':['8','3'],'buy_floor':['-1','3'],'sell_floor':['-2','3'],'action':'wait'}},
          {'args':[[10**9,-10**9],[10**9,10**9-1],[10**9-1,1],[10**9-1,1],10**9,0,10**9,0,0], 'expected':{'minimum':['999999999000000000','1000000001'],'maximum':['999999999000000000','1000000001'],'buy_floor':['-2000000000','1000000001'],'sell_floor':['-999999999000000000','1000000001'],'action':'wait'}},
          {'args':[list(range(1,13)),[10**9]*12,[0]*12,[10**9]*12,10**9,1,12,0,0], 'expected':{'minimum':['1','1'],'maximum':['12','1'],'buy_floor':['-11','1'],'sell_floor':['-11','1'],'action':'wait'}}],
         '''from itertools import product
from math import gcd

def rational(numerator, denominator):
    factor = gcd(abs(numerator), denominator)
    return [str(numerator // factor), str(denominator // factor)]

def solve(payoffs, likelihoods, lower, upper, mass, bid, ask, buy_cost, sell_cost):
    n = len(payoffs)
    minimum = maximum = None
    for free in range(n):
        others = [i for i in range(n) if i != free]
        for choices in product((0, 1), repeat=n-1):
            used = numerator = denominator = 0
            for i, choice in zip(others, choices):
                weight = upper[i] if choice else lower[i]
                used += weight
                joint = weight * likelihoods[i]
                numerator += joint * payoffs[i]
                denominator += joint
            weight = mass - used
            if not lower[free] <= weight <= upper[free]:
                continue
            joint = weight * likelihoods[free]
            numerator += joint * payoffs[free]
            denominator += joint
            if minimum is None or numerator * minimum[1] < minimum[0] * denominator:
                minimum = (numerator, denominator)
            if maximum is None or numerator * maximum[1] > maximum[0] * denominator:
                maximum = (numerator, denominator)
    lo, ld = minimum
    hi, hd = maximum
    buy = lo - (ask + buy_cost) * ld
    sell = (bid - sell_cost) * hd - hi
    return {'minimum': rational(lo, ld), 'maximum': rational(hi, hd),
            'buy_floor': rational(buy, ld), 'sell_floor': rational(sell, hd),
            'action': 'buy' if buy > 0 else 'sell' if sell > 0 else 'wait'}''',
         r'If two weights are strictly inside their bounds, perturb one by +ε and the other by −ε while keeping their sum. Small positive and negative ε stay feasible, so that point is not a vertex. Thus every vertex has at most one non-bound coordinate. Enumerate its possible free index, choose lower/upper for the other n−1 weights, and set the remaining weight from the sum constraint. All-bound vertices may appear repeatedly; degenerate/fixed bounds and n=1 need no special division. Feasibility ensures at least one vertex and positive likelihoods/mass ensure positive denominators.\n\nFor a feasible convex combination \(w=\sum_j\alpha_j u_j\) of vertices, write \(D_j=\sum_i u_{ji} L_i>0\). Its ratio satisfies\n\n\[m(w)=\sum_j\frac{\alpha_j D_j}{\sum_r\alpha_r D_r}\,m(u_j).\]\n\nThese are nonnegative weights summing to one, so m(w) lies between vertex ratios; a minimum and maximum occur at vertices. This is NOT an equal average of their posterior means. Vertex weights happen to be integers here because all bound weights and mass are integers; the proof still covers the requested REAL prior set. Compare ratios by integer cross-products, then reduce only the winning fractions. The buy worst case uses the minimum mean; the sell worst case uses the maximum. In the first sample, putting all five free weight units on payoff ten gives 10/101, while putting them on payoff five gives 5/2: strongest raw payoff need not give strongest conditional mean. Enumeration is \(O(n^2 2^{n-1})\) arithmetic operations and O(n) working entries, suitable for the stated n≤12, not a polynomial algorithm for an unbounded number of states. A robust positive expected edge is still a conditional model-set statement, not a guaranteed realised profit.')
