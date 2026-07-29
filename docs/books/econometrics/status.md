# 《計量經濟學》製作狀態

更新日期：2026-07-29

## 正式識別

- Book ID：`econometrics`
- 正式內容版本：`2026.07.29-1`
- 目前狀態：已完成候選內容、兩輪 QA、正式 Pages 部署與部署後 artifact 重驗；目前正式書庫仍包含本書。
- 範圍文件：`docs/books/econometrics/scope.md`
- QA 報告：`docs/books/econometrics/qa_report.md`

## 正式成品

- 正文：20 章（ch00–ch19）。
- 附錄：3 份。
- 題庫：100 題，每章 5 題。
- 搜尋索引：189 筆。
- 自製 SVG：20 張。
- 平板功能：沿用共同 PWA 的連續閱讀、章節導覽、全文搜尋、題庫、閱讀進度、錯題紀錄與離線快取。

## 本科邊界

- 核心為本科 introductory econometrics，不擴張成研究所計量理論、高維度計量、高階時間序列或軟體操作手冊。
- 迴歸與因果推論嚴格區分；OLS、robust SE、IV、FE、DiD、RDD 的成立條件必須和公式一起出現。
- 與統計學重疊內容只保留本書需要的複習，不把教材改寫成第二本統計學。

## 已通過 QA

1. 20 章、3 附錄、100 題與 20 SVG 全部生成。
2. 每章 5 題，題目 ID 唯一且 chapterId 正確。
3. 候選第一輪 `validate_econometrics.py`：384 項檢查通過，另有 29 個數值節點從原始輸入重新計算。
4. 第二輪 `validate_econometrics_v2.py`：675 項獨立檢查通過，含 32 題高風險答案 gate。
5. 高風險概念已覆核：因果與相關、外生性、OVB、Gauss–Markov、robust SE、多重共線性、log 解釋、IV 條件、FE／RE、parallel trends、RDD local effect、spurious regression、prediction vs causality。
6. 正式整合動態讀取當下 deployment receipt，只在正式 artifact 尾端追加 `econometrics`；加入前為 17 本／`2026.07.29-22`，加入後為 18 本／`2026.07.29-23`。
7. 正式部署前重跑：Round 1 = 384、Round 2 = 675；部署後下載 artifact 再驗：Round 1 = 382、Round 2 = 675，29 個數值重算與 32 個高風險答案 gate 仍通過。
8. 整合前後對既有教材做 hash 保護；`app.js`、`sw.js`、chapter／SVG／search／questions／offline cache 路徑均通過正式部署前與部署後驗證。

## 正式發布證據

- 正式 Pages run：`30471586965`。
- Source commit：`4bdca45ab4772982a812017b34984aff19a9a6c1`。
- Pages artifact：`8731859754`。
- Artifact digest／下載 SHA-256：`sha256:f53bf4979a85a0ff96e9e253cad04f97d37062d368195a97ce4189f8e934edf5`。
- 部署後重驗：`DEPLOYED_ARTIFACT_RECHECK_OK 2026.07.29-23 18`。
- 部署證明：18 本、shared library `2026.07.29-23`，Page URL 為正式固定入口。
- 後續《產業經濟學》發布後，最新正式書庫已成為 19 本／`2026.07.29-24`；正式 registry 仍包含 `econometrics`，位置在 `investments` 與 `industrial-economics` 之間。
- 閱讀進度與錯題儲存結構未改動。

## 發布狀態

已部署。PR #97 已併入 `main`；正式 Pages artifact、部署後下載重驗與後續 19 本正式 registry 均已核實。本文件先前停留在「最終發布驗證中」是 post-deploy 文件回寫漏項，現已依實際部署證據校正。