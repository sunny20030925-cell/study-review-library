#!/usr/bin/env python3
from __future__ import annotations

import base64
import gzip
import hashlib
import io
import json
import os
import re
import subprocess
import sys
from contextlib import redirect_stdout
from pathlib import Path


INTERMEDIATE_GENERATOR_SHA256 = "b60133689f2ede497597295688b82646ba070b787ea94a78e950da5603b8bf34"


def next_library_version(version: str) -> str:
    match = re.fullmatch(r"(\d{4}\.\d{2}\.\d{2})-(\d+)", version)
    if not match:
        raise AssertionError(f"unexpected library version: {version}")
    return f"{match.group(1)}-{int(match.group(2)) + 1}"


def run_logged(command: list[str], *, env: dict[str, str] | None = None) -> None:
    result = subprocess.run(
        command,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=env,
    )
    if result.stdout:
        print(result.stdout, file=sys.stderr, end="" if result.stdout.endswith("\n") else "\n")
    if result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, command, output=result.stdout)


def generate_and_validate_intermediate_accounting(site_root: str) -> str:
    repo_root = Path(__file__).resolve().parent.parent
    deploy_dir = repo_root / "deploy"
    parts = sorted(deploy_dir.glob("generate-intermediate-accounting.py.gz.b64.part*"))
    if not parts:
        raise AssertionError("intermediate accounting generator parts not found")

    encoded = "".join(part.read_text(encoding="utf-8") for part in parts)
    compressed = base64.b64decode("".join(encoded.split()), validate=True)
    digest = hashlib.sha256(compressed).hexdigest()
    if digest != INTERMEDIATE_GENERATOR_SHA256:
        raise AssertionError(f"intermediate accounting generator checksum mismatch: {digest}")

    generator_path = Path("/tmp/generate-intermediate-accounting.py")
    generator_path.write_bytes(gzip.decompress(compressed))

    site = Path(site_root)
    pre_library_path = Path("/tmp/pre-intermediate-accounting-library.json")
    pre_library_path.write_text(
        (site / "data/library.json").read_text(encoding="utf-8"),
        encoding="utf-8",
    )

    run_logged([sys.executable, str(generator_path), site_root])

    from finalize_intermediate_accounting_library import main as finalize_intermediate

    captured = io.StringIO()
    with redirect_stdout(captured):
        finalize_intermediate(site_root, str(pre_library_path))
    final_version = captured.getvalue().strip()
    if not re.fullmatch(r"\d{4}\.\d{2}\.\d{2}-\d+", final_version):
        raise AssertionError(f"unexpected intermediate accounting final version: {final_version!r}")

    validation_env = os.environ.copy()
    validation_env.update(
        {
            "EXPECTED_LIBRARY_VERSION": final_version,
            "PRE_LIBRARY_JSON": str(pre_library_path),
        }
    )
    run_logged(
        [sys.executable, str(deploy_dir / "validate_intermediate_accounting.py"), site_root],
        env=validation_env,
    )
    return final_version


def main(site_root: str, pre_library_path: str) -> None:
    site = Path(site_root)
    library_path = site / "data/library.json"
    pre = json.loads(Path(pre_library_path).read_text(encoding="utf-8"))
    post = json.loads(library_path.read_text(encoding="utf-8"))

    pre_ids = [book["id"] for book in pre["books"]]
    post_ids = [book["id"] for book in post["books"]]
    if "microeconomics" in pre_ids:
        raise AssertionError("microeconomics already existed before generation")
    if post_ids != pre_ids + ["microeconomics"]:
        raise AssertionError(f"book order drift: before={pre_ids}, after={post_ids}")

    micro_version = next_library_version(pre["version"])
    post["version"] = micro_version
    library_path.write_text(json.dumps(post, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    sw_path = site / "sw.js"
    sw = sw_path.read_text(encoding="utf-8")
    sw, count = re.subn(
        r"const VERSION = 'study-library-[^']+';",
        f"const VERSION = 'study-library-{micro_version}';",
        sw,
        count=1,
    )
    if count != 1:
        raise AssertionError("service worker version marker not found")
    sw_path.write_text(sw, encoding="utf-8")

    final_version = generate_and_validate_intermediate_accounting(site_root)
    print(final_version)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: finalize_microeconomics_library.py SITE_ROOT PRE_LIBRARY_JSON")
    main(sys.argv[1], sys.argv[2])
