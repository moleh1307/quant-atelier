"""Joint exposures, finite tail dependence and constrained discrete risk decisions."""
import math


def add_questions(add, questions):
    next(q for q in questions if q['id']=='q38')['rubric']=[
        'Compute covariance two in the same units/horizon and include both cross terms.',
        'Obtain equal-weight variance three and distinguish variance from standard deviation.',
        'Explain why the exact negative-correlation cancellation needs matching volatilities/exposures.']
    def question(suffix,title,level,minutes,prompt,answer,hints,solution,follow,follow_solution,rubric):
        add('q_l22_'+suffix,title,'Risk',level,'trader',minutes,prompt,answer,hints,solution,follow,follow_solution,'l22')
        questions[-1]['rubric']=rubric
        for key in ('prompt','solution','followSolution'):questions[-1][key]=questions[-1][key].replace(r'\n\n','\n\n')

    question('e1','A factor-neutral hedge still moves','Easy',8,
        r'Centred unit cash payoffs are X=2F+ε₁ and Y=3F+ε₂. The factor has variance nine; residual variances are four for ε₁ and nine for ε₂. F, ε₁ and ε₂ are pairwise uncorrelated with finite second moments. Take one unit of X and SHORT two thirds of a unit of Y, fixed before outcomes: H=X−(2/3)Y. What is Var(H)? Explain what was neutralised and what remains. These are position quantities, not fully allocated capital-fraction weights; no costs or other risks are included.',8,
        ['Combine factor loadings before measuring their variance.', 'The short residual coefficient is −2/3; square it before multiplying by residual variance nine.'],
        r'The factor coefficient is 2−(2/3)·3=0, so H=ε₁−(2/3)ε₂. Residual covariance is zero and \(\operatorname{Var}(H)=4+(2/3)^2\cdot9=8\). Only the specified common factor is neutralised. Gross position quantity is 5/3, net quantity 1/3; neither is the remaining variance. Independence or normality is unnecessary for this calculation.',
        r'The second factor loading changes from three to 2.5, while all stated variances and uncorrelated-residual assumptions remain. Keep the same positions. What is the new factor loading and total variance? Does setting net position quantity to zero by shorting one whole Y instead solve the problem?',
        r'The old hedge now has factor loading 2−(2/3)·2.5=1/3, giving factor variance (1/3)²·9=1 and total variance nine. A whole-unit short has net quantity zero but factor loading 2−2.5=−1/2; variance is (1/2)²·9+4+9=61/4. Net units and net factor exposure are different. An estimated model hedge is sensitive to changed loadings and does not eliminate residual, funding or execution risk.',
        ['Cancel the factor coefficient before squaring and obtain residual variance eight.', 'Separate quantities, factor loading and remaining risk.', 'Derive changed loading one third, total variance nine and reject net-unit neutrality as a substitute.'])

    question('e2','Joint stress changes variance and volatility differently','Easy',8,
        r'Two same-horizon returns are measured in percentage points. Fixed capital weights are one half each. Baseline standard deviations are two percentage points each, with correlation 0.5. A specified stress increases the FIRST standard deviation to four, keeps the SECOND at two, and raises correlation to one. What is the ratio of stressed portfolio STANDARD DEVIATION to baseline portfolio standard deviation? Derive both variances; do not report their ratio as the volatility ratio. The stress is a specified joint model, not a probability forecast.',math.sqrt(3),
        ['Baseline covariance is 0.5×2×2.', 'Standard deviation is the square root of variance.'],
        r'Baseline variance is (1/4)·4+(1/4)·4+2(1/4)·2=3. Stress covariance is 4·2=8, so stressed variance is (1/4)·16+(1/4)·4+2(1/4)·8=9. Standard deviations are √3 and three percentage points; the ratio is 3/√3=√3. Variance triples, but standard deviation does not. Variance units are squared percentage points.',
        r'Now use standard deviations two and three, and correlation −1. Do equal weights cancel risk? Which long-only weights summing to one do cancel the centred linear fluctuations in this exact model? Does zero variance imply zero mean return?',
        r'Equal-weight variance is (2−3)²/4=1/4. Perfect anticorrelation relates standardised centred fluctuations, not raw returns with different scales. Cancellation needs 2w₁=3w₂, hence w₁=3/5 and w₂=2/5. The centred portfolio is then zero almost surely, while its raw return equals its weighted mean, which need not be zero. This is an exact specified relationship, not a claim that estimated correlation stays −1.',
        ['Compute variances three and nine in consistent units.', 'Return the standard-deviation ratio √3 rather than three.', 'Handle unequal-volatility anticorrelation and distinguish a constant level from a zero mean.'])

    question('m1','More names cannot diversify away the shared shock','Medium',15,
        r'For each positive integer n, consider n centred same-horizon returns Rᵢ=F+εᵢ and weights 1/n. Var(F)=1 and Var(εᵢ)=4; residuals are mutually uncorrelated and uncorrelated with F, with finite second moments. No rebalancing or costs. What is the SMALLEST n for portfolio variance at most 1.1? Derive the variance rather than dividing the entire single-name variance by n.',40,
        ['The portfolio factor loading stays one.', 'Only the independent or uncorrelated residual part scales down with the number of names.'],
        r'The average is F+(1/n)Σ εᵢ. Its variance is 1+4/n, so 4/n≤0.1 requires n≥40. At n=40 variance equals 1.1; n=39 fails. The single-name variance five cannot simply be divided by n because every name contains the SAME factor. Mutually uncorrelated residuals suffice; independence is not required.',
        r'Instead every distinct residual pair has correlation 0.05, while residual variances remain four and all residuals stay uncorrelated with F. Derive the variance for general n and decide whether ANY finite n can achieve 1.1. Give a coherent construction for these residuals, rather than assuming arbitrary pairwise stress numbers form a valid matrix.',
        r'Each residual pair now has covariance 0.2. The average residual variance is 4/n+0.2(n−1)/n=0.2+3.8/n. Total variance is 1.2+3.8/n, exceeding 1.2 for every finite n; the target 1.1 is impossible. A coherent construction is εᵢ=√0.2·G+√3.8·Zᵢ, where G and all Zᵢ are centred, variance one, mutually uncorrelated and uncorrelated with F. The common residual component creates another nondiversifying exposure. A common correlation assumption should be checked collectively, not merely cell by cell.',
        ['Derive the factor floor and residual term 1+4/n; identify n=40 with the boundary.', 'Include all residual cross terms under the changed model.', 'Prove the unattainable target and exhibit a valid shared-residual construction.'])

    question('h1','The same covariance matrix hides different joint crashes','Hard',30,
        r'Three binary crash indicators X₁,X₂,X₃ each satisfy P(Xᵢ=1)=1/2. Every distinct pair is INDEPENDENT, but joint independence is not assumed. Unit cash payoffs are Yᵢ=1−2Xᵢ and the fixed equal-weight payoff is H=(Y₁+Y₂+Y₃)/3. Derive the SHARP possible interval for P(H<−2/3) over all joint distributions consistent with these assumptions. Construct distributions attaining both endpoints, and verify they have the SAME payoff means and covariance matrix. A covariance-only calculation must not invent a joint crash probability.',None,
        ['The strict loss threshold occurs exactly when all three indicators are one.', 'Write all eight cell probabilities in terms of q=P(1,1,1), using the marginal and pair constraints.', 'Nonnegativity of every cell gives bounds; explicit endpoint tables prove sharpness.'],
        r'Let q=P(X₁=X₂=X₃=1). Pair independence gives each double-one marginal probability 1/4. Consequently each EXACTLY-two-one cell has mass 1/4−q. The individual one-margins then force each EXACTLY-one-one cell to have mass q; total mass forces P(0,0,0)=1/4−q. Nonnegativity is equivalent to \(0\leq q\leq1/4\). Since H=1−(2/3)(X₁+X₂+X₃), the strict event H<−2/3 is exactly the all-one cell.\n\nAt q=0 use equal probability 1/4 on 000,011,101,110. At q=1/4 use equal probability 1/4 on 001,010,100,111. Every indicator is fair and every two-indicator table is uniform in both constructions. Each Yᵢ has mean zero/variance one, and each payoff pair has covariance zero. Therefore both give the same covariance matrix I and Var(H)=1/3, yet their joint crash probabilities are zero and 1/4. Every intermediate q is attained by mixing the two tables; the full interval is sharp. Jointly independent indicators would give 1/8, which is only one permitted value.',
        r'Can you reject the high-crash construction by calling its zero covariances evidence of three independent risks? If instead the requirement was full JOINT independence, what happens to the interval and the distribution of H? What additional evidence would a risk report need beyond second moments?',
        r'Zero payoff covariance, even paired with pairwise indicator independence, does not imply mutual independence. Under full joint independence all eight cells have probability 1/8, so the crash probability is fixed at 1/8. The crash count is then Binomial(3,1/2) and H has values 1,1/3,−1/3,−1 with probabilities 1/8,3/8,3/8,1/8. A report about the joint downside needs a specified or estimated joint law, including higher-order dependence and appropriate support/horizon, plus uncertainty and executable loss assumptions. The identical mean/variance alone do not determine it.',
        ['Translate the strict portfolio event to the all-one cell.', 'Derive all eight masses and prove 0≤q≤1/4 from their nonnegativity.', 'Construct both endpoints, verify pairwise independence and the identical covariance I/portfolio variance 1/3.', 'Distinguish pairwise from joint independence and compute the independent case 1/8.'])

    question('h2','A hedge chosen before uncertain loadings are known','Hard',30,
        r'In each specified model, centred payoffs are X=F+ε₁ and Y=bF+ε₂, with Var(F)=4, Var(ε₁)=Var(ε₂)=1 and all three components pairwise uncorrelated. The loading b is an unknown FIXED model parameter in [1,3], with no probability distribution assigned. Choose a fixed nonnegative short quantity h before knowing b: H=X−hY. Minimise the WORST-MODEL variance over that interval. Derive the globally optimal h and value, including where the active stress model changes. Do not replace the ambiguity set by its midpoint or choose h separately after learning b.',None,
        ['For fixed h, the variance is convex in b, so its maximum on the interval occurs at an endpoint.', 'Compare the two endpoint squared factor loadings; the active one switches at h=1/2.', 'Check derivatives on both sides of the switch, rather than averaging endpoint models.'],
        r'The specified variance is \(v_b(h)=4(1-bh)^2+1+h^2\). For fixed h its maximum in b is at 1 or 3. Their difference is \(v_1(h)-v_3(h)=16h(1-2h)\). Thus the worst-model envelope is\n\n\[v(h)=\begin{cases}5-8h+5h^2,&0\leq h\leq1/2,\\5-24h+37h^2,&h\geq1/2.\end{cases}\]\n\nThe left derivative −8+10h stays negative up to the switch, where it is −3. The right derivative −24+74h is positive from the switch onward, starting at 13. The unique global minimum is therefore h=1/2, with worst variance 9/4. Both endpoint models are active there; no single smooth derivative is zero at this kink. The midpoint model alone has minimiser 8/17, which gives worse worst-case variance 677/289. Averaging endpoint variances also describes another objective, not the model-set maximum.',
        r'Now the hedge residual variance is a known d≥0 instead of one, while the primary residual variance remains one. Derive the optimal robust hedge for ALL d, not just the original case. Explain why a factor-balanced hedge can become too costly in residual risk.',
        r'The factor comparison and switch at 1/2 are unchanged. The left branch is 5−8h+(4+d)h², whose unconstrained minimum is 4/(4+d); the right derivative at the switch is 12+d>0 and increases thereafter. Thus h*=min(1/2,4/(4+d)). For 0≤d≤4 the minimum is at the kink, with variance 2+d/4. For d≥4 it is on the low-loading branch, with variance 5−16/(4+d); the two formulas agree at d=4. At d=12, h*=1/4 and variance four, whereas the factor-balanced 1/2 hedge gives variance five. A hedge can reduce factor uncertainty while adding enough residual risk that a smaller position is preferable. Costs, means and funding rules could further change the action set/objective; none is included in this variance problem.',
        ['Derive each model variance with squared signed loadings and residual exposures.', 'Justify the endpoint worst case and active-model switch.', 'Use both one-sided derivatives to prove h=1/2/variance 9/4 is globally optimal.', 'Derive the d-dependent minimum, its boundary d=4 and d=12 counterexample.'])


def add_coding(add,tasks):
    def code(suffix,title,level,prompt,signature,samples,tests,solution,explanation):
        add('c_l22_'+suffix,title,level,'Risk',prompt,signature,samples,tests,solution,explanation)
        tasks[-1]['path']='trader'
        for key in ('prompt','explanation'):tasks[-1][key]=tasks[-1][key].replace(r'\n\n','\n\n')

    code('easy','Aggregate shared loadings before squaring risk','Easy',
        r'Centred unit cash payoffs satisfy \(Y_i=\sum_j b_{ij}F_j+\varepsilon_i\), where \(b_{ij}\) is loadings[i][j]. quantities gives n fixed signed INTEGER position quantities, 1≤n≤1000; loadings is an n by k integer matrix, 0≤k≤20. Each factor F_j has integer variance factor_variances[j]; residual ε_i has integer variance residual_variances[i]. All factors and residuals are pairwise uncorrelated with finite second moments. Quantities and loadings are in [−10^6,10^6]; variances in [0,10^6]. All dimensions match. Return {"exposures":[signed_integer_strings],"factor_variance":integer_string,"residual_variance":integer_string,"variance":integer_string} for the combined CASH payoff \(\sum_i q_iY_i\), where \(q_i\) is quantities[i]. Every number must be a canonical decimal STRING; zero is "0". Means, fees, funding and higher moments are outside this task. Preserve all inputs. Use O(n(k+1)) integer arithmetic/O(k) auxiliary integers, with bit costs additional. Do not normalise quantities into portfolio weights or square each position loading before aggregating a shared factor.',
        'def solve(quantities, loadings, factor_variances, residual_variances):',
        [{'args':[[1,-1],[[1],[1]],[9],[1,1]],'expected':risk_result([0],0,2)},
         {'args':[[2,-1],[[1,2],[3,-1]],[4,9],[1,4]],'expected':risk_result([-1,5],229,8)},
         {'args':[[10**6],[[10**6]],[10**6],[10**6]],'expected':risk_result([10**12],10**30,10**18)}],
        [{'args':[[2,-3],[[],[]],[],[4,1]],'expected':risk_result([],0,25)},
         {'args':[[0],[[99]],[100],[10]],'expected':risk_result([0],0,0)},
         {'args':[[-2],[[3,-4]],[0,5],[7]],'expected':risk_result([-6,8],320,28)},
         {'args':[[1]*1000,[[1]*20 for _ in range(1000)],[1]*20,[1]*1000],'expected':risk_result([1000]*20,20000000,1000)}],
        '''def solve(quantities, loadings, factor_variances, residual_variances):
    exposures = [0]*len(factor_variances)
    residual = 0
    for q,row,rv in zip(quantities,loadings,residual_variances):
        residual += q*q*rv
        for j,beta in enumerate(row):
            exposures[j] += q*beta
    factor = sum(a*a*v for a,v in zip(exposures,factor_variances))
    return {'exposures':[str(a) for a in exposures], 'factor_variance':str(factor),
            'residual_variance':str(residual), 'variance':str(factor+residual)}''',
        r'The combined loading on factor j is the SIGNED sum a_j=Σ_i q_i b_ij. Pairwise uncorrelated factors and residuals give factor variance Σ_j a_j² Var(F_j) and residual variance Σ_i q_i² Var(ε_i). A shared factor must be summed before it is squared; opposing exposures can cancel that factor while residual terms remain. Independence is stronger than necessary for this second-moment calculation. Empty factor lists leave only residual risk; zero factor variances do not make nonzero reported exposures disappear. A single pass accumulates the k exposures and residual scalar; exact Python integers and decimal strings preserve large squared quantities in the browser. This computes risk under the supplied model, not an empirical covariance estimate or an execution guarantee.')

    code('medium','Average the worst probability mass of the whole book','Medium',
        r'scenario_pnl is an m by n integer matrix of JOINT unit cash payoffs for fixed same-horizon scenarios, 1≤m≤5000 and 1≤n≤20. quantities has n signed integer quantities. weights has m integer probability COUNTS in [0,10^6] with positive total W. Pnl entries and quantities are in [−10^6,10^6]. Each portfolio cash LOSS is \(L_s=-\sum_i q_iP_{si}\), where \(q_i\) is quantities[i] and \(P_{si}\) is scenario_pnl[s][i]. Supplied payoffs already include all stated costs/exits: do not subtract them again. tail=[a,b], integers 1≤a≤b≤10^6, specifies alpha=a/b. Sort positive-mass scenarios by DESCENDING loss and take exactly the worst alpha fraction of total probability, splitting the final scenario mass if necessary. Return {"threshold":signed_integer_string,"tail_mean":[signed_numerator_string,positive_denominator_string]}. threshold is the SMALLEST loss used with positive mass in that selected tail, including when the cutoff is an exact boundary. tail_mean is the exact average loss in the selected probability mass. Losses may be NEGATIVE; never clamp profits to zero. Equal losses, duplicate scenarios and zero counts are permitted. Rationals must be reduced canonical decimal strings, with zero=["0","1"]. Preserve all inputs. Use O(mn+m log m) arithmetic/comparisons and O(m) auxiliary records, with integer bit/gcd costs additional. Aggregate the JOINT book before sorting; averaging whole scenario records or summing independently selected component tails is wrong. This is a specified finite-distribution tail measure, not an estimated probability or a guaranteed funding limit.',
        'def solve(scenario_pnl, quantities, weights, tail):',
        [{'args':[[[-10],[-4],[6]],[1],[1,2,7],[1,4]],'expected':{'threshold':'4','tail_mean':['32','5']}},
         {'args':[[[-5,5],[5,-5]],[1,1],[1,1],[1,2]],'expected':{'threshold':'0','tail_mean':['0','1']}},
         {'args':[[[-10**6,-10**6],[0,0]],[10**6,10**6],[10**6,999999],[1,1]],'expected':{'threshold':'0','tail_mean':['2000000000000000000','1999999']}}],
        [{'args':[[[-10],[0],[5]],[1],[1,8,1],[1,5]],'expected':{'threshold':'0','tail_mean':['5','1']}},
         {'args':[[[-10],[0],[5]],[1],[1,8,1],[1,20]],'expected':{'threshold':'10','tail_mean':['10','1']}},
         {'args':[[[5],[10]],[1],[1,1],[1,2]],'expected':{'threshold':'-5','tail_mean':['-5','1']}},
         {'args':[[[-999],[-3],[1]],[1],[0,1,1],[1,2]],'expected':{'threshold':'3','tail_mean':['3','1']}},
         {'args':[[[-10],[-2],[7]],[1],[1,1,2],[1,2]],'expected':{'threshold':'2','tail_mean':['6','1']}},
         {'args':[[[-4],[-4],[8]],[-2],[1,2,3],[1,1]],'expected':{'threshold':'-8','tail_mean':['4','1']}},
         {'args':[[[1]*20 for _ in range(5000)],[1]*20,[1]*5000,[1,10**6]],'expected':{'threshold':'-20','tail_mean':['-20','1']}}],
        '''from math import gcd

def solve(scenario_pnl, quantities, weights, tail):
    a,b = tail
    total = sum(weights)
    remaining = total*a
    rows = sorted((-sum(q*p for q,p in zip(quantities,row)),w)
                  for row,w in zip(scenario_pnl,weights) if w)
    numerator = 0
    threshold = None
    for loss,w in reversed(rows):
        take = min(w*b,remaining)
        numerator += take*loss
        threshold = loss
        remaining -= take
        if remaining == 0:
            break
    denominator = total*a
    divisor = gcd(abs(numerator),denominator)
    return {'threshold':str(threshold),
            'tail_mean':[str(numerator//divisor),str(denominator//divisor)]}''',
        r'First aggregate each joint scenario into the actual signed book loss. Weight counts describe probability mass, not equally likely scenario rows. Multiply count masses by b, so total scaled mass is Wb and the requested tail is the INTEGER amount Wa. Descending losses receive up to w_s b units until exactly Wa units are allocated. Their weighted loss numerator divided by Wa is the tail mean; the final positive allocation identifies the explicitly defined threshold. Splitting an atom is essential: sample one uses one count at loss ten and one-and-a-half counts at loss four, producing (10+1.5·4)/2.5=32/5. Taking every observation at or above the cutoff would instead average a different probability mass. Duplicate equal losses do not change the answer, and zero-count states are excluded before threshold selection. Alpha one recovers the full expected loss, which may be negative. Sample two has opposite unit movements but an identically zero book; summing two separate component tails would invent book losses. Exact integer scaling avoids rounding the tail size or a large rational numerator.')

    code('hard','Choose trades under shared-factor and gross-capital limits','Hard',
        r'There are n indivisible opportunities, 0≤n≤40. Integer lists gains, loadings and margins have length n: gain_i in [−10^6,10^6] is the declared expected NET cash payoff if selected once; loading_i in [−10,10] is its signed exposure to one centred variance-one common factor; margin_i in [1,80] is required gross capital. Write \(g_i\)=gains[i], \(\ell_i\)=loadings[i] and \(m_i\)=margins[i]. The stylised payoff is \(g_i+\ell_iF\), with no residual risks. A chosen subset I has expected payoff \(\sum_{i\in I}g_i\), factor loading \(\sum_{i\in I}\ell_i\) and variance \((\sum_{i\in I}\ell_i)^2\). Choose once BEFORE outcomes. Integer capital in [0,80] bounds \(\sum_{i\in I}m_i\); integer exposure_limit in [0,400] requires \(\left|\sum_{i\in I}\ell_i\right|\leq\texttt{exposure\_limit}\) at the FINAL book. Margins do not net, even for opposing exposures. Empty selection is allowed. Maximise total expected gain; ties prefer lower total margin, then fewer selected opportunities, then lexicographically smaller SORTED original index list. Return {"gain":integer,"margin":integer,"indices":[indices]}. Preserve all inputs. Negative-gain opportunities must not be discarded automatically: they can make a desirable combined exposure feasible. Do not prune an intermediate loading merely because it exceeds the FINAL limit; later positions may offset it. With B=capital and A=sum(abs(loadings)), use a dynamic program that selects each opportunity at most once, with O(n(B+1)(2A+1)) score transitions and O((B+1)(2A+1)) stored score/reconstruction states. State counts are finite; exact bit masks may use O(n) bits per state for reconstruction. This is a discrete specified selection model, not a live profitability or funding certification. No borrowing, partial trades, changing gains after outcomes or assumed zero covariance among these common-factor payoffs.',
        'def solve(gains, loadings, margins, capital, exposure_limit):',
        [{'args':[[10,-3],[10,-10],[1,1],2,0],'expected':{'gain':7,'margin':2,'indices':[0,1]}},
         {'args':[[6,6,12],[1,-1,0],[1,1,2],2,0],'expected':{'gain':12,'margin':2,'indices':[2]}},
         {'args':[[5,5,5],[0,0,0],[1,1,1],1,0],'expected':{'gain':5,'margin':1,'indices':[0]}}],
        [{'args':[[],[],[],80,0],'expected':{'gain':0,'margin':0,'indices':[]}},
         {'args':[[10,-3],[10,-10],[1,1],1,0],'expected':{'gain':0,'margin':0,'indices':[]}},
         {'args':[[6,6],[2,-2],[2,2],3,0],'expected':{'gain':0,'margin':0,'indices':[]}},
         {'args':[[0,0,-1],[0,0,0],[1,1,1],80,400],'expected':{'gain':0,'margin':0,'indices':[]}},
         {'args':[[5,5],[0,0],[2,1],2,0],'expected':{'gain':5,'margin':1,'indices':[1]}},
         {'args':[[10,2],[1,0],[1,1],2,0],'expected':{'gain':2,'margin':1,'indices':[1]}},
         {'args':[[4,4],[1,1],[1,1],2,2],'expected':{'gain':8,'margin':2,'indices':[0,1]}},
         {'args':[[1]*40,[10]*20+[-10]*20,[1]*40,20,0],'expected':{'gain':20,'margin':20,'indices':list(range(10))+list(range(20,30))}}],
        '''def solve(gains, loadings, margins, capital, exposure_limit):
    n = len(gains)
    states = {(0,0):(0,0,0)}
    for i,(gain,loading,margin) in enumerate(zip(gains,loadings,margins)):
        updated = dict(states)
        bit = 1 << (n-1-i)
        for (spent,exposure),(score,negative_count,mask) in states.items():
            if spent+margin > capital:
                continue
            key = (spent+margin,exposure+loading)
            candidate = (score+gain,negative_count-1,mask|bit)
            if key not in updated or candidate > updated[key]:
                updated[key] = candidate
        states = updated
    best = (0,0,0,0)
    for (spent,exposure),(score,negative_count,mask) in states.items():
        if abs(exposure) <= exposure_limit:
            best = max(best,(score,-spent,negative_count,mask))
    score,negative_spent,_,mask = best
    return {'gain':score,'margin':-negative_spent,
            'indices':[i for i in range(n) if mask & (1 << (n-1-i))]}''',
        r'A state records exact used gross capital and SIGNED factor loading after an item prefix. Keep the best expected gain for that state; on equal gains keep fewer trades, then the lexicographically smaller original-index list. All future choices affect two equal-state prefixes identically, so this dominance preserves the final objective and tie rules. Read transitions from the previous prefix and write into a copied next map: each opportunity is selected at most once. A load of +10 followed by −10 is feasible at final limit zero, so applying the final risk test during intermediate layers would discard sample one; so would discarding the negative-gain hedge. Gross margins add even when factor exposure cancels.\n\nFor compact exact reconstruction, give earlier indices more significant bits. When selection counts tie, the larger mask has the smaller first differing index and therefore the lexicographically smaller sorted list. Prefix dominance stores (gain,negative_count,mask). The final comparison additionally prefers smaller capital BEFORE fewer items. Empty selection supplies zero gain and zero capital. The possible capital coordinates are 0..B and exposure coordinates −A..A, where A is the sum of absolute input loadings; each item considers at most their product, rather than enumerating all 2^n subsets. Masks carry up to n bits and are internal, never an approximate numeric risk measure. This exact constrained optimum inherits every assumption and omitted risk of the supplied single-factor model.')


def risk_result(exposures,factor,residual):
    return {'exposures':[str(v) for v in exposures],'factor_variance':str(factor),
            'residual_variance':str(residual),'variance':str(factor+residual)}
