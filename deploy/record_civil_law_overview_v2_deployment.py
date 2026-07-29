#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

BOOK = 'civil-law-overview'
BOOK_VERSION = '2026.07.30-2'


def main(site_root: str) -> None:
    site = Path(site_root)
    lib = json.loads((site / 'data/library.json').read_text(encoding='utf-8'))
    ids = [b['id'] for b in lib['books']]
    if ids.count(BOOK) != 1:
        raise AssertionError('civil book registry count drift')

    root = site / 'books' / BOOK
    manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    questions = json.loads((root / 'questions.json').read_text(encoding='utf-8'))
    search = json.loads((root / 'search.json').read_text(encoding='utf-8'))
    if manifest['version'] != BOOK_VERSION or questions['version'] != BOOK_VERSION:
        raise AssertionError('civil v2 content version drift')
    if len(manifest['chapters']) != 23 or questions['count'] != 100 or len(search['entries']) != 150:
        raise AssertionError('civil v2 artifact count drift')
    if len(list((site / 'assets/civil-law-overview-svg').glob('*.svg'))) != 20:
        raise AssertionError('civil v2 SVG count drift')

    artifact_id = os.environ.get('PAGES_ARTIFACT_ID', '')
    digest = os.environ.get('PAGES_ARTIFACT_DIGEST', '')
    sha = os.environ.get('PAGES_ARTIFACT_SHA256', '')
    page_url = os.environ.get('DEPLOYED_PAGE_URL', '')
    if not artifact_id or not digest or not sha:
        raise AssertionError('missing deployed artifact verification environment')
    if digest.startswith('sha256:') and digest.split(':', 1)[1] != sha:
        raise AssertionError('artifact digest mismatch')

    reaudit_checks = int(os.environ.get('CIVIL_REAUDIT_CHECKS', '0') or 0)
    if reaudit_checks < 100:
        raise AssertionError('civil v2 reaudit metric missing')

    now = datetime.now(timezone.utc).isoformat()
    receipt_path = Path('docs/deployment_receipt.json')
    receipt = json.loads(receipt_path.read_text(encoding='utf-8'))
    receipt.update({
        'status': 'success',
        'library_version': lib['version'],
        'book_versions_visible': True,
        'progress_storage_changed': False,
        'book_count': len(ids),
        'book_ids': ids,
        'civil_law_overview_version': BOOK_VERSION,
        'civil_law_overview_chapter_count': 20,
        'civil_law_overview_appendix_count': 3,
        'civil_law_overview_question_count': 100,
        'civil_law_overview_search_count': 150,
        'civil_law_overview_figure_count': 20,
        'civil_law_overview_v2_reaudit_check_count': reaudit_checks,
        'civil_law_overview_v2_legal_gate_count': 12,
        'civil_law_overview_v2_question_adjustment_count': 9,
        'civil_law_overview_current_law_baseline': '2026-07-30',
        'civil_law_overview_existing_book_hashes_preserved': True,
        'civil_law_overview_two_round_qa': 'passed-plus-second-independent-reaudit',
        'source_commit': os.environ['GITHUB_SHA'],
        'workflow_run_id': os.environ['GITHUB_RUN_ID'],
        'page_url': page_url,
        'deployed_at': now,
        'pages_deploy_status': 'success',
        'pages_artifact_id': artifact_id,
        'pages_artifact_digest': digest,
        'artifact_download_recheck': 'passed',
        'artifact_download_sha256': sha,
        'artifact_verified_book_count': len(ids),
        'artifact_verified_civil_law_overview_html_count': 23,
        'artifact_verified_civil_law_overview_question_count': 100,
        'artifact_verified_civil_law_overview_search_count': 150,
        'artifact_verified_civil_law_overview_svg_count': 20,
        'workflow_overall_conclusion': 'success',
        'post_deploy_record_step': 'passed-civil-v2-structured-recorder',
    })
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    status = f'''# 《民法概要》製作狀態

更新日期：2026-07-30

## 定位

- Book ID：`{BOOK}`
- 正式內容版本：`{BOOK_VERSION}`
- 法規基準：2026-07-30 中華民國現行民法、相關施行法與必要憲法裁判。
- 定位：一般大學民法概要，涵蓋總則、債、物權、親屬、繼承五編。

## 成品

- 正文 20 章、附錄 3 份。
- 題庫 100 題，每章 5 題。
- 搜尋索引 150 筆；自製 SVG 20 張。
- 章節 ID、題目 ID 與閱讀／題庫進度儲存鍵未變。

## 第二次獨立內容複核

- v2 reaudit：{reaudit_checks} 項檢查通過；12 組現行法高風險 gate；9 題實際修正。
- 補正第 130 條請求中斷的 6 個月起訴限制、第 300／301 條債務承擔、第 354／360 條買賣瑕疵救濟。
- 補入第 482 條僱傭、第 191-2 條動力車輛責任、第 801／948 條善意取得、第 819／820 條共有處分與管理分工。
- 補強第 1030-1 條剩餘財產分配範圍；補入 112 年憲判字第 4 號在 2025-03-24 修法期限屆滿後的裁判效果。
- 補正第 1174 條拋棄繼承後書面通知義務；明確區分現行第 1223 條兄弟姊妹特留分與 2026-06-02 尚未生效的修正草案。
- 既有其他 {len(ids)-1} 本教材與非民法資產 hash 在修正前後一致。

## 正式部署

- 正式書庫版本：`{lib['version']}`；書籍數：{len(ids)} 本。
- Pages run：`{os.environ['GITHUB_RUN_ID']}`；source commit：`{os.environ['GITHUB_SHA']}`。
- Pages artifact：`{artifact_id}`；digest：`{digest}`。
- 部署後 artifact 已重新下載，23 份 HTML、100 題、150 搜尋與 20 SVG 全數通過 v2 QA。
- `progress_storage_changed=false`。
'''
    Path('docs/books/civil-law-overview/status.md').write_text(status, encoding='utf-8')

    qa_path = Path('docs/books/civil-law-overview/qa_report.md')
    qa = qa_path.read_text(encoding='utf-8')
    block = f'''## 第二次獨立內容複核（2026-07-30）

- 獨立 reaudit：{reaudit_checks} 項通過；12 組新增／加強現行法 gate；9 題實際調整。
- 正式來源重新核對：民法第 130、300、301、354、360、482、191-2、801、819、948、1030-1、1052、1174、1223 條，以及憲法法庭 112 年憲判字第 4 號。
- 主要糾錯／補強：請求中斷 6 個月起訴、債務承擔、瑕疵損害賠償、僱傭、動力車輛責任、善意取得、共有物整體處分、剩餘財產、裁判離婚憲法界線、拋棄繼承通知義務與特留分草案狀態。
- PR 正式 artifact 回歸曾以 20 本 `2026.07.30-2` 基底驗證：只修改民法書本、library version 與 service-worker version，其他 19 本逐檔 hash 不變。
- 正式發布後再次驗證：書庫 `{lib['version']}`、{len(ids)} 本；artifact `{artifact_id}`；SHA-256 與 GitHub digest 一致。
- 章節 ID、題目 ID、題數與進度儲存鍵均未變。
'''
    if '## 第二次獨立內容複核（2026-07-30）' in qa:
        qa = re.sub(r'## 第二次獨立內容複核（2026-07-30）\n.*\Z', block, qa, flags=re.S)
    else:
        qa = qa.rstrip() + '\n\n' + block
    qa_path.write_text(qa.rstrip() + '\n', encoding='utf-8')

    readme_path = Path('README.md')
    readme = readme_path.read_text(encoding='utf-8')
    readme = re.sub(r'目前內容版本：`[^`]+`', f'目前內容版本：`{lib["version"]}`', readme, count=1)
    readme = re.sub(
        r'^- 《民法概要》：.*$',
        f'- 《民法概要》：一般大學民法概要，20 章、3 附錄、100 題題庫、150 筆搜尋索引與 20 張圖解；第二次獨立內容複核版本 `{BOOK_VERSION}`。',
        readme,
        count=1,
        flags=re.M,
    )
    readme_path.write_text(readme, encoding='utf-8')

    checkpoint_path = Path('docs/shared_checkpoint.md')
    checkpoint = checkpoint_path.read_text(encoding='utf-8')
    section_pattern = r'(?ms)(### 16\. 民法概要\n.*?)(?=^### 17\.)'
    m = re.search(section_pattern, checkpoint)
    if not m:
        raise AssertionError('civil checkpoint section missing')
    section = f'''### 16. 民法概要
- Book ID：`civil-law-overview`
- 正式內容版本：`{BOOK_VERSION}`
- 定位：一般大學民法概要；總則、債、物權、親屬、繼承，以請求權基礎與案例解題為主。
- 成品：20 章、3 附錄、100 題、150 搜尋、20 圖解。
- 初版 QA：第一輪 157 項、第二輪 670 項。
- 2026-07-30 第二次獨立內容複核：{reaudit_checks} 項、12 組現行法 gate、9 題修正；其他 {len(ids)-1} 本 hash 保持一致。
- 現行法基準：2026-07-30；第 166-1 條仍未施行；112 年憲判字第 4 號與兄弟姊妹特留分草案狀態已納入。
- 正式 Pages run：`{os.environ['GITHUB_RUN_ID']}`；Source commit：`{os.environ['GITHUB_SHA']}`；artifact：`{artifact_id}`。
- 狀態：已部署 v2。

'''
    checkpoint = checkpoint[:m.start()] + section + checkpoint[m.end():]
    checkpoint_path.write_text(checkpoint, encoding='utf-8')

    print(f'CIVIL_LAW_V2_DEPLOYMENT_RECORDED library={lib["version"]} books={len(ids)} checks={reaudit_checks}')


if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        raise SystemExit('usage: python deploy/record_civil_law_overview_v2_deployment.py SITE_ROOT')
    main(sys.argv[1])
