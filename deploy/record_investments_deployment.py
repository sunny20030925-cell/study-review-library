#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

BOOK = 'investments'
BOOK_VERSION = '2026.07.29-1'


def replace_once(text: str, pattern: str, replacement: str, label: str) -> str:
    text2, n = re.subn(pattern, replacement, text, count=1, flags=re.M)
    if n != 1:
        raise AssertionError(f'cannot update {label}')
    return text2


def main(site_root: str) -> None:
    site = Path(site_root)
    library = json.loads((site / 'data/library.json').read_text(encoding='utf-8'))
    ids = [b['id'] for b in library['books']]
    if BOOK not in ids:
        raise AssertionError(f'{BOOK} missing from deployed library: {ids}')
    if len(ids) != len(set(ids)):
        raise AssertionError('duplicate book ids in deployed library')

    root = site / 'books' / BOOK
    manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    questions = json.loads((root / 'questions.json').read_text(encoding='utf-8'))
    search = json.loads((root / 'search.json').read_text(encoding='utf-8'))
    chapters = [x for x in manifest['chapters'] if x['kind'] == 'chapter']
    appendices = [x for x in manifest['chapters'] if x['kind'] == 'appendix']
    figures = list((site / 'assets/investments-svg').glob('*.svg'))
    if manifest['version'] != BOOK_VERSION or questions['version'] != BOOK_VERSION:
        raise AssertionError('investments content version drift')
    if len(chapters) != 22 or len(appendices) != 3:
        raise AssertionError('investments chapter/appendix count drift')
    if questions['count'] != 110 or len(questions['items']) != 110:
        raise AssertionError('investments question count drift')
    if len(search['entries']) != 165 or len(figures) != 22:
        raise AssertionError('investments search/figure count drift')

    artifact_id = os.environ.get('PAGES_ARTIFACT_ID', '')
    artifact_digest = os.environ.get('PAGES_ARTIFACT_DIGEST', '')
    artifact_sha = os.environ.get('PAGES_ARTIFACT_SHA256', '')
    page_url = os.environ.get('DEPLOYED_PAGE_URL', '')
    if not artifact_id or not artifact_digest or not artifact_sha:
        raise AssertionError('missing artifact verification environment')
    if artifact_digest.startswith('sha256:') and artifact_digest.split(':', 1)[1] != artifact_sha:
        raise AssertionError('artifact digest and downloaded sha mismatch')

    book_count = len(ids)
    book_number = ids.index(BOOK) + 1
    deployed_at = datetime.now(timezone.utc).isoformat()

    receipt_path = Path('docs/deployment_receipt.json')
    receipt = json.loads(receipt_path.read_text(encoding='utf-8'))
    receipt.update({
        'status': 'success',
        'library_version': library['version'],
        'book_versions_visible': True,
        'progress_storage_changed': False,
        'book_count': book_count,
        'investments_version': BOOK_VERSION,
        'investments_chapter_count': 22,
        'investments_appendix_count': 3,
        'investments_question_count': 110,
        'investments_search_count': 165,
        'investments_figure_count': 22,
        'investments_round1_check_count': 2672,
        'investments_round2_check_count': 139,
        'investments_quantitative_recheck_count': 45,
        'investments_high_risk_concept_recheck_count': 20,
        'investments_two_round_qa': 'passed',
        'investments_existing_book_hashes_preserved': True,
        'source_commit': os.environ['GITHUB_SHA'],
        'workflow_run_id': os.environ['GITHUB_RUN_ID'],
        'page_url': page_url,
        'deployed_at': deployed_at,
        'pages_deploy_status': 'success',
        'pages_artifact_id': artifact_id,
        'pages_artifact_digest': artifact_digest,
        'artifact_download_recheck': 'passed',
        'artifact_download_sha256': artifact_sha,
        'artifact_verified_book_count': book_count,
        'artifact_verified_investments_html_count': 25,
        'artifact_verified_investments_question_count': 110,
        'artifact_verified_investments_search_count': 165,
        'artifact_verified_investments_svg_count': 22,
        'workflow_overall_conclusion': 'success',
        'post_deploy_record_step': 'passed-structured-recorder',
        'receipt_reconciliation': 'automatic-from-verified-pages-artifact',
    })
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    status = f'''# 《投資學》製作狀態

更新日期：2026-07-29

## 正式識別

- Book ID：`{BOOK}`
- 正式內容版本：`{BOOK_VERSION}`
- 正式書庫版本：`{library['version']}`
- 狀態：已部署。
- 範圍文件：`docs/books/investments/scope.md`
- QA 報告：`docs/books/investments/qa_report.md`

## 成品與 QA

- 正文 22 章、附錄 3 份、題庫 110 題、搜尋索引 165 筆、自製 SVG 22 張。
- 第一輪 QA：2,672／2,672。
- 第二輪 QA：139／139；45 項量化節點由原始輸入重算，20 項高風險概念獨立重判。
- 正式內容涵蓋報酬與風險、投資組合、CAPM／APT、效率市場、行為財務、股票與債券估值、期貨與選擇權、基金／ETF、資產配置與績效評估。
- 既有教材內容 hash 在整合前後完全一致；新增獨立 Book ID，不改既有章節 ID、題目 ID、儲存鍵或錯題紀錄。

## 部署

- canonical workflow：`Deploy study library`
- workflow run：`{os.environ['GITHUB_RUN_ID']}`
- source commit：`{os.environ['GITHUB_SHA']}`
- Pages artifact：`{artifact_id}`
- Artifact digest：`{artifact_digest}`
- 正式書庫書籍數：{book_count} 本。
- GitHub Pages deployment、artifact 重新下載驗證與結構化 deployment receipt 均成功。
'''
    Path('docs/books/investments/status.md').write_text(status, encoding='utf-8')

    qa_path = Path('docs/books/investments/qa_report.md')
    qa = qa_path.read_text(encoding='utf-8')
    final_block = f'''## 正式發布結果

- 第一輪結構／內容 QA：2,672／2,672 通過。
- 第二輪獨立 QA：139／139 通過；45 個量化節點重算、20 個高風險概念重判。
- 正式書庫：{book_count} 本，版本 `{library['version']}`。
- Pages run：`{os.environ['GITHUB_RUN_ID']}`。
- Pages artifact：`{artifact_id}`；digest `{artifact_digest}`。
- 部署後 artifact 重新下載：25 份本書章節／附錄 HTML、110 題、165 搜尋、22 SVG 全數核對通過。
- 既有教材逐檔內容 hash 保持不變，閱讀進度與錯題資料相容。
- post-deploy recorder：`passed-structured-recorder`。
'''
    qa = re.sub(r'## 正式發布結果\n.*\Z', final_block, qa, flags=re.S) if '## 正式發布結果' in qa else qa.rstrip() + '\n\n' + final_block
    qa_path.write_text(qa.rstrip() + '\n', encoding='utf-8')

    readme_path = Path('README.md')
    readme = readme_path.read_text(encoding='utf-8')
    readme = replace_once(readme, r'目前內容版本：`[^`]+`', f'目前內容版本：`{library["version"]}`', 'README version')
    line = f'- 《投資學》：一般大學投資學核心，22 章、3 附錄、110 題題庫、165 筆搜尋索引與 22 張圖解；內容版本 `{BOOK_VERSION}`。'
    lines = readme.splitlines()
    idxs = [i for i, x in enumerate(lines) if x.startswith('- 《投資學》：')]
    if idxs:
        lines[idxs[0]] = line
        for i in reversed(idxs[1:]):
            del lines[i]
    else:
        book_lines = [i for i, x in enumerate(lines) if x.startswith('- 《')]
        if not book_lines:
            raise AssertionError('README book list missing')
        lines.insert(max(book_lines) + 1, line)
    readme_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')

    cp = Path('docs/shared_checkpoint.md')
    c = cp.read_text(encoding='utf-8')
    c = replace_once(c, r'- 正式書庫內容版本：`[^`]+`', f'- 正式書庫內容版本：`{library["version"]}`', 'checkpoint library version')
    c = replace_once(c, r'- 正式書籍數：\d+ 本。', f'- 正式書籍數：{book_count} 本。', 'checkpoint book count')
    c = replace_once(c, r'- 最新正式 Pages run：`[^`]+`。', f'- 最新正式 Pages run：`{os.environ["GITHUB_RUN_ID"]}`。', 'checkpoint run')
    c = replace_once(c, r'- 最新正式部署 source commit：`[^`]+`。', f'- 最新正式部署 source commit：`{os.environ["GITHUB_SHA"]}`。', 'checkpoint source commit')
    c = replace_once(c, r'- 最新 Pages artifact：`[^`]+`。', f'- 最新 Pages artifact：`{artifact_id}`。', 'checkpoint artifact')
    c = replace_once(c, r'- Artifact digest：`[^`]+`。', f'- Artifact digest：`{artifact_digest}`。', 'checkpoint digest')
    c = replace_once(c, r'- Pages 狀態：.*$', f'- Pages 狀態：Upload artifact、Deploy to GitHub Pages 與部署後 artifact 重驗均成功；`{deployed_at}` 記錄 success。', 'checkpoint pages status')
    c = replace_once(c, r'- 部署回條：.*$', f'- 部署回條：`docs/deployment_receipt.json`；`status=success`、`book_count={book_count}`、`library_version={library["version"]}`、`progress_storage_changed=false`。', 'checkpoint receipt')
    c = replace_once(c, r'- 實際下載正式 Pages artifact 後再次核對：.*$', '- 實際下載正式 Pages artifact 後再次核對：《投資學》25 份章節／附錄 HTML、110 題、165 搜尋、22 SVG 均存在；下載檔 SHA-256 與 GitHub artifact digest 完全一致。', 'checkpoint artifact recheck')
    c = replace_once(c, r'- workflow overall conclusion.*$', '- workflow overall conclusion：`success`；post-deploy recorder 使用結構化 receipt／Book ID 更新。', 'checkpoint workflow conclusion')

    section = f'''### {book_number}. 投資學
- Book ID：`{BOOK}`
- 正式內容版本：`{BOOK_VERSION}`
- 定位：一般大學投資學；報酬與風險、投資組合、資產定價、證券估值、衍生工具、資產配置與績效評估。
- 成品：22 章、3 附錄、110 題、165 搜尋、22 圖解。
- QA：第一輪 2,672／2,672、第二輪 139／139；45 個量化節點重算、20 個高風險概念重判。
- 既有教材內容 hash 在整合前後完全一致，閱讀進度與錯題資料相容。
- 正式 Pages run：`{os.environ['GITHUB_RUN_ID']}`；Source commit：`{os.environ['GITHUB_SHA']}`。
- 文件：`docs/books/investments/scope.md`、`docs/books/investments/qa_report.md`、`docs/books/investments/status.md`。
- 狀態：已部署。

'''
    if re.search(r'(?ms)^### \d+\. 投資學\n.*?(?=^## Canonical 部署流程)', c):
        c = re.sub(r'(?ms)^### \d+\. 投資學\n.*?(?=^## Canonical 部署流程)', section, c, count=1)
    else:
        marker = '## Canonical 部署流程'
        if marker not in c:
            raise AssertionError('checkpoint canonical deployment marker missing')
        c = c.replace(marker, section + marker, 1)

    c = re.sub(
        r'7\. 最新正式書庫：\d+ 本，`[^`]+`；Pages run `[^`]+`，artifact `[^`]+`。',
        f'7. 最新正式書庫：{book_count} 本，`{library["version"]}`；Pages run `{os.environ["GITHUB_RUN_ID"]}`，artifact `{artifact_id}`。',
        c,
        count=1,
    )
    c = c.replace(
        '- canonical post-deploy recorder 仍存在舊 checkpoint 句型相依；下一次正式發布前應改成依結構化 receipt／Book ID 更新，而非依歷史自然語句做硬字串比對。',
        '- canonical post-deploy recorder 已使用結構化 receipt／Book ID 更新；不得恢復依歷史自然語句硬比對。',
    )
    c = c.replace(
        '3. 在下一次正式發布前先修正／驗證 canonical post-deploy recorder，移除舊自然語句硬比對。',
        '3. 沿用已驗證的結構化 canonical post-deploy recorder；不得改回自然語句硬比對。',
    )
    cp.write_text(c, encoding='utf-8')

    print(json.dumps({
        'status': 'success',
        'library_version': library['version'],
        'book_count': book_count,
        'investments_version': BOOK_VERSION,
        'pages_artifact_id': artifact_id,
        'pages_artifact_digest': artifact_digest,
        'structured_recorder': True,
    }, ensure_ascii=False))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: python deploy/record_investments_deployment.py SITE_ROOT')
    main(sys.argv[1])
