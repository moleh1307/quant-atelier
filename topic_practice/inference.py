"""Inference practice: name the procedure before assigning its probability.

Exact coding cases are checked by independent record enumeration and backward
conditional-probability recursions in tests/test_inference_practice.py.
"""


def add_questions(add, questions):
    rubrics = {
        'q22': ['Give valid success counts and nonzero denominators with treatment ahead in both groups.',
                'Compute the pooled reversal and identify the different population weights.',
                'Explain why adjustment needs a causal argument, including collider and unmeasured-confounding risks.'],
        'q26': ['Define the p-value under a specified null, statistic and extremeness rule.',
                'Distinguish the probability of extreme data under the null from a posterior hypothesis probability.',
                'Identify prior model probabilities and alternative likelihoods, and explain why a large p-value need not establish equivalence.'],
        'q47': ['Identify the union of rejection events induced by repeated inspection and data-dependent stopping.',
                'Give a precommitted fixed-sample procedure and a justified sequential alternative without assuming independent looks.',
                'Explain why optional-stopping identities need conditions and why appropriately calibrated stopping can be valid.'],
    }
    for q in questions:
        if q['id'] in rubrics:
            q['rubric'] = rubrics[q['id']]

    def question(suffix, title, level, minutes, prompt, answer, hints, solution, follow, follow_solution, rubric):
        add(f'q_l12_{suffix}', title, 'Inference', level, 'researcher', minutes,
            prompt, answer, hints, solution, follow, follow_solution, 'l12')
        questions[-1]['rubric'] = rubric
        for key in ('prompt','solution','followSolution'):
            questions[-1][key] = questions[-1][key].replace(r'\n\n','\n\n')

    question('e1', 'An exact count is not its tail', 'Easy', 6,
        r'Before observing data, you specify SIX independent coin flips, null head probability 1/2, and a one-sided alternative favoring MORE heads. You observe five heads. The test statistic K is the total head count. What is the one-sided p-value \(P_{H_0}(K\geq5)\)? Do not change the endpoint or choose the direction after observing the flips.', 7/64,
        ['Under the null each six-flip ordered record has probability 1/64.', 'Include both five and six heads, not only the exact observed count.'],
        r'There are six ordered records with five heads and one with six, so the tail probability is (6+1)/64=7/64≈0.109375. The exact-count probability 6/64 omits a still more extreme outcome. This probability describes the specified statistic under the fair-coin model; it is not the probability the coin is fair after observing the record.',
        r'Using this pre-specified p-value, reject when p≤0.05. Which head counts reject? What is the ACTUAL type-I error, and what is the power if the true iid head probability is 3/4?',
        r'Five heads has p>0.05, while six has p=1/64≤0.05. Thus rejection is exactly K=6, with actual null error 1/64≈1.56%, not exactly 5%. Under head probability 3/4 its power is \((3/4)^6=729/4096\), about 17.8%. The discrete test conserves more error budget than its nominal upper bound and has modest power against this alternative. A nonrejection does not establish fairness.',
        ['Count the complete upper tail and obtain 7/64.', 'Identify the six-head rejection region and its actual null size 1/64.', 'Compute alternative power and distinguish null error, posterior probability and lack of detection.'])

    question('e2', 'An interval is a set of unrejected means', 'Easy', 6,
        r'You observe a sample mean 1.5 from n=36 iid Gaussian observations with unknown mean µ and KNOWN standard deviation σ=6. The sample size is fixed in advance. For a candidate mean m, the pre-specified two-sided test does NOT reject when \(|\sqrt n(\bar X-m)/\sigma|\leq2\), including equality. What is the largest candidate mean not rejected by this rule? The cutoff two is given; do not relabel its coverage as exactly 95%.', 3.5,
        ['The standard error of the sample mean is σ/√n.', 'Invert the same inequality with respect to the candidate mean.'],
        r'The standard error is 6/6=1, so nonrejection means |1.5−m|≤2. Its closed set is [−0.5,3.5], with largest candidate 3.5. Before sampling, this interval procedure has exact coverage \(P(|Z|\leq2)=2\Phi(2)-1\), about 95.45%, where Z is standard normal and Φ is its CDF. A quantile chosen for exactly 95% coverage would be slightly smaller than two. Inverting the specified test preserves its actual boundary and probability convention.',
        r'Keeping known σ and the cutoff fixed, how large must n be to halve the interval width? After seeing one interval, does its frequentist coverage assign that probability to this fixed µ?',
        r'Width is \(4\sigma/\sqrt n\), so n must quadruple from 36 to 144 to halve it. Coverage describes the random interval across repetitions with fixed µ, not a posterior probability for µ after seeing its endpoints. Under the given normal model a larger n narrows the interval while retaining the same pivot coverage. Unknown σ or dependent observations would require a different justification, rather than substituting them silently.',
        ['Use standard error one and correctly invert the inclusive test.', 'Give the interval [−0.5,3.5] and its actual pivot coverage.', 'Derive n=144 for half width and distinguish repeated-sample coverage from a posterior claim.'])

    question('m1', 'Spend a discrete error budget without rounding', 'Medium', 16,
        r'In SIX independent flips, test null head probability 1/2 against the specified simple alternative 3/4. You want null rejection probability EXACTLY α=1/20. Use the following pre-specified randomized rule: reject at K=6; at K=5 reject if an independent U∼Uniform(0,1) is at most γ; never reject for K≤4. Choose γ∈[0,1] and calculate the rule’s power at head probability 3/4. Explain why this extra randomization differs from deciding a test after seeing favorable data.', None,
        ['The six-head null mass is 1/64 and the five-head null mass is 6/64.', 'Set the weighted rejection mass equal to 1/20.', 'Compute the five-head and six-head masses again under the alternative.'],
        r'Exact size requires \((1+6\gamma)/64=1/20\), hence γ=11/30. An independent, pre-specified random draw spends only the missing part of the boundary mass. Under probability 3/4 the masses at six and five heads are respectively 729/4096 and 1458/4096. Therefore power is\n\n\[\frac{729}{4096}+\frac{11}{30}\frac{1458}{4096}=\frac{3159}{10240}\approx0.3085.\]\n\nWithout boundary randomization, rejecting only at six had size 1/64 and power 729/4096. The new rule is calibrated over both the sampling and the independent randomization. It does not use the outcome to invent a direction, endpoint or significance threshold. Its exact 5% error remains a null-model repeated-procedure statement, not a posterior probability.',
        r'For this simple null/alternative, explain why an upper-tail rule with at most one randomized boundary maximizes power among rules of the same null size. Would choosing U after looking at the record retain the argument?',
        r'Every ordered six-flip record with k heads has likelihood ratio \((3/2)^k(1/2)^{6-k}\), increasing by a factor three per added head. For fixed null rejection mass, moving a small amount of rejection probability from a lower-ratio record to a higher-ratio record strictly increases alternative rejection probability. Filling highest ratios first therefore yields the six-head region and just enough of the tied five-head region; additional randomization among equal-ratio records does not change power. This exchange argument uses fully specified models and pre-specified rejection probabilities. Picking a favorable U after observing the record changes those probabilities and need not preserve size.',
        ['Solve for γ=11/30 using both null masses.', 'Compute power 3159/10240 from the alternative masses and the independent randomized boundary.', 'Justify upper-tail optimality by increasing likelihood ratios and a fixed-size exchange argument.', 'Keep randomization independent and pre-specified, rather than treating a data-chosen rule as the calibrated one.'])

    question('h1', 'Evidence can survive every inspection', 'Hard', 30,
        r'Under H₀, coin flips are iid with head probability 1/2. Let Hₜ count heads after t flips and define \(M_t=3^{H_t}/2^t\), with M₀=1. This is the likelihood ratio for a FIXED iid alternative with head probability 3/4. A researcher may inspect after every flip and rejects at the first t with Mₜ≥20.\n\nProve that the probability of EVER rejecting under H₀ is at most 1/20. Establish the conditional expectation property, prove a bound for a finite horizon N using a bounded stopped process, then justify passage to an unlimited horizon. Do not assert an unbounded optional-stopping equality without conditions.', None,
        ['A head multiplies M by 3/2 and a tail multiplies it by 1/2.', 'Stop at the first crossing or at a fixed finite horizon, whichever comes first.', 'A nonnegative stopped value contributes at least twenty on the crossing event; then increase the horizon.'],
        r'Given the history through t, the next multiplier has null mean \((3/2+1/2)/2=1\). Thus M is a nonnegative martingale with finite values at each fixed time and E₀[Mₜ]=1. Let τ be its first threshold crossing, with τ=∞ if none. For T=τ∧N, write\n\n\[M_T=M_0+\sum_{t=1}^{N}\mathbf1\{\tau\geq t\}(M_t-M_{t-1}).\]\n\nThe indicator is determined before flip t. Its product with the martingale increment has expectation zero; the finite sum is integrable. Therefore E₀[M_T]=1. On {τ≤N}, M_T≥20; off that event it remains nonnegative. Hence \(1\geq20P_0(\tau\leq N)\). The crossing events increase with N, so probability continuity gives \(P_0(\tau<\infty)\leq1/20\). No claim that E₀[Mτ]=1 at an unbounded stopping time was needed. Inspection is allowed because THIS process and boundary control the whole crossing event, not because repeated ordinary p-values are automatically calibrated.',
        r'Does the same fixed process control error if the null merely requires the next head probability, conditional on the past, to be at most 1/2? Separately, under the fair null, what if at each flip you choose an alternative probability qₜ and use multiplier 2qₜ on a head or 2(1−qₜ) on a tail? Contrast choosing qₜ using PAST flips with choosing qₜ after seeing the CURRENT flip.',
        r'If the conditional head probability pₜ≤1/2, the fixed multiplier has conditional mean 1/2+pₜ≤1. M is then a nonnegative supermartingale. The same finite stopped-increment argument gives E[M_T]≤1 and the same ever-crossing bound without iid flips.\n\nUnder the fair null, a qₜ∈[0,1] determined from past flips still has conditional multiplier mean qₜ+(1−qₜ)=1; the betting rule may adapt predictably. Choosing qₜ from the current outcome breaks that property. If qₜ=1 after a head and zero after a tail, the selected multiplier is ALWAYS two. The process becomes 2ᵗ and crosses twenty after five flips with null probability one. A fitted alternative chosen using the same observation is not automatically a valid evidence increment. Independence of future flips or the stated conditional-null restriction, the information available before each multiplier, and nonnegativity are substantive assumptions.',
        ['Establish the conditional martingale property for the fixed likelihood ratio.', 'Prove the finite-horizon bound from predictable stopped increments and nonnegativity.', 'Pass to an unlimited horizon through increasing crossing events, without an unjustified expectation identity.', 'Handle the conditional composite null and distinguish predictable adaptation from the current-flip counterexample.'])

    question('h2', 'A significance filter changes interval coverage', 'Hard', 30,
        r'One observation X has distribution N(µ,1), where µ is a fixed unknown real number. Write Φ for the standard-normal CDF, α=0.05, and c=Φ⁻¹(1−α/2). The ordinary interval I(X)=[X−c,X+c] has unconditional coverage 1−α. You REPORT it only when the pre-specified positive-significance filter S={X>c} passes.\n\nDerive \(P_\mu(\mu\in I(X)\mid S)\) as an explicit piecewise function of µ, including µ≤0, 0<µ<2c and µ≥2c. Explain the zero-mean case and why the original unconditional guarantee is not a conditional guarantee for reported intervals. Do not turn selection into a prior probability for µ.', None,
        ['Coverage requires µ−c≤X≤µ+c; intersect this event with X>c.', 'Under fixed µ, standardize the intersection endpoints and divide by the probability of selection.', 'Check whether the upper coverage endpoint reaches the selection threshold before applying a CDF difference.'],
        r'Selection has probability 1−Φ(c−µ)>0 for every finite µ. The intersection is empty if µ≤0, because every reported interval has strictly positive lower endpoint. For µ>0 its lower observation endpoint is max(c,µ−c) and its upper endpoint is µ+c. Standardizing gives upper endpoint c and lower endpoint max(c−µ,−c). Consequently\n\n\[C(\mu)=\begin{cases}0,&\mu\leq0,\\\displaystyle\frac{\Phi(c)-\Phi(c-\mu)}{1-\Phi(c-\mu)},&0<\mu<2c,\\\displaystyle\frac{1-\alpha}{1-\Phi(c-\mu)},&\mu\geq2c.\end{cases}\]\n\nAt µ=0, NONE of the reported intervals contains zero, although 95% of intervals over all samples do. At µ=c the conditional coverage is 1−α; at µ=2c it is \((1-\alpha)/(1-\alpha/2)=38/39\), about 97.44%, and it approaches 95% as µ tends to positive infinity. Conditioning changes the sample distribution and can decrease or increase coverage. The reported subset is not a repeated unselected sample from the original normal law.',
        r'Give two ways to restore 95% coverage CONDITIONAL on reporting: first using an independent replication Y∼N(µ,1), and second by inverting a conditional pivot from the selected X itself. Derive the pivot and its coverage argument, rather than merely saying “adjust for selection.”',
        r'If Y is independent of X at every fixed µ, report [Y−c,Y+c] when X>c. Its coverage event is independent of the selection event, so its conditional coverage remains 95%; the same X cannot play the independent-replication role.\n\nAlternatively, for x>c define the truncated-normal CDF\n\n\[F_\mu^S(x)=\frac{\Phi(x-\mu)-\Phi(c-\mu)}{1-\Phi(c-\mu)}.\]\n\nConditional on S, the continuous probability-integral transform makes Fµˢ(X) uniform on (0,1) for each fixed µ. The confidence SET \(\{m:\alpha/2\leq F_m^S(x)\leq1-\alpha/2\}\) therefore covers the true µ with conditional probability 1−α. This inversion uses the actual selection rule and its truncated sampling law, not a posterior distribution. Its endpoints generally differ from x±c and can be very wide near the selection threshold. A more complex data-dependent reporting rule would require conditioning on that actual rule, not importing this particular formula.',
        ['Intersect the coverage and reporting events before standardizing.', 'Derive all three coverage branches and the zero-mean failure, including boundary consistency.', 'Separate unconditional coverage, conditional selected-sample coverage and a posterior interpretation.', 'Justify independent replication and the truncated-CDF confidence-set inversion with its conditional uniform pivot.'])


def add_coding(add, tasks):
    def exercise(level, title, prompt, signature, samples, tests, solution, explanation):
        add(f'c_l12_{level.lower()}', title, level, 'Inference', prompt, signature,
            samples, tests, solution, explanation)
        tasks[-1]['path']='researcher'
        for key in ('prompt','explanation'):
            tasks[-1][key]=tasks[-1][key].replace(r'\n\n','\n\n')

    exercise('Easy','Invert a known-variance test exactly',
        r'An iid Gaussian sample has a FIXED size n≥1, unknown mean and KNOWN positive variance sigma_squared. sample_sum is its observed sum. For each integer candidate mean m in means, return whether the pre-specified symmetric test does NOT reject: \((\bar X-m)^2/(\sigma^2/n)\leq\text{critical\_squared}\), including equality. Return booleans in original order; repeated candidates remain repeated. This inverts the stated test, rather than assigning a posterior probability or assuming its supplied cutoff means exactly 95% coverage.\n\nAll inputs are integers. 1≤n≤10^9, 1≤sigma_squared≤10^18, 0≤critical_squared≤10^6, |sample_sum|≤10^18, and means has at most 100000 entries with |m|≤10^9. Use O(len(means)) exact integer comparisons and O(1) integer accumulators beyond the returned list. Do not mutate means, round the sample mean, take square roots or use a floating tolerance. Integer bit costs are additional.',
        'def solve(sample_sum, n, sigma_squared, critical_squared, means):',
        [{'args':[54,36,36,4,[-1,0,1,3,4]],'expected':[False,True,True,True,False]},
         {'args':[0,9,36,4,[-4,4,5]],'expected':[True,True,False]}],
        [{'args':[1,2,1,0,[0,1]],'expected':[False,False]},
         {'args':[6,3,7,0,[2,2,1]],'expected':[True,True,False]},
         {'args':[0,1,1,1,[-2,-1,0,1,2]],'expected':[False,True,True,True,False]},
         {'args':[-54,36,36,4,[-4,-3,-1,0,1]],'expected':[False,True,True,True,False]},
         {'args':[999999999,1,999999998000000000,1,[0]],'expected':[False]},
         {'args':[10**18,10**9,1,1,[10**9,10**9-1]],'expected':[True,False]},
         {'args':[0,1,1,4,[]],'expected':[]},
         {'args':[0,1,1,1,[1,-1,2]*3000],'expected':[True,True,False]*3000}],
        '''def solve(sample_sum, n, sigma_squared, critical_squared, means):
    bound = critical_squared * n * sigma_squared
    return [(sample_sum - n * m) ** 2 <= bound for m in means]''',
        r'Write \(\bar X=\text{sample\_sum}/n\). Multiplying the nonrejection inequality by the positive n² gives \((\text{sample\_sum}-nm)^2\leq\text{critical\_squared}\,n\sigma^2\). Compare these integers directly for every candidate. Squaring is legitimate because the given statistic is two-sided; equality is retained. Even a zero cutoff or a mean that is not an integer needs no special approximation. The normal known-variance assumptions justify the statistical procedure, while this function performs its exact algebraic inversion. A floating conversion near a huge boundary can lose a difference of one and misclassify a candidate.')

    exercise('Medium','Compute fixed-endpoint size and power',
        r'A pre-specified experiment flips an iid coin EXACTLY n times and rejects when its total heads K≥threshold. Under H₀ the head probability is 1/2; under the specified alternative it is head_numerator/head_denominator. Compute the ACTUAL null rejection probability (size) and alternative rejection probability (power). No early inspection, boundary randomization or data-chosen direction is part of this rule.\n\nInputs are integers: 0≤n≤200, 0≤threshold≤n+1, 1≤head_denominator≤1000 and 0≤head_numerator≤head_denominator. Fractions need not be supplied reduced. At n=0 the only count is zero; threshold zero rejects and threshold one never rejects. Return {"size":[numerator_text,denominator_text],"power":[numerator_text,denominator_text]} with exact reduced rational pairs of canonical decimal STRINGS, nonnegative numerators, positive denominators and zero ["0","1"]. Do not return floats or numeric pairs.\n\nUse O(n) scalar recurrence iterations and a constant number of integer accumulators, with initial integer exponentiation and integer/gcd bit costs additional. Enumerating 2^n ordered records is too slow. No external probability package is needed.',
        'def solve(n, threshold, head_numerator, head_denominator):',
        [{'args':[6,6,3,4],'expected':{'size':['1','64'],'power':['729','4096']}},
         {'args':[6,5,3,4],'expected':{'size':['7','64'],'power':['2187','4096']}}],
        FIXED_CASES,
        '''from math import gcd
def solve(n, threshold, head_numerator, head_denominator):
    a = head_numerator
    b = head_denominator - a
    coefficient = 1
    weight = b ** n
    size_mass = 0
    power_mass = 0
    for k in range(n + 1):
        if k >= threshold:
            size_mass += coefficient
            power_mass += coefficient * weight
        if k < n:
            coefficient = coefficient * (n - k) // (k + 1)
            if b:
                weight = weight * a // b
    if b == 0:
        power_mass = head_denominator ** n if n >= threshold else 0
    def pair(numerator, denominator):
        divisor = gcd(numerator, denominator)
        return [str(numerator // divisor), str(denominator // divisor)]
    return {"size": pair(size_mass, 2 ** n), "power": pair(power_mass, head_denominator ** n)}''',
        r'The null tail is \(\sum_{k\geq h}\binom nk/2^n\); the alternative tail is \(\sum_{k\geq h}\binom nk a^k(d-a)^{n-k}/d^n\). Generate binomial coefficients by \(\binom n{k+1}=\binom nk(n-k)/(k+1)\). When b=d−a>0, start the alternative weight at bⁿ and update w←wa/b before the next count; the division is exact because the current weight contains a remaining b factor. At a=0 it correctly becomes zero after count zero. At b=0 only K=n has positive mass, so handle that deterministic alternative directly; n=0 still has mass one at K=0. Sum only counts at or above the inclusive threshold, reduce each rational by gcd and encode its integers as strings. A nominal significance label does not determine these actual probabilities. This task calibrates one fixed endpoint, not the union over repeated looks; the Hard task counts that different event.')

    exercise('Hard','Calibrate dependent inspections and stopping cost',
        r'The maximum experiment length horizon is an integer 0≤horizon≤120. The pre-specified looks list contains [time,head_threshold] pairs at STRICTLY increasing distinct times 1…horizon, with 0≤head_threshold≤time+1. Heads count CUMULATIVELY from the first flip. At a listed time, reject and STOP if the cumulative count is at least its threshold, including equality. Otherwise continue. There is no early acceptance; if no rejection occurs, take all horizon flips. Empty looks means no rejection, and horizon zero requires empty looks and takes zero flips.\n\nUnder H₀ flips are iid Bernoulli(1/2); under the specified alternative they are iid Bernoulli(head_numerator/head_denominator), with integer denominator 1…1000 and numerator 0…denominator. Calculate the probability of EVER rejecting by the horizon under each model, and the expected number of flips ACTUALLY TAKEN under each. Looks share observations and are not independent. Thresholds are supplied, not chosen by this function. Finite-horizon calibration alone does not establish unlimited-horizon validity.\n\nReturn a dictionary with keys "size", "power", "null_flips", "alternative_flips". Each value is an exact reduced rational pair of canonical decimal STRINGS [numerator_text,denominator_text], with nonnegative numerator, positive denominator and zero ["0","1"]. No floats, numeric pairs, simulation, mutation of looks or enumeration of all binary records. Use O(horizon²+len(looks)) scalar iterations and O(horizon) integer slots beyond outputs; integer power/gcd/bit costs are additional. Track which prefixes have NOT already rejected, then remove first-crossing paths before propagating them.',
        'def solve(horizon, looks, head_numerator, head_denominator):',
        [{'args':[3,[[1,1],[3,2]],3,4], 'expected':{'size':['5','8'],'power':['57','64'],'null_flips':['2','1'],'alternative_flips':['3','2']}},
         {'args':[4,[[2,2],[4,3]],1,2], 'expected':{'size':['3','8'],'power':['3','8'],'null_flips':['7','2'],'alternative_flips':['7','2']}}],
        SEQUENTIAL_CASES,
        '''from math import gcd
def solve(horizon, looks, head_numerator, head_denominator):
    n = horizon
    a, d = head_numerator, head_denominator
    b = d - a
    bounds = dict(looks)
    a_powers, b_powers, d_powers, two_powers = [1], [1], [1], [1]
    for _ in range(n):
        a_powers.append(a_powers[-1] * a)
        b_powers.append(b_powers[-1] * b)
        d_powers.append(d_powers[-1] * d)
        two_powers.append(two_powers[-1] * 2)
    alive = [1]
    size_mass = power_mass = null_cost = alternative_cost = 0
    for t in range(1, n + 1):
        null_cost += sum(alive) * two_powers[n - t + 1]
        alternative_cost += sum(count * a_powers[k] * b_powers[t - 1 - k] for k, count in enumerate(alive)) * d_powers[n - t + 1]
        next_alive = [0] * (t + 1)
        for k, count in enumerate(alive):
            next_alive[k] += count
            next_alive[k + 1] += count
        if t in bounds:
            for k in range(bounds[t], t + 1):
                count = next_alive[k]
                size_mass += count * two_powers[n - t]
                power_mass += count * a_powers[k] * b_powers[t - k] * d_powers[n - t]
                next_alive[k] = 0
        alive = next_alive
    def pair(numerator, denominator):
        divisor = gcd(numerator, denominator)
        return [str(numerator // divisor), str(denominator // divisor)]
    return {"size": pair(size_mass, two_powers[n]),
            "power": pair(power_mass, d_powers[n]),
            "null_flips": pair(null_cost, two_powers[n]),
            "alternative_flips": pair(alternative_cost, d_powers[n])}''',
        r'Let alive[k] count length-(t−1) ordered prefixes with k heads that did NOT reject at an earlier look. Each extends once by a tail to k and once by a head to k+1. At a scheduled time t, any resulting count at or above the threshold is a FIRST rejection; record its probability and zero it before the next extension. Do not propagate stopped paths and count them twice. Paths with the same cumulative count have the same probability under either iid model, so these counts are sufficient.\n\nFor null probability, a length-t rejected prefix has mass count/2ᵗ. Put every contribution over the common denominator 2ᴺ by multiplying its numerator by 2ᴺ⁻ᵗ. Under alternative a/d, the prefix mass is count·aᵏ(d−a)ᵗ⁻ᵏ/dᵗ; multiply its numerator by dᴺ⁻ᵗ to use denominator dᴺ. Summing these disjoint FIRST-hit masses gives size and power, with no independence assumption between looks. A threshold t+1 never rejects; zero rejects all still-alive paths at that time.\n\nFor stopping time T≤N, \(E[T]=\sum_{t=1}^N P(T\geq t)\). Before taking flip t, this event is exactly survival through t−1, whose null probability is Σalive/2ᵗ⁻¹ and whose alternative probability weights each alive count by aᵏ(d−a)ᵗ⁻¹⁻ᵏ/dᵗ⁻¹. Accumulate them over the same final denominators. Nonrejecting paths contribute every flip through N, so no terminal-cost correction is needed. Precompute integer powers once; all zero-probability branches work using the empty-product convention 0⁰=1. At N=0 rejection masses and costs are zero. Reduce all four rationals by gcd and preserve their digits as strings. State propagation and probability weighting each cost O(t) per step, giving O(N²+len(looks)) scalar work and O(N) integer slots, plus integer bit/power/gcd costs. This computes the actual supplied finite procedure; it does not itself choose calibrated boundaries or certify an infinite continuation.')


# Filled from independent, backward per-model probability recursions. The judge
# never imports an oracle or generates expectations from its own reference.
FIXED_CASES = [{'args': [0, 0, 0, 1], 'expected': {'size': ['1', '1'], 'power': ['1', '1']}},
 {'args': [0, 1, 1, 1], 'expected': {'size': ['0', '1'], 'power': ['0', '1']}},
 {'args': [10, 9, 3, 4], 'expected': {'size': ['11', '1024'], 'power': ['255879', '1048576']}},
 {'args': [10, 8, 1, 2], 'expected': {'size': ['7', '128'], 'power': ['7', '128']}},
 {'args': [8, 0, 0, 1], 'expected': {'size': ['1', '1'], 'power': ['1', '1']}},
 {'args': [8, 9, 1, 1], 'expected': {'size': ['0', '1'], 'power': ['0', '1']}},
 {'args': [8, 8, 0, 7], 'expected': {'size': ['1', '256'], 'power': ['0', '1']}},
 {'args': [8, 8, 7, 7], 'expected': {'size': ['1', '256'], 'power': ['1', '1']}},
 {'args': [15, 9, 2, 3], 'expected': {'size': ['9949', '32768'], 'power': ['3811840', '4782969']}},
 {'args': [200, 101, 499, 1000],
  'expected': {'size': ['189548691200360874297069739407959804830962300513422437307507',
                        '401734511064747568885490523085290650630550748445698208825344'],
               'power': ['23028440979156719540543655158062253166082416860236697787554036488332602239099710162679938791515010331840807848483876666719599802262267541039259937559996680349264236250816991936210763196521296954550834549425105180939691233448081550177921516648683551745833640041937041074246364404171862456299325834913150183763763848301869666978920610796147729075828643895604415648534381119048237333481519060955286896626198158819846517446773782612588904855095430854830448258740251124630276157894399890927465081809421001002259026127470615980332595562688427052381507745406488179642450424021736476829853858434195728278967',
                         '50000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000']}},
 {'args': [200, 200, 999, 1000],
  'expected': {'size': ['1', '1606938044258990275541962092341162602522202993782792835301376'],
               'power': ['818648829478635705560211139729092492748543016933095988331750309567939720597347950131449769386118290690398972362777140586627045268358067913327287004659860712040208485760395679903843643263315476822009524287814225027584835520035815718019020093247635570778315907835315729212962043159010930377934201059539867774420064168453113217755712476789532573499929321748369210473511458803022333652582472226426698748941165454588125328897377776992370655564914900035002882900805821235886295683753540930078602333104573916413123674701175773764378534564749980485551080892809073856476907658211563416490714643636619899800001',
                         '1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000']}}]
SEQUENTIAL_CASES = [{'args': [0, [], 1, 2],
  'expected': {'size': ['0', '1'],
               'power': ['0', '1'],
               'null_flips': ['0', '1'],
               'alternative_flips': ['0', '1']}},
 {'args': [1, [], 0, 1],
  'expected': {'size': ['0', '1'],
               'power': ['0', '1'],
               'null_flips': ['1', '1'],
               'alternative_flips': ['1', '1']}},
 {'args': [5, [], 1, 1],
  'expected': {'size': ['0', '1'],
               'power': ['0', '1'],
               'null_flips': ['5', '1'],
               'alternative_flips': ['5', '1']}},
 {'args': [2, [[1, 1], [2, 2]], 1, 2],
  'expected': {'size': ['1', '2'],
               'power': ['1', '2'],
               'null_flips': ['3', '2'],
               'alternative_flips': ['3', '2']}},
 {'args': [6, [[3, 3], [6, 5]], 3, 4],
  'expected': {'size': ['11', '64'],
               'power': ['2457', '4096'],
               'null_flips': ['45', '8'],
               'alternative_flips': ['303', '64']}},
 {'args': [5, [[2, 0], [5, 5]], 1, 3],
  'expected': {'size': ['1', '1'],
               'power': ['1', '1'],
               'null_flips': ['2', '1'],
               'alternative_flips': ['2', '1']}},
 {'args': [4, [[1, 2], [2, 3], [4, 5]], 1, 1],
  'expected': {'size': ['0', '1'],
               'power': ['0', '1'],
               'null_flips': ['4', '1'],
               'alternative_flips': ['4', '1']}},
 {'args': [6, [[1, 1], [3, 2], [6, 4]], 0, 1],
  'expected': {'size': ['21', '32'],
               'power': ['0', '1'],
               'null_flips': ['25', '8'],
               'alternative_flips': ['6', '1']}},
 {'args': [6, [[1, 1], [3, 2], [6, 4]], 1, 1],
  'expected': {'size': ['21', '32'],
               'power': ['1', '1'],
               'null_flips': ['25', '8'],
               'alternative_flips': ['1', '1']}},
 {'args': [10, [[2, 2], [5, 4], [10, 8]], 2, 3],
  'expected': {'size': ['327', '1024'],
               'power': ['35812', '59049'],
               'null_flips': ['123', '16'],
               'alternative_flips': ['1406', '243']}},
 {'args': [120,
           [[5, 5],
            [10, 8],
            [15, 10],
            [20, 13],
            [25, 15],
            [30, 18],
            [35, 20],
            [40, 23],
            [45, 25],
            [50, 28],
            [55, 30],
            [60, 33],
            [65, 35],
            [70, 38],
            [75, 40],
            [80, 43],
            [85, 45],
            [90, 48],
            [95, 50],
            [100, 53],
            [105, 55],
            [110, 58],
            [115, 60],
            [120, 63]],
           501,
           1000],
  'expected': {'size': ['49805580908466585595052884424964185', '83076749736557242056487941267521536'],
               'power': ['7580150221057389472774756880076082204099823852471324261649638242466109485496778648018860641501752742490922701034801878716880321402157869212423701681933106149239343498916619939059616466337048334066609200507963377229003706550378251113534414061563886290633005776234305320146383418524531367709360954445887611747310151057545270835962203224589848744629422052933497',
                         '12500000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'],
               'null_flips': ['1510259502812555081378095906796414985', '20769187434139310514121985316880384'],
               'alternative_flips': ['451077440308293179925045949578189659440353777249199955734447671874790016361362730638964327392880456155440357628649543516212948329340983725656263835380562810820185951056060860844534494006700145777004566646767986088513530642920054760110900572846998953685153258120790374462188645066020792438583250722459305656996705822373498209108163404547474043113',
                                     '6250000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000']}}]
