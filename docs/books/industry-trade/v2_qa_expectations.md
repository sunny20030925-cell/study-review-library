# 《產業及貿易》v2 QA expectations

正式發布前必須同時滿足：

- v2 content version `2026.07.30-1`。
- 100 題、160 搜尋、20 SVG、23 份正文／附錄 HTML。
- 20 個 q04 常見錯誤題皆直接回應並修正錯誤，無 `。。`。
- 24 個量化節點獨立重算。
- 28 個高風險正／負 gate 通過。
- 其他正式教材 hash 不變。
- 全站 Book ID 順序與數量不因本書內容修正而改變。
- `app.js`、`sw.js` 語法通過；service worker 版本隨共同書庫版本提高。
- Pages 部署後重抓 artifact，核對 digest、書籍數、本書 v2 與 progress compatibility。
