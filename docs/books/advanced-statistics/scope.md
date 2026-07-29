# 《高等統計學》科目範圍

## 定位

- Book ID：`advanced-statistics`
- 書名：《高等統計學》
- 副標：機率模型・抽樣分配・估計與檢定理論
- 層級：一般大學第二門統計學／高等統計／數理統計核心。
- 讀者起點：已接觸基礎統計概念；正文第 0 章補足本書實際需要的微積分、Taylor 展開、簡單矩陣與 Jacobian 工具。

本書承接既有《統計學》刻意不展開的數理統計範圍。主線為「機率模型 → 多元隨機變數 → 抽樣分配與極限定理 → 點與區間估計 → 檢定理論 → 常態線性模型」。目標是讓讀者不只會套入門公式，也能判斷公式的來源、成立條件與有限樣本／漸近結論的差別。

## 核心範圍

1. 高等統計所需的求和、積分、偏微分、Taylor 展開、簡單矩陣與 Jacobian。
2. 機率公理、條件機率、獨立、全機率與 Bayes 定理。
3. 隨機變數、PMF、PDF、CDF、分位數與支撐集。
4. Bernoulli、Binomial、Geometric、Negative Binomial、Poisson 等離散分配。
5. Uniform、Exponential、Gamma、Beta、Normal 等連續分配與參數化。
6. 聯合、邊際與條件分配，隨機變數獨立性的分配表達。
7. 期望、變異數、共變異數、相關、條件期望、全期望與全變異公式。
8. 多元常態、均值向量、共變異數矩陣、線性組合與條件常態。
9. 一維與二維變數轉換、逆像、Jacobian 與支撐集轉換。
10. MGF、PGF、特徵函數、動差與獨立和的分配運算。
11. 次序統計量、樣本最小值／最大值與 Uniform 次序統計量。
12. 依機率／分布收斂、大數法則、中央極限定理、Slutsky 定理與 Delta method。
13. 常態樣本下的 χ²、t、F 抽樣分配與樞紐量。
14. 動差法、最大概似估計、score、log-likelihood、邊界 MLE 與 invariance 直覺。
15. 充分統計量、Neyman–Fisher 因子分解、指數族與完備性。
16. bias、variance、MSE、一致性、漸近常態、Fisher information、Cramér–Rao、Rao–Blackwell、Lehmann–Scheffé。
17. 樞紐量、精確／大樣本信賴區間與 coverage 的正確解讀。
18. size、power function、p-value、Neyman–Pearson lemma 與最強力檢定。
19. UMP、monotone likelihood ratio 的核心直覺、likelihood-ratio test 與 Wilks 漸近理論。
20. 常態線性模型、OLS、Gauss–Markov、有限樣本 t/F 推論，以及迴歸／ANOVA 的共同線性模型結構。

## 與既有《統計學》的分工

既有 `statistics` 是第一門大學統計學，主力放在資料描述、常見機率分配、基礎抽樣與估計、一般假設檢定、兩群比較、卡方、單因子 ANOVA、相關與簡單迴歸。

本書不重做上述入門操作；只有在建立數理來源時才回顧。例如：
- t、χ²、F 在本書重點是抽樣分配與精確成立條件，而不是再次教一次基礎查表。
- 迴歸與 ANOVA 在本書重點是常態線性模型、OLS 與共同的 t/F 結構。
- p-value 在本書重點是檢定函數、size、power 與 NP／LRT 理論中的位置。

## 明確排除

正文與核心題庫不擴張至：

- 測度論機率、σ-algebra、Radon–Nikodym 定理與嚴格測度論證明。
- 隨機過程、Markov chain、Poisson process、martingale、Brownian motion。
- 完整多變量分析（PCA、factor analysis、MANOVA、canonical correlation）。
- 廣義線性模型、混合模型、生存分析、時間序列、空間統計。
- 計量經濟學的內生性、IV、panel、DiD、RDD 等因果識別。
- 完整 Bayesian inference、MCMC 與 decision theory；Bayesian 名詞只在必要比較時短暫出現。
- 機器學習、深度學習與軟體套件操作課程。
- 高階漸近展開、empirical process、semiparametric theory 等研究所專門內容。

上述主題若有助於指出邊界，只能作延伸提示，不占核心題庫與必讀進度。

## 重要精確性規則

- Gamma 第二參數固定標成 `rate λ`；不得與 scale 參數化混寫。
- 連續型隨機變數的密度高度不是單點機率。
- `Cov(X,Y)=0` 一般不推出獨立；只有在聯合常態等特殊條件下才可進一步推出。
- Jacobian 密度轉換使用行列式絕對值，多對一轉換必須加總所有有效逆像。
- MGF 並非每個分配都在 0 附近有限存在；特徵函數則總存在。
- LLN 不等於 CLT；CLT 描述適當標準化的和／平均之極限分布，不表示原始資料變成常態。
- χ²、t、F 的標準有限樣本精確結果必須標明常態與獨立等條件；大樣本近似不得冒充精確結果。
- Likelihood 是資料固定後的參數函數，不等於參數的機率分布。
- 充分、完備、無偏與一致性是不同性質，不得互相替代。
- Cramér–Rao 與 Fisher information 的等價公式要標明正則條件。
- 95% confidence interval 的 95% 是程序的長期 coverage，不是已觀察資料後固定參數的後驗機率。
- p-value 不是 `P(H0|data)`。
- Neyman–Pearson lemma 的標準結論針對 simple vs simple；UMP 未必存在。
- Wilks 的 χ² 結果通常是正則條件下的大樣本漸近結果。
- Gauss–Markov 的 BLUE 結論不需要常態誤差；傳統小樣本精確 t/F 推論才另外使用常態條件。
- R² 或顯著迴歸係數都不自動建立因果關係。

## 成品結構

- 正文：第 0 章至第 19 章，共 20 章。
- 附錄：核心分配／定理／公式速查、高等統計解題路線、中英名詞與符號對照，共 3 份。
- 題庫：100 題，每章 5 題；固定涵蓋基礎理解、標準計算／推導辨識、綜合判斷與常見陷阱。
- 搜尋索引：189 筆。
- 圖解：20 張自製 SVG，每章至少一張結構或推論流程圖。
- 平板功能：沿用共同 PWA 的連續閱讀、章節導覽、全文搜尋、題庫練習、閱讀進度、錯題紀錄與離線快取。

## 參考口徑

- 一般大學 Advanced Statistics／Mathematical Statistics 共同核心。
- 課程邊界以「基礎統計之後、研究所測度論與專門統計模型之前」為準。
- 公式與定理以標準數理統計教材常見表述為主；不同參數化時必須在正文先固定口徑。
