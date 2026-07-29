from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

VERSION = '2026.07.29-2'


def _chapter(chapters, chapter_id):
    return next(ch for ch in chapters if ch['id'] == chapter_id)


def _question(questions, question_id):
    return next(q for q in questions if q['id'] == question_id)


def build_v2(chapters, questions):
    chapters = deepcopy(chapters)
    questions = deepcopy(questions)

    # ch03 Public goods: the scope promised Lindahl pricing but v1 never taught it.
    ch = _chapter(chapters, 'ch03')
    ch['intuition'].append(
        'Lindahl 均衡用「個人化價格／個人化稅負份額」表示每個人對同一公共財數量的邊際願付價格。理想均衡中，每個人面對自己的 Lindahl 價格後都選擇同一個公共財數量，而且個人化價格加總等於供給公共財的邊際成本。它是理解 Samuelson 條件的理論機制，不代表現實中偏好能被無成本、誠實地揭露。'
    )
    ch['definitions'].append(
        ('Lindahl 價格（Lindahl Price）', '對同一公共財給不同個人設定的個人化邊際價格／稅負份額；理想均衡時，各人的個人化價格加總等於公共財的邊際成本，且各人選擇相同的公共財數量。')
    )
    ch['traps'].append('Lindahl 價格不是所有人面對同一價格；它依賴個人化負擔與偏好揭露，因此是理論基準而非自動可執行的現實收費制度。')
    ch['exam'].append('問 Lindahl 時，抓住「個人化價格＋共同 Q＋個人價格加總等於 MC」三件事。')
    q = _question(questions, 'ch03-q04')
    q['question'] = 'Lindahl 公共財均衡中，不同居民通常面對相同價格，還是個人化價格？這些價格和公共財邊際成本有何關係？'
    q['answer'] = '通常面對個人化價格；在理想均衡中，個人化價格加總等於公共財的邊際成本。'
    q['explanation'] = 'Lindahl 機制讓每個人對同一公共財數量面對不同的個人化價格；各人都選擇同一 Q，而個人化價格加總與 Samuelson 條件一致地對應到 MC。'

    # ch05 Rent seeking: v1 showed a conceptual decomposition as if it were an accounting identity.
    ch = _chapter(chapters, 'ch05')
    ch['formulas'][1] = (
        r'\text{尋租淨耗損}\;\text{需計入真實尋租資源與伴隨扭曲}',
        '這是概念提醒，不是一般會計恆等式。政策租金本身可能只是移轉；遊說、排隊、規避與其他為爭取租金耗掉的真實資源，以及政策本身造成的額外扭曲，才屬需要計入的社會成本。',
    )

    # ch06 Cost-benefit analysis: distinguish the social discount rate from a mechanically chosen market rate.
    ch = _chapter(chapters, 'ch06')
    ch['intuition'].append(
        '公共計畫使用的是「社會折現」概念：折現率應與分析口徑、跨期機會成本與政策規範一致，不能看到政府借款利率就機械地當成唯一正確折現率。風險也不一定只靠把折現率往上加處理；可用情境、風險調整後現金流或敏感度分析另行檢查。'
    )
    ch['definitions'].append(
        ('社會折現率（Social Discount Rate）', '公共成本效益分析中用來比較不同時間點社會成本與效益的折現率；其選擇需與實質／名目口徑、機會成本與跨期福利準則一致。')
    )
    ch['traps'].append('公共計畫的折現率不是看到一個市場利率就直接套用；必須先確認分析口徑與政策評估規範。')

    # ch07 Distribution: clarify Gini bounds and add transfer instruments promised by the scope.
    ch = _chapter(chapters, 'ch07')
    for i, (term, desc) in enumerate(ch['definitions']):
        if term == 'Gini coefficient':
            ch['definitions'][i] = (
                term,
                '衡量 Lorenz curve 偏離完全平等線的程度；在常見的非負所得與標準化設定下介於 0 與 1，遇到負所得等特殊資料時其界限與解讀需另行處理。',
            )
    ch['definitions'].extend([
        ('現金移轉（Cash Transfer）', '直接增加受領者可支配資源，通常給受領者較大的消費選擇空間。'),
        ('實物移轉（In-kind Transfer）', '以特定商品或服務提供利益，例如食物、住宅或醫療；可能用來鎖定政策目的，但也限制受領者選擇。'),
        ('負所得稅（Negative Income Tax）', '低所得時給予淨移轉，並隨市場所得上升逐步減少；退場率會形成有效邊際稅率。'),
    ])

    # ch08 Social insurance: funded is a financing dimension, not synonymous with an individual account.
    ch = _chapter(chapters, 'ch08')
    ch['intuition'].append(
        '失業保險的核心取捨也是保險與誘因：給付可在失業期間平滑消費、減輕流動性壓力，但較高或較久的給付也可能降低部分人的求職強度。這不代表所有較長失業期間都是「浪費」；福利分析要同時估計消費平滑利益、求職反應與再就業品質。'
    )
    for i, (term, desc) in enumerate(ch['definitions']):
        if term == '完全提存（Fully Funded）':
            ch['definitions'][i] = (
                term,
                '事先累積金融或其他資產，讓未來退休給付由所累積資產及其報酬支應。這描述的是融資方式，不必然等於個人帳戶；確定給付（DB）或確定提撥（DC）安排都可能採提存方式。',
            )
    ch['definitions'].append(
        ('失業保險（Unemployment Insurance）', '在符合資格的失業期間提供所得替代，用於消費平滑與風險分擔；給付水準、期間與求職條件同時影響保障與求職誘因。')
    )
    ch['traps'][1] = 'PAYG 與 funded 是融資方式；DB／DC 是給付或提撥規則。兩組分類不能互相畫等號，funded 也不必然代表個人帳戶。'
    q = _question(questions, 'ch08-q05')
    q['answer'] = '完全提存制事先累積資產供未來給付；PAYG 主要用當期收入支付當期受益者。'
    q['explanation'] = '這是在比較融資方式。funded 不必然是個人帳戶，也不等於 DC；DB 制度同樣可能有資產提存。'

    # ch09 Health: copayment and coinsurance are different cost-sharing instruments.
    ch = _chapter(chapters, 'ch09')
    ch['problem'] = '醫療市場為什麼同時有保險、資訊與供給者誘因問題？成本分擔與公共保險如何在風險保障和過度使用間取捨？'
    ch['intuition'][1] = '定額自付（copayment）、按比例共同保險（coinsurance）與自負額（deductible）都會讓病患負擔部分費用，但機制不同：copayment 是每次或每項服務固定金額；coinsurance 是合格費用的一定比例；deductible 則是保險開始分攤前由被保險人先負擔的門檻。提高成本分擔通常會降低使用量，但也可能一起壓低高價值照護。供給者端若按服務量付費，可能鼓勵數量；總額、論人或論病例支付則把更多成本風險移給提供者，也可能帶來減少服務或選擇病人的新誘因。'
    new_defs = []
    for term, desc in ch['definitions']:
        if term == '共付（Copayment / Coinsurance）':
            new_defs.extend([
                ('定額自付（Copayment）', '對一次就醫或一項服務支付固定金額；不是按服務價格百分比計算。'),
                ('共同保險（Coinsurance）', '由被保險人負擔合格醫療費用的一定比例，例如 20%；比例 c 可用於 P_patient=cP 的簡化分析。'),
                ('自負額（Deductible）', '在保險開始依契約分攤部分費用之前，由被保險人先自行負擔的累積門檻。'),
            ])
        else:
            new_defs.append((term, desc))
    ch['definitions'] = new_defs
    ch['formulas'][0] = (
        r'P_{patient}=c\cdot P',
        '若採共同保險（coinsurance）且被保險人負擔比例為 c，合格醫療服務價格 P 中由病患在邊際上直接負擔 cP；這個公式不適用於固定金額的 copayment。',
    )
    ch['traps'][2] = '降低成本分擔通常增加保障，也可能增加價格誘發的使用；但 copayment、coinsurance 與 deductible 的邊際價格機制不同，不能混成同一名詞。'
    q = _question(questions, 'ch09-q05')
    q['question'] = '降低病患的 coinsurance 自付比例後醫療使用增加，能否直接說所有新增使用都是無效率浪費？'
    q['answer'] = '不能。'
    q['explanation'] = '新增使用可能同時包含原本因價格而放棄的高價值治療與低價值使用；要比較健康效益與完整社會成本。'

    # ch10 Education: add the signaling channel promised by the scope.
    ch = _chapter(chapters, 'ch10')
    ch['intuition'].append(
        '教育帶來的薪資報酬也可能同時包含「人力資本」與「訊號／篩選」兩種機制。若教育真的提高技能與生產力，私人薪資報酬較接近新增產出；若部分報酬來自學歷向雇主傳遞原本就存在的能力資訊，私人薪資溢酬就不必然等於同額的社會生產力增量。實務上兩種機制可以同時存在。'
    )
    ch['definitions'].append(
        ('教育訊號／篩選（Signaling / Screening）', '教育或學歷可能向雇主傳遞能力、持續性等原本難以觀察的資訊；因此薪資報酬不必全部來自教育本身創造的人力資本。')
    )
    ch['traps'].append('觀察到大學畢業者薪資較高，不能直接把全部薪資差都解讀成教育造成的生產力增量；選擇與訊號效果也可能存在。')
    q = _question(questions, 'ch10-q05')
    q['question'] = '觀察到受教育者薪資較高，能否直接把全部薪資差都當成教育提高生產力的因果效果？'
    q['answer'] = '不能。'
    q['explanation'] = '薪資差可能同時包含人力資本、原有能力差異、選擇與教育訊號／篩選效果；財政學分析社會報酬時不能把觀察到的全部薪資溢酬直接當成生產力增量。'

    # ch11 Tax principles: define progressive/proportional/regressive explicitly.
    ch = _chapter(chapters, 'ch11')
    ch['definitions'].append(
        ('比例／累進／累退稅負', '若平均稅率隨稅基大致不變，稱比例；隨稅基上升而上升，稱累進；隨稅基上升而下降，稱累退。實際經濟負擔仍要結合稅基、歸宿與有效稅率判斷。')
    )

    # ch12 Tax incidence: make the elasticity share explicitly local/small-tax and competitive.
    ch = _chapter(chapters, 'ch12')
    ch['formulas'][1] = (
        r'\text{買方負擔比例}\approx\frac{E_s}{E_s+|E_d|}',
        '標準競爭市場、小幅從量稅的局部近似。Es 與 |Ed| 應在相關均衡附近評估；有限大稅負若彈性沿曲線改變，不能把單一點彈性公式當成全域精確答案。賣方局部負擔比例約為 |Ed|/(Es+|Ed|)。',
    )
    ch['example'][0] = '若需求彈性絕對值 |Ed|=0.5、供給彈性 Es=1.5，並把它們當作課稅前均衡附近的局部彈性，則買方約承擔 1.5/(1.5+0.5)=75% 的小幅單位稅，賣方約承擔 25%。若題目再用這個局部比例近似 NT$40 的稅楔，買方價格約上升 NT$30、賣方實收價約下降 NT$10；若 NT$40 並非小變動，精確結果仍應回到完整供需曲線求新均衡。'
    ch['exam'][2] = '若題目給彈性數字，要先確認是在做小稅／局部近似；若稅楔很大或彈性會變，應回到完整供需函數求新均衡。'
    for qid in ('ch12-q01', 'ch12-q02', 'ch12-q03'):
        q = _question(questions, qid)
        q['explanation'] += ' 這是標準競爭市場下的局部／小稅近似；有限大稅楔的精確分攤要看完整供需曲線。'

    # ch13 Excess burden: tax revenue is a transfer in the basic welfare diagram, not DWL itself.
    ch = _chapter(chapters, 'ch13')
    ch['problem'] = '納稅人繳出 NT$100、政府收到 NT$100 時，這 NT$100 本身是否就是無謂損失？為什麼扭曲性租稅還會另外產生超額負擔？'
    ch['definitions'][0] = (
        '超額負擔（Excess Burden）',
        '在基本福利分析中，扭曲性課稅相對於取得相同公共收入的無扭曲基準所多造成的福利損失；直覺上是扣除純移轉性稅收後，由行為扭曲留下的額外損失。',
    )
    ch['definitions'][1] = (
        '無謂損失（Deadweight Loss, DWL）',
        '因稅楔使互利交易或其他有效率行為消失而造成、沒有以他人收益完整對應的總剩餘損失；在最基本單一市場模型中常用三角形表示。',
    )
    ch['formulas'][0] = (
        r'DWL\approx\frac12\,t\,|\Delta Q|',
        '在課稅前市場本來有效率、沒有其他楔，且可用線性供需或局部三角形近似時成立。t 是單位稅楔，|ΔQ| 是課稅造成的交易量減少；有既有扭曲、非線性或多市場互動時不能直接套。',
    )
    ch['traps'][0] = '政府稅收在基本福利圖中主要是私人部門到政府的移轉，不是 DWL 本身；行政成本、遵從成本與資金用途若要計入，應另外列示。'
    q = _question(questions, 'ch13-q05')
    q['question'] = '在標準單一市場福利圖中，「政府取得 NT$1 億稅收，所以 DWL 就是 NT$1 億」這句話對嗎？'
    q['answer'] = '不對。'
    q['explanation'] = '稅收本身主要是私人部門向政府的移轉；DWL 是稅楔造成的額外總剩餘損失。若另有行政、遵從或既有扭曲成本，應分項處理。'

    # ch14 Optimal taxation: name the tax-inclusive wedge and state the restrictive assumptions.
    ch = _chapter(chapters, 'ch14')
    ch['definitions'][2] = (
        '逆彈性法則',
        '在需求彼此獨立、忽略分配差異等高度簡化的 Ramsey 商品稅設定下，補償需求較缺乏彈性的商品可承受較高的最適稅含價格楔；一般 Ramsey 問題有交叉價格效果時不只看自己的彈性。',
    )
    ch['formulas'][0] = (
        r'\omega_i\equiv\frac{t_i}{p_i+t_i},\qquad \omega_i\propto\frac{1}{|\varepsilon_i^c|}',
        '這是「逆彈性法則」的特殊情況：t_i 為從量稅、p_i+t_i 為消費者面對的含稅價格，ω_i 是稅含價格楔；需有需求彼此獨立（或交叉效果可忽略）、分配權重不改變排序等強假設。一般 Ramsey rule 應用補償需求系統與邊際超額負擔，而不是只套單一 own-price elasticity。',
    )
    ch['traps'][0] = '逆彈性法則只是 Ramsey 商品稅問題的特殊情況；一旦有重要交叉需求或分配權重，不能只用自己的需求彈性排稅率。'

    # ch15 Labour supply: state the normal-leisure condition behind the income-effect direction.
    ch = _chapter(chapters, 'ch15')
    ch['intuition'][0] = '勞動所得稅降低稅後工資，替代效果會讓休閒相對變便宜，傾向減少工作；同時稅使可支配資源下降，若休閒是正常財，所得效果會使人減少休閒、反而增加工作。因此已就業者的工時總反應不能只由「稅率提高」判定；是否進入勞動市場的廣延邊際又是另一個決策。'
    for i, (term, desc) in enumerate(ch['definitions']):
        if term == '應稅所得彈性（ETI）':
            ch['definitions'][i] = (
                term,
                '應稅所得對淨留存率（net-of-tax rate，1-t）的百分比反應；它會混合工時、努力、報酬形式、合法避稅與逃漏等多種反應，因此不等同單純的勞動工時彈性。',
            )
    q = _question(questions, 'ch15-q05')
    q['explanation'] = '稅後工資下降的替代效果傾向減少工作；若休閒是正常財，所得效果可能使工作增加。參與決策與既有工作者的工時反應也不同，所以總效果不必然單向。'

    # ch16 Corporate taxation: add debt-equity financing bias without tying it to any current tax code.
    ch = _chapter(chapters, 'ch16')
    ch['intuition'].append(
        '若一套稅制允許利息在公司層級扣除、但股利或股權正常報酬沒有同等扣除，在其他條件相同時就可能形成「債務偏向」：負債融資的公司層級稅後成本相對較低。這是制度設計可能造成的融資扭曲，不代表所有國家、所有期間都具有完全相同的規則。'
    )
    ch['definitions'].append(
        ('債務偏向（Debt Bias）', '利息扣除與股權報酬稅務處理不對稱時，稅制可能相對鼓勵負債融資的效果。')
    )
    ch['traps'].append('「利息可扣除」不能直接延伸成任何制度都一定偏好負債；要先看股權報酬、利息限制與其他稅制規則。')

    # ch17 Property/wealth taxation: distinguish recurring net-wealth taxation from transfer taxes.
    ch = _chapter(chapters, 'ch17')
    ch['intuition'][1] = '財產稅、淨財富稅與財產移轉稅要分開。週期性財產稅通常以不動產等資產價值為稅基；淨財富稅通常以某一時點的資產減可扣除負債後的淨財富為稅基；遺產、贈與或其他移轉稅則針對資產移轉事件。土地供給接近固定時，對純土地租的課稅在理論上扭曲較小；對可移動資本或可新增建物則可能改變投資與地點選擇。'
    ch['definitions'].extend([
        ('淨財富稅（Net Wealth Tax）', '以納稅人在特定時點持有的應稅資產減可扣除負債後的淨財富存量為稅基的週期性租稅；實際納入資產與負債範圍依制度而異。'),
        ('財產移轉稅', '在遺產、贈與、交易或其他資產移轉事件發生時課徵的租稅；它和每年按持有資產課徵的財產／淨財富稅不是同一稅基。'),
    ])
    ch['formulas'][1] = (
        r'\Delta V\approx-\theta\,PV(\Delta\text{future net tax}),\quad 0\le\theta\le1',
        '用 θ 表示資本化程度的概念式。只有在供給極固定、買方完全預期未來淨稅負且其他條件穩定等強條件下，才可能接近完全資本化（θ≈1）；公共服務、移動與供給反應都會改變 θ。',
    )
    ch['traps'].append('財產稅、淨財富稅與遺產／贈與等移轉稅的課稅時點與稅基不同，不能只因都和「資產」有關就混成同一種稅。')

    # ch18 Matching grant: clarify that m is the grant share of eligible expenditure.
    ch = _chapter(chapters, 'ch18')
    ch['definitions'][4] = (
        '配合款（Matching Grant）',
        '上級政府按地方符合條件的支出依一定比例補助；若補助率 m 定義為上級政府負擔合格支出的比例，地方面對的自付價格為 (1-m)P。',
    )
    ch['formulas'][0] = (
        r'P_{local}=(1-m)P',
        'm 定義為上級政府負擔合格支出的比例。地方每新增 P 元合格支出，自付 (1-m)P；若題目用「每地方一元配多少上級款」等不同 matching rate 定義，必須先換算，不能直接套同一公式。',
    )

    # ch19 Debt dynamics: show the exact discrete-time formula before the common r-g approximation.
    ch = _chapter(chapters, 'ch19')
    ch['intuition'].append(
        '債務比變動還可能受「存量－流量調整」（stock-flow adjustment）影響，例如金融資產交易、匯率評價、承接或實現或有負債等。因此年度赤字與債務增加不必一一相等。最基本的 r-g 式先假設沒有這些額外調整，再討論利率、成長與初級餘額。'
    )
    ch['definitions'].append(
        ('存量－流量調整（Stock-flow Adjustment）', '不直接出現在當期初級赤字中、但會改變政府債務存量的其他因素，例如部分金融交易、評價變動或或有負債實現。')
    )
    ch['formulas'] = [
        (
            r'b_t=\frac{1+r_t}{1+g_t}b_{t-1}-ps_t',
            '在沒有存量－流量調整、r 與 g 使用一致的實質（或一致的名目）口徑時的簡化離散式。b_t 是期末債務/GDP，ps_t 是當期初級盈餘/GDP（盈餘取正）。',
        ),
        (
            r'\Delta b_t=\frac{r_t-g_t}{1+g_t}b_{t-1}-ps_t\approx(r_t-g_t)b_{t-1}-ps_t',
            '左式是上述簡化模型的精確差分，右式是 g 不大時常用的 r-g 近似。若改用初級赤字 d_t=-ps_t 且赤字取正，最後一項改為 +d_t。',
        ),
    ]
    ch['example'][0] = '假設期初債務比 b=60%，實質利率 r=4%、實質成長率 g=2%，且初級餘額為 0。精確簡化式給 Δb=[(0.04-0.02)/(1.02)]×0.60≈0.01176，也就是約上升 1.18 個 GDP 百分點；常用 r-g 近似則為 0.012，約 1.2 個百分點。'
    ch['example'][1] = '若用 r-g 近似，要大致穩定債務比，需要約 1.2% GDP 的初級盈餘；若用精確離散式則約為 1.18% GDP。考題若明示使用 Δb≈(r-g)b-ps，就依近似式作答；若題目要求精確差分，則保留 1+g 分母。'
    ch['traps'].append('把 (r-g)b 當成任何情況都精確的債務動態會出錯；精確離散式有 1+g 分母，實務分解還可能需要存量－流量調整。')
    for qid, exact_note in {
        'ch19-q01': '若改用精確差分，結果為 [(0.03-0.01)/1.01]×0.50≈0.00990，約 0.99 個百分點。',
        'ch19-q02': '若改用精確差分，結果為 [(0.04-0.02)/1.02]×0.60≈0.01176，約 1.18 個百分點。',
        'ch19-q03': '若改用精確穩定條件，所需初級盈餘約 [(0.04-0.02)/1.02]×0.60≈1.18% GDP。',
    }.items():
        q = _question(questions, qid)
        q['explanation'] += ' ' + exact_note
    q = _question(questions, 'ch19-q05')
    q['explanation'] = 'r<g 使既有債務比的自動動態較有利，但財政永續仍取決於未來初級收支、融資條件、風險與可能的存量－流量調整；跨期預算限制並未消失。'

    return chapters, questions


def finalize_generated_metadata(site_root):
    site = Path(site_root)
    manifest_path = site / 'books/public-finance/manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    manifest['version'] = VERSION
    notes = manifest.get('releaseNotes', [])
    v2_note = {
        'version': VERSION,
        'date': '2026-07-29',
        'title': '發布後獨立二次內容審計與糾錯',
        'changes': [
            '補齊 Lindahl 價格、失業保險、教育訊號、累進／比例／累退與淨財富稅等原 scope 已列但初版展開不足的核心內容',
            '修正 copayment 與 coinsurance 混稱、funded pension 等同個人帳戶的風險，以及 Ramsey 逆彈性法則與租稅歸宿公式的適用條件',
            '把公債動態由單一 r-g 近似升級為先給精確離散式，再說明 r-g 近似與 stock-flow adjustment',
            '精確化 excess burden、社會折現率、ETI、公司債務偏向、資產稅分類與 matching grant 的定義邊界',
            '題目 ID 與題數維持不變；同步修正 Lindahl、funded pension、醫療成本分擔、教育訊號與公債題詳解',
        ],
        'progressImpact': '章節 ID、題目 ID 與題數均未變；既有閱讀進度與錯題紀錄可沿用。',
    }
    notes = [n for n in notes if n.get('version') != VERSION]
    manifest['releaseNotes'] = [v2_note] + notes
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
