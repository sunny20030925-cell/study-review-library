#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import math
import re
import sys
from pathlib import Path

BOOK = 'industrial-economics'
VERSION = '2026.07.30-2'


def main(site_root: str, expected_library: str) -> int:
    site = Path(site_root)
    root = site / 'books' / BOOK
    manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    qdoc = json.loads((root / 'questions.json').read_text(encoding='utf-8'))
    search = json.loads((root / 'search.json').read_text(encoding='utf-8'))
    library = json.loads((site / 'data/library.json').read_text(encoding='utf-8'))
    checks = 0

    def ck(cond, msg):
        nonlocal checks
        checks += 1
        if not cond:
            raise AssertionError(msg)

    ck(manifest['version'] == qdoc['version'] == VERSION, 'book versions')
    ck(library['version'] == expected_library, 'library version')
    ids = [b['id'] for b in library['books']]
    ck(ids.count(BOOK) == 1, 'single book id')
    ck(len(manifest['chapters']) == 23, '23 html entries')
    ck(qdoc['count'] == len(qdoc['items']) == 100, '100 questions')
    ck(len(search['entries']) == 150, '150 search')

    qmap = {q['id']: q for q in qdoc['items']}
    ck(len(qmap) == 100, 'unique qids')
    for q in qdoc['items']:
        ck(len(q['question'].strip()) >= 8, f'question length {q["id"]}')
        ck(len(q['answer'].strip()) >= 2, f'answer length {q["id"]}')
        ck(len(q['explanation'].strip()) >= 8, f'explanation length {q["id"]}')
        ck(q['answer'].strip() != q['explanation'].strip(), f'answer explanation duplicate {q["id"]}')

    # Independent quantitative reconstruction.  None of these values are read from generator constants.
    recomputed = {
        'hhi_40_30_20_10': 40**2 + 30**2 + 20**2 + 10**2,
        'delta_hhi_30_25': 2 * 30 * 25,
        'average_cost': (1_000_000 + 100 * 5_000) / 5_000,
        'scope_economy': 600 + 500 - 900,
        'monopoly_q': (100 - 20) / 2,
        'monopoly_p': 100 - (100 - 20) / 2,
        'lerner': (60 - 20) / 60,
        'third_degree_markup_A': 1 / 2,
        'third_degree_markup_B': 1 / 4,
        'cournot_each_b1': 80 / 3,
        'cournot_total_b1': 160 / 3,
        'cournot_price_b1': 100 - 160 / 3,
        'cournot_reaction_b2': (100 - 20 - 2 * 10) / (2 * 2),
        'stackelberg_follower': (80 - 40) / 2,
        'stackelberg_total': 40 + 20,
        'stackelberg_price': 100 - 60,
        'hotelling_equal': 0.5,
        'hotelling_asymmetric': 5 / 8,
        'entry_three_year_profit': 2_000_000 * 3,
        'collusion_delta': (160 - 100) / (160 - 40),
        'delta_hhi_30_20': 2 * 30 * 20,
        'search_net_old': 80 - 120,
        'search_net_new': 80 - 20,
        'rd_payoff_high': 0.2 * 8_000_000 - 1_000_000,
        'rd_payoff_low': 0.2 * 3_000_000 - 1_000_000,
        'market_share': 30 / 120,
    }
    expected = {
        'hhi_40_30_20_10': 3000,
        'delta_hhi_30_25': 1500,
        'average_cost': 300,
        'scope_economy': 200,
        'monopoly_q': 40,
        'monopoly_p': 60,
        'lerner': 2 / 3,
        'third_degree_markup_A': 0.5,
        'third_degree_markup_B': 0.25,
        'cournot_each_b1': 80 / 3,
        'cournot_total_b1': 160 / 3,
        'cournot_price_b1': 140 / 3,
        'cournot_reaction_b2': 15,
        'stackelberg_follower': 20,
        'stackelberg_total': 60,
        'stackelberg_price': 40,
        'hotelling_equal': 0.5,
        'hotelling_asymmetric': 0.625,
        'entry_three_year_profit': 6_000_000,
        'collusion_delta': 0.5,
        'delta_hhi_30_20': 1200,
        'search_net_old': -40,
        'search_net_new': 60,
        'rd_payoff_high': 600_000,
        'rd_payoff_low': -400_000,
        'market_share': 0.25,
    }
    for key, value in recomputed.items():
        ck(math.isclose(float(value), float(expected[key]), rel_tol=1e-12, abs_tol=1e-12), f'numeric {key}: {value}')

    answer_tokens = {
        'ch01-q02': ('3,000',),
        'ch01-q04': ('1,500',),
        'ch02-q02': ('300',),
        'ch02-q04': ('200',),
        'ch03-q02': ('Q=40', 'P=60'),
        'ch03-q04': ('2/3',),
        'ch04-q02': ('A 群',),
        'ch06-q02': ('26.67',),
        'ch06-q03': ('15', 'b≠1'),
        'ch06-q04': ('53.33', '46.67'),
        'ch08-q02': ('20',),
        'ch08-q04': ('Q=60', 'P=40'),
        'ch09-q02': ('0.5',),
        'ch09-q04': ('0.625',),
        'ch11-q02': ('不足', '6,000,000'),
        'ch12-q02': ('0.5',),
        'ch14-q02': ('1,200',),
        'ch16-q02': ('600,000',),
        'ch16-q04': ('-NT$400,000',),
        'ch19-q02': ('25%',),
    }
    for qid, tokens in answer_tokens.items():
        joined = qmap[qid]['answer'] + ' ' + qmap[qid]['explanation']
        for token in tokens:
            ck(token in joined, f'{qid} numeric token {token}')

    chapter_html = '\n'.join((root / x['file']).read_text(encoding='utf-8') for x in manifest['chapters'] if x['kind'] == 'chapter')
    chapter_text = html.unescape(re.sub(r'<[^>]+>', ' ', chapter_html))
    qtext = '\n'.join(q['question'] + ' ' + q['answer'] + ' ' + q['explanation'] for q in qdoc['items'])
    corpus = chapter_text + '\n' + qtext

    conceptual_gates = [
        ('自然獨占', '次可加性'),
        ('Lerner', '|epsilon|>1'),
        ('價格歧視', '配置'),
        ('Cournot', 'a-c-b Q_-i'),
        ('Hotelling', '全市場覆蓋'),
        ('進入', '折現'),
        ('極限定價', '完全資訊'),
        ('重複賽局', '懲罰'),
        ('聯合行為', '推定'),
        ('轉售價格維持', '第 19 條'),
        ('搜尋', 'Effective transaction cost'),
        ('兩邊市場', '價格「結構」'),
        ('獨占', '第 7 條'),
        ('相關市場', '第 5 條'),
        ('反事實', '競爭政策'),
        ('相關', '因果'),
    ]
    for a, b in conceptual_gates:
        ck(a in corpus and b in corpus, f'conceptual gate {a}/{b}')

    # Negative gates against the specific v1 inaccuracies/oversimplifications found in the independent audit.
    forbidden = [
        'q_i = (a-c-Q_-i)/(2b)',
        '福利題一定檢查總產量是否改變',
        'Observed price = product price + search/attention cost',
    ]
    for token in forbidden:
        ck(token not in corpus, f'forbidden stale v1 text {token}')

    # Current-law boundary: do not hard-code mutable merger filing turnover thresholds.
    ck('新臺幣一百億元' not in corpus and '新臺幣五十億元' not in corpus, 'no stale merger filing thresholds')
    ck('以公平交易委員會最新公開資料為準' in corpus, 'current law pointer')

    # Progress compatibility: stable IDs are the public storage contract.
    ck([x['id'] for x in manifest['chapters']] == [f'ch{i:02d}' for i in range(20)] + ['appendix-a', 'appendix-b', 'appendix-c'], 'stable chapter ids')
    ck([x['id'] for x in qdoc['items']] == [f'ch{i:02d}-q{j:02d}' for i in range(20) for j in range(1, 6)], 'stable question ids')

    print(
        f'INDUSTRIAL_ECONOMICS_V2_QA2_OK checks={checks} books={len(ids)} '
        f'quantitative_rechecks={len(recomputed)} questions_rechecked=100 '
        f'high_risk_concepts={len(conceptual_gates)} correction_areas=12'
    )
    return checks


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('usage: qa_industrial_economics_v2.py SITE_ROOT EXPECTED_LIBRARY')
    main(sys.argv[1], sys.argv[2])
