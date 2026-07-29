# 《賽局理論及應用》製作狀態

更新日期：2026-07-30

## 正式識別

- Book ID：`game-theory`
- 目前正式內容版本：`2026.07.29-1`
- 第二次內容重審候選版本：`2026.07.30-2`
- 目前正式書庫：20 本，shared library `2026.07.30-2`（v2 候選 QA 讀取 current `main` deployment receipt 時的正式基底）。
- 狀態：v1 已部署；v2 內容重審與隔離 artifact QA 已通過，待來源合併與正式發布。
- 範圍文件：`docs/books/game-theory/scope.md`
- 初版 QA：`docs/books/game-theory/qa_report.md`
- v2 重審報告：`docs/books/game-theory/v2_audit_report.md`

## v2 成品

- 正文：20 章。
- 附錄：3 份。
- 題庫：100 題，每章 5 題。
- 搜尋索引：189 筆。
- 自製 SVG：20 張。
- Book ID、章節 ID、附錄 ID、100 個題目 ID 全部保留，閱讀進度與錯題紀錄相容。

## 第二次內容重審主要修正

- 分清 complete information 與 perfect information；向後歸納改以 finite perfect-information game 為標準直接適用場景。
- 修正 ch04：原 payoff game 有 `(U,L)`、`(D,R)` 兩個純 Nash，並另有 `p=0.6、q=0.4` 的 mixed Nash。
- rationalizability 補入 mixed-strategy strict dominance 的完整性提醒。
- 標準 Bertrand `p1=p2=c` 改為精確均衡敘述並列明模型條件。
- subgame 定義補明起點必須是 singleton information set，且不能切斷任何資訊集合。
- Bayesian 進入例題改為「給定 type-contingent strategy 下的 expected best response」，不再暗示已完成動態 PBE。
- 第二價 truthful weak dominance 與 i.i.d.／risk-neutral 假設拆分；共同／相互依賴價值另行分析。
- PBE 補強 on-path Bayes、off-path belief 與 sequential rationality 邊界。
- signaling 教育例題重算 cross-type IC：`2≤e≤6`；連續訊號空間仍需 off-path beliefs／任意 deviation 檢查才能完成 PBE。
- Rubinstein、VCG payment sign convention、strategic complements 的 ordered-strategy 前提補強。

## v2 QA

成功 candidate workflow：`30488598568`

- 正式基底：20 本、shared library `2026.07.30-2`、game-theory v1。
- v2 artifact audit：`GAME_THEORY_V2_AUDIT_OK checks=504`；21 個數值節點獨立重算、19 個高風險概念重判。
- v2 source second pass：`GAME_THEORY_SECOND_PASS_OK checks=375`；24 個數值節點獨立重算、23 個概念重判。
- 23 個章節／附錄 HTML、100 題、189 搜尋、20 SVG 全部通過。
- 除 game-theory 外的所有正式教材逐檔 SHA-256 與 shared `app.js` hash 在 patch 前後完全一致。

## 下一步

- 合併 v2 source PR。
- 正式發布前再次從最新 `main` 讀 deployment receipt 與 Pages artifact；若其他教材已先發布，v2 直接接最新正式 artifact，不使用候選測試的固定書籍數或 shared-library 版本。
- 正式部署成功後，再把正式 game-theory version、shared library version、Pages run、artifact ID／digest 寫回 status、QA report、shared checkpoint 與 deployment receipt。
