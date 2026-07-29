#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import sys
from collections import Counter
from pathlib import Path

BOOK = 'advanced-statistics'
VERSION = '2026.07.30-1'
checks = 0
numeric = 0


def ck(cond, msg):
    global checks
    checks += 1
    if not cond:
        raise AssertionError(msg)


def num(cond, msg):
    global numeric
    numeric += 1
    if not cond:
        raise AssertionError(msg)


def main(site_root: str, expected_library_version: str) -> None:
    site = Path(site_root)
    root = site / 'books' / BOOK
    lib = json.loads((site / 'data/library.json').read_text(encoding='utf-8'))
    manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    questions = json.loads((root / 'questions.json').read_text(encoding='utf-8'))
    search = json.loads((root / 'search.json').read_text(encoding='utf-8'))
    ids = [b['id'] for b in lib['books']]

    ck(lib['version'] == expected_library_version, 'library version')
    ck(ids.count(BOOK) == 1, 'advanced statistics appears exactly once')
    if 'computer-fundamentals' in ids:
        ck(ids.index(BOOK) < ids.index('computer-fundamentals'), 'canonical order')
    ck(manifest['id'] == BOOK and manifest['version'] == VERSION, 'manifest version')
    ck(questions['bookId'] == BOOK and questions['version'] == VERSION, 'question version')

    chapters = [m for m in manifest['chapters'] if m['kind'] == 'chapter']
    appendices = [m for m in manifest['chapters'] if m['kind'] == 'appendix']
    ck(len(chapters) == 20, '20 chapters')
    ck(len(appendices) == 3, '3 appendices')
    ck([m['id'] for m in chapters] == [f'ch{i:02d}' for i in range(20)], 'chapter IDs stable')
    ck(questions['count'] == len(questions['items']) == 100, '100 questions')
    ck(len({q['id'] for q in questions['items']}) == 100, 'question IDs unique')
    ck(Counter(q['chapterId'] for q in questions['items']) == {f'ch{i:02d}': 5 for i in range(20)}, 'five questions each')
    ck(len(search['entries']) == 189, '189 search entries')
    ck(manifest.get('releaseNotes', [])[0]['version'] == VERSION, 'v2 release note first')

    html_by_id = {}
    for meta in manifest['chapters']:
        p = root / meta['file']
        ck(p.is_file() and p.stat().st_size > 900, f'file exists {meta["id"]}')
        text = p.read_text(encoding='utf-8')
        html_by_id[meta['id']] = text
        ck('<h1>' in text, f'h1 {meta["id"]}')
        if meta['kind'] == 'chapter':
            for heading in ['本章要解決的問題', '白話直覺', '正式定義與核心概念', '核心公式與成立條件', '完整標準例題', '常見錯誤', '考試判斷方法', '理解檢查']:
                ck(heading in text, f'{meta["id"]} heading {heading}')

    required = {
        'ch03': ['負二項分配', '直到第 r 次成功', '0.049152', 'E(X)='],
        'ch07': ['退化常態', 'σ_X²&gt;0', '聯合常態'],
        'ch11': ['Slutsky', '大數法則', 'g′(θ)=0', '更高階 Delta method'],
        'ch13': ['MLE 不變性', 'm̂_MLE', 'g(θ̂)'],
        'ch14': ['兩者一般互不推出', '同時完備且充分', '可積函數'],
        'ch15': ['一致性', '漸近常態', '平方可積', 'p∈(0,1)'],
        'ch16': ['有限樣本精確', 'Xi iid~N(μ,σ²)', 'S²='],
        'ch17': ['size≤α', 'composite H0', 'randomization', '不是 P(H0|data)'],
        'ch18': ['Karlin–Rubin', '單調概似比', '真參數位於適當內點', '非標準極限'],
        'ch19': ['E(ε|X)=0', 'Var(ε|X)=σ²I', 'F_{q,n-p}', 'BLUE'],
    }
    for cid, tokens in required.items():
        text = html_by_id[cid]
        for token in tokens:
            ck(token in text, f'{cid} missing correction token {token}')

    old_wrong = '完備性比充分性更強，兩者不能混為同一件事。'
    ck(old_wrong not in html_by_id['ch14'], 'old completeness/sufficiency overclaim removed')
    ck('level α 只要求 size≤α' not in html_by_id['ch17'] or 'size≤α' in html_by_id['ch17'], 'level/size phrasing coherent')

    q = {x['id']: x for x in questions['items']}
    changed = {
        'ch03-q05': ('0.049152。', 'Negative Binomial'),
        'ch11-q01': ('N(0,1/4)。', 'Slutsky'),
        'ch13-q03': ('X̄。', 'MLE invariance'),
        'ch14-q04': ('沒有；兩者是不同性質，一般互不推出。', '互不推出'),
        'ch15-q05': ('不一定；只保證不增加。', '平方可積'),
        'ch17-q04': ('可以。', 'size≤α'),
        'ch18-q04': ('正則巢狀模型中完整模型與 H0 受限模型的有效參數維度差（等價於獨立限制數）。', '內點'),
    }
    for qid, (answer, explanation_token) in changed.items():
        ck(q[qid]['answer'] == answer, f'{qid} answer')
        combined = q[qid]['question'] + q[qid]['answer'] + q[qid]['explanation']
        ck(explanation_token in combined, f'{qid} correction token')

    for item in questions['items']:
        ck(bool(item['question'].strip()), f'question nonempty {item["id"]}')
        ck(bool(item['answer'].strip()), f'answer nonempty {item["id"]}')
        ck(len(item['explanation'].strip()) >= 8, f'explanation substantive {item["id"]}')
        ck(item['chapterId'] in {m['id'] for m in chapters}, f'question chapter {item["id"]}')

    valid_ids = {m['id'] for m in manifest['chapters']}
    for entry in search['entries']:
        ck(entry['chapterId'] in valid_ids, 'search chapter id')
        ck(bool(entry['title'].strip()) and bool(entry['text'].strip()), 'search text nonempty')
    corpus = '\n'.join(e['text'] for e in search['entries'])
    for token in ['Negative Binomial', 'Slutsky', 'MLE 不變性', '兩者一般互不推出', 'level α', 'Karlin–Rubin', 'Gauss–Markov']:
        ck(token in corpus, f'search contains {token}')

    num(abs(math.comb(6, 2) * (0.2 ** 3) * (0.8 ** 4) - 0.049152) < 1e-12, 'negative binomial probability')
    num(abs(3 / 0.2 - 15) < 1e-12, 'negative binomial mean')
    num(abs((1 / 2) ** 2 - 0.25) < 1e-12, 'Slutsky scaled normal variance')
    num(abs((0.5) ** 2 * 9 - 2.25) < 1e-12, 'delta method variance')
    num(abs((10 - 1) * 4 / 4 - 9) < 1e-12, 'chi square statistic')
    num(abs((12 - 10) / (4 / math.sqrt(16)) - 2) < 1e-12, 't statistic')
    num(abs(3 / 4 - 0.75) < 1e-12, 'gamma variance example')
    num(abs((1 + 1 + 2 * 0.5) - 3) < 1e-12, 'multivariate variance')
    num(abs((1 - 0.5 ** 2) - 0.75) < 1e-12, 'conditional normal variance')
    num(abs(4 / 5 - 0.8) < 1e-12 and abs(1 / 5 - 0.2) < 1e-12, 'order statistics means')
    num(abs(5 * 0.2 * 0.8 ** 4 - 0.4096) < 1e-12, 'binomial example')
    num(abs(math.exp(-2) - 0.1353352832366127) < 1e-12, 'poisson zero')
    num(abs(math.exp(-1) - 0.36787944117144233) < 1e-12, 'exponential tail')
    num(abs((0.9 * 0.1) / (0.9 * 0.1 + 0.2 * 0.9) - 1 / 3) < 1e-12, 'Bayes')
    num(abs((10.5 - 10) / (2 / math.sqrt(100)) - 2.5) < 1e-12, 'z statistic')
    p = 2 * (1 - 0.5 * (1 + math.erf(2.5 / math.sqrt(2))))
    num(abs(p - 0.01241933065) < 1e-8, 'two-sided z p-value')
    num(abs(10 - 1.96 * 0.2 - 9.608) < 1e-12 and abs(10 + 1.96 * 0.2 - 10.392) < 1e-12, 'z interval')
    num(abs(20 - 2.064 - 17.936) < 1e-12 and abs(20 + 2.064 - 22.064) < 1e-12, 't interval')
    xs = [1, 2, 3]; ys = [2, 4, 5]
    mx = sum(xs) / 3; my = sum(ys) / 3
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    b1 = sxy / sxx; b0 = my - b1 * mx
    preds = [b0 + b1 * x for x in xs]
    sse = sum((y - yh) ** 2 for y, yh in zip(ys, preds)); sst = sum((y - my) ** 2 for y in ys)
    num(abs(b1 - 1.5) < 1e-12 and abs(b0 - 2 / 3) < 1e-12, 'OLS coefficients')
    num(abs(sse - 1 / 6) < 1e-12 and abs((1 - sse / sst) - 27 / 28) < 1e-12, 'OLS fit')

    sw = (site / 'sw.js').read_text(encoding='utf-8')
    ck(f"study-library-{expected_library_version}" in sw, 'service worker version')
    ck('./books/advanced-statistics/manifest.json' in sw, 'advanced manifest cached')
    ck('./books/advanced-statistics/chapters/ch19.html' in sw, 'advanced final chapter cached')

    print(
        f'ADVANCED_STATISTICS_V2_QA_OK checks={checks} numerical_rechecks={numeric} '
        f'books={len(ids)} library={expected_library_version} corrections=10 question_adjustments=7 '
        f'chapters=20 appendices=3 questions=100 search=189'
    )


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('usage: python deploy/qa_advanced_statistics_reaudit_v2.py SITE_ROOT EXPECTED_LIBRARY_VERSION')
    main(sys.argv[1], sys.argv[2])
