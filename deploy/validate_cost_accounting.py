from __future__ import annotations

import json
import sys
from pathlib import Path

from patch_cost_accounting_v2 import main as apply_v2_patch
from validate_cost_accounting_v2_core import main as validate_v2

SOURCE_VERSION = "2026.07.29-1"
TARGET_VERSION = "2026.07.29-2"


def main(site_arg: str) -> None:
    manifest_path = Path(site_arg) / "books" / "cost-accounting" / "manifest.json"
    version = json.loads(manifest_path.read_text(encoding="utf-8"))["version"]
    if version == SOURCE_VERSION:
        apply_v2_patch(site_arg)
    elif version != TARGET_VERSION:
        raise AssertionError(f"unexpected cost accounting version before validation: {version}")
    validate_v2(site_arg)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python validate_cost_accounting.py SITE_ROOT")
    main(sys.argv[1])
