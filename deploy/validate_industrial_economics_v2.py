#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import re
import sys
from collections import Counter
from pathlib import Path

BOOK = 'industrial-economics'
VERSION = '2026.07.30-2'


def main(site_root: str, expected_library: str) -> int:
    site = Path(site_root)
    root = site / 'books' / BOOK
    manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    questions = json.loads((root / 'questions.json').read_text(encoding='utf-8'))
    search = json.loads((root / 'search.json').read_text(encoding='utf-8'))
    library = json.loads((site / 'data/library.json').read_text(encoding='utf-8'))
    checks = 0

    def ck(cond, msg):
        nonlocal checks
        checks += 1
        if not cond:
            raise AssertionError(msg)

    ck(manifest['id'] == BOOK, 'manifest id')
    ck(manifest['version'] == VERSION, 'manifest version')
    ck(questions['bookId'] == BOOK, 'question book id')
    ck(questions['version'] == VERSION, 'question version')
    ck(library['version'] == expected_library, 'library version')
    ids = [b['id'] for b in library['books']]
    ck(ids.count(BOOK) == 1, 'single industrial economics book')

    chapters = [x for x in manifest['chapters'] if x['kind'] == 'chapter']
    appendices = [x for x in manifest['chapters'] if x['kind'] == 'appendix']
    ck(len(chapters) == 20, 'chapter count')
    ck([x['id'] for x in chapters] == [f'ch{i:02d}' for i in range(20)], 'chapter ids')
    ck(len(appendices) == 3, 'appendix count')
    ck([x['id'] for x in appendices] == ['appendix-a', 'appendix-b', 'appendix-c'], 'appendix ids')
    ck(questions['count'] == len(questions['items']) == 100, 'question count')
    ck([x['id'] for x in questions['items']] == [f'ch{i:02d}-q{j:02d}' for i in range(20) for j in range(1, 6)], 'question ids')
    ck(Counter(x['chapterId'] for x in questions['items']) == {f'ch{i:02d}': 5 for i in range(20)}, 'five questions each')
    ck(len(search['entries']) == 150, 'search count')

    html_docs = []
    for meta in manifest['chapters']:
        p = root / meta['file']
        ck(p.is_file(), f'missing {meta["file"]}')
        text = p.read_text(encoding='utf-8')
        html_docs.append(text)
        ck('<script' not in text.lower(), f'inline script {meta["id"]}')
        ck('href="http' not in text and "href='http" not in text, f'remote link {meta["id"]}')
        ck('<h1>' in text, f'h1 {meta["id"]}')

    figs = sorted((site / 'assets/industrial-economics-svg').glob('*.svg'))
    ck(len(figs) == 20, 'figure count')
    for p in figs:
        text = p.read_text(encoding='utf-8')
        ck('<title' in text and '<desc' in text and 'viewBox=' in text, f'figure accessibility {p.name}')
        ck('href="http' not in text and "href='http" not in text, f'figure remote {p.name}')

    plain = html.unescape(re.sub(r'<[^>]+>', ' ', '\n'.join(html_docs)))
    qtext = '\n'.join(x['question'] + ' ' + x['answer'] + ' ' + x['explanation'] for x in questions['items'])
    search_text = '\n'.join(x['title'] + ' ' + x['text'] for x in search['entries'])
    corpus = plain + '\n' + qtext + '\n' + search_text

    corrected_tokens = [
        '自然獨占（Natural Monopoly）',
        '次可加性（subadditivity）',
        '|epsilon|>1',
        '總產量是否增加是重要線索，但不是唯一判準',
        'q_i = (a-c-b Q_-i)/(2b)',
        '全市場覆蓋',
        'sum_t [pi_t/(1+r)^t] >= F_sunk',
        '不能把「每期利潤」直接與一次性進入成本相比',
        '互動更頻繁有時能加快偵測',
        '合意可依市場狀況、商品特性、成本與利潤、行為經濟合理性等相當依據推定',
        '公平交易法第 19 條原則禁止限制轉售價格，但有正當理由者例外',
        'Effective transaction cost = posted price + search/attention cost',
        '價格「結構」而不只是兩側價格總和',
        '公平交易法第 7 條所稱獨占',
        '沒有直接協議證據',
    ]
    for token in corrected_tokens:
        ck(token in corpus, f'missing v2 correction {token}')

    stale_tokens = [
        'q_i = (a-c-Q_-i)/(2b)',
        'Observed price = product price + search/attention cost',
        '福利題一定檢查總產量是否改變',
    ]
    for token in stale_tokens:
        ck(token not in corpus, f'stale v1 text {token}')

    qmap = {x['id']: x for x in questions['items']}
    required_q = {
        'ch02-q05': ('次可加性',),
        'ch03-q05': ('|epsilon|>1',),
        'ch04-q05': ('不能', '配置'),
        'ch06-q03': ('q_i=15', 'b≠1'),
        'ch09-q05': ('不可以', '[0,1]'),
        'ch11-q05': ('現值',),
        'ch12-q05': ('不一定', '第 14 條'),
        'ch13-q05': ('不能', '第 19 條'),
        'ch18-q04': ('兩個推論都不可以直接成立', '推定合意'),
    }
    for qid, tokens in required_q.items():
        joined = qmap[qid]['answer'] + ' ' + qmap[qid]['explanation']
        for token in tokens:
            ck(token in joined, f'{qid} token {token}')

    ck(manifest['releaseNotes'][0]['version'] == VERSION, 'v2 release note version')
    ck(manifest['releaseNotes'][0]['title'] == '第二次獨立內容複核與糾錯', 'v2 release note title')
    ck('Book ID、20 個章節 ID、3 個附錄 ID、100 個題目 ID 均未變' in manifest['releaseNotes'][0]['progressImpact'], 'progress preservation note')

    sw = (site / 'sw.js').read_text(encoding='utf-8')
    ck(f'study-library-{expected_library}' in sw, 'service worker version')
    ck('./books/industrial-economics/manifest.json' in sw, 'service worker manifest')
    ck('./books/industrial-economics/questions.json' in sw, 'service worker questions')

    print(
        f'INDUSTRIAL_ECONOMICS_V2_QA1_OK checks={checks} books={len(ids)} '
        f'library={expected_library} chapters=20 appendices=3 questions=100 search=150 figures=20 '
        f'correction_areas=12'
    )
    return checks


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('usage: validate_industrial_economics_v2.py SITE_ROOT EXPECTED_LIBRARY')
    main(sys.argv[1], sys.argv[2])
