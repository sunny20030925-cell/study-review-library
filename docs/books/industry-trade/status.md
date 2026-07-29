# 《產業及貿易》狀態

更新日期：2026-07-29

## 目前狀態

- Book ID：`industry-trade`
- 候選內容版本：`2026.07.29-1`
- 狀態：候選教材完成，待 GitHub candidate workflow 以最新正式 Pages artifact 重跑兩輪 QA；尚未正式部署。
- 正文：20 章。
- 附錄：3 份。
- 題庫：100 題，每章 5 題。
- 搜尋：160 筆。
- 圖解：20 張自製 SVG。

## 已完成

1. 依 `AGENTS.md`、knowledge index、content authoring spec、shared checkpoint 與 concurrent workflow 固定科目邊界。
2. 以「產業組織 × 國際貿易」為本科主線，避免重複完整《產業經濟學》或《國際經濟學》內容。
3. 完成 20 章、3 附錄、100 題、160 搜尋與 20 SVG 候選生成器。
4. 本地 Round 1：1,591 項檢查通過；既有正式 12 本書逐書 SHA-256 不變。
5. 本地 Round 2：545 項檢查通過；100 題逐題複核、20 題數值題獨立重算、12 個高風險章節重新判讀。
6. 修正 QA 發現的附錄變數覆蓋 bug、勞動邊際收益產品公式與三處公式字串轉義問題。
7. 反傾銷章依 WTO 公開說明精確化：正常價值／出口價格比較、重大損害與因果關係分開處理。
8. 已在正式 12 本 Pages artifact 副本模擬動態整合；測試結果為 13 本且 `app.js`／`sw.js` 語法通過。模擬 library version 僅作測試，不預占正式版本號。

## 發布邊界

- 候選內容與 QA 可與其他書籍平行。
- 正式共同書庫寫入不得使用本次本地 12 本副本直接發布。
- 準備正式發布時必須重新讀當下最新 `main`、`docs/shared_checkpoint.md`、registry、deployment receipt 與最新成功 Pages artifact。
- 若其他教材先部署，本書以最新正式書庫重新追加，動態提高 library／service worker 版本並重新跑兩輪 QA。
- 正式部署前要依 shared checkpoint 修正／驗證 canonical post-deploy recorder，不沿用過時自然語句硬比對。
- 正式部署後才把狀態改為「已部署」，並寫回最終 run、artifact、receipt 與全站書籍數。
