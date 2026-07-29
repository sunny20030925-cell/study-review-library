# 《計量經濟學》QA 報告

更新日期：2026-07-29

## 版本與範圍

- Book ID：`econometrics`
- 目標內容版本：`2026.07.29-1`
- 範圍：一般大學 introductory econometrics，共 20 章、3 附錄、100 題、189 筆搜尋索引與 20 張自製 SVG。
- 候選 QA：兩輪均已通過；正式發布仍需在當下最新共同書庫基底重跑。

## 第一輪：結構、公式、數值與整合檢查

執行器：`deploy/validate_econometrics.py`

結果：`ECONOMETRICS_QA_OK checks=384 chapters=20 appendices=3 questions=100 search=189 figures=20 numeric_rechecks=29`

主要覆核：

1. 20 個 chapter ID 為 `ch00`–`ch19`，3 個 appendix ID 固定且無重複。
2. 每章均包含問題、直覺、正式定義、核心公式、標準例題、常見錯誤、考試判斷與理解檢查。
3. 100 題題庫每章 5 題，題目 ID 唯一，答案與詳解完整。
4. 20 張 SVG 具有 title、desc、viewBox，沒有外部圖片依賴。
5. 搜尋索引為 189 筆，涵蓋全部章節與附錄。
6. manifest、questions、search、chapter HTML 與 service-worker cache 路徑一致。
7. tablet-facing chapter 與 SVG 檔案均存在且非空。
8. 29 個數值節點由原始輸入獨立重算，不只比對顯示答案。
9. `app.js` 與 `sw.js` 語法檢查通過。
10. 候選生成前後既有 12 本 `books/**` hash 完全一致。

## 第二輪：獨立內容與高風險答案複核

執行器：`deploy/validate_econometrics_v2.py`

結果：`ECONOMETRICS_QA_V2_OK checks=675 chapters=20 questions=100 search=189 high_risk_answer_gates=32`

第二輪沒有沿用第一輪的長字串 gate，而是重新從最終生成的 chapter HTML、questions JSON、search JSON 與 library entry 檢查：

- 每章關鍵概念是否實際存在。
- 每章題庫是否維持 `基礎 1／標準 2／綜合 1／陷阱 1`。
- 100 題是否都有題幹、答案、詳解與正確 Book ID。
- 32 題高風險答案是否明確保留正確限制條件。
- 20 章搜尋入口各 9 筆、3 附錄各 3 筆。
- `econometrics` library entry 唯一且可用，20 張 SVG 全數存在。

## 核心公式與數值重核

已覆核：

- 樣本平均、變異數、標準誤與基本檢定。
- 簡單 OLS 斜率／截距、TSS／RSS 與 R²。
- 多元迴歸與 partialling-out 直覺、adjusted R²。
- OVB 符號與數值例題。
- t／F 檢定與信賴區間。
- log 模型近似與 exact dummy percentage effect。
- heteroskedasticity-robust inference 的適用範圍。
- VIF 與 classical measurement-error attenuation。
- LPM／logit 機率與邊際效果。
- random walk、log difference、AR(1) 預測與長期平均。
- first differences／fixed effects transformation。
- IV Wald ratio、first stage／reduced form、2SLS。
- ATE／ITT。
- 2×2 DiD estimator。
- RDD cutoff local comparison。
- RMSE／MAE 與樣本外評估。

## 高風險負面 gate

候選已確認不把下列錯誤口號當成正確結論：

- 「顯著迴歸係數就代表因果」。
- 「R² 越高模型一定越正確」。
- 「robust SE 可以修正內生性」。
- 「多重共線性一定使 OLS 有偏」。
- 「first-stage 顯著即可證明 instrument 外生」。
- 「fixed effects 可以識別完全不隨時間變動的變數係數」。
- 「DiD 處置前係數不顯著就已證明 parallel trends」。
- 「RDD 效果可以無條件外推到所有樣本」。
- 「時間序列高 R² 就不可能是虛假迴歸」。
- 「預測較準即可證明係數具有因果意義」。

## 候選整合保護結果

本輪候選以 `docs/deployment_receipt.json` 指定的正式 Pages artifact 為唯一基底：

- 基底：12 本，shared library `2026.07.29-17`。
- 加入 `econometrics` 後：13 本。
- 模擬 shared library：`2026.07.29-18`。
- 新 Book ID 只追加於 registry 尾端。
- 既有 12 本內容 hash 不變。
- 閱讀進度、錯題與其他本機儲存鍵未改名。
- 平板端 chapter／SVG／search／questions／offline cache 路徑全部驗證通過。

## 發布狀態

候選內容與兩輪 QA 已完成，但目前仍不宣稱正式部署。發布前必須重新同步當下最新 `main`、shared checkpoint、registry 與 deployment receipt，修正／驗證 post-deploy recorder，並在最新共同書庫基底重跑兩輪 QA。正式 Pages run、artifact 與新的 deployment receipt 全部核實後再改為「已部署」。
