# 重點複習書庫 Shared Checkpoint

更新日期：2026-07-30

本文件只保留人類容易閱讀的全書庫總進度。逐書 stage、task ID、External Audit／Visual Polish queue 以 `docs/audit_progress_manifest.json` 為準；逐書證據以各書 `status.md`、QA／audit／visual-polish record 為準。

## 正式書庫

- Repo：`sunny20030925-cell/study-review-library`
- 預設分支：`main`
- 固定入口：`https://sunny20030925-cell.github.io/study-review-library/`
- 形式：平板直式 PWA 書庫。
- 正式書庫內容版本：`2026.07.30-17`
- 正式書籍數：**21 本**。
- 最新成功正式 Pages run：`30548922518`
- 正式部署 source commit：`ecba17e5506eda029ed0464061589a2c27b2f5f9`
- 最新成功 Pages artifact：`8761921480`
- Artifact digest：`sha256:9a96e0540acaf41a219ac45e327443a14d1c1ff142f9e106d3ba0ba2ea06bb3a`
- Artifact re-download：PASS；下載 SHA256 與 digest 完全一致。
- `docs/deployment_receipt.json`：`status=success`、`book_count=21`、`library_version=2026.07.30-17`、`progress_storage_changed=false`。

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
- Visual Polish：**8／21 完成**；`statistics`、`commercial-law`、`advanced-statistics`、`game-theory`、`civil-law-overview`、`investments`、`econometrics`、`mathematical-economics` 已通過，剩餘 13 本在 queue。
  - 《高等統計學》：《高等統計推論路線圖》，沿用既有 `math-bridge.svg` cache path，附錄 B 可放大。
  - 《數理經濟學》：《最佳化與動態判斷地圖》，沿用既有 `kkt-inequality.svg` cache path，VP validator 40 checks。
  - 《商事法》：《商事法案例題雙軌判斷地圖》，沿用既有 `law-map.svg` cache path；VP validator 59 checks，部署前及 artifact 重下載後各 PASS。
  - 《民法概要》：《民法案例題請求權基礎地圖》，沿用既有 `civil-map.svg` cache path；現行民法第 125／179／184／767 條等高風險節點再次核對；VP validator **70 checks**，部署前及 artifact 重下載後各 PASS。
  - 《計量經濟學》：《計量經濟學因果識別方法選擇地圖》，沿用既有資產 cache path；VP validator **76 checks**，部署前及 artifact 重下載後各 PASS。
  - 《投資學》：《投資學考前模型選擇地圖》，沿用既有資產 cache path；VP validator **89 checks**，部署前及 artifact 重下載後各 PASS。
  - 《統計學》：《統計學推論方法選擇地圖》，沿用既有資產 cache path；VP validator **108 checks**，部署前及 artifact 重下載後各 PASS。
  - 《賽局理論及應用》：《賽局理論資訊結構與均衡概念選擇地圖》，沿用既有資產 cache path；VP validator **96 checks**，部署前及 artifact 重下載後各 PASS。
- Published：**21／21** 保持正式發布與 PWA 相容性；完成 VP 的 8 本已進入新制 `PUB` 完成狀態。

External Audit 路由依內容類型執行：數學／數值用 Wolfram；必要研究方法與實證結論用 Consensus；法律／制度與會計採正式一次來源；Scite 僅在需要重要論文 citation support／dispute context 時使用。

## 下一個正式任務

- Task ID：`microeconomics:VP`
- 書籍：《個體經濟學》
- Stage：Visual Polish
- 原則：只處理真正有考前價值的高價值視覺資產；依該書正式 routing 與既有 QA／External Audit 證據先複核高風險內容。
- EA queue 已清空，因此由 `visual_polish_queue[0]` 自動判定下一個 VP 任務。
## 基礎設施注意事項

- Visual Polish 發布已統一由 owner-triggered `Apply next Visual Polish` 共用 runner 執行；完成 Canva 批准後可自動完成套用、QA、Pages、artifact 重驗、generic recorder 與 VP→PUB control-plane closure，不再為每本建立暫時 listener／closure PR。
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
