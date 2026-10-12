"""Finite evidence identities and an independent exact continuous LP oracle."""
import copy
import itertools
import math
import random
import unittest
from collections import Counter
from fractions import Fraction as F
from coding_bank import TASKS
from judge import run,submission_cases,parse_debug_cases
from test_topic_practice import BANK,QUESTIONS,reference


def pair(value):
    value=F(value)
    return [str(value.numerator),str(value.denominator)]


def linear_solve(rows,rhs):
    a=[[F(x) for x in row]+[F(y)] for row,y in zip(rows,rhs)];n=len(rows)
    for col in range(n):
        pivot=next((r for r in range(col,n) if a[r][col]),None)
        if pivot is None:return None
        a[col],a[pivot]=a[pivot],a[col]
        scale=a[col][col];a[col]=[x/scale for x in a[col]]
        for r in range(n):
            if r==col:continue
            scale=a[r][col]
            a[r]=[x-scale*y for x,y in zip(a[r],a[col])]
    return [row[-1] for row in a]


def continuous_lp(counts,payoffs,budget):
    """Vertices of the TV epigraph; no donor sorting or greedy allocation."""
    n=len(counts);p=[F(c,sum(counts)) for c in counts];epsilon=F(*budget)
    constraints=[]
    for i in range(n):
        row=[0]*(n+1);row[i]=-1;constraints.append((row,F(0)))
    # TV(q,p)=max over subsets S of q(S)-p(S).
    for bits in itertools.product((0,1),repeat=n):
        if not any(bits) or all(bits):continue
        constraints.append((list(bits)+[-1],sum((p[i] for i,b in enumerate(bits) if b),F(0))))
    constraints += [([0]*n+[-1],F(0)),([0]*n+[1],epsilon)]
    best=None
    for active in itertools.combinations(constraints,n):
        rows=[[1]*n+[0]]+[row for row,bound in active]
        rhs=[F(1)]+[bound for row,bound in active]
        point=linear_solve(rows,rhs)
        if point is None:continue
        if any(sum(a*x for a,x in zip(row,point))>bound for row,bound in constraints):continue
        objective=sum(g*q for g,q in zip(payoffs,point))
        candidate=(objective,point[-1])
        if best is None or candidate<best:best=candidate
    return {'worst_mean':pair(best[0]),'used_tv':pair(best[1])}


def compositions(total,n):
    if n==1:
        yield (total,)
    else:
        for k in range(total+1):
            for rest in compositions(total-k,n-1):yield (k,)+rest


def grid_oracle(counts,payoffs,budget):
    # Independent exhaustive admissible probability vectors in exact mass units.
    w=sum(counts);a,b=budget;d=w*b;best=None
    for units in compositions(d,len(counts)):
        tv=F(sum(abs(u-c*b) for u,c in zip(units,counts)),2*d)
        if tv>F(a,b):continue
        mean=F(sum(u*g for u,g in zip(units,payoffs)),d)
        candidate=(mean,tv)
        if best is None or candidate<best:best=candidate
    return {'worst_mean':pair(best[0]),'used_tv':pair(best[1])}


class ResearchDefencePracticeTests(unittest.TestCase):
    def test_contract_permanent_slots_specific_rubrics(self):
        lesson=next(l for l in BANK['lessons'] if l['id']=='l16')
        self.assertEqual(lesson['questions'][:2],['q33','q34'])
        self.assertEqual(Counter(QUESTIONS[id]['difficulty'] for id in lesson['questions']),Counter(Easy=2,Medium=2,Hard=2))
        self.assertEqual(lesson['coding'],['c_l16_easy','c11','c_l16_hard'])
        for id in lesson['questions']:
            self.assertGreaterEqual(len(QUESTIONS[id]['rubric']),3)
            self.assertNotIn('State the assumptions and the object you are computing.',QUESTIONS[id]['rubric'])

    def test_accuracy_economics_and_passive_selection(self):
        payoff=[F(1)-F(1,5)]*900+[-F(12)-F(1,5)]*100
        self.assertEqual(sum(payoff)/1000,F(-1,2));self.assertEqual(QUESTIONS['q_l16_e1']['answer'],-.5)
        self.assertTrue(13*938-12200<0<13*939-12200)
        self.assertEqual((F(12)+F(1,5))/13,F(61,65))
        strategy=[-2]*60+[0]*40;bid_changes=[-2]*60+[6]*40
        self.assertEqual(F(sum(strategy),100),F(-6,5))
        self.assertEqual(F(sum(bid_changes),100),F(6,5))
        self.assertEqual(QUESTIONS['q_l16_e2']['answer'],-6/5)
        fees=[F(-31,10)]*60+[F(-1,10)]*40
        self.assertEqual(sum(fees)/100,F(-19,10))

    def test_mixture_and_paired_information(self):
        conditional=[(F(96,100),F(99,100)),(F(70,100),F(60,100))]
        for w,expected in ((F(1,2),(F(83,100),F(159,200))),(F(9,10),(F(467,500),F(951,1000)))):
            self.assertEqual(tuple(w*conditional[0][i]+(1-w)*conditional[1][i] for i in range(2)),expected)
        w=F(10,13);self.assertEqual(-F(3,100)*w+F(1,10)*(1-w),0)
        # Same marginal correctness with different paired disagreement counts.
        self.assertEqual(reference('c_l16_easy')([0,1],[0,0],[0,0]),[1,1,0,0])
        self.assertEqual(reference('c_l16_easy')([0,1],[0,0],[1,1]),[1,1,1,1])

    def test_ips_four_outcomes_and_clipping(self):
        probabilities=[F(1,8),F(3,8),F(3,8),F(1,8)]
        scores=[F(12),F(0),F(-4,3),F(0)]
        mean=sum(p*z for p,z in zip(probabilities,scores))
        second=sum(p*z*z for p,z in zip(probabilities,scores))
        self.assertEqual(mean,1);self.assertEqual(second,F(56,3));self.assertEqual(second-mean*mean,F(53,3))
        traded_mass=probabilities[0]+probabilities[2]
        self.assertEqual((probabilities[0]*3-probabilities[2])/traded_mass,0)
        clipped=[F(6),0,F(-4,3),0]
        self.assertEqual(sum(p*z for p,z in zip(probabilities,clipped)),F(1,4))

    def test_ips_conditional_randomization_finite_oracle(self):
        for e1,e2 in itertools.product((F(1,5),F(1,2),F(1)),repeat=2):
            for pi in itertools.product((0,1),repeat=2):
                mean=second=F(0);target=F(0)
                for x,(e,action) in enumerate(zip((e1,e2),pi)):
                    for y,py in ((-3,F(1,3)),(x+2,F(2,3))):
                        target+=F(1,2)*py*action*y
                        for taken,pa in ((0,1-e),(1,e)):
                            z=taken*action*y/e
                            mean+=F(1,2)*py*pa*z;second+=F(1,2)*py*pa*z*z
                formula=sum(F(1,2)*action*(F(1,3)*9+F(2,3)*(x+2)**2)/e for x,(e,action) in enumerate(zip((e1,e2),pi)))
                self.assertEqual(mean,target);self.assertEqual(second,formula)

    def test_identification_failure_and_sharp_missing_support(self):
        # Marginal e=1/2 is known, but A is chosen using Y rather than randomized.
        worlds=[(F(1,2),-1,0),(F(1,2),1,1)]
        self.assertEqual(sum(p*y for p,y,a in worlds),0)
        self.assertEqual(sum(p*a*y/F(1,2) for p,y,a in worlds),1)
        for b in (1,3,10):
            possible=[(F(y)-1)/2 for y in range(-b,b+1)]
            self.assertEqual(min(possible),F(-b-1,2));self.assertEqual(max(possible),F(b-1,2))

    def test_paired_counting_all_binary_triples_and_maximum(self):
        solve=reference('c_l16_easy')
        for n in range(5):
            for triples in itertools.product(list(itertools.product((0,1),repeat=3)),repeat=n):
                actual=[t[0] for t in triples];model=[t[1] for t in triples];base=[t[2] for t in triples]
                mc={i for i,t in enumerate(triples) if t[0]==t[1]}
                bc={i for i,t in enumerate(triples) if t[0]==t[2]}
                before=copy.deepcopy([actual,model,base]);result=solve(actual,model,base)
                self.assertEqual(result,[len(mc),len(bc),len(mc-bc),len(bc-mc)])
                self.assertEqual(result[0]-result[1],result[2]-result[3])
                self.assertEqual([actual,model,base],before)
        self.assertEqual(solve([0,1]*50000,[0,0]*50000,[1,1]*50000),[50000]*4)

    def test_lagged_turnover_independent_rational_accounting(self):
        solve=reference('c11');rng=random.Random(1601)
        for _ in range(200):
            n=rng.randrange(20);positions=[rng.randrange(-3,4) for _ in range(n)]
            returns=[F(rng.randrange(-10,11),100) for _ in range(n)];cost=F(rng.randrange(5),100)
            # Explicit holding path with two flat prefixes; final decision is unexecuted.
            path=[0,0]+positions[:-1]
            expected=[path[t+1]*r-cost*abs(path[t+1]-path[t]) for t,r in enumerate(returns)]
            args=[positions,[float(x) for x in returns],float(cost)];before=copy.deepcopy(args)
            result=solve(*args)
            for a,b in zip(result[0],expected):self.assertAlmostEqual(a,float(b),places=12)
            self.assertAlmostEqual(result[1],float(sum(expected)),places=12);self.assertEqual(args,before)
        result=solve([1,-1,0],[0,.1,.2],.01)
        for actual,expected in zip(result[0],[0,.09,-.22]):self.assertAlmostEqual(actual,expected,places=12)
        self.assertAlmostEqual(result[1],-.13,places=12)

    def test_robust_mix_continuous_linear_program(self):
        solve=reference('c_l16_hard');rng=random.Random(1602)
        cases=[([0,1],[-5,3],[1,3]),([1,1,8],[10,5,0],[1,5]),([1,1,1],[2,2,2],[1,2]),([1,1,2],[4,-3,1],[1,4])]
        for _ in range(20):
            n=rng.randrange(1,4);counts=[rng.randrange(4) for _ in range(n)]
            if not sum(counts):counts[0]=1
            gains=[rng.randrange(-5,6) for _ in range(n)];b=rng.randrange(1,6);a=rng.randrange(b+1)
            cases.append((counts,gains,[a,b]))
        for counts,gains,budget in cases:
            args=copy.deepcopy([counts,gains,budget])
            self.assertEqual(solve(*args),continuous_lp(counts,gains,budget))
            self.assertEqual(args,[counts,gains,budget])

    def test_robust_mix_all_small_probability_vectors(self):
        solve=reference('c_l16_hard');rng=random.Random(1603)
        for _ in range(150):
            n=rng.randrange(1,5);counts=[rng.randrange(3) for _ in range(n)]
            if not sum(counts):counts[0]=1
            gains=[rng.randrange(-4,5) for _ in range(n)];b=rng.randrange(1,4);a=rng.randrange(b+1)
            self.assertEqual(solve(counts,gains,[a,b]),grid_oracle(counts,gains,[a,b]))
        # The range-times-budget shortcut is unattainable here: best loss is only 1.
        result=solve([1,9],[10,0],[2,5])
        self.assertEqual(result,{'worst_mean':['0','1'],'used_tv':['1','10']})

    def test_robust_mix_maximum_bounds_permutations_and_exactness(self):
        solve=reference('c_l16_hard')
        counts=[1]*20000;gains=[i%2 for i in range(20000)]
        self.assertEqual(solve(counts,gains,[1,4]),{'worst_mean':['1','4'],'used_tv':['1','4']})
        self.assertEqual(solve([2,0,3],[-7,-7,2],[1,1]),{'worst_mean':['-7','1'],'used_tv':['3','5']})
        args=[[2,0,3,1],[5,-9,2,5],[2,7]];expected=solve(*args)
        for order in itertools.permutations(range(4)):
            self.assertEqual(solve([args[0][i] for i in order],[args[1][i] for i in order],args[2]),expected)
        self.assertEqual(solve(args[0],args[1],[4,14]),expected)
        self.assertEqual(solve([0,10**9],[ -10**9,10**9],[1,10**9]),{'worst_mean':['999999998','1'],'used_tv':['1','1000000000']})

    def test_actual_judge_official_oracles_and_debug_roundtrip(self):
        for id in ('c_l16_easy','c11','c_l16_hard'):
            task=next(t for t in TASKS if t['id']==id);result=run(id,task['solution'])
            self.assertNotIn('error',result,(id,result));self.assertEqual(result['passed'],result['total'],(id,result))
            cases=task['samples']+task['tests'];copies=submission_cases(id)['cases']
            for original,copied in zip(cases,copies):
                args=copy.deepcopy(original['args']);reference(id)(*args)
                self.assertEqual(args,original['args']);self.assertEqual(parse_debug_cases(task,[copied]),[original])
                if id=='c_l16_hard' and len(args[0])<=3:
                    self.assertEqual(original['expected'],continuous_lp(*args))

if __name__=='__main__':unittest.main()
