# 《計量經濟學》製作狀態

更新日期：2026-07-29

## 正式識別

- Book ID：`econometrics`
- 目標初版內容版本：`2026.07.29-1`
- 目前狀態：候選內容與兩輪 QA 已完成；正式部署流程 PR #97 已併入 `main`，正以當下 deployment receipt 指定的 Pages artifact 進行最終發布驗證。
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
6. 正式整合已改為動態讀取最新 deployment receipt，不硬編碼既有書數或 shared library 版本；只在正式 artifact 尾端追加 `econometrics`。
7. 整合 QA 會在追加前後對所有既有 `books/**` 做 hash 比對，確認既有教材不變。
8. `app.js`、`sw.js` 語法、chapter／SVG／search／questions／offline cache 路徑都納入正式部署前與部署後重驗。

## 發布前剩餘 gate

- 從當下 deployment receipt 指定的正式 Pages artifact 生成新候選。
- 在該正式基底重跑兩輪 QA 與既有教材 hash 保護。
- Pages 部署後重新下載該 run 的 artifact，核對 digest／SHA-256 與本書 23 份 HTML、100 題、189 搜尋、20 SVG。
- 核實正式 Pages 與 deployment receipt 後，才把本狀態改為「已部署」。

## 發布狀態

目前不提前宣稱已部署；以實際 Pages artifact 與部署證據為準。
