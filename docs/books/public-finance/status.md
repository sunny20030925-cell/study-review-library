# 《財政學》製作狀態

更新日期：2026-07-30

## 正式識別

- Book ID：`public-finance`
- 正式內容版本：`2026.07.29-2`
- 正式書庫版本：`2026.07.30-23`
- 目前 stage：`PUB`
- Task ID：`public-finance:PUB`
- 下一階段：無；本書新制流程已完成。
- Published：`passed`。
- Internal QA：`docs/books/public-finance/qa_report.md`
- External Audit：`docs/books/public-finance/external_audit.md`

## Internal QA 證據

- 正文 20 章、附錄 3 份、題庫 100 題、搜尋索引 189 筆、SVG 20 張。
- 舊結構／題庫／搜尋／SVG gate 2,386 項；v2 gate 174 項；獨立數值重算 38 項。
- 已修正公共 CBA、social insurance、health insurance、education signaling、tax incidence/DWL、Ramsey、ETI、property tax 與 debt dynamics 等條件。

## External Audit

- 結果：`passed`
- 路由：Wolfram。
- 抽查 CBA、surplus、externality/Pigou、Samuelson public goods、median voter、tax/welfare 與 debt arithmetic。
- 核心答案錯誤：0；需要升版：否；unresolved blocker：0。

## 相容性

章節／題目 ID、題數、PWA、閱讀進度與錯題資料均不變；正式 21 本 artifact 維持 `2026.07.30-23`。

## Visual Polish 完成（2026-07-30）

- Task：`public-finance:VP`；結果：`passed`。
- 高價值資產：`財政學機制歸宿與福利判斷地圖`。
- Canva design ID：`DAHQ4tQIk3M`；可編輯來源：`https://www.canva.com/d/APhMiW3N5hUN-R5`。
- PWA 資產：`assets/public-finance-svg/public-finance-map.svg`；平板可閱讀、可放大、沿用既有離線 cache path。
- 正式 run：`30573739506`；Pages artifact：`8771835026`。
- Artifact digest：`sha256:bcdd932ff1fa098ee0eed8a7c6d04d2715e2c1ed893fcd306c292e73e1d48cd8`；重新下載 SHA256 完全一致。
- VP validator：`163 checks`，正式部署前與 artifact 重下載後均 `visual_polish=passed`。
- 正式內容版本未因純視覺整理升版；閱讀進度、錯題資料與 storage key 相容，`progress_storage_changed=false`。
- 詳細證據：`docs/books/public-finance/visual_polish.md`。
- 本書已切換至 `public-finance:PUB`。
- 全書庫下一個 Visual Polish target：`money-banking`。
