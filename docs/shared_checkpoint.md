# 重點複習書庫 Shared Checkpoint

更新日期：2026-07-30

本文件只保留人類容易閱讀的全書庫總進度。逐書詳細狀態、External Audit queue、task ID 與下一階段以 `docs/audit_progress_manifest.json` 為準；逐書證據以各書 `status.md`、QA／audit report 為準。

## 正式書庫

- Repo：`sunny20030925-cell/study-review-library`
- 預設分支：`main`
- 固定入口：`https://sunny20030925-cell.github.io/study-review-library/`
- 形式：平板直式 PWA 書庫，可持續加入新科目。
- 使用者操作限制：只使用平板；不得要求終端機、Git、電腦檔案管理、手動部署或多檔案上傳操作。
- 正式書庫內容版本：`2026.07.30-9`
- 正式書籍數：**21 本**。
- 最新正式 Pages run：`30494922034`
- 最新正式部署 source commit：`d502e3db8be674c030c5b13db88f1b33dfdedb28`
- 最新 Pages artifact：`8741187091`
- Artifact digest：`sha256:576f046c2f6e98f1cab56ca7136042e1dfb66a4af1ad21e74552ce16b2db1eeb`
- 部署回條：`docs/deployment_receipt.json`；`status=success`、`book_count=21`、`library_version=2026.07.30-9`、`progress_storage_changed=false`。

## 正式工作流

新制固定為：

`Draft → Internal QA → External Audit → Visual Polish → Published`

- `DR`：Draft
- `IQ`：Internal QA（既有兩輪 QA）
- `EA`：External Audit（風險式外部驗證）
- `VP`：Visual Polish（只處理高價值視覺資產）
- `PUB`：Published

Task ID：`<book-id>:<stage-code>`。

正式規則：

1. `AGENTS.md`
2. `docs/project_knowledge_index.md`
3. `docs/content_authoring_spec.md`
4. `docs/external_audit_workflow.md`
5. `docs/audit_progress_manifest.json`
6. 本 checkpoint
7. 目標書籍 status／QA／audit record
8. 涉及共同發布時再讀 `docs/concurrent_book_workflow.md`

## Workflow Upgrade 遷移結果

- 既有 21 本正式教材全部保留，沒有重新製作、刪除、重新編號或搬離 PWA。
- 21 本 `DR=passed`、`IQ=passed`、`PUB=passed`；既有發布標記為 workflow v2 建立前的 legacy publication，不因此下架。
- 《商事法》與《民法概要》已有以正式現行法規、官方資料／正式判決為核心的獨立法律複核證據，遷移為 `EA=passed_migrated`。
- 其餘 **19 本**為 `EA=pending`，進入正式 External Audit queue。
- External Audit 通過後才進入 Visual Polish；Canva 只處理封面、章末重點、比較圖、流程圖、公式／考前速查表等高價值資產，不搬移整本教材。

## 目前總進度

- 正式書籍：21／21 已發布。
- Internal QA：21／21 已完成既有兩輪 QA。
- External Audit：2／21 已有足夠正式證據遷移通過；19／21 待執行。
- Visual Polish：0／21 依新制正式完成；《商事法》、《民法概要》已具備進入 VP 的前置條件。
- Published：21／21 保持既有正式發布與 PWA 相容性。

## 下一個正式任務

- Task ID：`advanced-statistics:EA`
- 書籍：《高等統計學》
- 階段：External Audit
- 主路由：Wolfram
- 次路由：只有涉及實證研究／文獻主張時才使用 Consensus／Scite。
- 原則：先抽查高風險分配、估計、likelihood、檢定條件、漸近結果與推導；不對普通基礎敘述做無差別第三輪全量查核。

新對話不得要求使用者自己記得下一本。必須重新讀最新 `main` 與 `docs/audit_progress_manifest.json`，由 `external_audit_queue[0]` 自動判定。

## 不可破壞的正式邊界

- 21 本正式書籍與既有 Book ID 全部保留。
- chapter ID、question ID 不得重建或任意改名。
- 閱讀進度、錯題資料、字體與本機設定儲存鍵保持相容。
- External Audit 與 Visual Polish 不得把整本教材搬離目前 PWA 架構。
- 共同 PWA 整合與 Pages 發布仍依 `docs/concurrent_book_workflow.md` 序列化。
- GitHub `main` 仍是唯一正式進度來源；聊天記憶不能取代 repo 狀態。
