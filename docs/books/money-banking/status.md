# 《貨幣銀行學》製作狀態

更新日期：2026-07-29

## 正式識別

- Book ID：`money-banking`
- 正式內容版本：`2026.07.29-2`
- 正式書庫版本：`2026.07.29-17`
- 狀態：已部署。
- 固定入口：`https://sunny20030925-cell.github.io/study-review-library/`
- 範圍文件：`docs/books/money-banking/scope.md`
- QA 報告：`docs/books/money-banking/qa_report.md`

## 正式成品

- 正文：20 章（ch00–ch19）。
- 附錄：3 份。
- 題庫：100 題，每章 5 題。
- 搜尋索引：150 筆。
- 自製 SVG：20 張。
- 平板功能：共同 PWA 的連續閱讀、章節導覽、全文搜尋、題庫、閱讀進度、錯題紀錄與離線快取均已納入正式 artifact。

## 二次複核與修正

- 舊工作分支的 7 片壓縮 generator 經重新驗證確認內容損壞，正式發布完全未使用該封裝；教材改由可讀的 fresh source 重新生成。
- 修正／補強債券報酬與 YTM、存續期間與凸性、銀行監理與最後貸款者、準備貨幣／銀行準備、放款創造存款、貨幣乘數、臺灣央行工具、Fisher equation／effect、QE 與匯率方向等高風險內容。
- 9 個章節另加入二次複核框；7 題高風險題目詳解同步精確化。
- 新增前後既有 11 本教材目錄內容 SHA-256 完全一致，未覆蓋既有書籍。

## QA

- 第一輪結構／內容 QA：963／963 通過。
- 第二輪：20 個量化節點重新計算、10 個高風險概念重判，全數通過。
- v2 獨立 QA：473／473 通過。
- 正式 artifact 終檢：12 本書、全站版本 `2026.07.29-17`；本書 23 份章節／附錄 HTML、100 題、150 搜尋、20 SVG 全部存在。

## 正式部署

- canonical workflow：`Deploy study library`
- workflow run：`30460567595`
- source commit：`2a2fff311c76a6e05a8a93fee9f3d5daaa474574`
- Pages artifact：`8727395112`
- Artifact digest：`sha256:0d3dffa1e6b57d41f3ae8181d599f337b545d3f6ec92a0b677d65c7366104ba8`
- GitHub Pages：2026-07-29 14:23:09 UTC 回報 success。
- workflow overall conclusion：`failure-after-successful-pages-deploy`；唯一失敗為部署後 repo 記錄器的舊 checkpoint 句型匹配，未影響 artifact 或 Pages。
- 本狀態與 `docs/deployment_receipt.json` 已依 workflow job、Pages deployment 與實際下載 artifact 手動複核後校正。
- 閱讀進度相容性：新增獨立 Book ID；既有 11 本書內容 hash 不變，未改其章節 ID、題目 ID 或進度儲存鍵。
