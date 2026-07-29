# 重點複習書庫 Shared Checkpoint

更新日期：2026-07-29

## 書庫

- Repo：`sunny20030925-cell/study-review-library`
- 預設分支：`main`
- 固定入口：`https://sunny20030925-cell.github.io/study-review-library/`
- 形式：平板直式 PWA 書庫，可持續加入新科目。
- 使用者操作限制：只使用平板；不得要求終端機、Git、電腦檔案管理、手動部署或多檔案上傳操作。
- 正式書庫內容版本：`2026.07.29-14`
- 正式書籍數：11 本。
- 最新正式 Pages 部署 run：`30443143611`。
- 最新正式部署 source commit：`6babc326c5f8ae3ceed363466248c50c51ceecd6`。
- Pages 狀態：Upload artifact 與 Deploy to GitHub Pages 均成功；Pages 於 `2026-07-29T10:18:44.896999+00:00` 回報成功。
- 部署回條：`docs/deployment_receipt.json`；`status=success`、`book_count=11`、`library_version=2026.07.29-14`、`progress_storage_changed=false`。
- 已知工程瑕疵：Run `30443143611` 在 Pages 成功後的 `Record successful deployment` 步驟因舊 checkpoint 字串匹配器失敗，因此 workflow overall conclusion 為 failure-after-successful-pages-deploy；正式 artifact 與網站內容不受影響，deployment receipt 已依 artifact 與 deploy log 以 `[skip ci]` 校正。下一次新增教材正式發布前，應先修正這個 post-deploy recorder。

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
- 定位：標準大一微積分；不採經濟學取向。
- 題庫：73 題。
- QA：本版 181／181 項通過。
- QA 報告：`docs/books/calculus/qa_report.md`
- 狀態：已部署。

### 2. 會計學

- Book ID：`accounting`
- 正式內容版本：`2026.07.27-2`
- 定位：一般大學第一門會計學／基礎財務會計；不延伸至中級會計以上，也不混入成本／管理會計主體。
- 成品：14 章、3 附錄、70 題題庫、111 筆搜尋索引、13 張圖解。
- 二次獨立複核修正 29 個內容點；70 題數值答案重新驗算通過。
- 文件：`docs/books/accounting/scope.md`、`docs/books/accounting/qa_report.md`
- 狀態：已部署。

### 3. 經濟學原理

- Book ID：`economics`
- 正式內容版本：`2026.07.27-2`
- 定位：一般大學第一門經濟學／經濟學原理，涵蓋個體與總體共同核心。
- 成品：20 章、3 附錄、100 題題庫、144 筆搜尋索引、20 張圖解。
- 初版兩輪 QA：1,557／1,557、895／895；發布後複核 1,333／1,333，並完成 14 處正文／附錄修正與 6 題同步修正。
- 文件：`docs/books/economics/scope.md`、`docs/books/economics/qa_report.md`
- 狀態：已部署。

### 4. 統計學

- Book ID：`statistics`
- 正式內容版本：`2026.07.29-2`
- 定位：一般大學第一門統計學／基礎統計學。
- 成品：19 章、3 附錄、95 題、169 筆搜尋索引、19 張圖解。
- 發布後獨立二次校錯：1,195／1,195；44 個計算／公式判斷另行重算／重判。
- 文件：`docs/books/statistics/scope.md`、`docs/books/statistics/qa_report.md`
- 狀態：已部署。

### 5. 商事法

- Book ID：`commercial-law`
- 正式內容版本：`2026.07.29-2`
- 定位：一般大學商事法入門與考試重點整理，以公司法＋證券交易法為核心。
- 成品：18 章、3 附錄、90 題、111 筆搜尋索引、18 張圖解，另有法條速查入口。
- 發布後獨立內容複核與公司法第 8 條現行法 follow-up 已完成；舊法版本混用已回修。
- 文件：`docs/books/commercial-law/scope.md`、`docs/books/commercial-law/qa_report.md`
- 狀態：已部署。

### 6. 成本會計學

- Book ID：`cost-accounting`
- 正式內容版本：`2026.07.29-2`
- 定位：一般大學成本會計／成本與管理會計課程中的成本會計主體。
- 成品：19 章、3 附錄、95 題、150 筆搜尋索引、19 張圖解。
- 發布後二次內容審計：857／857；95 題全數重查，44 個數值答案由原始輸入重算。
- 文件：`docs/books/cost-accounting/scope.md`、`docs/books/cost-accounting/qa_report.md`
- 狀態：已部署。

### 7. 個體經濟學

- Book ID：`microeconomics`
- 正式內容版本：`2026.07.29-2`
- 定位：一般大學中級個體經濟學。
- 成品：20 章、3 附錄、100 題、154 筆搜尋索引、20 張圖解。
- 發布後獨立二次複核：1,616 項通過；15 題量化題獨立重算、20 題高風險觀念題獨立重判。
- 文件：`docs/books/microeconomics/scope.md`、`docs/books/microeconomics/qa_report.md`
- 狀態：已部署。

### 8. 中級會計學

- Book ID：`intermediate-accounting`
- 正式內容版本：`2026.07.29-2`
- 定位：一般大學中級會計學，聚焦 IFRS／TIFRS 下的認列、衡量、表達、分錄與財務報導判斷。
- 成品：22 章、3 附錄、110 題、145 筆搜尋索引、22 張圖解。
- 發布後二次內容審計：1,110 項獨立檢查、28 項量化重算全數通過。
- 文件：`docs/books/intermediate-accounting/scope.md`、`docs/books/intermediate-accounting/qa_report.md`
- 狀態：已部署。

### 9. 總體經濟學

- Book ID：`macroeconomics`
- 正式內容版本：`2026.07.29-2`
- 定位：一般大學總體經濟學，聚焦總體衡量、長期成長、短期景氣、財政貨幣政策與開放經濟。
- 成品：20 章、3 附錄、100 題、143 筆搜尋索引、20 張圖解。
- 發布後第二次獨立複核：201／201；14 個內容修正事件、7 題題庫調整、20 題量化題重新驗算。
- 文件：`docs/books/macroeconomics/scope.md`、`docs/books/macroeconomics/qa_report.md`
- 狀態：已部署。

### 10. 國際經濟學

- Book ID：`international-economics`
- 正式內容版本：`2026.07.29-1`
- 定位：一般大學國際經濟學，分為國際貿易與國際金融／開放經濟兩大主線。
- 核心：比較利益、Specific Factors、Heckscher–Ohlin、貿易條件、規模經濟、異質廠商、關稅／配額、WTO／區域整合、國際收支、外匯、CIP／UIP、PPP、匯率超調、DD–AA、固定匯率、國際貨幣制度、不可能三角與金融危機。
- 成品：20 章、3 附錄、100 題題庫、144 筆搜尋索引、20 張自製圖解。
- 第一輪 QA：696／696；17 題數值答案重算。
- 第二輪獨立複核：1,383／1,383；100 題逐題重查，17 題量化題由原始輸入獨立重算。
- 正式 Pages artifact 終檢：10 本書完整；本書 23 份章節／附錄、100 題、144 搜尋、20 SVG 全部存在，離線快取已包含本書。
- 正式部署 run：`30442682452`。
- Source commit：`00cf9286eb7bbe3b2d8e2b6165cc163fd64a4e72`。
- 文件：`docs/books/international-economics/scope.md`、`docs/books/international-economics/qa_report.md`、`docs/books/international-economics/status.md`
- 狀態：已部署。

### 11. 財政學

- Book ID：`public-finance`
- 正式內容版本：`2026.07.29-1`
- 定位：一般大學財政學／公共經濟學，核心涵蓋公共支出與市場失靈、分配與社會保險、租稅理論與主要稅目、地方財政與政府債務。
- 成品：20 章、3 附錄、100 題題庫、189 筆搜尋索引、20 張自製圖解。
- 第二輪內容與題庫複核：20／20 章、100／100 題重新檢查；40 個高風險答案固定重查，數值題另由原始輸入重算。
- 最新 10 書 canonical-tail preflight：Run `30443068402`；財政學 2,383 項 validator 檢查與總經 tail 265 項 QA 通過，原 10 本教材雜湊不變。
- 正式 Pages artifact 終檢：11 本書完整；書庫版本 `2026.07.29-14`；本書 23 份章節／附錄、100 題、189 搜尋、20 SVG 全部存在，離線快取已包含本書。
- 正式部署 run：`30443143611`；Pages 部署步驟成功。
- Source commit：`6babc326c5f8ae3ceed363466248c50c51ceecd6`。
- Artifact：`8720289195`；digest `sha256:4193fede294a374210549df3e71161681e63b654956c1207a38d0f5112803215`。
- 文件：`docs/books/public-finance/scope.md`、`docs/books/public-finance/qa_report.md`、`docs/books/public-finance/status.md`
- 狀態：已部署。

## Canonical 部署流程

1. 從正式基礎網站 artifact 開始，先驗證既有書庫與版本。
2. 依 canonical `Deploy study library` 既定順序套用既有書籍修正層並逐書驗證。
3. 新增書籍只可接在當下最新正式尾端，且必須確認所有既有 Book ID、內容版本與進度相容性未倒退。
4. 各書內容／題庫／搜尋／SVG 與高風險公式／法律要件驗證通過後，再檢查 `app.js` 與 `sw.js`。
5. 全部正式檢查通過後才上傳單一完整 Pages artifact。
6. Pages 部署成功後才寫回 `docs/deployment_receipt.json` 與各書 status／QA／本 checkpoint。
7. 最新正式書庫：11 本，`2026.07.29-14`；Pages deployment run `30443143611`，artifact `8720289195`。
8. Run `30443143611` 的 Pages 部署本身成功，但舊 post-deploy recorder 在之後寫 repo 文件時失敗；已依部署 log 與 artifact 手動校正 receipt。此 recorder 必須在下一次正式新增教材前修正。
9. 使用者不需要執行 Git、終端機、手動上傳或部署。

## 多書並行／發布規則

- 內容製作與 QA 可平行；發布要依 `docs/concurrent_book_workflow.md` 序列化。
- 每條準備發布的工作線都要在最後一刻重新同步最新 `main`，重新確認正式書籍清單與版本。
- 另一條工作線只新增候選 source／QA，不代表已取得正式書庫發布順位；不得把候選書計入正式 book count。
- workflow concurrency 造成 cancelled 不視為內容失敗；但不可直接以舊 SHA 覆蓋最新 main，必須從最新 main 重新觸發 canonical deploy。
- 任何 generator／artifact integrity gate 失敗都必須先定位根因，不得關閉 gate 或盲目重跑。
- 已知 post-deploy recorder 目前仍依賴舊 checkpoint 標題／句子格式；下一本正式發布前先修 recorder，再進入新的 canonical publish。

## 下一個新科目流程

1. 使用者只需指定科目，無須重貼歷史規格。
2. 助理先讀 `AGENTS.md`、knowledge index、content authoring spec、concurrent workflow 與本 checkpoint。
3. 先修正／驗證 canonical post-deploy recorder 的現行 checkpoint 相容性；不得等到 Pages 部署後才發現寫回器仍用舊格式。
4. 建立 `docs/books/<book-id>/scope.md` 與 `status.md`，固定科目邊界。
5. 依標準本科課程製作教材、圖解、題庫、搜尋資料；必要時用可信官方／大學來源交叉核對。
6. 完成兩輪獨立 QA，特別重算數值題並設高風險負面 gate。
7. 發布前重新同步最新 main；確認其他平行教材是否已先正式發布。
8. 依 canonical workflow 加入同一 PWA；只有 Pages artifact／deployment 與 deployment receipt 均核實後才標記「已部署」。
9. 同步更新該書 status、QA report、README、deployment receipt 與本 checkpoint，任務才算收尾。
