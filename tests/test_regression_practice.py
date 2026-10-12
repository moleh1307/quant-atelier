"""Independent regression checks: centered deletion refits, never PRESS fixtures.

The production reference performs one fraction-free augmented-matrix inverse.
The oracle independently fits each remaining dataset using centered Fraction
normal equations without an intercept column or leverage calculation.
No workspace progress endpoint or personal record is used.
"""
import copy
import itertools
import json
import random
import unittest
from collections import Counter
from fractions import Fraction as F


def linear_solve(matrix, rhs):
    rows = [[F(v) for v in row] + [F(v)] for row, v in zip(matrix, rhs)]
    d = len(rows)
    for column in range(d):
        pivot = next(i for i in range(column, d) if rows[i][column])
        rows[column], rows[pivot] = rows[pivot], rows[column]
        lead = rows[column][column]
        rows[column] = [v / lead for v in rows[column]]
        for i in range(d):
            if i != column:
                lead = rows[i][column]
                rows[i] = [a - lead*b for a, b in zip(rows[i], rows[column])]
    return [row[-1] for row in rows]


def refit_errors(features, targets, ridge):
    n = len(targets)
    if not n:
        return []
    if n == 1:
        return [None]
    d = len(features[0])
    result = []
    for held in range(n):
        remaining = [i for i in range(n) if i != held]
        size = n-1
        mean_x = [F(sum(features[i][j] for i in remaining), size) for j in range(d)]
        mean_y = F(sum(targets[i] for i in remaining), size)
        centered = [[F(features[i][j])-mean_x[j] for j in range(d)] for i in remaining]
        centered_y = [F(targets[i])-mean_y for i in remaining]
        covariance = [[sum(row[j]*row[k] for row in centered)+(ridge if j == k else 0)
                       for k in range(d)] for j in range(d)]
        cross = [sum(row[j]*y for row, y in zip(centered, centered_y)) for j in range(d)]
        slopes = linear_solve(covariance, cross)
        intercept = mean_y-sum(a*b for a, b in zip(slopes, mean_x))
        error = F(targets[held])-intercept-sum(a*b for a, b in zip(slopes, features[held]))
        result.append([str(error.numerator), str(error.denominator)])
    return result


def minimum_sse(x, y):
    if not y:
        return F(0)
    n = len(y)
    mx, my = F(sum(x), n), F(sum(y), n)
    xx = sum((a-mx)**2 for a in x)
    xy = sum((a-mx)*(b-my) for a, b in zip(x, y))
    yy = sum((b-my)**2 for b in y)
    return yy-xy*xy/xx if xx else yy


def moments(records, a, b):
    count = len(records)
    ma, mb = F(sum(row[a] for row in records), count), F(sum(row[b] for row in records), count)
    return F(sum((row[a]-ma)*(row[b]-mb) for row in records), count)


class RegressionPracticeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from test_topic_practice import BANK, CODES, QUESTIONS, reference
        cls.bank, cls.codes, cls.questions = BANK, CODES, QUESTIONS
        cls.reference = staticmethod(reference)

    def test_coverage_and_specific_preserved_rubrics(self):
        lesson = next(l for l in self.bank['lessons'] if l['id'] == 'l11')
        self.assertEqual(lesson['questions'][:3], ['q19','q21','q30'])
        self.assertEqual(Counter(self.questions[id]['difficulty'] for id in lesson['questions']),
                         Counter(Easy=2, Medium=2, Hard=4))
        self.assertEqual(lesson['coding'], ['c_l11_easy','c07','c_l11_hard'])
        for id in lesson['questions']:
            self.assertGreaterEqual(len(self.questions[id]['rubric']), 3)
            self.assertNotIn('State the assumptions and the object you are computing.', self.questions[id]['rubric'])

    def test_population_units_and_penalty_equivalence(self):
        b = F(6,4);a = 5-b*2
        self.assertEqual(b, F(3,2));self.assertEqual(a, 2)
        self.assertEqual(13-F(36,4), 4)
        self.assertEqual(F(6+2*5,4+2*2), 2)
        self.assertEqual(38-F(256,8), 6)
        transformed_b = b/10
        # The population line above has a different intercept from the lesson
        # sample. Independently check that sample's stated unit conversion.
        for x in (0,1,2):
            self.assertEqual(F(1,2)+F(3,2)*x, F(-5,2)+F(3,20)*(10*x+20))
        self.assertEqual(self.questions['q_l11_e1']['answer'], float(b))
        self.assertEqual(self.questions['q_l11_e2']['answer'], float(transformed_b))
        for physical_slope in (F(-7,3), F(0), F(3,2)):
            self.assertEqual(100*7*(physical_slope/10)**2, 7*physical_slope**2)

    def test_orthogonality_and_observed_gaussian_covariance(self):
        records = [(u+v,3*u+v,u-v,u) for u,v in itertools.product((-1,1),repeat=2)]
        self.assertEqual(moments(records,0,0), 2)
        self.assertEqual(moments(records,0,1), 4)
        self.assertEqual(moments(records,0,2), 0)
        self.assertEqual(moments(records,1,1), 10)
        for _,_,_,u in records:
            self.assertEqual(((8+1)+2*u)-(8+2*u), 1)
        # Independent Gaussian X and eta of variance two produce the same
        # covariance table. Gaussianity, not this finite enumeration, supplies
        # the conclusion that the complete observed distributions coincide.
        self.assertEqual(2*2, 4)
        self.assertEqual(2**2*2+2, 10)

    def test_instrument_moments_with_correlated_first_error(self):
        records = [(2*k+3*h,2*k+g,3*k+h+e) for k,h,g,e in itertools.product((-1,1),repeat=4)]
        self.assertEqual(moments(records,1,2), 6)
        self.assertEqual(moments(records,1,0), 4)
        self.assertEqual(moments(records,1,2)/moments(records,1,0), F(3,2))
        self.assertEqual(moments(records,0,2)/moments(records,0,0), F(9,13))
        for s,beta,error_var,error_cross,response_error in ((F(1),F(1),F(1),F(0),F(1)),
                                                         (F(3,4),F(4,3),F(5,4),F(1,4),F(2,3))):
            self.assertGreater(error_var**2-error_cross**2, 0)
            self.assertEqual(s+error_var, 2)
            self.assertEqual(s+error_cross, 1)
            self.assertEqual(beta*s, 1)
            self.assertEqual(beta**2*s+response_error, 2)

    def test_ols_deletion_identity_and_leverage_one(self):
        x = [[1,0],[1,1],[1,2]];y = [1,1,4]
        matrix = [[sum(row[j]*row[k] for row in x) for k in range(2)] for j in range(2)]
        fitted = linear_solve(matrix,[sum(row[j]*v for row,v in zip(x,y)) for j in range(2)])
        errors=[]
        for held,row in enumerate(x):
            z = linear_solve(matrix,row)
            h = sum(a*b for a,b in zip(row,z))
            r = y[held]-sum(a*b for a,b in zip(row,fitted))
            self.assertLess(h, 1)
            errors.append(r/(1-h))
        self.assertEqual(errors,[F(3),F(-3,2),F(3)])
        # For a two-row intercept+slope design, deletion destroys slope
        # identification despite a zero full-data training residual.
        matrix=[[2,1],[1,1]];row=[1,0];z=linear_solve(matrix,row)
        self.assertEqual(sum(a*b for a,b in zip(row,z)), 1)
        deleted=[[matrix[j][k]-row[j]*row[k] for k in range(2)] for j in range(2)]
        self.assertEqual([sum(a*b for a,b in zip(r,z)) for r in deleted], [0,0])
        self.assertEqual(sum(a*b for a,b in zip([1,1],z)), 0)
        self.assertEqual(refit_errors([[0],[1],[2]],[1,1,4],1), [['0','1'],['-3','2'],['3','1']])

    def test_easy_against_exact_minimum_and_nonunique_fits(self):
        solve = self.reference('c_l11_easy');rng=random.Random(11101)
        for _ in range(350):
            n=rng.randrange(12);x=[rng.randrange(-8,9) for _ in range(n)]
            y=[rng.randrange(-8,9) for _ in range(n)]
            a,b=rng.randrange(-5,6),rng.randrange(-5,6)
            expected=sum((v-a-b*u)**2 for u,v in zip(x,y)) == minimum_sse(x,y)
            original=copy.deepcopy([x,y])
            self.assertEqual(solve(x,y,a,b),expected)
            self.assertEqual([x,y],original)
            self.assertTrue(solve(x,[a+b*u for u in x],a,b))
        self.assertTrue(solve([7,7],[2,4],-11,2))
        self.assertFalse(solve([0,1,2],[1,1,4],1,1))
        self.assertTrue(solve([10**6]*100000,[10**6]*100000,10**6,0))

    def test_all_authored_expectations_and_debug_size(self):
        solve=self.reference('c_l11_hard')
        for case in self.codes['c_l11_hard']['samples']+self.codes['c_l11_hard']['tests']:
            features,y,ridge=case['args']
            self.assertLessEqual(len(json.dumps(case['args']))+len(json.dumps(case['expected'])),200000)
            if len(y)>100:
                total=sum(y);n=len(y)
                expected=[]
                for target in y:
                    v=F(n*target-total,n-1)
                    expected.append([str(v.numerator),str(v.denominator)])
            else:
                expected=refit_errors(features,y,ridge)
            self.assertEqual(case['expected'],expected)
            self.assertEqual(solve(*copy.deepcopy(case['args'])),expected)

    def test_seeded_full_deletion_refits_and_input_preservation(self):
        solve=self.reference('c_l11_hard');rng=random.Random(11102)
        for trial in range(180):
            n=rng.randrange(11);d=rng.randrange(5)
            features=[[rng.randrange(-7,8) for _ in range(d)] for _ in range(n)]
            y=[rng.randrange(-9,10) for _ in range(n)];ridge=rng.choice([1,2,19,10**9])
            original=copy.deepcopy(features)
            self.assertEqual(solve(features,y,ridge),refit_errors(features,y,ridge),trial)
            self.assertEqual(features,original)
        features=[[10**6]*6 for _ in range(10000)];y=[17]*10000
        self.assertEqual(solve(features,y,10**9), [['0','1']]*10000)

    def test_fixed_procedure_equivariances_and_lossless_outputs(self):
        solve=self.reference('c_l11_hard')
        x=[[2,-1],[5,4],[-3,2],[1,7],[0,-2]];y=[3,-8,11,4,7];ridge=13
        result=solve(x,y,ridge)
        permutation=[4,1,3,0,2]
        self.assertEqual(solve([x[i] for i in permutation],[y[i] for i in permutation],ridge),[result[i] for i in permutation])
        self.assertEqual(solve([[a+10,b-13] for a,b in x],y,ridge),result)
        self.assertEqual(solve([[-b,a] for a,b in x],y,ridge),result)
        self.assertEqual(solve([[10*a,10*b] for a,b in x],y,100*ridge),result)
        self.assertEqual(solve([row+[0] for row in x],y,ridge),result)
        shifted=solve(x,[3*v+9 for v in y],ridge)
        for pair,other in zip(result,shifted):
            self.assertEqual(F(int(other[0]),int(other[1])),3*F(int(pair[0]),int(pair[1])))
        self.assertEqual(solve(x,[27]*len(y),ridge),[['0','1']]*len(y))
        large_case=next(case for case in self.codes['c_l11_hard']['tests']
                        if any(pair and (abs(int(pair[0]))>2**53 or int(pair[1])>2**53) for pair in case['expected']))
        value=solve(*large_case['args'])
        self.assertEqual(json.loads(json.dumps(value)),value)
        for pair in value:
            self.assertEqual(str(int(pair[0])),pair[0]);self.assertEqual(str(int(pair[1])),pair[1])
            self.assertGreater(int(pair[1]),0)
            self.assertEqual(F(int(pair[0]),int(pair[1])).denominator,int(pair[1]))

    def test_actual_judge_and_wrong_training_shortcuts(self):
        from judge import run
        for id in ('c_l11_easy','c_l11_hard'):
            result=run(id,self.codes[id]['solution'],'submit')
            self.assertNotIn('error',result,id)
            self.assertEqual(result['passed'],result['total'],id)
        wrong='def solve(features, targets, ridge):\n    return [["0","1"] for _ in targets]'
        result=run('c_l11_hard',wrong,'submit')
        self.assertLess(result['passed'],result['total'])
        wrong='def solve(x,y,intercept,slope):\n    return sum(v-intercept-slope*u for u,v in zip(x,y)) == 0'
        result=run('c_l11_easy',wrong,'submit')
        self.assertLess(result['passed'],result['total'])


if __name__ == '__main__':
    unittest.main()
