"""Independent small oracles and deterministic source bank for l31/l32."""
from itertools import combinations

def bounds_oracle(values,queries):return [[sum(x<q for x in values),sum(x<=q for x in values)] for q in queries]
def topk_oracle(values,k):return sorted(range(len(values)),key=lambda i:(-values[i],i))[:k]
def median_oracle(values,k):
    result=[]
    for start in range(len(values)-k+1):
        w=sorted(values[start:start+k]);result.append(w[(k-1)//2]+w[k//2])
    return result

def distance_oracle(n,edges,source,weighted=True):
    # Floyd-Warshall all-pairs closure, not frontier/heap traversal.
    d=[[0 if i==j else None for j in range(n)] for i in range(n)]
    for edge in edges:
        u,v=edge[:2];w=edge[2] if weighted else 1
        if d[u][v] is None or w<d[u][v]:d[u][v]=w
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][k] is not None and d[k][j] is not None:
                    candidate=d[i][k]+d[k][j]
                    if d[i][j] is None or candidate<d[i][j]:d[i][j]=candidate
    return d[source] if weighted else [-1 if v is None else v for v in d[source]]

def interval_oracle(jobs):
    # Exhaust all subsets, then compare the reverse sorted inclusion vector.
    # Prefer 0 at the latest differing sorted job: independent global form of
    # the declared skip-on-equality policy, not the reference's DP recurrence.
    order=sorted(range(len(jobs)),key=lambda i:(jobs[i][1],jobs[i][0],i));best_value=0;best_ids=[];best_key=(0,)*len(jobs)
    for bits in range(1<<len(jobs)):
        ids=[i for i in order if bits>>i&1]
        if any(jobs[a][1]>jobs[b][0] for a,b in zip(ids,ids[1:])):continue
        value=sum(jobs[i][2] for i in ids);key=tuple(int(bool(bits>>i&1)) for i in reversed(order))
        if value>best_value or value==best_value and key<best_key:best_value,best_ids,best_key=value,ids,key
    return [best_value,best_ids]

BOUND_SOURCE='''def solve(values, queries):
    result = []
    for target in queries:
        pair = []
        for upper in [False, True]:
            lo, hi = 0, len(values)
            while lo < hi:
                mid = (lo+hi)//2
                if values[mid] < target or upper and values[mid] == target:
                    lo = mid+1
                else:
                    hi = mid
            pair.append(lo)
        result.append(pair)
    return result'''
TOPK_SOURCE='''import heapq
def solve(values, k):
    if k == 0:
        return []
    heap = []
    for i,value in enumerate(values):
        key = (value,-i)
        if len(heap) < k:
            heapq.heappush(heap,key)
        elif key > heap[0]:
            heapq.heapreplace(heap,key)
    return [-negative_index for value,negative_index in sorted(heap,reverse=True)]'''
MEDIAN_SOURCE='''def solve(values, k):
    if k > len(values):
        return []
    vocabulary = sorted(set(values))
    coordinates = {value:i+1 for i,value in enumerate(vocabulary)}
    u = len(vocabulary)
    tree = [0]*(u+1)
    def update(j,delta):
        while j <= u:
            tree[j] += delta
            j += j & -j
    def select(rank):
        pos, accumulated = 0,0
        step = 1 << (u.bit_length()-1)
        while step:
            candidate = pos+step
            if candidate <= u and accumulated+tree[candidate] < rank:
                accumulated += tree[candidate]
                pos = candidate
            step //= 2
        return vocabulary[pos]
    result = []
    for i,value in enumerate(values):
        update(coordinates[value],1)
        if i >= k:
            update(coordinates[values[i-k]],-1)
        if i >= k-1:
            result.append(select((k+1)//2)+select((k+2)//2))
    return result'''
BFS_SOURCE='''from collections import deque
def solve(n, edges, source):
    adjacency = [[] for _ in range(n)]
    for u,v in edges:
        adjacency[u].append(v)
    distance = [-1]*n
    distance[source] = 0
    queue = deque([source])
    while queue:
        u = queue.popleft()
        for v in adjacency[u]:
            if distance[v] == -1:
                distance[v] = distance[u]+1
                queue.append(v)
    return distance'''
DIJKSTRA_SOURCE='''import heapq
def solve(n, edges, source):
    adjacency = [[] for _ in range(n)]
    for u,v,w in edges:
        adjacency[u].append((v,w))
    distance = [None]*n
    distance[source] = 0
    heap = [(0,source)]
    while heap:
        cost,u = heapq.heappop(heap)
        if cost != distance[u]:
            continue
        for v,w in adjacency[u]:
            candidate = cost+w
            if distance[v] is None or candidate < distance[v]:
                distance[v] = candidate
                heapq.heappush(heap,(candidate,v))
    return distance'''
INTERVAL_SOURCE='''from bisect import bisect_right
def solve(jobs):
    order = sorted(range(len(jobs)),key=lambda i:(jobs[i][1],jobs[i][0],i))
    ends = [jobs[i][1] for i in order]
    dp, predecessor, take = [0],[0]*len(jobs),[False]*len(jobs)
    for j,i in enumerate(order):
        start,end,value = jobs[i]
        p = bisect_right(ends,start,0,j)
        predecessor[j] = p
        candidate = value+dp[p]
        take[j] = candidate > dp[-1]
        dp.append(candidate if take[j] else dp[-1])
    selected = []
    j = len(order)
    while j:
        if take[j-1]:
            selected.append(order[j-1])
            j = predecessor[j-1]
        else:
            j -= 1
    selected.reverse()
    return [dp[-1],selected]'''

def add_coding(add,tasks):
    def put(l,s,title,level,prompt,signature,args,oracle,source,explanation,large=()):
        cases=[dict(args=a,expected=oracle(*a)) for a in args]+list(large)
        add(f'c_{l}_{s}',title,level,'Search and data structures' if l=='l31' else 'Graphs and dynamic programming',prompt,signature,cases[:1],cases[1:],source,explanation)
    put('l31','easy','Find both insertion boundaries','Easy',
      'values is a NONDECREASING integer array; queries is an arbitrary-order integer list. For each query q return [first index with value≥q, first index with value>q], using n for a missing boundary. Return pairs in query order. Indices are zero-based, equality occupies [lower,upper), and duplicates/empty arrays/empty queries are valid. 0≤n≤100000,0≤query_count≤2000,|values_i|,|q|≤1e9. Inputs are already sorted; do not sort or mutate them. O(query_count*log(n+1)) search work, O(query_count) output and O(1) auxiliary state per search; special empty outputs are constant work. A boundary can equal zero or n.',
      'def solve(values, queries):',[[[1,2,2,2,5,8,8,11],[2,8,3,11,12,-1]],[[],[0,1]],[[2,2,2],[1,2,3]],[[1,5],[]],[[0],[0,-1,1]]],bounds_oracle,BOUND_SOURCE,
      'Maintain [lo,hi): everything before lo is strictly smaller for lower bound (or ≤ for upper bound), everything at/after hi satisfies the desired comparison. At each midpoint keep equality on the correct side, strictly reducing the interval. Terminate at the insertion boundary, not the first equal midpoint. The two endpoints differ exactly by the number of matching records.',
      [dict(args=[[0]*30000+[1]*40000+[2]*30000,[-1,0,1,2,3]*400],expected=[[0,0],[0,30000],[30000,70000],[70000,100000],[100000,100000]]*400)])
    values=[i%101 for i in range(100000)];large_top=sorted(range(len(values)),key=lambda i:(-values[i],i))[:200]
    put('l31','medium','Retain top-k observations with stable ties','Medium',
      'Read integer values in original order. Return original indices of the k BEST records, ranked by value descending then original index ascending. Equal-valued records are separate observations. k is an integer with 0≤k≤min(n,200),0≤n≤100000,|value|≤1e9. k=0 and empty inputs return[]. Preserve inputs. Use a bounded heap of at most k keys, one stream pass and one final sort of the retained keys. O(n*log(k+1)+k*log(k+1)) comparison work, O(k) auxiliary and returned storage; handle k=0 directly. Do not sort the entire input to satisfy this implementation contract.',
      'def solve(values, k):',[[[7,2,7,3,7,4],2],[[5,5,5,5],3],[[-8,-2,-2,-9],2],[[],0],[[9,1],0],[[1,2,3],3]],topk_oracle,TOPK_SOURCE,
      'A min-heap key (value,−index) makes the root the worst retained record. Push until full; then replace only for a strictly larger key. Induction shows the retained set is exactly the best min(k,seen) observations under that total order. Sort only its k records descending by heap key; convert negative indices back. Later equal values cannot displace earlier ties.',[dict(args=[values,200],expected=large_top)])
    put('l31','hard','Select sliding medians from a frequency tree','Hard',
      'Return TWICE the median of each complete current-inclusive window of width k, in time order. For odd k this is twice the middle value; for even k it is the sum of the two middle sorted VALUES. Duplicates count separately. values is an integer array,0≤n≤100000,|value|≤1e9,k is a positive integer≤100000; k>n returns[]. This is a BATCH function: compress the distinct whole-array values in sorted order, maintain only active-window frequencies, and use a Fenwick tree with O(log(u+1)) rank selection by binary lifting, u=distinct count. Delete exactly one outgoing occurrence before selecting ranks. O(n*log(n+1)) total time including compression, O(u) auxiliary storage plus O(max(n−k+1,0)) output; dictionary lookup has expected constant cost. Do not claim O(k) online memory. Preserve inputs and return exact Python integers; doubled answers lie within±2e9. A sorted-window recomputation or linear scan over all distinct coordinates per rank does not meet this implementation contract.',
      'def solve(values, k):',[[[4,1,4,2,9,8],4],[[3,-1,3,-1,0],3],[[2,2,2,2],2],[[],1],[[1,2],3],[[-1000000000,1000000000],2],[[9,-3,5],1]],median_oracle,MEDIAN_SOURCE,
      'One-based tree[j] stores the count block ending at j of length lowbit(j). Updates touch containing blocks; rank selection consumes aligned blocks only while their accumulated count stays STRICTLY below the requested rank. Counts stay nonnegative because one active occurrence expires. Select ranks (k+1)//2 and (k+2)//2; map coordinates back to values and add them, avoiding float medians. Batch compression stores vocabulary, not just the current window.',
      [dict(args=[[7]*100000,500],expected=[14]*99501),dict(args=[list(range(12000)),6000],expected=[2*i+5999 for i in range(6001)])])
    put('l32','easy','Compute directed hop distances','Easy',
      'Vertices are0..n−1. edges contains DIRECTED [u,v] pairs; parallel edges and self-loops are allowed. Return minimum edge counts from source to every vertex in index order, with−1 for unreachable vertices and zero for source. 1≤n≤50000,0≤edge_count≤100000,source and endpoints are valid vertex IDs. No implicit reverse edges. Use BFS with an adjacency list and mark a vertex discovered when enqueuing it. O(n+edge_count) time and auxiliary/output space; preserve inputs.',
      'def solve(n, edges, source):',[[6,[[0,1],[0,2],[1,3],[2,3],[3,4],[5,4]],0],[1,[[0,0],[0,0]],0],[3,[[0,1],[0,1],[1,1]],0],[4,[[0,1],[1,2]],3]],lambda n,edges,source:distance_oracle(n,edges,source,False),BFS_SOURCE,
      'FIFO processes discovered vertices in nondecreasing hop layers. First discovery sets distance and enqueues once, so duplicate edges/self-loops cannot create repeated scans of a vertex. Each directed adjacency entry is scanned at most once from its reachable tail. Initialize every other distance to−1 and do not invent reverse reachability.',[dict(args=[50000,[[0,1]],0],expected=[0,1]+[-1]*49998)])
    put('l32','medium','Settle nonnegative costs with stale-entry checks','Medium',
      'Vertices are0..n−1. edges contains DIRECTED [u,v,weight] integer triples with 0≤weight≤1e9. Parallel edges, zero-weight cycles and self-loops are valid. Return minimum total costs from source to every vertex in index order; unreachable vertices are None and source costs zero. 1≤n≤50000,0≤edge_count≤100000,valid endpoint/source IDs. Use adjacency-list Dijkstra with a min-heap. Add entries only on strict improvements; skip popped entries whose cost is obsolete. Lazy duplicate-entry heap storage may be O(edge_count), so use O(n+edge_count) auxiliary/output space and O((n+edge_count)*log(n+edge_count+1)) work. Preserve inputs. Distances are exact integers below5e13, safely displayed as JSON numbers. Negative weights are outside this contract; do not silently treat BFS as a weighted solver.',
      'def solve(n, edges, source):',[[5,[[0,1,9],[0,2,1],[2,1,1],[1,3,1],[2,3,10],[3,4,0],[1,4,7]],0],[4,[[0,1,0],[1,0,0],[1,2,0],[0,2,8],[2,2,0]],0],[3,[[0,1,100],[0,1,2]],0],[1,[],0],[3,[[0,1,4]],2]],distance_oracle,DIJKSTRA_SOURCE,
      'Extract the minimum valid tentative cost. With nonnegative edges a later unsettled path cannot improve that settled distance. For each outgoing edge test cost+w against the current distance. A prior larger heap record is stale after improvement; discard it without scanning its outgoing edges again. Strict comparison prevents zero-cycle equal-distance re-enqueueing. None marks unreachable, never an arbitrary large finite distance.',
      [dict(args=[10000,[[i,i+1,1000000000] for i in range(9999)],0],expected=[i*1000000000 for i in range(10000)]),dict(args=[50000,[],49999],expected=[None]*49999+[0])])
    jobs=[[0,3,5],[1,2,3],[2,4,4],[3,5,5],[4,6,4],[5,7,4],[0,7,12]]
    put('l32','hard','Reconstruct a canonical weighted interval schedule','Hard',
      'jobs gives original-index [start,end,value] INTEGER records with start<end. Select pairwise nonoverlapping HALF-OPEN intervals; touching endpoints are compatible. Empty selection is allowed, and negative/zero values may be skipped. Sort jobs by (end,start,original_index). Let D[j] be optimal value in first j sorted records; for a take candidate use only the earlier prefix with end≤current start. At EVERY equality between skip and take, SKIP the current sorted record. Return [optimal_total_value, selected_original_index_list_in_chronological_order] for this exact canonical recurrence. It does not generally minimize number of jobs or lexicographic IDs as a separate objective. Duplicated intervals are distinct records; do not mutate input or return sorted positions instead of original indices. 0≤n≤50000,integer|start|,|end|≤1e6,|value|≤1e6. O(n log(n+1)) time, O(n) auxiliary/output space including reconstruction. Values remain within±5e10, safely represented in the UI. Use binary-searched predecessors and an iterative DP/reconstruction rather than exponential subsets or recursion depth proportional to n.',
      'def solve(jobs):',[[jobs],[jobs+[[0,7,14]]],[[]],[[[0,1,-2],[1,2,0]]],[[[0,2,5],[0,2,5],[2,3,4]]],[[[3,4,7],[0,1,3],[1,3,4]]]],interval_oracle,INTERVAL_SOURCE,
      'Sort stable identities by finishing time. For sorted position j (zero-based), bisect earlier ends only to obtain p=number of compatible prior jobs. The take value is weight+dp[p], skip is dp[j]. Record a take only when it is strictly larger; store p for reconstruction. Every feasible optimum either excludes j or includes it after a compatible prefix, proving the recurrence. Walk backward through recorded decisions and reverse the recovered original IDs. Empty/negative inputs follow dp[0]=0 without a special forced-choice policy.',
      [dict(args=[[[0,1,1]]*50000],expected=[1,[0]]),dict(args=[[[i,i+1,1] for i in range(10000)]],expected=[10000,list(range(10000))])])
