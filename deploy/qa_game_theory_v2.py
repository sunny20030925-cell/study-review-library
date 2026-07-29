#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import sys
from collections import Counter
from pathlib import Path

BOOK = 'game-theory'
SOURCE_VERSION = '2026.07.29-1'
TARGET_VERSION = '2026.07.30-2'
checks = 0
quantitative = 0
conceptual = 0


def ck(cond, msg):
    global checks
    checks += 1
    if not cond:
        raise AssertionError(msg)


def qcheck(qmap, qid, expected):
    global quantitative
    quantitative += 1
    ck(qmap[qid]['answer'] == expected, f'{qid}: {qmap[qid]["answer"]!r} != {expected!r}')


def ccheck(qmap, qid, expected):
    global conceptual
    conceptual += 1
    ck(qmap[qid]['answer'] == expected, f'{qid}: {qmap[qid]["answer"]!r} != {expected!r}')


def main(site_root: str, expected_library_version: str | None = None) -> int:
    site = Path(site_root)
    library = json.loads((site / 'data/library.json').read_text(encoding='utf-8'))
    ids = [b['id'] for b in library['books']]
    ck(ids.count(BOOK) == 1, f'game theory registry count: {ids}')
    if expected_library_version is not None:
        ck(library['version'] == expected_library_version, f'library {library["version"]} != {expected_library_version}')

    root = site / 'books' / BOOK
    manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    qdoc = json.loads((root / 'questions.json').read_text(encoding='utf-8'))
    search = json.loads((root / 'search.json').read_text(encoding='utf-8'))

    ck(manifest['id'] == BOOK and qdoc['bookId'] == BOOK, 'book identity')
    ck(manifest['version'] == qdoc['version'] == TARGET_VERSION, 'v2 content version')
    ck(manifest.get('updatedAt') == '2026-07-30', 'v2 updated date')
    chapters = [x for x in manifest['chapters'] if x.get('kind') == 'chapter']
    appendices = [x for x in manifest['chapters'] if x.get('kind') == 'appendix']
    ck(len(chapters) == 20 and len(appendices) == 3, '20 chapters + 3 appendices')
    ck([x['id'] for x in chapters] == [f'ch{i:02d}' for i in range(20)], 'chapter ids preserved')
    ck([x['id'] for x in appendices] == ['appendix-a','appendix-b','appendix-c'], 'appendix ids preserved')
    ck(qdoc['count'] == len(qdoc['items']) == 100, '100 questions')
    ck(len({q['id'] for q in qdoc['items']}) == 100, 'question ids unique')
    ck(Counter(q['chapterId'] for q in qdoc['items']) == {f'ch{i:02d}':5 for i in range(20)}, 'five questions per chapter')
    ck(len(search['entries']) == 189, '189 search entries')
    figures = sorted((site / 'assets/game-theory-svg').glob('*.svg'))
    ck(len(figures) == 20, '20 figures')

    html_by_id: dict[str, str] = {}
    for item in manifest['chapters']:
        path = root / item['file']
        ck(path.is_file() and path.stat().st_size > 700, f'missing/short {item["id"]}')
        html = path.read_text(encoding='utf-8')
        html_by_id[item['id']] = html
        ck('<script' not in html.lower(), f'inline script {item["id"]}')
        if item.get('kind') == 'chapter':
            for section in ('白話直覺','正式定義與核心概念','核心公式與成立條件','完整標準例題','常見錯誤','考試判斷方法','理解檢查'):
                ck(section in html, f'{item["id"]} missing {section}')

    # Independent correction gates: verify the actual generated artifact, not only source files.
    correction_gates = {
        'ch02': ['混合策略', 'rationalizable', '嚴格支配'],
        'ch04': ['(U,L)', '(D,R)', '兩個純策略 NE', '混合 NE'],
        'ch06': ['p1=p2=c=10', '不是只「趨近」'],
        'ch07': ['有限、完美資訊', 'perfect information', 'complete information', '非單點資訊集合'],
        'ch08': ['單點資訊集合', '不能切斷任何資訊集合'],
        'ch11': ['給定', 'type-contingent strategy', '不能只算上面的期望值就宣稱已求出完整 PBE'],
        'ch12': ['不需要價值彼此獨立', '私人價值', 'revenue equivalence'],
        'ch13': ['off-path', 'sequential equilibrium', 'Bayes'],
        'ch14': ['2≤e≤6', '不是完整 PBE', 'off-path'],
        'ch16': ['正負號', 'payment', '準線性私人價值'],
        'ch18': ['可排序', 'strategic complements'],
        'ch19': ['不同的資訊維度', 'complete information', 'perfect information', '非單點資訊集合'],
    }
    for cid, tokens in correction_gates.items():
        text = html_by_id[cid]
        for token in tokens:
            ck(token in text, f'{cid} missing v2 correction token: {token}')

    appendix_a_text = html_by_id['appendix-a']
    appendix_b_text = html_by_id['appendix-b']
    appendix_c_text = html_by_id['appendix-c']
    for token in ('proper subgames','payoff/type','非單點資訊集合'):
        ck(token in appendix_a_text, f'appendix-a missing {token}')
    for token in ('complete information','perfect information','已有純 NE，也可能另有混合 NE'):
        ck(token in appendix_b_text, f'appendix-b missing {token}')
    for token in ('Complete Information','Perfect Information'):
        ck(token in appendix_c_text, f'appendix-c missing {token}')

    qmap = {q['id']: q for q in qdoc['items']}
    for q in qdoc['items']:
        ck(q['bookId'] == BOOK, f'book id {q["id"]}')
        ck(bool(q['question'].strip()) and bool(q['answer'].strip()) and len(q['explanation'].strip()) >= 18, f'question completeness {q["id"]}')

    # Recompute quantitative nodes independently.
    p, q = 3/5, 2/5
    ck(math.isclose(p,.6) and math.isclose(q,.4), 'mixed arithmetic')
    qcheck(qmap, 'ch04-q03', 'q=0.4。')
    qcheck(qmap, 'ch04-q04', 'p=0.6。')

    matrix=((2,-1),(-2,1))
    ck(max(min(r) for r in matrix) == -1, 'zero-sum maximin')
    qcheck(qmap, 'ch05-q03', '-1。')
    pz=.5; qz=1/3
    ck(math.isclose(4*pz-2,0) and math.isclose(3*qz-1,0), 'zero-sum mixed value')

    cq=(100-10)/3
    cp=100-2*cq
    ck((cq,cp)==(30,40), 'Cournot')
    qcheck(qmap, 'ch06-q03', '30。')
    qcheck(qmap, 'ch06-q04', '總產量60，價格40。')

    share=(1-.9)/(1-.9*.9)
    ck(math.isclose(share,10/19), 'Rubinstein')
    qcheck(qmap, 'ch09-q02', '約0.5263。')
    qcheck(qmap, 'ch09-q03', '約 NT$52.63。')

    threshold=(5-3)/(5-1)
    ck(math.isclose(threshold,.5), 'grim threshold')
    qcheck(qmap, 'ch10-q01', 'δ≥0.5。')
    ck(math.isclose(3/(1-.8),15) and math.isclose(5+.8/(1-.8),9), 'repeated PV')

    ck(math.isclose(.4*(-1)+.6*2,.8) and math.isclose(.8*(-1)+.2*2,-.4), 'Bayesian entry arithmetic')
    qcheck(qmap, 'ch11-q02', '0.8。')
    qcheck(qmap, 'ch11-q03', '-0.4。')

    bid=(3-1)/3*.9
    ck(math.isclose(bid,.6), 'first-price formula')
    qcheck(qmap, 'ch12-q01', '0.6。')

    posterior=.6/(.6+.4*.25)
    ck(math.isclose(posterior,6/7), 'Bayes posterior')
    qcheck(qmap, 'ch13-q03', '6/7，約0.8571。')

    e_min=(10-4)/3
    e_max=10-4
    ck(math.isclose(e_min,2) and math.isclose(e_max,6), 'signaling interval')
    qcheck(qmap, 'ch14-q02', '7.9。')
    qcheck(qmap, 'ch14-q03', '3.7。')
    qcheck(qmap, 'ch14-q04', '2≤e≤6。')

    ck((100-80,100*.5-25,100-70,50-70)==(20,25,30,-20), 'screening utilities')
    qcheck(qmap, 'ch15-q02', '20。')
    qcheck(qmap, 'ch15-q03', '25；不是 IC。')
    qcheck(qmap, 'ch15-q04', 'H=30，L=-20。')

    payment=sorted([100,80,50],reverse=True)[1]
    ck(payment==80 and 100-payment==20, 'VCG')
    qcheck(qmap, 'ch16-q03', 'NT$80。')
    qcheck(qmap, 'ch16-q04', 'NT$20。')

    ck(90/3*2==60, 'core arithmetic')
    qcheck(qmap, 'ch17-q04', '(30,30,30)。')

    # Re-evaluate the high-risk conceptual corrections independently.
    expected_concepts = {
        'ch02-q05':'不一定。',
        'ch03-q05':'不保證。',
        'ch04-q02':'可能。',
        'ch05-q05':'不能。',
        'ch06-q05':'需要。',
        'ch08-q01':'是。',
        'ch08-q02':'不是。',
        'ch09-q01':'不是。',
        'ch10-q05':'不是。',
        'ch11-q05':'不一定。',
        'ch12-q03':'標準私人價值環境。',
        'ch12-q05':'不是。',
        'ch13-q01':'完整策略與信念。',
        'ch13-q05':'不可以。',
        'ch14-q05':'不一定。',
        'ch16-q05':'是。',
        'ch17-q05':'不一定。',
        'ch18-q05':'不一定。',
        'ch19-q05':'不是。',
    }
    for qid, expected in expected_concepts.items():
        ccheck(qmap, qid, expected)

    forbidden = [
        '有限且完全資訊的賽局樹中，向後歸納',
        '完美資訊；是比完整資訊更強的條件',
        '價格競爭均衡則趨向 p=c=10',
        '這組策略加上信念構成一個簡單 separating PBE。',
        'e=1.5',
    ]
    corpus='\n'.join(html_by_id.values()) + '\n' + json.dumps(qdoc,ensure_ascii=False)
    for phrase in forbidden:
        ck(phrase not in corpus, f'stale v1 phrasing remains: {phrase}')

    notes=manifest.get('releaseNotes',[])
    ck(bool(notes) and notes[0].get('version')==TARGET_VERSION, 'v2 release note')
    ck('第二次內容審稿' in notes[0].get('title',''), 'v2 release note title')

    print(
        f'GAME_THEORY_V2_AUDIT_OK checks={checks} '
        f'quantitative_rechecks={quantitative} conceptual_rechecks={conceptual} '
        f'chapters=20 questions=100 search=189 figures=20'
    )
    return checks


if __name__ == '__main__':
    if len(sys.argv) not in (2,3):
        raise SystemExit('usage: python deploy/qa_game_theory_v2.py SITE_ROOT [EXPECTED_LIBRARY_VERSION]')
    main(sys.argv[1], sys.argv[2] if len(sys.argv)==3 else None)
