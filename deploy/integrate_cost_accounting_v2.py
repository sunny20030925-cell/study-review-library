#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise AssertionError(f"{label}: expected exactly one match, got {count}")
    return text.replace(old, new, 1)


def sub_once(text: str, pattern: str, replacement: str, label: str, *, flags: int = 0) -> str:
    text, count = re.subn(pattern, replacement, text, count=1, flags=flags)
    if count != 1:
        raise AssertionError(f"{label}: expected exactly one match, got {count}")
    return text


def main(workflow_path: str) -> None:
    path = Path(workflow_path)
    text = path.read_text(encoding="utf-8")

    old = """          final_library = json.loads(Path('_site/data/library.json').read_text(encoding='utf-8'))
          receipt = {
"""
    new = """          final_library = json.loads(Path('_site/data/library.json').read_text(encoding='utf-8'))
          cost_root = Path('_site/books/cost-accounting')
          cost_manifest = json.loads((cost_root / 'manifest.json').read_text(encoding='utf-8'))
          cost_questions = json.loads((cost_root / 'questions.json').read_text(encoding='utf-8'))
          cost_search = json.loads((cost_root / 'search.json').read_text(encoding='utf-8'))
          cost_chapter_count = sum(1 for item in cost_manifest['chapters'] if item['kind'] == 'chapter')
          cost_appendix_count = sum(1 for item in cost_manifest['chapters'] if item['kind'] == 'appendix')
          cost_figure_count = len(list(Path('_site/assets/cost-accounting-svg').glob('*.svg')))
          receipt = {
"""
    text = replace_once(text, old, new, "load generated cost accounting metadata")

    receipt_pattern = r"""              'cost_accounting_version': '2026\.07\.29-1',\n              'cost_accounting_chapter_count': 19,\n              'cost_accounting_question_count': 95,\n              'cost_accounting_search_count': 146,\n              'cost_accounting_figure_count': 19,\n              'cost_accounting_content_audit': 'passed',\n              'cost_accounting_independent_check_count': 655,\n              'cost_accounting_quantitative_recheck_count': 44,\n"""
    receipt_replacement = """              'cost_accounting_version': cost_manifest['version'],
              'cost_accounting_chapter_count': cost_chapter_count,
              'cost_accounting_appendix_count': cost_appendix_count,
              'cost_accounting_question_count': cost_questions['count'],
              'cost_accounting_search_count': len(cost_search['entries']),
              'cost_accounting_figure_count': cost_figure_count,
              'cost_accounting_content_audit': 'passed-after-post-publication-reaudit',
              'cost_accounting_initial_independent_check_count': 655,
              'cost_accounting_question_adjustment_count': 9,
              'cost_accounting_independent_check_count': 857,
              'cost_accounting_quantitative_recheck_count': 44,
"""
    text = sub_once(
        text,
        receipt_pattern,
        receipt_replacement,
        "update cost accounting deployment receipt metrics",
    )

    status_marker = """          status = f'''# 《個體經濟學》狀態
"""
    status_inject = """          cost_status = f'''# 《成本會計學》製作狀態

更新日期：2026-07-29

## 版本

- Book ID：`cost-accounting`
- 正式內容版本：`2026.07.29-2`
- 正式書庫版本：`{final_version}`

## 成品與發布後二次審計

- 正文 19 章、附錄 3 份、題庫 95 題、搜尋索引 150 筆、自製 SVG 19 張。
- 初版獨立驗證：655／655 項通過。
- 發布後獨立二次內容審計：857／857 項通過；95 題全數重查，9 題題幹、答案或詳解同步精確化，44 個數值答案另行重算。
- 主要修正：主要成本與加工成本、淨進料、CVP 適用條件、分步成本各成本成分約當產量、FIFO 轉入成本、正常損壞檢驗點、副產品、AQP／AQU、正常產能與吸收／變動成本利益調節。
- 閱讀進度相容性：章節 ID、題目 ID 與題數不變；既有閱讀進度與錯題紀錄保留。

## 正式部署

- canonical workflow：`Deploy study library`
- workflow run：`{os.environ['GITHUB_RUN_ID']}`
- source commit：`{os.environ['GITHUB_SHA']}`
- 部署回條：`docs/deployment_receipt.json`
- 狀態：已部署。
'''
          Path('docs/books/cost-accounting/status.md').write_text(cost_status, encoding='utf-8')

          status = f'''# 《個體經濟學》狀態
"""
    text = replace_once(text, status_marker, status_inject, "write deployed cost accounting status")

    checkpoint_marker = """          cp.write_text(c, encoding='utf-8')
"""
    checkpoint_inject = """          cost_section = f'''### 成本會計學

- Book ID：`cost-accounting`
- 正式內容版本：`2026.07.29-2`
- 定位：一般大學成本會計／成本與管理會計課程中的成本會計主體。
- 範圍：成本分類與成本流向、成本習性、基礎 CVP、成本分攤、分批成本制、正常成本制、多分／少分、分步成本制加權平均與 FIFO、損壞品、ABC、服務部門、聯產品／副產品、標準成本、材料／人工／製造費用差異、吸收／變動成本法、產能與整合解題。
- 成品：19 章、3 附錄、95 題題庫、150 筆搜尋索引、19 張自製圖解。
- 初版 QA：獨立驗證 655／655 項通過。
- 發布後獨立二次內容審計：857／857 項通過；95 題全數重查，9 題同步精確化，44 個數值答案由原始輸入重新計算。
- 主要修正：補入主要成本／加工成本與副產品；精確化淨進料、CVP、分步成本、FIFO 轉入成本、正常損壞檢驗點、AQP／AQU、正常產能及吸收／變動成本利益調節。
- 閱讀進度相容性：章節 ID、題目 ID 與題數不變；部署回條確認 `progress_storage_changed=false`。
- 範圍文件：`docs/books/cost-accounting/scope.md`
- QA 報告：`docs/books/cost-accounting/qa_report.md`
- GitHub Pages 部署 run：`{os.environ['GITHUB_RUN_ID']}`。
- Source commit：`{os.environ['GITHUB_SHA']}`。
- 部署回條：`docs/deployment_receipt.json`。
- 狀態：已部署。

'''
          c, cost_section_count = re.subn(
              r'(?ms)^### 成本會計學\n.*?(?=^### |^## 部署流程)',
              cost_section,
              c,
              count=1,
          )
          if cost_section_count != 1:
              raise AssertionError('cost accounting checkpoint section not found')
          c, cost_gate_count = re.subn(
              r'(?m)^9\. 成本會計.*$',
              '9. 成本會計先套用發布後獨立二次內容審計修正，再驗證 19 章、3 附錄、95 題、150 筆搜尋索引、19 張 SVG，並執行 857 項獨立檢查與 44 項數值重算。',
              c,
              count=1,
          )
          if cost_gate_count != 1:
              raise AssertionError('cost accounting deployment gate not found')
          c, cost_status_count = re.subn(
              r'(?m)^- 成本會計學初版內容、兩輪 QA、canonical integration 與正式 Pages 部署均已完成。$',
              '- 成本會計學初版、發布後獨立二次內容審計、糾錯修正與新版 Pages 部署均已完成；章節 ID、題目 ID 與題數未變。',
              c,
              count=1,
          )
          if cost_status_count != 1:
              raise AssertionError('cost accounting workline status not found')
          cp.write_text(c, encoding='utf-8')
"""
    text = replace_once(
        text,
        checkpoint_marker,
        checkpoint_inject,
        "update cost accounting shared checkpoint",
    )

    old_readme = """          cost = '- 《成本會計學》：一般大學成本會計，19 章、3 附錄、95 題題庫、146 筆搜尋索引與 19 張圖解；內容版本 `2026.07.29-1`。\n'
"""
    new_readme = """          cost = '- 《成本會計學》：一般大學成本會計，19 章、3 附錄、95 題題庫、150 筆搜尋索引與 19 張圖解；發布後獨立二次內容審計版本 `2026.07.29-2`。\n'
"""
    text = replace_once(text, old_readme, new_readme, "update cost accounting README entry")

    readme_marker = """          r = re.sub(r'五本書均由同一個 canonical GitHub Pages 工作流部署。', '全部正式教材均由同一個 canonical GitHub Pages 工作流部署。', r)
"""
    readme_inject = """          cost_v2_line = cost.rstrip('\n')
          r_lines = r.splitlines()
          cost_indexes = [i for i, line in enumerate(r_lines) if line.startswith('- 《成本會計學》：')]
          if cost_indexes:
              first = cost_indexes[0]
              r_lines[first] = cost_v2_line
              for i in reversed(cost_indexes[1:]):
                  del r_lines[i]
          else:
              insert_at = max(i for i, line in enumerate(r_lines) if line.startswith('- 《')) + 1
              r_lines.insert(insert_at, cost_v2_line)
          r = '\n'.join(r_lines) + ('\n' if r.endswith('\n') else '')
          r = re.sub(r'五本書均由同一個 canonical GitHub Pages 工作流部署。', '全部正式教材均由同一個 canonical GitHub Pages 工作流部署。', r)
"""
    text = replace_once(text, readme_marker, readme_inject, "deduplicate cost accounting README entry")

    git_add_pattern = r"(?m)^          git add (?P<paths>docs/deployment_receipt\.json README\.md docs/shared_checkpoint\.md[^\n]*)$"
    match = re.search(git_add_pattern, text)
    if match is None:
        raise AssertionError("deployment writeback git add line not found")
    paths = match.group("paths")
    cost_status_path = "docs/books/cost-accounting/status.md"
    if cost_status_path not in paths.split():
        paths = f"{paths} {cost_status_path}"
    text = sub_once(
        text,
        git_add_pattern,
        f"          git add {paths}",
        "include cost accounting status in deployment writeback",
    )

    path.write_text(text, encoding="utf-8")
    print("COST_ACCOUNTING_V2_WORKFLOW_INTEGRATION_OK")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python integrate_cost_accounting_v2.py WORKFLOW_PATH")
    main(sys.argv[1])
