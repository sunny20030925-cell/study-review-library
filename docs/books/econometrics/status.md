# 《計量經濟學》製作狀態

更新日期：2026-07-29

## 正式識別

- Book ID：`econometrics`
- 目標初版內容版本：`2026.07.29-1`
- 目前狀態：候選內容完成，兩輪 QA 已通過；PR #81 已同步最新 `main` 並進入正式審查，尚未正式發布。
- 範圍文件：`docs/books/econometrics/scope.md`
- QA 報告：`docs/books/econometrics/qa_report.md`

## 候選成品

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
3. 第一輪 `validate_econometrics.py`：384 項檢查通過，另有 29 個數值節點從原始輸入重新計算。
4. 第二輪 `validate_econometrics_v2.py`：675 項獨立檢查通過，含 32 題高風險答案 gate。
5. 高風險概念已覆核：因果與相關、外生性、OVB、Gauss–Markov、robust SE、多重共線性、log 解釋、IV 條件、FE／RE、parallel trends、RDD local effect、spurious regression、prediction vs causality。
6. 候選以正式 deployment receipt 指定的 12 本 Pages artifact 為基底生成；加入 `econometrics` 後為 13 本，候選共享版本由 `2026.07.29-17` 動態順增為 `2026.07.29-18`。
7. 既有 12 本 `books/**` 檔案 hash 在候選生成前後完全相同。
8. `app.js`、`sw.js` 語法檢查通過；chapter／SVG／search／questions／offline cache 路徑全部存在。

## 發布前剩餘 gate

- 重新同步當下最新 `main`、`docs/shared_checkpoint.md`、registry 與 `docs/deployment_receipt.json`。
- 修正／驗證目前 Pages workflow 的 post-deploy recorder，避免「Pages 已部署成功但歷史字串 recorder 失敗」再次出現。
- 在最新共同書庫基底上重新執行兩輪 QA 與既有書籍 hash 保護。
- 核實 canonical Pages artifact、Pages deployment 與新的 deployment receipt。

## 發布狀態

目前不宣稱已部署。正式 Pages run、artifact、deployment receipt 與當下全站書庫版本全部核實後，才改為「已部署」。
