#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

from civil_law_overview_v2_corrections import CHAPTERS, UPDATED_AT, VERSION
from civil_law_overview_questions_v2 import build_questions
from generate_civil_law_overview import chapter_html, appendix_b, search_entries

BOOK = 'civil-law-overview'


def dump(obj):
    return json.dumps(obj, ensure_ascii=False, indent=2) + '\n'


def next_library_version(version: str) -> str:
    m = re.fullmatch(r'(\d{4}\.\d{2}\.\d{2})-(\d+)', version)
    if not m:
        raise AssertionError(f'invalid library version: {version}')
    return f'{m.group(1)}-{int(m.group(2)) + 1}'


def appendix_a_v2() -> str:
    rows = [
        ('成年／未成年人', '民法 12、13', '18 歲成年；未滿 7 歲無行為能力；7 歲以上未成年人為限制行為能力。'),
        ('錯誤撤銷', '民法 90', '第 88、89 條撤銷權自意思表示後 1 年消滅。'),
        ('詐欺／脅迫撤銷', '民法 93', '發現詐欺或脅迫終止後 1 年；意思表示後逾 10 年不得撤銷。'),
        ('一般請求權時效', '民法 125', '原則 15 年；有較短特別期間者從其規定。'),
        ('單純請求中斷', '民法 129、130', '以請求中斷後，6 個月內不起訴，視為不中斷。'),
        ('定期給付', '民法 126', '利息、租金等各期請求權原則 5 年。'),
        ('侵權時效', '民法 197', '知悉損害及賠償義務人起 2 年；行為時起 10 年。'),
        ('動力車輛責任', '民法 191-2', '動力車輛使用中致人損害，駕駛人原則負責；能證明已盡相當注意者例外。'),
        ('約定利率上限', '民法 205', '週年利率超過 16% 的超過部分約定無效。'),
        ('物之瑕疵救濟', '民法 359、360、365', '解除／減價之外，保證品質欠缺或故意不告知瑕疵另可能請求不履行損害賠償；解除或減價權另有 6 個月／5 年期間。'),
        ('不動產物權法律行為', '民法 758', '書面＋登記；非經登記不生物權效力。'),
        ('動產善意取得', '民法 801、948', '先檢查善意受讓占有與無重大過失等要件，再判斷取得所有權效果。'),
        ('共有物處分／管理', '民法 819、820', '共有物整體處分、變更、設定負擔原則全體同意；一般管理另採法定多數決。'),
        ('結婚年齡／方式', '民法 980、982', '18 歲；書面＋二人以上證人簽名＋戶政登記。'),
        ('夫妻剩餘財產', '民法 1030-1', '法定財產制消滅時依婚後財產差額分配；繼承或其他無償取得、慰撫金不列入，法院並有調整權。'),
        ('裁判離婚', '民法 1052＋112 年憲判 4', '但書原則仍有效；修法期限 2025-03-24 屆滿未完成修法後，顯然過苛個案應依憲法判決意旨裁判。'),
        ('兩願離婚', '民法 1050', '書面＋二人以上證人簽名＋戶政登記。'),
        ('婚生否認', '民法 1063', '夫妻之一方或子女自知悉起 2 年；子女未成年時知悉者仍得成年後 2 年內提起。'),
        ('拋棄繼承', '民法 1174', '知悉得繼承起 3 個月內書面向法院；完成後原則另書面通知因拋棄而成為繼承人的人。'),
        ('遺囑能力', '民法 1186', '限制行為能力人無須法定代理人允許；未滿 16 歲不得為遺囑。'),
        ('特留分', '民法 1223', '現行：直系卑親屬、父母、配偶為應繼分 1/2；兄弟姊妹、祖父母為 1/3。2026-06-02 刪除兄弟姊妹特留分方案仍是草案。'),
    ]
    body = ''.join(
        f'<tr><td>{html.escape(a)}</td><td>{html.escape(b)}</td><td>{html.escape(c)}</td></tr>'
        for a, b, c in rows
    )
    return f'''<h1>附錄 A　高頻條文、年齡與期間速查</h1>
<p class="lead">本表依 2026-07-30 可查得現行法與憲法裁判整理。遇到修法新聞，先辨認「現行法、已公布未施行、草案」三種狀態。</p>
<div class="warningbox"><strong>未施行提醒：</strong>民法第 166-1 條施行日期仍待另定；不要把它當現行已生效的一般規則。</div>
<div class="warningbox"><strong>草案提醒：</strong>法務部 2026-06-02 預告刪除兄弟姊妹特留分的民法修正草案，截至本書基準日尚非現行法。</div>
<table><thead><tr><th>主題</th><th>核心依據</th><th>速查內容</th></tr></thead><tbody>{body}</tbody></table>
'''


def appendix_c_v2() -> str:
    pairs = [
        ('無效', '自始不生當事人所欲法律效果；仍要注意轉換、善意第三人等個別規定。'),
        ('得撤銷', '撤銷前有效；依法撤銷後原則視為自始無效。'),
        ('效力未定', '法律行為是否生效待有權人承認等後續事實確定。'),
        ('解除', '先檢查解除權成立與行使，再依第 259、260 條處理回復原狀及損害賠償；不要只背一句「契約消失」。'),
        ('債權', '特定人對特定人的相對請求。'),
        ('物權', '對特定物直接支配、具有排他與對世性的權利。'),
        ('消滅時效', '期間完成使義務人取得拒絕給付抗辯；單純請求中斷還有第 130 條 6 個月起訴限制。'),
        ('共有管理／處分', '第 820 條管理多數與第 819 條共有物整體處分全體同意是不同規則。'),
        ('善意受讓／所有權取得', '第 948 條看善意受讓占有要件，第 801 條接所有權取得效果。'),
        ('裁判離婚有責限制', '第 1052 條第 2 項但書沒有全面失效；但顯然過苛個案要同時適用 112 年憲判字第 4 號。'),
        ('應繼分', '依法定順位與配偶共同繼承規則計算的法定份額。'),
        ('特留分', '特定繼承人的最低保障份額；截至 2026-07-30 兄弟姊妹仍有應繼分 1/3 的特留分。'),
    ]
    rows = ''.join(f'<tr><td>{html.escape(a)}</td><td>{html.escape(b)}</td></tr>' for a, b in pairs)
    return f'''<h1>附錄 C　易混淆法律效果與現行法提醒</h1>
<p class="lead">第二次獨立內容複核把容易被新聞、舊教材或口訣帶偏的規則集中在這裡。</p>
<table><thead><tr><th>名詞／爭點</th><th>快速區分</th></tr></thead><tbody>{rows}</tbody></table>
<h2 id="現行法提醒">現行法提醒</h2>
<ul>
<li>成年年齡現為 18 歲；相關新制自 2023-01-01 施行。</li>
<li>民法第 166-1 條目前仍未施行。</li>
<li>112 年憲判字第 4 號的二年修法期限已於 2025-03-24 屆滿；未完成修法後，法院對判決所指顯然過苛個案應依其意旨裁判。</li>
<li>法務部 2026-06-02 預告刪除兄弟姊妹特留分，截至 2026-07-30 仍是草案；現行第 1223 條尚保留兄弟姊妹特留分。</li>
<li>相同性別二人婚姻須同時注意《司法院釋字第七四八號解釋施行法》。</li>
</ul>
'''


def main(site_root: str) -> str:
    site = Path(site_root)
    root = site / 'books' / BOOK
    if not root.is_dir():
        raise AssertionError(f'{BOOK} is not present in formal artifact')

    library_path = site / 'data' / 'library.json'
    library = json.loads(library_path.read_text(encoding='utf-8'))
    ids = [b['id'] for b in library['books']]
    if ids.count(BOOK) != 1:
        raise AssertionError(f'expected one {BOOK}, got {ids.count(BOOK)}')
    old_library_version = library['version']
    new_library_version = next_library_version(old_library_version)

    manifest_path = root / 'manifest.json'
    questions_path = root / 'questions.json'
    search_path = root / 'search.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    questions = json.loads(questions_path.read_text(encoding='utf-8'))

    expected_chapter_ids = [f'ch{i:02d}' for i in range(20)]
    actual_chapter_ids = [x['id'] for x in manifest['chapters'] if x.get('kind') == 'chapter']
    if actual_chapter_ids != expected_chapter_ids:
        raise AssertionError(f'civil chapter IDs drifted: {actual_chapter_ids}')

    for ch in CHAPTERS:
        path = root / 'chapters' / f"{ch['id']}.html"
        rendered = chapter_html(ch).replace('2026-07-29', UPDATED_AT)
        path.write_text(rendered, encoding='utf-8')
    (root / 'chapters' / 'appendix-a.html').write_text(appendix_a_v2(), encoding='utf-8')
    (root / 'chapters' / 'appendix-b.html').write_text(appendix_b(), encoding='utf-8')
    (root / 'chapters' / 'appendix-c.html').write_text(appendix_c_v2(), encoding='utf-8')

    raw = {x['id']: x for x in build_questions()}
    if set(raw) != {x['id'] for x in questions['items']}:
        raise AssertionError('civil question IDs drifted before v2 patch')
    for item in questions['items']:
        corrected = raw[item['id']]
        item['question'] = corrected['question']
        item['answer'] = corrected['answer']
        item['explanation'] = corrected['explanation']
    questions['version'] = VERSION
    questions['count'] = len(questions['items'])
    questions_path.write_text(dump(questions), encoding='utf-8')

    entries = search_entries(CHAPTERS)
    for entry in entries:
        if entry['chapterId'] == 'appendix-a':
            entry['text'] += ' 民法第130條請求後6個月起訴；第191-2條動力車輛；第819條共有物整體處分；第1030-1條剩餘財產；112年憲判字第4號；第1174條拋棄後通知；第1223條兄弟姊妹特留分現行法與2026-06-02草案。'
        elif entry['chapterId'] == 'appendix-c':
            entry['text'] += ' 第801條與第948條善意取得；第1052條但書未全面失效；2025-03-24修法期限屆滿；兄弟姊妹特留分草案尚未生效。'
    if len(entries) != 150:
        raise AssertionError(f'civil search count drift: {len(entries)}')
    search_path.write_text(dump({'entries': entries}), encoding='utf-8')

    manifest['version'] = VERSION
    manifest['updatedAt'] = UPDATED_AT
    release = {
        'version': VERSION,
        'date': UPDATED_AT,
        'title': '第二次獨立內容複核與糾錯',
        'changes': [
            '補正民法第 130 條單純請求中斷之 6 個月起訴限制',
            '補入債務承擔第 300、301 條、僱傭第 482 條、動力車輛第 191-2 條',
            '補正買賣瑕疵第 354、360 條、善意取得第 801、948 條與共有第 819、820 條分工',
            '補入 112 年憲判字第 4 號於 2025-03-24 修法期限屆滿後的裁判效果',
            '補正拋棄繼承後書面通知義務，並區分現行兄弟姊妹特留分與 2026-06-02 修法草案',
            '同步修正 9 題高風險題目與附錄速查',
        ],
        'progressImpact': '章節 ID、題目 ID、題數與進度儲存鍵均不變；既有閱讀與題庫進度可沿用。',
    }
    manifest['releaseNotes'] = [release] + [x for x in manifest.get('releaseNotes', []) if x.get('version') != VERSION]
    manifest_path.write_text(dump(manifest), encoding='utf-8')

    for book in library['books']:
        if book['id'] == BOOK and 'version' in book:
            book['version'] = VERSION
    library['version'] = new_library_version
    library_path.write_text(dump(library), encoding='utf-8')

    sw_path = site / 'sw.js'
    sw = sw_path.read_text(encoding='utf-8')
    sw, n = re.subn(
        r"const VERSION = 'study-library-[^']+';",
        f"const VERSION = 'study-library-{new_library_version}';",
        sw,
        count=1,
    )
    if n != 1:
        raise AssertionError('civil v2 could not bump service-worker version')
    sw_path.write_text(sw, encoding='utf-8')

    print(f'CIVIL_LAW_V2_PATCH_OK book={VERSION} library={old_library_version}->{new_library_version} questions=100 search=150')
    print(new_library_version)
    return new_library_version


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: python deploy/patch_civil_law_overview_v2.py SITE_ROOT')
    main(sys.argv[1])
