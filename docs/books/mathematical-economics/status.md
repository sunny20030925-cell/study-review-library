# 《數理經濟學》製作狀態

更新日期：2026-07-30

## 正式識別

- Book ID：`mathematical-economics`
- 正式內容版本：`2026.07.30-2`
- 正式書庫版本：`2026.07.30-9`
- 狀態：已部署；第二次獨立內容審計、糾錯與修正完成。
- QA 報告：`docs/books/mathematical-economics/qa_report.md`

## 成品與第二次內容審計

- 正文 20 章、附錄 3 份、題庫 100 題、搜尋索引 150 筆、自製 SVG 20 張。
- 第二次獨立內容審計修正／補強 13 個核心區域，調整 11 題高風險題庫。
- v2 獨立 QA：855 項；數值／公式重算：23 項；高風險邏輯 gate：10 項，全部通過。
- 補強內容含 rank／聯立系統一致性、內積與線性組合、鏈鎖律、隱函數 Jacobian、凹性／擬凹性、受限二階條件、bordered Hessian、KKT 前提、constrained envelope theorem、積分累積與動態穩定邊界。
- Book ID、20 個章節 ID 與 100 個題目 ID 保持穩定；既有正式教材內容 hash 未改動。

## 部署

- canonical workflow：`Deploy study library`
- workflow run：`30494922034`
- source commit：`d502e3db8be674c030c5b13db88f1b33dfdedb28`
- Pages artifact：`8741187091`
- Artifact digest：`sha256:576f046c2f6e98f1cab56ca7136042e1dfb66a4af1ad21e74552ce16b2db1eeb`
- 正式書庫書籍數：21 本。
- Pages deployment、artifact 下載重驗與結構化 deployment receipt 均成功。
