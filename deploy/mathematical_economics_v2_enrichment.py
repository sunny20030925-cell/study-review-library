from __future__ import annotations

import copy

from mathematical_economics_v2_corrections import CHAPTERS_V2 as CORRECTED


def enriched_chapters():
    chapters = copy.deepcopy(CORRECTED)
    by_id = {c['id']: c for c in chapters}

    ch = by_id['ch02']
    ch['definitions'].append(('矩陣秩（rank）', '矩陣中線性獨立列／欄的最大數目；在線性系統中可用來判斷方程資訊是否足夠、是否彼此矛盾。'))
    ch['formulas'].extend([
        (r'x=\frac{c_1b_2-c_2b_1}{D}', '二元線性系統在 D≠0 時的 Cramer 解。'),
        (r'y=\frac{a_1c_2-a_2c_1}{D}', '與上一式配對；D=a_1b_2-a_2b_1。'),
    ])
    ch['intuition'].append('當 D=0 時不能直接說「無解」：可能是兩條限制互相矛盾，也可能其實是同一條限制的倍數而有無限多解；此時要回到方程或比較係數矩陣與增廣矩陣的 rank。')
    ch['traps'] = ['只解出價格就不代回數量。', '看到 D=0 就直接宣稱無解；D=0 也可能有無限多解。', '消去變數或 Cramer 分子排列時符號錯誤。']
    ch['exam'] = ['先數未知數與獨立方程。', 'D≠0 可直接判唯一解；D=0 時改看方程是否矛盾或 rank 是否一致。', '解完代回每一式，確認同時成立並符合經濟可行域。']

    ch = by_id['ch03']
    ch['definitions'].extend([
        ('內積（dot product）', '同維向量逐項相乘後加總得到純量；幾何上可用來描述投影、正交與方向相似度。'),
        ('線性組合', '以純量係數加權多個向量後相加；矩陣乘向量可視為矩陣各欄向量的線性組合。'),
    ])
    ch['formulas'].extend([
        (r'x^Ty=\sum_i x_i y_i', '同維向量的內積；若 x^Ty=0，稱兩向量正交。'),
        (r'A(x+y)=Ax+Ay', '矩陣乘法對向量加法具有分配律。'),
        (r'A(Bx)=(AB)x', '矩陣乘法具有結合律，但一般不具有交換律。'),
    ])
    ch['example'].append('若 A 是 2×3、x 是 3×1，則 Ax 是 2×1；把 x 寫成欄向量後，Ax 也可看成 A 的三個欄向量按 x 的三個係數做線性組合。')
    ch['traps'] = ['逐元素相乘後說那是矩陣乘法。', '忽略列向量／欄向量與尺寸就直接相乘。', '把 AB=BA 當一般規則；即使 AB、BA 都存在，兩者通常也不同。']
    ch['exam'] = ['先在矩陣與向量旁標尺寸。', '矩陣乘法用「列乘欄」，向量內積則是同維逐項乘後加總。', '遇到轉置乘積用 (AB)^T=B^TA^T；遇到多個乘法可用結合律重新分組，但不可任意換順序。']

    ch = by_id['ch16']
    ch['definitions'].append(('累積函數', '若 A(x)=∫_a^x f(t)dt，則在 f 連續處 A′(x)=f(x)；這是微積分基本定理的另一個方向。'))
    ch['formulas'].extend([
        (r'\frac{d}{dx}\int_a^x f(t)dt=f(x)', '被積函數連續時，累積量對上限的邊際變化就是當下被積值。'),
        (r'CS=\int_0^{Q^*}[P_D(q)-P^*]dq', '需求曲線在交易量區間內高於市場價格時，消費者剩餘可寫成這個面積積分。'),
    ])
    ch['example'] = [
        '例 1：MC(q)=2q+4，且 C(0)=10。則 C(q)=10+∫_0^q(2s+4)ds=10+q²+4q；q=3 時 C=31。',
        '例 2：反需求 P_D(q)=20-q，市場價格 P*=8。交易量由 20-Q=8 得 Q*=12。',
        '因此消費者剩餘 CS=∫_0^{12}[(20-q)-8]dq=∫_0^{12}(12-q)dq=72；這裡 integrand 在區間內非負，所以帶符號積分也等於幾何面積。',
    ]
    ch['traps'] = ['不定積分忘記 +C。', '把任何定積分都直接叫幾何面積，忽略函數在 x 軸下方時會帶負號。', '由邊際量還原總量時忘記初始條件；沒有 C(0) 就不能唯一決定總成本水準。']
    ch['exam'] = ['看到「邊際→總量」就想到積分，並尋找初始條件。', '看到「累積量對上限求導」就想到微積分基本定理。', '剩餘／福利面積題先確認上下界與 integrand 正負，再決定是否需要分段或取絕對值。']

    return chapters


CHAPTERS_V2 = enriched_chapters()
assert len(CHAPTERS_V2) == 20
