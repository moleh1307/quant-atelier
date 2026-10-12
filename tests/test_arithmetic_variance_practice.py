"""Independent integer oracles, joint records and additive-state moments.

The optimized fraction code jumps along Stern–Brocot neighbours; its small-case
oracle instead scans denominators. The pattern reference uses pair covariances;
these tests enumerate paths or propagate count moments in suffix states.
"""
import itertools
import math
import random
import unittest
from fractions import Fraction as F

from coding_bank import TASKS
from judge import run
from test_topic_practice import QUESTIONS, reference


def simplest_fraction_by_denominator(report):
    digits = report.split('.')[1]
    value, scale = int(digits),10**len(digits)
    low, high, denominator = 2*value-1,2*value+1,2*scale
    # The displayed m/scale is itself eligible, bounding the search. This slow
    # oracle is used only for one-, two- and three-decimal reports.
    for b in range(1,scale+1):
        a = (low*b + denominator-1)//denominator
        if a*denominator < high*b:
            return [a,b]
    raise AssertionError('The displayed fraction must be in its rounding bin.')


def pattern_moments_from_states(n,pattern,heads,total):
    k=len(pattern)
    transition=[]
    for state in range(k):
        edges=[]
        for symbol,probability in [('H',F(heads,total)),('T',F(total-heads,total))]:
            history=pattern[:state]+symbol
            reward=int(history.endswith(pattern))
            target=max(j for j in range(k) if history.endswith(pattern[:j]))
            edges.append((target,reward,probability))
        transition.append(edges)
    masses=[[F(0),F(0),F(0)] for _ in range(k)]
    masses[0][0]=1
    for _ in range(n):
        next_masses=[[F(0),F(0),F(0)] for _ in range(k)]
        for state,(probability,first,second) in enumerate(masses):
            for target,reward,weight in transition[state]:
                next_masses[target][0] += probability*weight
                next_masses[target][1] += (first+reward*probability)*weight
                next_masses[target][2] += (second+2*reward*first+reward*probability)*weight
        masses=next_masses
    mean=sum(first for _,first,_ in masses)
    second=sum(second for _,_,second in masses)
    return mean,second-mean**2


class ArithmeticVariancePracticeTests(unittest.TestCase):
    def test_arithmetic_interview_answers_and_rounding_counterexamples(self):
        self.assertEqual(QUESTIONS['q_l06_e1']['answer'],98*107)
        self.assertEqual(F(36,10)/F(45,1000),80)
        self.assertEqual(QUESTIONS['q_l06_e2']['answer'],80)
        recovery=1/F(7,10)-1
        self.assertEqual(recovery,F(3,7))
        self.assertEqual(QUESTIONS['q_l06_m1']['answer'],float(recovery))
        initial=40*125+60*80
        changed=40*125*F(11,10)+60*80*F(9,10)
        self.assertEqual((changed-initial)/initial,F(1,490))
        self.assertEqual(QUESTIONS['q_l06_m2']['answer'],1/490)
        for bound,expected in [(15,{F(2,7)}),(20,{F(2,7),F(5,17)})]:
            compatible={F(a,b) for b in range(1,bound+1) for a in range(1,b)
                        if F(57,200)<=F(a,b)<F(59,200)}
            self.assertEqual(compatible,expected)
        self.assertEqual(QUESTIONS['q_l06_h1']['answer'],2/7)
        values=[F(496,1000),F(254,1000),F(514,1000),F(256,1000)]
        # Exact positive half-up rounding, distinct from the interval search.
        def report_value(x,digits):
            scaled=x*10**digits+F(1,2)
            return scaled.numerator//scaled.denominator
        self.assertEqual([report_value(x,2) for x in values],[50,25,51,26])
        self.assertLess(values[0]/values[1],values[2]/values[3])
        self.assertGreater(F(333,167),F(1021,519))
        # Check all tight-bound limits via rational approaches from inside.
        for denominator in [10**4,10**6,10**8]:
            epsilon=F(1,denominator)
            self.assertGreater(F(495,1000)/(F(255,1000)-epsilon),F(33,17))
            self.assertLess((F(505,1000)-epsilon)/F(245,1000),F(101,49))

    def test_finite_decimals_by_divisibility_not_prime_factorization(self):
        solve=reference('c_l06_easy')
        for n in range(-25,26):
            for d in range(1,61):
                expected=next((places for places in range(41) if (n*10**places)%d==0),None)
                self.assertEqual(solve(n,d),expected,(n,d))
        self.assertEqual(solve(1,2**39),39)

    def test_compound_changes_by_exact_fraction_products(self):
        solve=reference('c_l06_medium')
        rng=random.Random(607)
        examples=[[],[-10000,10000],[10000,-5000],[9999]*100]
        examples += [[rng.randint(-10000,10000) for _ in range(rng.randint(1,20))]
                     for _ in range(100)]
        for changes in examples:
            multiplier=F(1)
            for basis_points in changes: multiplier *= F(10000+basis_points,10000)
            expected=multiplier-1
            original=changes.copy()
            self.assertEqual(solve(changes),[expected.numerator,expected.denominator])
            self.assertEqual(changes,original)

    def test_simplest_fraction_against_every_small_decimal_report(self):
        solve=reference('c_l06_hard')
        for digits in range(1,4):
            for value in range(1,10**digits):
                report='0.'+str(value).zfill(digits)
                self.assertEqual(solve(report),simplest_fraction_by_denominator(report),report)
        scale=10**100
        self.assertEqual(solve('0.'+'0'*99+'1'),[1,2*scale//3+1])
        self.assertEqual(solve('0.'+'9'*100),[2*scale//3,2*scale//3+1])
        # Upper endpoint excluded versus lower endpoint included.
        self.assertEqual(solve('0.12'),[2,17])
        self.assertEqual(solve('0.13'),[1,8])

    def test_variance_interview_and_joint_reference_with_exact_moments(self):
        self.assertEqual(QUESTIONS['q_l07_e1']['answer'],0)
        values=[F(0),F(0),F(2)]
        mean=sum(values)/3
        variance=sum(value**2 for value in values)/3-mean**2
        self.assertEqual(variance,F(8,9))
        self.assertEqual(QUESTIONS['q_l07_m1']['answer'],8/9)
        solve=reference('c_l07_easy')
        rng=random.Random(706)
        for _ in range(100):
            points=[[rng.randint(-5,5),rng.randint(-5,5),F(1,8)] for _ in range(8)]
            a,b=rng.randint(-4,4),rng.randint(-4,4)
            mean=sum((a*x+b*y)*p for x,y,p in points)
            variance=sum((a*x+b*y)**2*p for x,y,p in points)-mean**2
            actual=solve([[x,y,float(p)] for x,y,p in points],a,b)
            self.assertEqual(actual,[float(mean),float(variance)])

    def test_equicorrelation_boundary_by_enumerated_centered_noise(self):
        n=5
        rows=[]
        for z in itertools.product((-1,1),repeat=n):
            mean=F(sum(z),n)
            rows.append([F(value)-mean for value in z])
        for i in range(n):
            self.assertEqual(sum(row[i] for row in rows),0)
            variance=sum(row[i]**2 for row in rows)/len(rows)
            self.assertEqual(variance,F(4,5))
            for j in range(i+1,n):
                covariance=sum(row[i]*row[j] for row in rows)/len(rows)
                self.assertEqual(covariance,F(-1,5))
                self.assertEqual(covariance/variance,F(-1,4))
        self.assertTrue(all(sum(row)==0 for row in rows))
        self.assertLess(5+20*F(-3,10),0)
        self.assertLess(6+30*F(-1,4),0)

    def test_pattern_variance_against_flip_enumeration(self):
        solve=reference('c_l07_hard')
        for length in range(1,5):
            for symbols in itertools.product('HT',repeat=length):
                pattern=''.join(symbols)
                for n in range(0,9):
                    for heads,total in [(1,2),(1,4),(3,4)]:
                        first=second=F(0)
                        for flips in itertools.product('HT',repeat=n):
                            sequence=''.join(flips)
                            successes=sequence.count('H')
                            mass=F(heads,total)**successes*F(total-heads,total)**(n-successes)
                            count=sum(sequence[i:i+length]==pattern for i in range(n-length+1))
                            first += count*mass
                            second += count*count*mass
                        expected=[float(first),float(second-first**2)]
                        actual=solve(n,pattern,heads,total)
                        for a,e in zip(actual,expected):
                            self.assertTrue(math.isclose(a,e,rel_tol=2e-15,abs_tol=1e-14),
                                            (n,pattern,heads,total,actual,expected))

    def test_pattern_interview_and_long_cases_by_additive_state_moments(self):
        solve=reference('c_l07_hard')
        self.assertEqual(pattern_moments_from_states(20,'HTH',1,2),(F(9,4),F(31,16)))
        self.assertEqual(pattern_moments_from_states(20,'HHT',1,2),(F(9,4),F(15,16)))
        self.assertEqual(QUESTIONS['q_l07_h1']['answer'],31/16)
        rng=random.Random(6707)
        for _ in range(50):
            n=rng.randint(1,45)
            pattern=''.join(rng.choice('HT') for _ in range(rng.randint(1,8)))
            heads,total=rng.choice([(1,10),(3,10),(4,7),(9,10)])
            expected=pattern_moments_from_states(n,pattern,heads,total)
            actual=solve(n,pattern,heads,total)
            for a,e in zip(actual,expected):
                self.assertTrue(math.isclose(a,float(e),rel_tol=5e-15,abs_tol=1e-12),
                                (n,pattern,heads,total,actual,expected))
        expected=pattern_moments_from_states(102,'H'*100,1,2)
        self.assertEqual(expected,(F(3,2**100),F(11*2**99-9,2**200)))
        self.assertEqual(solve(102,'H'*100,1,2),[float(e) for e in expected])

    def test_official_cases_with_separate_oracles(self):
        for task in TASKS:
            if not task['id'].startswith(('c_l06_','c_l07_')):continue
            for case in task['samples']+task['tests']:
                args=case['args']
                if task['id']=='c_l06_easy':
                    n,d=args
                    expected=next((i for i in range(41) if n*10**i%d==0),None)
                elif task['id']=='c_l06_medium':
                    multiplier=F(1)
                    for b in args[0]:multiplier *= F(10000+b,10000)
                    result=multiplier-1
                    expected=[result.numerator,result.denominator]
                elif task['id']=='c_l06_hard':
                    if len(args[0])>5:continue  # small enumeration, explicit extreme checks above
                    expected=simplest_fraction_by_denominator(args[0])
                elif task['id']=='c_l07_easy':
                    joint,a,b=args
                    mean=sum(F(p)*(a*x+b*y) for x,y,p in joint)
                    variance=sum(F(p)*(a*x+b*y)**2 for x,y,p in joint)-mean**2
                    expected=[float(mean),float(variance)]
                else:
                    n,pattern,heads,total=args
                    if n==10**12:
                        expected=[(n-1)/4,(n+1)/16] if pattern=='HT' else [(n-2)/8,(15*n-40)/64]
                    else:expected=[float(x) for x in pattern_moments_from_states(n,pattern,heads,total)]
                self.assertEqual(case['expected'],expected,(task['id'],args))

    def test_actual_judge_rejects_unjustified_shortcuts(self):
        shortcuts={
            'c_l06_hard': '''from math import gcd
def solve(report):
    digits=report.split('.')[1]
    n,d=int(digits),10**len(digits)
    common=gcd(n,d)
    return [n//common,d//common]''',
            'c_l06_medium': 'def solve(changes):\n    return [sum(changes),10000]',
            'c_l07_easy': 'def solve(joint,a,b):\n    mx=sum(x*p for x,y,p in joint); my=sum(y*p for x,y,p in joint)\n    return [a*mx+b*my,a*a*sum((x-mx)**2*p for x,y,p in joint)+b*b*sum((y-my)**2*p for x,y,p in joint)]',
            'c_l07_hard': 'def solve(n,pattern,heads,total):\n    q=(heads/total)**pattern.count("H")*(1-heads/total)**pattern.count("T")\n    m=max(0,n-len(pattern)+1)\n    return [m*q,m*q*(1-q)]',
        }
        for id,code in shortcuts.items():
            result=run(id,code)
            self.assertNotIn('error',result,id)
            self.assertLess(result['passed'],result['total'],id)


if __name__=='__main__':
    unittest.main()
