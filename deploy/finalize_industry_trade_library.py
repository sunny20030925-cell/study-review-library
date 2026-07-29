#!/usr/bin/env python3
from __future__ import annotations
import json, re, sys
from pathlib import Path

BOOK_ID='industry-trade'

def next_library_version(version: str) -> str:
    m=re.fullmatch(r'(\d{4}\.\d{2}\.\d{2})-(\d+)',version)
    if not m: raise AssertionError(f'unexpected library version: {version}')
    return f'{m.group(1)}-{int(m.group(2))+1}'

def main(site_root: str, pre_library_path: str) -> str:
    site=Path(site_root); lp=site/'data/library.json'
    pre=json.loads(Path(pre_library_path).read_text(encoding='utf-8'))
    post=json.loads(lp.read_text(encoding='utf-8'))
    pre_ids=[b['id'] for b in pre['books']]; post_ids=[b['id'] for b in post['books']]
    if BOOK_ID in pre_ids: raise AssertionError(f'{BOOK_ID} already existed before generation')
    if post_ids != pre_ids+[BOOK_ID]: raise AssertionError(f'book order drift: before={pre_ids}, after={post_ids}')
    final=next_library_version(pre['version']); post['version']=final
    lp.write_text(json.dumps(post,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    swp=site/'sw.js'; sw=swp.read_text(encoding='utf-8')
    sw,n=re.subn(r"const VERSION = 'study-library-[^']+';",f"const VERSION = 'study-library-{final}';",sw,count=1)
    if n!=1: raise AssertionError('service worker version marker not found')
    swp.write_text(sw,encoding='utf-8')
    print(final); return final

if __name__=='__main__':
    if len(sys.argv)!=3: raise SystemExit('usage: python deploy/finalize_industry_trade_library.py SITE_ROOT PRE_LIBRARY_JSON')
    main(sys.argv[1],sys.argv[2])
