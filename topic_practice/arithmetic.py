"""l06: choose a representation, retain exactness, know what rounding loses."""


def add_questions(add, questions):
    def question(suffix, title, level, minutes, prompt, answer, hints,
                 solution, follow, follow_answer, rubric):
        add(f'q_l06_{suffix}', title, 'Arithmetic', level, 'shared',
            minutes, prompt, answer, hints, solution, follow, follow_answer, 'l06')
        questions[-1]['rubric'] = rubric

    question('e1', 'Unequal offsets need a cross term', 'Easy', 3,
        r'Calculate \(98\times107\) exactly without a calculator. Explain a short decomposition and one independent check; the offsets from 100 are not equal.',
        10486,
        ['Compensate from 100 groups of 107, or expand both offsets about 100.',
         'A change of two in the first factor changes the product by two whole groups of 107.'],
        r'One route is \((100-2)107=10700-214=10486\). Another is \((100-2)(100+7)=10000+100(7-2)-14\), with the cross term -14 retained. The difference-of-squares shortcut does not apply to unequal offsets. A magnitude check puts the answer below 10700, and the final digit must be 6 because 8 times 7 ends in 6. Those checks catch different errors but do not independently prove every digit.',
        r'What makes \(98\times102\) different, and how would you compute it?',
        r'The offsets now have equal magnitude and opposite signs, so the linear terms cancel: \((100-2)(100+2)=10000-4=9996\). The same identity cannot be transferred to 107 without changing its correction.',
        ['Use an equivalent decomposition and obtain 10486.',
         'Explain the unit and sign of the correction.',
         'Give a distinct magnitude or final-digit check.'])

    question('e2', 'Scale the whole quotient', 'Easy', 3,
        r'Calculate \(3.6/0.045\) exactly without a calculator. Explain which quantities you scale, and why the answer should be larger than 3.6.',
        80,
        ['Multiplying numerator and denominator by 1000 leaves the quotient unchanged.',
         'Reduce 3600/45 using an easy multiple of 45.'],
        r'Equivalent scaling gives \(3.6/0.045=3600/45=80\). Scaling the denominator alone would instead give \(3.6/45=0.08\), changing the quotient by a factor of 1000. Dividing a positive number by a positive number smaller than one increases it. Reverse multiplication provides another check: \(0.045(80)=3.6\).',
        r'If 0.045 was itself a rounded measurement rather than an exact divisor, is 80 still an exact answer?',
        r'It is the exact quotient of the displayed numbers, but need not be the quotient of the underlying measurements. The uncertainty of the divisor must be specified before claiming exactness for the original quantity. Algebraic precision cannot recover information discarded by measurement or rounding.',
        ['Scale both numerator and denominator equally.',
         'Obtain 80 and verify by multiplication.',
         'Distinguish an exact displayed quotient from an uncertain underlying measurement.'])

    question('m1', 'Recovering from a loss uses a new base', 'Medium', 6,
        r'A positive quantity falls by 30% and then rises by a proportional rate r relative to its reduced value. What r restores the original value? Return r as a fraction or decimal proportion: for example 20% would be entered as 1/5, not 20. Explain why adding back 30% is insufficient.',
        3/7,
        ['Write the two changes as multipliers applied to an arbitrary initial value.',
         'The recovery gain is measured against 70% of the original base.'],
        r'If the original value is B>0, restoration requires \(0.7B(1+r)=B\). Therefore \(r=1/0.7-1=3/7\), about 42.857%. A 30% increase after the loss produces \(0.7(1.3)B=0.91B\). Both rates are called 30%, but their absolute changes use different bases. Keeping r as a fraction avoids turning an exact recovery rate into a premature decimal approximation.',
        'For a loss proportion d with 0<=d<=1, derive the recovery rate and identify the boundary at which recovery by a finite proportional increase becomes impossible.',
        r'For \(0\leq d<1\), \((1-d)(1+r)=1\) gives \(r=d/(1-d)\). At d=1 the quantity has become zero. Multiplying zero by any finite growth factor cannot restore a positive original value. The divergence as d approaches one reflects a changing base, not a numerical accident.',
        ['Write (1−0.3)(1+r)=1 with the correct recovery base.',
         'Obtain 3/7 and distinguish proportion from percentage notation.',
         'Explain the 100% loss boundary and the failure of additive rates.'])

    question('m2', 'Equal percentage moves need not cancel', 'Medium', 7,
        r'One fixed group contains 40 units priced at 125 each; a second contains 60 units priced at 80 each. The first price rises by 10% and the second falls by 10%. Unit counts stay fixed. What is the proportional change in their combined value? Return a fraction or decimal proportion, and identify the base used for each change.',
        1/490,
        ['Calculate each group\'s initial value before weighting its percentage move.',
         'Add the absolute value changes, then divide by the original combined value.'],
        r'The two starting values are \(40(125)=5000\) and \(60(80)=4800\). Their changes are +500 and -480, so the total change is +20 on a base of 9800. The proportional change is \(20/9800=1/490\), about 0.20408%. Equal percentage magnitudes cancel only when applied to equal value bases. Weighting by unit counts alone would ignore the different prices; averaging +10% and -10% would ignore both value bases.',
        'What decrease rate in the second group would exactly offset the first group\'s 10% increase?',
        r'The required absolute decrease is 500. Relative to the second group\'s starting value 4800, its decrease rate is \(500/4800=5/48\), about 10.4167%. Use the group whose price is being changed as the denominator, not the overall 9800.',
        ['Compute the value bases 5000 and 4800 rather than using unit counts as weights.',
         'Derive the net change +20 and proportional result 1/490.',
         'Explain why equal percentage moves do not cancel here.'])

    question('h1', 'Recover an exact fraction from a rounded report', 'Hard', 14,
        r'A number x in (0,1) is a reduced fraction a/b with positive integers a,b and b<=15. It is rounded to two decimal places using nearest rounding, with exact half ties rounded upward, and reported as 0.29. Determine x exactly and prove uniqueness under the denominator bound. The report is not a claim that x equals 29/100.',
        2/7,
        ['Translate the rounding rule into an exact half-open interval.',
         'Use x=a/b to bound the possible integer denominator for each small numerator.',
         'Fractions such as 4/14 are the same reduced candidate as 2/7.'],
        r'The report means \(57/200\leq a/b<59/200\). Since b<=15, the numerator satisfies \(a<(59/200)15<5\), so a is 1, 2, 3 or 4. For each a, the allowed denominator interval is \[\frac{200a}{59}<b\leq\frac{200a}{57}.\] For a=1 and a=3 it contains no integer; for a=2 it contains only b=7; for a=4 it contains only b=14. The latter fraction reduces to 2/7 and violates the assumption that a,b are already coprime. Thus the sole reduced fraction is \(x=2/7\), which does round to 0.29. The exact integer inequalities, including the excluded upper endpoint, establish uniqueness; numerical closeness alone does not.',
        'Does the same report identify x if the denominator bound is relaxed to 20?',
        r'No. In addition to 2/7, \(5/17\approx0.2941176\) lies in the interval and has a permitted reduced denominator. Adding a numerator bound or a rounding report is information; dropping it can destroy identifiability. Do not choose a favourite nearby fraction without justifying the candidate set.',
        ['Derive the interval [57/200,59/200) from the stated tie rule.',
         'Bound the numerator and inspect all permitted integer denominator intervals.',
         'Reduce duplicate representations and prove the unique candidate is 2/7.'])

    question('h2', 'Rounding can reverse a ranking', 'Hard', 18,
        r'Four positive numbers a,b,c,d are independently rounded as measurements, not sampled randomly. Nearest rounding to two decimal places with half ties upward reports a=0.50, b=0.25, c=0.51 and d=0.26. There are no other constraints on their true values. The displayed ratios satisfy 0.50/0.25 > 0.51/0.26. Is the true inequality a/b > c/d guaranteed? Derive tight possible intervals for both true ratios and, if needed, give explicit true values reversing the ranking. State whether the interval endpoints are attainable.',
        None,
        ['Each report defines a half-open interval of width 0.01.',
         'A positive ratio increases with its numerator and decreases with its denominator.',
         'Overlapping ratio bounds do not guarantee an ordering; construct a consistent reversal.'],
        r'The true intervals are \(a\in[0.495,0.505)\), \(b\in[0.245,0.255)\), \(c\in[0.505,0.515)\) and \(d\in[0.255,0.265)\). Monotonicity yields \[\frac{33}{17}<\frac ab<\frac{101}{49},\qquad\frac{101}{53}<\frac cd<\frac{103}{51}.\] The lower bound of each ratio needs the excluded upper denominator; the upper bound needs the excluded upper numerator. Neither endpoint is attained, but values can approach them arbitrarily closely, so the bounds are tight. A reversal is a=0.496, b=0.254, c=0.514, d=0.256, all consistent with the reports. Then \(a/b=248/127<257/128=c/d\), as exact cross multiplication confirms: 31744<32639. The measurements are unconstrained apart from their rounding intervals; the word independently here means the rounding acts on each separately, not a probabilistic independence assumption. Treating a two-decimal report as an exact input can give an unjustified ranking.',
        'A new, more precise measurement reports 0.500, 0.250, 0.510 and 0.260 using the same tie rule at three decimal places. Is the ranking now guaranteed? Why can you not reach that conclusion by simply adding zeros to the old reports?',
        r'The new intervals give \(a/b>0.4995/0.2505=333/167\) and \(c/d<0.5105/0.2595=1021/519\). The first lower bound exceeds the second upper bound: \(333(519)=172827>170507=1021(167)\). Thus the new information guarantees a/b>c/d. Printing an extra zero on an old two-decimal report does not narrow its original uncertainty interval; only the more precise measurement does.',
        ['Translate all reports into half-open intervals with correct endpoint rules.',
         'Derive tight ratio bounds and explain their unattained endpoints.',
         'Give a valid reversal and distinguish additional precision from cosmetic zeros.'])


def add_coding(add, tasks):
    def exercise(level, title, prompt, signature, samples, tests, solution, explanation):
        add(f'c_l06_{level.lower()}', title, level, 'Exact arithmetic', prompt,
            signature, samples, tests, solution, explanation)
        tasks[-1].update(path='shared', lesson='l06')

    exercise('Easy', 'Does this fraction have a finite decimal?',
        'numerator is an integer with absolute value <=10^12 and denominator is a positive integer <=10^12. Return the smallest number of digits after the decimal point needed to represent numerator/denominator exactly as a terminating decimal, or None if its decimal repeats forever. Return 0 for an integer, including zero. Reduce the fraction first; the written denominator alone does not determine termination. Do not use floating-point approximations or emit the decimal string.',
        'def solve(numerator, denominator):',
        [{'args': [15,24], 'expected': 3}, {'args': [1,6], 'expected': None}],
        [{'args': [0,999], 'expected': 0},
         {'args': [-3,8], 'expected': 3},
         {'args': [12,6], 'expected': 0},
         {'args': [6,15], 'expected': 1},
         {'args': [1,40], 'expected': 3},
         {'args': [1,125], 'expected': 3},
         {'args': [1,2**39], 'expected': 39},
         {'args': [7,28], 'expected': 2}],
        '''from math import gcd
def solve(numerator, denominator):
    denominator //= gcd(abs(numerator), denominator)
    twos = fives = 0
    while denominator % 2 == 0:
        denominator //= 2
        twos += 1
    while denominator % 5 == 0:
        denominator //= 5
        fives += 1
    if denominator != 1:
        return None
    return max(twos, fives)''',
        r'A reduced fraction terminates at d places exactly when its denominator divides \(10^d=2^d5^d\). It must therefore contain no prime factors other than two and five. If the reduced denominator is \(2^u5^v\), the least d is max(u,v). Cancellation can remove other factors: 6/15 reduces to 2/5. A zero numerator reduces the denominator to one and needs no fractional digits. Integer gcd and divisions retain exactness. O(log denominator) integer operations and O(1) additional storage under the stated integer bounds.')

    exercise('Medium', 'Compound percentage changes exactly',
        'changes is a list of at most 100 integer price changes in basis points, each from -10000 to 10000. One basis point is 1/100 of one percent, so 100 basis points is 1%. Starting from a positive value, apply each change to the current value. Return the exact NET proportional change as [numerator, denominator] in lowest terms, with denominator positive. For example +20% followed by -20% has net change -1/25. Return [0,1] for no changes. A -100% change makes the value zero; subsequent finite proportional changes keep it zero. Do not use floats, round intermediates, add the percentage changes or mutate changes. Exact integers and gcd are available.',
        'def solve(changes):',
        [{'args': [[2000,-2000]], 'expected': [-1,25]},
         {'args': [[1000,1000]], 'expected': [21,100]}],
        [{'args': [[]], 'expected': [0,1]},
         {'args': [[0,0]], 'expected': [0,1]},
         {'args': [[-10000,10000]], 'expected': [-1,1]},
         {'args': [[10000,-5000]], 'expected': [0,1]},
         {'args': [[1,1]], 'expected': [20001,100000000]},
         {'args': [[-2500,2000]], 'expected': [-1,10]},
         {'args': [[9999]*100], 'expected': [19999**100-10000**100,10000**100]}],
        '''from math import gcd
def solve(changes):
    numerator = denominator = 1
    for basis_points in changes:
        numerator *= 10000 + basis_points
        denominator *= 10000
        common = gcd(numerator, denominator)
        numerator //= common
        denominator //= common
    numerator -= denominator
    common = gcd(abs(numerator), denominator)
    return [numerator // common, denominator // common]''',
        r'Each step multiplies value by \((10000+b)/10000\). Multiply these rational factors while reducing numerator and denominator by their gcd. This models the changing percentage base exactly. Subtract one only at the end to turn the final value multiplier into the net change, then reduce again. A zero multiplier remains zero and gives net change -1. The empty product is one, giving zero net change. There are O(k) gcd/multiplication steps, but growing integers are not constant-cost: before reduction their bit lengths are O(k log 10000). Storage is proportional to those integer lengths. The large case rejects a float representation of an exact rational, not just an inaccurate decimal rounding.')

    scale = 10**100
    exercise('Hard', 'The simplest fraction a rounded report permits',
        r'report is a string of the form 0.digits with 1 to 100 decimal digits and a displayed value strictly between zero and one. It was produced by nearest decimal rounding, with exact half ties upward, of an unknown positive rational x in (0,1). Return [a,b] for a reduced fraction in the rounding interval with the smallest positive denominator b; if several have that denominator, choose the smallest numerator a. The lower rounding boundary is included and the upper excluded. Do not assume the displayed fraction is the original x, use floats, or scan denominators one by one: permitted denominators can have 100 digits. Use exact integer interval comparisons and a continued-fraction or Stern–Brocot search with quotient jumps. In Stern–Brocot search, neighbours L=a/b and R=c/d have \(cb-ad=1\); their mediant is \((a+c)/(b+d)\). The editorial explains why that helps minimize the denominator.',
        'def solve(report):',
        [{'args': ['0.29'], 'expected': [2,7]},
         {'args': ['0.12'], 'expected': [2,17]}],
        [{'args': ['0.13'], 'expected': [1,8]},
         {'args': ['0.5'], 'expected': [1,2]},
         {'args': ['0.10'], 'expected': [1,10]},
         {'args': ['0.99'], 'expected': [66,67]},
         {'args': ['0.01'], 'expected': [1,67]},
         {'args': ['0.333333333333333333'], 'expected': [1,3]},
         {'args': ['0.'+'0'*99+'1'], 'expected': [1,2*scale//3+1]},
         {'args': ['0.'+'9'*100], 'expected': [2*scale//3,2*scale//3+1]}],
        '''def solve(report):
    digits = report.split('.')[1]
    value = int(digits)
    denominator = 2 * 10**len(digits)
    low, high = 2*value-1, 2*value+1
    left_n, left_d = 0, 1
    right_n, right_d = 1, 0
    while True:
        n = left_n + right_n
        d = left_d + right_d
        if n*denominator < low*d:
            jumps = (low*left_d - denominator*left_n - 1) // (
                denominator*right_n - low*right_d)
            left_n += jumps*right_n
            left_d += jumps*right_d
        elif n*denominator >= high*d:
            jumps = (denominator*right_n - high*right_d) // (
                high*left_d - denominator*left_n)
            right_n += jumps*left_n
            right_d += jumps*left_d
        else:
            return [n,d]''',
        r'If the displayed integer digits are m at d decimal places, the exact interval is \([(2m-1)/(2\cdot10^d),(2m+1)/(2\cdot10^d))\). Start with neighbours 0/1 and 1/0 (the latter is an infinite right bound). Every fraction strictly between neighbours with determinant one has a numerator/denominator vector that is a positive-integer combination of their vectors. Consequently its denominator is at least the sum of their denominators. If the mediant is in the allowed interval, it achieves that lower bound and is the reduced minimum-denominator choice. Otherwise the entire interval lies on one side. Update the wrong-side neighbour by a multiple of the other, preserving the determinant-one invariant. For a left jump require \((L_n+jR_n)/(L_d+jR_d)<\text{low}\); cross multiplication gives the strict integer bound used in the reference. For a right jump require the analogous fraction >=high, retaining equality because high is excluded. The -1 in the strict bound is essential. Each jump skips a whole run of mediants, so a report near zero does not require visiting 10^100 denominators. Termination follows from the nested Stern–Brocot search reaching an allowed rational; quotient jumps are the Euclidean/continued-fraction acceleration. The number of jumps is O(log b) in the returned denominator, with exact large-integer arithmetic costs in addition. No general denominator bound needs to be guessed. For 0.12, 1/8 is at the excluded upper boundary; 2/17 is the simplest allowed fraction. This is the simplest compatible value, not proof that it was the unknown original value: uniqueness needs additional information, as in the interview question.')
