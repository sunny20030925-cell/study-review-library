#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

from qa_mathematical_economics import BOOK, main as qa_base

ACTUAL_BOOK_COUNT = 18
LEGACY_QA_BOOK_COUNT = 15


def main(site_root: str, expected_library: str) -> None:
    site = Path(site_root)
    library_path = site / 'data/library.json'
    actual = json.loads(library_path.read_text(encoding='utf-8'))
    ids = [b['id'] for b in actual['books']]
    if actual['version'] != expected_library:
        raise AssertionError((actual['version'], expected_library))
    if len(ids) != ACTUAL_BOOK_COUNT or ids[-3:] != ['civil-law-overview', 'investments', BOOK]:
        raise AssertionError(f'expected 18-book civil-law-overview -> investments -> mathematical-economics tail, got {ids}')

    # Reuse the already-reviewed deep two-round QA by projecting only the registry shape it was written for.
    math_entry = next(b for b in actual['books'] if b['id'] == BOOK)
    projected = copy.deepcopy(actual)
    projected['books'] = projected['books'][:14] + [math_entry]
    projected_ids = [b['id'] for b in projected['books']]
    if len(projected_ids) != LEGACY_QA_BOOK_COUNT or projected_ids[-3:] != ['advanced-statistics', 'computer-fundamentals', BOOK]:
        raise AssertionError(f'legacy QA projection drift: {projected_ids}')

    library_path.write_text(json.dumps(projected, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    try:
        qa_base(str(site), expected_library)
    finally:
        library_path.write_text(json.dumps(actual, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    restored = json.loads(library_path.read_text(encoding='utf-8'))
    restored_ids = [b['id'] for b in restored['books']]
    if restored_ids != ids:
        raise AssertionError('actual registry was not restored after deep QA projection')
    print(f'MATHEMATICAL_ECONOMICS_RELEASE_QA_OK books={len(restored_ids)} library={expected_library} preserved_formal_tail=17')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('usage: python deploy/qa_mathematical_economics_release.py SITE_ROOT EXPECTED_LIBRARY')
    main(sys.argv[1], sys.argv[2])
