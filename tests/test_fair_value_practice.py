"""Independent finite probability models and bounded-weight composition oracles."""
import copy
import itertools
import json
import math
import random
import unittest
from collections import Counter
from fractions import Fraction as F

from coding_bank import TASKS
from judge import run, submission_cases, parse_debug_cases
from test_topic_practice import BANK, QUESTIONS, reference

CODES = {t['id']: t for t in TASKS}


def canonical(q):
    return [str(q.numerator), str(q.denominator)]


def edges(mean, bid, ask, buy_cost, sell_cost):
    buy = mean - ask - buy_cost
    sell = bid - mean - sell_cost
    return {'value': canonical(mean), 'buy_edge': canonical(buy),
            'sell_edge': canonical(sell),
            'action': 'buy' if buy > 0 else 'sell' if sell > 0 else 'wait'}


def weighted_oracle(payoffs, weights, bid, ask, buy_cost, sell_cost):
    # Form a probability for every state first; this is not integer reference code.
    total = sum(weights)
    mean = sum((F(w, total) * v for v, w in zip(payoffs, weights)), F(0))
    return edges(mean, bid, ask, buy_cost, sell_cost)


def signal_oracle(payoffs, weights, likelihoods, bid, ask, buy_cost, sell_cost):
    k = len(likelihoods[0])
    total = sum(weights)
    d = sum(likelihoods[0])
    # Explicit joint probability records, then condition separately for each signal.
    records = [(j, v, F(w, total)*F(row[j], d))
               for v, w, row in zip(payoffs, weights, likelihoods) for j in range(k)]
    output = []
    for j in range(k):
        selected = [(v, p) for s, v, p in records if s == j]
        probability = sum((p for v, p in selected), F(0))
        if probability:
            mean = sum((v*p/probability for v, p in selected), F(0))
            item = edges(mean, bid, ask, buy_cost, sell_cost)
        else:
            item = {'value': None, 'buy_edge': None, 'sell_edge': None, 'action': 'unreachable'}
        item['probability'] = canonical(probability)
        output.append(item)
    return output


def composition_values(payoffs, likelihoods, lower, upper, mass):
    # ALL integer compositions, including interior points; no vertex shortcut.
    values = []
    for weights in itertools.product(*(range(lo, hi+1) for lo, hi in zip(lower, upper))):
        if sum(weights) != mass:
            continue
        joint = [F(w, mass)*F(l, 10**9) for w, l in zip(weights, likelihoods)]
        normaliser = sum(joint)
        values.append(sum(v*p/normaliser for v, p in zip(payoffs, joint)))
    return values


def robust_oracle(payoffs, likelihoods, lower, upper, mass, bid, ask, buy_cost, sell_cost):
    values = composition_values(payoffs, likelihoods, lower, upper, mass)
    low, high = min(values), max(values)
    buy, sell = low-ask-buy_cost, bid-high-sell_cost
    return {'minimum': canonical(low), 'maximum': canonical(high),
            'buy_floor': canonical(buy), 'sell_floor': canonical(sell),
            'action': 'buy' if buy > 0 else 'sell' if sell > 0 else 'wait'}


class FairValuePracticeTests(unittest.TestCase):
    def test_coverage_and_preserved_numeric_assessment(self):
        topic = next(l for l in BANK['lessons'] if l['id'] == 'l19')
        self.assertEqual(Counter(QUESTIONS[q]['difficulty'] for q in topic['questions']),
                         Counter({'Easy': 2, 'Medium': 2, 'Hard': 2}))
        self.assertEqual(topic['coding'], ['c_l19_easy','c_l19_medium','c_l19_hard'])
        self.assertEqual(QUESTIONS['q35']['answer'], 10.5)
        self.assertEqual(QUESTIONS['q35']['type'], 'numeric')
        self.assertEqual(QUESTIONS['q35']['tolerance'], 1e-6)
        self.assertEqual(QUESTIONS['q_l19_e2']['answer'], float(F(3, 4)))
        self.assertEqual(F(209,2)-105-F(1,4)-F(1,4), -1)
        self.assertEqual(104-F(1,4)-106, F(-9,4))

    def test_joint_signal_dependence_and_tower(self):
        records = [(0,0,F(2,5)), (0,10,F(1,10)), (10,0,F(1,10)), (10,10,F(2,5))]
        h = [(a,b,p*(F(3,4) if a==10 else F(1,4))) for a,b,p in records]
        self.assertEqual(sum(p for a,b,p in h), F(1,2))
        posterior = [p*2 for a,b,p in h]
        self.assertEqual(posterior, [F(1,5),F(1,20),F(3,20),F(3,5)])
        self.assertEqual(sum(a*p for (a,b,_),p in zip(h,posterior)), F(15,2))
        self.assertEqual(sum(b*p for (a,b,_),p in zip(h,posterior)), F(13,2))
        high_mean = sum((a+b)*p for (a,b,_),p in zip(h,posterior))
        low_records = [(a,b,p-joint) for (a,b,p),(_,_,joint) in zip(records,h)]
        low_mean = sum((a+b)*p*2 for a,b,p in low_records)
        self.assertEqual((high_mean,low_mean),(14,6))
        self.assertEqual((high_mean+low_mean)/2,sum((a+b)*p for a,b,p in records))
        selected = [(a,b,p) for a,b,p in h if b==10]
        self.assertEqual(sum((a+b)*p for a,b,p in selected)/sum(p for a,b,p in selected),F(250,13))

    def test_replication_cash_flows_and_physical_risk(self):
        prices, payments = [2,8], [1,13]
        delta = F(payments[1]-payments[0], prices[1]-prices[0])
        cash = payments[0]-delta*prices[0]
        self.assertEqual((delta,cash,delta*5+cash),(2,-3,7))
        for price, payment in zip(prices,payments):
            self.assertEqual(delta*price+cash,payment)
            # Both arbitrage directions have zero terminal residual.
            self.assertEqual(payment-(delta*price+cash),0)
        self.assertEqual(F(3,4)*13+F(1,4)*1,10)
        q = F(5-2,8-2)
        self.assertEqual(q,F(1,2))
        self.assertEqual((1-q)*1+q*13,7)
        self.assertEqual(1-8,-7)  # positive physical mean edge does not erase low-state loss

    def test_information_policy_and_fixed_action_inequality(self):
        # Enumerate all joint outcomes, checking actions, fees and actual losses.
        joint = [(0,'H',F(1,10)),(10,'H',F(2,5)),(0,'L',F(2,5)),(10,'L',F(1,10))]
        profit = sum(p*(v-F(13,2) if s=='H' else F(7,2)-v) for v,s,p in joint)
        self.assertEqual(profit,F(3,2))
        self.assertEqual(profit-1,F(1,2))
        self.assertEqual(F(10)-F(13,2),F(7,2))
        self.assertEqual(F(0)-F(13,2),F(-13,2))
        rng=random.Random(1919)
        g=lambda m:max(F(0),m-F(13,2),F(7,2)-m)
        for _ in range(300):
            probability=F(rng.randrange(1,10),10)
            x,y=F(rng.randrange(-20,31),2),F(rng.randrange(-20,31),2)
            self.assertGreaterEqual(probability*g(x)+(1-probability)*g(y),g(probability*x+(1-probability)*y))

    def test_ambiguity_and_hierarchical_model_conditioning(self):
        mean=lambda p:36*p/(1+2*p)
        self.assertEqual((mean(F(1,4)),mean(F(3,4))),(6,F(54,5)))
        self.assertEqual(mean(F(1,4))-F(37,4),F(-13,4))
        self.assertEqual(F(31,4)-mean(F(3,4)),F(-61,20))
        for i in range(10):
            self.assertLess(mean(F(10+i,40)),mean(F(11+i,40)))
        common = mean(F(1,2))
        self.assertEqual((common-F(37,4),F(31,4)-common),(F(-1,4),F(-5,4)))
        marginal = (F(3,8)+F(5,8))/2
        weights = [F(1,2)*s/marginal for s in (F(3,8),F(5,8))]
        self.assertEqual(weights,[F(3,8),F(5,8)])
        self.assertEqual(sum(w*m for w,m in zip(weights,(6,F(54,5)))),9)
        self.assertEqual((6+F(54,5))/2,F(42,5))

    def test_easy_all_fixtures_and_random_exact_means(self):
        fn=reference('c_l19_easy')
        task=CODES['c_l19_easy']
        for case in task['samples']+task['tests']:
            args=copy.deepcopy(case['args']); before=copy.deepcopy(args)
            expected=weighted_oracle(*args)
            self.assertEqual(case['expected'],expected)
            self.assertEqual(fn(*args),expected)
            self.assertEqual(args,before)
        rng=random.Random(1920)
        for _ in range(350):
            n=rng.randrange(1,20)
            values=[rng.randrange(-10**9,10**9+1) for _ in range(n)]
            weights=[rng.randrange(10**9+1) for _ in range(n)]
            if not sum(weights):weights[0]=1
            bid=rng.randrange(-30,31);ask=bid+rng.randrange(15)
            args=[values,weights,bid,ask,rng.randrange(4),rng.randrange(4)]
            self.assertEqual(fn(*args),weighted_oracle(*args))
        # Maximum magnitude and length tested without a huge browser-copy fixture.
        self.assertEqual(fn([10**9]*100000,[10**9]*100000,10**9-1,10**9,0,0),
                         edges(F(10**9),10**9-1,10**9,0,0))

    def test_medium_joint_record_oracle_conservation_and_scaling(self):
        fn=reference('c_l19_medium');task=CODES['c_l19_medium']
        for case in task['samples']+task['tests']:
            # Big uniform fixture's joint probabilities are hand-proven 1/50 each;
            # smaller cases use the general explicit record oracle.
            args=copy.deepcopy(case['args']);before=copy.deepcopy(args)
            expected=signal_oracle(*args) if len(args[0])<2000 else [dict(edges(F(7),6,8,0,0),probability=['1','50']) for _ in range(50)]
            self.assertEqual(case['expected'],expected)
            self.assertEqual(fn(*args),expected);self.assertEqual(args,before)
        rng=random.Random(1921)
        for _ in range(180):
            n,k=rng.randrange(1,8),rng.randrange(1,6)
            values=[rng.randrange(-20,21) for _ in range(n)]
            weights=[rng.randrange(5) for _ in range(n)]
            if not sum(weights):weights[0]=1
            rows=[]
            for i in range(n):
                row=[0]*k
                for _ in range(8):row[rng.randrange(k)]+=1
                rows.append(row)
            args=[values,weights,rows,-2,3,1,2]
            out=fn(*args)
            self.assertEqual(out,signal_oracle(*args))
            self.assertEqual(sum(F(*map(int,t['probability'])) for t in out),1)
            self.assertEqual(sum(F(*map(int,t['probability']))*F(*map(int,t['value'])) for t in out if t['value']),
                             F(sum(v*w for v,w in zip(values,weights)),sum(weights)))
            scaled=[values,[w*3 for w in weights],[[l*7 for l in row] for row in rows],-2,3,1,2]
            self.assertEqual(fn(*scaled),out)

    def test_hard_all_fixtures_independent_compositions(self):
        fn=reference('c_l19_hard');task=CODES['c_l19_hard']
        for case in task['samples']+task['tests']:
            args=copy.deepcopy(case['args']);before=copy.deepcopy(args)
            if max(args[3])<=100:
                expected=robust_oracle(*args)
            elif len(args[0])==2:
                # Bounds pin a SINGLE prior, independent direct probability calculation.
                v,l,lo,hi,mass,bid,ask,bc,sc=args
                mean=sum(F(w,mass)*F(lk,10**9)*value for w,lk,value in zip(lo,l,v))/sum(F(w,mass)*F(lk,10**9) for w,lk in zip(lo,l))
                expected={'minimum':canonical(mean),'maximum':canonical(mean),
                          'buy_floor':canonical(mean-ask-bc),'sell_floor':canonical(bid-mean-sc),'action':'wait'}
            else:
                # Equal likelihoods allow any mass on a single state; extrema 1 and12.
                expected={'minimum':['1','1'],'maximum':['12','1'],'buy_floor':['-11','1'],'sell_floor':['-11','1'],'action':'wait'}
            self.assertEqual(case['expected'],expected)
            self.assertEqual(fn(*args),expected);self.assertEqual(args,before)
        wrong_greedy=F(5*1*10,5*100+5*1)
        best=F(5*100*5,5*100+5*100)
        self.assertLess(wrong_greedy,best)
        self.assertEqual((wrong_greedy,best),(F(10,101),F(5,2)))

    def test_hard_random_compositions_permutations_and_real_mixtures(self):
        fn=reference('c_l19_hard');rng=random.Random(1922)
        for _ in range(180):
            n=rng.randrange(1,6)
            values=[rng.randrange(-8,9) for _ in range(n)]
            likelihoods=[rng.randrange(1,9) for _ in range(n)]
            lower=[rng.randrange(3) for _ in range(n)]
            upper=[lo+rng.randrange(4) for lo in lower]
            mass=rng.randrange(max(1,sum(lower)),sum(upper)+1) if sum(upper) else 1
            if not sum(upper):upper[0]=1
            bid=rng.randrange(-5,6);ask=bid+rng.randrange(5)
            args=[values,likelihoods,lower,upper,mass,bid,ask,rng.randrange(3),rng.randrange(3)]
            expected=robust_oracle(*args)
            self.assertEqual(fn(*args),expected)
            order=list(range(n));rng.shuffle(order)
            permuted=[[array[i] for i in order] for array in args[:4]]+args[4:]
            self.assertEqual(fn(*permuted),expected)
            scaled=[values,[l*5 for l in likelihoods],[w*3 for w in lower],[w*3 for w in upper],mass*3]+args[5:]
            self.assertEqual(fn(*scaled),expected)
            feasible=[w for w in itertools.product(*(range(lo,hi+1) for lo,hi in zip(lower,upper))) if sum(w)==mass]
            a,b=rng.choice(feasible),rng.choice(feasible)
            alpha=F(2,7)
            real_weights=[alpha*x+(1-alpha)*y for x,y in zip(a,b)]
            denominator=sum(w*l for w,l in zip(real_weights,likelihoods))
            ratio=sum(w*l*v for w,l,v in zip(real_weights,likelihoods,values))/denominator
            self.assertGreaterEqual(ratio,F(*map(int,expected['minimum'])))
            self.assertLessEqual(ratio,F(*map(int,expected['maximum'])))

    def test_exact_debug_copy_and_canonical_rationals(self):
        maximum=0;seen_large_integer=False
        for id in ('c_l19_easy','c_l19_medium','c_l19_hard'):
            for case in submission_cases(id)['cases']:
                copied={k:case[k] for k in ('argumentsJSON','expectedJSON')}
                maximum=max(maximum,sum(len(v) for v in copied.values()))
                task=CODES[id]
                parsed=parse_debug_cases(task,[copied])[0]
                expected=json.loads(copied['expectedJSON'])
                self.assertEqual(parsed['expected'],expected)
                items=expected if isinstance(expected,list) else [expected]
                for item in items:
                    for key,value in item.items():
                        if key=='action' or value is None:continue
                        self.assertTrue(all(isinstance(part,str) for part in value))
                        num,den=map(int,value)
                        self.assertGreater(den,0);self.assertEqual(math.gcd(abs(num),den),1)
                        self.assertEqual([str(num),str(den)],value)
                        seen_large_integer|=abs(num)>2**53 or den>2**53
        self.assertTrue(seen_large_integer)
        self.assertLessEqual(maximum,500000)
        self.assertGreater(maximum,400000)

    def test_full_judge_and_copied_large_exact_case(self):
        for id in ('c_l19_easy','c_l19_medium','c_l19_hard'):
            result=run(id,CODES[id]['solution'])
            self.assertFalse(result.get('error'),result.get('error'))
            self.assertEqual(result['passed'],result['total'])
        id='c_l19_medium'
        large=next(c for c in submission_cases(id)['cases'] if '1999999998000000001' in c.get('expectedJSON',''))
        copied={k:large[k] for k in ('argumentsJSON','expectedJSON')}
        result=run(id,CODES[id]['solution'],mode='debug',debug_cases=[copied])
        self.assertFalse(result.get('error'),result.get('error'))
        self.assertEqual(result['passed'],result['total'])


if __name__=='__main__':unittest.main()
