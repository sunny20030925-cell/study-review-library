from __future__ import annotations

import json
import re
import sys
from pathlib import Path

BOOK='computer-fundamentals'
TARGET_VERSION='2026.07.30-2'


def next_version(version: str) -> str:
    m=re.fullmatch(r'(\d{4}\.\d{2}\.\d{2})-(\d+)',version)
    if not m:
        raise AssertionError(f'invalid library version: {version}')
    return f'{m.group(1)}-{int(m.group(2))+1}'


def main(site_root: str, expected_before: str) -> str:
    site=Path(site_root)
    lp=site/'data/library.json'
    library=json.loads(lp.read_text(encoding='utf-8'))
    if library['version']!=expected_before:
        raise AssertionError(f'expected library {expected_before}, got {library["version"]}')
    ids=[b['id'] for b in library['books']]
    if BOOK not in ids:
        raise AssertionError('computer fundamentals missing from formal library')
    target=next_version(expected_before)
    library['version']=target
    for book in library['books']:
        if book.get('id')==BOOK:
            book['status']='available'
            if 'version' in book:
                book['version']=TARGET_VERSION
    lp.write_text(json.dumps(library,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

    swp=site/'sw.js'
    sw=swp.read_text(encoding='utf-8')
    sw,n=re.subn(r"const VERSION = 'study-library-[^']+';",f"const VERSION = 'study-library-{target}';",sw,count=1)
    if n!=1:
        raise AssertionError('service worker version marker missing')
    swp.write_text(sw,encoding='utf-8')
    print(target)
    return target


if __name__=='__main__':
    if len(sys.argv)!=3:
        raise SystemExit('usage: python deploy/finalize_computer_fundamentals_v2_library.py SITE_ROOT EXPECTED_BEFORE')
    main(sys.argv[1],sys.argv[2])
