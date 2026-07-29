# 《總體經濟學》製作狀態

更新日期：2026-07-29

## 版本

- Book ID：`macroeconomics`
- 書籍版本：`2026.07.29-1`
- 預定書庫版本：動態順延；依目前正式七書 `2026.07.29-8` 計算，先整合《中級會計學》再整合本書後，預期為 `2026.07.29-10`
- 工作分支：`agent/macroeconomics-book-20260729-v2`

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

- 原先由成本會計 validator 提前生成本書的舊掛接已移除。
- Canonical PWA 產生器、動態版本 finalizer 與保留既有書籍的 validator：完成。
- PR gate：會以最新 `main` 組裝《中級會計學》與《總體經濟學》九書 workflow，檢查 Python、YAML 與關鍵部署步驟。
- 合併後由一次性整合 workflow 更新唯一 canonical `Deploy study library`，再自我移除；不建立第二條 Pages 部署線。
- 既有七本正式教材、閱讀進度儲存格式與錯題紀錄必須保持不變。
- GitHub Pages：待 PR gate、合併與正式九書部署驗證。

## 目前狀態

內容與兩輪 QA 已完成；尚未宣稱正式部署完成。最終完成門檻是 canonical GitHub Pages workflow 實際部署 9 本書、書庫版本動態順延成功，並寫回 `book_count=9` 的正式 deployment receipt。
