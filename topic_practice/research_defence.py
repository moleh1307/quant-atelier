"""Evidence-aware research defence: economics, comparison and identification."""


def add_questions(add,questions):
    rubrics={
        'q33':['Define the decision-time information, forecast target and actually permitted action before claiming profit.',
               'Reconstruct receipts, revisions, label maturity, latency and baseline information on identical records.',
               'Specify fills, spread, fees, turnover, inventory liquidation and capacity; distinguish assumed execution from measured execution.',
               'Audit chronological selection/evaluation and uncertainty, naming a diagnostic that can contradict the proposed mechanism.'],
        'q34':['Reproduce the earlier implementation and reconcile timestamps, universe, transformations, labels and positions first.',
               'Separate search/overfitting evidence, conditional regime changes and gross-to-net cost accounting without insisting on one cause.',
               'Give a pre-specified diagnostic with an observable prediction that could falsify the preferred explanation.'],
    }
    for q in questions:
        if q['id'] in rubrics:q['rubric']=rubrics[q['id']]

    def question(suffix,title,level,minutes,prompt,answer,hints,solution,follow,follow_solution,rubric):
        add('q_l16_'+suffix,title,'Research design',level,'researcher',minutes,prompt,answer,hints,solution,follow,follow_solution,'l16')
        questions[-1]['rubric']=rubric
        for key in ('prompt','solution','followSolution'):
            questions[-1][key]=questions[-1][key].replace(r'\n\n','\n\n')

    question('e1','Ninety percent correct can lose money','Easy',7,
        r'A fixed toy action rule took exactly 1000 trades. In this stipulated payoff model, each correct prediction earns 1 tick gross and each incorrect prediction loses 12 ticks gross. There were 900 correct and 100 incorrect predictions. Every trade costs 0.2 ticks in total, regardless of outcome, with no other costs or remaining inventory. What is the REALIZED mean NET payoff per trade, in ticks? These explicit payoffs connect labels to money in this toy; accuracy alone would not supply that connection.',-1/2,
        ['Count the magnitudes of gains and losses, not only their frequencies.', 'The total fee is charged on all one thousand trades.'],
        r'Gross payoff is 900·1−100·12=−300 ticks. Total cost is 1000·0.2=200 ticks. The mean net payoff is (−300−200)/1000=−1/2 tick per trade. A 90-percent hit rate does not offset the asymmetric loss sizes. Flat has zero under the declared toy accounting; it is a relevant economic baseline even when it makes no market prediction. This finite arithmetic does not require independent trades, nor does it determine a standard error or future expected payoff.',
        r'If a future trade follows the SAME fixed payoff/cost model and has correct-prediction probability p, what p gives strictly positive expected net payoff? How many correct predictions among 1000 would give strictly positive realized net payoff under this model?',
        r'Expected net payoff is p−12(1−p)−0.2=13p−12.2. It is strictly positive when p>61/65, approximately 0.93846. With integer correct count k out of 1000, total net payoff is 13k−12200, so the smallest profitable count is 939. Equality gives zero rather than profit. Neither threshold is universal: changing costs, loss magnitudes, fill selection or action frequency changes the calculation.',
        ['Derive total gross −300, total costs 200 and mean net −1/2 tick.', 'Explain why label accuracy and arithmetic profit are different evidence.', 'Derive p>61/65 and the strict integer threshold of 939 successes.'])

    question('e2','The paths that fill are a selected sample','Easy',8,
        r'At one hypothetical passive entry price, 100 equally likely complete market paths are declared. On 60 paths the one-unit order fills and is later sold at an executable bid 2 ticks BELOW its entry price. On the other 40 paths it does not fill; their eventual bid is 6 ticks ABOVE the proposed entry price. Unfilled orders earn zero, filled orders are completely liquidated, and this toy charges no fees or other costs. What is expected strategy payoff PER POSTED OPPORTUNITY, in ticks? A future bid relative to a price at which no purchase occurred is not a realized gain.',-6/5,
        ['Attach zero trading payoff to unfilled paths.', 'Averaging all future bid changes answers a different question.'],
        r'The opportunity payoff is −2 on the 60 filled paths and zero on the 40 unfilled paths. Hence its expectation is −1.2=−6/5 ticks. Mean bid change relative to the proposed entry price is 0.6(−2)+0.4(6)=+1.2 ticks, but those favourable paths contain no entry. Conditional payoff given a fill is −2, while payoff per posted opportunity is 0.6 times that amount. Using unconditional future-price changes to evaluate only filled orders substitutes a different sampling event.',
        r'Now charge one tick on every FILLED round trip and an additional 0.1 tick on EVERY posted opportunity, including unfilled orders. Calculate conditional net payoff given a fill and unconditional net payoff per opportunity. Which charges can be multiplied by the fill probability?',
        r'Conditional on a fill the net is −2−1−0.1=−3.1 ticks. On an unfilled path it is −0.1. The opportunity mean is 0.6(−3)−0.1=−1.9 ticks. Equivalently it is 0.6(−3.1)+0.4(−0.1). The filled-round-trip fee is multiplied by fill probability; the posting cost is not. Keeping filled-only and opportunity denominators separate prevents both omitted costs and double counting. Real fill probabilities and liquidation bids would require evidence beyond this declared finite model.',
        ['Compute −6/5 per opportunity, distinguishing it from +6/5 unconditional bid change.', 'Separate conditional fill payoff from the full opportunity target.', 'Charge each fee on its actual event and obtain −3.1 conditional and −1.9 unconditional.'])

    question('m1','A changed mix can reverse the baseline comparison','Medium',17,
        r'A model M and persistence baseline P predict the same binary targets with the same available information. On QUIET opportunities their correct-prediction probabilities are respectively 0.96 and 0.99; on ACTIVE opportunities they are 0.70 and 0.60. These four conditional probabilities remain exactly the same in both periods. Quiet opportunities comprise one half of period one and nine tenths of period two. Calculate both aggregate accuracies in both periods and their paired population accuracy differences. Derive the quiet share w at which M and P tie. Does the reversal establish deterioration of the model WITHIN a market state, overfitting, or a change in trading profit?',None,
        ['Weight conditional accuracy by the population share, not by the number of states.', 'The conditional model-minus-baseline difference is −0.03 in quiet and +0.10 in active.', 'A changed population can reverse an aggregate comparison while all conditional quantities stay fixed.'],
        r'In period one M has accuracy 0.5(0.96)+0.5(0.70)=0.83, while P has 0.5(0.99)+0.5(0.60)=0.795: difference +0.035. In period two M has 0.9(0.96)+0.1(0.70)=0.934; P has 0.9(0.99)+0.1(0.60)=0.951: difference −0.017. The general difference is\n\n\[\Delta(w)=-0.03w+0.10(1-w)=0.10-0.13w.\]\n\nIt vanishes at w=10/13. The model’s own aggregate accuracy actually rises in the later period, even while its advantage over persistence becomes negative. By construction no within-state deterioration occurred. Reweighting the later conditional results to the original one-half quiet share would recover +0.035; this separates the mixture change in this stated model. It does not prove that a fitted regime definition was causal, that a real estimated conditional difference is precise, or that a selected strategy generalizes. Accuracy supplies no payoff sizes, fills or costs, so it cannot determine net profit.',
        r'In observed data rather than this declared model, what must be checked before treating reweighting as a diagnosis? Can subtracting the two marginal accuracies determine how many records M alone gets right?',
        r'State the regime definition and whether it was available at each decision; compare identical target records, account for missing observations, quantify conditional-sample uncertainty/dependence and disclose any regime selection after looking at outcomes. Reweighting requires relevant support: an absent state has no observed conditional performance to transport. The accuracy difference equals Pr(M right,P wrong)−Pr(M wrong,P right), but it does not identify either disagreement probability separately. Overlap counts require the paired record-level predictions. A pre-specified decomposition can diagnose a mixture contribution without ruling out implementation, search or execution problems elsewhere.',
        ['Calculate model versus baseline accuracy 0.83 versus 0.795, then 0.934 versus 0.951, with differences +0.035 and −0.017.', 'Derive w=10/13 and distinguish aggregate mixture from within-state changes.', 'Identify causal regime definitions, support and conditional uncertainty as evidence obligations.', 'Explain why marginal accuracy differences cannot recover paired disagreement counts or profit.'])

    question('h1','Selective observations do not identify a policy by themselves','Hard',40,
        r'Consider iid independent opportunities with observed context X. A fixed target policy \(\pi(X)\in\{0,1\}\) either takes a declared trade or stays flat. Let Y be the potential NET payoff of taking that trade, including zero/no-fill outcomes, all stated costs and complete terminal liquidation; staying flat has payoff zero. In this hypothetical model there is no market impact, interference, or inventory carried between opportunities, and implementing the target does not change Y. Historical action A is binary with KNOWN probability \(e(X)=P(A=1\mid X)\), and A is independent of Y conditional on X. Every opportunity and its A are recorded, but Y is observed only when A=1. On contexts where pi=1 assume e>0.\n\nProve unbiasedness for the target value \(v=E[\pi(X)Y]\) of the single-opportunity score \(Z=A\pi(X)Y/e(X)\), treating it as zero when pi=0. Derive its second moment and the variance of a mean of n independent scores, when those moments are finite. Then use two equally likely contexts: quiet with e=1/4 and deterministic Y=+3 ticks, stressed with e=3/4 and Y=−1 tick; pi=1 in both. Calculate v, the conditional mean payoff among historically traded opportunities, and Var(Z). Which assumptions would fail if your historical logger observed an unrecorded predictor of payoff?',None,
        ['Condition on X and the potential payoff before averaging the randomized historical action.', 'The traded-only mean weights contexts by e(X), whereas the target population need not.', r'Use \(A^2=A\). The second moment contains one inverse propensity factor after averaging A, not two.'],
        r'For pi=1, conditional independence gives \(E[A\mid X,Y]=e(X)\). Thus \(E[Z\mid X,Y]=\pi(X)Y\); for pi=0 the target and score are both zero without dividing by a zero e. Averaging gives E[Z]=v. Squaring before conditioning yields\n\n\[E[Z^2]=E\!\left[\frac{\pi(X)Y^2}{e(X)}\right],\]\n\nwhere the integrand is defined as zero on pi=0. Hence \(\operatorname{Var}(\bar Z_n)=(E[Z^2]-v^2)/n\) for independent identically distributed scores with finite second moment. Very small logging probabilities can make that moment large or infinite even when Y is bounded unless positivity is bounded away from zero.\n\nIn the declared two-state example v=(3−1)/2=1 tick. Historical trade probability is (1/4+3/4)/2=1/2. Unnormalized traded payoff is (1/2)(1/4)3+(1/2)(3/4)(−1)=0, so the traded-only conditional mean is zero. Z takes value 12 with probability 1/8, −4/3 with probability 3/8 and zero with remaining probability 1/2. Its second moment is 18+2/3=56/3 and variance is 53/3. Historical selection changes the context mix; simply averaging observed trades answers the wrong policy question.\n\nIf the logger selects using an unrecorded predictor of Y, knowing the marginal e(X) does not ensure conditional independence. The key equality E[A|X,Y]=e(X) can fail. Weighting then need not identify the counterfactual policy. Likewise these assumptions deliberately exclude size-dependent execution, carry-over inventory and intervention-dependent market paths: a reweighted toy cannot certify a different strategy’s live economics.',
        r'In a DIFFERENT dataset quiet opportunities still have probability one half, but are NEVER traded (e=0), and their potential payoff is otherwise unknown in [−B,B], B≥1. Stressed opportunities have known payoff −1. With pi=1 everywhere, derive the sharp interval for v. Separately, under |Y|≤B and e≥epsilon>0 wherever pi=1, bound E[Z²]. Does clipping inverse weights retain exact unbiasedness?',
        r'The stressed contribution is −1/2 and the unobserved quiet contribution can be any number in [−B/2,B/2]. Thus\n\n\[v\in\left[-\frac{B+1}{2},\frac{B-1}{2}\right].\]\n\nBoth endpoints are attainable by assigning every unobserved quiet trade payoff −B or +B; the logged observations are identical in those worlds. No reweighting recovers data where the action has zero support. Under the separate bounded-positivity assumptions, E[Z²]≤B²/epsilon, because E[pi Y²/e]≤B²/epsilon. Clipping at c replaces 1/e by min(1/e,c); conditional score mean becomes pi Y min(1,c e), generally changing the estimand/bias. It can reduce variance, but exact unbiasedness needs a new justification. Self-normalizing empirical weights also generally changes finite-sample unbiasedness. Choosing a policy after inspecting these same outcomes adds selection beyond the fixed-policy proof.',
        ['State fixed policy, conditional action independence, overlap and the net-payoff/no-interference accounting boundary.', 'Prove the first/second moments by conditioning and require finite moments for the iid variance formula.', 'Calculate target 1, traded-only mean 0 and score variance 53/3.', 'Identify unrecorded selection and zero action support as identification failures; derive sharp bounds and explain clipping bias.'])


def add_coding(add,tasks):
    def exercise(level,title,prompt,signature,samples,tests,reference,explanation):
        add('c_l16_'+level.lower(),title,level,'Research design',prompt,signature,samples,tests,reference,explanation)
        tasks[-1]['path']='researcher'
        for key in ('prompt','explanation'):
            tasks[-1][key]=tasks[-1][key].replace(r'\n\n','\n\n')

    exercise('Easy','Count paired forecast improvements',
        r'actual, model and baseline are equal-length lists of binary integers, each zero or one on the SAME target records. They may be empty and have at most 100000 entries. Return [model_correct,baseline_correct,model_only_correct,baseline_only_correct], where the last two count disagreements in correctness on each paired record. Preserve all inputs. Use O(n) time and O(1) auxiliary space. Do not discard records on which both forecasts are wrong; do not divide by n or turn accuracy into payoff. This audits a declared paired comparison; it cannot certify that timestamps, information availability or baseline construction were fair.',
        'def solve(actual, model, baseline):',
        [{'args':[[0,0,1,1],[0,1,1,0],[0,0,0,0]],'expected':[2,2,1,1]}, {'args':[[0,1,1],[0,1,1],[0,0,0]],'expected':[3,1,2,0]}],
        [{'args':[[],[],[]],'expected':[0,0,0,0]}, {'args':[[1],[0],[0]],'expected':[0,0,0,0]}, {'args':[[0],[0],[0]],'expected':[1,1,0,0]}, {'args':[[1,0],[0,1],[1,0]],'expected':[0,2,0,2]}, {'args':[[0,1]*3000,[0,0]*3000,[1,1]*3000],'expected':[3000,3000,3000,3000]}],EASY_REFERENCE,
        r'For each paired record compute two correctness booleans, increment their separate totals and increment the appropriate one-sided correctness count. Records where both agree in correctness contribute neither disagreement. The difference in total correct counts must equal model-only minus baseline-only counts. Equal marginal accuracies do not mean identical predictions, and disagreement counts support a paired analysis that marginal totals alone cannot reconstruct. No distributional or economic conclusion is manufactured by counting.')

    exercise('Hard','Bound a fixed payoff under a changed regime mix',
        r'counts and payoffs are equal-length lists for n declared market states, 1≤n≤20000. Counts are integers in [0,10^9], with positive total W; payoffs are integer NET ticks in [−10^9,10^9] for a FIXED rule in each state. Baseline probability is p_i=counts_i/W. A zero-count state is still in the declared uncertainty support and can receive future mass; it is not proved impossible. Payoffs are supplied fixed quantities, not estimated conditional means whose error this task would quantify. budget=[a,b] with 0≤a≤b≤10^9, b≥1 specifies epsilon=a/b; it need not be reduced.\n\nAmong ALL real probability vectors q on these n states with \(\tfrac12\sum_i|q_i-p_i|\leq\epsilon\), minimize \(\sum_i q_i g_i\), where g_i is the stated net payoff. Return {"worst_mean": [signed_numerator_text,positive_denominator_text], "used_tv": [numerator_text,denominator_text]}. Both pairs must be exact reduced decimal STRINGS; zero is ["0","1"]. used_tv is the SMALLEST total-variation distance among distributions attaining that minimum, not necessarily the full budget. Preserve all three inputs. Aim for O(n log n) comparisons, O(n) auxiliary storage and exact integer arithmetic, with integer bit/gcd costs additional. Do not enumerate all q or use floats.\n\nThis computes a sharp finite-support composition sensitivity bound. It keeps the policy and conditional payoffs fixed, allowing only the declared regime probabilities to change. It neither selects profitable trades after seeing outcomes nor includes unseen payoff changes, unvalidated fills, estimation uncertainty or states outside this declared support. A positive bound under these assumptions is not a certified live edge.',
        'def solve(counts, payoffs, budget):',HARD_SAMPLES,HARD_CASES,HARD_REFERENCE,
        r'Total variation is the amount of probability mass removed from some states and added to others. Any removed unit can improve the objective most by being placed in a state with MINIMUM payoff. Removing mass from a higher-payoff donor is always at least as useful as removing it from a lower-payoff donor: exchange a small donor amount while leaving the receiving minimum state fixed. Thus drain the highest-payoff states first until the budget is exhausted or every positive-payoff-gap state has been emptied. Equal-minimum states need no transfers; once all mass is on minima, spending more distance cannot improve the objective and would violate the minimal-used-distance requirement.\n\nFor exact arithmetic choose D=Wb. Each original state has count_i·b mass units, and the allowed transfer has W·a units. The baseline expectation numerator is b times sum(count_i·g_i). Transfer h units from payoff g to the minimum g_min, subtracting h(g−g_min) from that numerator. Only original nonminimum mass is ever drained, so capacities are respected. At most min(epsilon,1−P(baseline minimum states)) mass is used; this is the least distance that can attain the minimum. Sort indices by descending payoff, skipping zero capacity and zero gaps, and reduce the final mean and used-unit fractions by gcd.\n\nSharpness follows from constructing these transfers. For the lower bound, decompose any admissible q−p into removed/added masses of equal total h≤epsilon. Added payoff is at least h·g_min; removed mass from each donor cannot exceed its original p_i. The largest possible reduction therefore solves exactly the bounded donor allocation above. This proves a global bound over continuous distributions, not merely over a grid. The often used expression baseline_mean−epsilon(max payoff−min payoff) is only a bound and can be unattainable when the maximum-payoff state has insufficient mass.')


EASY_REFERENCE='''def solve(actual, model, baseline):
    model_correct = baseline_correct = model_only = baseline_only = 0
    for y,m,b in zip(actual,model,baseline):
        mc,bc = m == y,b == y
        model_correct += mc
        baseline_correct += bc
        model_only += mc and not bc
        baseline_only += bc and not mc
    return [model_correct,baseline_correct,model_only,baseline_only]'''

HARD_REFERENCE='''from math import gcd
def solve(counts, payoffs, budget):
    a,b = budget
    total = sum(counts)
    denominator = total*b
    remaining = total*a
    minimum = min(payoffs)
    numerator = b*sum(c*g for c,g in zip(counts,payoffs))
    used = 0
    for i in sorted(range(len(counts)),key=lambda i:payoffs[i],reverse=True):
        gap = payoffs[i]-minimum
        if not remaining or not gap:
            break
        moved = min(remaining,counts[i]*b)
        numerator -= moved*gap
        remaining -= moved
        used += moved
    def pair(n,d):
        divisor = gcd(n,d)
        return [str(n//divisor),str(d//divisor)]
    return {"worst_mean":pair(numerator,denominator),
            "used_tv":pair(used,denominator)}'''

HARD_SAMPLES=[
    {'args':[[1,1],[3,-1],[1,4]],'expected':{'worst_mean':['0','1'],'used_tv':['1','4']}},
    {'args':[[1,1],[3,-1],[3,4]],'expected':{'worst_mean':['-1','1'],'used_tv':['1','2']}},
    {'args':[[1,1,8],[10,5,0],[1,5]],'expected':{'worst_mean':['0','1'],'used_tv':['1','5']}},
]
HARD_CASES=[
    {'args':[[0,5],[ -7,2],[1,2]],'expected':{'worst_mean':['-5','2'],'used_tv':['1','2']}},
    {'args':[[2,3,0],[4,4,4],[1,1]],'expected':{'worst_mean':['4','1'],'used_tv':['0','1']}},
    {'args':[[3,1],[-2,6],[0,3]],'expected':{'worst_mean':['0','1'],'used_tv':['0','1']}},
    {'args':[[1],[ -10**9],[10**9,10**9]],'expected':{'worst_mean':['-1000000000','1'],'used_tv':['0','1']}},
    {'args':[[1,9],[10,0],[2,5]],'expected':{'worst_mean':['0','1'],'used_tv':['1','10']}},
    {'args':[[10**9,10**9-1],[-10**9,10**9],[1,10**9]],'expected':{'worst_mean':['-4999999998','1999999999'],'used_tv':['1','1000000000']}},
    {'args':[[1]*4000,[i%2 for i in range(4000)],[1,4]],'expected':{'worst_mean':['1','4'],'used_tv':['1','4']}},
]

# Two-state exact transfer: independent Fraction arithmetic, not the reference.
HARD_CASES += [{'args': [[1000000000, 999999937], [999999999, -999999989], [1, 999999929]], 'expected': {'worst_mean': ['68999994274000048447', '1999999795000004473'], 'used_tv': ['1', '999999929']}}]
