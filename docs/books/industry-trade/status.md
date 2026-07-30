# 《產業及貿易》狀態

更新日期：2026-07-30

## 正式識別

- Book ID：`industry-trade`
- 正式內容版本：`2026.07.29-1`
- 正式書庫版本：`2026.07.30-22`
- 目前 stage：`PUB`
- Task ID：`industry-trade:PUB`
- 下一階段：無；本書新制流程已完成。
- Published：`passed`。
- Internal QA：Round 1／Round 2 與正式部署證據保留。
- External Audit：`docs/books/industry-trade/external_audit.md`

## Internal QA 證據

- 正文 20 章、附錄 3 份、題庫 100 題、搜尋 160 筆、SVG 20 張。
- Round 1：1495；Round 2：545；100 題逐題複核、20 題數值題重算、12 個高風險章節重判。

## External Audit

- 結果：`passed`
- 路由：Wolfram + Consensus。
- 抽查 concentration/markup、scale、出口固定成本、tariff/subsidy、outsourcing 與 heterogeneous-firm trade conclusions。
- 核心答案錯誤：0；需要升版：否；unresolved blocker：0。

## 相容性

所有既有 ID、題數、PWA、閱讀進度與錯題資料均未修改；正式 21 本 artifact 維持 `2026.07.30-9`。

## Visual Polish 完成（2026-07-30）

- Task：`industry-trade:VP`；結果：`passed`。
- 高價值資產：`產業及貿易市場結構跨境策略與政策福利判斷地圖`。
- Canva design ID：`DAHQ4qrUfLQ`；可編輯來源：`https://www.canva.com/d/0BA4jmK8k64mjPs`。
- PWA 資產：`assets/industry-trade-svg/ch00.svg`；平板可閱讀、可放大、沿用既有離線 cache path。
- 正式 run：`30570357985`；Pages artifact：`8770517727`。
- Artifact digest：`sha256:402ad42b8613feb7c3a7fe980166e8cb6018a8620cca57aba04b59a47f0b1851`；重新下載 SHA256 完全一致。
- VP validator：`152 checks`，正式部署前與 artifact 重下載後均 `visual_polish=passed`。
- 正式內容版本未因純視覺整理升版；閱讀進度、錯題資料與 storage key 相容，`progress_storage_changed=false`。
- 詳細證據：`docs/books/industry-trade/visual_polish.md`。
- 本書已切換至 `industry-trade:PUB`。
- 全書庫下一個 Visual Polish target：`public-finance`。
