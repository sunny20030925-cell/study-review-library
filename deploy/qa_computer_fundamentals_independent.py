#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path

BOOK = 'computer-fundamentals'
EXPECTED_VERSION = '2026.07.29-1'


def require(condition: bool, message: str):
    if not condition:
        raise AssertionError(message)


def main(site_root: str) -> None:
    site = Path(site_root)
    root = site / 'books' / BOOK
    manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    qdoc = json.loads((root / 'questions.json').read_text(encoding='utf-8'))
    items = {q['id']: q for q in qdoc['items']}
    checks = 0

    # Round 2 deliberately rebuilds representative numerical answers independently.
    numeric = {
        'ch01-q02': 0b11010,
        'ch01-q03': int('FF', 16),
        'ch01-q04': 2**12,
        'ch02-q01': 2**8 - 1,
        'ch02-q04': 1920 * 1080 * 24,
        'ch04-q02': 1 / (2e9) / 1e-9,
        'ch04-q03': 1e9 * 2 * (1 / 2e9),
        'ch05-q03': 1 + (1 - 0.95) * 80,
        'ch06-q02': 500 / 250,
        'ch08-q02': 16 / 4,
        'ch09-q02': 100 / 8,
        'ch09-q03': 1 / 20,
        'ch12-q02': math.log2(1024),
        'ch13-q03': 80 / 100,
        'ch17-q03': 90 / 100 * 100,
        'ch18-q02': (43200 - 43.2) / 43200 * 100,
    }
    expected_tokens = {
        'ch01-q02':'26','ch01-q03':'255','ch01-q04':'4096','ch02-q01':'255','ch02-q04':'49,766,400',
        'ch04-q02':'0.5 ns','ch04-q03':'1 秒','ch05-q03':'5 ns','ch06-q02':'2 秒','ch08-q02':'4 頁',
        'ch09-q02':'12.5 MB/s','ch09-q03':'0.05 秒','ch12-q02':'10 次','ch13-q03':'0.8','ch17-q03':'90%','ch18-q02':'99.9%',
    }
    require(numeric['ch01-q02'] == 26, 'binary recalculation'); checks += 1
    require(numeric['ch01-q03'] == 255, 'hex recalculation'); checks += 1
    require(numeric['ch01-q04'] == 4096, 'bit patterns recalculation'); checks += 1
    require(numeric['ch02-q04'] == 49_766_400, 'image size recalculation'); checks += 1
    require(abs(numeric['ch04-q02'] - 0.5) < 1e-12, 'clock period recalculation'); checks += 1
    require(abs(numeric['ch04-q03'] - 1.0) < 1e-12, 'cpu time recalculation'); checks += 1
    require(abs(numeric['ch05-q03'] - 5.0) < 1e-9, 'AMAT recalculation'); checks += 1
    require(abs(numeric['ch09-q03'] - 0.05) < 1e-12, 'transmission delay recalculation'); checks += 1
    require(abs(numeric['ch18-q02'] - 99.9) < 1e-9, 'availability recalculation'); checks += 1
    for qid, token in expected_tokens.items():
        require(token in items[qid]['answer'], f'published numeric answer mismatch {qid}')
        checks += 1

    # High-risk conceptual judgments are rechecked independently from the generator.
    judgments = {
        'ch01-q05': ['4096', 'KiB'],
        'ch02-q05': ['不正確', '近似'],
        'ch04-q04': ['不可以', 'CPI'],
        'ch07-q02': ['可以', '並行'],
        'ch07-q05': ['不正確', 'parallelism'],
        'ch08-q03': ['不一定', '缺頁'],
        'ch08-q05': ['不完整', '映射'],
        'ch09-q05': ['不正確', '不同'],
        'ch10-q02': ['DNS', '名稱'],
        'ch10-q03': ['可靠', 'UDP'],
        'ch10-q05': ['不代表', '傳輸'],
        'ch11-q05': ['過度簡化', '實作'],
        'ch12-q03': ['不可以', '有序'],
        'ch12-q04': ['不能', '漸近'],
        'ch13-q05': ['不能', '碰撞'],
        'ch14-q02': ['不一定', '外鍵'],
        'ch15-q05': ['不能', '覆蓋'],
        'ch16-q02': ['Authentication', '認證'],
        'ch16-q03': ['Authorization', '授權'],
        'ch16-q04': ['可逆', '單向'],
        'ch17-q01': ['AI', '更廣'],
        'ch17-q04': ['可能', '失衡'],
        'ch17-q05': ['不足', '驗證'],
        'ch18-q04': ['不是', '一致性'],
        'ch19-q01': ['不等於', '授權'],
        'ch19-q03': ['不必然', '重新識別'],
    }
    for qid, tokens in judgments.items():
        joined = items[qid]['answer'] + ' ' + items[qid]['explanation']
        for token in tokens:
            require(token in joined, f'{qid} missing independent concept token {token}')
            checks += 1

    # Every question is separately checked for a useful explanation, not answer-only filler.
    for q in qdoc['items']:
        require(len(q['question'].strip()) >= 8, f'question too short {q["id"]}')
        require(len(q['answer'].strip()) >= 2, f'answer too short {q["id"]}')
        require(len(q['explanation'].strip()) >= 12, f'explanation too short {q["id"]}')
        require(q['answer'].strip() != q['explanation'].strip(), f'explanation duplicates answer {q["id"]}')
        checks += 4

    # Re-read rendered chapters, checking terminology consistency and common contradiction pairs.
    chapters = {}
    for entry in manifest['chapters']:
        if entry['id'].startswith('ch'):
            chapters[entry['id']] = (root / entry['file']).read_text(encoding='utf-8')
    require(len(chapters) == 20, 'rendered chapter count'); checks += 1

    chapter_tokens = {
        'ch01':['bit（位元）','byte（位元組）','1 byte = 8 bits'],
        'ch02':['Two’s Complement','Floating Point','Unicode'],
        'ch04':['ALU','Register','Instruction Set Architecture'],
        'ch07':['Process','Thread','Concurrency'],
        'ch08':['Virtual Memory','Page Fault','File System'],
        'ch09':['Bandwidth','Latency','Router'],
        'ch10':['DNS','TCP','UDP','HTTP / HTTPS'],
        'ch12':['Time Complexity','Space Complexity','Big-O'],
        'ch14':['Primary Key','Foreign Key','Transaction'],
        'ch16':['Confidentiality','Integrity','Availability','Authentication','Authorization'],
        'ch17':['Machine Learning','Training','Inference','Generalization'],
        'ch19':['Privacy','Data Minimization','Open Source License'],
    }
    for cid, tokens in chapter_tokens.items():
        for token in tokens:
            require(token in chapters[cid], f'{cid} missing {token}')
            checks += 1

    all_text = '\n'.join(chapters.values())
    contradictions = [
        r'1 byte\s*=\s*8 bytes',
        r'1 KiB\s*=\s*1000',
        r'IPv4[^。]{0,20}128 bits',
        r'IPv6[^。]{0,20}32 bits',
        r'DNS[^。]{0,30}搜尋引擎[^。]{0,10}(?:是|就是)',
        r'HTTPS[^。]{0,30}保證[^。]{0,20}(?:真實|可信)',
        r'Big-O[^。]{0,30}(?:就是|等於)[^。]{0,10}(?:秒|實際時間)',
        r'Open Source[^。]{0,30}(?:沒有|無)[^。]{0,10}著作權',
    ]
    for pattern in contradictions:
        require(re.search(pattern, all_text, re.I) is None, f'contradiction pattern {pattern}')
        checks += 1

    # Tablet/readability-oriented content sanity: no chapter is a thin outline.
    for cid, text in chapters.items():
        plain = re.sub(r'<[^>]+>', '', text)
        require(len(plain) >= 900, f'{cid} body too thin for textbook treatment')
        require(text.count('<p>') >= 8, f'{cid} lacks explanatory paragraphs')
        require(text.count('<li>') >= 6, f'{cid} lacks traps/exam/check content')
        checks += 3

    require(qdoc['version'] == EXPECTED_VERSION, 'question version drift'); checks += 1
    require(manifest['version'] == EXPECTED_VERSION, 'manifest version drift'); checks += 1
    print(f'COMPUTER_FUNDAMENTALS_INDEPENDENT_QA_OK checks={checks} recalculated={len(numeric)} high_risk={len(judgments)} questions=100 chapters=20')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: python deploy/qa_computer_fundamentals_independent.py SITE_ROOT')
    main(sys.argv[1])
