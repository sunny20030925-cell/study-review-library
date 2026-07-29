# 重點複習書庫 Shared Checkpoint

更新日期：2026-07-29

## 書庫

- Repo：`sunny20030925-cell/study-review-library`
- 預設分支：`main`
- 固定入口：`https://sunny20030925-cell.github.io/study-review-library/`
- 形式：平板直式 PWA 書庫，可持續加入新科目。
- 使用者操作限制：只使用平板；不得要求終端機、Git、電腦檔案管理、手動部署或多檔案上傳操作。
- 正式書庫內容版本：`2026.07.29-24`
- 正式書籍數：19 本。
- 最新正式 Pages run：`30472469702`。
- 最新正式部署 source commit：`00d76c2167c0132f7284e4e13e4106828d1647fc`。
- 最新 Pages artifact：`8732231529`。
- Artifact digest：`sha256:885891d570e82aa33dda22cb249584eca1733231f5fbda31cb7789b2dbc97a33`。
- Pages 狀態：正式 artifact 上傳、Pages deployment 與下載後 artifact recheck 均成功；`2026-07-29T16:49:21.676281+00:00`。
- 部署回條：`docs/deployment_receipt.json`；`status=success`、`book_count=19`、`library_version=2026.07.29-24`、`progress_storage_changed=false`。
- 實際下載正式 Pages artifact 後再次核對：19 本 registry；產業經濟學 23 份章節／附錄 HTML、100 題、150 搜尋、20 SVG 均存在；下載檔 SHA-256 與 GitHub artifact digest 一致。
- workflow overall conclusion：`success`；post-deploy recorder 採結構化 Book ID／receipt 更新。

## 正式規格與讀取順序

1. `AGENTS.md`：最高層執行規則。
2. `docs/project_knowledge_index.md`：新對話與新任務必讀順序。
3. `docs/content_authoring_spec.md`：教材、題庫、圖解與 QA 規格。
4. `docs/concurrent_book_workflow.md`：多書可平行製作、共同書庫必須序列發布的規則。
5. 本 checkpoint：目前正式書庫狀態。
6. 目標科目的 `scope.md`、`qa_report.md`、`status.md`。

固定原則：

- 科目本位：使用者背景只決定程度、先備知識與可能範圍，不得主導其他科目的正文、案例與題型。
- 跨科內容只有在標準課程本來包含、理解不可或缺或使用者明確要求時才可進入；其他內容列為延伸。
- 新科目先固定 scope，再製作內容；至少完成兩輪 QA 後才可正式整合。
- 不同科目的內容製作／QA 可平行；共同 PWA 整合與 Pages 發布必須序列化。
- 發布前必須重新讀最新 `main`、本 checkpoint、registry 與 deployment receipt，禁止拿舊 artifact 覆蓋較新的正式書庫。
- 正式成功以 canonical 產生／驗證、Pages artifact、Pages deployment 與 deployment receipt 為準；merge 本身不等於部署。
- 既有章節 ID、題目 ID、儲存鍵與閱讀／錯題進度不得無故破壞。

## 正式已部署書籍

### 1. 大一微積分
- Book ID：`calculus`
- 正式內容版本：`2026.07.27-3`
- 題庫：73 題；本版 QA 181／181。
- 狀態：已部署。

### 2. 會計學
- Book ID：`accounting`
- 正式內容版本：`2026.07.27-2`
- 成品：14 章、3 附錄、70 題、111 搜尋、13 圖解。
- 二次獨立複核修正 29 個內容點；70 題數值答案重算通過。
- 狀態：已部署。

### 3. 經濟學原理
- Book ID：`economics`
- 正式內容版本：`2026.07.27-2`
- 成品：20 章、3 附錄、100 題、144 搜尋、20 圖解。
- 初版兩輪 QA 與發布後獨立糾錯均完成。
- 狀態：已部署。

### 4. 統計學
- Book ID：`statistics`
- 正式內容版本：`2026.07.29-2`
- 成品：19 章、3 附錄、95 題、169 搜尋、19 圖解。
- 發布後二次校錯 1,195／1,195，44 項計算／公式重判。
- 狀態：已部署。

### 5. 商事法
- Book ID：`commercial-law`
- 正式內容版本：`2026.07.29-2`
- 成品：18 章、3 附錄、90 題、111 搜尋、18 圖解。
- 公司法第 8 條現行法 follow-up 與發布後內容複核已完成。
- 狀態：已部署。

### 6. 成本會計學
- Book ID：`cost-accounting`
- 正式內容版本：`2026.07.29-2`
- 成品：19 章、3 附錄、95 題、150 搜尋、19 圖解。
- 發布後二次內容審計 857／857，44 個數值答案重算。
- 狀態：已部署。

### 7. 個體經濟學
- Book ID：`microeconomics`
- 正式內容版本：`2026.07.29-2`
- 成品：20 章、3 附錄、100 題、154 搜尋、20 圖解。
- 發布後二次複核 1,616 項；15 題量化重算、20 題高風險觀念重判。
- 狀態：已部署。

### 8. 中級會計學
- Book ID：`intermediate-accounting`
- 正式內容版本：`2026.07.29-2`
- 成品：22 章、3 附錄、110 題、145 搜尋、22 圖解。
- 發布後二次內容審計 1,110 項；28 項量化重算。
- 狀態：已部署。

### 9. 總體經濟學
- Book ID：`macroeconomics`
- 正式內容版本：`2026.07.29-2`
- 成品：20 章、3 附錄、100 題、143 搜尋、20 圖解。
- 發布後第二次獨立複核 201／201；14 個內容修正、7 題題庫調整、20 題量化重算。
- 狀態：已部署。

### 10. 國際經濟學
- Book ID：`international-economics`
- 正式內容版本：`2026.07.29-2`
- 成品：20 章、3 附錄、100 題、144 搜尋、20 圖解。
- 初版 QA 696／696、1,383／1,383；v2 獨立 QA 1,656／1,656；17 題量化重算。
- 狀態：已部署。

### 11. 財政學
- Book ID：`public-finance`
- 正式內容版本：`2026.07.29-2`
- 成品：20 章、3 附錄、100 題、189 搜尋、20 圖解。
- 發布後獨立內容審計：16 個修正／補強區域；2,386 項結構／內容 gate、174 項 v2 gate、38 項量化重算通過。
- 狀態：已部署。

### 12. 貨幣銀行學
- Book ID：`money-banking`
- 正式內容版本：`2026.07.29-2`
- 定位：一般大學貨幣銀行學／貨幣金融學；貨幣、利率、金融市場、銀行、中央銀行、貨幣政策、通膨與開放經濟金融。
- 成品：20 章、3 附錄、100 題、150 搜尋、20 圖解。
- 舊工作線損壞 generator 未使用；由可讀 fresh source 重新生成。
- 第一輪 QA：963／963。
- 第二輪：20 個量化節點重算＋10 個高風險概念重判，全數通過。
- v2 獨立 QA：473／473；9 個章節二次複核修正、7 題詳解精確化。
- 正式 artifact 終檢：本書 23 份章節／附錄 HTML、100 題、150 搜尋、20 SVG 全部存在。
- 既有 11 本教材內容 hash 在整合前後完全一致，閱讀進度與錯題資料相容。
- 正式 Pages run：`30460567595`；Source commit：`2a2fff311c76a6e05a8a93fee9f3d5daaa474574`。
- 文件：`docs/books/money-banking/scope.md`、`docs/books/money-banking/qa_report.md`、`docs/books/money-banking/status.md`。
- 狀態：已部署。

### 13. 高等統計學
- Book ID：`advanced-statistics`
- 正式內容版本：`2026.07.29-1`
- 定位：一般大學高等統計／數理統計核心；承接基礎統計，聚焦機率模型、多元分配、極限定理、抽樣分配、估計與檢定理論。
- 成品：20 章、3 附錄、100 題、189 搜尋、20 圖解。
- QA：兩輪通過；27 個量化節點獨立重算、45 個高風險概念 gate。
- 既有 12 本教材內容 hash 在整合前後完全一致。
- 正式 Pages run：`30469711077`；Source commit：`cb320cac47bc58860ce92908d53646da94b7b103`。
- 文件：`docs/books/advanced-statistics/scope.md`、`docs/books/advanced-statistics/qa_report.md`、`docs/books/advanced-statistics/status.md`。
- 狀態：已部署。

### 14. 計算機概論
- Book ID：`computer-fundamentals`
- 正式內容版本：`2026.07.29-1`
- 定位：一般大學計算機概論；資料表示、硬體、作業系統、網路、程式與演算法、資料庫、資安、AI 與現代運算平台。
- 成品：20 章、3 附錄、100 題、150 搜尋、20 圖解。
- QA：第一輪 757 項、第二輪 598 項通過；17 個數值節點獨立重算、26 個高風險概念 gate。
- 既有 13 本教材內容 hash 在整合前後完全一致。
- 正式 Pages run：`30469780777`；Source commit：`85032444cfc17048117673e3c98546138771a88c`。
- 文件：`docs/books/computer-fundamentals/scope.md`、`docs/books/computer-fundamentals/qa_report.md`、`docs/books/computer-fundamentals/status.md`。
- 狀態：已部署。

### 15. 賽局理論及應用
- Book ID：`game-theory`
- 正式內容版本：`2026.07.29-1`
- 定位：一般大學賽局理論；策略式與展開式賽局、Nash／SPNE／BNE／PBE、重複賽局、拍賣、訊號、機制設計與合作賽局。
- 成品：20 章、3 附錄、100 題、189 搜尋、20 圖解。
- QA：第一輪 2385 項、第二輪 360 項通過；24 個數值節點獨立重算、19 個高風險概念 gate。
- 既有 14 本教材內容 hash 在整合前後完全一致。
- 正式 Pages run：`30470393224`；Source commit：`2c25ca9f2c0670002b819073d1a346c8c56f142c`。
- 文件：`docs/books/game-theory/scope.md`、`docs/books/game-theory/qa_report.md`、`docs/books/game-theory/status.md`。
- 狀態：已部署。

### 16. 民法概要
- Book ID：`civil-law-overview`
- 正式內容版本：`2026.07.29-1`
- 定位：一般大學民法概要；總則、債、物權、親屬、繼承，以請求權基礎與案例解題為主。
- 成品：20 章、3 附錄、100 題、150 搜尋、20 圖解。
- QA：第一輪 157 項、第二輪 670 項；14 組現行法高風險 gate、19 個高風險題目精確 gate。
- 現行法基準：2026-07-29；民法第 166-1 條保持「施行日期尚未另定」警示。
- 正式 Pages run：`30470779444`；Source commit：`34a0db9e8444bad4ac1b689c37bf5ea2bd679aa9`。
- 狀態：已部署。

### 17. 投資學
- Book ID：`investments`
- 正式內容版本：`2026.07.29-1`
- 定位：一般大學投資學；報酬與風險、投資組合、資產定價、證券估值、衍生工具、資產配置與績效評估。
- 成品：22 章、3 附錄、110 題、165 搜尋、22 圖解。
- QA：第一輪 2,672／2,672、第二輪 139／139；45 個量化節點重算、20 個高風險概念重判。
- 既有教材內容 hash 在整合前後完全一致，閱讀進度與錯題資料相容。
- 正式 Pages run：`30471109923`；Source commit：`63827e220a501c024ddd90482d7a798ac5995fad`。
- 文件：`docs/books/investments/scope.md`、`docs/books/investments/qa_report.md`、`docs/books/investments/status.md`。
- 狀態：已部署。

### 18. 計量經濟學
- Book ID：`econometrics`
- 正式內容版本：`2026.07.29-1`
- 定位：一般大學計量經濟學；OLS、多元迴歸與推論、異質變異、模型設定、二元結果、時間序列、panel、IV／2SLS、實驗、DiD、RDD、預測與實證研究流程。
- 成品：20 章、3 附錄、100 題、189 搜尋、20 圖解。
- QA：正式部署前 Round 1 = 384、Round 2 = 675；29 個數值節點獨立重算、32 個高風險答案 gate。部署後重新下載 artifact 再驗 Round 1 = 382、Round 2 = 675。
- 正式整合由 17 本／`2026.07.29-22` 追加為 18 本／`2026.07.29-23`，既有教材 hash 與進度儲存相容性受保護。
- 正式 Pages run：`30471586965`；Source commit：`4bdca45ab4772982a812017b34984aff19a9a6c1`；artifact：`8731859754`。
- Artifact digest／下載 SHA-256：`sha256:f53bf4979a85a0ff96e9e253cad04f97d37062d368195a97ce4189f8e934edf5`。
- 後續 19 本正式 registry 仍包含 `econometrics`，位置在 `investments` 與 `industrial-economics` 之間。
- 文件：`docs/books/econometrics/scope.md`、`docs/books/econometrics/qa_report.md`、`docs/books/econometrics/status.md`。
- 狀態：已部署。

### 19. 產業經濟學
- Book ID：`industrial-economics`
- 正式內容版本：`2026.07.29-1`
- 定位：一般大學產業經濟學／產業組織共同核心。
- 成品：20 章、3 附錄、100 題、150 搜尋、20 圖解。
- QA：兩輪通過；17 個量化節點、18 組高風險概念／條件複核。
- 既有 18 本教材 hash 在整合前後完全一致。
- 正式 Pages run：`30472469702`；Source commit：`00d76c2167c0132f7284e4e13e4106828d1647fc`。
- 狀態：已部署。

## Canonical 部署流程

1. 從正式基礎網站 artifact 開始，先驗證既有書庫與版本。
2. 直接下載 deployment receipt 指定的最新正式 Pages artifact，核對 digest、版本與書籍數；不再重播歷史書籍 generator／patch 鏈。
3. 新增或修正版教材只可接在當下最新正式尾端，且必須確認所有既有 Book ID、內容版本與進度相容性未倒退。
4. 各書內容／題庫／搜尋／SVG 與高風險公式／法律要件驗證通過後，再檢查 `app.js` 與 `sw.js`。
5. 全部正式檢查通過後才上傳單一完整 Pages artifact。
6. Pages deployment 成功後重新下載本次 artifact 驗證，再由結構化 recorder 寫回 deployment receipt、目標書 status／QA、README 與本 checkpoint。
7. 最新正式書庫：19 本，`2026.07.29-24`；Pages run `30472469702`，artifact `8732231529`。
8. 使用者不需要執行 Git、終端機、手動上傳或部署。

## 多書並行／發布規則

- 內容製作與 QA 可平行；發布依 `docs/concurrent_book_workflow.md` 序列化。
- 每條準備發布的工作線都要在最後一刻重新同步最新 `main`，確認正式書籍清單與版本。
- workflow concurrency 造成 cancelled 不視為內容失敗；不可用 cancelled run 當正式部署證據。
- workflow overall failure 若發生在 Pages deployment 成功後，必須用 job steps、artifact digest、Pages 狀態與下載 artifact 交叉驗證，再以 `[skip ci]` 校正 receipt；不得因此盲目重跑已成功 Pages。
- canonical post-deploy recorder 已採結構化 receipt／Book ID 更新；新增教材不得退回舊自然語句硬比對。

## 下一個新科目流程

1. 使用者只需指定科目，無須重貼歷史規格。
2. 助理先讀 `AGENTS.md`、knowledge index、content authoring spec、concurrent workflow 與本 checkpoint。
3. 沿用已驗證的結構化 canonical post-deploy recorder；不得改回自然語句硬比對。
4. 建立新科目的 `scope.md` 與 `status.md`，固定本科邊界。
5. 依標準本科課程製作教材、圖解、題庫、搜尋資料；必要時以可信官方／大學來源交叉核對。
6. 完成兩輪獨立 QA，重算數值題並設高風險負面 gate。
7. 發布前重新同步最新 main；確認其他平行教材是否已先正式發布。
8. 依 canonical workflow 加入同一 PWA；只有 Pages artifact／deployment 與 deployment receipt 均核實後才標記「已部署」。
9. 同步更新該書 status、QA report、README、deployment receipt 與本 checkpoint，任務才算收尾。