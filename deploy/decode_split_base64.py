#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import glob
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description='Decode separately padded Base64 file parts and concatenate their bytes.')
    parser.add_argument('pattern', help='Glob pattern for ordered Base64 part files')
    parser.add_argument('output', help='Output binary path')
    args = parser.parse_args()

    parts = [Path(path) for path in sorted(glob.glob(args.pattern))]
    if not parts:
        raise SystemExit(f'no files matched: {args.pattern}')

    decoded = bytearray()
    for part in parts:
        encoded = ''.join(part.read_text(encoding='utf-8').split())
        try:
            decoded.extend(base64.b64decode(encoded, validate=True))
        except ValueError as exc:
            raise SystemExit(f'invalid Base64 in {part}: {exc}') from exc

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(decoded)
    print(f'DECODED_SPLIT_BASE64 parts={len(parts)} bytes={len(decoded)} output={output}')


if __name__ == '__main__':
    main()
