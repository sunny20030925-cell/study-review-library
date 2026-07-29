# 《成本會計學》製作狀態

更新日期：2026-07-30

## 正式識別

- Book ID：`cost-accounting`
- 正式內容版本：`2026.07.29-2`
- 正式書庫版本：`2026.07.30-9`
- 目前 stage：`VP`
- Task ID：`cost-accounting:VP`
- 下一階段：`PUB`
- Published：workflow v2 前既有正式版本維持 `passed`。
- Internal QA：`docs/books/cost-accounting/qa_report.md`
- External Audit：`docs/books/cost-accounting/external_audit.md`

## Internal QA 證據

- 正文 19 章、附錄 3 份、題庫 95 題、搜尋索引 150 筆、SVG 19 張。
- 95／95 題重查；44／44 數值答案獨立重算；新版 validator 857／857。
- 已修正 materials flow、CVP 邊界、WA/FIFO process costing、spoilage、by-products、variances、absorption costing normal-capacity 等高風險節點。

## External Audit

- 結果：`passed`
- 路由：正式會計準則／規範 + Wolfram calculation only。
- 抽查 IAS 2 normal-capacity／unallocated overhead 邊界，以及 cost flow、CVP、EUP、ABC、joint cost、variances、absorption/variable costing 計算。
- 核心答案錯誤：0；需要升版：否；unresolved blocker：0。

## 相容性

章節／題目 ID、題數、PWA、閱讀進度與錯題資料均不變；正式 21 本 artifact 維持 `2026.07.30-9`。