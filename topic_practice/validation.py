"""Validation practice separates historical eligibility, overlap and evaluation targets."""


def add_questions(add, questions):
    rubrics = {
        'q27': ['Diagnose shared target outcomes, future-to-past training and fitted-transform/selection leakage separately.',
                'Specify decision-time availability, target-interval endpoint conventions, chronological refits and fold-local transformations.',
                'Separate inner selection from outer evaluation and final reserved evidence; justify any extra embargo rather than asserting independence.'],
        'q28': ['Identify the full-series fitted parameters as future information, without asserting every model benefits from every affine leak.',
                'Fit preprocessing inside each eligible training fold and freeze it for the corresponding evaluation decisions.',
                'Check receipt times, shifts and fitted state when claiming a rolling transformation is causal.'],
    }
    for q in questions:
        if q['id'] in rubrics:
            q['rubric'] = rubrics[q['id']]
            if q['id'] == 'q27':
                q['solution'] = q['solution'].replace('whose intervals touch test labels', 'whose intervals overlap test-label information')

    def question(suffix, title, level, minutes, prompt, answer, hints, solution, follow, follow_solution, rubric):
        add('q_l14_'+suffix, title, 'Validation', level, 'researcher', minutes,
            prompt, answer, hints, solution, follow, follow_solution, 'l14')
        questions[-1]['rubric'] = rubric
        for key in ('prompt','solution','followSolution'):
            questions[-1][key] = questions[-1][key].replace(r'\n\n','\n\n')

    question('e1','A historical row can still be unavailable','Easy',6,
        r'Each row below is [original decision time, feature receipt time, label receipt time]: [[0,0,3],[2,3,5],[4,4,9],[7,7,10],[8,8,12],[9,11,10]]. At fit time T=10 all receipts stamped at most 10 have arrived. A training row must have a decision strictly before T, a feature received no later than its ORIGINAL decision, and a label received no later than T. Each label uses future outcomes after its decision; its receipt includes any publication delay. How many rows qualify? Having a feature now does not mean it was usable at the original decision.',3,
        ['Apply the feature boundary at the original decision, not the later fit time.',
         'A label received exactly at ten is allowed under this explicit inclusive rule.'],
        r'Original rows 0,2,3 qualify: their decisions are 0,4,7, their features were received on time, and their labels arrived at 3,9,10. Thus the count is three. Row 1 uses a feature received at three for a decision at two; row 4 has an unfinished label; row 5 has a late feature even though its label is available. Sorting decision timestamps or checking only the fit-time receipt boundary misses different violations.',
        r'If fitting happens immediately BEFORE receipts stamped 10, how does the count change? If the late features were replaced by explicit missing values through a pre-specified causal pipeline, would discarding those rows still be compulsory?',
        r'The label criterion becomes strictly less than ten, excluding row 3 and leaving two. The declared original feature was unavailable, so it cannot be retroactively substituted. A different pre-specified model that can act on genuine missing inputs may keep such decisions with those missing values; its performance evaluates that different pipeline. This problem counts rows usable with the declared received feature, not every conceivable missing-value policy.',
        ['Check feature receipt against original decision and label receipt against fit cutoff.',
         'Identify rows 0,2,3 and obtain count three.',
         'Apply the strict-cutoff change and distinguish exclusion from a different missing-input procedure.'])

    question('e2','Averaging folds changes the population','Easy',6,
        r'Two nonoverlapping evaluation blocks contain two and eight decisions. Their average squared prediction losses are respectively 1 and 4. Predictions were recorded before outcomes, and the deployment estimand is average loss per decision over these TEN decisions, each weighted equally. What is the pooled average loss? Distinguish this from an unweighted average of the two block scores. No iid assumption is supplied.',17/5,
        ['Recover the total loss in each block before pooling.',
         'The denominator is ten decisions, not two blocks.'],
        r'Total loss is 2·1+8·4=34, giving 34/10=17/5=3.4. The unweighted block average is (1+4)/2=2.5. It assigns each decision in the short block four times the weight of each decision in the long block. This is an estimand choice, not an arithmetic approximation. Serial dependence does not alter this identity, but does affect the uncertainty assigned to the estimate.',
        r'Could 2.5 be the intended estimate under a different deployment target? Do two block scores justify estimating uncertainty as though there were ten independent losses?',
        r'Yes: choose a block with equal probability, then a decision uniformly inside that block. That population weights the blocks equally and has average loss 2.5. It differs from selecting one of the ten decisions uniformly. Two block means and counts do not identify within-block variance or cross-block dependence, so they cannot justify an iid ten-loss standard error. State both the target weighting and the dependence assumptions.',
        ['Recover block totals 2 and 32 and pool over ten decisions.',
         'Explain the different decision weights behind the value 2.5.',
         'Separate a loss identity from unsupported independence and uncertainty claims.'])

    question('m1','Disjoint labels can still be future training','Medium',16,
        r'At fit cutoff 10, all receipts with timestamp ≤10 are available. Five candidate rows have [label start,label end,label receipt] [[2,6,6],[6,10,10],[9,12,12],[14,17,17],[8,10,13]]. Labels use half-open intervals [start,end), and all features were available at their original starts. Protect the validation information interval [10,14). First identify original indices retained by OVERLAP PURGING ALONE. Then identify indices usable for a strict past-to-future fit at ten, requiring start<10 and label receipt≤10 as well as non-overlap. Explain why an arbitrary row-count gap is insufficient.',None,
        ['Touching half-open endpoints do not intersect.',
         'Purging alone knows neither the fit cutoff nor publication delay.',
         'Compare row 3, which is disjoint but future, with row 4, which ends on time but is released late.'],
        r'Purging alone retains indices [0,1,3,4]. Row 2 intersects [10,14); row 1 ends exactly at ten and row 3 starts exactly at fourteen, so neither touches the protected interior. The deployment fit retains only [0,1]. Row 3 is future training; row 4 has an unavailable label despite an end timestamp of ten. The correct maturity criterion is receipt, not end alone. An index gap counts rows rather than elapsed information time and cannot generally represent variable horizons, irregular timestamps or delayed publication.',
        r'For a strictly historical fit at T, suppose every selected label ends no later than its receipt, and every receipt is ≤T. If protected evaluation begins at T, can any selected half-open label overlap it? Does this imply independence or make embargo irrelevant in all resampling designs?',
        r'No selected label can overlap a protected interval beginning at T: its end is ≤T, so it lies on the non-overlap side of that boundary. Here the actual maturity rule already removes target spillover; a redundant purge is not an additional source of independence. Shared features, common factors and temporal dependence can remain. In resampling that reuses later rows or protects an earlier block, overlap and additional exclusion mechanisms may still matter. An embargo needs a stated information/dependence reason and does not universally turn data iid.',
        ['Apply half-open overlap exactly and retain [0,1,3,4] under purging alone.',
         'Apply history and receipt constraints separately to obtain [0,1].',
         'Prove the forward-boundary implication without claiming independence.',
         'Explain why irregular timing and publication delays defeat a fixed row gap.'])

    question('h1','An adaptive evaluation can be honest','Hard',30,
        r'At each of n≥1 pre-specified decisions, a binary prediction \(a_t\) is fixed before binary outcome \(Y_t\) arrives. Let \(\mathcal F_{t-1}\) denote EVERYTHING legitimately known when \(a_t\) is fixed, including earlier mature outcomes, past model choices and any already drawn prediction randomization. Define loss \(L_t=\mathbf1\{a_t\ne Y_t\}\) and conditional risk \(r_t=E[L_t\mid\mathcal F_{t-1}]\). All prior losses and risks are measurable at later decision information sets. Outcomes need NOT be iid. Prove that the mean realized loss minus the mean of these possibly RANDOM conditional risks has expectation zero, derive its second moment, and give a distribution-free 95-percent error band using only Chebyshev. What procedure does that band evaluate? Contrast refitting from mature past evaluation outcomes with retrospectively choosing a model using all the evaluation scores.',None,
        [r'The centered increment \(D_t=L_t-r_t\) has conditional mean zero.',
         r'For s<t, \(D_s\) is known in \(\mathcal F_{t-1}\), so compute the cross expectation by conditioning.',
         r'A binary loss has conditional variance \(r_t(1-r_t)\leq1/4\). The target here is the average conditional risk along the recorded procedure.'],
        r'Write \(\bar L_n=n^{-1}\sum_{t=1}^n L_t\), \(\bar r_n=n^{-1}\sum_{t=1}^n r_t\), and \(D_t=L_t-r_t\). By definition \(E[D_t\mid\mathcal F_{t-1}]=0\). For s<t, tower conditioning gives \(E[D_sD_t]=E[D_s E[D_t\mid\mathcal F_{t-1}]]=0\). This does not assert independent losses or constant risks. Since the binary loss has conditional probability \(r_t\) of being one, \(E[D_t^2\mid\mathcal F_{t-1}]=r_t(1-r_t)\). Consequently\n\n\[\begin{aligned}E[\bar L_n-\bar r_n]&=0,\\E[(\bar L_n-\bar r_n)^2]&=\frac1{n^2}\sum_{t=1}^n E[r_t(1-r_t)]\\&\leq\frac1{4n}.\end{aligned}\]\n\nChebyshev gives probability at least 0.95 that the recorded average conditional risk lies within \(\sqrt{5/n}\) of the average realized loss; intersect this band with [0,1]. It can be very wide. The radius uses a PRE-SPECIFIED n: selecting when to report after inspecting errors is a different stopping problem. It evaluates the recorded adaptive forecasting procedure and the risk along its realized information history. It is not automatically a confidence interval for one frozen final model, a future regime, or an iid population parameter. Refitting on earlier mature outcomes may imitate deployment, provided the originally recorded predictions are not rewritten. A retrospectively selected candidate was not generally predictable at the times whose losses are reported; that selection changes the evaluation question.',
        r'For two iid fair outcomes, evaluate the two constant classifiers zero and one on BOTH outcomes, then report the smaller average loss, breaking ties arbitrarily. Calculate its expected reported loss and its expected loss on an independent future fair outcome. If instead the classifier may adapt only to earlier outcomes before each prediction, what is its expected reported loss?',
        r'Of the four equally likely pairs 00,01,10,11, the smaller average loss is zero on 00 and 11 and one half on the mixed pairs. Its expectation is one quarter. Whichever constant is selected has error probability one half on an independent future fair bit. Under any genuinely predictable adaptive rule, each next fair bit is independent of its already fixed prediction, so \(E[L_t\mid\mathcal F_{t-1}]=1/2\) and average expected loss is one half. Updating from past scores and using future scores to choose which past prediction to report are different procedures. The cheap selected score is not unbiased evidence for the chosen model.',
        ['Define predictable predictions, nested information and the random conditional-risk target.',
         'Prove zero conditional increments and zero cross moments without claiming iid losses.',
         r'Derive the finite second-moment bound and \(\sqrt{5/n}\) 95-percent band for fixed n.',
         'Distinguish adaptive procedure risk from final-model/future-regime claims and calculate selected loss 1/4 versus future risk 1/2.'])


def add_coding(add, tasks):
    def exercise(level,title,prompt,signature,samples,tests,solution,explanation):
        add('c_l14_'+level.lower(),title,level,'Validation',prompt,signature,samples,tests,solution,explanation)
        tasks[-1]['path']='researcher'
        for key in ('prompt','explanation'):
            tasks[-1][key]=tasks[-1][key].replace(r'\n\n','\n\n')

    exercise('Easy','Keep only historically usable training rows',
        r'rows is an unsorted list of [decision_at,feature_received_at,label_received_at]. Each row is a distinct sample, including identical triples. For a fit at cutoff, require decision_at<cutoff, feature_received_at≤decision_at and label_received_at≤cutoff. Exact-time receipts are included by the stated rule. Features arriving after the original decision cannot be filled retrospectively. Return qualifying ORIGINAL indices in input order; do not reorder or mutate rows. Times and cutoff are integers in [0,10^12], label_received_at>decision_at, and there are at most 100000 rows. Empty inputs return []. Use O(n) time and O(1) auxiliary space beyond output. This checks availability of the declared feature/label, not all preprocessing, selection, independence or execution assumptions.',
        'def solve(rows, cutoff):',
        [{'args':[[[0,0,3],[2,3,5],[4,4,9],[7,7,10],[8,8,12],[9,11,10]],10],'expected':[0,2,3]},
         {'args':[[[5,5,6],[0,0,5],[0,0,5],[4,5,5]],5],'expected':[1,2]}],
        [{'args':[[],0],'expected':[]},
         {'args':[[[0,0,1]],0],'expected':[]},
         {'args':[[[0,0,1]],1],'expected':[0]},
         {'args':[[[1,1,3],[2,1,5],[3,2,6]],5],'expected':[0,1]},
         {'args':[[[1,2,3],[1,1,4],[1,0,3]],3],'expected':[2]},
         {'args':[[[10**12-1,10**12-1,10**12]],10**12],'expected':[0]},
         {'args':[[[i,i,i+1] for i in range(4000)],2000],'expected':list(range(2000))}],
        '''def solve(rows, cutoff):
    return [i for i,(decision,feature,label) in enumerate(rows)
            if decision < cutoff and feature <= decision and label <= cutoff]''',
        r'Check the three information boundaries independently on every original row. Feature causality uses the original decision; label maturity uses the later fit. Equality is deliberately inclusive for receipts and strict for historical decisions. Preserve duplicates as distinct indices. A single pass makes O(n) comparisons; output storage depends on how many rows qualify. Keeping a row with an unavailable feature by retroactively filling it implements a different, leaking pipeline.')

    exercise('Hard','Audit many delayed-label folds without scanning each one',
        r'Each unsorted row is [start,end,feature_received_at,label_received_at]. Its label uses the half-open information interval [start,end). All times are integers in [0,10^12], with start<end≤label_received_at. The feature may arrive later than start; such a row is permanently unusable for its original decision. Duplicate rows are distinct samples.\n\nEach unsorted query is [fit_at,earliest_start,protected_start,protected_end], with 0≤earliest_start≤fit_at≤10^12 and 0≤protected_start<protected_end≤10^12. Count rows that simultaneously have feature_received_at≤start, label_received_at≤fit_at, start≥earliest_start, and NO overlap with [protected_start,protected_end). Receipt equality is included; touching interval endpoints is disjoint. Since end≤label_received_at, active rows automatically have start<fit_at. Return counts in ORIGINAL query order, retaining duplicate queries and preserving both inputs. Empty lists are allowed; each list has at most 20000 entries.\n\nProtected blocks can lie earlier than fit_at: this task audits interval exclusion in a candidate resampling design. A count does not certify that such a design estimates a forward-deployed model. When protected_start≥fit_at, maturity already prevents label overlap. You must still honor earliest_start and feature causality.\n\nAim for O((N+Q)log²(N+Q+2)) time and O(N log(N+2)+Q) storage, including preprocessing/sorting, where N and Q are input lengths. Do not scan all N rows for every query. Prerequisite: coordinate compression and a Fenwick prefix-count tree; a nested Fenwick structure can count active points with start<x and end≤y. Derive a query decomposition that respects both endpoints.',
        'def solve(rows, queries):',HARD_SAMPLES,HARD_CASES,HARD_REFERENCE,
        r'Ignore feature-ineligible rows and sweep queries by fit_at, activating a row once its label receipt is ≤that cutoff. Store each active interval as a point (start,end). Non-overlap is end≤u OR start≥v for protected [u,v). These branches are DISJOINT because start<end and u<v. The first branch also needs start≥L; the second needs start≥max(L,v).\n\nLet P(x,y) count active points with start<x and end≤y, and let M=10^12+1, strictly beyond every input timestamp. The answer is\n\n\[P(M,u)-P(L,u)+P(M,M)-P(\max(L,v),M).\]\n\nBuild a compressed Fenwick tree over start; each outer node has its own sorted list of end coordinates and inner Fenwick counts. A point activation touches O(log N) outer nodes and O(log N) work inside each. Prefix counting uses the same two logarithmic traversals. Inner coordinate lists are compiled from all feature-eligible rows, but initially store ZERO counts: reading coordinate support during preprocessing does not activate future labels. Restore original query order after the fit-time sweep. The earliest boundary is inclusive, so prefix subtraction uses STRICT start<L; end≤u includes the disjoint touching case. Empty eligible support returns zeros. Purging is the stated interval operation, not a guarantee of independence or correct model-selection evidence.')


HARD_REFERENCE = '''from bisect import bisect_left, bisect_right
def solve(rows, queries):
    valid = [(a,b,r) for a,b,f,r in rows if f <= a]
    if not valid:
        return [0] * len(queries)
    starts = sorted(set(a for a,b,r in valid))
    n = len(starts)
    ends = [[] for _ in range(n+1)]
    for a,b,r in valid:
        i = bisect_left(starts,a)+1
        while i <= n:
            ends[i].append(b)
            i += i & -i
    ends = [sorted(set(values)) for values in ends]
    trees = [[0] * (len(values)+1) for values in ends]
    def activate(a,b):
        i = bisect_left(starts,a)+1
        while i <= n:
            j = bisect_left(ends[i],b)+1
            while j < len(trees[i]):
                trees[i][j] += 1
                j += j & -j
            i += i & -i
    def prefix(x,y):
        i = bisect_left(starts,x)
        count = 0
        while i:
            j = bisect_right(ends[i],y)
            while j:
                count += trees[i][j]
                j -= j & -j
            i -= i & -i
        return count
    valid.sort(key=lambda row:row[2])
    result = [0] * len(queries)
    cursor = 0
    infinity = 10**12+1
    for index,(cutoff,lower,u,v) in sorted(enumerate(queries),key=lambda item:item[1][0]):
        while cursor < len(valid) and valid[cursor][2] <= cutoff:
            a,b,r = valid[cursor]
            activate(a,b)
            cursor += 1
        result[index] = (prefix(infinity,u)-prefix(lower,u)
                         +cursor-prefix(max(lower,v),infinity))
    return result'''

HARD_SAMPLES = [
    {'args':[[[2,6,2,6],[6,10,6,10],[9,12,9,12],[14,17,14,17],[8,10,8,13]],
             [[10,0,10,14],[20,0,10,14],[20,8,10,14],[20,0,6,10]]],
     'expected':[2,4,2,2]},
    {'args':[[[0,3,0,3],[0,3,0,3],[3,5,4,5],[5,7,5,9]],
             [[9,0,3,5],[3,0,3,5],[8,5,7,8],[9,5,7,8],[9,6,7,8]]],
     'expected':[3,2,0,1,0]},
]
HARD_CASES = [
    {'args':[[],[[0,0,0,1],[10**12,0,0,10**12]]],'expected':[0,0]},
    {'args':[[[0,1,0,1]],[]],'expected':[]},
    {'args':[[[0,1,1,1],[2,4,3,4]],[[10,0,1,2]]],'expected':[0]},
    {'args':[[[0,2,0,10],[3,5,3,5],[5,7,5,7]],[[9,0,2,3],[10,0,2,3],[7,3,5,7],[7,4,0,5]]],'expected':[2,3,1,1]},
    {'args':[[[0,10,0,10],[3,4,3,4],[10,12,10,12]],[[12,0,4,10],[12,4,4,10],[12,10,4,10]]],'expected':[2,1,1]},
    {'args':[[[10**12-2,10**12,10**12-2,10**12]],[[10**12,10**12-2,0,10**12-2],[10**12,10**12-1,0,1]]],'expected':[1,0]},
    {'args':[[[i,i+2,i,i+3] for i in range(3000)],
             [[i+3,max(0,i-100),i+1,i+2] for i in range(2000)]],
     'expected':[min(i,100) for i in range(2000)]},
]
