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
- 最新成功正式 Pages run：`30494922034`
- 最新成功正式部署 source commit：`d502e3db8be674c030c5b13db88f1b33dfdedb28`
- 最新成功 Pages artifact：`8741187091`
- Artifact digest：`sha256:576f046c2f6e98f1cab56ca7136042e1dfb66a4af1ad21e74552ce16b2db1eeb`
- 部署回條：`docs/deployment_receipt.json`；`status=success`、`book_count=21`、`library_version=2026.07.30-9`、`progress_storage_changed=false`。

## 正式工作流

`Draft → Internal QA → External Audit → Visual Polish → Published`

- `DR`：Draft
- `IQ`：Internal QA（既有兩輪 QA）
- `EA`：External Audit（風險式外部驗證）
- `VP`：Visual Polish（只處理高價值視覺資產）
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

- 正式書籍：21／21 已發布。
- Internal QA：21／21 已完成既有兩輪 QA。
- External Audit：**3／21 已通過**；18／21 待執行。
  - `commercial-law`：`passed_migrated`
  - `civil-law-overview`：`passed_migrated`
  - `advanced-statistics`：`passed`（2026-07-30，Wolfram 風險式外部驗算）
- Visual Polish：0／21 依新制正式完成；`advanced-statistics`、`commercial-law`、`civil-law-overview` 已具備進入 VP 的前置條件。
- Published：21／21 保持既有正式發布與 PWA 相容性。

## 最新 External Audit 結果

### `advanced-statistics:EA`

- 結果：`passed`
- 內容版本：維持 `2026.07.30-1`，不需升版。
- Wolfram：獨立重算既有 v2 validator 20 個數值節點；另驗算 Bernoulli Fisher information／CRLB 與 Exponential MLE invariance，全部一致。
- 高風險定理條件：條件常態、Slutsky、Delta、MLE invariance、完備／充分、Rao–Blackwell、精確 z/t、size／level、NP、UMP／MLR／Wilks、Gauss–Markov／F-test 均未留下核心 blocker。
- Consensus／Scite：本輪無需使用，沒有抽到必須以實證研究或論文引用脈絡才能判斷的核心主張。
- Audit record：`docs/books/advanced-statistics/external_audit.md`
- Book ID、chapter ID、question ID、閱讀進度、錯題資料與 PWA 內容包均未修改。

## 下一個正式 External Audit

- Task ID：`mathematical-economics:EA`
- 書籍：《數理經濟學》
- 主路由：Wolfram。
- 次路由：只有涉及實證研究／學術主張或重要論文引用脈絡時才使用 Consensus／Scite。
- 原則：優先抽查最佳化、矩陣代數、比較靜態、差分／微分方程與高風險推導，不對普通基礎敘述做無差別第三輪全量查核。

新對話不得要求使用者自己記得下一本。必須重新讀最新 `main` 與 `docs/audit_progress_manifest.json`，由 `external_audit_queue[0]` 自動判定。

## 基礎設施注意事項

- Workflow Upgrade 合併後的 run `30496283761` 失敗於舊的 industry-trade inline gate：它仍假設 `industry-trade` 必須是 registry 最後一本；正式 21 本中其後已有 `mathematical-economics`。
- 此失敗沒有形成新的 Pages artifact，也沒有取代上述成功正式 artifact／deployment receipt；目前正式網站仍以 run `30494922034` 為準。
- 在下一次需要正常觸發共同 PWA／Pages 部署前，應先修正此過時的 20 本尾端假設。External Audit 的純狀態寫回可用 `[skip ci]`，不需要重跑已成功的正式 Pages artifact。

## 不可破壞的正式邊界

- 21 本正式書籍與既有 Book ID 全部保留。
- chapter ID、question ID 不得重建或任意改名。
- 閱讀進度、錯題資料、字體與本機設定儲存鍵保持相容。
- External Audit 與 Visual Polish 不得把整本教材搬離目前 PWA 架構。
- 共同 PWA 整合與 Pages 發布仍依 `docs/concurrent_book_workflow.md` 序列化。
- GitHub `main` 仍是唯一正式進度來源；聊天記憶不能取代 repo 狀態。
