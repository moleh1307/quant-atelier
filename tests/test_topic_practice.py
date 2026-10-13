"""Independent counting and finite-model checks for expanded topic practice.

No personal workspace, HTTP progress endpoint or progress fixture is touched.
References are checked against enumerated records, not against themselves.
"""
import copy
import itertools
import json
import math
import random
import unittest
from collections import Counter
from fractions import Fraction
from pathlib import Path

from coding_bank import TASKS
from judge import run
from topic_practice import COMPLETE_TOPICS, DIFFICULTIES, attach_and_validate

ROOT = Path(__file__).resolve().parents[1]
BANK = json.loads((ROOT / 'static/content.json').read_text())
QUESTIONS = {q['id']: q for q in BANK['questions']}
CODES = {c['id']: c for c in TASKS}


def reference(id):
    namespace = {}
    exec(CODES[id]['solution'], namespace)
    return namespace['solve']


def matchings(points):
    if not points:
        yield []
    else:
        a = points[0]
        for i in range(1, len(points)):
            for rest in matchings(points[1:i] + points[i+1:]):
                yield [(a, points[i])] + rest


class TopicPracticeTests(unittest.TestCase):
    def test_contract_and_future_topic_guard(self):
        for l in BANK['lessons']:
            self.assertTrue(l['practiceExpanded'])
            qs = Counter(QUESTIONS[id]['difficulty'] for id in l['questions'])
            cs = Counter(CODES[id]['difficulty'] for id in l['coding'])
            self.assertTrue(all(qs[level] >= 2 for level in DIFFICULTIES), l['id'])
            self.assertEqual(cs, Counter(DIFFICULTIES), l['id'])
        # A future lesson cannot be silently published without registration.
        future = copy.deepcopy(BANK['lessons']) + [{'id': 'l29'}]
        with self.assertRaisesRegex(ValueError, 'Register every new lesson'):
            attach_and_validate(future, BANK['questions'], TASKS)
        missing_hard = [q for q in BANK['questions'] if q['id'] != 'q_l01_h1']
        with self.assertRaises(ValueError):
            attach_and_validate(copy.deepcopy(BANK['lessons']), missing_hard, TASKS)

    def test_old_ids_and_new_written_rubrics(self):
        self.assertTrue({f'q{i:02d}' for i in range(1,52)} <= QUESTIONS.keys())
        self.assertTrue({f'c{i:02d}' for i in range(1,16)} <= CODES.keys())
        for id, q in QUESTIONS.items():
            if not id.startswith('q_l'):
                continue
            self.assertGreaterEqual(len(q['rubric']), 2)
            self.assertTrue(q['solution'].strip())
            self.assertTrue(q['followSolution'])
            self.assertNotIn('State the assumptions and the object you are computing.', q['rubric'])

    def test_sample_space_interview_answers(self):
        colours = 'R'*5 + 'B'*4 + 'G'*3
        samples = list(itertools.combinations(range(12), 3))
        favourable = sum(len({colours[i] for i in draw}) == 2 for draw in samples)
        self.assertEqual(Fraction(favourable, len(samples)), Fraction(29,44))
        counts = Counter()
        for draw in itertools.product(range(5), repeat=5):
            multiplicities = sorted(Counter(draw).values(), reverse=True)
            if len(multiplicities) == 3:
                counts[tuple(multiplicities)] += 1
        self.assertEqual(counts, {(3,1,1):600, (2,2,1):900})
        self.assertEqual(Fraction(counts[(3,1,1)],sum(counts.values())), Fraction(2,5))
        permutations = list(itertools.permutations(range(6)))
        one_match = sum(sum(i == p[i] for i in range(6)) == 1 for p in permutations)
        self.assertEqual(Fraction(one_match,len(permutations)), Fraction(11,30))
        for id, value in [('q_l01_m2',29/44), ('q_l01_h1',2/5), ('q_l01_h2',11/30)]:
            self.assertEqual(QUESTIONS[id]['answer'], value)

    def test_conditioning_interview_answers_and_attainable_tables(self):
        prior = Fraction(1,10)
        present = [Fraction(3,5), Fraction(1,5), Fraction(1,5), 0]
        absent = [Fraction(1,5), 0, 0, Fraction(4,5)]
        for table, marginal in [(present,Fraction(4,5)),(absent,Fraction(1,5))]:
            self.assertEqual(sum(table),1)
            self.assertEqual(table[0]+table[1],marginal)
            self.assertEqual(table[0]+table[2],marginal)
        lower = prior*present[0]/(prior*present[0]+(1-prior)*absent[0])
        self.assertEqual(lower,Fraction(1,4))
        # Enumerate feasible intersections on a rational grid; endpoints attain
        # the bounds and monotonicity is also explicit in the worked solution.
        posterior = []
        for a in map(lambda x: Fraction(x,100), range(60,81)):
            for b in map(lambda x: Fraction(x,100), range(21)):
                posterior.append(prior*a/(prior*a+(1-prior)*b))
        self.assertEqual(min(posterior),lower)
        self.assertEqual(max(posterior),1)
        likelihood = [Fraction(1,4),Fraction(3,4)]
        predictive = sum(p*p for p in likelihood)
        self.assertEqual(predictive,Fraction(5,8))
        self.assertEqual(QUESTIONS['q_l02_m1']['answer'],float(predictive))

    def test_expectation_interview_answers(self):
        samples = list(itertools.combinations(range(1,9),3))
        self.assertEqual(Fraction(sum(map(sum,samples)),len(samples)),Fraction(27,2))
        def cycles(p):
            seen=set(); count=0
            for i in range(len(p)):
                if i in seen: continue
                count+=1
                j=i
                while j not in seen:
                    seen.add(j);j=p[j]
            return count
        permutations=list(itertools.permutations(range(6)))
        self.assertEqual(Fraction(sum(map(cycles,permutations)),len(permutations)),Fraction(49,20))
        for n in range(2,5):
            pairings=list(matchings(list(range(2*n))))
            total=0
            for pairing in pairings:
                for (a,b),(c,d) in itertools.combinations(pairing,2):
                    # Points are in circular order and a<b, c<d.
                    total += (a<c<b) != (a<d<b)
            self.assertEqual(Fraction(total,len(pairings)),Fraction(n*(n-1),6))
        self.assertEqual(QUESTIONS['q_l03_h1']['answer'],49/20)
        self.assertEqual(QUESTIONS['q_l03_h2']['answer'],15)

    def test_unordered_records_against_physical_draws(self):
        solve=reference('c_l01_medium')
        for counts in itertools.product(range(3),repeat=3):
            physical=[i for i,c in enumerate(counts) for _ in range(c)]
            for replacement in [False,True]:
                draws=(itertools.product(range(len(physical)),repeat=2) if replacement
                       else itertools.permutations(range(len(physical)),2))
                frequencies=Counter(tuple(sorted([physical[a],physical[b]])) for a,b in draws)
                denominator=sum(frequencies.values())
                expected=([[i,j,frequencies[(i,j)]/denominator] for i in range(3) for j in range(i,3)]
                          if denominator else [])
                self.assertEqual(solve(list(counts),replacement),expected)

    def test_assignment_dp_against_permutations(self):
        solve=reference('c_l01_hard')
        for bits in itertools.product([0,1],repeat=9):
            allowed=[list(bits[i:i+3]) for i in range(0,9,3)]
            expected=sum(all(allowed[i][p[i]] for i in range(3)) for p in itertools.permutations(range(3)))
            self.assertEqual(solve(allowed),expected)
        self.assertEqual(solve([[int(i!=j) for j in range(5)] for i in range(5)]),44)

    def test_dynamic_conditioning_against_exact_hidden_paths(self):
        solve=reference('c_l02_hard')
        rng=random.Random(17)
        fractions=[Fraction(0),Fraction(1,4),Fraction(1,2),Fraction(3,4),Fraction(1)]
        for _ in range(100):
            p=rng.choice(fractions); prior=[p,1-p]
            a,b=rng.choice(fractions),rng.choice(fractions)
            transition=[[a,1-a],[b,1-b]]
            likelihoods=[[rng.choice(fractions),rng.choice(fractions)] for _ in range(3)]
            masses=[Fraction(0),Fraction(0)]
            for path in itertools.product(range(2),repeat=3):
                mass=prior[path[0]]*likelihoods[0][path[0]]
                for t in range(1,3):
                    mass*=transition[path[t-1]][path[t]]*likelihoods[t][path[t]]
                masses[path[-1]]+=mass
            total=sum(masses)
            got=solve(list(map(float,prior)),[[float(v) for v in row] for row in transition],
                      [[float(v) for v in row] for row in likelihoods])
            if total==0: self.assertIsNone(got)
            else:
                for actual,expected in zip(got[0],masses):
                    self.assertAlmostEqual(actual,float(expected/total),places=12)
                self.assertAlmostEqual(got[1],math.log(float(total)),places=12)
        # A state too small for ordinary probabilities must be recoverable.
        got=solve([.5,.5],[[1,0],[0,1]],[[1e-200,1],[1e-200,1],[1,0]])
        self.assertEqual(got[0],[1,0])
        self.assertAlmostEqual(got[1],math.log(.5)+2*math.log(1e-200),places=10)

    def test_expected_rank_against_all_subsets_with_ties(self):
        solve=reference('c_l03_hard')
        for n in range(1,6):
            for values in itertools.product([-1,0,2],repeat=n):
                for k in range(1,n+1):
                    samples=[sorted(values[i] for i in indices) for indices in itertools.combinations(range(n),k)]
                    for r in range(1,k+1):
                        expected=sum(sample[r-1] for sample in samples)/len(samples)
                        self.assertAlmostEqual(solve(list(values),k,r),expected,places=12)

    def test_all_new_references_pass_actual_judge_and_preserve_input(self):
        for task in TASKS:
            if not task['id'].startswith('c_l'): continue
            result=run(task['id'],task['solution'])
            self.assertNotIn('error',result,task['id'])
            self.assertEqual(result['passed'],result['total'],task['id'])
            solve=reference(task['id'])
            for case in task['samples']+task['tests']:
                args=copy.deepcopy(case['args']); original=copy.deepcopy(args)
                solve(*args)
                self.assertEqual(args,original,task['id'])


if __name__=='__main__':
    unittest.main()
