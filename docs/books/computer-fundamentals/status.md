# 《計算機概論》製作狀態

更新日期：2026-07-29

## 正式識別

- Book ID：`computer-fundamentals`
- 書名：《計算機概論》
- 目標內容版本：`2026.07.29-1`
- 目前階段：`candidate_qa_running`
- 正式部署：尚未完成。
- 範圍文件：`docs/books/computer-fundamentals/scope.md`
- QA 報告：`docs/books/computer-fundamentals/qa_report.md`

## 候選成品

- 20 章正文。
- 3 份附錄：數字／資料表示與核心關係速查、解題路線、中英名詞對照。
- 100 題題庫，每章 5 題。
- 150 筆搜尋索引。
- 20 張自製 SVG。
- 一般大學計算機概論共同核心：資料表示、數位邏輯、硬體、儲存、I/O、作業系統、網路、Internet、程式語言、演算法、資料結構、資料庫、軟體工程、資安、AI、雲端／分散式與資訊倫理。

## QA 設計

- 第一輪：`deploy/validate_computer_fundamentals.py`，做結構、整合、代表性答案與 PWA cache 檢查。
- 第二輪：`deploy/qa_computer_fundamentals_independent.py`，獨立重算數值、重判高風險概念並逐題檢查 100 題詳解。
- PR workflow：`.github/workflows/validate-computer-fundamentals-candidate.yml`。
- workflow 會從最新成功 Pages artifact 建立候選，不使用對話開始時的舊書庫副本。
- 既有書籍在候選生成前後做逐檔 SHA-256，比對不一致即失敗。
- 本 QA 分支只更新狀態文件以觸發正式 PR workflow，不修改候選教材內容；已在 workflow 進入 `main` 後再次同步一次。

## 發布規則

本書可在獨立分支完成內容與 QA；進入共同書庫整合前，必須重新同步最新 `main`、shared checkpoint、正式書籍清單、書庫版本與 deployment receipt。共同 PWA 寫入與 Pages deployment 依 `docs/concurrent_book_workflow.md` 序列化，不得用本分支開始時的 12 書狀態覆蓋之後的新版本。
