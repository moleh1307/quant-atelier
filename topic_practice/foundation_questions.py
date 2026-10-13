"""Authored transfer questions: probability records, conditioning, expectation.

Retained assessments receive separate editorial review in original_review.py.
Every new written task has a
specific rubric; numeric tasks also provide derivation criteria and follow-ups.
"""


def add_foundation_questions(add, questions):
    def question(lesson, suffix, title, level, minutes, prompt, answer,
                 hints, solution, follow, follow_answer, rubric):
        topics = {'l01': 'Counting', 'l02': 'Conditioning', 'l03': 'Expectation'}
        add(f'q_{lesson}_{suffix}', title, topics[lesson], level, 'shared',
            minutes, prompt, answer, hints, solution, follow, follow_answer, lesson)
        questions[-1]['rubric'] = rubric

    question('l01', 'm1', 'The same pairs, different weights', 'Medium', 8,
        r'Three distinct balls are labelled A, B and C. Procedure I draws twice independently and uniformly with replacement, then erases the order. Procedure II chooses uniformly from the six unordered multisets AA, AB, AC, BB, BC, CC. Do these procedures have the same distribution? Give every outcome its probability under each procedure, and find the probability of two different labels under each. Explain why listing six possible records is insufficient.',
        None,
        ['Start from the nine equally likely ordered records in Procedure I.',
         'AB can come from AB or BA, while AA has only one preimage.'],
        r'Under I, AA, BB and CC each have probability \(1/9\); AB, AC and BC each have probability \(2/9\). Erasing order combines records but keeps their probability mass. Thus different labels have probability \(6/9=2/3\). Under II all six records have probability \(1/6\), so different labels have probability \(3/6=1/2\). The same support does not imply the same measure. A counting denominator is justified only when the records being counted have equal weights.',
        'Change Procedure I to drawing without replacement. What happens?',
        r'There are six equally likely ordered records, with no AA, BB or CC. Each of AB, AC and BC now has exactly two preimages, so each unordered pair has probability \(1/3\). Equal-size groups preserve uniformity; replacement changed the group sizes.',
        ['Assign 1/9 to repeated-label and 2/9 to distinct-label records under I.',
         'Assign 1/6 to all six records under II and derive 2/3 versus 1/2.',
         'Explain uniformity through preimage sizes, rather than the number of possible records.'])

    question('l01', 'm2', 'Exactly two colours', 'Medium', 8,
        r'An urn contains 12 distinguishable balls: 5 red, 4 blue and 3 green. Draw three uniformly without replacement; ignore draw order. What is the probability that exactly two different colours appear? Explain your sample space and avoid counting a three-colour draw as a two-colour draw.',
        29/44,
        [r'Every physical three-ball subset has probability \(1/\binom{12}{3}\).',
         'Subtract the one-colour and three-colour subsets from all subsets.'],
        r'There are \(\binom{12}{3}=220\) equally likely subsets. One-colour subsets number \(\binom53+\binom43+\binom33=15\). Three-colour subsets number \(5\cdot4\cdot3=60\). The categories are disjoint and exhaustive, so exactly two colours account for \(220-15-60=145\) subsets and probability \(145/220=29/44\). Counting one red-blue pair within each draw instead would give different multiplicities to different draws.',
        'If balls of a given colour look identical, may you instead count colour multisets uniformly?',
        r'No. RRR has \(\binom53=10\) physical preimages, while RRB has \(\binom52\cdot4=40\). Observational indistinguishability does not make those records equally probable.',
        ['Identify uniform physical subsets and the denominator 220.',
         'Partition into one, two and three colours with counts 15, 145 and 60.',
         'Explain why colour records have unequal physical multiplicities.'])

    question('l01', 'h1', 'A conditional multiset is still weighted', 'Hard', 14,
        r'Five draws are made independently and uniformly with replacement from five labelled balls. Given that exactly three different labels were seen, what is the probability that their multiplicities are 3, 1, 1 rather than 2, 2, 1? Derive the conditional denominator from ordered draw records. Do not assume the possible multiplicity patterns are equally likely.',
        2/5,
        ['Once three labels appear in five draws, the only partitions are (3,1,1) and (2,2,1).',
         'Choose the three labels, choose which label has the exceptional multiplicity, then arrange the five draws.',
         r'The arrangement counts are \(5!/3!\) and \(5!/(2!2!)\).'],
        r'All \(5^5\) ordered records initially have equal probability. Fix a set of three labels. For (3,1,1), choose the tripled label in 3 ways and arrange in \(5!/3!=20\) ways, giving 60 records. For (2,2,1), choose the singleton in 3 ways and arrange in \(5!/(2!2!)=30\) ways, giving 90. There are \(\binom53\) choices of labels for either pattern. Conditioning retains \(\binom53(60+90)\) records, hence the required probability is \(60/150=2/5\). Both the chosen-label factor and the original \(5^{-5}\) probability cancel.',
        'What if a machine instead selects uniformly among unordered size-five multisets with exactly three labels?',
        r'For each three-label set there are three multisets of each pattern, so that machine gives probability \(1/2\). It implements a different sampling rule. The word “unordered” describes the record, not its probability.',
        ['Show that only the two stated multiplicity partitions remain.',
         'Count 60 and 90 ordered records per chosen three-label set.',
         'Normalise after conditioning and distinguish a uniform-multiset sampler.'])

    question('l01', 'h2', 'One fixed point, not six independent matches', 'Hard', 16,
        r'Six researchers have six individually labelled notebooks. A uniformly chosen permutation assigns one notebook to each researcher. What is the probability that exactly one researcher receives their own notebook? Derive your count; notebook matches are not independent Bernoulli trials.',
        11/30,
        ['Choose the sole fixed point, then count permutations of the other five with no fixed points.',
         'Use inclusion–exclusion for the derangement count; forbidding one match changes the other possible matches.'],
        r'Choose the fixed researcher in 6 ways. The remaining five notebooks must form a derangement. Inclusion–exclusion gives \[D_5=5!-\binom51 4!+\binom52 3!-\binom53 2!+\binom54 1!-\binom55 0!=44.\] Therefore \(6D_5/6!=264/720=11/30\). The expression \(6(1/6)(5/6)^5\) would require independent matches, which a permutation does not provide. For instance, exactly five fixed points is impossible: the last notebook must then also match.',
        'For n researchers, express the probability of exactly r matches and identify an impossible value.',
        r'The probability is \(\binom nr D_{n-r}/n!\), where \(D_m=m!\sum_{j=0}^m(-1)^j/j!\), including \(D_0=1\) and \(D_1=0\). Thus exactly \(n-1\) matches is impossible. For fixed r and growing n the probability tends to \(e^{-1}/r!\); this limiting statement follows from the alternating exponential series, not independence.',
        ['Count permutations, rather than independent notebook assignments.',
         'Derive D5=44 with inclusion–exclusion and probability 11/30.',
         'Use the impossible five-match outcome to expose the independence shortcut.'])

    question('l02', 'e1', 'After the first red', 'Easy', 4,
        r'An urn has 4 red and 4 blue distinguishable balls. Two are drawn uniformly without replacement. Given that the first ball was red, what is the probability that the second is blue?',
        4/7,
        ['Describe what remains after the observed first draw.',
         'The second draw is uniform over the seven remaining physical balls.'],
        r'The observation leaves seven balls: three red and four blue. The next draw is uniform over these seven, so \(P(B_2\mid R_1)=4/7\). The original blue fraction \(4/8\) is the unconditional probability for either position; conditioning changes the information and the remaining urn.',
        'Are the two colour indicators independent?',
        r'No. The conditional blue probability is \(4/7\), different from its unconditional probability \(1/2\). With replacement the urn would not change and these draws would be independent.',
        ['Update the remaining counts to 3 red and 4 blue.',
         'Use denominator 7 and distinguish a conditional from an unconditional probability.'])

    question('l02', 'm1', 'Predict the next flip of the same coin', 'Medium', 9,
        r'A coin is selected once, with equal prior probability from two coins whose head probabilities are 1/4 and 3/4. All flips of a selected coin are conditionally independent. You see a head on the first flip. What is the probability of a head on the second flip of that same coin?',
        5/8,
        ['Update the probabilities of the two coins after the first head.',
         'Average the next-head probabilities using the posterior, not the original prior.'],
        r'The first-head probability is \((1/2)(1/4)+(1/2)(3/4)=1/2\). Bayes gives posterior coin weights \(1/4\) and \(3/4\). The next-head probability is therefore \((1/4)(1/4)+(3/4)(3/4)=10/16=5/8\). Conditional independence given the selected coin does not imply independence after the coin identity is hidden. The first flip teaches us about a latent parameter shared by both flips.',
        'What changes if a new coin is independently selected before every flip?',
        r'The second coin selection then carries no information from the first head. The next-head probability stays \(1/2\). The distinction is whether the hidden parameter persists across observations.',
        ['Compute posterior coin weights 1/4 and 3/4.',
         'Form a posterior predictive mixture to obtain 5/8.',
         'Explain conditional independence versus marginal dependence.'])

    question('l02', 'h1', 'The report is part of the experiment', 'Hard', 14,
        r'A household has two children, with independent boy/girl labels, each equally likely. A reporting device says “a boy was observed”. It reports this with probability 1 for BB, with probability s for each of BG and GB, and with probability 0 for GG, where 0 < s <= 1. Derive the probability of BB given the report. Then compare (a) inspecting one uniformly chosen child and reporting only if that child is a boy, and (b) inspecting both and reporting whenever at least one is a boy. Can the words “a boy was observed” alone identify the answer?',
        None,
        ['Weight each household by the chance of this report from that household.',
         'The two reporting devices correspond to different values of s.'],
        r'Each household has prior mass \(1/4\). The report masses are \(1/4,s/4,s/4,0\), so \[P(BB\mid\text{report})=\frac{1}{1+2s}.\] A randomly inspected child gives \(s=1/2\), hence posterior \(1/2\). An at-least-one report gives \(s=1\), hence posterior \(1/3\). The same verbal evidence can arise through different likelihoods. Without a reporting mechanism, the posterior is not identified; quietly assuming uniformity among remaining households picks one mechanism without justification.',
        'If mixed households are more likely to send the report than BB households, can the posterior be below 1/3?',
        r'Yes. In the more general model let report probabilities be b for BB and s for each mixed household. Then the posterior is \(b/(b+2s)\), provided the report has positive probability. For example b=1/2 and s=1 gives 1/5. The original bound depended on fixing b=1.',
        ['Derive 1/(1+2s) by likelihood-weighting the four households.',
         'Identify s=1/2 and s=1 and obtain the two distinct posteriors.',
         'Explain why an unspecified observation mechanism does not identify a posterior.'])

    question('l02', 'h2', 'Two passes without an independence assumption', 'Hard', 18,
        r'A condition is present in 10% of a population. Two tests are applied to the same person. For each test separately, its pass probability is 4/5 if the condition is present and 1/5 if absent. Nothing is known about dependence between tests within either class. A person passes both. What is the smallest possible probability that the condition is present? Justify an attainable bound instead of assuming conditional independence.',
        1/4,
        ['Let a and b be the probabilities of two passes within the present and absent classes.',
         r'For two events each of probability p, their intersection lies in \([\max(0,2p-1),p]\).',
         'The posterior increases with a and decreases with b.'],
        r'Within the present class, \(3/5\le a\le4/5\); within the absent class, \(0\le b\le1/5\). Bayes gives \(P(\text{present}\mid\text{both})=(a/10)/(a/10+9b/10)\). Its minimum uses a=3/5 and b=1/5, yielding \(0.06/(0.06+0.18)=1/4\). Attainability matters: in the present class use pass/pass, pass/fail, fail/pass, fail/fail probabilities (3/5,1/5,1/5,0); in the absent class use (1/5,0,0,4/5). Both preserve the specified single-test probabilities. Conditional independence would instead give a=16/25, b=1/25 and posterior 16/25, a conclusion the stated evidence does not justify.',
        'What is the largest possible posterior, and is it attainable?',
        r'It is 1: set b=0, with absent-class probabilities (0,1/5,1/5,3/5). Choose any feasible a, for example 3/5. A two-pass observation then has positive probability only in the present class. Thus the identified posterior interval is [1/4,1], much wider than one assumed-independence answer.',
        ['Bound the two within-class intersections using their marginal probabilities.',
         'Optimise Bayes over the feasible bounds to obtain 1/4.',
         'Construct feasible joint tables attaining the lower bound and explain the missing independence assumption.'])

    question('l03', 'e1', 'A sum without independent draws', 'Easy', 4,
        r'Three distinct numbered cards are drawn uniformly without replacement from cards labelled 1 through 8. What is the expected sum of the three labels? Explain why the dependence between draws does not prevent your calculation.',
        27/2,
        ['Each draw position has the same uniform marginal distribution on the eight labels.',
         'Find the mean label at one position, then add the three marginal means.'],
        r'Write the labels as \(X_1,X_2,X_3\). Each has mean \((1+8)/2=9/2\) by symmetry, even though they are dependent. Linearity gives \(E[X_1+X_2+X_3]=3(9/2)=27/2\). Independence is not an assumption of linearity; finite expectations suffice here.',
        'Would replacement change the expected sum?',
        r'No: it changes the joint distribution but leaves each marginal mean 9/2. It does change the variance of the sum. Equal expectations do not imply equal distributions.',
        ['Use the marginal mean 9/2 for each position.',
         'Apply linearity without claiming the draws are independent.'])

    question('l03', 'e2', 'Expected notebook matches', 'Easy', 5,
        r'Seven labelled notebooks are assigned to their seven owners by a uniform random permutation. What is the expected number of owners who receive their own notebook? Do not enumerate all permutations.',
        1,
        ['Use one indicator per owner and find its marginal match probability.',
         'An owner has probability 1/7 of a match; add expectations, not outcome guarantees.'],
        r'For owner i, let \(I_i\) indicate a correct match. Every notebook is equally likely to be assigned to that owner, so \(E[I_i]=1/7\). The count is \(\sum_i I_i\), hence its mean is \(7/7=1\). Indicators are dependent, but their expectations add. A mean of one does not mean exactly one match occurs in every assignment.',
        'For two distinct owners, what is the probability they both match, and does this imply independence?',
        r'It is \(5!/7!=1/(7\cdot6)=1/42\), whereas the product of the marginal probabilities is \(1/49\). Therefore they are not independent. The expected count calculation never required that product rule.',
        ['Define match indicators with marginal expectation 1/7.',
         'Sum to one and distinguish an average count from a guaranteed outcome.'])

    question('l03', 'h1', 'Count cycles without their joint distribution', 'Hard', 18,
        r'A permutation of six labelled objects is chosen uniformly. Decompose it into disjoint cycles, counting a fixed point as a one-element cycle. What is the expected total number of cycles? Derive the expected number of cycles of each length, rather than guessing independent cycle counts.',
        49/20,
        ['For each k-element subset, use an indicator that these elements form one cycle.',
         'A fixed subset can form (k-1)! directed cycles; the remaining elements can be permuted freely.'],
        r'For a fixed k-element subset, the number of permutations in which it forms one complete cycle is \((k-1)!(6-k)!\). There are \(\binom6k\) such subsets. Thus the expected number of k-cycles is \[\binom6k\frac{(k-1)!(6-k)!}{6!}=\frac1k.\] Summing lengths gives \(1+1/2+1/3+1/4+1/5+1/6=49/20\). Every cycle corresponds to exactly one subset and is counted once. Different subset indicators cannot be treated as independent: overlapping subsets cannot both be separate cycles.',
        'Derive the mean for n objects and explain why it grows much more slowly than n.',
        r'The same cancellation gives \(E[C_n]=\sum_{k=1}^n1/k\). Comparing this sum with the integral of 1/x shows logarithmic growth: \(\log(n+1)\le E[C_n]\le1+\log n\). Large permutations usually contain long cycles, not a linear number of small cycles.',
        ['Count cycles of a fixed subset as (k-1)! and permute the complement.',
         'Sum subset indicators to obtain 1/k for every cycle length.',
         'Sum the six contributions to 49/20 without assuming independent cycles.'])

    question('l03', 'h2', 'Crossings in a random matching', 'Hard', 17,
        r'Twenty distinct points lie on a circle. Choose uniformly from all perfect matchings of these points, and join each matched pair by a straight chord. Count crossing pairs of chords: a pair counts once if their interiors cross, even if another pair happens to cross at the same geometric point. What is the expected number of crossing pairs? Explain the symmetry behind the probability for one pair; do not assume crossings are independent.',
        15,
        ['Temporarily label the ten matched chords; labelling does not change the crossing count.',
         'Conditional on four endpoints, exactly one of their three pairings alternates around the circle.'],
        r'Label the ten chords uniformly after matching. Fix any two chord labels. Conditional on their four endpoints, symmetry makes the three ways to pair those endpoints equally likely: each leaves exactly the same number of matchings and chord labellings on the remaining points. In circular order a,b,c,d, only (a,c) with (b,d) crosses; the other two pairings do not. The crossing indicator therefore has mean 1/3. There are \(\binom{10}{2}=45\) labelled pairs, so linearity gives \(45/3=15\). Pairwise crossings share chords and need not be independent. The calculation counts crossing pairs, not distinct intersection locations.',
        'For 2n points, what is the expected number, and may the variance use 45 independent Bernoulli terms in the original case?',
        r'The mean is \(\binom n2/3=n(n-1)/6\). The proposed independent-Bernoulli variance is unjustified: covariance terms must be checked for pairs of crossing indicators. Linearity settled the mean without supplying their joint distribution.',
        ['Justify uniformity among the three pairings of four chosen endpoints.',
         'Use crossing indicators and linearity to obtain 15.',
         'Distinguish crossing pairs from geometric intersection locations and avoid an independence claim.'])
