#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path

from investments_v2_corrections import (
    HTML_REPLACEMENTS,
    OLD_VERSION,
    QUESTION_UPDATES,
    UPDATED_AT,
    VERSION,
)

BOOK = "investments"
RELEASE_DATE = "2026.07.30"


def jdump(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=2) + "\n"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    n = text.count(old)
    if n != 1:
        raise AssertionError(f"{label}: expected exactly one old fragment, found {n}")
    return text.replace(old, new, 1)


def next_library_version(current: str) -> str:
    m = re.fullmatch(r"(\d{4}\.\d{2}\.\d{2})-(\d+)", current)
    if not m:
        raise AssertionError(f"unexpected library version: {current}")
    date, serial = m.group(1), int(m.group(2))
    if date < RELEASE_DATE:
        return f"{RELEASE_DATE}-1"
    return f"{date}-{serial + 1}"


class SectionTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.current_section = None
        self.in_h2 = False
        self.h2_parts = []
        self.in_lead = False
        self.lead_parts = []
        self.sections = defaultdict(list)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "h2":
            self.in_h2 = True
            self.h2_parts = []
        if tag == "p" and "lead" in attrs.get("class", "").split():
            self.in_lead = True

    def handle_endtag(self, tag):
        if tag == "h2":
            self.in_h2 = False
            self.current_section = " ".join(self.h2_parts).strip()
        if tag == "p":
            self.in_lead = False

    def handle_data(self, data):
        data = data.strip()
        if not data:
            return
        if self.in_h2:
            self.h2_parts.append(data)
        elif self.current_section:
            self.sections[self.current_section].append(data)
        if self.in_lead:
            self.lead_parts.append(data)


def search_pages_from_html(raw: str) -> dict[int, str]:
    p = SectionTextParser()
    p.feed(raw)
    section_by_page = {
        1: "正式定義與核心概念",
        2: "核心公式與成立條件",
        3: "完整標準例題",
        4: "常見錯誤",
        5: "考試判斷方法",
        6: "理解檢查",
    }
    overview = p.lead_parts + p.sections.get("本章要解決的問題", []) + p.sections.get("白話直覺", [])
    out = {0: " ".join(overview)}
    for page, section in section_by_page.items():
        out[page] = " ".join(p.sections.get(section, []))
    return out


def main(site_root: str) -> str:
    site = Path(site_root)
    root = site / "books" / BOOK
    lib_path = site / "data/library.json"
    manifest_path = root / "manifest.json"
    questions_path = root / "questions.json"
    search_path = root / "search.json"

    library = json.loads(lib_path.read_text(encoding="utf-8"))
    ids = [b["id"] for b in library["books"]]
    if ids.count(BOOK) != 1:
        raise AssertionError(f"investments must exist exactly once: {ids}")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    qtop = json.loads(questions_path.read_text(encoding="utf-8"))
    search = json.loads(search_path.read_text(encoding="utf-8"))

    if manifest.get("version") == VERSION and qtop.get("version") == VERSION:
        print(library["version"])
        return library["version"]
    if manifest.get("version") != OLD_VERSION or qtop.get("version") != OLD_VERSION:
        raise AssertionError(
            f"unexpected investments source version: manifest={manifest.get('version')} questions={qtop.get('version')}"
        )

    chapter_map = {m["id"]: m for m in manifest["chapters"]}
    for cid, replacements in HTML_REPLACEMENTS.items():
        if cid not in chapter_map:
            raise AssertionError(f"missing chapter/appendix id {cid}")
        path = root / chapter_map[cid]["file"]
        raw = path.read_text(encoding="utf-8")
        for idx, (old, new) in enumerate(replacements, start=1):
            raw = replace_once(raw, old, new, f"{cid} replacement {idx}")
        path.write_text(raw, encoding="utf-8")

    items = qtop["items"]
    ids_before = [item["id"] for item in items]
    qmap = {item["id"]: item for item in items}
    for qid, fields in QUESTION_UPDATES.items():
        if qid not in qmap:
            raise AssertionError(f"missing question {qid}")
        for key, value in fields.items():
            qmap[qid][key] = value
    if [item["id"] for item in items] != ids_before:
        raise AssertionError("question IDs/order changed")
    qtop["version"] = VERSION
    qtop["count"] = len(items)
    questions_path.write_text(jdump(qtop), encoding="utf-8")

    entry_map = {(e["chapterId"], e["page"]): e for e in search["entries"]}
    for cid in [x for x in HTML_REPLACEMENTS if x.startswith("ch")]:
        raw = (root / chapter_map[cid]["file"]).read_text(encoding="utf-8")
        pages = search_pages_from_html(raw)
        for page, value in pages.items():
            key = (cid, page)
            if key not in entry_map:
                raise AssertionError(f"missing search entry {key}")
            entry_map[key]["text"] = value
    if len(search["entries"]) != 165:
        raise AssertionError(f"search count drift: {len(search['entries'])}")
    search_path.write_text(jdump(search), encoding="utf-8")

    manifest["version"] = VERSION
    manifest["updatedAt"] = UPDATED_AT
    release = {
        "version": VERSION,
        "date": UPDATED_AT,
        "title": "發布後第二次獨立內容審計與精確化",
        "changes": [
            "APT 因子報酬式明列零均值 factor surprise／殘差條件，避免把 E[R] 截距口徑寫得過度簡略",
            "DuPont 統一期間流量與平均資產／平均權益口徑",
            "duration／convexity／immunization 補足凸性定義、單一與多負債配對及再平衡限制",
            "無收益標的成本持有式改為成立條件下的無套利等式",
            "ETF 明確區分交易架構、被動指數化與主動管理，更新臺灣主動式 ETF 後的名詞口徑",
            "國際投資本幣報酬改為固定匯率報價方向後的精確乘法關係",
            "Information Ratio 公式分子改為平均主動報酬，與文字定義一致",
        ],
        "progressImpact": "章節 ID、題目 ID、題數、Book ID 與儲存鍵不變，既有閱讀進度與錯題紀錄相容。",
    }
    notes = [x for x in manifest.get("releaseNotes", []) if x.get("version") != VERSION]
    manifest["releaseNotes"] = [release] + notes
    manifest_path.write_text(jdump(manifest), encoding="utf-8")

    final_library_version = next_library_version(library["version"])
    library["version"] = final_library_version
    lib_path.write_text(jdump(library), encoding="utf-8")

    sw_path = site / "sw.js"
    sw = sw_path.read_text(encoding="utf-8")
    sw, n = re.subn(
        r"const VERSION = 'study-library-[^']+';",
        f"const VERSION = 'study-library-{final_library_version}';",
        sw,
        count=1,
    )
    if n != 1:
        raise AssertionError("service-worker version marker not found")
    sw_path.write_text(sw, encoding="utf-8")

    print(final_library_version)
    return final_library_version


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python deploy/patch_investments_v2.py SITE_ROOT")
    main(sys.argv[1])
