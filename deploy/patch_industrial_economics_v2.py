#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

from generate_industrial_economics import (
    ACCENT,
    BOOK,
    COVER,
    SUBTITLE,
    TITLE,
    appendix_a,
    appendix_b,
    appendix_c,
    chapter_html,
    jdump,
    render_svg,
    search_entries,
)
from industrial_economics_content_v2 import CHAPTERS, VERSION
from industrial_economics_questions_v2 import build_questions

UPDATED_AT = '2026-07-30'
DIFFICULTY_BY_SLOT = {'q01': '基礎', 'q02': '標準', 'q03': '標準', 'q04': '進階', 'q05': '進階'}


def main(site_root: str) -> None:
    site = Path(site_root)
    root = site / 'books' / BOOK
    if not root.is_dir():
        raise AssertionError(f'missing deployed book: {BOOK}')

    manifest_path = root / 'manifest.json'
    questions_path = root / 'questions.json'
    search_path = root / 'search.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    questions_doc = json.loads(questions_path.read_text(encoding='utf-8'))

    old_chapter_ids = [x['id'] for x in manifest['chapters']]
    old_question_ids = [x['id'] for x in questions_doc['items']]
    expected_chapter_ids = [f'ch{i:02d}' for i in range(20)] + ['appendix-a', 'appendix-b', 'appendix-c']
    if old_chapter_ids != expected_chapter_ids:
        raise AssertionError(f'chapter id drift before v2 patch: {old_chapter_ids}')
    if old_question_ids != [f'ch{i:02d}-q{j:02d}' for i in range(20) for j in range(1, 6)]:
        raise AssertionError('question id drift before v2 patch')

    chapter_meta = []
    chapter_titles = {}
    figdir = site / 'assets/industrial-economics-svg'
    figdir.mkdir(parents=True, exist_ok=True)

    for ch in CHAPTERS:
        number = str(int(ch['id'][2:]))
        rel = f'chapters/{ch["id"]}.html'
        (root / rel).write_text(chapter_html(ch), encoding='utf-8')
        (figdir / f'{ch["slug"]}.svg').write_text(render_svg(ch), encoding='utf-8')
        chapter_meta.append({'id': ch['id'], 'number': number, 'title': ch['title'], 'file': rel, 'kind': 'chapter'})
        chapter_titles[ch['id']] = f'第 {number} 章 {ch["title"]}'

    appendices = [
        ('appendix-a', 'A', '核心公式與模型速查', 'chapters/appendix-a.html', appendix_a(CHAPTERS)),
        ('appendix-b', 'B', '產業經濟學解題路線', 'chapters/appendix-b.html', appendix_b()),
        ('appendix-c', 'C', '中英名詞對照', 'chapters/appendix-c.html', appendix_c()),
    ]
    for cid, number, title, rel, body in appendices:
        (root / rel).write_text(body, encoding='utf-8')
        chapter_meta.append({'id': cid, 'number': number, 'title': title, 'file': rel, 'kind': 'appendix'})

    manifest.update({
        'id': BOOK,
        'title': TITLE,
        'subtitle': SUBTITLE,
        'version': VERSION,
        'cover': COVER,
        'accent': ACCENT,
        'updatedAt': UPDATED_AT,
        'chapters': chapter_meta,
        'features': {'reader': True, 'quiz': True, 'formula': True},
    })
    release_notes = [x for x in manifest.get('releaseNotes', []) if x.get('version') != VERSION]
    manifest['releaseNotes'] = [{
        'version': VERSION,
        'date': UPDATED_AT,
        'title': '第二次獨立內容複核與糾錯',
        'changes': [
            '修正 Cournot 一般線性需求最佳反應函數遺漏的 b 係數',
            '修正價格歧視福利判斷：總產量不是唯一條件，跨市場配置也會影響總剩餘',
            '將進入決策改為折現現值與沉沒進入成本比較，修正流量與存量直接比較問題',
            '補強自然獨占次可加性、Lerner 彈性區段、Hotelling 全市場覆蓋／內點條件',
            '補強重複賽局懲罰條件、台灣公平交易法第 14 條推定合意與第 19 條限制轉售價格制度銜接',
            '修正搜尋章 observed price 用語，並強化兩邊平台價格結構的定義',
        ],
        'progressImpact': 'Book ID、20 個章節 ID、3 個附錄 ID、100 個題目 ID 均未變；既有閱讀進度與錯題紀錄可沿用。',
    }] + release_notes
    manifest_path.write_text(jdump(manifest), encoding='utf-8')

    raw_questions = build_questions()
    qitems = []
    for src in raw_questions:
        slot = src['id'].rsplit('-', 1)[-1]
        qitems.append({
            'id': src['id'],
            'bookId': BOOK,
            'chapterId': src['chapterId'],
            'chapterTitle': chapter_titles[src['chapterId']],
            'topic': next(ch['title'] for ch in CHAPTERS if ch['id'] == src['chapterId']),
            'difficulty': DIFFICULTY_BY_SLOT[slot],
            'question': src['question'],
            'answer': src['answer'],
            'explanation': src['explanation'],
            'source': '本書自編標準題型；v2 經第二次獨立內容複核',
        })
    questions_doc['bookId'] = BOOK
    questions_doc['version'] = VERSION
    questions_doc['count'] = len(qitems)
    questions_doc['items'] = qitems
    questions_path.write_text(jdump(questions_doc), encoding='utf-8')

    entries = search_entries(CHAPTERS)
    search_path.write_text(jdump({'entries': entries}), encoding='utf-8')

    final_manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    final_questions = json.loads(questions_path.read_text(encoding='utf-8'))
    if [x['id'] for x in final_manifest['chapters']] != old_chapter_ids:
        raise AssertionError('chapter ids changed by v2 patch')
    if [x['id'] for x in final_questions['items']] != old_question_ids:
        raise AssertionError('question ids changed by v2 patch')
    if final_manifest['version'] != VERSION or final_questions['version'] != VERSION:
        raise AssertionError('v2 content version not applied')
    if len(entries) != 150 or len(list(figdir.glob('*.svg'))) != 20:
        raise AssertionError('v2 artifact counts drift')

    print(json.dumps({
        'book': BOOK,
        'version': VERSION,
        'chapters': 20,
        'appendices': 3,
        'questions': len(qitems),
        'search': len(entries),
        'figures': 20,
        'chapter_ids_preserved': True,
        'question_ids_preserved': True,
    }, ensure_ascii=False))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: python deploy/patch_industrial_economics_v2.py SITE_ROOT')
    main(sys.argv[1])
