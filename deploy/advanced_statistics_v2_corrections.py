from __future__ import annotations

import copy

VERSION = '2026.07.30-1'
UPDATED_AT = '2026-07-30'


def build_v2(chapters_src, questions_src):
    chapters = copy.deepcopy(chapters_src)
    questions = copy.deepcopy(questions_src)
    ch = {c['id']: c for c in chapters}
    q = {x['id']: x for x in questions}

    # ch03 — the title/scope already promised Negative Binomial, but v1 only named it.
    c = ch['ch03']
    c['definitions'] = [
        ('Bernoulli 分配', 'X∈{0,1}，P(X=1)=p。'),
        ('二項分配（Binomial）', 'n 次彼此獨立且成功率固定為 p 的 Bernoulli 試驗之成功總數。'),
        ('幾何分配（Geometric）', '本書採 X=直到第一次成功所需試驗次數，故 X=1,2,…，且 P(X=x)=(1-p)^{x-1}p。'),
        ('負二項分配（Negative Binomial）', '本書採 X=直到第 r 次成功所需試驗總次數；X=r,r+1,…。不同教材也可能把 X 定義成第 r 次成功前的失敗數，兩種參數化不可混用。'),
        ('Poisson 分配', 'X=0,1,…，以 λ>0 描述固定區間平均事件數；E(X)=Var(X)=λ。'),
    ]
    c['formulas'] = [
        ('P(X=x)={n\\choose x}p^x(1-p)^{n-x}', 'X~Binomial(n,p)，x=0,…,n。'),
        ('P(X=x)={x-1\\choose r-1}p^r(1-p)^{x-r}', 'X 表示直到第 r 次成功所需試驗數時的 Negative Binomial PMF；x=r,r+1,…。'),
        ('E(X)=\\frac{r}{p},\\qquad Var(X)=\\frac{r(1-p)}{p^2}', '同一 Negative Binomial「試驗總次數」參數化的平均數與變異數。'),
        ('P(X=x)=e^{-\\lambda}\\frac{\\lambda^x}{x!}', 'X~Poisson(λ)，x=0,1,…。'),
    ]
    c['example'] = [
        '例：5 次獨立試驗，每次成功率 0.2。恰好 1 次成功的機率為 5×0.2×0.8⁴=0.4096。',
        '若固定區間事件數服從 Poisson(2)，零事件機率 e^{-2}≈0.1353。',
        '若每次成功率 p=0.25，且 geometric 定義為直到第一次成功的試驗次數，則 E(X)=1/p=4。',
        '若 Negative Binomial 採「直到第 3 次成功的試驗總次數」，p=0.2，則 P(X=7)=C(6,2)×0.2³×0.8⁴=0.049152，且 E(X)=3/0.2=15。',
    ]
    c['traps'] = [
        '二項分配漏掉試驗彼此獨立且成功率固定的假設。',
        'Poisson 的 λ 誤當成功機率。',
        '幾何或負二項分配不先確認 X 是「試驗總次數」還是「失敗次數」，造成支撐、平均數與 PMF 全部錯位。',
    ]
    c['exam'] = [
        '先用一句話說明隨機機制，再寫 X 的支撐。',
        'Geometric／Negative Binomial 題先固定 X 的計數口徑，再套公式。',
        'Poisson 近似二項時要有 n 大、p 小且 np 維持在適度範圍的情境。',
    ]
    c['checks'] = [
        'Binomial(5,0.2) 恰好 1 次成功機率是多少？',
        'Geometric(p=0.25) 若計直到第一次成功的試驗次數，期望值是多少？',
        'Negative Binomial 若 X 計直到第 r 次成功的試驗總次數，其支撐與 E(X) 如何寫？',
    ]

    # ch07 — make the joint-normal and positive-variance conditions explicit.
    c = ch['ch07']
    c['definitions'] = [
        ('均值向量', 'μ=E(X)，收集每個分量的期望。'),
        ('共變異數矩陣', 'Σ=E[(X-μ)(X-μ)ᵀ]，必為對稱半正定。'),
        ('多元常態（multivariate normal）', '對每個常數向量 a，線性組合 aᵀX 都是一維常態（可包含變異數為 0 的退化常態）。'),
    ]
    c['formulas'][1] = (
        'Y\\mid X=x\\sim N\\!\\left(\\mu_Y+\\frac{\\sigma_{XY}}{\\sigma_X^2}(x-\\mu_X),\\ \\sigma_Y^2-\\frac{\\sigma_{XY}^2}{\\sigma_X^2}\\right)',
        '二維聯合常態且 σ_X²>0 時的條件分配公式；只有邊際各自常態不足以使用此公式。',
    )

    # ch11 — Slutsky was named but not actually taught; Delta with zero derivative needs a warning.
    c = ch['ch11']
    c['definitions'] = [
        ('依機率收斂（convergence in probability）', '對任意 ε>0，P(|X_n-X|>ε)→0。'),
        ('分布收斂（convergence in distribution）', 'CDF 在極限分布的連續點收斂。'),
        ('大數法則（LLN）', '在標準 iid、有限母體平均等條件下，樣本平均 X̄_n 依機率收斂到 μ。'),
        ('中央極限定理（CLT）', 'iid、有限且正變異數時，√n(X̄_n-μ)/σ 分布收斂到 N(0,1)。'),
        ('Slutsky 定理', '若 X_n⇒X 且 Y_n→p c（常數），則 X_n+Y_n⇒X+c、X_nY_n⇒cX；c≠0 時 X_n/Y_n⇒X/c。'),
    ]
    c['formulas'] = [
        ('\\bar X_n\\xrightarrow{p}\\mu', '典型弱大數法則的結論；成立條件要跟所使用的 LLN 版本一起寫。'),
        ('\\sqrt{n}\\frac{\\bar X-\\mu}{\\sigma}\\Rightarrow N(0,1)', 'iid、E(X)=μ、0<Var(X)=σ²<∞ 的經典 CLT。'),
        ('X_n\\Rightarrow X,\\ Y_n\\xrightarrow{p}c\\ \Longrightarrow\\ X_nY_n\\Rightarrow cX', 'Slutsky 的乘法版本；加法與 c≠0 時的除法版本同理。'),
        ('\\sqrt n\\{g(\\hat\\theta)-g(\\theta)\\}\\Rightarrow N(0,[g^\\prime(\\theta)]^2V)', '若 √n(θ̂-θ)⇒N(0,V) 且 g 在 θ 可微。若 g′(θ)=0，這個一階極限會退化，通常要改用更高階 Delta method 才能得到非退化近似。'),
    ]
    c['example'] = [
        '例：母體平均 10、標準差 4，n=64。X̄ 的標準誤為 4/8=0.5。',
        'CLT 下 P(|X̄-10|≤1)≈P(|Z|≤2)≈0.9545。',
        '若 √n(X̄-μ)/σ⇒N(0,1) 且 S→pσ>0，Slutsky 給 √n(X̄-μ)/S⇒N(0,1)：一致估計的 S 可在大樣本中取代未知 σ。',
        '若 √n(X̄-2)⇒N(0,9)，取 g(x)=log x，g′(2)=1/2，則 √n(log X̄-log2) 的漸近變異數為 9/4。',
    ]
    c['traps'] = [
        '把 LLN 說成樣本平均在有限 n 必然等於 μ。',
        '把 CLT 說成原始資料 Xi 本身會隨 n 增大變成常態。',
        '套 Delta method 時只看「可微」卻忽略 g′(θ)=0；此時一階近似通常退化，不能假裝仍有同樣的非退化常態近似。',
    ]

    # ch13 — add the MLE invariance property promised by the scope.
    c = ch['ch13']
    c['definitions'].append(('MLE 不變性（invariance）', '若 θ̂ 是 θ 的 MLE，則在通常的參數轉換定義下，g(θ) 的 MLE 可取 g(θ̂)；非一對一或 MLE 不唯一時應理解為最大化集合的對應，而不是任意選值。'))
    c['formulas'].append(('\\widehat{g(\\theta)}_{\\mathrm{MLE}}=g(\\hat\\theta_{\\mathrm{MLE}})', 'MLE 的參數轉換不變性；仍須先確認原 MLE 存在與最大值集合。'))
    c['example'].append('同一 Exponential(rate=λ) 例中，母體平均 m=1/λ。既然 λ̂_MLE=1/X̄，依 MLE 不變性，m̂_MLE=1/λ̂=X̄。')
    c['exam'].append('若題目改問 g(θ) 而已知 θ̂_MLE，先檢查是否可直接用 MLE invariance，避免重新最大化一次。')

    # ch14 — v1 incorrectly described completeness as simply "stronger than" sufficiency.
    c = ch['ch14']
    c['intuition'] = [
        '充分性是在問「知道 T(X) 之後，原始樣本還有沒有額外關於 θ 的資訊」。因子分解定理讓這個概念能直接從 likelihood 辨認。',
        '完備性與充分性回答不同問題：充分性談資訊是否被保留，完備性談一族期望等式是否能唯一逼出函數為 0。兩者一般互不推出；「完備且充分」是同時具備兩個性質，不能把完備性單獨說成充分性的較強版本。',
        '指數族常自然產生低維充分統計量；要再推完備性，仍需檢查參數空間與該家族的額外條件。',
    ]
    c['definitions'][2] = ('完備（complete）', '對所有可積函數 g，若 Eθ[g(T)]=0 對每個 θ 都成立，則 g(T)=0 幾乎處處（對模型中各 θ）。完備性本身不等於充分性。')
    c['traps'] = [
        '把充分性解讀成樣本一定夠大。',
        '看到指數族就不檢查參數空間與統計量，直接宣稱完備。',
        '說「完備性比充分性強」而省略兩者是不同性質；正確比較應是「完備且充分」比「只有充分」多了一項條件。',
    ]
    c['exam'] = [
        '先把 likelihood 中與 θ 有關部分聚在一起，找充分統計量。',
        '若題目再問完備性，要另用期望唯一性或適用的指數族定理證明，不能由充分性直接推出。',
        '若要用 Lehmann–Scheffé，必須確認統計量同時完備且充分，並找出目標參數函數的無偏估計。',
    ]

    # ch15 — make asymptotic properties and the finite-variance Rao–Blackwell condition explicit.
    c = ch['ch15']
    c['definitions'] = [
        ('偏誤（bias）', 'Bias(θ̂)=Eθ(θ̂)-θ。'),
        ('均方誤差（MSE）', 'E[(θ̂-θ)²]=Var(θ̂)+Bias(θ̂)²。'),
        ('一致性（consistency）', '估計量序列 θ̂_n 若 θ̂_n→pθ，稱為對 θ 一致。'),
        ('漸近常態（asymptotic normality）', '若適當標準化後的估計誤差分布收斂到常態，例如 √n(θ̂_n-θ)⇒N(0,V(θ))。'),
        ('Fisher information', '常用 I_n(θ)=Eθ[(∂ℓ/∂θ)²]；與 -Eθ(∂²ℓ/∂θ²) 的等價以及 E(score)=0 需要相應正則條件。'),
    ]
    c['formulas'] = [
        ('MSE(\\hat\\theta)=Var(\\hat\\theta)+Bias(\\hat\\theta)^2', '偏誤與變異的共同尺度。'),
        ('\\hat\\theta_n\\xrightarrow{p}\\theta', '一致性的典型表示。'),
        ('\\sqrt n(\\hat\\theta_n-\\theta)\\Rightarrow N(0,V(\\theta))', '常見的 √n 漸近常態形式；V(θ) 由模型與估計量決定。'),
        ('Var(\\hat\\theta)\\ge \\frac{1}{I_n(\\theta)}', '一參數、估計 θ 本身的無偏估計量之 Cramér–Rao 下界；需相應可微、交換積分與參數位於正則區域等條件。'),
    ]
    c['example'] = [
        '例：Bernoulli(p) 樣本平均 p̂=X̄ 無偏，Var(p̂)=p(1-p)/n，而且由 LLN 可得 p̂→p p。',
        '對 p∈(0,1)，Bernoulli 樣本的 Fisher information I_n(p)=n/[p(1-p)]，所以 CRLB=p(1-p)/n；樣本平均達到此下界。',
        '若 U 是平方可積的無偏估計量、T 是充分統計量，Rao–Blackwell 化 U*=E(U|T) 仍無偏，且 Var(U*)≤Var(U)；等號可能發生，所以不能說一定嚴格變小。',
    ]
    c['traps'] = [
        '只比較 bias，不看 variance 或 MSE。',
        '把有限樣本無偏、一致性與漸近常態當成同一性質。',
        'CRLB 不檢查無偏與正則條件就套用，或在 p=0、1 這類邊界直接沿用內點 Fisher-information 公式。',
        'Rao–Blackwell 說成一定嚴格降低變異數，或忘記討論所需的可積／有限二階矩條件。',
    ]

    # ch16 — distinguish exact z/t intervals from asymptotic approximations.
    c = ch['ch16']
    c['formulas'][0] = ('\\bar X\\pm z_{1-\\alpha/2}\\frac{\\sigma}{\\sqrt n}', 'iid 常態母體且 σ 已知時為精確 z 區間；非正態情況可在相應 CLT 條件下作大樣本近似，但不能稱為有限樣本精確。')
    c['formulas'][1] = ('\\bar X\\pm t_{n-1,1-\\alpha/2}\\frac{S}{\\sqrt n}', 'Xi iid~N(μ,σ²)、σ 未知且 S²=(n-1)^{-1}Σ(Xi-X̄)² 時的一樣本平均數精確 t 區間。')

    # ch17 — distinguish test size from level and qualify p-values/NP in composite or discrete cases.
    c = ch['ch17']
    c['intuition'] = [
        '檢定規則把樣本空間分成拒絕域與不拒絕域。size 是 H0 參數集合中拒絕機率的上確界；「level α」表示 size≤α，不必剛好等於 α。power function 則描述各 θ 下拒絕 H0 的機率。',
        'p-value 必須相對於已指定的檢定統計量與「更極端」排序來定義。對 simple H0 可直接用該 null 分布；有 nuisance parameter 的 composite H0 則還需要有效的 null 校準（例如取最不利情形或使用能消去 nuisance 的方法），不能含糊地把某一個參數值的尾機率當成普遍 p-value。',
        'Neyman–Pearson 引理針對 simple H0 vs simple H1 給定 level/size 下的最強力檢定；離散模型若要精確達到某個 α，有時需要在臨界邊界隨機化。',
    ]
    c['definitions'] = [
        ('檢定大小（size）', 'size = sup_{θ∈Θ0} Pθ(拒絕 H0)。'),
        ('level-α 檢定', '若 size≤α，稱為 level α；只有在上確界恰為 α 時 size 才等於 α。'),
        ('檢定力（power）', 'π(θ)=Pθ(拒絕 H0)。'),
        ('p-value', '在指定 H0 校準與檢定統計量排序下，觀察到目前或更不利於 H0 的結果之 null 尾端機率；它不是 P(H0|data)。'),
        ('簡單假設（simple hypothesis）', '完全指定分配參數；複合假設則含多個可能參數值。'),
    ]
    c['formulas'] = [
        ('\\alpha^*=\\sup_{\\theta\\in\\Theta_0}P_\\theta(\\text{reject }H_0)', 'α* 是檢定 size；若 α*≤α，該檢定為 level α。'),
        ('\\Lambda(x)=\\frac{L(\\theta_1;x)}{L(\\theta_0;x)}', 'simple H1 對 simple H0 的 likelihood ratio；NP 最強力檢定傾向在此比值大時拒絕 H0，離散情形必要時可在臨界點隨機化以達指定 size。'),
        ('z=\\frac{\\bar X-\\mu_0}{\\sigma/\\sqrt n}', '常態 σ 已知平均數 z 檢定統計量。'),
    ]
    c['exam'] = [
        '先寫 H0/H1 與方向，再分清題目給的是 size、level 還是某個 θ 下的 Type I error。',
        'p-value 題先確認檢定統計量與「更極端」方向；composite H0 還要處理 nuisance parameter。',
        '若題目問最強力，先辨認是否 simple vs simple；離散模型注意是否需要 randomization 才能精確達 α。',
    ]

    # ch18 — tighten UMP/MLR/Wilks conditions.
    c = ch['ch18']
    c['intuition'] = [
        '一致最強力（UMP）要求同一個 level-α 檢定對對立假設中每個參數值都至少不比其他 level-α 檢定差，因此未必存在。對具有 monotone likelihood ratio（MLR）的適當單參數家族，Karlin–Rubin 型結果常能為單尾假設建立 UMP。',
        '概似比檢定（LRT）比較 H0 受限最大概似與完整參數空間最大概似。若 H0 為真且模型為正則巢狀、可識別，真參數位於適當內點，Wilks 定理常給 -2logΛ⇒χ²；邊界、不可識別或其他非正則問題可能產生混合 χ² 或其他非標準極限。',
    ]
    c['definitions'] = [
        ('UMP 檢定', '在指定 level α 的檢定類別中，對 H1 每個參數值皆具有不低於其他候選檢定之 power 的檢定。'),
        ('單調概似比（MLR）', '若 θ₂>θ₁ 時，f_{θ₂}(x)/f_{θ₁}(x) 可寫成統計量 T(x) 的非遞減函數，稱該家族對 T 具有 MLR；這是許多單尾 UMP 結果的關鍵結構。'),
        ('概似比統計量', 'H0 參數空間 Θ0⊂Θ 時，Λ=sup_{θ∈Θ0}L(θ)/sup_{θ∈Θ}L(θ)，因此在最大值有限且存在時 0≤Λ≤1。'),
        ('Wilks 定理', 'H0 為真且滿足正則、巢狀、可識別與內點等條件時，-2logΛ 漸近為 χ²；自由度通常等於完整與受限模型的有效維度差。'),
    ]
    c['formulas'][1] = ('-2\\log\\Lambda\\Rightarrow\\chi^2_{d}', '在 H0 與 Wilks 正則條件下的大樣本結果；d 通常是有效參數維度差／獨立限制數，非正則邊界問題不得直接套用。')
    c['exam'] = [
        'UMP 題先確認假設方向與檢定類別，再找 MLR／Karlin–Rubin 結構；不能只看到指數族三個字就宣稱 UMP。',
        'LRT 先各自找受限與不受限最大概似，再看 Λ 是否小到進入拒絕域。',
        '使用 Wilks 前逐一問：H0 是否為真下校準、模型是否巢狀可識別、真參數是否為正則內點；否則極限分布可能不是標準 χ²。',
    ]

    # ch19 — state Gauss–Markov and F-test dimensions conditionally on X.
    c = ch['ch19']
    c['intuition'] = [
        '線性模型 y=Xβ+ε 把多個係數一起整理。若 X 滿 column rank，且採條件於 X 的標準 Gauss–Markov 條件 E(ε|X)=0、Var(ε|X)=σ²I，則 OLS 是線性無偏估計量中的 BLUE；這個 BLUE 結論不需要常態性。',
        '若再加上 ε|X~N(0,σ²I)，才可得到傳統有限樣本 t 與 F 的精確分布。若沒有常態性，OLS 仍可能是 BLUE，但傳統小樣本 t/F 不再因 Gauss–Markov 本身而精確成立。',
        '這一章用矩陣看懂迴歸與 ANOVA 的共同結構，但不擴張成完整計量經濟學。',
    ]
    c['definitions'][2] = ('Gauss–Markov 定理', '在 X 滿 column rank、E(ε|X)=0、Var(ε|X)=σ²I 等標準條件下，OLS 為 BLUE；常態性不是此 BLUE 結論的必要條件。')
    c['formulas'][1] = ('F=\\frac{(SSE_R-SSE_U)/q}{SSE_U/(n-p)}', '比較 q 個獨立線性限制的巢狀模型；p 為 unrestricted model 估計係數數（含截距若模型有截距）。在常態線性模型條件下有精確 F_{q,n-p} 校準。')

    # Question-bank adjustments (IDs stay fixed to preserve progress/error history).
    q['ch03-q05'].update({
        'question': 'Negative Binomial 採 X=直到第 3 次成功的試驗總次數，p=0.2。P(X=7) 是多少？',
        'answer': '0.049152。',
        'explanation': 'P(X=7)=C(6,2)×0.2³×0.8⁴=15×0.008×0.4096=0.049152；支撐從 x=r=3 開始。',
    })
    q['ch11-q01'].update({
        'question': '若 Z_n⇒N(0,1) 且 S_n→p2，依 Slutsky，Z_n/S_n 的極限分布為何？',
        'answer': 'N(0,1/4)。',
        'explanation': '因 S_n→p2≠0，Slutsky 給 Z_n/S_n⇒Z/2；若 Z~N(0,1)，則 Z/2~N(0,1/4)。',
    })
    q['ch13-q03'].update({
        'question': 'Exponential(rate=λ) 的 λ̂_MLE=1/X̄。若改估母體平均 m=1/λ，依 MLE invariance，m̂_MLE 是什麼？',
        'answer': 'X̄。',
        'explanation': 'm̂_MLE=1/λ̂_MLE=1/(1/X̄)=X̄；這是 MLE 對參數轉換的不變性。',
    })
    q['ch14-q04'].update({
        'question': '完備性與充分性是否有一般的「完備 ⇒ 充分」或「充分 ⇒ 完備」包含關係？',
        'answer': '沒有；兩者是不同性質，一般互不推出。',
        'explanation': '充分性談資料壓縮後是否保留關於參數的全部資訊；完備性談 Eθ[g(T)]=0 對所有 θ 是否逼出 g(T)=0。Lehmann–Scheffé 使用的是同一統計量「同時完備且充分」。',
    })
    q['ch15-q05'].update({
        'question': '若 U 平方可積、T 充分，Rao–Blackwell 化 U*=E(U|T) 後變異數是否一定嚴格變小？',
        'answer': '不一定；只保證不增加。',
        'explanation': '由條件期望／全變異公式可得 Var(E(U|T))≤Var(U)；若 U 本來已是 T 的函數等情況可取等號。平方可積使這裡的變異數比較有意義。',
    })
    q['ch17-q04'].update({
        'question': '若檢定的 size=0.04，能否稱它為 level 0.05 的檢定？',
        'answer': '可以。',
        'explanation': 'level α 只要求 size≤α；0.04≤0.05，所以它是 level 0.05，但其 size 並不是 0.05。',
    })
    q['ch18-q04'].update({
        'question': 'Wilks 定理下 χ² 自由度通常對應什麼？',
        'answer': '正則巢狀模型中完整模型與 H0 受限模型的有效參數維度差（等價於獨立限制數）。',
        'explanation': '這個 χ² 結論是在 H0 為真且滿足正則、可識別與內點等條件下的漸近結果；邊界或不可識別問題可能不是標準 χ²。',
    })

    return chapters, questions
