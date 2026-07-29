#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

BOOK = 'mathematical-economics'
BAD = "\\'"
GOOD = "'"


def normalize_text_file(path: Path) -> int:
    text = path.read_text(encoding='utf-8')
    count = text.count(BAD)
    if count:
        path.write_text(text.replace(BAD, GOOD), encoding='utf-8')
    return count


def main(site_root: str) -> int:
    site = Path(site_root)
    root = site / 'books' / BOOK
    if not root.is_dir():
        raise AssertionError(f'missing generated book root: {root}')

    replacements = 0
    for path in sorted(root.rglob('*')):
        if path.is_file() and path.suffix in {'.html', '.json'}:
            replacements += normalize_text_file(path)

    # Search and quiz JSON must remain parseable after normalization.
    for name in ('manifest.json', 'questions.json', 'search.json'):
        json.loads((root / name).read_text(encoding='utf-8'))

    if replacements <= 0:
        raise AssertionError('expected derivative-prime normalization replacements')

    print(f'MATHEMATICAL_ECONOMICS_OUTPUT_NORMALIZED replacements={replacements}', file=sys.stderr)
    return replacements


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: normalize_mathematical_economics_output.py SITE_ROOT')
    main(sys.argv[1])
