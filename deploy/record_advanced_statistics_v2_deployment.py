#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

BOOK = 'advanced-statistics'
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
    if ids.count(BOOK) != 1:
        raise AssertionError(f'advanced statistics registry drift: {ids}')
    if 'computer-fundamentals' in ids and ids.index(BOOK) > ids.index('computer-fundamentals'):
        raise AssertionError('advanced statistics canonical order drift')

    root = site / 'books' / BOOK
    manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    questions = json.loads((root / 'questions.json').read_text(encoding='utf-8'))
    search = json.loads((root / 'search.json').read_text(encoding='utf-8'))
    if manifest['version'] != BOOK_VERSION or questions['version'] != BOOK_VERSION:
        raise AssertionError('advanced statistics v2 content version drift')
    if len(manifest['chapters']) != 23 or questions['count'] != 100 or len(search['entries']) != 189:
        raise AssertionError('advanced statistics artifact count drift')
    if len(list((site / 'assets/advanced-statistics-svg').glob('*.svg'))) != 20:
        raise AssertionError('advanced statistics SVG count drift')

    artifact_id = os.environ.get('PAGES_ARTIFACT_ID', '')
    digest = os.environ.get('PAGES_ARTIFACT_DIGEST', '')
    sha = os.environ.get('PAGES_ARTIFACT_SHA256', '')
    if not artifact_id or not digest or not sha:
        raise AssertionError('missing verified Pages artifact environment')
    if digest.startswith('sha256:') and digest.split(':', 1)[1] != sha:
        raise AssertionError('artifact digest mismatch')

    reaudit_checks = int(os.environ.get('ADVSTAT_REAUDIT_CHECKS', '0') or 0)
    numeric_rechecks = int(os.environ.get('ADVSTAT_NUMERIC_RECHECKS', '0') or 0)
    if reaudit_checks <= 0 or numeric_rechecks <= 0:
        raise AssertionError('missing advanced statistics reaudit metrics')

    receipt_path = Path('docs/deployment_receipt.json')
    receipt = json.loads(receipt_path.read_text(encoding='utf-8'))
    receipt.update({
        'advanced_statistics_version': BOOK_VERSION,
        'advanced_statistics_chapter_count': 20,
        'advanced_statistics_appendix_count': 3,
        'advanced_statistics_question_count': 100,
        'advanced_statistics_search_count': 189,
        'advanced_statistics_figure_count': 20,
        'advanced_statistics_initial_quantitative_recheck_count': 27,
        'advanced_statistics_initial_high_risk_concept_gate_count': 45,
        'advanced_statistics_post_publication_reaudit': 'passed-after-second-content-audit',
        'advanced_statistics_post_publication_correction_area_count': 10,
        'advanced_statistics_question_adjustment_count': 7,
        'advanced_statistics_reaudit_check_count': reaudit_checks,
        'advanced_statistics_reaudit_numeric_recheck_count': numeric_rechecks,
        'advanced_statistics_ids_preserved': True,
        'advanced_statistics_progress_compatibility': 'preserved',
        'advanced_statistics_other_books_hashes_preserved': True,
        'artifact_verified_advanced_statistics_html_count': 23,
        'artifact_verified_advanced_statistics_question_count': 100,
        'artifact_verified_advanced_statistics_search_count': 189,
        'artifact_verified_advanced_statistics_svg_count': 20,
    })
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    run_id = os.environ['GITHUB_RUN_ID']
    source_sha = os.environ['GITHUB_SHA']
    status = f'''# 《高等統計學》製作狀態

更新日期：2026-07-30

## 正式識別

- Book ID：`{BOOK}`
- 正式內容版本：`{BOOK_VERSION}`
- 正式書庫版本：`{library["version"]}`
- 狀態：已部署。
- 範圍文件：`docs/books/advanced-statistics/scope.md`
- QA 報告：`docs/books/advanced-statistics/qa_report.md`

## 成品與第二次內容審計

- 正文 20 章、附錄 3 份、題庫 100 題、搜尋索引 189 筆、自製 SVG 20 張。
- 初版兩輪 QA 保留：27 個量化節點獨立重算、45 個高風險概念 gate。
- 2026-07-30 第二次內容審計：10 個章節修正／補強區域、7 題題庫精確化；v2 validator {reaudit_checks} 項、獨立數值重算 {numeric_rechecks} 項全數通過。
- 主要修正：完備性與充分性的一般關係、Negative Binomial、Slutsky、MLE invariance、一致性／漸近常態、條件常態、Rao–Blackwell／CRLB、精確 z/t 區間、size vs level、p-value／NP、UMP／MLR／Wilks、Gauss–Markov 條件。
- chapter IDs `ch00`–`ch19`、100 個 question IDs、題數與儲存鍵全部維持；既有閱讀進度與錯題紀錄相容。
- 正式整合只改本書與本書衍生索引；其他正式教材內容 hash 保持不變。

## 部署

- canonical workflow：`Deploy study library`
- workflow run：`{run_id}`
- source commit：`{source_sha}`
- Pages artifact：`{artifact_id}`
- Artifact digest：`{digest}`
- 正式書庫：{len(ids)} 本，版本 `{library["version"]}`。
- Pages deployment、artifact 下載後重驗與 deployment receipt 均成功。
'''
    Path('docs/books/advanced-statistics/status.md').write_text(status, encoding='utf-8')

    qa_path = Path('docs/books/advanced-statistics/qa_report.md')
    qa = qa_path.read_text(encoding='utf-8')
    block = f'''## 第二次內容審計 v2（2026-07-30）

本輪不是重跑初版 QA，而是重新逐章審查公式、成立條件、參數化、例題與 100 題答案，優先處理「算式看似正確，但少一個條件就會誤導」的內容。

### 實際修正／補強

1. **充分與完備**：移除「完備性比充分性更強」的一般化說法。兩者是不同性質，一般互不推出；Lehmann–Scheffé 使用的是同一統計量同時完備且充分。
2. **Negative Binomial**：補齊「直到第 r 次成功的試驗總次數」參數化、支撐、PMF、期望與變異數，並明示另一種「失敗次數」口徑不可混用。
3. **多元常態**：條件常態公式明列聯合常態與 `Var(X)>0`；只有兩個邊際常態不足以套用。
4. **LLN／Slutsky／Delta method**：補正式 Slutsky 敘述與 studentization 例；補 `g'(theta)=0` 時一階 Delta method 退化的警告。
5. **MLE**：補 MLE invariance 與參數轉換例題。
6. **估計量品質**：補一致性、漸近常態；Fisher information／CRLB 明列內點與正則條件；Rao–Blackwell 明列平方可積／有限變異數語境。
7. **信賴區間**：區分常態且 sigma 已知時的精確 z 區間與一般 CLT 大樣本近似；精確 t 區間明列 iid 常態與 S² 定義。
8. **檢定理論**：分清 size 與 level alpha；p-value 補 composite null／nuisance parameter 校準；NP 補離散情況可能需 randomization。
9. **UMP／LRT／Wilks**：補 MLR／Karlin–Rubin 結構；Wilks 明列 H0、正則巢狀、可識別、內點條件及非正則邊界例外。
10. **線性模型**：Gauss–Markov 改成條件於 X 的 `E(epsilon|X)=0`、`Var(epsilon|X)=sigma²I`、full rank；精確 F 說明 q、p 與 `F_(q,n-p)`。

### 題庫調整

- 保留全部 100 個 question ID，只改 7 題內容／詳解：`ch03-q05`、`ch11-q01`、`ch13-q03`、`ch14-q04`、`ch15-q05`、`ch17-q04`、`ch18-q04`。
- 題數仍為每章 5 題，閱讀進度與錯題儲存鍵不變。

### 獨立 QA 與部署

- v2 reaudit validator：{reaudit_checks} 項通過。
- 獨立數值重算：{numeric_rechecks} 項通過；含 Negative Binomial、Slutsky 尺度轉換、Delta、χ²、t、Gamma、多元常態、次序統計量、Bayes、CI、p-value、OLS／R² 等。
- 其他正式教材逐檔 hash 比對：無變更。
- Book version：`{BOOK_VERSION}`；shared library：`{library["version"]}`，{len(ids)} 本。
- Pages run：`{run_id}`；artifact：`{artifact_id}`；digest `{digest}`。
- 部署後重新下載 artifact，再次核對本書 23 份 HTML、100 題、189 搜尋、20 SVG 與 v2 QA 全部通過。
'''
    marker = '## 第二次內容審計 v2（2026-07-30）'
    if marker in qa:
        qa = re.sub(r'## 第二次內容審計 v2（2026-07-30）\n.*\Z', block, qa, flags=re.S)
    else:
        qa = qa.rstrip() + '\n\n' + block
    qa_path.write_text(qa.rstrip() + '\n', encoding='utf-8')

    readme_path = Path('README.md')
    readme = readme_path.read_text(encoding='utf-8')
    lines = readme.splitlines()
    matches = [i for i, line in enumerate(lines) if line.startswith('- 《高等統計學》：')]
    if len(matches) != 1:
        raise AssertionError(f'README advanced-statistics line count={len(matches)}')
    lines[matches[0]] = (
        f'- 《高等統計學》：一般大學高等統計／數理統計核心，20 章、3 附錄、100 題題庫、189 筆搜尋索引與 20 張圖解；'
        f'第二次內容審計已修正充分／完備關係並補強 Negative Binomial、Slutsky、MLE invariance、size／level、Wilks 與 Gauss–Markov 等成立條件，內容版本 `{BOOK_VERSION}`。'
    )
    readme_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')

    cp_path = Path('docs/shared_checkpoint.md')
    cp = cp_path.read_text(encoding='utf-8')
    section = f'''### 13. 高等統計學
- Book ID：`advanced-statistics`
- 正式內容版本：`{BOOK_VERSION}`
- 定位：一般大學高等統計／數理統計核心；承接基礎統計，聚焦機率模型、多元分配、極限定理、抽樣分配、估計與檢定理論。
- 成品：20 章、3 附錄、100 題、189 搜尋、20 圖解。
- 初版 QA：27 個量化節點獨立重算、45 個高風險概念 gate。
- 2026-07-30 第二次內容審計：10 個章節修正／補強、7 題題庫精確化；v2 validator {reaudit_checks} 項、數值重算 {numeric_rechecks} 項通過。
- 修正重點：充分／完備關係、Negative Binomial、Slutsky、MLE invariance、一致性／漸近常態、Rao–Blackwell／CRLB、精確 z/t、size vs level、p-value／NP、UMP／MLR／Wilks、Gauss–Markov。
- chapter／question IDs、題數與閱讀／錯題儲存相容性全部保持不變；其他正式教材內容 hash 不變。
- 正式 Pages run：`{run_id}`；Source commit：`{source_sha}`；artifact：`{artifact_id}`。
- Artifact digest／下載 SHA-256：`{digest}`。
- 文件：`docs/books/advanced-statistics/scope.md`、`docs/books/advanced-statistics/qa_report.md`、`docs/books/advanced-statistics/status.md`。
- 狀態：已部署。

'''
    cp, n = re.subn(r'(?ms)^### 13\. 高等統計學\n.*?(?=^### 14\. 計算機概論)', section, cp, count=1)
    if n != 1:
        raise AssertionError('checkpoint advanced statistics section not found')
    cp_path.write_text(cp, encoding='utf-8')

    print(json.dumps({
        'book': BOOK,
        'version': BOOK_VERSION,
        'reaudit_checks': reaudit_checks,
        'numeric_rechecks': numeric_rechecks,
        'artifact': artifact_id,
    }, ensure_ascii=False))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: python deploy/record_advanced_statistics_v2_deployment.py SITE_ROOT')
    main(sys.argv[1])
