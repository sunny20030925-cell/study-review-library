# 《貨幣銀行學》製作狀態

更新日期：2026-07-29

## 版本

- Book ID：`money-banking`
- 正式候選內容版本：`2026.07.29-1`
- 狀態：內容與兩輪 QA 已完成，canonical tail 候選已通過最新十書 artifact 實跑；待正式 PR 合併與 Pages 部署。
- 範圍文件：`docs/books/money-banking/scope.md`
- QA 報告：`docs/books/money-banking/qa_report.md`

## 成品

- 正文 20 章、附錄 3 份。
- 題庫 100 題，每章 5 題。
- 搜尋索引 150 筆。
- 自製 SVG 20 張。
- 正文使用繁體中文；一般金額例題採新臺幣。
- 以貨幣、金融市場、銀行、中央銀行與貨幣政策為主線，總體經濟內容只保留政策傳遞所需部分。

## QA

- 第一輪：963 項結構、內容、題庫、搜尋、SVG、離線路徑與高風險敘述檢查通過。
- 第二輪：20 個量化節點重新驗算；貨幣乘數、放款創造存款、QE、Fisher、操作框架、Taylor principle、金融安全網與匯率方向等高風險觀念重新判讀。
- 最新正式十書 artifact 實跑：`2026.07.29-13`／10 本 → `2026.07.29-14`／11 本，新增尾端僅為 `money-banking`。
- 閱讀進度相容性：候選不修改既有 book ID、章節 ID、題目 ID 或儲存格式。

## 剩餘完成門檻

1. 合併前再次確認最新 `main`，避免同日其他教材發布造成序列化衝突。
2. Money and Banking PR 合併。
3. canonical `Deploy study library` 完整驗證與 Pages 部署成功。
4. deployment receipt 確認新增 `money-banking`、書籍數增加一、`progress_storage_changed=false`。
5. 將本 status、README、shared checkpoint 與 deployment receipt 更新為正式部署結果。
