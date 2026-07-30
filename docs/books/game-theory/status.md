# 《賽局理論及應用》製作狀態

更新日期：2026-07-30

## 正式識別

- Book ID：`game-theory`
- 正式內容版本：`2026.07.30-2`
- 正式書庫版本：`2026.07.30-17`
- 目前 stage：`PUB`
- Task ID：`game-theory:PUB`
- 下一階段：無；本書新制流程已完成。
- Published：`passed`。
- Internal QA：`docs/books/game-theory/qa_report.md`、`docs/books/game-theory/v2_audit_report.md`
- External Audit：`docs/books/game-theory/external_audit.md`

## Internal QA 證據

- 正文 20 章、附錄 3 份、題庫 100 題、搜尋索引 189 筆、SVG 20 張。
- v2 artifact audit：504 項；21 個數值節點、19 個高風險概念。
- v2 source second pass：375 項；24 個數值節點、23 個概念重判。

## External Audit

- 結果：`passed`
- 路由：Wolfram。
- 抽查 mixed/zero-sum Nash、Cournot、sequential/commitment、Rubinstein、repeated games、Bayesian games、auctions、PBE/signaling、VCG、core/Shapley。
- 核心答案錯誤：0；需要升版：否；unresolved blocker：0。

## 相容性

Book／chapter／question IDs、題數、閱讀進度、錯題資料與 PWA 均不變；正式 21 本 artifact 為 `2026.07.30-17`。

## Visual Polish 完成（2026-07-30）

- Task：`game-theory:VP`；結果：`passed`。
- 高價值資產：`賽局理論資訊結構與均衡概念選擇地圖`。
- Canva design ID：`DAHQ3QeJvMk`；可編輯來源：`https://www.canva.com/d/qZaqmF_yGFYibV5`。
- PWA 資產：`assets/game-theory-svg/game-map.svg`；平板可閱讀、可放大、沿用既有離線 cache path。
- 正式 run：`30548922518`；Pages artifact：`8761921480`。
- Artifact digest：`sha256:9a96e0540acaf41a219ac45e327443a14d1c1ff142f9e106d3ba0ba2ea06bb3a`；重新下載 SHA256 完全一致。
- VP validator：`96 checks`，正式部署前與 artifact 重下載後均 `visual_polish=passed`。
- 正式內容版本未因純視覺整理升版；閱讀進度、錯題資料與 storage key 相容，`progress_storage_changed=false`。
- 詳細證據：`docs/books/game-theory/visual_polish.md`。
- 本書已切換至 `game-theory:PUB`。
- 全書庫下一個 Visual Polish target：`microeconomics`。
