# 《高等統計學》製作狀態

更新日期：2026-07-30

## 正式識別

- Book ID：`advanced-statistics`
- 正式內容版本：`2026.07.30-1`
- 正式書庫版本：`2026.07.30-9`
- 發布狀態：已部署（workflow v2 建立前的既有正式發布）。
- 目前工作階段：`VP`（Visual Polish）
- 目前 Task ID：`advanced-statistics:VP`
- 下一階段：`PUB`
- 範圍文件：`docs/books/advanced-statistics/scope.md`
- QA 報告：`docs/books/advanced-statistics/qa_report.md`
- External Audit：`docs/books/advanced-statistics/external_audit.md`

## Internal QA

- 正文 20 章、附錄 3 份、題庫 100 題、搜尋索引 189 筆、自製 SVG 20 張。
- 初版兩輪 QA：27 個量化節點獨立重算、45 個高風險概念 gate。
- 2026-07-30 第二次內容審計：10 個章節修正／補強區域、7 題題庫精確化；v2 validator 1059 項、獨立數值重算 20 項全數通過。
- 主要修正：完備性與充分性、Negative Binomial、Slutsky、MLE invariance、一致性／漸近常態、條件常態、Rao–Blackwell／CRLB、精確 z/t、size vs level、p-value／NP、UMP／MLR／Wilks、Gauss–Markov 條件。

## External Audit

- Task：`advanced-statistics:EA`
- 狀態：`passed`
- 日期：2026-07-30
- 主工具：Wolfram。
- 模式：風險式抽查，不做第三次全量 Internal QA。
- Wolfram 已獨立重算既有 20 個高風險數值節點；另驗算 Bernoulli Fisher information／CRLB 與 Exponential MLE invariance，全部一致。
- 定理成立條件另由人工逐項複核：條件常態、Slutsky、Delta method、MLE invariance、完備／充分、Rao–Blackwell、精確 z/t、size／level、NP、UMP／MLR／Wilks、Gauss–Markov／F-test 均未留下核心 blocker。
- Consensus／Scite 本輪未使用：抽查內容沒有需要以實證研究或論文引用脈絡判斷的核心主張。
- 核心答案錯誤：0；需要內容版本升級的修正：0；unresolved blocker：0。

## 相容性

- chapter IDs `ch00`–`ch19` 不變。
- 100 個 question IDs 與題數不變。
- 閱讀進度、錯題紀錄與 progress storage 相容。
- External Audit 未修改教材正文、題庫或 PWA 內容包；正式內容版本維持 `2026.07.30-1`。

## 既有正式部署

- canonical workflow：`Deploy study library`
- 成功正式 Pages run：`30494922034`
- source commit：`d502e3db8be674c030c5b13db88f1b33dfdedb28`
- Pages artifact：`8741187091`
- Artifact digest：`sha256:576f046c2f6e98f1cab56ca7136042e1dfb66a4af1ad21e74552ce16b2db1eeb`
- 正式書庫：21 本，版本 `2026.07.30-9`。

## 下一步

本書已具備進入 Visual Polish 的條件。Visual Polish 僅處理封面、章末重點、比較圖／流程圖、公式或考前速查表等高價值資產，不把教材搬離現有 PWA。
