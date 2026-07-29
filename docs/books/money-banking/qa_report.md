# 《貨幣銀行學》QA 報告

更新日期：2026-07-29

## 正式範圍

- Book ID：`money-banking`
- 正式內容版本：`2026.07.29-2`
- 正式書庫版本：`2026.07.29-17`
- 成品：20 章、3 附錄、100 題、150 筆搜尋索引、20 張自製 SVG。

## 來源更正

先前工作分支留下 7 個 `generate-money-banking.py.gz.b64.part*` 舊封裝檔。重新驗證確認 GitHub blob 搬運無誤，但完整封裝與舊 staging 記錄不一致，gzip CRC 失敗，DEFLATE 解出的原始碼中段亦有非 UTF-8 位元損壞。

因此正式版完全停止使用舊封裝，改由可讀、可審查的 `money_banking_content.raw`、題庫資料與 fresh generator 重新生成完整教材。正式 artifact 已證明 fresh rebuild 路線成功。

## 二次內容複核與直接修正

1. 區分票面利率、當期收益率、YTM 與持有期間報酬，補上 YTM 解讀條件。
2. 存續期間只作小幅殖利率變動的一階近似，補充凸性邊界。
3. 殖利率曲線反轉只作資訊訊號，不寫成衰退的必然定律。
4. 區分個體審慎與總體審慎；Basel III 保留資本、槓桿與流動性要求的經濟直覺。
5. 最後貸款者核心情境限於具還款／償付能力但暫時流動性不足、且籌資困難的銀行。
6. 釐清準備貨幣／貨幣基數、銀行準備、放款創造存款與跨行清算。
7. `1/rr` 僅稱簡單存款乘數，列明通貨外流、超額準備、資本、流動性與信用需求限制。
8. 臺灣央行制度章採官方現行制度用語：準備金制度、貼現窗口、公開市場操作、金融機構轉存款與選擇性信用管理等；不寫死易過期數值。
9. 區分 Fisher equation 精確式 `(1+i)=(1+r)(1+π^e)`、低通膨近似 `i≈r+π^e` 與 Fisher effect 的額外經濟假設。
10. QE 明確列為中央銀行資產負債表政策，不等同財政支出，也不推論準備金與 M2 固定倍增。
11. 匯率全書固定 `E=NT$/US$`；E 上升＝新臺幣貶值。

其中 9 個章節另加入「二次複核」精確化區塊，7 題高風險題目詳解同步補強，9 個章節的搜尋文字同步更新。

## QA 結果

### 第一輪：結構與內容完整性

- 結果：963／963 通過。
- 驗證：20 章、3 附錄、100 題且每章 5 題、150 搜尋、20 SVG。
- 每章檢查標準例題、常見錯誤、考試判斷、理解檢查、圖解與必要核心概念。
- 檢查禁止誤述、題庫資料結構、圖解可及性與 service worker 離線路徑。

### 第二輪：獨立重算與高風險概念

- 20 個量化節點由原始輸入重新計算，全數一致。
- 10 個高風險觀念重新判斷，全數通過。
- 專項 gate：匯率報價方向、貨幣乘數成立邊界、貨幣政策操作架構均通過。

### v2 獨立 QA

- 結果：473／473 通過。
- 驗證 12 本 canonical 尾端、v2 修正內容、7 題詳解同步、150 搜尋、20 SVG 與 20 個量化節點再驗算。
- 新增前後既有 11 本教材目錄 SHA-256 完全一致，證明新增本書未覆寫既有教材內容。

## 正式 artifact 終檢

- workflow run：`30460567595`
- source commit：`2a2fff311c76a6e05a8a93fee9f3d5daaa474574`
- Pages artifact：`8727395112`
- GitHub 回報 digest：`sha256:0d3dffa1e6b57d41f3ae8181d599f337b545d3f6ec92a0b677d65c7366104ba8`
- 下載後 artifact ZIP 實算 SHA-256：`0d3dffa1e6b57d41f3ae8181d599f337b545d3f6ec92a0b677d65c7366104ba8`，一致。
- artifact `data/library.json`：`2026.07.29-17`、12 本，尾端為 `macroeconomics → international-economics → public-finance → money-banking`。
- artifact `money-banking/manifest.json`：版本 `2026.07.29-2`、23 個 chapter/appendix entry。
- artifact `questions.json`：100 題、100 個唯一題目 ID。
- artifact `search.json`：150 筆。
- artifact：23 份章節／附錄 HTML、20 張 money-banking SVG 均存在。

## 部署結論

- Upload Pages artifact：success。
- Deploy to GitHub Pages：success；2026-07-29T14:23:09Z 回報成功。
- 固定入口：`https://sunny20030925-cell.github.io/study-review-library/`
- workflow overall conclusion 顯示 failure，原因僅為部署成功後的 repo 記錄器仍依賴舊 checkpoint 句型，於 `microeconomics deployment-flow line not found` 停止；不影響已完成的教材 QA、artifact 或 Pages deployment。
- 本 QA 報告與 deployment receipt 已依 workflow job、artifact digest、實際下載 artifact 與 Pages 成功狀態手動複核後校正。

**結論：本版內容、題庫、搜尋、圖解、兩輪 QA、v2 獨立 QA、既有書籍保護與正式 Pages 部署均已完成。**
