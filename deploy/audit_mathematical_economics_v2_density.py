#!/usr/bin/env python3
from __future__ import annotations

import re

import generate_mathematical_economics as legacy
from mathematical_economics_v2_enrichment import CHAPTERS_V2


def main() -> None:
    legacy.CHAPTERS = CHAPTERS_V2
    lengths = []
    for chapter in CHAPTERS_V2:
        html = legacy.chapter_html(chapter)
        plain = re.sub(r'<[^>]+>', '', html)
        lengths.append((chapter['id'], len(plain), chapter['title']))
    for cid, length, title in lengths:
        print(f'{cid} chars={length} title={title}')
    thin = [(cid, length) for cid, length, _ in lengths if length < 700]
    print(f'MATHEMATICAL_ECONOMICS_V2_DENSITY thin_under_700={thin} min={min(x[1] for x in lengths)} max={max(x[1] for x in lengths)}')


if __name__ == '__main__':
    main()
