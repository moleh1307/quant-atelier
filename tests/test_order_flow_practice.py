"""Branch ledgers and explicit non-clairvoyant policy enumeration for order flow."""
import copy
import itertools
import json
import math
import random
import unittest
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache

from coding_bank import TASKS
from judge import run,submission_cases,parse_debug_cases
from test_topic_practice import BANK,QUESTIONS,reference

CODES={t['id']:t for t in TASKS}


def canonical(value):return [str(value.numerator),str(value.denominator)]


def fill_oracle(low,high,weights,counts,D,ask,fee):
    prior=[F(w,sum(weights)) for w in weights]
    joint=[p*F(c,D) for p,c in zip(prior,counts)]
    probability=sum(joint)
    opportunity=sum(p*(ask-fee-v) for p,v in zip(joint,(low,high)))
    return {'fill_probability':canonical(probability),
            'conditional_value':canonical(sum(p*v for p,v in zip(joint,(low,high)))/probability) if probability else None,
            'per_fill':canonical(opportunity/probability) if probability else None,
            'per_opportunity':canonical(opportunity)}


def quote_oracle(low,high,weights,quotes,D,fee):
    choices=[(F(0),-1)]
    for i,(ask,a,b) in enumerate(quotes):
        probability=[F(w,sum(weights))*F(c,D) for w,c in zip(weights,(a,b))]
        choices.append((sum(p*(ask-fee-v) for p,v in zip(probability,(low,high))),i))
    value,index=min(choices,key=lambda pair:(-pair[0],pair[1]))
    return {'index':index,'profit':canonical(value)}


def policies(prior,quotes,q,limit,h):
    """Enumerate complete policies indexed by OBSERVED events, never by hidden V."""
    if h==0:
        yield (-2,())
        return
    for child in policies(prior,quotes,q,limit,h-1):yield (-1,(child,))
    for index,(bid,ask,rows) in enumerate(quotes):
        D=sum(rows[0]);branches=[];feasible=True
        for event,delta in enumerate((-1,1,0)):
            joint=[p*F(row[event],D) for p,row in zip(prior,rows)]
            probability=sum(joint)
            if not probability:
                branches.append([None]);continue
            if not -limit<=q+delta<=limit:
                feasible=False;break
            posterior=[p/probability for p in joint]
            branches.append(list(policies(posterior,quotes,q+delta,limit,h-1)))
        if feasible:
            for children in itertools.product(*branches):yield(index,children)


def state_cashflow(policy,state,low,high,quotes,q,penalty,fee):
    """Evaluate a fixed complete policy IN each physical state, then average outside."""
    action,children=policy
    if action==-2:return F(q*(low,high)[state]-penalty*q*q)
    if action==-1:return state_cashflow(children[0],state,low,high,quotes,q,penalty,fee)
    bid,ask,rows=quotes[action];D=sum(rows[state]);total=F(0)
    for event,delta in enumerate((-1,1,0)):
        if rows[state][event]==0:continue
        cash=ask-fee if event==0 else -bid-fee if event==1 else 0
        total+=F(rows[state][event],D)*(cash+state_cashflow(children[event],state,low,high,quotes,q+delta,penalty,fee))
    return total


def policy_oracle(low,high,weights,quotes,horizon,inventory,limit,penalty,fee):
    prior=[F(w,sum(weights)) for w in weights]
    candidates=[]
    for policy in policies(prior,quotes,inventory,limit,horizon):
        value=sum(p*state_cashflow(policy,state,low,high,quotes,inventory,penalty,fee) for state,p in enumerate(prior) if p)
        action=-1 if horizon==0 else policy[0]
        candidates.append((value,action))
    value,action=min(candidates,key=lambda pair:(-pair[0],pair[1]))
    baseline=inventory*sum(p*v for p,v in zip(prior,(low,high)))-penalty*inventory**2
    return {'gain':canonical(value-baseline),'action':action}


def conditional_oracle(low,high,weights,quotes,horizon,inventory,limit,penalty,fee):
    """Long-horizon check via explicit Fraction posteriors, not scaled integer N_t."""
    @lru_cache(None)
    def value(p,q,h):
        if h==0:return q*((1-p)*low+p*high)-penalty*q*q,-1
        choices=[(value(p,q,h-1)[0],-1)]
        for index,(bid,ask,rows) in enumerate(quotes):
            D=sum(rows[0]);total=F(0);feasible=True
            for event,delta in enumerate((-1,1,0)):
                joint_low=(1-p)*F(rows[0][event],D)
                joint_high=p*F(rows[1][event],D)
                probability=joint_low+joint_high
                if not probability:continue
                if not -limit<=q+delta<=limit:feasible=False;break
                posterior=joint_high/probability
                cash=ask-fee if event==0 else -bid-fee if event==1 else 0
                total+=probability*(cash+value(posterior,q+delta,h-1)[0])
            if feasible:choices.append((total,index))
        return min(choices,key=lambda pair:(-pair[0],pair[1]))
    p=F(weights[1],sum(weights))
    score,action=value(p,inventory,horizon)
    baseline=inventory*((1-p)*low+p*high)-penalty*inventory**2
    return {'gain':canonical(score-baseline),'action':action}


class OrderFlowPracticeTests(unittest.TestCase):
    def test_coverage_and_permanent_assessment_meanings(self):
        topic=next(l for l in BANK['lessons'] if l['id']=='l20')
        self.assertEqual(Counter(QUESTIONS[id]['difficulty'] for id in topic['questions']),Counter({'Easy':2,'Medium':2,'Hard':3}))
        self.assertEqual(topic['coding'],['c_l20_easy','c_l20_medium','c_l20_hard'])
        self.assertEqual(QUESTIONS['q36']['answer'],float(F(200,3)))
        self.assertEqual((QUESTIONS['q36']['type'],QUESTIONS['q36']['difficulty']),('numeric','Hard'))
        self.assertEqual((QUESTIONS['q42']['type'],QUESTIONS['q42']['answer']),('structured',None))
        self.assertEqual(QUESTIONS['q_l20_e1']['answer'],float(F(-6,5)))
        self.assertEqual(QUESTIONS['q_l20_e2']['answer'],1)
        self.assertEqual(3*(1**2-2**2),-9);self.assertEqual(3*(3**2-2**2),15)

    def test_buy_no_buy_history_and_next_selection(self):
        high=F(1,2);low=F(1,2)
        for event in ('buy','none','buy'):
            high*=F(3,4) if event=='buy' else F(1,4)
            low*=F(1,4) if event=='buy' else F(3,4)
        p=high/(high+low)
        self.assertEqual(p,F(3,4));self.assertEqual(p*100,75)
        fill=p*F(3,4)+(1-p)*F(1,4)
        selected=p*F(3,4)/fill
        self.assertEqual((fill,selected*100),(F(5,8),90))
        self.assertEqual(fill*(80-selected*100),F(-25,4))
        for buys in range(5):
            for absent in range(5):
                a=F(3,4)**buys*F(1,4)**absent
                b=F(1,4)**buys*F(3,4)**absent
                self.assertEqual(a/b,F(3)**(buys-absent))

    def test_price_dependent_four_branch_ledger(self):
        records=list(itertools.product((0,100),('informed','uninformed')))
        means=[];profits=[];probabilities=[]
        for ask in (55,60,70,100):
            selected=[v for v,type in records if (v>ask if type=='informed' else ask<=60)]
            probability=F(len(selected),4)
            probabilities.append(probability)
            means.append(F(sum(selected),len(selected)) if selected else None)
            profits.append(sum((F(ask-1-v,4) for v in selected),F(0)))
        self.assertEqual(probabilities,[F(3,4),F(3,4),F(1,4),0])
        self.assertEqual(means,[F(200,3),F(200,3),100,None])
        self.assertEqual(profits,[F(-19,2),F(-23,4),F(-31,4),0])
        cutoff=F(18,59)
        self.assertEqual(59*(1-cutoff/2)-50,0)
        self.assertEqual(59*(1-F(1,2)/2)-50,F(-23,4))

    def test_two_opportunity_information_witness(self):
        task=CODES['c_l20_hard'];args=task['samples'][0]['args']
        self.assertEqual(policy_oracle(*args),{'gain':['5','1'],'action':0})
        self.assertEqual(conditional_oracle(*args),task['samples'][0]['expected'])
        once=copy.deepcopy(args);once[4]=1
        self.assertEqual(policy_oracle(*once),{'gain':['4','1'],'action':1})
        # The fixed A policy is allowed to adapt to buy/no-order, not to latent V.
        # High: sell12 then buy2 -> cash10/inventory0. Low: no order, then skip.
        # Complete two-opportunity observed policy, with B following A's high buy.
        policy=(0,((1,(None,(-2,()),None)),None,(-1,((-2,()),))))
        self.assertEqual(state_cashflow(policy,1,*args[:2],args[3],0,0,0),10)
        self.assertEqual(state_cashflow(policy,0,*args[:2],args[3],0,0,0),0)

    def test_easy_independent_branches_mutation_and_random_cases(self):
        fn=reference('c_l20_easy');task=CODES['c_l20_easy']
        for case in task['samples']+task['tests']:
            args=copy.deepcopy(case['args']);before=copy.deepcopy(args)
            expected=fill_oracle(*args)
            self.assertEqual(case['expected'],expected);self.assertEqual(fn(*args),expected);self.assertEqual(args,before)
        rng=random.Random(2020)
        for _ in range(400):
            low=rng.randrange(-10**9,10**9);high=rng.randrange(low,10**9+1)
            weights=[rng.randrange(10**9+1) for _ in range(2)]
            if not sum(weights):weights[0]=1
            D=rng.randrange(1,10**9+1);counts=[rng.randrange(D+1) for _ in range(2)]
            args=[low,high,weights,counts,D,rng.randrange(-10**9,10**9+1),rng.randrange(10**9+1)]
            out=fn(*args);self.assertEqual(out,fill_oracle(*args))
            if out['per_fill'] is not None:
                self.assertEqual(F(*map(int,out['fill_probability']))*F(*map(int,out['per_fill'])),F(*map(int,out['per_opportunity'])))

    def test_medium_independent_action_enumeration_and_ties(self):
        fn=reference('c_l20_medium');task=CODES['c_l20_medium']
        for case in task['samples']+task['tests']:
            args=copy.deepcopy(case['args']);before=copy.deepcopy(args)
            expected=quote_oracle(*args)
            self.assertEqual(case['expected'],expected);self.assertEqual(fn(*args),expected);self.assertEqual(args,before)
        rng=random.Random(2021)
        for _ in range(300):
            low=rng.randrange(-20,21);high=rng.randrange(low,31)
            weights=[rng.randrange(6),rng.randrange(6)]
            if not sum(weights):weights[0]=1
            D=rng.randrange(1,11)
            quotes=[[rng.randrange(-10,41),rng.randrange(D+1),rng.randrange(D+1)] for _ in range(rng.randrange(15))]
            args=[low,high,weights,quotes,D,rng.randrange(4)]
            self.assertEqual(fn(*args),quote_oracle(*args))
        self.assertEqual(fn(0,0,[1,1],[[1,1,1]]*100000,1,0),{'index':0,'profit':['1','1']})

    def test_hard_fixtures_complete_policy_enumeration(self):
        fn=reference('c_l20_hard');task=CODES['c_l20_hard']
        for case in task['samples']+task['tests']:
            args=copy.deepcopy(case['args']);before=copy.deepcopy(args)
            expected=policy_oracle(*args) if args[4]<=2 or len(args[3])<=1 or args[6]==0 else conditional_oracle(*args)
            self.assertEqual(case['expected'],expected);self.assertEqual(fn(*args),expected);self.assertEqual(args,before)

    def test_hard_random_complete_observation_policies(self):
        fn=reference('c_l20_hard');rng=random.Random(2022)
        rows=list(itertools.product(range(3),repeat=3));rows=[list(r) for r in rows if sum(r)==2]
        for _ in range(70):
            low=rng.randrange(-4,5);high=rng.randrange(low+1,10)
            weights=[rng.randrange(4),rng.randrange(4)]
            if not sum(weights):weights[0]=1
            quotes=[]
            for j in range(rng.randrange(1,3)):
                bid=rng.randrange(-5,8);ask=bid+rng.randrange(5)
                quotes.append([bid,ask,[rng.choice(rows).copy(),rng.choice(rows).copy()]])
            limit=rng.randrange(1,3);inventory=rng.randrange(-limit,limit+1)
            args=[low,high,weights,quotes,2,inventory,limit,rng.randrange(3),rng.randrange(2)]
            expected=policy_oracle(*args)
            self.assertEqual(fn(*args),expected);self.assertEqual(conditional_oracle(*args),expected)
            # Scaling all prior weights must not alter a policy or its gain.
            scaled=copy.deepcopy(args);scaled[2]=[w*17 for w in weights]
            self.assertEqual(fn(*scaled),expected)
            # Rescale all likelihood rows equally: probabilities must stay identical.
            for quote in scaled[3]:quote[2]=[[v*5 for v in row] for row in quote[2]]
            self.assertEqual(fn(*scaled),expected)
            self.assertGreaterEqual(F(*map(int,expected['gain'])),0)

    def test_hard_maximum_horizon_and_belief_scaling(self):
        fn=reference('c_l20_hard')
        quotes=[[4,9,[[2,4,5],[6,3,2]]],[3,11,[[1,5,5],[7,2,2]]],[2,10,[[3,2,6],[5,4,2]]]]
        args=[-3,13,[37,61],quotes,5,-1,4,2,1]
        expected=conditional_oracle(*args)
        self.assertEqual(fn(*args),expected)
        # Three uninformed event types/three menus at full horizon; marked inventory
        # has zero expected contribution, quote0 earns four each opportunity.
        uninformative=[[0,12,[[1,1,1],[1,1,1]]],[1,11,[[1,1,1],[1,1,1]]],[2,10,[[1,1,1],[1,1,1]]]]
        self.assertEqual(fn(0,12,[1,1],uninformative,5,0,5,0,0),{'gain':['20','1'],'action':0})

    def test_lossless_public_cases_and_canonical_rationals(self):
        large=False
        for id in ('c_l20_easy','c_l20_medium','c_l20_hard'):
            for case in submission_cases(id)['cases']:
                copied={k:case[k] for k in ('argumentsJSON','expectedJSON')}
                parsed=parse_debug_cases(CODES[id],[copied])[0]
                self.assertEqual(parsed['expected'],json.loads(copied['expectedJSON']))
                self.assertLessEqual(sum(len(v) for v in copied.values()),500000)
                for key,value in parsed['expected'].items():
                    if value is None or isinstance(value,int):continue
                    self.assertTrue(all(isinstance(part,str) for part in value))
                    numerator,denominator=map(int,value)
                    self.assertGreater(denominator,0);self.assertEqual(math.gcd(abs(numerator),denominator),1)
                    self.assertEqual([str(numerator),str(denominator)],value)
                    large|=abs(numerator)>2**53 or denominator>2**53
        self.assertTrue(large)

    def test_complete_judge_and_public_large_fraction_debug(self):
        for id in ('c_l20_easy','c_l20_medium','c_l20_hard'):
            out=run(id,CODES[id]['solution'])
            self.assertFalse(out.get('error'),out.get('error'));self.assertEqual(out['passed'],out['total'])
        id='c_l20_hard';case=submission_cases(id)['cases'][1]
        copied={k:case[k] for k in ('argumentsJSON','expectedJSON')}
        self.assertIn('999999999000000000',copied['expectedJSON'])
        out=run(id,CODES[id]['solution'],mode='debug',debug_cases=[copied])
        self.assertFalse(out.get('error'),out.get('error'));self.assertEqual(out['passed'],out['total'])


if __name__=='__main__':unittest.main()
