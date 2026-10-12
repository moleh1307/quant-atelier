"""Exact joint tables, independent tail objectives and exhaustive subset decisions."""
import copy
import itertools
import json
import math
import random
import unittest
from collections import Counter
from fractions import Fraction as F

from coding_bank import TASKS
from judge import run,submission_cases,parse_debug_cases
from test_topic_practice import BANK,QUESTIONS,reference

CODES={t['id']:t for t in TASKS}


def fraction_text(value):return [str(value.numerator),str(value.denominator)]


def covariance_oracle(q,b,factor_variances,residual_variances):
    n=len(q)
    matrix=[[sum(b[i][k]*b[j][k]*v for k,v in enumerate(factor_variances))+
             (residual_variances[i] if i==j else 0) for j in range(n)] for i in range(n)]
    total=sum(q[i]*q[j]*matrix[i][j] for i in range(n) for j in range(n))
    residual=sum(v*q[i]**2 for i,v in enumerate(residual_variances))
    return {'exposures':[str(sum(q[i]*b[i][k] for i in range(n))) for k in range(len(factor_variances))],
            'factor_variance':str(total-residual),'residual_variance':str(residual),'variance':str(total)}


def tail_oracle(rows,q,counts,tail):
    """Minimise the hinge-loss variational objective, without sorting tail mass."""
    losses=[-sum(x*y for x,y in zip(row,q)) for row in rows]
    total=sum(counts);alpha=F(*tail)
    candidates=set(l for l,w in zip(losses,counts) if w)
    value=min(F(t)+sum(F(w,total)*max(l-t,0) for l,w in zip(losses,counts))/alpha for t in candidates)
    thresholds=[t for t in candidates
                if sum(F(w,total) for l,w in zip(losses,counts) if l>t)<alpha<=
                sum(F(w,total) for l,w in zip(losses,counts) if l>=t)]
    assert len(thresholds)==1
    return {'threshold':str(thresholds[0]),'tail_mean':fraction_text(value)}


def subset_oracle(gains,loadings,margins,capital,limit):
    choices=[]
    for mask in range(1<<len(gains)):
        indices=[i for i in range(len(gains)) if mask>>i&1]
        cost=sum(margins[i] for i in indices)
        if cost>capital or abs(sum(loadings[i] for i in indices))>limit:continue
        score=sum(gains[i] for i in indices)
        choices.append((-score,cost,len(indices),indices))
    negative_score,cost,_,indices=min(choices)
    return {'gain':-negative_score,'margin':cost,'indices':indices}


def compositions(total,length):
    if length==1:
        yield (total,)
    else:
        for first in range(total+1):
            for rest in compositions(total-first,length-1):yield (first,)+rest


class JointRiskPracticeTests(unittest.TestCase):
    def test_coverage_and_stable_original_meaning(self):
        topic=next(l for l in BANK['lessons'] if l['id']=='l22')
        self.assertEqual(Counter(QUESTIONS[q]['difficulty'] for q in topic['questions']),Counter({'Easy':2,'Medium':2,'Hard':2}))
        self.assertEqual(topic['coding'],['c_l22_easy','c_l22_medium','c_l22_hard'])
        self.assertEqual((QUESTIONS['q38']['answer'],QUESTIONS['q38']['type'],QUESTIONS['q38']['difficulty']),(3,'numeric','Medium'))
        for id in topic['questions']:
            self.assertGreaterEqual(len(QUESTIONS[id]['rubric']),3)
            self.assertTrue(QUESTIONS[id]['followSolution'])

    def test_hedge_stress_units_and_boundary_answers(self):
        self.assertEqual(QUESTIONS['q_l22_e1']['answer'],8)
        changed=(2-F(2,3)*F(5,2))**2*9+4+F(4,9)*9
        self.assertEqual(changed,9)
        self.assertEqual((2-F(5,2))**2*9+4+9,F(61,4))
        baseline=F(1,4)*4*2+F(1,2)*2
        stress=F(1,4)*16+F(1,4)*4+F(1,2)*8
        self.assertEqual((baseline,stress),(3,9))
        self.assertEqual(F(stress,baseline),3)
        self.assertAlmostEqual(QUESTIONS['q_l22_e2']['answer'],math.sqrt(3))
        self.assertEqual((F(1,2)*2-F(1,2)*3)**2,F(1,4))
        self.assertEqual(F(3,5)*2-F(2,5)*3,0)

    def test_factor_floor_and_coherent_residual_stress(self):
        self.assertEqual(QUESTIONS['q_l22_m1']['answer'],40)
        self.assertGreater(1+F(4,39),F(11,10))
        self.assertEqual(1+F(4,40),F(11,10))
        for n in (1,2,7,40,100):
            # Direct weighted covariance sum over all pairs, including shared residual noise.
            total=sum(F(1,n*n)*(5 if i==j else F(6,5)) for i in range(n) for j in range(n))
            self.assertEqual(total,F(6,5)+F(19,5*n))
            self.assertGreater(total,F(6,5))
            self.assertEqual(F(1,5)+F(19,5),4)

    def test_sharp_tail_tables_have_identical_pairwise_information(self):
        cells=list(itertools.product((0,1),repeat=3))
        for q in (F(0),F(1,40),F(1,8),F(1,4)):
            probabilities=[F(1,4)-q if sum(c) in (0,2) else q for c in cells]
            self.assertEqual(sum(probabilities),1)
            self.assertTrue(all(p>=0 for p in probabilities))
            for i in range(3):
                self.assertEqual(sum(p*c[i] for c,p in zip(cells,probabilities)),F(1,2))
                for j in range(i+1,3):
                    for x,y in itertools.product((0,1),repeat=2):
                        self.assertEqual(sum(p for c,p in zip(cells,probabilities) if c[i]==x and c[j]==y),F(1,4))
            mean=sum(p*(1-F(2,3)*sum(c)) for c,p in zip(cells,probabilities))
            variance=sum(p*(1-F(2,3)*sum(c)-mean)**2 for c,p in zip(cells,probabilities))
            crash=sum(p for c,p in zip(cells,probabilities) if 1-F(2,3)*sum(c)<-F(2,3))
            self.assertEqual((mean,variance,crash),(0,F(1,3),q))
        # Enumerate all integer eight-cell tables on a finer finite grid independently.
        attainable=set()
        for counts in compositions(8,8):
            if any(sum(w*c[i] for c,w in zip(cells,counts))!=4 for i in range(3)):continue
            if any(sum(w*c[i]*c[j] for c,w in zip(cells,counts))!=2 for i in range(3) for j in range(i+1,3)):continue
            attainable.add(F(counts[-1],8))
        self.assertEqual(attainable,{F(0),F(1,8),F(1,4)})
        for invalid in (F(-1,100),F(26,100)):
            self.assertTrue(any(p<0 for p in (invalid,F(1,4)-invalid)))

    def test_uncertain_hedge_envelope_one_sided_and_changed_residual(self):
        def variance(h,b,d):return 4*(1-b*h)**2+1+d*h*h
        for d in (0,1,4,12,1000):
            h=min(F(1,2),F(4,4+d))
            worst=max(variance(h,1,d),variance(h,3,d))
            expected=2+F(d,4) if d<=4 else 5-F(16,4+d)
            self.assertEqual(worst,expected)
            for b in (F(1),F(3,2),F(2),F(5,2),F(3)):
                self.assertLessEqual(variance(h,b,d),worst)
            for candidate in (0,F(1,2),2,max(0,h-F(1,10000)),h+F(1,10000)):
                self.assertGreaterEqual(max(variance(candidate,1,d),variance(candidate,3,d)),worst)
        self.assertEqual((-8+10*F(1,2),-24+74*F(1,2)),(-3,13))
        self.assertEqual(max(variance(F(8,17),1,1),variance(F(8,17),3,1)),F(677,289))
        self.assertEqual(max(variance(F(1,2),1,12),variance(F(1,2),3,12)),5)

    def test_easy_against_full_covariance_and_physical_shocks(self):
        solve=reference('c_l22_easy');rng=random.Random(2201)
        for _ in range(250):
            n,k=rng.randint(1,5),rng.randint(0,4)
            args=[[rng.randint(-3,3) for _ in range(n)],[[rng.randint(-3,3) for _ in range(k)] for _ in range(n)],
                  [rng.randint(0,7) for _ in range(k)],[rng.randint(0,7) for _ in range(n)]]
            self.assertEqual(solve(*args),covariance_oracle(*args))
        for _ in range(40):
            n,k=rng.randint(1,3),rng.randint(0,3)
            q=[rng.randint(-3,3) for _ in range(n)];betas=[[rng.randint(-3,3) for _ in range(k)] for _ in range(n)]
            fs=[rng.randint(0,3) for _ in range(k)];rs=[rng.randint(0,3) for _ in range(n)]
            payoffs=[]
            for signs in itertools.product((-1,1),repeat=n+k):
                payoffs.append(sum(q[i]*(sum(betas[i][j]*fs[j]*signs[j] for j in range(k))+rs[i]*signs[k+i]) for i in range(n)))
            mean=F(sum(payoffs),len(payoffs));variance=sum((v-mean)**2 for v in payoffs)/len(payoffs)
            self.assertEqual(int(solve(q,betas,[x*x for x in fs],[x*x for x in rs])['variance']),variance)

    def test_medium_against_independent_hinge_objective_and_mass_allocations(self):
        solve=reference('c_l22_medium');rng=random.Random(2202)
        for _ in range(250):
            n,m=rng.randint(1,3),rng.randint(1,7)
            rows=[[rng.randint(-5,5) for _ in range(n)] for _ in range(m)]
            q=[rng.randint(-3,3) for _ in range(n)]
            counts=[rng.randint(0,4) for _ in range(m)]
            if not sum(counts):counts[0]=1
            b=rng.randint(1,7);tail=[rng.randint(1,b),b]
            self.assertEqual(solve(rows,q,counts,tail),tail_oracle(rows,q,counts,tail))
        for _ in range(60):
            losses=[rng.randint(-5,5) for _ in range(3)];counts=[rng.randint(0,2) for _ in range(3)]
            if not sum(counts):counts[0]=1
            b=rng.randint(1,3);a=rng.randint(1,b);required=sum(counts)*a
            allocations=[allocation for allocation in itertools.product(*(range(w*b+1) for w in counts)) if sum(allocation)==required]
            value=max(F(sum(v*l for v,l in zip(allocation,losses)),required) for allocation in allocations)
            expected=solve([[-l] for l in losses],[1],counts,[a,b])['tail_mean']
            self.assertEqual(expected,fraction_text(value))

    def test_hard_against_all_subsets_and_all_tie_priorities(self):
        solve=reference('c_l22_hard');rng=random.Random(2203)
        for _ in range(500):
            n=rng.randint(0,10)
            args=[[rng.randint(-8,8) for _ in range(n)],[rng.randint(-4,4) for _ in range(n)],
                  [rng.randint(1,5) for _ in range(n)],rng.randint(0,12),rng.randint(0,4)]
            self.assertEqual(solve(*args),subset_oracle(*args))
        # Same gain/margin/count, but lexicographic order does not follow ordinary mask order.
        args=[[3,3,3,3],[1,1,-1,-1],[1,1,1,1],2,0]
        self.assertEqual(solve(*args),{'gain':6,'margin':2,'indices':[0,2]})
        # A single gain-five item cannot be reused to earn ten.
        self.assertEqual(solve([5],[0],[1],2,0),{'gain':5,'margin':1,'indices':[0]})
        loadings=list(range(1,11))*2+list(range(-1,-11,-1))*2
        self.assertEqual(solve([1]*40,loadings,[2]*40,80,0),{'gain':40,'margin':80,'indices':list(range(40))})

    def test_fixture_references_mutation_and_exact_copy_contracts(self):
        oracles={'easy':covariance_oracle,'medium':tail_oracle}
        for suffix in ('easy','medium','hard'):
            task=CODES['c_l22_'+suffix];solve=reference(task['id'])
            for case in task['samples']+task['tests']:
                args=copy.deepcopy(case['args']);saved=copy.deepcopy(args)
                result=solve(*args)
                self.assertEqual(result,case['expected'],task['id'])
                self.assertEqual(args,saved)
                if suffix in oracles:self.assertEqual(oracles[suffix](*args),case['expected'])
                elif len(args[0])<=10:self.assertEqual(subset_oracle(*args),case['expected'])
            if suffix!='hard':
                for copied in submission_cases(task['id'])['cases']:
                    self.assertLessEqual(len(copied['argumentsJSON'])+len(copied['expectedJSON']),500000)
                    parsed=parse_debug_cases(task,[copied])
                    self.assertEqual(solve(*parsed[0]['args']),parsed[0]['expected'])
        easy=CODES['c_l22_easy']['samples'][2]['expected']
        self.assertEqual(easy['factor_variance'],str(10**30))
        self.assertEqual(easy['variance'],str(10**30+10**18))
        medium=CODES['c_l22_medium']['samples'][2]['expected']
        self.assertEqual(medium['tail_mean'],['2000000000000000000','1999999'])

    def test_actual_judge_full_and_public_exact_debugging(self):
        for suffix in ('easy','medium','hard'):
            id='c_l22_'+suffix;task=CODES[id]
            checked=run(id,task['solution']);self.assertNotIn('error',checked,id)
            self.assertEqual(checked['passed'],checked['total'],id)
            if suffix!='hard':
                public=submission_cases(id)['cases'][2]
                checked=run(id,task['solution'],mode='debug',debug_cases=[public])
                self.assertNotIn('error',checked,id)
                self.assertEqual((checked['passed'],checked['total']),(1,1))


if __name__=='__main__':unittest.main()
