"""Independent finite enumerations and rational equations for l04/l05.

No workspace or progress endpoint is accessed. Coin-pattern references use
failure links; this suite instead solves a full rational first-step system.
"""
import copy
import itertools
import math
import random
import unittest
from fractions import Fraction as F

from coding_bank import TASKS
from judge import run
from test_topic_practice import QUESTIONS, reference


def joint_outcomes(distributions):
    for records in itertools.product(*distributions):
        values = [value for value, _ in records]
        mass = math.prod(probability for _, probability in records)
        yield values, mass


def exact_linear_solve(matrix, rhs):
    n = len(rhs)
    rows = [[F(value) for value in row] + [F(value)]
            for row, value in zip(matrix, rhs)]
    for column in range(n):
        pivot = next(i for i in range(column, n) if rows[i][column])
        rows[column], rows[pivot] = rows[pivot], rows[column]
        factor = rows[column][column]
        rows[column] = [v / factor for v in rows[column]]
        for i in range(n):
            if i == column:
                continue
            factor = rows[i][column]
            rows[i] = [a - factor*b for a, b in zip(rows[i], rows[column])]
    return [row[-1] for row in rows]


def pattern_mean_from_states(pattern, probability):
    """Direct suffix search for every transition; no border expectation formula."""
    n = len(pattern)
    matrix = [[F(int(i == j)) for j in range(n)] for i in range(n)]
    for i in range(n):
        for symbol, mass in [('H', probability), ('T', 1-probability)]:
            history = pattern[:i] + symbol
            next_state = max(j for j in range(n+1)
                             if history.endswith(pattern[:j]))
            if next_state < n:
                matrix[i][next_state] -= mass
    return exact_linear_solve(matrix, [1]*n)[0]


class DistributionStoppingPracticeTests(unittest.TestCase):
    def test_density_and_hidden_race_answers(self):
        # Integrate the explicitly polynomial density at rational boundaries.
        self.assertEqual(F(1) - F(3,4)**2, F(7,16))
        self.assertEqual(QUESTIONS['q_l04_e1']['answer'], 7/16)
        prior = F(1,2)
        survival_a, survival_b = F(1,2)**5, F(1,2)**2
        evidence = prior*survival_a + prior*survival_b
        winner_and_evidence = prior*survival_a*F(4,5) + prior*survival_b*F(1,2)
        self.assertEqual(prior*survival_a/evidence, F(1,9))
        self.assertEqual(winner_and_evidence/evidence, F(8,15))
        self.assertEqual(QUESTIONS['q_l04_h1']['answer'], 8/15)
        density_total = prior*5*survival_a + prior*2*survival_b
        density_x = prior*4*survival_a + prior*survival_b
        self.assertEqual(density_x/density_total, F(4,7))
        # Quiet-time information changes regime weights, so prior mixing fails.
        self.assertNotEqual(winner_and_evidence/evidence, F(13,20))

    def test_discrete_distribution_references_against_joint_enumeration(self):
        cdf = reference('c_l04_easy')
        minimum = reference('c_l04_medium')
        rank_cdf = reference('c_l04_hard')
        rng = random.Random(405)
        for _ in range(100):
            distributions = []
            for j in range(rng.randint(1,4)):
                values = rng.sample(range(-3,5), rng.randint(1,3))
                weights = [rng.randint(0,4) for _ in values]
                if not sum(weights): weights[0] = 1
                distributions.append([[v,F(w,sum(weights))]
                                      for v,w in zip(values,weights)])
            numeric = [[[v,float(p)] for v,p in pmf] for pmf in distributions]
            support = sorted({v for pmf in distributions for v,_ in pmf})
            expected_min = {v:F(0) for v in support}
            thresholds = [8,0,-5,2,0,-1]
            expected_rank = [[F(0) for _ in thresholds] for _ in distributions]
            for values, mass in joint_outcomes(distributions):
                expected_min[min(values)] += mass
                ordered = sorted(values)
                for r, value in enumerate(ordered):
                    for i,t in enumerate(thresholds):
                        if value <= t: expected_rank[r][i] += mass
            # Waiting-time support is nonnegative: shift this separate minimum
            # model by three while keeping the rank task's negative values.
            nonnegative = [[[v+3,p] for v,p in pmf] for pmf in numeric]
            actual_min = minimum(nonnegative)
            self.assertEqual([v for v,_ in actual_min], [v+3 for v in support])
            for (_,actual), expected in zip(actual_min,expected_min.values()):
                self.assertAlmostEqual(actual,float(expected),places=12)
            self.assertAlmostEqual(sum(p for _,p in actual_min),1,places=12)
            for r, expected in enumerate(expected_rank,1):
                actual = rank_cdf(numeric,r,thresholds)
                for a,e in zip(actual,expected): self.assertAlmostEqual(a,float(e),places=12)
            first = distributions[0]
            expected = [sum(p for v,p in first if v<=t) for t in thresholds]
            for a,e in zip(cdf(numeric[0],thresholds),expected):
                self.assertAlmostEqual(a,float(e),places=12)
            before = copy.deepcopy(numeric)
            rank_cdf(numeric,1,thresholds)
            self.assertEqual(numeric,before)

    def test_unequal_collector_by_exact_seen_set_recurrences(self):
        probabilities = [F(1,2),F(1,3),F(1,6)]
        # Solve backwards over seen subsets: repeats stay in the same subset,
        # a new symbol always leads to a strictly larger set.
        expected = {7:F(0)}
        for mask in range(6,-1,-1):
            repeat = sum(p for i,p in enumerate(probabilities) if mask & (1<<i))
            continuation = sum(p*expected[mask | (1<<i)]
                               for i,p in enumerate(probabilities) if not mask & (1<<i))
            expected[mask] = (1+continuation)/(1-repeat)
        self.assertEqual(expected[0],F(73,10))
        self.assertEqual(QUESTIONS['q_l05_h1']['answer'],73/10)
        self.assertNotEqual(expected[1],expected[4])

    def test_walk_probability_duration_and_infinite_mean_bound(self):
        self.assertEqual(QUESTIONS['q_l05_e2']['answer'],2/5)
        for n in range(2,26):
            transitions = [[F(int(i==j)) for j in range(n-1)] for i in range(n-1)]
            for i in range(n-1):
                if i>0: transitions[i][i-1] -= F(1,2)
                if i<n-2: transitions[i][i+1] -= F(1,2)
            hitting = exact_linear_solve(transitions,[0]*(n-2)+[F(1,2)])
            durations = exact_linear_solve(transitions,[1]*(n-1))
            self.assertEqual(hitting[0],F(1,n))
            self.assertEqual(durations[0],n-1)
            for i,(h,t) in enumerate(zip(hitting,durations),1):
                self.assertEqual(h,F(i,n))
                self.assertEqual(t,i*(n-i))
        # This verifies each finite comparison used in the proof. Infinite
        # expectation itself is the argument for all N, not a simulation claim.

    def test_arbitrary_pattern_mean_by_rational_first_step_systems(self):
        solve = reference('c_l05_hard')
        for length in range(1,7):
            for symbols in itertools.product('HT',repeat=length):
                pattern = ''.join(symbols)
                for heads,total in [(1,2),(1,4),(3,4)]:
                    expected = pattern_mean_from_states(pattern,F(heads,total))
                    actual = solve(pattern,heads,total)
                    self.assertTrue(math.isclose(actual,float(expected),rel_tol=2e-15,abs_tol=1e-12),
                                    (pattern,heads,total,actual,expected))
        self.assertEqual(solve('HTH',1,2),10)
        self.assertEqual(solve('HHT',1,2),8)
        self.assertEqual(solve('H'*200,1,2),float(2**201-2))
        self.assertEqual(solve('T'+'H'*199,1,10),float(F(10**200,9)))

    def test_wrong_shortcuts_are_rejected_by_actual_bank(self):
        shortcuts = {
            'c_l04_easy': 'def solve(distribution, thresholds):\n    return [sum(p for v,p in distribution if v<t) for t in thresholds]',
            'c_l05_easy': 'def solve(success_probabilities):\n    return sum(1/p-1 for p in success_probabilities if p)',
            'c_l05_hard': 'def solve(pattern, heads, total):\n    return total**len(pattern)/(heads**pattern.count("H")*(total-heads)**pattern.count("T"))',
        }
        for task_id, code in shortcuts.items():
            result = run(task_id,code)
            self.assertNotIn('error',result,task_id)
            self.assertLess(result['passed'],result['total'],task_id)

    def test_new_official_samples_and_tests_have_independent_expectations(self):
        # Check published cases too, not just the code on an unrelated model.
        for task in TASKS:
            if not task['id'].startswith(('c_l04_', 'c_l05_')): continue
            for case in task['samples']+task['tests']:
                args = case['args']
                if task['id']=='c_l04_easy':
                    pmf, thresholds = args
                    expected = [sum(F(p) for v,p in pmf if v<=t) for t in thresholds]
                elif task['id']=='c_l04_medium':
                    distributions = args[0]
                    if len(distributions)>4: continue  # binomial extreme checked below
                    support = sorted({v for pmf in distributions for v,_ in pmf})
                    pmfs = [[[v,F(p)] for v,p in pmf] for pmf in distributions]
                    masses = {v:F(0) for v in support}
                    for values,mass in joint_outcomes(pmfs): masses[min(values)] += mass
                    expected = [[v,float(masses[v])] for v in support]
                elif task['id']=='c_l04_hard':
                    distributions,rank,thresholds = args
                    if len(distributions)>4: continue
                    pmfs = [[[v,F(p)] for v,p in pmf] for pmf in distributions]
                    expected = [F(0)]*len(thresholds)
                    for values,mass in joint_outcomes(pmfs):
                        value = sorted(values)[rank-1]
                        for i,t in enumerate(thresholds):
                            if value<=t: expected[i] += mass
                elif task['id']=='c_l05_easy':
                    probabilities = args[0]
                    expected = None if 0 in probabilities else sum(1/F(p) for p in probabilities)
                else:
                    pattern,heads,total = args
                    if len(pattern)>6: continue
                    expected = pattern_mean_from_states(pattern,F(heads,total))
                def compare(actual, expected):
                    if expected is None: self.assertIsNone(actual)
                    elif isinstance(expected,list):
                        self.assertEqual(len(actual),len(expected))
                        for a,e in zip(actual,expected): compare(a,e)
                    else: self.assertTrue(math.isclose(actual,float(expected),rel_tol=2e-15,abs_tol=1e-12),(task['id'],args,actual,expected))
                compare(case['expected'],expected)
        rank_case = next(t for t in TASKS if t['id']=='c_l04_hard')['tests'][-2]
        self.assertEqual(rank_case['expected'],[float(F(sum(math.comb(60,j) for j in range(30,61)),2**60))])


if __name__ == '__main__':
    unittest.main()
