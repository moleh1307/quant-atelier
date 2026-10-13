import copy,json,math,random,unittest
from collections import Counter
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from coding_bank import TASKS
from judge import run
from topic_practice.statistical_learning_coding import diagonal_oracle,logistic_oracle,cv_oracle,rational_solve
B=json.loads(Path('static/content.json').read_text());QS={q['id']:q for q in B['questions']};CS={c['id']:c for c in TASKS}
def solver(id):
    ns={};exec(CS[id]['solution'],ns);return ns['solve']
def near(a,b):
    if isinstance(b,list):return len(a)==len(b) and all(near(x,y) for x,y in zip(a,b))
    return math.isclose(a,b,rel_tol=1e-9,abs_tol=1e-7)
def lasso_certificate(G,z,b,lam):
    scores=[z[j]-sum(G[j][k]*b[k] for k in range(2)) for j in range(2)]
    return all((v==lam*(1 if b[j]>0 else -1)) if b[j] else abs(v)<=lam for j,v in enumerate(scores))
def active_oracle(G,z,lam):
    # Independently enumerate positive/negative/zero active faces with exact
    # rational linear systems and validate all subgradient inequalities.
    for signs in product([-1,0,1],repeat=2):
        active=[j for j,s in enumerate(signs) if s];b=[F(0),F(0)]
        values=rational_solve([[G[j][k] for k in active] for j in active],[z[j]-lam*signs[j] for j in active]) if active else []
        for j,v in zip(active,values):b[j]=v
        if all(b[j]*signs[j]>0 for j in active) and lasso_certificate(G,z,b,lam):return b
    raise AssertionError('No lasso face certified')

class StatisticalLearningTests(unittest.TestCase):
    def test_order_and_automatic_difficulty_contract(self):
        ids=[l['id'] for l in B['lessons']];i=ids.index('l11');self.assertEqual(ids[i:i+4],['l11','l29','l30','l12']);l=next(l for l in B['lessons'] if l['id']=='l29')
        self.assertEqual(l['path'],'researcher');self.assertEqual(Counter(QS[x]['difficulty'] for x in l['questions']),Counter(Easy=2,Medium=2,Hard=2));self.assertEqual(Counter(CS[x]['difficulty'] for x in l['coding']),Counter(Easy=1,Medium=1,Hard=1));self.assertTrue(all(QS[x]['type']!='written' for x in l['questions']))
    def test_risk_decomposition_by_finite_independent_samples(self):
        # Fresh Y=2±sqrt(3), fitted prediction=1±sqrt(.5), independent.
        errors=[(2+s*math.sqrt(3)-(1+t*math.sqrt(.5)))**2 for s,t in product([-1,1],repeat=2)];self.assertAlmostEqual(sum(errors)/4,QS['q_l29_e2']['answer'])
    def test_normalization_and_feature_units(self):
        xs=[F(-1),F(1)];ys=[F(-2),F(2)];G=sum(x*x for x in xs)/2;z=sum(x*y for x,y in zip(xs,ys))/2
        self.assertEqual(z/(G+1),F(QS['q_l29_e1']['answer']));self.assertEqual((2*z)/(2*G+2),1)
        lam=F(QS['q_l29_m1']['answer']);self.assertEqual(4/(4+lam),F(1,2));self.assertEqual(F(2*4,4+1),F(8,5))
    def test_newton_probability_curvature(self):
        residuals=[F(1,2),F(-1,2)];gradient=sum(x*r for x,r in zip([-1,1],residuals))/2;H=F(1,4)+F(1,2);self.assertEqual(-gradient/H,F(2,3));self.assertAlmostEqual(QS['q_l29_m2']['answer'],float(-gradient/H));self.assertEqual(sum(residuals),0)
    def test_fixed_design_ridge_risk_by_noise_enumeration(self):
        # X=diag(2,.5), ε independent Rademacher. Enumerate estimates directly,
        # then score future x in ±sqrt(2)e1/±sqrt(8)e2 equally likely (H=diag(1,4)).
        estimates=[[F(2*(2+u),5),(F(1,2)*v)/(F(1,4)+1)] for u,v in product([-1,1],repeat=2)]
        risk=sum((b[0]-1)**2+4*b[1]**2 for b in estimates)/4;self.assertEqual(risk,F(21,25));self.assertAlmostEqual(QS['q_l29_h1']['checks'][0]['answer'],float(risk))
        self.assertEqual(F(4,5)+F(1,5),F(QS['q_l29_h1']['checks'][1]['answer']));self.assertEqual(F(1,4)+4*4,F(65,4))
    def test_correlated_lasso_active_faces_and_duplicates(self):
        G=[[F(1),F(4,5)],[F(4,5),F(1)]];z=[F(1),F(9,10)];b=active_oracle(G,z,F(3,10));self.assertEqual(b,[F(11,18),F(1,9)]);self.assertAlmostEqual(QS['q_l29_h2']['checks'][0]['answer'],float(b[1]))
        for numerator in range(0,21):
            lam=F(numerator,20);coef=active_oracle(G,z,lam);self.assertEqual(coef[1]==0,lam>=F(1,2))
        self.assertEqual(QS['q_l29_h2']['checks'][1]['answer'],.5)
        objs=[]
        for a in [F(0),F(1,10),F(3,10),F(7,10)]:
            b=F(7,10)-a;objs.append((a+b)**2/2-(a+b)+F(3,10)*(abs(a)+abs(b)))
        self.assertEqual(len(set(objs)),1);self.assertEqual(F(7,10)/(2+F(1,5)),F(7,22));self.assertAlmostEqual(QS['q_l29_h2']['checks'][2]['answer'],7/22)
    def test_diagonal_soft_thresholds_vs_exact_oracle(self):
        solve=solver('c_l29_easy');rng=random.Random(29)
        for _ in range(80):
            args=[[rng.choice([.1,1,2,5]) for i in range(8)],[rng.randint(-10,10) for i in range(8)],rng.choice([0,.5,1,3]),rng.choice([0,.3,1])];saved=copy.deepcopy(args);self.assertTrue(near(solve(*args),diagonal_oracle(*args)));self.assertEqual(args,saved)
        self.assertEqual(solve([1,1],[.5,-.5],.5,0),[0,0])
    def test_logistic_high_precision_and_finite_difference_gradients(self):
        solve=solver('c_l29_medium');rng=random.Random(292)
        for _ in range(30):
            xs=[[rng.randint(-3,3) for j in range(3)] for i in range(6)];ys=[rng.randrange(2) for i in xs];weights=[rng.uniform(-1,1) for j in range(3)];a=.4;lam=.3;args=[xs,ys,weights,a,lam];saved=copy.deepcopy(args);got=solve(*args);self.assertTrue(near(got,logistic_oracle(*args)));self.assertEqual(args,saved)
            h=1e-5;derivative=(solve(xs,ys,weights,a+h,lam)[0]-solve(xs,ys,weights,a-h,lam)[0])/(2*h);self.assertAlmostEqual(derivative,got[1],delta=1e-8)
            for j in range(3):
                plus=weights.copy();minus=weights.copy();plus[j]+=h;minus[j]-=h;derivative=(solve(xs,ys,plus,a,lam)[0]-solve(xs,ys,minus,a,lam)[0])/(2*h);self.assertAlmostEqual(derivative,got[2][j],delta=1e-8)
        for z in [-1000,1000]:
            got=solve([[1]],[int(z<0)],[z],0,0);self.assertTrue(all(math.isfinite(v) for v in [got[0],got[1],*got[2]]));self.assertTrue(near(got,logistic_oracle([[1]],[int(z<0)],[z],0,0)))
        self.assertEqual(solve([[0],[0]],[1,1],[2],-3,.5)[2],[1])
    def test_fold_local_ridge_vs_raw_rational_parameterization(self):
        solve=solver('c_l29_hard');rng=random.Random(293)
        for _ in range(55):
            xs=[[rng.randint(-4,4) for j in range(3)] for i in range(10)];ys=[rng.randint(-5,5) for i in xs];folds=[[[0,1,2,3],[4]],[[1,2,3,4,5,6],[7,8,9]]];lambdas=[.1,.5,1,4];args=[xs,ys,folds,lambdas];saved=copy.deepcopy(args);got=solve(*args);self.assertTrue(near(got,cv_oracle(*args)));self.assertEqual(args,saved)
            transformed=[[3*x+7,2*y-4,z] for x,y,z in xs];self.assertTrue(near(solve(transformed,ys,folds,lambdas),got))
        self.assertTrue(near(solve([[0],[2],[4]],[0,2,4],[[[0,1],[2]]],[.5,1]),[0,[1,2.25]]))
        self.assertEqual(solve([[0],[2],[4]],[1,1,1],[[[0,1],[2]]],[10,.1,1]),[0,[0,0,0]])
    def test_actual_judge_and_rejected_wrong_procedures(self):
        for level in ['easy','medium','hard']:
            id=f'c_l29_{level}';result=run(id,CS[id]['solution']);self.assertNotIn('error',result,(id,result));self.assertEqual(result['passed'],result['total'],(id,result))
        wrongThreshold=CS['c_l29_easy']['solution'].replace('abs(z)-lambda1','abs(z)-lambda1/2');result=run('c_l29_easy',wrongThreshold);self.assertLess(result['passed'],result['total'])
        wrongIntercept=CS['c_l29_medium']['solution'].replace('ga = math.fsum(residuals)/n','ga = math.fsum(residuals)/n+penalty*intercept');result=run('c_l29_medium',wrongIntercept);self.assertLess(result['passed'],result['total'])
        wrongNormalization=CS['c_l29_hard']['solution'].replace('(lam if j == k else 0)','(lam/n if j == k else 0)');result=run('c_l29_hard',wrongNormalization);self.assertLess(result['passed'],result['total'])
        wrongScale=CS['c_l29_hard']['solution'].replace('mean = [math.fsum(xs[i][j] for i in train)/n','mean = [math.fsum(xs[i][j] for i in range(len(xs)))/len(xs)');result=run('c_l29_hard',wrongScale);self.assertLess(result['passed'],result['total'])
if __name__=='__main__':unittest.main()
