from __future__ import annotations

QUESTIONS_B = [
    {'id':'ch10-q01','chapterId':'ch10','question':'LPM 中某 dummy 的係數為 0.07。其他條件固定時，較自然的解讀是什麼？','answer':'預測成功機率高 7 個百分點。','explanation':'LPM 的 0.07 是機率單位；乘 100 得 7 個百分點，不是自動等於相對增加 7%。'},
    {'id':'ch10-q02','chapterId':'ch10','question':'Logit 中某觀察值 p=0.5、連續 X 的係數 beta=0.8。局部邊際效果 beta p(1-p) 是多少？','answer':'0.20，即約 20 個百分點／一單位 X。','explanation':'0.8×0.5×0.5=0.20。'},
    {'id':'ch10-q03','chapterId':'ch10','question':'同一 logit beta=0.8，但某觀察值 p=0.1。局部邊際效果是多少？','answer':'0.072，即約 7.2 個百分點／一單位 X。','explanation':'0.8×0.1×0.9=0.072，顯示 logit 邊際效果會依 X／p 而變。'},
    {'id':'ch10-q04','chapterId':'ch10','question':'為什麼 LPM 常有 heteroskedasticity？','answer':'因為二元 Y 下 Var(u|X)=p(X)[1-p(X)]，通常會隨 X 改變。','explanation':'只要條件成功機率 p(X) 隨 X 改變，誤差條件變異數通常也跟著改變。'},
    {'id':'ch10-q05','chapterId':'ch10','question':'Logit 預測值一定落在 0 到 1，是否因此自動解決 omitted-variable bias？','answer':'否。','explanation':'合法的機率函數形式不等於因果識別；遺漏變數與其他內生性仍可能存在。'},

    {'id':'ch11-q01','chapterId':'ch11','question':'random walk 從 y0=100 開始，兩期衝擊依序為 +2、-1。y2 是多少？','answer':'101。','explanation':'y1=102，y2=102-1=101。'},
    {'id':'ch11-q02','chapterId':'ch11','question':'指數從 100 增至 105，100×Delta log(y) 約是多少？','answer':'約 4.879%。','explanation':'100×[ln(105)-ln(100)]≈4.879%，與一般 5% 成長率在小變化時接近。'},
    {'id':'ch11-q03','chapterId':'ch11','question':'弱定態是否要求 y_t 每一期都幾乎不變？','answer':'否。','explanation':'弱定態要求平均、變異數固定且協方差只依期距；序列本身仍可上下波動。'},
    {'id':'ch11-q04','chapterId':'ch11','question':'無漂移 random walk 的一次衝擊通常會在下一期完全消失嗎？','answer':'不會，衝擊會被累積並具有持久影響。','explanation':'y_t=y_{t-1}+epsilon_t，新的水準承接前一期已包含的衝擊。'},
    {'id':'ch11-q05','chapterId':'ch11','question':'兩條互不相關但都有強趨勢的序列，是否可能出現高 R² 與顯著 t？','answer':'可能。','explanation':'這是 spurious regression 的典型風險，因此時間序列要先處理趨勢、定態與單位根等問題。'},

    {'id':'ch12-q01','chapterId':'ch12','question':'AR(1) y_t=2+0.8y_{t-1}+u_t，若 y_t=10，一步期條件平均預測是多少？','answer':'10。','explanation':'2+0.8×10=10。'},
    {'id':'ch12-q02','chapterId':'ch12','question':'AR(1) alpha=2、rho=0.8 且 |rho|<1，長期平均是多少？','answer':'10。','explanation':'alpha/(1-rho)=2/0.2=10。'},
    {'id':'ch12-q03','chapterId':'ch12','question':'AR(1) alpha=1、rho=0.5 且 |rho|<1，長期平均是多少？','answer':'2。','explanation':'1/(1-0.5)=2。'},
    {'id':'ch12-q04','chapterId':'ch12','question':'誤差存在正 serial correlation 時，傳統 iid／無序列相關標準誤可能可靠嗎？','answer':'通常不可靠。','explanation':'跨期相關使有效資訊量與傳統公式假設不同，常需依模型使用 HAC 或其他合適推論。'},
    {'id':'ch12-q05','chapterId':'ch12','question':'HAC／Newey–West SE 能否自動修正落後依變數與序列相關誤差造成的內生性？','answer':'不能。','explanation':'HAC 主要修正變異數估計；若 OLS 點估計因動態內生性而不一致，需要另外的識別／估計方法。'},

    {'id':'ch13-q01','chapterId':'ch13','question':'y_it=2x_it+alpha_i+u_it，某人的 x 從 3 變 5。忽略誤差差分時，Delta y 是多少？','answer':'4。','explanation':'First Difference 消掉 alpha_i，Delta y=2×Delta x=2×(5-3)=4。'},
    {'id':'ch13-q02','chapterId':'ch13','question':'First Difference 為什麼能消掉時間不變的 alpha_i？','answer':'因為 alpha_i-alpha_i=0。','explanation':'同一個體相鄰期相減時，任何固定不變的個體效果都被差掉。'},
    {'id':'ch13-q03','chapterId':'ch13','question':'個體 fixed effects 模型能否單獨識別完全不隨時間變動的性別 dummy 主效果？','answer':'不能。','explanation':'去個體平均後時間不變變數變成 0，與個體固定效果完全共線。'},
    {'id':'ch13-q04','chapterId':'ch13','question':'FE 是否能自動控制所有隨時間變化的遺漏 confounders？','answer':'不能。','explanation':'FE 主要消除時間不變個體效果；time-varying confounders 仍可能造成內生性。'},
    {'id':'ch13-q05','chapterId':'ch13','question':'Random Effects 相比 FE 通常需要哪個更強的關鍵假設？','answer':'個體效果 alpha_i 與解釋變數在相關時點上不相關。','explanation':'若 alpha_i 與 X 相關，RE 一般失去所需外生性，而 FE 可容許這種時間不變相關。'},

    {'id':'ch14-q01','chapterId':'ch14','question':'二元工具 Z 使平均 X 增加 2、平均 Y 增加 6。Wald IV estimator 是多少？','answer':'3。','explanation':'Wald=DeltaY/DeltaX=6/2=3。'},
    {'id':'ch14-q02','chapterId':'ch14','question':'Z 使 X 增加 3、使 Y 增加 9。Wald estimator 是多少？','answer':'3。','explanation':'9/3=3。'},
    {'id':'ch14-q03','chapterId':'ch14','question':'工具變數有很強的 first stage，能否由此證明 exclusion restriction？','answer':'不能。','explanation':'First stage 支持 relevance；exogeneity／exclusion 是另外的識別條件，通常需要制度與研究設計論證。'},
    {'id':'ch14-q04','chapterId':'ch14','question':'Cov(Z,X) 非常接近 0 時，最先擔心哪一類 IV 問題？','answer':'Weak instrument／缺乏 relevance。','explanation':'IV 比率分母接近 0，估計與推論會非常不穩定。'},
    {'id':'ch14-q05','chapterId':'ch14','question':'IV 的兩個核心檢查可簡化成哪兩類？','answer':'Relevance 與 exogeneity／exclusion。','explanation':'工具必須能推動 X，並且不能透過不允許的路徑直接影響 Y 或與結構誤差相關。'},

    {'id':'ch15-q01','chapterId':'ch15','question':'隨機實驗 treatment 組平均 75、control 組平均 70。差均值是多少？','answer':'5。','explanation':'75-70=5；完整遵從且設計有效時，這是最直接的 treatment-control 效果估計。'},
    {'id':'ch15-q02','chapterId':'ch15','question':'treatment 組平均 82、control 組平均 76。差均值是多少？','answer':'6。','explanation':'82-76=6。'},
    {'id':'ch15-q03','chapterId':'ch15','question':'ATE 的潛在結果表示式是什麼？','answer':'E[Y(1)-Y(0)]。','explanation':'它是同一母體中處置與未處置潛在結果差的平均。'},
    {'id':'ch15-q04','chapterId':'ch15','question':'有 noncompliance 時，ITT 是按實際接受 treatment 還是按原始 assignment 分組？','answer':'按原始隨機 assignment 分組。','explanation':'這樣保留隨機化設計所提供的可比性。'},
    {'id':'ch15-q05','chapterId':'ch15','question':'隨機分派是否要求這一次樣本中的每一個 baseline covariate 平均值完全一樣？','answer':'不要求。','explanation':'隨機化是機率機制；有限樣本中仍可能有偶然不平衡，重點是 assignment 在設計上與潛在結果獨立。'},

    {'id':'ch16-q01','chapterId':'ch16','question':'Treatment 由 50 升到 70，Control 由 45 升到 55。DiD 是多少？','answer':'10。','explanation':'(70-50)-(55-45)=20-10=10。'},
    {'id':'ch16-q02','chapterId':'ch16','question':'Treatment 由 40 升到 58，Control 由 35 升到 43。DiD 是多少？','answer':'10。','explanation':'(58-40)-(43-35)=18-8=10。'},
    {'id':'ch16-q03','chapterId':'ch16','question':'Parallel trends 的意思是政策後兩組結果水準必須相同嗎？','answer':'不是。','explanation':'它關心的是「若沒有處置」兩組的反事實趨勢可比較，而不是要求水準相同。'},
    {'id':'ch16-q04','chapterId':'ch16','question':'所有處置前 event-study 係數都不顯著，是否足以數學上證明 parallel trends？','answer':'不足以。','explanation':'Pre-trend 檢查只能提供支持或警訊；低檢定力與不可觀察反事實使它不能完全證明識別假設。'},
    {'id':'ch16-q05','chapterId':'ch16','question':'政策在學校層級分派、學生有多期觀察時，標準誤通常最少要考慮哪種相關？','answer':'同一處置／學校群組內的相關，常需在適當群組層級 cluster。','explanation':'不能因學生筆數很多就把所有 person-time 觀察當彼此獨立。'},

    {'id':'ch17-q01','chapterId':'ch17','question':'Sharp RDD 在 cutoff 左側局部預測 62、右側 68。結果跳躍是多少？','answer':'6。','explanation':'右側極限減左側極限=68-62=6。'},
    {'id':'ch17-q02','chapterId':'ch17','question':'cutoff 左側預測 10、右側 13，sharp RDD 跳躍是多少？','answer':'3。','explanation':'13-10=3。'},
    {'id':'ch17-q03','chapterId':'ch17','question':'RDD 在一般條件下最直接識別的是整個母體 ATE 還是 cutoff 附近的 local effect？','answer':'Cutoff 附近的 local effect。','explanation':'設計靠門檻附近的局部可比性；向遠離 cutoff 的個體外推需要額外假設。'},
    {'id':'ch17-q04','chapterId':'ch17','question':'若個體能精確操弄 running variable 以跨過 cutoff，為什麼會威脅 RDD？','answer':'門檻兩側個體可能不再具有局部可比性。','explanation':'排序／操弄可能讓未觀察特徵在 cutoff 也不連續，破壞 continuity 識別直覺。'},
    {'id':'ch17-q05','chapterId':'ch17','question':'Fuzzy RDD 的局部 Wald ratio 分子與分母分別是什麼？','answer':'分子是 cutoff 處 Y 的跳躍；分母是 cutoff 處 treatment probability／D 的跳躍。','explanation':'它把門檻對結果的 reduced-form 跳躍除以門檻對 treatment 的 first-stage 跳躍。'},

    {'id':'ch18-q01','chapterId':'ch18','question':'Test errors 為 1、-2、3。MAE 是多少？','answer':'2。','explanation':'(|1|+|-2|+|3|)/3=(1+2+3)/3=2。'},
    {'id':'ch18-q02','chapterId':'ch18','question':'Test errors 為 1、-2、3。RMSE 約多少？','answer':'約 2.160。','explanation':'sqrt[(1²+(-2)²+3²)/3]=sqrt(14/3)≈2.160。'},
    {'id':'ch18-q03','chapterId':'ch18','question':'一模型 training RMSE=0.5、test RMSE=3；另一模型 training RMSE=1.2、test RMSE=1.8。若目標是新資料預測，哪個較好？','answer':'第二個模型。','explanation':'樣本外 test RMSE 1.8 小於 3；預測重點是未看資料，不是只追求 training fit。'},
    {'id':'ch18-q04','chapterId':'ch18','question':'Test R² 可以小於 0 嗎？','answer':'可以。','explanation':'若樣本外 SSE 大於以 test mean 為基準的 TSS，定義下的 test R² 會是負值。'},
    {'id':'ch18-q05','chapterId':'ch18','question':'樣本外預測較準是否足以證明模型中的 X 係數是因果效果？','answer':'不足以。','explanation':'Prediction 與 causal identification 是不同目標；預測可利用非因果相關訊號。'},

    {'id':'ch19-q01','chapterId':'ch19','question':'研究流程中，Estimand 與 estimator 哪一個原則上應先由研究問題決定？','answer':'Estimand。','explanation':'先定義要知道的母體量，再選能在相應假設下估它的 estimator。'},
    {'id':'ch19-q02','chapterId':'ch19','question':'政策就業 LPM 係數 0.04、cluster-robust SE=0.015。係數效果應如何用百分點表達？','answer':'約提高 4 個百分點，標準誤為 1.5 個百分點。','explanation':'0.04 與 0.015 都是機率單位，乘 100 分別得到 4 與 1.5 個百分點。'},
    {'id':'ch19-q03','chapterId':'ch19','question':'只報「p<0.05」而不報係數、單位與信賴區間，主要缺少什麼？','answer':'效果大小與估計不確定性的實質資訊。','explanation':'顯著性不能替代 effect size、單位與 uncertainty。'},
    {'id':'ch19-q04','chapterId':'ch19','question':'Robustness check 的目的是否是嘗試很多規格直到找到顯著結果？','answer':'不是。','explanation':'合理的 robustness check 是檢查主要結論是否過度依賴可爭議的單一設定，而不是 specification searching。'},
    {'id':'ch19-q05','chapterId':'ch19','question':'一個陌生因果實證題，較穩健的回答順序為何？','answer':'Estimand → Identification → Estimator → Inference → Interpretation／limits。','explanation':'先知道要估什麼與靠什麼假設識別，再談估計方法、標準誤與結果解讀。'},
]
