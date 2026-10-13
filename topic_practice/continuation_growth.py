"""Optional decisions, conditional fees, model uncertainty and positive wealth."""


def add_questions(add,questions):
    rubrics={
        'q13':['Compare each observed value with continuation 3.5; keep 4,5,6 and reroll 1,2,3.',
               'Average the conditional maxima to 17/4; do not move the maximum outside the expectation.',
               'Charge a one-unit cost only on reroll branches to obtain threshold 2.5 and value 23/6.'],
        'q37':['Specify even-money multipliers 1+f and 1−f with admissible 0≤f<1.',
               'Differentiate expected log growth and use concavity to obtain f=0.2 under known p=0.6.',
               'Separate the log objective from one-round arithmetic gain and identify probability, dependence, costs and tail assumptions.']
    }
    for id,rubric in rubrics.items():next(q for q in questions if q['id']==id)['rubric']=rubric
    def question(suffix,title,level,minutes,prompt,answer,hints,solution,follow,follow_solution,rubric):
        add('q_l21_'+suffix,title,'Decision theory',level,'trader',minutes,prompt,answer,hints,solution,follow,follow_solution,'l21')
        questions[-1]['rubric']=rubric
        for key in ('prompt','solution','followSolution'):questions[-1][key]=questions[-1][key].replace(r'\n\n','\n\n')

    question('e1','Keep the payment or buy the remaining choice','Easy',8,
        r'You currently may keep payment four. Alternatively, pay a fee of 1.5 and take a compulsory fresh payment: two or eight, each with probability one half. The fresh outcome is independent of your current observation. Maximise expected cash payment MINUS any fee paid now; there are no further options, capital constraints or financing costs. What is the optimal conditional expected NET payment, and which action obtains it? A fee is charged only if you continue; no past cost is included.',4,
        ['The fresh payment has mean five, before its fee.', 'Compare four with five minus 1.5, rather than with the largest possible payment.'],
        r'Continuing gives expected net payment (2+8)/2−1.5=3.5. Keeping gives four, so keep and obtain optimal conditional value four. Eight being possible does not make the remaining action worth eight. Subtracting the fee from the kept payment would impose a cost that the stated action never incurs.',
        r'If the fee is instead 0.5, which action is optimal and what is its expected net payment? If it subsequently pays two, does that establish that the choice was wrong? What if the fee is one and the convention is to keep at an exact tie?',
        r'With fee 0.5, continue for expected net value 4.5. The realised low outcome gives 1.5, worse than keeping four, but it occurs within the model used to choose; it does not retroactively replace expected value with hindsight. At fee one both actions have expected value four, and the declared tie convention keeps. Decision quality depends on the information, objective and feasible alternatives at the time, not just the realised outcome.',
        ['Use the full fresh distribution and subtract the fee only on continuation.', 'Compare continuation 3.5 with keeping four.', 'Derive 4.5 at the changed fee, separate hindsight from decision quality and keep on the specified tie.'])

    question('e2','One win and one loss do not cancel percentages','Easy',8,
        r'Initial wealth is 100. In each of TWO even-money rounds you stake exactly one quarter of CURRENT wealth. There are no fees, withdrawals or borrowing. One round wins and the other loses. What is final wealth? Explain whether order changes it for this fixed-fraction policy; do not treat both stakes as 25 cash units.',93.75,
        ['A win multiplies current wealth by 1.25; a loss by 0.75.', 'The product is 1−f², not one.'],
        r'Final wealth is 100×1.25×0.75=93.75, a loss of 6.25. Win first: wealth becomes 125, then the loss is 31.25. Lose first: wealth becomes 75, then the gain is 18.75. The product of these fixed multipliers commutes, so either order gives the same answer. Constant-dollar stakes would describe a different policy.',
        r'If independent wins each have probability 0.6, what is expected wealth after the two rounds at this same fraction? Does the result above contradict that expectation? Does order remain irrelevant if the next fraction depends on the previous outcome?',
        r'The expected multiplier is 0.6×1.25+0.4×0.75=1.05. Independent rounds and a fixed fraction give expected final wealth 100×1.05²=110.25. Explicitly, two wins have probability 0.36 and wealth 156.25; mixed outcomes total probability 0.48 and wealth 93.75; two losses have probability 0.16 and wealth 56.25. Weighting them gives 110.25. A losing mixed path does not contradict positive arithmetic expectation. With a history-dependent policy order can matter: use f=1/4 first, then f=1/2 after a win or zero after a loss. Win-then-loss gives 62.5; loss-then-win gives 75. The fixed-fraction commutativity argument no longer applies.',
        ['Compound current-wealth multipliers to 93.75 in either order.', 'Distinguish proportional stakes from constant-dollar stakes.', 'Compute two-round expected wealth 110.25 under independence and retain the losing-path possibility.', 'Give the changed-policy order counterexample 62.5 versus 75.'])

    question('m1','The order of optional fees changes continuation value','Medium',24,
        r'Roll independent fair six-sided dice. After the first observation you may stop and keep it, or pay the FIRST listed fee to discard it and roll again. After that observation you may stop, or pay the SECOND fee to discard it and take one last compulsory roll. Fees are subtracted from the final numerical payment only when their reroll is taken; no financing or capital constraint. Maximise expected net cash payment BEFORE seeing the first roll. Compare fee schedules [1,0] and [0,1]. They have the same sum of listed fees. Derive each continuation threshold and expected value by backward induction, and explain why subtracting that sum from every path is wrong. At exact ties keep.',None,
        ['Begin with the final compulsory roll of mean 3.5.', 'The expected fresh roll WITH its remaining option is not generally 3.5.', 'The first fee is subtracted from the value of the next roll WITH the second option.'],
        r'For [1,0], the second decision has free continuation 3.5, so a fresh second roll with its option is worth 17/4. At the first observation, reroll continuation is 17/4−1=13/4. Reroll 1,2,3 and keep 4,5,6. Initial value is\n\n\[\frac{3(13/4)+4+5+6}{6}=\frac{33}{8}.\]\n\nFor [0,1], the second decision has continuation 3.5−1=2.5; a fresh second roll with that option is worth 23/6. The first fee is zero, so its continuation threshold is 23/6. Again reroll 1,2,3 and keep 4,5,6, but initial value is\n\n\[\frac{3(23/6)+4+5+6}{6}=\frac{53}{12}.\]\n\nThe policies’ first kept values coincide while their continuation values differ. The expensive early option must be paid whenever it is used; an expensive later option is paid only when the later observation warrants it. A listed fee is not an unavoidable cost on every branch. Past fees are sunk/additive under this cash objective and do not enter the remaining comparison again.',
        r'Two possible fresh-roll laws both have mean three: A pays three certainly; B pays zero or six with equal probabilities. You know which law applies, and fresh draws are iid under that law. A fresh draw comes with ONE free additional redraw option. What are the two continuation values? If you currently can keep four, can a common raw mean of three justify the same decision for both laws?',
        r'Under A, a fresh draw and any redraw always pay three, so its optional value is three. Under B, the redraw mean is three; a first zero is redrawn and a six is kept, giving optional value (3+6)/2=4.5. Currently keeping four beats continuing under A but loses to continuing under B. The raw means agree; the distributions of observed payments inside the maximum do not. If a signal/history determines which law applies, that information belongs in the state. Do not substitute the mean of a compulsory draw for the value of a draw with remaining options.',
        ['Work backward from compulsory mean 3.5 and charge only the applicable reroll fee.', 'Derive first thresholds 13/4 and 23/6, and values 33/8 and 53/12.', 'Explain optional branch costs and why sunk past fees do not change the remaining comparison.', 'Compute optional values three under A and 4.5 under B under equal raw means and opposite decisions at current value four.'])

    question('h1','Bayesian uncertainty is not a worst-case probability','Hard',35,
        r'A single hidden coin parameter P is 0.55 or 0.65 with equal PRIOR model probabilities. Conditional on P, outcomes are iid; P stays fixed. Before ONE even-money round choose 0≤f<1 of positive wealth W; wealth multiplier is 1+f on a win and 1−f on a loss. No fees, other outcomes or capital rules apply. Maximise BAYESIAN expected log final wealth, averaging over the stated model probabilities. Derive the optimal fraction and explain whether uncertainty about P alone forces a fraction below 0.2 for this objective. Separately replace those model probabilities by an AMBIGUITY SET p∈[0.55,0.65], with a worst-case expected-log objective; derive its fraction. These are toy criteria, not a real-money recommendation.',None,
        ['Expected one-round log growth is affine in p for a fixed fraction.', 'Averaging over model probabilities differs from minimising over a set.', 'For f≥0, log(1+f) exceeds log(1−f), so identify the worst p.'],
        r'Define the conditional growth \(g_p(f)=p\log(1+f)+(1-p)\log(1-f)\) for a fixed coin probability p. For a fixed fraction, Bayesian expected log growth is\n\n\[\begin{aligned}E[g_P(f)]&=\bar p\log(1+f)\\&\quad +(1-\bar p)\log(1-f),\end{aligned}\]\n\nwhere the current predictive probability is \(\bar p=E[P]=0.6\). Strict concavity and derivative zero give \(f=2\bar p-1=0.2\). Probability uncertainty alone does not introduce a separate variance penalty into this ONE-round expected-log expression. A different utility, ambiguity objective, drawdown constraint, cost or tail model could change the answer; none is stipulated here.\n\nUnder the ambiguity SET and f≥0, growth is increasing in p because its slope in p is \(\log((1+f)/(1-f))\geq0\). The worst case is p=0.55. Maximising that concave growth function gives f=0.10. Equal model weights and a worst-case model are distinct assumptions; they are not interchangeable interpretations of “uncertain”. At f approaching one any model has positive loss probability, making expected log wealth tend to minus infinity.',
        r'Extend the Bayesian problem to TWO rounds, allowing the second fraction to depend on the observed first outcome. The coin outcome is observed even if f=0; its distribution and future information do NOT depend on your fraction. All constraints remain proportional and unchanged. Compute the posterior model weights, second predictive win probabilities and optimal second fractions after win/loss. Prove whether a non-myopic first fraction improves on 0.2 under terminal expected log wealth.',
        r'After a win, the high-p model has weight 0.65/(0.55+0.65)=13/24 and the low model 11/24. Next predictive win probability is 29/48, giving second fraction 5/24. After a loss, model weights are 7/16 high and 9/16 low; next predictive probability 19/32 gives fraction 3/16. Their predictive probabilities average back to 0.6 under first-outcome probability 0.6 for a win and 0.4 for a loss.\n\nWrite terminal log wealth as current log W plus first-round log multiplier plus second-round log multiplier. The distribution of posterior information and the optimal continuation term is INDEPENDENT of the first fraction under the stated observation rule. Hence only the first expected log multiplier depends on that fraction, and its unique optimum remains 0.2. The same separation proves posterior-predictive myopic fractions optimal at any finite horizon in this particular model. Learning occurs, but no stake is needed to cause it. Action-dependent information, wealth-dependent feasible sets or nonlinear costs would invalidate this separation. Unconditionally the outcomes are correlated through the persistent P; the finite conditional-expectation argument does not assume unconditional iid outcomes.',
        ['Average one-round growth over the stated model weights to predictive p=0.6 and fraction 0.2.', 'Derive the distinct worst-case p=0.55/fraction 0.1 and check the positive-wealth domain.', 'Update model probabilities after win/loss and derive predictive 29/48 and 19/32, fractions 5/24 and 3/16.', 'Separate the first growth term from action-independent information/continuation; prove first fraction 0.2 remains optimal.', 'State the observation/feasibility assumptions and persistent-model dependence; do not claim uncertainty universally requires fractional sizing.'])

    question('h2','A rare third outcome invalidates the binary formula','Hard',34,
        r'Positive wealth W becomes W(1+fR) after a round. The NET return R is +1 with probability 0.60, −1 with probability 0.39 and −9 with probability 0.01. Exposure f is nonnegative; every possible wealth multiplier must be strictly positive. No fees or further constraints apply. Derive the admissible domain and maximise expected natural-log wealth growth. Is the binary even-money formula f=2(0.60)−1=0.20 even admissible? Show strict concavity and select the correct root, rather than applying an even-money formula to a three-outcome return. Expected one-round cash return and log growth are different objectives.',None,
        ['The largest possible loss is nine times exposure, not one.', 'Differentiate the three weighted logarithms within the positive-multiplier domain.', 'Multiply by the positive common denominator to obtain a quadratic; check which root stays admissible.'],
        r'The domain is \(0\leq f<1/9\); f=0.2 gives catastrophe multiplier −0.8 and is inadmissible. Expected net return is 0.6−0.39−9(0.01)=0.12, so growth initially increases. The objective and derivative are\n\n\[\begin{aligned}g(f)&=.60\log(1+f)\\&\quad+.39\log(1-f)\\&\quad+.01\log(1-9f),\end{aligned}\]\n\n\[g^{\prime}(f)=\frac{.60}{1+f}-\frac{.39}{1-f}-\frac{.09}{1-9f}.\]\n\nAn outcome with probability p and net return r contributes second derivative \(-pr^2/(1+fr)^2\). Each nonzero return therefore contributes negative curvature, so g is strictly concave. Its derivative starts at 0.12 and tends to minus infinity at 1/9. Multiplying by the positive denominator gives \(9f^2-2.88f+.12=0\), equivalently \(75f^2-24f+1=0\). Only\n\n\[f_* =\frac{12-\sqrt{69}}{75}\approx0.049245\]\n\nis admissible; the other root exceeds 1/9. This is the unique maximum, with growth about 0.00329237 per round. The lower fraction comes from the specified third outcome/domain, not from changing the probability of the original binary game while pretending its loss sizes stayed fixed.',
        r'Keep the win probability 0.60, but let catastrophe probability ε be only known to lie in [0,0.02], taken from the ordinary loss probability so it becomes 0.40−ε. Choose one exposure before knowing ε to maximise WORST-CASE expected log growth. Locate the adverse ε and derive the admissible optimum. Does putting equal weights on ε endpoints describe the same objective?',
        r'For positive f<1/9, shifting probability from R=−1 to R=−9 decreases growth by \(\log(1-9f)-\log(1-f)<0\). The worst ε is 0.02; at f=0 all models tie at zero. Feasibility must cover the possible catastrophic state, so the robust domain still ends at 1/9 even though ε=0 is allowed. The worst-model derivative has numerator \(9f^2-2.96f+.04\), giving\n\n\[f_*^{\rm robust}=\frac{37-\sqrt{1144}}{225}\approx0.0141197.\]\n\nIts derivative at zero is 0.04>0, and strict concavity plus the boundary identify the smaller root as the unique optimum. Equal PRIOR weights on the two ε endpoints would instead create predictive ε=0.01 for this one-round log objective and give the earlier 0.049245 result. That mixture is a different model choice from an ambiguity set. Neither objective supplies a guarantee for an individual realised wealth path.',
        ['Enforce 0≤f<1/9 and reject fraction 0.2 before evaluating any logarithm.', 'Derive all three derivative terms and strict concavity.', 'Obtain quadratic 75f²−24f+1 and its unique admissible smaller root.', 'Identify worst ε=0.02 and derive the robust root/domain, including the zero-fraction tie.', 'Separate expected cash, a Bayesian model mixture, a worst-case model and realised outcomes.'])


RATIONAL='''from math import gcd

def rational(numerator, denominator):
    divisor = gcd(abs(numerator), denominator)
    return [str(numerator // divisor), str(denominator // divisor)]
'''


def add_coding(add,tasks):
    def code(suffix,title,level,prompt,signature,samples,tests,solution,explanation):
        add('c_l21_'+suffix,title,level,'Decision theory',prompt,signature,samples,tests,solution,explanation)
        tasks[-1]['path']='trader'
        for key in ('prompt','explanation'):tasks[-1][key]=tasks[-1][key].replace(r'\n\n','\n\n')

    code('easy','Keep an observed payment or pay for a fresh one','Easy',
         r'You may KEEP observed, an integer in [−10^9,10^9], or pay integer cost in [0,10^9] to take a compulsory independent fresh payment. payoffs and weights are equally long integer lists of length 1..100000: payoffs in [−10^9,10^9], weights in [0,10^9] with positive sum W; fresh state i has probability weights[i]/W. observed need not belong to this fresh support. There are no other options, costs, capital constraints or financing charges; no fee is paid when keeping. Maximise conditional expected remaining payment MINUS any fee incurred now. Return {"action":"keep" or "reroll","value":[numerator_string,denominator_string]}. Keep on an EXACT tie. Value must be an exact reduced rational with positive denominator and canonical decimal strings; zero=["0","1"], integer values use denominator "1". Preserve both lists. Use O(n) arithmetic operations/O(1) auxiliary integers; do not simulate or use floats. Past sunk fees are outside this remaining-payment objective.',
         'def solve(observed, payoffs, weights, cost):',
         [{'args':[3,[1,2,3,4,5,6],[1]*6,1],'expected':{'action':'keep','value':['3','1']}},
          {'args':[-3,[-1,1],[1,2],0],'expected':{'action':'reroll','value':['1','3']}},
          {'args':[0,[0,10**9],[10**9,10**9-1],0],'expected':{'action':'reroll','value':['999999999000000000','1999999999']}}],
         [{'args':[2,[1,3],[1,1],0],'expected':{'action':'keep','value':['2','1']}},
          {'args':[-7,[-4,-2],[1,1],1],'expected':{'action':'reroll','value':['-4','1']}},
          {'args':[5,[0,999],[1,0],10**9],'expected':{'action':'keep','value':['5','1']}},
          {'args':[0,[1]*100000,[1]*100000,0],'expected':{'action':'reroll','value':['1','1']}}],
         RATIONAL+'''\ndef solve(observed, payoffs, weights, cost):
    mass = sum(weights)
    continuation = sum(value*weight for value,weight in zip(payoffs,weights)) - cost*mass
    if observed*mass >= continuation:
        return {'action': 'keep', 'value': [str(observed),'1']}
    return {'action': 'reroll', 'value': rational(continuation,mass)}''',
         r'The compulsory fresh mean is its weighted sum divided by W, and the fee is incurred only on continuation. Compare observed×W with the continuation numerator N−cost×W. A greater-or-equal kept value implements the exact tie rule; no subtraction from the kept branch is warranted. Reduce only the chosen continuation fraction. Decimal strings preserve large exact values in the browser. One weighted pass is O(n) arithmetic/O(1) auxiliary integer state; multiplication/gcd have magnitude-dependent bit costs. A large possible fresh outcome is not its expected value.')

    code('medium','Backward induction with an ordered fee schedule','Medium',
         r'Before a compulsory first draw, maximise expected final numerical payment minus optional reroll fees. payoffs and weights describe a FIXED finite law used by every independent fresh draw: equally long integer lists, length 1..1000, payoffs in [−10^9,10^9], weights in [0,10^9] with positive total W. Duplicated payoff values and zero weights are permitted. costs is an ordered list of at most 30 nonnegative integers ≤10^9. After the first observation you may keep it or pay costs[0] to discard it and draw again. After that observation you may keep or pay costs[1], and so on; a draw after the last paid reroll is compulsory with no remaining options. A fee is paid ONLY when that option is taken. No financing, wealth constraints or other costs. Keep at ties. Return {"value":[num_string,den_string],"threshold":[num_string,den_string] or None}. value is optimal expected NET payment BEFORE the first observation; threshold is the first-observation continuation value, so reroll exactly when observed<threshold. With no options threshold=None and value is the compulsory mean. All defined rationals must be exact reduced canonical decimal strings with positive denominator, zero=["0","1"]. Preserve all lists. Use O(n(k+1)) arithmetic operations/O(1) working integers for k fees, apart from input/output; integer bit costs grow with horizon. Iterate backward, not through all draw histories, and do not charge every listed fee on every path.',
         'def solve(payoffs, weights, costs):',
         [{'args':[[1,2,3,4,5,6],[1]*6,[1,0]],'expected':{'value':['33','8'],'threshold':['13','4']}},
          {'args':[[1,2,3,4,5,6],[1]*6,[0,1]],'expected':{'value':['53','12'],'threshold':['23','6']}},
          {'args':[[0,1],[4,1],[0]*30],'expected':{'value':[str(5**31-4**31),str(5**31)],'threshold':[str(5**30-4**30),str(5**30)]}}],
         [{'args':[[0,6],[1,1],[]],'expected':{'value':['3','1'],'threshold':None}},
          {'args':[[0,6],[1,1],[0]],'expected':{'value':['9','2'],'threshold':['3','1']}},
          {'args':[[-4,-2],[1,1],[1]],'expected':{'value':['-3','1'],'threshold':['-4','1']}},
          {'args':[[3,3,999],[1,2,0],[10**9,0,10**9]],'expected':{'value':['3','1'],'threshold':['-999999997','1']}},
          {'args':[[0,1],[1,1],[0]*30],'expected':{'value':['2147483647','2147483648'],'threshold':['1073741823','1073741824']}},
          {'args':[[0,2,5],[1,1,1],[0,1,3]],'expected':{'value':['95','27'],'threshold':['25','9']}},
          {'args':[[0,1]*500,[4,1]*500,[0]*30],'expected':{'value':[str(5**31-4**31),str(5**31)],'threshold':[str(5**30-4**30),str(5**30)]}}],
         RATIONAL+'''\ndef solve(payoffs, weights, costs):
    mass = sum(weights)
    numerator = sum(v*w for v,w in zip(payoffs,weights))
    denominator = mass
    factor = gcd(abs(numerator),denominator)
    numerator //= factor
    denominator //= factor
    threshold = None
    for cost in reversed(costs):
        future = numerator - cost*denominator
        threshold = rational(future,denominator)
        numerator = sum(w*max(v*denominator,future) for v,w in zip(payoffs,weights))
        denominator *= mass
        factor = gcd(abs(numerator),denominator)
        numerator //= factor
        denominator //= factor
    return {'value': [str(numerator),str(denominator)], 'threshold': threshold}''',
         r'Begin with the compulsory last draw mean. For the next fee c encountered BACKWARD, suppose the later fresh draw WITH all of its remaining choices has value N/d. Current continuation is (N−cd)/d. The current fresh value is the weighted mean of max(v_i,continuation), not max(mean,continuation). Form its numerator as \(\sum_iw_i\max\{v_i d,N-cd\}\) and denominator Wd, then reduce. The last backward iteration corresponds to costs[0], and its saved continuation is the first threshold. With no costs the initial mean survives and threshold is undefined. Sunk prior fees are additive constants under this cash objective. One pass per decision layer uses O(n(k+1)) arithmetic and O(1) working integers; exact denominators can grow with k and are returned as strings. A different conditional draw law would require a different state/recurrence, not silently the same iid calculation.')

    code('hard','Worst-model log growth, including a kink optimum','Hard',
         r'net_returns is a list of n integer NET returns in [−100,100], 1≤n≤50. weights is a matrix of m model rows, 1≤m≤30; each row has n integer counts in [0,10^9] with positive sum. Row j assigns state probabilities count/row_sum. This is a SET of models with no assigned model probabilities. Exposure f changes positive wealth by multiplier 1+f×net_return. cap is a finite float in [0,1]. For every state with nonzero weight in ANY model, 1+cap×net_return≥10^−4 is guaranteed, ensuring positive wealth throughout [0,cap]. States zero in every model are irrelevant; do not evaluate their invalid logarithms. Maximise WORST-MODEL expected natural-log growth over 0≤f≤cap. Return [fraction,growth], two finite floats accurate to absolute 10^−7; growth is the MINIMUM model log expectation at the chosen fraction. Choose the smallest maximising fraction: if a model gives no positive expected return, zero is optimal and this tie rule selects it, including an identically zero model. No fees, extra outcomes, drawdown constraints or simulation. Preserve all inputs. The worst-model curve is concave but can be NONDIFFERENTIABLE where its active model changes. Do not average model probabilities, optimise model roots independently or apply the binary 2p−1 formula to general returns. Use a bounded one-dimensional concave search; O(120mn) numerical work and O(mn) stored model probabilities is sufficient under these bounds. Use log1p for small f×return and accurate summation; do not round the output.',
         'def solve(net_returns, weights, cap):',
         [{'args':[[-1,1],[[9,11],[7,13]],.9],'expected':[.1,.005008366846356837]},
          {'args':[[1,-1,-9],[[60,39,1]],.1],'expected':[.049245015161092335,.0032923727073165955]},
          {'args':[[1,-1,-9],[[55,45,0],[90,5,5]],.1],'expected':[.07547246060002536,.004705436716017622]}],
         [{'args':[[-1,1],[[2,3]],0],'expected':[0,0]},
          {'args':[[-1,1],[[3,2],[1,4]],.9],'expected':[0,0]},
          {'args':[[0,1],[[1,0],[0,1]],1],'expected':[0,0]},
          {'args':[[1,-100],[[1,0]],1],'expected':[1,.6931471805599453]},
          {'args':[[-1,1],[[2,3]],.05],'expected':[.05,.00875678074558106]},
          {'args':[[1,0],[[1,1]]*30,1],'expected':[1,.34657359027997264]},
          {'args':[[-1,1]*25,[[2,3]*25 for _ in range(30)],.9],'expected':[.2,.020135513550688863]}],
         '''import math

def solve(net_returns, weights, cap):
    if cap == 0 or any(sum(w*r for w,r in zip(row,net_returns)) <= 0 for row in weights):
        return [0.0,0.0]
    models = []
    for row in weights:
        total = sum(row)
        models.append([(r,w/total) for r,w in zip(net_returns,row) if w])
    def growth(fraction):
        return min(math.fsum(p*math.log1p(fraction*r) for r,p in model) for model in models)
    left,right = 0.0,cap
    for _ in range(120):
        first = left+(right-left)/3
        second = right-(right-left)/3
        if growth(first) < growth(second):
            left = first
        else:
            right = second
    candidates = [(0.0,0.0),(cap,growth(cap))]
    middle = (left+right)/2
    candidates.append((middle,growth(middle)))
    fraction,value = min(candidates,key=lambda item:(-item[1],item[0]))
    return [fraction,value]''',
         r'For each model j, define \(g_j(f)=\sum_i p_{ji}\log(1+fr_i)\), where \(r_i\) is its net return and \(p_{ji}\) its normalised state probability. The positivity condition covers the UNION of reachable states, while zero-weight terms need no logarithm. Each g_j is concave; its pointwise minimum h is concave because every g_j at an interior convex combination is at least the same combination of endpoint h values. With a positive-mean nonconstant model, g_j is strictly concave. If ANY model has nonpositive mean return, concavity and its derivative at zero imply g_j(f)≤g_j(0)=0 for nonnegative f. Since h(0)=0, choose zero; an all-zero model is handled without an arbitrary positive stake. Otherwise every model has positive mean and strict curvature; for cap>0, h initially increases and has a unique maximum, which may occur at a boundary or a kink. Ternary search uses concavity without differentiating the minimum; compare cap and zero explicitly after narrowing. There is no need to infer which model is active near a numerical crossing.\n\nIn sample three, the two curves cross at a nonzero root of \((1-f)^8=(1+f)^7(1-9f)\). One is increasing and the other decreasing there, so the MINIMUM peaks at that kink, about 0.07547246, not at either separate model optimum or an averaged distribution’s optimum. This bounded scalar model-set calculation does not address estimation, drawdown or action-dependent learning. Probabilities are normalised once, log1p retains small increments, and fsum reduces summation loss; finite binary64 accuracy is checked against independent high-precision objectives and closed-form/polynomial roots.')
