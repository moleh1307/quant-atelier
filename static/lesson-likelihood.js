'use strict';
(()=>{
 const R=QuantCourseLessons,{math:m,equation:e,paragraph:p,pause,figure}=R,t=String.raw;
 function logLikelihood(k,n,prob){
  if(!Number.isInteger(n)||n<1||!Number.isInteger(k)||k<0||k>n||!Number.isFinite(prob)||prob<0||prob>1)throw Error('Invalid Bernoulli model');
  if(prob===0)return k===0?0:-Infinity;
  if(prob===1)return k===n?0:-Infinity;
  return (k?k*Math.log(prob):0)+(n-k?(n-k)*Math.log1p(-prob):0);
 }
 function relative(k,n,prob){return Math.exp(logLikelihood(k,n,prob)-logLikelihood(k,n,k/n));}
 const fmt=x=>Number.isFinite(x)?x.toFixed(3):'−∞';
 const x=prob=>52+prob*480,y=value=>224-value*176;
 const profile=(k,n)=>Array.from({length:201},(_,i)=>relative(k,n,i/200));
 const path=values=>values.map((v,i)=>`${i?'L':'M'}${x(i/200).toFixed(2)},${y(v).toFixed(2)}`).join(' ');
 const explorer=figure(`<div class="likelihood-explorer" data-likelihood-explorer>
  <div class="likelihood-controls"><label>Trials <select class="select" data-lk-n aria-label="Number of independent trials"><option>10</option><option>20</option><option>40</option><option>100</option></select></label><label>Successes <output data-lk-k-label>7 / 10</output><input type="range" min="0" max="10" value="7" step="1" data-lk-k aria-label="Observed successes"></label><label><span class="lk-candidate">Candidate p</span> <output data-lk-p-label>0.50</output><input type="range" min="0" max="100" value="50" step="1" data-lk-p aria-label="Candidate success probability"></label></div>
  <svg viewBox="0 0 580 270" role="img" aria-labelledby="likelihood-title likelihood-desc"><title id="likelihood-title">Compare candidate probabilities against a fixed record</title><desc id="likelihood-desc">Relative likelihood for seven successes in ten independent trials. The peak is at 0.7. The candidate is 0.5.</desc>
   <path class="lk-axis" d="M52 40V224H532"/><path class="lk-grid" d="M52 48H532M52 136H532"/><text x="39" y="52" text-anchor="end">1</text><text x="39" y="140" text-anchor="end">½</text><text x="39" y="228" text-anchor="end">0</text><text x="52" y="250" text-anchor="middle">0</text><text x="292" y="250" text-anchor="middle">0.5</text><text x="532" y="250" text-anchor="middle">1</text><text x="292" y="267" text-anchor="middle">candidate success probability p</text><text x="52" y="24">L(p) / L(p̂) · relative likelihood</text>
   <path class="lk-curve" data-lk-curve d="${path(profile(7,10))}"/>
   <g class="lk-peak" data-lk-peak style="transform:translateX(${x(.7)}px)"><path d="M0 43V224"/><circle cy="48" r="4"/></g>
   <g class="lk-marker" data-lk-marker style="transform:translate(${x(.5)}px,${y(relative(7,10,.5))}px)"><circle r="6"/></g>
  </svg><div class="likelihood-readout"><span>Best fit <strong class="lk-fit" data-lk-best>p̂ = 0.70</strong></span><span>Log-likelihood <strong data-lk-log>${fmt(logLikelihood(7,10,.5))}</strong></span><span>Relative likelihood <strong class="lk-candidate" data-lk-ratio>${relative(7,10,.5).toFixed(3)}</strong></span></div>
  <p class="likelihood-note" data-lk-note>The candidate p = 0.50 gives this record 0.439 times the likelihood of the best fit.</p>
 </div>`, `The <span class="lk-fit">green line marks the best fit</span>; the <span class="lk-candidate">ochre dot follows your candidate</span>. These are comparisons of models for the same record. The curve is not a probability distribution over p. Controls are ungraded.`);
 const support=figure(`<svg class="likelihood-support" viewBox="0 0 580 185" role="img" aria-labelledby="lk-support-title lk-support-desc"><title id="lk-support-title">An endpoint must contain the observed data</title><desc id="lk-support-desc">Observed values are 0.2, 0.5 and 0.8. An endpoint of 0.6 excludes the last observation and has zero likelihood. An endpoint of 0.8 contains all observations and maximizes the likelihood.</desc><text x="20" y="28">same observed record: 0.2, 0.5, 0.8</text><path class="lk-axis" d="M60 80H510M60 145H510"/><path class="lk-impossible" d="M60 80H330"/><path class="lk-feasible" d="M60 145H420"/><g class="lk-observation"><circle cx="150" cy="80" r="5"/><circle cx="285" cy="80" r="5"/><circle cx="420" cy="80" r="5"/><circle cx="150" cy="145" r="5"/><circle cx="285" cy="145" r="5"/><circle cx="420" cy="145" r="5"/></g><path class="lk-impossible" d="M330 65V95"/><path class="lk-feasible" d="M420 130V160"/><text x="60" y="65">θ = 0.6 · excludes 0.8</text><text x="60" y="128">θ = 0.8 · smallest feasible endpoint</text><text x="60" y="178">0</text><text x="510" y="178">1</text></svg>`, 'First rule out models that cannot produce the record. Among the feasible uniform endpoints, a shorter interval has a higher density. The optimum sits at the support boundary.');
 R.register('l25',{
  opening:R.opening('Seven successes. Ten trials. Which model makes that record less surprising?', 'In the estimation lesson, we compared rules for turning data into an estimate. Here we build one of those rules from the probability model itself. The important step is choosing what remains fixed and what is allowed to change.'),
  sections:[
   ['Read the record before fitting the model',
    p(`Imagine ten trials recorded in order: <strong>H, H, T, H, T, H, H, T, H, H</strong>. Encode a success as ${m('x_i=1')} and a failure as ${m('x_i=0')}. There are ${m('n=10')} observations and ${m(t`k=\sum_i x_i=7`)} successes. Assume the trials are <strong>independent</strong>, each with the <strong>same unknown</strong> success probability ${m('p')}. That is an iid Bernoulli model, with parameter domain ${m(t`0\le p\le1`)}.`)+
    p(`For a proposed ${m('p=0.5')}, each of the ten factors is one half. For ${m('p=0.7')}, the seven successes contribute factors of 0.7 and the three failures factors of 0.3. Multiplication is justified by independence; it is not justified merely because the data came in ten rows.`)+
    e(t`L(p;x)=\prod_{i=1}^{n}p^{x_i}(1-p)^{1-x_i}=p^k(1-p)^{n-k}.`)+
    p(`The notation ${m('L(p;x)')} is read “likelihood of p for the observed record x.” The semicolon separates the value we vary, p, from the record we hold fixed, x. At this stage p is an unknown parameter, not a random variable with an assigned distribution. A candidate is judged by how much probability its model assigns to the actual record.`)+
    e(t`\frac{L(0.7;x)}{L(0.5;x)}=\frac{0.7^7\,0.3^3}{0.5^{10}}\approx2.28.`)+
    p('The 0.7 model makes this particular record about 2.28 times as likely as the 0.5 model. That is a comparison, not proof that the first model is true. A different sample can favor a different parameter, and both candidates can be poor descriptions of the real sampling mechanism.')],
   ['Change the candidate, keep the evidence fixed',
    p('Move the candidate probability along the curve below. Its height compares your candidate with the best fit for the selected observations. Then change the number of successes: the preferred model should move because the evidence changed. Finally increase the trial count while keeping the success fraction fixed; the curve should narrow because more independent observations make disagreement more costly.')+
    explorer+
    p(`The plotted quantity is ${m(t`R(p)=L(p;x)/L(\hat p;x)`)}. The denominator is constant as you compare p values for one record, so the peak stays at the same place and has height one. Values near zero mean that the record is much less compatible with that candidate than with the best-fitting candidate. A displayed value rounded to zero is not necessarily a mathematically impossible observation.`)+
    pause('Predict before moving: what happens if all ten trials are successes?',p('Every factor favors increasing p. The best fit moves to p = 1 on the closed parameter interval. There is no interior peak. If the model instead excludes p = 1, the likelihood approaches its supremum there without attaining it. The allowed parameter domain changes the existence of the answer.'))],
   ['Probability and likelihood turn the same expression in different directions',
    p(`With <strong>p fixed</strong>, ${m('P_p(X=x)')} varies over possible records and sums to one across those records. With <strong>x fixed</strong>, ${m('L(p;x)')} varies over candidate parameters. It need not integrate to one over p. The same expression has become a different mathematical object because its argument changed.`)+
    p(`Recording only the count ${m('K=k')} also changes the expression. There are ${m(t`\binom nk`)} ordered Bernoulli records with that count, all equally likely under this common-p model:`)+
    e(t`P_p(K=k)=\binom nk p^k(1-p)^{n-k}.`)+
    p(`For fixed n and k, the binomial coefficient does not depend on p. It changes the numerical likelihood, but cancels from likelihood ratios and does not move the maximizer. Drop a factor only after explaining why it is constant in the parameter being optimized. A factor depending on p cannot be discarded this way.`)+
    p(`For continuous observations, use the joint <strong>density</strong> ${m('f(x;p)')}. The probability of one exact real-valued record is usually zero; a density measures probability per unit volume. Densities can exceed one. Comparing them is meaningful for a fixed observation model and fixed measurement units, but calling a density “the probability of this exact record” is wrong.`)+
    p(`To obtain a posterior, you need a prior density ${m(t`\pi(p)`)} and a finite, positive normalizing integral:`)+
    e(t`\pi(p\mid x)=\frac{L(p;x)\pi(p)}{\int_0^1L(u;x)\pi(u)\,du}.`)+
    p('A flat prior happens to produce a posterior proportional to likelihood in this parameterization. It is still an added modeling choice. Maximizing likelihood alone does not give a probability that p is 0.7, a credible interval, or a guarantee about the next trial.')],
   ['The logarithm exposes the tradeoff',
    p(`A maximum likelihood estimate, abbreviated MLE, is a parameter value attaining the largest likelihood within the stated domain. Write ${m(t`\hat p\in\operatorname*{arg\,max}_{0\le p\le1} L(p;x)`)}; the set notation allows several maximizers. First work in the interior ${m('0<p<1')} with ${m('0<k<n')}. Since the natural logarithm is strictly increasing, it preserves the order of positive likelihoods:`)+
    e(t`\ell(p)=\log L(p;x)=k\log p+(n-k)\log(1-p).`)+
    p('This transformation also replaces a long product of tiny numbers with a sum. Computation benefits, but the mathematical optimization problem stays the same. The two terms pull in opposite directions: successes reward raising p; failures reward lowering it.')+
    e(t`\ell'(p)=\frac{k}{p}-\frac{n-k}{1-p}=\frac{k-np}{p(1-p)}.`)+
    p(`The numerator vanishes at ${m(t`\hat p=k/n`)}. That stationary point is a maximum, rather than merely a convenient solution to an equation, because`)+
    e(t`\ell''(p)=-\frac{k}{p^2}-\frac{n-k}{(1-p)^2}<0.`)+
    p(`Strict concavity gives a unique interior maximum. When both successes and failures occur, either endpoint makes the record impossible and has zero likelihood. When ${m('k=0')}, however, ${m('L(p)=(1-p)^n')} decreases across the domain and maximizes at zero. When ${m('k=n')}, ${m('L(p)=p^n')} increases and maximizes at one. These boundary cases must be evaluated directly, not forced through a derivative with a zero denominator.`)+
    pause('Does “the MLE is 0” after ten failures establish an impossible success?',p('No. It is the best-fitting value within the specified model for that sample. A small positive p can also generate ten failures. Reporting an endpoint estimate as certainty confuses fitting with uncertainty; a prior, a confidence procedure, or a likelihood comparison addresses additional questions.'))+
    p('In the linked Python exercise, you will compute this log-likelihood without forming the probability product. Near zero, use a numerically stable logarithm of one minus p. This is a reason to write code: a correct algebraic expression can still lose information when evaluated carelessly.')],
   ['A maximum can live where the model starts being possible',
    p(`Now change the model. Observe independent uniform measurements ${m('0.2,0.5,0.8')} from an interval ${m(t`[0,\theta]`)}, with unknown endpoint ${m(t`\theta>0`)}. Let ${m(t`M=\max_i x_i=0.8`)}. Specify the density as ${m(t`f(x;\theta)=\theta^{-1}\mathbf1\{0\le x\le\theta\}`)}. That support indicator is part of the likelihood.`)+
    support+
    e(t`L(\theta;x)=\theta^{-n}\mathbf1\{\theta\ge M\},\qquad \hat\theta=M.`)+
    p(`An endpoint below M cannot have generated the observed maximum. For feasible endpoints, ${m(t`\theta^{-n}`)} strictly decreases as the interval expands. The smallest feasible endpoint is therefore the global maximum. Differentiating ${m(t`-n\log\theta`)} and complaining that there is no stationary point misses the boundary constraint. Check <strong>support and domain before calculus</strong>.`)+
    p(`This fit is not unbiased. Under the uniform model, ${m(t`P(M\le z)=(z/\theta)^n`)} for ${m(t`0\le z\le\theta`)}, because all n observations must lie below z. Integrating the resulting density gives ${m(t`E[M]=n\theta/(n+1)`)}. The correction ${m('(n+1)M/n')} removes this bias, but ceases to maximize likelihood. The previous lesson's distinction between fitting criteria and repeated-sample risk matters here.`)+
    pause('Why specify a closed-support density so carefully?',p('Including or excluding a single endpoint leaves a continuous probability law unchanged. But a strict support convention θ > M excludes the proposed maximizer: the likelihood has the same supremum, approached as θ decreases to M, without an attained maximum. Boundary estimation can depend on the density version. We specified the closed-support version so the stated optimization has an unambiguous answer.'))],
   ['The normal model connects fitting to squared error',
    p(`Suppose instead ${m(t`X_i\overset{\mathrm{iid}}\sim N(\mu,v)`)} with unknown mean ${m(t`\mu\in\mathbb R`)} and variance ${m('v>0')}. We write v for variance to keep differentiation clear. The joint log-density of a fixed record is`)+
    e(t`\ell(\mu,v)=-\frac n2\log(2\pi)-\frac n2\log v-\frac{1}{2v}\sum_i(x_i-\mu)^2.`)+
    p(`For any fixed positive v, maximize this by minimizing the sum of squared deviations. The identity ${m(t`\sum_i(x_i-\mu)^2=\sum_i(x_i-\bar x)^2+n(\bar x-\mu)^2`)} shows that the unique best center is ${m(t`\hat\mu=\bar x`)}. This is the statistical reason squared error appears in a normal location model; it is not a universal loss for every distribution.`)+
    p(`Let ${m(t`S=\sum_i(x_i-\bar x)^2`)} and assume ${m('S>0')}. Substitution leaves a one-variable problem:`)+
    e(t`\frac{\partial\ell(\bar x,v)}{\partial v}=\frac{S-nv}{2v^2},\qquad\hat v=\frac Sn.`)+
    p(`The derivative is positive before S/n and negative after it, giving a global maximum. For the observations 1, 2 and 3, the fitted mean is 2, S is 2, and the fitted variance is ${m('2/3')}. The unbiased sample variance is ${m('S/(n-1)=1')}. One denominator maximizes a joint density; the other corrects repeated-sample bias. Neither is a typo.`)+
    pause('What if all observed values are identical?',p('Then S = 0. At the common value of μ, the log-density increases without bound as v decreases toward zero. Since the normal model requires v > 0, there is no finite positive-variance MLE. Setting v = 0 is not a valid member of this model. A minimum variance constraint or a prior changes the problem and must be stated.'))],
   ['A sharp curve can still be confidently wrong',
    p(`For an interior Bernoulli fit, the downward log-likelihood curvature at the optimum is ${m(t`-\ell''(\hat p)=n/[\hat p(1-\hat p)]`)}. At a fixed observed proportion, increasing n increases curvature. The interactive curve shows this concentration. Curvature measures local sensitivity <strong>under the assumed observation model</strong>; it does not certify that the model is right.`)+
    p(`Imagine one Bernoulli success copied a hundred times. There was one random event, so the actual likelihood is p. Treating the copies as independent manufactures ${m('p^{100}')}. Both maximize at one, yet the ratio comparing p = 0.5 with p = 1 changes from 0.5 to ${m('2^{-100}')}. The reported estimate can look unchanged while its apparent evidential strength becomes absurd.`)+
    p(`Dependence does not make likelihood impossible. The chain rule always allows a joint model to factor into conditionals:`)+
    e(t`f(x_1,\ldots,x_n;\theta)=f(x_1;\theta)\prod_{i=2}^n f(x_i\mid x_1,\ldots,x_{i-1};\theta).`)+
    p('An iid assumption replaces those conditionals with a common marginal model. For market observations, ask whether serial dependence, shared regimes, duplicate records or changing exposure invalidate that simplification. Distinct rows with the same value are not automatically duplicates; the sampling process determines the observation unit.')+
    p('Selection also matters. If you retain only values above a threshold, the retained observations follow a conditional, truncated distribution. Its normalization often depends on the parameter and belongs in the likelihood. A smooth optimizer cannot repair an observation model that ignores how the sample was selected. Later inference and validation modules address uncertainty and held-out evidence; a good fit here is only the beginning.')]
  ],
  exampleTitle:'Transfer the method: waiting times and unfinished waits',
  example:p(`Assume independent exponential waiting times with a common rate ${m(t`\lambda>0`)}, measured in events per second. For a completed wait ${m(t`x\ge0`)}, the density is ${m(t`\lambda e^{-\lambda x}`)}. For completed waits 1, 2, 3 and 4 seconds, the total exposure is ${m('T=10')} seconds and there are ${m('d=4')} observed events.`)+
   e(t`L(\lambda)=\lambda^4e^{-10\lambda},\qquad\ell'(\lambda)=\frac4\lambda-10,\qquad\hat\lambda=0.4\ \mathrm{s}^{-1}.`)+
   p('The sample mean wait is 2.5 seconds; the estimated rate is its reciprocal. Always check units: a mean duration and a rate are different parameters. The second derivative is negative, and the likelihood approaches zero at either end of the positive-rate domain, confirming the global maximum.')+
   p(`Now suppose a clock stops before some waits finish. Observing “no event by time c” is right-censoring. It contributes the survival probability ${m(t`P(X>c)=e^{-\lambda c}`)}, not an event density. Under fixed censoring limits, or a censoring mechanism independent of event times with parameter-free factors, multiply event densities and survival factors:`)+
   e(t`L(\lambda)\propto\lambda^d e^{-\lambda T},\qquad\hat\lambda=\frac dT\quad(d>0).`)+
   p(`T includes time at risk from <strong>both completed and censored waits</strong>. Two events over ten seconds of total exposure give ${m(t`0.2\ \mathrm{s}^{-1}`)}. Dropping unfinished waits discards real information: they tell you an event did not happen during their exposure. Informative censoring requires modeling the censoring mechanism rather than this simplified factorization.`)+
   pause('No events over ten seconds: should the answer be a positive number?',p('The likelihood is exp(−10λ), strictly decreasing for λ > 0. Its supremum occurs as λ approaches zero, but zero is excluded here. There is no positive-rate maximizer. Reporting zero as a limit or adding a prior is a separate choice; neither proves that events can never occur.'))+
   p('When solving a new likelihood problem, narrate the sampling assumptions, write the probability or density of what was actually observed, identify support and parameter domain, optimize, and check whether the optimum is attained. Then distinguish the fitting answer from claims about bias, uncertainty or predictive usefulness. The linked practice asks you to make those distinctions without relying on a memorized formula.'),
  models:{logLikelihood,relative,profile},
  bind(root){
   const box=root.querySelector('[data-likelihood-explorer]');if(!box)return;
   const get=s=>box.querySelector(s),nInput=get('[data-lk-n]'),kInput=get('[data-lk-k]'),pInput=get('[data-lk-p]'),curve=get('[data-lk-curve]');
   let displayed=profile(Number(kInput.value),Number(nInput.value)),frame=null,previousN=Number(nInput.value);
   function draw(target){
    if(frame!==null&&typeof cancelAnimationFrame==='function')cancelAnimationFrame(frame);
    const reduced=typeof matchMedia==='function'&&matchMedia('(prefers-reduced-motion: reduce)').matches;
    if(reduced||typeof requestAnimationFrame!=='function'){displayed=target;curve.setAttribute('d',path(target));return;}
    const from=displayed.slice();let start=null;
    const tick=time=>{if(!box.isConnected){frame=null;return;}if(start===null)start=time;const progress=Math.min(1,(time-start)/440),ease=1-(1-progress)**3;displayed=from.map((v,i)=>v+(target[i]-v)*ease);curve.setAttribute('d',path(displayed));frame=progress<1?requestAnimationFrame(tick):null;};
    frame=requestAnimationFrame(tick);
   }
   function update(changeModel){
    const n=Number(nInput.value);if(n!==previousN){const scaled=Math.round(Number(kInput.value)*n/previousN);kInput.max=String(n);kInput.value=String(scaled);previousN=n;}
    const k=Number(kInput.value),prob=Number(pInput.value)/100,ratio=relative(k,n,prob);
    get('[data-lk-k-label]').textContent=`${k} / ${n}`;get('[data-lk-p-label]').textContent=prob.toFixed(2);get('[data-lk-best]').textContent=`p̂ = ${(k/n).toFixed(2)}`;get('[data-lk-log]').textContent=fmt(logLikelihood(k,n,prob));get('[data-lk-ratio]').textContent=ratio.toFixed(3);
    get('[data-lk-peak]').style.transform=`translateX(${x(k/n)}px)`;get('[data-lk-marker]').style.transform=`translate(${x(prob)}px,${y(ratio)}px)`;
    const note=ratio===0?'This candidate makes the observed record impossible.':`The candidate p = ${prob.toFixed(2)} gives this record ${ratio.toFixed(3)} times the likelihood of the best fit.`;
    get('[data-lk-note]').textContent=note;get('#likelihood-desc').textContent=`Relative likelihood for ${k} successes in ${n} independent trials. Best fit ${k/n}; candidate ${prob}; relative likelihood ${ratio}.`;
    if(changeModel)draw(profile(k,n));
   }
   nInput.addEventListener('change',()=>update(true));kInput.addEventListener('input',()=>update(true));pInput.addEventListener('input',()=>update(false));
  }
 });
})();
