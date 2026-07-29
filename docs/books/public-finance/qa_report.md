# 《財政學》QA 報告

更新日期：2026-07-29

## 最終版本

- Book ID：`public-finance`
- 正式內容版本：`2026.07.29-2`
- 最新正式書庫版本：`2026.07.29-16`
- 正式書庫順位：第 11 本。
- 狀態：發布後獨立內容審計、糾錯、完整重建驗證與正式 Pages artifact 終檢均完成。

## 成品與相容性

- 正文：20 章（`ch00`–`ch19`）
- 附錄：3 份
- 題庫：100 題，每章 5 題
- 搜尋索引：189 筆
- 圖解：20 張自製 SVG
- 章節 ID：完全不變
- 題目 ID：100／100 完全不變
- 題數：完全不變
- 既有閱讀進度與錯題紀錄可沿用。

## 本輪審計方法

本輪不把初版 QA 結論當成正確性前提，重新檢查：

1. 20／20 章核心定義、公式、成立條件、例題、常見錯誤與解題判斷。
2. 100／100 題題幹、答案與詳解。
3. scope 承諾是否真的在正文展開。
4. 容易因條件漏寫而誤用的公式：租稅歸宿、DWL、Ramsey rule、勞動供給、公債動態。
5. 容易混用的專有名詞：funded pension、DB/DC、copayment、coinsurance、deductible、property／wealth／transfer taxes。
6. 數值題從原始輸入重新計算，而不是只比對既有答案。

## 實質糾錯與補強

### 1. 公共財：Lindahl 價格

初版 scope 已列 Lindahl price，但正文沒有真正展開。v2 補上個人化價格／稅負份額、共同公共財數量、個人價格加總對應邊際成本，以及偏好揭露限制；`ch03-q04` 同步改成 Lindahl 核心題，題目 ID 不變。

### 2. 尋租：避免把概念式當會計恆等式

尋租成本改成概念關係：政策租金本身可能只是移轉；真實尋租資源與政策伴隨的額外扭曲才是需要另外計入的社會成本。

### 3. 成本效益分析：社會折現率

補 Social Discount Rate，明示公共計畫不能機械地以政府借款利率作唯一折現率；需配合名目／實質口徑、跨期機會成本與評估規範。

### 4. 分配與移轉

Gini 的 0–1 敘述加上非負所得／標準化設定條件；補現金移轉、實物移轉與負所得稅。

### 5. 社會保險：funded 不等於個人帳戶

- PAYG／funded 是融資方式。
- DB／DC 是給付或提撥規則。
- funded 不必然等於 individual account，也不等於 DC；DB 同樣可能 funded。
- 補失業保險的消費平滑、流動性與求職誘因取捨。
- `ch08-q05` 詳解同步修正。

### 6. 醫療保險：修正 Copayment／Coinsurance 混稱

這是本輪最明確的術語錯誤：

- Copayment：固定金額。
- Coinsurance：合格醫療費用的一定比例。
- Deductible：保險開始依契約分攤前由被保險人先負擔的門檻。
- `P_patient=cP` 僅用於比例型 coinsurance，不適用固定金額 copayment。
- `ch09-q05` 同步改用 coinsurance 自付比例。

此修正與 HealthCare.gov 的正式定義一致。

### 7. 教育：Signaling / Screening

補教育訊號／篩選，明示觀察到的教育薪資溢酬不能全部直接當成教育提高生產力的因果效果；`ch10-q05` 同步調整，題目 ID 不變。

### 8. 租稅原則

補比例／累進／累退稅負的正式定義，並提醒實際經濟負擔仍須結合歸宿與有效稅率。

### 9. 租稅歸宿

彈性分攤式明示為標準競爭市場下的小稅／局部近似。有限大稅楔或彈性沿曲線改變時，應回完整供需曲線求新均衡；`ch12-q01`～`q03` 詳解同步補條件。

### 10. Excess Burden / DWL

稅收在基本福利圖中主要是私人部門到政府的移轉，不是 DWL 本身。三角形近似要求課稅前市場原本有效率，且能以線性／局部近似處理；既有扭曲、行政成本、遵從成本與多市場互動需另行處理。

### 11. Ramsey Rule

inverse-elasticity rule 明示為 Ramsey 商品稅的特殊情況，需要需求彼此獨立／交叉效果可忽略、分配權重等強條件；一般 Ramsey 問題不能只看 own-price elasticity。

### 12. 個人所得稅與勞動供給

「所得效果使工作增加」補上休閒為正常財等條件。ETI 改為應稅所得對 net-of-tax rate `1-t` 的百分比反應，並說明它混合工時、努力、報酬形式、避稅與逃漏等反應。

### 13. 公司所得稅

補 debt bias：若利息可扣除而股權正常報酬沒有對稱扣除，稅制可能相對鼓勵負債融資；不把此結論寫成所有國家／期間都必然成立。

### 14. 財產／財富課稅

區分週期性財產稅、淨財富稅與財產移轉稅。資本化改寫成帶程度參數的概念式 `ΔV≈-θPV(Δ future net tax)`，避免把完全資本化當成無條件結果。

### 15. 地方財政

`P_local=(1-m)P` 明定 `m` 為上級政府負擔合格支出的比例；若題目使用另一種 matching-rate 定義，必須先換算。

### 16. 公債動態

v2 先給精確離散式：

`b_t=[(1+r_t)/(1+g_t)]b_{t-1}-ps_t`

再推：

`Δb_t=[(r_t-g_t)/(1+g_t)]b_{t-1}-ps_t`

最後才給常用近似：

`Δb≈(r-g)b-ps`

並加入 stock-flow adjustment。以 `b=60%、r=4%、g=2%、ps=0` 為例：

- 精確簡化式：約增加 1.18 個 GDP 百分點。
- `r-g` 近似：約增加 1.2 個 GDP 百分點。

若題目明示使用近似式，原答案保留 1.2；詳解另列精確值。

## 外部交叉核對

- HealthCare.gov：Copayment 為固定金額、Coinsurance 為費用比例、Deductible 為保險開始分攤前的門檻。
- OECD `Pensions at a Glance 2025`：DB 可以 funded、PAYG 或混合，因此 funded 不能直接等同 individual account。
- IMF 公債框架：利率－成長差的精確離散債務關係包含 `1+g` 分母，實務債務累積亦可能受 stock-flow adjustment 影響。

## v2 驗證

PR `#73` 最新成功驗證 Run `30452510166`：

- 固定從正式 10 本／`2026.07.29-13` pre-public-finance artifact 重建。
- 財政學內容版本：`2026.07.29-2`。
- 財政學產生後書庫：11 本／`2026.07.29-15`。
- 舊結構／題庫／搜尋／SVG gate：2,386 項通過。
- 新 v2 內容 gate：174 項通過。
- 數值題由原始輸入重算：38 項；公債精確離散式另行重算。
- 修正區域 gate：16 區。
- 題目同步調整：5 題，100 個題目 ID 全部保留。
- 總體經濟學尾端相容 QA：201 項通過。
- 原 10 本教材檔案 SHA-256 前後一致。
- `app.js`、`sw.js`、20 張 SVG 與所有平板資產路徑均通過。

## 正式 Pages 終檢

### 財政學 v2 專屬部署

- Source commit：`a084173fe7f6d5a85a1bcf13e77567c1dc7610bb`
- Run：`30452624395`
- Pages artifact：`8724145499`
- Artifact digest：`sha256:47f8d1c832a03e8cda401de76e4777c14b4b0c5cf29e5f25c3580726ac5a19cc`
- Upload Pages artifact：成功。
- Deploy to GitHub Pages：成功。
- 該 artifact：11 本／`2026.07.29-15`；財政學 `2026.07.29-2`。

### 最新序列化正式部署

在財政學 v2 後，《國際經濟學》v2 隨即依序發布；最新正式 artifact 因此再升一版，但保留並重新驗證財政學 v2：

- 最新 source commit：`24bcf00d73dcb2e11b4d2dfbce14c5e99b5db85d`
- 最新 Run：`30452678302`
- 最新 Pages artifact：`8724164394`
- Artifact digest：`sha256:282d2bdeec05a04427dd13a5c50aa1fcce172011fff4c1403fd563c4cfc1b201`
- 最新書庫：11 本／`2026.07.29-16`
- 財政學：`2026.07.29-2`，20 章＋3 附錄、100 題、189 搜尋、20 SVG。
- 國際經濟學：`2026.07.29-2`。
- 正式 run 中財政學 2,386 項結構 gate＋174 項 v2 gate再次通過。
- GitHub Pages 明確回報 `Reported success!`。
- 最新 artifact 已重新下載，確認 Copayment／Coinsurance／Deductible、Lindahl、教育 Signaling、精確公債式與 Stock-flow Adjustment 均已存在於正式成品。

## 已知工程技債

兩次正式 run 都是在 Pages 成功後，才因舊 `Record successful deployment` 寫回器仍依賴舊 checkpoint 標題／句子格式而報 `microeconomics checkpoint section not found`。因此 Actions 整體顯示 failure，但網站部署與 artifact 已成功。`docs/deployment_receipt.json` 已依最新正式 artifact 與 deploy log 用 `[skip ci]` 校正，並保留 recorder failure 紀錄。

## 最終結論

本輪不是單純文字潤飾。確實找出並修正一項明確術語錯誤（Copayment／Coinsurance 混稱）、多個會造成公式誤用的條件缺口，以及多個 scope 已承諾但初版正文展開不足的內容。修正版已正式部署為《財政學》`2026.07.29-2`，目前最新共同書庫版本為 `2026.07.29-16`。
