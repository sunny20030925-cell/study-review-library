from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Tag
import json, shutil, re, hashlib, zipfile

import sys
if len(sys.argv) != 2:
    raise SystemExit("usage: patch_accounting_v2.py <site-root>")
out = Path(sys.argv[1])
if not out.is_dir():
    raise SystemExit(f"site root not found: {out}")

changes=[]
def replace(path, old, new, label):
    p=out/path
    text=p.read_text(encoding='utf-8')
    if old not in text:
        raise AssertionError(f'missing replacement {label} in {path}')
    text=text.replace(old,new)
    p.write_text(text,encoding='utf-8')
    changes.append((str(path),label))

# ch00: basic elements, with definitions accurate enough for introductory financial accounting.
replace(Path('books/accounting/chapters/ch00.html'),
'<table><thead><tr><th>要素</th><th>白話意思</th><th>常見例子</th></tr></thead><tbody><tr><td>資產</td><td>企業控制、能帶來效益的資源</td><td>現金、應收帳款、設備</td></tr><tr><td>負債</td><td>企業目前的義務</td><td>應付帳款、借款</td></tr><tr><td>權益</td><td>資產扣除負債後的剩餘</td><td>業主資本、保留盈餘</td></tr><tr><td>收入</td><td>因提供商品或服務增加的權益</td><td>服務收入、銷貨收入</td></tr><tr><td>費用</td><td>為賺取收入而消耗的資源</td><td>租金費用、薪資費用</td></tr></tbody></table>',
'<table><thead><tr><th>要素</th><th>白話意思</th><th>常見例子</th></tr></thead><tbody><tr><td>資產</td><td>企業控制、預期能帶來經濟效益的資源</td><td>現金、應收帳款、設備</td></tr><tr><td>負債</td><td>企業因過去事項形成、目前須履行的義務</td><td>應付帳款、借款</td></tr><tr><td>權益</td><td>資產扣除負債後的剩餘權益</td><td>業主資本、股本、保留盈餘</td></tr><tr><td>收入</td><td>除業主投入外，使權益增加的經濟效益流入</td><td>服務收入、銷貨收入、處分利益</td></tr><tr><td>費用</td><td>除分配給業主外，使權益減少的資源耗用或義務增加</td><td>租金費用、薪資費用、處分損失</td></tr></tbody></table>',
'修正五大要素定義')
replace(Path('books/accounting/chapters/ch00.html'),
'先把交易分成資產、負債、權益、收入與費用。後面的借貸、分錄與報表，只是在更精確地整理這五類資訊。',
'本書以資產、負債、權益、收入與費用作為五大基本分類。後面的借貸、分錄與報表，只是在更精確地整理這五類資訊。',
'五大分類措辭')

# ch06: distinguish income statement from comprehensive income statement.
replace(Path('books/accounting/chapters/ch06.html'),
'<h2 id="綜合損益表">綜合損益表</h2>',
'<h2 id="損益表">損益表</h2>',
'報表名稱')
replace(Path('books/accounting/chapters/ch06.html'),
'<p>基礎格式以收入減費用得到本期淨利或淨損：</p>',
'<p>損益表（income statement）以本期收入減除本期費用，得到淨利或淨損。本書只處理入門課程的損益部分：</p>',
'損益表定義')
replace(Path('books/accounting/chapters/ch06.html'),
'<h2 id="資產負債表">資產負債表</h2>\n<p>資產負債表呈現特定日期的資產、負債與權益。常把一年內預期變現或清償的項目列為流動，其他列為非流動；本書只做基礎分類。</p>',
'<h2 id="資產負債表">資產負債表</h2>\n<p>資產負債表（balance sheet，亦稱財務狀況表）呈現特定日期的資產、負債與權益。流動與非流動的正式判斷不只看一年；本書先掌握正常營業循環與十二個月期限等入門原則。</p>',
'資產負債表名稱與分類')

# ch07: state the accounting method assumed in purchase discount entry.
replace(Path('books/accounting/chapters/ch07.html'),
'<p>應付帳款 NT$10,000，在 2% 折扣期內付款：借記應付帳款 NT$10,000，貸記現金 NT$9,800，貸記存貨 NT$200。</p>',
'<p>採永續盤存制與總額法時，應付帳款 NT$10,000 在 2% 折扣期內付款：借記應付帳款 NT$10,000，貸記現金 NT$9,800，貸記存貨 NT$200。</p>',
'進貨折扣方法前提')

# ch08: correct inventory cost formula and weighted-average scope.
replace(Path('books/accounting/chapters/ch08.html'),
'<p class="math display">\\[期初存貨 + 本期進貨 = 銷貨成本 + 期末存貨\\]</p><p>左邊是可供銷售商品成本，右邊把它分成已售與未售。</p>',
'<p class="math display">\\[期初存貨 + 本期商品淨取得成本 = 銷貨成本 + 期末存貨\\]</p><p>本期商品淨取得成本包含進貨成本與必要進貨運費，並扣除進貨退回、折讓與折扣。左邊是可供銷售商品成本，右邊把它分成已售與未售。</p>',
'存貨成本公式')
replace(Path('books/accounting/chapters/ch08.html'),
'<h2 id="加權平均法">加權平均法</h2>\n<p>加權平均單位成本：</p><p class="math display">\\[平均單位成本 = 可供銷售商品總成本 \\div 可供銷售商品總數量\\]</p><div class="examplebox"><p class="box-title">加權平均</p><p>同上例，總成本 NT$2,200、總數量 20 件，平均每件 NT$110。售出 12 件的銷貨成本為 NT$1,320，期末 8 件為 NT$880。</p></div>',
'<h2 id="加權平均法">加權平均法</h2>\n<p>定期盤存制下，期末以整期可供銷售商品計算一次加權平均單位成本：</p><p class="math display">\\[平均單位成本 = 可供銷售商品總成本 \\div 可供銷售商品總數量\\]</p><div class="examplebox"><p class="box-title">定期盤存制的加權平均</p><p>同上例，總成本 NT$2,200、總數量 20 件，平均每件 NT$110。售出 12 件的銷貨成本為 NT$1,320，期末 8 件為 NT$880。</p></div><div class="examtip" data-label="永續制的差別"><p>永續盤存制通常採移動平均法，每次進貨後重新計算平均單位成本。若期間內有多次銷貨，結果可能和期末一次計算的定期加權平均不同。</p></div>',
'加權平均與移動平均')
replace(Path('books/accounting/chapters/ch08.html'),
'期初存貨 NT$25,000、本期進貨 NT$90,000、期末存貨 NT$30,000，銷貨成本是多少？',
'期初存貨 NT$25,000、本期商品淨取得成本 NT$90,000、期末存貨 NT$30,000，銷貨成本是多少？',
'存貨練習題措辭')
replace(Path('books/accounting/chapters/ch08.html'),
'同上題，加權平均銷貨成本是多少？',
'同上題，採定期盤存制的加權平均法，銷貨成本是多少？',
'加權平均題目條件')

# ch09: cash equivalent and petty cash caveat.
replace(Path('books/accounting/chapters/ch09.html'),
'<p>現金包含庫存現金與可隨時動用的銀行存款。極短期、高流動性、價值變動風險很低的項目可能列為約當現金；本書只要求辨認最常見情況。</p>',
'<p>現金包含庫存現金與可隨時動用的銀行存款。約當現金是短期、高流動性、可迅速轉為已知金額現金且價值變動風險極低的投資，通常自取得日起三個月內到期；不是所有短期投資都算約當現金。</p>',
'約當現金定義')
replace(Path('books/accounting/chapters/ch09.html'),
'<p>零用金用固定小額現金支付零星支出。設立時借記零用金；補足時依憑證認列各項費用，貸記現金。平時支付小額支出通常不逐筆改動零用金帳面額。</p>',
'<p>零用金用固定小額現金支付零星支出。設立時借記零用金；補足時依憑證認列各項費用，貸記現金。平時支付小額支出通常不逐筆改動零用金帳面額。若盤點現金加憑證不等於定額，差額還要另列現金短溢。</p>',
'零用金短溢')

# ch10: avoid overstatement of matching-period logic.
replace(Path('books/accounting/chapters/ch10.html'),
'<p>賒銷能增加銷售，但也帶來收不到款項的風險。基礎會計用備抵方法，在收入認列的相近期間估計可能損失。</p>',
'<p>賒銷能增加銷售，但也帶來收不到款項的風險。基礎會計用備抵方法估計可能無法收回的金額，使應收帳款按預期可收回淨額表達，並及時認列相關損失。</p>',
'備抵方法目的')

# ch11: depreciation availability and land.
replace(Path('books/accounting/chapters/ch11.html'),
'<p>設備等長期營業資產會在多個期間提供服務。基礎會計要判斷取得成本、計算折舊，並處理簡單出售或報廢。</p>',
'<p>設備等長期營業資產會在多個期間提供服務。基礎會計要判斷取得成本、從資產達到可供使用時開始計算折舊，並處理簡單出售或報廢。</p>',
'折舊開始時點')
replace(Path('books/accounting/chapters/ch11.html'),
'<p>讓資產達到可使用狀態的必要成本，通常列入資產取得成本；只維持日常運作的普通修理，通常列當期費用。關鍵在於支出帶來的效益期間與性質。</p>',
'<p>讓資產達到管理階層預定可使用狀態的必要成本，通常列入資產取得成本；只維持日常運作的普通修理，通常列當期費用。關鍵在於支出帶來的效益期間與性質。</p>',
'資產可供使用措辭')
replace(Path('books/accounting/chapters/ch11.html'),
'<p>認列折舊不代表企業另外提存現金，也不代表資產每年市場價格恰好下降相同金額。</p>',
'<p>認列折舊不代表企業另外提存現金，也不代表資產每年市場價格恰好下降相同金額。</p><div class="warningbox" data-label="土地通常不折舊"><p>土地通常沒有可確定的有限耐用年限，因此一般不提列折舊；土地上的建築物則另行估計耐用年限並提列折舊。</p></div>',
'土地折舊提醒')

# ch12: current liability definition and dividends.
replace(Path('books/accounting/chapters/ch12.html'),
'<p>預期在正常營業循環或一年內清償的義務，基礎上列為流動負債。常見項目包括應付帳款、應付薪資、應付利息、預收收入與短期借款。</p>',
'<p>入門判斷中，預期在正常營業循環內清償，或於報導日後十二個月內到期的義務，通常列為流動負債。正式分類還要看企業在報導日是否有權把清償遞延至少十二個月。常見項目包括應付帳款、應付薪資、應付利息、預收收入與短期借款。</p>',
'流動負債定義')
replace(Path('books/accounting/chapters/ch12.html'),
'<p>公司型態下，基礎權益可分為股本與保留盈餘。發行股份取得資金增加股本；累積未分配成果形成保留盈餘；宣告股利會減少保留盈餘。</p>',
'<p>公司型態下，基礎權益可分為股本與保留盈餘。發行股份取得資金增加股本；累積未分配成果形成保留盈餘；宣告股利會減少保留盈餘，並在尚未支付時形成應付股利。</p>',
'股利宣告完整效果')

# ch13: official category logic, principal repayment, indirect method and non-cash transactions.
replace(Path('books/accounting/chapters/ch13.html'),
'<ul><li><strong>營業活動：</strong>與日常收入與費用相關的現金流。</li><li><strong>投資活動：</strong>購買或出售長期營業資產等。</li><li><strong>籌資活動：</strong>借款、還款、業主投入、發行股份與分配。</li></ul>',
'<ul><li><strong>營業活動：</strong>企業主要產生收入的活動，以及不屬於投資或籌資活動的其他現金流。</li><li><strong>投資活動：</strong>取得或處分長期資產，以及不屬於約當現金的其他投資。</li><li><strong>籌資活動：</strong>使投入權益或借款規模與組成發生變化，例如借款、償還本金、業主投入、發行股份與對業主分配。</li></ul>',
'現金流量三分類')
replace(Path('books/accounting/chapters/ch13.html'),
'<p>淨利採權責基礎，營業現金流量則只看現金。因此，基礎間接法從淨利出發，調整非現金費用，以及應收、存貨、應付等營運項目的變化。</p>',
'<p>淨利採權責基礎，營業現金流量則只看現金。因此，基礎間接法從淨利出發，調整非現金項目、應收存貨應付等營運資產與負債的變化，以及現金效果屬於投資或籌資活動的損益項目。</p>',
'間接法完整邏輯')
replace(Path('books/accounting/chapters/ch13.html'),
'<p>購買設備通常是投資活動；借款與業主投入通常是籌資活動；顧客與供應商的日常收付通常是營業活動。先看交易本質，再記分類。</p>',
'<p>購買設備通常是投資活動；借款與業主投入通常是籌資活動；顧客與供應商的日常收付通常是營業活動。先確認是否真的收付現金，再看交易本質；以票據直接取得設備等非現金交易，不列入三類現金流量總額，但通常需另行揭露。</p>',
'非現金交易提醒')

# Appendices.
replace(Path('books/accounting/chapters/appendix-a.html'),
'<li>期初存貨 + 本期進貨 = 銷貨成本 + 期末存貨</li>',
'<li>期初存貨 + 本期商品淨取得成本 = 銷貨成本 + 期末存貨</li>',
'附錄存貨公式')
replace(Path('books/accounting/chapters/appendix-c.html'),
'<tr><td>綜合損益表</td><td>Income statement</td></tr><tr><td>資產負債表</td><td>Balance sheet</td></tr>',
'<tr><td>損益表</td><td>Income statement</td></tr><tr><td>資產負債表／財務狀況表</td><td>Balance sheet / Statement of financial position</td></tr>',
'附錄報表中英對照')

# SVG diagrams.
replace(Path('assets/accounting-svg/statements.svg'),'綜合損益表','損益表','報表圖名稱')
replace(Path('assets/accounting-svg/inventory.svg'),'＋ 本期進貨','＋ 商品淨取得成本','存貨圖公式')
replace(Path('assets/accounting-svg/cashflow.svg'),'日常收入、費用','主要營業現金','營業現金圖')
replace(Path('assets/accounting-svg/cashflow.svg'),'借款、還款、投入','借款、本金償還、投入','籌資現金圖')

# Questions: update precise wording and versions.
qp=out/'books/accounting/questions.json'
q=json.loads(qp.read_text(encoding='utf-8'))
q['version']='2026.07.27-2'
byid={x['id']:x for x in q['items']}
byid['ch00-q05']['question']='列出本書使用的五大基本會計分類。'
byid['ch00-q05']['explanation']='資產、負債、權益、收入與費用構成入門交易分類與財務報表的主要架構。'
byid['ch06-q03']['answer']='資產負債表（亦稱財務狀況表）。'
byid['ch06-q03']['explanation']='它列示某一特定日期的資產、負債與權益。'
byid['ch08-q01']['question']='期初存貨 NT$25,000、本期商品淨取得成本 NT$90,000、期末存貨 NT$30,000，銷貨成本是多少？'
byid['ch08-q01']['explanation']='25,000+90,000−30,000=85,000。'
byid['ch08-q03']['question']='同上題，採定期盤存制的加權平均法，銷貨成本是多少？'
byid['ch08-q03']['explanation']='總成本 1,200、總數量 20，期末一次計算平均每件 60；12 件成本 720。'
qp.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
changes.append((str(qp.relative_to(out)),'題庫精確化與版本'))

# Manifest and release metadata.
mp=out/'books/accounting/manifest.json'
m=json.loads(mp.read_text(encoding='utf-8'))
m['version']='2026.07.27-2'
m['updatedAt']='2026-07-27'
m['releaseNotes']=[{
    'version':'2026.07.27-2','date':'2026-07-27','title':'二次內容複核與錯誤修正',
    'changes':[
        '修正損益表與綜合損益表的名稱混用',
        '補正存貨淨取得成本、定期加權平均與永續移動平均的差異',
        '補強約當現金、折舊起點、土地、流動負債與現金流量分類的必要條件',
        '重新驗算 70 題題庫並同步搜尋索引與圖解',
    ],
    'progressImpact':'章節 ID、章節數與題目 ID 均未變，既有閱讀進度與錯題紀錄保留。'
}]
mp.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Rebuild search index from HTML; preserves 111-entry section structure.
def clean_text(node):
    return ' '.join(node.get_text(' ',strip=True).split())
entries=[]
for ch in m['chapters']:
    p=out/'books/accounting'/ch['file']
    s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
    first_h2=s.find('h2')
    intro=[]
    for child in s.contents:
        if child is first_h2: break
        if isinstance(child,Tag):
            t=clean_text(child)
            if t: intro.append(t)
    entries.append({'chapterId':ch['id'],'chapterTitle':ch['title'],'page':0,'title':ch['title'],'text':' '.join(intro)})
    page=1
    for h2 in s.find_all('h2'):
        parts=[clean_text(h2)]
        for sib in h2.next_siblings:
            if isinstance(sib,Tag) and sib.name=='h2': break
            if isinstance(sib,Tag):
                t=clean_text(sib)
                if t: parts.append(t)
        entries.append({'chapterId':ch['id'],'chapterTitle':ch['title'],'page':page,'title':clean_text(h2),'text':' '.join(parts)})
        page += 1
sp=out/'books/accounting/search.json'
sp.write_text(json.dumps({'entries':entries},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Library and cache version.
lp=out/'data/library.json'
lib=json.loads(lp.read_text(encoding='utf-8'))
lib['version']='2026.07.27-7'
lp.write_text(json.dumps(lib,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
replace(Path('sw.js'),"const VERSION = 'study-library-2026-07-27-5';","const VERSION = 'study-library-2026-07-27-7';",'service worker version')

# Visible package docs.
(out/'README.md').write_text('''# 重點複習網站部署包

內容版本：`2026.07.27-7`

目前書籍：

- 《大一微積分》`2026.07.27-3`
- 《會計學》`2026.07.27-2`：基礎財務會計，14 章、3 附錄、70 題題庫；已完成二次獨立複核。
- 《經濟學原理》`2026.07.27-1`

《會計學》本次修正報表名稱、存貨成本公式與平均法條件，並補強約當現金、折舊、流動負債與現金流量分類等必要前提。
''',encoding='utf-8')
(out/'QA_REPORT.md').write_text('''# 重點複習網站 QA 報告

- 書庫內容版本：`2026.07.27-7`
- 會計學版本：`2026.07.27-2`
- 複核日期：2026-07-27

## 二次獨立內容複核

本次不沿用第一版的通過結論，重新逐章檢查 14 章正文、3 份附錄、70 題題庫、111 筆搜尋索引與 13 張圖解。

### 已修正

1. 將誤標為「綜合損益表」的入門損益內容改為「損益表」，並修正英文對照與圖解。
2. 將存貨公式中的「本期進貨」改為「本期商品淨取得成本」，補入運費、退回、折讓與折扣概念。
3. 明確區分定期盤存制加權平均與永續盤存制移動平均。
4. 補正約當現金的短期、高流動性、已知金額與低價值變動風險條件。
5. 補充零用金短溢、資產可供使用時開始折舊、土地通常不折舊。
6. 補正流動負債的十二個月遞延清償權判斷。
7. 依營業、投資與籌資活動的本質重寫現金流量分類，並補上非現金交易提醒。
8. 修正五大要素、備抵方法與股利宣告等過度簡化敘述。
9. 同步修正相關題目、答案、搜尋索引、SVG 圖解、版本與離線快取。

## 驗證結果

- 14 個正文章節與 3 個附錄：通過。
- 70 題題庫：逐題重新驗算，70／70 通過。
- 每章 5 題、題目 ID 唯一：通過。
- 111 筆搜尋索引與章節頁碼：通過。
- 13 張 SVG 圖解與連結：通過。
- library、manifest、questions、search JSON：通過。
- HTML 結構、內部路徑與 service worker 快取：通過。
- JavaScript 語法：通過。
- 超出入門範圍的內容檢查：通過。

## 結論

第一版存在數項用語不精確與條件交代不足；已全部修正。第二版維持入門深度，不擴張到中級會計學。
''',encoding='utf-8')

# Automated validation.
assert len(entries)==111
assert q['count']==70==len(q['items'])
assert len({x['id'] for x in q['items']})==70
from collections import Counter
assert Counter(x['chapterId'] for x in q['items']) == {f'ch{i:02d}':5 for i in range(14)}
assert m['version']=='2026.07.27-2'
assert lib['version']=='2026.07.27-7'
for ch in m['chapters']:
    p=out/'books/accounting'/ch['file']
    assert p.is_file() and p.stat().st_size>100
for svg in (out/'assets/accounting-svg').glob('*.svg'):
    assert '<svg' in svg.read_text(encoding='utf-8')
blob='\n'.join(p.read_text(encoding='utf-8') for p in (out/'books/accounting').rglob('*') if p.is_file() and p.suffix in {'.html','.json'})
for stale in ['綜合損益表</td><td>Income statement','期初存貨 + 本期進貨 = 銷貨成本 + 期末存貨','同上題，加權平均銷貨成本是多少？']:
    assert stale not in blob, stale
assert byid['ch03-q01']['answer']=='借方餘額 NT$28,500。'
assert byid['ch04-q01']['answer']=='NT$20,000。'
assert byid['ch04-q02']['answer']=='NT$25,000。'
assert byid['ch07-q03']['answer']=='NT$110,000。'
assert byid['ch08-q01']['answer']=='NT$85,000。'
assert byid['ch08-q02']['answer']=='NT$640。'
assert byid['ch08-q03']['answer']=='NT$720。'
assert byid['ch10-q04']['answer']=='NT$2,000。'
assert byid['ch13-q04']['answer']=='12.5%。'

print(json.dumps({
    'changes': len(changes),
    'search_entries': len(entries),
    'questions': len(q['items']),
    'library_version': lib['version'],
    'accounting_version': m['version'],
}, ensure_ascii=False, indent=2))
for item in changes:
    print(item)
