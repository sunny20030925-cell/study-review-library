# 《財政學》製作狀態

更新日期：2026-07-29

## 版本

- Book ID：`public-finance`
- 正式內容版本：`2026.07.29-1`
- 正式書庫版本：`2026.07.29-14`
- 正式書庫順位：第 11 本。
- 狀態：已部署。

## 成品與 QA

- 正文：20 章（`ch00`–`ch19`）。
- 附錄：3 份。
- 題庫：100 題，每章 5 題。
- 搜尋索引：189 筆。
- 圖解：20 張自製 SVG。
- 第一輪製作內檢完成。
- 第二輪獨立內容與題庫複核完成；20／20 章與 100／100 題重新檢查。
- 固定重查 40 個高風險答案；數值題由原始輸入重新計算。
- 最新正式 10 書 artifact 上的 canonical-tail preflight：Run `30443068402`，成功生成 11 書／`2026.07.29-14`，原 10 本教材雜湊不變。
- 正式財政學 validator：2,383 項檢查通過；20 章、3 附錄、100 題、189 搜尋索引、20 SVG 全部通過。

## 科目邊界

- 採一般大學財政學／公共經濟學本位。
- 核心主線：公共支出與市場失靈、分配與社會保險、租稅理論與主要稅目、地方財政與政府債務。
- 不把《總體經濟學》的 IS–LM、AD–AS、景氣穩定政策擴張成財政學正文。
- 不把會隨年度修法變動的臺灣稅率、扣除額與申報門檻寫成固定核心知識。

## 正式部署

- canonical workflow：`Deploy study library`
- 正式部署 run：`30443143611`
- Source commit：`6babc326c5f8ae3ceed363466248c50c51ceecd6`
- Pages artifact：`8720289195`
- Artifact digest：`sha256:4193fede294a374210549df3e71161681e63b654956c1207a38d0f5112803215`
- GitHub Pages 的 Upload 與 Deploy 步驟均成功；Pages 在 `2026-07-29T10:18:44.896999+00:00` 回報成功。
- 實際部署 artifact 已重新下載驗證：11 本、書庫版本 `2026.07.29-14`，尾端順序為 `macroeconomics` → `international-economics` → `public-finance`。
- 該 run 的最後「Record successful deployment」步驟因舊寫回器仍假設舊 checkpoint 標題格式而失敗；此錯誤發生在 Pages 成功之後，不影響已部署網站內容。正式 deployment receipt 已依 Pages artifact 與部署 log 以 `[skip ci]` 校正，並保留這個工程瑕疵紀錄。

## 平板相容性

- 題庫已包含正式介面需要的 `bookId`、`chapterTitle`、`topic`、`difficulty`、`source`。
- manifest 已包含章節／附錄顯示編號。
- service worker 已包含財政學 manifest、題庫、搜尋、23 份章節／附錄與 20 張 SVG。
- 原有 10 本教材檔案在正式 preflight 前後雜湊完全一致；沒有要求使用者執行任何終端機、Git 或手動部署操作。
