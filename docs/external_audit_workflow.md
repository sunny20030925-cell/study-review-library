# External Audit 與 Visual Polish 正式工作流

更新日期：2026-07-30

本文件定義教材在既有 Draft 與兩輪 Internal QA 之後的新正式階段。GitHub `main` 仍是唯一正式進度來源；聊天記憶、外掛歷史或本機副本不得取代 repo 狀態。

## 一、正式階段

每一本書的標準流程固定為：

`Draft → Internal QA → External Audit → Visual Polish → Published`

階段代碼：

- `DR`：Draft
- `IQ`：Internal QA（包含既有第一輪製作內檢＋第二輪獨立複核）
- `EA`：External Audit
- `VP`：Visual Polish
- `PUB`：Published

Task ID 格式：`<book-id>:<stage-code>`，例如 `advanced-statistics:EA`。每個 status／manifest 項目都要同時記錄 `current_stage`、`task_id` 與 `next_stage`。

## 二、External Audit 原則

External Audit 不是第三次全量重做 Internal QA，而是「風險式外部驗證」。目標是把免費外部額度集中在最可能造成實質錯誤、且外部工具真正能提高可信度的內容。

### 必查高風險內容

優先抽查：

1. 核心公式、數值答案、統計推導、邊界條件、特殊案例。
2. 容易因版本／時間改變的法律、會計準則、政策或制度性敘述。
3. 實證研究結論、學術爭議、因果推論與重要文獻主張。
4. 重要論文被支持、反駁或重新解釋的引用脈絡。
5. Internal QA 曾經修正過、條件特別多、或錯誤成本高的區域。

### 不應浪費外部額度的內容

一般定義、低風險基礎敘述、已由可靠正式來源直接確認且沒有爭議的常識型內容，不必為了「第三輪 QA」逐句送外部工具。

## 三、依內容類型路由

### 數學／公式／數值／統計推導

- 優先：Wolfram。
- 用途：代數化簡、微積分、方程、機率分配、數值答案、矩陣、最佳化與可形式化的統計推導。
- 若工具只能驗算數值而不能證成敘述條件，仍須保留人工條件審查。

### 實證研究、學術爭議、研究結論

- 優先：Consensus。
- 用途：確認研究結論是否有同儕審查文獻支持、結論是否過度概括、是否存在重要相反結果。

### 重要論文的支持／反駁／引用脈絡

- 使用：Scite。
- 用途：檢查重要引用是支持、反駁或僅背景引用，避免把單篇論文寫成已形成共識。

### 法律

- 第一順位：正式法規、主管機關官方資料、正式判決／憲法法庭資料與必要修法沿革。
- Consensus／Scite 不得取代正式法律來源。
- 若學術資料與正式法源衝突，以現行有效正式法源為準，並記錄適用日期。

### 會計

- 第一順位：正式準則、主管機關／準則制定機構之規範與正式解釋。
- Wolfram 僅用於計算驗證，不得用來決定會計認列、衡量、表達或揭露規範。

### 其他技術／制度內容

- 優先官方技術文件、標準文件或第一手來源。
- 只有涉及研究證據時才使用 Consensus／Scite。

## 四、風險式抽查與通過門檻

每本書 External Audit 至少要建立一份可重現的 audit record，記錄：

- 抽查範圍與抽樣理由。
- 使用的外部來源／工具與日期。
- 通過、修正、無法驗證的項目。
- 任何內容修正與對應 content version。
- Book ID、chapter ID、question ID 是否保持相容。

通過條件：

1. 所有被列為「高風險必查」的抽樣項目已完成。
2. 未留下會改變核心答案的 unresolved blocker。
3. 若有內容修正，已重新執行受影響的 Internal QA gate。
4. 沒有破壞既有 Book ID、chapter ID、question ID、閱讀進度、錯題資料或 PWA 相容性。

## 五、Visual Polish

只有 External Audit 通過後才進入 `VP`。

Canva 僅用於高價值視覺資產，例如：

- 封面。
- 章末重點整理。
- 比較圖、流程圖。
- 公式速查表、考前速查表。

禁止把整本教材搬離現有 PWA 架構。正文、題庫、搜尋、閱讀進度與錯題資料仍以既有 PWA 為正式載體。

Visual Polish 必須保持：

- Book ID／chapter ID／question ID 不變。
- 既有資料結構與 progress storage key 不變。
- 視覺資產可在平板正常閱讀、放大與離線載入。

## 六、既有 21 本的遷移規則

21 本教材在本工作流建立前已正式發布，不得因新增階段而取消或破壞既有發布。

遷移方式：

- `DR`：既有 21 本均視為 passed。
- `IQ`：既有 21 本均已有兩輪 QA 證據，視為 passed。
- `PUB`：既有 21 本維持 passed，並標記 `legacy_published_before_workflow_v2=true`。
- `EA`：只有具有足以符合本文件的新制外部證據者可遷移為 passed；其餘一律 pending，不得回填假通過。
- `VP`：尚未依本文件正式執行者為 pending。

目前《商事法》與《民法概要》已有以現行正式法規、官方資料／判決為核心的獨立法律複核，可遷移為 `EA=passed_migrated`；其餘 19 本進入 External Audit queue。

## 七、Machine-readable 狀態與自動選下一本

全書庫正式 machine-readable 入口：`docs/audit_progress_manifest.json`。

新對話開始 External Audit 時：

1. 先讀 `AGENTS.md`、knowledge index、本文件與 manifest。
2. 驗證 manifest 的 `book_count=21` 與正式 deployment receipt／registry 一致。
3. 直接取 `external_audit_queue[0]` 作為下一本，不要求使用者記憶或重貼先前內容。
4. 若 queue 第一項已被其他正式 commit 標為 passed／in_progress，重新讀最新 `main` 後取下一項。
5. 完成後更新該書 status、audit record、manifest；shared checkpoint 只更新總數與下一本。

## 八、External Audit 與共同發布的關係

- External Audit 與 Visual Polish 可在不同書籍工作線上準備，但共同 PWA 寫入與 Pages 部署仍依 `docs/concurrent_book_workflow.md` 序列化。
- 正式內容修正若需要重新發布，必須從當下最新正式 artifact 整合，不得重播過時 generator 鏈覆蓋較新的書庫。
- External Audit 本身不得一次硬跑完全部 21 本；以 manifest queue 逐本推進並保留外部免費額度。
