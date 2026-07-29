#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

import generate_mathematical_economics as legacy
from mathematical_economics_v2_corrections import CHAPTERS_V2, UPDATED_AT, VERSION
from mathematical_economics_v2_questions import build_questions_v2

BOOK = 'mathematical-economics'
TITLE = '數理經濟學'
SUBTITLE = '函數・矩陣・微積分・比較靜態・最佳化與動態系統'
COVER = '數'
ACCENT = '#7c3aed'
DIFFICULTY = legacy.DIFFICULTY


def jdump(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + '\n'


def main(site_root: str) -> None:
    site = Path(site_root)
    library_path = site / 'data/library.json'
    library = json.loads(library_path.read_text(encoding='utf-8'))
    ids = [b['id'] for b in library['books']]
    if BOOK in ids:
        raise AssertionError(f'{BOOK} already exists; use an in-place v2 patch instead of appending')
    if not ids:
        raise AssertionError('empty formal library')
    anchor = ids[-1]

    legacy.CHAPTERS = CHAPTERS_V2
    legacy.VERSION = VERSION
    legacy.UPDATED_AT = UPDATED_AT

    library['books'].append({
        'id': BOOK,
        'title': TITLE,
        'subtitle': SUBTITLE,
        'manifest': f'books/{BOOK}/manifest.json',
        'cover': COVER,
        'accent': ACCENT,
        'status': 'available',
    })
    library_path.write_text(jdump(library), encoding='utf-8')

    root = site / 'books' / BOOK
    (root / 'chapters').mkdir(parents=True, exist_ok=False)
    figure_dir = site / 'assets/mathematical-economics-svg'
    figure_dir.mkdir(parents=True, exist_ok=False)

    meta = []
    titles = {}
    for chapter in CHAPTERS_V2:
        number = str(int(chapter['id'][2:]))
        rel = f'chapters/{chapter["id"]}.html'
        (root / rel).write_text(legacy.chapter_html(chapter), encoding='utf-8')
        (figure_dir / f'{chapter["slug"]}.svg').write_text(legacy.render_svg(chapter), encoding='utf-8')
        meta.append({'id': chapter['id'], 'number': number, 'title': chapter['title'], 'file': rel, 'kind': 'chapter'})
        titles[chapter['id']] = f'第 {number} 章 {chapter["title"]}'

    appendices = [
        ('appendix-a', 'A', '核心公式速查', 'chapters/appendix-a.html', legacy.appendix_a()),
        ('appendix-b', 'B', '數理經濟學解題路線', 'chapters/appendix-b.html', legacy.appendix_b()),
        ('appendix-c', 'C', '中英名詞與符號對照', 'chapters/appendix-c.html', legacy.appendix_c()),
    ]
    for cid, number, title, rel, body in appendices:
        (root / rel).write_text(body, encoding='utf-8')
        meta.append({'id': cid, 'number': number, 'title': title, 'file': rel, 'kind': 'appendix'})

    manifest = {
        'id': BOOK,
        'title': TITLE,
        'subtitle': SUBTITLE,
        'version': VERSION,
        'cover': COVER,
        'accent': ACCENT,
        'features': {'reader': True, 'quiz': True, 'formula': True},
        'updatedAt': UPDATED_AT,
        'chapters': meta,
        'releaseNotes': [{
            'version': VERSION,
            'date': UPDATED_AT,
            'title': '第二次獨立內容審計與糾錯版',
            'changes': [
                '修正 KKT 必要條件的 constraint qualification 前提與充分性敘述',
                '修正 homothetic、特徵向量與全微分等定義精度',
                '移除彈性章自相矛盾公式，補上 Cobb–Douglas 對數微分',
                '補入鏈鎖律、凹性／擬凹性、受限制二階條件與 constrained envelope theorem',
                '強化差分／微分方程邊界穩定性與線性化失效情形',
                '調整 11 題高風險題庫題幹、答案或解析',
            ],
            'progressImpact': '保留 20 章、3 附錄、100 題及所有既有章節／題目 ID；僅提升內容正確性與完整性。',
        }],
    }
    (root / 'manifest.json').write_text(jdump(manifest), encoding='utf-8')

    qitems = []
    for source in build_questions_v2():
        slot = source['id'].rsplit('-', 1)[-1]
        qitems.append({
            'id': source['id'],
            'bookId': BOOK,
            'chapterId': source['chapterId'],
            'chapterTitle': titles[source['chapterId']],
            'topic': next(c['title'] for c in CHAPTERS_V2 if c['id'] == source['chapterId']),
            'difficulty': DIFFICULTY[slot],
            'question': source['question'],
            'answer': source['answer'],
            'explanation': source['explanation'],
            'source': '本書自編標準題型・第二次內容審計版',
        })
    (root / 'questions.json').write_text(jdump({'bookId': BOOK, 'version': VERSION, 'count': len(qitems), 'items': qitems}), encoding='utf-8')

    entries = legacy.search_entries()
    (root / 'search.json').write_text(jdump({'entries': entries}), encoding='utf-8')

    cache = [
        f'./books/{BOOK}/manifest.json',
        f'./books/{BOOK}/questions.json',
        f'./books/{BOOK}/search.json',
        *[f'./books/{BOOK}/{x["file"]}' for x in meta],
        *[f'./assets/mathematical-economics-svg/{c["slug"]}.svg' for c in CHAPTERS_V2],
    ]
    sw_path = site / 'sw.js'
    sw_path.write_text(legacy.append_sw_assets(sw_path.read_text(encoding='utf-8'), anchor, cache), encoding='utf-8')

    print(json.dumps({
        'book': BOOK,
        'version': VERSION,
        'chapters': 20,
        'appendices': 3,
        'questions': 100,
        'search': 150,
        'figures': 20,
        'pre_books': len(ids),
        'post_books': len(ids) + 1,
        'anchor': anchor,
    }, ensure_ascii=False), file=sys.stderr)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: python deploy/generate_mathematical_economics_v2.py SITE_ROOT')
    main(sys.argv[1])
