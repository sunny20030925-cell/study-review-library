# 《計量經濟學》製作狀態

更新日期：2026-07-29

## 正式識別

- Book ID：`econometrics`
- 目標初版內容版本：`2026.07.29-1`
- 目前狀態：製作中；scope 已固定，教材來源、題庫、候選驗證與兩輪 QA 尚待完成。
- 範圍文件：`docs/books/econometrics/scope.md`
- QA 報告：`docs/books/econometrics/qa_report.md`

## 目標成品

- 正文：20 章（ch00–ch19）。
- 附錄：3 份。
- 題庫：100 題，每章 5 題。
- 搜尋索引：至少 160 筆。
- 自製 SVG：20 張。
- 平板功能：沿用共同 PWA 的連續閱讀、章節導覽、全文搜尋、題庫、閱讀進度、錯題紀錄與離線快取。

## 本科邊界

- 核心為本科 introductory econometrics，不擴張成研究所計量理論、高維度計量、高階時間序列或軟體操作手冊。
- 迴歸與因果推論嚴格區分；OLS、robust SE、IV、FE、DiD、RDD 的成立條件必須和公式一起出現。
- 與統計學重疊內容只保留本書需要的複習，不把教材改寫成第二本統計學。

## QA 門檻

1. 20 章、3 附錄、100 題與 20 SVG 全部生成。
2. 每章 5 題，題目 ID 唯一且 chapterId 正確。
3. 所有核心公式重新核對，數值題由原始輸入重新計算。
4. 高風險概念至少覆核：因果與相關、外生性、OVB、Gauss–Markov、robust SE、多重共線性、log 解釋、IV 條件、FE／RE、parallel trends、RDD local effect、spurious regression。
5. 候選必須以最新已部署 Pages artifact 作基底生成，並證明既有書籍 hash 不變。
6. 平板端 chapter／SVG／search／questions／offline cache 路徑全部存在。
7. 正式發布前重新同步當下 `main`、shared checkpoint、registry 與 deployment receipt；不得假設本候選建立時的 12 本書仍是最新尾端。

## 發布狀態

目前不宣稱完成或已部署。只有兩輪 QA、共同書庫重新同步、canonical Pages artifact、Pages deployment 與 deployment receipt 全部核實後，才可改為「已部署」。
