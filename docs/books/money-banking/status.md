# 《貨幣銀行學》製作狀態

更新日期：2026-07-29

## 正式識別

- Book ID：`money-banking`
- 目標正式內容版本：`2026.07.29-2`
- 目前狀態：完整內容與二次糾錯層已準備，等待 canonical Pages run 驗證與正式部署。
- 範圍文件：`docs/books/money-banking/scope.md`
- QA 報告：`docs/books/money-banking/qa_report.md`

## 成品

- 正文：20 章（ch00–ch19）。
- 附錄：3 份。
- 題庫：100 題，每章 5 題。
- 搜尋索引：150 筆。
- 自製 SVG：20 張。
- 平板功能：沿用共同 PWA 的閱讀、搜尋、題庫、進度、錯題與離線快取。

## 本次修正

- 已套用 9 個章節的第二次內容精確化：債券報酬、存續期間、銀行監理與最後貸款者、準備貨幣與放款創造存款、貨幣乘數、臺灣央行政策工具、Fisher、QE、匯率方向。
- 已同步 7 題高風險題目詳解與 9 個章節的搜尋索引文字。
- 章節 ID、題目 ID、題數與既有 11 本教材內容均不得因本次新增而變更。
- 正式整合會重新執行既有結構 QA、v2 獨立 QA 與 20 個量化節點重算。

## 發布條件

- 以當下最新 11 本正式書庫作基底，貨幣銀行學只能追加為第 12 本。
- 全站版本只能由目前正式版本順增，不得沿用舊候選線版本。
- 修正既有 post-deploy recorder 對 numbered checkpoint heading 的相容問題，避免 Pages 已成功卻 workflow 顯示 failure。
- 正式 Pages artifact、deployment 與 deployment receipt 全部確認後，才把本狀態改為「已部署」。
