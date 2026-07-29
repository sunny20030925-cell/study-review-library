from __future__ import annotations

import copy

from mathematical_economics_content import CHAPTERS as V1_CHAPTERS

VERSION = '2026.07.30-2'
UPDATED_AT = '2026-07-30'


def corrected_chapters():
    chapters = copy.deepcopy(V1_CHAPTERS)
    by_id = {c['id']: c for c in chapters}

    ch = by_id['ch04']
    ch['definitions'][3] = ('Cramer 法則', '當 A 為 n×n 方陣且 det(A)≠0 時，以行列式比值解 Ax=b 的公式方法。')

    ch = by_id['ch05']
    ch['intuition'] = [
        '特徵向量張成的是矩陣作用後仍留在同一條直線上的特殊方向；λ>0 保持方向、λ<0 反向，λ=0 則被映到零向量。',
        '二次型 x^TAx 對稱矩陣的定號可描述各方向的正負；當 A 是 Hessian 時，才可直接把它解讀成局部曲率資訊。',
    ]
    ch['definitions'][0] = ('特徵值（eigenvalue）', '若 Av=λv 且 v≠0，λ 為 A 對特徵向量 v 的伸縮因子；λ<0 會反向，λ=0 會把 v 映到零向量。')
    ch['definitions'][1] = ('特徵向量（eigenvector）', '滿足 Av=λv 的非零向量 v；更精確地說，其所張成的一維子空間在矩陣作用下保持不變。')
    ch['formulas'][1] = (r'q(x)=x^TAx', 'A 為對稱矩陣時，可用特徵值或主子式判斷二次型定號；若 A 是 Hessian，定號才對應二階曲率。')

    ch = by_id['ch06']
    ch['definitions'][1] = ('連續（continuity）', '若 x0 在定義域內且 lim_{x→x0} f(x)=f(x0)，則 f 在 x0 連續。')
    ch['formulas'] = [
        (r"f'(x)=\lim_{h\to0}\frac{f(x+h)-f(x)}{h}", '導數定義。'),
        (r"(uv)'=u'v+uv'", '乘法法則。'),
        (r"\left(\frac{u}{v}\right)'=\frac{u'v-uv'}{v^2}", '商數法則，要求 v≠0。'),
        (r"\frac{d}{dx}f(g(x))=f'(g(x))g'(x)", '鏈鎖律；複合函數微分時不可漏掉內層導數。'),
        (r"\Delta y\approx f'(x_0)\Delta x", '一階小變動近似。'),
        (r"f(x)\approx f(a)+f'(a)(x-a)+\frac12f''(a)(x-a)^2", '二階 Taylor 近似；誤差大小仍取決於高階導數與離展開點的距離。'),
    ]
    ch['traps'] = ['把 Δy=f′Δx 當所有有限變動都精確成立。', '複合函數微分時漏掉內層導數。', '函數不可微時仍硬套導數或 Taylor 公式。']
    ch['exam'] = ['先辨認題目要精確值還是局部近似。', '乘積、商數、複合函數先選對微分法則；鏈鎖律最常漏項。', '小變動可先用一階；要求更精準再考慮二階與誤差。']

    ch = by_id['ch07']
    ch['intuition'] = [
        '偏導數是「其他自變數暫時固定，只動一個」。微分 dz 是基準點上的線性映射；用它近似有限變動時，才寫成 Δz≈f_xΔx+f_yΔy。',
        '在採用一般 Euclidean 距離且 ∇f≠0 時，梯度指向局部上升最快的方向；換一種尺度或度量，所謂「最快」方向也會改變。',
    ]
    ch['definitions'][1] = ('全微分（total differential）', '可微函數在基準點的一階線性映射 dz=Σf_i dx_i；對有限但夠小的變動，Δz 才以這個微分作一階近似。')
    ch['definitions'][2] = ('梯度（gradient）', '由各一階偏導數組成的向量 ∇f；在 Euclidean norm 下，非零梯度給出最陡上升方向。')

    ch = by_id['ch08']
    ch['definitions'][2] = ('隱函數定理', '若 F 對相關變數連續可微，且在基準點對欲解出的內生變數所形成的 Jacobian 為非奇異方陣，則局部可把這些內生變數寫成其餘變數／參數的可微函數。')
    ch['formulas'][2] = (r'J_y\,dy=-J_\alpha\,d\alpha', '多方程局部比較靜態；只有在對內生變數的 Jacobian J_y 為方陣且可逆時，才能寫 dy=-J_y^{-1}J_α dα。')

    ch = by_id['ch09']
    ch['formulas'] = [
        (r'\varepsilon_{yx}=\frac{dy}{dx}\frac{x}{y}', 'y 對 x 的點彈性；百分比解讀通常要求基準 x、y 為非零，經濟量常進一步限制為正。'),
        (r'd\ln y=\frac{dy}{y}', '正值 y 的對數微分。'),
        (r'y=Ax^a\Rightarrow \varepsilon_{yx}=a', '冪函數 y=Ax^a（A>0、x>0）的常數彈性為 a。'),
        (r'Q=AK^aL^b\Rightarrow d\ln Q=a\,d\ln K+b\,d\ln L', 'Cobb–Douglas 型函數的對數微分；小變動下可讀成輸出百分比變動約等於投入百分比變動的加權和。'),
    ]
    ch['example'] = [
        '例：Q=2P^{-2}，因此價格彈性 dQ/dP×P/Q=-2。',
        '若 P 在基準點附近上升約 1%，Q 的一階近似變動約為 -2%。',
        '若是 Q=AK^{0.3}L^{0.7}，K 上升 1%、L 上升 2%，則小變動近似下 Q 約增加 0.3×1%+0.7×2%=1.7%。',
    ]

    ch = by_id['ch11']
    ch['definitions'] = [
        ('Hessian', '由二階偏導數組成的方陣 H；若 f 為 C²，Hessian 對稱。'),
        ('駐點（stationary point）', '梯度 ∇f=0 的點。'),
        ('凹函數（concave）', '在凸定義域上，任意兩點的線性組合之函數值不低於兩端函數值的同權重平均。'),
        ('嚴格凹函數', '對任意不同兩點與 0<θ<1，上述凹性不等式為嚴格大於；因此至多有一個全域最大解。'),
        ('擬凹函數（quasi-concave）', '所有上位集合 {x:f(x)≥c} 都是凸集合；它比凹性弱，常用於偏好與受限最大化。'),
    ]
    ch['formulas'] = [
        (r'\nabla f(x^*)=0', '多元可微內點 FOC。'),
        (r'H_f(x^*)\prec0', 'Hessian 在駐點負定時，該點為嚴格局部極大。'),
        (r'H_f(x)\preceq0\ \forall x', '若定義域凸、f 為 C² 且 Hessian 處處負半定，則 f 為凹函數；處處負定是嚴格凹的充分條件之一。'),
        (r'D_1=f_{xx},\quad D_2=\det H', '二變數對稱 Hessian：負定可用 D1<0、D2>0；正定用 D1>0、D2>0。'),
    ]
    ch['exam'] = ['先算完整 gradient。', '再寫 Hessian 並做定號；不要只看主對角元素。', '若目標在凸可行域上為凹函數，滿足 FOC 的內點是全域最大；嚴格凹時若解存在則唯一。']

    ch = by_id['ch12']
    ch['definitions'] = [
        ('Lagrangian', '把目標函數與等式限制結合的輔助函數。'),
        ('Lagrange multiplier', '等式限制對應的乘數 λ。'),
        ('一階條件', '在正則內點候選上，對所有選擇變數與乘數求偏導並設為 0。'),
        ('正則條件', '例如限制梯度非零／多限制梯度線性獨立，使乘數法能描述局部候選點。'),
        ('切空間二階條件', '二階曲率應只沿著滿足一階可行方向 ∇g(x*)ᵀd=0 的切空間檢查；bordered Hessian 是其常見行列式捷徑。'),
    ]
    ch['formulas'] = [
        (r'\mathcal L=f(x)+\lambda\,[b-g(x)]', '本章固定採此符號慣例；若改成 g-b，λ 的符號會反向。'),
        (r'\nabla f(x^*)=\lambda^*\nabla g(x^*)', '單一正則等式限制下的 FOC 幾何關係。'),
        (r'g(x^*)=b', '限制本身必須與其他 FOC 一起解。'),
        (r'd^T\nabla_{xx}^2\mathcal L(x^*,\lambda^*)d<0\quad\text{for all }d\ne0\text{ with }\nabla g(x^*)^Td=0', '單一等式限制下嚴格局部極大的常用充分二階條件；bordered Hessian 只是等價的計算工具之一，符號規則取決於限制數與 max/min 慣例。'),
    ]
    ch['example'] = [
        '例：最大化 xy，限制 x+y=10，且 x,y>0。令 L=xy+λ(10-x-y)。',
        'FOC：y-λ=0、x-λ=0、10-x-y=0，所以 x=y=5。',
        '沿限制線令 y=10-x，目標變成 x(10-x)=10x-x²，二階導數為 -2<0；因此 x=y=5 是限制集合上的唯一全域最大點。',
    ]
    ch['traps'] = ['只解 ∂L/∂x、∂L/∂y，忘記限制式。', '用原目標 Hessian 的不定性直接否定受限制下的最大值；受限二階條件只看可行切方向。', '不同 Lagrangian 符號慣例下仍硬套同一 λ 影子價格解讀。']

    ch = by_id['ch13']
    ch['definitions'][0] = ('KKT 條件', '在可微問題且滿足適當 constraint qualification（如 LICQ；凸問題常用 Slater 條件）時，KKT 是局部最適解的一階必要條件；在凹／凸結構下亦可成為充分條件。')
    ch['formulas'] = [
        (r'g_i(x)\le0,\ \mu_i\ge0,\quad \mathcal L=f(x)-\sum_i\mu_i g_i(x)', '本章固定採「最大化、g_i≤0、μ_i≥0」的符號慣例；不同教材若改變限制方向，乘數與 Lagrangian 符號也要一起改。'),
        (r'\nabla f(x^*)-\sum_i\mu_i^*\nabla g_i(x^*)=0', 'stationarity；需與可行性、乘數符號及互補鬆弛一起檢查。'),
        (r'\mu_i^*g_i(x^*)=0', '互補鬆弛：限制有嚴格餘裕時 μ_i*=0；active constraint 也可能因退化而有 μ_i*=0。'),
    ]
    ch['exam'] = [
        '先統一所有不等式方向與 Lagrangian 符號。',
        '必要性要檢查 constraint qualification；不要把 KKT 當成完全無條件的必要條件。',
        '若最大化凹函數，且 g_i≤0 的 g_i 為凸函數（再配合仿射等式限制），則滿足 KKT 的可行點可作全域最適判斷；Slater 條件常用來保證凸問題的 KKT／強對偶成立。',
    ]

    ch = by_id['ch14']
    ch['formulas'] = [
        (r'V(\alpha)=f(x^*(\alpha),\alpha)', '值函數定義。'),
        (r"V'(\alpha)=f_\alpha(x^*(\alpha),\alpha)", '無限制內點、光滑且 FOC 適用時的典型包絡公式。'),
        (r'\frac{dV}{d\theta}=\frac{\partial\mathcal L}{\partial\theta}\Big|_{x^*,\lambda^*}', '受限制問題在適當正則條件下的通用包絡寫法；它自動把目標與限制中參數 θ 的直接效果一起計入。'),
        (r'\frac{\partial V}{\partial b}=\lambda^*', '若採 L=f+λ[b-g(x)]，且 b 只出現在限制右側，則 λ* 等於放寬 b 一單位的最適值邊際效果。'),
    ]
    ch['exam'] = ['先確認是在求「最適值」還是「最適選擇」。', '受限問題優先寫 dV/dθ=∂L/∂θ，再依所採 Lagrangian 符號展開。', '影子價格等於值函數對限制右側的導數，只在參數進入方式與符號慣例相符時成立。']

    ch = by_id['ch15']
    ch['definitions'][3] = ('homothetic', '可寫成某個齊次函數的嚴格遞增轉換；它保留由原點向外徑向擴張的等值集合結構，但函數本身不必齊次。')
    ch['traps'] = ['只看單一投入的邊際報酬就判斷規模報酬。', '把 homothetic 與 homogeneous 當同義，或把任意單調（含遞減）轉換都當成 homothetic。', 'Euler 定理忘記「所有投入同比例縮放」與可微條件。']

    ch = by_id['ch18']
    ch['formulas'][3] = (r'|b|<1', '一階線性差分方程對唯一穩態全域收斂；-1<b<0 時交替收斂。b=-1 通常形成二期循環而非漸近收斂；|b|>1 則偏離放大。')
    ch['exam'] = ['先令 x_{t+1}=x_t 求固定點；b=1 時要另外檢查穩態是否存在／是否唯一。', '再把方程改寫成偏離穩態形式。', '最後看特徵根的絕對值；|b|=1 是邊界情形，不能套 |b|<1 的收斂結論。']

    ch = by_id['ch19']
    ch['definitions'][3] = ('局部漸近穩定', '從足夠靠近穩態的初值出發，路徑會留在附近並隨時間回到該穩態。')
    ch['formulas'][3] = (r"F'(x^*)<0", '一維 C¹ 自治系統 ẋ=F(x) 的常用局部漸近穩定充分條件；F′(x*)>0 則不穩定，F′(x*)=0 時此線性化判準不下結論。')
    ch['exam'] = ['先由 ẋ=0 找固定點。', '再看 F′(x*) 或解中的指數係數；F′=0 時必須回到非線性項另判。', '最適控制、Hamiltonian 與 dynamic programming 只當後續課程入口。']

    return chapters


CHAPTERS_V2 = corrected_chapters()
assert len(CHAPTERS_V2) == 20
assert [c['id'] for c in CHAPTERS_V2] == [f'ch{i:02d}' for i in range(20)]
