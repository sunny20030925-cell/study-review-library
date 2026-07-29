#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import generate_econometrics as generator
from econometrics_v3_corrections import UPDATED_AT, VERSION, appendix_b_v3, appendix_c_v3, build_v3

BOOK = 'econometrics'
OLD_VERSION = '2026.07.30-1'
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
        raise AssertionError(f'econometrics must exist exactly once: {ids}')
    if 'industrial-economics' not in ids or ids.index(BOOK) > ids.index('industrial-economics'):
        raise AssertionError('econometrics registry order drifted behind industrial economics')
    if 'industry-trade' in ids and ids.index('industrial-economics') > ids.index('industry-trade'):
        raise AssertionError('industrial economics registry order drifted behind industry trade')

    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    questions_top = json.loads(questions_path.read_text(encoding='utf-8'))
    if manifest.get('version') == VERSION and questions_top.get('version') == VERSION:
        print(library['version'])
        return library['version']
    if manifest.get('version') != OLD_VERSION or questions_top.get('version') != OLD_VERSION:
        raise AssertionError(
            f'unexpected econometrics source version: manifest={manifest.get("version")} questions={questions_top.get("version")}'
        )

    chapters, questions = build_v3(generator.CHAPTERS, generator.QUESTIONS)
    if [c['id'] for c in chapters] != [f'ch{i:02d}' for i in range(20)]:
        raise AssertionError('chapter IDs changed during v3 correction layer')
    if [q['id'] for q in questions] != [q['id'] for q in generator.QUESTIONS]:
        raise AssertionError('question IDs changed during v3 correction layer')
    if len(questions) != 100:
        raise AssertionError('question count changed during v3 correction layer')

    chapter_meta = [m for m in manifest['chapters'] if m['kind'] == 'chapter']
    if [m['id'] for m in chapter_meta] != [f'ch{i:02d}' for i in range(20)]:
        raise AssertionError('published chapter metadata drift')
    for ch in chapters:
        meta = next(m for m in chapter_meta if m['id'] == ch['id'])
        (root / meta['file']).write_text(generator.chapter_html(ch), encoding='utf-8')

    appendix_b = appendix_b_v3(generator.appendix_b())
    appendix_c = appendix_c_v3(generator.appendix_c())
    appendix_bodies = {
        'appendix-a': generator.appendix_a(chapters),
        'appendix-b': appendix_b,
        'appendix-c': appendix_c,
    }
    for meta in [m for m in manifest['chapters'] if m['kind'] == 'appendix']:
        (root / meta['file']).write_text(appendix_bodies[meta['id']], encoding='utf-8')

    chapter_titles = {ch['id']: f'第 {int(ch["id"][2:])} 章 {ch["title"]}' for ch in chapters}
    corrected_items = []
    for src in questions:
        slot = src['id'].rsplit('-', 1)[-1]
        corrected_items.append({
            'id': src['id'],
            'bookId': BOOK,
            'chapterId': src['chapterId'],
            'chapterTitle': chapter_titles[src['chapterId']],
            'topic': next(ch['title'] for ch in chapters if ch['id'] == src['chapterId']),
            'difficulty': generator.DIFFICULTY_BY_SLOT[slot],
            'question': src['question'],
            'answer': src['answer'],
            'explanation': src['explanation'],
            'source': '本書自編標準題型',
        })
    questions_top['version'] = VERSION
    questions_top['count'] = len(corrected_items)
    questions_top['items'] = corrected_items
    questions_path.write_text(jdump(questions_top), encoding='utf-8')

    appendix_meta = [
        ('appendix-a', '核心公式與假設速查', 'OLS、推論、函數形式、時間序列、panel、IV／LATE、DiD、RDD 與成立條件。'),
        ('appendix-b', '計量經濟學解題路線', '從 estimand、identification 到 estimator、standard error、validation／test 與 interpretation 的解題流程。'),
        ('appendix-c', '中英名詞與輸出表對照', '計量經濟學英文術語、因果 estimand 與迴歸輸出表欄位對照。'),
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
        'title': '第二次獨立內容審校與精確性修正',
        'changes': [
            'IV／noncompliance 明確區分 complier LATE／CACE 與 ATE／ATT',
            'DiD 補上 no-anticipation／提前反應條件',
            'Fuzzy RDD 明確限定為 cutoff 處 local complier LATE',
            '預測章改用 validation／CV 選模，final test set 僅作最後評估',
            '附錄同步補齊 LATE、monotonicity、no anticipation 與 validation/test 解題路線',
            '維持 20 章、3 附錄、100 題、189 搜尋與全部既有章節／題目 ID',
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
        raise SystemExit('usage: python deploy/patch_econometrics_v3.py SITE_ROOT')
    main(sys.argv[1])
