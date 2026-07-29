# 《數理經濟學》製作狀態

更新日期：2026-07-30

## 正式識別

- Book ID：`mathematical-economics`
- 修正版目標內容版本：`2026.07.30-2`
- 目前狀態：第二次獨立內容審計修正版候選；尚未宣稱正式部署。

## 固定邊界

- 標準大學數理經濟學／Mathematics for Economists 本位。
- 維持 20 章、3 附錄、100 題、150 筆搜尋索引、20 張自製 SVG。
- 核心含線性代數、微積分、比較靜態、無限制／限制最佳化、KKT、積分、差分與微分方程。
- 高階最適控制、dynamic programming、實分析等仍只列選讀，不擴張成另一門課。

## v2 修正重點

- 補 KKT 的 constraint qualification、LICQ／Slater 與 necessary/sufficient distinction。
- 修正 homothetic、特徵向量、全微分等定義精度。
- 移除彈性章矛盾公式，補 Cobb–Douglas 對數微分。
- 補鏈鎖律、凹性／擬凹性、受限二階條件與 constrained envelope theorem。
- 補差分 `|b|=1` 與微分方程 `F′(x*)=0` 的邊界判斷。
- 調整 11 題高風險題目／答案／解析。

## 發布門檻

1. 以發布當下最新 verified formal Pages artifact 為底稿，不硬編碼舊的書籍數或前一本教材。
2. 若正式 artifact 尚無 `mathematical-economics`，修正版只允許 append 到當時最新尾端；若已存在，則必須改走 in-place v2 patch，不可重複新增 Book ID。
3. 生成後執行新的第二次獨立 QA，包含正文、題庫、搜尋、公式與動態穩定性重算。
4. 整合前後所有既有教材與既有 assets hash 必須完全一致。
5. Pages deployment、artifact 重新下載驗證、deployment receipt 與 shared checkpoint 全部成功後，才改成「已部署」。
