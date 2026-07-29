# 《計量經濟學》External Audit

更新日期：2026-07-30  
Task ID：`econometrics:EA`  
Book ID：`econometrics`  
內容版本：`2026.07.30-1`

## 結論

- External Audit：`passed`
- 審計模式：risk-based sampling
- 路由：Wolfram + Consensus；Scite 未使用（抽查未遇到必須判定特定重要論文引用支持／反駁脈絡的主張）。
- 核心答案錯誤：0
- 需要內容修正／升版：否
- unresolved blocker：0

## 高風險抽查

- OLS 斜率、截距、殘差正交與 R²。
- 同質變異下 OLS 變異數、robust standard error、OVB 符號。
- LPM／logit 邊際效果、random walk／AR(1)、HAC 語境。
- IV／Wald ratio、RCT、DiD、RDD、out-of-sample prediction。
- 因果識別條件：strict exogeneity、exclusion restriction、SATE/PATE、parallel trends、RDD cutoff locality。

Wolfram 對代表性數值節點獨立重算，OLS 範例得到 slope `3/2`、intercept `1/3`、`R²=27/28`；OVB、robust-t、logit marginal effect、AR(1)、IV、RCT、DiD、RDD 與 prediction 節點均與正式教材一致。

Consensus 針對方法論風險抽查：Jon Roth (2022) 對 pre-trend testing 的限制、Cattaneo & Escanciano (2021) 對 RDD 的局部識別框架、Degtiar & Rose (2021) 對 generalizability／transportability 的條件，均支持教材目前的限定語句；未發現把前趨勢不顯著當成平行趨勢證明、把 RDD 當全域效果或把 random assignment 直接等同 PATE 的過度主張。

## 相容性

本輪僅新增審計證據與更新狀態；教材正文、題庫、Book ID、chapter ID、question ID、搜尋、SVG、PWA、閱讀進度與錯題資料均未修改。