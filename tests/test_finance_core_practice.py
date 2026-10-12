"""State-by-state cash ledgers, payoff enumeration and independent finite pricing LPs."""
import copy
import itertools
import math
import random
import unittest
from fractions import Fraction as F

from coding_bank import TASKS
from judge import run,submission_cases,parse_debug_cases
from test_topic_practice import BANK,QUESTIONS,reference

CODES={t['id']:t for t in TASKS}


def canonical(x):return [str(x.numerator),str(x.denominator)]


def greek_oracle(positions,stock,denominator,move,days):
    delta=F(stock);gamma=theta=F(0);value=F(stock*move)
    for quantity,multiplier,d,g,t in positions:
        amount=quantity*multiplier
        dd,gg,tt=(F(v,denominator) for v in (d,g,t))
        delta+=amount*dd;gamma+=amount*gg;theta+=amount*tt
        # Evaluate each independently constructed local polynomial, then aggregate.
        value+=amount*(dd*move+gg*move*move/2+tt*days)
    return {k:canonical(v) for k,v in zip(('delta','gamma','theta','change'),(delta,gamma,theta,value))}


def payoff_oracle(contracts,stock,cash,prices):
    return [str(stock*s+cash+sum(q*m*(max(s-k,0) if kind=='call' else max(k-s,0))
                                for kind,k,q,m in contracts)) for s in prices]


def solve_system(matrix,target):
    """Exact pivoted elimination; distinct from slope and binary-search code."""
    n=len(target)
    rows=[[F(v) for v in row]+[F(t)] for row,t in zip(matrix,target)]
    for column in range(n):
        pivot=next((i for i in range(column,n) if rows[i][column]),None)
        if pivot is None:return None
        rows[column],rows[pivot]=rows[pivot],rows[column]
        scale=rows[column][column]
        rows[column]=[v/scale for v in rows[column]]
        for i in range(n):
            if i==column:continue
            scale=rows[i][column]
            rows[i]=[a-scale*b for a,b in zip(rows[i],rows[column])]
    return [row[-1] for row in rows]


def pricing_vertices(max_price,spot_num,denominator,strikes,prices,queries):
    # All payoff constraints/objectives are affine between these knots.
    # Compressing any continuous-support law to endpoints of those cells preserves them.
    states=sorted({0,max_price,*strikes,*queries})
    columns=[[1,s]+[max(s-k,0) for k in strikes] for s in states]
    target=[F(1),F(spot_num,denominator)]+[F(p,denominator) for p in prices]
    rank=len(target);vertices=[]
    for support in itertools.combinations(range(len(states)),rank):
        matrix=[[columns[j][i] for j in support] for i in range(rank)]
        masses=solve_system(matrix,target)
        if masses is None or any(p<0 for p in masses):continue
        vertices.append([(states[j],p) for j,p in zip(support,masses)])
    return vertices


def price_oracle(max_price,spot_num,denominator,strikes,prices,queries):
    vertices=pricing_vertices(max_price,spot_num,denominator,strikes,prices,queries)
    if not vertices:return {'feasible':False,'bounds':None}
    answer=[]
    for k in queries:
        values=[sum(p*max(s-k,0) for s,p in vertex) for vertex in vertices]
        answer.append([canonical(min(values)),canonical(max(values))])
    return {'feasible':True,'bounds':answer}


def compositions(total,length):
    if length==1:yield (total,)
    else:
        for first in range(total+1):
            for rest in compositions(total-first,length-1):yield (first,)+rest


def cash_ledger(prices,times,a,b,cost=F(0)):
    mark=lambda s,t:a*s*s-b*t
    delta=2*a*prices[0]
    cash=delta*prices[0]-mark(prices[0],times[0])-cost*abs(delta)*prices[0]
    for s in prices[1:-1]:
        new_delta=2*a*s
        cash+=(new_delta-delta)*s-cost*abs(new_delta-delta)*s
        delta=new_delta
    return cash+mark(prices[-1],times[-1])-delta*prices[-1]-cost*abs(delta)*prices[-1]


class FinanceCorePracticeTests(unittest.TestCase):
    def test_coverage_and_preserved_original_assessments(self):
        lesson=next(l for l in BANK['lessons'] if l['id']=='l23')
        levels=[QUESTIONS[id]['difficulty'] for id in lesson['questions']]
        self.assertEqual([levels.count(level) for level in ('Easy','Medium','Hard')],[2,3,2])
        self.assertEqual(lesson['coding'],['c_l23_easy','c_l23_medium','c_l23_hard'])
        self.assertEqual((QUESTIONS['q39']['answer'],QUESTIONS['q40']['answer']),(1,0))
        self.assertEqual((QUESTIONS['q39']['type'],QUESTIONS['q40']['type']),('numeric','numeric'))
        for id in lesson['questions']:
            self.assertGreaterEqual(len(QUESTIONS[id]['rubric']),3)
            self.assertTrue(QUESTIONS[id]['followSolution'])

    def test_contract_quantities_and_dividend_cashflows(self):
        self.assertEqual(QUESTIONS['q_l23_e1']['answer'],40)
        for s in range(301):
            book=2*max(s-100,0)-max(100-s,0)
            self.assertEqual(book,s-100+max(s-100,0))
            self.assertEqual(book,s-100 if s<100 else 2*(s-100))
        self.assertEqual(2*max(90-100,0)-max(100-90,0),-10)
        self.assertEqual(QUESTIONS['q_l23_e2']['answer'],14-108+3+95)
        self.assertEqual(108-3-95,10)
        # Earlier dividend cash is cancelled by its matched-date financing liability.
        for dividend in (F(3),F(21,5)):
            self.assertEqual(dividend-dividend,0)
            for s in (0,80,100,150):
                self.assertEqual(s-100,max(s-100,0)-max(100-s,0))

    def test_bid_ask_roundtrips_use_executable_cashflows(self):
        first=5-8-101+100;second=-8+5+97-100
        self.assertEqual((first,second),(-4,-6))
        self.assertEqual((-8+12+97-100,5-13-101+100),(1,-9))
        for s in range(251):
            c,p=max(s-100,0),max(100-s,0)
            self.assertEqual(-c+p+s-100,0)
            self.assertEqual(c-p-s+100,0)
        self.assertEqual(F(5+8,2)-F(5+8,2)-(F(97+101,2)-100),1)

    def test_incomplete_market_price_interval_and_digital_replication(self):
        states=[0,100,200];call=[0,0,100]
        # Matching first two rows of the stock/cash system already contradicts the third.
        self.assertEqual(solve_system([[0,1],[100,1]],[0,0]),[0,0])
        self.assertNotEqual(0*states[2]+0,call[2])
        for c in (F(1,10),F(7),F(25),F(499,10)):
            z=c/100;q=[z,1-2*z,z]
            self.assertTrue(all(w>0 for w in q))
            self.assertEqual(sum(q),1)
            self.assertEqual(sum(w*s for w,s in zip(q,states)),100)
            self.assertEqual(sum(w*v for w,v in zip(q,call)),c)
        self.assertEqual([F(s,2)-v for s,v in zip(states,call)],[0,50,0])
        for d in (F(1,10),F(1,2),F(9,10)):
            q=[(1-d)/2,d,(1-d)/2]
            self.assertTrue(all(p>0 for p in q))
            self.assertEqual(sum(q[i]*call[i] for i in range(3)),50*(1-d))
            for i,s in enumerate(states):
                self.assertEqual(F(s,2)-50*(i==1),call[i])
        # The endpoint digital/cash-minus-digital trades pay somewhere positive.
        self.assertEqual([int(s==100) for s in states],[0,1,0])
        self.assertEqual([1-int(s==100) for s in states],[1,0,1])

    def test_self_financing_quadratic_ledger_costs_and_refinement(self):
        a,b=F(1,50),F(3);times=[0,F(1,2),1]
        self.assertEqual(cash_ledger([100,110,100],times,a,b),1)
        self.assertEqual(cash_ledger([100,100,100],times,a,b),-3)
        self.assertEqual(cash_ledger([100,110,100],times,a,b,F(1,1000)),F(29,250))
        self.assertEqual(cash_ledger([100,100,100],times,a,b,F(1,1000)),-F(19,5))
        rng=random.Random(2301)
        for _ in range(150):
            n=rng.randint(1,6);prices=[F(rng.randint(0,10)) for _ in range(n+1)]
            times=[F(rng.randint(0,2))]
            for _ in range(n):times.append(times[-1]+F(rng.randint(1,4),2))
            a,b=F(rng.randint(1,5),7),F(rng.randint(1,7),3)
            expected=a*sum((y-x)**2 for x,y in zip(prices,prices[1:]))-b*(times[-1]-times[0])
            self.assertEqual(cash_ledger(prices,times,a,b),expected)
            deltas=[2*a*s for s in prices[:-1]]
            turnover=abs(deltas[0])*prices[0]+abs(deltas[-1])*prices[-1]
            turnover+=sum(abs(deltas[i]-deltas[i-1])*prices[i] for i in range(1,n))
            self.assertEqual(cash_ledger(prices,times,a,b,F(1,1000)),expected-turnover/1000)
        self.assertLess(10**2+10**2,20**2)
        self.assertGreater(10**2+(-10)**2,0**2)
        for x,y in ((3,5),(3,-5)):
            self.assertEqual(x*x+y*y-(x+y)**2,-2*x*y)

    def test_easy_independent_rational_local_surfaces_and_signs(self):
        solve=reference('c_l23_easy');rng=random.Random(2302)
        for _ in range(350):
            rows=[[rng.randint(-5,5),rng.randint(1,5),rng.randint(-5,5),rng.randint(-5,5),rng.randint(-5,5)]
                  for _ in range(rng.randint(0,10))]
            args=[rows,rng.randint(-5,5),rng.randint(1,9),rng.randint(-7,7),rng.randint(0,7)]
            self.assertEqual(solve(*args),greek_oracle(*args))

    def test_medium_against_all_contracts_and_exact_matching(self):
        solve=reference('c_l23_medium');rng=random.Random(2303)
        for _ in range(450):
            rows=[[rng.choice(('call','put')),rng.randint(0,12),rng.randint(-5,5),rng.randint(1,4)]
                  for _ in range(rng.randint(0,12))]
            args=[rows,rng.randint(-3,3),rng.randint(-5,5),[rng.randint(0,15) for _ in range(rng.randint(0,15))]]
            self.assertEqual(solve(*args),payoff_oracle(*args))
        for k in range(11):
            for q in (-3,-1,0,2):
                for multiplier in (1,4):
                    rows=[['call',k,q,multiplier],['put',k,-q,multiplier]]
                    args=[rows,-q*multiplier,k*q*multiplier,list(range(15))]
                    self.assertEqual(solve(*args),['0']*15)

    def test_hard_bounds_against_vertex_enumeration(self):
        solve=reference('c_l23_hard');rng=random.Random(2304)
        for _ in range(100):
            m=rng.randint(2,7)
            counts=[rng.randint(0,4) for _ in range(m+1)]
            if not sum(counts):counts[0]=1
            denominator=sum(counts);spot=sum(i*w for i,w in enumerate(counts))
            strikes=sorted(rng.sample(range(1,m),rng.randint(0,min(3,m-1))))
            quotes=[sum(w*max(i-k,0) for i,w in enumerate(counts)) for k in strikes]
            queries=list(range(m+1));rng.shuffle(queries)
            args=[m,spot,denominator,strikes,quotes,queries]
            self.assertEqual(solve(*args),price_oracle(*args))
        big=CODES['c_l23_hard']['samples'][2]
        self.assertEqual(solve(*big['args']),price_oracle(*big['args']))

    def test_hard_feasibility_against_all_small_probability_tables(self):
        solve=reference('c_l23_hard')
        feasible=set()
        for counts in compositions(2,4):
            feasible.add((sum(i*w for i,w in enumerate(counts)),
                          sum(w*max(i-1,0) for i,w in enumerate(counts)),
                          sum(w*max(i-2,0) for i,w in enumerate(counts))))
        for spot,c1,c2 in itertools.product(range(7),repeat=3):
            result=solve(3,spot,2,[1,2],[c1,c2],[1])
            self.assertEqual(result['feasible'],(spot,c1,c2) in feasible)
            if result['feasible']:self.assertEqual(result['bounds'],[[canonical(F(c1,2)),canonical(F(c1,2))]])
            else:self.assertIsNone(result['bounds'])

    def test_all_fixtures_limits_mutation_and_canonical_outputs(self):
        for suffix in ('easy','medium','hard'):
            task=CODES['c_l23_'+suffix];solve=reference(task['id'])
            for case in task['samples']+task['tests']:
                args=copy.deepcopy(case['args']);before=copy.deepcopy(args)
                result=solve(*args);self.assertEqual(result,case['expected'],task['id'])
                self.assertEqual(args,before,task['id'])
                if suffix=='easy':
                    self.assertEqual(result,greek_oracle(*args))
                    pairs=list(result.values())
                elif suffix=='medium':
                    if len(args[0])*len(args[3])<100000:self.assertEqual(result,payoff_oracle(*args))
                    self.assertTrue(all(str(int(v))==v for v in result))
                    pairs=[]
                else:
                    if len(args[3])<=3 and len(args[5])<=8:self.assertEqual(result,price_oracle(*args))
                    pairs=[p for bound in result['bounds'] for p in bound] if result['feasible'] else []
                for num,den in pairs:
                    self.assertEqual([str(int(num)),str(int(den))],[num,den])
                    self.assertGreater(int(den),0)
                    self.assertEqual(math.gcd(abs(int(num)),int(den)),1)
            for copied in submission_cases(task['id'])['cases']:
                self.assertLessEqual(len(copied['argumentsJSON'])+len(copied['expectedJSON']),500000)
                parsed=parse_debug_cases(task,[copied])
                self.assertEqual(solve(*parsed[0]['args']),parsed[0]['expected'])

    def test_actual_complete_judge_and_lossless_public_debug_copies(self):
        for suffix in ('easy','medium','hard'):
            id='c_l23_'+suffix;task=CODES[id]
            checked=run(id,task['solution'])
            self.assertNotIn('error',checked,id);self.assertEqual(checked['passed'],checked['total'],id)
            cases=submission_cases(id)['cases'][:3]
            copied=[{k:c[k] for k in ('argumentsJSON','expectedJSON')} for c in cases+[cases[2]]]
            checked=run(id,task['solution'],mode='debug',debug_cases=copied)
            self.assertNotIn('error',checked,id)
            self.assertEqual((checked['passed'],checked['total']),(4,4))


if __name__=='__main__':unittest.main()
