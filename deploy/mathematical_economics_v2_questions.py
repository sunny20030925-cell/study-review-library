from __future__ import annotations

from mathematical_economics_questions import build_questions as build_v1_questions

VERSION = '2026.07.30-2'

PATCHES = {
    'ch05-q03': {
        'question': '若 Av=λv 且 λ<0，對特徵向量 v 應如何解讀矩陣作用後的方向？',
        'answer': '仍在同一條一維子空間上，但方向反轉。',
        'explanation': 'Av=λv 代表結果仍是 v 的純量倍數；λ<0 時倍數為負，因此所在直線不變，但有向方向反轉。',
    },
    'ch06-q03': {
        'question': 'y=(3x+1)^2。用鏈鎖律求 x=1 時 dy/dx。',
        'answer': '24。',
        'explanation': '外層平方先微分得 2(3x+1)，再乘內層函數 3x+1 的導數 3，所以 dy/dx=2(3x+1)×3；代 x=1 得 24。',
    },
    'ch07-q03': {
        'question': '判斷：對可微函數，dz=f_xdx+f_ydy 與有限變動 Δz=f_xΔx+f_yΔy 永遠完全相等。',
        'answer': '錯。',
        'explanation': 'dz 是基準點的一階線性微分；有限變動通常只能寫 Δz≈f_xΔx+f_yΔy，除非函數本身是適當的線性／仿射形式。',
    },
    'ch09-q02': {
        'question': 'Q=AK^{0.3}L^{0.7}。若 K 小幅增加 1%、L 小幅增加 2%，用對數微分估計 Q 約增加多少？',
        'answer': '約 1.7%。',
        'explanation': 'd ln Q≈0.3 d ln K+0.7 d ln L，所以約為 0.3×1%+0.7×2%=1.7%。',
    },
    'ch11-q03': {
        'question': '若 f 定義在凸集合上、為 C²，且 Hessian 在所有點都負半定，可推出什麼？',
        'answer': 'f 為凹函數。',
        'explanation': '在凸定義域上，C² 函數 Hessian 處處負半定可推出凹性；負定處處成立則是嚴格凹的一個充分條件。',
    },
    'ch12-q03': {
        'question': '最大化 xy、限制 x+y=10。在候選點 (5,5)，沿限制的切方向 d=(1,-1)，若 dᵀH_Ld=-2，這支持哪個結論？',
        'answer': '支持該候選點是受限嚴格局部最大。',
        'explanation': '等式限制的二階條件只檢查滿足 ∇gᵀd=0 的可行切方向；非零切方向上二次型嚴格為負支持嚴格局部最大。',
    },
    'ch13-q03': {
        'question': '判斷：只要問題可微，任何局部最適點都一定滿足 KKT，完全不需要其他條件。',
        'answer': '錯。',
        'explanation': 'KKT 的必要性一般還需要適當 constraint qualification，例如 LICQ；凸問題也常用 Slater 條件。',
    },
    'ch14-q03': {
        'question': '受限制最適化中，若參數 θ 同時出現在目標與限制，包絡定理最穩健的寫法為何？',
        'answer': 'dV/dθ=∂L/∂θ，在最適解與最適乘數處評估。',
        'explanation': '受限制 envelope theorem 用最適 Lagrangian 對參數的偏導，可同時納入目標與限制中的直接參數效果。',
    },
    'ch15-q03': {
        'question': 'homothetic 函數可由哪一類轉換作用在齊次函數上得到？',
        'answer': '嚴格遞增轉換。',
        'explanation': 'homotheticity 要保留等值集合與排序的徑向結構，因此使用嚴格遞增轉換；不能把任意遞減轉換也算進來。',
    },
    'ch18-q03': {
        'question': '一階差分 x_{t+1}=a-x_t，也就是 b=-1。一般從非穩態初值出發會怎樣？',
        'answer': '通常形成二期循環，不會漸近收斂到穩態。',
        'explanation': '|b|=1 是邊界情形。偏離量每期乘 -1，大小不縮小，只在穩態初值時保持在穩態。',
    },
    'ch19-q03': {
        'question': '一維自治系統 ẋ=F(x) 在穩態 x* 若 F′(x*)=0，可以只靠線性化判斷穩定嗎？',
        'answer': '不可以，線性化判準在此不下結論。',
        'explanation': 'F′(x*)<0 可判局部漸近穩定、>0 可判不穩定；等於 0 時需檢查更高階或原非線性動態。',
    },
}


def build_questions_v2():
    items = build_v1_questions()
    by_id = {q['id']: q for q in items}
    for qid, patch in PATCHES.items():
        if qid not in by_id:
            raise AssertionError(f'missing question id {qid}')
        by_id[qid].update(patch)
    assert len(items) == 100
    assert len({q['id'] for q in items}) == 100
    return items
