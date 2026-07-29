#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
from collections import Counter
from pathlib import Path

BOOK = 'game-theory'
VERSION = '2026.07.29-1'
REQUIRED_PRE_IDS = {
    'calculus', 'accounting', 'economics', 'statistics', 'commercial-law',
    'cost-accounting', 'microeconomics', 'intermediate-accounting', 'macroeconomics',
    'international-economics', 'public-finance', 'money-banking',
}
checks = 0


def ck(cond, msg):
    global checks
    checks += 1
    if not cond:
        raise AssertionError(msg)


def main(arg):
    site = Path(arg)
    expected_library_version = os.environ.get('EXPECTED_LIBRARY_VERSION')
    pre_library_path = os.environ.get('PRE_LIBRARY_JSON')
    if not expected_library_version or not pre_library_path:
        raise SystemExit('EXPECTED_LIBRARY_VERSION and PRE_LIBRARY_JSON are required')

    pre = json.loads(Path(pre_library_path).read_text(encoding='utf-8'))
    lib = json.loads((site / 'data/library.json').read_text(encoding='utf-8'))
    pre_ids = [book['id'] for book in pre['books']]
    post_ids = [book['id'] for book in lib['books']]
    ck(REQUIRED_PRE_IDS.issubset(set(pre_ids)), f'missing prerequisite books: {pre_ids}')
    ck(BOOK not in pre_ids, 'game-theory already existed before generation')
    ck(post_ids == pre_ids + [BOOK], f'book order drift: before={pre_ids}, after={post_ids}')
    ck(lib['version'] == expected_library_version, 'library version')

    entry = lib['books'][-1]
    ck(entry['id'] == BOOK, 'library entry id')
    ck(entry.get('title') == '賽局理論及應用', 'library entry title')
    ck('Nash' in entry.get('subtitle','') and '資訊不完全' in entry.get('subtitle',''), 'library entry subtitle')
    ck(entry.get('cover') == '局', 'library cover')
    ck(entry.get('status') == 'available', 'library status')

    for existing_id in pre_ids:
        existing_root = site / 'books' / existing_id
        manifest = json.loads((existing_root / 'manifest.json').read_text(encoding='utf-8'))
        questions = json.loads((existing_root / 'questions.json').read_text(encoding='utf-8'))
        search = json.loads((existing_root / 'search.json').read_text(encoding='utf-8'))
        ck(manifest['id'] == existing_id, f'existing manifest id {existing_id}')
        ck(questions['count'] == len(questions['items']) > 0, f'existing questions {existing_id}')
        ck(bool(search['entries']), f'existing search {existing_id}')

    root = site / 'books' / BOOK
    manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    questions = json.loads((root / 'questions.json').read_text(encoding='utf-8'))
    search = json.loads((root / 'search.json').read_text(encoding='utf-8'))
    ck(manifest['id'] == BOOK, 'manifest id')
    ck(manifest['title'] == '賽局理論及應用', 'manifest title')
    ck(manifest['cover'] == '局', 'manifest cover')
    ck(manifest.get('accent') == entry.get('accent'), 'manifest/library accent')
    ck(manifest['version'] == questions['version'] == VERSION, 'book version')
    ck(questions.get('bookId') == BOOK, 'questions book id')
    chapters = [x for x in manifest['chapters'] if x['kind'] == 'chapter']
    appendices = [x for x in manifest['chapters'] if x['kind'] == 'appendix']
    ck(len(chapters) == 20, 'chapter count')
    ck([x['id'] for x in chapters] == [f'ch{i:02d}' for i in range(20)], 'chapter ids')
    ck([x.get('number') for x in chapters] == [str(i) for i in range(20)], 'chapter display numbers')
    ck(len(appendices) == 3, 'appendix count')
    ck([x.get('number') for x in appendices] == ['A','B','C'], 'appendix display numbers')
    ck(questions['count'] == 100 == len(questions['items']), 'question count')
    ck(Counter(q['chapterId'] for q in questions['items']) == {f'ch{i:02d}': 5 for i in range(20)}, 'five questions each chapter')
    ck(len({q['id'] for q in questions['items']}) == 100, 'unique question ids')
    ck(Counter(q.get('difficulty') for q in questions['items']) == {'基礎':20,'標準':40,'綜合':20,'陷阱':20}, 'difficulty distribution')
    ck(len(search['entries']) == 189, f'search count {len(search["entries"])}')

    ids = {x['id'] for x in manifest['chapters']}
    chapter_title_map = {x['id']: x['title'] for x in chapters}
    for q in questions['items']:
        ck(q['chapterId'] in chapter_title_map, f'question chapter {q["id"]}')
        for field in ('id','bookId','chapterId','chapterTitle','topic','difficulty','question','answer','explanation','source'):
            ck(bool(str(q.get(field,'')).strip()), f'question field {q["id"]} {field}')
        ck(q['bookId'] == BOOK, f'question book id {q["id"]}')
        ck(chapter_title_map[q['chapterId']] in q['chapterTitle'], f'question chapter title {q["id"]}')
        ck(q['source'] == '本書自編標準題型', f'question source {q["id"]}')

    expected = {
        'ch04-q03':'q=0.4。', 'ch04-q04':'p=0.6。',
        'ch05-q02':'-1 與 -2。', 'ch05-q03':'-1。',
        'ch06-q03':'30。', 'ch06-q04':'總產量60，價格40。',
        'ch07-q02':'Accommodate。', 'ch07-q03':'In。',
        'ch08-q04':'值得，若其他條件如題。',
        'ch09-q02':'約0.5263。', 'ch09-q03':'約 NT$52.63。', 'ch09-q04':'NT$50 與 NT$50。',
        'ch10-q01':'δ≥0.5。', 'ch10-q02':'15。', 'ch10-q03':'9。',
        'ch11-q02':'0.8。', 'ch11-q03':'-0.4。',
        'ch12-q01':'0.6。', 'ch12-q02':'出價 NT$100 者得標，支付 NT$80。',
        'ch13-q02':'1。', 'ch13-q03':'6/7，約0.8571。',
        'ch14-q02':'7.9。', 'ch14-q03':'3.7。', 'ch14-q04':'5.5，會想模仿。',
        'ch15-q02':'20。', 'ch15-q03':'25；不是 IC。', 'ch15-q04':'H=30，L=-20。',
        'ch16-q02':'給價值 NT$100 的玩家。', 'ch16-q03':'NT$80。', 'ch16-q04':'NT$20。',
        'ch17-q02':'x1+x2+x3=90。', 'ch17-q03':'至少60。', 'ch17-q04':'(30,30,30)。',
        'ch18-q03':'5。',
    }
    qmap = {q['id']:q for q in questions['items']}
    for qid, ans in expected.items():
        ck(qmap[qid]['answer'] == ans, f'{qid}: {qmap[qid]["answer"]!r} != {ans!r}')
    ck(qmap['ch17-q05']['answer'] == '不一定。', 'Shapley/core trap answer')

    text_all = []
    for ch in manifest['chapters']:
        path = root / ch['file']
        ck(path.is_file() and path.stat().st_size > 700, f'chapter file {ch["id"]}')
        text = path.read_text(encoding='utf-8')
        text_all.append(text)
        ck('\f' not in text and '\t' not in text, f'control chars {ch["id"]}')
        ck('<script' not in text.lower(), f'no inline script {ch["id"]}')
        if ch['kind'] == 'chapter':
            for token in ['白話直覺','正式定義與核心概念','核心公式與成立條件','完整標準例題','常見錯誤','考試判斷方法','理解檢查']:
                ck(token in text, f'{ch["id"]} missing {token}')
            ck('loading="lazy"' in text and 'assets/game-theory-svg/' in text, f'figure markup {ch["id"]}')

    full = '\n'.join(text_all)
    for token in [
        '最佳回應', '嚴格優勢', '合理化', 'Nash 均衡', '混合策略', 'minimax',
        'Cournot', 'Bertrand', '向後歸納', '子賽局完美', '可信威脅', 'Rubinstein',
        '重複賽局', 'grim trigger', 'Bayesian Nash', '第一價拍賣', '第二價拍賣',
        'Perfect Bayesian', '序列理性', '分離均衡', '混同均衡', '篩選', 'cheap talk',
        '揭示原理', 'VCG', 'core', 'Shapley', '擁擠賽局',
    ]:
        ck(token in full, f'missing core token {token}')

    titles = '|'.join(ch['title'] for ch in chapters)
    for excluded in [
        'Global Games 的完整證明', 'PPAD 複雜度', 'Myerson optimal auction',
        'Implementation Theory 的完整證明', '微分賽局',
    ]:
        ck(excluded not in titles, f'advanced topic promoted to core chapter: {excluded}')

    for overclaim in [
        'Nash 均衡一定有效率',
        'Nash 均衡一定是唯一的',
        '弱劣勢策略的刪除順序永遠不影響結果',
        'minimax theorem 適用於所有賽局',
        '第二價拍賣在任何資訊環境都應誠實出價',
        '有限次重複賽局一定可以靠未來懲罰維持合作',
    ]:
        ck(overclaim not in full, f'forbidden overclaim {overclaim}')
    ck('一般賽局不保證' in full, 'Shapley/core caveat')
    ck('NT$' in full, 'TWD examples')
    ck('SPNE ⇒ NE' in full, 'SPNE implication')
    ck('型態映到行動' in full or '型態到行動' in full, 'Bayesian strategy mapping')

    figures = sorted((site / 'assets/game-theory-svg').glob('*.svg'))
    ck(len(figures) == 20, 'figure count')
    for figure in figures:
        svg = figure.read_text(encoding='utf-8')
        ck('<title' in svg and '<desc' in svg and 'viewBox=' in svg, f'svg accessibility {figure.name}')
        ck('href="http' not in svg and "href='http" not in svg, f'no remote svg asset {figure.name}')

    for entry_search in search['entries']:
        ck(entry_search['chapterId'] in ids, 'search chapter id')
        ck(bool(entry_search['title'].strip()) and bool(entry_search['text'].strip()), 'search nonempty')
        ck(isinstance(entry_search['page'], int) and entry_search['page'] >= 0, 'search page')

    sw = (site / 'sw.js').read_text(encoding='utf-8')
    for token in [
        f"study-library-{expected_library_version}",
        './books/game-theory/manifest.json', './books/game-theory/questions.json', './books/game-theory/search.json',
        './books/game-theory/chapters/ch19.html', './books/game-theory/chapters/appendix-c.html',
        './assets/game-theory-svg/modeling-solution-concepts.svg',
    ]:
        ck(token in sw, f'sw cache {token}')

    raw = json.dumps({'manifest':manifest,'questions':questions,'search':search}, ensure_ascii=False)
    ck('money-banking' not in raw, 'template id leakage')
    ck(manifest.get('releaseNotes') and manifest['releaseNotes'][0]['version'] == VERSION, 'release notes')

    print(
        f'GAME_THEORY_QA_OK checks={checks} books={len(post_ids)} '
        f'library={expected_library_version} chapters=20 appendices=3 '
        f'questions=100 search=189 figures=20 numeric_rechecks={len(expected)}'
    )


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: python deploy/validate_game_theory.py SITE_ROOT')
    main(sys.argv[1])
