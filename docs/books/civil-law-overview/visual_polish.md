# 《民法概要》Visual Polish Record

- Task ID：`civil-law-overview:VP`
- 日期：2026-07-30
- 結果：`passed`
- 正式內容版本：`2026.07.30-2`
- 正式書庫版本：`2026.07.30-13`

## 高價值視覺資產

- 名稱：《民法案例題請求權基礎地圖》
- Canva design ID：`DAHQ2mt-Yds`
- Canva 可編輯來源：`https://www.canva.com/d/3hxkdRsJsAWGQB-`
- PWA 正式資產：`assets/civil-law-overview-svg/civil-map.svg`
- 使用位置：第 0 章既有民法總覽位置＋附錄 B「請求權基礎解題法」。
- 附錄 B 可另開 standalone SVG 放大閱讀。

## 法律精確性

本圖聚焦案例題的請求權基礎判斷，而不改寫教材實體法律規則。高風險法條於製作時再次以現行官方民法核對：

- 第 125 條：一般請求權原則 15 年不行使而消滅；法律另定較短期間者從其規定。
- 第 179 條：無法律上原因受利益，致他人受損害，應返還其利益；法律上原因其後不存在者亦同。
- 第 184 條：故意或過失不法侵害他人權利之一般侵權責任入口，並保留該條其他法定型態的判斷空間。
- 第 767 條：所有人對無權占有／侵奪、妨害及妨害之虞的返還、除去與防止請求。
- 圖中另明示「契約先行」、「債權 ≠ 物權」、「發生／變動／受阻／效果」與法規時點檢查，避免案例題直接跳結論。

## PWA／平板驗證

- 沿用既有 `civil-map.svg` service-worker cache URL，沒有新增第 21 張 SVG。
- SVG 總數：20，維持原正式契約。
- tablet readability：PASS。
- standalone SVG zoom：PASS。
- offline cache：PASS。
- Book ID、20 個 chapter ID、100 個 question ID 均未變。
- 題庫仍為 100 題、搜尋索引仍為 150 筆。
- 所有非民法書籍與非民法資產 hash 在本地 formal-artifact 模擬前後一致。
- 閱讀進度、錯題資料與 storage key 未變；`progress_storage_changed=false`。

## 正式 Actions 證據

- VP 基礎設施 PR：#157；merge SHA `a443017371949e4033c6ba105ec820b7d6ad44fc`。
- 部署前狀態 PR：#158；明確維持 VP pending，未提前切換 PUB。
- canonical run `30535648585` 的 Pages upload／deploy／artifact re-download 已成功，但 generic recorder 因 shared-checkpoint label 契約不一致而失敗；PR #159 以一行修正恢復 recorder label 契約。
- 修正後 canonical run：`30535904702`，success；正式基底 artifact `8756627609`、library `2026.07.30-12`。
- 原 `workflow_run` listener 未留下可驗證 success recorder，因此未把它視為完成。
- 一次性 owner-only fallback PR：#160；Issue #161 觸發後已成功並關閉。
- 正式 Visual Polish run：`30536727373`，job `visual-polish` 全步驟 success。
- 正式 Pages artifact：`8756956130`。
- Artifact digest：`sha256:b84acced62954c3afe1dadfddfdbc8bbe972dab843e38b2cc9e65554b2d9a92f`。
- Artifact re-download SHA256：`b84acced62954c3afe1dadfddfdbc8bbe972dab843e38b2cc9e65554b2d9a92f`，與 digest 完全一致。
- VP validator（部署前）：`70 checks`、`visual_polish=passed`。
- VP validator（重新下載 artifact 後）：再次 `70 checks`、`visual_polish=passed`。
- 正式 artifact：21 本、library `2026.07.30-13`、民法概要 20 章／3 附錄／100 題／150 搜尋／20 SVG。
- Formal recorder commit：`e551da144e169ce4b2b651dca21411a66d105f95`。

## 結論

`civil-law-overview:VP = passed`。正式內容版本不需升版；本書可回到 `civil-law-overview:PUB`。一次性 fallback 與本書專用 `workflow_run` listener 在 closure 中移除，避免後續共同部署持續產生無用觸發。全書庫下一個 Visual Polish target 為 `econometrics`。
