#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path

BOOK = 'computer-fundamentals'
BOOK_VERSION = '2026.07.29-1'


def main(site_root: str, expected_library_version: str) -> int:
    site = Path(site_root)
    root = site / 'books' / BOOK
    manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    qdoc = json.loads((root / 'questions.json').read_text(encoding='utf-8'))
    library = json.loads((site / 'data/library.json').read_text(encoding='utf-8'))
    by_id = {q['id']: q for q in qdoc['items']}
    checks = 0

    # Independent numerical reconstruction; these expressions do not reuse generator constants.
    recalculated = {
        'ch01-q02': 0b11010,
        'ch01-q03': int('FF', 16),
        'ch01-q04': 2 ** 12,
        'ch02-q01': 2 ** 8 - 1,
        'ch02-q04': 1920 * 1080 * 24,
        'ch04-q02': 1 / (2e9) / 1e-9,
        'ch04-q03': 1e9 * 2 * (1 / 2e9),
        'ch05-q03': 1 + 0.05 * 80,
        'ch06-q02': 500 / 250,
        'ch07-q04': 4 + 2,
        'ch08-q02': 16 / 4,
        'ch09-q02': 100 / 8,
        'ch09-q03': 1 / 20,
        'ch12-q02': math.log2(1024),
        'ch13-q03': 80 / 100,
        'ch17-q03': 90 / 100 * 100,
        'ch18-q02': (43200 - 43.2) / 43200 * 100,
    }
    expectations = {
        'ch01-q02': (26, '26'), 'ch01-q03': (255, '255'), 'ch01-q04': (4096, '4096'),
        'ch02-q01': (255, '255'), 'ch02-q04': (49_766_400, '49,766,400'),
        'ch04-q02': (0.5, '0.5 ns'), 'ch04-q03': (1.0, '1 秒'), 'ch05-q03': (5.0, '5 ns'),
        'ch06-q02': (2.0, '2 秒'), 'ch07-q04': (6, 't=6 ms'), 'ch08-q02': (4.0, '4 頁'),
        'ch09-q02': (12.5, '12.5 MB/s'), 'ch09-q03': (0.05, '0.05 秒'), 'ch12-q02': (10.0, '10 次'),
        'ch13-q03': (0.8, '0.8'), 'ch17-q03': (90.0, '90%'), 'ch18-q02': (99.9, '99.9%'),
    }
    for qid, (expected, token) in expectations.items():
        value = recalculated[qid]
        assert math.isclose(float(value), float(expected), rel_tol=1e-12, abs_tol=1e-12), (qid, value, expected)
        assert token in by_id[qid]['answer'], (qid, by_id[qid]['answer'])
        checks += 2

    high_risk = {
        'ch01-q05': ('4096', 'KiB'),
        'ch02-q05': ('不正確', '近似'),
        'ch04-q04': ('不可以', 'CPI'),
        'ch07-q02': ('可以', '並行'),
        'ch07-q05': ('不正確', 'parallelism'),
        'ch08-q03': ('不一定', '缺頁'),
        'ch08-q05': ('不完整', '映射'),
        'ch09-q05': ('不正確', '不同'),
        'ch10-q02': ('DNS', '名稱'),
        'ch10-q03': ('可靠', 'UDP'),
        'ch10-q05': ('不代表', '傳輸'),
        'ch11-q05': ('是。', '語言規格', '實作'),
        'ch12-q03': ('不可以', '有序'),
        'ch12-q04': ('不能', '漸近'),
        'ch13-q05': ('不能', '碰撞'),
        'ch14-q02': ('不一定', '外鍵'),
        'ch15-q05': ('不能', '覆蓋'),
        'ch16-q02': ('Authentication', '認證'),
        'ch16-q03': ('Authorization', '授權'),
        'ch16-q04': ('可逆', '單向'),
        'ch17-q01': ('AI', '更廣'),
        'ch17-q04': ('可能', '失衡'),
        'ch17-q05': ('不足', '驗證'),
        'ch18-q04': ('不是', '一致性'),
        'ch19-q01': ('不等於', '授權'),
        'ch19-q03': ('不必然', '重新識別'),
    }
    for qid, tokens in high_risk.items():
        text = by_id[qid]['answer'] + ' ' + by_id[qid]['explanation']
        for token in tokens:
            assert token in text, (qid, token, text)
            checks += 1

    # All questions must remain reusable study items with explanations, not answer stubs.
    assert len(qdoc['items']) == 100; checks += 1
    for q in qdoc['items']:
        assert len(q['question'].strip()) >= 8; checks += 1
        assert len(q['answer'].strip()) >= 2; checks += 1
        assert len(q['explanation'].strip()) >= 12; checks += 1
        assert q['answer'].strip() != q['explanation'].strip(); checks += 1

    chapters = {}
    for entry in manifest['chapters']:
        if entry['id'].startswith('ch'):
            text = (root / entry['file']).read_text(encoding='utf-8')
            chapters[entry['id']] = text
            plain = re.sub(r'<[^>]+>', '', text)
            assert len(plain) >= 900, entry['id']; checks += 1
            assert text.count('<p>') >= 8, entry['id']; checks += 1
            assert text.count('<li>') >= 6, entry['id']; checks += 1
    assert len(chapters) == 20; checks += 1

    concept_map = {
        'ch01': ('bit（位元）', 'byte（位元組）', 'Hexadecimal'),
        'ch02': ('Two’s Complement', 'Floating Point', 'Unicode'),
        'ch04': ('ALU', 'Register', 'Instruction Set Architecture'),
        'ch07': ('Process', 'Thread', 'Context Switch'),
        'ch08': ('Virtual Memory', 'Page Fault', 'File System'),
        'ch09': ('Bandwidth', 'Latency', 'Router'),
        'ch10': ('DNS', 'TCP', 'UDP', 'HTTP / HTTPS'),
        'ch12': ('Time Complexity', 'Space Complexity', 'Big-O'),
        'ch14': ('Primary Key', 'Foreign Key', 'ACID'),
        'ch16': ('Confidentiality', 'Integrity', 'Availability', 'Authentication', 'Authorization'),
        'ch17': ('Machine Learning', 'Training', 'Inference', 'Generalization'),
        'ch19': ('Privacy', 'Data Minimization', 'Open Source License'),
    }
    for cid, tokens in concept_map.items():
        for token in tokens:
            assert token in chapters[cid], (cid, token)
            checks += 1

    explicit_boundaries = [
        'CPU 時脈較高不等於任何工作一定較快',
        '並行（concurrency）不必然同時執行',
        'HTTPS 是 HTTP 在 TLS 保護下傳輸',
        '不等於「網站內容一定可信」',
        'Big-O 描述漸近成長上界／等級',
        '雜湊（hashing）與加密（encryption）不是同一件事',
        'AI 模型輸出是推論結果，不保證真實、完整或無偏',
    ]
    # Some boundary wording lives in scope rather than rendered chapters; verify the source scope independently.
    scope = Path('docs/books/computer-fundamentals/scope.md').read_text(encoding='utf-8')
    for token in explicit_boundaries:
        assert token in scope, token
        checks += 1

    assert manifest['version'] == qdoc['version'] == BOOK_VERSION; checks += 1
    assert library['version'] == expected_library_version; checks += 1
    assert [b['id'] for b in library['books']][-1] == BOOK; checks += 1
    print(f'COMPUTER_FUNDAMENTALS_RELEASE_QA_ROUND2_OK checks={checks} numeric_rechecks={len(recalculated)} high_risk={len(high_risk)} questions=100 chapters=20')
    return checks


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('usage: python deploy/qa_computer_fundamentals_release.py SITE_ROOT EXPECTED_LIBRARY_VERSION')
    main(sys.argv[1], sys.argv[2])
