#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

from generate_game_theory import (
    ACCENT,
    BOOK,
    CHAPTERS,
    COVER,
    DIFFICULTY_BY_SLOT,
    QUESTIONS,
    SUBTITLE,
    TITLE,
    UPDATED_AT,
    VERSION,
    appendix_a,
    appendix_b,
    appendix_c,
    chapter_html,
    jdump,
    render_svg,
    search_entries,
)

SOURCE_VERSION = '2026.07.29-1'
TARGET_VERSION = VERSION


def main(site_root: str) -> None:
    site = Path(site_root)
    root = site / 'books' / BOOK
    figdir = site / 'assets/game-theory-svg'
    library_path = site / 'data/library.json'
    if not root.is_dir() or not library_path.is_file():
        raise AssertionError('formal game-theory artifact missing')

    manifest_path = root / 'manifest.json'
    questions_path = root / 'questions.json'
    search_path = root / 'search.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    qdoc = json.loads(questions_path.read_text(encoding='utf-8'))
    library = json.loads(library_path.read_text(encoding='utf-8'))

    if manifest.get('id') != BOOK or qdoc.get('bookId') != BOOK:
        raise AssertionError('game-theory identity drift')
    if manifest.get('version') not in {SOURCE_VERSION, TARGET_VERSION}:
        raise AssertionError(f'unexpected source version: {manifest.get("version")}')
    if qdoc.get('version') not in {SOURCE_VERSION, TARGET_VERSION}:
        raise AssertionError(f'unexpected question source version: {qdoc.get("version")}')
    if [b['id'] for b in library['books']].count(BOOK) != 1:
        raise AssertionError('game-theory registry count drift')

    figdir.mkdir(parents=True, exist_ok=True)
    chapter_titles: dict[str, str] = {}
    expected_chapter_ids: list[str] = []
    for ch in CHAPTERS:
        number = str(int(ch['id'][2:]))
        expected_chapter_ids.append(ch['id'])
        chapter_titles[ch['id']] = f'第 {number} 章 {ch["title"]}'
        path = root / 'chapters' / f'{ch["id"]}.html'
        path.write_text(chapter_html(ch), encoding='utf-8')
        (figdir / f'{ch["slug"]}.svg').write_text(render_svg(ch), encoding='utf-8')

    appendix_files = {
        'appendix-a': appendix_a(CHAPTERS),
        'appendix-b': appendix_b(),
        'appendix-c': appendix_c(),
    }
    for appendix_id, body in appendix_files.items():
        (root / 'chapters' / f'{appendix_id}.html').write_text(body, encoding='utf-8')

    chapter_ids = [x['id'] for x in manifest.get('chapters', []) if x.get('kind') == 'chapter']
    appendix_ids = [x['id'] for x in manifest.get('chapters', []) if x.get('kind') == 'appendix']
    if chapter_ids != expected_chapter_ids or appendix_ids != ['appendix-a','appendix-b','appendix-c']:
        raise AssertionError('manifest chapter structure drift')

    manifest['title'] = TITLE
    manifest['subtitle'] = SUBTITLE
    manifest['version'] = TARGET_VERSION
    manifest['updatedAt'] = UPDATED_AT
    manifest['cover'] = COVER
    manifest['accent'] = ACCENT
    old_notes = [n for n in manifest.get('releaseNotes', []) if n.get('version') != TARGET_VERSION]
    manifest['releaseNotes'] = [{
        'version': TARGET_VERSION,
        'date': UPDATED_AT,
        'title': '第二次內容審稿：資訊結構、動態均衡與條件精度修正',
        'changes': [
            '更正向後歸納的標準條件為有限完美資訊，並分清 complete information 與 perfect information',
            '修正混合策略例題，明示同一協調賽局可同時有純策略與混合策略 Nash',
            '補強 Bayesian 動態例題、PBE 與 signaling 的 off-path／序列理性條件',
            '釐清第二價 truthful bidding、Bertrand p=c、Rubinstein bargaining 與 VCG 結論的適用假設',
            '補強 rationalizability 對混合策略嚴格支配的完整性提醒',
        ],
        'progressImpact': '保留 Book ID、章節 ID 與題目 ID；閱讀進度與錯題紀錄可延續。',
    }] + old_notes
    manifest_path.write_text(jdump(manifest), encoding='utf-8')

    qitems = []
    for src in QUESTIONS:
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
            'source': '本書自編標準題型',
        })
    qdoc['bookId'] = BOOK
    qdoc['version'] = TARGET_VERSION
    qdoc['count'] = len(qitems)
    qdoc['items'] = qitems
    questions_path.write_text(jdump(qdoc), encoding='utf-8')

    appendix_meta = [
        ('appendix-a','核心符號與解概念速查','NE、SPNE、BNE、PBE、最佳回應、混合策略、折現、信念與常用公式的快速定位。'),
        ('appendix-b','賽局理論標準解題路線','從玩家、時序、payoff/type 資訊與歷史可觀察性建模，再選解概念並檢查偏離與信念。'),
        ('appendix-c','中英名詞對照','賽局理論、資訊結構、拍賣、訊號、機制設計與合作賽局的常用英文術語。'),
    ]
    search_path.write_text(jdump({'entries': search_entries(CHAPTERS, appendix_meta)}), encoding='utf-8')

    for book in library['books']:
        if book.get('id') == BOOK:
            if 'version' in book:
                book['version'] = TARGET_VERSION
            book['status'] = 'available'
    library_path.write_text(jdump(library), encoding='utf-8')

    print(json.dumps({
        'book': BOOK,
        'source_version': SOURCE_VERSION,
        'target_version': TARGET_VERSION,
        'chapters': 20,
        'appendices': 3,
        'questions': len(qitems),
        'search': len(search_entries(CHAPTERS, appendix_meta)),
        'figures': len(CHAPTERS),
    }, ensure_ascii=False))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: python deploy/patch_game_theory_v2.py SITE_ROOT')
    main(sys.argv[1])
