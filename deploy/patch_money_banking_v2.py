#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

BOOK = 'money-banking'
VERSION = '2026.07.29-2'

CORRECTIONS = {
    'ch02': '''
<section class="callout precision-note" id="v2-bond-return-precision">
<h2>二次複核：利率與債券報酬不要混用</h2>
<p><strong>票面利率</strong>是票息相對面額；<strong>當期收益率</strong>是當期票息相對市價；<strong>到期殖利率（YTM）</strong>是使承諾現金流折現值等於目前價格的內部報酬率；<strong>持有期間報酬率</strong>則取決於實際持有期間收到的現金流與買賣價差。四者不是同一個概念。</p>
<p>YTM 的標準解讀隱含持有至到期、無違約，且票息再投資條件與計算假設相容；若提前出售，實際報酬率可能與原先 YTM 不同。</p>
</section>
''',
    'ch03': '''
<section class="callout precision-note" id="v2-duration-precision">
<h2>二次複核：存續期間與殖利率曲線</h2>
<p>以存續期間估計債券價格變動，是對<strong>小幅殖利率變動</strong>的一階近似；殖利率變動較大時，凸性等二階效果會使近似誤差擴大。</p>
<p>殖利率曲線反轉可包含未來短率預期與期限溢酬的資訊，歷史上常被視為景氣訊號，但不能把它寫成對衰退的無條件必然預測。</p>
</section>
''',
    'ch08': '''
<section class="callout precision-note" id="v2-regulation-lolr-precision">
<h2>二次複核：銀行監理、金融穩定與最後貸款者</h2>
<p><strong>個體審慎監理</strong>著重單一金融機構的資本、槓桿、流動性與風險管理；<strong>總體審慎政策</strong>則著重金融體系共同曝險、順循環與系統性風險。兩者相關但目的層次不同。</p>
<p>Basel III 在本課只掌握資本、槓桿與流動性要求（如 LCR、NSFR）的經濟意義，不把完整法遵計算列為核心。</p>
<p>最後貸款者的經典核心情境，是對<strong>具償付／還款能力但暫時流動性不足、且難以從其他來源籌資的銀行</strong>提供緊急流動性；不能把這項功能解讀成對已喪失償付能力機構的無條件救助。存款保險與最後貸款者能降低擠兌風險，也可能增加道德危險。</p>
</section>
''',
    'ch09': '''
<section class="callout precision-note" id="v2-base-money-credit-creation">
<h2>二次複核：準備貨幣、銀行準備與放款創造存款</h2>
<p><strong>準備貨幣（reserve money／base money，常稱貨幣基數）</strong>不是「銀行準備金」的另一個獨立總量；銀行存放央行的準備只是準備貨幣的組成之一，另一重要部分是流通中通貨。</p>
<p>銀行核貸時可以同時形成借款人的存款，但這不代表放款不受限制。個別銀行仍須面對跨行清算、流動性、資本、信用風險、資金成本與監理約束；整體銀行體系的信用與貨幣也同時受借款需求與中央銀行操作環境影響。</p>
</section>
''',
    'ch10': '''
<section class="callout precision-note" id="v2-multiplier-boundary">
<h2>二次複核：貨幣乘數是模型，不是機械定律</h2>
<p><code>1/rr</code> 只能稱為<strong>簡單存款乘數</strong>。它需要沒有通貨外流、沒有超額準備、銀行願意放款且借款人願意借款等嚴格條件；因此不能把準備金與現實世界 M2 之間寫成固定倍數關係。</p>
<p>較一般的貨幣乘數把通貨—存款比率與超額準備等行為納入，但這仍是會隨制度、利率、風險與行為改變的關係，而不是中央銀行可以固定指定的常數。</p>
</section>
''',
    'ch13': '''
<section class="callout precision-note" id="v2-taiwan-policy-tools">
<h2>二次複核：臺灣央行工具與操作架構</h2>
<p>臺灣制度段落以中央銀行公開資料為準。官方目前列示的貨幣政策工具包含<strong>準備金制度、貼現窗口制度、公開市場操作、金融機構轉存款與選擇性信用管理</strong>；公開市場操作中可見央行存單等工具。</p>
<p>「走廊型」「地板型」是理解不同國家與不同準備金環境的操作框架，不應把其中任何一種寫成臺灣或所有央行永遠固定採用的唯一制度。利率、準備率與操作數量會變動，本書不把當期數值寫成永久定義。</p>
</section>
''',
    'ch15': '''
<section class="callout precision-note" id="v2-fisher-precision">
<h2>二次複核：Fisher 關係與 Fisher effect 分開</h2>
<p>名目利率、實質利率與預期通膨的精確關係寫成 <code>(1+i)=(1+r)(1+π^e)</code>；在通膨率與利率不高時，才常近似為 <code>i≈r+π^e</code>。</p>
<p>這個<strong>Fisher equation</strong>是名目與實質報酬的關係式；<strong>Fisher effect</strong>則是額外的經濟命題：在其他條件與長期實質利率大致不變等假設下，預期通膨上升會反映在較高名目利率。不能把等式本身當成已經證明因果效果。</p>
</section>
''',
    'ch18': '''
<section class="callout precision-note" id="v2-qe-precision">
<h2>二次複核：QE 與準備金</h2>
<p>量化寬鬆（QE）是中央銀行擴張或改變資產負債表組成的操作，並透過期限溢酬、資產價格、信用條件與預期等管道影響金融環境；它不是財政支出，也不等於把同額現金直接交給家庭。</p>
<p>銀行準備增加，不代表銀行放款、M2 或名目支出一定按固定乘數同比例增加；資本、風險、借款需求、金融市場與政策制度都會影響傳遞。</p>
</section>
''',
    'ch19': '''
<section class="callout precision-note" id="v2-fx-quote-precision">
<h2>二次複核：匯率方向先固定報價</h2>
<p>本書固定用 <code>E = NT$/US$</code>：1 美元需要多少新臺幣。E 上升表示美元變貴、<strong>新臺幣貶值</strong>；E 下降表示新臺幣升值。沒有先固定報價方式，就不能只憑「匯率上升」判斷本幣升貶。</p>
</section>
''',
}

QUESTION_NOTES = {
    'ch02-q05': '二次複核補充：若題目使用 Fisher 關係，須分清精確式與低通膨近似式；Fisher effect 另需要經濟行為與長期條件。',
    'ch03-q01': '二次複核補充：存續期間的價格變動公式是一階近似，最適合小幅殖利率變動。',
    'ch08-q01': '二次複核補充：最後貸款者的核心案例是具還款能力但流動性不足的銀行，不等於無條件救助資不抵債機構。',
    'ch09-q01': '二次複核補充：放款創造存款不代表無限放款；資本、流動性、清算、信用風險、資金成本與需求都構成限制。',
    'ch10-q01': '二次複核補充：1/rr 是嚴格假設下的簡單存款乘數，不是現實 M2 的固定機械倍數。',
    'ch10-q02': '二次複核補充：一般貨幣乘數納入通貨與超額準備等行為，但相關比率會變動。',
    'ch19-q02': '二次複核補充：本書固定 E=NT$/US$；E 上升代表新臺幣貶值。',
}

SEARCH_NOTES = {
    'ch02': '票面利率、當期收益率、到期殖利率與持有期間報酬率必須分開。',
    'ch03': '存續期間是小幅殖利率變動的一階近似；殖利率曲線反轉不是衰退的必然定律。',
    'ch08': '個體審慎與總體審慎目的層次不同；最後貸款者核心為具還款能力但流動性不足的銀行。',
    'ch09': '準備貨幣又稱貨幣基數；銀行準備只是其組成之一。放款創造存款仍受資本、流動性與清算等限制。',
    'ch10': '1/rr 是嚴格假設下的簡單存款乘數，不是現實廣義貨幣固定倍數。',
    'ch13': '臺灣央行公開列示準備金制度、貼現窗口、公開市場操作、轉存款與選擇性信用管理等工具。',
    'ch15': 'Fisher equation 是名目與實質報酬關係；Fisher effect 是另需假設的經濟命題。',
    'ch18': 'QE 是中央銀行資產負債表操作，不是財政支出；準備金增加不保證 M2 或放款固定倍增。',
    'ch19': '固定 E=NT$/US$ 時，E 上升代表新臺幣貶值。',
}


def append_before_end(text: str, block: str) -> str:
    if block.strip() in text:
        return text
    for marker in ('</article>', '</main>', '</body>'):
        if marker in text:
            return text.replace(marker, block + '\n' + marker, 1)
    return text + '\n' + block


def main(site_root: str) -> None:
    site = Path(site_root)
    root = site / 'books' / BOOK
    manifest_path = root / 'manifest.json'
    questions_path = root / 'questions.json'
    search_path = root / 'search.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    questions = json.loads(questions_path.read_text(encoding='utf-8'))
    search = json.loads(search_path.read_text(encoding='utf-8'))

    manifest['version'] = VERSION
    manifest['updatedAt'] = '2026-07-29'
    note = {
        'version': VERSION,
        'date': '2026-07-29',
        'title': '二次內容複核、糾錯與制度精確化',
        'changes': [
            '區分債券票面利率、當期收益率、YTM 與持有期間報酬，補上存續期間近似條件',
            '修正準備貨幣／貨幣基數、放款創造存款與貨幣乘數的現代制度邊界',
            '區分個體審慎與總體審慎監理，限縮最後貸款者的核心適用情境',
            '依臺灣央行公開資料精確化政策工具，並區分 Fisher equation 與 Fisher effect',
            '補強 QE、準備金與匯率報價方向，避免機械乘數與必然性敘述',
        ],
        'progressImpact': '初次正式發布；本次修正不改 20 個章節 ID、100 個題目 ID 或題數。',
    }
    notes = [n for n in manifest.get('releaseNotes', []) if n.get('version') != VERSION]
    manifest['releaseNotes'] = [note] + notes

    questions['version'] = VERSION
    qmap = {q['id']: q for q in questions['items']}
    for qid, extra in QUESTION_NOTES.items():
        if qid not in qmap:
            raise AssertionError(f'missing question for v2 note: {qid}')
        explanation = qmap[qid].get('explanation', '').rstrip()
        if extra not in explanation:
            qmap[qid]['explanation'] = explanation + ('\n' if explanation else '') + extra

    for chapter_id, block in CORRECTIONS.items():
        path = root / 'chapters' / f'{chapter_id}.html'
        if not path.is_file():
            raise AssertionError(f'missing chapter: {chapter_id}')
        text = path.read_text(encoding='utf-8')
        path.write_text(append_before_end(text, block), encoding='utf-8')

    touched = set()
    for entry in search['entries']:
        cid = entry.get('chapterId')
        if cid in SEARCH_NOTES and cid not in touched:
            note_text = SEARCH_NOTES[cid]
            if note_text not in entry['text']:
                entry['text'] = entry['text'].rstrip() + ' ' + note_text
            touched.add(cid)
    if touched != set(SEARCH_NOTES):
        raise AssertionError(f'missing search chapters for v2 notes: {set(SEARCH_NOTES) - touched}')

    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    questions_path.write_text(json.dumps(questions, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    search_path.write_text(json.dumps(search, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'MONEY_BANKING_V2_PATCH_OK corrections={len(CORRECTIONS)} question_notes={len(QUESTION_NOTES)} search_notes={len(SEARCH_NOTES)} version={VERSION}')


if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        raise SystemExit('usage: patch_money_banking_v2.py SITE_ROOT')
    main(sys.argv[1])
