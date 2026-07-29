#!/usr/bin/env python3
from __future__ import annotations

import contextlib
import hashlib
import io
import json
import re
import sys
from pathlib import Path

from generate_mathematical_economics_v2 import main as generate_v2
from qa_mathematical_economics_v2 import main as qa_v2

BOOK = 'mathematical-economics'


def next_version(version: str) -> str:
    match = re.fullmatch(r'(\d{4}\.\d{2}\.\d{2})-(\d+)', version)
    if not match:
        raise AssertionError(f'invalid library version: {version}')
    return f'{match.group(1)}-{int(match.group(2)) + 1}'


def tree_hash(root: Path, exclude_prefix: str | None = None) -> str:
    h = hashlib.sha256()
    if not root.exists():
        return h.hexdigest()
    for path in sorted(p for p in root.rglob('*') if p.is_file()):
        rel = path.relative_to(root).as_posix()
        if exclude_prefix and (rel == exclude_prefix or rel.startswith(exclude_prefix + '/')):
            continue
        h.update(rel.encode())
        h.update(b'\0')
        h.update(path.read_bytes())
        h.update(b'\0')
    return h.hexdigest()


def book_hashes(site: Path, ids: list[str]) -> dict[str, str]:
    result = {}
    for book_id in ids:
        root = site / 'books' / book_id
        if not root.is_dir():
            raise AssertionError(f'missing existing book {book_id}')
        result[book_id] = tree_hash(root)
    return result


def main(site_root: str, expected_before: str) -> str:
    site = Path(site_root)
    library_path = site / 'data/library.json'
    before = json.loads(library_path.read_text(encoding='utf-8'))
    ids = [b['id'] for b in before['books']]
    if before['version'] != expected_before:
        raise AssertionError((before['version'], expected_before))
    if BOOK in ids:
        raise AssertionError(f'{BOOK} already exists in formal base; use an in-place v2 patch workflow')
    if not ids:
        raise AssertionError('empty formal base')

    existing_books = book_hashes(site, ids)
    existing_assets = tree_hash(site / 'assets', exclude_prefix='mathematical-economics-svg')
    target = next_version(expected_before)

    generate_v2(str(site))
    generated = json.loads(library_path.read_text(encoding='utf-8'))
    generated_ids = [b['id'] for b in generated['books']]
    if generated_ids != ids + [BOOK]:
        raise AssertionError(f'book order drift: {generated_ids}')
    generated['version'] = target
    library_path.write_text(json.dumps(generated, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    sw_path = site / 'sw.js'
    sw = sw_path.read_text(encoding='utf-8')
    sw, count = re.subn(r"const VERSION = 'study-library-[^']+';", f"const VERSION = 'study-library-{target}';", sw, count=1)
    if count != 1:
        raise AssertionError('service worker version marker missing')
    sw_path.write_text(sw, encoding='utf-8')

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        qa_v2(str(site), target)
    if buf.getvalue():
        print(buf.getvalue(), end='', file=sys.stderr)

    after_books = book_hashes(site, ids)
    changed_books = [book_id for book_id in ids if existing_books[book_id] != after_books[book_id]]
    if changed_books:
        raise AssertionError(f'existing book hashes changed: {changed_books}')
    after_assets = tree_hash(site / 'assets', exclude_prefix='mathematical-economics-svg')
    if after_assets != existing_assets:
        raise AssertionError('pre-existing shared/book asset hashes changed')

    final = json.loads(library_path.read_text(encoding='utf-8'))
    final_ids = [b['id'] for b in final['books']]
    if final['version'] != target or final_ids != ids + [BOOK]:
        raise AssertionError('final mathematical economics v2 state drift')

    print(
        f'MATHEMATICAL_ECONOMICS_V2_INTEGRATION_OK books={len(final_ids)} '
        f'library={target} preserved_existing_books={len(ids)} anchor={ids[-1]}',
        file=sys.stderr,
    )
    return target


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('usage: python deploy/integrate_mathematical_economics_v2.py SITE_ROOT EXPECTED_BEFORE')
    print(main(sys.argv[1], sys.argv[2]))
