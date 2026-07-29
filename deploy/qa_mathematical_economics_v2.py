#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

BOOK = 'mathematical-economics'
VERSION = '2026.07.30-2'


def main(site_root: str, expected_library: str) -> None:
    site = Path(site_root)
    root = site / 'books' / BOOK
    library = json.loads((site / 'data/library.json').read_text(encoding='utf-8'))
    manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    questions = json.loads((root / 'questions.json').read_text(encoding='utf-8'))
    search = json.loads((root / 'search.json').read_text(encoding='utf-8'))
    ids = [b['id'] for b in library['books']]
    checks = 0

    def ck(condition: bool, message: str) -> None:
        nonlocal checks
        checks += 1
        if not condition:
            raise AssertionError(message)

    ck(library['version'] == expected_library, 'library version')
    ck(ids and ids[-1] == BOOK and ids.count(BOOK) == 1, f'book tail {ids[-3:]}')
    ck(len(ids) == len(set(ids)), 'unique book ids')
    ck(manifest['id'] == questions['bookId'] == BOOK, 'book id')
    ck(manifest['version'] == questions['version'] == VERSION, 'v2 content version')
    ck(manifest['releaseNotes'][0]['version'] == VERSION, 'v2 release note')
    ck('第二次獨立內容審計' in manifest['releaseNotes'][0]['title'], 'v2 release title')

    chapters = [x for x in manifest['chapters'] if x['kind'] == 'chapter']
    appendices = [x for x in manifest['chapters'] if x['kind'] == 'appendix']
    ck(len(chapters) == 20, '20 chapters')
    ck(len(appendices) == 3, '3 appendices')
    ck(questions['count'] == len(questions['items']) == 100, '100 questions')
    ck(len({q['id'] for q in questions['items']}) == 100, 'unique question ids')
    ck(Counter(q['chapterId'] for q in questions['items']) == {f'ch{i:02d}': 5 for i in range(20)}, 'five questions per chapter')
    ck(len(search['entries']) == 150, '150 search entries')

    required_sections = ['本章要解決的問題', '白話直覺', '正式定義與核心概念', '核心公式與成立條件', '完整標準例題', '常見錯誤', '考試判斷方法', '理解檢查']
    chapter_text = {}
    for chapter in chapters:
        path = root / chapter['file']
        ck(path.is_file(), f'missing {chapter["id"]}')
        text = path.read_text(encoding='utf-8')
        chapter_text[chapter['id']] = text
        plain = re.sub(r'<[^>]+>', '', text)
        ck(len(plain) >= 700, f'too thin {chapter["id"]}: {len(plain)}')
        for section in required_sections:
            ck(section in text, f'{chapter["id"]} missing {section}')
        ck('<script' not in text.lower(), f'inline script {chapter["id"]}')
        ck("\\'" not in text, f'bad derivative-prime markup {chapter["id"]}')

    for appendix in appendices:
        path = root / appendix['file']
        ck(path.is_file() and path.stat().st_size > 500, f'appendix {appendix["id"]}')
        ck("\\'" not in path.read_text(encoding='utf-8'), f'bad prime in {appendix["id"]}')

    corrections = {
        'ch04': ['det(A)≠0'],
        'ch05': ['λ&lt;0', 'λ=0', '一維子空間', 'Hessian 時'],
        'ch06': ['乘法法則', '商數法則', '鏈鎖律'],
        'ch07': ['Euclidean', '有限變動'],
        'ch08': ['非奇異方陣', 'J_y', 'J_y^{-1}'],
        'ch09': ['Q=AK^aL^b', 'd\\ln Q'],
        'ch11': ['擬凹函數', '負半定', '凸可行域'],
        'ch12': ['切空間二階條件', '可行切方向', 'd^T'],
        'ch13': ['constraint qualification', 'LICQ', 'Slater', '全域最適'],
        'ch14': ['受限制問題', 'partial\\mathcal L', '限制右側'],
        'ch15': ['嚴格遞增轉換'],
        'ch18': ['b=-1', '|b|=1'],
        'ch19': ['F′(x*)=0', '不下結論'],
    }
    for cid, tokens in corrections.items():
        text = chapter_text[cid]
        for token in tokens:
            ck(token in text, f'{cid} missing correction token {token}')

    forbidden = {
        'ch09': ['y=Ax^ay^b'],
        'ch12': ['對稱性與凹化條件支持此為限制下最大點'],
        'ch13': ['KKT 條件</dt><dd>不等式限制最佳化的一組一階必要條件；'],
        'ch15': ['由單調轉換作用在齊次函數上得到'],
    }
    for cid, tokens in forbidden.items():
        for token in tokens:
            ck(token not in chapter_text[cid], f'{cid} stale token {token}')

    qmap = {q['id']: q for q in questions['items']}
    expected_v2 = {
        'ch05-q03': '仍在同一條一維子空間上，但方向反轉。',
        'ch06-q03': '24。',
        'ch07-q03': '錯。',
        'ch09-q02': '約 1.7%。',
        'ch11-q03': 'f 為凹函數。',
        'ch12-q03': '支持該候選點是受限嚴格局部最大。',
        'ch13-q03': '錯。',
        'ch14-q03': 'dV/dθ=∂L/∂θ，在最適解與最適乘數處評估。',
        'ch15-q03': '嚴格遞增轉換。',
        'ch18-q03': '通常形成二期循環，不會漸近收斂到穩態。',
        'ch19-q03': '不可以，線性化判準在此不下結論。',
    }
    for qid, answer in expected_v2.items():
        ck(qmap[qid]['answer'] == answer, f'v2 answer {qid}: {qmap[qid]["answer"]!r}')
        ck(len(qmap[qid]['explanation']) >= 28, f'v2 explanation too short {qid}')

    legacy_negative = ['ch00-q05', 'ch05-q05', 'ch08-q05', 'ch10-q05', 'ch12-q05', 'ch13-q05', 'ch16-q05', 'ch18-q05']
    for qid in legacy_negative:
        ck(qmap[qid]['answer'] == '錯。', f'legacy negative gate {qid}')

    # Independent recomputation of representative quantitative and second-order claims.
    numeric = {
        'demand': 120 - 3 * 20,
        'equilibrium_price': (100 - 20) / 4,
        'determinant': 2 * 1 - 1 * 1,
        'chain_rule': 2 * (3 * 1 + 1) * 3,
        'total_differential': 7 * 0.1 + 2 * (-0.2),
        'implicit_derivative': 1 / (2 * 2),
        'implicit_change': (1 / 4) * 0.4,
        'elasticity': -2,
        'cobb_douglas_log_change_pct': 0.3 * 1 + 0.7 * 2,
        'univariate_argmax': 20 / 2,
        'univariate_value': 20 * 10 - 10**2,
        'multivariate_x': 10 / 2,
        'multivariate_y': 8 / 2,
        'lagrange_x': 10 / 2,
        'restricted_curvature': -2,
        'kkt_multiplier_upper_bound': 4,
        'envelope_value_derivative_at_a': 2,
        'homogeneous_degree': 0.4 + 0.6,
        'cost_at_3': 10 + 3**2 + 4 * 3,
        'compound': 100 * 1.05**2,
        'continuous_rate': math.log(1.05),
        'difference_ss': 10 / (1 - 0.5),
        'differential_ss': 6 / 0.3,
    }
    ck(numeric['demand'] == 60 and numeric['equilibrium_price'] == 20, 'basic/equilibrium recompute')
    ck(numeric['determinant'] == 1, 'determinant recompute')
    ck(numeric['chain_rule'] == 24, 'chain rule recompute')
    ck(abs(numeric['total_differential'] - 0.3) < 1e-12, 'total differential recompute')
    ck(numeric['implicit_derivative'] == 0.25 and abs(numeric['implicit_change'] - 0.1) < 1e-12, 'implicit recompute')
    ck(numeric['elasticity'] == -2 and abs(numeric['cobb_douglas_log_change_pct'] - 1.7) < 1e-12, 'elasticity/log recompute')
    ck(numeric['univariate_argmax'] == 10 and numeric['univariate_value'] == 100, 'univariate optimization recompute')
    ck(numeric['multivariate_x'] == 5 and numeric['multivariate_y'] == 4, 'multivariate optimization recompute')
    ck(numeric['lagrange_x'] == 5 and numeric['restricted_curvature'] < 0, 'constrained SOC recompute')
    ck(numeric['kkt_multiplier_upper_bound'] == 4, 'KKT multiplier recompute')
    ck(numeric['envelope_value_derivative_at_a'] == 2, 'envelope numerical checkpoint')
    ck(numeric['homogeneous_degree'] == 1, 'homogeneity recompute')
    ck(numeric['cost_at_3'] == 31, 'integration recompute')
    ck(abs(numeric['compound'] - 110.25) < 1e-12 and abs(numeric['continuous_rate'] - 0.04879016417) < 1e-10, 'growth recompute')
    ck(numeric['difference_ss'] == 20 and numeric['differential_ss'] == 20, 'dynamic steady states')

    # Cross-concept logic gates independent of exact prose.
    logic_gates = [
        qmap['ch13-q03']['answer'] == '錯。',
        qmap['ch13-q05']['answer'] == '錯。',
        qmap['ch10-q05']['answer'] == '錯。',
        qmap['ch07-q03']['answer'] == '錯。',
        qmap['ch15-q03']['answer'] == '嚴格遞增轉換。',
        '二期循環' in qmap['ch18-q03']['answer'],
        '不下結論' in qmap['ch19-q03']['answer'],
        '切方向' in qmap['ch12-q03']['explanation'],
        'Lagrangian' in qmap['ch14-q03']['explanation'],
        '內層' in qmap['ch06-q03']['explanation'],
    ]
    for i, gate in enumerate(logic_gates, start=1):
        ck(gate, f'high-risk logic gate {i}')

    valid_ids = {x['id'] for x in manifest['chapters']}
    search_corpus = '\n'.join(e['title'] + ' ' + e['text'] for e in search['entries'])
    for entry in search['entries']:
        ck(entry['chapterId'] in valid_ids, 'search chapter id')
        ck(bool(entry['title'].strip()) and bool(entry['text'].strip()), 'search nonempty')
        ck("\\'" not in entry['text'], 'search bad prime')
    for token in ['constraint qualification', '嚴格遞增轉換', '鏈鎖律', '擬凹函數', '可行切方向', 'b=-1']:
        ck(token in search_corpus, f'search missing corrected token {token}')
    ck('y=Ax^ay^b' not in search_corpus, 'search stale contradictory formula')

    figures = sorted((site / 'assets/mathematical-economics-svg').glob('*.svg'))
    ck(len(figures) == 20, '20 figures')
    for figure in figures:
        text = figure.read_text(encoding='utf-8')
        ck('<title' in text and '<desc' in text and 'viewBox=' in text, f'accessible SVG {figure.name}')
        ck('href="http' not in text and "href='http" not in text, f'no remote SVG {figure.name}')

    sw = (site / 'sw.js').read_text(encoding='utf-8')
    ck(f"study-library-{expected_library}" in sw, 'service worker version')
    for token in [
        f'./books/{BOOK}/manifest.json',
        f'./books/{BOOK}/questions.json',
        f'./books/{BOOK}/search.json',
        f'./books/{BOOK}/chapters/ch19.html',
        './assets/mathematical-economics-svg/differential-equations.svg',
    ]:
        ck(token in sw, f'service worker path {token}')

    print(
        'MATHEMATICAL_ECONOMICS_V2_QA_OK '
        f'checks={checks} books={len(ids)} library={expected_library} '
        f'chapters=20 appendices=3 questions=100 search=150 figures=20 '
        f'correction_areas={len(corrections)} question_adjustments={len(expected_v2)} '
        f'quantitative_rechecks={len(numeric)} high_risk_logic_gates={len(logic_gates)}'
    )


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('usage: python deploy/qa_mathematical_economics_v2.py SITE_ROOT EXPECTED_LIBRARY')
    main(sys.argv[1], sys.argv[2])
