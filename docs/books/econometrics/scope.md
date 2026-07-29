# 《計量經濟學》科目範圍

## 定位

- Book ID：`econometrics`
- 書名：《計量經濟學》
- 副標：迴歸・因果推論・時間序列・縱橫資料
- 層級：一般大學計量經濟學／Undergraduate Econometrics，共同核心從接近零基礎銜接一般大學課程與考試。
- 讀者起點：正文不要求先熟悉矩陣推導或統計軟體；第 1 章補足本書真正會用到的機率、抽樣、期望值、變異數與統計推論。已學過統計學者可快速複習。

本書以「從資料提出可回答的問題 → 建立迴歸模型 → 理解 OLS 與推論 → 診斷模型問題 → 處理內生性 → 使用時間序列與縱橫資料 → 進入現代因果推論設計 → 正確解讀與報告實證結果」為主線。重點是知道估計量在什麼條件下回答什麼問題，而不是只會按軟體得到係數。

## 核心範圍

1. 計量經濟學的問題地圖：描述、預測、因果、資料型態、母體模型、樣本與估計量。
2. 必要統計複習：隨機變數、期望值、變異數、共變數、抽樣分配、大數法則、中央極限定理、信賴區間與假設檢定。
3. 簡單線性迴歸與 OLS：最小平方法、殘差、配適值、斜率與截距、SST／SSR／SSE、R²。
4. OLS 的抽樣性質：無偏性、一致性、條件期望、Gauss–Markov 定理與 BLUE 的正確範圍。
5. 多元迴歸：控制變數、偏迴歸／partialling out 直覺、ceteris paribus 解釋、調整後 R²。
6. 因果解釋與遺漏變數偏誤：外生性、內生性、混淆因子、短迴歸／長迴歸、OVB 符號判斷。
7. 迴歸推論：標準誤、t 檢定、信賴區間、F 檢定、聯合假設與有限樣本／大樣本條件。
8. 函數形式與虛擬變數：level-level、log-level、level-log、log-log、多項式、交互作用、dummy variable trap。
9. 異質變異與穩健推論：heteroskedasticity、heteroskedasticity-robust standard errors、WLS 的條件與限制。
10. 規格診斷與資料問題：多重共線性、離群值／高槓桿點、函數形式錯置、代理變數、測量誤差與資料探勘風險。
11. 二元依變數：Linear Probability Model、logit／probit 的基本直覺、機率預測與邊際效果；重點放在本科常見解讀。
12. 時間序列基礎：時間索引、趨勢、季節性、落後值、弱定態直覺、隨機漫步與虛假迴歸風險。
13. 時間序列迴歸與序列相關：動態迴歸、AR(1) 誤差直覺、serial correlation、HAC／Newey–West 標準誤與預測評估。
14. 縱橫資料：pooled OLS、first differences、fixed effects、random effects 的假設差異與時間不變特徵。
15. 工具變數與 2SLS：relevance、exogeneity／exclusion restriction、first stage、reduced form、Wald estimator、weak instruments 與同時性。
16. 隨機實驗與潛在結果：treatment、control、ATE、selection bias、random assignment、compliance 與意向治療 ITT 的基本概念。
17. Difference-in-Differences：parallel trends、2×2 DiD、固定效果表示、event-study 圖的用途與限制、clustered standard errors。
18. Regression Discontinuity Design：cutoff、running variable、continuity assumption、local treatment effect、帶寬與操弄檢查。
19. 預測、模型選擇與樣本外評估：training／test、RMSE／MAE、overfitting、預測目標與因果目標的差別。
20. 完整實證工作流程：研究問題、estimand、識別假設、資料清理、估計、穩健性檢查、表格／圖形、可重現性與結果解讀。

## 深度邊界

正文與核心題庫不擴張至：

- 研究所層級的大樣本理論證明、empirical process、M-estimation／GMM 的一般理論。
- 高維度計量、LASSO／double machine learning、非參數／半參數估計、quantile regression 的完整理論。
- 高階時間序列：完整 ARIMA 選模、VAR／SVAR、協整／VECM、頻域分析、狀態空間模型。
- 高階 panel：dynamic panel GMM、Arellano–Bond、nonlinear panel、interactive fixed effects。
- 結構估計、一般均衡估計、離散選擇結構模型、模擬估計與 Bayesian econometrics。
- 特定軟體語法教學。必要的輸出表只教「怎麼讀」，不把本書變成 R／Stata／Python 操作手冊。

上述內容若有助於理解，只能以「延伸」或邊界說明出現，不占核心題庫與必讀進度。

## 重要精確性規則

- 「迴歸有顯著關係」不得直接寫成「X 導致 Y」；因果解釋必須另外說明識別假設或研究設計。
- `E(u|X)=0` 是比 `Cov(X,u)=0` 更強的條件；不得把不同外生性條件混成一句口號。
- Gauss–Markov 的 BLUE 結論只是在相應線性模型與同方差等條件下，針對線性無偏估計量的有限樣本比較；不得寫成 OLS 在任何環境都「最佳」。
- R² 衡量樣本內線性配適，不代表因果、模型正確、預測一定好，也不能單獨決定是否加入控制變數。
- 異質變異穩健標準誤主要修正標準誤／推論，不會自動修正遺漏變數、反向因果、測量誤差或其他內生性。
- 多重共線性在外生性成立時不會使 OLS 係數本身產生系統性偏誤；它主要使個別係數難以精確估計，完全共線性則使模型無法估計。
- 對數模型的百分比解釋必須分清近似與精確變化；dummy 進入 log(y) 時，必要時使用 `100(exp(beta)-1)%` 的精確效果。
- 2SLS／IV 必須同時討論 instrument relevance 與 exogeneity／exclusion；強 first stage 不能證明工具變數外生。
- weak instrument 不能只看「第一階段有顯著」；教材會說明常見 first-stage F 診斷只是實務指標，不是萬用保證。
- fixed effects 依賴個體內變化；時間不變變數在個體固定效果模型中無法單獨識別。random effects 需要比 FE 更強的效果與解釋變數不相關假設。
- DiD 的核心是未受處置時趨勢可比較的 parallel-trends 假設；看到處置前係數不顯著不能證明假設必然成立。
- RDD 的因果效果通常是 cutoff 附近的 local effect；不得無條件外推到所有樣本。
- time-series regression 必須檢查趨勢、定態與序列依賴；高 R² 與顯著 t 值不能排除 spurious regression。
- 預測與因果是不同目標：樣本外預測較準的模型，不代表每個係數都有因果意義。

## 成品結構

- 正文：第 0 章至第 19 章，共 20 章。
- 附錄：核心公式與假設速查、計量題型判斷路線、中英名詞與輸出表對照，共 3 份。
- 題庫：100 題，每章 5 題，涵蓋基礎理解、標準計算／輸出判讀、綜合判斷與常見陷阱。
- 搜尋索引：至少 160 筆，初版目標約 166 筆。
- 圖解：20 張自製 SVG，每章至少一張真正幫助理解的資料流程、迴歸幾何、識別設計或時間／panel 結構圖。
- 平板功能：沿用共同 PWA 的連續閱讀、章節導覽、全文搜尋、題庫練習、閱讀進度、錯題紀錄與離線快取。

## 參考口徑

- 一般大學 introductory econometrics 共同課程架構；核心交集以 OLS、多元迴歸、推論、heteroskedasticity、IV、panel data 與 time series 為主。
- 現代本科常見的 program evaluation／causal inference 內容納入 random experiments、DiD 與 RDD，但不擴張成研究所因果推論專題課。
- 外部課程交叉核對包括 UC Berkeley ECON 140／141 與 MIT OpenCourseWare 14.32；只用來確認主題覆蓋，不照搬教材文字或受版權限制題目。
