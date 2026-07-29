from __future__ import annotations

from copy import deepcopy

from industrial_economics_content import CHAPTERS as V1_CHAPTERS

VERSION = '2026.07.30-2'


def _chapter(chapters, chapter_id):
    for ch in chapters:
        if ch['id'] == chapter_id:
            return ch
    raise KeyError(chapter_id)


def build_chapters():
    chapters = deepcopy(V1_CHAPTERS)

    # ch02 — natural monopoly is a cost-subadditivity concept, not merely "one firm near MES".
    ch = _chapter(chapters, 'ch02')
    ch['intuition'][0] = (
        '固定成本高、邊際成本相對低時，平均成本常會在一段產量範圍內下降；'
        '但真正判斷規模經濟要看長期平均成本隨產量的變化，不能只由「固定成本很高」直接推出。'
    )
    ch['definitions'].append((
        '自然獨占（Natural Monopoly）',
        '在相關需求範圍內，由單一廠商供應市場的總成本低於把同一總產量拆給兩家以上廠商生產；本質上是成本函數的次可加性（subadditivity）。'
    ))
    ch['formulas'].append((
        'C(Q) <= C(q_1)+...+C(q_n),  where sum(q_i)=Q',
        '自然獨占的成本判準示意：對相關產量 Q，單一廠商供應的成本不高於任意拆分生產。平均成本下降是常見充分背景，但不是定義本身。'
    ))
    ch['example'][2] = (
        '若在市場實際需求範圍內，把總產量拆成兩家公司生產會重複承擔大量固定成本，'
        '而一家供應的總成本始終較低，才符合自然獨占的成本直覺；不能只因「市場看起來只能容納一家」就直接下結論。'
    )
    ch['traps'].append('把自然獨占直接定義成「市場只剩一家廠商」，而沒有比較單一供應與分拆供應的成本。')

    # ch03 — Lerner condition must be stated at an interior optimum on the elastic part of demand.
    ch = _chapter(chapters, 'ch03')
    ch['formulas'][2] = (
        'L = (P-MC)/P = 1/|epsilon|',
        '標準單一產品、可微需求、內點利潤最大化且廠商面對的需求彈性以絕對值表示時成立；有正加價的內點解位於 |epsilon|>1 的彈性區段。'
    )
    ch['intuition'][2] = (
        'Lerner index 用價格相對邊際成本的加價比例描述市場力量。它與需求彈性的簡單反比關係只是在標準單一產品內點定價的一階條件；'
        '若有多產品交叉效果、價格管制、容量限制或需求不可微，就不能機械套用。'
    )
    ch['exam'].append('使用 Lerner–彈性關係時，先確認是廠商面對的需求彈性，而且內點最適應位於需求的彈性區段。')

    # ch04 — welfare is not determined by total output alone; allocation across groups also matters.
    ch = _chapter(chapters, 'ch04')
    ch['intuition'][2] = (
        '價格歧視的福利效果不是固定方向。總產量是否增加是重要線索，但不是唯一判準：'
        '即使總量不變，不同市場之間的銷售重新配置也可能讓高邊際願付價格者被排除、低邊際願付價格者取得商品，進而改變總剩餘。'
    )
    ch['traps'][2] = '認為價格歧視一定降低總福利，或只要總產量不變就必然只是消費者剩餘與利潤之間的移轉。'
    ch['exam'][2] = '福利題先看總產量，再檢查不同群體間的配置與邊際願付價格；只有效率交易集合與配置都不變時，才可把差異主要視為剩餘移轉。'
    ch['checks'][2] = '價格歧視的福利判斷除了總產量，為什麼還要檢查不同市場之間的配置？'

    # ch06 — substantive algebraic error in v1: the b multiplying rivals' output was missing.
    ch = _chapter(chapters, 'ch06')
    ch['formulas'][1] = (
        'q_i = (a-c-b Q_-i)/(2b)',
        '線性逆需求 P=a-bQ、常數邊際成本 c 下的 Cournot 最佳反應；Q_-i 是其他廠商總產量。v1 曾漏寫 Q_-i 前的 b，本版已修正。'
    )
    ch['exam'].append('若 b 不等於 1，最佳反應中的競爭者產量必須先乘上 b；不要被 b=1 的例題掩蓋代數錯誤。')

    # ch09 — Hotelling formula assumes a covered market and an interior marginal consumer.
    ch = _chapter(chapters, 'ch09')
    ch['intuition'][1] = (
        'Hotelling 線性城市模型把消費者放在一條線上，廠商位置代表產品特性。消費者比較商品價格加上「距離成本」。'
        '教科書常用的無差異點公式通常還假設市場被兩家廠商完全覆蓋，而且解出的邊界消費者位於 0 與 1 之間。'
    )
    ch['formulas'][1] = (
        'x* solves P_1+t x = P_2+t(1-x)',
        '單位線兩端廠商的無差異消費者位置；標準解另需全市場覆蓋、內點 x* in [0,1] 與指定的距離成本形式。若解落在線段外或部分消費者不購買，需求分割方式要重做。'
    )
    ch['traps'].append('算出 x* 後不檢查是否落在 [0,1]，也不檢查市場是否真的完全覆蓋。')

    # ch11 — entry is an intertemporal investment decision; compare PV to sunk entry cost.
    ch = _chapter(chapters, 'ch11')
    ch['intuition'][1] = (
        '極限定價是在進入發生前維持較低價格，試圖影響潛在進入者對成本、需求或進入後利潤的判斷。'
        '在完全資訊且進入後競爭不受先前價格約束的簡單模型裡，單靠進入前低價未必能阻嚇；是否有效取決於它能否傳遞資訊、建立承諾或實際改變進入後報酬。'
    )
    ch['formulas'][0] = (
        'sum_t [pi_t/(1+r)^t] >= F_sunk',
        '簡化進入條件：把進入後各期可得的增量經濟利潤折現，再與不可回收的進入成本 F_sunk 比較；不能把「每期利潤」直接與一次性進入成本相比。'
    )
    ch['example'][0] = (
        '潛在進入者需投入不可回收 NT$10,000,000；若只預期營運 3 年、每年增量經濟利潤 NT$2,000,000，'
        '即使先忽略折現，三年合計 NT$6,000,000 仍不足以回收沉沒投入。真正判斷應再使用適當折現率計算現值。'
    )
    ch['exam'][0] = '先預測進入後各期增量經濟利潤並折現，再和沉沒進入成本比較；不要把流量利潤與一次性成本直接相比。'

    # ch12 — repeated-game condition and Taiwan law inference need explicit conditions.
    ch = _chapter(chapters, 'ch12')
    ch['intuition'][1] = (
        '重複賽局讓未來懲罰可以約束今天。廠商越重視未來、偏離越容易被發現且懲罰越可信，協調通常越容易維持。'
        '互動更頻繁有時能加快偵測，但若同時改變每期折現方式，不能只靠「次數變多」就無條件斷言協調一定更容易。'
    )
    ch['intuition'][2] = (
        '經濟模型中的默契協調與法律上的聯合行為不是同一判斷。單純平行價格可能來自共同成本或獨立反應；'
        '但台灣公平交易法第 14 條也明定，聯合行為的「合意」可依市場狀況、商品特性、成本與利潤、行為經濟合理性等相當依據推定，因此也不能反過來誤解成必須取得書面或口頭直接協議才可能成立。'
    )
    ch['formulas'][1] = (
        'delta >= (pi_D-pi_C)/(pi_D-pi_P)',
        '簡化永久懲罰設定下的臨界折現因子；需 pi_D>pi_C>pi_P，且偏離只在當期取得 pi_D、次期起永久得到 pi_P。改成有限懲罰或其他策略時門檻會改變。'
    )
    ch['traps'][0] = '看到價格相同就直接認定有卡特爾；反過來，也不能因沒有直接協議文件就斷言法律上絕不可能推定合意。'
    ch['exam'][2] = '制度題區分經濟上的協調可持續性與法律上的合意／證據判斷；台灣法下還要記得第 14 條容許依相當依據推定合意。'

    # ch13 — distinguish economic effects from Taiwan's current RPM rule.
    ch = _chapter(chapters, 'ch13')
    ch['definitions'][2] = (
        '轉售價格維持（RPM）',
        '上游對下游轉售價格施加限制的安排。經濟上可能涉及服務誘因與品牌內價格競爭；台灣現行公平交易法第 19 條原則禁止限制轉售價格，但有正當理由者例外，法律判斷不能只用經濟模型取代。'
    )
    ch['intuition'][2] = (
        '因此轉售價格維持、獨家交易、搭售與平台規則都不能只靠經濟效果的單一標籤判斷；要比較有效率與排除效果。'
        '若題目進一步問台灣法律，還要分辨不同安排分屬公平交易法第 19 條或第 20 條等規範，並依現行正當理由與限制競爭要件判斷。'
    )

    # ch15 — “observed price” was the wrong label for a broader effective cost concept.
    ch = _chapter(chapters, 'ch15')
    ch['formulas'][1] = (
        'Effective transaction cost = posted price + search/attention cost',
        '概念式：消費者承擔的有效交易成本可能高於標示價格。搜尋與注意力成本不是商品「觀察價格」本身，v1 的 observed price 用語過度簡化。'
    )

    # ch17 — make the two-sided-market definition more precise.
    ch = _chapter(chapters, 'ch17')
    ch['definitions'][2] = (
        '兩邊市場／平台',
        '平台連結至少兩個彼此產生跨邊外部性的使用者群體，且一側的參與或交易條件會影響另一側；分析時價格「結構」而不只是兩側價格總和可能影響平台交易量與參與。'
    )
    ch['intuition'][1] = (
        '兩邊平台同時服務互相影響的使用者群。平台不只決定總收費，還要決定價格結構：哪一邊收費、補貼或設為零價格，'
        '會透過跨邊外部性影響另一側參與。因此單看某一側的零價格或只把兩側價格相加，都可能漏掉核心機制。'
    )

    # ch18 — current Taiwan statutory wording and Article 14 inference.
    ch = _chapter(chapters, 'ch18')
    ch['intuition'][1] = (
        '台灣公平交易法第 5 條以一定商品或服務從事競爭的區域或範圍界定相關市場；第 7 條的「獨占」不只指經濟學上一家廠商，'
        '也包括在相關市場處於無競爭狀態，或具有壓倒性地位、可排除競爭能力的事業。教材仍以經濟分析為主，易變申報金額與最新處理原則回到公平交易委員會現行公開資料。'
    )
    ch['definitions'][1] = (
        '獨占（台灣法制度銜接）',
        '公平交易法第 7 條所稱獨占，包括事業在相關市場處於無競爭狀態，或具有壓倒性地位、可排除競爭之能力；其範圍比經濟學上單純「只有一家廠商」更廣。'
    )
    ch['definitions'][3] = (
        '聯合行為分析',
        '先分析競爭者協調是否影響市場功能；法律上再依公平交易法第 14 條檢查合意與市場影響。合意可依法定相當依據推定，因此「沒有直接協議證據」與「沒有合意」不是同一句話。'
    )
    ch['traps'][1] = '把經濟學上的平行行為直接等同法律上的聯合行為成立，或反過來誤以為沒有書面／口頭直接協議就絕不可能依法推定合意。'
    ch['exam'][2] = '制度細節以公平交易委員會最新公開資料為準；聯合行為題另檢查第 14 條的合意要件與依法定因素推定合意的可能。'
    ch['checks'][1] = '經濟模型與法律認定的分工是什麼？台灣法下沒有直接協議文件是否就必然排除聯合行為？'

    return chapters


CHAPTERS = build_chapters()

assert len(CHAPTERS) == 20
assert [c['id'] for c in CHAPTERS] == [f'ch{i:02d}' for i in range(20)]
