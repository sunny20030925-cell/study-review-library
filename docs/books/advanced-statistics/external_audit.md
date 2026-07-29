# 《高等統計學》External Audit

更新日期：2026-07-30

- Book ID：`advanced-statistics`
- Task ID：`advanced-statistics:EA`
- 內容版本：`2026.07.30-1`
- 模式：風險式抽查（risk-based sampling）
- 主要外部工具：Wolfram
- Consensus／Scite：本輪未使用；抽查範圍未發現需要以實證研究結論、學術爭議或重要論文引用脈絡驗證的核心內容。

## 抽查理由

依 `docs/external_audit_workflow.md`，本輪不重做第三次全量 Internal QA，而集中在先前第二次內容審計曾修正、條件較多、錯誤成本較高的統計推導與數值節點：Negative Binomial、聯合常態條件分配、Slutsky、Delta method、MLE invariance、Fisher information／CRLB、精確 z/t、size／level、Neyman–Pearson、UMP／MLR／Wilks、Gauss–Markov 與 OLS。

## Wolfram 外部驗算

使用 Wolfram Language 以獨立式重新計算既有 v2 validator 的 20 個數值節點，並額外驗算 Fisher information 與 MLE invariance。

結果：

1. Negative Binomial（總試驗次數口徑）`P(X=7)=768/15625=0.049152`：通過。
2. 同口徑 `E(X)=15`、`Var(X)=60`：通過。
3. `N(0,1)` 除以 2 後變異數 `1/4`：通過。
4. Delta method 例 `g(x)=log x`、`g'(2)=1/2`、原漸近變異數 9，轉換後為 `9/4`：通過。
5. χ² 範例統計量：9：通過。
6. t 範例統計量：2：通過。
7. Gamma 例變異數：`3/4`：通過。
8. 多元變異數例：3：通過。
9. 條件常態變異數例：`3/4`：通過。
10. 次序統計量例均值：`{4/5,1/5}`：通過。
11. Binomial(5,0.2) 恰 1 次成功：`256/625=0.4096`：通過。
12. Poisson(2) 零事件：`0.1353352832366127`：通過。
13. Exponential(rate=1) 尾機率：`0.3678794411714423`：通過。
14. Bayes 範例：`1/3`：通過。
15. z 統計量：`2.5`：通過。
16. 雙尾 z p-value：`0.01241933065155227`：通過。
17. z 區間：`[9.608,10.392]`：通過。
18. t 區間：`[17.936,22.064]`：通過。
19. OLS：斜率 `3/2`、截距 `2/3`：通過。
20. OLS：SSE=`1/6`、`R²=27/28`：通過。
21. Bernoulli 單一觀測 Fisher information：`1/[p(1-p)]`；n 筆為 `n/[p(1-p)]`，CRLB=`p(1-p)/n`：通過。
22. Exponential(rate=λ) 若 `λ_hat=1/Xbar`，以 invariance 估 `m=1/λ` 得 `m_hat=Xbar`：通過。

## 高風險條件人工複核

Wolfram 適合驗算可形式化部分；定理成立條件仍逐項與教材目前文字核對：

- 二維條件常態：教材已明列「聯合常態」與 `Var(X)>0`；沒有把「兩邊際常態」誤當充分條件。
- Slutsky：收斂型態與常數分母 `c!=0` 條件正確。
- Delta method：已明列 `g'(theta)=0` 時一階極限可能退化，須考慮更高階方法。
- MLE invariance：教材保留 MLE 存在／最大值集合與非一對一轉換的必要語意限制。
- 完備性 vs 充分性：沒有一般包含關係；Lehmann–Scheffe 所需的是同一統計量同時完備且充分。
- Rao–Blackwell：平方可積／有限變異語境與 `Var(E(U|T)) <= Var(U)` 正確，沒有宣稱一定嚴格下降。
- 精確 z／t：已把常態、σ 已知／未知與 `S²` 定義分開；非正態只稱 CLT 大樣本近似。
- size／level：`level alpha` 只要求 `size<=alpha`，不要求等號。
- p-value：沒有誤寫成 `P(H0|data)`；composite null／nuisance parameter 另需有效校準。
- Neyman–Pearson：限定 simple vs simple；離散情況允許臨界點 randomization。
- UMP／MLR／Wilks：已限制於合適單參數 MLR 結構與正則、巢狀、可識別、內點條件；邊界／不可識別情形沒有硬套標準 χ²。
- Gauss–Markov：`E(epsilon|X)=0`、`Var(epsilon|X)=sigma²I`、X full column rank；BLUE 不依賴常態。精確小樣本 t/F 另要求常態誤差。
- F 檢定：q 個獨立線性限制、unrestricted model 參數數 p、分母自由度 `n-p` 的表達一致。

## 發現與修正

- 核心答案錯誤：0。
- 需要內容版本升級的實質修正：0。
- unresolved blocker：0。
- 本輪不消耗 Consensus／Scite 額度，因沒有抽到需要研究證據或引用脈絡才能判斷的核心敘述。

## 相容性

本輪只新增 audit record 與更新狀態控制檔；不修改教材正文、題庫、Book ID、chapter ID、question ID、閱讀進度、錯題資料或 PWA 內容包。

## 結論

`advanced-statistics:EA = passed`。

《高等統計學》可進入 `advanced-statistics:VP`。正式內容版本維持 `2026.07.30-1`。
