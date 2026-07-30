# 重點複習書庫 Shared Checkpoint

更新日期：2026-07-30

本文件只保留人類容易閱讀的全書庫總進度。逐書 stage、task ID、External Audit／Visual Polish queue 以 `docs/audit_progress_manifest.json` 為準；逐書證據以各書 `status.md`、QA／audit report 為準。

## 正式書庫

- Repo：`sunny20030925-cell/study-review-library`
- 預設分支：`main`
- 固定入口：`https://sunny20030925-cell.github.io/study-review-library/`
- 形式：平板直式 PWA 書庫。
- 正式書庫內容版本：`2026.07.30-10`
- 正式書籍數：**21 本**。
- 最新成功正式 Pages run：`30519227208`
- 最新成功正式部署 source commit：`d9f1d3695f78e327f733af742f56e4326bceaa41`
- 最新成功 Pages artifact：`8750076767`
- Artifact digest：`sha256:fb988b14e7208c29e123804057b8b60102a50e7d73ca8dc61d817e4593db872f`
- `docs/deployment_receipt.json`：`status=success`、`book_count=21`、`library_version=2026.07.30-9`、`progress_storage_changed=false`。

## 正式工作流

`Draft → Internal QA → External Audit → Visual Polish → Published`

- `DR`：Draft
- `IQ`：Internal QA（既有兩輪 QA）
- `EA`：External Audit（風險式外部驗證）
- `VP`：Visual Polish（只處理高價值視覺資產，不搬離 PWA）
- `PUB`：Published

Task ID：`<book-id>:<stage-code>`。

正式讀取順序：

1. `AGENTS.md`
2. `docs/project_knowledge_index.md`
3. `docs/content_authoring_spec.md`
4. `docs/external_audit_workflow.md`
5. `docs/audit_progress_manifest.json`
6. 本 checkpoint
7. 目標書籍 status／QA／audit record
8. 涉及共同發布時再讀 `docs/concurrent_book_workflow.md`

## 目前總進度

- 正式書籍：**21／21 已發布**。
- Internal QA：**21／21 已完成**既有兩輪 QA。
- External Audit：**21／21 已通過**；`external_audit_queue=[]`。
  - `commercial-law`、`civil-law-overview`：既有正式法源／判決複核證據遷移為 `passed_migrated`。
  - 其餘 19 本：依新制完成 risk-based External Audit，結果均 `passed`。
  - 本輪 External Audit 沒有發現需要教材升版的核心答案錯誤；所有逐書證據已寫入 `docs/books/<book-id>/external_audit.md`。
- Visual Polish：**0／21 完成**；21 本目前均具備進入 VP 的前置條件。
- Published：**21／21** 保持既有正式發布與 PWA 相容性。

External Audit 路由已實際依內容類型執行：數學／數值用 Wolfram；必要的研究方法與實證結論用 Consensus；法律／制度與會計採正式一次來源；沒有為普通基礎敘述無差別消耗外部額度。Scite 僅在需要判定重要論文 citation support／dispute context 時使用，本輪抽查沒有出現必須升級到 Scite 才能判斷的 blocker。

## 下一個正式任務

- Task ID：`advanced-statistics:VP`
- 書籍：《高等統計學》
- Stage：Visual Polish
- 原則：只處理高價值視覺資產，例如封面、章末重點、比較圖、流程圖、公式／考前速查表；不得把整本教材搬離目前 PWA 架構。
- 新對話必須重新讀最新 `main` 與 `docs/audit_progress_manifest.json`；EA queue 已清空，因此由 `visual_polish_queue[0]` 自動判定下一個 VP 任務，不要求使用者記憶。

## 基礎設施注意事項

- 21 本 registry 的 `industry-trade` tail assertion 已改為相對順序 gate，允許其後存在 `mathematical-economics`。
- 部署紀錄已由 workflow-v2 generic recorder 接管；不再以逐書 legacy recorder 重寫 shared checkpoint 或逐書 stage。
- 最新共同 PWA／Pages artifact 已完成 upload、deploy、重新下載、digest 與 21 本結構驗證。

## 不可破壞的正式邊界

- 21 本正式書籍與既有 Book ID 全部保留。
- chapter ID、question ID 不得重建或任意改名。
- 閱讀進度、錯題資料、字體與本機設定儲存鍵保持相容。
- External Audit 與 Visual Polish 不得把整本教材搬離目前 PWA 架構。
- 共同 PWA 整合與 Pages 發布仍依 `docs/concurrent_book_workflow.md` 序列化。
- GitHub `main` 仍是唯一正式進度來源；聊天記憶不能取代 repo 狀態。
