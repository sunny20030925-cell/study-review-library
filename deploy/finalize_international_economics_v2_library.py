#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

BOOK_ID = "international-economics"
TARGET_VERSION = "2026.07.29-2"


def next_library_version(version: str) -> str:
    m = re.fullmatch(r"(\d{4}\.\d{2}\.\d{2})-(\d+)", version)
    if not m:
        raise AssertionError(f"unexpected library version: {version}")
    return f"{m.group(1)}-{int(m.group(2)) + 1}"


def main(site_root: str, expected_before: str) -> None:
    site = Path(site_root)
    library_path = site / "data/library.json"
    library = json.loads(library_path.read_text(encoding="utf-8"))
    if library["version"] != expected_before:
        raise AssertionError(
            f"international v2 pre-version expected {expected_before}, got {library['version']}"
        )
    ids = [book["id"] for book in library["books"]]
    if len(ids) != 11 or ids[-3:] != ["macroeconomics", BOOK_ID, "public-finance"]:
        raise AssertionError(f"unexpected eleven-book tail: {ids[-3:]}")

    root = site / "books" / BOOK_ID
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    questions = json.loads((root / "questions.json").read_text(encoding="utf-8"))
    if manifest["version"] != TARGET_VERSION or questions["version"] != TARGET_VERSION:
        raise AssertionError("international economics v2 content not applied before finalizing")

    final = next_library_version(expected_before)
    library["version"] = final
    library_path.write_text(
        json.dumps(library, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    sw_path = site / "sw.js"
    sw = sw_path.read_text(encoding="utf-8")
    sw, count = re.subn(
        r"const VERSION = 'study-library-[^']+';",
        f"const VERSION = 'study-library-{final}';",
        sw,
        count=1,
    )
    if count != 1:
        raise AssertionError("service-worker version marker not found")
    sw_path.write_text(sw, encoding="utf-8")
    print(final)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(
            "usage: finalize_international_economics_v2_library.py SITE_ROOT EXPECTED_BEFORE"
        )
    main(sys.argv[1], sys.argv[2])
