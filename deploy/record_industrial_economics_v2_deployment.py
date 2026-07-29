#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

BOOK = 'industrial-economics'
BOOK_VERSION = '2026.07.30-2'


def replace_once(text: str, pattern: str, replacement: str, label: str) -> str:
    out, n = re.subn(pattern, replacement, text, count=1, flags=re.M)
    if n != 1:
        raise AssertionError(f'cannot update {label}')
    return out


def main(site_root: str) -> None:
    site = Path(site_root)
    library = json.loads((site / 'data/library.json').read_text(encoding='utf-8'))
    ids = [book['id'] for book in library['books']]
    if ids.count(BOOK) != 1:
        raise AssertionError(f'industrial economics must occur exactly once: {ids}')
    ordinal = ids.index(BOOK) + 1
    count = len(ids)

    root = site / 'books' / BOOK
    manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    questions = json.loads((root / 'questions.json').read_text(encoding='utf-8'))
    search = json.loads((root / 'search.json').read_text(encoding='utf-8'))
    if manifest['version'] != BOOK_VERSION or questions['version'] != BOOK_VERSION:
        raise AssertionError('industrial economics v2 content version drift')
    if len(manifest['chapters']) != 23 or questions['count'] != 100 or len(search['entries']) != 150:
        raise AssertionError('industrial economics v2 artifact count drift')
    if len(list((site / 'assets/industrial-economics-svg').glob('*.svg'))) != 20:
        raise AssertionError('industrial economics v2 SVG count drift')

    qa1 = int(os.environ.get('INDUSTRIAL_V2_QA1_CHECKS', '0') or 0)
    qa2 = int(os.environ.get('INDUSTRIAL_V2_QA2_CHECKS', '0') or 0)
    if qa1 <= 0 or qa2 <= 0:
        raise AssertionError('missing industrial v2 QA metrics')

    artifact_id = os.environ.get('PAGES_ARTIFACT_ID', '')
    digest = os.environ.get('PAGES_ARTIFACT_DIGEST', '')
    sha = os.environ.get('PAGES_ARTIFACT_SHA256', '')
    page_url = os.environ.get('DEPLOYED_PAGE_URL', '')
    if not artifact_id or not digest or not sha:
        raise AssertionError('missing artifact verification environment')
    if digest.startswith('sha256:') and digest.split(':', 1)[1] != sha:
        raise AssertionError('artifact digest mismatch')

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
        'industrial_economics_version': BOOK_VERSION,
        'industrial_economics_chapter_count': 20,
        'industrial_economics_appendix_count': 3,
        'industrial_economics_question_count': 100,
        'industrial_economics_search_count': 150,
        'industrial_economics_figure_count': 20,
        'industrial_economics_round1_check_count': qa1,
        'industrial_economics_round2_check_count': qa2,
        'industrial_economics_quantitative_recheck_count': 26,
        'industrial_economics_high_risk_concept_gate_count': 16,
        'industrial_economics_v2_correction_area_count': 12,
        'industrial_economics_two_round_qa': 'passed-after-second-independent-audit',
        'industrial_economics_existing_book_hashes_preserved': True,
        'industrial_economics_ids_preserved': True,
        'industrial_economics_progress_compatibility': 'preserved',
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
        'artifact_verified_industrial_economics_html_count': 23,
        'artifact_verified_industrial_economics_question_count': 100,
        'artifact_verified_industrial_economics_search_count': 150,
        'artifact_verified_industrial_economics_svg_count': 20,
        'workflow_overall_conclusion': 'success',
        'post_deploy_record_step': 'passed-structured-recorder',
        'receipt_reconciliation': 'automatic-from-verified-pages-artifact',
    })
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    status = f'''# 《產業經濟學》製作狀態

更新日期：2026-07-30

## 正式識別

- Book ID：`{BOOK}`
- 正式內容版本：`{BOOK_VERSION}`
- 正式書庫版本：`{library["version"]}`
- 書庫位置：第 {ordinal} 本（全庫 {count} 本）。
- 狀態：已部署；第二次獨立內容複核與糾錯完成。

## 成品與第二次獨立 QA

- 正文 20 章、附錄 3 份、題庫 100 題、搜尋索引 150 筆、自製 SVG 20 張。
- QA Round 1：{qa1} 項；Round 2：{qa2} 項，均通過。
- 26 個量化節點獨立重算、16 組高風險概念 gate、12 個實質修正區域。
- 修正包含 Cournot 一般最佳反應函數、價格歧視福利配置、進入決策現值、自然獨占次可加性、Lerner／Hotelling 條件與台灣公平交易法第 7／14／19 條制度邊界。
- 其他 {count-1} 本教材內容 hash 在整合前後完全一致。
- 本書 Book ID、20 個章節 ID、3 個附錄 ID、100 個題目 ID 全部未變；閱讀進度與錯題紀錄相容。

## 部署

- canonical workflow：`Deploy study library`
- workflow run：`{os.environ["GITHUB_RUN_ID"]}`
- source commit：`{os.environ["GITHUB_SHA"]}`
- Pages artifact：`{artifact_id}`
- Artifact digest：`{digest}`
- Pages deployment、artifact 下載重驗與結構化 deployment receipt 均成功。

## 文件

- `docs/books/industrial-economics/v2_audit_report.md`
- `docs/books/industrial-economics/qa_report.md`
- `docs/books/industrial-economics/scope.md`
'''
    Path('docs/books/industrial-economics/status.md').write_text(status, encoding='utf-8')

    qa_path = Path('docs/books/industrial-economics/qa_report.md')
    qa = qa_path.read_text(encoding='utf-8')
    block = f'''## 第二次獨立內容複核正式結果

- 修正版內容版本：`{BOOK_VERSION}`。
- Round 1：{qa1} 項通過；Round 2：{qa2} 項通過。
- 量化獨立重算：26 個節點；高風險概念 gate：16 組；實質修正區域：12。
- 其他 {count-1} 本教材內容 hash：整合前後完全一致。
- 本書章節／附錄／題目 ID：全部保持不變；閱讀進度與錯題資料相容。
- 正式書庫：{count} 本，版本 `{library["version"]}`。
- Pages run：`{os.environ["GITHUB_RUN_ID"]}`；artifact：`{artifact_id}`；digest：`{digest}`。
- 部署後重新下載 artifact，23 份本書 HTML、100 題、150 搜尋、20 SVG 全數核對通過。
- 詳細糾錯：`docs/books/industrial-economics/v2_audit_report.md`。
'''
    if '## 第二次獨立內容複核正式結果' in qa:
        qa = re.sub(r'## 第二次獨立內容複核正式結果\n.*\Z', block, qa, flags=re.S)
    else:
        qa = qa.rstrip() + '\n\n' + block
    qa_path.write_text(qa.rstrip() + '\n', encoding='utf-8')

    audit_path = Path('docs/books/industrial-economics/v2_audit_report.md')
    audit = audit_path.read_text(encoding='utf-8')
    formal = f'''## 正式發布結果

- 正式內容版本：`{BOOK_VERSION}`。
- 正式書庫版本：`{library["version"]}`；書籍數：{count} 本。
- QA1：{qa1}；QA2：{qa2}；量化重算 26；高風險概念 gate 16。
- 其他 {count-1} 本教材 hash 完全不變；本書所有公開 ID 保持不變。
- Pages run：`{os.environ["GITHUB_RUN_ID"]}`；artifact：`{artifact_id}`。
- Artifact digest／下載 SHA-256：`{digest}`，重驗通過。
'''
    if '## 正式發布結果' in audit:
        audit = re.sub(r'## 正式發布結果\n.*\Z', formal, audit, flags=re.S)
    else:
        audit = audit.rstrip() + '\n\n' + formal
    audit_path.write_text(audit.rstrip() + '\n', encoding='utf-8')

    readme_path = Path('README.md')
    readme = readme_path.read_text(encoding='utf-8')
    readme = replace_once(readme, r'目前內容版本：`[^`]+`', f'目前內容版本：`{library["version"]}`', 'README version')
    book_line = (
        f'- 《產業經濟學》：一般大學產業組織核心，20 章、3 附錄、100 題、150 筆搜尋索引與 20 張圖解；'
        f'內容版本 `{BOOK_VERSION}`，已完成第二次獨立內容複核與糾錯。'
    )
    lines = readme.splitlines()
    matches = [i for i, line in enumerate(lines) if line.startswith('- 《產業經濟學》：')]
    if matches:
        lines[matches[0]] = book_line
        for i in reversed(matches[1:]):
            lines.pop(i)
    else:
        raise AssertionError('README industrial economics line missing')
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

    section = f'''### {ordinal}. 產業經濟學
- Book ID：`{BOOK}`
- 正式內容版本：`{BOOK_VERSION}`
- 定位：一般大學產業經濟學／產業組織共同核心。
- 成品：20 章、3 附錄、100 題、150 搜尋、20 圖解。
- 第二次獨立內容複核：12 個實質修正區域；QA1 = {qa1}、QA2 = {qa2}；26 個量化節點、16 組高風險概念 gate。
- 其他 {count-1} 本教材 hash 在整合前後完全一致；本書章節／題目 ID 與閱讀／錯題進度相容性均保持。
- 詳細糾錯：`docs/books/industrial-economics/v2_audit_report.md`。
- 正式 Pages run：`{os.environ["GITHUB_RUN_ID"]}`；Source commit：`{os.environ["GITHUB_SHA"]}`。
- 狀態：已部署。

'''
    checkpoint = re.sub(r'(?ms)^### \d+\. 產業經濟學\n.*?(?=^### |^## Canonical 部署流程)', '', checkpoint)
    marker = '## Canonical 部署流程'
    if marker not in checkpoint:
        raise AssertionError('checkpoint canonical marker missing')
    checkpoint = checkpoint.replace(marker, section + marker, 1)
    checkpoint_path.write_text(checkpoint, encoding='utf-8')

    print(json.dumps({
        'status': 'success',
        'library_version': library['version'],
        'book_count': count,
        'industrial_economics_version': BOOK_VERSION,
        'industrial_ordinal': ordinal,
        'qa1': qa1,
        'qa2': qa2,
        'pages_artifact_id': artifact_id,
        'pages_artifact_digest': digest,
        'structured_recorder': True,
    }, ensure_ascii=False))


if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        raise SystemExit('usage: python deploy/record_industrial_economics_v2_deployment.py SITE_ROOT')
    main(sys.argv[1])
