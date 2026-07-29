#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

from econometrics_v3_corrections import VERSION

BOOK = 'econometrics'
EXPECTED_IDS = [f'ch{i:02d}-q{j:02d}' for i in range(20) for j in range(1, 6)]


def visible(raw: str) -> str:
    return html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', raw))).strip()


def close(a: float, b: float, tol: float = 1e-9) -> bool:
    return abs(a - b) <= tol


def main(site_root: str, expected_library_version: str | None = None) -> None:
    site = Path(site_root)
    root = site / 'books' / BOOK
    manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    qtop = json.loads((root / 'questions.json').read_text(encoding='utf-8'))
    search = json.loads((root / 'search.json').read_text(encoding='utf-8'))
    library = json.loads((site / 'data/library.json').read_text(encoding='utf-8'))
    chapters_meta = [m for m in manifest['chapters'] if m['kind'] == 'chapter']
    appendices_meta = [m for m in manifest['chapters'] if m['kind'] == 'appendix']
    raw_chapters = {m['id']: (root / m['file']).read_text(encoding='utf-8') for m in chapters_meta}
    chapters = {cid: visible(raw) for cid, raw in raw_chapters.items()}
    appendices = {m['id']: visible((root / m['file']).read_text(encoding='utf-8')) for m in appendices_meta}
    questions = qtop['items']
    qmap = {q['id']: q for q in questions}
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
    C([m['id'] for m in chapters_meta] == [f'ch{i:02d}' for i in range(20)], 'chapter IDs/order preserved')
    C([m['id'] for m in appendices_meta] == ['appendix-a', 'appendix-b', 'appendix-c'], 'appendix IDs/order preserved')
    C(qtop['count'] == len(questions) == 100, '100 questions')
    C([q['id'] for q in questions] == EXPECTED_IDS, 'question IDs/order preserved')
    C(Counter(q['chapterId'] for q in questions) == {f'ch{i:02d}': 5 for i in range(20)}, 'five questions per chapter')
    C(len(search['entries']) == 189, '189 search entries')
    C(len(list((site / 'assets/econometrics-svg').glob('*.svg'))) == 20, '20 SVG files')
    C(len({q['id'] for q in questions}) == 100, 'unique question IDs')
    C(len({(e['chapterId'], e['page'], e['title']) for e in search['entries']}) == 189, 'unique search entries')

    for q in questions:
        C(bool(q['question'].strip()), f'{q["id"]} question nonempty')
        C(bool(q['answer'].strip()), f'{q["id"]} answer nonempty')
        C(bool(q['explanation'].strip()), f'{q["id"]} explanation nonempty')
        C(q['bookId'] == BOOK, f'{q["id"]} book id')

    ids = [b['id'] for b in library['books']]
    C(ids.count(BOOK) == 1, 'single econometrics registry entry')
    C('industrial-economics' in ids, 'industrial economics present')
    C(ids.index(BOOK) < ids.index('industrial-economics'), 'econometrics before industrial economics')
    if 'industry-trade' in ids:
        C(ids.index('industrial-economics') < ids.index('industry-trade'), 'industrial economics before industry trade')
    if expected_library_version:
        C(library['version'] == expected_library_version, 'expected library version')
    C(f"study-library-{library['version']}" in (site / 'sw.js').read_text(encoding='utf-8'), 'service worker version')

    for token in ('strict exogeneity', '整段 X 歷史', 'time-varying confounder', '不等於 X 自動外生'):
        C(token.casefold() in chapters['ch13'].casefold(), f'v2 panel correction preserved: {token}')
    for token in ('SATE', 'PATE', '代表性抽樣', '不能只靠 random assignment'):
        C(token.casefold() in chapters['ch15'].casefold(), f'v2 experiment correction preserved: {token}')
    v2q13 = qmap['ch13-q04']['answer'] + ' ' + qmap['ch13-q04']['explanation']
    C('strict exogeneity' in v2q13, 'v2 ch13-q04 preserved')
    v2q15 = qmap['ch15-q02']['answer'] + ' ' + qmap['ch15-q02']['explanation']
    C('SATE' in v2q15 and 'PATE' in v2q15, 'v2 ch15-q02 preserved')

    for token in ('Complier', 'LATE', 'Monotonicity', 'defiers', 'ATE', 'ATT'):
        C(token.casefold() in chapters['ch14'].casefold(), f'ch14 LATE precision: {token}')
    C(r'LATE=E[Y(1)-Y(0)\mid D(1)>D(0)]' in raw_chapters['ch14'], 'ch14 LATE formula')
    q14 = qmap['ch14-q05']['answer'] + ' ' + qmap['ch14-q05']['explanation']
    for token in ('Compliers', 'LATE', 'monotonicity', 'ATE', 'ATT'):
        C(token.casefold() in q14.casefold(), f'ch14-q05 LATE gate: {token}')

    for token in ('compliers', 'LATE', 'ATT', 'TOT', 'assignment 作為實際 treatment 的工具'):
        C(token.casefold() in chapters['ch15'].casefold(), f'ch15 noncompliance precision: {token}')
    C('若要估接受處置者的局部效果' not in chapters['ch15'], 'old ambiguous treated-effect wording removed')
    q15 = qmap['ch15-q04']['answer'] + ' ' + qmap['ch15-q04']['explanation']
    for token in ('原始隨機 assignment', 'compliers', 'LATE'):
        C(token.casefold() in q15.casefold(), f'ch15-q04 noncompliance gate: {token}')

    for token in ('no anticipation', '提前反應', 'pre-treatment', 'parallel trends'):
        C(token.casefold() in chapters['ch16'].casefold(), f'ch16 anticipation gate: {token}')

    for token in ('local compliers', 'LATE', 'monotonicity', 'exclusion', 'cutoff'):
        C(token.casefold() in chapters['ch17'].casefold(), f'ch17 fuzzy RDD gate: {token}')
    q17 = qmap['ch17-q05']['answer'] + ' ' + qmap['ch17-q05']['explanation']
    for token in ('local compliers', 'LATE', 'monotonicity', '整體 ATE'):
        C(token.casefold() in q17.casefold(), f'ch17-q05 fuzzy gate: {token}')

    for token in ('validation RMSE', 'final test set', '尚未打開', 'model selection', 'test 已參與 model selection'):
        C(token.casefold() in chapters['ch18'].casefold(), f'ch18 holdout gate: {token}')
    C('training RMSE=0.5、test RMSE=3' not in chapters['ch18'], 'old test-selection example removed')
    q18 = qmap['ch18-q03']['question'] + ' ' + qmap['ch18-q03']['answer'] + ' ' + qmap['ch18-q03']['explanation']
    for token in ('validation RMSE', '第二個模型', 'untouched test set', '不能用 test 一邊選模型'):
        C(token.casefold() in q18.casefold(), f'ch18-q03 holdout gate: {token}')

    for token in ('LATE／CACE', 'monotonicity', 'ATE／ATT'):
        C(token.casefold() in appendices['appendix-b'].casefold(), f'appendix B IV gate: {token}')
    for token in ('no anticipation', 'local complier LATE', 'Validation／cross-validation', 'Final test set'):
        C(token.casefold() in appendices['appendix-b'].casefold(), f'appendix B workflow gate: {token}')
    for token in ('Sample Average Treatment Effect', 'Population Average Treatment Effect', 'Complier', 'Local Average Treatment Effect', 'No Anticipation', 'Validation Set'):
        C(token.casefold() in appendices['appendix-c'].casefold(), f'appendix C glossary gate: {token}')

    corpus = '\n'.join(chapters.values()) + '\n' + '\n'.join(q['answer'] + ' ' + q['explanation'] for q in questions)
    for bad in (
        'Wald ratio 一定等於全母體 ATE',
        'assignment 作 IV 就等於所有實際接受 treatment 者的效果',
        'parallel trends 成立就不需要考慮 anticipation',
        'fuzzy RDD 一定識別整體 ATE',
        '用 final test set 選完模型後仍可把同一 test 當完全未碰過的最終評估',
    ):
        C(bad.casefold() not in corpus.casefold(), f'negative overclaim gate: {bad}')

    numeric = [
        ('ch01-q01', 10 / math.sqrt(100), 1.0, '1。'),
        ('ch01-q02', (1 / math.sqrt(400)) / (1 / math.sqrt(100)), 0.5, '1/2'),
        ('ch01-q03', 2 + 3 * 4, 14.0, '14'),
        ('ch02-q01', 3 / 2, 1.5, '1.5'),
        ('ch02-q02', 10 / 3 - (3 / 2) * 2, 1 / 3, '1/3'),
        ('ch02-q04', 1 - 20 / 100, 0.8, '0.80'),
        ('ch03-q01', 4 / 20, 0.2, '0.20'),
        ('ch03-q02', math.sqrt(4 / 20), math.sqrt(0.2), '0.447'),
        ('ch04-q02', 1 - (1 - 0.40) * (99 / 96), 0.38125, '0.381'),
        ('ch05-q01', 5 + 3 * 0.2, 5.6, '5.6'),
        ('ch06-q01', 2.4 / 0.6, 4.0, '4'),
        ('ch06-q02', 2.4 - 1.96 * 0.6, 1.224, '1.224'),
        ('ch07-q04', (math.exp(0.1823) - 1) * 100, 19.9974132126, '20%'),
        ('ch08-q01', 1.2 / 0.4, 3.0, '3'),
        ('ch09-q01', 1 / (1 - 0.8), 5.0, '5'),
        ('ch09-q04', 2 * (4 / (4 + 1)), 1.6, '1.6'),
        ('ch10-q02', 0.8 * 0.5 * 0.5, 0.2, '0.20'),
        ('ch11-q01', 100 + 2 - 1, 101.0, '101'),
        ('ch11-q02', 100 * (math.log(105) - math.log(100)), 4.87901641694, '4.879'),
        ('ch12-q01', 2 + 0.8 * 10, 10.0, '10'),
        ('ch12-q02', 2 / (1 - 0.8), 10.0, '10'),
        ('ch13-q01', 2 * (5 - 3), 4.0, '4'),
        ('ch14-q01', 6 / 2, 3.0, '3'),
        ('ch15-q01', 75 - 70, 5.0, '5'),
        ('ch16-q01', (70 - 50) - (55 - 45), 10.0, '10'),
        ('ch17-q01', 68 - 62, 6.0, '6'),
        ('ch18-q01', (1 + 2 + 3) / 3, 2.0, '2'),
        ('ch18-q02', math.sqrt((1 + 4 + 9) / 3), 2.16024689947, '2.160'),
        ('ch19-q02', 100 * 0.04, 4.0, '4 個百分點'),
    ]
    for qid, calc, expected, token in numeric:
        C(qid in qmap, f'numeric question present {qid}')
        C(close(calc, expected, 1e-8), f'numeric recomputation {qid}')
        C(token in qmap[qid]['answer'], f'numeric displayed answer {qid}')

    print(
        f'ECONOMETRICS_REAUDIT_V3_OK checks={checks} chapters=20 appendices=3 '
        f'questions=100 search=189 figures=20 question_rechecks=100 '
        f'numeric_rechecks={len(numeric)} correction_areas=5 question_adjustments=4 ids_preserved=true'
    )


if __name__ == '__main__':
    if len(sys.argv) not in (2, 3):
        raise SystemExit('usage: python deploy/qa_econometrics_reaudit_v3.py SITE_ROOT [EXPECTED_LIBRARY_VERSION]')
    main(sys.argv[1], sys.argv[2] if len(sys.argv) == 3 else None)
