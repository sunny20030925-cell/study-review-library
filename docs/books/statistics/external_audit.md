# 《統計學》External Audit

更新日期：2026-07-30  
Task ID：`statistics:EA`  
Book ID：`statistics`  
內容版本：`2026.07.29-2`

## 結論

- External Audit：`passed`
- 審計模式：risk-based sampling
- 主路由：Wolfram
- Consensus／Scite：未使用；本輪高風險項目為公式、分配與推論條件，無須消耗研究文獻額度。
- 核心答案錯誤：0
- 需要內容修正／升版：否
- unresolved blocker：0

## 高風險抽查

獨立重算／重判 weighted mean、sample variance、z-score、機率加法與條件機率、Bayes、期望與變異轉換、Binomial／Poisson、常態標準化、sampling SE、confidence interval、z/t tests、two-sample SE、chi-square expected count／df、ANOVA df 與簡單迴歸 `R²=r²` 的限定條件。

代表性 Wolfram 結果包含：sample variance `{2,4,6}=4`、Bayes posterior `0.307692...`、Binomial(3,.5) 的 `P(X=2)=0.375`、Poisson(2) 零次機率 `e^-2`、95% z interval `{46.08,53.92}`、chi-square 3×4 df=`6`、ANOVA 4 群 between df=`3`、`r=.8` 時簡單含截距迴歸 `R²=.64`，均與教材一致。

另重判 p-value 不是 `P(H0|data)`、fail to reject 不等於證明 H0、比例 CI 與比例檢定標準誤口徑不同等高風險語意，未見核心缺口。

## 相容性

本輪不改教材、題庫、搜尋、圖解或 PWA；章節／題目 ID、閱讀進度與錯題紀錄保持不變。