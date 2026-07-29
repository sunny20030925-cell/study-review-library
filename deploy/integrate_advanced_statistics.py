#!/usr/bin/env python3
from __future__ import annotations

import contextlib
import hashlib
import io
import json
import re
import sys
from pathlib import Path

from generate_advanced_statistics import BOOK, VERSION, main as generate
from validate_advanced_statistics import main as validate

EXPECTED_PREVIOUS_BOOK='money-banking'

def next_version(v: str) -> str:
    m=re.fullmatch(r'(\d{4}\.\d{2}\.\d{2})-(\d+)',v)
    if not m:
        raise AssertionError(f'invalid library version: {v}')
    return f'{m.group(1)}-{int(m.group(2))+1}'

def book_hashes(site: Path, book_ids: list[str]) -> dict[str,str]:
    out={}
    for book_id in book_ids:
        root=site/'books'/book_id
        if not root.is_dir():
            raise AssertionError(f'missing existing book directory: {book_id}')
        h=hashlib.sha256()
        for p in sorted(x for x in root.rglob('*') if x.is_file()):
            h.update(p.relative_to(root).as_posix().encode())
            h.update(b'\0'); h.update(p.read_bytes()); h.update(b'\0')
        out[book_id]=h.hexdigest()
    return out

def emit_stderr(buf: io.StringIO) -> None:
    text=buf.getvalue()
    if text:
        print(text,end='',file=sys.stderr)

def integrate(site_root: str, expected_before: str) -> str:
    site=Path(site_root)
    lp=site/'data/library.json'
    pre=json.loads(lp.read_text(encoding='utf-8'))
    pre_ids=[b['id'] for b in pre['books']]
    if pre['version']!=expected_before:
        raise AssertionError(f'advanced statistics pre-version expected {expected_before}, got {pre["version"]}')
    if BOOK in pre_ids:
        raise AssertionError(f'{BOOK} already present before integration')
    if len(pre_ids)!=12 or pre_ids[-1]!=EXPECTED_PREVIOUS_BOOK:
        raise AssertionError(f'advanced statistics requires current twelve-book money-banking tail, got {pre_ids}')
    before_hashes=book_hashes(site,pre_ids)
    target=next_version(expected_before)

    buf=io.StringIO()
    with contextlib.redirect_stdout(buf):
        generate(str(site))
    emit_stderr(buf)

    post=json.loads(lp.read_text(encoding='utf-8'))
    post_ids=[b['id'] for b in post['books']]
    if post_ids!=pre_ids+[BOOK]:
        raise AssertionError(f'advanced statistics generator book order drift: {post_ids}')
    post['version']=target
    for b in post['books']:
        if b.get('id')==BOOK:
            b['status']='available'
            if 'version' in b:
                b['version']=VERSION
    lp.write_text(json.dumps(post,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

    swp=site/'sw.js'
    sw=swp.read_text(encoding='utf-8')
    sw,n=re.subn(r"const VERSION = 'study-library-[^']+';",f"const VERSION = 'study-library-{target}';",sw,count=1)
    if n!=1:
        raise AssertionError('advanced statistics service-worker version marker')
    swp.write_text(sw,encoding='utf-8')

    buf=io.StringIO()
    with contextlib.redirect_stdout(buf):
        validate(str(site),target)
    emit_stderr(buf)

    after_hashes=book_hashes(site,pre_ids)
    if before_hashes!=after_hashes:
        changed=[bid for bid in pre_ids if before_hashes.get(bid)!=after_hashes.get(bid)]
        raise AssertionError(f'existing book content changed during advanced statistics integration: {changed}')

    final=json.loads(lp.read_text(encoding='utf-8'))
    if final['version']!=target or [b['id'] for b in final['books']]!=pre_ids+[BOOK]:
        raise AssertionError('advanced statistics final library state drift')
    print(f'ADVANCED_STATISTICS_INTEGRATION_OK books=13 library={target} preserved_existing_books={len(pre_ids)}',file=sys.stderr)
    return target

if __name__=='__main__':
    if len(sys.argv)!=3:
        raise SystemExit('usage: python deploy/integrate_advanced_statistics.py SITE_ROOT EXPECTED_BEFORE')
    print(integrate(sys.argv[1],sys.argv[2]))
