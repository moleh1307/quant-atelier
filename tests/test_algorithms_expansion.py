"""Independent combinatorial/state oracles for the two added algorithm chapters."""
import copy,itertools,json,random,unittest
from collections import Counter
from pathlib import Path
from coding_bank import TASKS
from judge import run
from topic_practice.algorithms_expansion_coding import bounds_oracle,topk_oracle,median_oracle,distance_oracle,interval_oracle
B=json.loads(Path('static/content.json').read_text());QS={q['id']:q for q in B['questions']};CS={c['id']:c for c in TASKS}
def solver(id):
    scope={};exec(CS[id]['solution'],scope);return scope['solve']
class AlgorithmExpansionTests(unittest.TestCase):
    def test_route_banks_and_automatic_contract(self):
        ids=[l['id'] for l in B['lessons']];i=ids.index('l18');self.assertEqual(ids[i:i+3],['l18','l31','l32'])
        for id in ['l31','l32']:
            l=next(l for l in B['lessons'] if l['id']==id);self.assertEqual(l['path'],'researcher');self.assertEqual(Counter(QS[q]['difficulty'] for q in l['questions']),Counter(Easy=2,Medium=2,Hard=2));self.assertEqual(Counter(CS[c]['difficulty'] for c in l['coding']),Counter(Easy=1,Medium=1,Hard=1));self.assertTrue(all(QS[q]['type']!='written' for q in l['questions']))
    def test_boundaries_exhaustive_empty_duplicates_and_no_mutation(self):
        solve=solver('c_l31_easy')
        for n in range(7):
            for a in itertools.combinations_with_replacement([-1,0,1],n):
                args=[list(a),[-2,-1,0,1,2]];before=copy.deepcopy(args);self.assertEqual(solve(*args),bounds_oracle(*args));self.assertEqual(args,before)
        self.assertEqual(bounds_oracle([1,2,2,2,5,8,8,11],[8])[0][1],QS['q_l31_e1']['answer'])
    def test_prefix_frequency_count_by_all_intervals(self):
        a=[2,-1,2,1,-2,3];count=sum(sum(a[i:j])==3 for i in range(len(a)) for j in range(i+1,len(a)+1));self.assertEqual(count,QS['q_l31_e2']['answer'])
        for n in range(8):self.assertEqual(sum(sum([0]*(j-i))==0 for i in range(n) for j in range(i+1,n+1)),n*(n+1)//2)
    def test_topk_exhaustive_stable_ranking(self):
        solve=solver('c_l31_medium')
        for n in range(6):
            for a in itertools.product([-1,0,1],repeat=n):
                for k in range(n+1):self.assertEqual(solve(list(a),k),topk_oracle(a,k))
        self.assertEqual(topk_oracle([7,2,7,3,7,4],2)[1],QS['q_l31_m1']['answer']);a=[7,2,7];saved=a.copy();solve(a,2);self.assertEqual(a,saved)
    def test_median_exhaustive_signed_duplicates_all_widths(self):
        solve=solver('c_l31_hard')
        for n in range(7):
            for a in itertools.product([-1,0,1],repeat=n):
                for k in range(1,n+2):self.assertEqual(solve(list(a),k),median_oracle(list(a),k))
        self.assertEqual(median_oracle([4,1,4,2,9,8],4)[-1],QS['q_l31_m2']['answer']);a=[-10,5,5,1,99];saved=a.copy();solve(a,4);self.assertEqual(a,saved)
    def test_capacity_key_via_all_cuts_and_signed_failure(self):
        a=[7,2,5,10,8];capacities=[]
        for bits in range(1<<(len(a)-1)):
            cuts=[0]+[i+1 for i in range(len(a)-1) if bits>>i&1]+[len(a)]
            if len(cuts)-1<=3:capacities.append(max(sum(a[x:y]) for x,y in zip(cuts,cuts[1:])))
        self.assertEqual(min(capacities),QS['q_l31_h1']['checks'][0]['answer']);cuts=[sum(a[:2]),a[2],a[3],a[4]];self.assertTrue(all(x<=13 for x in cuts));self.assertEqual(len(cuts),QS['q_l31_h1']['checks'][1]['answer']);self.assertLessEqual(sum([6,-5]),2);self.assertGreater(max([6,-5]),2)
    def test_frequency_rank_keys_from_literal_multiset(self):
        values=[-5,-2,0,3,7,10,11,20];counts=[2,0,3,1,0,2,1,0];multiset=[v for v,c in zip(values,counts) for _ in range(c)];coordinate=values.index(multiset[4])+1;self.assertEqual(coordinate,QS['q_l31_h2']['checks'][0]['answer']);multiset.remove(-5);self.assertEqual(multiset[3]+multiset[4],QS['q_l31_h2']['checks'][1]['answer'])
    def test_bfs_all_three_vertex_graphs_and_directions(self):
        solve=solver('c_l32_easy');pairs=list(itertools.product(range(3),repeat=2))
        for mask in range(1<<9):
            edges=[list(e) for i,e in enumerate(pairs) if mask>>i&1]
            for source in range(3):self.assertEqual(solve(3,edges,source),distance_oracle(3,edges,source,False))
        edges=[[0,1],[0,2],[1,3],[2,3],[3,4],[5,4]];self.assertEqual(distance_oracle(6,edges,0,False)[4],QS['q_l32_e1']['answer']);self.assertEqual(distance_oracle(6,edges,0,False)[5],-1)
    def test_topological_order_count_by_permutations(self):
        count=0
        for order in itertools.permutations('ABCDE'):
            index={v:i for i,v in enumerate(order)}
            if all(index[u]<index[v] for u,v in [('A','C'),('B','C'),('C','D')]):count+=1
        self.assertEqual(count,QS['q_l32_e2']['answer'])
    def test_dijkstra_against_all_pairs_closure_and_mutation(self):
        solve=solver('c_l32_medium');rng=random.Random(320)
        for _ in range(150):
            n=rng.randrange(1,8);edges=[[rng.randrange(n),rng.randrange(n),rng.randrange(0,10)] for _ in range(rng.randrange(0,35))];source=rng.randrange(n);args=[n,edges,source];before=copy.deepcopy(args);self.assertEqual(solve(*args),distance_oracle(*args));self.assertEqual(args,before)
        edges=[[0,1,9],[0,2,1],[2,1,1],[1,3,1],[2,3,10],[3,4,0],[1,4,7]];self.assertEqual(distance_oracle(5,edges,0)[4],QS['q_l32_m1']['answer'])
    def test_all_dag_routes_by_explicit_path_enumeration(self):
        edges=[(0,1),(0,2),(1,3),(2,3),(1,4),(3,4),(3,5),(4,5)];paths=[]
        def visit(path):
            if path[-1]==5:paths.append(path);return
            for u,v in edges:
                if u==path[-1]:visit(path+[v])
        visit([0]);self.assertEqual(len(paths),QS['q_l32_m2']['answer']);self.assertEqual(sum(len(p)==4 for p in paths),3)
    def test_negative_edge_keys_by_simple_routes_and_settlement(self):
        edges=[(0,1,2),(0,2,5),(2,1,-4),(1,3,2),(2,3,1)];paths=[]
        def visit(u,cost,seen):
            if u==3:paths.append(cost);return
            for a,v,w in edges:
                if a==u and v not in seen:visit(v,cost+w,seen|{v})
        visit(0,0,{0});self.assertEqual(min(paths),QS['q_l32_h1']['checks'][0]['answer'])
        d=[0,None,None,None];settled=set()
        for _ in range(4):
            u=min((i for i in range(4) if i not in settled and d[i] is not None),key=lambda i:d[i]);settled.add(u)
            for a,v,w in edges:
                if a==u and v not in settled and (d[v] is None or d[u]+w<d[v]):d[v]=d[u]+w
        self.assertEqual(d[3],QS['q_l32_h1']['checks'][1]['answer']);self.assertEqual(-4+2-4,QS['q_l32_h1']['checks'][2]['answer'])
    def test_interval_dp_against_subsets_and_canonical_tie_vector(self):
        solve=solver('c_l32_hard');rng=random.Random(321)
        for _ in range(100):
            jobs=[]
            for j in range(rng.randrange(0,10)):
                start=rng.randrange(-3,8);jobs.append([start,start+rng.randrange(1,5),rng.randrange(-4,12)])
            before=copy.deepcopy(jobs);self.assertEqual(solve(jobs),interval_oracle(jobs));self.assertEqual(jobs,before)
        jobs=[[0,3,5],[1,2,3],[2,4,4],[3,5,5],[4,6,4],[5,7,4],[0,7,12]];out=interval_oracle(jobs);self.assertEqual(out,[14,[0,3,5]]);self.assertEqual(out[0],QS['q_l32_h2']['checks'][0]['answer']);self.assertEqual(3+4+4,QS['q_l32_h2']['checks'][1]['answer']);self.assertEqual(len(interval_oracle(jobs+[[0,7,14]])[1]),QS['q_l32_h2']['checks'][2]['answer'])
    def test_actual_judge_references_wrong_procedures_and_copy_limits(self):
        for l in [31,32]:
            for s in ['easy','medium','hard']:
                id=f'c_l{l}_{s}';result=run(id,CS[id]['solution']);self.assertNotIn('error',result);self.assertEqual(result['passed'],result['total'],result)
                for case in CS[id]['samples']+CS[id]['tests']:self.assertLessEqual(len(json.dumps(case['args'],separators=(',',':')))+len(json.dumps(case['expected'],separators=(',',':'))),500000)
        bad=[('c_l31_medium',CS['c_l31_medium']['solution'].replace('(value,-i)','(value,i)')),('c_l31_hard',CS['c_l31_hard']['solution'].replace('update(coordinates[values[i-k]],-1)','pass')),('c_l32_medium',CS['c_l32_medium']['solution'].replace('candidate < distance[v]','False')),('c_l32_hard',CS['c_l32_hard']['solution'].replace('bisect_right','bisect_left')),('c_l32_hard',CS['c_l32_hard']['solution'].replace('candidate > dp[-1]','candidate >= dp[-1]'))]
        for id,source in bad:
            result=run(id,source);self.assertTrue(result.get('error') or result['passed']<result['total'],(id,result))
