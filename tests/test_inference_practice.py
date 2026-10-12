"""Independent inference oracles and probability arguments.

Forward prefix-count references are checked against exhaustive ordered records
and a backward conditional-probability recursion using Fraction. Neither oracle
uses the production common-denominator first-hit accumulation.
Personal progress APIs and persisted user records are never touched.
"""
import copy
import itertools
import json
import math
import random
import unittest
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from statistics import NormalDist


def pair(value):
    return [str(value.numerator),str(value.denominator)]


def decode(value):
    return F(int(value[0]),int(value[1]))


def backward(n, looks, p):
    boundaries=dict(looks)
    @lru_cache(None)
    def visit(t,k):
        if t in boundaries and k>=boundaries[t]:
            return F(1),F(0)
        if t==n:
            return F(0),F(0)
        tail_probability,tail_cost=visit(t+1,k)
        head_probability,head_cost=visit(t+1,k+1)
        return ((1-p)*tail_probability+p*head_probability,
                1+(1-p)*tail_cost+p*head_cost)
    return visit(0,0)


def sequential_oracle(n,looks,a,d):
    size,null_cost=backward(n,looks,F(1,2))
    power,alternative_cost=backward(n,looks,F(a,d))
    return dict(size=pair(size),power=pair(power),null_flips=pair(null_cost),alternative_flips=pair(alternative_cost))


def enumerate_procedure(n,looks,p):
    boundaries=dict(looks);reject_probability=F(0);expected_cost=F(0)
    for record in itertools.product((0,1),repeat=n):
        heads=sum(record);probability=p**heads*(1-p)**(n-heads)
        seen=0;stopped=n;rejected=False
        for t,head in enumerate(record,1):
            seen+=head
            if t in boundaries and seen>=boundaries[t]:
                stopped=t;rejected=True;break
        reject_probability+=probability*rejected
        expected_cost+=probability*stopped
    return reject_probability,expected_cost


def fixed_oracle(n,threshold,a,d):
    # Factorial combinations are independent of the reference's coefficient
    # and integer weight recurrences; small instances are also enumerated.
    def tail(p):
        return sum((F(math.comb(n,k))*p**k*(1-p)**(n-k) for k in range(threshold,n+1)),F(0))
    return dict(size=pair(tail(F(1,2))),power=pair(tail(F(a,d))))


def phi(x):
    return math.erfc(-x/math.sqrt(2))/2


def integral_normal(lower,upper,mean=0,intervals=2400):
    if upper<=lower:return 0.0
    step=(upper-lower)/intervals
    def density(x):return math.exp(-(x-mean)**2/2)/math.sqrt(2*math.pi)
    terms=density(lower)+density(upper)
    terms+=sum((4 if j%2 else 2)*density(lower+j*step) for j in range(1,intervals))
    return step*terms/3


class InferencePracticeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from test_topic_practice import BANK,CODES,QUESTIONS,reference
        cls.bank,cls.codes,cls.questions=BANK,CODES,QUESTIONS
        cls.reference=staticmethod(reference)

    def test_difficulty_contract_and_preserved_specific_rubrics(self):
        lesson=next(l for l in self.bank['lessons'] if l['id']=='l12')
        self.assertEqual(lesson['questions'][:3],['q22','q26','q47'])
        self.assertEqual(Counter(self.questions[id]['difficulty'] for id in lesson['questions']),Counter(Easy=2,Medium=2,Hard=4))
        self.assertEqual(lesson['coding'],['c_l12_easy','c_l12_medium','c_l12_hard'])
        for id in lesson['questions']:
            self.assertGreaterEqual(len(self.questions[id]['rubric']),3)
            self.assertNotIn('State the assumptions and the object you are computing.',self.questions[id]['rubric'])

    def test_exact_tail_randomized_size_and_power(self):
        records=list(itertools.product((0,1),repeat=6))
        self.assertEqual(F(sum(sum(r)>=5 for r in records),64),F(7,64))
        self.assertEqual(self.questions['q_l12_e1']['answer'],float(F(7,64)))
        size=F(0);power=F(0)
        for record in records:
            k=sum(record)
            reject=F(1) if k==6 else F(11,30) if k==5 else F(0)
            size+=F(1,64)*reject
            power+=F(3,4)**k*F(1,4)**(6-k)*reject
        self.assertEqual(size,F(1,20));self.assertEqual(power,F(3159,10240))
        ratios=[F(3,2)**k*F(1,2)**(6-k) for k in range(7)]
        self.assertTrue(all(ratios[i+1]/ratios[i]==3 for i in range(6)))
        self.assertEqual((F(3,4)**6),F(729,4096))

    def test_interval_duality_and_width(self):
        n,sigma,mean=36,6,F(3,2)
        radius=F(2*sigma,math.isqrt(n))
        self.assertEqual([mean-radius,mean+radius],[F(-1,2),F(7,2)])
        self.assertEqual(self.questions['q_l12_e2']['answer'],3.5)
        self.assertEqual(F(4*sigma,math.isqrt(144)),radius)
        self.assertGreater(2*phi(2)-1,.95)

    def test_predictable_martingale_and_bounded_stopping(self):
        # Exhaustive records verify conditional multiplier means and stopped
        # expectations, even for a rule that chooses q from previous flips.
        for n in range(1,10):
            fixed_total=F(0);adaptive_total=F(0);crossing=0
            for record in itertools.product((0,1),repeat=n):
                fixed=F(1);adaptive=F(1);fixed_stopped=None;adaptive_stopped=None
                for t,head in enumerate(record,1):
                    q=F(1,4) if t>1 and record[t-2] else F(3,4)
                    adaptive*=2*q if head else 2*(1-q)
                    fixed*=F(3,2) if head else F(1,2)
                    if fixed_stopped is None and fixed>=3:fixed_stopped=fixed
                    if adaptive_stopped is None and adaptive>=3:adaptive_stopped=adaptive
                fixed_total+=fixed_stopped if fixed_stopped is not None else fixed
                adaptive_total+=adaptive_stopped if adaptive_stopped is not None else adaptive
                crossing+=fixed_stopped is not None
            self.assertEqual(fixed_total/2**n,1)
            self.assertEqual(adaptive_total/2**n,1)
            self.assertLessEqual(F(crossing,2**n),F(1,3))
        for conditional_p in (F(0),F(1,5),F(1,2)):
            self.assertLessEqual(conditional_p*F(3,2)+(1-conditional_p)*F(1,2),1)
        # Current-flip adaptation yields the deterministic multiplier two,
        # rejecting at time five under every fair-coin record.
        for record in itertools.product((0,1),repeat=5):
            process=1
            for head in record:
                q=head;process*=2*q if head else 2*(1-q)
            self.assertEqual(process,32)

    def test_selected_interval_coverage_by_independent_quadrature(self):
        c=NormalDist().inv_cdf(.975)
        for mu in (-2,0,.1,c,2*c,5,8):
            denominator=math.erfc((c-mu)/math.sqrt(2))/2
            if mu<=0:expression=0.0
            elif mu<2*c:expression=(phi(c)-phi(c-mu))/denominator
            else:expression=.95/denominator
            # Integrate the density in the original X coordinate over the
            # intersection, rather than reproduce the CDF branch calculation.
            probability=integral_normal(max(c,mu-c),mu+c,mean=mu)/denominator
            self.assertAlmostEqual(probability,expression,places=10)
        self.assertAlmostEqual(.95/(1-phi(-c)),38/39,places=12)
        self.assertAlmostEqual((phi(c)-phi(0))/(1-phi(0)),.95,places=12)

    def test_conditional_pivot_inversion_and_replication(self):
        c=NormalDist().inv_cdf(.975)
        for mu in (-1,0,1,4):
            survival=1-phi(c-mu)
            endpoints=[]
            for quantile in (.025,.975):
                lo,hi=c,c+20+abs(mu)
                for _ in range(80):
                    x=(lo+hi)/2
                    conditional=(phi(x-mu)-phi(c-mu))/survival
                    if conditional<quantile:lo=x
                    else:hi=x
                endpoints.append((lo+hi)/2)
            conditional_probability=integral_normal(endpoints[0],endpoints[1],mean=mu)/survival
            self.assertAlmostEqual(conditional_probability,.95,places=9)
            # Independent replication gives product probabilities, so selection
            # probability cancels without using the selected X twice.
            self.assertAlmostEqual(survival*(phi(c)-phi(-c))/survival,.95,places=12)

    def test_easy_inversion_against_rational_statistic(self):
        solve=self.reference('c_l12_easy');rng=random.Random(12101)
        for _ in range(250):
            total,n,variance,critical=rng.randrange(-200,201),rng.randrange(1,30),rng.randrange(1,100),rng.randrange(10)
            candidates=[rng.randrange(-20,21) for _ in range(rng.randrange(15))]
            expected=[(F(total,n)-m)**2/F(variance,n)<=critical for m in candidates]
            before=candidates.copy()
            self.assertEqual(solve(total,n,variance,critical,candidates),expected)
            self.assertEqual(candidates,before)
        self.assertEqual(solve(999999999,1,999999998000000000,1,[0]),[False])
        self.assertEqual(solve(0,1,1,1,[1,-1,2]*33333+[0]),[True,True,False]*33333+[True])

    def test_fixed_tails_by_enumeration_and_factorial_formula(self):
        solve=self.reference('c_l12_medium')
        for n in range(8):
            for threshold in range(n+2):
                for a,d in ((0,1),(1,1),(1,2),(1,3),(3,4)):
                    expected=fixed_oracle(n,threshold,a,d)
                    for p,key in ((F(1,2),'size'),(F(a,d),'power')):
                        probability,_=enumerate_procedure(n,[[n,threshold]] if n else [],p)
                        if n==0:probability=F(threshold==0)
                        self.assertEqual(decode(expected[key]),probability)
                    self.assertEqual(solve(n,threshold,a,d),expected)
        for case in self.codes['c_l12_medium']['samples']+self.codes['c_l12_medium']['tests']:
            self.assertEqual(case['expected'],fixed_oracle(*case['args']))
            self.assertEqual(solve(*case['args']),case['expected'])

    def test_sequential_oracle_against_ordered_records(self):
        rng=random.Random(12102);solve=self.reference('c_l12_hard')
        for trial in range(120):
            n=rng.randrange(10);looks=[[t,rng.randrange(t+2)] for t in range(1,n+1) if rng.randrange(3)]
            d=rng.randrange(1,8);a=rng.randrange(d+1)
            oracle=sequential_oracle(n,looks,a,d)
            for p,probability,cost in ((F(1,2),'size','null_flips'),(F(a,d),'power','alternative_flips')):
                enumerated,flips=enumerate_procedure(n,looks,p)
                self.assertEqual(enumerated,decode(oracle[probability]),trial)
                self.assertEqual(flips,decode(oracle[cost]),trial)
            before=copy.deepcopy(looks)
            self.assertEqual(solve(n,looks,a,d),oracle,trial)
            self.assertEqual(looks,before)
        # The independence shortcut overstates this dependent union:
        # first flip head or cumulative two heads at time two is just first head.
        result=solve(2,[[1,1],[2,2]],1,2)
        self.assertEqual(decode(result['size']),F(1,2))
        self.assertNotEqual(decode(result['size']),1-(1-F(1,2))*(1-F(1,4)))

    def test_all_authored_sequential_cases_and_maximum_bound(self):
        solve=self.reference('c_l12_hard')
        for case in self.codes['c_l12_hard']['samples']+self.codes['c_l12_hard']['tests']:
            expected=sequential_oracle(*case['args'])
            self.assertEqual(case['expected'],expected)
            self.assertEqual(solve(*case['args']),expected)
            self.assertLessEqual(len(json.dumps(case['args']))+len(json.dumps(expected)),200000)
        n=120;looks=[[t,(2*t)//3+1] for t in range(1,n+1)]
        self.assertEqual(solve(n,looks,999,1000),sequential_oracle(n,looks,999,1000))

    def test_procedure_invariants_and_lossless_case_copy(self):
        from judge import run
        solve=self.reference('c_l12_hard');fixed=self.reference('c_l12_medium')
        rng=random.Random(12103)
        for _ in range(60):
            n=rng.randrange(1,16);h=rng.randrange(n+2);a=rng.randrange(8)
            result=solve(n,[[n,h]],a,7)
            ordinary=fixed(n,h,a,7)
            self.assertEqual({key:result[key] for key in ('size','power')},ordinary)
            self.assertEqual(decode(result['null_flips']),n);self.assertEqual(decode(result['alternative_flips']),n)
            looks=[[t,rng.randrange(t+2)] for t in range(1,n+1) if rng.randrange(2)]
            base=solve(n,looks,a,7)
            self.assertEqual(base,solve(n,looks,2*a,14))
            extended=looks+[[n,n+1]] if not looks or looks[-1][0]<n else looks
            self.assertEqual(base,solve(n,extended,a,7))
            smaller=solve(n,looks[:-1],a,7)
            self.assertGreaterEqual(decode(base['size']),decode(smaller['size']))
            self.assertLessEqual(decode(base['null_flips']),decode(smaller['null_flips']))
        result=run('c_l12_hard',self.codes['c_l12_hard']['solution'])
        self.assertNotIn('error',result)
        self.assertEqual(result['passed'],result['total'])
        for i,entry in enumerate(result['results']):
            case=(self.codes['c_l12_hard']['samples']+self.codes['c_l12_hard']['tests'])[i]
            self.assertEqual(json.loads(entry['argumentsJSON']),case['args'])
            self.assertEqual(json.loads(entry['expectedJSON']),case['expected'])
        big=next(case for case in self.codes['c_l12_hard']['tests']
                 if any(int(v[1])>2**53 for v in case['expected'].values()))
        self.assertEqual(json.loads(json.dumps(big['expected'])),big['expected'])
        for value in big['expected'].values():
            self.assertEqual(pair(decode(value)),value)

    def test_actual_judge_and_procedure_shortcuts(self):
        from judge import run
        for id in ('c_l12_easy','c_l12_medium','c_l12_hard'):
            for case in self.codes[id]['samples']+self.codes[id]['tests']:
                self.assertLessEqual(len(json.dumps(case['args']))+len(json.dumps(case['expected'])),200000,id)
            result=run(id,self.codes[id]['solution'])
            self.assertNotIn('error',result,id)
            self.assertEqual(result['passed'],result['total'],id)
        wrong='def solve(horizon,looks,head_numerator,head_denominator):\n    return {"size":["0","1"],"power":["0","1"],"null_flips":[str(horizon),"1"],"alternative_flips":[str(horizon),"1"]}'
        result=run('c_l12_hard',wrong)
        self.assertLess(result['passed'],result['total'])
        wrong='def solve(sample_sum,n,sigma_squared,critical_squared,means):\n    return [(sample_sum/n-m)**2/(sigma_squared/n)<=critical_squared for m in means]'
        result=run('c_l12_easy',wrong)
        self.assertLess(result['passed'],result['total'])


if __name__=='__main__':
    unittest.main()
