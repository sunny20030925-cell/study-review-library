# 大一微積分 Status

更新日期：2026-07-30

## 正式識別

- Book ID：`calculus`
- 正式內容版本：`2026.07.27-3`
- 正式書庫版本：`2026.07.30-9`
- 目前 stage：`VP`
- Task ID：`calculus:VP`
- 下一階段：`PUB`
- Published：workflow v2 前既有正式版本維持 `passed`。
- Internal QA：`docs/books/calculus/qa_report.md`
- External Audit：`docs/books/calculus/external_audit.md`

## Internal QA 證據

- 標準大一微積分正文 14 章；題庫 73 題；搜尋索引 150 筆。
- 本版 QA：181／181；公式、章節、題庫、圖片、JSON、JavaScript、內容版本與 PWA cache 一致性均通過。
- 經濟學取向內容已移除，維持純微積分科目本位。

## External Audit

- 結果：`passed`
- 路由：Wolfram。
- 抽查 domain、limits、derivatives、implicit differentiation、MVT/L'Hôpital、integrals、geometry applications、exp/log、series、multivariable calculus、constrained optimization 與 ODE。
- 代表性 73 題掃描與形式化重算未發現核心錯誤。
- 核心答案錯誤：0；需要升版：否；unresolved blocker：0。

## 相容性

章節／題目 ID、題數、PWA、閱讀進度與錯題資料均不變；正式 21 本 artifact 維持 `2026.07.30-9`。