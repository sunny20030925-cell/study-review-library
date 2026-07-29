# 《賽局理論及應用》製作狀態

更新日期：2026-07-29

## 正式識別

- Book ID：`game-theory`
- 候選內容版本：`2026.07.29-1`
- 狀態：兩輪候選 QA 已完成，來源版可進入合併；尚未部署到正式共同書庫。
- 範圍文件：`docs/books/game-theory/scope.md`
- QA 報告：`docs/books/game-theory/qa_report.md`

## 候選成品

- 正文：20 章（ch00–ch19）。
- 附錄：3 份。
- 題庫：100 題，每章 5 題。
- 搜尋索引：189 筆。
- 自製 SVG：20 張。
- 平板功能：候選產生器沿用共同 PWA 的連續閱讀、章節導覽、全文搜尋、題庫、閱讀進度、錯題紀錄與離線快取資料結構。

## 內容主線

- 策略式賽局、最佳回應、優勢／劣勢、合理化。
- 純策略與混合策略 Nash equilibrium、零和 minimax。
- 連續策略與 Cournot／Bertrand。
- 展開式賽局、向後歸納、SPNE、可信威脅與承諾。
- 議價、重複賽局。
- Bayesian game、拍賣、PBE、訊號、篩選與 cheap talk。
- 機制設計入門、合作賽局、擁擠／網路應用與綜合解概念選擇。

## QA

- 第一輪候選驗證：PASS。
- GitHub Actions run：`30468164830`。
- 主 validator：`GAME_THEORY_QA_OK checks=2385`。
- 第二輪獨立複核：`GAME_THEORY_SECOND_PASS_OK checks=360`。
- 第二輪獨立重算 24 個數值節點、另做 19 個高風險概念 gate。
- 第二輪實際抓到 5 題詳解過短，已補足推導、模型條件或經濟含意後重新通過。
- 候選生成前後，既有正式書籍逐檔 SHA-256 無差異；平板端章節、圖解、搜尋與題庫資產路徑全部通過。

## 尚未完成

- 合併來源 PR #78。
- 正式發布前必須重新讀最新 `main`、`docs/shared_checkpoint.md`、registry 與 `docs/deployment_receipt.json`。
- 共同書庫整合與 GitHub Pages 部署必須依最新正式 artifact 序列進行，避免與其他並行教材互相覆蓋。
- 部署後仍需以正式 Pages artifact／deployment receipt 驗證書籍數量、library version 與 `game-theory` 實際存在。
