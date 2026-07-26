# 重點複習書庫 Shared Checkpoint

更新日期：2026-07-27

## 書庫

- Repo：`sunny20030925-cell/study-review-library`
- 預設分支：`main`
- 固定入口：`https://sunny20030925-cell.github.io/study-review-library/`
- 形式：平板直式 PWA 書庫，可持續加入新科目。
- 使用者操作限制：只使用平板；不得要求終端機、Git、電腦檔案管理、手動部署或多檔案上傳操作。
- 目前書庫內容版本：`2026.07.27-5`

## 正式規格

- `AGENTS.md`：最高層執行規則。
- `docs/project_knowledge_index.md`：新對話與新任務的必讀順序。
- `docs/content_authoring_spec.md`：教材、題庫、圖解與 QA 規格。
- 新任務必須先讀取上述文件與本 checkpoint。
- 科目本位原則已固定：使用者的主修背景只決定程度、先備知識與可能範圍，不得主導其他科目的正文、案例與題型。
- 跨科內容只有在標準課程本來包含、理解不可或缺或使用者明確要求時才可進入；其他內容只能列為選讀／延伸。

## 已有書籍

### 大一微積分

- Book ID：`calculus`
- 正式內容版本：`2026.07.27-3`
- 定位：標準大一微積分；不再採經濟學取向。
- 核心內容與 73 題題庫已完成科目本位重整。
- 已補入或強化：中值定理、洛必達法則、積分幾何應用、弧長、旋轉曲面、多變數微積分與純數學限制最佳化。
- 已移除核心中的成本、收益、彈性、消費者剩餘、效用與現值等經濟學專屬內容。
- 本版 QA：181 項檢查，181 項通過。
- QA 報告：`docs/books/calculus/qa_report.md`
- 狀態：已部署。

### 會計學

- Book ID：`accounting`
- 正式內容版本：`2026.07.27-1`
- 定位：一般大學第一門會計學／基礎財務會計；書名維持《會計學》。
- 範圍：交易分析、借貸分錄、會計循環、調整與結帳、財務報表、買賣業、存貨、現金、應收款項、折舊、負債與權益、現金流量與基礎財報分析。
- 深度邊界：不延伸至中級會計以上，也不混入成本或管理會計課程。
- 成品：14 章、3 附錄、70 題題庫、111 筆搜尋索引、13 張自製圖解。
- 第一輪 QA：233 項檢查，233 項通過。
- 第二輪 QA：內容邊界、版本、HTML、JSON、JavaScript、連結、題庫分布、快取與靜態載入全數通過。
- 範圍文件：`docs/books/accounting/scope.md`
- QA 報告：`docs/books/accounting/qa_report.md`
- 部署回條：`docs/deployment_receipt.json`
- 狀態：已合併至 `main` 並完成 GitHub Pages 正式部署。

### 經濟學原理

- Book ID：`economics`
- 正式內容版本：`2026.07.27-1`
- 定位：一般大學第一門經濟學／經濟學原理，完整涵蓋個體與總體共同核心。
- 範圍：選擇與機會成本、比較利益、供需與彈性、福利與政策、消費者與企業、市場結構、要素市場、市場失靈、GDP 與失業、成長、金融、AD–AS、乘數、財政貨幣政策與開放經濟。
- 深度邊界：不延伸至中級個體、中級總體、計量經濟或專門領域課程。
- 成品：20 章、3 附錄、100 題題庫、144 筆搜尋索引、20 張自製圖解。
- 第一輪 QA：1,557／1,557 通過。
- 第二輪 QA：895／895 通過；另完成 52 個靜態 HTTP 路徑、JavaScript、SVG 預覽與 ZIP 完整性檢查。
- 範圍文件：`docs/books/economics/scope.md`
- QA 報告：`docs/books/economics/qa_report.md`
- 狀態：內容與 QA 完成；合併至 `main` 後由 GitHub Pages 自動部署。

## 部署流程

1. GitHub Actions 下載固定 ID 的正式網站部署包。
2. 先核對部署包 SHA-256，再用 Python ZIP 模組解開；部署包可含前置檔頭，不依賴桌面解壓工具。
3. 驗證三本書的 manifest、題庫數量、章節檔、搜尋索引、經濟學圖解與 PWA 快取。
4. JavaScript 語法與全部正式檢查通過後，才上傳 Pages artifact。
5. Pages 部署成功後寫回 `docs/deployment_receipt.json`，失敗時不會產生成功回條。
6. 使用者不需要在平板上處理 ZIP、Git 或部署。

## 下一個新科目流程

1. 建議新開對話，避免不同書籍的章節、題庫與 QA 進度混淆。
2. 使用者只需指定科目，無須重貼歷史規格。
3. 助理必須先從本 repo 讀取：
   - `AGENTS.md`
   - `docs/project_knowledge_index.md`
   - `docs/content_authoring_spec.md`
   - `docs/shared_checkpoint.md`
4. 先建立該科目的 `scope.md` 與 `status.md`，固定科目邊界後再開始製作。
5. 完成兩輪 QA 後，加入同一個 PWA 書庫並更新本 checkpoint。

## 建議的新對話開頭

> 下一本製作「科目名稱」。請先從 `sunny20030925-cell/study-review-library` 讀取 `AGENTS.md`、knowledge index 與目前 checkpoint，再依正式規格開始。

同一科目的糾錯、補充與題庫擴充留在該科目的對話；書庫介面、部署與全站規格留在書庫維護對話。
