#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
from collections import Counter
from pathlib import Path

BOOK = 'public-finance'
VERSION = '2026.07.29-1'
REQUIRED_PRE_IDS = {
    'calculus', 'accounting', 'economics', 'statistics', 'commercial-law',
    'cost-accounting', 'microeconomics', 'intermediate-accounting', 'macroeconomics',
}
checks = 0


def ck(cond, msg):
    global checks
    checks += 1
    if not cond:
        raise AssertionError(msg)


def main(arg):
    site = Path(arg)
    expected_library_version = os.environ.get('EXPECTED_LIBRARY_VERSION')
    pre_library_path = os.environ.get('PRE_LIBRARY_JSON')
    if not expected_library_version or not pre_library_path:
        raise SystemExit('EXPECTED_LIBRARY_VERSION and PRE_LIBRARY_JSON are required')

    pre = json.loads(Path(pre_library_path).read_text(encoding='utf-8'))
    lib = json.loads((site / 'data/library.json').read_text(encoding='utf-8'))
    pre_ids = [book['id'] for book in pre['books']]
    post_ids = [book['id'] for book in lib['books']]
    ck(REQUIRED_PRE_IDS.issubset(set(pre_ids)), f'missing prerequisite books: {pre_ids}')
    ck(BOOK not in pre_ids, 'public-finance already existed before generation')
    ck(post_ids == pre_ids + [BOOK], f'book order drift: before={pre_ids}, after={post_ids}')
    ck(lib['version'] == expected_library_version, 'library version')

    entry = lib['books'][-1]
    ck(entry['id'] == BOOK, 'library entry id')
    ck(entry.get('title') == '財政學', 'library entry title')
    ck('公共支出' in entry.get('subtitle','') and '租稅' in entry.get('subtitle',''), 'library entry subtitle')

    for existing_id in pre_ids:
        existing_root = site / 'books' / existing_id
        manifest = json.loads((existing_root / 'manifest.json').read_text(encoding='utf-8'))
        questions = json.loads((existing_root / 'questions.json').read_text(encoding='utf-8'))
        search = json.loads((existing_root / 'search.json').read_text(encoding='utf-8'))
        ck(manifest['id'] == existing_id, f'existing manifest id {existing_id}')
        ck(questions['count'] == len(questions['items']) > 0, f'existing questions {existing_id}')
        ck(bool(search['entries']), f'existing search {existing_id}')

    root = site / 'books' / BOOK
    manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    questions = json.loads((root / 'questions.json').read_text(encoding='utf-8'))
    search = json.loads((root / 'search.json').read_text(encoding='utf-8'))
    ck(manifest['id'] == BOOK, 'manifest id')
    ck(manifest['title'] == '財政學', 'manifest title')
    ck(manifest['version'] == questions['version'] == VERSION, 'book version')
    chapters = [x for x in manifest['chapters'] if x['kind'] == 'chapter']
    appendices = [x for x in manifest['chapters'] if x['kind'] == 'appendix']
    ck(len(chapters) == 20, 'chapter count')
    ck([x['id'] for x in chapters] == [f'ch{i:02d}' for i in range(20)], 'chapter ids')
    ck(len(appendices) == 3, 'appendix count')
    ck(questions['count'] == 100 == len(questions['items']), 'question count')
    ck(Counter(q['chapterId'] for q in questions['items']) == {f'ch{i:02d}': 5 for i in range(20)}, 'five questions each chapter')
    ck(len({q['id'] for q in questions['items']}) == 100, 'unique question ids')
    ck(len(search['entries']) == 189, f'search count {len(search["entries"])}')

    ids = {x['id'] for x in manifest['chapters']}
    for q in questions['items']:
        ck(q['chapterId'] in ids, f'question chapter {q["id"]}')
        for field in ('id','question','answer','explanation'):
            ck(bool(str(q.get(field,'')).strip()), f'question field {q["id"]} {field}')

    expected = {
        'ch00-q03':'NT$300 萬。', 'ch01-q03':'NT$200 萬。', 'ch02-q02':'NT$110。',
        'ch03-q03':'應提供。', 'ch04-q01':'NT$105。', 'ch04-q02':'NT$25。',
        'ch05-q01':'50。', 'ch05-q02':'第 4 位。', 'ch06-q01':'NT$100。',
        'ch06-q02':'約 NT$13.22 萬。', 'ch07-q01':'20%。', 'ch07-q02':'0。',
        'ch07-q05':'100%。', 'ch08-q02':'NT$20,000。', 'ch08-q03':'NT$10,000。',
        'ch08-q04':'60%。', 'ch09-q01':'NT$400。', 'ch09-q02':'NT$900。',
        'ch10-q02':'約 NT$4,132。', 'ch11-q01':'10%。', 'ch12-q01':'75%。',
        'ch12-q02':'約 NT$30。', 'ch12-q03':'約 NT$10。', 'ch13-q01':'NT$2,500。',
        'ch13-q02':'NT$10,000。', 'ch13-q03':'NT$180,000。', 'ch14-q01':'約 2 倍。',
        'ch15-q01':'50%。', 'ch15-q02':'50%。', 'ch15-q03':'NT$3,000。',
        'ch15-q04':'NT$10,000。', 'ch16-q01':'NT$10,000。', 'ch16-q02':'NT$20,000。',
        'ch17-q01':'NT$15,000。', 'ch17-q02':'NT$20,000。', 'ch18-q01':'NT$75。',
        'ch18-q02':'NT$60。', 'ch19-q01':'約 1 個 GDP 百分點。', 'ch19-q02':'約 1.2 個 GDP 百分點。',
        'ch19-q03':'約 1.2% GDP。',
    }
    qmap = {q['id']:q for q in questions['items']}
    for qid, ans in expected.items():
        ck(qmap[qid]['answer'] == ans, f'{qid}: {qmap[qid]["answer"]!r} != {ans!r}')

    text_all = []
    for ch in manifest['chapters']:
        path = root / ch['file']
        ck(path.is_file() and path.stat().st_size > 700, f'chapter file {ch["id"]}')
        text = path.read_text(encoding='utf-8')
        text_all.append(text)
        ck('\f' not in text and '\t' not in text, f'control chars {ch["id"]}')
        ck('<script' not in text.lower(), f'no inline script {ch["id"]}')
        if ch['kind'] == 'chapter':
            for token in ['白話直覺','正式定義與核心概念','核心公式與成立條件','完整標準例題','常見錯誤','考試判斷方法','理解檢查']:
                ck(token in text, f'{ch["id"]} missing {token}')

    full = '\n'.join(text_all)
    for token in [
        'Pareto', '社會福利函數', 'Samuelson', '搭便車', 'Pigouvian', 'Coase', '可交易許可',
        '中位數選民', '尋租', '淨現值', '影子價格', 'Lorenz', 'Gini', '逆選擇', '道德風險',
        'PAYG', '共同保險', '教育外部性', '平均稅率', '邊際稅率', '租稅歸宿', 'P_b-P_s=t',
        '超額負擔', 'DWL', 'Ramsey', '有效邊際稅率', 'EMTR', '公司所得稅', 'VAT', '稅負資本化',
        'Tiebout', '財政聯邦主義', '初級餘額', '\\Delta b\\approx(r-g)b-ps', '財政永續',
    ]:
        ck(token in full, f'missing core token {token}')

    for excluded in ['Mirrlees 最適所得稅模型的正式機制設計', 'Diamond–Mirrlees 生產效率定理的正式證明', 'DSGE']:
        ck(excluded not in '|'.join(ch['title'] for ch in chapters), f'advanced topic promoted to core chapter: {excluded}')
    for overclaim in [
        '政府介入必然改善', '法定納稅人就是最終經濟負擔者', '總剩餘增加代表每個人都變好',
        'r<g 時任何赤字都沒有成本', '生活必需品就應高稅',
    ]:
        ck(overclaim not in full, f'forbidden overclaim {overclaim}')
    ck('NT$' in full, 'TWD examples')
    ck('百分點' in full, 'percentage-point distinction')

    figures = sorted((site / 'assets/public-finance-svg').glob('*.svg'))
    ck(len(figures) == 20, 'figure count')
    for figure in figures:
        svg = figure.read_text(encoding='utf-8')
        ck('<title' in svg and '<desc' in svg and 'viewBox=' in svg, f'svg accessibility {figure.name}')
        ck('href="http' not in svg and "href='http" not in svg, f'no remote svg asset {figure.name}')

    for entry in search['entries']:
        ck(entry['chapterId'] in ids, 'search chapter id')
        ck(bool(entry['title'].strip()) and bool(entry['text'].strip()), 'search nonempty')
        ck(isinstance(entry['page'], int) and entry['page'] >= 0, 'search page')

    sw = (site / 'sw.js').read_text(encoding='utf-8')
    for token in [
        f"study-library-{expected_library_version}",
        './books/public-finance/manifest.json', './books/public-finance/questions.json', './books/public-finance/search.json',
        './books/public-finance/chapters/ch19.html', './books/public-finance/chapters/appendix-c.html',
        './assets/public-finance-svg/public-debt.svg',
    ]:
        ck(token in sw, f'sw cache {token}')

    raw = json.dumps({'manifest':manifest,'questions':questions,'search':search}, ensure_ascii=False)
    ck('macroeconomics' not in raw, 'template id leakage')
    ck(manifest.get('releaseNotes') and manifest['releaseNotes'][0]['version'] == VERSION, 'release notes')

    print(
        f'PUBLIC_FINANCE_QA_OK checks={checks} books={len(post_ids)} '
        f'library={expected_library_version} chapters=20 appendices=3 '
        f'questions=100 search=189 figures=20 numeric_rechecks={len(expected)}'
    )


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: python deploy/validate_public_finance.py SITE_ROOT')
    main(sys.argv[1])
