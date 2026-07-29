#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

import validate_advanced_statistics_legacy as legacy

BOOK = 'advanced-statistics'


def main(site_root: str, expected_library: str) -> None:
    site = Path(site_root)
    library_path = site / 'data/library.json'
    original = json.loads(library_path.read_text(encoding='utf-8'))
    ids = [b['id'] for b in original['books']]

    if BOOK not in ids:
        raise AssertionError('advanced-statistics missing from current library')
    index = ids.index(BOOK)
    if index != 12 or ids[index - 1] != 'money-banking':
        raise AssertionError(f'advanced-statistics canonical position drift: index={index}, previous={ids[index-1] if index else None}')

    manifest = json.loads((site / 'books' / BOOK / 'manifest.json').read_text(encoding='utf-8'))
    questions = json.loads((site / 'books' / BOOK / 'questions.json').read_text(encoding='utf-8'))
    if manifest['version'] != questions['version']:
        raise AssertionError('advanced-statistics manifest/questions version mismatch')

    projected = dict(original)
    projected['books'] = original['books'][: index + 1]
    library_path.write_text(json.dumps(projected, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    old_version = legacy.VERSION
    legacy.VERSION = manifest['version']
    try:
        legacy.main(str(site), expected_library)
    finally:
        legacy.VERSION = old_version
        library_path.write_text(json.dumps(original, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    restored = json.loads(library_path.read_text(encoding='utf-8'))
    if restored != original:
        raise AssertionError('current library registry was not restored after advanced-statistics validation')
    print(f'ADVANCED_STATISTICS_CURRENT_LIBRARY_COMPAT_OK books={len(ids)} library={expected_library} version={manifest["version"]}')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('usage: python deploy/validate_advanced_statistics.py SITE_ROOT EXPECTED_LIBRARY')
    main(sys.argv[1], sys.argv[2])
