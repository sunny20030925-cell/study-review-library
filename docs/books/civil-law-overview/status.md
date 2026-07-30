# 《民法概要》製作狀態

更新日期：2026-07-30

## 定位

- Book ID：`civil-law-overview`
- 正式內容版本：`2026.07.30-2`
- 正式書庫版本：`2026.07.30-13`
- 正式分支：`main`
- 目前 stage：`PUB`
- Task ID：`civil-law-overview:PUB`
- 下一階段：無；本書新制流程已完成。
- Published：`passed`。
- 法規基準：2026-07-30 中華民國現行民法、相關施行法與必要憲法裁判。
- 定位：一般大學民法概要，涵蓋總則、債、物權、親屬、繼承五編。

## 成品

- 正文 20 章、附錄 3 份。
- 題庫 100 題，每章 5 題。
- 搜尋索引 150 筆；自製 SVG 20 張。
- 章節 ID、題目 ID 與閱讀／題庫進度儲存鍵未變。

## Internal QA／法律複核

- v2 reaudit：147 項檢查通過；12 組現行法高風險 gate；9 題實際修正。
- 補正第 130 條請求中斷的 6 個月起訴限制、第 300／301 條債務承擔、第 354／360 條買賣瑕疵救濟。
- 補入第 482 條僱傭、第 191-2 條動力車輛責任、第 801／948 條善意取得、第 819／820 條共有處分與管理分工。
- 補強第 1030-1 條剩餘財產分配範圍；補入 112 年憲判字第 4 號在 2025-03-24 修法期限屆滿後的裁判效果。
- 補正第 1174 條拋棄繼承後書面通知義務；明確區分現行第 1223 條兄弟姊妹特留分與 2026-06-02 尚未生效的修正草案。
- External Audit：既有正式法源／判決複核證據遷移為 `passed_migrated`。

## Visual Polish（2026-07-30）

- Task：`civil-law-overview:VP`。
- 結果：`passed`。
- 高價值資產：《民法案例題請求權基礎地圖》。
- Canva design ID：`DAHQ2mt-Yds`；可編輯來源：`https://www.canva.com/d/3hxkdRsJsAWGQB-`。
- PWA 正式資產：`assets/civil-law-overview-svg/civil-map.svg`。
- 使用位置：第 0 章既有民法總覽位置＋附錄 B；附錄 B 可另開 standalone SVG 放大。
- 沿用既有 service-worker cache URL；平板可閱讀、可放大、可離線；SVG 總數仍為 20。
- 高風險圖表法條再次核對現行第 125、179、184、767 條；不改寫教材核心實體法律規則。
- 正式 Actions：VP validator `70 checks`、`visual_polish=passed`，部署前與重新下載 artifact 後各通過一次。
- 未修改正文核心答案或題庫；正式內容版本維持 `2026.07.30-2`。
- Visual Polish 詳細證據：`docs/books/civil-law-overview/visual_polish.md`。

## 最新正式部署

- 正式入口：`https://sunny20030925-cell.github.io/study-review-library/`。
- 修正後 canonical `Deploy study library` run：`30535904702`，success。
- 正式 Visual Polish run：`30536727373`，success。
- 正式部署 source commit：`8043f625dd93c3e2fbf1e118a81a214a6ae917e4`。
- Pages artifact：`8756956130`。
- Artifact digest：`sha256:b84acced62954c3afe1dadfddfdbc8bbe972dab843e38b2cc9e65554b2d9a92f`。
- Artifact download recheck：`passed`；下載 SHA256 與 digest 完全一致。
- 正式書庫：21 本，版本 `2026.07.30-13`。
- 閱讀進度、錯題資料與 storage key 相容；`progress_storage_changed=false`。

## 下一步

本書 `DR → IQ → EA → VP → PUB` 新制流程已完成；全書庫下一個 Visual Polish 任務由 `docs/audit_progress_manifest.json` 的 queue 決定。
