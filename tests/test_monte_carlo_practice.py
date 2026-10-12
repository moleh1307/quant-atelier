"""Exact finite-world and exhaustive allocation oracles; no personal records."""
import copy
import itertools
import math
import random
import unittest
from collections import Counter
from fractions import Fraction as F
from coding_bank import TASKS
from judge import run,submission_cases,parse_debug_cases
from test_topic_practice import BANK,QUESTIONS,reference


def positive_compositions(total,k):
    if k==1:
        yield (total,)
    else:
        for first in range(1,total-k+2):
            for rest in positive_compositions(total-first,k-1):yield (first,)+rest


def allocation_oracle(weights,variances,budget):
    # Enumerate ALL feasible integer allocations, independent of marginal heaps.
    w=sum(weights)
    candidates=((sum((F(a*a*v,w*w*n) for a,v,n in zip(weights,variances,ns)),F(0)),tuple(-n for n in ns),ns)
                for ns in positive_compositions(budget,len(weights)))
    value,_,ns=min(candidates)
    return {'allocation':list(ns),'variance':[str(value.numerator),str(value.denominator)]}


def pair_oracle(pairs):
    if not pairs:return [None,None]
    values=[F(a+b,2) for a,b in pairs];n=len(values);mean=sum(values)/n
    return [float(mean),None if n==1 else math.sqrt(float(sum((v-mean)**2 for v in values)/(n*(n-1))))]


class MonteCarloPracticeTests(unittest.TestCase):
    def test_contract_retained_slots_and_rubrics(self):
        lesson=next(l for l in BANK['lessons'] if l['id']=='l17')
        self.assertEqual(lesson['questions'][:2],['q43','q48'])
        self.assertEqual(Counter(QUESTIONS[q]['difficulty'] for q in lesson['questions']),Counter(Easy=2,Medium=2,Hard=2))
        self.assertEqual(lesson['coding'],['c_l17_easy','c12','c_l17_hard'])
        for id in lesson['questions']:
            self.assertGreaterEqual(len(QUESTIONS[id]['rubric']),3)
            self.assertNotIn('State the assumptions and the object you are computing.',QUESTIONS[id]['rubric'])
        self.assertIn('finite second moments',QUESTIONS['q48']['prompt'])
        self.assertIn('correlation is undefined',QUESTIONS['q48']['solution'])

    def test_independent_units_equal_cost_and_covariance(self):
        self.assertEqual(F(36,256),F(3,8)**2)
        self.assertEqual(QUESTIONS['q_l17_e1']['answer'],3/8)
        # Explicit +/-2 joint law with identical marginals and covariance -3.
        worlds=[(-2,-2,F(1,16)),(-2,2,F(7,16)),(2,-2,F(7,16)),(2,2,F(1,16))]
        self.assertEqual(sum(p*x*y for x,y,p in worlds),-3)
        paired=sum(p*(F(x+y,2))**2 for x,y,p in worlds)
        self.assertEqual(paired,F(1,2));self.assertEqual((paired/1000)/F(4,2000),F(1,4))
        self.assertEqual(QUESTIONS['q_l17_e2']['answer'],1/4)
        self.assertEqual(F(4,1000)/F(4,2000),2)

    def test_zero_hit_bound_fixed_count_endpoints_and_selection(self):
        alpha=.05;upper=lambda n:-math.expm1(math.log(alpha)/n)
        self.assertAlmostEqual(upper(1000),.00299125,places=8)
        self.assertAlmostEqual(math.log(alpha)/math.log(.999),2994.234,places=3)
        self.assertGreater(upper(2994),.001);self.assertLessEqual(upper(2995),.001)
        # Rational grid avoids using rounded numerical endpoints for coverage.
        for n in range(1,15):
            for p in (F(i,20) for i in range(21)):
                # Sum coverage across the full binomial observation law, not just K=0.
                coverage=F(0)
                for hits in range(n+1):
                    probability=math.comb(n,hits)*p**hits*(1-p)**(n-hits)
                    if hits or float(p)<=upper(n):coverage+=probability
                self.assertGreaterEqual(coverage,F(19,20))
                if p==0 or p==1:self.assertEqual(coverage,1)
        # For p=1/2, block length 2995, repeated independent inspections eventually hit.
        block_zero=F(1,2)**2995
        self.assertGreater(block_zero,0);self.assertLess(1-block_zero,1)
        self.assertIn('almost surely',QUESTIONS['q_l17_m1']['followSolution'])

    def test_same_sample_secant_nine_worlds(self):
        values=[];correction=[]
        for a,b in itertools.product(range(3),repeat=2):
            c=a+b if a!=b else 0
            values.append(F(a*a+b*b,2)-c*(F(a+b,2)-1))
            correction.append(c*(F(a+b,2)-1))
        self.assertEqual(values,[0,1,2,1,1,1,2,1,4])
        self.assertEqual(sum(values)/9,F(13,9));self.assertEqual(sum(correction)/9,F(2,9))
        self.assertEqual(QUESTIONS['q_l17_m2']['answer'],13/9)

    def test_independent_pilot_all_81_worlds(self):
        worlds=[];cs=[]
        for a,b in itertools.product(range(3),repeat=2):
            c=a+b if a!=b else 0;cs.append(c);conditional=[]
            for x,y in itertools.product(range(3),repeat=2):
                t=F(x*x+y*y,2)-c*(F(x+y,2)-1);conditional.append(t);worlds.append(t)
            self.assertEqual(sum(conditional)/9,F(5,3))
        self.assertEqual(F(sum(cs),9),F(4,3));self.assertEqual(F(sum(c*c for c in cs),9),F(28,9))
        mean=sum(worlds)/81
        self.assertEqual(mean,F(5,3));self.assertEqual(sum((t-mean)**2 for t in worlds)/81,F(19,27))
        optimum=[F(x*x+y*y,2)-2*(F(x+y,2)-1) for x,y in itertools.product(range(3),repeat=2)]
        self.assertEqual(sum((t-mean)**2 for t in optimum)/9,F(1,9))
        self.assertEqual(F(19,27)-F(1,9),F(16,27))

    def test_uniform_squared_antithetic_and_control_degeneracy(self):
        # Integrate polynomial coefficients exactly on [0,1].
        integral=lambda coefficients:sum((F(c,i+1) for i,c in enumerate(coefficients)),F(0))
        mean=integral([0,0,1]);variance=integral([0,0,0,0,1])-mean**2
        covariance=integral([0,0,1,-2,1])-mean**2
        self.assertEqual(variance,F(4,45));self.assertEqual(covariance,-F(7,90))
        self.assertEqual((variance+covariance)/2,F(1,180))
        self.assertEqual((variance/2)/F(1,180),8)
        # Constant target Y=7 has zero covariance and residual variance, undefined corr.
        x=[F(0),F(1),F(2)];y=[F(7)]*3
        mx=sum(x)/3;my=sum(y)/3
        self.assertEqual(sum((a-mx)*(b-my) for a,b in zip(x,y))/3,0)
        self.assertEqual(sum((b-my)**2 for b in y)/3,0)

    def test_pair_uncertainty_centered_oracle_maximum_and_preservation(self):
        solve=reference('c_l17_easy');rng=random.Random(1701)
        for _ in range(250):
            offset=rng.choice((0,10**9-10,-10**9+10));n=rng.randrange(30)
            args=[[offset+rng.randrange(-5,6),offset+rng.randrange(-5,6)] for _ in range(n)];before=copy.deepcopy(args)
            self.assertEqual(solve(args),pair_oracle(args));self.assertEqual(args,before)
        n=100000;pairs=[[10**9,10**9]]*(n//2)+[[10**9-2,10**9-2]]*(n//2)
        self.assertEqual(solve(pairs),[10**9-1,math.sqrt(1/(n-1))])
        self.assertEqual(solve([[10**9,10**9],[10**9-1,10**9]]),[10**9-.25,.25])

    def test_retained_control_fixed_coefficient_centered_oracle(self):
        solve=reference('c12');rng=random.Random(1702)
        for _ in range(200):
            n=rng.randrange(15);x=[F(rng.randrange(-10,11),2) for _ in range(n)]
            y=[F(rng.randrange(-10,11),2) for _ in range(n)];mu=F(rng.randrange(-3,4),2);beta=F(rng.randrange(-4,5),2)
            args=[[float(v) for v in x],[float(v) for v in y],float(mu),float(beta)];before=copy.deepcopy(args)
            z=[a-beta*(b-mu) for a,b in zip(x,y)];result=solve(*args)
            if not n:expected=[None,None]
            else:
                mean=sum(z)/n;expected=[float(mean),None if n==1 else math.sqrt(float(sum((v-mean)**2 for v in z)/(n*(n-1))))]
            for a,b in zip(result,expected):
                if b is None:self.assertIsNone(a)
                else:self.assertAlmostEqual(a,b,places=12)
            self.assertEqual(args,before)
        self.assertEqual(solve([1,2,3],[1,2,3],2,1),[2.,0.])

    def test_integer_allocation_exhaustive_positive_compositions(self):
        solve=reference('c_l17_hard');rng=random.Random(1703)
        for _ in range(180):
            k=rng.randrange(1,6);w=[rng.randrange(4) for _ in range(k)];v=[rng.randrange(6) for _ in range(k)]
            if not sum(w):w[0]=1
            b=rng.randrange(k,13);args=[w,v,b];before=copy.deepcopy(args)
            self.assertEqual(solve(*args),allocation_oracle(*args));self.assertEqual(args,before)
        for w,v in itertools.product(itertools.product(range(3),repeat=2),repeat=2):
            if not sum(w):continue
            for b in range(2,9):self.assertEqual(solve(list(w),list(v),b),allocation_oracle(w,v,b))

    def test_exact_priority_scaling_and_budget_monotonicity(self):
        solve=reference('c_l17_hard');a,b=543339720,768398401
        self.assertEqual(b*b-2*a*a,1);self.assertEqual(float(b*b),float(2*a*a))
        self.assertEqual(solve([a,b],[2,1],3),allocation_oracle([a,b],[2,1],3))
        self.assertEqual(solve([1,1,1],[1,1,1],5)['allocation'],[2,2,1])
        w=[1,3,2];v=[2,1,4];previous=None
        for budget in range(3,25):
            base=solve(w,v,budget);self.assertEqual(solve([x*2 for x in w],v,budget),base)
            scaled=solve(w,[x*7 for x in v],budget)
            self.assertEqual(scaled['allocation'],base['allocation'])
            value=F(*map(int,base['variance']));self.assertEqual(F(*map(int,scaled['variance'])),7*value)
            if previous is not None:self.assertLessEqual(value,previous)
            previous=value

    def test_full_allocation_bounds_and_zero_gains(self):
        solve=reference('c_l17_hard');k=20000;budget=200000
        self.assertEqual(solve([1]*k,[1]*k,budget),{'allocation':[10]*k,'variance':['1','200000']})
        self.assertEqual(solve([10**9]*k,[0]*k,budget),{'allocation':[budget-k+1]+[1]*(k-1),'variance':['0','1']})
        self.assertEqual(solve([0,2,1],[9,0,4],5),allocation_oracle([0,2,1],[9,0,4],5))

    def test_actual_judge_official_oracles_and_lossless_debug(self):
        for id in ('c_l17_easy','c12','c_l17_hard'):
            task=next(t for t in TASKS if t['id']==id);result=run(id,task['solution'])
            self.assertNotIn('error',result,id);self.assertEqual(result['passed'],result['total'],id)
            for original,copied in zip(task['samples']+task['tests'],submission_cases(id)['cases']):
                self.assertEqual(parse_debug_cases(task,[copied]),[original])
                self.assertLessEqual(len(copied['argumentsJSON'])+len(copied['expectedJSON']),200000)
                if id=='c_l17_hard' and original['args'][2]<=20:
                    self.assertEqual(original['expected'],allocation_oracle(*original['args']))

if __name__=='__main__':unittest.main()
