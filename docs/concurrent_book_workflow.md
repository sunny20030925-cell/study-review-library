# 多書並行製作與共同書庫發布規則

更新日期：2026-07-30

本文件規範多個對話同時製作、QA、External Audit 或 Visual Polish 不同書籍時，如何避免使用舊書庫狀態覆蓋較新的內容。

## 一、允許的並行範圍

- 不同科目的內容研究、章節撰寫、圖解、題庫建立、Internal QA、External Audit 準備與 Visual Polish 資產準備，可以同時在不同對話進行。
- 每一本書必須使用獨立 Book ID、scope、status、QA report、audit record、正文與題庫內容包。
- 不同對話不得共用一份離線舊書庫副本作為最終發布來源。
- External Audit queue 的正式順序以最新 `docs/audit_progress_manifest.json` 為準；使用者不需要自行記憶下一本。

## 二、External Audit queue 協調

- 新對話要執行「下一本 External Audit」時，必須重新讀最新 `main` 與 manifest，再取 `external_audit_queue[0]`。
- 若 queue 第一項已被另一工作線正式標為 `in_progress` 或 `passed`，重新讀最新 `main` 後再選下一項；不得靠舊聊天記憶重複消耗外部額度。
- External Audit 採風險式抽查，不因多書並行而把所有普通敘述大量送外部工具。
- 同一本書的 External Audit 不得由兩條工作線在不知道彼此狀態的情況下重複進行。

## 三、正式發布必須序列化

- 「加入共同書庫、提高全站版本、更新 registry、service worker、部署包、Pages 部署」屬於共同資源寫入，必須一次只處理一本或一次只處理一個明確整合批次。
- 任一書籍準備正式發布前，必須重新讀取當下 GitHub `main`、`docs/audit_progress_manifest.json`、`docs/shared_checkpoint.md`、`docs/deployment_receipt.json`、最新書庫 registry 與部署流程；不得沿用該對話開始時保存的舊狀態直接覆蓋。
- 若其他書籍在本對話製作期間已發布，當前書籍必須以最新正式 artifact／GitHub 書庫為基底重新整合。

## 四、禁止覆蓋與版本倒退

正式發布前必須驗證：

1. 現有 21 本正式書籍仍全部存在。
2. 任何既有書籍的內容版本不得倒退。
3. 任何既有 Book ID、chapter ID、question ID 不得因另一科目的發布而被意外刪除、重建或重新編號。
4. 閱讀進度、錯題、字體與本機設定的儲存鍵不得被清空或改名，除非有明確遷移方案且使用者同意。
5. `docs/audit_progress_manifest.json` 的 `book_count`、正式 registry 與 deployment receipt 的 `book_count` 必須一致。
6. 新部署完成後，必須再次核對全站書籍數、各書版本、stage 狀態與 deployment receipt。

若任一項不符，停止部署並先修正，不得以「後一版再補」方式覆蓋上線。

## 五、版本規則

- 每一本書維持自己的 `content version`。
- 共同書庫另有全站內容版本。
- 修正某一本書內容時，該書自己的內容版本必須提高；只提高全站版本不能視為該書已更新。
- 純 workflow／status／manifest 調整若沒有教材內容變更，不提高教材 content version。
- 多本書同批整合時，每一本實際有內容變更的書都必須各自提高版本並留下 changelog／QA／audit 記錄。

## 六、發布前重新同步程序

每個準備發布的對話，在進入共同書庫寫入前必須：

1. 重新讀 `AGENTS.md`。
2. 重新讀 `docs/project_knowledge_index.md`。
3. 重新讀 `docs/external_audit_workflow.md`。
4. 重新讀 `docs/audit_progress_manifest.json`。
5. 重新讀本文件。
6. 重新讀最新 `docs/shared_checkpoint.md` 與 `docs/deployment_receipt.json`。
7. 讀目標科目的最新 scope、status、QA report 與 audit record（若有）。
8. 核對目前正式 21 本書籍清單與版本。
9. 在最新狀態上套入本次新增／修正內容。
10. 跑完整整合驗證後才部署。

## 七、使用者不需要協調發布鎖

- 使用者可以自由同時開多個科目對話，不需要自己排程誰先做。
- 各對話在準備發布時，應自行以 GitHub 最新狀態判斷是否需要重新同步。
- 若發現另一個對話正在進行共同書庫寫入，當前工作可繼續做內容、QA、External Audit 或 Visual Polish，但共同部署必須等前一個整合完成後再重新讀最新狀態。

## 八、收尾回報

每次正式內容發布後至少回報：

- 該書舊版本 → 新版本
- 全站舊版本 → 新版本
- 本次主要修改
- Internal QA／External Audit 結果
- Visual Polish 是否完成或未涉及
- 閱讀進度是否相容
- 正式部署 run／receipt
- 核對後的全站 21 本書籍與各書版本未倒退
- manifest 的該書 stage／task_id／next_stage 是否已同步

純工作流或狀態系統升級若沒有教材內容變更，則只需驗證正式 21 本 registry／IDs／progress compatibility 未被修改，不得假裝成新的教材發布。
