# 《商事法》Visual Polish Record

- Task ID：`commercial-law:VP`
- 日期：2026-07-30
- 結果：`passed`
- 正式內容版本：`2026.07.29-2`
- 正式書庫版本：`2026.07.30-12`

## 高價值視覺資產

- 名稱：《商事法案例題雙軌判斷地圖》
- Canva design ID：`DAHQ2c1bRXE`
- Canva 可編輯來源：`https://www.canva.com/d/tW8J87KlNJIiXkN`
- PWA 正式資產：`assets/commercial-law-svg/law-map.svg`
- 使用位置：第 0 章既有全書法律地圖位置＋附錄 B「案例題解題路線」。
- 附錄 B 可另開 standalone SVG 放大閱讀。

## 法律精確性

本圖以現行官方法規複核後的高風險區別為核心：

- 公司法第 194 條：董事會決議違反法令或章程，繼續持股 1 年以上之股東得請求董事會停止其行為。
- 公司法第 214 條：繼續持股 6 個月以上且持有已發行股份總數 1% 以上之股東，先以書面請求監察人為公司起訴；30 日內不提起時，股東得為公司提起訴訟。
- 證券交易法第 157 條：法定內部人 6 個月內反向交易之短線利益歸入公司；不以實際知悉重大消息為構成要件。
- 證券交易法第 157-1 條：法定主體實際知悉重大消息，消息明確後、未公開前或公開後 18 小時內之受規範交易受禁止。
- 圖中另明示「公開發行 ≠ 上市」，避免公司法與證交法適用主體混淆。

## PWA／平板驗證

- 沿用既有 service-worker cache URL，沒有新增第 19 張 SVG。
- SVG 總數：18，維持原正式契約。
- tablet readability：PASS。
- standalone SVG zoom：PASS。
- offline cache：PASS。
- Book ID、18 個 chapter ID、90 個 question ID 均未變。
- 題庫仍為 90 題、搜尋索引仍為 111 筆。
- 閱讀進度、錯題資料與 storage key 未變；`progress_storage_changed=false`。

## 正式 Actions 證據

- PWA 實作 PR：#154 `Complete commercial law Visual Polish`。
- PR #154 merge SHA：`2261c0f4e638bf516c4b79079a22a1900e5d14ad`。
- 重觸發控制面 PR：#155；其目的只是在 VP listener 已存在於 `main` 後重新啟動 canonical deployment，沒有提前標記 VP passed。
- canonical `Deploy study library` run：`30532630989`，success。
- Visual Polish run：`30532667241`，job `visual-polish` 全步驟 success。
- Pages artifact：`8755330612`。
- Artifact digest：`sha256:202289641e0ae502fa0bd2bbd78f8938c4978c8a5ba04d850d5f8cb12dedac13`。
- Artifact re-download SHA256：`202289641e0ae502fa0bd2bbd78f8938c4978c8a5ba04d850d5f8cb12dedac13`，與 digest 完全一致。
- VP validator（部署前）：`59 checks`、`visual_polish=passed`。
- VP validator（重新下載 artifact 後）：再次 `59 checks`、`visual_polish=passed`。
- 正式 artifact：21 本、library `2026.07.30-12`、商事法 18 章／3 附錄／90 題／111 搜尋／18 SVG。

## 結論

`commercial-law:VP = passed`。正式內容版本不需升版；本書可回到 `commercial-law:PUB`，全書庫下一個 Visual Polish target 為 `civil-law-overview`。
