# 《數理經濟學》External Audit

更新日期：2026-07-30  
Task ID：`mathematical-economics:EA`  
Book ID：`mathematical-economics`  
內容版本：`2026.07.30-2`  
起始正式 main：`ea1fd64c152249f5f080af2a7e29dcf8a4f59dfe`

## 結論

- External Audit：`passed`
- 審計模式：risk-based sampling
- 主路由：Wolfram
- Consensus／Scite：未使用；本輪高風險項目皆屬可形式化數學、公式、最佳化與動態系統內容，沒有需要以實證研究或論文引用脈絡才能判斷的核心主張。
- 核心答案錯誤：0
- 需要內容修正：0
- 需要提高 content version：否
- unresolved blocker：0

## 抽樣依據

本輪沒有把 20 章全部重做第三次 Internal QA，而是直接以既有 v2 第二次內容審計曾修正／補強的 13 個高風險區域，以及 `deploy/qa_mathematical_economics_v2.py` 的 23 個代表性數值／公式節點與 10 個高風險邏輯 gate 為母體進行外部抽查。

重點包含：

- 線性系統的 determinant／rank 與一致性。
- 特徵值、特徵向量與 invariant span。
- 鏈鎖律、全微分、有限變動近似。
- 隱函數定理與 Jacobian 可逆條件。
- 彈性與 Cobb–Douglas 對數微分。
- 一元／多元最佳化與 Hessian。
- 等式限制下的切方向二階條件。
- KKT 的符號慣例、constraint qualification、互補鬆弛與充分性條件。
- constrained envelope theorem。
- homogeneous／homothetic 與 Euler 定理。
- 積分累積、複利／連續成長。
- 一階差分方程 `|b|=1` 邊界。
- 一維自治微分方程 `F'(x*)=0` 的線性化失效。

## Wolfram 獨立重算：23 個 QA 節點

以下均與 repo v2 QA 一致：

1. 需求量：`120-3×20 = 60`。
2. 均衡價格：`(100-20)/4 = 20`。
3. `det([[2,1],[1,1]]) = 1`。
4. `y=(3x+1)^2` 在 `x=1` 的鏈鎖律導數 = `24`。
5. 全微分節點：`7×0.1 + 2×(-0.2) = 0.3`。
6. 隱函數導數節點 = `1/4`。
7. 對應 `Δx=0.4` 的一階變化 = `0.1`。
8. `Q=2P^-2` 點彈性 = `-2`。
9. Cobb–Douglas 對數微分：`0.3×1% + 0.7×2% = 1.7%`。
10. `20x-x^2` argmax = `10`。
11. 上式最大值 = `100`。
12. 多元二次目標最適 `x=5`。
13. 同一問題最適 `y=4`。
14. `max xy, x+y=10` 的 `x=5`。
15. 可行切方向 `d=(1,-1)` 上二階型 = `-2`。
16. `max 10x-x^2, x<=3` 上界 KKT multiplier = `4`。
17. `f(x,a)=ax-x^2/2` 在 `a=2` 的 envelope derivative = `2`。
18. `K^0.4 L^0.6` 齊次次數 = `1`。
19. `C(q)=10+q^2+4q` 在 `q=3` = `31`。
20. `100×1.05^2 = 110.25`。
21. `ln(1.05) = 0.048790164169432...`。
22. `x_{t+1}=10+0.5x_t` 穩態 = `20`。
23. `xdot=6-0.3x` 穩態 = `20`。

## 額外形式化高風險檢查

- 線性系統：可逆例的 `rank(A)=rank([A|b])=2`；矛盾例得到 `rank(A)=1`、`rank([A|b])=2`，與教材相容性敘述一致。
- 負特徵值：`Av=λv, λ<0` 仍留在 `span(v)`，但有向方向反轉；教材用 invariant one-dimensional subspace 的說法正確。
- 多元二次目標：在 `(5,4)` gradient = `(0,0)`，Hessian eigenvalues = `(-2,-2)`。
- 等式限制：`max xy, x+y=10` 的切方向二階型為 `-2<0`，支持受限嚴格局部最大；沿限制直接化簡亦得到唯一全域最大 `(5,5)`。
- KKT 邊界例：`x*=3`、上界乘數 `μ=4` 同時滿足 stationarity 與 complementary slackness；教材明列 CQ 前提，未把 KKT 說成無條件必要條件。
- Envelope：無限制例直接微分值函數與在最適點取 `f_a` 結果相同；受限版 `dV/dθ=∂L/∂θ` 的條件與符號提醒保留完整。
- Euler：Cobb–Douglas `K f_K + L f_L = (a+b)f` 形式化恆等成立。
- 差分邊界：`b=-1` 兩期迭代後回到原偏離量，確認通常形成二期循環；`b=1` 時固定點存在性必須另看常數項，不能套收斂判準。
- `F'(x*)=0`：`xdot=-x^3` 與 `xdot=x^3` 在 `x*=0` 都有導數 0，但前者向 0、後者離開 0，直接證明線性化在此不下結論的敘述正確。

## 相容性與版本

- 本輪沒有修改教材正文、題庫、搜尋、SVG 或 PWA 資產。
- `Book ID` 不變。
- `chapter IDs` 不變。
- `question IDs` 不變。
- 閱讀進度、錯題資料與 PWA storage key 不變。
- 正式內容版本維持 `2026.07.30-2`。

## 基礎設施註記

目前 repo 已知的舊 deployment inline gate 仍假設 `industry-trade` 是 registry 最後一本；21 本正式 registry 的最後一本已是 `mathematical-economics`。此問題與本次 External Audit 結果無關；在下一次真正需要共同 PWA／Pages 發布前必須先修正。純狀態寫回使用 `[skip ci]`，不重跑已成功的 21 本正式 artifact。
