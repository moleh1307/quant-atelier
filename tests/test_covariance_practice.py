"""Independent exact covariance geometry, singular bounds and coding oracles.

The optimisation oracle branches on covariance range membership; the production
reference instead eliminates an augmented multiplier system with integer rows.
A second oracle takes the zero-ridge limit of determinant/cofactor polynomials.
No personal progress or workspace API is touched.
"""
import copy
import itertools
import json
import random
import unittest
from fractions import Fraction as F
from math import gcd
from pathlib import Path


def solve_rational(matrix, rhs):
    """Return a particular rational solution or None; free variables are zero."""
    width=len(matrix[0])
    rows=[[F(x) for x in row]+[F(b)] for row,b in zip(matrix,rhs)]
    pivots=[]
    for column in range(width):
        pivot=next((i for i in range(len(pivots),len(rows)) if rows[i][column]),None)
        if pivot is None:continue
        r=len(pivots);rows[r],rows[pivot]=rows[pivot],rows[r]
        scale=rows[r][column];rows[r]=[x/scale for x in rows[r]]
        for i in range(len(rows)):
            if i!=r:
                scale=rows[i][column]
                rows[i]=[x-scale*y for x,y in zip(rows[i],rows[r])]
        pivots.append(column)
    if any(not any(row[:-1]) and row[-1] for row in rows):return None
    answer=[F(0)]*width
    for r,column in enumerate(pivots):answer[column]=rows[r][-1]
    return answer


def gram(factors):
    return [[sum(x*y for x,y in zip(a,b)) for b in factors] for a in factors]


def quadratic(matrix,w):
    return sum(w[i]*matrix[i][j]*w[j] for i in range(len(w)) for j in range(len(w)))


def optimum(factors):
    """Use the two range/null branches and return risk plus witness weights."""
    matrix=gram(factors);d=len(factors)
    v=solve_rational(matrix,[1]*d)
    if v is None:
        equations=[list(column) for column in zip(*factors)]+[[1]*d]
        weights=solve_rational(equations,[0]*len(factors[0])+[1])
        assert weights is not None
        return F(0),weights
    normalizer=sum(v)
    assert normalizer>0
    return 1/normalizer,[x/normalizer for x in v]


def determinant(matrix):
    if not matrix:return F(1)
    rows=[[F(x) for x in row] for row in matrix];result=F(1)
    for i in range(len(rows)):
        pivot=next((r for r in range(i,len(rows)) if rows[r][i]),None)
        if pivot is None:return F(0)
        if pivot!=i:rows[i],rows[pivot]=rows[pivot],rows[i];result=-result
        lead=rows[i][i];result*=lead
        for r in range(i+1,len(rows)):
            scale=rows[r][i]/lead
            for c in range(i+1,len(rows)):rows[r][c]-=scale*rows[i][c]
    return result


def interpolate(values):
    """Polynomial coefficients at integer points 0,...,degree."""
    vandermonde=[[F(x)**j for j in range(len(values))] for x in range(len(values))]
    return solve_rational(vandermonde,values)


def ridge_limit(factors):
    matrix=gram(factors);d=len(matrix);numerator=[];denominator=[]
    for epsilon in range(d+1):
        shifted=[[matrix[i][j]+(epsilon if i==j else 0) for j in range(d)] for i in range(d)]
        numerator.append(determinant(shifted))
        cofactors=F(0)
        for i in range(d):
            for j in range(d):
                minor=[[shifted[r][c] for c in range(d) if c!=j] for r in range(d) if r!=i]
                cofactors+=(-1)**(i+j)*determinant(minor)
        denominator.append(cofactors)
    p=interpolate(numerator);q=interpolate(denominator)
    a=next(i for i,x in enumerate(p) if x);b=next(i for i,x in enumerate(q) if x)
    assert a>=b
    return F(0) if a>b else p[a]/q[b]


def pair(risk):return [str(risk.numerator),str(risk.denominator)]


def blend(v1,v2,c):
    candidates=[F(0),F(1)];difference=v1+v2-2*c
    if difference and 0<=F(v2-c,difference)<=1:candidates.append(F(v2-c,difference))
    ranked=sorted((v1*w*w+v2*(1-w)**2+2*c*w*(1-w),w) for w in candidates)
    risk,w=ranked[0];return [float(w),float(risk)]


class CovariancePracticeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from coding_bank import TASKS
        from test_topic_practice import BANK,QUESTIONS,reference
        cls.codes={x['id']:x for x in TASKS};cls.bank=BANK;cls.questions=QUESTIONS;cls.reference=staticmethod(reference)

    def test_cross_terms_units_and_exact_relationships(self):
        # An independent two-factor construction has covariance -3 and Var 4,9.
        # Enumerate a variance-27/4 residual without square roots: six equally likely
        # errors [-9/2,9/2,0,0,0,0] have that exact variance.
        records=[(2*z,-F(3,2)*z+u) for z in (-1,1) for u in (-F(9,2),F(9,2),0,0,0,0)]
        self.assertEqual(sum((x+2*y)**2 for x,y in records)/len(records),28)
        self.assertTrue(all(x+2*y==x+F(1,5)*(10*y) for x,y in records))
        for z in (-3,3):
            x,y=2+z,7+z
            self.assertEqual(x-y,-5)
            y=7-z;self.assertEqual(x+y,9)
        self.assertEqual(self.questions['q_l10_e1']['answer'],28)
        self.assertEqual(self.questions['q_l10_e2']['answer'],0)

    def test_pairwise_deletion_and_identity_shrinkage(self):
        rows=[(-1,-1,None),(1,1,None),(None,-1,-1),(None,1,1),(-1,None,1),(1,None,-1)]
        R=[[1]*3 for _ in range(3)]
        for i,j in itertools.combinations(range(3),2):
            subset=[(r[i],r[j]) for r in rows if r[i] is not None and r[j] is not None]
            # All these pair-specific columns have exact mean zero and equal norm.
            correlation=F(sum(x*y for x,y in subset),sum(x*x for x,y in subset))
            R[i][j]=R[j][i]=correlation
        self.assertEqual(R,[[1,1,-1],[1,1,1],[-1,1,1]])
        w=[1,-1,1];self.assertEqual(quadratic(R,w),-3)
        for v in ([1,1,0],[1,0,-1]):
            self.assertEqual([sum(row[j]*v[j] for j in range(3)) for row in R],[2*x for x in v])
        for alpha in (F(0),F(1,4),F(1,2),F(3,4),F(1)):
            shifted=[[(1-alpha)*R[i][j]+(alpha if i==j else 0) for j in range(3)] for i in range(3)]
            self.assertEqual(quadratic(shifted,w),3*(-1+2*alpha))
            if alpha>=F(1,2):
                for direction in itertools.product(range(-2,3),repeat=3):self.assertGreaterEqual(quadratic(shifted,direction),0)
        self.assertTrue(all(None in row for row in rows))

    def test_singular_extension_square_identity_and_construction(self):
        e1=[F(3,5),F(4,5),F(0)];e0=[-F(4,5),F(3,5),F(0)];e2=[F(0),F(0),F(1)]
        B=[[4*e1[i]*e1[j]+9*e2[i]*e2[j] for j in range(3)] for i in range(3)]
        c=[2*e1[i]+3*e2[i] for i in range(3)];s=F(2)
        for residual in (0,1,2):
            v=s+residual**2
            block=[B[i]+[c[i]] for i in range(3)]+[c+[v]]
            for coords in itertools.product(range(-2,3),repeat=3):
                u=[coords[0]*e1[i]+coords[1]*e0[i]+coords[2]*e2[i] for i in range(3)]
                for t in (-2,-1,0,1,2):
                    squares=4*(F(coords[0])+F(t,2))**2+9*(F(coords[2])+F(t,3))**2+t*t*residual**2
                    self.assertEqual(quadratic(block,u+[t]),squares)
            records=[]
            for z1,z2,z0 in itertools.product((-1,1),repeat=3):
                U=[2*e1[i]*z1+3*e2[i]*z2 for i in range(3)]
                records.append(U+[z1+z2+residual*z0])
            empirical=[[sum(r[i]*r[j] for r in records)/len(records) for j in range(4)] for i in range(4)]
            self.assertEqual(empirical,block)
        # Any null-direction covariance is incompatible, however large v is.
        for v in (0,1,10**6,10**18):
            bad_c=[c[i]+e0[i] for i in range(3)]
            block=[B[i]+[bad_c[i]] for i in range(3)]+[bad_c+[v]]
            u=[-F(v+1,2)*x for x in e0]
            self.assertEqual(quadratic(block,u+[1]),-1)
        for eps in (F(1),F(1,10),F(1,1000)):
            B2=[[1+eps,1],[1,1+eps]]
            solution=solve_rational(B2,[1,2])
            threshold=sum(a*b for a,b in zip([1,2],solution))
            self.assertEqual(threshold,F(9,2)/(2+eps)+F(1,2)/eps)
        self.assertEqual(optimum([[0],[0]])[0],0)

    def test_two_variable_feasibility_and_convex_blend(self):
        easy=self.reference('c_l10_easy');medium=self.reference('c_l10_medium')
        for v1,v2,c in itertools.product(range(-2,9),range(-2,9),range(-9,10)):
            # Independent exact eigenvalue-sign criterion: trace/determinant.
            feasible=(v1+v2>=0 and v1*v2-c*c>=0)
            self.assertEqual(easy(v1,v2,c),feasible)
            if not feasible:continue
            self.assertEqual(medium(v1,v2,c),blend(v1,v2,c))
        for id in ('c_l10_easy','c_l10_medium'):
            for case in self.codes[id]['samples']+self.codes[id]['tests']:
                args=case['args']
                expected=(args[0]>=0 and args[1]>=0 and args[2]**2<=args[0]*args[1]) if id.endswith('easy') else blend(*args)
                self.assertEqual(case['expected'],expected)
                self.assertEqual(self.reference(id)(*args),expected)

    def test_singular_pool_global_bounds_and_all_minimiser_directions(self):
        rng=random.Random(10012)
        for _ in range(220):
            d,k=rng.randrange(1,8),rng.randrange(1,8)
            A=[[rng.randrange(-4,5) for _ in range(k)] for _ in range(d)]
            V,w=optimum(A);matrix=gram(A)
            self.assertEqual(sum(w),1);self.assertEqual(quadratic(matrix,w),V)
            self.assertEqual([sum(row[j]*w[j] for j in range(d)) for row in matrix],[V]*d)
            for _ in range(3):
                h=[F(rng.randrange(-5,6)) for _ in range(d-1)];h.append(-sum(h))
                shifted=[a+b for a,b in zip(w,h)]
                self.assertEqual(quadratic(matrix,shifted)-V,quadratic(matrix,h))
                self.assertGreaterEqual(quadratic(matrix,shifted),V)
            self.assertEqual(self.reference('c_l10_hard')(copy.deepcopy(A)),pair(V))
        for d in range(1,13):
            V,w=optimum([[1]]*d);self.assertEqual(V,1)
            V,w=optimum([[0]]*d);self.assertEqual(V,0)
        V,w=optimum([[1],[2]]);self.assertEqual((V,w),(0,[F(2),F(-1)]))
        self.assertEqual(blend(1,4,2),[1,1])

    def test_independent_determinant_cofactor_ridge_limit(self):
        rng=random.Random(10100)
        for _ in range(65):
            d,k=rng.randrange(1,5),rng.randrange(1,5)
            A=[[rng.randrange(-3,4) for _ in range(k)] for _ in range(d)]
            self.assertEqual(ridge_limit(A),optimum(A)[0])
            self.assertEqual(self.reference('c_l10_hard')(A),pair(ridge_limit(A)))
        # Gram determinant one despite huge almost-parallel rows; optimal weights
        # are large and opposite, whereas the exact minimal risk is one half.
        A=[[999999,999998],[1000000,999999]]
        self.assertEqual(determinant(gram(A)),1)
        self.assertEqual(optimum(A)[0],F(1,2))
        self.assertEqual(self.reference('c_l10_hard')(A),['1','2'])

    def test_pool_metamorphic_properties_and_published_expectations(self):
        hard=self.reference('c_l10_hard');rng=random.Random(10101)
        for _ in range(80):
            d,k=rng.randrange(1,7),rng.randrange(1,7)
            A=[[rng.randrange(-5,6) for _ in range(k)] for _ in range(d)]
            V=optimum(A)[0];original=copy.deepcopy(A)
            result=hard(A);self.assertEqual(A,original);self.assertEqual(result,pair(V))
            self.assertEqual(gcd(*(int(x) for x in result)),1);self.assertGreater(int(result[1]),0)
            rng.shuffle(A);self.assertEqual(hard(A),result)
            self.assertEqual(hard([[-3*x for x in row] for row in A]),pair(9*V))
            self.assertEqual(hard(A+[A[0][:]]),result)
            self.assertEqual(hard([row+[0] for row in A]),result)
            signs=[rng.choice((-1,1)) for _ in range(k)]
            self.assertEqual(hard([[x*s for x,s in zip(row,signs)] for row in A]),result)
        for case in self.codes['c_l10_hard']['samples']+self.codes['c_l10_hard']['tests']:
            self.assertEqual(case['expected'],pair(optimum(case['args'][0])[0]))
        # Maximum dimensions and large entries, without tolerance or rank loss.
        A=[[10**6 if i==j else 999999 for j in range(12)] for i in range(12)]
        self.assertEqual(hard(A),[str(11999989**2),'12'])

    def test_actual_judge_mutation_size_and_wrong_shortcuts(self):
        from judge import run
        for id in ('c_l10_easy','c_l10_medium','c_l10_hard'):
            task=self.codes[id];result=run(id,task['solution'])
            self.assertEqual(result.get('passed'),result.get('total'),result)
            self.assertGreater(result.get('total',0),1)
            for case in task['samples']+task['tests']:
                self.assertLessEqual(len(json.dumps(case['args']))+len(json.dumps(case['expected'])),200000)
                args=copy.deepcopy(case['args']);original=copy.deepcopy(args)
                self.reference(id)(*args);self.assertEqual(args,original)
        wrong={'c_l10_easy':'def solve(v1,v2,covariance):\n    return v1>0 and v2>0 and covariance*covariance<v1*v2',
               'c_l10_medium':'def solve(v1,v2,covariance):\n    if v1+v2==0:return [0,0]\n    return [v2/(v1+v2),v1*v2/(v1+v2)]',
               'c_l10_hard':"def solve(factors):\n    return ['0','1']"}
        for id,code in wrong.items():
            result=run(id,code);self.assertLess(result.get('passed',0),result.get('total',1),result)

    def test_difficulty_coverage_specific_rubrics_and_preserved_links(self):
        lesson=next(l for l in self.bank['lessons'] if l['id']=='l10')
        self.assertEqual(lesson['questions'][:2],['q20','q29'])
        self.assertEqual(len(lesson['questions']),7)
        self.assertEqual(lesson['coding'],['c_l10_easy','c_l10_medium','c_l10_hard'])
        for q in lesson['questions']:
            self.assertNotIn('Show the decisive derivation or counterexample.',self.questions[q]['rubric'])
        self.assertTrue(all(len(self.questions[q]['rubric'])>=4 for q in ('q_l10_h1','q_l10_h2')))


if __name__=='__main__':unittest.main()
