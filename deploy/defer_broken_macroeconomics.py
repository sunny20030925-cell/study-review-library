#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


def sub_once(text: str, pattern: str, replacement: str, label: str, *, flags: int = 0) -> str:
    updated, count = re.subn(pattern, replacement, text, count=1, flags=flags)
    if count != 1:
        raise AssertionError(f"{label}: expected exactly one match, got {count}")
    return updated


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise AssertionError(f"{label}: expected exactly one match, got {count}")
    return text.replace(old, new, 1)


def main(workflow_path: str) -> None:
    path = Path(workflow_path)
    text = path.read_text(encoding="utf-8")

    text = sub_once(
        text,
        r"\n      - name: Generate and independently validate macroeconomics textbook\n"
        r"        run: \|\n.*?(?=\n      - name: Upload Pages artifact)",
        "\n      - name: Note deferred macroeconomics deployment\n"
        "        run: echo 'Macroeconomics deployment deferred until the damaged generator source is reconstructed and revalidated.'\n",
        "remove broken macroeconomics generation step",
        flags=re.S,
    )

    text = sub_once(
        text,
        r"(?m)^              'macroeconomics_version': '2026\.07\.29-1',\n"
        r"^              'macroeconomics_chapter_count': 20,\n"
        r"^              'macroeconomics_appendix_count': 3,\n"
        r"^              'macroeconomics_question_count': 100,\n"
        r"^              'macroeconomics_search_count': 143,\n"
        r"^              'macroeconomics_figure_count': 20,\n"
        r"^              'macroeconomics_content_audit': 'passed',\n"
        r"^              'macroeconomics_numeric_recheck_count': 18,\n"
        r"^              'macroeconomics_two_round_qa': 'passed',\n",
        "",
        "remove undeployed macroeconomics receipt claims",
    )

    text = sub_once(
        text,
        r"(?ms)^          macro_status = \(\n.*?^          Path\('docs/books/macroeconomics/status\.md'\)\.write_text\(macro_status, encoding='utf-8'\)\n\n",
        "",
        "remove macroeconomics deployed-status writeback",
    )

    text = sub_once(
        text,
        r"(?m)^          if '總體經濟學均已納入同一套正式書庫部署流程。' not in c:\n"
        r"^              c = c\.replace\('成本會計學、個體經濟學、中級會計學均已納入同一套正式書庫部署流程。', '成本會計學、個體經濟學、中級會計學、總體經濟學均已納入同一套正式書庫部署流程。'\)\n",
        "",
        "remove macroeconomics deployed-workline claim",
    )

    text = sub_once(
        text,
        r"(?ms)^          if '### 總體經濟學' not in c:\n.*?^              c = c\.replace\('## 部署流程\\n', section \+ '## 部署流程\\n', 1\)\n",
        "",
        "remove macroeconomics checkpoint deployment section",
    )

    text = sub_once(
        text,
        r"(?m)^          macro = '- 《總體經濟學》：一般大學總體經濟學，20 章、3 附錄、100 題題庫、143 筆搜尋索引與 20 張圖解；內容版本 `2026\.07\.29-1`。\\n'\n",
        "",
        "remove macroeconomics README variable",
    )

    text = sub_once(
        text,
        r"(?m)^          if macro not in r:\n"
        r"^              lines = r\.splitlines\(True\)\n"
        r"^              idx = max\(i for i, x in enumerate\(lines\) if x\.startswith\('- 《'\)\) \+ 1\n"
        r"^              lines\.insert\(idx, macro\)\n"
        r"^              r = ''\.join\(lines\)\n",
        "",
        "remove macroeconomics README insertion",
    )

    text = replace_once(
        text,
        "docs/books/microeconomics/status.md docs/books/intermediate-accounting/status.md docs/books/macroeconomics/status.md",
        "docs/books/microeconomics/status.md docs/books/intermediate-accounting/status.md",
        "remove macroeconomics status from deployment commit",
    )

    required = [
        "python deploy/patch_microeconomics_v2.py _site",
        "python deploy/qa_microeconomics_v2.py _site",
        "'microeconomics_version': '2026.07.29-2'",
        "'microeconomics_post_publication_correction_count': 16",
        "'microeconomics_question_adjustment_count': 4",
        "'microeconomics_independent_check_count': 1616",
        "'intermediate_accounting_version': '2026.07.29-1'",
        "Note deferred macroeconomics deployment",
    ]
    for marker in required:
        if marker not in text:
            raise AssertionError(f"required marker missing after deferral: {marker}")

    forbidden = [
        "Generate and independently validate macroeconomics textbook",
        "'macroeconomics_version': '2026.07.29-1'",
        "Path('docs/books/macroeconomics/status.md').write_text",
        "總體經濟學均已納入同一套正式書庫部署流程。",
        "macro = '- 《總體經濟學》",
    ]
    for marker in forbidden:
        if marker in text:
            raise AssertionError(f"stale macroeconomics deployment claim remains: {marker}")

    path.write_text(text, encoding="utf-8")
    print("MACRO_DEFERRAL_OK micro_v2_preserved=true macro_claims_removed=true")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: defer_broken_macroeconomics.py WORKFLOW_PATH")
    main(sys.argv[1])
