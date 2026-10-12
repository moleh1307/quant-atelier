"""Independent squared-loss calculations and predictive probability oracles.

Small predictions use beta-integral moments as exact fractions; large ones use
an endpoint-based Decimal distribution, independent of the mode-based reference.
All coding/judge checks run without reading or writing personal progress.
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


def rising(x, n):
    return math.prod(x+i for i in range(n))


def predictive_moments(a, b, m):
    """Integrate each conditional binomial mass using exact beta moments."""
    divisor = rising(a+b,m)
    return [F(math.comb(m,k)*rising(a,k)*rising(b,m-k),divisor)
            for k in range(m+1)]


def decimal_prediction(a, b, m, thresholds):
    """Full PMF from the endpoint; Decimal retains even tiny endpoint masses."""
    with localcontext() as ctx:
        ctx.prec=85
        initial=D(1)
        for j in range(m):
            initial*=D(b+j)/D(a+b+j)
        masses=[initial]
        for k in range(m):
            masses.append(masses[-1]*D(m-k)*D(a+k)/(D(k+1)*D(b+m-k-1)))
        # This oracle does not renormalise. Its integral construction should
        # already sum to one, even where a float endpoint would be zero.
        assert abs(sum(masses)-1)<D('1e-65')
        return [float(sum(masses[r:])) for r in thresholds]


def posterior_summaries(alpha,beta,batches):
    # Prefix slicing and exact raw posterior moments intentionally do not use
    # the reference's mutable cumulative counts or variance factorisation.
    result=[]
    for i in range(len(batches)):
        a=alpha+sum(s for s,f in batches[:i+1])
        b=beta+sum(f for s,f in batches[:i+1])
        mean=F(a,a+b)
        second=F(a*(a+1),(a+b)*(a+b+1))
        result.append([float(mean),float(second-mean**2)])
    return result


class EstimationPracticeTests(unittest.TestCase):
    def assertVectorClose(self, actual, expected, tolerance=3e-12):
        self.assertEqual(len(actual),len(expected))
        for x,y in zip(actual,expected):
            if isinstance(x,list):self.assertVectorClose(x,y,tolerance)
            else:self.assertLessEqual(abs(x-y),tolerance,f'{x} != {y}')

    def test_easy_interview_and_prediction_noise(self):
        self.assertEqual(QUESTIONS['q_l09_e1']['answer'],2)
        self.assertEqual(F(12**2,36),4)
        # A finite, nonnormal iid model has the same exact variance identity.
        values=[-2,2]
        means=[F(x+y,2) for x,y in itertools.product(values,repeat=2)]
        self.assertEqual(sum(x*x for x in means)/len(means),2)
        errors=[(F(y)-x)**2 for x,y in itertools.product(means,values)]
        self.assertEqual(sum(errors)/len(errors),6)
        self.assertEqual(144+4,148)

    def test_uniform_endpoint_risks_by_polynomial_integration(self):
        for n in range(1,31):
            # Exact integration of (cx−1)^2 against n*x^(n−1) on [0,1].
            def integrated(c):
                coefficients=[n,-2*n*c,n*c*c]
                return sum(F(value,n+power) for power,value in enumerate(coefficients))
            optimal=F(n+2,n+1)
            best=integrated(optimal)
            raw=integrated(F(1))
            unbiased=integrated(F(n+1,n))
            self.assertEqual(best,F(1,(n+1)**2))
            self.assertEqual(raw,F(2,(n+1)*(n+2)))
            self.assertEqual(unbiased,F(1,n*(n+2)))
            self.assertLess(best,raw)
            self.assertLess(best,unbiased)
            self.assertEqual(optimal*F(n,n+1)-1,-best)
            for step in (F(-1),F(-1,7),F(1,7),F(1)):
                self.assertEqual(integrated(optimal+step)-best,F(n,n+2)*step**2)
            # The mean rule's independently known mean/variance also yields
            # its exact risk, showing where the maximum comparison is strict.
            a=F(6*n,3*n+1)
            mean_risk=a*a/F(12*n)+(a/F(2)-1)**2
            self.assertEqual(mean_risk,F(1,3*n+1))
            self.assertLessEqual(best,mean_risk)
            self.assertEqual(best==mean_risk,n==1)

    def test_constant_risk_by_actual_binomial_enumeration(self):
        for n in range(1,45):
            a=math.sqrt(n)/2
            expected=1/(4*(math.sqrt(n)+1)**2)
            for p in [0,.001,.1,.25,.5,.9,.999,1]:
                actual=math.fsum(math.comb(n,k)*p**k*(1-p)**(n-k)*
                                 ((k+a)/(n+2*a)-p)**2 for k in range(n+1))
                self.assertAlmostEqual(actual,expected,places=13)
        # Square sample sizes give an entirely rational check of endpoints,
        # interior values, average risk, and a strict competing-rule bound.
        for root in range(1,6):
            n=root*root;a=F(root,2);risk=F(1,4*(root+1)**2)
            for p in map(lambda j:F(j,20),range(21)):
                actual=sum(math.comb(n,k)*p**k*(1-p)**(n-k)*
                           (F(k+a,n+2*a)-p)**2 for k in range(n+1))
                self.assertEqual(actual,risk)
            # Marginal probability of K under Beta(a,a) and integrated
            # posterior loss; this is a lower bound for any other rule.
            marginal=predictive_moments(a,a,n)
            averaged=F(0)
            for k,prob in enumerate(marginal):
                post_a=a+k;post_b=a+n-k;total=post_a+post_b
                variance=F(post_a*post_b,total**2*(total+1))
                averaged+=prob*variance
            self.assertEqual(averaged,risk)
            self.assertGreater(averaged+marginal[0]*F(1,25),risk)

    def test_uniform_prior_risk_piecewise_and_lesson_special_case(self):
        for n in range(1,31):
            risks=[]
            for p in map(lambda j:F(j,20),range(21)):
                risks.append(sum(math.comb(n,k)*p**k*(1-p)**(n-k)*
                                 (F(k+1,n+2)-p)**2 for k in range(n+1)))
            expected=F(max(4,n),4*(n+2)**2)
            self.assertEqual(max(risks),expected)
            minimax=1/(4*(math.sqrt(n)+1)**2)
            if n==4:self.assertAlmostEqual(float(expected),minimax,places=14)
            else:self.assertGreater(float(expected),minimax)
        self.assertEqual(max(risks),F(30,4*32**2))

    def test_posterior_batches_against_exact_prefix_moments(self):
        solve=reference('c_l09_easy');rng=random.Random(109)
        for _ in range(300):
            alpha,beta=rng.randint(1,20),rng.randint(1,20)
            batches=[[rng.randint(0,40),rng.randint(0,40)] for _ in range(rng.randrange(20))]
            original=copy.deepcopy(batches)
            self.assertVectorClose(solve(alpha,beta,batches),posterior_summaries(alpha,beta,batches))
            self.assertEqual(batches,original)
        for case in CODES['c_l09_easy']['samples']+CODES['c_l09_easy']['tests']:
            expected=posterior_summaries(*case['args'])
            self.assertVectorClose(case['expected'],expected)
            self.assertVectorClose(solve(*case['args']),expected)
        # Same total evidence, different batching: final posterior agrees.
        self.assertVectorClose(solve(3,5,[[2,1],[4,7]])[-1],solve(3,5,[[6,8]])[-1])

    def test_predictive_mass_by_exact_beta_integral(self):
        solve=reference('c_l09_hard')
        for a,b,m in itertools.product(range(1,6),range(1,6),range(13)):
            masses=predictive_moments(a,b,m)
            self.assertEqual(sum(masses),1)
            queries=list(reversed(range(m+2)))+[0,m,m+1]
            expected=[float(sum(masses[r:])) for r in queries]
            self.assertVectorClose(solve(a,b,0,0,m,queries),expected)
            mean=sum(k*p for k,p in enumerate(masses))
            variance=sum((k-mean)**2*p for k,p in enumerate(masses))
            self.assertEqual(mean,F(m*a,a+b))
            self.assertEqual(variance,F(m*a*b*(a+b+m),(a+b)**2*(a+b+1)))
        # Plugging in E[p] discards Var(p); an asymmetric posterior checks
        # parameter convention, not merely a symmetric coin example.
        self.assertVectorClose(solve(2,2,3,1,2,[2,1]),[5/12,5/6])
        self.assertNotAlmostEqual(solve(2,2,3,1,2,[2])[0],(5/8)**2)

    def test_predictive_reference_matches_high_precision_and_boundaries(self):
        solve=reference('c_l09_hard')
        for case in CODES['c_l09_hard']['samples']+CODES['c_l09_hard']['tests']:
            alpha,beta,s,f,m,queries=case['args']
            original=copy.deepcopy(case['args'])
            if alpha+s==beta+f==1:
                expected=[(m-r+1)/(m+1) for r in queries]
            elif not queries:expected=[]
            else:expected=decimal_prediction(alpha+s,beta+f,m,queries)
            self.assertVectorClose(case['expected'],expected)
            self.assertVectorClose(solve(*case['args']),expected)
            self.assertEqual(case['args'],original)
        # A balanced large posterior has an endpoint below double precision.
        with localcontext() as ctx:
            ctx.prec=85
            endpoint=D(1)
            for j in range(3000):endpoint*=D(2000+j)/D(4000+j)
            self.assertLess(endpoint,D('1e-324'))
        self.assertGreater(solve(2000,2000,0,0,3000,[1500])[0],.5)

    def test_predictive_symmetry_update_and_query_order(self):
        solve=reference('c_l09_hard');rng=random.Random(2109)
        for _ in range(150):
            a,b=rng.randint(1,15),rng.randint(1,15)
            s,f=rng.randint(0,10),rng.randint(0,10);m=rng.randint(0,70)
            queries=[rng.randint(0,m+1) for _ in range(20)]
            direct=solve(a,b,s,f,m,queries)
            self.assertVectorClose(direct,solve(a+s,b+f,0,0,m,queries))
            opposite=solve(b,a,f,s,m,[m-r+1 for r in queries])
            self.assertVectorClose(direct,[1-p for p in opposite])
            self.assertTrue(all(-1e-14<=p<=1+1e-14 for p in direct))

    def test_published_references_pass_actual_judge(self):
        for id in ['c_l09_easy','c_l09_hard']:
            result=run(id,CODES[id]['solution'])
            self.assertEqual(result['passed'],result['total'],result)
        wrong='''def solve(alpha,beta,batches):
    return [[(alpha+s)/(alpha+beta+s+f), 0] for s,f in batches]'''
        result=run('c_l09_easy',wrong)
        self.assertLess(result['passed'],result['total'])
        plug_in='''from math import comb, fsum
def solve(alpha,beta,successes,failures,m,thresholds):
    p=(alpha+successes)/(alpha+beta+successes+failures)
    return [fsum(comb(m,k)*p**k*(1-p)**(m-k) for k in range(r,m+1)) for r in thresholds]'''
        result=run('c_l09_hard',plug_in)
        self.assertLess(result['passed'],result['total'])
        # This wrong solver fixes the model but starts from an underflowed
        # float endpoint; the balanced 3000-trial case must reject it.
        endpoint='''from math import fsum
def solve(alpha,beta,successes,failures,m,thresholds):
    a=alpha+successes;b=beta+failures
    w=1.0
    for j in range(m):w*= (b+j)/(a+b+j)
    weights=[w]
    for k in range(m):
        weights.append(weights[-1]*(m-k)*(a+k)/((k+1)*(m-k-1+b)))
    tails=[0.0]*(m+2)
    for k in range(m,-1,-1):tails[k]=tails[k+1]+weights[k]
    return [tails[r] for r in thresholds]'''
        result=run('c_l09_hard',endpoint)
        self.assertLess(result['passed'],result['total'])

    def test_max_queries_and_editable_official_copies(self):
        solve=reference('c_l09_hard')
        queries=list(range(100000))
        self.assertVectorClose(solve(1,1,0,0,100000,queries),
                               [(100001-r)/100001 for r in queries])
        # Every new official case can be copied within the existing editor's
        # combined 200000-character per-case limit; large complexity tests
        # must not create an official case that the learner cannot debug.
        for id in ['c_l09_easy','c_l09_hard']:
            for case in CODES[id]['samples']+CODES[id]['tests']:
                size=len(json.dumps(case['args']))+len(json.dumps(case['expected']))
                self.assertLessEqual(size,200000,id)

    def test_topic_specific_assessment_and_old_medium_identity(self):
        lesson=next(l for l in BANK['lessons'] if l['id']=='l09')
        self.assertEqual(lesson['coding'],['c_l09_easy','c04','c_l09_hard'])
        self.assertTrue(lesson['practiceExpanded'])
        self.assertGreaterEqual(len(QUESTIONS['q_l09_h2']['rubric']),4)
        self.assertNotIn('State the assumptions and the object you are computing.',QUESTIONS['q24']['rubric'])
        self.assertEqual(reference('c04')([1,2,3]),[2,1])


if __name__=='__main__':unittest.main()
