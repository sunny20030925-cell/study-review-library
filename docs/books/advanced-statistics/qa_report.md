# 《高等統計學》QA 報告

更新日期：2026-07-29

## 版本與範圍

- Book ID：`advanced-statistics`
- 候選內容版本：`2026.07.29-1`
- 範圍：一般大學高等統計／數理統計核心。
- 結構：20 章、3 附錄、100 題、189 筆搜尋索引、20 張 SVG。

## 第一輪 QA

候選驗證固定檢查：

1. `ch00` 至 `ch19` 與 3 份附錄完整存在。
2. 每章具問題、白話直覺、定義、公式與成立條件、完整例題、錯誤、考試方法、理解檢查。
3. 100 題 ID 唯一且每章恰 5 題。
4. 搜尋索引 189 筆皆指向有效章節。
5. 20 張 SVG 具 `title`、`desc`、`viewBox`，且不依賴遠端圖片。
6. service worker 含本書所有離線核心路徑。
7. 既有 12 本教材逐書內容 hash 在整合前後完全一致。

## 第二輪獨立複核

第二輪不只比對儲存答案，另獨立重算／重判：

- 27 個具體數值節點：Bayes、Binomial、Poisson、Exponential、Gamma、Beta、共變異數、多元常態、Jacobian、次序統計量、CLT、Delta method、χ²、t、MLE、CI、z test／p-value、OLS／R² 等。
- 高風險概念：零共變異數與獨立、多元常態、MGF 存在、CLT、精確 t/χ²/F、likelihood、充分／完備、CRLB 正則條件、confidence coverage、p-value、NP、UMP、Wilks、Gauss–Markov 與 R²。
- 正面 token 與負面 forbidden-overclaim gate 同時存在，避免只檢查「有提到」卻把結論寫反。
- 特別檢查 finite-sample exact result 與 asymptotic result 不混用。

## 發布與整合 QA

- 候選工作流從 `docs/deployment_receipt.json` 指定的最新正式 Pages artifact 起算。
- 下載 artifact 先核對 digest、書庫版本與書籍數。
- 新書只允許追加在正式 `money-banking` 尾端。
- 書庫版本由正式版本順增一版；service worker 使用同一版本。
- 正式部署後重新下載該次 `github-pages` artifact，核對 digest、13 本 registry、本書 23 份 HTML、100 題、189 搜尋與 20 SVG。
- post-deploy recorder 改為結構化更新 receipt／status／README／shared checkpoint，不依賴舊章節自然語句。

## 發布狀態

目前記錄候選 QA 規格；正式 PR validation 與 Pages run 通過後，由結構化 recorder 回寫最終 run、artifact 與正式狀態。
