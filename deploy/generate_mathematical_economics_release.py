#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

from generate_mathematical_economics import BOOK, main as generate_base

PRE_COUNT = 17
PREVIOUS = 'investments'
LEGACY_BASE_COUNT = 14


def main(site_root: str) -> None:
    site = Path(site_root)
    library_path = site / 'data/library.json'
    original = json.loads(library_path.read_text(encoding='utf-8'))
    ids = [b['id'] for b in original['books']]
    if BOOK in ids:
        raise AssertionError(f'{BOOK} already exists')
    if len(ids) != PRE_COUNT or ids[-2:] != ['civil-law-overview', PREVIOUS]:
        raise AssertionError(f'expected 17-book civil-law-overview -> investments tail, got {ids}')
    if original['books'][LEGACY_BASE_COUNT - 1]['id'] != 'computer-fundamentals':
        raise AssertionError('legacy mathematical-economics generator projection no longer ends at computer-fundamentals')

    projected = copy.deepcopy(original)
    projected['books'] = projected['books'][:LEGACY_BASE_COUNT]
    library_path.write_text(json.dumps(projected, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    try:
        generate_base(str(site))
        generated = json.loads(library_path.read_text(encoding='utf-8'))
        if len(generated['books']) != LEGACY_BASE_COUNT + 1 or generated['books'][-1]['id'] != BOOK:
            raise AssertionError('legacy generator did not append mathematical economics as expected')
        math_entry = generated['books'][-1]
    except Exception:
        library_path.write_text(json.dumps(original, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        raise

    restored = copy.deepcopy(original)
    restored['books'].append(math_entry)
    library_path.write_text(json.dumps(restored, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    # Clarify comparative statics wording and align the legacy deep-QA guard with the rendered text.
    for rel in ('chapters/ch08.html', 'search.json'):
        path = site / 'books' / BOOK / rel
        text = path.read_text(encoding='utf-8')
        text = text.replace('比較靜態不是追時間路徑', '比較靜態不是時間路徑；它比較參數改變前後的兩個均衡')
        path.write_text(text, encoding='utf-8')
    json.loads((site / 'books' / BOOK / 'search.json').read_text(encoding='utf-8'))

    print(json.dumps({'book': BOOK, 'pre_books': PRE_COUNT, 'post_books': PRE_COUNT + 1, 'base_projection_books': LEGACY_BASE_COUNT}, ensure_ascii=False), file=sys.stderr)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: python deploy/generate_mathematical_economics_release.py SITE_ROOT')
    main(sys.argv[1])
