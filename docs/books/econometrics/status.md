# 《計量經濟學》製作狀態

更新日期：2026-07-30

## 正式識別

- Book ID：`econometrics`
- 正式內容版本：`2026.07.30-1`
- 正式書庫版本：`2026.07.30-6`
- 狀態：已部署。
- 範圍文件：`docs/books/econometrics/scope.md`
- QA 報告：`docs/books/econometrics/qa_report.md`

## 正式成品

- 正文：20 章（ch00–ch19）。
- 附錄：3 份。
- 題庫：100 題，每章 5 題。
- 搜尋索引：189 筆。
- 自製 SVG：20 張。
- 章節 ID、題目 ID、題數與儲存鍵均未改動；既有閱讀進度與錯題紀錄相容。

## QA 與發布後獨立審計

- 初版第一輪 QA：384 項，29 個數值節點獨立重算。
- 初版第二輪 QA：675 項，32 題高風險答案 gate。
- 2026-07-30 發布後獨立內容審計：修正 2 個精確性缺口，reaudit validator 共 57 項通過。
- 修正一：Panel FE／FD 明列標準靜態模型的 strict-exogeneity 條件；不再讓「消掉 alpha_i」被誤讀成已充分解決所有時間變動內生性。
- 修正二：隨機實驗明確區分 SATE 與 PATE；random assignment 建立實驗單位內部因果識別，但外推更大母體仍需要 sampling／external-validity 條件。
- 其他高風險章節與既有 100 題 ID 全部保持相容。

## 正式發布證據

- canonical workflow：`Deploy study library`
- workflow run：`30490197263`
- source commit：`92506854f20bc7caa8a77b2e9774f2be11fbb9be`
- Pages artifact：`8739358772`
- Artifact digest：`sha256:6936173acc641daef1c2e369a09407f2ee4533499735b78f5cbb280a147440ce`
- 正式書庫：20 本，版本 `2026.07.30-6`。
- Pages deployment、artifact 下載後重驗與 deployment receipt 均成功。
