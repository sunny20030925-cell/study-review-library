# 《數理經濟學》QA 報告

更新日期：2026-07-29

## 版本與範圍

- Book ID：`mathematical-economics`
- 內容版本：`2026.07.29-1`
- 正文：20 章。
- 附錄：3 份。
- 題庫：100 題，每章 5 題。
- 搜尋索引：150 筆。
- 自製 SVG：20 張。

## 第一輪：結構與內容完整性

驗證項目：

- 20 章與 3 附錄檔案完整。
- 每章均包含問題、白話直覺、正式定義、核心公式與成立條件、完整例題、常見錯誤、考試判斷方法與理解檢查。
- 線性代數、微積分、比較靜態、彈性、Hessian、Lagrange、KKT、包絡定理、Euler 定理、積分、差分／微分方程均有正式覆蓋。
- 100 題題庫 ID 唯一且每章固定 5 題。
- 150 筆搜尋資料全部指向有效章節／附錄。
- 20 張 SVG 具有 `title`、`desc`、`viewBox`，不依賴遠端圖片。
- Service Worker 包含本書 manifest、questions、search、章節與 SVG 離線路徑。

## 第二輪：獨立重算與高風險邏輯

獨立重算／重判至少涵蓋：

- 聯立均衡、矩陣乘法、determinant 與反矩陣解。
- 導數、Taylor 近似、偏導數、全微分與隱函數比較靜態。
- 彈性、一元／多元最佳化、Hessian 定號。
- 等式限制 Lagrange、KKT 邊界與互補鬆弛。
- 包絡定理、齊次函數、Euler 定理。
- 邊際量積分回總量、離散複利與連續成長率轉換。
- 一階差分與微分方程穩態與穩定性。

高風險負面 gate：

- `FOC=0` 不得被寫成自動充分的最大值條件。
- Hessian 不得只憑主對角元素符號就判定正／負定。
- 比較靜態不得誤寫成時間動態。
- Lagrange multiplier 的符號解讀必須與 Lagrangian 慣例一致。
- KKT 不得在缺乏凹凸性等條件時被宣稱自動充分。
- 定積分不得無條件等同幾何面積。
- 差分方程穩定性必須檢查 `|b|<1`，不能只檢查 `b<1`。
- 微分方程穩態令 `ẋ=0`，不是令狀態變數本身等於 0。

## 自動化 gate

- 本書接在 canonical serialized tail 的 `computer-fundamentals` 之後；生成後必須形成 14 本書庫，尾端固定為 `money-banking → computer-fundamentals → mathematical-economics`。
- `deploy/integrate_mathematical_economics.py` 會在正式 `Deploy study library` 流程內執行第一輪結構／內容 QA 與第二輪獨立數值、公式、最佳化與穩定性重算。
- integration 前後逐本計算既有 13 本教材 hash；任何既有教材內容變動都直接失敗，不得部署。
- 正式通過仍以 canonical Pages artifact、Pages deployment 與 deployment receipt 為準。

## 發布狀態

本報告在 canonical QA 與 Pages run 完成前不宣稱正式通過。通過數、正式 library version、run 與 deployment receipt 會在實際驗證後回寫。