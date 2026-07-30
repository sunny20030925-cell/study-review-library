# 《中級會計學》製作狀態

更新日期：2026-07-30

## 正式識別

- Book ID：`intermediate-accounting`
- 正式內容版本：`2026.07.29-2`
- 正式書庫版本：`2026.07.30-25`
- 目前 stage：`PUB`
- Task ID：`intermediate-accounting:PUB`
- 下一階段：無；本書新制流程已完成。
- Published：`passed`。
- Internal QA：`docs/books/intermediate-accounting/qa_report.md`
- External Audit：`docs/books/intermediate-accounting/external_audit.md`

## Internal QA 證據

- 正文 22 章、附錄 3 份、題庫 110 題、搜尋索引 145 筆、SVG 22 張。
- 初版 QA：135 項、23 項數值／公式重算、第二輪 485 項；v2 部署驗證 1,110 項＋28 項量化重算。

## External Audit

- 結果：`passed`
- 路由：IFRS／IAS 正式準則與臺灣正式規範；Wolfram 僅計算驗證。
- 抽查 ECL、inventory/NRV、PPE、impairment、provisions、EPS、revenue、leases、deferred tax、employee benefits、cash flows 與 IFRS 18 過渡時程。
- 核心答案錯誤：0；需要升版：否；unresolved blocker：0。

## 相容性

章節／題目 ID、題數、PWA、閱讀進度與錯題資料均不變；正式 21 本 artifact 維持 `2026.07.30-25`。

## Visual Polish 完成（2026-07-30）

- Task：`intermediate-accounting:VP`；結果：`passed`。
- 高價值資產：`中級會計學認列衡量後續處理與表達判斷地圖`。
- Canva design ID：`DAHQ41pBkpo`；可編輯來源：`https://www.canva.com/d/RwAvCpLNxeqkcjn`。
- PWA 資產：`assets/intermediate-accounting-svg/ch00.svg`；平板可閱讀、可放大、沿用既有離線 cache path。
- 正式 run：`30577166991`；Pages artifact：`8773152372`。
- Artifact digest：`sha256:7542adb3551d8ac7a6b1bec3fd48f55151aa5b8686dc9bef32af984573465133`；重新下載 SHA256 完全一致。
- VP validator：`161 checks`，正式部署前與 artifact 重下載後均 `visual_polish=passed`。
- 正式內容版本未因純視覺整理升版；閱讀進度、錯題資料與 storage key 相容，`progress_storage_changed=false`。
- 詳細證據：`docs/books/intermediate-accounting/visual_polish.md`。
- 本書已切換至 `intermediate-accounting:PUB`。
- 全書庫下一個 Visual Polish target：`cost-accounting`。
