from __future__ import annotations

from money_banking_content import CHAPTERS

NUMERIC = {
'ch02-q01': {'question':'一年後確定收到 NT$10,500，市場一年期利率為 5%。這筆現金流今天的現值是多少？','answer':'NT$10,000。','explanation':'用 PV=FV/(1+i)：10,500/1.05=10,000。'},
'ch02-q02': {'question':'將 NT$100,000 以年利率 4% 複利兩年，兩年後的未來值是多少？','answer':'NT$108,160。','explanation':'FV=100,000×(1.04)^2=108,160。'},
'ch02-q05': {'question':'名目利率為 6%，預期通膨率為 2%。用低通膨 Fisher 近似，實質利率約多少？','answer':'約 4%。','explanation':'低通膨近似 r≈i−π^e=6%−2%=4%。精確式則使用 (1+i)=(1+r)(1+π^e)。'},
'ch03-q01': {'question':'某債券修正存續期間為 5，殖利率上升 0.5 個百分點。以一階近似，價格約變動多少？','answer':'約下降 2.5%。','explanation':'ΔP/P≈−D_mod×Δy=−5×0.005=−0.025，即約下降 2.5%；大幅利率變動需進一步考慮凸性。'},
'ch06-q01': {'question':'銀行總資產為 NT$1,000 億、總負債為 NT$920 億，權益是多少？','answer':'NT$80 億。','explanation':'由資產＝負債＋權益，權益=1,000−920=80 億。'},
'ch06-q02': {'question':'銀行淨利 NT$8 億、平均資產 NT$1,000 億，ROA 是多少？','answer':'0.8%。','explanation':'ROA=8/1,000=0.008=0.8%。'},
'ch06-q03': {'question':'銀行淨利 NT$8 億、平均權益 NT$80 億，ROE 是多少？','answer':'10%。','explanation':'ROE=8/80=0.10=10%。'},
'ch06-q04': {'question':'銀行利息收入 NT$80 億、利息支出 NT$50 億，淨利息收入是多少？','answer':'NT$30 億。','explanation':'淨利息收入=80−50=30 億；這不等於最終淨利。'},
'ch07-q01': {'question':'銀行一年內利率敏感資產 RSA=NT$300 億、利率敏感負債 RSL=NT$500 億，GAP 是多少？','answer':'-NT$200 億。','explanation':'GAP=RSA−RSL=300−500=−200 億。'},
'ch07-q02': {'question':'承上題 GAP=−NT$200 億，相關利率普遍上升 1 個百分點。簡化估計淨利息收入變化為多少？','answer':'約 -NT$2 億。','explanation':'ΔNII≈GAP×Δi=−200×0.01=−2 億。'},
'ch10-q01': {'question':'在沒有通貨外流、沒有超額準備等嚴格假設下，準備率 rr=10%，簡單存款乘數是多少？','answer':'10。','explanation':'簡單存款乘數=1/rr=1/0.10=10。這只是嚴格假設下的模型基準。'},
'ch10-q02': {'question':'若通貨—存款比率 c=0.2、超額準備率 e=0.05、準備率 rr=0.10，依 m=(1+c)/(rr+e+c)，貨幣乘數約多少？','answer':'約 3.43。','explanation':'m=1.2/(0.10+0.05+0.20)=1.2/0.35≈3.43；c、e 與信用行為會變，因此不是固定機械常數。'},
'ch11-q01': {'question':'名目貨幣餘額為 NT$200 萬，價格水準相對基期為 1.25。實質貨幣餘額是多少？','answer':'NT$160 萬。','explanation':'M/P=200/1.25=160 萬，以基期購買力表示。'},
'ch12-q02': {'question':'中央銀行向銀行買進 NT$50 億證券，並以銀行準備支付。在最簡情況下銀行準備增加多少？','answer':'增加 NT$50 億。','explanation':'央行資產端證券 +50 億，負債端銀行準備 +50 億，因此準備增加 50 億。'},
'ch15-q02': {'question':'名目利率 8%、預期通膨 3%。用低通膨 Fisher 近似，實質利率約多少？','answer':'約 5%。','explanation':'r≈i−π^e=8%−3%=5%。'},
'ch15-q03': {'question':'若長期實質利率約 3% 不變，預期通膨由 2% 升至 4%。依 Fisher effect 的近似直覺，名目利率約如何變？','answer':'約由 5% 升到 7%。','explanation':'近似 i≈r+π^e：原為 3%+2%=5%，之後為 3%+4%=7%。此結論需要長期實質利率大致不變等條件。'},
'ch16-q02': {'question':'預期通膨 2%、κ=0.5、正產出缺口 2%，供給衝擊為 0。依 π=π^e+κx+v，通膨是多少？','answer':'3%。','explanation':'π=2%+0.5×2%+0=3%。'},
'ch17-q01': {'question':'教學用 Taylor 型規則 i=r*+π+0.5(π−π*)+0.5x。若 r*=1%、π=4%、π*=2%、x=1%，i 是多少？','answer':'6.5%。','explanation':'i=1+4+0.5×(4−2)+0.5×1=6.5%。這是教學規則計算，不是任何央行依法必須採用的利率。'},
'ch19-q02': {'question':'本書固定 E=NT$/US$。進口商要支付 US$10,000；E 由 31 升至 32。新臺幣成本如何變？','answer':'由 NT$310,000 升到 NT$320,000。','explanation':'31×10,000=310,000；32×10,000=320,000。E 上升表示新臺幣貶值。'},
}

SPECIAL = {
'ch08-q01': {'question':'一家銀行資產長期可收回，但今日大量存款人同時提款，短期無法變現資產。這首先屬於什麼問題？最後貸款者的核心適用情境為何？','answer':'首先是流動性問題；核心適用於具還款／償付能力、但暫時流動性不足且難以由其他來源籌資的銀行。','explanation':'最後貸款者處理緊急流動性，不等於央行無條件填補所有資不抵債機構的信用損失。'},
'ch09-q01': {'question':'銀行核准 NT$100 萬新貸款並把款項記入借款人存款帳戶，銀行資產負債表最直接如何變動？','answer':'放款資產增加 NT$100 萬，存款負債增加 NT$100 萬。','explanation':'這是「放款創造存款」的最簡會計效果；借款人後續跨行支付會引發準備清算，銀行仍受資本、流動性、風險、資金成本與信用需求限制。'},
}


def default_question(ch, slot: int):
    term, desc = ch['definitions'][min(slot-1, len(ch['definitions'])-1)]
    formula, note = ch['formulas'][min(slot-1, len(ch['formulas'])-1)]
    if slot == 1:
        return {'question':f'下列關於「{term}」的敘述，最精確的定義是什麼？','answer':desc,'explanation':f'判斷關鍵是先辨認本章的正式定義。「{term}」在本書指：{desc}' }
    if slot == 2:
        return {'question':f'公式或關係「{formula}」應在什麼條件下使用？','answer':note,'explanation':f'公式不能脫離成立條件使用。本章給定的限制是：{note}' }
    if slot == 3:
        return {'question':f'根據本章機制，為什麼「{ch["title"]}」不能只靠一個帳面數字判斷？','answer':'必須同時追蹤機制、資產負債表或價格變化，以及題目給定的成立條件。','explanation':ch['intuition'][0]+' '+ch['intuition'][-1]}
    if slot == 4:
        return {'question':f'綜合題：若題目以「{ch["figure"][0]}」呈現流程，作答時最穩健的順序是什麼？','answer':'先辨認各節點與方向，再套用必要公式，最後檢查制度假設與單位。','explanation':'本書圖解用來壓縮機制；作答不能只背箭頭，還要回到定義、條件與資產負債表。'}
    trap = ch['traps'][0]
    return {'question':f'常見陷阱判斷：「{trap}」為什麼不能直接成立？','answer':'因為它忽略本章明示的條件、機制或反例，不能把條件性關係寫成無條件必然。','explanation':f'本章把這句列為常見錯誤。正確作法是回到「{ch["exam"][0]}」並補上成立條件。'}


def build_questions():
    items=[]
    for ch in CHAPTERS:
        for slot in range(1,6):
            qid=f'{ch["id"]}-q{slot:02d}'
            item={'id':qid,'chapterId':ch['id'],**default_question(ch,slot)}
            if qid in SPECIAL:
                item.update(SPECIAL[qid])
            if qid in NUMERIC:
                item.update(NUMERIC[qid])
            items.append(item)
    assert len(items)==100
    assert len({x['id'] for x in items})==100
    return items
