#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

BOOK = 'computer-fundamentals'
BOOK_VERSION = '2026.07.29-1'
CHAPTER_IDS = [f'ch{i:02d}' for i in range(20)]
APPENDIX_IDS = ['appendix-a', 'appendix-b', 'appendix-c']
SECTIONS = [
    '本章要解決的問題', '白話直覺', '正式定義與核心概念', '核心公式與成立條件',
    '完整標準例題', '常見錯誤', '考試判斷方法', '理解檢查',
]


def load(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def main(site_root: str, expected_library_version: str) -> int:
    site = Path(site_root)
    root = site / 'books' / BOOK
    manifest = load(root / 'manifest.json')
    qdoc = load(root / 'questions.json')
    sdoc = load(root / 'search.json')
    library = load(site / 'data/library.json')
    checks = 0

    assert manifest['id'] == BOOK and manifest['version'] == BOOK_VERSION; checks += 1
    assert manifest['title'] == '計算機概論'; checks += 1
    assert library['version'] == expected_library_version; checks += 1
    meta = manifest['chapters']
    assert len(meta) == 23; checks += 1
    assert [x['id'] for x in meta[:20]] == CHAPTER_IDS; checks += 1
    assert [x['id'] for x in meta[20:]] == APPENDIX_IDS; checks += 1

    rendered = {}
    for item in meta:
        path = root / item['file']
        assert path.is_file() and path.stat().st_size > 700; checks += 1
        text = path.read_text(encoding='utf-8')
        assert '<h1>' in text; checks += 1
        if item['id'].startswith('ch'):
            rendered[item['id']] = text
            for section in SECTIONS:
                assert section in text; checks += 1
            assert 'assets/computer-fundamentals-svg/' in text; checks += 1

    figures = sorted((site / 'assets/computer-fundamentals-svg').glob('*.svg'))
    assert len(figures) == 20; checks += 1
    for figure in figures:
        svg = figure.read_text(encoding='utf-8')
        assert figure.stat().st_size > 300 and '<title' in svg and '<desc' in svg and 'viewBox' in svg; checks += 1

    items = qdoc['items']
    assert qdoc['bookId'] == BOOK and qdoc['version'] == BOOK_VERSION; checks += 1
    assert qdoc['count'] == len(items) == 100; checks += 1
    assert len({q['id'] for q in items}) == 100; checks += 1
    assert Counter(q['chapterId'] for q in items) == Counter({cid: 5 for cid in CHAPTER_IDS}); checks += 1
    for q in items:
        assert q['bookId'] == BOOK and q['chapterId'] in CHAPTER_IDS; checks += 1
        assert q['question'].strip() and q['answer'].strip() and q['explanation'].strip(); checks += 1
        assert q['source'] == '本書自編標準題型'; checks += 1

    entries = sdoc['entries']
    assert len(entries) == 150; checks += 1
    valid = set(CHAPTER_IDS + APPENDIX_IDS)
    for entry in entries:
        assert entry['chapterId'] in valid and entry['title'].strip() and entry['text'].strip(); checks += 1

    q = {x['id']: x for x in items}
    numeric_tokens = {
        'ch01-q02':'26','ch01-q03':'255','ch01-q04':'4096','ch02-q01':'255','ch02-q04':'49,766,400',
        'ch04-q02':'0.5 ns','ch04-q03':'1 秒','ch05-q03':'5 ns','ch06-q02':'2 秒','ch07-q04':'t=6 ms',
        'ch08-q02':'4 頁','ch09-q02':'12.5 MB/s','ch09-q03':'0.05 秒','ch12-q02':'10 次','ch13-q03':'0.8',
        'ch17-q03':'90%','ch18-q02':'99.9%',
    }
    for qid, token in numeric_tokens.items():
        assert token in q[qid]['answer'], (qid, q[qid]['answer']); checks += 1

    all_text = '\n'.join(rendered.values())
    safeguards = [
        '1 byte = 8 bits', '1 KiB = 1024', '二補數', '只能近似許多實數',
        '效能因素之一，但不是唯一因素', '單核心上，多個工作可快速交錯產生並行',
        '虛擬記憶體的概念比「用硬碟補 RAM」更廣', 'TCP 提供可靠、有序的位元組串流',
        'UDP 提供較精簡的資料報服務', '不代表 UDP 在任何情況都一定比較快',
        '不保證網站內容本身一定真實可信', 'Big-O 不是某次計時器結果',
        '加密是用金鑰可逆地保護內容；雜湊通常是單向映射',
        '生成式模型學習資料分布中的模式後產生新內容', '所以流暢不代表真實',
        '開源不等於沒有著作權',
    ]
    for token in safeguards:
        assert token in all_text, token; checks += 1

    forbidden_exact = [
        '1 byte = 8 bytes', '1 KiB = 1000 B', 'IPv4 為 128 bits', 'IPv6 為 32 bits',
        'DNS 是搜尋引擎', 'TCP 一定比 UDP 慢', 'UDP 一定比 TCP 快',
        '雜湊就是加密', '開源軟體沒有著作權',
    ]
    for token in forbidden_exact:
        assert token not in all_text, token; checks += 1

    sw = (site / 'sw.js').read_text(encoding='utf-8')
    assert f"const VERSION = 'study-library-{expected_library_version}';" in sw; checks += 1
    required_cache = [
        f'./books/{BOOK}/manifest.json', f'./books/{BOOK}/questions.json', f'./books/{BOOK}/search.json',
        './books/computer-fundamentals/chapters/ch00.html', './books/computer-fundamentals/chapters/ch19.html',
        './books/computer-fundamentals/chapters/appendix-c.html',
    ]
    for token in required_cache:
        assert token in sw, token; checks += 1

    print(f'COMPUTER_FUNDAMENTALS_RELEASE_QA_ROUND1_OK checks={checks} chapters=20 appendices=3 questions=100 search=150 figures=20')
    return checks


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('usage: python deploy/validate_computer_fundamentals_release.py SITE_ROOT EXPECTED_LIBRARY_VERSION')
    main(sys.argv[1], sys.argv[2])
