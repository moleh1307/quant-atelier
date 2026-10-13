"""Independent paired-record, finite-joint-law and population identity checks."""
import copy
import json
import math
import random
import unittest
from collections import Counter
from fractions import Fraction as F
from unittest.mock import patch

from coding_bank import TASKS
from judge import run, submission_cases, parse_debug_cases
from test_topic_practice import BANK, QUESTIONS, reference
from topic_practice import COMPLETE_TOPICS, attach_and_validate

CODES = {t['id']: t for t in TASKS}


def text(value):
    return f'{value.numerator}/{value.denominator}'


def score_oracle(probabilities, outcomes, weights, scale):
    total = sum(weights)
    records = [(F(p, scale), y, F(w, total))
               for p, y, w in zip(probabilities, outcomes, weights) if w]
    rate = sum(y*w for p,y,w in records)
    reliability = resolution = F(0)
    for p in {p for p,y,w in records}:
        group = [(y,w) for f,y,w in records if f == p]
        mass = sum(w for y,w in group)
        group_rate = sum(y*w for y,w in group)/mass
        reliability += mass*(p-group_rate)**2
        resolution += mass*(group_rate-rate)**2
    return {k:text(v) for k,v in (
        ('score',sum(w*(p-y)**2 for p,y,w in records)),
        ('reliability',reliability), ('resolution',resolution),
        ('uncertainty',rate*(1-rate)))}


def bid_oracle(states, cap):
    total = sum(w for v,h,w in states)
    # Every permitted integer action, not just the reference's breakpoints.
    gains = [sum(F(w,total)*(v-b) for v,h,w in states if b > h)
             for b in range(cap+1)]
    b = max(range(cap+1), key=lambda b:gains[b])
    mass = sum(w for v,h,w in states if b > h)
    value = sum(v*w for v,h,w in states if b > h)
    return {'bid':b, 'gain':text(F(gains[b])),
            'win_probability':text(F(mass,total)),
            'win_value':text(F(value,mass)) if mass else None}


class CalibrationPracticeTests(unittest.TestCase):
    def test_coverage_original_grading_and_shared_bookmark(self):
        lesson = next(l for l in BANK['lessons'] if l['id']=='l24')
        self.assertEqual(Counter(QUESTIONS[id]['difficulty'] for id in lesson['questions']),
                         {'Easy':2,'Medium':2,'Hard':3})
        self.assertEqual(lesson['coding'],['c14','c_l24_medium','c_l24_hard'])
        self.assertEqual(QUESTIONS['q41']['type'],'structured')
        self.assertIsNone(QUESTIONS['q41']['answer'])
        self.assertEqual(CODES['c14']['difficulty'],'Easy')
        legacy = next(l for l in BANK['lessons'] if l['id']=='l18')['legacyCoding']
        self.assertIn('c14',legacy)
        for id in lesson['questions']:
            self.assertGreaterEqual(len(QUESTIONS[id]['rubric']),3)

    def test_future_registration_does_not_bypass_coverage(self):
        future = {'id':'l31','questions':[],'coding':[]}
        with patch('topic_practice.COMPLETE_TOPICS',COMPLETE_TOPICS+('l31',)):
            with self.assertRaisesRegex(ValueError,'l31 needs at least two'):
                attach_and_validate(copy.deepcopy(BANK['lessons'])+[future],BANK['questions'],TASKS)
            future_questions = [dict(QUESTIONS['q_l24_e1'],id=f'q_future_{i}',
                                     lesson='l31',difficulty=level)
                                for i,level in enumerate(('Easy','Easy','Medium','Medium','Hard','Hard'))]
            with self.assertRaisesRegex(ValueError,'l31 needs exactly one coding'):
                attach_and_validate(copy.deepcopy(BANK['lessons'])+[copy.deepcopy(future)],
                                    BANK['questions']+future_questions,TASKS)
        for lesson in BANK['lessons']:
            for level in ('Easy','Medium','Hard'):
                fixture = copy.deepcopy(BANK['lessons'])
                item = next(l for l in fixture if l['id']==lesson['id'])
                # Remove the linked records themselves so ownership attachment cannot repair the gap.
                ids = {id for id in item['questions'] if QUESTIONS[id]['difficulty']==level}
                qs = [q for q in BANK['questions'] if q['id'] not in ids]
                item['questions'] = [id for id in item['questions'] if id not in ids]
                with self.assertRaises(ValueError,msg=(lesson['id'],level)):
                    attach_and_validate(fixture,qs,TASKS)

    def test_proper_loss_log_domain_and_coarse_pairing(self):
        q=F(3,4)
        loss=lambda p:q*(1-p)**2+(1-q)*p*p
        self.assertEqual(loss(1)-loss(q),F(1,16))
        self.assertEqual(QUESTIONS['q_l24_e1']['answer'],float(F(1,16)))
        self.assertAlmostEqual((math.log(4)+math.log(16))/2,math.log(8))
        self.assertEqual(QUESTIONS['q_l24_e2']['answer'],8)
        for x in (4,5,8,10,16):
            self.assertAlmostEqual((abs(math.log(x/4))+abs(math.log(x/16)))/2,math.log(2))
        self.assertEqual(((10-4)**2+(10-16)**2)/2,36)
        p=[F(1,10),F(9,10)]
        for y,expected,cov in [([0,1],F(1,100),F(1,5)),([1,0],F(81,100),-F(1,5))]:
            direct=sum((a-b)**2 for a,b in zip(p,y))/2
            covariance=sum((a-F(1,2))*(b-F(1,2)) for a,b in zip(p,y))/2
            self.assertEqual(direct,expected)
            self.assertEqual(covariance,cov)
            self.assertEqual(direct,F(4,25)+F(1,4)-2*covariance)

    def test_winning_joint_law_and_continuous_action_objective(self):
        for m in range(1,9):
            low=F(3,4)*F(4,5)**m; high=F(1,4)*F(2,5)**m
            self.assertEqual(high/(low+high),F(1,1+3*2**m))
        self.assertEqual(QUESTIONS['q_l24_m2']['answer'],float(F(100,13)))
        self.assertEqual(F(13,25)*(F(100,13)-10),-F(6,5))
        # Analytic derivative sign plus dense independent conditional payoff integration.
        for m in range(1,9):
            b=F(100*m,m+1)
            best=F(50*m**m,(m+1)**(m+1))
            self.assertEqual(F(1,2)*(100-b)*(b/100)**m,best)
            for i in range(201):
                low_win=min(F(i,100),1)**m
                high_win=max(F(i-100,100),0)**m
                gain=F(1,2)*((100-i)*low_win+(200-i)*high_win)
                self.assertLessEqual(gain,best)
                if i>100:self.assertLess(gain,0)
        self.assertEqual(F(1,2)*(-50+50*F(1,4)),-F(75,4))

    def test_population_refinement_and_calibration_by_finite_joint_tables(self):
        rng=random.Random(2413)
        for _ in range(150):
            # Entries (reported P, pre-outcome G, Y, integer population mass).
            rows=[(F(p,4),g,y,rng.randrange(1,20))
                  for p in range(5) for g in range(3) for y in (0,1)]
            total=sum(w for p,g,y,w in rows)
            rates={p:sum(y*w for pp,g,y,w in rows if pp==p)/F(sum(w for pp,g,y,w in rows if pp==p))
                   for p in {p for p,g,y,w in rows}}
            refined={(p,g):sum(y*w for pp,gg,y,w in rows if (pp,gg)==(p,g))/F(sum(w for pp,gg,y,w in rows if (pp,gg)==(p,g)))
                     for p,g,y,w in rows}
            loss=lambda fn:sum(F(w,total)*(fn(p,g)-y)**2 for p,g,y,w in rows)
            self.assertEqual(loss(lambda p,g:p)-loss(lambda p,g:rates[p]),
                sum(F(w,total)*(p-rates[p])**2 for p,g,y,w in rows))
            self.assertEqual(loss(lambda p,g:rates[p])-loss(lambda p,g:refined[p,g]),
                sum(F(w,total)*(refined[p,g]-rates[p])**2 for p,g,y,w in rows))
            for fn in (lambda p,g:rates[p], lambda p,g:refined[p,g]):
                for report in {fn(p,g) for p,g,y,w in rows}:
                    selected=[(y,w) for p,g,y,w in rows if fn(p,g)==report]
                    self.assertEqual(sum(y*w for y,w in selected)/F(sum(w for y,w in selected)),report)

    def test_weighted_score_random_definitions_and_canonical_outputs(self):
        rng=random.Random(2414);solve=reference('c_l24_medium')
        for _ in range(450):
            n=rng.randrange(1,60);d=rng.randrange(1,35)
            args=[[rng.randrange(d+1) for _ in range(n)],
                  [rng.randrange(2) for _ in range(n)],
                  [rng.randrange(6) for _ in range(n)],d]
            if not sum(args[2]):args[2][0]=1
            before=copy.deepcopy(args);actual=solve(*args)
            self.assertEqual(actual,score_oracle(*args));self.assertEqual(args,before)
            for value in actual.values():self.assertEqual(value,text(F(value)))
            self.assertEqual(F(actual['score']),F(actual['uncertainty'])-F(actual['resolution'])+F(actual['reliability']))
            args[2]=[17*w for w in args[2]]
            self.assertEqual(solve(*args),actual)
        for id in ('c_l24_medium',):
            for case in CODES[id]['samples']+CODES[id]['tests']:
                self.assertEqual(reference(id)(*case['args']),score_oracle(*case['args']))
        # Maximum forecast-level count with nontrivial exact denominators.
        args=[list(range(50)),[i%2 for i in range(50)],[10**9-i*113 for i in range(50)],10**9]
        self.assertEqual(solve(*args),score_oracle(*args))

    def test_integer_bids_exhaustive_actions_and_joint_pairing(self):
        rng=random.Random(2415);solve=reference('c_l24_hard')
        for _ in range(650):
            cap=rng.randrange(16)
            states=[[rng.randrange(-10,30),rng.randrange(20),rng.randrange(5)]
                    for _ in range(rng.randrange(1,30))]
            if not sum(w for v,h,w in states):states[0][2]=1
            before=copy.deepcopy(states);actual=solve(states,cap)
            self.assertEqual(actual,bid_oracle(states,cap));self.assertEqual(states,before)
            rng.shuffle(states);self.assertEqual(solve(states,cap),actual)
            self.assertEqual(solve([[v,h,w*29] for v,h,w in states],cap),actual)
        for case in CODES['c_l24_hard']['samples']+CODES['c_l24_hard']['tests']:
            states,cap=case['args']
            if cap<=200:
                self.assertEqual(solve(states,cap),bid_oracle(states,cap))
            self.assertEqual(solve(states,cap),case['expected'])
        # Identical marginal value and threshold lists, different pairings/optimal actions.
        a=[[100,0,1],[0,100,1]];b=[[0,0,1],[100,100,1]]
        self.assertNotEqual(solve(a,101),solve(b,101))

    def test_actual_judge_limits_and_large_official_debug_round_trip(self):
        for id in ('c14','c_l24_medium','c_l24_hard'):
            task=CODES[id];result=run(id,task['solution'],'submit')
            self.assertNotIn('error',result);self.assertEqual(result['passed'],result['total'],result)
            for case in submission_cases(id)['cases']:
                self.assertLessEqual(len(case['argumentsJSON'])+len(case['expectedJSON']),500000)
            if id=='c14':continue
            copied=submission_cases(id)['cases'][2]
            decoded=parse_debug_cases(task,[copied])
            self.assertEqual(decoded[0]['expected'],task['samples'][2]['expected'])
            self.assertEqual(decoded[0]['args'],task['samples'][2]['args'])
            copies=submission_cases(id)['cases'][:3]
            debug=run(id,task['solution'],'debug',debug_cases=copies+[copies[2]])
            self.assertNotIn('error',debug)
            self.assertEqual((debug['passed'],debug['total']),(4,4),debug)
        # A rounded numerical answer violates the exact-output contract.
        bad='def solve(probabilities,outcomes,weights,scale): return {"score":0.0,"reliability":0.0,"resolution":0.0,"uncertainty":0.0}'
        failed=run('c_l24_medium',bad,'submit')
        self.assertLess(failed['passed'],failed['total'])


if __name__ == '__main__':unittest.main()
