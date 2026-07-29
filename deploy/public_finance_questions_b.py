from __future__ import annotations

QUESTIONS_B = [
    {'id':'ch10-q01','chapterId':'ch10','question':'教育具有正外部性時，私人邊際效益 MPB 與社會邊際效益 MSB 的關係通常如何？','answer':'MSB 大於 MPB。','explanation':'MSB=MPB+MEB；正外部效益 MEB>0，使市場自費教育量可能低於社會有效率量。'},
    {'id':'ch10-q02','chapterId':'ch10','question':'某訓練現在總機會成本 NT$100,000，一年後增加所得 NT$60,000、兩年後再增加 NT$60,000，折現率 10%。私人淨現值約多少？','answer':'約 NT$4,132。','explanation':'60,000/1.1+60,000/1.1²≈104,132；減去 100,000 後約 NT$4,132。'},
    {'id':'ch10-q03','chapterId':'ch10','question':'政府把學費補助到零，是否代表教育的社會機會成本也變成零？','answer':'不是。','explanation':'補助改變誰支付，不會讓教師時間、校舍、教材與學生放棄工作的機會成本消失。'},
    {'id':'ch10-q04','chapterId':'ch10','question':'家庭因無法用未來所得借款支付現在學費而放棄高報酬教育，這是哪一種常見政策介入理由？','answer':'借貸限制。','explanation':'即使教育私人淨現值為正，信用市場不完整仍可能阻止投資。'},
    {'id':'ch10-q05','chapterId':'ch10','question':'教育補助主要發給原本就會就學的人，是否能只用補助總額判斷新增教育效果？','answer':'不能。','explanation':'補助的一部分可能只是移轉；政策效果應看真正改變的就學、學習成果與外部效益。'},

    {'id':'ch11-q01','chapterId':'ch11','question':'所得 NT$800,000、總稅額 NT$80,000，平均稅率 ATR 是多少？','answer':'10%。','explanation':'ATR=T/Y=80,000/800,000=10%。'},
    {'id':'ch11-q02','chapterId':'ch11','question':'某人平均稅率 10%，最後新增一元所得落在 20% 稅率級距。影響新增所得誘因較直接的是哪個稅率？','answer':'20% 的邊際稅率。','explanation':'行為決策通常看最後新增一元稅基能保留多少，因此 MTR 比 ATR 更直接。'},
    {'id':'ch11-q03','chapterId':'ch11','question':'扣除額 NT$10,000 與可全額使用的稅額抵免 NT$10,000，是否一定減少相同稅額？','answer':'不一定。','explanation':'扣除額先減稅基，節稅額取決於邊際稅率；抵免額則直接減少稅額。'},
    {'id':'ch11-q04','chapterId':'ch11','question':'「相同納稅能力者應受到相似稅務待遇」比較接近水平公平還是垂直公平？','answer':'水平公平。','explanation':'水平公平強調相似能力者相似對待；垂直公平處理不同能力者的差異負擔。'},
    {'id':'ch11-q05','chapterId':'ch11','question':'稅制中的免稅、扣除、抵免或優惠稅率若用來給特定活動財政利益，常統稱為什麼？','answer':'稅式支出。','explanation':'稅式支出透過稅制而非直接預算支出提供利益，也有收入與分配效果。'},

    {'id':'ch12-q01','chapterId':'ch12','question':'需求彈性絕對值 |Ed|=0.5、供給彈性 Es=1.5。簡化競爭模型下，買方約承擔單位稅的多少比例？','answer':'75%。','explanation':'買方比例=Es/(Es+|Ed|)=1.5/(1.5+0.5)=75%。'},
    {'id':'ch12-q02','chapterId':'ch12','question':'延續上一題，單位稅為 NT$40 時，買方支付價相對未稅均衡約上升多少？','answer':'約 NT$30。','explanation':'買方承擔 75%×40=NT$30。'},
    {'id':'ch12-q03','chapterId':'ch12','question':'延續上一題，賣方實收價相對未稅均衡約下降多少？','answer':'約 NT$10。','explanation':'賣方承擔剩餘 25%×40=NT$10。'},
    {'id':'ch12-q04','chapterId':'ch12','question':'需求完全無彈性而供給有彈性時，簡化部分均衡模型下哪一方承擔主要稅負？','answer':'需求方／買方。','explanation':'較缺乏彈性的一方較難透過改變交易量逃離稅基，因此承擔較多。'},
    {'id':'ch12-q05','chapterId':'ch12','question':'只把法定申報義務從賣方改成買方，在同一競爭市場、同一稅楔下，是否必然大幅改變經濟歸宿？','answer':'不必然。','explanation':'經濟歸宿由市場價格調整與相對彈性決定，法定歸宿與經濟歸宿要分開。'},

    {'id':'ch13-q01','chapterId':'ch13','question':'單位稅 NT$10 使交易量減少 500 單位。線性近似的 DWL 是多少？','answer':'NT$2,500。','explanation':'DWL≈1/2×10×500=NT$2,500。'},
    {'id':'ch13-q02','chapterId':'ch13','question':'單位稅 NT$20 使交易量由 10,000 降到 9,000。線性近似 DWL 是多少？','answer':'NT$10,000。','explanation':'DWL≈1/2×20×1,000=NT$10,000。'},
    {'id':'ch13-q03','chapterId':'ch13','question':'延續上一題，若課稅後每單位都收 NT$20，政府稅收是多少？','answer':'NT$180,000。','explanation':'Revenue=20×9,000=NT$180,000；稅收是移轉，不等於 NT$10,000 的 DWL。'},
    {'id':'ch13-q04','chapterId':'ch13','question':'需求幾乎完全無彈性、課稅後數量幾乎不變時，傳統供需三角形 DWL 通常大還是小？','answer':'較小。','explanation':'行為數量反應小，消失的互利交易少；但分配稅負仍可能很重。'},
    {'id':'ch13-q05','chapterId':'ch13','question':'「稅收有 NT$1 億，所以社會無謂損失就是 NT$1 億」這句話對嗎？','answer':'不對。','explanation':'稅收多半是私人向政府的移轉；DWL 是額外因行為扭曲消失的總剩餘。'},

    {'id':'ch14-q01','chapterId':'ch14','question':'在極度簡化的 Ramsey 條件下，A、B 商品補償需求彈性絕對值分別為 0.5 與 1.0。A 的相對稅楔約是 B 的幾倍？','answer':'約 2 倍。','explanation':'逆彈性直覺下稅楔與 1/|εc| 成比例：1/0.5 相對 1/1.0 為 2 倍。'},
    {'id':'ch14-q02','chapterId':'ch14','question':'純 Ramsey 效率直覺偏向對需求較有彈性還是較無彈性的稅基課較高稅？','answer':'較無彈性的稅基。','explanation':'在限制條件下，較無彈性的稅基同樣收入造成的數量扭曲較小。'},
    {'id':'ch14-q03','chapterId':'ch14','question':'可以只憑逆彈性法則就推出「低所得者常買的必需品應課最高稅」嗎？','answer':'不可以。','explanation':'現實最適課稅還要加入分配權重、交叉需求與其他政策工具；純效率規則不是完整政策結論。'},
    {'id':'ch14-q04','chapterId':'ch14','question':'一次總額稅為何在理論基準中常被視為扭曲較小？','answer':'因為稅額不隨個人可改變的邊際行為或稅基變動。','explanation':'若行為無法降低稅額，就不會在邊際上改變相對價格；但公平與可行性可能很差。'},
    {'id':'ch14-q05','chapterId':'ch14','question':'最適課稅只需要最小化超額負擔，不需要考慮政府收入需求或公平，對嗎？','answer':'不對。','explanation':'最適課稅是在收入需求下權衡效率與分配；不同社會福利權重會改變最適結論。'},

    {'id':'ch15-q01','chapterId':'ch15','question':'某人多賺 NT$10,000，多繳稅 NT$2,000、福利又減少 NT$3,000。有效邊際稅率 EMTR 是多少？','answer':'50%。','explanation':'可支配所得只增加 10,000-2,000-3,000=5,000；EMTR=1-5,000/10,000=50%。'},
    {'id':'ch15-q02','chapterId':'ch15','question':'某人多賺 NT$1,000，多繳稅 NT$200、福利減少 NT$300。EMTR 是多少？','answer':'50%。','explanation':'可支配所得增加 500；EMTR=1-500/1,000=50%。'},
    {'id':'ch15-q03','chapterId':'ch15','question':'處於 30% 邊際稅率的人獲得 NT$10,000 所得扣除，若可全額利用，簡化節稅多少？','answer':'NT$3,000。','explanation':'扣除額減少稅基，節稅≈10,000×30%=NT$3,000。'},
    {'id':'ch15-q04','chapterId':'ch15','question':'同一人若改拿可全額使用的 NT$10,000 稅額抵免，簡化減稅多少？','answer':'NT$10,000。','explanation':'抵免直接減少稅額，不是只減少稅基。'},
    {'id':'ch15-q05','chapterId':'ch15','question':'所得稅率提高後，勞動供給是否必然下降？','answer':'不必然。','explanation':'替代效果傾向降低工作，但所得效果可能朝相反方向；參與與工時反應也不同。'},

    {'id':'ch16-q01','chapterId':'ch16','question':'可扣除利息 NT$50,000、公司稅率 20%，且題目明示可全額扣除。簡化利息稅盾是多少？','answer':'NT$10,000。','explanation':'Tax shield=50,000×20%=NT$10,000。'},
    {'id':'ch16-q02','chapterId':'ch16','question':'可扣除利息 NT$100,000、公司稅率 20% 時，簡化利息稅盾是多少？','answer':'NT$20,000。','explanation':'100,000×20%=NT$20,000。'},
    {'id':'ch16-q03','chapterId':'ch16','question':'公司是法定納稅人，能否直接推論公司所得稅的經濟負擔百分之百落在股東？','answer':'不能。','explanation':'長期價格、工資與資本移動會讓稅負可能分散到股東、勞工或消費者。'},
    {'id':'ch16-q04','chapterId':'ch16','question':'兩種折舊制度允許的名目扣除總額相同，但 A 制度更早扣除。其他條件相同時，哪一種扣除現值通常較高？','answer':'A 制度。','explanation':'較早取得扣除的折現損失較小，因此稅收利益現值通常較高。'},
    {'id':'ch16-q05','chapterId':'ch16','question':'分析公司稅長期歸宿時，為什麼資本可否跨區移動很重要？','answer':'因為較能移動的資本較可能避開高稅地區，稅負會透過工資、價格或較不流動稅基重新分配。','explanation':'經濟歸宿取決於行為反應與相對彈性，而不只是法定繳納者。'},

    {'id':'ch17-q01','chapterId':'ch17','question':'銷項稅額 NT$40,000、可扣抵進項稅額 NT$25,000，簡化應納 VAT 是多少？','answer':'NT$15,000。','explanation':'VAT payable=40,000-25,000=NT$15,000。'},
    {'id':'ch17-q02','chapterId':'ch17','question':'某企業銷項稅額 NT$50,000、可扣抵進項稅額 NT$30,000，簡化應納 VAT 是多少？','answer':'NT$20,000。','explanation':'50,000-30,000=NT$20,000。'},
    {'id':'ch17-q03','chapterId':'ch17','question':'VAT 在多個交易階段徵收，是否必然代表同一價值被完整重複課稅很多次？','answer':'不必然。','explanation':'加值型制度以進項扣抵把每一階段稅負集中到增加價值，避免一般流轉稅式的層層重複。'},
    {'id':'ch17-q04','chapterId':'ch17','question':'其他條件相同時，預期未來某不動產淨稅負永久提高，資產價格可能如何反應？','answer':'可能下降，將未來稅負資本化。','explanation':'買方會把未來淨稅負折現進目前願付價格；實際幅度仍取決於供需與公共服務。'},
    {'id':'ch17-q05','chapterId':'ch17','question':'土地供給近似固定的稅負結論，可以不加條件直接套到可新增建物與可移動資本嗎？','answer':'不可以。','explanation':'建物與資本供給較有彈性，會改變投資與區位選擇，因此歸宿與效率效果不同。'},

    {'id':'ch18-q01','chapterId':'ch18','question':'上級政府提供 25% 配合款。地方每新增 NT$100 合格支出，自付多少？','answer':'NT$75。','explanation':'地方自付=(1-0.25)×100=NT$75。'},
    {'id':'ch18-q02','chapterId':'ch18','question':'上級政府提供 40% 配合款。地方每新增 NT$100 合格支出，自付多少？','answer':'NT$60。','explanation':'(1-0.40)×100=NT$60。'},
    {'id':'ch18-q03','chapterId':'ch18','question':'一般不指定用途補助與配合補助相比，哪一種會直接降低特定合格支出的相對價格？','answer':'配合補助。','explanation':'配合補助使地方每增加一元特定支出只需負擔其中一部分，產生價格效果。'},
    {'id':'ch18-q04','chapterId':'ch18','question':'Tiebout 模型要順利運作，居民移動成本高還是低較有利？','answer':'低。','explanation':'用腳投票需要居民能在不同地方稅費與公共服務組合間移動；高移動成本會削弱機制。'},
    {'id':'ch18-q05','chapterId':'ch18','question':'某污染效益與損害跨越多個地方行政區，完全由單一地方決策是否容易忽略外部性？','answer':'是。','explanation':'跨區效益或成本會超出地方決策者面對的範圍，構成較高層級協調的理由。'},

    {'id':'ch19-q01','chapterId':'ch19','question':'債務比 b=50%、實質利率 r=3%、實質成長率 g=1%、初級盈餘 ps=0。用 Δb≈(r-g)b-ps，債務比約增加多少？','answer':'約 1 個 GDP 百分點。','explanation':'(0.03-0.01)×0.50=0.01，即債務/GDP 約增加 0.01=1 個百分點。'},
    {'id':'ch19-q02','chapterId':'ch19','question':'債務比 b=60%、r=4%、g=2%、ps=0。債務比約增加多少？','answer':'約 1.2 個 GDP 百分點。','explanation':'(0.04-0.02)×0.60=0.012，即 1.2 個百分點。'},
    {'id':'ch19-q03','chapterId':'ch19','question':'延續上一題，要讓債務比大致穩定，簡化下需要多少初級盈餘比？','answer':'約 1.2% GDP。','explanation':'穩定條件 ps*≈(r-g)b=0.012，因此需約 1.2% GDP 的初級盈餘。'},
    {'id':'ch19-q04','chapterId':'ch19','question':'年度赤字是流量還是存量？政府債務是流量還是存量？','answer':'赤字是流量；債務是存量。','explanation':'赤字描述一段期間的收支差，債務描述某一時點累積未償負債。'},
    {'id':'ch19-q05','chapterId':'ch19','question':'當 r<g 時，可以推出政府跨期預算限制永久消失、任何赤字都沒有成本嗎？','answer':'不可以。','explanation':'r<g 使既有債務比動態較有利，但財政永續仍取決於未來初級收支、風險與融資條件。'},
]
