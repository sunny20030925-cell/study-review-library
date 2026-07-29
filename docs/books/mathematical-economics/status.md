# 《數理經濟學》製作狀態

更新日期：2026-07-29

## 正式識別

- Book ID：`mathematical-economics`
- 目標內容版本：`2026.07.29-1`
- 目前狀態：scope 已固定；內容、題庫、圖解與兩輪 QA 製作中，尚未宣稱正式部署。

## 固定邊界

- 標準大學數理經濟學／Mathematics for Economists 本位。
- 20 章、3 附錄、100 題、20 張自製 SVG。
- 核心含線性代數、微積分、比較靜態、無限制／限制最佳化、KKT、積分、差分與微分方程。
- 高階最適控制、dynamic programming、實分析等只列選讀，不擴張成另一門課。

## 發布門檻

1. 正文、題庫、搜尋與 SVG 全數生成。
2. 第一輪結構／內容 QA 通過。
3. 第二輪獨立公式與數值重算、最佳化條件重判、動態穩定性重判通過。
4. 發布前重新同步最新 `main`、shared checkpoint、registry 與 deployment receipt。
5. 既有全部書籍內容 hash 不變，Book ID／章節 ID／題目 ID／進度儲存鍵不倒退。
6. canonical Pages artifact、Pages deployment、deployment receipt 均核實後，才改成「已部署」。

## 目前正式基底

建立本工作線時正式書庫為 12 本、library version `2026.07.29-17`。此數字只是建立時基底；正式發布前必須重新讀最新 `main`，不得硬編碼覆蓋其他平行教材。