"""Likelihood mechanisms checked by enumeration, quadrature and Decimal scores.

The truncated-fit oracle solves an algebraically different score with Decimal
exponentials. It uses neither the reference's small-root series nor expm1.
"""
import copy
import itertools
import json
import math
import random
import unittest
from decimal import Decimal as D, localcontext
from fractions import Fraction as F

from coding_bank import TASKS
from judge import run
from test_topic_practice import BANK, CODES, QUESTIONS, reference


def selected_fit(waits, cutoff):
    if not waits or 2*sum(waits)>=len(waits)*cutoff:return None
    with localcontext() as ctx:
        ctx.prec=85
        mean=D(sum(waits))/D(len(waits)*cutoff)
        low,high=D(0),1/mean
        for _ in range(340):
            z=(low+high)/2
            q=(-z).exp()
            # Multiplying the score by z*(1-exp(-z)) gives this expression.
            # All arithmetic is high precision; tiny roots need no series.
            numerator=(1-mean*z)*(1-q)-z*q
            if numerator>0:low=z
            else:high=z
        z=(low+high)/2
        return [float(z),float(z/D(cutoff))]


def log_phi(x,mean,variance):
    return -.5*math.log(2*math.pi*variance)-(x-mean)**2/(2*variance)


def quadrature_moments(z, cells=20000):
    xs=[(i+.5)/cells for i in range(cells)]
    weights=[math.exp(-z*x) for x in xs]
    norm=math.fsum(weights)
    first=math.fsum(x*w for x,w in zip(xs,weights))/norm
    second=math.fsum(x*x*w for x,w in zip(xs,weights))/norm
    return first,second-first*first


class LikelihoodPracticeTests(unittest.TestCase):
    def assertFitClose(self,actual,expected):
        if expected is None:self.assertIsNone(actual);return
        self.assertIsNotNone(actual)
        for x,y in zip(actual,expected):
            self.assertLessEqual(abs(x-y),max(2e-13,abs(y)*3e-14),f'{x} != {y}')

    def test_record_count_and_conditioned_count(self):
        records=list(itertools.product((0,1),repeat=5))
        record=(1,0,1,1,0)
        likelihood=lambda p,x:p**sum(x)*(1-p)**(len(x)-sum(x))
        ratio=likelihood(F(3,4),record)/likelihood(F(1,2),record)
        self.assertEqual(ratio,F(27,32))
        self.assertEqual(QUESTIONS['q_l25_e1']['answer'],float(ratio))
        for p in [F(1,5),F(1,2),F(3,4),F(9,10)]:
            count_mass=sum(likelihood(p,x) for x in records if sum(x)==3)
            self.assertEqual(count_mass,10*likelihood(p,record))
            self.assertEqual(likelihood(p,record)/count_mass,F(1,10))
        self.assertEqual(QUESTIONS['q_l25_e2']['answer'],.9)
        self.assertTrue(all(F(k,10)**8<F(9,10)**8 for k in range(9)))

    def test_rounded_bin_likelihood_and_global_score(self):
        # At lambda=log 2, a one-second bin has exact mass 2^(-k-1).
        bins=[0,1,2,1]
        probability=math.prod(F(1,2**(k+1)) for k in bins)
        self.assertEqual(probability,F(1,256))
        self.assertEqual(QUESTIONS['q_l25_m1']['answer'],math.log(2))
        for rate in [.01,.1,.4,math.log(2),1,10]:
            integrated=math.prod(math.exp(-rate*k)-math.exp(-rate*(k+1)) for k in bins)
            algebra=(1-math.exp(-rate))**4*math.exp(-rate*4)
            self.assertAlmostEqual(integrated,algebra,places=14)
            score=4/math.expm1(rate)-4
            if rate<math.log(2):self.assertGreater(score,0)
            elif rate>math.log(2):self.assertLess(score,0)
            else:self.assertAlmostEqual(score,0,places=14)
        self.assertNotAlmostEqual(math.log(2),4/sum(bins))
        self.assertTrue(all((1-math.exp(-b))**4>(1-math.exp(-a))**4
                            for a,b in zip([.1,1,10],[1,10,100])))

    def test_truncated_mean_and_derivative_by_quadrature(self):
        # Integrating the bounded tilted density is separate from the reference
        # root function and checks the variance argument in the written proof.
        for z in [0,.001,.1,1,3,10]:
            mean,variance=quadrature_moments(z)
            if z==0:self.assertAlmostEqual(mean,.5,places=14)
            else:self.assertAlmostEqual(mean,1/z-1/math.expm1(z),delta=3e-9)
            self.assertGreater(variance,0)
            step=1e-4
            left=quadrature_moments(z-step)[0]
            right=quadrature_moments(z+step)[0]
            self.assertAlmostEqual((right-left)/(2*step),-variance,delta=3e-9)
        # Conditional retained-only likelihood decreases if mean >= c/2.
        for mean in [.5,.75]:
            for z in [.01,.1,1,10]:
                model_mean=quadrature_moments(z)[0]
                self.assertLess(model_mean-mean,0)
        self.assertEqual(F(1,F(3,4)+1),F(4,7))
        self.assertIsNone(selected_fit([3],4))

    def test_mixture_witness_bounds_whole_record(self):
        xs=[-10,0,8]
        fixed_sum=sum(log_phi(x,0,1)-math.log(2) for x in xs[1:])
        previous_bound=-math.inf
        for epsilon in [1,.1,.01,.001,1e-12]:
            bound=-math.log(2)-.5*math.log(2*math.pi)-math.log(epsilon)+fixed_sum
            self.assertGreater(bound,previous_bound)
            logs=[]
            for x in xs:
                first=log_phi(x,xs[0],epsilon*epsilon)-math.log(2)
                second=log_phi(x,0,1)-math.log(2)
                top=max(first,second)
                logs.append(top+math.log(math.exp(first-top)+math.exp(second-top)))
            self.assertGreaterEqual(sum(logs)+1e-12,bound)
            previous_bound=bound
        # The bound's log grows by log(1/epsilon) plus a finite fixed constant.
        self.assertAlmostEqual(previous_bound-(-math.log(2)-.5*math.log(2*math.pi)+fixed_sum),math.log(1e12))

    def test_variance_floor_compact_box_does_not_decrease_densities(self):
        rng=random.Random(2525)
        for _ in range(500):
            xs=[rng.uniform(-10,10) for _ in range(5)]
            lower,upper=min(xs),max(xs);span=upper-lower
            floor=rng.uniform(.001,100)
            mean=rng.uniform(-100,100);variance=floor+rng.uniform(0,20000)
            clipped=min(upper,max(lower,mean))
            capped=min(variance,max(floor,span*span))
            for x in xs:
                original=log_phi(x,mean,variance)
                changed=log_phi(x,clipped,capped)
                self.assertGreaterEqual(changed+1e-12,original)
        # Source proof supplies compactness/continuity; numerical points alone
        # do not prove the existence theorem or global optimisation.

    def test_bernoulli_interval_fit_by_exact_likelihood(self):
        solve=reference('c_l25_easy');bounds=[F(j,4) for j in range(5)]
        for n in range(11):
            for s in range(n+1):
                for low,high in itertools.combinations_with_replacement(bounds,2):
                    candidates=set([low,high])
                    if n and low<=F(s,n)<=high:candidates.add(F(s,n))
                    def likelihood(p):return p**s*(1-p)**(n-s)
                    best=max(likelihood(p) for p in candidates)
                    expected=None if best==0 else float(min(p for p in candidates if likelihood(p)==best))
                    self.assertEqual(solve(s,n,float(low),float(high)),expected)
        for case in CODES['c_l25_easy']['samples']+CODES['c_l25_easy']['tests']:
            self.assertEqual(solve(*case['args']),case['expected'])
        self.assertIsNone(solve(10**18-1,10**18,1,1))

    def test_small_root_series_by_exact_formal_division(self):
        # expm1(z)/z = sum z^k/(k+1)!. Invert its polynomial coefficients
        # as rationals; this checks all constants without using the reference.
        a=[F(1,math.factorial(k+1)) for k in range(11)]
        inverse=[F(1)]
        for n in range(1,11):inverse.append(-sum(a[k]*inverse[n-k] for k in range(1,n+1)))
        self.assertEqual(inverse[1],F(-1,2))
        self.assertEqual([inverse[i] for i in [2,4,6,8,10]],
                         [F(1,12),F(-1,720),F(1,30240),F(-1,1209600),F(1,47900160)])
        self.assertTrue(all(inverse[i]==0 for i in [3,5,7,9]))
        self.assertLess(float(F(1,100)**9/F(47900160)),2.1e-26)

    def test_selected_fit_against_independent_decimal_score(self):
        solve=reference('c_l25_hard');rng=random.Random(2526)
        for _ in range(150):
            cutoff=rng.randint(2,300)
            waits=[rng.randint(1,cutoff-1) for _ in range(rng.randrange(1,25))]
            original=waits.copy()
            self.assertFitClose(solve(waits,cutoff),selected_fit(waits,cutoff))
            self.assertEqual(waits,original)
        for case in CODES['c_l25_hard']['samples']+CODES['c_l25_hard']['tests']:
            expected=selected_fit(*case['args'])
            self.assertFitClose(case['expected'],expected)
            self.assertFitClose(solve(*case['args']),expected)

    def test_scaled_units_permutations_and_exact_existence(self):
        solve=reference('c_l25_hard')
        for waits,cutoff in [([1,2,3],8),([49],100),([499999999999],10**12),([1],10**12)]:
            result=solve(waits,cutoff)
            self.assertFitClose(result,solve(list(reversed(waits)),cutoff))
            if cutoff<10**12:
                scaled=solve([7*x for x in waits],7*cutoff)
                self.assertFitClose([scaled[0],scaled[1]*7],result)
        self.assertIsNone(solve([],100))
        self.assertIsNone(solve([3,7],10))
        self.assertIsNone(solve([3,8],10))
        tiny=solve([499999999999],10**12)
        self.assertGreater(tiny[0],0)
        self.assertFitClose(tiny,selected_fit([499999999999],10**12))
        # Near the half-mean threshold, comparing exact integers is needed.
        near=[499999999999]*100000
        self.assertFitClose(solve(near,10**12),selected_fit([near[0]],10**12))
        self.assertTrue(all(x==499999999999 for x in near))

    def test_published_references_judge_and_debug_copy_limits(self):
        for id in ['c_l25_easy','c_l25_hard']:
            result=run(id,CODES[id]['solution'])
            self.assertEqual(result.get('passed'),result.get('total'),result)
            self.assertGreater(result.get('total',0),1)
            for case in CODES[id]['samples']+CODES[id]['tests']:
                self.assertLessEqual(len(json.dumps(case['args']))+len(json.dumps(case['expected'])),200000)
        wrong='''def solve(waits,cutoff):
    if not waits:return None
    rate=len(waits)/sum(waits)
    return [rate*cutoff,rate]'''
        result=run('c_l25_hard',wrong)
        self.assertLess(result['passed'],result['total'])
        wrong='''def solve(successes,trials,low,high):
    return max(low,min(high,(successes+1)/(trials+2)))'''
        result=run('c_l25_easy',wrong)
        self.assertLess(result['passed'],result['total'])

    def test_coverage_and_specific_preserved_assessments(self):
        lesson=next(l for l in BANK['lessons'] if l['id']=='l25')
        self.assertEqual(lesson['questions'][:3],['q49','q50','q51'])
        self.assertEqual(lesson['coding'],['c_l25_easy','c15','c_l25_hard'])
        self.assertEqual(len(lesson['questions']),8)
        self.assertTrue(lesson['practiceExpanded'])
        for id in ['q49','q50','q51']:
            self.assertNotIn('State the assumptions and the object you are computing.',QUESTIONS[id]['rubric'])
        self.assertEqual(CODES['c15']['difficulty'],'Medium')


if __name__=='__main__':unittest.main()
