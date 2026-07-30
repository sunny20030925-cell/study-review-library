# 《民法概要》製作狀態

更新日期：2026-07-30

## 定位

- Book ID：`civil-law-overview`
- 正式內容版本：`2026.07.30-2`
- 正式書庫版本：`2026.07.30-12`
- 正式分支：`main`
- 目前 stage：`VP`
- Task ID：`civil-law-overview:VP`
- 下一階段：`PUB`
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

## Visual Polish 執行中（2026-07-30）

- Task：`civil-law-overview:VP`。
- 已核准並正式儲存 Canva 高價值資產：《民法案例題請求權基礎地圖》。
- Canva design ID：`DAHQ2mt-Yds`；可編輯來源：`https://www.canva.com/d/3hxkdRsJsAWGQB-`。
- VP 基礎設施 PR：#157；merge SHA `a443017371949e4033c6ba105ec820b7d6ad44fc`。
- 預定正式資產：`assets/civil-law-overview-svg/civil-map.svg`；沿用既有 service-worker cache URL，SVG 總數維持 20。
- 使用位置：第 0 章既有民法總覽位置＋附錄 B；附錄 B 提供 standalone SVG 放大入口。
- 本地正式 artifact 模擬：library `2026.07.30-12 → 2026.07.30-13`；第二次套用維持 `-13`；VP validator `70 checks` PASS。
- 20 章、3 附錄、100 題、150 搜尋、20 SVG 與所有 chapter／question IDs 均維持不變；所有非民法書籍與資產 hash 不變。
- 高風險圖表法條已以現行法再次核對：第 125 條一般 15 年時效、第 179 條不當得利、第 184 條侵權、第 767 條所有權物上請求權。
- 本節只是部署前中間節點；正式 follow-up Pages artifact 尚未產生，因此 **VP 仍為 pending，不得提前切換 PUB**。

## 正式入口

- GitHub Pages：`https://sunny20030925-cell.github.io/study-review-library/`。
- 最新正式書庫基底：21 本、library `2026.07.30-12`。
- `progress_storage_changed=false`。

## 下一步

等待本次 main push 的 canonical `Deploy study library` 完成；其成功事件將由已存在於 `main` 的 `Apply civil law overview Visual Polish` workflow 接手。只有 follow-up artifact 上傳、Pages 部署、重新下載 digest 驗證與 70-check VP QA 全部通過後，才可正式記錄 `civil-law-overview:VP = passed` 並切換至 `civil-law-overview:PUB`。
