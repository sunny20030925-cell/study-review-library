#!/usr/bin/env python3
from __future__ import annotations

import contextlib
import hashlib
import io
import json
import sys
from pathlib import Path

from finalize_game_theory_v2_library import main as finalize_v2
from patch_game_theory_v2 import SOURCE_VERSION, TARGET_VERSION, main as patch_v2
from qa_game_theory_second_pass import main as qa_source_second_pass
from qa_game_theory_v2 import main as qa_artifact_v2

BOOK = 'game-theory'


def file_tree_hash(root: Path, exclude_prefixes: tuple[str, ...] = ()) -> str:
    digest = hashlib.sha256()
    for path in sorted(p for p in root.rglob('*') if p.is_file()):
        rel = path.relative_to(root).as_posix()
        if any(rel.startswith(prefix) for prefix in exclude_prefixes):
            continue
        digest.update(rel.encode('utf-8'))
        digest.update(b'\0')
        digest.update(path.read_bytes())
        digest.update(b'\0')
    return digest.hexdigest()


def emit_stderr(buf: io.StringIO) -> None:
    text = buf.getvalue()
    if text:
        print(text, end='', file=sys.stderr)


def main(site_root: str) -> str:
    site = Path(site_root)
    library_path = site / 'data/library.json'
    library = json.loads(library_path.read_text(encoding='utf-8'))
    before_version = library['version']
    before_ids = [book['id'] for book in library['books']]
    if before_ids.count(BOOK) != 1:
        raise AssertionError(f'game-theory registry count drift: {before_ids}')

    manifest_path = site / 'books' / BOOK / 'manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    current_content_version = manifest.get('version')
    if current_content_version not in {SOURCE_VERSION, TARGET_VERSION}:
        raise AssertionError(f'unexpected game-theory content version: {current_content_version}')

    other_books_hash = file_tree_hash(site / 'books', (f'{BOOK}/',))
    other_assets_hash = file_tree_hash(site / 'assets', ('game-theory-svg/',))
    app_hash = hashlib.sha256((site / 'app.js').read_bytes()).hexdigest()

    if current_content_version == SOURCE_VERSION:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            patch_v2(str(site))
        emit_stderr(buf)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            final_version = finalize_v2(str(site), before_version)
        emit_stderr(buf)
        action = 'patched'
    else:
        final_version = before_version
        action = 'already-v2'

    after_library = json.loads(library_path.read_text(encoding='utf-8'))
    after_ids = [book['id'] for book in after_library['books']]
    if after_ids != before_ids:
        raise AssertionError(f'book registry changed during game-theory v2 release: before={before_ids}, after={after_ids}')
    if after_library['version'] != final_version:
        raise AssertionError(f'final library version drift: {after_library["version"]} != {final_version}')

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        qa_artifact_v2(str(site), final_version)
    emit_stderr(buf)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        qa_source_second_pass()
    emit_stderr(buf)

    if file_tree_hash(site / 'books', (f'{BOOK}/',)) != other_books_hash:
        raise AssertionError('non-game-theory book content changed')
    if file_tree_hash(site / 'assets', ('game-theory-svg/',)) != other_assets_hash:
        raise AssertionError('non-game-theory assets changed')
    if hashlib.sha256((site / 'app.js').read_bytes()).hexdigest() != app_hash:
        raise AssertionError('shared app.js changed')

    final_manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    if final_manifest.get('version') != TARGET_VERSION:
        raise AssertionError(f'game-theory target version missing: {final_manifest.get("version")}')

    print(
        f'GAME_THEORY_V2_RELEASE_OK action={action} books={len(after_ids)} '
        f'library={final_version} content={TARGET_VERSION}',
        file=sys.stderr,
    )
    print(final_version)
    return final_version


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: python deploy/apply_game_theory_v2_release.py SITE_ROOT')
    main(sys.argv[1])
