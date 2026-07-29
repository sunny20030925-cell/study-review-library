#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import binascii
import glob
import hashlib
import string
from pathlib import Path

BASE64_ALPHABET = string.ascii_uppercase + string.ascii_lowercase + string.digits + '+/'


def decode_payload(encoded: str) -> bytes:
    padded = encoded + ('=' * (-len(encoded) % 4))
    return base64.b64decode(padded, validate=True)


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Join ordered Base64 text parts, normalize whitespace and decode their combined payload.'
    )
    parser.add_argument('pattern', help='Glob pattern for ordered Base64 part files')
    parser.add_argument('output', help='Output binary path')
    parser.add_argument('--expected-sha256', help='Expected binary SHA-256; enables one-character boundary recovery')
    args = parser.parse_args()

    parts = [Path(path) for path in sorted(glob.glob(args.pattern))]
    if not parts:
        raise SystemExit(f'no files matched: {args.pattern}')

    chunks = [
        ''.join(part.read_text(encoding='utf-8').split())
        for part in parts
    ]
    encoded = ''.join(chunks)
    expected = args.expected_sha256.lower() if args.expected_sha256 else None
    decoded: bytes | None = None
    recovery: tuple[int, str] | None = None

    try:
        candidate = decode_payload(encoded)
        if expected is None or hashlib.sha256(candidate).hexdigest() == expected:
            decoded = candidate
    except binascii.Error:
        pass

    if decoded is None and expected:
        boundaries = []
        running = 0
        for chunk in chunks[:-1]:
            running += len(chunk)
            boundaries.append(running)

        positions = []
        for boundary in boundaries:
            for position in range(max(0, boundary - 64), min(len(encoded), boundary + 64) + 1):
                if position not in positions:
                    positions.append(position)

        for position in positions:
            prefix = encoded[:position]
            suffix = encoded[position:]
            for character in BASE64_ALPHABET:
                repaired = prefix + character + suffix
                try:
                    candidate = decode_payload(repaired)
                except binascii.Error:
                    continue
                if hashlib.sha256(candidate).hexdigest() == expected:
                    decoded = candidate
                    recovery = (position, character)
                    encoded = repaired
                    break
            if decoded is not None:
                break

    if decoded is None:
        lengths = ','.join(str(len(chunk)) for chunk in chunks)
        raise SystemExit(
            f'unable to decode or match expected SHA-256; parts={len(parts)} '
            f'chunk_lengths={lengths} combined_chars={len(encoded)} mod4={len(encoded) % 4}'
        )

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(decoded)
    digest = hashlib.sha256(decoded).hexdigest()
    recovery_text = 'none' if recovery is None else f'position={recovery[0]} character={recovery[1]!r}'
    print(
        f'DECODED_SPLIT_BASE64 parts={len(parts)} chunk_lengths={",".join(str(len(chunk)) for chunk in chunks)} '
        f'encoded_chars={len(encoded)} bytes={len(decoded)} sha256={digest} recovery={recovery_text} output={output}'
    )


if __name__ == '__main__':
    main()
