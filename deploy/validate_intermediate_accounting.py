from __future__ import annotations

import json
import os
import sys
from collections import Counter
from pathlib import Path

BOOK_ID = "intermediate-accounting"
BOOK_VERSION = "2026.07.29-1"
REQUIRED_PRE_IDS = {
    "calculus", "accounting", "economics", "statistics",
    "commercial-law", "cost-accounting", "microeconomics",
}


def main() -> None:
    site = Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
    expected_version = os.environ.get("EXPECTED_LIBRARY_VERSION")
    pre_path = os.environ.get("PRE_LIBRARY_JSON")
    if not expected_version or not pre_path:
        raise SystemExit("EXPECTED_LIBRARY_VERSION and PRE_LIBRARY_JSON are required")

    pre = json.loads(Path(pre_path).read_text(encoding="utf-8"))
    library = json.loads((site / "data/library.json").read_text(encoding="utf-8"))
    pre_ids = [book["id"] for book in pre["books"]]
    post_ids = [book["id"] for book in library["books"]]
    assert REQUIRED_PRE_IDS.issubset(set(pre_ids)), pre_ids
    assert BOOK_ID not in pre_ids
    assert post_ids == pre_ids + [BOOK_ID]
    assert library["version"] == expected_version

    for existing_id in pre_ids:
        root = site / "books" / existing_id
        manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
        questions = json.loads((root / "questions.json").read_text(encoding="utf-8"))
        search = json.loads((root / "search.json").read_text(encoding="utf-8"))
        assert manifest["id"] == existing_id
        assert questions["count"] == len(questions["items"]) > 0
        assert search["entries"]

    root = site / "books" / BOOK_ID
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    questions = json.loads((root / "questions.json").read_text(encoding="utf-8"))
    search = json.loads((root / "search.json").read_text(encoding="utf-8"))
    assert manifest["version"] == questions["version"] == BOOK_VERSION
    chapters = [item for item in manifest["chapters"] if item["kind"] == "chapter"]
    appendices = [item for item in manifest["chapters"] if item["kind"] == "appendix"]
    assert len(chapters) == 22
    assert len(appendices) == 3
    assert questions["count"] == len(questions["items"]) == 110
    assert len(search["entries"]) == 145
    assert Counter(q["chapterId"] for q in questions["items"]) == {f"ch{i:02d}": 5 for i in range(22)}
    assert len({q["id"] for q in questions["items"]}) == 110

    for chapter in manifest["chapters"]:
        path = root / chapter["file"]
        assert path.is_file() and path.stat().st_size > 300
    for chapter in chapters:
        assert not any(term in chapter["title"] for term in ("企業合併", "合併財務報表", "外幣換算", "分公司會計"))

    all_text = "\n".join((root / item["file"]).read_text(encoding="utf-8") for item in manifest["chapters"])
    for token in (
        "IFRS 9", "IFRS 15", "IFRS 16", "IAS 12", "IFRS 18", "2028",
        "預期信用損失", "有效利率", "可回收金額", "遞延所得稅", "每股盈餘", "現金流量",
    ):
        assert token in all_text, token
    assert "\x00" not in all_text and "\x0c" not in all_text

    figures = sorted((site / "assets/intermediate-accounting-svg").glob("*.svg"))
    assert len(figures) == 22
    for figure in figures:
        svg = figure.read_text(encoding="utf-8")
        assert "<title" in svg and "<desc" in svg and "viewBox" in svg

    sw = (site / "sw.js").read_text(encoding="utf-8")
    assert f"study-library-{expected_version}" in sw
    for path in (
        "./books/cost-accounting/manifest.json",
        "./books/microeconomics/manifest.json",
        "./books/intermediate-accounting/manifest.json",
        "./books/intermediate-accounting/questions.json",
        "./books/intermediate-accounting/search.json",
        "./books/intermediate-accounting/chapters/ch21.html",
        "./books/intermediate-accounting/chapters/appendix-c.html",
        "./assets/intermediate-accounting-svg/ch21.svg",
    ):
        assert path in sw, path

    app = (site / "app.js").read_text(encoding="utf-8")
    styles = (site / "styles.css").read_text(encoding="utf-8")
    assert "查看版本與更新內容" in app
    assert ".release-notes{" in styles

    quantitative = {
        "present_value": abs(110000 / (1.10 ** 2) - 90909.090909) < 1e-6,
        "ecl": 800000 * 0.02 == 16000,
        "inventory_nrv": 128000 - 6000 - 5000 == 117000,
        "depreciation": (600000 - 100000) / 5 == 100000,
        "bond_interest": 940000 * 0.06 == 56400,
        "bond_amortisation": 56400 - 40000 == 16400,
        "basic_eps": 560000 / 112000 == 5,
        "lease_liability": 500000 + 25000 - 120000 == 405000,
        "dtl": (800000 - 700000) * 0.20 == 20000,
        "cfo": 500000 + 80000 - 60000 + 30000 + 20000 == 570000,
    }
    assert all(quantitative.values())

    print(
        "INTERMEDIATE_ACCOUNTING_VALIDATION_OK "
        f"books={len(post_ids)} library={expected_version} chapters=22 appendices=3 "
        "questions=110 search=145 figures=22 quantitative=10"
    )


if __name__ == "__main__":
    main()
