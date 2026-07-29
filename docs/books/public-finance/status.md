# 《財政學》製作狀態

更新日期：2026-07-29

## 版本

- Book ID：`public-finance`
- 正式內容版本：`2026.07.29-2`
- 最新正式書庫版本：`2026.07.29-16`
- 正式書庫順位：第 11 本。
- 狀態：發布後獨立內容審計、糾錯、完整驗證與正式 Pages 部署均已完成。

## 成品與相容性

- 正文：20 章（`ch00`–`ch19`）。
- 附錄：3 份。
- 題庫：100 題，每章 5 題。
- 搜尋索引：189 筆。
- 圖解：20 張自製 SVG。
- 章節 ID、題目 ID 與題數均不變；既有閱讀進度與錯題紀錄可沿用。

## v2 發布後獨立內容審計

本輪不沿用初版 QA 結論，重新逐章檢查定義、公式條件、例題與 100 題題庫。主要修正／補強 16 個內容區域：

1. 補齊 Lindahl 個人化價格與偏好揭露限制。
2. 尋租成本改為概念關係，避免誤作一般會計恆等式。
3. 補社會折現率與公共 CBA 折現口徑。
4. Gini 0–1 加入非負所得條件；補現金／實物移轉、負所得稅。
5. 修正 funded pension 不等於個人帳戶；區分 PAYG／funded 與 DB／DC，並補失業保險。
6. 修正 copayment／coinsurance 混稱，另列 deductible；比例公式只適用 coinsurance。
7. 補教育 signalling／screening，避免把全部薪資溢酬直接當生產力因果效果。
8. 補比例／累進／累退稅負定義。
9. 租稅歸宿彈性分攤式明示為競爭市場小稅／局部近似。
10. 精確化 excess burden／DWL、稅收移轉與三角形近似成立條件。
11. Ramsey inverse-elasticity 明示為特殊情況，不等同一般 Ramsey rule。
12. 勞動供給所得效果補「休閒為正常財」條件；ETI 改以 net-of-tax rate 定義。
13. 補公司稅 debt bias 的條件式概念。
14. 區分週期性財產稅、淨財富稅與財產移轉稅；資本化加入程度參數。
15. matching grant 明定補助率 `m` 的定義。
16. 公債章先給精確離散式 `(r-g)/(1+g)`，再給常用 `r-g` 近似，並補 stock-flow adjustment。

## 驗證與部署

- PR：`#73`
- 最新 PR 驗證 Run：`30452510166`，成功。
- 舊結構／題庫／搜尋／SVG gate：2,386 項通過。
- 新 v2 內容 gate：174 項通過。
- 獨立數值重算：38 項；公債精確離散式另行重算。
- 原 10 本教材檔案 SHA-256 前後一致。
- 財政學專屬正式 Pages run：`30452624395`，Upload／Deploy 均成功。
- 隨後《國際經濟學》v2 序列發布形成目前最新正式 Pages run：`30452678302`；該 run 重新生成並驗證財政學 v2，Pages 再次成功。
- 最新正式 source commit：`24bcf00d73dcb2e11b4d2dfbce14c5e99b5db85d`。
- 最新 Pages artifact：`8724164394`。
- Artifact digest：`sha256:282d2bdeec05a04427dd13a5c50aa1fcce172011fff4c1403fd563c4cfc1b201`。
- 最新 artifact 已重新下載驗證：11 本、書庫 `2026.07.29-16`；財政學 `2026.07.29-2`、20 章＋3 附錄、100 題、189 搜尋、20 SVG 均存在。

## 平板相容性

- 題庫保留 `bookId`、`chapterTitle`、`topic`、`difficulty`、`source`。
- manifest 保留章節／附錄顯示編號。
- service worker 已切換至 `study-library-2026.07.29-16` 並包含財政學全部離線資產。
- 本輪沒有要求使用者執行終端機、Git 或手動部署操作。

## 已知工程技債

canonical workflow 的最後 `Record successful deployment` 仍依賴舊 checkpoint 標題／句子格式，所以最新 run 在 Pages 已成功後才於文件寫回步驟失敗。此問題不影響正式網站或 artifact；deployment receipt 已依最新 artifact 與 deploy log 以 `[skip ci]` 校正。下一本正式新教材發布前仍應修正 recorder。
