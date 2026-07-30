# 《投資學》製作狀態

更新日期：2026-07-30

## 正式識別

- Book ID：`investments`
- 正式內容版本：`2026.07.30-1`
- 正式書庫版本：`2026.07.30-15`
- 目前 stage：`PUB`
- Task ID：`investments:PUB`
- 下一階段：無；本書新制流程已完成。
- Published：`passed`。
- 範圍：`docs/books/investments/scope.md`
- Internal QA：`docs/books/investments/qa_report.md`
- External Audit：`docs/books/investments/external_audit.md`

## Internal QA 證據

- 正文 22 章、附錄 3 份、題庫 110 題、搜尋索引 165 筆、SVG 22 張。
- 第一輪 QA：2,672／2,672；第二輪：139／139。
- 45 項量化節點、20 項高風險概念重判；發布後 reaudit validator 730 項通過。

## External Audit

- 結果：`passed`
- 路由：Wolfram + Consensus。
- 抽查 returns／portfolio risk、CAPM/APT、EMH/event study、behavioral finance、valuation、bonds/duration、derivatives、performance。
- 核心答案錯誤：0；需要升版：否；unresolved blocker：0。

## 相容性與部署

Book ID、22 個章節 ID、110 個題目 ID、PWA 儲存鍵、閱讀進度與錯題紀錄均不變；正式 21 本 artifact 已更新為 `2026.07.30-15`，Pages artifact `8760756025`，重新下載 SHA256 與 digest 完全一致。

## Visual Polish 完成（2026-07-30）

- Task：`investments:VP`；結果：`passed`。
- 高價值資產：`投資學考前模型選擇地圖`。
- Canva design ID：`DAHQ22yayGI`；可編輯來源：`https://www.canva.com/d/YcSot4oME9FMJ6w`。
- PWA 資產：`assets/investments-svg/investment-map.svg`；平板可閱讀、可放大、沿用既有離線 cache path。
- 正式 run：`30546107426`；Pages artifact：`8760756025`。
- Artifact digest：`sha256:9d3d3d3a3c5b6622d5359f6fd14c4ca481e3e5d0517674ba64fe1ff147b8f304`；重新下載 SHA256 完全一致。
- VP validator：`89 checks`，正式部署前與 artifact 重下載後均 `visual_polish=passed`。
- 正式內容版本未因純視覺整理升版；閱讀進度、錯題資料與 storage key 相容，`progress_storage_changed=false`。
- 詳細證據：`docs/books/investments/visual_polish.md`。
- 本書已切換至 `investments:PUB`。
- 全書庫下一個 Visual Polish target：`statistics`。
