#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import sys
from html.parser import HTMLParser
from pathlib import Path

BOOK_ID = 'intermediate-accounting'
OLD_VERSION = '2026.07.29-1'
NEW_VERSION = '2026.07.29-2'


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        value = ' '.join(data.split())
        if value:
            self.parts.append(value)


def search_text(markup: str) -> str:
    parser = TextExtractor()
    parser.feed(markup)
    return html.unescape(' '.join(parser.parts))[:600]


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise AssertionError(f'{label}: expected exactly one old occurrence, got {count}')
    return text.replace(old, new, 1)


def patch_html(path: Path, replacements: list[tuple[str, str, str]]) -> None:
    text = path.read_text(encoding='utf-8')
    for old, new, label in replacements:
        text = replace_once(text, old, new, label)
    path.write_text(text, encoding='utf-8')


def assert_v2_markers(root: Path) -> None:
    required = {
        'chapters/ch01.html': ['不要求該效益「很可能」流入', '不是資產定義本身的固定機率門檻'],
        'chapters/ch02.html': ['僅要求在報導日後遵守的條件不影響當日分類', '可能需要附註揭露'],
        'chapters/ch04.html': ['為支應短期現金承諾而持有', '自取得日起原始到期日約三個月內'],
        'chapters/ch07.html': ['使用該資產生產存貨', '依 IAS 2 判斷是否進入存貨成本'],
        'chapters/ch11.html': ['不得重分類至損益，但可在權益內移轉', '股利通常列入損益，除非該股利明確代表投資成本的一部分收回', '2026 IFRS 9 更新提醒'],
        'chapters/ch12.html': ['FVTPL 金融負債的交易成本則於發生時認列損益', '2026 電子支付除列提醒'],
        'chapters/ch17.html': ['不超過 12 個月且不含購買選擇權', '資產「全新時」的價值判斷'],
        'chapters/ch18.html': ['單一交易的初始認列豁免', '租賃與除役義務是常見例子'],
        'chapters/ch21.html': ['以 IFRS 18 的「營業損益」小計作為營業現金流調節起點', '利息收入與股利收入原則列投資活動', '利息支出與股利支付原則列籌資活動'],
        'chapters/appendix-b.html': ['2026 現行修正提醒', 'Annual Improvements—Volume 11', '自然條件相依電力合約'],
    }
    for relative, tokens in required.items():
        text = (root / relative).read_text(encoding='utf-8')
        for token in tokens:
            if token not in text:
                raise AssertionError(f'{relative}: missing v2 marker {token!r}')


def main(site_root: str) -> None:
    site = Path(site_root)
    root = site / 'books' / BOOK_ID
    manifest_path = root / 'manifest.json'
    questions_path = root / 'questions.json'
    search_path = root / 'search.json'

    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    questions = json.loads(questions_path.read_text(encoding='utf-8'))
    current_version = manifest['version']
    if current_version not in {OLD_VERSION, NEW_VERSION}:
        raise AssertionError(f'unexpected manifest version {current_version}')
    if questions['version'] not in {OLD_VERSION, NEW_VERSION}:
        raise AssertionError(f'unexpected questions version {questions["version"]}')

    if current_version == OLD_VERSION:
        patch_html(root / 'chapters/ch01.html', [
            ('<h2 id="資產與負債">資產與負債</h2><p>資產是企業因過去事項所控制的現時經濟資源；負債是企業因過去事項而負有移轉經濟資源的現時義務。關鍵不是「有沒有實體」，而是控制與義務。</p>',
             '<h2 id="資產與負債">資產與負債</h2><p>資產是企業因過去事項所控制的現時經濟資源；負債是企業因過去事項而負有移轉經濟資源的現時義務。經濟資源本質上是具有產生經濟效益潛力的權利；符合資產定義不要求該效益「很可能」流入，低機率會影響認列、衡量或揭露判斷，但不是資產定義本身的固定機率門檻。關鍵不是「有沒有實體」，而是權利、控制與義務。</p>',
             'ch01 asset definition')
        ])

        patch_html(root / 'chapters/ch02.html', [
            ('<h2 id="流動與非流動">流動與非流動</h2><p>資產與負債通常依流動／非流動分類。負債判斷重點之一，是企業在報導日是否具有將清償遞延至少十二個月的權利，而非只看管理階層主觀打算。</p>',
             '<h2 id="流動與非流動">流動與非流動</h2><p>資產與負債通常依流動／非流動分類。負債判斷重點之一，是企業在報導日是否具有將清償遞延至少十二個月的實質權利，而非只看管理階層主觀打算。若該權利受借款契約條款限制，須分辨條款何時必須遵守：要求在報導日或以前遵守的條件會影響報導日分類；僅要求在報導日後遵守的條件不影響當日分類，但可能需要附註揭露相關條款與提前清償風險。</p>',
             'ch02 covenant classification')
        ])

        patch_html(root / 'chapters/ch04.html', [
            ('<h2 id="現金與受限制存款">現金與受限制存款</h2><p>現金列報要看是否可供一般營運使用；重大受限制款項可能需要依限制期間與性質另行分類或揭露。約當現金要求短期、高度流動、可隨時轉換成確定金額且價值變動風險甚低。</p>',
             '<h2 id="現金與受限制存款">現金與受限制存款</h2><p>現金列報要看是否可供一般營運使用；重大受限制款項可能需要依限制期間與性質另行分類或揭露。約當現金是為支應短期現金承諾而持有、而非為投資或其他目的，並須短期、高度流動、可迅速轉換成已知金額且價值變動風險甚低；實務上通常只有自取得日起原始到期日約三個月內的投資才符合「短期」特徵。</p>',
             'ch04 cash equivalents')
        ])

        patch_html(root / 'chapters/ch07.html', [
            ('<h2 id="除役義務">除役義務</h2><p>若取得或使用資產產生依法或推定必須拆除、移除或復原場址的現時義務，初始估計現值通常同時增加 PPE 成本與負債準備。其後時間經過造成的負債增加，通常認列融資成本。</p>',
             '<h2 id="除役義務">除役義務</h2><p>若取得、建造資產時即產生依法或推定必須拆除、移除或復原場址的現時義務，初始估計現值通常同時納入 PPE 成本並認列負債準備。若義務是日後「使用該資產生產存貨」的結果，該期間新增的相關成本應依 IAS 2 判斷是否進入存貨成本，而不是一律再加到 PPE。其後單純因時間經過造成的折現轉回，通常認列融資成本。</p>',
             'ch07 decommissioning boundary')
        ])

        patch_html(root / 'chapters/ch11.html', [
            ('<h2 id="權益工具指定">權益工具指定</h2><p>非交易目的的權益投資，初始認列時可作不可撤銷選擇將後續公允價值變動列 OCI；其累積 OCI 日後不重分類至損益。股利原則在符合收益定義時列損益。</p>',
             '<h2 id="權益工具指定">權益工具指定</h2><p>非交易目的且符合 IFRS 9 範圍的權益投資，初始認列時可逐項作不可撤銷選擇，將後續公允價值變動列 OCI；其累積 OCI 日後不得重分類至損益，但可在權益內移轉。股利通常列入損益，除非該股利明確代表投資成本的一部分收回。</p>',
             'ch11 equity FVOCI dividends'),
            ('<div class="summarybox" data-label="本章收尾"><p>債務工具：業務模式＋SPPI → AC／FVOCI／FVTPL；權益工具另判斷是否交易目的及是否作 FVOCI 指定。</p></div>',
             '<h2 id="2026 IFRS 9 更新提醒">2026 IFRS 9 更新提醒</h2><p>2026 年起生效的金融工具分類與衡量修正進一步釐清含或有事件連動特徵的契約現金流如何做 SPPI 評估；不能只因現金流會隨或有事件改變，就機械式判定一定不符合 SPPI，仍須依修正後要求分析該特徵與基本放款風險及成本的關係。核心分類地圖仍是業務模式＋契約現金流特徵。</p><div class="summarybox" data-label="本章收尾"><p>債務工具：業務模式＋SPPI → AC／FVOCI／FVTPL；權益工具另判斷是否交易目的及是否作 FVOCI 指定。</p></div>',
             'ch11 2026 amendment')
        ])

        patch_html(root / 'chapters/ch12.html', [
            ('<h2 id="初始衡量">初始衡量</h2><p>一般按攤銷後成本衡量的金融負債，初始通常按公允價值加減可直接歸屬交易成本；之後用有效利息法攤銷。</p>',
             '<h2 id="初始衡量">初始衡量</h2><p>不屬 FVTPL 的金融負債，初始衡量為公允價值並調整可直接歸屬於發行的交易成本；對發行公司債等負債而言，這類交易成本通常使初始帳面金額低於未扣成本前的收取對價，之後透過有效利率法攤銷。FVTPL 金融負債的交易成本則於發生時認列損益。</p>',
             'ch12 transaction costs'),
            ('<div class="summarybox" data-label="本章收尾"><p>公司債表格固定四欄：期初帳面 × 有效利率＝利息費用；面額 × 票面利率＝現金；差額＝溢折價攤銷；更新期末帳面。</p></div>',
             '<h2 id="2026 電子支付除列提醒">2026 電子支付除列提醒</h2><p>IFRS 9 自 2026 年起的修正釐清電子支付系統下金融資產與金融負債的除列時點，並在符合特定條件時提供一項會計政策選擇，使金融負債可在現金實際交付前視為已清償。一般公司債題若沒有這種特定電子支付情境，仍依通常除列規則處理，不要把例外擴張到所有付款。</p><div class="summarybox" data-label="本章收尾"><p>公司債表格固定四欄：期初帳面 × 有效利率＝利息費用；面額 × 票面利率＝現金；差額＝溢折價攤銷；更新期末帳面。</p></div>',
             'ch12 2026 electronic settlement')
        ])

        patch_html(root / 'chapters/ch17.html', [
            ('<h2 id="豁免">豁免</h2><p>短期租賃及低價值標的資產租賃可依政策選擇不採一般承租人資產負債認列模式，改將租賃給付按系統基礎認列費用。</p>',
             '<h2 id="豁免">豁免</h2><p>短期租賃是開始日租賃期間不超過 12 個月且不含購買選擇權的租賃；其認列豁免選擇按標的資產類別作成。低價值標的資產則以資產「全新時」的價值判斷，相關豁免可逐項租賃選擇。若採豁免，租賃給付通常按直線法或更能反映效益耗用型態的其他系統基礎認列費用。</p>',
             'ch17 exemptions'),
            ('<li><p>一年內的短期租賃是否一定要認列使用權資產？</p></li>',
             '<li><p>租賃期間為 12 個月但含購買選擇權，是否屬 IFRS 16 定義的短期租賃？</p></li>',
             'ch17 practice q4')
        ])

        patch_html(root / 'chapters/ch18.html', [
            ('<h2 id="衡量稅率">衡量稅率</h2><p>遞延所得稅以資產回收或負債清償時預期適用、且於報導日已制定或實質制定的稅率衡量。遞延所得稅資產與負債不折現。</p>',
             '<h2 id="衡量稅率">衡量稅率</h2><p>遞延所得稅以資產回收或負債清償時預期適用、且於報導日已制定或實質制定的稅率衡量。遞延所得稅資產與負債不折現。</p><h2 id="單一交易的初始認列豁免">單一交易的初始認列豁免</h2><p>IAS 12 自 2023 年起已收窄初始認列豁免：若一筆非企業合併交易在初始認列時同時產生等額的應課稅與可減除暫時性差異，豁免不再適用。租賃與除役義務是常見例子，因此不能再用舊版口訣一概說「初始認列所以不認列遞延所得稅」。</p>',
             'ch18 single transaction')
        ])

        patch_html(root / 'chapters/ch21.html', [
            ('<h2 id="IFRS 18 過渡提醒">IFRS 18 過渡提醒</h2><p>IFRS 18 同時修訂 IAS 7，對利息與股利現金流分類等規定帶來變動。2026 解舊題時仍應依題目指定準則與當期規範作答；新制題則依 IFRS 18 修訂後要求。</p>',
             '<h2 id="IFRS 18 過渡提醒">IFRS 18 過渡提醒</h2><p>IFRS 18 同時修訂 IAS 7。採間接法時，新制要求以 IFRS 18 的「營業損益」小計作為營業現金流調節起點；對沒有特定主要經營活動的企業，利息收入與股利收入原則列投資活動，利息支出與股利支付原則列籌資活動，移除舊制的部分分類選擇。具有特定主要經營活動的企業另依新制判斷。國際規範自 2027 年起生效；臺灣證券發行人相關規範自 2028 年起施行，因此 2026 舊題仍須依題目指定版本作答。</p>',
             'ch21 IFRS18 IAS7')
        ])

        patch_html(root / 'chapters/appendix-b.html', [
            ('<h2 id="ifrs18">IFRS 18 過渡</h2><p>IFRS 18 國際強制生效日為 2027 年 1 月 1 日起的年度報導期間。臺灣證券發行人相關財報規範已公告自 2028 年起施行。2026 年教材因此保留 IAS 1 現行考題架構，同時用明確的「過渡」標示 IFRS 18，不把兩套分類規則混寫。</p>',
             '<h2 id="2026-current-amendments">2026 現行修正提醒</h2><p>2026 年起生效的 IFRS 修正包含金融工具分類與衡量修正、Annual Improvements—Volume 11，以及與自然條件相依電力合約相關的 IFRS 9／IFRS 7 修正。本書只把與一般中會核心直接相關的 SPPI 與電子支付除列邊界納入正文；自然條件相依電力合約等高度專題仍列選讀，避免把專門議題誤當成每門中會都必考的核心。</p><h2 id="ifrs18">IFRS 18 過渡</h2><p>IFRS 18 國際強制生效日為 2027 年 1 月 1 日起的年度報導期間。臺灣證券發行人相關財報規範已公告自 2028 年起施行。2026 年教材因此保留 IAS 1 現行考題架構，同時用明確的「過渡」標示 IFRS 18，不把兩套分類規則混寫。</p>',
             'appendix b 2026 amendments')
        ])

        by_id = {q['id']: q for q in questions['items']}
        by_id['ch02-q02']['explanation'] = '除管理階層意圖外，還要看報導日是否存在可將清償遞延至少十二個月的實質權利；若有契約條款，須區分要求在報導日以前或以後遵守，後者不影響報導日分類但可能需要揭露。'
        by_id['ch04-q05']['explanation'] = '除短期、高度流動、可迅速轉換為已知金額及價值變動風險甚低外，還要看是否為支應短期現金承諾而持有；通常以自取得日起原始到期日約三個月內作為短期指標。'
        by_id['ch11-q04']['explanation'] = '指定權益 FVOCI 的累積公允價值變動不得重分類至損益，但可以在權益內移轉；股利通常進損益，除非明確代表收回部分投資成本。'
        by_id['ch17-q04']['question'] = '租賃期間為 12 個月但含購買選擇權，是否屬 IFRS 16 定義的短期租賃？'
        by_id['ch17-q04']['answer'] = '不屬於。'
        by_id['ch17-q04']['explanation'] = '短期租賃須在開始日租賃期間不超過 12 個月，且不能含購買選擇權。'

        manifest['version'] = NEW_VERSION
        manifest['updatedAt'] = '2026-07-29'
        notes = manifest.setdefault('releaseNotes', [])
        notes.insert(0, {
            'version': NEW_VERSION,
            'date': '2026-07-29',
            'title': '發布後二次內容審計與準則邊界修正',
            'changes': [
                '修正流動／非流動負債契約條款、約當現金、除役義務成本歸屬與權益 FVOCI 股利等準則邊界',
                '補入 2026 IFRS 9 修正、IFRS 16 短期／低價值豁免條件及 IAS 12 單一交易遞延所得稅修正',
                '明確化 IFRS 18 對 IAS 7 間接法起點與利息／股利現金流分類的過渡要求',
                '110 題 ID 與題數不變；同步精確化 3 題題解並改寫 1 題租賃判斷題',
            ],
            'progressImpact': '章節 ID、題目 ID 與題數不變；既有閱讀進度與錯題紀錄可沿用。',
        })
        questions['version'] = NEW_VERSION
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        questions_path.write_text(json.dumps(questions, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    else:
        if questions['version'] != NEW_VERSION:
            raise AssertionError('manifest/questions version drift in already-patched output')

    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    search = json.loads(search_path.read_text(encoding='utf-8'))
    chapter_markup = {c['id']: (root / c['file']).read_text(encoding='utf-8') for c in manifest['chapters']}
    for entry in search['entries']:
        entry['text'] = search_text(chapter_markup[entry['chapterId']])
    search_path.write_text(json.dumps(search, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    assert_v2_markers(root)
    qmap = {q['id']: q for q in json.loads(questions_path.read_text(encoding='utf-8'))['items']}
    assert qmap['ch17-q04']['answer'] == '不屬於。'
    assert '購買選擇權' in qmap['ch17-q04']['question']
    assert qmap['ch11-q04']['explanation'].startswith('指定權益 FVOCI')

    print(f'INTERMEDIATE_ACCOUNTING_V2_PATCHED version={NEW_VERSION} questions={len(qmap)} search={len(search["entries"])}')


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else '_site')
