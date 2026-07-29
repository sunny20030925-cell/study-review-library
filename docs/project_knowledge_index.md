# 重點複習專案 Knowledge Index

本文件定義新對話與新任務的正式讀取順序。聊天記憶只能作輔助，GitHub 文件才是正式規格與進度來源。

## 必讀文件

1. [`AGENTS.md`](../AGENTS.md)
   - 最高層執行規則、平板操作邊界、科目本位原則、QA 與發布門檻。
2. [`docs/content_authoring_spec.md`](content_authoring_spec.md)
   - 教材、圖解、題庫、語言與內容密度的具體製作規格。
3. [`docs/shared_checkpoint.md`](shared_checkpoint.md)
   - 目前書庫版本、已完成書籍、待修正事項與下一個正式任務。
4. 目標科目的正式文件
   - 建議路徑：`docs/books/<book-id>/scope.md`
   - 建議路徑：`docs/books/<book-id>/qa_report.md`
   - 建議路徑：`docs/books/<book-id>/status.md`

## 任務類型與額外讀取

### 新增新科目

依序讀取：

1. `AGENTS.md`
2. `docs/project_knowledge_index.md`
3. `docs/content_authoring_spec.md`
4. `docs/shared_checkpoint.md`
5. 若同時還有其他書籍對話在製作，讀 `docs/concurrent_book_workflow.md`。
6. 建立該科目的 `scope.md`，先固定科目邊界與共同課程範圍，再開始寫內容。

### 修改既有科目

除上述文件外，必須再讀：

- 該科目的 scope
- 最新 QA report
- 最新 status
- 線上 manifest 與題庫版本
- 若本次會發布到共同書庫，讀 `docs/concurrent_book_workflow.md`

### 修改書庫介面或部署

除上述文件外，必須檢查：

- `docs/concurrent_book_workflow.md`
- PWA manifest
- service worker 快取版本
- 書庫 registry
- GitHub Pages workflow
- 現有書籍入口與本機進度相容性
- 當下最新正式書籍清單與各書內容版本，避免版本倒退或覆蓋較新的書庫狀態

## 多書並行的正式原則

- 不同科目的內容製作與 QA 可以平行進行。
- 共同書庫整合與正式部署必須依 `docs/concurrent_book_workflow.md` 序列化。
- 每個準備發布的對話都必須重新讀最新 `main` 與 `docs/shared_checkpoint.md`，不得使用對話開始時的舊書庫副本直接發布。
- 使用者不需要自行排發布順序；發布對話必須自行同步最新狀態並確認所有既有書籍與版本未倒退。

## 正式狀態原則

- `docs/shared_checkpoint.md` 是跨科目總進度的唯一正式 checkpoint。
- 各科目的 `status.md` 是該書進度的唯一正式來源。
- 完成內容更新、QA 或部署後，必須同步更新 checkpoint；否則任務不算收尾。
