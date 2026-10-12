"""Independent covariance/loadings checks, not calls to the production recurrences."""
import copy
import itertools
import json
import math
import random
import unittest
from collections import Counter
from fractions import Fraction as F


def pair(x):
    return [str(x.numerator), str(x.denominator)]


def linear_solve(matrix, rhs):
    rows = [[F(x) for x in row] + [F(b)] for row, b in zip(matrix, rhs)]
    for j in range(len(rows)):
        pivot = next(i for i in range(j, len(rows)) if rows[i][j])
        rows[j], rows[pivot] = rows[pivot], rows[j]
        scale = rows[j][j]
        rows[j] = [x / scale for x in rows[j]]
        for i in range(len(rows)):
            if i != j:
                scale = rows[i][j]
                rows[i] = [x - scale * y for x, y in zip(rows[i], rows[j])]
    return [row[-1] for row in rows]


def covariance_oracle(a, b, q, prior_mean, prior_variance, observations, requests):
    """Condition the entire joint Gaussian covariance for each requested prefix.

    Covariances are built from independent innovation loadings. This oracle has
    no scalar Kalman predict/update or stored filtered mean/variance timeline.
    """
    rho = F(a, b)
    def covariance(t, s):
        return rho**(t+s)*prior_variance + q*sum((rho**(t+s-2*j) for j in range(1,min(t,s)+1)), F(0))
    answer = []
    for asof, target in requests:
        seen = [(s,y,r) for s,y,r in observations if s <= asof]
        cross = [covariance(target,s) for s,_,_ in seen]
        matrix = [[covariance(s,t)+(r if i==j else 0) for j,(t,_,_) in enumerate(seen)] for i,(s,_,r) in enumerate(seen)]
        weights = linear_solve(matrix,cross) if seen else []
        mean = rho**target*prior_mean + sum((w*(y-rho**s*prior_mean) for w,(s,y,_) in zip(weights,seen)), F(0))
        variance = covariance(target,target) - sum((w*c for w,c in zip(weights,cross)), F(0))
        answer.append(dict(mean=pair(mean),variance=pair(variance)))
    return answer


def moving_average_covariances(kernel):
    return [sum(kernel[j]*kernel[j+h] for j in range(len(kernel)-h)) for h in range(len(kernel))]


def moving_average_sum_variance(n, kernel):
    # Coefficients of independent innovations in the finite sum, rather than
    # lag covariance pair counts from the production reference.
    loadings = {}
    for t in range(n):
        for j,k in enumerate(kernel):
            loadings[t-j] = loadings.get(t-j,0) + k
    return F(sum(x*x for x in loadings.values()),n*n)


class TimeSeriesPractice(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import build_content
        from coding_bank import TASKS
        cls.questions={x['id']:x for x in build_content.Q}
        cls.lesson=next(x for x in build_content.L if x['id']=='l13')
        cls.tasks={x['id']:x for x in TASKS}
        cls.solutions={}
        for task in TASKS:
            if task['id'] in ('c_l13_easy','c08','c_l13_hard'):
                scope={};exec(task['solution'],scope)
                cls.solutions[task['id']]=scope['solve']

    def test_topic_contract_and_specific_rubrics(self):
        self.assertEqual(Counter(self.questions[x]['difficulty'] for x in self.lesson['questions']),Counter(Easy=2,Medium=2,Hard=4))
        self.assertEqual(self.lesson['questions'][:2],['q18','q31'])
        self.assertEqual(self.lesson['coding'],['c_l13_easy','c08','c_l13_hard'])
        for key in self.lesson['questions']:
            self.assertGreaterEqual(len(self.questions[key]['hints']),2)
            self.assertGreaterEqual(len(self.questions[key]['rubric']),3)
        self.assertIn('full-series mean',self.tasks['c08']['prompt'])

    def test_authored_inputs_respect_the_contract(self):
        for case in self.tasks['c_l13_easy']['samples']+self.tasks['c_l13_easy']['tests']:
            n,v,c=case['args']
            self.assertTrue(1<=n<=10**9 and 1<=v<=10**18)
            self.assertLessEqual(len(c),100000)
            self.assertTrue(all(abs(x)<=v for x in c))
        for case in self.tasks['c_l13_hard']['samples']+self.tasks['c_l13_hard']['tests']:
            a,b,q,m,v,observations,requests=case['args']
            self.assertTrue(1<=b<=20 and abs(a)<=b)
            self.assertTrue(0<=q<=10**6 and 0<=v<=10**6 and abs(m)<=10**6)
            self.assertLessEqual(len(requests),10000)
            self.assertEqual([t for t,_,_ in observations],sorted({t for t,_,_ in observations}))
            self.assertTrue(all(1<=t<=120 and abs(y)<=10**6 and 1<=r<=10**6 for t,y,r in observations))
            self.assertTrue(all(0<=s<=t<=120 for s,t in requests))

    def test_finite_covariances_and_forecast_innovations(self):
        for rho,variance in ((F(1,2),F(22,9)),(F(-1,2),F(2,3))):
            matrix=[[4*rho**abs(i-j) for j in range(3)] for i in range(3)]
            self.assertEqual(sum(map(sum,matrix))/9,variance)
        self.assertAlmostEqual(self.questions['q_l13_e1']['answer'],22/9)
        self.assertEqual(2+F(1,4)*(10-2),4)
        self.assertEqual(3*(1+F(1,4)),F(15,4))
        for h in range(1,10):
            self.assertEqual(sum(3*F(1,4)**j for j in range(h)),4*(1-F(1,4)**h))
        self.assertEqual(3*F(1,2),F(3,2))

    def test_hidden_nonlinear_dependence_exact_moments(self):
        # A finite proxy has the same standardized moments through order four
        # as the Gaussian innovations. X=3*z[t]*z[t-1] avoids irrational values.
        choices=[(-1,F(1,6)),(0,F(2,3)),(1,F(1,6))]
        for n in range(1,6):
            ey=F(0);ey2=F(0);ex=F(0);ex2=F(0);adjacent=F(0)
            for record in itertools.product(choices,repeat=n+1):
                z=[x for x,_ in record];weight=math.prod(p for _,p in record)
                xs=[3*z[i]*z[i-1] for i in range(1,n+1)]
                y=F(sum(x*x for x in xs),n);x=F(sum(xs),n)
                ey+=weight*y;ey2+=weight*y*y;ex+=weight*x;ex2+=weight*x*x
                if n>1: adjacent+=weight*xs[0]**2*xs[1]**2
            self.assertEqual(ey,1);self.assertEqual(ex,0)
            self.assertEqual(ex2,F(1,n))
            self.assertEqual(ey2-ey*ey,F(12*n-4,n*n))
            if n>1: self.assertEqual(adjacent,3)

    def test_overlap_counts_against_independent_return_records(self):
        for n in range(1,5):
            for k in range(1,n+1):
                total=F(0)
                for returns in itertools.product((-1,1),repeat=n+k-1):
                    estimate=F(sum(sum(returns[t:t+k]) for t in range(n)),n*k)
                    total+=estimate*estimate
                actual=total/(2**(n+k-1))
                stated=F(1,n)-F(k*k-1,3*n*n*k)
                self.assertEqual(actual,stated)
                self.assertGreaterEqual(actual,F(1,n+k-1))
        for k in range(1,8):
            for h in range(k+2):
                self.assertEqual(len(set(range(k)) & set(range(h,h+k))),max(0,k-h))

    def test_blue_weights_against_dense_covariance_optimization(self):
        for n in range(2,9):
            for rho in (F(-4,5),F(-1,2),F(0),F(1,2),F(4,5)):
                matrix=[[rho**abs(i-j) for j in range(n)] for i in range(n)]
                precision=linear_solve(matrix,[1]*n)
                weights=[x/sum(precision) for x in precision]
                d=n-(n-2)*rho
                expected=[F(1,d)]+[(1-rho)/d]*(n-2)+[F(1,d)]
                self.assertEqual(weights,expected)
                variance=sum(weights[i]*matrix[i][j]*weights[j] for i in range(n) for j in range(n))
                self.assertEqual(variance,(1+rho)/d)
                changed=weights.copy();changed[0]+=F(1,7);changed[-1]-=F(1,7)
                self.assertGreater(sum(changed[i]*matrix[i][j]*changed[j] for i in range(n) for j in range(n)),variance)
        self.assertEqual(4*F(3,2)/F(5,2),F(12,5))
        self.assertLess(F(12,5),F(22,9))
        # E max of two iid N(mu,1): half the absolute N(0,2) difference.
        self.assertAlmostEqual(math.sqrt(2)*math.sqrt(2/math.pi)/2,1/math.sqrt(math.pi))

    def test_changing_persistence_and_initialization_limits(self):
        for c in (.1,1,3,8):
            g=2*(c+math.expm1(-c))/(c*c)
            initialized=g-(-math.expm1(-c)/c)**2
            errors=[]
            for n in (200,2000,10000):
                rho=math.exp(-c/n)
                # Independent recurrence for variance of successive sums:
                # Cov(S[t-1],X[t])=rho*(Cov(S[t-2],X[t-1])+1).
                covariance=0.;sum_variance=0.
                for t in range(1,n+1):
                    sum_variance+=1+2*covariance
                    covariance=rho*(covariance+1)
                finite=sum_variance/(n*n)
                initial_loading=sum(rho**t for t in range(1,n+1))/n
                errors.append(abs(finite-g))
                if n==10000:
                    self.assertAlmostEqual(finite,g,delta=3e-4)
                    self.assertAlmostEqual(finite-initial_loading**2,initialized,delta=3e-4)
                    fixed_innovation=finite/(1-rho*rho)/n
                    self.assertAlmostEqual(fixed_innovation,(c-1+math.exp(-c))/c**3,delta=3e-3)
            self.assertLess(errors[-1],errors[0])
        self.assertAlmostEqual(1/(2/math.e),math.e/2)
        self.assertNotAlmostEqual(math.e/2,.5)

    def test_easy_against_innovation_loadings_and_boundaries(self):
        solve=self.solutions['c_l13_easy'];rng=random.Random(1301)
        for _ in range(180):
            n=rng.randint(1,18);kernel=[rng.randint(-5,5) for _ in range(rng.randint(1,7))]
            if not any(kernel):kernel[0]=1
            cov=moving_average_covariances(kernel);before=cov[1:].copy()
            self.assertEqual(solve(n,cov[0],before),pair(moving_average_sum_variance(n,kernel)))
            self.assertEqual(before,cov[1:])
        self.assertEqual(solve(2,4,[-4]),['0','1'])
        self.assertEqual(solve(1,7,[2]*100000),['7','1'])
        self.assertEqual(solve(10**9,3,[-2,1]),['1',str(10**9)])
        for case in self.tasks['c_l13_easy']['samples']+self.tasks['c_l13_easy']['tests']:
            self.assertEqual(solve(*case['args']),case['expected'])

    def test_hard_against_dense_gaussian_conditioning(self):
        solve=self.solutions['c_l13_hard'];rng=random.Random(1313)
        for _ in range(90):
            end=rng.randint(0,9);b=rng.randint(1,5);a=rng.randint(-b,b)
            times=sorted(rng.sample(range(1,end+1),rng.randint(0,end)))
            obs=[[t,rng.randint(-12,12),rng.randint(1,8)] for t in times]
            requests=[]
            for _ in range(6):
                asof=rng.randint(0,end);requests.append([asof,rng.randint(asof,end)])
            args=[a,b,rng.randint(0,6),rng.randint(-5,5),rng.randint(0,7),obs,requests]
            before=copy.deepcopy(args)
            self.assertEqual(solve(*args),covariance_oracle(*args))
            self.assertEqual(args,before)
        for case in self.tasks['c_l13_hard']['samples']+self.tasks['c_l13_hard']['tests']:
            self.assertEqual(solve(*case['args']),case['expected'])
            if len(case['args'][-1])<100:
                self.assertEqual(case['expected'],covariance_oracle(*case['args']))

    def test_forecast_information_boundary_and_metamorphic_identities(self):
        solve=self.solutions['c_l13_hard']
        args=[-2,3,2,5,7,[[1,-4,2],[3,20,3],[6,999,1]],[[0,6],[1,6],[3,6],[6,6],[1,6]]]
        result=solve(*args)
        for request,item in zip(args[-1],result):
            truncated=[row for row in args[-2] if row[0]<=request[0]]
            self.assertEqual(solve(*args[:5],truncated,[request])[0],item)
        self.assertEqual(result,solve(-4,6,*args[2:]))
        reflected=solve(-2,3,2,-5,7,[[t,-y,r] for t,y,r in args[-2]],args[-1])
        for x,y in zip(result,reflected):
            self.assertEqual(F(*map(int,x['mean'])),-F(*map(int,y['mean'])))
            self.assertEqual(x['variance'],y['variance'])
        variances=[F(*map(int,x['variance'])) for x in result[:4]]
        self.assertTrue(all(a>=b for a,b in zip(variances,variances[1:])))
        self.assertEqual(result[1],result[-1])

    def test_maximum_horizon_queries_and_degenerate_models(self):
        solve=self.solutions['c_l13_hard']
        observations=[[t,t-60,1+t%7] for t in range(1,121)]
        requests=[[t,t] for t in range(121)]+[[t,120] for t in range(120)]
        result=solve(0,1,3,5,0,observations,requests)
        for (asof,target),value in zip(requests,result):
            if target==0:expected=dict(mean=['5','1'],variance=['0','1'])
            elif target==asof:
                r=1+target%7;expected=dict(mean=pair(F(3*(target-60),3+r)),variance=pair(F(3*r,3+r)))
            else:expected=dict(mean=['0','1'],variance=['3','1'])
            self.assertEqual(value,expected)
        many=[[0,0],[0,120],[119,120]]*3333+[[0,0]]
        results=solve(-1,1,0,-3,0,[],many)
        self.assertEqual(len(results),10000)
        self.assertTrue(all(x==dict(mean=['-3','1'],variance=['0','1']) for x in results))
        self.assertEqual(solve(1,1,0,3,0,[[1,999,1]],[[1,1],[1,120]]),[dict(mean=['3','1'],variance=['0','1'])]*2)
        self.assertEqual(solve(1,2,3,0,4,[],[]),[])

    def test_actual_judge_copy_limits_and_wrong_shortcuts(self):
        import judge
        for key in ('c_l13_easy','c08','c_l13_hard'):
            task=self.tasks[key];result=judge.run(key,task['solution'])
            self.assertNotIn('error',result,result)
            self.assertEqual(result['passed'],result['total'],result)
            for case in task['samples']+task['tests']:
                self.assertLessEqual(len(json.dumps(case['args']))+len(json.dumps(case['expected'])),200000)
        bad='def solve(n, variance, lag_covariances):\n    from math import gcd\n    g=gcd(variance,n)\n    return [str(variance//g),str(n//g)]'
        result=judge.run('c_l13_easy',bad)
        self.assertLess(result['passed'],result['total'])
        # Incorrectly smooth with all observations, ignoring request asof.
        args=[1,2,3,0,4,[[1,8,1],[3,-10,4]],[[0,3],[1,3]]]
        proper=self.solutions['c_l13_hard'](*args)
        future_seen=self.solutions['c_l13_hard'](*args[:-1],[[3,3],[3,3]])
        self.assertNotEqual(proper,future_seen)
        self.assertEqual(judge.parse_debug_cases(self.tasks['c_l13_hard'],judge.submission_cases('c_l13_hard')['cases']),self.tasks['c_l13_hard']['samples']+self.tasks['c_l13_hard']['tests'])


if __name__=='__main__':unittest.main()
