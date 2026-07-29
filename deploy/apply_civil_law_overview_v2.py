#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

from civil_law_overview_v2_corrections import VERSION
from patch_civil_law_overview_v2 import main as patch_main

BOOK = 'civil-law-overview'


def main(site_root: str) -> str:
    site = Path(site_root)
    root = site / 'books' / BOOK
    manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    questions = json.loads((root / 'questions.json').read_text(encoding='utf-8'))
    library = json.loads((site / 'data/library.json').read_text(encoding='utf-8'))
    if manifest.get('version') == VERSION and questions.get('version') == VERSION:
        print(f'CIVIL_LAW_V2_ALREADY_APPLIED book={VERSION} library={library["version"]}')
        print(library['version'])
        return library['version']
    return patch_main(site_root)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: python deploy/apply_civil_law_overview_v2.py SITE_ROOT')
    main(sys.argv[1])
