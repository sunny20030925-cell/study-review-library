# 《財政學》製作狀態

更新日期：2026-07-29

## 版本

- Book ID：`public-finance`
- 目前正式內容版本：`2026.07.29-1`
- 目前正式書庫版本：`2026.07.29-14`
- 發布後內容審計候選版本：`2026.07.29-2`
- 候選目標書庫版本：`2026.07.29-15`
- 正式書庫順位：第 11 本。
- 狀態：v2 獨立內容審計、糾錯與 canonical-tail preflight 已通過；尚待正式 Pages 部署，正式網站在部署完成前仍以 v1 為準。

## 成品與相容性

- 正文：20 章（`ch00`–`ch19`）。
- 附錄：3 份。
- 題庫：100 題，每章 5 題。
- 搜尋索引：189 筆。
- 圖解：20 張自製 SVG。
- 章節 ID、題目 ID 與題數均不變；既有閱讀進度與錯題紀錄可沿用。

## v2 發布後獨立內容審計

本輪不沿用初版 QA 結論，重新逐章檢查定義、公式條件、例題與 100 題題庫。主要修正／補強共 16 個內容區域：

1. 補齊 Lindahl 個人化價格與偏好揭露限制。
2. 尋租社會成本改為概念關係，不再呈現成一般會計恆等式。
3. 補社會折現率與公共 CBA 的折現口徑。
4. Gini 0–1 加入非負所得條件；補現金／實物移轉與負所得稅。
5. 修正 funded pension 不等於個人帳戶，明確區分 PAYG／funded 與 DB／DC；補失業保險。
6. 修正 copayment 與 coinsurance 混稱；另列 deductible，比例公式只適用 coinsurance。
7. 補教育 signalling／screening，避免把全部薪資溢酬直接當成生產力因果效果。
8. 補比例／累進／累退稅負定義。
9. 租稅歸宿彈性分攤式明示為競爭市場小稅／局部近似。
10. 精確化 excess burden／DWL、稅收移轉與三角形近似的成立條件。
11. Ramsey inverse-elasticity 明示為特殊情況，不等同一般 Ramsey rule。
12. 勞動供給所得效果補「休閒為正常財」條件；ETI 改以 net-of-tax rate 定義。
13. 補公司稅 debt bias 的條件式概念。
14. 區分週期性財產稅、淨財富稅與財產移轉稅；資本化加入程度參數。
15. matching grant 明定補助率 `m` 的定義，避免不同教材 matching-rate 定義混用。
16. 公債章先給精確離散式 `(r-g)/(1+g)`，再給常用 `r-g` 近似，並補 stock-flow adjustment。

## v2 驗證

- PR：`#73`
- 候選驗證 Run：`30452275674`
- 正式 10 本 pre-public-finance 基底：`2026.07.29-13`
- v2 產生結果：11 本／書庫 `2026.07.29-15`／財政學 `2026.07.29-2`
- 舊結構／題庫／搜尋／SVG gate：2,386 項通過。
- 新 v2 內容 gate：174 項通過。
- 獨立數值重算：38 項；公債精確離散式另行重算。
- 總體經濟學尾端相容 QA：201 項通過。
- 原 10 本教材檔案 SHA-256 前後一致。
- `app.js`、`sw.js` 語法與財政學平板資產路徑均通過。

## 初版正式部署紀錄

- v1 正式部署 run：`30443143611`
- v1 Source commit：`6babc326c5f8ae3ceed363466248c50c51ceecd6`
- v1 Pages artifact：`8720289195`
- v1 Artifact digest：`sha256:4193fede294a374210549df3e71161681e63b654956c1207a38d0f5112803215`
- 初版 Pages 部署成功；舊 post-deploy recorder 在 Pages 成功後因 checkpoint 格式假設失敗，正式回條已另行校正。

## 平板相容性

- 題庫保留正式介面需要的 `bookId`、`chapterTitle`、`topic`、`difficulty`、`source`。
- manifest 保留章節／附錄顯示編號。
- service worker 包含財政學 manifest、題庫、搜尋、23 份章節／附錄與 20 張 SVG。
- 本輪不要求使用者執行任何終端機、Git 或手動部署操作。
