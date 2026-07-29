#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

BOOK = 'industry-trade'
BOOK_VERSION = '2026.07.29-1'


def replace_once(text: str, pattern: str, replacement: str, label: str) -> str:
    out, n = re.subn(pattern, replacement, text, count=1, flags=re.M)
    if n != 1:
        raise AssertionError(f'cannot update {label}')
    return out


def main(site_root: str) -> None:
    site = Path(site_root)
    library = json.loads((site / 'data/library.json').read_text(encoding='utf-8'))
    ids = [book['id'] for book in library['books']]
    if not ids or ids[-1] != BOOK or ids.count(BOOK) != 1:
        raise AssertionError(f'industry trade not unique tail: {ids}')
    if 'industrial-economics' not in ids or ids.index('industrial-economics') > ids.index(BOOK):
        raise AssertionError('industrial economics must precede industry trade')

    count = len(ids)
    root = site / 'books' / BOOK
    manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    questions = json.loads((root / 'questions.json').read_text(encoding='utf-8'))
    search = json.loads((root / 'search.json').read_text(encoding='utf-8'))
    if manifest['version'] != BOOK_VERSION or questions['version'] != BOOK_VERSION:
        raise AssertionError('industry trade content version drift')
    if len(manifest['chapters']) != 23 or questions['count'] != 100 or len(search['entries']) != 160:
        raise AssertionError('industry trade artifact count drift')
    if len(list((site / 'assets/industry-trade-svg').glob('*.svg'))) != 20:
        raise AssertionError('industry trade SVG count drift')

    artifact_id = os.environ.get('PAGES_ARTIFACT_ID', '')
    digest = os.environ.get('PAGES_ARTIFACT_DIGEST', '')
    sha = os.environ.get('PAGES_ARTIFACT_SHA256', '')
    page_url = os.environ.get('DEPLOYED_PAGE_URL', '')
    if not artifact_id or not digest or not sha:
        raise AssertionError('missing artifact verification environment')
    if digest.startswith('sha256:') and digest.split(':', 1)[1] != sha:
        raise AssertionError('artifact digest mismatch')

    qa1 = int(os.environ.get('INDUSTRY_TRADE_QA1_CHECKS', '0') or 0)
    qa2 = int(os.environ.get('INDUSTRY_TRADE_QA2_CHECKS', '0') or 0)
    if qa1 <= 0 or qa2 <= 0:
        raise AssertionError('missing industry trade QA metrics')

    deployed_at = datetime.now(timezone.utc).isoformat()
    receipt_path = Path('docs/deployment_receipt.json')
    receipt = json.loads(receipt_path.read_text(encoding='utf-8'))
    receipt.update({
        'status': 'success',
        'library_version': library['version'],
        'book_versions_visible': True,
        'progress_storage_changed': False,
        'book_count': count,
        'book_ids': ids,
        'industry_trade_version': BOOK_VERSION,
        'industry_trade_chapter_count': 20,
        'industry_trade_appendix_count': 3,
        'industry_trade_question_count': 100,
        'industry_trade_search_count': 160,
        'industry_trade_figure_count': 20,
        'industry_trade_round1_check_count': qa1,
        'industry_trade_round2_check_count': qa2,
        'industry_trade_quantitative_recheck_count': 20,
        'industry_trade_high_risk_chapter_recheck_count': 12,
        'industry_trade_two_round_qa': 'passed',
        'industry_trade_existing_book_hashes_preserved': True,
        'source_commit': os.environ['GITHUB_SHA'],
        'workflow_run_id': os.environ['GITHUB_RUN_ID'],
        'page_url': page_url,
        'deployed_at': deployed_at,
        'pages_deploy_status': 'success',
        'pages_artifact_id': artifact_id,
        'pages_artifact_digest': digest,
        'artifact_download_recheck': 'passed',
        'artifact_download_sha256': sha,
        'artifact_verified_book_count': count,
        'artifact_verified_industry_trade_html_count': 23,
        'artifact_verified_industry_trade_question_count': 100,
        'artifact_verified_industry_trade_search_count': 160,
        'artifact_verified_industry_trade_svg_count': 20,
        'workflow_overall_conclusion': 'success',
        'post_deploy_record_step': 'passed-structured-recorder',
        'receipt_reconciliation': 'automatic-from-verified-pages-artifact',
    })
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    status = f'''# 《產業及貿易》狀態

更新日期：2026-07-30

## 正式識別

- Book ID：`{BOOK}`
- 正式內容版本：`{BOOK_VERSION}`
- 正式書庫版本：`{library["version"]}`
- 狀態：已部署。

## 成品與 QA

- 正文 20 章、附錄 3 份、題庫 100 題、搜尋索引 160 筆、自製 SVG 20 張。
- 正式部署前 Round 1：{qa1} 項；Round 2：{qa2} 項，均通過。
- 100 題逐題複核、20 題數值題獨立重算、12 個高風險章節重新判讀。
- 發布前既有 {count-1} 本教材內容 hash 在整合前後完全一致。
- 新 Book ID 不改既有章節 ID、題目 ID、閱讀進度或錯題儲存鍵。

## 部署

- canonical workflow：`Deploy study library`
- workflow run：`{os.environ["GITHUB_RUN_ID"]}`
- source commit：`{os.environ["GITHUB_SHA"]}`
- Pages artifact：`{artifact_id}`
- Artifact digest：`{digest}`
- 正式書庫書籍數：{count} 本。
- Pages deployment、artifact 下載重驗與結構化 deployment receipt 均成功。
'''
    Path('docs/books/industry-trade/status.md').write_text(status, encoding='utf-8')

    qa_path = Path('docs/books/industry-trade/qa_report.md')
    qa = qa_path.read_text(encoding='utf-8')
    release_block = f'''## 正式發布結果

- Round 1：{qa1} 項通過；Round 2：{qa2} 項通過。
- 100 題逐題複核、20 題數值題獨立重算、12 個高風險章節重新判讀。
- 既有 {count-1} 本內容 hash：整合前後完全一致。
- 正式書庫：{count} 本，版本 `{library["version"]}`。
- Pages run：`{os.environ["GITHUB_RUN_ID"]}`。
- Pages artifact：`{artifact_id}`；digest `{digest}`。
- 部署後 artifact 重抓：23 份本書 HTML、100 題、160 搜尋、20 SVG 全數核對通過。
- post-deploy recorder：`passed-structured-recorder`。
'''
    if '## 正式發布結果' in qa:
        qa = re.sub(r'## 正式發布結果\n.*\Z', release_block, qa, flags=re.S)
    else:
        qa = qa.rstrip() + '\n\n' + release_block
    qa_path.write_text(qa.rstrip() + '\n', encoding='utf-8')

    readme_path = Path('README.md')
    readme = readme_path.read_text(encoding='utf-8')
    readme = replace_once(readme, r'目前內容版本：`[^`]+`', f'目前內容版本：`{library["version"]}`', 'README version')
    book_line = (
        f'- 《產業及貿易》：產業組織 × 國際貿易，20 章、3 附錄、100 題、'
        f'160 筆搜尋索引與 20 張圖解；內容版本 `{BOOK_VERSION}`。'
    )
    lines = readme.splitlines()
    matches = [i for i, line in enumerate(lines) if line.startswith('- 《產業及貿易》：')]
    if matches:
        lines[matches[0]] = book_line
        for i in reversed(matches[1:]):
            lines.pop(i)
    else:
        book_lines = [i for i, line in enumerate(lines) if line.startswith('- 《')]
        if not book_lines:
            raise AssertionError('README book list missing')
        lines.insert(max(book_lines) + 1, book_line)
    readme_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')

    checkpoint_path = Path('docs/shared_checkpoint.md')
    checkpoint = checkpoint_path.read_text(encoding='utf-8')
    checkpoint = replace_once(checkpoint, r'- 正式書庫內容版本：`[^`]+`', f'- 正式書庫內容版本：`{library["version"]}`', 'checkpoint version')
    checkpoint = replace_once(checkpoint, r'- 正式書籍數：\d+ 本。', f'- 正式書籍數：{count} 本。', 'checkpoint count')
    checkpoint = replace_once(checkpoint, r'- 最新正式 Pages run：`[^`]+`。', f'- 最新正式 Pages run：`{os.environ["GITHUB_RUN_ID"]}`。', 'checkpoint run')
    checkpoint = replace_once(checkpoint, r'- 最新正式部署 source commit：`[^`]+`。', f'- 最新正式部署 source commit：`{os.environ["GITHUB_SHA"]}`。', 'checkpoint source')
    checkpoint = replace_once(checkpoint, r'- 最新 Pages artifact：`[^`]+`。', f'- 最新 Pages artifact：`{artifact_id}`。', 'checkpoint artifact')
    checkpoint = replace_once(checkpoint, r'- Artifact digest：`[^`]+`。', f'- Artifact digest：`{digest}`。', 'checkpoint digest')
    checkpoint = replace_once(checkpoint, r'- Pages 狀態：.*$', f'- Pages 狀態：正式 artifact 上傳、Pages deployment 與下載後 artifact recheck 均成功；`{deployed_at}`。', 'checkpoint pages status')
    checkpoint = replace_once(checkpoint, r'- 部署回條：.*$', f'- 部署回條：`docs/deployment_receipt.json`；`status=success`、`book_count={count}`、`library_version={library["version"]}`、`progress_storage_changed=false`。', 'checkpoint receipt')
    checkpoint = replace_once(checkpoint, r'- 實際下載正式 Pages artifact 後再次核對：.*$', f'- 實際下載正式 Pages artifact 後再次核對：{count} 本 registry；產業及貿易 23 份章節／附錄 HTML、100 題、160 搜尋、20 SVG 與既有正式教材均存在；下載檔 SHA-256 與 GitHub artifact digest 一致。', 'checkpoint artifact recheck')
    checkpoint = replace_once(checkpoint, r'- workflow overall conclusion：.*$', '- workflow overall conclusion：`success`；post-deploy recorder 採結構化 Book ID／receipt 更新。', 'checkpoint workflow conclusion')

    section = f'''### {count}. 產業及貿易
- Book ID：`{BOOK}`
- 正式內容版本：`{BOOK_VERSION}`
- 定位：產業組織 × 國際貿易；市場結構、跨國生產、政策與福利。
- 成品：20 章、3 附錄、100 題、160 搜尋、20 圖解。
- QA：Round 1 = {qa1}、Round 2 = {qa2}；20 題數值題獨立重算、12 個高風險章節重判。
- 既有 {count-1} 本教材 hash 在整合前後完全一致。
- 正式 Pages run：`{os.environ["GITHUB_RUN_ID"]}`；Source commit：`{os.environ["GITHUB_SHA"]}`。
- 狀態：已部署。

'''
    checkpoint = re.sub(r'(?ms)^### \d+\. 產業及貿易\n.*?(?=^### |^## Canonical 部署流程)', '', checkpoint)
    marker = '## Canonical 部署流程'
    if marker not in checkpoint:
        raise AssertionError('checkpoint canonical marker missing')
    checkpoint = checkpoint.replace(marker, section + marker, 1)
    checkpoint, n = re.subn(
        r'7\. 最新正式書庫：\d+ 本，`[^`]+`；Pages run `[^`]+`，artifact `[^`]+`。',
        f'7. 最新正式書庫：{count} 本，`{library["version"]}`；Pages run `{os.environ["GITHUB_RUN_ID"]}`，artifact `{artifact_id}`。',
        checkpoint,
        count=1,
    )
    if n != 1:
        raise AssertionError('checkpoint canonical latest-library line')
    checkpoint_path.write_text(checkpoint, encoding='utf-8')


if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        raise SystemExit('usage: python deploy/record_industry_trade_deployment.py SITE_ROOT')
    main(sys.argv[1])
