#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import re
import sys
from collections import Counter
from pathlib import Path

from econometrics_v2_corrections import VERSION

BOOK = 'econometrics'
EXPECTED_IDS = [f'ch{i:02d}-q{j:02d}' for i in range(20) for j in range(1, 6)]


def visible(raw: str) -> str:
    return html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', raw))).strip()


def main(site_root: str, expected_library_version: str | None = None) -> None:
    site = Path(site_root)
    root = site / 'books' / BOOK
    manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    qtop = json.loads((root / 'questions.json').read_text(encoding='utf-8'))
    search = json.loads((root / 'search.json').read_text(encoding='utf-8'))
    library = json.loads((site / 'data/library.json').read_text(encoding='utf-8'))
    checks = 0

    def C(condition: bool, message: str) -> None:
        nonlocal checks
        if not condition:
            raise AssertionError(message)
        checks += 1

    C(manifest['id'] == BOOK, 'manifest id')
    C(manifest['version'] == VERSION, 'manifest version')
    C(qtop['bookId'] == BOOK, 'question book id')
    C(qtop['version'] == VERSION, 'question version')
    C(qtop['count'] == 100, 'question count top')
    C(len(qtop['items']) == 100, 'question item count')
    C([q['id'] for q in qtop['items']] == EXPECTED_IDS, 'question IDs/order preserved')
    C(Counter(q['chapterId'] for q in qtop['items']) == {f'ch{i:02d}': 5 for i in range(20)}, 'five questions per chapter')
    C(len(search['entries']) == 189, 'search count')
    chapters = [m for m in manifest['chapters'] if m['kind'] == 'chapter']
    appendices = [m for m in manifest['chapters'] if m['kind'] == 'appendix']
    C([m['id'] for m in chapters] == [f'ch{i:02d}' for i in range(20)], 'chapter IDs preserved')
    C([m['id'] for m in appendices] == ['appendix-a', 'appendix-b', 'appendix-c'], 'appendix IDs preserved')
    C(len(list((site / 'assets/econometrics-svg').glob('*.svg'))) == 20, '20 SVG preserved')

    ids = [b['id'] for b in library['books']]
    C(ids.count(BOOK) == 1, 'single econometrics registry entry')
    C('industrial-economics' in ids, 'industrial economics remains present')
    C(ids.index(BOOK) < ids.index('industrial-economics'), 'registry order preserved')
    if expected_library_version:
        C(library['version'] == expected_library_version, 'expected library version')
    C(f"study-library-{library['version']}" in (site / 'sw.js').read_text(encoding='utf-8'), 'service worker version')

    chapter_text = {
        m['id']: visible((root / m['file']).read_text(encoding='utf-8'))
        for m in chapters
    }
    ch13 = chapter_text['ch13']
    ch15 = chapter_text['ch15']

    # Panel-data precision gate: FE/FD cannot be taught as sufficient by themselves.
    for token in (
        'strict exogeneity',
        '整段 X 歷史',
        'idiosyncratic error',
        'time-varying confounder',
        '落後依變數',
        '不等於 X 自動外生',
    ):
        C(token.casefold() in ch13.casefold(), f'ch13 precision token {token}')
    C('E(u_{it}\\mid x_{i1},\\ldots,x_{iT},\\alpha_i)=0' in (root / next(m['file'] for m in chapters if m['id'] == 'ch13')).read_text(encoding='utf-8'), 'strict exogeneity formula')

    # Randomized-experiment precision gate: random assignment != population sampling.
    for token in (
        'SATE',
        'PATE',
        '代表性抽樣',
        '外部效度',
        '不能只靠 random assignment',
        '實驗單位',
    ):
        C(token.casefold() in ch15.casefold(), f'ch15 precision token {token}')

    qmap = {q['id']: q for q in qtop['items']}
    q13 = qmap['ch13-q04']['answer'] + ' ' + qmap['ch13-q04']['explanation']
    for token in ('不能', 'strict exogeneity', 'time-varying confounder'):
        C(token.casefold() in q13.casefold(), f'ch13-q04 gate {token}')

    q15 = qmap['ch15-q02']['answer'] + ' ' + qmap['ch15-q02']['explanation']
    for token in ('不能', 'SATE', 'PATE', '代表性', '外部效度'):
        C(token.casefold() in q15.casefold(), f'ch15-q02 gate {token}')
    C('SATE' in qmap['ch15-q03']['explanation'] and 'PATE' in qmap['ch15-q03']['explanation'], 'ch15-q03 sample/population distinction')

    # Negative gates against the two audited overclaims.
    combined = ch13 + '\n' + ch15 + '\n' + '\n'.join(q['answer'] + ' ' + q['explanation'] for q in qtop['items'])
    C('FE 消掉 alpha_i，所以不需要任何外生性條件' not in combined, 'no FE sufficiency overclaim')
    C('random assignment 自動保證母體代表性' not in combined, 'no random-assignment external-validity overclaim')

    # Existing structure and high-risk content remain intact around the corrections.
    required = {
        'ch03': ('Zero conditional mean', 'Gauss–Markov'),
        'ch08': ('heteroskedasticity-robust', 'WLS'),
        'ch10': ('Linear Probability Model', 'Logit'),
        'ch12': ('HAC', 'AR(1)'),
        'ch14': ('relevance', 'exclusion'),
        'ch16': ('parallel trends', 'cluster'),
        'ch17': ('Fuzzy RDD', 'local effect'),
        'ch18': ('Test set', 'Overfitting'),
    }
    for cid, tokens in required.items():
        for token in tokens:
            C(token.casefold() in chapter_text[cid].casefold(), f'{cid} preserved concept {token}')

    print(
        f'ECONOMETRICS_REAUDIT_V2_OK checks={checks} chapters=20 appendices=3 '
        f'questions=100 search=189 figures=20 corrections=2 ids_preserved=true'
    )


if __name__ == '__main__':
    if len(sys.argv) not in (2, 3):
        raise SystemExit('usage: python deploy/qa_econometrics_reaudit_v2.py SITE_ROOT [EXPECTED_LIBRARY_VERSION]')
    main(sys.argv[1], sys.argv[2] if len(sys.argv) == 3 else None)
