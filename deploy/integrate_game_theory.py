#!/usr/bin/env python3
from __future__ import annotations

import contextlib
import hashlib
import io
import json
import os
import re
import sys
import tempfile
from pathlib import Path

from generate_game_theory import BOOK, VERSION as BOOK_VERSION, main as generate_book
from finalize_game_theory_library import main as finalize_library
from validate_game_theory import main as qa_round1
from qa_game_theory_second_pass import main as qa_round2

EXPECTED_PREVIOUS_BOOK = 'advanced-statistics'
EXPECTED_EXISTING_BOOK_COUNT = 13


def next_version(version: str) -> str:
    match = re.fullmatch(r'(\d{4}\.\d{2}\.\d{2})-(\d+)', version)
    if not match:
        raise AssertionError(f'invalid library version: {version}')
    return f'{match.group(1)}-{int(match.group(2)) + 1}'


def emit_stderr(buf: io.StringIO) -> None:
    text = buf.getvalue()
    if text:
        print(text, end='', file=sys.stderr)


def book_hashes(site: Path, book_ids: list[str]) -> dict[str, str]:
    out: dict[str, str] = {}
    for book_id in book_ids:
        root = site / 'books' / book_id
        if not root.is_dir():
            raise AssertionError(f'missing existing book directory: {book_id}')
        digest = hashlib.sha256()
        for path in sorted(p for p in root.rglob('*') if p.is_file()):
            digest.update(path.relative_to(root).as_posix().encode('utf-8'))
            digest.update(b'\0')
            digest.update(path.read_bytes())
            digest.update(b'\0')
        out[book_id] = digest.hexdigest()
    return out


def integrate(site_root: str, expected_before: str) -> str:
    site = Path(site_root)
    library_path = site / 'data/library.json'
    pre = json.loads(library_path.read_text(encoding='utf-8'))
    pre_ids = [book['id'] for book in pre['books']]

    if pre['version'] != expected_before:
        raise AssertionError(f'game theory pre-version expected {expected_before}, got {pre["version"]}')
    if BOOK in pre_ids:
        raise AssertionError(f'{BOOK} already exists before integration')
    if len(pre_ids) != EXPECTED_EXISTING_BOOK_COUNT or pre_ids[-1] != EXPECTED_PREVIOUS_BOOK:
        raise AssertionError(f'game theory requires current 13-book advanced-statistics tail, got {pre_ids}')

    expected_target = next_version(expected_before)
    before_hashes = book_hashes(site, pre_ids)
    app_before = hashlib.sha256((site / 'app.js').read_bytes()).hexdigest()

    with tempfile.TemporaryDirectory(prefix='game-theory-') as temp_dir:
        pre_library = Path(temp_dir) / 'pre-library.json'
        pre_library.write_text(json.dumps(pre, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            generate_book(str(site))
        emit_stderr(buf)

        generated = json.loads(library_path.read_text(encoding='utf-8'))
        generated_ids = [book['id'] for book in generated['books']]
        if generated_ids != pre_ids + [BOOK]:
            raise AssertionError(f'game theory generator order drift: {generated_ids}')
        if generated['version'] != expected_before:
            raise AssertionError('game theory generator must not pre-increment the shared library version')

        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            finalized = finalize_library(str(site), str(pre_library))
        emit_stderr(buf)
        if finalized != expected_target:
            raise AssertionError(f'game theory finalizer target drift: expected {expected_target}, got {finalized}')

        old_expected = os.environ.get('EXPECTED_LIBRARY_VERSION')
        old_pre = os.environ.get('PRE_LIBRARY_JSON')
        try:
            os.environ['EXPECTED_LIBRARY_VERSION'] = expected_target
            os.environ['PRE_LIBRARY_JSON'] = str(pre_library)
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                qa_round1(str(site))
            emit_stderr(buf)
        finally:
            if old_expected is None:
                os.environ.pop('EXPECTED_LIBRARY_VERSION', None)
            else:
                os.environ['EXPECTED_LIBRARY_VERSION'] = old_expected
            if old_pre is None:
                os.environ.pop('PRE_LIBRARY_JSON', None)
            else:
                os.environ['PRE_LIBRARY_JSON'] = old_pre

        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            qa_round2()
        emit_stderr(buf)

    after_hashes = book_hashes(site, pre_ids)
    if after_hashes != before_hashes:
        changed = [book_id for book_id in pre_ids if after_hashes.get(book_id) != before_hashes.get(book_id)]
        raise AssertionError(f'existing book content changed during game theory integration: {changed}')
    if hashlib.sha256((site / 'app.js').read_bytes()).hexdigest() != app_before:
        raise AssertionError('shared app.js changed during game theory integration')

    final = json.loads(library_path.read_text(encoding='utf-8'))
    final_ids = [book['id'] for book in final['books']]
    if final['version'] != expected_target or final_ids != pre_ids + [BOOK]:
        raise AssertionError(f'game theory final library drift: version={final["version"]}, ids={final_ids}')

    sw = (site / 'sw.js').read_text(encoding='utf-8')
    if f"const VERSION = 'study-library-{expected_target}';" not in sw:
        raise AssertionError('game theory final service-worker version drift')

    print(
        f'GAME_THEORY_INTEGRATION_OK books={len(final_ids)} library={expected_target} '
        f'preserved_existing_books={len(pre_ids)} content_version={BOOK_VERSION}',
        file=sys.stderr,
    )
    return expected_target


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('usage: python deploy/integrate_game_theory.py SITE_ROOT EXPECTED_BEFORE')
    print(integrate(sys.argv[1], sys.argv[2]))
