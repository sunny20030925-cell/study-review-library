# 《計量經濟學》製作狀態

更新日期：2026-07-30

## 正式識別

- Book ID：`econometrics`
- 正式內容版本：`2026.07.30-1`
- 正式書庫版本：`2026.07.30-14`
- 目前 stage：`PUB`
- Task ID：`econometrics:PUB`
- 下一階段：無；本書新制流程已完成。
- Published：`passed`。
- 範圍：`docs/books/econometrics/scope.md`
- Internal QA：`docs/books/econometrics/qa_report.md`
- External Audit：`docs/books/econometrics/external_audit.md`

## Internal QA 證據

- 初版第一輪 QA：384 項；29 個數值節點獨立重算。
- 初版第二輪 QA：675 項；32 題高風險答案 gate。
- 發布後獨立內容審計 validator：57 項通過；已補 strict exogeneity 與 SATE/PATE 邊界。
- 正文 20 章、附錄 3 份、題庫 100 題、搜尋索引與 20 張 SVG 均已正式部署。

## External Audit

- 結果：`passed`
- 路由：Wolfram + Consensus。
- 高風險抽查：OLS／robust SE／OVB、time series、IV、RCT、DiD、RDD、prediction 與因果識別條件。
- 核心答案錯誤：0；需要升版：否；unresolved blocker：0。

## 相容性與部署

- Book ID、chapter ID、question ID、題數、閱讀進度與錯題資料均不變。
- 正式 21 本 Pages artifact 維持 `2026.07.30-9`；本輪純狀態寫回不重新部署教材。

## Visual Polish 完成（2026-07-30）

- Task：`econometrics:VP`；結果：`passed`。
- 高價值資產：`計量經濟學因果識別方法選擇地圖`。
- Canva design ID：`DAHQ2ztIet0`；可編輯來源：`https://www.canva.com/d/qDaRkhTIyinoAfS`。
- PWA 資產：`assets/econometrics-svg/econometrics-map.svg`；平板可閱讀、可放大、沿用既有離線 cache path。
- 正式 run：`30538616335`；Pages artifact：`8757716872`。
- Artifact digest：`sha256:3eb406b951a827c182c7e745479fa2a7b4c9647dcfc0fb6dcac05a7d09fe3df1`；重新下載 SHA256 完全一致。
- VP validator：`76 checks`，正式部署前與 artifact 重下載後均 `visual_polish=passed`。
- 正式內容版本未因純視覺整理升版；閱讀進度、錯題資料與 storage key 相容，`progress_storage_changed=false`。
- 詳細證據：`docs/books/econometrics/visual_polish.md`。
- 本書已切換至 `econometrics:PUB`。
- 全書庫下一個 Visual Polish target：`investments`。
