# 《個體經濟學》狀態

更新日期：2026-07-29

## 正式定位

- Book ID：`microeconomics`
- 內容版本：`2026.07.29-1`
- 書庫版本：於正式部署當下依最新正式書庫版本順延，不硬編號覆蓋其他同步教材工作線。
- 狀態：預發布 QA、canonical workflow 整合與 YAML 驗證完成，待 GitHub Pages 實際部署回條。
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
- 已在目前正式六本書網站包上實際生成第七本測試站；`app.js`、`sw.js` 語法與 28 個代表性靜態路徑通過。
- 已於 canonical `Deploy study library` 中加入個體經濟學生成、動態書庫版本順延與正式 QA gate。
- canonical YAML 已由獨立 Actions 診斷以 Ruby parser 驗證通過；修復 commit 為 `184dbe67b41d385ef8746fc5abc2f09d13e3cfd3`。

## 待完成

1. GitHub Pages 實際部署成功。
2. 寫回 deployment receipt、正式 status、README 與 `docs/shared_checkpoint.md`。

在 Pages 成功回條產生前，不標記為「已部署」。
