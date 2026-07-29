#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

SRC = Path('.github/workflows/deploy-pages.yml')
DST = Path('deploy/generated-deploy-pages.intermediate-accounting.yml')

text = SRC.read_text(encoding='utf-8')

step = '''      - name: Generate and independently validate intermediate accounting textbook
        run: |
          cp _site/data/library.json /tmp/pre-intermediate-accounting-library.json
          cat deploy/generate-intermediate-accounting.py.gz.b64.part* | tr -d '\\n' | base64 --decode > /tmp/generate-intermediate-accounting.py.gz
          echo 'b60133689f2ede497597295688b82646ba070b787ea94a78e950da5603b8bf34  /tmp/generate-intermediate-accounting.py.gz' | sha256sum --check -
          gzip --decompress --stdout /tmp/generate-intermediate-accounting.py.gz > /tmp/generate-intermediate-accounting.py
          python /tmp/generate-intermediate-accounting.py _site
          FINAL_LIBRARY_VERSION="$(python deploy/finalize_intermediate_accounting_library.py _site /tmp/pre-intermediate-accounting-library.json)"
          EXPECTED_LIBRARY_VERSION="$FINAL_LIBRARY_VERSION" PRE_LIBRARY_JSON=/tmp/pre-intermediate-accounting-library.json python deploy/validate_intermediate_accounting.py _site
          node --check _site/app.js
          node --check _site/sw.js
          echo "INTERMEDIATE_ACCOUNTING_FINAL_LIBRARY_VERSION=$FINAL_LIBRARY_VERSION"

'''
marker = '      - name: Upload Pages artifact\n'
if 'Generate and independently validate intermediate accounting textbook' not in text:
    if marker not in text:
        raise AssertionError('upload Pages marker not found')
    text = text.replace(marker, step + marker, 1)

metrics = '''              'intermediate_accounting_version': '2026.07.29-1',
              'intermediate_accounting_chapter_count': 22,
              'intermediate_accounting_appendix_count': 3,
              'intermediate_accounting_question_count': 110,
              'intermediate_accounting_search_count': 145,
              'intermediate_accounting_figure_count': 22,
              'intermediate_accounting_content_audit': 'passed',
              'intermediate_accounting_round1_check_count': 135,
              'intermediate_accounting_quantitative_recheck_count': 23,
              'intermediate_accounting_round2_check_count': 485,
'''
metric_marker = "              'source_commit': os.environ['GITHUB_SHA'],\n"
if "'intermediate_accounting_version':" not in text:
    if metric_marker not in text:
        raise AssertionError('receipt metric marker not found')
    text = text.replace(metric_marker, metrics + metric_marker, 1)

ia_status = """          ia_status = f'''# 《中級會計學》製作狀態

更新日期：2026-07-29

## 版本

- Book ID：`intermediate-accounting`
- 正式內容版本：`2026.07.29-1`
- 正式書庫版本：`{final_version}`
- 狀態：已部署。

## 成品與 QA

- 正文 22 章、附錄 3 份、題庫 110 題、搜尋索引 145 筆、自製 SVG 22 張。
- 第一輪 QA：135 項通過；獨立數值與公式重算 23 項通過。
- 第二輪 QA：485 項通過；110 題逐題複核。
- 閱讀進度相容性：新增獨立 book ID，不改既有教材章節、題目 ID、儲存鍵或錯題紀錄。

## 部署

- canonical workflow：`Deploy study library`
- workflow run：`{os.environ['GITHUB_RUN_ID']}`
- source commit：`{os.environ['GITHUB_SHA']}`
- 正式書庫書籍數：{book_count} 本。
- GitHub Pages 部署成功並已寫回 deployment receipt。
'''
          Path('docs/books/intermediate-accounting/status.md').write_text(ia_status, encoding='utf-8')

"""
status_marker = "          cp = Path('docs/shared_checkpoint.md')\n"
if "ia_status = f'''# 《中級會計學》製作狀態" not in text:
    if status_marker not in text:
        raise AssertionError('status marker not found')
    text = text.replace(status_marker, ia_status + status_marker, 1)

checkpoint = """          if '### 中級會計學' not in c:
              section = f'''### 中級會計學

- Book ID：`intermediate-accounting`
- 正式內容版本：`2026.07.29-1`
- 定位：一般大學中級會計學，銜接基礎會計，核心聚焦 IFRS／TIFRS 的認列、衡量、現值、金融工具、收入、租賃、所得稅、EPS 與現金流量。
- 成品：22 章、3 附錄、110 題題庫、145 筆搜尋索引、22 張自製圖解。
- QA：第一輪 135 項、數值與公式獨立重算 23 項、第二輪 485 項，全數通過。
- 範圍文件：`docs/books/intermediate-accounting/scope.md`
- QA 報告：`docs/books/intermediate-accounting/qa_report.md`
- GitHub Pages 部署 run：`{os.environ['GITHUB_RUN_ID']}`。
- Source commit：`{os.environ['GITHUB_SHA']}`。
- 狀態：已部署。

              '''
              c = c.replace('## 部署流程\\n', section + '## 部署流程\\n', 1)
"""
checkpoint_marker = "          c = c.replace('同一個 canonical `Deploy study library` 工作流先完成既有五本書驗證，再生成並獨立驗證 `cost-accounting`，最終部署六本書。',\n"
if "if '### 中級會計學' not in c:" not in text:
    if checkpoint_marker not in text:
        raise AssertionError('checkpoint marker not found')
    text = text.replace(checkpoint_marker, checkpoint + checkpoint_marker, 1)

old = "          if '個體經濟學均已納入同一套正式書庫部署流程。' not in c:\n              c = c.replace('成本會計學均已納入同一套正式書庫部署流程。', '成本會計學、個體經濟學均已納入同一套正式書庫部署流程。')\n"
new = old + "          if '中級會計學均已納入同一套正式書庫部署流程。' not in c:\n              c = c.replace('成本會計學、個體經濟學均已納入同一套正式書庫部署流程。', '成本會計學、個體經濟學、中級會計學均已納入同一套正式書庫部署流程。')\n"
if "中級會計學均已納入同一套正式書庫部署流程" not in text:
    if old not in text:
        raise AssertionError('checkpoint process summary marker not found')
    text = text.replace(old, new, 1)

readme_def_marker = "          micro = '- 《個體經濟學》：一般大學中級個體經濟學，20 章、3 附錄、100 題題庫、154 筆搜尋索引與 20 張圖解；內容版本 `2026.07.29-1`。\\n'\n"
readme_def = readme_def_marker + "          intermediate = '- 《中級會計學》：一般大學中級會計學，22 章、3 附錄、110 題題庫、145 筆搜尋索引與 22 張圖解；內容版本 `2026.07.29-1`。\\n'\n"
if "          intermediate = '- 《中級會計學》" not in text:
    if readme_def_marker not in text:
        raise AssertionError('README definition marker not found')
    text = text.replace(readme_def_marker, readme_def, 1)

readme_insert_marker = "          r = re.sub(r'五本書均由同一個 canonical GitHub Pages 工作流部署。', '全部正式教材均由同一個 canonical GitHub Pages 工作流部署。', r)\n"
readme_insert = "          if intermediate not in r:\n              lines = r.splitlines(True)\n              idx = max(i for i, x in enumerate(lines) if x.startswith('- 《')) + 1\n              lines.insert(idx, intermediate)\n              r = ''.join(lines)\n" + readme_insert_marker
if "          if intermediate not in r:" not in text:
    if readme_insert_marker not in text:
        raise AssertionError('README insertion marker not found')
    text = text.replace(readme_insert_marker, readme_insert, 1)

old_add = "          git add docs/deployment_receipt.json README.md docs/shared_checkpoint.md docs/books/microeconomics/status.md\n"
new_add = "          git add docs/deployment_receipt.json README.md docs/shared_checkpoint.md docs/books/microeconomics/status.md docs/books/intermediate-accounting/status.md\n"
if new_add not in text:
    if old_add not in text:
        raise AssertionError('git add marker not found')
    text = text.replace(old_add, new_add, 1)

DST.write_text(text, encoding='utf-8')
print(f'generated {DST}')
