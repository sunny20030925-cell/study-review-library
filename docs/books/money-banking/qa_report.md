# 《貨幣銀行學》QA 報告

更新日期：2026-07-29

## 結論

《貨幣銀行學》初版候選已完成兩輪獨立 QA，並以 2026-07-29 最新正式十書 GitHub Pages artifact（書庫版本 `2026.07.29-13`，尾端為 `international-economics`）重跑 canonical tail 整合。候選結果為 11 本書、書庫版本 `2026.07.29-14`、尾端 `money-banking`。

## 成品盤點

- 正文：20 章（ch00–ch19）。
- 附錄：3 份。
- 題庫：100 題，每章 5 題。
- 搜尋索引：150 筆。
- 自製 SVG：20 張，每章至少 1 張。
- 內容版本：`2026.07.29-1`。
- 一般金額例題：使用新臺幣（NT$）。
- 外匯報價：固定 `E=NT$/US$`，E 上升＝新臺幣貶值。

## 第一輪：結構、內容與整合 QA

獨立驗證器 `deploy/validate_money_banking.py` 共通過 963 項檢查，涵蓋：

1. 書庫 book ID、manifest、questions、search 的版本與識別一致。
2. 20 章、3 附錄、100 題、150 筆搜尋、20 張 SVG 數量完整。
3. 每章固定 5 題且 question ID 唯一。
4. 每章均包含標準例題、常見錯誤、考試判斷方法、理解檢查與圖解。
5. 章節與 SVG 實體路徑存在；SVG 含 title、desc、viewBox，且沒有遠端圖檔依賴。
6. service worker 包含貨銀 manifest、題庫、搜尋、章節與圖解離線路徑。
7. 核心概念覆蓋：M1A／M1B／M2、現值與殖利率、期限結構、資訊不對稱、銀行資產負債表、銀行風險與監理、準備貨幣、放款創造存款、貨幣乘數、貨幣需求、央行資產負債表、公開市場操作、央行存單、走廊／地板框架、政策傳遞、Fisher 關係、Phillips curve、Taylor principle、QE、前瞻指引、沖銷與不可能三角。
8. 排除過度簡化敘述，例如「1/rr 永遠是現實貨幣乘數」、「銀行可無限制創造貨幣」、「QE 必然讓 M2 等比例增加」、「殖利率曲線反轉必然造成衰退」等。
9. 控制字元、inline script、遠端 SVG 等平板閱讀／離線風險檢查通過。

第一輪輸出：

```text
MONEY_BANKING_QA_ROUND1_OK checks=963 chapters=20 appendices=3 questions=100 search=150 figures=20
```

## 第二輪：數值與高風險觀念獨立複核

重新驗算 20 個量化節點，包含：

- 單期現值與複利終值。
- 存續期間近似價格變動。
- 銀行權益、ROA、ROE、利率重定價缺口。
- 簡單存款乘數與 `m=(1+c)/(rr+e+c)`。
- 實質貨幣餘額。
- 央行資產負債表準備變化。
- 數量方程式成長率近似。
- Fisher 關係。
- Phillips curve 簡化題。
- Taylor 型規則。
- `E=NT$/US$` 的新臺幣設備成本方向。

另重新判讀高風險觀念：

- 銀行放款可同時創造存款，但仍受跨行清算、資本、流動性、風險、資金成本與信用需求限制。
- 準備充裕不代表貸款或廣義貨幣固定倍數增加。
- 簡單 `1/rr` 必須附帶無通貨外流、無超額準備等假設。
- QE 是央行資產負債表操作，不等同財政直接發錢。
- Fisher 精確式與低通膨近似式需區分。
- 走廊與地板操作框架不能混為單一制度。
- Taylor principle 是標準模型條件下的反應原則，不是各央行法定機械公式。
- 存款保險／最後貸款者同時具有穩定效果與道德危險。
- 外匯方向必須先固定報價方式。
- 不可能三角是高度資本流動下的政策取捨框架，不應寫成所有現實制度都只有純粹兩選一。

第二輪輸出：

```text
MONEY_BANKING_QA_ROUND2_OK numeric_rechecks=20 high_risk_concepts=10 fx_quote=passed multiplier_boundaries=passed policy_framework=passed
```

## 最新十書 artifact 整合實跑

使用正式 workflow run `30442682452` 的 GitHub Pages artifact 作為基底：

- 整合前：`2026.07.29-13`、10 本書、尾端 `international-economics`。
- 執行：`integrate_money_banking(site_root, "2026.07.29-13")`。
- 整合後：`2026.07.29-14`、11 本書、尾端 `money-banking`。
- 函式 stdout：只有 `2026.07.29-14`，不污染 canonical finalizer 的版本捕捉。
- 貨銀兩輪 QA 全部再次通過。
- 既有 10 本書的 book ID 與順序保持不變，貨銀只追加在尾端。
- 閱讀進度儲存格式不需改動；正式 deployment receipt 仍須在發布成功後再次確認 `progress_storage_changed=false`。

## 制度性資料核對口徑

制度性敘述優先依台灣中央銀行公開資料與一般中央銀行操作框架：

- 台灣貨幣總計數以 M1A、M1B、M2 分層說明；不把單月數值寫死在核心定義。
- 公開市場操作、央行存單、貼現／融通、準備金制度皆納入；不把法定準備率寫成每日唯一政策槓桿。
- 非常規政策與準備充裕框架明確區分「準備數量」與「短期利率／金融條件」。

## 發布門檻

候選內容 QA 已完成。正式完成仍以以下事項全部成立為準：

1. 最新 `main` 已同步且沒有覆蓋其他同日新增教材。
2. Money and Banking canonical tail PR 合併。
3. `Deploy study library` 成功部署完整書庫。
4. deployment receipt 顯示貨銀已加入、book count 增加、`progress_storage_changed=false`。
5. 正式 README、status、shared checkpoint 與 QA 文件同步完成。
