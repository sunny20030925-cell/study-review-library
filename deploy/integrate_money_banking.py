#!/usr/bin/env python3
from __future__ import annotations

import contextlib
import io
import json
import re
import sys
from pathlib import Path

import validate_money_banking as structural_validator
from generate_money_banking_fresh import main as generate_fresh
from patch_money_banking_v2 import VERSION, main as patch_v2
from qa_money_banking_v2 import main as qa_v2

BOOK='money-banking'
EXPECTED_PREVIOUS_BOOK='public-finance'


def next_version(v: str) -> str:
    m=re.fullmatch(r'(\d{4}\.\d{2}\.\d{2})-(\d+)',v)
    if not m: raise AssertionError(f'invalid library version: {v}')
    return f'{m.group(1)}-{int(m.group(2))+1}'


def emit_stderr(buf: io.StringIO) -> None:
    text=buf.getvalue()
    if text: print(text,end='',file=sys.stderr)


def book_hashes(site: Path,book_ids: list[str]) -> dict[str,str]:
    import hashlib
    out={}
    for book_id in book_ids:
        root=site/'books'/book_id
        if not root.is_dir(): raise AssertionError(f'missing existing book directory: {book_id}')
        h=hashlib.sha256()
        for p in sorted(x for x in root.rglob('*') if x.is_file()):
            h.update(p.relative_to(root).as_posix().encode()); h.update(b'\0'); h.update(p.read_bytes()); h.update(b'\0')
        out[book_id]=h.hexdigest()
    return out


def normalize_checkpoint_for_existing_recorder() -> None:
    path=Path('docs/shared_checkpoint.md')
    text=path.read_text(encoding='utf-8')
    for title in ('個體經濟學','中級會計學','總體經濟學'):
        text=re.sub(rf'^###\s+\d+\.\s+{re.escape(title)}\s*$',f'### {title}',text,flags=re.M)
    path.write_text(text,encoding='utf-8')


def integrate(site_root: str,expected_before: str) -> str:
    site=Path(site_root); lp=site/'data/library.json'
    pre=json.loads(lp.read_text(encoding='utf-8')); pre_ids=[b['id'] for b in pre['books']]
    if pre['version']!=expected_before: raise AssertionError(f'money pre-version expected {expected_before}, got {pre["version"]}')
    if BOOK in pre_ids: raise AssertionError('money-banking already present before integration')
    if len(pre_ids)!=11 or pre_ids[-2:]!=['international-economics',EXPECTED_PREVIOUS_BOOK]:
        raise AssertionError(f'money integration requires current eleven-book intl/public-finance tail, got {pre_ids}')
    before_hashes=book_hashes(site,pre_ids)
    target=next_version(expected_before)

    # finalize_macroeconomics_v2_library.py is executed inside shell command substitution.
    # Keep all diagnostic output off stdout so that only the final library-version token
    # is captured by the workflow variable.
    buf=io.StringIO()
    with contextlib.redirect_stdout(buf): generate_fresh(str(site))
    emit_stderr(buf)
    post_gen=json.loads(lp.read_text(encoding='utf-8')); post_ids=[b['id'] for b in post_gen['books']]
    if post_ids!=pre_ids+[BOOK]: raise AssertionError(f'money fresh generator book order drift: {post_ids}')

    buf=io.StringIO()
    with contextlib.redirect_stdout(buf): patch_v2(str(site))
    emit_stderr(buf)

    post=json.loads(lp.read_text(encoding='utf-8')); post['version']=target
    for book in post['books']:
        if book.get('id')==BOOK:
            if 'version' in book: book['version']=VERSION
            book['status']='available'
    lp.write_text(json.dumps(post,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

    swp=site/'sw.js'; sw=swp.read_text(encoding='utf-8')
    sw,n=re.subn(r"const VERSION = 'study-library-[^']+';",f"const VERSION = 'study-library-{target}';",sw,count=1)
    if n!=1: raise AssertionError('money sw version marker')
    swp.write_text(sw,encoding='utf-8')

    old_version=structural_validator.VERSION
    structural_validator.VERSION=VERSION
    try:
        buf=io.StringIO()
        with contextlib.redirect_stdout(buf): structural_validator.main(str(site))
        emit_stderr(buf)
    finally:
        structural_validator.VERSION=old_version

    buf=io.StringIO()
    with contextlib.redirect_stdout(buf): qa_v2(str(site),target)
    emit_stderr(buf)

    after_hashes=book_hashes(site,pre_ids)
    if after_hashes!=before_hashes:
        changed=[bid for bid in pre_ids if after_hashes.get(bid)!=before_hashes.get(bid)]
        raise AssertionError(f'existing book content changed during money integration: {changed}')

    normalize_checkpoint_for_existing_recorder()
    final=json.loads(lp.read_text(encoding='utf-8'))
    if final['version']!=target or [b['id'] for b in final['books']]!=pre_ids+[BOOK]:
        raise AssertionError('money final library state drift')
    print(f'MONEY_BANKING_FRESH_INTEGRATION_OK books=12 library={target} preserved_existing_books={len(pre_ids)}',file=sys.stderr)
    return target

if __name__=='__main__':
    if len(sys.argv)!=3: raise SystemExit('usage: integrate_money_banking.py SITE_ROOT EXPECTED_BEFORE')
    print(integrate(sys.argv[1],sys.argv[2]))
