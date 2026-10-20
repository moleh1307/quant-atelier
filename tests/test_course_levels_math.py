"""Independent finite enumerations for the l01–l03 progressive chapters.

These compare the written probability arguments with explicit experiments;
no learner records, judge submissions or application formula helpers are used.
"""
import itertools as it
import math
import unittest
from collections import Counter
from fractions import Fraction as F

class ProgressiveCourseMathTests(unittest.TestCase):
    def test_group_and_multiplicity_weights(self):
        counts = Counter(sum(i < 6 for i in subset) for subset in it.combinations(range(10), 3))
        self.assertEqual([counts[j] for j in range(4)], [4, 36, 60, 20])
        groups = Counter(tuple(sorted(x)) for x in it.product('ABC', repeat=3))
        self.assertEqual([groups[tuple(x)] for x in ['AAA', 'AAB', 'ABC']], [1, 3, 6])
        for d in range(1, 5):
            for k in range(5):
                observed = Counter(tuple(x.count(i) for i in range(d)) for x in it.product(range(d), repeat=k))
                for counts, actual in observed.items():
                    self.assertEqual(actual, math.factorial(k) // math.prod(math.factorial(c) for c in counts))

    def test_collision_complement_and_approximation_direction(self):
        for n in range(1, 6):
            for k in range(6):
                actual = F(sum(len(set(x)) < len(x) for x in it.product(range(n), repeat=k)), n**k)
                exact = F(1) - math.prod(F(n-j, n) for j in range(k)) if k <= n else F(1)
                self.assertEqual(actual, exact)
                self.assertLessEqual(1-math.exp(-k*(k-1)/(2*n)), float(exact)+1e-14)
        self.assertEqual(F(1)-F(3,4)*F(2,4), F(5,8))

    def test_derangements_and_exact_fixed_points(self):
        derangements = []
        for n in range(8):
            perms = list(it.permutations(range(n)))
            counts = Counter(sum(i == x for i, x in enumerate(p)) for p in perms)
            d = sum((-1)**j*math.comb(n,j)*math.factorial(n-j) for j in range(n+1))
            derangements.append(d)
            self.assertEqual(counts[0], d)
            for r in range(n+1):
                self.assertEqual(counts[r], math.comb(n,r)*derangements[n-r])
        self.assertEqual(4*derangements[3], 8)

    def test_bayes_reporting_and_attainable_dependence_bound(self):
        self.assertEqual(F(90,90+495), F(2,13))
        for s, expected in [(F(1),F(1,3)), (F(1,2),F(1,2))]:
            likelihood = [F(1),s,s,F(0)]
            self.assertEqual(likelihood[0]/sum(likelihood), expected)
        affected, absent = [F(3,5), F(1,5), F(1,5), F(0)], [F(1,5),F(0),F(0),F(4,5)]
        for table, marginal in [(affected,F(4,5)),(absent,F(1,5))]:
            self.assertEqual(sum(table), 1)
            self.assertEqual(table[0]+table[1], marginal)
            self.assertEqual(table[0]+table[2], marginal)
        prior=F(1,10)
        posterior=lambda a,b:prior*a/(prior*a+(1-prior)*b)
        self.assertEqual(posterior(affected[0],absent[0]),F(1,4))
        for a in [F(i,100) for i in range(60,81)]:
            for b in [F(j,100) for j in range(21)]:
                self.assertGreaterEqual(posterior(a,b),F(1,4))
        self.assertEqual(posterior(F(16,25), F(1,25)), F(16,25))

    def test_moving_hidden_state_against_joint_paths(self):
        prior=[F(1,2)]*2; transition=[[F(9,10),F(1,10)],[F(1,10),F(9,10)]]; heads=[F(4,5),F(1,5)]
        weights=[sum(prior[i]*heads[i]*transition[i][j]*heads[j] for i in range(2)) for j in range(2)]
        self.assertEqual(weights[0]/sum(weights),F(148,161))
        self.assertEqual(sum(weights), F(161,500))
        self.assertEqual(prior[0]*heads[0]**2/sum(prior[j]*heads[j]**2 for j in range(2)),F(16,17))
        self.assertAlmostEqual(math.exp(-1000-(-1000))/(math.exp(0)+math.exp(-1)), 1/(1+math.exp(-1)))

    def test_distinct_and_singleton_indicator_claims(self):
        for n in range(1,5):
            for m in range(1,5):
                records=list(it.product(range(n), repeat=m))
                self.assertEqual(F(sum(len(set(x)) for x in records),len(records)),n*(1-F(n-1,n)**m))
                self.assertEqual(F(sum(sum(c==1 for c in Counter(x).values()) for x in records),len(records)),m*F(n-1,n)**(m-1))
        self.assertEqual(4*(1-F(3,4)**3),F(37,16))

    def test_cycle_count_and_constraint(self):
        for n in range(1,8):
            total=[0]*(n+1)
            for perm in it.permutations(range(n)):
                visited=set(); lengths=[]
                for i in range(n):
                    if i in visited: continue
                    j=i; size=0
                    while j not in visited:
                        visited.add(j);size+=1;j=perm[j]
                    lengths.append(size)
                self.assertEqual(sum(lengths),n)
                for size in lengths: total[size]+=1
            for j in range(1,n+1):self.assertEqual(F(total[j],math.factorial(n)),F(1,j))

    def test_matching_crossings(self):
        def matchings(points):
            if not points: yield ();return
            a=points[0]
            for i in range(1,len(points)):
                for rest in matchings(points[1:i]+points[i+1:]):yield ((a,points[i]),)+rest
        for m in range(2,6):
            values=[]
            for pairs in matchings(tuple(range(2*m))):
                values.append(sum((a<c<b<d or c<a<d<b) for (a,b),(c,d) in it.combinations(pairs,2)))
            self.assertEqual(F(sum(values),len(values)),F(m*(m-1),6))

    def test_rank_weights_including_ties_and_negative_labels(self):
        for n in range(1,9):
            values=sorted((i//2)-2 for i in range(n))
            for k in range(1,n+1):
                subsets=list(it.combinations(range(n),k))
                for r in range(1,k+1):
                    counts=Counter(subset[r-1]+1 for subset in subsets)
                    for j in range(r,n-k+r+1):
                        self.assertEqual(counts[j],math.comb(j-1,r-1)*math.comb(n-j,k-r))
                    self.assertEqual(sum(counts.values()), math.comb(n,k))
                    weighted=sum(F(values[j-1]*counts[j],len(subsets)) for j in counts)
                    self.assertEqual(weighted,F(sum(values[subset[r-1]] for subset in subsets),len(subsets)))
        self.assertEqual(F(1+8+27,6),6)

if __name__ == '__main__': unittest.main()
