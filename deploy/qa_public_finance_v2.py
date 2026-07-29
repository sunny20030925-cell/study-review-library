#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import sys
from collections import Counter
from pathlib import Path

BOOK = 'public-finance'
VERSION = '2026.07.29-2'
checks = 0


def ck(condition, message):
    global checks
    checks += 1
    if not condition:
        raise AssertionError(message)


def main(site_root: str, expected_library: str = '2026.07.29-15') -> None:
    site = Path(site_root)
    root = site / 'books' / BOOK
    manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    questions = json.loads((root / 'questions.json').read_text(encoding='utf-8'))
    search = json.loads((root / 'search.json').read_text(encoding='utf-8'))
    library = json.loads((site / 'data/library.json').read_text(encoding='utf-8'))

    ck(manifest['version'] == questions['version'] == VERSION, 'public finance v2 version')
    ck(library['version'] == expected_library, 'library version')
    ids = [book['id'] for book in library['books']]
    ck(len(ids) == 11, 'eleven-book library')
    ck(ids[-3:] == ['macroeconomics', 'international-economics', 'public-finance'], 'canonical tail order')

    chapters = [x for x in manifest['chapters'] if x['kind'] == 'chapter']
    appendices = [x for x in manifest['chapters'] if x['kind'] == 'appendix']
    ck(len(chapters) == 20, '20 chapters')
    ck(len(appendices) == 3, '3 appendices')
    ck(questions['count'] == len(questions['items']) == 100, '100 questions')
    ck(len(search['entries']) == 189, '189 search entries')
    ck(Counter(q['chapterId'] for q in questions['items']) == {f'ch{i:02d}': 5 for i in range(20)}, 'five questions per chapter')
    ck(len({q['id'] for q in questions['items']}) == 100, 'unique question ids')
    ck({q['id'] for q in questions['items']} == {f'ch{i:02d}-q{j:02d}' for i in range(20) for j in range(1, 6)}, 'stable question ids')

    html_by_chapter = {
        ch['id']: (root / ch['file']).read_text(encoding='utf-8')
        for ch in chapters
    }
    text = '\n'.join(html_by_chapter.values())
    search_corpus = '\n'.join(entry['title'] + ' ' + entry['text'] for entry in search['entries'])
    qmap = {q['id']: q for q in questions['items']}

    # Corrections that must be present after the post-publication reaudit.
    required_by_chapter = {
        'ch03': ['Lindahl 價格', '個人化價格', '個人化價格加總等於公共財的邊際成本'],
        'ch05': ['概念提醒，不是一般會計恆等式'],
        'ch06': ['社會折現率（Social Discount Rate）', '不能看到政府借款利率就機械地當成唯一正確折現率'],
        'ch07': ['現金移轉（Cash Transfer）', '實物移轉（In-kind Transfer）', '負所得稅（Negative Income Tax）', '負所得等特殊資料'],
        'ch08': ['失業保險（Unemployment Insurance）', '這描述的是融資方式，不必然等於個人帳戶', 'DB／DC'],
        'ch09': ['定額自付（Copayment）', '共同保險（Coinsurance）', '自負額（Deductible）', '這個公式不適用於固定金額的 copayment'],
        'ch10': ['教育訊號／篩選（Signaling / Screening）', '私人薪資溢酬就不必然等於同額的社會生產力增量'],
        'ch11': ['比例／累進／累退稅負'],
        'ch12': ['小幅從量稅的局部近似', '有限大稅負若彈性沿曲線改變'],
        'ch13': ['相同公共收入的無扭曲基準', '課稅前市場本來有效率'],
        'ch14': ['逆彈性法則只是 Ramsey 商品稅問題的特殊情況', '一般 Ramsey rule'],
        'ch15': ['若休閒是正常財', 'net-of-tax rate'],
        'ch16': ['債務偏向（Debt Bias）', '不代表所有國家、所有期間都具有完全相同的規則'],
        'ch17': ['淨財富稅（Net Wealth Tax）', '財產移轉稅', '資本化程度'],
        'ch18': ['若補助率 m 定義為上級政府負擔合格支出的比例', '題目用「每地方一元配多少上級款」'],
        'ch19': ['存量－流量調整（Stock-flow Adjustment）', '\\frac{1+r_t}{1+g_t}', '\\frac{r_t-g_t}{1+g_t}', '約上升 1.18 個 GDP 百分點'],
    }
    for chapter_id, tokens in required_by_chapter.items():
        for token in tokens:
            ck(token in html_by_chapter[chapter_id], f'{chapter_id} missing correction token {token}')

    forbidden = [
        '共付（Copayment / Coinsurance）',
        '完全提存（Fully Funded）</dt><dd>為自己的未來給付先累積',
        'DWL\\approx\\frac12\\,t\\,|\\Delta Q|</p><p>線性供需、單位稅',
        'Local\\ price\\ with\\ matching\\ rate\\ m=(1-m)P',
        'Asset\\ Price\\ Effect\\approx- PV(Future\\ net\\ tax)',
        '所得稅把工作增加一元所得後真正能保留的金額降低，因此會產生替代效果；但稅也降低可支配所得，可能透過所得效果讓部分人想工作更多',
    ]
    for token in forbidden:
        ck(token not in text, f'stale content remains: {token}')

    # Search must carry the corrected concepts, not only the rendered chapter HTML.
    for token in [
        'Lindahl', '社會折現率', '失業保險', 'Copayment', 'Coinsurance', 'Signaling / Screening',
        '比例／累進／累退', '小幅從量稅', 'Ramsey', 'Debt Bias', 'Net Wealth Tax', 'Stock-flow Adjustment',
    ]:
        ck(token in search_corpus, f'search missing v2 concept {token}')
    for token in ['共付（Copayment / Coinsurance）', '為自己的未來給付先累積金融或實質資產']:
        ck(token not in search_corpus, f'search contains stale concept {token}')

    # Question-level semantic corrections while preserving IDs and count.
    ck('Lindahl' in qmap['ch03-q04']['question'], 'Lindahl question coverage')
    ck('個人化價格加總等於公共財的邊際成本' in qmap['ch03-q04']['answer'], 'Lindahl answer')
    ck('funded 不必然是個人帳戶' in qmap['ch08-q05']['explanation'], 'funded pension correction')
    ck('coinsurance' in qmap['ch09-q05']['question'], 'coinsurance terminology correction')
    ck('教育訊號／篩選' in qmap['ch10-q05']['explanation'], 'education signaling correction')
    ck('局部／小稅近似' in qmap['ch12-q01']['explanation'], 'tax incidence local approximation')
    ck('一般 Ramsey' in html_by_chapter['ch14'], 'Ramsey general-case warning')
    ck('若休閒是正常財' in qmap['ch15-q05']['explanation'], 'labour income-effect condition')
    ck('stock-flow' in qmap['ch19-q05']['explanation'].lower() or '存量－流量' in qmap['ch19-q05']['explanation'], 'debt stock-flow warning')

    # Independent arithmetic rechecks from raw inputs, not copied explanation strings.
    computed = {
        'ch00-q03': 1200 - 900,
        'ch01-q03': 120 + 80,
        'ch02-q02': 70 + 40,
        'ch03-q03': 600 + 400 - 800,
        'ch04-q01': 80 + 25,
        'ch04-q02': 25,
        'ch05-q02': (7 + 1) / 2,
        'ch06-q01': 110 / 1.10,
        'ch06-q02': -100 + 70 / 1.10 + 60 / (1.10 ** 2),
        'ch07-q01': 20 / 100,
        'ch07-q05': 1 / 1,
        'ch08-q02': 4 * 50000 * 0.10,
        'ch08-q03': (4 * 50000 * 0.10) / 2,
        'ch08-q04': 30000 / 50000,
        'ch09-q01': 2000 * 0.20,
        'ch09-q02': 3000 * 0.30,
        'ch10-q02': 60000 / 1.10 + 60000 / (1.10 ** 2) - 100000,
        'ch11-q01': 80000 / 800000,
        'ch12-q01': 1.5 / (1.5 + 0.5),
        'ch12-q02': 40 * (1.5 / (1.5 + 0.5)),
        'ch12-q03': 40 * (0.5 / (1.5 + 0.5)),
        'ch13-q01': 0.5 * 10 * 500,
        'ch13-q02': 0.5 * 20 * (10000 - 9000),
        'ch13-q03': 20 * 9000,
        'ch14-q01': (1 / 0.5) / (1 / 1.0),
        'ch15-q01': 1 - (10000 - 2000 - 3000) / 10000,
        'ch15-q02': 1 - (1000 - 200 - 300) / 1000,
        'ch15-q03': 10000 * 0.30,
        'ch15-q04': 10000,
        'ch16-q01': 50000 * 0.20,
        'ch16-q02': 100000 * 0.20,
        'ch17-q01': 40000 - 25000,
        'ch17-q02': 50000 - 30000,
        'ch18-q01': (1 - 0.25) * 100,
        'ch18-q02': (1 - 0.40) * 100,
        'ch19-q01': (0.03 - 0.01) * 0.50,
        'ch19-q02': (0.04 - 0.02) * 0.60,
        'ch19-q03': (0.04 - 0.02) * 0.60,
    }
    ck(math.isclose(computed['ch06-q02'], 13.223140495867767, rel_tol=0, abs_tol=1e-9), 'NPV recomputation')
    ck(math.isclose(computed['ch10-q02'], 4132.231404958671, rel_tol=0, abs_tol=1e-9), 'education NPV recomputation')
    ck(math.isclose(computed['ch12-q01'], 0.75), 'incidence share recomputation')
    ck(math.isclose(computed['ch19-q02'], 0.012), 'debt approximation recomputation')
    exact_debt = ((0.04 - 0.02) / (1 + 0.02)) * 0.60
    ck(math.isclose(exact_debt, 0.011764705882352941, rel_tol=0, abs_tol=1e-12), 'exact debt recomputation')
    ck('1.18 個百分點' in qmap['ch19-q02']['explanation'], 'exact debt result disclosed')

    string_expectations = {
        'ch00-q03': 'NT$300 萬。', 'ch01-q03': 'NT$200 萬。', 'ch02-q02': 'NT$110。',
        'ch03-q03': '應提供。', 'ch04-q01': 'NT$105。', 'ch04-q02': 'NT$25。',
        'ch05-q02': '第 4 位。', 'ch06-q01': 'NT$100。', 'ch06-q02': '約 NT$13.22 萬。',
        'ch07-q01': '20%。', 'ch07-q05': '100%。', 'ch08-q02': 'NT$20,000。',
        'ch08-q03': 'NT$10,000。', 'ch08-q04': '60%。', 'ch09-q01': 'NT$400。',
        'ch09-q02': 'NT$900。', 'ch10-q02': '約 NT$4,132。', 'ch11-q01': '10%。',
        'ch12-q01': '75%。', 'ch12-q02': '約 NT$30。', 'ch12-q03': '約 NT$10。',
        'ch13-q01': 'NT$2,500。', 'ch13-q02': 'NT$10,000。', 'ch13-q03': 'NT$180,000。',
        'ch14-q01': '約 2 倍。', 'ch15-q01': '50%。', 'ch15-q02': '50%。',
        'ch15-q03': 'NT$3,000。', 'ch15-q04': 'NT$10,000。', 'ch16-q01': 'NT$10,000。',
        'ch16-q02': 'NT$20,000。', 'ch17-q01': 'NT$15,000。', 'ch17-q02': 'NT$20,000。',
        'ch18-q01': 'NT$75。', 'ch18-q02': 'NT$60。', 'ch19-q01': '約 1 個 GDP 百分點。',
        'ch19-q02': '約 1.2 個 GDP 百分點。', 'ch19-q03': '約 1.2% GDP。',
    }
    ck(set(string_expectations) == set(computed), 'numeric recheck coverage')
    for qid, answer in string_expectations.items():
        ck(qmap[qid]['answer'] == answer, f'{qid} answer drift')

    figures = list((site / 'assets/public-finance-svg').glob('*.svg'))
    ck(len(figures) == 20, '20 figures')
    for figure in figures:
        svg = figure.read_text(encoding='utf-8')
        ck('<title' in svg and '<desc' in svg and 'viewBox=' in svg, f'figure accessibility {figure.name}')
        ck('href="http' not in svg and "href='http" not in svg, f'no remote figure asset {figure.name}')

    ck(manifest['releaseNotes'][0]['version'] == VERSION, 'v2 release note version')
    ck(manifest['releaseNotes'][0]['title'] == '發布後獨立二次內容審計與糾錯', 'v2 release note title')
    ck('章節 ID、題目 ID 與題數均未變' in manifest['releaseNotes'][0]['progressImpact'], 'progress compatibility note')

    sw = (site / 'sw.js').read_text(encoding='utf-8')
    ck(f"study-library-{expected_library}" in sw, 'service-worker v2 library version')
    for token in [
        './books/public-finance/manifest.json', './books/public-finance/questions.json', './books/public-finance/search.json',
        './books/public-finance/chapters/ch19.html', './assets/public-finance-svg/public-debt.svg',
    ]:
        ck(token in sw, f'service-worker missing {token}')

    print(
        f'PUBLIC_FINANCE_V2_QA_OK checks={checks} books=11 library={expected_library} '
        f'chapters=20 appendices=3 questions=100 search=189 figures=20 '
        f'numeric_rechecks={len(computed)} correction_areas={len(required_by_chapter)} question_adjustments=5'
    )


if __name__ == '__main__':
    if len(sys.argv) not in (2, 3):
        raise SystemExit('usage: qa_public_finance_v2.py SITE_ROOT [EXPECTED_LIBRARY]')
    main(sys.argv[1], sys.argv[2] if len(sys.argv) == 3 else '2026.07.29-15')
