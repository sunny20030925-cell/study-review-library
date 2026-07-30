# 《高等統計學》Visual Polish Record

- Task ID：`advanced-statistics:VP`
- 日期：2026-07-30
- 結果：`passed`
- 正式內容版本：`2026.07.30-1`
- 正式書庫版本：`2026.07.30-10`

## 高價值視覺資產

- 名稱：《高等統計推論路線圖》
- 類型：公式／考前速查＋推論流程圖。
- Canva 可編輯來源：design ID `DAHQ1ZXj2QA`
- Canva 編輯連結：`https://www.canva.com/d/JJGioLQiGpjgePs`
- PWA 正式向量資產：`assets/advanced-statistics-svg/math-bridge.svg`
- PWA 使用位置：第 0 章既有解題地圖位置＋附錄 B《高等統計解題路線》。

## 視覺內容

路線圖把高等統計核心推論濃縮成四區：

1. 建模與抽樣：PMF／PDF、support、joint／marginal／conditional、Jacobian，以及 LLN、CLT、Slutsky、Delta method。
2. 點估計與估計量品質：MoM、MLE、bias／variance／MSE、consistency、asymptotic normality、Fisher information／CRLB。
3. 檢定理論：size、power、Neyman–Pearson、UMP／MLR、LRT、p-value 與 Wilks。
4. 線性模型與最後檢查：Gauss–Markov、BLUE、精確小樣本 t／F 的常態條件，以及 Exact／Asymptotic 的作答順序。

Canva 初始候選曾出現無教材價值的「模型數量／極限定理數量」內容，正式版本已移除並改成上述考試判斷點。

## 平板與 PWA 相容性

- 使用既有 `math-bridge.svg` 路徑，不增加新的 service-worker cache URL。
- 高等統計 SVG 總數仍為 20。
- 附錄 B 的圖可點開 standalone SVG，大圖可在平板瀏覽器縮放閱讀。
- 既有 service worker 已快取同一路徑，因此離線載入能力保留。
- Book ID、chapter IDs `ch00`–`ch19`、100 個 question IDs、題數、閱讀進度與錯題 storage key 均未變更。
- 正式內容版本不需升級；共同 PWA 為快取失效與視覺資產更新升至 `2026.07.30-10`。

## 正式驗證

- workflow：`Deploy study library`
- run：`30519227208`
- source commit：`d9f1d3695f78e327f733af742f56e4326bceaa41`
- Pages artifact：`8750076767`
- artifact digest：`sha256:fb988b14e7208c29e123804057b8b60102a50e7d73ca8dc61d817e4593db872f`
- artifact download recheck：`passed`
- artifact verified book count：21
- 高等統計結構：20 章、3 附錄、100 題、189 搜尋、20 SVG。
- GitHub Actions validator：`1072 checks`、`20 numerical_rechecks`、`visual_polish=passed`。
- 部署後重新下載 artifact 再次執行同一高等統計 VP gate：通過。

## 結論

- Visual Polish：`passed`
- unresolved blocker：0
- content version change required：false
- PWA／progress compatibility：preserved
- 下一階段：`PUB`
