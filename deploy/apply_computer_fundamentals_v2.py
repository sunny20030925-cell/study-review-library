from __future__ import annotations

import contextlib
import hashlib
import io
import json
import sys
from pathlib import Path

from patch_computer_fundamentals_v2 import BOOK, SOURCE_VERSION, TARGET_VERSION, main as patch_v2
from finalize_computer_fundamentals_v2_library import main as finalize_library
from qa_computer_fundamentals_v2 import main as qa_v2


def book_hashes(site: Path, book_ids: list[str]) -> dict[str,str]:
    out={}
    for book_id in book_ids:
        root=site/'books'/book_id
        if not root.is_dir():
            raise AssertionError(f'missing book directory {book_id}')
        h=hashlib.sha256()
        for p in sorted(x for x in root.rglob('*') if x.is_file()):
            h.update(p.relative_to(root).as_posix().encode('utf-8'))
            h.update(b'\0'); h.update(p.read_bytes()); h.update(b'\0')
        out[book_id]=h.hexdigest()
    return out


def emit(buf: io.StringIO) -> None:
    text=buf.getvalue()
    if text:
        print(text,end='',file=sys.stderr)


def apply(site_root: str, expected_before: str) -> str:
    site=Path(site_root)
    lp=site/'data/library.json'
    library=json.loads(lp.read_text(encoding='utf-8'))
    if library['version']!=expected_before:
        raise AssertionError(f'expected {expected_before}, got {library["version"]}')
    ids=[b['id'] for b in library['books']]
    if BOOK not in ids or ids.count(BOOK)!=1:
        raise AssertionError(f'computer fundamentals registration drift: {ids}')
    root=site/'books'/BOOK
    manifest=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
    other_ids=[bid for bid in ids if bid!=BOOK]
    before_hashes=book_hashes(site,other_ids)

    if manifest['version']==SOURCE_VERSION:
        buf=io.StringIO()
        with contextlib.redirect_stdout(buf):
            patch_v2(site_root)
        emit(buf)
        buf=io.StringIO()
        with contextlib.redirect_stdout(buf):
            target_library=finalize_library(site_root,expected_before)
        emit(buf)
    elif manifest['version']==TARGET_VERSION:
        target_library=expected_before
    else:
        raise AssertionError(f'unexpected computer fundamentals version {manifest["version"]}')

    buf=io.StringIO()
    with contextlib.redirect_stdout(buf):
        qa_v2(site_root,target_library)
    emit(buf)

    after_hashes=book_hashes(site,other_ids)
    if before_hashes!=after_hashes:
        changed=[bid for bid in other_ids if before_hashes.get(bid)!=after_hashes.get(bid)]
        raise AssertionError(f'non-target books changed during computer fundamentals v2 audit: {changed}')

    final=json.loads(lp.read_text(encoding='utf-8'))
    final_manifest=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
    if final['version']!=target_library or final_manifest['version']!=TARGET_VERSION:
        raise AssertionError('computer fundamentals v2 final state drift')
    if [b['id'] for b in final['books']]!=ids:
        raise AssertionError('book order/identity changed during v2 audit')

    print(f'COMPUTER_FUNDAMENTALS_V2_APPLY_OK books={len(ids)} library={target_library} preserved_non_target_books={len(other_ids)} content_version={TARGET_VERSION}',file=sys.stderr)
    return target_library


if __name__=='__main__':
    if len(sys.argv)!=3:
        raise SystemExit('usage: python deploy/apply_computer_fundamentals_v2.py SITE_ROOT EXPECTED_LIBRARY_VERSION')
    print(apply(sys.argv[1],sys.argv[2]))
