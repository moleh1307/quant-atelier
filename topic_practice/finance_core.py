"""Exact payoff matching, local sensitivity arithmetic and finite pricing feasibility."""
from math import gcd


def ratio(numerator,denominator=1):
    divisor=gcd(abs(numerator),denominator)
    return [str(numerator//divisor),str(denominator//divisor)]


def greeks(delta,gamma,theta,change):
    return dict(zip(('delta','gamma','theta','change'),(ratio(*value) for value in (delta,gamma,theta,change))))


def bounds(values):
    return {'feasible':True,'bounds':[[ratio(*lo),ratio(*hi)] for lo,hi in values]}


def add_questions(add,questions):
    rubrics={
        'q39':['Include the one-half coefficient and obtain retained change one.',
               'Explain that initial delta neutrality removes a local first-order response, not all risk.',
               'Handle the negative move and name the omitted time, volatility, rehedging and higher-order terms.'],
        'q40':['Match long-call/short-put terminal payments state by state for identical European contracts.',
               'Replicate with underlying and strike financing under the stated no-dividend/frictionless assumptions.',
               'Obtain price difference zero without claiming each option is worthless; correct for known dividend present value.']
    }
    for id,rubric in rubrics.items():next(q for q in questions if q['id']==id)['rubric']=rubric
    def question(suffix,title,level,minutes,prompt,answer,hints,solution,follow,follow_solution,rubric):
        add('q_l23_'+suffix,title,'Mathematical finance',level,'trader',minutes,prompt,answer,hints,solution,follow,follow_solution,'l23')
        questions[-1]['rubric']=rubric
        for key in ('prompt','solution','followSolution'):questions[-1][key]=questions[-1][key].replace(r'\n\n','\n\n')

    question('e1','Contract quantities change the synthetic payoff','Easy',8,
        r'European calls and puts have the same strike 100, underlying and maturity; each pays per one underlying unit. Hold TWO long calls and ONE short put. At terminal underlying price 120, what is the combined cash payoff? This asks terminal payment, not profit after an initial premium. Does the usual one-call-minus-one-put identity turn this whole position into one unit of a forward?',
        40,
        ['Apply the signed contract quantities to max(S−100,0) and max(100−S,0).', 'One copy of call-minus-put leaves another long call.'],
        r'Each call pays twenty and the short put pays zero, so the combined payment is forty. The unit identity applies to ONE call and ONE short put. Write H(S) for this combined payoff at terminal price S. Its exact decomposition is\n\n\[\begin{aligned}H(S)&=2(S-100)^+\\&\quad-(100-S)^+\\&=(S-100)+(S-100)^+.\end{aligned}\]\n\nThe extra call changes the upside slope; multiplying a remembered parity expression by an unrelated net contract count would lose that payment.',
        r'What is the payment at terminal price ninety? Derive the whole piecewise payoff and explain why a fixed stock-and-cash position alone cannot replicate it for every nonnegative terminal price. Give an exact decomposition using one call as well as stock/cash, assuming no dividends and zero interest.',
        r'At ninety the two calls pay zero and the short put pays minus ten. Below one hundred the payoff is S−100; above it the payoff is 2(S−100), with continuity and zero payment at the strike. A fixed stock/cash payoff aS+b has one constant slope, so it cannot match both slopes one and two. Exactly one long call plus one underlying unit and a terminal cash liability of one hundred does replicate it. Under zero interest/no dividends the liability can be financed by borrowing one hundred initially. This is state-by-state matching, not an expectation or a claim that the initial portfolio cost is zero.',
        ['Use both long calls and the negative put quantity to obtain forty.', 'Distinguish terminal payment from net profit or an initial price.', 'Derive both slopes, the payment minus ten at ninety, and the stock/cash/extra-call decomposition.'])

    question('e2','Finance the strike and the dividend separately','Easy',9,
        r'A European call and put share strike 100, maturity and underlying. Spot is 108. A risk-free claim paying the strike at maturity costs 95 today. A known cash dividend before maturity has present value three. The call costs fourteen. Assume frictionless matched borrowing/lending, available shorting and no other dividends. What put price is forced by exact replication? The present value of the dividend is not a change to the contractual strike.',
        4,
        ['The stock position delivers both the terminal stock and the earlier dividend.', 'Subtract the dividend present value and the present value of the strike from spot to match call-minus-put.'],
        r'Put-call replication gives C−P=108−3−95=10. Therefore P=14−10=4. Ignoring the dividend would produce one, and subtracting the undiscounted strike in place of its present value would produce nine. The financing prices and dividend timing are part of the matching argument; neither volatility nor a physical expected stock return is required.',
        r'Describe the stock and financing cash flows that replicate call-minus-put at both dates. Why is borrowing only 95 insufficient to match all intervening cash flows? Would identical terminal payoff reasoning alone justify the same equality for American exercise rights?',
        r'Hold one underlying unit. Borrow 95 through maturity, repaying one hundred there. Also borrow an amount with current value three and repayment equal to the known dividend at its payment date. The stock dividend cancels that second repayment; terminal net payment is S_T−100. Initial cost is ten. Borrowing only the strike present value leaves an unmatched dividend receipt and therefore costs thirteen rather than ten. With American rights, an early exercise action can change payment timing; a terminal-only equality does not match every available exercise policy. Exact European matching needs the stated contract/financing assumptions.',
        ['Use the two distinct present-value cash-flow corrections and obtain put price four.', 'Match the dividend liability at its date and the strike liability at maturity.', 'Explain the extra stock dividend and why terminal matching alone does not establish American parity.'])

    question('m1','A midpoint discrepancy is not an executable parity trade','Medium',23,
        r'One-period, no-dividend European call and put share strike one hundred. Interest is zero; stock, call and put can each be bought/shorted in unit quantities, with no costs beyond these executable bid/ask pairs: stock [97,101], call [5,8], put [5,8]. Buying uses the ask and selling the bid. Midpoints give C−P=0 while spot-minus-strike is −1. Can EITHER of the two standard matched parity round trips lock positive initial cash with zero terminal cash flow? Enumerate both directions and all four initial cash flows. Do not infer overall absence of every possible arbitrage merely from checking these two trades.',
        None,
        ['Compare a sold synthetic forward with a bought stock-minus-strike position.', 'For the opposite direction buy the synthetic forward and sell the stock-minus-strike position.', 'Borrowing one hundred receives cash now; depositing one hundred spends cash now.'],
        r'Direction A: short the call at five, buy the put at eight, buy stock at 101, and borrow one hundred. Initial cash is 5−8−101+100=−4. Its terminal payment is −call+put+S−100=0 in every state. Direction B: buy the call at eight, short the put at five, short stock at 97 and deposit one hundred. Initial cash is −8+5+97−100=−6; terminal payment call−put−S+100 is again zero. Both require a positive initial payment and give no terminal receipt, so neither yields the proposed locked gain. The midpoint discrepancy cannot pay the bid/ask crossings. These calculations concern the two named matched trades and the declared execution/financing terms.',
        r'Change the put bid/ask to [12,13], keeping all other terms and shorting availability. Which direction now locks cash, how much, and why are the terminal payments still matched? Identify one realistic omitted constraint that would have to be checked before interpreting actual market quotes this way.',
        r'Direction B now receives −8+12+97−100=one initially and still has zero terminal net cash for every underlying price. The put CONTRACT did not change, only its executable quote. Direction A has initial cash 5−13−101+100=−9. Actual execution would also need matching quantity availability, financing, short borrow/collateral, fees and consistent contract/dividend terms; the specified exercise assumes those trades feasible. A real discrepancy in midpoints alone does not establish this executable four-leg outcome.',
        ['Write both opposite four-leg trades using the correct bid/ask and funding signs.', 'Obtain initial cash minus four/minus six and prove terminal cancellation.', 'Derive the changed-quote receipt one and separate the declared feasible toy trade from additional execution conditions.'])

    question('h1','Three terminal states need not determine one option price','Hard',32,
        r'At time zero a no-dividend stock costs one hundred, and cash has zero interest. The ONLY terminal stock states are 0,100,200, each with strictly positive PHYSICAL probability. One-period stock/cash holdings can be any real signed quantities, with frictionless shorting and borrowing. Add a European strike-one-hundred call with unknown price C. There are no intervening dates or other securities. Show whether stock/cash can exactly replicate the call. Derive the FULL arbitrage-free interval of C, including whether endpoints are included, and prove sufficiency. You may construct positive pricing weights q₀,q₁,q₂ for states 0,100,200 respectively, summing to one and pricing stock at its current value; these are not assumed physical probabilities. Arbitrage means a zero-cost financed terminal payoff nonnegative in every possible state and positive in at least one.',
        None,
        ['A stock/cash payoff is affine in the terminal stock price; the call payments are 0,0,100.', 'The stock-pricing constraint gives q₀=q₂ and q₁=1−2q₂.', 'Use strictly positive pricing weights for sufficiency and explicit endpoint payoff trades for necessity.'],
        r'If aS+b matches the call, state zero forces b=0 and state one hundred then forces a=0, contradicting the required payment one hundred at state two hundred. The claim is not redundant with stock and cash.\n\nThe positive pricing constraints are\n\n\[\begin{aligned}q_0+q_1+q_2&=1,\\q_1+2q_2&=1.\end{aligned}\]\n\nThus \(q_0=q_2=z\), \(q_1=1-2z\) and \(0<z<1/2\). The call price is \(C=100z\), giving the OPEN interval \(0<C<50\). For any such C these positive weights correctly price cash, stock and call. Every zero-cost terminal payoff formed from those assets has zero weighted mean; if it is everywhere nonnegative and somewhere positive, the strictly positive weights make that mean positive, a contradiction. This proves sufficiency without choosing physical probabilities.\n\nAt C=0, a free long call pays a strictly positive amount in the high state. At C=50, half a stock minus one call costs zero and pays (0,50,0). Both are arbitrages because the relevant physical states have positive probability. For C<0 or C>50, the same respective portfolios have a positive initial receipt; put it in cash to obtain a zero-cost financed arbitrage. Mere nonnegative pricing weights at the boundaries would miss these trades. No-arbitrage leaves a range here rather than an automatic unique expected payoff price.',
        r'Add a cash digital paying one ONLY when terminal stock equals one hundred, with price d. Determine the feasible interval for d, the forced call price and an exact stock/digital replication. Does knowing the physical state probabilities by itself impose that same unique price?',
        r'The digital prices q₁=d, so q₀=q₂=(1−d)/2. Strict positivity requires 0<d<1, and call price is C=50(1−d). The exact payoff identity is call=half a stock minus fifty middle-state digitals: its payments are (0,0,100). At d=0 the digital itself is a free positive payoff; at d=1 cash minus the digital is free and positive in the outer states. Adding the traded digital supplies the missing state-price information and makes this replication possible. Physical probabilities alone describe real-world expectations, not the pricing weights; no equality between those measures was stipulated.',
        ['Prove nonreplicability from all three state payments.', 'Derive and prove the strict interval 0<C<50, including positive-weight sufficiency.', 'Construct arbitrages at both endpoints and outside the interval.', 'Derive digital interval 0<d<1 and the stock/digital identity forcing C=50(1−d).'])

    question('h2','Rebalancing cash belongs in the gamma calculation','Hard',35,
        r'Use a CONSTRUCTED smooth mark function V(S,t)=aS²−bt, with a,b>0 and nonnegative observed stock prices at dates t₀<...<t_n, n≥1. Interest, dividends and fees are initially zero. Hold one long marked contract and short Δ_i=2aS_i stock units over interval [t_i,t_{i+1}); rebalance at interior dates and liquidate at the final date. Fund the initial purchase/short through a cash account so initial TOTAL net wealth is zero; all later trades must be self-financing. Derive the terminal cash wealth, including the cash-account changes at rehedges. Compare paths (100,110,100) and (100,100,100) at dates (0,1/2,1), with a=0.02,b=3. Compare with a frozen initial-delta hedge. The mark function is a mathematical illustration, not a claimed arbitrage-free market price or a general option repricing law.',
        None,
        ['Over one interval, exact contract change minus the HELD initial delta times stock change simplifies to a squared-move term and time decay.', 'Changing the short from Δ_{i−1} to Δ_i receives (Δ_i−Δ_{i−1})S_i into cash.', 'Sum actual interval gains; do not replace the sum of squared moves by the square of the total move.'],
        r'Write \(V_0=V(S_0,t_0)\). Start with \(B_0=\Delta_0S_0-V_0\), so \(V_0-\Delta_0S_0+B_0=0\). At each interior rebalance,\n\n\[B_i=B_{i-1}+(\Delta_i-\Delta_{i-1})S_i.\]\n\nThe stock trade changes cash and stock holdings by opposite amounts; it does not create an external gain. Write \(V_i=V(S_i,t_i)\), \(x_i=S_{i+1}-S_i\) and \(u_i=t_{i+1}-t_i\). Exact marked interval gain is\n\n\[G_i=V_{i+1}-V_i-\Delta_i x_i,\]\n\nwhich simplifies to \(G_i=ax_i^2-bu_i\). Therefore final liquidated wealth is\n\n\[\begin{aligned}W_n&=a\sum_{i=0}^{n-1}x_i^2\\&\quad-b(t_n-t_0).\end{aligned}\]\n\nFor the first path the two squared moves total two hundred, so W=4−3=one. Direct ledger: V₀=200, Δ₀=4, B₀=200; at 110 delta becomes 4.4 and cash receives 44, giving B₁=244. At maturity V=197 and the stock close costs 440; terminal cash is 244+197−440=one. The flat path has zero price contribution and wealth minus three. A frozen initial-delta hedge in either same-endpoint path gives V_n−V₀−Δ₀(S_n−S₀)=−3. This quadratic function has constant gamma 2a and theta −b, so its interval expression is EXACT; a general smooth instrument would have approximation error and varying sensitivities.',
        r'Charge proportional stock trading cost c=0.001 on the absolute trade quantity times execution price, INCLUDING the initial short and final stock close; contract fees stay zero. Keep initial EXTERNAL outlay zero; fund the initial fee through the cash account instead of adding outside money. Derive the cost-adjusted terminal wealth for both paths. Can inserting more hedge dates only increase the sum of squared moves?',
        r'Let the held short quantities be Δ₀ through Δ_{n−1}. Deduct\n\n\[\begin{aligned}c\big(&|\Delta_0|S_0\\&+\sum_{i=1}^{n-1}|\Delta_i-\Delta_{i-1}|S_i\\&+|\Delta_{n-1}|S_n\big).\end{aligned}\]\n\nInitial financing includes the first cost, so initial post-trade marked wealth is minus that fee; it is not reset by an outside cash injection. Interior cash updates subtract their execution cost; the final close subtracts the last cost. First-path cost base is 400+44+440=884, so cost is 0.884 and net wealth 0.116. Flat-path cost base is 400+0+400=800; net wealth is −3.8. Positive gamma alone did not secure positive net wealth.\n\nRefinement is not monotone: splitting an interval with increments x,y replaces (x+y)² by x²+y², a difference −2xy. A reversal can increase the sum; a same-direction split decreases it. Flat endpoints 100→100 give zero before adding an intermediate 110, but two hundred after. Conversely 100→120 gives four hundred before splitting at 110, but two hundred after. More dates also change turnover and omitted real-world risks; the constructed identity does not certify a general strategy.',
        ['Set initial cash to make wealth zero and include every self-financing rebalance.', 'Derive the exact sum of interval squared moves minus time decay.', 'Verify dynamic wealth one/minus three and distinguish the frozen hedge.', 'Include initial/interior/final costs to obtain 0.116 and minus 3.8.', 'Show both refinement directions and separate the constructed quadratic identity from a general local approximation.'])


EASY_REFERENCE='''from math import gcd

def rational(num,den):
    divisor = gcd(abs(num),den)
    return [str(num//divisor),str(den//divisor)]

def solve(positions, stock_units, sensitivity_denominator, move, days):
    denominator = sensitivity_denominator
    delta = stock_units*denominator
    gamma = theta = 0
    for quantity,multiplier,d,g,t in positions:
        scale = quantity*multiplier
        delta += scale*d
        gamma += scale*g
        theta += scale*t
    change = 2*delta*move+gamma*move*move+2*theta*days
    return {'delta':rational(delta,denominator),'gamma':rational(gamma,denominator),
            'theta':rational(theta,denominator),'change':rational(change,2*denominator)}'''

MEDIUM_REFERENCE='''def solve(contracts, stock_units, cash, prices):
    events = {}
    slope = stock_units
    value = cash
    for kind,strike,quantity,multiplier in contracts:
        amount = quantity*multiplier
        events[strike] = events.get(strike,0)+amount
        if kind == 'put':
            slope -= amount
            value += amount*strike
    cuts = sorted(events)
    cursor = 0
    previous = 0
    answer = [None]*len(prices)
    for index in sorted(range(len(prices)),key=lambda i:prices[i]):
        price = prices[index]
        while cursor < len(cuts) and cuts[cursor] <= price:
            strike = cuts[cursor]
            value += slope*(strike-previous)
            slope += events[strike]
            previous = strike
            cursor += 1
        answer[index] = str(value+slope*(price-previous))
    return answer'''

HARD_REFERENCE='''from bisect import bisect_left
from math import gcd

def rational(num,den):
    divisor = gcd(abs(num),den)
    return [str(num//divisor),str(den//divisor)]

def solve(max_price, spot_numerator, price_denominator, strikes, call_numerators, queries):
    d = price_denominator
    if spot_numerator > d*max_price:
        return {'feasible':False,'bounds':None}
    x = [0]+strikes+[max_price]
    y = [spot_numerator]+call_numerators+[0]
    slopes = [(y[i+1]-y[i],x[i+1]-x[i]) for i in range(len(x)-1)]
    previous_num,previous_den = -d,1
    for num,den in slopes:
        if num > 0 or num*previous_den < previous_num*den:
            return {'feasible':False,'bounds':None}
        previous_num,previous_den = num,den
    answer = []
    for k in queries:
        right = bisect_left(x,k)
        if x[right] == k:
            fixed = rational(y[right],d)
            answer.append([fixed[:],fixed[:]])
            continue
        left = right-1
        ln,ld = slopes[left-1] if left else (-d,1)
        rn,rd = slopes[right] if right < len(x)-1 else (0,1)
        low_left = y[left]*ld+ln*(k-x[left])
        low_right = y[right]*rd-rn*(x[right]-k)
        if low_left*rd >= low_right*ld:
            lower = rational(low_left,d*ld)
        else:
            lower = rational(low_right,d*rd)
        upper = rational(y[left]*(x[right]-k)+y[right]*(k-x[left]),d*(x[right]-x[left]))
        answer.append([lower,upper])
    return {'feasible':True,'bounds':answer}'''


def add_coding(add,tasks):
    def code(suffix,title,level,prompt,signature,samples,tests,solution,explanation):
        add('c_l23_'+suffix,title,level,'Mathematical finance',prompt,signature,samples,tests,solution,explanation)
        tasks[-1]['path']='trader'
        for key in ('prompt','explanation'):tasks[-1][key]=tasks[-1][key].replace(r'\n\n','\n\n')

    code('easy','Aggregate signed Greeks with their contract multipliers','Easy',
        r'positions contains up to 10000 rows [quantity,multiplier,delta_num,gamma_num,theta_num]. Quantity is an integer in [−10^6,10^6]; multiplier is a positive integer ≤10^6. All sensitivity numerators are integers in [−10^6,10^6] and share positive integer sensitivity_denominator D≤10^9. These are per-unit delta, gamma and CALENDAR-TIME theta, with theta per DAY. stock_units is an integer in [−10^6,10^6]; stock contributes delta stock_units and zero gamma/theta. move is an integer underlying price change in [−10^6,10^6], and days is an integer in [0,10^6]. Other inputs, financing and fees are held fixed. Aggregate SIGNED quantities/multipliers first. Write \(x=\texttt{move}\), \(h=\texttt{days}\), and compute the retained Taylor change \(\Delta x+\tfrac12\Gamma x^2+\Theta h\). Return {"delta":[num_text,den_text],"gamma":[num_text,den_text],"theta":[num_text,den_text],"change":[num_text,den_text]}, all exact reduced canonical decimal STRINGS with positive denominators; zero=["0","1"]. Preserve positions. Use O(n) integer arithmetic/O(1) working integers, with bit/gcd costs additional. The retained quantity is computed exactly as algebra; it is a local value approximation for a general instrument, especially unreliable for arbitrary large moves. Do not omit the half factor, change theta to a remaining-time derivative, or treat the output as terminal payoff or guaranteed trading profit.',
        'def solve(positions, stock_units, sensitivity_denominator, move, days):',
        [{'args':[[[2,100,50,2,-3]],-100,100,5,1],'expected':greeks((0,1),(4,1),(-6,1),(44,1))},
         {'args':[[[1,1,1,-1,-1]],0,2,-3,2],'expected':greeks((1,2),(-1,2),(-1,2),(-19,4))},
         {'args':[[[10**6,10**6,10**6,10**6,-10**6]],0,999999937,10**6,1],
          'expected':greeks((10**18,999999937),(10**18,999999937),(-10**18,999999937),(500000999999000000000000000000,999999937))}],
        [{'args':[[],3,7,-2,9],'expected':greeks((3,1),(0,1),(0,1),(-6,1))},
         {'args':[[[2,3,4,5,-6],[-2,3,4,5,-6]],0,9,100,4],'expected':greeks((0,1),(0,1),(0,1),(0,1))},
         {'args':[[[0,10**6,10**6,10**6,10**6]],0,1,0,0],'expected':greeks((0,1),(0,1),(0,1),(0,1))},
         {'args':[[[1,1,0,0,-3]],0,2,0,2],'expected':greeks((0,1),(0,1),(-3,2),(-3,1))},
         {'args':[[[1,1,1,1,-1] for _ in range(10000)],-10000,1,2,1],'expected':greeks((0,1),(10000,1),(-10000,1),(10000,1))}],
        EASY_REFERENCE,
        r'Use D as the common denominator for each aggregate sensitivity. Stock delta starts at stock_units·D; each row adds quantity·multiplier times each numerator. A short position reverses ALL of that contract’s contributions. Write d,g,t for the aggregate sensitivity numerators, x for move and h for days. The retained change has common denominator 2D and numerator \(2dx+gx^2+2th\). Reduce each result separately. This keeps the half-gamma coefficient, signed theta and stated day units without floating arithmetic. For sample one, the stock neutralises delta but aggregate gamma four/time contribution minus six remain, giving forty-four. Local initial delta cancellation does not maintain neutrality after a move; summing these numbers is not a self-financing rehedging calculation. Large exact strings survive display and copied cases.')

    code('medium','Evaluate a signed option book at every terminal price','Medium',
        r'contracts contains up to 20000 rows [kind,strike,quantity,multiplier]. kind is "call" or "put"; strike is an integer in [0,10^9], quantity in [−10^6,10^6], and multiplier in [1,10^6]. All European contracts use the SAME nonnegative terminal underlying price and maturity. Each unit call pays max(S−strike,0), each put max(strike−S,0). stock_units is an integer in [−10^6,10^6]; cash is a fixed TERMINAL cash payment in [−10^9,10^9], possibly a liability. prices contains up to 20000 integer terminal prices in [0,10^9], in arbitrary order with duplicates. Return the exact combined TERMINAL cash payoff at each price, including stock_units·S+cash, as canonical signed decimal STRINGS in original query order; zero is "0". Do not subtract premiums or reinterpret terminal cash as its present value. Preserve every input. Use sorting and slope changes or equivalent preprocessing, avoiding a scan through every contract for every query: O(n log n+m log m) arithmetic/comparisons and O(n+m) storage is sufficient. Integer bit costs are additional. Handle shared strikes, calls/puts at zero strike, negative quantities, exact strike prices and empty lists. A signed book need not be convex; slope jumps can be negative. No volatility model, early exercise, simulation or Greek approximation is involved.',
        'def solve(contracts, stock_units, cash, prices):',
        [{'args':[[['call',100,1,1],['put',100,-1,1]],-1,100,[0,90,100,120,200]],'expected':['0']*5},
         {'args':[[['call',100,1,1],['put',120,-1,1]],0,0,[90,110,130,0]],'expected':['-30','0','30','-120']},
         {'args':[[['call',1,10**6,10**6]],0,0,[10**9,1,0]],'expected':['999999999000000000000','0','0']}],
        [{'args':[[],2,-3,[4,0,4]],'expected':['5','-3','5']},
         {'args':[[['call',0,2,1],['put',0,-7,2]],-1,5,[0,10,3]],'expected':['5','15','8']},
         {'args':[[['call',3,-2,4],['call',3,2,4],['put',3,-1,2]],0,0,[4,3,2,0]],'expected':['0','0','-2','-6']},
         {'args':[[['put',5,1,3],['call',7,-2,2]],1,-1,[8,5,7,0]],'expected':['3','4','6','14']},
         {'args':[[['call',5,1,1]],0,0,[]],'expected':[]},
         {'args':[[['call',0,1,1] for _ in range(20000)],0,0,[1]*19000],'expected':['20000']*19000},
         {'args':[[['call',1,1,1]],0,0,list(range(20000,0,-1))],'expected':[str(s-1) for s in range(20000,0,-1)]}],
        MEDIUM_REFERENCE,
        r'At price zero the book value is terminal cash plus every signed put amount times strike; its initial right-hand slope starts at stock units minus all put amounts. At each strike, BOTH a call and a put add their signed amount to the slope: a call begins paying above its strike, while a put stops losing one unit of payoff per added stock-price unit. Combine events sharing a strike. Advance the value continuously to each event, change the slope there, then evaluate sorted queries in the current linear segment. At a strike either adjoining segment gives the same payoff; processing the event before the equal-price query is safe. Restore the original query order. Zero-strike put events cancel their provisional initial slope; signed events can cancel or create negative curvature. The stock/cash piece is already a terminal linear payment. This exact piecewise calculation does not price the options, include premiums or use local sensitivities.')

    code('hard','Validate call quotes and bound an unquoted strike exactly','Hard',
        r'Use a ONE-period, zero-interest, no-dividend pricing class defined by \(C(K)=E[(S_T-K)^+]\) and \(E[S_T]=S_0\), with a NONNEGATIVE probability measure supported on [0,M]. Zero masses are explicitly allowed; no physical probabilities or strictly-positive-support condition are imposed. M=max_price is an integer in [1,10^9]. price_denominator D is an integer in [1,10^9]; spot_numerator and call_numerators are integers in [0,10^9]. Spot is S₀=spot_numerator/D. strikes is a strictly increasing list of n integers with 0<K<M, n≤20000; call_numerators has matching length and quote i is call_numerators[i]/D. queries contains m≤20000 integer strikes in [0,M], arbitrarily ordered with duplicates. Input dimensions/order are guaranteed, but quote FEASIBILITY is not. Return {"feasible":False,"bounds":None} if NO such probability measure matches all quotes/spot. Otherwise return {"feasible":True,"bounds":[[lower_pair,upper_pair],...]} in query order, with SHARP inclusive price bounds over ALL matching measures. Each pair is [signed_numerator_text,positive_denominator_text], exact reduced canonical decimal STRINGS; zero=["0","1"]. A quoted strike and endpoints have fixed prices. Preserve all lists. Aim for O(n+m log(n+2)) exact arithmetic/comparisons and O(n+m) auxiliary storage; bit/gcd costs are additional. Use collective convexity, decreasing slopes and endpoint slope bounds, not independent pairwise price tests or a linear-programming package. The support cap matters. These inclusive bounds describe the declared NONNEGATIVE-measure class; they do not prove strict no-arbitrage for a different specified physical support in which every state must have positive probability.',
        'def solve(max_price, spot_numerator, price_denominator, strikes, call_numerators, queries):',
        [{'args':[200,100,1,[50,150],[60,10],[100,25,175,50,0,200]],
          'expected':bounds([((20,1),(35,1)),((75,1),(80,1)),((0,1),(5,1)),((60,1),(60,1)),((100,1),(100,1)),((0,1),(0,1))])},
         {'args':[200,100,1,[50,100,150],[55,40,5],[100]],'expected':{'feasible':False,'bounds':None}},
         {'args':[10**9,10**9,999999937,[123456789,876543211],[800000000,100000000],[333333333]],
          'expected':bounds([((66666666700000000,123456781222222293),(227777778400000000,376543187277777707))])}],
        [{'args':[10,4,1,[],[],[0,2,8,10]],'expected':bounds([((4,1),(4,1)),((2,1),(16,5)),((0,1),(4,5)),((0,1),(0,1))])},
         {'args':[2,3,1,[1],[1],[1]],'expected':{'feasible':False,'bounds':None}},
         {'args':[10,4,1,[5],[5],[2]],'expected':{'feasible':False,'bounds':None}},
         {'args':[3,1,1,[1,2],[0,0],[0,1,2,3]],'expected':bounds([((1,1),(1,1)),((0,1),(0,1)),((0,1),(0,1)),((0,1),(0,1))])},
         {'args':[10,0,7,[],[],[1,1,9]],'expected':bounds([((0,1),(0,1))]*3)},
         {'args':[10,40,4,[],[],[3]],'expected':bounds([((7,1),(7,1))])},
         {'args':[20001,20001,1,list(range(1,20001)),list(range(20000,0,-1)),[20000]*8000],'expected':bounds([((1,1),(1,1))]*8000)},
         {'args':[1,0,1,[],[],[0]*20000],'expected':bounds([((0,1),(0,1))]*20000)}],
        HARD_REFERENCE,
        r'Add the known endpoint quotes C(0)=S₀ and C(M)=0. A bounded nonnegative expectation gives a continuous convex decreasing call curve, with strike slope between −1 and zero. In scaled numerators, adjacent secant slopes must therefore be nondecreasing, between −D and zero. Check every secant by integer cross multiplication, including the first/last bounds and S₀≤M. These are also SUFFICIENT: linearly join the quotes, extend slope −1 left of zero and zero right of M, and put probability mass equal to each nonnegative slope jump divided by D at its knot. The jumps sum to one; the resulting call expectations equal the curve and its mean is C(0).\n\nFor a query K strictly between adjacent knots a,b with prices A,B, the largest feasible price is their chord. A new price cannot fall below the line through A with the PREVIOUS secant slope, or the line through B with the NEXT secant slope. Use synthetic boundary slopes −1 and zero where those neighbouring intervals do not exist. Thus\n\n\[\begin{aligned}L&=\max\{A+s_L(K-a),\\&\qquad B-s_R(b-K)\},\end{aligned}\]\n\n\[\begin{aligned}U&=\frac{A(b-K)}{b-a}\\&\quad+\frac{B(K-a)}{b-a}.\end{aligned}\]\n\nAny inserted price in [L,U] maintains all adjacent slope inequalities; the SAME slope-jump construction yields a matching measure on the augmented knots. This proves sharpness over continuous terminal support, not merely a fixed grid or numerical sample. Equality/zero mass is allowed by this task’s class. Each query is bounded separately: its extremising measure need not attain every OTHER query bound simultaneously. Binary-search the interval, calculate the two lower candidate rationals and the chord with integer products, compare exactly, and reduce each pair. For the first example at strike one hundred, both supporting lines give twenty while the chord gives thirty-five. Merely interpolating the old quotes would select one admissible price, not establish a unique implied price. No probability forecast, Black–Scholes parameter or extra empirical regularity was supplied.')
