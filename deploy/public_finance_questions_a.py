from __future__ import annotations

QUESTIONS_A = [
    {'id':'ch00-q01','chapterId':'ch00','question':'「提高某項稅會使交易量下降多少」主要屬於實證分析還是規範分析？','answer':'實證分析。','explanation':'它在描述政策造成的可觀察結果；若問「因此是否應提高稅」才需要額外的規範判準。'},
    {'id':'ch00-q02','chapterId':'ch00','question':'政府今年支出大於收入 NT$80 億。這個 NT$80 億首先描述的是赤字還是債務存量？','answer':'赤字。','explanation':'支出與收入在一段期間的差額是流量；債務是歷年累積的存量。'},
    {'id':'ch00-q03','chapterId':'ch00','question':'某公共方案一年社會總效益 NT$1,200 萬、社會總成本 NT$900 萬。忽略分配與風險時，社會淨效益是多少？','answer':'NT$300 萬。','explanation':'社會淨效益=1,200-900=NT$300 萬；正值只代表總量效率證據，不代表每個人都變好。'},
    {'id':'ch00-q04','chapterId':'ch00','question':'某改革提高總剩餘，但低所得者承擔較多損失。能否只因總剩餘提高就說它「比較公平」？','answer':'不能。','explanation':'效率與公平是不同判準；總剩餘可用於效率分析，但公平需要另外說明分配與價值準則。'},
    {'id':'ch00-q05','chapterId':'ch00','question':'政府把某計畫預算由 NT$5 億提高到 NT$6 億，是否能直接推出社會福利增加 NT$1 億？','answer':'不能。','explanation':'預算增加是會計支出，不是福利本身；必須比較新增支出的社會效益、機會成本與融資扭曲。'},

    {'id':'ch01-q01','chapterId':'ch01','question':'什麼是 Pareto 改善？','answer':'至少一人變好，而且沒有人變差。','explanation':'只要有任何人變差，就不能稱為實際 Pareto 改善。'},
    {'id':'ch01-q02','chapterId':'ch01','question':'存在未內部化的污染外部性時，可以直接用第一福利經濟學定理斷言競爭均衡 Pareto 有效率嗎？','answer':'不可以。','explanation':'第一福利定理需要無外部性等條件；污染外部性使私人價格未反映完整社會成本。'},
    {'id':'ch01-q03','chapterId':'ch01','question':'某無外部性的市場中，消費者剩餘 NT$120 萬、生產者剩餘 NT$80 萬。總剩餘是多少？','answer':'NT$200 萬。','explanation':'TS=CS+PS=120+80=NT$200 萬。'},
    {'id':'ch01-q04','chapterId':'ch01','question':'改革使甲增加 NT$120、乙損失 NT$20，且沒有補償。若暫以金額代表福利，這是 Pareto 改善嗎？','answer':'不是。','explanation':'乙變差，因此不是 Pareto 改善；最多只能討論總淨得益或潛在補償。'},
    {'id':'ch01-q05','chapterId':'ch01','question':'社會福利函數 W(U1,…,Un) 的權重能否只靠效率理論唯一決定？','answer':'不能。','explanation':'不同人的福利如何加總包含規範價值判斷；效率理論本身不能唯一給出社會權重。'},

    {'id':'ch02-q01','chapterId':'ch02','question':'「市場價格很高，所以一定有市場失靈」這句話對嗎？','answer':'不對。','explanation':'市場失靈是市場無法在特定條件下達成有效率配置；價格高本身不等於外部性、公共財、資訊問題或市場力。'},
    {'id':'ch02-q02','chapterId':'ch02','question':'某活動的私人邊際成本 MPC=NT$70、邊際外部成本 MEC=NT$40。社會邊際成本 MSC 是多少？','answer':'NT$110。','explanation':'MSC=MPC+MEC=70+40=NT$110。'},
    {'id':'ch02-q03','chapterId':'ch02','question':'政府出資但委託民間公司提供服務，是否仍可稱為公共提供？','answer':'可以。','explanation':'公共提供重點是政府負責供給或融資，不必等同政府親自生產。'},
    {'id':'ch02-q04','chapterId':'ch02','question':'什麼是政府失靈？','answer':'政策因資訊、誘因、行政或政治程序等因素產生足以抵銷政策利益的成本。','explanation':'發現市場失靈不代表任何政府介入都必然改善；應比較可行方案。'},
    {'id':'ch02-q05','chapterId':'ch02','question':'若某污染有明確不可超過的安全總量上限，純粹用價格型污染稅一定比數量管制更合適嗎？','answer':'不一定。','explanation':'工具選擇取決於資訊、不確定性與損害型態；存在硬性安全臨界值時數量工具可能更直接。'},

    {'id':'ch03-q01','chapterId':'ch03','question':'純公共財的兩個核心特徵是什麼？','answer':'非敵對性與非排他性。','explanation':'判斷公共財看消費與排除技術，不是看它是否由政府提供。'},
    {'id':'ch03-q02','chapterId':'ch03','question':'公共財的個人邊際願付價格應在同一數量下垂直加總，還是像私人財一樣把數量橫向加總？','answer':'在同一數量下垂直加總。','explanation':'每個人同時消費同一公共財數量，因此社會邊際效益是個人 MB 的垂直加總。'},
    {'id':'ch03-q03','chapterId':'ch03','question':'兩人對某公共財下一單位的邊際願付價格分別是 NT$600 與 NT$400，邊際成本 NT$800。依 Samuelson 條件，這一單位應提供嗎？','answer':'應提供。','explanation':'總邊際願付=600+400=NT$1,000，高於 NT$800 的邊際成本。'},
    {'id':'ch03-q04','chapterId':'ch03','question':'若下一單位公共財的兩人邊際願付價格是 NT$350 與 NT$250，邊際成本仍為 NT$800，應繼續提供嗎？','answer':'不應。','explanation':'社會邊際效益只有 NT$600，低於 NT$800 邊際成本。'},
    {'id':'ch03-q05','chapterId':'ch03','question':'一座可收費且在未擁擠時多人同時使用幾乎不互相影響的設施，比較接近純公共財還是俱樂部財？','answer':'俱樂部財。','explanation':'可排他但在未擁擠時近似非敵對，是俱樂部財的典型特徵。'},

    {'id':'ch04-q01','chapterId':'ch04','question':'若 MPC=NT$80、MEC=NT$25，社會邊際成本 MSC 為多少？','answer':'NT$105。','explanation':'MSC=MPC+MEC=80+25=NT$105。'},
    {'id':'ch04-q02','chapterId':'ch04','question':'社會最適數量 Q* 處的邊際外部損害 MEC(Q*)=NT$25。簡化 Pigouvian 稅每單位應約設多少？','answer':'NT$25。','explanation':'在標準簡化模型中，t*=MEC(Q*)，使私人決策者面對完整社會邊際成本。'},
    {'id':'ch04-q03','chapterId':'ch04','question':'生產具有負外部性且未受政策矯正時，市場產量通常相對社會有效率產量偏高還是偏低？','answer':'偏高。','explanation':'MPC 低於 MSC，私人決策忽略外部成本，因此生產過多。'},
    {'id':'ch04-q04','chapterId':'ch04','question':'Coase 協商較可能有效，需要哪些關鍵條件？','answer':'產權清楚、交易成本很低，且協商參與者與資訊條件足以支持交易。','explanation':'Coase 結果依賴強條件；交易成本很高時不能用定理否定政府角色。'},
    {'id':'ch04-q05','chapterId':'ch04','question':'可交易排放許可在交易順利時，為什麼能降低達成既定總減量的成本？','answer':'因為交易會讓不同污染源的邊際減量成本趨於一致。','explanation':'減量成本低者多減、成本高者少減並購買許可，可用較低總成本達成同一排放上限。'},

    {'id':'ch05-q01','chapterId':'ch05','question':'5 位單峰選民的理想政策點依序是 20、40、50、80、100。中位數選民的理想點是多少？','answer':'50。','explanation':'排序後第 3 位是中位數選民；在一維、單峰等條件下具有關鍵地位。'},
    {'id':'ch05-q02','chapterId':'ch05','question':'7 位選民依單一政策理想點排序後，中位數是第幾位？','answer':'第 4 位。','explanation':'奇數 n 的中位數位置為 (n+1)/2=(7+1)/2=4。'},
    {'id':'ch05-q03','chapterId':'ch05','question':'社會多數偏好出現 A 勝 B、B 勝 C、C 又勝 A，這稱為什麼？','answer':'投票悖論或循環多數。','explanation':'群體的兩兩多數關係可能不具傳遞性，因此議程順序會影響結果。'},
    {'id':'ch05-q04','chapterId':'ch05','question':'企業花費大量真實資源遊說取得只把既有利益轉給自己的特權，這類投入常稱為什麼？','answer':'尋租。','explanation':'尋租把資源用在爭取政策租金而非創造新產出，其真實資源投入可能形成社會成本。'},
    {'id':'ch05-q05','chapterId':'ch05','question':'中位數選民定理可否無條件套用到多維政策與任意偏好？','answer':'不可以。','explanation':'它依賴一維政策、單峰偏好與特定投票程序等條件。'},

    {'id':'ch06-q01','chapterId':'ch06','question':'一年後的 NT$110，在年折現率 10% 下現值是多少？','answer':'NT$100。','explanation':'PV=110/1.1=NT$100。'},
    {'id':'ch06-q02','chapterId':'ch06','question':'某方案現在成本 NT$100 萬，一年後效益 NT$70 萬、兩年後效益 NT$60 萬，折現率 10%。NPV 約多少？','answer':'約 NT$13.22 萬。','explanation':'NPV=-100+70/1.1+60/1.1²≈13.223（萬元）。'},
    {'id':'ch06-q03','chapterId':'ch06','question':'已支付且無法回收、也不因目前方案選擇改變的研究費，是否應列入未來方案的增量成本？','answer':'不應。','explanation':'這是沉沒成本；目前決策應比較未來可改變的增量成本與效益。'},
    {'id':'ch06-q04','chapterId':'ch06','question':'當市場價格因稅補貼或其他扭曲不能反映社會機會成本時，CBA 常使用什麼概念調整？','answer':'影子價格。','explanation':'影子價格用來估計資源的社會機會成本，而不是盲目照帳面市場價格。'},
    {'id':'ch06-q05','chapterId':'ch06','question':'以實質價格估計的未來效益，能否直接搭配含預期通膨的名目折現率而不調整？','answer':'不宜。','explanation':'現金流與折現率必須口徑一致：實質配實質，名目配名目。'},

    {'id':'ch07-q01','chapterId':'ch07','question':'100 人中有 20 人所得低於採用的貧窮線，貧窮率是多少？','answer':'20%。','explanation':'poverty rate=20/100=20%。'},
    {'id':'ch07-q02','chapterId':'ch07','question':'完全平等分配的 Gini coefficient 理想值是多少？','answer':'0。','explanation':'Lorenz curve 與完全平等線重合時，兩者間面積 A=0，因此 G=0。'},
    {'id':'ch07-q03','chapterId':'ch07','question':'在其他定義一致時，Lorenz curve 越接近 45 度完全平等線，所得分配通常越平等還是越不平等？','answer':'越平等。','explanation':'偏離完全平等線的面積縮小，Gini 通常也較低。'},
    {'id':'ch07-q04','chapterId':'ch07','question':'兩個地區的貧窮率都為 10%，能否由此斷言貧窮者距離貧窮線的缺口也一樣？','answer':'不能。','explanation':'貧窮率只計低於線的人數比例；貧窮缺口才反映低於線的深度。'},
    {'id':'ch07-q05','chapterId':'ch07','question':'某福利每多賺 NT$1 就減少給付 NT$1，暫不考慮其他稅。這項退場機制本身形成的隱含邊際稅率是多少？','answer':'100%。','explanation':'多賺 NT$1 同時少拿 NT$1，新增市場所得沒有增加可支配所得。'},

    {'id':'ch08-q01','chapterId':'ch08','question':'高風險者在投保前更願意購買保險，導致風險池惡化，這是逆選擇還是道德風險？','answer':'逆選擇。','explanation':'逆選擇是交易前的隱藏風險類型問題；道德風險通常是保障後的行為反應。'},
    {'id':'ch08-q02','chapterId':'ch08','question':'4 名工作者各領 NT$50,000，PAYG 繳費率 10%，共同支應 1 名退休者。忽略其他收入與成本時，可支應給付多少？','answer':'NT$20,000。','explanation':'4×50,000×10%=NT$20,000。'},
    {'id':'ch08-q03','chapterId':'ch08','question':'延續上一題，若退休者增加為 2 人、其他條件不變且平均分配，每名退休者可支應多少？','answer':'NT$10,000。','explanation':'總繳費仍 NT$20,000，兩人平均各 NT$10,000。'},
    {'id':'ch08-q04','chapterId':'ch08','question':'退休給付 NT$30,000、退休前參考薪資 NT$50,000，替代率是多少？','answer':'60%。','explanation':'replacement rate=30,000/50,000=60%。'},
    {'id':'ch08-q05','chapterId':'ch08','question':'完全提存制與 PAYG 最核心的融資差異是什麼？','answer':'完全提存制先累積資產供未來給付；PAYG 主要用當期工作者繳費支付當期受益者。','explanation':'兩者都可能有公共管理，但資金跨期來源不同。'},

    {'id':'ch09-q01','chapterId':'ch09','question':'醫療完整價格 NT$2,000，共同保險率 20%。病患邊際自付價格是多少？','answer':'NT$400。','explanation':'P_patient=cP=0.2×2,000=NT$400。'},
    {'id':'ch09-q02','chapterId':'ch09','question':'醫療完整價格 NT$3,000，共同保險率 30%。病患邊際自付價格是多少？','answer':'NT$900。','explanation':'0.3×3,000=NT$900。'},
    {'id':'ch09-q03','chapterId':'ch09','question':'投保後因自付價格下降而增加就醫，這主要屬於哪種保險問題？','answer':'道德風險。','explanation':'保障改變了使用者在邊際上的價格與行為。'},
    {'id':'ch09-q04','chapterId':'ch09','question':'按服務量付費可能鼓勵提供者增加服務數量。這是在分析病患端還是供給者端誘因？','answer':'供給者端誘因。','explanation':'醫療政策必須同時分析需求端保障與提供者支付制度。'},
    {'id':'ch09-q05','chapterId':'ch09','question':'降低病患共付率後醫療使用增加，能否直接說所有新增使用都是無效率浪費？','answer':'不能。','explanation':'新增使用可能同時包含高價值治療與低價值使用；要比較健康效益與成本。'},
]
