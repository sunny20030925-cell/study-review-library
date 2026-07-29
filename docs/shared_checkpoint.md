# 重點複習書庫 Shared Checkpoint

更新日期：2026-07-29

## 書庫

- Repo：`sunny20030925-cell/study-review-library`
- 預設分支：`main`
- 固定入口：`https://sunny20030925-cell.github.io/study-review-library/`
- 形式：平板直式 PWA 書庫，可持續加入新科目。
- 使用者操作限制：只使用平板；不得要求終端機、Git、電腦檔案管理、手動部署或多檔案上傳操作。
- 正式書庫內容版本：`2026.07.29-16`
- 正式書籍數：11 本。
- 最新正式 Pages run：`30452678302`。
- 最新正式部署 source commit：`24bcf00d73dcb2e11b4d2dfbce14c5e99b5db85d`。
- 最新 Pages artifact：`8724164394`。
- Artifact digest：`sha256:282d2bdeec05a04427dd13a5c50aa1fcce172011fff4c1403fd563c4cfc1b201`。
- Pages 狀態：Upload artifact 與 Deploy to GitHub Pages 均成功，2026-07-29T12:42:18.566584+00:00 回報成功。
- 部署回條：`docs/deployment_receipt.json`；`status=success`、`book_count=11`、`library_version=2026.07.29-16`、`progress_storage_changed=false`。
- 已知工程技債：最新 run 的最後 `Record successful deployment` 仍因舊 checkpoint 字串匹配器失敗，使 workflow overall conclusion 顯示 `failure-after-successful-pages-deploy`；教材產生、正式 QA、artifact upload 與 Pages deployment 均已先成功，正式 receipt 已依最新 artifact 與 deploy log 校正。下一本正式新教材發布前應修正 recorder。

## 正式規格與讀取順序

1. `AGENTS.md`：最高層執行規則。
2. `docs/project_knowledge_index.md`：新對話與新任務必讀順序。
3. `docs/content_authoring_spec.md`：教材、題庫、圖解與 QA 規格。
4. `docs/concurrent_book_workflow.md`：多書可平行製作、共同書庫必須序列發布的規則。
5. 本 checkpoint：目前正式書庫狀態。
6. 目標科目的 `scope.md`、`qa_report.md`、`status.md`。

固定原則：

- 科目本位：使用者的主修背景只決定程度、先備知識與可能範圍，不得主導其他科目的正文、案例與題型。
- 跨科內容只有在標準課程本來包含、理解不可或缺或使用者明確要求時才可進入；其他內容列為延伸。
- 新科目先固定 scope，再製作內容；至少完成兩輪 QA 後才可進入正式整合。
- 不同科目的內容製作／QA 可平行；共同 PWA 整合與 Pages 發布必須序列化。
- 發布前必須重新讀最新 `main`、本 checkpoint、書庫 registry 與 deployment receipt，禁止拿舊 artifact 覆蓋較新的正式書庫。
- 正式成功以 canonical 產生／驗證、Pages artifact、Pages deployment 與 deployment receipt 為準；merge 成功本身不等於已部署。
- 既有章節 ID、題目 ID、儲存鍵與閱讀／錯題進度不得無故破壞。

## 正式已部署書籍

### 1. 大一微積分
- Book ID：`calculus`
- 正式內容版本：`2026.07.27-3`
- 題庫 73 題；本版 QA 181／181 通過。
- 狀態：已部署。

### 2. 會計學
- Book ID：`accounting`
- 正式內容版本：`2026.07.27-2`
- 成品：14 章、3 附錄、70 題、111 搜尋、13 圖解。
- 二次獨立複核修正 29 個內容點，70 題數值答案重算通過。
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
- 發布後二次複核 1,616 項，15 題量化重算、20 題高風險觀念重判。
- 狀態：已部署。

### 8. 中級會計學
- Book ID：`intermediate-accounting`
- 正式內容版本：`2026.07.29-2`
- 成品：22 章、3 附錄、110 題、145 搜尋、22 圖解。
- 發布後二次內容審計 1,110 項，28 項量化重算。
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
- 定位：一般大學國際經濟學，分為國際貿易與國際金融／開放經濟兩大主線。
- 成品：20 章、3 附錄、100 題、144 搜尋、20 圖解。
- 初版 QA：696／696 與 1,383／1,383；17 題量化題重算。
- 發布後第二次內容複核：修正 11 個內容節點，精確化 7 題；100 題全數重查，17 題量化題再由原始輸入重算，沒有數值答案需要更改。
- v2 獨立 QA：1,656／1,656 通過。
- 主要修正：H–O 定理群條件、獨占性競爭品種／廠商數、傾銷定義、關稅／出口補貼福利、BPM7 金融帳符號、CIP／PPP 條件、Marshall–Lerner／J 曲線、Bretton Woods 官方美元兌金範圍。
- 正式部署 run：`30452678302`；Source commit：`24bcf00d73dcb2e11b4d2dfbce14c5e99b5db85d`。
- 章節 ID、題目 ID、題數與儲存鍵不變，既有閱讀進度與錯題紀錄可沿用。
- 文件：`docs/books/international-economics/scope.md`、`docs/books/international-economics/qa_report.md`、`docs/books/international-economics/status.md`
- 狀態：已部署。

### 11. 財政學
- Book ID：`public-finance`
- 正式內容版本：`2026.07.29-2`
- 定位：一般大學財政學／公共經濟學。
- 成品：20 章、3 附錄、100 題、189 搜尋、20 圖解。
- 發布後獨立內容審計：16 個修正／補強區域；2,386 項結構／內容 gate、174 項 v2 獨立 gate、38 項量化重算通過。
- 最新正式 Pages run 同為 `30452678302`；財政學 v2 在同一序列中先完成，再由國際經濟學 v2 形成最終 `2026.07.29-16` artifact。
- 章節 ID、題目 ID 與題數不變，既有閱讀進度與錯題紀錄可沿用。
- 文件：`docs/books/public-finance/scope.md`、`docs/books/public-finance/qa_report.md`、`docs/books/public-finance/status.md`
- 狀態：已部署。

## Canonical 部署流程

1. 從正式基礎網站 artifact 開始，先驗證既有書庫與版本。
2. 依 canonical `Deploy study library` 既定順序套用既有書籍修正層並逐書驗證。
3. 新增或修正版教材只可接在當下最新正式尾端，且必須確認所有既有 Book ID、內容版本與進度相容性未倒退。
4. 各書內容／題庫／搜尋／SVG 與高風險公式／法律要件驗證通過後，再檢查 `app.js` 與 `sw.js`。
5. 全部正式檢查通過後才上傳單一完整 Pages artifact。
6. Pages deployment 成功後核對 artifact，再寫回 deployment receipt、各書 status／QA 與本 checkpoint。
7. 最新正式書庫：11 本，`2026.07.29-16`；Pages run `30452678302`，artifact `8724164394`。
8. 使用者不需要執行 Git、終端機、手動上傳或部署。

## 多書並行／發布規則

- 內容製作與 QA 可平行；發布依 `docs/concurrent_book_workflow.md` 序列化。
- 每條準備發布的工作線都要在最後一刻重新同步最新 `main`，重新確認正式書籍清單與版本。
- workflow concurrency 造成 cancelled 不視為內容失敗；不可用舊 SHA 覆蓋最新 main。
- generator／artifact integrity gate 失敗必須先定位根因，不得關閉 gate 或盲目重跑。
- canonical post-deploy recorder 目前仍依賴舊 checkpoint 標題／句子格式；下一本正式新教材發布前必須修正並驗證。

## 下一個新科目流程

1. 使用者只需指定科目，無須重貼歷史規格。
2. 助理先讀 `AGENTS.md`、knowledge index、content authoring spec、concurrent workflow 與本 checkpoint。
3. 先修正／驗證 canonical post-deploy recorder 的現行 checkpoint 相容性。
4. 建立 `docs/books/<book-id>/scope.md` 與 `status.md`，固定科目邊界。
5. 依標準本科課程製作教材、圖解、題庫、搜尋資料；必要時用可信官方／大學來源交叉核對。
6. 完成兩輪獨立 QA，特別重算數值題並設高風險負面 gate。
7. 發布前重新同步最新 main；確認其他平行教材是否已先正式發布。
8. 依 canonical workflow 加入同一 PWA；只有 Pages artifact／deployment 與 deployment receipt 均核實後才標記「已部署」。
9. 同步更新該書 status、QA report、README、deployment receipt 與本 checkpoint，任務才算收尾。
