#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise AssertionError(f'{label}: expected one occurrence, got {count}')
    return text.replace(old, new, 1)


def main(source_path: str, target_path: str) -> None:
    source = Path(source_path)
    target = Path(target_path)
    text = source.read_text(encoding='utf-8')

    old_macro_step = '''      - name: Generate and independently validate macroeconomics textbook
        run: |
          cp _site/data/library.json /tmp/pre-macroeconomics-library.json
          cat deploy/generate-macroeconomics.py.gz.b64.part* | tr -d '\\n\\r\\t ' | base64 --decode > /tmp/generate-macroeconomics.py.gz
          echo 'c3643675f863883a429d492334b291d430ebfa87bf0b1cbf49806dfe790b6b34  /tmp/generate-macroeconomics.py.gz' | sha256sum --check -
          gzip --test /tmp/generate-macroeconomics.py.gz
          gzip --decompress --stdout /tmp/generate-macroeconomics.py.gz > /tmp/generate-macroeconomics.py
          python -m py_compile /tmp/generate-macroeconomics.py
          python /tmp/generate-macroeconomics.py _site
          FINAL_LIBRARY_VERSION="$(python deploy/finalize_macroeconomics_library.py _site /tmp/pre-macroeconomics-library.json)"
          EXPECTED_LIBRARY_VERSION="$FINAL_LIBRARY_VERSION" PRE_LIBRARY_JSON=/tmp/pre-macroeconomics-library.json python deploy/validate_macroeconomics.py _site
          node --check _site/app.js
          node --check _site/sw.js
          echo "MACROECONOMICS_FINAL_LIBRARY_VERSION=$FINAL_LIBRARY_VERSION"
'''
    new_macro_step = '''      - name: Generate, independently validate, and apply macroeconomics v2 reaudit
        run: |
          cp _site/data/library.json /tmp/pre-macroeconomics-library.json
          cat deploy/generate-macroeconomics.py.gz.b64.part* | tr -d '\\n\\r\\t ' | base64 --decode > /tmp/generate-macroeconomics.py.gz
          echo 'c3643675f863883a429d492334b291d430ebfa87bf0b1cbf49806dfe790b6b34  /tmp/generate-macroeconomics.py.gz' | sha256sum --check -
          gzip --test /tmp/generate-macroeconomics.py.gz
          gzip --decompress --stdout /tmp/generate-macroeconomics.py.gz > /tmp/generate-macroeconomics.py
          python -m py_compile /tmp/generate-macroeconomics.py
          python /tmp/generate-macroeconomics.py _site
          INITIAL_MACRO_LIBRARY_VERSION="$(python deploy/finalize_macroeconomics_library.py _site /tmp/pre-macroeconomics-library.json)"
          EXPECTED_LIBRARY_VERSION="$INITIAL_MACRO_LIBRARY_VERSION" PRE_LIBRARY_JSON=/tmp/pre-macroeconomics-library.json python deploy/validate_macroeconomics.py _site
          python -m py_compile deploy/patch_macroeconomics_v2.py deploy/finalize_macroeconomics_v2_library.py deploy/qa_macroeconomics_v2.py
          python deploy/patch_macroeconomics_v2.py _site
          FINAL_LIBRARY_VERSION="$(python deploy/finalize_macroeconomics_v2_library.py _site "$INITIAL_MACRO_LIBRARY_VERSION")"
          python deploy/qa_macroeconomics_v2.py _site "$FINAL_LIBRARY_VERSION"
          node --check _site/app.js
          node --check _site/sw.js
          echo "MACROECONOMICS_V2_QA library=$FINAL_LIBRARY_VERSION checks=201 corrections=14 question_adjustments=7 quantitative_rechecks=20"
'''
    text = replace_once(text, old_macro_step, new_macro_step, 'macro generation step')

    old_receipt = '''              'macroeconomics_version': '2026.07.29-1',
              'macroeconomics_chapter_count': 20,
              'macroeconomics_appendix_count': 3,
              'macroeconomics_question_count': 100,
              'macroeconomics_search_count': 143,
              'macroeconomics_figure_count': 20,
              'macroeconomics_content_audit': 'passed',
              'macroeconomics_numeric_recheck_count': 18,
              'macroeconomics_two_round_qa': 'passed',
'''
    new_receipt = '''              'macroeconomics_version': '2026.07.29-2',
              'macroeconomics_chapter_count': 20,
              'macroeconomics_appendix_count': 3,
              'macroeconomics_question_count': 100,
              'macroeconomics_search_count': 143,
              'macroeconomics_figure_count': 20,
              'macroeconomics_content_audit': 'passed-after-post-publication-reaudit',
              'macroeconomics_initial_numeric_recheck_count': 18,
              'macroeconomics_post_publication_correction_count': 14,
              'macroeconomics_question_adjustment_count': 7,
              'macroeconomics_independent_check_count': 201,
              'macroeconomics_quantitative_recheck_count': 20,
              'macroeconomics_two_round_qa': 'passed',
'''
    text = replace_once(text, old_receipt, new_receipt, 'macro receipt fields')

    status_start = "          macro_status = (\n"
    status_end = "          Path('docs/books/macroeconomics/status.md').write_text(macro_status, encoding='utf-8')\n"
    start = text.index(status_start)
    end = text.index(status_end, start) + len(status_end)
    new_status = '''          macro_status = (
              '# 《總體經濟學》製作狀態\\n\\n'
              '更新日期：2026-07-29\\n\\n'
              '## 版本\\n\\n'
              '- Book ID：`macroeconomics`\\n'
              '- 正式內容版本：`2026.07.29-2`\\n'
              f'- 正式書庫版本：`{final_version}`\\n'
              '- 狀態：已部署。\\n\\n'
              '## 成品與 QA\\n\\n'
              '- 正文 20 章、附錄 3 份、題庫 100 題、搜尋索引 143 筆、自製 SVG 20 張。\\n'
              '- 初版 QA：兩輪內容與題庫複核通過；100 題逐題複核，18 題具體數值題獨立重算一致。\\n'
              '- 發布後第二次獨立內容複核：201／201 項通過；完成 14 個實質內容修正事件、7 題題幹／答案／詳解調整，20 題量化題重新驗算。\\n'
              '- 主要修正：百分點單位、自然失業搜尋流量變數、IS 儲蓄投資推導、SRAS 機制、Taylor principle、完整經常帳 CA=S-I、相對 PPP 匯率方向與 Mundell–Fleming 標準模型政策結論。\\n'
              '- 閱讀進度相容性：章節 ID、題目 ID 與題數均未變；既有閱讀進度與錯題紀錄保留。\\n\\n'
              '## 部署\\n\\n'
              '- canonical workflow：`Deploy study library`\\n'
              f'- workflow run：`{os.environ["GITHUB_RUN_ID"]}`\\n'
              f'- source commit：`{os.environ["GITHUB_SHA"]}`\\n'
              f'- 正式書庫書籍數：{book_count} 本。\\n'
              '- GitHub Pages 部署成功並已寫回 deployment receipt。\\n'
          )
          Path('docs/books/macroeconomics/status.md').write_text(macro_status, encoding='utf-8')
'''
    text = text[:start] + new_status + text[end:]

    checkpoint_start = "          if '### 總體經濟學' not in c:\n"
    checkpoint_end = "          cp.write_text(c, encoding='utf-8')\n"
    start = text.index(checkpoint_start)
    end = text.index(checkpoint_end, start)
    new_checkpoint = '''          macro_section = (
              '### 總體經濟學\\n\\n'
              '- Book ID：`macroeconomics`\\n'
              '- 正式內容版本：`2026.07.29-2`\\n'
              '- 定位：一般大學總體經濟學，聚焦總體衡量、長期成長、短期景氣、財政貨幣政策與開放經濟。\\n'
              '- 成品：20 章、3 附錄、100 題題庫、143 筆搜尋索引、20 張自製圖解。\\n'
              '- 初版 QA：兩輪內容與題庫複核通過；18 題數值題獨立重算一致。\\n'
              '- 發布後第二次獨立內容複核：201／201 項通過；14 個實質內容修正事件、7 題題庫調整、20 題量化題重新驗算。\\n'
              '- 閱讀進度相容性：章節 ID、題目 ID 與題數均未變；部署回條確認 `progress_storage_changed=false`。\\n'
              '- 範圍文件：`docs/books/macroeconomics/scope.md`\\n'
              '- QA 報告：`docs/books/macroeconomics/qa_report.md`\\n'
              f'- GitHub Pages 部署 run：`{os.environ["GITHUB_RUN_ID"]}`。\\n'
              f'- Source commit：`{os.environ["GITHUB_SHA"]}`。\\n'
              '- 部署回條：`docs/deployment_receipt.json`。\\n'
              '- 狀態：已部署。\\n\\n'
          )
          c, macro_section_count = re.subn(
              r'(?ms)^### 總體經濟學\\n.*?(?=^### |^## 部署流程)',
              macro_section,
              c,
              count=1,
          )
          if macro_section_count != 1:
              raise AssertionError('macroeconomics checkpoint section not found')
'''
    text = text[:start] + new_checkpoint + text[end:]

    readme_start = "          macro = '- 《總體經濟學》"
    readme_end = "          r = re.sub(r'五本書均由同一個 canonical GitHub Pages 工作流部署。', '全部正式教材均由同一個 canonical GitHub Pages 工作流部署。', r)\n"
    start = text.index(readme_start)
    end = text.index(readme_end, start)
    new_readme = '''          macro_v2_line = '- 《總體經濟學》：一般大學總體經濟學，20 章、3 附錄、100 題題庫、143 筆搜尋索引與 20 張圖解；發布後第二次獨立內容複核版本 `2026.07.29-2`。'
          r_lines = r.splitlines()
          macro_indexes = [i for i, line in enumerate(r_lines) if line.startswith('- 《總體經濟學》：')]
          if macro_indexes:
              first = macro_indexes[0]
              r_lines[first] = macro_v2_line
              for i in reversed(macro_indexes[1:]):
                  del r_lines[i]
          else:
              insert_at = max(i for i, line in enumerate(r_lines) if line.startswith('- 《')) + 1
              r_lines.insert(insert_at, macro_v2_line)
          r = '\\n'.join(r_lines) + ('\\n' if r.endswith('\\n') else '')
'''
    text = text[:start] + new_readme + text[end:]

    required = [
        'python deploy/patch_macroeconomics_v2.py _site',
        'python deploy/finalize_macroeconomics_v2_library.py _site',
        'python deploy/qa_macroeconomics_v2.py _site',
        "'macroeconomics_version': '2026.07.29-2'",
        "'macroeconomics_post_publication_correction_count': 14",
        "'macroeconomics_question_adjustment_count': 7",
        "'macroeconomics_independent_check_count': 201",
        "'macroeconomics_quantitative_recheck_count': 20",
        '發布後第二次獨立內容複核',
    ]
    for token in required:
        if token not in text:
            raise AssertionError(f'missing staged workflow token: {token}')
    if "'macroeconomics_version': '2026.07.29-1'" in text:
        raise AssertionError('stale macroeconomics v1 receipt field remains')

    target.write_text(text, encoding='utf-8')
    print('MACRO_V2_WORKFLOW_STAGED_OK')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('usage: stage_macroeconomics_v2_workflow.py SOURCE_WORKFLOW TARGET_WORKFLOW')
    main(sys.argv[1], sys.argv[2])
