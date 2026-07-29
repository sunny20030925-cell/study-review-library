# 《數理經濟學》QA 報告

更新日期：2026-07-29

## 版本與成品目標

- Book ID：`mathematical-economics`
- 內容版本：`2026.07.29-1`
- 正文：20 章。
- 附錄：3 份。
- 題庫：100 題，每章 5 題。
- 搜尋索引：150 筆。
- 自製 SVG：20 張。

## 第一輪：結構與內容完整性

自動 gate 驗證：

- 20 章與 3 附錄檔案完整，每章均包含問題、白話直覺、正式定義、核心公式與成立條件、完整例題、常見錯誤、考試判斷方法與理解檢查。
- 線性代數、微積分、隱函數比較靜態、彈性、Hessian、Lagrange、KKT、包絡定理、Euler 定理、積分與一階離散／連續動態均有正式覆蓋。
- 100 題題庫 ID 唯一且每章固定 5 題；150 筆搜尋資料全部指向有效章節／附錄。
- 20 張 SVG 必須具備 `title`、`desc`、`viewBox`，不得依賴遠端圖片。
- Service Worker 必須包含本書 manifest、questions、search、章節與 SVG 路徑。
- 導數 prime 的 MathJax 輸出不得殘留 `\\'` 形式，避免被誤判成重音命令。

## 第二輪：獨立重算與高風險邏輯

獨立重算涵蓋：

- 聯立均衡、矩陣乘法、determinant 與反矩陣解。
- 導數、Taylor 近似、偏導數、全微分與隱函數比較靜態。
- 彈性、一元／多元最佳化、Hessian 定號。
- 等式限制 Lagrange、KKT 邊界與互補鬆弛。
- 包絡定理、齊次函數與 Euler 定理。
- 邊際量積分回總量、離散複利與連續成長率轉換。
- 一階差分與微分方程的穩態、震盪與穩定性。

高風險負面 gate：

- `FOC=0` 不得被寫成自動充分的最大值條件。
- Hessian 不得只憑主對角元素符號就判定正／負定。
- 比較靜態不得誤寫成時間動態。
- Lagrange multiplier 的符號解讀必須與 Lagrangian 慣例一致。
- KKT 不得在缺乏凹凸性等條件時被宣稱自動充分。
- 定積分不得無條件等同幾何面積。
- 差分方程穩定性必須檢查 `|b|<1`，不能只檢查 `b<1`。
- 微分方程穩態令 `ẋ=0`，不是令狀態變數本身等於 0。

## 整合 gate

- 數理經濟學只接受 14 本且尾端為 `advanced-statistics → computer-fundamentals` 的正式 artifact。
- 整合完成後必須形成 15 本書庫，尾端為 `advanced-statistics → computer-fundamentals → mathematical-economics`。
- 整合前後逐本計算既有 14 本教材內容 SHA-256；任何既有教材內容變動都直接失敗。
- 正式發布成功仍以 canonical `Deploy study library`、Pages artifact、重新下載驗證與 deployment receipt 為準。

## 正式發布結果

尚未執行。不得把 source merge 或候選 QA 當成正式部署成功；正式 run 完成後再回寫此節。
