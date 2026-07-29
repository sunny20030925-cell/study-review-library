#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

BOOK = 'computer-fundamentals'
BOOK_VERSION = '2026.07.29-1'
EXPECTED_CHAPTERS = [f'ch{i:02d}' for i in range(20)]
EXPECTED_APPENDICES = ['appendix-a', 'appendix-b', 'appendix-c']
REQUIRED_SECTIONS = [
    '本章要解決的問題', '白話直覺', '正式定義與核心概念', '核心公式與成立條件',
    '完整標準例題', '常見錯誤', '考試判斷方法', '理解檢查',
]


def load_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def require(condition: bool, message: str):
    if not condition:
        raise AssertionError(message)


def main(site_root: str) -> None:
    site = Path(site_root)
    root = site / 'books' / BOOK
    manifest = load_json(root / 'manifest.json')
    questions = load_json(root / 'questions.json')
    search = load_json(root / 'search.json')
    library = load_json(site / 'data/library.json')
    checks = 0

    require(manifest['id'] == BOOK, 'manifest book id'); checks += 1
    require(manifest['version'] == BOOK_VERSION, 'manifest version'); checks += 1
    require(manifest['title'] == '計算機概論', 'manifest title'); checks += 1
    meta = manifest['chapters']
    require(len(meta) == 23, f'chapter metadata count={len(meta)}'); checks += 1
    require([x['id'] for x in meta[:20]] == EXPECTED_CHAPTERS, 'chapter id sequence'); checks += 1
    require([x['id'] for x in meta[20:]] == EXPECTED_APPENDICES, 'appendix id sequence'); checks += 1

    for item in meta:
        p = root / item['file']
        require(p.is_file(), f'missing chapter file {p}')
        require(p.stat().st_size > 700, f'chapter too small {p}')
        checks += 2
        text = p.read_text(encoding='utf-8')
        require('<h1>' in text, f'missing h1 {p}'); checks += 1
        if item['id'].startswith('ch'):
            for section in REQUIRED_SECTIONS:
                require(section in text, f'{item["id"]} missing {section}')
                checks += 1
            require('assets/computer-fundamentals-svg/' in text, f'{item["id"]} missing figure path'); checks += 1

    figures = sorted((site / 'assets/computer-fundamentals-svg').glob('*.svg'))
    require(len(figures) == 20, f'figure count={len(figures)}'); checks += 1
    for p in figures:
        require(p.stat().st_size > 300, f'figure too small {p}')
        text = p.read_text(encoding='utf-8')
        require('<title' in text and '<desc' in text, f'figure accessibility {p}')
        checks += 2

    require(questions['bookId'] == BOOK, 'questions book id'); checks += 1
    require(questions['version'] == BOOK_VERSION, 'questions version'); checks += 1
    items = questions['items']
    require(questions['count'] == 100 == len(items), f'question count={len(items)}'); checks += 1
    ids = [x['id'] for x in items]
    require(len(set(ids)) == 100, 'question ids not unique'); checks += 1
    counts = Counter(x['chapterId'] for x in items)
    require(counts == Counter({cid: 5 for cid in EXPECTED_CHAPTERS}), f'question distribution={counts}'); checks += 1
    for q in items:
        require(q['chapterId'] in EXPECTED_CHAPTERS, f'bad chapter in {q["id"]}')
        require(bool(q['question'].strip()) and bool(q['answer'].strip()) and bool(q['explanation'].strip()), f'empty q/a/explanation {q["id"]}')
        require(q['source'] == '本書自編標準題型', f'question source {q["id"]}')
        checks += 3

    entries = search['entries']
    require(len(entries) == 150, f'search count={len(entries)}'); checks += 1
    valid_ids = set(EXPECTED_CHAPTERS + EXPECTED_APPENDICES)
    for entry in entries:
        require(entry['chapterId'] in valid_ids, f'bad search chapter {entry}')
        require(bool(entry['title'].strip()) and bool(entry['text'].strip()), f'empty search entry {entry}')
        checks += 2

    by_qid = {q['id']: q for q in items}
    exact = {
        'ch01-q02': '26',
        'ch01-q03': '255',
        'ch01-q04': '4096',
        'ch02-q01': '255',
        'ch02-q04': '49,766,400',
        'ch04-q02': '0.5 ns',
        'ch04-q03': '1 秒',
        'ch05-q03': '5 ns',
        'ch06-q02': '2 秒',
        'ch07-q04': 't=6 ms',
        'ch08-q02': '4 頁',
        'ch09-q02': '12.5 MB/s',
        'ch09-q03': '0.05 秒',
        'ch12-q02': '10 次',
        'ch13-q03': '0.8',
        'ch17-q03': '90%',
        'ch18-q02': '99.9%',
    }
    for qid, token in exact.items():
        require(token in by_qid[qid]['answer'], f'numeric answer mismatch {qid}: {by_qid[qid]["answer"]}')
        checks += 1

    critical_text = '\n'.join((root / f'chapters/ch{i:02d}.html').read_text(encoding='utf-8') for i in range(20))
    critical_tokens = [
        '1 byte = 8 bits', '1 KiB = 1024', '−128', 'Floating Point', 'CPU time', 'AMAT',
        'Process', 'Thread', 'Virtual Memory', 'IPv4', 'IPv6', 'DNS', 'TCP', 'UDP', 'HTTPS',
        'Big-O', 'Primary Key', 'ACID', 'Regression Test', 'Authentication', 'Authorization',
        'KDF', 'Training', 'Inference', 'Cloud Computing', 'Data Minimization',
    ]
    for token in critical_tokens:
        require(token in critical_text, f'missing critical token {token}')
        checks += 1

    dangerous_patterns = [
        r'TCP[^。]{0,30}一定(?:比)?UDP慢',
        r'UDP[^。]{0,30}一定(?:比)?TCP快',
        r'HTTPS[^。]{0,40}一定(?:安全|可信|真實)',
        r'浮點數[^。]{0,30}精確表示所有實數',
        r'雜湊[^。]{0,20}就是加密',
        r'AI[^。]{0,40}保證(?:正確|真實)',
    ]
    for pattern in dangerous_patterns:
        require(re.search(pattern, critical_text) is None, f'unsafe overclaim pattern: {pattern}')
        checks += 1

    lib_ids = [b['id'] for b in library['books']]
    require(lib_ids.count(BOOK) == 1, 'library registration'); checks += 1
    expected_library = os.getenv('EXPECTED_LIBRARY_VERSION')
    if expected_library:
        require(library['version'] == expected_library, f'library version expected {expected_library}, got {library["version"]}')
        checks += 1
    pre_path = os.getenv('PRE_LIBRARY_JSON')
    if pre_path:
        pre = load_json(Path(pre_path))
        pre_ids = [b['id'] for b in pre['books']]
        require(lib_ids == pre_ids + [BOOK], f'book append drift pre={pre_ids} post={lib_ids}')
        checks += 1

    sw = (site / 'sw.js').read_text(encoding='utf-8')
    required_cache = [
        f'./books/{BOOK}/manifest.json', f'./books/{BOOK}/questions.json', f'./books/{BOOK}/search.json',
    ]
    required_cache += [f'./books/{BOOK}/chapters/ch{i:02d}.html' for i in range(20)]
    required_cache += [f'./books/{BOOK}/chapters/appendix-{x}.html' for x in ('a','b','c')]
    required_cache += [f'./assets/computer-fundamentals-svg/{c["slug"]}.svg' for c in __import__('computer_fundamentals_content_a').CHAPTERS_A + __import__('computer_fundamentals_content_b').CHAPTERS_B]
    for path in required_cache:
        require(path in sw, f'missing service-worker cache path {path}')
        checks += 1
    if expected_library:
        require(f"const VERSION = 'study-library-{expected_library}';" in sw, 'service worker version not finalized')
        checks += 1

    print(f'COMPUTER_FUNDAMENTALS_STRUCTURAL_QA_OK checks={checks} chapters=20 appendices=3 questions=100 search=150 figures=20')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: python deploy/validate_computer_fundamentals.py SITE_ROOT')
    main(sys.argv[1])
