"""Expanded original courses; stable lesson IDs and understanding checks."""
CATALOG = {'l02': {'id': 'l02',
         'title': 'Condition, then normalise',
         'topic': 'Conditioning',
         'path': 'shared',
         'check': 'After seeing H from this mixture, what is P(always-heads)?',
         'options': ['1/2', '2/3', '3/4', '1'],
         'correct': 1,
         'explain': 'Divide 1/2 by the total H probability 3/4.',
         'qs': ['q02', 'q03'],
         'codes': []},
 'l03': {'id': 'l03',
         'title': 'Expectation without independence',
         'topic': 'Expectation',
         'path': 'shared',
         'check': 'Do overlapping indicators prevent adding their expectations?',
         'options': ['Yes, always',
                     'Only if they have equal means',
                     'No; covariance matters for variance',
                     'No; they must be independent'],
         'correct': 2,
         'explain': 'Linearity of expectation does not require independence.',
         'qs': ['q06', 'q07'],
         'codes': ['c02']},
 'l04': {'id': 'l04',
         'title': 'Distributions as usable models',
         'topic': 'Distributions',
         'path': 'shared',
         'check': 'Given an Exponential(rate 2) wait has exceeded 5, what is the expected '
                  'remaining wait?',
         'options': ['5', '2', '0.5', '5.5'],
         'correct': 2,
         'explain': 'Memorylessness gives a fresh expected wait of 1/2.',
         'qs': ['q08', 'q14', 'q15', 'q16'],
         'codes': []},
 'l05': {'id': 'l05',
         'title': 'A state is a sufficient memory',
         'topic': 'Stopping times',
         'path': 'shared',
         'check': 'What is the expected wait for HH in fair coin flips?',
         'options': ['2', '4', '6', '8'],
         'correct': 2,
         'explain': 'A tail erases a partial match; solving the two state equations gives 6.',
         'qs': ['q09', 'q10', 'q11', 'q12'],
         'codes': ['c03']},
 'l06': {'id': 'l06',
         'title': 'Arithmetic with a method',
         'topic': 'Mental math',
         'path': 'shared',
         'check': 'What is 15% of 240?',
         'options': ['24', '30', '36', '40'],
         'correct': 2,
         'explain': '10% is 24 and 5% is 12; add them.',
         'qs': ['q45'],
         'codes': []},
 'l07': {'id': 'l07',
         'title': 'Variance remembers dependence',
         'topic': 'Statistics',
         'path': 'shared',
         'check': 'What is Var(3X+2) when Var(X)=4?',
         'options': ['12', '14', '36', '38'],
         'correct': 2,
         'explain': 'Multiply variance by 3²; the shift adds no variance.',
         'qs': ['q17', 'q45'],
         'codes': ['c04']},
 'l08': {'id': 'l08',
         'title': 'Write data code that respects time',
         'topic': 'Research coding',
         'path': 'shared',
         'check': 'Which timestamp controls whether a feature was usable?',
         'options': ['Its event time in all cases',
                     'Its availability time at the decision point',
                     'The end of the dataset',
                     'Its row number'],
         'correct': 1,
         'explain': 'Availability defines the actual information set.',
         'qs': ['q44'],
         'codes': ['c05', 'c06']},
 'l09': {'id': 'l09',
         'title': 'Estimators, bias and uncertainty',
         'topic': 'Estimation',
         'path': 'researcher',
         'check': 'Which criterion combines variance and squared bias?',
         'options': ['Correlation', 'Mean squared error', 'A p-value', 'Sample size'],
         'correct': 1,
         'explain': 'MSE=Var(θ̂)+Bias(θ̂)².',
         'qs': ['q23', 'q24', 'q46'],
         'codes': ['c04']},
 'l10': {'id': 'l10',
         'title': 'Covariance is a matrix constraint',
         'topic': 'Linear algebra',
         'path': 'researcher',
         'check': 'Can a valid covariance matrix have a negative eigenvalue?',
         'options': ['Yes, if correlations are small',
                     'Yes, if variances are positive',
                     'No',
                     'Only for three variables'],
         'correct': 2,
         'explain': 'An eigenvector with negative eigenvalue would have negative portfolio '
                    'variance.',
         'qs': ['q20', 'q29'],
         'codes': []},
 'l11': {'id': 'l11',
         'title': 'Regression as projection',
         'topic': 'Regression',
         'path': 'researcher',
         'check': 'Which OLS property follows from including an intercept?',
         'options': ['Future errors have mean zero',
                     'Residuals sum to zero in sample',
                     'The slope is causal',
                     'The model cannot overfit'],
         'correct': 1,
         'explain': 'The intercept normal equation forces the in-sample residual sum to vanish.',
         'qs': ['q19', 'q21', 'q30'],
         'codes': ['c07']},
 'l12': {'id': 'l12',
         'title': 'Inference is a procedure',
         'topic': 'Inference',
         'path': 'researcher',
         'check': 'Does p=0.03 imply a 97% probability the alternative is true?',
         'options': ['Yes',
                     'No; posterior inference needs priors and likelihoods',
                     'Only with a large sample',
                     'Only for a two-sided test'],
         'correct': 1,
         'explain': 'The two probabilities condition on different things.',
         'qs': ['q22', 'q26', 'q47'],
         'codes': []},
 'l13': {'id': 'l13',
         'title': 'Dependent returns and effective sample size',
         'topic': 'Time series',
         'path': 'researcher',
         'check': 'With positive autocorrelation, the iid standard error of the mean is generally…',
         'options': ['Too large', 'Too small', 'Always exact', 'Zero'],
         'correct': 1,
         'explain': 'Positive covariance increases the variance of the mean.',
         'qs': ['q18', 'q31'],
         'codes': ['c08']},
 'l14': {'id': 'l14',
         'title': 'Validation must imitate deployment',
         'topic': 'Validation',
         'path': 'researcher',
         'check': 'Where should a scaler be fitted during cross-validation?',
         'options': ['On all rows once',
                     'Inside each training fold',
                     'On the final holdout',
                     'On train plus test'],
         'correct': 1,
         'explain': 'Its fitted parameters are part of the model and cannot use the test fold.',
         'qs': ['q27', 'q28'],
         'codes': ['c09', 'c10']},
 'l15': {'id': 'l15',
         'title': 'Search size belongs in the result',
         'topic': 'Validation',
         'path': 'researcher',
         'check': 'What does selecting the best validation result tend to do?',
         'options': ['Make it unbiased',
                     'Bias the selected score upward',
                     'Prove the winning mechanism',
                     'Remove the need for a final test'],
         'correct': 1,
         'explain': 'The winning model is often one that benefited from favourable validation '
                    'noise.',
         'qs': ['q04', 'q25', 'q32'],
         'codes': []},
 'l16': {'id': 'l16',
         'title': 'Defend a research result',
         'topic': 'Research design',
         'path': 'researcher',
         'check': 'Which is strongest evidence of a tradable result?',
         'options': ['High classification accuracy alone',
                     'A reproducible time-aware net backtest with executable prices and stated '
                     'assumptions',
                     'The best in-sample Sharpe',
                     'A persuasive story'],
         'correct': 1,
         'explain': 'It tests the actual decision and its economics, while remaining evidence '
                    'rather than a guarantee.',
         'qs': ['q33', 'q34'],
         'codes': ['c11']},
 'l17': {'id': 'l17',
         'title': 'Monte Carlo with variance reduction',
         'topic': 'Simulation',
         'path': 'researcher',
         'check': 'When does an antithetic pair reduce variance relative to independent draws?',
         'options': ['Whenever it uses the same seed',
                     'When the covariance of the pair is negative',
                     'Only when the function is linear',
                     'Always'],
         'correct': 1,
         'explain': 'Negative covariance lowers the variance of the average.',
         'qs': ['q43', 'q48'],
         'codes': ['c12']},
 'l18': {'id': 'l18',
         'title': 'Algorithms for a research notebook',
         'topic': 'Research coding',
         'path': 'researcher',
         'check': 'What is the main advantage of a monotone deque for sliding maxima?',
         'options': ['It sorts every window',
                     'Each index enters and leaves at most once',
                     'It requires no memory',
                     'It handles all operations in constant total time'],
         'correct': 1,
         'explain': 'That amortised argument gives O(n) total time and O(window) space.',
         'qs': ['q44'],
         'codes': ['c05', 'c13', 'c14']},
 'l19': {'id': 'l19',
         'title': 'Fair value before a trade',
         'topic': 'Expected value',
         'path': 'trader',
         'check': 'Fair value is 12; bid is 11 and ask 13. Which trade has positive expected edge '
                  'before costs?',
         'options': ['Buy', 'Sell', 'Both', 'Neither'],
         'correct': 3,
         'explain': 'Both directions lose one unit in expectation.',
         'qs': ['q35'],
         'codes': []},
 'l20': {'id': 'l20',
         'title': 'Order flow is information',
         'topic': 'Market making',
         'path': 'trader',
         'check': 'Why can selling above prior fair value still lose money?',
         'options': ['Arithmetic cannot be trusted',
                     'The buyer’s decision may reveal information',
                     'A spread is always bad',
                     'Risk-neutral agents never trade'],
         'correct': 1,
         'explain': 'Condition on the fill, not only on the prior.',
         'qs': ['q36', 'q42'],
         'codes': []},
 'l21': {'id': 'l21',
         'title': 'Continuation value and log growth',
         'topic': 'Decision theory',
         'path': 'trader',
         'check': 'For one free reroll, should you keep an initial 4?',
         'options': ['Yes, because 4 exceeds continuation value 3.5',
                     'No, because 6 is possible',
                     'Only if the last roll was high',
                     'Never'],
         'correct': 0,
         'explain': 'Choose by expected continuation payoff rather than the maximum possible '
                    'outcome.',
         'qs': ['q13', 'q37'],
         'codes': []},
 'l22': {'id': 'l22',
         'title': 'Risk lives in joint exposures',
         'topic': 'Risk',
         'path': 'trader',
         'check': 'Does positive expected value imply a trade should always be taken?',
         'options': ['Yes',
                     'No; constraints, risk and costs matter',
                     'Only when volatility is zero',
                     'Only in derivatives'],
         'correct': 1,
         'explain': 'Expected value does not describe feasibility or the full distribution.',
         'qs': ['q38'],
         'codes': []},
 'l23': {'id': 'l23',
         'title': 'The small mathematical-finance core',
         'topic': 'Mathematical finance',
         'path': 'trader',
         'check': 'Which term captures curvature in the underlying price?',
         'options': ['Delta', 'Gamma', 'The bid', 'The interest rate alone'],
         'correct': 1,
         'explain': 'Gamma is the second derivative with respect to the underlying.',
         'qs': ['q39', 'q40'],
         'codes': []},
 'l24': {'id': 'l24',
         'title': 'Strategic inference and calibration',
         'topic': 'Decision theory',
         'path': 'trader',
         'check': 'What is the central common-value auction correction?',
         'options': ['Bid your unconditional mean',
                     'Condition value on your signal and winning',
                     'Always bid zero',
                     'Ignore other bidders'],
         'correct': 1,
         'explain': 'Winning carries information about the relative extremeness of your estimate.',
         'qs': ['q41'],
         'codes': ['c14']}}

LESSONS=[]
def add(id,minutes,intro,objectives,sections,example,explain=None,trainers=None):
    meta=dict(CATALOG[id])
    meta.pop("id")
    if id=='l06':meta['qs']=[]
    if explain is not None:meta['explain']=explain
    LESSONS.append(dict(id=id,minutes=minutes,intro=intro,objectives=objectives,
                        sections=sections,example=example,trainers=trainers or [],**meta))

add('l02',22,
    'Conditioning changes the information you are allowed to use. Rebuild the relevant population before calculating, then use Bayes to compare explanations of what you observed.',
    ['Build a conditional sample space and normalise its probabilities.','Distinguish likelihood, prior and posterior.','Explain why conditioning can create dependence.'],[
('What does “given” mean?',r'''Let A and B be events in an experiment. The statement “given B” means that you know B happened, so outcomes outside B are no longer possible. You are computing a probability in that restricted population, not in the original one.

Provided \(P(B)>0\), define
\[P(A\mid B)=\frac{P(A\cap B)}{P(B)}.\]
The numerator is the probability mass that satisfies both conditions. Dividing by the mass of B rescales the restricted population so its total probability becomes one. If the original outcomes are equally likely, you may count favourable outcomes inside B. Otherwise, retain their probability weights.

The direction matters: “has a positive test given disease” and “has disease given a positive test” condition on different populations. They can have very different answers.'''),
('A concrete conditional sample space',r'''Roll two independent fair six-sided dice, with the first die distinguishable from the second. Before observing anything there are 36 equally likely ordered pairs. Now learn that the sum is 8. The surviving pairs are (2,6), (3,5), (4,4), (5,3) and (6,2).

Each surviving pair originally had probability 1/36. Their total mass is 5/36, so each now has conditional probability one fifth. The event “the dice agree” contains only (4,4), giving \(P(\text{double}\mid\text{sum}=8)=1/5\).

Do not keep a denominator of 36: that would compute the chance of a double AND a sum of 8, before receiving the observation. The new question asks about an experiment whose outcome is already known to satisfy the sum constraint.'''),
('Multiplication and total probability',r'''Rearranging the definition gives \(P(A\cap B)=P(A\mid B)P(B)\). This identity does not require independence. Independence is the additional statement that conditioning on B does not change the probability of A.

Suppose hypotheses \(H_1,\ldots,H_m\) are mutually exclusive and cover every possibility. For an observation D, split its probability into branches:
\[P(D)=\sum_{i=1}^{m}P(D\mid H_i)P(H_i).\]
You multiply along each branch and add across alternatives that cannot occur together. Check that the hypothesis list really covers the population. Omitting an alternative produces the wrong normalising denominator even if every multiplication is correct.'''),
('Bayes: update weights, then normalise',r'''The prior \(P(H_i)\) is a hypothesis's probability before D. The likelihood \(P(D\mid H_i)\) is the probability of the observation under that hypothesis. The posterior is its updated probability after D:
\[P(H_i\mid D)=\frac{P(D\mid H_i)P(H_i)}{\sum_jP(D\mid H_j)P(H_j)}.\]
A reliable interview method is to write one unnormalised weight for each hypothesis, then divide each weight by their sum. A large likelihood alone does not establish a large posterior: a very rare hypothesis can still have little total weight.

For a fair coin and an always-heads coin selected with equal probability, observing one head gives weights (one half times one half) and (one half times one). Their sum is three quarters, so the always-heads posterior is two thirds.'''),
('More observations require a sampling model',r'''Keep the SAME selected coin for k flips. Conditional on the fair-coin hypothesis, assume flips are independent. Its likelihood for k consecutive heads is \(2^{-k}\); the always-heads likelihood is one. Equal priors therefore give
\[P(\text{always-heads}\mid k\text{ heads})=\frac{1}{1+2^{-k}}.\]
For k=2 the posterior is four fifths. This formula would not describe a procedure that selects a fresh coin before every flip. An observed tail assigns zero posterior weight to the always-heads hypothesis under this idealised model. If the “always-heads” coin actually has a small tail probability, zero is no longer justified.

Before multiplying likelihoods, ask what remains fixed and which observations are conditionally independent.'''),
('Exact continuous observations need a different definition',r'''The event formula divides by P(B), so it does not directly define conditioning on an exact value of a continuous variable when that event has probability zero. A continuous signal requires a conditional-density model or another appropriate conditional-probability construction.

For discrete hypotheses and a continuous signal s, posterior weights can use the signal DENSITY under each hypothesis: prior weight times density at s, then normalise. A density is not the probability of that exact signal; it describes probability per unit signal near s. Its value can exceed one without violating probability bounds.

This distinction prevents an otherwise sensible Bayes argument from dividing by zero or treating a density as an event probability. Match likelihoods to whether the observation is a discrete event, an interval or a continuous measurement.'''),
('Conditioning can create dependence',r'''The two dice were independent before you learned their sum. Given sum 8, if you learn that the first die is 2, the second must be 6. The observation couples variables that previously varied freely.

Conversely, observations can be independent conditional on a hidden hypothesis while being dependent before that hypothesis is known. Repeated heads suggest that the same hidden coin is favourable, changing the prediction of the next flip. Be explicit about whether an independence claim is unconditional or conditional on a specified variable.

Rehearse the argument aloud: state the observation, identify surviving possibilities or hypothesis weights, normalise, and check that the result lies between zero and one. Finally say which sampling assumption would change the answer.''')],
r'''Compare the two dice and coin examples. For dice, the observation removes ordered pairs; for coins, both hypotheses survive but with different weights. In the coin experiment, the joint mass of “always-heads and a head” is one half; the total head probability is three quarters. Dividing yields two thirds. Predict the next flip without picking the most likely coin as if it were certain: \(P(\text{next H}\mid\text{first H})=(2/3)\times1+(1/3)\times(1/2)=5/6\). The posterior still retains uncertainty about the coin.''',
    explain='The always-heads branch contributes probability 1/2; the fair branch contributes 1/4. Normalise the first weight by their sum 3/4 to obtain 2/3.')

add('l03',22,
    'Expectation is a probability-weighted average. Its linearity lets you break complicated counts into simple indicators, even when their events overlap.',
    ['Define expectation and turn a count into indicators.','Use linearity without inventing independence.','Derive discrete and continuous tail-sum identities.'],[
('A random variable and its mean',r'''A random variable assigns a number to each outcome. For a discrete variable X with possible values x, its expectation is \(E[X]=\sum_x xP(X=x)\), whenever the expectation is well defined. A fair die has expectation (1+2+3+4+5+6)/6=3.5. The mean need not itself be a possible realised value.

For ordinary signed variables, absolute integrability, \(E[|X|]<\infty\), is a convenient condition that makes sums and rearrangements safe. Nonnegative variables can have an infinite expectation; the formula then describes an extended value rather than a finite average. State the assumption before manipulating an infinite series.'''),
('Why linearity works',r'''For integrable variables X and Y and constants a and b,
\[E[aX+bY]=aE[X]+bE[Y].\]
This follows by averaging the linear expression outcome by outcome. It does not require X and Y to be independent. If Y always equals X, the variables are maximally dependent, yet the mean of their sum is still twice the mean of X.

Independence is needed for other shortcuts. In general \(E[XY]\) does not equal \(E[X]E[Y]\). For a fair die X, the expectation of its square is 91/6, whereas the square of its expectation is 12.25. Always distinguish a sum, a product and a nonlinear transformation before selecting a rule.'''),
('Indicators convert events into arithmetic',r'''For an event A, its indicator \(I_A\) is one when A happens and zero otherwise. Hence \(E[I_A]=P(A)\). If a count C records how many of m events occur, write \(C=\sum_{i=1}^{m}I_i\). Linearity then gives
\[E[C]=\sum_{i=1}^{m}P(I_i=1).\]
You only need each event's individual probability to compute this mean. The indicators may overlap or share a common cause. A useful first step in a counting problem is to ask what one indicator should count: a position, an object, a pair or a distinct category. Choosing the wrong unit can double-count or omit events.'''),
('Overlapping heads, carefully counted',r'''Flip a fair coin independently 20 times. Let \(I_i\) indicate that flips i and i+1 are both heads, for i from 1 through 19. There are 19 possible adjacent positions, not 20. Each position is HH with probability one quarter, so the expected number of adjacent HH pairs is 19/4=4.75.

The sequence HHH contributes two pairs, at its first and second positions. Adjacent indicators are dependent because they share a flip, but their expectations still add. If the head probability is p with independent flips, the corresponding expectation is \((n-1)p^2\) for n flips. If flips are dependent, linearity still works but the individual pair probability may cease to be p squared.'''),
('Tail sums: count how many thresholds are crossed',r'''For a nonnegative integer-valued variable N, a realised value of three can be written as three ones: it exceeds or equals thresholds 1, 2 and 3. Thus \(N=\sum_{k=1}^{\infty}I_{\{N\geq k\}}\), giving
\[E[N]=\sum_{k=1}^{\infty}P(N\geq k).\]
Nonnegativity justifies this interchange even if the result is infinite. For a nonnegative continuous variable X, the analogous identity is
\[E[X]=\int_0^{\infty}P(X>t)\,dt.\]
The area under the survival curve represents the mean. Do not apply these nonnegative formulas unchanged to a variable that can take negative values. Separate its positive and negative parts and check finiteness.'''),
('The maximum of two dice',r'''Let M be the larger of two independent fair dice. For integer k from 1 through 6, both dice are at most k with probability \(P(M\leq k)=k^2/36\). Subtract successive cumulative probabilities to obtain
\[P(M=k)=\frac{k^2-(k-1)^2}{36}=\frac{2k-1}{36}.\]
Multiplying each k by this probability and summing yields 161/36, approximately 4.4722. A maximum preferentially selects larger outcomes, so the maximum of the means, 3.5, is not the expected maximum.

As a check, the minimum plus maximum equals the sum of the two dice in every outcome. Their expectations must therefore sum to seven, giving an expected minimum of 91/36. This uses a pointwise identity, not an independence assumption about minimum and maximum.'''),
('What linearity does not tell you',r'''A mean does not describe fluctuation around that mean. For a sum, variance contains covariance terms. With n independent fair flips, the HH-count variance is \((5n-7)/16\) for n at least two: each indicator contributes variance 3/16 and each adjacent pair contributes covariance 1/16 twice in the sum formula.

You will derive that variance machinery in the dependence lesson. For now, identify exactly where dependence mattered: not in adding means, but in relating indicators jointly. Practise explaining both the short solution and why the longer independence argument is unnecessary.''')],
r'''For two dice, compute the maximum's weighted sum explicitly: the numerator is \(1\times1+2\times3+3\times5+4\times7+5\times9+6\times11=161\), and the denominator is 36. A second route uses \(P(M\geq k)=1-(k-1)^2/36\) for k=1 through 6. Summing gives \(6-(0+1+4+9+16+25)/36=161/36\). Matching two methods is a useful interview check; neither treats the maximum as a fair die.''')

add('l04',25,
    'A distribution is a model for how an experiment produces outcomes. Learn its assumptions, support and probabilities before memorising its mean.',
    ['Distinguish probability mass, density, CDF and survival.','Derive the extremes of independent uniform draws.','Explain exponential memorylessness and competing clocks.'],[
('Describe the distribution before using a formula',r'''For a random variable X, the cumulative distribution function is \(F_X(x)=P(X\leq x)\). Its survival probability is \(P(X>x)=1-F_X(x)\). A discrete probability mass function assigns probabilities to individual values. A continuous density assigns probability through integration over intervals; a density value itself is not a point probability.

Specify the support: the set of allowed values. A Uniform(0,1) variable takes values between zero and one, with constant density one there. Its CDF is zero below zero, x on the unit interval and one above one. An exponential waiting time is nonnegative and unbounded. Mixing these supports is a common source of incorrect integrals.'''),
('Independent uniform draws and the maximum',r'''Draw n independent Uniform(0,1) variables \(U_1,\ldots,U_n\), with n a positive integer. Let M be their maximum. For x between zero and one, M is at most x precisely when every draw is at most x. Independence gives
\[P(M\leq x)=\prod_{i=1}^{n}P(U_i\leq x)=x^n.\]
Its density is \(nx^{n-1}\) on this interval, obtained by differentiating the CDF. The tail-integral identity also gives
\[E[M]=\int_0^1(1-x^n)\,dx=\frac{n}{n+1}.\]
For one draw the mean is one half; increasing n moves the expected maximum toward one. Both checks are consistent with the experiment.'''),
('The minimum uses survival probabilities',r'''Let m be the minimum of the same independent draws. The event m>x requires every draw to exceed x, so \(P(m>x)=(1-x)^n\) for x in the unit interval. Therefore,
\[E[m]=\int_0^1(1-x)^n\,dx=\frac{1}{n+1}.\]
For three draws, the minimum's mean is one quarter and the maximum's is three quarters. Those symmetric means result from the Uniform(0,1) model. They are not a general minimum/maximum rule for arbitrary distributions.

If all n draws are actually copies of one shared uniform variable, the independence multiplication fails. The minimum and maximum then both equal that variable and both have mean one half, regardless of n.'''),
('Exponential waiting times and units',r'''A waiting time T has exponential rate \(\lambda>0\) when its survival probability is \(P(T>t)=e^{-\lambda t}\) for t at least zero. Its density is \(\lambda e^{-\lambda t}\), and integrating the survival curve gives \(E[T]=1/\lambda\).

Rate and mean are different parameters. A rate of two arrivals per minute produces a mean wait of half a minute. A rate of one half per minute produces a mean wait of two minutes. The exponent must be dimensionless: rate times time has no units.

A constant exponential rate models a wait whose instantaneous chance of ending does not depend on its age. Real waits need not satisfy this assumption.'''),
('Memorylessness: remaining time is not total time',r'''For nonnegative s and t,
\[P(T>s+t\mid T>s)=\frac{e^{-\lambda(s+t)}}{e^{-\lambda s}}=e^{-\lambda t}.\]
Conditional on already waiting s, the remaining wait has the same exponential distribution as a fresh wait. Consequently its expected remaining time is 1/rate, while expected total time is s plus 1/rate.

With rate one half per minute and three minutes already elapsed, remaining expectation is two and total expectation is five. This distinction is the whole point of that interview question. For a wait uniformly distributed between zero and ten minutes, surviving past minute nine instead leaves a mean of half a minute; memorylessness fails.'''),
('Competing independent clocks',r'''Let X and Y be independent exponential waits with rates a and b, respectively. Their minimum exceeds t when both exceed t, so its survival is \(e^{-at}e^{-bt}=e^{-(a+b)t}\). The first ring therefore has exponential rate a+b.

The chance that X wins is
\[P(X<Y)=\int_0^\infty ae^{-at}e^{-bt}\,dt=\frac{a}{a+b}.\]
The integrand combines “X rings around t” with “Y has not rung yet”. Ties have probability zero for these continuous waits. This ratio assumes independent clocks and constant exponential rates; it is not a universal race formula for any waiting-time distributions.'''),
('Geometric probability depends on the experiment',r'''For the stick-cutting problem, choose two independent uniform positions on a unit stick, then order them as U<V. The three lengths are U, V-U and 1-V. A nondegenerate triangle requires every piece to be less than one half.

The ordered cut locations occupy a triangle of area one half. The valid region satisfies U<1/2, V>1/2 and V-U<1/2, with area one eighth. Their ratio is one quarter. Boundary equalities have probability zero.

Choosing an existing piece first and then cutting that piece defines another experiment and another distribution. Always derive the density on the region you are measuring instead of assuming that every visually plausible region is uniform.''')],
r'''Take two independent exponential clocks with rates three and two per minute. Their first ring has rate five per minute and expected time one fifth of a minute. The rate-three clock wins with probability three fifths. These are different objects: a time and a probability. Their joint density for “clock one wins at time t” is \(3e^{-5t}\), which factors into \((3/5)(5e^{-5t})\). Under this specific model the winner and first-ring time are independent.''')

add('l05',25,
    'Overlapping patterns and stopping problems become manageable when you retain exactly the history that affects the future. Turn that history into states and write first-step equations.',
    ['Define states, terminal conditions and first-step recurrences.','Solve overlapping-pattern waits without treating windows as independent trials.','Check finite expectation and solve a bounded random walk.'],[
('What are you counting, and when do you stop?',r'''A stopping time is a random time whose decision to stop can be made from observations available so far. Counting flips until the first HH pattern is a stopping-time problem. Deciding at time five whether to stop because flip six will be heads uses future information and is not a stopping time with respect to the observed flips.

State the convention: our wait includes every flip, including the final flips completing the pattern. Distinguish an expected stopping time from a probability of eventually stopping. A process can stop with probability one yet have infinite expected duration. Do not assume a finite answer merely because a recurrence can be written.'''),
('Choose a sufficient state',r'''Flip a fair coin independently until HH occurs. Before finishing, there are two useful states: state 0 means no trailing head, and state H means the latest flip was a head. State HH is terminal. Earlier history does not change future transition probabilities because the coin flips are independent and only the suffix matters for matching HH.

Let E0 and EH be expected additional flips from the two nonterminal states. The terminal state's expected additional wait is zero. Be precise about “additional”: EH is not the total number of flips already spent reaching H. This choice prevents adding elapsed time twice.'''),
('First-step equations and their solution',r'''From state 0, pay one flip. A tail leaves you in 0 and a head moves you to H, each with probability one half. From H, a head finishes while a tail returns to 0. Hence
\[E_0=1+\frac{E_0+E_H}{2},\qquad E_H=1+\frac{E_0}{2}.\]
The first equation gives \(E_0=2+E_H\). Substitute the second: \(E_0=3+E_0/2\), so E0=6 and EH=4.

The tempting answer four is the reciprocal of the probability of HH in a fixed two-flip window. Consecutive windows overlap and are not fresh independent attempts. A tail can destroy partial progress; the state recurrence records that information.'''),
('Why HT has a different waiting time',r'''For HT, retain state H again. From H, a tail finishes and another head leaves the useful suffix H. Thus \(E_H=1+E_H/2\), giving EH=2. The state-0 equation is unchanged, so E0=4.

For HHH, use states with zero, one and two trailing heads. Every tail returns to zero. With terminal wait zero, the equations are
\[E_0=1+(E_0+E_1)/2,\quad E_1=1+(E_0+E_2)/2,\quad E_2=1+E_0/2.\]
Solving yields E0=14. The probability of a particular HHH window is one eighth, but the expected wait is not eight. The distinction between a fixed-window event and a sequential search must remain visible in your explanation.'''),
('Prove that the wait has a finite mean',r'''For HH, split flips into nonoverlapping blocks of two. Each block is HH with probability one quarter, independently across blocks. Waiting for the first successful block has geometric mean four blocks, or eight flips. The actual HH search stops no later than that block procedure, so its expectation is at most eight and is finite.

This bound is not the exact answer six. Its job is to justify treating the expected-state equations as finite quantities. Similar block arguments work for any fixed finite pattern with positive probability under independent flips. For processes with unbounded states, finiteness may require a different argument.'''),
('Collecting symbols by stages',r'''Suppose each independent draw returns one of m equally likely symbols, with m a positive integer. After seeing k distinct symbols, a new symbol arrives with probability (m-k)/m. The stage wait is geometric, counting the successful draw, and has mean m/(m-k).

Add expected stage durations using linearity:
\[E[T]=m\sum_{j=1}^{m}\frac1j.\]
For four symbols the terms are 1, 4/3, 2 and 4, summing to 25/3. Unequal symbol probabilities change the success rate according to WHICH symbols you have seen, not only their count. The state “k distinct symbols” then ceases to be sufficient.'''),
('A bounded random walk',r'''A fair integer random walk moves one step left or right with equal probability and stops at 0 or N, where N is a positive integer. Let ti be the expected additional steps from position i. The boundary conditions are t0=tN=0 and
\[t_i=1+\frac{t_{i-1}+t_{i+1}}2.\]
The quadratic \(t_i=i(N-i)\) satisfies both the recurrence and boundaries. For N=12 and i=5 it gives 35. A finite interval and positive chance of reaching a boundary in a bounded number of steps imply a finite expected exit time.

For the probability of hitting N first, omit the one-step cost and use boundary probabilities zero and one. The solution is i/N. Means and hitting probabilities solve different equations; identify your target before writing the recurrence.''')],
r'''Solve HH again using a different counting convention. If you have just seen a head, a second head ends the search next flip; a tail consumes one flip and puts you back at the start. Thus EH=1+E0/2. At the start, E0=1+(E0+EH)/2. Solve to obtain EH=4 and E0=6. Explain out loud why EH is still four additional flips even though one head has already been observed: a tail may erase that progress and restart a six-flip expected search.''')

add('l06',18,
    'Mental arithmetic improves when you choose a structure before calculating. Build accuracy with decompositions, reciprocal anchors and checks, then train speed on the same methods.',
    ['Choose efficient decompositions for products and percentages.','Convert between fractions and decimals with stated precision.','Use magnitude checks and measured practice to improve speed.'],[
('Accuracy first: represent the calculation',r'''Mental math is not only recalling multiplication tables. It is choosing an equivalent expression that uses easier numbers and remembering the intermediate values reliably. Start a drill with a method you can explain; a fast wrong answer is not progress.

For 49 times 21, replace 49 by 50 minus one. Compute 50 times 21 as 1050, then subtract 21 to obtain 1029. The subtraction corrects the deliberate overestimate. If you subtract 49 instead, you are correcting the wrong factor. State what you changed before calculating its correction.'''),
('Distribute, then compensate',r'''The distributive identity \((a+b)c=ac+bc\) is the basic tool. For 23 times 14, use 23 times (10+4), giving 230+92=322. For 99 times 37, use 100 times 37 minus 37, giving 3663.

When both factors lie near the same anchor, the difference-of-squares identity can be shorter:
\[(a-b)(a+b)=a^2-b^2.\]
Thus 97 times 103 equals 100 squared minus 3 squared, or 9991. The factors must be equally far below and above the anchor. For 97 times 104, that identity does not apply directly; use 100 times 104 minus 3 times 104, giving 10088.'''),
('Percentages are fractions of the base',r'''A percentage p means p/100 of the stated base. Fifteen percent of 240 is ten percent plus five percent: 24+12=36. Eighteen percent of 250 is ten percent plus eight percent: 25+20=45. You may also exchange the operands: 18% of 250 equals 250% of 18, because both are the same product divided by 100.

Always identify the base. Increasing 100 by 20% gives 120. Decreasing that new value by 20% gives 96, not 100, because the second percentage applies to a different base. A relative change uses the original value in the denominator; a difference between percentages may instead be measured in percentage points.'''),
('Fractions: exact values and decimal anchors',r'''Keep common exact anchors available: one half is 0.5, one quarter 0.25, one fifth 0.2 and one eighth 0.125. Three eighths is three times 0.125=0.375. One sixteenth is half of one eighth=0.0625.

One sixth has repeating decimal 0.1666…, so 0.1667 is an approximation, not an equality. One seventh repeats the block 142857. Use a fraction when exactness matters; give a rounded decimal only with a stated precision.

For fractions with the same denominator, combine numerators before converting. Five twelfths plus seven twelfths equals one exactly. Converting each to a short rounded decimal can introduce an unnecessary rounding error.'''),
('Division and cancellation',r'''Division is multiplication by a reciprocal, but cancelling common factors is often easier. For 84 divided by 12, both numbers divide by three, reducing the problem to 28 divided by four, or seven. For 2.4 divided by 0.06, multiply numerator and denominator by 100 to obtain 240 divided by six, or forty.

Changing only the denominator changes the problem. When decimal places differ, write the common scaling operation explicitly. For 15/24, cancel a factor of three to obtain 5/8=0.625.

Approximate before doing a difficult division. Since 19 is slightly less than 20, 380 divided by 19 must be slightly more than 19; the exact value is twenty. A result near two or two hundred would fail the magnitude check.'''),
('Check the answer without repeating the same mistake',r'''Use an independent check: magnitude, last digit, reverse multiplication or a nearby anchor. For 49 times 21, the result should lie just below 50 times 21=1050 and end in nine. The answer 1029 meets both tests. For a probability, the result must lie between zero and one; that check catches many arithmetic failures but cannot prove the model is correct.

Avoid rounding too early in a chain of operations. If a trainer accepts fractions, an exact fraction is often safer than a decimal truncated to too few places. In an interview, state when your answer is an approximation and give an error scale when that matters.'''),
('Turn a short session into deliberate practice',r'''Start with untimed accuracy, then use a short timed round at a manageable difficulty. Review errors by cause: wrong sign, lost intermediate value, poor decomposition or premature rounding. Repeat the METHOD, rather than memorising only that one question's answer.

Compare both accuracy and correct answers per minute across similar rounds. A higher attempt rate paired with sharply lower accuracy may indicate rushing. Stopped rounds have a different duration from completed rounds, so compare pace as well as counts.

Rotate mental arithmetic and fraction conversion. Explain one mistake in writing after each session. The aim is reliable number sense you can use while reasoning about a harder probability or statistical problem.''')],
r'''Work out 15% of 240 in three ways: 10%+5% gives 24+12=36; 0.15 times 240 gives 36; and 240% of 15 is 2.4 times 15=36. Now calculate 97 times 103 using the symmetric anchor: \((100-3)(100+3)=10000-9=9991\). Check that it lies below 10000 and ends in one. These checks support the arithmetic; they do not replace the derivation.''',trainers=['math','fractions'])

add('l07',24,
    'Averages reduce idiosyncratic noise, but shared variation can remain. Build variance from its definition and keep covariance terms when observations move together.',
    ['Define variance, covariance and correlation with their units.','Derive the variance of a dependent mean.','Explain the common-shock limit and feasible correlation bounds.'],[
('Variance measures squared deviations',r'''For a variable X with finite second moment and mean mu, variance is \(\operatorname{Var}(X)=E[(X-\mu)^2]\). Expanding the square gives \(E[X^2]-E[X]^2\). Its units are the square of X's units; standard deviation is the square root and has the original units.

If you shift every value by a constant b, deviations from the shifted mean are unchanged. Scaling by a multiplies deviations by a, so
\[\operatorname{Var}(aX+b)=a^2\operatorname{Var}(X).\]
With variance four, multiplying by three and adding two produces variance 36, not fourteen. The additive constant changes the mean, not dispersion.'''),
('Covariance records joint movement',r'''For variables X and Y with finite second moments, covariance is \(\operatorname{Cov}(X,Y)=E[(X-E[X])(Y-E[Y])]\). Positive covariance means positive and negative deviations tend to align; negative covariance means they tend to oppose each other. Covariance has the product of the variables' units.

When both variances are positive, correlation is covariance divided by the product of their standard deviations. It is unitless and lies between minus one and one. If either variable is constant, that denominator vanishes and ordinary correlation is undefined.

Independence implies zero covariance when moments exist. Zero covariance alone does not imply independence: a symmetric variable and its square can have zero covariance while being deterministically related.'''),
('Expand a sum before applying shortcuts',r'''Subtract the means, square the sum and take expectations:
\[\operatorname{Var}(X+Y)=\operatorname{Var}(X)+\operatorname{Var}(Y)+2\operatorname{Cov}(X,Y).\]
For a weighted sum of m variables, the general form is
\[\operatorname{Var}\!\left(\sum_i a_iX_i\right)=\sum_i\sum_j a_i a_j\operatorname{Cov}(X_i,X_j).\]
The diagonal terms are individual variances. Each distinct unordered pair contributes twice, once as (i,j) and once as (j,i). Do not combine an ordered double sum with another extra factor of two.

If X and Y each have variance one and correlation one, they fluctuate together and the sum has variance four. The independence shortcut would give two.'''),
('Variance of the arithmetic mean',r'''For n observations, define \(\bar X=(X_1+\cdots+X_n)/n\). Applying the scaling and sum rules gives
\[\operatorname{Var}(\bar X)=\frac{1}{n^2}\sum_{i=1}^{n}\sum_{j=1}^{n}\operatorname{Cov}(X_i,X_j).\]
Under independence and a common variance sigma squared, only n diagonal terms remain, giving variance sigma squared divided by n. Without independence, count the off-diagonal terms too.

This is a statement about repeated samples of the estimator. It is not the sample variance of the observed numbers themselves. The standard error of the mean estimates the square root of this sampling variance.'''),
('Equicorrelation and the common component',r'''Assume every observation has variance \(\sigma^2>0\), and every distinct pair has the same correlation rho. There are n diagonal terms and n(n-1) ordered off-diagonal terms. Thus
\[\operatorname{Var}(\bar X)=\sigma^2\left[\rho+\frac{1-\rho}{n}\right].\]
For n=100, variance one and rho=0.1, the result is 0.109, not 0.01. As n grows, variance approaches 0.1. Averaging cannot eliminate a component shared by every observation.

For nonnegative rho, a concrete representation is \(X_i=Z+\epsilon_i\), with independent common shock Z and idiosyncratic noises, variances rho times sigma squared and (1-rho) times sigma squared. Averaging reduces the noises, while Z remains.'''),
('Not every correlation specification is possible',r'''An equicorrelation matrix must be positive semidefinite. Its common-direction eigenvalue is \(1+(n-1)\rho\), and the other n-1 eigenvalues are 1-rho. Nonnegative eigenvalues require
\[-\frac{1}{n-1}\leq\rho\leq1\qquad(n>1).\]
For 100 variables, pairwise correlation minus one tenth is impossible even though it lies inside the ordinary two-variable range. It would make the proposed mean variance negative.

The lower bound produces a zero-variance sum in the singular boundary case. Correlations constrain one another collectively; the covariance-matrix lesson develops this point further.'''),
('Apply the same reasoning to overlapping counts',r'''In independent fair coin flips, each HH indicator has mean one quarter and variance three sixteenths. Adjacent indicators jointly occur when three consecutive flips are heads, with probability one eighth. Their covariance is one eighth minus one sixteenth, or one sixteenth. Indicators at disjoint positions are independent.

For n flips with n at least two, the count has n-1 indicator variances and n-2 adjacent covariance pairs. Its variance is \(3(n-1)/16+2(n-2)/16=(5n-7)/16\). This illustrates exactly why linearity simplified the mean but did not remove dependence from the variance.''')],
r'''Compare 100 independent variance-one observations with 100 equicorrelated observations at rho=0.1. Their mean variances are 0.01 and 0.109; their standard errors are 0.1 and approximately 0.3302. The standard-error ratio is \(\sqrt{10.9}\), approximately 3.30. Do not compare the variance ratio as if it were the standard-error ratio. Explain what common variation remains when the sample size becomes very large.''')

add('l08',23,
    'A correct-looking calculation can use information that was not yet available. Treat time, boundaries and reproducibility as part of the algorithm.',
    ['Separate event time, availability time and decision time.','Define causal rolling windows and as-of joins precisely.','Build small reference tests before optimising an implementation.'],[
('Write an input and output contract',r'''Before coding, define what each input represents, its ordering and the intended output at every index. Specify empty inputs, duplicate timestamps, missing values and ties. A short example often reveals an ambiguity that a long implementation would hide.

For a rolling mean, “window three” is incomplete. Does the result at index i include the value at i, or only the three previous observations? What happens before three previous values exist? Write those rules first. In an interview, a clarified contract is evidence of reasoning, not a delay before the real work.'''),
('Three timestamps describe different facts',r'''Event time is when something happened in the source system. Availability time is when the feature reached the system making a decision. Decision time is when that system chose an action. If a feature's event time is 10:00:00 but it arrives at 10:00:02, a decision at 10:00:01 cannot use it.

Sorting and joining only by event time may introduce future information even when every join operation is mechanically correct. Preserve both event and availability timestamps when they differ. For historical revised data, distinguish a first published value from a later revision; the final cleaned database may not describe what was knowable earlier.'''),
('A causal rolling window',r'''Let values be x0, x1 and so on, and let w be a positive integer window size. A lagged mean at index i uses exactly the previous w observations: indices i-w through i-1, excluding i. Define a missing result when i<w unless the task explicitly allows a shorter initial window.

For values [2,4,6,8] and w=3, the first complete lagged mean occurs at i=3 and equals four, from [2,4,6]. A window including the current eight instead gives six. Both are arithmetic means; only one matches the specified timing contract.

A running sum removes the oldest value and adds the newly eligible previous value. Confirm that subtraction and addition use the same boundary convention as the slow reference implementation.'''),
('As-of joins use the available history',r'''For each decision time, select the most recent feature whose availability time is no later than that decision. Decide whether an exactly equal timestamp is allowed and how same-time ties are resolved. “At or before” is appropriate only if the feature was accessible at that instant under the system's timestamp convention.

With sorted features and decisions, maintain a pointer into the feature stream. Advance it while the next feature is eligible, then emit the latest eligible value. Both pointers move only forward, so total work is linear in the number of records after sorting. Before the first available feature, return the task's explicit missing-value representation.

A fast join on the wrong timestamp is still wrong. Complexity and information validity answer different questions.'''),
('Reference implementation before optimisation',r'''Start with a small transparent function that scans the available history for every decision. It may be slow, but its logic should directly express the contract. Compare the optimised two-pointer algorithm against that function on hand-built cases.

Include a feature arriving between two decisions, an exact-time tie, a decision before any feature, two revisions of one event and repeated decision timestamps. For windows, include size one, an input shorter than the window and constant data. Use assertions about eligibility as well as expected numbers: every selected feature must have been available by its decision.

Do not manufacture expected outputs by calling the same implementation being tested; that only repeats its assumptions.'''),
('Numerical and operational reproducibility',r'''A calculation should identify its data version, transformation parameters and time conventions. If a simulation contributes a feature, record the seed and sampling method. If floating-point sums are used, distinguish exact mathematical identities from approximate numerical equality.

Keep a simple baseline and reconcile a handful of records manually. A complicated notebook can hide a one-row offset behind persuasive charts. A reproducible research function should make it possible to inspect what inputs produced one output without reconstructing the whole project.

Passing the provided examples proves behaviour on those cases. It does not establish that every boundary, every time convention or every asymptotic complexity claim is correct.'''),
('Explain the solution as a sequence of invariants',r'''For a two-pointer join, the invariant is that the selected feature is the latest eligible one among all records passed by the feature pointer. For a rolling window, it is that the running sum contains exactly the specified eligible indices. State why initialization establishes the invariant and why each update preserves it.

Then separate time for sorting from time for the scan: an unsorted input may require sorting even though the join itself is linear. State auxiliary memory independently of output storage. The interview explanation should connect the code to the information boundary and the complexity argument.''')],
r'''A feature has event time 10:00:00, availability time 10:00:02 and value seven. At decision 10:00:01, output no available value if there is no older eligible feature. At 10:00:02, use seven only if equality is explicitly allowed; at 10:00:03 it is eligible. A later revision arriving at 10:00:05 must not alter what the earlier decisions could have used. Build these four cases into a reference test before implementing the fast scan.''')
add('l09',25,
    'An estimator is a rule applied to a random sample. Assess its repeated-sample behaviour separately from the particular value your dataset produced.',
    ['Distinguish parameters, estimators, estimates and uncertainty.','Derive the bias–variance decomposition of mean squared error.','Work through a biased maximum estimator and a Beta posterior update.'],[
('Parameter, estimator and estimate',r'''A parameter describes a population or model: a mean mu, success probability p or endpoint theta. An estimator is a function of random observations, such as their arithmetic mean. An estimate is the numerical result after you observe one dataset. The parameter is fixed in a frequentist sampling calculation; the estimator varies across possible samples.

For n independent identically distributed observations with mean mu and variance sigma squared, the sample mean is unbiased because its expectation is mu. Its sampling variance is sigma squared divided by n. The actual estimate from one sample can still be far from mu. Unbiasedness is an average property across repeated samples, not a guarantee about one result.'''),
('Bias and variance describe different errors',r'''For estimator T of parameter theta, define \(\operatorname{Bias}(T)=E[T]-\theta\). Its variance describes fluctuation around its own mean. A perfectly constant wrong estimator has zero variance but nonzero bias.

Mean squared error measures squared distance from the target:
\[\operatorname{MSE}(T)=E[(T-\theta)^2]=\operatorname{Var}(T)+\operatorname{Bias}(T)^2.\]
To derive this, write T-theta as (T-E[T])+(E[T]-theta), expand the square and observe that the cross term has expectation zero. This identity requires the relevant second moment to be finite. Reducing bias can increase variance, so unbiasedness alone does not rank estimators by MSE.'''),
('A maximum that underestimates an endpoint',r'''Draw n independent Uniform(0,theta) observations, with theta positive and n a positive integer. Let M be their maximum. It cannot exceed theta, and typically falls below it. Scaling the uniform-maximum result gives
\[E[M]=\frac{n}{n+1}\theta.\]
The bias is minus theta/(n+1). Multiplying by (n+1)/n yields an unbiased endpoint estimator. This correction follows from the assumed independent uniform model; it does not automatically apply to an arbitrary bounded distribution.

Notice why a common intuition fails: being close to the largest observation does not make an endpoint estimate unbiased. The random unobserved gap between the maximum and the endpoint has a positive mean.'''),
('Standard deviation versus standard error',r'''The standard deviation of individual observations describes their population spread. The standard error of an estimator describes how its value varies across repeated datasets. For an iid sample mean with finite variance, estimate its standard error by the sample standard deviation divided by the square root of n.

For iid observations, the usual sample variance with denominator n-1 is unbiased for the population variance. The correction accounts for estimating the sample mean from the same observations. This does not mean its square root is an unbiased standard-deviation estimator.

If observations are dependent, the sample-mean standard error must include covariance terms. A large number of rows is not automatically a large amount of independent information.'''),
('What a central limit theorem supplies',r'''For iid observations with finite mean mu and positive finite variance sigma squared, the classical central limit theorem says
\[\frac{\sqrt n(\bar X-\mu)}{\sigma}\Rightarrow N(0,1).\]
The arrow means convergence in distribution as n grows. It does not claim that observations themselves become Gaussian. It concerns a centred and scaled sample mean.

The normal approximation can be poor in a finite sample, especially with highly skewed or heavy-tailed observations. Infinite-variance data fall outside this classical theorem. Dependence requires different assumptions and often a different asymptotic variance. State both the object converging and the assumptions; “large sample” alone is not a theorem.'''),
('Bayesian estimation uses an explicit prior',r'''Now model Bernoulli trials with an unknown common success probability p. A Beta(alpha,beta) prior, with positive parameters alpha and beta, has density proportional to \(p^{\alpha-1}(1-p)^{\beta-1}\) on the unit interval. Its mean is alpha divided by alpha+beta.

Observe s successes and f failures, conditionally independent given p. Multiplying prior density by the likelihood gives a Beta(alpha+s,beta+f) posterior. This exponent addition is the conjugate update, not a memorised adjustment with unexplained pseudo-counts.

With Beta(2,2), three successes and one failure produce Beta(5,3), with mean 5/8. The sample proportion is 3/4. The posterior mean differs because it combines the prior with four observations. The next-trial predictive success probability is the posterior mean under this shared-p model.'''),
('Interpret an uncertainty statement',r'''A frequentist confidence interval is built by a sampling procedure with a stated long-run coverage rate under its assumptions. After observing a particular interval, the fixed parameter is either inside it or outside it. A Bayesian credible interval assigns posterior probability to parameter values conditional on the observed data and prior.

Both require a valid model; neither repairs selection bias or leakage. When explaining an estimate, give its target, sampling assumptions, method and uncertainty, then identify which source of uncertainty was omitted. Prediction uncertainty for a new observation also includes its own noise, so it is usually different from uncertainty about a population mean.''')],
r'''For a Bernoulli probability with Beta(2,2) prior and data containing three successes and one failure, write the unnormalised posterior as \(p^{1+3}(1-p)^{1+1}=p^4(1-p)^2\). Those exponents correspond to Beta(5,3), not Beta(4,2). Its mean is 5/8=0.625. Predict a new trial by averaging its conditional success probability p over the posterior, giving the same 0.625. State that the trials share one common p; a changing probability would need a different model.''')

add('l10',25,
    'A covariance matrix describes variation in every linear combination of variables. Its entries cannot be chosen independently: the whole matrix must represent a possible joint system.',
    ['Interpret covariance matrices and quadratic forms.','Use positive semidefiniteness to constrain correlations.','Explain singularity and stable numerical solutions.'],[
('What the entries mean',r'''Let X be a column vector of d random variables with finite second moments, and let mu be its mean vector. The covariance matrix is
\[\Sigma=E[(X-\mu)(X-\mu)^T].\]
Entry (i,j) is the covariance of variables i and j. Diagonal entries are variances; off-diagonal entries describe joint movement. The matrix is symmetric because covariance is symmetric.

A correlation matrix divides each covariance by the corresponding two standard deviations, assuming those standard deviations are positive. Its diagonal entries are one. Standardisation removes units but does not remove constraints between entries.'''),
('A portfolio is a linear combination',r'''For a real weight vector w, the scalar \(w^TX\) is a weighted combination of the variables. Its variance is
\[\operatorname{Var}(w^TX)=w^T\Sigma w.\]
Since a variance cannot be negative, a valid covariance matrix must give a nonnegative quadratic form for EVERY weight vector. This property is called positive semidefiniteness, abbreviated PSD.

Positive definiteness is stronger: the quadratic form is strictly positive for every nonzero w. A covariance matrix may be merely semidefinite when some nonzero linear combination is constant. Perfectly duplicated variables supply a simple example.'''),
('Eigenvalues describe variation along directions',r'''A real symmetric matrix can be decomposed into orthogonal eigenvector directions. Along an eigenvector, its quadratic form scales with the corresponding eigenvalue. Consequently a symmetric matrix is PSD exactly when all eigenvalues are nonnegative.

For two standardised variables with correlation rho, the correlation matrix has eigenvalues 1+rho and 1-rho. Their nonnegativity yields the familiar bound minus one to one. In larger systems, checking each pair separately is not enough: a vector involving several variables may still have a negative proposed variance.

Tiny negative eigenvalues in an estimated matrix may arise from rounding, but a materially negative one is evidence of an invalid covariance construction. Diagnose estimation, missing-data conventions and scaling before using the matrix in an optimisation.'''),
('Three correlations must fit together',r'''For standardised variables X, Y and Z, write a=Corr(X,Y), b=Corr(Y,Z) and c=Corr(X,Z). Their correlation matrix is
\[R=\begin{pmatrix}1&a&c\\a&1&b\\c&b&1\end{pmatrix}.\]
Its determinant is \(1+2abc-a^2-b^2-c^2\). PSD requires that determinant to be nonnegative, along with the other principal-minor conditions. For correlations a and b in the usual range, rearrangement yields
\[(c-ab)^2\leq(1-a^2)(1-b^2).\]
Thus c lies between \(ab-\sqrt{(1-a^2)(1-b^2)}\) and the corresponding plus expression. This is a joint feasibility bound; it is not obtained by checking c alone.'''),
('Show that the correlation bound is attainable',r'''Set a=b=0.8. The allowed c interval is 0.64 plus or minus 0.36, so its minimum is 0.28. Construct independent zero-mean variance-one variables Y and U and define
\[X=0.8Y+0.6U,\qquad Z=0.8Y-0.6U.\]
Both new variables have variance one. Their correlations with Y are 0.8, and their covariance with each other is 0.64-0.36=0.28. Because their variances are one, that covariance is also their correlation.

The boundary matrix is singular: X+Z=1.6Y exactly. Singularity here is a meaningful linear relationship, not a contradiction. A construction proves that the algebraic lower bound can actually occur.'''),
('Why direct inversion can be fragile',r'''An invertible covariance matrix can still be ill-conditioned: a tiny variance along one direction makes inverse-based weights extremely sensitive to estimation noise. Near-duplicate variables are a typical cause. A numerically returned inverse is not proof that the resulting estimate is stable.

When solving a linear system, prefer an appropriate solver or factorisation to explicitly forming an inverse. Cholesky factorisation is suited to symmetric positive-definite matrices; a singular PSD matrix may require an eigenvalue or singular-value treatment. Regularisation can improve stability but changes the problem, so explain what assumption or penalty it introduces.

Inspect both feasibility and sensitivity. An optimiser may exploit precisely the covariance directions you estimate least reliably.'''),
('Explain the matrix constraint in plain language',r'''In an interview, start from “every weighted combination must have a nonnegative variance”. Then show how that condition produces a pairwise bound, an eigenvalue condition or a determinant inequality in the specific example.

For two independent unbiased estimates of one parameter with variances v1 and v2, weights w and 1-w give variance w²v1+(1-w)²v2. Differentiation gives w=v2/(v1+v2): weights are proportional to inverse variances. At v1=1 and v2=4, weights are 4/5 and 1/5 and combined variance is 4/5. With covariance c, the derivative instead gives w=(v2-c)/(v1+v2-2c) when the denominator is positive and these weights are permitted. Boundaries or a zero denominator need separate treatment. Dependence changes the optimisation.

Avoid treating PSD as a magic property detached from random variables. Also avoid claiming every PSD matrix must be invertible: semidefinite includes zero eigenvalues. If you propose a matrix with unusual correlations, try a simple weight vector or explicit variable construction to check what it means. Feasibility and profitable predictive information are separate issues.''')],
r'''Suppose X and Y are standardised and perfectly correlated. Their covariance matrix has rows [1,1] and [1,1]. The variance of X-Y is zero, while the variance of X+Y is four. Its eigenvalues are zero and two, so it is valid PSD but singular. This example simultaneously explains why zero eigenvalues are allowed and why a formula requiring an ordinary inverse cannot be used without checking invertibility.''')

add('l11',25,
    'Least squares is a geometric projection and an optimisation problem. Derive its algebraic properties, then separate those properties from causal and out-of-sample claims.',
    ['Derive the normal equations and the intercept residual property.','Compute a population slope from covariance.','Diagnose measurement error, regularisation and causal overclaims.'],[
('Define the regression problem',r'''Observe n responses and p features per observation. Put the responses in a column vector y and the features in a design matrix X. If you include an intercept, add a column of ones to X. A coefficient vector beta predicts \(X\beta\), and the residual vector is \(r=y-X\beta\).

Ordinary least squares chooses beta to minimise the sum of squared residuals, \(\|y-X\beta\|^2\). This is a finite-data optimisation statement. It does not assume the features cause the response or that the fitted relation will remain stable on new data.'''),
('Differentiate to obtain the normal equations',r'''Differentiating the squared-error objective with respect to beta gives \(-2X^T(y-X\beta)\). At a least-squares solution,
\[X^TX\hat\beta=X^Ty,\qquad X^Tr=0.\]
The residual is orthogonal to every design column. Geometrically, the fitted response is the projection of y onto the space spanned by those columns.

If X has full column rank, the coefficient solution is unique and can be written using the inverse of \(X^TX\). In practical numerical work, solve the system with a stable factorisation rather than explicitly computing that inverse. If columns are redundant, coefficients need not be unique even though the fitted projection is.'''),
('Why residuals sum to zero with an intercept',r'''The intercept column contains one in every row. Orthogonality to that column means \(\sum_{i=1}^{n}r_i=0\). Equivalently, differentiating the loss with respect to the intercept gives minus twice the residual sum, which must vanish at an optimum.

Without an intercept column, there is no normal equation requiring that sum to be zero. With penalised or constrained fitting, inspect the actual objective and constraints rather than importing every unconstrained OLS property automatically.

A zero average in-sample residual is an algebraic consequence of fitting the intercept. It does not establish an unbiased future forecast: a model can satisfy it on training data and systematically miss on a changed population.'''),
('The population slope is a covariance ratio',r'''For a population regression of Y on one nonconstant feature W with an intercept and finite second moments, minimising expected squared error gives
\[b=\frac{\operatorname{Cov}(W,Y)}{\operatorname{Var}(W)},\qquad a=E[Y]-bE[W].\]
One derivation centres both variables, expands the squared-error expectation and differentiates the quadratic in b. This population coefficient is different from the random estimate fitted on one sample.

The slope describes the best linear prediction under this squared-error criterion. Even if the actual conditional mean is nonlinear, the population linear projection still has a well-defined meaning under these moment assumptions.'''),
('Measurement error in the feature',r'''Suppose \(Y=\beta X+\epsilon\), but you observe \(W=X+u\). Assume X, u and epsilon are mutually independent, centred, with finite variances. Then \(\operatorname{Cov}(W,Y)=\beta\operatorname{Var}(X)\), while \(\operatorname{Var}(W)=\operatorname{Var}(X)+\operatorname{Var}(u)\). Hence
\[b=\beta\frac{\operatorname{Var}(X)}{\operatorname{Var}(X)+\operatorname{Var}(u)}.\]
This shrinks the population slope toward zero. With beta=2, signal variance one and measurement-error variance three, the observed-feature slope is one half.

If u and epsilon are correlated, an additional covariance enters the numerator; attenuation can fail. Measurement error only in the response has a different consequence under independent, mean-zero error. State which variable is contaminated.'''),
('Regularisation changes the objective',r'''Ridge regression adds a penalty proportional to the squared coefficient norm, typically leaving the intercept unpenalised. For the penalised feature coefficients, the normal equations gain a positive diagonal term. This discourages large unstable coefficients and can reduce variance at the cost of bias.

Standardisation matters because a coefficient penalty depends on feature units. Fit scaling parameters on training data only, and apply those parameters to validation data. Regularisation strength is a selected model choice; evaluate that selection without using the final holdout.

Better numerical stability does not prove better deployment performance. Compare with a simple baseline under the same chronological validation and cost assumptions.'''),
('Prediction, explanation and causation',r'''An association may arise because a feature causes the response, the response affects the feature, or another variable affects both. OLS orthogonality by itself does not identify a causal effect. If important omitted factors correlate with included features, the slope can absorb their influence.

When asked to explain a fitted coefficient, state the population, information set, conditioning variables and target. When asked to defend a prediction, discuss availability, validation and distribution changes. A statistically precise in-sample coefficient can still be unusable in a real decision if its input was only available afterward.''')],
r'''Take centred independent X, u and epsilon, with variances one, three and any finite error variance, and let Y=2X+epsilon and W=X+u. Compute covariance first: it is two because every cross covariance vanishes. Compute W's variance: one plus three equals four. The slope is 2/4=0.5. Now introduce Cov(u,epsilon)=c while keeping the other required cross covariances zero: the slope becomes (2+c)/4. This shows exactly which independence assumption supported attenuation.''')

add('l12',25,
    'A statistical conclusion depends on a complete procedure: hypotheses, statistic, sampling plan and interpretation. A small p-value cannot compensate for changing those rules after looking at the data.',
    ['Interpret p-values and confidence intervals correctly.','Identify the sampling procedure behind an error-rate claim.','Explain optional stopping and reversals after pooling.'],[
('Specify the question and hypotheses',r'''A null hypothesis describes a population or data-generating model you want to assess; an alternative describes departures of interest. For example, a mean may equal zero under the null and differ from zero under a two-sided alternative. Choose the statistic and direction of extremeness before seeing the result.

A test statistic summarises the data. Its null distribution describes how that statistic varies when the null and the sampling assumptions hold. A test therefore depends on more than an observed number: sample selection, dependence, nuisance-parameter estimation and the stopping plan can all alter calibration.'''),
('What a p-value conditions on',r'''A p-value is the null-model probability of a statistic at least as extreme as the observed statistic, using the test's specified definition of extremeness. It conditions on the null model; it is not the probability that the null hypothesis is true given your data.

A p-value of 0.03 does not supply a 97% posterior probability for the alternative. Posterior inference requires priors and likelihoods over the hypotheses. Nor does 0.03 measure economic importance or the chance a strategy will make money.

A valid level-alpha test rejects according to a rule whose type-I error is at most alpha under the relevant null assumptions. That long-run property belongs to the entire procedure.'''),
('Confidence intervals and effect size',r'''A 95% confidence-interval procedure covers the fixed target parameter in 95% of repeated samples under its calibration assumptions. The particular interval you observe is not assigned a 95% posterior probability for that fixed parameter by this frequentist interpretation.

For an iid Gaussian mean with known positive standard deviation sigma, an exact normal-based interval is \(\bar X\pm1.96\sigma/\sqrt n\) to the usual rounded quantile precision. With unknown variance, the iid Gaussian setting uses an appropriate Student-t quantile and sample standard deviation. Asymptotic approximations need their own conditions.

Report the estimate and its uncertainty together. A tiny but precisely measured effect may be statistically detectable and practically irrelevant after costs.'''),
('Repeated looks change the test',r'''Suppose you recompute an ordinary fixed-sample 5% test after each new observation and stop at the first rejection. You have changed the sampling plan from the one used to calibrate a single fixed-sample test. The probability of ever crossing a boundary can exceed 5%.

The sequential p-values are generally dependent, so treating every look as an independent test is another unsupported shortcut. The key issue is that the stopping rule creates repeated opportunities to reject, not that every conceivable stopping rule is invalid.

Two principled approaches are to precommit to the fixed sample size and test, or to use a sequential procedure with justified boundary/error control. Alpha-spending designs or appropriately constructed always-valid tests need their stated assumptions; naming a martingale alone is not a proof.'''),
('Pooling can reverse comparisons',r'''Consider an easy group and a hard group. In the easy group, treatment succeeds 9 out of 10 times and control 80 out of 100: treatment wins 90% to 80%. In the hard group, treatment succeeds 20 out of 100 and control 1 out of 10: treatment again wins, 20% to 10%.

Overall, treatment has 29 successes out of 110 and control has 81 out of 110. The pooled comparison reverses because the treatment population places much greater weight on the hard group. Different mixtures, rather than an arithmetic contradiction, create the reversal.

Before interpreting a pooled rate, ask whether group composition differs and what population-level effect you actually want to estimate.'''),
('Adjustment requires a causal argument',r'''Stratifying by a relevant common cause can help compare similar groups, but adjusting for every measured variable is not a universal solution. Conditioning on a collider, a variable influenced by both sides of a relationship, can create an association that was absent before conditioning. Unmeasured confounding can also remain.

Distinguish a descriptive comparison, a predictive model and a causal claim. Random assignment helps identify treatment effects under additional assumptions, but a retrospectively chosen subgroup can still suffer from selection. State why each adjustment variable belongs in the design rather than relying only on its predictive usefulness.'''),
('Rehearse a defensible inference statement',r'''A clear statement identifies the target, estimate, uncertainty method, sample construction and decision rule. Add whether the hypothesis was selected before or after exploring the data, and whether any repeated looks or multiple candidate tests occurred.

If a result loses significance after a valid design correction, explain what information the original calculation omitted. Do not replace a missing inference design with a confident narrative. In quant research, the statistical procedure and the chronology of information are both part of the evidence.''')],
r'''Take the two-group comparison above. Treatment's pooled success rate is 29/110, about 26.4%; control's is 81/110, about 73.6%. Yet treatment wins within both groups. Recompute the comparison using a common 50/50 mixture: treatment averages (90%+20%)/2=55%, while control averages (80%+10%)/2=45%. This arithmetic isolates the composition effect. It does not, by itself, prove that either mixture identifies a causal treatment effect.''')

add('l13',26,
    'Time-series observations can carry repeated information. Derive how lagged covariance changes uncertainty before using iid standard errors or square-root-of-time scaling.',
    ['Define weak stationarity, autocovariance and autocorrelation.','Derive exact mean-estimation variance and an AR(1) approximation.','State what effective sample size and Sharpe scaling do—and do not—mean.'],[
('Define the time-series assumptions',r'''A time series records observations in order, such as X1, X2 and so on. Weak stationarity means the mean is constant, variances are finite and constant, and covariance depends only on the lag separating observations. It does not require independence or a Gaussian marginal distribution.

Write \(\gamma_h=\operatorname{Cov}(X_t,X_{t+h})\). The lag-zero value is the marginal variance. When it is positive, autocorrelation at lag h is \(\gamma_h/\gamma_0\). Stationarity concerns the population model; an apparently stable plot is not sufficient evidence for it.'''),
("Count each lag's covariance contribution",r'''For a stationary series of n observations, expand the variance of their sum. There are n variance terms. At lag h, there are n-h unordered observation pairs, each contributing covariance twice. Therefore,
\[\operatorname{Var}\left(\sum_{t=1}^nX_t\right)=n\gamma_0+2\sum_{h=1}^{n-1}(n-h)\gamma_h.\]
Divide by n squared to obtain mean-estimation variance. Equivalently,
\[\frac{\operatorname{Var}(\bar X)}{\gamma_0/n}=1+2\sum_{h=1}^{n-1}\left(1-\frac hn\right)\frac{\gamma_h}{\gamma_0}.\]
The taper 1-h/n counts fewer pairs at long lags. The iid formula discards every nonzero-lag term.'''),
('The stationary AR(1) model',r'''Consider \(X_t-\mu=\rho(X_{t-1}-\mu)+\epsilon_t\), with absolute rho less than one, independent centred innovations of variance tau squared, and the stationary solution. Then marginal variance is \(\tau^2/(1-\rho^2)\), and autocorrelation at lag h is rho to the power h.

The coefficient rho is not the innovation variance or the marginal variance. Positive rho produces persistence; negative rho produces alternating-sign autocorrelation. At absolute rho at least one, the usual stationary formulas no longer apply to this model.

If you initialise an AR(1) simulation at a fixed zero rather than its stationary distribution, its early observations do not automatically have stationary variance. Account for initialization or use an appropriate burn-in when the experiment requires stationarity.'''),
('Large-sample variance inflation',r'''For fixed absolute rho less than one and a long sample, the finite-lag taper becomes negligible in the AR(1) sum. The geometric series gives
\[1+2\sum_{h=1}^{\infty}\rho^h=\frac{1+\rho}{1-\rho}.\]
Thus mean-estimation variance is approximately marginal variance divided by n, multiplied by this factor. For rho=0.8, the factor is nine. The iid standard error understates the approximate standard error by a factor of three, because standard error is a square root.

Near a unit root, or in a short sample, the finite-n terms matter. The approximation assumes rho stays fixed as n grows; it should not be invoked blindly when persistence grows with sample size.'''),
('Define effective sample size for a specific estimator',r'''Define \(n_{\mathrm{eff}}\) by equating mean-estimation variance to \(\gamma_0/n_{\mathrm{eff}}\). The AR(1) asymptotic approximation becomes
\[n_{\mathrm{eff}}\approx n\frac{1-\rho}{1+\rho}.\]
For n=100 and rho=0.8 it is 100/9, about 11.11. The exact finite-n tapered variance yields a somewhat different number, about 11.63. Specify which quantity the question requests.

This is an information comparison for estimating the mean, not a universal count of independent rows for every estimator. Negative autocorrelation can produce a value larger than n under this definition because alternating fluctuations reduce mean variance.'''),
('Why square-root-of-time Sharpe scaling can fail',r'''Suppose returns have constant per-period mean and stationary covariance. A k-period sum has expected return k times the per-period mean, but its variance includes the lag terms above. Multiplying a one-period Sharpe ratio by the square root of k assumes the summed-return variance grows exactly linearly in k, among other modelling conventions.

Positive serial covariance can make that scaling optimistic. Negative serial covariance can have the opposite effect. Compounded returns, changing exposure and nonstationarity add further distinctions. Derive the variance of the actual return object rather than applying an annualisation factor because it is familiar.'''),
('Turn dependence into a validation question',r'''Plot and estimate autocorrelation, but remember that estimates have sampling noise. Overlapping targets mechanically share future increments and can create dependence even when underlying single-period returns are independent. Repeated measurements of one common exposure can also inflate the apparent sample size.

A defensible explanation states the target estimator, dependence model, finite-sample formula or approximation, and how uncertainty was estimated. If the model is only a rough illustration, say so. Blocking, appropriate time-series standard errors and chronological validation address different aspects of dependence; none is an automatic cure for leakage.''')],
r'''For a stationary AR(1) mean with rho=0.8 and 100 observations, compare the asymptotic variance \(9\gamma_0/100\) with the iid variance \(\gamma_0/100\). The approximate standard-error ratio is three and the effective sample size is 11.11. For the exact comparison, sum \(1+2\sum_{h=1}^{99}(1-h/100)0.8^h\), approximately 8.6, giving 100/8.6, approximately 11.63. These two answers correspond to different approximations, not contradictory definitions.''')
add('l14',25,
    'Validation is a simulation of how a decision would have been made. Preserve the order of information, fit every transformation within that boundary, and separate model selection from final evidence.',
    ['Design chronological training and validation splits.','Identify overlapping targets and explain purging or embargo choices.','Keep transformation fitting, model selection and final evaluation separate.'],[
('Start from the deployment question',r'''Define the decision time, prediction target and horizon before splitting rows. If a model will be trained on past observations and used on later observations, a validation experiment should imitate that chronology. Randomly mixing past and future rows may answer an easier but irrelevant question.

A training set supplies information used to fit model parameters. A validation set supports choices such as feature sets or hyperparameters. A final test set assesses the procedure after those choices are fixed. These roles concern information flow, not the names assigned to three files.

Include the retraining schedule: a model fixed for a month differs from one refitted each day using newly matured labels.'''),
('Walk forward through time',r'''A walk-forward split trains on an earlier interval and evaluates on a later interval. An expanding window keeps all eligible historical data; a rolling window keeps a bounded recent interval. Choose that convention to match the proposed deployment and explain its tradeoff between sample size and changing conditions.

At a training cutoff, a row's features may exist but its future target may not yet be known. If a target uses the next five observations, the final five rows before the cutoff can have unfinished labels. Exclude them until those labels would have matured.

Record exact boundaries and whether endpoints are included. A chronological split with an incorrectly available target can still leak.'''),
('Overlapping label intervals',r'''Suppose the target for a sample beginning at time t uses outcomes through t+5. Adjacent samples share parts of their target intervals. A training sample whose target interval overlaps a validation target may reveal information about validation outcomes.

Purging removes training samples with label-information intervals that intersect the protected validation intervals under the chosen endpoint convention. The overlap rule should reflect what actually enters the label, not merely whether starting timestamps differ.

Draw a small timeline and mark both ends of every interval. For a validation sample using times 10 through 15, a training label using 8 through 13 shares future outcomes with it. A sample using only times 2 through 7 does not share that label interval, although other dependence can remain.'''),
('Embargo needs a specific reason',r'''An embargo excludes an additional neighbourhood around protected data to address information reuse or dependence beyond the label overlap rule. Its length should be justified by feature construction, publication delays, target horizons or the evaluation design.

An arbitrary percentage of rows is not a substitute for identifying the dependence. In a strictly past-to-future split, data after the validation interval are not used for that fold's training anyway; an after-validation embargo may add no protection there. Other cross-validation designs can reuse later samples, making that boundary relevant.

Purging, embargo and chronological ordering solve related but distinct problems. Explain which leak or dependence each step addresses.'''),
('Transformations are part of fitting',r'''A scaler, imputer, feature selector or learned representation uses data to choose parameters. Fit it using the training portion of each fold, then transform validation data using those fixed parameters. Fitting a scaler once on the full dataset gives the training procedure information about the validation distribution.

For example, a validation-period price jump changes the full-data mean and standard deviation. If the training feature scale already reflects that jump, the simulated historical training was not actually limited to what was known then.

A transformation using a fixed, genuinely pre-specified constant is different from one estimated from future rows. Distinguish their information sources rather than labelling every preprocessing operation alike.'''),
('Selection belongs inside the evaluation loop',r'''To evaluate a model-selection procedure, use chronological inner splits inside each outer training interval. Select hyperparameters on those inner splits, refit the selected configuration on the eligible outer training data and evaluate once on the outer validation interval.

If you choose the configuration with the best outer results, those outer intervals have become selection data. They cannot simultaneously remain untouched evidence for that selected configuration. An honest report states which choices each dataset influenced.

Reserve a final holdout for the frozen procedure. If a disappointing final result causes you to change the model, the accessed holdout is no longer an untouched final test for that new model.'''),
('Validate the economic decision as well as the prediction',r'''Specify how forecasts become positions or quotes, then evaluate executable prices after realistic information and order latency. Include fees, spread, impact, turnover and relevant constraints. A predictive metric and net performance can move in different directions.

Use the same information boundary and cost conventions for the baseline. A sophisticated model should not receive more favourable data or execution assumptions than a simple comparison.

Before presenting a result, trace one validation decision end to end: available features, fitted parameters, forecast, action, execution price and realised target. This audit often finds errors that aggregate metrics hide.''')],
r'''You train at time 100 on labels that use outcomes through five time units after each sample's start. A sample starting at 98 has a label ending at 103, so its target is not yet known at the training cutoff. A sample starting at 94 ends at 99 and may be eligible if all its inputs and target were available. Fit the scaler on eligible training rows only, choose parameters with earlier inner splits, and evaluate decisions after the cutoff using the frozen training state.''')

add('l15',24,
    'The best result in a large search is partly selected for favourable noise. Keep the size and structure of that search visible when interpreting a promising candidate.',
    ['Combine base rates with test sensitivity and false-positive rates.','Compute a family-wise false-rejection probability under independence.','Separate discovery, selection and confirmation of a research idea.'],[
('Start with the candidate population',r'''Suppose only 2% of candidate ideas are genuinely useful under a stated definition. A screening test passes a useful idea with probability 90%, and passes a useless one with probability 10%. Sensitivity describes useful ideas; the false-positive rate describes useless ones. They are not probabilities of usefulness after observing a pass.

In 1000 candidates under these assumptions, expect 20 useful ideas, of which 18 pass, and 980 useless ideas, of which 98 pass. Among 116 expected passes, only 18 are useful. Thus
\[P(\text{useful}\mid\text{pass})=\frac{0.02\times0.9}{0.02\times0.9+0.98\times0.1}=\frac9{58}.\]
The approximately 15.5% posterior follows from the base rate as well as test performance.'''),
('A second test is not automatically independent evidence',r'''If two tests are conditionally independent GIVEN usefulness, their pass likelihoods multiply within each hypothesis. Two passes yield useful weight 0.02 times 0.9 squared and useless weight 0.98 times 0.1 squared, giving posterior 81/130, approximately 62.3%.

Conditional independence is doing substantive work. Two backtests on the same returns, with similar features and costs, may share the same noise or data error. Repeating the same test twice does not supply the likelihood multiplication above.

Specify why a new test measures something meaningfully different or uses appropriately held-out information. More result rows are not necessarily more independent evidence.'''),
('Many null tests create more rejection opportunities',r'''For m independent tests of true null hypotheses, each with exact false-rejection probability alpha, the probability that none rejects is \((1-\alpha)^m\). Therefore the chance of at least one false rejection is
\[1-(1-\alpha)^m.\]
Twenty independent 5% tests give approximately 64.2%, even though each individual test is correctly calibrated at 5%. This is a family-wise probability, not the expected fraction of false findings among all selected discoveries.

If tests are dependent, this exact formula changes. Dependence does not erase the selection issue; it changes the joint probability structure. State when the independence approximation is being used.'''),
('The winning score is a selected statistic',r'''Imagine testing many models with no true difference in expected performance. Their validation estimates vary because of sample noise. Selecting the highest estimate selects a model that benefited from positive noise in that particular sample, so its reported score tends to overstate its future performance.

The search includes manual changes: choosing a universe after inspecting results, trying different horizons, dropping an inconvenient period or revising transaction-cost assumptions. A search ledger should record these choices, not only the final hyperparameter grid.

A plausible economic story can help propose an idea, but writing the story after selection does not remove the score's selection bias.'''),
('Corrections answer different questions',r'''A family-wise-error procedure aims to limit the probability of one or more false rejections within a stated family. A false-discovery-rate procedure controls a different average property of the rejected set under its assumptions. Neither is interchangeable with “probability this particular strategy is useful”.

For example, a Bonferroni allocation tests each of m hypotheses at alpha/m and gives a family-wise bound by the union bound, without requiring independence. It can be conservative, and its relevance depends on what the family and decision rule actually are.

Research replication on genuinely new information addresses predictive stability, which is not identical to a multiple-testing correction. Use procedures whose targets match the claim you want to make.'''),
('Design discovery and confirmation separately',r'''Use exploratory data to generate hypotheses and choose a procedure. Freeze the target, feature construction, model-selection rules and evaluation metrics before confirmation. Chronological nested validation can estimate the whole selection procedure; a separately protected final holdout supplies an additional check.

Keep rejected ideas and simple baselines in the record. Report the number of trials you know about and acknowledge unrecorded manual exploration when it occurred. A result can remain interesting while its evidence is weaker than the largest plotted Sharpe suggests.

If confirmation fails, diagnose the failure. Quietly turning the holdout into another tuning set and continuing to label it “unseen” makes the reported evidence misleading.'''),
('What to say in an interview',r'''Explain a winning backtest as the outcome of both an economic hypothesis and a selection process. Identify where candidate generation occurred, which data chose the winner, and which data assessed the frozen procedure.

Then discuss dependence among trials, uncertainty in costs and sensitivity to deployment choices. Avoid giving an exact adjusted significance level when the actual search family is unknown. The strong answer makes the missing information explicit and proposes a design that can produce interpretable new evidence.''')],
r'''You ran twenty independent exact-level 5% tests under their true nulls. The chance of no false rejection is \(0.95^{20}\), approximately 0.3585. The chance of at least one is approximately 0.6415. If the tests all return the same decision because they are perfectly dependent copies, the family-wise probability is instead 5%. These contrasting cases show why search count alone cannot establish an exact correction without the joint structure.''')

add('l16',24,
    'A research defence should make one result traceable from its proposed mechanism to available information, executable decisions and out-of-sample evidence.',
    ['Connect the hypothesis, timestamps, target and decision rule.','Distinguish forecast accuracy, gross performance and executable net results.','Diagnose implementation, selection, regime and cost failures with falsifiable checks.'],[
('Define a claim narrow enough to test',r'''Begin with the universe, decision horizon and mechanism. For example, a temporary liquidity imbalance might predict a short-horizon movement under a specified market state. That is more testable than “machine learning predicts markets”. State what observation would weaken or contradict the mechanism.

Define the target and action separately. Predicting the next recorded trade price does not automatically tell you when to buy, at which price or for how long to hold. A research result should specify how a forecast becomes an executable decision, including a no-trade condition when the forecast does not cover costs or constraints.'''),
('Describe the information set',r'''For every input, state when it was created, published, received and usable. Include revisions, delayed feeds and asynchronous markets. A feature labelled with an old event time may still arrive too late for the decision.

Record the training interval and which labels had matured at each refit. If you evaluate after realistic latency, update the execution price rather than assuming the earlier displayed quote remains available.

Choose one decision and reconstruct it from raw records. If you cannot demonstrate that its inputs existed at that time, an attractive aggregate performance chart does not resolve the information-validity question.'''),
('Choose a baseline that tests the real claim',r'''Compare against a simple forecast and a simple decision rule. For next-price prediction, carrying forward the last price can already be highly accurate when prices change infrequently. High classification accuracy may mainly predict the large “no change” class.

Use metrics tied to the decision: calibration, conditional payoff, turnover and net performance, alongside the forecasting measure. Apply the same universe, timestamps, execution delays and costs to the baseline and the proposed model.

If the advanced model only wins under more favourable execution assumptions, the comparison does not identify a modelling improvement.'''),
('Separate gross and net economics',r'''Gross price movement is not the same as realised profit. A taker generally buys at ask and sells at bid; fees and impact add further deductions. A passive fill has a conditional selection process and an uncertain execution probability, which also require modelling.

As a toy example, buying at 100.05 and later selling at an executable bid of 100.10 gives gross profit 0.05 per unit. Fees of 0.01 on entry and exit leave 0.03, before additional impact. A chart of midpoint movement could show a larger gain than this actual route.

State units: price units, percentages, basis points and monetary profit should not be mixed. Report turnover because repeated small costs can dominate a small predictive advantage.'''),
('Diagnose a result that stops working',r'''First check implementation and data: timestamps, universe, missingness, labels, positions and reproducibility of the earlier result. Then inspect the selection process: how many models and evaluation choices were tried, and whether protected data influenced them.

Next examine distribution and market-state changes. Compare feature distributions, conditional outcomes and baseline performance across periods. Finally decompose gross versus net performance, fills, spreads, fees and impact.

These causes can coexist. A regime-change story should predict a diagnostic that can fail; it should not be used to bypass an unresolved code or leakage error.'''),
('Report uncertainty and robustness',r'''A point estimate needs an uncertainty method appropriate to dependence and selection. Break results into meaningful subperiods without treating every slice as another chance to select a flattering view. Test reasonable execution and parameter perturbations chosen for substantive reasons.

Capacity asks what happens when proposed order size grows relative to available liquidity; performance at negligible size may not scale. Risk asks about drawdowns, concentration and exposures, not just average profit.

An honest result separates observations from assumptions and acknowledges where the model lacks executable data or a validated fill process. Calling such evidence preliminary can make the argument clearer and more credible.'''),
('A compact defence sequence',r'''Rehearse the defence in this order: hypothesis and mechanism; available information; target and action; baseline; chronological validation; gross and net performance; uncertainty and constraints; the most important falsification test.

For each claim, identify the record, calculation or experiment supporting it. If the strongest evidence is a time-aware backtest, call it a backtest rather than a demonstrated live edge. The interview goal is to show that your reasoning survives concrete scrutiny, including a realistic account of what remains uncertain.''')],
r'''A forecast predicts that the next recorded trade price will remain at 100.00. It is accurate on many rows because trades are sparse and the last price is stale. At your decision time, the executable ask may already be 100.08 and the bid 100.06. Buying at the ask and immediately selling at the bid loses 0.02 before fees, despite an apparently accurate prediction of the recorded last price. Rebuild the target and baseline around prices and information usable by the decision.''')

add('l17',26,
    'Monte Carlo estimates an expectation through sampling. Treat simulation error explicitly, then design dependence or a control variable to reduce that error without changing the target.',
    ['State the target distribution and estimate a Monte Carlo standard error.','Derive an antithetic pair variance and compare equal simulation budgets.','Derive the optimal control coefficient and protect unbiasedness when estimating it.'],[
('Define the target and the estimator',r'''Suppose you want theta=E[g(X)] under a specified distribution for X. Draw independent samples from that distribution and average their transformed values Yi=g(Xi). The Monte Carlo mean is unbiased when the expectation exists; its variance is \(\operatorname{Var}(Y)/n\) when the variance is finite.

Simulation estimates the chosen model's expectation. It does not establish that the model describes a real market. Separate Monte Carlo error, numerical approximation and model misspecification when reporting a result.

Specify the distribution, random-generation method, sample size and function being evaluated. A reproducible seed helps recreate a run, but one seed is not evidence that the estimated expectation is accurate.'''),
('Quantify simulation uncertainty',r'''For independent finite-variance Yi, estimate the mean's standard error with their sample standard deviation divided by the square root of n. Approximate confidence intervals need an appropriate sampling approximation and can be unreliable for small samples or rare heavy-tailed payoffs.

To reduce standard error by a factor of two using independent sampling alone, you need roughly four times as many draws. This square-root rate motivates variance reduction.

If you generate dependent pairs, the independent units may be the pair averages, not the individual members. Estimate variance at the level of independent simulation units. Treating two deliberately correlated values as two independent observations gives the wrong error estimate.'''),
('Antithetic variables preserve marginals',r'''Let U be Uniform(0,1). Then 1-U is also Uniform(0,1). For a target g(U), the pair average \(A=[g(U)+g(1-U)]/2\) has the same expectation as g(U). Its variance is
\[\operatorname{Var}(A)=\frac12\left[\operatorname{Var}(g(U))+\operatorname{Cov}(g(U),g(1-U))\right].\]
An average of two independent copies instead has variance one half of Var(g(U)). Thus antithetic pairing helps when the covariance is negative; it can hurt when the covariance is positive.

Compare equal function-evaluation budgets. One pair uses two evaluations. Across n independently generated pairs, average n pair averages and estimate their sampling error as independent units.'''),
('Work through a squared-uniform example',r'''Take g(U)=U squared. The mean is one third, because integrating u squared from zero to one gives one third. The second moment is one fifth, so variance is \(1/5-1/9=4/45\).

For the pair, the product moment is \(E[U^2(1-U)^2]=1/30\), giving covariance \(1/30-1/9=-7/90\). Hence pair-average variance is
\[\frac12\left(\frac4{45}-\frac7{90}\right)=\frac1{180}.\]
Two independent squared uniforms have average variance 2/45. The antithetic variance is eight times smaller for these same two function evaluations. The improvement comes from negative covariance, not from a generic rule that symmetric inputs always help.'''),
('Control variates subtract predictable noise',r'''Let Y be the target variable and X a related variable whose expectation is known exactly. For a fixed coefficient c, define \(Z=Y-c(X-E[X])\). The subtracted term has expectation zero, so E[Z]=E[Y].

Expanding variance gives
\[\operatorname{Var}(Z)=\operatorname{Var}(Y)+c^2\operatorname{Var}(X)-2c\operatorname{Cov}(X,Y).\]
If Var(X)>0, differentiating in c yields \(c^*=\operatorname{Cov}(X,Y)/\operatorname{Var}(X)\). When both variances are positive, the resulting variance is \(\operatorname{Var}(Y)(1-\operatorname{Corr}(X,Y)^2)\).

A positive correlation leads to a positive coefficient; a negative correlation leads to a negative one. The control must have a known mean under the same sampling distribution.'''),
('Estimating the coefficient changes the argument',r'''The unbiasedness proof above treats c as fixed. If you estimate it from the same simulation data and then plug it into the final mean, its dependence on those data can complicate a finite-sample unbiasedness claim.

A simple design estimates c from an independent pilot sample, freezes it, and generates a new main sample. Conditional on the pilot, the main estimator remains unbiased under the stated model. Another option is a properly analysed sample-splitting or cross-fitting procedure.

The optimal theoretical coefficient is not a guarantee that a noisy estimated coefficient improves variance. A weak or badly estimated control can deliver little benefit; measure the error using the actual design.'''),
('Explain which error you reduced',r'''Variance reduction changes Monte Carlo precision for a fixed target and model. It does not reduce data leakage, transaction-cost uncertainty or systematic modelling error. Report both the estimator and the independent sampling unit used for its error estimate.

As a check, compare a small independent-sampling baseline against the reduced-variance estimator over reproducible independent replications. Agreement in their estimated means supports correct implementation; the spread across replications illustrates the variance change. A single unusually close result is not enough to establish that an estimator is better.''')],
r'''For Y=U squared and control X=U, the known control mean is one half. Cov(U,U squared)=1/4-1/6=1/12, and Var(U)=1/12, so the optimal coefficient is one. The adjusted observation is \(Z=U^2-U+1/2\), with mean one third and variance 1/180. It equals the squared-uniform antithetic pair average algebraically. Here the two techniques lead to the same random quantity, although evaluating the original function twice and using a simple control can have different computation costs.''')

add('l18',25,
    'Build research primitives around explicit invariants. Derive a stable streaming update, a linear-time window algorithm and a timestamp-safe join, then test their boundaries.',
    ['Derive and implement Welford mean/variance updates.','Explain the monotone-deque amortised complexity argument.','Specify timing, ties and reference tests for research data code.'],[
('Separate the contract from the algorithm',r'''An algorithm should implement a clearly defined mapping from inputs to outputs. Specify whether inputs are sorted, which windows include the current observation, how ties are resolved and what empty inputs return.

A fast implementation of a different contract is not an improvement. Write a slow transparent reference for small datasets first. Then derive an invariant: a statement about the algorithm's state that is true initially and remains true after every update.

Keep complexity claims precise. Linear time after sorting does not imply linear time for the entire pipeline when the input arrives unsorted. Output memory and auxiliary working memory are also different quantities.'''),
('Why naive variance can lose precision',r'''The identity variance=mean of squares minus square of mean is mathematically correct. When data have a very large common offset and small variation, these two large floating-point quantities can nearly cancel, amplifying rounding error.

Welford's algorithm maintains the count n, running mean m and sum of squared deviations M2. Its updates use deviations from the changing mean, avoiding that direct subtraction of two enormous nearly equal totals.

This improves numerical behaviour in common cases; it does not make floating-point arithmetic exact. Confirm the required behaviour for nonfinite inputs and very large magnitudes rather than silently accepting every value.'''),
('Welford updates, in order',r'''When a new value x arrives, increase n by one. Let delta be x minus the OLD mean. Update the mean to \(m_{\mathrm{new}}=m_{\mathrm{old}}+\delta/n\). Then update
\[M_{2,\mathrm{new}}=M_{2,\mathrm{old}}+\delta(x-m_{\mathrm{new}}).\]
The second factor uses the new mean. After n values, M2 equals the sum of squared deviations from the current sample mean. Dividing by n gives the descriptive variance of these observed values; dividing by n-1 gives the usual unbiased iid population-variance estimate when n is at least two.

Initialize count zero and M2 zero; handle the first observation consistently. Do not divide by n-1 for a single observation.'''),
('A monotone deque for sliding maxima',r'''For a current-inclusive window of positive integer size w, output the maximum among indices i-w+1 through i whenever the window is complete. Store candidate INDICES in a deque, ordered by increasing index and decreasing value.

Before processing an output, remove front indices older than the window. Before appending the new index, remove back candidates with value no greater than the new value: they are smaller or equal and will expire no later, so they cannot be needed for a future maximum. The front then identifies the current maximum.

Using “no greater” keeps the most recent of equal-valued candidates. If the task requires the earliest maximum index rather than only its value, reconsider this tie rule.'''),
('Why total deque work is linear',r'''Each index enters the deque once. It leaves at most once, either by expiring from the front or by being dominated at the back. Across n observations, the total number of insertions and removals is therefore proportional to n, even if one update removes many candidates.

This is an amortised argument, not a claim that every individual update performs only one operation. Auxiliary space is at most the window size, excluding the output list.

For [4,2,5,1] with a current-inclusive window of two, full-window maxima are [4,5,5]. A lagged window excluding the current observation is a different contract; adjust eligibility and indexing accordingly.'''),
('As-of joins and invariants',r'''For sorted decision times and feature availability times, maintain a feature pointer and the latest eligible record. Advance while the next feature is available at or before the decision under the stated tie convention. The invariant is that no unprocessed feature is eligible and the selected record is the most recent eligible one.

If timestamps repeat, define a stable secondary order or aggregate policy. If no feature has yet become eligible, emit the specified missing result. Event time alone is insufficient when availability differs.

A two-pointer scan takes linear time in the total records once inputs are sorted. Keep any sorting and data-cleaning cost separate in the analysis.'''),
('Tests that probe the reasoning',r'''For Welford, test constant values, a single observation and a large shared offset with small differences. For the deque, test increasing and decreasing sequences, equal values, window one and an input shorter than the window. For joins, test delayed availability, exact ties and a decision before the first feature.

Compare small random cases to a transparent reference and assert structural invariants. A correct result on one visible example does not establish the complexity argument; the insertion/removal reasoning does. In an interview, explain both why the state is sufficient and how its work is bounded.''')],
r'''Process [2,4,6] with Welford. After two values, n=2, mean=3 and M2=2. For x=6, delta=3, the new mean is four and the M2 increment is 3 times (6-4)=6. Final M2 is eight. Descriptive variance is 8/3; the usual sample variance is 8/(3-1)=4. Both values are legitimate answers to different variance definitions, so state the denominator convention before coding.''')

add('l19',22,
'Calculate the value of the payoff under your current information, then compare it with the price you can actually trade. A fair-value estimate and a profitable execution are different objects.',
['Translate a payoff into a conditional expected value.','Read bid and ask from the correct side of the trade.','Account for costs, uncertainty and information revealed by a fill.'],[
('Define the contract and information',r'''A contract specifies what you receive or owe under each future outcome. Let V denote its eventual cash payoff and let I denote the information currently available. In a simple risk-neutral, zero-interest, frictionless model, its fair value is the conditional expectation E[V|I]. This is a modelling assumption, not a universal pricing law for every risky asset.

Specify the settlement rule, currency, time horizon and information before calculating. If a payoff is the sum of three independent fair six-sided dice, each die has mean (1+2+3+4+5+6)/6=3.5. Before any reveal, expected payoff is 10.5.

Independence is not needed to add expectations. It is needed if you assert that revealing one die leaves the distributions of the others unchanged.'''),
('A reveal changes the calculation',r'''Suppose the first die is revealed as six and the remaining two are independent fair dice. The conditional expected payoff is now 6+3.5+3.5=13. The old value 10.5 used a different information set.

A noisy signal requires a probability-weighted update rather than replacing an unknown quantity with the signal itself. For possible values v and a signal s, compute posterior probabilities using prior weights times signal likelihoods, then calculate
\[E[V\mid s]=\sum_v vP(V=v\mid s).\]
A confident-looking observation cannot bypass the prior and observation model. Also distinguish seeing a value from seeing someone choose to trade: the latter may reveal information indirectly.'''),
('Read a two-sided quote',r'''A dealer's bid is the price at which the dealer buys from you; its ask is the price at which the dealer sells to you. If you take liquidity, you BUY at the ask and SELL at the bid. A quote 11 / 13 therefore offers you a purchase at 13 or a sale at 11.

The midpoint is 12 and the spread is two. The midpoint is a description of the quote, not automatically the contract's fair value. Your valuation could differ because of information, model assumptions or financing.

Describe the side explicitly in an interview. “Buy at the bid” would require posting an order and waiting for a fill, which is a different execution model from immediately accepting the displayed quote.'''),
('Expected edge uses executable prices',r'''For an immediate one-unit purchase held to settlement, expected profit before financing is fair value minus ask minus the applicable costs. For a permitted one-unit sale, it is bid minus fair value minus costs. Here costs should include the actual fees and other expenses of the assumed transaction.

With value 12 and quote 11 / 13, buying has edge -1 and selling also has edge -1 before costs. Neither is attractive under this objective. With value 13 and ask 12, the purchase has one unit of expected gross edge, which costs may reduce or eliminate.

If you plan to exit early, the relevant payoff is the executable exit value, not necessarily terminal settlement. Do not subtract a spread twice if your entry and exit prices already incorporate it.'''),
('Expectations do not describe all the risk',r'''A fair value can be correct while the realised payoff is very different. Before the dice reveal, the payoff ranges from three to eighteen; a buyer at 10.5 can lose or gain. Expected profit averages across repeated outcomes rather than promising each transaction's result.

An uncertain valuation adds another layer. Ask how edge changes under plausible posterior or parameter errors, and which losses are possible. If trades share the same underlying uncertain event, repeating them does not create independent trials.

A positive mean therefore does not settle whether a trade is feasible under a capital limit, acceptable under a risk objective or available in the stated size.'''),
('Discounting and replication are distinct arguments',r'''If a known cash payment K arrives after time T and the constant continuously compounded risk-free rate is r, its present value in the idealised borrowing/lending model is \(Ke^{-rT}\). A deterministic payment can be replicated by an appropriate investment in cash.

For uncertain payoffs, simply discounting a physical expectation is not generally enough to establish a no-arbitrage price. Replication or an appropriate pricing model may be required. Our dice examples deliberately use immediate settlement, risk-neutral valuation and no financing to isolate conditional expectation.

State these simplifying assumptions rather than applying the dice pricing rule to every derivative or risky security.'''),
('Evaluate the information at execution',r'''A quote can be chosen before the counterparty decides whether to trade. If their decision depends on private information, the distribution conditional on a fill differs from the prior distribution. Selling above prior fair value can then lose on average among actual sales.

A disciplined sequence is: define the payoff; identify the information; update the value; read the executable side; subtract costs; inspect risk; and ask what the fill itself reveals. The next module develops this final step with a complete probability tree. Keeping these objects separate makes both your arithmetic and your interview explanation easier to audit.''')],
r'''Three independent fair dice settle their sum. After seeing the first die as six, fair value is 13. A dealer quotes 12 / 14. Buying at 14 loses one unit in expectation; selling at 12 also loses one. Now suppose a different executable ask is 12.5 and the all-in purchase cost is 0.2. Expected net profit from buying and holding to immediate settlement is 13-12.5-0.2=0.3. This conclusion uses independent unrevealed dice and an uninformed fill; it does not say the payoff cannot fall below your purchase price.''')

add('l20',25,
'An order is an observation about the person choosing to trade. Build the distribution of actual fills before deciding whether a spread protects you.',
['Calculate conditional fair value after an informed-or-uninformed buy.','Distinguish adverse selection from inventory exposure.','Explain a quote skew without claiming an unspecified optimum.'],[
('Specify who trades and when',r'''Consider a contract whose payoff V is either zero or 100, each with probability one half. A potential buyer's type is independent of V: with probability one half they are informed and observe V; otherwise they are uninformed.

For this particular model, an informed buyer buys only when V=100, while an uninformed buyer ALWAYS buys. Assume a displayed ask of 55, one-unit trades and no other costs. The unconditional expected payoff is 50.

The uninformed decision rule matters. Replacing “always buys” with “randomly buys or sells” changes the posterior. Write the actual rules before drawing a probability tree; a remembered answer from a similar example may be wrong.'''),
('Enumerate the four branches',r'''There are four equally likely combinations, each with probability one quarter: high value/informed, high value/uninformed, low value/informed and low value/uninformed. The first, second and fourth produce a buy. Low value/informed produces no buy.

Thus P(buy)=3/4 and P(V=100 and buy)=1/2. Bayes gives
\[P(V=100\mid\text{buy})=\frac{1/2}{3/4}=\frac23.\]
The payoff conditional on a buy is therefore \(100\times2/3=200/3\), about 66.67. Conditioning has removed the low-value informed branch and renormalised the remaining probability mass.'''),
('Evaluate profit among actual sales',r'''The dealer receives 55 upon a sale and ultimately pays V. Expected profit conditional on a buy is
\[E[55-V\mid\text{buy}]=55-\frac{200}{3}=-\frac{35}{3}.\]
That is an expected loss of approximately 11.67 per filled sale, despite asking five above the PRIOR fair value of 50. The execution selected a more valuable population of contracts.

Per opportunity, expected profit also includes the chance of no trade: (3/4)(-35/3)=-35/4=-8.75. Equivalently, weight the three filled branches' profits -45, -45 and 55 by one quarter each. Distinguish per-fill and per-opportunity quantities.'''),
('A conditional break-even price needs its model',r'''Holding the stated buying rules fixed, an ask of 200/3 would break even among fills before costs. But changing a quote can change who chooses to trade. In a realistic response model, conditional value depends on the quote as well as the observed side.

For example, an uninformed buyer may stop buying at a higher ask. Removing their low-value buys can increase adverse selection among remaining fills. One cannot generally solve for a profitable quote by taking a posterior calculated at one price and treating it as price-invariant.

The calculation above explains a mechanism under specified behaviour. An optimal quote requires a demand or arrival model, cost assumptions, position constraints and an objective.'''),
('Inventory changes the objective',r'''Inventory is the position you already hold. A dealer with positive inventory is long: it benefits from an increase in value and loses from a decrease. Even an informationally fair new purchase could increase exposure beyond a desired limit.

Adverse selection concerns what an incoming order reveals about value; inventory risk concerns the consequences of your existing and resulting position. They may interact, but they are not the same cost.

Track how a fill changes both belief and quantity. A customer's buy reduces the dealer's long inventory by one; a customer's sale to the dealer increases it by one. This sign convention helps prevent quote-skew arguments from being reversed.'''),
('Quote centre and width have different effects',r'''Under ordinary price-responsive flow, lowering both bid and ask can encourage customers to buy from a long dealer by offering a cheaper ask, while discouraging customers from selling to it by offering a less attractive bid. This shifts the quote centre downward.

Widening symmetrically lowers the bid and raises the ask. It can reduce fills on both sides, including the sales that would reduce a long inventory. It is therefore not the same action as changing the centre.

These are directional arguments under stated customer responses. Their magnitudes and even applicability depend on the market and flow model. There is no universal optimal skew amount supplied by the sign of inventory alone.'''),
('Explain the mechanism with a counterexample',r'''If informed and uninformed customers had identical trading behaviour independent of V, observing a buy would carry no information about V and conditional fair value would remain 50. If informed traders were much more prevalent, the posterior would move more sharply toward high value.

An interview defence should identify the exact branch that gets selected out, compute the conditional denominator, evaluate dealer profit and describe how changed behaviour would change the result. Do not replace this argument with “market makers earn the spread”: a spread can compensate for costs, but its existence does not prove positive expected profit.''')],
r'''Let the informed fraction be a, independent of payoff, with 0≤a≤1. Retain the rule that uninformed buyers always buy. A buy occurs with probability a/2+(1-a)=1-a/2, while high value AND a buy has probability 1/2. Conditional expected payoff is 100/(2-a). It is 50 when a=0, 200/3 when a=1/2 and 100 when a=1. More informed flow increases conditional value among sales. This formula relies on the same trading rules at every a; it does not establish how demand responds to a changed ask.''')

add('l21',25,
'Compare the payoff you can keep with the value of the remaining choices. Then see why maximising an expected payoff and maximising expected log wealth produce different decisions.',
['Derive the continuation value of a finite reroll game.','Distinguish realised outcomes from the quality of a decision.','Derive a toy log-growth optimum and state its assumptions.'],[
('Define the decision and objective',r'''A fair six-sided die is rolled. After observing its value x, you may keep x or reroll once, accepting the second result. Assume no reroll cost, independent rolls, and an objective of maximising expected numerical payoff.

The expected payoff of a fresh roll is 3.5. After observing x, that number is the continuation value of rerolling: it averages the outcomes of your remaining action. Keep x if x exceeds 3.5 and reroll if x is smaller. For integer faces this means keep four, five and six.

The possibility of rolling six does not make rerolling a four optimal. You must compare a certain four with the entire distribution of the alternative, using the specified objective.'''),
('Average the optimal conditional decisions',r'''Before the first roll, each face occurs with probability one sixth. Optimal conditional values are 3.5 for initial one, two or three, and four, five or six for the other faces. Therefore
\[E[\text{optimal payoff}]=\frac{3(3.5)+4+5+6}{6}=4.25.\]
This is the value of the option to reroll selectively. Rerolling every face would give only 3.5; keeping every face also gives 3.5.

If a reroll costs one payoff unit, continuation becomes 2.5, so keep three through six. The ex-ante optimal value becomes (2×2.5+3+4+5+6)/6=23/6. The action threshold changes because the alternative changed.'''),
('More stages require backward induction',r'''Let c_k be the value of a fresh roll when you may still reroll up to k times after observing it. With no rerolls, c_0=3.5. A new roll with k≥1 has value
\[c_k=\frac16\sum_{x=1}^6\max(x,c_{k-1}).\]
The previous-stage value is the continuation alternative. Thus c_1=4.25. With two rerolls available, keep five or six and reroll one through four, giving c_2=(4×4.25+5+6)/6=14/3.

This finite-horizon recurrence uses independence and no costs. A different payoff utility, state-dependent cost or dependent roll process needs different states or continuation values. Name the remaining choices before applying a threshold.'''),
('A good decision can lose this time',r'''Keeping four is optimal in the one-free-reroll game even if a hypothetical reroll would have produced six. That unseen favourable outcome does not change the expected value at the decision point. Conversely, a poor decision can happen to pay off.

Distinguish policy quality, evaluated under the available information and objective, from the realised result. In research, comparing policies requires consistent information and sampling rules; selecting only lucky realised choices distorts the evaluation.

The objective itself matters. A person who strongly dislikes low outcomes may maximise expected utility rather than expected payoff, changing the continuation comparison.'''),
('Set up the log-wealth model',r'''Consider a repeated even-money bet with known win probability p, where 0<p<1. Assume independent rounds, a constant fraction f of current wealth staked each round, no fees, and 0≤f<1. A win multiplies wealth by 1+f; a loss multiplies it by 1-f.

Expected log growth per round is
\[g(f)=p\log(1+f)+(1-p)\log(1-f).\]
Logs convert multiplication of wealth into addition across rounds. This objective differs from expected profit in one round. Betting everything has a possible ruin outcome when p<1 and makes log wealth undefined there, which is why f=1 is excluded.'''),
('Differentiate and check the constraints',r'''The derivative is \(g'(f)=p/(1+f)-(1-p)/(1-f)\). Setting it to zero gives p(1-f)=(1-p)(1+f), hence f=2p-1. The second derivative is negative throughout the domain, so the function is strictly concave.

With the long-only constraint 0≤f<1, the optimum is max(0,2p-1). At p=0.6 it is 0.2. Substitution gives 0.6 log(1.2)+0.4 log(0.8), about 0.0201 per round in the specified model.

If negative fractions were allowed, the feasible set and interpretation would differ. Derive the stationary point, then check the boundary and permitted actions; a formula without its domain is incomplete.'''),
('Uncertain probabilities are a different problem',r'''The derivation assumes p is known and the only payoffs are equal-sized wins and losses. An estimate of p from a short sample is uncertain; correlated opportunities, unequal payoffs, fees, liquidity constraints and larger-than-modelled losses also alter the objective.

A sensitivity calculation already shows fragility: changing p from 0.60 to 0.52 changes the toy optimum from 0.20 to 0.04. A model-based fraction cannot be carried directly into real trading without defining those missing features and constraints.

For an interview, present log growth as a mathematical decision model, derive it and explain its limitations. Do not confuse positive expected payoff with a license to increase size indefinitely.''')],
r'''At p=0.6, an even-money fraction f=0.2 gives expected log growth about 0.0201. At f=0.5 it becomes 0.6 log(1.5)+0.4 log(0.5), about -0.03398, even though expected one-round wealth gain is f(2p-1)>0 in both cases. The larger fraction wins on average in the arithmetic one-round objective yet loses in expected log growth. The difference comes from the objective's treatment of downside compounding, not from different win probabilities.''')

add('l22',23,
'Positions interact through their joint payoffs. Measure the combined exposure, then separate an estimated variance from the constraints and tail behaviour it leaves out.',
['Calculate portfolio variance including covariance.','Stress correlations and identify shared exposures.','Distinguish a risk estimate from feasibility and tail-loss control.'],[
('Specify weights, units and returns',r'''Let R_1 and R_2 be returns measured over the same horizon, and let w_1 and w_2 be portfolio weights fixed before those returns occur. In a simple linear portfolio, return is R_p=w_1R_1+w_2R_2. State whether weights are capital fractions, notionals or position quantities; the units of the resulting payoff differ.

For weights summing to one, this describes a fully allocated simple-return portfolio under the stated linear model. Shorts and leverage can make weights negative or make total gross exposure exceed one.

Do not combine daily variance with hourly covariance, or return weights with cash-profit variances, without conversion. A precise horizon and unit convention comes before the formula.'''),
('Expand the square to see covariance',r'''For finite second moments, centre both returns around their means and square the weighted sum. Taking expectations gives
\[\operatorname{Var}(R_p)=w_1^2\sigma_1^2+w_2^2\sigma_2^2+2w_1w_2\operatorname{Cov}(R_1,R_2).\]
Here sigma_i is the standard deviation of asset i. Covariance equals rho times sigma_1 times sigma_2, where rho is their correlation and both standard deviations are positive.

The cross term is why two individually risky assets can offset each other, or reinforce the same risk. With more assets the formula becomes \(w^\top\Sigma w\), where Sigma is the joint covariance matrix, not a list of isolated variances.'''),
('Work through an equal-weight pair',r'''Suppose both assets have variance four, so each standard deviation is two, and their correlation is 0.5. Their covariance is 0.5×2×2=2. At weights one half each, portfolio variance is
\[\tfrac14(4)+\tfrac14(4)+2(\tfrac12)(\tfrac12)(2)=3.\]
The standard deviation is sqrt(3), not three. At correlation zero variance becomes two; at correlation minus one half it becomes one; at correlation one it becomes four.

These comparisons hold variances and weights fixed. Correlation changing together with volatility can produce a larger risk increase than this isolated calculation suggests.'''),
('Diversification depends on shared causes',r'''Two instruments with different names may load on the same interest-rate, volatility or market factor. A schematic model R_i=beta_i F+epsilon_i separates a common factor F from residual components. Under uncorrelated factor and residuals, the portfolio's factor contribution is (sum of w_i beta_i)F.

Adding more positions does not necessarily reduce that shared loading. If all beta_i have the same sign, the common exposure can persist while independent residual noise averages away.

Explain what economic or statistical event could make the positions move together. Historical pairwise correlation is a summary of past joint variation, not a promise that dependencies stay fixed during stress.'''),
('Stress the inputs and constraints',r'''A covariance estimate has sampling error and may change with the regime. Recalculate portfolio behaviour under larger volatilities, stronger positive correlations and concentrated common shocks. Check whether the assumed covariance matrix is mathematically valid: every weighted variance must be nonnegative.

A capital limit, exposure cap or liquidity requirement is a constraint on permitted actions, not just a term inside expected profit. A trade with positive expected edge may breach a limit or be impossible to exit at the assumed size.

Stress scenarios are explicit alternatives, not forecasts with automatically known probabilities. Report which inputs moved, what stayed fixed and which constraint becomes binding.'''),
('Variance does not specify the tail',r'''Two payoff distributions can have the same mean and variance but different probabilities of severe loss. A normal approximation may miss jumps or a mixture with rare large negative outcomes. State the distributional assumption before turning a standard deviation into a tail-loss probability.

Even a numerical quantile does not describe how bad losses beyond it can be. Liquidity can also disappear in precisely the state when reducing exposure is most valuable.

Ask about downside magnitude, timing, financing and feasible exits separately. No single variance estimate answers every risk question, and a narrow confidence interval for a mean does not guarantee a harmless payoff distribution.'''),
('Hedges leave model and nonlinear risk',r'''Offsetting a linear factor loading can reduce first-order exposure, but estimated hedge coefficients can be wrong and change over time. Nonlinear instruments also have curvature and sensitivity to other state variables.

A delta-neutral option position, for example, removes a local first derivative with respect to the underlying at the current state. It can retain gamma, volatility and time exposure. A hedge that is neutral now may not remain so after a price move.

A strong interview answer computes the specified combined risk, identifies what the model omits and tests the conclusion under changed assumptions. It does not call a portfolio safe merely because it contains many positions or has a positive mean.''')],
r'''For the equal-weight, variance-four pair, covariance two gives variance three. If correlation rises from 0.5 to one while individual standard deviations also rise from two to three, the new covariance is nine and the portfolio variance is (1/4)9+(1/4)9+(1/2)9=9. Standard deviation rises from sqrt(3) to three. Merely changing correlation at the old volatility would have predicted variance four and understated this joint stress. This is a scenario calculation, not an estimated probability that the scenario will occur.''')

add('l23',25,
'Use payoff identities and local derivatives to understand the mathematical-finance essentials. Keep exercise style, financing and the meaning of each sensitivity explicit.',
['Derive European put-call parity from terminal payoffs.','Interpret delta, gamma and theta with correct variables and units.','Explain why local neutrality does not remove all risk.'],[
('Write the terminal payoff first',r'''A European call with strike K and maturity T pays max(S_T-K,0), where S_T is the underlying price at maturity. A European put with the same strike and maturity pays max(K-S_T,0). European exercise means the payoff is determined at maturity; early exercise is not an available action.

Subtracting put payoff from call payoff gives S_T-K in both cases: if S_T≥K, the call contributes S_T-K and the put zero; if S_T<K, the call is zero and subtracting the put gives -(K-S_T).

This identity is exact at maturity. It is not an approximation and does not require knowing a volatility or a probability distribution.'''),
('Replicate the difference today',r'''Assume a non-dividend-paying underlying, a constant continuously compounded risk-free rate r, and frictionless trading with borrowing, lending and shorting available. Holding one unit of underlying and borrowing \(Ke^{-rT}\) today produces terminal value S_T-K, because the debt grows to K.

The call-minus-put portfolio has the same terminal payoff, so no-arbitrage implies
\[C-P=S_0-Ke^{-rT}.\]
Here C and P are current option prices and S_0 is the current underlying price. If equal payoffs had different prices under these assumptions, buying the cheaper portfolio and selling the more expensive one would create a price discrepancy with offsetting terminal payoffs.

Costs and trading constraints can prevent the idealised arbitrage trade. State them before interpreting a small observed discrepancy.'''),
('Check the assumptions and direction',r'''At S_0=100, K=100 and r=0, parity gives C-P=0. It states that call and put prices are equal for this setup, not that both options cost zero. Each can have positive value because its payoff is nonnegative and uncertain.

A known dividend changes the underlying replication's cash flows. American exercise introduces an early-exercise right, so the same European equality cannot simply be reused. Different strikes or maturities also destroy the matched payoff identity.

For an interview, derive the two terminal cases first. Then identify the portfolio replicating their difference and discount the deterministic debt. This is more robust than recalling a formula with an uncertain sign.'''),
('Define local sensitivities',r'''Let V(S,t) be the current value of a smooth instrument as a function of underlying price S and calendar time t, holding other model inputs fixed. Define delta as \(\Delta=\partial V/\partial S\), gamma as \(\Gamma=\partial^2V/\partial S^2\), and theta as \(\Theta=\partial V/\partial t\).

Delta describes the local linear response to price. Gamma describes the change in that slope as price changes. Theta describes the response to passing calendar time with the other inputs held fixed.

If a model instead uses time remaining tau=T-t, its derivative with respect to tau has the opposite sign to calendar-time theta. Specify which clock you differentiate before assigning a sign.'''),
('Use a Taylor expansion carefully',r'''For small changes, a common approximation keeps second order in price and first order in time:
\[\delta V\approx\Delta\,\delta S+\tfrac12\Gamma(\delta S)^2+\Theta\,\delta t.\]
This deliberately drops higher price terms, time curvature and cross terms. It is not an exact full second-order expansion in every variable. Volatility and rate changes require additional sensitivities when they occur.

At delta zero, gamma 0.08 and a price move of five, with no time or other input change, the retained gamma term is (1/2)×0.08×25=1. Reversing the sign of the price move leaves that term unchanged because it is squared.'''),
('Neutrality is local and variable-specific',r'''Delta-neutral means the combined first derivative with respect to S is zero at the current state. It does not make gamma zero, remove time exposure or fix the response to volatility. After S changes, delta itself generally changes approximately by gamma times the price move.

A finite move can also make the Taylor approximation inaccurate, especially near a discontinuity or when omitted derivatives are large. Compare with full model repricing when available, and identify the step size over which the approximation is reasonable.

Greeks depend on the pricing model and its state inputs. A derivative calculated correctly inside a misspecified model can still misdescribe realised exposure.'''),
('Check units, net positions and payoff logic',r'''For an option value measured in currency and an underlying price in currency per unit, delta has units of underlying quantity, and gamma has units that make gamma times squared price change a currency amount. Theta must match the time unit: a per-year theta cannot be multiplied directly by a number of days.

Sum sensitivities across positions with their signed quantities before calling the portfolio neutral. Buying and selling identical contracts offset exposures; different strikes or maturities can offset one derivative while retaining others.

The small core is payoff replication plus explicit local approximations. These tools help you reason about a changed contract or assumption without memorising product trivia.''')],
r'''Suppose a portfolio has delta 0.4, gamma 0.08 and theta -0.2 per day. For an underlying increase of five over one day, holding other inputs fixed, the retained approximation is 0.4×5+(1/2)×0.08×25-0.2×1=2.8. For a decrease of five it is -2+1-0.2=-1.2. The gamma contribution is one in both directions; the delta contribution changes sign. These are approximate value changes using sensitivities at the initial state, not guaranteed realised profits.''')

add('l24',25,
'Condition on the other side’s decision, and evaluate forecasts with a loss that matches the task. Winning, confidence and numerical precision can each hide a selection problem.',
['Explain the information in winning a common-value auction.','Derive the expected Brier score and distinguish calibration from sharpness.','Choose meaningful error measures for positive quantities.'],[
('Common value and private value differ',r'''In a common-value auction, the eventual object value V is shared across bidders but initially uncertain. Each bidder receives a noisy private signal about it. The highest estimate can win partly because it contains an unusually favourable error.

In a private-value model, bidders instead have their own values for the object. Other bidders' low valuations do not necessarily mean your own consumption value is low. Strategic bidding still matters, but the information problem differs.

Specify which model applies, what signals reveal, how bids relate to signals, and the auction format. There is no single correct bid formula for every auction or every noisy estimate.'''),
('Winning is an additional observation',r'''Suppose m≥2 bidders observe signals s_i=V+epsilon_i, where the noises are independent of V and of each other, have a continuous cumulative distribution F, and higher signals lead to higher bids. Ignore reserves and ties. Conditional on your signal s and value v, you win when all other noises are below s-v.

Consequently,
\[P(\text{win}\mid V=v,s_i=s)=F(s-v)^{m-1}.\]
For a fixed s, this likelihood decreases as v increases. A high true value would make the other bidders' signals high too, making it less likely that your observed s beats all of them.

Conditioning on your signal alone omits this information from the winning event.'''),
('Write the posterior correction',r'''When the prior and noise have densities, the posterior after observing signal s and winning is proportional to
\[f_V(v)f_\varepsilon(s-v)F(s-v)^{m-1}.\]
The first two factors describe inference from your signal alone. The extra winning factor gives relatively more weight to smaller common values under this model. Normalise the product before taking its expected value.

This explains the winner's-curse correction: evaluate value conditional on both your signal and winning, rather than bidding from the signal-only estimate. It does not by itself solve strategic equilibrium bidding. Payment rules, competitors' strategies and your objective are additional parts of that problem.'''),
('Forecast probabilities rather than certainty',r'''A probability forecast p describes an uncertain binary outcome Y∈{0,1}. A forecast of 0.7 does not mean each event will succeed or that an observed failure proves the forecast wrong. Over many comparable events with that forecast, a calibrated forecaster should see a success rate near 0.7, allowing for sampling variability.

Calibration compares predicted probabilities with observed frequencies. It is different from sharpness: how much forecasts vary away from the base rate. A constant base-rate forecast may be calibrated while failing to distinguish easier from harder cases.

Assess groups of forecasts with sufficient data, a defined population and honest evaluation timestamps. Repeated outcomes about the same event do not create independent calibration observations.'''),
('Derive the Brier score',r'''For one binary outcome, the Brier loss is (p-Y)². For n forecasts, the score is their average loss; lower is better. If the true conditional success probability is q, expected loss is
\[q(1-p)^2+(1-q)p^2=(p-q)^2+q(1-q).\]
The second term is irreducible uncertainty at that information set. The first is minimised by reporting p=q. Thus this loss rewards an honest probability under the model rather than an artificially confident zero or one.

This expectation result does not say the honest forecast beats every other forecast on every realised event. A single realised outcome can make an overconfident lucky prediction look better.'''),
('Evaluate out of sample with the right context',r'''Suppose ten comparable forecasts are all 0.7 and seven outcomes succeed. Each success contributes 0.09 and each failure 0.49, so the average Brier score is (7×0.09+3×0.49)/10=0.21.

That group matches the advertised frequency exactly, but ten events are too few to establish precise long-run calibration. Compare with a meaningful base-rate forecast and evaluate on data not used to adjust probabilities. If the sample base rate is estimated from those same ten outcomes, recognise that this baseline used evaluation information.

A score aggregates performance. Inspect reliability by probability range and whether the forecasts distinguish subgroups without selecting favourable bins after looking at the outcomes.'''),
('Use an error scale that matches the quantity',r'''For a positive quantity y and positive estimate x, absolute log-ratio error |log(x/y)| treats multiplication by two and division by two symmetrically: both have error log(2). Ordinary absolute error gives very different penalties depending on the unit and magnitude.

This can suit order-of-magnitude estimates, but it is undefined at zero and penalises near-zero values strongly. Choose the loss because of the task, not because it makes a chosen estimate look good. A range with stated assumptions is often more informative than a highly precise unsupported number.

Across auctions and forecasts, the recurring discipline is the same: identify the information used, model how observations were selected and score the conclusion with an explicit objective.''')],
r'''For a binary common value V∈{0,100} with equal prior weights, imagine your signal has equal likelihood under both values. Before considering the win, your posterior is still one half each. Suppose the probability of winning conditional on that signal is 0.8 when V=0 and 0.2 when V=100. After winning, the unnormalised weights are 0.4 and 0.1, so the high-value posterior is 0.1/0.5=0.2 and conditional expected value is 20. This deliberately specified likelihood example shows why a signal-only value of 50 can be too high. Computing an actual bid also requires the auction's payment and strategic rules.''')
