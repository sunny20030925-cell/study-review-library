from __future__ import annotations

QUESTIONS_A = [
{'id':'ch00-q01','chapterId':'ch00','question':'賽局理論與一般單人決策分析最核心的差別是什麼？','answer':'結果會策略性地依賴其他決策者的選擇。','explanation':'賽局題的報酬不只由自己的行動決定，還取決於其他玩家如何行動，因此必須同時分析彼此最佳回應。'},
{'id':'ch00-q02','chapterId':'ch00','question':'在動態賽局中，「策略」是否通常只等於玩家實際走到的那一步行動？','answer':'不是。','explanation':'策略是完整應變計畫，必須指定玩家在所有可能遇到的決策情況下要做什麼，包括均衡路徑外。'},
{'id':'ch00-q03','chapterId':'ch00','question':'兩家店原本同時定價，改成 A 先公開價格、B 再定價。是否可以不改模型、直接沿用原本的同時行動矩陣？','answer':'不宜。','explanation':'先後順序改變了資訊與策略空間，應以展開式賽局或等價的動態表示重新分析。'},
{'id':'ch00-q04','chapterId':'ch00','question':'賽局中的 payoff 是否一定等於實際收到的新臺幣金額？','answer':'不一定。','explanation':'payoff 用來表示偏好排序；金錢常可當代理，但若風險、名聲或其他目標重要，報酬應反映完整偏好。'},
{'id':'ch00-q05','chapterId':'ch00','question':'題目有先後行動且玩家完全知道前面實際發生的行動時，第一個應檢查的模型特徵是什麼？','answer':'動態時序與賽局樹。','explanation':'先把決策節點、行動順序與資訊畫清楚，再決定是否使用向後歸納與 SPNE。'},

{'id':'ch01-q01','chapterId':'ch01','question':'玩家 A 的報酬矩陣中，若 B 選 L 時 A 選 U 得4、選 D 得2，則 BR_A(L) 是什麼？','answer':'U。','explanation':'固定 B=L，比較 A 的4與2，U 給較高報酬。'},
{'id':'ch01-q02','chapterId':'ch01','question':'若 B 選 R 時 A 選 U 得1、選 D 得3，則 BR_A(R) 是什麼？','answer':'D。','explanation':'固定 B=R，比較 A 的1與3，D 是最佳回應。'},
{'id':'ch01-q03','chapterId':'ch01','question':'某玩家對同一個對手策略，兩個自己的策略都得到5。最佳回應可以有兩個嗎？','answer':'可以。','explanation':'最佳回應集合可以包含多個同樣最大化報酬的策略。'},
{'id':'ch01-q04','chapterId':'ch01','question':'找 2×2 矩陣中的純策略 Nash 均衡時，標記最佳回應後要找什麼？','answer':'兩位玩家最佳回應的交會格。','explanation':'一格若同時是列玩家對該欄的最佳回應、也是欄玩家對該列的最佳回應，就滿足純策略 Nash 的互為最佳回應條件。'},
{'id':'ch01-q05','chapterId':'ch01','question':'「最佳回應」是否代表某策略不論對手怎麼做都最好？','answer':'不是。','explanation':'最佳回應是條件式概念；若不論對手策略都最好，才接近優勢策略概念。'},

{'id':'ch02-q01','chapterId':'ch02','question':'若策略 U 在對手每一種可能策略下都比 D 多得到1，U 與 D 的關係是什麼？','answer':'U 嚴格支配 D。','explanation':'對所有對手策略都給更高報酬，符合 strict dominance。'},
{'id':'ch02-q02','chapterId':'ch02','question':'若 U 在所有情況都不比 D 差，且至少一種情況更好，這稱為什麼？','answer':'U 弱支配 D。','explanation':'weak dominance 要求處處至少一樣好，且至少一處嚴格更好。'},
{'id':'ch02-q03','chapterId':'ch02','question':'反覆刪除嚴格劣勢策略的結果，是否比反覆刪除弱劣勢策略更不依賴刪除順序？','answer':'是。','explanation':'嚴格劣勢刪除有較穩健的順序性質；弱劣勢刪除可能因順序不同而影響剩餘策略與均衡。'},
{'id':'ch02-q04','chapterId':'ch02','question':'某策略只在對手的一種行動下比較差，其他情況反而比較好。能否稱它是嚴格劣勢策略？','answer':'不能。','explanation':'嚴格劣勢要求存在另一個純策略或適當混合策略，在所有對手策略下都嚴格更好。'},
{'id':'ch02-q05','chapterId':'ch02','question':'rationalizable strategy 是否只靠「純策略對純策略」的嚴格支配刪除就一定能完整判定？','answer':'不一定。','explanation':'有限賽局的完整 rationalizability 判定可能需要考慮某純策略是否被一個混合策略嚴格支配，而不只是純策略彼此的一對一比較。'},

{'id':'ch03-q01','chapterId':'ch03','question':'Nash 均衡的「沒有偏離誘因」是檢查單方面偏離還是所有玩家同時改策略？','answer':'單方面偏離。','explanation':'Nash 固定其他玩家策略，只讓一位玩家改變自己的策略並比較報酬。'},
{'id':'ch03-q02','chapterId':'ch03','question':'某策略組合的總報酬在全矩陣最高，是否因此必然是 Nash 均衡？','answer':'不必然。','explanation':'Nash 看的是互為最佳回應，不是總報酬最大。'},
{'id':'ch03-q03','chapterId':'ch03','question':'協調賽局中 (L,L) 與 (R,R) 都是互為最佳回應。此賽局有幾個純策略 Nash 均衡？','answer':'至少兩個： (L,L) 與 (R,R)。','explanation':'每個互為最佳回應的策略組合都是純策略 NE；多重均衡是常見情況。'},
{'id':'ch03-q04','chapterId':'ch03','question':'每個優勢策略均衡是否一定也是 Nash 均衡？','answer':'是。','explanation':'若每位玩家的策略在任何對手行動下都最好，當然也會是對均衡對手策略的最佳回應。'},
{'id':'ch03-q05','chapterId':'ch03','question':'Nash 均衡是否保證 Pareto 有效率？','answer':'不保證。','explanation':'囚徒困境就是經典反例：個別偏離誘因穩定的 Nash 可以被另一結果 Pareto 改善。'},

{'id':'ch04-q01','chapterId':'ch04','question':'混合策略中各純策略機率必須滿足哪兩個基本限制？','answer':'每個機率非負，且總和等於1。','explanation':'任何機率分配都必須滿足 p_k≥0 與 Σp_k=1。'},
{'id':'ch04-q02','chapterId':'ch04','question':'一個 2×2 賽局已經有純策略 Nash equilibrium，是否仍可能另外存在混合策略 Nash equilibrium？','answer':'可能。','explanation':'協調型 2×2 賽局常同時有兩個純策略 NE 與一個內點混合 NE；找到純 NE 不代表可以停止檢查混合均衡。'},
{'id':'ch04-q03','chapterId':'ch04','question':'例題中 A 的 U 報酬為3q、D 報酬為2(1-q)。令 A 無差異可得 q 為多少？','answer':'q=0.4。','explanation':'3q=2-2q，所以5q=2，q=0.4。'},
{'id':'ch04-q04','chapterId':'ch04','question':'例題中 B 的 L 報酬為2p、R 報酬為3(1-p)。令 B 無差異可得 p 為多少？','answer':'p=0.6。','explanation':'2p=3-3p，所以5p=3，p=0.6。'},
{'id':'ch04-q05','chapterId':'ch04','question':'要求「求 A 的混合機率 p」時，為什麼常用 B 的無差異條件？','answer':'因 A 的 p 決定 B 面對各純策略的期望報酬。','explanation':'在內點混合均衡中，A 調整自己的混合機率使 B 願意在其支撐策略間混合。'},

{'id':'ch05-q01','chapterId':'ch05','question':'二人零和賽局中，若列玩家得到 v，欄玩家的報酬是多少？','answer':'-v。','explanation':'零和表示每個結果中兩位玩家報酬總和為0，因此列玩家得到 v 時，欄玩家必須得到 -v。'},
{'id':'ch05-q02','chapterId':'ch05','question':'列玩家報酬矩陣 [[2,-1],[-2,1]] 的兩列最小值分別是多少？','answer':'-1 與 -2。','explanation':'第一列 min(2,-1)=-1；第二列 min(-2,1)=-2。'},
{'id':'ch05-q03','chapterId':'ch05','question':'同一矩陣的純策略 maximin 值是多少？','answer':'-1。','explanation':'在兩列最小值 -1、-2 中取最大值，得到 -1。'},
{'id':'ch05-q04','chapterId':'ch05','question':'若零和賽局的純 maximin 等於純 minimax，代表什麼？','answer':'存在純策略鞍點，兩者共同值就是賽局價值。','explanation':'maximin=minimax 時不需靠混合策略縮小安全值差距。'},
{'id':'ch05-q05','chapterId':'ch05','question':'minimax theorem 能否直接套用到一般非零和協調賽局？','answer':'不能。','explanation':'定理的標準版本針對有限二人零和賽局；一般總和賽局要用一般 Nash 分析。'},

{'id':'ch06-q01','chapterId':'ch06','question':'Cournot 模型中兩家廠商主要選擇的策略變數是什麼？','answer':'產量。','explanation':'Cournot 是同時選產量的寡占模型。'},
{'id':'ch06-q02','chapterId':'ch06','question':'Bertrand 模型中主要策略變數是什麼？','answer':'價格。','explanation':'Bertrand competition 以價格作為同時選擇的策略。'},
{'id':'ch06-q03','chapterId':'ch06','question':'反需求 P=100-Q、兩家邊際成本10的對稱 Cournot 模型中，每家均衡產量是多少？','answer':'30。','explanation':'q_i=(90-q_j)/2；對稱 q_i=q_j=q，故 2q=90-q，3q=90，q=30。'},
{'id':'ch06-q04','chapterId':'ch06','question':'上題 Cournot 均衡總產量與價格各是多少？','answer':'總產量60，價格40。','explanation':'Q=30+30=60，P=100-60=40。'},
{'id':'ch06-q05','chapterId':'ch06','question':'同質商品 Bertrand 模型得到 p=c 是否需要無容量限制等標準條件？','answer':'需要。','explanation':'在相同邊際成本、同質商品、連續價格、無容量限制等標準條件下，純策略均衡是精確的 p1=p2=c；產品差異、容量限制、離散價格或不對稱成本都可能改變結果。'},

{'id':'ch07-q01','chapterId':'ch07','question':'有限完美資訊賽局中的標準向後歸納從賽局樹的哪一端開始？','answer':'從最後的決策節點開始。','explanation':'先求最末端玩家在各可能續局中的最佳行動，再逐層往前替換；若有非單點資訊集合，普通向後歸納不一定足夠。'},
{'id':'ch07-q02','chapterId':'ch07','question':'進入賽局中，若既有廠商在 Fight 得 -1、Accommodate 得1，進入發生後它會選哪個？','answer':'Accommodate。','explanation':'在該決策節點比較自己的續局報酬，1>-1。'},
{'id':'ch07-q03','chapterId':'ch07','question':'若進入者預見 Accommodate 後 In 得2、Out 得0，第一步會選什麼？','answer':'In。','explanation':'向後歸納先得到既有廠商會容納，再由進入者比較2與0。'},
{'id':'ch07-q04','chapterId':'ch07','question':'動態賽局的完整策略是否需要寫均衡路徑外節點的行動？','answer':'需要。','explanation':'策略是每個可能決策情況的完整應變計畫，即使某節點在均衡中不會到達。'},
{'id':'ch07-q05','chapterId':'ch07','question':'「如果你進入我就打價格戰」若進入後 Fight 的報酬反而低於容納，這個威脅有何問題？','answer':'不可信。','explanation':'真的到達該節點時威脅者不願照做；在有限完美資訊賽局中可由向後歸納／SPNE 排除這種威脅。'},

{'id':'ch08-q01','chapterId':'ch08','question':'每個 SPNE 是否一定也是 Nash equilibrium？','answer':'是。','explanation':'SPNE 要求所有子賽局都是 Nash，因此整個賽局本身當然也是 Nash。'},
{'id':'ch08-q02','chapterId':'ch08','question':'每個 Nash equilibrium 是否一定是 SPNE？','answer':'不是。','explanation':'一般 Nash 可能依賴均衡路徑外的不可信威脅，未必在每個子賽局都構成 Nash。'},
{'id':'ch08-q03','chapterId':'ch08','question':'有效承諾與單純口頭威脅的核心差別是什麼？','answer':'有效承諾會改變未來可行選項或報酬，使後續行動真的符合自身利益。','explanation':'若後續誘因完全沒變，口頭宣布通常無法讓原本不可信的威脅變可信。'},
{'id':'ch08-q04','chapterId':'ch08','question':'某投資成本0.5，可讓既有廠商嚇阻進入後淨得2.5；不投資則進入發生後只得1。是否值得投資？','answer':'值得，若其他條件如題。','explanation':'承諾後已扣除投資成本的淨報酬是2.5，高於不承諾時的1，因此在題目給定續局下投資值得。'},
{'id':'ch08-q05','chapterId':'ch08','question':'從非單點資訊集合中的某一節點單獨切出後繼樹，能否直接算子賽局？','answer':'不能。','explanation':'真正子賽局的起點本身必須是單點資訊集合，並且往後不能切斷任何資訊集合。'},

{'id':'ch09-q01','chapterId':'ch09','question':'Nash bargaining solution 與 Nash equilibrium 是同一概念嗎？','answer':'不是。','explanation':'Nash bargaining solution 是合作式公理化議價解；Nash equilibrium 是非合作策略互動的均衡概念。'},
{'id':'ch09-q02','chapterId':'ch09','question':'雙方交替出價且 δ1=δ2=0.9、玩家1先提案，Rubinstein 模型中玩家1份額約多少？','answer':'約0.5263。','explanation':'在標準無限交替出價、拒絕延遲一期與固定折現因子的模型下，(1-0.9)/(1-0.9×0.9)=0.1/0.19≈0.5263。'},
{'id':'ch09-q03','chapterId':'ch09','question':'若總餅為 NT$100，上題玩家1約拿多少？','answer':'約 NT$52.63。','explanation':'玩家1的均衡份額約0.5263，所以 NT$100×0.5263≈NT$52.63；這是標準交替出價模型的先提案者份額。'},
{'id':'ch09-q04','chapterId':'ch09','question':'對稱 Nash bargaining、分歧點皆0、可行條件 x1+x2=100 時，解是多少？','answer':'NT$50 與 NT$50。','explanation':'最大化 x1x2 且總和固定100，在對稱情況由 x1=x2=50 達到最大。'},
{'id':'ch09-q05','chapterId':'ch09','question':'談判中的 disagreement point 為什麼重要？','answer':'它決定談判破裂時的外部選項，會改變可接受分配與談判力。','explanation':'議價收益通常看相對於分歧點的增益，不可只看總餅大小。'}
]
