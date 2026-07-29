#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

BOOK = 'econometrics'
BOOK_VERSION = '2026.07.30-2'


def replace_once(text: str, pattern: str, replacement: str, label: str) -> str:
    out, n = re.subn(pattern, replacement, text, count=1, flags=re.M)
    if n != 1:
        raise AssertionError(f'cannot update {label}')
    return out


def main(site_root: str) -> None:
    site = Path(site_root)
    library = json.loads((site / 'data/library.json').read_text(encoding='utf-8'))
    ids = [b['id'] for b in library['books']]
    if ids.count(BOOK) != 1 or 'industrial-economics' not in ids or ids.index(BOOK) > ids.index('industrial-economics'):
        raise AssertionError(f'econometrics registry/order drift: {ids}')
    if 'industry-trade' in ids and ids.index('industrial-economics') > ids.index('industry-trade'):
        raise AssertionError(f'industrial economics / industry trade order drift: {ids}')

    root = site / 'books' / BOOK
    manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    questions = json.loads((root / 'questions.json').read_text(encoding='utf-8'))
    search = json.loads((root / 'search.json').read_text(encoding='utf-8'))
    if manifest['version'] != BOOK_VERSION or questions['version'] != BOOK_VERSION:
        raise AssertionError('econometrics v3 content version drift')
    if len(manifest['chapters']) != 23 or questions['count'] != 100 or len(search['entries']) != 189:
        raise AssertionError('econometrics v3 artifact count drift')
    if len(list((site / 'assets/econometrics-svg').glob('*.svg'))) != 20:
        raise AssertionError('econometrics SVG count drift')

    artifact_id = os.environ.get('PAGES_ARTIFACT_ID', '')
    digest = os.environ.get('PAGES_ARTIFACT_DIGEST', '')
    sha = os.environ.get('PAGES_ARTIFACT_SHA256', '')
    if not artifact_id or not digest or not sha:
        raise AssertionError('missing verified Pages artifact environment')
    if digest.startswith('sha256:') and digest.split(':', 1)[1] != sha:
        raise AssertionError('artifact digest mismatch')
    reaudit_checks = int(os.environ.get('ECONOMETRICS_V3_REAUDIT_CHECKS', '0') or 0)
    if reaudit_checks <= 0:
        raise AssertionError('missing econometrics v3 reaudit metric')

    receipt_path = Path('docs/deployment_receipt.json')
    receipt = json.loads(receipt_path.read_text(encoding='utf-8'))
    receipt.update({
        'econometrics_version': BOOK_VERSION,
        'econometrics_chapter_count': 20,
        'econometrics_appendix_count': 3,
        'econometrics_question_count': 100,
        'econometrics_search_count': 189,
        'econometrics_figure_count': 20,
        'econometrics_initial_round1_check_count': 384,
        'econometrics_initial_round2_check_count': 675,
        'econometrics_initial_numeric_recheck_count': 29,
        'econometrics_initial_high_risk_answer_gate_count': 32,
        'econometrics_post_publication_reaudit': 'passed',
        'econometrics_post_publication_correction_count': 2,
        'econometrics_post_publication_reaudit_check_count': 57,
        'econometrics_second_content_reaudit': 'passed',
        'econometrics_second_content_reaudit_check_count': reaudit_checks,
        'econometrics_second_content_correction_area_count': 5,
        'econometrics_second_content_question_adjustment_count': 4,
        'econometrics_second_content_numeric_recheck_count': 29,
        'econometrics_ids_preserved': True,
        'econometrics_progress_compatibility': 'preserved',
        'artifact_verified_econometrics_html_count': 23,
        'artifact_verified_econometrics_question_count': 100,
        'artifact_verified_econometrics_search_count': 189,
        'artifact_verified_econometrics_svg_count': 20,
    })
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    run_id = os.environ['GITHUB_RUN_ID']
    source_sha = os.environ['GITHUB_SHA']
    status = f'''# 《計量經濟學》製作狀態

更新日期：2026-07-30

## 正式識別

- Book ID：`{BOOK}`
- 正式內容版本：`{BOOK_VERSION}`
- 正式書庫版本：`{library["version"]}`
- 狀態：已部署。
- 範圍文件：`docs/books/econometrics/scope.md`
- QA 報告：`docs/books/econometrics/qa_report.md`

## 正式成品

- 正文：20 章（ch00–ch19）。
- 附錄：3 份。
- 題庫：100 題，每章 5 題。
- 搜尋索引：189 筆。
- 自製 SVG：20 張。
- 章節 ID、題目 ID、題數與儲存鍵均未改動；既有閱讀進度與錯題紀錄相容。

## QA 與兩次發布後內容審計

- 初版第一輪 QA：384 項，29 個數值節點獨立重算。
- 初版第二輪 QA：675 項，32 題高風險答案 gate。
- 第一次發布後獨立內容審計：修正 FE／FD strict exogeneity 與 SATE／PATE 外推邊界；57 項 reaudit gate 通過。
- 第二次內容層人工審校：v3 獨立 validator 共 {reaudit_checks} 項通過，100 題重新結構／答案檢查，29 個數值節點重新由輸入計算。
- 本輪修正 5 個區域：
  1. IV／Wald 在效果異質時明確限定為相應假設下的 complier LATE／CACE，不再和 ATE／ATT 混用。
  2. 隨機實驗 noncompliance 明確區分 ITT、actual-treatment 非隨機比較與 assignment-as-IV 的 complier LATE。
  3. DiD 補上 no-anticipation／提前反應的識別邊界。
  4. Fuzzy RDD 明確寫成 cutoff 處 local compliers 的 LATE，不能無條件外推整體 ATE。
  5. 預測章修正 test-set leakage：validation／CV 用來選模，final test set 僅在選模完成後作最後評估。
- 同步修正 4 個題目／詳解節點，並更新附錄解題路線與名詞表；所有題目 ID 保持不變。

## 正式發布證據

- canonical workflow：`Deploy study library`
- workflow run：`{run_id}`
- source commit：`{source_sha}`
- Pages artifact：`{artifact_id}`
- Artifact digest：`{digest}`
- 正式書庫：{len(ids)} 本，版本 `{library["version"]}`。
- Pages deployment、artifact 下載後重驗與 deployment receipt 均成功。
'''
    Path('docs/books/econometrics/status.md').write_text(status, encoding='utf-8')

    qa_path = Path('docs/books/econometrics/qa_report.md')
    qa = qa_path.read_text(encoding='utf-8')
    block = f'''## 第二次內容層獨立審校 v3（2026-07-30）

本輪不是重跑既有 v2 gate，而是重新逐章閱讀正文、例題、題庫與附錄，專門尋找「公式表面沒錯，但 estimand、識別範圍或資料切分解讀會帶錯學生」的問題。

### 修正 1：Binary IV／Wald 的 LATE 範圍

- 保留既有 relevance、exogeneity／exclusion 與 weak-instrument 教學。
- 新增 complier、LATE／CACE 與 monotonicity（無 defiers）定義。
- 在 treatment effects 異質時，明確說明標準二元 IV 的 Wald ratio 在相應條件下識別 compliers 的 LATE，不得無條件改稱整體 ATE、ATT 或「所有實際接受 treatment 者效果」。
- 題目 `ch14-q05` 保留 ID，改為直接檢查 LATE 的目標族群與成立條件。

### 修正 2：Randomized experiment 的 noncompliance

- 修掉原先「assignment 作 IV 可估接受處置者的局部效果」的含糊說法。
- 改為：ITT 仍依原始 assignment；若把 assignment 作 IV，需額外 relevance、exclusion、monotonicity 等條件，典型 estimand 是 compliers 的 LATE／CACE，而非所有 actual treatment takers 的 ATT／TOT。
- 題目 `ch15-q04` 保留題幹與答案，詳解補上上述界線。

### 修正 3：DiD 的 no anticipation

- 在 parallel trends 之外補上 no-anticipation／提前反應邊界。
- 若政策正式生效前，單位已因預期政策而調整，被標成 pre-treatment 的期間可能已受處置時點影響；標準 pre／post 切分需重新定義或顯式處理 anticipation window。

### 修正 4：Fuzzy RDD 的 local complier estimand

- 明確把 fuzzy RDD 說成 cutoff 附近的局部 IV。
- 在 continuity、first-stage jump、exclusion、monotonicity 等標準條件下，局部 Wald ratio 的因果解讀是 cutoff 處 local compliers 的 LATE，不是全母體 ATE。
- 題目 `ch17-q05` 保留 ID，詳解補上 local complier 與 monotonicity 限制。

### 修正 5：Prediction 的 validation／test 分工

- 原正文已說 test set 應留到最後，但例題與 `ch18-q03` 卻用 test RMSE 比較候選模型，形成內部矛盾。
- 已把模型選擇改成 training + validation／cross-validation；final test set 在模型與超參數固定後才使用。
- 明列反覆看 test 再挑模型會造成 test leakage，不能再把同一 test 當未碰過的 final holdout。

### 題庫、數值與相容性重驗

- v3 獨立 validator：{reaudit_checks} 項通過。
- 100 題全部重新做存在性、答案、詳解、Book ID 與每章 5 題結構檢查。
- 29 個既有數值節點重新從原始輸入計算，並再比對正式顯示答案。
- 4 個題目／詳解節點調整：`ch14-q05`、`ch15-q04`、`ch17-q05`、`ch18-q03`；全部保留原 question ID。
- 20 章、3 附錄、100 題、189 搜尋、20 SVG 全部維持。
- chapter IDs `ch00`–`ch19`、100 個 question IDs、閱讀進度與錯題儲存結構均保持相容。

### v3 正式部署

- Book version：`{BOOK_VERSION}`。
- Shared library：`{library["version"]}`，{len(ids)} 本。
- Pages run：`{run_id}`。
- Pages artifact：`{artifact_id}`；digest `{digest}`。
- 部署後重新下載 artifact，再核對本書 23 份 HTML、100 題、189 搜尋與 20 SVG 均通過。
'''
    if '## 第二次內容層獨立審校 v3（2026-07-30）' in qa:
        qa = re.sub(r'## 第二次內容層獨立審校 v3（2026-07-30）\n.*\Z', block, qa, flags=re.S)
    else:
        qa = qa.rstrip() + '\n\n' + block
    qa_path.write_text(qa.rstrip() + '\n', encoding='utf-8')

    readme_path = Path('README.md')
    readme = readme_path.read_text(encoding='utf-8')
    readme = replace_once(readme, r'目前內容版本：`[^`]+`', f'目前內容版本：`{library["version"]}`', 'README version')
    econ_line = (
        f'- 《計量經濟學》：一般大學計量經濟學核心，20 章、3 附錄、100 題題庫、189 筆搜尋索引與 20 張圖解；'
        f'兩次發布後獨立審校已補強 FE strict exogeneity、SATE／PATE、IV／fuzzy RDD 的 LATE 範圍、DiD no anticipation 與 validation／test 分工，內容版本 `{BOOK_VERSION}`。'
    )
    lines = readme.splitlines()
    matches = [i for i, line in enumerate(lines) if line.startswith('- 《計量經濟學》：')]
    if len(matches) != 1:
        raise AssertionError(f'README econometrics line count={len(matches)}')
    lines[matches[0]] = econ_line
    readme_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')

    cp_path = Path('docs/shared_checkpoint.md')
    cp = cp_path.read_text(encoding='utf-8')
    section = f'''### 18. 計量經濟學
- Book ID：`econometrics`
- 正式內容版本：`{BOOK_VERSION}`
- 定位：一般大學計量經濟學；OLS、多元迴歸與推論、異質變異、模型設定、二元結果、時間序列、panel、IV／2SLS、實驗、DiD、RDD、預測與實證研究流程。
- 成品：20 章、3 附錄、100 題、189 搜尋、20 圖解。
- 初版 QA：Round 1 = 384、Round 2 = 675；29 個數值節點獨立重算、32 個高風險答案 gate。
- 第一次發布後審計：2 個精確化修正；v2 reaudit validator 57 項通過。
- 第二次內容層獨立審校：5 個修正區域、4 個題目／詳解節點調整；v3 reaudit validator {reaudit_checks} 項通過，100 題重檢、29 個數值節點重算。
- v3 修正重點：IV／noncompliance 與 fuzzy RDD 明確限定 complier LATE；DiD 補 no anticipation；prediction 改為 validation／CV 選模、final test 最後評估。
- 章節 ID、題目 ID、題數與閱讀／錯題儲存相容性均保持不變。
- 正式 Pages run：`{run_id}`；Source commit：`{source_sha}`；artifact：`{artifact_id}`。
- Artifact digest／下載 SHA-256：`{digest}`。
- 文件：`docs/books/econometrics/scope.md`、`docs/books/econometrics/qa_report.md`、`docs/books/econometrics/status.md`。
- 狀態：已部署。

'''
    cp, n = re.subn(r'(?ms)^### 18\. 計量經濟學\n.*?(?=^### 19\. 產業經濟學)', section, cp, count=1)
    if n != 1:
        raise AssertionError('checkpoint econometrics section not found')
    cp_path.write_text(cp, encoding='utf-8')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: python deploy/record_econometrics_v3_deployment.py SITE_ROOT')
    main(sys.argv[1])
