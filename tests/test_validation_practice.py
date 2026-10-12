"""Independent membership and finite information-history checks for validation.

No user state or live server progress endpoints are read or written.
"""
import copy
import itertools
import json
import random
import unittest
from collections import Counter
from fractions import Fraction as F

from coding_bank import TASKS
from judge import run, submission_cases, parse_debug_cases
from topic_practice import LEGACY_CODING_LINKS
from test_topic_practice import BANK, QUESTIONS, reference


def direct_count(rows,queries):
    # Direct intersection membership: no sweep, Fenwick tree or complement formula.
    return [sum(f<=a and r<=t and a>=lower and not(a<v and b>u)
                for a,b,f,r in rows) for t,lower,u,v in queries]


class ValidationPracticeTests(unittest.TestCase):
    def test_contract_and_permanent_additional_practice(self):
        l=next(x for x in BANK['lessons'] if x['id']=='l14')
        self.assertEqual(Counter(QUESTIONS[x]['difficulty'] for x in l['questions']),Counter(Easy=2,Medium=2,Hard=2))
        self.assertEqual(l['questions'][:2],['q27','q28'])
        self.assertEqual(l['coding'],['c_l14_easy','c09','c_l14_hard'])
        self.assertEqual(l['legacyCoding'],['c10'])
        self.assertEqual(LEGACY_CODING_LINKS['l14'],['c10'])
        self.assertEqual(reference('c10')(8,3,2,1),[[[0,1,2],[4,5]],[[0,1,2,3,4],[6,7]]])
        for qid in l['questions']:
            self.assertGreaterEqual(len(QUESTIONS[qid]['hints']),2)
            self.assertGreaterEqual(len(QUESTIONS[qid]['rubric']),3)
            self.assertNotIn('State the assumptions and the object you are computing.',QUESTIONS[qid]['rubric'])

    def test_availability_examples_and_loss_estimands(self):
        rows=[[0,0,3],[2,3,5],[4,4,9],[7,7,10],[8,8,12],[9,11,10]]
        valid=[i for i,(a,f,r) in enumerate(rows) if a<10 and f<=a and r<=10]
        self.assertEqual(valid,[0,2,3]);self.assertEqual(QUESTIONS['q_l14_e1']['answer'],3)
        self.assertEqual([i for i in valid if rows[i][2]<10],[0,2])
        losses=[1,1]+[4]*8
        self.assertEqual(F(sum(losses),len(losses)),F(17,5))
        self.assertAlmostEqual(QUESTIONS['q_l14_e2']['answer'],17/5)
        self.assertEqual((F(1)+F(4))/2,F(5,2))

    def test_half_open_purge_and_publication_delay(self):
        triples=[[2,6,6],[6,10,10],[9,12,12],[14,17,17],[8,10,13]]
        retained=[i for i,(a,b,r) in enumerate(triples) if not(a<14 and b>10)]
        self.assertEqual(retained,[0,1,3,4])
        self.assertEqual([i for i in retained if triples[i][0]<10 and triples[i][2]<=10],[0,1])
        # Exhaust actual interval membership on a half-unit grid independently.
        intervals=list(itertools.combinations(range(6),2))
        for u,v in intervals:
            kept=[]
            protected={F(x,2) for x in range(2*u,2*v)}
            for i,(a,b) in enumerate(intervals):
                support={F(x,2) for x in range(2*a,2*b)}
                if not support & protected: kept.append(i)
            self.assertEqual(reference('c09')(intervals,[u,v]),kept)
        for a,b in intervals:
            for receipt in range(b,8):
                for cutoff in range(receipt,8):
                    self.assertFalse(a<cutoff+2 and b>cutoff)

    def test_predictable_fair_bit_loss_calibration(self):
        for n in range(1,9):
            for rule in ('last','parity','majority'):
                errors=[]
                for outcomes in itertools.product((0,1),repeat=n):
                    loss=0
                    for t,y in enumerate(outcomes):
                        history=outcomes[:t]
                        a=(history[-1] if history else 0) if rule=='last' else (sum(history)%2 if rule=='parity' else int(sum(history)>t/2))
                        loss+=a!=y
                    errors.append(F(loss,n)-F(1,2))
                self.assertEqual(sum(errors)/len(errors),0)
                self.assertEqual(sum(x*x for x in errors)/len(errors),F(1,4*n))
        self.assertEqual(F(1,4)/F(1,20),5) # Chebyshev radius squared = 5/n.

    def test_dependent_outcomes_and_random_risk_target(self):
        for n in range(1,8):
            mean=second=mass=F(0);risk_averages=set()
            for ys in itertools.product((0,1),repeat=n):
                probability=F(1);centered=F(0);previous=0;risk_sum=F(0)
                for y in ys:
                    p=F(1+previous,3)
                    a=0
                    risk=p if a==0 else 1-p
                    centered+=int(a!=y)-risk
                    risk_sum+=risk
                    probability*=p if y else 1-p
                    previous=y
                risk_averages.add(risk_sum/n)
                mean+=probability*centered/n
                second+=probability*(centered/n)**2
                mass+=probability
            self.assertEqual(mass,1);self.assertEqual(mean,0)
            self.assertEqual(second,F(2,9*n))
            if n>1:self.assertGreater(len(risk_averages),1)
        # Dependent risks vary across paths; the target is not one frozen model.
        self.assertNotEqual(F(1,3),F(2,3))

    def test_retrospective_selection_counterexample(self):
        pairs=list(itertools.product((0,1),repeat=2))
        report=sum(F(min(sum(y),2-sum(y)),2) for y in pairs)/4
        self.assertEqual(report,F(1,4))
        future=F(0)
        for ys in pairs:
            a=int(sum(ys)>1)
            future+=sum(int(a!=y) for y in (0,1))/8
        self.assertEqual(future,F(1,2))

    def test_easy_against_membership_and_input_preservation(self):
        solve=reference('c_l14_easy')
        triples=[(a,f,r) for a in range(3) for f in range(4) for r in range(a+1,5)]
        for rows in itertools.product(triples,repeat=2):
            for cutoff in range(6):
                expected=[i for i,row in enumerate(rows) if row[0]<cutoff and row[1]<=row[0] and row[2]<=cutoff]
                data=list(map(list,rows));original=copy.deepcopy(data)
                self.assertEqual(solve(data,cutoff),expected)
                self.assertEqual(data,original)
        rows=[[i,i,i+1] for i in range(100000)]
        self.assertEqual(solve(rows,100000),list(range(100000)))

    def test_hard_against_independent_membership(self):
        solve=reference('c_l14_hard');rng=random.Random(141414)
        for _ in range(240):
            rows=[]
            for __ in range(rng.randrange(35)):
                a=rng.randrange(15);b=a+rng.randrange(1,8)
                rows.append([a,b,rng.randrange(23),b+rng.randrange(6)])
            queries=[]
            for __ in range(rng.randrange(35)):
                t=rng.randrange(30);u=rng.randrange(23)
                queries.append([t,rng.randrange(t+1),u,u+rng.randrange(1,8)])
            original=copy.deepcopy((rows,queries))
            self.assertEqual(solve(rows,queries),direct_count(rows,queries))
            self.assertEqual((rows,queries),original)
        for task in TASKS:
            if task['id']!='c_l14_hard':continue
            for case in task['samples']+task['tests']:
                self.assertEqual(case['expected'],direct_count(*case['args']))

    def test_query_order_duplicates_and_future_invariance(self):
        solve=reference('c_l14_hard')
        rows=[[0,3,0,3],[2,7,2,8],[5,9,6,9],[7,10,7,12]]
        queries=[[12,0,3,7],[8,2,7,9],[8,0,8,10],[12,5,0,7]]
        expected=direct_count(rows,queries)
        self.assertEqual(solve(rows[::-1],queries),expected)
        self.assertEqual(solve(rows,queries[::-1]),expected[::-1])
        self.assertEqual(solve(rows*2,queries),[2*x for x in expected])
        self.assertEqual(solve(rows,queries*2),expected*2)
        self.assertEqual(solve(rows+[[1,100,1,100],[100,101,100,101]],queries),expected)
        for t,lower,u,v in queries:
            before=[r for r in rows if r[3]<=t]
            self.assertEqual(solve(rows,[[t,lower,u,v]]),solve(before,[[t,lower,u,v]]))

    def test_maximum_bounds_and_empty_queries(self):
        solve=reference('c_l14_hard')
        rows=[[i,i+1,i,i+2] for i in range(20000)]
        qs=[[i+2,0,100000,100001] for i in range(20000)]
        self.assertEqual(solve(rows,qs),list(range(1,20001)))
        self.assertEqual(solve(rows,[]),[])
        self.assertEqual(solve([],qs),[0]*len(qs))
        self.assertEqual(solve([[10**12-1,10**12,0,10**12]],[[10**12,0,0,10**12-1]]),[1])

    def test_official_fixture_contracts_and_exact_debug_copies(self):
        for task in TASKS:
            if task['id'] not in ('c_l14_easy','c09','c_l14_hard'):continue
            if task['id']=='c_l14_hard':
                for case in task['samples']+task['tests']:
                    rows,qs=case['args'];self.assertLessEqual(len(rows),20000);self.assertLessEqual(len(qs),20000)
                    for a,b,f,r in rows:self.assertTrue(0<=a<b<=r<=10**12 and 0<=f<=10**12)
                    for t,l,u,v in qs:self.assertTrue(0<=l<=t<=10**12 and 0<=u<v<=10**12)
            if task['id']=='c_l14_easy':
                for case in task['samples']+task['tests']:
                    rows,t=case['args'];self.assertTrue(0<=t<=10**12);self.assertLessEqual(len(rows),100000)
                    for a,f,r in rows:self.assertTrue(0<=a<r<=10**12 and 0<=f<=10**12)
            copies=submission_cases(task['id'])['cases']
            for c,original in zip(copies,task['samples']+task['tests']):
                self.assertLessEqual(len(c['argumentsJSON'])+len(c['expectedJSON']),200000)
                self.assertEqual(parse_debug_cases(task,[c])[0],original)

    def test_actual_judge_and_wrong_shortcut(self):
        for id in ('c_l14_easy','c09','c_l14_hard'):
            task=next(t for t in TASKS if t['id']==id)
            result=run(id,task['solution'])
            self.assertNotIn('error',result,id);self.assertEqual(result['passed'],result['total'],id)
        wrong=run('c_l14_hard','def solve(rows, queries):\n    return [sum(r<=t for a,b,f,r in rows) for t,l,u,v in queries]')
        self.assertNotIn('error',wrong);self.assertLess(wrong['passed'],wrong['total'])


if __name__=='__main__':unittest.main()
