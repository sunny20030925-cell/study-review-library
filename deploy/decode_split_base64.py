#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import binascii
import glob
import hashlib
import multiprocessing as mp
import os
import string
from pathlib import Path

BASE64_ALPHABET = string.ascii_uppercase + string.ascii_lowercase + string.digits + '+/'
_SEARCH_BASE = ''
_SEARCH_EXPECTED = ''


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


def _search_range(position_range: tuple[int, int]) -> tuple[int, str, bytes] | None:
    start, stop = position_range
    base = _SEARCH_BASE
    expected = _SEARCH_EXPECTED
    for position in range(start, stop):
        prefix = base[:position]
        suffix = base[position:]
        for character in BASE64_ALPHABET:
            candidate_text = prefix + character + suffix
            try:
                payload = base64.b64decode(candidate_text, validate=True)
            except binascii.Error:
                continue
            if hashlib.sha256(payload).hexdigest() == expected:
                return position, character, payload
    return None


def _full_verified_insertion_search(base: str, expected: str) -> tuple[int, str, bytes] | None:
    global _SEARCH_BASE, _SEARCH_EXPECTED
    _SEARCH_BASE = base
    _SEARCH_EXPECTED = expected
    data_end = base.find('=')
    if data_end < 0:
        data_end = len(base)
    chunk_size = 192
    ranges = [(start, min(start + chunk_size, data_end + 1)) for start in range(0, data_end + 1, chunk_size)]
    process_count = max(1, min(4, os.cpu_count() or 1))
    print(
        f'FULL_INSERTION_SEARCH positions={data_end + 1} alphabet={len(BASE64_ALPHABET)} '
        f'candidates={(data_end + 1) * len(BASE64_ALPHABET)} processes={process_count}',
        flush=True,
    )
    context = mp.get_context('fork')
    with context.Pool(processes=process_count) as pool:
        for result in pool.imap_unordered(_search_range, ranges, chunksize=1):
            if result is not None:
                pool.terminate()
                pool.join()
                return result
    return None


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Join ordered Base64 text parts, diagnose corruption and recover only a checksum-verified payload.'
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
        gzip_header_repaired = 'H4sI' + encoded[4:]
        cheap_positions = set(range(0, min(96, len(gzip_header_repaired) + 1)))
        data_end = gzip_header_repaired.find('=')
        if data_end < 0:
            data_end = len(gzip_header_repaired)
        for boundary in [sum(len(chunk) for chunk in chunks[:index]) for index in range(1, len(chunks))]:
            cheap_positions.update(range(max(0, boundary - 96), min(data_end, boundary + 96) + 1))
        cheap_positions.update(range(max(0, data_end - 96), data_end + 1))
        for position in sorted(cheap_positions):
            prefix = gzip_header_repaired[:position]
            suffix = gzip_header_repaired[position:]
            for character in BASE64_ALPHABET:
                repaired = prefix + character + suffix
                candidate = digest_match(repaired, expected)
                if candidate is not None:
                    decoded = candidate
                    encoded = repaired
                    recovery = f'gzip-header-plus-selected-insertion position={position} character={character!r}'
                    break
            if decoded is not None:
                break

        if decoded is None:
            result = _full_verified_insertion_search(gzip_header_repaired, expected)
            if result is not None:
                position, character, payload = result
                decoded = payload
                encoded = gzip_header_repaired[:position] + character + gzip_header_repaired[position:]
                recovery = f'gzip-header-plus-full-insertion position={position} character={character!r}'

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
            'full_checksum_verified_insertion_search=no_match',
        ]
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
