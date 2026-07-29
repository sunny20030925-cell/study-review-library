#!/usr/bin/env python3
from __future__ import annotations

import contextlib
import hashlib
import io
import json
import re
import sys
from pathlib import Path

from industrial_economics_content_v2 import VERSION
from patch_industrial_economics_v2 import main as patch_v2
from qa_industrial_economics_v2 import main as qa2
from validate_industrial_economics_v2 import main as qa1

BOOK = 'industrial-economics'


def next_version(v: str) -> str:
    m = re.fullmatch(r'(\d{4}\.\d{2}\.\d{2})-(\d+)', v)
    if not m:
        raise AssertionError(f'invalid library version: {v}')
    return f'{m.group(1)}-{int(m.group(2)) + 1}'


def book_hashes(site: Path, book_ids: list[str]) -> dict[str, str]:
    out = {}
    for book_id in book_ids:
        root = site / 'books' / book_id
        if not root.is_dir():
            raise AssertionError(f'missing existing book directory: {book_id}')
        h = hashlib.sha256()
        for p in sorted(x for x in root.rglob('*') if x.is_file()):
            h.update(p.relative_to(root).as_posix().encode())
            h.update(b'\0')
            h.update(p.read_bytes())
            h.update(b'\0')
        out[book_id] = h.hexdigest()
    return out


def emit_stderr(buf: io.StringIO) -> None:
    text = buf.getvalue()
    if text:
        print(text, end='', file=sys.stderr)


def run_qa_to_stderr(fn, site: str, version: str) -> None:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        fn(site, version)
    emit_stderr(buf)


def integrate(site_root: str, expected_before: str) -> str:
    site = Path(site_root)
    library_path = site / 'data/library.json'
    library = json.loads(library_path.read_text(encoding='utf-8'))
    ids = [b['id'] for b in library['books']]
    if library['version'] != expected_before:
        raise AssertionError(f'pre-version expected {expected_before}, got {library["version"]}')
    if ids.count(BOOK) != 1:
        raise AssertionError(f'expected one deployed industrial economics book, got {ids.count(BOOK)}')

    root = site / 'books' / BOOK
    manifest_before = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    questions_before = json.loads((root / 'questions.json').read_text(encoding='utf-8'))
    chapter_ids_before = [x['id'] for x in manifest_before['chapters']]
    question_ids_before = [x['id'] for x in questions_before['items']]
    other_ids = [x for x in ids if x != BOOK]
    other_hashes_before = book_hashes(site, other_ids)

    if manifest_before.get('version') == VERSION and questions_before.get('version') == VERSION:
        # Idempotent validation path: already formally patched; do not create another library version.
        run_qa_to_stderr(qa1, str(site), expected_before)
        run_qa_to_stderr(qa2, str(site), expected_before)
        print(
            f'INDUSTRIAL_ECONOMICS_V2_ALREADY_APPLIED books={len(ids)} library={expected_before} '
            f'preserved_other_books={len(other_ids)}',
            file=sys.stderr,
        )
        return expected_before

    target = next_version(expected_before)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        patch_v2(str(site))
    emit_stderr(buf)

    library = json.loads(library_path.read_text(encoding='utf-8'))
    library['version'] = target
    for book in library['books']:
        if book.get('id') == BOOK:
            if 'version' in book:
                book['version'] = VERSION
            book['status'] = 'available'
    library_path.write_text(json.dumps(library, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    sw_path = site / 'sw.js'
    sw = sw_path.read_text(encoding='utf-8')
    sw, n = re.subn(
        r"const VERSION = 'study-library-[^']+';",
        f"const VERSION = 'study-library-{target}';",
        sw,
        count=1,
    )
    if n != 1:
        raise AssertionError('service-worker version marker')
    sw_path.write_text(sw, encoding='utf-8')

    run_qa_to_stderr(qa1, str(site), target)
    run_qa_to_stderr(qa2, str(site), target)

    manifest_after = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    questions_after = json.loads((root / 'questions.json').read_text(encoding='utf-8'))
    if [x['id'] for x in manifest_after['chapters']] != chapter_ids_before:
        raise AssertionError('chapter ids changed during v2 integration')
    if [x['id'] for x in questions_after['items']] != question_ids_before:
        raise AssertionError('question ids changed during v2 integration')

    other_hashes_after = book_hashes(site, other_ids)
    if other_hashes_after != other_hashes_before:
        changed = [bid for bid in other_ids if other_hashes_after.get(bid) != other_hashes_before.get(bid)]
        raise AssertionError(f'other book content changed during industrial v2 integration: {changed}')

    final = json.loads(library_path.read_text(encoding='utf-8'))
    final_ids = [b['id'] for b in final['books']]
    if final['version'] != target or final_ids != ids:
        raise AssertionError('library order/version drift during industrial v2 integration')

    print(
        f'INDUSTRIAL_ECONOMICS_V2_INTEGRATION_OK books={len(final_ids)} library={target} '
        f'preserved_other_books={len(other_ids)} chapter_ids_preserved=true question_ids_preserved=true',
        file=sys.stderr,
    )
    return target


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('usage: integrate_industrial_economics_v2.py SITE_ROOT EXPECTED_BEFORE')
    print(integrate(sys.argv[1], sys.argv[2]))
