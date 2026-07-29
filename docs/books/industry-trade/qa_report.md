# 《產業及貿易》QA 報告

更新日期：2026-07-29
內容版本：`2026.07.29-1`
狀態：本地兩輪候選 QA 已通過；GitHub candidate workflow 與正式部署驗證待完成。

## 第一輪：製作內檢

本地以正式 12 本 Pages artifact 的乾淨副本生成候選後執行。

- 結果：`INDUSTRY_TRADE_QA_ROUND1_OK`
- 檢查數：1,591
- 正文：20／20
- 附錄：3／3
- 題庫：100／100；每章 5 題；題目 ID 唯一。
- 搜尋：160／160；每章 8 筆。
- SVG：20／20，具 `viewBox`、`title`、`desc` 與本地資產路徑。
- 題庫 schema：必要欄位、難度、Book ID、章節 ID 全部通過。
- 章節結構：白話直覺、正式概念、公式條件、完整例題、常見錯誤、考試判斷與理解檢查均存在。
- PWA：候選 cache 路徑存在；`app.js`、`sw.js` 語法檢查通過。
- 相容性：既有 12 本教材目錄 SHA-256 在候選生成前後逐書一致。

### 第一輪實際修正

1. 修正附錄 A／B 在 glossary 迴圈中被區域變數覆蓋，避免附錄內容只剩單一字串。
2. 將勞動需求公式由含混的 `MRPL=MRP_L` 改為 `MRPL=MR×MPL`，並把 `w=MRPL` 明定為競爭勞動市場、內點解與利潤極大下的條件。
3. 修正三處 LaTeX 文字間距字串的 Python escape warning。
4. 擴充附錄 A／B，使模型條件、福利帳與解題順序可獨立閱讀。
5. 寡占章明示 Cournot／Bertrand／Stackelberg 結論不可直接互換。
6. 反傾銷章補強重大損害（material injury）與因果關係邊界。
7. 區域整合章的機制題補明貿易創造與貿易轉向。

## 第二輪：獨立複核

使用獨立 QA 程式，不沿用第一輪的通過條件。

- 結果：`INDUSTRY_TRADE_QA_ROUND2_OK`
- 檢查數：545
- 題庫逐題：100／100 重新檢查題幹、答案與必要詳解。
- 數值題：20／20 由原始數值獨立重算。
- 高風險章節：12 章重新判讀模型條件與負面 gate。
- 搜尋索引：確認高風險修正內容已同步，無簡化過頭的舊敘述。

### 20 個獨立重算節點

HHI、Lerner 指標、Cournot 最佳回應、CES markup、平均成本與規模、出口固定成本門檻、關稅價格／收入、策略性補貼福利帳、垂直整合獨占量價、外包總成本、FDI 臨界銷量、固定費／權利金、簡化傾銷差額、平行貿易套利、範疇經濟、Nash 議價、MRPL、研發期望報酬、Pigouvian 稅、貿易轉向真實資源成本。

## 外部精確性核對

反傾銷相關高風險內容以 WTO 公開技術說明與 Anti-Dumping Agreement 摘要交叉核對：正常價值與出口價格的公平比較用於傾銷判定；採取反傾銷措施還需確認國內產業重大損害與傾銷進口之因果關係。本書不提供個案法律意見。

## 尚待完成

1. GitHub candidate workflow 必須從執行當下最新成功 Pages artifact 重建候選並重跑兩輪 QA。
2. 正式發布前重新同步最新 `main` 與 shared checkpoint；若其他平行教材先發布，重新整合而非使用舊基底。
3. 正式共同書庫部署後，核對 Pages artifact、deployment receipt、書籍數、版本與 progress storage，再更新本報告為正式發布版。

## 正式發布結果

- Round 1：1495 項通過；Round 2：545 項通過。
- 100 題逐題複核、20 題數值題獨立重算、12 個高風險章節重新判讀。
- 既有 19 本內容 hash：整合前後完全一致。
- 正式書庫：20 本，版本 `2026.07.30-6`。
- Pages run：`30490197263`。
- Pages artifact：`8739358772`；digest `sha256:6936173acc641daef1c2e369a09407f2ee4533499735b78f5cbb280a147440ce`。
- 部署後 artifact 重抓：23 份本書 HTML、100 題、160 搜尋、20 SVG 全數核對通過。
- post-deploy recorder：`passed-structured-recorder`。
