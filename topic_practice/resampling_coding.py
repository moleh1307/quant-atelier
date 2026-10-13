"""Deterministic resampling exercises: supplied draws, explicit quantiles, exact blocks."""
from fractions import Fraction as F
from math import sqrt
from itertools import product

def paired_oracle(rows,resamples):
    n=len(rows);d=[F(a)-F(b) for a,b in rows]
    return [float(sum(d)/n),[float(sum(d[i] for i in indices)/n) for indices in resamples]]

def interval_oracle(observed,replicates,alpha):
    xs=sorted(map(F,replicates));n=len(xs);mean=sum(xs)/n
    def q(p):
        location=(n-1)*p;j=location.numerator//location.denominator;w=location-j
        return xs[j]*(1-w)+xs[min(j+1,n-1)]*w
    lo,hi=q(F(alpha)/2),q(1-F(alpha)/2)
    return [float(mean-F(observed)),sqrt(float(sum((x-mean)**2 for x in xs)/(n-1))),[float(lo),float(hi)],[float(2*F(observed)-hi),float(2*F(observed)-lo)]]

def block_enumeration(values,length):
    n=len(values);q=(n+length-1)//length;means=[]
    for starts in product(range(n),repeat=q):
        indices=[(s+j)%n for s in starts for j in range(length)][:n]
        means.append(F(sum(values[i] for i in indices),n))
    mu=sum(means)/len(means)
    return float(sum((m-mu)**2 for m in means)/len(means))

def add_coding(add,tasks):
    arguments=[[[[1,2],[3,5],[2,1]],[[0,0,2],[1,2,1]]],[[[2,7]],[[0],[0]]],[[[1,2],[2,3],[4,5]],[[0,1,2],[2,2,0],[1,1,1]]],[[[-3,2],[2,-3]],[[0,0],[0,1],[1,1]]],[[[5,5],[5,5]],[[0,1],[1,1]]]]
    cases=[dict(args=a,expected=paired_oracle(*a)) for a in arguments]
    add('c_l28_easy','Keep both losses on the same resampled record','Easy','Resampling',
      r'Each row [loss_A,loss_B] is one matched record. resamples supplies B lists of exactly n record indices (zero-based, repetitions allowed). For EACH list use the SAME indices for both columns. Return [observed_mean_A_minus_B, replicate_mean_differences_in_given_order]. Do not draw additional random numbers or modify inputs. All losses are finite with magnitude≤1e6; 1≤n≤2000, B≥1 and total supplied indices≤100000. Indices are in [0,n−1]. O(n+Bn) time and O(B) returned space; no independently resampling the columns.',
      'def solve(rows, resamples):',cases[:1],cases[1:]+[{'args':[[[1,2],[3,5],[2,1]],[[0,1,2]]*1000],'expected':[-2/3,[-2/3]*1000]}],
      'import math\ndef solve(rows, resamples):\n    n = len(rows)\n    observed = math.fsum(a-b for a,b in rows)/n\n    results = [math.fsum(rows[i][0]-rows[i][1] for i in indices)/n for indices in resamples]\n    return [observed,results]',
      r'Derive the statistic on matched differences, then apply exactly the supplied record indices. Repeated indices repeat the whole pair. This preserves empirical covariance between the columns. Summing n residuals per replicate costs O(Bn), plus O(n) for the original estimate. The exercise deliberately supplies randomness so outputs are reproducible and grading checks the resampling logic rather than a particular pseudorandom generator.')
    arguments=[[10,[7,9,10,12,15],.2],[5,[5,5,5],.05],[0,[1,3],.5],[-2,[-7,-2,1,4],.1],[10,[15,7,12,9,10],.2],[1000,[999,1000,1001,1002,1003],.4]]
    cases=[dict(args=a,expected=interval_oracle(*a)) for a in arguments]
    add('c_l28_medium','Summarize bootstrap error with explicit interval rules','Medium','Resampling',
      r'Given original observed estimate, B≥2 finite bootstrap replicate estimates, and 0<alpha<1, return [estimated_bias, bootstrap_standard_error, percentile_interval, basic_interval]. Bias is replicate mean minus observed. Standard error is the SAMPLE standard deviation across replicates (denominator B−1), NOT that deviation divided by sqrt(B). For sorted replicates v define the p quantile by h=(B−1)p, j=floor(h), and linear interpolation between v[j] and v[min(j+1,B−1)] with weight h−j. Percentile endpoints use p=alpha/2 and 1−alpha/2; basic endpoints reflect those endpoints around observed, in increasing order. 2≤B≤100000; all estimate magnitudes≤1e6. Do not mutate input. O(B log B) time, O(B) space. Identical replicates return zero bias if they equal observed and zero standard error; no exact confidence-coverage claim is made.',
      'def solve(observed, replicates, alpha):',cases[:1],cases[1:],
      'import math\ndef solve(observed, replicates, alpha):\n    values = sorted(replicates)\n    n = len(values)\n    mean = math.fsum(values)/n\n    se = math.sqrt(math.fsum((x-mean)**2 for x in values)/(n-1))\n    def quantile(p):\n        h = (n-1)*p\n        j = int(h)\n        return values[j]+(h-j)*(values[min(j+1,n-1)]-values[j])\n    lo,hi = quantile(alpha/2),quantile(1-alpha/2)\n    return [mean-observed,se,[lo,hi],[2*observed-hi,2*observed-lo]]',
      r'The spread of replicate estimates approximates estimator uncertainty under the chosen bootstrap model. Dividing by √B instead measures the Monte Carlo error of estimating their conditional mean. A basic interval uses [2*observed−upper_quantile,2*observed−lower_quantile]; preserve the reflection and reversal. Explicit linear interpolation avoids library-specific quantile differences. Equal replicates define a degenerate conditional law, not proof of population certainty. Tests use independent rational interpolation/moments.')
    arguments=[[[0,0,10,10],2],[[0,0,10,10],3],[[1,3,8],2],[[4],1],[[2,2,2,2],3],[[-2,1,0,4],2],[[0,0,0,0,10,10,10,10],3]]
    cases=[dict(args=a,expected=block_enumeration(*a)) for a in arguments]
    add('c_l28_hard','Exact variance of a circular-block bootstrap mean','Hard','Resampling',
      r'Given n integer values and block_length ℓ, define this exact conditional resampling law: independently choose q=ceil(n/ℓ) start indices uniformly from 0,…,n−1. From each start s take ℓ consecutive values values[(s+j) mod n], j=0,…,ℓ−1. Concatenate blocks in their draw order, then TRUNCATE to exactly n values and compute their mean. Return the exact CONDITIONAL variance of that mean as a float, averaging all possible start choices analytically, not by simulation or enumerating n^q draws. 1≤n≤20000, |values[i]|≤1000, 1≤ℓ≤n. Use O(n) time, O(1) auxiliary space and do not mutate input. The last retained block may be shorter. ℓ=n yields zero variance, not a universally good inferential choice.',
      'def solve(values, block_length):',cases[:1],cases[1:]+[{'args':[[1000,-1000]*10000,10001],'expected':.005},{'args':[list(range(100))*200,20000],'expected':0}],
      'def solve(values, block_length):\n    n = len(values)\n    total = sum(values)\n    full = (n-1)//block_length\n    tail = n-full*block_length\n    def variance_numerator(size):\n        window = sum(values[j] for j in range(size))\n        squares = 0\n        for start in range(n):\n            squares += window*window\n            window += values[(start+size)%n]-values[start]\n        return n*squares-size*size*total*total\n    return (full*variance_numerator(block_length)+variance_numerator(tail))/(n**4)',
      r'Let S_s(k) be a circular window sum of length k. Its expectation over a uniform start is k times the original mean. Its variance is [n*ΣS_s(k)²−k²*(Σvalues)²]/n². The q−1 full retained blocks and one tail of length r=n−(q−1)ℓ have independent starts, so add their sum variances and divide by n² for the final mean. Two sliding-window scans calculate the needed sums of squares in O(n) time and O(1) auxiliary space. Integer arithmetic keeps the nonnegative variance numerator exact until the final division. Tiny cases are checked by direct enumeration of whole resampled sequences; the large alternating case has a separate analytic oracle. Handling the truncated tail and avoiding O(nℓ) work are the main transfer challenges.')
