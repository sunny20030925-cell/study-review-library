#!/usr/bin/env python3
from __future__ import annotations

import base64
import hashlib
from pathlib import Path
from textwrap import dedent, indent

EXPECTED_SHA = 'c3643675f863883a429d492334b291d430ebfa87bf0b1cbf49806dfe790b6b34'


def add_once(text: str, anchor: str, addition: str, label: str) -> str:
    if text.count(anchor) != 1:
        raise AssertionError(f'{label} anchor count={text.count(anchor)}')
    return text.replace(anchor, anchor + addition, 1)


def main() -> None:
    deploy = Path('deploy')
    chunks = sorted(deploy.glob('rebuilt-macroeconomics.b64.chunk*'))
    if len(chunks) != 5:
        raise AssertionError(f'expected 5 upload chunks, got {len(chunks)}')
    encoded = ''.join(''.join(path.read_text(encoding='utf-8').split()) for path in chunks)
    if len(encoded) != 37248:
        raise AssertionError(f'unexpected rebuilt Base64 length: {len(encoded)}')
    payload = base64.b64decode(encoded, validate=True)
    digest = hashlib.sha256(payload).hexdigest()
    if digest != EXPECTED_SHA:
        raise AssertionError(f'rebuilt generator digest mismatch: {digest}')
    (deploy / 'generate-macroeconomics.py.gz.b64.part00').write_text(encoded[:20000] + '\n', encoding='utf-8')
    (deploy / 'generate-macroeconomics.py.gz.b64.part01').write_text(encoded[20000:] + '\n', encoding='utf-8')

    source = Path('.github/workflows/deploy-pages.yml')
    target = deploy / 'staged-final-macroeconomics-deploy-pages.yml'
    text = source.read_text(encoding='utf-8')

    deferred = (
        "      - name: Note deferred macroeconomics deployment\n"
        "        run: echo 'Macroeconomics deployment deferred until the damaged generator source is reconstructed and revalidated.'\n"
    )
    macro_step = indent(dedent(f"""\
    - name: Generate and independently validate macroeconomics textbook
      run: |
        cp _site/data/library.json /tmp/pre-macroeconomics-library.json
        cat deploy/generate-macroeconomics.py.gz.b64.part* | tr -d '\\n\\r\\t ' | base64 --decode > /tmp/generate-macroeconomics.py.gz
        echo '{EXPECTED_SHA}  /tmp/generate-macroeconomics.py.gz' | sha256sum --check -
        gzip --test /tmp/generate-macroeconomics.py.gz
        gzip --decompress --stdout /tmp/generate-macroeconomics.py.gz > /tmp/generate-macroeconomics.py
        python -m py_compile /tmp/generate-macroeconomics.py
        python /tmp/generate-macroeconomics.py _site
        FINAL_LIBRARY_VERSION="$(python deploy/finalize_macroeconomics_library.py _site /tmp/pre-macroeconomics-library.json)"
        EXPECTED_LIBRARY_VERSION="$FINAL_LIBRARY_VERSION" PRE_LIBRARY_JSON=/tmp/pre-macroeconomics-library.json python deploy/validate_macroeconomics.py _site
        node --check _site/app.js
        node --check _site/sw.js
        echo "MACROECONOMICS_FINAL_LIBRARY_VERSION=$FINAL_LIBRARY_VERSION"
    """), '      ')
    if text.count(deferred) != 1:
        raise AssertionError(f'deferred step count={text.count(deferred)}')
    text = text.replace(deferred, macro_step, 1)

    if 'macroeconomics_version' not in text:
        receipt_anchor = "              'intermediate_accounting_round2_check_count': 485,\n"
        macro_fields = (
            "              'macroeconomics_version': '2026.07.29-1',\n"
            "              'macroeconomics_chapter_count': 20,\n"
            "              'macroeconomics_appendix_count': 3,\n"
            "              'macroeconomics_question_count': 100,\n"
            "              'macroeconomics_search_count': 143,\n"
            "              'macroeconomics_figure_count': 20,\n"
            "              'macroeconomics_content_audit': 'passed',\n"
            "              'macroeconomics_numeric_recheck_count': 18,\n"
            "              'macroeconomics_two_round_qa': 'passed',\n"
        )
        text = add_once(text, receipt_anchor, macro_fields, 'receipt')

    if "Path('docs/books/macroeconomics/status.md')" not in text:
        status_anchor = "          Path('docs/books/intermediate-accounting/status.md').write_text(ia_status, encoding='utf-8')\n"
        macro_status = indent(dedent("""\
        macro_status = (
            '# 《總體經濟學》製作狀態\\n\\n'
            '更新日期：2026-07-29\\n\\n'
            '## 版本\\n\\n'
            '- Book ID：`macroeconomics`\\n'
            '- 正式內容版本：`2026.07.29-1`\\n'
            f'- 正式書庫版本：`{final_version}`\\n'
            '- 狀態：已部署。\\n\\n'
            '## 成品與 QA\\n\\n'
            '- 正文 20 章、附錄 3 份、題庫 100 題、搜尋索引 143 筆、自製 SVG 20 張。\\n'
            '- 兩輪內容與題庫 QA 通過；100 題逐題複核，18 題具體數值題獨立重算一致。\\n'
            '- 閱讀進度相容性：新增獨立 book ID，不改既有教材章節、題目 ID、儲存鍵或錯題紀錄。\\n\\n'
            '## 部署\\n\\n'
            '- canonical workflow：`Deploy study library`\\n'
            f'- workflow run：`{os.environ["GITHUB_RUN_ID"]}`\\n'
            f'- source commit：`{os.environ["GITHUB_SHA"]}`\\n'
            f'- 正式書庫書籍數：{book_count} 本。\\n'
            '- GitHub Pages 部署成功並已寫回 deployment receipt。\\n'
        )
        Path('docs/books/macroeconomics/status.md').write_text(macro_status, encoding='utf-8')
        """), '          ')
        text = add_once(text, status_anchor, '\n' + macro_status, 'status')

    if "if '### 總體經濟學' not in c:" not in text:
        checkpoint_anchor = "          cp.write_text(c, encoding='utf-8')\n"
        checkpoint_code = indent(dedent("""\
        if '### 總體經濟學' not in c:
            section = (
                '### 總體經濟學\\n\\n'
                '- Book ID：`macroeconomics`\\n'
                '- 正式內容版本：`2026.07.29-1`\\n'
                '- 定位：一般大學總體經濟學，聚焦總體衡量、長期成長、短期景氣、財政貨幣政策與開放經濟。\\n'
                '- 成品：20 章、3 附錄、100 題題庫、143 筆搜尋索引、20 張自製圖解。\\n'
                '- QA：兩輪內容與題庫複核通過；18 題數值題獨立重算一致。\\n'
                '- 範圍文件：`docs/books/macroeconomics/scope.md`\\n'
                '- QA 報告：`docs/books/macroeconomics/qa_report.md`\\n'
                f'- GitHub Pages 部署 run：`{os.environ["GITHUB_RUN_ID"]}`。\\n'
                f'- Source commit：`{os.environ["GITHUB_SHA"]}`。\\n'
                '- 狀態：已部署。\\n\\n'
            )
            c = c.replace('## 部署流程\\n', section + '## 部署流程\\n', 1)
        """), '          ')
        if text.count(checkpoint_anchor) != 1:
            raise AssertionError(f'checkpoint anchor count={text.count(checkpoint_anchor)}')
        text = text.replace(checkpoint_anchor, checkpoint_code + checkpoint_anchor, 1)

    if "macro = '- 《總體經濟學》" not in text:
        readme_anchor = "          r = re.sub(r'五本書均由同一個 canonical GitHub Pages 工作流部署。', '全部正式教材均由同一個 canonical GitHub Pages 工作流部署。', r)\n"
        readme_code = indent(dedent("""\
        macro = '- 《總體經濟學》：一般大學總體經濟學，20 章、3 附錄、100 題題庫、143 筆搜尋索引與 20 張圖解；內容版本 `2026.07.29-1`。\\n'
        if macro not in r:
            lines = r.splitlines(True)
            idx = max(i for i, line in enumerate(lines) if line.startswith('- 《')) + 1
            lines.insert(idx, macro)
            r = ''.join(lines)
        """), '          ')
        if text.count(readme_anchor) != 1:
            raise AssertionError(f'README anchor count={text.count(readme_anchor)}')
        text = text.replace(readme_anchor, readme_code + readme_anchor, 1)

    old_add = '          git add docs/deployment_receipt.json README.md docs/shared_checkpoint.md docs/books/microeconomics/status.md docs/books/intermediate-accounting/status.md\n'
    new_add = '          git add docs/deployment_receipt.json README.md docs/shared_checkpoint.md docs/books/microeconomics/status.md docs/books/intermediate-accounting/status.md docs/books/macroeconomics/status.md\n'
    if text.count(old_add) != 1:
        raise AssertionError(f'deployment git-add count={text.count(old_add)}')
    text = text.replace(old_add, new_add, 1)

    target.write_text(text, encoding='utf-8')
    print(f'STAGED_FINAL_MACRO_OK chars={len(encoded)} sha256={digest} target={target}')


if __name__ == '__main__':
    main()
