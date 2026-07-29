#!/usr/bin/env python3
from __future__ import annotations
import contextlib,hashlib,io,json,re,sys
from pathlib import Path

from generate_civil_law_overview import main as generate_fresh, BOOK, VERSION
from validate_civil_law_overview import main as qa1
from qa_civil_law_overview import main as qa2

MIN_EXISTING_BOOKS=12

def next_version(v):
    m=re.fullmatch(r'(\d{4}\.\d{2}\.\d{2})-(\d+)',v)
    if not m: raise AssertionError(f'invalid library version: {v}')
    return f'{m.group(1)}-{int(m.group(2))+1}'

def emit_stderr(buf):
    text=buf.getvalue()
    if text: print(text,end='',file=sys.stderr)

def book_hashes(site,book_ids):
    out={}
    for bid in book_ids:
        root=site/'books'/bid; h=hashlib.sha256()
        if not root.is_dir(): raise AssertionError(f'missing book {bid}')
        for p in sorted(x for x in root.rglob('*') if x.is_file()):
            h.update(p.relative_to(root).as_posix().encode()); h.update(b'\0'); h.update(p.read_bytes()); h.update(b'\0')
        out[bid]=h.hexdigest()
    return out

def integrate(site_root,expected_before):
    site=Path(site_root); lp=site/'data/library.json'
    pre=json.loads(lp.read_text(encoding='utf-8')); pre_ids=[b['id'] for b in pre['books']]
    if pre['version']!=expected_before: raise AssertionError(f'civil pre-version expected {expected_before}, got {pre["version"]}')
    if BOOK in pre_ids: raise AssertionError('civil book already present')
    if len(pre_ids)<MIN_EXISTING_BOOKS or len(set(pre_ids))!=len(pre_ids): raise AssertionError(f'civil integration requires a valid formal library, got {pre_ids}')
    before=book_hashes(site,pre_ids); target=next_version(expected_before)
    buf=io.StringIO()
    with contextlib.redirect_stdout(buf): generate_fresh(str(site))
    emit_stderr(buf)
    post=json.loads(lp.read_text(encoding='utf-8')); post_ids=[b['id'] for b in post['books']]
    if post_ids!=pre_ids+[BOOK]: raise AssertionError(f'civil generated book order drift: {post_ids}')
    post['version']=target
    for b in post['books']:
        if b['id']==BOOK:
            if 'version' in b: b['version']=VERSION
            b['status']='available'
    lp.write_text(json.dumps(post,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    swp=site/'sw.js'; sw=swp.read_text(encoding='utf-8'); sw,n=re.subn(r"const VERSION = 'study-library-[^']+';",f"const VERSION = 'study-library-{target}';",sw,count=1)
    if n!=1: raise AssertionError('civil sw version marker')
    swp.write_text(sw,encoding='utf-8')
    buf=io.StringIO()
    with contextlib.redirect_stdout(buf): qa1(str(site),target)
    emit_stderr(buf)
    buf=io.StringIO()
    with contextlib.redirect_stdout(buf): qa2(str(site),target)
    emit_stderr(buf)
    after=book_hashes(site,pre_ids)
    if after!=before:
        changed=[bid for bid in pre_ids if after.get(bid)!=before.get(bid)]
        raise AssertionError(f'existing book content changed during civil integration: {changed}')
    final=json.loads(lp.read_text(encoding='utf-8'))
    if final['version']!=target or [b['id'] for b in final['books']]!=pre_ids+[BOOK]: raise AssertionError('civil final state drift')
    print(f'CIVIL_LAW_OVERVIEW_INTEGRATION_OK books={len(final["books"])} library={target} preserved_existing_books={len(pre_ids)}',file=sys.stderr)
    return target

if __name__=='__main__':
    if len(sys.argv)!=3: raise SystemExit('usage: python deploy/integrate_civil_law_overview.py SITE_ROOT EXPECTED_BEFORE')
    print(integrate(sys.argv[1],sys.argv[2]))
