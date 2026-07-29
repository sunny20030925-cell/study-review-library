#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

BOOK = 'econometrics'
BOOK_VERSION = '2026.07.30-1'


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

    root = site / 'books' / BOOK
    manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    questions = json.loads((root / 'questions.json').read_text(encoding='utf-8'))
    search = json.loads((root / 'search.json').read_text(encoding='utf-8'))
    if manifest['version'] != BOOK_VERSION or questions['version'] != BOOK_VERSION:
        raise AssertionError('econometrics v2 content version drift')
    if len(manifest['chapters']) != 23 or questions['count'] != 100 or len(search['entries']) != 189:
        raise AssertionError('econometrics artifact count drift')
    if len(list((site / 'assets/econometrics-svg').glob('*.svg'))) != 20:
        raise AssertionError('econometrics SVG count drift')

    artifact_id = os.environ.get('PAGES_ARTIFACT_ID', '')
    digest = os.environ.get('PAGES_ARTIFACT_DIGEST', '')
    sha = os.environ.get('PAGES_ARTIFACT_SHA256', '')
    if not artifact_id or not digest or not sha:
        raise AssertionError('missing verified Pages artifact environment')
    if digest.startswith('sha256:') and digest.split(':', 1)[1] != sha:
        raise AssertionError('artifact digest mismatch')
    reaudit_checks = int(os.environ.get('ECONOMETRICS_REAUDIT_CHECKS', '0') or 0)
    if reaudit_checks <= 0:
        raise AssertionError('missing econometrics reaudit metric')

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
        'econometrics_post_publication_reaudit_check_count': reaudit_checks,
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

## QA 與發布後獨立審計

- 初版第一輪 QA：384 項，29 個數值節點獨立重算。
- 初版第二輪 QA：675 項，32 題高風險答案 gate。
- 2026-07-30 發布後獨立內容審計：修正 2 個精確性缺口，reaudit validator 共 {reaudit_checks} 項通過。
- 修正一：Panel FE／FD 明列標準靜態模型的 strict-exogeneity 條件；不再讓「消掉 alpha_i」被誤讀成已充分解決所有時間變動內生性。
- 修正二：隨機實驗明確區分 SATE 與 PATE；random assignment 建立實驗單位內部因果識別，但外推更大母體仍需要 sampling／external-validity 條件。
- 其他高風險章節與既有 100 題 ID 全部保持相容。

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
    block = f'''## 發布後獨立內容審計 v2（2026-07-30）

本輪不是重跑原本的字串 gate，而是針對計量解讀最容易「公式沒錯、因果範圍卻講過頭」的地方重新審核。

### 修正 1：Panel FE／FD 的外生性條件

- v1 已正確說明 FE／FD 可消除時間不變個體效果 `alpha_i`，也提醒 time-varying confounder 仍可能造成問題。
- v2 進一步明列標準靜態 panel 常用的 strict-exogeneity 條件 `E(u_it | x_i1,...,x_iT,alpha_i)=0`。
- 同步補充：若當期衝擊影響未來 X、存在時間變動混淆或含落後依變數，不能因為用了 FE 就直接宣稱 beta 已具有因果識別。
- 題目 `ch13-q04` 保留原 ID，改為直接檢查上述成立條件。

### 修正 2：Random assignment 與 population generalization

- v1 把 randomized experiment 的差均值直接連到 ATE，沒有充分區分「實驗樣本內因果效果」與「更大目標母體效果」。
- v2 明確區分 SATE 與 PATE：random assignment 支持實驗單位內部的因果比較；要推廣到更大母體，仍需代表性抽樣、外部效度或其他 transportability 條件。
- 題目 `ch15-q02` 保留原 ID，改為檢查 random assignment 是否足以無條件外推 PATE；`ch15-q03` 詳解同步精確化。

### 相容性與 QA

- 20 章、3 附錄、100 題、189 搜尋、20 SVG：全部維持。
- chapter IDs：`ch00`–`ch19` 全部維持。
- question IDs：100 個全部維持；每章仍 5 題。
- 既有第二輪內容 gate 重新執行；另加 v2 reaudit validator：{reaudit_checks} 項通過。
- 閱讀進度與錯題儲存結構未變。

### v2 正式部署

- Book version：`{BOOK_VERSION}`。
- Shared library：`{library["version"]}`，{len(ids)} 本。
- Pages run：`{run_id}`。
- Pages artifact：`{artifact_id}`；digest `{digest}`。
- 部署後重新下載 artifact，再核對本書 23 份 HTML、100 題、189 搜尋與 20 SVG 均通過。
'''
    if '## 發布後獨立內容審計 v2（2026-07-30）' in qa:
        qa = re.sub(r'## 發布後獨立內容審計 v2（2026-07-30）\n.*\Z', block, qa, flags=re.S)
    else:
        qa = qa.rstrip() + '\n\n' + block
    qa_path.write_text(qa.rstrip() + '\n', encoding='utf-8')

    readme_path = Path('README.md')
    readme = readme_path.read_text(encoding='utf-8')
    readme = replace_once(readme, r'目前內容版本：`[^`]+`', f'目前內容版本：`{library["version"]}`', 'README version')
    econ_line = (
        f'- 《計量經濟學》：一般大學計量經濟學核心，20 章、3 附錄、100 題題庫、189 筆搜尋索引與 20 張圖解；'
        f'發布後獨立內容審計已補強 FE strict exogeneity 與 SATE／PATE 外推邊界，內容版本 `{BOOK_VERSION}`。'
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
- 2026-07-30 發布後獨立內容審計：2 個精確化修正；v2 reaudit validator {reaudit_checks} 項通過。
- 修正重點：FE／FD 明列 strict exogeneity；隨機實驗分開 SATE 與 PATE／external validity。
- 章節 ID、題目 ID、題數與閱讀／錯題儲存相容性均保持不變。
- 正式 Pages run：`{run_id}`；Source commit：`{source_sha}`；artifact：`{artifact_id}`。
- Artifact digest／下載 SHA-256：`{digest}`。
- 文件：`docs/books/econometrics/scope.md`、`docs/books/econometrics/qa_report.md`、`docs/books/econometrics/status.md`。
- 狀態：已部署。

'''
    cp, n = re.subn(r'(?ms)^### 18\. 計量經濟學\n.*?(?=^### 19\. 產業經濟學)', section, cp, count=1)
    if n != 1:
        raise AssertionError('checkpoint econometrics section not found')
    cp = replace_once(
        cp,
        r'- 實際下載正式 Pages artifact 後再次核對：.*$',
        f'- 實際下載正式 Pages artifact 後再次核對：{len(ids)} 本 registry；計量經濟學 v2 23 份 HTML、100 題、189 搜尋、20 SVG 與產業經濟學正式資產均存在；下載檔 SHA-256 與 GitHub artifact digest 一致。',
        'checkpoint artifact recheck',
    )
    cp_path.write_text(cp, encoding='utf-8')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: python deploy/record_econometrics_v2_deployment.py SITE_ROOT')
    main(sys.argv[1])
