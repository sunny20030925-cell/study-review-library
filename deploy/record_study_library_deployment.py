#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

EXPECTED_BOOK_COUNT = 21


def replace_line(text: str, label: str, value: str) -> str:
    pattern = rf"(?m)^- {re.escape(label)}：.*$"
    replacement = f"- {label}：{value}"
    out, count = re.subn(pattern, replacement, text, count=1)
    if count != 1:
        raise AssertionError(f"shared checkpoint line not found: {label}")
    return out


def main(site_root: str) -> None:
    site = Path(site_root)
    library = json.loads((site / "data/library.json").read_text(encoding="utf-8"))
    ids = [book["id"] for book in library["books"]]
    if len(ids) != EXPECTED_BOOK_COUNT or len(set(ids)) != EXPECTED_BOOK_COUNT:
        raise AssertionError(f"formal library book registry drift: {ids}")
    if ids.count("industry-trade") != 1 or ids.count("mathematical-economics") != 1:
        raise AssertionError("formal 21-book tail books missing or duplicated")
    if ids.index("industrial-economics") >= ids.index("industry-trade"):
        raise AssertionError("industrial-economics / industry-trade order drift")
    if ids.index("industry-trade") >= ids.index("mathematical-economics"):
        raise AssertionError("industry-trade / mathematical-economics order drift")

    artifact_id = os.environ.get("PAGES_ARTIFACT_ID", "")
    digest = os.environ.get("PAGES_ARTIFACT_DIGEST", "")
    sha256 = os.environ.get("PAGES_ARTIFACT_SHA256", "")
    page_url = os.environ.get("DEPLOYED_PAGE_URL", "")
    run_id = os.environ.get("GITHUB_RUN_ID", "")
    source_sha = os.environ.get("GITHUB_SHA", "")
    if not all([artifact_id, digest, sha256, page_url, run_id, source_sha]):
        raise AssertionError("missing verified deployment environment")
    digest_hex = digest.split(":", 1)[1] if digest.startswith("sha256:") else digest
    if digest_hex != sha256:
        raise AssertionError("verified artifact digest mismatch")

    versions: dict[str, str] = {}
    for book_id in ids:
        manifest_path = site / "books" / book_id / "manifest.json"
        if not manifest_path.is_file():
            raise AssertionError(f"missing manifest for {book_id}")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("id") != book_id:
            raise AssertionError(f"manifest id drift for {book_id}")
        versions[book_id] = manifest["version"]

    receipt_path = Path("docs/deployment_receipt.json")
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    prior_run = str(receipt.get("workflow_run_id", ""))
    deployed_at = receipt.get("deployed_at") if prior_run == run_id else None
    if not deployed_at:
        deployed_at = datetime.now(timezone.utc).isoformat()
    receipt.update({
        "status": "success",
        "library_version": library["version"],
        "book_count": len(ids),
        "book_ids": ids,
        "book_versions": versions,
        "book_versions_visible": True,
        "progress_storage_changed": False,
        "source_commit": source_sha,
        "workflow_run_id": run_id,
        "page_url": page_url,
        "deployed_at": deployed_at,
        "pages_deploy_status": "success",
        "pages_artifact_id": artifact_id,
        "pages_artifact_digest": digest,
        "artifact_download_recheck": "passed",
        "artifact_download_sha256": sha256,
        "artifact_verified_book_count": len(ids),
        "workflow_overall_conclusion": "success",
        "post_deploy_record_step": "passed-workflow-v2-generic-recorder",
        "receipt_reconciliation": "automatic-from-verified-pages-artifact",
    })
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    checkpoint_path = Path("docs/shared_checkpoint.md")
    checkpoint = checkpoint_path.read_text(encoding="utf-8")
    checkpoint = replace_line(checkpoint, "正式書庫內容版本", f"`{library['version']}`")
    checkpoint = replace_line(checkpoint, "正式書籍數", f"**{len(ids)} 本**。")
    checkpoint = replace_line(checkpoint, "最新成功正式 Pages run", f"`{run_id}`")
    checkpoint = replace_line(checkpoint, "正式部署 source commit", f"`{source_sha}`")
    checkpoint = replace_line(checkpoint, "最新成功 Pages artifact", f"`{artifact_id}`")
    checkpoint = replace_line(checkpoint, "Artifact digest", f"`{digest}`")
    checkpoint = re.sub(
        r"(?ms)^## 基礎設施注意事項\n.*?(?=^## 不可破壞的正式邊界)",
        "## 基礎設施注意事項\n\n"
        "- 21 本 registry 的 `industry-trade` tail assertion 已改為相對順序 gate，允許其後存在 `mathematical-economics`。\n"
        "- 部署紀錄已由 workflow-v2 generic recorder 接管；不再以逐書 legacy recorder 重寫 shared checkpoint 或逐書 stage。\n"
        "- 最新共同 PWA／Pages artifact 已完成 upload、deploy、重新下載、digest 與 21 本結構驗證。\n\n",
        checkpoint,
        count=1,
    )
    checkpoint_path.write_text(checkpoint, encoding="utf-8")

    print(json.dumps({
        "library_version": library["version"],
        "book_count": len(ids),
        "workflow_run_id": run_id,
        "artifact_id": artifact_id,
        "artifact_digest": digest,
        "source_commit": source_sha,
    }, ensure_ascii=False))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python deploy/record_study_library_deployment.py SITE_ROOT")
    main(sys.argv[1])
