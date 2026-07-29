#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import generate_advanced_statistics as generator
from advanced_statistics_v2_corrections import UPDATED_AT, VERSION, build_v2

BOOK = 'advanced-statistics'
OLD_VERSION = '2026.07.29-1'
RELEASE_DATE = '2026.07.30'


def jdump(obj):
    return json.dumps(obj, ensure_ascii=False, indent=2) + '\n'


def next_library_version(current: str) -> str:
    m = re.fullmatch(r'(\d{4}\.\d{2}\.\d{2})-(\d+)', current)
    if not m:
        raise AssertionError(f'unexpected library version: {current}')
    date, serial = m.group(1), int(m.group(2))
    if date < RELEASE_DATE:
        return f'{RELEASE_DATE}-1'
    return f'{date}-{serial + 1}'


def main(site_root: str) -> str:
    site = Path(site_root)
    lib_path = site / 'data/library.json'
    root = site / 'books' / BOOK
    manifest_path = root / 'manifest.json'
    questions_path = root / 'questions.json'
    search_path = root / 'search.json'

    library = json.loads(lib_path.read_text(encoding='utf-8'))
    ids = [b['id'] for b in library['books']]
    if ids.count(BOOK) != 1:
        raise AssertionError(f'advanced statistics must exist exactly once: {ids}')
    if 'computer-fundamentals' in ids and ids.index(BOOK) > ids.index('computer-fundamentals'):
        raise AssertionError('advanced statistics canonical order drift')

    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    questions_top = json.loads(questions_path.read_text(encoding='utf-8'))
    if manifest.get('version') == VERSION and questions_top.get('version') == VERSION:
        print(library['version'])
        return library['version']
    if manifest.get('version') != OLD_VERSION or questions_top.get('version') != OLD_VERSION:
        raise AssertionError(
            f'unexpected advanced-statistics version: manifest={manifest.get("version")} questions={questions_top.get("version")}'
        )

    chapters, questions = build_v2(generator.CHAPTERS, generator.QUESTIONS)
    if [c['id'] for c in chapters] != [f'ch{i:02d}' for i in range(20)]:
        raise AssertionError('chapter IDs changed during v2 correction')
    if [x['id'] for x in questions] != [x['id'] for x in generator.QUESTIONS]:
        raise AssertionError('question IDs changed during v2 correction')
    if len(questions) != 100:
        raise AssertionError('question count changed during v2 correction')

    chapter_meta = [m for m in manifest['chapters'] if m['kind'] == 'chapter']
    if [m['id'] for m in chapter_meta] != [f'ch{i:02d}' for i in range(20)]:
        raise AssertionError('published chapter metadata drift')
    for chapter in chapters:
        meta = next(m for m in chapter_meta if m['id'] == chapter['id'])
        (root / meta['file']).write_text(generator.chapter_html(chapter), encoding='utf-8')

    appendix_bodies = {
        'appendix-a': generator.appendix_a(chapters),
        'appendix-b': generator.appendix_b(),
        'appendix-c': generator.appendix_c(),
    }
    for meta in [m for m in manifest['chapters'] if m['kind'] == 'appendix']:
        (root / meta['file']).write_text(appendix_bodies[meta['id']], encoding='utf-8')

    chapter_titles = {c['id']: f'第 {int(c["id"][2:])} 章 {c["title"]}' for c in chapters}
    items = []
    for src in questions:
        slot = src['id'].rsplit('-', 1)[-1]
        items.append({
            'id': src['id'],
            'bookId': BOOK,
            'chapterId': src['chapterId'],
            'chapterTitle': chapter_titles[src['chapterId']],
            'topic': next(c['title'] for c in chapters if c['id'] == src['chapterId']),
            'difficulty': generator.DIFFICULTY_BY_SLOT[slot],
            'question': src['question'],
            'answer': src['answer'],
            'explanation': src['explanation'],
            'source': '本書自編標準題型',
        })
    questions_top['version'] = VERSION
    questions_top['count'] = len(items)
    questions_top['items'] = items
    questions_path.write_text(jdump(questions_top), encoding='utf-8')

    appendix_meta = [
        ('appendix-a', '核心分配、定理與公式速查', '常用分配、抽樣分配、估計與檢定公式及其成立條件。'),
        ('appendix-b', '高等統計解題路線', '從模型與支撐到抽樣分配、估計量與檢定的判斷流程。'),
        ('appendix-c', '中英名詞與符號對照', '高等統計與數理統計常見英文術語、定理名稱與縮寫。'),
    ]
    entries = generator.search_entries(chapters, appendix_meta)
    if len(entries) != 189:
        raise AssertionError(f'search count drift: {len(entries)}')
    search_path.write_text(jdump({'entries': entries}), encoding='utf-8')

    manifest['version'] = VERSION
    manifest['updatedAt'] = UPDATED_AT
    release = {
        'version': VERSION,
        'date': UPDATED_AT,
        'title': '發布後第二次內容審計與條件精確化',
        'changes': [
            '修正「完備性比充分性更強」的錯誤概括：兩者為不同性質，一般互不推出',
            '補齊 Negative Binomial、Slutsky、MLE invariance、一致性與漸近常態等原 scope 已列但 v1 講解不足的內容',
            '精確化多元常態條件分布、Rao–Blackwell、z/t 區間、size vs level、p-value、Neyman–Pearson、UMP／MLR、Wilks 與 Gauss–Markov 條件',
            '維持 20 章、3 附錄、100 題、189 搜尋、20 圖解及全部既有章節／題目 ID',
        ],
        'progressImpact': '章節 ID、題目 ID、題數與儲存鍵不變，既有閱讀進度與錯題紀錄相容。',
    }
    notes = [n for n in manifest.get('releaseNotes', []) if n.get('version') != VERSION]
    manifest['releaseNotes'] = [release] + notes
    manifest_path.write_text(jdump(manifest), encoding='utf-8')

    for entry in library['books']:
        if entry['id'] == BOOK and 'version' in entry:
            entry['version'] = VERSION
    final_library_version = next_library_version(library['version'])
    library['version'] = final_library_version
    lib_path.write_text(jdump(library), encoding='utf-8')

    sw_path = site / 'sw.js'
    sw = sw_path.read_text(encoding='utf-8')
    sw, count = re.subn(
        r"const VERSION = 'study-library-[^']+';",
        f"const VERSION = 'study-library-{final_library_version}';",
        sw,
        count=1,
    )
    if count != 1:
        raise AssertionError('service worker version marker not found')
    sw_path.write_text(sw, encoding='utf-8')

    print(final_library_version)
    return final_library_version


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: python deploy/patch_advanced_statistics_v2.py SITE_ROOT')
    main(sys.argv[1])
