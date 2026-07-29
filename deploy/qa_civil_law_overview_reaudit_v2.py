#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

BOOK = 'civil-law-overview'
VERSION = '2026.07.30-2'
checks = 0


def ck(condition, message):
    global checks
    checks += 1
    if not condition:
        raise AssertionError(message)


def main(site_root: str, expected_library: str) -> None:
    site = Path(site_root)
    root = site / 'books' / BOOK
    manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    questions = json.loads((root / 'questions.json').read_text(encoding='utf-8'))
    search = json.loads((root / 'search.json').read_text(encoding='utf-8'))
    library = json.loads((site / 'data/library.json').read_text(encoding='utf-8'))

    ck(library['version'] == expected_library, 'library version')
    ck([b['id'] for b in library['books']].count(BOOK) == 1, 'one civil book')
    ck(manifest['version'] == questions['version'] == VERSION, 'civil v2 version')
    ck(manifest['updatedAt'] == '2026-07-30', 'updatedAt')

    chapters = [x for x in manifest['chapters'] if x.get('kind') == 'chapter']
    appendices = [x for x in manifest['chapters'] if x.get('kind') == 'appendix']
    ck(len(chapters) == 20, '20 chapters')
    ck(len(appendices) == 3, '3 appendices')
    ck([x['id'] for x in chapters] == [f'ch{i:02d}' for i in range(20)], 'chapter IDs unchanged')
    ck(questions['count'] == len(questions['items']) == 100, '100 questions')
    ck(len({x['id'] for x in questions['items']}) == 100, 'unique question IDs')
    ck(Counter(x['chapterId'] for x in questions['items']) == {f'ch{i:02d}': 5 for i in range(20)}, 'five questions each')
    ck(len(search['entries']) == 150, '150 search entries')
    ck(len(list((site / 'assets/civil-law-overview-svg').glob('*.svg'))) == 20, '20 SVGs')

    for ch in manifest['chapters']:
        p = root / ch['file']
        ck(p.is_file() and p.stat().st_size > 500, f'chapter file {ch["id"]}')
        text = p.read_text(encoding='utf-8')
        ck('<script' not in text.lower(), f'no script {ch["id"]}')

    corpus = '\n'.join((root / x['file']).read_text(encoding='utf-8') for x in manifest['chapters'])
    compact = ' '.join(corpus.split())

    legal_gates = {
        'art130': ['民法第 130 條', '請求後 6 個月內不起訴', '視為不中斷'],
        'debt_assumption': ['民法第 300、301 條', '非經債權人承認'],
        'sale_354_360': ['民法第 354 條', '減少程度無關重要者', '民法第 360 條', '故意不告知瑕疵'],
        'employment_482': ['民法第 482 條', '一定或不定期限內服勞務'],
        'motor_191_2': ['民法第 191-2 條', '動力車輛', '已盡相當注意'],
        'good_faith_801_948': ['民法第 801、948 條', '無重大過失', '取得所有權'],
        'coownership_819_820': ['民法第 819 條', '共有物整體的處分、變更及設定負擔', '全體共有人同意', '民法第 820 條'],
        'marital_property_1030_1': ['民法第 1030-1 條', '繼承或其他無償取得', '慰撫金'],
        'divorce_constitutional': ['112 年憲判字第 4 號', '2025-03-24', '顯然過苛', '法院對此等個案應依該判決意旨裁判'],
        'renunciation_notice': ['民法第 1174 條', '書面通知因其拋棄而成為繼承人的人', '不能通知者例外'],
        'forced_share_current': ['民法第 1223 條（2026-07-30 現行法）', '兄弟姊妹與祖父母為其應繼分三分之一', '2026-06-02', '仍只是草案'],
        'article_166_1': ['民法第 166-1 條', '施行日期尚未另定'],
    }
    for gate, tokens in legal_gates.items():
        for token in tokens:
            ck(token in compact, f'{gate} missing {token}')

    # These are only phrases that would be wrong even without surrounding context.
    # Do not blacklist wording that may legitimately appear inside a warning such as
    # 「不得誤解成……已全面失效」.
    forbidden = [
        '兄弟姊妹已無特留分',
        '兄弟姊妹沒有特留分',
        '修法期限尚未屆滿',
        '使有效契約關係依法溯及消滅並發生回復原狀等效果',
        '共有物整體處分適用共有人過半數且應有部分過半數',
    ]
    for phrase in forbidden:
        ck(phrase not in compact, f'forbidden stale/misleading phrase: {phrase}')

    qmap = {x['id']: x for x in questions['items']}
    expected_question_tokens = {
        'ch05-q04': ['6 個月內不起訴', '視為不中斷'],
        'ch08-q04': ['第 300 條', '第 301 條', '債權人承認'],
        'ch10-q05': ['第 360 條', '不履行之損害賠償'],
        'ch11-q05': ['僱傭', '承攬', '第 482 條'],
        'ch12-q05': ['第 191-2 條', '已盡相當注意'],
        'ch13-q04': ['第 948 條', '第 801 條', '取得所有權'],
        'ch14-q03': ['第 819 條', '全體共有人同意'],
        'ch17-q03': ['112 年憲判字第 4 號', '2025-03-24', '顯然過苛'],
        'ch19-q03': ['3 個月內', '書面向法院', '書面通知', '不能通知者例外'],
    }
    for qid, tokens in expected_question_tokens.items():
        ck(qid in qmap, f'question exists {qid}')
        joined = qmap[qid]['question'] + ' ' + qmap[qid]['answer'] + ' ' + qmap[qid]['explanation']
        for token in tokens:
            ck(token in joined, f'{qid} missing {token}')

    ck(qmap['ch17-q03']['answer'].startswith('不是。'), 'divorce answer rejects absolute bar')
    ck('沒有把第 1052 條第 2 項但書全面宣告失效' in qmap['ch17-q03']['explanation'], 'constitutional nuance')
    ck('原則應以書面通知' in qmap['ch19-q03']['answer'], 'renunciation notice answer')

    search_corpus = '\n'.join(e['title'] + ' ' + e['text'] for e in search['entries']).replace(' ', '')
    for token in ['民法第130條', '第191-2條', '第819條', '112年憲判字第4號', '2025-03-24', '2026-06-02草案', '第801條與第948條']:
        ck(token in search_corpus, f'search contains {token}')

    release = manifest.get('releaseNotes', [])[0]
    ck(release.get('version') == VERSION, 'release note v2')
    ck(release.get('title') == '第二次獨立內容複核與糾錯', 'release note title')
    ck('章節 ID、題目 ID、題數與進度儲存鍵均不變' in release.get('progressImpact', ''), 'progress compatibility')

    sw = (site / 'sw.js').read_text(encoding='utf-8')
    ck(f"study-library-{expected_library}" in sw, 'service worker library version')

    print(
        f'CIVIL_LAW_REAUDIT_V2_OK checks={checks} legal_gates={len(legal_gates)} '
        f'question_corrections={len(expected_question_tokens)} chapters=20 appendices=3 questions=100 search=150 figures=20'
    )


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('usage: python deploy/qa_civil_law_overview_reaudit_v2.py SITE_ROOT EXPECTED_LIBRARY')
    main(sys.argv[1], sys.argv[2])
