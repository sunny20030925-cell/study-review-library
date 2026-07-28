# 《個體經濟學》狀態

更新日期：2026-07-29

## 正式定位

- Book ID：`microeconomics`
- 內容版本：`2026.07.29-1`
- 書庫目標版本：`2026.07.29-7`
- 狀態：預發布 QA 完成，待 canonical GitHub Pages 實際部署。
- 範圍文件：`docs/books/microeconomics/scope.md`
- QA 報告：`docs/books/microeconomics/qa_report.md`

## 已完成

- 20 章正文＋3 附錄。
- 100 題題庫，每章 5 題。
- 154 筆搜尋索引。
- 20 張自製 SVG 圖解。
- 與《經濟學原理》分工：本書採一般大學中級個體經濟學深度，不重複製作入門經濟學。
- 第一輪結構／離線資源 QA：1321／1321 通過。
- 第二輪內容 gate：87／87 通過。
- 100 題逐題重新閱讀與重判；另獨立重算 15 題量化題、重判 15 題高風險觀念題。
- 在目前正式五本書網站包上實際生成測試站；`app.js`、`sw.js` 語法與 28 個代表性靜態路徑通過。

## 待完成

1. 將產生器與 QA gate 接入唯一 canonical `Deploy study library` 工作流。
2. GitHub Pages 實際部署成功。
3. 寫回 deployment receipt、正式 status、README 與 `docs/shared_checkpoint.md`。

在 Pages 成功回條產生前，不標記為「已部署」。
