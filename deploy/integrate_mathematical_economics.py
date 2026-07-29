#!/usr/bin/env python3
from __future__ import annotations

import contextlib, hashlib, io, json, re, sys
from pathlib import Path

from generate_mathematical_economics import main as generate_book
from qa_mathematical_economics import main as qa_book

BOOK='mathematical-economics'
PREVIOUS='computer-fundamentals'
PRE_COUNT=14


def next_version(v: str) -> str:
    m=re.fullmatch(r'(\d{4}\.\d{2}\.\d{2})-(\d+)',v)
    if not m: raise AssertionError(f'invalid library version: {v}')
    return f'{m.group(1)}-{int(m.group(2))+1}'


def book_hashes(site: Path, ids: list[str]) -> dict[str,str]:
    out={}
    for bid in ids:
        root=site/'books'/bid
        if not root.is_dir(): raise AssertionError(f'missing existing book: {bid}')
        h=hashlib.sha256()
        for p in sorted(x for x in root.rglob('*') if x.is_file()):
            h.update(p.relative_to(root).as_posix().encode()); h.update(b'\0'); h.update(p.read_bytes()); h.update(b'\0')
        out[bid]=h.hexdigest()
    return out


def main(site_root: str, expected_before: str) -> str:
    site=Path(site_root); lp=site/'data/library.json'
    before_doc=json.loads(lp.read_text(encoding='utf-8')); ids=[b['id'] for b in before_doc['books']]
    if before_doc['version']!=expected_before: raise AssertionError((before_doc['version'],expected_before))
    if BOOK in ids: raise AssertionError(f'{BOOK} already exists')
    if len(ids)!=PRE_COUNT or ids[-2:]!=['advanced-statistics',PREVIOUS]: raise AssertionError(f'expected 14-book advanced-statistics -> computer-fundamentals tail, got {ids}')
    before_hashes=book_hashes(site,ids)
    target=next_version(expected_before)

    buf=io.StringIO()
    with contextlib.redirect_stdout(buf): generate_book(str(site))
    if buf.getvalue(): print(buf.getvalue(),end='',file=sys.stderr)

    doc=json.loads(lp.read_text(encoding='utf-8')); new_ids=[b['id'] for b in doc['books']]
    if new_ids!=ids+[BOOK]: raise AssertionError(f'book order drift: {new_ids}')
    doc['version']=target; lp.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    swp=site/'sw.js'; sw=swp.read_text(encoding='utf-8'); sw,n=re.subn(r"const VERSION = 'study-library-[^']+';",f"const VERSION = 'study-library-{target}';",sw,count=1)
    if n!=1: raise AssertionError('service worker version marker missing')
    swp.write_text(sw,encoding='utf-8')

    qa_book(str(site),target)
    after_hashes=book_hashes(site,ids)
    changed=[bid for bid in ids if before_hashes[bid]!=after_hashes[bid]]
    if changed: raise AssertionError(f'existing book hashes changed: {changed}')
    final=json.loads(lp.read_text(encoding='utf-8'))
    if final['version']!=target or len(final['books'])!=15 or final['books'][-1]['id']!=BOOK: raise AssertionError('final mathematical economics state drift')
    print(f'MATHEMATICAL_ECONOMICS_INTEGRATION_OK books=15 library={target} preserved_existing_books=14',file=sys.stderr)
    return target


if __name__=='__main__':
    if len(sys.argv)!=3: raise SystemExit('usage: integrate_mathematical_economics.py SITE_ROOT EXPECTED_BEFORE')
    print(main(sys.argv[1],sys.argv[2]))
