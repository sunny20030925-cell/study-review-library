# 大一微積分 Status

更新日期：2026-07-30

## 正式識別

- Book ID：`calculus`
- 正式內容版本：`2026.07.27-3`
- 正式書庫版本：`2026.07.30-30`
- 目前 stage：`PUB`
- Task ID：`calculus:PUB`
- 下一階段：無；本書新制流程已完成。
- Published：`passed`。
- Internal QA：`docs/books/calculus/qa_report.md`
- External Audit：`docs/books/calculus/external_audit.md`

## Internal QA 證據

- 標準大一微積分正文 14 章；題庫 73 題；搜尋索引 150 筆。
- 本版 QA：181／181；公式、章節、題庫、圖片、JSON、JavaScript、內容版本與 PWA cache 一致性均通過。
- 經濟學取向內容已移除，維持純微積分科目本位。

## External Audit

- 結果：`passed`
- 路由：Wolfram。
- 抽查 domain、limits、derivatives、implicit differentiation、MVT/L'Hôpital、integrals、geometry applications、exp/log、series、multivariable calculus、constrained optimization 與 ODE。
- 代表性 73 題掃描與形式化重算未發現核心錯誤。
- 核心答案錯誤：0；需要升版：否；unresolved blocker：0。

## 相容性

章節／題目 ID、題數、PWA、閱讀進度與錯題資料均不變；正式 21 本 artifact 現為 `2026.07.30-30`。

## Visual Polish 完成（2026-07-30）

- Task：`calculus:VP`；結果：`passed`。
- 高價值資產：`大一微積分極限導數積分級數與多變數判斷地圖`。
- Canva design ID：`DAHQ5AiFZNo`；可編輯來源：`https://www.canva.com/d/J7WcMqzKE9zH_Cf`。
- PWA 資產：`assets/calculus-svg/calculus-map.svg`；平板可閱讀、可放大；本輪新增專用 SVG，並納入既有 service-worker 離線 cache。
- 正式 run：`30587649125`；Pages artifact：`8777119969`。
- Artifact digest：`sha256:79ac8ec575c1bd401c69d2933368fe4d3d89700f482c3097c17905cc771e912c`；重新下載 SHA256 完全一致。
- VP validator：`62 checks`，正式部署前與 artifact 重下載後均 `visual_polish=passed`。
- 正式內容版本未因純視覺整理升版；閱讀進度、錯題資料與 storage key 相容，`progress_storage_changed=false`。
- 詳細證據：`docs/books/calculus/visual_polish.md`。
- 本書已切換至 `calculus:PUB`。
- 全書庫 Visual Polish queue 已清空。
