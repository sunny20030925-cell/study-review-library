#!/usr/bin/env python3
from __future__ import annotations

import contextlib
import hashlib
import io
import json
import re
import sys
from pathlib import Path

from generate_mathematical_economics_release import main as generate_release
from qa_mathematical_economics_release import main as qa_release

BOOK = 'mathematical-economics'
PRE_COUNT = 17


def next_version(version: str) -> str:
    m = re.fullmatch(r'(\d{4}\.\d{2}\.\d{2})-(\d+)', version)
    if not m:
        raise AssertionError(f'invalid library version: {version}')
    return f'{m.group(1)}-{int(m.group(2)) + 1}'


def book_hashes(site: Path, ids: list[str]) -> dict[str, str]:
    out = {}
    for bid in ids:
        root = site / 'books' / bid
        if not root.is_dir():
            raise AssertionError(f'missing existing book: {bid}')
        h = hashlib.sha256()
        for path in sorted(p for p in root.rglob('*') if p.is_file()):
            h.update(path.relative_to(root).as_posix().encode())
            h.update(b'\0')
            h.update(path.read_bytes())
            h.update(b'\0')
        out[bid] = h.hexdigest()
    return out


def main(site_root: str, expected_before: str) -> str:
    site = Path(site_root)
    library_path = site / 'data/library.json'
    before = json.loads(library_path.read_text(encoding='utf-8'))
    ids = [b['id'] for b in before['books']]
    if before['version'] != expected_before:
        raise AssertionError((before['version'], expected_before))
    if BOOK in ids:
        raise AssertionError(f'{BOOK} already exists')
    if len(ids) != PRE_COUNT or ids[-2:] != ['civil-law-overview', 'investments']:
        raise AssertionError(f'expected 17-book civil-law-overview -> investments tail, got {ids}')

    hashes_before = book_hashes(site, ids)
    target = next_version(expected_before)

    generate_release(str(site))
    generated = json.loads(library_path.read_text(encoding='utf-8'))
    if [b['id'] for b in generated['books']] != ids + [BOOK]:
        raise AssertionError('mathematical economics append order drift')
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
        qa_release(str(site), target)
    if buf.getvalue():
        print(buf.getvalue(), end='', file=sys.stderr)

    hashes_after = book_hashes(site, ids)
    changed = [bid for bid in ids if hashes_before[bid] != hashes_after[bid]]
    if changed:
        raise AssertionError(f'existing book hashes changed: {changed}')

    final = json.loads(library_path.read_text(encoding='utf-8'))
    final_ids = [b['id'] for b in final['books']]
    if final['version'] != target or len(final_ids) != 18 or final_ids[-1] != BOOK:
        raise AssertionError('final mathematical economics state drift')
    print(f'MATHEMATICAL_ECONOMICS_RELEASE_INTEGRATION_OK books=18 library={target} preserved_existing_books=17', file=sys.stderr)
    return target


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('usage: python deploy/integrate_mathematical_economics_release.py SITE_ROOT EXPECTED_BEFORE')
    print(main(sys.argv[1], sys.argv[2]))
