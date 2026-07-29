# 《賽局理論及應用》QA 報告

更新日期：2026-07-29

## 目前狀態

- 內容版本：`2026.07.29-1` 候選版。
- 第一輪製作內檢：內容來源、100 題題庫、產生器與獨立 validator 已建立；等待 GitHub Actions 候選驗證回條。
- 第二輪獨立複核：尚未執行。
- 正式部署：尚未執行。

因此本書目前仍是候選版，不能宣稱已完成兩輪校對或正式發布。

## 第一輪驗證範圍

候選 workflow 將獨立檢查：

1. 20 章、3 附錄、100 題、189 筆搜尋與 20 張 SVG 的結構完整性。
2. 每章固定 5 題，題目 ID 唯一，difficulty 分布為基礎 20、標準 40、綜合 20、陷阱 20。
3. 所有章節包含白話直覺、正式定義、公式／條件、完整例題、常見錯誤、考試判斷與理解檢查。
4. 核心範圍涵蓋 best response、dominance、Nash、mixed strategy、minimax、Cournot／Bertrand、backward induction、SPNE、bargaining、repeated games、BNE、auctions、PBE、signaling、screening、cheap talk、mechanism design、VCG、core 與 Shapley value。
5. 34 個高風險數值／均衡答案以固定 expected answer gate 重新核對。
6. 禁止把 Nash 等同效率、把 weak dominance 當成順序無關、把 minimax 泛化到所有賽局、把第二價誠實出價泛化到所有資訊環境等典型過度敘述。
7. 20 張 SVG 皆需有 `title`、`desc`、`viewBox`，且不得依賴遠端圖片。
8. 共同 PWA 的 `app.js`、`sw.js` 語法與新書離線快取路徑必須有效。
9. 候選產生前後，所有既有書籍逐檔 SHA-256 必須完全一致。

## 第二輪獨立複核規劃

第一輪通過後，第二輪會另外重做而不是只重跑同一個 validator：

- 逐章重新核對核心定義與解概念適用條件。
- 重算混合策略、零和、Cournot、Rubinstein、重複賽局折現、Bayes 更新、拍賣、訊號、screening、VCG 與 cooperative-game 數值節點。
- 逐題重新判斷 100 題答案與詳解，特別檢查 Nash／SPNE／BNE／PBE 混稱、on-path／off-path belief、finite／infinite repetition、private／common value 等高風險區域。
- 檢查章節之間符號、策略／行動用語、payoff 順序與機率定義是否一致。
- 抽查平板直式閱讀、章節切換、搜尋、題庫、錯題紀錄與離線資產。

## 已知限制

- 均衡存在的 fixed-point proof、高階 equilibrium refinement、Myerson optimal auction、完整 implementation theory、algorithmic game theory 等維持選讀／範圍外，不進核心題庫。
- 應用案例只用來說明賽局結構，不取代個體經濟學、產業組織、財務或政治學專門課程。
