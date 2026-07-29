# 《計量經濟學》製作狀態

更新日期：2026-07-30

## 正式識別

- Book ID：`econometrics`
- 正式內容版本：`2026.07.30-1`
- 正式書庫版本：`2026.07.30-9`
- 目前 stage：`VP`
- Task ID：`econometrics:VP`
- 下一階段：`PUB`
- Published：workflow v2 前既有正式版本維持 `passed`。
- 範圍：`docs/books/econometrics/scope.md`
- Internal QA：`docs/books/econometrics/qa_report.md`
- External Audit：`docs/books/econometrics/external_audit.md`

## Internal QA 證據

- 初版第一輪 QA：384 項；29 個數值節點獨立重算。
- 初版第二輪 QA：675 項；32 題高風險答案 gate。
- 發布後獨立內容審計 validator：57 項通過；已補 strict exogeneity 與 SATE/PATE 邊界。
- 正文 20 章、附錄 3 份、題庫 100 題、搜尋索引與 20 張 SVG 均已正式部署。

## External Audit

- 結果：`passed`
- 路由：Wolfram + Consensus。
- 高風險抽查：OLS／robust SE／OVB、time series、IV、RCT、DiD、RDD、prediction 與因果識別條件。
- 核心答案錯誤：0；需要升版：否；unresolved blocker：0。

## 相容性與部署

- Book ID、chapter ID、question ID、題數、閱讀進度與錯題資料均不變。
- 正式 21 本 Pages artifact 維持 `2026.07.30-9`；本輪純狀態寫回不重新部署教材。