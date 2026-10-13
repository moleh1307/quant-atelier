"""Exact nonlinear-model checks independent of reference implementation paths."""
import copy,json,math,random,unittest
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from coding_bank import TASKS
from judge import run
from topic_practice.nonlinear_ml_coding import leaf_oracle,stump_oracle,kernel_oracle
B=json.loads(Path('static/content.json').read_text());QS={q['id']:q for q in B['questions']};CS={c['id']:c for c in TASKS}
def solver(id):
    ns={};exec(CS[id]['solution'],ns);return ns['solve']
def near(a,b):
    if b is None:return a is None
    if isinstance(b,list):return isinstance(a,list) and len(a)==len(b) and all(near(x,y) for x,y in zip(a,b))
    return math.isclose(a,b,rel_tol=1e-9,abs_tol=1e-7)
class NonlinearTests(unittest.TestCase):
    def test_route_and_difficulty_contract(self):
        ids=[l['id'] for l in B['lessons']];i=ids.index('l29');self.assertEqual(ids[i:i+3],['l29','l30','l12']);l=next(l for l in B['lessons'] if l['id']=='l30');self.assertEqual(l['path'],'researcher')
        self.assertEqual([QS[id]['difficulty'] for id in l['questions']],['Easy']*2+['Medium']*2+['Hard']*2);self.assertEqual([CS[id]['difficulty'] for id in l['coding']],['Easy','Medium','Hard']);self.assertTrue(all(QS[id]['type']!='written' for id in l['questions']))
    def test_easy_leaf_and_feature_ridge_independent(self):
        self.assertEqual(leaf_oracle([0,2,4,8],[1]*4,[0,0,1,1],[])[1],QS['q_l30_e1']['answer'])
        # Feature normal equation in primal rather than canonical kernel.
        phi=[[-1,1],[1,1]];z=[sum(r[j] for r in phi)/2 for j in range(2)];G=[[sum(r[j]*r[k] for r in phi)/2 for k in range(2)] for j in range(2)];self.assertEqual(z,[0,1]);coef=[z[j]/(G[j][j]+1) for j in range(2)];self.assertEqual(2*coef[0]+4*coef[1],QS['q_l30_e2']['answer'])
    def test_variance_by_common_and_individual_noise(self):
        # T_b = mean + 1.5 U + sqrt(27/4) V_b, independent zero-mean
        # unit variances. Compute covariance entries via those loadings.
        Bn=20;load_common=F(3,2);individual_var=F(27,4);cov=[[load_common**2+(individual_var if i==j else 0) for j in range(Bn)] for i in range(Bn)];risk=sum(map(sum,cov))/Bn**2+1+2;self.assertEqual(risk,F(447,80));self.assertAlmostEqual(float(risk),QS['q_l30_m1']['answer'])
    def test_logistic_leaf_surrogate_and_true_loss(self):
        ys=[1,1,1,0];g=sum(F(1,2)-y for y in ys);h=len(ys)*F(1,4);v=-g/(h+1);self.assertEqual(v,F(1,2));self.assertEqual(float(v),QS['q_l30_m2']['answer']);self.assertAlmostEqual(1/(1+math.exp(-.1)),.52497918747894)
        loss=lambda v:sum(max(v,0)-y*v+math.log1p(math.exp(-abs(v))) for y in ys)+v*v/2
        self.assertLess(loss(float(v)),loss(0));self.assertNotAlmostEqual(4/(1+math.exp(-float(v)))-3+float(v),0)
    def test_singular_kernel_representation_and_wrong_penalty(self):
        from topic_practice.statistical_learning_coding import rational_solve
        K=[[F(1)]*2 for _ in range(2)];A=[[K[i][j]+int(i==j) for j in range(2)] for i in range(2)];a=rational_solve(A,[F(1),F(-1)]);self.assertEqual(a,[1,-1]);self.assertEqual(sum(a),0)
        self.assertEqual(sum((y-sum(a))**2 for y in [1,-1]),QS['q_l30_h1']['checks'][0]['answer']);self.assertEqual(sum(a)**2,QS['q_l30_h1']['checks'][1]['answer'])
        wrong=rational_solve([[F(3),F(2)],[F(2),F(3)]],[F(2),F(2)]);self.assertEqual(sum(wrong),F(4,5));self.assertEqual(float(sum(wrong)),QS['q_l30_h1']['checks'][2]['answer']);right=rational_solve(A,[F(1),F(1)]);self.assertEqual(sum(right),F(2,3))
    def test_xor_projection_greedy_gain_and_shift(self):
        corners=list(product([-1,1],repeat=2));ys=[x*z for x,z in corners]
        self.assertEqual(sum(ys),0);self.assertTrue(all(sum(y*x[j] for x,y in zip(corners,ys))==0 for j in range(2)))
        for j in range(2):self.assertTrue(all(sum(y for x,y in zip(corners,ys) if x[j]==sign)==0 for sign in [-1,1]))
        for g1 in product([-2,0,3],repeat=2):
            for g2 in product([-1,2],repeat=2):
                v=[a+b for a in g1 for b in g2];self.assertEqual(v[3]-v[2]-v[1]+v[0],0)
        weights=[F(1,8),F(1,8),F(3,8),F(3,8)];stump=[F(x[1],2) for x in corners];train=sum(w*(y-p)**2 for w,y,p in zip(weights,ys,stump));deploy=sum((y-p)**2 for y,p in zip(ys,stump))/4
        self.assertEqual(train,F(3,4));self.assertEqual(deploy,F(5,4));self.assertEqual(float(1-train),QS['q_l30_h2']['checks'][1]['answer']);self.assertEqual(float(deploy),QS['q_l30_h2']['checks'][2]['answer'])
    def test_leaf_reference_exact_and_mutation(self):
        solve=solver('c_l30_easy');rng=random.Random(300)
        for _ in range(50):
            ys=[rng.randint(-10,10) for _ in range(12)];weights=[rng.randint(1,100) for _ in ys];groups=[rng.choice([-7,4,90]) for _ in ys];args=[ys,weights,groups,list(set(groups))*2];before=copy.deepcopy(args);self.assertTrue(near(solve(*args),leaf_oracle(*args)));self.assertEqual(args,before)
    def test_stump_reference_exact_ties_and_boundaries(self):
        solve=solver('c_l30_medium');rng=random.Random(301)
        for _ in range(100):
            n=rng.randrange(1,12);p=rng.randrange(1,5);args=[[[rng.randrange(-2,3) for _ in range(p)] for _ in range(n)],[rng.randrange(-10,11) for _ in range(n)],[rng.randrange(1,100) for _ in range(n)],rng.randrange(1,n+1)];before=copy.deepcopy(args);self.assertTrue(near(solve(*args),stump_oracle(*args)));self.assertEqual(args,before)
        self.assertEqual(solve([[0,0],[1,1],[2,2]],[4,4,4],[1,2,3],1),[0,.5,4,4,0]);self.assertIsNone(solve([[0],[0]],[1,2],[1,1],1));self.assertIsNone(solve([[0],[1],[2]],[1,2,3],[100,1,1],2))
    def test_kernel_reference_vs_direct_deleted_refits(self):
        solve=solver('c_l30_hard');rng=random.Random(302)
        for _ in range(30):
            n=rng.randrange(2,8);p=rng.randrange(1,4);args=[[[rng.randrange(-2,3) for _ in range(p)] for _ in range(n)],[rng.randrange(-10,11) for _ in range(n)],[[rng.randrange(-2,3) for _ in range(p)] for _ in range(rng.randrange(0,4))],rng.choice([.5,1,2,10])];before=copy.deepcopy(args);self.assertTrue(near(solve(*args),kernel_oracle(*args)));self.assertEqual(args,before)
        # All training feature vectors identical: exact rank-one closed law,
        # including maximally declared dimensions and m=70.
        n=70;xs=[[2]*6 for _ in range(n)];ys=[i%11-5 for i in range(n)];q=625;lam=.5;got=solve(xs,ys,xs,lam);expected=[q*sum(ys)/(lam+n*q)]*n;loo=[q*(sum(ys)-y)/(lam+(n-1)*q) for y in ys];self.assertTrue(near(got,[expected,loo,sum((y-v)**2 for y,v in zip(ys,loo))/n]))
    def test_actual_judge_references_and_wrong_implementations(self):
        for suffix in ['easy','medium','hard']:
            id='c_l30_'+suffix;out=run(id,CS[id]['solution']);self.assertNotIn('error',out);self.assertEqual(out['passed'],out['total'],out)
        wrong_leaf=CS['c_l30_easy']['solution'].replace('totals[g] = totals.get(g,0)+w','totals[g] = totals.get(g,0)+1').replace('sums[g] = sums.get(g,0)+w*y','sums[g] = sums.get(g,0)+y')
        wrong_kernel=CS['c_l30_hard']['solution'].replace('y-a/d for y,a,d','y-a for y,a,d')
        for id,source in [('c_l30_easy',wrong_leaf),('c_l30_hard',wrong_kernel)]:
            result=run(id,source);self.assertNotIn('error',result);self.assertLess(result['passed'],result['total'])
