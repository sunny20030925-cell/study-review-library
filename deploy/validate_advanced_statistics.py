#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

import qa_advanced_statistics_reaudit_v2 as reaudit_v2
import validate_advanced_statistics_legacy as legacy

BOOK = 'advanced-statistics'
V1 = '2026.07.29-1'
V2 = '2026.07.30-1'


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
    version = manifest['version']
    if version != questions['version']:
        raise AssertionError('advanced-statistics manifest/questions version mismatch')

    if version == V1:
        projected = dict(original)
        projected['books'] = original['books'][: index + 1]
        library_path.write_text(json.dumps(projected, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        old_version = legacy.VERSION
        legacy.VERSION = V1
        try:
            legacy.main(str(site), expected_library)
        finally:
            legacy.VERSION = old_version
            library_path.write_text(json.dumps(original, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

        restored = json.loads(library_path.read_text(encoding='utf-8'))
        if restored != original:
            raise AssertionError('current library registry was not restored after advanced-statistics v1 validation')
        print(f'ADVANCED_STATISTICS_V1_COMPAT_OK books={len(ids)} library={expected_library} version={version}')
        return

    if version == V2:
        reaudit_v2.main(str(site), expected_library)
        print(f'ADVANCED_STATISTICS_V2_COMPAT_OK books={len(ids)} library={expected_library} version={version}')
        return

    raise AssertionError(f'unsupported advanced-statistics version: {version}')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('usage: python deploy/validate_advanced_statistics.py SITE_ROOT EXPECTED_LIBRARY')
    main(sys.argv[1], sys.argv[2])
