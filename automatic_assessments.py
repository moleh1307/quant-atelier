"""Authored objective checkpoints for the 70 former written problems.

Keep each original task/derivation and ID. Exact-set choices assess mathematical
claims, not free-form prose. Numerical transfer cases accompany general proofs.
A versioned pass is required; legacy self-assessments never become passes.
"""
import hashlib
import math

VERSION = 'objective-v1'
CHECKS = {}

def N(prompt, answer, explanation, tolerance=1e-6):
    return dict(type='numeric', prompt=prompt, answer=answer, tolerance=tolerance, explanation=explanation)

def S(prompt, *rows):
    return dict(type='select', prompt=prompt, options=[dict(correct=ok, text=text, explanation=reason) for ok, text, reason in rows])

def add(id, *checks):
    CHECKS[id] = list(checks)

add('q21',
    N('Without an intercept, fit y=(1,3) on the single column x=(1,2). What is the sum of the fitted residuals?', -0.2, 'The slope is 7/5; residuals are −2/5 and 1/5.'),
    S('Which statements follow from the least-squares normal equations?',
      (True, r'With a free intercept, the constant vector belongs to the design space, so \(\mathbf1^Tr=0\).', 'Residuals are orthogonal to every design column.'),
      (False, 'Without an intercept, the residual sum can never be zero.', 'It can happen accidentally, for example with an exact fit.'),
      (True, r'The identity \(X^Tr=0\) concerns the training fit; it does not force the mean prediction error on new data to vanish.', 'There is no normal-equation constraint on unseen responses.'),
      (False, 'Zero residual sum establishes that the model is correctly specified.', 'This is an algebraic property, even for a misspecified regression.')))
add('q22',
    N('Use this table: easy group A=81/90 successes, B=19/20; difficult group A=2/10, B=18/80. What is overall A success rate minus overall B success rate?', .46, 'A=83/100; B=37/100. B beats A within each group but has more difficult cases.'),
    S('Which conclusions about the pooling reversal are valid?',
      (True, 'A pooled rate uses treatment-specific group weights; different weights can reverse both within-group comparisons.', 'The two pooled quantities need not average with the same coefficients.'),
      (False, 'The displayed reversal requires either within-group rate to have been miscomputed.', 'All four rates can be correct simultaneously.'),
      (False, 'This table proves A has a larger causal treatment effect.', 'Assignment and confounding have not been identified.'),
      (True, 'If both treatments were averaged with the same positive group weights, strict within-group dominance would survive pooling.', 'Subtract the two weighted averages term by term.')))
add('q24', N(r'For n=5 and \(\sigma^2=9\), what is the expectation of the variance computed with divisor n?', 7.2, 'Its expectation is (n−1)σ²/n.'),
    S('Select the valid derivation and boundary claims.',
      (True, r'\(\sum_i(X_i-\bar X)^2=\sum_i(X_i-\mu)^2-n(\bar X-\mu)^2\).', 'Expand both sides around the population mean.'),
      (True, r'For n>1, dividing the centred sum by n−1 gives an unbiased variance estimator.', 'The sample-mean term has expectation σ².'),
      (False, 'The correction depends on the observations having a normal distribution.', 'Iid observations and finite variance suffice.'),
      (False, 'For n=1, replacing the denominator by n−1 gives a well-defined unbiased variance estimate.', 'The centred sum is zero and the proposed denominator is zero.')))
add('q26', S('Which interpretations of p=0.03 are valid?',
      (True, 'Under the specified null law, the pre-specified statistic is at least as extreme as the observed statistic with probability 0.03.', 'Extremeness and the null sampling model must be declared.'),
      (False, 'The null is false with posterior probability 0.97.', 'A p-value is not a posterior model probability.'),
      (False, 'Repeating this experiment has a 3% chance of reproducing its result.', 'The p-value does not specify replication probability.'),
      (True, 'A posterior comparison needs prior model weights and likelihoods under the models being compared.', 'Bayes normalization uses both likelihoods and prior masses.')),
    N('For a separate model comparison, take P(H1)=0.1, P(D|H1)=0.8 and P(D|H0)=0.2. Compute P(H1|D). These are event likelihoods, not the reported p-value.', 4/13, '0.08/(0.08+0.18)=4/13.'))
add('q27', S('Which flaws can make the original random-row validation unsuitable for deployment?',
      (True, 'Training and validation targets can share the same underlying returns.', 'Their five-period label intervals overlap.'),
      (True, 'A training row later in time can use information unavailable at an earlier test decision.', 'Random row placement is not a historical fit cutoff.'),
      (False, 'Keeping exactly five rows between splits guarantees safety for any timestamp spacing and receipt delay.', 'Time intervals and availability matter, not a fixed row count.'),
      (True, 'Preprocessing or feature selection fitted before splitting creates an additional leakage channel.', 'Learned transforms are part of the fitted procedure.')),
    S('Select the valid replacement requirements.',
      (True, 'Evaluate past-to-future fits using only labels mature and available by each fit cutoff.', 'A label end timestamp alone need not be its receipt time.'),
      (False, 'Purging overlap alone makes future training rows permissible.', 'Disjoint future rows still violate historical availability.'),
      (True, 'Fit transforms inside training folds and reserve final evaluation from model-selection decisions.', 'Both preprocessing and adaptive selection must respect the split.'),
      (False, 'An embargo repairs every source of information leakage automatically.', 'Embargo is one boundary control, not a proof of pipeline validity.')))
add('q28', N('Training values are 0 and 2; the later test value is 100. Use population mean/variance scaling. What is the correctly scaled test value?', 99, 'Training mean=1 and standard deviation=1.'),
    S('Which pipeline statements are correct?',
      (True, 'Fit the scaler on the training fold, then apply its frozen parameters to that fold’s validation observations.', 'Validation values must not affect learned parameters.'),
      (False, 'A transform that ignores target labels cannot leak information.', 'Future feature distribution information can leak too.'),
      (False, 'Refitting the scaler separately on the test set is the normal deployment evaluation of the same trained model.', 'It changes the coordinate system relative to training.'),
      (True, 'Past-only online updating can be evaluated if that updating rule is part of the declared deployed procedure.', 'Availability and the pre-specified algorithm determine validity.')))
add('q30', N('Take X=diag(1,0.01), y=(1,1), λ=0.01. What is the second ridge coefficient?', 100/101, 'β₂=0.01/(0.0001+0.01); unregularized coefficient would be 100.'),
    S('Which ridge identities are valid for the stated objective?',
      (True, r'\(\hat\beta=(X^TX+\lambda I)^{-1}X^Ty\), even when X lacks full column rank.', 'Adding λI makes the Gram matrix positive definite.'),
      (False, r'Ridge training residuals always satisfy \(X^Tr=0\).', 'They satisfy Xᵀr=λβ under this penalty.'),
      (True, r'Along singular value s, the response-to-coefficient factor is \(s/(s^2+\lambda)\).', 'The penalty suppresses small-singular-value amplification.'),
      (False, 'The displayed objective leaves an intercept unpenalized automatically.', 'Every component of β is penalized unless the objective excludes it.')))
add('q31', N('For stationary daily returns with marginal variance 1, lag-one covariance 0.25 and all larger-lag covariances zero, what is the variance of the sum over 252 days?', 377.5, '252+2×251×0.25=377.5.'),
    S('Which annualization statements are valid?',
      (True, r'For iid additive returns, k-period mean is kµ and variance is \(k\sigma^2\).', 'This yields √k times the one-period mean/SD ratio.'),
      (False, 'Zero lag-one covariance alone guarantees the square-root rule at every horizon.', 'Higher-lag covariance can remain.'),
      (True, r'Under stationarity, sum variance is \(k\gamma_0+2\sum_{h=1}^{k-1}(k-h)\gamma_h\).', 'Each lag contributes its actual number of covariance pairs.'),
      (False, 'The same additive derivation is exact for compounded returns.', 'Compounding has a different nonlinear payoff.')))
add('q32', S('Which statements about selecting among 1,000 models are valid?',
      (True, 'The selected validation score is generally optimistic because the same scores chose the winner.', 'Selection favors favorable evaluation noise.'),
      (False, 'Only the number of free parameters in the winning model matters for the search bias.', 'The selection procedure and dependence among candidates also matter.'),
      (False, 'A new filename for the chosen validation set makes it an untouched test set.', 'Its role is determined by actual use.'),
      (True, 'Nested selection evaluates the entire tuning procedure on an outer evaluation split.', 'The inner stage selects; the outer stage evaluates.')),
    S('Which proposed fixes preserve a credible final evaluation?',
      (False, 'Try more variants on the final test and report the best one.', 'This repeats the original problem on the final test.'),
      (True, 'Freeze the selection procedure before evaluating on genuinely unused deployment-like data.', 'The final data must not become a tuning signal.'),
      (True, 'Report what was searched and compare candidates using uncertainty that respects score dependence.', 'Nominal model count alone does not describe effective search.'),
      (False, 'Subtract one universal penalty determined only by the number 1,000.', 'A valid penalty requires assumptions about noise and dependence.')))
add('q33', N('Concrete audit: 40 filled trades each earn 2 ticks gross and pay 1.5 ticks in total costs; 60 opportunities do not fill and earn zero. A remaining inventory position costs 30 ticks to liquidate. What is the total net episode profit?', -10, '40×(2−1.5)−30=−10; no-fill opportunities are not profitable executions.'),
    S('Which evidence is needed before converting price prediction into a trading claim?',
      (True, 'Verify that every feature was available before the decision and that the target is not leaking execution information.', 'Historical availability must match the decision.'),
      (False, 'High directional accuracy establishes positive expected net profit.', 'Payoff sizes, fills, costs and inventory can dominate accuracy.'),
      (True, 'Evaluate executable prices, latency, fills and terminal inventory liquidation against an executable baseline.', 'A complete trading episode differs from predicting a recorded print.'),
      (False, 'Exclude no-fill opportunities from all policy evaluation.', 'Fill conditioning can select outcomes and changes the evaluated quantity.')))
add('q34', S('Classify the evidence without claiming more than it establishes.',
      (True, 'If a timestamp-safe replay removes performance, investigate availability or implementation before asserting regime change.', 'The replay directly tests an information/implementation mechanism.'),
      (False, 'A bad second period by itself proves the model was overfit.', 'Many distinct mechanisms can produce the same observation.'),
      (True, 'Stable gross performance but larger measured fees can explain a decline in net performance.', 'Compare the same episodes before and after actual costs.'),
      (False, 'A distribution shift proves the model has lost skill conditional on each market state.', 'Changed mixture weights can change aggregate scores without conditional deterioration.')),
    S('Which diagnostic comparisons are appropriately controlled?',
      (True, 'Reproduce the old run with frozen data, code and settings; then vary one suspected mechanism.', 'Reproducibility distinguishes changed inputs from changed inference.'),
      (False, 'Choose the best explanation after repeatedly tuning on the failed period and treat that period as confirmation.', 'The failed period is now part of selection.'),
      (False, 'Compare different sets of filled trades and attribute every difference to the model.', 'Selection of opportunities can confound the comparison.'),
      (True, 'Compare the model and baseline on matched opportunities and inspect state-specific performance and net costs.', 'Matched evaluation separates mixture, prediction and execution effects.')))
add('q41', N('Transfer case: V is 100 or 200 with equal priors. Conditional winning probabilities for a fixed bid are 0.8 and 0.2 respectively. What is E[V|win]?', 120, 'Normalize joint masses 0.4 and 0.1; winning selects the low-value state.'),
    S('Which bidding claims are justified?',
      (True, 'Unbiasedness before selection does not guarantee unbiasedness after winning.', 'Winning is another observation about common value.'),
      (False, 'The optimal first-price bid always equals E[V|win] for the current bid.', 'Changing a bid changes both win probability and conditional margin.'),
      (True, 'Expected profit must account jointly for the bid-dependent winning event and payment.', 'Optimize E[(V−b)1{win at b}], with the stated rules and costs.'),
      (False, 'A winner’s curse necessarily occurs in every auction with an uncertain value.', 'Its direction and existence depend on the joint information/selection law.')))
add('q42', N('Starting bid/ask is 99/101. Lower both by 0.5. What is the new spread?', 2, 'The midpoint shifts but ask−bid is unchanged.'),
    S('Which distinctions matter for a long dealer’s choice?',
      (True, 'Lowering both prices reduces the bid and ask; widening symmetrically reduces the bid but raises the ask.', 'A shift and a width change create different customer incentives.'),
      (False, 'Symmetric widening mechanically guarantees inventory reduction.', 'It may also discourage the selling fills that reduce a long position.'),
      (True, 'The choice needs fill responses, adverse-selection estimates, inventory limits and the risk/horizon objective.', 'Quote changes affect both selection and inventory dynamics.'),
      (False, 'One may calculate a new quote’s payoff using an unchanged fill-conditioned fair value without checking the flow model.', 'Changing quotes can change who trades.')))
add('q43', N('Compute the variance of the antithetic pair average.', 1/180, 'The centered polynomial U²−U+1/2 has variance 1/180.'), N('Compute the variance of the average of two independent squared uniforms.', 2/45, 'Var(U²)=1/5−1/9=4/45; average two independent terms halves it.'),
    S('Select the valid comparison claims.',
      (True, r'\(\operatorname{Cov}(U^2,(1-U)^2)=-7/90\).', 'E[U²(1−U)²]=1/30; subtract 1/9.'),
      (False, 'The two antithetic outputs constitute two independent simulation units.', 'The pair shares U.'),
      (True, 'Both averages are unbiased for 1/3.', 'Each squared uniform has expectation 1/3.'),
      (False, 'Antithetic coupling reduces variance for every possible integrand.', 'The covariance can be positive, for example for a symmetric integrand.')))
add('q44', S('Choose the valid historical join rules.',
      (False, 'The feature can be used at 10:00:01 because its event label is 10:00:00.', 'It had not arrived.'),
      (True, 'Eligibility requires receipt time no later than the decision, with the declared timestamp tie rule.', 'Information must actually be available.'),
      (True, 'Join the appropriate latest eligible vintage rather than the final revised value.', 'Revisions can change both values and historical signals.'),
      (False, 'A fixed one-second lag is sufficient for arbitrarily delayed receipts.', 'Receipt delays are not necessarily bounded by one second.')),
    N('Two rows have (event,receipt,value)=(0,2,4) and (1,4,9). At decision time 3, select the latest-event row whose receipt is ≤3. What value is available?', 4, 'The later-event row has not arrived.'))
add('q47', S('Which claims about repeated testing are correct?',
      (True, 'Pointwise 5% validity at each fixed sample size does not bound the probability of ever rejecting at 5%.', 'The rejection event is now a union over inspections.'),
      (False, 'The inspections must be independent for optional stopping to be a problem.', 'Dependence does not supply a general 5% guarantee.'),
      (True, 'A pre-specified single fixed-horizon test is a principled alternative.', 'Its advertised sampling guarantee then applies.'),
      (False, 'Stopping immediately after a rejection preserves the original fixed-sample level.', 'That is the selected stopping rule being audited.')),
    S('Which sequential controls have a valid stated justification?',
      (True, r'Pre-specify levels \(\alpha_t\) with \(\sum_t\alpha_t\leq0.05\); if each inspection is null-valid, the union bound controls any rejection.', 'No cross-inspection independence is needed.'),
      (False, 'Use 5% at every look and average the reported p-values after stopping.', 'This is not a demonstrated anytime-valid test.'),
      (True, 'Use a nonnegative null supermartingale starting at one and reject at threshold 20, with an appropriate maximal bound.', 'This controls crossing at any time.'),
      (False, 'Calling the ordinary p-value an e-value makes the same threshold rule valid.', 'The required expectation property must be proved.')))
add('q48', N('For Var(X)=4, Var(Y)=9 and Cov(X,Y)=3, give the optimal control coefficient c.', .75, 'Differentiate 9+4c²−6c.'), N('For that coefficient, give the residual variance.', 6.75, '9−9/4=27/4.'),
    S('Which general control-variate statements are valid?',
      (True, r'\(c_*=\operatorname{Cov}(X,Y)/\operatorname{Var}(X)\).', 'Complete the square in the variance.'),
      (False, 'The optimal coefficient must be positive.', 'Its sign follows the covariance.'),
      (True, 'Any fixed coefficient preserves unbiasedness when the declared control mean is correct.', 'The adjustment has mean zero.'),
      (False, 'Fitting c on the same observations automatically preserves finite-sample unbiasedness.', 'The fitted coefficient can correlate with the control sample mean.')))
add('q50', N('For n=4 and observed maximum M=6, what is the MLE?', 6, 'The likelihood vanishes below M and decreases above it.'),
    S('Select the valid general likelihood claims.',
      (True, r'\(L(\theta)=\theta^{-n}\mathbf1\{\theta\geq M\}\) for the stated observed record.', 'Parameter-dependent support cannot be dropped.'),
      (False, 'A likelihood maximum must occur at a zero derivative in the interior.', 'Boundary maxima exist.'),
      (True, r'\(E[M]=n\theta/(n+1)\), so the MLE is biased down.', 'The maximum’s CDF is (m/θ)^n.'),
      (False, 'Multiplying M by (n+1)/n gives another MLE under the same model.', 'It is an unbiased correction, not the maximizing parameter.')))
add('q51', N('When the observed Y=1, compute naive likelihood divided by correct likelihood at p=1/2.', 2**-99, 'The ratio p^100/p=p^99.', 1e-33),
    S('Which conclusions survive the duplicated-row comparison?',
      (True, 'The correct likelihood is p; the falsely iid likelihood is p to power 100.', 'There is only one random draw.'),
      (True, 'Both likelihoods attain their maximum at p=1 on the closed interval.', 'Agreement of point maxima does not imply equal information.'),
      (False, 'The copies give 100 independent Bernoulli observations because they occupy different rows.', 'Their values are perfectly dependent.'),
      (False, 'One can infer valid iid uncertainty merely from agreement of the two MLEs.', 'The curvature and sampling law differ.')))
add('q_l01_m1', N('Probability of different labels under procedure I?', 2/3, 'Six of nine ordered draws have different labels.'), N('Probability of different labels under procedure II?', .5, 'Three of six equally weighted multisets have different labels.'),
    S('Which outcome-weight statements are valid?',
      (True, 'Under I, AA has weight 1/9 and AB has weight 2/9.', 'Erasing order merges two mixed-label records.'),
      (False, 'Under I every unordered multiset has probability 1/6.', 'Equal record names do not mean equal weights.'),
      (True, 'Under II each of AA and AB has weight 1/6.', 'This is how procedure II is defined.'),
      (False, 'The procedures become identical merely because they have the same six possible records.', 'Their probability measures differ.')))
add('q_l02_h1', N('Use reporting probability s=1/4. What is P(BB|report)?', 2/3, 'BB mass=1/4; the two mixed masses total s/2.'),
    S('Which reporting-law claims are valid?',
      (True, r'The general posterior is \(1/(1+2s)\).', 'Normalize BB weight against both mixed households.'),
      (False, 'Inspecting one uniformly selected child corresponds to s=1.', 'For a mixed household the selected child is a boy only half the time.'),
      (True, 'Inspecting both and reporting at least one boy gives posterior 1/3.', 'This rule uses s=1.'),
      (False, 'The wording alone determines a unique posterior independent of the device.', 'The report likelihood is part of the experiment.')))
add('q_l05_h2', N('At artificial boundary N=100, what is the expected exit time starting from 1?', 99, 'Use i(N−i)=N−1.'),
    S('Which proof steps are valid on the unbounded half-line?',
      (True, r'\(P(T<\infty)\geq1-1/N\) for every N, hence termination has probability one.', 'Hitting zero before N is a subset of eventual termination.'),
      (True, r'Pathwise \(T\geq\tau_N\), so \(E[T]\geq N-1\) for every N.', 'Artificial upper absorption can only shorten the path.'),
      (False, 'Almost-sure termination implies the duration has a finite expectation.', 'This very model is a counterexample.'),
      (False, 'Any finite solution of the local first-step recurrence is automatically the expected duration.', 'It must satisfy nonnegativity and global integrability conditions.')))
add('q_l06_h2', N('Give the infimum of a/b consistent with the rounding reports.', 33/17, '0.495/0.255=33/17, approached but not attained.'), N('Give the supremum of c/d consistent with the reports.', 103/51, '0.515/0.255=103/51, approached but not attained.'),
    S('Which boundary and ranking conclusions are valid?',
      (True, r'The tight intervals are \((33/17,101/49)\) and \((101/53,103/51)\).', 'The excluded numerator/denominator endpoints make both ratio bounds open.'),
      (False, 'Half ties upward makes the upper measurement endpoint included.', 'The exact upper tie rounds to the next displayed value.'),
      (True, 'a=0.496,b=0.254,c=0.514,d=0.256 reverses the displayed ranking.', 'Both ratios obey their measurement intervals and 248/127<257/128.'),
      (False, 'Independent rounding gives a probability that the ranking is correct without a distribution of true values.', 'It supplies intervals, not a probability law.')))
add('q_l07_h2', N('What would the proposed variance of the sum of all five variables be?', -1, '5+20×(−0.3)=−1, impossible.'),
    S('Which feasibility claims are valid?',
      (True, r'The complete common-correlation range is \([-1/4,1]\).', 'The eigenvalues are 1+4ρ and 1−ρ.'),
      (False, 'It is enough that each two-variable covariance matrix is PSD.', 'That does not imply joint PSD.'),
      (True, r'\(X_i=\sqrt{5/4}(Z_i-\bar Z)\) attains the lower boundary with variance one.', 'Centered independent inputs yield zero sum and pair covariance −1/4.'),
      (False, 'A singular covariance at the lower boundary is necessarily invalid.', 'A deterministic zero-sum relation is feasible.')))
add('q_l08_h1', N('With shared revision budget B=2, how many distinct historical total-profit values are attainable?', 2, 'Possible profits are −2 and 0; attaining +2 requires total revision strictly greater than 4.'),
    S('Select the exact identification statements.',
      (True, 'Without a revision bound the profit set is {−2,0,2}; per-measurement bound 2 reduces it to {−2,0}.', 'The second original stays ≥6 under the individual bound.'),
      (False, 'Under shared B=4, profit +2 becomes attainable.', 'It requires u≥5 and v<5: revision cost strictly exceeds 4.'),
      (True, 'For shared B<1 the set is {−2}; for 1≤B≤4 it is {−2,0}; for B>4 it is {−2,0,2}.', 'The switching thresholds are affected by the strict inequality for v.'),
      (False, 'Replaying the final values identifies the actual historical positions.', 'Multiple original histories yield the same final table.')))
add('q_l08_h2', S('Use zero-based feature indices. Which conditions establish the required information boundary?',
      (True, r'Whenever two finite sequences have the same first i inputs, their \(F_n(x)_i\) values must agree, for every n>i.', 'Use zero-based indexing: feature i appears before x_i.'),
      (False, 'Checking that each explicitly referenced raw value is lagged is sufficient.', 'A global normalization or final-length dependence can still leak.'),
      (True, 'The prefix condition must compare different final lengths as well as different suffix values.', 'The online procedure does not know the final length.'),
      (False, 'Equal results on finitely many changed suffixes prove the universal condition.', 'Finite tests can falsify but not establish arbitrary function-family invariance.')),
    S('Which proof or counterexample constructions are valid?',
      (True, 'To emit index i, evaluate F on the observed i-element prefix followed by one dummy input, and return index i.', 'The universal prefix condition makes that finite batch result independent of the dummy and final length.'),
      (False, 'The online implementation must retain only constant-size memory for the equivalence to hold.', 'The task explicitly permits retaining the full past.'),
      (True, 'For i>0, using x_(i−1)/n violates the condition despite lagging the raw value.', 'The final length n is unavailable.'),
      (False, 'A batch procedure that always terminates automatically has an equivalent online implementation.', 'Finite computability does not imply causal dependence.')))
add('q_l09_h1', N('For n=2, what coefficient c minimizes squared-error risk of cM?', 4/3, 'c*=(n+2)/(n+1).'),
    S('Which risk claims are valid for every n≥1?',
      (True, r'\(R_\theta(cM)/\theta^2=c^2n/(n+2)-2cn/(n+1)+1\).', 'Use the first two moments of the normalized maximum.'),
      (False, 'The unbiased correction necessarily has the smallest squared-error risk.', 'Risk includes variance as well as squared bias.'),
      (True, r'The minimizing coefficient is \((n+2)/(n+1)\), with risk \(\theta^2/(n+1)^2\).', 'Complete the quadratic in c.'),
      (False, 'The coefficient may depend on the realized maximum while still belonging to the stipulated fixed-coefficient family.', 'The family constrains c to depend only on n.')))
add('q_l09_h2', N('For n=16, what is the constant minimax risk?', .01, 'a=√n/2=2; risk=1/[4(√n+1)²].'),
    S('Which steps correctly prove global minimaxity?',
      (True, r'\(R_p(\delta_a)=[np(1-p)+a^2(1-2p)^2]/(n+2a)^2\).', 'Variance plus squared bias gives the expression.'),
      (False, 'A constant-risk rule is globally minimax without any further lower bound.', 'Another estimator might have uniformly smaller risk.'),
      (True, r'Choose \(a=\sqrt n/2\); its Beta(a,a) Bayes posterior mean is the same rule, and Bayes risk lower-bounds every supremum risk.', 'Its constant risk meets that global lower bound.'),
      (False, 'The posterior mode rather than mean minimizes posterior squared error.', 'Conditional squared loss is minimized by the conditional mean.')))
add('q_l25_h1', N('With c=10 and retained mean 6, how many finite positive-rate maximizing points exist?', 0, 'The conditional mean under λ>0 is strictly below c/2; the likelihood supremum is at λ↓0.'),
    S('Which truncated-likelihood conclusions are valid?',
      (True, r'\(L(\lambda)=\lambda^n e^{-\lambda\sum x_i}/(1-e^{-\lambda c})^n\).', 'Retention normalization depends on λ.'),
      (False, 'The MLE is always the reciprocal of the retained mean.', 'That omits the selection normalization.'),
      (True, r'A unique finite positive MLE exists exactly when \(\bar x<c/2\); otherwise the open domain has a supremum at zero, not an attained maximum.', 'The conditional mean decreases strictly from c/2 toward zero.'),
      (False, 'The mean-derivative identity is positive variance for density proportional to exp(−λx).', 'Differentiating the normalized expectation gives minus variance.')))
add('q_l25_h2', N('Set µ1=x1,v1=ε²,µ2=0,v2=1. For each other observation the second-component density is a fixed positive lower bound. What is the divergence exponent a in L≥C ε^(−a) supplied just by x1?', 1, 'The x1 factor is at least 1/[2√(2π)ε], and all other factors are bounded below positively.'),
    S('Which mixture-existence claims are valid?',
      (True, 'Collapsing one component around an observation makes the whole-record likelihood unbounded.', 'The other component supplies positive density to every remaining finite observation.'),
      (False, 'Nonzero spread of the full dataset prevents each component variance from collapsing.', 'A latent component need not explain the entire dataset.'),
      (False, 'A finite converged optimizer output proves the global MLE exists.', 'Numerical termination does not establish global boundedness/attainment.'),
      (True, 'Fixed half weights do not prevent this collapse.', 'The singular density is still multiplied by a positive constant.')))
add('q_l10_m1', N('For the reported pairwise matrix, what is the quadratic form in direction w=(1,−1,1)?', -3, 'The three pair correlations are +1,+1,−1; w has eigenvalue −1.'),
    S('Which audit conclusions are valid?',
      (True, 'The reported matrix is [[1,1,−1],[1,1,1],[−1,1,1]].', 'Each pair is fitted on a different two-row sample.'),
      (False, 'Correct pairwise Pearson calculations guarantee a joint PSD matrix.', 'There is no common set of observations supporting the three pair calculations.'),
      (True, 'A negative weighted variance disproves a proposed joint covariance law.', 'Every actual covariance matrix must be PSD.'),
      (False, 'Setting the diagonal to one repairs any invalid correlation table.', 'The invalid weighted variance remains.')))
add('q_l10_h1', N('Use B=[[1,1],[1,1]] and c=(2,2). What is the smallest feasible v?', 4, 'c lies in the range; cᵀB⁺c=4.'),
    S('Which singular block-covariance statements are valid?',
      (True, r'For every zero eigenvalue, \(c_i=0\) is necessary.', 'A variance-zero predictor direction has zero covariance with T.'),
      (False, 'A sufficiently large finite v repairs c=(1,2) for the stated singular B.', 'c has a nonzero null-direction projection.'),
      (True, r'With c in the range, feasibility is equivalent to \(v\geq\sum_{\lambda_i>0}c_i^2/\lambda_i\).', 'Complete the square; an independent residual constructs sufficiency.'),
      (False, 'The ordinary Schur complement using B inverse applies without modification to singular B.', 'The inverse is undefined and the range constraint is essential.')))
add('q_l10_h2', N('For covariance [[1,2],[2,4]], what is the minimum variance of an unbiased weighted mean?', 0, 'The null vector (2,−1) sums to one and gives exact cancellation.'),
    S('Which complete singular-covariance characterizations are valid?',
      (True, 'If a null vector has nonzero sum, zero variance is attainable by normalizing it; all optimal weights are null vectors summing to one.', 'PSD quadratic form vanishes exactly on the null space.'),
      (False, 'Normalizing Σ⁺1 always yields the optimum, including every singular case.', 'It can miss a feasible zero-risk null direction.'),
      (True, r'Otherwise optimum variance is \(1/(\mathbf1^T\Sigma^+\mathbf1)\), with weights proportional to \(\Sigma^+\mathbf1\) plus any null vector.', 'The null space is orthogonal to 1; the positive-space Cauchy–Schwarz bound is sharp.'),
      (False, 'Negative weights must be disallowed for the zero-risk construction.', 'The problem explicitly permits signed weights.')))
add('q_l11_m1', N('What is the population regression slope?', 2, 'X=U+V and Y=3U+V; Cov=4 and Var(X)=2.'), N('What is the intervention response to a unit increase in X?', 1, 'The generator Y=X+2U holds U fixed under intervention.'),
    S('Select the valid observational/causal distinctions.',
      (True, 'The fitted residual is U−V and is uncorrelated with X.', 'Cov(U−V,U+V)=0.'),
      (False, 'Residual orthogonality proves the fitted slope is the causal effect.', 'Confounding remains through U.'),
      (True, 'The intervention replaces the X equation while preserving the equation for Y.', 'That is the stipulated intervention mechanism.'),
      (False, 'The fitted residual must be independent of X under only the assumptions given.', 'Uncorrelatedness need not imply independence.')))
add('q_l11_h1', N('Suppose Cov(W1,W2)=2, Cov(W2,Y)=6, Var(W1)=5 and Cov(W1,Y)=8. What is the identified latent slope β?', 3, 'β=Cov(W2,Y)/Cov(W2,W1); OLS on W1 is 8/5 instead.'),
    S('Which identification claims are valid?',
      (True, 'Cov(W1,W2)=s>0 under the specified zero-covariance assumptions.', 'The two independent-error directions leave the latent covariance.'),
      (False, 'Allowing Cov(u1,ε)≠0 invalidates the W2 covariance ratio.', 'The numerator uses u2, not u1.'),
      (True, 'Relaxing Cov(u2,ε)=0 can destroy identification from this ratio.', 'The numerator acquires an unknown error covariance.'),
      (False, 'An identified population ratio implies its finite-sample empirical ratio is unbiased.', 'Expectation of a ratio is not generally the ratio of expectations.')))
add('q_l11_h2', N('For a row with r_i=6 and h_i=0.4, what is the leave-one-out prediction error?', 10, 'The deletion error is r_i/(1−h_i).'),
    S('Which deletion and rank statements are valid?',
      (True, r'For \(h_i<1\), the deleted fit has full column rank and error \(r_i/(1-h_i)\).', 'The rank-one inverse update has denominator 1−h_i.'),
      (False, 'When h_i=1, the full-fit residual r_i=0 proves a zero held-out error.', 'Deleting that row loses an identified design direction.'),
      (True, 'If h_i=1, the deleted design is rank deficient and its prediction at the deleted row is not uniquely determined by least-squares minimization.', 'The removed row is the only evidence in one direction.'),
      (False, 'Full column rank of X guarantees every deleted design also has full column rank.', 'A row can have unit leverage.')))
add('q_l12_m1', N('What randomization probability γ spends exactly the null error budget?', 11/30, '(1/20−1/64)/(6/64)=11/30.'), N('What is the power at p=3/4?', 3159/10240, '(3/4)^6+γ×6×(3/4)^5×(1/4).'),
    S('Which testing statements are valid?',
      (True, 'The independent uniform draw randomizes the boundary BEFORE its outcome is used to decide rejection.', 'The rule and γ are pre-specified.'),
      (False, 'Rounding γ to one preserves exact 5% null size.', 'Rejecting K≥5 has null probability 7/64.'),
      (True, 'The alternative-to-null likelihood ratio increases with K.', 'The simple alternative gives factor 3 per additional head.'),
      (False, 'Choosing γ after seeing whether it helps the observed record is the same pre-specified test.', 'That changes the selection procedure.')))
add('q_l12_h1', N('What threshold starting from M0=1 gives the same maximal-bound guarantee at level 0.01?', 100, 'A threshold 1/α gives crossing probability at most α.'),
    S('Which steps establish the unlimited-inspection bound?',
      (True, 'Under the null, the next multiplier is 3/2 or 1/2 with equal probability, so its conditional mean is one.', 'This establishes the martingale property.'),
      (False, 'Under the null, every sample path has decreasing M_t.', 'Heads multiply it by 3/2.'),
      (True, 'Stop at first crossing or fixed N; nonnegativity and bounded stopping give 1≥20P(cross by N).', 'The stopped value is at least 20 on crossing.'),
      (False, 'To handle unlimited inspection, one must assume E[M_τ]=1 at the unbounded crossing time.', 'Increasing finite crossing events and their probabilities suffice.'),
      (True, 'The events of crossing by N increase to the event of ever crossing.', 'Probability continuity passes the finite bound to the union.')))
add('q_l12_h2', N('What is conditional coverage at µ=2c?', 38/39, 'The numerator is 0.95 and selection probability is 0.975.'),
    S('Which conditional-coverage expressions are valid?',
      (True, 'For µ≤0, the conditional coverage is zero.', 'The largest X that could cover µ is µ+c≤c, outside the selection event.'),
      (False, 'At µ=0, conditioning on positive significance leaves coverage at 0.95.', 'A reported interval then excludes zero.'),
      (True, r'For \(0<\mu<2c\), coverage is \([\Phi(c)-\Phi(c-\mu)]/[1-\Phi(c-\mu)]\).', 'Intersect the covering interval with X>c and normalize.'),
      (True, r'For \(\mu\geq2c\), coverage is \((1-\alpha)/[1-\Phi(c-\mu)]\).', 'The whole coverage event lies inside the selection region.'),
      (False, 'Selection assigns a posterior distribution to the fixed unknown µ without a prior.', 'Conditional sampling coverage is not Bayesian probability.')))
add('q_l13_m1', N('What is Var of the mean of Y over n=4?', 11/4, '(12n−4)/n²=44/16.'),
    S('Which dependence calculations are valid?',
      (True, 'X has zero covariance at every nonzero lag, while Y has variance 8 and lag-one covariance 2.', 'Products involving an unpaired centered Gaussian vanish; squared products share ε².'),
      (False, 'Zero autocovariance implies adjacent X values are independent.', 'Their squared values have nonzero covariance.'),
      (True, r'\(\operatorname{Var}(\bar Y_n)=(12n-4)/n^2\) for n≥1.', 'There are n diagonal terms and two copies of n−1 adjacent covariance terms.'),
      (False, 'The iid shortcut 8/n is exact for every n.', 'It omits the adjacent Y covariances.')))
add('q_l13_m2', N('Use n=5, k=3 and σ²=1. What is Var of the stated one-period mean estimator?', 37/225, 'The numerator is nk²−k(k²−1)/3=37; divide by n²k².'),
    S('Which overlapping-sum identities are valid?',
      (True, r'\(\operatorname{Cov}(Y_t,Y_{t+h})=(k-|h|)\sigma^2\) for |h|<k and zero otherwise.', 'Count shared underlying returns.'),
      (False, 'The n labels are independent because the original returns are iid.', 'Adjacent labels share k−1 returns.'),
      (True, r'\(\operatorname{Var}(\hat\mu)=\sigma^2[nk^2-k(k^2-1)/3]/(n^2k^2)\).', 'Expand the label-sum covariance with the finite-horizon lag counts.'),
      (False, 'The stated calculation applies unchanged to compounded k-period returns.', 'The task’s labels are linear sums.')))
add('q_l13_h1', N('For n=5, ρ=1/2 and γ0=1, what is the optimal variance?', 3/7, 'γ0(1+ρ)/[n−(n−2)ρ]=3/7.'),
    S('Which explicit GLS results are valid?',
      (True, r'Writing \(D=n-(n-2)\rho\), endpoint weights are 1/D and each interior weight is (1−ρ)/D.', 'The inverse-covariance row sums differ at the endpoints.'),
      (False, 'The arithmetic mean is optimal for every ρ in (−1,1) and every n.', 'For n>2 and nonzero ρ the endpoint weights differ from the interior.'),
      (True, r'The optimum variance is \(\gamma_0(1+\rho)/D\) and the optimum is unique.', 'The covariance is positive definite.'),
      (False, 'The weighted-variance argument requires Gaussian observations.', 'Second moments and fixed unbiased weights suffice.')))
add('q_l13_h2', N('For c=2, compute the limiting variance ratio Var(mean)/γ0.', (1+math.exp(-2))/2, 'The integral is 2(c−1+e^(−c))/c².'),
    S('Which changing-model limits are valid?',
      (True, r'The limiting ratio is \(2(c-1+e^{-c})/c^2>0\).', 'The covariance sum becomes the integral of e^(−c|u−v|) on the unit square.'),
      (False, 'Substituting ρ_n into the fixed-ρ asymptotic count always gives the exact limiting effective count.', 'That substitution gives c/2 and omits the finite-horizon taper that remains material.'),
      (True, 'The exact effective count tends to the reciprocal of this ratio.', 'Its definition uses γ0 divided by actual mean variance.'),
      (False, 'The sample mean is consistent because every row n has |ρ_n|<1.', 'The Gaussian estimation error retains positive limiting variance.')))
add('q_l14_m1', N('How many rows are eligible for the strict past-to-future fit?', 2, 'Original rows 0 and 1 meet both receipt and interval constraints.'),
    S('Which row-selection statements are valid?',
      (True, 'Using zero-based indices, overlap purging alone retains [0,1,3,4].', 'Half-open endpoints allow [6,10) and [14,17) outside [10,14).'),
      (False, 'Row 3 is valid training at time 10 because its label is disjoint from validation.', 'Its start and receipt are future.'),
      (True, 'Row 4 is invalid training at time 10 despite a label ending at 10.', 'Its receipt is at 13.'),
      (False, 'Replacing receipt checks with a fixed row-count gap establishes the same information boundary.', 'Row order does not supply availability timestamps.')))
add('q_l14_h1', N('For n=500, what is the Chebyshev 95% error-band half-width using only the stated bound?', .1, 'The squared-error bound is 1/(4n), so half-width is √(5/n).'),
    S('Which adaptive-evaluation proof claims are valid?',
      (True, 'D_t=L_t−r_t has conditional mean zero; earlier D values are measurable at later information sets.', 'These conditions make distinct D values orthogonal in expectation.'),
      (False, 'The risk sequence must be deterministic for the expectation-zero result.', 'It can adapt predictably to earlier mature outcomes.'),
      (True, r'\(E[(n^{-1}\sum D_t)^2]=n^{-2}\sum E[r_t(1-r_t)]\leq1/(4n)\).', 'Bernoulli conditional variance and martingale-difference orthogonality give the bound.'),
      (False, 'The resulting band automatically evaluates a retrospectively chosen winner among all models.', 'It evaluates the actual pre-outcome decisions, not a hindsight selection.')))
add('q_l15_h1', N('With σ=2, ρ=1/2 and a=−1/2, what is the selected confirmation score’s mean minus θ?', -.5*math.sqrt(2/math.pi), 'Selection bias is σ√((1−ρ)/π); confirmation retains a times that bias.'),
    S('Which correlated-selection identities are valid?',
      (True, r'\(E[X_J]=\theta+\sigma\sqrt{(1-\rho)/\pi}\).', 'Use max=(sum+absolute difference)/2.'),
      (False, 'At ρ=−1 the selected score has variance σ².', 'It is θ+|ε1|, with variance σ²(1−2/π).'),
      (True, r'\(\operatorname{Var}(X_J)=\sigma^2[1-(1-\rho)/\pi]\), including both endpoints.', 'The Gaussian sum and difference are independent; handle degeneracies by their exact laws.'),
      (False, 'A confirmation filename makes shared selection noise vanish.', 'Its bias is a times the selection bias; a must be zero for this guarantee.')))
add('q_l16_m1', N('What quiet share w makes the two models tie?', 10/13, '0.70+0.26w=0.60+0.39w.'), N('In period two, what is model accuracy minus baseline accuracy?', -.017, '0.934−0.951=−0.017.'),
    S('Which diagnoses are supported?',
      (True, 'In period one the difference is 0.035; changing only mixture weights reverses it.', 'The conditional accuracies stay fixed.'),
      (False, 'The reversal proves that conditional skill deteriorated within the quiet state.', 'The stated quiet accuracy is unchanged.'),
      (True, 'These prediction probabilities alone do not identify trading profit.', 'They omit payouts and execution.'),
      (False, 'The changing aggregate comparison proves overfitting.', 'The declared fixed conditional laws already explain the change.')))
add('q_l16_h1', N('In the two-context example, what is Var(Z)?', 53/3, 'E[Z²]=56/3 and E[Z]=1.'), N('What is the average payoff conditional on a historical trade?', 0, 'Its numerator E[AY]=0 and P(A=1)=1/2; target value instead equals 1.'),
    S('Which policy-evaluation identities and requirements are valid?',
      (True, r'\(E[Z\mid X]=\pi(X)E[Y\mid X]\).', 'Known propensities and conditional action independence cancel selection.'),
      (False, 'An unrecorded payoff predictor used by the logger cannot affect unbiasedness.', 'It can violate A independent of Y conditional on recorded X.'),
      (True, r'\(E[Z^2]=E[\pi(X)Y^2/e(X)]\), and independent mean variance is \((E[Z^2]-v^2)/n\).', 'Use A²=A and π²=π.'),
      (False, 'The formula identifies payoff on target contexts with e=0 from the same log.', 'Those outcomes lack observational support.')))
add('q_l17_m1', N('What is the smallest n for which the specified upper bound is ≤0.001?', 2995, 'Ceil(log(0.05)/log(0.999))=2995.'), N('Compute u_1000.', 1-.05**.001, 'u_n=1−α^(1/n).'),
    S('Which coverage claims are valid?',
      (True, r'\(u_n=1-\alpha^{1/n}\) solves \(P_{u_n}(K=0)=\alpha\).', 'The zero-hit probability is (1−p)^n.'),
      (False, 'Observing zero hits establishes p=0.', 'Positive event probabilities can produce zero counts.'),
      (True, 'If p>u_n, noncoverage occurs only at K=0 with probability smaller than α; at p=u_n the endpoint is covered.', 'This proves coverage for the complete declared reporting rule.'),
      (False, 'The interval means a 95% posterior probability that this fixed p lies inside it.', 'No prior or posterior was supplied.')))
add('q_l18_m1', N('What is the merged centered sum M2 for the two given batches?', 107.2, 'Within sums are 2 and 8; the between-batch correction is (2×3/5)×9²=97.2.'),
    S('Which merge rules are valid?',
      (True, r'For \(\delta=m_B-m_A\), merged mean is \(m_A+\delta n_B/(n_A+n_B)\).', 'It is the weighted batch mean.'),
      (False, 'Merged M2 is simply M2_A+M2_B.', 'This loses between-batch mean differences.'),
      (True, r'Merged \(M_2=M_{2,A}+M_{2,B}+\delta^2 n_A n_B/(n_A+n_B)\).', 'Expand each observation around the merged mean.'),
      (True, 'An empty batch acts as identity; sample variance requires n>1, and exact associativity need not be bitwise floating associativity.', 'Rounding depends on arithmetic order.'),
      (False, 'The centered sum M2 already contains the unbiased variance divisor.', 'It is a sum; denominator conventions are separate.')))
add('q_l18_h1', N('From window [0,2,4], remove the oldest 0 and append 6. What is the new M2?', 8, 'The new window [2,4,6] has mean 4 and squared deviations 4+0+4.'),
    S('Which rolling-state statements are valid?',
      (True, r'Remove y using \(m_-=(km-y)/(k-1)\) and \(M_{2,-}=M_2-(y-m)(y-m_-)\); then use a Welford insertion.', 'Recenter on the remaining k−1 observations before inserting x.'),
      (False, 'The insertion-only summary and new x determine what leaves for every history.', 'Windows [0,2] and [2,0] have the same summary but different outgoing values.'),
      (True, 'A FIFO of outgoing values supports constant arithmetic per step with O(k) storage.', 'The monitor must remember order, not merely symmetric moments.'),
      (False, 'The removal formula may divide by k−1 unchanged at k=1.', 'A width-one replacement has mean x and M2 zero; no removal division is valid.')))
add('q_l18_h2', N('For k=2 and strictly increasing values 1 through 100, how many entries remain in the described lazy heap after the last arrival?', 100, 'The newest, valid maximum is always at the root; expired smaller entries never reach the cleanup root.'),
    S('Which correctness and complexity claims are valid?',
      (True, 'The root cleanup can report a correct maximum while retaining arbitrarily many expired entries.', 'Correctness of the reported root does not bound total heap size.'),
      (False, 'The heap necessarily uses O(k) space because only k timestamps are active.', 'Expired entries can remain hidden below the root.'),
      (True, 'A decreasing deque removes expired front indices and pops strictly smaller tail values; retaining equal values preserves the earliest tie.', 'Each index is pushed once and removed at most once.'),
      (False, 'For earliest ties the deque should pop tail values equal to the new value.', 'This discards the older equal maximum.'),
      (True, 'The deque has O(n) total operations and O(k) auxiliary space, but one update can still remove O(k) entries.', 'Amortized constant work is not a worst-case constant update.')))
add('q_l19_m1', N('Compute E[V|H].', 14, 'Posterior cells are 0.2,0.05,0.15,0.6.'),
    S('Which information and action statements are valid?',
      (True, 'After H, E[A]=7.5 and E[B]=6.5.', 'The signal updates B through its dependence on A.'),
      (False, 'Conditional independence of H and B given A lets E[B] remain at 5 after H.', 'Marginal independence does not follow.'),
      (True, 'Both buy and sell have negative expected net edge at the given quote; abstaining is optimal.', 'Buy edge is −0.75 and sell edge is −2.25.'),
      (False, 'Buying is profitable merely because the signal raises fair value above its prior mean.', 'Compare updated fair value with executable ask and costs.')))
add('q_l19_m2', N('What is the replication cost?', 7, 'Hold two units of stock and minus three units of cash.'), N('What is the physical expected payoff?', 10, '1×1/4+13×3/4=10.'),
    S('Which pricing arguments are valid?',
      (True, 'Risk-neutral weights are one half in each state, determined by the traded stock and cash.', '2×1/2+8×1/2=5.'),
      (False, 'Use the physical high-state probability to price the replicated claim at 10.', 'That conflicts with its state-by-state replication cost.'),
      (True, 'A different claim price from 7 creates an arbitrage by taking opposite claim and replicating positions.', 'The terminal payments cancel in both states.'),
      (False, 'The risk-neutral weights assert that high occurs half the time physically.', 'Pricing weights are not an empirical probability estimate.')))
add('q_l19_h1', N('What is the largest break-even acquisition fee f?', 1.5, 'Buy after H and sell after L; each conditional net edge is 1.5, so expected pre-fee gain is 1.5.'),
    S('Which value-of-information arguments are valid?',
      (True, 'The posterior means are 8 after H and 2 after L; their average is still 5.', 'Information does not increase the unconditional payoff mean.'),
      (False, 'The value of information must be zero because posterior means average back to the prior.', 'It improves action selection before averaging payoffs.'),
      (True, 'With fixed available actions and zero acquisition cost, the informed decision maker can always imitate the old policy.', 'The larger policy set cannot reduce the optimum.'),
      (False, 'The same guarantee applies unchanged when observing the signal causes the quote to disappear.', 'That changes the available actions.')))
add('q_l19_h2', N('What is the upper endpoint of the posterior fair-value interval?', 10.8, 'The posterior high probability ranges from 1/2 to 9/10.'),
    S('Which robust-policy results are valid?',
      (True, 'The conditional fair-value interval is [6,10.8]; worst buy edge is −3.25 and worst sell edge is −3.05.', 'Use the unfavorable endpoint for each signed payoff.'),
      (False, 'The midpoint of the two posterior endpoints is the Bayesian fair value implied by the problem.', 'No distribution over models is specified.'),
      (True, 'Abstention has minimax value zero.', 'Both deterministic trades have negative worst-case value.'),
      (False, 'An equal random mixture of buy and sell creates a positive robust edge.', 'Its value is −0.75 regardless of model.'),
      (True, 'No buy/sell/abstain randomization can improve strictly on zero.', 'At an interior allowed fair value such as 8.5, both trade payoffs are strictly negative.')))
add('q_l20_m1', N('What is the expected dealer profit per next opportunity at ask 80?', -6.25, 'Next fill probability is 5/8, and fill-conditioned value is 90, giving −10 per fill.'),
    S('Which filtering and selection statements are valid?',
      (True, 'The Buy,No order,Buy sequence gives posterior high probability 3/4.', 'Likelihood odds multiply by 3,1/3,3.'),
      (False, 'No order can be omitted because it is not a trade.', 'It is more likely in the low state.'),
      (True, 'The next buy updates high probability to 9/10, so ask 80 loses 10 per fill in expectation.', 'A fill is additional evidence.'),
      (False, 'Expected profit per opportunity equals expected profit per fill.', 'Multiply by the probability of a fill, retaining zero/no-order outcomes.')))
add('q_l20_m2', N('What is expected net profit per opportunity at ask 70?', -7.75, 'Fill probability 1/4, value on fill 100, net margin −31.'),
    S('Which quote-dependent comparisons are valid?',
      (True, 'At asks 55 and 60, fill probability is 3/4 and conditional value is 200/3.', 'Uninformed buyers fill in both states; informed buyers only in high.'),
      (False, 'The same conditional value 200/3 applies at ask 70.', 'At 70 only informed high-state buyers accept.'),
      (True, 'Ask 100 has no fills under the strict acceptance rule and ties abstention at zero expected gain.', 'All lower allowed quotes have negative net expectation.'),
      (False, 'An ask equal to the high value necessarily fills an informed high-state customer.', 'The rule requires V strictly greater than ask.')))
add('q_l20_h1', N('What is the optimal expected final cash-plus-inventory value?', 5, 'A first learns the state; after a high-state fill, B buys back at two, locking ten; after no order, avoid buying.'),
    S('Which policy and state statements are valid?',
      (True, 'Start with A; after its fill choose B; after its no-order observation skipping is optimal (a zero-payoff A also ties).', 'The observed A branch identifies the fixed terminal value.'),
      (False, 'Starting with B gives the same optimal value as starting with A.', 'B first yields only four even with optimal continuation.'),
      (True, 'An action is infeasible if any positive-probability branch breaches the inventory constraint.', 'One cannot quote first and reject the inconvenient fill later.'),
      (False, 'Signed inventory alone is a sufficient state for second-period optimization.', 'Posterior information and remaining opportunities also matter.')))
add('q_l21_m1', N('What is the optimal value for fees [1,0]?', 33/8, 'Last free reroll value is 17/4; first continuation after fee is 13/4.'), N('What is the optimal value for fees [0,1]?', 53/12, 'Last-stage value with fee one is 23/6; first free continuation uses that value.'),
    S('Which backward-induction statements are valid?',
      (True, 'For [1,0], reroll first values 1,2,3 and reroll second values 1,2,3.', 'The thresholds are 13/4 at the first decision and 7/2 at the second.'),
      (False, 'Both fee schedules have equal value because the listed fees have equal sum.', 'Only fees on actually chosen rerolls are paid.'),
      (True, 'For [0,1], reroll first values 1,2,3 and second values 1,2.', 'First continuation is 23/6; last reroll net mean is 5/2.'),
      (False, 'Subtract the sum of both fees from every path regardless of decisions.', 'Stopping early avoids later fees.')))
add('q_l21_h1', N('What is the Bayesian optimal fraction?', .2, 'One-round expected log growth depends on the predictive mean probability 0.6.'), N('What is the worst-case model-set optimal fraction?', .1, 'For f≥0 the worst success probability is 0.55.'),
    S('Which objective distinctions are valid?',
      (True, 'Averaging model-specific log growth yields the binary growth objective with p=E[P].', 'For fixed f the expression is affine in P.'),
      (False, 'Parameter uncertainty alone necessarily shrinks the one-round Bayesian optimum below 0.2.', 'The stated utility has no separate variance penalty in P.'),
      (True, 'The model-set problem uses a minimum over p, rather than weighted averaging.', 'These are different declared uncertainty objectives.'),
      (False, 'f=1 is allowed because mean success probability exceeds one half.', 'A loss then gives zero wealth and log wealth is undefined.')))
add('q_l21_h2', N('Compute the admissible optimum f.', (12-math.sqrt(69))/75, 'Choose the smaller root of 75f²−24f+1=0, inside [0,1/9).'),
    S('Which domain and optimization claims are valid?',
      (True, r'Admissibility is \(0\leq f<1/9\), so f=0.2 is invalid.', 'The rare loss would produce negative wealth.'),
      (False, 'Discarding the 1% outcome leaves the same log-growth optimum.', 'A rare large loss determines both domain and curvature.'),
      (True, r"\(g\) is strictly concave, \(g^{\prime}(0)=0.12\), and \(g^{\prime}\) tends to minus infinity at the upper boundary.", 'Every nonzero return contributes negative second derivative.'),
      (False, 'Both roots of the derivative numerator are valid stationary points of the original objective.', 'The larger root lies outside its domain.')))
add('q_l22_h1', N('What is the largest possible probability of H<−2/3?', .25, 'The event is exactly X1=X2=X3=1; nonnegative cell masses bound q at 1/4.'),
    S('Which sharp-bound constructions are valid?',
      (True, 'Uniform mass on 000,011,101,110 gives joint crash probability zero.', 'Every pair remains independent and fair.'),
      (True, 'Uniform mass on 001,010,100,111 gives joint crash probability 1/4.', 'It has the same one- and two-dimensional margins.'),
      (False, 'Pairwise independence forces joint crash probability 1/8.', 'That requires joint independence.'),
      (False, 'The two endpoint constructions must have different payoff covariance matrices.', 'Both have mean zero and covariance I.'),
      (True, 'Mixing the endpoint tables attains every value in [0,1/4].', 'All fixed marginal constraints are linear.')))
add('q_l22_h2', N('What is the minimax short quantity h?', .5, 'The worst-case envelope decreases to its switch at 1/2 and increases afterward.'), N('What is its worst-model variance?', 9/4, 'Both endpoint loading models give 4(1−b/2)²+1+1/4=9/4.'),
    S('Which robust-hedging claims are valid?',
      (True, 'For fixed h the largest variance over b∈[1,3] occurs at an endpoint.', 'The variance is convex in b.'),
      (False, 'The minimax solution must have zero derivative under one active smooth model.', 'The optimum is a kink, with left derivative −3 and right derivative 13.'),
      (True, 'At h=1/2 both endpoint models are active.', 'Their difference is 16h(1−2h).'),
      (False, 'Replacing b by its midpoint evaluates the same worst-case objective.', 'That solves a different optimization problem.')))
add('q_l23_m1', N('What is initial cash for short call, long put, long stock, borrow strike?', -4, '5−8−101+100=−4.'), N('What is initial cash for the opposite parity direction?', -6, '−8+5+97−100=−6.'),
    S('Which executable-parity conclusions are valid?',
      (True, 'Both named matched portfolios have zero terminal cash in every state.', 'Call minus put equals terminal stock minus strike.'),
      (False, 'The midpoint discrepancy supplies a locked gain after bid/ask execution.', 'Both executable directions require an initial payment.'),
      (True, 'Neither of these two named trades produces the proposed arbitrage.', 'Negative initial cash followed by zero terminal cash is not a gain.'),
      (False, 'Auditing only these trades proves absence of every possible arbitrage in the market.', 'That broader statement has not been checked.')))
add('q_l23_h1', N('For C=25, what positive pricing weight is assigned to the middle stock state?', .5, 'q0=q2=C/100=1/4 and q1=1−2q2=1/2.'),
    S('Which replication and no-arbitrage claims are valid?',
      (False, 'Stock and cash exactly replicate the call because two tradable securities suffice for any three-state payoff.', 'Matching states zero and 100 forces zero holdings, which fails state 200.'),
      (True, 'The full arbitrage-free interval is 0<C<50, excluding both endpoints.', 'Positive pricing weights exist exactly in this open interval.'),
      (True, 'At C=50, half a stock minus one call is zero-cost and pays (0,50,0).', 'The middle state has strictly positive physical probability.'),
      (False, 'Nonnegative pricing weights at the endpoints suffice for no arbitrage with all three states possible.', 'Zero pricing mass can hide a strictly positive payoff in a possible state.'),
      (True, 'Strictly positive pricing weights rule out a zero-cost, nonnegative, sometimes-positive terminal payoff.', 'Such a payoff would have strictly positive pricing expectation.')))
add('q_l23_h2', N('What is terminal wealth for the moving path (100,110,100)?', 1, 'a times total squared moves minus b times total elapsed time: 0.02×200−3.'), N('What is terminal wealth on that path using the frozen initial delta?', -3, 'The endpoints coincide, so there is no frozen stock gain.'),
    S('Which cash-ledger identities are valid?',
      (True, r'\(B_0=\Delta_0S_0-V_0\), and rehedging gives \(B_i=B_{i-1}+(\Delta_i-\Delta_{i-1})S_i\).', 'An increased short stock position receives cash, balancing the stock liability.'),
      (False, 'An increase in the short hedge creates extra wealth equal to the cash received.', 'The offsetting stock liability changes simultaneously.'),
      (True, r'Terminal wealth is \(a\sum_i(S_{i+1}-S_i)^2-b(t_n-t_0)\).', 'The interval identity is exact for this stipulated quadratic mark.'),
      (False, 'The same constant-gamma interval formula is exact for every smooth option-price function.', 'General functions have changing derivatives and remainder terms.')))
add('q_l24_m1', N('What is mean Brier loss for dataset B?', .81, 'The two errors are −0.9 and +0.9.'),
    S('Which coarse-bin and pairing statements are valid?',
      (True, 'Both datasets have count two, mean forecast 1/2 and mean outcome 1/2.', 'The bin erases how forecasts pair with outcomes.'),
      (False, 'These three bin summaries reconstruct exact mean Brier loss.', 'Dataset A has 0.01 while B has 0.81.'),
      (True, 'Empirical forecast variance is 0.16 and outcome variance 0.25; covariance is +0.2 in A and −0.2 in B.', 'Use divisor two and the paired centered records.'),
      (False, 'A zero bin gap establishes population calibration.', 'A single coarse empirical average is insufficient.'),
      (True, 'Mean squared error equals squared mean gap plus both empirical variances minus twice their covariance.', 'Expand the centered difference.')))
add('q_l24_h1', N('What is the globally optimal first-price bid?', 200/3, 'The lower segment maximizes (100−b)b²/20000; the upper segment is nonpositive.'), N('What is its expected gain per opportunity?', 200/27, 'Win probability 2/9 times conditional margin 100/3.'),
    S('Which global-selection arguments are valid?',
      (True, r'For b≤100, \(G(b)=\tfrac12(100-b)(b/100)^2\).', 'Only the low state can be won, and both rival crossings are needed.'),
      (False, 'Winning conditional value is always the unconditional mean 150.', 'At the optimal bid winning implies V=100.'),
      (True, r'For b≥100, using x=(b−100)/100 gives \(G(b)=50[-x+(1-x)x^2]\leq0\).', 'The low state always wins and incurs a loss; the high branch cannot compensate.'),
      (False, 'Bidding the conditional value at the current bid necessarily maximizes expected gain.', 'Changing b also changes win probabilities and margin.')))
add('q_l24_h2', N('In the two equal-probability regimes with success rates 1/4 and 3/4 and constant P=1/2, what is the Brier-loss improvement from using the true regime?', 1/16, 'Loss falls from 1/4 to 3/16.'),
    S('Which conditional-expectation identities are valid?',
      (True, r'\(E[(P-Y)^2]-E[(R-Y)^2]=E[(P-R)^2]\).', 'The cross term vanishes when conditioned on P.'),
      (False, 'Calibration of P rules out improvement from any additional pre-outcome feature G.', 'G can refine information within a fixed report value.'),
      (True, r'\(E[(R-Y)^2]-E[(T-Y)^2]=E[(T-R)^2]\); improvement is strict exactly when T differs from R with positive probability.', 'Condition on the enlarged information set.'),
      (True, 'R and T are calibrated by tower conditioning.', 'Their exact conditional expectations are measurable under their defining information.'),
      (False, 'The same nonnegative-improvement guarantee holds automatically for arbitrarily fitted estimates on fresh data.', 'Estimation error can outweigh oracle information gains.')))


# Close mathematical alternatives supplement conceptual pitfalls in the harder
# checks. They are deliberately wrong for a specific, explained reason.
DISTRACTORS = {
 'q43': ('The antithetic pair variance is 1/90, since averaging two equal-variance terms divides covariance by two.', 'Variance of (A+B)/2 is [Var(A)+Var(B)+2Cov(A,B)]/4, giving 1/180.'),
 'q48': ('The optimal coefficient is Var(X) divided by Cov(X,Y) when the covariance is nonzero.', 'The derivative sets c Var(X)=Cov(X,Y), not its reciprocal.'),
 'q_l09_h1': ('The risk-minimizing coefficient is (n+1)/n; it coincides with the unbiased correction for every n.', 'Risk minimization uses both moments of M; the coefficient is (n+2)/(n+1).'),
 'q_l09_h2': ('Choosing a=n/2 gives constant risk for every n≥1.', 'The p-dependent coefficient vanishes at 4a²=n, rather than 2a=n.'),
 'q_l25_h1': ('Whenever the retained sample mean is below c, a finite positive maximizing rate exists.', 'Conditional means under positive rates lie strictly below c/2, not merely c.'),
 'q_l25_h2': ('The collapsing component makes the other observations’ likelihood factors vanish, regardless of the second component.', 'The fixed normal second component gives a positive lower bound at every fixed observation.'),
 'q_l10_h1': ('After imposing the range condition, the lower bound on v is the sum of c_i squared divided by lambda_i squared over positive eigenvalues.', 'Completing the covariance quadratic divides by lambda_i once, not twice.'),
 'q_l10_h2': ('For covariance diag(1,4), equally weighting the estimates minimizes variance because both means are the same.', 'The minimizing weights are (4/5,1/5), with variance 4/5; equal weights give 5/4.'),
 'q_l11_h1': ('Even under the stated assumptions, the identified slope uses Cov(W1,Y)/Cov(W1,W2).', 'The first measurement can have response-error covariance; use W2 in the numerator.'),
 'q_l11_h2': ('When h_i<1, the deleted-row error is r_i divided by one plus h_i.', 'Deleting the row downdates the Gram matrix, yielding denominator one minus h_i.'),
 'q_l12_h1': ('The crossing probability equals exactly 1/20 because M0=1.', 'The maximal inequality supplies an upper bound; discrete overshoots and non-crossing paths need not saturate it.'),
 'q_l12_h2': ('For µ≥2c, the reported intervals have coverage 0.95 times the selection probability.', 'Conditional coverage divides joint covering probability by selection probability.'),
 'q_l13_h1': ('For n=5 and rho=1/2, endpoint weights are 1/7 and interior weights are 2/7.', 'The actual endpoint weights are 2/7, with interior weights 1/7; the proposed weights do not even sum to one.'),
 'q_l13_h2': ('The limiting variance ratio is (1−exp(−c))/c.', 'That integrates a single covariance row without the full two-dimensional lag multiplicity.'),
 'q_l14_h1': ('The second moment of mean realized loss minus mean conditional risk always equals the variance of mean realized loss.', 'The conditional risk average is itself random and correlated with realized losses; the martingale difference is the object being bounded.'),
 'q_l15_h1': ('The selected score variance is sigma squared times (1−rho)/pi.', 'That term is the squared selection bias, which is subtracted from the uncentered second moment sigma squared.'),
 'q_l16_h1': ('The score second moment is E[pi(X) times E[Y|X] squared divided by e(X)].', 'Conditional payoff variability also contributes; the correct conditional term is E[Y²|X].'),
 'q_l18_h1': ('Removing y updates M2 by subtracting only the square of y minus the old mean.', 'Every remaining observation must be recentered; the correction is (y−m)(y−m_minus).'),
 'q_l18_h2': ('The lazy heap’s total work is O(n log k) on every stream, even if its retained size grows to n.', 'Heap operations depend on retained heap size, so a growing heap does not justify log k.'),
 'q_l20_h1': ('A B fill identifies the high-value state, just as an A fill does.', 'The customer sells under B in both states; that observation leaves the prior unchanged.'),
 'q_l21_h2': ('The net-return mean is 0.20, so the initial log-growth derivative is 0.20.', 'Its mean and initial derivative are 0.60−0.39−0.09=0.12.'),
 'q_l22_h2': ('For every h>1/2, the b=1 model determines the worst-case envelope.', 'For h>1/2 the b=3 model has larger variance.'),
 'q_l23_h1': ('At C=25, the pricing weights imply that the actual physical probability of the middle state is 1/2.', 'These are pricing weights; the physical probabilities were only required to be strictly positive.'),
 'q_l23_h2': ('Increasing delta from 4 to 4.4 at stock price 110 reduces the cash account by 44.', 'Increasing a short hedge sells extra stock, receiving 44 in the cash account.'),
 'q_l24_h1': ('For 100<b<200, the high-state probability of beating both rivals is (b−100)/100.', 'Two conditionally independent crossings require the square of that probability.'),
 'q_l24_h2': ('The cross term between T−R and Y−T need not vanish even for the exact conditional expectation T.', 'Conditioning on (P,G) gives E[Y−T|P,G]=0, while T−R is measurable there.'),
}
for id, (text,reason) in DISTRACTORS.items():
    target=next(c for c in reversed(CHECKS[id]) if c['type']=='select')
    target['options'].append(dict(correct=False,text=text,explanation=reason))

# Explicit spoken equivalents keep formula-only checkbox names meaningful after
# KaTeX replaces their visual text. They express claims, never reveal the key.
SPOKEN = {
 'q21:2:1':'With a free intercept, the constant vector belongs to the design space, so the sum of residuals is zero.',
 'q21:2:3':'X transpose times residuals equals zero for the training fit; it does not force the mean prediction error on new data to vanish.',
 'q24:2:1':'Sum of squared deviations from the sample mean equals sum of squared deviations from mu minus n times the squared sample-mean error.',
 'q30:2:1':'Beta hat equals inverse of X transpose X plus lambda I, times X transpose y, even when X lacks full column rank.',
 'q30:2:2':'Ridge training residuals always satisfy X transpose r equals zero.',
 'q30:2:3':'Along singular value s, the response-to-coefficient factor is s divided by s squared plus lambda.',
 'q31:2:1':'For iid additive returns, k-period mean is k mu and variance is k sigma squared.',
 'q31:2:3':'Under stationarity, sum variance is k gamma zero plus twice the sum, for h from one through k minus one, of k minus h times gamma h.',
 'q43:3:1':'Covariance of U squared and the square of the quantity one minus U is minus seven divided by ninety.',
 'q47:2:1':'Pre-specify levels alpha t whose sum is at most 0.05; if each inspection is null-valid, the union bound controls any rejection.',
 'q48:3:1':'The optimal c is covariance of X and Y divided by variance of X.',
 'q50:2:1':'Likelihood is theta to power minus n, times the indicator that theta is at least M, for the stated observed record.',
 'q50:2:3':'Expected M is n theta divided by n plus one, so the MLE is biased down.',
 'q_l02_h1:2:1':'The general posterior is one divided by one plus two s.',
 'q_l05_h2:2:1':'Probability of finite T is at least one minus one over N for every N, hence termination has probability one.',
 'q_l05_h2:2:2':'Pathwise T is at least tau N, so expected T is at least N minus one for every N.',
 'q_l06_h2:3:1':'The tight open intervals are 33 over 17 to 101 over 49, and 101 over 53 to 103 over 51.',
 'q_l07_h2:2:1':'The complete common-correlation range is the closed interval minus one quarter to one.',
 'q_l07_h2:2:3':'X i equals square root of five quarters times Z i minus Z bar, attaining the lower boundary with variance one.',
 'q_l08_h2:1:1':'Whenever two finite sequences have the same first i inputs, their index i outputs from F n must agree, for every n greater than i.',
 'q_l09_h1:2:1':'Risk of c M divided by theta squared equals c squared n over n plus two, minus two c n over n plus one, plus one.',
 'q_l09_h1:2:3':'The minimizing coefficient is n plus two over n plus one, with risk theta squared over the square of n plus one.',
 'q_l09_h2:2:1':'Risk at p equals n p times one minus p, plus a squared times the square of one minus two p, all divided by the square of n plus two a.',
 'q_l09_h2:2:3':'Choose a equal to square root n divided by two; its Beta a a Bayes posterior mean is the same rule, and Bayes risk lower-bounds every supremum risk.',
 'q_l25_h1:2:1':'Likelihood is lambda to power n times exp of minus lambda times sum of x i, divided by one minus exp of minus lambda c, to power n.',
 'q_l25_h1:2:3':'A unique finite positive MLE exists exactly when the sample mean is less than c divided by two; otherwise the open domain has a supremum at zero, not an attained maximum.',
 'q_l10_h1:2:1':'For every zero eigenvalue, the corresponding c i must equal zero.',
 'q_l10_h1:2:3':'With c in the range, feasibility is equivalent to v at least the sum over positive eigenvalues of c i squared divided by lambda i.',
 'q_l10_h2:2:3':'Otherwise optimum variance is one divided by ones transpose Sigma pseudoinverse ones, with weights proportional to Sigma pseudoinverse ones plus any null vector.',
 'q_l11_h2:2:1':'For leverage h i less than one, the deleted fit has full column rank and error r i divided by one minus h i.',
 'q_l12_h2:2:3':'For mu strictly between zero and two c, coverage is Phi of c minus Phi of c minus mu, divided by one minus Phi of c minus mu.',
 'q_l12_h2:2:4':'For mu at least two c, coverage is one minus alpha divided by one minus Phi of c minus mu.',
 'q_l13_m1:2:3':'Variance of Y bar n equals twelve n minus four divided by n squared, for n at least one.',
 'q_l13_m2:2:1':'Covariance of Y t and Y t plus h is k minus absolute h times sigma squared for absolute h less than k, and zero otherwise.',
 'q_l13_m2:2:3':'Variance of mu hat is sigma squared times n k squared minus k times k squared minus one divided by three, all divided by n squared k squared.',
 'q_l13_h1:2:1':'Writing D equal to n minus n minus two times rho, endpoint weights are one over D and each interior weight is one minus rho over D.',
 'q_l13_h1:2:3':'The optimum variance is gamma zero times one plus rho divided by D, and the optimum is unique.',
 'q_l13_h2:2:1':'The limiting ratio is two times c minus one plus exp of minus c, divided by c squared, and is positive.',
 'q_l14_h1:2:3':'Expected square of the average D t equals one over n squared times the sum of expected r t times one minus r t, at most one over four n.',
 'q_l15_h1:2:1':'Expected selected score is theta plus sigma times square root of one minus rho divided by pi.',
 'q_l15_h1:2:3':'Variance of selected score is sigma squared times one minus one minus rho divided by pi, including both endpoints.',
 'q_l16_h1:3:1':'Expected Z conditional on X equals policy pi of X times expected Y conditional on X.',
 'q_l16_h1:3:3':'Expected Z squared equals expected policy pi of X times Y squared divided by e of X; independent mean variance is expected Z squared minus v squared, divided by n.',
 'q_l17_m1:3:1':'u n equals one minus alpha to power one over n, and makes the zero-hit probability equal alpha.',
 'q_l18_m1:2:1':'For delta equal to batch B mean minus batch A mean, merged mean is batch A mean plus delta times batch B count divided by total count.',
 'q_l18_m1:2:3':'Merged M two is both within-batch M two sums plus delta squared times both batch counts divided by total count.',
 'q_l18_h1:2:1':'Remove y using new mean equal to k m minus y over k minus one, and new M two equal to M two minus y minus m times y minus new mean; then use a Welford insertion.',
 'q_l21_h2:2:1':'Admissibility is zero at most f strictly below one ninth, so f equal to 0.2 is invalid.',
 'q_l21_h2:2:3':'g is strictly concave, its derivative at zero is 0.12, and its derivative tends to minus infinity at the upper boundary.',
 'q_l23_h2:3:1':'Initial cash is delta zero times stock zero minus V zero; rehedging cash adds delta i minus delta i minus one, times stock i.',
 'q_l23_h2:3:3':'Terminal wealth is a times the sum of squared stock increments minus b times total elapsed time.',
 'q_l24_h1:3:1':'For b at most one hundred, G of b is one half times one hundred minus b times the square of b over one hundred.',
 'q_l24_h1:3:3':'For b at least one hundred, with x equal to b minus one hundred over one hundred, G is fifty times minus x plus one minus x times x squared, at most zero.',
 'q_l24_h2:2:1':'Expected squared loss of P minus expected squared loss of R equals expected square of P minus R.',
 'q_l24_h2:2:3':'Expected squared loss of R minus expected squared loss of T equals expected square of T minus R; improvement is strict exactly when T differs from R with positive probability.',
}

def attach_objective_assessments(questions):
    written = {q['id'] for q in questions if q['type'] == 'written'}
    if written != set(CHECKS):
        raise ValueError(f'Author objective checks for every written problem: missing={written-set(CHECKS)}, unexpected={set(CHECKS)-written}')
    for q in questions:
        if q['id'] not in CHECKS:
            continue
        q['type'] = 'structured'
        q['assessmentVersion'] = VERSION
        # Deep copy: annotate/build must not mutate the source registry.
        import copy
        q['checks'] = copy.deepcopy(CHECKS[q['id']])
        for i, check in enumerate(q['checks']):
            check['id'] = f'part{i+1}'
            if check['type'] == 'select':
                for j, option in enumerate(check['options']):
                    option['id'] = f'choice{j+1}'
                    option['label'] = SPOKEN.get(f"{q['id']}:{i+1}:{j+1}", option['text'])
                    if r'\(' in option['label']:
                        raise ValueError(f"Author a spoken formula label in {q['id']}")
                # Stable authored IDs survive display reordering. No fixed
                # correct-first position or identical mask across the bank.
                check['options'].sort(key=lambda o: hashlib.sha256(f"{q['id']}:{check['id']}:{o['id']}".encode()).digest())
    validate_assessments(questions)


def validate_assessments(questions):
    for q in questions:
        if q['type'] == 'numeric':
            if not isinstance(q['answer'], (int, float)) or not math.isfinite(q['answer']):
                raise ValueError(f"Invalid numeric answer in {q['id']}")
            continue
        if q['type'] != 'structured' or not q.get('assessmentVersion') or len(q.get('checks', [])) < 2:
            raise ValueError(f"Question {q['id']} needs authored automatic checks")
        ids = [c.get('id') for c in q['checks']]
        if len(ids) != len(set(ids)) or any(not id for id in ids):
            raise ValueError(f"Duplicate/missing checkpoint IDs in {q['id']}")
        for c in q['checks']:
            if not c.get('prompt') or not c.get('type'):
                raise ValueError(f"Incomplete checkpoint in {q['id']}")
            if c['type'] == 'numeric':
                if not isinstance(c.get('answer'), (int,float)) or not math.isfinite(c['answer']) or not (0 < c.get('tolerance',0) <= 1e-6) or not c.get('explanation'):
                    raise ValueError(f"Incomplete numeric checkpoint in {q['id']}")
            elif c['type'] == 'select':
                opts=c.get('options',[])
                if len(opts)<4 or len({o.get('id') for o in opts}) != len(opts) or len({o.get('text') for o in opts}) != len(opts):
                    raise ValueError(f"Incomplete choice checkpoint in {q['id']}")
                if not any(o.get('correct') is True for o in opts) or not any(o.get('correct') is False for o in opts) or any(type(o.get('correct')) is not bool or not o.get('text') or not o.get('explanation') or not o.get('label') for o in opts):
                    raise ValueError(f"Author true and false claims with explanations in {q['id']}")
            else:
                raise ValueError(f"Unknown checkpoint type in {q['id']}")
