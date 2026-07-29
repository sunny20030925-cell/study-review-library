#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

WORKFLOW = Path('.github/workflows/deploy-pages.yml')
text = WORKFLOW.read_text(encoding='utf-8')

step = '''      - name: Generate and independently validate macroeconomics textbook
        run: |
          cp _site/data/library.json /tmp/pre-macroeconomics-library.json
          cat deploy/generate-macroeconomics.py.gz.b64.part* | tr -d '\\n' | base64 --decode > /tmp/generate-macroeconomics.py.gz
          echo '05259f866024c5e442207ae2e9d448f4511c33db3868f14d504424b103fb058e  /tmp/generate-macroeconomics.py.gz' | sha256sum --check -
          gzip --decompress --stdout /tmp/generate-macroeconomics.py.gz > /tmp/generate-macroeconomics.py
          python -m py_compile /tmp/generate-macroeconomics.py
          python /tmp/generate-macroeconomics.py _site
          FINAL_LIBRARY_VERSION="$(python deploy/finalize_macroeconomics_library.py _site /tmp/pre-macroeconomics-library.json)"
          EXPECTED_LIBRARY_VERSION="$FINAL_LIBRARY_VERSION" PRE_LIBRARY_JSON=/tmp/pre-macroeconomics-library.json python deploy/validate_macroeconomics.py _site
          node --check _site/app.js
          node --check _site/sw.js
          echo "MACROECONOMICS_FINAL_LIBRARY_VERSION=$FINAL_LIBRARY_VERSION"

'''
marker = '      - name: Upload Pages artifact\n'
if 'Generate and independently validate macroeconomics textbook' not in text:
    if marker not in text:
        raise AssertionError('Upload Pages marker not found')
    text = text.replace(marker, step + marker, 1)

metrics = '''              'macroeconomics_version': '2026.07.29-1',
              'macroeconomics_chapter_count': 20,
              'macroeconomics_appendix_count': 3,
              'macroeconomics_question_count': 100,
              'macroeconomics_search_count': 143,
              'macroeconomics_figure_count': 20,
              'macroeconomics_content_audit': 'passed',
              'macroeconomics_numeric_recheck_count': 18,
              'macroeconomics_two_round_qa': 'passed',
'''
metric_marker = "              'source_commit': os.environ['GITHUB_SHA'],\n"
if "'macroeconomics_version':" not in text:
    if metric_marker not in text:
        raise AssertionError('receipt metric marker not found')
    text = text.replace(metric_marker, metrics + metric_marker, 1)

macro_status = """          macro_status = f'''# 《總體經濟學》製作狀態

更新日期：2026-07-29

## 版本

- Book ID：`macroeconomics`
- 正式內容版本：`2026.07.29-1`
- 正式書庫版本：`{final_version}`
- 狀態：已部署。

## 成品與 QA

- 正文 20 章、附錄 3 份、題庫 100 題、搜尋索引 143 筆、自製 SVG 20 張。
- 第一輪製作內檢通過；第二輪獨立複核通過。
- 100 題逐題重新檢查；18 題具體數值題獨立重算一致。
- 閱讀進度相容性：新增獨立 book ID，不改既有教材章節、題目 ID、儲存鍵或錯題紀錄。

## 部署

- canonical workflow：`Deploy study library`
- workflow run：`{os.environ['GITHUB_RUN_ID']}`
- source commit：`{os.environ['GITHUB_SHA']}`
- 正式書庫書籍數：{book_count} 本。
- GitHub Pages 部署成功並已寫回 deployment receipt。
'''
          Path('docs/books/macroeconomics/status.md').write_text(macro_status, encoding='utf-8')

"""
status_marker = "          cp = Path('docs/shared_checkpoint.md')\n"
if "macro_status = f'''# 《總體經濟學》製作狀態" not in text:
    if status_marker not in text:
        raise AssertionError('status marker not found')
    text = text.replace(status_marker, macro_status + status_marker, 1)

checkpoint = """          if '### 總體經濟學' not in c:
              section = f'''### 總體經濟學

- Book ID：`macroeconomics`
- 正式內容版本：`2026.07.29-1`
- 定位：一般大學總體經濟學，深度高於《經濟學原理》的總體共同核心，聚焦總體衡量、成長、景氣、政策與開放經濟。
- 成品：20 章、3 附錄、100 題題庫、143 筆搜尋索引、20 張自製圖解。
- QA：兩輪內容複核通過；100 題逐題重查，18 題數值題獨立重算一致。
- 範圍文件：`docs/books/macroeconomics/scope.md`
- QA 報告：`docs/books/macroeconomics/qa_report.md`
- GitHub Pages 部署 run：`{os.environ['GITHUB_RUN_ID']}`。
- Source commit：`{os.environ['GITHUB_SHA']}`。
- 狀態：已部署。

              '''
              c = c.replace('## 部署流程\\n', section + '## 部署流程\\n', 1)
"""
checkpoint_marker = "          cp.write_text(c, encoding='utf-8')\n"
if "if '### 總體經濟學' not in c:" not in text:
    if checkpoint_marker not in text:
        raise AssertionError('checkpoint write marker not found')
    text = text.replace(checkpoint_marker, checkpoint + checkpoint_marker, 1)

old_summary = "          if '中級會計學均已納入同一套正式書庫部署流程。' not in c:\n              c = c.replace('成本會計學、個體經濟學均已納入同一套正式書庫部署流程。', '成本會計學、個體經濟學、中級會計學均已納入同一套正式書庫部署流程。')\n"
new_summary = old_summary + "          if '總體經濟學均已納入同一套正式書庫部署流程。' not in c:\n              c = c.replace('成本會計學、個體經濟學、中級會計學均已納入同一套正式書庫部署流程。', '成本會計學、個體經濟學、中級會計學、總體經濟學均已納入同一套正式書庫部署流程。')\n"
if '總體經濟學均已納入同一套正式書庫部署流程' not in text:
    if old_summary not in text:
        raise AssertionError('checkpoint process summary marker not found')
    text = text.replace(old_summary, new_summary, 1)

intermediate_def = "          intermediate = '- 《中級會計學》：一般大學中級會計學，22 章、3 附錄、110 題題庫、145 筆搜尋索引與 22 張圖解；內容版本 `2026.07.29-1`。\\n'\n"
macro_def = intermediate_def + "          macro = '- 《總體經濟學》：一般大學總體經濟學，20 章、3 附錄、100 題題庫、143 筆搜尋索引與 20 張圖解；內容版本 `2026.07.29-1`。\\n'\n"
if "          macro = '- 《總體經濟學》" not in text:
    if intermediate_def not in text:
        raise AssertionError('README intermediate definition marker not found')
    text = text.replace(intermediate_def, macro_def, 1)

readme_insert_marker = "          if intermediate not in r:\n              lines = r.splitlines(True)\n              idx = max(i for i, x in enumerate(lines) if x.startswith('- 《')) + 1\n              lines.insert(idx, intermediate)\n              r = ''.join(lines)\n"
readme_insert = readme_insert_marker + "          if macro not in r:\n              lines = r.splitlines(True)\n              idx = max(i for i, x in enumerate(lines) if x.startswith('- 《')) + 1\n              lines.insert(idx, macro)\n              r = ''.join(lines)\n"
if '          if macro not in r:' not in text:
    if readme_insert_marker not in text:
        raise AssertionError('README insertion marker not found')
    text = text.replace(readme_insert_marker, readme_insert, 1)

old_add = "          git add docs/deployment_receipt.json README.md docs/shared_checkpoint.md docs/books/microeconomics/status.md docs/books/intermediate-accounting/status.md\n"
new_add = "          git add docs/deployment_receipt.json README.md docs/shared_checkpoint.md docs/books/microeconomics/status.md docs/books/intermediate-accounting/status.md docs/books/macroeconomics/status.md\n"
if new_add not in text:
    if old_add not in text:
        raise AssertionError('git add marker not found')
    text = text.replace(old_add, new_add, 1)

WORKFLOW.write_text(text, encoding='utf-8')
print(f'updated {WORKFLOW}')
