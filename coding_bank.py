"""Original Python exercises with deterministic behavioural test cases."""
TASKS = []
def task(id, title, level, topic, prompt, signature, sample, tests, solution, explanation):
    TASKS.append(dict(id=id,title=title,difficulty=level,topic=topic,path='shared' if id in ['c01','c02','c03','c04','c05','c06'] else 'researcher',prompt=prompt,starter=signature+'\n    # Write your implementation here.\n    pass\n',samples=sample,tests=tests,solution=solution,explanation=explanation))

task('c01','Count pairs with a target sum','Easy','Algorithms',
     'Given a list of integers and a target, return the number of index pairs i < j whose values sum to target. Repeated values count as distinct observations. Aim for O(n) expected time. Do not modify the input.',
     'def solve(values, target):', [{'args':[[1,2,2,3],4],'expected':2}],
     [{'args':[[],0],'expected':0},{'args':[[2,2,2,2],4],'expected':6},{'args':[[-3,0,3,3],0],'expected':2},{'args':[list(range(20000)),19999],'expected':10000}],
     'def solve(values, target):\n    seen = {}\n    count = 0\n    for value in values:\n        count += seen.get(target - value, 0)\n        seen[value] = seen.get(value, 0) + 1\n    return count',
     'Count matches against previously seen values before inserting the current value. This prevents pairing an observation with itself and counts duplicates correctly. O(n) expected time, O(n) space.')
task('c02','Expected maximum of discrete draws','Medium','Probability',
     'Given a list of [value, probability] pairs (distinct values, nonnegative probabilities summing to one) and an integer draws >= 1, return the expected maximum of that many iid draws. Values may be negative and input order is arbitrary. Compute from the discrete CDF; do not simulate.',
     'def solve(distribution, draws):',[{'args':[[[1,0.5],[3,0.5]],2],'expected':2.5}],
     [{'args':[[[-4,1.0]],10],'expected':-4},{'args':[[[3,.2],[-2,.3],[1,.5]],1],'expected':.5},{'args':[[[1,.5],[3,.5]],3],'expected':2.75},{'args':[[[0,0],[5,1]],2],'expected':5}],
     'def solve(distribution, draws):\n    cumulative = previous = total = 0.0\n    for value, probability in sorted(distribution):\n        cumulative += probability\n        current = cumulative ** draws\n        total += value * (current - previous)\n        previous = current\n    return total',
     'P(max <= v)=F(v)^draws. Differences of consecutive CDF values give the probability mass at v. Sort the support first. O(m log m) time.')
task('c03','Expected wait for consecutive heads','Medium','Recurrences',
     'Return the expected number of flips to obtain k consecutive heads, where k >= 1 and 0 < p <= 1 is the head probability. Include all flips up to completion. Handle p=1 explicitly. Derive from trailing-head states rather than treating overlapping blocks as independent.',
     'def solve(k, p):',[{'args':[3,.5],'expected':14}],
     [{'args':[1,.25],'expected':4},{'args':[4,1],'expected':4},{'args':[2,.5],'expected':6},{'args':[6,.8],'expected':sum(.8**(-i) for i in range(1,7))}],
     'def solve(k, p):\n    return sum(p ** (-i) for i in range(1, k + 1))',
     'The recurrence solution is the sum p^(-1)+...+p^(-k), equivalent to (1-p^k)/((1-p)p^k) for p<1. The sum also handles p=1 without a singularity.')
task('c04','Streaming mean and sample variance','Medium','Statistics',
     'Return [mean, sample_variance] using Welford’s one-pass update. For an empty list return [None, None]; for one value return [value, None]. Use the n-1 denominator and do not round. Handle large offsets stably.',
     'def solve(values):',[{'args':[[1,2,3]],'expected':[2,1]}],
     [{'args':[[]],'expected':[None,None]},{'args':[[7]],'expected':[7,None]},{'args':[[4,4,4]],'expected':[4,0]},{'args':[[1000000000000+i for i in range(5)]],'expected':[1000000000002,2.5]}],
     'def solve(values):\n    n = 0\n    mean = m2 = 0.0\n    for value in values:\n        n += 1\n        delta = value - mean\n        mean += delta / n\n        m2 += delta * (value - mean)\n    if n == 0:\n        return [None, None]\n    return [mean, m2 / (n - 1) if n > 1 else None]',
     'Updating centred differences avoids subtracting two enormous nearly equal sums. O(n) time, O(1) auxiliary space.')
task('c05','Lagged rolling mean','Medium','Time-aware data',
     'For each index i, return the mean of the previous window observations values[i-window:i], excluding the current value. Return None until a full previous window exists. window >= 1. Aim for O(n) time.',
     'def solve(values, window):',[{'args':[[2,4,8,10],2],'expected':[None,None,3,6]}],
     [{'args':[[],2],'expected':[]},{'args':[[5],1],'expected':[None]},{'args':[[1,2,3],1],'expected':[None,1,2]},{'args':[[1,2],3],'expected':[None,None]},{'args':[[2,-2,2,-2,2],2],'expected':[None,None,0,0,0]}],
     'def solve(values, window):\n    result = []\n    total = 0.0\n    for i, value in enumerate(values):\n        result.append(total / window if i >= window else None)\n        total += value\n        if i >= window:\n            total -= values[i - window]\n    return result',
     'Emit the window value before adding the current observation. Then remove the oldest value for the next iteration. The chronology is the key invariant.')
task('c06','Join by availability time','Medium','Time-aware data',
     'Events are [available_at, value] pairs sorted by availability, not economic-event time. Decisions are sorted timestamps. At each decision return the latest event value with available_at <= decision, or None. For tied event timestamps, later input wins. Aim for O(events + decisions) time.',
     'def solve(events, decisions):',[{'args':[[[2,10],[5,20]],[1,2,4,5]],'expected':[None,10,10,20]}],
     [{'args':[[],[1,2]],'expected':[None,None]},{'args':[[[1,3]],[]],'expected':[]},{'args':[[[2,7],[2,8],[4,9]],[2,2,3,4]],'expected':[8,8,8,9]},{'args':[[[5,42]],[0,4,6]],'expected':[None,None,42]}],
     'def solve(events, decisions):\n    j = 0\n    latest = None\n    result = []\n    for timestamp in decisions:\n        while j < len(events) and events[j][0] <= timestamp:\n            latest = events[j][1]\n            j += 1\n        result.append(latest)\n    return result',
     'A forward pointer consumes every eligible event, including all ties. Never use a future release just because its economic timestamp precedes the decision.')
task('c07','OLS with an intercept','Medium','Regression',
     'Given equally sized x and y lists, return [intercept, slope] for ordinary least squares with an intercept. Return None for fewer than two observations or constant x. Do not use external numerical libraries.',
     'def solve(x, y):',[{'args':[[1,2,3],[3,5,7]],'expected':[1,2]}],
     [{'args':[[],[]],'expected':None},{'args':[[1],[4]],'expected':None},{'args':[[2,2,2],[1,4,7]],'expected':None},{'args':[[0,1,2],[2,1,0]],'expected':[2,-1]},{'args':[[-1,0,1],[2,0,2]],'expected':[4/3,0]}],
     'def solve(x, y):\n    if len(x) < 2:\n        return None\n    mx, my = sum(x) / len(x), sum(y) / len(y)\n    denominator = sum((v - mx) ** 2 for v in x)\n    if denominator == 0:\n        return None\n    slope = sum((a - mx) * (b - my) for a, b in zip(x, y)) / denominator\n    return [my - slope * mx, slope]',
     'Centre both variables and divide cross-deviation by x’s squared deviation. The intercept restores the means. Degenerate predictors cannot identify a unique slope.')
task('c08','Sample autocorrelation','Medium','Time series',
     'Given values and lag >= 1, return sum((x[i]-mean)*(x[i-lag]-mean), i=lag..n-1) / sum((x[i]-mean)^2, i=0..n-1). This explicitly uses the full-series mean and denominator. Return None if n <= lag or variance is zero.',
     'def solve(values, lag):',[{'args':[[1,2,3],1],'expected':0}],
     [{'args':[[1,2,3,4],1],'expected':.25},{'args':[[1,2],2],'expected':None},{'args':[[4,4,4],1],'expected':None},{'args':[[1,-1,1,-1],1],'expected':-.75}],
     'def solve(values, lag):\n    if len(values) <= lag:\n        return None\n    mean = sum(values) / len(values)\n    d = [v - mean for v in values]\n    denominator = sum(v * v for v in d)\n    if denominator == 0:\n        return None\n    return sum(d[i] * d[i-lag] for i in range(lag, len(d))) / denominator',
     'Different libraries normalise differently. Implement the stated estimator rather than importing an unspecified convention. O(n) time.')
task('c09','Purge overlapping target intervals','Medium','Validation',
     'Each training label is a half-open interval [start, end) with start < end. Return original indices whose intervals DO NOT overlap the half-open validation interval [vstart, vend). Touching endpoints do not overlap. Preserve input order. This tests interval purging only, not a complete deployment validation scheme.',
     'def solve(intervals, validation):',[{'args':[[[0,3],[2,5],[5,7]],[3,5]],'expected':[0,2]}],
     [{'args':[[],[1,2]],'expected':[]},{'args':[[[0,10],[3,4],[10,12]],[4,10]],'expected':[1,2]},{'args':[[[1,2],[2,3],[3,4]],[2,3]],'expected':[0,2]},{'args':[[[-5,-2],[-3,1]],[0,2]],'expected':[0]}],
     'def solve(intervals, validation):\n    start, end = validation\n    return [i for i, (a, b) in enumerate(intervals) if b <= start or a >= end]',
     'Overlap is a < validation_end and b > validation_start. Negate it carefully for half-open boundaries. Chronological train selection is a separate requirement.')
task('c10','Expanding walk-forward folds','Medium','Validation',
     'Return [[train_indices, test_indices], ...] for n chronologically ordered rows. First training block has initial rows. Leave gap unused rows before each test block of width step. Advance the training endpoint by step each fold. Include a final partial test block; stop when test start >= n. Inputs n >= 0, initial >= 1, step >= 1, gap >= 0.',
     'def solve(n, initial, step, gap):',[{'args':[8,3,2,1],'expected':[[[0,1,2],[4,5]],[[0,1,2,3,4],[6,7]]]}],
     [{'args':[3,3,2,0],'expected':[]},{'args':[6,2,3,0],'expected':[[[0,1],[2,3,4]],[[0,1,2,3,4],[5]]]},{'args':[7,2,2,2],'expected':[[[0,1],[4,5]],[[0,1,2,3],[6]]]}],
     'def solve(n, initial, step, gap):\n    result = []\n    end = initial\n    while end + gap < n:\n        result.append([list(range(end)), list(range(end + gap, min(n, end + gap + step)))])\n        end += step\n    return result',
     'The training endpoint expands; the gap sits between it and the test start. Time gaps alone do not guarantee purging for variable-length labels.')
task('c11','Lag a decision and charge turnover','Medium','Execution',
     'positions[i] is decided after return[i] is observed and takes effect for return[i+1]. Begin flat. For each period subtract cost * abs(new_held_position - previous_held_position). Return [period_net_pnl, total_net_pnl]. No terminal liquidation charge. Lists have equal length; returns are simple signed unit returns, positions unit exposures.',
     'def solve(positions, returns, cost):',[{'args':[[1,0,-1],[.1,.2,.3],.01],'expected':[[0,.19,-.01],.18]}],
     [{'args':[[],[],.01],'expected':[[],0]},{'args':[[10],[.5],.1],'expected':[[0],0]},{'args':[[1,-1,0],[0,.1,.2],.01],'expected':[[0,.09,-.22],-.13]},{'args':[[2,2,2],[.2,.1,-.1],0],'expected':[[0,.2,-.2],0]}],
     'def solve(positions, returns, cost):\n    pnl = []\n    held = 0\n    for i, value in enumerate(returns):\n        new_held = positions[i-1] if i else 0\n        pnl.append(new_held * value - cost * abs(new_held - held))\n        held = new_held\n    return [pnl, sum(pnl)]',
     'Lag the exposure before multiplying by the return. A direction reversal from +1 to -1 incurs two units of turnover. Specify liquidation and execution assumptions rather than silently inventing them.')
task('c12','A fixed control variate estimator','Medium','Simulation',
     'Given paired samples x and y, a known population mean mu_y and a coefficient beta fixed BEFORE sampling, return [estimate, standard_error] for z_i = x_i - beta*(y_i-mu_y). Use sample variance of z and sqrt(var/n). Return [None,None] for empty data; one pair returns [estimate,None].',
     'def solve(x, y, mu_y, beta):',[{'args':[[2,4,6],[1,2,3],2,2],'expected':[4,0]}],
     [{'args':[[],[],0,1],'expected':[None,None]},{'args':[[3],[1],0,1],'expected':[2,None]},{'args':[[1,3],[0,0],0,0],'expected':[2,1]},{'args':[[3,5,7],[1,2,3],2,2],'expected':[5,0]}],
     'import math\ndef solve(x, y, mu_y, beta):\n    z = [a - beta * (b - mu_y) for a, b in zip(x, y)]\n    n = len(z)\n    if not n:\n        return [None, None]\n    mean = sum(z) / n\n    if n == 1:\n        return [mean, None]\n    variance = sum((v - mean) ** 2 for v in z) / (n - 1)\n    return [mean, math.sqrt(variance / n)]',
     'A fixed coefficient preserves unbiasedness when mu_y is correct. Estimate uncertainty from the adjusted samples, not the raw x values. Independently pilot-fitted beta avoids same-sample fitting concerns.')
task('c13','Sliding-window maximum','Hard','Algorithms',
     'Return the maximum in each full contiguous window of width k, k >= 1. Return [] if k exceeds n. Aim for O(n) total time and O(k) auxiliary space using a monotone deque. Do not sort or scan each window.',
     'def solve(values, k):',[{'args':[[1,3,-1,-3,5,3,6,7],3],'expected':[3,3,5,5,6,7]}],
     [{'args':[[],1],'expected':[]},{'args':[[2,2,1,2],2],'expected':[2,2,2]},{'args':[[4,3,2,1],3],'expected':[4,3]},{'args':[[1,2],3],'expected':[]},{'args':[list(range(30000)),15000],'expected':list(range(14999,30000))}],
     'from collections import deque\ndef solve(values, k):\n    queue = deque()\n    result = []\n    for i, value in enumerate(values):\n        while queue and queue[0] <= i - k:\n            queue.popleft()\n        while queue and values[queue[-1]] <= value:\n            queue.pop()\n        queue.append(i)\n        if i >= k - 1:\n            result.append(values[queue[0]])\n    return result',
     'Store indices in decreasing value order. Evict expired indices and discard dominated ones. Each index is inserted and removed at most once. The large case discourages window scans, but a pass is not a formal complexity proof.')
task('c14','Brier score and calibration bins','Easy','Statistics',
     'Given probabilities in [0,1], binary outcomes, and bins >= 1, return {"brier": score, "bins": [[count, mean_forecast, observed_rate], ...]}. Equal-width bins are [j/bins,(j+1)/bins), with probability 1 in the final bin. Empty bins have [0,None,None]. Empty input has brier None.',
     'def solve(probabilities, outcomes, bins):',[{'args':[[0,.5,1],[0,1,1],2],'expected':{'brier':1/12,'bins':[[1,0,0],[2,.75,1]]}}],
     [{'args':[[],[],2],'expected':{'brier':None,'bins':[[0,None,None],[0,None,None]]}},{'args':[[1,0],[0,1],1],'expected':{'brier':1,'bins':[[2,.5,.5]]}},{'args':[[.25,.75],[0,1],4],'expected':{'brier':.0625,'bins':[[0,None,None],[1,.25,0],[0,None,None],[1,.75,1]]}}],
     'def solve(probabilities, outcomes, bins):\n    groups = [[] for _ in range(bins)]\n    for p, y in zip(probabilities, outcomes):\n        groups[min(int(p * bins), bins - 1)].append((p, y))\n    return {"brier": sum((p-y)**2 for p,y in zip(probabilities,outcomes)) / len(probabilities) if probabilities else None,\n            "bins": [[len(g), sum(p for p,y in g)/len(g), sum(y for p,y in g)/len(g)] if g else [0,None,None] for g in groups]}',
     'Handle p=1 as an explicit boundary. Brier is a proper score, while bin summaries are noisy diagnostics whose interpretation depends on counts.')

if __name__ == '__main__':
    import json
    from pathlib import Path
    from math_markup import math_text
    public = [{k:math_text(v) if k in {'prompt','explanation'} else v for k,v in t.items() if k != 'tests'} for t in TASKS]
    Path(__file__).parent.joinpath('static/coding.json').write_text(json.dumps(public,indent=2))
    print(f'{len(TASKS)} coding exercises')
