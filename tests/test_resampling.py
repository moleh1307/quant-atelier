import copy,json,math,random,unittest
from collections import Counter
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from coding_bank import TASKS
from judge import run
from topic_practice.resampling_coding import paired_oracle,interval_oracle,block_enumeration
B=json.loads(Path('static/content.json').read_text());QS={q['id']:q for q in B['questions']};CS={c['id']:c for c in TASKS}
def solver(id):
    ns={};exec(CS[id]['solution'],ns);return ns['solve']
def near(a,b):
    if isinstance(b,list):return len(a)==len(b) and all(near(x,y) for x,y in zip(a,b))
    return math.isclose(a,b,rel_tol=1e-10,abs_tol=1e-7)
def block_covariance(values,length):
    n=len(values);mu=F(sum(values),n);centered=[F(x)-mu for x in values]
    cov=lambda h:sum(centered[i]*centered[(i+h)%n] for i in range(n))/n
    window=lambda size:size*cov(0)+2*sum((size-h)*cov(h) for h in range(1,size))
    full=(n-1)//length;tail=n-full*length
    return (full*window(length)+window(tail))/(n*n)

class ResamplingTests(unittest.TestCase):
    def test_prerequisite_order_and_difficulty_contract(self):
        ids=[l['id'] for l in B['lessons']];i=ids.index('l13');self.assertEqual(ids[i:i+3],['l13','l28','l14'])
        l=next(l for l in B['lessons'] if l['id']=='l28');self.assertEqual(l['path'],'researcher')
        self.assertEqual(Counter(QS[id]['difficulty'] for id in l['questions']),Counter(Easy=2,Medium=2,Hard=2));self.assertEqual(Counter(CS[id]['difficulty'] for id in l['coding']),Counter(Easy=1,Medium=1,Hard=1));self.assertTrue(all(QS[id]['type']!='written' for id in l['questions']))
    def test_mean_variance_and_distinct_indices_by_enumeration(self):
        means=[F(sum([1,2,4][i] for i in draw),3) for draw in product(range(3),repeat=3)]
        mu=sum(means)/len(means);var=sum((v-mu)**2 for v in means)/len(means);self.assertEqual(var,F(14,27));self.assertAlmostEqual(QS['q_l28_e1']['answer'],float(var))
        distinct=sum(len(set(draw)) for draw in product(range(4),repeat=4));self.assertEqual(F(distinct,4**4),F(175,64));self.assertEqual(QS['q_l28_e2']['answer'],175/64)
    def test_pairing_keeps_the_correlation(self):
        a=[1,2,4];b=[2,3,5];meansA=[F(sum(a[i] for i in ids),3) for ids in product(range(3),repeat=3)];meansB=[v+1 for v in meansA]
        independent=[x-y for x,y in product(meansA,meansB)];mean=sum(independent)/len(independent);var=sum((v-mean)**2 for v in independent)/len(independent);self.assertEqual(var,F(28,27));self.assertEqual(QS['q_l28_m2']['answer'],float(var));self.assertTrue(all(sum(a[i]-b[i] for i in ids)/3==-1 for ids in product(range(3),repeat=3)))
    def test_interval_reflection_and_exact_quantile_rules(self):
        self.assertEqual(QS['q_l28_m1']['answer'],10-5)
        solve=solver('c_l28_medium');rng=random.Random(28)
        for _ in range(100):
            reps=[rng.randint(-10,20) for _ in range(rng.randrange(2,35))];obs=rng.randint(-10,20);alpha=rng.choice([.05,.1,.2,.5]);saved=reps.copy();got=solve(obs,reps,alpha)
            self.assertTrue(near(got,interval_oracle(obs,reps,alpha)));self.assertEqual(reps,saved)
            transformed=solve(3*obs+7,[3*x+7 for x in reps],alpha)
            self.assertTrue(near(transformed,[3*got[0],3*got[1],[3*x+7 for x in got[2]],[3*x+7 for x in got[3]]]))
        self.assertTrue(near(solve(10,[7,9,10,12,15],.2),[.6,math.sqrt(9.3),[7.8,13.8],[6.2,12.2]]));self.assertEqual(solve(5,[5,5,5],.05),[0,0,[5,5],[5,5]])
    def test_maximum_atom_and_true_pivot(self):
        maxima=[max(ids) for ids in product(range(4),repeat=4)];mass=F(sum(m==3 for m in maxima),4**4);self.assertEqual(mass,F(175,256));self.assertEqual(QS['q_l28_h1']['checks'][0]['answer'],float(mass));self.assertAlmostEqual(QS['q_l28_h1']['checks'][1]['answer'],1-math.exp(-1))
        counts=Counter(maxima);self.assertEqual([counts[i] for i in range(4)],[1,15,65,175])
        for n in (4,10,50):
            alpha=.05;self.assertAlmostEqual(1-(alpha**(1/n))**n,1-alpha)
        self.assertGreater(1-(1-1/10000)**10000,.63);self.assertLess(1-math.exp(-.01),.01)
    def test_cluster_ratios_and_conditional_bias(self):
        clusters=[[0,0],[10]*4];means=[]
        for ids in product(range(2),repeat=2):
            values=[v for i in ids for v in clusters[i]];means.append(F(sum(values),len(values)))
        mu=sum(means)/4;var=sum((x-mu)**2 for x in means)/4;self.assertEqual(mu,F(35,6));self.assertEqual(var,F(475,36));self.assertEqual(mu-F(20,3),F(-5,6))
        self.assertEqual(QS['q_l28_h2']['checks'][0]['answer'],float(mu));self.assertEqual(QS['q_l28_h2']['checks'][1]['answer'],float(var))
    def test_jackknife_mean_variance(self):
        for values in ([1,2,4],[0,0,6],[-2,4,8,9]):
            n=len(values);mu=F(sum(values),n);deletes=[F(sum(values)-v,n-1) for v in values];center=sum(deletes)/n
            variance=F(n-1,n)*sum((v-center)**2 for v in deletes);s2=sum((F(v)-mu)**2 for v in values)/(n-1);self.assertEqual(center,mu);self.assertEqual(variance,s2/n)
    def test_supplied_pairs_preserve_inputs_and_replicate_order(self):
        solve=solver('c_l28_easy');rng=random.Random(99)
        for _ in range(60):
            rows=[[rng.randint(-8,8),rng.randint(-8,8)] for i in range(rng.randrange(1,8))];indices=[[rng.randrange(len(rows)) for i in rows] for b in range(7)];args=[rows,indices];saved=copy.deepcopy(args);self.assertTrue(near(solve(*args),paired_oracle(*args)));self.assertEqual(args,saved)
    def test_circular_blocks_vs_enumeration_and_covariance(self):
        solve=solver('c_l28_hard');rng=random.Random(17)
        for n in range(1,9):
            for _ in range(8):
                values=[rng.randint(-9,9) for _ in range(n)];saved=values.copy()
                for length in range(1,n+1):
                    expected=float(block_covariance(values,length));self.assertAlmostEqual(solve(values,length),expected,delta=1e-10)
                    if n**((n+length-1)//length)<=10000:self.assertAlmostEqual(block_enumeration(values,length),expected,delta=1e-10)
                self.assertEqual(values,saved)
        self.assertEqual(solve([0]*4+[10]*4,3),325/64);self.assertEqual(solve([1000,-1000]*10000,10001),.005)
    def test_actual_submit_suites_and_rejected_conceptual_errors(self):
        for level in ('easy','medium','hard'):
            id=f'c_l28_{level}';result=run(id,CS[id]['solution']);self.assertNotIn('error',result,id);self.assertEqual(result['passed'],result['total'],(id,result))
        wrongSE=CS['c_l28_medium']['solution'].replace('mean-observed,se,','mean-observed,se/math.sqrt(n),');r=run('c_l28_medium',wrongSE);self.assertLess(r['passed'],r['total'])
        wrongTail=CS['c_l28_hard']['solution'].replace('full*variance_numerator(block_length)+variance_numerator(tail)','(full+1)*variance_numerator(block_length)');r=run('c_l28_hard',wrongTail);self.assertLess(r['passed'],r['total'])
if __name__=='__main__':unittest.main()
