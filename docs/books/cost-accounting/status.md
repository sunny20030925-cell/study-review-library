# 《成本會計學》製作狀態

更新日期：2026-07-30

## 正式識別

- Book ID：`cost-accounting`
- 正式內容版本：`2026.07.29-2`
- 正式書庫版本：`2026.07.30-26`
- 目前 stage：`PUB`
- Task ID：`cost-accounting:PUB`
- 下一階段：無；本書新制流程已完成。
- Published：`passed`。
- Internal QA：`docs/books/cost-accounting/qa_report.md`
- External Audit：`docs/books/cost-accounting/external_audit.md`

## Internal QA 證據

- 正文 19 章、附錄 3 份、題庫 95 題、搜尋索引 150 筆、SVG 19 張。
- 95／95 題重查；44／44 數值答案獨立重算；新版 validator 857／857。
- 已修正 materials flow、CVP 邊界、WA/FIFO process costing、spoilage、by-products、variances、absorption costing normal-capacity 等高風險節點。

## External Audit

- 結果：`passed`
- 路由：正式會計準則／規範 + Wolfram calculation only。
- 抽查 IAS 2 normal-capacity／unallocated overhead 邊界，以及 cost flow、CVP、EUP、ABC、joint cost、variances、absorption/variable costing 計算。
- 核心答案錯誤：0；需要升版：否；unresolved blocker：0。

## 相容性

章節／題目 ID、題數、PWA、閱讀進度與錯題資料均不變；正式 21 本 artifact 維持 `2026.07.30-9`。

## Visual Polish 完成（2026-07-30）

- Task：`cost-accounting:VP`；結果：`passed`。
- 高價值資產：`成本會計學成本流分攤約當產量與差異分析判斷地圖`。
- Canva design ID：`DAHQ5Eq5yIA`；可編輯來源：`https://www.canva.com/d/PfgNzm2JtNHRzyX`。
- PWA 資產：`assets/cost-accounting-svg/cost-map.svg`；平板可閱讀、可放大、沿用既有離線 cache path。
- 正式 run：`30580411658`；Pages artifact：`8774373855`。
- Artifact digest：`sha256:ef983bd8d9f343d2b02a8fc918b058de2a679f325ab7fc27cfa5b8f9f09b44e5`；重新下載 SHA256 完全一致。
- VP validator：`144 checks`，正式部署前與 artifact 重下載後均 `visual_polish=passed`。
- 正式內容版本未因純視覺整理升版；閱讀進度、錯題資料與 storage key 相容，`progress_storage_changed=false`。
- 詳細證據：`docs/books/cost-accounting/visual_polish.md`。
- 本書已切換至 `cost-accounting:PUB`。
- 全書庫下一個 Visual Polish target：`accounting`。
