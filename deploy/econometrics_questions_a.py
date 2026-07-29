from __future__ import annotations

QUESTIONS_A = [
    {'id':'ch00-q01','chapterId':'ch00','question':'研究者只想描述樣本中教育年數與薪資的線性關係。此時 OLS 斜率一定需要因果識別假設才能作描述嗎？','answer':'不一定。','explanation':'若目標只是描述樣本線性關係，OLS 可作描述統計；只有把斜率解讀為教育的因果效果時才需要額外識別假設。'},
    {'id':'ch00-q02','chapterId':'ch00','question':'同一批 500 家公司被連續追蹤 8 年，這屬於哪種資料結構？','answer':'縱橫資料（panel data）。','explanation':'同時具有多個個體與多個時點，且追蹤相同個體。'},
    {'id':'ch00-q03','chapterId':'ch00','question':'「把樣本資料代入 OLS 公式後得到 1.7」中的 1.7 是 estimator 還是 estimate？','answer':'Estimate（估計值）。','explanation':'Estimator 是從資料到數值的計算規則；某一份樣本算出的具體 1.7 是 estimate。'},
    {'id':'ch00-q04','chapterId':'ch00','question':'Identification（識別）主要在問什麼？','answer':'在給定資料與假設下，目標參數能否和其他可能機制區分並被確定。','explanation':'識別先於估計；即使演算法能算出係數，也不代表它就是研究想要的因果參數。'},
    {'id':'ch00-q05','chapterId':'ch00','question':'一條薪資迴歸的 R²=0.90，能否只憑這點判定教育係數是因果效果？','answer':'不能。','explanation':'R² 是樣本內配適度，不提供處理遺漏變數、反向因果或其他內生性的識別保證。'},

    {'id':'ch01-q01','chapterId':'ch01','question':'樣本數 n=100、樣本標準差 s=10。樣本平均的估計標準誤是多少？','answer':'1。','explanation':'SE(xbar)=s/sqrt(n)=10/10=1。'},
    {'id':'ch01-q02','chapterId':'ch01','question':'s 不變時，樣本數從 100 增加到 400，樣本平均的標準誤變成原來幾倍？','answer':'1/2。','explanation':'SE 與 1/sqrt(n) 成比例；sqrt(400)/sqrt(100)=2，所以 SE 減半。'},
    {'id':'ch01-q03','chapterId':'ch01','question':'若 E(X)=4，求 E(2+3X)。','answer':'14。','explanation':'期望值線性：E(2+3X)=2+3E(X)=2+12=14。'},
    {'id':'ch01-q04','chapterId':'ch01','question':'若 Var(X)=4，求 Var(2+3X)。','answer':'36。','explanation':'平移常數不影響變異數，Var(2+3X)=3²Var(X)=9×4=36。'},
    {'id':'ch01-q05','chapterId':'ch01','question':'樣本平均 52、H0: mu=50、平均數標準誤為 1。t 統計量是多少？','answer':'2。','explanation':'t=(52-50)/1=2。'},

    {'id':'ch02-q01','chapterId':'ch02','question':'資料 X=(1,2,3)、Y=(2,3,5)。簡單 OLS 斜率是多少？','answer':'1.5。','explanation':'xbar=2、ybar=10/3；斜率分子為 3，分母為 2，所以 hat beta1=3/2=1.5。'},
    {'id':'ch02-q02','chapterId':'ch02','question':'延續 X=(1,2,3)、Y=(2,3,5)，OLS 截距是多少？','answer':'1/3，約 0.333。','explanation':'hat beta0=ybar-hat beta1 xbar=10/3-1.5×2=1/3。'},
    {'id':'ch02-q03','chapterId':'ch02','question':'含截距 OLS 的樣本殘差加總通常等於多少？','answer':'0。','explanation':'OLS 一階條件使殘差與常數項正交，因此 sum(hat u_i)=0。'},
    {'id':'ch02-q04','chapterId':'ch02','question':'若本書定義 RSS=殘差平方和，TSS=100、RSS=20，R² 是多少？','answer':'0.80。','explanation':'R²=1-RSS/TSS=1-20/100=0.80。'},
    {'id':'ch02-q05','chapterId':'ch02','question':'X 在樣本中完全沒有變化時，為什麼簡單 OLS 斜率不能估？','answer':'因為斜率公式分母 sum(x_i-xbar)^2=0。','explanation':'沒有 X 的樣本變動，就沒有可用來辨認斜率的資訊。'},

    {'id':'ch03-q01','chapterId':'ch03','question':'簡單迴歸中 sigma²=4、Sxx=sum(x_i-xbar)²=20。Var(hat beta1|X) 是多少？','answer':'0.20。','explanation':'Var(hat beta1|X)=sigma²/Sxx=4/20=0.20。'},
    {'id':'ch03-q02','chapterId':'ch03','question':'延續上一題，hat beta1 的條件標準差約是多少？','answer':'約 0.447。','explanation':'sqrt(0.20)≈0.447。'},
    {'id':'ch03-q03','chapterId':'ch03','question':'若 E(u|X)=0 仍成立，但存在 heteroskedasticity，OLS 係數是否因此必然有偏？','answer':'否。','explanation':'同方差不是 OLS 無偏的必要條件；異質變異主要破壞傳統標準誤與 Gauss–Markov 效率結論。'},
    {'id':'ch03-q04','chapterId':'ch03','question':'Gauss–Markov 定理中的 BLUE，「Best」是在比較哪一類估計量？','answer':'線性且無偏的估計量。','explanation':'在相應線性模型與同方差等條件下，OLS 在線性無偏估計量中具有最小變異數。'},
    {'id':'ch03-q05','chapterId':'ch03','question':'其他條件固定時，Sxx 變成原來 4 倍，簡單 OLS 斜率的標準差變成原來幾倍？','answer':'1/2。','explanation':'標準差與 1/sqrt(Sxx) 成比例；Sxx 乘 4，標準差除以 2。'},

    {'id':'ch04-q01','chapterId':'ch04','question':'多元迴歸中 beta1 的 ceteris paribus 解釋是什麼？','answer':'在模型中其他解釋變數固定時，X1 增加一單位與 Y 條件平均的線性變化。','explanation':'它不是 X1 與 Y 的無條件簡單相關。'},
    {'id':'ch04-q02','chapterId':'ch04','question':'n=100、k=3、R²=0.40。含截距模型的 adjusted R² 約是多少？','answer':'約 0.381。','explanation':'1-(1-0.40)×(99/96)=1-0.61875=0.38125。'},
    {'id':'ch04-q03','chapterId':'ch04','question':'含截距 OLS 中加入一個新解釋變數，普通 R² 會下降嗎？','answer':'不會。','explanation':'OLS 至少可以把新係數設為 0，因此殘差平方和不會增加，普通 R² 不會下降；adjusted R² 則可能下降。'},
    {'id':'ch04-q04','chapterId':'ch04','question':'Frisch–Waugh–Lovell 的 partialling-out 直覺是什麼？','answer':'先把 X1 與 Y 中可由其他控制變數線性解釋的部分扣掉，再用剩餘部分估 X1 的係數。','explanation':'這說明多元迴歸係數利用的是控制其他變數後的 X1 變動。'},
    {'id':'ch04-q05','chapterId':'ch04','question':'若目標是 treatment 的總因果效果，處置發生後才產生的變數是否一定適合當控制？','answer':'不一定，通常要非常小心。','explanation':'處置後控制可能切斷部分因果路徑或引入選擇偏誤；控制選擇應由因果結構與 estimand 決定。'},

    {'id':'ch05-q01','chapterId':'ch05','question':'真實 beta1=5，遺漏變數對 Y 的效果 beta2=3，且 Z 對 X 的線性關係 delta1=0.2。短迴歸斜率約多少？','answer':'5.6。','explanation':'tilde beta1=beta1+beta2 delta1=5+3×0.2=5.6。'},
    {'id':'ch05-q02','chapterId':'ch05','question':'若 beta2>0、delta1<0，遺漏變數偏誤方向為何？','answer':'向下偏。','explanation':'OVB=beta2×delta1<0，所以短迴歸斜率低於目標 beta1。'},
    {'id':'ch05-q03','chapterId':'ch05','question':'某遺漏 Z 影響 Y，但與 X 完全無線性關係（delta1=0）。在簡化 OVB 公式中它造成多少偏誤？','answer':'0。','explanation':'OVB=beta2 delta1；delta1=0 時這個特定遺漏變數不造成簡化線性 OVB。'},
    {'id':'ch05-q04','chapterId':'ch05','question':'Y 會反過來影響 X，使 X 與結構誤差相關。這屬於哪一類問題？','answer':'反向因果造成的內生性。','explanation':'此時 OLS 一般不能直接識別 X 對 Y 的單向因果效果。'},
    {'id':'ch05-q05','chapterId':'ch05','question':'改用 heteroskedasticity-robust SE 可以修正 omitted-variable bias 嗎？','answer':'不能。','explanation':'Robust SE 修正的是抽樣變異估計，不會把內生的 OLS 點估計變成無偏因果效果。'},

    {'id':'ch06-q01','chapterId':'ch06','question':'hat beta=2.4、SE=0.6，檢定 H0: beta=0 的 t 統計量是多少？','answer':'4。','explanation':'t=(2.4-0)/0.6=4。'},
    {'id':'ch06-q02','chapterId':'ch06','question':'hat beta=2.4、SE=0.6，用 1.96 作大樣本 95% 臨界值，近似信賴區間是多少？','answer':'約 [1.224, 3.576]。','explanation':'2.4±1.96×0.6=2.4±1.176。'},
    {'id':'ch06-q03','chapterId':'ch06','question':'hat beta=1、SE=0.5，檢定 H0: beta=0 的 t 統計量是多少？','answer':'2。','explanation':'t=1/0.5=2。'},
    {'id':'ch06-q04','chapterId':'ch06','question':'F 檢定公式中的 q 通常代表什麼？','answer':'同時檢驗的線性限制個數。','explanation':'例如同時令兩個斜率為 0，q=2。'},
    {'id':'ch06-q05','chapterId':'ch06','question':'某雙尾檢定 p-value=0.08，在 5% 顯著水準下應如何判斷？','answer':'不拒絕 H0。','explanation':'0.08>0.05；這不是證明 H0 為真，只是樣本證據不足以在 5% 水準拒絕。'},

    {'id':'ch07-q01','chapterId':'ch07','question':'log(Y)=beta0+0.02X+u。X 增加 1 單位時，Y 約變動多少百分比？','answer':'約增加 2%。','explanation':'log-level 模型的小變化近似為 100×0.02=2%。'},
    {'id':'ch07-q02','chapterId':'ch07','question':'Y=beta0+20 log(X)+u。X 增加 1% 時，Y 約改變多少個 Y 單位？','answer':'約增加 0.20 個 Y 單位。','explanation':'level-log 模型中 1% 的 X 變化約對應 beta/100=20/100=0.20。'},
    {'id':'ch07-q03','chapterId':'ch07','question':'log(Y)=beta0+0.6 log(X)+u。0.6 應如何解讀？','answer':'X 增加 1%，Y 約增加 0.6%。','explanation':'log-log 的斜率是彈性。'},
    {'id':'ch07-q04','chapterId':'ch07','question':'log(Y) 迴歸中的 dummy 係數為 0.1823。用精確公式 100(exp(beta)-1)% 的效果約多少？','answer':'約 20%。','explanation':'100×(exp(0.1823)-1)≈19.997%，約 20%。'},
    {'id':'ch07-q05','chapterId':'ch07','question':'Y=beta0+1.2X+beta2 D+0.3(XD)+u。D=1 組的 X 斜率是多少？','answer':'1.5。','explanation':'D=1 時 X 的斜率=beta1+beta3=1.2+0.3=1.5。'},

    {'id':'ch08-q01','chapterId':'ch08','question':'OLS 係數 1.2、heteroskedasticity-robust SE=0.4。檢定 H0: beta=0 的 robust t 是多少？','answer':'3。','explanation':'t=1.2/0.4=3。'},
    {'id':'ch08-q02','chapterId':'ch08','question':'外生性成立但有 heteroskedasticity，OLS 點估計是否因此必然有偏？','answer':'否。','explanation':'異質變異主要影響傳統標準誤與效率；外生性仍成立時 OLS 點估計不因此必然有偏。'},
    {'id':'ch08-q03','chapterId':'ch08','question':'從 conventional SE 改成 robust SE，是否通常要重新計算 OLS 係數本身？','answer':'不用。','explanation':'同一 OLS 點估計保留，主要替換其 estimated variance／standard error。'},
    {'id':'ch08-q04','chapterId':'ch08','question':'Robust SE 能否修正反向因果造成的內生性？','answer':'不能。','explanation':'內生性是點估計的識別問題，不是只靠換標準誤能解決。'},
    {'id':'ch08-q05','chapterId':'ch08','question':'若 Var(u_i|X_i) 已知，理想 WLS 權重通常與什麼量成比例？','answer':'與條件誤差變異數的倒數成比例。','explanation':'高變異觀察值通常給較低權重；精確形式依模型的權重定義而定。'},

    {'id':'ch09-q01','chapterId':'ch09','question':'把 X_j 對其他解釋變數迴歸得到 R_j²=0.80。VIF_j 是多少？','answer':'5。','explanation':'VIF=1/(1-R_j²)=1/0.2=5。'},
    {'id':'ch09-q02','chapterId':'ch09','question':'高度但非完全多重共線性，在外生性成立時主要傷害 OLS 的偏誤還是精確度？','answer':'主要傷害精確度。','explanation':'它常使標準誤變大、個別係數難以精確估計；不會單靠共線性就製造系統性 OLS 偏誤。'},
    {'id':'ch09-q03','chapterId':'ch09','question':'完全多重共線性時，相關係數為什麼無法分別估？','answer':'因為設計矩陣缺乏獨立變動，相關係數不具唯一解。','explanation':'某解釋變數可由其他解釋變數精確線性表示，無法分離各自效果。'},
    {'id':'ch09-q04','chapterId':'ch09','question':'經典 X 測量誤差中，Var(X*)=4、Var(v)=1、真實 beta=2。簡單模型的機率極限約多少？','answer':'1.6。','explanation':'attenuation factor=4/(4+1)=0.8，所以 plim hat beta=2×0.8=1.6。'},
    {'id':'ch09-q05','chapterId':'ch09','question':'「所有測量誤差都一定把係數往 0 拉」是否正確？','answer':'不正確。','explanation':'往 0 的 attenuation 是經典解釋變數測量誤差的特定結果；更一般測量誤差可有不同偏誤方向。'},
]
