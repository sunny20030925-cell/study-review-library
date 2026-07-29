# 《國際經濟學》製作狀態

更新日期：2026-07-29

## 版本

- Book ID：`international-economics`
- 候選內容版本：`2026.07.29-1`
- 目標書庫版本：依正式發布當下最新 `main` 順延，不預先鎖死舊版本。
- 狀態：內容與兩輪 QA 已完成；canonical 部署封裝已修正，正由最新 `main` 重新執行正式發布驗證。

## 成品與 QA

- 正文 20 章、附錄 3 份、題庫 100 題、搜尋索引 144 筆、自製 SVG 20 張。
- 第一輪製作內檢：696／696 項通過；17 題數值答案重新驗算。
- 第二輪獨立複核：1,383／1,383 項通過；100 題逐題重新檢查，17 題量化題由原始輸入獨立重算。
- 高風險重查：比較利益／所得分配、H–O 定理群、關稅與配額福利、WTO 非歧視原則、國際收支符號、CIP／UIP、PPP、實質匯率、匯率超調、DD–AA、Marshall–Lerner／J 曲線、固定匯率干預、不可能三角與金融危機。
- 已用正式九書 Pages artifact 驗證新增書籍不刪除既有 9 本，並通過 JavaScript、service worker 與靜態路徑檢查。
- 正式部署首次執行由 generator gzip 雜湊閘門擋下；已定位為單一分片內容偏差，修復後改以解壓後 generator source SHA-256 `05c760972b8c444c69c35b6e597ebf2d78241be2ea8e3ad83b1981c5a19f9e2a` 驗證完整性。後續一次 run 因平行教材驗證回寫新 `main` 而被 concurrency 取消，未視為內容失敗。

## 發布邊界

- 共同書庫整合前必須重新讀取最新 `main`、shared checkpoint、registry 與 deployment receipt。
- 若其他科目已先發布，本書必須重做書序／版本整合驗證，不得以目前九書離線副本覆蓋較新的正式書庫。
- 正式部署成功後才可把狀態改為「已部署」，並寫回正式書庫版本、run、source commit 與 receipt。
