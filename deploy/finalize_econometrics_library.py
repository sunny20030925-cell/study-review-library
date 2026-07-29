#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

BOOK_ID='econometrics'


def next_library_version(version: str) -> str:
    match=re.fullmatch(r'(\d{4}\.\d{2}\.\d{2})-(\d+)',version)
    if not match: raise AssertionError(f'unexpected library version: {version}')
    return f'{match.group(1)}-{int(match.group(2))+1}'


def main(site_root: str, pre_library_path: str) -> None:
    site=Path(site_root); library_path=site/'data/library.json'
    pre=json.loads(Path(pre_library_path).read_text(encoding='utf-8')); post=json.loads(library_path.read_text(encoding='utf-8'))
    pre_ids=[b['id'] for b in pre['books']]; post_ids=[b['id'] for b in post['books']]
    if BOOK_ID in pre_ids: raise AssertionError(f'{BOOK_ID} already existed before generation')
    if post_ids!=pre_ids+[BOOK_ID]: raise AssertionError(f'book order drift: before={pre_ids}, after={post_ids}')
    final_version=next_library_version(pre['version']); post['version']=final_version; library_path.write_text(json.dumps(post,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    sw_path=site/'sw.js'; sw=sw_path.read_text(encoding='utf-8')
    sw,count=re.subn(r"const VERSION = 'study-library-[^']+';",f"const VERSION = 'study-library-{final_version}';",sw,count=1)
    if count!=1: raise AssertionError('service worker version marker not found')
    sw_path.write_text(sw,encoding='utf-8'); print(final_version)


if __name__=='__main__':
    if len(sys.argv)!=3: raise SystemExit('usage: python deploy/finalize_econometrics_library.py SITE_ROOT PRE_LIBRARY_JSON')
    main(sys.argv[1],sys.argv[2])
