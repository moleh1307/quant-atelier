"""Selection denominators, price-dependent demand and belief/inventory decisions."""


def add_questions(add, questions):
    for id, rubric in {
        'q36': ['Compute buy mass 3/4 and buy-plus-high mass 1/2 under the stated independent types.',
                'Normalise to posterior high probability 2/3 and conditional value 200/3.',
                'Separate prior value 50 from value among fills; keep the fixed-behaviour qualification on the break-even ask.'],
        'q42': ['Explain how lowering both prices changes the quote centre and, under price-responsive demand, inventory-reducing versus inventory-increasing flow.',
                'Contrast symmetric widening, which changes width and can suppress both sides including inventory-reducing sales.',
                'Identify information, flow response, horizon, correlated exposure and constraints needed to choose; do not claim an unspecified optimum.',
                'Explain why standalone positive expectation does not make a trade feasible under capital or risk limits.']
    }.items():
        next(q for q in questions if q['id']==id)['rubric']=rubric

    def question(suffix,title,level,minutes,prompt,answer,hints,solution,follow,follow_solution,rubric):
        add('q_l20_'+suffix,title,'Market making',level,'trader',minutes,prompt,answer,hints,solution,follow,follow_solution,'l20')
        questions[-1]['rubric']=rubric
        for key in ('prompt','solution','followSolution'):
            questions[-1][key]=questions[-1][key].replace(r'\n\n','\n\n')

    question('e1','A fill rate is part of the profit calculation','Easy',8,
        r'A dealer starts with no inventory and offers one contract at ask 75. The probability of a sale during this single opportunity is 1/5. CONDITIONAL ON that sale, the contract’s expected terminal cash payment is 80. A filled sale incurs one unit of fees; no sale incurs no fee and creates no position. Interest is zero. What is expected net profit PER OPPORTUNITY? Also identify expected profit per fill and why using a prior value of 70 would answer the wrong question.',-1.2,
        ['The dealer receives the ask and owes the payment after a sale.', 'Multiply the conditional net edge by the probability of a sale; no sale contributes zero.'],
        r'Expected net profit per filled sale is 75−80−1=−6. Since an opportunity fills with probability 1/5 and otherwise contributes zero, expected net profit per opportunity is −6/5=−1.2. The prior value 70 describes the unselected population, while the liability on sold contracts has conditional mean 80. The quoted positive prior edge 75−70 is not the expected edge among executions. There is no additional spread to subtract when the entry ask and settlement payment are already specified.',
        r'An alternative quote earns a conditional net profit of two per sale but fills only with probability 1/100. What is its profit per opportunity? Can comparing only per-fill edge decide between quotes, or justify scaling quantity on one common settlement?',
        r'The alternative gives 2/100=1/50 per opportunity, positive under its declared model. Per-fill edge alone omits how often the action occurs: a rarer, larger edge can earn less per opportunity than a smaller frequent one. Multiplying contracts on the SAME settlement scales that common exposure; it does not create independent trials. Quote choice and permitted quantity also require costs, information, inventory and constraints to be specified.',
        ['Use sale cash-flow signs and one fee to obtain −6 per fill.', 'Include no-fill mass to obtain −6/5 per opportunity.', 'Reject the prior-mean substitution and separate frequency from conditional edge and shared risk.'])

    question('e2','Whose buy changes whose inventory?','Easy',8,
        r'A dealer’s signed inventory q=2 means it owns two contracts; negative inventory means a settlement liability. A CUSTOMER buys one contract from the dealer, with no other transaction. What is the dealer’s new q? Separately, its stated terminal inventory penalty is three times q squared. Compute the change in that penalty and contrast a customer SALE to the dealer. This is an accounting exercise, not an optimal-quote claim.',1,
        ['The customer takes a unit OUT of the dealer’s position.', 'Compare the penalty at the resulting inventory with the penalty at two.'],
        r'A customer buy is a dealer sale, so q changes from two to one. The penalty changes from 3×2²=12 to 3×1²=3, a reduction of nine. A customer sale is a dealer purchase: q becomes three and the penalty becomes 27, an increase of fifteen. Cash direction and inventory direction must be stated from the same party’s perspective. A quoted bid is the dealer’s buying price; an ask is its selling price.',
        r'If a filled dealer sale has zero expected cash trading edge under the CURRENT conditional payoff distribution, how does that nine-unit penalty reduction affect the change in the specified objective? Does this establish that lowering the ask is always optimal?',
        r'For expected cash trading profit MINUS the declared inventory penalty, zero trading edge plus a nine-unit penalty reduction gives an objective improvement of nine, when comparing the position change under the same current conditional information. This is an explicit preference/model, not free cash earned. It does not establish a quote optimum: changing ask can change fill probability, conditional payoff, feasible actions and information about existing inventory. Compare full action-dependent outcomes and limits before recommending a skew.',
        ['Translate customer buy into dealer sale and new inventory one.', 'Compute penalty changes −9 on a sale and +15 on a purchase.', 'Separate an objective improvement from cash profit and from an unspecified optimal quote.'])

    question('m1','The missing order is an observation too','Medium',23,
        r'A SINGLE terminal contract value V is zero or 100, with prior probabilities one half each. During each opportunity a customer buys with probability 3/4 if V=100 and 1/4 if V=0; otherwise no order occurs. Opportunities are conditionally independent GIVEN this same V. You observe Buy, No order, Buy in that order. Derive the posterior value, including the no-order likelihood. Then you post an executable ask 80 for the NEXT opportunity under the same rule, with no fees or financing. Compute the dealer’s expected profit per NEXT fill and per NEXT opportunity. Do not treat posting as execution or reset the prior for each order.',None,
        ['Multiply the three history likelihoods within each fixed state.', 'The next fill selects AGAIN from the posterior reached after the history.', 'Next-fill conditional value and current posterior value are different quantities.'],
        r'The history likelihood is (3/4)(1/4)(3/4)=9/64 in high and (1/4)(3/4)(1/4)=3/64 in low. Equal prior weights give posterior high probability 3/4 and current mean 75. Ignoring the no-order event would instead use two buys and get high probability 9/10.\n\nFor the NEXT buy, joint high-and-buy mass is (3/4)(3/4)=9/16; low-and-buy mass is (1/4)(1/4)=1/16. Hence next fill probability is 5/8 and next-fill mean is 90. Selling at ask 80 gives −10 per fill and −25/4 per opportunity. Comparing the ask only with current mean 75 misses the next execution’s selection. These results hold because the stated likelihoods remain unchanged at ask 80.',
        r'Derive posterior odds after b buys and n no-order events under these assumptions. What breaks if repeated orders come from a single counterparty whose hidden type persists? Can an unfilled order be ignored simply because it produces no trade cash flow?',
        r'With prior odds one, each buy multiplies odds by three and each no-order observation divides them by three. Posterior odds are \(3^{b-n}\); normalise odds o to high probability o/(1+o). No-order cash flow is zero but its state likelihood is informative. A persistent counterparty type can make observations dependent even conditional on V; the product likelihood then needs the joint process or a state that also tracks that type. The finite experiment’s conditional-independence assumption is essential, not a conclusion from observing a sequence.',
        ['Use all three state-specific history likelihoods and obtain current mean 75.', 'Recondition on the next fill to obtain mean 90 and fill rate 5/8.', 'Separate next-fill profit −10 from next-opportunity profit −25/4.', 'Derive the odds update and identify conditional independence/persistent-type limits.'])

    question('m2','Raising the ask changes who accepts it','Medium',25,
        r'V is zero or 100 with equal priors. A customer is independently informed with probability 1/2; an informed customer buys only when V STRICTLY exceeds the ask. An uninformed customer buys only at asks ≤60. The dealer may post ONE ask from {55,60,70,100} for one opportunity, or refrain from quoting. Each filled sale costs a fee of one; no trade costs zero. Interest is zero and inventory initially zero. For each quote, compute fill probability, conditional payment when defined, and expected net profit per opportunity. Choose an action using these quantities. Explain why keeping the posterior calculated at ask 55 while evaluating ask 70 is incorrect.',None,
        ['At 55 and 60 both uninformed branches and the informed high branch buy.', 'At 70 only informed high buys; at 100 informed high is indifferent and DOES NOT buy under the stipulated strict rule.', 'An empty fill event has no conditional mean but still gives zero per-opportunity profit.'],
        r'At 55 or 60 the fill probability is 3/4 and conditional value 200/3. Net profits per opportunity are (3/4)(55−1−200/3)=−19/2 and (3/4)(60−1−200/3)=−23/4. At 70 only the informed high branch fills, so fill probability 1/4, conditional value 100, and profit (1/4)(70−1−100)=−31/4. At 100 nobody buys: fill probability zero, conditional value undefined, opportunity profit zero. Refrain from quoting; an unfilled ask 100 ties at zero. Among quotes that can fill, 60 loses least, but it still loses. The likelihood changed at the uninformed participation threshold, so an old posterior cannot be transferred to a new quote.',
        r'Keep these behavioural rules but replace the informed fraction by α in [0,1]. At ask 60 with the same fee, derive net expected profit and the largest α for nonnegative profit. What does this say about claiming that no dealer can profit in general?',
        r'At ask 60, the high branch buys with total probability 1/2, and low buys with probability (1−α)/2. The fee-adjusted cash received per fill is 59. Expected profit is\n\n\[59(1-\alpha/2)-50=9-\frac{59}{2}\alpha.\]\n\nIt is nonnegative exactly when \(\alpha\leq18/59\). For α=1/2 this agrees with −23/4. The original no-positive-profit menu result belongs to its stated informed fraction, participation threshold and cost convention. It is not a universal impossibility theorem for real market making or a fitted demand model.',
        ['Recompute each quote’s eligible branches and distinguish zero fill from a defined conditional mean.', 'Obtain per-opportunity profits −19/2, −23/4, −31/4 and zero.', 'Choose refraining and reject a price-invariant posterior.', 'Derive 9−59α/2 and threshold 18/59 without generalising the toy demand model.'])

    question('h1','The best immediate edge can be the wrong first action','Hard',32,
        r'A fixed terminal V is zero or 12 with equal priors. A dealer starts at q=0 with zero cash and must always keep signed inventory in [−1,1]. There are TWO customer opportunities, followed by settlement of all remaining inventory at V. No fees, interest or risk penalty apply. At each opportunity the dealer can skip (no observation), post quote A, or post quote B. Under A the customer buys ONE from the dealer at ask 12 if V=12 and sends NO ORDER if V=0. Under B the customer SELLS ONE to the dealer at bid two in either state. These behaviours, including accepting at V=ask, are STIPULATED and remain available in the second opportunity. You observe the actual order or no-order event before choosing again. A whole quote is infeasible if any positive-probability resulting inventory would breach the limit; you cannot reject a filled branch retroactively. Derive the optimal first action and conditional second actions, with expected final cash-plus-inventory value. Compare an immediate-edge strategy that chooses B first. Explain which observations and state variables the optimal policy needs.',None,
        ['A has zero immediate expected trading edge, but its buy/no-order observations identify V.', 'After B first the dealer is long one; another B is infeasible.', 'Settle terminal inventory along each complete path before averaging.'],
        r'With one opportunity left at prior beliefs/q=0, B has expected edge six minus two = four; A has zero edge. With TWO opportunities, A first is better. If its customer buys, V=12 is known, dealer cash is +12 and q=−1. Choose B next, paying two and returning q to zero; final value is ten. If A produces no order, V=0 is known, q=0/cash=0; skip because B would lose two and A again produces no order. The expected final value is (1/2)10+(1/2)0=5.\n\nB first pays two and sets q=1 without changing the prior. A second is feasible: high sells the unit for twelve, ending at q=0/cash=10; low produces no order, leaving q=1 worth zero and cash −2. Average final value is four. Skipping after B gives the same four. A second cannot improve B’s expectation because its high-state sale is at the exact value. Another B is prohibited. Skipping FIRST leaves only one opportunity and value four. Thus A first attains five and beats immediate-edge B and skipping. Enumerating these available first actions and optimal continuations proves optimality in this finite game.',
        r'Write the form of a Bellman state and terminal value for a general finite quote menu with state-dependent customer buy/sell/no-order probabilities, a quadratic terminal penalty \(\lambda q^2\), and h opportunities remaining. Why may past cash be left out of the state? Why must no-order branches and quote feasibility be included BEFORE optimisation?',
        r'Let \(v_0<v_1\) be the two possible terminal payments, \(p\) the current high-state posterior, \(q\) the signed inventory and \(h\) the remaining horizon. Here \(\lambda\) is the nonnegative terminal-penalty coefficient. Terminal expected marked value minus penalty is\n\n\[F_0(p,q)=q[(1-p)v_0+pv_1]-\lambda q^2.\]\n\nFor each reachable event e, let \(p_e\) be its updated high-state posterior and \(\delta_e\) its signed inventory change. For each feasible quote, average immediate dealer cash \(c_e\) plus continuation \(F_{h-1}(p_e,q+\delta_e)\) over its reachable events e; compare with skip, which supplies no observation. Bayes updates \(p_e\) with that quote’s event likelihood, including no order. A customer buy has delta −1/cash ask−fee; a customer sale has delta +1/cash −bid−fee; no order has delta zero/cash zero. Past cash is additive and does not affect later choices under this expected-cash objective and these inventory-only constraints; wealth-dependent utility/capital rules could invalidate that reduction. A quote that might breach limits is excluded in full before selecting it. Deleting its bad branch afterwards would describe a different execution model and invent profit.',
        ['Compute A’s complete high/low paths with final values ten/zero and expectation five.', 'Show B-first value four, its forbidden second purchase and feasible A continuation.', 'Compare skip-first and prove optimality across the actual finite first-action set.', 'Specify posterior, signed inventory and remaining horizon, with terminal marked value/penalty.', 'Explain additive cash, informative no-order events and ex-ante quote feasibility; avoid clairvoyant or retroactively rejected branches.'])


RATIONAL = '''from math import gcd

def rational(numerator, denominator):
    factor = gcd(abs(numerator), denominator)
    return [str(numerator // factor), str(denominator // factor)]
'''


def add_coding(add,tasks):
    def code(suffix,title,level,prompt,signature,samples,tests,solution,explanation):
        add('c_l20_'+suffix,title,level,'Market making',prompt,signature,samples,tests,solution,explanation)
        tasks[-1]['path']='trader'
        for key in ('prompt','explanation'):tasks[-1][key]=tasks[-1][key].replace(r'\n\n','\n\n')

    code('easy','Reconcile a filled sale with its opportunity','Easy',
         r'A terminal contract pays low or high, integers with −10^9≤low≤high≤10^9. weights=[w_low,w_high] has nonnegative integers at most 10^9 and positive sum W. fill_counts=[l_low,l_high] has integers in [0,D], where integer 1≤D≤10^9. Prior state probabilities are weights/W; the probability of a CUSTOMER BUY from the dealer in each state is fill_counts/D. One filled sale receives integer ask in [−10^9,10^9], costs integer fee in [0,10^9] and creates a one-contract settlement liability. No fill costs/pays nothing. Interest is zero; inventory starts at zero. Return keys fill_probability, conditional_value, per_fill, per_opportunity. All defined quantities are EXACT reduced rational [numerator_string,denominator_string], with positive denominator, canonical decimal strings, integers using denominator "1", zero=["0","1"]. If fill probability is zero, conditional_value and per_fill are None, while fill_probability and per_opportunity are ["0","1"]. Preserve both input lists. Use O(1) arithmetic state/work; do not simulate or use floats. This is a dealer SALE, so per-fill profit subtracts the selected liability and fee from the ask.',
         'def solve(low, high, weights, fill_counts, D, ask, fee):',
         [{'args':[0,100,[1,1],[1,2],2,55,0],'expected':{'fill_probability':['3','4'],'conditional_value':['200','3'],'per_fill':['-35','3'],'per_opportunity':['-35','4']}},
          {'args':[-3,7,[1,0],[0,1],1,5,1],'expected':{'fill_probability':['0','1'],'conditional_value':None,'per_fill':None,'per_opportunity':['0','1']}}],
         [{'args':[-4,-4,[2,3],[1,1],2,-3,0],'expected':{'fill_probability':['1','2'],'conditional_value':['-4','1'],'per_fill':['1','1'],'per_opportunity':['1','2']}},
          {'args':[0,10,[0,5],[0,3],3,11,1],'expected':{'fill_probability':['1','1'],'conditional_value':['10','1'],'per_fill':['0','1'],'per_opportunity':['0','1']}},
          {'args':[0,10**9,[10**9,10**9-1],[1,1],1,0,0],'expected':{'fill_probability':['1','1'],'conditional_value':['999999999000000000','1999999999'],'per_fill':['-999999999000000000','1999999999'],'per_opportunity':['-999999999000000000','1999999999']}}],
         RATIONAL+'''\ndef solve(low, high, weights, fill_counts, D, ask, fee):
    a = weights[0] * fill_counts[0]
    b = weights[1] * fill_counts[1]
    selected = a + b
    total = sum(weights) * D
    if selected == 0:
        return {'fill_probability': ['0','1'], 'conditional_value': None,
                'per_fill': None, 'per_opportunity': ['0','1']}
    liability = a * low + b * high
    profit = (ask - fee) * selected - liability
    return {'fill_probability': rational(selected,total),
            'conditional_value': rational(liability,selected),
            'per_fill': rational(profit,selected),
            'per_opportunity': rational(profit,total)}''',
         r'Form the joint state-and-fill weights a=w_low l_low and b=w_high l_high. Fill probability is (a+b)/(WD); conditional payment is (a low+b high)/(a+b), provided that the fill event has positive mass. The net profit numerator is (ask−fee)(a+b)−a low−b high. Divide by a+b for profit per fill, or by WD for profit per opportunity. Zero fill has no defined conditional payment, not a fabricated value zero. Both ways agree with weighting complete branch cash flows. Integer gcd reduction and decimal strings preserve exact signs/digits beyond binary64; arithmetic-operation count is constant but integer bit costs depend on magnitude.')

    code('medium','Choose using quote-specific demand','Medium',
         r'low, high, weights=[w_low,w_high], integer D and fee have these bounds: −10^9≤low≤high≤10^9; 0≤weights[i]≤10^9 with positive total W; 1≤D≤10^9; 0≤fee≤10^9. quotes is a list of at most 100000 rows [ask,l_low,l_high], with integer ask in [−10^9,10^9] and counts in [0,D]. Each row stipulates its OWN probabilities of a customer buying one from the dealer: l_state/D. These need not be monotone in ask; do not transfer a posterior between rows. Only ONE quote may be chosen for one opportunity. Filled dealer sale cash is ask−fee and liability is the state payment; no fill contributes zero. No interest or starting inventory. Refraining gives zero. Return {"index":i,"profit":[num_string,den_string]} for the highest expected net profit PER OPPORTUNITY. Choose index −1 for zero/no positive profit (including empty quotes); among strictly positive tied quotes choose the LOWEST original index. Profit is an exact reduced rational with positive denominator, canonical decimal strings and zero=["0","1"]. Preserve all lists; use O(m) arithmetic operations and O(1) auxiliary integer state for m rows. Do not simulate, sort, round or optimise only per-fill edge.',
         'def solve(low, high, weights, quotes, D, fee):',
         [{'args':[0,100,[1,1],[[55,1,2],[60,1,2],[70,0,1],[100,0,0]],2,1],'expected':{'index':-1,'profit':['0','1']}},
          {'args':[0,0,[1,1],[[10,1,1],[3,10,10]],10,0],'expected':{'index':1,'profit':['3','1']}}],
         [{'args':[0,100,[1,1],[[60,1,1],[80,0,1]],2,1],'expected':{'index':0,'profit':['9','2']}},
          {'args':[0,0,[1,0],[],2,0],'expected':{'index':-1,'profit':['0','1']}},
          {'args':[0,0,[1,1],[[2,1,1],[1,2,2]],2,0],'expected':{'index':0,'profit':['1','1']}},
          {'args':[-4,-4,[1,1],[[-3,1,1],[-4,1,1]],1,1],'expected':{'index':-1,'profit':['0','1']}},
          {'args':[0,10**9,[10**9,10**9-1],[[10**9,1,1],[10**9,0,1]],1,0],'expected':{'index':0,'profit':['1000000000000000000','1999999999']}},
          {'args':[0,0,[1,1],[[2,1,1]]*4096,1,0],'expected':{'index':0,'profit':['2','1']}}],
         RATIONAL+'''\ndef solve(low, high, weights, quotes, D, fee):
    best = 0
    index = -1
    for i, (ask, l_low, l_high) in enumerate(quotes):
        profit = weights[0] * l_low * (ask - fee - low)
        profit += weights[1] * l_high * (ask - fee - high)
        if profit > best:
            best = profit
            index = i
    return {'index': index, 'profit': rational(best,sum(weights)*D)}''',
         r'Use the joint state-and-order branch probabilities specific to EACH quote. Its profit numerator is w_low l_low(ask−fee−low)+w_high l_high(ask−fee−high), over the common positive WD. Compare numerators directly; begin with the zero no-quote alternative and replace only on a strictly greater value. This preserves earliest positive ties and prefers refraining at zero. A rare favourable fill can lose to a more frequent modest edge when compared per opportunity. A quote with no reachable fills has zero profit, with no need to divide by its fill mass. One scan is O(m) arithmetic/O(1) auxiliary integer state; it does not derive demand curves from price or assert real-world optimality.')

    A=[0,12,[[0,0,2],[2,0,0]]]
    B=[2,2,[[0,2,0],[0,2,0]]]
    code('hard','Learn from orders while respecting inventory limits','Hard',
         r'low<high are integer terminal payments in [−10^9,10^9]. ONE hidden V is fixed for the whole game. weights=[w_low,w_high] are nonnegative integers ≤10^9, positive total W, describing its prior. quotes contains at most three [bid,ask,rows] entries, with −10^9≤bid≤ask≤10^9 and rows=[[customer_buy,customer_sell,no_order] in low, same in high]. All counts are integers in [0,100]. Every row of EVERY quote sums to the SAME integer D in [1,100], so its entry divided by D is the event probability conditional on V and that quote. Customers’ events are conditionally independent given V and selected quotes; menus/counts stay fixed.\n\nAt each of 0≤horizon≤5 opportunities choose one whole quote or SKIP. Skip gives no cash, inventory change or observation, and uses that opportunity. After quoting you observe buy, sell OR no order. Customer buy: dealer cash ask−fee, q changes by −1. Customer sell: dealer cash −bid−fee, q changes by +1. No order: cash zero, q unchanged, but Bayes still updates. Initial inventory is integer q in [−limit,limit], 0≤limit≤5. Exclude a quote if ANY positive-probability event under CURRENT beliefs would breach the limit; no retroactive rejection of an executed branch. fee and penalty are integers in [0,10^9]. Financing is zero. Final objective is accumulated cash plus qV MINUS penalty×q², in one currency unit. There is no interim penalty or wealth/capital constraint.\n\nReturn {"gain":[numerator_string,denominator_string],"action":index}. Gain is the EXACT best expected final objective minus the expectation from skipping EVERY opportunity with the original inventory. Reduce to canonical decimal strings, positive denominator, zero=["0","1"]. action is the optimal FIRST quote index, or −1 for skip; ties prefer skip, then the lowest quote index. At horizon zero return zero gain/action −1. Choose subsequent actions using only observed history, not V. Preserve every input. Use a finite-horizon belief/inventory recursion; memoisation may identify scaled equivalent beliefs. A conservative tree bound is \(O(m(1+3m)^h)\) arithmetic operations and \(O((1+3m)^h)\) memo states for m quotes/h opportunities (handle m=0 separately). These explicit small limits support exact computation; no polynomial/unbounded-horizon claim. Do not use float posteriors, a greedy immediate edge or simulation.',
         'def solve(low, high, weights, quotes, horizon, inventory, limit, penalty, fee):',
         [{'args':[0,12,[1,1],[A,B],2,0,1,0,0],'expected':{'gain':['5','1'],'action':0}},
          {'args':[0,10**9,[10**9,10**9-1],[[0,0,[[0,1,0],[0,1,0]]]],1,0,1,0,0],'expected':{'gain':['999999999000000000','1999999999'],'action':0}}],
         [{'args':[0,12,[1,1],[A,B],1,0,1,0,0],'expected':{'gain':['4','1'],'action':1}},
          {'args':[0,12,[1,1],[A,B],5,0,0,0,0],'expected':{'gain':['0','1'],'action':-1}},
          {'args':[0,12,[1,1],[],5,1,1,2,0],'expected':{'gain':['0','1'],'action':-1}},
          {'args':[0,10,[0,1],[[8,8,[[1,0,0],[1,0,0]]]],1,1,1,3,0],'expected':{'gain':['1','1'],'action':0}},
          {'args':[0,10,[0,1],[[8,8,[[1,0,0],[1,0,0]]]],1,0,1,3,0],'expected':{'gain':['0','1'],'action':-1}},
          {'args':[0,12,[1,1],[B,B],1,0,1,0,0],'expected':{'gain':['4','1'],'action':0}},
          {'args':[0,12,[1,1],[A,B],0,1,1,5,0],'expected':{'gain':['0','1'],'action':-1}},
          {'args':[0,12,[1,1],[B],5,0,5,0,0],'expected':{'gain':['20','1'],'action':0}},
          {'args':[-3,13,[37,61],[[4,9,[[2,4,5],[6,3,2]]],[3,11,[[1,5,5],[7,2,2]]],[2,10,[[3,2,6],[5,4,2]]]],5,-1,4,2,1],'expected':{'gain':['11179260','7891499'],'action':2}},
          {'args':[0,12,[1,1],[[0,12,[[1,1,1],[1,1,1]]],[1,11,[[1,1,1],[1,1,1]]],[2,10,[[1,1,1],[1,1,1]]]],5,0,5,0,0],'expected':{'gain':['20','1'],'action':0}}],
         RATIONAL+'''from functools import lru_cache

def solve(low, high, weights, quotes, horizon, inventory, limit, penalty, fee):
    D = sum(quotes[0][2][0]) if quotes else 1
    powers = [D**t for t in range(horizon+1)]

    def terminal(a, b, q):
        return q*(a*low + b*high) - penalty*q*q*(a+b)

    def scaled(a, b, q, t):
        factor = gcd(a, b)
        value, action = best(a//factor, b//factor, q, t)
        return factor*value

    @lru_cache(None)
    def best(a, b, q, t):
        if t == 0:
            return terminal(a,b,q), -1
        winning = D*scaled(a,b,q,t-1)
        chosen = -1
        for index,(bid,ask,rows) in enumerate(quotes):
            candidate = 0
            feasible = True
            for event,delta in enumerate((-1,1,0)):
                x = a*rows[0][event]
                y = b*rows[1][event]
                if x+y == 0:
                    continue
                next_q = q+delta
                if not -limit <= next_q <= limit:
                    feasible = False
                    break
                cash = ask-fee if event==0 else -bid-fee if event==1 else 0
                candidate += cash*(x+y)*powers[t-1] + scaled(x,y,next_q,t-1)
            if feasible and candidate > winning:
                winning = candidate
                chosen = index
        return winning,chosen

    factor = gcd(weights[0],weights[1])
    a,b = weights[0]//factor,weights[1]//factor
    value,action = best(a,b,inventory,horizon)
    gain = value - terminal(a,b,inventory)*powers[horizon]
    return {'gain': rational(gain,(a+b)*powers[horizon]), 'action': action}''',
         r'Write \(v_0=\mathrm{low}\), \(v_1=\mathrm{high}\) and \(\lambda=\mathrm{penalty}\). For each quote, \(L_{0e}\) and \(L_{1e}\) are its low/high ROW COUNTS for event e, with common row total D; the event probabilities are these counts divided by D. Conditional beliefs can be stored as two nonnegative integer weights \(u=(a,b)\), with positive sum \(U=a+b\). At t remaining opportunities define an INTEGER value numerator \(N_t\) so expected future cash plus terminal marked inventory/penalty is \(N_t/(UD^t)\). The terminal numerator is\n\n\[N_0(u,q)=q(av_0+bv_1)-\lambda q^2 U.\]\n\nSkip has candidate D times the t−1 numerator. For a quoted event e, let \(c_e\) be dealer cash received and \(\delta_e\) the inventory increment; set \(u_e=(aL_{0e},bL_{1e})\) and \(z_e=aL_{0e}+bL_{1e}\). Its contribution to the common numerator is\n\n\[c_e z_e D^{t-1}+N_{t-1}(u_e,q+\delta_e).\]\n\nSum the reachable event contributions and maximise over feasible quotes and skip. This cancels posterior normalising denominators exactly. A zero-mass event supplies no constraint or continuation; a reachable limit breach invalidates the entire quote. No-order branches have zero cash but can move the posterior and change future choices. Scaling \(u\) by \(g\) scales \(N_t\) by \(g\) without changing its chosen action, so cache gcd-normalised beliefs and multiply the cached numerator back by g when using it in the parent. Omitting that factor corrupts branch weights. Compare exact integer candidates, replacing only on a strict improvement to preserve skip/earliest ties. At the root subtract the original hold-to-settlement objective, including its original penalty, using the same denominator. Past cash need not be cached because it is additive and does not change feasible future actions here. Sample one gives gain five after A, versus four after greedy B; no order is precisely the observation identifying the zero state. The exponential tree bound, memo storage and integer bit costs are separate from the small declared horizon; this is not a realistic fitted market or a universal market-making policy.')
