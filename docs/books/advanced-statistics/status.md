# 《高等統計學》製作狀態

更新日期：2026-07-29

## 正式識別

- Book ID：`advanced-statistics`
- 目標內容版本：`2026.07.29-1`
- 目前狀態：候選內容、題庫、圖解生成器與兩輪 QA gate 已建立；尚未標記正式部署。
- 範圍文件：`docs/books/advanced-statistics/scope.md`
- QA 報告：`docs/books/advanced-statistics/qa_report.md`

## 目標成品

- 正文 20 章、附錄 3 份。
- 題庫 100 題，每章 5 題。
- 搜尋索引 189 筆。
- 自製 SVG 20 張。
- 與既有《統計學》分工：本書聚焦數理統計、抽樣分配、估計與檢定理論。

## 發布條件

- 候選必須在最新正式 Pages artifact 上生成，不能從舊離線書庫覆蓋。
- 既有 12 本教材內容 hash 必須在整合前後完全一致。
- 結構、公式條件、100 題答案、27 個獨立數值節點與高風險概念 gate 必須通過。
- canonical Pages workflow 必須以結構化 deployment receipt 更新，不再依靠 shared checkpoint 的舊自然語句硬比對。
- Pages artifact、deployment、下載後 artifact recheck 與 deployment receipt 全部成功後，才可把狀態改為「已部署」。
