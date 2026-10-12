"""Independent finite probability, closed-testing and randomization oracles."""
import copy
import itertools
import math
import random
import unittest
from collections import Counter
from fractions import Fraction as F
from coding_bank import TASKS
from judge import run, submission_cases, parse_debug_cases
from test_topic_practice import BANK, QUESTIONS, reference


def pair(x):
    x=F(x)
    return [str(x.numerator),str(x.denominator)]


def closed_bonferroni(p_values,alpha):
    # All intersections, not sorted step-down or its running-maximum formula.
    ps=[F(*p) for p in p_values];m=len(ps);adj=[F(0)]*m
    for membership in itertools.product((0,1),repeat=m):
        indices=[i for i,b in enumerate(membership) if b]
        if not indices: continue
        intersection=min(F(1),len(indices)*min(ps[i] for i in indices))
        for i in indices: adj[i]=max(adj[i],intersection)
    return {'adjusted':[pair(x) for x in adj],
            'rejected':[i for i,x in enumerate(adj) if x<=F(*alpha)]}


def balanced(n):
    # Bitstring enumeration independent of production's index combinations.
    return [bits for bits in itertools.product((0,1),repeat=n) if sum(bits)==n//2]


def randomization_oracle(features,assignment):
    n=len(features);m=len(features[0]);k=n//2
    def statistics(bits):
        return [abs(sum(F(row[j],k) for row,b in zip(features,bits) if b)
                    -sum(F(row[j],k) for row,b in zip(features,bits) if not b)) for j in range(m)]
    obs=statistics(assignment)
    null=[max(statistics(bits)) for bits in balanced(n)]
    tail=lambda t:pair(F(sum(x>=t for x in null),len(null)))
    return {'statistics':[pair(x) for x in obs], 'adjusted':[tail(x) for x in obs], 'global_p':tail(max(obs))}


class SearchPracticeTests(unittest.TestCase):
    def test_contract_ids_and_specific_rubrics(self):
        lesson=next(l for l in BANK['lessons'] if l['id']=='l15')
        self.assertEqual(lesson['questions'][:3],['q04','q25','q32'])
        self.assertEqual(Counter(QUESTIONS[x]['difficulty'] for x in lesson['questions']),Counter(Easy=2,Medium=2,Hard=2))
        self.assertEqual(lesson['coding'],['c_l15_easy','c_l15_medium','c_l15_hard'])
        for qid in lesson['questions']:
            self.assertGreaterEqual(len(QUESTIONS[qid]['rubric']),3)
            self.assertNotIn('State the assumptions and the object you are computing.',QUESTIONS[qid]['rubric'])
        self.assertEqual(QUESTIONS['q04']['answer'],9/58)
        self.assertAlmostEqual(QUESTIONS['q25']['answer'],1-.95**20)

    def test_copy_events_and_discovery_targets(self):
        any_false=expected_false=F(0)
        for blocks in itertools.product((0,1),repeat=3):
            mass=math.prod(F(1,10) if b else F(9,10) for b in blocks)
            any_false+=mass*any(blocks)
            expected_false+=mass*4*sum(blocks)
        self.assertEqual(any_false,F(271,1000));self.assertEqual(expected_false,F(6,5))
        self.assertEqual(QUESTIONS['q_l15_e2']['answer'],float(any_false))
        self.assertEqual(QUESTIONS['q_l15_e1']['answer'],.5)
        self.assertEqual(reference('c_l15_easy')([[0,0],[1,2]]),[.25,.5,.5])

    def test_discovery_summaries_exact_oracle_and_maximum(self):
        rng=random.Random(1501);solve=reference('c_l15_easy')
        for _ in range(150):
            runs=[]
            for _ in range(rng.randrange(1,100)):
                r=rng.randrange(1000);runs.append([rng.randrange(r+1),r])
            before=copy.deepcopy(runs)
            fdr=sum((F(v,max(1,r)) for v,r in runs),F(0))/len(runs)
            fwer=F(sum(v>0 for v,r in runs),len(runs))
            total=sum(r for v,r in runs)
            pooled=F(sum(v for v,r in runs),total) if total else None
            actual=solve(runs)
            for a,b in zip(actual,[fdr,fwer,pooled]):
                if b is None: self.assertIsNone(a)
                else: self.assertAlmostEqual(a,float(b),places=12)
            self.assertEqual(runs,before)
        self.assertEqual(solve([[1,2]]*50000+[[0,0]]*50000),[.25,.5,.5])

    def test_holm_against_closed_intersections(self):
        solve=reference('c_l15_medium')
        for m in range(5):
            for values in itertools.product((F(0),F(1,4),F(1,2),F(1)),repeat=m):
                ps=[[x.numerator,x.denominator] for x in values]
                for alpha in ([0,1],[1,4],[1,2],[1,1]):
                    self.assertEqual(solve(ps,alpha),closed_bonferroni(ps,alpha))
        rng=random.Random(1502)
        for _ in range(150):
            ps=[[rng.randrange(101),100] for _ in range(rng.randrange(1,9))]
            alpha=[rng.randrange(101),100]
            before=copy.deepcopy([ps,alpha])
            self.assertEqual(solve(ps,alpha),closed_bonferroni(ps,alpha))
            self.assertEqual([ps,alpha],before)
            scaled=[[3*a,3*b] for a,b in ps]
            self.assertEqual(solve(scaled,alpha),solve(ps,alpha))

    def test_holm_strong_fwer_with_false_nulls_and_copied_true_nulls(self):
        solve=reference('c_l15_medium');grid=6
        for alternative in (F(0),F(1,20),F(1)):
            for copied in (False,True):
                support=list(itertools.product(range(1,grid+1),repeat=1 if copied else 2))
                for alpha in (F(0),F(1,6),F(1,3),F(1,2),F(1)):
                    false=0
                    for values in support:
                        p1=F(values[0],grid);p2=p1 if copied else F(values[1],grid)
                        ps=[[x.numerator,x.denominator] for x in (alternative,p1,p2)]
                        result=solve(ps,[alpha.numerator,alpha.denominator])
                        false+=any(i in result['rejected'] for i in (1,2))
                    self.assertLessEqual(F(false,len(support)),alpha)

    def test_holm_maximum_ties_and_near_boundaries(self):
        solve=reference('c_l15_medium');ps=[[1,40000]]*20000;before=copy.deepcopy(ps)
        result=solve(ps,[1,2]);self.assertEqual(result['adjusted'],[['1','2']]*20000)
        self.assertEqual(result['rejected'],list(range(20000)));self.assertEqual(ps,before)
        self.assertEqual(solve(ps,[499999999,10**9])['rejected'],[])
        self.assertEqual(solve([[1,10],[1,10],[2,5]],[3,10]),closed_bonferroni([[1,10],[1,10],[2,5]],[3,10]))

    def test_randomization_seeded_exact_joint_oracle(self):
        rng=random.Random(1503);solve=reference('c_l15_hard')
        for n in (2,4,6,8):
            for _ in range(25):
                matrix=[[rng.randrange(-5,6) for _ in range(rng.randrange(1,5))]]
                m=len(matrix[0]);matrix += [[rng.randrange(-5,6) for _ in range(m)] for i in range(n-1)]
                assignment=list(rng.choice(balanced(n)))
                before=copy.deepcopy([matrix,assignment])
                self.assertEqual(solve(matrix,assignment),randomization_oracle(matrix,assignment))
                self.assertEqual([matrix,assignment],before)

    def test_global_null_rank_calibration_including_ties(self):
        solve=reference('c_l15_hard')
        for features in ([[0],[0],[1],[1]],[[0,0],[0,1],[1,1],[1,0]],[[0]]*6,[[0,1],[2,1],[3,0],[4,5],[0,1],[3,2]]):
            outputs=[solve(features,list(bits)) for bits in balanced(len(features))]
            ps=[F(*map(int,r['global_p'])) for r in outputs]
            for alpha in sorted(set(ps+[F(0),F(1,20),F(1,2),F(1)])):
                self.assertLessEqual(F(sum(p<=alpha for p in ps),len(ps)),alpha)
                any_rejected=[any(F(*map(int,p))<=alpha for p in r['adjusted']) for r in outputs]
                self.assertEqual(any_rejected,[p<=alpha for p in ps])
            for result in outputs:
                self.assertEqual(F(*map(int,result['global_p'])),min(F(*map(int,p)) for p in result['adjusted']))
                self.assertGreater(F(*map(int,result['global_p'])),0)

    def test_randomization_invariance_and_marginal_bound(self):
        solve=reference('c_l15_hard');matrix=[[0,0],[0,1],[2,0],[2,1]];bits=[0,0,1,1]
        original=solve(matrix,bits)
        self.assertEqual(solve(matrix,[1-b for b in bits]),original)
        order=[2,0,3,1]
        self.assertEqual(solve([matrix[i] for i in order],[bits[i] for i in order]),original)
        duplicated=solve([row+[row[0],-row[1]] for row in matrix],bits)
        self.assertEqual(duplicated['global_p'],original['global_p'])
        self.assertEqual(duplicated['adjusted'][:2],original['adjusted'])
        for j,p in enumerate(original['adjusted']):
            individual=solve([[row[j]] for row in matrix],bits)['global_p']
            self.assertGreaterEqual(F(*map(int,p)),F(*map(int,individual)))
        permuted=solve([list(reversed(row)) for row in matrix],bits)
        self.assertEqual(permuted['adjusted'],list(reversed(original['adjusted'])))

    def test_randomization_maximum_bound_analytic_tail(self):
        solve=reference('c_l15_hard');matrix=[[-10**6]*8]*9+[[10**6]*8]*9;bits=[0]*9+[1]*9
        expected={'statistics':[['2000000','1']]*8,'adjusted':[['1','24310']]*8,'global_p':['1','24310']}
        # Only the two pure splits attain the largest possible difference.
        self.assertEqual(math.comb(18,9)//2,24310)
        self.assertEqual(solve(matrix,bits),expected)

    def test_gaussian_winner_integral_and_unequal_mean_formula(self):
        # Independent quadrature of the truncated standard-normal expectation.
        for threshold in (-3.,-1.,0.,1.,3.):
            steps=20000;upper=10.;h=(upper-threshold)/steps
            density=lambda z: math.exp(-z*z/2)/math.sqrt(2*math.pi)
            values=[(threshold+i*h)*density(threshold+i*h) for i in range(steps+1)]
            integral=h/3*(values[0]+values[-1]+4*sum(values[1:-1:2])+2*sum(values[2:-1:2]))
            self.assertAlmostEqual(integral,density(threshold),places=10)
        for rho in (-1.,0.,.5,1.):
            var_s=(1+rho)/2;var_d=(1-rho)/2
            bias=math.sqrt(2*var_d/math.pi)
            self.assertAlmostEqual(var_s+var_d-bias*bias,1-(1-rho)/math.pi)
            if rho<1:
                s=math.sqrt(2*(1-rho));self.assertAlmostEqual(s/math.sqrt(2*math.pi),bias)
        self.assertEqual(math.sqrt((1-1)/math.pi),0)

    def test_actual_judge_exact_debug_roundtrip_and_preservation(self):
        for id in ('c_l15_easy','c_l15_medium','c_l15_hard'):
            task=next(t for t in TASKS if t['id']==id)
            cases=task['samples']+task['tests']
            before=copy.deepcopy(cases)
            result=run(id,task['solution'])
            self.assertEqual(result['passed'],result['total'],(id,result))
            self.assertEqual(cases,before)
            for case in cases:
                code=reference(id);args=copy.deepcopy(case['args']);code(*args)
                self.assertEqual(args,case['args'])
            copies=submission_cases(id)['cases']
            for copied,original in zip(copies,cases):
                self.assertEqual(parse_debug_cases(task,[copied]),[original])
            if id=='c_l15_hard':
                for case in cases:
                    matrix,bits=case['args'];n=len(matrix);m=len(matrix[0])
                    self.assertTrue(n%2==0 and 2<=n<=18 and 1<=m<=8)
                    self.assertEqual(sum(bits),n//2)
                    self.assertTrue(all(len(row)==m and all(abs(x)<=10**6 for x in row) for row in matrix))
                    if n<=8: self.assertEqual(case['expected'],randomization_oracle(matrix,bits))

if __name__=='__main__': unittest.main()
