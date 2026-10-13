"""Six deterministic exercises. Expected cases use independent mathematical oracles."""
from fractions import Fraction as F
from math import log, exp, log1p, fsum

def weighted_oracle(rows,m,b):
    w=sum(F(v[2]) for v in rows)
    return [float(sum(F(weight)*(F(m)*F(x)+F(b)-F(y))*F(x) for x,y,weight in rows)/w),float(sum(F(weight)*(F(m)*F(x)+F(b)-F(y)) for x,y,weight in rows)/w)]

def recurrence_oracle(a,x0,inputs,targets):
    # Forward sensitivities, independently of the reverse-mode reference.
    a,x=F(a),F(x0); da=F(0); dx=F(1); du=[F(0)]*len(inputs)
    loss=ga=gx=F(0); gu=[F(0)]*len(inputs);n=len(inputs)
    for t,(u,y) in enumerate(zip(inputs,targets)):
        da=x+a*da; dx=a*dx;du=[a*v for v in du];du[t]+=1;x=a*x+F(u);r=x-F(y)
        loss+=r*r/(2*n);ga+=r*da/n;gx+=r*dx/n
        gu=[v+r*d/n for v,d in zip(gu,du)]
    return [float(loss),float(ga),float(gx),list(map(float,gu))]

def gd_oracle(curvatures,linear,start,step,iterations):
    # Closed-form geometric error, independent of the iterative solver.
    out=[float(-F(b)/F(a)+(1-F(step)*F(a))**iterations*(F(x)+F(b)/F(a))) for a,b,x in zip(curvatures,linear,start)]
    return [out,fsum(.5*a*x*x+b*x for a,b,x in zip(curvatures,linear,out))]

def armijo_oracle(h,b,x,alpha,c):
    g=[sum(F(h[i][j])*F(x[j]) for j in range(2))+F(b[i]) for i in range(2)]
    if g==[0,0]:return [x.copy(),0.,0]
    threshold=2*(1-F(c))*sum(v*v for v in g)/sum(g[i]*F(h[i][j])*g[j] for i in range(2) for j in range(2))
    alpha=F(alpha);k=0
    while alpha>threshold:alpha/=2;k+=1
    return [[float(F(x[i])-alpha*g[i]) for i in range(2)],float(alpha),k]

def box_oracle(h,b,bounds):
    # Enumerate active sets and check KKT signs, independently of face minimization.
    from itertools import product
    a,c,d=F(h[0][0]),F(h[0][1]),F(h[1][1]);b=list(map(F,b));bounds=[list(map(F,z)) for z in bounds]
    for states in product((-1,0,1),repeat=2):
        x=[None if s==0 else bounds[i][0 if s==-1 else 1] for i,s in enumerate(states)]
        if states==(0,0):x=[(-d*b[0]+c*b[1])/(a*d-c*c),(c*b[0]-a*b[1])/(a*d-c*c)]
        elif states[0]==0:x[0]=-(c*x[1]+b[0])/a
        elif states[1]==0:x[1]=-(c*x[0]+b[1])/d
        if not all(lo<=v<=hi for v,(lo,hi) in zip(x,bounds)):continue
        g=[a*x[0]+c*x[1]+b[0],c*x[0]+d*x[1]+b[1]]
        if not all(bounds[i][0]==bounds[i][1] or (g[i]==0 if s==0 else g[i]>=0 if s==-1 else g[i]<=0) for i,s in enumerate(states)):continue
        val=(a*x[0]**2+2*c*x[0]*x[1]+d*x[1]**2)/2+b[0]*x[0]+b[1]*x[1]
        return [float(x[0]),float(x[1]),float(val)]
    raise AssertionError('SPD box must have an optimum')

def add_coding(add,tasks):
    def cases(oracle,arguments):return [{'args':args,'expected':oracle(*args)} for args in arguments]
    add('c_l26_easy','Differentiate a weighted squared loss','Easy','Calculus',
      r'Given rows [x,y,weight], fit the affine prediction slope*x+intercept. Define \(\ell=\sum_i w_i(mx_i+b-y_i)^2/(2W)\), W=sum weights. Return [derivative_slope, derivative_intercept]. Inputs are finite; 1≤n≤2000, |x|,|y|,|slope|,|intercept|≤1000, 0≤weight≤1000 and W>0. Zero-weight rows have no influence. Use O(n) time and O(1) extra space; do not modify inputs.',
      'def solve(rows, slope, intercept):',
      [{'args':[[[0,1,1],[2,3,1]],1,0],'expected':[-1,-1]}],
      cases(weighted_oracle,[[[[2,5,3]],2,1],[[[1,2,1],[3,5,2],[-2,9,0]],1,1],[[[-3,2,4],[1,-5,.5]],-.5,2],[[[i%7,i%5,i%3] for i in range(2000)],.25,-2]]),
      'def solve(rows, slope, intercept):\n    w = gm = gb = 0.0\n    for x, y, weight in rows:\n        r = slope*x + intercept - y\n        w += weight\n        gm += weight*r*x\n        gb += weight*r\n    return [gm/w, gb/w]',
      r'One half cancels the outer square derivative. Each slope contribution contains x, while the intercept contribution does not. Normalize by total weight, not row count. A zero-weight row is irrelevant even if its residual is large. The loop takes O(n) time and O(1) auxiliary space. This differentiates the defined objective; it does not fit its optimum.')
    logcases=[{'args':[[[1,0]],0,0],'expected':[log(2),.5,.5]},
      {'args':[[[1,1],[-1,0]],1000,0],'expected':[0,0,0]},
      {'args':[[[1,0],[-1,1]],1000,0],'expected':[1000,1,0]},
      {'args':[[[0,1]],0,-1000],'expected':[1000,0,-1]},
      {'args':[[[0,0],[0,1]],0,0],'expected':[log(2),0,0]},
      {'args':[[[1,1]],0,log(3)],'expected':[log(4/3),-.25,-.25]},
      {'args':[[[2,0],[-2,1]],log(3)/2,0],'expected':[log(4),1.5,0]}]
    add('c_l26_medium','A logistic derivative that survives large scores','Medium','Calculus',
      r'Rows [x,y] have binary y∈{0,1}. With z=slope*x+intercept, define the MEAN loss \(\ell=n^{-1}\sum[\log(1+e^z)-yz]\). Return [loss, derivative_slope, derivative_intercept]. Do not overflow or subtract two large nearly equal terms. 1≤n≤2000, finite inputs |x|≤1000, |slope|,|intercept|≤1000 and |z|≤1000. O(n) time, O(1) auxiliary space; no simulation or external libraries. A predicted probability is sigmoid(z)=1/(1+exp(−z)); the target is held fixed.',
      'def solve(rows, slope, intercept):',logcases[:1],logcases[1:],
      'import math\ndef solve(rows, slope, intercept):\n    loss = gm = gb = 0.0\n    for x, y in rows:\n        z = slope*x + intercept\n        loss += max(z, 0.0) - y*z + math.log1p(math.exp(-abs(z)))\n        if z >= 0:\n            p = 1/(1+math.exp(-z))\n        else:\n            ez = math.exp(z)\n            p = ez/(1+ez)\n        r = p-y\n        gm += r*x\n        gb += r\n    n = len(rows)\n    return [loss/n, gm/n, gb/n]',
      r'Differentiate softplus to obtain sigmoid, so the score derivative is p−y. The affine chain rule multiplies it by x for the slope. Rewrite softplus as max(z,0)+log1p(exp(−|z|)); its exponent is never positive. For a correct confident label, cancellation occurs between exactly matching z terms before adding the small remainder. Branching sigmoid avoids exp(1000). This is algebraic stability, not a change in the objective. The outputs need not be a minimum.')
    add('c_l26_hard','Reverse derivatives through a shared recurrence','Hard','Calculus',
      r'Let x₀=x0 and \(x_t=a x_{t-1}+inputs[t-1]\), t=1,…,T. Define \(\ell=(2T)^{-1}\sum_t(x_t-targets[t-1])^2\). Return [loss, derivative_a, derivative_x0, derivative_inputs], with the final item a list in input order. a is SHARED at every time. 1≤T≤2000, lengths match, |a|≤0.99, |x0|,|inputs|,|targets|≤10; all finite. Use O(T) time, O(T) space and do not mutate inputs. Finite differences are too slow and inaccurate for this task.',
      'def solve(a, x0, inputs, targets):',[{'args':[.5,2,[1,0,-1],[0,0,0]],'expected':[.875,23/12,19/48,[19/24,.25,-1/6]]}],
      cases(recurrence_oracle,[[0,2,[1,-2,3],[0,1,-1]],[-.5,-1,[2,0,-2,1],[1,2,0,-1]],[.75,0,[1]*8,[.5]*8],[.5,3,[0],[1]],[.99,1,[0]*35,[1]*35]])+ [{'args':[0,2,[1]*2000,[0]*2000],'expected':[.5,2001/2000,0,[1/2000]*2000]}],
      'def solve(a, x0, inputs, targets):\n    states = [x0]\n    for u in inputs:\n        states.append(a*states[-1]+u)\n    n = len(inputs)\n    loss = sum((states[t+1]-targets[t])**2 for t in range(n))/(2*n)\n    adjoint = ga = 0.0\n    gu = [0.0]*n\n    for t in range(n-1, -1, -1):\n        adjoint = (states[t+1]-targets[t])/n + a*adjoint\n        gu[t] = adjoint\n        ga += adjoint*states[t]\n    return [loss, ga, a*adjoint, gu]',
      r'Forward states retain every local parameter input. Reverse adjoints add the direct residual/T and propagate the future adjoint through a. Every a occurrence contributes adjoint*previous_state, so sum across time. An input has local derivative one; x0 has local derivative a into the first state. O(T) time and space includes the returned sensitivity list. The tests use independent forward sensitivities, including negative a, zero a, a one-step computation and a long sequence.')
    add('c_l27_easy','Follow the exact quadratic updates','Easy','Optimization',
      r'Define \(f(\theta)=\tfrac12\sum_i curvatures_i\theta_i^2+\sum_i linear_i\theta_i\). Starting at start, take exactly iterations updates θ←θ−step*∇f(θ). Return [final_point, final_loss]. Positive curvatures, matching nonempty dimensions d≤100, 0≤iterations≤20, 0≤step≤2.5/max(curvatures); finite coefficients/start magnitudes≤20 and curvatures in [0.1,20]. The step need NOT converge. Do not stop early or change inputs. Aim for O(d*iterations) time or better, O(d) space.',
      'def solve(curvatures, linear, start, step, iterations):', [{'args':[[2,10],[0,0],[1,1],.25,1],'expected':[[.5,-1.5],11.5]}],
      cases(gd_oracle,[[[1,9],[0,0],[2,1],.2,6],[[2],[4],[-2],.5,4],[[2,4],[1,-2],[3,-1],0,20],[[2],[0],[3],1,4],[[.5,3],[-2,1],[0,0],.125,0],[[2,10],[0,0],[1,1],.25,20]]),
      'def solve(curvatures, linear, start, step, iterations):\n    point = list(start)\n    for _ in range(iterations):\n        point = [x-step*(a*x+b) for a,b,x in zip(curvatures,linear,point)]\n    loss = sum(.5*a*x*x+b*x for a,b,x in zip(curvatures,linear,point))\n    return [point,loss]',
      r'The gradient coordinate is aᵢθᵢ+bᵢ. Compute the requested finite trajectory, even when it oscillates or diverges. A closed-form check uses θ*ᵢ=−bᵢ/aᵢ and error multiplier (1−step*aᵢ)^iterations. A zero step or zero iterations leaves the input point unchanged. Distinguish simulation of a prescribed update rule from solving its optimization problem.')
    add('c_l27_medium','Implement one Armijo backtracking step','Medium','Optimization',
      r'For a symmetric positive-definite 2×2 hessian H, linear vector b and point x, let f(x)=xᵀHx/2+bᵀx and g=Hx+b. Starting at positive initial_step, halve α until f(x−αg)≤f(x)−armijo*α*||g||², with equality accepted. Return [new_point, accepted_step, halvings]. If g is exactly zero, return [a copy of point,0.0,0]. H entries are integers of magnitude≤100, point and linear entries are multiples of 1/4 with magnitude≤20, initial_step is a positive power of two between 1/16 and 16, and armijo is 1/4 or 1/2. Do not mutate inputs. You may use the exact quadratic equivalence α*gᵀHg≤2(1−armijo)||g||² to avoid subtracting similar losses.',
      'def solve(hessian, linear, point, initial_step, armijo):',[{'args':[[[4,1],[1,2]],[0,0],[1,1],1,.25],'expected':[[-.25,.25],.25,2]}],
      cases(armijo_oracle,[[[[2,0],[0,2]],[-2,4],[1,-2],1,.25],[[[2,0],[0,2]],[0,0],[1,0],.5,.5],[[[10,-3],[-3,2]],[1,-2],[.5,1],16,.25],[[[1,0],[0,1]],[0,0],[0,1],.0625,.25],[[[100,9],[9,1]],[-1,2],[1,-1],8,.5]]),
      'def solve(hessian, linear, point, initial_step, armijo):\n    g = [sum(hessian[i][j]*point[j] for j in range(2))+linear[i] for i in range(2)]\n    norm = sum(v*v for v in g)\n    if norm == 0:\n        return [list(point),0.0,0]\n    curvature = sum(g[i]*hessian[i][j]*g[j] for i in range(2) for j in range(2))\n    step = initial_step\n    halves = 0\n    while step*curvature > 2*(1-armijo)*norm:\n        step *= .5\n        halves += 1\n    return [[point[i]-step*g[i] for i in range(2)],step,halves]',
      r'Expand f(x−αg)=f(x)−α||g||²+α²gᵀHg/2. For α>0 this gives the stated equivalent comparison. Positive definiteness ensures positive directional curvature for nonzero g and a positive acceptance threshold, so halving terminates. Inputs were chosen to keep dyadic comparisons exact at equality in double precision. This returns one accepted step, not a globally optimal point. Runtime is proportional to the halving count in fixed dimension.')
    args=[[[[1,1],[1,2]],[-2,-3],[[0,2],[0,.5]]],[[[2,0],[0,4]],[-2,-4],[[-2,2],[-2,2]]],[[[2,-1],[-1,2]],[3,-5],[[0,1],[0,1]]],[[[5,2],[2,1]],[-7,3],[[-2,2],[1,1]]],[[[2,1],[1,3]],[-4,1],[[.5,.5],[-1,-1]]],[[[2,-1],[-1,2]],[0,0],[[-1,1],[-1,1]]],[[[100,9],[9,1]],[20,-10],[[-2,3],[-4,2]]]]
    add('c_l27_hard','Solve a coupled quadratic on a box','Hard','Optimization',
      r'Given symmetric positive-definite H=[[a,c],[c,d]], linear vector b, and bounds [[lo_x,hi_x],[lo_y,hi_y]], minimize f=xᵀHx/2+bᵀx on the CLOSED box. Return [optimal_x,optimal_y,minimum_value]. Integer H entries have magnitude≤1000, a,d>0 and ad−c²>0. Finite b and bounds have magnitude≤20; lo≤hi, including zero-width intervals. Do not modify inputs. Use an exact finite-candidate algorithm in dimension two, not iterative gradient descent, grids, or coordinate clipping of the unconstrained solution. No external libraries. Numerical output tolerance is 1e−7.',
      'def solve(hessian, linear, bounds):',[{'args':args[0],'expected':[1.5,.5,-19/8]}],cases(box_oracle,args[1:]),
      'def solve(hessian, linear, bounds):\n    a,c = hessian[0]\n    d = hessian[1][1]\n    b,e = linear\n    lx,hx = bounds[0]\n    ly,hy = bounds[1]\n    det = a*d-c*c\n    x,y = (c*e-d*b)/det,(c*b-a*e)/det\n    candidates = []\n    if lx <= x <= hx and ly <= y <= hy:\n        candidates.append((x,y))\n    for x in (lx,hx):\n        candidates.append((x,max(ly,min(hy,-(c*x+e)/d))))\n    for y in (ly,hy):\n        candidates.append((max(lx,min(hx,-(c*y+b)/a)),y))\n    def loss(z):\n        x,y = z\n        return .5*(a*x*x+2*c*x*y+d*y*y)+b*x+e*y\n    x,y = min(candidates,key=loss)\n    return [x,y,loss((x,y))]',
      r'Positive definiteness makes the objective strictly convex, while a nonempty closed bounded box guarantees existence. An interior minimum solves Hx=−b. On each boundary face, the remaining one-dimensional positive-curvature quadratic has its stationary point clamped to the allowed interval; its endpoint cases include corners. Compare these candidates. Any minimum is either interior or on a face, so the enumeration is complete and remains valid for line or point boxes. Constant time and space applies to this two-dimensional special case. Hidden expected outputs come from independent exact-rational active-set/KKT enumeration.')
