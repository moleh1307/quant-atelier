import copy, json, math, random, unittest
from collections import Counter
from pathlib import Path
from coding_bank import TASKS
from judge import run
from topic_practice.calculus_optimization_coding import box_oracle, recurrence_oracle, weighted_oracle, armijo_oracle, gd_oracle
BANK=json.loads(Path('static/content.json').read_text());QS={q['id']:q for q in BANK['questions']};CS={c['id']:c for c in TASKS}

def solver(id):
    scope={};exec(CS[id]['solution'],scope);return scope['solve']

def near(a,b):
    if isinstance(b,list):return len(a)==len(b) and all(near(x,y) for x,y in zip(a,b))
    return math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-7)

class DifferentialPractice(unittest.TestCase):
    def test_registration_order_and_coverage(self):
        ids=[l['id'] for l in BANK['lessons']];self.assertEqual(ids[8:12],['l26','l27','l09','l25'])
        for n in (26,27):
            l=next(l for l in BANK['lessons'] if l['id']==f'l{n}')
            self.assertEqual(Counter(QS[q]['difficulty'] for q in l['questions']),Counter(Easy=2,Medium=2,Hard=2))
            self.assertEqual(Counter(CS[c]['difficulty'] for c in l['coding']),Counter(Easy=1,Medium=1,Hard=1))
            self.assertTrue(all(QS[q]['type']!='written' for q in l['questions']))
    def test_independent_interview_derivations(self):
        self.assertEqual(QS['q_l26_e1']['answer'],2*(2*1-3))
        self.assertAlmostEqual(QS['q_l26_e2']['answer'],-2*3/5-4*4/5)
        self.assertEqual(QS['q_l26_m1']['answer'],2*(2-4))
        self.assertEqual(QS['q_l26_m2']['answer'],-2)
        for h in (.1,.001,1e-8):self.assertAlmostEqual((h*h/math.sqrt(2*h*h))/math.sqrt(2*h*h),.5)
        v=recurrence_oracle(.5,2,[1,0,-1],[0,0,0]);self.assertAlmostEqual(QS['q_l26_h2']['checks'][0]['answer'],v[1]);self.assertAlmostEqual(QS['q_l26_h2']['checks'][1]['answer'],v[2])
        self.assertEqual(QS['q_l27_m1']['answer'],2/10)
        step=armijo_oracle([[4,1],[1,2]],[0,0],[1,1],1,.25);self.assertEqual(QS['q_l27_m2']['answer'],step[1])
        for a in (0,.1,.2,.5,1):
            y=max(a,.2);x=1-y;mu=5*y-1;nu=-x
            self.assertAlmostEqual(x+nu,0);self.assertAlmostEqual(4*y+nu-mu,0);self.assertGreaterEqual(mu,-1e-15);self.assertAlmostEqual(mu*(a-y),0)
        bx=box_oracle([[1,1],[1,2]],[-2,-3],[[0,2],[0,.5]])
        self.assertEqual(bx,[1.5,.5,-19/8]);self.assertEqual(QS['q_l27_h2']['checks'][1]['answer'],-9/4-bx[2])
    def test_all_six_actual_runner_submissions_and_hidden_cases(self):
        for n in (26,27):
            for level in ('easy','medium','hard'):
                id=f'c_l{n}_{level}';result=run(id,CS[id]['solution']);self.assertNotIn('error',result,id);self.assertTrue(result['passed'] == result['total'],(id,result))
    def test_reverse_gradient_vs_forward_and_finite_differences(self):
        solve=solver('c_l26_hard');rng=random.Random(26)
        for _ in range(45):
            a=rng.choice([-.75,-.5,0,.25,.75]);x=rng.randint(-4,4);us=[rng.randint(-3,3) for _ in range(rng.randint(1,9))];ys=[rng.randint(-3,3) for _ in us];args=[a,x,us,ys];saved=copy.deepcopy(args)
            got=solve(*args);self.assertTrue(near(got,recurrence_oracle(*args)));self.assertEqual(args,saved)
            h=1e-5
            for index in (0,1):
                hi=copy.deepcopy(args);lo=copy.deepcopy(args);hi[index]+=h;lo[index]-=h
                deriv=(solve(*hi)[0]-solve(*lo)[0])/(2*h);self.assertAlmostEqual(got[index+1],deriv,delta=1e-6)
    def test_weighted_gradient_invariance_and_numerical_derivative(self):
        solve=solver('c_l26_easy');rng=random.Random(4)
        for _ in range(50):
            rows=[[rng.randint(-10,10),rng.randint(-10,10),rng.randint(1,5)] for _ in range(7)];m,b=rng.randint(-3,3),rng.randint(-3,3)
            got=solve(rows,m,b);self.assertTrue(near(got,weighted_oracle(rows,m,b)))
            self.assertTrue(near(got,solve([[x,y,8*w] for x,y,w in rows],m,b)))
            def loss(m,b):return sum(w*(m*x+b-y)**2 for x,y,w in rows)/(2*sum(z[2] for z in rows))
            h=1e-4;self.assertAlmostEqual(got[0],(loss(m+h,b)-loss(m-h,b))/(2*h),delta=1e-6)
    def test_stable_logistic_against_independent_probability_loss(self):
        solve=solver('c_l26_medium')
        for z in (-10,-2,0,2,10):
            for y in (0,1):
                prob=1/(1+math.exp(-z));expected=-math.log(prob if y else 1-prob)
                v=solve([[1,y]],0,z);self.assertAlmostEqual(v[0],expected,delta=1e-10);self.assertAlmostEqual(v[1],prob-y)
                h=1e-4;self.assertAlmostEqual(v[2],(solve([[1,y]],0,z+h)[0]-solve([[1,y]],0,z-h)[0])/(2*h),delta=1e-8)
        self.assertEqual(solve([[1,0],[-1,1]],1000,0),[1000,1,0])
    def test_box_reference_vs_rational_kkt_and_all_feasible_direction_signs(self):
        solve=solver('c_l27_hard');rng=random.Random(27)
        for _ in range(300):
            # Gram construction with a positive diagonal ensures SPD.
            u,v=rng.randint(-5,5),rng.randint(-5,5);h=[[u*u+1,u*v],[u*v,v*v+1]];b=[rng.randint(-10,10),rng.randint(-10,10)];bounds=[sorted([rng.randint(-4,4),rng.randint(-4,4)]) for _ in range(2)];args=[h,b,bounds];saved=copy.deepcopy(args)
            got=solve(*args);self.assertTrue(near(got,box_oracle(*args)),args);self.assertEqual(args,saved)
            x,y,_=got;grad=[h[0][0]*x+h[0][1]*y+b[0],h[1][0]*x+h[1][1]*y+b[1]]
            for zx in bounds[0]:
                for zy in bounds[1]:self.assertGreaterEqual(grad[0]*(zx-x)+grad[1]*(zy-y),-1e-8)
    def test_updates_and_backtracking_against_exact_independent_oracles(self):
        gd=solver('c_l27_easy');ls=solver('c_l27_medium');rng=random.Random(42)
        for _ in range(90):
            h=[[rng.randint(1,20),0],[0,rng.randint(1,20)]];b=[rng.randint(-5,5),rng.randint(-5,5)];x=[rng.randint(-3,3),rng.randint(-3,3)];alpha=rng.choice([.25,.5,1,2,8]);c=rng.choice([.25,.5]);args=[h,b,x,alpha,c];saved=copy.deepcopy(args);self.assertTrue(near(ls(*args),armijo_oracle(*args)));self.assertEqual(args,saved)
            a=[h[0][0],h[1][1]];step=.125/max(a);n=rng.randrange(21);self.assertTrue(near(gd(a,b,x,step,n),gd_oracle(a,b,x,step,n)))

if __name__=='__main__':unittest.main()
