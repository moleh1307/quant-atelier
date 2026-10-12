"""Independent history replay and temporal noninterference checks.

The reference uses a sweep and heaps. This oracle rebuilds each decision's
eligible publication history, then directly selects its active event.
"""
import copy
import itertools
import random
import unittest
from unittest.mock import patch
from fractions import Fraction as F

from coding_bank import TASKS
from judge import run
from test_topic_practice import BANK, QUESTIONS, reference
from topic_practice import LEGACY_CODING_LINKS, attach_and_validate


def snapshot_by_history(updates, decisions, horizon):
    result = []
    for decision, key in decisions:
        history = sorted((row for row in updates if row[0] <= decision and row[2] == key),
                         key=lambda row: (row[0], row[1]))
        values = {}
        for _, _, _, event, value in history:
            values[event] = value
        active = [(event, value) for event, value in values.items()
                  if decision-horizon <= event <= decision and value is not None]
        result.append(max(active)[1] if active else None)
    return result


class DataTimePracticeTests(unittest.TestCase):
    def test_interview_boundaries_and_future_selected_population(self):
        rows = [(0,2),(1,4),(1,8),(4,10),(6,20)]
        eligible = [value for time,value in rows if 1 <= time < 4]
        self.assertEqual(F(sum(eligible),len(eligible)),6)
        self.assertEqual(QUESTIONS['q_l08_e1']['answer'],6)
        self.assertEqual(QUESTIONS['q_l08_e2']['answer'],9)
        pairs = list(itertools.product((0,1),repeat=2))
        kept = [(x,y) for x,y in pairs if x==y]
        given_one = [y for x,y in kept if x==1]
        self.assertEqual(F(sum(given_one),len(given_one)),1)
        self.assertEqual(F(len(kept),len(pairs)),F(1,2))
        self.assertEqual(F(sum(x==y for x,y in pairs),len(pairs)),F(1,2))
        causal_kept = [(x,y) for x,y in pairs if x==1]
        self.assertEqual(F(sum(x==y for x,y in causal_kept),len(causal_kept)),F(1,2))
        self.assertEqual(QUESTIONS['q_l08_m1']['answer'],1)
        rubric=QUESTIONS['q44']['rubric']
        self.assertIn('10:00:02',rubric[0])
        self.assertIn('as-of join',rubric[1])
        self.assertNotIn('State the assumptions and the object you are computing.',rubric)

    def test_final_vintage_identified_sets_and_threshold_equality(self):
        def profit(u,v): return (1 if u>=5 else -1)-(1 if v>=5 else -1)
        initial_values = list(range(11))
        self.assertEqual({profit(u,v) for u,v in itertools.product(initial_values,repeat=2)},
                         {-2,0,2})
        for bound,expected in [(2,{-2,0}),(1,{-2,0}),(F(99,100),{-2})]:
            # Include interval endpoints and the threshold as well as a dense
            # rational grid. These verify attainment; the prose proves all reals.
            values = [F(i,100) for i in range(1001)]
            us = [u for u in values if abs(u-4)<=bound]
            vs = [v for v in values if abs(v-8)<=bound]
            self.assertEqual({profit(u,v) for u,v in itertools.product(us,vs)},expected)
        self.assertEqual(profit(5,8),0,'A bound of one includes the switch point')
        # Independent fixed-precision lattice checks all shared-budget branches
        # and includes the exact one/four budget boundaries and a point just beyond 4.
        cheapest={-2:10000,0:10000,2:10000}
        for u in range(1001):
            for v in range(1001):
                payoff=(1 if u>=500 else -1)-(1 if v>=500 else -1)
                cost=abs(u-400)+abs(v-800)
                cheapest[payoff]=min(cheapest[payoff],cost)
        self.assertEqual(cheapest,{-2:0,0:100,2:401})
        for budget,expected in [(0,{-2}),(99,{-2}),(100,{-2,0}),
                                (400,{-2,0}),(401,{-2,0,2}),(500,{-2,0,2})]:
            self.assertEqual({p for p,cost in cheapest.items() if cost<=budget},expected)
        # For all real inputs producing +2 the symbolic proof uses u>=5,v<5.
        # The lattice minimum above is not presented as the real-valued infimum.

    def test_lagged_global_fit_violates_prefix_condition(self):
        def unsafe(values):
            mean=F(sum(values),len(values))
            return [None]+[F(values[i-1])-mean for i in range(1,len(values))]
        self.assertEqual(unsafe([1,3])[1],-1)
        self.assertEqual(unsafe([1,103])[1],-51)
        self.assertNotEqual(unsafe([1,3])[1],unsafe([1,3,100])[1])
        # A fixed pre-stream mean has a causal dependence argument, illustrated
        # here across different continuations and lengths. This is not claimed
        # to prove the universal theorem by finite testing.
        def fixed(values): return [None]+[values[i-1]-7 for i in range(1,len(values))]
        for suffix in [[0],[99],[-99,99],[0,0,0]]:
            self.assertEqual(fixed([1]+suffix)[1],-6)

    def test_elapsed_window_counts_against_explicit_membership(self):
        solve=reference('c_l08_easy')
        for n in range(7):
            for times in itertools.combinations_with_replacement(range(5),n):
                for horizon in range(1,6):
                    expected=[sum(t-horizon<=other<t for other in times) for t in times]
                    data=list(times)
                    self.assertEqual(solve(data,horizon),expected,(times,horizon))
                    self.assertEqual(data,list(times))

    def test_original_medium_against_independent_eligible_row_scan(self):
        solve=reference('c06')
        rng=random.Random(806)
        for _ in range(250):
            events=sorted([[rng.randrange(10),rng.randrange(-10,11)]
                           for _ in range(rng.randrange(20))],key=lambda row:row[0])
            decisions=sorted(rng.randrange(12) for _ in range(rng.randrange(15)))
            expected=[]
            for decision in decisions:
                eligible=[value for timestamp,value in events if timestamp<=decision]
                expected.append(eligible[-1] if eligible else None)
            self.assertEqual(solve(events,decisions),expected)

    def test_revisions_against_rebuilt_snapshot_oracle(self):
        solve=reference('c_l08_hard')
        rng=random.Random(808)
        for _ in range(750):
            updates=[]
            for sequence in range(rng.randrange(30)):
                available=rng.randrange(13)
                event=rng.randrange(available+1)
                value=rng.choice([None,0,-2,7,19])
                updates.append([available,sequence,rng.choice(['A','B','C']),event,value])
            rng.shuffle(updates)
            decisions=[[rng.randrange(16),rng.choice(['A','B','C','absent'])]
                       for _ in range(rng.randrange(20))]
            horizon=rng.randrange(1,9)
            inputs=copy.deepcopy([updates,decisions])
            expected=snapshot_by_history(updates,decisions,horizon)
            self.assertEqual(solve(updates,decisions,horizon),expected)
            self.assertEqual([updates,decisions],inputs)
            self.assertEqual(solve(list(reversed(updates)),decisions,horizon),expected,
                             'Unique sequence precedence is independent of input order')

    def test_future_revisions_and_unrelated_keys_cannot_change_past(self):
        solve=reference('c_l08_hard')
        history=[[1,1,'A',0,4],[2,2,'A',2,8],[3,3,'A',0,9]]
        decisions=[[3,'A'],[2,'A'],[1,'A'],[3,'A']]
        expected=[8,8,4,8]
        self.assertEqual(solve(history,decisions,5),expected)
        future=[[4,4,'A',2,None],[5,5,'A',2,-999],[9,6,'A',0,100]]
        unrelated=[[3,7,'B',3,999]]
        self.assertEqual(solve(history+future+unrelated,decisions,5),expected)
        later=[[4,'A'],[5,'A'],[6,'A'],[8,'A']]
        self.assertEqual(solve(history+future,later,5),[9,-999,-999,None])

    def test_published_cases_against_separate_oracles(self):
        for task in TASKS:
            if task['id'] not in ('c_l08_easy','c_l08_hard'): continue
            for case in task['samples']+task['tests']:
                if task['id']=='c_l08_easy':
                    times,horizon=case['args']
                    # Direct membership is deliberately quadratic. For the
                    # long arithmetic progression, count its endpoints exactly.
                    if len(times)>1000:
                        self.assertEqual(times,list(range(len(times))))
                        expected=[min(i,horizon) for i in range(len(times))]
                    else:
                        expected=[sum(t-horizon<=other<t for other in times) for t in times]
                else:
                    expected=snapshot_by_history(*case['args'])
                self.assertEqual(case['expected'],expected,task['id'])

    def test_legacy_code_is_outside_current_slots_and_preserved(self):
        lesson=next(l for l in BANK['lessons'] if l['id']=='l08')
        self.assertEqual(lesson['legacyCoding'],['c05'])
        self.assertEqual(lesson['coding'],['c_l08_easy','c06','c_l08_hard'])
        self.assertEqual(reference('c05')([2,4,8,10],2),[None,None,3,6])

    def test_validator_requires_preserved_removed_bookmarks(self):
        original=copy.deepcopy(BANK['lessons'])
        next(l for l in original if l['id']=='l08')['coding']=['c05','c06']
        with patch.dict(LEGACY_CODING_LINKS,{},clear=True):
            with self.assertRaisesRegex(ValueError,'Preserve removed coding bookmarks'):
                attach_and_validate(original,BANK['questions'],TASKS)
        for links,message in [(['c06'],'distinct'),(['missing'],'Broken additional'),
                              (['c05','c05'],'distinct')]:
            with patch.dict(LEGACY_CODING_LINKS,{'l08':links},clear=True):
                with self.assertRaisesRegex(ValueError,message):
                    attach_and_validate(copy.deepcopy(BANK['lessons']),BANK['questions'],TASKS)

    def test_judge_rejects_current_time_and_last_publication_shortcuts(self):
        wrong_easy='''def solve(times, horizon):
    return [sum(t-horizon<=v<=t for v in times[:i]) for i,t in enumerate(times)]'''
        self.assertLess(run('c_l08_easy',wrong_easy)['passed'],
                        len(next(t for t in TASKS if t['id']=='c_l08_easy')['samples'])+
                        len(next(t for t in TASKS if t['id']=='c_l08_easy')['tests']))
        wrong_hard='''def solve(updates, decisions, horizon):
    result = []
    for time,key in decisions:
        rows = sorted([r for r in updates if r[0]<=time and r[2]==key and r[3]>=time-horizon])
        result.append(rows[-1][-1] if rows else None)
    return result'''
        result=run('c_l08_hard',wrong_hard)
        self.assertLess(result['passed'],result['total'])


if __name__=='__main__':
    unittest.main()
