#!/usr/bin/env python3
from __future__ import annotations

import base64
import gzip
import hashlib
import subprocess
import sys
import tempfile
from pathlib import Path

EXPECTED_GZIP_SHA256 = 'e31937c06988a26fd52e8f056eb7432ae2cac136e4aebb1ab7fab6ccf15b96bb'


def main(site_root: str) -> None:
    repo = Path.cwd()
    deploy = repo / 'deploy'
    parts = sorted(deploy.glob('generate-money-banking.py.gz.b64.part*'))
    if not parts:
        raise AssertionError('money-banking generator package parts missing')

    encoded = ''.join(''.join(p.read_text(encoding='utf-8').split()) for p in parts)
    payload = base64.b64decode(encoded, validate=True)
    digest = hashlib.sha256(payload).hexdigest()
    if digest != EXPECTED_GZIP_SHA256:
        raise AssertionError(f'money-banking generator checksum mismatch: {digest}')

    source = gzip.decompress(payload)
    with tempfile.TemporaryDirectory(prefix='money-banking-') as td:
        script = Path(td) / 'generate-money-banking.py'
        script.write_bytes(source)
        subprocess.run([sys.executable, '-m', 'py_compile', str(script)], check=True)
        subprocess.run([sys.executable, str(script), site_root], check=True)

    subprocess.run([sys.executable, str(deploy / 'validate_money_banking.py'), site_root], check=True)
    subprocess.run(['node', '--check', str(Path(site_root) / 'app.js')], check=True)
    subprocess.run(['node', '--check', str(Path(site_root) / 'sw.js')], check=True)
    print('MONEY_BANKING_CANONICAL_INTEGRATION_OK')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: integrate_money_banking.py SITE_ROOT')
    main(sys.argv[1])
