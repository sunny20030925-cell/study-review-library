# 《總體經濟學》製作狀態

更新日期：2026-07-30

## 正式識別

- Book ID：`macroeconomics`
- 正式內容版本：`2026.07.29-2`
- 正式書庫版本：`2026.07.30-19`
- 目前 stage：`PUB`
- Task ID：`macroeconomics:PUB`
- 下一階段：無；本書新制流程已完成。
- Published：`passed`。
- Internal QA：原兩輪 QA 與發布後第二次獨立內容複核。
- External Audit：`docs/books/macroeconomics/external_audit.md`

## Internal QA 證據

- 正文 20 章、附錄 3 份、題庫 100 題、搜尋索引 143 筆、SVG 20 張。
- 發布後第二次獨立內容複核：201／201；14 個內容修正事件、7 題調整、20 題量化題重算。
- 已補自然失業流量、growth accounting、Taylor principle、CA、PPP 方向與 Mundell–Fleming 模型邊界。

## External Audit

- 結果：`passed`
- 路由：Wolfram + Consensus。
- 抽查 national accounts、unemployment/growth、Solow、saving、multipliers、money/Fisher、debt、Taylor、CA/PPP 與 open-economy assumptions。
- 核心答案錯誤：0；需要升版：否；unresolved blocker：0。

## 相容性

章節／題目 ID、題數、PWA、閱讀進度與錯題資料均未變；正式 21 本 artifact 維持 `2026.07.30-9`。

## Visual Polish 完成（2026-07-30）

- Task：`macroeconomics:VP`；結果：`passed`。
- 高價值資產：`總體經濟學政策模型選擇與方向判斷地圖`。
- Canva design ID：`DAHQ4eP1njs`；可編輯來源：`https://www.canva.com/d/1Mr3R5q87YNMNux`。
- PWA 資產：`assets/macroeconomics-svg/macro-map.svg`；平板可閱讀、可放大、沿用既有離線 cache path。
- 正式 run：`30565088816`；Pages artifact：`8768479929`。
- Artifact digest：`sha256:cbf6c78477020bf8896d1e2a2a42a4a548853fed3e68fb1525bc9d7926523dd7`；重新下載 SHA256 完全一致。
- VP validator：`116 checks`，正式部署前與 artifact 重下載後均 `visual_polish=passed`。
- 正式內容版本未因純視覺整理升版；閱讀進度、錯題資料與 storage key 相容，`progress_storage_changed=false`。
- 詳細證據：`docs/books/macroeconomics/visual_polish.md`。
- 本書已切換至 `macroeconomics:PUB`。
- 全書庫下一個 Visual Polish target：`international-economics`。
