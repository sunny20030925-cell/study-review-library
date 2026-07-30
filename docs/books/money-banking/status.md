# 《貨幣銀行學》製作狀態

更新日期：2026-07-30

## 正式識別

- Book ID：`money-banking`
- 正式內容版本：`2026.07.29-2`
- 正式書庫版本：`2026.07.30-24`
- 目前 stage：`PUB`
- Task ID：`money-banking:PUB`
- 下一階段：無；本書新制流程已完成。
- Published：`passed`。
- Internal QA：`docs/books/money-banking/qa_report.md`
- External Audit：`docs/books/money-banking/external_audit.md`

## Internal QA 證據

- 正文 20 章、附錄 3 份、題庫 100 題、搜尋索引 150 筆、SVG 20 張。
- 第一輪 963／963；第二輪 20 個量化節點＋10 個高風險概念；v2 QA 473／473。
- 已精確化 YTM、duration/convexity、銀行準備、deposit creation、money multiplier、臺灣央行工具、Fisher、QE 與匯率方向。

## External Audit

- 結果：`passed`
- 路由：Wolfram + 臺灣中央銀行官方資料。
- 抽查 time value、bond/duration、bank balance sheet、ROA/ROE、money multiplier caveat、準備金／公開市場／貼現窗口制度。
- 核心答案錯誤：0；需要升版：否；unresolved blocker：0。

## 相容性

Book／chapter／question IDs、題數、PWA、閱讀進度與錯題資料均不變；正式 21 本 artifact 維持 `2026.07.30-9`。

## Visual Polish 完成（2026-07-30）

- Task：`money-banking:VP`；結果：`passed`。
- 高價值資產：`貨幣銀行學貨幣創造政策傳導與利率匯率方向判斷地圖`。
- Canva design ID：`DAHQ45LQcmg`；可編輯來源：`https://www.canva.com/d/GPYtOwpOZTmyRuy`。
- PWA 資產：`assets/money-banking-svg/money-map.svg`；平板可閱讀、可放大、沿用既有離線 cache path。
- 正式 run：`30575380058`；Pages artifact：`8772467872`。
- Artifact digest：`sha256:11d362be033746f776ce64d5f64b45e5fc25974d9606bc40aa4a26fcccf97afb`；重新下載 SHA256 完全一致。
- VP validator：`160 checks`，正式部署前與 artifact 重下載後均 `visual_polish=passed`。
- 正式內容版本未因純視覺整理升版；閱讀進度、錯題資料與 storage key 相容，`progress_storage_changed=false`。
- 詳細證據：`docs/books/money-banking/visual_polish.md`。
- 本書已切換至 `money-banking:PUB`。
- 全書庫下一個 Visual Polish target：`intermediate-accounting`。
