# 《計量經濟學》Visual Polish Record

- Task ID：`econometrics:VP`
- 日期：2026-07-30
- 結果：`passed`
- 正式內容版本：`2026.07.30-1`
- 正式書庫版本：`2026.07.30-14`

## 高價值視覺資產

- 名稱：《計量經濟學｜因果識別方法選擇地圖》
- Canva design ID：`DAHQ2ztIet0`
- Canva 可編輯來源：`https://www.canva.com/d/qDaRkhTIyinoAfS`
- PWA 正式資產：`assets/econometrics-svg/econometrics-map.svg`
- 使用位置：第 0 章既有全書地圖位置＋附錄 B「計量經濟學解題路線」。
- 第 0 章與附錄 B 均可另開 standalone SVG 放大閱讀。

## 內容與方法論邊界

本圖聚焦「估計」與「識別」的區分，不改寫教材核心公式或題庫答案。高風險節點沿用已通過的 Internal QA 與 External Audit 結論：

- 描述／預測與因果問題先分流；預測準確不代表因果成立。
- RCT：random assignment 支持樣本內部因果比較；SATE 外推至 PATE 仍需代表性、外部效度或 transportability 條件。
- FE／FD：可消除 time-invariant individual effect，但標準靜態 panel 仍需適當 strict exogeneity；time-varying confounding 或 lagged outcome 仍可能破壞因果解讀。
- IV／2SLS：relevance 與 exclusion／exogeneity 必須分開；強 first stage 不足以證明 instrument 有效。
- DiD：parallel trends 是核心識別條件；處置前係數不顯著不能被寫成「已證明」平行趨勢。
- RDD：cutoff 周圍的局部比較識別 local effect，不能無條件外推至所有樣本。
- robust SE 修正推論，不修正內生性；顯著、高 R²、預測較準都不能單獨建立因果。

## PWA／平板驗證

- 沿用既有 `econometrics-map.svg` service-worker cache URL，沒有新增第 21 張 SVG。
- SVG 總數：20，維持原正式契約。
- tablet readability：PASS。
- standalone SVG zoom：PASS。
- offline cache：PASS。
- Book ID、20 個 chapter ID、100 個 question ID 均未變。
- 題庫仍為 100 題、搜尋索引仍為 189 筆。
- 本地 formal-artifact 模擬：library `2026.07.30-13 → 2026.07.30-14`；第二次套用維持 `-14`。
- 所有非計量書籍與非計量資產 hash 在套用前後一致。
- 閱讀進度、錯題資料與 storage key 未變；`progress_storage_changed=false`。

## 正式 Actions 證據

- 實作／共用 runner PR：#163；merge SHA `b46770756b829751169bf6f5baecb2fef67eae61`。
- 共用 owner-triggered Visual Polish runner 第一次正式執行：Issue #164。
- 正式 run：`30538616335`，job `visual-polish` 全步驟 success。
- 正式 Pages artifact：`8757716872`。
- Artifact digest：`sha256:3eb406b951a827c182c7e745479fa2a7b4c9647dcfc0fb6dcac05a7d09fe3df1`。
- Artifact re-download SHA256：`3eb406b951a827c182c7e745479fa2a7b4c9647dcfc0fb6dcac05a7d09fe3df1`，與 digest 完全一致。
- VP validator（部署前）：`76 checks`、`visual_polish=passed`。
- VP validator（重新下載 artifact 後）：再次 `76 checks`、`visual_polish=passed`。
- 正式 artifact：21 本、library `2026.07.30-14`、計量經濟學 20 章／3 附錄／100 題／189 搜尋／20 SVG。
- Formal recorder commit：`b94aa69257ddcd1bb1e91556d6c4643ee82571bb`。

## 結論

`econometrics:VP = passed`。正式內容版本不需升版；本書回到 `econometrics:PUB`。全書庫下一個 Visual Polish target 為 `investments`。
