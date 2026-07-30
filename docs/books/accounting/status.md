# 《會計學》製作狀態

更新日期：2026-07-30

## 正式識別

- Book ID：`accounting`
- 正式內容版本：`2026.07.27-2`
- 正式書庫版本：`2026.07.30-27`
- 目前 stage：`PUB`
- Task ID：`accounting:PUB`
- 下一階段：無；本書新制流程已完成。
- Published：`passed`。
- Internal QA：既有第二版獨立複核；詳細證據保留於本書 QA 文件與部署紀錄。
- External Audit：`docs/books/accounting/external_audit.md`

## Internal QA 證據

- 正文 14 章、附錄 3 份、題庫 70 題、搜尋索引 111 筆、SVG 13 張。
- 70／70 題數值答案重新驗算；29 個內容點修正；4 題補正題意／條件／詳解。
- 科目邊界維持基礎財務會計，不納入中級會計、成本會計或管理會計。

## External Audit

- 結果：`passed`
- 路由：正式財務報導準則／臺灣正式規範；Wolfram 僅計算驗證。
- 抽查 financial statement elements、inventory、depreciation、cash-flow classification、基礎認列與 IFRS 18 臺灣過渡時程。
- 核心答案錯誤：0；需要升版：否；unresolved blocker：0。

## 相容性

章節／題目 ID、題數、PWA、閱讀進度與錯題資料均不變；正式 21 本 artifact 維持 `2026.07.30-9`。

## Visual Polish 完成（2026-07-30）

- Task：`accounting:VP`；結果：`passed`。
- 高價值資產：`會計學交易調整報表與現金流判斷地圖`。
- Canva design ID：`DAHQ5G-UZ3g`；可編輯來源：`https://www.canva.com/d/__AMHur-jvd7l6c`。
- PWA 資產：`assets/accounting-svg/accounting-map.svg`；平板可閱讀、可放大、沿用既有離線 cache path。
- 正式 run：`30580853942`；Pages artifact：`8774541538`。
- Artifact digest：`sha256:99de1677740e7b4693ff211756aad15a10ee853567198e55479fb70a8363e106`；重新下載 SHA256 完全一致。
- VP validator：`102 checks`，正式部署前與 artifact 重下載後均 `visual_polish=passed`。
- 正式內容版本未因純視覺整理升版；閱讀進度、錯題資料與 storage key 相容，`progress_storage_changed=false`。
- 詳細證據：`docs/books/accounting/visual_polish.md`。
- 本書已切換至 `accounting:PUB`。
- 全書庫下一個 Visual Polish target：`economics`。
