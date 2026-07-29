#!/usr/bin/env python3
from __future__ import annotations

import contextlib
import copy
import hashlib
import io
import json
import os
import re
import sys
import tempfile
from pathlib import Path

from generate_industry_trade import load_source
from qa_industry_trade_independent import main as qa_round2
from validate_industry_trade import main as qa_round1

BOOK = 'industry-trade'
VERSION = '2026.07.29-1'
TEMPLATE_BOOK = 'money-banking'


def next_version(version: str) -> str:
    match = re.fullmatch(r'(\d{4}\.\d{2}\.\d{2})-(\d+)', version)
    if not match:
        raise AssertionError(f'invalid library version: {version}')
    return f'{match.group(1)}-{int(match.group(2)) + 1}'


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


def emit(buf: io.StringIO) -> None:
    text = buf.getvalue()
    if text:
        print(text, end='', file=sys.stderr)


def run_embedded_generator(site_root: str) -> None:
    source = load_source()
    namespace = {'__name__': 'industry_trade_embedded', '__file__': '<industry-trade-embedded>'}
    exec(compile(source, '<industry-trade-embedded>', 'exec'), namespace)
    namespace['generate'](site_root)


def integrate(site_root: str, expected_before: str) -> str:
    site = Path(site_root)
    library_path = site / 'data/library.json'
    pre = json.loads(library_path.read_text(encoding='utf-8'))
    pre_ids = [book['id'] for book in pre['books']]

    if pre['version'] != expected_before:
        raise AssertionError(f'industry trade pre-version expected {expected_before}, got {pre["version"]}')
    if BOOK in pre_ids:
        raise AssertionError(f'{BOOK} already present before integration')
    if TEMPLATE_BOOK not in pre_ids:
        raise AssertionError('money-banking template book missing')

    before_hashes = book_hashes(site, pre_ids)
    target = next_version(expected_before)

    money_index = pre_ids.index(TEMPLATE_BOOK)
    core_books = copy.deepcopy(pre['books'][:money_index + 1])
    if len(core_books) != 12 or core_books[-1]['id'] != TEMPLATE_BOOK:
        raise AssertionError(f'unexpected stable template segment: {[b["id"] for b in core_books]}')

    staged = copy.deepcopy(pre)
    staged['books'] = core_books
    library_path.write_text(json.dumps(staged, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            run_embedded_generator(str(site))
    finally:
        emit(buf)

    generated = json.loads(library_path.read_text(encoding='utf-8'))
    new_entries = [book for book in generated['books'] if book.get('id') == BOOK]
    if len(new_entries) != 1:
        raise AssertionError('generator did not produce exactly one industry-trade registry entry')

    final = copy.deepcopy(pre)
    final['version'] = target
    final['books'] = copy.deepcopy(pre['books']) + [new_entries[0]]
    final['books'][-1]['status'] = 'available'
    if 'version' in final['books'][-1]:
        final['books'][-1]['version'] = VERSION
    library_path.write_text(json.dumps(final, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    sw_path = site / 'sw.js'
    sw = sw_path.read_text(encoding='utf-8')
    sw, count = re.subn(
        r"const VERSION = 'study-library-[^']+';",
        f"const VERSION = 'study-library-{target}';",
        sw,
        count=1,
    )
    if count != 1:
        raise AssertionError('service-worker version marker')
    sw_path.write_text(sw, encoding='utf-8')

    with tempfile.TemporaryDirectory(prefix='industry-trade-') as temp_dir:
        pre_library = Path(temp_dir) / 'pre-library.json'
        pre_library.write_text(json.dumps(pre, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        old_expected = os.environ.get('EXPECTED_LIBRARY_VERSION')
        old_pre = os.environ.get('PRE_LIBRARY_JSON')
        os.environ['EXPECTED_LIBRARY_VERSION'] = target
        os.environ['PRE_LIBRARY_JSON'] = str(pre_library)
        try:
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                qa_round1(str(site))
            emit(buf)
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
        qa_round2(str(site))
    emit(buf)

    after_hashes = book_hashes(site, pre_ids)
    if after_hashes != before_hashes:
        changed = [book_id for book_id in pre_ids if before_hashes.get(book_id) != after_hashes.get(book_id)]
        raise AssertionError(f'existing book content changed during industry trade integration: {changed}')

    check = json.loads(library_path.read_text(encoding='utf-8'))
    check_ids = [book['id'] for book in check['books']]
    if check['version'] != target or check_ids != pre_ids + [BOOK]:
        raise AssertionError(f'industry trade final library drift: version={check["version"]}, ids={check_ids}')

    sw = sw_path.read_text(encoding='utf-8')
    if f"const VERSION = 'study-library-{target}';" not in sw:
        raise AssertionError('industry trade final service-worker version drift')

    print(
        f'INDUSTRY_TRADE_INTEGRATION_OK books={len(check_ids)} library={target} '
        f'preserved_existing_books={len(pre_ids)} content_version={VERSION}',
        file=sys.stderr,
    )
    return target


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('usage: python deploy/integrate_industry_trade.py SITE_ROOT EXPECTED_BEFORE')
    print(integrate(sys.argv[1], sys.argv[2]))
