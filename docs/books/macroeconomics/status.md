# 《總體經濟學》製作狀態

更新日期：2026-07-29

## 版本

- Book ID：`macroeconomics`
- 書籍版本：`2026.07.29-1`
- 預定書庫版本：`2026.07.29-7`
- 工作分支：`agent/macroeconomics-book-20260729`

## 已固定範圍

- 定位：一般大學總體經濟學，深度高於《經濟學原理》的總體共同核心。
- 主線：總體衡量、長期成長、消費與投資、貨幣、短期景氣模型、財政貨幣政策、開放經濟。
- 核心模型：Solow、Keynesian Cross、IS–LM、AD–AS、預期增廣 Phillips curve、Mundell–Fleming。
- 排除：Ramsey／OLG／RBC／New Keynesian／DSGE 的正式動態最佳化與研究所級推導。

## 成品

- 正文：20 章。
- 附錄：3 份。
- 題庫：100 題，每章 5 題。
- 搜尋索引：143 筆。
- 自製圖解：20 張 SVG。
- 平板功能：沿用既有書庫的閱讀、搜尋、題庫、閱讀進度、錯題紀錄與離線快取。

## QA

- 第一輪製作內檢：通過。
- 第二輪獨立複核：通過。
- 100 題逐題重新檢查。
- 18 題需要具體數值結果的題目已獨立重算，18／18 一致。
- 已修正 Python／LaTeX 轉義、IS–LM 名目／實質利率條件與政府債務動態符號精度。
- QA 報告：`docs/books/macroeconomics/qa_report.md`。

## 整合狀態

- Canonical PWA 產生器：完成。
- 六書 canonical deployment gate：已加入工作分支。
- 既有五本書的正式修正流程：保留。
- 新增第六本不得改動既有閱讀進度儲存格式。
- GitHub Pages：待 PR 審查、合併與正式部署驗證。

## 目前狀態

內容與兩輪 QA 已完成；尚未宣稱正式部署完成。最終完成門檻是六本書的 canonical GitHub Pages workflow 實際成功，並寫回正式 deployment receipt。
