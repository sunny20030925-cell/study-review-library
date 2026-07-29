# 重點複習專案 Knowledge Index

本文件定義新對話與新任務的正式讀取順序。聊天記憶只能作輔助，GitHub `main` 才是正式規格與進度來源。

## 必讀文件

1. [`AGENTS.md`](../AGENTS.md)
   - 最高層執行規則、平板操作邊界、科目本位、完整 stage 與發布門檻。
2. [`docs/content_authoring_spec.md`](content_authoring_spec.md)
   - 教材、圖解、題庫、語言與 Internal QA 的具體製作規格。
3. [`docs/external_audit_workflow.md`](external_audit_workflow.md)
   - External Audit、外部工具路由、風險式抽查、Visual Polish 與 task ID convention。
4. [`docs/audit_progress_manifest.json`](audit_progress_manifest.json)
   - 21 本全書庫 machine-readable stage、audit queue、下一本與不可破壞 invariants。
5. [`docs/shared_checkpoint.md`](shared_checkpoint.md)
   - 人類可讀的總進度、正式部署摘要、queue 數量與下一個正式任務。
6. 目標科目的正式文件
   - `docs/books/<book-id>/scope.md`
   - `docs/books/<book-id>/qa_report.md`
   - `docs/books/<book-id>/status.md`
   - 若已執行 External Audit，另讀該書 audit record／audit report。
7. 若涉及共同書庫寫入或多書並行，讀 [`docs/concurrent_book_workflow.md`](concurrent_book_workflow.md)。

## 任務類型與額外讀取

### 新增新科目

依序讀取：

1. `AGENTS.md`
2. `docs/project_knowledge_index.md`
3. `docs/content_authoring_spec.md`
4. `docs/external_audit_workflow.md`
5. `docs/audit_progress_manifest.json`
6. `docs/shared_checkpoint.md`
7. 若同時還有其他書籍對話在製作，讀 `docs/concurrent_book_workflow.md`。
8. 建立該科目的 `scope.md`，先固定科目邊界與共同課程範圍，再開始寫內容。

新書必須依新制完整通過 `DR → IQ → EA → VP → PUB`，不能因既有 21 本是 legacy migration 而跳過新階段。

### 修改既有科目

除上述文件外，必須再讀：

- 該科目的 scope。
- 最新 QA report。
- 最新 status。
- 最新 External Audit record（若已有）。
- 線上 manifest 與題庫版本。
- 本書在 `docs/audit_progress_manifest.json` 的 stage／task_id／next_stage。
- 若本次會發布到共同書庫，讀 `docs/concurrent_book_workflow.md`。

### 執行下一本 External Audit

不向使用者詢問「上一本文到哪裡」或要求重貼過去內容。流程固定為：

1. 重新讀最新 GitHub `main`。
2. 驗證 `docs/audit_progress_manifest.json` 的 `book_count=21` 與 deployment receipt／正式 registry 一致。
3. 取 `external_audit_queue[0]`。
4. 讀該書 scope、QA report、status 與實際正式內容。
5. 依 `docs/external_audit_workflow.md` 做風險式外部驗證。
6. 完成後更新該書詳細狀態、audit record 與 manifest。
7. shared checkpoint 只更新總數與下一本，不複製完整逐項 audit 細節。

### 修改書庫介面或部署

除上述文件外，必須檢查：

- `docs/concurrent_book_workflow.md`
- `docs/audit_progress_manifest.json`
- `docs/deployment_receipt.json`
- PWA manifest
- service worker 快取版本
- 書庫 registry
- GitHub Pages workflow
- 現有書籍入口與本機進度相容性
- 當下最新正式 21 本書籍清單與各書內容版本，避免版本倒退或覆蓋較新的書庫狀態

## 多書並行的正式原則

- 不同科目的 Draft、Internal QA、External Audit 準備與 Visual Polish 資產準備可以平行進行。
- 共同書庫整合與正式部署必須依 `docs/concurrent_book_workflow.md` 序列化。
- 每個準備發布的對話都必須重新讀最新 `main`、manifest、shared checkpoint 與 deployment receipt，不得使用對話開始時的舊書庫副本直接發布。
- 使用者不需要自行排發布順序；發布對話必須自行同步最新狀態並確認所有既有書籍與版本未倒退。

## 正式狀態來源

- `docs/audit_progress_manifest.json`：全書庫 machine-readable stage／queue／next task 的正式來源。
- 各科目的 `status.md`：該書詳細進度與證據的正式來源。
- 各科目的 QA／audit report：檢查證據與修正紀錄。
- `docs/shared_checkpoint.md`：只保留人類易讀的跨科目總進度與部署摘要，不再作逐書細節資料庫。
- `docs/deployment_receipt.json`：正式 Pages 部署與 21 本 registry 的部署證據。

任何內容更新、QA、External Audit、Visual Polish 或部署完成後，都必須更新適用的正式狀態來源；不能只在聊天中宣稱完成。
