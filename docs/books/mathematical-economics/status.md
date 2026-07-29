# 《數理經濟學》製作狀態

更新日期：2026-07-29

## 正式識別

- Book ID：`mathematical-economics`
- 目標內容版本：`2026.07.29-1`
- 目前狀態：release candidate；scope、正文、題庫、圖解生成器與兩輪 QA gate 已建置，尚未宣稱正式部署。

## 固定邊界

- 標準大學數理經濟學／Mathematics for Economists 本位。
- 20 章、3 附錄、100 題、150 筆搜尋索引、20 張自製 SVG。
- 核心含線性代數、微積分、比較靜態、無限制／限制最佳化、KKT、積分、差分與微分方程。
- 高階最適控制、dynamic programming、實分析等只列選讀，不擴張成另一門課。

## 發布門檻

1. 以最新正式 15 本 Pages artifact 為唯一發布底稿；尾端必須為 `computer-fundamentals → game-theory`。
2. 數理經濟學只能接在正式 `game-theory` 後方，不跳過或覆蓋較新的正式 artifact。
3. 生成後執行第一輪結構／內容 QA 與第二輪獨立數值、公式、最佳化、比較靜態與穩定性重算。
4. 整合前後既有 15 本教材內容 hash 必須完全一致。
5. Pages artifact、Pages deployment、重新下載驗證與 deployment receipt 全部成功後，才改成「已部署」。

## 預定正式位置

- 正式順序尾端：`advanced-statistics → computer-fundamentals → game-theory → mathematical-economics`。
- 預定成為第 16 本教材。
- 若正式發布前又有其他教材先完成 canonical release，仍須以最新 receipt／artifact 重新排序，不硬編碼覆蓋平行工作線。
