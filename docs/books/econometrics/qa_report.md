# 《計量經濟學》QA 報告

更新日期：2026-07-29

## 版本與範圍

- Book ID：`econometrics`
- 正式內容版本：`2026.07.29-1`
- 範圍：一般大學 introductory econometrics，共 20 章、3 附錄、100 題、189 筆搜尋索引與 20 張自製 SVG。
- 狀態：候選兩輪 QA、正式部署前兩輪 QA、Pages 部署與部署後 artifact 重驗均已完成。

## 第一輪：結構、公式、數值與整合檢查

執行器：`deploy/validate_econometrics.py`

候選／正式部署前結果：`ECONOMETRICS_QA_OK checks=384 chapters=20 appendices=3 questions=100 search=189 figures=20 numeric_rechecks=29`

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
10. 候選生成前後既有書籍 hash 保護通過。

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

已確認不把下列錯誤口號當成正確結論：

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

## 早期候選整合紀錄

候選階段曾以當時 `docs/deployment_receipt.json` 指定的 12 本正式 Pages artifact 驗證：

- 基底：12 本，shared library `2026.07.29-17`。
- 加入 `econometrics` 後：13 本。
- 模擬 shared library：`2026.07.29-18`。
- 新 Book ID 只追加於 registry 尾端。
- 既有 12 本內容 hash 不變。
- 閱讀進度、錯題與其他本機儲存鍵未改名。
- 平板端 chapter／SVG／search／questions／offline cache 路徑全部驗證通過。

以上僅為候選期歷史紀錄，正式發布並未使用這個舊 12 本基底。

## 正式發布與部署後重驗

正式發布以當時最新共同書庫為基底：

- 正式基底：17 本、shared library `2026.07.29-22`。
- 加入 `econometrics`：18 本、shared library `2026.07.29-23`。
- 正式 Pages run：`30471586965`。
- Source commit：`4bdca45ab4772982a812017b34984aff19a9a6c1`。
- Pages artifact：`8731859754`。
- Artifact digest／下載 SHA-256：`sha256:f53bf4979a85a0ff96e9e253cad04f97d37062d368195a97ce4189f8e934edf5`。
- 部署前：Round 1 = 384、Round 2 = 675。
- Pages 部署成功後重新下載 artifact：`DEPLOYED_ARTIFACT_RECHECK_OK 2026.07.29-23 18`。
- 部署後：Round 1 = 382、Round 2 = 675；29 個數值重算與 32 個高風險答案 gate 仍通過。
- 最終 deployment proof：`run=30471586965 artifact=8731859754 ... library=2026.07.29-23 books=18`。
- 後續《產業經濟學》正式發布後，最新 19 本／`2026.07.29-24` registry 仍包含 `econometrics`，證明本書未被後續序列發布覆蓋。

## 發布狀態

已部署。先前 QA 報告尾段仍寫成「正式發布仍需重跑」屬 post-deploy 文件回寫漏項；現已依正式 run、artifact、下載後重驗與最新 registry 校正。

## 發布後獨立內容審計 v2（2026-07-30）

本輪不是重跑原本的字串 gate，而是針對計量解讀最容易「公式沒錯、因果範圍卻講過頭」的地方重新審核。

### 修正 1：Panel FE／FD 的外生性條件

- v1 已正確說明 FE／FD 可消除時間不變個體效果 `alpha_i`，也提醒 time-varying confounder 仍可能造成問題。
- v2 進一步明列標準靜態 panel 常用的 strict-exogeneity 條件 `E(u_it | x_i1,...,x_iT,alpha_i)=0`。
- 同步補充：若當期衝擊影響未來 X、存在時間變動混淆或含落後依變數，不能因為用了 FE 就直接宣稱 beta 已具有因果識別。
- 題目 `ch13-q04` 保留原 ID，改為直接檢查上述成立條件。

### 修正 2：Random assignment 與 population generalization

- v1 把 randomized experiment 的差均值直接連到 ATE，沒有充分區分「實驗樣本內因果效果」與「更大目標母體效果」。
- v2 明確區分 SATE 與 PATE：random assignment 支持實驗單位內部的因果比較；要推廣到更大母體，仍需代表性抽樣、外部效度或其他 transportability 條件。
- 題目 `ch15-q02` 保留原 ID，改為檢查 random assignment 是否足以無條件外推 PATE；`ch15-q03` 詳解同步精確化。

### 相容性與 QA

- 20 章、3 附錄、100 題、189 搜尋、20 SVG：全部維持。
- chapter IDs：`ch00`–`ch19` 全部維持。
- question IDs：100 個全部維持；每章仍 5 題。
- 既有第二輪內容 gate 重新執行；另加 v2 reaudit validator：57 項通過。
- 閱讀進度與錯題儲存結構未變。

### v2 正式部署

- Book version：`2026.07.30-1`。
- Shared library：`2026.07.30-4`，20 本。
- Pages run：`30489306339`。
- Pages artifact：`8738999051`；digest `sha256:d21d233e589919d29631074724231a16cdda4cc9f2881543e75f61a6e3903ec4`。
- 部署後重新下載 artifact，再核對本書 23 份 HTML、100 題、189 搜尋與 20 SVG 均通過。
