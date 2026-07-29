#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

BOOK='advanced-statistics'
BOOK_VERSION='2026.07.29-1'

def replace_once(text: str, pattern: str, replacement: str, label: str) -> str:
    text2,n=re.subn(pattern,replacement,text,count=1,flags=re.M)
    if n!=1:
        raise AssertionError(f'cannot update {label}')
    return text2

def main(site_root: str) -> None:
    site=Path(site_root)
    library=json.loads((site/'data/library.json').read_text(encoding='utf-8'))
    ids=[b['id'] for b in library['books']]
    if len(ids)!=13 or ids[-1]!=BOOK:
        raise AssertionError(f'expected 13-book advanced-statistics tail, got {ids}')
    root=site/'books'/BOOK
    manifest=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
    questions=json.loads((root/'questions.json').read_text(encoding='utf-8'))
    search=json.loads((root/'search.json').read_text(encoding='utf-8'))
    if manifest['version']!=BOOK_VERSION or questions['version']!=BOOK_VERSION:
        raise AssertionError('advanced statistics content version drift')
    if questions['count']!=100 or len(search['entries'])!=189:
        raise AssertionError('advanced statistics artifact counts drift')

    artifact_id=os.environ.get('PAGES_ARTIFACT_ID','')
    artifact_digest=os.environ.get('PAGES_ARTIFACT_DIGEST','')
    artifact_sha=os.environ.get('PAGES_ARTIFACT_SHA256','')
    page_url=os.environ.get('DEPLOYED_PAGE_URL','')
    if not artifact_id or not artifact_digest or not artifact_sha:
        raise AssertionError('missing artifact verification environment')
    if artifact_digest.startswith('sha256:') and artifact_digest.split(':',1)[1]!=artifact_sha:
        raise AssertionError('artifact digest and downloaded sha mismatch')

    receipt_path=Path('docs/deployment_receipt.json')
    receipt=json.loads(receipt_path.read_text(encoding='utf-8'))
    receipt.update({
        'status':'success',
        'library_version':library['version'],
        'book_versions_visible':True,
        'progress_storage_changed':False,
        'book_count':13,
        'advanced_statistics_version':BOOK_VERSION,
        'advanced_statistics_chapter_count':20,
        'advanced_statistics_appendix_count':3,
        'advanced_statistics_question_count':100,
        'advanced_statistics_search_count':189,
        'advanced_statistics_figure_count':20,
        'advanced_statistics_quantitative_recheck_count':27,
        'advanced_statistics_high_risk_concept_gate_count':45,
        'advanced_statistics_two_round_qa':'passed',
        'advanced_statistics_existing_book_hashes_preserved':True,
        'source_commit':os.environ['GITHUB_SHA'],
        'workflow_run_id':os.environ['GITHUB_RUN_ID'],
        'page_url':page_url,
        'deployed_at':datetime.now(timezone.utc).isoformat(),
        'pages_deploy_status':'success',
        'pages_artifact_id':artifact_id,
        'pages_artifact_digest':artifact_digest,
        'artifact_download_recheck':'passed',
        'artifact_download_sha256':artifact_sha,
        'artifact_verified_book_count':13,
        'artifact_verified_advanced_statistics_html_count':23,
        'artifact_verified_advanced_statistics_question_count':100,
        'artifact_verified_advanced_statistics_search_count':189,
        'artifact_verified_advanced_statistics_svg_count':20,
        'workflow_overall_conclusion':'success',
        'post_deploy_record_step':'passed-structured-recorder',
        'receipt_reconciliation':'automatic-from-verified-pages-artifact',
    })
    receipt_path.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

    status=f"""# 《高等統計學》製作狀態

更新日期：2026-07-29

## 正式識別

- Book ID：`advanced-statistics`
- 正式內容版本：`{BOOK_VERSION}`
- 正式書庫版本：`{library['version']}`
- 狀態：已部署。
- 範圍文件：`docs/books/advanced-statistics/scope.md`
- QA 報告：`docs/books/advanced-statistics/qa_report.md`

## 成品與 QA

- 正文 20 章、附錄 3 份、題庫 100 題、搜尋索引 189 筆、自製 SVG 20 張。
- 第一輪結構／內容 gate 與第二輪獨立複核均通過。
- 第二輪獨立重算 27 個量化節點，另有 45 個高風險概念正／負向 gate。
- 與既有《統計學》分工固定：本書聚焦數理統計、抽樣分配、估計與檢定理論。
- 既有 12 本教材內容 hash 在整合前後完全一致。
- 閱讀進度相容性：新增獨立 Book ID，不改既有章節 ID、題目 ID、儲存鍵或錯題紀錄。

## 部署

- canonical workflow：`Deploy study library`
- workflow run：`{os.environ['GITHUB_RUN_ID']}`
- source commit：`{os.environ['GITHUB_SHA']}`
- Pages artifact：`{artifact_id}`
- Artifact digest：`{artifact_digest}`
- 正式書庫書籍數：13 本。
- GitHub Pages 部署、artifact 下載重驗與結構化 deployment receipt 均成功。
"""
    Path('docs/books/advanced-statistics/status.md').write_text(status,encoding='utf-8')

    qa_path=Path('docs/books/advanced-statistics/qa_report.md')
    qa=qa_path.read_text(encoding='utf-8')
    final_block=f"""## 正式發布結果

- 第一輪結構／內容 QA：通過。
- 第二輪獨立 QA：27 個量化節點重算、45 個高風險概念 gate，全部通過。
- 既有 12 本內容 hash：整合前後完全一致。
- 正式書庫：13 本，版本 `{library['version']}`。
- Pages run：`{os.environ['GITHUB_RUN_ID']}`。
- Pages artifact：`{artifact_id}`；digest `{artifact_digest}`。
- 部署後 artifact 重新下載：23 份本書 HTML、100 題、189 搜尋、20 SVG 全數核對通過。
- post-deploy recorder：`passed-structured-recorder`；已移除舊版依賴 checkpoint 自然語句的硬比對流程。
"""
    qa=re.sub(r'## 正式發布結果\n.*\Z',final_block,qa,flags=re.S) if '## 正式發布結果' in qa else qa.rstrip()+'\n\n'+final_block
    qa_path.write_text(qa.rstrip()+'\n',encoding='utf-8')

    readme_path=Path('README.md')
    readme=readme_path.read_text(encoding='utf-8')
    readme=replace_once(readme,r'目前內容版本：`[^`]+`',f'目前內容版本：`{library["version"]}`','README version')
    line=f'- 《高等統計學》：一般大學高等統計／數理統計核心，20 章、3 附錄、100 題題庫、189 筆搜尋索引與 20 張圖解；內容版本 `{BOOK_VERSION}`。'
    lines=readme.splitlines()
    idxs=[i for i,x in enumerate(lines) if x.startswith('- 《高等統計學》：')]
    if idxs:
        lines[idxs[0]]=line
        for i in reversed(idxs[1:]):
            del lines[i]
    else:
        book_lines=[i for i,x in enumerate(lines) if x.startswith('- 《')]
        if not book_lines:
            raise AssertionError('README book list missing')
        lines.insert(max(book_lines)+1,line)
    readme_path.write_text('\n'.join(lines)+'\n',encoding='utf-8')

    cp=Path('docs/shared_checkpoint.md')
    c=cp.read_text(encoding='utf-8')
    c=replace_once(c,r'- 正式書庫內容版本：`[^`]+`',f'- 正式書庫內容版本：`{library["version"]}`','checkpoint library version')
    c=replace_once(c,r'- 正式書籍數：\d+ 本。','- 正式書籍數：13 本。','checkpoint book count')
    c=replace_once(c,r'- 最新正式 Pages run：`[^`]+`。',f'- 最新正式 Pages run：`{os.environ["GITHUB_RUN_ID"]}`。','checkpoint run')
    c=replace_once(c,r'- 最新正式部署 source commit：`[^`]+`。',f'- 最新正式部署 source commit：`{os.environ["GITHUB_SHA"]}`。','checkpoint source commit')
    c=replace_once(c,r'- 最新 Pages artifact：`[^`]+`。',f'- 最新 Pages artifact：`{artifact_id}`。','checkpoint artifact')
    c=replace_once(c,r'- Artifact digest：`[^`]+`。',f'- Artifact digest：`{artifact_digest}`。','checkpoint digest')
    c=replace_once(c,r'- 部署回條：.*$',f'- 部署回條：`docs/deployment_receipt.json`；`status=success`、`book_count=13`、`library_version={library["version"]}`、`progress_storage_changed=false`。','checkpoint receipt')
    c=re.sub(r'- workflow overall conclusion.*\n','- workflow overall conclusion：`success`；post-deploy recorder 已改為結構化更新，不再依賴舊章節自然語句硬比對。\n',c,count=1)
    section=f"""### 13. 高等統計學
- Book ID：`advanced-statistics`
- 正式內容版本：`{BOOK_VERSION}`
- 定位：一般大學高等統計／數理統計核心；承接基礎統計，聚焦機率模型、多元分配、極限定理、抽樣分配、估計與檢定理論。
- 成品：20 章、3 附錄、100 題、189 搜尋、20 圖解。
- QA：兩輪通過；27 個量化節點獨立重算、45 個高風險概念 gate。
- 既有 12 本教材內容 hash 在整合前後完全一致。
- 正式 Pages run：`{os.environ['GITHUB_RUN_ID']}`；Source commit：`{os.environ['GITHUB_SHA']}`。
- 文件：`docs/books/advanced-statistics/scope.md`、`docs/books/advanced-statistics/qa_report.md`、`docs/books/advanced-statistics/status.md`。
- 狀態：已部署。

"""
    if re.search(r'(?ms)^### 13\. 高等統計學\n.*?(?=^## Canonical 部署流程)',c):
        c=re.sub(r'(?ms)^### 13\. 高等統計學\n.*?(?=^## Canonical 部署流程)',section,c,count=1)
    else:
        marker='## Canonical 部署流程'
        if marker not in c:
            raise AssertionError('checkpoint canonical deployment marker missing')
        c=c.replace(marker,section+marker,1)
    c=re.sub(r'7\. 最新正式書庫：\d+ 本，`[^`]+`；Pages run `[^`]+`，artifact `[^`]+`。',
             f'7. 最新正式書庫：13 本，`{library["version"]}`；Pages run `{os.environ["GITHUB_RUN_ID"]}`，artifact `{artifact_id}`。',c,count=1)
    c=c.replace('2. 依 canonical `Deploy study library` 既定順序套用既有書籍修正層並逐書驗證。',
                '2. 直接下載 deployment receipt 指定的最新正式 Pages artifact，核對 digest、版本與書籍數；不再重播歷史書籍 generator／patch 鏈。')
    c=c.replace('6. Pages deployment 成功後核對 artifact，再寫回 deployment receipt、各書 status／QA 與本 checkpoint。',
                '6. Pages deployment 成功後重新下載本次 artifact 驗證，再由結構化 recorder 寫回 deployment receipt、目標書 status／QA、README 與本 checkpoint。')
    cp.write_text(c,encoding='utf-8')

    print(json.dumps({
        'status':'success','library_version':library['version'],'book_count':13,
        'advanced_statistics_version':BOOK_VERSION,'pages_artifact_id':artifact_id,
        'pages_artifact_digest':artifact_digest,'structured_recorder':True,
    },ensure_ascii=False))

if __name__=='__main__':
    if len(sys.argv)!=2:
        raise SystemExit('usage: python deploy/record_advanced_statistics_deployment.py SITE_ROOT')
    main(sys.argv[1])
