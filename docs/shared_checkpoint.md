# 重點複習書庫 Shared Checkpoint

更新日期：2026-07-30

本文件只保留人類容易閱讀的全書庫總進度。逐書 stage、task ID、External Audit／Visual Polish queue 以 `docs/audit_progress_manifest.json` 為準；逐書證據以各書 `status.md`、QA／audit／visual-polish record 為準。

## 正式書庫

- Repo：`sunny20030925-cell/study-review-library`
- 預設分支：`main`
- 固定入口：`https://sunny20030925-cell.github.io/study-review-library/`
- 形式：平板直式 PWA 書庫。
- 正式書庫內容版本：`2026.07.30-12`
- 正式書籍數：**21 本**。
- 最新成功正式 Pages run：`30532667241`（`Apply commercial law Visual Polish`）。
- 正式部署 source commit：`dd52ab5bfa1797678a2676de5abbc05a049a9d8b`。
- 最新成功 Pages artifact：`8755330612`。
- Artifact digest：`sha256:202289641e0ae502fa0bd2bbd78f8938c4978c8a5ba04d850d5f8cb12dedac13`。
- Artifact re-download：PASS；下載 SHA256 與 digest 完全一致。
- `docs/deployment_receipt.json`：`status=success`、`book_count=21`、`library_version=2026.07.30-12`、`progress_storage_changed=false`。

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
7. 目標書籍 status／QA／audit／visual-polish record
8. 涉及共同發布時再讀 `docs/concurrent_book_workflow.md`

## 目前總進度

- 正式書籍：**21／21 已發布**。
- Internal QA：**21／21 已完成**既有兩輪 QA。
- External Audit：**21／21 已通過**；`external_audit_queue=[]`。
  - `commercial-law`、`civil-law-overview`：既有正式法源／判決複核證據遷移為 `passed_migrated`。
  - 其餘 19 本：依新制完成 risk-based External Audit，結果均 `passed`。
- Visual Polish：**3／21 完成**；`advanced-statistics`、`mathematical-economics`、`commercial-law` 已通過，剩餘 18 本在 queue。
  - 《高等統計學》：《高等統計推論路線圖》，沿用既有 `math-bridge.svg` cache path，附錄 B 可放大。
  - 《數理經濟學》：《最佳化與動態判斷地圖》，沿用既有 `kkt-inequality.svg` cache path，VP validator 40 checks。
  - 《商事法》：《商事法案例題雙軌判斷地圖》，沿用既有 `law-map.svg` cache path；公司法 §194／§214、證交法 §157／§157-1 等高風險區別以現行法精確化；VP validator **59 checks**，部署前及 artifact 重下載後各 PASS。
- Published：**21／21** 保持正式發布與 PWA 相容性；完成 VP 的 3 本已進入新制 `PUB` 完成狀態。

External Audit 路由依內容類型執行：數學／數值用 Wolfram；必要研究方法與實證結論用 Consensus；法律／制度與會計採正式一次來源；Scite 僅在需要重要論文 citation support／dispute context 時使用。

## 下一個正式任務

- Task ID：`civil-law-overview:VP`
- 書籍：《民法概要》
- Stage：Visual Polish
- 原則：只處理一個真正有考前價值的高價值視覺資產；法律內容須以現行官方法規／必要判決先複核，不得為了美化改變實體法律規則。
- 新對話必須重新讀最新 `main` 與 `docs/audit_progress_manifest.json`；EA queue 已清空，因此由 `visual_polish_queue[0]` 自動判定下一個 VP 任務。

## 基礎設施注意事項

- 21 本 registry 的 `industry-trade` tail assertion 已改為相對順序 gate，允許其後存在 `mathematical-economics`。
- 部署紀錄由 workflow-v2 generic recorder 接管；不再以逐書 legacy recorder 重寫逐書 stage。
- 商事法 VP 初次 follow-up 未留下 recorder；在 listener 已存在於 `main` 後以 control-plane-only PR #155 重新觸發 canonical deployment，之後 VP run `30532667241` 成功。此事件已留下完整 deployment evidence，不需再次重跑。
- 最新共同 PWA／Pages artifact 已完成 upload、deploy、重新下載、digest 與 21 本結構驗證。

## 不可破壞的正式邊界

- 21 本正式書籍與既有 Book ID 全部保留。
- chapter ID、question ID 不得重建或任意改名。
- 閱讀進度、錯題資料、字體與本機設定儲存鍵保持相容。
- External Audit 與 Visual Polish 不得把整本教材搬離目前 PWA 架構。
- 共同 PWA 整合與 Pages 發布仍依 `docs/concurrent_book_workflow.md` 序列化。
- GitHub `main` 仍是唯一正式進度來源；聊天記憶不能取代 repo 狀態。
