# 《國際經濟學》製作狀態

更新日期：2026-07-29

## 版本

- Book ID：`international-economics`
- 正式內容版本：`2026.07.29-1`
- 正式書庫版本：`2026.07.29-13`
- 狀態：已部署。
- GitHub Pages 部署 run：`30442682452`。
- Source commit：`00cf9286eb7bbe3b2d8e2b6165cc163fd64a4e72`。
- 部署回條：`docs/deployment_receipt.json`。

## 成品與 QA

- 正文 20 章、附錄 3 份、題庫 100 題、搜尋索引 144 筆、自製 SVG 20 張。
- 第一輪製作內檢：696／696 項通過；17 題數值答案重新驗算。
- 第二輪獨立複核：1,383／1,383 項通過；100 題逐題重新檢查，17 題量化題由原始輸入獨立重算。
- 高風險重查：比較利益／所得分配、H–O 定理群、關稅與配額福利、WTO 非歧視原則、國際收支符號、CIP／UIP、PPP、實質匯率、匯率超調、DD–AA、Marshall–Lerner／J 曲線、固定匯率干預、不可能三角與金融危機。
- 正式 Pages artifact 終檢：書庫 10 本；本書 23 份章節／附錄檔、100 題、144 筆搜尋、20 張 SVG 全部存在；manifest 內容版本為 `2026.07.29-1`，service worker 已納入本書離線快取。
- 部署回條確認 `progress_storage_changed=false`，既有閱讀進度／錯題儲存結構未變。

## 部署紀錄

- 首次正式部署由 generator gzip 雜湊閘門擋下，定位為單一分片內容偏差；修正後改以解壓後 generator source SHA-256 `05c760972b8c444c69c35b6e597ebf2d78241be2ea8e3ad83b1981c5a19f9e2a` 驗證完整性。
- 後續一次 run 因平行教材驗證回寫新 `main` 而被 concurrency 取消；另一次已完成 Pages 部署但 receipt push 遇到 non-fast-forward。最終由最新 `main` 的 `00cf9286eb7bbe3b2d8e2b6165cc163fd64a4e72` 成功完成 canonical 部署與回條寫入。
