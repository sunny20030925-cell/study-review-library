# 《賽局理論及應用》第二次內容重審報告

更新日期：2026-07-30

## 結論

這次不是重跑原本 QA，而是重新閱讀正文、例題與題庫，針對解概念、資訊結構、公式成立條件與例題是否真正證成結論做獨立複核。

- v2 內容版本：`2026.07.30-2`
- 正文：20 章；附錄：3 份；題庫：100 題；搜尋：189 筆；SVG：20 張。
- Book ID、20 個章節 ID、3 個附錄 ID、100 個題目 ID 全部保留。
- 因 ID 不變，閱讀進度、錯題紀錄與平板端既有儲存相容。
- 最新隔離驗證直接取 current `main` 的正式 Pages artifact；驗證當下正式書庫為 20 本、shared library `2026.07.30-2`、game-theory 正式內容仍為 `2026.07.29-1`。
- v2 artifact QA：`GAME_THEORY_V2_AUDIT_OK checks=504`。
- v2 source second pass：`GAME_THEORY_SECOND_PASS_OK checks=375`。
- 數值重算：artifact QA 21 個、source second pass 24 個。
- 高風險概念重判：artifact QA 19 個、source second pass 23 個。
- 所有其他正式書籍與 shared `app.js` 在 v2 patch 前後 hash 完全一致。

## 實際找到並修正的內容

### 1. complete information 與 perfect information 混淆

舊版把完美資訊寫成完整資訊的單純「更強版本」，並把普通 backward induction 的適用條件寫成有限且「完全／完整資訊」。這不夠精確。

修正為：

- complete information：payoff functions、types 等 payoff-relevant 特徵是否共同已知。
- perfect information：展開式賽局中每個決策資訊集合是否為單點，亦即輪到玩家時能否辨認此前實際歷史。
- 標準 backward induction 的直接適用場景寫成有限 perfect-information game。
- 有非單點資訊集合時，不再只靠普通 backward induction；視題目改用 belief、PBE／sequential rationality 等工具。

### 2. 混合策略例題漏說兩個純策略 Nash

舊版 ch04 的 2×2 payoff：

- `(U,L)=(3,2)`
- `(U,R)=(0,0)`
- `(D,L)=(0,0)`
- `(D,R)=(2,3)`

其實已有兩個純策略 Nash：`(U,L)` 與 `(D,R)`，同時另有內點 mixed Nash。舊文字容易讓人誤以為這是「因為沒有純 Nash 才混合」。

修正後明確列出三個 Nash 類型；混合解仍為 A 以 `p=0.6` 選 U、B 以 `q=0.4` 選 L。

### 3. rationalizability 的完整判定

舊版主要用 pure-strategy dominance 說明反覆刪除。這適合入門直覺，但若題目正式要求 rationalizable strategies，可能漏掉「某純策略被一個 mixed strategy 嚴格支配」的情況。

修正後在定義、陷阱與考試判斷中加入 mixed-strategy strict dominance 的提醒。

### 4. Bertrand `p=c` 的表述

舊版寫成標準同質商品 Bertrand 下價格「趨向」 `p=c`。在教科書標準條件下，這應是純策略 Nash 的精確結論，而不是只說極限趨勢。

修正後寫明：同質商品、相同邊際成本、連續價格、無容量限制、消費者向最低價者購買等標準條件下，`p1=p2=c`。

### 5. 子賽局定義補完整

舊版只寫「從單一決策節點開始且不切斷資訊集合」，容易漏掉起點本身必須是一個 singleton information set。

修正後明確要求：起點本身是單點資訊集合，且後續不能切斷任何資訊集合。

### 6. Bayesian 進入例題的定位

舊版用 Tough／Weak 與 Fight／Accommodate 的動態故事示範 BNE 期望值，容易讓人誤以為只算進入者的期望 payoff 就完成整個動態均衡。

修正後明確把 `Tough→Fight、Weak→Accommodate` 當成「給定的 type-contingent strategy」來示範 expected best response；若 Fight／Accommodate 是進入後再選的動態行動，完整分析仍需檢查續局 sequential rationality／PBE。

### 7. 第二價拍賣的假設拆分

舊版把「truthful bidding 是 weakly dominant」和 i.i.d.／risk-neutral 等常見假設綁得太緊。

修正後分開：

- 第二價 truthful weak dominance 的核心是標準 private-value 與 threshold-payment 邏輯；價值彼此獨立不是這個弱優勢結果本身的必要條件。
- i.i.d.、risk neutrality 等假設主要用在本書第一價拍賣的簡潔 closed form 與標準 revenue equivalence。
- common/interdependent values 仍須重新分析，不能直接沿用 private-value truthful bidding 結論。

### 8. PBE 的 off-path 精度

補明：on-path positive-probability information set 依 Bayes rule；off-path beliefs 未必由 Bayes 唯一決定，但 action 仍須在指定 belief 下 sequentially rational。另提醒不同教材對 PBE off-path consistency 的形式定義可能略有差異，進階時可用 sequential equilibrium 等更強概念。

### 9. signaling 教育例題真正的 IC 範圍

舊版只檢查 `e=2.1`，且容易被讀成已經完整證明 separating PBE。

在簡化 wage schedule 中重新推導：

- H 不模仿 L：`10-e ≥ 4`，所以 `e≤6`。
- L 不模仿 H：`4 ≥ 10-3e`，所以 `e≥2`。
- 因此只看兩個 cross-type IC 時，候選範圍是 `2≤e≤6`，`e=2.1` 只是其中一點。

若 signal space 是連續的，這兩個 IC 仍不足以證明完整 PBE；還要指定其他 off-path `e` 的 beliefs／receiver action，並排除任意其他 deviation。

### 10. Rubinstein、VCG 與 strategic complements 的條件補強

- Rubinstein 份額公式補明標準 infinite alternating offers、完整資訊、拒絕延遲一期、固定 discount factors。
- VCG 補明標準 quasilinear private-value 環境，且 payment-to-mechanism 與 transfer-to-player 的正負號 convention 可能相反。
- strategic complements／substitutes 的「別人提高，我也提高／降低」語言補上 ordered strategy set 的前提，不再對任意離散標籤硬套。

## 題庫同步修正

題目 ID 不變，但下列高風險題目的題幹、答案或詳解已依 v2 同步：

- `ch02-q05`：mixed-strategy dominance 與 rationalizability。
- `ch04-q02`：純 Nash 與 mixed Nash 可共存。
- `ch06-q05`：標準 Bertrand `p=c` 的精確條件。
- `ch07-q01`、`ch07-q05`：finite perfect information 與 backward induction。
- `ch08-q05`：subgame 起點的 singleton information set。
- `ch11-q02`、`q03`、`q05`：BNE 期望值與動態 PBE 邊界。
- `ch12-q03`：第二價 truthful bidding 與 independence 假設拆分。
- `ch13-q01`、`q05`：PBE belief／off-path。
- `ch14-q04`：答案改為 `2≤e≤6`。
- `ch16-q03`：VCG payment sign convention。
- `ch18-q05`：strategic complements 的 ordered-strategy 前提。
- `ch19-q02`、`q05`：SPNE 與 complete/perfect information 分流。

## 驗證結果

成功 workflow run：`30488598568`

- 直接從 current `main` 取得 deployment receipt，再下載正式 Pages artifact 並核對 SHA-256。
- 正式 artifact 基底：20 本、shared library `2026.07.30-2`、game-theory v1。
- isolated v2 shared library：`2026.07.30-3`（只供候選驗證，正式發布時會依當時最新版本重新遞增）。
- `GAME_THEORY_V2_AUDIT_OK checks=504 quantitative_rechecks=21 conceptual_rechecks=19`
- `GAME_THEORY_SECOND_PASS_OK checks=375 quantitative_rechecks=24 concept_rechecks=23`
- 23 個 HTML、100 題、189 搜尋、20 SVG 均通過平板資產檢查。
- 所有非 game-theory 書籍逐檔 SHA-256 與 shared `app.js` hash 前後一致。

## 狀態

v2 內容與候選 artifact QA 已通過；尚待來源 PR 合併與正式 Pages v2 發布。正式發布前仍須再次以最新 deployment receipt／Pages artifact 為唯一基底，不使用本次候選的隔離 shared-library 版本號硬套正式環境。

## 正式 v2 發布結果

- 正式內容版本：`2026.07.30-2`。
- 正式 shared library：`2026.07.30-8`；正式書籍數：20 本。
- Pages run：`30490932468`；source commit：`3b5d3f894432810299bc30fc86fd741d3feb6ff8`。
- Pages artifact：`8739640949`；digest：`sha256:dfefd00509f0b661dc03bfc09bb98262ea762bab096769c7356256f09182d150`。
- 部署後重新下載 artifact：23 HTML、100 題、189 搜尋、20 SVG 全數存在。
- 部署後 `GAME_THEORY_V2_AUDIT_OK` 再次通過；其他教材與 shared `app.js` 維持不變。
- `progress_storage_changed=false`；Book／chapter／question IDs 未改，平板閱讀進度與錯題紀錄相容。
