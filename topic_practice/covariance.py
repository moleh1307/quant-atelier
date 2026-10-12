"""Covariance practice: collective feasibility and rank-aware optimisation.

Hard questions derive singular-block compatibility and the two branches of an
unrestricted unbiased combination. Exact coding works from a shared-factor Gram
model, so singular covariance is allowed rather than patched with a ridge.
"""


def add_questions(add, questions):
    old_rubrics = {
        'q20': ['Use collective PSD or residual Cauchy–Schwarz, rather than pairwise bounds alone.',
                'Derive the lower bound 0.28 and distinguish feasible singularity from invalidity.',
                'Give the explicit variance-one construction attaining the bound.'],
        'q29': ['Use common-target unbiasedness and independence in the variance expression.',
                'Derive weight 4/5 and the resulting variance 4/5.',
                'For dependent estimates, include covariance and check the difference-variance denominator and permitted weights.'],
    }
    for q in questions:
        if q['id'] in old_rubrics:q['rubric']=old_rubrics[q['id']]

    def question(suffix,title,level,minutes,prompt,answer,hints,solution,follow,follow_solution,rubric):
        add(f'q_l10_{suffix}',title,'Linear algebra',level,'researcher',minutes,
            prompt,answer,hints,solution,follow,follow_solution,'l10')
        questions[-1]['rubric']=rubric
        for key in ('prompt','solution','followSolution'):
            questions[-1][key]=questions[-1][key].replace(r'\n\n','\n\n')

    question('e1','The cross term has units and a sign','Easy',5,
        r'Random variables X and Y have finite second moments with \(\operatorname{Var}(X)=4\), \(\operatorname{Var}(Y)=9\) and \(\operatorname{Cov}(X,Y)=-3\). Coefficients are fixed real numbers. Compute \(\operatorname{Var}(X+2Y)\). Do not assume independence.',28,
        ['Expand the square of the centered linear combination.', 'The covariance term appears twice, and both coefficients multiply it.'],
        r'Centering removes the means. Expanding \([(X-E[X])+2(Y-E[Y])]^2\) gives \(4+4\cdot9+4(-3)=28\). The cross term is \(2ab\operatorname{Cov}(X,Y)\), not a second independent variance. The negative covariance reduces this combination’s variation. It is feasible: its correlation is \(-3/(2\cdot3)=-1/2\), within the two-variable bound.',
        r'Replace Y by Y′=10Y, a change of reported units. Which coefficients describe the SAME random combination, and what happens to the covariance and correlation?',
        r'The same combination is \(X+0.2Y^{\prime}\). Now \(\operatorname{Var}(Y^{\prime})=900\) and \(\operatorname{Cov}(X,Y^{\prime})=-30\); its variance remains \(4+0.04(900)+0.4(-30)=28\). Correlation remains −1/2 because the positive unit conversion also multiplies the standard deviation by ten. Keeping coefficient 2 would change the random quantity, rather than merely its units. A negative conversion would flip the correlation sign.',
        ['Include both fixed coefficients in the covariance cross term.',
         'Obtain variance 28 without replacing covariance by independence.',
         'Transform coefficients and covariance consistently when units change.'])

    question('e2','Zero variation does not mean zero level','Easy',5,
        r'X and Y have finite second moments, means 2 and 7, variances 9 each, and correlation one. What is \(\operatorname{Var}(X-Y)\)? Does the resulting conclusion imply X=Y almost surely?',0,
        ['Correlation one and standard deviations three give covariance nine.', 'A zero-variance random variable equals its own mean almost surely.'],
        r'Covariance is 9, so \(\operatorname{Var}(X-Y)=9+9-18=0\). Therefore \(X-Y=E[X-Y]=-5\) almost surely. The CENTERED variables coincide, but the raw levels differ by five. The covariance matrix is valid PSD and singular, not invertible. Its zero-variance direction describes an exact relationship rather than the absence of all randomness.',
        r'If the same means and variances hold but correlation is −1, what exact relationship replaces the difference? Is this independence?',
        r'Now covariance is −9, so \(\operatorname{Var}(X+Y)=0\) and \(X+Y=9\) almost surely. Neither perfect positive nor perfect negative correlation is independence here: independence with finite second moments would force covariance zero, whereas both variables have positive variance and nonzero covariance. No normal-distribution assumption was needed for these exact relationships.',
        ['Compute the zero variance from covariance nine.',
         'Identify X−Y=−5 rather than X=Y from the unequal means.',
         'Distinguish singular PSD structure and deterministic dependence from independence.'])

    question('m1','Every pair passed, but the table failed','Medium',15,
        r'A six-row dataset has columns (X,Y,Z). Missing entries are written None:\n\n(-1,-1,None), (1,1,None), (None,-1,-1), (None,1,1), (-1,None,1), (1,None,-1).\n\nA pipeline computes each Pearson correlation using only rows where THAT pair is observed, and sets all diagonal entries to one. Derive its reported matrix. Show by an explicit weighted variance that it cannot be a correlation matrix of one joint distribution. Explain how individually correct pair calculations produced this outcome.',None,
        ['Each pair has exactly two matching or opposite observations.', 'Try coefficients (1,−1,1). A joint variance cannot be negative.', 'The pairs used different observation subsets, not one centered sample matrix.'],
        r'The reported correlations are XY=1, YZ=1 and XZ=−1, so\n\n\[R=\begin{pmatrix}1&1&-1\\1&1&1\\-1&1&1\end{pmatrix}.\]\n\nFor \(w=(1,-1,1)^T\), its quadratic form is \(3-2-2-2=-3\). Hence R is not PSD and no joint finite-second-moment model has this correlation table. Each pair’s calculation is correct for its own two rows, but those different subsets do not produce the Gram matrix of one common centered record. There are no complete three-column rows here, so blindly switching to complete cases would leave no data. Report the missingness/sample convention and consider an explicitly justified joint model; per-cell plausibility is not collective feasibility.',
        r'An engineer blends the table toward the identity: \(R_\alpha=(1-\alpha)R+\alpha I\), with 0≤α≤1. Find the smallest α making it PSD, distinguish strict positive definiteness, and explain what this repair does NOT prove.',
        r'The vector w above is an eigenvector with eigenvalue −1; its perpendicular plane has eigenvalue 2. Thus the blended eigenvalues are \(-1+2\alpha\) and \(2-\alpha\) twice. PSD requires α≥1/2, and strict positive definiteness requires α>1/2 on the stated interval. At α=1/2 it is valid but singular. The repair gives a feasible approximation with the same diagonal, not evidence that the original pairwise table came from one jointly observed sample or that the missingness model is correct.',
        ['Derive all three pairwise correlations from the specified rows.',
         'Exhibit a negative quadratic form and explain the differing sample subsets.',
         'Derive the shrinkage threshold from all eigenvalue directions and separate repair from evidence.'])

    question('h1','A new variable cannot contradict a null direction','Hard',25,
        r'Centered predictors form a d-dimensional random vector U with KNOWN covariance B, a real symmetric PSD matrix that may be singular. A proposed additional centered variable T has variance v≥0 and covariance vector \(c=\operatorname{Cov}(U,T)\). Let \(B e_i=\lambda_i e_i\) in an orthonormal eigenbasis, with λᵢ≥0, and write \(c_i=e_i^Tc\).\n\nDerive necessary AND sufficient conditions on c and v for the block table \(\begin{pmatrix}B&c\\c^T&v\end{pmatrix}\) to be a covariance matrix. Prove necessity from weighted variances and sufficiency by constructing a joint model. Handle zero eigenvalues explicitly rather than substituting an ordinary inverse. Apply the result to B=[[1,1],[1,1]], c=(1,2): can an arbitrarily large finite v make it feasible?',None,
        ['A null predictor combination has zero variance and cannot covary with anything.',
         'For each positive eigenvalue, complete the square in its weighted direction.',
         'Independent centered variance-one variables can construct all positive eigen-directions and any remaining target noise.'],
        r'In eigen-coordinates, a predictor weight u and target coefficient t give\n\n\[Q(u,t)=\sum_i\lambda_i u_i^2+2t\sum_i c_i u_i+vt^2.\]\n\nIf λᵢ=0 but cᵢ≠0, choose t=1 and send uᵢ in the opposite sign direction: Q becomes negative without bound. Therefore every zero-eigenvalue coordinate must have cᵢ=0, equivalently c is orthogonal to the null space and lies in the range of B. Completing squares in the remaining directions then gives\n\n\[Q=\sum_{\lambda_i>0}\lambda_i\left(u_i+\frac{tc_i}{\lambda_i}\right)^2+t^2\left(v-\sum_{\lambda_i>0}\frac{c_i^2}{\lambda_i}\right).\]\n\nThus feasibility is exactly the range condition plus \(v\geq s=\sum_{\lambda_i>0}c_i^2/\lambda_i\). Empty sums are zero: B=0 forces c=0 and allows any v≥0. Necessity follows by choosing the square-minimising u; the same display shows PSD sufficiency.\n\nFor an actual joint construction, take independent zero-mean variance-one variables Zᵢ for positive eigenvalues and a further independent Z₀. Set \(U=\sum_{\lambda_i>0}\sqrt{\lambda_i}\,e_i Z_i\) and \(T=\sum_{\lambda_i>0}c_i Z_i/\sqrt{\lambda_i}+\sqrt{v-s}\,Z_0\). Independent symmetric ±1 variables suffice; normality is unnecessary. Their covariances are exactly B,c,v, including the equality case. In the specified example, the null vector (1,−1) has nonzero inner product −1 with c. No finite v repairs that contradiction.',
        r'What is the minimum v for the SAME B and c=(2,2)? For the inconsistent c=(1,2), explain quantitatively why replacing B by B+εI may hide the issue at fixed ε>0 but cannot recover a finite target variance as ε tends to zero.',
        r'For c=(2,2), the positive eigenvalue is 2 and its coordinate is 2√2, so s=4. Let U=(Y,Y) and T=2Y+√(v−4)Z with independent centered variance-one Y,Z; v≥4 works. For c=(1,2), its squared projection on the positive eigenvector is 9/2 and on the null eigenvector is 1/2. The regularised threshold becomes \(s_\varepsilon=\frac{9/2}{2+\varepsilon}+\frac{1/2}{\varepsilon}\), which diverges. At fixed ε, sufficiently large v is feasible for the CHANGED predictor covariance B+εI, not for B. The null-direction incompatibility cannot be cured by pretending an arbitrarily small ridge left the original model unchanged.',
        ['Derive the zero-eigenvalue range condition from a rejecting quadratic direction.',
         'Complete squares to obtain the exact residual-variance lower bound, with equality and B=0 handled.',
         'Construct variables proving sufficiency and reject c=(1,2) for every finite target variance.',
         'Compute the consistent threshold four and the divergent regularised null contribution.'])

    question('h2','Singularity can remove risk or merely duplicate it','Hard',30,
        r'd≥1 estimates Xᵢ have the SAME unknown mean µ and a KNOWN symmetric PSD error covariance Σ. Choose fixed real weights w with \(\mathbf1^Tw=1\); negative weights are allowed. The combined estimate is unbiased and has variance \(w^T\Sigma w\).\n\nCharacterise the minimum variance and all minimising weights, allowing singular Σ. Separate the case where some null vector z has \(\mathbf1^Tz\ne0\) from the case where every null vector has zero sum. Define any generalised inverse you use in an eigenbasis and prove the global lower bound, rather than only writing stationary equations. Explain why “replace inverse by pseudoinverse” alone can miss a zero-risk fit.',None,
        ['A zero-variance direction can be made unbiased only if its weight sum is nonzero.',
         'Otherwise the all-ones vector lies in the range of Σ; use Cauchy–Schwarz on its positive eigen-directions.',
         'Adding a null vector to an optimum leaves its variance unchanged, but check the weight sum.'],
        r'PSD makes zero variance equivalent to membership in the null space. If a null vector z has nonzero sum, \(w=z/(\mathbf1^Tz)\) is feasible with variance zero, the global lower bound. All minimisers are exactly null vectors whose sums equal one.\n\nOtherwise \(\mathbf1\) is orthogonal to the null space, hence in the range of the symmetric matrix. Define \(\Sigma^+=\sum_{\lambda_i>0}\lambda_i^{-1}e_i e_i^T\). Let \(s=\mathbf1^T\Sigma^+\mathbf1>0\). For positive eigen-directions define \(a_i=(e_i^T\mathbf1)/\sqrt{\lambda_i}\) and \(b_i=\sqrt{\lambda_i}(e_i^Tw)\). Every sum below runs only over λᵢ>0. Any feasible w satisfies\n\n\[\begin{aligned}1&=\left(\sum_i a_i b_i\right)^2\\&\leq\left(\sum_i a_i^2\right)\left(\sum_i b_i^2\right)\\&=s\,w^T\Sigma w.\end{aligned}\]\n\nThe minimum is 1/s. Equality holds precisely for positive-range weights \(w_0=\Sigma^+\mathbf1/s\); all minimisers are \(w_0+z\) with z in the null space. Such z has zero sum in this branch, so all these weights remain feasible. Positive definiteness makes the null space trivial and the optimiser unique. A singular matrix can still have positive minimum variance; an inverse fails, but the statistical problem need not fail.\n\nBlindly normalising Σ⁺1 without checking the first branch can miss feasible zero-risk weights, because the ones vector then has an informative null component. These claims use known covariance and fixed weights, not a promise that estimated covariance or fitted cancellation holds out of sample.',
        r'Compare Σ=[[1,2],[2,4]] with a d×d all-ones covariance matrix. For the first matrix, how does additionally requiring nonnegative weights change the answer?',
        r'The first matrix is aaᵀ with a=(1,2). Its null weight vector (2,−1) sums to one, so it gives zero variance. Nonnegative weights instead give exposure \(w_1+2w_2=2-w_1\) with 0≤w₁≤1; the smallest squared exposure is one, attained at (1,0). Allowing negative weights was consequential. In the all-ones matrix, every sum-one combination has variance \((\sum_iw_i)^2=1\). Null vectors have zero sum and cannot remove the common noise; the pseudoinverse branch gives s=1. Singularity in these two examples has different consequences.',
        ['Separate the null-space nonzero-sum zero-risk branch from the range branch.',
         'Define the pseudoinverse and prove the positive-variance global bound with equality conditions.',
         'Describe every minimiser and explain when uniqueness holds.',
         'Distinguish unrestricted cancellation, nonnegative constraints and perfectly duplicated common noise.'])


def add_coding(add,tasks):
    def exercise(level,title,prompt,signature,samples,tests,solution,explanation):
        add(f'c_l10_{level.lower()}',title,level,'Linear algebra',prompt,signature,samples,tests,solution,explanation)
        tasks[-1]['path']='researcher'
        for key in ('prompt','explanation'):tasks[-1][key]=tasks[-1][key].replace(r'\n\n','\n\n')

    exercise('Easy','Check a two-variable covariance proposal',
        r'Inputs v1, v2 and covariance are integers of absolute value at most 10^18. They propose the symmetric covariance matrix [[v1,covariance],[covariance,v2]]. Return True exactly when SOME real-valued joint model with finite second moments has this covariance matrix; return False otherwise. Include singular and zero-variance cases. Do not require positive definiteness, apply a numerical tolerance or silently change an entry. Use O(1) integer arithmetic; no simulation or matrix library is needed.',
        'def solve(v1, v2, covariance):',
        [{'args':[1,4,2],'expected':True},{'args':[1,4,3],'expected':False}],
        [{'args':[0,0,0],'expected':True},{'args':[0,9,0],'expected':True},
         {'args':[0,9,1],'expected':False},{'args':[-1,4,0],'expected':False},
         {'args':[4,-1,0],'expected':False},{'args':[4,9,-6],'expected':True},
         {'args':[4,9,-7],'expected':False},{'args':[10**18,10**18,10**18],'expected':True},
         {'args':[10**18-1,10**18-1,10**18],'expected':False}],
        '''def solve(v1, v2, covariance):
    return v1 >= 0 and v2 >= 0 and covariance * covariance <= v1 * v2''',
        r'A covariance matrix must be PSD: both proposed variances must be nonnegative and its determinant \(v_1v_2-c^2\) must be nonnegative. These are sufficient for a symmetric 2×2 matrix. For v₁>0, construct X=√v₁ Z and \(Y=(c/\sqrt{v_1})Z+\sqrt{v_2-c^2/v_1}\,U\), with independent centered variance-one Z,U. For v₁=0, the determinant condition forces c=0, and a constant X with variance-v₂ Y works. Singular boundaries are permitted. Exact integer products avoid falsely accepting a tiny negative determinant after large-number float rounding. O(1) bounded-size arithmetic and auxiliary state.')

    exercise('Medium','Blend two estimates without forbidden weights',
        r'Inputs v1, v2 and covariance are integers of absolute value at most 10^12. The matrix [[v1,covariance],[covariance,v2]] is GUARANTEED PSD. X and Y are unbiased estimates of the same target with these known error variances/covariance. Choose a fixed blend wX+(1−w)Y with 0≤w≤1. Return [w, minimum_variance] as numerical values, without manual rounding. If all weights tie, choose the smallest w. Zero variances, identical errors and perfect negative dependence are valid. Do not use an independent-estimates formula or allow negative weights. Aim for O(1) arithmetic and space; preserve integer products until the final divisions to avoid cancellation.',
        'def solve(v1, v2, covariance):',
        [{'args':[1,4,0],'expected':[.8,.8]},{'args':[9,1,2],'expected':[0,1]}],
        [{'args':[1,9,2],'expected':[1,1]},{'args':[3,3,3],'expected':[0,3]},
         {'args':[0,0,0],'expected':[0,0]},{'args':[0,9,0],'expected':[1,0]},
         {'args':[9,0,0],'expected':[0,0]},{'args':[1,4,-2],'expected':[2/3,0]},
         {'args':[4,9,-6],'expected':[3/5,0]}, {'args':[4,9,6],'expected':[1,4]},
         {'args':[10**12,10**12,10**12-1],'expected':[.5,10**12-.5]},
         {'args':[10**12,10**12,0],'expected':[.5,5*10**11]}],
        '''def solve(v1, v2, covariance):
    difference = v1 + v2 - 2 * covariance
    numerator = v2 - covariance
    if difference == 0 or numerator <= 0:
        return [0, v2]
    if numerator >= difference:
        return [1, v1]
    return [numerator / difference, (v1 * v2 - covariance * covariance) / difference]''',
        r'The variance is \(V(w)=v_2+2w(c-v_2)+w^2D\), where \(D=v_1+v_2-2c=\operatorname{Var}(X-Y)\geq0\). For D>0 the unconstrained minimiser is (v₂−c)/D; clip it to [0,1]. At clipped zero or one return v₂ or v₁. At an interior optimum the variance simplifies to \((v_1v_2-c^2)/D\); calculate that numerator as an integer before division rather than subtracting large float terms. If D=0, PSD implies v₁=v₂=c, so every blend ties and w=0 is the specified choice. A zero determinant can give a zero-risk nonnegative blend for negative covariance, while positive dependence can push the best allowed blend to a boundary. Known covariance and common-target unbiasedness are assumptions, not properties inferred by this function.')

    # Exact expectations are supplied independently by the rational range/null
    # oracle in tests/test_covariance_practice.py, not by running this reference.
    hard_cases=[{'args': [[[2, 3]]], 'expected': ['13', '1']},
 {'args': [[[1], [1]]], 'expected': ['1', '1']},
 {'args': [[[0], [0]]], 'expected': ['0', '1']},
 {'args': [[[1], [-1]]], 'expected': ['0', '1']},
 {'args': [[[1, 0], [1, 0], [0, 2]]], 'expected': ['4', '5']},
 {'args': [[[0, 0], [3, 4]]], 'expected': ['0', '1']},
 {'args': [[[2], [3], [5]]], 'expected': ['0', '1']},
 {'args': [[[1, 1], [2, 1]]], 'expected': ['1', '1']},
 {'args': [[[999999, 999998], [1000000, 999999]]], 'expected': ['1', '2']},
 {'args': [[[1, 2, 0], [0, 1, 3], [2, 0, 1]]], 'expected': ['169', '50']},
 {'args': [[[1, 1, 0], [1, 1, 1], [1, 1, 2]]], 'expected': ['2', '1']},
 {'args': [[[1, 0, 0], [0, 2, 0], [0, 0, 3]]], 'expected': ['36', '49']},
 {'args': [[[1000000,
             999999,
             999999,
             999999,
             999999,
             999999,
             999999,
             999999,
             999999,
             999999,
             999999,
             999999],
            [999999,
             1000000,
             999999,
             999999,
             999999,
             999999,
             999999,
             999999,
             999999,
             999999,
             999999,
             999999],
            [999999,
             999999,
             1000000,
             999999,
             999999,
             999999,
             999999,
             999999,
             999999,
             999999,
             999999,
             999999],
            [999999,
             999999,
             999999,
             1000000,
             999999,
             999999,
             999999,
             999999,
             999999,
             999999,
             999999,
             999999],
            [999999,
             999999,
             999999,
             999999,
             1000000,
             999999,
             999999,
             999999,
             999999,
             999999,
             999999,
             999999],
            [999999,
             999999,
             999999,
             999999,
             999999,
             1000000,
             999999,
             999999,
             999999,
             999999,
             999999,
             999999],
            [999999,
             999999,
             999999,
             999999,
             999999,
             999999,
             1000000,
             999999,
             999999,
             999999,
             999999,
             999999],
            [999999,
             999999,
             999999,
             999999,
             999999,
             999999,
             999999,
             1000000,
             999999,
             999999,
             999999,
             999999],
            [999999,
             999999,
             999999,
             999999,
             999999,
             999999,
             999999,
             999999,
             1000000,
             999999,
             999999,
             999999],
            [999999,
             999999,
             999999,
             999999,
             999999,
             999999,
             999999,
             999999,
             999999,
             1000000,
             999999,
             999999],
            [999999,
             999999,
             999999,
             999999,
             999999,
             999999,
             999999,
             999999,
             999999,
             999999,
             1000000,
             999999],
            [999999,
             999999,
             999999,
             999999,
             999999,
             999999,
             999999,
             999999,
             999999,
             999999,
             999999,
             1000000]]],
  'expected': ['143999736000121', '12']},
 {'args': [[[1, 2, 3], [1, 2, 3], [1, 2, 3]]], 'expected': ['14', '1']},
 {'args': [[[4, 1], [4, -1], [4, 3], [4, -3]]], 'expected': ['16', '1']},
 {'args': [[[999983, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 999979, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 999961, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 999959, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 999953, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 999931, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 999917, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 999907, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 999883, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 999863, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 999853, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 999809]]],
  'expected': ['997997889902713398032859464626029931741045274637004425419193109515109287463011483547019675717524139668741725949398747488865304600078879593434929',
               '11977975016930212403546584174099880837086226603774104231738457514938749702639372673833603751764848946282795712589578081184044101459932']}]
    exercise('Hard','Pool shared-factor estimates through singularity',
        r'd estimates have the same unknown mean µ and the error model \(X_i-\mu=\sum_{j=1}^k A_{ij}Z_j\), where centered factor vector Z has covariance I. factors supplies the d×k INTEGER matrix A, with 1≤d,k≤12 and entries of absolute value at most 10^6. No distributional or independence assumption beyond these second moments is needed. Its covariance \(\Sigma=AA^T\) is guaranteed PSD and may be singular or zero.\n\nAmong all FIXED real weights summing to one, including negative weights, compute the exact minimum variance of the unbiased pooled estimate. Return a reduced rational pair [numerator_text,denominator_text] as canonical base-ten STRINGS, with a nonnegative numerator, positive denominator and gcd=1; zero must be ["0","1"]. Use str(integer), with no sign on positive values or leading zeroes. Large answers exceed the browser’s exact numeric range, so strings preserve the exact rational through display and copying. Do not return weights, add a ridge, clamp eigenvalues or approximate an exact zero. Input is nonempty and rectangular; do not mutate it.\n\nUse O(d²k+d³) scalar arithmetic and O(d²) auxiliary storage, with Python integer arithmetic for exact rank decisions. Integer bit costs and gcd costs are additional; dimensions are small. No external numerical package is needed. The editorial derives a consistent equality-constrained system whose multiplier identifies the variance even when weights are nonunique.',
        'def solve(factors):',
        [{'args':[[[1,0],[0,2]]],'expected':['4','5']},
         {'args':[[[1],[2]]],'expected':['0','1']}],hard_cases,
        '''from math import gcd
def solve(factors):
    d, k = len(factors), len(factors[0])
    rows = [[sum(factors[i][j] * factors[h][j] for j in range(k)) for h in range(d)] + [1, 0] for i in range(d)]
    rows.append([1] * d + [0, 1])
    rank = 0
    multiplier_row = None
    for column in range(d + 1):
        pivot = next((i for i in range(rank, d + 1) if rows[i][column] != 0), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        divisor = 0
        for value in rows[rank]:
            divisor = gcd(divisor, abs(value))
        if divisor:
            rows[rank] = [value // divisor for value in rows[rank]]
        for i in range(d + 1):
            if i == rank or rows[i][column] == 0:
                continue
            a, b = rows[rank][column], rows[i][column]
            rows[i] = [a * value - b * lead for value, lead in zip(rows[i], rows[rank])]
            divisor = 0
            for value in rows[i]:
                divisor = gcd(divisor, abs(value))
            if divisor:
                rows[i] = [value // divisor for value in rows[i]]
        if column == d:
            multiplier_row = rank
        rank += 1
    numerator = -rows[multiplier_row][-1]
    denominator = rows[multiplier_row][d]
    if denominator < 0:
        numerator, denominator = -numerator, -denominator
    divisor = gcd(abs(numerator), denominator)
    return [str(numerator // divisor), str(denominator // divisor)]''',
        r'The objective is \(\|A^Tw\|^2=w^T\Sigma w\); the sum-one constraint preserves the common target. An optimum exists: \(A^T\) maps the feasible affine set onto a finite-dimensional affine set, and its squared distance to zero is attained. At an optimum the covariance gradient is constant across coordinates, because every zero-sum perturbation has zero first derivative. Write this as \(\Sigma w+\nu\mathbf1=0\), together with \(\mathbf1^Tw=1\), giving\n\n\[\begin{pmatrix}\Sigma&\mathbf1\\\mathbf1^T&0\end{pmatrix}\begin{pmatrix}w\\\nu\end{pmatrix}=\begin{pmatrix}0\\1\end{pmatrix}.\]\n\nConversely any solution is globally optimal: for a feasible perturbation h, \(h^T\mathbf1=0\), and the objective change is \(2h^T\Sigma w+h^T\Sigma h=h^T\Sigma h\geq0\). Multiplying the first equation by wᵀ gives minimum variance −ν. The multiplier is unique even if weights are not: the difference of two solutions obeys \(\Sigma\Delta w+\Delta\nu\mathbf1=0\), \(\mathbf1^T\Delta w=0\); its quadratic form is zero, so PSD implies ΣΔw=0 and Δν=0. Thus every solution has the same requested scalar.\n\nConstruct the integer Gram matrix, append this system and perform rank-aware elimination. For a pivot a and row coefficient b, replace a row by a·row−b·pivot_row; divide the entire resulting row, including its right side, by its integer gcd to control growth. These exact nonzero row operations preserve the solution set. Eliminate ABOVE and below pivots; skip absent pivots rather than dividing by zero. The multiplier column always has a pivot: if it were free, a consistent system would allow different ν, contradicting uniqueness. After elimination its pivot row contains only that variable and its right side, so their ratio gives ν. Reduce −ν to a positive-denominator rational pair and encode its integers as decimal strings; both the judge and copied debugging cases retain every digit. No choices of free weight variables are needed. Gcd normalization is not floating tolerance and a singular Gram matrix is not automatically zero-risk: duplicated factor rows can share unavoidable common noise. Building the Gram matrix costs O(d²k); elimination costs O(d³) scalar arithmetic with O(d²) state, plus integer/gcd bit costs.')
