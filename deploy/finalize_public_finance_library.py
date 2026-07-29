#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

BOOK_ID = 'public-finance'


def advance_library_version(version: str, steps: int = 1) -> str:
    match = re.fullmatch(r'(\d{4}\.\d{2}\.\d{2})-(\d+)', version)
    if not match:
        raise AssertionError(f'unexpected library version: {version}')
    return f'{match.group(1)}-{int(match.group(2)) + steps}'


def main(site_root: str, pre_library_path: str) -> None:
    site = Path(site_root)
    library_path = site / 'data/library.json'
    pre = json.loads(Path(pre_library_path).read_text(encoding='utf-8'))
    post = json.loads(library_path.read_text(encoding='utf-8'))

    pre_ids = [book['id'] for book in pre['books']]
    post_ids = [book['id'] for book in post['books']]
    if BOOK_ID in pre_ids:
        raise AssertionError(f'{BOOK_ID} already existed before generation')
    if post_ids != pre_ids + [BOOK_ID]:
        raise AssertionError(f'book order drift: before={pre_ids}, after={post_ids}')

    # The canonical pre-public-finance tail is still 2026.07.29-13.
    # -14 was the already published public-finance v1 release; this post-publication
    # content reaudit must publish a distinct cache/library version, so advance to -15.
    final_version = advance_library_version(pre['version'], steps=2)
    post['version'] = final_version
    library_path.write_text(json.dumps(post, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

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


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('usage: python deploy/finalize_public_finance_library.py SITE_ROOT PRE_LIBRARY_JSON')
    main(sys.argv[1], sys.argv[2])
