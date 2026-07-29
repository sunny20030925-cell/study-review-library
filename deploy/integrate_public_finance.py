#!/usr/bin/env python3
from __future__ import annotations

import contextlib
import hashlib
import io
import json
import os
import sys
import tempfile
from pathlib import Path

import generate_public_finance as generator
import validate_public_finance as structural_validator
from finalize_public_finance_library import main as finalize_public_finance
from public_finance_v2_corrections import VERSION, build_v2, finalize_generated_metadata
from qa_public_finance_v2 import main as qa_public_finance_v2

BOOK = 'public-finance'
EXPECTED_PREVIOUS_BOOK = 'international-economics'


def emit_stderr(buf: io.StringIO) -> None:
    text = buf.getvalue()
    if text:
        print(text, end='', file=sys.stderr)


def book_hashes(site: Path, book_ids: list[str]) -> dict[str, str]:
    result: dict[str, str] = {}
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
        result[book_id] = digest.hexdigest()
    return result


def integrate(site_root: str, expected_before: str) -> str:
    site = Path(site_root)
    library_path = site / 'data/library.json'
    pre = json.loads(library_path.read_text(encoding='utf-8'))
    pre_ids = [book['id'] for book in pre['books']]

    if pre['version'] != expected_before:
        raise AssertionError(
            f'public finance pre-version expected {expected_before}, got {pre["version"]}'
        )
    if BOOK in pre_ids:
        raise AssertionError('public finance already present before integration')
    if len(pre_ids) != 10 or pre_ids[-1] != EXPECTED_PREVIOUS_BOOK:
        raise AssertionError(
            f'public finance integration requires ten-book international-economics tail, got {pre_ids}'
        )

    before_hashes = book_hashes(site, pre_ids)
    pre_path = Path(tempfile.gettempdir()) / 'pre-public-finance-library.json'
    pre_path.write_text(json.dumps(pre, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    corrected_chapters, corrected_questions = build_v2(generator.CHAPTERS, generator.QUESTIONS)
    # Keep the familiar shorthand explicitly visible after the exact discrete debt formula;
    # the older structural validator also requires this canonical token.
    debt_chapter = next(ch for ch in corrected_chapters if ch['id'] == 'ch19')
    exact_note = debt_chapter['formulas'][1][1]
    debt_chapter['formulas'][1] = (
        r'\Delta b_t=\frac{r_t-g_t}{1+g_t}b_{t-1}-ps_t,\qquad \Delta b\approx(r-g)b-ps',
        exact_note,
    )
    generator.CHAPTERS = corrected_chapters
    generator.QUESTIONS = corrected_questions
    generator.VERSION = VERSION

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        generator.main(str(site))
        finalize_generated_metadata(str(site))
    emit_stderr(buf)

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        finalize_public_finance(str(site), str(pre_path))
    emit_stderr(buf)
    final = json.loads(library_path.read_text(encoding='utf-8'))['version']

    old_expected = os.environ.get('EXPECTED_LIBRARY_VERSION')
    old_pre = os.environ.get('PRE_LIBRARY_JSON')
    old_structural_version = structural_validator.VERSION
    os.environ['EXPECTED_LIBRARY_VERSION'] = final
    os.environ['PRE_LIBRARY_JSON'] = str(pre_path)
    structural_validator.VERSION = VERSION
    try:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            structural_validator.main(str(site))
        emit_stderr(buf)

        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            qa_public_finance_v2(str(site), final)
        emit_stderr(buf)
    finally:
        structural_validator.VERSION = old_structural_version
        if old_expected is None:
            os.environ.pop('EXPECTED_LIBRARY_VERSION', None)
        else:
            os.environ['EXPECTED_LIBRARY_VERSION'] = old_expected
        if old_pre is None:
            os.environ.pop('PRE_LIBRARY_JSON', None)
        else:
            os.environ['PRE_LIBRARY_JSON'] = old_pre

    after_hashes = book_hashes(site, pre_ids)
    if after_hashes != before_hashes:
        changed = [book_id for book_id in pre_ids if after_hashes.get(book_id) != before_hashes.get(book_id)]
        raise AssertionError(f'existing book content changed during public finance integration: {changed}')

    post = json.loads(library_path.read_text(encoding='utf-8'))
    post_ids = [book['id'] for book in post['books']]
    if post_ids != pre_ids + [BOOK]:
        raise AssertionError(f'public finance final book order drift: {post_ids}')

    return final


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('usage: integrate_public_finance.py SITE_ROOT EXPECTED_BEFORE')
    print(integrate(sys.argv[1], sys.argv[2]))
