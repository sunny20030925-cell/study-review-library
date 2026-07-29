# 《計量經濟學》QA 報告

更新日期：2026-07-29

## 版本與範圍

- Book ID：`econometrics`
- 目標內容版本：`2026.07.29-1`
- 範圍：一般大學 introductory econometrics，共 20 章、3 附錄、100 題與 20 張自製 SVG。
- 本文件目前先記錄候選 QA 計畫與 gate；只有實際驗證完成後才回填通過數。

## 第一輪：製作內檢

預定逐項檢查：

1. 20 個 chapter ID 為 `ch00`–`ch19`，3 個 appendix ID 固定且無重複。
2. 每章均包含問題、直覺、正式定義、核心公式、標準例題、常見錯誤、考試判斷與理解檢查。
3. 100 題題庫每章 5 題，題目 ID 唯一，答案與詳解完整。
4. 20 張 SVG 具有 title、desc、viewBox，沒有外部圖片依賴。
5. 搜尋索引至少 160 筆，且涵蓋全部章節與附錄。
6. manifest、questions、search、chapter HTML 與 service-worker cache 路徑一致。
7. tablet-facing chapter 與 SVG 檔案均存在且非空。

## 第二輪：獨立複核

### 核心公式重核

- 樣本平均、變異數、標準誤與基本檢定。
- 簡單 OLS 斜率／截距、TSS／ESS／SSR 與 R²。
- 多元迴歸與 partialling-out 直覺。
- OVB 符號公式。
- t／F 檢定與信賴區間。
- log 模型近似與 exact dummy percentage effect。
- heteroskedasticity-robust inference 的適用範圍。
- LPM／logit 機率與邊際效果的差別。
- AR(1)、autocorrelation 與 HAC 推論。
- first differences／fixed effects transformation。
- IV Wald ratio、first stage／reduced form、2SLS。
- ATE／ITT。
- 2×2 DiD estimator。
- RDD cutoff local comparison。
- RMSE／MAE 與樣本外評估。

### 高風險負面 gate

候選內容不得出現下列錯誤敘述：

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

## 數值重算

每章至少抽一個量化節點從原始輸入重新計算；所有題庫中含明確數值答案的題目全部重算，不只比對字串。

## 整合保護

候選驗證必須從當下最新成功 Pages artifact 建立暫存網站，加入 `econometrics` 後：

- 既有全部書籍內容 hash 不變。
- 新 Book ID 只追加於 registry 尾端。
- 共同書庫版本在候選中只做一次順增模擬，不寫回正式 main。
- app.js、sw.js 語法檢查通過。
- 閱讀進度、錯題與其他本機儲存鍵不改名。

## 發布狀態

本報告目前為候選階段。正式 Pages run、artifact、deployment receipt、最終書庫版本與實際 QA 通過數，必須在共同書庫重新同步並完成正式發布後再回填。
