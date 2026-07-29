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

## 正式發布結果

- 第一輪結構／內容 QA：通過。
- 第二輪獨立 QA：27 個量化節點重算、45 個高風險概念 gate，全部通過。
- 既有 12 本內容 hash：整合前後完全一致。
- 正式書庫：13 本，版本 `2026.07.29-18`。
- Pages run：`30469711077`。
- Pages artifact：`8731080555`；digest `sha256:e94982473758beeee6234d33e0962b979267c9f46ab9e0a8b9926c9cce66a25b`。
- 部署後 artifact 重新下載：23 份本書 HTML、100 題、189 搜尋、20 SVG 全數核對通過。
- post-deploy recorder：`passed-structured-recorder`；已移除舊版依賴 checkpoint 自然語句的硬比對流程。

## 第二次內容審計 v2（2026-07-30）

本輪不是重跑初版 QA，而是重新逐章審查公式、成立條件、參數化、例題與 100 題答案，優先處理「算式看似正確，但少一個條件就會誤導」的內容。

### 實際修正／補強

1. **充分與完備**：移除「完備性比充分性更強」的一般化說法。兩者是不同性質，一般互不推出；Lehmann–Scheffé 使用的是同一統計量同時完備且充分。
2. **Negative Binomial**：補齊「直到第 r 次成功的試驗總次數」參數化、支撐、PMF、期望與變異數，並明示另一種「失敗次數」口徑不可混用。
3. **多元常態**：條件常態公式明列聯合常態與 `Var(X)>0`；只有兩個邊際常態不足以套用。
4. **LLN／Slutsky／Delta method**：補正式 Slutsky 敘述與 studentization 例；補 `g'(theta)=0` 時一階 Delta method 退化的警告。
5. **MLE**：補 MLE invariance 與參數轉換例題。
6. **估計量品質**：補一致性、漸近常態；Fisher information／CRLB 明列內點與正則條件；Rao–Blackwell 明列平方可積／有限變異數語境。
7. **信賴區間**：區分常態且 sigma 已知時的精確 z 區間與一般 CLT 大樣本近似；精確 t 區間明列 iid 常態與 S² 定義。
8. **檢定理論**：分清 size 與 level alpha；p-value 補 composite null／nuisance parameter 校準；NP 補離散情況可能需 randomization。
9. **UMP／LRT／Wilks**：補 MLR／Karlin–Rubin 結構；Wilks 明列 H0、正則巢狀、可識別、內點條件及非正則邊界例外。
10. **線性模型**：Gauss–Markov 改成條件於 X 的 `E(epsilon|X)=0`、`Var(epsilon|X)=sigma²I`、full rank；精確 F 說明 q、p 與 `F_(q,n-p)`。

### 題庫調整

- 保留全部 100 個 question ID，只改 7 題內容／詳解：`ch03-q05`、`ch11-q01`、`ch13-q03`、`ch14-q04`、`ch15-q05`、`ch17-q04`、`ch18-q04`。
- 題數仍為每章 5 題，閱讀進度與錯題儲存鍵不變。

### 獨立 QA 與部署

- v2 reaudit validator：1059 項通過。
- 獨立數值重算：20 項通過；含 Negative Binomial、Slutsky 尺度轉換、Delta、χ²、t、Gamma、多元常態、次序統計量、Bayes、CI、p-value、OLS／R² 等。
- 其他正式教材逐檔 hash 比對：無變更。
- Book version：`2026.07.30-1`；shared library：`2026.07.30-6`，20 本。
- Pages run：`30490197263`；artifact：`8739358772`；digest `sha256:6936173acc641daef1c2e369a09407f2ee4533499735b78f5cbb280a147440ce`。
- 部署後重新下載 artifact，再次核對本書 23 份 HTML、100 題、189 搜尋、20 SVG 與 v2 QA 全部通過。
