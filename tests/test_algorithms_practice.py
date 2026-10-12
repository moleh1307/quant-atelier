"""Exact centred moment identities, exhaustive windows and streaming cost witnesses."""
import copy
import heapq
import itertools
import math
import random
import unittest
from collections import Counter,deque
from fractions import Fraction as F
from coding_bank import TASKS
from judge import run,submission_cases,parse_debug_cases
from test_topic_practice import BANK,QUESTIONS,reference


def summary(values):
    if not values:return (0,None,F(0))
    mean=sum(map(F,values))/len(values)
    return len(values),mean,sum((F(v)-mean)**2 for v in values)


def merge(a,b):
    na,ma,sa=a;nb,mb,sb=b
    if not na:return b
    if not nb:return a
    n=na+nb;delta=mb-ma
    return n,ma+F(nb,n)*delta,sa+sb+F(na*nb,n)*delta**2


def replace(state,old,new):
    k,m,s=state
    if k==1:return (1,F(new),F(0))
    removed=m+(m-old)/(k-1)
    residual=s-(old-m)*(old-removed)
    updated=removed+(new-removed)/k
    return k,updated,residual+(new-removed)*(new-updated)


def earliest_windows(values,k):
    return [min(range(i-k+1,i+1),key=lambda j:(-values[j],j)) for i in range(k-1,len(values))]


def deque_trace(values,k):
    candidates=deque();answers=[];removed=set();pushes=pops=maximum=largest_burst=0
    for i,x in enumerate(values):
        burst=0
        while candidates and candidates[0]<=i-k:
            gone=candidates.popleft();assert gone not in removed;removed.add(gone);pops+=1;burst+=1
        while candidates and values[candidates[-1]]<x:
            gone=candidates.pop();assert gone not in removed;removed.add(gone);pops+=1;burst+=1
        candidates.append(i);pushes+=1;maximum=max(maximum,len(candidates));largest_burst=max(largest_burst,burst)
        indices=list(candidates)
        assert all(a<b for a,b in zip(indices,indices[1:]))
        assert all(values[a]>=values[b] for a,b in zip(indices,indices[1:]))
        assert all(j>i-k for j in indices)
        if i>=k-1:answers.append(candidates[0])
    return answers,(pushes,pops,maximum,largest_burst)


class AlgorithmsPracticeTests(unittest.TestCase):
    def test_contract_and_legacy_calibration_meaning(self):
        lesson=next(l for l in BANK['lessons'] if l['id']=='l18')
        self.assertEqual(lesson['questions'][0],'q44')
        self.assertEqual(Counter(QUESTIONS[id]['difficulty'] for id in lesson['questions']),Counter(Easy=2,Medium=2,Hard=2))
        self.assertEqual(lesson['coding'],['c_l18_easy','c05','c13']);self.assertEqual(lesson['legacyCoding'],['c14'])
        trader=next(l for l in BANK['lessons'] if l['id']=='l24');self.assertIn('c14',trader['coding'])
        for id in lesson['questions']:self.assertGreaterEqual(len(QUESTIONS[id]['rubric']),3)

    def test_welford_every_prefix_exact_centred_oracle(self):
        rng=random.Random(1801)
        for _ in range(200):
            values=[rng.randrange(-10,11) for _ in range(rng.randrange(1,20))];n=0;m=s=F(0)
            for i,x in enumerate(values):
                n+=1;delta=F(x)-m;m+=delta/n;s+=delta*(x-m)
                self.assertEqual((n,m,s),summary(values[:i+1]))
        n,m,s=summary([8,10,12,14]);self.assertEqual(s,20)
        self.assertEqual(s/n,5);self.assertEqual(s/(n-1),F(20,3));self.assertEqual(QUESTIONS['q_l18_e1']['answer'],20)

    def test_tie_indices_exhaustive_direct_window_oracle(self):
        for n in range(7):
            for values in itertools.product((-1,0,1),repeat=n):
                for k in range(1,n+2):
                    answers,counts=deque_trace(values,k)
                    self.assertEqual(answers,earliest_windows(values,k))
                    self.assertEqual(counts[0],n);self.assertLessEqual(counts[1],n);self.assertLessEqual(counts[2],min(k,n))
        self.assertEqual(earliest_windows([5,5,4,5],3),[0,1])
        self.assertEqual(earliest_windows([5,5,4,5,0],3),[0,1,3]);self.assertEqual(QUESTIONS['q_l18_e2']['answer'],1)

    def test_merge_exact_partition_associativity_empty_and_between(self):
        rng=random.Random(1802)
        for _ in range(200):
            data=[F(rng.randrange(-10,11),rng.randrange(1,5)) for _ in range(rng.randrange(20))]
            i=rng.randrange(len(data)+1);j=rng.randrange(i,len(data)+1)
            a,b,c=map(summary,(data[:i],data[i:j],data[j:]));expected=summary(data)
            self.assertEqual(merge(merge(a,b),c),expected);self.assertEqual(merge(a,merge(b,c)),expected)
            self.assertEqual(merge(a,b),merge(b,a))
        self.assertEqual(merge(summary([0,2]),summary([8,10,12])),(5,F(32,5),F(536,5)))
        self.assertEqual(summary([0,0,10,10]),(4,F(5),F(100)))
        self.assertEqual(merge(summary([0,2]),summary([2,4])),summary([0,2,2,4]))
        self.assertNotEqual(summary([0,2,2,4]),summary([0,2,4]))

    def test_remove_add_every_small_window_and_counterexample(self):
        for k in range(1,6):
            for window in itertools.product((-1,0,1),repeat=k):
                for x in (-1,0,1):
                    self.assertEqual(replace(summary(window),window[0],x),summary(window[1:]+(x,)))
        a=[0,1,2];b=list(reversed(a));self.assertEqual(summary(a),summary(b))
        self.assertEqual(summary(a[1:]+[3]),(3,F(2),F(2)))
        self.assertEqual(summary(b[1:]+[3]),(3,F(4,3),F(14,3)))

    def test_binary_state_bound_unique_continuations_and_recovery(self):
        for k in range(1,9):
            signatures=set()
            for bits in itertools.product((0,1),repeat=k):
                sums=[sum(bits[t:]) for t in range(k+1)]
                self.assertEqual(tuple(a-b for a,b in zip(sums,sums[1:])),bits)
                signatures.add(tuple(sums))
            self.assertEqual(len(signatures),2**k)
        self.assertIn('BIT lower bound',QUESTIONS['q_l18_h1']['followSolution'])

    def test_lazy_heap_correctness_does_not_bound_retained_size(self):
        rng=random.Random(1803)
        for _ in range(150):
            data=[rng.randrange(-4,5) for _ in range(rng.randrange(1,35))];k=rng.randrange(1,len(data)+2);heap=[];answers=[]
            for i,x in enumerate(data):
                heapq.heappush(heap,(-x,i))
                while heap and heap[0][1]<=i-k:heapq.heappop(heap)
                if i>=k-1:answers.append(heap[0][1])
            self.assertEqual(answers,earliest_windows(data,k))
        # Manual push counts swaps on the fixed-k increasing witness.
        heap=[];swaps=0;n=1024
        for i in range(n):
            item=(-i,i);heap.append(item);at=len(heap)-1
            while at and item<heap[(at-1)//2]:
                heap[at]=heap[(at-1)//2];at=(at-1)//2;swaps+=1
            heap[at]=item
            self.assertGreater(heap[0][1],i-2)
        self.assertEqual(len(heap),n);self.assertEqual(swaps,sum(i.bit_length()-1 for i in range(1,n+1)))

    def test_deque_total_work_and_expensive_individual_update(self):
        data=list(range(1000,0,-1))+[2000];k=1000
        answers,(pushes,pops,maximum,burst)=deque_trace(data,k)
        self.assertEqual(answers,earliest_windows(data,k));self.assertEqual(pushes,1001)
        self.assertEqual(maximum,k);self.assertEqual(burst,k);self.assertLessEqual(pops,pushes)
        constant=[7]*10000;answers,counts=deque_trace(constant,200)
        self.assertEqual(answers,list(range(9801)));self.assertEqual(counts[2],200)

    def test_reexpanded_boundary_needs_discarded_history(self):
        values=[10,1,2]
        retained_index=deque_trace(values,1)[0][-1]
        self.assertEqual(values[retained_index],2);self.assertEqual(max(values),10)
        self.assertIn('left boundary BACKWARD',QUESTIONS['q_l18_h2']['followup'])

    def test_prefix_code_exhaustive_negative_ties_limits_preservation(self):
        solve=reference('c_l18_easy')
        for n in range(8):
            for values in itertools.product((-2,-1,0),repeat=n):
                data=list(values);before=data.copy()
                expected=[min(range(i+1),key=lambda j:(-data[j],j)) for i in range(n)]
                self.assertEqual(solve(data),expected);self.assertEqual(data,before)
        self.assertEqual(solve([-10**9]*100000),[0]*100000)
        self.assertEqual(solve(list(range(100000))),list(range(100000)))
        self.assertEqual(solve(list(range(100000,0,-1))),[0]*100000)

    def test_retained_rolling_contracts_direct_oracles_and_chronology(self):
        mean=reference('c05');maximum=reference('c13');rng=random.Random(1804)
        for _ in range(300):
            data=[rng.randrange(-10,11) for _ in range(rng.randrange(50))];k=rng.randrange(1,60);before=data.copy()
            expected=[None if i<k else float(F(sum(data[i-k:i]),k)) for i in range(len(data))]
            for a,b in zip(mean(data,k),expected):
                if b is None:self.assertIsNone(a)
                else:self.assertAlmostEqual(a,b,places=12)
            self.assertEqual(maximum(data,k),[max(data[i-k+1:i+1]) for i in range(k-1,len(data))]);self.assertEqual(data,before)
        self.assertEqual(mean([2,4,8,10],2),[None,None,3,6])
        original=mean([2,4,8,10],2);changed=mean([2,4,999,10],2)
        self.assertEqual(original[:3],changed[:3]);self.assertNotEqual(original[3],changed[3])
        self.assertEqual(maximum(list(range(30000)),15000),list(range(14999,30000)))

    def test_actual_judge_and_full_official_debug_roundtrip(self):
        for id in ('c_l18_easy','c05','c13'):
            task=next(t for t in TASKS if t['id']==id);result=run(id,task['solution'])
            self.assertNotIn('error',result,id);self.assertEqual(result['passed'],result['total'],id)
            cases=task['samples']+task['tests'];copies=submission_cases(id)['cases']
            for original,copied in zip(cases,copies):
                self.assertEqual(parse_debug_cases(task,[copied]),[original])
                args=copy.deepcopy(original['args']);reference(id)(*args);self.assertEqual(args,original['args'])
            if id=='c13':
                size=len(copies[-1]['argumentsJSON'])+len(copies[-1]['expectedJSON'])
                self.assertGreater(size,200000);self.assertLessEqual(size,500000)
                debug=run(id,task['solution'],'debug',[copies[-1]])
                self.assertNotIn('error',debug);self.assertEqual(debug['passed'],1)

if __name__=='__main__':unittest.main()
