#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

BOOK = 'game-theory'
TARGET_VERSION = '2026.07.30-2'


def next_library_version(version: str) -> str:
    match = re.fullmatch(r'(\d{4}\.\d{2}\.\d{2})-(\d+)', version)
    if not match:
        raise AssertionError(f'unexpected library version: {version}')
    return f'{match.group(1)}-{int(match.group(2)) + 1}'


def main(site_root: str, expected_before: str) -> str:
    site = Path(site_root)
    library_path = site / 'data/library.json'
    library = json.loads(library_path.read_text(encoding='utf-8'))
    if library['version'] != expected_before:
        raise AssertionError(f'expected shared library {expected_before}, got {library["version"]}')
    ids = [book['id'] for book in library['books']]
    if ids.count(BOOK) != 1:
        raise AssertionError(f'game-theory registry count drift: {ids}')

    manifest = json.loads((site / 'books' / BOOK / 'manifest.json').read_text(encoding='utf-8'))
    questions = json.loads((site / 'books' / BOOK / 'questions.json').read_text(encoding='utf-8'))
    if manifest.get('version') != TARGET_VERSION or questions.get('version') != TARGET_VERSION:
        raise AssertionError('game-theory v2 content must be patched before shared library finalization')

    final_version = next_library_version(expected_before)
    library['version'] = final_version
    for book in library['books']:
        if book.get('id') == BOOK:
            if 'version' in book:
                book['version'] = TARGET_VERSION
            book['status'] = 'available'
    library_path.write_text(json.dumps(library, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    sw_path = site / 'sw.js'
    sw = sw_path.read_text(encoding='utf-8')
    sw, count = re.subn(
        r"const VERSION = 'study-library-[^']+';",
        f"const VERSION = 'study-library-{final_version}';",
        sw,
        count=1,
    )
    if count != 1:
        raise AssertionError('service worker version marker not found')
    sw_path.write_text(sw, encoding='utf-8')

    print(final_version)
    return final_version


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('usage: python deploy/finalize_game_theory_v2_library.py SITE_ROOT EXPECTED_BEFORE')
    main(sys.argv[1], sys.argv[2])
