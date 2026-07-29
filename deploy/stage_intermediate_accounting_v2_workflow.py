#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise AssertionError(f'{label}: expected 1 occurrence, got {count}')
    return text.replace(old, new, 1)


def main(src: str, dst: str) -> None:
    source = Path(src)
    target = Path(dst)
    text = source.read_text(encoding='utf-8')

    old_metrics = """              'intermediate_accounting_version': '2026.07.29-1',
              'intermediate_accounting_chapter_count': 22,
              'intermediate_accounting_appendix_count': 3,
              'intermediate_accounting_question_count': 110,
              'intermediate_accounting_search_count': 145,
              'intermediate_accounting_figure_count': 22,
              'intermediate_accounting_content_audit': 'passed',
              'intermediate_accounting_round1_check_count': 135,
              'intermediate_accounting_quantitative_recheck_count': 23,
              'intermediate_accounting_round2_check_count': 485,
"""
    new_metrics = """              'intermediate_accounting_version': '2026.07.29-2',
              'intermediate_accounting_chapter_count': 22,
              'intermediate_accounting_appendix_count': 3,
              'intermediate_accounting_question_count': 110,
              'intermediate_accounting_search_count': 145,
              'intermediate_accounting_figure_count': 22,
              'intermediate_accounting_content_audit': 'passed-after-post-publication-reaudit',
              'intermediate_accounting_initial_round1_check_count': 135,
              'intermediate_accounting_initial_quantitative_recheck_count': 23,
              'intermediate_accounting_initial_round2_check_count': 485,
              'intermediate_accounting_post_publication_correction_count': 12,
              'intermediate_accounting_corrected_file_count': 10,
              'intermediate_accounting_question_adjustment_count': 4,
              'intermediate_accounting_independent_check_count': 1110,
              'intermediate_accounting_quantitative_recheck_count': 28,
"""
    text = replace_once(text, old_metrics, new_metrics, 'receipt metrics')

    ia_status_re = re.compile(
        r"          ia_status = \(\n.*?          Path\('docs/books/intermediate-accounting/status\.md'\)\.write_text\(ia_status, encoding='utf-8'\)\n",
        re.S,
    )
    ia_status_new = """          ia_status = (
              '# 《中級會計學》製作狀態\\n\\n'
              '更新日期：2026-07-29\\n\\n'
              '## 版本\\n\\n'
              '- Book ID：`intermediate-accounting`\\n'
              '- 正式內容版本：`2026.07.29-2`\\n'
              f'- 正式書庫版本：`{final_version}`\\n'
              '- 狀態：已部署。\\n\\n'
              '## 成品與 QA\\n\\n'
              '- 正文 22 章、附錄 3 份、題庫 110 題、搜尋索引 145 筆、自製 SVG 22 張。\\n'
              '- 初版 QA：第一輪 135 項、獨立數值與公式重算 23 項、第二輪 485 項，全數通過。\\n'
              '- 發布後獨立二次內容審計：修正 12 個內容節點，分布於 10 份章節／附錄；4 題題幹或詳解精確化。\\n'
              '- v2 獨立部署驗證：1,110 項檢查與 28 項量化重算通過。\\n'
              '- 閱讀進度相容性：章節 ID、題目 ID 與題數不變；既有閱讀進度與錯題紀錄可沿用。\\n\\n'
              '## 部署\\n\\n'
              '- canonical workflow：`Deploy study library`\\n'
              f'- workflow run：`{os.environ["GITHUB_RUN_ID"]}`\\n'
              f'- source commit：`{os.environ["GITHUB_SHA"]}`\\n'
              f'- 正式書庫書籍數：{book_count} 本。\\n'
              '- GitHub Pages 部署成功並已寫回 deployment receipt。\\n'
          )
          Path('docs/books/intermediate-accounting/status.md').write_text(ia_status, encoding='utf-8')
"""
    text, count = ia_status_re.subn(ia_status_new, text, count=1)
    if count != 1:
        raise AssertionError(f'ia status block: expected 1, got {count}')

    checkpoint_anchor = "          if '### 總體經濟學' not in c:\n"
    checkpoint_runtime = """          ia_section_v2 = (
              '### 中級會計學\\n\\n'
              '- Book ID：`intermediate-accounting`\\n'
              '- 正式內容版本：`2026.07.29-2`\\n'
              '- 定位：一般大學中級會計學，銜接基礎會計，聚焦 IFRS／TIFRS 下的認列、衡量、表達、分錄與財務報導判斷。\\n'
              '- 範圍：現值與攤銷、ECL、存貨、PPE、借款成本、無形資產、減損、投資性不動產、金融工具、公司債、負債準備、權益、EPS、收入、租賃、所得稅、員工福利、會計變動、期後事項與現金流量。\\n'
              '- 成品：22 章、3 附錄、110 題題庫、145 筆搜尋索引、22 張自製圖解。\\n'
              '- 初版 QA：第一輪 135 項、獨立數值與公式重算 23 項、第二輪 485 項。\\n'
              '- 發布後獨立二次內容審計：修正 12 個內容節點／10 份章節與附錄，4 題題幹或詳解同步精確化；v2 獨立驗證 1,110 項、量化重算 28 項全數通過。\\n'
              '- 閱讀進度相容性：章節 ID、題目 ID 與題數未變；部署回條確認 `progress_storage_changed=false`。\\n'
              '- 範圍文件：`docs/books/intermediate-accounting/scope.md`\\n'
              '- QA 報告：`docs/books/intermediate-accounting/qa_report.md`\\n'
              f'- GitHub Pages 部署 run：`{os.environ["GITHUB_RUN_ID"]}`。\\n'
              f'- Source commit：`{os.environ["GITHUB_SHA"]}`。\\n'
              '- 部署回條：`docs/deployment_receipt.json`。\\n'
              '- 狀態：已部署。\\n\\n'
          )
          c, ia_section_count = re.subn(
              r'(?ms)^### 中級會計學\\n.*?(?=^### |^## 部署流程)',
              ia_section_v2,
              c,
              count=1,
          )
          if ia_section_count != 1:
              raise AssertionError('intermediate accounting checkpoint section not found')
          old_ia_flow = '11. 中級會計學額外驗證 22 章、3 附錄、110 題、145 筆搜尋索引、22 張 SVG，並執行 135 項第一輪檢查、23 項獨立數值與公式重算及 485 項第二輪檢查。'
          new_ia_flow = '11. 中級會計學先完成初版 QA，再套用發布後獨立二次內容審計修正；額外驗證 22 章、3 附錄、110 題、145 筆搜尋索引、22 張 SVG、1,110 項 v2 獨立檢查與 28 項量化重算。'
          if old_ia_flow in c:
              c = c.replace(old_ia_flow, new_ia_flow, 1)
          elif new_ia_flow not in c:
              raise AssertionError('intermediate accounting deployment-flow line not found')
          old_ia_workline = '- 中級會計學初版內容、兩輪 QA、canonical integration 與正式 Pages 部署均已完成。'
          new_ia_workline = '- 中級會計學初版、發布後獨立二次內容審計、糾錯修正與新版 Pages 部署均已完成；章節 ID、題目 ID 與題數未變。'
          if old_ia_workline in c:
              c = c.replace(old_ia_workline, new_ia_workline, 1)
          elif new_ia_workline not in c:
              raise AssertionError('intermediate accounting workline status not found')
"""
    if 'ia_section_v2 = (' not in text:
        text = replace_once(text, checkpoint_anchor, checkpoint_runtime + checkpoint_anchor, 'checkpoint v2 runtime')

    readme_anchor = "          micro_v2_line = '- 《個體經濟學》：一般大學中級個體經濟學，20 章、3 附錄、100 題題庫、154 筆搜尋索引與 20 張圖解；發布後獨立二次複核版本 `2026.07.29-2`。'\n"
    readme_runtime = """          intermediate_v2_line = '- 《中級會計學》：一般大學中級會計學，22 章、3 附錄、110 題題庫、145 筆搜尋索引與 22 張圖解；發布後獨立二次內容審計版本 `2026.07.29-2`。'
          ia_indexes = [i for i, line in enumerate(r_lines) if line.startswith('- 《中級會計學》：')]
          if ia_indexes:
              first = ia_indexes[0]
              r_lines[first] = intermediate_v2_line
              for i in reversed(ia_indexes[1:]):
                  del r_lines[i]
          else:
              insert_at = max(i for i, line in enumerate(r_lines) if line.startswith('- 《')) + 1
              r_lines.insert(insert_at, intermediate_v2_line)
"""
    # Insert after r_lines exists, immediately after the micro v2 normalization block.
    readme_insert_anchor = "          r = '\\n'.join(r_lines) + ('\\n' if r.endswith('\\n') else '')\n"
    if 'intermediate_v2_line =' not in text:
        text = replace_once(text, readme_insert_anchor, readme_runtime + readme_insert_anchor, 'README v2 runtime')

    target.write_text(text, encoding='utf-8')
    print(f'INTERMEDIATE_ACCOUNTING_V2_WORKFLOW_STAGED {target}')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('usage: stage_intermediate_accounting_v2_workflow.py SRC DST')
    main(sys.argv[1], sys.argv[2])
