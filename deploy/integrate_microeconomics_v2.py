#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise AssertionError(f"{label}: expected exactly one match, got {count}")
    return text.replace(old, new, 1)


def main(workflow_path: str) -> None:
    path = Path(workflow_path)
    text = path.read_text(encoding="utf-8")

    old = '''          EXPECTED_LIBRARY_VERSION="$FINAL_LIBRARY_VERSION" python deploy/qa_microeconomics.py _site
          node --check _site/app.js
'''
    new = '''          EXPECTED_LIBRARY_VERSION="$FINAL_LIBRARY_VERSION" python deploy/qa_microeconomics.py _site
          python deploy/patch_microeconomics_v2.py _site
          python deploy/qa_microeconomics_v2.py _site
          node --check _site/app.js
'''
    text = replace_once(text, old, new, "insert microeconomics v2 patch and QA")

    old = '''              'microeconomics_version': '2026.07.29-1',
              'microeconomics_chapter_count': 20,
              'microeconomics_appendix_count': 3,
              'microeconomics_question_count': 100,
              'microeconomics_search_count': 154,
              'microeconomics_figure_count': 20,
              'microeconomics_content_audit': 'passed',
              'microeconomics_round1_check_count': 1321,
              'microeconomics_round2_check_count': 87,
              'microeconomics_quantitative_recheck_count': 15,
              'microeconomics_logic_recheck_count': 15,
'''
    new = '''              'microeconomics_version': '2026.07.29-2',
              'microeconomics_chapter_count': 20,
              'microeconomics_appendix_count': 3,
              'microeconomics_question_count': 100,
              'microeconomics_search_count': 154,
              'microeconomics_figure_count': 20,
              'microeconomics_content_audit': 'passed-after-post-publication-reaudit',
              'microeconomics_initial_round1_check_count': 1321,
              'microeconomics_initial_round2_check_count': 87,
              'microeconomics_post_publication_correction_count': 16,
              'microeconomics_question_adjustment_count': 4,
              'microeconomics_independent_check_count': 1616,
              'microeconomics_quantitative_recheck_count': 15,
              'microeconomics_logic_recheck_count': 20,
'''
    text = replace_once(text, old, new, "update deployment receipt metrics")

    text = replace_once(
        text,
        "- 正式內容版本：`2026.07.29-1`\n- 正式書庫版本：`{final_version}`",
        "- 正式內容版本：`2026.07.29-2`\n- 正式書庫版本：`{final_version}`",
        "update generated status version",
    )
    text = replace_once(
        text,
        "- 第一輪 QA：1321／1321 通過。\n- 第二輪 QA：87／87 通過；100 題逐題複核，另獨立重算 15 題量化題與重判 15 題高風險觀念題。",
        "- 初版 QA：第一輪 1321／1321、第二輪 87／87 通過。\n- 發布後獨立二次複核：1,616 項檢查通過；修正 16 個內容點，4 題題幹或詳解同步精確化，另重算 15 題量化題、重判 20 題高風險觀念題。",
        "update generated status QA summary",
    )

    marker = """          if '個體經濟學均已納入同一套正式書庫部署流程。' not in c:
              c = c.replace('成本會計學均已納入同一套正式書庫部署流程。', '成本會計學、個體經濟學均已納入同一套正式書庫部署流程。')
          cp.write_text(c, encoding='utf-8')
"""
    inject = '''          if '個體經濟學均已納入同一套正式書庫部署流程。' not in c:
              c = c.replace('成本會計學均已納入同一套正式書庫部署流程。', '成本會計學、個體經濟學均已納入同一套正式書庫部署流程。')
          micro_section = f''' + "'''" + '''### 個體經濟學

- Book ID：`microeconomics`
- 正式內容版本：`2026.07.29-2`
- 定位：一般大學中級個體經濟學，從近零基礎銜接消費者對偶、Slutsky、生產與成本、競爭／獨占、賽局、一般均衡、福利與資訊不對稱。
- 成品：20 章、3 附錄、100 題題庫、154 筆搜尋索引、20 張自製圖解。
- 初版 QA：第一輪 1,321／1,321、第二輪 87／87。
- 發布後獨立二次複核：1,616 項檢查通過；修正 16 個內容點，4 題題幹或詳解同步精確化；15 題量化題獨立重算、20 題高風險觀念題獨立重判。
- 閱讀進度相容性：章節 ID、題目 ID 與題數未變；部署回條確認 `progress_storage_changed=false`。
- 範圍文件：`docs/books/microeconomics/scope.md`
- QA 報告：`docs/books/microeconomics/qa_report.md`
- GitHub Pages 部署 run：`{os.environ['GITHUB_RUN_ID']}`。
- Source commit：`{os.environ['GITHUB_SHA']}`。
- 部署回條：`docs/deployment_receipt.json`。
- 狀態：已部署。

''' + "'''" + '''
          c, micro_section_count = re.subn(
              r'(?ms)^### 個體經濟學\\n.*?(?=^### |^## 部署流程)',
              micro_section,
              c,
              count=1,
          )
          if micro_section_count != 1:
              raise AssertionError('microeconomics checkpoint section not found')
          old_flow = '10. 個體經濟學額外驗證 20 章、3 附錄、100 題、154 筆搜尋索引、20 張 SVG，並執行 1,321 項第一輪檢查、87 項第二輪內容 gate、15 題量化重算與 15 題高風險觀念重判。'
          if old_flow not in c:
              raise AssertionError('microeconomics deployment-flow line not found')
          c = c.replace(
              old_flow,
              '10. 個體經濟學先通過初版兩輪 QA，再套用發布後獨立二次複核修正；額外驗證 20 章、3 附錄、100 題、154 筆搜尋索引、20 張 SVG、1,616 項二次檢查、15 題量化重算與 20 題高風險觀念重判。',
              1,
          )
          old_workline = '- 個體經濟學初版內容、兩輪 QA、canonical integration 與正式 Pages 部署均已完成。'
          if old_workline not in c:
              raise AssertionError('microeconomics workline status not found')
          c = c.replace(
              old_workline,
              '- 個體經濟學初版、發布後獨立二次複核、糾錯修正與新版 Pages 部署均已完成；章節 ID、題目 ID 與題數未變。',
              1,
          )
          cp.write_text(c, encoding='utf-8')
'''
    text = replace_once(text, marker, inject, "update shared checkpoint writeback")

    marker = "          r = re.sub(r'五本書均由同一個 canonical GitHub Pages 工作流部署。', '全部正式教材均由同一個 canonical GitHub Pages 工作流部署。', r)\n"
    inject = '''          micro_v2_line = '- 《個體經濟學》：一般大學中級個體經濟學，20 章、3 附錄、100 題題庫、154 筆搜尋索引與 20 張圖解；發布後獨立二次複核版本 `2026.07.29-2`。'
          r_lines = r.splitlines()
          micro_indexes = [i for i, line in enumerate(r_lines) if line.startswith('- 《個體經濟學》：')]
          if micro_indexes:
              first = micro_indexes[0]
              r_lines[first] = micro_v2_line
              for i in reversed(micro_indexes[1:]):
                  del r_lines[i]
          else:
              insert_at = max(i for i, line in enumerate(r_lines) if line.startswith('- 《')) + 1
              r_lines.insert(insert_at, micro_v2_line)
          r = '\\n'.join(r_lines) + ('\\n' if r.endswith('\\n') else '')
          r = re.sub(r'五本書均由同一個 canonical GitHub Pages 工作流部署。', '全部正式教材均由同一個 canonical GitHub Pages 工作流部署。', r)
'''
    text = replace_once(text, marker, inject, "update README writeback")

    path.write_text(text, encoding="utf-8")
    print("MICRO_V2_WORKFLOW_INTEGRATION_OK")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: integrate_microeconomics_v2.py WORKFLOW_PATH")
    main(sys.argv[1])
