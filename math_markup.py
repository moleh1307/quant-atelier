"""Author-time mathematical notation for the original practice library.

Exact, reviewed expressions become explicit TeX spans. This only touches prose;
Python sources, sample arguments, numeric answers and saved drafts stay literal.
Keep new material in explicit \\(inline\\) or \\[display\\] delimiters.
"""
import re

# Longest match wins; replacements are never fed back into the matcher.
FORMULAS = {
    '19/4=4.75': r'\frac{19}{4}=4.75',
    '1/8−1/16=1/16': r'\frac18-\frac1{16}=\frac1{16}',
    '161/36≈4.47222': r'\frac{161}{36}\approx4.47222',
    '3+2=5': r'3+2=5', 'n=100': r'n=100', 'n=4,max=8': r'n=4,\quad\max=8',
    'n=4': r'n=4', '[−1,1]': r'[-1,1]', '[0,θ]': r'[0,\theta]',
    '29/110≈26.4%': r'\frac{29}{110}\approx26.4\%',
    '81/110≈73.6%': r'\frac{81}{110}\approx73.6\%',
    '1/4+1/4=1/2': r'\frac14+\frac14=\frac12',
    'conditional fair value=200/3': r'\text{conditional fair value}=\frac{200}{3}',
    'Portfolio variance=0.25×4+0.25×4+2×0.25×2=3': r'\text{Portfolio variance}=0.25\times4+0.25\times4+2\times0.25\times2=3',
    'P(A)=|A|/|Ω|': r'P(A)=\frac{|A|}{|\Omega|}',
    'C(n,2)': r'\binom{n}{2}',
    'C(10,2)': r'\binom{10}{2}',
    'P(A∪B)=P(A)+P(B)−P(A∩B)': r'P(A\cup B)=P(A)+P(B)-P(A\cap B)',
    'P(A|B)=P(A∩B)/P(B)': r'P(A\mid B)=\frac{P(A\cap B)}{P(B)}',
    'P(B)>0': r'P(B)>0',
    'P(at least one H)': r'P(\text{at least one H})',
    'P(always-heads)': r'P(\text{always-heads})',
    'prior×likelihood': r'\text{prior}\times\text{likelihood}',
    'ΣI_i': r'\sum_i I_i',
    'E[count]=ΣP(I_i=1)': r'\mathbb{E}[\text{count}]=\sum_i P(I_i=1)',
    'E[N]=Σ_(k≥1)P(N≥k)': r'\mathbb{E}[N]=\sum_{k\geq1}P(N\geq k)',
    'E[X]=∫₀∞P(X>x)dx': r'\mathbb{E}[X]=\int_0^\infty P(X>x)\,dx',
    'Uniform(0,1)': r'\operatorname{Uniform}(0,1)',
    'Uniform(0,θ)': r'\operatorname{Uniform}(0,\theta)',
    'U~Uniform(0,1)': r'U\sim\operatorname{Uniform}(0,1)',
    'P(max≤x)=x^n': r'P(\max\leq x)=x^n',
    'P(min>x)=(1−x)^n': r'P(\min>x)=(1-x)^n',
    'n/(n+1)': r'\frac{n}{n+1}',
    '1/(n+1)': r'\frac{1}{n+1}',
    'exp(−λt)': r'e^{-\lambda t}',
    '1/λ': r'\frac{1}{\lambda}',
    'λ_i/Σλ_j': r'\frac{\lambda_i}{\sum_j\lambda_j}',
    'E₀=1+(E₀+E_H)/2': r'E_0=1+\frac{E_0+E_H}{2}',
    'E_H=1+E₀/2': r'E_H=1+\frac{E_0}{2}',
    'E_H=1+E_H/2': r'E_H=1+\frac{E_H}{2}',
    'E₀=4': r'E_0=4', 'E₀=6': r'E_0=6', 'E_H=2': r'E_H=2',
    '49×21': r'49\times21', '50×21−21=1029': r'50\times21-21=1029',
    '10%+8%=25+20=45': r'10\%+8\%=25+20=45',
    '1/8=0.125': r'\frac18=0.125', '1/6≈0.1667': r'\frac16\approx0.1667',
    '1/7≈0.142857': r'\frac17\approx0.142857',
    '97×103=(100−3)(100+3)=10000−9=9991': r'97\times103=(100-3)(100+3)=10000-9=9991',
    'Var(aX+b)=a²Var(X)': r'\operatorname{Var}(aX+b)=a^2\operatorname{Var}(X)',
    'Var(X+Y)=Var(X)+Var(Y)+2Cov(X,Y)': r'\operatorname{Var}(X+Y)=\operatorname{Var}(X)+\operatorname{Var}(Y)+2\operatorname{Cov}(X,Y)',
    'Var(X̄)=n^(−2)Σ_iΣ_j Cov(X_i,X_j)': r'\operatorname{Var}(\bar X)=\frac{1}{n^2}\sum_i\sum_j\operatorname{Cov}(X_i,X_j)',
    'σ²[ρ+(1−ρ)/n]': r'\sigma^2\left[\rho+\frac{1-\rho}{n}\right]',
    'n=100,σ²=1,ρ=0.1': r'n=100,\quad\sigma^2=1,\quad\rho=0.1',
    'Var(mean)=0.109': r'\operatorname{Var}(\bar X)=0.109',
    'Var(3X+2)': r'\operatorname{Var}(3X+2)', 'Var(X)=4': r'\operatorname{Var}(X)=4',
    'E[θ̂]−θ': r'\mathbb{E}[\hat\theta]-\theta',
    'nθ/(n+1)': r'\frac{n\theta}{n+1}', '(n+1)/n': r'\frac{n+1}{n}',
    'MSE=Var(θ̂)+Bias(θ̂)²': r'\operatorname{MSE}(\hat\theta)=\operatorname{Var}(\hat\theta)+\operatorname{Bias}(\hat\theta)^2',
    'wᵀΣw≥0': r'w^{\mathsf T}\Sigma w\geq0', 'Var(wᵀX)': r'\operatorname{Var}(w^{\mathsf T}X)',
    'wᵀΣw': r'w^{\mathsf T}\Sigma w',
    '||y−Xβ||²+λ||β||²': r'\lVert y-X\beta\rVert^2+\lambda\lVert\beta\rVert^2',
    '||y−Xβ||²': r'\lVert y-X\beta\rVert^2',
    'XᵀXβ=Xᵀy': r'X^{\mathsf T}X\beta=X^{\mathsf T}y',
    'Xᵀr=0': r'X^{\mathsf T}r=0', 'XᵀX': r'X^{\mathsf T}X', 'λI': r'\lambda I',
    'Y=2X+ε,W=X+u': r'Y=2X+\varepsilon,\quad W=X+u',
    'Var(X)=1,Var(u)=3': r'\operatorname{Var}(X)=1,\quad\operatorname{Var}(u)=3',
    'p=0.03': r'p=0.03',
    'Var(Σ_(t=1)^n X_t)=nγ₀+2Σ_(h=1)^(n−1)(n−h)γ_h': r'\operatorname{Var}\!\left(\sum_{t=1}^n X_t\right)=n\gamma_0+2\sum_{h=1}^{n-1}(n-h)\gamma_h',
    '|ρ|<1': r'|\rho|<1', '(1+ρ)/(1−ρ)': r'\frac{1+\rho}{1-\rho}',
    'n(1−ρ)/(1+ρ)': r'\frac{n(1-\rho)}{1+\rho}', '√k': r'\sqrt{k}',
    'ρ=0.8': r'\rho=0.8', 's/√n': r'\frac{s}{\sqrt n}',
    'Cov(X,Y)/Var(X)': r'\frac{\operatorname{Cov}(X,Y)}{\operatorname{Var}(X)}',
    '(1−U)²': r'(1-U)^2', 'U²': r'U^2',
    'O(n)': r'O(n)', 'O(window)': r'O(\text{window})', 'O(k)': r'O(k)',
    'fair−ask>cost': r'\text{fair}-\text{ask}>\text{cost}',
    'bid−fair>cost': r'\text{bid}-\text{fair}>\text{cost}', 'f=2p−1': r'f=2p-1',
    'C−P=S−D−K exp(−rT)': r'C-P=S-D-Ke^{-rT}',
    'C−P=S−K exp(−rT)': r'C-P=S-Ke^{-rT}', 'S_T−K': r'S_T-K',
    'ΔV≈delta ΔS+½ gamma (ΔS)²+theta Δt': r'\Delta V\approx\delta\,\Delta S+\frac12\gamma(\Delta S)^2+\theta\,\Delta t',
    '(5/6)²': r'\left(\frac56\right)^2', '(5/6)^n < 0.1': r'\left(\frac56\right)^n<0.1',
    'n > 12.63': r'n>12.63', '(1/2)/(3/4)=2/3': r'\frac{1/2}{3/4}=\frac23',
    '1/(1+2^(-k))': r'\frac{1}{1+2^{-k}}',
    '0.02×0.9² / (0.02×0.9²+0.98×0.1²)=81/130≈0.62308': r'\frac{0.02\times0.9^2}{0.02\times0.9^2+0.98\times0.1^2}=\frac{81}{130}\approx0.62308',
    'P(useful | pass)=0.018/(0.018+0.098)=9/58≈0.15517': r'P(\text{useful}\mid\text{pass})=\frac{0.018}{0.018+0.098}=\frac9{58}\approx0.15517',
    '0.02×0.9': r'0.02\times0.9', '0.98×0.1': r'0.98\times0.1', '6×4': r'6\times4',
    '(6/10)(4/9)+(4/10)(6/9)': r'\frac6{10}\frac49+\frac4{10}\frac69',
    '2rb/[(r+b)(r+b-1)]': r'\frac{2rb}{(r+b)(r+b-1)}',
    '(3(n−1)+2(n−2))/16=(5n−7)/16': r'\frac{3(n-1)+2(n-2)}{16}=\frac{5n-7}{16}',
    'n≥2': r'n\geq2',
    'P(max=k)=(k²−(k−1)²)/36=(2k−1)/36': r'P(\max=k)=\frac{k^2-(k-1)^2}{36}=\frac{2k-1}{36}',
    'P(max≤k)=k²/36': r'P(\max\leq k)=\frac{k^2}{36}',
    'P(max=k)': r'P(\max=k)', 'k(2k−1)/36': r'\frac{k(2k-1)}{36}',
    'E[min]=7−161/36=91/36': r'\mathbb E[\min]=7-\frac{161}{36}=\frac{91}{36}',
    'P(min>x)=(1−x)³': r'P(\min>x)=(1-x)^3', '0≤x≤1': r'0\leq x\leq1',
    'E[M]=∫P(M>x)dx': r'\mathbb E[M]=\int P(M>x)\,dx',
    '∫₀¹(1−x)³dx=1/4': r'\int_0^1(1-x)^3\,dx=\frac14',
    'P(max≤x)=x³': r'P(\max\leq x)=x^3', 'E[max]=3/4': r'\mathbb E[\max]=\frac34',
    'E[max]': r'\mathbb E[\max]', 'm(1+1/2+…+1/m)': r'm\left(1+\frac12+\cdots+\frac1m\right)',
    'E₂=1+E₀/2': r'E_2=1+\frac{E_0}{2}',
    'E₁=1+(E₂+E₀)/2': r'E_1=1+\frac{E_2+E_0}{2}',
    'E₀=1+(E₁+E₀)/2': r'E_0=1+\frac{E_1+E_0}{2}',
    'E₁=E₀−2': r'E_1=E_0-2', 'E₀−2=1+(1+1.5E₀)/2': r'E_0-2=1+\frac{1+1.5E_0}{2}',
    'E₀=14': r'E_0=14', '1/P(HHH)=8': r'\frac1{P(HHH)}=8',
    '(1−p^k)/[(1−p)p^k]': r'\frac{1-p^k}{(1-p)p^k}', '0<p<1': r'0<p<1', 'p=1': r'p=1',
    't_i=1+(t_(i−1)+t_(i+1))/2': r't_i=1+\frac{t_{i-1}+t_{i+1}}2',
    't_0=t_12=0': r't_0=t_{12}=0', 't_i=i(12−i)': r't_i=i(12-i)', 't_5=35': r't_5=35',
    'p_i=(p_(i−1)+p_(i+1))/2': r'p_i=\frac{p_{i-1}+p_{i+1}}2',
    'p_0=0,p_12=1': r'p_0=0,\quad p_{12}=1', 'i/12': r'\frac{i}{12}',
    '(3×3.5+4+5+6)/6=4.25': r'\frac{3\times3.5+4+5+6}{6}=4.25',
    'Mean=(2×2.5+3+4+5+6)/6=23/6': r'\text{Mean}=\frac{2\times2.5+3+4+5+6}{6}=\frac{23}{6}',
    'U<V': r'U<V', 'U,V−U,1−V': r'U,\ V-U,\ 1-V', '0<U<V<1': r'0<U<V<1',
    'U<1/2': r'U<\frac12', 'V>1/2': r'V>\frac12', 'V−U<1/2': r'V-U<\frac12',
    '1/rate': r'\frac1{\text{rate}}', 'E[T−3 | T>3]=2': r'\mathbb E[T-3\mid T>3]=2',
    'P(T>7 | T>3)': r'P(T>7\mid T>3)', 'exp(−(1/2)×4)=exp(−2)': r'e^{-(1/2)\times4}=e^{-2}',
    'f_X(t)P(Y>t)': r'f_X(t)P(Y>t)', '3 exp(−5t)': r'3e^{-5t}',
    '∫₀∞3e^(−3t)e^(−2t)dt=3/5': r'\int_0^\infty3e^{-3t}e^{-2t}\,dt=\frac35',
    '3e^(−5t)': r'3e^{-5t}', '5e^(−5t)': r'5e^{-5t}',
    'Var(mean)=[n+n(n−1)ρ]/n²=ρ+(1−ρ)/n=0.109': r'\operatorname{Var}(\bar X)=\frac{n+n(n-1)\rho}{n^2}=\rho+\frac{1-\rho}{n}=0.109',
    'ρ≥−1/(n−1)': r'\rho\geq-\frac1{n-1}', 'ρ=0.1': r'\rho=0.1',
    'σ²/n_eff': r'\frac{\sigma^2}{n_{\mathrm{eff}}}', 'n_eff': r'n_{\mathrm{eff}}',
    'ρ^k': r'\rho^k', '1+2Σρ^k=(1+ρ)/(1−ρ)': r'1+2\sum_{k=1}^\infty\rho^k=\frac{1+\rho}{1-\rho}',
    '100×0.2/1.8=100/9≈11.11': r'\frac{100\times0.2}{1.8}=\frac{100}{9}\approx11.11',
    'Var(mean)/[γ₀/n]=1+2Σ_(k=1)^(n−1)(1−k/n)ρ^k': r'\frac{\operatorname{Var}(\bar X)}{\gamma_0/n}=1+2\sum_{k=1}^{n-1}\left(1-\frac{k}{n}\right)\rho^k',
    'Y=2X+ε': r'Y=2X+\varepsilon', 'W=X+u': r'W=X+u',
    'Var(X)=1': r'\operatorname{Var}(X)=1', 'Var(u)=3': r'\operatorname{Var}(u)=3',
    'Cov(W,Y)/Var(W)': r'\frac{\operatorname{Cov}(W,Y)}{\operatorname{Var}(W)}',
    'Cov(W,Y)=2Var(X)=2': r'\operatorname{Cov}(W,Y)=2\operatorname{Var}(X)=2',
    'Var(W)=1+3=4': r'\operatorname{Var}(W)=1+3=4', 'Cov(u,ε)': r'\operatorname{Cov}(u,\varepsilon)',
    'Corr(X,Y)=Corr(Y,Z)=0.8': r'\operatorname{Corr}(X,Y)=\operatorname{Corr}(Y,Z)=0.8',
    'a=Corr(X,Y), b=Corr(Y,Z), c=Corr(X,Z)': r'a=\operatorname{Corr}(X,Y),\quad b=\operatorname{Corr}(Y,Z),\quad c=\operatorname{Corr}(X,Z)',
    '(c−ab)²≤(1−a²)(1−b²)': r'(c-ab)^2\leq(1-a^2)(1-b^2)',
    'ab±√[(1−a²)(1−b²)]': r'ab\pm\sqrt{(1-a^2)(1-b^2)}',
    '0.64±0.36': r'0.64\pm0.36', 'c≥0.28': r'c\geq0.28',
    'X=0.8Y+0.6U': r'X=0.8Y+0.6U', 'Z=0.8Y−0.6U': r'Z=0.8Y-0.6U',
    'Corr(X,Z)=0.64−0.36=0.28': r'\operatorname{Corr}(X,Z)=0.64-0.36=0.28',
    'Corr(X,Z)': r'\operatorname{Corr}(X,Z)',
    'Σ(y_i−a−bᵀx_i)²': r'\sum_i(y_i-a-b^{\mathsf T}x_i)^2', '−2Σr_i=0': r'-2\sum_i r_i=0',
    '90%>80%,20%>10%': r'90\%>80\%,\quad20\%>10\%',
    'E[max]=nθ/(n+1)': r'\mathbb E[\max]=\frac{n\theta}{n+1}',
    '(m/θ)^n': r'\left(\frac m\theta\right)^n', '(n+1)max/n': r'\frac{(n+1)\max}{n}',
    'Σ(X_i−X̄)²/n': r'\frac1n\sum_i(X_i-\bar X)^2',
    'Σ(X_i−X̄)²=Σ(X_i−μ)²−n(X̄−μ)²': r'\sum_i(X_i-\bar X)^2=\sum_i(X_i-\mu)^2-n(\bar X-\mu)^2',
    'Var(X̄)=σ²/n': r'\operatorname{Var}(\bar X)=\frac{\sigma^2}{n}',
    'n Var(X̄)=σ²': r'n\operatorname{Var}(\bar X)=\sigma^2',
    '(n−1)σ²': r'(n-1)\sigma^2', 'nσ²': r'n\sigma^2', 'σ²/n': r'\frac{\sigma^2}{n}',
    '0.95²⁰': r'0.95^{20}', '0.05/20=0.0025': r'\frac{0.05}{20}=0.0025',
    'P(null | data)': r'P(\text{null}\mid\text{data})',
    'wX+(1−w)Y': r'wX+(1-w)Y', 'w²+4(1−w)²': r'w^2+4(1-w)^2',
    '2w−8(1−w)=0': r'2w-8(1-w)=0', 'w=4/5': r'w=\frac45',
    'w=(v_Y−c)/(v_X+v_Y−2c)': r'w=\frac{v_Y-c}{v_X+v_Y-2c}',
    '(XᵀX+λI)β̂=Xᵀy': r'(X^{\mathsf T}X+\lambda I)\hat\beta=X^{\mathsf T}y',
    'β̂=(XᵀX+λI)⁻¹Xᵀy': r'\hat\beta=(X^{\mathsf T}X+\lambda I)^{-1}X^{\mathsf T}y',
    'λ>0': r'\lambda>0', 'd/(d+λ)': r'\frac d{d+\lambda}',
    '√252': r'\sqrt{252}', 'kμ': r'k\mu', 'kσ²': r'k\sigma^2',
    '√k μ/σ': r'\sqrt k\,\frac\mu\sigma',
    'kγ₀+2Σ_(h=1)^(k−1)(k−h)γ_h': r'k\gamma_0+2\sum_{h=1}^{k-1}(k-h)\gamma_h',
    '3×3.5=10.5': r'3\times3.5=10.5', '6+2×3.5=13': r'6+2\times3.5=13',
    'payoff=100': r'\text{payoff}=100', 'P(high | buy)=2/3': r'P(\text{high}\mid\text{buy})=\frac23',
    '0.6 log(1+f)+0.4 log(1−f)': r'0.6\log(1+f)+0.4\log(1-f)',
    '0.6/(1+f)−0.4/(1−f)': r'\frac{0.6}{1+f}-\frac{0.4}{1-f}', 'f=0.2': r'f=0.2',
    'Cov=0.5×2×2=2': r'\operatorname{Cov}=0.5\times2\times2=2',
    '0.25×4+0.25×4+2×0.25×2=3': r'0.25\times4+0.25\times4+2\times0.25\times2=3',
    'ΔV≈delta×ΔS+(1/2)gamma×(ΔS)²=0+0.5×0.08×25=1': r'\Delta V\approx\delta\,\Delta S+\frac12\gamma(\Delta S)^2=0+0.5\times0.08\times25=1',
    'ΔS=−5': r'\Delta S=-5', 'ΔS=5': r'\Delta S=5',
    'K=100': r'K=100', 'T=1': r'T=1', 'S=100': r'S=100', 'r=0': r'r=0',
    'C−P=100−100=0': r'C-P=100-100=0', 'C−P': r'C-P',
    'E[value | your signal, winning]': r'\mathbb E[\text{value}\mid\text{your signal},\text{winning}]',
    'E[U²]': r'\mathbb E[U^2]', 'Cov(U²,(1−U)²)': r'\operatorname{Cov}(U^2,(1-U)^2)',
    'E[U²(1−U)²]=1/30': r'\mathbb E[U^2(1-U)^2]=\frac1{30}',
    'E[U²]=1/3': r'\mathbb E[U^2]=\frac13',
    'Var(U²)=1/5−1/9=4/45': r'\operatorname{Var}(U^2)=\frac15-\frac19=\frac4{45}',
    '1/30−1/9=−7/90': r'\frac1{30}-\frac19=-\frac7{90}',
    '(1/2)(4/45−7/90)=1/180': r'\frac12\left(\frac4{45}-\frac7{90}\right)=\frac1{180}',
    'Var(2X+7)=4Var(X)=36': r'\operatorname{Var}(2X+7)=4\operatorname{Var}(X)=36',
    'Corr(X,−2X+7)': r'\operatorname{Corr}(X,-2X+7)', 'Var(X)>0': r'\operatorname{Var}(X)>0',
    'Beta(2+3,2+1)=Beta(5,3)': r'\operatorname{Beta}(2+3,2+1)=\operatorname{Beta}(5,3)',
    'Beta(2,2)': r'\operatorname{Beta}(2,2)', 'Beta(5,3)': r'\operatorname{Beta}(5,3)',
    'Z=Y−c(X−E[X])': r'Z=Y-c(X-\mathbb E[X])', 'E[X]': r'\mathbb E[X]', 'E[Y]': r'\mathbb E[Y]',
    'Var(Y−cX)': r'\operatorname{Var}(Y-cX)',
    'Var(Z)=Var(Y)+c²Var(X)−2cCov(X,Y)': r'\operatorname{Var}(Z)=\operatorname{Var}(Y)+c^2\operatorname{Var}(X)-2c\operatorname{Cov}(X,Y)',
    'c*=Cov(X,Y)/Var(X)': r'c^*=\frac{\operatorname{Cov}(X,Y)}{\operatorname{Var}(X)}',
    'Var(Y)(1−Corr(X,Y)²)': r'\operatorname{Var}(Y)\left(1-\operatorname{Corr}(X,Y)^2\right)',
    # Python-like formulas in coding prose are mathematical, but source stays code.
    'z_i = x_i - beta*(y_i-mu_y)': r'z_i=x_i-\beta(y_i-\mu_y)',
    'sqrt(var/n)': r'\sqrt{\frac{\operatorname{var}}n}',
    '[j/bins,(j+1)/bins)': r'\left[\frac{j}{\text{bins}},\frac{j+1}{\text{bins}}\right)',
    'p^(-1)+...+p^(-k)': r'p^{-1}+\cdots+p^{-k}',
    '(1-p^k)/((1-p)p^k)': r'\frac{1-p^k}{(1-p)p^k}',
    'p<1': r'p<1',
    'Σ': r'\Sigma', 'σ²': r'\sigma^2', 'ρ': r'\rho', 'θ': r'\theta',
    'θ̂': r'\hat\theta', 'β̂': r'\hat\beta', 'μ': r'\mu', 'σ': r'\sigma',
    'γ₀': r'\gamma_0', 'γ_h': r'\gamma_h', 'E₀': r'E_0', 'E₁': r'E_1', 'E₂': r'E_2',
    'E_H': r'E_H', '3²': r'3^2', 'n−1': r'n-1', 'n(n−1)': r'n(n-1)',
}

DISPLAY = {
    key for key in FORMULAS if len(key) > 36
} | {'Var(X+Y)=Var(X)+Var(Y)+2Cov(X,Y)', 'MSE=Var(θ̂)+Bias(θ̂)²',
     '97×103=(100−3)(100+3)=10000−9=9991', 'β̂=(XᵀX+λI)⁻¹Xᵀy',
     'Var(Z)=Var(Y)+c²Var(X)−2cCov(X,Y)',
     'P(A)=|A|/|Ω|', 'P(A∪B)=P(A)+P(B)−P(A∩B)', 'P(A|B)=P(A∩B)/P(B)',
     'E[count]=ΣP(I_i=1)', 'E[N]=Σ_(k≥1)P(N≥k)', 'E[X]=∫₀∞P(X>x)dx',
     'Var(X̄)=n^(−2)Σ_iΣ_j Cov(X_i,X_j)', 'XᵀXβ=Xᵀy',
     'ΔV≈delta ΔS+½ gamma (ΔS)²+theta Δt'}
PATTERN = re.compile('|'.join(re.escape(x) for x in sorted(FORMULAS, key=len, reverse=True))
                     + r'|(?<![\w:.])\d+(?:\.\d+)?/\d+(?:\.\d+)?(?![\w/])')
EXPLICIT = re.compile(r'(\\\(.*?\\\)|\\\[.*?\\\])', re.S)

def math_text(text):
    def replace(match):
        source = match.group()
        tex = FORMULAS.get(source)
        if tex is None:
            numerator, denominator = source.split('/')
            tex = rf'\frac{{{numerator}}}{{{denominator}}}'
        return ('\\[' + tex + '\\]') if source in DISPLAY else ('\\(' + tex + '\\)')
    # Explicit TeX authored in future lessons is left intact, not converted twice.
    result = ''.join(part if i % 2 else PATTERN.sub(replace, part)
                     for i, part in enumerate(EXPLICIT.split(text)))
    # Sentence punctuation belongs on the equation line, rather than alone
    # at the start of the following paragraph line.
    return re.sub(r'(\\\[.*?)(\\\])([.,;])', r'\1\3\2', result, flags=re.S)

PROSE_FIELDS = {'prompt', 'hints', 'solution', 'followup', 'followSolution',
                'rubric', 'intro', 'text', 'example', 'check', 'options', 'explanation'}

def annotate(value, field=None):
    if isinstance(value, dict):
        annotated = {k: annotate(v, k) for k, v in value.items()}
        if 'options' in value:
            annotated['optionLabels'] = value['options']
        return annotated
    if isinstance(value, list):
        return [annotate(v, field) for v in value]
    if isinstance(value, str) and field in PROSE_FIELDS:
        return math_text(value)
    return value
