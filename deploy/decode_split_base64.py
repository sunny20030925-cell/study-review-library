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


def digest_match(encoded: str, expected: str | None) -> bytes | None:
    try:
        payload = decode_payload(encoded)
    except binascii.Error:
        return None
    if expected is not None and hashlib.sha256(payload).hexdigest() != expected:
        return None
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Join ordered Base64 text parts, diagnose transformations and recover a verified payload.'
    )
    parser.add_argument('pattern', help='Glob pattern for ordered Base64 part files')
    parser.add_argument('output', help='Output binary path')
    parser.add_argument('--expected-sha256', help='Expected binary SHA-256; required for any recovery')
    args = parser.parse_args()

    parts = [Path(path) for path in sorted(glob.glob(args.pattern))]
    if not parts:
        raise SystemExit(f'no files matched: {args.pattern}')

    chunks = [''.join(part.read_text(encoding='utf-8').split()) for part in parts]
    encoded = ''.join(chunks)
    expected = args.expected_sha256.lower() if args.expected_sha256 else None
    decoded: bytes | None = None
    recovery = 'none'

    transformations = [
        ('joined', encoded),
        ('part-order-reversed', ''.join(reversed(chunks))),
        ('all-characters-reversed', encoded[::-1]),
        ('each-part-reversed', ''.join(chunk[::-1] for chunk in chunks)),
        ('each-part-and-order-reversed', ''.join(chunk[::-1] for chunk in reversed(chunks))),
    ]
    seen = set()
    for label, candidate_text in transformations:
        if candidate_text in seen:
            continue
        seen.add(candidate_text)
        candidate = digest_match(candidate_text, expected)
        if candidate is not None:
            decoded = candidate
            encoded = candidate_text
            recovery = f'transformation={label}'
            break

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
                candidate = digest_match(repaired, expected)
                if candidate is not None:
                    decoded = candidate
                    encoded = repaired
                    recovery = f'boundary-insertion position={position} character={character!r}'
                    break
            if decoded is not None:
                break

    if decoded is None:
        equals = [index for index, character in enumerate(encoded) if character == '=']
        diagnostic_lines = [
            'BASE64_DIAGNOSTIC',
            f'parts={len(parts)}',
            f'chunk_lengths={",".join(str(len(chunk)) for chunk in chunks)}',
            f'combined_chars={len(encoded)} mod4={len(encoded) % 4}',
            f'combined_head={encoded[:48]!r}',
            f'combined_tail={encoded[-48:]!r}',
            f'chunk_heads={[chunk[:24] for chunk in chunks]!r}',
            f'chunk_tails={[chunk[-24:] for chunk in chunks]!r}',
            f'equals_count={len(equals)} equals_positions={equals[:20]!r}',
            f'H4sI_positions={[i for i in range(len(encoded)) if encoded.startswith("H4sI", i)][:20]!r}',
        ]
        for label, candidate_text in transformations:
            try:
                loose = base64.b64decode(candidate_text + ('=' * (-len(candidate_text) % 4)), validate=False)
                diagnostic_lines.append(f'{label}_decoded_head={loose[:12].hex()} decoded_tail={loose[-12:].hex()}')
            except Exception as exc:
                diagnostic_lines.append(f'{label}_decode_error={type(exc).__name__}:{exc}')
        raise SystemExit('\n'.join(diagnostic_lines))

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(decoded)
    digest = hashlib.sha256(decoded).hexdigest()
    print(
        f'DECODED_SPLIT_BASE64 parts={len(parts)} chunk_lengths={",".join(str(len(chunk)) for chunk in chunks)} '
        f'encoded_chars={len(encoded)} bytes={len(decoded)} sha256={digest} recovery={recovery} output={output}'
    )


if __name__ == '__main__':
    main()
