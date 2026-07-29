from __future__ import annotations

QUESTIONS_B = [
{'id':'ch10-q01','chapterId':'ch10','question':'囚徒困境重複賽局中，合作每期3、單次偏離5、之後永久懲罰每期1。grim trigger 可支撐合作的折現門檻是多少？','answer':'δ≥0.5。','explanation':'3/(1-δ)≥5+δ/(1-δ)；整理得3≥5-4δ，因此δ≥0.5。'},
{'id':'ch10-q02','chapterId':'ch10','question':'上題若 δ=0.8，永遠合作的現值是多少？','answer':'15。','explanation':'3/(1-0.8)=3/0.2=15。'},
{'id':'ch10-q03','chapterId':'ch10','question':'上題若 δ=0.8，今天偏離一次後永久受懲罰的現值是多少？','answer':'9。','explanation':'5+0.8×1/(1-0.8)=5+4=9，因此合作15優於偏離9。'},
{'id':'ch10-q04','chapterId':'ch10','question':'有限次重複、階段賽局有唯一 Nash、且最後一期沒有未來懲罰時，為什麼常出現向後歸納回一次性 Nash？','answer':'因最後一期先回到階段 Nash，前一期也無法再用最後一期懲罰偏離，如此逐期往前。','explanation':'標準有限重複賽局的終期會切斷未來誘因。'},
{'id':'ch10-q05','chapterId':'ch10','question':'folk theorem 是否表示「任何報酬都可以成為均衡」？','answer':'不是。','explanation':'通常仍要求可行、個別理性、玩家夠有耐心以及相應監督與策略條件。'},

{'id':'ch11-q01','chapterId':'ch11','question':'Bayesian game 中，有私人資訊玩家的純策略通常寫成什麼形式？','answer':'型態到行動的映射。','explanation':'策略必須說明每個可能 type 下要做哪個 action。'},
{'id':'ch11-q02','chapterId':'ch11','question':'給定 Tough→Fight、Weak→Accommodate，且 Tough 機率0.4，進入者遇 Tough 得-1、遇 Weak 得2。In 的期望報酬是多少？','answer':'0.8。','explanation':'0.4(-1)+0.6(2)=-0.4+1.2=0.8；這只是對一組給定 type-contingent strategy 的期望最佳回應計算。'},
{'id':'ch11-q03','chapterId':'ch11','question':'同一給定策略下，若 Tough 機率改為0.8，In 的期望報酬是多少？','answer':'-0.4。','explanation':'0.8(-1)+0.2(2)=-0.8+0.4=-0.4，因此若 Out=0，進入者會選 Out。若 Fight／Accommodate 是後續動態行動，完整均衡仍要另做序列理性分析。'},
{'id':'ch11-q04','chapterId':'ch11','question':'BNE 的最佳回應是否要對每個可能型態分別檢查？','answer':'要。','explanation':'每個 type 在其可用資訊與信念下都必須沒有偏離誘因。'},
{'id':'ch11-q05','chapterId':'ch11','question':'一個故事有私人 type，又有先後行動與非單點資訊集合；只算 BNE 的期望報酬是否一定足夠？','answer':'不一定。','explanation':'BNE 是策略式基準；動態不完全資訊若涉及資訊集合、belief 與續局最適性，通常還要檢查 PBE／sequential rationality。'},

{'id':'ch12-q01','chapterId':'ch12','question':'三位風險中立投標人、價值 i.i.d. Uniform[0,1] 的第一價對稱均衡中，v=0.9 的出價是多少？','answer':'0.6。','explanation':'b(v)=(n-1)v/n=(2/3)×0.9=0.6。'},
{'id':'ch12-q02','chapterId':'ch12','question':'第二價拍賣三人出價 NT$100、NT$80、NT$50，誰得標、支付多少？','answer':'出價 NT$100 者得標，支付 NT$80。','explanation':'最高出價者得標，標準第二價規則支付第二高出價。'},
{'id':'ch12-q03','chapterId':'ch12','question':'第二價拍賣「誠實出價是弱優勢」最典型依賴哪一類價值環境？','answer':'標準私人價值環境。','explanation':'核心是私人價值與第二價門檻付款邏輯；bidder values 彼此獨立並不是 truthful weak dominance 本身的必要條件，i.i.d.／風險中立更多是第一價閉式解與標準 revenue equivalence 常用假設。'},
{'id':'ch12-q04','chapterId':'ch12','question':'共同價值拍賣中，winner\'s curse 指什麼？','answer':'得標可能代表自己的訊號特別樂觀，因此若未條件化「自己是最高者」會高估標的價值。','explanation':'贏本身帶來負面資訊更新，常使理性投標人下修出價。'},
{'id':'ch12-q05','chapterId':'ch12','question':'revenue equivalence 是否不需要任何假設就成立？','answer':'不是。','explanation':'標準結果依賴對稱／同分布、獨立私人價值、風險中立、相同配置規則與邊界條件等。'},

{'id':'ch13-q01','chapterId':'ch13','question':'PBE 至少包含哪兩大類物件？','answer':'完整策略與信念。','explanation':'動態不完美／不完全資訊下，除了 strategy 還要明確寫各資訊集合的 belief。'},
{'id':'ch13-q02','chapterId':'ch13','question':'候選 separating 策略 H→A、L→B，兩種型態都確定照做。on-path 的 μ(H|A) 是多少？','answer':'1。','explanation':'A 在均衡中只由 H 送出，因此 Bayes 更新後接 A 時確信為 H。'},
{'id':'ch13-q03','chapterId':'ch13','question':'先驗 Pr(H)=0.6、Pr(L)=0.4；H 一定傳 A，L 以0.25機率傳 A。觀察 A 後 μ(H|A) 是多少？','answer':'6/7，約0.8571。','explanation':'0.6/(0.6+0.4×0.25)=0.6/0.7=6/7。'},
{'id':'ch13-q04','chapterId':'ch13','question':'PBE 的 sequential rationality 是在哪些資訊集合檢查？','answer':'每個資訊集合。','explanation':'即使某資訊集合在均衡路徑外，完整策略仍需在給定信念下是續局最佳回應。'},
{'id':'ch13-q05','chapterId':'ch13','question':'正機率到達的 on-path 資訊集合，其 belief 可以任意指定嗎？','answer':'不可以。','explanation':'只要 Bayes rule 可用，就必須依先驗與均衡策略更新；off-path belief 雖未必唯一，行動仍須對所指定信念序列理性。'},

{'id':'ch14-q01','chapterId':'ch14','question':'signaling game 中通常是哪一方先知道自己的 type？','answer':'Sender。','explanation':'Sender 先知道私人型態並選可觀察訊號，Receiver 再更新信念並行動。'},
{'id':'ch14-q02','chapterId':'ch14','question':'教育訊號例題中 H 的生產力10、教育成本 e；若 H 選 e=2.1 並拿工資10，淨報酬是多少？','answer':'7.9。','explanation':'高型態收到工資10並負擔教育成本2.1，所以淨報酬是10-2.1=7.9；這通過 H 不模仿 L 的一個 IC 檢查，但不是完整 PBE 的全部條件。'},
{'id':'ch14-q03','chapterId':'ch14','question':'同例 L 的教育成本為3e。若 L 模仿 e=2.1 並拿工資10，淨報酬是多少？','answer':'3.7。','explanation':'10-3×2.1=10-6.3=3.7，低於 L 不教育時的4，因此 L 不願模仿 H。'},
{'id':'ch14-q04','chapterId':'ch14','question':'若只看兩型態互相模仿的 IC，上例哪些教育程度 e 可支撐 L 選0、H 選e 的分離候選？','answer':'2≤e≤6。','explanation':'H 不模仿 L 要 10-e≥4，所以 e≤6；L 不模仿 H 要 4≥10-3e，所以 e≥2。連續訊號空間下仍要另外處理其他 off-path e 才能完成 PBE。'},
{'id':'ch14-q05','chapterId':'ch14','question':'pooling PBE 是否一定通過所有更強的 equilibrium refinement？','answer':'不一定。','explanation':'某些 pooling 均衡依賴不合理 off-path beliefs，可能被 intuitive criterion 等精煉排除。'},

{'id':'ch15-q01','chapterId':'ch15','question':'screening 與 signaling 最簡單的先動者差別是什麼？','answer':'screening 常由資訊較少的一方先設計選單；signaling 則由有私人資訊的一方先送訊號。','explanation':'兩者都處理資訊不對稱，但制度方向相反。'},
{'id':'ch15-q02','chapterId':'ch15','question':'篩選例題原菜單中 H 對高方案 (q=1,p=80) 的效用是多少？','answer':'20。','explanation':'H 的完整品質價值100，所以100-80=20。'},
{'id':'ch15-q03','chapterId':'ch15','question':'同一原菜單中 H 對低方案 (q=0.5,p=25) 的效用是多少？因此原菜單是否 IC？','answer':'25；不是 IC。','explanation':'100×0.5-25=25>20，所以 H 會冒充選低方案。'},
{'id':'ch15-q04','chapterId':'ch15','question':'把高方案價格降到70後，H 的高方案效用與 L 的高方案效用各是多少？','answer':'H=30，L=-20。','explanation':'H:100-70=30；L:50-70=-20，因此 H 偏好高方案而 L 不會模仿。'},
{'id':'ch15-q05','chapterId':'ch15','question':'cheap talk 因為傳訊沒有直接成本，是否必然完全無資訊？','answer':'不必然。','explanation':'若 Sender 與 Receiver 利益足夠一致，truthful communication 仍可能構成均衡；利益嚴重衝突時才更可能被忽略。'},

{'id':'ch16-q01','chapterId':'ch16','question':'revelation principle 的主要用途是什麼？','answer':'把可實現結果的分析簡化為 truthful direct mechanism。','explanation':'它是分析工具，不代表任何社會目標都必然可實現。'},
{'id':'ch16-q02','chapterId':'ch16','question':'單一物品 VCG 中三人價值 NT$100、NT$80、NT$50，效率配置給誰？','answer':'給價值 NT$100 的玩家。','explanation':'效率配置最大化總價值，因此把物品給最高價值者。'},
{'id':'ch16-q03','chapterId':'ch16','question':'上題採「支付給機制為正」的 Clarke pivot／第二價 convention 時，得標者支付多少？','answer':'NT$80。','explanation':'沒有得標者時其他人可得到的最大福利是80；有他並由他取得物品時其他人福利0，因此其外部性支付80。若教材把 transfer to player 記為正，公式符號會相反。'},
{'id':'ch16-q04','chapterId':'ch16','question':'上題得標者效用是多少？','answer':'NT$20。','explanation':'準線性效用等於自己的物品價值減支付，因此得標者效用是 NT$100-NT$80=NT$20。'},
{'id':'ch16-q05','chapterId':'ch16','question':'機制設計中 efficiency、IC、IR 與 budget balance 是否應分開檢查？','answer':'是。','explanation':'這些是不同性質；一個機制可能有效率且 truthful，卻不一定滿足其他要求。'},

{'id':'ch17-q01','chapterId':'ch17','question':'合作賽局的 characteristic function v(S) 表示什麼？','answer':'聯盟 S 能自行創造或保證的總價值。','explanation':'合作賽局把不同 coalition 的可達價值作為基本資料。'},
{'id':'ch17-q02','chapterId':'ch17','question':'三人例題中 v(N)=90。有效率分配 x1,x2,x3 必須滿足什麼？','answer':'x1+x2+x3=90。','explanation':'效率要求 grand coalition 的總價值被完全分配。'},
{'id':'ch17-q03','chapterId':'ch17','question':'若任何兩人聯盟價值60，core 還要求每一對的分配和至少多少？','answer':'至少60。','explanation':'否則該兩人 coalition 可脫離並自行取得60，阻擋原分配。'},
{'id':'ch17-q04','chapterId':'ch17','question':'三人完全對稱、任兩人價值60、三人價值90的例題中，唯一 core 分配是多少？','answer':'(30,30,30)。','explanation':'效率總和90且三個 pair 都至少60；相加 pair 條件使三者只能各30。'},
{'id':'ch17-q05','chapterId':'ch17','question':'Shapley value 是否永遠落在 core？','answer':'不一定。','explanation':'Shapley 強調平均邊際貢獻與公理性；core 強調 coalition blocking，兩者一般不必重合。'},

{'id':'ch18-q01','chapterId':'ch18','question':'兩位駕駛例題中，(A,B) 是否是 Nash equilibrium？','answer':'是。','explanation':'A 上駕駛改去B會從2變4；B 上駕駛改去A會從3變5，兩人都不願單方面改。'},
{'id':'ch18-q02','chapterId':'ch18','question':'同例 (B,A) 是否也是 Nash equilibrium？','answer':'是。','explanation':'問題對兩位駕駛對稱，交換玩家後同樣沒有單方面偏離誘因。'},
{'id':'ch18-q03','chapterId':'ch18','question':'同例兩個純策略 Nash 的總旅行時間是多少？','answer':'5。','explanation':'一人走A花2、一人走B花3，總成本2+3=5。'},
{'id':'ch18-q04','chapterId':'ch18','question':'政策若收擁擠費，從賽局模型角度主要改變哪個元素？','answer':'payoff／成本結構。','explanation':'通行費會改變各路線在不同擁擠狀態下的私人報酬，因此最佳回應與均衡可能改變。'},
{'id':'ch18-q05','chapterId':'ch18','question':'strategic complements／substitutes 的「別人提高、我也提高／降低」語言，是否適合所有沒有自然次序的離散策略賽局？','answer':'不一定。','explanation':'這種單調比較通常要策略集合本身具有可排序結構；一般任意標籤的離散策略不能硬用「提高／降低」來定義。'},

{'id':'ch19-q01','chapterId':'ch19','question':'靜態、完整資訊的標準賽局，通常先用哪個核心解概念？','answer':'Nash equilibrium。','explanation':'沒有動態續局或私人 type 時，NE 是標準起點。'},
{'id':'ch19-q02','chapterId':'ch19','question':'動態賽局有真正子賽局時，哪個解概念能進一步要求每個子賽局都為 Nash？','answer':'SPNE。','explanation':'SPNE 要求每個 proper subgame 都構成 Nash equilibrium；在有限完美資訊賽局中常可用向後歸納求得。'},
{'id':'ch19-q03','chapterId':'ch19','question':'靜態不完全資訊、玩家有私人 type 時，通常先用哪個核心解概念？','answer':'BNE。','explanation':'Bayesian Nash 直接處理 type-dependent strategies 與條件期望最佳回應。'},
{'id':'ch19-q04','chapterId':'ch19','question':'Nature 決定 type、Sender 發訊號、Receiver 觀察訊號後行動，通常需要哪個解概念？','answer':'PBE。','explanation':'這是動態不完全資訊賽局，需要同時處理策略、belief、Bayes 更新與序列理性。'},
{'id':'ch19-q05','chapterId':'ch19','question':'complete information 與 perfect information 是否同義，或只是同一概念的強弱兩級？','answer':'不是。','explanation':'complete information 描述 payoff／type 是否共同已知；perfect information 描述每次決策時能否辨認此前實際歷史。兩者是不同資訊維度，不能只寫成單純強弱階層。'}
]
