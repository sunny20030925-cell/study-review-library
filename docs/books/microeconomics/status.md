# 《個體經濟學》狀態

更新日期：2026-07-29

## 正式定位

- Book ID：`microeconomics`
- 內容版本：`2026.07.29-1`
- 書庫版本：正式生成驗證為 `2026.07.29-8`；仍以本次 canonical run 的正式回條為準。
- 狀態：教材生成與 Pages 部署步驟已驗證通過；正在以最新 `main` 執行最後一次乾淨 canonical 驗收。
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
- canonical YAML 已由獨立 Actions 診斷解析通過。
- run `30410694604` 已確認個體經濟學生成、QA、Pages artifact 上傳與 GitHub Pages 部署步驟全部成功；該 run 僅因最後 metadata push 遭同步 workflow commit 插隊而標記失敗。

## 待完成

1. 從最新 `main` 完成乾淨 canonical run。
2. 由該 run 自動寫回 deployment receipt、正式 status、README 與 `docs/shared_checkpoint.md`。

在正式成功回條寫回前，不標記為「已部署」。
