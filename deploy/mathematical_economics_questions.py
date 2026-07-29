from __future__ import annotations

from mathematical_economics_content import CHAPTERS

NUMERIC = {
'ch00-q01': {'question':'模型 Q=120-3P 中，若 P=20，Q 等於多少？','answer':'60。','explanation':'Q=120-3×20=60。先辨認 P 是給定值，再代回函數。'},
'ch01-q01': {'question':'y=5+4x，當 x=3 時 y 等於多少？','answer':'17。','explanation':'y=5+4×3=17。'},
'ch01-q02': {'question':'y=10-2x 的反函數寫成 x 關於 y 的函數為何？','answer':'x=(10-y)/2。','explanation':'由 y=10-2x 移項：2x=10-y，所以 x=(10-y)/2。'},
'ch02-q01': {'question':'Qd=100-2P、Qs=20+2P。市場均衡價格與數量為何？','answer':'P*=20，Q*=60。','explanation':'令 Qd=Qs：100-2P=20+2P，得 P=20；代回 Q=60。'},
'ch03-q01': {'question':'A=[[1,2],[3,4]]，x=[2,1]^T。Ax 為何？','answer':'[4,10]^T。','explanation':'第一列：1×2+2×1=4；第二列：3×2+4×1=10。'},
'ch04-q01': {'question':'A=[[2,1],[1,1]] 的 determinant 為何？','answer':'1。','explanation':'det(A)=2×1-1×1=1，因此 A 可逆。'},
'ch04-q02': {'question':'Ax=b，其中 A=[[2,1],[1,1]]、b=[5,3]^T。x 為何？','answer':'[2,1]^T。','explanation':'解 2x+y=5、x+y=3，相減得 x=2，再得 y=1。'},
'ch05-q01': {'question':'A=diag(2,-1) 的兩個特徵值為何？','answer':'2 與 -1。','explanation':'對角矩陣的特徵值就是其主對角元素。'},
'ch05-q02': {'question':'對稱矩陣的特徵值為 3 與 1。此矩陣的定號為何？','answer':'正定。','explanation':'對稱矩陣所有特徵值皆為正，因此正定。'},
'ch06-q01': {'question':'用一階 Taylor 近似，以 a=10 估計 10.1^2。','answer':'約 102。','explanation':'f(x)=x^2，f(10)=100、f′(10)=20、Δx=0.1，所以約 100+20×0.1=102。'},
'ch06-q02': {'question':'f(x)=x^3，f′(2) 為何？','answer':'12。','explanation':'f′(x)=3x^2，所以 f′(2)=12。'},
'ch07-q01': {'question':'z=x^2+xy，在 x=2,y=3 時，f_x 與 f_y 各為何？','answer':'f_x=7，f_y=2。','explanation':'f_x=2x+y=7；f_y=x=2。'},
'ch07-q02': {'question':'承上題，在 x=2,y=3，若 Δx=0.1、Δy=-0.2，用全微分估計 Δz。','answer':'約 0.3。','explanation':'Δz≈7×0.1+2×(-0.2)=0.7-0.4=0.3。'},
'ch08-q01': {'question':'均衡 F(Q,a)=Q^2-a=0。在 Q=2 附近，dQ/da 為何？','answer':'1/4。','explanation':'dQ/da=-F_a/F_Q=-(-1)/(2Q)=1/(2Q)=1/4。'},
'ch08-q02': {'question':'承上題，在 Q=2 附近若 a 增加 0.4，用一階比較靜態估計 Q 增加多少？','answer':'約 0.1。','explanation':'ΔQ≈(dQ/da)Δa=(1/4)×0.4=0.1。'},
'ch09-q01': {'question':'Q=2P^{-2} 的點價格彈性為何？','answer':'-2。','explanation':'冪函數 Q=AP^a 對 P 的彈性等於指數 a，因此為 -2。'},
'ch10-q01': {'question':'π(q)=20q-q^2，q≥0。內點最大化的 q* 為何？','answer':'10。','explanation':'π′=20-2q=0 得 q=10；π″=-2<0。'},
'ch10-q02': {'question':'承上題，q*=10 時 π(q*) 為何？','answer':'100。','explanation':'π(10)=20×10-10^2=200-100=100。'},
'ch11-q01': {'question':'f(x,y)=10x+8y-x^2-y^2 的駐點為何？','answer':'(5,4)。','explanation':'FOC：10-2x=0、8-2y=0，所以 x=5、y=4。'},
'ch11-q02': {'question':'H=diag(-2,-2) 是正定、負定或不定？','answer':'負定。','explanation':'所有特徵值都為 -2<0，所以 H 負定。'},
'ch12-q01': {'question':'最大化 xy，限制 x+y=10 且 x,y>0。最適解為何？','answer':'x*=5，y*=5。','explanation':'L=xy+λ(10-x-y)。FOC 得 x=y=λ，再由 x+y=10 得 x=y=5。'},
'ch12-q02': {'question':'承上題，最大目標值 xy 為何？','answer':'25。','explanation':'5×5=25。'},
'ch13-q01': {'question':'最大化 10x-x^2，限制 0≤x≤3。最適 x 為何？','answer':'x*=3。','explanation':'無限制 FOC 給 x=5，但不符合 x≤3；目標在 [0,3] 仍遞增，因此邊界 x=3 最適。'},
'ch13-q02': {'question':'若一個 KKT 不等式限制有嚴格餘裕（slack），其對應乘數依互補鬆弛應為何？','answer':'0。','explanation':'互補鬆弛要求乘數×限制餘裕=0；餘裕不為 0 時乘數必須為 0。'},
'ch14-q01': {'question':'f(x,a)=ax-x^2/2。最適 x*(a) 為何？','answer':'x*=a。','explanation':'FOC：a-x=0，所以 x*=a。'},
'ch14-q02': {'question':'承上題，值函數 V(a) 與 V′(a) 為何？','answer':'V(a)=a^2/2，V′(a)=a。','explanation':'代 x*=a 得 V=a^2-a^2/2=a^2/2；微分得 V′=a，亦符合 envelope theorem 的 f_a=x*=a。'},
'ch15-q01': {'question':'Q=K^{0.4}L^{0.6} 的齊次次數為何？','answer':'1。','explanation':'Cobb–Douglas 型函數的齊次次數為指數和 0.4+0.6=1。'},
'ch15-q02': {'question':'承上題，K、L 同時都變成原來 2 倍，Q 變成幾倍？','answer':'2 倍。','explanation':'一次齊次函數滿足 Q(2K,2L)=2^1Q(K,L)=2Q。'},
'ch16-q01': {'question':'MC(q)=2q+4 且 C(0)=10。總成本函數 C(q) 為何？','answer':'C(q)=10+q^2+4q。','explanation':'C(q)=10+∫_0^q(2s+4)ds=10+q^2+4q。'},
'ch16-q02': {'question':'承上題，q=3 時 C(3) 為何？','answer':'31。','explanation':'10+3^2+4×3=10+9+12=31。'},
'ch17-q01': {'question':'本金 100 以每期 5% 離散複利兩期，期末值為何？','answer':'110.25。','explanation':'100×(1.05)^2=110.25。'},
'ch17-q02': {'question':'離散一期間成長率 i=5%，等效連續率 g 的精確表示為何？','answer':'g=ln(1.05)，約 0.04879。','explanation':'等效要求 e^g=1.05，所以 g=ln(1.05)≈0.04879。'},
'ch18-q01': {'question':'x_{t+1}=10+0.5x_t 的穩態 x* 為何？','answer':'20。','explanation':'令 x_{t+1}=x_t=x*：x*=10+0.5x*，所以 0.5x*=10，x*=20。'},
'ch18-q02': {'question':'一階差分 x_{t+1}=a+bx_t 的 b=-0.5。穩態附近路徑屬於哪種型態？','answer':'交替震盪並收斂。','explanation':'|b|=0.5<1，所以偏離量縮小；b<0 使正負方向逐期交替。'},
'ch19-q01': {'question':'ẋ=6-0.3x 的穩態 x* 為何？','answer':'20。','explanation':'穩態令 ẋ=0：0=6-0.3x*，所以 x*=20。'},
'ch19-q02': {'question':'承上題，F′(x*)=-0.3。穩態在一維局部判斷下是否穩定？','answer':'穩定。','explanation':'F′(x*)=-0.3<0，附近偏離會被拉回；解中的 e^{-0.3t} 也會衰減。'},
}

SPECIAL = {
'ch00-q05': {'question':'判斷：只要兩個變數滿足同一條方程，就已經證明其中一個造成另一個。','answer':'錯。','explanation':'方程描述模型關係，不會自動提供因果識別；因果需要額外假設或研究設計。'},
'ch05-q05': {'question':'判斷：對稱 Hessian 只要每個主對角元素都小於 0，就一定負定。','answer':'錯。','explanation':'二變數還要檢查 determinant 等主子式條件；一般情況需完整定號判斷。'},
'ch08-q05': {'question':'判斷：比較靜態導數 dQ/da 是 Q 隨時間的成長率。','answer':'錯。','explanation':'比較靜態比較參數改變前後的均衡，不描述調整所需的時間路徑。'},
'ch10-q05': {'question':'判斷：只要 f′(x*)=0，x* 就一定是最大值。','answer':'錯。','explanation':'FOC 只給候選點；還需二階條件、凹性、端點或直接比較。'},
'ch12-q05': {'question':'判斷：Lagrange multiplier 的正負與影子價格解讀完全不受 Lagrangian 符號寫法影響。','answer':'錯。','explanation':'把限制寫成 b-g 或 g-b 會改變 λ 的符號；必須連同符號慣例解讀。'},
'ch13-q05': {'question':'判斷：KKT 條件在任何非線性最佳化問題中都自動是充分條件。','answer':'錯。','explanation':'充分性通常需要目標與可行集合的凹凸性等額外條件。'},
'ch16-q05': {'question':'判斷：定積分 ∫_a^b f(x)dx 永遠等於曲線與 x 軸之間的幾何面積。','answer':'錯。','explanation':'定積分是帶符號面積；若函數跨過 x 軸，幾何面積需分段取絕對值。'},
'ch18-q05': {'question':'判斷：x_{t+1}=a+bx_t 只要 b<1 就一定收斂。','answer':'錯。','explanation':'收斂需要 |b|<1；例如 b=-2 雖然 -2<1，卻會發散震盪。'},
}


def default_question(ch, slot: int):
    term, desc = ch['definitions'][min(slot-1, len(ch['definitions'])-1)]
    formula, note = ch['formulas'][min(slot-1, len(ch['formulas'])-1)]
    if slot == 1:
        return {'question':f'下列關於「{term}」的定義，最精確的是什麼？','answer':desc,'explanation':f'先回到正式定義：「{term}」是：{desc}'}
    if slot == 2:
        return {'question':f'關係「{formula}」的使用條件或判讀重點是什麼？','answer':note,'explanation':f'公式不能脫離條件使用。本章明示：{note}'}
    if slot == 3:
        return {'question':f'綜合判斷：處理「{ch["title"]}」題目時，為什麼要先固定符號、可行域或基準點？','answer':'因為同一公式在不同定義域、符號慣例、基準點或限制條件下可能有不同結論。','explanation':ch['intuition'][0]+' '+ch['exam'][0]}
    if slot == 4:
        return {'question':f'圖形／結構題：若以「{ch["figure"][0]}」整理本章，最穩健的解題順序為何？','answer':'先辨認節點與數學物件，再套公式，最後檢查條件、符號與解的可行性。','explanation':'數理經濟學的圖解用來整理推導順序，不取代條件檢查。'}
    return {'question':f'常見陷阱判斷：「{ch["traps"][0]}」錯在哪裡？','answer':'它忽略本章必要的成立條件或把局部／條件性結論誤寫成無條件結論。','explanation':f'正確作法是：{ch["exam"][0]}'}


def build_questions():
    items=[]
    for ch in CHAPTERS:
        for slot in range(1,6):
            qid=f'{ch["id"]}-q{slot:02d}'
            item={'id':qid,'chapterId':ch['id'],**default_question(ch,slot)}
            if qid in SPECIAL: item.update(SPECIAL[qid])
            if qid in NUMERIC: item.update(NUMERIC[qid])
            items.append(item)
    assert len(items)==100
    assert len({x['id'] for x in items})==100
    return items
