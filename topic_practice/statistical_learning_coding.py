"""Deterministic learning contracts and independently formulated exact oracles."""
from fractions import Fraction as F
from decimal import Decimal,localcontext

def diagonal_oracle(diagonal,cross,l1,l2):
    d=list(map(lambda x:F(str(x)),diagonal));z=list(map(lambda x:F(str(x)),cross));a,b=F(str(l1)),F(str(l2))
    return [float((max(abs(t)-a,0)*(1 if t>=0 else -1))/(v+b)) for v,t in zip(d,z)]

def logistic_oracle(xs,ys,weights,intercept,penalty):
    with localcontext() as ctx:
        ctx.prec=65;D=lambda x:Decimal(str(x));n=D(len(xs));b=list(map(D,weights));a=D(intercept);lam=D(penalty)
        loss=D(0);ga=D(0);gb=[D(0) for _ in b]
        for row,label in zip(xs,ys):
            z=a+sum((D(x)*w for x,w in zip(row,b)),D(0));p=D(1)/(D(1)+(-z).exp());res=p-D(label)
            # Direct high-precision likelihood expression, not the reference's
            # floating softplus branch. Decimal retains both tails at ±1000.
            loss+=(D(1)+z.exp()).ln()-D(label)*z;ga+=res
            for j,x in enumerate(row):gb[j]+=res*D(x)
        return [float(loss/n+lam*sum(w*w for w in b)/2),float(ga/n),[float(v/n+lam*w) for v,w in zip(gb,b)]]

def rational_solve(matrix,rhs):
    n=len(rhs);a=[list(row)+[v] for row,v in zip(matrix,rhs)]
    for j in range(n):
        k=next(i for i in range(j,n) if a[i][j]);a[j],a[k]=a[k],a[j];pivot=a[j][j];a[j]=[v/pivot for v in a[j]]
        for i in range(n):
            if i!=j:
                c=a[i][j];a[i]=[v-c*w for v,w in zip(a[i],a[j])]
    return [r[-1] for r in a]

def cv_oracle(xs,ys,folds,lambdas):
    # Solve in raw centered coordinates: a standardized ridge penalty is
    # lambda * sum(var_train_j * raw_slope_j²)/2. No square roots/Cholesky.
    p=len(xs[0]);scores=[F(0) for _ in lambdas];count=0
    for train,valid in folds:
        m=len(train);means=[sum(F(xs[i][j]) for i in train)/m for j in range(p)];ym=sum(F(ys[i]) for i in train)/m
        cov=[[sum((F(xs[i][j])-means[j])*(F(xs[i][k])-means[k]) for i in train)/m for k in range(p)] for j in range(p)]
        cross=[sum((F(xs[i][j])-means[j])*(F(ys[i])-ym) for i in train)/m for j in range(p)];active=[j for j in range(p) if cov[j][j]>0]
        for h,lam in enumerate(lambdas):
            lam=F(str(lam));mat=[[cov[j][k]+(lam*cov[j][j] if j==k else 0) for k in active] for j in active];coef=rational_solve(mat,[cross[j] for j in active]) if active else []
            for i in valid:
                pred=ym+sum((F(xs[i][j])-means[j])*b for j,b in zip(active,coef));scores[h]+=(F(ys[i])-pred)**2
        count+=len(valid)
    exact=[v/count for v in scores];minimum=min(exact);chosen=next(i for i,v in enumerate(exact) if v<=minimum+F(1,10**9));return [chosen,list(map(float,exact))]

DIAGONAL_SOLUTION='''def solve(diagonal, cross, lambda1, lambda2):
    return [(1 if z >= 0 else -1)*max(abs(z)-lambda1, 0)/(d+lambda2)
            for d,z in zip(diagonal,cross)]'''
LOGISTIC_SOLUTION='''import math
def solve(xs, ys, weights, intercept, penalty):
    n, p = len(xs), len(weights)
    losses, residuals = [], []
    for row,y in zip(xs,ys):
        z = intercept+math.fsum(x*w for x,w in zip(row,weights))
        losses.append(max(z,0)-y*z+math.log1p(math.exp(-abs(z))))
        if z >= 0:
            probability = 1/(1+math.exp(-z))
        else:
            ez = math.exp(z)
            probability = ez/(1+ez)
        residuals.append(probability-y)
    loss = math.fsum(losses)/n+penalty*math.fsum(w*w for w in weights)/2
    ga = math.fsum(residuals)/n
    gb = [math.fsum(r*row[j] for r,row in zip(residuals,xs))/n+penalty*weights[j]
          for j in range(p)]
    return [loss,ga,gb]'''
CV_SOLUTION='''import math
def solve(xs, ys, folds, lambdas):
    p = len(xs[0])
    scores = [0.0]*len(lambdas)
    count = 0
    for train,valid in folds:
        n = len(train)
        mean = [math.fsum(xs[i][j] for i in train)/n for j in range(p)]
        ym = math.fsum(ys[i] for i in train)/n
        scales = [math.sqrt(math.fsum((xs[i][j]-mean[j])**2 for i in train)/n) for j in range(p)]
        standardized = [[(xs[i][j]-mean[j])/scales[j] if scales[j] else 0.0
                         for j in range(p)] for i in train]
        gram = [[math.fsum(row[j]*row[k] for row in standardized)/n
                 for k in range(p)] for j in range(p)]
        cross = [math.fsum(row[j]*(ys[i]-ym) for row,i in zip(standardized,train))/n for j in range(p)]
        for h,lam in enumerate(lambdas):
            lower = [[0.0]*p for _ in range(p)]
            for j in range(p):
                for k in range(j+1):
                    v = gram[j][k]+(lam if j == k else 0)-math.fsum(lower[j][s]*lower[k][s] for s in range(k))
                    lower[j][k] = math.sqrt(v) if j == k else v/lower[k][k]
            forward = [0.0]*p
            for j in range(p):
                forward[j] = (cross[j]-math.fsum(lower[j][k]*forward[k] for k in range(j)))/lower[j][j]
            beta = [0.0]*p
            for j in range(p-1,-1,-1):
                beta[j] = (forward[j]-math.fsum(lower[k][j]*beta[k] for k in range(j+1,p)))/lower[j][j]
            for i in valid:
                prediction = ym+math.fsum(beta[j]*(xs[i][j]-mean[j])/scales[j] for j in range(p) if scales[j])
                scores[h] += (ys[i]-prediction)**2
        count += len(valid)
    scores = [s/count for s in scores]
    best = min(scores)
    chosen = next(i for i,s in enumerate(scores) if s <= best+1e-9)
    return [chosen,scores]'''

def add_coding(add,tasks):
    args=[[[1,2],[2,.8],.5,.5],[[1,1],[.5,-.5],.5,0],[[2,3,4],[-2,0,5],0,0],[[.1,10],[1,-3],2,5],[[1],[0],0,0]]
    cases=[dict(args=a,expected=diagonal_oracle(*a)) for a in args]
    add('c_l29_easy','Shrink or threshold an orthogonal quadratic','Easy','Statistical learning',
      r'The objective is \(\frac12\sum_j d_j b_j^2-\sum_j z_j b_j+\lambda_1\sum_j|b_j|+\frac{\lambda_2}2\sum_j b_j^2\). diagonal supplies d_j and cross supplies z_j. Return the unique minimizing coefficient list in the given order. Derive the zero-coordinate condition; do not solve by a numerical search. Arrays have equal length 1≤p≤100000, finite 0.1≤d_j≤1e6, |z_j|≤1e6 and 0≤lambda1,lambda2≤1e6. There is no intercept in this specified quadratic. O(p) time and O(p) returned space; do not modify inputs.',
      'def solve(diagonal, cross, lambda1, lambda2):',cases[:1],cases[1:]+[dict(args=[[1]*10000,[2,-2]*5000,1,1],expected=[.5,-.5]*5000)],DIAGONAL_SOLUTION,
      r'The objective separates into coordinates. At nonzero b the derivative is (d+lambda2)b−z+lambda1 sign(b); at zero, the subgradient contains zero exactly if |z|≤lambda1. Thus use soft threshold S(z,lambda1)/(d+lambda2). A positive d ensures uniqueness, including lambda2=0. Keep the half factors: replacing lambda1 with lambda1/2 solves another objective.')
    args=[[[[-1],[1]],[0,1],[0],0,.5],[[[1],[1]],[1,0],[1000],0,0],[[[1],[-1]],[1,0],[-1000],0,.1],[[[0,2],[1,-1],[-2,1]],[1,0,1],[.7,-.3],.2,.4],[[[0],[0]],[1,1],[2],-3,.5],[[[1]],[1],[0],1000,0]]
    cases=[dict(args=a,expected=logistic_oracle(*a)) for a in args]
    add('c_l29_medium','Evaluate a regularized logistic loss and gradient','Medium','Statistical learning',
      r'For rows xs, labels ys in {0,1}, slope weights, intercept a and nonnegative penalty lambda, return [average_penalized_log_loss, intercept_gradient, slope_gradient_list]. The objective is \(\frac1n\sum_i[\log(1+e^{a+x_i^Tb})-y_i(a+x_i^Tb)]+\frac\lambda2\|b\|^2\). DO NOT penalize the intercept. Compute an objective/gradient at the supplied coefficients, not an optimizer. Handle logits at ±1000 without overflow or log(0). Finite inputs: 1≤n≤10000, 1≤p≤20, n*p≤100000, |xs_ij|,|weights_j|,|intercept|≤1000, 0≤penalty≤100. O(np) time; preserve inputs. Loss and gradient are ordinary Python floats.',
      'def solve(xs, ys, weights, intercept, penalty):',cases[:1],cases[1:],LOGISTIC_SOLUTION,
      r'The derivative of one loss with respect to its logit is sigmoid(z)−y. Average this residual for the intercept, average residual*x for slopes, and add lambda*b only to slopes. Evaluate softplus(z)−yz as max(z,0)−yz+log1p(exp(−abs(z))); sigmoid uses a sign-dependent exponential. This keeps both extreme tails finite. Average data loss before adding the penalty, rather than averaging the penalty n times or using a summed-loss convention.')
    args=[[[[0],[2],[4]],[0,2,4],[[[0,1],[2]]],[.5,1]],[[[0,1],[1,2],[2,3],[3,4],[10,-2]],[1,3,5,7,-4],[[[0,1,2],[3]],[[1,2,3],[4]]],[.1,1,10]],[[[2,5],[2,5],[10,100]],[1,3,8],[[[0,1],[2]]],[.1,1,2]],[[[-1],[0],[1],[2],[8]],[2,0,2,4,-3],[[[0,1],[2]],[[1,2],[3,4]]],[.2,.5,2]],[[[0],[2],[4]],[1,1,1],[[[0,1],[2]]],[10,.1,1]],[[[0,1],[1,0],[2,-1],[3,-2]],[0,2,3,7],[[[0,1],[2,3]]],[.01,.1,1]]]
    cases=[dict(args=a,expected=cv_oracle(*a)) for a in args]
    # Duplicate-feature and varied-scale fixtures preserve a full-rank ridge
    # solve even when a fold's data Gram is singular.
    args_large=[[[i%9,(i%9)*2,7,(i%5)-2] for i in range(120)],[(i%9)*3-(i%5) for i in range(120)],[[list(range(60)),list(range(60,80))],[list(range(80)),list(range(80,120))]],[.01,.1,1,10]]
    cases.append(dict(args=args_large,expected=cv_oracle(*args_large)))
    # Maximum declared dimensions, repeated valid folds, exactly duplicate
    # standardized columns. The rank-one closed form is independent of Cholesky.
    large_lambdas=[100,50,20,10,5,2,1,.5,.2,.1,.05,.01]
    large_xs=[[(1 if i%2 else -1)*j for j in range(1,7)] for i in range(2000)]
    large_ys=[3 if i%2 else -1 for i in range(2000)]
    large_folds=[[list(range(1000)),list(range(1000,2000))] for _ in range(5)]
    cases.append(dict(args=[large_xs,large_ys,large_folds,large_lambdas],expected=[11,[float((2*F(str(lam))/(6+F(str(lam))))**2) for lam in large_lambdas]]))
    add('c_l29_hard','Tune ridge with fold-local transformations','Hard','Statistical learning',
      r'xs is an n-by-p integer feature matrix, ys an integer target list, folds a list of [training_indices,validation_indices], and lambdas an ordered list of POSITIVE candidates. In EACH fold compute feature means and standard deviations using ONLY its training rows, with variance denominator m (training size). A training-constant feature becomes zero for ALL rows in that fold, even if it varies in validation. Center training targets by their training mean. Fit an unpenalized intercept and ridge slopes minimizing average HALF-squared training loss plus lambda/2 times the squared standardized slopes. Predict validation targets using that same training transform and intercept. For each candidate, pool all validation squared errors and divide by the TOTAL validation appearances across folds; do not average fold MSEs equally. Return [selected_candidate_index, pooled_MSE_list_in_candidate_order]. Choose the FIRST candidate whose score is within 1e-9 of the minimum. Never use validation data for scaling, fitting or target centering. No final-test score is implied. Within a fold, unique training/validation index sets are nonempty and disjoint; training size≥2. Indices may recur in different folds and each validation appearance contributes once. 3≤n≤2000,1≤p≤6,1≤K≤5,1≤L≤12, integer input magnitudes≤100,0.01≤lambda≤100. Use O(sum_f(m_f*p²+L*(p³+v_f*p))) time; do not mutate inputs or require third-party libraries. The caller supplies eligible folds; this function does not certify chronology, purging or independence.',
      'def solve(xs, ys, folds, lambdas):',cases[:1],cases[1:],CV_SOLUTION,
      r'Fit preprocessing once per fold. Training centering and an unpenalized intercept give a=mean(y_train) in standardized coordinates. Build G=ZᵀZ/m and c=Zᵀ(y−mean_y)/m. Solve (G+lambda I)b=c by a factorization such as Cholesky; positive lambda makes the matrix positive definite even with duplicate/zero columns. Validation loss excludes the coefficient penalty. Accumulate error sums, then divide by total validation appearances so unequal folds receive the specified weights. Keep candidates in supplied order and apply the explicit tie tolerance. An independent oracle solves in raw centered coordinates with exact rational arithmetic and penalty lambda times training variance on each raw coefficient. Selecting on these folds still needs separate outer evaluation for the selected learning procedure.')
