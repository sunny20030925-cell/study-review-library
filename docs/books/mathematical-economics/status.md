# 《數理經濟學》製作狀態

更新日期：2026-07-29

## 正式識別

- Book ID：`mathematical-economics`
- 目標內容版本：`2026.07.29-1`
- 目前狀態：scope、正文、題庫、圖解與兩輪 QA gate 已建置；等待 canonical run 實際驗證後才可宣稱正式部署。

## 固定邊界

- 標準大學數理經濟學／Mathematics for Economists 本位。
- 20 章、3 附錄、100 題、150 筆搜尋索引、20 張自製 SVG。
- 核心含線性代數、微積分、比較靜態、無限制／限制最佳化、KKT、積分、差分與微分方程。
- 高階最適控制、dynamic programming、實分析等只列選讀，不擴張成另一門課。

## 發布門檻

1. 正文、題庫、搜尋與 SVG 全數生成。
2. 第一輪結構／內容 QA 通過。
3. 第二輪獨立公式與數值重算、最佳化條件重判、動態穩定性重判通過。
4. 發布前重新同步最新 `main`、shared checkpoint、registry 與 deployment receipt。
5. 既有全部書籍內容 hash 不變，Book ID／章節 ID／題目 ID／進度儲存鍵不倒退。
6. canonical Pages artifact、Pages deployment、deployment receipt 均核實後，才改成「已部署」。

## 串接位置

- 建立本工作線時正式書庫為 12 本、library version `2026.07.29-17`。
- 其後 `computer-fundamentals` 已先進入 canonical source tail，因此數理經濟學不再搶第 13 本位置。
- 本候選固定接在 `computer-fundamentals` 後方；成功 run 的目標尾端為 `money-banking → computer-fundamentals → mathematical-economics`，共 14 本。
- 若正式發布前 `main` 又有其他教材完成 canonical integration，仍須重新同步並依最新順序調整，不硬編碼覆蓋平行工作線。