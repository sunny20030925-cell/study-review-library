# 《賽局理論及應用》製作狀態

更新日期：2026-07-30

## 正式識別

- Book ID：`game-theory`
- 正式內容版本：`2026.07.30-2`
- 正式書庫版本：`2026.07.30-8`
- 正式書庫書籍數：20 本。
- 狀態：v2 已部署。
- 範圍文件：`docs/books/game-theory/scope.md`
- 初版 QA：`docs/books/game-theory/qa_report.md`
- v2 重審報告：`docs/books/game-theory/v2_audit_report.md`

## v2 內容重審

- 正文 20 章、附錄 3 份、題庫 100 題、搜尋索引 189 筆、自製 SVG 20 張。
- v2 artifact audit：504 項；21 個數值節點獨立重算、19 個高風險概念重判。
- v2 source second pass：375 項；24 個數值節點獨立重算、23 個概念重判。
- 修正 complete／perfect information、混合策略例題、rationalizability、Bertrand、subgame、Bayesian dynamic boundary、second-price assumptions、PBE／signaling、Rubinstein、VCG 與 strategic complements 等精度問題。
- Book ID、章節 ID、附錄 ID 與 100 個題目 ID 全部保留；閱讀進度與錯題紀錄相容。
- 正式 release helper 已驗證除 game-theory 外所有書籍、其他 assets 與 shared `app.js` 未被修改。

## 部署

- canonical workflow：`Deploy study library`
- workflow run：`30493853637`
- source commit：`d6a83769482eb2fcfc9fcf93a08aa037b4abdddd`
- Pages artifact：`8740798612`
- Artifact digest：`sha256:c863a5421710c55696d1b62492d4dfb2d8ed2ecc2f15b37137efd03e1f9e7f94`
- 部署後重新下載 artifact 並再次執行 v2 artifact QA：PASS。
