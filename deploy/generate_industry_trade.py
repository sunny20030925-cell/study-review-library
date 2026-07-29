#!/usr/bin/env python3
from __future__ import annotations
import base64, gzip, hashlib, sys
from pathlib import Path

SOURCE_SHA256='228b3217d79335ef56f086285e58efe958f9366f6932004f8b523be1a79a7832'
PARTS=[
    'generate-industry-trade.py.gz.b64.part01',
    'generate-industry-trade.py.gz.b64.part02',
    'generate-industry-trade.py.gz.b64.part03',
]

def load_source() -> bytes:
    root=Path(__file__).resolve().parent
    encoded=''.join((root/name).read_text(encoding='utf-8').strip() for name in PARTS)
    source=gzip.decompress(base64.b64decode(encoded))
    got=hashlib.sha256(source).hexdigest()
    if got!=SOURCE_SHA256:
        raise AssertionError(f'industry-trade source hash mismatch: {got}')
    return source

def main(site_root: str):
    source=load_source()
    ns={'__name__':'industry_trade_embedded','__file__':'<industry-trade-embedded>'}
    exec(compile(source,'<industry-trade-embedded>','exec'),ns)
    result=ns['generate'](site_root)
    print(result)

if __name__=='__main__':
    if len(sys.argv)!=2: raise SystemExit('usage: python deploy/generate_industry_trade.py SITE_ROOT')
    main(sys.argv[1])
