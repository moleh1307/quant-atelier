"""Complete stopping policies, exact fee ledgers and high-precision robust objectives."""
import copy
import itertools
import json
import math
import random
import unittest
from collections import Counter
from decimal import Decimal as D,localcontext
from fractions import Fraction as F

from coding_bank import TASKS
from judge import run,submission_cases,parse_debug_cases
from test_topic_practice import BANK,QUESTIONS,reference

CODES={t['id']:t for t in TASKS}


def canonical(q):return [str(q.numerator),str(q.denominator)]


def one_choice(observed,values,weights,cost):
    mean=sum(F(w,sum(weights))*v for v,w in zip(values,weights))
    if F(observed)>=mean-cost:return {'action':'keep','value':canonical(F(observed))}
    return {'action':'reroll','value':canonical(mean-cost)}


def fixed_policy_value(values,weights,costs,masks):
    """Enumerate paid paths for one complete stop/redraw policy, without a max."""
    probabilities=[F(w,sum(weights)) for w in weights]
    def paths(stage,probability,spent):
        score=F(0)
        for i,(v,p) in enumerate(zip(values,probabilities)):
            joint=probability*p
            if stage==len(costs) or not masks[stage]&(1<<i):score+=joint*(v-spent)
            else:score+=paths(stage+1,joint,spent+costs[stage])
        return score
    return paths(0,F(1),0)


def stopping_oracle(values,weights,costs):
    def optimal(schedule):
        return max(fixed_policy_value(values,weights,schedule,masks)
                   for masks in itertools.product(range(1<<len(values)),repeat=len(schedule)))
    value=optimal(costs)
    threshold=optimal(costs[1:])-costs[0] if costs else None
    return {'value':canonical(value),'threshold':canonical(threshold) if threshold is not None else None}


def decimal_growth(returns,weights,fraction):
    f=D(str(fraction))
    return min(sum(D(w)/D(sum(row))*(1+f*D(r)).ln() for r,w in zip(returns,row) if w) for row in weights)


def robust_derivative_oracle(returns,weights,cap):
    """Use active-curve derivative bisection, independently of ternary search."""
    with localcontext() as ctx:
        ctx.prec=75
        cap=D(str(cap))
        if cap==0 or any(sum(w*r for w,r in zip(row,returns))<=0 for row in weights):return D(0),D(0)
        probabilities=[[D(w)/D(sum(row)) for w in row] for row in weights]
        def scores(f):
            out=[]
            for row in probabilities:
                g=sum(p*(1+f*D(r)).ln() for p,r in zip(row,returns) if p)
                slope=sum(p*D(r)/(1+f*D(r)) for p,r in zip(row,returns) if p)
                out.append((g,slope))
            return out
        low,high=D(0),cap
        for _ in range(135):
            f=(low+high)/2
            pairs=scores(f);minimum=min(v for v,s in pairs)
            active=[s for v,s in pairs if v-minimum<D('1e-35')]
            # Right derivative at an exact crossing is the minimum active slope.
            if min(active)>0:low=f
            else:high=f
        middle=(low+high)/2
        candidates=[(D(0),D(0)),(middle,min(v for v,s in scores(middle))),
                    (cap,min(v for v,s in scores(cap)))]
        return min(candidates,key=lambda pair:(-pair[1],pair[0]))


class ContinuationGrowthPracticeTests(unittest.TestCase):
    def test_coverage_and_permanent_numeric_meanings(self):
        topic=next(l for l in BANK['lessons'] if l['id']=='l21')
        self.assertEqual(Counter(QUESTIONS[q]['difficulty'] for q in topic['questions']),Counter({'Easy':2,'Medium':2,'Hard':3}))
        self.assertEqual(topic['coding'],['c_l21_easy','c_l21_medium','c_l21_hard'])
        self.assertEqual((QUESTIONS['q13']['answer'],QUESTIONS['q13']['type']),(4.25,'numeric'))
        self.assertEqual((QUESTIONS['q37']['answer'],QUESTIONS['q37']['difficulty']),(.2,'Hard'))
        self.assertEqual(QUESTIONS['q_l21_e1']['answer'],4)
        self.assertEqual(QUESTIONS['q_l21_e2']['answer'],93.75)
        self.assertEqual((F(2)+8)/2-F(3,2),F(7,2))

    def test_wealth_paths_and_changed_policy_order(self):
        probabilities={True:F(3,5),False:F(2,5)}
        total=F(0)
        for path in itertools.product((True,False),repeat=2):
            wealth=F(100);probability=F(1)
            for win in path:
                wealth*=1+(F(1,4) if win else F(-1,4));probability*=probabilities[win]
            total+=probability*wealth
            if path[0]!=path[1]:self.assertEqual(wealth,F(375,4))
        self.assertEqual(total,F(441,4))
        self.assertEqual(100*F(5,4)*F(1,2),F(125,2))
        self.assertEqual(100*F(3,4)*1,75)

    def test_ordered_fee_question_by_complete_draw_ledgers(self):
        for costs,threshold,value in [([1,0],F(13,4),F(33,8)),([0,1],F(23,6),F(53,12))]:
            total=F(0)
            last_threshold=F(7,2)-costs[1]
            for x,y,z in itertools.product(range(1,7),repeat=3):
                payment=x if x>=threshold else y-costs[0] if y>=last_threshold else z-sum(costs)
                total+=F(payment,216)
            self.assertEqual(total,value)
        self.assertEqual(stopping_oracle([3],[1],[0])['value'],['3','1'])
        self.assertEqual(stopping_oracle([0,6],[1,1],[0])['value'],['9','2'])

    def test_bayesian_and_adverse_models_are_distinct(self):
        models=[F(11,20),F(13,20)];prior=[F(1,2),F(1,2)]
        predictive=sum(w*p for w,p in zip(prior,models))
        self.assertEqual(predictive,F(3,5));self.assertEqual(2*predictive-1,F(1,5))
        self.assertEqual(2*min(models)-1,F(1,10))
        win=[w*p/predictive for w,p in zip(prior,models)]
        loss=[w*(1-p)/(1-predictive) for w,p in zip(prior,models)]
        self.assertEqual(win,[F(11,24),F(13,24)]);self.assertEqual(loss,[F(9,16),F(7,16)])
        next_win=sum(w*p for w,p in zip(win,models));next_loss=sum(w*p for w,p in zip(loss,models))
        self.assertEqual((next_win,next_loss),(F(29,48),F(19,32)))
        self.assertEqual((2*next_win-1,2*next_loss-1),(F(5,24),F(3,16)))
        self.assertEqual(predictive*next_win+(1-predictive)*next_loss,predictive)
        covariance=sum(w*p*p for w,p in zip(prior,models))-predictive**2
        self.assertEqual(covariance,F(1,400))
        # Continuation depends on the outcome/predictive law, not first fraction.
        g=lambda f,p:float(p)*math.log1p(float(f))+(1-float(p))*math.log1p(-float(f))
        continuation=float(predictive)*g(F(5,24),next_win)+float(1-predictive)*g(F(3,16),next_loss)
        optimum=g(F(1,5),predictive)+continuation
        for i in range(100):self.assertGreaterEqual(optimum+1e-15,g(F(i,100),predictive)+continuation)

    def test_tail_root_algebra_domain_and_robust_endpoint(self):
        with localcontext() as ctx:
            ctx.prec=75
            f=(D(12)-D(69).sqrt())/75
            self.assertTrue(0<f<D(1)/9)
            self.assertLess(abs(75*f*f-24*f+1),D('1e-70'))
            slope=D('.6')/(1+f)-D('.39')/(1-f)-D('.09')/(1-9*f)
            self.assertLess(abs(slope),D('1e-70'))
            self.assertLess(1-D('.2')*9,0)
            robust=(D(37)-D(1144).sqrt())/225
            self.assertLess(abs(225*robust*robust-74*robust+1),D('1e-70'))
            self.assertLess(robust,f)
            for x in (D('.01'),D('.05'),D('.1')):
                self.assertLess((1-9*x).ln()-(1-x).ln(),0)
        # Independently verify the common-denominator polynomial coefficients.
        for x in (F(0),F(1,50),F(1,20),F(1,10)):
            denominator=(1+x)*(1-x)*(1-9*x)
            slope=F(3,5)/(1+x)-F(39,100)/(1-x)-F(9,100)/(1-9*x)
            self.assertEqual(slope*denominator,9*x*x-F(72,25)*x+F(3,25))

    def test_easy_independent_distribution_and_exact_ties(self):
        fn=reference('c_l21_easy');task=CODES['c_l21_easy']
        for case in task['samples']+task['tests']:
            args=copy.deepcopy(case['args']);before=copy.deepcopy(args)
            expected=one_choice(*args)
            self.assertEqual(case['expected'],expected);self.assertEqual(fn(*args),expected);self.assertEqual(args,before)
        rng=random.Random(2120)
        for _ in range(300):
            n=rng.randrange(1,20);values=[rng.randrange(-10**9,10**9+1) for _ in range(n)]
            weights=[rng.randrange(10**9+1) for _ in range(n)]
            if not sum(weights):weights[0]=1
            args=[rng.randrange(-10**9,10**9+1),values,weights,rng.randrange(10**9+1)]
            self.assertEqual(fn(*args),one_choice(*args))

    def test_medium_fixtures_and_complete_stopping_policies(self):
        fn=reference('c_l21_medium');task=CODES['c_l21_medium']
        for case in task['samples']+task['tests']:
            args=copy.deepcopy(case['args']);before=copy.deepcopy(args)
            values,weights,costs=args
            if len(costs)==30:
                zero_probability=F(sum(w for v,w in zip(values,weights) if v==0),sum(weights))
                expected={'value':canonical(1-zero_probability**31),'threshold':canonical(1-zero_probability**30)}
            elif len(values)<=3 and len(costs)<=3:expected=stopping_oracle(*args)
            else:expected=case['expected']  # exact die ledgers verified separately above
            self.assertEqual(case['expected'],expected);self.assertEqual(fn(*args),expected);self.assertEqual(args,before)
        rng=random.Random(2121)
        for _ in range(80):
            n=rng.randrange(1,4);values=[rng.randrange(-7,9) for _ in range(n)]
            weights=[rng.randrange(5) for _ in range(n)]
            if not sum(weights):weights[0]=1
            costs=[rng.randrange(5) for _ in range(rng.randrange(3))]
            args=[values,weights,costs]
            self.assertEqual(fn(*args),stopping_oracle(*args))
        # Maximum duplicate-support length/horizon has an independent Bernoulli law.
        expected={'value':canonical(1-F(4,5)**31),'threshold':canonical(1-F(4,5)**30)}
        self.assertEqual(fn([0,1]*500,[4,1]*500,[0]*30),expected)

    def test_hard_fixtures_high_precision_and_no_mutation(self):
        fn=reference('c_l21_hard');task=CODES['c_l21_hard']
        for case in task['samples']+task['tests']:
            args=copy.deepcopy(case['args']);before=copy.deepcopy(args)
            returns,weights,cap=args
            # Duplicate binary rows compress to the exact p=.6 model for the oracle.
            oracle_args=([-1,1],[[2,3]],cap) if len(returns)==50 else args
            expected=robust_derivative_oracle(*oracle_args)
            self.assertAlmostEqual(case['expected'][0],float(expected[0]),delta=1e-7)
            self.assertAlmostEqual(case['expected'][1],float(expected[1]),delta=1e-7)
            actual=fn(*args);self.assertEqual(args,before)
            self.assertAlmostEqual(actual[0],float(expected[0]),delta=1e-7)
            self.assertAlmostEqual(actual[1],float(expected[1]),delta=1e-7)
            with localcontext() as ctx:
                ctx.prec=60
                self.assertAlmostEqual(actual[1],float(decimal_growth(returns,weights,actual[0])),delta=1e-7)

    def test_kink_optimum_by_polynomial_not_ternary_search(self):
        with localcontext() as ctx:
            ctx.prec=80
            low,high=D('.07'),D('.08')
            for _ in range(220):
                f=(low+high)/2
                if (1-f)**8-(1+f)**7*(1-9*f)<0:low=f
                else:high=f
            f=(low+high)/2
            first=D('.55')*(1+f).ln()+D('.45')*(1-f).ln()
            second=D('.9')*(1+f).ln()+D('.05')*(1-f).ln()+D('.05')*(1-9*f).ln()
            self.assertLess(abs(first-second),D('1e-60'))
            self.assertGreater(D('.55')/(1+f)-D('.45')/(1-f),0)
            self.assertLess(D('.9')/(1+f)-D('.05')/(1-f)-D('.45')/(1-9*f),0)
            out=reference('c_l21_hard')([1,-1,-9],[[55,45,0],[90,5,5]],.1)
            self.assertAlmostEqual(out[0],float(f),delta=1e-7)
            self.assertAlmostEqual(out[1],float(first),delta=1e-7)

    def test_hard_seeded_models_against_active_slope_oracle(self):
        fn=reference('c_l21_hard');rng=random.Random(2122)
        for _ in range(20):
            returns=[-3,-1,0,1,2];weights=[]
            for j in range(rng.randrange(1,4)):
                row=[rng.randrange(8) for _ in returns]
                # Include positive mean models, so this exercises an interior search.
                while sum(w*r for w,r in zip(row,returns))<=0:row[-1]+=1
                weights.append(row)
            args=[returns,weights,.2]
            expected=robust_derivative_oracle(*args);actual=fn(*args)
            self.assertAlmostEqual(actual[0],float(expected[0]),delta=1e-7)
            self.assertAlmostEqual(actual[1],float(expected[1]),delta=1e-7)
            self.assertEqual(fn(returns,[[w*7 for w in row] for row in weights],.2),actual)

    def test_exact_copies_preserve_both_public_large_samples(self):
        large={}
        for id in ('c_l21_easy','c_l21_medium'):
            large[id]=False
            for case in submission_cases(id)['cases']:
                copied={k:case[k] for k in ('argumentsJSON','expectedJSON')}
                parsed=parse_debug_cases(CODES[id],[copied])[0]
                self.assertEqual(parsed['expected'],json.loads(copied['expectedJSON']))
                self.assertLessEqual(sum(len(v) for v in copied.values()),500000)
                for key,value in parsed['expected'].items():
                    if value is None or isinstance(value,str):continue
                    self.assertTrue(all(isinstance(part,str) for part in value))
                    num,den=map(int,value)
                    self.assertGreater(den,0);self.assertEqual(math.gcd(abs(num),den),1)
                    self.assertEqual([str(num),str(den)],value)
                    large[id]|=abs(num)>2**53 or den>2**53
            self.assertTrue(large[id])
            public=CODES[id]['samples'][-1]['expected']
            self.assertTrue(any(abs(int(part))>2**53 for value in public.values() if isinstance(value,list) for part in value))

    def test_actual_complete_judge_and_public_exact_debugging(self):
        for id in ('c_l21_easy','c_l21_medium','c_l21_hard'):
            result=run(id,CODES[id]['solution'])
            self.assertFalse(result.get('error'),result.get('error'));self.assertEqual(result['passed'],result['total'])
        for id in ('c_l21_easy','c_l21_medium'):
            case=submission_cases(id)['cases'][2]
            copied={k:case[k] for k in ('argumentsJSON','expectedJSON')}
            result=run(id,CODES[id]['solution'],mode='debug',debug_cases=[copied])
            self.assertFalse(result.get('error'),result.get('error'));self.assertEqual(result['passed'],result['total'])


if __name__=='__main__':unittest.main()
