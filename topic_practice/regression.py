"""Regression practice: projection, identification and exact deletion errors.

These are original exercises. Expected coding outputs are independently checked
by centered, per-deletion rational refits in test_regression_practice.py.
"""


def add_questions(add, questions):
    rubrics = {
        'q19': ['Derive covariance two and observed predictor variance four under the stated independence assumptions.',
                'Obtain the population slope 1/2 and explain which latent coefficient it differs from.',
                'When measurement and response noise covary, include that covariance in the numerator rather than assuming attenuation.'],
        'q21': ['Differentiate with respect to the unpenalized intercept to derive the zero residual sum.',
                'Identify the intercept column in the normal equations and explain why removing it removes that constraint.',
                'Separate an in-sample stationarity identity from unbiased predictions on future data.'],
        'q30': ['Derive (XᵀX+λI)β=Xᵀy from the stated penalty on every coefficient.',
                'Use eigen-directions to explain shrinkage when the ordinary least-squares coefficients are identified.',
                'Explain why changing feature units changes the stated coefficient penalty and motivates consistent scaling.'],
    }
    for q in questions:
        if q['id'] in rubrics:
            q['rubric'] = rubrics[q['id']]

    def question(suffix, title, level, minutes, prompt, answer, hints, solution, follow, follow_solution, rubric):
        add(f'q_l11_{suffix}', title, 'Regression', level, 'researcher', minutes,
            prompt, answer, hints, solution, follow, follow_solution, 'l11')
        questions[-1]['rubric'] = rubric
        for key in ('prompt', 'solution', 'followSolution'):
            questions[-1][key] = questions[-1][key].replace(r'\n\n', '\n\n')

    question('e1', 'A population slope is a covariance ratio', 'Easy', 6,
        r'Random variables W and Y have finite second moments, with E[W]=2, E[Y]=5, Var(W)=4 and Cov(W,Y)=6. Choose real a,b to minimize the POPULATION mean squared error \(E[(Y-a-bW)^2]\). What is the optimal slope b? An intercept is fitted; no causal or conditional-mean model is assumed.', 1.5,
        ['First optimize the intercept for a fixed slope.', 'Centering leaves a quadratic with cross term −2b Cov(W,Y).'],
        r'For fixed b, the optimal intercept is \(a=E[Y]-bE[W]\). The remaining error is \(\operatorname{Var}(Y)-2b\operatorname{Cov}(W,Y)+b^2\operatorname{Var}(W)\). Its derivative vanishes at b=6/4=3/2, and a=5−(3/2)·2=2. Positive predictor variance makes this quadratic strictly convex in b. These are coefficients of the best LINEAR prediction; the conditional mean need not itself be linear, and an association is not an intervention effect.',
        r'If Var(Y)=13 as well, find the minimum mean squared error. Why would forcing a=0 generally change the slope?',
        r'The minimum error is \(13-6^2/4=4\). Without an intercept the derivative gives \(b=E[WY]/E[W^2]\), rather than the centered ratio. Here E[WY]=6+2·5=16 and E[W²]=4+2²=8, so b=2. Its error is E[Y²]−E[WY]²/E[W²]=38−256/8=6. An intercept allows the mean level and the slope to be fitted separately.',
        ['Center both variables after optimizing the intercept.', 'Derive b=3/2 and a=2 from the population moments.', 'Compute the minimum error and distinguish linear prediction from a causal or conditional-mean claim.'])

    question('e2', 'A changed unit changes the coefficient', 'Easy', 6,
        r'An ordinary least-squares fit with a free intercept gives \(\widehat Y=0.5+1.5X\) for observations X=[0,1,2], Y=[1,1,4]. Report the predictor instead as W=10X+20. Keeping EXACTLY the same fitted predictions, write \(\widehat Y=a^{\prime}+b^{\prime}W\). What is the new slope?', .15,
        ['Solve the change of coordinates for X.', 'A changed label on the predictor must not change the predictions.'],
        r'Substitute X=(W−20)/10: \(\widehat Y=0.5+0.15(W-20)=-2.5+0.15W\). Thus b′=0.15 and a′=−2.5. Both lines give predictions [0.5,2,3.5]. The coefficient value changes with the unit, while the fitted quantity and its residuals stay identical.',
        r'Now fit ridge regression with objective SSE+λb², where λ>0 and the intercept is UNPENALIZED. After the same change W=10X+20, what λ′ preserves the entire objective and hence the physical predictions? What happens if λ is kept unchanged?',
        r'Because b′=b/10, the same penalty needs \(\lambda^{\prime}(b^{\prime})^2=\lambda b^2\), so λ′=100λ. The free intercept absorbs the shift of twenty. Keeping λ unchanged divides the physical slope penalty by 100; it generally changes the fitted predictions. This argument concerns a penalty on the slope only. Penalizing the intercept would make the shift matter as well. Scaling learned from data also belongs inside the training procedure, not on a held-out record.',
        ['Transform the slope and intercept together and verify unchanged predictions.', 'Give slope 0.15 and intercept −2.5.', 'Derive λ′=100λ for a slope-only penalty and explain the free-intercept assumption.'])

    question('m1', 'Orthogonal residuals do not remove confounding', 'Medium', 16,
        r'Let U,V be independent centered random variables with variance one. Interpret the following equations as a CAUSAL GENERATOR: \(X=U+V\), \(Y=X+2U\). An intervention on X replaces its first equation while leaving U and the equation for Y unchanged.\n\nDerive the population least-squares slope of Y on X with a free intercept and its residual. Show that the residual is uncorrelated with X. Compare this observational slope with the change in Y caused by increasing X by one under the stated intervention. Does residual orthogonality resolve the discrepancy?', None,
        ['In observed data Y=3U+V, but an intervention uses the stated structural equation.', 'Compute Cov(X,Y) and Var(X) before forming the slope.', 'Orthogonality is a property of the fitted projection, not a test for an unconfounded causal generator.'],
        r'Means are zero, Var(X)=2 and Cov(X,Y)=Cov(U+V,3U+V)=4. The fitted intercept is zero and slope is 2. The residual is \(r=Y-2X=U-V\), so Cov(X,r)=Var(U)−Var(V)=0. Nevertheless the structural equation Y=X+2U gives an intervention effect of ONE when U is held fixed. The observational coefficient contains the association between X and U: Cov(X,2U)/Var(X)=1 in addition to the direct coefficient one. Least squares made the residual orthogonal by choosing its coefficient; it did not remove the common cause. No Gaussian assumption was needed so far.',
        r'Additionally suppose U,V are independent standard Gaussian variables. Construct another causal generator with exactly the SAME observed joint distribution of (X,Y), but with intervention effect two. Explain why matching only a slope would have been a weaker argument.',
        r'In the first generator, X=U+V and η=U−V are jointly Gaussian with zero covariance, so they are independent; each has variance two. The alternative generator draws independent X,η with distributions N(0,2) and sets Y=2X+η. It has the same centered Gaussian observed law, with Var(X)=2, Cov(X,Y)=4 and Var(Y)=10, but its intervention effect is two. Thus even the complete observed law, not merely its fitted slope, fails to choose between these two causal explanations. Zero covariance alone would not imply independence without the Gaussian assumption.',
        ['Derive the observed slope two and residual U−V.', 'Show Cov(X,r)=0 explicitly and derive intervention effect one from the specified generator.', 'Give the Gaussian alternative with the same full observed law and explain its different intervention effect.'])

    question('h1', 'Two noisy views can identify a latent slope', 'Hard', 28,
        r'All variables below are centered and have finite second moments. A latent variable Z has variance s>0. Observed measurements and response obey \(W_1=Z+u_1\), \(W_2=Z+u_2\), \(Y=\beta Z+\varepsilon\). Z is uncorrelated with u₁,u₂,ε. Assume Cov(u₁,u₂)=0 and Cov(u₂,ε)=0, but allow Cov(u₁,ε) to be nonzero.\n\nUsing only observable population covariances, identify β and prove why the denominator is nonzero. Compare your result with the population ordinary least-squares slope on W₁. Explain which assumptions made the second measurement useful; do not assume full independence or claim that a sample ratio is unbiased.', None,
        ['Cross the response with the measurement whose noise is uncorrelated with response noise.', 'The cross-covariance of the two measurements isolates the latent variance.', 'The first measurement may have both a variance inflation and a response-noise covariance.'],
        r'The restrictions give Cov(W₂,Y)=βs and Cov(W₂,W₁)=s, so\n\n\[\beta=\frac{\operatorname{Cov}(W_2,Y)}{\operatorname{Cov}(W_2,W_1)}.\]\n\nThe denominator is positive by s>0. In contrast, the ordinary slope on W₁ is \(\{\beta s+\operatorname{Cov}(u_1,\varepsilon)\}/\{s+\operatorname{Var}(u_1)\}\); it need not equal β or even exhibit attenuation. W₂ acts as an instrument for W₁ in this specified measurement model: it shares the latent variation but its error contributes neither to the cross-measurement moment nor to the cross-response moment. Only the stated covariance restrictions were used. Identification here is of a latent slope within that model, not an established causal effect. Replacing population moments by sample moments produces a ratio, not automatically an unbiased finite-sample estimator; a small empirical denominator can be unstable.',
        r'Drop ONLY Cov(u₁,u₂)=0, keeping all other restrictions. Construct two centered joint Gaussian latent models with different β and exactly the same FULL observed law of (W₁,W₂,Y). Use observed covariance [[2,1,1],[1,2,1],[1,1,2]], and verify each variance and cross-covariance. Why does this prove more than saying the ratio now has an extra term?',
        r'Model A has s=1, β=1, mutually independent Z,u₁,u₂,ε of variance one. It gives the displayed observed covariance. Model B has s=3/4, β=4/3, Var(u₁)=Var(u₂)=5/4, Cov(u₁,u₂)=1/4 and Var(ε)=2/3. Z, the error pair and ε are independent Gaussian blocks. The error covariance is positive definite: its eigenvalues are 3/2 and 1. For example, u₁=H/2+E₁ and u₂=H/2+E₂, with independent standard Gaussian H,E₁,E₂, constructs it.\n\nModel B gives measurement variances 3/4+5/4=2, their covariance 3/4+1/4=1, response cross-covariances βs=1, and response variance \((4/3)^2(3/4)+2/3=2\). Both observed vectors are centered jointly Gaussian with identical covariance, hence identical joint distributions, while β is respectively one and 4/3. All retained covariance restrictions hold. The observable ratio is one for both, and no amount of observing this same law distinguishes the latent slopes. This is an explicit nonidentification proof, not just failure of a particular estimator.',
        ['Derive both cross-moments and the nonzero denominator from the exact restrictions.', 'Compare with ordinary least squares, including Cov(u₁,ε), without adding independence.', 'Separate population identification from finite-sample ratio behavior and causal claims.', 'Verify two feasible Gaussian models with the same complete observed law and different latent slopes.'])

    question('h2', 'One training fit encodes every deletion error', 'Hard', 30,
        r'A fixed real design matrix X has n rows and p columns and FULL COLUMN RANK. In ordinary unweighted least squares, set \(M=X^TX\), \(\widehat\beta=M^{-1}X^Ty\), \(H=XM^{-1}X^T\). Let xᵢ be the column vector representing row i, \(h_i=x_i^TM^{-1}x_i\), and \(r_i=y_i-x_i^T\widehat\beta\).\n\nDerive the prediction error at row i when the fit is trained on every OTHER row. Express it using rᵢ and hᵢ when hᵢ<1. Justify this condition, and show precisely why hᵢ=1 does not mean a zero held-out error even though rᵢ=0 in the full fit. Do not silently assume every deleted design still has full rank.', None,
        ['Deletion subtracts xᵢxᵢᵀ from M and xᵢyᵢ from the right-hand side.', 'Try a coefficient correction in direction M⁻¹xᵢ.', 'At hᵢ=1 that direction becomes a null vector of the deleted normal matrix.'],
        r'H is an orthogonal projection, so 0≤hᵢ≤1. Put z=M⁻¹xᵢ. For hᵢ<1, the rank-one inverse identity or direct substitution gives\n\n\[\widehat\beta^{(-i)}=\widehat\beta-\frac{z r_i}{1-h_i}.\]\n\nIndeed the deleted normal matrix is M−xᵢxᵢᵀ, and (M−xᵢxᵢᵀ)z=xᵢ(1−hᵢ); substituting the correction leaves exactly Xᵀy−xᵢyᵢ. Its inverse exists when 1−hᵢ>0. The held-out error is therefore\n\n\[y_i-x_i^T\widehat\beta^{(-i)}=r_i+\frac{h_i r_i}{1-h_i}=\frac{r_i}{1-h_i}.\]\n\nIf hᵢ=1, z is a nonzero null vector of the deleted matrix and xᵢᵀz=1. Since that matrix is the Gram matrix of the remaining rows, those rows annihilate z. Adding any multiple of z to a deleted-fit minimizer changes no remaining fitted value but changes the held-out prediction arbitrarily. It is not identified without an extra fitting convention. Meanwhile \(\|(I-H)e_i\|^2=1-h_i=0\), where eᵢ is a coordinate vector, so the full-fit residual at i is zero for every y. The apparent 0/0 is not an error of zero. Summing squared valid deletion errors gives the fixed-procedure leave-one-out score; the small training residual alone hides leverage.',
        r'Now X includes an intercept column of ones and ridge penalizes every other coefficient, with FIXED λ>0 and no penalty on the intercept. Set \(M=X^TX+\operatorname{diag}(0,\lambda,\ldots,\lambda)\). Does the same deletion formula apply if features are redundant? When is its denominator positive? What changes if preprocessing or λ selection uses the held-out observation?',
        r'For any nonempty training set, vᵀMv is the sum of squared fitted linear values plus λ times squared slope coefficients. A nonzero slope vector makes the penalty positive; a pure nonzero intercept gives a positive data term. Thus M is positive definite even with redundant features. For n≥2 the deleted training set is also nonempty and positive definite. The determinant identity \(\det(M-x_ix_i^T)=\det(M)(1-h_i)\) makes 1−hᵢ positive, and the same coefficient substitution proves the deletion formula. The ridge smoother H need not be an idempotent projection; the algebra uses a fixed quadratic penalty, not projection idempotence. For n=1, deletion leaves an unpenalized intercept with no data, so the held-out prediction is again unidentified. A λ or feature transform learned using the held-out row changes the procedure: this formula alone does not undo that information use. Fix such ingredients in advance, or refit their training-only selection inside each deletion; choosing λ by the same score also creates a separate model-selection assessment issue.',
        ['Derive the rank-one coefficient correction and residual rᵢ/(1−hᵢ).', 'Use the projection bound and explain rank loss, null directions and unidentified predictions at leverage one.', 'Prove positive definiteness for slope-only ridge on nonempty data and positivity after deletion for n≥2.', 'Keep penalty and preprocessing fixed and separate deletion identities from an independent model-selection evaluation.'])


def add_coding(add, tasks):
    def exercise(level, title, prompt, signature, samples, tests, solution, explanation):
        add(f'c_l11_{level.lower()}', title, level, 'Regression', prompt, signature,
            samples, tests, solution, explanation)
        tasks[-1]['path'] = 'researcher'
        for key in ('prompt', 'explanation'):
            tasks[-1][key] = tasks[-1][key].replace(r'\n\n', '\n\n')

    exercise('Easy', 'Check a proposed least-squares fit',
        r'x and y are equally sized INTEGER lists of length 0≤n≤100000. Entries and the INTEGER parameters intercept,slope have absolute value at most 10^6. Return True exactly when the proposed line intercept+slope*x[i] globally minimizes the sum of squared residuals among ALL real intercepts and slopes. Nonunique coefficients are allowed: a constant predictor still has optimal fitted values. With no observations every proposed line is optimal.\n\nUse exact integer arithmetic, O(n) time and O(1) auxiliary state. Do not mutate either input, use a floating tolerance, or require an invertible design. This task verifies a proposed minimizer; it does not request unique coefficients as the separate OLS exercise does.',
        'def solve(x, y, intercept, slope):',
        [{'args': [[0,1,2],[1,3,5],1,2], 'expected': True},
         {'args': [[0,1,2],[1,3,5],3,0], 'expected': False}],
        [{'args': [[],[],7,8], 'expected': True},
         {'args': [[7,7],[2,4],3,0], 'expected': True},
         {'args': [[7,7],[2,4],-11,2], 'expected': True},
         {'args': [[7,7],[2,4],3,1], 'expected': False},
         {'args': [[0,1,2],[1,1,4],1,1], 'expected': False},
         {'args': [[-9],[4],-14,-2], 'expected': True},
         {'args': [[-9],[4],4,1], 'expected': False},
         {'args': [[-10**6,10**6],[-10**6,10**6],0,1], 'expected': True},
         {'args': [[10**6]*10000,[10**6]*10000,10**6,0], 'expected': True}],
        '''def solve(x, y, intercept, slope):
    residual_sum = 0
    cross_sum = 0
    for a, b in zip(x, y):
        residual = b - intercept - slope * a
        residual_sum += residual
        cross_sum += a * residual
    return residual_sum == 0 and cross_sum == 0''',
        r'For a free intercept and slope, stationarity requires \(\sum_i r_i=0\) and \(\sum_i x_i r_i=0\). These conditions are also sufficient, even if the design is rank deficient. For any parameter perturbation δa,δb, expand its SSE change as \(-2\delta a\sum_i r_i-2\delta b\sum_i x_i r_i+\sum_i(\delta a+\delta b x_i)^2\). When both sums vanish it is nonnegative. Conversely a nonzero gradient admits a decreasing small perturbation. Check both sums in one pass. Mean residual zero alone misses a wrong slope. A constant predictor can have many minimizing parameter pairs, and empty data makes both sums zero. Exact integer accumulation avoids rounding a small nonzero stationarity error away.')

    # General small fixtures are inserted by an independent centered-refit oracle,
    # not by running the reference below. Long intercept-only errors are analytic.
    hard_cases = [
        {'args': [[],[],1], 'expected': []},
        {'args': [[[9]],[4],1], 'expected': [None]},
        {'args': [[[7],[7],[7]],[2,4,9],3], 'expected': [['-9','2'],['-3','2'],['6','1']]},
        {'args': [[[-10**6],[10**6]],[-10**6,10**6],1], 'expected': [['-2000000','1'],['2000000','1']]},
        {'args': [[[],[],[]],[0,3,6],5], 'expected': [['-9','2'],['0','1'],['9','2']]},
    ]
    # Additional varied dimensions and exact large fractions are authored below.
    hard_cases.extend(EXACT_REFIT_CASES)
    n = 6000
    hard_cases.append({'args': [[[] for _ in range(n)], [i % 3 - 1 for i in range(n)], 1],
                       'expected': [[str(n * (i % 3 - 1)), str(n-1)] if i % 3 != 1 else ['0','1'] for i in range(n)]})

    exercise('Hard', 'Compute every ridge deletion error in one fit',
        r'features is a rectangular n×d INTEGER matrix, where 0≤n≤10000 and 0≤d≤6; targets is an integer list of length n. All entries have absolute value at most 10^6. ridge is an integer λ with 1≤λ≤10^9. For each row i, fit the OTHER rows by minimizing\n\n\[\sum_{j\ne i}(y_j-a-b^Tf_j)^2+\lambda\sum_{k=1}^d b_k^2.\]\n\nThe intercept a is UNPENALIZED. λ and the raw feature coordinates stay fixed across all deletions: do not divide λ by training size or learn a full-data scaler. Return the held-out residual yᵢ−a−bᵀfᵢ for every original row, in original order. Encode each exact result as a reduced pair [numerator_text,denominator_text] of canonical base-ten STRINGS: signed numerator, positive denominator, gcd=1, no leading zeroes or plus sign. Zero is ["0","1"]. Large rational components exceed exact browser numeric range, so do not return floats or numeric pairs.\n\nFor n=0 return []; for n=1 return [None], since deleting the only observation leaves an unidentified unpenalized intercept. For n≥2 every deleted prediction is unique, even with constant or redundant features. Empty feature rows mean an intercept-only fit. Do not mutate inputs.\n\nUse one full-data fit and its diagonal leverages: O(n(d+1)²+(d+1)³) scalar arithmetic and O((d+1)²) working storage beyond the returned list. Integer bit and gcd costs are additional. Refitting once per observation is too slow. Python integer arithmetic and math.gcd suffice; no external matrix library is needed. The editorial explains an exact fraction-free computation, avoiding cancellation when leverage is almost one.',
        'def solve(features, targets, ridge):',
        [{'args': [[[0],[1],[2]],[1,1,4],1], 'expected': [['0','1'],['-3','2'],['3','1']]},
         {'args': [[[],[],[]],[0,3,6],5], 'expected': [['-9','2'],['0','1'],['9','2']]}],
        hard_cases,
        '''from math import gcd
def solve(features, targets, ridge):
    n = len(targets)
    if n == 0:
        return []
    if n == 1:
        return [None]
    width = len(features[0]) + 1
    matrix = [[0] * width for _ in range(width)]
    rhs = [0] * width
    for features_i, target in zip(features, targets):
        row = [1] + features_i
        for j in range(width):
            rhs[j] += row[j] * target
            for k in range(width):
                matrix[j][k] += row[j] * row[k]
    for j in range(1, width):
        matrix[j][j] += ridge
    rows = [matrix[j] + [int(j == k) for k in range(width)] for j in range(width)]
    previous = 1
    for column in range(width):
        pivot = rows[column][column]
        for i in range(width):
            if i == column:
                continue
            factor = rows[i][column]
            for j in range(2 * width):
                if j != column:
                    rows[i][j] = (pivot * rows[i][j] - factor * rows[column][j]) // previous
            rows[i][column] = 0
        previous = pivot
    determinant = rows[0][0]
    adjugate = [row[width:] for row in rows]
    coefficients = [sum(a * b for a, b in zip(row, rhs)) for row in adjugate]
    result = []
    for features_i, target in zip(features, targets):
        row = [1] + features_i
        fitted = sum(a * b for a, b in zip(row, coefficients))
        leverage = sum(row[j] * adjugate[j][k] * row[k] for j in range(width) for k in range(width))
        numerator = determinant * target - fitted
        denominator = determinant - leverage
        divisor = gcd(abs(numerator), denominator)
        result.append([str(numerator // divisor), str(denominator // divisor)])
    return result''',
        r'Augment each feature row to xᵢ=(1,fᵢᵀ)ᵀ. Let P=diag(0,λ,…,λ), M=Σxᵢxᵢᵀ+P and g=Σxᵢyᵢ. M is positive definite on nonempty data: nonzero slopes pay a positive penalty, and a pure nonzero intercept has positive data loss. For n≥2 this remains true after any deletion, including duplicate features.\n\nThe deleted equations subtract xᵢxᵢᵀ and xᵢyᵢ. If β=M⁻¹g and hᵢ=xᵢᵀM⁻¹xᵢ, substituting \(\beta^{(-i)}=\beta-M^{-1}x_i r_i/(1-h_i)\) gives the exact deleted fit. Its error is rᵢ/(1−hᵢ). The positive deleted determinant implies 1−hᵢ>0; subtracting floating numbers near one can nevertheless destroy its value.\n\nWork with integer determinant D and adjugate A, so M⁻¹=A/D. The requested residual is\n\n\[\frac{D y_i-x_i^T A g}{D-x_i^T A x_i}.\]\n\nCompute D and A once by fraction-free Gauss–Jordan elimination on [M|I]. At pivot c, with p=current pivot and q=previous pivot (initially one), update each nonpivot row entry j≠c by (p·entry−row[c]·pivot_row[j])/q, then zero its pivot column. Leave the pivot row untouched during that step. Determinant identities make every division exact; positive leading principal minors ensure nonzero pivots for this M. At termination the left block is D·I and the right block is A. This is exact integer elimination, not a tolerance-based inverse. Multiply A by g once, compute each quadratic leverage numerator in O((d+1)²), and reduce its positive-denominator rational by gcd.\n\nFor intercept-only data the formula reduces to (n yᵢ−Σy)/(n−1), a useful independent check. With one remaining row the fitted slopes are zero and its intercept is that row’s target, even if full-data leverage was extremely close to one. n=1 instead leaves no remaining intercept information and returns None. Fixing λ and feature coordinates is part of the contract; the algebra removes the row’s fit contribution, but does not undo preprocessing or tuning that used it. Reading all rows for sufficient statistics and again for errors uses O(n(d+1)²+(d+1)³) scalar work and O((d+1)²) auxiliary state; exact integer and gcd bit costs are separate.')


# Filled from the independent per-deletion centered ridge oracle, then committed
# as deterministic judge fixtures. Keeping this separate makes provenance clear.
EXACT_REFIT_CASES = [{'args': [[[1, 1], [2, 2], [4, 4], [7, 7]], [3, -2, 5, 9], 1],
  'expected': [['461', '79'], ['-635', '111'], ['97', '127'], ['77', '31']]},
 {'args': [[[0, 2], [1, -1], [-4, 3], [2, 0], [3, 5]], [7, -3, 2, 9, -1], 13],
  'expected': [['31841', '5997'],
               ['-47821', '4341'],
               ['-1427', '587'],
               ['44547', '4937'],
               ['-22859', '2529']]},
 {'args': [[[0, 0, 0], [1, 2, 3], [3, 2, 1]], [4, -7, 9], 1000000000],
  'expected': [['3', '1'], ['-13500000102', '1000000007'], ['10500000090', '1000000007']]},
 {'args': [[[1000000, -999983], [999979, 999961], [-999959, 999953], [999931, -999917], [-999907, -999883]],
           [999979, -999961, 999959, -999953, 999931],
           1],
  'expected': [['31991600866849060407984401351945', '15995920399774124921136676'],
               ['-31989233381472824657554176972004', '31990672985557862625115795'],
               ['31994128400200636158293653771844', '31993072643920948597113691'],
               ['-95979985565997358314495725616460', '63988000832080525396071871'],
               ['-31991312920126694818181356591160', '31995168296779525675357171']]},
 {'args': [[[-3, 9, -27, 81, -243, 729],
            [-2, 4, -8, 16, -32, 64],
            [-1, 1, -1, 1, -1, 1],
            [0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1],
            [2, 4, 8, 16, 32, 64],
            [3, 9, 27, 81, 243, 729],
            [4, 16, 64, 256, 1024, 4096]],
           [11, -7, 9, -2, 13, 4, -9, 1],
           17],
  'expected': [['228435235560468115436', '3336829295220354967'],
               ['-379482862031379454724', '33197192273400406235'],
               ['2721511652035883538076', '408762383059543396327'],
               ['-4574742120308005558956', '387995042705751146647'],
               ['3548708587077584782332', '395021932835268802423'],
               ['-108193858492313853564', '354807126630701940967'],
               ['899242157847606524', '436479559322126099'],
               ['-30710455447670565204', '1361067684896670007']]}]
