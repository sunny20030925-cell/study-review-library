#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import sys
from collections import Counter
from pathlib import Path

BOOK = 'advanced-statistics'
SUPPORTED_VERSIONS = {'2026.07.29-1', '2026.07.30-1'}


def main(site_root: str, expected_library: str) -> int:
    site = Path(site_root)
    root = site / 'books' / BOOK
    lib = json.loads((site / 'data/library.json').read_text(encoding='utf-8'))
    manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    questions = json.loads((root / 'questions.json').read_text(encoding='utf-8'))
    search = json.loads((root / 'search.json').read_text(encoding='utf-8'))
    checks = 0
    numeric = 0

    def ck(cond, msg):
        nonlocal checks
        checks += 1
        if not cond:
            raise AssertionError(msg)

    def num(cond, msg):
        nonlocal numeric
        numeric += 1
        if not cond:
            raise AssertionError(msg)

    ids = [b['id'] for b in lib['books']]
    ck(lib['version'] == expected_library, 'library version')
    ck(ids.count(BOOK) == 1, 'single advanced-statistics registry entry')
    ck(len(ids) == len(set(ids)), 'unique book ids')
    if 'money-banking' in ids:
        ck(ids.index('money-banking') < ids.index(BOOK), 'advanced statistics remains after money banking')
    if 'computer-fundamentals' in ids:
        ck(ids.index(BOOK) < ids.index('computer-fundamentals'), 'advanced statistics remains before computer fundamentals')

    version = manifest['version']
    ck(version in SUPPORTED_VERSIONS, f'supported content version: {version}')
    ck(manifest['id'] == BOOK, 'manifest id')
    ck(questions['bookId'] == BOOK and questions['version'] == version, 'questions identity/version')
    ck(manifest.get('releaseNotes', [{}])[0].get('version') == version, 'release note version')

    chapters = [x for x in manifest['chapters'] if x['kind'] == 'chapter']
    appendices = [x for x in manifest['chapters'] if x['kind'] == 'appendix']
    ck(len(chapters) == 20, '20 chapters')
    ck(len(appendices) == 3, '3 appendices')
    ck([x['id'] for x in chapters] == [f'ch{i:02d}' for i in range(20)], 'stable chapter ids')
    ck([x['id'] for x in appendices] == ['appendix-a', 'appendix-b', 'appendix-c'], 'stable appendix ids')
    ck(questions['count'] == len(questions['items']) == 100, '100 questions')
    ck(len({q['id'] for q in questions['items']}) == 100, 'unique question ids')
    ck(Counter(q['chapterId'] for q in questions['items']) == {f'ch{i:02d}': 5 for i in range(20)}, 'five questions per chapter')
    ck(len(search['entries']) == 189, '189 search entries')

    headings = ['本章要解決的問題', '白話直覺', '正式定義與核心概念', '核心公式與成立條件', '完整標準例題', '常見錯誤', '考試判斷方法', '理解檢查']
    all_text = []
    for meta in manifest['chapters']:
        p = root / meta['file']
        ck(p.is_file() and p.stat().st_size > 900, f'chapter/appendix exists {meta["id"]}')
        text = p.read_text(encoding='utf-8')
        all_text.append(text)
        ck('<h1>' in text, f'h1 {meta["id"]}')
        if meta['kind'] == 'chapter':
            for heading in headings:
                ck(heading in text, f'{meta["id"]} heading {heading}')

    corpus = '\n'.join(all_text) + '\n' + json.dumps(questions, ensure_ascii=False)
    for token in [
        '條件機率（conditional probability）', '累積分配函數（CDF）', 'Gamma(α,λ)', '聯合密度（joint density）',
        '條件期望（conditional expectation）', '多元常態（multivariate normal）', 'Jacobian', '特徵函數（characteristic function）',
        '次序統計量（order statistic）', '中央極限定理（CLT）', 'Student t 分配', '最大概似估計（MLE）',
        '充分統計量（sufficient statistic）', 'Cramér–Rao 下界', 'Rao–Blackwell', '樞紐量（pivotal quantity）',
        'Neyman–Pearson', 'UMP 檢定', 'Wilks 定理', 'Gauss–Markov 定理',
        'R² 高仍不等於因果關係成立',
    ]:
        ck(token in corpus, f'core/corrective concept {token}')
    ck(('不是 H0 為真的機率' in corpus) or ('不是 P(H0|data)' in corpus), 'p-value is not posterior probability of H0')

    if version == '2026.07.30-1':
        for token in ['負二項分配（Negative Binomial）', 'Slutsky 定理', 'MLE 不變性（invariance）', '兩者一般互不推出', 'level-α 檢定', '單調概似比（MLR）']:
            ck(token in corpus, f'v2 correction present: {token}')
        ck('完備性比充分性更強，兩者不能混為同一件事。' not in corpus, 'old completeness/sufficiency overclaim removed')

    qmap = {q['id']: q for q in questions['items']}
    invariant_answers = {
        'ch00-q01': '1。', 'ch01-q01': '0.8。', 'ch01-q04': '1/3。', 'ch02-q01': '0.75。',
        'ch03-q01': '0.4096。', 'ch04-q02': '1.5。', 'ch05-q01': 'f_X(x)=2x，0<x<1。',
        'ch06-q01': '19。', 'ch07-q01': '3。', 'ch08-q02': '1/2。', 'ch09-q03': 'Poisson(5)。',
        'ch10-q01': '4/5。', 'ch11-q05': '9/4。', 'ch12-q02': '2。', 'ch13-q02': '0.5。',
        'ch15-q01': 'p(1-p)/n。', 'ch16-q01': '[9.608, 10.392]。', 'ch17-q01': '2.5。',
        'ch19-q01': '1.5。', 'ch19-q03': '27/28，約 0.9643。',
    }
    for qid, answer in invariant_answers.items():
        ck(qmap[qid]['answer'] == answer, f'invariant answer {qid}')

    if version == '2026.07.30-1':
        changed = {
            'ch03-q05': '0.049152。',
            'ch11-q01': 'N(0,1/4)。',
            'ch13-q03': 'X̄。',
            'ch14-q04': '沒有；兩者是不同性質，一般互不推出。',
            'ch15-q05': '不一定；只保證不增加。',
            'ch17-q04': '可以。',
            'ch18-q04': '正則巢狀模型中完整模型與 H0 受限模型的有效參數維度差（等價於獨立限制數）。',
        }
        for qid, answer in changed.items():
            ck(qmap[qid]['answer'] == answer, f'v2 answer {qid}')

    num(abs(5 * .2 * (.8 ** 4) - .4096) < 1e-12, 'binomial')
    num(abs(math.exp(-2) - .1353352832366127) < 1e-12, 'poisson zero')
    num(abs(math.exp(-1) - .36787944117144233) < 1e-12, 'exponential tail')
    num(abs((4 + 9 + 2 * 3) - 19) < 1e-12, 'variance sum')
    num(abs((1 + 1 + 2 * .5) - 3) < 1e-12, 'multivariate variance')
    num(abs((1 - .5 ** 2) - .75) < 1e-12, 'conditional normal variance')
    num(abs((.5) ** 2 * 9 - 2.25) < 1e-12, 'delta method')
    num(abs((12 - 10) / (4 / math.sqrt(16)) - 2) < 1e-12, 't statistic')
    num(abs(10 - 1.96 * .2 - 9.608) < 1e-12, 'z interval')
    z = (10.5 - 10) / (2 / math.sqrt(100))
    num(abs(z - 2.5) < 1e-12, 'z statistic')
    if version == '2026.07.30-1':
        num(abs(math.comb(6, 2) * (.2 ** 3) * (.8 ** 4) - .049152) < 1e-12, 'negative binomial v2')
        num(abs((1 / 2) ** 2 - .25) < 1e-12, 'Slutsky v2')

    valid_ids = {m['id'] for m in manifest['chapters']}
    for entry in search['entries']:
        ck(entry['chapterId'] in valid_ids, 'search chapter id')
        ck(bool(entry['title'].strip()) and bool(entry['text'].strip()), 'search nonempty')

    figs = sorted((site / 'assets/advanced-statistics-svg').glob('*.svg'))
    ck(len(figs) == 20, '20 figures')
    for p in figs:
        svg = p.read_text(encoding='utf-8')
        ck('<title' in svg and '<desc' in svg and 'viewBox=' in svg, f'svg accessibility {p.name}')
        ck('href="http' not in svg and "href='http" not in svg, f'no remote svg {p.name}')

    sw = (site / 'sw.js').read_text(encoding='utf-8')
    ck(f'study-library-{expected_library}' in sw, 'sw library version')
    for token in [
        './books/advanced-statistics/manifest.json', './books/advanced-statistics/questions.json',
        './books/advanced-statistics/search.json', './books/advanced-statistics/chapters/ch19.html',
        './assets/advanced-statistics-svg/linear-model-theory.svg',
    ]:
        ck(token in sw, f'sw path {token}')

    print(f'ADVANCED_STATISTICS_STRUCTURAL_QA_OK checks={checks} numerical_rechecks={numeric} books={len(ids)} library={expected_library} content={version}')
    return checks


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('usage: python deploy/validate_advanced_statistics.py SITE_ROOT EXPECTED_LIBRARY')
    main(sys.argv[1], sys.argv[2])
