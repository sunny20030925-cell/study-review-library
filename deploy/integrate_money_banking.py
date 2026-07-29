#!/usr/bin/env python3
from __future__ import annotations

import base64
import contextlib
import gzip
import hashlib
import importlib.util
import io
import json
import re
import sys
import tempfile
from pathlib import Path

GENERATOR_SHA256='e31937c06988a26fd52e8f056eb7432ae2cac136e4aebb1ab7fab6ccf15b96bb'
BOOK='money-banking'


def load_module(path: Path, name: str):
    spec=importlib.util.spec_from_file_location(name,path)
    if spec is None or spec.loader is None:
        raise AssertionError(f'cannot load {path}')
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def emit_stderr(buf: io.StringIO):
    txt=buf.getvalue()
    if txt:
        print(txt,end='',file=sys.stderr)


def next_version(version: str) -> str:
    m=re.fullmatch(r'(\d{4}\.\d{2}\.\d{2})-(\d+)',version)
    if not m:
        raise AssertionError(f'unexpected library version: {version}')
    return f'{m.group(1)}-{int(m.group(2))+1}'


def integrate(site_root: str, expected_before: str) -> str:
    site=Path(site_root)
    deploy=Path(__file__).resolve().parent
    libp=site/'data/library.json'
    pre=json.loads(libp.read_text(encoding='utf-8'))
    pre_ids=[b['id'] for b in pre['books']]
    if pre['version']!=expected_before:
        raise AssertionError(f'money-banking pre-version expected {expected_before}, got {pre["version"]}')
    if BOOK in pre_ids:
        raise AssertionError('money-banking already present before integration')
    if not pre_ids or pre_ids[-1]!='public-finance':
        raise AssertionError(f'money-banking integration requires public-finance tail, got {pre_ids[-4:]}')

    parts=sorted(deploy.glob('generate-money-banking.py.gz.b64.part*'))
    if not parts:
        raise AssertionError('money-banking generator package parts missing')
    encoded=''.join(''.join(p.read_text(encoding='utf-8').split()) for p in parts)
    gz=base64.b64decode(encoded,validate=True)
    digest=hashlib.sha256(gz).hexdigest()
    if digest!=GENERATOR_SHA256:
        raise AssertionError(f'money-banking generator sha256 mismatch: {digest}')
    source=gzip.decompress(gz)
    tmpgen=Path(tempfile.gettempdir())/'generate-money-banking.py'
    tmpgen.write_bytes(source)
    compile(source,str(tmpgen),'exec')

    gen=load_module(tmpgen,'generate_money_banking_runtime')
    qa=load_module(deploy/'validate_money_banking.py','validate_money_banking_runtime')

    buf=io.StringIO()
    with contextlib.redirect_stdout(buf):
        gen.build(str(site))
    emit_stderr(buf)

    post=json.loads(libp.read_text(encoding='utf-8'))
    final=post['version']
    if final!=next_version(expected_before):
        raise AssertionError(f'money-banking version expected {next_version(expected_before)}, got {final}')
    if [b['id'] for b in post['books']]!=pre_ids+[BOOK]:
        raise AssertionError('money-banking book order drift')

    buf=io.StringIO()
    with contextlib.redirect_stdout(buf):
        qa.main(str(site))
    emit_stderr(buf)
    print('MONEY_BANKING_CANONICAL_INTEGRATION_OK',file=sys.stderr)
    return final


if __name__=='__main__':
    if len(sys.argv)!=3:
        raise SystemExit('usage: integrate_money_banking.py SITE_ROOT EXPECTED_BEFORE')
    print(integrate(sys.argv[1],sys.argv[2]))
