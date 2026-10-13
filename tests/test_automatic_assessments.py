"""Check conversion isolation, publication guards and independent concrete keys.

New numerical examples are checked by direct finite records, exact fractions,
quadratic minimization and probability calculations, not by the UI grader.
Existing topic suites retain their full derivation/algorithm checks.
"""
import copy
import hashlib
import itertools
import json
import math
import unittest
from fractions import Fraction as F
from pathlib import Path

from automatic_assessments import CHECKS, VERSION, validate_assessments, attach_objective_assessments

ROOT=Path(__file__).resolve().parents[1]
BANK=json.loads((ROOT/'static/content.json').read_text())
QS={q['id']:q for q in BANK['questions']}
BASE=json.loads((ROOT/'tests/fixtures/objective-conversion-contract.json').read_text())
FIELDS=('prompt','solution','hints','followup','followSolution','rubric','title','difficulty','lesson','path','minutes','answer','tolerance')

class AutomaticAssessmentTests(unittest.TestCase):
    def key(self,id,part,expected):
        c=QS[id]['checks'][part-1]
        self.assertEqual(c['type'],'numeric')
        self.assertAlmostEqual(c['answer'],float(expected),delta=max(1e-40,abs(float(expected))*1e-12),msg=f'{id} part {part}')

    def test_every_old_prompt_derivation_id_and_numeric_contract_survives(self):
        self.assertEqual(set(QS)-set(BASE),{f'q_l{n}_{s}' for n in (26,27,28,29,30,31,32) for s in ('e1','e2','m1','m2','h1','h2')})
        self.assertEqual(len(CHECKS),84)
        self.assertEqual(sum(q['type']=='numeric' for q in QS.values()),122)
        self.assertEqual(sum(q['type']=='structured' for q in QS.values()),84)
        for id in BASE:
            q=QS[id]
            digest=hashlib.sha256(json.dumps({k:q[k] for k in FIELDS},sort_keys=True,ensure_ascii=False).encode()).hexdigest()
            self.assertEqual(digest,BASE[id]['sha256'],id)
            self.assertEqual(q['type'],'structured' if BASE[id]['type']=='written' else BASE[id]['type'])
        validate_assessments(list(QS.values()))

    def test_future_automatic_authoring_guard(self):
        missing=[dict(id='new-written',type='written')]
        with self.assertRaisesRegex(ValueError,'Author objective checks'):attach_objective_assessments(missing)
        for mutate in (
            lambda q:q.pop('assessmentVersion'),
            lambda q:q.update(checks=[]),
            lambda q:q['checks'][0].update(answer=math.inf),
            lambda q:q['checks'][1]['options'][0].pop('explanation'),
            lambda q:[o.update(correct=True) for o in q['checks'][1]['options']],
            lambda q:q['checks'][1]['options'][0].update(id=q['checks'][1]['options'][1]['id']),
            lambda q:q['checks'][0].update(tolerance=1)):
            q=copy.deepcopy(QS['q_l09_h2']);mutate(q)
            with self.assertRaises(ValueError):validate_assessments([q])

    def test_regression_scaling_probability_and_likelihood_examples(self):
        x=[F(1),F(2)];y=[F(1),F(3)]
        b=sum(a*t for a,t in zip(x,y))/sum(a*a for a in x)
        self.key('q21',1,sum(t-b*a for a,t in zip(x,y)))
        self.key('q22',1,F(81+2,100)-F(19+18,100))
        # Compute expected centered sum from every equally likely Rademacher
        # sample, scaled to variance nine: no variance correction formula used.
        sums=[]
        for sample in itertools.product([-3,3],repeat=5):
            m=F(sum(sample),5);sums.append(sum((v-m)**2 for v in sample)/5)
        self.key('q24',1,sum(sums)/len(sums))
        self.key('q26',2,F(1,10)*F(4,5)/(F(1,10)*F(4,5)+F(9,10)*F(1,5)))
        train=[0,2];mean=F(sum(train),len(train));sd=math.sqrt(sum((a-mean)**2 for a in train)/len(train))
        self.key('q28',1,(100-mean)/sd)
        self.key('q30',1,F(1,100)/(F(1,10000)+F(1,100)))
        # Sum covariance entries, including both off-diagonal directions.
        self.key('q31',1,sum(F(1) if i==j else F(1,4) if abs(i-j)==1 else F(0) for i in range(252) for j in range(252)))
        self.key('q33',1,40*(F(2)-F(3,2))-30)
        self.key('q41',1,(100*F(4,5)+200*F(1,5))/(F(4,5)+F(1,5)))
        self.key('q42',1,F(201,2)-F(197,2))
        # Integrate the squared antithetic polynomial exactly term by term.
        coeff=[F(1,2),-1,1];squared=[sum(coeff[i]*coeff[j] for i in range(3) for j in range(3) if i+j==k) for k in range(5)]
        second=sum(v/F(k+1) for k,v in enumerate(squared));self.key('q43',1,second-F(1,3)**2)
        self.key('q43',2,(F(1,5)-F(1,3)**2)/2)
        self.key('q44',2,max([(0,2,4),(1,4,9)],key=lambda r:r[0] if r[1]<=3 else -math.inf)[2])
        self.key('q48',1,F(3,4));self.key('q48',2,9+F(3,4)**2*4-2*F(3,4)*3)
        self.key('q50',1,max([1,2,4,6]));self.key('q51',1,F(1,2)**100/F(1,2))
        self.assertLess(QS['q51']['checks'][0]['tolerance'],float(F(1,2)**99)/100)

    def test_counting_covariance_and_estimation_transfer_cases(self):
        draws=list(itertools.product('ABC',repeat=2));self.key('q_l01_m1',1,F(sum(a!=b for a,b in draws),len(draws)))
        multisets=list(itertools.combinations_with_replacement('ABC',2));self.key('q_l01_m1',2,F(sum(a!=b for a,b in multisets),len(multisets)))
        self.key('q_l02_h1',1,F(1,4)/(F(1,4)+2*F(1,4)*F(1,4)))
        self.key('q_l05_h2',1,1*(100-1))
        self.key('q_l06_h2',1,F(495,1000)/F(255,1000));self.key('q_l06_h2',2,F(515,1000)/F(255,1000))
        self.key('q_l07_h2',1,sum(1 if i==j else F(-3,10) for i in range(5) for j in range(5)))
        # Enumerate the attained outcomes at the budget in the concrete check.
        profits={int(1 if u>=5 else -1)-int(1 if v>=5 else -1) for u in [0,4,5,6,10] for v in [0,4,5,6,8,10] if abs(u-4)+abs(v-8)<=2}
        self.key('q_l08_h1',1,len(profits))
        self.key('q_l09_h1',1,F(2,3)/F(2,4))
        risks=[]
        for p in [F(0),F(1,4),F(1,2),F(3,4),F(1)]:
            risks.append(sum(F(math.comb(16,k))*p**k*(1-p)**(16-k)*(F(k+2,20)-p)**2 for k in range(17)))
        self.assertEqual(len(set(risks)),1);self.key('q_l09_h2',1,risks[0])
        self.key('q_l25_h1',1,0);self.key('q_l25_h2',1,1)
        b=[[1,1,-1],[1,1,1],[-1,1,1]];w=[1,-1,1];self.key('q_l10_m1',1,sum(w[i]*b[i][j]*w[j] for i in range(3) for j in range(3)))
        self.key('q_l10_h1',1,F(2+2,2)**2)
        self.key('q_l10_h2',1,(2-2)**2)
        # Direct four-point generator moments, without assuming causality from fit.
        records=[(u+v,3*u+v) for u,v in itertools.product([-1,1],repeat=2)]
        self.key('q_l11_m1',1,F(sum(x*y for x,y in records),sum(x*x for x,y in records)));self.key('q_l11_m1',2,1)
        self.key('q_l11_h1',1,F(6,2));self.key('q_l11_h2',1,F(6)/(1-F(2,5)))

    def test_testing_time_series_and_evaluation_keys(self):
        null=[F(math.comb(6,k),64) for k in range(7)];gamma=(F(1,20)-null[6])/null[5]
        self.key('q_l12_m1',1,gamma)
        alt=[math.comb(6,k)*F(3,4)**k*F(1,4)**(6-k) for k in range(7)]
        self.key('q_l12_m1',2,alt[6]+gamma*alt[5])
        self.key('q_l12_h1',1,1/F(1,100));self.key('q_l12_h2',1,F(95,100)/F(975,1000))
        self.key('q_l13_m1',1,F(4*8+2*3*2,16))
        # Each underlying iid return carries its observed overlap multiplicity.
        multiplicities=[sum(t<=j<t+3 for t in range(5)) for j in range(7)]
        self.key('q_l13_m2',1,F(sum(v*v for v in multiplicities),15**2))
        weights=[F(2,7),F(1,7),F(1,7),F(1,7),F(2,7)]
        self.key('q_l13_h1',1,sum(weights[i]*weights[j]*F(1,2)**abs(i-j) for i in range(5) for j in range(5)))
        # Numerical quadrature of the limiting kernel, independent of its closed form.
        m=2000;integral=sum(2*(1-(i+.5)/m)*math.exp(-2*(i+.5)/m)/m for i in range(m))
        self.assertAlmostEqual(QS['q_l13_h2']['checks'][0]['answer'],integral,delta=1e-6)
        rows=[[2,6,6],[6,10,10],[9,12,12],[14,17,17],[8,10,13]]
        self.key('q_l14_m1',1,sum(start<10 and receipt<=10 and not(start<14 and end>10) for start,end,receipt in rows))
        self.key('q_l14_h1',1,math.sqrt((1/(4*500))/.05))
        self.key('q_l15_h1',1,-.5*math.sqrt(2/math.pi))
        self.key('q_l16_m1',1,(F(7,10)-F(6,10))/((F(99,100)-F(6,10))-(F(96,100)-F(7,10))))
        self.key('q_l16_m1',2,F(9,10)*F(96-99,100)+F(1,10)*F(70-60,100))
        records=[(F(1,8),12),(F(3,8),0),(F(3,8),F(-4,3)),(F(1,8),0)]
        mean=sum(p*z for p,z in records);self.key('q_l16_h1',1,sum(p*(z-mean)**2 for p,z in records))
        self.key('q_l16_h1',2,(F(1,2)*F(1,4)*3+F(1,2)*F(3,4)*(-1))/F(1,2))
        n=1
        while (1-.001)**n>.05:n+=1
        self.key('q_l17_m1',1,n);self.key('q_l17_m1',2,1-math.exp(math.log(.05)/1000))

    def test_streaming_and_trading_keys(self):
        xs=[0,2,8,10,12];mean=F(sum(xs),len(xs));self.key('q_l18_m1',1,sum((x-mean)**2 for x in xs))
        self.key('q_l18_h1',1,sum((x-4)**2 for x in [2,4,6]))
        import heapq
        heap=[]
        for i,value in enumerate(range(1,101)):
            heapq.heappush(heap,(-value,i))
            while heap[0][1]<=i-2:heapq.heappop(heap)
        self.key('q_l18_h2',1,len(heap))
        cells=[((0,0),F(4,10)),((0,10),F(1,10)),((10,0),F(1,10)),((10,10),F(4,10))]
        weights=[p*(F(3,4) if a else F(1,4)) for (a,b),p in cells]
        self.key('q_l19_m1',1,sum(w*(a+b) for w,((a,b),p) in zip(weights,cells))/sum(weights))
        self.key('q_l19_m2',1,2*5-3);self.key('q_l19_m2',2,F(1,4)*1+F(3,4)*13)
        self.key('q_l19_h1',1,F(1,2)*(8-6-F(1,2))+F(1,2)*(4-2-F(1,2)))
        self.key('q_l19_h2',1,12*(F(3,4)*F(3,4))/(F(3,4)*F(3,4)+F(1,4)*F(1,4)))
        prior=F(1,2);high=F(3,4)*F(1,4)*F(3,4)*prior;low=F(1,4)*F(3,4)*F(1,4)*(1-prior);posterior=high/(high+low)
        self.key('q_l20_m1',1,posterior*F(3,4)*(80-100)+(1-posterior)*F(1,4)*80)
        self.key('q_l20_m2',1,F(1,2)*F(1,2)*(70-100-1))
        self.key('q_l20_h1',1,F(1,2)*(12-2)+F(1,2)*0)
        def stage(continuation):return sum(max(F(i),continuation) for i in range(1,7))/6
        self.key('q_l21_m1',1,stage(stage(F(7,2))-1));self.key('q_l21_m1',2,stage(stage(F(7,2)-1)))
        def binary(p):return 2*p-1
        self.key('q_l21_h1',1,binary((F(55,100)+F(65,100))/2));self.key('q_l21_h1',2,binary(F(55,100)))
        # Derivative bisection, independent of the quadratic root expression.
        lo,hi=0,1/9
        for _ in range(90):
            mid=(lo+hi)/2;der=.6/(1+mid)-.39/(1-mid)-.09/(1-9*mid)
            if der>0:lo=mid
            else:hi=mid
        self.key('q_l21_h2',1,(lo+hi)/2)
        self.key('q_l22_h1',1,F(1,4))
        h=F(1,2);self.key('q_l22_h2',1,h);self.key('q_l22_h2',2,max(4*(1-b*h)**2+1+h*h for b in [1,3]))
        self.key('q_l23_m1',1,5-8-101+100);self.key('q_l23_m1',2,-8+5+97-100)
        self.key('q_l23_h1',1,1-2*F(25,100))
        delta0=F(4);v0=F(200);cash=delta0*100-v0;cash+=(F(44,10)-delta0)*110
        self.key('q_l23_h2',1,cash+197-F(44,10)*100);self.key('q_l23_h2',2,197-v0-delta0*(100-100))
        self.key('q_l24_m1',1,((F(1,10)-1)**2+(F(9,10)-0)**2)/2)
        optimum=F(200,3);self.key('q_l24_h1',1,optimum);self.key('q_l24_h1',2,F(1,2)*(100-optimum)*(optimum/100)**2)
        self.key('q_l24_h2',1,F(1,4)-(F(1,4)*F(3,4)+F(3,4)*F(1,4))/2)
