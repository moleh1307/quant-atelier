"""Original practice about the information that existed at a decision.

Publication histories, selection and window endpoints are explicit contracts.
The legacy rolling-mean task remains available through its permanent bookmark.
"""


def add_questions(add, questions):
    next(q for q in questions if q['id']=='q44')['rubric'] = [
        'Reject the time-10:00:01 use of a feature that first arrives at 10:00:02.',
        'Specify an availability-based as-of join, explicit missing value, key and tie convention.',
        'Retain event/availability timestamps and distinguish a genuinely available event-time join from assumed availability.',
    ]
    def question(suffix, title, level, minutes, prompt, answer, hints, solution,
                 follow, follow_answer, rubric):
        add(f'q_l08_{suffix}', title, 'Time-aware data', level, 'shared',
            minutes, prompt, answer, hints, solution, follow, follow_answer, 'l08')
        questions[-1]['rubric'] = rubric
        for key in ('prompt','solution','followSolution'):
            questions[-1][key] = questions[-1][key].replace(r'\n\n', '\n\n')

    question('e1', 'Three seconds are not three records', 'Easy', 4,
        r'Five distinct observations have availability times [0,1,1,4,6] seconds and corresponding values [2,4,8,10,20]. Immediately before all observations at time 4 become available, a feature averages records available in the preceding three seconds: the interval \([1,4)\). What is the feature value? Equal-time observations are distinct records; neither is a replacement for the other.',
        6,
        ['Write the time interval before choosing records.',
         'A record at the lower endpoint is included; one at the upper endpoint is excluded.'],
        r'Only the two records at time 1 qualify. Their mean is \((4+8)/2=6\). The record at time 0 is too old, and the record at time 4 has not yet entered the information set. A three-second window does not mean the last three rows, and two distinct records at the same timestamp both count. There is no requirement to fill three records or insert zeros for missing seconds.',
        'Under the same rule, what is the feature immediately before time 6? What if the interval contains no records?',
        r'The interval is [3,6), containing only the time-4 value ten, so the mean is ten. An empty interval has no arithmetic mean; return an explicit missing result such as None rather than zero. The feature contract determines elapsed-time versus record-count windows and the missing-value rule.',
        ['Select both time-1 records and exclude both outside endpoints.',
         'Divide by the two eligible records, not by three seconds.',
         'Keep distinct equal-time observations separate.'])

    question('e2', 'The equality convention changes the snapshot', 'Easy', 4,
        r'A single feature stream has [available_at,value] records [[2,5],[4,7],[4,9]], sorted by availability. At a decision at time 4, every record with available_at<=4 is known, and a later input row wins tied availability timestamps. What value is selected? The timestamp and tie rules are guaranteed by this problem, rather than inferred from a coarse clock.',
        9,
        ['Consume every eligible update, including all exact-time ties.',
         'The last eligible row wins in this particular stream.'],
        r'All three records are eligible under the inclusive rule. The later of the two time-4 rows is value nine, so nine is selected. Stopping at the first tie would select seven; comparing with a strict inequality would select five. Neither alternative implements the stated contract.',
        'What value would a strictly-before rule select, and can a millisecond timestamp alone justify inclusive eligibility in a real log?',
        r'A strictly-before rule would use five. A coarse timestamp alone does not establish whether an update arrived before the decision within that timestamp bucket. A sequence key, receipt log or other ordering evidence must justify equality; a convenient join convention cannot supply missing historical ordering.',
        ['Include both exact-time records under the given rule.',
         'Apply later-input tie precedence to select nine.',
         'Distinguish the explicit assumption from historical ordering evidence.'])

    question('m1', 'A causal feature can be paired with a leaking sample', 'Medium', 9,
        r'At each decision, X is an already known fair bit and Y is a future fair bit independent of X. Predict Y=X. An analyst retains a row only if X=Y, a condition evaluated after Y arrives. On retained rows, what is \(P(Y=1\mid X=1,\mathrm{retained})\)? Compare it with the probability available at the decision, calculate the retention rate, and explain the reported accuracy.',
        1,
        ['Enumerate the four equally likely (X,Y) records.',
         'Row selection can use future information even when the feature does not.'],
        r'The original records 00, 01, 10 and 11 each have probability 1/4. The retained set is {00,11}, so its mass is 1/2. Given X=1 and retention, only 11 remains, hence the requested probability is one. At decision time, before learning the future-dependent retention event, independence gives \(P(Y=1\mid X=1)=1/2\). Predicting X has 50-percent accuracy on the original population but 100-percent accuracy on the selected rows. The feature itself is available; the evaluation population was selected using its future success. A causal feature join does not repair a leaking inclusion rule.',
        'Instead retain rows only when X=1. What accuracy does the same prediction have, and what limitation remains?',
        r'The prediction is now one on every retained row, and Y is still a fair independent bit, so accuracy is 1/2. This inclusion rule is available at the decision and does not select by future success. It changes the target population to X=1, however; performance on that population is not automatically a statement about all decisions.',
        ['Enumerate the retained joint records and obtain probability one.',
         'Compute half retention and contrast 100-percent selected accuracy with 50-percent deployable accuracy.',
         'Identify future-dependent inclusion as the source of leakage.'])

    question('h1', 'Final vintages do not identify the historical trade', 'Hard', 19,
        r'Two scalar measurements are first published at times 0 and 1. Their original values are unknown real numbers in [0,10]. Each is revised once at time 2; the stored final values are respectively 4 and 8. Decisions at times 1/4 and 5/4 use the most recently published measurement at that decision: choose position +1 if its original value is at least 5, and -1 otherwise. Their subsequently realised unit payoffs are respectively +1 and -1; total profit is the sum of position times payoff, without costs.\n\nDetermine the exact set of historical total profits consistent with the retained final table, and construct histories attaining it. Then suppose an independently documented rule limits each revision magnitude to at most 2. Determine the new exact set.\n\nFinally replace that per-measurement limit with a shared total revision budget \(|u-4|+|v-8|\leq B\), where u,v are the original values and B>=0 is known. Determine the profit set for every B, including exact boundary budgets. Explain what replaying final values by event time establishes.',
        None,
        ['Each original value can fall on either side of the threshold unless a revision constraint excludes it.',
         'For the extra constraint, intersect [final-2,final+2] with the allowed original range.',
         'A compatible history must keep the publication times and final table fixed.'],
        r'Let the original publications be u and v. Positions are \(s(u),s(v)\in\{-1,+1\}\), where s(z)=+1 exactly when z>=5. Total profit is \(s(u)-s(v)\). With only the range [0,10], all four position pairs are possible, giving the exact set {-2,0,2}. For example (u,v)=(2,8) gives -2, (2,2) gives 0, and (8,2) gives 2; all are later revised to the same stored (4,8) at time 2. Thus neither the historical positions nor profit are identified by that table.\n\nUnder the revision bound, u must lie in [2,6] and v in [6,10]. The second position is necessarily +1, but the first can be either sign. The exact set is now {-2,0}: (4,8) attains -2 and (6,6) attains 0, with both revisions within the bound. Replaying final (4,8) produces -2, which is merely one compatible counterfactual calculation; it does not prove the unavailable original first release was below five. A publication/vintage log would identify the historical inputs. The known final table and a stated revision bound can give an identified set, but not justify inventing a first-release value.\n\nUnder the shared budget, profit -2 is always possible at (4,8), costing zero. Profit zero first becomes possible at (5,8), costing one; the alternative both-sell branch costs strictly more than three and cannot improve that threshold. Profit +2 requires u>=5 and v<5, so \(|u-4|+|v-8|\geq1+(8-v)>4\). Its infimum cost four is not attained because v=5 selects +1. For every B>4, choose \(u=5,v=5-\epsilon\) with \(0<\epsilon\leq\min(1,(B-4)/2)\); this costs \(4+\epsilon\leq B\) and attains profit +2. Therefore the exact sets are {-2} for 0<=B<1, {-2,0} for 1<=B<=4, and {-2,0,2} for B>4. Checking the sum of revisions, rather than independent component bounds, is essential for these sharp budget thresholds.',
        'If the documented revision bound were one instead of two, would historical profit become identified? What is the largest symmetric revision bound that guarantees the original positions?',
        r'A bound of one gives u in [3,5] and v in [7,9]. Because equality at five chooses +1, u can still switch sign; profits remain {-2,0}. Every bound strictly below one forces u<5 and v>5 and hence profit -2. There is no largest admissible bound: its supremum is one, excluded by the threshold equality. Saying that a revision is small without checking the decision boundary does not establish stability.',
        ['Derive the discrete set {-2,0,2} and exhibit histories with the same final table.',
         'Use the component constraint to derive {-2,0}, then prove and attain the shared-budget thresholds at one and strictly above four.',
         'Separate a final-vintage replay from an identified historical decision and handle the threshold equality.'])

    question('h2', 'Characterize an implementation that cannot see the future', 'Hard', 22,
        r'For every n>=1, a deterministic batch transformation F_n maps a real input sequence of length n to n scalar-or-None features. Feature index i is emitted immediately before x_i is observed. One batch procedure evaluates F_n(x) in finite time when given n and x. All fixed parameters are public before the stream begins; no external data or random state is allowed.\n\nState a precise prefix condition on the whole family {F_n} that is necessary and sufficient for an online implementation to emit the same features at every index for every finite input, without knowing the final stream length. Prove both directions, give a batch transformation that violates it even though the raw observation used at index i is lagged, and explain the limit of testing only several changed future suffixes. Treat this as an information-dependence question: the online implementation may retain its entire past and need not run in constant time.',
        None,
        ['Compare different input lengths as well as different suffix values.',
         'For a sufficiency proof, define the emitted value using any one fixed artificial continuation.',
         'Lagging the raw observation does not ensure that its fitted normalization excludes future data.'],
        r'The condition is: for all n,m>=i+1 and all sequences x of length n and y of length m with \((x_0,\ldots,x_{i-1})=(y_0,\ldots,y_{i-1})\), \[F_n(x)_i=F_m(y)_i.\] Equality of an empty prefix at i=0 requires a common initial feature independent of current value, suffix and final length. Necessity follows because an online deterministic procedure has exactly the same available inputs and fixed parameters before index i in both streams; it must emit the same feature. For sufficiency, retain the observed prefix p of length i, append one fixed dummy value zero, and emit \(F_{i+1}(p\mathbin{\Vert}[0])_i\). The prefix condition makes this independent of the dummy and identical to the feature in any actual continuation, including every longer stream. This establishes information feasibility, not efficient memory or runtime.\n\nA violating family is F_n(x)_0=None and, for i>=1, \(F_n(x)_i=x_{i-1}-n^{-1}\sum_{j=0}^{n-1}x_j\). The selected raw observation is lagged, but its full-stream centering changes if future values or stream length change. For x=[1,3] and y=[1,103], the index-1 features are -1 and -51 despite identical known prefix [1]. A finite set of changed-suffix tests can falsify the universal condition, but cannot prove it for every real sequence and length. An invariant or dependence argument must cover all allowed inputs; adversarial tests support it rather than replace it.',
        'Is fitting a normalizer on a completed training period always forbidden? Can a family that satisfies the condition still be computationally impractical?',
        r'A normalizer fitted before the evaluated decision period may be an allowed fixed public parameter. The condition must compare streams under that same already fitted parameter, not pretend its fitting data belonged to a later information set. A prefix-causal family can still need a long history or expensive recomputation: the construction proves availability, not an O(1) state representation. Information leakage and algorithmic efficiency are separate questions.',
        ['Quantify prefix equality across both lengths and suffixes, excluding the current observation.',
         'Prove necessity from identical information and sufficiency by an artificial continuation.',
         'Give the lagged-but-globally-normalized counterexample and distinguish falsification from universal proof.'])


def add_coding(add, tasks):
    def exercise(level, title, prompt, signature, samples, tests, solution, explanation):
        add(f'c_l08_{level.lower()}', title, level, 'Time-aware data', prompt,
            signature, samples, tests, solution, explanation)
        tasks[-1].update(path='shared', lesson='l08')
        for key in ('prompt','explanation'):
            tasks[-1][key] = tasks[-1][key].replace(r'\n\n', '\n\n')

    exercise('Easy', 'Count records strictly before the current timestamp',
        r'times is a nondecreasing list of nonnegative integer availability timestamps. Each entry is a distinct observation, including repeated timestamps. For each input row at timestamp t, return the number of records with timestamps in \([t-h,t)\), where h is horizon. The decision happens before every record at time t arrives, so all records with that same timestamp are excluded, even if they occur earlier in the input list. horizon is a positive integer. There are at most 200000 timestamps, each at most 10^12; horizon<=10^12. Return a list of integer counts of the same length, without mutating times. Aim for O(n) time and O(1) auxiliary storage excluding output.',
        'def solve(times, horizon):',
        [{'args': [[0,1,1,4,6],3], 'expected': [0,1,1,2,1]},
         {'args': [[2,2,2],1], 'expected': [0,0,0]}],
        [{'args': [[],4], 'expected': []},
         {'args': [[0],1], 'expected': [0]},
         {'args': [[0,1,2,3],1], 'expected': [0,1,1,1]},
         {'args': [[0,0,1,1,2],1], 'expected': [0,0,2,2,2]},
         {'args': [[0,3,3,4],3], 'expected': [0,1,1,2]},
         {'args': [[0,100,100,101],1], 'expected': [0,0,0,2]},
         {'args': [[0,10**12,10**12],10**12], 'expected': [0,1,1]},
         {'args': [list(range(8000)),1234], 'expected': [min(i,1234) for i in range(8000)]}],
        '''def solve(times, horizon):
    first = before = 0
    result = []
    for timestamp in times:
        while before < len(times) and times[before] < timestamp:
            before += 1
        while first < before and times[first] < timestamp-horizon:
            first += 1
        result.append(before-first)
    return result''',
        r'The eligible records form a contiguous sorted slice. before is the first index whose timestamp is at least t, so it excludes the whole current-time group. first is the first unexpired record in that prefix, with timestamp at least t-horizon. The answer is before-first. Each pointer advances at most n times, including across repeated timestamps, giving O(n) time and O(1) auxiliary space. Merely using the current row index as the upper boundary would admit earlier rows at time t that the contract declares unavailable. The implementation reads the sorted timestamp array to locate boundaries but never uses future observation values; an online equivalent keeps counts of prior timestamp groups and removes expired groups. The missing feature mean in the interview question is not the same as this integer count: an empty interval has count zero.')

    exercise('Hard', 'Replay revisions, retractions and expiration by key',
        r'updates is an unsorted list of [available_at,sequence,key,event_at,value] records. sequence is a unique integer from 0 through 10^12 across all updates, key is a string of at most 32 characters, and value is an integer or None.\n\nTimes are integers with 0<=event_at<=available_at<=10^12. A record revises the measurement identified by (key,event_at); None retracts that measurement, while a later numeric revision can restore it. decisions is an unsorted list of [decision_at,key] pairs, with integer decision_at in [0,10^12]. At each decision, all releases with available_at<=decision_at are known, including all exact-time releases.\n\nProcess releases in increasing (available_at,sequence) order. For each measurement, its last eligible release determines its current value. Select the greatest event_at among that key’s currently nonretracted measurements in \([t-h,t]\), where t is decision_at and h is horizon, or None if no such measurement exists. Thus an old measurement revised later does not automatically outrank a newer event, and retracting the newest can reveal an older active measurement.\n\nRestore results to original decision order, preserve both inputs, and return one value or None per decision. horizon is an integer from 1 through 10^12; update/decision counts are at most 100000 each and numeric |value|<=10^9. Aim for \(O((U+D)\log(U+D+2))\) time and \(O(U+D)\) storage, where U and D are the update and decision counts, without scanning the entire publication history per decision.',
        'def solve(updates, decisions, horizon):',
        [{'args': [[[3,2,'A',2,20],[4,3,'A',0,9],[1,1,'A',0,5],
                    [5,4,'A',2,None],[6,5,'A',2,25]],
                   [[4,'A'],[2,'A'],[5,'A'],[6,'A'],[8,'A']],5],
          'expected': [20,5,9,25,None]},
         {'args': [[[2,2,'A',1,8],[2,1,'A',1,7],[2,3,'B',1,50]],
                   [[2,'A'],[2,'B'],[1,'A']],1], 'expected': [8,50,None]}],
        [{'args': [[],[[0,'A'],[9,'B']],3], 'expected': [None,None]},
         {'args': [[[0,1,'A',0,3]],[],2], 'expected': []},
         {'args': [[[1,1,'A',1,5],[2,2,'A',1,None]],[[1,'A'],[2,'A'],[3,'A']],4], 'expected': [5,None,None]},
         {'args': [[[2,1,'A',0,5],[2,2,'A',2,7],[2,3,'A',2,None],[2,4,'A',0,9]],[[2,'A'],[2,'A']],2], 'expected': [9,9]},
         {'args': [[[1,1,'A',1,0],[3,2,'A',1,-8]],[[2,'A'],[3,'A'],[4,'A']],2], 'expected': [0,-8,None]},
         {'args': [[[1,1,'A',0,1],[8,2,'A',0,999]],[[1,'A'],[8,'A']],3], 'expected': [1,None]},
         {'args': [[[3,1,'A',0,1],[3,2,'B',3,8],[4,3,'A',4,2]],[[4,'A'],[3,'A'],[4,'B'],[3,'C']],3], 'expected': [2,1,8,None]},
         {'args': [[[10**12,1,'A',10**12,7]],[[10**12,'A'],[0,'A']],1], 'expected': [7,None]},
         {'args': [[[i,i,'A',i,i] for i in range(1,1201)],
                   [[i,'A'] for i in range(1200,-1,-1)],1],
          'expected': list(range(1200,0,-1))+[None]}],
        '''import heapq
def solve(updates, decisions, horizon):
    releases = sorted(updates, key=lambda row: (row[0],row[1]))
    ordered = sorted(enumerate(decisions), key=lambda item: item[1][0])
    latest = {}
    heaps = {}
    result = [None]*len(decisions)
    cursor = 0
    for index, (timestamp,key) in ordered:
        while cursor < len(releases) and releases[cursor][0] <= timestamp:
            available,sequence,stream,event,value = releases[cursor]
            latest[(stream,event)] = (sequence,value)
            if value is not None:
                heapq.heappush(heaps.setdefault(stream,[]),(-event,sequence,value))
            cursor += 1
        heap = heaps.get(key,[])
        while heap:
            negative_event,sequence,value = heap[0]
            event = -negative_event
            if event < timestamp-horizon or latest[(key,event)] != (sequence,value):
                heapq.heappop(heap)
            else:
                result[index] = value
                break
    return result''',
        r'Sort publication records by their information order, and sort indexed decisions by time. Before answering each decision, consume every eligible release. latest[(key,event)] stores the version that actually existed at this decision; this is separate from ranking events by economic time. Per-key heaps prioritize the greatest event_at. Numeric releases push candidates; retractions update the version map without pushing. Lazily discard a candidate if its version has been replaced/retracted, or if its event is below the inclusive expiration boundary. A newer publication of an older event cannot jump ahead of a newer active event. A retraction invalidates its old candidate and lets the heap reveal the next eligible event. A later numeric revision restores a measurement, provided its event remains in the window. Zero is a real value, not a missing flag. Since event_at<=available_at<=decision_at for consumed releases, no upper-window check is missing. Every candidate is pushed and popped at most once; sorting and heap work are O((U+D) log(U+D+2)), with O(U+D) stored records including output. Restore output using the original decision indices. After processing one decision, later releases change the mutable version map for later decisions only: earlier scalar results are already captured.\n\nThe independent reference should instead filter eligible releases, rebuild versions and scan active events separately for each decision; that slower model is useful for small cases. A final-vintage table or one last value per key loses information required by this contract.')
