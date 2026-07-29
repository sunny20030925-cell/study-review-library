# 《貨幣銀行學》製作狀態

更新日期：2026-07-30

## 正式識別

- Book ID：`money-banking`
- 正式內容版本：`2026.07.29-2`
- 正式書庫版本：`2026.07.30-9`
- 目前 stage：`VP`
- Task ID：`money-banking:VP`
- 下一階段：`PUB`
- Published：workflow v2 前既有正式版本維持 `passed`。
- Internal QA：`docs/books/money-banking/qa_report.md`
- External Audit：`docs/books/money-banking/external_audit.md`

## Internal QA 證據

- 正文 20 章、附錄 3 份、題庫 100 題、搜尋索引 150 筆、SVG 20 張。
- 第一輪 963／963；第二輪 20 個量化節點＋10 個高風險概念；v2 QA 473／473。
- 已精確化 YTM、duration/convexity、銀行準備、deposit creation、money multiplier、臺灣央行工具、Fisher、QE 與匯率方向。

## External Audit

- 結果：`passed`
- 路由：Wolfram + 臺灣中央銀行官方資料。
- 抽查 time value、bond/duration、bank balance sheet、ROA/ROE、money multiplier caveat、準備金／公開市場／貼現窗口制度。
- 核心答案錯誤：0；需要升版：否；unresolved blocker：0。

## 相容性

Book／chapter／question IDs、題數、PWA、閱讀進度與錯題資料均不變；正式 21 本 artifact 維持 `2026.07.30-9`。