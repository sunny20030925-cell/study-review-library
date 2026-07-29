#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import glob
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description='Join ordered Base64 text parts, normalize whitespace and decode their combined payload.')
    parser.add_argument('pattern', help='Glob pattern for ordered Base64 part files')
    parser.add_argument('output', help='Output binary path')
    args = parser.parse_args()

    parts = [Path(path) for path in sorted(glob.glob(args.pattern))]
    if not parts:
        raise SystemExit(f'no files matched: {args.pattern}')

    encoded = ''.join(
        ''.join(part.read_text(encoding='utf-8').split())
        for part in parts
    )
    padded = encoded + ('=' * (-len(encoded) % 4))
    try:
        decoded = base64.b64decode(padded, validate=True)
    except ValueError as exc:
        raise SystemExit(f'invalid combined Base64 payload from {len(parts)} parts: {exc}') from exc

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(decoded)
    print(
        f'DECODED_SPLIT_BASE64 parts={len(parts)} encoded_chars={len(encoded)} '
        f'padding_added={len(padded) - len(encoded)} bytes={len(decoded)} output={output}'
    )


if __name__ == '__main__':
    main()
