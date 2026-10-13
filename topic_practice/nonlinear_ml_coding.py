"""Deterministic nonlinear-model contracts with independent exact oracles."""
from fractions import Fraction as F
from .statistical_learning_coding import rational_solve

def leaf_oracle(ys,weights,groups,queries):
    ids=sorted(set(groups));means={g:sum(F(str(y))*w for y,w,h in zip(ys,weights,groups) if h==g)/sum(w for w,h in zip(weights,groups) if h==g) for g in ids}
    rss=sum(F(w)*(F(str(y))-means[g])**2 for y,w,g in zip(ys,weights,groups))
    return [[float(means[g]) for g in queries],float(rss)]

def stump_oracle(xs,ys,weights,min_leaf):
    # Enumerate subsets at every actual threshold and calculate residuals
    # directly; no prefix-statistic score formula from the reference.
    best=None
    for j in range(len(xs[0])):
        values=sorted(set(r[j] for r in xs))
        for a,b in zip(values,values[1:]):
            t=F(a+b,2);groups=[int(r[j]>t) for r in xs]
            if min(groups.count(0),groups.count(1))<min_leaf:continue
            # Direct rational residuals establish exact comparisons.
            means=[sum(F(y)*w for y,w,g in zip(ys,weights,groups) if g==h)/sum(w for w,g in zip(weights,groups) if g==h) for h in [0,1]]
            score=sum(w*(F(y)-means[g])**2 for y,w,g in zip(ys,weights,groups));key=(score,j,t)
            if best is None or key<best[0]:best=(key,[j,float(t),*map(float,means),float(score)])
    return best[1] if best else None

def kernel(x,z):return (1+sum(a*b for a,b in zip(x,z)))**2

def kernel_oracle(xs,ys,queries,penalty):
    # Direct leave-one-out REFITS of smaller exact rational systems; does not
    # use the reference's inverse diagonal shortcut or floating Cholesky.
    n=len(xs);lam=F(str(penalty))
    def fit(indices):return rational_solve([[F(kernel(xs[i],xs[j]))+(lam if i==j else 0) for j in indices] for i in indices],[F(ys[i]) for i in indices])
    alpha=fit(list(range(n)));pred=[sum(F(kernel(z,x))*a for x,a in zip(xs,alpha)) for z in queries];loo=[]
    for i in range(n):
        indices=[j for j in range(n) if j!=i];a=fit(indices);loo.append(sum(F(kernel(xs[i],xs[j]))*v for j,v in zip(indices,a)))
    mse=sum((F(y)-v)**2 for y,v in zip(ys,loo))/n
    return [list(map(float,pred)),list(map(float,loo)),float(mse)]

LEAF_SOLUTION='''import math
def solve(ys, weights, groups, query_groups):
    totals, sums = {}, {}
    for y,w,g in zip(ys,weights,groups):
        totals[g] = totals.get(g,0)+w
        sums[g] = sums.get(g,0)+w*y
    means = {g:sums[g]/totals[g] for g in totals}
    rss = math.fsum(w*(y-means[g])**2 for y,w,g in zip(ys,weights,groups))
    return [[means[g] for g in query_groups],rss]'''
STUMP_SOLUTION='''def solve(xs, ys, weights, min_leaf):
    n,p = len(xs),len(xs[0])
    total_w = sum(weights)
    total_s = sum(w*y for w,y in zip(weights,ys))
    total_q = sum(w*y*y for w,y in zip(weights,ys))
    best = None
    for j in range(p):
        order = sorted(range(n),key=lambda i:xs[i][j])
        w,s = 0,0
        for k,i in enumerate(order[:-1],1):
            w += weights[i]
            s += weights[i]*ys[i]
            a,b = xs[i][j],xs[order[k]][j]
            if a == b or k < min_leaf or n-k < min_leaf:
                continue
            rw,rs = total_w-w,total_s-s
            # RSS = numerator / denominator. Integer cross multiplication
            # gives exact comparisons and the stated tie rule without eps.
            numerator = total_q*w*rw-s*s*rw-rs*rs*w
            denominator = w*rw
            threshold = (a+b)/2
            if best is None or numerator*best[1] < best[0]*denominator:
                best = (numerator,denominator,j,threshold,s/w,rs/rw)
            # Feature then threshold are visited in ascending order.
    if best is None:
        return None
    num,den,j,t,left,right = best
    return [j,t,left,right,num/den]'''
KERNEL_SOLUTION='''import math
def solve(xs, ys, queries, penalty):
    n = len(xs)
    def kernel(x,z):
        return (1+sum(a*b for a,b in zip(x,z)))**2
    lower = [[0.0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1):
            v = kernel(xs[i],xs[j])+(penalty if i == j else 0)
            v -= math.fsum(lower[i][k]*lower[j][k] for k in range(j))
            lower[i][j] = math.sqrt(v) if i == j else v/lower[j][j]
    def forward(rhs):
        out = [0.0]*n
        for i in range(n):
            out[i] = (rhs[i]-math.fsum(lower[i][j]*out[j] for j in range(i)))/lower[i][i]
        return out
    u = forward(ys)
    alpha = [0.0]*n
    for i in range(n-1,-1,-1):
        alpha[i] = (u[i]-math.fsum(lower[j][i]*alpha[j] for j in range(i+1,n)))/lower[i][i]
    diagonal = []
    for i in range(n):
        unit = [0.0]*n
        unit[i] = 1.0
        column = forward(unit)
        diagonal.append(math.fsum(v*v for v in column))
    prediction = [math.fsum(kernel(z,x)*a for x,a in zip(xs,alpha)) for z in queries]
    loo = [y-a/d for y,a,d in zip(ys,alpha,diagonal)]
    mse = math.fsum((y-v)**2 for y,v in zip(ys,loo))/n
    return [prediction,loo,mse]'''

def add_coding(add,tasks):
    args=[[[0,2,4,8],[1,1,1,1],[0,0,1,1],[1,0,1]],[[1,3,10],[1,3,2],[-7,-7,4],[-7,4]],[[5],[2],[99],[99,99]],[[2,-2,7,1],[100,1,3,9],[8,8,2,2],[2,8]]]
    cases=[dict(args=a,expected=leaf_oracle(*a)) for a in args]
    cases.append(dict(args=[[1,-1]*50000,[1]*100000,[0,1]*50000,[0,1]],expected=[[1,-1],0]))
    add('c_l30_easy','Fit the values inside supplied leaves','Easy','Nonlinear machine learning',
      r'ys gives finite response values, weights POSITIVE INTEGER observation weights, groups supplied integer leaf IDs and query_groups requested EXISTING leaf IDs. Fit a separate constant in each group to minimize SUMMED weighted squared error. Return [query_predictions_in_order, total_weighted_RSS]. Group IDs need not be consecutive; queries may repeat. 1≤n≤100000, 1≤query_count≤100000, |y|≤100, 1≤weight≤100, |group|≤100000. Preserve inputs; O(n+query_count) expected time and O(number_of_groups+query_count) space. This fits a supplied partition; do not train a tree or choose a split.',
      'def solve(ys, weights, groups, query_groups):',cases[:1],cases[1:],LEAF_SOLUTION,
      r'Differentiate each group loss: its constant is sum(w*y)/sum(w). Accumulate group statistics, then compute RSS from actual weighted residuals and map requested IDs to means. The weighting belongs in BOTH fitting and scoring. Do not divide total RSS by n or sum(weights); those would be other outputs. A supplied partition can have one leaf or a singleton leaf.')
    args=[[[[0],[1],[3],[4]],[0,2,4,8],[1,1,1,1],1],[[[0,0],[0,1],[1,0],[1,1]],[1,-1,-1,1],[1]*4,1],[[[0],[0],[1],[2]],[0,10,1,2],[1,2,1,3],1],[[[0],[1],[2]],[2,1,0],[100,1,1],2],[[[1,2],[1,2]],[0,10],[1,1],1],[[[0,0],[1,1],[2,2],[3,3]],[2,2,2,2],[1,2,3,4],1],[[[0],[1],[2],[3]],[100,-100,3,4],[99,100,1,2],2]]
    cases=[dict(args=a,expected=stump_oracle(*a)) for a in args]
    # Max n, repeated integer features; exact zero score and earliest feature.
    large=[[[i%2]*8 for i in range(5000)],[3 if i%2 else -2 for i in range(5000)],[1]*5000,100]
    cases.append(dict(args=large,expected=[0,.5,-2,3,0]))
    add('c_l30_medium','Find a weighted regression stump without splitting ties','Medium','Nonlinear machine learning',
      r'xs is an integer n-by-p matrix, ys integer responses and weights positive integer observation weights. Search EVERY feature for a two-leaf split xs[i][j]≤threshold versus >threshold. Candidate thresholds are MIDPOINTS between adjacent DISTINCT observed feature values. Both children must contain at least min_leaf RECORDS (not total weight). Fit weighted response means and minimize total weighted RSS. Return [feature_index, threshold, left_mean, right_mean, total_RSS], or None if no valid split. Choose exact minimal RSS; exact ties choose smallest feature index then smallest threshold. Even a zero-gain split is eligible: no stopping criterion is requested. 1≤n≤5000,1≤p≤8, integer |x|,|y|≤100,1≤weight≤100,1≤min_leaf≤n. Preserve inputs. O(p*n*log(n)) time, O(n) auxiliary space; use sorting and prefix statistics. Compare rational scores exactly using integer cross-products, not arbitrary epsilon ties.',
      'def solve(xs, ys, weights, min_leaf):',cases[:1],cases[1:],STUMP_SOLUTION,
      r'Within each feature order, accumulate weight W and weighted response S. For a candidate with left/right summaries, RSS=Q−SL²/WL−SR²/WR, where Q=sum(w*y²). Equal feature values must remain together and record counts enforce min_leaf. Write RSS with integer numerator Q*WL*WR−SL²*WR−SR²*WL and denominator WL*WR, comparing scores by cross multiplication. Visit feature/threshold pairs in tie order and retain the first exact minimizer. Divide only for returned means/score. Finding a locally best root does not produce a globally best tree.')
    args=[[[[-1],[1]],[1,1],[[0],[2]],1],[[[1],[1]],[1,-1],[[1],[2]],1],[[[0,1],[1,0],[1,1],[2,-1]],[1,2,-1,3],[[0,0],[3,1]],.5],[[[0],[0],[1]],[2,5,-1],[],2],[[[2,-2],[2,-2],[2,-2]],[1,4,7],[[2,-2],[0,0]],.5]]
    cases=[dict(args=a,expected=kernel_oracle(*a)) for a in args]
    # Constant identical feature rows give a rank-one Gram of q*ones.
    n=70;q=169;ys=[(i%9)-4 for i in range(n)];lam=.5;total=sum(ys)
    loo=[q*(total-y)/(lam+q*(n-1)) for y in ys];pred=[q*total/(lam+q*n)]
    cases.append(dict(args=[[[2,-2,2]]*n,ys,[[2,-2,2]],lam],expected=[pred,loo,sum((y-v)**2 for y,v in zip(ys,loo))/n]))
    add('c_l30_hard','Kernel ridge and exact leave-one-out from one factorization','Hard','Nonlinear machine learning',
      r'Fit the FIXED polynomial kernel k(x,z)=(1+x·z)² using SUMMED half-squared data loss plus penalty/2 times squared feature-space norm. There is NO separately fitted intercept, centering, scaling or bandwidth tuning. xs has n training integer rows, ys their integer responses, queries m integer feature rows, and penalty>0. Return [query_prediction_list, leave_one_out_prediction_list_in_training_order, LOO_MSE]. A leave-one-out fit removes that record, but keeps the SAME summed-loss penalty and FIXED kernel. Use one Cholesky factorization of A=K+penalty*I; do not perform n smaller refits. Derive y_i−alpha_i/(A inverse)_ii for LOO predictions, where alpha solves A alpha=y. Obtain inverse diagonal entries from triangular solves, without forming a numerical inverse. 2≤n≤70,1≤p≤6,0≤m≤70, integer |x|≤2,|y|≤10,0.5≤penalty≤10. Duplicate rows and empty queries are valid. O(n³+n²*p+m*n*p) time and O(n²+m) space; standard library only, preserve inputs. These exact deletion predictions do not certify chronological eligibility or an unbiased post-tuning test score.',
      'def solve(xs, ys, queries, penalty):',cases[:1],cases[1:],KERNEL_SOLUTION,
      r'A is positive definite for positive penalty even when K is singular. Factor A=LLᵀ and solve for alpha. Block elimination of record i gives alpha_i=(y_i−k_i,minusᵀ A_minus inverse y_minus)/(A_ii−k_i,minusᵀ A_minus inverse k_i,minus); the reciprocal denominator is (A inverse)_ii, yielding the deletion identity. For unit vector e_i, (A inverse)_ii=||L inverse e_i||²: solve L v=e_i and sum v². Query prediction is k_queryᵀalpha. This is a fixed procedure with summed penalty, so removing a row leaves the smaller principal system unchanged. If average-loss lambda were fixed instead, the regularizer would change from n*lambda to (n−1)*lambda and this shortcut on the original matrix would not directly apply. Kernel/transform selection must remain inside outer training boundaries.')
